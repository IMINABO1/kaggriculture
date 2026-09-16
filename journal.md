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

### Checkpoint: what the replay quota looks like so far
- 00:50-01:02Z: 158 downloads, then refusals (Retry-After 1,180 s, then 45-70 s per
  attempt for an hour while still refusing).
- 01:44-03:09Z: no requests at all. A single probe at 03:09Z succeeded.
- 03:09-03:20Z: 330 downloads at 83 a minute with two workers, then refusals again
  (Retry-After 65-120 s, still refusing at 03:35Z).
So the endpoint behaves like a bucket of roughly 300-350 downloads that refills only over a
long quiet stretch; Retry-After does not describe the closure. The detached fetcher now
backs off progressively (2 to 20 minutes between attempts) and resets on success. At this
rate the batch's current-submission windows (C0 and L, fetched first) need about 4-5 more
hours and the full sample most of a day, so the comparison will be built first on the
current submissions and refreshed as the history windows fill in.

## 2026-09-15

### Checkpoint: interim top-14 vs next-15 comparison built on the C0 windows
All 29 teams' C0 windows (the current submission's first 50 games) are fetched, traced,
and rated (100% rating coverage after two refreshes); the batch's L, F, and Q windows are
still arriving at about 120 replays an hour. `reports/top10/groups.md` compares the groups
on the same features with a Mann-Whitney AUC and p per feature. Headline numbers:
- **Shared plans.** At turn 100 (day 4) 11 of the 15 batch teams sit on a field line
  byte-identical to another studied team's; 3 of the 14 top teams do (アルモンド, Thomas
  Tschinkel, Catalyst, on the same line as 9 batch teams). Through turn 200 (day 8) the
  largest family still has 7 members; at turn 400 two batch teams are still identical.
  None of the top 7 shares a line with anyone from turn 24.
- **Branching.** First field branch on day 1: 6 of 14 top, 1 of 15 batch; on day 8 or
  later: 5 of 14 top, 12 of 15 batch. Opponent-driven branching only in the top group
  (3 teams); weed-driven branching dominates the batch (5). Median distinct games at
  turn 400: 100% top vs 74% batch.
- **Economy: no difference.** Quadrants, land day 1, hands, cows, wheat, units sold,
  units in the last 3 days, final money (105k vs 103k), rating after 25 and 50 games.
  Batch: land day 2 later (11 vs 9.5), 33 vs 31 strawberry, CARE 403 vs 338, FERTILIZE
  113 vs 151.
- **Market.** Batch dumps melon on day 11 and never sells melon again (last sell day 11
  vs 20); strawberry first sold day 19 vs 15.5; wool day 6 vs 8.5; melon sold 12 vs 18.
- **Weeds.** Sharpest separator: 12 of 15 batch teams leave 0 weed tile-days at day end
  (same-day repair, the public tape); the top 7 leave 8-49 tile-days per game with the
  same DIG count.
- **Head to head.** All-time 663-439 (60%) for the top-14; current subs 60-13 (82%).
  Unknown Mother-Goose (rank 8, a runtime agent by every measure) is 150-135 all-time
  against the top-14, the only batch team above 50%.
- **Ratings.** Identical to game 50 (~2,850 both); after game 200, 3,043 vs 2,882 (few
  batch teams have 200 games yet).
The interim report uses the C0 window for both groups (`analyze.py --profile-window C0`);
it is re-run on all current-submission games when the batch's L window lands.

### Checkpoint: comparison re-run on every current-submission game
The batch's L window landed at 12:16Z (1,305 of 1,305), so the comparison now measures all
29 teams on every sampled game of their current submission (50-126 games each) instead of
the first 50 only. Same picture, nearly the same numbers: distinct games at turn 400 100%
vs 69%; first field branch on day 1 for 7 of 14 top teams vs 1 of 15 batch, on day 8 or
later for 3 vs 11; opponent-driven branching only in the top group (Majkel1337, Orbital
Terraformer); weed-driven for 6 batch teams; 11 of 15 batch teams on a shared line at day
4 vs 3 of 14; melon last sale day 19 vs 11; strawberry first sale 15.5 vs 19; weed
tile-days 10.5 vs 0; CARE 334 vs 403; FERTILIZE 154 vs 111; final money 104k vs 103k; win
rate 84% vs 83% against opponents rated 2,453 vs 2,394; current subs head to head 60-13.
Losses differ in kind: the top-14 lose mostly to each other (58%, median margin 4.5k),
the batch to unstudied teams (78%, margin 2.3k). Memo findings 10-15 updated. The
fetcher continues on the batch's F and quarter windows (about 3,200 replays, a day at
the quota's pace); they change only the dossiers' evolution tables.

