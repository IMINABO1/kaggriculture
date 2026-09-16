# How the top-14 and next-15 observation study was done

This is the plain-language description of the study whose results live in `summary.md`,
`groups.md`, the team dossiers, and `decision_memo.md`. It says what was observed, how, and
how to rerun it.

## 1. Who was studied: the top-14, then the next-15

The leaderboard's ranks 5 to 15 sit inside the rating noise the former #1 documented on the
forum (about ±50 points), and the tenth place changed hands three times in the hour the study
was set up. So "the top 10" was taken as a band: every team that was top-10 either in
Iminabo's screenshot or on the live board when the pipeline snapshotted it (2026-09-14T1936Z).
That gave 14 teams, the **top-14** group.

The second group answers a different question: is there something the rest of the gold zone
does not do that the top 10 do? Iminabo's rule was contiguous chunks of ranks with gaps
between them, across the gold zone outside the 14, about 15 teams. The board was snapshotted
once more (2026-09-15T0033Z) and chunks "8-9, 13-14, 20-23, 29-31, 38-39, 47-48" were taken;
a chunk skips teams already in the top-14 and extends past them, because the board moves
between reading it and snapshotting it. The **next-15** are ranks 8, 11, 17, 19, 20, 21, 22,
23, 29, 30, 31, 38, 39, 47, and 48 at that snapshot (names in `summary.md` and `groups.md`).
That batch mixed zones: under Kaggle's rule for competitions with 1,000+ teams (gold = top
10 + 0.2% of teams, silver = top 5%, bronze = top 10%) gold ended at rank 28, so 8 of the
15 were gold and 7 silver (P13 in `problems_encountered.md`). The study was therefore
re-cut by medal zone from a snapshot of the **full** leaderboard (2026-09-15T1342Z, 9,125
teams: gold to rank 28, silver to 456, bronze to 912; `snapshot.py --full`):
- **top-14**: the original 14, kept as the study's subject (two had slipped into silver by
  that snapshot);
- **gold**: every other gold team the crawl could seed, ranks 6-28 (16 teams);
- **silver**: the first-batch teams now in silver plus rank chunks 120-122, 250-252,
  400-402 (21 teams);
- **bronze**: rank chunks 470-472, 600-602, 750-752, 880-882 (12 teams; one team without a
  seed was skipped and the chunk extended).
Ranks move by tens of places in a day at these depths, so every table shows each team's
zone and rank at the full snapshot and, for the first 29, the rank at the first snapshot.
`data/top10/snapshot_latest.csv` carries `zone` and `group` columns.

## 2. Which games were looked at

For each team, its **history** is every public ladder game across every submission the crawl
could find (validation self-play games excluded), ordered by time. Iminabo's rule was: the
first 50 games and the last 50 no matter what, and for long histories also 50-game windows at
the quarter points. Every team turned out to have 906 to 9,162 games, so all five windows
apply:

| window | games |
|---|---|
| F | first 50 of the team's history |
| Q1, Q2, Q3 | 50 centred at 25%, 50%, 75% of the history |
| L | last 50 |
| C0 | first 50 of the team's *current* submission (its ladder-entry phase) |

The rule is `research/sampling.py`; the resulting list is `data/top10/sample.csv`. The
top-14's history windows are frozen at the first sample
(`data/top10/sample_top14_2026-09-14T1936Z.csv`): the second crawl lengthened their
histories, which would have moved every quarter-point window for no gain. Only their C0 was
recomputed, because one team's current submission had been mis-identified (P11 in
`problems_encountered.md`). The first batch of 15 was cut fresh from the second snapshot
with all windows (`data/top10/sample_29teams_2026-09-15T0033Z.csv`). The 34 teams added
for the zone comparison get only C0, the current submission's first 50 games: Kaggle
rations replay downloads to roughly 120 an hour (P12), and the group comparison is built
on current submissions anyway.

## 3. Where the data came from

- **Which submissions belong to a team**: seeded from `georgymamarin/kaggriculture-episodes`
  (a community index of 145k games, Apache-2.0) and from the listings already cached (two
  batch teams are absent from the index but appear as opponents of studied teams), then
  expanded by following every listed game's participants until no new submission of a
  studied team appeared. 843 submissions in total for the 29 teams.
