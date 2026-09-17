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

### Checkpoint: second build session opened; baseline reproduced
Read in the handoff's order (CLAUDE.md, METHOD.md, analysis.md 1-4, 7, 9b, 11, the memo's
answer, architecture and plan, the 2026-09-16 journal and P17-P21, then `agent/`,
`scripts/eval.sh`, `scripts/gauntlet.py`, the engine's market and end-of-day code). The five
routers are under `data/notebooks/` (`ls data/notebooks/*/output/main.py`: 5 files); engine
1.32.7. `scripts/eval.sh` reproduced to the dollar: production 158,165 (seeds 1, 2, 4),
competition 0-10, mean bank 69,409 vs 94,145, margin -24,736. The notebook list (`kaggle
kernels list --competition kaggriculture --sort-by dateRun --page-size 50`) shows v6 as the
family's newest (2026-09-16 02:25Z, 3 votes) and five higher-voted new agents dated 09-15/16:
tetsutani "Market-Smart Farming" (95 votes), flexonafft "Multi-Route Farming Agent" (93),
ahmedberatozer V45 (86), reyhanksatria "Dynamic Route Agent" (85), guruprasaathas111
"Master Engine V3" (79). None pulled yet; they are the candidates for the next public line.

### Surprise: the town's shop draw is coupled to both farms' empty tiles (P22)
`_end_of_day` seeds one `random.Random((seed * 1_000_003) ^ day)` per day, `_spawn_weeds`
consumes one draw per empty tile of farm 0 and then of farm 1, and the shop for the next
day (days 3, 6, ..., 24) is `rng.choice` from the same generator. So a change to our own
empty-tile count on any day before a shop day changes the town for both players from then
on. Seen directly: seed 1 with the committed executor unlocks BAKERY, PIZZA, PIZZA,
ICE_CREAM, FARMERS, YARN, BAKERY, PET_CAFE; with change A (below) it unlocks BAKERY, PIZZA,
ICE_CREAM, PET_CAFE, FARMERS, YARN, FARMERS, BRUNCH. A "fixed seed" is therefore not a fixed
environment across executor changes: v5's own mean bank moved from 94,145 to 103,565 between
two runs that differed only in one of our watering priorities. **Decision:** `eval.sh` now
plays production on seeds 1-8 and competition on seeds 0-9, both seats (28 games, about four
minutes at three jobs), and the verdict is the mean; the earlier numbers are not comparable.
New baseline at commit f81686a's executor: production 137,622 (seeds 1-8; the three-seed
figure was flattering), competition 0-20, mean bank 70,236 vs 99,096, margin -28,861.
Reading a single seed's diagnostic still needs the shops printed next to it. The same
coupling qualifies the gauntlet rule: a seat-0 recording does see its recorded weeds, but its
town diverges from the recorded game as soon as our empty-tile count differs from its
recorded opponent's, so the tape's fixed sales meet a different demand than they were
played for (how often is not yet measured; a check against the tapes' recorded shops is on
the list).

### Checkpoint: where the 25k comes from, per product, on five seeds
Executed sales from the engine-faithful replica (`research/market_replay.py`) on local
replays of `main.py` (seat 0) against v5, our revenue minus v5's in $k:

| seed | melon | strawberry | milk | wool | egg | wheat | carrot | tomato | fertilizer | gross | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | -4.8 | -6.6 | -0.6 | -0.2 | +0.5 | -7.3 | -2.5 | 0 | -4.2 | -25.6 | -24.2 |
| 1 | -4.6 | -4.6 | -2.9 | -1.5 | +0.6 | -5.7 | +0.1 | -13.5 | -4.6 | -36.7 | -30.4 |
| 2 | -4.2 | -4.8 | -2.2 | -2.6 | +1.1 | -7.0 | -0.3 | 0 | -4.6 | -24.6 | -24.0 |
| 4 | -4.2 | -7.3 | -2.2 | -0.2 | +1.1 | -9.1 | -0.1 | 0 | -4.7 | -26.8 | -25.9 |
| 5 | -4.8 | -3.8 | -0.6 | -0.2 | +1.0 | -9.0 | +0.3 | 0 | -4.4 | -21.6 | -20.5 |

Units (ours / v5): melon 63-68 / 72 at $181 / $225; strawberry 219-233 / 247-248; wheat
195-243 / 340-451; fertilizer 243-256 / 347-352; milk within 5-20 units. Mechanisms, seed 1:
- Melon: on day 10 each of my units waters and harvests one tile, then walks to the
  neighbouring melon (URGENT priority at distance 1 beats the deposit at distance 3) and
  harvests it too, so the first sale lands at hour 12 (4 units) and hour 13 (29) against
  v5's hours 9-13 (48 units); 14 of mine go on day 11 at $114. Three of my twelve melons
  carried 4 units and two carried 5: waterings on melon tiles were 8, 11 and 9 of 12 on days
  7, 8 and 9 (v5: 12 every day; a one-time crop starts at 1 unit and gains one per watered
  day in its window, ages 6-12 for melon, so five waterings make 6).
- Wheat: I plant 125 wheat tiles to v5's 172 and harvest 1.7 units per tile to its 2.0; the
  daily tile census shows 1-9 empty tiles at hour 0 on most days from day 12 (v5: 0 until its
  tomato land opens), 1-6 standing weeds from day 23 (v5: 0-1), and carrots on every
  non-strawberry tile on days 24-26 (39 carrots to v5's 29) while v5 keeps 27-38 wheat tiles
  to day 27.
- Fertilizer: collected 359 to v5's 367, but v5 sells 347 and spreads 103, so its tape also
  buys fertilizer (about 80 units; the gross column overstates its net by that spend).
- Tomato: v5's route V219 (below), seed 1 only.
Reading: the competition gap is mostly production (wheat, fertilizer, strawberry and milk
units), and the pure timing part (melon price, strawberry price in the first five days of the
season) is 6-8k, not 25k. **Decision:** melon day first, because its mechanism is fully read;
then the executor's idle tiles and walking; the market layer after, since against a daily
dumper the strawberry inventory reaches the floor from day 19-20 whatever I hold (the price
falls $1.92 a unit above the anchor and v5 alone adds 25 a day against a drain of 13).

### Note: v5's two route switches, traced in its code
`_v219_qualifies` (day 18): NW, NE and SW unlocked, money at least 12,000, tomato price at
or above its minimum, at least three Pizza Shop or Farmers Market instances among the
unlocked shops, SE locked, no tomatoes anywhere: it buys SE, ten tomato seeds and extra
hands, fertilizes on days 24 and 27, and sold 80 tomatoes at $169 on seed 1 (13.5k).
`_v233_eligible` (day 12): at least two Yarn Stores, wool at $220 or more, wheat at $45 or
less: it buys SE and six more sheep (the seed-3 17-sheep route). The previous entry's
"tomatoes against my mirror" is consistent with the shop trigger rather than the mirror
detector (`_r37_similarity` only reorders sales): the shops in the pass game and the mirror
game differ through P22, and that difference was not checked (not verified).

### Decision: change A (melon-window watering at priority -6) rejected
Applied alone to the committed executor, on the old three-and-five-seed yardstick:
production 147,885 (from 158,165), competition 0-10 with margin -35,721 (from -24,736; part
of it the shop draw). Seed 1 census: FEED 292 (from 357), CARE 319 (353),
COLLECT_FERTILIZER 330 (359), NE bought on day 7 instead of 6; melon waterings did reach 12
of 12 on every day. A priority of -6 beats FEED (0) and COLLECT (5) from up to ten tiles
away, so the herd waited and the fertilizer that funds the land stayed on the pasture.
Reverted. Next: B (a melon-day crew: no morning feeders that day, and a unit carrying
melons walks straight to the shed), then A again at the WATER_MUST level.

### Checkpoint: change B (melon-day crew) accepted
On melon day (any melon-ready watering or harvest job present) no hand is a morning feeder,
and a unit carrying melons takes no job off its own tile until it has dropped them, with the
deposit at URGENT priority. Wide yardstick: production 141,490 (from 137,622), competition
0-20, mean bank 69,209 vs 95,781, margin -26,572 (from -28,861; v5's mean fell 3.3k, mine
1k, both within the shop-draw noise of P22). Seed 1 hour table: first melon sales at hour 9
(6 units at $266, the same turn as v5's 6) and hour 10 (15 at $247) instead of hours 12-13,
but 27 of 64 still went on day 11 at $128; the turn view of that day is next. The melon
waterings on days 7-9 are unchanged (8, 11, 9 of 12).

### Note: the production yardstick is half shop luck
Seed 5 against pass banks 99-104k because the town drew three Yarn Stores and no milk shop:
wool sold at $248 (153 units, 38.0k) and milk at $50 (179 units, 9.0k), against $137 milk
on seed 1. The eight-seed spread against pass is 99k to 177k for one executor. So
`scripts/arena.py` now records, per game, the shop list and the units harvested by product
(counted from HARVEST actions in the replay), which do not depend on prices; production
changes are judged on those columns as well as on the bank.

### Surprise: the melon haul stopped at every pasture on the way home
Turn view of day 10 on seed 1 with change B: the twelve units fanned out one per melon tile
by hour 4 and the first four loads sold at hours 9-10, but units 7, 8 and 10 spent hours
10-13 doing CARE, COLLECT and an animal HARVEST on the pastures at (4,2), (3,3), (2,4) and
(4,3) that lie between the melon field and the shed (an on-tile job costs no walk, so it
beat the deposit), and once the last melon tile was harvested the "melon rush" flag went
off, so a hand holding six melons ($1,140, under the URGENT deposit threshold) watered wheat
around NW until the day-end drop put its load into the shed for the hour-1 sale on day 11
(27 of 64 units at $128). B2: a unit carrying melons takes no job at all, on-tile or not,
until it has dropped them, on any day. `scripts/arena.py` now also records each game's shop
list and the units harvested by product; `results/arena.csv` restarts with the new header
(the old log is `results/arena_to_2026-09-16.csv`).

### Checkpoint: B2 measured by harvested units; the melon carriers skipped the herd
`scripts/arena.py` now prints, per run, the mean units harvested by product and a basket
value at the line's realized prices from analysis.md section 7 (melon 198, strawberry 116,
wheat 39, carrot 49, tomato 143, milk 84, wool 105, egg 55), which the shop draw cannot
move. Production, eight seeds against pass, B (committed) against B2 (melon carriers take
no job at all until they drop):

| executor | bank | basket | melon | strawberry | wheat | carrot | milk | wool | egg |
|---|---|---|---|---|---|---|---|---|---|
| B | 141,490 | 95,436 | 67 | 219 | 351 | 77 | 232 | 143 | 87 |
| B2 | 137,361 | 94,609 | 67 | 218 | 362 | 74 | 229 | 138 | 83 |

B's basket is higher on 6 of 8 seeds (paired mean +827); the shops differed on all eight
seeds, so the 4.1k bank difference is mostly P22. Competition, B2: 0-20, mean bank 72,564 vs
98,457, margin -25,893 (B: -26,572). The units B2 loses are milk, wool and egg: on melon day
the twelve carriers pass the pastures without CARE or COLLECT and no feeder exists that day
(B turned them off), so some animals go uncared at the lowest priority. B3 assigns the
feeders the turn the last melon job disappears; measured next with the basket.

### Decision: B2 kept, B3 rejected
B3 (feeders assigned the turn the melon rush ends) did not bring the animal units back:
basket 94,719, milk 223, wool 138, egg 86 (B2: 94,609 / 229 / 138 / 83; B: 95,436 / 232 /
143 / 87), competition margin -26,746 (B2 -25,893, B -26,572). The three margins sit inside
the shop-draw noise, and milk units themselves move with the draw because `needs_feed`
feeds daily only while milk is worth 1.2 wheat. B2 is kept as the simplest complete rule:
on seed 1 it sells all 64 melons on day 10 (6 at $266 in v5's turn at hour 9, 15 at $247,
25 at $193, 18 at $143) and v5's last 12 fall to $109 on day 11; melon revenue 12,700
against 11,593 before, v5's 15,084 against 16,196, a 2.2k swing on that seed. The two
late batches (hours 13 and 16) are the far tiles; the eight missing units are the days 7-9
waterings, which A' addresses next.

### Checkpoint: the three new high-vote agents are one family, and the shop draw is decoupled for A/B runs
Pulled under `data/notebooks/` (gitignored): tetsutani "Market-Smart Farming" (95 votes),
flexonafft "Multi-Route Farming Agent" (93), reyhanksatria "Dynamic Route Agent" (85). The
last two are byte-identical (`main.py` 329,112 bytes, md5 266b8f0e, 3,496 lines; one is the
other's archive republished), and tetsutani's is the same code plus a 73-line mirror-reorder
wrapper (329,591 bytes). All three carry the lineage markers "V41" and "EXP260"; v5 is
"EXP257", v6 "V44/V45". So the candidates for the next public line are a sibling generation
of the family, not a new agent; arena aliases follow once they have been replayed against a
recorded game for fidelity, as v5 and v6 were.

A' (melon-window watering at the WATER_MUST level) on coupled shops: basket 95,266 (B2
94,609), melon 72 (67), milk 218 (229), wheat 377 (362); competition margin -27,879 (B2
-25,893). Every one of those differences is inside the P22 noise, so the harness changes
first: `scripts/arena.py --decouple-shops` patches the engine's `_end_of_day` in the arena
process so each day's shop comes from a generator keyed by seed and day only (the weed draw
is untouched; the engine's own draw is suppressed by setting its shop cap to zero for the
call). `eval.sh` uses it for both yardsticks, so a rerun of the same seed now meets the same
town whatever the farm does; the ladder keeps the coupled draw, which is a random effect
there. The gauntlet scripts each tape's recorded shop sequence from its trace instead, so a
seat-0 recording now plays in its recorded weeds and its recorded town. **Decision:** B2 and
A' are re-measured under the decoupled draw before anything else is judged; the numbers
above are the last on the coupled draw.

