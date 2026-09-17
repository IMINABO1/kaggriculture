"""Replay a recorded opening line with the repairs a tape needs on a farm that is not the one it
was recorded on: plantings are trimmed to the seeds in hand (the engine drops every PLANT of a
crop when the requests exceed the seeds), a planned PLANT or BUILD on a weed becomes a DIG, and
the hands list is cut or padded to the hands that exist."""

from __future__ import annotations

import copy

PASS = ["PASS"]


class OpeningTape:
    def __init__(self, actions: list[dict]):
        self.actions = actions

    def __len__(self) -> int:
        return len(self.actions)

    def __call__(self, obs) -> dict:
        step = int(obs["step"])
        if step >= len(self.actions):
            return {"farmer": PASS, "hands": [], "market": []}
        action = copy.deepcopy(self.actions[step])
        me = obs["farms"][obs["player"]]
        tiles = me["tiles"]
        seeds = dict(obs["private"]["seeds"])
        positions = [me["farmer"]] + list(me["hands"])
        ops = [action.get("farmer") or PASS] + list(action.get("hands") or [])
        ops = ops[: len(positions)] + [PASS] * max(0, len(positions) - len(ops))
        for i, op in enumerate(ops):
            x, y = positions[i]
            tile = tiles[y][x]
            if op[0] == "PLANT" and len(op) > 1:
                if isinstance(tile, dict) and tile.get("kind") == "WEED":
                    ops[i] = ["DIG"]
                elif seeds.get(op[1], 0) <= 0:
                    ops[i] = PASS
                else:
                    seeds[op[1]] -= 1
            elif op[0] in ("BUILD_COOP", "BUILD_PASTURE") and isinstance(tile, dict) and tile.get("kind") == "WEED":
                ops[i] = ["DIG"]
        action["farmer"], action["hands"] = ops[0], ops[1:]
        return action
