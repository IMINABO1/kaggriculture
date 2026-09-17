"""A planned day: every unit gets a block of tiles and the ops to do at each, built once a day.

The public line's searched tapes spend the end game in crews: a few units walk the herd
(feed, care, collect, harvest, five or six pens each), the rest work column blocks of the
field doing several ops per stop (water a ready wheat, harvest it, replant, water the new
plant) with few moves and no hauling; the greedy per-turn assignment does 10% fewer work ops
with 40% more walking (journal 2026-09-17). From `PLAN_FROM_DAY` this module builds the
day's stops from the hour-0 observation, chains them nearest-neighbour from the shed, splits
the chain into one contiguous segment per unit balanced by cost, and the executor follows
the segments; a unit that finishes its segment joins the greedy pool for the rest of the day.
"""

from __future__ import annotations

import os

from agent import plan as P
from agent.executor import (
    CROPS,
    FERTILIZE_BEST,
    FERTILIZE_FROM_DAY,
    PRODUCE,
    SHED_TILES,
    crop_exhausted,
    crop_for_empty_tile,
    dist,
    needs_feed,
    water_adds_unit,
)

# 99 = off: the planner matches the greedy executor's production and banks the same while
# the tape banks 1.5k more against it (journal 2026-09-17); KAGG_PLAN_FROM_DAY=24 turns it on
PLAN_FROM_DAY = int(os.environ.get("KAGG_PLAN_FROM_DAY", 99))
PLAN_LAST_DAY = 28          # the last day keeps the greedy liquidation the search tuned
HERD_LOAD = 6               # pens per herd unit
MAX_HANDS = 14              # the fifteenth hand costs $610 a day, about what a unit-day of end-game work earns
ACT_HOURS = 24              # acting turns in a planned day
HAUL_VALUE = 1200           # carried produce worth this much is walked to the shed at once (1200 > 600 > 250 on the day-24 evaluator)
DROP_AT_SHED_VALUE = 100    # worth this much, a unit on a shed tile spends the turn dropping it
WAIT_FOR_INPUT_HOUR = 2     # a pickup the shed cannot serve yet waits this long: the hour-0 purchase lands at hour 1
RETURN_TO_SHED = False      # a segment ends with a walk home and a drop (field-only: -160 / -240 on the evaluator)
# ages at which the plan spreads fertilizer: the tape spreads 40 over days 24-28 where the
# greedy executor spreads 27 and sells the rest at $1-15; a wheat fertilized at age 3 still
# doubles two waterings (FERTILIZE_BEST in the executor allows age 2 only)
FERT_AGES = {"STRAWBERRY": (9, 11, 13, 15), "WHEAT": (2, 3), "CARROT": (2,)}
SPAWN_CYCLE = ((5, 4), (4, 5), (5, 5), (4, 4))  # where hands appear, in hire order, farmer at (4, 4)
ANIMAL_HARVEST_MIN = {True: 1, False: 2}


class Stop:
    __slots__ = ("pos", "ops")

    def __init__(self, pos, ops):
        self.pos, self.ops = pos, list(ops)


def plant_ops(x, y, day):
    crop = crop_for_empty_tile(x, y, day)
    return [["PLANT", crop], ["WATER"]] if crop else []


def tile_ops(tile, x, y, day, prices) -> list:
    """The ops worth doing on this tile today, in execution order."""
    if tile is None:
        return plant_ops(x, y, day)
    if tile == "LOCKED":
        return []
    kind = tile.get("kind")
    replant = plant_ops(x, y, day)
    if kind == "WEED":
        return [["DIG"]] + replant if replant else []  # a dig that frees nothing is a wasted turn
    if kind == "PLANT":
        if crop_exhausted(tile, day):
            return [["DIG"]] + replant if replant else []
        crop, cd = tile["crop"], CROPS[tile["crop"]]
        age = day - tile["planted_day"]
        ops = []
        fertilize = (FERTILIZE_FROM_DAY <= day < 29 and tile.get("fertilized_until_day", -1) < day
                     and age in FERT_AGES.get(crop, FERTILIZE_BEST.get(crop, ())))
        if fertilize:
            ops.append(["FERTILIZE"])
        # a watering is spare when the plant was watered yesterday and today's adds nothing:
        # no unit for a one-time crop, no doubled production for an ongoing one tonight
        must = tile.get("consecutive_unwatered", 0) >= 1
        if cd["ongoing"]:
            production_tonight = (day + 1 - tile["planted_day"] - cd["first"]) % cd["interval"] == 0 and age + 1 >= cd["first"]
            fertilized_tonight = fertilize or tile.get("fertilized_until_day", -1) >= day
            if not tile["watered_today"]:
                spare = not must and not (production_tonight and fertilized_tonight)
                ops.append(["WATER", "spare"] if spare else ["WATER"])
            if tile.get("yield_units", 0) > 0 and age >= cd["first"]:
                ops.append(["HARVEST"])
                if age >= cd["first"] + cd["interval"] * (cd["max_yield"] - 1) and replant:
                    ops += [["DIG"]] + replant  # its last yield: the tile goes to the next crop today
            return ops
        ready = age >= cd["ready"] or tile["yield_units"] >= cd["max_yield"] or age > cd["max_day"]
        if ready:
            if not tile["watered_today"] and water_adds_unit(tile, day):
                ops.append(["WATER"])
            ops.append(["HARVEST"])
            return ops + plant_ops(x, y, day)
        if not tile["watered_today"]:
            spare = not must and not water_adds_unit(tile, day)
            ops.append(["WATER", "spare"] if spare else ["WATER"])
        return ops
    if "animal" in tile:
        ops = []
        feed = needs_feed(tile, day, prices)
        if feed:
            ops.append(["FEED"])
        if not tile["cared_today"] and (feed or tile["fed_today"]):
            ops.append(["CARE"])
        if tile.get("fertilizer_available"):
            ops.append(["COLLECT_FERTILIZER"])
        if tile.get("yield_units", 0) >= ANIMAL_HARVEST_MIN[day >= 28]:
            ops.append(["HARVEST"])
        return ops
    return []


