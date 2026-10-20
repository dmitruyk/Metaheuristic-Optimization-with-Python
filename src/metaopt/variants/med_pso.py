"""Multi-epoch diversity PSO (ME-D-PSO), Section 1.4.5 and Appendix B.

Each epoch draws fresh inertia and acceleration coefficients

``w ~ Uniform(0, 1)``, ``c1, c2 ~ Uniform(0, 2)``

and stops early when the relative change of the best value is at most
``acceptable_rate`` and the value actually changed. The next epoch restarts
the swarm and inserts the incumbent best into one particle.

The manuscript indexes ``CostFunctionValues[-2]`` even when a restarted epoch
has only one recorded value, which raises ``IndexError``. This implementation
waits until two history values exist. That is the only intentional change
inside an epoch.

Chapter 1.4.5 illustrates ``acceptable_rate=0.01``. The Chapter 5 experiment
uses ``5e-3``. The default here is the experiment value.

Boundary policy: zero-velocity-and-clip.
"""

from __future__ import annotations

import numpy as np

from metaopt._search import (
    evaluate,
    evaluate_rows,
    make_result,
    notify,
    personal_best_update,
    require_bounds,
    resolve_rng,
)


def _epoch(objective, box, generator, population_size, iterations, acceptable_rate, history, incumbent, nfev, max_evaluations, callback):
    position = box.sample(generator, population_size)
    velocity = np.zeros_like(position)
    if nfev + population_size > max_evaluations:
        return None
    cost = evaluate_rows(objective, position)
    nfev += population_size
    pbest = position.copy()
    pbest_cost = cost.copy()
    g = int(np.argmin(pbest_cost))
    best_cost = float(pbest_cost[g])
    if incumbent is not None and len(incumbent) > 0:
        incumbent = np.asarray(incumbent, dtype=float)
        if nfev + 1 > max_evaluations:
            return None
        position[g] = incumbent
        cost[g] = evaluate(objective, incumbent)
        nfev += 1
        pbest[g] = incumbent
        pbest_cost[g] = cost[g]
        g = int(np.argmin(pbest_cost))
        best_cost = float(pbest_cost[g])
    else:
        history.append(best_cost)
    step = len(history)
    stopped_early = False

    while step <= iterations - 1:
        if nfev + population_size > max_evaluations:
            break
        r1 = generator.random(position.shape)
        r2 = generator.random(position.shape)
        inertia = generator.random(position.shape)
        c1 = generator.uniform(0.0, 2.0, position.shape)
        c2 = generator.uniform(0.0, 2.0, position.shape)
        social = pbest[g]
        velocity = inertia * velocity + c1 * r1 * (pbest - position) + c2 * r2 * (social - position)
        position = position + velocity
        position, velocity = box.zero_velocity_and_clip(position, velocity)
        cost = evaluate_rows(objective, position)
        nfev += population_size
        pbest, pbest_cost = personal_best_update(position, cost, pbest, pbest_cost)
        g = int(np.argmin(pbest_cost))
        best_cost = float(pbest_cost[g])
        history.append(best_cost)
        step += 1
        notify(callback, step, iterations, best_cost)
        if len(history) >= 2:
            last, prev = history[-1], history[-2]
            if last != prev and abs((last - prev) / max(abs(last), 1e-300)) <= acceptable_rate:
                stopped_early = True
                break
    incumbent = pbest[g].copy()
    return best_cost, incumbent, history, step, nfev, stopped_early


def minimize(
    objective,
    bounds,
    *,
    rng: np.random.Generator | None = None,
    seed: int | None = None,
    population_size: int = 25,
    iterations: int | None = None,
    max_evaluations: int | None = None,
    acceptable_rate: float = 5e-3,
    callback=None,
    violation=None,
):
    if iterations is None and max_evaluations is None:
        raise ValueError("pass iterations or max_evaluations")
    if iterations is None:
        iterations = max(1, max_evaluations // population_size)
    if max_evaluations is None:
        # Several epochs can each spend a full swarm. Leave room for restarts.
        max_evaluations = population_size * iterations * 4
    box = require_bounds(bounds)
    generator, recorded_seed = resolve_rng(rng, seed)
    history: list[float] = []
    incumbent: np.ndarray | None = None
    step = 0
    nfev = 0
    best_cost = float("inf")
    stopped_early = False
    while step <= iterations - 1:
        outcome = _epoch(
            objective,
            box,
            generator,
            population_size,
            iterations,
            acceptable_rate,
            history,
            incumbent,
            nfev,
            max_evaluations,
            callback,
        )
        if outcome is None:
            break
        best_cost, incumbent, history, step, nfev, stopped_early = outcome
        if not stopped_early:
            continue
        # Another epoch starts only when the manuscript while-condition still holds.
    if incumbent is None:
        raise RuntimeError("ME-D-PSO could not evaluate the initial population within the budget")
    violation_value = None if violation is None else float(violation(incumbent))
    message = f"completed ME-D-PSO through manuscript step {step}"
    if stopped_early and step > iterations - 1:
        message = f"ME-D-PSO reached the iteration horizon after an early-stop epoch (step {step})"
    elif nfev >= max_evaluations or (max_evaluations - nfev) < population_size:
        message = f"ME-D-PSO stopped on the evaluation budget at step {step}"
    return make_result(
        x=incumbent,
        fun=best_cost,
        nfev=nfev,
        history=history,
        seed=recorded_seed,
        algorithm="ME-D-PSO",
        population_size=population_size,
        max_evaluations=max_evaluations,
        generations=max(1, len(history)),
        requested_iterations=iterations,
        violation=violation_value,
        message=message,
    )
