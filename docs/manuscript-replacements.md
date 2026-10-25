# Manuscript replacements for author and editor approval

Phase: Validation. Date: 2026-10-19.

Rendered pages are estimates from page-break markers in `Metaheuristic_Optimization_with_Python_Editorial_Edition.docx`. They are not a KDP page proof. None of the conflicting items below was decided by this repository. Code keeps Appendix B unless a guard was required to run.

## Open decisions (do not apply until the authors say so)

### Whitley, Table 4.1 versus Appendix B

- **Where.** Table 4.1 and Appendix B, Whitley row. Columns are location, then value.
- **Before.** Location `0`, value `1`.
- **After.** Location `1` (every coordinate is 1, the same notation the table uses for Rosenbrock). Value `0`.
- **Reason.** Appendix B cites Jamil and Yang. `WhitleyFunction(np.ones(D))` is 0. At the origin every pair term has `y = 1`, so the value is `D^2 * (1/4000 - cos(1) + 1)`, equal to about 1.83979 for `D = 2`, not 1. The printed cells are that pair swapped. The formula was not changed to match the printed cells.
- **Result change.** The code is unchanged. `scripts/prepare_reviewed_manuscript.py` applies the cell edit to a local review copy that is not committed, because the manuscript is all rights reserved.
- **Decision.** Scientific correction applied to the review copy on 2026-10-20. KDP use of that copy still needs author acceptance and visual QA. Owner for publication acceptance: handbook authors.

### Problem 1a objective

- **Where.** Section 6.3 reduction of Problem 1a, and Practical Exercise 1.
- **Before.** An earlier note treated the settling-time listing as a second Problem 1a objective in the solving section. That note is withdrawn. The exercise uses plant `1/(1+s)**3`.
- **After.** Problem 1a remains the ITAE objective. The library names are `objective_1a_itae`, `objective_1a_settling_time` (same plant, different criterion), and `objective_chapter6_exercise1_settling` (exercise plant).
- **Reason.** The printed values 19655252.199124742 and 18.796046141402556 match ITAE and do not match the settling-time value at the same gains. Section 6.3 names ITAE.
- **Result change.** No printed Chapter 6 optimizer table was relabeled. Appendix-style search results for Problem 1a were not recomputed.
- **Decision.** Identification made from the manuscript text and the worked scalars. No objective was deleted.

### Author order and license

- **Where.** Manuscript copyright line; repository `LICENSE`, `CITATION.cff`, and `README.md`.
- **Before (manuscript, as reviewed).** Copyright names Yuriy Romasevych and Viatcheslav Loveikin.
- **Current repository text.** Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk, with Komarchuk last. `LICENSE` records approval on 19 October 2026 to create the companion repository and states that no open-source license has been selected.
- **After, 2026-10-25.** Repository metadata keeps Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk, in that order. The review-copy title page and copyright line add Dmytro Komarchuk. The line does not state copyright shares. MIT is not applied. See `docs/licensing-audit.md`.
- **Result change.** Review-copy author lines only. Bibliography entries that cite earlier papers are left as printed.
- **Decision.** Co-author order for the revised Python edition is the order above. The MIT grant is still absent.

## Replacements that do not change a formula

### 1. Conditional expressions, Problem 1a and Problem 5

- **Where.** Problem 5, rendered page 203, and the Problem 1a solving-section line on the same rendered page.
- **Before.** A one-line conditional, for example `penalty_terminal = 0.0 if reached else W_TERMINAL * np.linalg.norm(S[-1])`.
- **After.** Keep the expression, and if it wraps, parenthesize it so `else` is not the first token of the next line.
- **Reason.** The editorial DOCX parses. A wrap without parentheses is a syntax error.
- **Result change.** None. `src/metaopt/applications/cart_pole.py` already parenthesizes the penalty.

### 2. Crane speed sentence

- **Where.** Problem 3, rendered page 195, coefficients `(-5, 6, 10, -2, 5, 20, -4)`.
- **Before.** Prose that the penalty terms are absent.
- **After.** State that the speed constraint is satisfied up to roundoff on the order of `1e-7` m/s. In this environment the excess is about `6.4e-8` m/s and the objective still prints `0.4209773021079328`.
- **Reason.** `dx1.max()` is `1.2000000000000635`.
- **Result change.** The polynomial is unchanged. Feasibility in code treats a penalty below `1e-6` as inactive so the flag matches the prose; the returned objective still includes the tiny penalty and still matches the printed scalar.

### 3. Random numbers

- **Where.** Optimizer listings and Appendix B `run_once_perf` (`BASE_SEED = 12345`).
- **Before.** `np.random.seed(seed)` and `np.random.rand`.
- **After.** `rng = np.random.default_rng(seed)` and `rng.random`.
- **Reason.** The legacy call mutates process-wide state.
- **Result change.** Printed search traces and `raw_benchmark_results.npz` are not replayed. Appendix C must be labeled as a historical legacy-stream result or replaced by a new Generator experiment. This repository did the second only for the reduced study in `results/reduced_comparison_summary.json`, which is explicitly not Appendix C.

