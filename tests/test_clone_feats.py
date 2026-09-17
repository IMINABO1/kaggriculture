import numpy as np
import pytest

from research.kaggle_api import load_replay, replay_path

PROBE_EPISODE = 108982600


@pytest.mark.skipif(not replay_path(PROBE_EPISODE).exists(), reason="probe replay not stored")
def test_runtime_tile_encoding_matches_the_research_encoder():
    from agent.clone_feats import destination_mask, encode_tiles, step_planes
    from research.encode import N_TILE_CH, encode_tiles as research_encode_tiles

    replay = load_replay(PROBE_EPISODE)
    for t in (0, 150, 400, 719):
        for seat in (0, 1):
            tiles = replay["steps"][t][0]["observation"]["farms"][seat]["tiles"]
            want = np.zeros((10, 10, N_TILE_CH), dtype=np.uint8)
            research_encode_tiles(tiles, t // 24, t, want)
            got = encode_tiles(tiles, t // 24, t)
            assert (got == want).all(), (t, seat)
    planes = step_planes(got, [(4, 4), (4, 4), (5, 4)])
    assert planes.shape == (13, 10, 10) and planes[12, 4, 4] == 2.0 and planes[12, 4, 5] == 1.0
    mask = destination_mask(got)
    assert mask.shape == (10, 10) and mask[4, 4] and mask[5, 5]
