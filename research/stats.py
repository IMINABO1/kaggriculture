"""Rank statistics for comparing two small groups of teams without extra dependencies."""

from __future__ import annotations

import math


def mann_whitney(a: list[float], b: list[float]) -> tuple[float, float]:
    """(AUC, two-sided p) for "a random a exceeds a random b", normal approximation with ties.

    AUC is U / (len(a) * len(b)): 0.5 means the groups overlap completely, 1.0 means every
    value in a is above every value in b. The p-value uses the tie-corrected normal
    approximation, which is adequate for groups of ten or more.
    """
    a = [float(x) for x in a if not math.isnan(x)]
    b = [float(x) for x in b if not math.isnan(x)]
    n1, n2 = len(a), len(b)
    if n1 == 0 or n2 == 0:
        return math.nan, math.nan
    pooled = sorted((v, 0) for v in a) + sorted((v, 1) for v in b)
    pooled.sort(key=lambda t: t[0])
    ranks = [0.0] * len(pooled)
    i = 0
    tie_term = 0.0
    while i < len(pooled):
        j = i
        while j + 1 < len(pooled) and pooled[j + 1][0] == pooled[i][0]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = avg
        t = j - i + 1
        if t > 1:
            tie_term += t**3 - t
        i = j + 1
    r1 = sum(r for r, (_, g) in zip(ranks, pooled) if g == 0)
    u1 = r1 - n1 * (n1 + 1) / 2
    auc = u1 / (n1 * n2)
    n = n1 + n2
    mu = n1 * n2 / 2
    var = n1 * n2 / 12 * ((n + 1) - tie_term / (n * (n - 1)))
    if var <= 0:
        return auc, 1.0
    z = (u1 - mu) / math.sqrt(var)
    p = math.erfc(abs(z) / math.sqrt(2))
    return auc, p
