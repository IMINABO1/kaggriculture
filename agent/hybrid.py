"""The public line's tape for the opening, our runtime agent for the rest of the game."""

from __future__ import annotations

import os

from agent import plan as P
from agent.policy import act as runtime_act

TURNS_PER_DAY = 24
_TAPE = None


def tape():
    """The bundled v41 agent, loaded the way kaggle-environments loads a main.py."""
    global _TAPE
    if _TAPE is None:
        from kaggle_environments.agent import get_last_callable

        # KAGG_TAPE points an arena run at another public build without repackaging
        path = os.environ.get("KAGG_TAPE") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "line_v41.py")
        with open(path, encoding="utf-8") as fh:
            _TAPE = get_last_callable(fh.read(), path=path)
    return _TAPE


def act(obs, config=None):
    if int(obs.get("step", 0)) < P.TAPE_DAYS * TURNS_PER_DAY:
        return tape()(obs, config)
    return runtime_act(obs)
