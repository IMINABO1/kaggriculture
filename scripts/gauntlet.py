"""The gauntlet: our agent in seat 1 against seat-0 recordings of named teams, many games each.

    uv run python scripts/gauntlet.py --tapes "opponents/gauntlet/*.json" --jobs 3

A recording in seat 0 draws its weeds before our farm does, so it plays exactly as it was
recorded whatever we do (journal 2026-09-16); the only coupling left is the market. Each
tape's file name starts with the team slug, so the summary is per team. Results append to
results/gauntlet.csv.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import statistics
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

from arena import play  # noqa: E402

RESULTS = ROOT / "results" / "gauntlet.csv"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", default="main.py")
    ap.add_argument("--tapes", default="opponents/gauntlet/*.json")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--steps", type=int, default=720)
    args = ap.parse_args()

    files = sorted(Path(p) for p in glob.glob(str(ROOT / args.tapes)))
    if not files:
        raise SystemExit(f"no tapes match {args.tapes}")
    tasks = []
    for path in files:
        tape = json.loads(path.read_text(encoding="utf-8"))
        if tape["tape_seat"] != 0:
            continue
        tasks.append({"a": str(ROOT / args.a), "b": str(path), "b_kind": "tape", "seed": tape["seed"],
                      "seat": 1, "steps": args.steps, "tape_seat": 0, "team": path.stem.rsplit("_", 1)[0]})
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            rows = list(pool.map(play, tasks))
    else:
        rows = [play(t) for t in tasks]

    ts = datetime.now(UTC).isoformat(timespec="seconds")
    RESULTS.parent.mkdir(exist_ok=True)
    new_file = not RESULTS.exists()
    with RESULTS.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["ts", "a", "team", "tape", "seed", "me", "opp", "result", "ref_me", "ref_opp", "me_status", "opp_status"])
        if new_file:
            writer.writeheader()
        for task, row in zip(tasks, rows):
            writer.writerow({"ts": ts, "a": args.a, "team": task["team"], "tape": Path(task["b"]).name, "seed": row["seed"],
                             "me": row["me"], "opp": row["opp"], "result": row["result"], "ref_me": row["ref_me"],
                             "ref_opp": row["ref_opp"], "me_status": row["me_status"], "opp_status": row["opp_status"]})

    by_team = defaultdict(list)
    for task, row in zip(tasks, rows):
        by_team[task["team"]].append(row)
    print(f"{'team':<24} {'games':>5} {'W-L-T':>8} {'win%':>5} {'our bank':>9} {'their bank':>10} {'recorded':>9} {'their recorded':>14}")
    total_w = total = 0
    for team, rs in by_team.items():
        w = sum(r["result"] == "W" for r in rs)
        losses = sum(r["result"] == "L" for r in rs)
        t = len(rs) - w - losses
        total_w += w
        total += len(rs)
        print(f"{team:<24} {len(rs):>5} {f'{w}-{losses}-{t}':>8} {w / len(rs):>5.0%} "
              f"{statistics.mean(r['me'] for r in rs):>9.0f} {statistics.mean(r['opp'] for r in rs):>10.0f} "
              f"{statistics.mean(r['ref_me'] for r in rs):>9.0f} {statistics.mean(r['ref_opp'] for r in rs):>14.0f}")
    errors = sum(r["me_status"] != "DONE" for r in rows)
    print(f"\nall: {total_w}-{total - total_w} of {total}, win rate {total_w / total:.0%}, errors {errors}")
    print("recorded = the bank the recording's original opponent made in that seat; their recorded = the tape's own bank then")


if __name__ == "__main__":
    main()
