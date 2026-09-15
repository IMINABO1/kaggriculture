"""Build the top-10 report from the crawled history, the sample, and the extracted features.

    uv run python scripts/top10/analyze.py

Writes reports/top10/summary.md, one dossier per team, and figures. Every number in the
report is computed here from data/top10/*; nothing is typed in by hand.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter

import numpy as np
import pandas as pd

from research.narrate import day_table
from research.paths import REPORTS, TOP10
from research.report import SERIES, WINDOW_ORDER, bar_figure, line_figure, md_table
from research.stats import mann_whitney
from research.store import load_trace

CUTS = ["h24", "h48", "h100", "h136", "h200", "h300", "h400", "h719"]
PREMIUM = ["melon", "strawberry", "milk", "wool"]
PLAN_COLS = {
    "peak_hands": "hands (peak)",
    "quadrants_final": "quadrants",
    "land_day_1": "land day 1",
    "land_day_2": "land day 2",
    "bought_cow": "cows bought",
    "bought_sheep": "sheep bought",
    "bought_goose": "geese bought",
    "first_cow_day": "first cow day",
    "plants_wheat": "wheat planted",
    "plants_carrot": "carrot planted",
    "plants_tomato": "tomato planted",
    "plants_strawberry": "strawberry planted",
    "plants_melon": "melon planted",
    "op_fertilize": "FERTILIZE ops",
    "op_care": "CARE ops",
    "sold_melon": "melon sold",
    "sold_strawberry": "strawberry sold",
    "sold_milk": "milk sold",
    "sold_wool": "wool sold",
    "sold_wheat": "wheat sold",
    "sold_fertilizer": "fertilizer sold",
    "sells_last_3_days": "units sold last 3 days",
    "shed_peak": "shed peak",
    "weeds_spawned": "weeds spawned",
    "invalid_orders": "unexecutable market orders",
}
GROUP_NAMES = {"top": "top-14", "gold": "gold", "silver": "silver", "bronze": "bronze"}
MIN_PROFILE_GAMES = 10
GROUP_COLORS = {"top": SERIES[0], "gold": SERIES[1], "silver": SERIES[2], "bronze": SERIES[3]}
KAGGLE_GOLD_RANK = 28
RATING_MARKS = (1, 10, 25, 50, 100, 200)
PROFILE_LABELS = {
    **PLAN_COLS,
    "final_money": "final money",
    "op_dig": "DIG ops",
    "weed_days": "weed tile-days",
    "weed_peak": "weed tiles standing (peak)",
    "sold_units_total": "units sold total",
    "sell_first_day_melon": "melon first sell day",
    "sell_last_day_melon": "melon last sell day",
    "sell_first_day_strawberry": "strawberry first sell day",
    "sell_first_day_milk": "milk first sell day",
    "sell_first_day_wool": "wool first sell day",
}
PROFILE_MEDIANS = [
    "final_money",
    "peak_hands",
    "quadrants_final",
    "land_day_1",
    "land_day_2",
    "bought_cow",
    "bought_sheep",
    "bought_goose",
    "plants_strawberry",
    "plants_wheat",
    "plants_melon",
    "op_care",
    "op_fertilize",
    "op_dig",
    "sold_melon",
    "sold_strawberry",
    "sold_milk",
    "sold_wool",
    "sold_units_total",
    "sells_last_3_days",
    "sell_first_day_melon",
    "sell_last_day_melon",
    "sell_first_day_strawberry",
    "sell_first_day_milk",
    "sell_first_day_wool",
    "weeds_spawned",
    "weed_days",
    "weed_peak",
    "invalid_orders",
]
COMPARE_SECTIONS = [
    ("Outcome", ["win %", "opp rating", "final money"]),
    ("Determinism", ["field branch turn", "plan branch turn", "distinct % at 400"]),
    (
        "Farm plan",
        [
            PLAN_COLS[c]
            for c in (
                "peak_hands",
                "quadrants_final",
                "land_day_1",
                "land_day_2",
                "bought_cow",
                "bought_sheep",
                "bought_goose",
                "plants_strawberry",
                "plants_wheat",
                "plants_melon",
                "op_care",
                "op_fertilize",
            )
        ],
    ),
    (
        "Market",
        [
            PLAN_COLS[c]
            for c in (
                "sold_melon",
                "sold_strawberry",
                "sold_milk",
                "sold_wool",
                "sells_last_3_days",
            )
        ]
        + [
            "units sold total",
            "melon first sell day",
            "melon last sell day",
            "strawberry first sell day",
            "milk first sell day",
            "wool first sell day",
        ],
    ),
    (
        "Weeds and repair",
        [
            "weeds spawned",
            "weed tile-days",
            "weed tiles standing (peak)",
            "DIG ops",
            "weed tile-days per weed",
        ],
    ),
    ("Noise", ["unexecutable market orders"]),
    ("Rating path", [f"rating after game {k}" for k in RATING_MARKS] + ["games to 2900"]),
]
DIFF_COLS = [
    "bought_cow",
    "bought_sheep",
    "bought_goose",
    "peak_hands",
    "quadrants_final",
    "land_day_1",
    "sold_melon",
    "sold_strawberry",
    "sold_milk",
    "sold_wool",
    "sells_last_3_days",
    "plants_strawberry",
    "plants_wheat",
    "weeds_spawned",
    "op_care",
    "op_fertilize",
]


def line_label(i: int) -> str:
    """A, B, ..., Z, AA, AB, ... for the i-th most common line."""
    label = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        label = chr(65 + r) + label
    return label


def slug(name: str, team_id=None) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-")
    return s or (f"team-{int(team_id)}" if team_id is not None else "team")


def display(name: str, team_id=None) -> str:
    """Figure-safe team name: the bundled font has no emoji or CJK glyphs."""
    s = re.sub(r"[^\x20-\x7e -ɏ]", "", str(name)).strip()
    return s or (f"team {int(team_id)}" if team_id is not None else "team")


def load() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    teams = pd.read_csv(TOP10 / "teams.csv").sort_values("rank")
    if "group" not in teams:
        teams["group"] = "top"
    snap = pd.read_csv(TOP10 / "snapshot_latest.csv")
    zone = snap.set_index("team_id").get("zone")
    teams["zone"] = teams.team_id.map(zone) if zone is not None else ""
    first = TOP10 / "snapshot_2026-09-15T0033Z.csv"
    teams["first_rank"] = (
        teams.team_id.map(pd.read_csv(first).set_index("team_id")["rank"])
        if first.exists()
        else np.nan
    )
    stamp = str(teams.iloc[0].get("snapshot", ""))
    bounds_file = TOP10 / f"zones_{stamp}.json"
    if bounds_file.exists():
        b = json.loads(bounds_file.read_text(encoding="utf-8"))
        teams["zone_bounds"] = (
            f"{b['teams']} teams; gold to rank {b['gold']}, silver to {b['silver']}, "
            f"bronze to {b['bronze']}"
        )
    else:
        teams["zone_bounds"] = ""
    hist = pd.read_parquet(TOP10 / "history.parquet")
    sample = pd.read_csv(TOP10 / "sample.csv")
    feats = pd.read_parquet(TOP10 / "features.parquet")
    return teams, hist, sample, feats


def team_windows(sample: pd.DataFrame, feats: pd.DataFrame, team_id: int) -> pd.DataFrame:
    """One row per (window, episode) for a team, with its own and its opponent's features."""
    s = sample[sample.team_id == team_id][["window", "position", "history_len", "episode_id"]]
    mine = feats[(feats.team_id == team_id)]
    rows = s.merge(mine, on="episode_id", how="inner")
    opp = feats.add_prefix("o_")
    rows = rows.merge(opp, left_on=["episode_id"], right_on=["o_episode_id"], how="left")
    rows = rows[rows.o_seat == 1 - rows.seat].copy()
    if "ALL" in set(rows.window):
        n = int(rows.history_len.max())
        first = rows[(rows.window == "ALL") & (rows.position < 50)].assign(window="ALL:first50")
        last = rows[(rows.window == "ALL") & (rows.position >= n - 50)].assign(window="ALL:last50")
        rows = pd.concat([rows, first, last], ignore_index=True)
    return rows


