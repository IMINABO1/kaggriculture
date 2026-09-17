"""Replay our agent (main.py, with the KAGG_* overrides from the environment) in the recorded seat
of a team's current-submission games: the opponent's stream as a tape, the town as recorded.
Reports the first day the tile census differs from the recording, the banks against the
recorded banks, and the win count.

    KAGG_POLICY=clone KAGG_OPENING=tfc KAGG_TAPE_DAYS=0 uv run python scripts/learn/fidelity.py --team "THIRD FARM CLUB" --n 10 --jobs 3
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))


def census(tiles) -> dict:
    out: dict = {}
    for row in tiles:
        for t in row:
            k = "empty" if t is None else "locked" if t == "LOCKED" else (t.get("crop") or t.get("animal") or t.get("kind"))
            out[k] = out.get(k, 0) + 1
    return out


def run_one(task: dict) -> dict:
    from kenv import import_ke

    ke = import_ke()
    from kaggle_environments.agent import get_last_callable
    from kaggle_environments.utils import structify

    from agent.tape import Tape, actions_from_replay
    from arena import patch_town
    from research.kaggle_api import load_replay

    ep, seat = task["ep"], task["seat"]
    replay = load_replay(ep)
    seed = replay["info"]["seed"]
    patch_town(seed, list(replay["steps"][-1][0]["observation"]["town"]["unlocked_shops"]))
    opp = Tape(actions_from_replay(replay, 1 - seat))
    main_py = ROOT / "main.py"
    agent = get_last_callable(main_py.read_text(encoding="utf-8"), path=str(main_py))
    env = ke.make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    shared = env._Environment__get_shared_state
    cfg = env.configuration
    t, first_census_day, money_diff = 0, None, {}
    while not env.done:
        actions = [None, None]
        for i in (0, 1):
            obs = structify(shared(i).observation)
            if i == seat and t % 24 == 0:
                rec_farm = replay["steps"][t][0]["observation"]["farms"][seat]
                if first_census_day is None and census(obs["farms"][seat]["tiles"]) != census(rec_farm["tiles"]):
                    first_census_day = t // 24
                if t % 120 == 0:
                    money_diff[t // 24] = int(obs["farms"][seat]["money"] - rec_farm["money"])
            try:
                actions[i] = agent(obs, cfg) if i == seat else opp(obs, cfg)
            except Exception as exc:  # noqa: BLE001
                actions[i] = {"farmer": ["PASS"], "hands": [], "market": []}
                money_diff.setdefault("error", f"{t}:{exc!r}"[:60])
        env.step(actions)
        t += 1
    banks = [s.reward for s in env.steps[-1]]
    return {"ep": ep, "seat": seat, "first_census_day": first_census_day, "money_diff_by_day": money_diff,
            "bank": banks[seat], "rec_bank": replay["rewards"][seat], "opp_bank": banks[1 - seat], "rec_opp": replay["rewards"][1 - seat]}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--team", default="THIRD FARM CLUB")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    import pandas as pd

    from research.encode import FEATURES

    h = pd.read_parquet(ROOT / "data/gold/history.parquet")
    h["create_time"] = pd.to_datetime(h["create_time"])
    enc = set(pd.read_csv(FEATURES / "manifest.csv").episode_id.astype(int))
    mine = h[(h.team_name == args.team) & (h.is_current_sub == True) & (h.episode_id.astype(int).isin(enc))].drop_duplicates("episode_id")
    mine = mine.sort_values("create_time", ascending=False).head(args.n)
    tasks = [{"ep": int(r.episode_id), "seat": int(r.seat)} for r in mine.itertuples()]
    rows = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for r in pool.map(run_one, tasks):
            rows.append(r)
            if not args.quiet:
                print(json.dumps(r), flush=True)
    ratio = [r["bank"] / r["rec_bank"] for r in rows if r["rec_bank"]]
    opp_ratio = [r["opp_bank"] / r["rec_opp"] for r in rows if r["rec_opp"]]
    days = [r["first_census_day"] for r in rows if r["first_census_day"] is not None]
    print(f"{len(rows)} games: bank/recorded median {statistics.median(ratio):.2f}, opponent bank/recorded median {statistics.median(opp_ratio):.2f}, "
          f"first census difference median day {statistics.median(days) if days else None}, wins {sum(1 for r in rows if r['bank'] > r['opp_bank'])}, "
          f"mean bank {statistics.mean(r['bank'] for r in rows):.0f} vs recorded {statistics.mean(r['rec_bank'] for r in rows):.0f}", flush=True)


if __name__ == "__main__":
    main()
