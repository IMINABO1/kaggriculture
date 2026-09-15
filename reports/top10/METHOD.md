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
Which medal rule "gold zone" means: Kaggle's rule for competitions with 1,000+ teams is
gold = top 10 + 0.2%, which with the 9,066 teams entered is rank 28; silver is the top 5%
(rank 453). Iminabo's working assumption was gold = top 50. Ranks 8-23 of the batch are gold
either way; ranks 29-48 are gold only under the top-50 assumption, and every batch team
carries its rank so the comparison can be cut at 28 as well. One batch team (rank 8) was
inside the top 10 at snapshot time: the groups are "the 14" and "the next 15", not "top 10
today" and the rest. `data/top10/snapshot_latest.csv` carries a `group` column.

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
`problems_encountered.md`). The next-15 are cut fresh from the second snapshot.

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
  from the public endpoint. Result: `data/top10/history.parquet`, 56,338 (submission, game)
  rows, 99% of sampled games with a rating.
- **Replays**: downloaded through the authenticated client, one 20-33 MB JSON per game,
  stored zstd-compressed (about 150 KB each) under `data/replays/`. A replay holds both
  seats' actions and full observations for all 720 turns. Kaggle rations this endpoint
  (429 with a Retry-After near 20 minutes once a quota is spent), so the fetcher waits the
  quota out with one shared gate and runs for hours; see section 8 for the counts.

## 4. What was extracted from each game

Every replay is reduced to a **trace** (`research/trace.py`, stored under `data/traces/`)
with, per seat:

- the full action stream (so the game can be replayed or used as an arena opponent);
- per-day series: money at day start, hands, unlocked quadrants, farm composition at day
  end, shed contents, new weeds;
- events: land purchases, animal and seed purchases, plantings by crop and day, sells by
  product with the price at that step and the **executed** units (capped by what the shed
  held before the turn, because some agents request thousands of units every turn);
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
| top-14 vs next-15 comparison | `reports/top10/groups.md` |
| one dossier per team | `reports/top10/<team>.md` |
| the recommendation | `reports/top10/decision_memo.md` |
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
uv run python scripts/top10/fetch.py --jobs 3                                 # replays; waits out the quota, hours
uv run python scripts/top10/extract.py --traces-only --jobs 2 --limit 700     # traces, in chunks
uv run python scripts/top10/extract.py --jobs 2                               # feature table
uv run python scripts/top10/analyze.py                                        # summary, groups, dossiers
uv run python scripts/top10/export_tapes.py --window L --per-team 5           # arena opponents
```

Every stage is resumable per file. Keep the fetch and the crawl from running at the same
time (they share Kaggle's rate limit), keep extraction at two workers on this machine (the
harness kills background jobs when free memory is low), and expect the replay fetch to be
quota-bound: it downloads a burst, then waits about 20 minutes, and repeats.
