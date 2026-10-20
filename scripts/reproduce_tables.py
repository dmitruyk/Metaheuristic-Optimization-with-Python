"""Reference-value table for benchmarks whose minima are stated in Table 4.1.

This does not rebuild Appendix C. It evaluates the Appendix B functions at the
locations Table 4.1 names, and writes a CSV under results/.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from metaopt.benchmarks import (
    Ackley1Function,
    Alpine1Function,
    ChungReynoldsFunction,
    ExponentialFunction,
    GriewankFunction,
    HappyCatFunction,
    LevyFunction,
    PeriodicFunction,
    QingFunction,
    QuinticFunction,
    RastriginFunction,
    RosenbrockFunction,
    SalomonFunction,
    Schwefel220Function,
    Schwefel226Function,
    SphericalFunction,
    StyblinskiTangFunction,
    SumSquaresFunction,
    Trigonometric2Function,
    WavyFunction,
    XinSheYang3Function,
    XinSheYang4Function,
    ZakharovFunction,
)

ROOT = Path(__file__).resolve().parents[1]
SCHWEFEL = 420.968746359982015


def main() -> None:
    rows = []

    def add(name, point, value, printed):
        rows.append(
            {
                "benchmark": name,
                "observed": value,
                "printed": printed,
                "absolute_difference": abs(value - printed) if printed is not None else "",
            }
        )
        del point

    dimension = 4
    zeros = np.zeros(dimension)
    ones = np.ones(dimension)
    checks = [
        ("Spherical", zeros, SphericalFunction(zeros), 0.0),
        ("Ackley No. 1", zeros, Ackley1Function(zeros), 0.0),
        ("Alpine No. 1", zeros, Alpine1Function(zeros), 0.0),
        ("Chung-Reynolds", zeros, ChungReynoldsFunction(zeros), 0.0),
        ("Exponential", zeros, ExponentialFunction(zeros), -1.0),
        ("Griewank", zeros, GriewankFunction(zeros), 0.0),
        ("Happy Cat", -ones, HappyCatFunction(-ones), 0.0),
        ("Levy", ones, LevyFunction(ones), 0.0),
        ("Periodic", zeros, PeriodicFunction(zeros), 0.9),
        ("Rastrigin", zeros, RastriginFunction(zeros), 0.0),
        ("Rosenbrock", ones, RosenbrockFunction(ones), 0.0),
        ("Salomon", zeros, SalomonFunction(zeros), 0.0),
        ("Schwefel No. 2.20", zeros, Schwefel220Function(zeros), 0.0),
        ("Sum of Squares", zeros, SumSquaresFunction(zeros), 0.0),
        ("Wavy", zeros, WavyFunction(zeros), 0.0),
        ("Xin-She Yang No. 3", zeros, XinSheYang3Function(zeros), -1.0),
        ("Xin-She Yang No. 4", zeros, XinSheYang4Function(zeros), -1.0),
        ("Zakharov", zeros, ZakharovFunction(zeros), 0.0),
        ("Quintic at -1", -ones, QuinticFunction(-ones), 0.0),
        ("Trigonometric No. 2", np.full(dimension, 0.9), Trigonometric2Function(np.full(dimension, 0.9)), 1.0),
        (
            "Schwefel No. 2.26",
            np.full(dimension, SCHWEFEL),
            Schwefel226Function(np.full(dimension, SCHWEFEL)),
            -418.9828872724338,
        ),
        (
            "Styblinski-Tang",
            np.full(dimension, -2.903534),
            StyblinskiTangFunction(np.full(dimension, -2.903534)),
            -39.165990 * dimension,
        ),
        (
            "Qing",
            np.sqrt(np.arange(1, dimension + 1, dtype=float)),
            QingFunction(np.sqrt(np.arange(1, dimension + 1, dtype=float))),
            0.0,
        ),
    ]
    for name, point, value, printed in checks:
        add(name, point, value, printed)
    destination = ROOT / "results" / "reference_minima.csv"
    destination.parent.mkdir(exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["benchmark", "observed", "printed", "absolute_difference"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {destination}")


if __name__ == "__main__":
    main()
