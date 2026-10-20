# Validation report

Phase: Validation. This is a local macOS run, not a GitHub-hosted Linux run and not a live deployment.

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
