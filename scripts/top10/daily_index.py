"""Index the official daily episode datasets so replays can be taken from them.

    uv run python scripts/top10/daily_index.py
    uv run python scripts/top10/daily_index.py --dates 2026-09-09,2026-09-14

Kaggle publishes one dataset per day (`kaggle/kaggriculture-episodes-<date>`, listed in
`kaggle/kaggriculture-episodes-index`'s manifest.csv) holding the day's top-rated episodes
as individual `<episode_id>.json` files. Those files download through the datasets endpoint,
which is not subject to the replay endpoint's quota. This script lists every daily dataset
named in the manifest (or only --dates) and writes data/top10/daily_index.csv with one row
per (episode_id, date, dataset, bytes). Listings are cached per day under
data/top10/daily/ so reruns only touch new days.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

import pandas as pd
import requests

from research.kaggle_api import _kaggle
from research.paths import TOP10

INDEX_DATASET = "kaggle/kaggriculture-episodes-index"
DAILY_DIR = TOP10 / "daily"


def manifest() -> pd.DataFrame:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            [
                "kaggle",
                "datasets",
                "download",
                INDEX_DATASET,
                "-f",
                "manifest.csv",
                "-p",
                tmp,
                "--force",
                "--quiet",
            ],
            check=True,
            capture_output=True,
            env=env,
        )
        return pd.read_csv(Path(tmp) / "manifest.csv")


def _with_backoff(call, attempts: int = 8):
    """Run a client call, sleeping out api.kaggle.com's 429s (Retry-After or exponential)."""
    for attempt in range(attempts):
        try:
            return call()
        except requests.HTTPError as exc:
            if exc.response is None or exc.response.status_code != 429:
                raise
            retry_after = exc.response.headers.get("Retry-After")
            wait = (
                float(retry_after)
                if retry_after and retry_after.isdigit()
                else min(120, 5 * 2**attempt)
            )
            print(f"api throttled: waiting {wait:.0f}s", flush=True)
            time.sleep(wait + 1)
    raise RuntimeError("api.kaggle.com kept throttling")


def list_day(slug: str) -> list[dict]:
    """Every file of one daily dataset, following page tokens."""
    api = _kaggle()
    out: list[dict] = []
    token = None
    while True:
        page = _with_backoff(
            lambda t=token: api.dataset_list_files(slug, page_token=t, page_size=1000)
        )
        for f in page.files:
            name = getattr(f, "name", None) or getattr(f, "ref", "")
            if not name.endswith(".json"):
                continue
            out.append({"episode_id": int(name[:-5]), "bytes": int(getattr(f, "size", 0) or 0)})
        token = getattr(page, "nextPageToken", None) or getattr(page, "next_page_token", None)
        if not token:
            break
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--dates", default="", help="comma list of YYYY-MM-DD to (re)list")
    ap.add_argument("--refresh", action="store_true", help="ignore cached day listings")
    args = ap.parse_args()

    days = manifest()
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    wanted = {d.strip() for d in args.dates.split(",") if d.strip()}
    rows = []
    for r in days.itertuples(index=False):
        date, slug = str(r.date), f"kaggle/{r.daily_dataset_slug}"
        if wanted and date not in wanted:
            continue
        cache = DAILY_DIR / f"{date}.json"
        if cache.exists() and not args.refresh:
            files = json.loads(cache.read_text(encoding="utf-8"))
        else:
            files = list_day(slug)
            cache.write_text(json.dumps(files), encoding="utf-8")
            print(
                f"{date}: {len(files)} episode files (manifest says {r.episode_count})", flush=True
            )
        rows += [
            {"episode_id": f["episode_id"], "date": date, "dataset": slug, "bytes": f["bytes"]}
            for f in files
        ]
    index = pd.DataFrame(rows).drop_duplicates("episode_id")
    with (TOP10 / "daily_index.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["episode_id", "date", "dataset", "bytes"])
        w.writeheader()
        w.writerows(index.to_dict("records"))
    print(f"daily_index.csv: {len(index)} episodes over {index.date.nunique()} days")


if __name__ == "__main__":
    main()
