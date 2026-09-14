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

### Milestone: top-10 study planned and approved
Iminabo's ask: for each top-10 team, study the first 50 games, the last 50, and 50-game windows
at the quarter points of long histories, and settle whether our agent should be a fixed plan or
switch strategy. Plan file: `~/.claude/plans/parallel-floating-aurora.md`. Facts established in
plan mode that the pipeline relies on:
- The unauthenticated `ListEpisodes` endpoint returns, per game, both agents' bank, rating
  before and after, submission and team ids, plus the submissions and teams involved. The CLI
  and the Python client drop the ratings, so the pipeline calls the endpoint directly
  (1.2 s spacing, cached).
- Replays download through the authenticated Python client only; the old public CDN path
  now returns 404. A replay is 20-33 MB and compresses ~236x with zstd.
- Replaying a recorded game from its seed and both action streams reproduced episode
  108982600's banks exactly (113995 / 113209) in 4.7 s. That makes recorded games usable as
  local opponents and lets us regenerate any observation from actions alone.
- Community assets reused: `georgymamarin/kaggriculture-episodes` (index of 145k episodes,
  Apache-2.0) for team-to-submission seeds; `raykkretzschmar/kaggriculture-reference-agents`
  (MIT, ten runnable agents) and `destbreso/kaggriculture-benchmark-matchups` (CC0, 45k
  replayable matchups) noted for the arena.

### Decision: sample windows over the team's whole history, plus the current sub's first 50
"First 50 plays" is read as the team's earliest games across all its submissions, because
that is what shows how they climbed. The current submission's first 50 (window C0) is added
because that is the agent that will be on the ladder at the deadline. Histories of 250 games
or fewer are taken whole; sampling them would cost more than fetching them.

### Decision: study the union of the screenshot's top 10 and the live top 10
Between Iminabo's screenshot, my first read, and the crawl's snapshot an hour later, four
teams rotated through ranks 7-10 (Otter Vibe, Catalyst, Thomas Tschinkel, feel the agi out;
アルモンド, Artem The Farmer, HowardLeeTW, DSM in). Ranks 5-15 sit within the ±50-point
noise the former #1 documented, so "the top 10" is really a band. The study therefore covers
every team that was top-10 in either the screenshot or the snapshot (14 teams), each tagged
with its live rank at snapshot time. Cost: roughly 40% more replays than a strict ten.

### Surprise: the top three are not tapes
First 144 traces (the current subs' first and last 50 games). Distinct field-action lines
across a submission's games, by turn cut:
- Majkel1337 (#1), 100 games: 4 openings at turn 24 (largest 49%), 23 lines at turn 48,
  53 at turn 100, all 100 distinct by turn 300. Market orders branch the same way.
- ymg_aq (#2), 47 games: one identical line through turn 48 (day 2), 21 lines at turn 100,
  all distinct by turn 200. The break sits right after the first shop unlock on day 3.
- SpaTaro (#3), 19 games: every game distinct from turn 24 onward.
So the leaders react to state from the first days; the "everyone replays a tape" picture
from the forum describes the mass of the ladder, not its head. Sell units in traces are now
the executed amount (capped by the shed), because one agent requests 17,878 wheat a game.

### Surprise: weeds are coupled to the opponent through the shared random stream
Replaying Majkel1337's recorded actions from episode 108982600 on its own seed:
- against the original opponent's recording: 113,209 (exact);
- against `pass`: 52,568; against `starter`: 48,467. Weeds land on days 3, 5, 8 (five at once)
  instead of days 1, 16, 17. The opponent's farm consumes a different number of random draws,
  so every later draw shifts.
- seats swapped (same two recordings): 110,698 / 114,496, close but not exact.
Consequences: a verbatim tape is only faithful against the opponent it was recorded with;
the arena's `tape:` opponents understate reactive teams (whose recordings cannot react);
and any deterministic plan we write must survive weeds landing anywhere, because the seed
alone does not fix them. This is the mechanism behind the forum's "weed route repair" work.

### Surprise: SpaTaro's uniqueness is partly manufactured
Every SpaTaro game is distinct from turn 24, yet its day-0 plan is stable: 2 cows, 2 sheep,
7-10 melons, 6-8 wheat, 4-5 pastures, 6 hands hired on turn 0, animals placed by turn 4.
The difference between games is dozens of `BUY_PRODUCT CARROT/MILK/TOMATO/WOOL/MELON/EGG n`
orders the engine cannot execute (only wheat and fertilizer are buyable), sprinkled through
the market queue with varying counts. They cost nothing and make every action stream, and
every naive plan hash, unique. Whether the intent is anti-copying or a side effect of a
noisy market layer, the effect is the same: replay-based cloning of SpaTaro is harder.

### Decision: measure plans, not just streams
Three fingerprints per game now: the exact action stream (community convention), the field
stream (farmer + hands only), and an order-insensitive plan signature (multiset of
non-movement unit ops with arguments plus executable market orders). The plan signature
ignores orders the engine would drop, and `invalid_orders` per game is a feature in its own
right. This separates "different plan" from "same plan, different path" from "same plan
plus noise".

### Checkpoint: histories crawled for 14 teams
`data/top10/history.parquet`: 56,338 (submission, game) rows from 364 submissions. Public
games per team range from 906 (Catalyst, playing since 2026-09-12) to 9,162 (Mengfei Li,
77 submissions since 08-02). Every team exceeds 250 games, so all get F/Q1/Q2/Q3/L plus C0:
4,200 sample rows, 4,043 unique episodes, 941 already stored from the prefetch.
Two caveats recorded for the report: the API's `submissionCount` is the number of *active*
submissions (always 2), not the lifetime count, so "found vs declared" cannot be checked that
way; and ratings come from the community index because both Kaggle listing endpoints throttle,
so rating coverage is uneven (4,519 of 9,162 games for Mengfei Li, 1 of 906 for Catalyst).
A slow refresher for the current submissions' ratings runs after the downloads.

### Surprise: the top 10 is brand new
Every current top-10 submission is 0-6 days old (all created 2026-09-08 to 09-14), and the
board's tenth place flipped between two reads an hour apart. The community index has only
0-2 stored games for these subs, so their games must be fetched directly. Team histories are
long though: Mengfei Li has 70+ submissions since 2026-08-02, Thomas Tschinkel 49+ since 08-14.
