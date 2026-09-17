"""Market orders: the public line's purchase schedule and a sell-what-you-hold policy.

Sells go first in the queue so their money funds the buys behind them in the same turn.
By default every product is sold as soon as it reaches the shed, keeping back only the wheat
the animals eat and the fertilizer the strawberries are about to get; `METER` switches the
memo's metering rule on.
"""

from __future__ import annotations

from agent import plan as P
from agent.executor import PRODUCE, target_crop

MAX_ORDERS = 10
# metering (memo, "The answer" 2): where the town drains a premium product faster than the
# opponent supplies it, sell only into that room, in small lots across the day, and hold the
# rest; where the opponent floods it, holding buys nothing (journal 2026-09-16) and the stock
# is sold as it reaches the shed
METER = False               # off against the line: holding hands a dumper a recovered price (journal 2026-09-16)
METERED = ("STRAWBERRY", "MILK", "WOOL", "EGG", "CARROT", "TOMATO")
METER_FROM_DAY = 12         # before this the premium stock is a few units
DUMP_FROM_DAY = 28          # everything goes from here
METER_K = 1.0               # sell this multiple of the room
METER_MIN_ROOM = 4          # units a day of room below which the market counts as flooded
OPP_WINDOW = 48             # turns over which the opponent's selling rate is measured
SHOPS = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"), "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
MIN_SELL_PRICE = 2
FEED_BUY_HOUR = 22
FERTILIZER_RESERVE_CAP = 16
HIRE_LAST_HOUR = 2
OPENING_WHEAT = 5           # the line's day-0 lot: feed for the first animals and day 1
# cheap seeds kept in hand so a harvested tile is replanted by the unit still standing on it
SEED_BUFFER = {"WHEAT": 3, "CARROT": 0}
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


def drain_at_step(obs, step: int) -> dict:
    """Units the town removes right after this step's market (the engine's _town_consume)."""
    drain = {item: 0 for item in PRODUCE}
    if step % 4 == 0:
        for shop in obs["town"].get("unlocked_shops", []):
            products = SHOPS.get(shop, ())
            for item in products:
                drain[item] += 2 if len(products) == 1 else 1
    if step % 24 == 0:
        for item in PRODUCE:
            if item != "FERTILIZER":
                drain[item] += 1
    return drain


def opponent_rate(state: dict, obs, step: int) -> dict:
    """Units a day the opponent has been selling of each metered product: the market
    inventory's change since last turn, net of the town's drain and our own executed sells
    (we never order more than the shed holds, so an order executes in full)."""
    inv = obs["market"]["inventory"]
    hist = state.setdefault("opp_hist", {item: [] for item in METERED})
    if state.get("inv_step") == step - 1:
        prev, mine, drained = state["inv_prev"], state.get("my_sells", {}), drain_at_step(obs, step - 1)
        for item in METERED:
            hist[item].append(max(0, inv[item] - prev[item] + drained[item] - mine.get(item, 0)))
            del hist[item][:-OPP_WINDOW]
    state["inv_prev"], state["inv_step"] = dict(inv), step
    return {item: sum(hist[item]) * 24.0 / max(1, len(hist[item])) for item in METERED}


