"""Mobile-robot spline path, Chapter 6 Problem 2.

Three free nodes connect (0, 0) to (10, 10). The objective is path length
plus a domain penalty of weight 1e10 and an obstacle penalty of weight 1e6.
"""

from __future__ import annotations

import numpy as np
from scipy.interpolate import CubicSpline

OBSTACLES = np.array([[2.0, 2.0], [7.0, 3.0], [7.0, 7.5], [2.5, 7.0]], dtype=float)
RADII = np.array([1.1, 1.4, 1.6, 1.5], dtype=float)
WORKED_INFEASIBLE = (1.33, 2.65, 2.75, 1.13, 5.17, 6.8)
WORKED_INFEASIBLE_VALUE = 35571448004.83873
WORKED_FEASIBLE = (3.76, 1.77, 5.93, 4.13, 7.96, 5.90)
WORKED_FEASIBLE_VALUE = 14.74322171254588


def path_geometry(x: np.ndarray) -> dict:
    kx1, ky1, kx2, ky2, kx3, ky3 = np.asarray(x, dtype=float).reshape(-1)
    nodes = np.array(
        [[0.0, 0.0], [kx1, ky1], [kx2, ky2], [kx3, ky3], [10.0, 10.0]],
        dtype=float,
    )
    parameter = np.arange(len(nodes), dtype=float)
    splines = [CubicSpline(parameter, nodes[:, axis]) for axis in range(2)]
    sample = np.linspace(0, len(nodes) - 1, 201)
    points = np.column_stack([spline(sample) for spline in splines])
    length = float(np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1)))
    outside = np.maximum(0, -points[:, 0]) + np.maximum(0, points[:, 0] - 10)
    outside = outside + np.maximum(0, -points[:, 1]) + np.maximum(0, points[:, 1] - 10)
    domain_penalty = float(1e10 * np.sum(outside))
    distances = np.linalg.norm(points[:, None, :] - OBSTACLES[None, :, :], axis=2)
    penetration = np.maximum(0, RADII[None, :] - distances)
    obstacle_penalty = float(1e6 * np.sum(penetration))
    return {
        "points": points,
        "length": length,
        "domain_penalty": domain_penalty,
        "obstacle_penalty": obstacle_penalty,
        "fun": float(length + domain_penalty + obstacle_penalty),
        "feasible": domain_penalty == 0.0 and obstacle_penalty == 0.0,
    }


def objective(x: np.ndarray) -> float:
    return path_geometry(x)["fun"]
