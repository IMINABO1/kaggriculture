"""Where the money comes from: executed revenue by product and by hour for both seats of local
games between two agents (the market replica on the played game), plus harvest and op counts.

    KAGG_POLICY=clone KAGG_OPENING=tfc KAGG_TAPE_DAYS=0 uv run python scripts/learn/revenue.py --a main.py --b line:v41 --seeds 0,1,2
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
BUCKETS = ((0, 1), (2, 11), (12, 19), (20, 23))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", default="main.py")
    ap.add_argument("--b", default="line:v41")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--seat", type=int, default=0, help="the seat A plays")
    args = ap.parse_args()
    from kenv import import_ke

    ke = import_ke()
    from agent.tape import actions_from_replay
    from arena import harvested_units, patch_town, resolve
    from research.market_replay import market_events

    seeds = [int(s) for s in args.seeds.split(",")]
    rev = [defaultdict(float), defaultdict(float)]
    units = [defaultdict(int), defaultdict(int)]
    hours = [defaultdict(float), defaultdict(float)]
    spend = [defaultdict(float), defaultdict(float)]
    ops = [Counter(), Counter()]
    harvest = ["", ""]
    banks = []
    for seed in seeds:
        patch_town(seed)
        order = [None, None]
        order[args.seat], order[1 - args.seat] = resolve(args.a), resolve(args.b)
        env = ke.make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
        env.run(order)
        replay = env.toJSON()
        banks.append(replay["rewards"])
        actions = [actions_from_replay(replay, 0), actions_from_replay(replay, 1)]
        events, _ = market_events(replay, actions)
        for s in (0, 1):
            for ev in events[s]:
                if ev["type"] == "SELL":
                    rev[s][ev["item"]] += ev["revenue"] / len(seeds)
                    units[s][ev["item"]] += ev["executed"] / len(seeds)
                    b = next(i for i, (lo, hi) in enumerate(BUCKETS) if lo <= ev["hour"] <= hi)
                    hours[s][(ev["item"], b)] += ev["revenue"] / len(seeds)
                elif ev["type"] in ("BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT"):
                    spend[s][ev["item"]] += ev["spent"] / len(seeds)
            for a in actions[s]:
                for op in [a.get("farmer")] + list(a.get("hands") or []):
                    if op:
                        ops[s][op[0]] += 1 / len(seeds)
            harvest[s] = harvested_units(env.steps, s)
    a, b = args.seat, 1 - args.seat
    print(f"banks by seed (A in seat {a}): {banks}")
    print(f"{'product':<11} {'A rev':>8} {'units':>6}   {'B rev':>8} {'units':>6}   A hours 0-1/2-11/12-19/20-23   B hours")
    for p in PRODUCTS:
        ha = [hours[a][(p, i)] for i in range(4)]
        hb = [hours[b][(p, i)] for i in range(4)]
        sa, sb = sum(ha) or 1, sum(hb) or 1
        print(f"{p:<11} {rev[a][p]:>8.0f} {units[a][p]:>6.0f}   {rev[b][p]:>8.0f} {units[b][p]:>6.0f}   "
              + "/".join(f"{100 * v / sa:.0f}" for v in ha) + "   " + "/".join(f"{100 * v / sb:.0f}" for v in hb))
    print(f"total A {sum(rev[a].values()):.0f} B {sum(rev[b].values()):.0f}; spend A {sum(spend[a].values()):.0f} B {sum(spend[b].values()):.0f}")
    print(f"harvest last game A {harvest[a]} | B {harvest[b]}")
    print("ops A", {k: round(v) for k, v in ops[a].most_common(12)})
    print("ops B", {k: round(v) for k, v in ops[b].most_common(12)})


if __name__ == "__main__":
    main()
