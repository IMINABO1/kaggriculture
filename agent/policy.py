"""The runtime agent: the public line's plan, executed from the observation every turn."""

from __future__ import annotations

from agent.executor import act_units
from agent.market import market_orders

TURNS_PER_DAY = 24
_GAMES: dict = {}


def act(obs):
    step = int(obs.get("step", 0))
    player = int(obs.get("player", 0))
    state = _GAMES.get(player)
    if state is None or step <= state.get("last_step", -1):
        state = _GAMES[player] = {"last_step": -1, "day": -1, "feeders": set()}
    state["last_step"] = step
    day, hour = step // TURNS_PER_DAY, step % TURNS_PER_DAY
    units, summary = act_units(obs, day, hour, state, step)
    return {
        "farmer": units[0],
        "hands": units[1:],
        "market": market_orders(obs, day, hour, summary, state),
    }
