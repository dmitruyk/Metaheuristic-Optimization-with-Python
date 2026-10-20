"""Fifty-four benchmark functions from Appendix B of the handbook.

Formulas and domains follow the manuscript listing ``BENCHMARKS AND DOMAINS``.
Equation images in Chapter 4 are not stored as text in the DOCX; where this
module and Table 4.1 disagree, the disagreement is recorded in ``docs/errata.md``
and the executable formula is left as printed in Appendix B.

Stochastic benchmarks (Quartic, Xin-She Yang) draw noise from
:func:`uniform_noise`, not from the optimizer's generator.
"""

from __future__ import annotations

import warnings

import numpy as np

_noise_rng = np.random.default_rng(0)


def seed_benchmark_noise(seed: int) -> np.random.Generator:
    """Replace the noise generator used by Quartic and Xin-She Yang.

    The manuscript calls ``np.random.random`` on the global legacy stream,
    which is also the stream used by ``np.random.seed`` inside the optimizers.
    Separating the streams changes search trajectories on those two functions.
    """

    global _noise_rng
    _noise_rng = np.random.default_rng(seed)
    return _noise_rng


def uniform_noise(size: int | None = None) -> float | np.ndarray:
    """Uniform sample on ``[0, 1)`` from the benchmark-noise generator."""

    if size is None:
        return float(_noise_rng.random())
    return _noise_rng.random(size)


def Ackley1Function(x):
    x = np.asarray(x, dtype=float)
    D = x.size
    return float(-20 * np.exp(-0.2 * np.sqrt(np.sum(x**2) / D)) - np.exp(np.sum(np.cos(2 * np.pi * x)) / D) + 20 + np.e)


def Ackley4Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(np.exp(-0.2) * np.sqrt(x[:-1] ** 2 + x[1:] ** 2) + 3 * (np.cos(2 * x[:-1]) + np.sin(2 * x[1:]))))


def Alpine1Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(np.abs(x * np.sin(x) + 0.1 * x)))


def Alpine2Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.real(-np.prod(np.sqrt(x) * np.sin(x))))


def BrownFunction(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum((x[:-1] ** 2) ** (x[1:] ** 2 + 1) + (x[1:] ** 2) ** (x[:-1] ** 2 + 1)))


def ChungReynoldsFunction(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(x**2) ** 2)


def CosineMixtureFunction(x):
    x = np.asarray(x, dtype=float)
    return float(-0.1 * np.sum(np.cos(5 * np.pi * x)) + np.sum(x**2))


def Deb1Function(x):
    x = np.asarray(x, dtype=float)
    return float(-np.sum(np.sin(5 * np.pi * x) ** 6) / x.size)


def Deb3Function(x):
    x = np.asarray(x, dtype=float)
    return float(-np.sum(np.sin(5 * np.pi * (x ** (3 / 4) - 0.05)) ** 6) / x.size)


def DixonAndPriceFunction(x):
    x = np.asarray(x, dtype=float)
    i = np.arange(2, x.size + 1, dtype=float)
    return float((x[0] - 1) ** 2 + np.sum(i * (2 * x[1:] ** 2 - x[:-1]) ** 2))


def EggHolderFunction(x):
    x = np.asarray(x, dtype=float)
    xi, xj = x[:-1], x[1:]
    return float(np.sum(-(xj + 47) * np.sin(np.sqrt(np.abs(xj + xi / 2 + 47))) - xi * np.sin(np.sqrt(np.abs(xi - (xj + 47))))))


def EllipticFunction(x):
    x = np.asarray(x, dtype=float)
    D = x.size
    if D < 2:
        raise ValueError("EllipticFunction is defined only for D >= 2 (the manuscript exponent uses i/(D-1)).")
    i = np.arange(D, dtype=float)
    return float(np.sum((1e6) ** (i / (D - 1)) * x**2))


def ExponentialFunction(x):
    x = np.asarray(x, dtype=float)
    return float(-np.exp(-0.5 * np.sum(x**2)))


def GriewankFunction(x):
    x = np.asarray(x, dtype=float)
    i = np.arange(1, x.size + 1, dtype=float)
    return float(1 + np.sum(x**2) / 4000 - np.prod(np.cos(x / np.sqrt(i))))


