"""Job-level labels from encoded replays: for every unit at every step, the tile it goes to
next and what it does there.

A unit's job at step t is its next non-move op within the same day (hands are re-indexed
every morning, so the scan never crosses a day boundary): the destination is the tile where
that op is performed, the op is the op, and `wait` is how many steps away it is. A unit that
only moves or passes until the day ends, or whose next op is more than `MAX_WAIT` steps
away, gets the NONE label. Shed ops (PICKUP, PLACE, DROP) have one of the four shed-access
tiles as their destination.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from research.encode import FEATURES, OPS, load_encoded

JOBS = FEATURES / "jobs"
MAX_WAIT = 12
FIRST_WORK_OP = OPS.index("PLANT") + 1      # op ids below this are PASS and the four moves
WORK_OPS = OPS[FIRST_WORK_OP - 1:]         # PLANT .. DROP, 13 classes; label class = op id - FIRST_WORK_OP + 1
N_CLASSES = len(WORK_OPS) + 1              # 0 = NONE


def jobs_path(episode_id: int) -> Path:
    return JOBS / f"{episode_id}.npz"


def label_game(z: dict, turns_per_day: int = 24) -> dict:
    op, arg, count, pos, n_units = z["op"], z["op_arg"], z["op_count"], z["unit_pos"], z["n_units"]
    S, T, U = op.shape
    T = T - 1                                   # the last observation carries no action
    lab_op = np.zeros((S, T, U), dtype=np.uint8)
    lab_arg = np.zeros((S, T, U), dtype=np.uint8)
    lab_count = np.zeros((S, T, U), dtype=np.int16)
    dest = np.full((S, T, U, 2), -1, dtype=np.int8)
    wait = np.zeros((S, T, U), dtype=np.uint8)
    valid = np.zeros((S, T, U), dtype=bool)
    for s in range(S):
        exists = (np.arange(U)[None, :] < n_units[s, :T, None])          # [T, U]
        work = exists & (op[s, :T] >= FIRST_WORK_OP)
        for d in range(0, T, turns_per_day):
            t0, t1 = d, min(d + turns_per_day, T)
            for u in range(U):
                if not exists[t0:t1, u].any():
                    continue
                w = np.flatnonzero(work[t0:t1, u]) + t0
                for t in range(t0, t1):
                    if not exists[t, u]:
                        continue
                    valid[s, t, u] = True
                    k = np.searchsorted(w, t)
                    if k >= len(w) or w[k] - t > MAX_WAIT:
                        continue
                    st = int(w[k])
                    lab_op[s, t, u] = op[s, st, u] - FIRST_WORK_OP + 1
                    lab_arg[s, t, u] = arg[s, st, u]
                    lab_count[s, t, u] = count[s, st, u]
                    dest[s, t, u] = pos[s, st, u]
                    wait[s, t, u] = st - t
    return {"lab_op": lab_op, "lab_arg": lab_arg, "lab_count": lab_count, "dest": dest, "wait": wait, "valid": valid}


def save_labels(episode_id: int, labels: dict) -> Path:
    JOBS.mkdir(parents=True, exist_ok=True)
    out = jobs_path(episode_id)
    tmp = out.with_suffix(".tmp.npz")
    with open(tmp, "wb") as fh:
        np.savez_compressed(fh, **labels)
    tmp.replace(out)
    return out


def load_labels(episode_id: int) -> dict:
    with np.load(jobs_path(episode_id)) as f:
        return {k: f[k] for k in f.files}


def build(episode_id: int) -> Path:
    return save_labels(episode_id, label_game(load_encoded(episode_id)))


def class_counts(labels: dict, seat: int | None = None) -> np.ndarray:
    lab, valid = labels["lab_op"], labels["valid"]
    if seat is not None:
        lab, valid = lab[seat], valid[seat]
    return np.bincount(lab[valid].ravel(), minlength=N_CLASSES)
