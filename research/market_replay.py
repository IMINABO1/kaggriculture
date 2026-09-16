"""Replay one turn's market the way the engine runs it, from the recorded observations.

The engine applies every unit action (DROP, PLACE and PICKUP change the shed) before it
processes the market queues, and it processes both players' queues in a per-unit lockstep
against one shared inventory. A sale's executed units and the price of each unit therefore
depend on what was dropped into the shed the same turn and on what the opponent sells at the
same moment. This module rebuilds that turn from the observation before it and both players'
actions, and checks itself against the money the observation after it records.

The price function and the market parameters mirror `kaggriculture.py`; `tests/test_research.py`
checks them against the engine.
"""

from __future__ import annotations

import math
from copy import deepcopy

MARKET_I0 = 10000
PRICE_FLOOR = 1
HINGE_GAIN = 8.0
LAND_PRICES = [1000, 2000, 4000]
SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]
ORDER_KEYS = ("type", "item", "requested", "executed", "revenue", "spent")

MARKET_PARAMS = {
    "WHEAT": {"base": 25, "I0": MARKET_I0, "T": 400, "below_func": "sqrt", "below_target": 0.80, "above_func": "log", "above_target": 0.20},
    "CARROT": {"base": 35, "I0": MARKET_I0, "T": 450, "below_func": "hinge", "below_target": 1.00, "above_func": "sqrt", "above_target": 0.70},
    "TOMATO": {"base": 60, "I0": MARKET_I0, "T": 200, "below_func": "hinge", "below_target": 0.40, "above_func": "sqrt", "above_target": 0.60},
    "STRAWBERRY": {"base": 120, "I0": MARKET_I0, "T": 100, "below_func": "sqrt", "below_target": 0.70, "above_func": "linear", "above_target": 1.60},
    "MELON": {"base": 250, "I0": MARKET_I0, "T": 300, "below_func": "log", "below_target": 0.20, "above_func": "sq", "above_target": 3.60},
    "EGG": {"base": 50, "I0": MARKET_I0, "T": 332, "below_func": "hinge", "below_target": 0.40, "above_func": "log", "above_target": 0.20},
    "MILK": {"base": 160, "I0": MARKET_I0, "T": 122, "below_func": "sqrt", "below_target": 0.60, "above_func": "linear", "above_target": 1.60},
    "WOOL": {"base": 200, "I0": MARKET_I0, "T": 105, "below_func": "log", "below_target": 0.20, "above_func": "sq", "above_target": 3.20},
    "FERTILIZER": {"base": 100, "I0": MARKET_I0, "T": 200, "below_func": "linear", "below_target": 0.40, "above_func": "linear", "above_target": 0.40},
}


def _shape(func: str, x: float, T=None) -> float:
    x = max(0.0, x)
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return math.sqrt(x)
    if func == "log":
        return math.log(1.0 + x)
    if func == "log10":
        return math.log10(1.0 + x)
    if func == "hinge":
        if not T or T <= 0:
            return x
        u = x / T
        return u + HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x


def resolve_params(overrides) -> dict:
    resolved = {item: dict(p) for item, p in MARKET_PARAMS.items()}
    for item, patch in (overrides or {}).items():
        if item in resolved and isinstance(patch, dict):
            resolved[item].update(patch)
    return resolved


def market_price(item: str, inventory: float, params: dict | None = None) -> int:
    p = (params or MARKET_PARAMS)[item]
    base, I0, T = p["base"], p["I0"], p["T"]
    if inventory < I0:
        f = p["below_func"]
        amp = p["below_target"] * base / _shape(f, T, T)
        price = base + amp * _shape(f, I0 - inventory, T)
    else:
        f = p["above_func"]
        amp = p["above_target"] * base / _shape(f, T, T)
        price = base - amp * _shape(f, inventory - I0, T)
    return max(PRICE_FLOOR, int(round(price)))


def _fib(n: int) -> int:
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _shed_adjacent(pos, board: int) -> bool:
    half = board // 2
    return tuple(pos) in {(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)}


def _count(op, default: int = 1) -> int | None:
    try:
        return int(op[2]) if len(op) >= 3 else default
    except (TypeError, ValueError):
        return None


