"""Paired-seat, fixed-seed head-to-head arena.

    uv run python scripts/arena.py --a main.py --b starter --seeds 0-9
    uv run python scripts/arena.py --a main.py --b opponents/ref/rancher_rita.py --seeds 100-119 --jobs 4
    uv run python scripts/arena.py --a main.py --b "tape:opponents/top10/majkel1337_*.json" --jobs 4

Opponents are builtin names, agent files, or `tape:<glob>` recordings exported by
scripts/top10/export_tapes.py. A tape plays its recorded actions in its recorded seat on its
recorded seed, so the recorded bank of the seat we take over is a ground-truth reference.
Pass --tape-both-seats to also play each tape from the other seat.

Every game is appended to results/arena.csv. The ladder scores wins only, so win rate is the
number that matters; mean margin is a diagnostic.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
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
    "ref_me",
    "ref_opp",
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


def tape_files(spec: str) -> list[Path]:
    pattern = spec[len("tape:") :]
    files = sorted(Path(p) for p in glob.glob(str(ROOT / pattern))) or sorted(
        Path(p) for p in glob.glob(pattern)
    )
    if not files:
        raise SystemExit(f"no tape files match {pattern}")
    return files


def build_tasks(args) -> list[dict]:
    a = resolve(args.a)
    if args.b.startswith("tape:"):
        tasks = []
        for path in tape_files(args.b):
            tape = json.loads(path.read_text(encoding="utf-8"))
            seats = [1 - tape["tape_seat"]]
            if args.tape_both_seats:
                seats.append(tape["tape_seat"])
            for seat in seats:
                tasks.append(
                    {
                        "a": a,
                        "b": str(path),
                        "b_kind": "tape",
                        "seed": tape["seed"],
                        "seat": seat,
                        "steps": args.steps,
                        "tape_seat": tape["tape_seat"],
                    }
                )
        return tasks
    b = resolve(args.b)
    seats = (0,) if args.one_seat else (0, 1)
    return [
        {"a": a, "b": b, "b_kind": "agent", "seed": seed, "seat": seat, "steps": args.steps}
        for seed in parse_seeds(args.seeds)
        for seat in seats
    ]


def play(task: dict) -> dict:
    from kenv import import_ke

    ke = import_ke()
    seat, seed, steps = task["seat"], task["seed"], task["steps"]
    ref_me = ref_opp = None
    if task["b_kind"] == "tape":
        from agent.tape import Tape

        tape = json.loads(Path(task["b"]).read_text(encoding="utf-8"))
        opp_seat = 1 - seat
        opponent = Tape(tape["actions"][tape["tape_seat"]])
        ref_opp = tape["banks"][tape["tape_seat"]]
        ref_me = tape["banks"][1 - tape["tape_seat"]]
    else:
        opponent = task["b"]
        opp_seat = 1 - seat
    order = [None, None]
    order[seat] = task["a"]
    order[opp_seat] = opponent
    env = ke.make("kaggriculture", configuration={"episodeSteps": steps, "seed": seed}, debug=False)
    t0 = time.time()
    env.run(order)
    final = env.steps[-1]
    bank = [s.reward if s.reward is not None else 0.0 for s in final]
    status = [str(s.status) for s in final]
    result = "W" if bank[seat] > bank[opp_seat] else "L" if bank[seat] < bank[opp_seat] else "T"
    return {
        "seed": seed,
        "seat": seat,
        "steps": steps,
        "me": bank[seat],
        "opp": bank[opp_seat],
        "result": result,
        "me_status": status[seat],
        "opp_status": status[opp_seat],
        "ref_me": ref_me,
        "ref_opp": ref_opp,
        "secs": round(time.time() - t0, 1),
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--a", default="main.py", help="agent under test (file or builtin)")
    ap.add_argument("--b", default="starter", help="opponent: builtin, agent file, or tape:<glob>")
    ap.add_argument("--seeds", default="0-4", help="ignored for tape opponents")
    ap.add_argument("--steps", type=int, default=720)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--one-seat", action="store_true", help="only play A in seat 0")
    ap.add_argument(
        "--tape-both-seats", action="store_true", help="also play tapes from the other seat"
    )
    args = ap.parse_args()

    tasks = build_tasks(args)
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
        for task, row in zip(tasks, rows):
            writer.writerow(
                {
                    "ts": ts,
                    "a": args.a,
                    "b": Path(task["b"]).name if task["b_kind"] == "tape" else args.b,
                    **row,
                }
            )

    for task, row in zip(tasks, rows):
        flag = (
            "" if row["me_status"] == "DONE" and row["opp_status"] == "DONE" else "  <-- not DONE"
        )
        ref = (
            f"  (recorded {row['ref_me']:.0f} vs {row['ref_opp']:.0f})"
            if row["ref_opp"] is not None
            else ""
        )
        label = Path(task["b"]).stem if task["b_kind"] == "tape" else f"seed {row['seed']:>6}"
        print(
            f"{label:<40} seat {row['seat']}  {row['result']}  "
            f"{row['me']:>9.0f} vs {row['opp']:>9.0f}{ref}  ({row['secs']}s){flag}"
        )

    wins = sum(r["result"] == "W" for r in rows)
    losses = sum(r["result"] == "L" for r in rows)
    ties = sum(r["result"] == "T" for r in rows)
    errors = sum(r["me_status"] != "DONE" for r in rows)
    margin = statistics.mean(r["me"] - r["opp"] for r in rows)
    print(f"\n{args.a} vs {args.b} | {len(rows)} games")
    print(
        f"W-L-T {wins}-{losses}-{ties}  win rate {wins / len(rows):.0%}  "
        f"mean bank {statistics.mean(r['me'] for r in rows):.0f} vs "
        f"{statistics.mean(r['opp'] for r in rows):.0f}  mean margin {margin:+.0f}  "
        f"errors {errors}  ({statistics.mean(r['secs'] for r in rows):.1f} s/game)"
    )


if __name__ == "__main__":
    main()
