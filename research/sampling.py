"""The window rule for a team's chronological game history.

With N games: everything if N <= 250; otherwise the first 50 (F), 50 centred at each quarter
point (Q1, Q2, Q3), and the last 50 (L). Windows may overlap for N just above 250; a game then
appears once per window it belongs to.
"""

from __future__ import annotations

WINDOW = 50
TAKE_ALL_BELOW = 250


def windows(n: int) -> dict[str, list[int]]:
    """Map window name -> list of 0-based positions in the chronological history."""
    if n <= TAKE_ALL_BELOW:
        return {"ALL": list(range(n))}
    half = WINDOW // 2
    out = {"F": list(range(WINDOW))}
    for name, frac in (("Q1", 0.25), ("Q2", 0.5), ("Q3", 0.75)):
        centre = int(round(n * frac))
        start = min(max(centre - half, 0), n - WINDOW)
        out[name] = list(range(start, start + WINDOW))
    out["L"] = list(range(n - WINDOW, n))
    return out


def current_sub_windows(n: int) -> dict[str, list[int]]:
    """First 50 games of the current submission (its ladder-entry phase)."""
    return {"C0": list(range(min(n, WINDOW)))}
