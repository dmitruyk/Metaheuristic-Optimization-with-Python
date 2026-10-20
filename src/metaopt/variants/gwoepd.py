"""GWO with elimination of the poorest wolves (GWOEPD / ``EPDGWO``).

After the ordinary GWO move, the worst half of the pack is replaced. With
``u ~ Uniform(0, 1)`` the manuscript sets

``sel = min(int(u / 0.25), 3)``.

``sel`` of 0, 1, or 2 builds a point from alpha, beta, or delta plus or minus
a uniform vector drawn from the whole box. ``sel`` of 3 draws a fresh uniform
point in the box. Replaced wolves are re-evaluated; the others keep the cost
from the GWO move. Boundary policy: clip to the box.

The leaders used in the replacement are the wolves that were alpha, beta, and
delta *before* the GWO move, as in the Appendix B listing.
"""

from __future__ import annotations

import numpy as np

from metaopt._search import (
    evaluate_rows,
    make_result,
    notify,
    require_bounds,
    resolve_rng,
)
from metaopt.gwo import _gwo_update, linear_a


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
):
    if population_size < 3:
        raise ValueError("GWOEPD needs at least 3 wolves")
    if iterations is None and max_evaluations is None:
        raise ValueError("pass iterations or max_evaluations")
    if iterations is not None and iterations < 1:
        raise ValueError("iterations must be >= 1")
    box = require_bounds(bounds)
    generator, recorded_seed = resolve_rng(rng, seed)
    half = population_size // 2
    # Generation 1 costs population_size. Each later generation costs
    # population_size + half.
    if iterations is None:
        remaining = max_evaluations - population_size
        later = 0 if remaining < population_size + half else remaining // (population_size + half)
        generations = 1 + later
        schedule_length = generations
    else:
        generations = iterations
        schedule_length = iterations
        if max_evaluations is not None:
            affordable_later = 0
            remaining = max_evaluations - population_size
            if remaining >= 0 and half >= 0:
                cost = population_size + half
                affordable_later = remaining // cost if cost else 0
            generations = 1 + min(iterations - 1, affordable_later)
    if generations < 1 or (max_evaluations is not None and max_evaluations < population_size):
        raise ValueError("the evaluation budget cannot pay for the initial pack")

    pack = box.sample(generator, population_size)
    costs = evaluate_rows(objective, pack)
    nfev = population_size
    best_index = int(np.argmin(costs))
    best = pack[best_index].copy()
    best_cost = float(costs[best_index])
    history = [best_cost]
    notify(callback, 1, generations, best_cost)

    for step in range(2, generations + 1):
        order = np.argsort(costs)
        x_alpha = pack[order[0]].copy()
        x_beta = pack[order[1]].copy()
        x_delta = pack[order[2]].copy()
        a_coeff = linear_a(step, schedule_length)
        pack = _gwo_update(pack, x_alpha, x_beta, x_delta, a_coeff, box, generator)
        costs = evaluate_rows(objective, pack)
        nfev += population_size
        if half > 0:
            worst = np.argsort(costs)[-half:]
            leaders = np.stack([x_alpha, x_beta, x_delta])
            sel = np.minimum((generator.random(half) / 0.25).astype(int), 3)
            sign = generator.choice(np.array([-1.0, 1.0]), size=(half, 1))
            uniform_box = box.sample(generator, half)
            from_leader = leaders[np.minimum(sel, 2)] + sign * uniform_box
            from_random = box.sample(generator, half)
            replacement = np.where((sel == 3)[:, None], from_random, from_leader)
            pack[worst] = box.clip(replacement)
            replaced_costs = evaluate_rows(objective, pack[worst])
            costs[worst] = replaced_costs
            nfev += half
        challenger = int(np.argmin(costs))
        if costs[challenger] < best_cost:
            best_cost = float(costs[challenger])
            best = pack[challenger].copy()
        history.append(best_cost)
        notify(callback, step, generations, best_cost)

    violation_value = None if violation is None else float(violation(best))
    limit = nfev if max_evaluations is None else max_evaluations
    return make_result(
        x=best,
        fun=best_cost,
        nfev=nfev,
        history=history,
        seed=recorded_seed,
        algorithm="GWOEPD",
        population_size=population_size,
        max_evaluations=limit,
        generations=generations,
        requested_iterations=iterations,
        violation=violation_value,
    )
