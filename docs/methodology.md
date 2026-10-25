# Methodology

This repository follows the editorial manuscript *Metaheuristic Optimization with Python: Algorithms, Engineering Applications, and Practical Examples* by Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk. Equation images in the DOCX are not text. Appendix B is the executable source for the 54 benchmark formulas and for the experiment implementations of the optimizers. Where Appendix B and a table disagree, `docs/errata.md` records both and the code keeps Appendix B.

## What is minimized

Every public minimizer has the shape

`minimize(objective, bounds, *, rng=None, seed=None, population_size=25, iterations=None, max_evaluations=None) -> OptimizationResult`.

`OptimizationResult` carries `x`, `fun`, `nfev`, `history`, `seed`, `success`, and `message`. `history` is the best-so-far objective value after each completed generation, including the initial population. `nfev` counts objective calls. Non-finite objective values are treated as `+inf` for selection and do not become the reported best unless every value is non-finite.

Pass `seed` or a `numpy.random.Generator`, not both. `seed` is stored on the result. A caller-supplied generator is not asked for its seed; the result then records `seed=None`.

## Budgets

The manuscript loop is `for step in range(2, Iterations + 1)` after an initial sample, so `Iterations` generations are evaluated. For PSO, DE, and GWO that is `population_size * iterations` objective calls. GWOEPD adds `population_size // 2` calls on every generation after the first, because it re-evaluates the replaced wolves. ME-D-PSO can leave an epoch early and start another, so its call count is not `population_size * iterations`.

`max_evaluations` stops a run on a generation boundary. A budget that cannot pay for the initial population raises `ValueError`. Comparisons in `metaopt.experiments.compare` pass the same `max_evaluations` and the same `seed` to every algorithm. That is the fair comparison. Matching the manuscript's iteration count is not the same thing, and the Chapter 5 tables were built from iteration counts.

## Boundary policies

| Algorithm | Policy |
| --- | --- |
| PSO and the PSO variants except where noted | A coordinate outside the box has its velocity component set to 0, then the coordinate is clipped to the nearest bound. |
| BB-PSO | No velocity. The Gaussian sample is clipped. |
| DE/rand/1/bin, DE/best/1/bin, SADE | The donor is clipped to the box before binomial crossover. Trial vectors are inside the box. |
| GWO, mGWO, GWOEPD | The averaged position, and any replacement wolf, is clipped. There is no velocity. |
| SciPy `differential_evolution` | SciPy's own bound handling. It is not the manuscript DE. |

## Coefficients kept from the listings

- PSO, Ring-PSO, von Neumann PSO, VCT-PSO: `w=0.72`, `c1=c2=1.19`. VCT-PSO refreshes the cognitive attractor every 5 generations unless `refresh_period` is set. The chapter listing takes that period as an argument; Appendix B hardcodes 5.
- LDW-PSO: `w_max=0.9`, `w_min=0.4`, `c1=c2=1.19`, with `w = (w_max - w_min) * (iterations - step) / iterations + w_min`.
- IA-PSO: the manuscript position update `x * (1 - rho) + v`, not `x + v`.
- DE: `CR=0.5`, `F=0.6`.
- SADE: shared `F` and `CR`, adapted with `tau1=tau2=0.1`. This is the listing. It is not a strategy-pool SaDE.
- GWO: `a = 2 - 2 * (step / iterations)` with `step` starting at 2.
- mGWO: `a = 2 - 2 * (step / iterations) ** 2`.
- ME-D-PSO default `acceptable_rate=5e-3`, which is the Chapter 5 experiment. Section 1.4.5 also shows a call with `0.01`.

## Benchmarks

`src/metaopt/benchmarks.py` is the Appendix B listing, with these documented edits: Quartic and Xin-She Yang draw uniforms from `seed_benchmark_noise` instead of the global legacy stream; Elliptic raises `ValueError` for `D < 2` because the exponent divides by `D - 1`; Paviani warns, without changing the expression, when a coordinate is outside `(2, 10)`; `outside_domain` reports the registered box; the domain helper rejects a nonpositive dimension. Stochastic noise defaults to `default_rng(0)`.

## What was not run

Appendix C (14 algorithms, 54 functions, 100 runs, population 25, 500 iterations, D=30, base seed 12345 on the legacy stream) and Appendix E (timing, 20 runs, Excel export) were not repeated. A rough count for Appendix C is `14 * 54 * 100 * 25 * 500 = 9.45e8` objective evaluations before GWOEPD's extra half-pack evaluations. No file in `figures/generated/` is a substitute for a book figure.
