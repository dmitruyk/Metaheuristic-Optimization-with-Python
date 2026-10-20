"""Write the ten walkthrough notebooks. Run from the repository root."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


def cell(source: str, kind: str = "code") -> dict:
    lines = source.strip("\n").split("\n")
    payload = [line + "\n" for line in lines[:-1]]
    if lines:
        payload.append(lines[-1] + "\n")
    if kind == "markdown":
        return {"cell_type": "markdown", "metadata": {}, "source": payload}
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": payload,
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def write(name: str, cells: list[dict]) -> None:
    path = NOTEBOOKS / name
    path.write_text(json.dumps(notebook(cells), indent=1), encoding="utf-8")
    print(path.name)


def main() -> None:
    NOTEBOOKS.mkdir(exist_ok=True)
    write(
        "01_particle_swarm.ipynb",
        [
            cell(
                """# Chapter 1 — Particle swarm optimization

Canonical PSO from the handbook. The ten-variable worked objective is
`sum of squares + sum of absolute values`. The printed value at the stated point is 12.3901.
Search traces use an explicit NumPy Generator and will not match a run that called `np.random.seed`.
""",
                "markdown",
            ),
            cell(
                """
import numpy as np
from metaopt.pso import minimize

def objective(x):
    x = np.asarray(x, dtype=float)
    return float(np.sum(x**2) + np.sum(np.abs(x)))

point = np.array([0.1, 0.2, 0.3, -0.2, 0.51, -0.2, 0.0, -0.2, -1.6, 2.0])
print(objective(point))

result = minimize(
    objective,
    [[-20.0, 20.0]] * 10,
    seed=1,
    population_size=12,
    iterations=8,
)
print(result.fun, result.nfev, result.message)
""",
            ),
        ],
    )
    write(
        "02_differential_evolution.ipynb",
        [
            cell(
                """# Chapter 2 — Differential evolution

`DE/rand/1/bin` and `DE/best/1/bin` use `CR=0.5` and `F=0.6`. The donor is clipped to the box before crossover.
""",
                "markdown",
            ),
            cell(
                """
import numpy as np
from metaopt.de import minimize, minimize_best

def sphere(x):
    return float(np.sum(np.square(x)))

bounds = [[-5.0, 5.0]] * 4
common = dict(seed=2, population_size=12, max_evaluations=120)
print("rand", minimize(sphere, bounds, **common).fun)
print("best", minimize_best(sphere, bounds, **common).fun)
""",
            ),
        ],
    )
    write(
        "03_grey_wolf_optimizer.ipynb",
        [
            cell(
                """# Chapter 3 — Grey wolf optimizer

`a = 2 - 2 * (step / iterations)` with `step` starting at 2, because the initial pack is generation 1. Positions are clipped to the box.
""",
                "markdown",
            ),
            cell(
                """
import numpy as np
from metaopt.gwo import minimize

def sphere(x):
    return float(np.sum(np.square(x)))

result = minimize(sphere, [[-5.0, 5.0]] * 3, seed=3, population_size=12, iterations=10)
print(result.fun, result.nfev, result.history[-1])
""",
            ),
        ],
    )
    write(
        "04_benchmarks.ipynb",
        [
            cell(
                """# Chapter 4 — Benchmarks

Appendix B defines 54 functions. This notebook checks the printed reference locations that do not depend on a figure. Elliptic is undefined for one variable because the listing divides by `D - 1`.
""",
                "markdown",
            ),
            cell(
                """
import numpy as np
from metaopt.benchmarks import BENCHMARKS, SphericalFunction, RosenbrockFunction, benchmark_domain

print(len(BENCHMARKS))
print(SphericalFunction(np.zeros(4)))
print(RosenbrockFunction(np.ones(5)))
print(benchmark_domain(0, 3))
""",
            ),
        ],
    )
    write(
        "05_fair_comparisons.ipynb",
        [
            cell(
                """# Chapter 5 — Equal evaluation budgets

The handbook's 500-iteration protocol does not give GWOEPD the same number of objective calls as PSO. This notebook gives every listed algorithm the same `max_evaluations`. The sphere values are smoke results, not Appendix C.
""",
                "markdown",
            ),
            cell(
                """