### Decision: zones come from the full board, and silver and bronze join the study
Iminabo's correction (P13): gold ends at rank 28, so ranks 29-48 of the batch are silver.
`snapshot.py --full` now downloads the whole leaderboard (9,125 teams at 2026-09-15T1342Z;
Kaggle's rule gives gold = 28, silver = 456, bronze = 912) and labels every team with its
zone at that snapshot. Groups for the comparison:
- **top**: the original 14 (kept as the study's subject even though two of them, redblackbst
  and Thomas Tschinkel, had slipped to ranks 31 and 41 by this snapshot);
- **gold**: every other gold team the crawl can seed, ranks 6-28 (16 teams, including the
  three of the first batch that are gold now: Unknown Mother-Goose at 3, leave you at 10,
  kyy666 at 28);
- **silver**: the 12 first-batch teams now in silver plus chunks 120-122, 250-252, 400-402;
- **bronze**: chunks 470-472, 600-602, 750-752, 880-882.
The board moved a lot in 13 hours (Unknown Mother-Goose from 8 to 3, ElephtAI from 23 to
234), so the report states each team's rank at both snapshots. New teams get only the
current-submission window (C0, 50 games each) because of the replay quota; the 29 teams
already sampled keep their windows (`data/top10/sample_29teams_2026-09-15T0033Z.csv`).

### Checkpoint: histories for 63 teams, current submissions confirmed
Crawl at 15:20Z: 2,189 submissions, 309,306 (submission, game) rows. The 12-hour listing
cache had expired, so every listing came from the client, which carries no team block:
all 63 current submissions started as "latest episode" guesses and the ratings refresher
corrected 36 of them from the endpoint's team block. A team's most recently played
submission is its leaderboard submission only about half the time (P11 was not a fluke).
Sample: the 29 already-studied teams keep their windows; the 34 new gold, silver, and
bronze teams get C0 only (50 games each, 1,700 replays, about 14 hours at the quota's
pace). The fetcher takes C0 first, so the zone comparison lands before the first batch's
remaining history windows.

### Decision: keep the first-50 window, drop the quarter points for the second batch, then stop
Iminabo's call after seeing the leaderboard shape (a plateau of near-identical agents in
the medal zones, not a power law; `reports/top10/figs/leaderboard_rank_curve.png` and
`leaderboard_powerlaw_check.png`): sampling a dozen teams per zone is enough to see the
pattern, and the remaining fetch should buy findings, not completeness. Kept: every team's
current submission (C0, all 63 teams; L for the first 29) and the first 50 games ever (F)
for the 29 studied in full, because "did the rest of gold ever change, or start as tapes
and stay tapes" is a finding in its own right and costs about 250 replays. Dropped: the
quarter-point windows Q1-Q3 for the second batch of 15 (about 2,300 replays, a day at the
quota's pace) whose value on the top-14 was one gradual change the endpoints already
showed. The fetcher now runs `--windows C0,F` and exits when those are complete; the
four-group report is built when C0 lands, refreshed when F lands, and the thorough
analysis of the zone comparison follows in a fresh session. Replays on disk at this point:
6,700; the quarter windows can be fetched later if a finding needs them.

## 2026-09-16

### Checkpoint: four-group comparison built (top-14, gold, silver, bronze)
C0 landed for all 63 teams at 03:20Z (2,949 replays, 7,221 episodes with features). The
refresher overwrote three pinned submissions on the way (P16, fixed and re-pinned before
the build). `reports/top10/groups.md` now compares four groups (14 top-14, 14 gold, 21
silver, 10 bronze profiled; four teams with fewer than 10 games left out). Headline
numbers, all per-team medians of the current submission:
- One tape family runs the plateau: at turn 24, 34 of 59 teams share one field line (7
  top-14, 7 gold, 20 of 21 silver, 10 of 10 bronze); at day 8 silver 18 of 21 and bronze
  10 of 10 are still on a shared line, gold 5 of 14, top-14 2 of 14.
- First branch on day 8 or later: 3, 10, 18, 10 of 14, 14, 21, 10. Opponent-driven
  branching: 2 top-14, 2 gold, none below. Distinct games at turn 400: 100, 89, 74, 64%.
- Same farm everywhere (final money 104k, 106k, 102k, 106k; last-3-day units 265-269);
  CARE 334, 363, 405, 417; FERTILIZE 154, 117, 111, 103; weed tile-days 10.5, 0.2, 0, 0;
  last melon sale day 19 vs 11, 11, 11.
- Head to head, current submissions: top-14 over gold 99-89 (53%), gold over silver
  76-37 (67%). Rating after 100 games: 2,967, 2,922, 2,888, 2,622. The first batch's
  60-13 looked lopsided because that batch was mostly silver.
Memo findings 16-19 added. The fetcher continues on the F window (about 190 replays);
milestone B closes the fetch. Thorough analysis follows in a fresh session per Iminabo.

### Checkpoint: fetch closed, final rebuild
The fetcher finished the C0 and F windows at 04:57Z (446 of 446 in its last run, 0
failures) and exited. Final counts: 63 teams, 2,189 submissions, 309,306 history rows;
7,692 replays and traces on disk, 7,394 in the sample, features for 14,788 (game, seat)
rows. Coverage by group: top-14 every window; first batch of 15 C0, L and F; the 34 zone
teams C0. The report, dossiers, groups.md and memo are rebuilt from this state. The
thorough analysis of the zone comparison starts in a fresh session.

### Milestone: thorough-analysis phase started (no agent code)
Iminabo's instruction: analyse what is in hand deeply before writing any agent code. Plan
for this phase, in order: (1) the two unread items the handoff flagged, the #1's four day-1
openings side by side and the tile-level mechanism behind "standing weeds"; (2) a trace-wide
pass that adds realized sale prices per product per game (the feature table has units and
days but not the price received, which is where the market layer's value must show);
(3) trajectories and switching points per team from the history table (per-submission
rating paths, when each team stopped being a tape); (4) the layer-by-layer comparison
(opening read, market clock, labour discipline) across the named candidates; (5) a PCA
and clustering over the per-game features to see whether the zones are a continuum or
discrete strategies; (6) an account of what the data cannot answer and what it would cost
under the replay quota. Output: `reports/top10/analysis.md` plus figures, built by
`scripts/top10/deep.py`, and memo updates where a finding changes the build.

### Surprise: nobody reads the opponent on day 1; the "four openings" are one plan spent to the last dollar
Read the #1's four day-1 field lines side by side (traces, then three replays turn by turn).
All four buy the same things in the same order (2 cows, 3 sheep, 5 pastures, 6+2 melon
seeds, 10 wheat seeds, 4 hands) and the farmer's 24 actions are identical; the lines differ
only in how many wheat seeds get planted at the end of the day (12, 11, 9) because the plan
spends down to $7, $6, $5 and the last seed purchases depend on the wheat price ($27 vs $28),
which the opponent's turn-0 wheat trades move by a dollar. That is why "opponent off its
modal line" predicts the branch: the opponent's trades move the price, not the plan. The
same holds for every day-1 brancher: DSM shares Majkel1337's three lines byte for byte,
Orbital Terraformer runs the same list with 11 wheat seeds, Sida Zuo's three lines differ by
1-3 wheat plantings, redblackbst's five lines by 4-7 wheat plantings at $5-$32 left, and
Mengfei Li's 12 lines have identical purchases and identical money at day end (walking-order
noise). The whole medal plateau uses two openings: "2c3s, 8 melon, ~10 wheat, 4 hands"
(Majkel1337, DSM, Orbital Terraformer) and "2c2s, 12 melon, 7 wheat, 5 hands" (the public
family: Catalyst, redblackbst, Kaggriculture Agent, Unknown Mother-Goose, yomogii, Mengfei
Li). HowardLeeTW (5 cows, 1 sheep, 18 wheat, 1 melon, 7 hands) and Sida Zuo (3 cows, 2 sheep,
7 pastures, 8 melon) are the only different day-1 plans among the branchers. Consequence:
memo finding 4 and the recommended "layer 2: day-1 opponent read" have no evidence behind
them; the leaders' edge over the family must be in what happens after day 1. Logged as P17.

### Surprise: the "weeds" in the study are exhausted strawberries, and full farms cannot grow weeds
Tile-level pass over 144 replays (`scripts/top10/weed_tiles.py`, 18 teams, 8 current-sub games
each, 2,837 weed events). Weeds that spawn on empty tiles are rare: 0.1 to 2 a game, because
the engine only rolls the 0.5% chance on *empty* unlocked tiles and the plateau farm keeps
every tile occupied (the public family has 0 empty tiles at day end; the leaders 1-5). The
other 95-99% of weed events are plants that finished their life and decayed in place:
strawberries after their fourth yield (100% of the family's events, 15 before day 27 and 4
in the last three days, every game), plus some wheat, tomato and carrot for the leaders.
The family digs every one within about 0.6 days; the leaders leave 5-27% of the mid-game
ones standing for 1-2 days while they have spare tiles, and most of the last-three-day ones
forever. So "the top 7 tolerate weeds" (memo finding 14) is an executor that digs when it
needs the tile, not a labour strategy, and the DIG count is the same because an exhausted
plant costs one DIG whether it is dug before or after it turns into a weed. Finding 5 (weeds
coupled to the opponent through the shared RNG) stands, but only matters while a farm has
empty tiles, i.e. the first week and the leaders' spare tiles; a tape with no empty tiles
sees no weed at all.

### Checkpoint: engine-faithful market replica built and verified
`research/market_replay.py` rebuilds every turn's market from the recorded observation:
both seats' DROP/PLACE/PICKUP applied to the sheds first, then both order queues in the
engine's per-unit lockstep against the shared inventory, each unit quoted at the live
price. Checked on five replays (ten seats, 3,595 turns): zero turns where the simulated
money differs from the recorded money; the price function agrees with the engine on 2,565
inventory points; 0.3 s a game. The tracer now takes its sells, buys, hires and land from it
(`trace_version` 2, `money_check` per seat) and every sampled trace is being rebuilt.
First corrected numbers: in the #1's loss to Mengfei Li (108982600) Mengfei sold 102 melon,
254 strawberry, 195 milk and 158 wool against the #1's 72/228/153/144; Artem sold 78 melon
and 289 strawberry in a current-sub game where the old trace had 6 and 143. The "#1 sells
four times the melon" finding was the undercount, not the market.

### Surprise: everyone on the plateau reacts to the shop draw; the leaders just react to more of it
Conditioning each team's current-submission games on the shops unlocked on days 3, 6 and 9
(`features.shops`, the first three entries): with a Yarn Store among them, every one of the
59 profiled teams buys 10-14 sheep instead of 4-6, from the #1 to the last bronze team; with
a milk shop (Pizza, Ice Cream, Smoothie) cows go from 5-7 to 8-9. So the public family is not
a pure tape either: it is one shared agent whose herd follows the demand the town reveals.
The leaders differ in *how much* they react: carrots 50-95 with a Pet Cafe or Farmers Market
against 20-35 without (the family plants 31 either way), tomatoes 8-12 with a milk shop
(the family 1-3), and SpaTaro goes to 20 sheep or 13 cows. This is also what the "shop"
branch driver in `groups.md` was measuring. The mechanism is the market model: each shop
instance consumes one of every product it lists every four turns (12 a day; a single-product
shop 24 a day) against a town centre that takes one a day, so a premium product's whole
demand curve is decided by the eight random unlocks. The reactive layer that matters is
"produce what the town is buying", and it is universal; the study's "reactivity gradient"
is a gradient in the breadth of that response, not in whether it exists.

### Checkpoint: head to head among the leaders, current submissions
Artem The Farmer beats Majkel1337 19-11; Majkel1337 beats everyone else by wide margins
(21-2 Mengfei Li, 14-2 feel the agi, 10-0 SpaTaro, 5-0 Orbital Terraformer, 4-0 DSM) and is
level with Unknown Mother-Goose 4-4; ymg_aq beats Mengfei Li 12-3 and feel the agi 6-0. Of
643 current-sub games among the top 15, the median bank margin is 4.1k, a quarter are
within 2k. There is no seat effect: seat 0 wins 60.9% and seat 1 60.8% of the studied
teams' 309k games (bronze 47/49, gold 75/77 by seat).

### Checkpoint: verifier-facing checks on the zone extension
Zone rule: 9,125 teams give gold = 10 + round(0.2%) = 28, silver = 5% = 456, bronze = 10% =
912, matching the snapshot's zone column (sampled maxima 28 / 402 / 882). Pinning: all 29
first-studied teams have `current_sub_source = frozen` in `teams.csv`. Sampling: the 34 zone
teams carry only C0 (30 of them have games; 4 have none), the top-14 and the first batch
carry C0, F, Q1-Q3 and L. Shared lines: 44 of the 59 profiled teams' modal day-1 field
hashes are shared with another team and the largest family has 34 members, the numbers in
`groups.md`. The four teams left out of `groups.md` (现实是个乐子, Excluding, Roman Katasonov,
MtN) really have no crawled game of their current submission; `analyze.py` matches teams by
id, so the fact that several teams have changed their display name (Artem Veshkin, Blurry,
shiggriculture, Lin Alpha...) does not affect it. My own ad-hoc scripts joined on the
replay's team name and were corrected to join on id.

### Checkpoint: a "breadth of response" score grades the zones
For each profiled team, the mean change in sheep (Yarn Store early), cows (milk shop),
geese (egg shop), carrot plantings (Pet Cafe or Farmers Market) and tomato plantings (Pizza
or Farmers Market) between games with and without the shop by day 9, thresholded (3 sheep,
1.5 cows, 1 goose, 10 carrots, 3 tomatoes), counts how many products a team's plan follows.
Medians: top-14 4.5, gold 3.5, silver 2, bronze 1; AUC silver over bronze 0.86 (p = 0.001),
gold over silver 0.72 (p = 0.02), top-14 over gold 0.67 (p = 0.11). Every bronze team reacts
to the Yarn Store alone. Within the public family the score varies (Catalyst 2, Kaggriculture
Agent 4, feel the agi 5), so the family agent ships with switches its users set differently.
`tests/test_research.py`: 10 passed, including the new replica tests.

### Checkpoint: the zone is the margin over the public line
Labelling every sampled opponent by its day-5 field line and taking each team's current
submission's games against opponents on the current public line (G with 33 strawberry, 163
wheat, 31 carrots): the top-14 win 88.8% of 544 such games by a median 7.2k (Artem 96% by
11.6k, DSM 98% by 11.0k, ymg_aq 96% by 13.9k, THIRD FARM CLUB 93% by 13.4k, Majkel1337 93% by
10.5k); gold 87.8% by 4.2k; silver 80.5% by 2.3k; bronze 58.2% by 0.3k, with several bronze
teams tying (identical banks: two pure tapes of the same line) or losing to it (Toru59er 14%).
The family agent's reactive switches beat its own tape copies, and the leaders beat the
family by the same 8-14k that separates their farms' revenue. The yardstick for our agent is
therefore the margin against the current public line on fixed seeds, both seats, and the
line will change before the deadline (section 4 of `analysis.md`).

