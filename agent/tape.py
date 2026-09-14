"""Replay a recorded action stream. Turns any public game into a local opponent."""

from __future__ import annotations

PASS = {"farmer": ["PASS"], "hands": [], "market": []}


class Tape:
    """Callable agent that returns the recorded action for the current step, PASS after the end."""

    def __init__(self, actions):
        self.actions = list(actions)

    def __call__(self, obs, config=None):
        step = obs["step"]
        return self.actions[step] if step < len(self.actions) else PASS


def actions_from_replay(replay: dict, seat: int) -> list[dict]:
    """The action stream a seat submitted: steps[t].action is what it did at obs.step == t-1."""
    return [step[seat].get("action") or PASS for step in replay["steps"][1:]]