def window_sort_key(w: str) -> int:
    base = w.split(":")[0]
    order = {k: i for i, k in enumerate(WINDOW_ORDER)}
    return order.get(base, 99) * 10 + (
        1 if w.endswith("first50") else 2 if w.endswith("last50") else 0
    )


def ladder_table(rows: pd.DataFrame) -> pd.DataFrame:
    out = []
    for w, g in rows.groupby("window"):
        res = g.result.fillna("?")
        out.append(
            {
                "window": w,
                "games": len(g),
                "W-L-T": f"{(res == 'W').sum()}-{(res == 'L').sum()}-{(res == 'T').sum()}",
                "win %": 100 * (res == "W").mean(),
                "median bank": g.final_money.median(),
                "mean bank": g.final_money.mean(),
                "opp rating (mean)": g.opp_rating_before.mean(),
                "seat 0 %": 100 * (g.seat == 0).mean(),
                "engines": ",".join(sorted(set(g.engine.dropna().astype(str)))),
                "from": str(g.create_time.min())[:10],
                "to": str(g.create_time.max())[:10],
            }
        )
    df = pd.DataFrame(out)
    return df.iloc[sorted(range(len(df)), key=lambda i: window_sort_key(df.window.iloc[i]))]


def plan_table(rows: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in PLAN_COLS if c in rows.columns]
    med = rows.groupby("window")[cols].median(numeric_only=True).rename(columns=PLAN_COLS)
    med = med.loc[sorted(med.index, key=window_sort_key)]
    return med.T.reset_index().rename(columns={"index": "median per game"})


def family_table(rows: pd.DataFrame, prefix: str) -> pd.DataFrame:
    out = []
    for w, g in rows.groupby("window"):
        rec = {"window": w, "games": len(g)}
        for cut in CUTS:
            col = f"{prefix}_{cut}"
            counts = g[col].value_counts()
            rec[cut] = f"{len(counts)} ({100 * counts.iloc[0] / len(g):.0f}%)" if len(g) else ""
        out.append(rec)
    df = pd.DataFrame(out)
    return df.iloc[sorted(range(len(df)), key=lambda i: window_sort_key(df.window.iloc[i]))]


def verdict(rows: pd.DataFrame, prefix: str) -> str:
    """Where a submission's games stop sharing one line, from the largest-family share per cut."""
    if len(rows) < 5:
        return "too few games"
    n = len(rows)
    share = {cut: rows[f"{prefix}_{cut}"].value_counts().iloc[0] / n for cut in CUTS}
    distinct = {cut: rows[f"{prefix}_{cut}"].nunique() for cut in CUTS}
    fixed_until = None
    for cut in CUTS:
        if share[cut] >= 0.9:
            fixed_until = cut
        else:
            break
    all_distinct = next((cut for cut in CUTS if distinct[cut] == n), None)
    turn = lambda c: int(c[1:])
    if fixed_until == "h719":
        return f"fixed plan: {share['h719']:.0%} of games identical to the last turn"
    if fixed_until is not None and turn(fixed_until) >= 400:
        return (
            f"fixed plan through turn {turn(fixed_until)} ({share[fixed_until]:.0%} one line), "
            f"small end-game variation"
        )
    if fixed_until is not None:
        tail = f"; every game distinct by turn {turn(all_distinct)}" if all_distinct else ""
        return (
            f"one line through turn {turn(fixed_until)} ({share[fixed_until]:.0%}), then branching "
            f"({distinct['h136']} lines at turn 136, {distinct['h400']} at turn 400){tail}"
        )
    tail = f"; every game distinct by turn {turn(all_distinct)}" if all_distinct else ""
    return (
        f"reactive from day 1: {distinct['h24']} openings at turn 24 (largest {share['h24']:.0%}), "
        f"{distinct['h100']} lines at turn 100{tail}"
    )