### Surprise: two ways to beat the plateau, and the #1 uses the one the study could not see
Money at the start of day 28 is the same in every zone (top-14 88.9k, gold 89.3k, silver
86.8k, bronze 89.6k) and Artem's is *below* Catalyst's (85.5k vs 86.1k), yet Artem beats the
public line 96% of the time by 11.6k. The opponent's bank explains it: a seat on the public
line banks a median 98.9k over all sampled games (101k against non-family opponents, 96k in
mirror matches), but 87.5k against Artem, 81.6k against ymg_aq and 88.2k against Mengfei Li,
while those three bank 95-98k themselves. Majkel1337, THIRD FARM CLUB, Unknown Mother-Goose,
feel the agi and HowardLeeTW win the other way: the family opponent keeps 98-108k and they
bank 108-115k. So there is an out-earn axis and a suppress axis; Artem is #1 because
suppression also works on the out-earners, whose banks depend on premium prices, and the
19-11 record over Majkel1337 is where it shows. The product being flooded is the next thing
to read from the rebuilt sales (the family opponent's realized prices per product in games
against each leader), which is exactly what the pre-P18 traces could not show.

### Surprise: the starvers flood milk and wool, not melon; the out-earners hold their prices
Rebuilt traces (about half done) already show what each leader does to a public-line
opponent's realized prices. Reference: a family seat against a non-family opponent receives
$132 a strawberry, $211 a melon, $118 a milk, $147 a wool and banks 111k. Against Artem the
same seat gets $119 / $202 / $91 / $102 (milk down 23%, wool 31%) and banks 89k; against
ymg_aq $83 / $238 / $87 / $114 (strawberry down 37%) and 82k; against Mengfei Li $105 / $198 /
$60 / $113 (milk halved) and 84k. Artem does this with 202 milk and 162 wool sold at $105
and $130, i.e. it sells more of the same premium goods *earlier and steadier* than the family,
whose 245 milk and 161 wool arrive in the family's fixed dump days; ymg_aq sells 1,270 wheat
(three times anyone) and takes strawberry down instead. Majkel1337, THIRD FARM CLUB and
Unknown Mother-Goose leave the opponent's prices almost untouched ($125 / $227 / $104 /
$161 for Majkel's opponents) and win by receiving more themselves ($164 a strawberry, $132 a
milk, $154 a wool against the family's $132 / $118 / $147). The two axes are therefore
"sell before the family's dump" (starve) and "sell where the family is not selling" (out-
earn); the exact days come from the per-day series once the rebuild finishes.

