"""Per-turn assignment of unit actions from the plan and the live farm.

Every turn the farm is read into a list of jobs (feed this animal, water that plant, plant
this tile, ...). Units act in order: a unit standing on a tile with a job it can do does it;
a shed-adjacent unit picks up what the outstanding jobs need or deposits what it carries;
otherwise it walks one step toward the cheapest job by distance plus priority. Nothing is
remembered between turns except the plan; the observation is re-read every turn, so a weed,
an escaped animal or a failed purchase is simply seen next turn.
"""

from __future__ import annotations

from agent import plan as P

# "ready" is the age at which daily watering has filled the yield (1 + watered days in the
# bonus window): a one-time crop is harvested once watered on that day, or later.
CROPS = {
    "WHEAT": {"first": 2, "max_day": 4, "ready": 4, "max_yield": 6, "ongoing": False, "interval": 0},
    "CARROT": {"first": 2, "max_day": 3, "ready": 3, "max_yield": 4, "ongoing": False, "interval": 0},
    "TOMATO": {"first": 8, "max_day": 8, "ready": 8, "max_yield": 4, "ongoing": True, "interval": 1},
    "STRAWBERRY": {"first": 10, "max_day": 10, "ready": 10, "max_yield": 4, "ongoing": True, "interval": 2},
    "MELON": {"first": 10, "max_day": 12, "ready": 10, "max_yield": 6, "ongoing": False, "interval": 0},
}
PRODUCE = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
INPUTS = ("WHEAT", "FERTILIZER", "COW", "SHEEP", "GOOSE")
SHED_TILES = ((4, 4), (5, 4), (4, 5), (5, 5))
STRAWBERRY_TILES = set(P.STRAWBERRIES_NW + P.STRAWBERRIES_NE + P.STRAWBERRIES_SW)
PASTURE_TILES = P.PASTURES_NW + P.PASTURES_NE
STRUCTURE_TILES = set(PASTURE_TILES) | set(P.COOPS_NW)
# ages at which one FERTILIZE (3 days) doubles the most yield: strawberry productions land at
# ages 10, 12, 14, 16 (end of days 9, 11, 13, 15), wheat's bonus window is ages 2-4
# strawberries: every production age not already covered (a shot at 9 covers 9 and 11); wheat
# and carrots at the start of their bonus window
FERTILIZE_BEST = {"STRAWBERRY": (9, 11, 13, 15), "WHEAT": (2,), "CARROT": (2,)}
FERTILIZE_ANY = {}
FERTILIZE_PRIO = {"STRAWBERRY": 0.5, "WHEAT": 3.0, "CARROT": 4.5}
PICKUP_CAP = {"WHEAT": 6, "FERTILIZER": 4, "COW": 1, "SHEEP": 1, "GOOSE": 1}
LAST_PLANT_HOUR = 22
LIQUIDATION_HOUR = 15
DEPOSIT_VALUE = 250         # carried produce worth this much walks to the shed when nothing is nearer (D3)
DEPOSIT_URGENT_VALUE = 1800  # worth this much, the walk comes before any other job
URGENCY_FROM_HOUR = 13      # feeding and must-watering climb over other work from this hour
URGENCY_PER_HOUR = 1.5
ON_TILE_BONUS = -10.0       # a job under the unit's feet comes before walking to an ordinary one
FEED_DEADLINE_HOUR = 18     # from here an unfed animal outranks everything but the last melons
FEEDER_LOAD = 3             # animals one morning feeder takes on (feed, care, collect, harvest)
SPARE_WATER_HOUR = 18       # from here a plant not yet watered is worth a walk
LAST_ACT_HOUR = 22          # step 718 is the last executed action
LATE_HARVEST_HOUR = 19      # a ready crop still unwatered by now is taken, freeing the tile tonight
STICKY_BONUS = -4.0         # a unit keeps the job it set out for unless another beats it by this

