"""Run a short seeded PSO on the pressure-vessel listing and report feasibility.

The search budget is intentionally small. A nonzero penalty is reported as
infeasibility rather than treated as a design recommendation.
"""

from __future__ import annotations

from metaopt.api import Bounds
from metaopt.applications.engineering_design import pressure_vessel_components
from metaopt.pso import minimize


def main() -> None:
    bounds = Bounds.from_pairs([[1, 99], [1, 99], [10, 200], [10, 200]])
    result = minimize(
        pressure_vessel_components_value,
        bounds,
        seed=12345,
        population_size=12,
        iterations=8,
    )
    details = pressure_vessel_components(result.x)
    print(f"seed={result.seed} nfev={result.nfev} fun={details['fun']:.6g}")
    print(f"feasible={details['feasible']} penalty={details['penalty']:.6g}")
    print(f"Ts={details['Ts']:.4f} in  Th={details['Th']:.4f} in  R,L={result.x[2:]}")
    if not details["feasible"]:
        print("infeasible: at least one pressure-vessel penalty is positive")
    print(result.message)


def pressure_vessel_components_value(x):
    return pressure_vessel_components(x)["fun"]


if __name__ == "__main__":
    main()
