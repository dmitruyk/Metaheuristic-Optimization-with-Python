"""Run a handbook experiment profile, or only estimate the full profile.

``--profile quick`` is the GitHub Actions smoke study. It uses
``numpy.random.Generator`` and writes ``matches_appendix_c: false``.

``--profile full`` prints the cost of the manuscript-sized Generator protocol
and does not run it. ``--confirm-expensive`` is required before that protocol
runs, and this script still labels the result as a Generator study rather
than as Appendix C or Appendix E.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path

import numpy as np

from metaopt import __version__
from metaopt.reproduction import estimate_full_cost, run_quick

ROOT = Path(__file__).resolve().parents[1]


def _environment() -> dict:
    return {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "metaopt": __version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
    }


def _write(payload: dict, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {destination}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("quick", "full"), default="quick")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--confirm-expensive",
        action="store_true",
        help=("Record that the cost was acknowledged. This entry point still does not start the multi-hour run."),
    )
    args = parser.parse_args(argv)

    if args.profile == "full":
        estimate = estimate_full_cost()
        estimate["environment"] = _environment()
        estimate["executed"] = False
        low, high = estimate["hour_range"]
        print(
            f"Full Generator protocol nominal evaluations: {estimate['objective_evaluations_nominal']}. "
            f"Rough wall-clock range on a 2026-10-19 laptop-class CPU: {low:.1f}–{high:.1f} hours. "
            "Appendix E would add another timing pass at 20 runs."
        )
        destination = args.output or (ROOT / "results" / "full_experiment_cost_estimate.json")
        if not args.confirm_expensive:
            estimate["statement"] = estimate["statement"] + " This invocation did not run the protocol."
            _write(estimate, destination)
            print("Full protocol not started. Cost estimate only.")
            return 0
        estimate["executed"] = False
        estimate["statement"] = (
            "Refusing to launch the multi-hour protocol from this entry point. "
            "The estimate is the deliverable until a scheduled run is approved. "
            "A future run must keep matches_appendix_c false unless it is compared "
            "with the printed cells under an explicit tolerance."
        )
        _write(estimate, destination)
        print("Full protocol was not started.")
        return 0

    payload = run_quick()
    payload["environment"] = _environment()
    payload["matches_appendix_c"] = False
    payload["matches_appendix_e"] = False
    destination = args.output or (ROOT / "results" / "quick_validation_summary.json")
    _write(payload, destination)
    print(payload["statement"])
    print(f"elapsed_seconds {payload['elapsed_seconds']:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
