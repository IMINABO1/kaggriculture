"""Day-by-day timeline of one seat in one game, built from its trace."""

from __future__ import annotations

from collections import Counter

import pandas as pd

from research.trace import ANIMALS, CROPS, PRODUCTS, unit_ops

SHORT = {
    "WHEAT": "W",
    "CARROT": "C",
    "TOMATO": "T",
    "STRAWBERRY": "S",
    "MELON": "M",
    "EGG": "E",
    "MILK": "Mk",
    "WOOL": "Wl",
    "FERTILIZER": "F",
    "GOOSE": "goose",
    "COW": "cow",
    "SHEEP": "sheep",
}


def compact(counter: Counter, keys) -> str:
    return " ".join(f"{SHORT.get(k, k)}{int(counter[k])}" for k in keys if counter.get(k))


def farm_state(tiles: dict | None) -> str:
    if not tiles:
        return ""
    animals = " ".join(
        f"{SHORT[a]}{tiles[f'animal_{a.lower()}']}"
        for a in ANIMALS
        if tiles.get(f"animal_{a.lower()}")
    )
    plants = " ".join(
        f"{SHORT[c]}{tiles[f'plant_{c.lower()}']}" for c in CROPS if tiles.get(f"plant_{c.lower()}")
    )
    extras = []
    if tiles.get("weed"):
        extras.append(f"weeds {tiles['weed']}")
    if tiles.get("pasture_empty") or tiles.get("coop_empty"):
        extras.append(f"empty pens {tiles.get('pasture_empty', 0) + tiles.get('coop_empty', 0)}")
    return "; ".join(x for x in (animals, plants, " ".join(extras)) if x)


def day_table(trace: dict, seat: int) -> pd.DataFrame:
    s = trace["seats"][seat]
    tpd = trace["turns_per_day"]
    days = len(s["money_by_day"])
    per_day_ops = [Counter() for _ in range(days)]
    for i, action in enumerate(s["actions"]):
        for op in unit_ops(action):
            per_day_ops[i // tpd][op[0]] += 1
    buys = [Counter() for _ in range(days)]
    seeds = [Counter() for _ in range(days)]
    for b in s["buys"]:
        if b["kind"] == "BUY_ANIMAL":
            buys[b["day"]][b["item"]] += b["n"]
        elif b["kind"] == "BUY_SEED":
            seeds[b["day"]][b["item"]] += b["n"]
    sells = [Counter() for _ in range(days)]
    revenue = [0.0] * days
    for x in s["sells"]:
        sells[x["day"]][x["item"]] += x["n"]
        revenue[x["day"]] += x["n"] * (x["price"] or 0)
    shops = {}
    for sh in trace["shops"]:
        shops.setdefault(sh["day"], []).append(
            sh["shop"].replace("_SHOP", "").replace("_", " ").title()
        )
    rows = []
    for d in range(days):
        ops = per_day_ops[d]
        rows.append(
            {
                "day": d,
                "money": round(s["money_by_day"][d]),
                "hands": s["hands_by_day"][d],
                "quads": s["quadrants_by_day"][d],
                "bought": compact(buys[d], ANIMALS)
                + (" | " if buys[d] and seeds[d] else "")
                + compact(seeds[d], CROPS),
                "built": (f"pasture {ops['BUILD_PASTURE']} " if ops["BUILD_PASTURE"] else "")
                + (f"coop {ops['BUILD_COOP']}" if ops["BUILD_COOP"] else ""),
                "planted": compact(Counter(s["plants_by_day"][d]), CROPS),
                "care/fert": f"{ops['CARE']}/{ops['FERTILIZE']}",
                "harvest": ops["HARVEST"],
                "sold": compact(sells[d], PRODUCTS),
                "revenue": round(revenue[d]),
                "farm at day end": farm_state(s["tiles_by_day"][d]),
                "new weeds": s["weeds_spawned_by_day"][d] or "",
                "shop unlock": ", ".join(shops.get(d, [])),
            }
        )
    return pd.DataFrame(rows)
