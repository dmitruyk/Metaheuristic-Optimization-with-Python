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