def chain(stops: list, start) -> list:
    """Nearest-neighbour order from `start`, ties by position."""
    left = list(stops)
    out = []
    pos = start
    while left:
        nxt = min(left, key=lambda s: (dist(pos, s.pos), s.pos))
        left.remove(nxt)
        out.append(nxt)
        pos = nxt.pos
    return out


def serpentine(stops: list) -> list:
    """Column bands: x ascending, y up one column and down the next, so a contiguous run of
    the sequence is a compact block of the field."""
    return sorted(stops, key=lambda s: (s.pos[0], s.pos[1] if s.pos[0] % 2 == 0 else -s.pos[1]))


def segment_cost(seg: list, start) -> int:
    cost, pos = 0, start
    for s in seg:
        cost += dist(pos, s.pos) + len(s.ops)
        pos = s.pos
    return cost


def pack(seq: list, cap: int, start) -> list[list]:
    """Cut a sequence into contiguous segments none of which costs more than `cap` (a segment
    that would exceed it on its first stop takes that stop alone)."""
    segments, current, acc = [], [], 0
    for s in seq:
        add = len(s.ops) + (dist(current[-1].pos, s.pos) if current else dist(start, s.pos))
        if current and acc + add > cap:
            segments.append(current)
            current, acc = [], 0
            add = len(s.ops) + dist(start, s.pos)
        current.append(s)
        acc += add
    if current:
        segments.append(current)
    return segments


def split(seq: list, k: int, start) -> list[list]:
    """At most k contiguous segments of a sequence with the smallest possible maximum cost."""
    if k <= 0 or not seq:
        return []
    lo = max(len(s.ops) + dist(start, s.pos) for s in seq)
    hi = segment_cost(seq, start)
    while lo < hi:
        mid = (lo + hi) // 2
        if len(pack(seq, mid, start)) <= k:
            hi = mid
        else:
            lo = mid + 1
    segments = pack(seq, lo, start)
    for seg in segments:  # walk in from the nearer end
        if dist(start, seg[-1].pos) < dist(start, seg[0].pos):
            seg.reverse()
    return segments


def drop_spare_waters(stops: list) -> None:
    for s in stops:
        s.ops = [op for op in s.ops if op != ["WATER", "spare"]]


def drop_plantings(stops: list, crop: str) -> None:
    """Remove the planting of `crop` and the watering that follows it (and a dig that only
    served it) from every stop."""
    for s in stops:
        ops = []
        skip_water = False
        for op in s.ops:
            if op[0] == "PLANT" and op[1] == crop:
                skip_water = True
                if ops and ops[-1] == ["DIG"]:
                    ops.pop()
                continue
            if skip_water and op[0] == "WATER":
                skip_water = False
                continue
            ops.append(op)
        s.ops = ops


def drop_fertilize(stops: list, tiles, crops: tuple) -> None:
    for s in stops:
        tile = tiles[s.pos[1]][s.pos[0]]
        if isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile.get("crop") in crops:
            s.ops = [op for op in s.ops if op[0] != "FERTILIZE"]


FIT_CUTS = 1                # how many of the cuts below a too-short day may take (1 = spare waterings only)


