# Reproducibility

## What repeats

In one Python process, on one NumPy build, `minimize(..., seed=S)` twice returns the same `history`, the same `x`, and the same `nfev` for PSO, both DE variants, and GWO. `tests/test_reproducibility.py` checks that. A different seed is expected to produce a different history.

Record, with any reported value:

- the integer `seed` or the fact that an external `Generator` was injected
- `population_size`, `iterations`, and `max_evaluations`
- `nfev` (do not compare algorithms on iteration count alone)
- NumPy, SciPy, and Python versions (`docs/validation-report.md` has the versions used for the tests in this checkout)
- the platform string from `platform.platform()`
- for Quartic and Xin-She Yang, the seed passed to `metaopt.benchmarks.seed_benchmark_noise`
- for a constrained example, the penalty components, not only the scalar objective

## What does not repeat the manuscript's search traces

The experiment listing does this:

```python
def run_once_perf(algo, function, Vars, Domain, pop, iters, seed):
    np.random.seed(seed)
    ...
```

and the optimizers then call `np.random.rand` and `np.random.choice`. That is NumPy's legacy `RandomState`.

This library calls `numpy.random.default_rng(seed)`, which is a `Generator` (PCG64). The same integer does not produce the same uniforms. Histories in this repository are therefore not a replay of `raw_benchmark_results.npz`, even if that file is regenerated with `BASE_SEED = 12345`. The change is intentional: the global legacy stream is not used. `docs/errata.md` states it as a correction to the listings, not as a claim that the printed box plots were recomputed.

A second, separate change affects only Quartic and Xin-She Yang. In the manuscript those functions call `np.random.random` on the same global stream the optimizer uses, so each objective evaluation consumes uniforms that the next velocity update would otherwise have used. Here the noise generator is independent. Search paths on those two functions differ for that reason as well.

## Tolerances

Worked scalar examples that were checked are compared in `tests/test_examples_smoke.py`. Deterministic printed values that match in this environment use a relative tolerance of `1e-6` or an absolute tolerance of `1e-8` or tighter, as written in that file. The crane "feasible" coefficient vector exceeds the speed limit by about `6e-8` m/s; the scalar objective still matches the printed value. See the errata.

Benchmark reference checks use the locations in Table 4.1 where the location is a simple vector (origin, ones, or a named constant). `results/reference_minima.csv` is the output of `scripts/reproduce_tables.py`. It is a reference-value check, not Appendix C.

## Figures

`scripts/reproduce_figures.py` writes plots under `figures/generated/` with `unverified` in the file name. They are not copies of Appendix A and they are not claimed to match any printed curve.

## Two profiles (neither one is Appendix C or Appendix E)

`python scripts/handbook_experiment.py --profile quick` writes `results/quick_validation_summary.json`. On 2026-10-20 that run took 0.032 s on Python 3.11.7, used PSO, DE/rand, and GWO, Spherical and Rastrigin, dimension 5, population 8, 64 evaluations, 2 runs, seeds 12345 and 12346, `Generator`. `matches_appendix_c` is false.

`python scripts/handbook_experiment.py --profile full` writes `results/full_experiment_cost_estimate.json` and does not start the run. The nominal count is `14 * 54 * 100 * 25 * 500 = 945000000` objective evaluations. The hour range in that file is 8.75–65.625 hours on the 2026-10-19 timing assumptions (30000 and 4000 evaluations per second). Appendix E at 20 runs would be about one fifth of that, still hours. `scripts/compare_published_values.py` writes `results/published_comparison.json`. On this date it matched 11 worked scalars and left Appendix C, Appendix E, and the settling-time value unmatched. Tolerances are relative `1e-6` and absolute `1e-8`.

The manuscript sizes, seeds, and the legacy-versus-Generator distinction are in `docs/experiment-protocol.md`.

## Reduced study (not Appendix C or Appendix E)

`python scripts/reduced_statistical_comparison.py` writes `results/reduced_comparison_summary.json`, a copy named for the Python version, and the matching CSV files. The protocol is PSO, DE/rand, and GWO on Spherical and Rastrigin, dimension 5, population 8, 64 evaluations, 5 runs, seeds `12345` through `12349`, using `Generator`. The JSON field `matches_appendix_c` is false. The same field is false for Appendix E. Wall-clock seconds in that file are timings of this reduced protocol only. `requirements/lock-py312.txt` is a macOS snapshot of the Python 3.12 environment used for local validation; its header records the Python version, platform, and date. It is not the Linux CI install.

Paviani outside `(2, 10)` warns and returns a non-finite value. `outside_domain` and `evaluate_benchmark` check the registered box. Neither function changes an Appendix B formula. Quartic noise is uniform on `[0, 1)` and advances a generator that is separate from the optimizer, so two calls differ until `seed_benchmark_noise` is called again.