### Checkpoint: labour per unit of work is the same in every zone; only fertilizer differs
Dividing ops by what they act on (day-end farm censuses from the traces): CARE per animal-day
0.86 / 0.88 / 0.98 / 1.01 by zone, FEED per animal-day 0.80-0.84, WATER per crop tile-day 0.86-
0.87, HARVEST per crop tile-day 0.37 everywhere, movement 49% of every unit-turn everywhere,
PASS 7% everywhere. The one gradient is FERTILIZE per crop tile-day: 0.115 / 0.089 / 0.087 /
0.079. So "labour discipline" in the memo reduces to one lever: the leaders fertilize about
30% more per tile and care for animals every day only when a yield day is coming (the family
cares every animal every day; care banked on non-yield days is wasted on cows and sheep
once the max_held cap is hit). Two more code signatures fell out: Majkel1337, DSM and
Orbital Terraformer never PASS (0.8% of unit-turns against 5-16% for everyone else) and
issue more WATER ops than they have crop tile-days (1.04-1.08, i.e. redundant waterings),
which marks them as one code base with an "always act" executor; HowardLeeTW spends 8.3k on
hands against 4.5-5k for the rest and gets the lowest CARE per animal-day (0.72).

### Checkpoint: the plateau is one point with a halo, not a continuum (PCA preview)
PCA over the current-submission games on 21 farm and ops features (no sales, which await
the rebuilt traces): PC1 (18%) runs from "fertilize, tomatoes, melon, geese" to "late land,
much wheat, much CARE"; PC2 (16%) is the always-act signature (PLANT and WATER ops, no PASS).
Every family team sits at PC1 = 0.8-1.5 with a within-team spread of 0.5-0.7; the leaders
scatter at -0.2 to -4.9 with spreads of 0.9-1.5 (their games vary more because they follow
the shop draw). Silver and bronze centroids are indistinguishable from gold's family members
(1.0 / 1.2 vs 0.8). So the zones are not strategies: there is one dense public point, and
around it a halo of hand-built agents, each in its own place. Sales features are added to
the PCA and the k-means run once the rebuild lands.

