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

from research.paths import REPORTS, TOP10
from research.report import SERIES, WINDOW_ORDER, bar_figure, line_figure, md_table

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
}
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


def slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-")
    return s or "team"


def load() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    teams = pd.read_csv(TOP10 / "teams.csv").sort_values("rank")
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
    name, sl = t.team_name, slug(t.team_name)
    md = [f"# {name} (rank {int(t['rank'])}, score {t.score:.1f})", ""]
    md += [
        f"- team id {int(t.team_id)}; current submission {int(t.current_sub) if pd.notna(t.current_sub) else 'unknown'}"
        f" ({int(t.current_sub_games)} public games)",
        f"- submissions found {int(t.subs_found)} of {int(t.subs_declared) if pd.notna(t.subs_declared) else '?'} declared;"
        f" {int(t.public_games)} public games from {str(t.first_game)[:10]} to {str(t.last_game)[:10]}",
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
            f"{name}: rating of the current submission",
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
            f"{name}: median money by day, per window",
            "day",
            "coins",
            REPORTS / "figs" / f"{sl}_money.png",
            colors=SERIES,
        )
        md += [f"![money by day](figs/{sl}_money.png)", ""]

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
    ]
    cur = rows[rows.is_current_sub == True].drop_duplicates("episode_id")
    if len(cur):
        md += [
            f"Current submission ({len(cur)} sampled games): field is **{verdict(cur, 'field')}**; "
            f"market is **{verdict(cur, 'market')}**.",
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
                f"What goes with being off the modal field line at turn {int(branch[1:])} "
                f"(the first cut where fewer than 90% of games share one line):",
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


def cross_team(teams, hist, sample, feats) -> str:
    md = [
        "# Top-10 study: summary",
        "",
        f"Snapshot: {teams.iloc[0].get('snapshot', '')}. Teams studied: {len(teams)}.",
        "",
    ]
    cov = teams[
        [
            "rank",
            "team_name",
            "score",
            "current_sub",
            "current_sub_games",
            "subs_found",
            "subs_declared",
            "public_games",
            "first_game",
            "last_game",
        ]
    ].copy()
    cov["first_game"] = cov.first_game.astype(str).str[:10]
    cov["last_game"] = cov.last_game.astype(str).str[:10]
    md += ["## Coverage", "", md_table(cov), ""]

    latest = {}
    fam_rows = []
    verdicts = []
    for _, t in teams.iterrows():
        rows = team_windows(sample, feats, int(t.team_id))
        cur = rows[rows.is_current_sub == True].drop_duplicates("episode_id")
        latest[t.team_name] = cur
        if len(cur):
            verdicts.append(
                {
                    "rank": int(t["rank"]),
                    "team": t.team_name,
                    "games": len(cur),
                    "field": verdict(cur, "field"),
                    "market": verdict(cur, "market"),
                }
            )
            rec = {"rank": int(t["rank"]), "team": t.team_name}
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
            "Letters name the modal field-action line of each team at each turn cut; two teams with the "
            "same letter at a cut submitted identical farmer and hand actions through that turn.",
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
            rest = plan.iloc[1:].median(numeric_only=True)
            diff = pd.DataFrame(
                {
                    "feature": rest.index,
                    f"#1 {top1.team}": [top1[c] for c in rest.index],
                    "median of the others": rest.values,
                }
            )
            diff = diff[diff.feature.isin([PLAN_COLS.get(c, c) for c in plan_cols] + ["win %"])]
            md += ["## What the #1 does differently", "", md_table(diff), ""]

    timing = []
    for _, t in teams.iterrows():
        cur = latest[t.team_name]
        if len(cur):
            rec = {"rank": int(t["rank"]), "team": t.team_name}
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

    labels = [v["team"] for v in verdicts]
    values = [len(latest[v["team"]].field_h400.unique()) for v in verdicts]
    if labels:
        bar_figure(
            labels,
            values,
            "Distinct field-action lines at turn 400 (current submissions)",
            "lines",
            REPORTS / "figs" / "families_h400.png",
        )
        md += ["![families](figs/families_h400.png)", ""]
    curves = {}
    for v in verdicts:
        cur = latest[v["team"]]
        arr = np.array([list(m) + [np.nan] * (30 - len(m)) for m in cur.money_by_day])
        curves[v["team"]] = list(np.nanmedian(arr, axis=0))
    if curves:
        small_multiples(curves, REPORTS / "figs" / "money_current.png")
        md += ["![money by day, current submissions](figs/money_current.png)", ""]
    md += ["## Team dossiers", ""]
    md += [f"- [{t.team_name}]({slug(t.team_name)}.md)" for _, t in teams.iterrows()]
    return "\n".join(md) + "\n"


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
        (REPORTS / f"{slug(t.team_name)}.md").write_text(text, encoding="utf-8")
        print(f"wrote {slug(t.team_name)}.md")
    (REPORTS / "summary.md").write_text(cross_team(teams, hist, sample, feats), encoding="utf-8")
    print("wrote summary.md")
    meta = {
        "teams": len(teams),
        "episodes_with_features": int(feats.episode_id.nunique()),
        "top_seats": int(feats.is_top10_seat.sum()),
    }
    (REPORTS / "build.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(Counter(feats[feats.is_top10_seat].team_name).most_common())


if __name__ == "__main__":
    main()