def _apply_shed_ops(farm: dict, shed: dict, inventories: list[dict], ops: list, board: int, cap: int) -> None:
    """Mirror the engine's DROP, PICKUP and PLACE for one seat on working copies."""
    positions = [farm["farmer"]] + list(farm.get("hands") or [])
    for idx, op in enumerate(ops):
        if not isinstance(op, list) or not op or idx >= len(positions) or idx >= len(inventories):
            continue
        pos = positions[idx]
        inv = inventories[idx]
        kind = op[0]
        if kind == "DROP":
            if not _shed_adjacent(pos, board):
                continue
            for item, n in list(inv.items()):
                if n <= 0:
                    del inv[item]
                    continue
                room = max(0, cap - sum(shed.values()))
                take = min(n, room)
                if take > 0:
                    shed[item] = shed.get(item, 0) + take
                del inv[item]
        elif kind == "PICKUP":
            if not _shed_adjacent(pos, board) or len(op) < 2:
                continue
            item = op[1]
            n = _count(op)
            if n is None:
                continue
            n = min(n, shed.get(item, 0))
            if n <= 0:
                continue
            shed[item] -= n
            inv[item] = inv.get(item, 0) + n
        elif kind == "PLACE":
            if len(op) < 2:
                continue
            item = op[1]
            x, y = pos
            tile = farm["tiles"][y][x] if 0 <= y < board and 0 <= x < board else None
            if (
                item in ANIMAL_STRUCTURE
                and isinstance(tile, dict)
                and tile.get("kind") == ANIMAL_STRUCTURE[item]
                and "animal" not in tile
            ):
                if inv.get(item, 0) > 0:
                    inv[item] -= 1
                continue
            if not _shed_adjacent(pos, board):
                continue
            n = _count(op)
            if n is None:
                continue
            n = min(n, inv.get(item, 0), max(0, cap - sum(shed.values())))
            if n <= 0:
                continue
            inv[item] -= n
            shed[item] = shed.get(item, 0) + n


def _parse_order(order):
    if not isinstance(order, list) or not order:
        return None
    op = order[0]
    if op in ("HIRE", "BUY_LAND"):
        return {"type": op}
    if op in ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL") and len(order) >= 3:
        n = _count(order)
        if n is None or n <= 0:
            return None
        return {
            "type": op,
            "item": order[1],
            "remaining": n,
            "requested": n,
            "executed": 0,
            "revenue": 0.0,
            "spent": 0.0,
        }
    return None


