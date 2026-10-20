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
