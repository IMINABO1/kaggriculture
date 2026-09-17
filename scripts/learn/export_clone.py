"""Export a trained JobNet to agent/clone_weights.npz and check the numpy forward against torch.

    .venv-learn/Scripts/python.exe scripts/learn/export_clone.py data/features/jobs/models/tfc_e5.pt
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "learn"))

from agent.clone_feats import MAX_UNITS, N_PLANES, N_SCALARS, N_UNIT  # noqa: E402
from agent.clone_net import CloneNet  # noqa: E402


def main() -> None:
    import torch

    from train_jobs import build_model

    src = Path(sys.argv[1])
    out = ROOT / "agent" / "clone_weights.npz"
    model = build_model()
    state = torch.load(src, map_location="cpu")
    model.load_state_dict(state)
    model.eval()
    arrays = {k: v.detach().cpu().numpy().astype(np.float32) for k, v in state.items() if k not in ("tile_x", "tile_y")}
    np.savez(out, **arrays)
    net = CloneNet.load(str(out))
    rng = np.random.default_rng(0)
    worst = 0.0
    for _ in range(20):
        planes = rng.random((N_PLANES, 10, 10), dtype=np.float32)
        scal = rng.random(N_SCALARS, dtype=np.float32)
        n = int(rng.integers(1, MAX_UNITS + 1))
        units = rng.random((n, N_UNIT), dtype=np.float32)
        upos = rng.integers(0, 10, size=(n, 2))
        dmask = rng.random(100) > 0.2
        dest = rng.integers(0, 100, size=n)
        with torch.no_grad():
            tp = torch.from_numpy(planes)[None]
            flat_t, h_t = model.unit_state(tp, torch.from_numpy(scal)[None], torch.from_numpy(units)[None], torch.from_numpy(upos)[None])
            dl_t = model.dest_logits(flat_t, h_t, torch.from_numpy(upos)[None], torch.from_numpy(dmask)[None])
            op_t, arg_t, cnt_t = model.heads_at(flat_t, h_t, torch.from_numpy(upos)[None], torch.from_numpy(dest)[None])
        flat = net.trunk(planes)
        h = net.unit_state(flat, scal, units, upos)
        dl = net.dest_logits(flat, h, upos, dmask)
        op, arg, cnt = net.heads_at(flat, h, upos, dest)
        for a, b in ((dl, dl_t), (op, op_t), (arg, arg_t), (cnt, cnt_t)):
            b = b[0].numpy()
            m = np.isfinite(b) & (b > -1e8)
            worst = max(worst, float(np.abs(a[m] - b[m]).max()))
    print(f"exported {out} ({out.stat().st_size / 1e6:.1f} MB, {len(arrays)} arrays); max |numpy - torch| over 20 random inputs: {worst:.2e}")
    if worst > 1e-3:
        raise SystemExit("numpy forward differs from torch")


if __name__ == "__main__":
    main()