def HappyCatFunction(x):
    x = np.asarray(x, dtype=float)
    D = x.size
    return float(((np.sum(x**2) - D) ** 2) ** (1 / 8) + (0.5 * np.sum(x**2) + np.sum(x)) / D + 0.5)


def LevyFunction(x):
    # Jamil & Yang: last term (w_D-1)^2 (1+sin^2(2*pi*w_D)) is outside the sum
    x = np.asarray(x, dtype=float)
    w = 1 + (x - 1) / 4
    return float(
        np.sin(np.pi * w[0]) ** 2
        + np.sum((w[:-1] - 1) ** 2 * (1 + 10 * np.sin(np.pi * w[:-1] + 1) ** 2))
        + (w[-1] - 1) ** 2 * (1 + np.sin(2 * np.pi * w[-1]) ** 2)
    )


def MichalewiczFunction(x):
    x = np.asarray(x, dtype=float)
    i = np.arange(1, x.size + 1, dtype=float)
    return float(-np.sum(np.sin(x) * np.sin(i * x**2 / np.pi) ** 20))


def PavianiFunction(x):
    """Appendix B Paviani formula.

    The logs are defined on the open interval ``(2, 10)``. A point outside
    that interval is still passed through the same expression. NumPy's
    invalid-log warning is replaced by one explicit warning, and the returned
    value stays non-finite. The formula is not rewritten.
    """

    x = np.asarray(x, dtype=float)
    outside = (x <= 2.0) | (x >= 10.0)
    if np.any(outside):
        warnings.warn(
            "PavianiFunction is defined on the open interval (2, 10); "
            f"{int(np.count_nonzero(outside))} coordinate(s) are outside it and the formula is non-finite there.",
            RuntimeWarning,
            stacklevel=2,
        )
    with np.errstate(invalid="ignore", divide="ignore"):
        value = np.sum(np.log(x - 2) ** 2 + np.log(10 - x) ** 2) - np.prod(x) ** 0.2
    return float(value)


def PeriodicFunction(x):
    # Jamil & Yang: f = 1 + sum(sin^2 x_i) - 0.1*exp(-sum x_i^2), min = 0.9
    x = np.asarray(x, dtype=float)
    return float(1 + np.sum(np.sin(x) ** 2) - 0.1 * np.exp(-np.sum(x**2)))


def PermDBetaFunction(x):
    x = np.asarray(x, dtype=float)
    D = x.size
    j = np.arange(1, D + 1, dtype=float)
    total = 0.0
    for i in range(1, D + 1):
        total += np.sum((j**i + 10) * ((x / j) ** i - 1)) ** 2
    return float(total)


def Perm0DBetaFunction(x):
    x = np.asarray(x, dtype=float)
    D = x.size
    j = np.arange(1, D + 1, dtype=float)
    total = 0.0
    for i in range(1, D + 1):
        total += np.sum((j + 10) * (x**i - 1 / j**i)) ** 2
    return float(total)


def PowellFunction(x):
    x = np.asarray(x, dtype=float)
    i = np.arange(1, x.size + 1, dtype=float)
    return float(np.sum(np.abs(x) ** (i + 1)))


def QingFunction(x):
    x = np.asarray(x, dtype=float)
    i = np.arange(1, x.size + 1, dtype=float)
    return float(np.sum((x**2 - i) ** 2))


def QuarticFunction(x):
    x = np.asarray(x, dtype=float)
    i = np.arange(1, x.size + 1, dtype=float)
    # Manuscript draws np.random.random() from the global legacy stream.
    # The companion uses the separate benchmark-noise generator.
    return float(np.sum(i * x**4) + uniform_noise())


def QuinticFunction(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(np.abs(x**5 - 3 * x**4 + 4 * x**3 + 2 * x**2 - 10 * x - 4)))


def RastriginFunction(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(x**2 - 10 * np.cos(2 * np.pi * x) + 10))


def RosenbrockFunction(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(100 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2))


def RotatedHyperEllipsoidFunction(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(np.cumsum(x**2)))


def SalomonFunction(x):
    x = np.asarray(x, dtype=float)
    r = np.sqrt(np.sum(x**2))
    return float(1 - np.cos(2 * np.pi * r) + 0.1 * r)


