"""The thorough analysis of the zone study: what separates the leaders, with the mechanisms read.

    uv run python scripts/top10/deep.py

Builds reports/top10/analysis.md and its figures from data/top10/{features,market,history}.parquet,
data/top10/weed_events.parquet, data/top10/sample.csv and the snapshot. Every table is
regenerable; the prose states what the table shows and where it was checked by hand.
"""

from __future__ import annotations

from collections import Counter

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import research  # noqa: F401,E402
from research.features import mask_unreliable_sales  # noqa: E402
from research.paths import REPORTS, TOP10  # noqa: E402
from research.stats import mann_whitney  # noqa: E402
from research.store import load_trace, trace_path  # noqa: E402
from research.trace import unit_ops  # noqa: E402

FIGS = REPORTS / "figs"
GROUPS = ["top", "gold", "silver", "bronze"]
GROUP_NAMES = {"top": "top-14", "gold": "gold", "silver": "silver", "bronze": "bronze"}
PREMIUM = ["strawberry", "melon", "milk", "wool"]
STAPLE = ["wheat", "carrot", "tomato", "egg", "fertilizer"]
MILK_SHOPS = {"PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP"}
EGG_SHOPS = {"BAKERY", "BRUNCH_SPOT"}
CARROT_SHOPS = {"PET_CAFE", "FARMERS_MARKET"}
STRAWBERRY_SHOPS = {"BRUNCH_SPOT", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP", "FARMERS_MARKET"}
TOMATO_SHOPS = {"PIZZA_SHOP", "FARMERS_MARKET"}


def md_table(df: pd.DataFrame, floatfmt: str = "{:.2f}") -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        cells = []
        for c in cols:
            v = row[c]
            if isinstance(v, float):
                cells.append("" if np.isnan(v) else (f"{v:.0f}" if abs(v) >= 100 or v == int(v) else floatfmt.format(v)))
            else:
                cells.append(str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def load() -> dict:
    feats, masked = mask_unreliable_sales(pd.read_parquet(TOP10 / "features.parquet"))
    feats["create_time"] = feats.groupby("episode_id").create_time.transform("first")
    snap = pd.read_csv(TOP10 / "snapshot_latest.csv")
    hist = pd.read_parquet(TOP10 / "history.parquet")
    teams = pd.read_csv(TOP10 / "teams.csv")
    sample = pd.read_csv(TOP10 / "sample.csv")
    # A team's name in a replay is the name it had when the game was played; the snapshot
    # has the current one. Studied seats carry team_id from the history join, so name them
    # from the snapshot and key every lookup on that name.
    snap_name = dict(zip(snap.team_id, snap.team_name))
    studied = feats.team_id.notna()
    feats.loc[studied, "team"] = feats.loc[studied, "team_id"].map(snap_name).fillna(feats.loc[studied, "team"])
    rank = dict(zip(snap.team_name, snap["rank"]))
    group = dict(zip(snap.team_name, snap.group))
    zone = dict(zip(snap.team_name, snap.zone))
    feats["rank"] = feats.team.map(rank)
    feats["group"] = feats.team.map(group)
    feats["zone"] = feats.team.map(zone)
    if "revenue_total" in feats and "revenue_staple" not in feats:
        feats["revenue_staple"] = feats.revenue_total - feats.revenue_premium
    cur = feats[feats.is_current_sub == True].copy()  # noqa: E712
    counts = cur.team.value_counts()
    cur = cur[cur.team.isin(counts[counts >= 10].index)]
    market = pd.read_parquet(TOP10 / "market.parquet") if (TOP10 / "market.parquet").exists() else None
    weeds = pd.read_parquet(TOP10 / "weed_events.parquet") if (TOP10 / "weed_events.parquet").exists() else None
    return dict(feats=feats, cur=cur, snap=snap, hist=hist, teams=teams, sample=sample, market=market, weeds=weeds, rank=rank, group=group, masked=masked)


def team_order(d: dict, names) -> list[str]:
    return sorted(names, key=lambda t: d["rank"].get(t, 9999))


# ---------------------------------------------------------------- 1. openings


def day1_summary(actions: list[dict]) -> tuple[dict, dict]:
    ops: Counter = Counter()
    buys: Counter = Counter()
    for a in actions[:24]:
        for op in unit_ops(a):
            if op[0] in ("PLANT", "BUILD_PASTURE", "BUILD_COOP"):
                ops[op[0].replace("BUILD_", "").lower() + (f" {op[1].lower()}" if len(op) > 1 else "")] += 1
        for o in a.get("market") or []:
            if o and o[0] in ("BUY_ANIMAL", "BUY_SEED", "HIRE"):
                buys[(o[0].split("_")[-1].lower() + " " + str(o[1]).lower()) if len(o) > 1 else "hire"] += int(o[2]) if len(o) > 2 else 1
    return ops, buys


def section_openings(d: dict) -> str:
    cur = d["cur"]
    rows = []
    for team in team_order(d, cur.team.unique()):
        g = cur[cur.team == team]
        if g.field_h24.nunique() < 2 or g["rank"].iloc[0] > 50:
            continue
        for h, gg in g.groupby("field_h24"):
            if len(gg) < 2:
                continue
            ep, seat = int(gg.episode_id.iloc[0]), int(gg.seat.iloc[0])
            if not trace_path(ep).exists():
                continue
            tr = load_trace(ep)
            ops, buys = day1_summary(tr["seats"][seat]["actions"])
            money = [load_trace(int(e))["seats"][int(s)]["money_by_day"][1] for e, s in zip(gg.episode_id.iloc[:6], gg.seat.iloc[:6])]
            rows.append(
                {
                    "rank": int(g["rank"].iloc[0]),
                    "team": team,
                    "day-1 line": h[:8],
                    "games": len(gg),
                    "win %": round(100 * gg.won.mean()),
                    "seat 0 %": round(100 * (gg.seat == 0).mean()),
                    "$ left at day end": float(np.median(money)),
                    "bought": ", ".join(f"{v} {k}" for k, v in sorted(buys.items())),
                    "planted / built": ", ".join(f"{v} {k}" for k, v in sorted(ops.items())),
                }
            )
    table = pd.DataFrame(rows)
    text = f"""## 1. Day 1: two purchase lists run the plateau, and nobody reads the opponent

The study's branch-driver table said the #1 and Orbital Terraformer "leave their usual day-1
opening when the opponent's opening is unusual". Reading the openings shows what the branch
is. Every team whose games split on day 1 has **one** purchase list; the lines differ only in
the number of wheat seeds planted at the end of the day, because the list spends the $3,000
down to the last few dollars and the final wheat seeds are bought one at a time while the
wheat price (moved by a dollar or two by the opponent's turn-0 wheat trades) decides how many
fit. Checked turn by turn in three replays of the #1 (107673304, 107674293, 107682064: $7, $6,
$5 left; 12, 11, 9 wheat planted; identical farmer actions). The table lists every day-1 line
with at least two games among the teams ranked 50 or better.

{md_table(table)}

Two lists cover the plateau: **2 cows, 3 sheep, 5 pastures, 8 melon, 10-11 wheat, 4 hands**
(Majkel1337, DSM and Orbital Terraformer, byte-identical between the first two) and
**2 cows, 2 sheep, 4 pastures, 12 melon, 7 wheat, 5 hands** (the public family, Unknown
Mother-Goose, redblackbst, Mengfei Li, Catalyst, yomogii, Kaggriculture Agent). Mengfei Li's
twelve day-1 lines have identical purchases and identical money at day end: walking order.
HowardLeeTW (5 cows, 1 sheep, 18 wheat, 1 melon, 7 hands) and Sida Zuo (3 cows, 2 sheep,
7 pastures, 8 melon) are the only different day-1 plans in the top 50. Consequence for the
memo: finding 4 and "layer 2, a day-1 opponent read" have no evidence behind them (P17).
"""
    return text


# ---------------------------------------------------------------- 2. weeds


def section_weeds(d: dict) -> str:
    w = d["weeds"]
    if w is None or "origin" not in w:
        return "## 2. Weeds\n\nNo tile-level weed events on disk (run `scripts/top10/weed_tiles.py`).\n"
    w = w[w.get("error").isna()] if "error" in w else w
    w["rank"] = w.team.map(d["rank"])
    w["group"] = w.team.map(d["group"])
    w["stood_days"] = w.stood_turns / 24
    games = w.groupby("team").episode_id.nunique()
    spawn = w[w.origin == "spawn"]
    decay = w[w.origin == "decay"]
    early = decay[decay.start_day < 27]
    late = decay[decay.start_day >= 27]
    rows = []
    for team in team_order(d, w.team.unique()):
        n = games[team]
        e, l, s = early[early.team == team], late[late.team == team], spawn[spawn.team == team]
        rows.append(
            {
                "rank": int(d["rank"].get(team, 0)),
                "team": team,
                "group": GROUP_NAMES.get(d["group"].get(team), ""),
                "games": n,
                "spawned weeds / game": round(len(s) / n, 1),
                "decayed plants / game (day < 27)": round(len(e) / n, 1),
                "of which strawberry %": round(100 * (e.before == "plant_strawberry").mean()) if len(e) else np.nan,
                "cleared %": round(100 * e.cleared.mean()) if len(e) else np.nan,
                "median days standing": round(e.stood_days.median(), 1) if len(e) else np.nan,
                "empty tiles at that day end": e.empties_at_start_dayend.median() if len(e) else np.nan,
                "decayed / game (day 27-29)": round(len(l) / n, 1),
                "of which cleared %": round(100 * l.cleared.mean()) if len(l) else np.nan,
            }
        )
    table = pd.DataFrame(rows)
    text = f"""## 2. "Standing weeds" are exhausted strawberries, and a full farm cannot grow a weed

Tile-level pass over {w.episode_id.nunique()} current-submission replays of {w.team.nunique()} teams
(`scripts/top10/weed_tiles.py`, {len(w)} weed events). The engine rolls the 0.5% weed chance only on
**empty** unlocked tiles; the plateau farm keeps every tile occupied from day 8, so weeds that
spawn are rare ({len(spawn)} of {len(w)} events, 0.1 to 2 a game). Everything else counted as a "weed"
in the feature table is a plant that reached the end of its life and decayed in place: a
strawberry after its fourth yield ({round(100 * (decay.before == "plant_strawberry").mean())}% of decay events), or wheat,
tomato and carrot left unharvested by the leaders. The public family digs every one within
about 0.6 days; the leaders leave 5-27% of the mid-game ones standing for a day or two while
they have spare empty tiles, and most of the ones that decay in the last three days forever.

{md_table(table)}

So memo finding 14 ("the top 7 tolerate weeds") describes an executor that digs when it needs
the tile, not a labour strategy: an exhausted plant costs one DIG whether it is removed before
or after it turns into a weed, which is why the DIG counts match. Finding 5 (weeds coupled to
the opponent through the shared random stream) stands, but it bites only while a farm has
empty tiles: the first week, and the leaders' spare tiles.
"""
    return text


# ---------------------------------------------------------------- 3. shops


def shop_flags(cur: pd.DataFrame, n_first: int = 3) -> pd.DataFrame:
    early = cur.shops.fillna("").str.split("|").apply(lambda l: l[:n_first])
    out = cur.copy()
    out["yarn_early"] = early.apply(lambda l: "YARN_STORE" in l)
    out["milk_early"] = early.apply(lambda l: any(s in MILK_SHOPS for s in l))
    out["egg_early"] = early.apply(lambda l: any(s in EGG_SHOPS for s in l))
    out["carrot_early"] = early.apply(lambda l: any(s in CARROT_SHOPS for s in l))
    return out


def section_shops(d: dict) -> str:
    cur = shop_flags(d["cur"])
    rows = []
    for team in team_order(d, cur.team.unique()):
        g = cur[cur.team == team]
        if len(g) < 30:
            continue
        r = {"rank": int(g["rank"].iloc[0]), "team": team, "group": GROUP_NAMES.get(g.group.iloc[0], ""), "games": len(g)}
        for flag, col, label in (("yarn_early", "bought_sheep", "sheep"), ("milk_early", "bought_cow", "cows"), ("egg_early", "bought_goose", "geese"), ("carrot_early", "plants_carrot", "carrot plantings"), ("milk_early", "plants_tomato", "tomato plantings")):
            a, b = g[g[flag]], g[~g[flag]]
            r[f"{label}: shop / none"] = f"{a[col].mean():.1f} / {b[col].mean():.1f}" if len(a) and len(b) else ""
        rows.append(r)
    table = pd.DataFrame(rows)
    grp = []
    for gname in GROUPS:
        g = cur[cur.group == gname]
        if not len(g):
            continue
        r = {"group": GROUP_NAMES[gname], "teams": g.team.nunique()}
        for flag, col, label in (("yarn_early", "bought_sheep", "sheep"), ("milk_early", "bought_cow", "cows"), ("egg_early", "bought_goose", "geese"), ("carrot_early", "plants_carrot", "carrot plantings"), ("milk_early", "plants_tomato", "tomato plantings")):
            a, b = g[g[flag]], g[~g[flag]]
            r[f"{label}: shop / none"] = f"{a[col].median():.1f} / {b[col].median():.1f}"
        grp.append(r)
    early = cur.shops.fillna("").str.split("|").apply(lambda l: l[:3])
    cur["tomato_early"] = early.apply(lambda l: any(s in TOMATO_SHOPS for s in l))
    breadth_rows = []
    for team, g in cur.groupby("team"):
        if len(g) < 30:
            continue

        def diff(flag, col):
            a, b = g[g[flag]][col], g[~g[flag]][col]
            return (a.mean() - b.mean()) if len(a) >= 3 and len(b) >= 3 else np.nan

        ds = {"sheep": diff("yarn_early", "bought_sheep"), "cows": diff("milk_early", "bought_cow"), "geese": diff("egg_early", "bought_goose"), "carrots": diff("carrot_early", "plants_carrot"), "tomatoes": diff("tomato_early", "plants_tomato")}
        score = int((ds["sheep"] > 3) + (ds["cows"] > 1.5) + (ds["geese"] > 1) + (ds["carrots"] > 10) + (ds["tomatoes"] > 3))
        breadth_rows.append({"rank": int(g["rank"].iloc[0]), "team": team, "group": g.group.iloc[0], **{f"d {k}": round(v, 1) for k, v in ds.items()}, "breadth (0-5)": score})
    br = pd.DataFrame(breadth_rows).sort_values("rank")
    br_group = br.groupby("group")["breadth (0-5)"].agg(["median", "mean"]).reindex(GROUPS).reset_index()
    br_group["group"] = br_group.group.map(GROUP_NAMES)
    br_group["AUC vs next zone"] = [auc_line(br.rename(columns={"breadth (0-5)": "b"}), "b", a, b) for a, b in (("top", "gold"), ("gold", "silver"), ("silver", "bronze"), ("bronze", "bronze"))]
    br_show = br.copy()
    br_show["group"] = br_show.group.map(GROUP_NAMES)
    text = f"""## 3. Everyone on the plateau reacts to the shop draw; the leaders react to more of it

The town unlocks eight shop instances at days 3, 6, 9, ... 24, drawn with replacement, and each
instance consumes one of every product it lists every four turns (12 a day; a single-product
shop 24 a day) against a town centre that takes one of each a day. A premium product's whole
demand curve is therefore decided by the draw. Conditioning each team's current-submission
games on the shops unlocked by day 9 (the first three entries of `shops`):

{md_table(pd.DataFrame(grp))}

Every one of the profiled teams, from the #1 to the last bronze team, buys 10-14 sheep when a
Yarn Store is among the first three shops and 4-6 otherwise, and 8-9 cows against 5-7 with a
milk shop (Pizza, Ice Cream, Smoothie). The public family is therefore not a pure tape: it is
one shared agent whose herd follows the demand the town reveals, which is what the "shop"
branch driver in `groups.md` was measuring. The leaders differ in the breadth of the response:

{md_table(table)}

Carrots and tomatoes are where the leaders react and the family does not (the family plants
31 carrots and no tomatoes whatever the draw). SpaTaro goes furthest on herds (20 sheep with a
Yarn Store, 13 cows with a milk shop). The reactive layer that exists on the ladder is
"produce what the town is buying", and the study's reactivity gradient is a gradient in the
breadth of that response, not in whether a team reacts. Counting, per team, how many of the
five products its plan follows (thresholds: 3 sheep, 1.5 cows, 1 goose, 10 carrots, 3
tomatoes between games with and without the shop by day 9):

{md_table(br_group)}

{md_table(br_show)}

Every bronze team follows the Yarn Store and nothing else; the family agent ships with
switches its users set differently (Catalyst 2, Kaggriculture Agent 4, feel the agi 5 on the
same day-1 line).
"""
    return text


# ---------------------------------------------------------------- 4. generations and trajectories


def section_generations(d: dict) -> str:
    f = d["feats"].copy()
    f["date"] = pd.to_datetime(f.create_time).dt.normalize()
    key = "field_h136"
    vc = f[key].value_counts()
    big = vc[vc >= 100].index
    prof = (
        f[f[key].isin(big)]
        .groupby(key)
        .agg(seats=("episode_id", "size"), teams=("team", "nunique"), first=("date", "min"), last=("date", "max"), hands=("peak_hands", "median"), cows=("bought_cow", "median"), sheep=("bought_sheep", "median"), geese=("bought_goose", "median"), strawberry=("plants_strawberry", "median"), wheat=("plants_wheat", "median"), melon=("plants_melon", "median"), carrot=("plants_carrot", "median"), tomato=("plants_tomato", "median"), care=("op_care", "median"), fertilize=("op_fertilize", "median"), bank=("final_money", "median"))
        .sort_values("first")
        .reset_index()
    )
    prof["line"] = [f"G{i + 1}" for i in range(len(prof))]
    label = dict(zip(prof[key], prof.line))
    cur = d["cur"]
    who = {}
    for h, g in cur[cur[key].isin(big)].groupby(key):
        vc2 = g.team.value_counts()
        who[label[h]] = ", ".join(f"{t}" for t in vc2.index[:6]) + (f" (+{len(vc2) - 6})" if len(vc2) > 6 else "")
    prof["current subs on it"] = prof.line.map(who).fillna("")
    prof["first"] = prof["first"].dt.strftime("%m-%d")
    prof["last"] = prof["last"].dt.strftime("%m-%d")
    prof = prof.drop(columns=[key])
    f["line"] = f[key].map(label).fillna("other")
    share = pd.crosstab(f.date.dt.strftime("%m-%d"), f.line, normalize="index")
    share = share[[c for c in prof.line if c in share.columns] + ["other"]]
    share["seats"] = f.groupby(f.date.dt.strftime("%m-%d")).size()
    share = share[share.seats >= 50]
    share_tbl = (share.drop(columns="seats") * 100).round(0).astype(int).astype(str).replace("0", "")
    share_tbl["seats"] = share.seats
    share_tbl = share_tbl.reset_index().rename(columns={"date": "day"})
    text = f"""## 4. The plateau is a sequence of public lines, each replacing the last within a week

Grouping every sampled seat (both players of every sampled game, {len(f)} seats) by its
farmer-and-hand action line through day 5 (`field_h136`) and keeping the lines with at least
100 seats gives the public generations of the tape. Medians per line:

{md_table(prof)}

Share of sampled seats on each line by game date (percent; the sample over-weights the
studied teams' windows, so read the columns as when a line appeared and when it went, not as
ladder-wide shares):

{md_table(share_tbl)}

The line that runs the medal plateau today (G with 33 strawberry, 163 wheat, 12 melon, 31
carrot, 8 cows, 6 sheep, 3 geese) first appears on 2026-09-09 and is on two thirds of sampled
seats by 09-15; the line before it (33 strawberry, 185 wheat, 9 carrots, 1 goose) appeared
on 09-02 and peaked on 09-05/06; before that, lines from 08-30, 08-23, 08-14 and 08-03 each
had their week. A new public line every seven to ten days is the ladder's clock, and the
final tournament (games after 2026-09-30) will be played against whatever line is public by
then, not against today's. The one line in the table that belongs to a leader is Artem The
Farmer's (26.5 strawberry, 145 wheat, 37 carrot, 9 tomato, land on days 6 and 8, 149
fertilize), on three teams' seats.
"""
    return text


def section_trajectories(d: dict) -> str:
    hist = d["hist"].merge(d["snap"][["team_id", "rank", "group"]], on="team_id").sort_values("create_time")
    rows = []
    for tid, g in hist.groupby("team_id"):
        gr = g.dropna(subset=["rating_after"])
        hit = gr[gr.rating_after >= 2900]
        first_game = g.create_time.min()
        rows.append(
            {
                "rank": int(g["rank"].iloc[0]),
                "team": g.team_name.iloc[0],
                "group": GROUP_NAMES.get(g.group.iloc[0], ""),
                "first public game": first_game.strftime("%m-%d"),
                "submissions found": g["sub"].nunique(),
                "first game rated 2900+": hit.create_time.min().strftime("%m-%d") if len(hit) else "never",
                "submissions before it": g[g.create_time < hit.create_time.min()]["sub"].nunique() if len(hit) else np.nan,
                "days to it": round((hit.create_time.min() - first_game).total_seconds() / 86400, 1) if len(hit) else np.nan,
            }
        )
    t = pd.DataFrame(rows).sort_values("rank")
    wt = pd.read_csv(TOP10 / "window_trajectories.csv") if (TOP10 / "window_trajectories.csv").exists() else None
    wtext = ""
    if wt is not None:
        keep = ["team_name", "window", "from_", "games", "subs", "win", "opp", "modal_h100", "distinct400", "hands", "cows", "sheep", "geese", "straw", "wheat", "melon", "carrot", "tomato", "care", "fert", "money"]
        wt = wt[keep].rename(columns={"team_name": "team", "from_": "from", "modal_h100": "modal line share @day4", "distinct400": "distinct @day16", "straw": "strawberry", "fert": "fertilize", "money": "bank", "opp": "opp rating"})
        wt["win"] = (wt.win * 100).round(0)
        wt["modal line share @day4"] = (wt["modal line share @day4"] * 100).round(0)
        wt["distinct @day16"] = (wt["distinct @day16"] * 100).round(0)
        parts = []
        for team, g in wt.groupby("team", sort=False):
            if len(g) < 3:
                continue
            parts.append(f"**{team}** (rank {d['rank'].get(team, '')})\n\n" + md_table(g.drop(columns=["team"])))
        wtext = "\n\n".join(parts)
    text = f"""## 5. Trajectories: everyone climbed in the same week, on new submissions

![rating paths](figs/an_rating_paths_top15.png)

One line per submission, rating after each public game, teams ranked 1-15. The picture is the
same for almost every team: weeks of submissions between 1,000 and 2,500, then a new
submission between 2026-09-06 and 09-13 that goes to 3,000 within its first hundred games.
Ratings are relative, so a 2,900 in early August (DSM, Mengfei Li, leave you, Thomas
Tschinkel, Kaggriculture Agent, THUNDER THUNDER, fog flower, Jacky Chan, Cyrus, kevin park,
Emile Andrieu, local) meant less than a 2,900 now; the table dates each team's first game
rated 2,900 or more and how many submissions it took.

{md_table(t)}

Per-window farm and determinism for the teams with history windows (F first 50 games, Q1-Q3
quarter points, L last 50, C0 current submission's first 50; windows are frozen at the
sample dates in `METHOD.md`). "Modal line share" is the share of the window's games on its
most common farmer-and-hand line at day 4; "distinct" the share of distinct lines at day 16.

{wtext}

What the windows say, team by team: the leaders' current farms are recognisable in their
first windows (Artem's fixed five-day opening and 13 hands from 08-19; Majkel1337's 11 hands,
8 cows and 13-14 melon from 08-28; Otter Vibe's geese and tomatoes from 08-27), and what
changed between the early windows and now is wheat (from 8-140 to 140-190 plantings),
carrots and tomatoes (from none to 30-50 and 8-10), fertilizer (from 50-80 to 150-190 ops),
and geese. The family teams' windows show the public generations of section 4 one after
another (Zhenghongshuang, Thomas Tschinkel, ElephtAI and Emile Andrieu's first windows are
the 08-13 line; アルモンド's and redblackbst's the 09-01 line; every family C0 the 09-09
line). The "tape to runtime" story of the memo is therefore two different stories: the
leaders were runtime agents from their first window and improved their economy; the family
teams replaced one public line with the next.
"""
    return text


# ---------------------------------------------------------------- 6. head to head


def section_h2h(d: dict) -> str:
    hist = d["hist"]
    snap = d["snap"]
    top = snap[snap["rank"] <= 15].sort_values("rank")
    ids = top.team_id.tolist()
    names = dict(zip(top.team_id, top.team_name))
    cur_sub = dict(zip(d["teams"].team_id, d["teams"].current_sub))
    hh = hist[hist.team_id.isin(ids) & hist.opp_team_id.isin(ids)]
    hh_cur = hh[hh.is_current_sub & (hh.opp_sub == hh.opp_team_id.map(cur_sub))]

    def matrix(df):
        m = pd.DataFrame("", index=[names[i][:14] for i in ids], columns=[names[i][:10] for i in ids])
        for a in ids:
            for b in ids:
                if a == b:
                    continue
                g = df[(df.team_id == a) & (df.opp_team_id == b)]
                if len(g):
                    m.loc[names[a][:14], names[b][:10]] = f"{(g.result == 'W').sum()}-{(g.result == 'L').sum()}"
        return m.reset_index().rename(columns={"index": "row beats column"})

    margin = (hh_cur.bank - hh_cur.opp_bank).abs()
    seat = hist.assign(win=(hist.result == "W")).groupby("seat").win.mean()
    text = f"""## 6. Who beats whom at the top

Current submissions on both sides, teams ranked 1-15 at the full snapshot (W-L, row beats column):

{md_table(matrix(hh_cur))}

All public games between the same teams, any submission:

{md_table(matrix(hh))}

Artem The Farmer beats Majkel1337 19-11 on current submissions (58-54 all-time); Majkel1337
beats everyone else by wide margins (21-2 Mengfei Li, 14-2 feel the agi, 10-0 SpaTaro, 5-0
Orbital Terraformer, 4-0 DSM) and is level with Unknown Mother-Goose (4-4). Of {len(hh_cur)}
current-submission games among these teams the median bank margin is {margin.median():.0f}, a quarter
are within {margin.quantile(0.25):.0f}. There is no seat effect: seat 0 wins {100 * seat[0]:.1f}% and seat 1 {100 * seat[1]:.1f}%
of the studied teams' {len(hist):,} games.
"""
    return text


# ---------------------------------------------------------------- 7. market, corrected


def team_medians(cur: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    return cur.groupby(["group", "rank", "team"])[cols].median().reset_index().sort_values("rank")


def group_of_team_medians(tm: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    g = tm.groupby("group")[cols].median()
    g = g.reindex([x for x in GROUPS if x in g.index])
    g.insert(0, "teams", tm.groupby("group").team.nunique().reindex(g.index))
    g.index = [GROUP_NAMES[x] for x in g.index]
    return g.reset_index().rename(columns={"index": "group"})


def auc_line(tm: pd.DataFrame, col: str, a: str = "top", b: str = "gold") -> str:
    x, y = tm[tm.group == a][col].dropna(), tm[tm.group == b][col].dropna()
    if len(x) < 3 or len(y) < 3:
        return ""
    auc, p = mann_whitney(list(x), list(y))
    return f"{auc:.2f} (p={p:.2f})"


def section_market(d: dict) -> str:
    cur = d["cur"]
    mk = d["market"]
    if "revenue_total" not in cur or mk is None or "units_cheap_melon" not in mk:
        return "## 7. Market\n\nCorrected sales columns are missing; rebuild traces, features and market.parquet first.\n"
    cur = cur.merge(mk.drop(columns=["team"]), on=["episode_id", "seat"], how="left", suffixes=("", "_mk"))
    cur["premium_units"] = sum(cur[f"sold_{p}"] for p in PREMIUM)
    cur["premium_cheap_pct"] = 100 * sum(cur[f"units_cheap_{p}"] for p in PREMIUM) / cur.premium_units.replace(0, np.nan)
    cur["last3_share_pct"] = 100 * cur.revenue_last_3_days / cur.revenue_total.replace(0, np.nan)
    cols = ["final_money", "revenue_total", "revenue_premium", "revenue_staple", "revenue_last_3_days", "last3_share_pct", "hire_spend", "sold_melon", "price_melon", "sold_strawberry", "price_strawberry", "sold_milk", "price_milk", "sold_wool", "price_wool", "sold_egg", "sold_wheat", "price_wheat", "sold_carrot", "sold_tomato", "sold_fertilizer", "premium_cheap_pct"]
    tm = team_medians(cur, cols)
    grp = group_of_team_medians(tm, cols)
    grp_t = grp.set_index("group").T.reset_index().rename(columns={"index": "median of per-team medians"})
    grp_t["P(top-14 > gold)"] = [auc_line(tm, c) if c in cols else "" for c in grp_t["median of per-team medians"]]
    grp_t["P(gold > silver)"] = [auc_line(tm, c, "gold", "silver") if c in cols else "" for c in grp_t["median of per-team medians"]]
    show = tm[tm["rank"] <= 31].copy()
    show["group"] = show.group.map(GROUP_NAMES)
    show_cols = ["rank", "team", "group", "final_money", "revenue_premium", "revenue_staple", "revenue_last_3_days", "sold_melon", "price_melon", "sold_strawberry", "price_strawberry", "sold_milk", "price_milk", "sold_wool", "price_wool", "sold_egg", "sold_carrot", "sold_tomato", "premium_cheap_pct"]

    fig, axes = plt.subplots(1, 4, figsize=(18, 4), sharey=False)
    for ax, p in zip(axes, PREMIUM):
        col = f"units_by_day_{p}"
        for gname in GROUPS:
            g = cur[cur.group == gname]
            if not len(g):
                continue
            arr = np.array([np.asarray(v) for v in g[col] if v is not None and len(v) == 30])
            if not len(arr):
                continue
            ax.plot(range(30), np.median(arr, axis=0), label=GROUP_NAMES[gname], lw=1.5)
        for team, ls in (("Majkel1337", "--"), ("Artem The Farmer 🍅", ":")):
            g = cur[cur.team == team]
            arr = np.array([np.asarray(v) for v in g[col] if v is not None and len(v) == 30])
            if len(arr):
                ax.plot(range(30), np.median(arr, axis=0), ls=ls, color="black", lw=1.2, label=team.split(" ")[0])
        ax.set_title(f"{p}: median units sold per day")
        ax.set_xlabel("day")
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / "an_sales_by_day.png", dpi=110)
    plt.close(fig)

    sc = shop_flags(cur)
    early = sc.shops.fillna("").str.split("|").apply(lambda l: l[:3])
    sc["straw_shops_early"] = early.apply(lambda l: sum(s in STRAWBERRY_SHOPS for s in l))
    rows = []

    def cond(g, flag, col):
        a, b = g[g[flag]], g[~g[flag]]
        if len(a) < 3 or len(b) < 3:
            return ""
        return f"{a[col].median():,.0f} / {b[col].median():,.0f}"

    for gname in GROUPS:
        g = sc[sc.group == gname]
        if not len(g):
            continue
        rows.append(
            {
                "who": GROUP_NAMES[gname],
                "games": len(g),
                "wool revenue: Yarn Store early / not": cond(g, "yarn_early", "revenue_wool"),
                "milk revenue: milk shop early / not": cond(g, "milk_early", "revenue_milk"),
                "egg revenue: egg shop early / not": cond(g, "egg_early", "revenue_egg"),
                "carrot revenue: carrot shop early / not": cond(g, "carrot_early", "revenue_carrot"),
                "bank: Yarn Store early / not": cond(g, "yarn_early", "final_money"),
            }
        )
    for team in team_order(d, sc.team.unique())[:10]:
        g = sc[sc.team == team]
        rows.append(
            {
                "who": f"#{int(g['rank'].iloc[0])} {team}",
                "games": len(g),
                "wool revenue: Yarn Store early / not": cond(g, "yarn_early", "revenue_wool"),
                "milk revenue: milk shop early / not": cond(g, "milk_early", "revenue_milk"),
                "egg revenue: egg shop early / not": cond(g, "egg_early", "revenue_egg"),
                "carrot revenue: carrot shop early / not": cond(g, "carrot_early", "revenue_carrot"),
                "bank: Yarn Store early / not": cond(g, "yarn_early", "final_money"),
            }
        )
    shop_tbl = pd.DataFrame(rows)
    text = f"""## 7. The market, measured correctly

Every number here comes from the rebuilt traces (P18): executed units and revenue per sale as
the engine computed them, checked against the recorded money in every turn of every game.
Seats where that check fails are excluded from every sales column before any median is taken
(`research/features.py`): {len(d["masked"])} of {len(d["feats"])} seat rows in the whole sample, of which
{int((d["masked"].is_current_sub == True).sum())} are current-submission rows (final-step
mismatches of at most $466, see P18); the rest are historical windows played on engine
versions 1.32.2-1.32.6, whose market this replica does not model (Emile Andrieu's,
Thomas Tschinkel's and THUNDER THUNDER's first-50 windows and Mengfei Li's first quarter
window in full). Medians of per-team medians by group, with the chance that a random top-14
team is above a random gold team:

{md_table(grp_t)}

Per team, ranks 1-31:

{md_table(show[show_cols])}

![units sold per day](figs/an_sales_by_day.png)

Median units sold per day by group (solid), with Majkel1337 (dashed) and Artem The Farmer
(dotted). Revenue conditional on the shops unlocked by day 9 (medians, "with / without"):

{md_table(shop_tbl)}

**What the corrected numbers say.** The zones do not differ in what they sell or in what
they bank: total revenue is 133-136k and the final bank 102-105k in every group, and the
top-14 sell *fewer* premium units than the family (strawberry 222 against 248, milk 182
against 191, wool 113 against 126, melon 75 against 72) at higher prices (strawberry $125
against $116, milk $93 against $84, wool $117 against $105). The family sells 342 fertilizer
a game against the leaders' 218, because the leaders spread it on the fields. Every earlier
"the #1 sells four times the melon" statement was the P18 undercount. The leaders' edge is
relative, and section 9b shows where it comes from; the per-day tables behind the figure
(mean units and revenue per day, computed from `market.parquet`) give the mechanism:

- **The public line's clock is fixed.** Melon: 60 units on day 10 and the last 12 on day 11.
  No shop demands melon, so the town removes one a day and a 72-melon dump takes the price
  from $250 to about $200 (the glut curve is quadratic, 3.6 times base over 300 units); two
  farms dumping in the same hours take it near the floor. Strawberries: days 15-29 with the
  bulk on days 20-24 at 20-29 a day, sold late in the day (hours 13 and 19-23) in orders of
  six. Milk about 10 a day from day 8; wool 8-16 every third day from day 6; wheat rising
  to 61 on day 29; fertilizer 10-20 a day all season.
- **The town's drain sets the price-holding rate.** Median units removed per day across the
  sampled games: strawberry 7 before the shops accumulate and 22-36 from day 18; milk 14;
  wool 12; carrot 13; egg 7; tomato 7; wheat 32; melon 1. Strawberry's price falls by 1.6
  times base for every 100 units above the anchor and milk's by the same for every 122, so
  whoever sells faster than the drain crashes the price for both farms.
- **Out-earning = metering.** Majkel1337 sells strawberries in orders of two spread over the
  day (67 orders a game against the line's 40 of six): 18-21 a day on days 16-18 at about
  $190 like everyone, then 9-10 a day from day 20 while the line sells 20-29. It holds
  $144-170 a unit through day 28 while the line's own units fetch $67-75 on days 22-24, and
  sells its last 20 at $150 on day 29. Milk goes out in bursts of 18-19 on days 14 and 16,
  ahead of the line's day-15 burst. Result: $169 a strawberry, $100 a milk, $132 a wool on
  fewer units, and a bank of 113k against the family's 101-105k.
- **Starving = selling first and selling every day.** 29% of Artem's strawberries and 23% of
  ymg_aq's leave at hour 0, from the previous day's harvest, before the line's evening
  orders; both then sell every premium product every day to the end (Artem 10-14 milk,
  6-9 wool, 7-12 strawberries a day through day 29) so the price never recovers, and they
  replace the late premium income with staples (Artem 44k, ymg_aq 71k, of which 48k is
  1,270 wheat at $38: wheat's glut curve is logarithmic and 400 units cost $5). The line's
  late dump then meets a loaded market: its strawberry price falls to $93 against Artem and
  $77 against ymg_aq (reference $110), its milk to $70 and $69 (reference $82).
- **Melon timing is worthless.** Spreading melon (Majkel1337 29 on day 10 and a trickle to
  day 22; ymg_aq days 16-19) earns 13.9k against the dump's 14.6k, because the glut never
  clears. The "melon last sell day 20 against 11" separator in `groups.md` is real and means
  nothing for the bank.
"""
    return text


# ---------------------------------------------------------------- 8. labour


def section_labour(d: dict) -> str:
    cur = d["cur"]
    mk = d["market"]
    if mk is None or "days_cow" not in mk or "revenue_total" not in cur:
        return "## 8. Labour\n\nMissing market.parquet or corrected feature columns.\n"
    cur = cur.merge(mk[["episode_id", "seat", "days_cow", "days_sheep", "days_goose", "tile_days_strawberry", "tile_days_wheat", "tile_days_melon", "hire_spend", "hires_total"]], on=["episode_id", "seat"], how="left")
    hands_days = cur.hands_by_day.apply(lambda v: float(np.sum(v)) if v is not None else np.nan)
    animal_days = cur.days_cow + cur.days_sheep + cur.days_goose
    cur = cur.assign(
        milk_per_cow_day=cur.sold_milk / cur.days_cow.replace(0, np.nan),
        wool_per_sheep_day=cur.sold_wool / cur.days_sheep.replace(0, np.nan),
        egg_per_goose_day=cur.sold_egg / cur.days_goose.replace(0, np.nan),
        care_per_animal_day=cur.op_care / animal_days.replace(0, np.nan),
        feed_per_animal_day=cur.op_feed / animal_days.replace(0, np.nan),
        fert_per_strawberry=cur.op_fertilize / cur.plants_strawberry.replace(0, np.nan),
        strawberry_per_planting=cur.sold_strawberry / cur.plants_strawberry.replace(0, np.nan),
        wheat_per_planting=cur.sold_wheat / cur.plants_wheat.replace(0, np.nan),
        melon_per_planting=cur.sold_melon / cur.plants_melon.replace(0, np.nan),
        revenue_per_hand_day=cur.revenue_total / hands_days.replace(0, np.nan),
        water_per_tile_day=cur.op_water / (cur.tile_days_strawberry + cur.tile_days_wheat + cur.tile_days_melon).replace(0, np.nan),
        dig_ops=cur.op_dig,
        pass_ops=cur.op_pass,
    )
    cols = ["milk_per_cow_day", "wool_per_sheep_day", "egg_per_goose_day", "care_per_animal_day", "feed_per_animal_day", "fert_per_strawberry", "strawberry_per_planting", "wheat_per_planting", "melon_per_planting", "revenue_per_hand_day", "water_per_tile_day", "dig_ops", "pass_ops", "hire_spend"]
    tm = team_medians(cur, cols)
    grp = group_of_team_medians(tm, cols)
    grp_t = grp.set_index("group").T.reset_index().rename(columns={"index": "median of per-team medians"})
    grp_t["P(top-14 > gold)"] = [auc_line(tm, c) if c in cols else "" for c in grp_t["median of per-team medians"]]
    show = tm[tm["rank"] <= 31].copy()
    show["group"] = show.group.map(GROUP_NAMES)
    text = f"""## 8. Labour: what an action buys

Yields per animal-day and per planting, and ops per unit of work, from the corrected sales
and the day-end farm censuses. An animal-day is one animal present at one day end; a
cow yields base 1 milk every second day plus its banked CARE days, a sheep 1 wool every third
day plus CARE, a goose 1 egg a day plus CARE (all capped by `max_held`).

{md_table(grp_t)}

Per team, ranks 1-31:

{md_table(show[["rank", "team", "group"] + cols])}
"""
    return text


# ---------------------------------------------------------------- 9. PCA and clustering


PCA_FEATURES = [
    "peak_hands", "bought_cow", "bought_sheep", "bought_goose", "plants_strawberry", "plants_wheat", "plants_melon", "plants_carrot", "plants_tomato",
    "land_day_1", "land_day_2", "op_care", "op_fertilize", "op_dig", "op_water", "op_harvest", "op_plant", "op_pass", "weed_days",
    "sold_melon", "sold_strawberry", "sold_milk", "sold_wool", "sold_egg", "sold_wheat", "sold_carrot", "sold_tomato", "sold_fertilizer",
    "revenue_premium", "revenue_staple", "revenue_last_3_days", "price_melon", "price_strawberry", "price_milk", "price_wool", "invalid_orders",
]


def kmeans(X: np.ndarray, k: int, seed: int = 0, iters: int = 100) -> np.ndarray:
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(10):
        centers = X[rng.choice(len(X), k, replace=False)]
        for _ in range(iters):
            lab = np.argmin(((X[:, None, :] - centers[None]) ** 2).sum(-1), axis=1)
            new = np.array([X[lab == j].mean(0) if (lab == j).any() else centers[j] for j in range(k)])
            if np.allclose(new, centers):
                break
            centers = new
        inertia = sum(((X[lab == j] - centers[j]) ** 2).sum() for j in range(k))
        if best is None or inertia < best[0]:
            best = (inertia, lab)
    return best[1]


def section_pca(d: dict) -> str:
    cur = d["cur"]
    feats = [c for c in PCA_FEATURES if c in cur]
    if len(feats) < 20:
        return "## 9. Structure\n\nCorrected feature columns missing.\n"
    X = cur[feats].astype(float)
    X = X.fillna(X.median())
    mu, sd = X.mean(), X.std().replace(0, 1)
    Z = ((X - mu) / sd).to_numpy()
    U, S, Vt = np.linalg.svd(Z, full_matrices=False)
    var = S**2 / (S**2).sum()
    scores = U[:, :3] * S[:3]
    load = pd.DataFrame(Vt[:3].T, index=feats, columns=["PC1", "PC2", "PC3"])
    load_rows = []
    for pc in ("PC1", "PC2", "PC3"):
        s = load[pc].sort_values()
        load_rows.append({"component": pc, "variance %": round(100 * var[int(pc[-1]) - 1], 1), "negative end": ", ".join(f"{i} ({v:.2f})" for i, v in s.head(5).items()), "positive end": ", ".join(f"{i} ({v:.2f})" for i, v in s.tail(5)[::-1].items())})
    sc = cur[["team", "group", "rank", "won"]].copy()
    sc["PC1"], sc["PC2"], sc["PC3"] = scores[:, 0], scores[:, 1], scores[:, 2]
    cent = sc.groupby(["group", "rank", "team"])[["PC1", "PC2", "PC3"]].median().reset_index().sort_values("rank")
    fig, ax = plt.subplots(figsize=(9, 7))
    colors = {"top": "#c0392b", "gold": "#d4a017", "silver": "#7f8c8d", "bronze": "#8e5a2b"}
    for gname in GROUPS:
        g = sc[sc.group == gname]
        ax.scatter(g.PC1, g.PC2, s=4, alpha=0.15, color=colors[gname])
        c = cent[cent.group == gname]
        ax.scatter(c.PC1, c.PC2, s=40, color=colors[gname], edgecolor="black", label=GROUP_NAMES[gname])
    for r in cent[cent["rank"] <= 10].itertuples():
        ax.annotate(f"#{int(r.rank)} {r.team[:12]}", (r.PC1, r.PC2), fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel(f"PC1 ({100 * var[0]:.0f}%)")
    ax.set_ylabel(f"PC2 ({100 * var[1]:.0f}%)")
    ax.legend()
    ax.set_title("Current-submission games (faint) and team medians (solid), first two components")
    fig.tight_layout()
    fig.savefig(FIGS / "an_pca.png", dpi=110)
    plt.close(fig)
    tm = cur.groupby(["group", "rank", "team"])[feats].median().reset_index().sort_values("rank")
    Zt = ((tm[feats] - mu) / sd).fillna(0).to_numpy()
    rows = []
    for k in (2, 3, 4, 5):
        lab = kmeans(Zt, k)
        tm[f"k{k}"] = lab
        for j in range(k):
            members = tm[tm[f"k{k}"] == j]
            rows.append({"k": k, "cluster": j, "teams": len(members), "top-14": int((members.group == "top").sum()), "gold": int((members.group == "gold").sum()), "silver": int((members.group == "silver").sum()), "bronze": int((members.group == "bronze").sum()), "who (by rank)": ", ".join(members.sort_values("rank").team.head(8)) + (" ..." if len(members) > 8 else "")})
    clus = pd.DataFrame(rows)
    sep = cent.groupby("group")[["PC1", "PC2", "PC3"]].median().reindex(GROUPS)
    sep.index = [GROUP_NAMES[g] for g in sep.index]
    text = f"""## 9. Structure: one dense public point and two leader clusters

PCA over {len(cur)} current-submission games of {cur.team.nunique()} teams on {len(feats)} standardised features
(farm plan, ops, corrected sales and prices). The first three components carry
{100 * var[:3].sum():.0f}% of the variance. PC1 runs from the family's signature (fertilizer sold rather
than used, CARE every day, land bought late, wool) to the leaders' (fertilizer used, tomatoes
and eggs, geese); PC2 separates the two leader groups (cows, strawberries and milk against
sheep, carrots and wool):

{md_table(pd.DataFrame(load_rows))}

![pca](figs/an_pca.png)

Group medians of the team centroids:

{md_table(sep.reset_index().rename(columns={"index": "group"}))}

k-means on the {len(tm)} team medians (standardised the same way), for k = 2 to 5, with the zone
make-up of each cluster:

{md_table(clus)}

The picture is not a continuum: 44 of the 59 teams form one tight cluster (every silver and
bronze team, nine of the fourteen gold, and the five family members of the top-14) with a
within-team spread of about 0.5 on PC1; the other 15 teams split into two stable groups, the
2-cow-3-sheep code base and its relatives (Majkel1337, DSM, Orbital Terraformer, SpaTaro,
Artem The Farmer, ymg_aq, Sida Zuo) and the goose-and-tomato agents (Unknown Mother-Goose,
THIRD FARM CLUB, Mengfei Li, HowardLeeTW, Otter Vibe, THUNDER THUNDER). The zone medians of
PC1 differ only because the zones contain different numbers of leaders: a silver team is
not "between" gold and bronze, it is on the public point like most of gold.
"""
    return text


# ---------------------------------------------------------------- 9b. beating the plateau


def section_versus_line(d: dict) -> str:
    feats = d["feats"]
    line = feats.field_h136.value_counts().index[0]
    feats = feats.assign(on_line=feats.field_h136 == line)
    opp_cols = ["episode_id", "seat", "on_line"] + [c for c in feats.columns if c.startswith(("price_", "sold_", "revenue_"))]
    opp = feats[opp_cols].copy()
    opp["seat"] = 1 - opp.seat
    opp = opp.rename(columns={c: f"opp_{c}" for c in opp.columns if c not in ("episode_id", "seat")})
    cur = d["cur"].merge(opp, on=["episode_id", "seat"], how="left")
    line_seats = feats[feats.on_line].merge(opp[["episode_id", "seat", "opp_on_line"]], on=["episode_id", "seat"], how="left")
    ref_all = line_seats.final_money.median()
    ref_mirror = line_seats[line_seats.opp_on_line == True].final_money.median()  # noqa: E712
    ref_other = line_seats[line_seats.opp_on_line != True].final_money.median()  # noqa: E712
    rows = []
    for team in team_order(d, cur.team.unique()):
        g = cur[cur.team == team]
        v = g[g.opp_on_line == True]  # noqa: E712
        if len(v) < 8 or (g["rank"].iloc[0] > 15 and team not in ("Catalyst", "Thomas Tschinkel", "Kilupy", "Cyrus", "Toru59er")):
            continue
        rows.append(
            {
                "rank": int(g["rank"].iloc[0]),
                "team": team,
                "games vs the line": len(v),
                "win %": round(100 * v.won.mean()),
                "median margin": (v.final_money - v.opp_final_money).median(),
                "own bank vs the line": v.final_money.median(),
                "own bank, all games": g.final_money.median(),
                "line opponent's bank": v.opp_final_money.median(),
                "line's bank vs others": ref_other,
            }
        )
    bank_tbl = pd.DataFrame(rows)
    price_text = ""
    if "opp_price_strawberry" in cur:
        prows = []
        base = {"strawberry": 120, "melon": 250, "milk": 160, "wool": 200, "wheat": 25, "carrot": 35, "tomato": 60, "egg": 50}
        ref = line_seats[line_seats.opp_on_line != True]  # noqa: E712
        for team in team_order(d, cur.team.unique()):
            g = cur[cur.team == team]
            v = g[g.opp_on_line == True]  # noqa: E712
            if len(v) < 8 or g["rank"].iloc[0] > 15:
                continue
            r = {"rank": int(g["rank"].iloc[0]), "team": team, "n": len(v)}
            for p in ("strawberry", "melon", "milk", "wool", "wheat", "carrot", "tomato", "egg"):
                r[f"opp {p} $ / ref"] = f"{v[f'opp_price_{p}'].median():.0f} / {ref[f'price_{p}'].median():.0f}"
            r["opp premium revenue / ref"] = f"{v.opp_revenue_premium.median() / 1000:.0f}k / {ref.revenue_premium.median() / 1000:.0f}k"
            r["own premium revenue"] = f"{v.revenue_premium.median() / 1000:.0f}k"
            r["own staple revenue"] = f"{v.revenue_staple.median() / 1000:.0f}k"
            prows.append(r)
        price_text = f"""
What the line's opponent receives per unit when it plays each leader, against what a seat on
the line receives against non-family opponents ("ref"), corrected sales:

{md_table(pd.DataFrame(prows))}
"""
    text = f"""## 9b. Two ways to beat the plateau: out-earn it, or starve it

A seat on the current public line banks a median {ref_all / 1000:.1f}k over all sampled games
({ref_other / 1000:.1f}k against opponents off the line, {ref_mirror / 1000:.1f}k in mirror matches). Each leader's
games against opponents on that line, current submissions:

{md_table(bank_tbl)}

Majkel1337, THIRD FARM CLUB, Unknown Mother-Goose, feel the agi and HowardLeeTW **out-earn**
the line: the opponent keeps roughly its usual bank and they finish 108-115k. Artem The
Farmer, ymg_aq and Mengfei Li **starve** it: their own banks are ordinary (95-98k) and the
opponent's falls to 82-88k. The memo's "the #1 wins on the market" was half right in the
wrong way: the top of the ladder is a market-denial contest, and Artem is #1 (19-11 over
Majkel1337) because denial also hurts the out-earners, whose banks rest on premium prices.
Section 7 names the two mechanisms: metering premium sales at the town's drain rate in small
orders across the day (out-earn), and selling first each day from the previous day's
harvest, every product, every day to the end, with staples covering the late income
(starve).
{price_text}"""
    return text


# ---------------------------------------------------------------- 10. gaps


def section_gaps(d: dict) -> str:
    sample = d["sample"]
    have = sample.groupby("team_name").window.apply(lambda w: sorted(set(w)))
    only_c0 = [t for t, w in have.items() if w == ["C0"]]
    text = f"""## 10. What the data cannot answer, and what it would cost

- **History for the zone teams.** {len(only_c0)} of the 63 teams have only their current submission's
  first 50 games (C0); the per-window trajectories in section 5 exist for the 29 teams of the
  first two batches only. Every "how did silver and bronze get here" statement rests on the
  generations table (section 4), which dates lines by the sampled seats of *both* players and
  therefore does see those teams' earlier submissions as opponents, but not their own first
  games. Fetching F for the 34 zone teams is 1,700 replays, about 14 hours at the quota's
  pace (`fetch.py --windows F`).
- **The last 50 games of the zone teams (L).** Also missing for the same 34 teams; C0 games are
  entry-phase games against weaker opponents, so their win rates and opponent ratings are
  not comparable with the top-14's L windows. 1,700 replays, 14 hours.
- **Ladder-wide shares of the public generations.** The sample over-weights the studied
  teams; the community hash index (`data/community/stream_hashes.csv`, full-stream hashes
  through 2026-09-14) cannot date the family's field lines because its hash includes market
  orders, which vary. A daily sample of 100 random public games from the episode listing
  would give unbiased shares; the listing endpoint is not replay-rationed but the replays
  are (100 a day, about an hour a day).
- **Prices the agents saw when they decided to sell.** The traces carry the price before each
  turn and the revenue per sale; a per-turn price series for every game would need the
  replays again (kept on disk, no quota) and about an hour of extraction.
- **Whether the leaders' extra carrots and tomatoes pay.** Section 7 shows the conditional
  revenue, not the counterfactual. That is an arena question (plant the family's 31 carrots
  vs 60 when a Pet Cafe unlocks, same seeds), not a data question.
"""
    return text


# ---------------------------------------------------------------- 11. what to clone


def section_recommendation(d: dict) -> str:
    return """## 11. What to clone, what to hybridise, and how to judge it

Layer by layer, which studied version is best and whether they combine:

- **Economy (clone the public line, then Artem's variant of it).** The current public line
  (33 strawberry, 163 wheat, 12 melon, 31 carrot, 8 cows, 6 sheep, 3 geese, land on days 6
  and 11, 12 hands) banks 99-101k against ordinary opponents and is what four fifths of the
  medal plateau runs; matching it is the floor. Artem The Farmer's skeleton differs in the
  second land purchase (day 8, three days earlier), fewer strawberries (24-29), more carrots
  and tomatoes, and 13 hands, and is the only leader line that other teams have copied
  (section 4). The two farms are compatible: same quadrants, same herd order, same melon
  cash-in on day 10-11.
- **Opening (clone the family's or the 2c3s list; no opponent read).** Both day-1 lists
  spend the $3,000 to the last dollar on animals, pastures, melon and wheat and hire 4-5
  hands. Nothing on day 1 depends on the opponent (section 1), so the opening is a fixed
  list with a budget loop for the last wheat seeds.
- **Shop response (clone the leaders' breadth).** Every zone follows the Yarn Store; the
  leaders also follow milk shops (cows and tomatoes), egg shops (geese) and carrot shops
  (carrots) and they follow them further (section 3). This is a table of per-shop
  increments applied when a shop unlocks on days 3, 6 and 9, not a strategy switch, and it
  is the one reactive layer with evidence behind it. The increments are read off the
  conditional means in section 3.
- **Labour (clone the leaders' end game, keep the family's mid game).** Ops per unit of work
  are identical across the zones (section 8) except fertilizer, where the leaders spend 30%
  more per crop tile-day. The leaders' CARE and FEED taper from day 27 and their herds are
  allowed to escape once no yield can be sold: do that, and fertilize more.
- **Market (hybridise Artem's denial with Majkel1337's metering).** Two things beat the
  public line (section 9b): out-earning it (Majkel1337, THIRD FARM CLUB, Unknown
  Mother-Goose finish 108-115k while the opponent keeps its usual 98-108k) and starving it
  (Artem, ymg_aq, Mengfei Li bank an ordinary 95-98k while the opponent falls to 82-88k).
  Artem is #1 and 19-11 over Majkel1337 because denial also works on the out-earners. The
  concrete rules (section 7): sell premium goods first thing each day from the previous
  day's harvest; meter each product at about the town's drain rate (strawberry 7 a day
  before day 18 and 22-36 after, milk 14, wool 12, split with the opponent) in small orders
  across the day, holding the rest in the shed; never let a premium price recover once the
  opponent's bulk sales start (days 20-24 for the current line); dump melon on day 10 with
  everyone else, since no shop buys it and timing earns nothing; and let staples (tomatoes,
  carrots, eggs, and wheat, whose glut curve is flat) carry the last ten days. Whether
  metering and denial combine against a line that also adapts is an arena question.
- **Noise (skip).** SpaTaro's unexecutable orders protect it from cloning and cost nothing,
  but they are not why it wins and it is 5th, not 1st.

**The yardstick.** Everything above is measured against the current public line; the line
changes every seven to ten days (section 4), so the local gate should be paired-seat games on
fixed seeds against (a) the current public line's recorded games (`export_tapes.py` on the
family's C0 windows, both seats), (b) Artem's and Majkel1337's recordings, and (c) whatever
line is public two weeks from now, re-exported then. Win rate is the score; the median margin
over the line (7k for the top-14, 4k for gold, 2k for silver) is the diagnostic.
"""


# ---------------------------------------------------------------- assemble


def main() -> None:
    d = load()
    FIGS.mkdir(parents=True, exist_ok=True)
    parts = [
        "# Analysis: what the zone study says once the mechanisms are read\n",
        "Built by `scripts/top10/deep.py` on the rebuilt traces (trace version 2, see P18). Groups and "
        "zones as in `groups.md` (snapshot 2026-09-15T1342Z). Sections 1-6 read mechanisms behind the "
        "study's statistics; sections 7-10 use the corrected sales data.\n",
        section_openings(d),
        section_weeds(d),
        section_shops(d),
        section_generations(d),
        section_trajectories(d),
        section_h2h(d),
        section_market(d),
        section_labour(d),
        section_pca(d),
        section_versus_line(d),
        section_gaps(d),
        section_recommendation(d),
    ]
    (REPORTS / "analysis.md").write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {REPORTS / 'analysis.md'}")


if __name__ == "__main__":
    main()
