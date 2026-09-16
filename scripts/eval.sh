#!/usr/bin/env bash
# Two yardsticks for the runtime agent: production (against pass, no competing sales) and
# competition (paired seats against the public line v5). Both sides are deterministic, so
# any change in these lines is the code change.
cd "$(dirname "$0")/.."
F='^(OpenSpiel|[a-z_0-9]+$|Available games)'
echo "production vs pass (seeds 1,2,4, seat 0):"
uv run python scripts/arena.py --a main.py --b pass --seeds 1,2,4 --one-seat --jobs 3 2>&1 | grep -v -E "$F" | tail -1
echo "competition vs line:v5 (seeds 0,1,2,4,5, both seats):"
uv run python scripts/arena.py --a main.py --b line:v5 --seeds 0,1,2,4,5 --jobs 3 2>&1 | grep -v -E "$F" | tail -1
