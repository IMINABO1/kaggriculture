"""Fill rating_before / rating_after in history.parquet from the public episode endpoint.

    uv run python scripts/top10/refresh_ratings.py --budget-min 30

One raw ListEpisodes call returns every game of a submission with both agents' ratings, so a
handful of calls covers the sampled submissions. The endpoint answers 429 with Retry-After
for long stretches, so this runs slowly and stops at the time budget; rerun to continue.
Current submissions first, then older sampled submissions with the fewest known ratings.

The raw payload also carries each team's publicLeaderboardSubmissionId, which the client
listing does not. Teams whose current submission was guessed from their latest episode
(`current_sub_source = latest-episode` in teams.csv) are corrected from it, so run this
before sample.py when the crawl reported such teams.
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
    teams = pd.read_csv(TOP10 / "teams.csv")
    sample_path = TOP10 / "sample.csv"
    sampled = (
        hist[hist.episode_id.isin(pd.read_csv(sample_path).episode_id)]
        if sample_path.exists()
        else hist[hist.is_current_sub]
    )
    known = sampled.groupby("sub").rating_after.apply(lambda s: s.notna().mean())
    current = set(hist[hist.is_current_sub]["sub"])
    guessed = set(teams[teams.current_sub_source == "latest-episode"].current_sub.dropna())
    frozen = set(teams[teams.current_sub_source == "frozen"].current_sub.dropna())
    current |= frozen
    for sub in guessed:
        known[sub] = known.get(sub, 0.0)
    order = sorted(known.index, key=lambda s: (s not in guessed, s not in current, known[s]))

    session = requests.Session()
    session.headers["User-Agent"] = "kaggriculture-research (IMINABO1)"
    updates = {}
    leaderboard_sub: dict[int, int] = {}
    done = 0
    for sub in order:
        if known[sub] >= 0.99 and sub not in guessed:
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
        for t in data.get("teams", []):
            if t.get("publicLeaderboardSubmissionId"):
                leaderboard_sub[int(t["id"])] = int(t["publicLeaderboardSubmissionId"])
        done += 1
        print(f"refreshed sub {sub}: {len(data.get('episodes', []))} episodes", flush=True)

    fixed = 0
    for i, r in teams.iterrows():
        real = leaderboard_sub.get(int(r.team_id))
        if r.current_sub_source in ("leaderboard", "frozen") or real is None:
            continue
        if real != int(r.current_sub):
            print(f"current submission of {r.team_name}: {int(r.current_sub)} -> {real}")
            fixed += 1
        teams.loc[i, "current_sub"] = real
        teams.loc[i, "current_sub_source"] = "leaderboard"
        h = hist[(hist.team_id == r.team_id) & (hist.type == "EPISODE_TYPE_PUBLIC")]
        teams.loc[i, "current_sub_games"] = int((h["sub"] == real).sum())
    if leaderboard_sub:
        teams.to_csv(TOP10 / "teams.csv", index=False)
        current_of = dict(zip(teams.team_id, teams.current_sub))
        hist["is_current_sub"] = [s == current_of.get(t) for t, s in zip(hist.team_id, hist["sub"])]
        print(f"teams.csv: {fixed} current submissions corrected")

    if not updates:
        if leaderboard_sub:
            hist.to_parquet(TOP10 / "history.parquet", index=False)
        print("no rating updates")
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
    covered = hist[hist.episode_id.isin(sampled.episode_id)].rating_after.notna().mean()
    print(f"history.parquet updated; sampled games with a rating: {covered:.0%}")


if __name__ == "__main__":
    main()
