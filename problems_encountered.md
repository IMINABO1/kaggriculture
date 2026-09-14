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
