"""Mine a team's purchase schedule from its encoded games: hands per day, land days, animals
owned per day by shop draw, seed purchases per day by crop, and the sell lots by product and
hour. Prints Python literals for agent/plan.py.

    uv run python scripts/learn/mine_market.py --team "THIRD FARM CLUB"
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research.encode import ANIMALS, CROPS, FEATURES, SHOPS, load_encoded  # noqa: E402
from research.paths import DATA  # noqa: E402

YARN = SHOPS.index("YARN_STORE") + 1
EGG = {SHOPS.index("BAKERY") + 1, SHOPS.index("BRUNCH_SPOT") + 1}
MILK = {SHOPS.index("PIZZA_SHOP") + 1, SHOPS.index("ICE_CREAM_SHOP") + 1, SHOPS.index("SMOOTHIE_SHOP") + 1}
CARROT = {SHOPS.index("PET_CAFE") + 1, SHOPS.index("FARMERS_MARKET") + 1}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--team", default="THIRD FARM CLUB")
    args = ap.parse_args()
    hist = pd.read_parquet(DATA / "gold/history.parquet")
    enc = set(pd.read_csv(FEATURES / "manifest.csv").episode_id.astype(int))
    mine = hist[(hist.team_name == args.team) & (hist.is_current_sub == True) & (hist.episode_id.astype(int).isin(enc))].drop_duplicates("episode_id")
    hands = []
    quads = []
    animals = defaultdict(list)      # (condition, animal) -> list of per-day arrays
    seeds_bought = defaultdict(lambda: np.zeros(30))
    n_games = 0
    for r in mine.itertuples():
        z = load_encoded(int(r.episode_id))
        s = int(r.seat)
        n_games += 1
        hands.append([int(z["n_units"][s, d * 24 + 2]) - 1 for d in range(30)])
        quads.append([int(z["quadrants"][s, d * 24]) for d in range(30)])
        shops9 = set(int(x) for x in z["shops"][9 * 24][:3] if x)
        cond = {"yarn": YARN in shops9, "egg": bool(EGG & shops9), "milk": bool(MILK & shops9), "carrot": bool(CARROT & shops9)}
        for a_id, a in zip(range(6, 9), ANIMALS):
            per_day = [int(((z["tiles"][s, d * 24, :, :, 0] == 5) & (z["tiles"][s, d * 24, :, :, 1] == a_id)).sum() + z["shed"][s, d * 24, 9 + ANIMALS.index(a)]) for d in range(30)]
            for key in ("all", "yarn" if cond["yarn"] else "noyarn", "egg" if cond["egg"] else "noegg", "milk" if cond["milk"] else "nomilk"):
                animals[(key, a)].append(per_day)
        m_type, m_item, m_qty = z["m_type"][s], z["m_item"][s], z["m_qty"][s]
        for t in range(719):
            for k in range(10):
                if m_type[t, k] == 3 and m_item[t, k] > 0:   # BUY_SEED
                    seeds_bought[(CROPS[m_item[t, k] - 1], "carrot" if cond["carrot"] else "nocarrot")][t // 24] += int(m_qty[t, k])
    print(f"{args.team}: {n_games} games")
    print("HANDS_BY_DAY =", np.median(np.array(hands), axis=0).astype(int).tolist())
    q = np.array(quads)
    print("land: median day NE unlocked", int(np.median([next((d for d in range(30) if row[d] & 2), 30) for row in q])),
          "SW", int(np.median([next((d for d in range(30) if row[d] & 4), 30) for row in q])),
          "SE", int(np.median([next((d for d in range(30) if row[d] & 8), 30) for row in q])), "(30 = never)")
    for key in ("all", "yarn", "noyarn", "egg", "noegg", "milk", "nomilk"):
        for a in ANIMALS:
            arr = np.array(animals[(key, a)])
            if len(arr):
                med = np.median(arr, axis=0).astype(int).tolist()
                print(f"  {key:<7} {a:<6} n={len(arr):>3} owned by day: {med}")
    print("seeds bought per game by day (mean), by crop and carrot-shop condition:")
    for (crop, cond), arr in sorted(seeds_bought.items()):
        n = sum(1 for _ in mine.itertuples())
        print(f"  {crop:<11} {cond:<9} " + " ".join(f"{v:.0f}" for v in arr / max(1, n)))


if __name__ == "__main__":
    main()