### Surprise: the successor line routes on the first two shops with 28 searched tapes
Read in the V41/EXP260 `main.py` (flexonafft's, byte-identical to reyhanksatria's):
`_router` fires at step 144 (day 6) on the first two shops. Without a Yarn Store among them it
uses a table of 64 shop pairs mapping to 28 routes (ids 101-128; 21 pairs share route 105,
the rest are 1-5 pairs each; `_R108_DATA` decodes to 41 route tapes); with a Yarn Store it
falls back to the older V39 table (route 0 or 3). It keeps v5's V219 tomato route (three
Pizza Shop or Farmers Market instances, day 18) and V233 sheep route (two Yarn Stores, day
12), and adds layers R70-R148, a "RACE" layer that detects a rival dropping the same
product into the market without a sale of its own and quotes at the drop for the rest of
the game, and a turn-0 wheat round trip changed to one large order so a rival's round trip
cannot leave it a melon seed short. So the plateau's next generation carries a searched
plan for every first-two-shop draw, which is the breadth of shop response the study found
only among the leaders (analysis.md section 3). Consequences: (1) the competition yardstick
should add this router (alias `line:v41`) once its fidelity against a recorded game is
checked as v5's was; (2) Phase 2a's "follow the town" has to be at least as broad as this
table to matter against the line the final tournament will meet. Not measured yet against
our agent (the arena is running the decoupled re-baseline).

### Checkpoint: decoupled baseline, and A' accepted
Under `--decouple-shops` a seed's town is the same for every executor (checked on seed 1:
both executors met SMOOTHIE, YARN, BRUNCH, BRUNCH, SMOOTHIE, PET_CAFE x3). The numbers
below are the new baseline and the first change judged on it:

| executor | production basket | production bank | competition basket | mean bank vs v5 | margin |
|---|---|---|---|---|---|
| B2 (committed) | 92,896 | 144,546 | 94,531 | 84,688 vs 112,130 | -27,442 |
| A' (melon-window watering at the must level) | 94,713 | 146,208 | 95,276 | 85,076 vs 111,346 | -26,270 |

A' harvests 72 melons in both yardsticks (68 and 66 before), 5 more strawberries and 11 more
wheat against pass, 3 fewer milk; both gates pass, so it is kept. The decoupled towns on
seeds 0-9 are richer than the coupled ones were (both banks about 12k higher), so the
margin, not the bank, is comparable with earlier entries. Next, one at a time on this
baseline: E3 (carrots only on the freed strawberry tiles, wheat elsewhere to day 27), E1
(exhausted strawberries dug at planting priority), E2 (planting until hour 22), S (a unit
keeps its walking target unless another job beats it by 1.5).

### Checkpoint: E3 accepted (carrots only on the freed strawberry tiles)
Production basket 94,896 (A' 94,713), bank 147,416 (146,208): wheat 408 (358) against
carrots 39 (80), so the basket is flat and the bank gains 1.2k because the extra carrots
had been selling below their basket price. Competition margin -25,644 (-26,270), mean bank
85,726 vs 111,370. Both gates pass; kept. The executor now plants carrots on days 24-26 on
the strawberry tiles only, which is the plan `agent/plan.py` documents and what v5's tape
does (31 carrots, 27-38 wheat tiles to day 27).

### Checkpoint: E1 accepted (an exhausted strawberry is dug at planting priority)
Production basket 95,002 (E3 94,896), bank 147,474 (147,416), wheat 413 (408); competition
basket 95,672 (95,352), margin -25,291 (-25,644), mean bank 86,038 vs 111,329. Both gates
pass by small amounts; kept. Standing weeds late in the game were exhausted strawberries
waiting for a DIG that ranked below everything else (priority 3.5); the tile is a wheat
planting, so the dig now ranks with a planting (1.0).

### Surprise: the multi-route family is already the plateau, hidden by the day-5 hash
Hashing every V41 route tape's farmer-and-hand stream with the study's convention
(`research.trace.split_streams`, `stream_hashes`) and matching against
`data/top10/features.parquet` (14,788 seat rows): all 40 shop routes and the old routes share
one field line through turn 136, and it is G11 (4,895 seats, 1,089 teams, 2026-09-09 to
09-15). They part after the day-6 router. At turn 200, 4,358 seats (1,056 teams) match one of
12 V41 lines; at turn 300, 3,365 seats (951 teams) match one of 24; at turn 400, 967 seats
(549 teams) match one of 30. At turn 300 the v5-style routes 0 and 2 carry 1,485 seats (662
teams; Catalyst 154, doubao 43, ElephtAI 43) and the shop-pair routes 101-128 about 1,300
(route 123 alone 410 seats and 205 teams; the route-105 group 409 seats and 109 teams;
elmo, Tom&Jerry, Thomas Tschinkel, Emile Andrieu, nilochan, yomogii among the top carriers).
So section 4's G11 generation was never one plan: from 2026-09-09 the plateau has been a
family that picks one of 28 searched routes from the first two shops, and section 3's
"the family follows only the Yarn Store" is true of v5's router and false of the family's
majority. The exact matches through turn 400 on hundreds of seats are a stronger fidelity
check of the route tapes than one replay; the runtime layers on top are the same lineage
as v5's. `scripts/arena.py` gains `line:v41` (flexonafft's `main.py`), and the competition
yardstick will report against v5 and v41 both once the executor queue is through.

### Decision: E2 (planting until hour 22) rejected
Production basket 95,162 (E1 95,002) and bank 147,586 (147,474), but competition basket
95,260 (95,672) and margin -26,448 (-25,291), mean bank 85,130 vs 111,578. With the towns
fixed the competition move is the change itself, not the draw: a plant set at hour 22 needs
its watering at 23 from a unit that is often elsewhere, and a missed one weeds the tile.
Reverted; the executor stays at E1. Next: S (a unit keeps its walking target unless another
job beats it by 1.5), then the successor line as a second competition opponent.

### Checkpoint: S accepted (a unit keeps its walking target unless another job beats it by 1.5)
Production basket 95,566 (E1 95,002), bank 148,836 (147,474); competition basket 96,754
(95,672), margin -24,516 (-25,291), mean bank 86,667 vs 111,183. Both gates pass; kept. The
previous session removed a sticky-target hook that had only ever been tried at zero; at
-1.5 it stops units re-targeting each other's jobs every turn. A stronger value is a later
single change. Executor queue done for now: B2, A', E3, E1, S kept; E2 rejected. Baseline
for what follows: production basket 95,566, competition margin -24,516 against v5.

### Checkpoint: the successor line and the gauntlet with scripted towns
Executor at S (commit c552018), decoupled shops, seeds 0-9 both seats: against `line:v41`
0-20, mean bank 85,410 vs 111,340, margin -25,930 (against v5 the same day: 0-20, -24,516).
The gauntlet, 80 seat-0 recordings of the top five and three gold teams, each played in its
recorded town (80 of 80 matched), our agent in seat 1:

| team | W-L | our bank | their bank | their recorded opponent's bank | their bank when recorded |
|---|---|---|---|---|---|
| Artem The Farmer | 0-10 | 85.7k | 119.1k | 96.5k | 107.9k |
| Majkel1337 | 4-6 | 99.9k | 104.4k | 101.2k | 112.9k |
| Unknown Mother-Goose | 0-10 | 86.6k | 125.6k | 97.6k | 119.8k |
| DSM | 7-3 | 102.5k | 84.0k | 90.1k | 99.6k |
| SpaTaro | 2-8 | 89.7k | 95.5k | 81.7k | 94.8k |
| HowardLeeTW | 0-10 | 84.4k | 114.6k | 96.6k | 102.0k |
| carbonapi | 0-10 | 80.0k | 118.2k | 99.6k | 104.3k |
| Ebi | 0-10 | 89.1k | 120.5k | 102.8k | 105.1k |

13-67 (16%), against 26-54 in the previous session's run, whose towns were drawn at random
relative to the tapes' plans (P22) and handicapped them. Two readings. First, six of the
eight recordings bank 10-15k more against us than they did against their real opponents,
and our bank is 5-20k below those opponents', so a recording that cannot react still
out-produces us and is left unpressed in the market: the gap is production and market
both. Second, DSM and SpaTaro make 8-16k less against us than when recorded, so where
our sales do land on the same products they hurt a tape. The answer to "do we stand a
chance" is unchanged: not yet, and the distance to the top five is 15-40k a game.

**Assessment.** After two sessions the runtime executor sits about 5-10% below the line's
searched tapes in units and has no market layer beyond selling what reaches the shed;
the plateau's own agents, the leaders included (Artem's line is a tape on other teams'
seats, section 4), are searched tapes under runtime layers, and the multi-route family's
tapes match 3,365 sampled seats through turn 300. Against that, the memo's market rules
(sell first, meter at the drain, deny) are skeleton-independent: they decide when the shed's
stock is sold, whatever put it there. **Decision:** build the market layer next as a module
that works on top of any skeleton, measure it on ours against v5 and v41, and then run the
architecture question as an arena experiment before the handoff: v41's tapes under our
market layer against plain v41, in mirror seats. If the tapes-plus-layer wins by the
leaders' 8-14k margin (section 9b) while our runtime skeleton does not, the handoff will
say so plainly and recommend switching the skeleton; that is a change to the plan Iminabo
saw and is flagged as such, not made silently.

### Decision: the opponent-aware metering is built, measured, and switched off against the line
`agent/market.py` now estimates the opponent's selling rate per premium product from the
market inventory's turn-to-turn change net of the town's drain and our own orders
(`opponent_rate`), and `metered_quantity` sells only into the room the drain leaves after
the opponent, holding at most what that room can still take before day 28. With it on
(`METER = True`), executor at S, decoupled shops:

| yardstick | METER off | METER on |
|---|---|---|
| production vs pass, bank / basket | 148,836 / 95,566 | 149,903 / 95,317 |
| competition vs v5, mean bank, margin | 86,667 vs 111,183, -24,516 | 87,041 vs 112,987, -25,946 |
| competition vs v41, mean bank, margin | 85,410 vs 111,340, -25,930 | 86,014 vs 113,263, -27,249 |

Against pass, where nobody floods the market, it earns 1.1k; against the line it raises
our bank by 0.4-0.6k and the line's by 1.8-1.9k, so the margin falls 1.3-1.4k. Holding
stock hands a daily dumper a recovered price: that is the out-earn pattern of section 9b
(Majkel1337's opponents keep their bank), and the ladder scores wins. Artem's "denial" is
not holding either: it sells 7-12 strawberries a day from fewer tiles (24-29), so its steady
supply is what the line's bulk dump lands on. On our 33-tile skeleton there is no steady
rate to sell at without holding. `METER` stays off; the estimator stays for opponents who
do not dump, and the production mix (fewer strawberries, more staples) is the lever the
data points to, which is a skeleton change, not a market one.

**Decision (architecture experiment):** the tape-plus-metering wrapper would only repeat
this result, so the experiment that answers the skeleton question is a hybrid: v41's tape
and layers for the first N days, then our runtime executor and market from hour 0 of day
N. The margin against plain v41 as N grows shows where our executor falls behind the
searched tapes; N = 6, 10, 13, 16 are run next.

### Surprise: the whole gap to the line sits in the second half of the game
Hybrid agents (v41's tape and layers for the first N days, then `agent.policy.act`) against
plain v41, seeds 0-9 both seats, decoupled shops:

| tape for days | our bank | v41's bank | margin | our basket |
|---|---|---|---|---|
| 0 (our agent) | 85,410 | 111,340 | -25,930 | 96,616 |
| 6 | 85,845 | 110,035 | -24,190 | 97,372 |
| 10 | 85,764 | 107,548 | -21,784 | 97,130 |
| 13 | 85,540 | 102,763 | -17,223 | 98,382 |
| 16 | 85,644 | 101,543 | -15,899 | 98,653 |

Our bank does not move with N (85.4-85.8k); v41's falls as our seat's sales coincide with
its own for longer. With the farms identical through day 16, the one that keeps the tape
banks 101.5k and the one that switches to our executor and market banks 85.6k, although
its harvest basket is 2k higher than our own agent's. So the opening and the melon day are
at parity with the searched tapes, and about 16k, the whole of the remaining gap, is lost
in days 16-29: the strawberry season, the wheat cycles, carrots and the end game, and the
prices they fetch. The single game that follows says which.

### Checkpoint: what the second half loses, on one seed
Hybrid-16 against v41 on seed 1 (decoupled town SMOOTHIE, YARN, BRUNCH, BRUNCH, SMOOTHIE,
PET_CAFE x3; both farms on the sheep route): identical banks through day 15 ($25,367 at
day 15 hour 0), then ours 97,274 against v41's 110,669. Executed sales, whole game, ours
against v41: strawberry 232 at $191 against 248 at $194 (-3.6k), wheat 315 against 416
(-4.2k), carrot 48 against 96 (-2.6k), milk 174 against 183 and wool 228 against 236
(-1.7k together), fertilizer 288 against 348 (v41 buys fertilizer, so that column is
inflated), egg +0.7k; gross 127.1k against 138.2k. The tile census from day 16: ours shows
1-8 empty tiles at hour 0 on most days, 1-3 standing weeds from day 23, and wheat left past
age 4 (a ready wheat is harvested only once watered that day, and the watering often comes
too late for the harvest to follow); v41 shows no empty tiles, no late wheat, and a
steady pipeline of 6-8 young and 17-19 window-age wheat tiles. Ops from day 16: our CARE
344 against 398, FERTILIZE 85 against 101, PASS 419 against 606, moves 3,360 against 3,104.
Reading: the second half is a labour-scheduling gap (wheat cycle, care, fertilizing) plus
one plan choice (carrots: the route plants 29 on the freed tiles and keeps them coming; our
E3 rule plants fewer). Two single changes follow: CARE at a value-based priority, and a
late-hour harvest of ready wheat.

### Decision: C1 (CARE at priority 2.0) rejected, and what it showed about sale hours
Production basket 96,358 (S 95,566) and bank 151,796 (148,836), strawberries 234 (220),
eggs 95 (89); but competition margin -27,216 (-24,516) with our mean bank unchanged
(86,665 against 86,667) and v5's up 2.7k (113,880 against 111,183). With the towns fixed
and weeds negligible, a change in our own priorities can move v5's bank only through the
market, and the plausible route is timing: caring before collecting delays our milk and
wool into the shed, so they sell after v5's hour-1 lots (its day-end drop) instead of
alongside them, and v5 takes the higher price on the same units. Reverted. The converse is
the next single change after W1: collect animal products late in the day so the free
day-end drop sells them at hour 1 in the same turn as the line's (A2).

### Checkpoint: W1 accepted (ready wheat harvested from hour 18 without that day's watering)
Production basket 96,041 (S 95,566), bank 149,710 (148,836), wheat 408 (400); competition
basket 96,514 (96,754), margin -24,022 (-24,516), mean bank 86,858 vs 110,881. Both gates
pass; kept. A wheat at its ready age no longer waits past nightfall for a watering that
adds one unit; the tile is freed for tonight's replanting instead.

### Decision: A2 (animal products collected from hour 16) rejected; the hour matters the other way
Production basket 95,043 (W1 96,041), bank 148,339 (149,710); competition margin -28,388
(-24,022), our mean bank 86,128 (86,858), v5's 114,516 (110,881). Deferring the collection
so the day-end drop sells milk and wool at hour 1 hands v5 3.6k: our units then land
after v5's daytime lots of the same day, not beside its hour-1 lot. Together with C1
(caring before collecting, v5 +2.7k), both changes that put our animal products into the
market later raised v5's bank, so the mirror rule is tested next as A3: collect milk, wool
and eggs first thing in the morning, before feeding and caring.

### Decision: A3 (animal products collected first thing in the morning) rejected
Production basket 95,228 (W1 96,041), bank 148,743 (149,710); competition margin -25,784
(-24,022), our mean bank 85,567, v5's 111,352, wheat 400 against 439: collecting before
feeding displaced the morning's feed and field work. Reverted. So a priority change on the
collection hour fails the gates in both directions, and what raised v5's bank under C1
and A2 (2.7k and 3.6k with our own bank nearly unchanged) is not explained by "our animal
products later"; it stays an open question for a per-hour sales comparison of those two
runs, not a finding.

### Checkpoint: end of the second build session
State at commit: executor with B2 (melon carriers haul straight home), A' (melon-window
watering at the must level), E3 (carrots only on freed strawberry tiles), E1 (exhausted
strawberries dug at planting priority), S (sticky walking targets, -1.5) and W1 (ready
wheat harvested from hour 18); E2, C1, A2 and A3 rejected; the opponent-aware metering
built in `agent/market.py` and off. Yardstick (`scripts/eval.sh`, decoupled shops,
harvest basket): production basket 96,041, bank 149,710 on seeds 1-8; competition against
v5 0-20, mean bank 86,858 vs 110,881, margin -24,022 (the session's decoupled baseline was
-27,442). Against v41: 0-20, -25,930, measured at S and not re-run after W1. Gauntlet in
recorded towns: 13-67 (16%) at S. 13 tests pass; `scripts/package.py` builds and
self-plays the bundle. Harness: `--decouple-shops`, per-game shop list and harvested units,
the basket, `line:v41`, scripted towns in the gauntlet. Phase 1's acceptance (parity with
the line) is not met, and no submission has been made.

