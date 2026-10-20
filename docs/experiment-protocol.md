# Experiment protocol

Phase: Validation. Date: 2026-10-20.

Parameters below were read from `Metaheuristic_Optimization_with_Python_Editorial_Edition.docx` (modified 2026-10-15, 29201623 bytes). They are not taken from `Documents/HANDBOOK.docx`, which is an older file and does not contain `BASE_SEED`.

## Appendix C, historical

Source: Chapter 5 prose ("D=30", 100 runs, population 25, 500 iterations) and Appendix B cell "SETTINGS AND RUN - ALGORITHMS SEARCH PERFORMANCE".

| Item | Value |
| --- | --- |
| Algorithms | PSO, LDW-PSO, IA-PSO, BB-PSO, VCT-PSO, ME-D-PSO, Ring-PSO, vN-PSO, DE/best, DE/rand, SADE, GWO, mGWO, GWOEPD |
| Benchmarks | the 54 names in `metaopt.benchmarks.BENCHMARKS` |
| Dimension | 30 |
| Population | 25 |
| Iterations | 500 |
| Runs | 100 |
| Base seed | 12345 |
| Seed | `BASE_SEED + 100000 * problem_index + 1000 * algorithm_index + run` |
| Random stream | `np.random.seed` then `np.random.rand` inside the listings |
| ME-D-PSO rate | `5e-3` |
| Stopping | iteration count. GWOEPD re-evaluates replaced wolves, so `nfev` is not `25 * 500` for every algorithm |
| Output named in the listing | `raw_benchmark_results.npz` |

A Chapter 4 snippet also prints `Dimension = 10` next to `Runs = 100`. The performance cell and the Chapter 5 paragraph that introduces Appendix C both set dimension 30. The protocol used here for Appendix C is dimension 30. The dimension-10 line is a different, smaller example.

`src/metaopt/reproduction.py` yields the same sizes and the same seed formula with `matches_appendix_c: false` and `rng` set to `Generator`. That schedule is `iter_full_jobs`. It does not evaluate the objectives.

## Appendix E, historical

Source: Appendix B cell "SETTINGS AND RUN - ALGORITHMS EXECUTION TIME".

| Item | Value |
| --- | --- |
| Same algorithms, benchmarks, dimension, population, iterations, base seed | as Appendix C |
| Runs | 20 |
| Parallel | false in the listing (`USE_PARALLEL = False`) |
| Metrics | wall (`time.perf_counter`) and CPU (`time.process_time`) |
| Output named in the listing | `raw_timing_results.npz` |

Chapter 6 prose once says the timing settings are "the same as in Section 5.1 (20 runs...)". Section 5.1's search study is 100 runs. The timing cell is the authority for the 20-run count.

## Quick validation

`scripts/handbook_experiment.py --profile quick`. PSO, DE/rand, GWO, Spherical, Rastrigin, dimension 5, population 8, 64 evaluations, 2 runs, seeds 12345 and 12346, `Generator`. This is a CI smoke test. It is not Appendix C and not Appendix E.

## What a replacement study would be

A scientifically defensible replacement of the printed tables would:

1. Use `numpy.random.Generator`.
2. State that it does not replay `raw_benchmark_results.npz`.
3. Record `nfev`, seeds, package versions, platform, and wall time.
4. Either keep the manuscript's iteration stopping rule and say the budgets differ for GWOEPD and ME-D-PSO, or give every algorithm the same `max_evaluations` and say the comparison is no longer the printed protocol.
5. Compare medians with the printed cells only after those cells are transcribed, under a tolerance written down before the run.

That study was not run. The cost estimate is `results/full_experiment_cost_estimate.json`.
