"""Level-k analysis of one team's current submission: who it plays (K1), how it earns against
them (K2), and what beats it (K3), from the encoded arrays and the market replica.

    uv run python scripts/top10/klevel.py --team "THIRD FARM CLUB" --jobs 3

Writes data/top10/klevel_<slug>.parquet (one row per game) and prints the tables the
report quotes: opponent classes, revenue by product for the team and its opponents, sale
hours by product, the shop-draw conditionals, and the loss table.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from research.encode import ANIMALS, CROPS, FEATURES, PRODUCTS, SHOPS, load_encoded  # noqa: E402
from research.paths import DATA  # noqa: E402

PREMIUM = ("STRAWBERRY", "MILK", "WOOL", "EGG", "MELON")
HOUR_BUCKETS = ((0, 1), (2, 11), (12, 19), (20, 23))
SHOP_GROUPS = {
    "yarn": ("YARN_STORE",),
    "milk": ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP"),
    "egg": ("BAKERY", "BRUNCH_SPOT"),
    "carrot": ("PET_CAFE", "FARMERS_MARKET"),
}
TOP10 = ("Majkel1337", "DSM", "SpaTaro", "Sida Zuo", "Unknown Mother-Goose", "ymg_aq", "Excluding",
         "Arda Ceylan", "Orbital Terraformer", "THIRD FARM CLUB")


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def field_hash(z: dict, seat: int, upto: int) -> str:
    return hashlib.md5(z["op"][seat][:upto].tobytes() + z["op_arg"][seat][:upto].tobytes()).hexdigest()[:10]


def line_hashes() -> dict[str, str]:
    """The public builds' own field lines through turn 136, from one local game each."""
    from kenv import import_ke

    ke = import_ke()
    from research.encode import encode_replay

    out = {}
    for name, path in (("v41", ROOT / "agent/line_v41.py"), ("v7", ROOT / "agent/line_v7.py")):
        env = ke.make("kaggriculture", configuration={"episodeSteps": 720, "seed": 1}, debug=False)
        env.run([str(path), "pass"])
        z = encode_replay(env.toJSON())
        out[name] = field_hash(z, 0, 136)
    return out


