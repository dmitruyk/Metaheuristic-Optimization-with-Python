"""Self-adaptive DE as printed in Chapter 2 and Appendix B (``SADE``).

This is not Qin and Suganthan's SaDE strategy pool. The manuscript keeps one
shared ``F`` and one shared ``CR``. Before each target vector, each parameter
is replaced with probability ``tau``:

``F <- Uniform(0.1, 0.9)`` with probability ``tau1=0.1``,
``CR <- Uniform(0, 1)`` with probability ``tau2=0.1``.

Otherwise the previous value is kept, including across individuals and
generations. Mutation is DE/rand/1 and crossover is binomial. The donor is
clipped to the box before crossover.
"""

from __future__ import annotations

import numpy as np

from metaopt.de import _de_loop


def _adapt(generator, cr_value, f_value, tau1, tau2, f_lower, f_upper):
    if generator.random() < tau1:
        f_value = f_lower + generator.random() * (f_upper - f_lower)
    if generator.random() < tau2:
        cr_value = float(generator.random())
    return cr_value, f_value


def minimize(
    objective,
    bounds,
    *,
    rng: np.random.Generator | None = None,
    seed: int | None = None,
    population_size: int = 25,
    iterations: int | None = None,
    max_evaluations: int | None = None,
    cr: float = 0.5,
    f: float = 0.6,
    tau1: float = 0.1,
    tau2: float = 0.1,
    f_lower: float = 0.1,
    f_upper: float = 0.9,
    callback=None,
    violation=None,
):
    from metaopt.de import _mutate_rand

    def adapt(generator, cr_value, f_value):
        return _adapt(generator, cr_value, f_value, tau1, tau2, f_lower, f_upper)

    return _de_loop(
        objective,
        bounds,
        rng=rng,
        seed=seed,
        population_size=population_size,
        iterations=iterations,
        max_evaluations=max_evaluations,
        mutation=_mutate_rand,
        cr=cr,
        f_scale=f,
        algorithm="SADE",
        callback=callback,
        violation=violation,
        adapt=adapt,
    )
