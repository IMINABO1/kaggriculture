"""Import a workspace's missing games from the official daily episode datasets, one archive at a time.

    KAGG_WORKSPACE=data/gold uv run python scripts/top10/pull_daily_bulk.py [--datasets N]

For every dataset in <workspace>/daily_index.csv that holds games still missing from the
replay store (most first): download the whole archive (the datasets endpoint, no replay
quota), store just the wanted <episode_id>.json members compressed, delete the archive.
Resumable: datasets whose games are all on disk are skipped.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import time
import zipfile
from collections import defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research.kaggle_api import _store_raw, replay_path  # noqa: E402
from research.paths import TOP10  # noqa: E402


def wanted_by_dataset() -> dict[str, set[int]]:
    hist = pd.read_parquet(TOP10 / "history.parquet")
    missing = {int(e) for e in hist.episode_id if not replay_path(int(e)).exists()}
    daily = pd.read_csv(TOP10 / "daily_index.csv")
    out: dict[str, set[int]] = defaultdict(set)
    for e, ds in zip(daily.episode_id.astype(int), daily.dataset):
        if e in missing:
            out[ds].add(e)
    return out


def import_dataset(dataset: str, wanted: set[int]) -> int:
    stored = 0
    with tempfile.TemporaryDirectory() as tmp:
        t0 = time.time()
        subprocess.run(["uv", "run", "kaggle", "datasets", "download", "-d", dataset, "-p", tmp, "--force"],
                       cwd=ROOT, check=True, capture_output=True)
        archives = list(Path(tmp).glob("*.zip"))
        if not archives:
            raise FileNotFoundError(f"{dataset}: no archive downloaded")
        size = archives[0].stat().st_size / 1e6
        with zipfile.ZipFile(archives[0]) as z:
            names = {n for n in z.namelist()}
            for e in sorted(wanted):
                member = next((n for n in (f"{e}.json", f"episodes/{e}.json") if n in names), None)
                if member is None:
                    member = next((n for n in names if n.endswith(f"/{e}.json")), None)
                if member is None:
                    continue
                _store_raw(e, z.read(member))
                stored += 1
        print(f"[daily_bulk] {dataset}: {size:.0f} MB, {stored}/{len(wanted)} wanted games stored, {time.time() - t0:.0f} s", flush=True)
    return stored


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datasets", type=int, default=0, help="stop after this many archives (0 = all)")
    args = ap.parse_args()
    todo = sorted(wanted_by_dataset().items(), key=lambda kv: -len(kv[1]))
    print(f"[daily_bulk] {len(todo)} datasets hold {sum(len(v) for _, v in todo)} missing games", flush=True)
    for i, (dataset, wanted) in enumerate(todo):
        if args.datasets and i >= args.datasets:
            break
        try:
            import_dataset(dataset, wanted)
        except Exception as exc:  # noqa: BLE001 - one bad archive must not stop the rest
            print(f"[daily_bulk] {dataset}: failed: {exc!r}", flush=True)


if __name__ == "__main__":
    main()
