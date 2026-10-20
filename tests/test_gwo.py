"""GWO, mGWO, and GWOEPD."""

from __future__ import annotations

import numpy as np
import pytest

from metaopt.gwo import minimize
from metaopt.variants.gwoepd import minimize as gwoepd
from metaopt.variants.mgwo import minimize as mgwo
from metaopt.variants.von_neumann_pso import minimize as von_neumann


def sphere(x):
    return float(np.sum(np.square(x)))


def test_gwo_and_mgwo_share_the_evaluation_count():
    bounds = [[-3.0, 3.0]] * 2
    gwo = minimize(sphere, bounds, seed=6, population_size=12, iterations=15)
    modified = mgwo(sphere, bounds, seed=6, population_size=12, iterations=15)
    assert gwo.fun < 0.5
    assert modified.fun < 0.5
    assert gwo.nfev == 12 * 15
    assert modified.nfev == gwo.nfev
    assert gwo.algorithm == "GWO"
    assert modified.algorithm == "mGWO"


def test_gwoepd_counts_the_replaced_wolves():
    result = gwoepd(sphere, [[-3.0, 3.0]] * 2, seed=7, population_size=10, iterations=4)
    # initial pack + 3 generations * (10 + 5)
    assert result.nfev == 10 + 3 * 15
    assert np.isfinite(result.fun)


def test_gwo_rejects_a_pack_smaller_than_three():
    with pytest.raises(ValueError):
        minimize(sphere, [[-1.0, 1.0]], seed=1, population_size=2, iterations=2)


def test_von_neumann_requires_a_square_population():
    with pytest.raises(ValueError):
        von_neumann(sphere, [[-1.0, 1.0]], seed=1, population_size=10, iterations=2)
    result = von_neumann(sphere, [[-2.0, 2.0]] * 2, seed=1, population_size=9, iterations=4)
    assert result.nfev == 36
