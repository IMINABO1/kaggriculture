"""Numpy forward pass of the job-level clone (scripts/learn/train_jobs.py's JobNet), so the
bundle needs no torch. Weights come from agent/clone_weights.npz (scripts/learn/export_clone.py).
"""

from __future__ import annotations

import os

import numpy as np

N_CLASSES = 14
TILE_X = np.tile(np.arange(10), 10)
TILE_Y = np.repeat(np.arange(10), 10)


def relu(x):
    return np.maximum(x, 0.0)


def conv3x3(x: np.ndarray, w: np.ndarray, b: np.ndarray) -> np.ndarray:
    """x [C, 10, 10], w [O, C, 3, 3] (torch layout), b [O] -> [O, 10, 10], padding 1."""
    C, H, W = x.shape
    xp = np.zeros((C, H + 2, W + 2), dtype=np.float32)
    xp[:, 1:-1, 1:-1] = x
    out = np.tile(b[:, None, None].astype(np.float32), (1, H, W))
    for dy in range(3):
        for dx in range(3):
            patch = xp[:, dy:dy + H, dx:dx + W].reshape(C, -1)          # [C, 100]
            out += (w[:, :, dy, dx] @ patch).reshape(-1, H, W)
    return out


def linear(x: np.ndarray, w: np.ndarray, b: np.ndarray) -> np.ndarray:
    return x @ w.T + b


class CloneNet:
    def __init__(self, weights: dict):
        self.w = {k: np.asarray(v, dtype=np.float32) for k, v in weights.items()}

    @classmethod
    def load(cls, path: str | None = None) -> "CloneNet":
        path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "clone_weights.npz")
        with np.load(path) as z:
            return cls({k: z[k] for k in z.files})

    def trunk(self, planes: np.ndarray) -> np.ndarray:
        x = planes
        for i in (0, 2, 4, 6):
            x = relu(conv3x3(x, self.w[f"trunk.{i}.weight"], self.w[f"trunk.{i}.bias"]))
        return x.reshape(x.shape[0], -1)                                   # [ch, 100]

    def unit_state(self, flat: np.ndarray, scal: np.ndarray, units: np.ndarray, upos: np.ndarray) -> np.ndarray:
        """flat [ch, 100]; units [U, N_UNIT]; upos [U, 2] -> h [U, 256]."""
        idx = upos[:, 1] * 10 + upos[:, 0]
        f_at = flat[:, idx].T                                              # [U, ch]
        pooled = np.tile(flat.mean(1), (len(idx), 1))
        x = np.concatenate([f_at, pooled, units, np.tile(scal, (len(idx), 1))], axis=1)
        x = relu(linear(x, self.w["unit_mlp.0.weight"], self.w["unit_mlp.0.bias"]))
        return relu(linear(x, self.w["unit_mlp.2.weight"], self.w["unit_mlp.2.bias"]))

    def dest_logits(self, flat: np.ndarray, h: np.ndarray, upos: np.ndarray, dmask: np.ndarray) -> np.ndarray:
        q = linear(h, self.w["query.weight"], self.w["query.bias"])        # [U, ch]
        logits = (q @ flat) / 8.0 + linear(flat.T, self.w["tile_w.weight"], self.w["tile_w.bias"]).reshape(1, -1)
        dx = TILE_X[None, :] - upos[:, 0:1]
        dy = TILE_Y[None, :] - upos[:, 1:2]
        logits = logits + self.w["b_dist"][np.clip(np.abs(dx) + np.abs(dy), 0, 18)] + self.w["b_rel"][np.clip(dy + 9, 0, 18), np.clip(dx + 9, 0, 18)]
        return np.where(dmask[None, :], logits, -1e4)

    def heads_at(self, flat: np.ndarray, h: np.ndarray, upos: np.ndarray, dest: np.ndarray):
        f_d = flat[:, dest].T                                              # [U, ch]
        rel = np.stack([(dest % 10 - upos[:, 0]) / 9.0, (dest // 10 - upos[:, 1]) / 9.0], axis=1).astype(np.float32)
        x = np.concatenate([h, f_d, rel], axis=1)
        x = relu(linear(x, self.w["op_mlp.0.weight"], self.w["op_mlp.0.bias"]))
        op = linear(x, self.w["op_mlp.2.weight"], self.w["op_mlp.2.bias"])
        hd = np.concatenate([h, f_d], axis=1)
        return op, linear(hd, self.w["arg_head.weight"], self.w["arg_head.bias"]), linear(hd, self.w["count_head.weight"], self.w["count_head.bias"])
