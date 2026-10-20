"""Small equal-budget study. This is not Appendix C and not Appendix E.

The handbook study is 14 algorithms, 54 benchmarks, 100 runs, dimension 30,
population 25, and 500 iterations, seeded with ``np.random.seed(12345)``.
That legacy stream is not replayed here. This script runs three algorithms
on two functions so a machine-readable summary can be stored without claiming
that the printed tables were reproduced.
"""

from __future__ import annotations

import json
import os
import platform
import time
from pathlib import Path

import numpy as np

from metaopt import __version__
from metaopt.benchmarks import RastriginFunction, SphericalFunction, seed_benchmark_noise
from metaopt.de import minimize as de_minimize
from metaopt.experiments import summarize_groups
from metaopt.gwo import minimize as gwo_minimize
from metaopt.pso import minimize as pso_minimize

ROOT = Path(__file__).resolve().parents[1]
ALGORITHMS = {
    "PSO": pso_minimize,
    "DE/rand": de_minimize,
    "GWO": gwo_minimize,
}
BENCHMARKS = {
    "Spherical": SphericalFunction,
    "Rastrigin": RastriginFunction,
}
PROTOCOL = {
    "label": "reduced-generator-study",
    "matches_appendix_c": False,
    "matches_appendix_e": False,
    "reason_not_the_handbook_study": (
        "Three of fourteen algorithms, two of fifty-four benchmarks, five runs, "
        "dimension 5, population 8, and 64 objective evaluations. Random numbers "
        "come from numpy.random.Generator, not from np.random.seed."
    ),
    "dimension": 5,
    "population_size": 8,
    "max_evaluations": 64,
    "runs": 5,
    "base_seed": 12345,
    "rng": "numpy.random.Generator (PCG64 via numpy.random.default_rng)",
    "noise_seed": None,
    "algorithms": list(ALGORITHMS),
    "benchmarks": list(BENCHMARKS),
}


def _row(algorithm: str, benchmark: str, run: int, seed: int, result, seconds: float) -> dict:
    return {
        "experiment": PROTOCOL["label"],
        "matches_appendix_c": False,
        "matches_appendix_e": False,
        "algorithm": algorithm,
        "benchmark": benchmark,
        "run": run,
        "seed": seed,
        "fun": result.fun,
        "nfev": result.nfev,
        "seconds": seconds,
        "dimension": PROTOCOL["dimension"],
        "population_size": PROTOCOL["population_size"],
        "max_evaluations": PROTOCOL["max_evaluations"],
    }


def main() -> None:
    started = time.perf_counter()
    seed_benchmark_noise(0)
    rows = []
    dimension = PROTOCOL["dimension"]
    bounds = [[-5.12, 5.12]] * dimension
    for run in range(PROTOCOL["runs"]):
        seed = PROTOCOL["base_seed"] + run
        for benchmark, function in BENCHMARKS.items():
            for algorithm, minimizer in ALGORITHMS.items():
                t0 = time.perf_counter()
                result = minimizer(
                    function,
                    bounds,
                    seed=seed,
                    population_size=PROTOCOL["population_size"],
                    max_evaluations=PROTOCOL["max_evaluations"],
                )
                rows.append(_row(algorithm, benchmark, run, seed, result, time.perf_counter() - t0))
    summary = summarize_groups(rows)
    payload = {
        "protocol": PROTOCOL,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "metaopt": __version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
        },
        "elapsed_seconds": time.perf_counter() - started,
        "summary": summary,
        "rows": rows,
        "statement": (
            "These numbers are a new reduced experiment. They are not a reproduction "
            "of Appendix C or Appendix E and must not be substituted for the printed tables."
        ),
    }
    text = json.dumps(payload, indent=2) + "\n"
    destination = ROOT / "results" / "reduced_comparison_summary.json"
    versioned = ROOT / "results" / f"reduced_comparison_py{platform.python_version()}.json"
    destination.write_text(text, encoding="utf-8")
    versioned.write_text(text, encoding="utf-8")
    csv_path = ROOT / "results" / "reduced_comparison_summary.csv"
    header = ["algorithm", "benchmark", "runs", "median", "minimum", "maximum", "mean", "sample_std", "median_nfev", "total_seconds"]
    lines = [",".join(header)]
    for item in summary:
        lines.append(",".join(str(item[column]) for column in header))
    csv_text = "\n".join(lines) + "\n"
    csv_path.write_text(csv_text, encoding="utf-8")
    versioned_csv = ROOT / "results" / f"reduced_comparison_py{platform.python_version()}.csv"
    versioned_csv.write_text(csv_text, encoding="utf-8")
    print(f"wrote {destination}")
    print(f"wrote {versioned}")
    print(f"wrote {csv_path}")
    print(f"wrote {versioned_csv}")
    print(f"elapsed_seconds={payload['elapsed_seconds']:.4f}")
    print(payload["statement"])


if __name__ == "__main__":
    main()
