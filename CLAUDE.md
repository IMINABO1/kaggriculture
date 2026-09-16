# Kaggriculture project conventions

Goal: finish in the top 10 (prize contenders) of the Kaggle Kaggriculture competition.
Entry deadline 2026-09-23, final submission deadline 2026-09-30, both 23:59 UTC.

## Environment
- Python 3.12 via uv, matching Kaggle's runner image. Run everything with `uv run ...`; never the global Python.
- `uv sync` after any change to `pyproject.toml`.

## Journaling (mandatory, every session, written as the work happens)
- `journal.md`: one `## YYYY-MM-DD` section per day, chronological, newest at the bottom. Entry types:
  **Milestone**, **Checkpoint** (with numbers), **Decision** (with the why, especially when not obvious),
  **Surprise**, **Note**.
- `problems_encountered.md`: same date sectioning. Every problem goes here with: Symptom, Cause, Fix,
  Caught by (me / verifier / Iminabo). When someone else caught it, add "Why I missed it" and what
  changes so it does not recur.

## Evaluation rules
- The ladder scores wins, losses, and ties only. Judge every change by paired-seat win rate on fixed
  seeds against strong opponents (`scripts/arena.py`), never by mean bank against `starter`.
- Both seats, same seeds, previous best kept as a veto opponent.
- The engine draws each day's shop from the stream that spawns weeds (one draw per empty tile
  on both farms), so `scripts/eval.sh` runs the arena with `--decouple-shops`; judge
  production by the arena's harvest basket as well as the bank (journal 2026-09-16, P22).
- The engine (`kaggle_environments/envs/kaggriculture/kaggriculture.py` in the venv) is the source of
  truth over the docs in `data/`.

## Submission
- `main.py` at repo root. kaggle-environments execs it into an empty namespace (no `__file__`) and uses
  the LAST callable bound there as the agent, so `agent` must be the final definition.
- `uv run python scripts/package.py` builds and verifies `submission.tar.gz`.

## Git
- Commit as the repo's configured user only. No AI attribution in commits, PRs, or tags.