def Schwefel12Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(np.cumsum(x) ** 2))


def Schwefel24Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum((x - 1) ** 2 + (x[0] - x**2) ** 2))


def Schwefel220Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(np.abs(x)))


def Schwefel221Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.max(np.abs(x)))


def Schwefel222Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(np.abs(x)) + np.prod(np.abs(x)))


def Schwefel223Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(x**10))


def Schwefel226Function(x):
    x = np.asarray(x, dtype=float)
    return float(-np.sum(x * np.sin(np.sqrt(np.abs(x)))) / x.size)


def ShubertFunction(x):
    # Jamil & Yang: prod_i sum_j j*cos((j+1)x_i + j)
    x = np.asarray(x, dtype=float)
    j = np.arange(1, 6, dtype=float)
    return float(np.prod([np.sum(j * np.cos((j + 1) * xi + j)) for xi in x]))


def Shubert3Function(x):
    x = np.asarray(x, dtype=float)
    j = np.arange(1, 6, dtype=float)
    return float(np.sum([np.sum(j * np.sin((j + 1) * xi + j)) for xi in x]))


def Shubert4Function(x):
    x = np.asarray(x, dtype=float)
    j = np.arange(1, 6, dtype=float)
    return float(np.sum([np.sum(j * np.cos((j + 1) * xi + j)) for xi in x]))


def SphericalFunction(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(x**2))


def StretchedVSineWaveFunction(x):
    x = np.asarray(x, dtype=float)
    r2 = x[:-1] ** 2 + x[1:] ** 2
    return float(np.sum(r2**0.25 * (np.sin(50 * r2**0.1) ** 2 + 0.1)))


def StyblinskiTangFunction(x):
    x = np.asarray(x, dtype=float)
    return float(0.5 * np.sum(x**4 - 16 * x**2 + 5 * x))


def SumSquaresFunction(x):
    x = np.asarray(x, dtype=float)
    i = np.arange(1, x.size + 1, dtype=float)
    return float(np.sum(i * x**2))


def TridFunction(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum((x - 1) ** 2) - np.sum(x[1:] * x[:-1]))


def Trigonometric1Function(x):
    # Jamil & Yang: sum_i [D - sum_j cos x_j + i*(1 - cos x_i - sin x_i)]^2
    x = np.asarray(x, dtype=float)
    D = x.size
    i = np.arange(1, D + 1, dtype=float)
    return float(np.sum((D - np.sum(np.cos(x)) + i * (1 - np.cos(x) - np.sin(x))) ** 2))


def Trigonometric2Function(x):
    # Jamil & Yang: 1 + sum [8 sin^2(7(x_i-0.9)^2) + 6 sin^2(14(x_i-0.9)^2) + (x_i-0.9)^2]
    x = np.asarray(x, dtype=float)
    return float(1 + np.sum(8 * np.sin(7 * (x - 0.9) ** 2) ** 2 + 6 * np.sin(14 * (x - 0.9) ** 2) ** 2 + (x - 0.9) ** 2))


def WavyFunction(x):
    x = np.asarray(x, dtype=float)
    return float(1 - np.sum(np.cos(10 * x) * np.exp(-(x**2) / 2)) / x.size)


def WeierstrassFunction(x):
    # Jamil & Yang: sum_i sum_k a^k cos(2 pi b^k (x_i+0.5)) - D * sum_k a^k cos(pi b^k)
    x = np.asarray(x, dtype=float)
    k = np.arange(0, 21, dtype=float)
    first = np.sum((0.5**k)[:, None] * np.cos(2 * np.pi * (3**k)[:, None] * (x[None, :] + 0.5)))
    second = x.size * np.sum((0.5**k) * np.cos(np.pi * (3**k)))
    return float(first - second)


def WhitleyFunction(x):
    # Jamil & Yang: sum_i sum_j [y^2/4000 - cos(y) + 1],  y = 100(x_i^2-x_j)^2 + (1-x_j)^2
    x = np.asarray(x, dtype=float)
    q = 100 * (x[:, None] ** 2 - x[None, :]) ** 2 + (1 - x[None, :]) ** 2
    return float(np.sum(q**2 / 4000 - np.cos(q) + 1))


