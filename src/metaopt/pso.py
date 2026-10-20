"""Canonical PSO from Chapter 1 and Appendix B.

Boundary policy: zero the velocity component that left the box, then clip
the coordinate (``Bounds.zero_velocity_and_clip``). Coefficients default to
the handbook values ``w=0.72``, ``c1=c2=1.19``.

Random numbers come from the injected ``numpy.random.Generator``. The
manuscript draws them with ``np.random.rand`` after ``np.random.seed``. Those
two streams are not the same, so a shared integer seed does not reproduce
the handbook's particle trajectories. See ``docs/reproducibility.md``.
"""

from __future__ import annotations

import numpy as np

from metaopt._search import (
    evaluate_rows,
    make_result,
    notify,
    personal_best_update,
    require_bounds,
    resolve_generations,
    resolve_rng,
)
from metaopt.api import OptimizationResult


def minimize(
    objective,
    bounds,
    *,
    rng: np.random.Generator | None = None,
    seed: int | None = None,
    population_size: int = 25,
    iterations: int | None = None,
    max_evaluations: int | None = None,
    w: float = 0.72,
    c1: float = 1.19,
    c2: float = 1.19,
    callback=None,
    violation=None,
) -> OptimizationResult:
    """Minimize ``objective`` with the handbook PSO update.

    The initial population is generation 1. Later generations use

    ``v = w v + c1 r1 (pbest - x) + c2 r2 (gbest - x)``, ``x = x + v``.

    ``iterations`` is the handbook iteration count. ``max_evaluations`` caps
    the number of objective calls. When both are set, the run stops at the
    first limit. One objective call is used per particle per generation.
    """

    box = require_bounds(bounds)
    generator, recorded_seed = resolve_rng(rng, seed)
    generations, limit = resolve_generations(population_size, iterations, max_evaluations)
    position = box.sample(generator, population_size)
    velocity = np.zeros_like(position)
    cost = evaluate_rows(objective, position)
    pbest = position.copy()
    pbest_cost = cost.copy()
    g = int(np.argmin(pbest_cost))
    gbest = pbest[g].copy()
    gbest_cost = float(pbest_cost[g])
    history = [gbest_cost]
    nfev = population_size
    notify(callback, 1, generations, gbest_cost)

    for step in range(2, generations + 1):
        r1 = generator.random(position.shape)
        r2 = generator.random(position.shape)
        velocity = w * velocity + c1 * r1 * (pbest - position) + c2 * r2 * (gbest - position)
        position = position + velocity
        position, velocity = box.zero_velocity_and_clip(position, velocity)
        cost = evaluate_rows(objective, position)
        nfev += population_size
        pbest, pbest_cost = personal_best_update(position, cost, pbest, pbest_cost)
        g = int(np.argmin(pbest_cost))
        if pbest_cost[g] < gbest_cost:
            gbest_cost = float(pbest_cost[g])
            gbest = pbest[g].copy()
        history.append(gbest_cost)
        notify(callback, step, generations, gbest_cost)

    violation_value = None if violation is None else float(violation(gbest))
    return make_result(
        x=gbest,
        fun=gbest_cost,
        nfev=nfev,
        history=history,
        seed=recorded_seed,
        algorithm="PSO",
        population_size=population_size,
        max_evaluations=limit,
        generations=generations,
        requested_iterations=iterations,
        violation=violation_value,
    )
