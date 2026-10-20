"""Objective values, feasibility, seeds, budgets, noise, domains, and bounds."""

from __future__ import annotations

import warnings

import numpy as np
import pytest

from metaopt.benchmarks import (
    Alpine2Function,
    EllipticFunction,
    QuarticFunction,
    Schwefel223Function,
    benchmark_domain,
    benchmark_names,
    evaluate_benchmark,
    outside_domain,
    seed_benchmark_noise,
)
from metaopt.de import minimize as de_minimize
from metaopt.experiments import HANDBOOK_ALGORITHMS, summarize_groups
from metaopt.gwo import minimize as gwo_minimize
from metaopt.pso import minimize as pso_minimize
from metaopt.variants.ia_pso import minimize as ia_pso_minimize
from metaopt.variants.med_pso import minimize as med_pso_minimize


def sphere(x):
    return float(np.sum(np.square(np.asarray(x, dtype=float))))


def test_seed_and_generator_draw_the_same_pso_history():
    bounds = [[-3.0, 3.0]] * 2
    from_seed = pso_minimize(sphere, bounds, seed=5, population_size=6, iterations=3)
    from_generator = pso_minimize(
        sphere,
        bounds,
        rng=np.random.default_rng(5),
        population_size=6,
        iterations=3,
    )
    assert from_seed.history == from_generator.history
    assert from_seed.nfev == 18
    assert from_seed.seed == 5
    assert from_generator.seed is None


def test_explicit_budget_bounds_nfev_for_pso_de_and_gwo():
    bounds = [[-2.0, 2.0]]
    for minimizer in (pso_minimize, de_minimize, gwo_minimize):
        result = minimizer(sphere, bounds, seed=4, population_size=5, iterations=50, max_evaluations=15)
        assert result.nfev == 15
        assert result.nfev <= 15


def test_minimizers_keep_the_reported_point_inside_the_box():
    bounds = [[0.0, 1.0]]

    def push_high(x):
        return float(-np.asarray(x, dtype=float)[0])

    for minimizer in (pso_minimize, de_minimize, gwo_minimize):
        result = minimizer(push_high, bounds, seed=8, population_size=8, iterations=12)
        assert np.all(result.x >= 0.0)
        assert np.all(result.x <= 1.0)
        assert np.isfinite(result.fun)


@pytest.mark.parametrize("name", sorted(HANDBOOK_ALGORITHMS))
def test_every_handbook_algorithm_respects_the_box_and_the_budget(name):
    result = HANDBOOK_ALGORITHMS[name](
        sphere,
        [[-2.0, 2.0], [-2.0, 2.0]],
        seed=11,
        population_size=9,
        max_evaluations=36,
    )
    assert result.nfev <= 36
    assert np.all(result.x >= -2.0)
    assert np.all(result.x <= 2.0)
    assert np.isfinite(result.fun)


def test_feasibility_flag_follows_the_violation_measure():
    feasible = pso_minimize(
        sphere,
        [[-1.0, 1.0]],
        seed=1,
        population_size=4,
        iterations=2,
        violation=lambda _x: 0.0,
    )
    infeasible = pso_minimize(
        sphere,
        [[-1.0, 1.0]],
        seed=1,
        population_size=4,
        iterations=2,
        violation=lambda _x: 2.5,
    )
    assert feasible.feasible is True
    assert feasible.success is True
    assert feasible.constraint_violation == 0.0
    assert infeasible.feasible is False
    assert infeasible.success is False
    assert infeasible.constraint_violation == 2.5


def test_quartic_noise_is_uniform_and_repeats_only_after_reseeding():
    point = np.array([0.5, -0.25, 0.1])
    weights = np.arange(1, 4, dtype=float)
    deterministic = float(np.sum(weights * point**4))
    seed_benchmark_noise(3)
    first = QuarticFunction(point)
    second = QuarticFunction(point)
    seed_benchmark_noise(3)
    repeated = QuarticFunction(point)
    noise = first - deterministic
    assert 0.0 <= noise < 1.0
    assert first != second
    assert first == repeated


