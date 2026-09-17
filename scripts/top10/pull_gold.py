"""Pull every replay of the teams in a workspace's history until the replay store reaches a size cap.

    KAGG_WORKSPACE=data/gold uv run python scripts/top10/pull_gold.py --cap-gb 10 --jobs 3

Runs after crawl.py has filled <workspace>/history.parquet. Writes <workspace>/ids.txt (every
episode of every listed submission, deduplicated, not yet on disk), then calls fetch.py in
batches: the daily-dataset source first (no quota), the replay endpoint after (rationed; the
fetcher waits the quota out). Stops when data/replays exceeds --cap-gb or nothing is left.
Resumable: rerun it and it continues from what is on disk.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research.kaggle_api import replay_path  # noqa: E402
from research.paths import REPLAYS, TOP10  # noqa: E402


def store_gb() -> float:
    return sum(p.stat().st_size for p in REPLAYS.glob("*.json.zst")) / 1e9


def missing_ids(teams_first: list[str] | None = None) -> list[int]:
    """Every listed game not on disk, newest first; the current-submission games of the
    named teams (in the order given) ahead of everything else."""
    hist = pd.read_parquet(TOP10 / "history.parquet")
    ids = sorted({int(e) for e in hist.episode_id}, reverse=True)
    todo = [e for e in ids if not replay_path(e).exists()]
    if not teams_first:
        return todo
    first: list[int] = []
    seen: set[int] = set()
    for name in teams_first:
        cur = hist[(hist.team_name == name) & (hist.is_current_sub == True)]
        for e in sorted({int(x) for x in cur.episode_id}, reverse=True):
            if e not in seen and not replay_path(e).exists():
                first.append(e)
                seen.add(e)
    return first + [e for e in todo if e not in seen]


def read_teams(path: str) -> list[str]:
    if not path:
        return []
    return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cap-gb", type=float, default=10.0)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--batch", type=int, default=500, help="downloads per fetch.py call")
    ap.add_argument("--sources", default="daily,endpoint", help="comma list, in order")
    ap.add_argument("--teams-first", default="", help="file of team names (one a line, UTF-8) whose current-submission games are fetched first")
    args = ap.parse_args()
    ids_file = TOP10 / "ids.txt"
    teams_first = read_teams(args.teams_first)
    for source in [s for s in args.sources.split(",") if s]:
        while True:
            size = store_gb()
            todo = missing_ids(teams_first)
            ids_file.write_text("\n".join(str(e) for e in todo), encoding="utf-8")
            print(f"[pull_gold] {time.strftime('%H:%M:%SZ', time.gmtime())} store {size:.2f} GB, {len(todo)} episodes missing, source {source}", flush=True)
            if size >= args.cap_gb:
                print(f"[pull_gold] cap of {args.cap_gb} GB reached", flush=True)
                return
            if not todo:
                print("[pull_gold] nothing left to fetch", flush=True)
                return
            before = len(todo)
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "top10" / "fetch.py"), "--ids-file", str(ids_file),
                 "--source", source, "--jobs", str(args.jobs), "--limit", str(args.batch)],
                cwd=ROOT, check=False,
            )
            if len(missing_ids()) == before:
                print(f"[pull_gold] source {source} made no progress; moving on", flush=True)
                break


if __name__ == "__main__":
    main()