def XinSheYangFunction(x):
    x = np.asarray(x, dtype=float)
    i = np.arange(1, x.size + 1, dtype=float)
    return float(np.sum(uniform_noise(x.size) * np.abs(x) ** i))


def XinSheYang2Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(np.abs(x)) * np.exp(-np.sum(np.sin(x**2))))


def XinSheYang3Function(x):
    x = np.asarray(x, dtype=float)
    return float(np.exp(-np.sum((x / 15) ** 10)) - 2 * np.exp(-np.sum(x**2)) * np.prod(np.cos(x) ** 2))


def XinSheYang4Function(x):
    # Jamil & Yang: [sum sin^2 x_i - exp(-sum x_i^2)] * exp(-sum sin^2 sqrt|x_i|), min = -1
    x = np.asarray(x, dtype=float)
    return float((np.sum(np.sin(x) ** 2) - np.exp(-np.sum(x**2))) * np.exp(-np.sum(np.sin(np.sqrt(np.abs(x))) ** 2)))


def ZakharovFunction(x):
    x = np.asarray(x, dtype=float)
    i = np.arange(1, x.size + 1, dtype=float)
    s = 0.5 * np.sum(i * x)
    return float(np.sum(x**2) + s**2 + s**4)


def _domain(lo, hi, n):
    return [[float(lo), float(hi)] for _ in range(n)]


def make_benchmark_vars(n, prefix="x"):
    return [f"{prefix}{i}" for i in range(1, n + 1)]


BENCHMARKS = [
    ("Ackley No. 1", Ackley1Function, (-32, 32)),
    ("Ackley No. 4", Ackley4Function, (-35, 35)),
    ("Alpine No. 1", Alpine1Function, (-10, 10)),
    ("Alpine No. 2", Alpine2Function, (0, 10)),
    ("Brown", BrownFunction, (-1, 1)),
    ("Chung-Reynolds", ChungReynoldsFunction, (-100, 100)),
    ("Cosine Mixture", CosineMixtureFunction, (-1, 1)),
    ("Deb No. 1", Deb1Function, (-1, 1)),
    ("Deb No. 3", Deb3Function, (0, 1)),
    ("Dixon-Price", DixonAndPriceFunction, (-10, 10)),
    ("Egg Holder", EggHolderFunction, (-512, 512)),
    ("Elliptic", EllipticFunction, (-0.5, 0.5)),
    ("Exponential", ExponentialFunction, (-1, 1)),
    ("Griewank", GriewankFunction, (-600, 600)),
    ("Happy Cat", HappyCatFunction, (-2, 2)),
    ("Levy", LevyFunction, (-10, 10)),
    ("Michalewicz", MichalewiczFunction, (0, np.pi)),
    ("Paviani", PavianiFunction, (2.0001, 9.9999)),
    ("Periodic", PeriodicFunction, (-10, 10)),
    ("Perm d, beta", PermDBetaFunction, (-1, 1)),  # bounds set in benchmark_domain
    ("Perm 0 d, beta", Perm0DBetaFunction, (-1, 1)),  # bounds set in benchmark_domain
    ("Powell", PowellFunction, (-1, 1)),
    ("Qing", QingFunction, (-500, 500)),
    ("Quartic", QuarticFunction, (-1.28, 1.28)),
    ("Quintic", QuinticFunction, (-10, 10)),
    ("Rastrigin", RastriginFunction, (-5.12, 5.12)),
    ("Rosenbrock", RosenbrockFunction, (-30, 30)),
    ("Rotated Hyper Ellipsoid", RotatedHyperEllipsoidFunction, (-65.536, 65.536)),
    ("Salomon", SalomonFunction, (-100, 100)),
    ("Schwefel No. 1.2", Schwefel12Function, (-100, 100)),
    ("Schwefel No. 2.4", Schwefel24Function, (-100, 100)),
    ("Schwefel No. 2.20", Schwefel220Function, (-100, 100)),
    ("Schwefel No. 2.21", Schwefel221Function, (-100, 100)),
    ("Schwefel No. 2.22", Schwefel222Function, (-100, 100)),
    ("Schwefel No. 2.23", Schwefel223Function, (-10, 10)),
    ("Schwefel No. 2.26", Schwefel226Function, (-500, 500)),
    ("Shubert", ShubertFunction, (-10, 10)),
    ("Shubert No. 3", Shubert3Function, (-10, 10)),
    ("Shubert No. 4", Shubert4Function, (-10, 10)),
    ("Spherical", SphericalFunction, (-10, 10)),
    ("Stretched V Sine Wave", StretchedVSineWaveFunction, (-10, 10)),
    ("Styblinski-Tang", StyblinskiTangFunction, (-10, 10)),
    ("Sum of Squares", SumSquaresFunction, (-10, 10)),
    ("Trid", TridFunction, None),  # [-D^2, D^2]
    ("Trigonometric No. 1", Trigonometric1Function, None),  # [0, i*pi]
    ("Trigonometric No. 2", Trigonometric2Function, (-500, 500)),
    ("Wavy", WavyFunction, (-np.pi, np.pi)),
    ("Weierstrass", WeierstrassFunction, (-0.5, 0.5)),
    ("Whitley", WhitleyFunction, (0, 2)),
    ("Xin-She Yang", XinSheYangFunction, (-5, 5)),
    ("Xin-She Yang No. 2", XinSheYang2Function, (-2 * np.pi, 2 * np.pi)),
    ("Xin-She Yang No. 3", XinSheYang3Function, (-20, 20)),
    ("Xin-She Yang No. 4", XinSheYang4Function, (-10, 10)),
    ("Zakharov", ZakharovFunction, (-5, 10)),
]