def test_elliptic_and_registered_domains_reject_bad_inputs():
    with pytest.raises(ValueError, match="D >= 2"):
        EllipticFunction(np.zeros(1))
    assert not np.any(outside_domain("Spherical", [0.0, 0.0]))
    assert np.all(outside_domain("Paviani", [0.0, 11.0]))
    assert not np.any(outside_domain("Paviani", [5.0, 5.0]))
    assert not np.any(outside_domain("Rotated Hyper Ellipsoid", [-65.536, 65.536]))
    assert np.any(outside_domain("Rotated Hyper Ellipsoid", [-65.53, 65.54]))
    with pytest.raises(ValueError, match="outside the registered domain"):
        evaluate_benchmark("Spherical", [0.0, 40.0], strict=True)
    with pytest.warns(RuntimeWarning, match="outside the registered domain"):
        value = evaluate_benchmark("Spherical", [0.0, 40.0], strict=False)
    assert value == pytest.approx(1600.0)
    with pytest.raises(KeyError):
        outside_domain("Not a benchmark", [0.0])


def test_ia_pso_defines_inertia_when_every_particle_is_the_best():
    result = ia_pso_minimize(
        lambda _x: 0.0,
        [[0.0, 0.0], [0.0, 0.0]],
        seed=2,
        population_size=4,
        iterations=3,
    )
    assert result.fun == 0.0
    assert result.nfev == 12
    assert np.all(result.x == 0.0)


def test_med_pso_restarts_without_indexing_an_empty_history():
    result = med_pso_minimize(
        sphere,
        [[-1.0, 1.0], [-1.0, 1.0]],
        seed=9,
        population_size=6,
        iterations=4,
        max_evaluations=80,
        acceptable_rate=1.0,
    )
    assert np.isfinite(result.fun)
    assert result.nfev <= 80
    assert len(result.history) >= 2


@pytest.mark.parametrize("name", benchmark_names())
def test_every_benchmark_is_finite_at_the_domain_midpoint(name):
    seed_benchmark_noise(0)
    index = benchmark_names().index(name)
    domain = np.asarray(benchmark_domain(index, 2), dtype=float)
    midpoint = (domain[:, 0] + domain[:, 1]) / 2.0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        value = evaluate_benchmark(name, midpoint)
    assert np.isfinite(value)


def test_invalid_dimension_and_empty_point_are_rejected():
    with pytest.raises(ValueError, match="dimension"):
        benchmark_domain(0, 0)
    with pytest.raises(ValueError, match="at least one"):
        outside_domain("Spherical", [])


def test_nonfinite_objective_values_do_not_become_the_reported_best():
    def objective(x):
        value = float(np.asarray(x, dtype=float)[0])
        if value < 0.0:
            return float("nan")
        return (value - 0.2) ** 2

    result = pso_minimize(objective, [[-1.0, 1.0]], seed=3, population_size=12, iterations=8)
    assert np.isfinite(result.fun)
    assert result.x[0] >= 0.0


def test_budget_smaller_than_the_population_is_rejected():
    with pytest.raises(ValueError, match="initial population"):
        pso_minimize(sphere, [[-1.0, 1.0]], seed=1, population_size=8, max_evaluations=4)


def test_de_and_gwo_reject_populations_that_cannot_form_the_update():
    with pytest.raises(ValueError):
        de_minimize(sphere, [[-1.0, 1.0]], seed=1, population_size=3, iterations=2)
    with pytest.raises(ValueError):
        gwo_minimize(sphere, [[-1.0, 1.0]], seed=1, population_size=2, iterations=2)


def test_alpine2_stays_nonfinite_for_a_negative_coordinate():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        value = Alpine2Function(np.array([-1.0, 2.0]))
    assert not np.isfinite(value)


def test_schwefel_223_overflow_does_not_raise():
    with np.errstate(over="ignore"):
        value = Schwefel223Function(np.array([1e40, -1e40]))
    assert np.isinf(value)


def test_summarize_groups_uses_the_sample_standard_deviation():
    rows = [
        {"algorithm": "PSO", "benchmark": "Spherical", "fun": 1.0, "nfev": 10, "seconds": 0.1},
        {"algorithm": "PSO", "benchmark": "Spherical", "fun": 3.0, "nfev": 10, "seconds": 0.2},
    ]
    summary = summarize_groups(rows)
    assert summary[0]["median"] == 2.0
    assert summary[0]["minimum"] == 1.0
    assert summary[0]["maximum"] == 3.0
    assert summary[0]["mean"] == 2.0
    assert summary[0]["sample_std"] == pytest.approx(np.std([1.0, 3.0], ddof=1))
    assert summary[0]["runs"] == 2
