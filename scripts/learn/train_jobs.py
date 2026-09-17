"""Train the job-level clone: for each unit at each step, where it goes next and what it does there.

    .venv-learn/Scripts/python.exe scripts/learn/train_jobs.py --team "THIRD FARM CLUB" --holdout 25 --epochs 6 --name tfc
    .venv-learn/Scripts/python.exe scripts/learn/train_jobs.py --split team --train-teams "Majkel1337,SpaTaro,..." --test-teams "DSM,..." --stride 2 --name general

Runs in the learning venv. Games come from data/features/manifest.csv joined to the gold
history (the team's seat); labels from data/features/jobs (scripts/learn/build_jobs.py).
--team: the team's current submission, the last --holdout games by create_time held out.
--split team: every encoded game of the training teams up to the cutoff, tested on the test
teams only. Metrics per epoch go to data/features/jobs/metrics.jsonl; weights to
data/features/jobs/models/<name>_e<epoch>.pt.
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

from agent.clone_feats import MAX_UNITS, N_PLANES, N_SCALARS, N_UNIT, destination_mask, step_planes, step_scalars, unit_vector  # noqa: E402
from research.encode import FEATURES, load_encoded  # noqa: E402
from research.jobs import N_CLASSES, WORK_OPS, jobs_path, load_labels  # noqa: E402

OUT = FEATURES / "jobs"
CUTOFF = "2026-09-17T03:23:00Z"
ARG_OPS = {WORK_OPS.index(o) + 1 for o in ("PLANT", "PICKUP", "PLACE")}
COUNT_OPS = {WORK_OPS.index(o) + 1 for o in ("PICKUP", "PLACE")}
N_ARG = 13
N_COUNT = 13


def game_arrays(ep: int, seat: int, stride: int) -> dict:
    z = load_encoded(ep)
    lab = load_labels(ep)
    T = lab["lab_op"].shape[1]
    steps = list(range(0, T, stride))
    S = len(steps)
    planes = np.zeros((S, N_PLANES, 10, 10), np.float32)
    scal = np.zeros((S, N_SCALARS), np.float32)
    units = np.zeros((S, MAX_UNITS, N_UNIT), np.float32)
    upos = np.zeros((S, MAX_UNITS, 2), np.int64)
    valid = np.zeros((S, MAX_UNITS), bool)
    dmask = np.zeros((S, 100), bool)
    for i, t in enumerate(steps):
        n = min(int(z["n_units"][seat, t]), MAX_UNITS)
        pos = [tuple(int(v) for v in z["unit_pos"][seat, t, u]) for u in range(n)]
        planes[i] = step_planes(z["tiles"][seat, t], pos)
        shops = np.bincount(z["shops"][t][z["shops"][t] > 0], minlength=9)[1:9]
        scal[i] = step_scalars(z["shed"][seat, t], z["seeds"][seat, t], z["money"][seat, t], z["prices"][t], z["inventory"][t],
                               shops, int(z["day"][t]), int(z["hour"][t]), n, int(z["quadrants"][seat, t]))
        dmask[i] = destination_mask(z["tiles"][seat, t]).ravel()
        for u, (x, y) in enumerate(pos):
            units[i, u] = unit_vector(x, y, u, z["unit_inv"][seat, t, u])
            upos[i, u] = (x, y)
            valid[i, u] = lab["valid"][seat, t, u]
    d = lab["dest"][seat, steps]
    dest_idx = np.where(d[..., 0] >= 0, d[..., 1].astype(np.int64) * 10 + d[..., 0].astype(np.int64), -1)
    return {"planes": planes, "scal": scal, "units": units, "upos": upos, "valid": valid, "dmask": dmask,
            "op": lab["lab_op"][seat, steps].astype(np.int64), "dest": dest_idx,
            "arg": np.minimum(lab["lab_arg"][seat, steps], N_ARG - 1).astype(np.int64),
            "count": np.clip(lab["lab_count"][seat, steps], 0, N_COUNT - 1).astype(np.int64),
            "day": z["day"][steps].astype(np.int64)}


def stream_batches(games: list[tuple[int, int]], stride: int, batch: int, rng: np.random.Generator, chunk_games: int = 16):
    order = list(games)
    rng.shuffle(order)
    for c in range(0, len(order), chunk_games):
        parts = [game_arrays(ep, seat, stride) for ep, seat in order[c: c + chunk_games] if jobs_path(ep).exists()]
        if not parts:
            continue
        data = {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}
        idx = rng.permutation(len(data["op"]))
        for b in range(0, len(idx), batch):
            sel = idx[b: b + batch]
            yield {k: v[sel] for k, v in data.items()}


def build_model(ch: int = 64):
    import torch
    from torch import nn

    class JobNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.trunk = nn.Sequential(
                nn.Conv2d(N_PLANES, ch, 3, padding=1), nn.ReLU(),
                nn.Conv2d(ch, ch, 3, padding=1), nn.ReLU(),
                nn.Conv2d(ch, ch, 3, padding=1), nn.ReLU(),
                nn.Conv2d(ch, ch, 3, padding=1), nn.ReLU())
            self.unit_mlp = nn.Sequential(nn.Linear(2 * ch + N_UNIT + N_SCALARS, 256), nn.ReLU(), nn.Linear(256, 256), nn.ReLU())
            self.query = nn.Linear(256, ch)
            self.tile_w = nn.Linear(ch, 1)
            self.b_dist = nn.Parameter(torch.zeros(19))
            self.b_rel = nn.Parameter(torch.zeros(19, 19))
            self.op_mlp = nn.Sequential(nn.Linear(256 + ch + 2, 256), nn.ReLU(), nn.Linear(256, N_CLASSES))
            self.arg_head = nn.Linear(256 + ch, N_ARG)
            self.count_head = nn.Linear(256 + ch, N_COUNT)
            yy, xx = torch.meshgrid(torch.arange(10), torch.arange(10), indexing="ij")
            self.register_buffer("tile_x", xx.reshape(-1))
            self.register_buffer("tile_y", yy.reshape(-1))

        def unit_state(self, planes, scal, units, upos):
            F = self.trunk(planes)                                   # [B, ch, 10, 10]
            B, C = F.shape[0], F.shape[1]
            flat = F.flatten(2)                                      # [B, ch, 100]
            uidx = (upos[..., 1] * 10 + upos[..., 0]).clamp(0, 99)   # [B, U]
            f_at = torch.gather(flat, 2, uidx.unsqueeze(1).expand(B, C, uidx.shape[1])).transpose(1, 2)  # [B, U, ch]
            pooled = flat.mean(2).unsqueeze(1).expand(-1, units.shape[1], -1)
            h = self.unit_mlp(torch.cat([f_at, pooled, units, scal.unsqueeze(1).expand(-1, units.shape[1], -1)], dim=2))
            return flat, h

        def dest_logits(self, flat, h, upos, dmask):
            q = self.query(h)                                        # [B, U, ch]
            logits = torch.einsum("buc,bct->but", q, flat) / 8.0 + self.tile_w(flat.transpose(1, 2)).squeeze(-1).unsqueeze(1)
            dx = self.tile_x.view(1, 1, -1) - upos[..., 0].unsqueeze(-1)
            dy = self.tile_y.view(1, 1, -1) - upos[..., 1].unsqueeze(-1)
            logits = logits + self.b_dist[(dx.abs() + dy.abs()).clamp(0, 18)] + self.b_rel[(dy + 9).clamp(0, 18), (dx + 9).clamp(0, 18)]
            return logits.masked_fill(~dmask.unsqueeze(1), -1e4)

        def heads_at(self, flat, h, upos, dest):
            B, C = flat.shape[0], flat.shape[1]
            d = dest.clamp(0, 99)
            f_d = torch.gather(flat, 2, d.unsqueeze(1).expand(B, C, d.shape[1])).transpose(1, 2)
            rel = torch.stack([(d % 10 - upos[..., 0]).float() / 9.0, (d // 10 - upos[..., 1]).float() / 9.0], dim=-1)
            op = self.op_mlp(torch.cat([h, f_d, rel], dim=2))
            hd = torch.cat([h, f_d], dim=2)
            return op, self.arg_head(hd), self.count_head(hd)

    return JobNet()


def to_torch(b, device):
    import torch

    return {k: torch.from_numpy(v).to(device) for k, v in b.items()}


def evaluate(model, device, games, stride, batch, rng):
    import torch

    model.eval()
    tot = {"n": 0, "dest_top1": 0, "dest_near": 0, "op_true_dest": 0, "joint": 0, "none_n": 0, "none_ok": 0, "n_job": 0}
    per_op = np.zeros((N_CLASSES, 2), np.int64)
    by_day = np.zeros((4, 2), np.int64)
    with torch.no_grad():
        for b in stream_batches(games, stride, batch, rng):
            t = to_torch(b, device)
            flat, h = model.unit_state(t["planes"], t["scal"], t["units"], t["upos"])
            dl = model.dest_logits(flat, h, t["upos"], t["dmask"])
            pred_dest = dl.argmax(-1)
            op_true, _, _ = model.heads_at(flat, h, t["upos"], torch.where(t["dest"] >= 0, t["dest"], t["upos"][..., 1] * 10 + t["upos"][..., 0]))
            op_pred_d, _, _ = model.heads_at(flat, h, t["upos"], pred_dest)
            valid = t["valid"]
            job = valid & (t["op"] > 0)
            none = valid & (t["op"] == 0)
            pd_, td = pred_dest, t["dest"]
            near = ((pd_ % 10 - td % 10).abs() + (pd_ // 10 - td // 10).abs()) <= 1
            op_at_pred = op_pred_d.argmax(-1)
            tot["n"] += int(valid.sum()); tot["n_job"] += int(job.sum())
            tot["dest_top1"] += int(((pd_ == td) & job).sum())
            tot["dest_near"] += int((near & job).sum())
            tot["op_true_dest"] += int(((op_true.argmax(-1) == t["op"]) & job).sum())
            tot["joint"] += int(((pd_ == td) & (op_at_pred == t["op"]) & job).sum())
            tot["none_n"] += int(none.sum()); tot["none_ok"] += int(((op_at_pred == 0) & none).sum())
            ops_np, pred_np, v_np = t["op"].cpu().numpy(), op_at_pred.cpu().numpy(), valid.cpu().numpy()
            ok = (ops_np == pred_np)
            for c in range(N_CLASSES):
                m = v_np & (ops_np == c)
                per_op[c, 0] += int(m.sum()); per_op[c, 1] += int((m & ok).sum())
            days = np.broadcast_to(b["day"][:, None], ops_np.shape)
            for k, (lo, hi) in enumerate(((0, 5), (6, 15), (16, 23), (24, 29))):
                m = v_np & (days >= lo) & (days <= hi) & (ops_np > 0)
                joint_np = ((pd_ == td) & (op_at_pred == t["op"])).cpu().numpy()
                by_day[k, 0] += int(m.sum()); by_day[k, 1] += int((m & joint_np).sum())
    model.train()
    n, nj = max(1, tot["n"]), max(1, tot["n_job"])
    return {"unit_steps": tot["n"], "dest_top1": tot["dest_top1"] / nj, "dest_within1": tot["dest_near"] / nj,
            "op_given_dest": tot["op_true_dest"] / nj, "joint": tot["joint"] / nj, "none_acc": tot["none_ok"] / max(1, tot["none_n"]),
            "per_op": {(("NONE",) + WORK_OPS)[c]: (int(per_op[c, 0]), round(per_op[c, 1] / per_op[c, 0], 3)) for c in range(N_CLASSES) if per_op[c, 0]},
            "joint_by_day": {k: (int(by_day[i, 0]), round(by_day[i, 1] / max(1, by_day[i, 0]), 3)) for i, k in enumerate(("d0-5", "d6-15", "d16-23", "d24-29"))}}


def select_games(args) -> tuple[list, list]:
    import pandas as pd

    hist = pd.read_parquet(ROOT / "data/gold/history.parquet")
    hist["create_time"] = pd.to_datetime(hist["create_time"])
    hist = hist[hist.create_time <= pd.Timestamp(CUTOFF)]
    enc = set(pd.read_csv(FEATURES / "manifest.csv").episode_id.astype(int))
    hist = hist[hist.episode_id.astype(int).isin(enc)]
    if args.split == "team":
        train_t = [t.strip() for t in args.train_teams.split(",") if t.strip()]
        test_t = [t.strip() for t in args.test_teams.split(",") if t.strip()]
        tr = hist[hist.team_name.isin(train_t)].drop_duplicates("episode_id")
        te = hist[hist.team_name.isin(test_t) & ~hist.episode_id.isin(tr.episode_id)].drop_duplicates("episode_id")
        return [(int(r.episode_id), int(r.seat)) for r in tr.itertuples()], [(int(r.episode_id), int(r.seat)) for r in te.itertuples()]
    mine = hist[(hist.team_name == args.team) & (hist.is_current_sub == True)].drop_duplicates("episode_id").sort_values("create_time")
    games = [(int(r.episode_id), int(r.seat)) for r in mine.itertuples()]
    return games[: -args.holdout], games[-args.holdout:]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--team", default="THIRD FARM CLUB")
    ap.add_argument("--holdout", type=int, default=25)
    ap.add_argument("--split", choices=["time", "team"], default="time")
    ap.add_argument("--train-teams", default="")
    ap.add_argument("--test-teams", default="")
    ap.add_argument("--epochs", type=int, default=6)
    ap.add_argument("--batch", type=int, default=48, help="steps per batch (each with up to 20 units)")
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--lr", type=float, default=2e-3)
    ap.add_argument("--init", default="", help="weights to start from (the general model)")
    ap.add_argument("--name", default="tfc")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-train-games", type=int, default=0)
    args = ap.parse_args()
    import torch
    from torch import nn

    device = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.default_rng(args.seed)
    train, test = select_games(args)
    if args.max_train_games:
        train = train[: args.max_train_games]
    train = [g for g in train if jobs_path(g[0]).exists()]
    test = [g for g in test if jobs_path(g[0]).exists()]
    print(f"[jobs] {device}: {len(train)} train games, {len(test)} test games, stride {args.stride}", flush=True)
    model = build_model().to(device)
    if args.init:
        model.load_state_dict(torch.load(args.init, map_location=device))
    # class weights from a sample of the training labels, 1/sqrt(freq) capped at 8x
    counts = np.zeros(N_CLASSES)
    for ep, seat in train[:60]:
        lab = load_labels(ep)
        counts += np.bincount(lab["lab_op"][seat][lab["valid"][seat]], minlength=N_CLASSES)
    freq = counts / max(1, counts.sum())
    w = np.minimum(8.0, 1.0 / np.sqrt(np.maximum(freq, 1e-4)))
    w = w / w[freq > 0].mean()
    ce_op = nn.CrossEntropyLoss(weight=torch.tensor(w, dtype=torch.float32, device=device), reduction="none")
    ce = nn.CrossEntropyLoss(reduction="none")  # no label smoothing: it would spread mass onto masked destinations
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    steps_per_epoch = max(1, int(sum(719 // args.stride for _ in train) / args.batch))
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(1, args.epochs * steps_per_epoch), eta_min=args.lr / 20)
    (OUT / "models").mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    step = 0
    for epoch in range(args.epochs):
        for b in stream_batches(train, args.stride, args.batch, rng):
            t = to_torch(b, device)
            flat, h = model.unit_state(t["planes"], t["scal"], t["units"], t["upos"])
            valid = t["valid"]
            job = valid & (t["op"] > 0)
            own = t["upos"][..., 1] * 10 + t["upos"][..., 0]
            dest_in = torch.where(t["dest"] >= 0, t["dest"], own)
            dl = model.dest_logits(flat, h, t["upos"], t["dmask"])
            op_l, arg_l, count_l = model.heads_at(flat, h, t["upos"], dest_in)
            loss_dest = (ce(dl.flatten(0, 1), dest_in.flatten()) * job.flatten()).sum() / max(1, int(job.sum()))
            loss_op = (ce_op(op_l.flatten(0, 1), t["op"].flatten()) * valid.flatten()).sum() / max(1, int(valid.sum()))
            arg_m = valid & torch.isin(t["op"], torch.tensor(sorted(ARG_OPS), device=device)) & (t["arg"] > 0)
            cnt_m = valid & torch.isin(t["op"], torch.tensor(sorted(COUNT_OPS), device=device)) & (t["count"] > 0)
            loss_arg = (ce(arg_l.flatten(0, 1), t["arg"].flatten()) * arg_m.flatten()).sum() / max(1, int(arg_m.sum()))
            loss_cnt = (ce(count_l.flatten(0, 1), t["count"].flatten()) * cnt_m.flatten()).sum() / max(1, int(cnt_m.sum()))
            loss = loss_dest + 1.5 * loss_op + 0.5 * loss_arg + 0.3 * loss_cnt
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 2.0)
            opt.step()
            sched.step()
            step += 1
            if step % 200 == 0:
                acc_d = float(((dl.argmax(-1) == dest_in) & job).sum() / max(1, job.sum()))
                acc_o = float(((op_l.argmax(-1) == t["op"]) & valid).sum() / max(1, valid.sum()))
                print(f"[jobs] epoch {epoch} step {step} loss {loss.item():.3f} (dest {loss_dest.item():.2f} op {loss_op.item():.2f}) batch dest {acc_d:.3f} op {acc_o:.3f} ({time.time() - t0:.0f} s)", flush=True)
        m = evaluate(model, device, test, args.stride, args.batch, np.random.default_rng(1))
        print(f"[jobs] epoch {epoch} TEST unit-steps {m['unit_steps']}: dest top1 {m['dest_top1']:.3f} within1 {m['dest_within1']:.3f} "
              f"op|dest {m['op_given_dest']:.3f} joint {m['joint']:.3f} none {m['none_acc']:.3f}; by day {m['joint_by_day']}; per op {m['per_op']}", flush=True)
        torch.save(model.state_dict(), OUT / "models" / f"{args.name}_e{epoch}.pt")
        with (OUT / "metrics.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "name": args.name, "epoch": epoch, "train_games": len(train),
                                 "test_games": len(test), "split": args.split, "stride": args.stride, **{k: v for k, v in m.items()}}) + "\n")


if __name__ == "__main__":
    main()
