"""Evaluate the feasible worked example for the gripper's π/4 variant."""

from __future__ import annotations

import numpy as np

from metaopt.applications.engineering_design import gripper_components


def main() -> None:
    point = np.array([114.532, 20.1116, 299.668, 83.5222, 0.17874, 105.607, 2.81435])
    details = gripper_components(point)
    print(f"fun={details['fun']:.6g} feasible={details['feasible']} penalty={details['penalty']:.6g}")
    if not details["feasible"]:
        print("At least one gripper penalty is positive.")


if __name__ == "__main__":
    main()
