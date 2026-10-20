"""Evaluate the Chapter 6 mobile-robot worked trajectories."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from metaopt.applications import mobile_robot
from metaopt.plotting import plot_xy


def main() -> None:
    bad = mobile_robot.path_geometry(mobile_robot.WORKED_INFEASIBLE)
    good = mobile_robot.path_geometry(mobile_robot.WORKED_FEASIBLE)
    print(f"crossing trajectory value: {bad['fun']:.6f} feasible={bad['feasible']}")
    print(f"printed value: {mobile_robot.WORKED_INFEASIBLE_VALUE:.6f}")
    print(f"clear trajectory value: {good['fun']:.6f} feasible={good['feasible']}")
    print(f"printed value: {mobile_robot.WORKED_FEASIBLE_VALUE:.6f}")
    print(f"absolute difference, clear path: {abs(good['fun'] - mobile_robot.WORKED_FEASIBLE_VALUE):.6g}")
    sample = np.linspace(0, 1, good["points"].shape[0])
    destination = Path("figures/generated/mobile_robot_path.png")
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure = plot_xy(
        {
            "worked feasible path": (good["points"][:, 0], good["points"][:, 1]),
            "worked crossing path": (bad["points"][:, 0], bad["points"][:, 1]),
        },
        xlabel="x (workspace units)",
        ylabel="y (workspace units)",
        title="Problem 2 spline paths (library evaluation, not a book figure)",
        path=destination,
    )
    plt.close(figure)
    del sample
    print(f"wrote {destination}")


if __name__ == "__main__":
    main()
