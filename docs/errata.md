# Errata proposed for the editorial manuscript

Review status, 2026-10-19: code-side guards from items 4, 5, 6, 9, 10, and 12 are in the library and covered by tests. Items 2 and 8 (Problem 1a, Whitley) and the license/author question are waiting on the authors. Proposed before/after text for the editor is in `docs/manuscript-replacements.md`. This file does not apply those decisions.

Rendered pages below are estimates from page-break markers in `Metaheuristic_Optimization_with_Python_Editorial_Edition.docx`. Word reports 346 pages; the counter used here ends at 347. The implementation brief cited pp. 224–226 for the PID listing, p. 231 for the crane, and pp. 289–298 for the benchmark appendix. In this file those passages are near rendered pages 187 (Problem 1a), 194–195 (crane polynomial), 203 (cart-pole penalty), and 272–279 (Appendix B). The suggestions are about the text, not about those brief page numbers.

Each item gives the original excerpt, a corrected excerpt, and why an editor should look at it. Code in this repository keeps the Appendix B formulas unless a line could not run.

## 1. PID conditional, and the cart-pole penalty line

**Where.** Problem 1a, rendered page 187, and Problem 5, rendered page 203.

**Original (Problem 5, one line in the DOCX, valid Python).**

```python
penalty_terminal = 0.0 if reached else W_TERMINAL * np.linalg.norm(S[-1])
```

**Corrected layout, if a typesetter wraps the line.**

```python
penalty_terminal = (
    0.0 if reached else W_TERMINAL * np.linalg.norm(S[-1])
)
```

**Why.** The expression in the editorial DOCX parses. A line wrap that places `else` at the start of the next line, without parentheses, is a syntax error. The same risk applies to the Problem 1a solving-section line `penalty_terminal = 0.0 if np.allclose(...) else 1e8 * ...` on rendered page 203. Problem 1a's earlier ITAE listing does not use a conditional expression; it uses an `if` block and it parses. No mathematical change is proposed.

## 2. Two different PID objectives

**Where.** Section 6.3, reduction of Problem 1a, and Practical Exercise 1 after the Chapter 6 review questions.

**Revised identification, 2026-10-20.** An earlier note in this file called the settling-time listing the solving section of Problem 1a. That identification is withdrawn. The exercise heading is "Practical Exercise No. 1", and its plant is `1/(1+s)**3`, not the Problem 1a plant `1/((s+1)(1+s/5+s^2))`. Section 6.3 says Problem 1a minimizes ITAE. The withdrawal is recorded because the paragraph sequence in the editorial DOCX shows the exercise after "Practical exercises for Chapter 6", not inside the Problem 1a reduction.

**Original, solving section.** The return value adds a 2% settling time and an overshoot that is not divided by the setpoint:

```python
overshoot = max(0.0, np.max(y) - r)
settling = next((t[i] for i in range(len(t)) if np.all(np.abs(y[i:] - r) <= 0.02 * r)), T)
return float(penalty_terminal + 1e6 * overshoot + settling)
```

**The reduction listing, which matches the printed numbers 19655252.199124742 and 18.796046141402556.**

```python
overshoot_penalty = 1e6 * max(0.0, (np.max(y) - r) / r)
itae = np.trapezoid(time * np.abs(r - y), time)
return float(terminal_penalty + overshoot_penalty + itae)
```

**Why.** The printed worked values match `objective_1a_itae`. `objective_1a_settling_time` keeps the settling expression on the Problem 1a plant and does not match those values. `objective_chapter6_exercise1_settling` is the exercise plant. None of the three replaces another.

## 3. Crane polynomial, line wrapping, and a floating-point penalty

**Where.** Problem 3, rendered page 195. The long `dx1` and `delta` expressions parse when the parentheses in the DOCX are kept.

**Observed.** For coefficients `(-5, 6, 10, -2, 5, 20, -4)` the function returns `0.4209773021079328`, matching the printed value. `dx1.max()` is `1.2000000000000635`, so `max(dx1.max() - 1.2, 0)` is about `6.4e-8` rather than a clean zero. The prose says the penalty terms are absent.

**Correction to the prose, not to the formula.** State that the speed constraint is satisfied up to roundoff on the order of `1e-7` m/s, or clip the violation with a tolerance before multiplying by `1e6`. Do not rewrite the polynomial.

## 4. Global `np.random` versus an explicit generator

**Where.** Every optimizer listing, and `run_once_perf` in Appendix B (rendered page 294, `BASE_SEED = 12345`).

**Original.**

```python
np.random.seed(seed)
Position = lb + np.random.rand(SwarmPopulation, n) * (ub - lb)
```

**Corrected.**

```python
rng = np.random.default_rng(seed)
position = lb + rng.random((population_size, n)) * (ub - lb)
```

**Why.** `np.random.seed` mutates process-wide legacy state. `default_rng` does not, and it does not reproduce the legacy stream. Printed search traces and `raw_benchmark_results.npz` cannot be replayed by this change. The repository makes the change and does not claim that Appendix C was reproduced. Quartic and Xin-She Yang also call `np.random.random` on that same global stream; they should take the same generator or a separate documented noise generator. This repository uses a separate noise generator (`seed_benchmark_noise`). That is a second, deliberate divergence on those two functions only.

## 5. `clear_output` inside the algorithm

**Where.** Chapter listings and the Appendix B `OPTIMIZERS` cell.

**Original.**

```python
from IPython.display import clear_output
clear_output(wait=True)
print(...)
```

**Corrected.** Pass an optional callback. The library does not import IPython and does not clear a display. The Appendix B experiment already rebinds `clear_output = lambda *args, **kwargs: None` before the long run, which shows that the call is not part of the search.

