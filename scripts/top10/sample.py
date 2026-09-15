"""Apply the window rule to every team's history.

    uv run python scripts/top10/sample.py

Reads data/top10/history.parquet, writes data/top10/sample.csv with one row per
(team, window, episode). Windows: ALL when the history has <= 250 public games, else
F / Q1 / Q2 / Q3 / L; plus C0 = the first 50 games of the team's current submission.

    uv run python scripts/top10/sample.py --freeze data/top10/sample_top14_2026-09-14T1936Z.csv

With --freeze, teams of the frozen group (default: top; "all" for every team in the file)
keep the history windows of that earlier sample instead of being re-cut from the longer
history; only C0 is recomputed, since the current submission may have been corrected. This
keeps already-studied teams' windows fixed while new teams are added. --new-windows C0
gives teams absent from the frozen file only their current-submission window (the replay
quota makes full histories for every new team unaffordable).
"""

from __future__ import annotations

import argparse

import pandas as pd

from research.paths import TOP10
from research.sampling import current_sub_windows, windows


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--freeze", default="", help="earlier sample.csv whose windows are kept")
    ap.add_argument(
        "--freeze-group", default="top", help="group whose windows are frozen ('all' = every team)"
    )
    ap.add_argument(
        "--new-windows",
        default="all",
        choices=["all", "C0"],
        help="windows for teams not in the frozen file: all history windows, or C0 only",
    )
    args = ap.parse_args()

    hist = pd.read_parquet(TOP10 / "history.parquet")
    hist = hist[(hist.type == "EPISODE_TYPE_PUBLIC") & (hist.state == "COMPLETED")]
    teams = pd.read_csv(TOP10 / "teams.csv")
    if "group" not in teams:
        teams["group"] = "top"
    frozen = pd.read_csv(args.freeze) if args.freeze else pd.DataFrame(columns=["team_id"])
    if "window" in frozen:
        frozen = frozen[frozen.window != "C0"]

    rows = []
    kept = 0
    for _, t in teams.iterrows():
        h = (
            hist[hist.team_id == t.team_id]
            .sort_values(["create_time", "episode_id"])
            .reset_index(drop=True)
        )
        old = frozen[frozen.team_id == t.team_id]
        if (args.freeze_group == "all" or t.group == args.freeze_group) and len(old):
            rows.extend(old.to_dict("records"))
            kept += 1
            history_windows = {}
        elif args.freeze and args.new_windows == "C0":
            history_windows = {}
        else:
            history_windows = windows(len(h))
        for name, positions in history_windows.items():
            for pos in positions:
                r = h.iloc[pos]
                rows.append(
                    {
                        "team_id": t.team_id,
                        "team_name": t.team_name,
                        "window": name,
                        "position": pos,
                        "history_len": len(h),
                        "episode_id": r.episode_id,
                        "sub": r["sub"],
                        "create_time": r.create_time,
                    }
                )
        c = h[h["sub"] == t.current_sub].reset_index(drop=True)
        for name, positions in current_sub_windows(len(c)).items():
            for pos in positions:
                r = c.iloc[pos]
                rows.append(
                    {
                        "team_id": t.team_id,
                        "team_name": t.team_name,
                        "window": name,
                        "position": pos,
                        "history_len": len(c),
                        "episode_id": r.episode_id,
                        "sub": r["sub"],
                        "create_time": r.create_time,
                    }
                )
    sample = pd.DataFrame(rows)
    sample.to_csv(TOP10 / "sample.csv", index=False)

    summary = sample.groupby(["team_name", "window"]).size().unstack(fill_value=0)
    print(summary.to_string())
    print(f"\nrows {len(sample)}, unique episodes to fetch {sample.episode_id.nunique()}")
    if kept:
        print(f"history windows of {kept} teams kept from {args.freeze}")


if __name__ == "__main__":
    main()
