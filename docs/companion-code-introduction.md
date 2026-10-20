# Companion code

Phase: Validation. Date: 2026-10-20.

This is the short introduction for readers of *Metaheuristic Optimization with Python*. The same paragraphs are inserted into the local review copy of the manuscript by `scripts/prepare_reviewed_manuscript.py`.

## Install

Python 3.11 or 3.12 is required. NumPy must be at least 2.0.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,notebooks]'
pytest -q
```

The repository is <https://github.com/dmitruyk/Metaheuristic-Optimization-with-Python>. No release tag has been published. Links use `/blob/main/` and will move when `main` moves. A QR code is not included, because a code aimed at moving `main` would send a printed reader to a later commit.

Chapter paths are listed in `docs/book-code-map.md`.

## What repeats, and what does not

`minimize(..., seed=S)` repeats on one NumPy build. The handbook's search traces used `np.random.seed`. The same integer does not replay Appendix C or Appendix E. Those printed results stay historical until a new Generator study is run and labeled as a replacement. The quick validation file is not that study.

Problem 1a in Section 6.3 minimizes ITAE (`objective_1a_itae`). Practical Exercise 1 minimizes settling time for the plant `1/(1+s)**3`.