# what goes first when the day is too short for everything, cheapest per unit-turn first
def fit_to_day(field: list, tiles, k: int, start) -> list[list]:
    cap = ACT_HOURS - 1
    cuts = (
        lambda: drop_spare_waters(field),
        lambda: drop_plantings(field, "WHEAT"),
        lambda: drop_fertilize(field, tiles, ("WHEAT", "CARROT")),
        lambda: drop_plantings(field, "CARROT"),
    )
    segments = split(field, k, start)
    for cut in cuts[:FIT_CUTS]:
        if not segments or max(segment_cost(seg, start) for seg in segments) <= cap:
            break
        cut()
        field[:] = [s for s in field if s.ops]
        segments = split(field, k, start)
    return segments


# a stop's worth, so a segment the day cannot finish leaves its cheapest stops undone
STOP_VALUE = {"HARVEST": 3.0, "WATER": 2.0, "FERTILIZE": 2.0, "PLANT": 1.0, "DIG": 1.0, "FEED": 3.0, "CARE": 2.0,
              "COLLECT_FERTILIZER": 1.0, "PICKUP": 9.0}
ORDER_BY_VALUE = True


def stop_value(stop, tiles) -> float:
    best = 0.0
    tile = tiles[stop.pos[1]][stop.pos[0]]
    for op in stop.ops:
        v = STOP_VALUE.get(op[0], 0.0)
        if op[0] == "WATER":
            if len(op) > 1 and op[1] == "spare":
                v = 0.0
            elif isinstance(tile, dict) and tile.get("consecutive_unwatered", 0) >= 1:
                v = 3.0
        best = max(best, v)
    return best


def order_segment(seg: list, tiles, start) -> list:
    """Most valuable stops first, each class walked nearest-neighbour from where the last ended."""
    if not ORDER_BY_VALUE:
        return seg
    classes: dict[float, list] = {}
    for s in seg:
        classes.setdefault(stop_value(s, tiles), []).append(s)
    out, pos = [], start
    for value in sorted(classes, reverse=True):
        part = chain(classes[value], pos)
        out += part
        pos = part[-1].pos
    return out


def spawn_positions(n_units: int) -> list:
    return [(4, 4)] + [SPAWN_CYCLE[(k - 1) % 4] for k in range(1, n_units)]


