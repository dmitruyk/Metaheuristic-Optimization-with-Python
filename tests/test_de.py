"""DE/rand/1/bin, DE/best/1/bin, and the separate SciPy baseline."""

from __future__ import annotations

import numpy as np
import pytest

from metaopt.de import minimize, minimize_best, scipy_minimize


def sphere(x):
    return float(np.sum(np.square(x)))


def test_both_mutation_strategies_decrease_sphere():
    bounds = [[-5.0, 5.0]] * 3
    rand = minimize(sphere, bounds, seed=4, population_size=15, iterations=25)
    best = minimize_best(sphere, bounds, seed=4, population_size=15, iterations=25)
    assert rand.fun < 1.0
    assert best.fun < 1.0
    assert rand.nfev == 15 * 25
    assert best.nfev == rand.nfev
    assert np.all(np.abs(rand.x) <= 5)
    assert rand.algorithm == "DE/rand/1/bin"
    assert best.algorithm == "DE/best/1/bin"


def test_population_must_support_three_distinct_indices():
    with pytest.raises(ValueError):
        minimize(sphere, [[-1.0, 1.0]], seed=1, population_size=3, iterations=2)


def test_scipy_baseline_is_labeled_and_finite():
    result = scipy_minimize(sphere, [[-2.0, 2.0]] * 2, seed=5, population_size=10, max_evaluations=80)
    assert result.algorithm.startswith("scipy")
    assert np.isfinite(result.fun)
    assert result.nfev > 0
