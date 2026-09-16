#!/usr/bin/env bash
# Two yardsticks for the runtime agent: production (against pass, no competing sales) and
# competition (paired seats against the public line v5). Both sides are deterministic, but the
# engine draws each day's shop from the stream that spawns weeds, one draw per empty tile on
# both farms, so a change that alters our empty-tile count also changes the shop sequence of
# that seed (P22). Both runs therefore draw the shops from the seed alone (--decouple-shops),
# which makes every rerun a true A/B; the ladder itself keeps the coupled draw.
cd "$(dirname "$0")/.."
F='^(OpenSpiel|[a-z_0-9]+$|Available games)'
echo "production vs pass (seeds 1-8, seat 0):"
uv run python scripts/arena.py --a main.py --b pass --seeds 1-8 --one-seat --decouple-shops --jobs 3 2>&1 | grep -v -E "$F" | tail -2
echo "competition vs line:v5 (seeds 0-9, both seats):"
uv run python scripts/arena.py --a main.py --b line:v5 --seeds 0-9 --decouple-shops --jobs 3 2>&1 | grep -v -E "$F" | tail -2
