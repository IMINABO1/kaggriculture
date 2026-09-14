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