- **Which submission is a team's current one**: the public endpoint's team block names the
  leaderboard submission. The client listing does not, and "the submission of the latest
  game" is wrong half the time because both active submissions play constantly, so the
  ratings refresher reads the team block and corrects `teams.csv` before sampling.
- **Every game of every submission**: Kaggle's episode listing. The public JSON endpoint
  returns ratings before and after each game but throttles for long stretches; the
  authenticated client is fast but returns no ratings. The crawl uses the client, joins
  ratings from the community index, and a slow refresher (`refresh_ratings.py`) fills the rest
  from the public endpoint. Result: `data/top10/history.parquet`, 127,435 (submission,
  game) rows for the 29 teams, 100% of sampled games with a rating.
- **Replays**: one 20-33 MB JSON per game, stored zstd-compressed (about 150 KB each)
  under `data/replays/`. A replay holds both seats' actions and full observations for all
  720 turns. Two sources: the official daily episode datasets
  (`kaggle/kaggriculture-episodes-<date>`, each day's top-scoring 650-930 games as
  individual files, indexed by `scripts/top10/daily_index.py`, no quota) for the games
  they hold, and the authenticated client's replay endpoint for the rest. Kaggle rations
  that endpoint (429 with a Retry-After near 20 minutes once a quota is spent), so the
  fetcher waits it out with one shared gate and runs for hours. Final state on
  2026-09-16: 7,692 replays and traces on disk (about 1.2 GB), 7,394 of them in the
  sample, features for 14,788 (game, seat) rows; the top-14 have every window, the first
  batch of 15 has C0, L and F (Q1-Q3 dropped by decision, see the journal), the 34 zone
  teams have C0.

## 4. What was extracted from each game

Every replay is reduced to a **trace** (`research/trace.py`, stored under `data/traces/`)
with, per seat:

- the full action stream (so the game can be replayed or used as an arena opponent);
- per-day series: money at day start, hands, unlocked quadrants, farm composition at day
  end, shed contents, new weeds;
- events: land purchases, animal and seed purchases, plantings by crop and day, and every
  market order **as the engine executed it**: `research/market_replay.py` replays each
  turn's market from the recorded observation (both seats' DROP, PLACE and PICKUP applied
  to the sheds first, then both order queues in the engine's per-unit lockstep against the
  shared inventory, each unit quoted at the live price), so a sale carries its executed
  units and the revenue received, a purchase its executed units and spend. The simulated
  end-of-turn money is checked against the recorded money for both seats in every turn and
  the mismatch count is stored per seat (`money_check`; zero for 99% of seats). Traces
  carry `trace_version` 2; the earlier version capped sales by the shed as observed before
  the turn's unit actions and undercounted most teams' sales by 35-50% (P18);
- counts of every unit op (CARE, FERTILIZE, HARVEST, DIG, ...);
- three fingerprints at turns 24, 48, 100, 136, 200, 300, 400, 719:
  - the exact action-stream hash in the community's convention (comparable with their
    `stream_hashes.csv`, verified byte for byte in a test);
  - the same hash over farmer-and-hand actions only, and over market orders only;
  - an **order-insensitive plan signature**: the multiset of non-movement unit ops with
    their arguments plus executable market orders. Two games that follow the same plan along
    different paths hash the same; two games that plant, buy, or sell differently do not.
    Orders the engine cannot execute are ignored, and counted separately as `invalid_orders`.

The flat table `data/top10/features.parquet` has one row per (game, seat) with all of the
above as scalars, joined to the history (submission, ratings, opponent, result) and the
window labels. The day-by-day timeline shown in each dossier is built from the trace by
`research/narrate.py`.

## 4b. How the two groups were compared

`groups.md` (built by `analyze.py`) profiles each team on every sampled game of its
current submission: the first branch cut and its dominant driver (section 5), the share of
distinct games at turn 400, medians of the farm, market, weed, and noise features, and
the rating path. Group medians are compared feature by feature with a Mann-Whitney test
(`research/stats.py`): "P(top > next)" is the chance that a random top-14 team's value is
above a random next-15 team's, 0.5 meaning no separation. It also counts, per cut, how
many teams of each group sit on a field line byte-identical to another studied team's,
tallies all public games between the groups, and breaks down each group's sampled losses
by opponent group, margin, and the feature the winner differed in most (in pooled standard
deviations). Teams with fewer than 10 sampled current-submission games are left out.