# priority weights added to walking distance; lower wins
PRIO = {
    "FEED": 0.5, "PLACE": -3.0, "PLANT": -0.5, "BUILD": -2.5, "WATER": 2.0, "HARVEST": 2.0,
    "FERTILIZE": 4.0, "DIG": 4.0, "CARE": 2.0, "COLLECT": 5.5, "WATER_SPARE": 7.0,
    "WATER_MUST": 1.5,
}
FERTILIZE_FROM_DAY = 12     # earlier, every fertilizer sold at $90-100 is what buys the herd
# a melon dump that lands before the opponent's is worth more than any other job that day;
# strawberries are worth hauling ahead of wheat
URGENT = -20.0              # beats a job under another unit's feet from ten tiles away
HARVEST_PRIO = {"MELON": URGENT, "STRAWBERRY": 1.5}
PLANT_PRIO = {"MELON": -1.0, "STRAWBERRY": -0.5, "CARROT": 1.0, "WHEAT": 2.5}
# a watering that adds a unit to a one-time crop is worth the unit ($225 for a melon), so it
# ranks with a must-watering; higher than that and it starves the herd (journal 2026-09-16)
WATER_YIELD_PRIO = {"MELON": PRIO["WATER_MUST"]}


def dist(a, b) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def step_toward(pos, target):
    dx, dy = target[0] - pos[0], target[1] - pos[1]
    if dx == 0 and dy == 0:
        return None
    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"
    return "SOUTH" if dy > 0 else "NORTH"


def is_shed_adjacent(pos) -> bool:
    return (pos[0], pos[1]) in SHED_TILES


def nearest_shed_tile(pos):
    return min(SHED_TILES, key=lambda t: (dist(pos, t), SHED_TILES.index(t)))


class Job:
    __slots__ = ("kind", "x", "y", "need", "arg", "taken", "prio")

    def __init__(self, kind, x, y, need=None, arg=None, prio=None):
        self.kind, self.x, self.y, self.need, self.arg, self.taken = kind, x, y, need, arg, False
        self.prio = PRIO[kind] if prio is None else prio

    @property
    def pos(self):
        return (self.x, self.y)

    def op(self):
        if self.kind in ("PLANT", "PLACE"):
            return [self.kind, self.arg]
        if self.kind == "BUILD":
            return ["BUILD_" + self.arg]
        if self.kind == "COLLECT":
            return ["COLLECT_FERTILIZER"]
        return [self.kind]


def crop_harvestable(tile, day, hour=0, wanted=None, seeds=None) -> bool:
    if tile.get("yield_units", 0) <= 0:
        return False
    cd = CROPS[tile["crop"]]
    age = day - tile["planted_day"]
    if age < cd["first"]:
        return False
    if cd["ongoing"]:
        return True
    if day >= 29:
        # water first while a watering still adds a unit, unless the day is running out
        window_start = (cd["max_day"] + 1) // 2
        adds = window_start <= age <= cd["max_day"] and tile["yield_units"] < cd["max_yield"]
        return tile["watered_today"] or not adds or hour >= FEED_DEADLINE_HOUR
    if tile["crop"] == "WHEAT" and wanted and wanted != "WHEAT" and seeds and seeds.get(wanted, 0) > 0:
        return True  # a wheat filler making way for the crop the tile is meant for
    if tile["yield_units"] >= cd["max_yield"] or age > cd["max_day"]:
        return True
    return age >= cd["ready"] and (tile["watered_today"] or hour >= LATE_HARVEST_HOUR)


def needs_water(tile, day) -> tuple:
    """(needed, must): every unwatered plant, "must" when a second unwatered day would weed it.

    Skipping off days saves nothing (the line's water count equals ours) and leaves no slack."""
    if tile["watered_today"]:
        return False, False
    return True, tile.get("consecutive_unwatered", 0) >= 1


def water_adds_unit(tile, day) -> bool:
    """A one-time crop gains a unit from each watering in its yield window (the engine's
    WATER rule: ages from half the max day to the max day, up to the max yield)."""
    cd = CROPS[tile["crop"]]
    if cd["ongoing"] or tile["yield_units"] >= cd["max_yield"]:
        return False
    age = day - tile["planted_day"]
    return (cd["max_day"] + 1) // 2 <= age <= cd["max_day"]


def crop_exhausted(tile, day) -> bool:
    """An ongoing crop that has fired its last yield and been picked clean: it weeds tonight."""
    cd = CROPS[tile["crop"]]
    if not cd["ongoing"] or tile.get("yield_units", 0) > 0:
        return False
    age = day - tile["planted_day"]
    last_age = cd["first"] + cd["interval"] * (cd["max_yield"] - 1)
    return age >= last_age


