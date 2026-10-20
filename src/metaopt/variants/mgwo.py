"""Modified GWO (mGWO) from Appendix B.

Same position update and clip-to-box rule as GWO. The schedule is

``a = 2 - 2 * (step / iterations) ** 2``.
"""

from __future__ import annotations

import numpy as np

from metaopt.gwo import _gwo_minimize, nonlinear_a


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
    return _gwo_minimize(
        objective,
        bounds,
        rng=rng,
        seed=seed,
        population_size=population_size,
        iterations=iterations,
        max_evaluations=max_evaluations,
        a_rule=nonlinear_a,
        algorithm="mGWO",
        callback=callback,
        violation=violation,
    )
