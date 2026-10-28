# Code validation

> Editorial tooling note: the scripts named in this report (`scripts/editorial/…`, `tests/test_editorial_tools.py`) and the edit records are the editor's working tools. They are kept on the fork branch `dtkachenko:editorial/manuscript-edit-2026-10-27` and are not part of this pull request; the manuscript binaries are never committed.

Phase: Validation. Date: 2026-10-27. Branch `editorial/manuscript-edit-2026-10-27` (fork `dtkachenko/Metaheuristic-Optimization-with-Python`), started from upstream `main` at `a3725fe`.

This pass changed no algorithm, benchmark, application or notebook code. It standardised the supported Python version on 3.12 and added editorial tooling under `scripts/editorial/` with its own tests. Every result below was produced on this machine unless a GitHub Actions run is named.

## Environment

| Item | Value |
| --- | --- |
| Machine | Apple Silicon Mac, macOS 27.2 (arm64) |
| Python | 3.12.13 (`~/.local/bin/python3.12`, uv-managed) in `.venv` |
| NumPy / SciPy / Matplotlib | 2.5.4 / 1.18.1 / 3.11.2 |
| pandas / SymPy | 3.1.0 / 1.14.0 |
| pytest / ruff | 9.2.0 / 0.17.3 |
| Lock | `requirements/lock-py312.txt`, regenerated 2026-10-27 from this venv (`pip freeze`); not a Linux lock |

## Python 3.12 standardisation (commit `chore: standardise on Python 3.12`)

| Change | Before | After |
| --- | --- | --- |
| `.python-version` | 3.11 | 3.12 |
| `pyproject.toml` `requires-python` | `>=3.11` | `>=3.12` |
| `pyproject.toml` ruff `target-version` | py311 | py312 |
| `.github/workflows/ci.yml` test matrix | 3.11, 3.12 | 3.12 |
| `.github/workflows/ci.yml` notebooks job | 3.11 | 3.12 |
| `requirements/` | `lock-py311.txt`, `lock-py312.txt` (2026-10-19, x86_64) | `lock-py312.txt` (2026-10-27, arm64) |
| README, `docs/companion-code-introduction.md`, `docs/practical-notes.md`, `docs/release-candidate.md`, `docs/reproducibility.md`, `docs/release-readiness.md`, `docs/validation-report.md` (one sentence), `scripts/prepare_reviewed_manuscript.py` | "Python 3.11 or 3.12" / `python3.11 -m venv` | "Python 3.12" / `python3.12 -m venv` |
| `tests/test_publish_ci_results.py` | fixture artifact `pytest-3.11` | `pytest-3.12` |
| Manuscript ¶58 | "Install Python 3.11 or newer" | "Install Python 3.12" (tracked change, FM-02) |

Historical records of earlier runs on 3.11 (`docs/validation-report.md`, `docs/final-audit.md`, `docs/final-change-summary.md`, `results/ci/*`, `results/*py3.11*`) were left as written. No notebook records a Python version in its metadata; `CITATION.cff` names none.

## Results on this machine

| Check | Command | Result |
| --- | --- | --- |
| Baseline before any change | `.venv/bin/python -m pytest -q` | 134 passed in 33.55 s |
| After the 3.12 change | `.venv/bin/python -m pytest -q` | 134 passed in 5.56 s |
| With the editorial tests | `.venv/bin/python -m pytest -q` | 137 passed (134 + `tests/test_editorial_tools.py`: 3) |
| Lint | `.venv/bin/ruff check .` and `.venv/bin/ruff format --check .` | all checks passed; 76 files already formatted |
| Documentation links | `.venv/bin/python scripts/validate_doc_links.py` | markdown relative links missing: 0 |
| Notebooks 01–10 | `.venv/bin/python scripts/execute_notebooks.py` (the CI command) | all 10 executed from a clean kernel, exit 0, 10.5 s wall; notebooks unmodified |
| Manuscript listings | `scripts/verify_book_code.py` on the edited manuscript | see `chapter-review.md` (run after the tracked changes were applied) |

GitHub Actions on this branch: to be recorded in `publication-readiness.md` once the branch is pushed; the matrix is now 3.12 only.

## Editorial tooling

- `scripts/editorial/editorial_docx.py`, `extract_paragraphs.py`, `apply_tracked_edits.py`: standard library only (`lxml` was installed in the venv solely to run the docx validator, and is not a project dependency).
- `tests/test_editorial_tools.py` builds a small WordprocessingML body with the manuscript's constructs (plain paragraph, two-column listing table, embedded object, hyperlink, heading, stale TOC table) and checks: code cells are refused, the accepted view equals the new text, the rejected view equals the original text, run formatting and objects survive, inserted paragraphs and style changes are marked, every revision has author/date/unique id.
- Smoke run on the real manuscript (three edits) and the trial run (108 structural and front-matter edits, 759 tracked segments): the docx validator reports `All validations PASSED` with `--original … --author "Editorial (Claude)"`, i.e. XSD-clean and no text changed outside a tracked revision.

## What this pass did not validate

- The Appendix C and Appendix E experiments (not rerun; see `docs/experiment-protocol.md`).
- Chapter 6 optimizer-run tables (Table 6.2) and Chapter 7's 500-run statistics: stochastic, not rerun.
- Equation images: not machine-readable.
- Printed listings were parsed (`ast.parse`) by the reviewers chapter by chapter; the ones that do not parse are recorded in `scientific-corrections.md` (SADE fragment ¶1535, Table 3.1 code column as extracted, Chapter 4 Exercise 1 `function` undefined).