def target_crop(x, y, day):
    """The crop the plan wants on a tile today: the line's layout by tile and date."""
    if (x, y) in STRUCTURE_TILES:
        return "MELON" if day == P.MELON_DAY and (x, y) in P.MELONS_NW else None
    if day == P.MELON_DAY and (x, y) in P.MELONS_NW:
        return "MELON"
    if (x, y) in STRAWBERRY_TILES and P.STRAWBERRY_FIRST_DAY <= day <= P.STRAWBERRY_LAST_DAY:
        return "STRAWBERRY"
    # the line's 31 carrots go on the freed strawberry tiles; its wheat tiles run to day 27
    if (x, y) in STRAWBERRY_TILES and P.CARROT_FIRST_DAY <= day <= P.CARROT_LAST_DAY:
        return "CARROT"
    if day <= P.WHEAT_LAST_DAY:
        return "WHEAT"
    return None


def crop_for_empty_tile(x, y, day, seeds=None):
    """What to plant on an empty tile now: the target crop when its seed is in hand, else
    wheat as a filler (the line does this while strawberry seeds are still unaffordable,
    and takes the filler out at age 2-3 when the strawberry arrives)."""
    crop = target_crop(x, y, day)
    if crop is None:
        return None
    if seeds is not None and crop != "WHEAT" and seeds.get(crop, 0) <= 0 and day <= P.WHEAT_LAST_DAY:
        return "WHEAT"
    return crop


ANIMALS = {
    "GOOSE": {"first": 4, "interval": 1},
    "COW": {"first": 8, "interval": 2},
    "SHEEP": {"first": 6, "interval": 3},
}


ANIMAL_PRODUCT = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}
FEED_DAILY_RATIO = 1.2      # feed and care every day while the product is worth this much wheat


def needs_feed(tile, day, prices) -> bool:
    """Every fed-and-cared day banks one more unit of product for one wheat, so feed daily
    while the product is worth more than the wheat; otherwise only on production nights (the
    care bank pays out only if fed) and when a second unfed day would let the animal escape."""
    if tile["fed_today"]:
        return False
    if tile.get("consecutive_unfed", 0) >= 1:
        return True
    if prices.get(ANIMAL_PRODUCT[tile["animal"]], 0) >= FEED_DAILY_RATIO * prices.get("WHEAT", 25):
        return True
    a = ANIMALS[tile["animal"]]
    since = day + 1 - tile["placed_day"] - a["first"]
    return since >= 0 and since % a["interval"] == 0


