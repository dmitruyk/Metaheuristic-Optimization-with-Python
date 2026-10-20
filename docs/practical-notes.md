# Practical notes for readers

Phase: Validation. Date: 2026-10-20.

These notes sit beside the manuscript. They do not add algorithms. The handbook's depth is unchanged.

1. **Environment.** Use Python 3.11 or 3.12 and NumPy 2, in a virtual environment. Do not let a listing run `pip install`. See `docs/companion-code-introduction.md`.
2. **Parameters.** PSO uses `w=0.72`, `c1=c2=1.19` unless the variant says otherwise. DE uses `CR=0.5`, `F=0.6`. SADE in this book adapts one shared `F` and `CR`; it is not a strategy-pool SaDE. GWO decreases `a` from 2 toward 0. The coefficients are in `docs/methodology.md`.
3. **Convergence curves.** `result.history` is the best value after each generation, including the initial sample. A log plot that falls and then flattens has stopped improving the best-so-far value. It has not proved that the point is the global minimum.
4. **Fair comparisons.** The Chapter 5 tables use the same iteration count. GWOEPD spends extra evaluations, and ME-D-PSO can stop early. `metaopt.experiments.compare` gives every algorithm the same `max_evaluations`. Say which budget you used.
5. **Choosing an optimizer.** Start with canonical PSO or DE/rand on a smooth bound problem, and use the benchmark chapter when the surface is multimodal. The Chapter 6 recommendation list is a historical result of that study, not a universal ranking.
6. **Constraints.** The engineering examples add penalties to the objective. A feasible flag is a separate report (`violation` returns 0 when the point is allowed). A tiny penalty can be roundoff; the crane speed excess of about `6e-8` m/s is the worked example.
7. **Numerical mistakes.** Elliptic is undefined for one variable. Paviani's logarithms need the open interval `(2, 10)`. Alpine No. 2 is not real for a negative coordinate. Non-finite objective values are ignored for selection. Schwefel 2.23 overflows to infinity far outside its box; the formula is unchanged.
8. **Seeds.** Pass `seed` or a `Generator`, not both. Quartic and Xin-She Yang use `seed_benchmark_noise`, separate from the optimizer.
9. **SciPy.** `examples/scipy_differential_evolution.py` calls SciPy. It is not DE/rand/1/bin from Chapter 2. Report it as a baseline, not as the handbook DE.
