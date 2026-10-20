# Coverage matrix

Phase: Validation. Date: 2026-10-19.

This matrix is the chapter-level view. Listing-level rows stay in `docs/book-code-map.md`. Status words match that file: `verified`, `corrected-with-erratum`, `unverified`, `not-applicable`.

A `verified` row was executed in this checkout and compared with a printed scalar, or the behavior is locked by a test that does not claim a printed search trace. Figures and Appendix C/E tables stay `unverified`. The reduced study in `results/reduced_comparison_summary.json` is new evidence. It is not a match to those tables.

| Chapter | Example or function | Source | Tests | Notebook | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Section 1.3 ten-variable objective at the printed point | notebook and `tests/test_examples_smoke.py` | `test_ten_variable_objective_on_the_printed_point` | `notebooks/01_particle_swarm.ipynb` | verified (12.3901) |
| 1 | Canonical PSO | `src/metaopt/pso.py` | `tests/test_pso.py`, `tests/test_reproducibility.py`, `tests/test_edge_cases.py` | 01 | corrected-with-erratum (Generator, no `clear_output`) |
| 1 | LDW-PSO, BB-PSO, VCT-PSO, Ring-PSO | `src/metaopt/variants/` | `test_every_handbook_algorithm_respects_the_box_and_the_budget` | 05 smoke | corrected-with-erratum |
| 1 | IA-PSO, including a zero distance scale | `src/metaopt/variants/ia_pso.py` | `test_ia_pso_defines_inertia_when_every_particle_is_the_best` | 05 smoke | corrected-with-erratum |
| 1 | ME-D-PSO early-stop history guard | `src/metaopt/variants/med_pso.py` | `test_med_pso_restarts_without_indexing_an_empty_history` | 05 smoke | corrected-with-erratum |
| 1 | von Neumann PSO square population | `src/metaopt/variants/von_neumann_pso.py` | `test_von_neumann_requires_a_square_population` | 05 uses population 9 | corrected-with-erratum |
| 1 | Figures 1.1–1.19 and Table 1.1–1.2 | none claimed | none | none | unverified |
| 2 | DE/rand/1/bin and DE/best/1/bin | `src/metaopt/de.py` | `tests/test_de.py`, `tests/test_reproducibility.py` | `notebooks/02_differential_evolution.ipynb` | corrected-with-erratum |
| 2 | SADE | `src/metaopt/variants/sade.py` | budget and bounds test | 05 smoke | corrected-with-erratum; chapter fragment indentation is a manuscript fix |
| 2 | SciPy differential evolution | `examples/scipy_differential_evolution.py` | `tests/test_examples_smoke.py` script smoke | none | not-applicable (not the handbook DE) |
| 2 | Figures 2.1–2.7 and Tables 2.1–2.2 | none claimed | none | none | unverified |
| 3 | GWO and mGWO | `src/metaopt/gwo.py`, `src/metaopt/variants/mgwo.py` | `tests/test_gwo.py` | `notebooks/03_grey_wolf_optimizer.ipynb` | corrected-with-erratum; `nfev = population * iterations` verified in tests |
| 3 | GWOEPD extra evaluations | `src/metaopt/variants/gwoepd.py` | `test_gwoepd_counts_the_replaced_wolves` | 05 smoke | verified accounting (`10 + 3 * 15 = 55` in that test); figures unverified |
| 3 | Figures 3.1–3.8 and Table 3.1 | none claimed | none | none | unverified |
| 4 | 54 Appendix B formulas | `src/metaopt/benchmarks.py` | `tests/test_benchmarks.py` | `notebooks/04_benchmarks.ipynb` | verified where a simple reference location is tested; see `results/reference_minima.csv` |
| 4 | Whitley | `WhitleyFunction` | `test_whitley_table_disagrees_with_the_listing` | 04 prose | unverified as a table match; code follows Appendix B; editor decision open |
| 4 | Paviani outside `(2, 10)` | `PavianiFunction` | `test_paviani_warns_and_is_nonfinite_outside_the_open_interval` | 04 exercise | corrected-with-erratum (warning only; formula unchanged) |
| 4 | Elliptic at `D = 1` | `EllipticFunction` | `test_elliptic_and_registered_domains_reject_bad_inputs` | 04 exercise | corrected-with-erratum (`ValueError`) |
| 4 | Domain mask | `outside_domain`, `evaluate_benchmark` | `test_elliptic_and_registered_domains_reject_bad_inputs` | 04 | verified as a guard, not as Table 4.1 |
| 4 | Quartic and Xin-She Yang noise | `seed_benchmark_noise` | `test_stochastic_benchmarks_repeat_when_reseeded`, `test_quartic_noise_is_uniform_and_repeats_only_after_reseeding` | none | corrected-with-erratum (separate noise generator) |
| 4 | Tables 4.1 and 4.2 as printed images | `docs/errata.md` item 8 | partial reference checks | 04 | unverified as a full table; disagreements listed for the editor |
| 5 | Equal-budget smoke | `src/metaopt/experiments.py` | edge-case budget tests | `notebooks/05_fair_comparisons.ipynb` | verified as a smoke budget only |
| 5 | Tables 5.1 and 5.2, Figure 5.2 | not recomputed | none | none | unverified |
| 6 | Problem 1a ITAE | `src/metaopt/applications/pid.py` `objective_1a` | `test_pid_worked_values` | `notebooks/06_pid_tuning.ipynb` | verified against the reduction-section numbers |
| 6 | Problem 1a settling listing | `objective_1a_settling` | exercised by the notebook; not selected as the published objective | 06 | unverified as the Section 6.3 objective; both functions are kept |
| 6 | Problem 1b | `objective_1b` | `test_pid_worked_values` | 06 | verified |
| 6 | Robot paths | `src/metaopt/applications/mobile_robot.py` | `test_robot_and_crane_worked_values` | `notebooks/07_robot_path_planning.ipynb` | verified |
| 6 | Crane polynomial | `src/metaopt/applications/crane.py` | `test_robot_and_crane_worked_values` | `notebooks/08_crane_control.ipynb` | verified scalars; feasibility uses a `1e-6` penalty cutoff documented in the source |
| 6 | Mountain car and cart-pole | `mountain_car.py`, `cart_pole.py` | `test_mountain_car_and_cart_pole_worked_values` | `notebooks/09_cart_pole.ipynb` | verified worked scalars |
| 6 | Chapter 6 figures | none claimed | none | none | unverified |
| 7 | Pressure vessel, gripper, beam | `src/metaopt/applications/engineering_design.py`, `examples/` | example script smoke | `notebooks/10_engineering_design.ipynb` | unverified against a printed optimum; smoke run only |
| Appendix B | Optimizer listings and benchmark cell | `src/metaopt/` | tests above | 01–05 | corrected-with-erratum |
| Appendix C | Rank tables and box plots | not stored | not matched | none | unverified |
| Appendix E | Timing workbook | not stored | not matched | none | unverified |
| Appendix A | Surface figures | `scripts/reproduce_figures.py` writes `figures/generated/*unverified*` | not compared with the book | none | unverified |

## Public minimizers

Every name in `metaopt.experiments.HANDBOOK_ALGORITHMS` has the signature `minimize(objective, bounds, *, rng=None, seed=None, population_size=25, iterations=None, max_evaluations=None)`. The bounds-and-budget test calls each of them.

## What this matrix does not certify

- Page-by-page visual equality with the 346-page DOCX.
- Bit-for-bit replay of `raw_benchmark_results.npz`.
- A choice between the two Problem 1a listings.
- A choice between Table 4.1 Whitley and Appendix B Whitley.
- An open-source license or a change in author order.
