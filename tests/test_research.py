import pandas as pd
import pytest

from research import sampling
from research.kaggle_api import load_replay, replay_path
from research.paths import COMMUNITY
from research.trace import build_trace, stream_hashes

PROBE_EPISODE = 108982600
COMMUNITY_EPISODE = 104462171


def test_windows_take_everything_up_to_250():
    assert sampling.windows(60) == {"ALL": list(range(60))}
    assert sampling.windows(250)["ALL"] == list(range(250))


def test_windows_sample_five_blocks_of_fifty_above_250():
    w = sampling.windows(1000)
    assert list(w) == ["F", "Q1", "Q2", "Q3", "L"]
    assert w["F"] == list(range(50))
    assert w["L"] == list(range(950, 1000))
    assert w["Q2"] == list(range(475, 525))
    assert all(len(v) == 50 for v in w.values())


def test_windows_stay_in_range_just_above_250():
    w = sampling.windows(260)
    assert all(0 <= p < 260 for v in w.values() for p in v)
    assert w["Q3"] == list(range(170, 220))


def test_current_sub_windows_cap_at_fifty():
    assert sampling.current_sub_windows(30) == {"C0": list(range(30))}
    assert sampling.current_sub_windows(400) == {"C0": list(range(50))}


@pytest.mark.skipif(not replay_path(PROBE_EPISODE).exists(), reason="probe replay not stored")
def test_trace_final_money_matches_rewards():
    replay = load_replay(PROBE_EPISODE)
    trace = build_trace(replay)
    assert [s["final_money"] for s in trace["seats"]] == trace["rewards"]
    assert len(trace["seats"][0]["actions"]) == 719
    assert trace["seats"][0]["money_by_day"][0] == 3000


@pytest.mark.skipif(not replay_path(PROBE_EPISODE).exists(), reason="probe replay not stored")
def test_tape_replay_reproduces_banks():
    from kaggle_environments import make

    from agent.tape import Tape

    replay = load_replay(PROBE_EPISODE)
    trace = build_trace(replay)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": trace["seed"]})
    env.run([Tape(trace["seats"][0]["actions"]), Tape(trace["seats"][1]["actions"])])
    assert [s.reward for s in env.steps[-1]] == trace["rewards"]


@pytest.mark.skipif(
    not (COMMUNITY / "replays_2026-08b.parquet").exists(), reason="community shard absent"
)
def test_stream_hash_matches_community_convention():
    import json

    import pyarrow.dataset as pads

    from agent.tape import actions_from_replay

    ds = pads.dataset(str(COMMUNITY / "replays_2026-08b.parquet"))
    row = ds.scanner(filter=pads.field("episode_id") == COMMUNITY_EPISODE, batch_size=1).head(1)
    replay = json.loads(row.column("replay_json")[0].as_py())
    hashes = (
        pd.read_csv(COMMUNITY / "stream_hashes.csv")
        if (COMMUNITY / "stream_hashes.csv").exists()
        else None
    )
    if hashes is None:
        pytest.skip("stream_hashes.csv not downloaded")
    ref = hashes[(hashes.episode_id == COMMUNITY_EPISODE) & (hashes.seat == 0)].iloc[0]
    ours = stream_hashes(actions_from_replay(replay, 0))
    for cut in (24, 100, 200, 400, 719):
        assert ours[f"h{cut}"] == ref[f"stream_h{cut}"]


@pytest.mark.skipif(not replay_path(PROBE_EPISODE).exists(), reason="probe replay not stored")
def test_day_table_covers_every_day():
    from research.narrate import day_table

    trace = build_trace(load_replay(PROBE_EPISODE))
    table = day_table(trace, 0)
    assert len(table) == 30
    assert table.money.iloc[0] == 3000
    assert table.quads.iloc[-1] >= 1
    assert (table.harvest >= 0).all()
