"""Snapshot the public leaderboard and pick the studied teams.

    uv run python scripts/top10/snapshot.py --top 10
    uv run python scripts/top10/snapshot.py --full --include "A,B" --members "C,D" --ranks "120-122,470-472"

Writes data/top10/snapshot_<UTC>.csv and data/top10/snapshot_latest.csv with rank, team id,
team name, score, medal zone, and group. The board moves hourly, so every downstream file
records which snapshot it was built from.

--full downloads the whole leaderboard (every team) instead of the top 60, which is needed
for ranks beyond 60 and for the medal zones. Zones follow Kaggle's rule for competitions
with 1,000+ teams: gold = top 10 + 0.2% of teams, silver = top 5%, bronze = top 10%.

Groups: teams taken by --top or --include are "top"; teams named by --members and teams
taken by --ranks are labelled with their zone (gold, silver, bronze, none). A --ranks chunk
"20-23" means "the four teams at or after rank 20 that are not already selected": the board
moves hourly, so a chunk that lands on a selected team extends past it. With --seeded-only
a chunk also skips teams the crawl could not seed (absent from the community index and
from every cached listing).
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import subprocess
import tempfile
import zipfile
from datetime import UTC, datetime
from pathlib import Path

from research.paths import COMMUNITY, EPISODE_CACHE, TOP10


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


def full_leaderboard() -> list[dict]:
    """Every team on the public leaderboard, in rank order, same keys as leaderboard_csv."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["kaggle", "competitions", "leaderboard", "kaggriculture", "--download", "-p", tmp],
            capture_output=True,
            check=True,
            env=env,
        )
        archive = next(Path(tmp).glob("*.zip"))
        with zipfile.ZipFile(archive) as zf:
            name = next(n for n in zf.namelist() if n.endswith(".csv"))
            text = zf.read(name).decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))
    rows.sort(key=lambda r: int(r["Rank"]))
    return [{"teamId": r["TeamId"], "teamName": r["TeamName"], "score": r["Score"]} for r in rows]


def zone_bounds(n_teams: int) -> dict[str, int]:
    """Last rank of each medal zone under Kaggle's rule for 1,000+ teams."""
    return {
        "gold": 10 + round(0.002 * n_teams),
        "silver": round(0.05 * n_teams),
        "bronze": round(0.10 * n_teams),
    }


def zone_of(rank: int, bounds: dict[str, int]) -> str:
    for name in ("gold", "silver", "bronze"):
        if rank <= bounds[name]:
            return name
    return "none"


def seeded_team_ids() -> set[int]:
    """Teams the crawl can seed: in the community index or in any cached listing."""
    ids: set[int] = set()
    agents = COMMUNITY / "agents.csv"
    if agents.exists():
        with agents.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            ids.update(int(r["team_id"]) for r in reader if r.get("team_id"))
    pattern = re.compile(r'"teamId":\s*"?(\d+)')
    for path in EPISODE_CACHE.glob("*.json"):
        ids.update(int(m) for m in pattern.findall(path.read_text(encoding="utf-8")))
    return ids


def parse_chunks(spec: str) -> list[tuple[int, int, int | None]]:
    """Chunk specs as (first rank, how many teams, last rank or None).

    "8-9" takes two unselected teams at or after rank 8, filling forward past selected
    ones; "11..28" takes every unselected team ranked 11 to 28 and no more.
    """
    chunks: list[tuple[int, int, int | None]] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if ".." in part:
            lo, hi = part.split("..")
            chunks.append((int(lo), int(hi) - int(lo) + 1, int(hi)))
        else:
            lo, _, hi = part.partition("-")
            chunks.append((int(lo), int(hi or lo) - int(lo) + 1, None))
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
        help='comma list of rank ranges for the comparison batches, e.g. "120-122,470-472"',
    )
    ap.add_argument(
        "--members",
        default="",
        help="comma list of team names to keep, labelled with their zone rather than 'top'",
    )
    ap.add_argument("--full", action="store_true", help="download the whole leaderboard")
    ap.add_argument(
        "--seeded-only", action="store_true", help="rank chunks skip teams the crawl cannot seed"
    )
    args = ap.parse_args()

    board = full_leaderboard() if args.full else leaderboard_csv()
    rank_of = {r["teamId"]: i + 1 for i, r in enumerate(board)}
    bounds = zone_bounds(len(board))
    print(
        f"{len(board)} teams on the board; zones end at gold {bounds['gold']}, "
        f"silver {bounds['silver']}, bronze {bounds['bronze']}"
    )
    rows = board[: args.top]
    wanted = {n.strip() for n in args.include.split(",") if n.strip()}
    members = {n.strip() for n in args.members.split(",") if n.strip()}
    have = {r["teamName"] for r in rows}
    group = {r["teamId"]: "top" for r in rows}
    for r in board:
        if r["teamName"] in wanted and r["teamName"] not in have:
            rows.append(r)
            have.add(r["teamName"])
            group[r["teamId"]] = "top"
    for r in board:
        if r["teamName"] in members and r["teamName"] not in have:
            rows.append(r)
            have.add(r["teamName"])
            group[r["teamId"]] = zone_of(rank_of[r["teamId"]], bounds)
    missing = (wanted | members) - have
    if missing:
        print(f"warning: not on the board, skipped: {sorted(missing)}")
    seeded = seeded_team_ids() if args.seeded_only else None
    for start, count, last in parse_chunks(args.ranks):
        taken = 0
        for r in board[start - 1 :]:
            if taken == count or (last is not None and rank_of[r["teamId"]] > last):
                break
            if r["teamName"] in have:
                continue
            if seeded is not None and int(r["teamId"]) not in seeded:
                print(f"  rank {rank_of[r['teamId']]} {r['teamName']}: no seed, skipped")
                continue
            rows.append(r)
            have.add(r["teamName"])
            group[r["teamId"]] = zone_of(rank_of[r["teamId"]], bounds)
            taken += 1
        if taken < count and last is None:
            print(f"warning: chunk from rank {start} wanted {count} teams, found {taken}")
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
                "zone": zone_of(rank_of[r["teamId"]], bounds),
                "group": group[r["teamId"]],
            }
            for r in rows
        ),
        key=lambda rec: rec["rank"],
    )
    (TOP10 / f"zones_{stamp}.json").write_text(
        json.dumps({"teams": len(board), **bounds}), encoding="utf-8"
    )
    for name in (f"snapshot_{stamp}.csv", "snapshot_latest.csv"):
        with (TOP10 / name).open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(records[0].keys()))
            w.writeheader()
            w.writerows(records)
    for r in records:
        print(
            f"{r['rank']:>4}  {r['score']:7.1f}  {r['zone']:<6} {r['group']:<6}  "
            f"{r['team_name']}  ({r['team_id']})"
        )
    print(f"snapshot {stamp} written to {TOP10}")


if __name__ == "__main__":
    main()
