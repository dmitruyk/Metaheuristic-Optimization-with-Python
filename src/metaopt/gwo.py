"""Grey Wolf Optimizer from Chapter 3 and Appendix B.

Boundary policy: the averaged wolf position is clipped to the box. There is
no velocity. The coefficient ``a`` follows the handbook schedule evaluated at
the loop index ``step``, which starts at 2 because generation 1 is the
initial sample:

``a = 2 - 2 * (step / iterations)`` for GWO.

``mGWO`` uses ``a = 2 - 2 * (step / iterations) ** 2``.
"""

from __future__ import annotations

import numpy as np

from metaopt._search import (
    evaluate_rows,
    make_result,
    notify,
    require_bounds,
    resolve_generations,
    resolve_rng,
)
from metaopt.api import OptimizationResult


def _gwo_update(pack, x_alpha, x_beta, x_delta, a, bounds, rng):
    rows, dimension = pack.shape
    updated = np.zeros_like(pack)
    for leader in (x_alpha, x_beta, x_delta):
        c_coeff = 2 * rng.random((rows, dimension))
        a_coeff = 2 * a * rng.random((rows, dimension)) - a
        distance = np.abs(c_coeff * leader - pack)
        updated += leader - a_coeff * distance
    return bounds.clip(updated / 3.0)


def _gwo_minimize(
    objective,
    bounds,
    *,
    rng,
    seed,
    population_size,
    iterations,
    max_evaluations,
    a_rule,
    algorithm,
    callback,
    violation,
) -> OptimizationResult:
    if population_size < 3:
        raise ValueError(f"{algorithm} needs at least 3 wolves")
    box = require_bounds(bounds)
    generator, recorded_seed = resolve_rng(rng, seed)
    generations, limit = resolve_generations(population_size, iterations, max_evaluations)
    # The manuscript divides by the configured iteration horizon, not by a
    # budget-truncated length. When the caller sets only max_evaluations,
    # that horizon is the number of generations the budget can pay for.
    schedule_length = generations if iterations is None else iterations
    pack = box.sample(generator, population_size)
    costs = evaluate_rows(objective, pack)
    nfev = population_size
    order = np.argsort(costs)
    best = pack[order[0]].copy()
    best_cost = float(costs[order[0]])
    history = [best_cost]
    notify(callback, 1, generations, best_cost)

    for step in range(2, generations + 1):
        a_coeff = float(a_rule(step, schedule_length))
        order = np.argsort(costs)
        x_alpha = pack[order[0]].copy()
        x_beta = pack[order[1]].copy()
        x_delta = pack[order[2]].copy()
        pack = _gwo_update(pack, x_alpha, x_beta, x_delta, a_coeff, box, generator)
        costs = evaluate_rows(objective, pack)
        nfev += population_size
        challenger = int(np.argmin(costs))
        if costs[challenger] < best_cost:
            best_cost = float(costs[challenger])
            best = pack[challenger].copy()
        history.append(best_cost)
        notify(callback, step, generations, best_cost)

    violation_value = None if violation is None else float(violation(best))
    return make_result(
        x=best,
        fun=best_cost,
        nfev=nfev,
        history=history,
        seed=recorded_seed,
        algorithm=algorithm,
        population_size=population_size,
        max_evaluations=limit,
        generations=generations,
        requested_iterations=iterations,
        violation=violation_value,
    )


def linear_a(step: int, iterations: int) -> float:
    """Handbook GWO schedule. ``step`` uses the manuscript's 1-based index."""

    return 2.0 - 2.0 * (step / iterations)


def nonlinear_a(step: int, iterations: int) -> float:
    """Handbook mGWO schedule ``a = 2 - 2 (step / iterations)^2``."""

    return 2.0 - 2.0 * (step / iterations) ** 2


def minimize(
    objective,
    bounds,
    *,
    rng: np.random.Generator | None = None,
    seed: int | None = None,
    population_size: int = 25,
    iterations: int | None = None,
    max_evaluations: int | None = None,
    callback=None,
    violation=None,
) -> OptimizationResult:
    """Standard GWO, handbook function ``GWO``."""

    return _gwo_minimize(
        objective,
        bounds,
        rng=rng,
        seed=seed,
        population_size=population_size,
        iterations=iterations,
        max_evaluations=max_evaluations,
        a_rule=linear_a,
        algorithm="GWO",
        callback=callback,
        violation=violation,
    )
