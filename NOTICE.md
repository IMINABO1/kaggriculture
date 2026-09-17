# Third-party code

`agent/line_v41.py` is the public Kaggle notebook
`flexonafft/kaggriculture-multi-route-farming-agent` (output `main.py`, 2026-09-16),
bundled verbatim. It is an Apache-2.0 derivation of work by thomastschinkel, yhay81,
destbreso, aurax7, tetsutani, prvsiyan, Dmitrii Gluzdov, Ahmed Berat Ozer and others; the
upstream notices are retained inside the file. The file is used as the opening skeleton of
the hybrid agent (`agent/hybrid.py`) for the first `plan.TAPE_DAYS` days of a game.

`agent/line_v7.py` is the public Kaggle notebook
`aurax7/kaggriculture-shop-router-reactive-v7` (output `main.py`, 2026-09-17), bundled
verbatim: "V45 Full Chassis + V44 Same-Turn Race Escalator + _r60 Survival Guard + 2842
Advance/Frontload Overlay", an Apache-2.0 derivation of work by aurax7, sdy623/jaxa623,
Ahmed Berat Ozer, Rayk Kretzschmar, yhay81, thomastschinkel, tetsutani and destbreso; the
upstream notices are retained inside the file. `plan.TAPE_FILE` selects which of the two
bundled builds the hybrid plays.
