import numpy as np
import pytest

from research.kaggle_api import replay_path

PROBE_EPISODE = 108982600


@pytest.mark.skipif(not replay_path(PROBE_EPISODE).exists(), reason="probe replay not stored")
def test_job_labels_point_at_the_recorded_op():
    from research.encode import encode_replay
    from research.jobs import FIRST_WORK_OP, MAX_WAIT, label_game
    from research.kaggle_api import load_replay

    z = encode_replay(load_replay(PROBE_EPISODE))
    lab = label_game(z)
    S, T, U = lab["lab_op"].shape
    assert T == z["op"].shape[1] - 1
    checked = 0
    for s in range(S):
        for t in range(T):
            for u in range(U):
                if not lab["valid"][s, t, u]:
                    assert lab["lab_op"][s, t, u] == 0 and lab["dest"][s, t, u, 0] == -1
                    continue
                if lab["lab_op"][s, t, u] == 0:
                    continue
                st = t + int(lab["wait"][s, t, u])
                assert st // 24 == t // 24 and st - t <= MAX_WAIT
                assert int(z["op"][s, st, u]) - FIRST_WORK_OP + 1 == int(lab["lab_op"][s, t, u])
                assert tuple(lab["dest"][s, t, u]) == tuple(z["unit_pos"][s, st, u])
                assert not (z["op"][s, t:st, u] >= FIRST_WORK_OP).any()
                checked += 1
    assert checked > 1000
    # a work op at t labels itself with no wait
    work = (z["op"][:, :T] >= FIRST_WORK_OP) & lab["valid"]
    assert (lab["wait"][work] == 0).all()
    assert (lab["lab_op"][work] == z["op"][:, :T][work] - FIRST_WORK_OP + 1).all()
    assert np.isin(lab["lab_op"][lab["valid"]], range(0, 14)).all()