**Correction to the entry above.** The sentence "care banked on non-yield days is wasted on
cows and sheep once the max_held cap is hit" is wrong: the engine adds every fed-and-cared day
to `pending_care_bonus` and pays the whole bank at the next production, so a cow cared on
both days of its cycle gives 3 milk instead of 1, and a CARE op is worth one unit of premium
product as long as the tile is harvested. Reading CARE per animal by day from the traces
shows where the leaders' lower total comes from: every zone cares every animal every day
through day 16 (ratio 1.0); from day 17-20 the top-14 drop to 0.76-0.88 while gold, silver
and bronze stay at 1.0 through day 27; and in the last three days the leaders wind down
(0.56, 0.27, 0.00 on days 27-29; Artem 0.66 / 0.41 / 0.15; ymg_aq 0.10 / 0.00 / 0.00) while
the family cares at 0.88-1.00 until day 28 and stops only on day 29. The leaders also let
their herds shrink at the end (12 animals at day 29 against 17: unfed animals escape after
two days, which costs nothing once no further sale is possible). "Labour discipline" is thus
an end-game rule: stop paying for yields that cannot be sold before the season ends, and put
those hands on harvest and hauling instead. The mid-game dip (days 17-26) is unexplained yet
and may be prioritisation of harvest over care when both compete for a hand.

