"""Linear decreasing inertia PSO (LDW-PSO), Section 1.4.1 and Appendix B.

``w = (w_max - w_min) * (iterations - step) / iterations + w_min``
with the handbook defaults ``w_max=0.9``, ``w_min=0.4``, ``c1=c2=1.19``.
``step`` is the manuscript's 1-based generation index. Boundary policy is
the same zero-velocity-and-clip rule as canonical PSO.
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
    w_max: float = 0.9,
    w_min: float = 0.4,
    c1: float = 1.19,
    c2: float = 1.19,
    callback=None,
    violation=None,
):
    def propose(state, step, generator, box):
        del box
        horizon = state["schedule_length"]
        inertia = (w_max - w_min) * (horizon - step) / horizon + w_min
        r1 = generator.random(state["position"].shape)
        r2 = generator.random(state["position"].shape)
        velocity = (
            inertia * state["velocity"] + c1 * r1 * (state["pbest"] - state["position"]) + c2 * r2 * (state["gbest"] - state["position"])
        )
        return state["position"] + velocity, velocity

    return run_particle_swarm(
        objective,
        bounds,
        rng=rng,
        seed=seed,
        population_size=population_size,
        iterations=iterations,
        max_evaluations=max_evaluations,
        algorithm="LDW-PSO",
        propose=propose,
        callback=callback,
        violation=violation,
    )
