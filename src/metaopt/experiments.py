"""Equal-budget comparisons.

The Chapter 5 protocol runs 14 algorithms for 500 iterations with population
25, which is not the same number of objective evaluations for GWOEPD or for
ME-D-PSO when it stops early. :func:`compare` gives every algorithm the same
``max_evaluations`` and the same seed so the comparison is by objective calls.
"""

from __future__ import annotations

import time
from collections.abc import Callable

import numpy as np

from metaopt import de, gwo, pso
from metaopt.api import OptimizationResult
from metaopt.variants import (
    bb_pso_minimize,
    gwoepd_minimize,
    ia_pso_minimize,
    ldw_pso_minimize,
    med_pso_minimize,
    mgwo_minimize,
    ring_pso_minimize,
    sade_minimize,
    vct_pso_minimize,
    von_neumann_pso_minimize,
)

Minimizer = Callable[..., OptimizationResult]

HANDBOOK_ALGORITHMS: dict[str, Minimizer] = {
    "PSO": pso.minimize,
    "LDW-PSO": ldw_pso_minimize,
    "IA-PSO": ia_pso_minimize,
    "BB-PSO": bb_pso_minimize,
    "VCT-PSO": vct_pso_minimize,
    "ME-D-PSO": med_pso_minimize,
    "Ring-PSO": ring_pso_minimize,
    "vN-PSO": von_neumann_pso_minimize,
    "DE/best": de.minimize_best,
    "DE/rand": de.minimize,
    "SADE": sade_minimize,
    "GWO": gwo.minimize,
    "mGWO": mgwo_minimize,
    "GWOEPD": gwoepd_minimize,
}


def compare(
    objective,
    bounds,
    algorithms: dict[str, Minimizer] | None = None,
    *,
    seed: int = 12345,
    population_size: int = 25,
    max_evaluations: int = 500,
    value_tolerance: float = 0.0,
) -> list[dict]:
    """Run each algorithm from ``seed`` under the same evaluation budget.

    ``value_tolerance`` is recorded on each row so a later check can say
    whether two objective values agree. It does not change the run.
    """

    selected = HANDBOOK_ALGORITHMS if algorithms is None else algorithms
    rows = []
    for name, minimizer in selected.items():
        kwargs = {
            "seed": seed,
            "population_size": population_size,
            "max_evaluations": max_evaluations,
        }
        if name == "vN-PSO":
            side = int(round(np.sqrt(population_size)))
            if side * side != population_size:
                rows.append(
                    {
                        "algorithm": name,
                        "success": False,
                        "message": "skipped: von Neumann PSO needs a square population",
                        "fun": float("nan"),
                        "nfev": 0,
                        "seconds": 0.0,
                        "seed": seed,
                        "max_evaluations": max_evaluations,
                        "value_tolerance": value_tolerance,
                    }
                )
                continue
        started = time.perf_counter()
        result = minimizer(objective, bounds, **kwargs)
        elapsed = time.perf_counter() - started
        rows.append(
            {
                "algorithm": name,
                "fun": result.fun,
                "nfev": result.nfev,
                "success": result.success,
                "feasible": result.feasible,
                "message": result.message,
                "seconds": elapsed,
                "seed": result.seed,
                "max_evaluations": max_evaluations,
                "history_length": len(result.history),
                "value_tolerance": value_tolerance,
            }
        )
    return rows


def summarize_groups(rows: list[dict]) -> list[dict]:
    """Median, extrema, mean, and sample standard deviation for labeled runs.

    Rows need ``algorithm``, ``benchmark``, ``fun``, ``nfev``, and ``seconds``.
    The sample standard deviation uses ``ddof=1``. A single run records 0.
    This summary does not compare the rows with a printed table.
    """

    grouped: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        grouped.setdefault((str(row["algorithm"]), str(row["benchmark"])), []).append(row)
    summary = []
    for (algorithm, benchmark), items in grouped.items():
        values = np.asarray([float(item["fun"]) for item in items], dtype=float)
        evaluations = np.asarray([float(item["nfev"]) for item in items], dtype=float)
        sample_std = float(np.std(values, ddof=1)) if values.size > 1 else 0.0
        summary.append(
            {
                "algorithm": algorithm,
                "benchmark": benchmark,
                "runs": int(values.size),
                "median": float(np.median(values)),
                "minimum": float(np.min(values)),
                "maximum": float(np.max(values)),
                "mean": float(np.mean(values)),
                "sample_std": sample_std,
                "median_nfev": float(np.median(evaluations)),
                "total_seconds": float(sum(float(item["seconds"]) for item in items)),
            }
        )
    return summary


def rank_by_median(summary: list[dict]) -> list[dict]:
    """Rank algorithms inside each benchmark by ascending median.

    Ties share the best rank in the tie (1, 2, 2, 4). The rank is for a
    minimization summary produced by :func:`summarize_groups`. It does not
    reproduce a printed Chapter 5 or Appendix C rank table.
    """

    grouped: dict[str, list[dict]] = {}
    for row in summary:
        grouped.setdefault(str(row["benchmark"]), []).append(row)
    ranked = []
    for benchmark, items in grouped.items():
        ordered = sorted(items, key=lambda item: (float(item["median"]), str(item["algorithm"])))
        previous = None
        previous_rank = 0
        for index, item in enumerate(ordered, start=1):
            median = float(item["median"])
            if previous is not None and median == previous:
                rank = previous_rank
            else:
                rank = index
                previous_rank = index
            previous = median
            ranked.append({**item, "benchmark": benchmark, "median_rank": rank})
    return ranked
