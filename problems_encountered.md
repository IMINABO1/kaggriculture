# Problems Encountered

Every problem hit on this project, by date, chronological. Each entry records the symptom, the
cause, the fix, and who caught it. When the verifier or Iminabo catches something I missed, the
entry also says why I missed it and what changes so it does not happen again.

## 2026-09-14

### P1: `uv sync` failed on first run
- **Symptom:** hatchling build error `OSError: Readme file does not exist: README.md`.
- **Cause:** `pyproject.toml` declared `readme = "README.md"` before the file existed.
- **Fix:** created `README.md`, re-ran `uv sync`.
- **Caught by:** me (build error).
- **Lesson:** create every file the project metadata references before the first sync.

### P2: Windows console could not print scraped forum text
- **Symptom:** `UnicodeEncodeError: 'charmap' codec can't encode character '​'` while printing
  discussion threads during research.
- **Cause:** the shell's Python stdout defaults to cp1252 on this machine.
- **Fix:** run with `PYTHONIOENCODING=utf-8`. Project scripts avoid printing scraped text.
- **Caught by:** me.

### P3: Kaggle notebook bodies are invisible to page-text extraction
- **Symptom:** reading a notebook page returned only its table of contents.
- **Cause:** Kaggle renders notebook output inside an iframe on `kaggleusercontent.com`.
- **Fix:** read the iframe's `src` and load that URL directly.
- **Caught by:** me.

### P4: importing kaggle-environments floods stderr
- **Symptom:** every `import kaggle_environments` prints ~336 lines of
  `OpenSpiel exception: Unknown game 'universal_poker'...` followed by the full game list, twice.
  Arena output was unreadable.
- **Cause:** the package eagerly loads every env, and its open_spiel poker envs fail to register
  on this Windows build. Harmless for Kaggriculture, but the messages come from native code.
- **Fix:** `scripts/kenv.py` imports the package with file descriptor 2 pointed at devnull
  (a `sys.stderr` redirect does not catch native writes). All scripts import through it.
- **Caught by:** me.

### P5: `ruff format .` rewrote the competition docs
- **Symptom:** after formatting, `data/README.md` and `data/AGENTS.md` no longer matched the
  files in `kaggriculture.zip` (aligned dict literals in the observation-format examples were
  reflowed; one trailing newline added).
- **Cause:** this ruff version formats fenced Python blocks inside Markdown, and `data/` was
  not excluded. I ran `ruff format .` repo-wide without checking which non-Python files it
  would touch.
- **Fix:** restored both files from the zip (verified byte-identical with `cmp`) and added
  `extend-exclude = ["data"]` to `[tool.ruff]`.
- **Caught by:** me, but only because the harness reported the files as changed and I checked
  against the zip. I would otherwise have committed silently altered reference docs.
- **Why I missed it:** assumed a Python formatter only touches `.py` files.
- **Prevention:** run formatters with an explicit path list, or check `git status` for
  unexpected modifications before every commit. Reference material under `data/` is read-only.

### P6: leaderboard snapshot crashed on a team name
- **Symptom:** `scripts/top10/snapshot.py` died with `CalledProcessError` from
  `kaggle competitions leaderboard -s -v`; the CLI had printed
  `'charmap' codec can't encode characters in position 9-13` after the first rows.
- **Cause:** same root cause as P2, one layer down: the CLI runs as a subprocess whose stdout
  is cp1252 on this machine, and the top 50 contains team names in mathematical bold and CJK
  characters. My subprocess call also used `check=True` without surfacing stderr, so the first
  run in the background log showed only a traceback.
- **Fix, first attempt:** pass `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` to the subprocess and
  decode its output as UTF-8. That fixed the CLI call, and the rerun then crashed one line
  later in my own `print` of the rank-7 team name, for the same reason. Two background runs
  lost to one root cause.
- **Fix, second attempt:** `research/__init__.py` reconfigures `sys.stdout` and `sys.stderr` to
  UTF-8 on import, so every research script and test is covered without remembering anything.
- **Caught by:** me (background job exited 1, twice).
- **Why I missed it the first time:** I patched the layer that failed instead of the property
  that failed (console encoding for the whole process tree).
- **Prevention:** on this machine, treat "prints user-generated text" as "needs UTF-8 streams",
  and fix it once at the process level, not per call site.

