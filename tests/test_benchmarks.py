"""Sanity checks for the 54 Appendix B benchmarks."""

from __future__ import annotations

import numpy as np
import pytest

from metaopt.benchmarks import (
    BENCHMARKS,
    Ackley1Function,
    Alpine2Function,
    DixonAndPriceFunction,
    ExponentialFunction,
    HappyCatFunction,
    LevyFunction,
    PavianiFunction,
    PeriodicFunction,
    Perm0DBetaFunction,
    PermDBetaFunction,
    QingFunction,
    QuinticFunction,
    RastriginFunction,
    RosenbrockFunction,
    Schwefel226Function,
    SphericalFunction,
    StyblinskiTangFunction,
    TridFunction,
    Trigonometric2Function,
    WavyFunction,
    WeierstrassFunction,
    WhitleyFunction,
    XinSheYang3Function,
    XinSheYang4Function,
    XinSheYangFunction,
    benchmark_domain,
    seed_benchmark_noise,
)

SCHWEFEL_226_POINT = 420.968746359982015


def test_there_are_54_benchmarks():
    assert len(BENCHMARKS) == 54
    assert len({name for name, _, _ in BENCHMARKS}) == 54


def test_domains_match_dimension_and_contain_finite_values():
    for index, (name, function, _bounds) in enumerate(BENCHMARKS):
        if name == "Elliptic":
            with pytest.raises(ValueError):
                function(np.zeros(1))
        for dimension in (2, 5):
            domain = np.asarray(benchmark_domain(index, dimension), dtype=float)
            assert domain.shape == (dimension, 2)
            assert np.all(domain[:, 1] >= domain[:, 0])
            span = domain[:, 1] - domain[:, 0]
            sample = domain[:, 0] + 0.5 * span
            if name == "Paviani":
                sample = np.clip(sample, 2.1, 9.9)
            if name in ("Quartic", "Xin-She Yang"):
                seed_benchmark_noise(dimension)
            value = function(sample)
            assert np.isfinite(value), name


def test_known_reference_values():
    zeros = np.zeros(4)
    ones = np.ones(4)
    assert SphericalFunction(zeros) == 0.0
    assert RastriginFunction(zeros) == 0.0
    assert Ackley1Function(zeros) == pytest.approx(0.0, abs=1e-12)
    assert RosenbrockFunction(ones) == 0.0
    assert LevyFunction(ones) == pytest.approx(0.0, abs=1e-12)
    assert ExponentialFunction(zeros) == pytest.approx(-1.0)
    assert PeriodicFunction(zeros) == pytest.approx(0.9)
    assert HappyCatFunction(-np.ones(4)) == pytest.approx(0.0, abs=1e-12)
    assert XinSheYang3Function(zeros) == pytest.approx(-1.0)
    assert XinSheYang4Function(zeros) == pytest.approx(-1.0)
    assert Trigonometric2Function(np.full(4, 0.9)) == pytest.approx(1.0)
    assert WavyFunction(zeros) == pytest.approx(0.0, abs=1e-12)
    assert WeierstrassFunction(zeros) == pytest.approx(0.0, abs=1e-8)
    assert QuinticFunction(np.full(3, -1.0)) == 0.0
    assert QuinticFunction(np.full(3, 2.0)) == 0.0
    qing = np.sqrt(np.arange(1, 5, dtype=float))
    assert QingFunction(qing) == pytest.approx(0.0, abs=1e-12)
    dixon = np.ones(4)
    for index in range(1, 4):
        dixon[index] = np.sqrt(dixon[index - 1] / 2)
    assert DixonAndPriceFunction(dixon) == pytest.approx(0.0, abs=1e-10)
    perm = np.arange(1, 5, dtype=float)
    assert PermDBetaFunction(perm) == pytest.approx(0.0, abs=1e-8)
    perm0 = 1 / np.arange(1, 5, dtype=float)
    assert Perm0DBetaFunction(perm0) == pytest.approx(0.0, abs=1e-8)
    schwefel = np.full(3, SCHWEFEL_226_POINT)
    assert Schwefel226Function(schwefel) == pytest.approx(-418.9828872724338, rel=1e-6)
    style = np.full(3, -2.903534)
    assert StyblinskiTangFunction(style) == pytest.approx(-39.165990 * 3, rel=1e-4)
    dimension = 6
    trid_x = np.array([i * (dimension + 1 - i) for i in range(1, dimension + 1)], dtype=float)
    expected = -dimension * (dimension + 4) * (dimension - 1) / 6
    assert TridFunction(trid_x) == pytest.approx(expected, rel=1e-10)


def test_whitley_table_disagrees_with_the_listing():
    # Table 4.1 says the minimum is 1 at the origin. Appendix B, citing
    # Jamil and Yang, is 0 at the all-ones vector.
    assert WhitleyFunction(np.ones(2)) == pytest.approx(0.0, abs=1e-10)
    at_origin = WhitleyFunction(np.zeros(2))
    assert at_origin != pytest.approx(1.0, abs=1e-6)
    assert at_origin > 0


def test_alpine2_is_finite_on_its_closed_domain():
    value = Alpine2Function(np.full(2, 7.9170526))
    assert np.isfinite(value)
    assert value < 0


def test_stochastic_benchmarks_repeat_when_reseeded():
    x = np.array([0.2, -0.1, 0.3])
    seed_benchmark_noise(7)
    first = XinSheYangFunction(x)
    seed_benchmark_noise(7)
    second = XinSheYangFunction(x)
    seed_benchmark_noise(8)
    third = XinSheYangFunction(x)
    assert first == second
    assert first != third


def test_paviani_warns_and_is_nonfinite_outside_the_open_interval():
    # The formula uses log(x-2) and log(10-x). x=0 is outside (2, 10).
    with pytest.warns(RuntimeWarning, match="open interval"):
        value = PavianiFunction(np.zeros(2))
    assert not np.isfinite(value)
    assert np.isfinite(PavianiFunction(np.full(2, 5.0)))