def turn_market(replay: dict, actions: list[list[dict]], t: int) -> tuple[list[list[dict]], list[float]]:
    """Both seats' executed orders for action index t, and each seat's simulated end-of-turn money.

    `actions[seat][t]` is the action seat submitted for the observation `replay['steps'][t]`.
    """
    cfg = replay["configuration"]
    board = int(cfg.get("boardSize", 10))
    cap = int(cfg.get("shedCapacity", 100))
    max_orders = max(1, int(cfg.get("maxMarketOrdersPerTurn", 10)))
    hire_mult = int(cfg.get("farmHandCostMult", 1))
    params = resolve_params(cfg.get("marketParams"))
    step = replay["steps"][t]
    obs0 = step[0]["observation"]
    market_inv = dict(obs0["market"]["inventory"])
    farms = [deepcopy(obs0["farms"][s]) for s in (0, 1)]
    sheds, invs, queues = [], [], []
    for s in (0, 1):
        private = step[s]["observation"].get("private") or {}
        sheds.append(dict(private.get("shed") or {}))
        invs.append([dict(i) for i in (private.get("inventories") or [{}])])
        a = actions[s][t] if t < len(actions[s]) else {}
        ops = [a.get("farmer") or ["PASS"]] + list(a.get("hands") or [])
        _apply_shed_ops(farms[s], sheds[s], invs[s], ops, board, cap)
        m = a.get("market") or []
        queues.append([_parse_order(o) for o in (m if isinstance(m, list) else [])][:max_orders])
    money = [float(f["money"]) for f in farms]
    hires_today = [int(f.get("hires_today", 0)) for f in farms]
    quadrants = [len(f.get("unlocked_quadrants") or []) for f in farms]
    results: list[list[dict]] = [[], []]

    max_len = max((len(q) for q in queues), default=0)
    for i in range(max_len):
        states = [q[i] if i < len(q) else None for q in queues]
        unit_orders = [st for st in states if st is not None and "item" in st]
        for s, st in enumerate(states):
            if st is None:
                continue
            if st["type"] == "HIRE":
                cost = hire_mult * _fib(hires_today[s])
                if money[s] >= cost:
                    money[s] -= cost
                    hires_today[s] += 1
                    results[s].append({"type": "HIRE", "spent": float(cost)})
                states[s] = None
            elif st["type"] == "BUY_LAND":
                extra = quadrants[s] - 1
                if extra < len(LAND_PRICES) and money[s] >= LAND_PRICES[extra]:
                    money[s] -= LAND_PRICES[extra]
                    quadrants[s] += 1
                    results[s].append({"type": "BUY_LAND", "spent": float(LAND_PRICES[extra])})
                states[s] = None
        guard = 0
        while True:
            guard += 1
            if guard >= 100_000:
                break
            quoted = [None, None]
            for s, st in enumerate(states):
                if st is None or st["remaining"] <= 0:
                    continue
                op, item = st["type"], st["item"]
                if op == "SELL" and item in PRODUCTS:
                    quoted[s] = (op, item, market_price(item, market_inv[item], params), st)
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    quoted[s] = (op, item, market_price(item, market_inv[item] - 1, params), st)
                elif op == "BUY_SEED" and item in SEED_COST:
                    quoted[s] = (op, item, SEED_COST[item], st)
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    quoted[s] = (op, item, ANIMAL_COST[item], st)
                else:
                    states[s] = None
            if all(q is None for q in quoted):
                break
            committed = False
            for s, q in enumerate(quoted):
                if q is None:
                    continue
                op, item, price, st = q
                ok = False
                if op == "SELL":
                    if sheds[s].get(item, 0) > 0:
                        sheds[s][item] -= 1
                        money[s] += price
                        if price > 1:
                            market_inv[item] += 1
                        st["revenue"] += price
                        ok = True
                elif op == "BUY_PRODUCT":
                    if money[s] >= price and sum(sheds[s].values()) < cap:
                        money[s] -= price
                        sheds[s][item] = sheds[s].get(item, 0) + 1
                        market_inv[item] -= 1
                        st["spent"] += price
                        ok = True
                elif op == "BUY_SEED":
                    if money[s] >= price:
                        money[s] -= price
                        st["spent"] += price
                        ok = True
                elif op == "BUY_ANIMAL":
                    if money[s] >= price and sum(sheds[s].values()) < cap:
                        money[s] -= price
                        sheds[s][item] = sheds[s].get(item, 0) + 1
                        st["spent"] += price
                        ok = True
                if ok:
                    st["remaining"] -= 1
                    st["executed"] += 1
                    committed = True
                else:
                    states[s] = None
            if not committed:
                break
        for s in (0, 1):
            st = queues[s][i] if i < len(queues[s]) else None
            if st is not None and "item" in st:
                results[s].append({k: st[k] for k in ORDER_KEYS})
    return results, money


def market_events(replay: dict, actions: list[list[dict]]) -> tuple[list[list[dict]], list[dict]]:
    """Every order of both seats with what it executed, plus a money reconciliation per seat."""
    tpd = int(replay["configuration"].get("turnsPerDay", 24))
    steps = replay["steps"]
    events: list[list[dict]] = [[], []]
    checks = [{"turns_mismatched": 0, "abs_error": 0.0, "max_error": 0.0} for _ in (0, 1)]
    for t in range(len(actions[0])):
        results, money = turn_market(replay, actions, t)
        for s in (0, 1):
            for r in results[s]:
                r["day"], r["hour"] = t // tpd, t % tpd
                events[s].append(r)
            if t + 1 < len(steps):
                recorded = float(steps[t + 1][0]["observation"]["farms"][s]["money"])
                err = abs(recorded - money[s])
                if err > 0.5:
                    checks[s]["turns_mismatched"] += 1
                    checks[s]["abs_error"] += err
                    checks[s]["max_error"] = max(checks[s]["max_error"], err)
    return events, checks
