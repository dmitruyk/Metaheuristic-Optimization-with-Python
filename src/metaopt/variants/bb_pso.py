"""Bare Bones PSO (BB-PSO), Section 1.4.3 and Appendix B.

Each coordinate is drawn from a normal distribution whose mean is the
midpoint of the personal best and the global best and whose standard
deviation is their absolute difference. A floor of ``1e-20`` keeps the
deviation nonzero, as in the manuscript. There is no velocity. Positions
are clipped to the box.
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
    callback=None,
    violation=None,
    epsilon: float = 1e-20,
):
    def propose(state, step, generator, box):
        del step, box
        mean = 0.5 * (state["gbest"] + state["pbest"])
        std = np.abs(state["gbest"] - state["pbest"]) + epsilon
        position = generator.normal(mean, std)
        return position, np.zeros_like(position)

    return run_particle_swarm(
        objective,
        bounds,
        rng=rng,
        seed=seed,
        population_size=population_size,
        iterations=iterations,
        max_evaluations=max_evaluations,
        algorithm="BB-PSO",
        propose=propose,
        callback=callback,
        violation=violation,
    )
