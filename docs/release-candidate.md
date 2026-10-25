# Release candidate notes for 0.1.0

Book: *Metaheuristic Optimization with Python: Algorithms, Engineering Applications, and Practical Examples.* Authors, in order: Yuriy Romasevych, Viatcheslav Loveikin, Dmytro Komarchuk. No ISBN, DOI, or publisher is recorded here.

Phase: Validation. Date: 2026-10-25. Base: `main` at `c803af2`.

**This is not a GitHub release.** No tag was created. Book links stay on `/blob/main/` until a tag exists.

## Install

Python 3.11 or 3.12. NumPy at least 2.0.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,notebooks]'
```

There is no pinned cross-platform lock used by GitHub Actions. Local snapshots are `requirements/lock-py311.txt` and `requirements/lock-py312.txt`. Declared dependencies are in `pyproject.toml`: `numpy>=2.0`, `scipy>=1.11`, `matplotlib>=3.8`, plus the `dev` and `notebooks` extras.

## What this candidate contains

- Whitley formula unchanged. Table 4.1 review-copy cells are location 1, value 0.
- Problem 1a is ITAE (`objective_1a_itae`). Settling time and Practical Exercise 1 stay separate.
- Quick validation is not Appendix C or Appendix E. The full protocol is estimated at 945000000 evaluations and was not run.

## Tests and CI already on record

Previous week, 2026-10-20: local pytest 132 passed on Python 3.11.7 (13.29 s) and 3.12.13 (14.89 s). Linux run [39380621540](https://github.com/dmitruyk/Metaheuristic-Optimization-with-Python/actions/runs/39380621540) on merge commit `c803af2` succeeded for test 3.11, test 3.12, and notebooks. `publish-results` was skipped on that `main` push because the workflow refuses to commit logs onto `main`.

Local checks on 2026-10-25 and Linux run [40239854669](https://github.com/dmitruyk/Metaheuristic-Optimization-with-Python/actions/runs/40239854669) on `a36d610` are in `docs/validation-report.md`. Do not describe that run as Appendix C.

## License

`LICENSE` is unchanged as a grant. MIT was not applied. The book stays all rights reserved (`BOOK_LICENSE.md`).

## Known scientific limits

Appendix C and Appendix E remain historical `RandomState` results. Printed search traces are not replayed by `numpy.random.Generator` seeds. Figures under `figures/generated/` are unverified.
