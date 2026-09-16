#!/usr/bin/env bash
# Two yardsticks for the runtime agent: production (against pass, no competing sales) and
# competition (paired seats against the public line v5). Both sides are deterministic, but the
# engine draws each day's shop from the stream that spawns weeds, one draw per empty tile on
# both farms, so a change that alters our empty-tile count also changes the shop sequence of
# that seed (journal 2026-09-16). Enough seeds make the draw noise; read the mean, not one seed.
cd "$(dirname "$0")/.."
F='^(OpenSpiel|[a-z_0-9]+$|Available games)'
echo "production vs pass (seeds 1-8, seat 0):"
uv run python scripts/arena.py --a main.py --b pass --seeds 1-8 --one-seat --jobs 3 2>&1 | grep -v -E "$F" | tail -1
echo "competition vs line:v5 (seeds 0-9, both seats):"
uv run python scripts/arena.py --a main.py --b line:v5 --seeds 0-9 --jobs 3 2>&1 | grep -v -E "$F" | tail -1
