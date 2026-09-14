"""Export recorded games of the top teams as replayable arena opponents.

    uv run python scripts/top10/export_tapes.py --window L --per-team 10

Writes opponents/top10/<team-slug>_<episode_id>.json holding the seed, both action streams,
both recorded banks, and which seat the top team played. `scripts/arena.py --b tape:<glob>`
plays the top team's stream in its recorded seat on its recorded seed.
"""

from __future__ import annotations

import argparse
import json
import re

import pandas as pd

from research.paths import OPPONENTS, TOP10
from research.store import load_trace, trace_path


def slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "team"


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--window", default="L", help="which window to export from (L = latest games)")
    ap.add_argument("--per-team", type=int, default=10)
    ap.add_argument("--team", default="", help="substring filter on team name")
    args = ap.parse_args()

    sample = pd.read_csv(TOP10 / "sample.csv")
    hist = pd.read_parquet(TOP10 / "history.parquet")[["episode_id", "team_id", "seat", "result"]]
    rows = sample[sample.window == args.window].merge(
        hist, on=["episode_id", "team_id"], how="left"
    )
    if args.team:
        rows = rows[rows.team_name.str.contains(args.team, case=False, regex=False)]
    out_dir = OPPONENTS / "top10"
    out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for team_id, group in rows.groupby("team_id"):
        group = group.sort_values("position", ascending=False)
        n = 0
        for r in group.itertuples(index=False):
            if n >= args.per_team or not trace_path(int(r.episode_id)).exists():
                continue
            trace = load_trace(int(r.episode_id))
            seat = int(r.seat)
            tape = {
                "episode_id": int(r.episode_id),
                "seed": trace["seed"],
                "engine": trace["engine"],
                "teams": trace["teams"],
                "banks": trace["rewards"],
                "tape_seat": seat,
                "tape_team": trace["teams"][seat],
                "recorded_result": r.result,
                "actions": [trace["seats"][0]["actions"], trace["seats"][1]["actions"]],
            }
            path = out_dir / f"{slug(str(r.team_name))}_{int(r.episode_id)}.json"
            path.write_text(json.dumps(tape, separators=(",", ":")), encoding="utf-8")
            written += 1
            n += 1
        print(f"{group.team_name.iloc[0]}: {n} tapes")
    print(f"{written} tapes written to {out_dir}")


if __name__ == "__main__":
    main()
