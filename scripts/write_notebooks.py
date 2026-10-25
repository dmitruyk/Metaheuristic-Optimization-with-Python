"""Write the ten walkthrough notebooks. Run from the repository root."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


BOOK_LINE = "*Metaheuristic Optimization with Python: Algorithms, Engineering Applications, and Practical Examples.*"


def cell(source: str, kind: str = "code") -> dict:
    if kind == "markdown" and source.lstrip().startswith("# Chapter") and BOOK_LINE not in source:
        source = source.replace("\n\n", "\n\n" + BOOK_LINE + "\n\n", 1)
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

**Goal.** Evaluate the Section 1.3 worked objective and run canonical PSO with an explicit seed and an explicit generation count.

The objective is `sum of squares + sum of absolute values`. At the printed point the value is 12.3901. The search uses `numpy.random.Generator`. It will not match a run that called `np.random.seed`.

**Expected.** The first printed number is 12.3901 within `1e-9`. `nfev` is `12 * 8 = 96`. `fun` is finite and nonnegative. That search value is not Figure 1.8.

**Interpretation.** A repeated seed repeats `history` in this NumPy build. A different seed may change `fun` and must not change `nfev` while the population and iteration count stay fixed.
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
if abs(objective(point) - 12.3901) > 1e-9:
    raise SystemExit("the Section 1.3 value drifted")
if result.nfev != 96 or not np.isfinite(result.fun):
    raise SystemExit("PSO budget or objective was not the expected smoke result")
""",
            ),
            cell(
                """## Exercise

Call the same minimizer with `seed=2`. Confirm `nfev` is still 96. The objective value may change. Do not install packages from the notebook.
""",
                "markdown",
            ),
            cell(
                """
other = minimize(objective, [[-20.0, 20.0]] * 10, seed=2, population_size=12, iterations=8)
print(other.fun, other.nfev)
if other.nfev != result.nfev:
    raise SystemExit("the evaluation budget changed with the seed")
""",
            ),
        ],
    )
    write(
        "02_differential_evolution.ipynb",
        [
            cell(
                """# Chapter 2 — Differential evolution

**Goal.** Compare `DE/rand/1/bin` and `DE/best/1/bin` on the sphere under one evaluation budget.

Both use `CR=0.5` and `F=0.6`. The donor is clipped to the box before crossover.

**Expected.** Each run prints a finite objective. `max_evaluations=120` is the shared budget. These values are not Figure 2.5.

**Interpretation.** The same seed makes each variant repeatable. The two variants do not have to return the same value. Compare them by `nfev`, not by a claim about the printed chapter figure.
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
rand = minimize(sphere, bounds, **common)
best = minimize_best(sphere, bounds, **common)
print("rand", rand.fun, rand.nfev)
print("best", best.fun, best.nfev)
if rand.nfev > 120 or best.nfev > 120:
    raise SystemExit("a DE run exceeded the shared budget")
if not np.isfinite(rand.fun) or not np.isfinite(best.fun):
    raise SystemExit("a DE run returned a non-finite objective")
""",
            ),
            cell(
                """## Exercise

Set `seed=3` in `common` and run the cell again. Both calls must still respect `max_evaluations=120`.
""",
                "markdown",
            ),
            cell(
                """
common_seed_3 = dict(common, seed=3)
again = minimize(sphere, bounds, **common_seed_3)
print(again.fun, again.nfev)
if again.nfev > 120:
    raise SystemExit("the exercise run exceeded the budget")
""",
            ),
        ],
    )
    write(
        "03_grey_wolf_optimizer.ipynb",
        [
            cell(
                """# Chapter 3 — Grey wolf optimizer

**Goal.** Run canonical GWO on the sphere and check the evaluation count.

`a = 2 - 2 * (step / iterations)` with `step` starting at 2, because the initial pack is generation 1. Positions are clipped to the box.

**Expected.** `nfev` is `12 * 10 = 120`. `history[-1]` equals `fun`. The curve is not Figure 3.5.

**Interpretation.** mGWO changes the schedule of `a`. GWOEPD spends extra evaluations on the replaced wolves, so its `nfev` is not this number. See `tests/test_gwo.py`.
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
if result.nfev != 120 or result.history[-1] != result.fun:
    raise SystemExit("GWO accounting did not match the smoke budget")
""",
            ),
            cell(
                """## Exercise

Run `metaopt.variants.mgwo.minimize` with the same seed, population, and iteration count. Its `nfev` should also be 120. The objective value may differ because `a` follows a square schedule.
""",
                "markdown",
            ),
            cell(
                """
from metaopt.variants.mgwo import minimize as mgwo_minimize

modified = mgwo_minimize(sphere, [[-5.0, 5.0]] * 3, seed=3, population_size=12, iterations=10)
print(modified.fun, modified.nfev)
if modified.nfev != result.nfev:
    raise SystemExit("mGWO did not use the same evaluation count")
""",
            ),
        ],
    )
    write(
        "04_benchmarks.ipynb",
        [
            cell(
                """# Chapter 4 — Benchmarks

**Goal.** Check that Appendix B exposes 54 functions and that two reference locations still return the printed values.

Elliptic is undefined for one variable because the listing divides by `D - 1`. Paviani is defined on `(2, 10)`; a point outside that interval warns and is non-finite. Table 4.1 and Appendix B disagree on Whitley. This notebook does not choose a replacement formula.

**Expected.** `len(BENCHMARKS)` is 54. The sphere at the origin is 0. Rosenbrock at the all-ones vector is 0.

**Interpretation.** `results/reference_minima.csv` is a location check, not a Chapter 5 rank table.
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
if len(BENCHMARKS) != 54 or SphericalFunction(np.zeros(4)) != 0.0 or RosenbrockFunction(np.ones(5)) != 0.0:
    raise SystemExit("a reference benchmark value changed")
""",
            ),
            cell(
                """## Exercise

Evaluate Paviani at the origin and Elliptic in one variable. The first call warns. The second raises `ValueError`. Neither call is a reason to edit the Appendix B formula.
""",
                "markdown",
            ),
            cell(
                """
import warnings
from metaopt.benchmarks import EllipticFunction, PavianiFunction

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    paviani = PavianiFunction(np.zeros(2))
print(paviani, len(caught))
try:
    EllipticFunction(np.zeros(1))
except ValueError as exc:
    print(type(exc).__name__)
""",
            ),
        ],
    )
    write(
        "05_fair_comparisons.ipynb",
        [
            cell(
                """# Chapter 5 — Equal evaluation budgets

**Goal.** Give every handbook algorithm the same `max_evaluations` on the sphere.

The handbook's 500-iteration protocol does not give GWOEPD the same number of objective calls as PSO. Population 9 is a square, so von Neumann PSO can run. These sphere values are smoke results. They are not Appendix C. The reduced study in `results/reduced_comparison_summary.json` is also a new experiment, not the printed rank tables.

**Expected.** Each row prints a finite `fun` and an `nfev` no larger than 90.

**Interpretation.** Equal budgets are the fair comparison in this library. Matching the manuscript's iteration count is a different experiment, and that experiment was not rerun.
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
    if row["nfev"] > 90 or not np.isfinite(row["fun"]):
        raise SystemExit(f"{row['algorithm']} broke the smoke budget")
""",
            ),
            cell(
                """## Exercise

Read one row's `nfev`. It has to be at most 90. Do not treat the printed `fun` as a cell from Table 5.1 or Appendix C.
""",
                "markdown",
            ),
            cell(
                """
print(rows[0]["algorithm"], rows[0]["nfev"], rows[0]["max_evaluations"])
if rows[0]["nfev"] > rows[0]["max_evaluations"]:
    raise SystemExit("the first algorithm exceeded the shared budget")
""",
            ),
        ],
    )
    write(
        "06_pid_tuning.ipynb",
        [
            cell(
                """# Chapter 6 — PID worked values

**Goal.** Evaluate the printed Problem 1a and Problem 1b points.

`objective_1a_itae` (also available as `objective_1a`) is the Section 6.3 ITAE objective. The printed numbers 19655252.199124742 and 18.796046141402556 belong to that function. `objective_1a_settling_time` is the settling-time expression on the same Problem 1a plant; it does not match those numbers. Practical Exercise 1 uses the settling-time expression on a different plant, `1/(1+s)**3`, implemented as `objective_chapter6_exercise1_settling`.

**Expected.** The two ITAE prints match those published numbers within the tolerances in `tests/test_examples_smoke.py`. The settling value at the same gains does not.

**Interpretation.** Section 6.3 states that Problem 1a minimizes ITAE. The exercise is a separate task. Both functions stay in the library.
""",
                "markdown",
            ),
            cell(
                """
from metaopt.applications import pid

print(pid.objective_1a_itae(*pid.WORKED_1A_UNSTABLE))
print(pid.objective_1a_itae(*pid.WORKED_1A_FEASIBLE))
print(pid.objective_1b(*pid.WORKED_1B))
print(pid.objective_1a_settling_time(*pid.WORKED_1A_FEASIBLE))
print(pid.objective_chapter6_exercise1_settling(1.0, 1.0, 1.0))
""",
            ),
            cell(
                """## Exercise

Subtract the ITAE value from the Problem 1a settling-time value at `(0.276, 0.765, 2.221)`. The difference should not be zero. Do not delete either function.
""",
                "markdown",
            ),
            cell(
                """
itae = pid.objective_1a_itae(*pid.WORKED_1A_FEASIBLE)
settling = pid.objective_1a_settling_time(*pid.WORKED_1A_FEASIBLE)
print(abs(itae - settling))
""",
            ),
        ],
    )
    write(
        "07_robot_path_planning.ipynb",
        [
            cell(
                """# Chapter 6 — Mobile robot

**Goal.** Evaluate the two printed node sets.

The crossing node set is infeasible and prints 35571448004.83873. The clear node set is feasible and prints 14.74322171254588.

**Expected.** Those two objective values, with feasibility flags false and true.

**Interpretation.** The large value is the penalty for an infeasible path, not a path length.
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
            cell(
                """## Exercise

Check that the infeasible value is larger than the feasible value by more than `1e6`. That gap is the penalty, not a second path length.
""",
                "markdown",
            ),
            cell(
                """
print(bad["fun"] - good["fun"])
if not (bad["fun"] > good["fun"] + 1e6):
    raise SystemExit("the infeasible penalty was not visible")
""",
            ),
        ],
    )
    write(
        "08_crane_control.ipynb",
        [
            cell(
                """# Chapter 6 — Crane polynomial reduction

**Goal.** Evaluate the two printed coefficient vectors.

The first vector is infeasible and prints 707599.2688799157. The second prints 0.4209773021079328. Its speed excess is about `6e-8` m/s, so the penalty is tiny and the feasibility flag treats a penalty below `1e-6` as inactive. The polynomial is unchanged.

**Expected.** Those objective values. The second penalty is below `1e-6` and above 0.

**Interpretation.** A prose note should say the speed constraint holds up to roundoff. Clipping the violation inside the formula would change the printed objective and is not done here.
""",
                "markdown",
            ),
            cell(
                """
from metaopt.applications import crane

blocked = crane.polynomial_profiles(crane.WORKED_POLY_INFEASIBLE)
clear = crane.polynomial_profiles(crane.WORKED_POLY_FEASIBLE)
print(blocked["fun"], blocked["feasible"])
print(clear["fun"], clear["feasible"], clear["penalty"])
""",
            ),
            cell(
                """## Exercise

Print `clear["penalty"]`. It should be positive and below `1e-6`. That is the floating-point speed excess, not a second crane model.
""",
                "markdown",
            ),
            cell(
                """
print(clear["penalty"])
if not (0.0 < clear["penalty"] < 1e-6):
    raise SystemExit("the roundoff penalty was not in the expected range")
""",
            ),
        ],
    )
    write(
        "09_cart_pole.ipynb",
        [
            cell(
                """# Chapter 6 — Mountain car and cart-pole

**Goal.** Check the printed one-step maps and the two cart-pole parameter vectors.

The terminal penalty stays a parenthesized conditional so a typesetter cannot split it into an illegal `else` line. No package is installed from this notebook.

**Expected.** The feasible cart-pole vector prints `True`. The infeasible vector prints `False`. Mountain-car 4a at the feasible vector returns 90.

**Interpretation.** These are direct evaluations of printed inputs. They are not traced copies of the chapter figures.
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
            cell(
                """## Exercise

Evaluate mountain-car goals 4a and 4b at their feasible vectors. The printed objectives are 90 and 145.
""",
                "markdown",
            ),
            cell(
                """
print(mountain_car.objective_4a(mountain_car.WORKED_4A_FEASIBLE))
print(mountain_car.objective_4b(mountain_car.WORKED_4B_FEASIBLE))
""",
            ),
        ],
    )
    write(
        "10_engineering_design.ipynb",
        [
            cell(
                """# Chapter 7 — Design listings

**Goal.** Run a four-generation PSO on the pressure-vessel penalty and report feasibility.

Feasibility is the penalty. This run does not claim the known literature optimum.

**Expected.** `nfev` is `8 * 4 = 32`. `fun` is finite. `feasible` may be false at this budget.

**Interpretation.** A longer search would still be a new Generator experiment, not a reproduction of a printed design table, unless that table is checked number by number.
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
if result.nfev != 32 or not (details["fun"] == details["fun"]):
    raise SystemExit("the design smoke run did not finish")
""",
            ),
            cell(
                """## Exercise

Read `details["feasible"]`. If it is false, name the penalty rather than calling the vessel dimensions optimal.
""",
                "markdown",
            ),
            cell(
                """
print("feasible" if details["feasible"] else "penalty still active")
""",
            ),
        ],
    )


if __name__ == "__main__":
    main()
    subprocess.check_call([sys.executable, "-m", "ruff", "format", str(NOTEBOOKS)])
