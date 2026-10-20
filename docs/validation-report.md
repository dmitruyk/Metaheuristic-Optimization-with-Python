# Validation report

Phase: Validation.

## Current status (2026-10-20 UTC)

This section is the latest evidence. The sections below it are historical local notes from 2026-10-19 and are not restated as the current CI result.

Time range of the checks in this section: 2026-10-20 05:55–05:56 UTC for GitHub Actions, and the local session on 2026-10-19 22:57 America/Los_Angeles onward. Data source: this checkout and the GitHub Actions API for `dmitruyk/Metaheuristic-Optimization-with-Python`. Execution: local computation on one Mac, plus GitHub-hosted `ubuntu-latest`. Not paper trading and not live execution.

| Metric | Previous review (2026-10-19) | This status | Delta |
| --- | --- | --- | --- |
| `pytest -q` on Python 3.11.7 | 60 passed, 15.79 s | 132 passed, 13.29 s | +72 tests |
| `pytest -q` on Python 3.12.13 | 60 passed, 43.83 s | 132 passed, 14.89 s | +72 tests |
| Linux CI on `main` | described in the historical section as not yet observed | run [39377458555](https://github.com/dmitruyk/Metaheuristic-Optimization-with-Python/actions/runs/39377458555) on `0fc55d5` succeeded for test 3.11, test 3.12, and notebooks | main is verified |
| Linux CI on this branch | not started | run [39379558457](https://github.com/dmitruyk/Metaheuristic-Optimization-with-Python/actions/runs/39379558457) on `e6940ba` succeeded for test 3.11, test 3.12, notebooks, and publish-results | this branch is verified for that commit |
| Committed CI log | `results/ci/summary.json` for `e85e014` | still that file; the workflow skips the results commit on `main` | the green main run is not copied into `results/ci/` |
| Appendix C / Appendix E | not run | still not run; cost estimate is `results/full_experiment_cost_estimate.json` | labeled historical |
| Worked scalars | matched in tests | 11 matched, 3 unmatched in `results/published_comparison.json` | Appendix C, Appendix E, and the settling-time value stay unmatched |

`main` at `0fc55d5` passed GitHub Actions. This branch at `e6940ba` also passed, in run 39379558457. The workflow then wrote `results/ci/summary.json` as commit `d37e243`. A `GITHUB_TOKEN` push does not start another run, so `d37e243` is the log of `e6940ba`, not a separate test. Run `39377406220` (pull request, commit `d0b5c29609`) is recorded as a failure, and the jobs API returned zero jobs. Logs for that run returned HTTP 403 without authentication, so the failure has no job log in this session. It is not evidence that pytest failed. The next commit on `main` passed.

Local commands for the library changes on this branch:

```bash
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest -q
.venv/bin/python scripts/handbook_experiment.py --profile quick
.venv/bin/python scripts/handbook_experiment.py --profile full
.venv/bin/python scripts/compare_published_values.py
MPLBACKEND=Agg MPLCONFIGDIR=.cache/matplotlib IPYTHONDIR=.cache/ipython JUPYTER_CONFIG_DIR=.cache/jupyter .venv/bin/python scripts/execute_notebooks.py
```

Python 3.11.7, NumPy 2.4.6, platform `macOS-26.6.2-x86_64-i386-64bit`. Pytest: 132 passed in 13.29 s. The same tree on Python 3.12.13: 132 passed in 14.89 s. Notebooks 01–10: exit code 0. Quick validation: 0.032 s, `matches_appendix_c` false, file `results/quick_validation_summary.json`. Full profile: not executed. Nominal cost 945000000 objective evaluations, about 8.8–65.6 hours at 30000 and 4000 evaluations per second. `scripts/validate_doc_links.py` on the local review DOCX: 0 missing repository paths, 8 external citation links not fetched.

LibreOffice 6.3.4.2 (`60da17e045e08f1793c57c00ba83cdfce946d0aa`) aborts with signal 6 on this Mac before it opens a file. The same abort happens for the editorial source DOCX and for `manuscript/Metaheuristic_Optimization_with_Python_reviewed.docx`. No PDF was written. Page-by-page visual QA is therefore not done in this session. KDP approval stays pending.

## Historical local report

Phase: Validation. This historical section is a local macOS run, not a GitHub-hosted Linux run and not a live deployment. It is kept so the earlier numbers stay next to the current ones. Do not read its "Linux CI not observed" sentences as the current status; run 39377458555 supersedes them.

## Environment

| Item | Value |
| --- | --- |
| Date | 2026-10-19 (local session continuing into 2026-10-20 UTC) |
| Platform | macOS-26.6.2-x86_64-i386-64bit |
| Python | 3.11.7 |
| NumPy | 2.4.6 |
| SciPy | 1.17.1 |
| Matplotlib | 3.11.2 |
| SymPy | 1.14.0 |
| pandas | 3.0.6 |
| Data source | Editorial DOCX `Metaheuristic_Optimization_with_Python_Editorial_Edition.docx`, plus executions in this checkout |
| Execution | Local computation. Not paper trading and not live execution. |

Python 3.12 and Ubuntu were not executed in this session. `.github/workflows/ci.yml` runs both on Linux. That workflow has not been observed here.

## Commands

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -e '.[dev,notebooks]'
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest -q
.venv/bin/python scripts/reproduce_tables.py
MPLBACKEND=Agg MPLCONFIGDIR=.cache/matplotlib .venv/bin/python scripts/reproduce_figures.py
MPLBACKEND=Agg MPLCONFIGDIR=.cache/matplotlib IPYTHONDIR=.cache/ipython .venv/bin/python scripts/execute_notebooks.py
```

## Results

| Check | Result |
| --- | --- |
| Editable install of `.[dev,notebooks]` | Passed on Python 3.11.7 |
| `ruff check .` and `ruff format --check .` | Passed |
| `pytest -q` | 37 passed, 1 warning, 11.68 s |
| Notebooks 01–10, clean kernel, top to bottom | Passed (exit code 0). Outputs were not written back into the notebooks. |
| Same seed, PSO / DE/rand / DE/best / GWO | Histories identical across two calls; a different seed differed. Test seed 12345, population 10, 7 iterations, sphere in 3 variables. |
| Appendix C / Appendix E | Not run |

The pytest warning is `RuntimeWarning: invalid value encountered in log` from Paviani at `x = 0`, which is outside its open domain `(2, 10)`. That is the expected edge-case check.

Notebook 05 uses population 9 and `max_evaluations=90` on the sphere. Those objective values are smoke results. They are not Appendix C.

## Worked scalars

Seeds do not apply: these are direct evaluations of the printed points.

| Example | Printed | Observed | Absolute difference |
| --- | --- | --- | --- |
| Section 1.3, ten-variable objective | 12.3901 | 12.3901 | 0 |
| Problem 1a at (0.1, 1, 9) | 19655252.199124742 | matches within relative 1e-6 | test passed |
| Problem 1a at (0.276, 0.765, 2.221) | 18.796046141402556 | matches within relative 1e-5 | test passed; feasible (value &lt; 100) |
| Problem 1b at (0.1, 2, 6) | -0.036514370221270194 | matches within relative 1e-6 | test passed |
| Robot path, crossing nodes | 35571448004.83873 | 35571448004.83873 | 0; infeasible |
| Robot path, clear nodes | 14.74322171254588 | 14.74322171254588 | 0; feasible |
| Crane coefficients (-6, 9, 20, 5, 5, 60, 0) | 707599.2688799157 | 707599.2688799157 | 0; infeasible |
| Crane coefficients (-5, 6, 10, -2, 5, 20, -4) | 0.4209773021079328 | 0.4209773021079328 | 0; speed excess about 6.4e-8 m/s |
| Mountain-car feasible 4a / 4b | 90 and 145 | 90 and 145 | 0 |
| Cart-pole feasible vector | 4.350040156962044 | matches within relative 1e-8 | feasible |
| Cart-pole infeasible vector | 1224151813560.341 | matches within relative 1e-8 | infeasible |

Reference minima at Table 4.1 locations are in `results/reference_minima.csv` (regenerate with `scripts/reproduce_tables.py`). Largest gap in that file is Styblinski–Tang: observed `-156.66466` at `x_i = -2.903534` in 4 variables, against `-39.16599 * 4 = -156.66396`. The table's rounded `-39.166 D` is `-156.664`. The code was not changed. Schwefel 2.26 at `420.968746359982015` differs from `-418.9828872724338` by `6e-14`.

## Objective-evaluation accounting in the tests

Canonical PSO on the sphere, seed 1, population 20, 40 iterations: `nfev = 800`. A budget of 24 with population 8 stops at `nfev = 24`. GWOEPD with population 10 and 4 iterations: `nfev = 10 + 3 * 15 = 55`.

## Figures

`figures/generated/` contains library plots only. File names for the benchmark drawings include `unverified`. They are not substitutes for Appendix A or Figure 1.8. The PID, robot, and crane example plots are evaluations of the printed inputs, not traced copies of the book's figures.

## Known failures

- Appendix C box plots and rank tables: not computed.
- Appendix E timing workbook: not computed.
- Legacy `np.random.seed(12345)` traces: not reproduced, by design. See `docs/reproducibility.md`.
- Python 3.12 and Linux CI: configured, not observed.
- License: not chosen. On 19 October 2026 Dmytro Komarchuk approved creating this companion repository and is listed last in `LICENSE`. That approval does not name MIT, Apache-2.0, GPL, or another open-source license.
- Paviani outside `(2, 10)` returns NaN. Elliptic with one variable raises `ValueError`.

## Completion

Local Python 3.11 checks of the library, the worked scalars, and the smoke notebooks are done. Numerical reconciliation with the manuscript's optimizer tables is not done. Counting Appendix C and Appendix E as the unpublished performance claim, that claim is 0% verified. Counting the acceptance checks that can be run on this machine, the 3.11 local set passed and the 3.12/Linux matrix did not run.

## Publication-readiness verdict

Not ready to publish as a reproduction of the handbook's experimental tables, and not ready to publish as an openly licensed repository.

Blockers:

1. Authors have not approved a license. Do not add MIT, Apache, or GPL until they do. Do not invent a GitHub URL.
2. Appendix C and Appendix E have not been recomputed, and they cannot be recomputed bit-for-bit without the legacy random stream. Either rerun them under `Generator` and replace the printed tables with a clearly labeled new experiment, or keep an optional legacy `RandomState` path and show the difference. This repository does not do either of those for the full study.
3. Table 4.1 Whitley (location 0, value 1) disagrees with Appendix B (value 0 at the all-ones vector). An editor has to pick one. The code follows Appendix B.
4. Problem 1a has two listings (ITAE, and settling time). Section 6.3 should say which one was minimized.
5. Confirm Python 3.12 on Linux by running the workflow.

Exact fixes for the book are in `docs/errata.md`.

## Review run on 2026-10-19

Phase: Validation. This section is new evidence from the branch `review/reproducibility-2026-10-19`. The tables above are the previous local report and are not restated as if they were rerun.

Time range: 2026-10-20 05:28–05:43 UTC (2026-10-19 22:28–22:43 America/Los_Angeles). Data source: this checkout, plus `Metaheuristic_Optimization_with_Python_Editorial_Edition.docx` from `~/Downloads` (not stored in the repository). Execution: local computation on one Mac. Not paper trading and not live execution. Not a GitHub-hosted Linux run.

### Previous metrics beside this run

| Metric | Previous report | This review | Delta |
| --- | --- | --- | --- |
| `pytest -q` | 37 passed, 1 warning, 11.68 s, Python 3.11.7 only | 60 passed, 15.79 s on Python 3.11.7; 60 passed, 43.83 s on Python 3.12.13 | +23 tests; the Paviani log warning is now an explicit `RuntimeWarning` asserted by a test |
| Notebooks 01–10 | Passed; elapsed time not recorded | Exit code 0 in 20 s (3.11.7) and 23 s (3.12.13). Outputs were not written back | timing added |
| `ruff check` and `ruff format --check` | Passed | Passed on both interpreters with ruff 0.17.1. On 3.12 each command was under 1 s | same result |
| Appendix C / Appendix E | Not run | Still not run. Reduced study below is a different experiment | full tables remain unverified |
| Python 3.12 | Not executed | Executed locally on macOS. Linux Actions not yet observed | local only |
| License and author order | Unapproved license; Komarchuk listed last | Unchanged | none |

### Commands and results

Python 3.11.7, NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.2, SymPy 1.14.0, pandas 3.0.6, ruff 0.17.1, platform `macOS-26.6.2-x86_64-i386-64bit`, 16 CPUs.

```bash
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest -q
MPLBACKEND=Agg MPLCONFIGDIR=.cache/matplotlib .venv/bin/python scripts/reproduce_tables.py
MPLBACKEND=Agg MPLCONFIGDIR=.cache/matplotlib .venv/bin/python scripts/reproduce_figures.py
.venv/bin/python scripts/reduced_statistical_comparison.py
MPLBACKEND=Agg MPLCONFIGDIR=.cache/matplotlib IPYTHONDIR=.cache/ipython JUPYTER_CONFIG_DIR=.cache/jupyter .venv/bin/python scripts/execute_notebooks.py
.venv/bin/python scripts/validate_doc_links.py
```

| Check | Result |
| --- | --- |
| `ruff check .` and `ruff format --check .` | Passed |
| `pytest -q` | 60 passed, 15.79 s |
| `scripts/reproduce_tables.py` | Exit 0, about 1 s. Wrote `results/reference_minima.csv` |
| `scripts/reproduce_figures.py` | Exit 0, about 2 s. Files under `figures/generated/` stay unverified |
| `scripts/reduced_statistical_comparison.py` | Exit 0, 0.1084 s inside the script. See `results/reduced_comparison_py3.11.7.json` |
| `scripts/execute_notebooks.py` | Exit 0, 20 s, notebooks 01–10 |
| `scripts/validate_doc_links.py` on the Downloads DOCX | 0 missing repository paths. The file has 8 external citation links and no `github.com` or `metaopt` text, so the seven chapter-title repository links are not in this DOCX |

Python 3.12.13, NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2, SymPy 1.14.0, pandas 3.0.6, ruff 0.17.1, same platform string.

```bash
.cache/venv312/bin/ruff check .
.cache/venv312/bin/ruff format --check .
.cache/venv312/bin/pytest -q
.cache/venv312/bin/python scripts/reproduce_tables.py
.cache/venv312/bin/python scripts/reproduce_figures.py
.cache/venv312/bin/python scripts/reduced_statistical_comparison.py
.cache/venv312/bin/python scripts/execute_notebooks.py
```

| Check | Result |
| --- | --- |
| `ruff check .` | Passed, under 1 s |
| `ruff format --check .` | 63 files already formatted, under 1 s |
| `pytest -q` | 60 passed, 43.83 s |
| Reproduction scripts together | Exit 0, about 3 s. Reduced script 0.0895 s. File: `results/reduced_comparison_py3.12.13.json` |
| Notebooks 01–10 | Exit 0, 23 s |

The 30 objective values and `nfev` counts in the two reduced JSON files were equal. That is agreement between these two local NumPy builds on this protocol. It is not agreement with Appendix C.

`results/reduced_comparison_summary.json` is whichever interpreter ran the script last. In this session that was Python 3.12.13. Use the versioned JSON files when quoting a number.

Grouped medians (identical in both files): Spherical PSO 1.6932, DE/rand 5.58251, GWO 1.7852; Rastrigin PSO 28.2014, DE/rand 38.2869, GWO 23.0007. Every run used `nfev` 64. These are not printed handbook cells.

Dependency snapshots: `requirements/lock-py311.txt` and `requirements/lock-py312.txt`. They record this Mac. They are not the install used by `.github/workflows/ci.yml`.

### Verdict for this review

No-go for a tagged release and no-go for a KDP-ready claim. Rationale and owners are in `docs/release-readiness.md`. Stakeholders who have to decide the open items: Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk.

Blockers that this run did not close:

1. License still unnamed. Author order in the repository was not changed.
2. Appendix C and Appendix E were not recomputed. The reduced study is labeled `matches_appendix_c: false` and `matches_appendix_e: false`.
3. Whitley and the Problem 1a objective remain editor decisions. Text is in `docs/manuscript-replacements.md`.
4. Linux GitHub Actions for Python 3.11 and 3.12 has not been observed yet. Local macOS success is not that observation.
5. The Downloads DOCX has eight external citation links and no repository links under the chapter titles. Repository markdown relative links had no missing targets. A later linked DOCX still needs the same check.
6. No page-by-page visual check of a print PDF was done.
