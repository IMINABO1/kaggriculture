"""The learned unit policy: every step the clone network scores, for each unit without a job,
the tile it should go to and the op to do there; the unit keeps that job while its op stays
possible, walks to the tile and does it. Tiles claimed by a job are off the greedy executor's
table; a unit the network gives no valid job falls back to the executor for the step.
"""

from __future__ import annotations

import numpy as np

from agent import dayplan as DP
from agent.clone_feats import ITEMS, CROPS, MAX_UNITS, SHED_TILES, destination_mask, encode_tiles, step_planes, step_scalars, unit_vector
from agent.clone_net import CloneNet
from agent.executor import ANIMAL_PRODUCT, CROPS as CROP_TABLE, FEED_DAILY_RATIO, crop_exhausted, step_toward

WORK_OPS = ("PLANT", "WATER", "HARVEST", "FERTILIZE", "FEED", "CARE", "COLLECT_FERTILIZER", "BUILD_COOP",
            "BUILD_PASTURE", "DIG", "PLACE", "PICKUP", "DROP")
SHOPS = ("BAKERY", "PIZZA_SHOP", "BRUNCH_SPOT", "YARN_STORE", "ICE_CREAM_SHOP", "PET_CAFE", "SMOOTHIE_SHOP", "FARMERS_MARKET")
SHOP_ID = {s: i + 1 for i, s in enumerate(SHOPS)}
QUADRANT_BIT = {"NW": 1, "NE": 2, "SW": 4, "SE": 8}
TOP_DESTS = 4               # candidate destinations tried per unit before giving up
WAIT_FOR_INPUT_HOUR = 2
HERD_GUARD_HOUR = int(__import__("os").environ.get("KAGG_HERD_GUARD", 16))  # an animal unfed since yesterday escapes tonight; 99 = off
# what a NONE prediction means: "pass" idles the unit as the team would, "greedy" hands it
# to the executor for the step (fidelity 0.69 against 0.67 and -50.6k against -54.4k vs
# v41 with the six-epoch weights, journal 2026-09-17; KAGG_CLONE_NONE overrides)
NONE_MEANS = __import__("os").environ.get("KAGG_CLONE_NONE", "greedy")
_NET = None


def net() -> CloneNet:
    global _NET
    if _NET is None:
        _NET = CloneNet.load()
    return _NET


def possible(op, tile, inv, shed, seeds, day, plant_left) -> bool:
    """Whether the op can be executed on the tile now (the engine's preconditions)."""
    kind = op[0]
    if kind == "PICKUP":
        return shed.get(op[1], 0) > 0
    if kind == "DROP":
        return any(v > 0 for v in inv.values())
    if kind == "PLACE":
        item = op[1]
        if item in ("COW", "SHEEP", "GOOSE"):
            structure = "COOP" if item == "GOOSE" else "PASTURE"
            if isinstance(tile, dict) and tile.get("kind") == structure and "animal" not in tile:
                return inv.get(item, 0) > 0
        return inv.get(item, 0) > 0
    if kind == "PLANT":
        return tile is None and plant_left.get(op[1], 0) > 0
    if kind in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is None
    if kind == "DIG":
        return isinstance(tile, dict) and (tile.get("kind") == "WEED" or (tile.get("kind") == "PLANT" and crop_exhausted(tile, day)))
    if not isinstance(tile, dict):
        return False
    if kind == "WATER":
        return tile.get("kind") == "PLANT" and not tile["watered_today"]
    if kind == "FERTILIZE":
        return tile.get("kind") == "PLANT" and inv.get("FERTILIZER", 0) > 0 and tile.get("fertilized_until_day", -1) < day
    if kind == "HARVEST":
        if tile.get("yield_units", 0) <= 0:
            return False
        return "animal" in tile or day - tile["planted_day"] >= CROP_TABLE[tile["crop"]]["first"]
    if kind == "FEED":
        return "animal" in tile and not tile["fed_today"] and inv.get("WHEAT", 0) > 0
    if kind == "CARE":
        return "animal" in tile and not tile["cared_today"]
    if kind == "COLLECT_FERTILIZER":
        return "animal" in tile and bool(tile.get("fertilizer_available"))
    return False


