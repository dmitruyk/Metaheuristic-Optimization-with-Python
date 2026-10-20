"""Common optimization types used by every algorithm in this companion.

Boundary policies are algorithm-specific and documented on each minimizer.
``Bounds.zero_velocity_and_clip`` is the PSO policy from Chapter 1:
a coordinate that leaves the box has its velocity set to zero and is then
projected onto the nearest bound.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class Bounds:
    """Box constraints, one ``[lower, upper]`` pair per variable."""

    lower: np.ndarray
    upper: np.ndarray

    def __post_init__(self) -> None:
        lower = np.asarray(self.lower, dtype=float).reshape(-1)
        upper = np.asarray(self.upper, dtype=float).reshape(-1)
        if lower.shape != upper.shape:
            raise ValueError("lower and upper bounds must have the same length")
        if lower.size == 0:
            raise ValueError("at least one variable is required")
        if not np.all(np.isfinite(lower)) or not np.all(np.isfinite(upper)):
            raise ValueError("bounds must be finite")
        if np.any(upper < lower):
            raise ValueError("each upper bound must be greater than or equal to the lower bound")
        object.__setattr__(self, "lower", lower)
        object.__setattr__(self, "upper", upper)

    @classmethod
    def from_pairs(cls, pairs: list | np.ndarray) -> Bounds:
        array = np.asarray(pairs, dtype=float)
        if array.ndim != 2 or array.shape[1] != 2:
            raise ValueError("bounds must have shape (n_variables, 2)")
        return cls(array[:, 0], array[:, 1])

    @property
    def dimension(self) -> int:
        return int(self.lower.size)

    def sample(self, rng: np.random.Generator, rows: int) -> np.ndarray:
        if rows < 1:
            raise ValueError("rows must be >= 1")
        unit = rng.random((rows, self.dimension))
        return self.lower + unit * (self.upper - self.lower)

    def clip(self, position: np.ndarray) -> np.ndarray:
        return np.clip(np.asarray(position, dtype=float), self.lower, self.upper)

    def zero_velocity_and_clip(self, position: np.ndarray, velocity: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Manuscript PSO boundary rule: zero the outgoing velocity, then clip."""

        position = np.asarray(position, dtype=float).copy()
        velocity = np.asarray(velocity, dtype=float).copy()
        outside = (position < self.lower) | (position > self.upper)
        velocity[outside] = 0.0
        np.clip(position, self.lower, self.upper, out=position)
        return position, velocity


@dataclass
class Problem:
    """An objective, its box, and an optional violation measure.

    ``violation(x)`` should return a nonnegative number that is zero if and
    only if ``x`` is feasible. Engineering examples in this repository fold
    penalties into ``objective``; ``violation`` is optional extra reporting.
    """

    objective: object
    bounds: Bounds
    violation: object | None = None
    name: str = ""

    def evaluate(self, x: np.ndarray) -> float:
        return float(self.objective(np.asarray(x, dtype=float)))


@dataclass
class OptimizationResult:
    """Minimization result.

    ``history`` is the best-so-far objective value after each completed
    generation, including the initial population. ``nfev`` counts objective
    calls. ``seed`` is the integer passed to ``numpy.random.default_rng``
    when the caller supplied one; it is ``None`` when a ready-made generator
    was injected.
    """

    x: np.ndarray
    fun: float
    nfev: int
    history: list[float]
    seed: int | None
    success: bool
    message: str
    feasible: bool | None = None
    constraint_violation: float | None = None
    algorithm: str = ""
    population_size: int = 0
    max_evaluations: int = 0
    extras: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.x = np.asarray(self.x, dtype=float).copy()
        self.history = [float(value) for value in self.history]
