"""Where traces live on disk and how to read and write them."""

from __future__ import annotations

import json
from pathlib import Path

import zstandard as zstd

from research.paths import TRACES


def trace_path(episode_id: int) -> Path:
    return TRACES / f"{episode_id}.json.zst"


def load_trace(episode_id: int) -> dict:
    return json.loads(zstd.ZstdDecompressor().decompress(trace_path(episode_id).read_bytes()))


def save_trace(trace: dict) -> Path:
    TRACES.mkdir(parents=True, exist_ok=True)
    out = trace_path(int(trace["episode_id"]))
    raw = json.dumps(trace, separators=(",", ":")).encode()
    tmp = out.with_suffix(".tmp")
    tmp.write_bytes(zstd.ZstdCompressor(level=10).compress(raw))
    tmp.replace(out)
    return out
