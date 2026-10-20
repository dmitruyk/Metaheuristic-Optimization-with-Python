"""Shared evaluation, seeding, and generation-budget helpers."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from metaopt.api import Bounds, OptimizationResult

Objective = Callable[[np.ndarray], float]


def resolve_rng(rng: np.random.Generator | None, seed: int | None) -> tuple[np.random.Generator, int | None]:
    if rng is not None and seed is not None:
        raise ValueError("pass either rng or seed, not both")
    if rng is None:
        return np.random.default_rng(seed), seed
    if not isinstance(rng, np.random.Generator):
        raise TypeError("rng must be a numpy.random.Generator from np.random.default_rng")
    return rng, None


def resolve_generations(
    population_size: int,
    iterations: int | None,
    max_evaluations: int | None,
    *,
    cost_per_generation: int | None = None,
) -> tuple[int, int]:
    """Return ``(generations, evaluation_limit)`` for a constant per-generation cost.

    A generation is one pass over the population, matching the handbook's
    iteration count: the initial sample is generation 1, and the loop runs
    through ``iterations``. The limit stops the run on a generation boundary
    so ``nfev`` is ``generations * cost_per_generation``.
    """

    if population_size < 1:
        raise ValueError("population_size must be >= 1")
    if iterations is None and max_evaluations is None:
        raise ValueError("pass iterations or max_evaluations")
    if iterations is not None and iterations < 1:
        raise ValueError("iterations must be >= 1")
    if max_evaluations is not None and max_evaluations < 1:
        raise ValueError("max_evaluations must be >= 1")
    cost = population_size if cost_per_generation is None else cost_per_generation
    if cost < 1:
        raise ValueError("cost_per_generation must be >= 1")
    generations = iterations
    if max_evaluations is not None:
        affordable = max_evaluations // cost
        generations = affordable if generations is None else min(generations, affordable)
    if generations is None or generations < 1:
        raise ValueError(f"the evaluation budget cannot pay for the initial population ({cost} evaluations)")
    return int(generations), int(generations * cost)


def evaluate(objective: Objective, x: np.ndarray) -> float:
    """Call ``objective`` and map non-finite results to ``+inf`` for minimization."""

    value = objective(np.asarray(x, dtype=float))
    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError("objective must return a real scalar") from exc
    if not np.isfinite(value):
        return float(np.inf)
    return value


def evaluate_rows(objective: Objective, population: np.ndarray) -> np.ndarray:
    costs = np.empty(population.shape[0], dtype=float)
    for index, row in enumerate(population):
        costs[index] = evaluate(objective, row)
    return costs


def personal_best_update(
    position: np.ndarray,
    cost: np.ndarray,
    pbest: np.ndarray,
    pbest_cost: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    improved = cost < pbest_cost
    pbest = np.array(pbest, copy=True)
    pbest_cost = np.array(pbest_cost, copy=True)
    pbest[improved] = position[improved]
    pbest_cost[improved] = cost[improved]
    return pbest, pbest_cost


def notify(callback, step: int, iterations: int, best: float) -> None:
    if callback is not None:
        callback({"step": step, "iterations": iterations, "best": float(best)})


def make_result(
    *,
    x: np.ndarray,
    fun: float,
    nfev: int,
    history: list[float],
    seed: int | None,
    algorithm: str,
    population_size: int,
    max_evaluations: int,
    generations: int,
    requested_iterations: int | None,
    violation: float | None = None,
    message: str | None = None,
) -> OptimizationResult:
    finite = np.isfinite(fun)
    feasible = None if violation is None else bool(violation <= 0.0)
    success = bool(finite) and (feasible is not False)
    if message is None:
        if not finite:
            message = "every evaluated objective value was NaN or infinite"
        elif requested_iterations is not None and generations < requested_iterations:
            message = f"stopped after {generations} generations because the objective-evaluation budget was exhausted"
        else:
            message = f"completed {generations} generations"
    return OptimizationResult(
        x=np.asarray(x, dtype=float),
        fun=float(fun) if finite else float("inf"),
        nfev=int(nfev),
        history=history,
        seed=seed,
        success=success,
        message=message,
        feasible=feasible,
        constraint_violation=None if violation is None else float(violation),
        algorithm=algorithm,
        population_size=int(population_size),
        max_evaluations=int(max_evaluations),
    )


def require_bounds(bounds) -> Bounds:
    if isinstance(bounds, Bounds):
        return bounds
    return Bounds.from_pairs(bounds)
