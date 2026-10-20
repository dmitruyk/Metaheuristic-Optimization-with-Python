# Results

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
