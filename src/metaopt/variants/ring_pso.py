"""Ring-topology PSO, Section 1.5.1 and Appendix B.

The social attractor of each particle is the personal best of the better of
itself and its two ring neighbors. Boundary policy: zero-velocity-and-clip.
Coefficients default to ``w=0.72``, ``c1=c2=1.19``.
"""

from __future__ import annotations

import numpy as np

from metaopt.variants._common import run_particle_swarm


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
):
    def propose(state, step, generator, box):
        del step, box
        rows = state["position"].shape[0]
        index = np.arange(rows)
        left = np.roll(index, 1)
        right = np.roll(index, -1)
        neighbors = np.stack([left, index, right], axis=1)
        neighbor_costs = state["pbest_cost"][neighbors]
        choice = np.argmin(neighbor_costs, axis=1)
        chosen = neighbors[index, choice]
        local_best = state["pbest"][chosen]
        r1 = generator.random(state["position"].shape)
        r2 = generator.random(state["position"].shape)
        velocity = w * state["velocity"] + c1 * r1 * (state["pbest"] - state["position"]) + c2 * r2 * (local_best - state["position"])
        return state["position"] + velocity, velocity

    return run_particle_swarm(
        objective,
        bounds,
        rng=rng,
        seed=seed,
        population_size=population_size,
        iterations=iterations,
        max_evaluations=max_evaluations,
        algorithm="Ring-PSO",
        propose=propose,
        callback=callback,
        violation=violation,
    )
