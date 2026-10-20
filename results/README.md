# Results

`quick_validation_summary.json` is the Generator smoke profile. `full_experiment_cost_estimate.json` is a cost estimate and records `executed: false`. `published_comparison.json` matches worked scalars and leaves Appendix C and Appendix E unmatched. None of these files is a reproduction of Appendix C or Appendix E.

This directory is for local experiment output.

Do not treat a file here as a reproduction of Appendix C or Appendix E unless
`docs/validation-report.md` says that the file was compared with the printed
table at a stated tolerance. The full Chapter 5 protocol (14 algorithms, 54
benchmarks, 100 runs, population 25, 500 iterations, D=30) is about
9.5×10^8 objective evaluations for the performance study alone, before
GWOEPD's extra evaluations. It was not run for this repository.

The manuscript stores that study in `raw_benchmark_results.npz` and the timing
study in `raw_timing_results.npz`, then exports `Appendix_E_execution_time.xlsx`.
Those files are not in this repository. Seeds in the manuscript listing are
`BASE_SEED = 12345` passed to `np.random.seed`, which is the legacy NumPy
stream. This library uses `numpy.random.Generator`, so the same integer does
not replay that file even if the study is rerun.

`reduced_comparison_summary.json` is the latest run of
`scripts/reduced_statistical_comparison.py`. The same script also writes
`reduced_comparison_py<version>.json` so a later Python does not erase the
other interpreter's summary. Those files are a five-run Generator study on
two functions and three algorithms. They are not Appendix C or Appendix E.
`reference_minima.csv` is a direct evaluation at stated locations, not a search.

`ci/` is written by `.github/workflows/ci.yml`. On a push to a branch other
than `main`, the `publish-results` job copies the Linux pytest and notebook
logs into that directory and commits them on the same branch. `summary.json`
is that commit. `run-39376535919.json` records the earlier green run, which
did not save pytest stdout. None of these files is Appendix C or Appendix E.
