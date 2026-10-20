"""Evaluate the robot-gripper listing at the box center and report feasibility.

The manuscript does not print a worked numerical value for this listing.
The point below is only a smoke evaluation.
"""

from __future__ import annotations

import numpy as np

from metaopt.applications.engineering_design import gripper_components


def main() -> None:
    # Bounds are not printed as numbers in the extracted listing. This point
    # uses positive link lengths so the square roots in the listing are real.
    point = np.array([50.0, 60.0, 40.0, 20.0, 30.0, 80.0, 0.2])
    details = gripper_components(point)
    print(f"fun={details['fun']:.6g} feasible={details['feasible']} penalty={details['penalty']:.6g}")
    if not details["feasible"]:
        print("infeasible at the smoke point: at least one gripper penalty is positive")


if __name__ == "__main__":
    main()
