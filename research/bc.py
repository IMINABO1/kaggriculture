"""Behaviour cloning of a per-unit policy from encoded replays (research/encode.py).

A sample is one unit at one step of one seat: what the unit saw (its farm as a tile grid
with a plane for its own tile and one for every unit of the farm, the opponent's grid, the
unit's inventory, the shed, seeds, money, prices, market inventory, shops, day, hour, unit
index) and what it did (the op, and the crop for a PLANT). The model is a small
convolutional net over the two grids with the scalars joined before the heads. Everything
here is numpy except the model, so the dataset side runs without torch.
"""

from __future__ import annotations

import numpy as np

from research.encode import ITEMS, CROPS, N_TILE_CH, OPS, PRODUCTS, load_encoded

N_OPS = len(OPS) + 1        # 0 = no action recorded
N_CROPS = len(CROPS) + 1
GRID_CH = 2 * N_TILE_CH + 2  # own grid, opponent grid, own-tile plane, units plane
SCALARS = len(ITEMS) + len(ITEMS) + len(CROPS) + 1 + len(PRODUCTS) + len(PRODUCTS) + 8 + 4 + 2
# unit inventory, shed, seeds, money, prices, market inventory, shop counts, day/hour/unit index/n_units, is-farmer flags


def grid_planes(z: dict, seat: int, t: int) -> np.ndarray:
    """[GRID_CH, 10, 10] float32 for one seat at one step, without the unit's own plane."""
    own = z["tiles"][seat, t].astype(np.float32)
    opp = z["tiles"][1 - seat, t].astype(np.float32)
    scale = np.array([5, 10, 30, 6, 1, 2, 3, 1, 1, 1, 6, 5], dtype=np.float32)
    own /= scale
    opp /= scale
    units = np.zeros((10, 10), dtype=np.float32)
    for u in range(int(z["n_units"][seat, t])):
        x, y = z["unit_pos"][seat, t, u]
        if x >= 0:
            units[y, x] += 1.0
    return np.concatenate([own.transpose(2, 0, 1), opp.transpose(2, 0, 1), np.zeros((1, 10, 10), np.float32), units[None]], axis=0)


def scalars(z: dict, seat: int, t: int, u: int) -> np.ndarray:
    shops = np.zeros(8, dtype=np.float32)
    for s in z["shops"][t]:
        if s > 0:
            shops[s - 1] += 1
    return np.concatenate([
        z["unit_inv"][seat, t, u].astype(np.float32) / 6.0,
        np.minimum(z["shed"][seat, t], 100).astype(np.float32) / 100.0,
        np.minimum(z["seeds"][seat, t], 50).astype(np.float32) / 50.0,
        [np.log1p(max(0.0, float(z["money"][seat, t]))) / 12.0],
        z["prices"][t].astype(np.float32) / 300.0,
        (z["inventory"][t].astype(np.float32) - 10000.0) / 500.0,
        shops / 3.0,
        [z["day"][t] / 29.0, z["hour"][t] / 23.0, u / 15.0, z["n_units"][seat, t] / 15.0],
        [1.0 if u == 0 else 0.0, 1.0 if z["quadrants"][seat, t] & 8 else 0.0],
    ]).astype(np.float32)


def game_samples(episode_id: int, seats=(0, 1), step_stride: int = 1, rng: np.random.Generator | None = None):
    """Yield (grid, scalars, op, crop) for every unit at every step of the chosen seats."""
    z = load_encoded(episode_id)
    T = z["tiles"].shape[1] - 1
    for seat in seats:
        for t in range(0, T, step_stride):
            base = grid_planes(z, seat, t)
            n = min(int(z["n_units"][seat, t]), z["op"].shape[2])
            for u in range(n):
                op = int(z["op"][seat, t, u])
                if op == 0:
                    continue
                g = base.copy()
                x, y = z["unit_pos"][seat, t, u]
                if x >= 0:
                    g[2 * N_TILE_CH, y, x] = 1.0
                crop = int(z["op_arg"][seat, t, u]) if OPS[op - 1] == "PLANT" else 0
                yield g, scalars(z, seat, t, u), op, crop


def batches(episode_ids, batch_size: int, seats=(0, 1), step_stride: int = 1, seed: int = 0):
    """Shuffle games, stream their samples, and yield stacked numpy batches."""
    rng = np.random.default_rng(seed)
    ids = list(episode_ids)
    rng.shuffle(ids)
    grids, scals, ops, crops = [], [], [], []
    for ep in ids:
        try:
            for g, s, op, crop in game_samples(ep, seats, step_stride, rng):
                grids.append(g)
                scals.append(s)
                ops.append(op)
                crops.append(crop)
                if len(ops) >= batch_size:
                    yield np.stack(grids), np.stack(scals), np.array(ops, np.int64), np.array(crops, np.int64)
                    grids, scals, ops, crops = [], [], [], []
        except (OSError, KeyError, ValueError):
            continue
    if ops:
        yield np.stack(grids), np.stack(scals), np.array(ops, np.int64), np.array(crops, np.int64)


def build_model():
    import torch
    from torch import nn

    class UnitPolicy(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv = nn.Sequential(
                nn.Conv2d(GRID_CH, 48, 3, padding=1), nn.ReLU(),
                nn.Conv2d(48, 64, 3, padding=1), nn.ReLU(),
                nn.Conv2d(64, 64, 3, padding=1), nn.ReLU(),
            )
            self.body = nn.Sequential(nn.Linear(64 * 100 + SCALARS, 512), nn.ReLU(), nn.Linear(512, 256), nn.ReLU())
            self.op_head = nn.Linear(256, N_OPS)
            self.crop_head = nn.Linear(256, N_CROPS)

        def forward(self, grid, scal):
            h = self.conv(grid).flatten(1)
            h = self.body(torch.cat([h, scal], dim=1))
            return self.op_head(h), self.crop_head(h)

    return UnitPolicy()