What the day established, in order of weight: (1) the town's shop draw is coupled to both
farms' empty tiles (P22), so the earlier yardstick was noisy by about 10k a seed; (2) the
plateau is the multi-route family, whose route tapes match 3,365 sampled seats through
turn 300; (3) our opening and melon day are at parity with the searched tapes and the
whole gap to the line sits in days 16-29 (hybrid curve: our bank 85.4-85.8k for every N,
the tape's 101.5k from the same day-16 farm); (4) the second half loses on the wheat
cycle, the carrot count, CARE and FERTILIZE counts, and sale hours; (5) holding stock
against a daily dumper loses margin, so metering is off against the line.

Next, in order: (1) Iminabo's decision on the skeleton (memo amendment 6: path (a) keep
closing the second half of our executor, path (b) v41's tape for days 0-16 and our agent
after, which is -15.9k against v41 today); (2) under either path, the second half: carrots
sized to the town's carrot drain (Pet Cafe, Farmers Market) on the freed tiles, FERTILIZE
coverage of every strawberry production age (85 against the tape's 101 from day 16), the
idle tiles at hour 0 (seed purchases stop at hour 20 and planting at 21), and the per-hour
sales comparison behind C1 and A2; (3) after each accepted layer, eval.sh against v5, the
v41 run, and the gauntlet; (4) Phase 2a's Yarn Store and tomato routes, gated against v41
on the seeds that draw those shops; (5) the notebook watch every few days; (6) still not
verified: the competition rules page (last read 2026-09-14), the 31 last-step money
mismatches, the leaders' CARE dip on days 17-26, v41's runtime layers against a recorded
game (only its tapes are hash-verified), and no game against a live adaptive opponent
other than v5 and v41.

### Note: the yardstick runs in 44 seconds at six workers; nothing here uses the GPU
Iminabo asked whether the RTX 5070 is used. It is not and cannot be: every arena game is
the kaggle-environments engine in single-threaded Python and the agent is rule-based, so
the only speed lever is CPU parallelism. The machine has 8 cores, 16 threads and 31 GB;
the eight production games take 15 s at three workers and 10 s at six with identical
results, and a full `eval.sh` (28 games) takes 44 s at six. `eval.sh` now uses `--jobs 6`.
The previous session's 1,200-second timeout came with `deep.py` and three other processes
running at once; six arena workers alone are within memory. The four-to-five-minute waits
recorded during today's evals were the background-task plumbing, not the games.

### Decision (Iminabo): run both paths and see which works
Iminabo, on the memo's amendment 6: "can't we do both and see which works". So the hybrid
becomes a real agent in the package (v41's `main.py` bundled verbatim as
`agent/line_v41.py` under its Apache-2.0 notices, `agent/hybrid.py` switching from the tape
to our runtime agent at `plan.TAPE_DAYS`), and both paths are measured with the same
yardsticks: `TAPE_DAYS = 0` is our executor alone, 16-24 the hybrid, 29 the tape alone. The
hybrid is also the instrument for the executor work, because with identical farms until
the switch its margin against v41 measures our play after that day against the tape's.

### Checkpoint: both paths measured; the hybrid wins, and the later the switch the better
Decoupled shops, seeds 0-9 both seats, the packaged hybrid with the switch day varied:

| tape for days | vs v41: our bank, v41's, margin | vs v5: our bank, v5's, margin | basket vs v41 |
|---|---|---|---|
| 0 (our executor) | 85,762 / 111,560 / -25,798 | 86,858 / 110,881 / -24,022 | 96,761 |
| 16 | 85,652 / 101,808 / -16,156 | 86,667 / 99,586 / -12,918 | 98,406 |
| 20 | 88,411 / 100,597 / -12,185 | 90,018 / 98,278 / -8,260 | 99,037 |
| 24 | 91,073 / 99,052 / -7,979 | 92,990 / 96,688 / -3,698 | 102,531 |

Production against pass at switch day 16: bank 156,798, basket 98,236. Gauntlet at switch
day 16, recorded towns: 22-58 (28%; 13-67 for our executor alone): Majkel1337 9-1 (our
130.6k against its recording's 41.4k) and DSM 8-2 (130.7k against 37.9k), whose recorded
plans collapse against the tape's sales; Unknown Mother-Goose 2-8 (104.3k against 104.3k),
SpaTaro 3-7; Artem, carbonapi, Ebi and HowardLeeTW 0-10 at 87-89k against 108-112k.
Reading: our executor is behind the tape's play in every stretch after day 16, by about
4k for days 16-20, 4k for days 20-24 and 8k for days 24-29 against v41. The package now
ships with `TAPE_DAYS = 24`, the best measured, and the executor work targets the end game
first.

### Surprise: the end game is carrots and a last-day wheat dump
Switch day 24 on seed 1 (town SMOOTHIE, YARN, BRUNCH, BRUNCH, SMOOTHIE, PET_CAFE x3),
identical farms through day 23 ($84,603 at day 24 hour 0), then ours 101,893 against
v41's 107,740. From day 24 the tape plants carrots on 4, 18, 29, 24 and 12 tiles (days
25-29 census) and stops planting wheat, so it sells 74 carrots at $55 on day 29 and winds
its wheat down on days 27-28 (54 and 34 units at $30 and $24); ours plants 3, 11, 19, 18, 8
carrots (E3 keeps them to the freed strawberry tiles), plants 17 wheat on day 27, and dumps
89 wheat at $21 on day 29 (v41: 64), with 6 empty tiles and 3 weeds on days 25-26 (v41: 0).
Whole-game sales from the same day-24 farm: carrots 49 against 94 (-2.5k), strawberries
238 against 248 (-1.5k), wheat 376 against 401 (-0.8k). A carrot planted on day 24-26
yields 3 units by day 27-29 ($165 with a Pet Cafe, about $75 without) against a wheat
planted on day 27 yielding 2 units ($42), so E4 next: carrots on every free tile on days
24-26 when the town has a carrot shop (Pet Cafe or Farmers Market), measured at switch
day 24 against v41 and v5.

### Decision: E4 (carrots on every free tile on days 24-26 in carrot towns) rejected
Switch day 24: against v41 margin -8,118 (-7,979 without), against v5 -4,356 (-3,698);
carrots 80 (38), wheat 481 (533), basket 101,843 (102,531). The extra carrots did not pay
for the wheat they displaced, so the tape's end-game edge is not the carrot count alone;
the idle tiles on days 25-26, the last-day wheat dump and the strawberry tail remain the
candidates, each to be measured at switch day 24 where the farms are identical until then.

### Checkpoint: gauntlet at switch day 24, and the state that ships
Recorded towns, 80 games: 29-51 (36%). DSM 10-0 (our 138.5k against its recording's 37.3k),
Majkel1337 10-0 (137.3k against 40.8k): both recorded plans sell into the tape's schedule
and collapse. Unknown Mother-Goose 4-6 (109.6k against 102.5k), SpaTaro 4-6 (93.4k against
89.2k), Ebi 1-9 (95.1k against 105.7k); Artem 0-10 (90.1k against 107.7k), carbonapi and
HowardLeeTW 0-10 (91.5k against 104-106k). The progression today: 13-67 with our executor
alone, 22-58 with the tape for 16 days, 29-51 with the tape for 24. Against a recording of
the #1 we are still 17.6k short in every game.

State at commit: `main.py` is the hybrid, `TAPE_DAYS = 24` (v41's tape and layers for days
0-23, our runtime agent from day 24), tests 13 of 13, package 148 KiB. Yardstick at this
setting: against v41 0-20, margin -7,979 (our bank 91,073 against 99,052); against v5
0-20, -3,698 (92,990 against 96,688); gauntlet 29-51. No submission has been made.

Next, in order: (1) the end game at switch day 24 is the cleanest gate (identical farms
until then): the idle tiles on days 25-26, the last-day wheat dump against a wheat cut-off
at day 25, the strawberry tail, and the liquidation hour, one change at a time, each
measured against v41 and v5 at switch day 24; (2) once our day-24-onwards play beats the
tape's, move the switch earlier (20, then 16) and repeat with the losses named for those
stretches; (3) the market layer on top of the tape's opening, where the tape's own sale
hours are now ours to change from the switch day; (4) Phase 2a on top of the tape's
routes; (5) the notebook watch, since the tape we bundle is the plateau's current
generation and will be replaced.

### Checkpoint: where the hybrid would stand if submitted (Iminabo's question)
Packaged agent (TAPE_DAYS = 24) under the ladder's own coupled shop draw, fresh seeds
10-29, both seats: against v41 0-40, mean bank 88,628 against 98,781, margin -10,153;
against v5 1-39, 89,057 against 94,046, margin -4,989. So on ladder conditions the hybrid
loses to the plain public line almost every game. The final ranking is a Bradley-Terry
over post-deadline games (competition facts, memory), in which an agent that loses to a
block of near-identical agents ranks below the whole block; the line's block is the
plateau (its day-5 line is on 1,089 sampled teams' seats, from rank 9 through silver into
bronze on the running ladder). Estimate, not measured: a submission today would land below
the plateau, in silver or bronze, and the plain tape alone (TAPE_DAYS = 30) would land
mid-plateau. Iminabo's rule stands: no submission until the gauntlet says we stand a
chance; the entry deadline of 2026-09-23 still requires some submission to exist by then.

## 2026-09-17

### Checkpoint: days 24-29 from the same farm, ours against the tape, op by op
Seed 1, switch day 24 (identical farms at day 24 hour 0). Harvested units by day, ours /
v41: strawberries 7, 20, 0, 20 / 7, 25, 0, 26 on days 24-27 (both harvest on the
production days; the tape's are doubled on five more tiles: it FERTILIZEs 11 strawberries
on day 24 to our 6); wheat 32, 41, 32, 16, 14, 72 / 37, 42, 55, 36, 44, 19 (the tape
fertilizes wheat 17 times on days 24-26 to our 3, harvests six-unit tiles on days 26-28,
and does not dump on day 29; ours dumps 72 at two to four units); carrots 0, 0, 0, 3, 28,
18 / 0, 0, 0, 17, 39, 37 (the tape has 18 carrot tiles at day 26 and 29 at day 27, ours 11
and 19, because it plants carrots on freed wheat tiles as well and stops replanting
wheat). Ops per day: CARE 6-13 / 15-17 (all 17 animals every day); FERTILIZE 27 / 40 over
days 24-28 while both collect about 75, so we sell 50 fertilizer at $1-15 that the tape
spreads; hands 11-12 / 13 on days 24-26; moves 157, 132, 134, 116, 177 / 121, 136, 130,
105, 135 with the tape still idling 5-24 unit-turns a day. Candidates measured alone at
the switch-day-24 gate (40 games, against v41 and v5): W2 wheat cut-off day 25, F2
strawberry fertilize at -2.0, L1 liquidation hour 16, S2 sticky -3.0; then FW wheat and
carrot fertilize at 1.5 with age 3 allowed, FR fertilizer reserve 60, H3 13 hands on days
24-27, C1 care at 2.0.

### Checkpoint: end-game candidates, first batch; W2 accepted
Switch-day-24 gate, each alone on the committed agent (baseline -7,979 against v41,
-3,698 against v5): W2 (no wheat planted after day 25) -7,066 and -3,139, kept; F2
(strawberry fertilize at -2.0) -8,589 and -4,377, rejected; L1 (liquidation from hour 16)
-9,638 and -4,844, rejected, its basket rose 800 but the later harvests sold worse; S2
(sticky -3.0) -7,922 and -3,529, a few hundred better, re-tested on top of W2 next. F2's
failure with the tape spreading 40 fertilizer to our 27 says the shortfall is the
fertilizer in hand rather than the job's rank, so the second batch carries the reserve
(FR) and the wheat and carrot fertilize rules (FW) as well as S2, H3, C1 and L0.

### Checkpoint: second batch, partly; a hang under FW
On top of W2 (baseline -7,066 against v41, -3,139 against v5): S2 (sticky -3.0) -7,169 and
-2,863, mixed, rejected. FW (wheat and carrot fertilize at 1.5, age 3 allowed) hung: its
20-game run against v41 produced nothing for 88 minutes with six workers alive, and the
runner's output was invisible because the grep in its pipeline block-buffers. The
processes were stopped, the tree reverted; FW is being run seed by seed with a timeout to
find the hanging game, since an agent that can hang would be timed out on the ladder.
The runner will write unbuffered to a file and give each run a timeout from here on.

### Checkpoint: third batch on W2; H3 accepted, C1 passes at this gate
Switch-day-24 gate on W2 (baseline -7,066 against v41, -3,139 against v5, basket 102,168):
FW (wheat and carrot fertilize at 1.5, age 3 allowed) -7,308 and -3,191, rejected; FR
(fertilizer reserve 60) identical to the baseline, the cap never binds, dropped; H3 (13
hands on days 24-27, as the tape hires) -6,834 and -2,473 with basket 104,202, kept; C1
(care at 2.0) -6,537 and -2,449, better on both, so the full-game rejection this morning
was a days-0-23 effect and it is re-tested on top of H3 now; L0 (liquidation from hour 12)
-7,398 and -3,399, rejected. The earlier "hang" under FW was a worker-pool stall, not the
agent: FW plays seeds 0-4 in 6-9 s each. Follow-ons queued: H4 (14 hands on days 24-27)
and E2e (planting and seed purchases to hour 22 from day 24 only).

### Checkpoint: fourth batch on W2 and H3; C1 accepted
Baseline -6,834 against v41, -2,473 against v5, basket 104,202. C1 (CARE at 2.0) -6,154
and -1,958, kept: a care is worth about $40 a day per cow and the old 4.0 ranked it last.
H4 (14 hands on days 24-27) -7,740 and -3,546, rejected, basket up 900 but the fourteenth
hand costs 377 a day; E2e (planting and seed purchases to hour 22 from day 24) -7,158 and
-2,930, rejected. End-game stack so far: W2, H3, C1, from -7,979 and -3,698 to -6,154 and
-1,958 at switch day 24. Note on C1: the full-game gate rejected it this morning through a
days-0-23 effect, so it holds only while the package switches at day 24 or later; a move
of the switch earlier re-tests it.

### Checkpoint: fifth batch on W2, H3 and C1; C3 accepted
Baseline -6,154 against v41, -1,958 against v5, basket 104,219. E4 (carrots on every free
tile in carrot towns) -8,063 and -3,536, rejected for the second time; C3 (carrots
plantable through day 27, two units on day 29) -5,682 and -1,229 with basket 105,186,
kept; D3 (haul threshold 250) -6,108 and -1,682 and H2 (late harvest from hour 15) -6,103
and -1,904, both a little better, re-tested on top of C3 with C5 (carrots from day 23 on
the freed strawberry tiles). End-game stack: W2, H3, C1, C3: from -7,979 and -3,698 to
-5,682 and -1,229 at switch day 24.

### Checkpoint: sixth batch; D3 accepted, the end-game pass closes
On W2, H3, C1, C3 (baseline -5,682 against v41, -1,229 against v5): D3 (haul threshold
250) -5,606 and -1,029, kept; H2 (late harvest from hour 15) -5,756 and -1,349, rejected;
C5 (carrots from day 23) identical to the baseline, no strawberry tile is free that day,
dropped. End-game stack at switch day 24: W2, H3, C1, C3, D3, from -7,979 and -3,698 to
-5,606 and -1,029 (our mean bank 92,144 against v41's 97,750; 94,243 against v5's
95,272). Rejected on the way: F2, L1, S2, FW, FR (no effect), L0, H4, E2e, E4 (twice),
H2, C5. Tests 13 of 13; package builds and self-plays. Still 0-20 against both lines at
this switch day; the remaining 5.6k against v41 sits in days 24-29 and the next candidates
from the op comparison are the strawberry doublings (11 against 6 fertilized on day 24)
and the fertilizer that is sold at $1-15 instead of spread. The gauntlet and the
ladder-style coupled run were not repeated after this stack.

### Checkpoint: the D3 stack under ladder conditions (Iminabo's question)
Coupled shop draw, fresh seeds 10-29, both seats: against v41 0-40, mean bank 90,264
against 97,496, margin -7,231 (before the end-game pass: 0-40, -10,153); against v5 8-32,
91,047 against 93,201, margin -2,154 (before: 1-39, -4,989). The end-game pass moved the
ladder-style margin by about 2.9k against both lines and turned the v5 matchup from one
win in forty to eight, but the multi-route family, which is the ladder's majority, still
wins every game by about 7k. Standing estimate unchanged: below the plateau, silver or
bronze in a final Bradley-Terry, not top 10; no submission.

### Milestone: first submission (Iminabo: "Submit this let's see")
2026-09-17 02:12Z, Kaggle submission 56291900, `submission.tar.gz` rebuilt from commit
8444506 (148.2 KiB, 9 files: main.py, agent/{__init__,executor,hybrid,line_v41,market,
plan,policy,tape}.py), message "hybrid: v41 tape days 0-23, runtime agent from day 24 (W2
H3 C1 C3 D3), commit 8444506". Status PENDING at submission; 4 submissions remain today.
This overrides the no-submission rule of 2026-09-16 by Iminabo's decision; the local
reading stands (0-40 against v41 and 8-32 against v5 under ladder conditions), so the
ladder result is the test of that reading. Check with `uv run kaggle competitions
submissions -c kaggriculture`; the entry deadline of 2026-09-23 is now met and the final
uses the last two active submissions at 2026-09-30.

### Note: rating thresholds for the medal zones (Iminabo's question), and the submission's first status
Public leaderboard downloaded 2026-09-17 about 02:20Z (`kaggle competitions leaderboard
--download`): 9,288 teams, so under Kaggle's rule for 1,000+ teams gold ends at rank 29
(10 + 0.2%), silver at 465 (5%), bronze at 929 (10%). Scores at those ranks: rank 1 3,170,
rank 10 3,005, gold cut 2,929, silver cut 2,666, bronze cut 2,432. Submission 56291900
validated (status COMPLETE) with an initial score of 1,419.3, the starting point a new
submission climbs from as it plays (Majkel1337's current submission went 651 after game 1,
2,543 after 25, 3,097 after 100, memo finding 6); it says nothing yet.

### Decision (Iminabo): pull every game of the gold zone, about 10 GB, no RL yet
Iminabo, 2026-09-17: "Do rl with only gold. Don't do the rl but just pull all the gold
until we have like 10gb of data. Don't skip anything." So: a replay dataset of the gold
zone's games for a later learning run; nothing is trained now. Scope: the 29 teams at
ranks 1-29 on the board downloaded 2026-09-17 about 02:20Z (gold = 10 + 0.2% of 9,288),
every submission the crawl can find for each and every public game of those submissions
(the crawl keeps two-agent public games; a submission's validation self-play against
itself is not a ladder game and is left out, said here so it is not a silent skip), plus
Artem The Farmer as a thirtieth team, flagged: it was rank 1 until it resubmitted at
2026-09-15 18:42Z and sits at rank 1,162 today with the new submission's rating of 2,277
still climbing, and its earlier submissions are the strongest recorded games there are.
Iminabo can strike it. Sixteen of the 29 are already in the study's crawl (histories to
2026-09-15); thirteen are new: Arda Ceylan, kwa, Driz Lo, Planned Economy, lingxiaojun,
mikelou1, QQ, "Mot hai ba bon 5 sau bay tam 9", Crop Dustas, Hamed Vakili, forever young,
Ishan Karnick, Radiant. Storage: replays are kept zstd-compressed at about 143 KB each
(7,692 on disk take 1.1 GB), so 10 GB is about 70,000 games, roughly the whole gold zone;
608 GB free. Sources in order: the official daily episode datasets (no quota; the index
holds 32,802 episodes over 47 days) and then the rationed replay endpoint (about 300 then
2-4 a minute, so days). Mechanics: `research/paths.py` gains `KAGG_WORKSPACE`, so the gold
crawl writes its snapshot, teams, history and daily index under `data/gold/` while the
replay store and the episode-listing cache stay shared with the study; the crawl runs
alone first, the fetch after it, never together (memory: Kaggle replay quota).

