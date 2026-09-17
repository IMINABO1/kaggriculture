"""The public line's economy as day-indexed targets and a tile layout.

Read off yhay81's Shop Router 0909 plan 0 (the no-Yarn-Store route the medal plateau runs,
first seen 2026-09-09) and the recorded Catalyst game 108947518: 2 cows + 2 sheep on day 0,
8 cows / 6 sheep / 3 geese by day 11, land NE on day 6 and SW on day 11, 12 melon on day 0,
33 strawberry tiles planted days 5-11, wheat on every other tile, carrots on the freed
strawberry tiles from day 24, and the hire count per day of the tape.
"""

from __future__ import annotations

import os

# the tape's hires per day, plus one from day 10: this executor walks more than the searched
# routes and the twelfth hand costs $144 a day; 13 on days 24-27 as v41's tape hires (H3)
HANDS_BY_DAY = [5, 3, 4, 5, 4, 4, 7, 7, 8, 8, 12, 11, 10, 10, 10, 11, 12, 12, 12, 11,
                12, 12, 11, 11, 13, 11, 11, 13, 11, 11]

LAND_DAYS = {"NE": 6, "SW": 11}
LAND_PRICES = [1000, 2000, 4000]

# cumulative animal targets by day (the count owned or in the shed from that day on)
COW_TARGET = {0: 2, 2: 3, 3: 4, 6: 6, 7: 8}
SHEEP_TARGET = {0: 2, 8: 4, 9: 6}
GOOSE_TARGET = {10: 2, 11: 3}

LAST_ANIMAL_DAY = 16          # a replacement bought later cannot pay for itself

ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}

# tiles in build order; animals near the shed so the daily feed walk is short
PASTURES_NW = [(4, 3), (4, 4), (3, 3), (3, 4), (4, 2), (2, 4), (1, 4)]  # (1, 4) after its melon
PASTURES_NE = [(5, 2), (6, 2), (5, 3), (6, 3), (5, 4), (6, 4), (7, 4)]
COOPS_NW = [(4, 0), (4, 1), (3, 2), (2, 3)]

MELONS_NW = [(3, 0), (4, 0), (2, 1), (3, 1), (4, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3),
             (0, 4), (1, 4)]
WHEAT_NW_DAY0 = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2), (0, 3)]

STRAWBERRIES_NW = [(2, 0), (1, 1), (0, 2), (0, 3), (1, 0)]
STRAWBERRIES_NE = [(5, 0), (6, 0), (7, 0), (5, 1), (6, 1), (7, 1), (8, 1), (7, 2), (8, 2),
                   (9, 2), (7, 3), (8, 3), (9, 3), (8, 4), (9, 4)]
STRAWBERRIES_SW = [(1, 5), (2, 5), (3, 5), (4, 5), (1, 6), (2, 6), (3, 6), (4, 6), (2, 7),
                   (3, 7), (4, 7), (3, 8), (4, 8)]

STRAWBERRY_FIRST_DAY = 5
STRAWBERRY_LAST_DAY = 13      # planted later than this cannot finish its four yields
CARROT_FIRST_DAY = 23
CARROT_LAST_DAY = 27          # planted day 27 it still gives two units on day 29 (C3)
WHEAT_LAST_DAY = 24           # planted later it reaches day 29 with 2-3 units and joins the last-day dump
MELON_DAY = 0

WHEAT_FEED_RESERVE_DAYS = 0   # shed wheat kept back from sales, in days of feed

# the public line's tape plays the first TAPE_DAYS days, our runtime agent the rest; 0 is our
# agent alone, 30 the tape alone (journal 2026-09-16, hybrid curve). TAPE_FILE picks the
# bundled build: line_v41.py (the multi-route family, the ladder's majority) or line_v7.py
# (its successor, +1.9k over v41 in mirror seats, journal 2026-09-17)
TAPE_DAYS = int(os.environ.get("KAGG_TAPE_DAYS", 24))
TAPE_FILE = "line_v41.py"
# a recorded team's modal opening (agent/opening_<name>.py, scripts/learn/extract_opening.py)
# played for OPENING_STEPS before the tape or the executor takes over; None = off. The
# KAGG_* variables override these for arena runs and are absent on Kaggle.
OPENING = os.environ.get("KAGG_OPENING") or None
OPENING_STEPS = int(os.environ.get("KAGG_OPENING_STEPS", 144))
# "executor": the greedy executor after the opening or the tape; "clone": the learned
# job-level policy (agent/clone.py, weights in agent/clone_weights.npz) with the executor
# as its fallback, and no public tape
POLICY = os.environ.get("KAGG_POLICY", "executor")

# THIRD FARM CLUB's purchase schedule, mined from its 135 recorded games by
# scripts/learn/mine_market.py (journal 2026-09-17): hands per day (median), land bought on
# days 6 and 9, and animals owned by day conditioned on the shops unlocked so far
TFC_HANDS_BY_DAY = [4, 4, 6, 6, 6, 6, 11, 9, 9, 12, 13, 10, 9, 8, 9, 11, 10, 10, 11, 11,
                    11, 11, 11, 10, 11, 11, 11, 10, 9, 11]
TFC_LAND_DAYS = {"NE": 6, "SW": 9}
TFC_COW = {1: 2, 7: 6, 9: 7, 10: 9}
TFC_COW_MILK_SHOP = {13: 10}
TFC_SHEEP = {1: 3}
TFC_SHEEP_YARN = {7: 6, 9: 8, 10: 10, 14: 11}
TFC_GOOSE = {7: 1, 8: 2, 12: 4, 13: 5, 15: 6}
TFC_GOOSE_EGG_SHOP = {14: 7}
TFC_GOOSE_NO_EGG_SHOP = {12: 3, 19: 4}
TFC_GOOSE_YARN = {12: 3, 14: 4}
MILK_SHOPS = ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP")
EGG_SHOPS = ("BAKERY", "BRUNCH_SPOT")


def tfc_animal_targets(day: int, shops) -> dict:
    """Cumulative animal targets for today under the shops unlocked so far."""
    yarn = "YARN_STORE" in shops
    milk = any(s in MILK_SHOPS for s in shops)
    egg = any(s in EGG_SHOPS for s in shops)
    cow = max(cumulative(TFC_COW, day), cumulative(TFC_COW_MILK_SHOP, day) if milk else 0)
    sheep = max(cumulative(TFC_SHEEP, day), cumulative(TFC_SHEEP_YARN, day) if yarn else 0)
    if yarn:
        goose = cumulative(TFC_GOOSE_YARN, day)
    elif egg:
        goose = max(cumulative(TFC_GOOSE, day), cumulative(TFC_GOOSE_EGG_SHOP, day))
    else:
        goose = min(cumulative(TFC_GOOSE, day), max(cumulative(TFC_GOOSE_NO_EGG_SHOP, day), 2 if day >= 8 else 1 if day >= 7 else 0))
    if yarn:
        cow = min(cow, 7 if day >= 14 else 6 if day >= 12 else 4 if day >= 7 else 2)
    return {"COW": cow, "SHEEP": sheep, "GOOSE": goose}


def cumulative(target: dict[int, int], day: int) -> int:
    return max([n for d, n in target.items() if d <= day], default=0)


def quadrant(x: int, y: int) -> str:
    return ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
