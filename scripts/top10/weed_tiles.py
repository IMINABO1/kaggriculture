"""Tile-level history of every weed on a studied seat's farm, from full replays.

    uv run python scripts/top10/weed_tiles.py --per-team 8 --teams "Majkel1337,DSM,..."

For each sampled current-submission game of the listed teams (or every profiled team), open
the replay and follow every tile of the studied seat's farm turn by turn. A weed event starts
when a tile becomes WEED (either spawned on an empty tile or decayed from a plant) and ends
when the tile stops being WEED. Per event: the day and turn it appeared, whether it was a
spawn or a decay, how many turns it stood, whether it was cleared by the end, what the tile
held before and what it was used for afterwards, and how many empty unlocked tiles the farm
had at that day end. Writes data/top10/weed_events.parquet.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor

import pandas as pd

import research  # noqa: F401
from research.kaggle_api import load_replay, replay_path
from research.paths import TOP10


def tile_kind(tile) -> str:
    if tile is None:
        return "empty"
    if tile == "LOCKED":
        return "locked"
    if tile.get("kind") == "WEED":
        return "weed"
    if tile.get("kind") == "PLANT":
        return "plant_" + tile["crop"].lower()
    if tile.get("animal"):
        return "animal_" + tile["animal"].lower()
    return tile.get("kind", "?").lower() + "_empty"


def events_for(episode_id: int, seat: int, team: str, tpd: int = 24) -> list[dict]:
    replay = load_replay(episode_id)
    steps = replay["steps"]
    n = len(steps)
    board = len(steps[0][0]["observation"]["farms"][seat]["tiles"])
    prev = [[tile_kind(t) for t in row] for row in steps[0][0]["observation"]["farms"][seat]["tiles"]]
    open_events: dict[tuple[int, int], dict] = {}
    done: list[dict] = []
    empties_by_day: dict[int, int] = {}
    for t in range(1, n):
        farm = steps[t][0]["observation"]["farms"][seat]
        tiles = farm["tiles"]
        day = t // tpd
        cur = [[tile_kind(x) for x in row] for row in tiles]
        if t % tpd == tpd - 1 or t == n - 1:
            empties_by_day[day] = sum(1 for row in cur for k in row if k == "empty")
        for y in range(board):
            for x in range(board):
                a, b = prev[y][x], cur[y][x]
                if a == b:
                    continue
                key = (x, y)
                if b == "weed":
                    open_events[key] = {
                        "episode_id": episode_id,
                        "seat": seat,
                        "team": team,
                        "x": x,
                        "y": y,
                        "quadrant": ("N" if y < board // 2 else "S") + ("W" if x < board // 2 else "E"),
                        "start_turn": t,
                        "start_day": day,
                        "origin": "spawn" if a == "empty" else ("decay" if a.startswith("plant_") else a),
                        "before": a,
                    }
                elif a == "weed" and key in open_events:
                    ev = open_events.pop(key)
                    ev.update(end_turn=t, end_day=day, cleared=True, after=b, stood_turns=t - ev["start_turn"])
                    done.append(ev)
        prev = cur
    last_day = (n - 1) // tpd
    for ev in open_events.values():
        ev.update(end_turn=n - 1, end_day=last_day, cleared=False, after="weed", stood_turns=n - 1 - ev["start_turn"])
        done.append(ev)
    # what the tile became after clearing: look ahead to the first non-empty kind within the game
    for ev in done:
        ev["empties_at_start_dayend"] = empties_by_day.get(ev["start_day"])
        if ev["cleared"]:
            x, y = ev["x"], ev["y"]
            use = "never"
            for t in range(ev["end_turn"], n):
                k = tile_kind(steps[t][0]["observation"]["farms"][seat]["tiles"][y][x])
                if k not in ("empty", "weed"):
                    use = k
                    ev["reused_after_turns"] = t - ev["end_turn"]
                    break
            ev["reuse"] = use
        else:
            ev["reuse"] = "uncleared"
    return done


def one(args) -> list[dict]:
    episode_id, seat, team = args
    if not replay_path(episode_id).exists():
        return []
    try:
        return events_for(episode_id, seat, team)
    except Exception as exc:  # keep the batch alive; report the failure as a row
        return [{"episode_id": episode_id, "seat": seat, "team": team, "error": repr(exc)}]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--per-team", type=int, default=8)
    ap.add_argument("--teams", default="", help="comma-separated team names; default every profiled team")
    ap.add_argument("--jobs", type=int, default=1)
    args = ap.parse_args()
    feats = pd.read_parquet(TOP10 / "features.parquet")
    cur = feats[feats.is_current_sub == True]  # noqa: E712
    if args.teams:
        names = [s.strip() for s in args.teams.split(",")]
        cur = cur[cur.team.isin(names)]
    picks = []
    for team, g in cur.groupby("team"):
        g = g.sort_values("episode_id")
        picks += [(int(r.episode_id), int(r.seat), team) for r in g.head(args.per_team).itertuples()]
    print(f"{len(picks)} games", flush=True)
    rows = []
    with ProcessPoolExecutor(args.jobs) as pool:
        for i, out in enumerate(pool.map(one, picks)):
            rows.extend(out)
            if i % 10 == 0:
                print(f"{i}/{len(picks)} games, {len(rows)} events", flush=True)
    df = pd.DataFrame(rows)
    df.to_parquet(TOP10 / "weed_events.parquet", index=False)
    print(f"wrote {len(df)} events for {df.episode_id.nunique()} games")


if __name__ == "__main__":
    main()
