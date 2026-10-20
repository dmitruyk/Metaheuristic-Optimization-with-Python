"""von Neumann PSO, Section 1.5.2 and Appendix B.

Particles sit on a square torus. The social attractor is the best personal
best among the up, down, left, and right neighbors. The particle itself is
not in that neighborhood, matching the manuscript. ``population_size`` must
be a perfect square (the experiments use 25). Boundary policy:
zero-velocity-and-clip.
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
    side = int(round(np.sqrt(population_size)))
    if side * side != population_size:
        raise ValueError("von Neumann PSO requires a square population, for example 25")

    def propose(state, step, generator, box):
        del step, box
        grid = np.arange(population_size).reshape(side, side)
        up = np.roll(grid, 1, axis=0).ravel()
        down = np.roll(grid, -1, axis=0).ravel()
        left = np.roll(grid, 1, axis=1).ravel()
        right = np.roll(grid, -1, axis=1).ravel()
        neighbors = np.stack([up, down, left, right], axis=1)
        neighbor_costs = state["pbest_cost"][neighbors]
        choice = np.argmin(neighbor_costs, axis=1)
        index = np.arange(population_size)
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
        algorithm="vonNeumann-PSO",
        propose=propose,
        callback=callback,
        violation=violation,
    )