import numpy as np
from metaopt.experiments import compare

def sphere(x):
    return float(np.sum(np.square(x)))

rows = compare(sphere, [[-5.0, 5.0]] * 2, seed=4, population_size=9, max_evaluations=90)
for row in rows:
    print(f"{row['algorithm']:12} fun={row['fun']:.4e} nfev={row['nfev']}")
""",
            ),
        ],
    )
    write(
        "06_pid_tuning.ipynb",
        [
            cell(
                """# Chapter 6 — PID worked values

Problem 1a at `(0.1, 1, 9)` and `(0.276, 0.765, 2.221)`, and Problem 1b at `(0.1, 2, 6)`. Tolerances used by the tests are in `tests/test_examples_smoke.py`.
""",
                "markdown",
            ),
            cell(
                """
from metaopt.applications import pid

print(pid.objective_1a(*pid.WORKED_1A_UNSTABLE))
print(pid.objective_1a(*pid.WORKED_1A_FEASIBLE))
print(pid.objective_1b(*pid.WORKED_1B))
""",
            ),
        ],
    )
    write(
        "07_robot_path_planning.ipynb",
        [
            cell(
                """# Chapter 6 — Mobile robot

The crossing node set is infeasible. The second printed node set stays inside the workspace and outside the obstacles.
""",
                "markdown",
            ),
            cell(
                """
from metaopt.applications import mobile_robot

bad = mobile_robot.path_geometry(mobile_robot.WORKED_INFEASIBLE)
good = mobile_robot.path_geometry(mobile_robot.WORKED_FEASIBLE)
print(bad["fun"], bad["feasible"])
print(good["fun"], good["feasible"])
""",
            ),
        ],
    )
    write(
        "08_crane_control.ipynb",
        [
            cell(
                """# Chapter 6 — Crane polynomial reduction

The first coefficient vector violates the speed bounds. The second does not. The long expression is parenthesized so a line wrap cannot break the sum.
""",
                "markdown",
            ),
            cell(
                """
from metaopt.applications import crane

blocked = crane.polynomial_profiles(crane.WORKED_POLY_INFEASIBLE)
clear = crane.polynomial_profiles(crane.WORKED_POLY_FEASIBLE)
print(blocked["fun"], blocked["feasible"])
print(clear["fun"], clear["feasible"])
""",
            ),
        ],
    )
    write(
        "09_cart_pole.ipynb",
        [
            cell(
                """# Chapter 6 — Mountain car and cart-pole

Smoke checks of the printed one-step maps and the two cart-pole parameter vectors. The terminal penalty stays a parenthesized conditional so it cannot be split into an illegal `else` line.
""",
                "markdown",
            ),
            cell(
                """
from metaopt.applications import cart_pole, mountain_car

print(mountain_car.step(*mountain_car.WORKED_STEP))
print(mountain_car.objective_4a(mountain_car.WORKED_4A_FEASIBLE))
print(cart_pole.step(*cart_pole.WORKED_STEP))
print(cart_pole.simulate(cart_pole.WORKED_FEASIBLE)["feasible"])
print(cart_pole.simulate(cart_pole.WORKED_INFEASIBLE)["feasible"])
""",
            ),
        ],
    )
    write(
        "10_engineering_design.ipynb",
        [
            cell(
                """# Chapter 7 — Design listings

A short PSO run on the pressure vessel. Feasibility is the penalty, not a claim that the known literature optimum was found.
""",
                "markdown",
            ),
            cell(
                """
from metaopt.api import Bounds
from metaopt.applications.engineering_design import pressure_vessel_components
from metaopt.pso import minimize

bounds = Bounds.from_pairs([[1, 99], [1, 99], [10, 200], [10, 200]])
result = minimize(lambda x: pressure_vessel_components(x)["fun"], bounds, seed=11, population_size=8, iterations=4)
details = pressure_vessel_components(result.x)
print(details["fun"], details["feasible"], result.nfev)
""",
            ),
        ],
    )


if __name__ == "__main__":
    main()
