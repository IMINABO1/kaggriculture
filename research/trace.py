"""Reduce a 30 MB replay to the facts the study needs.

A trace keeps both seats' full action streams (so the game can be replayed or used as an
opponent), per-day state series, per-event lists, and the stream hashes the community uses
to identify a line of play. Sell units are the executed amount, capped by what the shed held
before the turn's orders, because some agents request thousands of units every turn. Hashing follows destbreso's normalisation byte for byte (canonical
JSON per action, NUL between turns, first 16 hex chars, steps[0] skipped) so values are
comparable with `stream_hashes.csv` from georgymamarin/kaggriculture-episodes.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter

from agent.tape import PASS, actions_from_replay

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


def seat_trace(replay: dict, seat: int, turns_per_day: int) -> dict:
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
    sells: list[dict] = []
    buys: list[dict] = []
    hires_ordered = [0] * days
    land_orders: list[int] = []
    for i, action in enumerate(actions):
        t = i + 1
        day = i // turns_per_day
        hour = i % turns_per_day
        for op in unit_ops(action):
            op_counts[op[0]] += 1
            if op[0] == "PLANT" and len(op) > 1 and op[1] in CROPS:
                plants_by_day[day][op[1]] += 1
        before = steps[t - 1]
        prices = before[0]["observation"]["market"]["prices"]
        shed = dict((before[seat]["observation"].get("private") or {}).get("shed") or {})
        for order in action.get("market") or []:
            if not isinstance(order, list) or not order:
                continue
            kind = order[0]
            if kind == "SELL" and len(order) >= 3 and order[1] in PRODUCTS:
                requested = max(int(order[2]), 0)
                executed = min(requested, int(shed.get(order[1], 0)))
                shed[order[1]] = shed.get(order[1], 0) - executed
                sells.append(
                    {
                        "day": day,
                        "hour": hour,
                        "item": order[1],
                        "n": executed,
                        "requested": requested,
                        "price": prices.get(order[1]),
                    }
                )
            elif kind in ("BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT") and len(order) >= 3:
                buys.append(
                    {"day": day, "hour": hour, "kind": kind, "item": order[1], "n": int(order[2])}
                )
            elif kind == "HIRE":
                hires_ordered[day] += 1
            elif kind == "BUY_LAND":
                land_orders.append(day)

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
    return {
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
        "seats": [seat_trace(replay, 0, tpd), seat_trace(replay, 1, tpd)],
    }


def pass_only(actions: list[dict]) -> bool:
    return all(canon(a) == canon(PASS) for a in actions)
