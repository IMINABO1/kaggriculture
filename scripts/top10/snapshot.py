"""Snapshot the top of the public leaderboard.

    uv run python scripts/top10/snapshot.py --top 10
    uv run python scripts/top10/snapshot.py --top 0 --include "A,B" --ranks "8-9,13-14,20-23"

Writes data/top10/snapshot_<UTC>.csv and data/top10/snapshot_latest.csv with rank, team id,
team name, score, and group. The board moves hourly, so every downstream file records which
snapshot it was built from.

Groups: teams taken by --top or --include are "top", teams taken by --ranks are "batch".
A --ranks chunk "20-23" means "the four teams at or after rank 20 that are not in the top
group": the board moves hourly, so a chunk that lands on a top-group team extends past it
rather than coming up short.
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
        ["kaggle", "competitions", "leaderboard", "kaggriculture", "-s", "-v", "--page-size", "60"],
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


def parse_chunks(spec: str) -> list[tuple[int, int]]:
    """ "8-9,13-14,20" -> [(8, 2), (13, 2), (20, 1)] as (first rank, how many teams)."""
    chunks: list[tuple[int, int]] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        lo, _, hi = part.partition("-")
        chunks.append((int(lo), int(hi or lo) - int(lo) + 1))
    return chunks


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
    ap.add_argument(
        "--ranks",
        default="",
        help='comma list of rank ranges for the comparison batch, e.g. "8-9,13-14,20-23"',
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
    group = {r["teamId"]: "top" for r in rows}
    for start, count in parse_chunks(args.ranks):
        taken = 0
        for r in board[start - 1 :]:
            if taken == count:
                break
            if r["teamName"] in have:
                continue
            rows.append(r)
            have.add(r["teamName"])
            group[r["teamId"]] = "batch"
            taken += 1
        if taken < count:
            print(f"warning: chunk from rank {start} wanted {count} teams, found {taken}")
    rank_of = {r["teamId"]: i + 1 for i, r in enumerate(board)}
    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H%MZ")
    TOP10.mkdir(parents=True, exist_ok=True)
    records = sorted(
        (
            {
                "rank": rank_of[r["teamId"]],
                "team_id": int(r["teamId"]),
                "team_name": r["teamName"],
                "score": float(r["score"]),
                "snapshot": stamp,
                "group": group[r["teamId"]],
            }
            for r in rows
        ),
        key=lambda rec: rec["rank"],
    )
    for name in (f"snapshot_{stamp}.csv", "snapshot_latest.csv"):
        with (TOP10 / name).open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(records[0].keys()))
            w.writeheader()
            w.writerows(records)
    for r in records:
        print(
            f"{r['rank']:>2}  {r['score']:7.1f}  {r['group']:<5}  {r['team_name']}  ({r['team_id']})"
        )
    print(f"snapshot {stamp} written to {TOP10}")


if __name__ == "__main__":
    main()