def build_jobs(me, day, hour, shed, seeds, carried, prices) -> list:
    tiles = me["tiles"]
    jobs: list[Job] = []
    empty_structures = {"PASTURE": [], "COOP": []}
    pastures = coops = 0
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile is None or tile == "LOCKED":
                continue
            kind = tile.get("kind")
            if kind == "WEED":
                jobs.append(Job("DIG", x, y))
            elif kind == "PLANT":
                needed, must = needs_water(tile, day)
                if needed:
                    prio = PRIO["WATER_MUST"] if must else PRIO["WATER"]
                    if water_adds_unit(tile, day):
                        prio = min(prio, WATER_YIELD_PRIO.get(tile["crop"], prio))
                    if tile["crop"] == "MELON" and day - tile["planted_day"] >= CROPS["MELON"]["ready"]:
                        prio = HARVEST_PRIO["MELON"]  # the watering that makes the melon ready
                    jobs.append(Job("WATER", x, y, arg="must" if must else None, prio=prio))
                elif not tile["watered_today"]:
                    # not needed today, but a unit with time watering it buys a day of slack
                    spare = PRIO["WATER_SPARE"] if hour < SPARE_WATER_HOUR else PRIO["WATER"]
                    jobs.append(Job("WATER", x, y, prio=spare))
                if crop_harvestable(tile, day, hour, target_crop(x, y, day), seeds):
                    jobs.append(Job("HARVEST", x, y, prio=HARVEST_PRIO.get(tile["crop"], PRIO["HARVEST"])))
                elif crop_exhausted(tile, day):
                    jobs.append(Job("DIG", x, y, prio=PRIO["PLANT"]))  # the tile is a planting
                age = day - tile["planted_day"]
                if tile.get("fertilized_until_day", -1) < day and FERTILIZE_FROM_DAY <= day < 29:
                    # one fertilizer doubles two strawberry yields (about $200) but adds two
                    # wheat (about $80) or one carrot, so strawberries come first
                    base = FERTILIZE_PRIO.get(tile["crop"], PRIO["FERTILIZE"])
                    if age in FERTILIZE_BEST.get(tile["crop"], ()):
                        jobs.append(Job("FERTILIZE", x, y, need=("FERTILIZER", 1), prio=base))
                    elif age in FERTILIZE_ANY.get(tile["crop"], ()):
                        jobs.append(Job("FERTILIZE", x, y, need=("FERTILIZER", 1), prio=base + 1.0))
            elif "animal" in tile:
                if kind == "PASTURE":
                    pastures += 1
                else:
                    coops += 1
                feed = needs_feed(tile, day, prices)
                if feed:
                    jobs.append(Job("FEED", x, y, need=("WHEAT", 1)))
                if not tile["cared_today"] and (feed or tile["fed_today"]):
                    jobs.append(Job("CARE", x, y))
                if tile.get("fertilizer_available"):
                    jobs.append(Job("COLLECT", x, y))
                if tile.get("yield_units", 0) >= (1 if day >= 28 else 2):
                    jobs.append(Job("HARVEST", x, y, arg="animal"))
            elif kind in ("PASTURE", "COOP"):
                empty_structures[kind].append((x, y))
                if kind == "PASTURE":
                    pastures += 1
                else:
                    coops += 1

    # animals waiting in the shed go onto empty structures, nearest the shed first
    for animal in ("COW", "SHEEP", "GOOSE"):
        structure = P.ANIMAL_STRUCTURE[animal]
        free = sorted(empty_structures[structure], key=lambda t: dist(t, (4, 4)))
        for pos in free[: shed.get(animal, 0) + carried.get(animal, 0)]:
            jobs.append(Job("PLACE", pos[0], pos[1], need=(animal, 1), arg=animal))
            empty_structures[structure].remove(pos)

    # structures the plan calls for by today that do not exist yet
    want_pastures = P.cumulative(P.COW_TARGET, day) + P.cumulative(P.SHEEP_TARGET, day)
    want_coops = P.cumulative(P.GOOSE_TARGET, day)
    unlocked = set(me["unlocked_quadrants"])
    for structure, missing, order in (("PASTURE", want_pastures - pastures, PASTURE_TILES),
                                      ("COOP", want_coops - coops, P.COOPS_NW)):
        for (x, y) in order:
            if missing <= 0:
                break
            if P.quadrant(x, y) not in unlocked or tiles[y][x] is not None:
                continue
            jobs.append(Job("BUILD", x, y, arg=structure))
            missing -= 1

    # planting on empty tiles, limited by the seeds in hand (the engine drops every PLANT
    # of a crop when the requests exceed the seeds)
    if hour <= LAST_PLANT_HOUR:
        build_targets = {j.pos for j in jobs if j.kind == "BUILD"}
        budget = dict(seeds)
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile is not None or (x, y) in build_targets:
                    continue
                crop = crop_for_empty_tile(x, y, day, seeds)
                if crop and budget.get(crop, 0) > 0:
                    budget[crop] -= 1
                    jobs.append(Job("PLANT", x, y, arg=crop, prio=PLANT_PRIO.get(crop, PRIO["PLANT"])))
    return jobs


ANIMAL_JOBS = {"FEED", "CARE", "COLLECT", "PLACE"}


def is_animal_job(j) -> bool:
    return j.kind in ANIMAL_JOBS or (j.kind == "HARVEST" and j.arg == "animal")


