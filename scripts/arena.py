"""Paired-seat, fixed-seed head-to-head arena.

    uv run python scripts/arena.py --a main.py --b starter --seeds 0-9
    uv run python scripts/arena.py --a main.py --b opponents/ref/rancher_rita.py --seeds 100-119 --jobs 4
    uv run python scripts/arena.py --a main.py --b "tape:opponents/top10/majkel1337_*.json" --jobs 4
    uv run python scripts/arena.py --a main.py --b line:v5 --seeds 0-19 --jobs 3

Opponents are builtin names, agent files, `line:<name>` public-line routers (LINES below),
or `tape:<glob>` recordings exported by scripts/top10/export_tapes.py. A tape plays its recorded actions in its recorded seat on its
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
# public-line routers pulled from Kaggle (data/notebooks/, gitignored; see journal 2026-09-16)
LINES = {
    "line:0909": "data/notebooks/shop-router-0909/output/main.py",
    "line:0913": "data/notebooks/shop-router-0913/output/main.py",
    "line:v5": "data/notebooks/kaggriculture-shop-router-reactive-v5/output/main.py",
    "line:v6": "data/notebooks/kaggriculture-shop-router-reactive-v6/output/main.py",
    # the multi-route family (V41/EXP260): 28 routes chosen by the first two shops; its route
    # tapes match hundreds of sampled ladder seats through turn 400 (journal 2026-09-16)
    "line:v41": "data/notebooks/kaggriculture-multi-route-farming-agent/output/main.py",
}
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
    "shops",
    "harvest",
]
HARVEST_KEYS = {"MELON": "MEL", "STRAWBERRY": "STR", "WHEAT": "WHE", "CARROT": "CAR", "TOMATO": "TOM",
                "COW": "MIL", "SHEEP": "WOO", "GOOSE": "EGG"}
# the public line's realized prices (analysis.md section 7, gold medians): a basket value of
# the units harvested that does not move with the shop draw
BASKET_PRICES = {"MEL": 198, "STR": 116, "WHE": 39, "CAR": 49, "TOM": 143, "MIL": 84, "WOO": 105, "EGG": 55}


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
    path = Path(LINES.get(spec, spec))
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
        {"a": a, "b": b, "b_kind": "agent", "seed": seed, "seat": seat, "steps": args.steps,
         "decouple_shops": args.decouple_shops}
        for seed in parse_seeds(args.seeds)
        for seat in seats
    ]


def harvested_units(steps, seat: int) -> str:
    """Units harvested by product, counted from HARVEST actions against the tile they stood on:
    a production readout that does not depend on the prices the shop draw set."""
    counts: dict[str, int] = {}
    for t in range(len(steps) - 1):
        farm = steps[t][seat].observation["farms"][seat]
        action = steps[t + 1][seat].action or {}
        units = [farm["farmer"]] + list(farm["hands"])
        ops = [action.get("farmer")] + list(action.get("hands") or [])
        for i, op in enumerate(ops):
            if not op or op[0] != "HARVEST" or i >= len(units):
                continue
            x, y = units[i]
            tile = farm["tiles"][y][x]
            if not isinstance(tile, dict):
                continue
            key = HARVEST_KEYS.get(tile.get("crop") or tile.get("animal"))
            if key:
                counts[key] = counts.get(key, 0) + int(tile.get("yield_units", 0))
    return " ".join(f"{k}{counts[k]}" for k in HARVEST_KEYS.values() if counts.get(k))


def parse_harvest(text: str) -> dict[str, int]:
    return {tok[:3]: int(tok[3:]) for tok in text.split() if tok[3:].isdigit()}


def basket(text: str) -> float:
    return sum(n * BASKET_PRICES.get(k, 0) for k, n in parse_harvest(text).items())


def patch_town(seed: int, scripted: list[str] | None = None) -> None:
    """Make the town's shop draw depend on the seed alone (or follow a scripted list).

    The engine draws each day's shop from the per-day generator that has just spawned the
    weeds, one draw per empty tile on both farms, so the shops of a "fixed" seed move with
    either farm's empty-tile count (P22). For A/B runs the shop is drawn here from a
    generator keyed by seed and day only; the gauntlet scripts a recording's own town. The
    weeds keep the engine's draw. This patches the engine module in this process only.
    """
    import random

    from kaggle_environments.envs.kaggriculture import kaggriculture as mod

    orig = mod._end_of_day

    def end_of_day(state, env, day):
        cap = mod.MAX_SHOP_INSTANCES
        mod.MAX_SHOP_INSTANCES = 0  # the original then skips its own draw
        try:
            orig(state, env, day)
        finally:
            mod.MAX_SHOP_INSTANCES = cap
        town = state[0].observation.town
        next_day = day + 1
        interval = max(1, int(mod.get(env.configuration, "townShopUnlockInterval", 3)))
        if next_day > 0 and next_day % interval == 0 and len(town["unlocked_shops"]) < cap:
            if scripted is not None:
                idx = len(town["unlocked_shops"])
                if idx < len(scripted):
                    town["unlocked_shops"].append(scripted[idx])
            else:
                rng = random.Random((seed * 1_000_003) ^ (next_day * 7919) ^ 0x5EED)
                town["unlocked_shops"].append(rng.choice(sorted(mod.SHOPS)))

    mod._end_of_day = end_of_day


def play(task: dict) -> dict:
    from kenv import import_ke

    ke = import_ke()
    seat, seed, steps = task["seat"], task["seed"], task["steps"]
    if task.get("shops") is not None:
        patch_town(seed, list(task["shops"]))
    elif task.get("decouple_shops"):
        patch_town(seed)
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
        "shops": " ".join(s[:6] for s in final[0].observation["town"]["unlocked_shops"]),
        "harvest": harvested_units(env.steps, seat),
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
    ap.add_argument(
        "--decouple-shops", action="store_true",
        help="draw each day's shop from the seed alone, not the engine's weed stream (P22)",
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
    keys = list(HARVEST_KEYS.values())
    mean_units = {k: statistics.mean(parse_harvest(r["harvest"]).get(k, 0) for r in rows) for k in keys}
    print("harvest mean " + " ".join(f"{k}{mean_units[k]:.0f}" for k in keys if mean_units[k])
          + f"  basket {statistics.mean(basket(r['harvest']) for r in rows):.0f}")
    print(
        f"W-L-T {wins}-{losses}-{ties}  win rate {wins / len(rows):.0%}  "
        f"mean bank {statistics.mean(r['me'] for r in rows):.0f} vs "
        f"{statistics.mean(r['opp'] for r in rows):.0f}  mean margin {margin:+.0f}  "
        f"errors {errors}  ({statistics.mean(r['secs'] for r in rows):.1f} s/game)"
    )


if __name__ == "__main__":
    main()
