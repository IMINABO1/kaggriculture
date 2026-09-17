import pytest

from research.kaggle_api import load_replay, replay_path

PROBE_EPISODE = 108982600


def test_unit_action_round_trip():
    from research.encode import decode_unit_action, encode_unit_action

    for op in (["PASS"], ["NORTH"], ["PLANT", "STRAWBERRY"], ["PICKUP", "WHEAT", 6], ["PLACE", "COW", 1],
               ["HARVEST"], ["COLLECT_FERTILIZER"], ["BUILD_PASTURE"]):
        assert decode_unit_action(*encode_unit_action(op)) == op
    assert encode_unit_action(["BOGUS"]) == (0, 0, 0)
    assert encode_unit_action(None) == (0, 0, 0)


def test_order_encoding():
    from research.encode import encode_order

    assert encode_order(["HIRE"]) == (1, 0, 0)
    assert encode_order(["SELL", "MILK", 12]) == (6, 7, 12)
    assert encode_order(["BUY_SEED", "WHEAT", 3]) == (3, 1, 3)
    assert encode_order(["SELL", "MILK"]) == (6, 0, 0)
    assert encode_order(["NOPE", "MILK", 1]) == (0, 0, 0)


@pytest.mark.skipif(not replay_path(PROBE_EPISODE).exists(), reason="probe replay not stored")
def test_encoded_replay_matches_the_observation():
    from agent.tape import actions_from_replay
    from research.encode import OPS, decode_unit_action, encode_replay
    from research.trace import tile_summary, unit_ops

    replay = load_replay(PROBE_EPISODE)
    z = encode_replay(replay)
    steps = replay["steps"]
    assert z["tiles"].shape == (2, len(steps), 10, 10, 12)
    assert float(z["money"][0, -1]) == replay["steps"][-1][0]["observation"]["farms"][0]["money"]
    for t in (0, 200, len(steps) - 1):
        for seat in (0, 1):
            kinds = z["tiles"][seat, t, :, :, 0]
            summary = tile_summary(steps[t][0]["observation"]["farms"][seat]["tiles"])
            assert int((kinds == 0).sum()) == summary["empty"]
            assert int((kinds == 1).sum()) == summary["locked"]
            assert int((kinds == 3).sum()) == sum(v for k, v in summary.items() if k.startswith("plant_"))
            assert int((kinds == 5).sum()) == sum(v for k, v in summary.items() if k.startswith("animal_"))
    for seat in (0, 1):
        for t, action in enumerate(actions_from_replay(replay, seat)):
            for u, op in enumerate(unit_ops(action)[:20]):
                if op[0] not in OPS:
                    continue
                want = list(op)
                if want[0] in ("PLACE", "PICKUP"):
                    want = [want[0], want[1], int(want[2]) if len(want) > 2 else 1]
                assert decode_unit_action(int(z["op"][seat, t, u]), int(z["op_arg"][seat, t, u]), int(z["op_count"][seat, t, u])) == want
