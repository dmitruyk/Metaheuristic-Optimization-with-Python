"""Inertia-adaptation PSO (IA-PSO), Section 1.4.2 and Appendix B.

The manuscript update is not a plain position increment. After the velocity
update it applies

``x = x * (1 - rho) + v``, ``rho ~ Uniform(-0.25, 0.25)``,

and the inertia of each particle is

``w = w0 * (1 - ||gbest - x|| / max_j ||gbest - x_j||)``, ``w0 ~ Uniform(0.5, 1)``.

If every particle sits on the global best, the manuscript divides by zero.
This implementation uses scale 1 in that case, which yields ``w = w0``
because every distance is zero. Boundary policy: zero-velocity-and-clip.
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
    c1: float = 1.19,
    c2: float = 1.19,
    callback=None,
    violation=None,
):
    def propose(state, step, generator, box):
        del step, box
        dist = np.linalg.norm(state["gbest"] - state["position"], axis=1)
        scale = float(np.max(dist))
        if scale == 0.0:
            scale = 1.0
        w0 = generator.uniform(0.5, 1.0, state["position"].shape[0])
        inertia = (w0 * (1.0 - dist / scale))[:, None]
        r1 = generator.random(state["position"].shape)
        r2 = generator.random(state["position"].shape)
        rho = generator.uniform(-0.25, 0.25, state["position"].shape)
        velocity = (
            inertia * state["velocity"] + c1 * r1 * (state["pbest"] - state["position"]) + c2 * r2 * (state["gbest"] - state["position"])
        )
        position = state["position"] * (1.0 - rho) + velocity
        return position, velocity

    result = run_particle_swarm(
        objective,
        bounds,
        rng=rng,
        seed=seed,
        population_size=population_size,
        iterations=iterations,
        max_evaluations=max_evaluations,
        algorithm="IA-PSO",
        propose=propose,
        callback=callback,
        violation=violation,
    )
    return result
