"""Polite client for the two Kaggle episode endpoints the study needs.

ListEpisodes is the unauthenticated JSON endpoint the site itself uses. It returns per-agent
banks and before/after ratings that the CLI drops. Kaggle throttles it hard (429s come in
bursts), so calls are spaced, backoff is exponential, and every response is cached on disk.
When the endpoint keeps refusing, the authenticated Python client serves as a fallback: it
returns the same episodes and agents but no ratings, and the cached payload is marked so a
later refresh can fill them in.

Replays come through the authenticated Python client (the old public CDN path 404s) and are
stored zstd-compressed, which shrinks a 30 MB replay to roughly 150 KB.
"""

from __future__ import annotations

import json
import tempfile
import threading
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import requests
import zstandard as zstd

from research.paths import EPISODE_CACHE, REPLAYS

LIST_URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"
MIN_SPACING_S = 1.5
CACHE_MAX_AGE = timedelta(hours=12)
MAX_ATTEMPTS = 8

_session = requests.Session()
_session.headers["User-Agent"] = "kaggriculture-research (IMINABO1)"
_lock = threading.Lock()
_last_call = 0.0
_local = threading.local()


def _throttle() -> None:
    global _last_call
    with _lock:
        wait = MIN_SPACING_S - (time.monotonic() - _last_call)
        if wait > 0:
            time.sleep(wait)
        _last_call = time.monotonic()


def _kaggle():
    """One authenticated client per thread; the client's HTTP session is not shared."""
    api = getattr(_local, "api", None)
    if api is None:
        from kaggle.api.kaggle_api_extended import KaggleApi

        api = KaggleApi()
        api.authenticate()
        _local.api = api
    return api


def _as_dict(obj) -> dict:
    if isinstance(obj, dict):
        return obj
    data = getattr(obj, "__dict__", {})
    return {k.lstrip("_"): v for k, v in data.items()}


def _enum_name(value) -> str:
    s = str(value)
    return s.rsplit(".", 1)[-1]


def _list_via_client(submission_id: int) -> dict:
    """Same shape as the raw endpoint, minus ratings, submissions, and teams."""
    episodes = []
    for ep in _kaggle().competition_list_episodes(int(submission_id)):
        d = _as_dict(ep)
        agents = []
        for i, a in enumerate(d.get("agents") or []):
            ad = _as_dict(a)
            agents.append(
                {
                    "submissionId": ad.get("submissionId") or ad.get("submission_id"),
                    "index": ad.get("index", i),
                    "reward": ad.get("reward"),
                    "teamId": ad.get("teamId") or ad.get("team_id"),
                    "teamName": ad.get("teamName") or ad.get("team_name"),
                }
            )
        episodes.append(
            {
                "id": int(d.get("id")),
                "createTime": str(d.get("createTime") or d.get("create_time") or ""),
                "endTime": str(d.get("endTime") or d.get("end_time") or ""),
                "state": _enum_name(d.get("state")),
                "type": _enum_name(d.get("type")),
                "agents": agents,
            }
        )
    return {"episodes": episodes, "submissions": [], "teams": [], "source": "client"}


def list_episodes(submission_id: int, refresh: bool = False) -> dict:
    """Full ListEpisodes payload for one submission: episodes, submissions, teams."""
    path = EPISODE_CACHE / f"{submission_id}.json"
    if path.exists() and not refresh:
        age = datetime.now(UTC) - datetime.fromtimestamp(path.stat().st_mtime, UTC)
        cached = json.loads(path.read_text(encoding="utf-8"))
        if age < CACHE_MAX_AGE and cached.get("source") != "client":
            return cached
    data = None
    for attempt in range(MAX_ATTEMPTS):
        _throttle()
        try:
            resp = _session.post(LIST_URL, json={"submissionId": int(submission_id)}, timeout=30)
        except requests.RequestException:
            time.sleep(min(120, 5 * 2**attempt))
            continue
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After")
            wait = (
                float(retry_after)
                if retry_after and retry_after.isdigit()
                else min(120, 5 * 2**attempt)
            )
            time.sleep(wait)
            continue
        resp.raise_for_status()
        data = resp.json()
        data["source"] = "raw"
        break
    if data is None:
        data = _list_via_client(submission_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
    return data


def replay_path(episode_id: int) -> Path:
    return REPLAYS / f"{episode_id}.json.zst"


def download_replay(episode_id: int) -> Path:
    """Fetch one replay through the authenticated client and store it compressed."""
    out = replay_path(episode_id)
    if out.exists():
        return out
    with tempfile.TemporaryDirectory() as tmp:
        _kaggle().competition_episode_replay(int(episode_id), path=tmp, quiet=True)
        files = list(Path(tmp).glob("*.json"))
        if not files:
            raise FileNotFoundError(f"no replay file returned for episode {episode_id}")
        raw = files[0].read_bytes()
    json.loads(raw)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp_out = out.with_suffix(".tmp")
    tmp_out.write_bytes(zstd.ZstdCompressor(level=10).compress(raw))
    tmp_out.replace(out)
    return out


def load_replay(episode_id: int) -> dict:
    return json.loads(zstd.ZstdDecompressor().decompress(replay_path(episode_id).read_bytes()))


def store_replay_json(episode_id: int, raw: bytes) -> Path:
    """Store an already-downloaded replay (used for the probe files and tests)."""
    out = replay_path(episode_id)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(zstd.ZstdCompressor(level=10).compress(raw))
    return out