### 4. Quartic and Xin-She Yang

- **Where.** Appendix B definitions that call `np.random.random`.
- **Before.** Noise is drawn from the same global stream as the optimizer.
- **After.** Say that those two functions consume extra uniforms, or give them a separate noise generator and state that search paths then differ.
- **Reason.** The companion uses `metaopt.benchmarks.seed_benchmark_noise`.
- **Result change.** Search paths on those two functions differ from the manuscript for this second reason. Table 4.1 should say the Xin-She Yang factor is uniform on `[0, 1)`, not a normal draw confined to `[0, 1]`.

### 5. `clear_output` and package installation

- **Where.** Chapter listings, Appendix B `OPTIMIZERS`, and the Problem 1a setup cell.
- **Before.** `from IPython.display import clear_output` inside the algorithm, and `subprocess` `pip install` when an import fails.
- **After.** Pass an optional callback. Declare `numpy>=2` in the environment. Keep `%pip` only in a notebook cell, not in a `.py` file.
- **Reason.** Display clearing and installation are not part of the search. The Appendix B experiment already disables `clear_output`.
- **Result change.** None in the update equations.

### 6. ME-D-PSO history index

- **Where.** `BreakPSO` in Section 1.4.5 and Appendix B.
- **Before.** `last, prev = CostFunctionValues[-1], CostFunctionValues[-2]` with no length check.
- **After.** Run that line only when at least two history values exist. Keep the relative-change test.
- **Reason.** A restarted epoch can have a single new sample.
- **Result change.** The early-stop rule is unchanged. Runs that previously raised `IndexError` now continue.

### 7. IA-PSO scale

- **Where.** Section 1.4.2, `DistList / DistList.max()`.
- **Before.** Division by the maximum distance with no guard.
- **After.** If the maximum distance is 0, use scale 1. Then `w = w0`.
- **Reason.** The maximum is 0 when every particle sits on the global best.
- **Result change.** None when any distance is positive.

### 8. SADE fragment indentation

- **Where.** Chapter 2 fragment beginning `if np.random.rand() < tau1`.
- **Before.** The assignment to `F` is not indented.
- **After.** Indent the assignment, matching the Appendix B `SADE` function.
- **Reason.** The fragment does not parse. Appendix B does.
- **Result change.** None. The repository follows Appendix B.

### 9. von Neumann population

- **Where.** Section 1.5.2.
- **Before.** The listing raises `ValueError` unless the population is a square, without a nearby reminder.
- **After.** State that the population must be a square. The Chapter 5 protocol uses 25, which is valid. Population 30, used in some other examples, is not.
- **Result change.** None.

### 10. Table 4.1 notes that do not require a code edit

| Item | Before | After | Result change |
| --- | --- | --- | --- |
| Rotated hyper-ellipsoid domain | lower end printed as `-65.53`, upper `65.536` | lower end `-65.536`, unless the asymmetry is intentional | none if the table changes; code already uses `[-65.536, 65.536]` |
| Griewank, Table 4.2 separability | `+` | not separable | none |
| Schwefel 2.26 | value near `-418.983` with no factor `D` | add that this handbook uses the mean, because Appendix B divides by `D` | none; code and table already agree |
| Powell, Table 4.2 differentiability | marked absent | either change the flag or show the image formula if it is not `sum abs(x_i) ** (i + 1)` with `i` starting at 1 | none until the image is transcribed |
| Perm 0, d, β location | `i-1` | `1/i` if that is what the image says | none; code is zero at `1/i` |
| Elliptic | no `D = 1` note | state that `D >= 2` | code raises `ValueError` at `D < 2` |
| Trid | location and value blank | `x_i = i (D + 1 - i)`, value `-D (D + 4) (D - 1) / 6` | none; `D = 6` matches that value in tests |
| Paviani | domain includes values at which `log(x-2)` or `log(10-x)` is undefined | state the open interval `(2, 10)` | code warns and returns a non-finite value; the expression is unchanged |

### 11. Stable links, after a tag exists

- **Where.** Chapter-title links that point at `https://github.com/dmitruyk/Metaheuristic-Optimization-with-Python/blob/main/...`.
- **Before.** `/blob/main/` paths.
- **After.** `/blob/<tag>/` once a tag is published.
- **Reason.** `main` moves.
- **Result change.** None until the authors approve a release tag. This branch does not create that tag.

## Checked and not proposed as corrections

Section 1.3 value 12.3901. Mountain-car and cart-pole worked values. Robot trajectories `35571448004.83873` and `14.74322171254588`. Crane coefficients `(-6, 9, 20, 5, 5, 60, 0)` return `707599.2688799157`. Problem 1b at `(0.1, 2, 6)` returns `-0.036514370221270194`.