### Checkpoint: gold-zone crawl done
`KAGG_WORKSPACE=data/gold crawl.py`, 02:30Z to 03:23Z: 30 teams, 1,172 submissions listed,
173,017 game rows, 168,025 unique public games (all `EPISODE_TYPE_PUBLIC`), dated
2026-07-31 to 2026-09-17. Per team, submissions found / public games: Majkel1337 12 /
2,028; DSM 79 / 11,676; SpaTaro 23 / 5,550; Sida Zuo 26 / 4,100; Unknown Mother-Goose 29 /
3,900; ymg_aq 37 / 6,262; Excluding 56 / 7,653; Arda Ceylan 65 / 8,910; Orbital
Terraformer 8 / 2,362; THIRD FARM CLUB 64 / 8,512; feel the agi 21 / 4,099; kwa 53 / 7,509;
Driz Lo 33 / 6,754; Ebi 2 / 625; Planned Economy 94 / 10,747; Thomas Tschinkel 91 /
10,505; lingxiaojun 8 / 2,326; mikelou1 39 / 8,322; lumen 31 / 3,497; HowardLeeTW 12 /
2,987; 现实是个乐子 64 / 9,145; QQ 4 / 466; Một hai ba bốn 5 sáu bảy tám 9 29 / 3,145; Crop
Dustas 141 / 17,039; Hamed Vakili 27 / 6,073; local 53 / 8,090; forever young 31 / 5,243;
Ishan Karnick 6 / 802; Radiant 9 / 1,395; Artem The Farmer 25 / 3,295. At 144 KB a replay
the whole zone is about 24 GB compressed; the 10 GB cap is about 69,000 games, taken
newest first (current submissions before old ones). Tables under `data/gold/`
(snapshot_latest.csv, teams.csv, history.parquet) are tracked; the listings cache is
shared with the study's.

### Checkpoint: where the gold games can come from
Of the 168,025 gold games, 3,130 were on disk from the study. Sources for the rest:
- the official daily episode datasets (no replay quota): 34,093 episodes over 49 days after
  today's index refresh, of which 8,528 are missing gold games, spread over 40 archives of
  400-630 MB (median 185 gold games an archive, up to 632 for 2026-09-15). The fetcher's
  file-by-file route ran at about 15 a minute, so `pull_daily_bulk.py` downloads each
  archive whole and stores only the wanted games;
- the community dataset georgymamarin/kaggriculture-episodes (19.3 GB of replay shards,
  updated 2026-09-17 01:01Z): its index of 165,593 episodes holds only 2,911 of the missing
  gold games (674 of the 1,172 gold submissions, 2,738 stored), so the shards are not
  pulled;
- the replay endpoint for the other 156,000: the detached runner (`pull_gold.cmd`, endpoint
  only, cap 10 GB, two workers, newest first) opened at 106-109 a minute in the burst and
  will trickle at 2-4 a minute once the quota bites; days for the cap, weeks for the zone.

### Milestone: the gold pull is running, detached
03:30Z: two detached runners (started with PowerShell `Start-Process`, so they outlive this
session): `scripts/top10/pull_daily_bulk.cmd` importing the wanted games from the 39
remaining daily archives (7,896 games; the first archive gave 632 in 106 s), and
`scripts/top10/pull_gold.cmd` pulling the rest from the replay endpoint, two workers,
newest first, until the store passes 10 GB. Logs: `data/gold/daily_bulk.log`,
`data/gold/pull.log`. Store at launch: 8,498 replays, about 1.2 GB. To resume after a
reboot, start the two `.cmd` files again; both skip what is on disk.

### Milestone: a resume-based evaluator for policy search, exact to the dollar
Iminabo: "set it up" (the plan search). Since a searched action sequence fits only the
farm it was searched from and the family's tapes already are that search, the search is
over the executor's constants, with `scripts/search/resume.py` as the evaluator: snapshots
of the hybrid against v41 at hour 0 of day 24 on seeds 0-19, both seats, decoupled shops
(40 files, 7.9 MB, built in 97 s), each holding both players' state, v41's recorded actions
for the rest of that game as a frozen opponent, and the full game's banks. Three seams had
to be closed for the resumed game to equal the full game: the framework numbers steps by
the length of its history (the prefix is padded to the switch step), agents must be handed
the runner's shared-state merge (player 1's stored view lacks the shared fields), and the
weed generator reads the seed from `env.info`, which a rebuilt environment lacks. With all
three, `resume.py check` reproduces 40 of 40 full games exactly; one evaluation of 40 games
takes 16 s on six workers. Caveat by construction: the frozen opponent cannot react, so
the arena against the live lines stays the gate for anything the search finds.