### Note: memo findings 4 and 14 rewritten; the rest waits for the corrected sales
`decision_memo.md` findings 4 (the "day-1 opponent read" is the wheat-seed budget; the
real reactive layer is the shop draw, graded by breadth down the zones) and 14 ("standing
weeds" are exhausted strawberries; the labour signal is the end-game taper and fertilizer)
now carry the mechanisms, each marked "rewritten 2026-09-16" with a pointer to
`analysis.md`. Findings 6, 7, 13 and 18 (sales), "The answer" and the architecture are
rewritten once the rebuilt traces have gone through features, `groups.md` and `deep.py`.

### Milestone: traces, features, reports and the analysis rebuilt on engine-faithful sales
All 7,394 sampled traces rebuilt (trace version 2, 0 failures, 202 a minute with five
workers), `features.parquet` (14,788 seat rows, new `revenue_*`, `price_*`,
`money_check_*` columns), `market.parquet`, `groups.md`, `summary.md`, the 63 dossiers and
`reports/top10/analysis.md` (11 sections) regenerated. Money reconciles in every turn for
99% of current-submission seats. What P18 changed in the published numbers: units sold
in the last three days 393-399 in every zone (was 265-269); melon sold 72-75 everywhere
(was 12-18); strawberry 222 / 248 / 249 / 248 by zone (was 172 / 152 / 129 / 133); milk
182 / 191 / 192 / 205 (was 129 / 125 / 110 / 126); first strawberry sale day 14.5-15
everywhere (was 15.5 / 16 / 19 / 18); first milk sale day 8 and first wool sale day 6
everywhere. `bought_*` now counts executed purchases, which moved a few herd medians by
one (Majkel1337's first window: 7 cows and 5 sheep, not 8 and 7).

### Decision: the market layer is two rules read from the corrected per-day curves
The top-14 sell fewer premium units than the family at higher prices for the same bank;
the edge is relative (the opponent's bank). Two mechanisms, both now in `analysis.md`
section 7 and the memo's "The answer": (1) metering, Majkel1337's, premium goods sold in
two-unit orders across the day at about the town's drain rate (strawberry 7 a day before
day 18 and 22-36 after, milk 14, wool 12, wheat 32, melon 1, medians from inventory
changes), holding the rest in the shed, so it keeps $144-170 a strawberry through day 28
while the line's dump of 20-29 a day fetches $67-75; (2) denial, Artem's and ymg_aq's, 23-29%
of strawberries sold at hour 0 from the previous day's harvest before the line's evening
orders, every premium product sold every day to the end so the price never recovers, staples
(carrots, tomatoes, eggs, 1,270 wheat for ymg_aq) carrying the last ten days. Melon timing
earns nothing (no shop buys melon; the town removes one a day), so the day-10 dump stays.
The memo's architecture drops the opponent classifier for a shop-increment table and gives
the market module the two rules; findings 6, 7, 13 and 18 rewritten with the corrected
numbers. Structure (PCA + k-means over 36 features): 44 of 59 teams on one public point,
two leader clusters (the 2c3s code base and relatives; the goose-and-tomato agents); zones
differ only in how many leaders they hold.

### Surprise: the verifier found a claimed filter that did not exist (P19)
The P18 entry said the feature build "refuses seats where [the reconciliation error]
exceeds a few dollars a game". It did not: the counter existed, nothing read it, and 410 of
14,788 seat rows (four teams' whole historical windows on engine versions 1.32.2-1.32.6,
errors up to $1,114) went into the dossiers' evolution tables unflagged while the report
said "reconciles for 99% of current-submission seats". Iminabo pointed at the Pokémon TCG
post-mortem, where the same habit (a plausible statement about the code or the data written
as if verified) cost the campaign. Fixed today: `research/features.py` blanks the sales
columns of every unreliable seat before `analyze.py` and `deep.py` take a median (the
affected windows now show no sales figures; Thomas Tschinkel's and Emile Andrieu's and
THUNDER THUNDER's first 50, Mengfei Li's first quarter); P18, `METHOD.md` and
`analysis.md` state the true scope with the denominator; P19 records the miss and the rule:
grep or query before writing "X does Y", and quote the count. The 31 mismatches on the
current engine all sit at the last executed step, where the recording shows a shop tick's
units removed before that step's sales were priced; bounded at $466, left as a known gap.
Current-submission medians in `groups.md` did not move (one range edge, 185 to 184).
Tests: 13 passed.

### Checkpoint: build phase opened; breadth table repaired (P20)
Session "phase 1" (Iminabo's name for it). Read in order: CLAUDE.md, METHOD.md, analysis.md
(all 11 sections), decision_memo.md, groups.md's headline, the 2026-09-16 journal and
P17-P19, then the engine source (`kaggriculture.py`, 1,086 lines), its README and AGENTS.md.
Verifier-facing checks confirmed by reading the artifacts, not the record: `research/
features.py` is imported and applied in `analyze.py` (line 227) and `deep.py` (line 56);
Thomas Tschinkel's F window and Mengfei Li's Q1 window show blank sales cells in their
dossiers; the breadth-table bug found on the way is P20 (numpy booleans add as OR, every
team scored 1). `deep.py` rebuilt: medians 4.5 / 3.5 / 2 / 1, AUC 0.67 / 0.73 / 0.86, the
memo's numbers within rounding. Nothing else in analysis.md moved.

### Milestone: the public line's source is on Kaggle, and it runs locally as the arena opponent
Searching the competition's notebooks for the line's date (first seen 2026-09-09, section 4
of analysis.md) found `yhay81/shop-router-0909` (Apache-2.0): a `main.py` that replays one
of 13 complete 719-turn tapes, picks the tape at step 144 from the first two shops (a Yarn
Store among them gives a 6-cow / 10-11-sheep / 0-goose plan instead of 8 / 6 / 3; a double
Yarn Store 4 / 14 / 0), inserts DIG when a weed blocks a planned PLANT or BUILD, brings
sales forward one turn, and liquidates on the last turn. Its plan 0 matches Catalyst's
recorded farmer-and-hand actions for the first 317 turns (13 days). The plateau's current
variants are `aurax7/kaggriculture-shop-router-reactive-v5` (2026-09-14, 92 votes) and
`-v6` (2026-09-16): the same tapes under a 3,300-line stack of runtime repairs (feed
reserve, weed repair, sale lead, budget guard, terminal liquidation) from the
ahmedberatozer / prvsiyan / thomastschinkel lineage, all Apache-2.0. Replaying each router
in the recorded seat of one C0 game per family team, with the opponent's recorded stream
as a tape (`data/notebooks/`, gitignored; `logs/fidelity_routers.log`):
- v5 reproduces Cyrus's and Toru59er's games exactly (0 differing field turns, bank +0),
  ElephtAI's within 15 turns (+$1,437) and Catalyst's within 71 turns from turn 317 (-$1,736);
- v6 reproduces Toru59er exactly and Thomas Tschinkel, Kilupy and Tom&Jerry within 7-15
  turns from turn 349-383 (+$267 to +$1,211);
- kyy666, doubao and mtmr_s1 run forks that part from every candidate by turn 2, 94 and
  218; v5 is still within $1.2k of two of them.
- v5's router never switches plan (it reads the shops and discards them; every game is
  plan 0, then the shared ending at step 648); v6 and 0909 switch on the Yarn Store.
So the family's whole shop response is that one switch, and the "8-9 cows with a milk shop"
of section 3 is the same switch seen from the other side (no Yarn Store means the 8-cow
plan). The leaders' carrots and tomatoes remain real reactions.

### Decision: the yardstick is the public routers themselves; the runtime clone is our skeleton
The plan's Phase 1 asked for a runtime reimplementation of the line as "the only faithful
arena opponent". The routers are more faithful than any reimplementation can be (they are
the opponent), so the arena's public-line opponents are v5, v6, 0909 and 0913 run from
`data/notebooks/` (aliases `line:v5` etc. in `scripts/arena.py`), re-pulled when a new
notebook takes over the plateau. The runtime clone is still built, because every Phase 2
layer (following the town beyond the Yarn Store, the end-game taper, metering and denial)
needs an executor that re-plans from the observation, which a tape cannot do. Its
acceptance changes accordingly: bank within about 2k of the routers' in the same seats, and
a paired-seat win rate near 50% against v5 on fixed seeds, both seats. Not yet approved by
Iminabo in so many words; the session was opened under the name "phase 1" and this keeps
Phase 1's intent, so the work proceeds and the change is flagged in the handoff.

**Note (environment).** The first fidelity run raised the framework's 1,200-second
`runTimeout` on its first game; the rerun took 5-11 s a game. It coincided with `deep.py`
and three other `uv` processes running at once, so it is filed as memory pressure on this
machine, not a router property. Keep arena batches to a few processes.

### Checkpoint: runtime skeleton built; production is the gap, measured against pass
The runtime agent exists (`agent/plan.py` targets and layout read off Shop Router 0909's
plan 0 and Catalyst's game 108947518; `agent/executor.py` builds a job list from the
observation every turn and assigns units to jobs cheapest (unit, job) pair first;
`agent/market.py` follows the line's purchase schedule and sells what reaches the shed).
Measured on fixed seeds, both seats, deterministic on both sides so every rerun is an A/B:
- against the pass agent (no competing sales), seed 1: 123.6k-128.9k; v5 makes 151.1k
  there. The per-product census (`research/market_replay.py` on the local replay) puts the
  gap in production, not prices: wheat 352-405 harvested against 519 (plantings 123-125
  against 162), strawberries 207-213 against 249 (83 of 131 yields doubled by fertilizer
  against 119 of 130), carrots 34-43 against 104, milk 208-229 against 245, fertilizer
  collected 310 against 372, and animals bought as replacements after escapes (cows 11
  bought against 8, sheep 8 against 6);
- against v5 on the non-Yarn-Store seeds 0, 1, 2, 4, 5, both seats: 0-10, mean bank
  64-77k against 88-120k, margin -24k to -48k depending on the build; on seed 3 v5 plays a
  17-sheep, four-quadrant Yarn Store route and makes $90k on wool alone, which is the Phase
  2 shop response, not a Phase 1 defect.
What the day tables and turn views found, in order: animals picked up but never placed;
the hire orders pushed past the ten-order cap by the sells; melons harvested at age 12
instead of 10; a 14th pasture missing; on-tile jobs losing to a neighbouring tile when a
priority went negative (units oscillated for two days and the field weeded); the fertilizer
reserve starving the early cash flow; every dollar spent on seeds so the feed wheat could
not be bought and the herd escaped on days 1 and 10; fertilizer collected on day 1 held in
inventories all day because the haul threshold was above its value. Each was fixed from the
turn view, and each fix is one constant or rule in the executor, so the next session can read
them from `git log -p agent/`.

### Decision: no submission; the gate is many rounds against the top 5 and three gold teams
Iminabo, mid-session: do not submit when the model is made; play it against the top five and
against three randomly chosen gold teams outside the top ten, for multiple rounds, and see
whether it stands a chance. The only local form of those teams is their recorded games
(`scripts/top10/export_tapes.py`, `scripts/arena.py --b tape:...`), which derail once the
weeds differ (METHOD.md section 6), so that gauntlet is a floor, not a forecast, and it runs
once the agent is at parity with the public routers. Phase 3's early submission is cancelled.

### Decision: every executor change is accepted or rejected by a bisect on the production yardstick
Four edits made together (dig priority, opportunistic deposits, morning animal harvests, a
stronger haul priority) dropped production against pass from 151.2k to 137.4k, while each
alone measured 149.2k, 158.2k, 151.8k and 152.7k: the assignment rule interacts with itself.
From here every change is applied alone to the committed executor and measured on
`scripts/eval.sh` (production: seeds 1, 2, 4 against pass; competition: seeds 0, 1, 2, 4, 5
both seats against v5), both deterministic, and kept only if production does not fall and
the competition margin does not worsen. Scratch bisect script: applies each variant to
`git show HEAD:agent/executor.py` and runs the production arena.

### Surprise: the public family agent does read the opponent, mid-game, by farm layout
Read in aurax7's v5 code (`_r37_similarity`, lines 1749-1763 of the code part of
`data/notebooks/kaggriculture-shop-router-reactive-v5/output/main.py`; `_r44_before`,
1820-1833): it compares the two farms tile by tile (crop and animal on each occupied tile,
after checking the unlocked quadrants are equal) and, between steps 336 and 648, probes
whether the rival's money moves within 5% of its own after an all-sale turn; a similarity of
0.90 or more with a matching probe marks the rival as a mirror and switches the agent's
sale ordering (`_R37_ADAPTIVE`). Against my layout-identical clone on seed 1 it also bought
the SE quadrant and planted ten tomatoes (80 sold at $169, $13.5k) and hired for $6.8k,
none of which it does against the pass agent on the same seed. So analysis.md section 1
stands (no day-1 read) but the family's runtime layers include a mid-game mirror detector,
and any clone that copies the line's tile layout meets a stronger v5 than a non-copy does.
Moving the SW strawberries to different rows did not change the margin (-25.6k against
-24.7k) and cost 12k of production from the longer walks, so it was reverted; whether the
detector fired in those games was not checked.

### Checkpoint: where Phase 1 stands
`scripts/eval.sh`, executor = commit 4b5c6ad plus opportunistic deposits: production
against pass 158.2k (v5: 165.9k on the same seeds); competition against v5 0-10, mean bank
69.4k against 94.1k, margin -24.7k. The production gap is 5%; the competition gap is three
times that, and the hour-by-hour sales (`scratch hours_diag.py`) show why: my melon dump
lands at hours 12-21 after v5's at 9-15 ($181 against $225 a unit), my strawberries sell the
next morning at hour 1 while v5 sells the same day's harvest at hours 13-23, and in the
shared glut of a seed without strawberry or milk shops both farms sell at $1-20 from day 21.
Phase 1's acceptance (parity with the line in mirror matches) is not met.

### Decision: the gauntlet plays each recording in seat 0 and our agent in seat 1
The engine draws the day's weeds from one random stream, farm 0 first
(`_end_of_day` in kaggriculture.py: `_spawn_weeds` runs for player 0, then player 1, on
the same `rng`), and each empty tile consumes one draw. A recording in seat 1 therefore
derails as soon as our seat-0 farm has a different number of empty tiles than the farm it
was recorded against; a recording in seat 0 draws first and sees exactly the weeds it saw
when it was recorded, whatever we do in seat 1. Its actions do not react to us, so the only
coupling left is the market, which is the coupling we want to measure. Iminabo's gauntlet
(the top five and three random gold teams outside the top ten, many rounds) will use
seat-0 recordings of each team's current submission, with our agent in seat 1; a
tape-vs-tape rerun of each recording first confirms it reproduces both banks (the
`tests/test_research.py` check). Not verified yet: how many of each team's C0 games are
seat-0 recordings; the listing is being produced now.

### Checkpoint: first gauntlet, 26-54 against the top five and three gold recordings
`scripts/gauntlet.py` on 80 seat-0 recordings of current submissions (ten each, exported
with `export_tapes.py --window C0 --seat 0 --out gauntlet`; three of them replayed tape
against tape reproduce both recorded banks to the dollar), our agent in seat 1, executor at
commit b76f4fd:

| team | W-L | our bank | their bank | their bank when recorded |
|---|---|---|---|---|
| Artem The Farmer | 0-10 | 88.7k | 119.9k | 107.9k |
| Majkel1337 | 4-6 | 96.3k | 93.5k | 112.9k |
| Unknown Mother-Goose | 1-9 | 90.6k | 109.3k | 119.8k |
| DSM | 8-2 | 92.9k | 79.0k | 99.6k |
| SpaTaro | 9-1 | 107.9k | 82.0k | 94.8k |
| HowardLeeTW (rank 13) | 1-9 | 89.3k | 104.6k | 102.0k |
| carbonapi (rank 19) | 1-9 | 76.1k | 105.5k | 104.3k |
| Ebi (rank 21) | 2-8 | 89.0k | 99.1k | 105.1k |

The three gold teams were drawn with `random_state=20260916` from the 16 gold teams
ranked 11-28 that have at least ten seat-0 recordings (现实是个乐子, drawn first, has no
crawled current-submission game and was replaced by the second draw). Reading: our bank
against these recordings (76-108k) is where the ladder's ordinary opponents sit, and the
recordings of DSM and SpaTaro make 13-20k less against us than they did when recorded (our
sales press their prices), while Artem's makes 12k more than it did. A recording cannot
front-run, meter or switch the way the live agents do (v5's mirror detector, journal above),
so 32% here is a ceiling for the live result, not a floor. The answer to "do we stand a
chance" is: not yet, and not against the top three.

### Checkpoint: end of the first build session
State at commit time: `agent/` is a runtime clone of the public line's economy (plan 0 of
Shop Router 0909) with a global nearest-pair executor; `scripts/eval.sh` gives production
158.2k against pass (v5: 165.9k, seeds 1, 2, 4) and competition 0-10 against v5 with a mean
margin of -24.7k (seeds 0, 1, 2, 4, 5, both seats); the gauntlet is 26-54 against seat-0
recordings of the top five and three gold teams; 13 tests pass; `scripts/package.py` builds
and self-plays the bundle. A metering layer exists in `agent/market.py` behind `METER`
(off): sold at the town's drain rate it made no difference against a daily dumper.
What the next session should do, in order: (1) the market timing that costs the 25k in
competition, starting from `scratch hours_diag.py`: melons harvested and hauled to sell by
hour 8 of day 10 (v5 sells at 9-15), the day's premium harvest sold the same day rather than
at hour 1 next morning, and the denial rule of the memo (every premium product every day
once the opponent's bulk sales start); (2) the labour efficiency that still costs 5% of
production (3,500 moves a game against the line's 2,900; zone-based routing rather than
greedy nearest-pair); (3) then Phase 2a, the Yarn Store plan (6 cows, 10-11 sheep, 0 geese)
and the leaders' carrots and tomatoes, since v5 already switches to a yarn route and made
$90k on wool alone in seed 3. Every change through `eval.sh`, one at a time.
