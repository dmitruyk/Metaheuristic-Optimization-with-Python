"""Experiment profiles for the handbook companion.

Appendix C and Appendix E in the manuscript were seeded with
``np.random.seed`` (legacy ``RandomState``). Profiles in this module use
``numpy.random.Generator`` and set ``matches_appendix_c`` and
``matches_appendix_e`` to false. A quick run is a smoke test. The full
profile describes the manuscript protocol and is not executed unless a caller
passes an explicit confirmation after reading the cost estimate.
"""

from __future__ import annotations

import time
from typing import Any

from metaopt.benchmarks import RastriginFunction, SphericalFunction, benchmark_names, seed_benchmark_noise
from metaopt.experiments import HANDBOOK_ALGORITHMS, rank_by_median, summarize_groups

# Appendix B cell "SETTINGS AND RUN - ALGORITHMS SEARCH PERFORMANCE".
HISTORICAL_APPENDIX_C: dict[str, Any] = {
    "label": "appendix-c-historical-randomstate",
    "status": "historical",
    "matches_appendix_c": False,
    "matches_appendix_e": False,
    "rng": "numpy.random.RandomState via np.random.seed",
    "dimension": 30,
    "population_size": 25,
    "iterations": 500,
    "runs": 100,
    "base_seed": 12345,
    "seed_formula": "BASE_SEED + 100000 * problem_index + 1000 * algorithm_index + run",
    "acceptable_rate": 5e-3,
    "algorithms": list(HANDBOOK_ALGORITHMS),
    "benchmarks": benchmark_names(),
    "stopping": "iteration count, not a shared evaluation budget",
    "source": "Editorial DOCX Appendix B performance cell and Chapter 5 prose (D=30)",
}

# Appendix B cell "SETTINGS AND RUN - ALGORITHMS EXECUTION TIME".
HISTORICAL_APPENDIX_E: dict[str, Any] = {
    "label": "appendix-e-historical-randomstate",
    "status": "historical",
    "matches_appendix_c": False,
    "matches_appendix_e": False,
    "rng": "numpy.random.RandomState via np.random.seed",
    "dimension": 30,
    "population_size": 25,
    "iterations": 500,
    "runs": 20,
    "base_seed": 12345,
    "seed_formula": "BASE_SEED + 100000 * problem_index + 1000 * algorithm_index + run",
    "acceptable_rate": 5e-3,
    "time_metric": "wall and cpu",
    "parallel": False,
    "algorithms": list(HANDBOOK_ALGORITHMS),
    "benchmarks": benchmark_names(),
    "source": "Editorial DOCX Appendix B timing cell (Runs = 20) and Appendix E prose",
}

QUICK_PROFILE: dict[str, Any] = {
    "label": "quick-validation",
    "matches_appendix_c": False,
    "matches_appendix_e": False,
    "reason_not_the_handbook_study": (
        "Three of fourteen algorithms, two of fifty-four benchmarks, two runs, "
        "dimension 5, population 8, and 64 objective evaluations. Random numbers "
        "come from numpy.random.Generator, not from np.random.seed."
    ),
    "rng": "numpy.random.Generator (PCG64 via numpy.random.default_rng)",
    "dimension": 5,
    "population_size": 8,
    "max_evaluations": 64,
    "iterations": None,
    "runs": 2,
    "base_seed": 12345,
    "noise_seed": 0,
    "algorithms": ["PSO", "DE/rand", "GWO"],
    "benchmarks": ["Spherical", "Rastrigin"],
    "bounds": [-5.12, 5.12],
}

_QUICK_FUNCTIONS = {
    "Spherical": SphericalFunction,
    "Rastrigin": RastriginFunction,
}


def full_generator_protocol() -> dict[str, Any]:
    """Manuscript sizes with a Generator, still not a printed-table reproduction."""

    protocol = {
        "label": "full-generator-protocol",
        "matches_appendix_c": False,
        "matches_appendix_e": False,
        "rng": "numpy.random.Generator (PCG64 via numpy.random.default_rng)",
        "historical_rng": HISTORICAL_APPENDIX_C["rng"],
        "dimension": HISTORICAL_APPENDIX_C["dimension"],
        "population_size": HISTORICAL_APPENDIX_C["population_size"],
        "iterations": HISTORICAL_APPENDIX_C["iterations"],
        "runs": HISTORICAL_APPENDIX_C["runs"],
        "base_seed": HISTORICAL_APPENDIX_C["base_seed"],
        "seed_formula": HISTORICAL_APPENDIX_C["seed_formula"],
        "acceptable_rate": HISTORICAL_APPENDIX_C["acceptable_rate"],
        "algorithms": list(HISTORICAL_APPENDIX_C["algorithms"]),
        "benchmarks": list(HISTORICAL_APPENDIX_C["benchmarks"]),
        "stopping": (
            "The manuscript stops on iteration count. This profile would do the same "
            "and record nfev. GWOEPD and early-stopped ME-D-PSO therefore do not share "
            "one evaluation budget with PSO."
        ),
        "statement": (
            "A completed run of this profile would be a new Generator experiment with "
            "the manuscript's sizes. It would not reproduce Appendix C, because the "
            "handbook seeded the legacy RandomState."
        ),
    }
    return protocol