### Milestone: the parameter search is running, detached
`scripts/search/climb.py` over 47 constants of the executor, plan and market (priorities,
hours, thresholds, day cut-offs, hands per day for days 24-29, seed buffers, reserves),
one or two knobs perturbed per iteration, accepted only if the mean margin on the search
seeds (0-9, 20 resumed games, frozen v41) rises; every accepted step also scored on the
hold-out seeds 10-19. Baseline: search margin -5,606 (the arena gate's -5,606 for the D3
stack, as it should be), hold-out -5,994, day-24-onward basket 28,123. About 19 s an
iteration on six workers. The smoke test accepted one step (feed priority 0.5, wheat
planting 1.0: -5,569, hold-out -5,799). Detached via `scripts/search/climb.cmd` for three
hours; log `results/search.log`, every candidate in `results/search.csv`, the incumbent in
`results/search_best.json` (the run resumes from it). The frozen opponent cannot react, so
the incumbent is confirmed against the live lines with the arena gate before it is
adopted; two more detached jobs (the gold pull) share the machine.

### Milestone: the search's incumbent adopted (22 constants), confirmed against the live lines
The first run ended after 354 candidates (24 accepted) when a worker process died (the
pool flake seen twice today; the runner now uses four workers and resumes from
`results/search_best.json`). Incumbent: search margin -4,388 (from -5,606), hold-out
-5,326 (from -5,994). Against the live lines at switch day 24, decoupled, seeds 0-9: v41
0-20, margin -4,398 (D3 stack -5,606; the frozen-opponent prediction of -4,388 held), v5
8-12, margin -781 (from -1,029), the first wins against a live line at this gate. The 22
constants are written into the source (verified equal to the incumbent by reading the
modules back): feed 0.5, plant 0.5, build -2.5, fertilize 4.0, must-water 1.5, strawberry
harvest 1.5, carrot planting 0.0, wheat and carrot fertilize 3.0 and 4.5, haul threshold
200, urgency 1.75 an hour from hour 13, feed deadline 15, spare watering from 18,
liquidation from 15, sticky -2.5, hands 13, 11, 11, 13, 11, 12 on days 24-29, seed
buffers 3 wheat and 2 carrots, fertilizer reserve 20, no feed-wheat reserve. Full
yardstick on this state: production against pass 166,550 (basket 106,045), competition
against v5 8-12 at -781; gauntlet in recorded towns 31-49 (39%; from 29-51): DSM and
Majkel1337 10-0, Unknown Mother-Goose 6-4, SpaTaro 4-6, Ebi 1-9, Artem, carbonapi and
HowardLeeTW 0-10, Artem's recording 15.9k ahead (from 17.6k). Twenty-two constants moved
together is not the one-at-a-time rule; the live gate on both lines is the check that
stands in for it, and the hold-out seeds say about half the search gain is real.

### Checkpoint: the adopted state under ladder conditions; the search relaunched
Coupled shop draw, seeds 10-29, both seats: against v41 0-40, margin -6,883 (D3 stack
-7,231); against v5 12-28, margin -1,285 (from -2,154; 8 wins became 12). The gains are
smaller than on the decoupled gate the search saw (-4,398 and -781), as the search seeds'
towns are not the coupled ones; the direction holds. The search relaunched at 05:52Z for
three hours with four workers, resuming from the incumbent (`results/search.log`).

### Checkpoint: submission 56291900 after 61 ladder games
02:12Z to 05:42Z: 61 games (the first its validation self-play), 36-25, rating 1,587 after
1,419 at validation and 1,596 after the first hour. The pattern is the local reading:
wins by 20-60k against farms banking 50-70k, losses by 1-6k against farms banking
95-140k (91,955 to 96,213; 102,972 to 105,380 against prvsiyan; 137,766 to 140,650;
120,433 to 122,220; 104,444 to 109,313). The ladder pairs a new submission with
similarly rated opponents, so the early wins buy little rating, and the plateau's 2,900
needs wins against plateau agents, which the local gate says we do not get (0-40 against
v41 under ladder conditions). The submission is the D3 stack; the adopted search
constants are not on the ladder.

### Checkpoint: the rating our ladder games imply (Iminabo asked for verification)
Public episode endpoint, 68 rated games of submission 56291900 to about 06:40Z: 40-28,
running rating 1,600.6. Opponents rated 743 to 1,728 (median 1,579). Against opponents
under 1,500: 16-2; against 1,500-1,800: 24-26. Maximum-likelihood Elo with the opponents
held fixed: 1,608, 95% interval 1,520-1,698. So the running rating has already found the
level of the pool it is matched with. Two readings, both stated: the earlier "silver or
bronze" band (2,432-2,666) is not supported by these games; and the implied 1,608 is a
floor rather than the settled value, because the low-rated pool contains fresh
submissions of strong teams still on their own ramps (we lost to farms banking 124k,
133k and 141k that were rated 1,575-1,650 at the time). What is settled: we are about even
with the farms the ladder matches us with and lose narrowly to anything at plateau
strength; the clean verification is the rating in a day and, in the end, the
post-deadline Bradley-Terry.

### Checkpoint: the first search ended; its later incumbent rejected on hold-out; the anchors
The relaunched run ended 08:47Z at 1,444 candidates in total (38 accepted): final
incumbent -4,143 on the search seeds, -5,430 on hold-out (the adopted state: -4,388 and
-5,326). Live gates, decoupled: on the search seeds 0-9 the final incumbent is -4,128
against v41 and -443 against v5 (adopted: -4,398, -781), in-sample for the search; on the
hold-out seeds 10-19 the adopted state is 2-18 at -5,298 against v41 (two wins against the
live successor) and the final incumbent 0-20 at -5,407. The later incumbent is fitted to
its ten seeds and is not adopted. Anchors: the plain tape (switch day 30) against v41 ties
1-1-18 with margin 0, so the parity floor is exact; v41 beats v5 20-0 by 4,613, so the
successor is the stronger generation and the target. The second search run widens the
search seeds to 0-19 with hold-out 20-29 and starts from the adopted state.

### Milestone: search run 2 launched on twenty search seeds
09:0xZ: snapshots for seeds 20-29 built (60 on disk); `climb.py` now searches on seeds 0-19
(40 resumed games a candidate, about 30 s) with hold-out 20-29, starting from the adopted
state; run 1's files archived as `results/search_run1.*`. Three hours, four workers,
detached. The pull continues: 20,285 replays at 08:47Z.

### Checkpoint: front-running the tape's melon dump is not available (option 3 closed)
One game, our executor from day 9 against v41, seed 1, decoupled: our melon lots land at
hours 9 (6 units, $266, the same turn as the tape's 6), 10, 13 and 16; the tape's at 9,
10, 11, 12, 13 and 15 plus 12 on day 11. Ours 72 at $190, its 72 at $205. Every unit
respawns at the shed each morning (the engine dismisses the hands and resets the farmer
at day end), so the earliest a melon can reach the shed is hour 7 for the farmer and 8
for a hand on the nearest tiles, and the tape already sells at 9: the most a perfect
melon crew could take from it is about $500 a game. The same bound applies to the tape's
other lots, which it hauls as it harvests. The lever that remains against the block is a
stronger second half or a different skeleton, not sale timing. Submission 56291900 at
1,580.7 (flat).

### Checkpoint: the daily-archive import is complete; the endpoint pull is in its trickle
`pull_daily_bulk.cmd` finished at 04:24Z: all 40 archives, the 8,528 gold games they held
imported in about an hour. Store at 09:15Z: 20,297 replays, 2.97 GB (12,600 gold games
added since the pull began at 03:23Z). The endpoint runner is in quota waits between
batches (2-4 a minute); at that pace the 10 GB cap is about two weeks away and the log
is `data/gold/pull.log`. Both runners survive this session; rerunning the `.cmd` files
resumes them.

### Checkpoint: search run 2 has stalled at the adopted constants
By 10:42Z: 477 candidates on the twenty search seeds, 7 accepted, best -4,827 (the adopted
state scores about -4,857 there), hold-out on seeds 20-29 -8,829 (from -8,915 at start),
and no improvement since candidate 214. The 47-constant space is at a local optimum
around the adopted state; the remaining 4-5k to the tape's second half is in what the
executor does (its assignment of units to jobs, its walking), not in how it weighs the
jobs. The run finishes its budget at about 11:52Z for the record and will not change the
package. What would move the second half from here is a different executor (a planned
daily route per unit rather than the greedy pair assignment) or a different skeleton,
both larger than the days that remain before the entry deadline of 2026-09-23 allow
without a decision on scope.

### Milestone: second submission, the plain tape (Iminabo: "submit the plain tape as the second one")
Kaggle submission 56306746, built from commit 5245c0a (`TAPE_DAYS = 30`: v41's tape and
layers for the whole game, nothing of ours after), 148.2 KiB, tests 13 of 13, self-play
verified; message "plain multi-route tape (v41) for the whole game, commit 5245c0a;
parity anchor". Three submissions remain today. The repo is back on `TAPE_DAYS = 24`
(commit 67bbfee) as the development target. Both active submissions now sit on the
ladder: 56291900 (the pre-search hybrid, 1,569.9 at this check) and the parity anchor;
their ramps over the same hours are the comparison.

### Milestone: search run 2's incumbent adopted (19 constants); parity with v5 at switch day 24
Run 2 ended 11:52Z at 779 candidates, 23 accepted, after finding 16 steps in its last
hour: incumbent -4,144 on search seeds 0-19, hold-out 20-29 -7,088 (from -8,915). Live
gates, decoupled: against v41 -3,774 on seeds 0-9 (adopted state -4,398) and -7,110 on the
never-searched seeds 20-29 (adopted -8,718); against v5 on seeds 0-9 10-10 with margin
+34. Adopted into the source (verified equal): plant -0.5, harvest 2.0, dig 4.0, collect
5.5, planting priorities strawberry -0.5, carrot 1.0, wheat 2.5, haul 250 and urgent
1,800, urgency 1.5, feed deadline 18, late harvest 19, sticky -4.0, planting to hour 22,
wheat to day 24, carrots from day 23, 11 hands on day 29, no carrot seed buffer,
fertilizer reserve 16. Full yardstick: production 167,701 (basket 106,564); competition
vs v5 10-10 at +34; ladder-style coupled seeds 10-29: v41 0-40 at -5,311 (from -6,883), v5
14-26 at -556 (from -1,285); gauntlet 30-50 (38%), Unknown Mother-Goose 5-5, DSM and
Majkel1337 10-0, Artem 0-10 at 91.9k against its 107k. Neither active submission carries
these constants: 56291900 is the pre-search hybrid, 56306746 the plain tape (validated at
the fresh-start 600).

### Decision (Iminabo): both tracks, and how they share the machine
Track A, the executor: replace the greedy per-turn pair assignment for days 24-29 with a
planned daily route per unit. At hour 0 each unit gets a block of tiles (nearest-neighbour
tour from the shed over the day's jobs, hands split by quadrant), feeders keep the herd,
one or two runners haul; the day-24 resume evaluator (`scripts/search/resume.py`, exact,
40 games in 16 s) is the development loop and the live arena against v41 and v5 the gate.
Target: the 4-5k the tape's second half still holds (the tape idles 5-24 unit-turns a day
and walks 20% less). Then move the switch day earlier once our post-switch play beats the
tape's. Track B, the learning run: featurise the replay store incrementally (per step, per
seat: tiles as a 10x10 grid of crop/age/water/animal channels, shed, seeds, money, market
prices and inventory, town shops, hour and day; actions per unit as op plus argument,
market orders as a small set) into arrays as the pull proceeds, then behaviour cloning of
a per-unit policy on the gold games; RL only after a vectorised simulator exists. Cores:
the pull two, featurising two to three in the background, the arena the rest; the crawl
and the fetch never together. Both tracks keep their numbers in this journal; nothing is
adopted without the live gate.

### Checkpoint: third build session opened; baseline reproduced, both pullers checked, four new notebooks pulled
Read in the handoff's order (CLAUDE.md, METHOD.md, analysis.md 1-4, 7, 9b, 11, the memo's
answer, plan and amendments 6-7, the journal from "build phase opened" and all of today,
P17-P22, then `agent/`, `scripts/eval.sh`, `scripts/search/resume.py` and `climb.py`,
`scripts/arena.py`, the pullers, `research/trace.py` and the engine source). Checks, 14:42Z:
- `scripts/eval.sh` reproduced to the dollar: production 167,701 (basket 106,564) on seeds
  1-8; competition against v5 10-10, margin +34 on seeds 0-9. Engine 1.32.7; seven routers
  under `data/notebooks/`; 13 tests pass.
- Gold pull: 20,991 replays, 3.0 GB in `data/replays`. The daily-archive runner finished
  at 04:24Z (all 40 archives); the endpoint runner (one process pair) is in its trickle,
  250 of a 500 batch at 2.0 a minute with 120 s quota waits.
- Submissions: 56291900 (hybrid) 1,569.9; 56306746 (plain tape, validated 14:18Z) 921.1,
  on its ramp.