## 5. How "deterministic or adaptive" was judged

For a submission's sampled games, at each turn cut, count the distinct lines and the share of
games on the most common one. The verdict text is mechanical:

- one line through turn T when at least 90% of games share it at T;
- "branching" from the first cut where that share drops below 90%;
- "reactive from day 1" when even turn 24 has no 90% line;
- "every game distinct by turn T" when the number of lines equals the number of games.

At the first branching cut, the dossier also reports what goes with being off the modal
line: a weed on the team's own farm before that day, the opponent being off *its* usual line
at the previous cut, the seat, the result, and (from day 4) the first shop draw. These are
plain conditional rates, not causal claims.

Everything else in the dossiers is medians per window (farm plan, market timing), per-window
ladder records, the rating path of the current submission, every loss in the first and last
windows with the three largest feature differences against the winner, head-to-head records
between the studied teams over their whole histories, and the episode ids behind each window.

## 6. Two checks that anchor the numbers

- A recorded game replayed locally from its seed and both action streams reproduces both
  banks to the dollar (`tests/test_research.py`). That is what makes traces trustworthy and
  recorded games usable as opponents.
- The same replay against a *different* opponent does not reproduce: weeds are drawn from a
  random stream shared by both farms, so the opponent's farm shifts every later draw. This is
  why tapes of reactive teams understate them in the arena.

## 7. Where things are

| what | where |
|---|---|
| summary tables and figures | `reports/top10/summary.md`, `reports/top10/figs/` |
| four-group comparison | `reports/top10/groups.md` |
| the thorough analysis (mechanisms, corrected market, structure, what to clone) | `reports/top10/analysis.md` (built by `scripts/top10/deep.py`) |
| one dossier per team | `reports/top10/<team>.md` |
| the recommendation | `reports/top10/decision_memo.md` |
| per-seat market and labour table, tile-level weed events | `data/top10/market.parquet` (`market_extract.py`), `data/top10/weed_events.parquet` (`weed_tiles.py`) |
| histories, sample, teams, features | `data/top10/` (tracked) |
| replays and traces | `data/replays/`, `data/traces/` (local only, regenerable) |
| arena opponents from the latest games | `opponents/top10/` (local only) |
| pipeline | `scripts/top10/`, `research/` |
| what went wrong along the way | `problems_encountered.md`, P7 to P10 |

## 8. Rerunning or extending it

```bash
uv run python scripts/top10/snapshot.py --top 0 --include "Team A,Team B" --ranks "8-9,13-14"  # top group by name, batch by rank chunks
uv run python scripts/top10/crawl.py                                          # histories
uv run python scripts/top10/refresh_ratings.py --budget-min 8                 # ratings; fixes guessed current submissions
uv run python scripts/top10/sample.py --freeze data/top10/sample_top14_2026-09-14T1936Z.csv   # windows (top-14 frozen)
uv run python scripts/top10/daily_index.py                                    # index the official daily episode datasets
uv run python scripts/top10/fetch.py --jobs 2 --source daily                  # replays held by the daily datasets, no quota
uv run python scripts/top10/fetch.py --jobs 2 --source endpoint               # the rest; waits out the quota, hours
uv run python scripts/top10/extract.py --traces-only --jobs 2 --limit 700     # traces, in chunks
uv run python scripts/top10/extract.py --upgrade --traces-only --jobs 5       # rebuild traces written by an older tracer
uv run python scripts/top10/extract.py --jobs 2                               # feature table
uv run python scripts/top10/market_extract.py 4                               # per-seat market and labour table
uv run python scripts/top10/weed_tiles.py --per-team 8 --jobs 2               # tile-level weed events (opens replays)
uv run python scripts/top10/analyze.py                                        # summary, groups, dossiers
uv run python scripts/top10/deep.py                                           # analysis.md and its figures
uv run python scripts/top10/export_tapes.py --window L --per-team 5           # arena opponents
```

Every stage is resumable per file. Keep the fetch and the crawl from running at the same
time (they share Kaggle's rate limit), keep extraction at two workers on this machine (the
harness kills background jobs when free memory is low), and expect the replay fetch to be
quota-bound: a burst of about 300, then a trickle of 2-4 a minute. `fetch.py --windows
C0,F` limits a run to the windows that carry findings; the quarter-point windows for the
second batch were left unfetched for that reason.
