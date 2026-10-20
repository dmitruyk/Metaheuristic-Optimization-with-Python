"""Compare library values with published worked scalars.

Appendix C and Appendix E cells are not stored as numbers in this repository.
Those comparisons are reported as unmatched. Worked scalars that the tests
already lock are compared with the relative tolerance 1e-6 and the absolute
tolerance 1e-8, and a row is matched only when both tolerances hold.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from metaopt.applications import cart_pole, crane, mobile_robot, mountain_car, pid

ROOT = Path(__file__).resolve().parents[1]
RELATIVE_TOLERANCE = 1e-6
ABSOLUTE_TOLERANCE = 1e-8


def _close(observed: float, published: float) -> bool:
    scale = max(abs(published), abs(observed), 1.0)
    return abs(observed - published) <= max(ABSOLUTE_TOLERANCE, RELATIVE_TOLERANCE * scale)


def worked_rows() -> list[dict]:
    unstable = pid.objective_1a_itae(*pid.WORKED_1A_UNSTABLE)
    feasible = pid.objective_1a_itae(*pid.WORKED_1A_FEASIBLE)
    settling = pid.objective_1a_settling_time(*pid.WORKED_1A_FEASIBLE)
    rows = [
        _row("Problem 1a ITAE", "(0.1, 1, 9)", unstable, pid.WORKED_1A_UNSTABLE_VALUE),
        _row("Problem 1a ITAE", "(0.276, 0.765, 2.221)", feasible, pid.WORKED_1A_FEASIBLE_VALUE),
        _row("Problem 1b dominant pole", "(0.1, 2, 6)", pid.objective_1b(*pid.WORKED_1B), pid.WORKED_1B_VALUE),
        _row(
            "Robot path",
            "infeasible nodes",
            mobile_robot.path_geometry(mobile_robot.WORKED_INFEASIBLE)["fun"],
            mobile_robot.WORKED_INFEASIBLE_VALUE,
        ),
        _row(
            "Robot path",
            "feasible nodes",
            mobile_robot.path_geometry(mobile_robot.WORKED_FEASIBLE)["fun"],
            mobile_robot.WORKED_FEASIBLE_VALUE,
        ),
        _row(
            "Crane polynomial",
            "infeasible coefficients",
            crane.polynomial_profiles(crane.WORKED_POLY_INFEASIBLE)["fun"],
            crane.WORKED_POLY_INFEASIBLE_VALUE,
        ),
        _row(
            "Crane polynomial",
            "feasible coefficients",
            crane.polynomial_profiles(crane.WORKED_POLY_FEASIBLE)["fun"],
            crane.WORKED_POLY_FEASIBLE_VALUE,
        ),
        _row(
            "Mountain car 4a",
            "feasible",
            float(mountain_car.rollout(mountain_car.WORKED_4A_FEASIBLE, goal="4a")["fun"]),
            float(mountain_car.WORKED_4A_FEASIBLE_VALUE),
        ),
        _row(
            "Mountain car 4b",
            "feasible",
            float(mountain_car.rollout(mountain_car.WORKED_4B_FEASIBLE, goal="4b")["fun"]),
            float(mountain_car.WORKED_4B_FEASIBLE_VALUE),
        ),
        _row(
            "Cart-pole",
            "feasible vector",
            cart_pole.objective(cart_pole.WORKED_FEASIBLE),
            cart_pole.WORKED_FEASIBLE_VALUE,
        ),
        _row(
            "Cart-pole",
            "infeasible vector",
            cart_pole.objective(cart_pole.WORKED_INFEASIBLE),
            cart_pole.WORKED_INFEASIBLE_VALUE,
        ),
    ]
    rows.append(
        {
            "area": "Problem 1a settling-time on the Problem 1a plant",
            "point": "(0.276, 0.765, 2.221)",
            "observed": settling,
            "published": pid.WORKED_1A_FEASIBLE_VALUE,
            "status": "unmatched",
            "reason": (
                "The printed feasible value belongs to the ITAE objective. "
                "The settling-time value is a different criterion and is not expected to match."
            ),
        }
    )
    return rows


def _row(area: str, point: str, observed: float, published: float) -> dict:
    matched = _close(float(observed), float(published))
    return {
        "area": area,
        "point": point,
        "observed": float(observed),
        "published": float(published),
        "absolute_difference": abs(float(observed) - float(published)),
        "relative_tolerance": RELATIVE_TOLERANCE,
        "absolute_tolerance": ABSOLUTE_TOLERANCE,
        "status": "matched" if matched else "unmatched",
    }


def appendix_rows() -> list[dict]:
    return [
        {
            "area": "Appendix C",
            "status": "unmatched",
            "reason": (
                "The printed rank tables and box-plot statistics are not stored as "
                "machine-readable cells in this repository. The quick Generator study "
                "must not be substituted for them."
            ),
        },
        {
            "area": "Appendix E",
            "status": "unmatched",
            "reason": (
                "The printed timing workbook was not recomputed. Historical settings "
                "are 20 runs, population 25, 500 iterations, dimension 30, legacy RandomState."
            ),
        },
    ]


def build_report() -> dict:
    scalar_rows = worked_rows()
    extra_rows = appendix_rows()
    matched = [row for row in scalar_rows if row["status"] == "matched"]
    unmatched = [row for row in scalar_rows if row["status"] != "matched"] + extra_rows
    return {
        "relative_tolerance": RELATIVE_TOLERANCE,
        "absolute_tolerance": ABSOLUTE_TOLERANCE,
        "matched_count": len(matched),
        "unmatched_count": len(unmatched),
        "matches_appendix_c": False,
        "matches_appendix_e": False,
        "rows": scalar_rows + extra_rows,
        "statement": ("Matched rows are worked scalars. Appendix C and Appendix E stay unmatched."),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "published_comparison.json")
    args = parser.parse_args(argv)
    report = build_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"matched {report['matched_count']} unmatched {report['unmatched_count']} matches_appendix_c {report['matches_appendix_c']}")
    print(f"wrote {args.output}")
    failed = [row for row in report["rows"] if row["area"].startswith("Problem 1a ITAE") and row["status"] != "matched"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
