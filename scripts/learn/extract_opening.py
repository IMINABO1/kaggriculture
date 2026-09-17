"""Extract a team's modal opening line from its encoded games as a replayable tape.

    uv run python scripts/learn/extract_opening.py --team "THIRD FARM CLUB" --steps 137 --out agent/opening_tfc.py

Walks the steps in order; at each step the action (farmer and hands ops, market orders) is
the most common one among the games still on the line so far, and games that diverge leave
the pool. Prints the pool size at the usual cuts and writes the tape as a Python module
holding ACTIONS (a list of action dicts) and the pool table.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research.encode import CROPS, FEATURES, ITEMS, ORDER_TYPES, decode_unit_action, load_encoded  # noqa: E402
from research.paths import DATA  # noqa: E402

CUTS = (24, 48, 100, 136, 144, 200)


def decode_order(kind: int, item: int, qty: int) -> list | None:
    if kind <= 0:
        return None
    name = ORDER_TYPES[kind - 1]
    if name in ("HIRE", "BUY_LAND"):
        return [name]
    if name == "BUY_SEED":
        return [name, CROPS[item - 1], int(qty)] if item else None
    return [name, ITEMS[item - 1], int(qty)] if item else None


def action_at(z: dict, seat: int, t: int) -> dict:
    n = int(z["n_units"][seat, t])
    ops = [decode_unit_action(int(z["op"][seat, t, u]), int(z["op_arg"][seat, t, u]), int(z["op_count"][seat, t, u])) for u in range(min(n, 20))]
    orders = [decode_order(int(z["m_type"][seat, t, k]), int(z["m_item"][seat, t, k]), int(z["m_qty"][seat, t, k])) for k in range(10)]
    return {"farmer": ops[0] if ops else ["PASS"], "hands": ops[1:], "market": [o for o in orders if o]}


def canon(action: dict) -> str:
    return json.dumps(action, sort_keys=True, separators=(",", ":"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--team", default="THIRD FARM CLUB")
    ap.add_argument("--sub", type=int, default=0, help="submission id (default: the current one)")
    ap.add_argument("--steps", type=int, default=137)
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    hist = pd.read_parquet(DATA / "gold/history.parquet")
    enc = set(pd.read_csv(FEATURES / "manifest.csv").episode_id.astype(int))
    mine = hist[(hist.team_name == args.team) & (hist.episode_id.astype(int).isin(enc))]
    mine = mine[mine["sub"] == args.sub] if args.sub else mine[mine.is_current_sub == True]
    mine = mine.drop_duplicates("episode_id")
    games = [(load_encoded(int(r.episode_id)), int(r.seat), int(r.episode_id)) for r in mine.itertuples()]
    print(f"{args.team} sub {int(mine['sub'].iloc[0])}: {len(games)} games", flush=True)
    pool = list(range(len(games)))
    tape: list[dict] = []
    table = {}
    for t in range(args.steps):
        votes = Counter()
        acts = {}
        for i in pool:
            z, seat, _ = games[i]
            a = action_at(z, seat, t)
            c = canon(a)
            votes[c] += 1
            acts[c] = a
        best, n_best = votes.most_common(1)[0]
        tape.append(acts[best])
        pool = [i for i in pool if canon(action_at(games[i][0], games[i][1], t)) == best]
        if t + 1 in CUTS or t == args.steps - 1:
            table[t + 1] = len(pool)
            print(f"  through turn {t + 1}: {len(pool)} of {len(games)} games on the line ({100 * len(pool) / len(games):.0f}%); {len(votes)} candidates at this step, modal {n_best}", flush=True)
    if args.out:
        out = Path(args.out)
        out.write_text(
            f'"""{args.team}\'s modal opening line, extracted by scripts/learn/extract_opening.py from '
            f'{len(games)} recorded games of submission {int(mine["sub"].iloc[0])}; games on the line by turn: {table}."""\n\n'
            f"ACTIONS = {json.dumps(tape, separators=(',', ':'))}\n",
            encoding="utf-8")
        print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KiB)")


if __name__ == "__main__":
    main()