- Notebook list (`kernels list --sort-by dateRun`), new since 2026-09-16's check: aurax7 v7
  (09-17 04:33Z, 15 votes), ahmedberatozer V46 "First-Turn Microstructure" (58), nathanjacob
  "Pipe-7 Wheat Microstructure" (61) and "Pipe-8 Clean Opening" (2), jaxa623 "[2802] Two
  Identical Agents, 90 Points Apart" (67), degnonguidi "cloning agent" (59), and tetsutani
  re-run at 13:42Z (98). Pulled V46, Pipe-7, 2802 and v7 (gitignored). Lineage by size and
  markers: Pipe-7's `main.py` is V41's with one constant changed (`_OPEN_UNITS` 5 against
  70, the turn-0 wheat round trip); V46 is V41 plus EXP293 layers (3,627 lines); v7 is
  3,937 lines with V43-V45 markers; 2802 is a 315-line, 350 KB packed build with V43/V45
  markers. All four are the family. Their strength against v41 is being measured (arena,
  decoupled, seeds 0-9, both seats) before either track starts.

**Decision (order of work).** Track B's featuriser is written first and left running in the
background on two workers, since it is mechanical and the pull grows under it; track A's
route planner is developed against `resume.py` while it runs; the successor check decides
which tape the hybrid bundles.

### Surprise: the plateau's successor is already stronger than the tape we bundle
Arena, decoupled shops, seeds 0-9 both seats, each new build against `line:v41`:

| build | W-L | mean bank vs v41's | margin | basket |
|---|---|---|---|---|
| aurax7 v7 | 20-0 | 98,668 vs 96,791 | +1,877 | 108,165 |
| jaxa623 2802 | 20-0 | 98,668 vs 96,791 | +1,877 | 108,165 |
| ahmedberatozer V46 | 19-1 | 98,694 vs 98,175 | +519 | 108,030 |

v7 and 2802 produce identical harvests and identical banks on all twenty games: 2802 is a
315-line wrapper that embeds V43 verbatim (`_PARENT_SRC`, 335 KB) with a single-order
turn-0 wheat round trip, a 24-turn sale-reservation horizon, market front-loading and a
two-turn sale advance; v7 describes itself as "V45 Full Chassis + V44 Same-Turn Race
Escalator + _r60 Survival Guard + 2842 Advance/Frontload Overlay", so it has absorbed the
same overlay. Every one of the four carries Apache-2.0 notices and retains its upstream
attributions. The plain tape we submitted (56306746, v41) therefore sits a generation
behind the newest public build by about 1.9k a game in mirror seats, and the hybrid's
target moves to v7. Whether v7 is on the ladder yet is being checked by replaying it in
the recorded seat of the 60 most recent gold games (a first-divergence count, as v5 was
checked on 2026-09-16); the hybrid with v7's code as its tape is measured after that
(`KAGG_TAPE` now points `agent/hybrid.py` at any build for an arena run).

### Milestone: the featuriser is written and running detached (track B)
`research/encode.py` turns a replay into arrays with a step axis: both farms as
`[2, 720, 10, 10, 12]` uint8 tile grids (kind, crop or animal id, age, yield, tended,
missed days, fertilizer days left, decaying, cared, dung, care bonus, days of life left),
each seat's unit positions and inventories (up to 20 units), shed, seeds, money, hires
and quadrant mask, the shared prices, inventory, shops, day and hour, and each seat's
actions: per unit an op id (18 ops), argument (crop or item) and count, and up to ten
market orders as type, item and quantity. The action at index t is the one submitted on
observation t. Checked on the probe replay 108982600: 14,181 unit ops decode back to the
recorded ops with 0 mismatches, tile-kind counts equal `tile_summary` at steps 0, 100,
400 and 719, final money equals the reward; 0.45 s a game, 100 KB compressed
(`tests/test_encode.py`, 3 tests). `scripts/learn/featurise.py` encodes every gold game
on disk newest first into `data/features/<episode>.npz` (gitignored) with a manifest,
two workers, rescanning every ten minutes; started detached through
`scripts/learn/featurise.cmd` (log `data/features/featurise.log`). At this pace the
16,422 gold games on disk take about an hour and 1.6 GB.

