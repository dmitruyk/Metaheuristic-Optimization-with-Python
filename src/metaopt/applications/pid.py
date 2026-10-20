"""PID plants from Chapter 6.

Problem 1a uses the plant ``1 / ((s+1)(1 + s/5 + s^2))`` with a PID controller
``Ki/s + Kp + Kd*s`` and unity negative feedback. Section 6.3 minimizes the
ITAE criterion. The printed worked values 19655252.199124742 and
18.796046141402556 match :func:`objective_1a_itae`.

:func:`objective_1a_settling_time` keeps the 2% settling-time expression on
that same Problem 1a plant. It is not the function that produced those printed
values.

Practical Exercise 1 uses a different plant, ``1/(1+s)**3``, and the
settling-time expression. That exercise is
:func:`objective_chapter6_exercise1_settling`. Neither settling function
replaces the ITAE objective.

NumPy >= 2 is required because the ITAE listing calls ``numpy.trapezoid``.
SymPy is imported inside this module and is an optional dependency.
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
from scipy import signal

WORKED_1A_UNSTABLE = (0.1, 1.0, 9.0)
WORKED_1A_UNSTABLE_VALUE = 19655252.199124742
WORKED_1A_FEASIBLE = (0.276, 0.765, 2.221)
WORKED_1A_FEASIBLE_VALUE = 18.796046141402556
WORKED_1B = (0.1, 2.0, 6.0)
WORKED_1B_VALUE = -0.036514370221270194


@lru_cache(maxsize=1)
def _coefficient_function():
    import sympy as sp

    s = sp.symbols("s")
    ki, kp, kd = sp.symbols("Ki Kp Kd", real=True)
    plant = 1 / ((s + 1) * (1 + sp.Rational(1, 5) * s + s**2))
    controller = ki / s + kp + kd * s
    loop = controller * plant
    closed = sp.cancel(sp.together(loop / (1 + loop)))
    numerator, denominator = sp.fraction(closed)
    num_coeffs = sp.Poly(numerator, s).all_coeffs()
    den_coeffs = sp.Poly(denominator, s).all_coeffs()
    return sp.lambdify((ki, kp, kd), [num_coeffs, den_coeffs], "numpy")


def _coefficients(ki: float, kp: float, kd: float) -> tuple[np.ndarray, np.ndarray]:
    get_coeffs = _coefficient_function()
    numerator, denominator = get_coeffs(ki, kp, kd)
    numerator = np.atleast_1d(np.array(numerator, dtype=float))
    denominator = np.array(denominator, dtype=float)
    return numerator, denominator


def objective_1a_itae(ki: float, kp: float, kd: float, *, horizon: float = 25.0, dt: float = 0.1) -> float:
    """Problem 1a ITAE objective (integral of time-weighted absolute error).

    This is the reduction listing. It matches the printed values
    19655252.199124742 at ``(0.1, 1, 9)`` and 18.796046141402556 at
    ``(0.276, 0.765, 2.221)``.
    """

    gains = np.asarray([ki, kp, kd], dtype=float).reshape(-1)
    ki, kp, kd = (float(value) for value in gains)
    numerator, denominator = _coefficients(ki, kp, kd)
    if np.any(np.roots(denominator).real >= 0):
        return 1e12
    system = signal.TransferFunction(numerator, denominator)
    time = np.arange(0.0, horizon + dt / 2, dt)
    _tout, response = signal.step(system, T=time)
    if not np.all(np.isfinite(response)):
        return 1e12
    velocity = np.gradient(response, dt)
    acceleration = np.gradient(velocity, dt)
    final_state = np.array([response[-1], velocity[-1], acceleration[-1]])
    tolerances = np.array([1e-2, 1e-4, 1e-4])
    residual = np.array([1.0, 0.0, 0.0]) - final_state
    terminal_penalty = 0.0
    if np.any(np.abs(residual) > tolerances):
        terminal_penalty = 1e8 * np.linalg.norm(residual)
    overshoot_penalty = 1e6 * max(0.0, (np.max(response) - 1.0) / 1.0)
    itae = np.trapezoid(time * np.abs(1.0 - response), time)
    return float(terminal_penalty + overshoot_penalty + itae)


def objective_1a(ki: float, kp: float, kd: float, *, horizon: float = 25.0, dt: float = 0.1) -> float:
    """Compatibility name for :func:`objective_1a_itae`."""

    return objective_1a_itae(ki, kp, kd, horizon=horizon, dt=dt)


def objective_1a_vector(x: np.ndarray) -> float:
    values = np.asarray(x, dtype=float).reshape(-1)
    return objective_1a_itae(values[0], values[1], values[2])


def objective_1a_settling_time(ki: float, kp: float, kd: float, *, horizon: float = 25.0, dt: float = 0.1) -> float:
    """Settling-time criterion on the Problem 1a plant.

    Overshoot is ``max(0, max(y) - r)`` and is not divided by the setpoint.
    The time term is the first instant after which the output stays inside a
    2% band, or the horizon if it never does. Practical Exercise 1 uses this
    expression on ``1/(1+s)**3`` instead; see
    :func:`objective_chapter6_exercise1_settling`.
    """

    numerator, denominator = _coefficients(ki, kp, kd)
    system = signal.TransferFunction(numerator, denominator)
    time = np.arange(0.0, horizon + dt / 2, dt)
    _tout, response = signal.step(system, T=time)
    velocity = np.gradient(response, dt)
    acceleration = np.gradient(np.gradient(response, dt), dt)
    terminal = np.array([response[-1], velocity[-1], acceleration[-1]])
    reference = np.array([1.0, 0.0, 0.0])
    if np.allclose(terminal, reference, atol=[1e-2, 1e-4, 1e-4]):
        terminal_penalty = 0.0
    else:
        terminal_penalty = 1e8 * np.linalg.norm(terminal - reference)
    overshoot = max(0.0, float(np.max(response) - 1.0))
    band = 0.02
    settling = horizon
    for index, instant in enumerate(time):
        if np.all(np.abs(response[index:] - 1.0) <= band):
            settling = float(instant)
            break
    return float(terminal_penalty + 1e6 * overshoot + settling)


def objective_1a_settling(ki: float, kp: float, kd: float, *, horizon: float = 25.0, dt: float = 0.1) -> float:
    """Compatibility name for :func:`objective_1a_settling_time`."""

    return objective_1a_settling_time(ki, kp, kd, horizon=horizon, dt=dt)


@lru_cache(maxsize=1)
def _exercise1_coefficient_function():
    import sympy as sp

    s = sp.symbols("s")
    ki, kp, kd = sp.symbols("Ki Kp Kd", real=True)
    plant = 1 / (1 + s) ** 3
    controller = ki / s + kp + kd * s
    loop = controller * plant
    closed = sp.cancel(sp.together(loop / (1 + loop)))
    numerator, denominator = sp.fraction(closed)
    num_coeffs = sp.Poly(numerator, s).all_coeffs()
    den_coeffs = sp.Poly(denominator, s).all_coeffs()
    return sp.lambdify((ki, kp, kd), [num_coeffs, den_coeffs], "numpy")


def objective_chapter6_exercise1_settling(
    ki: float,
    kp: float,
    kd: float,
    *,
    horizon: float = 25.0,
    dt: float = 0.1,
) -> float:
    """Practical Exercise 1: settling time for the plant ``1/(1+s)**3``.

    The expression matches the exercise listing, including overshoot that is
    not divided by the setpoint. The plant is not the Problem 1a plant.
    """

    get_coeffs = _exercise1_coefficient_function()
    numerator, denominator = get_coeffs(ki, kp, kd)
    numerator = np.atleast_1d(np.array(numerator, dtype=float))
    denominator = np.array(denominator, dtype=float)
    system = signal.TransferFunction(numerator, denominator)
    time = np.arange(0.0, horizon + dt / 2, dt)
    _tout, response = signal.step(system, T=time)
    velocity = np.gradient(response, dt)
    acceleration = np.gradient(np.gradient(response, dt), dt)
    terminal = np.array([response[-1], velocity[-1], acceleration[-1]])
    reference = np.array([1.0, 0.0, 0.0])
    if np.allclose(terminal, reference, atol=[1e-2, 1e-4, 1e-4]):
        terminal_penalty = 0.0
    else:
        terminal_penalty = 1e8 * np.linalg.norm(terminal - reference)
    overshoot = max(0.0, float(np.max(response) - 1.0))
    band = 0.02
    settling = horizon
    for index, instant in enumerate(time):
        if np.all(np.abs(response[index:] - 1.0) <= band):
            settling = float(instant)
            break
    return float(terminal_penalty + 1e6 * overshoot + settling)


def objective_1b(ki: float, kp: float, kd: float) -> float:
    """Largest real part among the closed-loop poles."""

    _numerator, denominator = _coefficients(ki, kp, kd)
    poles = np.roots(np.atleast_1d(denominator))
    return float(np.max(poles.real))


def objective_1b_vector(x: np.ndarray) -> float:
    values = np.asarray(x, dtype=float).reshape(-1)
    return objective_1b(values[0], values[1], values[2])


def step_response(ki: float, kp: float, kd: float, *, horizon: float = 25.0, dt: float = 0.1):
    numerator, denominator = _coefficients(ki, kp, kd)
    system = signal.TransferFunction(numerator, denominator)
    time = np.arange(0.0, horizon + dt / 2, dt)
    _tout, response = signal.step(system, T=time)
    return time, np.asarray(response, dtype=float)