def one_game(task: dict) -> dict:
    from agent.tape import actions_from_replay
    from research.kaggle_api import load_replay
    from research.market_replay import market_events

    ep, seat = task["episode_id"], task["seat"]
    z = load_encoded(ep)
    opp = 1 - seat
    row = {"episode_id": ep, "seat": seat, "bank": float(z["money"][seat, -1]), "opp_bank": float(z["money"][opp, -1])}
    row["opp_h136"] = field_hash(z, opp, 136)
    row["own_h136"] = field_hash(z, seat, 136)
    shops = [SHOPS[s - 1] for s in z["shops"][300] if s > 0][:3]
    row["shops3"] = " ".join(shops)
    for g, names in SHOP_GROUPS.items():
        row[f"shop_{g}"] = int(any(s in names for s in shops))
    # crop plantings, animals at day 15, hands per day
    for s_name, s in (("own", seat), ("opp", opp)):
        op, arg = z["op"][s], z["op_arg"][s]
        plants = Counter()
        for crop_id in range(1, 6):
            plants[CROPS[crop_id - 1]] = int(((op == 6) & (arg == crop_id)).sum())
        for c in CROPS:
            row[f"{s_name}_plant_{c.lower()}"] = plants[c]
        tiles15 = z["tiles"][s, 360]
        for a_id, a in zip(range(6, 9), ANIMALS):
            row[f"{s_name}_{a.lower()}_d15"] = int(((tiles15[:, :, 0] == 5) & (tiles15[:, :, 1] == a_id)).sum())
        hands = [int(z["n_units"][s, d * 24 + 2]) - 1 for d in range(30)]
        row[f"{s_name}_hands_mean"] = float(np.mean(hands))
        row[f"{s_name}_hands_json"] = json.dumps(hands)
        for d in (10, 16, 24):
            t = z["tiles"][s, d * 24]
            kinds = t[:, :, 0]
            row[f"{s_name}_census_d{d}"] = json.dumps({
                "empty": int((kinds == 0).sum()), "weed": int((kinds == 2).sum()),
                **{c.lower(): int(((kinds == 3) & (t[:, :, 1] == i + 1)).sum()) for i, c in enumerate(CROPS)},
                "animals": int((kinds == 5).sum())})
        fert_ops = int((op == 9).sum())
        row[f"{s_name}_fertilize_ops"] = fert_ops
        row[f"{s_name}_weeds_max"] = int(max((z["tiles"][s, d * 24, :, :, 0] == 2).sum() for d in range(30)))
    # market replica: executed revenue by product, by day and by hour bucket
    replay = load_replay(ep)
    events, checks = market_events(replay, [actions_from_replay(replay, 0), actions_from_replay(replay, 1)])
    row["money_check_own"] = int(checks[seat].get("turns_mismatched", 0)) if isinstance(checks[seat], dict) else -1
    for s_name, s in (("own", seat), ("opp", opp)):
        rev = defaultdict(float)
        units = defaultdict(int)
        hours = defaultdict(float)
        last3 = 0.0
        spend = defaultdict(float)
        n_orders = Counter()
        for ev in events[s]:
            if ev["type"] == "SELL":
                rev[ev["item"]] += ev["revenue"]
                units[ev["item"]] += int(ev["executed"])
                b = next(i for i, (lo, hi) in enumerate(HOUR_BUCKETS) if lo <= ev["hour"] <= hi)
                hours[(ev["item"], b)] += ev["revenue"]
                if ev["day"] >= 27:
                    last3 += ev["revenue"]
                if int(ev["executed"]) > 0:
                    n_orders[ev["item"]] += 1
            elif ev["type"] in ("BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT"):
                spend[ev["item"]] += ev["spent"]
        for p in PRODUCTS:
            row[f"{s_name}_rev_{p.lower()}"] = rev[p]
            row[f"{s_name}_units_{p.lower()}"] = units[p]
            row[f"{s_name}_orders_{p.lower()}"] = n_orders[p]
            for b, (lo, hi) in enumerate(HOUR_BUCKETS):
                row[f"{s_name}_h{lo}_{hi}_{p.lower()}"] = hours[(p, b)]
        row[f"{s_name}_rev_total"] = sum(rev.values())
        row[f"{s_name}_rev_last3"] = last3
        row[f"{s_name}_spend_total"] = sum(spend.values())
        for a in ANIMALS:
            row[f"{s_name}_spend_{a.lower()}"] = spend[a]
    return row


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--team", default="THIRD FARM CLUB")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    hist = pd.read_parquet(DATA / "gold/history.parquet")
    hist["create_time"] = pd.to_datetime(hist["create_time"])
    enc = set(pd.read_csv(FEATURES / "manifest.csv").episode_id.astype(int))
    mine = hist[(hist.team_name == args.team) & (hist.is_current_sub == True) & (hist.episode_id.astype(int).isin(enc))]
    mine = mine.drop_duplicates("episode_id").sort_values("create_time")
    if args.limit:
        mine = mine.head(args.limit)
    sub = int(mine["sub"].iloc[0])
    print(f"{args.team} current submission {sub}: {len(mine)} encoded games", flush=True)
    tasks = [{"episode_id": int(r.episode_id), "seat": int(r.seat)} for r in mine.itertuples()]
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        rows = list(pool.map(one_game, tasks))
    df = pd.DataFrame(rows)
    meta = mine[["episode_id", "create_time", "result", "opp_team_name", "opp_sub", "rating_after", "opp_rating_after"]].copy()
    meta["episode_id"] = meta.episode_id.astype(int)
    df = df.merge(meta, on="episode_id")
    lines = line_hashes()
    df["opp_class"] = np.where(df.opp_h136 == lines["v41"], "line-v41",
                       np.where(df.opp_h136 == lines["v7"], "line-v7",
                       np.where(df.opp_team_name.isin(TOP10), "top10", "other")))
    out = DATA / "top10" / f"klevel_{slug(args.team)}.parquet"
    df.to_parquet(out, index=False)
    print(f"wrote {out} ({len(df)} rows); own line at t136: {df.own_h136.value_counts().iloc[0]} of {len(df)} on the modal line; "
          f"public lines v41 {lines['v41']} v7 {lines['v7']}; money checks with mismatches: {int((df.money_check_own > 0).sum())}")
    pd.set_option("display.width", 220)
    print("\n== K1: opponents by class (games, win rate, median margin)")
    g = df.groupby("opp_class").agg(games=("episode_id", "count"), win=("result", lambda s: (s == "W").mean()),
                                    margin=("bank", "median"), opp_bank=("opp_bank", "median"))
    g["margin"] = df.assign(m=df.bank - df.opp_bank).groupby("opp_class").m.median()
    print(g.round(2).to_string())
    print("\n== opponent teams (top 12 by games)")
    print(df.groupby("opp_team_name").agg(games=("episode_id", "count"), win=("result", lambda s: (s == "W").mean()),
                                          cls=("opp_class", "first")).sort_values("games", ascending=False).head(12).round(2).to_string())
    print("\n== K2: revenue by product, own vs opponent (means over games against the public line)")
    line = df[df.opp_class.str.startswith("line")]
    for p in PRODUCTS:
        pl = p.lower()
        print(f"  {p:<11} own {line[f'own_rev_{pl}'].mean():>8.0f} ({line[f'own_units_{pl}'].mean():>5.0f} u, {line[f'own_orders_{pl}'].mean():>4.0f} lots)"
              f"   opp {line[f'opp_rev_{pl}'].mean():>8.0f} ({line[f'opp_units_{pl}'].mean():>5.0f} u, {line[f'opp_orders_{pl}'].mean():>4.0f} lots)")
    print(f"  total own {line.own_rev_total.mean():.0f} opp {line.opp_rev_total.mean():.0f}; last 3 days own {line.own_rev_last3.mean():.0f} opp {line.opp_rev_last3.mean():.0f}; "
          f"spend own {line.own_spend_total.mean():.0f} opp {line.opp_spend_total.mean():.0f}; hands/day own {line.own_hands_mean.mean():.1f} opp {line.opp_hands_mean.mean():.1f}; "
          f"fertilize ops own {line.own_fertilize_ops.mean():.0f} opp {line.opp_fertilize_ops.mean():.0f}")
    print("\n== K2: sale hours by product (share of revenue at hours 0-1 / 2-11 / 12-19 / 20-23), own vs opp, vs the line")
    for p in PREMIUM + ("CARROT", "TOMATO", "WHEAT"):
        pl = p.lower()
        own = [line[f"own_h{lo}_{hi}_{pl}"].sum() for lo, hi in HOUR_BUCKETS]
        opp = [line[f"opp_h{lo}_{hi}_{pl}"].sum() for lo, hi in HOUR_BUCKETS]
        so, sp = sum(own) or 1, sum(opp) or 1
        print(f"  {p:<11} own " + " ".join(f"{100 * v / so:>3.0f}%" for v in own) + "   opp " + " ".join(f"{100 * v / sp:>3.0f}%" for v in opp))
    print("\n== K2: plan by shop draw (means: with / without the shop by day 9)")
    for g_name in SHOP_GROUPS:
        w, wo = df[df[f"shop_{g_name}"] == 1], df[df[f"shop_{g_name}"] == 0]
        cols = {"cows d15": "own_cow_d15", "sheep d15": "own_sheep_d15", "geese d15": "own_goose_d15",
                "carrots planted": "own_plant_carrot", "tomatoes planted": "own_plant_tomato", "strawberries planted": "own_plant_strawberry", "bank": "bank"}
        print(f"  {g_name:<7} ({len(w)} / {len(wo)} games): " + ", ".join(f"{k} {w[c].mean():.1f} / {wo[c].mean():.1f}" for k, c in cols.items()))
    print("\n== K3: losses")
    losses = df[df.result == "L"].assign(margin=lambda d: d.bank - d.opp_bank).sort_values("margin")
    print(f"  {len(losses)} losses of {len(df)}; by class: {losses.opp_class.value_counts().to_dict()}; shop groups among losses vs all: "
          + ", ".join(f"{g_name} {losses[f'shop_{g_name}'].mean():.2f}/{df[f'shop_{g_name}'].mean():.2f}" for g_name in SHOP_GROUPS))
    for r in losses.itertuples():
        diffs = sorted(((getattr(r, f"opp_rev_{p.lower()}") - getattr(r, f"own_rev_{p.lower()}"), p) for p in PRODUCTS), reverse=True)[:3]
        own_early = sum(getattr(r, f"own_h0_1_{p.lower()}") for p in PREMIUM) / max(1, sum(getattr(r, f"own_rev_{p.lower()}") for p in PREMIUM))
        opp_early = sum(getattr(r, f"opp_h0_1_{p.lower()}") for p in PREMIUM) / max(1, sum(getattr(r, f"opp_rev_{p.lower()}") for p in PREMIUM))
        print(f"  {r.episode_id} vs {str(r.opp_team_name)[:20]:<20} [{r.opp_class:<8}] margin {r.margin:>7.0f} bank {r.bank:>7.0f}  opp ahead on "
              + ", ".join(f"{p} +{d:.0f}" for d, p in diffs) + f"  premium sold at h0-1: own {own_early:.0%} opp {opp_early:.0%}  shops {r.shops3}")


if __name__ == "__main__":
    main()
