"""PID plant from Chapter 6, Problems 1a and 1b.

The plant is ``1 / ((s+1)(1 + s/5 + s^2))`` with a PID controller
``Ki/s + Kp + Kd*s`` and unity negative feedback.

``objective_1a`` is the ITAE objective printed with the worked values
19655252.199124742 and 18.796046141402556. ``objective_1a_settling`` is the
later listing in the solving section, which replaces ITAE by a 2% settling
time. They are not the same function. See ``docs/errata.md``.

NumPy >= 2 is required because the listing calls ``numpy.trapezoid``.
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


def objective_1a(ki: float, kp: float, kd: float, *, horizon: float = 25.0, dt: float = 0.1) -> float:
    """ITAE objective from the reduction of Problem 1a."""

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


def objective_1a_vector(x: np.ndarray) -> float:
    values = np.asarray(x, dtype=float).reshape(-1)
    return objective_1a(values[0], values[1], values[2])


def objective_1a_settling(ki: float, kp: float, kd: float, *, horizon: float = 25.0, dt: float = 0.1) -> float:
    """Solving-section listing: terminal penalty, overshoot, and settling time."""

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
