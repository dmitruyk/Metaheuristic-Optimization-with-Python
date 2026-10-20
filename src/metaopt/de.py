"""Differential evolution from Chapter 2 and Appendix B.

``minimize`` is DE/rand/1/bin, the handbook function ``DERand``.
``minimize_best`` is DE/best/1/bin, the handbook function ``DEBest``.
Both use ``CR=0.5`` and ``F=0.6`` unless overridden.

Boundary policy: the donor vector is clipped to the box before binomial
crossover, which is the manuscript rule. Trial vectors are therefore feasible
with respect to the box. This is not the boundary rule used by
``scipy.optimize.differential_evolution``.

``scipy_minimize`` below is a separate baseline. It is not the manuscript DE.
"""

from __future__ import annotations

import numpy as np

from metaopt._search import (
    evaluate,
    evaluate_rows,
    make_result,
    notify,
    require_bounds,
    resolve_generations,
    resolve_rng,
)
from metaopt.api import OptimizationResult


def _de_loop(
    objective,
    bounds,
    *,
    rng,
    seed,
    population_size,
    iterations,
    max_evaluations,
    mutation,
    cr,
    f_scale,
    algorithm,
    callback,
    violation,
    adapt=None,
) -> OptimizationResult:
    if population_size < 4:
        raise ValueError(f"{algorithm} needs at least 4 individuals")
    box = require_bounds(bounds)
    generator, recorded_seed = resolve_rng(rng, seed)
    generations, limit = resolve_generations(population_size, iterations, max_evaluations)
    population = box.sample(generator, population_size)
    costs = evaluate_rows(objective, population)
    nfev = population_size
    best_index = int(np.argmin(costs))
    best_cost = float(costs[best_index])
    history = [best_cost]
    notify(callback, 1, generations, best_cost)
    cr_value = float(cr)
    f_value = float(f_scale)

    for step in range(2, generations + 1):
        for index in range(population_size):
            if adapt is not None:
                cr_value, f_value = adapt(generator, cr_value, f_value)
            donor = mutation(population, costs, index, best_index, f_value, generator, box)
            donor = box.clip(donor)
            j_rand = int(generator.integers(0, box.dimension))
            mask = generator.random(box.dimension) <= cr_value
            mask[j_rand] = True
            trial = np.where(mask, donor, population[index])
            trial_cost = evaluate(objective, trial)
            nfev += 1
            if trial_cost < costs[index]:
                population[index] = trial
                costs[index] = trial_cost
        best_index = int(np.argmin(costs))
        best_cost = float(costs[best_index])
        history.append(best_cost)
        notify(callback, step, generations, best_cost)

    best = population[best_index].copy()
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


def _mutate_rand(population, costs, index, best_index, f_scale, generator, box):
    del costs, best_index, box
    candidates = [i for i in range(population.shape[0]) if i != index]
    i1, i2, i3 = generator.choice(candidates, size=3, replace=False)
    return population[i1] + f_scale * (population[i2] - population[i3])


def _mutate_best(population, costs, index, best_index, f_scale, generator, box):
    del costs, box
    candidates = [i for i in range(population.shape[0]) if i != index and i != best_index]
    if len(candidates) < 2:
        raise ValueError("DE/best/1/bin could not draw two distinct difference vectors")
    i2, i3 = generator.choice(candidates, size=2, replace=False)
    return population[best_index] + f_scale * (population[i2] - population[i3])


def minimize(
    objective,
    bounds,
    *,
    rng: np.random.Generator | None = None,
    seed: int | None = None,
    population_size: int = 25,
    iterations: int | None = None,
    max_evaluations: int | None = None,
    cr: float = 0.5,
    f: float = 0.6,
    callback=None,
    violation=None,
) -> OptimizationResult:
    """DE/rand/1/bin, handbook name ``DERand``."""

    return _de_loop(
        objective,
        bounds,
        rng=rng,
        seed=seed,
        population_size=population_size,
        iterations=iterations,
        max_evaluations=max_evaluations,
        mutation=_mutate_rand,
        cr=cr,
        f_scale=f,
        algorithm="DE/rand/1/bin",
        callback=callback,
        violation=violation,
    )


def minimize_best(
    objective,
    bounds,
    *,
    rng: np.random.Generator | None = None,
    seed: int | None = None,
    population_size: int = 25,
    iterations: int | None = None,
    max_evaluations: int | None = None,
    cr: float = 0.5,
    f: float = 0.6,
    callback=None,
    violation=None,
) -> OptimizationResult:
    """DE/best/1/bin, handbook name ``DEBest``."""

    return _de_loop(
        objective,
        bounds,
        rng=rng,
        seed=seed,
        population_size=population_size,
        iterations=iterations,
        max_evaluations=max_evaluations,
        mutation=_mutate_best,
        cr=cr,
        f_scale=f,
        algorithm="DE/best/1/bin",
        callback=callback,
        violation=violation,
    )


def scipy_minimize(
    objective,
    bounds,
    *,
    seed: int | None = None,
    rng: np.random.Generator | None = None,
    population_size: int = 25,
    max_evaluations: int | None = None,
    iterations: int | None = None,
) -> OptimizationResult:
    """SciPy's ``differential_evolution``, kept distinct from the handbook DE.

    SciPy samples, mutates, and handles bounds with its own implementation.
    A matching ``max_evaluations`` does not make the two histories comparable
    number-by-number; compare final values at an equal evaluation budget.
    """

    from scipy.optimize import differential_evolution

    if rng is not None and seed is not None:
        raise ValueError("pass either rng or seed, not both")
    box = require_bounds(bounds)
    if max_evaluations is None:
        if iterations is None:
            raise ValueError("pass iterations or max_evaluations")
        max_evaluations = population_size * iterations
    # SciPy 1.17 takes maxiter, not maxfun. Its population is popsize * dimension,
    # so the requested population is rounded down to a multiple of the dimension
    # (and at least one multiple). maxiter is chosen so the initial sample plus
    # later generations stay near the requested evaluation budget. The realized
    # nfev can still differ by a generation.
    multiplier = max(1, population_size // box.dimension)
    actual_population = multiplier * box.dimension
    maxiter = max(1, max_evaluations // actual_population)
    kwargs = {
        "bounds": list(zip(box.lower.tolist(), box.upper.tolist(), strict=True)),
        "popsize": multiplier,
        "maxiter": maxiter,
        "polish": False,
        "atol": 0.0,
        "tol": 0.0,
    }
    if rng is not None:
        kwargs["rng"] = rng
    else:
        kwargs["seed"] = seed
    result = differential_evolution(objective, **kwargs)
    history = [float(result.fun)]
    return OptimizationResult(
        x=np.asarray(result.x, dtype=float),
        fun=float(result.fun),
        nfev=int(result.nfev),
        history=history,
        seed=seed,
        success=bool(result.success) and np.isfinite(result.fun),
        message="scipy.optimize.differential_evolution (not the handbook DE): " + str(result.message),
        algorithm="scipy.optimize.differential_evolution",
        population_size=population_size,
        max_evaluations=int(max_evaluations),
    )