def iter_full_jobs():
    """Yield one manuscript-sized job description per run. Does not evaluate it.

    Seeds follow the Appendix B formula. The random stream is recorded as
    ``Generator`` so a later executor cannot be confused with ``np.random.seed``.
    """

    protocol = full_generator_protocol()
    for problem_index, benchmark in enumerate(protocol["benchmarks"]):
        for algorithm_index, algorithm in enumerate(protocol["algorithms"]):
            for run in range(int(protocol["runs"])):
                seed = int(protocol["base_seed"]) + 100000 * problem_index + 1000 * algorithm_index + run
                yield {
                    "benchmark": benchmark,
                    "algorithm": algorithm,
                    "run": run,
                    "seed": seed,
                    "dimension": protocol["dimension"],
                    "population_size": protocol["population_size"],
                    "iterations": protocol["iterations"],
                    "rng": "numpy.random.Generator",
                    "matches_appendix_c": False,
                    "matches_appendix_e": False,
                }


def estimate_full_cost() -> dict[str, Any]:
    """Count objective evaluations for the full Generator protocol. Does not run it.

    The count uses ``population_size * iterations`` per run. GWOEPD adds about
    half a pack on every generation after the first, and ME-D-PSO can stop
    early, so the count is a lower bound for GWOEPD and an upper bound for
    ME-D-PSO. The hour range uses per-evaluation timings measured on one
    Mac on 2026-10-19 for sphere-like and Shubert-like functions at dimension 30.
    """

    protocol = full_generator_protocol()
    population = int(protocol["population_size"])
    iterations = int(protocol["iterations"])
    runs = int(protocol["runs"])
    n_algorithms = len(protocol["algorithms"])
    n_benchmarks = len(protocol["benchmarks"])
    evaluations_per_run = population * iterations
    runs_total = n_algorithms * n_benchmarks * runs
    evaluations = runs_total * evaluations_per_run
    # 2026-10-19 local timing: PSO on the sphere did about 3e4 evaluations/s
    # including the optimizer. Shubert at D=30 was about 225 microseconds per
    # bare evaluation, near 4e3 evaluations/s once optimizer overhead is included.
    return {
        "protocol": protocol["label"],
        "matches_appendix_c": False,
        "matches_appendix_e": False,
        "algorithms": n_algorithms,
        "benchmarks": n_benchmarks,
        "runs_total": runs_total,
        "evaluations_per_run_nominal": evaluations_per_run,
        "objective_evaluations_nominal": evaluations,
        "seconds_if_30000_evaluations_per_second": evaluations / 30000,
        "seconds_if_4000_evaluations_per_second": evaluations / 4000,
        "hour_range": [evaluations / 30000 / 3600, evaluations / 4000 / 3600],
        "timing_runs_if_same_rate": {
            "appendix_e_runs": n_algorithms * n_benchmarks * int(HISTORICAL_APPENDIX_E["runs"]),
            "hour_range": [
                n_algorithms * n_benchmarks * int(HISTORICAL_APPENDIX_E["runs"]) * evaluations_per_run / 30000 / 3600,
                n_algorithms * n_benchmarks * int(HISTORICAL_APPENDIX_E["runs"]) * evaluations_per_run / 4000 / 3600,
            ],
        },
        "statement": (
            "Nominal count is 14 * 54 * 100 * 25 * 500 = 945000000 objective "
            "evaluations before GWOEPD's extra half-pack evaluations. Do not describe "
            "a smaller run as Appendix C or Appendix E."
        ),
    }


def run_quick() -> dict[str, Any]:
    """Equal-budget smoke study. Not Appendix C and not Appendix E."""

    profile = QUICK_PROFILE
    seed_benchmark_noise(int(profile["noise_seed"]))
    selected = {name: HANDBOOK_ALGORITHMS[name] for name in profile["algorithms"]}
    functions = {name: _QUICK_FUNCTIONS[name] for name in profile["benchmarks"]}
    bounds = [list(profile["bounds"])] * int(profile["dimension"])
    started = time.perf_counter()
    rows = []
    for run in range(int(profile["runs"])):
        seed = int(profile["base_seed"]) + run
        for benchmark, function in functions.items():
            for algorithm, minimizer in selected.items():
                t0 = time.perf_counter()
                result = minimizer(
                    function,
                    bounds,
                    seed=seed,
                    population_size=int(profile["population_size"]),
                    max_evaluations=int(profile["max_evaluations"]),
                )
                rows.append(
                    {
                        "experiment": profile["label"],
                        "matches_appendix_c": False,
                        "matches_appendix_e": False,
                        "algorithm": algorithm,
                        "benchmark": benchmark,
                        "run": run,
                        "seed": seed,
                        "fun": result.fun,
                        "nfev": result.nfev,
                        "seconds": time.perf_counter() - t0,
                        "dimension": profile["dimension"],
                        "population_size": profile["population_size"],
                        "max_evaluations": profile["max_evaluations"],
                        "rng": "numpy.random.Generator",
                    }
                )
    summary = summarize_groups(rows)
    return {
        "protocol": profile,
        "elapsed_seconds": time.perf_counter() - started,
        "summary": summary,
        "ranks": rank_by_median(summary),
        "rows": rows,
        "statement": ("Quick validation only. These numbers are not Appendix C or Appendix E."),
    }