def build_dayplan(me, private, day, prices, n_units: int, positions=None) -> dict:
    """Stops per unit for today. `positions` are the units' tiles now (hour 1) or None for
    the expected spawn tiles (hour 0, hands not hired yet)."""
    tiles = me["tiles"]
    herd, field = [], []
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            ops = tile_ops(tile, x, y, day, prices)
            if not ops:
                continue
            (herd if isinstance(tile, dict) and "animal" in tile else field).append(Stop((x, y), ops))
    shed_pos = (4, 4)
    field = serpentine(field)
    if positions is None:
        # hour 0, before the hires: as many hands as the day's work needs, up to MAX_HANDS
        need = -(-(segment_cost(chain(herd, shed_pos), shed_pos) + segment_cost(field, shed_pos)) // (ACT_HOURS - 3))
        n_units = min(1 + MAX_HANDS, max(n_units, need))
        positions = spawn_positions(n_units)
    positions = list(positions)
    n_units = len(positions)
    n_herd = min(max(0, n_units - 1), -(-len(herd) // HERD_LOAD)) if herd else 0
    segments = split(chain(herd, shed_pos), n_herd, shed_pos)
    segments += [order_segment(seg, tiles, shed_pos) for seg in fit_to_day(field, tiles, n_units - len(segments), shed_pos)]

    # each segment goes to the free unit nearest its first stop
    units: dict[int, list] = {}
    free = list(range(n_units))
    shed = private["shed"]
    # the market buys today's feed at hour 0 (agent/market.py, step 3) and it lands at hour 1,
    # so the herd's pickups are planned for the whole need, not for what the shed holds now
    wheat_left = max(shed.get("WHEAT", 0), sum(1 for s in herd for op in s.ops if op[0] == "FEED"))
    fert_left = shed.get("FERTILIZER", 0)
    for seg in segments:
        ui = min(free, key=lambda u: (dist(positions[u], seg[0].pos), u))
        free.remove(ui)
        pre = []
        inv = private["inventories"][ui] if ui < len(private["inventories"]) else {}
        n_feed = sum(1 for s in seg for op in s.ops if op[0] == "FEED") - inv.get("WHEAT", 0)
        if n_feed > 0 and wheat_left > 0:
            n = min(n_feed, wheat_left)
            wheat_left -= n
            pre.append(["PICKUP", "WHEAT", n])
        n_fert = sum(1 for s in seg for op in s.ops if op[0] == "FERTILIZE") - inv.get("FERTILIZER", 0)
        if n_fert > 0:
            n = min(n_fert, fert_left)
            fert_left -= n
            if n > 0:
                pre.append(["PICKUP", "FERTILIZER", n])
            # fertilize ops beyond what this unit will carry are dropped from the tail
            short = n_fert - n
            for s in reversed(seg):
                while short > 0 and ["FERTILIZE"] in s.ops:
                    s.ops.remove(["FERTILIZE"])
                    short -= 1
        stops = ([Stop(nearest_shed(positions[ui]), pre)] if pre else []) + seg
        if RETURN_TO_SHED:
            stops.append(Stop(nearest_shed(seg[-1].pos), [["DROP"]]))  # the day's harvest sells tonight, ahead of the tape's morning lots
        units[ui] = stops
    wanted: dict[str, int] = {}
    for seg in segments:
        for s in seg:
            for op in s.ops:
                if op[0] == "PLANT":
                    wanted[op[1]] = wanted.get(op[1], 0) + 1
    return {"day": day, "n_units": n_units, "units": units, "plant_wanted": wanted, "hands": n_units - 1}


def nearest_shed(pos):
    return min(SHED_TILES, key=lambda t: (dist(pos, t), SHED_TILES.index(t)))


def op_allowed(op, tile, inv, day, shed_left, plant_left) -> bool:
    """Whether the op still makes sense on the tile as observed now."""
    kind = op[0]
    if kind == "DROP":
        return any(inv.get(p, 0) > 0 for p in PRODUCE)
    if kind == "PLANT":
        return tile is None and plant_left.get(op[1], 0) > 0
    if kind == "DIG":
        return tile is not None and tile != "LOCKED" and (tile.get("kind") == "WEED"
                                                           or (tile.get("kind") == "PLANT" and crop_exhausted(tile, day)))
    if not isinstance(tile, dict):
        return False
    if kind == "WATER":
        return tile.get("kind") == "PLANT" and not tile["watered_today"]
    if kind == "FERTILIZE":
        return tile.get("kind") == "PLANT" and inv.get("FERTILIZER", 0) > 0 and tile.get("fertilized_until_day", -1) < day
    if kind == "HARVEST":
        if tile.get("yield_units", 0) <= 0:
            return False
        return "animal" in tile or day - tile["planted_day"] >= CROPS[tile["crop"]]["first"]
    if kind == "FEED":
        return "animal" in tile and not tile["fed_today"] and inv.get("WHEAT", 0) > 0
    if kind == "CARE":
        return "animal" in tile and not tile["cared_today"]
    if kind == "COLLECT_FERTILIZER":
        return "animal" in tile and bool(tile.get("fertilizer_available"))
    return False


def follow(stops: list, pos, tiles, inv, day, hour, shed_left, plant_left, prices):
    """The next action for a unit on its segment, or None once the segment is spent; ops
    whose precondition no longer holds are dropped. A unit on a shed tile drops what it
    carries, and one carrying more than `HAUL_VALUE` walks it home first."""
    from agent.executor import step_toward

    keep = {item for s in stops for op in s.ops
            for item in (("WHEAT",) if op[0] == "FEED" else ("FERTILIZER",) if op[0] == "FERTILIZE" else ())}
    value = sum(inv.get(p, 0) * prices.get(p, 0) for p in PRODUCE if p not in keep)
    at_shed = pos in SHED_TILES
    # a herd unit feeds before it hauls: a haul in the middle of its round leaves pens unfed
    if value > 0 and ((at_shed and value >= DROP_AT_SHED_VALUE) or (value >= HAUL_VALUE and "WHEAT" not in keep)):
        if not at_shed:
            return [step_toward(pos, nearest_shed(pos))]
        if keep:
            item = max((p for p in PRODUCE if inv.get(p, 0) > 0 and p not in keep), key=lambda p: inv[p] * prices.get(p, 0))
            return ["PLACE", item, int(inv[item])]
        return ["DROP"]
    while stops:
        stop = stops[0]
        if pos != stop.pos:
            return [step_toward(pos, stop.pos)]
        tile = tiles[stop.pos[1]][stop.pos[0]]
        while stop.ops:
            op = stop.ops.pop(0)
            if op[0] == "PICKUP":
                have, want = shed_left.get(op[1], 0), int(op[2])
                if have <= 0:
                    if hour <= WAIT_FOR_INPUT_HOUR:
                        stop.ops.insert(0, op)
                        return ["PASS"]
                    continue
                n = min(want, have)
                shed_left[op[1]] -= n
                if n < want and hour <= WAIT_FOR_INPUT_HOUR:
                    stop.ops.insert(0, ["PICKUP", op[1], want - n])
                return ["PICKUP", op[1], n]
            if op_allowed(op, tile, inv, day, shed_left, plant_left):
                if op[0] == "PLANT":
                    plant_left[op[1]] -= 1
                return ["WATER"] if op[0] == "WATER" else op
        stops.pop(0)
    return None
