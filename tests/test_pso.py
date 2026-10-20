"""PSO behavior, budget, bounds, and invalid input."""

from __future__ import annotations

import numpy as np
import pytest

from metaopt.api import Bounds
from metaopt.pso import minimize


def sphere(x):
    return float(np.sum(np.square(x)))


def test_pso_reaches_a_small_sphere_value_and_respects_bounds():
    bounds = Bounds.from_pairs([[-5, 5], [-5, 5]])
    result = minimize(sphere, bounds, seed=1, population_size=20, iterations=40)
    assert result.success
    assert result.fun < 1e-3
    assert result.nfev == 20 * 40
    assert len(result.history) == 40
    assert result.history[-1] == pytest.approx(result.fun)
    assert np.all(result.history[1:] <= np.array(result.history[:-1]) + 1e-12)
    assert np.all(result.x >= -5) and np.all(result.x <= 5)


def test_evaluation_budget_stops_on_a_generation_boundary():
    bounds = [[-1.0, 1.0]]
    result = minimize(sphere, bounds, seed=2, population_size=8, iterations=100, max_evaluations=24)
    assert result.nfev == 24
    assert len(result.history) == 3
    assert "budget" in result.message


def test_nonfinite_objectives_do_not_become_the_best():
    def broken(x):
        if x[0] > 0:
            return float("nan")
        return sphere(x)

    result = minimize(broken, [[-1.0, 1.0]], seed=3, population_size=10, iterations=5)
    assert np.isfinite(result.fun)
    assert result.x[0] <= 0


def test_invalid_bounds_and_population():
    with pytest.raises(ValueError):
        minimize(sphere, [[1.0, -1.0]], seed=1, population_size=4, iterations=2)
    with pytest.raises(ValueError):
        minimize(sphere, [[0.0, 1.0]], seed=1, population_size=0, iterations=2)
    with pytest.raises(ValueError):
        minimize(sphere, [[0.0, 1.0]], seed=1, rng=np.random.default_rng(1), iterations=2)
