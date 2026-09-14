"""Fill rating_before / rating_after in history.parquet from the public episode endpoint.

    uv run python scripts/top10/refresh_ratings.py --budget-min 30

One raw ListEpisodes call returns every game of a submission with both agents' ratings, so a
handful of calls covers the sampled submissions. The endpoint answers 429 with Retry-After
for long stretches, so this runs slowly and stops at the time budget; rerun to continue.
Current submissions first, then older sampled submissions with the fewest known ratings.
"""

from __future__ import annotations

import argparse
import json
import time

import pandas as pd
import requests

from research.kaggle_api import EPISODE_CACHE, LIST_URL
from research.paths import TOP10


def fetch_raw(session: requests.Session, sub: int, deadline: float) -> dict | None:
    while time.time() < deadline:
        resp = session.post(LIST_URL, json={"submissionId": int(sub)}, timeout=30)
        if resp.status_code == 429:
            wait = resp.headers.get("Retry-After")
            time.sleep(float(wait) + 1 if wait and wait.isdigit() else 31)
            continue
        resp.raise_for_status()
        data = resp.json()
        data["source"] = "raw"
        (EPISODE_CACHE / f"raw_{sub}.json").write_text(json.dumps(data), encoding="utf-8")
        return data
    return None


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--budget-min", type=float, default=30)
    args = ap.parse_args()
    deadline = time.time() + args.budget_min * 60

    hist = pd.read_parquet(TOP10 / "history.parquet")
    sample = pd.read_csv(TOP10 / "sample.csv")
    sampled = hist[hist.episode_id.isin(sample.episode_id)]
    known = sampled.groupby("sub").rating_after.apply(lambda s: s.notna().mean())
    current = set(hist[hist.is_current_sub]["sub"])
    order = sorted(known.index, key=lambda s: (s not in current, known[s]))

    session = requests.Session()
    session.headers["User-Agent"] = "kaggriculture-research (IMINABO1)"
    updates = {}
    done = 0
    for sub in order:
        if known[sub] >= 0.99:
            continue
        cached = EPISODE_CACHE / f"raw_{sub}.json"
        data = (
            json.loads(cached.read_text(encoding="utf-8"))
            if cached.exists()
            else fetch_raw(session, sub, deadline)
        )
        if data is None:
            print(f"budget spent after {done} submissions")
            break
        for ep in data.get("episodes", []):
            for a in ep.get("agents", []):
                sid = int(a.get("submissionId") or 0)
                if a.get("updatedScore") is not None:
                    updates[(int(ep["id"]), sid)] = (a.get("initialScore"), a.get("updatedScore"))
        done += 1
        print(f"refreshed sub {sub}: {len(data.get('episodes', []))} episodes", flush=True)

    if not updates:
        print("no updates")
        return
    before = [updates.get((e, s), (None, None))[0] for e, s in zip(hist.episode_id, hist["sub"])]
    after = [updates.get((e, s), (None, None))[1] for e, s in zip(hist.episode_id, hist["sub"])]
    hist["rating_before"] = pd.Series(before, index=hist.index, dtype=float).fillna(
        hist.rating_before
    )
    hist["rating_after"] = pd.Series(after, index=hist.index, dtype=float).fillna(hist.rating_after)
    ob = [updates.get((e, s), (None, None))[0] for e, s in zip(hist.episode_id, hist.opp_sub)]
    oa = [updates.get((e, s), (None, None))[1] for e, s in zip(hist.episode_id, hist.opp_sub)]
    hist["opp_rating_before"] = pd.Series(ob, index=hist.index, dtype=float).fillna(
        hist.opp_rating_before
    )
    hist["opp_rating_after"] = pd.Series(oa, index=hist.index, dtype=float).fillna(
        hist.opp_rating_after
    )
    hist.to_parquet(TOP10 / "history.parquet", index=False)
    covered = hist[hist.episode_id.isin(sample.episode_id)].rating_after.notna().mean()
    print(f"history.parquet updated; sampled games with a rating: {covered:.0%}")


if __name__ == "__main__":
    main()
