"""Shared generation loop for PSO variants.

Each variant supplies ``propose``, which returns the new position and velocity
before the handbook boundary rule is applied. The personal-best and
global-best bookkeeping matches Chapter 1.
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


def run_particle_swarm(
    objective,
    bounds,
    *,
    rng,
    seed,
    population_size,
    iterations,
    max_evaluations,
    algorithm,
    propose,
    callback,
    violation,
    minimum_population=1,
):
    if population_size < minimum_population:
        raise ValueError(f"{algorithm} needs at least {minimum_population} particles")
    box = require_bounds(bounds)
    generator, recorded_seed = resolve_rng(rng, seed)
    generations, limit = resolve_generations(population_size, iterations, max_evaluations)
    schedule_length = generations if iterations is None else iterations
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
    state = {
        "position": position,
        "velocity": velocity,
        "pbest": pbest,
        "pbest_cost": pbest_cost,
        "gbest": gbest,
        "gbest_cost": gbest_cost,
        "schedule_length": schedule_length,
    }
    notify(callback, 1, generations, gbest_cost)

    for step in range(2, generations + 1):
        position, velocity = propose(state, step, generator, box)
        position, velocity = box.zero_velocity_and_clip(position, velocity)
        cost = evaluate_rows(objective, position)
        nfev += population_size
        pbest, pbest_cost = personal_best_update(position, cost, state["pbest"], state["pbest_cost"])
        g = int(np.argmin(pbest_cost))
        gbest = state["gbest"]
        gbest_cost = state["gbest_cost"]
        if pbest_cost[g] < gbest_cost:
            gbest_cost = float(pbest_cost[g])
            gbest = pbest[g].copy()
        state.update(
            position=position,
            velocity=velocity,
            pbest=pbest,
            pbest_cost=pbest_cost,
            gbest=gbest,
            gbest_cost=gbest_cost,
            local_index=g,
        )
        history.append(gbest_cost)
        notify(callback, step, generations, gbest_cost)

    violation_value = None if violation is None else float(violation(state["gbest"]))
    return make_result(
        x=state["gbest"],
        fun=state["gbest_cost"],
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
