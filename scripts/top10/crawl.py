"""Build the full public game history of every team in the latest snapshot.

    uv run python scripts/top10/crawl.py

For each team: seed its submission ids from the community index (data/community/agents.csv),
list every episode of every known submission, and expand the submission set from what those
listings reveal until nothing new appears. Only submissions of snapshot teams are listed.

Listings go through the authenticated Kaggle client (fast, never throttled so far). It does
not return ratings, so ratings are joined from the community index (episodes.csv, which
carries the rating after each game) and from any cached raw-endpoint payloads. The rating
before a game is the same submission's rating after its previous game.

Outputs:
  data/top10/history.parquet  one row per (submission, episode) of a snapshot team
  data/top10/teams.csv        per team: current submission, submissions found vs declared
"""

from __future__ import annotations

from collections import defaultdict

import pandas as pd

from research.kaggle_api import list_episodes
from research.paths import COMMUNITY, TOP10


def main() -> None:
    snap = pd.read_csv(TOP10 / "snapshot_latest.csv")
    targets = {int(t): n for t, n in zip(snap.team_id, snap.team_name)}

    agents = pd.read_csv(COMMUNITY / "agents.csv")
    known: dict[int, set[int]] = defaultdict(set)
    seeds = agents[agents.team_id.isin(targets)][["team_id", "submission_id"]]
    for team_id, sub in seeds.itertuples(index=False):
        known[int(team_id)].add(int(sub))

    team_info: dict[int, dict] = {}
    listed: dict[int, dict] = {}
    sub_team = {s: t for t, subs in known.items() for s in subs}
    queue = sorted(sub_team)
    while queue:
        sub = queue.pop(0)
        if sub in listed:
            continue
        data = list_episodes(sub, prefer_client=True)
        listed[sub] = data
        for t in data.get("teams", []):
            if int(t["id"]) in targets:
                team_info[int(t["id"])] = t
        discovered = [
            (int(s.get("teamId", 0)), int(s["id"])) for s in data.get("submissions", [])
        ] + [
            (int(a.get("teamId") or 0), int(a.get("submissionId") or 0))
            for ep in data.get("episodes", [])
            for a in ep.get("agents", [])
        ]
        for team_id, sid in discovered:
            if team_id in targets and sid and sid not in listed and sid not in sub_team:
                known[team_id].add(sid)
                sub_team[sid] = team_id
                queue.append(sid)
        print(
            f"listed sub {sub} ({targets.get(sub_team.get(sub), '?')}): "
            f"{len(data.get('episodes', []))} episodes; queue {len(queue)}",
            flush=True,
        )

    rows = []
    for sub, data in listed.items():
        team_id = sub_team[sub]
        for ep in data.get("episodes", []):
            agents_ = ep.get("agents", [])
            mine = [a for a in agents_ if int(a.get("submissionId") or 0) == sub]
            if len(mine) != 1 or len(agents_) != 2:
                continue
            me = mine[0]
            opp = next(a for a in agents_ if a is not me)
            bank, opp_bank = me.get("reward"), opp.get("reward")
            rows.append(
                {
                    "team_id": team_id,
                    "team_name": targets[team_id],
                    "sub": sub,
                    "episode_id": int(ep["id"]),
                    "create_time": ep.get("createTime"),
                    "end_time": ep.get("endTime"),
                    "type": ep.get("type"),
                    "state": ep.get("state"),
                    "seat": int(me.get("index") or 0),
                    "bank": bank,
                    "rating_before": me.get("initialScore"),
                    "rating_after": me.get("updatedScore"),
                    "opp_sub": int(opp.get("submissionId") or 0),
                    "opp_team_id": int(opp.get("teamId") or 0),
                    "opp_team_name": opp.get("teamName"),
                    "opp_bank": opp_bank,
                    "opp_rating_before": opp.get("initialScore"),
                    "opp_rating_after": opp.get("updatedScore"),
                    "result": None
                    if bank is None or opp_bank is None
                    else "W"
                    if bank > opp_bank
                    else "L"
                    if bank < opp_bank
                    else "T",
                }
            )
    hist = pd.DataFrame(rows)
    hist["create_time"] = pd.to_datetime(hist.create_time, utc=True, format="mixed")
    hist["end_time"] = pd.to_datetime(hist.end_time, utc=True, format="mixed")
    hist = hist.sort_values(["team_id", "create_time", "episode_id"]).reset_index(drop=True)

    comm = pd.read_csv(
        COMMUNITY / "episodes.csv",
        usecols=["episode_id", "sub_0", "rating_0", "sub_1", "rating_1"],
    )
    after = {}
    for e, s0, r0, s1, r1 in comm.itertuples(index=False):
        after[(int(e), int(s0))] = r0
        after[(int(e), int(s1))] = r1
    hist["rating_after"] = hist.rating_after.astype(float)
    hist["opp_rating_after"] = hist.opp_rating_after.astype(float)
    fill = [after.get((e, s)) for e, s in zip(hist.episode_id, hist["sub"])]
    hist["rating_after"] = hist.rating_after.fillna(pd.Series(fill, index=hist.index, dtype=float))
    fill = [after.get((e, s)) for e, s in zip(hist.episode_id, hist.opp_sub)]
    hist["opp_rating_after"] = hist.opp_rating_after.fillna(
        pd.Series(fill, index=hist.index, dtype=float)
    )
    hist["rating_before"] = hist.rating_before.astype(float)
    shifted = hist.groupby("sub").rating_after.shift(1)
    hist["rating_before"] = hist.rating_before.fillna(shifted)
    hist["opp_rating_before"] = hist.opp_rating_before.astype(float)
    hist["opp_rating_before"] = hist.opp_rating_before.fillna(hist.opp_rating_after)

    current = {}
    current_source = {}
    for t in targets:
        info = team_info.get(t, {})
        if info.get("publicLeaderboardSubmissionId"):
            current[t] = int(info["publicLeaderboardSubmissionId"])
            current_source[t] = "leaderboard"
        else:
            h = hist[(hist.team_id == t) & (hist.type == "EPISODE_TYPE_PUBLIC")]
            if len(h):
                current[t] = int(h.sort_values("create_time")["sub"].iloc[-1])
                current_source[t] = "latest-episode"
    hist["is_current_sub"] = [s == current.get(t) for t, s in zip(hist.team_id, hist["sub"])]
    hist.to_parquet(TOP10 / "history.parquet", index=False)

    teams = []
    for _, r in snap.iterrows():
        t = int(r.team_id)
        info = team_info.get(t, {})
        h = hist[(hist.team_id == t) & (hist.type == "EPISODE_TYPE_PUBLIC")]
        teams.append(
            {
                "rank": int(r["rank"]),
                "team_id": t,
                "team_name": r.team_name,
                "score": r.score,
                "snapshot": r.get("snapshot"),
                "current_sub": current.get(t),
                "current_sub_source": current_source.get(t),
                "subs_found": len(known[t]),
                "subs_declared": info.get("submissionCount"),
                "public_games": len(h),
                "first_game": h.create_time.min() if len(h) else None,
                "last_game": h.create_time.max() if len(h) else None,
                "current_sub_games": int((h["sub"] == current.get(t)).sum()),
                "games_with_rating": int(h.rating_after.notna().sum()),
            }
        )
    teams_df = pd.DataFrame(teams)
    teams_df.to_csv(TOP10 / "teams.csv", index=False)
    print()
    print(teams_df.to_string(index=False))
    print(f"\nhistory.parquet: {len(hist)} rows, {len(listed)} submissions listed")


if __name__ == "__main__":
    main()
