"""Build the top-10 report from the crawled history, the sample, and the extracted features.

    uv run python scripts/top10/analyze.py

Writes reports/top10/summary.md, one dossier per team, and figures. Every number in the
report is computed here from data/top10/*; nothing is typed in by hand.
"""

from __future__ import annotations

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
GROUP_NAMES = {"top": "top-14", "batch": "next-15"}
GROUP_COLORS = {"top": SERIES[0], "batch": SERIES[1]}
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
    n_top = int((teams.group == "top").sum())
    n_batch = int((teams.group == "batch").sum())
    md = [
        "# Top-10 study: summary",
        "",
        (
            f"Snapshot: {teams.iloc[0].get('snapshot', '')}. Teams studied: {len(teams)} "
            f"({n_top} top-14, {n_batch} next-15)."
        ),
        "",
    ]
    cov = teams[
        [
            "rank",
            "team_name",
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
            ids = {h: chr(65 + i) for i, h in enumerate(fam[cut].value_counts().index)}
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
            batch = others[others.group == GROUP_NAMES["batch"]].median(numeric_only=True)
            diff = pd.DataFrame(
                {
                    "feature": rest.index,
                    f"#1 {top1.team}": [top1[c] for c in rest.index],
                    "median of the other top-14": rest.values,
                    "median of the next-15": [batch.get(c, np.nan) for c in rest.index],
                }
            )
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


def current_games(teams, sample, feats) -> dict[str, pd.DataFrame]:
    """Team name -> its current submission's sampled games (one row per episode)."""
    out = {}
    for _, t in teams.iterrows():
        rows = team_windows(sample, feats, int(t.team_id))
        out[t.team_name] = rows[rows.is_current_sub == True].drop_duplicates("episode_id")
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


def compare_table(profile: pd.DataFrame, labels: list[str]) -> pd.DataFrame:
    top, batch = profile[profile.group == "top"], profile[profile.group == "batch"]
    out = []
    for lab in labels:
        if lab not in profile.columns:
            continue
        auc, p = mann_whitney(top[lab].tolist(), batch[lab].tolist())
        out.append(
            {
                "feature": lab,
                "top-14 median": top[lab].median(),
                "top-14 range": _rng(top[lab]),
                "next-15 median": batch[lab].median(),
                "next-15 range": _rng(batch[lab]),
                "P(top > next)": auc,
                "p": p,
            }
        )
    return pd.DataFrame(out)


def _fmt(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "n/a"
    return f"{v:.0f}" if abs(v) >= 20 or float(v).is_integer() else f"{v:.1f}"


def separation_bullets(cmp: pd.DataFrame) -> tuple[list[str], list[str]]:
    c = cmp.dropna(subset=["P(top > next)"]).copy()
    c["d"] = (c["P(top > next)"] - 0.5).abs()
    sig = c[c.p < 0.05].sort_values("d", ascending=False)
    flat = c[(c.p >= 0.2) & (c.d <= 0.15)].sort_values("d")
    sep = [
        (
            f"**{r.feature}**: top-14 median {_fmt(r['top-14 median'])} vs next-15 "
            f"{_fmt(r['next-15 median'])}; a random top-14 team is above a random next-15 team "
            f"{100 * r['P(top > next)']:.0f}% of the time (p = {r.p:.3f})"
        )
        for _, r in sig.iterrows()
    ]
    same = [
        f"{r.feature} ({_fmt(r['top-14 median'])} vs {_fmt(r['next-15 median'])})"
        for _, r in flat.iterrows()
    ]
    return sep, same


def _wlt(df: pd.DataFrame, flip: bool = False) -> str:
    w, l = (df.result == "W").sum(), (df.result == "L").sum()
    if flip:
        w, l = l, w
    return f"{w}-{l}-{(df.result == 'T').sum()}"


def group_h2h(hist: pd.DataFrame, teams: pd.DataFrame) -> tuple[str, pd.DataFrame, pd.DataFrame]:
    pub = hist[hist.type == "EPISODE_TYPE_PUBLIC"]
    top_ids = set(teams[teams.group == "top"].team_id.astype(int))
    batch_ids = set(teams[teams.group == "batch"].team_id.astype(int))
    g = pub[pub.team_id.isin(top_ids) & pub.opp_team_id.isin(batch_ids)]
    current = set(teams.current_sub.dropna().astype(int))
    gc = g[g["sub"].isin(current) & g.opp_sub.isin(current)]
    names = dict(zip(teams.team_id.astype(int), teams.team_name))
    ranks = dict(zip(teams.team_id.astype(int), teams["rank"].astype(int)))
    overall = (
        f"All public games between the groups, seen from the top-14 side: **{_wlt(g)}** "
        f"({100 * (g.result == 'W').mean():.0f}% wins over {len(g)} games); current "
        f"submissions of both sides only: **{_wlt(gc)}** ({len(gc)} games)."
        if len(g)
        else "No public games between the groups."
    )
    per_top, per_batch = [], []
    for tid in sorted(top_ids, key=lambda i: ranks[i]):
        d = g[g.team_id == tid]
        dc = gc[gc.team_id == tid]
        per_top.append(
            {
                "rank": ranks[tid],
                "team": names[tid],
                "games vs next-15": len(d),
                "W-L-T": _wlt(d),
                "win %": 100 * (d.result == "W").mean() if len(d) else np.nan,
                "current subs W-L-T": _wlt(dc),
            }
        )
    for tid in sorted(batch_ids, key=lambda i: ranks[i]):
        d = g[g.opp_team_id == tid]
        dc = gc[gc.opp_team_id == tid]
        per_batch.append(
            {
                "rank": ranks[tid],
                "team": names[tid],
                "games vs top-14": len(d),
                "W-L-T": _wlt(d, flip=True),
                "win %": 100 * (d.result == "L").mean() if len(d) else np.nan,
                "current subs W-L-T": _wlt(dc, flip=True),
            }
        )
    return overall, pd.DataFrame(per_top), pd.DataFrame(per_batch)


def group_losses(
    teams: pd.DataFrame, latest: dict[str, pd.DataFrame], feats: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Losses of the current submissions per group, and which feature the winner differed in most.

    Differences are measured in pooled standard deviations of each feature (over every seat
    with features) so that a cow and a CARE op count on the same footing; the dossiers' loss
    tables use raw differences instead.
    """
    scale = {c: max(float(feats[c].std()), 1.0) for c in DIFF_COLS if c in feats}
    top_ids = set(teams[teams.group == "top"].team_id.astype(int))
    batch_ids = set(teams[teams.group == "batch"].team_id.astype(int))
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
                    "opp group": "top-14"
                    if oid in top_ids
                    else "next-15"
                    if oid in batch_ids
                    else "other",
                    "feature": PLAN_COLS.get(c, c),
                    "direction": "opponent higher" if d > 0 else "opponent lower",
                }
            )
    df = pd.DataFrame(rows)
    if not len(df):
        return pd.DataFrame(), pd.DataFrame()
    summary, top_feats = [], []
    for grp in ("top", "batch"):
        g = df[df.group == grp]
        if not len(g):
            continue
        summary.append(
            {
                "group": GROUP_NAMES[grp],
                "losses": len(g),
                "median margin": g.margin.median(),
                "within 3k %": 100 * (g.margin > -3000).mean(),
                "to top-14 %": 100 * (g["opp group"] == "top-14").mean(),
                "to next-15 %": 100 * (g["opp group"] == "next-15").mean(),
                "to others %": 100 * (g["opp group"] == "other").mean(),
            }
        )
        counts = g.groupby(["feature", "direction"]).size().sort_values(ascending=False)
        for (feat, direction), n in counts.head(4).items():
            top_feats.append(
                {
                    "group": GROUP_NAMES[grp],
                    "biggest scaled difference in the loss": f"{feat}, {direction}",
                    "losses": int(n),
                    "share %": 100 * n / len(g),
                }
            )
    return pd.DataFrame(summary), pd.DataFrame(top_feats)


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
        ax.plot(range(1, len(v) + 1), v, color=GROUP_COLORS[group], alpha=0.22, linewidth=0.8)
    for group in ("top", "batch"):
        arr = [
            list(vals[:n]) + [np.nan] * (n - len(vals[:n])) for _, g, vals in paths if g == group
        ]
        if not arr:
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

    cols = 4
    rows_n = max(math.ceil(len(features) / cols), 1)
    fig, axes = plt.subplots(rows_n, cols, figsize=(11, 2.3 * rows_n), dpi=130)
    fig.patch.set_facecolor(SURFACE)
    axes = np.array(axes).reshape(-1)
    rng = np.random.default_rng(0)
    for ax, feat in zip(axes, features):
        for yi, group in enumerate(("top", "batch")):
            vals = profile[profile.group == group][feat].dropna().astype(float)
            y = yi + rng.uniform(-0.18, 0.18, len(vals))
            ax.scatter(
                vals,
                y,
                s=20,
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
        ax.set_yticks([0, 1])
        ax.set_yticklabels([GROUP_NAMES["top"], GROUP_NAMES["batch"]], fontsize=7)
        ax.set_ylim(-0.7, 1.7)
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
    profiles = []
    for _, t in teams.iterrows():
        cur = latest.get(t.team_name)
        if cur is None or not len(cur):
            continue
        profiles.append(team_profile(t, cur, hist))
    profile = pd.DataFrame(profiles)
    n_top = int((profile.group == "top").sum()) if len(profile) else 0
    n_batch = int((profile.group == "batch").sum()) if len(profile) else 0
    if n_top == 0 or n_batch == 0:
        note = "_Group comparison needs replays for both groups; not built yet._"
        return f"## Top-14 vs next-15\n\n{note}\n", f"# Top-14 vs next-15\n\n{note}\n"

    cmp_parts = []
    for section, labels in COMPARE_SECTIONS:
        c = compare_table(profile, labels)
        c.insert(0, "section", section)
        cmp_parts.append(c)
    cmp = pd.concat(cmp_parts, ignore_index=True)
    sep, same = separation_bullets(cmp)

    snapshot = teams.iloc[0].get("snapshot", "")
    who = teams[["rank", "team_name", "group", "score", "public_games", "current_sub_games"]].copy()
    who["group"] = who.group.map(GROUP_NAMES)
    who["Kaggle medal zone"] = np.where(who["rank"] <= KAGGLE_GOLD_RANK, "gold", "silver")
    who["sampled current-sub games"] = [len(latest.get(n, [])) for n in teams.team_name]
    who = who.rename(columns={"team_name": "team"})

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
    classes = ["day 1", "day 2", "day 4-6", "day 8-16", "end-game only", "fixed"]
    field_class = profile["field branch turn"].map(branch_class)
    cls = pd.DataFrame(
        {
            "first field branch": classes,
            "top-14 teams": [
                int(((profile.group == "top") & (field_class == c)).sum()) for c in classes
            ],
            "next-15 teams": [
                int(((profile.group == "batch") & (field_class == c)).sum()) for c in classes
            ],
        }
    )
    drivers = ["opponent", "weed", "seat", "shop", "none", "fixed", "n/a"]
    drv = pd.DataFrame(
        {
            "dominant driver at the first branch": drivers,
            "top-14 teams": [
                int(((profile.group == "top") & (profile.driver == d)).sum()) for d in drivers
            ],
            "next-15 teams": [
                int(((profile.group == "batch") & (profile.driver == d)).sum()) for d in drivers
            ],
        }
    )
    drv = drv[(drv["top-14 teams"] + drv["next-15 teams"]) > 0]

    overall, per_top, per_batch = group_h2h(hist, teams)
    loss_summary, loss_feats = group_losses(teams, latest, feats)

    paths = []
    for _, t in teams.iterrows():
        if pd.isna(t.current_sub) or t.team_name not in latest or not len(latest[t.team_name]):
            continue
        paths.append((t.team_name, t.group, list(rating_path(hist, int(t.current_sub)))))
    group_rating_figure(paths, REPORTS / "figs" / "group_rating.png")
    ranked = cmp.dropna(subset=["P(top > next)"]).copy()
    ranked["d"] = (ranked["P(top > next)"] - 0.5).abs()
    strip_feats = ranked.sort_values(["d", "p"], ascending=[False, True]).feature.head(8).tolist()
    group_strip_figure(profile, strip_feats, REPORTS / "figs" / "group_strip.png")

    md = [
        "# Top-14 vs next-15",
        "",
        (
            f"Snapshot {snapshot}. The top-14 are the teams that were top-10 in Iminabo's "
            f"screenshot or on the live board on 2026-09-14; the next-15 are chunks of the "
            f"gold zone outside them (ranks 8-48 at snapshot time, {n_batch} teams with "
            f"replays). Under Kaggle's medal rule for 9,066 teams (gold = top 10 + 0.2% = rank "
            f"{KAGGLE_GOLD_RANK}, silver = top 5%), ranks 8-23 of the batch are gold and 29-48 "
            f"silver; under the top-50 working assumption all are gold. Every number below is "
            f"a per-team median over the current submission's sampled games, compared across "
            f"teams: 'P(top > next)' is the chance that a random top-14 team's value is above a "
            f"random next-15 team's (0.5 = no separation), 'p' is the two-sided Mann-Whitney "
            f"test. Numbers are per game unless stated."
        ),
        "",
        "## Who is in each group",
        "",
        md_table(who),
        "",
        "## What separates the groups",
        "",
    ]
    md += [f"- {b}" for b in sep] if sep else ["- nothing at p < 0.05"]
    md += ["", "## What does not separate them (p >= 0.2 and P(top > next) within 0.35-0.65)", ""]
    md += [f"- {b}" for b in same] if same else ["- (none)"]
    md += [
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
        "## Feature comparison",
        "",
    ]
    for section, _ in COMPARE_SECTIONS:
        part = cmp[cmp.section == section].drop(columns=["section"])
        if len(part):
            md += [f"**{section}**", "", md_table(part, floatfmt=".2f"), ""]
    md += ["## Head to head between the groups", "", overall, ""]
    if len(per_top):
        md += ["Top-14 teams against the next-15:", "", md_table(per_top), ""]
    if len(per_batch):
        md += ["Next-15 teams against the top-14:", "", md_table(per_batch), ""]
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
        md_table(profile.drop(columns=["driver gap"]).sort_values("rank")),
        "",
    ]
    groups_md = "\n".join(md) + "\n"

    section = [
        "## Top-14 vs next-15",
        "",
        (
            f"{n_top} top-14 teams against {n_batch} next-15 teams, per-team medians of the "
            f"current submissions. Full tables, head-to-head, losses, and figures in "
            f"[groups.md](groups.md)."
        ),
        "",
        "Separates the groups (p < 0.05):",
        "",
    ]
    section += [f"- {b}" for b in sep[:8]] if sep else ["- nothing at p < 0.05"]
    section += ["", "Does not separate them:", ""]
    section += [f"- {b}" for b in same[:8]] if same else ["- (none)"]
    section += ["", overall, ""]
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
        "top": int((teams.group == "top").sum()),
        "batch": int((teams.group == "batch").sum()),
        "episodes_with_features": int(feats.episode_id.nunique()),
        "top_seats": int(feats.is_top10_seat.sum()),
    }
    (REPORTS / "build.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(Counter(feats[feats.is_top10_seat].team_name).most_common())


if __name__ == "__main__":
    main()