### Checkpoint: v7 is on the ladder, and it is the target
v7 replayed in the recorded seat of the 60 most recent gold games on disk (both seats, the
opponent's recorded stream as a tape; scratch `fidelity_v7.py`): of 120 seat replays, 3
errored, 67 part from the recording by turn 2 (a different agent's turn-0 market), 34
match it through the day-6 router (turn 144 or later) and 14 through turn 400 or later.
The longest matches are LK30's two seats (turns 712 and 698, both seat 0; banks 132,364
against 133,065 recorded and 133,575 against 133,628), then Ishan Karnick 646, tokitamago
603, Auto Fermers 584 and 584, lemon13418 533, kanno 516: v7's generation is already
played on the ladder, by opponents of the gold teams more than by the gold teams
themselves (of the gold teams, Hamed Vakili's four seats match through turn 383, the rest
part by turn 2). No seat matched to the end, so v7 is a proxy for the generation, not a
byte-for-byte copy of any one submission; its live strength is what the arena measured
(+1,877 over v41 in mirror seats). **Decision:** v7 is the hybrid's target and the
candidate tape for both slots: the hybrid on v7's code (`KAGG_TAPE`) is being measured
against v7 and v41 at switch day 24, and the plain v7 tape replaces the plain v41 tape as
the parity floor once that run is in. The V41 pull and `line:v41` stay as the previous
generation's yardstick.

### Checkpoint: the hybrid on v7's opening loses more than on v41's
Switch day 24, decoupled, seeds 0-9 both seats, `KAGG_TAPE` = v7's `main.py`: against v7
0-20, mean bank 92,713 against 97,608, margin -4,895 (basket 104,942); against v41 0-20,
92,930 against 98,473, margin -5,542. On v41's opening the same executor is -3,774 against
v41. So our post-switch play is 4.9k behind v7's own, and swapping the opening alone gains
nothing: v7's edge over v41 (+1,877 in mirror seats) is in layers that play the whole
game, which the hybrid discards from day 24. The plain v7 tape is still the better
parity anchor; the hybrid's second half has to close 4.9k against v7 before it beats it.

### Checkpoint: the day planner, first two cuts (track A)
`agent/dayplan.py`: from `PLAN_FROM_DAY` (24) to day 28, the hour-0 observation becomes
one stop per tile with the ops worth doing there today in execution order (a ready wheat:
water, harvest, replant, water; a strawberry: fertilize on a production age, water,
harvest; a pen: feed, care, collect, harvest; a weed or exhausted plant: dig, plant,
water), the pens are chained nearest-neighbour and cut into segments of six for the herd
units, the field stops are cut into segments for the rest, each unit picks up the wheat or
fertilizer its segment needs at its spawn tile, and `follow` executes the segment,
dropping any op whose precondition no longer holds; a unit whose segment is spent joins
the greedy pool. Jobs on tiles still on a segment are off the greedy table, and the
market buys the seeds the plan will plant (`plant_wanted`). Measured on the day-24
snapshots (frozen v41, `scripts/search/resume.py`), the greedy executor's marks being
-4,144 on seeds 0-19 and -7,088 on 20-29:
- cut 1 (nearest-neighbour chain from the shed, split into k contiguous pieces of equal
  chain cost): -7,696 and -10,694, basket 26,998 against 28,266. The diagnostic on seed 1
  (scratch `plan_diag.py`) showed why: the chain's tail is scattered, so one unit got a
  49-turn segment for a 23-hour day and seven of its tiles were never reached, five of
  them strawberries the tape had left unwatered on day 23, which weeded overnight (7
  weeds at the next hour 0 against the tape's 0).
- cut 2 (column-serpentine order, a min-max partition by binary search on the segment
  cap, each segment walked in from its nearer end, spare waterings dropped first when the
  cap exceeds the day): segments of 16-21 turns, no weeds, -6,469 and -9,406; the basket
  rises to 28,917 and 29,961 (wheat 216 against 159 a game after day 24, strawberries 53
  against 50) but milk, wool, eggs and carrots fall (59/36/29/81 against 66/41/34/93)
  and, decisive, the frozen opponent's bank rises by 2.0k and 1.4k. A frozen tape's
  orders cannot change, so its extra revenue is price: the planned units carry the
  harvest to the day-end drop and it sells at hour 0 beside the tape's own morning lots,
  where the greedy executor hauls a strawberry load home within the hour (D3) and sells
  ahead of them. The tape itself drops animal products when a herd unit passes a shed
  tile (`PLACE` at (4,4) and (5,4) in its tours).
Cut 3 adds both: a planned unit on a shed tile drops what it carries, and one carrying
more than `HAUL_VALUE` walks it home before continuing; four thresholds are running.

### Checkpoint: cut 3 (hauling) and where the planner still loses
Day-24 evaluator, search seeds 0-19 / hold-out 20-29 (greedy -4,144 / -7,088):

| HAUL_VALUE | margin | basket | opponent's bank |
|---|---|---|---|
| 250 | -8,609 / -12,127 | 23,108 | 105,174 |
| 600 | -5,772 / -8,890 | 26,847 | 104,933 |
| 1,200 | -5,611 / -8,438 | 28,103 | 105,145 |
| drop at a shed tile only | -5,711 / -8,672 | 28,496 | 105,164 |

Hauling at 250 wastes a fifth of the harvest in walking; 1,200 is the best and is the
default. But the frozen opponent banks about 105.1k under every threshold against 103.5k
against the greedy executor, so the price effect is not sale timing. It is the herd: the
planned suffix harvests 53-59 milk, 30-36 wool and 25-32 eggs a game against greedy's 66,
41 and 34, and fewer units of ours in the market leave the tape's daily milk and wool
lots a higher price (milk falls 1.6 times base per 122 units, wool by the square). The
census on seed 1 (scratch `census_diag.py`) names the cause: on day 24 the plan wrote 6
FEED ops and 4 were done, because the herd units' wheat pickups were sized to the shed at
hour 0, which holds only yesterday's leftover; the market buys the day's feed at hour 0
and it lands at hour 1, so most FEEDs met an empty inventory and were dropped, and the
unfed sheep produced 11 wool the next morning where the tape's fed ones gave 14. The
tape, for comparison, cares for all 17 animals every day (17/17/17/17/15 CARE ops on
days 24-28), feeds 5-15, and lets 13-32 plants go unwatered on days it has better work.
Two more losses seen there: the planner digs exhausted strawberries on day 28 when
nothing can follow (10 wasted DIGs, 33 idle unit-turns), and on the last planned day it
banks 2.1k less than greedy in one day. Cut 4: pickups sized to the whole feed need with
the residual retried at the shed until hour 2, no dig without a planting, and A/Bs of
the last planned day (27) and the fertilizer reserve cap (40).

### Checkpoint: cut 4, and the herd was not the cause after all
Cut 4 (pickups sized to the feed need, retried at the shed until hour 2; no dig without a
planting): -5,835 / -7,602 (cut 3: -5,611 / -8,438; greedy -4,144 / -7,088). Last planned
day 27: -5,883 / -7,979, worse. Fertilizer reserve cap 40: identical to the cap of 16, so
the reserve never binds. The census on seeds 1 and 2 with cut 4 (days 24-29) now shows the
herd even: seed 1 milk 44 against greedy's 44 and wool 60 against 60, seed 2 milk 36
against 36 and wool 63 against 66; the plan harvests more wheat (192 against 153, 223
against 191) and as many or more strawberries (54 against 53, 70 against 61) and still
banks 1.4k and 0.5k less. Two causes read off the census. First, carrots: 94 against 111
and 89 against 106 units, because on day 27 greedy digs the strawberries it has just
harvested for the last time and plants carrots on them the same day (13 DIG, 19 PLANT),
while the hour-0 plan saw a strawberry with yield and wrote only the harvest, so the
tile waited for a fallback unit; cut 5 writes dig, plant and water after a last harvest.
Second, timing: the planned harvest reaches the shed at the day-end drop and sells at
hour 0 beside the tape's own lots (day-end money runs 0.4-2.3k behind greedy's and
catches up the next morning), where greedy's hauled loads sell the same afternoon; the
evaluator preferred less hauling (1,200) to more, so the answer is not more trips but
ending each segment at the shed, which the greedy fallback already does from hour 21.

### Checkpoint: cut 5 out-banks greedy on our side; the rest is the opponent's price
Cut 5 (a strawberry's last harvest is followed by dig, plant and water in the same stop),
haul 1,200: search seeds -5,013 (our bank 99,977 against greedy's 99,402, the tape's
104,991 against 103,547), hold-out -7,684 (93,753 against 93,364; 101,437 against
100,452); carrots back to 96 and 90 a game. Haul 900: -5,333 / -8,000, worse. So the
planned suffix now banks 400-600 more than the greedy one and harvests a bigger basket
(29,166 against 28,266), and the whole remaining deficit, 0.9-1.4k, is the frozen tape
banking more against it: milk, wool and eggs are 6 units a game lower each on the search
seeds, and what the tape sells of them fetches more. Per-seed differences are being
tabulated to find the seeds where the herd falls short.

### Checkpoint: per-seed table, herd load, and two more causes
Per seed (search seeds 0-19, both seats, cut 5 against greedy): our bank is higher on 32
of 40 games and the tape's is higher on 40 of 40 (by 280 to 3,110); milk, wool and eggs
total -246, -216 and -224 units over the 40 games, wheat +2,183, carrots +105. Seed 18
(a four-quadrant farm with 23 pens) is the outlier at -6.9k a seat: its day-24 plan costs
363 unit-turns for 14 units, 25.9 each against a 23-hour day, and the overflow weeded
five strawberries and a wheat that day and seven more tiles on day 26. Seed 15 shows the
herd cause: a herd unit carrying $1,200 of milk at a 3-Smoothie-Shop price broke off its
round to haul it and two pens were never fed. HERD_LOAD 5: -5,338 / -8,966; 4: -4,607 /
-8,563 (search seeds within 460 of greedy, hold-out worse); the evaluator's own noise is
a few hundred, so the load stays at 6 for now. Cut 6: a herd unit does not haul while it
still has pens to feed; when the day is too short the plan drops, in order, spare
waterings, new wheat plantings, wheat and carrot fertilizing and carrot plantings before
it leaves tiles unreached (`fit_to_day`); and at hour 0 the plan sizes the day's hires to
the work (`hands`, up to 14, read by `agent/market.py`) instead of the fixed list.

### Surprise: v7's whole edge over v41 is one melon
Executed revenue by product from the market replica on four v7-vs-v41 games (seeds 0-3,
decoupled, money checks 0 mismatches): melon +1,279 (72 units against 66: v7 ends day 0
with a twelfth melon seed where v41's 70-wheat turn-0 round trip leaves it one short),
milk +170, wheat net +108 (v7 sells 60 fewer wheat and spends 1,922 less buying it),
everything else within 60. The "same-turn race", "sale advance" and "front-loading"
overlays contribute nothing measurable in mirror seats against v41. So the newest public
generation is v41 with its opening defect repaired, and both tapes hold the same shed and
farm at the switch (checked at steps 575-577 on seeds 0-2). The hybrid-on-v7 numbers of
the earlier checkpoint are being re-measured: that arena run was launched in the same
response as the first planner hook went into `agent/executor.py`, so its workers may have
imported the untested planner (P23).

### Checkpoint: the hybrid-on-v7 numbers stand; the opening's opponent effect
Re-run with the planner switched off (`KAGG_PLAN_FROM_DAY=99`): the hybrid on v7's
opening is again 0-20 at -4,895 against v7 (basket 104,942, to the dollar the same as
before), and the hybrid on v41's opening at the same commit is 0-20 at -3,774 against
v41 (the journal's number of this morning, reproduced). So both runs were clean and the
gap is real: with identical farms and sheds at the switch, our executor is 1.8k worse
against v41 after v7's opening than after v41's. The difference is on the opponent's
side. Against v7's turn-0 order v41 ends day 0 a melon seed short (66 melons against 72)
and its runtime layers, which watch the rival's market drops (the RACE layer, journal
2026-09-16), see a different first 23 days; a v41 that reacts differently to our tape
then meets our executor differently. Practical reading: the choice of opening tape is
not free of the opponent, and the hybrid is 3.8-4.9k behind the tapes' own second half
whichever opening it takes; the plain v7 tape remains the parity floor.

### Checkpoint: first behaviour-cloning run on the GPU (track B)
Learning environment: a separate venv (`.venv-learn`, gitignored) with torch 2.11.0+cu128
on the RTX 5070 (CUDA available), so the project venv and the detached `uv run` runners
are untouched. `scripts/learn/train_bc.py --games 400 --holdout 40 --epochs 1 --stride 2
--seat gold`: 360 gold games, the gold team's seat only, every second step, 1.5 million
unit-steps in 80 s. Hold-out op accuracy 0.648 over 101,824 unit-steps of 40 unseen
games: PLANT 0.95, WATER 0.95, CARE 0.85, FEED 0.84, COLLECT 0.76, HARVEST 0.72, PASS
0.69, the four moves 0.46-0.52, FERTILIZE 0.30. The moves are the hard part, as expected
without the unit's destination in the input; the tile ops are already close to their
ceiling from the grid alone. Encoded games so far: 7,500 of the 16,422 on disk
(208 a minute). The pipeline is what this session set out to build; the model itself is
a first cut and nothing plays it.

### Checkpoint: cuts 6 and 7 of the planner
Cut 6 (feed-first hauling, the four capacity cuts, hires sized to the work): -5,287 /
-8,968, worse than cut 5: dropping carrot plantings to fit the day cost 40 carrots a
game. Cut 7 keeps the feed-first rule and the hire sizing, limits the capacity cut to
spare waterings again, and orders each segment by the worth of its stops (harvests and
must-waterings first, spare waterings last) so an unfinished segment leaves its
cheapest stops: -5,023 / -8,250 (strawberries 57 a game against 48 without the
ordering, which alone scores -5,606 / -8,329); the hire sizing never fires (MAX_HANDS
13 gives the same numbers). Against greedy's -4,144 / -7,088 the planner is level or
better on our own bank (100,004 against 99,402 on the search seeds) and the whole gap is
the tape's bank, 105,028 against 103,547: the same 1.5k as in cut 2. Milk, wool and eggs
are now 59/39/31 against 66/41/34, too close to carry 1.5k, so the remaining suspect is
when our produce sells: greedy hauls loads during the day and its units are in the
market before the tape's hour-0 lots; the planner's harvest reaches the shed at the
day-end drop and sells beside them. A revenue-by-hour census on three seeds settles it,
and cut 8 ends every field segment with a walk home and a drop (`RETURN_TO_SHED`).
(The census was launched in the same response as the cut-8 edit, against P23's rule; it
is read as indicative only and the evaluator's A/B of `RETURN_TO_SHED` is the measure.)

### Milestone: v7 bundled as a second opening build, byte-exact
`agent/line_v7.py` is aurax7's v7 `main.py` verbatim (347,606 bytes, md5 8bd6aeab, the
same as the pull), under its Apache-2.0 notices (NOTICE.md); `plan.TAPE_FILE` selects
line_v41.py (default) or line_v7.py, and `KAGG_TAPE` still overrides for arena runs. The
bundled file against the notebook's own file in mirror seats, seeds 0-4 both seats:
1-1-8, margin 0, identical banks on seeds 1-4 and the seat-0 turn-0 asymmetry on seed 0
(70,865 against 70,576 either way), the same pattern as the plain v41 tape's 1-1-18. So
a plain v7 tape package (`TAPE_DAYS = 30`, `TAPE_FILE = "line_v7.py"`) is ready to build
as the parity anchor at the newest public generation; it is not submitted (Iminabo's
call), and the tree's default stays the v41-opening hybrid.

### Checkpoint: the plain tape's ramp, and when the produce sells
Ladder at 15:35Z: the plain v41 tape (56306746, validated 14:18Z at 921) is at 1,935.7;
the hybrid (56291900) at 1,575.1 after a day. The parity anchor is climbing past the
hybrid within its first two hours, as the local reading said it would.
The revenue-by-hour census (days 24-29, seeds 1, 2, 4, hybrid against v41; indicative,
see P23's caveat above): greedy sells 13.8k of its 21.5k at hours 0-1 and 7.7k during
the day; the planner 14.6k of 20.4k at hours 0-1 and 5.8k during the day; v41 sells 6.7k
at hours 0-1 and 17.9k during the day, 8.3k of it at hours 20-23. Milk is the clearest
difference: greedy sells 1,573 of it at hours 2-11 and the planner 610, whose herd units
finish their rounds at hour 21-22 and drop at day end. So the tape gets its produce into
the market during the day and both of our executors dump at dawn, the planner more so;
HERD_LOAD 4's gain on the search seeds (shorter rounds, units home by mid-afternoon) is
the same mechanism, and cut 8's return-to-shed stop should apply to the herd as well.

### Checkpoint: cuts 8 and 9; the planner is not adopted
Day-24 evaluator (search 0-19 / hold-out 20-29; greedy -4,144 / -7,088):

| cut | change | margin |
|---|---|---|
| 7 | value-ordered segments, feed-first haul | -5,023 / -8,250 |
| 8 | field segments end with a walk home and a drop | -5,180 / -8,489 |
| 9 | wheat fertilized at ages 2-3 as well (the tape's 40 spreadings) | -4,959 / -8,776 |
| 9 + herd load 4 | | -5,330 / -9,133 (wheat 119 a game: the field loses two units) |
| 9 + herd load 4 + every segment ends at the shed | | -5,542 / -9,975 |

The frozen tape's bank is 105.0-105.1k under every planner variant against 103.5k under
greedy, whatever we do with hauling, herd size or fertilizer; the return-to-shed drop did
not move it by $10. Our own bank is level with greedy's or a few hundred better, the
basket is bigger, and the net margin is 0.8-1.7k worse. After nine cuts the planner
matches the greedy executor's production and hands the frozen opponent about 1.5k of
price, and the evaluator's noise (a few hundred between seed sets) is now larger than
the differences between cuts. **Decision:** the planner is not adopted. It stays in the
tree switched off (`PLAN_FROM_DAY = 99`; `KAGG_PLAN_FROM_DAY=24` turns it on) with the
live gate run once for the record, so the next session can pick it up or drop it. What
it established: the tape's 20% fewer moves and idle turns are not where its second-half
margin comes from; a planned executor that out-harvests greedy still banks the same,
because the last 4-5k against the tape sits in the market interaction, which the frozen
evaluator cannot show and the live arena has to.

### Checkpoint: the planner's live gate, and the shipped state reproduced
Live arena, `KAGG_PLAN_FROM_DAY=24` (cut 9), hybrid switch day 24 against v41, seeds 0-9
both seats, decoupled: 0-20, our bank 93,894 against v41's 98,575, margin -4,681, basket
105,209; the greedy executor at the same commit is 0-20 at -3,774 (93,614 against 97,388,
basket 104,910). The live line says what the frozen one said: the planner adds 280 to
our bank and 1,187 to the opponent's. With the planner off `scripts/eval.sh` reproduces
the morning's numbers to the dollar (production 167,701, basket 106,564; against v5 10-10
at +34), so the tree's shipped behaviour is the adopted search state; 16 tests pass.

### Checkpoint: end of the third build session
State at commit 7f47d9b (tree clean, pushed): the packaged agent is unchanged from this
morning's adopted search state (hybrid, v41 opening, switch day 24; `scripts/package.py`
builds 293 KiB, 11 files, self-play verified). New in the tree: `agent/line_v7.py` (the
successor build, byte-exact, selectable by `plan.TAPE_FILE`), `agent/dayplan.py` (the
planned-route executor, off), `research/encode.py` and `scripts/learn/` (the featuriser
and the behaviour-cloning pipeline), `KAGG_TAPE` and `KAGG_PLAN_FROM_DAY` overrides, 16
tests. Running detached: the gold pull (21,086 replays, 3.0 GB, endpoint at 2 a minute)
and the featuriser (9,500 of 16,422 gold games encoded, 203 a minute, 886 MB).
Ladder at 15:35Z: plain v41 tape 1,935.7 and climbing, hybrid 1,575.1.

Numbers of the day, all decoupled seeds 0-9 both seats unless said:
- v7 and 2802 beat v41 20-0 by +1,877, V46 19-1 by +519; the edge is v41's lost melon
  at turn 0 (+1,279 of it), not the market overlays.
- Hybrid (switch 24) against v41: -3,774 on v41's opening, -5,542 on v7's; against v7:
  -4,895 on v7's opening. The bundled v7 ties the notebook's v7 at margin 0.
- Day planner, nine cuts: best -4,959 / -8,250 on the day-24 evaluator against greedy's
  -4,144 / -7,088; live against v41 -4,681 against greedy's -3,774. Not adopted.
- Behaviour cloning: 0.648 hold-out op accuracy from 360 games in 80 s on the GPU; a
  2,900-game run was killed by the harness's low-memory watchdog (4.2 GB free of 31.3,
  most of it held by the browser, not by our processes); a 1,440-game run is retrying.

What is missing or unverified, said plainly: the rules page is still unread since
2026-09-14; no game against a live adaptive opponent other than v5, v41 and v7; the
opening's opponent effect (1.8k) is a reading, not a traced mechanism; the revenue-by-hour
census was launched against P23's rule and is indicative only; the planner's remaining
1.5k is attributed to the frozen tape's prices without a per-product decomposition of
its revenue; the BC model has never been played and its accuracy is on the gold seat's
own games, not on unseen teams.

### Decision (Iminabo): clone the most straightforward top-10 team, split the learning data by team
Plan approved 16:10Z (plan file `temporal-snuggling-star`). Iminabo's framing: copy the
strategy of one top-10 team's most successful submission, chosen by how straightforward
it is, and only after a level-k analysis (K1 what the field does, K2 how the team beats
it, K3 what beats the team); for the learning track, train on six of the top ten over all
their games up to the crawl cutoff (2026-09-17T03:23Z) and test only, never tune, on
ranks 2, 5, 10 plus one random gold team from ranks 11-29. The data read that picked the
target (current submissions, encoded games; distinct field lines at turns 24/100/200/300
with the modal share): Majkel1337 73 (24%) / 221 / 228 / 228 of 228; DSM 4 (50%) / 40 /
97 / 108 of 108; SpaTaro 106 of 106 at turn 24 (noise); Unknown Mother-Goose 3 (79%) /
21 (77%) / 49 / 112 of 116; THIRD FARM CLUB 1 (100%) / 4 (90%) / 61 / 135 of 135. No
top-10 team is a replayable tape past day 8; THIRD FARM CLUB (rank 10, median bank 111k,
the highest of the ten) plays one field line through turn 136 in 98% of its games and
branches per game afterwards, not by the shop draw (within-shop-pair agreement 0.55 at
turn 200, 0.28 at 300). It is the target, conditional on the level-k report (gate G0).
The random test team drawn with `default_rng(20260917)` from ranks 11-29 is HowardLeeTW;
`data/gold/teams_first.txt` lists the six training teams, the three named test teams
and it.

### Milestone: third submission, the plain v7 tape (Iminabo: submit it now)
16:21Z, Kaggle submission 56309360, built from the tree at commit 1fc4642 with
`TAPE_DAYS = 30` and `TAPE_FILE = "line_v7.py"` (293.4 KiB, 11 files, self-play verified),
message "plain v7 tape (aurax7 v7 verbatim) for the whole game ... parity anchor at the
newest public build". Validated COMPLETE at 600.0 (the fresh-start rating). Two
submissions remain today. The active slots are now the plain v41 tape (56306746, at
2,169 and climbing) and the plain v7 tape; the hybrid (56291900, 1,568) drops out. The
tree is back on `TAPE_DAYS = 24`, `TAPE_FILE = "line_v41.py"`. My estimate for v7 settled,
stated to Iminabo: 2,950-3,050, near the gold cut (2,929) and short of rank 10 (3,005),
because gold teams beat v7-like ladder agents 55-78% of the time (8 such teams, 55-152
games each as opponents of the gold teams).

### Milestone: the puller re-ordered to finish the top 10's current submissions
`pull_gold.py --teams-first <file>` puts the named teams' missing current-submission games
at the front of the queue (`missing_ids(teams_first)`), then newest-first as before;
`pull_gold.cmd` passes `data/gold/teams_first.txt`. The old runner and its orphaned
`fetch.py` batch were stopped (the first attempt killed the shell that issued it; the
second found the fetch child holding the log) and one runner restarted at 16:23Z: store
3.20 GB, 151,408 episodes missing, the first 700 of the queue all games of the ten teams'
current submissions (Majkel1337's first). Pull status at the cutoff (16,588 of 168,025
gold games on disk, 10%): current submissions complete for DSM, Excluding, Arda Ceylan,
THIRD FARM CLUB, kwa, Driz Lo, QQ, Planned Economy, forever young, Ishan Karnick; partial
for Majkel1337 71%, Unknown Mother-Goose 64%, Sida Zuo 59%, ymg_aq 58%, SpaTaro 54%,
Orbital Terraformer 50%; older submissions 3-30% everywhere.

### Milestone: gate G0 passed; THIRD FARM CLUB confirmed as the clone target
`scripts/top10/klevel.py` (one row per game from the encoded arrays and the market replica,
`data/top10/klevel_third-farm-club.parquet`) and the report `reports/top10/tfc_klevel.md`.
K1: of its 135 current-submission games, 63 were against the public line (v41 and v7
share the field line through turn 136), 27 against top-10 teams, 45 against others; it
wins 92% against the line by a median 12,718 and 33% against the peers (median -2,406).
The margin over the line is 12.4-13.6k with or without each shop group, so the edge is
not the draw. K2: equal gross revenue (142.8k against 141.6k) but 10.7k less spent (no
fertilizer bought, 176 FERTILIZE ops from its own 259 units against the line's 114 and
347 sold); eggs 8.2k, tomatoes 6.8k and carrots 9.1k against the line's 3.8k, 1.0k and
5.0k; fewer strawberry units at a higher price (177 at $159 against 246 at $110); milk
42% and eggs 72% sold at hours 0-1 where the line sells its strawberries 79% in the
afternoon; the last three days 31.0k against 21.7k; hands 4, 4, 6, 6, 6, 6, 11, 9, 9, 12,
13, then 9-11. K3: 18 of its 26 losses are to top-10 teams, which keep its morning timing
(their early share 11-42% against the line's 8-15%) and out-produce it in bulk: wheat
504 units against its 298 and 175 tiles planted against 130, strawberries 193 against
160; the two largest losses are wool on Yarn Store towns (Arda Ceylan +34.8k, Orbital
Terraformer +16.9k). Front-running by the opponent is rejected as a cause (its own
early share is higher in the losses). Decision: clone its K2 play; the K3 candidates,
each a single measured change later, are more wheat on its empty and weeded tiles and
a heavier sheep response on Yarn towns.

### Milestone: THIRD FARM CLUB's opening extracted as a tape
`scripts/learn/extract_opening.py` walks the recorded games step by step, keeping the most
common full action (every unit op and market order) among the games still on the line:
135 of 135 through turn 24, 128 through 48, 104 through 100, 136 and 144 (77%), 25
through 200. Written to `agent/opening_tfc.py` (200 steps, 25 KiB). `agent/opening.py`
replays it with the family's repairs (plantings trimmed to the seeds in hand, a weed under
a planned PLANT or BUILD dug first, the hands list cut to the hands that exist);
`agent/hybrid.py` plays `plan.OPENING` for `plan.OPENING_STEPS` before the tape or the
executor, with `KAGG_OPENING`, `KAGG_OPENING_STEPS` and `KAGG_TAPE_DAYS` overrides for
arena runs (`OPENING = None` in the shipped tree). Next: the fidelity check in its
recorded seats and the floor measurement (opening tape + our executor) against v41 and v7.

### Checkpoint: the opening tape is faithful in effect; our executor after it is the same 85k
Fidelity (scratch `fidelity_tape.py`; the tape for 144 steps then our executor with
`KAGG_TAPE_DAYS=0`, in THIRD FARM CLUB's recorded seat of its 20 latest games, the
opponent's stream as a tape, the town as recorded): the tile census equals the recording
at hour 0 of every day through day 6 in 20 of 20 games and first differs on day 7, after
the tape ends; the action-stream comparison reports a difference from turn 0 only
because the recording lists `PASS` for hands it is hiring that turn while the extractor
keeps the hands that exist (the engine ignores both). Banks: ours 0.78 of the recorded
median, 2 wins of 20 against opponents the team beat 16 times. Floor arena (opening tape
144 steps + our executor with the v41 skeleton, decoupled, seeds 0-9 both seats): 0-20
at -21,704 against v41 (85,220 against 106,925; basket 97,943) and 0-20 at -23,084
against v7. Our executor banks about 85k from THIRD FARM CLUB's day-6 farm as it does
from v41's (85.4-85.8k on the hybrid curve), so the opening is not where the clone's
value is: the learned second half is. Job labels for THIRD FARM CLUB's 135 games
(`research/jobs.py`: a unit's next non-move op within the day and the tile it happens
on; `tests/test_jobs.py`): 962,299 unit-steps on its own seat; NONE 8.7%, WATER 32.0%,
COLLECT_FERTILIZER 14.4%, HARVEST 9.2%, FERTILIZE 6.5%, PICKUP 5.9%, FEED 5.7%, PLANT
5.6%, CARE 4.8%, DROP 3.7%, PLACE 1.7%, DIG 1.1%, BUILD_PASTURE 0.6%, BUILD_COOP 0.2%.
`agent/clone_feats.py` holds the numpy feature code the trainer and the runtime share.

### Note: the job-level trainer, its first run, and the runtime pieces
`scripts/learn/train_jobs.py`: a four-layer convolutional trunk over the 13 planes once per
step, a per-unit state from the trunk at the unit's tile, the pooled trunk, the unit
vector and the step scalars, a destination head over the 100 tiles (a query against the
trunk plus learned distance and relative-offset bias tables, locked tiles masked), and op,
argument and count heads read at the destination (teacher-forced in training). Batches
are 48 steps with all their units; games stream in chunks of 16; the test set is the last
25 games of the submission by create_time. The first run trained nothing: label smoothing
on the destination loss put mass on the masked tiles (logit -1e9) and the loss read in
the millions; the destination loss is now plain cross-entropy with a -1e4 mask (matched
in `agent/clone_net.py`, the numpy forward pass for the bundle, exported and checked
against torch by `scripts/learn/export_clone.py`). The loader runs 2,500 steps a second
on the GPU, about 30 s an epoch on 110 games. `agent/clone.py` is the runtime policy: per
step the network scores every unit without a job; a unit keeps its (destination, op) job
while the op stays possible, walks there and does it; the four best destinations are
tried before the unit falls to the greedy executor; jobs' tiles are off the greedy table.
`plan.POLICY` ("executor" or "clone", `KAGG_POLICY` override) selects it in
`agent/hybrid.py` and `agent/executor.py`; the clone plays after the opening tape with no
public tape in between. The market is still `agent/market.py` (the mined rules come next).

### Checkpoint: the first real training epoch, and the mined purchase schedule
Trainer fixed (plain cross-entropy on the destination, -1e4 mask): one epoch on 110 games
of THIRD FARM CLUB, tested on its 25 latest games (177,508 unit-steps): destination top-1
0.663 and within one tile 0.813, op given the true destination 0.834, joint 0.561, NONE
0.225; per op CARE 0.94, FEED 0.80, PLANT 0.75, WATER 0.71, COLLECT 0.61, FERTILIZE 0.41,
HARVEST 0.37; joint by day 0.72 (days 0-5), 0.57, 0.55, 0.49 (days 24-29). A six-epoch run
follows, and the general model (six training teams, stride 2, four epochs, tested on DSM,
Unknown Mother-Goose, THIRD FARM CLUB and HowardLeeTW) runs after it on the same GPU.
`scripts/learn/mine_market.py` on the 135 games: hands by day (median) 4, 4, 6, 6, 6, 6,
11, 9, 9, 12, 13, 10, 9, 8, 9, 11, 10, 10, 11 x5, 10, 11, 11, 11, 10, 9, 11; land NE during
day 6 and SW during day 9, SE never; animals owned by day (median): cows 2 from day 1, 6
on day 7, 7 on day 9, 9 on day 10, 10 from day 13 with a milk shop (105 games) and let go
from day 17 without one (30 games: 9 to 2 by day 24); sheep 3, and on Yarn Store towns (37)
6 on day 7, 8 on day 9, 10 on day 10, 11 from day 14 with cows held at 4-7; geese 1 on day
7, 2 on day 8, 4-5 on days 12-13, 6 from day 15, 7 with an egg shop (78), 3-4 without,
3-4 on Yarn towns. Seeds: strawberries mostly on day 6 (about 10) after 1-2 a day on days
2-4, melon 3+2+1 on days 0-2, carrots and tomatoes from day 11 and days 18-27, wheat 6
on day 0 and 12 on day 9 for feed then 2-5 a day. These are now `plan.TFC_*` and
`plan.tfc_animal_targets(day, shops)`; `agent/market.py` uses them when `POLICY ==
"clone"`, and buys the seeds the clone reports wanting (`clone_seed_wanted`) instead
of the v41 layout's.

### Checkpoint: six epochs of the THIRD FARM CLUB clone
Test set (its 25 latest games, 177,508 unit-steps), by epoch: destination top-1 0.667,
0.706, 0.726, 0.742, 0.748, 0.753; within one tile 0.815 to 0.856; op given the true
destination 0.843 to 0.910; joint (right tile and right op) 0.571, 0.608, 0.662, 0.681,
0.692, 0.697; NONE 0.27 (the model gives a job to most units the team leaves idle). Joint
by day at epoch 5: 0.978 on days 0-5 (the tape's days), 0.70 on days 6-15, 0.65 on days
16-23, 0.62 on days 24-29. Per op at epoch 5: CARE 0.955, PICKUP 0.918, PLACE 0.893,
PLANT 0.89, DROP 0.873, FEED 0.872, WATER 0.80, BUILD_PASTURE 0.77, COLLECT 0.75,
HARVEST 0.65, FERTILIZE 0.64, BUILD_COOP 0.48, DIG 0.40. Gate G1 asks for joint 0.80 and
op-given-destination 0.90: the second is met, the first is not, and the curve is still
rising, so a ten-epoch continuation at a lower rate runs alongside the general model.
The one-epoch weights are exported to `agent/clone_weights.npz` (numpy forward equal to
torch) for the first end-to-end runs: one local game for errors and step time, then ten
recorded-seat fidelity games.

### Checkpoint: the clone plays end to end; two thirds of the team's bank
The first export dropped the `tile_w` weights along with the coordinate buffers (a prefix
filter; every step after the opening fell to `main.py`'s PASS fallback), fixed and
re-exported from the six-epoch weights: 1.4 MB, 26 arrays, numpy within 1.9e-5 of torch.
One game against pass on seed 1 (decoupled; opening tape 144 steps then the clone with
the greedy executor as fallback, THIRD FARM CLUB's purchase schedule): bank 114,849, no
fallback steps, 2.2 ms a step (10.5 ms max), 13 hands on day 10 and 11 on day 20. Ops
per game against the team's own (means over its 135 games): WATER 1,004 / 1,089, HARVEST
335 / 436, COLLECT 310 / 414, FEED 304 / 373, CARE 307 / 340, PLANT 208 / 239, FERTILIZE
91 / 172, PICKUP 372 / 327, PASS 883 / 669, moves 3,110 / 2,880; final farm 7 weeds, 6
empty tiles, 8 empty pastures and 2 empty coops (the team ends with 3.6 weeds and 5.6
empty structures). Fidelity in the team's recorded seat, 10 latest games: bank 0.67 of
the recorded median, 0 wins, and the opponents bank far more than they did (one game:
143,712 against 111,484 recorded). So the clone reaches the team's farm and schedule
but under-harvests, fertilizes half as much, lets animals escape and idles more; the
per-op recalls said as much (HARVEST 0.65, FERTILIZE 0.64, NONE 0.27). Next, one change
at a time on the fidelity set: a NONE prediction hands the unit to the greedy executor
instead of idling; then the longer-trained and the general-pretrained weights.

### Checkpoint: the six-epoch clone against the live lines
Decoupled, seeds 0-9 both seats: against v41 0-20, mean bank 72,553 against 126,945,
margin -54,392, basket 80,937 (strawberries 152, milk 144, wool 127, carrots 43, tomatoes
14); against v7 0-20, 69,451 against 126,682, margin -57,231, basket 79,163. The line
banks 20-27k more against the clone than against anything else we have fielded, so the
clone both under-produces (basket 81k against the executor's 105k) and leaves the market
to the line's dumps. The harness's scratch directory was withdrawn mid-session, so the
fidelity harness now lives in the repo (`scripts/learn/fidelity.py`) with a revenue
diagnostic (`scripts/learn/revenue.py`, executed revenue by product and hour for both
seats of a local game). Free memory fell to 2.8 GB with two training processes and the
browser resident; the memory watchdog killed one run earlier in the session, so the
runs are sequenced from here.

### Checkpoint: ten more epochs plateau at joint 0.72
Continuation from the six-epoch weights at half the learning rate (`tfc2`, 10 epochs):
joint 0.685, 0.687, 0.696, 0.703, 0.700, 0.712, 0.713, 0.718, 0.717, 0.719; destination
top-1 0.745 to 0.770, within one tile 0.867, op given the destination 0.921 at the end.
By day at epoch 9: 0.994 on days 0-5, 0.734 on days 6-15. On 110 games the offline curve
flattens a full eight points short of gate G1's joint 0.80; the general model's
pretraining is the remaining offline lever, and the runtime's behaviour (what it does
with the 28% of jobs it gets wrong) matters more than the last points of accuracy.
