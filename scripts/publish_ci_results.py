"""Copy GitHub Actions artifacts into results/ci and write a summary.

The workflow commits that directory. The summary is evidence that the Linux
jobs ran. It is not Appendix C or Appendix E.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path


def assemble(artifact_root: Path, destination: Path, metadata: dict) -> dict:
    """Copy artifact files into ``destination`` and return the summary."""

    destination.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    if artifact_root.is_dir():
        for path in sorted(artifact_root.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(artifact_root)
            # download-artifact uses <artifact-name>/<file>.
            if len(relative.parts) >= 2:
                name = f"{relative.parts[0]}-{relative.name}"
            else:
                name = path.name
            target = destination / name
            shutil.copy2(path, target)
            copied.append(name)
    summary = {
        "schema": 1,
        "matches_appendix_c": False,
        "matches_appendix_e": False,
        "statement": (
            "Linux GitHub Actions output committed by the ci workflow. These files are not a reproduction of Appendix C or Appendix E."
        ),
        "run_id": metadata.get("run_id"),
        "run_url": metadata.get("run_url"),
        "sha": metadata.get("sha"),
        "ref": metadata.get("ref"),
        "event": metadata.get("event"),
        "test_result": metadata.get("test_result"),
        "notebooks_result": metadata.get("notebooks_result"),
        "files": copied,
    }
    (destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: python scripts/publish_ci_results.py ARTIFACT_DIR DESTINATION", file=sys.stderr)
        return 2
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    run_url = f"{server}/{repository}/actions/runs/{run_id}" if repository and run_id else ""
    summary = assemble(
        Path(argv[1]),
        Path(argv[2]),
        {
            "run_id": run_id,
            "run_url": run_url,
            "sha": os.environ.get("GITHUB_SHA", ""),
            "ref": os.environ.get("GITHUB_REF", ""),
            "event": os.environ.get("GITHUB_EVENT_NAME", ""),
            "test_result": os.environ.get("CI_TEST_RESULT", ""),
            "notebooks_result": os.environ.get("CI_NOTEBOOKS_RESULT", ""),
        },
    )
    print(json.dumps({"run_url": summary["run_url"], "files": summary["files"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
