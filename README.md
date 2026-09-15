# Kaggriculture

Agent, local arena, and research tooling for the Kaggle [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture) simulation competition. Goal: top 10.

## Setup

```bash
uv sync                       # Python 3.12 (matches Kaggle's runner image) + deps
uv run pytest -q              # smoke tests: loader contract, self-play validation, full season
```

## Daily loop

```bash
uv run python scripts/play.py --a main.py --b starter --seed 0 --replay      # one game + replay JSON
uv run python scripts/arena.py --a main.py --b starter --seeds 0-9 --jobs 4  # paired-seat win rate
uv run python scripts/package.py                                             # build + verify submission.tar.gz
kaggle competitions submit kaggriculture -f submission.tar.gz -m "..."
```

## Top-14 and next-15 study

How the prize contenders play, sampled across each team's history, and what separates them
from the next 15 teams of the gold zone. Method in `reports/top10/METHOD.md`, results in
`reports/top10/summary.md`, the group comparison in `reports/top10/groups.md`, one dossier
per team, recommendation in `reports/top10/decision_memo.md`.

## Layout

- `main.py` — submission entrypoint (`agent` must stay the last callable in the file)
- `agent/` — the policy
- `scripts/` — arena, single-game runner, packager
- `tests/` — smoke tests
- `data/` — competition kit docs (README.md, AGENTS.md); the engine is the source of truth
- `journal.md` — chronological milestones, surprises, decisions
- `problems_encountered.md` — every problem, its cause, fix, and who caught it
