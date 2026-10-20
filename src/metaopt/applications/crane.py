"""Crane objectives from Chapter 6.

``polynomial_objective`` is Problem 3, the degree-13 polynomial reduction.
``switching_objective`` is the three-interval force schedule whose simulator
is printed later in the chapter. Both are kept because the manuscript gives
both listings. Worked polynomial values:

``(-6, 9, 20, 5, 5, 60, 0) -> 707599.2688799157``
``(-5, 6, 10, -2, 5, 20, -4) -> 0.4209773021079328``
"""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

WORKED_POLY_INFEASIBLE = (-6.0, 9.0, 20.0, 5.0, 5.0, 60.0, 0.0)
WORKED_POLY_INFEASIBLE_VALUE = 707599.2688799157
WORKED_POLY_FEASIBLE = (-5.0, 6.0, 10.0, -2.0, 5.0, 20.0, -4.0)
WORKED_POLY_FEASIBLE_VALUE = 0.4209773021079328


def polynomial_profiles(coefficients: np.ndarray) -> dict:
    a0, a1, a2, a3, a4, a5, a6 = np.asarray(coefficients, dtype=float).reshape(-1)
    length, gravity, speed, horizon = 5.0, 9.81, 1.2, 3.0
    time = np.arange(301) * 0.01
    window = np.array([1, -4, 6, -4, 1], dtype=float)
    packed = np.r_[1, 2, 2, 0, a0, a1, a2, a3, a4, a5, a6, 0, 0, 0, 0]
    velocity = (
        speed
        * time
        / (2 * gravity * horizon**13)
        * sum(
            (k + 4) * (window @ packed[k : k + 5]) * time**k * ((k + 2) * (k + 3) * length + gravity * time**2) * horizon ** (10 - k)
            for k in range(11)
        )
    )
    gap = (
        speed
        * length
        * time**2
        * (time - horizon) ** 2
        / (gravity * horizon**13)
        * (
            91 * a6 * time**8
            + 26 * (3 * a5 - 5 * a6) * time**7 * horizon
            + 3 * (22 * a4 - 36 * a5 + 15 * a6) * time**6 * horizon**2
            + (55 * a3 - 88 * a4 + 36 * a5) * time**5 * horizon**3
            + (45 * a2 - 70 * a3 + 28 * a4) * time**4 * horizon**4
            + 3 * (12 * a1 - 18 * a2 + 7 * a3) * time**3 * horizon**5
            + (28 * a0 - 40 * a1 + 15 * a2) * time**2 * horizon**6
            + 2 * (-14 * a0 + 5 * a1) * time * horizon**7
            + 6 * (5 + a0) * horizon**8
        )
    )
    velocity_violation = max(float(velocity.max() - speed), 0.0) + max(float(-velocity.min()), 0.0)
    penalty = 1e6 * velocity_violation
    return {
        "time_s": time,
        "velocity_m_s": velocity,
        "position_gap_m": gap,
        "penalty": float(penalty),
        "fun": float(gap.max() + penalty),
        # The printed "feasible" coefficients make dx1.max() exceed 1.2 m/s by
        # about 6e-8 because of floating-point evaluation. The objective value
        # still matches the printed number. Treat a penalty below 1e-6 as inactive.
        "feasible": penalty < 1e-6,
    }


def polynomial_objective(coefficients: np.ndarray) -> float:
    return polynomial_profiles(coefficients)["fun"]


def simulate_switching(t1: float, t2: float, t3: float, dt: float = 0.1) -> SimpleNamespace:
    """Three-interval crane simulator printed with the switching objective."""

    m1, m2, length, gravity = 20000.0, 10000.0, 5.0, 9.81
    friction = 0.01 * gravity * (m1 + m2)
    force, stiffness = 50000.0, gravity / length

    def state_matrix(drive: float, slipping: float) -> np.ndarray:
        matrix = np.zeros((5, 5))
        matrix[0, 1] = matrix[2, 3] = 1.0
        matrix[3, 0], matrix[3, 2] = stiffness, -stiffness
        if slipping:
            matrix[1, 0] = -m2 / m1 * stiffness
            matrix[1, 2] = m2 / m1 * stiffness
            matrix[1, 4] = (drive - slipping * friction) / m1
        else:
            matrix[0, 1] = 0.0
        return matrix

    def event(state: np.ndarray, drive: float, slipping: float) -> float:
        if slipping:
            return float(slipping * state[1])
        return float(friction - abs(drive - m2 * stiffness * (state[0] - state[2])))

    state = np.array([0.0, 0.0, 0.0, 0.0, 1.0])
    times = [0.0]
    samples = [state[:4].copy()]
    origin = 0.0
    for drive, duration in ((force, t1), (0.0, t2), (force, t3)):
        elapsed = 0.0
        for _ in range(100):
            remaining = duration - elapsed
            if remaining <= 1e-12:
                break
            net = drive - m2 * stiffness * (state[0] - state[2])
            if state[1]:
                slipping = float(np.sign(state[1]))
            elif abs(net) <= friction:
                slipping = 0.0
            else:
                slipping = float(np.sign(net))
            matrix = state_matrix(drive, slipping)
            pieces = int(remaining / dt) + 1
            step = remaining / pieces
            transition = expm(matrix * step)
            cursor = state
            previous = event(state, drive, slipping)
            hit = None
            for piece in range(pieces):
                nxt = transition @ cursor
                value = event(nxt, drive, slipping)
                if value <= 0 < previous:
                    hit = piece
                    break
                cursor, previous = nxt, value
                times.append(origin + elapsed + (piece + 1) * step)
                samples.append(nxt[:4].copy())
            if hit is None:
                state = cursor
                break
            tau = brentq(lambda instant: event(expm(matrix * instant) @ cursor, drive, slipping), 0.0, step)
            state = expm(matrix * tau) @ cursor
            elapsed = elapsed + hit * step + tau
            if slipping:
                state[1] = 0.0
            times.append(origin + elapsed)
            samples.append(state[:4].copy())
        origin += duration
    return SimpleNamespace(t=np.array(times), y=np.array(samples).T)


def switching_objective(times: np.ndarray) -> float:
    t1, t2, t3 = np.asarray(times, dtype=float).reshape(-1)
    target_speed = 1.2
    solution = simulate_switching(t1, t2, t3)
    x1, v1, x2, v2 = solution.y[:, -1]
    penalty = 1e8 * (abs(x1 - x2) + abs(v1 - target_speed) + abs(v2 - target_speed))
    return float(t1 + t2 + t3 + penalty)
