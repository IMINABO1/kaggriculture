"""Market orders: the public line's purchase schedule and a sell-what-you-hold policy.

Sells go first in the queue so their money funds the buys behind them in the same turn.
Phase 1 sells every product as soon as it reaches the shed, keeping back only the wheat the
animals eat and the fertilizer the strawberries are about to get; the metering and denial
rules of the memo are Phase 2 and live here later.
"""

from __future__ import annotations

from agent import plan as P
from agent.executor import PRODUCE, STRAWBERRY_TILES, crop_for_empty_tile

MAX_ORDERS = 10
MIN_SELL_PRICE = 2
FEED_BUY_HOUR = 22
FERTILIZER_RESERVE_CAP = 24
HIRE_LAST_HOUR = 2
# cheap seeds kept in hand so a harvested tile is replanted by the unit still standing on it
SEED_BUFFER = {"WHEAT": 6, "CARROT": 3}


def hire_cost(n: int) -> int:
    a, b, total = 1, 1, 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total


def count_animals(me, private) -> dict:
    """Animals on the farm, in the shed, or carried by a unit on its way to a pen."""
    counts = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    for row in me["tiles"]:
        for tile in row:
            if isinstance(tile, dict) and tile.get("animal"):
                counts[tile["animal"]] += 1
    for animal in counts:
        counts[animal] += private["shed"].get(animal, 0)
        counts[animal] += sum(inv.get(animal, 0) for inv in private["inventories"])
    return counts


def empty_tiles_wanting(me, day, crop) -> int:
    n = 0
    for y, row in enumerate(me["tiles"]):
        for x, tile in enumerate(row):
            if tile is None and crop_for_empty_tile(x, y, day) == crop:
                n += 1
    return n


def market_orders(obs, day, hour, summary) -> list:
    me = obs["farms"][obs["player"]]
    private = obs["private"]
    shed = private["shed"]
    seeds = private["seeds"]
    prices = obs["market"]["prices"]
    money = me["money"]
    orders: list = []
    animals = count_animals(me, private)
    herd = sum(animals.values())
    carried_wheat = sum(inv.get("WHEAT", 0) for inv in private["inventories"])

    # 1. sells first: everything, less the feed reserve and tomorrow's fertilizer
    feed_reserve = 0 if day >= 29 else herd * P.WHEAT_FEED_RESERVE_DAYS
    fert_reserve = 0 if day >= 29 else min(FERTILIZER_RESERVE_CAP, summary.get("fertilize_pending", 0) + summary.get("fertilize_taken", 0))
    expected = 0.0
    for item in PRODUCE:
        have = shed.get(item, 0)
        if item == "WHEAT":
            have -= feed_reserve
        elif item == "FERTILIZER":
            have -= fert_reserve
        if have > 0 and prices.get(item, 0) >= MIN_SELL_PRICE:
            orders.append(["SELL", item, int(have)])
            expected += 0.8 * have * prices[item]
    cash = money + expected

    # 2. hands for the day, ahead of the sells so the order cap never drops them
    if hour <= HIRE_LAST_HOUR and day < len(P.HANDS_BY_DAY):
        already = me.get("hires_today", 0)
        n = P.HANDS_BY_DAY[day] - already
        while n > 0 and hire_cost(already + n) - hire_cost(already) > money:
            n -= 1
        if n > 0:
            orders = [["HIRE"]] * n + orders[: MAX_ORDERS - n]
            cash -= hire_cost(already + n) - hire_cost(already)

    # 3. land
    unlocked = me["unlocked_quadrants"]
    for quad, land_day in P.LAND_DAYS.items():
        if day >= land_day and quad not in unlocked:
            price = P.LAND_PRICES[len(unlocked) - 1]
            if cash >= price:
                orders.append(["BUY_LAND"])
                cash -= price
            break

    # 4. animals up to the plan's cumulative target
    targets = {"COW": P.COW_TARGET, "SHEEP": P.SHEEP_TARGET, "GOOSE": P.GOOSE_TARGET}
    for animal, target in targets.items():
        if day > P.LAST_ANIMAL_DAY:
            break
        want = P.cumulative(target, day) - animals[animal]
        n = min(want, int(cash // P.ANIMAL_COST[animal]))
        if n > 0:
            orders.append(["BUY_ANIMAL", animal, n])
            cash -= n * P.ANIMAL_COST[animal]

    # 5. seeds for the tiles the plan wants planted today
    if hour <= 20:
        for crop in ("MELON", "STRAWBERRY", "CARROT", "WHEAT"):
            want = empty_tiles_wanting(me, day, crop) + SEED_BUFFER.get(crop, 0) - seeds.get(crop, 0)
            if crop == "WHEAT" and day > P.WHEAT_LAST_DAY:
                want = 0
            n = min(want, int(cash // P.SEED_COST[crop]))
            if n > 0:
                orders.append(["BUY_SEED", crop, n])
                cash -= n * P.SEED_COST[crop]

    # 6. wheat for the animals: tomorrow's feed at the end of the day, today's if short
    if day < 29:
        wheat_on_hand = shed.get("WHEAT", 0) + carried_wheat
        need = 0
        if hour >= FEED_BUY_HOUR:
            need = herd - wheat_on_hand
        elif hour <= 20 and summary.get("unfed", 0) > wheat_on_hand:
            need = summary["unfed"] - wheat_on_hand
        n = min(need, int(cash // max(1, prices.get("WHEAT", 25) + 2)))
        if n > 0:
            orders.append(["BUY_PRODUCT", "WHEAT", n])

    return orders[:MAX_ORDERS]
