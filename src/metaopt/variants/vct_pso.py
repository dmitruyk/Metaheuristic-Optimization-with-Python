"""Varying cognitive term PSO (VCT-PSO), Section 1.4.4 and Appendix B.

Every ``refresh_period`` generations (handbook ``RC``, default 5 in Appendix B;
the chapter listing takes ``RC`` as an argument), the cognitive attractor is
another particle's personal best. The index map is the manuscript rule

``idx = randint(0, K - 1)``, then ``idx += (idx >= arange(K))``,

which excludes a particle's own index and also never draws ``K - 1`` before
the shift. Boundary policy: zero-velocity-and-clip.
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
    refresh_period: int = 5,
    callback=None,
    violation=None,
):
    if refresh_period < 1:
        raise ValueError("refresh_period must be >= 1")

    def propose(state, step, generator, box):
        del box
        position = state["position"]
        rows = position.shape[0]
        if step % refresh_period == 0:
            if rows < 2:
                raise ValueError("VCT-PSO needs at least 2 particles to resample the cognitive term")
            idx = generator.integers(0, rows - 1, size=rows)
            idx = idx + (idx >= np.arange(rows))
            cognitive = state["pbest"][idx]
        else:
            cognitive = state["pbest"]
        r1 = generator.random(position.shape)
        r2 = generator.random(position.shape)
        velocity = w * state["velocity"] + c1 * r1 * (cognitive - position) + c2 * r2 * (state["gbest"] - position)
        return position + velocity, velocity

    return run_particle_swarm(
        objective,
        bounds,
        rng=rng,
        seed=seed,
        population_size=population_size,
        iterations=iterations,
        max_evaluations=max_evaluations,
        algorithm="VCT-PSO",
        propose=propose,
        callback=callback,
        violation=violation,
        minimum_population=2,
    )
