"""Exterior penalty helpers used by the handbook's constrained examples.

The Chapter 6 construction adds a large weight times a nonnegative violation
to the original criterion. A reported objective below the weight means every
penalty that uses that weight is zero. Callers that need a sharper statement
should use the component dictionaries returned by the application modules.
"""

from __future__ import annotations

import numpy as np


def hinge(value: float) -> float:
    """``max(0, value)`` for a ``g(x) <= 0`` inequality."""

    return float(max(0.0, value))


def equality_band(residual: float, tolerance: float) -> float:
    """Zero inside ``[-tolerance, tolerance]``, otherwise the absolute residual."""

    residual = float(residual)
    if abs(residual) <= tolerance:
        return 0.0
    return abs(residual)


def weighted_sum(violations: list[float], weight: float) -> float:
    if weight < 0:
        raise ValueError("penalty weight must be nonnegative")
    return float(weight * np.sum(np.maximum(0.0, np.asarray(violations, dtype=float))))


def feasible_from_penalty(total: float, weight: float, criterion_upper: float) -> bool:
    """True when ``total`` cannot contain a positive penalty of size ``weight``.

    Valid only when the raw criterion is known to be strictly below ``weight``
    and at least ``-criterion_upper`` is not required. Prefer component-wise
    checks when they are available.
    """

    if weight <= 0:
        raise ValueError("weight must be positive")
    return float(total) < weight - criterion_upper
