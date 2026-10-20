"""Compare the handbook DE/rand/1/bin with SciPy's differential evolution.

Both runs use the same sphere problem, the same seed, and the same
evaluation budget. Histories are not expected to match: SciPy is a different
algorithm and a different implementation.
"""

from __future__ import annotations

import numpy as np

from metaopt.de import minimize, scipy_minimize


def sphere(x: np.ndarray) -> float:
    return float(np.sum(np.asarray(x, dtype=float) ** 2))


def main() -> None:
    bounds = [[-5.0, 5.0]] * 4
    handbook = minimize(sphere, bounds, seed=12345, population_size=12, max_evaluations=120)
    scipy_result = scipy_minimize(sphere, bounds, seed=12345, population_size=12, max_evaluations=120)
    print(f"handbook DE/rand/1/bin  fun={handbook.fun:.6e} nfev={handbook.nfev} seed={handbook.seed}")
    print(f"scipy differential_evolution  fun={scipy_result.fun:.6e} nfev={scipy_result.nfev}")
    print("These objective values are not a reproduction of a handbook table.")


if __name__ == "__main__":
    main()
