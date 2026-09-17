"""Hill-climb the executor's constants against the resume evaluator.

    uv run python scripts/search/climb.py --hours 3 --jobs 6

Each iteration perturbs one or two constants, evaluates the candidate on the search seeds
(0-9, 20 games from the day-24 snapshots, frozen v41), and keeps it only if the mean margin
rises. Every accepted step is also scored on the hold-out seeds (10-19). Everything is
logged to results/search.csv; the incumbent lives in results/search_best.json and is
loaded on start, so the run resumes. The arena against the live lines remains the gate.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from search.resume import evaluate  # noqa: E402

LOG = ROOT / "results" / "search.csv"
BEST = ROOT / "results" / "search_best.json"
SEARCH_SEEDS = set(range(0, 10))
HOLDOUT_SEEDS = set(range(10, 20))

# name -> (kind, low, high, step); "f" float, "i" int
SPACE = {
    "executor.PRIO[FEED]": ("f", -4, 4, 0.5), "executor.PRIO[PLACE]": ("f", -6, 2, 0.5),
    "executor.PRIO[PLANT]": ("f", -3, 5, 0.5), "executor.PRIO[BUILD]": ("f", -5, 3, 0.5),
    "executor.PRIO[WATER]": ("f", -2, 6, 0.5), "executor.PRIO[HARVEST]": ("f", -2, 6, 0.5),
    "executor.PRIO[FERTILIZE]": ("f", -2, 7, 0.5), "executor.PRIO[DIG]": ("f", -2, 7, 0.5),
    "executor.PRIO[CARE]": ("f", -2, 7, 0.5), "executor.PRIO[COLLECT]": ("f", -2, 9, 0.5),
    "executor.PRIO[WATER_SPARE]": ("f", 2, 12, 0.5), "executor.PRIO[WATER_MUST]": ("f", -4, 3, 0.5),
    "executor.HARVEST_PRIO[STRAWBERRY]": ("f", -6, 4, 0.5), "executor.PLANT_PRIO[STRAWBERRY]": ("f", -3, 3, 0.5),
    "executor.PLANT_PRIO[CARROT]": ("f", -3, 4, 0.5), "executor.PLANT_PRIO[WHEAT]": ("f", -3, 5, 0.5),
    "executor.FERTILIZE_PRIO[STRAWBERRY]": ("f", -5, 4, 0.5), "executor.FERTILIZE_PRIO[WHEAT]": ("f", -3, 7, 0.5),
    "executor.FERTILIZE_PRIO[CARROT]": ("f", -3, 7, 0.5),
    "executor.DEPOSIT_VALUE": ("i", 50, 900, 50), "executor.DEPOSIT_URGENT_VALUE": ("i", 600, 3000, 100),
    "executor.URGENCY_FROM_HOUR": ("i", 6, 20, 1), "executor.URGENCY_PER_HOUR": ("f", 0.0, 2.0, 0.25),
    "executor.ON_TILE_BONUS": ("f", -20, -2, 1.0), "executor.FEED_DEADLINE_HOUR": ("i", 10, 21, 1),
    "executor.FEEDER_LOAD": ("i", 1, 6, 1), "executor.SPARE_WATER_HOUR": ("i", 8, 23, 1),
    "executor.LIQUIDATION_HOUR": ("i", 8, 20, 1), "executor.LATE_HARVEST_HOUR": ("i", 12, 22, 1),
    "executor.STICKY_BONUS": ("f", -6, 0, 0.5), "executor.LAST_PLANT_HOUR": ("i", 16, 22, 1),
    "executor.FEED_DAILY_RATIO": ("f", 0.5, 3.0, 0.1),
    "plan.WHEAT_LAST_DAY": ("i", 22, 27, 1), "plan.CARROT_FIRST_DAY": ("i", 21, 26, 1),
    "plan.CARROT_LAST_DAY": ("i", 24, 28, 1),
    "plan.HANDS_BY_DAY[24]": ("i", 8, 15, 1), "plan.HANDS_BY_DAY[25]": ("i", 8, 15, 1),
    "plan.HANDS_BY_DAY[26]": ("i", 8, 15, 1), "plan.HANDS_BY_DAY[27]": ("i", 8, 15, 1),
    "plan.HANDS_BY_DAY[28]": ("i", 8, 15, 1), "plan.HANDS_BY_DAY[29]": ("i", 6, 15, 1),
    "market.SEED_BUFFER[WHEAT]": ("i", 0, 12, 1), "market.SEED_BUFFER[CARROT]": ("i", 0, 12, 1),
    "market.FEED_BUY_HOUR": ("i", 16, 23, 1), "market.FERTILIZER_RESERVE_CAP": ("i", 0, 60, 4),
    "market.WHEAT_FEED_RESERVE_DAYS": ("i", 0, 3, 1), "market.MIN_SELL_PRICE": ("i", 1, 8, 1),
}
FIELDS = ["ts", "iteration", "accepted", "search_margin", "search_bank", "search_basket", "holdout_margin", "changed", "params"]


def current_values() -> dict:
    import importlib

    out = {}
    for key in SPACE:
        module_name, attr = key.split(".", 1)
        mod = importlib.import_module(f"agent.{module_name}")
        if "[" in attr:
            name, sub = attr[:-1].split("[")
            target = getattr(mod, name)
            out[key] = target[int(sub)] if isinstance(target, list) else target[sub]
        else:
            out[key] = getattr(mod, attr)
    return out


def perturb(params: dict, rng: random.Random) -> dict:
    cand = dict(params)
    for key in rng.sample(list(SPACE), k=rng.choice((1, 1, 2))):
        kind, lo, hi, step = SPACE[key]
        value = min(hi, max(lo, cand[key] + step * rng.choice((-2, -1, 1, 2))))
        cand[key] = int(round(value)) if kind == "i" else round(value, 3)
    return cand


def score(params: dict, seeds: set, jobs: int) -> dict:
    res = evaluate(params, day=24, seeds=seeds, jobs=jobs)
    return {"margin": res["margin"], "bank": res["bank"], "opp": res["opp"], "basket": res["basket"]}


def log_row(row: dict) -> None:
    new = not LOG.exists()
    with LOG.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)


def stamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hours", type=float, default=3.0)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--iterations", type=int, default=0, help="stop after this many (0 = by time)")
    ap.add_argument("--seed", type=int, default=20260917)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    LOG.parent.mkdir(exist_ok=True)
    if BEST.exists():
        best = json.loads(BEST.read_text(encoding="utf-8"))
        params, best_margin = best["params"], best["margin"]
        print(f"[climb] resuming from {BEST.name}: margin {best_margin:.0f}", flush=True)
    else:
        params = current_values()
        base = score(params, SEARCH_SEEDS, args.jobs)
        hold = score(params, HOLDOUT_SEEDS, args.jobs)
        best_margin = base["margin"]
        BEST.write_text(json.dumps({"params": params, "margin": best_margin, "holdout": hold["margin"]}, indent=1), encoding="utf-8")
        print(f"[climb] baseline: search margin {base['margin']:.0f}, holdout {hold['margin']:.0f}, basket {base['basket']:.0f}", flush=True)
        log_row({"ts": stamp(), "iteration": 0, "accepted": 1, "search_margin": base["margin"], "search_bank": base["bank"],
                 "search_basket": base["basket"], "holdout_margin": hold["margin"], "changed": "", "params": json.dumps(params)})
    t_end = time.time() + args.hours * 3600
    it = 0
    while (args.iterations and it < args.iterations) or (not args.iterations and time.time() < t_end):
        it += 1
        cand = perturb(params, rng)
        changed = {k: (params[k], v) for k, v in cand.items() if v != params[k]}
        if not changed:
            continue
        res = score(cand, SEARCH_SEEDS, args.jobs)
        accepted = res["margin"] > best_margin
        hold = score(cand, HOLDOUT_SEEDS, args.jobs) if accepted else None
        log_row({"ts": stamp(), "iteration": it, "accepted": int(accepted), "search_margin": res["margin"],
                 "search_bank": res["bank"], "search_basket": res["basket"],
                 "holdout_margin": hold["margin"] if hold else "", "changed": json.dumps(changed), "params": json.dumps(cand)})
        tail = f" holdout {hold['margin']:.0f}" if hold else ""
        print(f"[climb] it {it}: {'ACCEPT' if accepted else 'reject'} margin {res['margin']:.0f} (best {best_margin:.0f}) changed {changed}{tail}", flush=True)
        if accepted:
            params, best_margin = cand, res["margin"]
            BEST.write_text(json.dumps({"params": params, "margin": best_margin, "holdout": hold["margin"]}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
