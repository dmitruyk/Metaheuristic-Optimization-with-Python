"""Evaluate the Chapter 6 PID worked examples and save a step-response plot.

The plot is library output. It is not a claim that Figure 6.17 was reproduced.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from metaopt.applications import pid
from metaopt.plotting import plot_xy


def main() -> None:
    unstable = pid.objective_1a(*pid.WORKED_1A_UNSTABLE)
    feasible = pid.objective_1a(*pid.WORKED_1A_FEASIBLE)
    dominant = pid.objective_1b(*pid.WORKED_1B)
    print(f"Problem 1a at (0.1, 1, 9): {unstable:.6f}")
    print(f"printed value: {pid.WORKED_1A_UNSTABLE_VALUE:.6f}")
    print(f"absolute difference: {abs(unstable - pid.WORKED_1A_UNSTABLE_VALUE):.6g}")
    print(f"Problem 1a at (0.276, 0.765, 2.221): {feasible:.6f}")
    print(f"printed value: {pid.WORKED_1A_FEASIBLE_VALUE:.6f}")
    print(f"absolute difference: {abs(feasible - pid.WORKED_1A_FEASIBLE_VALUE):.6g}")
    print(f"feasible by the printed penalty test (value < 1e3): {feasible < 1e3}")
    print(f"Problem 1b at (0.1, 2, 6): {dominant:.12f}")
    print(f"printed value: {pid.WORKED_1B_VALUE:.12f}")
    print(f"absolute difference: {abs(dominant - pid.WORKED_1B_VALUE):.6g}")
    time, response = pid.step_response(*pid.WORKED_1A_FEASIBLE)
    destination = Path("figures/generated/pid_step_response.png")
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure = plot_xy(
        {"Ki=0.276, Kp=0.765, Kd=2.221": (time, response)},
        xlabel="time (s)",
        ylabel="output (dimensionless setpoint = 1)",
        title="Problem 1a step response (library evaluation, not a book figure)",
        path=destination,
    )
    plt.close(figure)
    print(f"wrote {destination}")


if __name__ == "__main__":
    main()
