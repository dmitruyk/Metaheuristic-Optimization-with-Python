"""Same seed and same budget reproduce the same history in one environment."""

from __future__ import annotations

import numpy as np

from metaopt.de import minimize as de_minimize
from metaopt.de import minimize_best
from metaopt.gwo import minimize as gwo_minimize
from metaopt.pso import minimize as pso_minimize


def sphere(x):
    array = np.asarray(x, dtype=float)
    return float(np.sum(array**2))


def test_pso_de_and_gwo_histories_repeat():
    bounds = [[-4.0, 4.0]] * 3
    for minimizer in (pso_minimize, de_minimize, minimize_best, gwo_minimize):
        first = minimizer(sphere, bounds, seed=12345, population_size=10, iterations=7)
        second = minimizer(sphere, bounds, seed=12345, population_size=10, iterations=7)
        third = minimizer(sphere, bounds, seed=99, population_size=10, iterations=7)
        assert first.history == second.history
        assert first.x.tolist() == second.x.tolist()
        assert first.nfev == second.nfev
        assert first.history != third.history
