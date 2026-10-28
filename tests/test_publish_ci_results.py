"""The CI publisher copies logs into a committable summary."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "publish_ci_results",
    Path(__file__).resolve().parents[1] / "scripts" / "publish_ci_results.py",
)
_MODULE = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_MODULE)
assemble = _MODULE.assemble


def test_assemble_prefixes_artifact_names_and_marks_the_study(tmp_path: Path):
    artifacts = tmp_path / "artifacts"
    (artifacts / "pytest-3.12").mkdir(parents=True)
    (artifacts / "pytest-3.12" / "pytest.log").write_text("60 passed\n", encoding="utf-8")
    (artifacts / "notebooks").mkdir()
    (artifacts / "notebooks" / "notebooks.log").write_text("executing 01\n", encoding="utf-8")
    destination = tmp_path / "results" / "ci"
    summary = assemble(
        artifacts,
        destination,
        {
            "run_id": "99",
            "run_url": "https://github.com/example/repo/actions/runs/99",
            "sha": "abc",
            "ref": "refs/heads/review",
            "event": "push",
            "test_result": "success",
            "notebooks_result": "success",
        },
    )
    assert (destination / "pytest-3.12-pytest.log").read_text(encoding="utf-8") == "60 passed\n"
    assert summary["matches_appendix_c"] is False
    assert summary["matches_appendix_e"] is False
    saved = json.loads((destination / "summary.json").read_text(encoding="utf-8"))
    assert saved["files"] == ["notebooks-notebooks.log", "pytest-3.12-pytest.log"]
    assert saved["test_result"] == "success"
