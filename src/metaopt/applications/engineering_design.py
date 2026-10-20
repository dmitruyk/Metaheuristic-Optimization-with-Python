"""Chapter 7 design objectives.

Variable names follow the listings. Penalty weights are the printed powers of ten.
A design is reported feasible only when every penalty term is zero. No global
optimum is claimed: the manuscript's formula images are not text, and these
functions were not matched to an external reference solution in this repository.
"""

from __future__ import annotations

import numpy as np


def beam_components(x: np.ndarray) -> dict:
    """Listing with variables ``b, h, tw, tf``."""

    b, h, tw, tf = np.asarray(x, dtype=float).reshape(-1)
    g1 = 2 * b * tw + tw * (h - 2 * tf) - 300
    denominator = tw * (h - 2 * tf) ** 3 + 2 * b * tw * (4 * tf**2 + 3 * h * (h - 2 * tf))
    g2 = (18 * 10**4 * h) / denominator + (15 * 10**3 * b) / ((h - 2 * tf) * tw**3 + 2 * tw * b**3) - 6
    penalty = (max(0.0, g1) + max(0.0, g2)) * 10**8
    inertia = tw * (h - 2 * tf) ** 3 / 12 + b * tf**3 / 6 + 2 * b * tf * ((h - tf) / 2) ** 2
    criterion = 5000 / inertia
    return {
        "fun": float(criterion + penalty),
        "criterion": float(criterion),
        "penalty": float(penalty),
        "feasible": penalty == 0.0 and np.isfinite(criterion),
    }


def beam_objective(x: np.ndarray) -> float:
    return beam_components(x)["fun"]


def pressure_vessel_components(x: np.ndarray) -> dict:
    """Pressure-vessel listing. Thicknesses are discrete multiples of 0.0625."""

    n_ts, n_th, radius, length = np.asarray(x, dtype=float).reshape(-1)
    ts = np.floor(n_ts + 0.5) * 0.0625
    th = np.floor(n_th + 0.5) * 0.0625
    g1 = 0.0193 * radius - ts
    g2 = 0.00954 * radius - th
    g3 = 1296000 - np.pi * radius**2 * length - 4 / 3 * np.pi * radius**3
    penalty = (max(0.0, g1) + max(0.0, g2) + max(0.0, g3)) * 10**20
    criterion = 0.6224 * ts * radius * length + 1.7781 * th * radius**2 + 3.1661 * ts**2 * length + 19.84 * ts**2 * radius
    return {
        "fun": float(criterion + penalty),
        "criterion": float(criterion),
        "penalty": float(penalty),
        "feasible": penalty == 0.0 and np.isfinite(criterion),
        "Ts": float(ts),
        "Th": float(th),
    }


def pressure_vessel_objective(x: np.ndarray) -> float:
    return pressure_vessel_components(x)["fun"]


def concrete_beam_components(x: np.ndarray) -> dict:
    n_as, n_b, h = np.asarray(x, dtype=float).reshape(-1)
    levels = np.array([6, 6.16, 6.32, 6.6, 7, 7.11, 7.2, 7.8, 7.9, 8, 8.4])
    midpoints = (levels[:-1] + levels[1:]) / 2
    area = levels[np.searchsorted(midpoints, n_as, side="right")]
    b = np.floor(n_b + 0.5)
    g1 = b / h - 4
    g2 = 180 + 7.375 * area**2 / h - area * b
    penalty = (max(0.0, g1) + max(0.0, g2)) * 10**8
    criterion = 29.4 * area + 0.6 * b * h
    return {
        "fun": float(criterion + penalty),
        "criterion": float(criterion),
        "penalty": float(penalty),
        "feasible": penalty == 0.0 and np.isfinite(criterion),
    }


def concrete_beam_objective(x: np.ndarray) -> float:
    return concrete_beam_components(x)["fun"]


def gripper_components(x: np.ndarray) -> dict:
    a, b, c, e, f, length, delta = np.asarray(x, dtype=float).reshape(-1)
    z_min, z_max = 0, 25
    y_min, y_max = 70, 150
    z_values = np.arange(z_min, z_max + 1)

    def g_length(z):
        return np.sqrt((length - z) ** 2 + e**2)

    def phi(z):
        denominator = length - z
        if denominator == 0:
            return np.pi / 2 if e > 0 else 0.0
        return np.arctan(e / denominator)

    def alpha(z):
        value = (a**2 + g_length(z) ** 2 - b**2) / (2 * g_length(z) * a)
        return np.arccos(np.clip(value, -1, 1)) + phi(z)

    def beta(z):
        value = (g_length(z) ** 2 + b**2 - a**2) / (2 * g_length(z) * b)
        return np.arccos(np.clip(value, -1, 1)) - phi(z)

    def y_opening(z):
        return 2 * (e + f + c * np.sin(beta(z) + delta))

    y_values = np.array([y_opening(z) for z in z_values])
    alpha_values = np.array([alpha(z) for z in z_values])
    phi_values = np.array([phi(z) for z in z_values])
    gamma_values = np.array([beta(z) for z in z_values])
    cos_alpha = np.array([(a**2 + g_length(z) ** 2 - b**2) / (2 * g_length(z) * a) for z in z_values])
    cos_beta = np.array([(g_length(z) ** 2 + b**2 - a**2) / (2 * g_length(z) * b) for z in z_values])
    h1_values = np.array([abs(z + a * np.cos(alpha(z)) + b * np.cos(beta(z)) - length) for z in z_values])
    h2_values = np.array([abs(a * np.sin(alpha(z)) - b * np.sin(beta(z)) - e) for z in z_values])
    criterion = -abs((y_opening(z_max) - y_opening(z_min)) / (z_max - z_min))
    g1 = np.min(y_values)
    g2 = np.min(alpha_values - phi_values)
    g3 = np.min(np.pi / 2 - alpha_values)
    g4 = np.min(np.pi / 4 - np.abs(gamma_values))
    g5 = y_min - y_opening(z_max)
    g6 = y_opening(0) - y_max
    g7 = np.min(length - z_values)
    g8 = np.max(np.abs(cos_alpha))
    g9 = np.max(np.abs(cos_beta))
    h1 = np.min(h1_values)
    h2 = np.min(h2_values)
    penalties = [
        max(0.0, -g1),
        max(0.0, -g2),
        max(0.0, -g3),
        max(0.0, -g4),
        max(0.0, -g5),
        max(0.0, -g6),
        max(0.0, -g7),
        h1 if h1 > 10**-6 else 0.0,
        h2 if h2 > 10**-6 else 0.0,
        g8 if g8 > 1 else 0.0,
        g9 if g9 > 1 else 0.0,
    ]
    penalty = float(sum(penalties) * 10**6)
    return {
        "fun": float(criterion + penalty),
        "criterion": float(criterion),
        "penalty": penalty,
        "feasible": penalty == 0.0 and np.isfinite(criterion),
    }


def gripper_objective(x: np.ndarray) -> float:
    return gripper_components(x)["fun"]
