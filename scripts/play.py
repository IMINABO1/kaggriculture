"""Play one game and inspect it.

    uv run python scripts/play.py --a main.py --b starter --seed 0 --replay

Prints final banks and statuses, the money trajectory at each day boundary, and an
end-of-season tile summary per farm. --replay writes replays/<a>_vs_<b>_<seed>.json for the
visualizer or offline analysis.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILTINS = {"starter", "random", "pass"}


def resolve(spec: str) -> str:
    if spec in BUILTINS:
        return spec
    path = Path(spec)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        raise SystemExit(f"agent not found: {spec}")
    return str(path)


def summarize_farm(farm) -> Counter:
    counts: Counter = Counter()
    for row in farm["tiles"]:
        for tile in row:
            if tile is None:
                counts["empty"] += 1
            elif tile == "LOCKED":
                counts["locked"] += 1
            elif tile["kind"] == "PLANT":
                counts[f"plant:{tile['crop']}"] += 1
            elif tile["kind"] == "WEED":
                counts["weed"] += 1
            else:
                counts[f"{tile['kind'].lower()}:{tile.get('animal') or 'empty'}"] += 1
    return counts


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--a", default="main.py")
    ap.add_argument("--b", default="starter")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--steps", type=int, default=720)
    ap.add_argument("--replay", action="store_true")
    args = ap.parse_args()

    from kenv import import_ke

    env = import_ke().make(
        "kaggriculture", configuration={"episodeSteps": args.steps, "seed": args.seed}, debug=True
    )
    env.run([resolve(args.a), resolve(args.b)])

    turns_per_day = env.configuration.turnsPerDay
    final = env.steps[-1]
    for i, state in enumerate(final):
        name = args.a if i == 0 else args.b
        print(f"player {i} ({name}): bank {state.reward}  status {state.status}")

    print("\nmoney by day:")
    for i in range(2):
        trajectory = [
            round(step[0].observation.farms[i].money) for step in env.steps[::turns_per_day]
        ]
        print(f"  p{i}: {trajectory}")

    print("\nend-of-season tiles:")
    obs = final[0].observation
    for i in range(2):
        summary = ", ".join(f"{k}={v}" for k, v in sorted(summarize_farm(obs.farms[i]).items()))
        print(f"  p{i}: quadrants={list(obs.farms[i].unlocked_quadrants)}  {summary}")
    print(f"\nshops: {list(obs.town.unlocked_shops)}")

    if args.replay:
        out_dir = ROOT / "replays"
        out_dir.mkdir(exist_ok=True)
        out = out_dir / f"{Path(args.a).stem}_vs_{Path(args.b).stem}_{args.seed}.json"
        out.write_text(json.dumps(env.toJSON()))
        print(f"replay written to {out}")


if __name__ == "__main__":
    main()
