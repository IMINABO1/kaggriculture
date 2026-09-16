"""Market orders: the public line's purchase schedule and a sell-what-you-hold policy.

Sells go first in the queue so their money funds the buys behind them in the same turn.
Phase 1 sells every product as soon as it reaches the shed, keeping back only the wheat the
animals eat and the fertilizer the strawberries are about to get; the metering and denial
rules of the memo are Phase 2 and live here later.
"""

from __future__ import annotations

from agent import plan as P
from agent.executor import PRODUCE, target_crop

MAX_ORDERS = 10
# metering (memo, "The answer" 2): sell each premium product at about the town's drain rate
# in small orders across the day and hold the rest, instead of dumping what reaches the shed
METER = False               # off: against a daily dumper the held stock sold at the same floor (journal 2026-09-16)
METERED = ("STRAWBERRY", "MILK", "WOOL", "EGG", "CARROT", "TOMATO")
METER_K = 1.3               # sell this multiple of the drain so the stock still clears
METER_MIN_DRAIN = 6         # units a day the town must take before metering is worth it
METER_STOCK_CAP = 40        # shed stock above this is sold whatever the drain
DUMP_FROM_DAY = 28          # everything goes from here
SHOPS = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"), "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
MIN_SELL_PRICE = 2
FEED_BUY_HOUR = 22
FERTILIZER_RESERVE_CAP = 24
HIRE_LAST_HOUR = 2
OPENING_WHEAT = 5           # the line's day-0 lot: feed for the first animals and day 1
# cheap seeds kept in hand so a harvested tile is replanted by the unit still standing on it
SEED_BUFFER = {"WHEAT": 6, "CARROT": 3}
SEED_BUFFER_FROM_DAY = 10   # before the melon money every dollar goes to the herd


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


def tiles_wanting(me, day, crop) -> int:
    """Tiles the plan wants under this crop today that do not carry it yet (a wheat filler
    standing where a strawberry belongs counts: the seed lets the executor swap it out)."""
    n = 0
    for y, row in enumerate(me["tiles"]):
        for x, tile in enumerate(row):
            if tile == "LOCKED" or target_crop(x, y, day) != crop:
                continue
            if tile is None or (isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile["crop"] != crop):
                n += 1
    return n


def town_drain_per_day(obs) -> dict:
    """Units of each product the town removes a day: every shop instance takes one of each of
    its products every four turns (two for a single-product shop), the town centre one a day."""
    drain = {item: 1.0 for item in PRODUCE if item != "FERTILIZER"}
    for shop in obs["town"].get("unlocked_shops", []):
        products = SHOPS.get(shop, ())
        for item in products:
            drain[item] = drain.get(item, 0.0) + (12.0 if len(products) == 1 else 6.0)
    return drain


def market_orders(obs, day, hour, summary, state=None) -> list:
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

    # 1. sells first: everything, less the feed reserve and the fertilizer about to be used
    feed_reserve = 0 if day >= 29 else herd * P.WHEAT_FEED_RESERVE_DAYS + 1
    fert_reserve = 0 if day >= 29 else min(
        FERTILIZER_RESERVE_CAP, summary.get("fertilize_pending", 0) + summary.get("fertilize_taken", 0)
    )
    expected = 0.0
    drain = town_drain_per_day(obs) if METER else {}
    budget = state.setdefault("meter", {}) if state is not None else {}
    for item in PRODUCE:
        have = shed.get(item, 0)
        if item == "WHEAT":
            have -= feed_reserve
        elif item == "FERTILIZER":
            have -= fert_reserve
        if have <= 0 or prices.get(item, 0) < MIN_SELL_PRICE:
            continue
        n = have
        if METER and item in METERED and day < DUMP_FROM_DAY and drain.get(item, 0) >= METER_MIN_DRAIN:
            budget[item] = budget.get(item, 0.0) + drain[item] * METER_K / 24.0
            n = min(have, int(budget[item]))
            if have > METER_STOCK_CAP:
                n = max(n, have - METER_STOCK_CAP)
            if n <= 0:
                continue
            budget[item] -= n
        orders.append(["SELL", item, int(n)])
        expected += 0.8 * n * prices[item]
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

    # 3. wheat for the animals comes before anything else money can buy: the opening lot on
    #    day 0, today's shortfall as income arrives, tomorrow's at the end of the day; the
    #    cash for today's still-unfed animals is kept back from seeds and animals
    wheat_on_hand = shed.get("WHEAT", 0) + carried_wheat
    wheat_price = prices.get("WHEAT", 25) + 3
    need = 0
    if day == 0 and hour == 0:
        need = OPENING_WHEAT
    elif day < 29 and hour >= FEED_BUY_HOUR:
        need = herd - wheat_on_hand
    elif day < 29 and hour <= 20:
        need = summary.get("unfed", 0) - wheat_on_hand
    n = min(max(0, need), int(cash // wheat_price))
    if n > 0:
        orders.append(["BUY_PRODUCT", "WHEAT", n])
        cash -= n * wheat_price
    if need > n:
        cash -= (need - n) * wheat_price

    # 4. land
    unlocked = me["unlocked_quadrants"]
    for quad, land_day in P.LAND_DAYS.items():
        if day >= land_day and quad not in unlocked:
            price = P.LAND_PRICES[len(unlocked) - 1]
            if cash >= price:
                orders.append(["BUY_LAND"])
                cash -= price
            break

    # 5. animals up to the plan's cumulative target
    targets = {"COW": P.COW_TARGET, "SHEEP": P.SHEEP_TARGET, "GOOSE": P.GOOSE_TARGET}
    for animal, target in targets.items():
        if day > P.LAST_ANIMAL_DAY:
            break
        want = P.cumulative(target, day) - animals[animal]
        n = min(want, int(cash // P.ANIMAL_COST[animal]))
        if n > 0:
            orders.append(["BUY_ANIMAL", animal, n])
            cash -= n * P.ANIMAL_COST[animal]

    # 6. seeds for the tiles the plan wants planted today, plus a small buffer in season
    if hour <= 20:
        for crop in ("MELON", "STRAWBERRY", "CARROT", "WHEAT"):
            wanting = tiles_wanting(me, day, crop)
            if crop == "WHEAT" and day > P.WHEAT_LAST_DAY:
                wanting = 0
            buffer = SEED_BUFFER.get(crop, 0) if wanting > 0 and day >= SEED_BUFFER_FROM_DAY else 0
            want = wanting + buffer - seeds.get(crop, 0)
            n = min(want, int(cash // P.SEED_COST[crop]))
            if n > 0:
                orders.append(["BUY_SEED", crop, n])
                cash -= n * P.SEED_COST[crop]

    return orders[:MAX_ORDERS]
