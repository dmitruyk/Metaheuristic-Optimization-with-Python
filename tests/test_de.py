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


@pytest.mark.parametrize("use_rng", [False, True])
@pytest.mark.parametrize(
    "bounds,population,cap,actual_population",
    [
        ([[-2, 2]] * 2, 10, 80, 10),
        ([[-2, 2]] * 2, 10, 19, 10),
        ([[-2, 2]] * 3, 11, 27, 9),
        ([[1, 1], [-2, 2]], 10, 10, 5),
        ([[1, 1]] * 2, 10, 5, 5),
        ([[-2, 2]], 1, 5, 5),
        ([[-2, 2]] * 6, 1, 6, 6),
    ],
)
def test_scipy_hard_budget_and_realized_population(bounds, population, cap, actual_population, use_rng):
    calls = []

    def counted_objective(x):
        calls.append(x.copy())
        return sphere(x)

    random = {"rng": np.random.default_rng(5)} if use_rng else {"seed": 5}
    result = scipy_minimize(counted_objective, bounds, population_size=population, max_evaluations=cap, **random)
    assert actual_population <= len(calls) == result.nfev <= cap
    assert result.population_size == actual_population
    assert result.max_evaluations == cap
    assert result.fun == pytest.approx(min(map(sphere, calls)))
    assert np.all(result.x >= np.asarray(bounds)[:, 0])
    assert np.all(result.x <= np.asarray(bounds)[:, 1])


@pytest.mark.parametrize("cap", [0, 1, 4, 9])
def test_scipy_rejects_unaffordable_initial_population_without_evaluations(cap):
    def unexpected_objective(x):
        pytest.fail("an unaffordable population must not call the objective")

    with pytest.raises(ValueError, match="initial population"):
        scipy_minimize(unexpected_objective, [[-2, 2]] * 2, seed=5, population_size=10, max_evaluations=cap)


def test_scipy_iteration_budget_includes_initial_population():
    result = scipy_minimize(sphere, [[-2, 2]] * 2, seed=5, population_size=10, iterations=1)
    assert result.nfev == result.max_evaluations == 10


def test_scipy_injected_generator_reproducibility():
    results = [
        scipy_minimize(sphere, [[-2, 2]] * 2, rng=np.random.default_rng(3), population_size=10, max_evaluations=80) for _ in range(2)
    ]
    np.testing.assert_array_equal(results[0].x, results[1].x)
    assert results[0].fun == results[1].fun
