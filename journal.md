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
Later, five of Majkel1337's latest tapes against the passive wheat baseline banked 116k-175k
versus 88k-132k recorded: with nobody else selling, premium prices hold up. So the coupling
cuts both ways: weeds can wreck a fixed tape, and an uncontested market inflates it.
Consequences: a verbatim tape is only faithful against the opponent it was recorded with;
the arena's `tape:` opponents understate reactive teams (whose recordings cannot react);
and any deterministic plan we write must survive weeds landing anywhere, because the seed
alone does not fix them. This is the mechanism behind the forum's "weed route repair" work.

### Checkpoint: the top-14 study is built
`reports/top10/summary.md`, 14 dossiers, `decision_memo.md`. 3,769 replays stored and traced
(zero trace failures), 3,431 of the 4,043 sampled games; the shortfall is the Q3 window,
which the fetcher reached last before Kaggle's API started dropping connections. F, Q1, Q2,
L, and C0 are complete for every team. Ratings cover 99% of sampled games after the refresh.

Headline findings (numbers in the report):
- **The head of the ladder moved from tapes to runtime agents in three weeks.** In their first
  50 games most teams shared one field line across dozens of games (ymg_aq's Q1 window: 9
  field lines and a single market line over 50 games; Mengfei Li F: 15 lines; DSM F: 16;
  HowardLeeTW F: 7; アルモンド F: 9). In their latest 50 games every team's games are all
  distinct by turn 400. Artem The Farmer and Otter Vibe were reactive from their first window.
- **The #1's current submission is reactive from day 1** (4 openings, largest 54%), and being
  off its usual opening tracks the opponent's opening (70% vs 16%). Its rating path: 651 after
  game 1, 2,543 after 25, 2,875 after 50, 3,097 after 100, 3,247 after 200.
- **Its edge is sales, not the farm**: 72 melons sold vs 18 for the median team, 182 milk vs
  128, 109 wool vs 63, 365 units in the last three days vs 262, from 11 hands and 8 cows.
- **Three teams run the identical public plan** (アルモンド, Catalyst, Thomas Tschinkel: 33
  strawberry, 163 wheat, 12 melon, 8 cows, 6 sheep, 3 geese, same field line through turn
  200). They sit at ranks 9-14 with 78-84% sampled win rates.
- **Only one studied team beats the #1 head to head**: Artem The Farmer, 28-26, on a fixed
  five-day opening with a sheep-heavy herd and almost no melon sales.
- **Everyone's farm converged**: 3 quadrants, land on days 5-6 and 8-11, 11-15 hands, 7-11
  cows, 3-8 sheep. Over time the field shifted from ~40 strawberry and ~100 wheat plantings
  to ~30 strawberry and 150-190 wheat, and geese appeared in the latest windows.

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

### Milestone: second batch started (the gold zone outside the 14)
Iminabo's ask: repeat the study for about 15 teams that were not among the 14, drawn from the
gold-medal zone in contiguous chunks with gaps, then compare the two groups on the same
features to see what separates the top 10 from the rest of gold. Snapshot 2026-09-15T0033Z
(19:33 local on 09-14). The board had moved since the 19:36Z read: DSM and Artem The Farmer
are now 2 and 3, and two teams outside the 14 (Unknown Mother-Goose, tetsuya & yuanzhe &
guoqi) had rotated into the top 10. The 14 now occupy ranks 1-7, 9-10, 13-16, and 18.

