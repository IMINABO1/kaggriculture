"""Evaluate a saved JobNet on the encoded games of named teams, one line per team.

    .venv-learn/Scripts/python.exe scripts/learn/eval_jobs.py data/features/jobs/models/general_e0.pt --teams "DSM,Unknown Mother-Goose,THIRD FARM CLUB,HowardLeeTW" --stride 2 --max-games 150
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "learn"))

from research.encode import FEATURES  # noqa: E402
from research.jobs import jobs_path  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("weights")
    ap.add_argument("--teams", required=True)
    ap.add_argument("--stride", type=int, default=2)
    ap.add_argument("--max-games", type=int, default=150, help="latest games per team")
    ap.add_argument("--current-only", action="store_true")
    args = ap.parse_args()
    import pandas as pd
    import torch

    from train_jobs import CUTOFF, build_model, evaluate

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = build_model().to(device)
    model.load_state_dict(torch.load(args.weights, map_location=device))
    hist = pd.read_parquet(ROOT / "data/gold/history.parquet")
    hist["create_time"] = pd.to_datetime(hist["create_time"])
    hist = hist[hist.create_time <= pd.Timestamp(CUTOFF)]
    enc = set(pd.read_csv(FEATURES / "manifest.csv").episode_id.astype(int))
    for team in [t.strip() for t in args.teams.split(",") if t.strip()]:
        sel = hist[(hist.team_name == team) & hist.episode_id.astype(int).isin(enc)]
        if args.current_only:
            sel = sel[sel.is_current_sub == True]
        sel = sel.drop_duplicates("episode_id").sort_values("create_time", ascending=False).head(args.max_games)
        games = [(int(r.episode_id), int(r.seat)) for r in sel.itertuples() if jobs_path(int(r.episode_id)).exists()]
        t0 = time.time()
        m = evaluate(model, device, games, args.stride, 48, np.random.default_rng(1))
        print(f"{team:<22} games {len(games):>4} unit-steps {m['unit_steps']:>8} dest {m['dest_top1']:.3f} within1 {m['dest_within1']:.3f} "
              f"op|dest {m['op_given_dest']:.3f} joint {m['joint']:.3f} none {m['none_acc']:.3f} ({time.time() - t0:.0f} s)", flush=True)
        with (FEATURES / "jobs" / "eval.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"weights": str(args.weights), "team": team, "games": len(games), **{k: v for k, v in m.items()}}) + "\n")


if __name__ == "__main__":
    main()
