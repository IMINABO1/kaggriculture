"""Turn stored replays into traces and one flat feature table.

    uv run python scripts/top10/extract.py --jobs 4

For every sampled episode with a replay on disk: write data/traces/<id>.json.zst (skipped if
present), then rebuild data/top10/features.parquet with one row per (episode, seat), joined to
history.parquet so each top-10 seat carries its submission, ratings, and window labels.
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor

import pandas as pd

from research.kaggle_api import load_replay, replay_path
from research.paths import TOP10
from research.store import load_trace, save_trace, trace_path
from research.trace import ANIMALS, CROPS, PRODUCTS, build_trace


def make_trace(episode_id: int) -> tuple[int, str | None]:
    if trace_path(episode_id).exists():
        return episode_id, None
    try:
        save_trace(build_trace(load_replay(episode_id)))
        return episode_id, None
    except Exception as exc:  # noqa: BLE001 - one bad replay must not stop the batch
        return episode_id, repr(exc)


def seat_features(trace: dict, seat: int) -> dict:
    s = trace["seats"][seat]
    days = len(s["money_by_day"])
    final_tiles = s["tiles_by_day"][-1] or {}
    sells = (
        pd.DataFrame(s["sells"])
        if s["sells"]
        else pd.DataFrame(columns=["day", "hour", "item", "n", "price"])
    )
    buys = (
        pd.DataFrame(s["buys"])
        if s["buys"]
        else pd.DataFrame(columns=["day", "hour", "kind", "item", "n"])
    )
    plants_total = {c: sum(d.get(c, 0) for d in s["plants_by_day"]) for c in CROPS}
    animals_bought = buys[buys.kind == "BUY_ANIMAL"] if len(buys) else buys
    row = {
        "episode_id": trace["episode_id"],
        "seat": seat,
        "team": s["team"],
        "engine": trace["engine"],
        "seed": trace["seed"],
        "final_money": s["final_money"],
        "opp_final_money": trace["seats"][1 - seat]["final_money"],
        "won": s["final_money"] > trace["seats"][1 - seat]["final_money"],
        "status": s["status"],
        "days": days,
        "town_center_interval": trace["config"].get("townCenterSellInterval"),
        "shops": "|".join(x["shop"] for x in trace["shops"]),
        "n_shops": len(trace["shops"]),
        "peak_hands": max(s["hands_by_day"]),
        "hands_by_day": s["hands_by_day"],
        "money_by_day": s["money_by_day"],
        "quadrants_final": s["quadrants_by_day"][-1],
        "land_days": s["land_days"],
        "land_day_1": s["land_days"][0] if len(s["land_days"]) > 0 else None,
        "land_day_2": s["land_days"][1] if len(s["land_days"]) > 1 else None,
        "land_day_3": s["land_days"][2] if len(s["land_days"]) > 2 else None,
        "weeds_spawned": sum(s["weeds_spawned_by_day"]),
        "weeds_by_day": s["weeds_spawned_by_day"],
        "shed_peak": max((sum(d.values()) for d in s["shed_by_day"] if d), default=0),
    }
    for c in CROPS:
        row[f"plants_{c.lower()}"] = plants_total[c]
    for a in ANIMALS:
        n = int(animals_bought[animals_bought.item == a].n.sum()) if len(animals_bought) else 0
        first = int(animals_bought[animals_bought.item == a].day.min()) if n else None
        row[f"bought_{a.lower()}"] = n
        row[f"first_{a.lower()}_day"] = first
        row[f"final_{a.lower()}"] = final_tiles.get(f"animal_{a.lower()}", 0)
    for op in (
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
        "DROP",
        "PASS",
    ):
        row[f"op_{op.lower()}"] = s["op_counts"].get(op, 0)
    for p in PRODUCTS:
        sp = sells[sells.item == p] if len(sells) else sells
        row[f"sold_{p.lower()}"] = int(sp.n.sum()) if len(sp) else 0
        row[f"sell_first_day_{p.lower()}"] = int(sp.day.min()) if len(sp) else None
        row[f"sell_last_day_{p.lower()}"] = int(sp.day.max()) if len(sp) else None
    row["sold_units_total"] = int(sells.n.sum()) if len(sells) else 0
    row["sells_last_3_days"] = int(sells[sells.day >= days - 3].n.sum()) if len(sells) else 0
    row["final_tiles"] = json.dumps(final_tiles, sort_keys=True)
    for name, cut in (
        ("h24", 24),
        ("h48", 48),
        ("h100", 100),
        ("h136", 136),
        ("h200", 200),
        ("h300", 300),
        ("h400", 400),
        ("h719", 719),
    ):
        row[f"full_{name}"] = s["hashes"].get(name)
        row[f"field_{name}"] = s["field_hashes"].get(name)
        row[f"market_{name}"] = s["market_hashes"].get(name)
    return row


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--all", action="store_true", help="every replay on disk, not just sample.csv")
    ap.add_argument("--traces-only", action="store_true", help="skip the feature table")
    args = ap.parse_args()

    if args.all:
        episodes = sorted(
            int(p.name.split(".")[0]) for p in replay_path(0).parent.glob("*.json.zst")
        )
        sample = pd.DataFrame({"episode_id": episodes, "window": "ALL"})
    else:
        sample = pd.read_csv(TOP10 / "sample.csv")
        episodes = sorted({int(e) for e in sample.episode_id if replay_path(int(e)).exists()})
    todo = [e for e in episodes if not trace_path(e).exists()]
    print(f"{len(episodes)} replays on disk, {len(todo)} traces to build")
    failures = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for i, (episode_id, err) in enumerate(pool.map(make_trace, todo, chunksize=4), start=1):
            if err:
                failures.append((episode_id, err))
                print(f"FAILED {episode_id}: {err[:160]}", flush=True)
            if i % 50 == 0 or i == len(todo):
                print(f"traces {i}/{len(todo)}", flush=True)
    if args.traces_only:
        print(f"{len(failures)} trace failures")
        return

    rows = []
    for episode_id in episodes:
        if not trace_path(episode_id).exists():
            continue
        trace = load_trace(episode_id)
        for seat in (0, 1):
            rows.append(seat_features(trace, seat))
    feats = pd.DataFrame(rows)

    hist = pd.read_parquet(TOP10 / "history.parquet")[
        [
            "episode_id",
            "seat",
            "team_id",
            "team_name",
            "sub",
            "is_current_sub",
            "create_time",
            "rating_before",
            "rating_after",
            "opp_sub",
            "opp_team_id",
            "opp_rating_before",
            "result",
        ]
    ]
    feats = feats.merge(hist, on=["episode_id", "seat"], how="left")
    feats["is_top10_seat"] = feats.team_id.notna()
    labels = (
        sample.groupby("episode_id")
        .window.apply(lambda w: "|".join(sorted(set(w))))
        .rename("windows")
        .reset_index()
    )
    feats = feats.merge(labels, on="episode_id", how="left")
    feats.to_parquet(TOP10 / "features.parquet", index=False)
    print(
        f"features.parquet: {len(feats)} seat rows from {feats.episode_id.nunique()} episodes; "
        f"{int(feats.is_top10_seat.sum())} top-10 seats; {len(failures)} trace failures"
    )


if __name__ == "__main__":
    main()
