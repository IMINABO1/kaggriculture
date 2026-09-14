"""Baseline policy: one farmer working a small wheat patch beside the shed.

This exists so the pipeline (arena, packaging, tests) has something real to run.
It is not the competitive agent.
"""

from __future__ import annotations

WHEAT_SEED_COST = 10
WHEAT_HARVEST_AGE = 4
LAST_SAFE_PLANT_HOUR = 21
PATCH = [(x, y) for y in (3, 4) for x in (1, 2, 3, 4)]
SELLABLE = {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"}
MAX_MARKET_ORDERS = 10


def step_toward(pos, target):
    x, y = pos
    tx, ty = target
    if x < tx:
        return "EAST"
    if x > tx:
        return "WEST"
    if y < ty:
        return "SOUTH"
    if y > ty:
        return "NORTH"
    return None


def tile_action(tile, day, hour, seeds):
    """The useful op for a unit standing on ``tile``, or None."""
    if tile is None:
        if seeds > 0 and hour <= LAST_SAFE_PLANT_HOUR:
            return ["PLANT", "WHEAT"]
        return None
    if tile == "LOCKED":
        return None
    kind = tile.get("kind")
    if kind == "WEED":
        return ["DIG"]
    if kind == "PLANT":
        if not tile["watered_today"]:
            return ["WATER"]
        if day - tile["planted_day"] >= WHEAT_HARVEST_AGE and tile["yield_units"] > 0:
            return ["HARVEST"]
    return None


def market_orders(me, private):
    orders = []
    for item, count in private["shed"].items():
        if item in SELLABLE and count > 0:
            orders.append(["SELL", item, int(count)])
    empty = sum(1 for x, y in PATCH if me["tiles"][y][x] is None)
    shortfall = empty - private["seeds"].get("WHEAT", 0)
    if shortfall > 0 and me["money"] >= WHEAT_SEED_COST * shortfall:
        orders.append(["BUY_SEED", "WHEAT", shortfall])
    return orders[:MAX_MARKET_ORDERS]


def act(obs):
    me = obs["farms"][obs["player"]]
    private = obs["private"]
    day, hour = obs["day"], obs["hour"]
    tiles = me["tiles"]
    fx, fy = me["farmer"]
    seeds = private["seeds"].get("WHEAT", 0)

    farmer = None
    if (fx, fy) in PATCH:
        farmer = tile_action(tiles[fy][fx], day, hour, seeds)
    if farmer is None:
        pending = [
            (x, y)
            for x, y in PATCH
            if (x, y) != (fx, fy) and tile_action(tiles[y][x], day, hour, seeds) is not None
        ]
        if pending:
            tx, ty = min(pending, key=lambda t: abs(t[0] - fx) + abs(t[1] - fy))
            farmer = [step_toward((fx, fy), (tx, ty))]
    if farmer is None:
        farmer = ["PASS"]

    return {
        "farmer": farmer,
        "hands": [["PASS"] for _ in me["hands"]],
        "market": market_orders(me, private),
    }
