"""Cart-pole swing-up, Chapter 6 Problem 5.

The manuscript ternary

``penalty_terminal = 0.0 if reached else W_TERMINAL * np.linalg.norm(S[-1])``

is valid Python when it stays on one line. A layout wrap that puts ``else``
on the next line without parentheses is a syntax error. This module keeps
the expression in parentheses so a formatter cannot split it illegally.

``reached`` is true if *any* state, including the start, lies inside the
tolerance box. The start is ``(pi, 0, 0, 0)``, which is outside that box.
"""

from __future__ import annotations

import numpy as np

DT = 0.025
N_STEPS = 200
F_MAX = 5.0
X_MAX = 0.7
TOL = np.array([0.005, 0.005, 0.001, 0.005])
W_POSITION = 1e4
W_TERMINAL = 1e10

WORKED_STEP = (0.1, -0.3, 1.0, -0.2, 4.0)
WORKED_STEP_STATE = np.array([0.0925, -1.04018082, 0.995, 0.14734152])
WORKED_ANN = np.array(
    [
        -1.29,
        -1.54,
        -0.54,
        -1.98,
        1.89,
        -1.57,
        -0.11,
        -0.14,
        -0.49,
        1.5,
        0.73,
        -0.79,
        -0.26,
        -0.45,
        -0.07,
        0.44,
        0.82,
        -0.15,
        0.05,
        -1.44,
        1.73,
        0.32,
        -0.3,
        -0.32,
        0.05,
        1.82,
        1.17,
        -1.38,
        0.58,
        0.69,
        -0.68,
        0.1,
        0.96,
        1.06,
        0.34,
    ]
)
WORKED_ANN_OUTPUT = -1.1699388753567221
WORKED_INFEASIBLE = np.array(
    [
        -1.39,
        0.14,
        -0.71,
        -0.09,
        0.570,
        -1.07,
        0.72,
        0.75,
        -1.89,
        1.75,
        -1.87,
        1.75,
        -1.38,
        -1.11,
        1.27,
        1.16,
        -0.06,
        1.03,
        -0.86,
        1.5,
        -0.66,
        1.95,
        0.51,
        1.55,
        1.45,
        -0.92,
        0.7,
        -0.21,
        -0.81,
        1.32,
        0.47,
    ]
)
WORKED_INFEASIBLE_VALUE = 1224151813560.341
WORKED_FEASIBLE = np.array(
    [
        1.439,
        0.402,
        0.856,
        0.852,
        0.176,
        0.385,
        -1.242,
        0.243,
        0.152,
        -0.632,
        1.377,
        0.006,
        -1.449,
        0.047,
        1.468,
        0.662,
        1.5,
        0.124,
        -1.472,
        0.026,
        -0.6920,
        -0.617,
        -1.116,
        -1.102,
        0.904,
        -1.145,
        -0.26,
        1.413,
        -0.392,
        0.945,
        -0.776,
    ]
)
WORKED_FEASIBLE_VALUE = 4.350040156962044


def step(phi: float, omega: float, x: float, v: float, force: float, dt: float = 0.025) -> np.ndarray:
    pole_mass, cart_mass, length, gravity = 0.3, 0.2, 0.5, 9.81
    sine, cosine = np.sin(phi), np.cos(phi)
    denominator = pole_mass * length + cart_mass * length * sine * sine
    phi_acc = (-(pole_mass + cart_mass) * gravity * sine - cart_mass * length * omega**2 * sine * cosine - force * cosine) / denominator
    x_acc = (cart_mass * sine * (length * omega**2 + gravity * cosine) + force) / (pole_mass + cart_mass * sine * sine)
    return np.array(
        [phi + omega * dt, omega + phi_acc * dt, x + v * dt, v + x_acc * dt],
        dtype=float,
    )


def network(theta, state=None) -> float:
    theta = np.asarray(theta, dtype=float).ravel()
    if state is None:
        if theta.size != 35:
            raise ValueError("single-argument form expects 31 parameters followed by the state")
        theta, state = theta[:31], theta[31:]
    elif theta.size != 31:
        raise ValueError("expected 31 ANN parameters")
    state = np.asarray(state, dtype=float)
    weights_in = theta[:20].reshape(5, 4)
    weights_out = theta[20:25]
    bias_hidden = theta[25:30]
    bias_out = theta[30]
    hidden = np.arctan(bias_hidden + weights_in @ state)
    return float(np.arctan(bias_out + weights_out @ hidden))


def simulate(theta) -> dict:
    theta = np.asarray(theta, dtype=float)
    if theta.size != 31:
        raise ValueError("expected 31 ANN parameters")
    state = np.array([np.pi, 0.0, 0.0, 0.0])
    states = [state.copy()]
    forces = []
    for _ in range(N_STEPS):
        force = float(np.clip(5 * network(theta, state), -F_MAX, F_MAX))
        state = np.asarray(step(*state, force, dt=DT), dtype=float)
        states.append(state.copy())
        forces.append(force)
    trajectory = np.array(states)
    force_array = np.array(forces)
    reached = bool(np.any(np.all(np.abs(trajectory) < TOL, axis=1)))
    terminal_penalty = 0.0 if reached else W_TERMINAL * float(np.linalg.norm(trajectory[-1]))
    x_max = float(np.abs(trajectory[:, 2]).max())
    position_penalty = W_POSITION * max(0.0, x_max - X_MAX)
    control_cost = float(np.sqrt(np.sum(force_array**2) * DT))
    return {
        "fun": float(terminal_penalty + position_penalty + control_cost),
        "feasible": reached and position_penalty == 0.0,
        "terminal_penalty": float(terminal_penalty),
        "position_penalty": float(position_penalty),
        "control_cost": control_cost,
        "states": trajectory,
        "force_n": force_array,
        "time_s": np.arange(trajectory.shape[0]) * DT,
    }


def objective(theta) -> float:
    return simulate(theta)["fun"]
