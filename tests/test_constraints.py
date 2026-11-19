"""Penalty helpers and the remaining manuscript variants."""

from __future__ import annotations

import numpy as np
import pytest

from metaopt.constraints import equality_band, feasible_from_penalty, hinge, weighted_sum
from metaopt.variants.bb_pso import minimize as bb
from metaopt.variants.ia_pso import minimize as ia
from metaopt.variants.ldw_pso import minimize as ldw
from metaopt.variants.med_pso import minimize as med
from metaopt.variants.ring_pso import minimize as ring
from metaopt.variants.sade import minimize as sade
from metaopt.variants.vct_pso import minimize as vct


def sphere(x):
    return float(np.sum(np.square(x)))


def test_penalty_helpers():
    assert hinge(-3) == 0
    assert hinge(1.5) == 1.5
    assert equality_band(0.01, 0.02) == 0
    assert equality_band(0.05, 0.02) == pytest.approx(0.05)
    assert weighted_sum([-1, 2, 0], 10) == 20


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_hinge_rejects_nonfinite_residuals(value):
    with pytest.raises(ValueError, match="finite"):
        hinge(value)


@pytest.mark.parametrize("violation", [0.001, 1e-30])
def test_small_penalty_cannot_certify_feasibility(violation):
    total = weighted_sum([violation], 1000)
    with pytest.raises(ValueError, match="cannot certify"):
        feasible_from_penalty(total, 1000, 0)
    assert not feasible_from_penalty(total, 1000, 0, violations=[0, violation])


def test_feasibility_checks_every_component_with_explicit_tolerance():
    assert feasible_from_penalty(2000, 1000, 0, violations=[0, 0])
    assert feasible_from_penalty(1, 1000, 0, violations=[0.001], tolerance=0.001)
    assert not feasible_from_penalty(1, 1000, 0, violations=[0, 0.002], tolerance=0.001)


@pytest.mark.parametrize("violations", [[float("nan")], [float("inf")], [-1], [[0]]])
def test_feasibility_rejects_invalid_components(violations):
    with pytest.raises(ValueError, match="violations"):
        feasible_from_penalty(0, 1000, 0, violations=violations)


@pytest.mark.parametrize("tolerance", [-1, float("nan"), float("inf")])
def test_feasibility_rejects_invalid_tolerance(tolerance):
    with pytest.raises(ValueError, match="tolerance"):
        feasible_from_penalty(0, 1000, 0, violations=[0], tolerance=tolerance)


@pytest.mark.parametrize(
    "minimizer",
    [ldw, ia, bb, vct, ring, sade],
)
def test_variant_smoke(minimizer):
    result = minimizer(sphere, [[-2.0, 2.0]] * 2, seed=9, population_size=12, iterations=6)
    assert np.isfinite(result.fun)
    assert result.nfev >= 12
    assert result.history[0] >= result.history[-1] - 1e-9


def test_med_pso_does_not_index_an_empty_history():
    result = med(sphere, [[-2.0, 2.0]] * 2, seed=10, population_size=8, iterations=6, acceptable_rate=1e-6)
    assert np.isfinite(result.fun)
    assert len(result.history) >= 1
    assert result.nfev >= 8