### P7: the history crawl died on the episode endpoint's rate limit
- **Symptom:** `crawl.py` exited after 81 of ~190 submissions with
  `RuntimeError: ListEpisodes kept throttling for submission 55865537`. Progress had slowed
  from ~40 listings a minute (plan-mode probe) to ~3.
- **Cause:** the public endpoint returns 429 in bursts; my client gave up after six tries with
  a linear 5-30 s backoff. I had also started the bulk replay download (65 replays a minute
  through the authenticated client) from the same address at the same time, which is the
  likeliest reason the bursts got denser.
- **Fix:** exponential backoff capped at 120 s over eight attempts, honour `Retry-After`,
  and fall back to the authenticated Python client (same episodes and agents, no ratings;
  the cached payload is marked `source=client` so a refresh can fill the ratings later).
  The crawl was already resumable through its per-submission cache, so nothing was lost.
- **Caught by:** me (background job exited 1).
- **Prevention:** never run the metadata crawl concurrently with bulk downloads; make every
  network client survive a throttling burst rather than raise on it.
- **Follow-up:** after the downloads ended, the public endpoint still answered every call with
  429 and `Retry-After: 30`, so the crawl was moved to the authenticated client (5 listings
  in 1.1 s in a probe). That client then returned 429 from `api.kaggle.com` after ~60 fast
  listings. Final shape: client-first with 1.5 s spacing and exponential backoff (10 tries,
  capped at 90 s), ratings joined from the community index instead of the public endpoint.

### P8: `git push` disconnected twice on a 4.5 MB commit
- **Symptom:** `send-pack: unexpected disconnect while reading sideband packet` /
  `the remote end hung up unexpectedly`, twice in a row, on the commit that first added
  `history.parquet` (3 MB) and `features.parquet` (1.5 MB).
- **Cause:** Git's default HTTP post buffer (1 MiB) makes larger pushes go through chunked
  transfer, which this connection dropped.
- **Fix:** `git config http.postBuffer 524288000` (repo-local); the push then succeeded.
- **Caught by:** me.
- **Note:** `features.parquet` will grow to roughly 8 MB with all 4,043 episodes. It stays
  tracked because it lets the verifier check every report number without the 100 GB of
  replays behind it.