def benchmark_domain(index, dimension):
    name, _, bounds = BENCHMARKS[index]
    if dimension < 1:
        raise ValueError("dimension must be >= 1")
    if name in ("Perm d, beta", "Perm 0 d, beta"):
        return _domain(-dimension, dimension, dimension)
    if name == "Trid":
        return _domain(-(dimension**2), dimension**2, dimension)
    if name == "Trigonometric No. 1":
        return [[0.0, i * np.pi] for i in range(1, dimension + 1)]
    if bounds is None:
        raise ValueError(f"no rectangular domain is registered for {name}")
    return _domain(bounds[0], bounds[1], dimension)


def get_benchmark(name: str) -> tuple:
    """Return ``(name, function, raw_bounds)`` for a Table 4.1 benchmark name."""

    for item in BENCHMARKS:
        if item[0] == name:
            return item
    known = ", ".join(item[0] for item in BENCHMARKS)
    raise KeyError(f"unknown benchmark {name!r}. Known names: {known}")


def benchmark_names() -> list[str]:
    return [item[0] for item in BENCHMARKS]


def outside_domain(name: str, point: np.ndarray | list[float]) -> np.ndarray:
    """Boolean mask of coordinates outside the registered Appendix B box.

    The box is the closed interval from :func:`benchmark_domain`. Paviani's
    formula is only defined on ``(2, 10)``. The registered Paviani box is
    ``[2.0001, 9.9999]``, which sits inside that open interval. This check
    does not change the function value.
    """

    array = np.asarray(point, dtype=float).reshape(-1)
    if array.size < 1:
        raise ValueError("point must contain at least one coordinate")
    get_benchmark(name)
    index = benchmark_names().index(name)
    domain = np.asarray(benchmark_domain(index, int(array.size)), dtype=float)
    return (array < domain[:, 0]) | (array > domain[:, 1])


def evaluate_benchmark(name: str, point: np.ndarray | list[float], *, strict: bool = False) -> float:
    """Evaluate one Appendix B function and report registered-domain violations.

    ``strict=True`` raises ``ValueError`` when any coordinate is outside the
    box. The default still evaluates the formula, after a ``RuntimeWarning``.
    Elliptic with fewer than two variables still raises from the formula.
    """

    array = np.asarray(point, dtype=float).reshape(-1)
    mask = outside_domain(name, array)
    if np.any(mask):
        message = f"{name}: {int(np.count_nonzero(mask))} coordinate(s) are outside the registered domain"
        if strict:
            raise ValueError(message)
        warnings.warn(message, RuntimeWarning, stacklevel=2)
    function = get_benchmark(name)[1]
    return float(function(array))