def shared_cut_table(rows: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """How many games still sit on the modal line at each cut (the modal line per cut)."""
    n = len(rows)
    recs = []
    for cut in CUTS:
        counts = rows[f"{prefix}_{cut}"].value_counts()
        recs.append(
            {
                "turn": int(cut[1:]),
                "day": int(cut[1:]) // 24,
                "distinct lines": len(counts),
                "on modal line": int(counts.iloc[0]),
                "share %": 100 * counts.iloc[0] / n,
            }
        )
    return pd.DataFrame(recs)


def first_branch_cut(rows: pd.DataFrame, prefix: str) -> str | None:
    """The first cut where fewer than 90% of games share one line."""
    for cut in CUTS:
        if rows[f"{prefix}_{cut}"].value_counts().iloc[0] / len(rows) < 0.9:
            return cut
    return None


def divergence_drivers(rows: pd.DataFrame, cut: str) -> pd.DataFrame:
    """At the first branching cut, what goes with being off the modal line: weeds, opponent, seat?"""
    if len(rows) < 10:
        return pd.DataFrame()
    day = int(cut[1:]) // 24
    modal = rows[f"field_{cut}"].value_counts().index[0]
    off = rows[f"field_{cut}"] != modal
    prev = CUTS[max(CUTS.index(cut) - 1, 0)]
    opp_modal = rows[f"o_field_{prev}"].value_counts().index[0]
    weeds_before = rows.weeds_by_day.apply(lambda w: sum(list(w)[: max(day, 1)]))
    checks = {
        f"weeds on own farm before day {max(day, 1)}": weeds_before > 0,
        f"opponent off its modal line at turn {int(prev[1:])}": rows[f"o_field_{prev}"]
        != opp_modal,
        "played seat 1": rows.seat == 1,
        "lost the game": rows.result == "L",
    }
    if day >= 4:
        first_shop = rows.shops.fillna("").str.split("|").str[0]
        modal_shop = first_shop.value_counts().index[0]
        checks[f"first shop (day 3) is not {modal_shop.title().replace('_', ' ')}"] = (
            first_shop != modal_shop
        )
    out = []
    for name, cond in checks.items():
        a, b = (
            off[cond].mean() if cond.any() else np.nan,
            off[~cond].mean() if (~cond).any() else np.nan,
        )
        out.append(
            {
                "condition": name,
                "games with condition": int(cond.sum()),
                "off-line % (condition)": 100 * a,
                "off-line % (without)": 100 * b,
            }
        )
    return pd.DataFrame(out)


def losses_table(rows: pd.DataFrame, windows: list[str]) -> tuple[pd.DataFrame, list[str]]:
    g = rows[(rows.window.isin(windows)) & (rows.result == "L")].drop_duplicates("episode_id")
    out, notes = [], []
    for r in g.sort_values("create_time").itertuples(index=False):
        diffs = {}
        for c in DIFF_COLS:
            mine, theirs = getattr(r, c, np.nan), getattr(r, f"o_{c}", np.nan)
            if pd.notna(mine) and pd.notna(theirs) and mine != theirs:
                diffs[PLAN_COLS.get(c, c)] = (theirs, mine)
        top = sorted(diffs.items(), key=lambda kv: -abs(kv[1][0] - kv[1][1]))[:3]
        diff_txt = "; ".join(f"{k}: they {a:.0f} vs me {b:.0f}" for k, (a, b) in top)
        out.append(
            {
                "window": r.window,
                "episode": int(r.episode_id),
                "opponent": r.o_team,
                "opp rating": r.opp_rating_before,
                "my bank": r.final_money,
                "opp bank": r.o_final_money,
                "margin": r.final_money - r.o_final_money,
                "opp opening": str(r.o_field_h24)[:8],
                "biggest differences (opponent vs me)": diff_txt,
            }
        )
    return pd.DataFrame(out), notes


def evolution_table(rows: pd.DataFrame) -> pd.DataFrame:
    recs = []
    for w, g in rows.groupby("window"):
        res = g.result.fillna("?")
        recs.append(
            {
                "window": w,
                "games": len(g),
                "win %": 100 * (res == "W").mean(),
                "median bank": g.final_money.median(),
                "hands": g.peak_hands.median(),
                "cows": g.bought_cow.median(),
                "sheep": g.bought_sheep.median(),
                "geese": g.bought_goose.median(),
                "quadrants": g.quadrants_final.median(),
                "land day 1": g.land_day_1.median(),
                "strawberry": g.plants_strawberry.median(),
                "wheat": g.plants_wheat.median(),
                "melon": g.plants_melon.median(),
                "melon sold": g.sold_melon.median(),
                "milk sold": g.sold_milk.median(),
                "wool sold": g.sold_wool.median(),
                "field lines @400": g.field_h400.nunique(),
                "market lines @400": g.market_h400.nunique(),
            }
        )
    df = pd.DataFrame(recs)
    return df.iloc[sorted(range(len(df)), key=lambda i: window_sort_key(df.window.iloc[i]))]


def money_curves(rows: pd.DataFrame) -> dict[str, list[float]]:
    curves = {}
    for w in sorted(rows.window.unique(), key=window_sort_key):
        if w.startswith("ALL:"):
            continue
        arr = np.array(
            [list(m) + [np.nan] * (30 - len(m)) for m in rows[rows.window == w].money_by_day]
        )
        curves[w] = list(np.nanmedian(arr, axis=0))
    return curves


def rating_path(hist: pd.DataFrame, sub: int) -> pd.Series:
    h = hist[(hist["sub"] == sub) & (hist.type == "EPISODE_TYPE_PUBLIC")].sort_values(
        ["create_time", "episode_id"]
    )
    return h.rating_after.reset_index(drop=True)


def team_dossier(t, hist, sample, feats, all_team_ids) -> str:
    rows = team_windows(sample, feats, int(t.team_id))
    name, sl = t.team_name, slug(t.team_name, t.team_id)
    shown = display(name, t.team_id)
    title = f"# {name} (rank {int(t['rank'])}, score {t.score:.1f}, {GROUP_NAMES.get(t.group, t.group)})"
    md = [title, ""]
    current = int(t.current_sub) if pd.notna(t.current_sub) else "unknown"
    md += [
        (
            f"- team id {int(t.team_id)}; current submission {current}"
            f" ({int(t.current_sub_games)} public games)"
        ),
        (
            f"- {int(t.subs_found)} submissions found; {int(t.public_games)} public games from "
            f"{str(t.first_game)[:10]} to {str(t.last_game)[:10]}; "
            f"{int(t.games_with_rating)} of them with a known rating"
        ),
        f"- sampled games with a replay: {rows.episode_id.nunique()}",
        "",
    ]
    if rows.empty:
        md.append("_No replays extracted yet for this team._")
        return "\n".join(md)

    md += ["## Ladder record by window", "", md_table(ladder_table(rows)), ""]

    path = (
        rating_path(hist, int(t.current_sub)) if pd.notna(t.current_sub) else pd.Series(dtype=float)
    )
    if len(path):
        marks = {
            k: path.iloc[min(k, len(path)) - 1] for k in (1, 10, 25, 50, 100, 200) if k <= len(path)
        }
        marks["last"] = path.iloc[-1]
        md += [
            "## Rating path of the current submission",
            "",
            ", ".join(f"game {k}: {v:.0f}" for k, v in marks.items()),
            "",
        ]
        line_figure(
            {"rating after game": list(path)},
            f"{shown}: rating of the current submission",
            "game",
            "rating",
            REPORTS / "figs" / f"{sl}_rating.png",
        )
        md += [f"![rating]({'figs/' + sl + '_rating.png'})", ""]

    md += ["## Farm plan by window (median per game)", "", md_table(plan_table(rows)), ""]
    curves = money_curves(rows)
    if curves:
        line_figure(
            curves,
            f"{shown}: median money by day, per window",
            "day",
            "coins",
            REPORTS / "figs" / f"{sl}_money.png",
            colors=SERIES,
        )
        md += [f"![money by day](figs/{sl}_money.png)", ""]

    latest = rows[rows.window.isin(("L", "ALL:last50"))].drop_duplicates("episode_id")
    if len(latest):
        order = (latest.final_money - latest.final_money.median()).abs().sort_values()
        pick = latest.loc[order.index[0]]
        trace = load_trace(int(pick.episode_id))
        md += [
            "## A typical recent game, day by day",
            "",
            (
                f"Episode {int(pick.episode_id)} (the median-bank game of the latest window): seat "
                f"{int(pick.seat)}, bank {pick.final_money:.0f} vs {pick.o_final_money:.0f} "
                f"({pick.o_team}), seed {trace['seed']}. Letters: W wheat, C carrot, T tomato, "
                f"S strawberry, M melon, E egg, Mk milk, Wl wool, F fertilizer."
            ),
            "",
            md_table(day_table(trace, int(pick.seat))),
            "",
        ]

    md += [
        "## Determinism",
        "",
        "Distinct action lines per window at each turn cut, with the share of the largest line in brackets.",
        "",
        "**Field actions (farmer + hands)**",
        "",
        md_table(family_table(rows, "field")),
        "",
        "**Market orders**",
        "",
        md_table(family_table(rows, "market")),
        "",
        (
            "**Plans (order-insensitive)**: same multiset of non-movement unit ops and market "
            "orders through the cut, regardless of path or hand order."
        ),
        "",
        md_table(family_table(rows, "plan")),
        "",
    ]
    cur = rows[rows.is_current_sub == True].drop_duplicates("episode_id")
    if len(cur):
        md += [
            (
                f"Current submission ({len(cur)} sampled games): field is "
                f"**{verdict(cur, 'field')}**; market is **{verdict(cur, 'market')}**; "
                f"plan is **{verdict(cur, 'plan')}**."
            ),
            "",
            "Games on the modal field line, by cut (current submission):",
            "",
            md_table(shared_cut_table(cur, "field")),
            "",
        ]
        branch = first_branch_cut(cur, "field")
        drv = divergence_drivers(cur, branch) if branch else pd.DataFrame()
        if len(drv):
            md += [
                (
                    f"What goes with being off the modal field line at turn {int(branch[1:])} "
                    f"(the first cut where fewer than 90% of games share one line):"
                ),
                "",
                md_table(drv),
                "",
            ]

    md += ["## Evolution across windows", "", md_table(evolution_table(rows)), ""]

    loss_windows = [
        w for w in rows.window.unique() if w in ("F", "L", "C0", "ALL:first50", "ALL:last50")
    ]
    losses, _ = losses_table(rows, loss_windows)
    md += ["## Losses in the first and last windows", ""]
    md += [
        md_table(losses) if len(losses) else "_No losses in the sampled first/last windows._",
        "",
    ]

    h2h = hist[(hist.team_id == t.team_id) & (hist.opp_team_id.isin(all_team_ids))]
    if len(h2h):
        rec = h2h.groupby("opp_team_id").result.value_counts().unstack(fill_value=0)
        for c in ("W", "L", "T"):
            if c not in rec:
                rec[c] = 0
        rec = rec[["W", "L", "T"]].reset_index()
        md += [
            "## Head to head with the other studied teams (all games, not only sampled)",
            "",
            md_table(rec),
            "",
        ]

    md += ["## Episodes behind each window", ""]
    for w in sorted(rows.window.unique(), key=window_sort_key):
        if w.startswith("ALL:"):
            continue
        ids = (
            rows[rows.window == w]
            .drop_duplicates("episode_id")
            .sort_values("position")
            .episode_id.astype(int)
            .tolist()
        )
        md.append(f"- **{w}** ({len(ids)}): " + ", ".join(map(str, ids)))
    return "\n".join(md) + "\n"


def cross_team(teams, hist, sample, feats) -> tuple[str, str]:
    counts = ", ".join(
        f"{int((teams.group == g).sum())} {GROUP_NAMES[g]}"
        for g in GROUP_ORDER
        if (teams.group == g).any()
    )
    md = [
        "# Top-10 study: summary",
        "",
        (
            f"Snapshot: {teams.iloc[0].get('snapshot', '')}. Teams studied: {len(teams)} "
            f"({counts}). Current-submission tables below use "
            f"{PROFILE_SETS[profile_set]}."
        ),
        "",
    ]
    cov = teams[
        [
            "rank",
            "team_name",
            "zone",
            "group",
            "score",
            "current_sub",
            "current_sub_games",
            "subs_found",
            "public_games",
            "games_with_rating",
            "first_game",
            "last_game",
        ]
    ].copy()
    cov["first_game"] = cov.first_game.astype(str).str[:10]
    cov["last_game"] = cov.last_game.astype(str).str[:10]
    cov["group"] = cov.group.map(GROUP_NAMES)
    md += ["## Coverage", "", md_table(cov), ""]

    latest = current_games(teams, sample, feats)
    group_section, groups_md = group_comparison(teams, hist, feats, latest)
    md += [group_section]
    ids_by_name = {}
    fam_rows = []
    verdicts = []
    for _, t in teams.iterrows():
        cur = latest[t.team_name]
        ids_by_name[t.team_name] = int(t.team_id)
        if len(cur):
            verdicts.append(
                {
                    "rank": int(t["rank"]),
                    "team": t.team_name,
                    "group": GROUP_NAMES[t.group],
                    "games": len(cur),
                    "field": verdict(cur, "field"),
                    "market": verdict(cur, "market"),
                    "plan": verdict(cur, "plan"),
                }
            )
            rec = {"rank": int(t["rank"]), "team": t.team_name, "group": GROUP_NAMES[t.group]}
            for cut in ("h24", "h100", "h200", "h400", "h719"):
                rec[cut] = cur[f"field_{cut}"].value_counts().index[0]
            fam_rows.append(rec)
    md += [
        "## Determinism verdicts (current submissions)",
        "",
        md_table(pd.DataFrame(verdicts)),
        "",
    ]

    if fam_rows:
        fam = pd.DataFrame(fam_rows)
        for cut in ("h24", "h100", "h200", "h400", "h719"):
            ids = {h: line_label(i) for i, h in enumerate(fam[cut].value_counts().index)}
            fam[cut] = fam[cut].map(ids)
        md += [
            "## Shared field lines among the current submissions",
            "",
            (
                "Letters name the modal field-action line of each team at each turn cut; two teams "
                "with the same letter at a cut submitted identical farmer and hand actions through "
                "that turn."
            ),
            "",
            md_table(fam),
            "",
        ]

    plan_cols = [
        "peak_hands",
        "quadrants_final",
        "land_day_1",
        "land_day_2",
        "bought_cow",
        "bought_sheep",
        "bought_goose",
        "plants_strawberry",
        "plants_wheat",
        "plants_melon",
        "op_care",
        "op_fertilize",
        "sold_melon",
        "sold_strawberry",
        "sold_milk",
        "sold_wool",
        "sells_last_3_days",
        "final_money",
    ]
    recs = []
    for _, t in teams.iterrows():
        cur = latest[t.team_name]
        if len(cur):
            rec = {
                "rank": int(t["rank"]),
                "team": t.team_name,
                "group": GROUP_NAMES[t.group],
                "games": len(cur),
                "win %": 100 * (cur.result == "W").mean(),
            }
            rec.update({PLAN_COLS.get(c, c): cur[c].median() for c in plan_cols})
            recs.append(rec)
    if recs:
        plan = pd.DataFrame(recs)
        md += ["## Farm plan of the current submissions (median per game)", "", md_table(plan), ""]
        if len(plan) > 1:
            top1 = plan.iloc[0]
            others = plan.iloc[1:]
            rest = others[others.group == GROUP_NAMES["top"]].median(numeric_only=True)
            diff = pd.DataFrame(
                {
                    "feature": rest.index,
                    f"#1 {top1.team}": [top1[c] for c in rest.index],
                    "median of the other top-14": rest.values,
                }
            )
            for grp in GROUP_ORDER[1:]:
                sub = others[others.group == GROUP_NAMES[grp]]
                if len(sub):
                    med = sub.median(numeric_only=True)
                    diff[f"median of {GROUP_NAMES[grp]}"] = [med.get(c, np.nan) for c in rest.index]
            diff = diff[diff.feature.isin([PLAN_COLS.get(c, c) for c in plan_cols] + ["win %"])]
            md += ["## What the #1 does differently", "", md_table(diff), ""]

    timing = []
    for _, t in teams.iterrows():
        cur = latest[t.team_name]
        if len(cur):
            rec = {"rank": int(t["rank"]), "team": t.team_name, "group": GROUP_NAMES[t.group]}
            for p in PREMIUM:
                rec[f"{p} first sell day"] = cur[f"sell_first_day_{p}"].median()
                rec[f"{p} last sell day"] = cur[f"sell_last_day_{p}"].median()
            rec["units sold last 3 days"] = cur.sells_last_3_days.median()
            rec["units sold total"] = cur.sold_units_total.median()
            timing.append(rec)
    if timing:
        md += [
            "## Market timing of the current submissions (median day)",
            "",
            md_table(pd.DataFrame(timing)),
            "",
        ]

    ids = set(teams.team_id.astype(int))
    h2h = hist[
        (hist.team_id.isin(ids))
        & (hist.opp_team_id.isin(ids))
        & (hist.type == "EPISODE_TYPE_PUBLIC")
    ]
    if len(h2h):
        names = dict(zip(teams.team_id.astype(int), teams.team_name))
        mat = h2h.assign(me=h2h.team_id.map(names), opp=h2h.opp_team_id.map(names))
        tbl = mat.pivot_table(
            index="me",
            columns="opp",
            values="result",
            aggfunc=lambda s: f"{(s == 'W').sum()}-{(s == 'L').sum()}",
            fill_value="",
        )
        md += [
            "## Head to head (wins-losses, row vs column, all public games in the histories)",
            "",
            md_table(tbl, index=True),
            "",
        ]

    labels = [display(v["team"], ids_by_name[v["team"]]) for v in verdicts]
    values = [
        100 * latest[v["team"]].field_h100.value_counts().iloc[0] / len(latest[v["team"]])
        for v in verdicts
    ]
    if labels:
        bar_figure(
            labels,
            values,
            "Games on the modal field line at turn 100, current submissions (%)",
            "% of games",
            REPORTS / "figs" / "families_h400.png",
        )
        md += ["![families](figs/families_h400.png)", ""]
    curves = {}
    for v in verdicts:
        cur = latest[v["team"]]
        arr = np.array([list(m) + [np.nan] * (30 - len(m)) for m in cur.money_by_day])
        curves[display(v["team"], ids_by_name[v["team"]])] = list(np.nanmedian(arr, axis=0))
    if curves:
        small_multiples(curves, REPORTS / "figs" / "money_current.png")
        md += ["![money by day, current submissions](figs/money_current.png)", ""]
    md += ["## Team dossiers", ""]
    md += [
        f"- [{t.team_name}]({slug(t.team_name, t.team_id)}.md) "
        f"({GROUP_NAMES[t.group]}, rank {int(t['rank'])})"
        for _, t in teams.iterrows()
    ]
    return "\n".join(md) + "\n", groups_md


PROFILE_SETS = {
    "current": "every sampled game of the current submission (C0 plus its games in L)",
    "C0": "the C0 window only (the current submission's first 50 games)",
}
profile_set = "current"
GROUP_ORDER = ["top", "gold", "silver", "bronze"]
PAIRS = [("top", "gold"), ("gold", "silver"), ("silver", "bronze"), ("top", "bronze")]
OVERVIEW_FEATURES = [
    "win %",
    "opp rating",
    "final money",
    "field branch turn",
    "distinct % at 400",
    "land day 2",
    "CARE ops",
    "FERTILIZE ops",
    "strawberry planted",
    "melon last sell day",
    "strawberry first sell day",
    "weed tile-days",
    "units sold last 3 days",
    "rating after game 50",
    "rating after game 100",
]


def present_groups(profile: pd.DataFrame) -> list[str]:
    return [g for g in GROUP_ORDER if (profile.group == g).sum() >= 3]


def current_games(teams, sample, feats) -> dict[str, pd.DataFrame]:
    """Team name -> its current submission's sampled games (one row per episode).

    With profile_set == "C0" only that window is kept, so every team is measured on the
    same 50 games.
    """
    out = {}
    for _, t in teams.iterrows():
        rows = team_windows(sample, feats, int(t.team_id))
        rows = rows[rows.is_current_sub == True]
        if profile_set == "C0":
            rows = rows[rows.window == "C0"]
        out[t.team_name] = rows.drop_duplicates("episode_id")
    return out


def branch_driver(rows: pd.DataFrame, cut: str | None) -> tuple[str, float]:
    """The condition with the largest off-line gap at the first branch cut, if it is 25+ points."""
    if cut is None:
        return "fixed", np.nan
    drv = divergence_drivers(rows, cut)
    if not len(drv):
        return "n/a", np.nan
    drv = drv[(drv["games with condition"] >= 3) & ~drv.condition.str.startswith("lost")]
    drv = drv.assign(gap=drv["off-line % (condition)"] - drv["off-line % (without)"])
    drv = drv.dropna(subset=["gap"])
    if not len(drv):
        return "none", np.nan
    best = drv.loc[drv.gap.abs().idxmax()]
    if abs(best.gap) < 25:
        return "none", float(best.gap)
    c = best.condition
    label = (
        "weed"
        if c.startswith("weeds")
        else "opponent"
        if c.startswith("opponent")
        else "seat"
        if c.startswith("played")
        else "shop"
        if c.startswith("first shop")
        else c
    )
    return label, float(best.gap)


def branch_class(turn: int) -> str:
    if turn >= 720:
        return "fixed"
    if turn <= 24:
        return "day 1"
    if turn <= 48:
        return "day 2"
    if turn <= 136:
        return "day 4-6"
    if turn <= 400:
        return "day 8-16"
    return "end-game only"


def team_profile(t, cur: pd.DataFrame, hist: pd.DataFrame) -> dict:
    res = cur.result.fillna("?")
    rec = {
        "rank": int(t["rank"]),
        "team": t.team_name,
        "zone": t.get("zone", ""),
        "group": t.group,
        "games": len(cur),
        "win %": 100 * (res == "W").mean(),
        "opp rating": cur.opp_rating_before.mean(),
    }
    fb, pb = first_branch_cut(cur, "field"), first_branch_cut(cur, "plan")
    rec["field branch turn"] = int(fb[1:]) if fb else 720
    rec["plan branch turn"] = int(pb[1:]) if pb else 720
    rec["distinct % at 400"] = 100 * cur.field_h400.nunique() / len(cur)
    rec["driver"], rec["driver gap"] = branch_driver(cur, fb)
    for c in PROFILE_MEDIANS:
        rec[PROFILE_LABELS.get(c, c)] = cur[c].median() if c in cur else np.nan
    weedy = cur[cur.weeds_spawned > 0] if "weed_days" in cur else cur.iloc[0:0]
    rec["weed tile-days per weed"] = (
        float((weedy.weed_days / weedy.weeds_spawned).median()) if len(weedy) else np.nan
    )
    path = (
        rating_path(hist, int(t.current_sub)) if pd.notna(t.current_sub) else pd.Series(dtype=float)
    )
    for k in RATING_MARKS:
        rec[f"rating after game {k}"] = float(path.iloc[k - 1]) if len(path) >= k else np.nan
    hit = path[path >= 2900]
    rec["games to 2900"] = int(hit.index[0]) + 1 if len(hit) else np.nan
    return rec


def _rng(series: pd.Series) -> str:
    s = series.dropna()
    if not len(s):
        return ""
    return f"{round(float(s.min()), 1):g} to {round(float(s.max()), 1):g}"


def compare_table(profile: pd.DataFrame, labels: list[str], a: str, b: str) -> pd.DataFrame:
    A, B = GROUP_NAMES[a], GROUP_NAMES[b]
    pa, pb = profile[profile.group == a], profile[profile.group == b]
    out = []
    for lab in labels:
        if lab not in profile.columns:
            continue
        auc, p = mann_whitney(pa[lab].tolist(), pb[lab].tolist())
        out.append(
            {
                "feature": lab,
                f"{A} median": pa[lab].median(),
                f"{A} range": _rng(pa[lab]),
                f"{B} median": pb[lab].median(),
                f"{B} range": _rng(pb[lab]),
                f"P({A} > {B})": auc,
                "p": p,
            }
        )
    return pd.DataFrame(out)


def _fmt(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "n/a"
    return f"{v:.0f}" if abs(v) >= 20 or float(v).is_integer() else f"{v:.1f}"


def separation_bullets(cmp: pd.DataFrame, a: str, b: str) -> tuple[list[str], list[str]]:
    A, B = GROUP_NAMES[a], GROUP_NAMES[b]
    auc_col = f"P({A} > {B})"
    c = cmp.dropna(subset=[auc_col]).copy()
    c["d"] = (c[auc_col] - 0.5).abs()
    sig = c[c.p < 0.05].sort_values("d", ascending=False)
    flat = c[(c.p >= 0.2) & (c.d <= 0.15)].sort_values("d")
    sep = [
        (
            f"**{r.feature}**: {A} median {_fmt(r[f'{A} median'])} vs {B} "
            f"{_fmt(r[f'{B} median'])}; a random {A} team is above a random {B} team "
            f"{100 * r[auc_col]:.0f}% of the time (p = {r.p:.3f})"
        )
        for _, r in sig.iterrows()
    ]
    same = [
        f"{r.feature} ({_fmt(r[f'{A} median'])} vs {_fmt(r[f'{B} median'])})"
        for _, r in flat.iterrows()
    ]
    return sep, same


def _wlt(df: pd.DataFrame, flip: bool = False) -> str:
    w, l = (df.result == "W").sum(), (df.result == "L").sum()
    if flip:
        w, l = l, w
    return f"{w}-{l}-{(df.result == 'T').sum()}"


def group_h2h(
    hist: pd.DataFrame, teams: pd.DataFrame, a: str, b: str
) -> tuple[str, pd.DataFrame, pd.DataFrame]:
    A, B = GROUP_NAMES[a], GROUP_NAMES[b]
    pub = hist[hist.type == "EPISODE_TYPE_PUBLIC"]
    a_ids = set(teams[teams.group == a].team_id.astype(int))
    b_ids = set(teams[teams.group == b].team_id.astype(int))
    g = pub[pub.team_id.isin(a_ids) & pub.opp_team_id.isin(b_ids)]
    current = set(teams.current_sub.dropna().astype(int))
    gc = g[g["sub"].isin(current) & g.opp_sub.isin(current)]
    names = dict(zip(teams.team_id.astype(int), teams.team_name))
    ranks = dict(zip(teams.team_id.astype(int), teams["rank"].astype(int)))
    overall = (
        f"All public games between {A} and {B}, seen from the {A} side: **{_wlt(g)}** "
        f"({100 * (g.result == 'W').mean():.0f}% wins over {len(g)} games); current "
        f"submissions of both sides only: **{_wlt(gc)}** ({len(gc)} games)."
        if len(g)
        else f"No public games between {A} and {B}."
    )
    per_a, per_b = [], []
    for tid in sorted(a_ids, key=lambda i: ranks[i]):
        d, dc = g[g.team_id == tid], gc[gc.team_id == tid]
        if len(d):
            per_a.append(
                {
                    "rank": ranks[tid],
                    "team": names[tid],
                    f"games vs {B}": len(d),
                    "W-L-T": _wlt(d),
                    "win %": 100 * (d.result == "W").mean(),
                    "current subs W-L-T": _wlt(dc),
                }
            )
    for tid in sorted(b_ids, key=lambda i: ranks[i]):
        d, dc = g[g.opp_team_id == tid], gc[gc.opp_team_id == tid]
        if len(d):
            per_b.append(
                {
                    "rank": ranks[tid],
                    "team": names[tid],
                    f"games vs {A}": len(d),
                    "W-L-T": _wlt(d, flip=True),
                    "win %": 100 * (d.result == "L").mean(),
                    "current subs W-L-T": _wlt(dc, flip=True),
                }
            )
    return overall, pd.DataFrame(per_a), pd.DataFrame(per_b)


def group_losses(
    teams: pd.DataFrame, latest: dict[str, pd.DataFrame], feats: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Losses of the current submissions per group, and which feature the winner differed in most.

    Differences are in pooled standard deviations so a cow and a CARE op count on the same
    footing (the dossiers' loss tables use raw differences).
    """
    scale = {c: max(float(feats[c].std()), 1.0) for c in DIFF_COLS if c in feats}
    group_of = {int(t.team_id): t.group for _, t in teams.iterrows()}
    rows = []
    for _, t in teams.iterrows():
        cur = latest.get(t.team_name)
        if cur is None or not len(cur):
            continue
        for r in cur[cur.result == "L"].itertuples(index=False):
            oid = int(r.o_team_id) if pd.notna(r.o_team_id) else None
            diffs = {}
            for c, unit in scale.items():
                mine, theirs = getattr(r, c, np.nan), getattr(r, f"o_{c}", np.nan)
                if pd.notna(mine) and pd.notna(theirs):
                    diffs[c] = (theirs - mine) / unit
            if not diffs:
                continue
            c, d = max(diffs.items(), key=lambda kv: abs(kv[1]))
            rows.append(
                {
                    "group": t.group,
                    "team": t.team_name,
                    "margin": r.final_money - r.o_final_money,
                    "opp group": GROUP_NAMES.get(group_of.get(oid), "other"),
                    "feature": PLAN_COLS.get(c, c),
                    "direction": "opponent higher" if d > 0 else "opponent lower",
                }
            )
    df = pd.DataFrame(rows)
    if not len(df):
        return pd.DataFrame(), pd.DataFrame()
    summary, top_feats = [], []
    for grp in GROUP_ORDER:
        g = df[df.group == grp]
        if not len(g):
            continue
        rec = {
            "group": GROUP_NAMES[grp],
            "losses": len(g),
            "median margin": g.margin.median(),
            "within 3k %": 100 * (g.margin > -3000).mean(),
        }
        for other in GROUP_ORDER:
            rec[f"to {GROUP_NAMES[other]} %"] = 100 * (g["opp group"] == GROUP_NAMES[other]).mean()
        rec["to others %"] = 100 * (g["opp group"] == "other").mean()
        summary.append(rec)
        counts = g.groupby(["feature", "direction"]).size().sort_values(ascending=False)
        for (feat, direction), n in counts.head(3).items():
            top_feats.append(
                {
                    "group": GROUP_NAMES[grp],
                    "biggest scaled difference in the loss": f"{feat}, {direction}",
                    "losses": int(n),
                    "share %": 100 * n / len(g),
                }
            )
    return pd.DataFrame(summary), pd.DataFrame(top_feats)


def line_families(teams: pd.DataFrame, latest: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Per cut and group: how many teams sit on a field line shared with another team."""
    modal = {}
    for _, t in teams.iterrows():
        cur = latest.get(t.team_name)
        if cur is None or len(cur) < MIN_PROFILE_GAMES:
            continue
        modal[t.team_name] = (t.group, {c: cur[f"field_{c}"].value_counts().index[0] for c in CUTS})
    groups = [g for g in GROUP_ORDER if any(v[0] == g for v in modal.values())]
    out = []
    for cut in ("h24", "h48", "h100", "h136", "h200", "h300", "h400"):
        counts = Counter(v[1][cut] for v in modal.values())
        rec = {"turn": int(cut[1:]), "day": int(cut[1:]) // 24}
        for grp in groups:
            names = [n for n, v in modal.items() if v[0] == grp]
            shared = [n for n in names if counts[modal[n][1][cut]] > 1]
            rec[f"{GROUP_NAMES[grp]} on a shared line"] = f"{len(shared)} of {len(names)}"
        rec["largest family"] = max(counts.values()) if counts else 0
        out.append(rec)
    return pd.DataFrame(out)


def count_table(profile: pd.DataFrame, column: str, classes: list[str], label: str) -> pd.DataFrame:
    groups = present_groups(profile)
    out = pd.DataFrame({label: classes})
    for grp in groups:
        out[f"{GROUP_NAMES[grp]} teams"] = [
            int(((profile.group == grp) & (profile[column] == c)).sum()) for c in classes
        ]
    return out[out.iloc[:, 1:].sum(axis=1) > 0]


def overview_table(profile: pd.DataFrame) -> pd.DataFrame:
    groups = present_groups(profile)
    out = []
    for lab in OVERVIEW_FEATURES:
        if lab not in profile.columns:
            continue
        rec = {"feature (median per team)": lab}
        for grp in groups:
            rec[GROUP_NAMES[grp]] = profile[profile.group == grp][lab].median()
        out.append(rec)
    head = {"feature (median per team)": "teams"}
    head.update({GROUP_NAMES[g]: int((profile.group == g).sum()) for g in groups})
    return pd.DataFrame([head] + out)


def group_rating_figure(paths: list[tuple[str, str, list[float]]], path) -> None:
    import warnings

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from research.report import INK_2, SURFACE, style_axes

    n = 300
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=130)
    fig.patch.set_facecolor(SURFACE)
    for _, group, vals in paths:
        v = vals[:n]
        ax.plot(range(1, len(v) + 1), v, color=GROUP_COLORS[group], alpha=0.18, linewidth=0.7)
    for group in GROUP_ORDER:
        arr = [
            list(vals[:n]) + [np.nan] * (n - len(vals[:n])) for _, g, vals in paths if g == group
        ]
        if len(arr) < 3:
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            med = np.nanmedian(np.array(arr, dtype=float), axis=0)
        ax.plot(
            range(1, n + 1),
            med,
            color=GROUP_COLORS[group],
            linewidth=2.2,
            label=f"{GROUP_NAMES[group]} median",
        )
    style_axes(ax)
    ax.set_title("Rating path of the current submissions, by group", fontsize=10, loc="left")
    ax.set_xlabel("game of the current submission", fontsize=8)
    ax.set_ylabel("rating after game", fontsize=8)
    ax.set_ylim(bottom=1500)
    ax.legend(fontsize=7, frameon=False, labelcolor=INK_2, loc="lower right")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def group_strip_figure(profile: pd.DataFrame, features: list[str], path) -> None:
    import math

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from research.report import GRID, INK, INK_2, SURFACE, style_axes

    groups = present_groups(profile)
    cols = 4
    rows_n = max(math.ceil(len(features) / cols), 1)
    fig, axes = plt.subplots(
        rows_n, cols, figsize=(11, (1.3 + 0.55 * len(groups)) * rows_n), dpi=130
    )
    fig.patch.set_facecolor(SURFACE)
    axes = np.array(axes).reshape(-1)
    rng = np.random.default_rng(0)
    for ax, feat in zip(axes, features):
        for yi, group in enumerate(reversed(groups)):
            vals = profile[profile.group == group][feat].dropna().astype(float)
            y = yi + rng.uniform(-0.18, 0.18, len(vals))
            ax.scatter(
                vals,
                y,
                s=18,
                color=GROUP_COLORS[group],
                alpha=0.85,
                edgecolor=SURFACE,
                linewidth=0.6,
                zorder=3,
            )
            if len(vals):
                ax.plot(
                    [vals.median()] * 2,
                    [yi - 0.32, yi + 0.32],
                    color=GROUP_COLORS[group],
                    linewidth=2.2,
                    zorder=2,
                )
        style_axes(ax)
        ax.yaxis.grid(False)
        ax.xaxis.grid(True, color=GRID, linewidth=0.6)
        ax.set_yticks(range(len(groups)))
        ax.set_yticklabels([GROUP_NAMES[g] for g in reversed(groups)], fontsize=7)
        ax.set_ylim(-0.7, len(groups) - 0.3)
        ax.tick_params(labelsize=6)
        ax.set_title(feat, fontsize=8, loc="left", color=INK)
    for ax in axes[len(features) :]:
        ax.axis("off")
    fig.suptitle(
        "Per-team medians of the current submissions: one dot per team, bar = group median",
        fontsize=9,
        color=INK_2,
        x=0.01,
        ha="left",
    )
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def group_comparison(teams, hist, feats, latest) -> tuple[str, str]:
    """(section for summary.md, full text of groups.md)."""
    profiles, too_few = [], []
    for _, t in teams.iterrows():
        cur = latest.get(t.team_name)
        if cur is None or len(cur) < MIN_PROFILE_GAMES:
            too_few.append(f"{t.team_name} ({0 if cur is None else len(cur)})")
            continue
        profiles.append(team_profile(t, cur, hist))
    profile = pd.DataFrame(profiles)
    groups = present_groups(profile) if len(profile) else []
    if len(groups) < 2:
        note = "_Group comparison needs replays for at least two groups; not built yet._"
        return f"## Groups\n\n{note}\n", f"# Groups\n\n{note}\n"
    pairs = [(a, b) for a, b in PAIRS if a in groups and b in groups]
    counts = ", ".join(f"{int((profile.group == g).sum())} {GROUP_NAMES[g]}" for g in groups)

    snapshot = teams.iloc[0].get("snapshot", "")
    zones = teams.iloc[0].get("zone_bounds", "")
    who = teams[
        [
            "rank",
            "first_rank",
            "team_name",
            "zone",
            "group",
            "score",
            "public_games",
            "current_sub_games",
        ]
    ].copy()
    who["group"] = who.group.map(GROUP_NAMES)
    who["sampled current-sub games"] = [len(latest.get(n, [])) for n in teams.team_name]
    who = who.rename(columns={"team_name": "team", "first_rank": "rank at first snapshot"})

    det = profile[
        [
            "rank",
            "team",
            "group",
            "games",
            "field branch turn",
            "plan branch turn",
            "distinct % at 400",
            "driver",
            "driver gap",
        ]
    ].copy()
    det["group"] = det.group.map(GROUP_NAMES)
    det["field branch"] = det["field branch turn"].map(branch_class)
    det = det.sort_values("rank")
    profile["field branch"] = profile["field branch turn"].map(branch_class)
    cls = count_table(
        profile,
        "field branch",
        ["day 1", "day 2", "day 4-6", "day 8-16", "end-game only", "fixed"],
        "first field branch",
    )
    drv = count_table(
        profile,
        "driver",
        ["opponent", "weed", "seat", "shop", "none", "fixed", "n/a"],
        "dominant driver at the first branch",
    )
    families = line_families(teams, latest)
    loss_summary, loss_feats = group_losses(teams, latest, feats)

    paths = []
    for _, t in teams.iterrows():
        if pd.isna(t.current_sub) or t.team_name not in latest or not len(latest[t.team_name]):
            continue
        paths.append((t.team_name, t.group, list(rating_path(hist, int(t.current_sub)))))
    group_rating_figure(paths, REPORTS / "figs" / "group_rating.png")

    pair_md, pair_summary, first_sep, first_same, strip_feats = [], [], [], [], []
    for a, b in pairs:
        A, B = GROUP_NAMES[a], GROUP_NAMES[b]
        parts = []
        for section, labels in COMPARE_SECTIONS:
            c = compare_table(profile, labels, a, b)
            c.insert(0, "section", section)
            parts.append(c)
        cmp = pd.concat(parts, ignore_index=True)
        sep, same = separation_bullets(cmp, a, b)
        overall, per_a, per_b = group_h2h(hist, teams, a, b)
        if not first_sep and not strip_feats:
            first_sep, first_same = sep, same
            auc_col = f"P({A} > {B})"
            ranked = cmp.dropna(subset=[auc_col]).copy()
            ranked["d"] = (ranked[auc_col] - 0.5).abs()
            ranked["weak"] = ranked.p >= 0.1
            strip_feats = (
                ranked.sort_values(["weak", "d", "p"], ascending=[True, False, True])
                .feature.head(8)
                .tolist()
            )
        pair_md += [f"## {A} vs {B}", "", "Separates them (p < 0.05):", ""]
        pair_md += [f"- {x}" for x in sep] if sep else ["- nothing at p < 0.05"]
        pair_md += ["", "Does not separate them (p >= 0.2, AUC within 0.35-0.65):", ""]
        pair_md += [f"- {x}" for x in same] if same else ["- (none)"]
        pair_md += ["", overall, ""]
        if len(per_a):
            pair_md += [f"{A} teams against {B}:", "", md_table(per_a), ""]
        if len(per_b):
            pair_md += [f"{B} teams against {A}:", "", md_table(per_b), ""]
        for section, _ in COMPARE_SECTIONS:
            part = cmp[cmp.section == section].drop(columns=["section"])
            if len(part):
                pair_md += [f"**{section}**", "", md_table(part, floatfmt=".2f"), ""]
        pair_summary.append(f"- {A} vs {B}: {overall}")
    if strip_feats:
        group_strip_figure(profile, strip_feats, REPORTS / "figs" / "group_strip.png")

    md = [
        "# Groups: top-14, the rest of gold, silver, bronze",
        "",
        (
            f"Snapshot {snapshot} of the full leaderboard ({zones}). Medal zones follow "
            f"Kaggle's rule for competitions with 1,000+ teams (gold = top 10 + 0.2% of teams, "
            f"silver = top 5%, bronze = top 10%) applied to that snapshot. Groups: the "
            f"**top-14** are the teams that were top-10 in Iminabo's screenshot or on the live "
            f"board on 2026-09-14 (two of them had slipped into silver by this snapshot and "
            f"stay in the top-14); **gold** is every other gold team the crawl could seed; "
            f"**silver** and **bronze** are rank chunks inside those zones, plus the "
            f"first-batch teams that sit there now. Teams with replays: {counts}. Every "
            f"number is a per-team median over {PROFILE_SETS[profile_set]}, compared across "
            f"teams: 'P(A > B)' is the chance that a random team of A is above a random team "
            f"of B on that feature (0.5 = no separation), 'p' the two-sided Mann-Whitney "
            f"test. Teams with fewer than {MIN_PROFILE_GAMES} sampled games are left out"
            + (f": {', '.join(too_few)}." if too_few else ".")
        ),
        "",
        "## Who is in each group",
        "",
        md_table(who),
        "",
        "## Overview",
        "",
        md_table(overview_table(profile)),
        "",
        "![rating paths by group](figs/group_rating.png)",
        "",
        "![per-team medians by group](figs/group_strip.png)",
        "",
        "## Determinism and branch point (current submissions)",
        "",
        (
            "Branch turn: the first cut at which fewer than 90% of a team's games share one "
            "line (720 = one line to the end). Driver: the condition whose presence moves the "
            "off-line rate by 25+ points at that cut (weed on own farm before that day, "
            "opponent off its own modal line at the previous cut, seat, first shop draw)."
        ),
        "",
        md_table(det),
        "",
        md_table(cls),
        "",
        md_table(drv),
        "",
        (
            "Teams whose modal field line (farmer and hand actions) is byte-identical to "
            "another studied team's through the cut, i.e. members of a shared plan family, "
            "and the size of the largest family at that cut:"
        ),
        "",
        md_table(families),
        "",
    ]
    md += pair_md
    md += ["## Losses of the current submissions", ""]
    if len(loss_summary):
        md += [
            (
                "Sampled losses per group: how close they were, who inflicted them, and which "
                "feature the winner differed in most (in pooled standard deviations of the "
                "feature)."
            ),
            "",
            md_table(loss_summary),
            "",
            md_table(loss_feats),
            "",
        ]
    else:
        md += ["_No sampled losses._", ""]
    md += [
        "## Per-team profile",
        "",
        md_table(profile.drop(columns=["driver gap", "field branch"]).sort_values("rank")),
        "",
    ]
    groups_md = "\n".join(md) + "\n"

    a, b = pairs[0]
    section = [
        "## Groups: top-14, the rest of gold, silver, bronze",
        "",
        (
            f"Teams with replays: {counts}. Per-team medians of the current submissions; "
            f"full tables, all pairwise comparisons, head-to-head, losses, and figures in "
            f"[groups.md](groups.md)."
        ),
        "",
        f"{GROUP_NAMES[a]} vs {GROUP_NAMES[b]}, separates them (p < 0.05):",
        "",
    ]
    section += [f"- {x}" for x in first_sep[:8]] if first_sep else ["- nothing at p < 0.05"]
    section += ["", "Does not separate them:", ""]
    section += [f"- {x}" for x in first_same[:8]] if first_same else ["- (none)"]
    section += ["", "Head to head:", ""] + pair_summary + [""]
    return "\n".join(section) + "\n", groups_md


def small_multiples(curves: dict[str, list[float]], path) -> None:
    import math

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from research.report import INK, INK_2, SURFACE, style_axes

    n = len(curves)
    cols = 4
    rows_n = math.ceil(n / cols)
    fig, axes = plt.subplots(rows_n, cols, figsize=(11, 2.4 * rows_n), dpi=130, sharey=True)
    fig.patch.set_facecolor(SURFACE)
    axes = np.array(axes).reshape(-1)
    for ax, (name, vals) in zip(axes, curves.items()):
        ax.plot(range(len(vals)), vals, color=SERIES[0], linewidth=1.6)
        style_axes(ax)
        ax.set_title(name, fontsize=8, loc="left", color=INK)
        ax.tick_params(labelsize=6)
    for ax in axes[n:]:
        ax.axis("off")
    fig.suptitle(
        "Median money by day, current submissions", fontsize=10, color=INK_2, x=0.01, ha="left"
    )
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def main() -> None:
    global profile_set
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--profile-window",
        default="current",
        choices=sorted(PROFILE_SETS),
        help="which games of the current submission feed the per-team profiles and verdicts",
    )
    args = ap.parse_args()
    profile_set = args.profile_window
    teams, hist, sample, feats = load()
    REPORTS.mkdir(parents=True, exist_ok=True)
    ids = set(teams.team_id.astype(int))
    for _, t in teams.iterrows():
        text = team_dossier(t, hist, sample, feats, ids)
        (REPORTS / f"{slug(t.team_name, t.team_id)}.md").write_text(text, encoding="utf-8")
        print(f"wrote {slug(t.team_name, t.team_id)}.md")
    summary_md, groups_md = cross_team(teams, hist, sample, feats)
    (REPORTS / "summary.md").write_text(summary_md, encoding="utf-8")
    (REPORTS / "groups.md").write_text(groups_md, encoding="utf-8")
    print("wrote summary.md and groups.md")
    meta = {
        "teams": len(teams),
        "groups": {g: int((teams.group == g).sum()) for g in GROUP_ORDER},
        "episodes_with_features": int(feats.episode_id.nunique()),
        "top_seats": int(feats.is_top10_seat.sum()),
        "profile_window": profile_set,
    }
    (REPORTS / "build.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(Counter(feats[feats.is_top10_seat].team_name).most_common())


if __name__ == "__main__":
    main()
