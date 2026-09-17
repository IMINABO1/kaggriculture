"""Day-N snapshots of hybrid-vs-line games and a resume-based evaluator for policy search.

    uv run python scripts/search/resume.py build --seeds 0-19 --day 24 --jobs 6
    uv run python scripts/search/resume.py check            # resumed baseline == full game

A snapshot holds both players' states at hour 0 of the switch day, the line's recorded actions
for the rest of that game (a frozen opponent: it cannot react to a candidate, so the arena
against the live line stays the final gate), and the full game's banks. `evaluate(overrides)`
resumes every snapshot with the given module constants set on agent.executor / plan / market
and returns the mean margin, bank and harvest basket over the suffix.
"""

from __future__ import annotations

import argparse
import json
import pickle
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

SNAPSHOTS = ROOT / "results" / "snapshots"
V41 = ROOT / "agent" / "line_v41.py"
TURNS_PER_DAY = 24


def _line_agent():
    from kaggle_environments.agent import get_last_callable

    return get_last_callable(V41.read_text(encoding="utf-8"), path=str(V41))


def _our_agent():
    from agent.hybrid import act

    return lambda obs, config=None: act(obs, config)


def build_one(task: dict) -> dict:
    from kenv import import_ke

    ke = import_ke()
    from arena import patch_town, parse_seeds  # noqa: F401

    seed, seat, day = task["seed"], task["seat"], task["day"]
    patch_town(seed)
    agents = [None, None]
    agents[seat] = _our_agent()
    agents[1 - seat] = _line_agent()
    env = ke.make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run(agents)
    doc = env.toJSON()
    steps = doc["steps"]
    cut = day * TURNS_PER_DAY
    snap = {
        "seed": seed, "seat": seat, "day": day, "configuration": doc["configuration"],
        "prefix": steps[cut - 1: cut + 1],
        "opp_actions": [s[1 - seat].get("action") or {"farmer": ["PASS"], "hands": [], "market": []} for s in steps[1:]],
        "baseline": doc["rewards"],
    }
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    (SNAPSHOTS / f"d{day}_s{seed}_p{seat}.pkl").write_bytes(pickle.dumps(snap))
    return {"seed": seed, "seat": seat, "banks": doc["rewards"]}


def _apply(overrides: dict) -> None:
    import importlib

    for key, value in overrides.items():
        module_name, attr = key.split(".", 1)
        mod = importlib.import_module(f"agent.{module_name}")
        if "[" in attr:
            name, sub = attr[:-1].split("[")
            target = getattr(mod, name)
            target[int(sub) if isinstance(target, list) else sub] = value
        else:
            setattr(mod, attr, value)


def resume_one(task: dict) -> dict:
    from kenv import import_ke

    ke = import_ke()
    from arena import harvested_units, basket, patch_town
    from agent.tape import Tape

    snap = pickle.loads(Path(task["path"]).read_bytes())
    _apply(task.get("overrides") or {})
    seat = snap["seat"]
    patch_town(snap["seed"])
    cut = snap["day"] * TURNS_PER_DAY
    # the framework numbers steps by the length of its history, so the prefix is padded to
    # the switch step with placeholders; only the last two entries are read
    prefix = [[{}, {}]] * (cut + 1 - len(snap["prefix"])) + snap["prefix"]
    env = ke.make("kaggriculture", configuration=snap["configuration"], info={"seed": snap["seed"]}, steps=prefix, debug=False)
    ours = _our_agent()
    opp = Tape(snap["opp_actions"])
    cfg = env.configuration
    from kaggle_environments.utils import structify

    shared = env._Environment__get_shared_state  # the runner's merge of the shared fields into a seat's view
    while not env.done:
        actions = [None, None]
        for i in (0, 1):
            obs = structify(shared(i).observation)
            actions[i] = ours(obs, cfg) if i == seat else opp(obs, cfg)
        env.step(actions)
    banks = [s.reward for s in env.steps[-1]]
    suffix = [[structify(p) if isinstance(p, dict) else p for p in st] for st in env.steps[cut:]]
    harvest = harvested_units(suffix, seat)
    return {"seed": snap["seed"], "seat": seat, "me": banks[seat], "opp": banks[1 - seat],
            "baseline": snap["baseline"], "basket": basket(harvest), "harvest": harvest}


def evaluate(overrides: dict | None = None, day: int = 24, seeds=None, jobs: int = 6) -> dict:
    paths = sorted(SNAPSHOTS.glob(f"d{day}_s*_p*.pkl"))
    if seeds is not None:
        paths = [p for p in paths if int(p.stem.split("_s")[1].split("_")[0]) in seeds]
    tasks = [{"path": str(p), "overrides": overrides or {}} for p in paths]
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        rows = list(pool.map(resume_one, tasks))
    return {
        "games": len(rows),
        "margin": statistics.mean(r["me"] - r["opp"] for r in rows),
        "bank": statistics.mean(r["me"] for r in rows),
        "opp": statistics.mean(r["opp"] for r in rows),
        "basket": statistics.mean(r["basket"] for r in rows),
        "rows": rows,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "check"])
    ap.add_argument("--seeds", default="0-19")
    ap.add_argument("--day", type=int, default=24)
    ap.add_argument("--jobs", type=int, default=6)
    args = ap.parse_args()
    from arena import parse_seeds

    if args.cmd == "build":
        tasks = [{"seed": s, "seat": p, "day": args.day} for s in parse_seeds(args.seeds) for p in (0, 1)]
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            for r in pool.map(build_one, tasks):
                print(f"snapshot seed {r['seed']} seat {r['seat']}: banks {r['banks']}", flush=True)
    else:
        res = evaluate({}, day=args.day, seeds=set(parse_seeds(args.seeds)), jobs=args.jobs)
        exact = sum(1 for r in res["rows"] if [r["me"], r["opp"]] == [r["baseline"][r["seat"]], r["baseline"][1 - r["seat"]]])
        print(f"resumed {res['games']} games: margin {res['margin']:.0f}, bank {res['bank']:.0f} vs {res['opp']:.0f}, basket {res['basket']:.0f}; exact matches with the full game: {exact}/{res['games']}")
        for r in res["rows"]:
            if [r["me"], r["opp"]] != [r["baseline"][r["seat"]], r["baseline"][1 - r["seat"]]]:
                print(f"  seed {r['seed']} seat {r['seat']}: resumed {r['me']:.0f}/{r['opp']:.0f} vs full {r['baseline']}")


if __name__ == "__main__":
    main()
