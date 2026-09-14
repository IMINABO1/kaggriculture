"""Snapshot the top of the public leaderboard.

    uv run python scripts/top10/snapshot.py --top 10

Writes data/top10/snapshot_<UTC>.csv and data/top10/snapshot_latest.csv with rank, team id,
team name, and score. The board moves hourly, so every downstream file records which snapshot
it was built from.
"""

from __future__ import annotations

import argparse
import csv
import io
import os
import subprocess
from datetime import UTC, datetime

from research.paths import TOP10


def leaderboard_csv() -> list[dict]:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    out = subprocess.run(
        ["kaggle", "competitions", "leaderboard", "kaggriculture", "-s", "-v", "--page-size", "50"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        env=env,
    ).stdout
    body = "\n".join(
        line for line in out.splitlines() if line.strip() and not line.startswith("Next Page")
    )
    return list(csv.DictReader(io.StringIO(body)))


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument(
        "--include",
        default="",
        help="comma list of extra team names to keep (e.g. teams seen in the top 10 earlier)",
    )
    args = ap.parse_args()

    board = leaderboard_csv()
    rows = board[: args.top]
    wanted = {n.strip() for n in args.include.split(",") if n.strip()}
    have = {r["teamName"] for r in rows}
    for r in board:
        if r["teamName"] in wanted and r["teamName"] not in have:
            rows.append(r)
            have.add(r["teamName"])
    missing = wanted - have
    if missing:
        print(f"warning: not in the top {len(board)} rows, skipped: {sorted(missing)}")
    rank_of = {r["teamId"]: i + 1 for i, r in enumerate(board)}
    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H%MZ")
    TOP10.mkdir(parents=True, exist_ok=True)
    records = [
        {
            "rank": rank_of[r["teamId"]],
            "team_id": int(r["teamId"]),
            "team_name": r["teamName"],
            "score": float(r["score"]),
            "snapshot": stamp,
        }
        for r in rows
    ]
    for name in (f"snapshot_{stamp}.csv", "snapshot_latest.csv"):
        with (TOP10 / name).open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(records[0].keys()))
            w.writeheader()
            w.writerows(records)
    for r in records:
        print(f"{r['rank']:>2}  {r['score']:7.1f}  {r['team_name']}  ({r['team_id']})")
    print(f"snapshot {stamp} written to {TOP10}")


if __name__ == "__main__":
    main()
