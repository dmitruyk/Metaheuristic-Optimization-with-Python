"""Mountain-car model and ANN controller, Chapter 6 Problems 4a and 4b."""

from __future__ import annotations

import numpy as np

WORKED_STEP = (0.3, -0.1, -0.5)
WORKED_STEP_STATE = np.array([0.2, -0.10205402])
WORKED_ANN = np.array(
    [
        -0.79,
        -1.99,
        1.98,
        -0.24,
        0.31,
        1.2,
        0.56,
        0.12,
        0.34,
        -0.56,
        -0.11,
        1.69,
        -1.67,
        0.64,
        -1.29,
        -1.09,
        1.19,
        1.31,
        1.71,
        -0.73,
        0.65,
        0.3,
        -0.1,
    ]
)
WORKED_ANN_OUTPUT = 1.1740677276903562
WORKED_4A_INFEASIBLE = np.array(
    [
        0.04,
        -0.5,
        -1.35,
        -1.67,
        -0.57,
        0.29,
        -1.77,
        1.54,
        1.27,
        1.39,
        0.98,
        -0.75,
        -0.29,
        -1.19,
        1.55,
        1.16,
        -0.82,
        0.6,
        -0.89,
        1.87,
        -1.94,
    ]
)
WORKED_4A_INFEASIBLE_VALUE = 150776854.88275862
WORKED_4A_FEASIBLE = np.array(
    [
        -0.18,
        1.47,
        1.03,
        -0.61,
        -1.1,
        0.8,
        -0.03,
        1.49,
        0.31,
        1.42,
        0.56,
        0.97,
        1.05,
        1.32,
        1.5,
        -0.41,
        -1.45,
        -1.25,
        -1.02,
        0.82,
        1.49,
    ]
)
WORKED_4A_FEASIBLE_VALUE = 90.0
WORKED_4B_INFEASIBLE = np.array(
    [
        1.65,
        0.63,
        1.93,
        -1.51,
        1.11,
        -1.3,
        1.15,
        -1.86,
        0.53,
        0.24,
        -0.44,
        1.29,
        -0.22,
        0.77,
        -0.76,
        -1.66,
        -0.42,
        0.32,
        -1.38,
        -1.79,
        0.5,
    ]
)
WORKED_4B_INFEASIBLE_VALUE = 149009158.79243287
WORKED_4B_FEASIBLE = np.array(
    [
        1.0789,
        0.1076,
        -1.0444,
        0.5144,
        -0.241,
        0.4818,
        0.3733,
        -0.4115,
        0.5062,
        -0.2813,
        1.0257,
        0.7564,
        -0.713,
        -1.0223,
        -0.7651,
        -1.1686,
        0.0911,
        -1.1384,
        0.3539,
        -0.1077,
        -0.5485,
    ]
)
WORKED_4B_FEASIBLE_VALUE = 145.0


def step(x: float, v: float, action: float) -> np.ndarray:
    return np.array([x + v, v + 0.001 * action - 0.0025 * np.cos(3 * x)], dtype=float)


def network(theta, x=None, v=None) -> float:
    theta = np.asarray(theta, dtype=float).ravel()
    if x is None and v is None:
        if theta.size != 23:
            raise ValueError("single-argument form expects 21 weights followed by x and v")
        theta, x, v = theta[:21], theta[21], theta[22]
    elif x is None or v is None:
        raise TypeError("pass both x and v, or neither")
    elif theta.size != 21:
        raise ValueError("expected 21 ANN parameters")
    weights_in = theta[:10].reshape(5, 2)
    weights_out = theta[10:15]
    bias_hidden = theta[15:20]
    bias_out = theta[20]
    hidden = np.arctan(bias_hidden + weights_in @ np.array([x, v], dtype=float))
    return float(np.arctan(bias_out + weights_out @ hidden))


def control(theta, x: float, v: float) -> float:
    return float(np.clip(5 * network(theta, 2 * x, 20 * v), -1.0, 1.0))


def rollout(theta, *, goal: str, horizon: int = 200) -> dict:
    x, v, count = -0.5, 0.0, 1
    positions = [x]
    velocities = [v]
    actions = []
    reached = False
    for _ in range(horizon):
        action = control(theta, x, v)
        x, v = step(x, v, action)
        count += 1
        positions.append(x)
        velocities.append(v)
        actions.append(action)
        if goal == "4a" and x > 0.5:
            reached = True
            break
        if goal == "4b" and abs(x - 0.5) <= 0.002 and abs(v) <= 0.002:
            reached = True
            break
    if goal == "4a":
        value = float(count if reached else 1e8 * (0.5 - x) + count)
    elif goal == "4b":
        value = float(count if reached else 1e8 * np.hypot(0.5 - x, v) + count)
    else:
        raise ValueError("goal must be '4a' or '4b'")
    return {
        "fun": value,
        "feasible": reached,
        "steps": count,
        "position_m": np.asarray(positions, dtype=float),
        "velocity": np.asarray(velocities, dtype=float),
        "action": np.asarray(actions, dtype=float),
    }


def objective_4a(theta, horizon: int = 200) -> float:
    return rollout(theta, goal="4a", horizon=horizon)["fun"]


def objective_4b(theta, horizon: int = 200) -> float:
    return rollout(theta, goal="4b", horizon=horizon)["fun"]
