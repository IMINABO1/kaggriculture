"""The public line's economy as day-indexed targets and a tile layout.

Read off yhay81's Shop Router 0909 plan 0 (the no-Yarn-Store route the medal plateau runs,
first seen 2026-09-09) and the recorded Catalyst game 108947518: 2 cows + 2 sheep on day 0,
8 cows / 6 sheep / 3 geese by day 11, land NE on day 6 and SW on day 11, 12 melon on day 0,
33 strawberry tiles planted days 5-11, wheat on every other tile, carrots on the freed
strawberry tiles from day 24, and the hire count per day of the tape.
"""

from __future__ import annotations

# the tape's hires per day, plus one from day 10: this executor walks more than the searched
# routes and the twelfth hand costs $144 a day
HANDS_BY_DAY = [5, 3, 4, 5, 4, 4, 7, 7, 8, 8, 12, 11, 10, 10, 10, 11, 12, 12, 12, 11,
                12, 12, 11, 11, 11, 11, 11, 11, 12, 12]

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
CARROT_FIRST_DAY = 24
CARROT_LAST_DAY = 26          # planted day 26 it is harvested at age 3 on day 29
WHEAT_LAST_DAY = 27           # harvest at age 2 on day 29 gives 2 units for a $10 seed
MELON_DAY = 0

WHEAT_FEED_RESERVE_DAYS = 1   # shed wheat kept back from sales, in days of feed

# the public line's tape (agent/line_v41.py) plays the first TAPE_DAYS days, our runtime agent
# the rest; 0 is our agent alone, 30 the tape alone (journal 2026-09-16, hybrid curve)
TAPE_DAYS = 16


def cumulative(target: dict[int, int], day: int) -> int:
    return max([n for d, n in target.items() if d <= day], default=0)


def quadrant(x: int, y: int) -> str:
    return ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
