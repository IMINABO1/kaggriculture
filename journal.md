# Journal

Chronological record of milestones, checkpoints, surprises, and engineering decisions. One
section per day, newest at the bottom. Problems live in `problems_encountered.md`.

## 2026-09-14

### Milestone: competition research complete
Read the overview, rules, leaderboard, discussion (11 top threads), the daily replay dataset, and
the most-voted findings notebook. What matters for reaching the top 10:
- Final ranking is a single Bradley-Terry tournament over the two weeks of games after the
  2026-09-30 deadline. Live rating history counts for nothing. Only the last 2 submissions play.
- Rating moves on win/loss/tie only. Coin margin is irrelevant. Optimize win rate against strong
  opponents, on both seats, with fixed seeds.
- Top scores are ~3000-3230. Most of the top 100 are "tapes": recorded 720-turn action histories
  from strong public episodes replayed verbatim, sometimes with a market-timing router on top.
- The converged farm: ~8 cows, 6 sheep, 3 quadrants (NE+SW, never SE), 12 hands/day, ~23
  strawberry + ~31 wheat tiles, ~21 melon seeds early. The remaining edge is premium-product sell
  timing against near-clone opponents.
- Pure RL and behavior cloning have both plateaued far below the tape meta (best documented PPO
  run ~80k bank). SpaTaro (#3) is the one top-10 entry identified as a real runtime agent.
- Engine 1.32.7 is the ladder version. Two balance patches landed in August; the hosts said
  that was the last one barring bugs.
- Runtime budget: 1 s/step + 60 s overage per game, 1.6 vCPU, 6.5 GiB RAM.

### Decision: Python 3.12 pinned via uv
Kaggle's runner image (`Kaggle/docker-python` Dockerfile) is Python 3.12. The machine's default
is 3.14, which the runner does not have. Pinning 3.12 removes one class of "works locally,
errors on the ladder" failures. uv already had 3.12.13 installed.

### Decision: repo is a package plus an arena, not a notebook
`agent/` is an installable package, `main.py` is a thin entrypoint, `scripts/arena.py` plays
paired-seat fixed-seed matches and appends every game to `results/arena.csv`. Reason: the forum
consensus is that the people who climb are the ones with a disciplined local gate (both seats,
same seeds, previous best as veto). The arena is that gate. Nothing gets submitted without it.

### Surprise: how kaggle-environments loads a .py agent
Read `kaggle_environments/agent.py` before writing `main.py`. It execs the file into an empty
dict (so `__file__` is undefined), appends the file's directory to `sys.path` only during the
exec, and returns the LAST callable in the namespace. Consequences baked into `main.py` and
tested in `tests/test_smoke.py`: no `__file__`, imports at the top, `agent` defined last.

### Decision: baseline is a placeholder, not a strategy
`agent/policy.py` is a single farmer working an 8-tile wheat patch beside the shed. Its only job
is to give the arena, packager, and tests something real to run. The competitive agent comes
next and will be judged against reconstructed top tapes from the daily replay dataset, not
against `starter`.

### Checkpoint: environment works end to end
- `uv run pytest -q`: 3 passed (loader contract, self-play validation, full season vs pass).
- `scripts/arena.py --a main.py --b starter --seeds 0-4 --jobs 4`: 10-0-0, mean bank 8500 vs
  3529, 0 errors, 1.4 s per full 720-step game. A full-season game being this cheap means
  hundreds of paired-seat games per candidate are affordable.
- `scripts/package.py`: 1.8 KiB archive, loader picks `agent()`, self-play DONE/DONE.
- Seat 0 and seat 1 banks are identical per seed because neither agent moves the market
  enough to affect the other. That will stop being true once real agents sell premium goods.

### Note: direction for the next sessions
1. Pull one day of the replay dataset and reconstruct the current top tape as a local opponent.
2. Build the economy as a runtime agent (labor scheduling, feed safety, land timing) until it
   beats the tape family on both seats.
3. Only then work the market layer: premium sell timing and clone detection.