### Decision: which medal rule, and which chunks
`kaggle competitions list` reports 9,066 teams. Kaggle's rule for competitions with 1,000+
teams is gold = top 10 + 0.2% (rank 28 here), silver = top 5% (rank 453), bronze = top 10%
(rank 907). Iminabo's working assumption was gold = top 50. The batch spans both: ranks 8-23
are gold under Kaggle's rule, ranks 29-48 are silver under Kaggle's rule and gold under the
top-50 assumption. Each batch team carries its rank so the comparison can be cut either way.
Chunks were specified as "8-9,13-14,20-23,29-31,38-39,47-48"; a chunk fills forward past
teams already in the top group (the board moves between reading it and snapshotting it,
and the first attempt landed three chunk ranks on studied teams). Result, 15 teams:
- 8 Unknown Mother-Goose, 11 leave you (chunk from 8)
- 17 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔, 19 Zhenghongshuang (chunk from 13; ranks 13-16 and 18 are studied teams)
- 20 kyy666, 21 Kilupy, 22 elmo, 23 ElephtAI
- 29 Emile Andrieu, 30 mtmr_s1, 31 Kaggriculture Agent
- 38 THUNDER THUNDER, 39 yomogii
- 47 doubao, 48 Tom&Jerry
Unknown Mother-Goose is in the top 10 at snapshot time and is kept in the batch: the groups
are "the 14" versus "the next 15", not "top 10 today" versus the rest, and the memo says so.
`snapshot_latest.csv` now carries a `group` column (top / batch) that every later stage reads.

### Note: two batch teams are missing from the community index
𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 and Kilupy have no submission in `georgymamarin/kaggriculture-episodes`, and
Kaggle's episode endpoint only filters by submission id (a `teamId` filter returns 400). Both
appear as opponents in the 364 listings already cached from the first crawl (4 submissions
each), so `crawl.py` now seeds from its own cache as well as from the index.

### Decision: the top-14's windows are frozen at the first sample
The crawl of the batch also grew the top-14's histories (new opponents revealed new
submissions; Mengfei Li went from 9,162 to 10,390 games), which moved their quarter-point
windows and made their "last 50" a different 50. Re-cutting them would have cost about
1,900 replays for windows that shift by a few percent. `sample.py --freeze` now keeps the
top-14's F/Q1/Q2/Q3/L rows from the committed first sample
(`data/top10/sample_top14_2026-09-14T1936Z.csv`) and recomputes only C0, because
アルモンド's current submission was corrected (P11). The batch is cut fresh from the
2026-09-15T0033Z snapshot. Remaining to fetch after the freeze: 4,851 replays (4,284 for
the batch, 523 for the top-14's Q3 backlog, 44 for アルモンド's C0).

### Surprise: Kaggle rations replay downloads
About 160 replays into the batch, the replay endpoint began answering 429 with a
Retry-After near 20 minutes (P12). The community replay dataset holds only 92 of the
missing games, so the fetch is quota-bound and runs as one long background job with a
shared wait gate. Throughput per quota window is measured below once the window reopens.

### Checkpoint: batch histories crawled, sample cut, comparison code in place
- `history.parquet`: 127,435 (submission, game) rows from 843 submissions for 29 teams.
  Batch histories range from 728 games (𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔, playing since 09-02) to 9,900
  (leave you, 95 submissions since 08-01). Every batch team exceeds 250 games, so all get
  F/Q1/Q2/Q3/L plus C0: 8,700 sample rows, 8,480 unique episodes, 4,851 still to fetch.
- Four current submissions corrected from the endpoint's team block (P11), one of them a
  first-study team (アルモンド), whose dossier is rebuilt from the right submission.
- `analyze.py` builds `groups.md`: per-team profiles of the current submissions, group
  medians with a Mann-Whitney AUC and p per feature, branch-point and driver counts,
  head-to-head between the groups, and a loss breakdown. A dry run on the 158 batch replays
  fetched before the quota closed produced tables and figures without errors; its numbers
  are not reported anywhere.
- Committed and pushed as f07814c.

### Surprise: the official daily episode datasets hold only the leaders' games
Kaggle publishes one dataset per day (`kaggle/kaggriculture-episodes-<date>`, indexed by
`kaggle/kaggriculture-episodes-index`) with that day's top-scoring 650-930 episodes as
individual JSON files, and the datasets endpoint is not rationed (32 MB in 3 s). A full
index (`scripts/top10/daily_index.py`, 32,802 episodes over 47 days) covers only 290 of the
4,851 missing games: 184 of the top-14's Q3 backlog and about 100 batch games. The batch
teams' games rarely score high enough to be "top episodes". The fetcher now takes indexed
episodes from the daily datasets and everything else from the rationed endpoint.
