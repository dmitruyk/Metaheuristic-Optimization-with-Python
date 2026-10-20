"""Evaluate the Chapter 6 crane polynomial worked points."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from metaopt.applications import crane
from metaopt.plotting import plot_xy


def main() -> None:
    blocked = crane.polynomial_profiles(crane.WORKED_POLY_INFEASIBLE)
    clear = crane.polynomial_profiles(crane.WORKED_POLY_FEASIBLE)
    print(f"infeasible coefficients: {blocked['fun']:.6f} feasible={blocked['feasible']}")
    print(f"printed value: {crane.WORKED_POLY_INFEASIBLE_VALUE:.6f}")
    print(f"difference: {abs(blocked['fun'] - crane.WORKED_POLY_INFEASIBLE_VALUE):.6g}")
    print(f"feasible coefficients: {clear['fun']:.12f} feasible={clear['feasible']}")
    print(f"printed value: {crane.WORKED_POLY_FEASIBLE_VALUE:.12f}")
    print(f"difference: {abs(clear['fun'] - crane.WORKED_POLY_FEASIBLE_VALUE):.6g}")
    destination = Path("figures/generated/crane_velocity.png")
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure = plot_xy(
        {
            "velocity, feasible coefficients": (clear["time_s"], clear["velocity_m_s"]),
            "speed limit 1.2 m/s": (clear["time_s"], [1.2] * len(clear["time_s"])),
        },
        xlabel="time (s)",
        ylabel="crane velocity (m/s)",
        title="Problem 3 velocity (library evaluation, not a book figure)",
        path=destination,
    )
    plt.close(figure)
    print(f"wrote {destination}")


if __name__ == "__main__":
    main()
