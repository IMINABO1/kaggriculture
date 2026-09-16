"""Reduce a 30 MB replay to the facts the study needs.

A trace keeps both seats' full action streams (so the game can be replayed or used as an
opponent), per-day state series, per-event lists, and the stream hashes the community uses
to identify a line of play. Sell units are the executed amount, capped by what the shed held
before the turn's orders, because some agents request thousands of units every turn.

Stream hashing follows destbreso's normalisation byte for byte (canonical JSON per action,
NUL between turns, first 16 hex chars, steps[0] skipped) so values are comparable with
`stream_hashes.csv` from georgymamarin/kaggriculture-episodes.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter

from agent.tape import PASS, actions_from_replay
from research.market_replay import market_events

TRACE_VERSION = 2
HASH_CUTS = (24, 48, 100, 136, 200, 300, 400, 719)
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
ANIMALS = ("GOOSE", "COW", "SHEEP")
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
UNIT_OPS = (
    "PLANT",
    "WATER",
    "HARVEST",
    "FERTILIZE",
    "FEED",
    "CARE",
    "COLLECT_FERTILIZER",
    "BUILD_COOP",
    "BUILD_PASTURE",
    "DIG",
    "PLACE",
    "PICKUP",
    "DROP",
    "PASS",
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST",
)


def canon(action) -> bytes:
    return json.dumps(action or {}, sort_keys=True, separators=(",", ":")).encode()


def stream_hashes(actions: list[dict], cuts=HASH_CUTS) -> dict[str, str]:
    """Prefix hashes of the whole action stream, keyed 'h<turn>'."""
    h = hashlib.sha256()
    out = {}
    for t, a in enumerate(actions, start=1):
        h.update(canon(a))
        h.update(b"\0")
        if t in cuts:
            out[f"h{t}"] = h.hexdigest()[:16]
    return out


MOVES = {"NORTH", "SOUTH", "EAST", "WEST", "PASS"}
BUYABLE = {"WHEAT", "FERTILIZER"}


def order_is_valid(order) -> bool:
    """Structural validity of a market order; the engine silently drops the rest."""
    if not isinstance(order, list) or not order:
        return False
    kind = order[0]
    if kind in ("HIRE", "BUY_LAND"):
        return True
    if len(order) < 3:
        return False
    item = order[1]
    return (
        (kind == "BUY_PRODUCT" and item in BUYABLE)
        or (kind == "BUY_SEED" and item in CROPS)
        or (kind == "BUY_ANIMAL" and item in ANIMALS)
        or (kind == "SELL" and item in PRODUCTS)
    )


def invalid_order_count(actions: list[dict]) -> int:
    return sum(1 for a in actions for order in (a.get("market") or []) if not order_is_valid(order))


def plan_signature(actions: list[dict], upto: int) -> str:
    """Order-insensitive fingerprint of what was done through turn `upto`.

    Counts every non-movement unit op (with its arguments) and every executable market order,
    so two games that follow the same plan along different paths, or with hands in a different
    order, hash the same; two games that plant, buy, or sell differently do not. Orders the
    engine cannot execute are ignored: some agents emit them by the dozen, which would make
    every game look unique.
    """
    ops: Counter = Counter()
    for a in actions[:upto]:
        for op in unit_ops(a):
            if op[0] not in MOVES:
                ops["U " + " ".join(map(str, op))] += 1
        for order in a.get("market") or []:
            if order_is_valid(order):
                ops["M " + " ".join(map(str, order))] += 1
    payload = json.dumps(sorted(ops.items()), separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()[:16]


def plan_hashes(actions: list[dict], cuts=HASH_CUTS) -> dict[str, str]:
    return {f"h{t}": plan_signature(actions, t) for t in cuts}


def split_streams(actions: list[dict]) -> tuple[list[dict], list[dict]]:
    """(field-only, market-only) views of an action stream."""
    field = [{"farmer": a.get("farmer"), "hands": a.get("hands")} for a in actions]
    market = [{"market": a.get("market")} for a in actions]
    return field, market


def tile_summary(tiles) -> Counter:
    counts: Counter = Counter()
    for row in tiles:
        for tile in row:
            if tile is None:
                counts["empty"] += 1
            elif tile == "LOCKED":
                counts["locked"] += 1
            elif tile["kind"] == "PLANT":
                counts[f"plant_{tile['crop'].lower()}"] += 1
            elif tile["kind"] == "WEED":
                counts["weed"] += 1
            elif tile.get("animal"):
                counts[f"animal_{tile['animal'].lower()}"] += 1
            else:
                counts[f"{tile['kind'].lower()}_empty"] += 1
    return counts


def unit_ops(action: dict) -> list[list]:
    ops = [action.get("farmer") or ["PASS"]]
    ops += [h or ["PASS"] for h in (action.get("hands") or [])]
    return [op for op in ops if isinstance(op, list) and op]


def seat_trace(
    replay: dict, seat: int, turns_per_day: int, events: list[dict], money_check: dict
) -> dict:
    steps = replay["steps"]
    actions = actions_from_replay(replay, seat)
    field, market = split_streams(actions)
    days = (len(steps) + turns_per_day - 1) // turns_per_day

    money = [None] * days
    hands = [0] * days
    quadrants = [0] * days
    tiles_by_day = [None] * days
    shed_by_day = [None] * days
    weeds_seen = [0] * days
    prev_weeds = 0
    for t, step in enumerate(steps):
        day = t // turns_per_day
        farm = step[0]["observation"]["farms"][seat]
        if money[day] is None:
            money[day] = farm["money"]
        hands[day] = max(hands[day], farm.get("hires_today", 0), len(farm.get("hands", [])))
        quadrants[day] = max(quadrants[day], len(farm.get("unlocked_quadrants", [])))
        if t % turns_per_day == turns_per_day - 1 or t == len(steps) - 1:
            summary = tile_summary(farm["tiles"])
            tiles_by_day[day] = dict(summary)
            private = step[seat]["observation"].get("private") or {}
            shed_by_day[day] = dict(private.get("shed") or {})
        weeds_now = sum(
            1
            for row in farm["tiles"]
            for tile in row
            if isinstance(tile, dict) and tile.get("kind") == "WEED"
        )
        if weeds_now > prev_weeds:
            weeds_seen[day] += weeds_now - prev_weeds
        prev_weeds = weeds_now

    op_counts: Counter = Counter()
    plants_by_day = [Counter() for _ in range(days)]
    for i, action in enumerate(actions):
        day = i // turns_per_day
        for op in unit_ops(action):
            op_counts[op[0]] += 1
            if op[0] == "PLANT" and len(op) > 1 and op[1] in CROPS:
                plants_by_day[day][op[1]] += 1

    # Market orders as the engine executed them (research.market_replay): a SELL's units
    # are what the shed held after this turn's DROP/PLACE/PICKUP, and its revenue is the
    # sum of the per-unit prices quoted in the lockstep with the opponent. `price` is the
    # quote before the turn, kept for the narrators; `avg_price` is what was received.
    sells: list[dict] = []
    buys: list[dict] = []
    hires_ordered = [0] * days
    land_orders: list[int] = []
    for ev in events:
        kind = ev["type"]
        if kind == "HIRE":
            hires_ordered[ev["day"]] += 1
        elif kind == "BUY_LAND":
            land_orders.append(ev["day"])
        elif kind == "SELL" and ev["item"] in PRODUCTS:
            t = ev["day"] * turns_per_day + ev["hour"]
            quote = steps[t][0]["observation"]["market"]["prices"].get(ev["item"])
            n = int(ev["executed"])
            sells.append(
                {
                    "day": ev["day"],
                    "hour": ev["hour"],
                    "item": ev["item"],
                    "n": n,
                    "requested": int(ev["requested"]),
                    "price": quote,
                    "revenue": float(ev["revenue"]),
                    "avg_price": (float(ev["revenue"]) / n) if n else None,
                }
            )
        elif kind in ("BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT"):
            buys.append(
                {
                    "day": ev["day"],
                    "hour": ev["hour"],
                    "kind": kind,
                    "item": ev["item"],
                    "n": int(ev["executed"]),
                    "requested": int(ev["requested"]),
                    "spent": float(ev["spent"]),
                }
            )

    final_money = steps[-1][0]["observation"]["farms"][seat]["money"]
    land_days = [d for d in range(1, days) if quadrants[d] > quadrants[d - 1]]
    if quadrants[0] > 1:
        land_days = [0] * (quadrants[0] - 1) + land_days

    return {
        "seat": seat,
        "team": replay["info"]["TeamNames"][seat],
        "final_money": final_money,
        "reward": replay["rewards"][seat],
        "status": replay["statuses"][seat],
        "hashes": stream_hashes(actions),
        "field_hashes": stream_hashes(field),
        "market_hashes": stream_hashes(market),
        "money_by_day": money,
        "hands_by_day": hands,
        "hires_ordered_by_day": hires_ordered,
        "quadrants_by_day": quadrants,
        "land_days": land_days,
        "land_orders": land_orders,
        "tiles_by_day": tiles_by_day,
        "shed_by_day": shed_by_day,
        "weeds_spawned_by_day": weeds_seen,
        "plants_by_day": [dict(c) for c in plants_by_day],
        "op_counts": dict(op_counts),
        "sells": sells,
        "buys": buys,
        "money_check": money_check,
        "actions": actions,
    }


def shop_unlocks(replay: dict, turns_per_day: int) -> list[dict]:
    seen = 0
    out = []
    for t, step in enumerate(replay["steps"]):
        shops = step[0]["observation"]["town"]["unlocked_shops"]
        while seen < len(shops):
            out.append({"day": t // turns_per_day, "shop": shops[seen]})
            seen += 1
    return out


def market_series(replay: dict, turns_per_day: int) -> dict:
    """Per-day closing price and inventory for every product (shared between seats)."""
    steps = replay["steps"]
    days = (len(steps) + turns_per_day - 1) // turns_per_day
    prices = {p: [None] * days for p in PRODUCTS}
    inventory = {p: [None] * days for p in PRODUCTS}
    for t, step in enumerate(steps):
        day = t // turns_per_day
        m = step[0]["observation"]["market"]
        for p in PRODUCTS:
            prices[p][day] = m["prices"].get(p)
            inventory[p][day] = m["inventory"].get(p)
    return {"prices": prices, "inventory": inventory}


def build_trace(replay: dict) -> dict:
    cfg = replay["configuration"]
    tpd = int(cfg.get("turnsPerDay", 24))
    actions = [actions_from_replay(replay, 0), actions_from_replay(replay, 1)]
    events, checks = market_events(replay, actions)
    return {
        "trace_version": TRACE_VERSION,
        "episode_id": replay["info"]["EpisodeId"],
        "seed": replay["info"].get("seed"),
        "engine": replay.get("module_version"),
        "teams": list(replay["info"]["TeamNames"]),
        "rewards": list(replay["rewards"]),
        "statuses": list(replay["statuses"]),
        "steps": len(replay["steps"]),
        "turns_per_day": tpd,
        "config": {
            k: cfg.get(k)
            for k in (
                "townCenterSellInterval",
                "townShopSellInterval",
                "townShopUnlockInterval",
                "weedSpawnChance",
                "startingMoney",
                "shedCapacity",
            )
        },
        "shops": shop_unlocks(replay, tpd),
        "market": market_series(replay, tpd),
        "seats": [
            seat_trace(replay, 0, tpd, events[0], checks[0]),
            seat_trace(replay, 1, tpd, events[1], checks[1]),
        ],
    }


def pass_only(actions: list[dict]) -> bool:
    return all(canon(a) == canon(PASS) for a in actions)
