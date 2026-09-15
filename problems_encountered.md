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
