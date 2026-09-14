"""Paired-seat, fixed-seed head-to-head arena.

    uv run python scripts/arena.py --a main.py --b starter --seeds 0-9
    uv run python scripts/arena.py --a main.py --b opponents/tape.py --seeds 100-119 --jobs 4

Every seed is played from both seats unless --one-seat. Reports W-L-T, win rate, mean bank
margin, and any non-DONE status. Every game is appended to results/arena.csv.

The ladder scores wins only, so win rate is the number that matters. Mean margin is a
diagnostic.
"""

from __future__ import annotations

import argparse
import csv
import statistics
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "arena.csv"
BUILTINS = {"starter", "random", "pass"}
FIELDS = [
    "ts",
    "a",
    "b",
    "seed",
    "seat",
    "steps",
    "me",
    "opp",
    "result",
    "me_status",
    "opp_status",
    "secs",
]


def parse_seeds(spec: str) -> list[int]:
    seeds: list[int] = []
    for part in spec.split(","):
        if "-" in part:
            lo, hi = part.split("-")
            seeds.extend(range(int(lo), int(hi) + 1))
        else:
            seeds.append(int(part))
    return seeds


def resolve(spec: str) -> str:
    if spec in BUILTINS:
        return spec
    path = Path(spec)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        raise SystemExit(f"agent not found: {spec}")
    return str(path)


def play(task: tuple[str, str, int, int, int]) -> dict:
    a, b, seed, seat, steps = task
    from kenv import import_ke

    env = import_ke().make(
        "kaggriculture", configuration={"episodeSteps": steps, "seed": seed}, debug=False
    )
    t0 = time.time()
    env.run([a, b] if seat == 0 else [b, a])
    final = env.steps[-1]
    bank = [s.reward if s.reward is not None else 0.0 for s in final]
    status = [str(s.status) for s in final]
    me, opp = (0, 1) if seat == 0 else (1, 0)
    result = "W" if bank[me] > bank[opp] else "L" if bank[me] < bank[opp] else "T"
    return {
        "seed": seed,
        "seat": seat,
        "steps": steps,
        "me": bank[me],
        "opp": bank[opp],
        "result": result,
        "me_status": status[me],
        "opp_status": status[opp],
        "secs": round(time.time() - t0, 1),
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--a", default="main.py", help="agent under test (file or builtin)")
    ap.add_argument("--b", default="starter", help="opponent (file or builtin)")
    ap.add_argument("--seeds", default="0-4")
    ap.add_argument("--steps", type=int, default=720)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--one-seat", action="store_true", help="only play A in seat 0")
    args = ap.parse_args()

    a, b = resolve(args.a), resolve(args.b)
    seats = (0,) if args.one_seat else (0, 1)
    tasks = [(a, b, seed, seat, args.steps) for seed in parse_seeds(args.seeds) for seat in seats]

    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            rows = list(pool.map(play, tasks))
    else:
        rows = [play(t) for t in tasks]

    ts = datetime.now(UTC).isoformat(timespec="seconds")
    RESULTS.parent.mkdir(exist_ok=True)
    new_file = not RESULTS.exists()
    with RESULTS.open("a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        for row in rows:
            writer.writerow({"ts": ts, "a": args.a, "b": args.b, **row})

    for row in rows:
        flag = (
            "" if row["me_status"] == "DONE" and row["opp_status"] == "DONE" else "  <-- not DONE"
        )
        print(
            f"seed {row['seed']:>6} seat {row['seat']}  {row['result']}  "
            f"{row['me']:>9.0f} vs {row['opp']:>9.0f}  ({row['secs']}s){flag}"
        )

    wins = sum(r["result"] == "W" for r in rows)
    losses = sum(r["result"] == "L" for r in rows)
    ties = sum(r["result"] == "T" for r in rows)
    errors = sum(r["me_status"] != "DONE" for r in rows)
    margin = statistics.mean(r["me"] - r["opp"] for r in rows)
    print(f"\n{args.a} vs {args.b} | seeds {args.seeds} | {len(rows)} games")
    print(
        f"W-L-T {wins}-{losses}-{ties}  win rate {wins / len(rows):.0%}  "
        f"mean bank {statistics.mean(r['me'] for r in rows):.0f} vs "
        f"{statistics.mean(r['opp'] for r in rows):.0f}  mean margin {margin:+.0f}  "
        f"errors {errors}  ({statistics.mean(r['secs'] for r in rows):.1f} s/game)"
    )


if __name__ == "__main__":
    main()
