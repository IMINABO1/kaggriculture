"""Encode the replay store into learning arrays, incrementally, as the pull grows.

    KAGG_WORKSPACE=data/gold uv run python scripts/learn/featurise.py --jobs 2 [--limit N] [--watch 600]

Every episode listed in <workspace>/history.parquet whose replay is on disk and whose
encoding (data/features/<episode_id>.npz, research/encode.py) is not gets encoded, newest
first. Each success appends a row to data/features/manifest.csv; each failure a line to
data/features/failures.txt. With --watch the scan repeats every N seconds so the runner can
follow the pull; without it one pass is made. Resumable: rerun and it continues.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research.encode import FEATURES, feature_path  # noqa: E402

MANIFEST = FEATURES / "manifest.csv"
FAILURES = FEATURES / "failures.txt"
FIELDS = ["episode_id", "seed", "team0", "team1", "bank0", "bank1", "status0", "status1", "engine", "steps",
          "create_time", "secs", "bytes"]


def encode_one(task: dict) -> dict:
    from research.encode import encode_replay, save_encoded
    from research.kaggle_api import load_replay

    ep = task["episode_id"]
    t0 = time.time()
    try:
        replay = load_replay(ep)
        arrays = encode_replay(replay)
        out = save_encoded(arrays, feature_path(ep))
        meta = json.loads(str(arrays["meta"]))
        return {
            "episode_id": ep, "seed": meta["seed"], "team0": meta["teams"][0] if meta["teams"] else "",
            "team1": meta["teams"][1] if len(meta["teams"]) > 1 else "",
            "bank0": meta["rewards"][0] if meta["rewards"] else "", "bank1": meta["rewards"][1] if len(meta["rewards"]) > 1 else "",
            "status0": meta["statuses"][0] if meta["statuses"] else "", "status1": meta["statuses"][1] if len(meta["statuses"]) > 1 else "",
            "engine": meta["engine"], "steps": meta["steps"], "create_time": task.get("create_time", ""),
            "secs": round(time.time() - t0, 2), "bytes": out.stat().st_size,
        }
    except Exception:  # noqa: BLE001 - one bad replay must not stop the pass
        return {"episode_id": ep, "error": traceback.format_exc(limit=3).strip().splitlines()[-1]}


def pending(limit: int) -> list[dict]:
    import pandas as pd

    from research.kaggle_api import replay_path
    from research.paths import TOP10

    hist = pd.read_parquet(TOP10 / "history.parquet", columns=["episode_id", "create_time"])
    hist = hist.drop_duplicates("episode_id").sort_values("create_time", ascending=False)
    failed = set()
    if FAILURES.exists():
        failed = {int(line.split(",")[0]) for line in FAILURES.read_text(encoding="utf-8").splitlines() if line.strip()}
    out = []
    for ep, ct in zip(hist.episode_id.astype(int), hist.create_time.astype(str)):
        if ep in failed or feature_path(ep).exists() or not replay_path(ep).exists():
            continue
        out.append({"episode_id": ep, "create_time": ct})
        if limit and len(out) >= limit:
            break
    return out


def one_pass(jobs: int, limit: int) -> int:
    todo = pending(limit)
    stamp = time.strftime("%H:%M:%SZ", time.gmtime())
    done = sum(1 for _ in FEATURES.glob("*.npz")) if FEATURES.exists() else 0
    print(f"[featurise] {stamp} {done} encoded, {len(todo)} to do", flush=True)
    if not todo:
        return 0
    FEATURES.mkdir(parents=True, exist_ok=True)
    new = not MANIFEST.exists()
    n_ok = n_err = 0
    t0 = time.time()
    with MANIFEST.open("a", newline="", encoding="utf-8") as fh, ProcessPoolExecutor(max_workers=jobs) as pool:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for r in pool.map(encode_one, todo, chunksize=4):
            if "error" in r:
                n_err += 1
                with FAILURES.open("a", encoding="utf-8") as ff:
                    ff.write(f"{r['episode_id']},{r['error']}\n")
                continue
            w.writerow(r)
            fh.flush()
            n_ok += 1
            if n_ok % 100 == 0:
                rate = n_ok / max(1e-9, time.time() - t0)
                print(f"[featurise] {n_ok} encoded, {n_err} failed, {rate * 60:.0f}/min", flush=True)
    print(f"[featurise] pass done: {n_ok} encoded, {n_err} failed in {time.time() - t0:.0f} s", flush=True)
    return n_ok + n_err


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0, help="episodes per pass (0 = all pending)")
    ap.add_argument("--watch", type=int, default=0, help="seconds between passes (0 = one pass)")
    args = ap.parse_args()
    while True:
        n = one_pass(args.jobs, args.limit)
        if not args.watch:
            break
        if n == 0:
            time.sleep(args.watch)


if __name__ == "__main__":
    main()
