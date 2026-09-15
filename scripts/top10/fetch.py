"""Download every replay named in data/top10/sample.csv.

    uv run python scripts/top10/fetch.py --jobs 3
    uv run python scripts/top10/fetch.py --windows C0,L,F --team Catalyst

Resumable: replays already in data/replays/ are skipped. The windows Iminabo asked for no
matter what (first 50, last 50, and the current submission's first 50) are fetched before
the quarter-point windows. Failures go to data/top10/fetch_failures.csv with the error text.

Episodes listed in data/top10/daily_index.csv (built by daily_index.py) are taken from the
official daily episode datasets, which are not subject to the replay endpoint's quota;
--source daily fetches only those, --source endpoint only the rest, auto (default) both.
"""

from __future__ import annotations

import argparse
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from research.kaggle_api import download_replay, download_replay_from_daily, replay_path
from research.paths import TOP10

PRIORITY = {"C0": 0, "L": 1, "F": 2, "ALL": 3, "Q2": 4, "Q1": 5, "Q3": 6}


def fetch(episode_id: int, dataset: str | None = None) -> tuple[int, str | None]:
    for attempt in range(3):
        try:
            if dataset:
                download_replay_from_daily(episode_id, dataset)
            else:
                download_replay(episode_id)
            return episode_id, None
        except Exception as exc:  # noqa: BLE001 - logged and retried, never fatal for the batch
            err = repr(exc)
            time.sleep(10 * (attempt + 1))
    return episode_id, err


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0, help="stop after this many downloads (0 = all)")
    ap.add_argument("--windows", default="", help="comma list, e.g. C0,L,F")
    ap.add_argument("--team", default="", help="substring of the team name")
    ap.add_argument("--ids-file", default="", help="one episode id per line; bypasses sample.csv")
    ap.add_argument("--source", default="auto", choices=["auto", "daily", "endpoint"])
    args = ap.parse_args()
    daily_path = TOP10 / "daily_index.csv"
    daily = (
        dict(pd.read_csv(daily_path)[["episode_id", "dataset"]].itertuples(index=False))
        if daily_path.exists()
        else {}
    )

    if args.ids_file:
        text = Path(args.ids_file).read_text(encoding="utf-8")
        ids = [int(x) for x in text.split() if x.strip()]
        sample = pd.DataFrame(
            {
                "episode_id": ids,
                "window": "IDS",
                "team_id": 0,
                "position": range(len(ids)),
                "team_name": "",
            }
        )
    else:
        sample = pd.read_csv(TOP10 / "sample.csv")
    if args.windows:
        sample = sample[sample.window.isin(args.windows.split(","))]
    if args.team:
        sample = sample[sample.team_name.str.contains(args.team, case=False, regex=False)]
    sample = sample.assign(prio=sample.window.map(PRIORITY).fillna(9))
    order = (
        sample.sort_values(["prio", "team_id", "position"])
        .drop_duplicates("episode_id")
        .episode_id.astype(int)
        .tolist()
    )
    todo = [e for e in order if not replay_path(e).exists()]
    stored = len(order) - len(todo)
    if args.source == "daily":
        todo = [e for e in todo if e in daily]
    elif args.source == "endpoint":
        todo = [e for e in todo if e not in daily]
    if args.limit:
        todo = todo[: args.limit]
    from_daily = sum(1 for e in todo if e in daily)
    print(
        f"{len(order)} episodes in scope, {stored} already stored, {len(todo)} to fetch now "
        f"({from_daily} from daily datasets, {len(todo) - from_daily} from the replay endpoint)"
    )

    failures = []
    done = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(fetch, e, daily.get(e)) for e in todo]
        for fut in as_completed(futures):
            episode_id, err = fut.result()
            done += 1
            if err:
                failures.append({"episode_id": episode_id, "error": err})
                print(f"FAILED {episode_id}: {err[:160]}", flush=True)
            if done % 25 == 0 or done == len(todo):
                rate = done / max(time.time() - t0, 1e-9)
                stamp = time.strftime("%H:%M:%SZ", time.gmtime())
                print(
                    f"{stamp} {done}/{len(todo)} done, {len(failures)} failed, "
                    f"{rate * 60:.1f}/min, eta {(len(todo) - done) / max(rate, 1e-9) / 60:.0f} min",
                    flush=True,
                )

    if failures:
        path = TOP10 / "fetch_failures.csv"
        with path.open("a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["episode_id", "error"])
            if path.stat().st_size == 0:
                w.writeheader()
            w.writerows(failures)
        print(f"{len(failures)} failures appended to {path}")


if __name__ == "__main__":
    main()
