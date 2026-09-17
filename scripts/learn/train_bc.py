"""Train the per-unit behaviour-cloning policy on encoded gold games.

    .venv-learn/Scripts/python.exe scripts/learn/train_bc.py --games 2000 --epochs 1 --seat gold

Runs in the learning venv (torch, CUDA 12.8; see journal 2026-09-17), not the project venv.
Games come from data/features/manifest.csv; --seat gold keeps the gold team's seat of each
game (from the gold workspace's history), --seat both keeps both. The last --holdout games
of the shuffled list are never trained on and give the reported op accuracy. Saves the
model and a metrics line to data/features/bc/.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research.bc import N_OPS, batches, build_model  # noqa: E402
from research.encode import FEATURES, OPS  # noqa: E402

OUT = FEATURES / "bc"


def gold_seats(episode_ids: list[int]) -> dict[int, tuple[int, ...]]:
    import pandas as pd

    hist = pd.read_parquet(ROOT / "data/gold/history.parquet", columns=["episode_id", "seat"])
    seats: dict[int, set] = {}
    for ep, seat in zip(hist.episode_id.astype(int), hist.seat.astype(int)):
        seats.setdefault(ep, set()).add(seat)
    return {ep: tuple(sorted(seats.get(ep, {0, 1}))) for ep in episode_ids}


def evaluate(model, device, ids, seats_of, stride, batch_size, limit_batches=200):
    import torch

    model.eval()
    correct = total = 0
    per_op = np.zeros((N_OPS, 2), dtype=np.int64)
    with torch.no_grad():
        for i, (g, s, op, crop) in enumerate(_stream(ids, seats_of, stride, batch_size, seed=1)):
            if i >= limit_batches:
                break
            logits, _ = model(torch.from_numpy(g).to(device), torch.from_numpy(s).to(device))
            pred = logits.argmax(1).cpu().numpy()
            correct += int((pred == op).sum())
            total += len(op)
            for o, p in zip(op, pred):
                per_op[o, 0] += 1
                per_op[o, 1] += int(o == p)
    model.train()
    return correct / max(1, total), per_op


def _stream(ids, seats_of, stride, batch_size, seed):
    by_seats: dict[tuple, list] = {}
    for ep in ids:
        by_seats.setdefault(seats_of[ep], []).append(ep)
    for seats, eps in by_seats.items():
        yield from batches(eps, batch_size, seats=seats, step_stride=stride, seed=seed)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--holdout", type=int, default=50)
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--batch", type=int, default=512)
    ap.add_argument("--stride", type=int, default=1, help="use every n-th step")
    ap.add_argument("--seat", choices=["gold", "both"], default="gold")
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    import torch
    from torch import nn

    device = "cuda" if torch.cuda.is_available() else "cpu"
    rows = list(csv.DictReader((FEATURES / "manifest.csv").open(encoding="utf-8")))
    ids = [int(r["episode_id"]) for r in rows]
    rng = np.random.default_rng(args.seed)
    rng.shuffle(ids)
    ids = ids[: args.games]
    train_ids, hold_ids = ids[: -args.holdout], ids[-args.holdout:]
    seats_of = gold_seats(ids) if args.seat == "gold" else {ep: (0, 1) for ep in ids}
    model = build_model().to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    ce = nn.CrossEntropyLoss()
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"[bc] {device}, {len(train_ids)} train games, {len(hold_ids)} holdout, seat {args.seat}", flush=True)
    step = 0
    t0 = time.time()
    for epoch in range(args.epochs):
        for g, s, op, crop in _stream(train_ids, seats_of, args.stride, args.batch, seed=args.seed + epoch):
            g_t = torch.from_numpy(g).to(device)
            s_t = torch.from_numpy(s).to(device)
            op_t = torch.from_numpy(op).to(device)
            crop_t = torch.from_numpy(crop).to(device)
            logits, crop_logits = model(g_t, s_t)
            loss = ce(logits, op_t)
            plant = crop_t > 0
            if plant.any():
                loss = loss + 0.3 * ce(crop_logits[plant], crop_t[plant])
            opt.zero_grad()
            loss.backward()
            opt.step()
            step += 1
            if step % 200 == 0:
                acc = float((logits.argmax(1) == op_t).float().mean())
                print(f"[bc] epoch {epoch} step {step} loss {loss.item():.3f} batch acc {acc:.3f} ({time.time() - t0:.0f} s)", flush=True)
        acc, per_op = evaluate(model, device, hold_ids, seats_of, args.stride, args.batch)
        detail = {OPS[i - 1] if i else "none": (int(n), round(k / n, 3)) for i, (n, k) in enumerate(per_op) if n}
        print(f"[bc] epoch {epoch} holdout op accuracy {acc:.4f} on {int(per_op[:, 0].sum())} unit-steps; per op {detail}", flush=True)
        torch.save(model.state_dict(), OUT / f"unit_policy_e{epoch}.pt")
        with (OUT / "metrics.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "epoch": epoch, "games": len(train_ids),
                                 "seat": args.seat, "stride": args.stride, "holdout_acc": acc, "per_op": detail}) + "\n")


if __name__ == "__main__":
    main()
