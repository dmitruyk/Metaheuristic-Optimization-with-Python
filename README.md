# Metaheuristic Optimization with Python

Companion code for the handbook by **Yuriy Romasevych**, **Viatcheslav Loveikin**, and **Dmytro Komarchuk** (independently published, 2026). The algorithms, benchmark formulas, and engineering models follow the manuscript. This repository does not replace PSO, DE, or GWO with an unrelated package.

No public repository URL is stated here. The authors have not approved a license; see `LICENSE`.

## Five-minute setup

Python 3.11 or 3.12 is required. NumPy must be at least 2.0 because the PID listing calls `numpy.trapezoid`.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev,notebooks]'
pytest -q
python examples/pid_tuning.py
```

The editable install puts the package on the path. Notebooks live in `notebooks/` and call `src/metaopt` rather than reimplementing the algorithms.

## Run a first example

Sphere in two variables, canonical PSO, seed 1, 20 particles, 30 generations (600 objective evaluations):

```python
import numpy as np
from metaopt.pso import minimize


def sphere(x):
    return float(np.sum(np.square(x)))


result = minimize(sphere, [[-5, 5], [-5, 5]], seed=1, population_size=20, iterations=30)
print(result.fun, result.nfev, result.x)
```

`result.history` is the best value after each generation, including the initial sample.

## Where the chapters went

| Handbook | Code |
| --- | --- |
| Chapter 1, PSO and its variants | `src/metaopt/pso.py`, `src/metaopt/variants/` |
| Chapter 2, DE/rand/1/bin, DE/best/1/bin, SADE | `src/metaopt/de.py`, `src/metaopt/variants/sade.py` |
| Chapter 3, GWO, mGWO, GWOEPD | `src/metaopt/gwo.py`, `src/metaopt/variants/mgwo.py`, `src/metaopt/variants/gwoepd.py` |
| Chapters 4–5 and Appendix B, 54 benchmarks | `src/metaopt/benchmarks.py` |
| Chapter 6, PID, robot, crane, mountain car, cart-pole | `src/metaopt/applications/`, `examples/` |
| Chapter 7, pressure vessel, gripper, beam listings | `src/metaopt/applications/engineering_design.py` |
| SciPy's differential evolution, not the handbook DE | `examples/scipy_differential_evolution.py` |

Notebooks `01` through `10` follow that order. `docs/book-code-map.md` lists manuscript listings, tables, and figures.

## How to cite

Cite the handbook. A machine-readable record is in `CITATION.cff`:

Romasevych, Yuriy, Loveikin, Viatcheslav, and Komarchuk, Dmytro. *Metaheuristic Optimization with Python: Algorithms, Reproducible Experiments, and Engineering Applications.* 2026.

## Reproducibility

Read `docs/reproducibility.md` before comparing a run with a printed table. Short version:

- Pass `seed=` or an explicit `numpy.random.Generator`. The same seed repeats objective values and histories in the same NumPy version.
- The handbook seeds the legacy global stream with `np.random.seed`. This library does not. Equal integers therefore do not replay the printed search traces.
- Compare algorithms by `max_evaluations`, not only by iteration count. GWOEPD evaluates the replaced wolves again, and ME-D-PSO can stop an epoch early.
- Quartic and Xin-She Yang draw noise from a separate generator (`metaopt.benchmarks.seed_benchmark_noise`). In the manuscript they share the optimizer's global stream.
- Appendix C and Appendix E were not rerun. Nothing in `figures/generated/` is marked as a match to a book figure.

## Troubleshooting

`ModuleNotFoundError: metaopt` — install with `python -m pip install -e '.[dev,notebooks]'` from the repository root, or set `PYTHONPATH=src`.

`np.trapezoid` missing — the environment is on NumPy 1.x. Install NumPy 2.

`von Neumann PSO requires a square population` — use 9, 16, 25, or another square. The handbook experiments use 25.

PID import error mentioning SymPy — install the `notebooks` or `dev` extra. The core PSO/DE/GWO modules do not import SymPy.

A design example prints `infeasible` — the penalty terms are nonzero. The script is reporting the manuscript constraint, not hiding it.

Notebook output differs from a figure in the book — expected. See the reproducibility note above. Do not overwrite the book's figures with these plots.