def decode_op(cls: int, arg: int, count: int) -> list:
    name = WORK_OPS[cls - 1]
    if name == "PLANT":
        return [name, CROPS[max(0, min(4, arg - 1))]]
    if name in ("PICKUP", "PLACE"):
        return [name, ITEMS[max(0, min(11, arg - 1))], max(1, count)]
    return [name]


def features(obs, me, private, day, hour, positions, invs):
    tiles_u8 = encode_tiles(me["tiles"], day, day * 24 + hour)
    planes = step_planes(tiles_u8, positions)
    shop_counts = np.zeros(8, np.float32)
    for s in obs["town"].get("unlocked_shops", []):
        if s in SHOP_ID:
            shop_counts[SHOP_ID[s] - 1] += 1
    prices = obs["market"]["prices"]
    inventory = obs["market"]["inventory"]
    products = ITEMS[:9]
    scal = step_scalars([private["shed"].get(it, 0) for it in ITEMS], [private["seeds"].get(c, 0) for c in CROPS], me["money"],
                        [prices.get(p, 0) for p in products], [inventory.get(p, 10000) for p in products], shop_counts, day, hour,
                        len(positions), sum(QUADRANT_BIT.get(q, 0) for q in me["unlocked_quadrants"]))
    units = np.stack([unit_vector(x, y, u, [invs[u].get(it, 0) for it in ITEMS]) for u, (x, y) in enumerate(positions)])
    return planes, scal, units, destination_mask(tiles_u8).ravel()


