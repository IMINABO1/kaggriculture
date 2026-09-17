"""Features for the job-level clone, shared by training (from encoded arrays) and the runtime
(from the observation). Numpy only, so the bundle needs no torch.

Tile channels follow research/encode.py: kind, crop or animal id, age, yield, tended, missed,
fertilizer days, decaying, cared, dung, care bonus, life. A step's planes are those twelve
scaled to about [0, 1] plus one plane counting the farm's units per tile; a step's scalars
are the shed, seeds, money, prices, market inventory, shop counts, day, hour, unit count and
quadrant bits; a unit's vector is its position, index, farmer flag and inventory.
"""

from __future__ import annotations

import numpy as np

N_TILE_CH = 12
TILE_SCALE = np.array([5, 10, 30, 6, 1, 2, 3, 1, 1, 1, 6, 5], dtype=np.float32)
N_PLANES = N_TILE_CH + 1
N_SCALARS = 12 + 5 + 1 + 9 + 9 + 8 + 4 + 4
N_UNIT = 2 + 1 + 1 + 12
MAX_UNITS = 20
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
ANIMALS = ("GOOSE", "COW", "SHEEP")
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
ITEMS = PRODUCTS + ANIMALS
SHOPS = ("BAKERY", "PIZZA_SHOP", "BRUNCH_SPOT", "YARN_STORE", "ICE_CREAM_SHOP", "PET_CAFE", "SMOOTHIE_SHOP", "FARMERS_MARKET")
STRUCTURE_ID = {"PASTURE": 9, "COOP": 10}
SHED_TILES = ((4, 4), (5, 4), (4, 5), (5, 5))


def encode_tiles(tiles, day: int, step: int) -> np.ndarray:
    """The observation's tile grid as [10, 10, 12] uint8, identical to research.encode.encode_tiles."""
    out = np.zeros((10, 10, N_TILE_CH), dtype=np.uint8)
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
                out[y, x, 1] = CROPS.index(tile["crop"]) + 1 if tile.get("crop") in CROPS else 0
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
                out[y, x, 1] = ANIMALS.index(tile["animal"]) + 6 if tile.get("animal") in ANIMALS else 0
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
    return out


def _u8(x) -> int:
    try:
        return max(0, min(255, int(x)))
    except (TypeError, ValueError):
        return 0


def step_planes(tiles_u8: np.ndarray, positions) -> np.ndarray:
    """[N_PLANES, 10, 10] float32 from a [10, 10, 12] uint8 grid and the farm's unit positions."""
    planes = np.empty((N_PLANES, 10, 10), dtype=np.float32)
    planes[:N_TILE_CH] = (tiles_u8.astype(np.float32) / TILE_SCALE).transpose(2, 0, 1)
    units = np.zeros((10, 10), dtype=np.float32)
    for x, y in positions:
        if 0 <= x < 10 and 0 <= y < 10:
            units[y, x] += 1.0
    planes[N_TILE_CH] = units
    return planes


def step_scalars(shed, seeds, money, prices, inventory, shop_counts, day, hour, n_units, quadrant_bits) -> np.ndarray:
    """shed [12] items, seeds [5] crops, prices/inventory [9] products, shop_counts [8], quadrant_bits 0-15."""
    return np.concatenate([
        np.minimum(np.asarray(shed, np.float32), 100) / 100.0,
        np.minimum(np.asarray(seeds, np.float32), 50) / 50.0,
        [np.log1p(max(0.0, float(money))) / 12.0],
        np.asarray(prices, np.float32) / 300.0,
        (np.asarray(inventory, np.float32) - 10000.0) / 500.0,
        np.asarray(shop_counts, np.float32) / 3.0,
        [day / 29.0, hour / 23.0, n_units / 15.0, 1.0],
        [1.0 if quadrant_bits & b else 0.0 for b in (1, 2, 4, 8)],
    ]).astype(np.float32)


def unit_vector(x, y, u, inv) -> np.ndarray:
    """inv [12] item counts."""
    return np.concatenate([[x / 9.0, y / 9.0, u / 15.0, 1.0 if u == 0 else 0.0], np.asarray(inv, np.float32) / 6.0]).astype(np.float32)


def destination_mask(tiles_u8: np.ndarray) -> np.ndarray:
    """[10, 10] bool: a unit may be sent to any tile that is not locked, and to the shed tiles always."""
    ok = tiles_u8[:, :, 0] != 1
    for x, y in SHED_TILES:
        ok[y, x] = True
    return ok