## 6. `np.trapezoid` and the setup cell that installs packages

**Where.** Problem 1a, rendered page 176–187. The setup cell runs `subprocess` `pip install` when an import is missing, and a comment says `np.trapz` for NumPy older than 2.

**Correction.** Declare `numpy>=2` in the environment (this repository does). Do not install packages from library code. The Jupyter-only line `%pip install tqdm joblib openpyxl ipywidgets` in Appendix B is not valid in a `.py` file. Those packages are optional extras here (`experiments`), not imports of PSO, DE, or GWO.

## 7. Ten-variable worked value

**Where.** Section 1.3, rendered page 21. Printed value `12.3901`.

**Check.** For `x = [0.1, 0.2, 0.3, -0.2, 0.51, -0.2, 0, -0.2, -1.6, 2.0]`, `sum(x**2) + sum(abs(x)) = 12.3901` exactly. No correction.

## 8. Table 4.1 and Appendix B disagreements

Formulas in Table 4.1 are images, so the comparison is between the table's location/value columns and Appendix B.

**Whitley.** Table 4.1 columns are location, then value. The Whitley cells were location `0`, value `1`. Appendix B cites Jamil and Yang. At the all-ones vector the function is 0. At the origin, `y_ij = 1`, so the value is `D^2 (1/4000 - cos(1) + 1)`, which is 1.83979... for `D = 2` and is not 1. The table cells are the swapped pair of the correct location `1` and value `0`. The code is unchanged. `scripts/prepare_reviewed_manuscript.py` writes that cell correction into a local review copy.

**Xin-She Yang.** The table text says the random factor is normally distributed on `[0, 1]`. A normal draw is not confined to `[0, 1]`. The code uses `np.random.random`, which is uniform on `[0, 1)`. Correct the table to say uniform on `[0, 1)`.

**Rotated hyper-ellipsoid.** The table domain is printed as `-65.53 ≤ xi` and `xi ≤ 65.536`. Appendix B uses `[-65.536, 65.536]`. Correct the lower endpoint to `-65.536` unless the asymmetry is intentional.

**Griewank, Table 4.2.** The separability column is `+`. The product of cosines in Appendix B is not separable. Correct the flag to not separable.

**Schwefel 2.26.** Appendix B divides the sum by `D`, and Table 4.1 gives a value near `-418.983` with no factor `D`. The code and the table agree with each other. Many other papers report about `-418.983 * D` because they do not divide. Add a sentence that this handbook uses the mean, not the sum. No code change.

**Powell, Table 4.2.** Differentiability is marked absent. Appendix B computes `sum |x_i| ** (i + 1)` with `i` starting at 1, so every exponent is at least 2 and the origin is differentiable. Either the image formula differs from the code, or the flag should be changed. The repository keeps the code and does not invent the classical four-variable Powell function.

**Perm 0, d, β.** The location column reads `i-1`. Appendix B is zero at `x_i = 1/i` (with the constant `10` that the code uses for β). Print the location as `1/i` if that is what the image formula says.

**Elliptic.** The code divides by `D - 1`. It is undefined at `D = 1`. State that restriction. The repository raises `ValueError` in that case.

**Trid.** Table 4.1 leaves the location and value unknown. Appendix B matches the usual formula, which is zero of the gradient at `x_i = i (D + 1 - i)` with value `-D (D + 4) (D - 1) / 6`. For `D = 6` the code returns that value. An editor can fill the table; the code was not changed.

## 9. ME-D-PSO can index an empty history

**Where.** `BreakPSO` in Section 1.4.5 and Appendix B.

**Original.**

```python
last, prev = CostFunctionValues[-1], CostFunctionValues[-2]
```

**Corrected.**

```python
if len(CostFunctionValues) >= 2:
    last, prev = CostFunctionValues[-1], CostFunctionValues[-2]
    if last != prev and abs((last - prev) / max(abs(last), 1e-300)) <= AcceptableRate:
        break
```

**Why.** On a restarted epoch the history may contain a single new sample when this line runs, and `[-2]` raises `IndexError`. The relative-change test itself is unchanged.

## 10. IA-PSO divides by the maximum distance

**Where.** Section 1.4.2.

**Original.** `DistList / DistList.max()`.

**Corrected.** If the maximum distance is 0, use scale `1`. Every distance is then 0, so `w = w0`, which is the same formula with a defined denominator. This happens when every particle sits on the global best.

## 11. Chapter fragment of SADE is not indented

**Where.** A one-column fragment in Chapter 2 (extracted listing beginning `if np.random.rand() < tau1`).

**Original.**

```python
if np.random.rand() < tau1:
F = FLower + np.random.rand() * (FUpper - FLower)
```

**Corrected.** Indent the assignment. The full `SADE` function in Appendix B is already indented and parses. The repository follows Appendix B.

## 12. von Neumann population

**Where.** Section 1.5.2. The listing raises `ValueError` unless the population is a perfect square. The Chapter 5 protocol uses population 25, which is valid. State that restriction next to the algorithm so a reader does not pass the population 30 used in some other examples.

## Items checked and not changed

- Mountain-car step, ANN value, and both worked objective values for Problems 4a and 4b match the printed numbers in this environment.
- Cart-pole one-step map, ANN value, and both worked objective values for Problem 5 match the printed numbers.
- Robot trajectories `35571448004.83873` (infeasible) and `14.74322171254588` (feasible) match.
- Crane coefficients `(-6, 9, 20, 5, 5, 60, 0)` return `707599.2688799157`.
- Problem 1b at `(0.1, 2, 6)` returns `-0.036514370221270194`.
- Appendix B's 54 function definitions parse. The one-column listings that do not parse are the explanation tables (prose in the code column), the unindented SADE fragment, and the `%pip` cell.
