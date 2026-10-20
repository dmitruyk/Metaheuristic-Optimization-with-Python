"""Penalty helpers and the remaining manuscript variants."""

from __future__ import annotations

import numpy as np
import pytest

from metaopt.constraints import equality_band, hinge, weighted_sum
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
