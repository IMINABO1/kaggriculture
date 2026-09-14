"""Apply the window rule to every team's history.

    uv run python scripts/top10/sample.py

Reads data/top10/history.parquet, writes data/top10/sample.csv with one row per
(team, window, episode). Windows: ALL when the history has <= 250 public games, else
F / Q1 / Q2 / Q3 / L; plus C0 = the first 50 games of the team's current submission.
"""

from __future__ import annotations

import pandas as pd

from research.paths import TOP10
from research.sampling import current_sub_windows, windows


def main() -> None:
    hist = pd.read_parquet(TOP10 / "history.parquet")
    hist = hist[(hist.type == "EPISODE_TYPE_PUBLIC") & (hist.state == "COMPLETED")]
    teams = pd.read_csv(TOP10 / "teams.csv")

    rows = []
    for _, t in teams.iterrows():
        h = (
            hist[hist.team_id == t.team_id]
            .sort_values(["create_time", "episode_id"])
            .reset_index(drop=True)
        )
        for name, positions in windows(len(h)).items():
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


if __name__ == "__main__":
    main()
