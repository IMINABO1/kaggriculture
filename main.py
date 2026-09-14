"""Kaggriculture submission entrypoint.

kaggle-environments execs this file into an EMPTY namespace (no ``__file__``), appends the
file's directory to sys.path only for the duration of that exec, and then uses the LAST
callable bound in the namespace as the agent. Therefore: do all imports at the top, and keep
``agent`` as the final definition in this file.
"""

import os
import sys

for _path in ("/kaggle_simulations/agent", os.getcwd()):
    if os.path.isdir(_path) and _path not in sys.path:
        sys.path.insert(0, _path)

from agent.policy import act

FALLBACK = {"farmer": ["PASS"], "hands": [], "market": []}


def agent(obs, config=None):
    try:
        return act(obs)
    except Exception as exc:  # noqa: BLE001 - an erroring agent forfeits every game
        print(f"[agent] fallback at step {obs.get('step')}: {exc!r}", file=sys.stderr)
        return FALLBACK