def act_units(obs, day, hour, state, me, private, positions, invs, shed_left, plant_left) -> dict:
    """Per unit index, the action from its job (None when the network gives no valid job).
    Jobs are kept in state["clone_jobs"] as (dest, op) and cleared at the day change."""
    if state.get("clone_day") != day:
        state["clone_day"], state["clone_jobs"] = day, {}
    jobs: dict = state["clone_jobs"]
    stats = state.setdefault("clone_stats", {"kept": 0, "done": 0, "dropped_on_arrival": 0, "dropped_en_route": 0,
                                              "new": 0, "none": 0, "no_job": 0, "seed_wanted": 0, "immediate": 0})
    tiles = me["tiles"]
    n = min(len(positions), MAX_UNITS)
    planes, scal, units, dmask = features(obs, me, private, day, hour, positions[:n], invs[:n])
    model = net()
    flat = model.trunk(planes)
    upos = np.array(positions[:n], dtype=np.int64)
    h = model.unit_state(flat, scal, units, upos)
    dest_logits = model.dest_logits(flat, h, upos, dmask)
    claimed = {jobs[u][0] for u in jobs if u < n}
    out: dict[int, list] = {}
    # the herd guard: from HERD_GUARD_HOUR an animal that would escape tonight pulls the
    # nearest unit off its model job, and the greedy executor feeds it with its urgency rules
    guarded: set[int] = set()
    if hour >= HERD_GUARD_HOUR:
        prices = obs["market"]["prices"]
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if (isinstance(tile, dict) and "animal" in tile and not tile["fed_today"] and tile.get("consecutive_unfed", 0) >= 1
                        and prices.get(ANIMAL_PRODUCT[tile["animal"]], 0) >= FEED_DAILY_RATIO * prices.get("WHEAT", 25)):
                    # only an animal whose product is worth its feed; the team lets the rest go
                    free = [u for u in range(n) if u not in guarded]
                    if free:
                        u = min(free, key=lambda k: abs(positions[k][0] - x) + abs(positions[k][1] - y))
                        guarded.add(u)
                        jobs.pop(u, None)
                        stats["guard"] = stats.get("guard", 0) + 1
    for u in range(n):
        if u in guarded:
            continue
        pos = positions[u]
        inv = invs[u]
        job = jobs.get(u)
        if job is not None:
            dest, op = job
            tile = tiles[dest[1]][dest[0]]
            if pos == dest:
                if possible(op, tile, inv, shed_left, private["seeds"], day, plant_left):
                    out[u] = _execute(op, inv, shed_left, plant_left)
                    stats["done"] += 1
                else:
                    stats["dropped_on_arrival"] += 1
                del jobs[u]
                if u in out:
                    continue
            else:
                if op[0] in ("PICKUP", "DROP", "PLACE") or possible(op, tile, inv, shed_left, private["seeds"], day, plant_left):
                    out[u] = [step_toward(pos, dest)]
                    stats["kept"] += 1
                    continue
                stats["dropped_en_route"] += 1
                del jobs[u]
        # a new job: the best destination not claimed by another unit, and the op there
        order = np.argsort(-dest_logits[u])[:TOP_DESTS]
        for d in order:
            dest = (int(d % 10), int(d // 10))
            op_l, arg_l, cnt_l = model.heads_at(flat, h[u:u + 1], upos[u:u + 1], np.array([d]))
            cls = int(np.argmax(op_l[0]))
            if cls == 0:
                stats["none"] += 1
                if NONE_MEANS == "pass":
                    out[u] = ["PASS"]
                break
            op = decode_op(cls, int(np.argmax(arg_l[0])), int(np.argmax(cnt_l[0])))
            tile = tiles[dest[1]][dest[0]]
            if op[0] == "FERTILIZE" and inv.get("FERTILIZER", 0) <= 0 and shed_left.get("FERTILIZER", 0) > 0:
                # fetch the fertilizer first; the model decides again once it is in hand
                op, dest = ["PICKUP", "FERTILIZER", min(4, shed_left["FERTILIZER"])], DP.nearest_shed(pos)
                tile = tiles[dest[1]][dest[0]]
                stats["fert_fetch"] = stats.get("fert_fetch", 0) + 1
            if op[0] == "PLANT" and tile is None and plant_left.get(op[1], 0) <= 0:
                wanted = state.setdefault("clone_seed_wanted", {})
                wanted[op[1]] = wanted.get(op[1], 0) + 1   # the market buys it next turn
                stats["seed_wanted"] += 1
                stats[f"seed_wanted_{op[1]}_h{'late' if hour > 20 else 'day'}"] = stats.get(f"seed_wanted_{op[1]}_h{'late' if hour > 20 else 'day'}", 0) + 1
                continue
            if op[0] in ("PICKUP", "DROP", "PLACE") and dest not in SHED_TILES and not (op[0] == "PLACE" and op[1] in ("COW", "SHEEP", "GOOSE")):
                continue
            if dest in claimed and op[0] not in ("PICKUP", "DROP", "PLACE"):
                continue
            if op[0] == "PICKUP" and shed_left.get(op[1], 0) <= 0 and hour <= WAIT_FOR_INPUT_HOUR:
                jobs[u] = (dest, op)
                out[u] = ["PASS"] if pos == dest else [step_toward(pos, dest)]
                break
            if pos == dest:
                if possible(op, tile, inv, shed_left, private["seeds"], day, plant_left):
                    out[u] = _execute(op, inv, shed_left, plant_left)
                    stats["immediate"] += 1
                    break
                continue
            if op[0] in ("PICKUP", "DROP", "PLACE") or possible(op, tile, inv, shed_left, private["seeds"], day, plant_left):
                jobs[u] = (dest, op)
                claimed.add(dest)
                out[u] = [step_toward(pos, dest)]
                stats["new"] += 1
                break
        if u not in out and u not in jobs:
            stats["no_job"] += 1
    return out


def _execute(op, inv, shed_left, plant_left) -> list:
    if op[0] == "PICKUP":
        n = min(int(op[2]), shed_left.get(op[1], 0))
        shed_left[op[1]] -= n
        return ["PICKUP", op[1], n]
    if op[0] == "PLANT":
        plant_left[op[1]] -= 1
    if op[0] == "PLACE":
        return ["PLACE", op[1], min(int(op[2]), inv.get(op[1], 0))]
    return list(op)
