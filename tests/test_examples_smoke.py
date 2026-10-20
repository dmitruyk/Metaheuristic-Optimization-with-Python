"""Worked numerical examples from the handbook, plus example-script smoke runs."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from metaopt.applications import cart_pole, crane, mobile_robot, mountain_car, pid
from metaopt.benchmarks import SphericalFunction

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = [
    "pid_tuning.py",
    "mobile_robot.py",
    "crane_control.py",
    "pressure_vessel.py",
    "robot_gripper.py",
    "scipy_differential_evolution.py",
]


def test_ten_variable_objective_on_the_printed_point():
    # Section 1.3. The printed value is 12.3901.
    x = np.array([0.1, 0.2, 0.3, -0.2, 0.51, -0.2, 0, -0.2, -1.6, 2.0])

    def objective(point):
        return float(np.sum(point**2) + np.sum(np.abs(point)))

    assert objective(x) == pytest.approx(12.3901, abs=1e-12)
    # Sphere is a different function; this guards against swapping them.
    assert SphericalFunction(x) != pytest.approx(12.3901, abs=1e-3)


def test_pid_worked_values():
    unstable = pid.objective_1a(*pid.WORKED_1A_UNSTABLE)
    feasible = pid.objective_1a(*pid.WORKED_1A_FEASIBLE)
    dominant = pid.objective_1b(*pid.WORKED_1B)
    assert unstable == pytest.approx(pid.WORKED_1A_UNSTABLE_VALUE, rel=1e-6, abs=1e-4)
    assert feasible == pytest.approx(pid.WORKED_1A_FEASIBLE_VALUE, rel=1e-5, abs=1e-4)
    assert dominant == pytest.approx(pid.WORKED_1B_VALUE, rel=1e-6, abs=1e-8)
    assert feasible < 100


def test_robot_and_crane_worked_values():
    bad = mobile_robot.path_geometry(mobile_robot.WORKED_INFEASIBLE)
    good = mobile_robot.path_geometry(mobile_robot.WORKED_FEASIBLE)
    assert bad["feasible"] is False
    assert good["feasible"] is True
    assert bad["fun"] == pytest.approx(mobile_robot.WORKED_INFEASIBLE_VALUE, rel=1e-6)
    assert good["fun"] == pytest.approx(mobile_robot.WORKED_FEASIBLE_VALUE, rel=1e-6)
    blocked = crane.polynomial_profiles(crane.WORKED_POLY_INFEASIBLE)
    clear = crane.polynomial_profiles(crane.WORKED_POLY_FEASIBLE)
    assert blocked["feasible"] is False
    assert clear["feasible"] is True
    assert blocked["fun"] == pytest.approx(crane.WORKED_POLY_INFEASIBLE_VALUE, rel=1e-6)
    assert clear["fun"] == pytest.approx(crane.WORKED_POLY_FEASIBLE_VALUE, rel=1e-6)


def test_mountain_car_and_cart_pole_worked_values():
    stepped = mountain_car.step(*mountain_car.WORKED_STEP)
    assert stepped == pytest.approx(mountain_car.WORKED_STEP_STATE, abs=5e-8)
    assert mountain_car.network(mountain_car.WORKED_ANN) == pytest.approx(mountain_car.WORKED_ANN_OUTPUT, rel=1e-10)
    bad_4a = mountain_car.rollout(mountain_car.WORKED_4A_INFEASIBLE, goal="4a")
    good_4a = mountain_car.rollout(mountain_car.WORKED_4A_FEASIBLE, goal="4a")
    assert bad_4a["feasible"] is False
    assert good_4a["feasible"] is True
    assert bad_4a["fun"] == pytest.approx(mountain_car.WORKED_4A_INFEASIBLE_VALUE, rel=1e-8)
    assert good_4a["fun"] == mountain_car.WORKED_4A_FEASIBLE_VALUE
    bad_4b = mountain_car.rollout(mountain_car.WORKED_4B_INFEASIBLE, goal="4b")
    good_4b = mountain_car.rollout(mountain_car.WORKED_4B_FEASIBLE, goal="4b")
    assert bad_4b["feasible"] is False
    assert good_4b["feasible"] is True
    assert bad_4b["fun"] == pytest.approx(mountain_car.WORKED_4B_INFEASIBLE_VALUE, rel=1e-8)
    assert good_4b["fun"] == mountain_car.WORKED_4B_FEASIBLE_VALUE

    stepped_pole = cart_pole.step(*cart_pole.WORKED_STEP)
    assert stepped_pole == pytest.approx(cart_pole.WORKED_STEP_STATE, abs=5e-8)
    assert cart_pole.network(cart_pole.WORKED_ANN) == pytest.approx(cart_pole.WORKED_ANN_OUTPUT, rel=1e-10)
    bad = cart_pole.simulate(cart_pole.WORKED_INFEASIBLE)
    good = cart_pole.simulate(cart_pole.WORKED_FEASIBLE)
    assert bad["feasible"] is False
    assert good["feasible"] is True
    assert bad["fun"] == pytest.approx(cart_pole.WORKED_INFEASIBLE_VALUE, rel=1e-8)
    assert good["fun"] == pytest.approx(cart_pole.WORKED_FEASIBLE_VALUE, rel=1e-8)


@pytest.mark.parametrize("script", EXAMPLES)
def test_example_script_exits_zero(script):
    cache = ROOT / ".cache"
    cache.mkdir(exist_ok=True)
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    env["MPLCONFIGDIR"] = str(cache / "matplotlib")
    env["XDG_CACHE_HOME"] = str(cache)
    completed = subprocess.run(
        [sys.executable, str(ROOT / "examples" / script)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert completed.returncode == 0, completed.stderr
