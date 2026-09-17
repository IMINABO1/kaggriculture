"""Diagnose the clone in one recorded game: our ops, harvests, unfed animals and money per day
against the recording's, plus the clone's decision counters.

    KAGG_POLICY=clone KAGG_OPENING=tfc KAGG_TAPE_DAYS=0 uv run python scripts/learn/clone_diag.py --team "THIRD FARM CLUB" --index 0
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}


def day_stats(steps, seat, day, action_at):
    ops = Counter()
    harvest = Counter()
    for h in range(24):
        t = day * 24 + h
        if t + 1 >= len(steps):
            break
        farm = steps[t][0]["observation"]["farms"][seat] if isinstance(steps[t][0], dict) else steps[t][0].observation["farms"][seat]
        action = action_at(t)
        poss = [farm["farmer"]] + list(farm["hands"])
        acts = [action.get("farmer")] + list(action.get("hands") or [])
        for i, a in enumerate(acts):
            if not a or i >= len(poss):
                continue
            op = a[0]
            ops["move" if op in MOVES else op] += 1
            if op == "HARVEST":
                x, y = poss[i]
                tile = farm["tiles"][y][x]
                if isinstance(tile, dict):
                    harvest[(tile.get("crop") or tile.get("animal"))[:3]] += int(tile.get("yield_units", 0))
    end = steps[min(len(steps) - 1, day * 24 + 23)][0]
    end = end["observation"] if isinstance(end, dict) else end.observation
    farm = end["farms"][seat]
    unfed = sum(1 for row in farm["tiles"] for t in row if isinstance(t, dict) and "animal" in t and not t["fed_today"])
    unwatered = sum(1 for row in farm["tiles"] for t in row if isinstance(t, dict) and t.get("kind") == "PLANT" and not t["watered_today"])
    weeds = sum(1 for row in farm["tiles"] for t in row if isinstance(t, dict) and t.get("kind") == "WEED")
    animals = sum(1 for row in farm["tiles"] for t in row if isinstance(t, dict) and "animal" in t)
    crops = Counter(t["crop"][:3] for row in farm["tiles"] for t in row if isinstance(t, dict) and t.get("kind") == "PLANT")
    crops["emp"] = sum(1 for row in farm["tiles"] for t in row if t is None)
    for row in farm["tiles"]:
        for t in row:
            if isinstance(t, dict) and "animal" in t:
                crops[t["animal"][:3]] += 1
            elif isinstance(t, dict) and t.get("kind") in ("PASTURE", "COOP"):
                crops["pen0"] += 1
    shed = end["private"]["shed"] if "private" in end else {}
    for a in ("COW", "SHEEP", "GOOSE"):
        if shed.get(a, 0):
            crops[f"shed_{a[:3]}"] = shed[a]
    seeds = Counter()
    for h in range(24):
        t = day * 24 + h
        if t + 1 >= len(steps):
            break
        for order in action_at(t).get("market") or []:
            if order and order[0] == "BUY_SEED" and len(order) > 2:
                seeds[order[1][:3]] += int(order[2])
    return ops, harvest, unfed, unwatered, weeds, animals, farm["money"], dict(crops), dict(seeds)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--team", default="THIRD FARM CLUB")
    ap.add_argument("--index", type=int, default=0, help="which of the team's latest games")
    ap.add_argument("--days", default="6,8,10,12,15,18,21,24,27,29")
    args = ap.parse_args()
    import pandas as pd

    from kenv import import_ke

    ke = import_ke()
    from kaggle_environments.agent import get_last_callable
    from kaggle_environments.utils import structify

    import agent.policy as policy
    from agent.tape import Tape, actions_from_replay
    from arena import patch_town
    from research.encode import FEATURES
    from research.kaggle_api import load_replay

    h = pd.read_parquet(ROOT / "data/gold/history.parquet")
    h["create_time"] = pd.to_datetime(h["create_time"])
    enc = set(pd.read_csv(FEATURES / "manifest.csv").episode_id.astype(int))
    mine = h[(h.team_name == args.team) & (h.is_current_sub == True) & (h.episode_id.astype(int).isin(enc))].drop_duplicates("episode_id")
    row = mine.sort_values("create_time", ascending=False).iloc[args.index]
    ep, seat = int(row.episode_id), int(row.seat)
    replay = load_replay(ep)
    seed = replay["info"]["seed"]
    patch_town(seed, list(replay["steps"][-1][0]["observation"]["town"]["unlocked_shops"]))
    opp = Tape(actions_from_replay(replay, 1 - seat))
    main_py = ROOT / "main.py"
    agent = get_last_callable(main_py.read_text(encoding="utf-8"), path=str(main_py))
    env = ke.make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    shared = env._Environment__get_shared_state
    ours = []
    while not env.done:
        actions = [None, None]
        for i in (0, 1):
            obs = structify(shared(i).observation)
            actions[i] = agent(obs, env.configuration) if i == seat else opp(obs, env.configuration)
        ours.append(actions[seat])
        env.step(actions)
    rec = actions_from_replay(replay, seat)
    print(f"game {ep} seat {seat} vs {row.opp_team_name}: our bank {env.steps[-1][seat].reward:.0f}, recorded {replay['rewards'][seat]:.0f}; "
          f"opponent {env.steps[-1][1 - seat].reward:.0f}, recorded {replay['rewards'][1 - seat]:.0f}")
    keys = ["WATER", "HARVEST", "FERTILIZE", "FEED", "CARE", "COLLECT_FERTILIZER", "PLANT", "DIG", "PICKUP", "DROP", "PLACE", "move", "PASS"]
    for d in [int(x) for x in args.days.split(",")]:
        o_ops, o_h, o_unfed, o_unw, o_weed, o_an, o_money, o_crops, o_seeds = day_stats(env.steps, seat, d, lambda t: ours[t] if t < len(ours) else {})
        r_ops, r_h, r_unfed, r_unw, r_weed, r_an, r_money, r_crops, r_seeds = day_stats(replay["steps"], seat, d, lambda t: rec[t] if t < len(rec) else {})
        print(f"day {d:>2} ours: " + " ".join(f"{k[:4]}{o_ops.get(k, 0)}" for k in keys) + f" | harvest {dict(o_h)} | unfed {o_unfed} unwatered {o_unw} weeds {o_weed} animals {o_an} money {o_money:.0f} | crops {o_crops} seeds bought {o_seeds}")
        print(f"       rec:  " + " ".join(f"{k[:4]}{r_ops.get(k, 0)}" for k in keys) + f" | harvest {dict(r_h)} | unfed {r_unfed} unwatered {r_unw} weeds {r_weed} animals {r_an} money {r_money:.0f} | crops {r_crops} seeds bought {r_seeds}")
    st = policy._GAMES.get(seat, {}).get("clone_stats")
    print("clone counters:", st)


if __name__ == "__main__":
    main()