def act_units(obs, day, hour, state):
    """Return (unit actions, summary) for this turn.

    Jobs are assigned globally, cheapest (unit, job) pair first, so the nearest unit takes
    each job whatever its index. A job on the unit's own tile beats walking to an ordinary
    one; a few urgent kinds (the melon dump, a valuable load, an animal still unfed late in
    the day) beat that. Pickups at the shed and deposits into it are jobs too. Each morning
    the first few hands are feeders: they take wheat from the shed and work the herd until
    every animal is fed and cared for, then join the field.
    """
    from agent import dayplan as DP  # dayplan imports this module's helpers

    me = obs["farms"][obs["player"]]
    private = obs["private"]
    shed = private["shed"]
    seeds = private["seeds"]
    prices = obs["market"]["prices"]
    money = me["money"]
    positions = [tuple(me["farmer"])] + [tuple(h) for h in me["hands"]]
    invs = [dict(inv) for inv in private["inventories"]]
    while len(invs) < len(positions):
        invs.append({})
    carried = {item: sum(inv.get(item, 0) for inv in invs) for item in INPUTS}

    jobs = build_jobs(me, day, hour, shed, seeds, carried, prices)
    if day >= 29:
        # nothing fed or planted today can be sold before the season ends; a watering
        # still counts when it adds a unit to a one-time crop harvested later today
        jobs = [j for j in jobs if j.kind in ("HARVEST", "COLLECT")
                or (j.kind == "WATER" and j.arg != "must" and j.prio == PRIO["WATER"])]
    liquidating = day >= 29 and hour >= LIQUIDATION_HOUR
    if liquidating:
        # only harvests a unit can still carry back to the shed by the last acting turn
        jobs = [j for j in jobs if j.kind == "HARVEST"
                and dist(j.pos, nearest_shed_tile(j.pos)) <= LAST_ACT_HOUR - hour - 1]

    # planned days: each unit follows its segment of stops; the tiles still on a segment are
    # off the greedy table, and a unit whose segment is spent joins the greedy pool
    planned: dict[int, list] = {}
    shed_left = dict(shed)
    plant_left = dict(seeds)
    if DP.PLAN_FROM_DAY <= day <= DP.PLAN_LAST_DAY:
        plan = state.get("dayplan")
        if plan is None or plan["day"] != day or (hour >= 1 and plan["n_units"] != len(positions)):
            expected = len(positions) if hour >= 1 else 1 + P.HANDS_BY_DAY[day]
            plan = DP.build_dayplan(me, private, day, prices, expected, positions if hour >= 1 else None)
            state["dayplan"] = plan
        for ui, stops in plan["units"].items():
            if ui >= len(positions):
                continue
            act = DP.follow(stops, positions[ui], me["tiles"], invs[ui], day, hour, shed_left, plant_left, prices)
            if act is not None:
                planned[ui] = act
                if act[0] == "PLANT":
                    plan["plant_wanted"][act[1]] = plan["plant_wanted"].get(act[1], 1) - 1
        busy = {s.pos for stops in plan["units"].values() for s in stops}
        for j in jobs:
            if j.pos in busy:
                j.taken = True
    if P.POLICY == "clone" and (not P.OPENING or day * 24 + hour >= P.OPENING_STEPS):
        from agent import clone

        planned.update(clone.act_units(obs, day, hour, state, me, private, positions, invs, shed_left, plant_left))
        claimed = {job[0] for job in state.get("clone_jobs", {}).values()}
        for j in jobs:
            if j.pos in claimed:
                j.taken = True

    # shed inputs the outstanding jobs still need beyond what units carry
    need_from_shed = {item: 0 for item in INPUTS}
    for j in jobs:
        if j.need and not j.taken:
            need_from_shed[j.need[0]] += j.need[1]
    for item in INPUTS:
        need_from_shed[item] -= carried[item]
    pending_inputs = {item for item in INPUTS if any(j.need and j.need[0] == item and not j.taken for j in jobs)}

    # the melon dump: every unit takes one melon tile first thing and walks its load straight
    # back, so the whole crop sells before the opponent's; the herd is fed afterwards
    melon_rush = any(j.prio == HARVEST_PRIO["MELON"] for j in jobs)
    if state.get("day") != day:
        unfed = 0 if melon_rush else sum(1 for j in jobs if j.kind == "FEED")
        n_feeders = min(max(0, len(positions) - 1), -(-unfed // FEEDER_LOAD))
        state.update(day=day, feeders=set(range(1, 1 + n_feeders)))
    if state["feeders"] and not any(j.kind in ("FEED", "CARE") for j in jobs):
        state["feeders"] = set()
    feeders = state["feeders"]

    def input_needed_by(inv, item):
        return item in pending_inputs and inv.get(item, 0) > 0

    # candidate (score, unit, job) pairs; a unit's walking target of the previous turn is
    # remembered by (kind, tile) and favoured so units stop re-targeting each other's jobs
    step = day * 24 + hour
    previous = state.get("targets", {}) if state.get("target_step") == step - 1 else {}
    pairs = []
    for ui, pos in enumerate(positions):
        if ui in planned:
            continue
        inv = invs[ui]
        feeder = ui in feeders
        haul_now = inv.get("MELON", 0) > 0   # not even the pasture under its feet on the way
        for ji, j in enumerate(jobs):
            if haul_now or (j.need and inv.get(j.need[0], 0) < j.need[1]):
                continue
            if feeder and not is_animal_job(j):
                continue
            d = dist(pos, j.pos)
            score = j.prio + ON_TILE_BONUS if d == 0 else d + j.prio
            if d > 0 and previous.get(ui) == (j.kind, j.x, j.y):
                score += STICKY_BONUS
            if j.kind == "FEED" or (j.kind == "WATER" and j.arg == "must"):
                score -= URGENCY_PER_HOUR * max(0, hour - URGENCY_FROM_HOUR)
                if hour >= FEED_DEADLINE_HOUR:
                    score = d + URGENT
            pairs.append((score, ui, ji))
        shed_tile = nearest_shed_tile(pos)
        d_shed = dist(pos, shed_tile)
        for item in INPUTS:
            if need_from_shed[item] <= 0 or shed.get(item, 0) <= 0 or inv.get(item, 0) >= PICKUP_CAP[item]:
                continue
            if feeder and item == "FERTILIZER":
                continue
            targets = [j for j in jobs if j.need and j.need[0] == item]
            if not targets:
                continue
            score = d_shed + 1 + min(dist(shed_tile, j.pos) for j in targets) + PRIO[targets[0].kind]
            pairs.append((score, ui, ("PICKUP", item, shed_tile)))
        value = sum(inv.get(p, 0) * prices.get(p, 0) for p in PRODUCE if not input_needed_by(inv, p))
        # while the bank is nearly empty every collected fertilizer is the next feed purchase
        deposit_value = min(DEPOSIT_VALUE, max(50, money))
        if value > 0 or (liquidating and any(inv.get(p, 0) > 0 for p in PRODUCE)):
            if value >= DEPOSIT_URGENT_VALUE or liquidating or haul_now:
                prio = URGENT
            elif value >= deposit_value or hour >= 21:
                prio = 1.0
            else:
                prio = 6.0
            # beside the shed a deposit costs one turn and no walk: treat it like an on-tile job
            score = ON_TILE_BONUS + 2.0 if d_shed == 0 else d_shed + prio
            pairs.append((score, ui, ("DEPOSIT", None, shed_tile)))
    pairs.sort(key=lambda t: (t[0], t[1], str(t[2])))

    assigned = [None] * len(positions)
    for ui, act in planned.items():
        assigned[ui] = ("PLANNED", act, 0, positions[ui])
    for score, ui, ji in pairs:
        if assigned[ui] is not None:
            continue
        if isinstance(ji, tuple):
            kind, item, shed_tile = ji
            if kind == "PICKUP":
                if need_from_shed[item] <= 0 or shed_left.get(item, 0) <= 0:
                    continue
                n = int(min(PICKUP_CAP[item] - invs[ui].get(item, 0), need_from_shed[item], shed_left[item]))
                if n <= 0:
                    continue
                need_from_shed[item] -= n
                shed_left[item] -= n
                assigned[ui] = ("PICKUP", item, n, shed_tile)
            else:
                assigned[ui] = ("DEPOSIT", None, 0, shed_tile)
            continue
        j = jobs[ji]
        if j.taken:
            continue
        if j.kind == "PLANT":
            if plant_left.get(j.arg, 0) <= 0:
                continue
            plant_left[j.arg] -= 1
        j.taken = True
        assigned[ui] = ("JOB", j, 0, j.pos)

    state["targets"] = {ui: (a[1].kind, a[1].x, a[1].y) for ui, a in enumerate(assigned)
                        if a is not None and a[0] == "JOB" and a[3] != positions[ui]}
    state["target_step"] = step

    actions = []
    for ui, pos in enumerate(positions):
        a = assigned[ui]
        if a is None:
            actions.append(["PASS"])
            continue
        kind, payload, n, target = a
        if kind == "PLANNED":
            actions.append(payload)
            continue
        move = step_toward(pos, target)
        if move:
            actions.append([move])
        elif kind == "JOB":
            actions.append(payload.op())
        elif kind == "PICKUP":
            actions.append(["PICKUP", payload, n])
        else:
            inv = invs[ui]
            keep = [p for p in INPUTS if input_needed_by(inv, p)]
            if keep:
                item = max((p for p in PRODUCE if inv.get(p, 0) > 0 and p not in keep),
                           key=lambda p: inv[p] * prices.get(p, 0), default=None)
                actions.append(["PLACE", item, int(inv[item])] if item else ["PASS"])
            else:
                actions.append(["DROP"])

    summary = {
        "jobs": len(jobs),
        "idle": sum(1 for a in actions if a == ["PASS"]),
        "unfed": sum(1 for j in jobs if j.kind == "FEED"),
        "unwatered": sum(1 for j in jobs if j.kind == "WATER"),
        "fertilize_pending": sum(1 for j in jobs if j.kind == "FERTILIZE" and not j.taken),
        "fertilize_taken": sum(1 for j in jobs if j.kind == "FERTILIZE" and j.taken),
    }
    return actions, summary
