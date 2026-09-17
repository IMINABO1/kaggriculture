"""Build job-level labels (research/jobs.py) for encoded games.

    uv run python scripts/learn/build_jobs.py --team "THIRD FARM CLUB" --jobs 3
    uv run python scripts/learn/build_jobs.py --all --jobs 2

Writes data/features/jobs/<episode>.npz for every encoded game of the team's current
submission (or of every team in --teams-file, or --all), skipping those already built, and
prints the label class counts for the team's own seat.
"""

from __future__ import annotations

import argparse
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research.encode import FEATURES  # noqa: E402
from research.jobs import N_CLASSES, WORK_OPS, build, class_counts, jobs_path, load_labels  # noqa: E402
from research.paths import DATA  # noqa: E402


def build_one(ep: int) -> int:
    if not jobs_path(ep).exists():
        build(ep)
    return ep


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--team", default="")
    ap.add_argument("--teams-file", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--jobs", type=int, default=3)
    args = ap.parse_args()
    hist = pd.read_parquet(DATA / "gold/history.parquet")
    enc = set(pd.read_csv(FEATURES / "manifest.csv").episode_id.astype(int))
    if args.all:
        sel = hist[hist.episode_id.astype(int).isin(enc)]
    else:
        teams = [args.team] if args.team else [line.strip() for line in Path(args.teams_file).read_text(encoding="utf-8").splitlines() if line.strip()]
        sel = hist[hist.team_name.isin(teams) & hist.episode_id.astype(int).isin(enc)]
    eps = sorted({int(e) for e in sel.episode_id})
    todo = [e for e in eps if not jobs_path(e).exists()]
    print(f"{len(eps)} games selected, {len(todo)} to build", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for i, _ in enumerate(pool.map(build_one, todo, chunksize=8), 1):
            if i % 200 == 0:
                print(f"  {i} built ({i / (time.time() - t0):.1f}/s)", flush=True)
    print(f"built {len(todo)} in {time.time() - t0:.0f} s", flush=True)
    if args.team:
        counts = np.zeros(N_CLASSES, dtype=np.int64)
        cur = sel[sel.is_current_sub == True].drop_duplicates("episode_id")
        for r in cur.itertuples():
            counts += class_counts(load_labels(int(r.episode_id)), int(r.seat))
        total = counts.sum()
        print(f"{args.team} current submission, own seat: {total:,} unit-steps; " + ", ".join(
            f"{name} {100 * c / total:.1f}%" for name, c in zip(("NONE",) + WORK_OPS, counts)))


if __name__ == "__main__":
    main()
