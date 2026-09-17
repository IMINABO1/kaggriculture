"""Encode a replay into fixed-size arrays for learning.

One replay becomes a dict of numpy arrays with a leading step axis over the recorded
observations (720 for a full game). Both farms are encoded, because both players see both,
with each seat's private state (shed, seeds, unit inventories, money) and each seat's actions.
The action stored at step t is the one the seat submitted on seeing observation t
(``steps[t + 1].action``), so the last step carries no action.

Tile channels (uint8, ``tiles[seat, step, y, x, channel]``):
    0 kind      0 empty, 1 locked, 2 weed, 3 plant, 4 empty structure, 5 animal in structure
    1 id        crop 1-5 (WHEAT..MELON), animal 6-8 (GOOSE, COW, SHEEP), 9 pasture, 10 coop
    2 age       days since planted or placed
    3 yield     yield_units
    4 tended    watered_today (plant) or fed_today (animal)
    5 missed    consecutive_unwatered (plant) or consecutive_unfed (animal)
    6 fert      days of fertilizer left including today (plant)
    7 decaying  plant past its lifespan and losing a unit every other step
    8 cared     cared_today (animal)
    9 dung      fertilizer_available (animal)
    10 bonus    pending_care_bonus (animal)
    11 life     whole days before a one-time crop starts to decay (plant)
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from research.paths import DATA

FEATURES = DATA / "features"
ENCODING_VERSION = 1
MAX_UNITS = 20
MAX_ORDERS = 10
BOARD = 10
N_TILE_CH = 12

CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
ANIMALS = ("GOOSE", "COW", "SHEEP")
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
ITEMS = PRODUCTS + ANIMALS
SHOPS = ("BAKERY", "PIZZA_SHOP", "BRUNCH_SPOT", "YARN_STORE", "ICE_CREAM_SHOP", "PET_CAFE",
         "SMOOTHIE_SHOP", "FARMERS_MARKET")
OPS = ("PASS", "NORTH", "SOUTH", "EAST", "WEST", "PLANT", "WATER", "HARVEST", "FERTILIZE", "FEED",
       "CARE", "COLLECT_FERTILIZER", "BUILD_COOP", "BUILD_PASTURE", "DIG", "PLACE", "PICKUP", "DROP")
ORDER_TYPES = ("HIRE", "BUY_LAND", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL")
QUADRANT_BIT = {"NW": 1, "NE": 2, "SW": 4, "SE": 8}

CROP_ID = {c: i + 1 for i, c in enumerate(CROPS)}
ANIMAL_ID = {a: i + 6 for i, a in enumerate(ANIMALS)}
STRUCTURE_ID = {"PASTURE": 9, "COOP": 10}
ITEM_ID = {it: i + 1 for i, it in enumerate(ITEMS)}
SHOP_ID = {s: i + 1 for i, s in enumerate(SHOPS)}
OP_ID = {op: i + 1 for i, op in enumerate(OPS)}
ORDER_ID = {o: i + 1 for i, o in enumerate(ORDER_TYPES)}


def feature_path(episode_id: int) -> Path:
    return FEATURES / f"{episode_id}.npz"


def _u8(x) -> int:
    try:
        return max(0, min(255, int(x)))
    except (TypeError, ValueError):
        return 0


def encode_tiles(tiles, day: int, step: int, out) -> None:
    """Fill ``out[y, x, :]`` (uint8, N_TILE_CH) from one farm's tile grid."""
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile is None:
                continue
            if tile == "LOCKED":
                out[y, x, 0] = 1
                continue
            kind = tile.get("kind")
            if kind == "WEED":
                out[y, x, 0] = 2
            elif kind == "PLANT":
                out[y, x, 0] = 3
                out[y, x, 1] = CROP_ID.get(tile.get("crop"), 0)
                out[y, x, 2] = _u8(day - tile.get("planted_day", day))
                out[y, x, 3] = _u8(tile.get("yield_units", 0))
                out[y, x, 4] = 1 if tile.get("watered_today") else 0
                out[y, x, 5] = _u8(tile.get("consecutive_unwatered", 0))
                out[y, x, 6] = _u8(tile.get("fertilized_until_day", -1) - day + 1)
                mls = tile.get("max_lifespan_step", -1)
                if mls is not None and mls >= 0:
                    out[y, x, 7] = 1 if step >= mls else 0
                    out[y, x, 11] = _u8((mls - step) // 24) if step < mls else 0
            elif "animal" in tile:
                out[y, x, 0] = 5
                out[y, x, 1] = ANIMAL_ID.get(tile.get("animal"), 0)
                out[y, x, 2] = _u8(day - tile.get("placed_day", day))
                out[y, x, 3] = _u8(tile.get("yield_units", 0))
                out[y, x, 4] = 1 if tile.get("fed_today") else 0
                out[y, x, 5] = _u8(tile.get("consecutive_unfed", 0))
                out[y, x, 8] = 1 if tile.get("cared_today") else 0
                out[y, x, 9] = 1 if tile.get("fertilizer_available") else 0
                out[y, x, 10] = _u8(tile.get("pending_care_bonus", 0))
            elif kind in STRUCTURE_ID:
                out[y, x, 0] = 4
                out[y, x, 1] = STRUCTURE_ID[kind]


def encode_unit_action(op) -> tuple[int, int, int]:
    """(op id, argument id, count) for one unit's action; (0, 0, 0) when absent or malformed."""
    if not isinstance(op, list) or not op or op[0] not in OP_ID:
        return 0, 0, 0
    name = op[0]
    arg = count = 0
    if name == "PLANT" and len(op) > 1:
        arg = CROP_ID.get(op[1], 0)
    elif name in ("PLACE", "PICKUP") and len(op) > 1:
        arg = ITEM_ID.get(op[1], 0)
        try:
            count = int(op[2]) if len(op) > 2 else 1
        except (TypeError, ValueError):
            count = 0
        count = max(-32768, min(32767, count))
    return OP_ID[name], arg, count


def encode_order(order) -> tuple[int, int, int]:
    if not isinstance(order, list) or not order or order[0] not in ORDER_ID:
        return 0, 0, 0
    kind = order[0]
    if kind in ("HIRE", "BUY_LAND"):
        return ORDER_ID[kind], 0, 0
    if len(order) < 3:
        return ORDER_ID[kind], 0, 0
    item = CROP_ID.get(order[1], 0) if kind == "BUY_SEED" else ITEM_ID.get(order[1], 0)
    try:
        qty = int(order[2])
    except (TypeError, ValueError):
        qty = 0
    return ORDER_ID[kind], item, max(-(2 ** 31), min(2 ** 31 - 1, qty))


def encode_replay(replay: dict) -> dict:
    steps = replay["steps"]
    T = len(steps)
    tpd = int(replay["configuration"].get("turnsPerDay", 24))
    tiles = np.zeros((2, T, BOARD, BOARD, N_TILE_CH), dtype=np.uint8)
    unit_pos = np.full((2, T, MAX_UNITS, 2), -1, dtype=np.int8)
    unit_inv = np.zeros((2, T, MAX_UNITS, len(ITEMS)), dtype=np.uint8)
    n_units = np.zeros((2, T), dtype=np.int16)
    shed = np.zeros((2, T, len(ITEMS)), dtype=np.int16)
    seeds = np.zeros((2, T, len(CROPS)), dtype=np.int16)
    money = np.zeros((2, T), dtype=np.float32)
    hires_today = np.zeros((2, T), dtype=np.uint8)
    quadrants = np.zeros((2, T), dtype=np.uint8)
    prices = np.zeros((T, len(PRODUCTS)), dtype=np.int16)
    inventory = np.zeros((T, len(PRODUCTS)), dtype=np.int32)
    shops = np.zeros((T, 8), dtype=np.uint8)
    day = np.zeros(T, dtype=np.uint8)
    hour = np.zeros(T, dtype=np.uint8)
    op = np.zeros((2, T, MAX_UNITS), dtype=np.uint8)
    op_arg = np.zeros((2, T, MAX_UNITS), dtype=np.uint8)
    op_count = np.zeros((2, T, MAX_UNITS), dtype=np.int16)
    m_type = np.zeros((2, T, MAX_ORDERS), dtype=np.uint8)
    m_item = np.zeros((2, T, MAX_ORDERS), dtype=np.uint8)
    m_qty = np.zeros((2, T, MAX_ORDERS), dtype=np.int32)
    n_orders = np.zeros((2, T), dtype=np.int16)

    for t, step in enumerate(steps):
        shared_obs = step[0]["observation"]
        d, h = t // tpd, t % tpd
        day[t], hour[t] = d, h
        market = shared_obs["market"]
        for i, p in enumerate(PRODUCTS):
            prices[t, i] = max(-32768, min(32767, int(market["prices"].get(p, 0))))
            inventory[t, i] = int(market["inventory"].get(p, 0))
        for i, s in enumerate(shared_obs["town"].get("unlocked_shops", [])[:8]):
            shops[t, i] = SHOP_ID.get(s, 0)
        for seat in (0, 1):
            farm = shared_obs["farms"][seat]
            encode_tiles(farm["tiles"], d, t, tiles[seat, t])
            money[seat, t] = float(farm.get("money", 0.0))
            hires_today[seat, t] = _u8(farm.get("hires_today", 0))
            quadrants[seat, t] = sum(QUADRANT_BIT.get(q, 0) for q in farm.get("unlocked_quadrants", []))
            units = [farm["farmer"]] + list(farm.get("hands", []))
            n_units[seat, t] = len(units)
            for u, pos in enumerate(units[:MAX_UNITS]):
                unit_pos[seat, t, u] = (pos[0], pos[1])
            private = step[seat]["observation"].get("private") or {}
            for i, it in enumerate(ITEMS):
                shed[seat, t, i] = max(-32768, min(32767, int((private.get("shed") or {}).get(it, 0))))
            for i, c in enumerate(CROPS):
                seeds[seat, t, i] = max(-32768, min(32767, int((private.get("seeds") or {}).get(c, 0))))
            for u, inv in enumerate((private.get("inventories") or [])[:MAX_UNITS]):
                for it, n in (inv or {}).items():
                    if it in ITEM_ID:
                        unit_inv[seat, t, u, ITEM_ID[it] - 1] = _u8(n)
            if t + 1 < T:
                action = step_action = steps[t + 1][seat].get("action") or {}
                if not isinstance(action, dict):
                    action = {}
                ops = [action.get("farmer")] + list(action.get("hands") or []) if isinstance(action.get("hands"), list) else [action.get("farmer")]
                for u, unit_op in enumerate(ops[:MAX_UNITS]):
                    op[seat, t, u], op_arg[seat, t, u], op_count[seat, t, u] = encode_unit_action(unit_op)
                orders = action.get("market") or []
                if isinstance(orders, list):
                    n_orders[seat, t] = min(32767, len(orders))
                    for k, order in enumerate(orders[:MAX_ORDERS]):
                        m_type[seat, t, k], m_item[seat, t, k], m_qty[seat, t, k] = encode_order(order)

    info = replay.get("info") or {}
    meta = {
        "encoding_version": ENCODING_VERSION,
        "episode_id": info.get("EpisodeId"),
        "seed": info.get("seed"),
        "teams": list(info.get("TeamNames") or []),
        "rewards": list(replay.get("rewards") or []),
        "statuses": list(replay.get("statuses") or []),
        "engine": replay.get("module_version"),
        "steps": T,
        "turns_per_day": tpd,
        "config": {k: replay["configuration"].get(k) for k in (
            "startingMoney", "shedCapacity", "weedSpawnChance", "townShopUnlockInterval",
            "townShopSellInterval", "townCenterSellInterval", "farmHandCostMult", "maxMarketOrdersPerTurn")},
    }
    return {
        "tiles": tiles, "unit_pos": unit_pos, "unit_inv": unit_inv, "n_units": n_units,
        "shed": shed, "seeds": seeds, "money": money, "hires_today": hires_today, "quadrants": quadrants,
        "prices": prices, "inventory": inventory, "shops": shops, "day": day, "hour": hour,
        "op": op, "op_arg": op_arg, "op_count": op_count,
        "m_type": m_type, "m_item": m_item, "m_qty": m_qty, "n_orders": n_orders,
        "meta": np.array(json.dumps(meta)),
    }


def save_encoded(arrays: dict, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp.npz")
    with open(tmp, "wb") as fh:
        np.savez_compressed(fh, **arrays)
    tmp.replace(path)
    return path


def load_encoded(episode_id: int) -> dict:
    with np.load(feature_path(episode_id)) as z:
        out = {k: z[k] for k in z.files}
    out["meta"] = json.loads(str(out["meta"]))
    return out


def decode_unit_action(op_id: int, arg: int, count: int) -> list:
    """The inverse of encode_unit_action, for checks."""
    if op_id <= 0:
        return ["PASS"]
    name = OPS[op_id - 1]
    if name == "PLANT":
        return [name, CROPS[arg - 1]] if arg else [name]
    if name in ("PLACE", "PICKUP"):
        return [name, ITEMS[arg - 1], int(count)] if arg else [name]
    return [name]
