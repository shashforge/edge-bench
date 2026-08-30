"""Medians and spreads. There is deliberately no mean() in this file;
one thermal throttle event ruins a mean and merely dents a median."""
from __future__ import annotations


def median(xs: list[float]) -> float:
    if not xs:
        raise ValueError("median of nothing")
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2


def percentile(xs: list[float], p: float) -> float:
    """Nearest-rank percentile, 0 < p <= 100."""
    if not xs:
        raise ValueError("percentile of nothing")
    s = sorted(xs)
    import math
    rank = max(1, math.ceil(p / 100 * len(s)))
    return s[rank - 1]


def iqr(xs: list[float]) -> float:
    return percentile(xs, 75) - percentile(xs, 25)