### P9: the replay fetch and the queued pipeline were killed for low memory
- **Symptom:** both background jobs stopped by the harness ("system is running low on
  memory") at 2,150 of 3,351 downloads. The machine had 5.7 GB of 31 GB free with none of my
  processes alive afterwards, so the rest of the desktop was already using most of it.
- **Cause:** `download_replay` validated each 30 MB download with a full `json.loads`, which
  expands to several hundred MB of Python objects per worker, three workers at a time, on top
  of the trace extractor's own full parses.
- **Fix:** structural validation only (starts with `{`, ends with `}`, contains `"steps"`);
  fetch resumed with two workers; extraction runs with two workers. Nothing was lost: every
  stored replay is written to a temp file and renamed only when complete.
- **Caught by:** the harness (kill notification), then me.
- **Prevention:** never fully parse a large payload just to check it; size worker counts to
  the memory actually free, not the core count.

### P10: sell orders that executed nothing counted toward "first sell day"
- **Symptom:** the market-timing table showed DSM selling melon, strawberry, milk, and wool
  from day 0, before any exist.
- **Cause:** DSM issues SELL orders every turn; after P4's fix those rows carry `n = 0`
  executed units, but the day statistics still included them.
- **Fix:** zero-unit sells are dropped before computing first and last sell days
  (`scripts/top10/extract.py`); unit totals were already unaffected.
- **Caught by:** me, reading the final summary table (a day-0 melon sale is impossible).
- **Lesson:** when a derived record can legitimately be empty, exclude it from "first" and
  "last" statistics explicitly; sums forgive zeros, extrema do not.

### P11: "latest episode" picked the wrong current submission for four teams
- **Symptom:** after the second crawl, seven teams had `current_sub_source = latest-episode`
  (the client listing carries no team block, so `crawl.py` falls back to the submission of
  the team's most recent public game). Fetching the raw endpoint's team block showed four of
  the seven were wrong: アルモンド (56230634 → 56233099), 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔, elmo, and doubao.
  アルモンド was in the first study, so its published dossier's "current submission"
  section (C0 window, rating path, determinism verdict) described the team's *other* active
  submission.
- **Cause:** every team keeps two active submissions and both play constantly, so the most
  recently played one is the leaderboard submission only half the time. I treated
  "latest episode" as a safe approximation without checking it against the one endpoint
  that states the leaderboard submission.
- **Fix:** `refresh_ratings.py` now reads `publicLeaderboardSubmissionId` from the raw
  payload's team block, corrects `teams.csv` and `history.parquet` for guessed teams, and
  fetches those teams' submissions first; it runs before `sample.py`. Catalyst, the other
  first-study team with a guessed submission, was confirmed correct.
- **Caught by:** me, only because I questioned the fallback while reviewing the crawl
  output for the new batch. The verifier did not flag it and neither did I in the first pass.
- **Why I missed it:** the first crawl had two guessed teams out of 14 and I read the
  fallback as harmless; a 50/50 guess on the thing the C0 window is defined by is not.
- **Prevention:** a derived label that a downstream window depends on must be either
  verified against its source of truth or marked as a guess in the report. The rebuilt
  report regenerates アルモンド's dossier from the right submission.

### P12: replay downloads stalled, then Kaggle started rationing them
- **Symptom:** the first fetch chunk for the batch stored 158 replays in 12 minutes and
  then nothing for 20 minutes. The process held two established connections to Kaggle,
  no failure was logged, no temp file was being written. Killing it and probing by hand
  returned `429 Too many requests` with `Retry-After: 1180` (about 20 minutes), and the
  value grew with each probe.
- **Cause:** two layers. The client sends its metadata request with no timeout and
  streams replay chunks with a 300 s timeout and five retries, so a connection Kaggle
  stops serving parks a worker for up to half an hour with no error. Underneath, the
  replay endpoint now enforces a quota (the first study's unfinished Q3 window, "the API
  started dropping connections", was very likely the same quota showing up as hangs).
- **Fix:** `research/kaggle_api.py` installs a (30 s connect, 90 s read) default timeout on
  every `requests` session send, streams replays itself with a 90 s chunk timeout and two
  retries, and keeps a quota gate shared by all workers: a 429 parks every worker until
  `Retry-After` has elapsed instead of burning the retry budget of each episode. The fetch
  now runs as one long background job; it is resumable, so a kill costs one file.
- **Caught by:** me, from the replay count not moving while the job looked alive.
- **Why I missed it:** the first study's download rate (65 a minute for an hour) made me
  treat the endpoint as unlimited, and I piped the fetch through `tail`, which hid its
  progress lines until exit. Progress that cannot be seen cannot be judged.
- **Prevention:** every network worker needs a timeout and a visible heartbeat; measure
  the quota (replays per window) and plan fetch volume against it before promising a
  schedule. The community replay dataset was checked as an alternative source and covers
  only 92 of the missing games, so the quota is the binding constraint.

## 2026-09-15

### P13: the "gold" batch was cut at rank 50, not at Kaggle's gold line
- **Symptom:** the next-15 batch and the memo's group comparison were labelled "the rest
  of the gold zone" although 7 of the 15 teams (ranks 29-48) are silver under Kaggle's
  rule, which I had computed myself (top 10 + 0.2% of 9,066 teams = rank 28).
- **Cause:** I followed the handoff's example chunks (11-50) instead of the rule I had
  just verified, and softened it in the text ("gold under the top-50 assumption") instead
  of cutting the batch at 28.
- **Fix:** every team now carries a `zone` (gold / silver / bronze / none) computed from
  the full leaderboard at snapshot time; the comparison is re-cut as top-14 vs the rest of
  gold, and silver and bronze are sampled as their own groups (chunks deep in each zone,
  current-submission windows only, because of the replay quota).
- **Caught by:** Iminabo ("the limit for gold is 28, 29 is silver").
- **Why I missed it:** I treated the instruction's illustrative ranks as the rule and the
  rule as a footnote. When a rule has been checked, the checked rule wins over the example.
- **Prevention:** medal zones come from `snapshot.py --full` (Kaggle's rule applied to the
  live team count), never from a hand-picked cutoff, and every report table shows the zone.

### P14: the 63-team crawl died on one dropped connection
- **Symptom:** `crawl.py` exited with `ConnectionError: Remote end closed connection
  without response` after 555 listings, before writing `teams.csv`.
- **Cause:** the listing client retried only on 429; every other exception propagated.
- **Fix:** connection errors and timeouts now back off and retry like a 429 (up to ten
  attempts). The crawl resumed from its per-submission cache and lost nothing.
- **Caught by:** me (background job exited with a traceback).
- **Prevention:** the same rule as P7 and P12: a network call in a long job retries on
  every transient failure, not only the one seen last.

### P15: the detached fetcher stalled silently for three and a half hours
- **Symptom:** the fetch log stopped at 21:18Z and no replay landed until 00:49Z, while
  both fetcher processes stayed alive with no error. The hourly maintenance job did not
  fire between 21:23Z and 00:23Z either.
- **Cause:** most likely the machine slept (both the fetcher's connections and the
  in-session scheduler went quiet at the same time); after waking, the two worker threads
  sat in requests that never returned. Not proven; no error was recorded anywhere.
- **Fix:** killed and relaunched the fetcher; it immediately drew a 125-replay burst from
  the quota that had refilled during the stall. The hourly job now restarts the fetcher
  whenever no replay has landed for 20 minutes, alive or not.
- **Caught by:** me, on the next hourly check (C0 count unchanged, log timestamp stale).
- **Prevention:** liveness means "produced output recently", not "process exists".

### P16: the ratings refresher overwrote three pinned submissions
- **Symptom:** after the C0 fetch finished, `refresh_ratings.py` reported "3 current
  submissions corrected", one of them yomogii, whose studied submission had been pinned
  to the first snapshot by `sample.py --keep-c0`.
- **Cause:** the refresher corrects every team whose `current_sub_source` is not
  "leaderboard"; the pin writes "frozen", which it read as a guess.
- **Fix:** "frozen" is now authoritative in the refresher; `sample.py --keep-c0` was re-run
  to restore the three pins before the feature table was rebuilt.
- **Caught by:** me, reading the refresher's output before building the report.
- **Lesson:** a new marker value must be added to every consumer's allow-list the moment
  it is introduced, not when it bites.

## 2026-09-16

### P17: memo finding 4 read a conditional rate as a mechanism (the "day-1 opponent read")
- **Symptom:** `decision_memo.md` finding 4 and the recommended architecture's layer 2 said
  Majkel1337 and Orbital Terraformer "read the first hours of the opponent's farm and change
  their own day" because being off their modal day-1 line was far more likely when the
  opponent was off its own modal line (70% vs 16%). Reading the four lines shows identical
  purchases and identical farmer actions; they differ only in the last one to three wheat
  seeds the budget allows, and the wheat price (moved a dollar by the opponent's turn-0
  trades) decides that. No team on the plateau changes its day-1 plan for the opponent.
- **Cause:** the branch-driver table was built as a conditional-rate statistic and the memo
  wrote it up as a causal read without diffing the actions between the branches. The
  handoff flagged this as unverified ("nobody has read what the branch actually changes").
- **Fix:** finding 4 and the layer-2 recommendation are rewritten in the memo from this
  analysis; the analysis report states the mechanism with the turn-by-turn evidence.
- **Caught by:** me, in the thorough-analysis phase, following the handoff's "check first" list.
- **Why I missed it:** the statistic was suggestive and matched a story (a smart #1 that
  reads its opponent), and the study's pace favoured tables over reading action streams.
- **Prevention:** a "driver" or "reactive" claim about a team is not reportable until the
  actions on the two sides of the branch have been diffed and the difference named.

### P18: executed sale units were capped by the shed *before* the turn's unit actions
- **Symptom:** summing each seat's recorded sale revenue gives 35-50% less than its final bank
  implies for 55 of the 59 profiled teams (Artem The Farmer: 70k recorded against 123k
  banked in one game). Only Majkel1337, Orbital Terraformer, DSM, Ebi and Kaggriculture
  Agent are within 10%. The tape family's melon dump reads as 12 units when the replay
  shows 72; Artem's "6 melons a game" is really about 72.
- **Cause:** P10's fix capped executed units by the private shed as observed at the start
  of the turn. The engine runs unit actions (DROP, PLACE into the shed, PICKUP) before it
  processes market orders in the same turn, so an agent that harvests, walks to the shed,
  drops and sells in one turn sells from a shed the trace never saw. Most agents do exactly
  that; the three that sell a turn later were measured correctly, which is why the #1's
  sales looked four times larger than everyone else's.
- **Fix:** the tracer now replicates the engine's turn: both seats' DROP/PLACE/PICKUP are
  applied to copies of the sheds, then both market queues are processed in the engine's
  per-unit lockstep against the recorded market inventory, quoting each unit at the live
  price. Every sale carries executed units and revenue; the simulated end-of-turn money is
  checked against the recorded money for both seats and the mismatch count is stored in
  the trace. All sampled traces, the feature table, `groups.md`, `summary.md`, the dossiers
  and the memo's sales findings are rebuilt from it.
- **Caught by:** me, in the thorough-analysis phase, because the new realized-price table
  put Artem's revenue below its bank.
- **Why I missed it:** P10 was fixed by reading the observation, not the engine's turn
  order; the check "does revenue add up to the bank" was never run. Every derived
  quantity that has an accounting identity should be checked against it once.
- **Prevention:** the tracer stores a per-seat money-reconciliation count and error
  (`money_check`), and `research/features.py` blanks the sales columns of every seat whose
  count is above zero before `analyze.py` or `deep.py` take a median. (Corrected 2026-09-16:
  the first version of this entry claimed the filter existed when only the counter did; P19.)
- **What does not reconcile:** 410 of 14,788 seat rows. 379 are on engine versions
  1.32.2-1.32.6, whose market the replica does not model, and they fall on whole historical
  windows: Emile Andrieu's, Thomas Tschinkel's and THUNDER THUNDER's first-50 windows and
  Mengfei Li's first quarter window (50 seats each, errors up to $1,114 a game), plus a few
  seats of Kaggriculture Agent, kevin park and Mengfei Li's first window. 31 are on 1.32.7
  (8 of them current-submission rows) and all but one sit at the last executed step: the
  recorded inventory shows a shop tick's worth of units removed before that step's sales
  were priced, which the replica does not reproduce (checked on 108862197: shed identical
  after the unit actions, 4 strawberries missing from the inventory, $466 more revenue). It
  is bounded at $466 a game and is left as a known gap.
- **Affected published numbers (before rebuild):** every `sold_*`, `sell_first/last_day_*`,
  `sold_units_total`, `sells_last_3_days` column; groups.md market tables; memo findings 6,
  7, 13, 18 (market parts); the "melon last sell day 19 vs 11" separator is suspect because
  the family's later melon sales were dropped as zero-unit sells.

### P19: an unverified claim about the code was written into the record
- **Symptom:** the P18 entry said "the feature build refuses seats where [the reconciliation
  error] exceeds a few dollars a game". No such filter existed; `money_check_turns` and
  `money_check_max_error` were computed and stored, and nothing downstream read them. The
  report and journal said money reconciles "for 99% of current-submission seats", which was
  true as scoped and silent about the 410 seat rows (four teams' whole historical windows,
  errors up to $1,114) that fed the dossiers' evolution tables unflagged.
- **Cause:** I wrote the prevention line as the design I intended, in the same sentence as
  the parts I had built, and never went back to build or check it. The "99%" line was scoped
  to the slice I had looked at.
- **Fix:** `research/features.py` blanks the sales columns of unreliable seats before any
  median; `analyze.py` and `deep.py` apply it and print the exclusion; `analysis.md`,
  `METHOD.md` and P18 state the true scope and name the affected windows.
- **Caught by:** the verifier session, by grepping the code for the claimed filter and
  querying `features.parquet` for the failing rows.
- **Why I missed it:** the same failure the Pokémon TCG post-mortem records twice (the
  "our search can't do combinatorial targeting" claim that was never checked; gauntlet
  results reported as confirmation): a plausible statement about what the code does or what
  the data shows, written down as if verified. Here it was caught before the handoff because
  the verifier was asked to check.
- **Prevention:** before writing "X refuses / excludes / drops / guarantees Y" into the
  journal, the problems log or a report, grep for the code that does it or run the query
  that shows it, and quote the count. Any statement of coverage ("reconciles for 99%")
  names the denominator and the excluded rows. Applies to every remaining session on this
  project.

### P20: the breadth-of-response table in analysis.md scored every team 1
- **Symptom:** `analysis.md` section 3 showed "breadth (0-5)" = 1 for all 59 teams and zone
  medians 1 / 1 / 1 / 1 with AUC 0.50 (p=1.00) in every row, while the journal, the memo
  (finding 4, "What this changes") and the handoff quoted medians 4.5 / 3.5 / 2 / 1 and AUC
  0.86 / 0.72 / 0.67. Both builds of the report (commits d7feffc and 09b6857) carried the
  wrong table.
- **Cause:** `deep.py` computed the score as `(d_sheep > 3) + (d_cows > 1.5) + ...` on numpy
  floats; numpy booleans add as logical OR (`np.True_ + np.True_ == np.True_`), so any team
  that passed one threshold scored 1. The 4.5 / 3.5 / 2 / 1 figures came from the earlier
  ad-hoc script, which used Python floats, and were never re-checked against the report.
- **Fix:** the score now sums `int(bool(x))` per threshold; the rebuilt table gives medians
  4.5 / 3.5 / 2 / 1, means 4.14 / 3.43 / 2.48 / 1.30, AUC top-14 over gold 0.67 (p=0.11),
  gold over silver 0.73 (p=0.02), silver over bronze 0.86 (p=0.00), which matches the memo
  within rounding (0.72 there for gold over silver).
- **Caught by:** me, reading analysis.md in full at the start of the build phase.
- **Why I missed it (previous session):** the report was regenerated after the ad-hoc check
  and the table was not re-read; a number quoted from one script was assumed to be what the
  other script printed. Same family as P19: a figure written into the record from a source
  other than the artifact that is supposed to carry it.
- **Prevention:** after any rebuild, diff the regenerated report against the numbers the
  memo and journal quote from it, and quote from the report, not from the scratch script.

### P21: a scratch file named bisect.py shadowed the standard library and re-ran the arena
- **Symptom:** a diagnostic that imported kaggle-environments failed with "cannot import name
  'bisect' from 'bisect'", and its output began with the lines of an earlier bisect run,
  after a delay of several minutes.
- **Cause:** the scratchpad directory holds the script being run, so it is first on
  `sys.path`; `random` imports `bisect`, which resolved to my `bisect.py`, whose top-level
  code ran five arena games and rewrote `agent/executor.py` before failing.
- **Fix:** renamed to `ab_bisect.py`; the executor was restored by the script's own final
  step (verified by grep for the opportunistic-deposit line).
- **Caught by:** me, from the traceback.
- **Prevention:** scratch scripts never take a standard-library module's name, and a script
  that rewrites project files does its work under `if __name__ == "__main__"`.

### P22: "fixed seeds" are not fixed environments across executor changes
- **Symptom:** seed 1 unlocked different shops in two arena runs of the same seed, and a
  change that touched only one watering priority moved v5's mean bank from 94,145 to
  103,565 and the competition margin by 11k.
- **Cause:** `_end_of_day` draws the day's weeds and the next shop from one
  `random.Random` per day, and every empty tile on either farm consumes one draw before the
  shop is chosen, so our own empty-tile count decides the town for both players.
- **Fix:** `scripts/eval.sh` plays 8 production and 10 competition seeds (28 games) and the
  verdict is the mean; single-seed diagnostics print the shops next to the numbers.
- **Caught by:** me, from the census script printing the shop list of both runs.
- **Why the previous session missed it:** it read `_end_of_day` for the weed order (the
  gauntlet seat rule) and stopped two lines above the shop draw; the bisect rule was written
  on three and five seeds without checking what else the seed fixed.
- **Prevention:** an A/B on fixed seeds is trusted only when the environment is shown to be
  identical between arms (here: the shop lists), or when the seed count is large enough
  that the coupled draw averages out; every diagnostic that names a seed names its shops.

## 2026-09-17

### P23: an arena run launched in the same response as a code edit measured a moving target
- **Symptom:** the hybrid on v7's opening measured -5,542 against v41 where the same
  executor on v41's opening had measured -3,774 the day before, although both tapes leave
  an identical farm and shed at the switch and v7's bank is 1.1-1.5k higher there.
- **Cause:** the background arena was started in the same response as the edits that
  hooked the first, untested cut of the day planner into `agent/executor.py`; the arena's
  workers import the working tree when they start, so some or all of the 40 games may have
  run the planner (which the evaluator later scored 3.5k below greedy) rather than the
  committed executor. Which games did cannot be known from the output.
- **Fix:** `KAGG_PLAN_FROM_DAY` switches the planner off for an arena run; the run is
  repeated with it off and the earlier numbers are struck.
- **Caught by:** me, when the shed-at-switch check left no other explanation.
- **Why I missed it:** the tool calls in one response were treated as sequential; a
  background command and an edit are not, and the arena reads the tree, not a commit.
- **Prevention:** no background arena or evaluator run is launched in a response that also
  edits `agent/`; a measurement names the commit or the environment override it ran under.