def metered_quantity(item: str, have: int, day: int, drain: dict, opp: dict, budget: dict) -> int:
    room = drain.get(item, 0.0) - opp.get(item, 0.0)
    if room < METER_MIN_ROOM:
        return have
    holdable = room * (DUMP_FROM_DAY - day)
    budget[item] = budget.get(item, 0.0) + room * METER_K / 24.0
    n = int(budget[item])
    if have > holdable:
        n = max(n, int(have - holdable))
    n = min(n, have)
    budget[item] = max(0.0, budget[item] - n)
    return n


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
    metering = METER and state is not None
    if metering:
        opp = opponent_rate(state, obs, day * 24 + hour)
        drain = town_drain_per_day(obs)
        budget = state.setdefault("meter", {})
    for item in PRODUCE:
        have = shed.get(item, 0)
        if item == "WHEAT":
            have -= feed_reserve
        elif item == "FERTILIZER":
            have -= fert_reserve
        if have <= 0 or prices.get(item, 0) < MIN_SELL_PRICE:
            continue
        n = have
        if metering and item in METERED and METER_FROM_DAY <= day < DUMP_FROM_DAY:
            n = metered_quantity(item, have, day, drain, opp, budget)
            if n <= 0:
                continue
        orders.append(["SELL", item, int(n)])
        expected += 0.8 * n * prices[item]
    cash = money + expected

    # 2. hands for the day, ahead of the sells so the order cap never drops them; on a
    #    planned day the plan sizes the crew to the work
    dayplan = (state or {}).get("dayplan") or {}
    clone = P.POLICY == "clone"
    hands_by_day = P.TFC_HANDS_BY_DAY if clone else P.HANDS_BY_DAY
    if hour <= HIRE_LAST_HOUR and day < len(hands_by_day):
        already = me.get("hires_today", 0)
        hands = dayplan.get("hands", hands_by_day[day]) if dayplan.get("day") == day else hands_by_day[day]
        n = hands - already
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
    for quad, land_day in (P.TFC_LAND_DAYS if clone else P.LAND_DAYS).items():
        if day >= land_day and quad not in unlocked:
            price = P.LAND_PRICES[len(unlocked) - 1]
            if cash >= price:
                orders.append(["BUY_LAND"])
                cash -= price
            break

    # 5. animals up to the plan's cumulative target (the clone follows THIRD FARM CLUB's
    #    schedule under the shops unlocked so far)
    if clone:
        wanted_animals = P.tfc_animal_targets(day, obs["town"].get("unlocked_shops", []))
    else:
        wanted_animals = {a: P.cumulative(t, day) for a, t in (("COW", P.COW_TARGET), ("SHEEP", P.SHEEP_TARGET), ("GOOSE", P.GOOSE_TARGET))}
    for animal, target in wanted_animals.items():
        if day > P.LAST_ANIMAL_DAY:
            break
        want = target - animals[animal]
        n = min(want, int(cash // P.ANIMAL_COST[animal]))
        if n > 0:
            orders.append(["BUY_ANIMAL", animal, n])
            cash -= n * P.ANIMAL_COST[animal]

    # 6. seeds for the tiles the plan wants planted today, plus a small buffer in season; on a
    #    planned day the day plan knows how many tiles will be replanted after their harvest,
    #    and the clone reports the plantings it wanted but had no seed for
    plan_wanted = dict(dayplan.get("plant_wanted", {}) if dayplan.get("day") == day else {})
    if clone and state is not None:
        for crop, n in state.pop("clone_seed_wanted", {}).items():
            plan_wanted[crop] = plan_wanted.get(crop, 0) + n
        if hour == 0:  # the team's own purchase schedule, so the seeds are there when the model plants
            for crop, n in P.tfc_seeds_today(day, obs["town"].get("unlocked_shops", [])).items():
                plan_wanted[crop] = max(plan_wanted.get(crop, 0), n + seeds.get(crop, 0))
    if hour <= 20:
        for crop in ("MELON", "STRAWBERRY", "CARROT", "WHEAT", "TOMATO"):
            wanting = max(0 if clone else tiles_wanting(me, day, crop), plan_wanted.get(crop, 0))
            if crop == "WHEAT" and day > P.WHEAT_LAST_DAY and not clone:
                wanting = 0
            buffer = SEED_BUFFER.get(crop, 0) if wanting > 0 and day >= SEED_BUFFER_FROM_DAY else 0
            want = wanting + buffer - seeds.get(crop, 0)
            n = min(want, int(cash // P.SEED_COST[crop]))
            if n > 0:
                orders.append(["BUY_SEED", crop, n])
                cash -= n * P.SEED_COST[crop]

    orders = orders[:MAX_ORDERS]
    if state is not None:
        state["my_sells"] = {o[1]: int(o[2]) for o in orders if o[0] == "SELL"}
    return orders
