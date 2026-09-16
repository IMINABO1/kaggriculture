"""Per-(game, seat) market and labour facts that the feature table does not carry.

    uv run python scripts/top10/market_extract.py

Reads every trace in the sample and writes data/top10/market.parquet with, per seat: revenue
and executed units per product (as the engine executed them, trace version 2), the average
price received, units sold below half the base price, units and revenue by day, the day-end
weed and empty-tile series, animal-days and crop tile-days, hire spend, and the market's per-day
prices (shared by both seats). Everything comes from the traces; no replay is opened.
"""

from __future__ import annotations

import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import research  # noqa: F401  (UTF-8 streams)
from research.paths import TOP10
from research.store import load_trace, trace_path
from research.trace import ANIMALS, CROPS, PRODUCTS

BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}
FIB = [1, 1]
while len(FIB) < 40:
    FIB.append(FIB[-1] + FIB[-2])


def hire_cost(n: int) -> int:
    return sum(FIB[:n])


def seat_row(trace: dict, seat: int) -> dict:
    s = trace["seats"][seat]
    days = len(s["money_by_day"])
    row = {"episode_id": int(trace["episode_id"]), "seat": seat, "team": s["team"]}
    units = {p: np.zeros(days) for p in PRODUCTS}
    revenue = {p: np.zeros(days) for p in PRODUCTS}
    cheap = {p: 0 for p in PRODUCTS}
    for sale in s["sells"]:
        if sale["n"] <= 0:
            continue
        rev = sale.get("revenue", sale["n"] * (sale["price"] or 0))
        units[sale["item"]][sale["day"]] += sale["n"]
        revenue[sale["item"]][sale["day"]] += rev
        if rev / sale["n"] < 0.5 * BASE[sale["item"]]:
            cheap[sale["item"]] += sale["n"]
    for p in PRODUCTS:
        u, r = units[p].sum(), revenue[p].sum()
        row[f"units_{p.lower()}"] = int(u)
        row[f"revenue_{p.lower()}"] = float(r)
        row[f"price_{p.lower()}"] = float(r / u) if u else np.nan
        row[f"units_by_day_{p.lower()}"] = units[p].astype(int).tolist()
        row[f"revenue_by_day_{p.lower()}"] = revenue[p].tolist()
        row[f"units_cheap_{p.lower()}"] = int(cheap[p])
    total_rev = sum(revenue[p] for p in PRODUCTS)
    row["revenue_total"] = float(total_rev.sum())
    row["revenue_by_day"] = total_rev.tolist()
    row["revenue_last3"] = float(total_rev[-3:].sum())
    row["revenue_premium"] = float(sum(revenue[p].sum() for p in ("STRAWBERRY", "MELON", "MILK", "WOOL")))
    row["revenue_staple"] = float(sum(revenue[p].sum() for p in ("WHEAT", "CARROT", "TOMATO", "EGG", "FERTILIZER")))

    weeds = []
    empty = []
    animal_days = {a: 0 for a in ANIMALS}
    crop_days = {c: 0 for c in CROPS}
    for tiles in s["tiles_by_day"]:
        tiles = tiles or {}
        weeds.append(int(tiles.get("weed", 0)))
        empty.append(int(tiles.get("empty", 0)))
        for a in ANIMALS:
            animal_days[a] += int(tiles.get(f"animal_{a.lower()}", 0))
        for c in CROPS:
            crop_days[c] += int(tiles.get(f"plant_{c.lower()}", 0))
    row["weeds_by_dayend"] = weeds
    row["empty_by_dayend"] = empty
    row["weed_tile_days"] = int(sum(weeds))
    row["empty_tile_days"] = int(sum(empty))
    for a in ANIMALS:
        row[f"days_{a.lower()}"] = animal_days[a]
    for c in CROPS:
        row[f"tile_days_{c.lower()}"] = crop_days[c]

    hires = s["hires_ordered_by_day"]
    row["hire_spend"] = int(sum(hire_cost(n) for n in hires))
    row["hires_total"] = int(sum(hires))
    row["hands_by_day"] = list(s["hands_by_day"])

    bought = {}
    for b in s["buys"]:
        key = f"bought_{b['kind'].lower()}_{b['item'].lower()}"
        bought[key] = bought.get(key, 0) + int(b["n"])
    row.update(bought)
    row["money_by_day"] = list(s["money_by_day"])
    return row


def market_row(trace: dict) -> dict:
    row = {"episode_id": int(trace["episode_id"])}
    for p in PRODUCTS:
        row[f"price_by_day_{p.lower()}"] = trace["market"]["prices"][p]
        row[f"inventory_by_day_{p.lower()}"] = trace["market"]["inventory"][p]
    row["shops"] = "|".join(f"{d['day']}:{d['shop']}" for d in trace["shops"])
    return row


def one(episode_id: int) -> tuple[list[dict], dict] | None:
    if not trace_path(episode_id).exists():
        return None
    trace = load_trace(episode_id)
    return [seat_row(trace, 0), seat_row(trace, 1)], market_row(trace)


def main() -> None:
    sample = pd.read_csv(TOP10 / "sample.csv")
    ids = sorted(set(int(e) for e in sample.episode_id))
    jobs = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    seat_rows, market_rows = [], []
    with ProcessPoolExecutor(jobs) as pool:
        for i, out in enumerate(pool.map(one, ids, chunksize=50)):
            if out is None:
                continue
            seat_rows.extend(out[0])
            market_rows.append(out[1])
            if i % 500 == 0:
                print(f"{i}/{len(ids)}", flush=True)
    pd.DataFrame(seat_rows).to_parquet(TOP10 / "market.parquet", index=False)
    pd.DataFrame(market_rows).to_parquet(TOP10 / "market_prices.parquet", index=False)
    print(f"wrote {len(seat_rows)} seat rows, {len(market_rows)} market rows")


if __name__ == "__main__":
    main()
