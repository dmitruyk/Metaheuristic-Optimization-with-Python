"""Exterior penalty helpers used by the handbook's constrained examples.

The Chapter 6 construction adds a large weight times a nonnegative violation
to the original criterion. A small penalized objective does not certify
feasibility: positive proportional penalties can be arbitrarily small.
Check the individual violations returned by the application modules.
"""

from __future__ import annotations

import numpy as np


def hinge(value: float) -> float:
    """``max(0, value)`` for a finite ``g(x) <= 0`` inequality residual."""

    if not np.isfinite(value):
        raise ValueError("constraint residual must be finite")
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


def feasible_from_penalty(
    total: float,
    weight: float,
    criterion_upper: float,
    *,
    violations: list[float] | None = None,
    tolerance: float = 0.0,
) -> bool:
    """Check explicit nonnegative component violations against a tolerance.

    ``total``, ``weight`` and ``criterion_upper`` remain accepted for source
    compatibility but cannot certify feasibility. Calls without ``violations``
    now raise ValueError instead of making the unsafe former threshold inference.
    Supply every constraint's violation (e.g. from ``hinge``/``equality_band``).
    Nonfinite or negative components and invalid tolerances are rejected.
    """

    del total, criterion_upper
    if not np.isfinite(weight) or weight <= 0:
        raise ValueError("weight must be positive")
    if violations is None:
        raise ValueError("penalty totals cannot certify feasibility; supply component violations")
    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    components = np.asarray(violations, dtype=float)
    if components.ndim != 1 or not np.all(np.isfinite(components)) or np.any(components < 0):
        raise ValueError("violations must be a one-dimensional sequence of finite nonnegative values")
    return bool(np.all(components <= tolerance))
