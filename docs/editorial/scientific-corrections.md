# Scientific corrections log

> Editorial tooling note: the scripts named in this report (`scripts/editorial/…`, `tests/test_editorial_tools.py`) and the edit records are the editor's working tools. They are kept on the fork branch `dtkachenko:editorial/manuscript-edit-2026-10-27` and are not part of this pull request; the manuscript binaries are never committed.

Phase: Technical correction. Date: 2026-10-27. Branch `editorial/manuscript-edit-2026-10-27`.
Source manuscript: `manuscript/Metaheuristic_Optimization_with_Python_source_2026-10-25.docx` (paragraph indices ¶idx from `manuscript_extract/paragraphs.jsonl`).
Inputs consolidated: the seven reviews in `manuscript_extract/review/01-chapter-1.md` … `07-chapter-7.md`, `docs/errata.md`, `docs/manuscript-replacements.md`, `docs/editorial/initial-audit.md`. Finding IDs are the reviewers' (C1-01 …). Items that recur in every chapter (legacy `np.random` stream, `clear_output`, single-run conclusions) are merged into the cross-chapter entries XC-01 … XC-03, which list every paragraph they cover.

## How to read the statuses

- **APPLIED** — a text-only change whose wording is fixed by the book's own printed listing, table or code, or by arithmetic the reviewer reproduced. Each APPLIED item has a record in `manuscript_extract/edits/corrections.jsonl` (`ref` = the ID below) that the tracked-change tool applies as a Word redline; the authors can still reject it. Code paragraphs are never edited in this pass; where an APPLIED item has a code-side remainder it is named in the entry and counted under "Open author decisions" or "Repository follow-ups".
- **PENDING** — needs an author decision or a rerun: anything that changes an algorithm, a formula image, a result table, a figure, or the meaning of a claim beyond adding a qualifier. "Partially applied" in the status line means that the certain, text-only part of the finding is in `corrections.jsonl` and the rest waits.
- **REPO** — repository-side only (docs, examples, results files); nothing in the manuscript changes.
- **NOTED** — editorial observation with no text change in this pass (reference formatting and typesetting go to the copyedit; colour-only figures etc.).

## Counts

| Status | Count |
| --- | ---: |
| APPLIED | 86 |
| PENDING | 77 |
| NOTED | 16 |
| REPO | 1 |
| **Total entries** | **180** |

| Section | Entries | APPLIED | PENDING | NOTED | REPO |
| --- | ---: | ---: | ---: | ---: | ---: |
| Front matter (FM) | 3 | 3 | 0 | 0 | 0 |
| Cross-chapter (XC, merges C1-06, C1-27, C1-28, C2-11, C2-19, C2-20, C3-03, C3-21, C3-22) | 3 | 3 | 0 | 0 | 0 |
| Chapter 1 | 28 | 11 | 14 | 3 | 0 |
| Chapter 2 | 25 | 11 | 9 | 5 | 0 |
| Chapter 3 | 21 | 11 | 8 | 2 | 0 |
| Chapter 4 (+ Appendices A, B) | 31 | 20 | 8 | 3 | 0 |
| Chapter 5 (+ Appendices C, E) | 22 | 12 | 8 | 1 | 1 |
| Chapter 6 (+ Appendix D) | 27 | 9 | 16 | 2 | 0 |
| Chapter 7 | 20 | 6 | 14 | 0 | 0 |

`corrections.jsonl`: 135 records (134 replacements, 1 `insert_after`; 6 records carry `allow_object: true` and change only words away from the embedded object). Every `old` was copied from `paragraphs.jsonl` and re-checked by script; the file parses. Note for the tool run: 86 of these paragraphs are also touched by the copyedit files `01-chapter-1.jsonl` … `07-chapter-7.jsonl`; the tool refuses a second edit on a paragraph that already carries tracked changes, so the scientific records must be applied first (or merged) and the copyedit `old` texts rebased. `smoke.jsonl` duplicates ¶19, ¶58 and ¶2703 and must not be applied together with this file.

---

## Front matter

### FM-01 Subtitle
- **Location:** ¶19 (title page)
- **Original:** "Algorithms, Python Implementations, and Engineering Applications"
- **Issue:** Not the approved subtitle.
- **Evidence:** Repository `README.md`, `CITATION.cff` (approved subtitle).
- **Correction:** "Algorithms, Engineering Applications, and Practical Examples"
- **Status:** APPLIED
- **Why this status:** Approved wording; text only.

### FM-02 Python version in the setup text
- **Location:** ¶58 (Reader Prerequisites)
- **Original:** "Install Python 3.11 or newer and clone the companion repository. "
- **Issue:** The repository was standardised on Python 3.12 on 2026-10-27 (`pyproject.toml` `requires-python`, CI).
- **Evidence:** `pyproject.toml`; CI workflow; `docs/editorial/style-guide.md` ("Python 3.12 everywhere a version is given").
- **Correction:** "Install Python 3.12 and clone the companion repository. "
- **Status:** APPLIED
- **Why this status:** Single supported version; text only.

### FM-03 Author names
- **Location:** ¶0, ¶1, ¶2 (title page); ¶50 (copyright line) left as is
- **Original:** "Y. Romasevych", "V. Loveikin", "D. Komarchuk"
- **Issue:** The approved author line uses full names.
- **Evidence:** `docs/manuscript-replacements.md` (author order and license); `docs/editorial/initial-audit.md`.
- **Correction:** "Yuriy Romasevych", "Viatcheslav Loveikin", "Dmytro Komarchuk". The copyright line ¶50 is not changed because copyright shares are undecided.
- **Status:** APPLIED
- **Why this status:** Approved author line; the authors may reject.

---

## Cross-chapter entries

### XC-01 Legacy global `np.random` stream and no seed anywhere in Chapters 1–3 (merges C1-27, C2-19, C3-21; errata item 4)
- **Location:** Chapter 1 listings ¶314, ¶332–¶333, ¶395, ¶405–¶406, ¶524, ¶536, ¶541, ¶598, ¶609, ¶652, ¶662–¶666, ¶727, ¶747–¶751, ¶832, ¶846, ¶912, ¶930 and prose ¶460; Chapter 2 listings ¶1321, ¶1333, ¶1339, ¶1355–¶1360, ¶1414, ¶1419, ¶1428, ¶1446, ¶1461, ¶1469, ¶1478, ¶1486, ¶1494, ¶1500, ¶1535, ¶1602, ¶1641–¶1658, ¶1678–¶1694 and prose ¶1376; Chapter 3 listings ¶1908, ¶1924–¶1932, ¶2013, ¶2030–¶2057, ¶2126, ¶2164–¶2178, ¶2210, ¶2223–¶2231, ¶2301, ¶2317–¶2325 and prose ¶1964
- **Original:** `np.random.rand(...)`, `np.random.uniform(...)`, `np.random.choice(...)` throughout; ¶460 "Note that rerunning the PSO algorithm will give different results; therefore, the numerical values given above are not universal …"
- **Issue:** The three chapters contain no `np.random.seed` or `default_rng` call, so none of the printed values (¶444, ¶492, ¶572, ¶630, ¶698, ¶799, ¶881, ¶966) or Figures 1.6–1.19, 2.3, 2.5–2.7, 3.3, 3.5, 3.7, 3.8 can be reproduced even in principle. The prose acknowledges variability but names no remedy.
- **Evidence:** grep of the three section extracts (no match for `np.random.seed`/`default_rng`); `docs/errata.md` item 4; `docs/reproducibility.md`; repository `src/metaopt/_search.py` (`resolve_rng`).
- **Correction:** Text notes only. ¶460: append "The listings draw from NumPy's legacy global random stream without a seed, so the quoted values are from unseeded single runs. For a reproducible run, create a generator once, rng = np.random.default_rng(seed), pass it to the function, and replace np.random.rand with rng.random." ¶1376: "Running the DE algorithm again will produce somewhat different results, because the listing draws from NumPy's legacy global random stream without a seed (a fixed seed makes a run repeatable, see Section 5.1); the plot in Figure 2.5 is therefore presented purely to illustrate the results of applying the DE function." (this also closes C2-04). ¶1964: append "A fixed seed of the random-number generator makes a run repeatable (see Section 5.1); the listings of this chapter do not set one." The code replacement (`rng = np.random.default_rng(seed)`, `docs/manuscript-replacements.md` item 3) is not made in this pass.
- **Status:** APPLIED
- **Why this status:** Honest qualifier backed by the chapter text; the listing rewrite is an author decision recorded under "Open author decisions" (AD-01).

### XC-02 `clear_output` inside every listing (merges C1-28, C2-20, C3-22; errata item 5)
- **Location:** Chapter 1 ¶302, ¶304, ¶356 (Table 1.2); ¶387, ¶426; ¶516, ¶564; ¶590, ¶625; ¶644, ¶690; ¶717, ¶771; ¶824, ¶875; ¶900, ¶957. Chapter 2 ¶1345 (Table 2.1), ¶1353, ¶1362, ¶1632, ¶1667, ¶1703. Chapter 3 ¶1891–¶1892 (Table 3.1), ¶1902, ¶1947–¶1948, ¶2005, ¶2068–¶2069, ¶2203, ¶2249–¶2250, ¶2293, ¶2341–¶2342. Note placed in prose ¶363.
- **Original:** `from IPython.display import clear_output` … `clear_output(wait=True)`
- **Issue:** The listings fail at import in a plain Python interpreter without IPython. ¶304 explains the call as a notebook feature but no listing says what to do outside a notebook. ¶2069 writes the progress line differently from ¶1948/¶2342 (cosmetic).
- **Evidence:** `docs/errata.md` item 5; every review's check script had to stub `IPython.display`.
- **Correction:** Append to ¶363: "The listings in this book refresh their progress line with IPython.display.clear_output, which is available only in a Jupyter or Colab notebook; when running the code in a plain Python interpreter, delete the two lines that import and call it." (¶304, the natural place, is flagged code-like by the extractor and is not edited.) The callback replacement in `docs/manuscript-replacements.md` item 5 is a code change and is not made.
- **Status:** APPLIED
- **Why this status:** One-sentence instruction, no code change; code-side alternative goes to AD-01.

### XC-03 Comparative conclusions drawn from single unseeded runs (merges C1-06, C2-11, C3-03)
- **Location:** ¶492, ¶572, ¶630, ¶698, ¶799, ¶881, ¶966 (Chapter 1, against ¶967); ¶1511, ¶1537 (Chapter 2); ¶1987, ¶2072 (Chapter 3, against ¶1964 and the hedge in ¶2081)
- **Original:** e.g. ¶492 "Consequently, this modification is less well suited to the particular features of the objective function (1.13) than the classical PSO algorithm."; ¶698 "Figure 1.14 shows that the parameter RC has a direct effect on the result obtained."; ¶966 "this modification, in many cases, shows a better result than the Ring-PSO algorithm … one of the most refined"; ¶1511 "the most effective algorithms … are DE/best/1, DE/current-to-best/1, and DE/rand-to-best/1"; ¶1987 "Thus, this modification strategy is justified."; ¶2072 "did not produce better results than those obtained using the GWO and mGWO algorithms."
- **Issue:** Every variant is judged on one unseeded run of one function and the judgement is phrased as a property of the algorithm; ¶967 itself says this is not a valid basis. No printed number is contradicted by the reviewers' multi-seed runs (Chapter 1: 20 seeds, medians PSO 2.6e-06, LDW 6.7e-04, BB 2.2e-07, VCT RC=4/5/6 5.1e-03/1.1e-03/2.5e-04, ME-D 1.3e-03, Ring 3.0e-03, vN 6.8e-05; Chapter 3: 30 seeds, mGWO < GWO in 30/30, EPD-GWO worse than both in 30/30), but the book shows none of this.
- **Evidence:** Chapter 1 review `checks.py` section C; Chapter 3 review `ch3_check.py`; Chapter 2 review (reasoning; `docs/reproducibility.md`).
- **Correction:** Append to each paragraph "This conclusion is drawn from a single unseeded run; a comparison over repeated runs is given in Chapter 5." (Chapter 2 wording: "These are single unseeded runs on one function; a statistically grounded comparison with repeated runs is given in Chapter 5."). The unsupported "in many cases" and "one of the most refined" in ¶966 are left for the authors (AD-02), as is the option of printing a small multi-seed table instead.
- **Status:** APPLIED
- **Why this status:** The qualifier is exactly the sentence the brief allows; replacing the claims by medians is an author decision.

---

## Chapter 1 — PSO and its variants

### C1-01 IA-PSO's record result is an artifact of the optimum lying at the origin
- **Location:** ¶544 (listing, 1.4.2), ¶509, ¶513 (prose), ¶572 (claim), Figure 1.11
- **Original:** `Position = Position * (1 - rho) + Velocity`; ¶509 "a particle's new position is updated with a certain possible deviation from the point indicated by the velocity vector v"; ¶572 "The objective-function value found after two hundred iterations (5.986802266001554e-16) is orders of magnitude smaller …"
- **Issue:** The perturbation scales the position, so it is proportional to the distance from the origin and vanishes at the minimum of (1.13); on the same function shifted to x = 10 IA-PSO fails (median 8.99 vs PSO 9.7e-07), a shift of 0.5 costs five orders of magnitude. ¶509 does not describe what the code does.
- **Evidence:** `checks.py` section E: unshifted IA-PSO median 9.5e-16, PSO 2.6e-06; shift 10: PSO 9.7e-07, IA-PSO 8.99 (min 4.9, max 11.6); shift 0.5: IA-PSO 3.2e-01. `src/metaopt/variants/ia_pso.py` lines 45–50 identical.
- **Correction:** Applied: ¶509 → "a particle's new position is computed with a random deviation: the position itself is multiplied by the factor (1−ρ), so the deviation is proportional to the particle's distance from the coordinate origin, not to the velocity step:"; ¶572 append "Note that this value is specific to objective (1.13), whose minimum lies at the coordinate origin, where the random deviation of (1.16) vanishes; the mechanism does not transfer to functions whose minimum is not at the origin." plus the XC-03 sentence. Pending: whether to make the perturbation translation-invariant (`Position + Velocity * (1 - rho)` or box-width scaling) and re-run Figure 1.11 — this changes the algorithm as cited from [9].
- **Status:** PENDING (partially applied)
- **Why this status:** Algorithm change and figure rerun need the authors (AD-03); the descriptive fix and the limitation are certain from the listing and the shift test.

### C1-02 Clerc–Kennedy inertia value is misprinted
- **Location:** ¶259 (1.2)
- **Original:** "The authors of [2] recommend setting w=0.7968, c₁=c₂=1.4962."
- **Issue:** χ = 2/|2 − φ − √(φ² − 4φ)| = 0.7298 for φ = 4.1; the printed c = 1.4962 = 0.7298·2.05 is consistent only with 0.7298. "0.7968" is a digit transposition.
- **Evidence:** `checks.py` section A: `chi(phi=4.1) = 0.7298437881283576`, `chi*2.05 = 1.496179765663133`.
- **Correction:** "w=0.7298, c₁=c₂=1.4962".
- **Status:** APPLIED
- **Why this status:** One unambiguous value reproduced by arithmetic.

### C1-03 von Neumann listing includes the particle itself in its neighbourhood; Appendix B and the repository exclude it
- **Location:** ¶927 (listing, 1.5.2), ¶893 (prose); Appendix B ¶7688; `src/metaopt/variants/von_neumann_pso.py`
- **Original:** ¶927 `neighbor_idx = np.stack([self_idx, up_idx, down_idx, left_idx, right_idx], axis=1)`; Appendix B ¶7688 without `self_idx`.
- **Issue:** Two different algorithms are printed under one name; the Chapter 5 benchmark ran the Appendix B version, not the one explained in Chapter 1. Which one (1.23) states cannot be read (image).
- **Evidence:** `checks.py` section C: chapter listing median 6.8e-05, appendix listing 2.9e-04 (20 seeds); printed 0.000111 (¶966) is compatible with either.
- **Correction:** Authors to decide one definition; then change ¶927 (and ¶922) or Appendix B ¶7688 and the repository, and state in ¶893 whether the particle's own personal best is a candidate for gl.
- **Status:** PENDING
- **Why this status:** Changes an algorithm and possibly the Chapter 5 results (AD-04).

### C1-04 Wrong equation cross-reference for the reinitialization condition
- **Location:** ¶709 (1.4.5)
- **Original:** "In Figure 1.15, the iterations at which conditions (1.19) are satisfied are marked with red dots"
- **Issue:** (1.19) is the VCT-PSO rule; the ME-D-PSO conditions are (1.20), labelled so in ¶707.
- **Evidence:** ¶707, ¶638.
- **Correction:** "conditions (1.20)".
- **Status:** APPLIED
- **Why this status:** Certain target (same paragraph labels the conjunction (1.20)).

### C1-05 VCT-PSO prose says the personal best is "replaced"; the listing swaps the cognitive attractor for one iteration
- **Location:** ¶636, ¶640 (prose) vs ¶665–¶670 (listing)
- **Original:** ¶636 "the personal best of the k-th particle is forcibly replaced by the personal best of another (not the k-th) particle"; ¶640 "the first line of expression (1.19) is executed, and the particle's personal best is replaced."
- **Issue:** `PBest` is never overwritten; another particle's personal best is used as the cognitive attractor only in that iteration's velocity update. The repository implements the temporary version.
- **Evidence:** listing ¶665–¶670; `src/metaopt/variants/vct_pso.py` lines 44–50.
- **Correction:** ¶636 "… the cognitive term of the k-th particle is computed from the personal best of another (not the k-th) particle, while the stored personal best itself is not modified"; ¶640 "… and the personal best of another particle is used as the cognitive attractor for that iteration." (¶640 carries the fraction image; only the final clause is changed.) If the authors intend a permanent replacement, listing and repository must change instead (AD-05).
- **Status:** APPLIED
- **Why this status:** Describes the printed listing correctly; the alternative is logged as an author decision.

### C1-07 ME-D-PSO prose describes scalar coefficients; the listing draws a K×n matrix for each
- **Location:** ¶710 (prose) vs ¶749–¶751 (listing)
- **Original:** "a constant (at every iteration) and stochastic … change of the coefficients w, c1, and c2 within certain bounds"; listing `w = np.random.rand(SwarmPopulation, n)`, `c1 = np.random.uniform(0, 2, (SwarmPopulation, n))`, …
- **Issue:** The code samples an independent coefficient for every particle and coordinate; the prose and the scalar symbols of 1.1–1.2 say three scalars.
- **Evidence:** listing; `src/metaopt/variants/med_pso.py` lines 64–66.
- **Correction:** Append to ¶710: "In the implementation below, w, c1, and c2 are drawn independently for every particle and every coordinate at each iteration (matrices of size K×D), not as three scalars."
- **Status:** APPLIED
- **Why this status:** Describes the listing; no claim changes.

### C1-08 ME-D-PSO call description misnames the second empty argument
- **Location:** ¶798 (1.4.5)
- **Original:** "The empty arrays [], [] … correspond to the initial array of objective-function values and the initial array of initialized particles."
- **Issue:** `InitialVarValues` is a single position vector (the retained global best inserted into one particle, ¶737), not an array of particles; the sentence also contradicts ¶709.
- **Evidence:** listing ¶735–¶740.
- **Correction:** "… and the position of the retained global best (empty on the first epoch)."
- **Status:** APPLIED
- **Why this status:** Certain from the listing.

### C1-09 ME-D-PSO stagnation test: exact-zero improvement never triggers reinitialization; chapter line divides by the current best
- **Location:** ¶774 (listing), ¶709 (prose); Appendix B ¶7604–¶7605
- **Original:** `if CostFunctionValues[-1] != CostFunctionValues[-2] and abs((CostFunctionValues[-1] - CostFunctionValues[-2]) / CostFunctionValues[-1]) <= AcceptableRate:`; Appendix B uses `max(abs(last), 1e-300)` in the denominator.
- **Issue:** (a) A plateau (no improvement) never restarts the swarm, contrary to what ¶709 leads the reader to expect; (b) the chapter line raises `ZeroDivisionError` when the best value is exactly 0; the chapter and the appendix print different code.
- **Evidence:** `checks.py` section F2: restart fires 2–9 times per run, always on small nonzero steps; reasoning for (b).
- **Correction:** Applied: ¶709 append "Note that an iteration with no change in the global best does not satisfy conditions (1.20) as implemented in the listing below; reinitialization is triggered by a small but nonzero improvement." Pending: replace ¶774 by the Appendix B form (with the guard) so the two listings agree.
- **Status:** PENDING (partially applied)
- **Why this status:** The code replacement is a listing edit (no code changes in this pass); the sentence describes the listing as printed.

### C1-10 Boundary rule: prose describes clipping only; every listing also zeroes the velocity component
- **Location:** ¶243 and (1.10) (1.1); listings ¶339–¶342; Exercise 3 ¶1076, ¶1111; flowchart text ¶297
- **Original:** "If any of the updated variables goes beyond the upper or lower bound, it is forcibly returned to the corresponding bound:"; listing `Velocity[out] = 0; Position = np.clip(...)`.
- **Issue:** The velocity reset is part of the implemented algorithm (and of the repository `Bounds.zero_velocity_and_clip`) but absent from the theory; it changes the dynamics.
- **Evidence:** listings; `src/metaopt/pso.py` docstring lines 3–5.
- **Correction:** ¶243 "… it is forcibly returned to the corresponding bound (in the listings below, the corresponding component of the velocity vector is also set to zero):". Whether (1.10) should be a two-line rule is an image question for the authors.
- **Status:** APPLIED
- **Why this status:** Adds the missing rule as implemented; the equation image is untouched.

### C1-11 IA-PSO explanation confuses inertia with attraction
- **Location:** ¶504 (1.4.2)
- **Original:** "This means that the inertia factor predominates … Thus, the closer a particle is to the global best gi, the more strongly it is attracted to it."
- **Issue:** At the global best both difference vectors vanish, so the inertia share is 1 trivially; a larger w preserves velocity, it does not increase attraction. The last sentence states the opposite of what (1.15)–(1.16) do.
- **Evidence:** reasoning from ¶537 and ¶543 (reviewer confidence medium).
- **Correction:** Proposed: "At the global best both difference vectors vanish, so the velocity update consists of the inertia term alone (relative share 1); the particle keeps its previous velocity and overshoots the global best, which maintains diversity around it. Far from the global best wk → 0, inertia is lost, and the cognitive and social terms dominate."
- **Status:** PENDING
- **Why this status:** Rewrites the authors' interpretation of their own formula; medium confidence, no computation.

### C1-12 Exercise 5 objective can be negative; log-scale plot unusable; single runs cannot "establish the effect"
- **Location:** ¶1189, ¶1196, ¶1199–¶1200, ¶1213–¶1214 (Exercise 5)
- **Original:** `return (np.sum(np.sqrt(np.abs(x))) + sum(np.sin((j + 1) * x[j]) for j in range(Dimension)))`; "Compare the results obtained with one another and establish the effect of the factors K and I"; `Vars = list(range(Dimension))`.
- **Issue:** The function is negative in parts of the domain (PSO found −2.49 in one of 20 seeds; median +5.98; the single run of step 4 gave 26.75), so `plt.semilogy` from ¶453 cannot be reused, and the seed spread exceeds the K/I effect. `Vars` as a list of integers silently changes the convention.
- **Evidence:** `checks.py` section G.
- **Correction:** Add to the task: repeat each setting at least 10 times and compare medians; compare on a linear scale; use `Vars = [f"x{i+1}" for i in range(Dimension)]`.
- **Status:** PENDING
- **Why this status:** Changes the exercise's steps and a code line (AD-06).

### C1-13 "Global best" denotes a position in 1.1 and a value in 1.3
- **Location:** ¶197 (definition), ¶201, ¶297, ¶328, ¶355, ¶440, ¶442; glossary ¶13082
- **Original:** ¶197 "This position is called the global best g"; ¶440 "OptimizationResult = {value of the objective function at the last iteration, {numerical values of the variables}, {global best across the iterations}}"
- **Issue:** The same term is used for the position and for the scalar value; ¶440 uses set braces for a tuple and calls the first element "value at the last iteration" while ¶442 calls it the minimum value.
- **Evidence:** reasoning; the listings separate `GBest` and `GBestCost`.
- **Correction:** Applied: ¶440 → "OptimizationResult = (GBestCost, GBest, CostFunctionValues) ‒ the best objective-function value, the position at which it was found, and the list of the best objective-function values after each iteration". The consistent use of "global-best position g" / "global-best value f(g)" elsewhere is handed to the copyedit (style guide: personal best, global best).
- **Status:** APPLIED
- **Why this status:** ¶440 misdescribed the tuple the listing returns; the terminology sweep is wording, not science.

### C1-14 Subscript order for particle and iteration is inconsistent
- **Location:** ¶196 vs ¶502
- **Original:** "pk = xk.3 (the subscript '3' … indicates … the third iteration)" vs "the position of the k-th particle xi.k"
- **Issue:** particle.iteration in one place, iteration.particle in the other; the convention in the equation images (1.4), (1.15), (1.22), (1.23) is unknown.
- **Evidence:** reasoning.
- **Correction:** Pick one order (iteration first, as gi, vi−1, xi−1 in 1.1) and apply it in ¶196 and the equations.
- **Status:** NOTED
- **Why this status:** Depends on the equation images, which are not editable in this pass.

### C1-15 The objective value of the printed PSO solution is not shown
- **Location:** ¶443–¶444 (1.3)
- **Original:** "Referencing it as OptimizationResult[0] gives the objective-function value obtained in that run." followed directly by the ten variable values.
- **Issue:** A number is promised and none is printed; ¶572 later compares against an unstated PSO value.
- **Evidence:** `checks.py` section A: objective (1.13) at the printed vector = 7.662417638614574e-07 (recomputed from the printed digits; the original run's own printout is unknown).
- **Correction:** Append to ¶443: "For the solution printed below, this value is 7.662417638614574e-07 (recomputed from the printed digits of the solution)."
- **Status:** APPLIED
- **Why this status:** Arithmetic on the book's own printed vector, labelled as such.

### C1-16 VCT-PSO: no call example, and the chapter signature differs from Appendix B
- **Location:** ¶646 (listing), ¶695; Appendix B ¶7521, ¶7525
- **Original:** `def VCTPSO(function, Vars, DomainVarsList, SwarmPopulation, Iterations, RC):` vs Appendix B `def VCTPSO(function, Vars, DomainArgumentList, SwarmPopulation, Iterations):` with `RC = 5` hard-coded.
- **Issue:** The chapter call signature does not work with the appendix code and vice versa; no launch command is given; parameter names differ (`DomainVarsList`/`DomainArgumentList`).
- **Evidence:** grep of `12-appendix-b.md` lines 438–442; `vct_pso.py` `refresh_period=5`.
- **Correction:** Add after ¶693 `OptimizationResult = VCTPSO(ObjectiveFunction, Vars, DomainVarsList, SwarmPopulation, Iterations, 5)`; give `RC=5` a default in both listings; one parameter name.
- **Status:** PENDING
- **Why this status:** Code paragraphs (new and existing) — not edited in this pass.

### C1-17 LDW-PSO: w never takes the value wmax
- **Location:** ¶475, ¶485
- **Original:** "The initial (at i=1) and final (at i=I) values of the coefficient w are recommended to be set as follows: wmax=0.9, wmin=0.4."; `w=(wMax-wMin)*(Iterations-step)/Iterations+wMin`
- **Issue:** The first update is at step = 2 where w = 0.895 (I = 200); w = wmin is reached exactly at step = I.
- **Evidence:** `checks.py` section A: w(2, 200) = 0.895; w(200) = 0.4.
- **Correction:** ¶475 → "The initial and final values of the coefficient w are recommended to be set as wmax=0.9 and wmin=0.4; in the listing below w decreases linearly from approximately wmax at the first velocity update (i=2) to exactly wmin at the last (i=I)."
- **Status:** APPLIED
- **Why this status:** Describes the listing; the code is left as is (reviewer: not worth a change).

### C1-18 Figure 1.6 uses the Griewank function before it is defined and without dimension or domain
- **Location:** ¶282–¶289 (1.2), caption ¶285
- **Original:** "Curves showing the reduction of the Griewank function using the PSO algorithm with swarm size K=25"
- **Issue:** Griewank appears only in Table 4.1; D, box and seeds for the three curves are not given, so the statements about convergence at I = 50/100/200 cannot be checked, and ¶288 attributes run-to-run variance to the iteration count.
- **Evidence:** grep for "Griewank" in Chapter 1: only ¶285, ¶289.
- **Correction:** State D, the box and "three independent runs" in the caption; add "(Griewank function, see Table 4.1)".
- **Status:** PENDING
- **Why this status:** D and the box are unknown; only the authors can supply them (AD-07).

### C1-19 "w=0.72, c₁=c₂=1.19" has no source
- **Location:** ¶259
- **Original:** "However, quite often w=0.72, c₁=c₂=1.19 is used. It is this latter recommendation that we will follow."
- **Issue:** The standard pairing with w ≈ 0.72 is c ≈ 1.49; 1.19 is used throughout the book without a source.
- **Evidence:** reasoning (not checked online).
- **Correction:** Cite the source or say it is the authors' empirical choice.
- **Status:** PENDING
- **Why this status:** Author knowledge needed (AD-08).

### C1-20 `DomainVarsList = [[-20, 20]] * 10` uses a literal and aliases one list
- **Location:** ¶383
- **Original:** `DomainVarsList = [[-20, 20]] * 10`
- **Issue:** `Dimension` is defined two lines earlier; list multiplication yields ten references to one inner list.
- **Evidence:** reasoning; `tests/test_pso.py` and the notebook use the same literal.
- **Correction:** `DomainVarsList = [[-20, 20] for _ in range(Dimension)]`.
- **Status:** PENDING
- **Why this status:** Code line.

### C1-21 ME-D-PSO BreakPSO does not re-evaluate the best index after inserting the retained global best
- **Location:** ¶732–¶740
- **Original:** `g = np.argmin(PBestCost); GBestCost = float(PBestCost[g])` then `Position[g] = InitialVarValues … PBestCost[g] = Cost[g]` with no recomputation.
- **Issue:** `GBestCost` is stale until the first loop iteration; the repository recomputes (`med_pso.py` lines 49–51).
- **Evidence:** reasoning; repository diff (reviewer confidence medium).
- **Correction:** After ¶740 add `g = np.argmin(PBestCost)` and `GBestCost = float(PBestCost[g])`.
- **Status:** PENDING
- **Why this status:** Code change.

### C1-22 Exercise 1/4 "Particle" entries store views; "empty array" is a list
- **Location:** ¶1013, ¶1027, ¶1163
- **Original:** `Particle = [Position[k], Velocity[k], float(Cost[k]), PBest[k], float(PBestCost[k])]`; "Declare an empty array Swarm"
- **Issue:** `Position[k]` and `PBest[k]` are views; Exercise 3 (¶1091) correctly uses `.copy()`.
- **Evidence:** reasoning.
- **Correction:** `.copy()` as in Exercise 3; "empty list".
- **Status:** PENDING
- **Why this status:** Code change; the wording "empty list" alone is not worth a separate record.

### C1-23 1-based indices in prose versus 0-based indices in the listings
- **Location:** ¶893 vs ¶921–¶926; ¶817 vs ¶842–¶843
- **Original:** "for the first particle its neighbors have indices 2 (right), 5 (left), 6 (below), and 21 (above)"
- **Issue:** The listing's particle 0 has neighbours 1, 4, 5, 20.
- **Evidence:** `np.roll` on `np.arange(25).reshape(5, 5)`.
- **Correction:** Insert after "(above)": "(particles are numbered from 1 here; the Python arrays are numbered from 0, so these are indices 1, 4, 5, and 20 in the listing)". ¶817 (Ring) left to the copyedit.
- **Status:** APPLIED
- **Why this status:** Certain; adds a bridging remark.

### C1-24 Errata item 9 confirmed: ME-D-PSO indexes an empty history
- **Location:** ¶774 (listing); Appendix B ¶7604
- **Original:** `if CostFunctionValues[-1] != CostFunctionValues[-2] and ...`
- **Issue:** `MEDPSO(F, Vars, Dom, 25, 200, 0.01, [], [x0])` raises `IndexError`; the standard call runs.
- **Evidence:** `checks.py` section F; `docs/errata.md` item 9; guard in `med_pso.py` line 79.
- **Correction:** As in `docs/manuscript-replacements.md` item 6 (length guard).
- **Status:** PENDING
- **Why this status:** Listing edit; the repository already carries the guard.

### C1-25 Errata item 10 confirmed: IA-PSO divides by the maximum distance
- **Location:** ¶537; Appendix B ¶7464
- **Original:** `w = (w0 * (1 - DistList / DistList.max()))[:, None]`
- **Issue:** Division by zero when every particle sits on the global best.
- **Evidence:** `docs/errata.md` item 10; `ia_pso.py` lines 40–42.
- **Correction:** As in `docs/manuscript-replacements.md` item 7 (scale 1 when the maximum is 0).
- **Status:** PENDING
- **Why this status:** Listing edit; repository already guarded.

### C1-26 Errata item 12 confirmed: perfect-square population enforced in code but not stated in prose
- **Location:** ¶888, ¶897; listing ¶908–¶910
- **Original:** ¶888 "… forming a grid of particles, for example 5×5."; ¶910 `raise ValueError("SwarmPopulation must be a perfect square ...")`
- **Issue:** The prose never says K must be a perfect square.
- **Evidence:** `docs/errata.md` item 12.
- **Correction:** Append to ¶888: "The swarm size must be a perfect square (K = 9, 16, 25, 36, …); the listing below raises an error otherwise."
- **Status:** APPLIED
- **Why this status:** Adds a missing restriction stated by the listing.

### C1-29 Advantages list makes unsupported claims
- **Location:** ¶466 (1.4)
- **Original:** "their values are already well substantiated by decades of scientific research"; "it is balanced with respect to 'exploration–exploitation'"; "it identifies the attractors of the objective function's minima fairly well"
- **Issue:** ¶289 has just shown premature convergence and ¶467 says PSO does not always reach an acceptable solution; no citation.
- **Evidence:** reasoning.
- **Correction:** Attribute to the literature with citations or phrase as "is often reported to".
- **Status:** PENDING
- **Why this status:** Author's claims and citations (AD-08).

### C1-30 Code lines without code style in the DOCX
- **Location:** ¶426, ¶667, ¶770, ¶789, ¶910; Appendix B ¶7601, ¶7675
- **Original:** `clear_output(wait=True)` / `print(...)`, `idx += (idx >= np.arange(SwarmPopulation))`, `step += 1`, `AcceptableRate, listCoFuVal, listGlobPos`, `raise ValueError(...)`
- **Issue:** Extractor tags these as non-code while surrounding lines are code; likely a paragraph-style slip that will show in print.
- **Evidence:** tag pattern in the extract (low confidence).
- **Correction:** Check the paragraph style of these lines in the DOCX.
- **Status:** NOTED
- **Why this status:** Typesetting; goes to the copyedit/structure pass.

### C1-31 Reference list: inconsistent formatting
- **Location:** ¶1218–¶1230
- **Original:** "pp. 1942-1948." vs "P. 58–73"; "[13] Liu, Q., Wei, W., …" (different author style); "[7] … Springer. Berlin. Heidelberg. 2009."
- **Issue:** Mixed "pp."/"P.", hyphen/en dash, author styles, terminal punctuation.
- **Evidence:** reasoning; contents of [1], [2], [5], [8], [10] match the reviewer's recollection, the rest unverified.
- **Correction:** Normalise to one style.
- **Status:** NOTED
- **Why this status:** Reference formatting is copyedit work.

---

## Chapter 2 — Differential Evolution

### C2-01 Section 2.1 and the flowchart describe DE/rand/1, but the DE function in Table 2.1 is DE/best/1
- **Location:** ¶1255, ¶1305 (prose), ¶1332–¶1334 (Table 2.1), ¶1439 (2.4.1)
- **Original:** ¶1305 "three distinct vectors xr1, xr2, and xr3 are randomly chosen"; listing ¶1332 `i1 = BestDotNumber`; ¶1439 "The DE/best/1 algorithm has already been presented as the DE function's code (Table 2.1)."
- **Issue:** The algorithm explained is DE/rand/1; the code the reader is told implements it fixes the base vector to the best individual. Table 2.1's own explanation ¶1334 contradicts ¶1305.
- **Evidence:** ¶1332–¶1335; Appendix B `DEBest` ¶7729 vs `DERand` ¶7751; `src/metaopt/de.py`.
- **Correction:** Either (a) make Table 2.1 the DE/rand/1 listing (lines from ¶1418–¶1419) and rewrite ¶1334, deriving DE/best/1 in 2.4.1; or (b) keep the listing and state in ¶1304/¶1305 and the caption that the function implements DE/best/1/bin.
- **Status:** PENDING
- **Why this status:** Changes a listing or the exposition order (AD-09).

### C2-02 Exercise 2 redraws dRAND for every component, breaking the guarantee of (2.3)
- **Location:** ¶1602 (listing); ¶1279 (prose)
- **Original:** `for i in range(VarsLength):` / `    iRand = np.random.choice(DimensionIndexes)` / `    if np.random.rand() <= CR or iRand == i:`
- **Issue:** A new index per component means every component can come from x; per-component probability becomes CR + (1−CR)/D. Table 2.1 (¶1339) does it correctly. `docs/book-code-map.md` tags the cell "corrected-with-erratum" but no erratum text exists.
- **Evidence:** analytic `((1-CR)*(1-1/D))**D` = 3.405e-4 (D=10, CR=0.5); Monte Carlo of the listing, 200 000 trials, seed 0: 3.45e-4 identical trial vectors; 0 with a single dRAND.
- **Correction:** Move `iRand = np.random.choice(DimensionIndexes)` before the loop; add the erratum entry.
- **Status:** PENDING
- **Why this status:** Code change (brief lists it as pending); erratum entry is a repository follow-up.

### C2-03 "SADE" implements a simplified jDE, not the scheme of [5], and the name collides with Qin–Suganthan's SaDE
- **Location:** ¶1514–¶1537 (2.4.2), ¶1546, ¶1725
- **Original:** ¶1516 "Let us give an example of how this is proposed in [5] …"; ¶1535 sets a single shared `F`/`CR`.
- **Issue:** Brest et al. 2006 (jDE) keep per-individual (F_k, CR_k) retained only on survival; the chapter keeps one population-wide pair re-drawn with probability τ regardless of success. The repository docstring warns; the manuscript does not.
- **Evidence:** Brest et al. 2006 Sec. III; `src/metaopt/variants/sade.py` `_adapt`; Appendix B ¶7802–¶7805.
- **Correction:** Implement the [5] rule, or add after ¶1521 "Unlike [5], where each vector carries its own F and CR that are kept only when its trial vector survives, the implementation here uses a single population-wide pair that is re-drawn with probabilities τ1, τ2 before each target vector." and consider renaming.
- **Status:** PENDING
- **Why this status:** Algorithm/naming decision (AD-10); (2.5) is an image.

### C2-04 ¶1376 refers to "numerical values given above" that do not appear
- **Location:** ¶1376; ¶1364–¶1374
- **Original:** "Running the DE algorithm again will produce somewhat different results; the numerical values given above are therefore presented purely to illustrate the results of applying the DE function."
- **Issue:** No number is printed between ¶1364 and ¶1376.
- **Evidence:** reasoning; one legacy-seeded run (seed 12345) gives 1.79e-08, shown only for magnitude.
- **Correction:** "… the plot in Figure 2.5 is therefore presented purely to illustrate …" (merged with the XC-01 seed sentence in the same record).
- **Status:** APPLIED
- **Why this status:** Describes what is printed; adding `print(GBestCost)` would be a code change.

### C2-05 Wrong figure cross-reference: Figure 2.4 is the flowchart
- **Location:** ¶1299
- **Original:** "a plot similar to the one shown in Figure2.4 at I=200"
- **Issue:** Figure 2.4 (¶1308) is the flowchart; the convergence plots are Figure 2.3 (¶1295).
- **Evidence:** captions ¶1295, ¶1308.
- **Correction:** "Figure 2.3".
- **Status:** APPLIED
- **Why this status:** Certain target.

### C2-06 Wrong table cross-reference: mutation variants are in Table 2.2
- **Location:** ¶1407
- **Original:** "the mutation-operation variants shown in Table 2.1"
- **Issue:** Table 2.1 is the DE code; the schemes are Table 2.2 (¶1387).
- **Evidence:** ¶1311, ¶1387.
- **Correction:** "Table 2.2".
- **Status:** APPLIED
- **Why this status:** Certain target.

### C2-07 DE/current-to-best/1 derivation starts from "the DE function" but shows DE/best/2 lines
- **Location:** ¶1457–¶1462
- **Original:** "we take the code of the DE function as a basis. To do this, the piece of code" followed by the four-index DE/best/2 lines.
- **Issue:** The DE function contains two-index lines (¶1333, ¶1335); the quoted lines are those produced at ¶1446/¶1454.
- **Evidence:** compare ¶1461–¶1462 with ¶1446, ¶1454, ¶1333, ¶1335.
- **Correction:** "we take the code of the DE/best/2 algorithm as a basis".
- **Status:** APPLIED
- **Why this status:** Certain from the printed listings.

### C2-08 "K≥4 must always hold" is only true for single-difference schemes
- **Location:** ¶1291; listings ¶1428, ¶1446, ¶1486
- **Original:** "to perform the mutation operation (2.1), the condition K≥4 must always hold."
- **Issue:** DE/rand/2 and DE/best/2 need K≥6, DE/rand-to-best/1 K≥5; `np.random.choice(..., replace=False)` raises otherwise. The repository guards only `< 4`.
- **Evidence:** `np.random.choice` checks for each scheme (K=5 → ValueError for two-difference schemes, K=6 ok; K=4 → ValueError for rand-to-best, K=5 ok).
- **Correction:** After the sentence: "Schemes with two difference vectors (DE/rand/2 and DE/best/2, Section 2.4.1) require K≥6, and DE/rand-to-best/1 requires K≥5, because the indices are drawn without replacement and must differ from the current and, where used, the best vector."
- **Status:** APPLIED
- **Why this status:** Adds a missing restriction, reproduced by the reviewer.

### C2-09 Table 2.1 evaluates the objective three times per vector per iteration; Appendix B evaluates once
- **Location:** ¶1339–¶1342 (Table 2.1), ¶1361, ¶1660–¶1662, ¶1696–¶1698 (Exercise 4); note placed at ¶1372
- **Original:** `if function(TrialVector) < function(Generation[k]):` … `GenerationCosts = np.array([function(x) for x in Generation], dtype=float)`
- **Issue:** 3K evaluations per iteration against K in Appendix B and the library; Figures 2.5–2.7 are therefore not comparable with Chapter 1 on an evaluation basis. Secondary: asynchronous in-loop replacement with `BestDotNumber` refreshed only per iteration.
- **Evidence:** instrumented run K=25, I=200: 14,950 calls = K + 3K(I−1); repository `minimize_best` nfev = 5000.
- **Correction:** Applied: append to ¶1372 "Note that the listing of Table 2.1 is written for clarity: it evaluates the objective function three times per vector per iteration (3K evaluations per iteration, against K per iteration in the Appendix B version and in the PSO listing of Chapter 1), so the iteration axis of Figures 2.5–2.7 is not an equal-budget axis." Pending: rewrite Table 2.1 in the Appendix B form (stored costs, one evaluation per trial).
- **Status:** PENDING (partially applied)
- **Why this status:** Listing rewrite is a code change; the budget note is the certain part.

### C2-10 DE/rand-to-best/1 code takes the "to-best" difference from the current vector, not from the base vector
- **Location:** ¶1483–¶1487; Table 2.2 row ¶1400–¶1401 (image)
- **Original:** `i2 = BestDotNumber` / `i3 = k` / `DonorVector = Generation[i1] + F * (Generation[i2] - Generation[i3]) + F * (Generation[i4] - Generation[i5])`
- **Issue:** Standard form is x_r1 + F(x_best − x_r1) + F(x_r2 − x_r3); the chapter mixes the base x_r1 with a displacement belonging to x_k. Same F for both terms and crossover on current-to-rand are unstated simplifications.
- **Evidence:** reasoning; the Table 2.2 formula image could not be read (medium confidence).
- **Correction:** If Table 2.2 states the standard form, change the listing; otherwise say in ¶1406 that the chapter's variant uses (x_best − x_k); add "In the schemes with two differences the same factor F is used for both terms."
- **Status:** PENDING
- **Why this status:** Depends on the image formula (AD-11).

### C2-12 Exercise 4 task statement omits the objective function
- **Location:** ¶1626; ¶1628
- **Original:** "solve the problem of minimizing the objective function with its variables ranging from -500 to 500"
- **Issue:** No function is named; only step 1 (¶1628) points to Exercise 5 of Chapter 1.
- **Evidence:** ¶1626 carries no equation image; ¶1628.
- **Correction:** "minimizing the objective function of Exercise 5 of Chapter 1 (D=10) with its variables ranging from -500 to 500".
- **Status:** APPLIED
- **Why this status:** Certain from ¶1628.

### C2-13 "selection" is used for the crossover choice, then defined as the third operator
- **Location:** ¶1275; ¶1280
- **Original:** "Mathematical model of this selection is described by the expression given below for the d-th component of vector u:"
- **Issue:** The component-wise choice in (2.3) is called "selection" five lines before "Selection" is introduced as operator (2.4).
- **Evidence:** reasoning.
- **Correction:** "The component-wise choice is described by the expression given below for the d-th component of vector u:"
- **Status:** APPLIED
- **Why this status:** Removes a real operator ambiguity without changing a claim.

### C2-14 Notation: x_{i−1} appears only in the selection sentence; chained ≠ for mutual distinctness
- **Location:** ¶1280, ¶1255; (2.4) image
- **Original:** "between the vectors xi-1 and u"; "xr1≠xr2≠xr3≠x"
- **Issue:** Unintroduced subscript; the chain does not express pairwise distinctness.
- **Evidence:** reasoning (medium).
- **Correction:** "between the current vector x and the trial vector u"; "r1, r2, r3 ≠ k, pairwise distinct".
- **Status:** NOTED
- **Why this status:** Notation that must agree with the equation images; copyedit may harmonise the prose once the authors confirm.

### C2-15 ¶1304 cites (1.4), the PSO global best over personal bests, for the DE best vector
- **Location:** ¶1304
- **Original:** "and the best vector of the population is determined (1.4)"
- **Issue:** (1.4) defines g from personal bests; DE has none.
- **Evidence:** Chapter 1 ¶197–¶199.
- **Correction:** "and the best vector of the population (the one with the smallest objective-function value) is determined."
- **Status:** APPLIED
- **Why this status:** Removes a technically wrong cross-reference; wording is certain.

### C2-16 Index/vector confusion: "xr1 = rand[1, K]"
- **Location:** ¶1405 (paragraph carries an equation image; the edited clause is away from it)
- **Original:** "The case xr1=rand[1, K] corresponds to a stochastic search"
- **Issue:** rand[1, K] is an index; xr1 a vector.
- **Evidence:** reasoning; ¶1511 uses the index `BestDotNumber`.
- **Correction:** "The case r1=rand[1, K] (a random index) corresponds …"
- **Status:** APPLIED
- **Why this status:** Certain; words only.

### C2-17 Review question uses "zeroth-order", a term Chapter 2 never introduces
- **Location:** ¶1553; ¶1247
- **Original:** "Why is the DE method considered a zeroth-order optimization method?"; ¶1247 "a derivative-free search method"
- **Issue:** Two spellings across chapters and no definition in this one.
- **Evidence:** grep: only ¶466 uses "zero-order".
- **Correction:** ¶1247 → "… provide a derivative-free (zero-order) search method …".
- **Status:** APPLIED
- **Why this status:** Adds the missing definition.

### C2-18 Errata-confirmed: the SADE fragment is not indented
- **Location:** ¶1535
- **Original:** `if np.random.rand() < tau1:` / `F = FLower + np.random.rand() * (FUpper - FLower)` / …
- **Issue:** `SyntaxError` as printed; must also be indented to the `for k` body when inserted after ¶1531.
- **Evidence:** `compile()` of ¶1535; Appendix B ¶7802–¶7805 is correct.
- **Correction:** As in `docs/errata.md` item 11.
- **Status:** PENDING
- **Why this status:** Code paragraph; the brief keeps this errata item out of the text pass.

### C2-21 Errata-confirmed: population minimum of 4 is stated
- **Location:** ¶1291
- **Original:** "the condition K≥4 must always hold"
- **Issue:** Correct for (2.1); the gap for two-difference schemes is C2-08.
- **Evidence:** `src/metaopt/de.py` `_de_loop`; `tests/test_de.py`.
- **Correction:** None beyond C2-08.
- **Status:** NOTED
- **Why this status:** No change.

### C2-22 Exercises 1 and 3 show no expected output
- **Location:** ¶1582; ¶1621–¶1623
- **Original:** `print(v)` with no result shown; "the vector x has been updated to the vector u because the condition f(u)<f(x) is satisfied."
- **Issue:** The learner cannot self-check Exercise 1; Exercise 3's claim is correct.
- **Evidence:** `.venv/bin/python`: Exercise 1 gives `[ 2.12 -9.96 -2.02  3.74 -1.04]`; Exercise 3 f(x)=3.1, f(u)=1.74.
- **Correction:** Print the Exercise 1 result after ¶1582; optionally quote f(x)=3.1 and f(u)=1.74 in ¶1623.
- **Status:** PENDING
- **Why this status:** The output line is a new code-style paragraph; the authors may prefer to show it as a listing cell.

### C2-23 Exercise 4: inconsistent function names and no output step
- **Location:** ¶1634, ¶1671, ¶1713; ¶1711; ¶1546
- **Original:** `def DEBest1bin(...)`, `def DERand1bin(...)`; "display the result"; `OptimizationResult = DEBest1bin(...)`
- **Issue:** Four naming schemes for the same two algorithms across the book; step 4 says "display" but nothing is printed.
- **Evidence:** Appendix B ¶7716, ¶7751.
- **Correction:** Use `DEBest`/`DERand` in Exercise 4 and ¶1546; add `print(OptimizationResult[0])` after ¶1713.
- **Status:** PENDING
- **Why this status:** Renames in code.

### C2-24 Garbled replacement instruction for DE/best/2 and a stray space in DE/rand/2
- **Location:** ¶1440–¶1446; ¶1428
- **Original:** ¶1440 "To do this, after the line"; ¶1444 "must be modified as follows"; ¶1428 `i1, i2, i3 , i4, i5 = ...`
- **Issue:** "after the line X must be modified" is not a sentence; the space before the comma is valid Python but inconsistent.
- **Evidence:** reasoning.
- **Correction:** ¶1440 "To do this, the line"; ¶1444 "must be replaced with". ¶1428 (code) not edited.
- **Status:** APPLIED
- **Why this status:** Prose fix is certain by analogy with ¶1422–¶1428; the code space goes to a later code pass.

### C2-25 Table 2.1 cells ¶1329 and ¶1343 are unindented in the extraction
- **Location:** ¶1329, ¶1343
- **Original:** `CostFunctionValues.append(GenerationBestCost)` at column 0
- **Issue:** If the DOCX cells really lack indentation, a reader copying the table gets wrong code; may be an extraction artifact.
- **Evidence:** extraction text (low confidence).
- **Correction:** Verify in the DOCX; indent to 4 and 8 spaces.
- **Status:** NOTED
- **Why this status:** Needs a visual check of the table cells.

### C2-26 Parameter recommendations attributed to [2] and [3] look doubtful
- **Location:** ¶1289–¶1290
- **Original:** "Values of the parameter F are chosen in the range 0.4...1"; "Rainer Storn, in [2], recommends … CR … 0.3 or within the range 0.8...1. Sometimes it is recommended to set F=0.8, CR=0.9 [3]."
- **Issue:** "0.4…1" has no source; CR = 0.3 from [2] is unusual; F=0.8/CR=0.9 is Storn's own advice, attributed here to a 2024 paper.
- **Evidence:** reasoning only, citations not checked (low confidence).
- **Correction:** Authors to re-check [2] and [3].
- **Status:** PENDING
- **Why this status:** Citation content (AD-08).

### C2-27 References: inconsistent formatting
- **Location:** ¶1721–¶1725
- **Original:** three author-list styles, two DOI styles, two dash styles.
- **Issue:** Formatting only; [1] and [5] bibliographically correct, [2]–[4] unverified.
- **Evidence:** reasoning.
- **Correction:** One style.
- **Status:** NOTED
- **Why this status:** Copyedit.

### C2-28 Table 2.1 explanation of the index-selection cell does not match the cell split
- **Location:** ¶1332–¶1334
- **Original:** ¶1334 "Runs the iterations and selects three distinct population indices, with the best vector used as the base vector."
- **Issue:** One explanation for two code cells; `AllIndexes` and the `[k, i1]` exclusion are unexplained.
- **Evidence:** reasoning (medium).
- **Correction:** Split into two explanations (iteration loop / base-vector choice).
- **Status:** NOTED
- **Why this status:** Explanation-cell wording belongs to the copyedit, and it depends on C2-01.

---

## Chapter 3 — Grey Wolf Optimizer

### C3-01 EPD-GWO is compared with GWO/mGWO on an unequal evaluation budget
- **Location:** ¶2045, ¶2060 (listing), ¶2072 (prose), Figure 3.8 caption ¶2074
- **Original:** `WolvesCosts = np.array([function(x) for x in Pack], dtype=float)` twice per iteration; ¶2072 "did not produce better results than those obtained using the GWO and mGWO algorithms."
- **Issue:** The listing evaluates the whole pack twice per iteration (9975 evaluations for K=25, I=200 against 5000 for GWO/mGWO); the repository re-evaluates only the replaced wolves (7388); Figure 3.8 compares per iteration without saying so.
- **Evidence:** `ch3_check.py` counting wrapper: GWO 5000, mGWO 5000, EPDGWO 9975 (= 25 + 199·50); repo `epd(...).nfev == 7388`.
- **Correction:** Applied: append to ¶2072 "Note that each iteration of the EPD-GWO listing costs 2K objective-function evaluations (the whole pack is evaluated twice; K + ⌊K/2⌋ if only the replaced wolves are re-evaluated), against K for GWO and mGWO, so Figure 3.8 is not an equal-budget comparison with Figures 3.5 and 3.7." Pending: re-evaluate only the replaced wolves in the listing (`WolvesCosts[g] = function(Pack[g])` in the loop, drop ¶2060).
- **Status:** PENDING (partially applied)
- **Why this status:** Listing change pending; the budget note is certain.

### C3-02 "Near the α-, β-, δ-wolves" — the EPD replacement offset spans the whole box
- **Location:** ¶1992, ¶2001 (prose), ¶2051–¶2055 (listing); (3.9) image
- **Original:** ¶1992 "placed near the α-, β-, and δ-wolves"; ¶2001 "cover the neighborhoods of the α-, β-, and δ-wolves"; listing `Pack[g] = XAlpha + np.random.choice([-1, 1]) * (lb + np.random.rand(len(Vars)) * (ub - lb))`
- **Issue:** The offset is a uniform point from the whole box (mean |offset| ≈ 10 on [−20, 20]), faithful to Saremi et al. [4], but "near" misdescribes it.
- **Evidence:** `default_rng(0)`: mean |off| = 9.98, max 20.0; `gwoepd.py` identical.
- **Correction:** ¶1992 "… generated around the α-, β-, and δ-wolves with a random displacement drawn from the full range of each variable (the result is then clipped to the feasible domain)."; ¶2001 "… constructed so as to place new wolves around the α-, β-, and δ-wolves (the displacement is drawn from the full range of each variable, so it can be as large as the domain width) …".
- **Status:** APPLIED
- **Why this status:** Describes the listing correctly.

### C3-04 Table 3.1 omits the `lb`/`ub` definitions that the next line uses
- **Location:** ¶1821–¶1823 (Table 3.1)
- **Original:** `CostFunctionValues = []` followed directly by `Pack = lb + np.random.rand(PackSize, len(Vars)) * (ub - lb)`
- **Issue:** `NameError` when typed from the table; the single block (¶1906–¶1907) has the lines.
- **Evidence:** table vs block comparison in `ch3_check.py`.
- **Correction:** Insert two rows after ¶1821 with `lb = np.array([d[0] for d in DomainVarsList], dtype=float)` / `ub = …` and an explanation cell.
- **Status:** PENDING
- **Why this status:** New code rows.

### C3-05 Table 3.1 indentation does not parse as extracted
- **Location:** ¶1833, ¶1840–¶1850, ¶1873, ¶1889
- **Original:** three rows at column 0; the α/β/δ block one level too deep.
- **Issue:** `SyntaxError: unexpected indent (line 9)` for the re-assembled table; the single block compiles. May be a table-cell artefact.
- **Evidence:** `compile(table_code, ...)`.
- **Correction:** Match the indentation of ¶1913–¶1946.
- **Status:** PENDING
- **Why this status:** Code cells; needs a DOCX check first.

### C3-06 Minimum pack size: prose says K > 3, library accepts K = 3
- **Location:** ¶1759
- **Original:** "Thus, a necessary condition for running the GWO algorithm is K>3."
- **Issue:** Three leaders suffice; K > 3 is the condition for ω-wolves to exist, not for the algorithm to run.
- **Evidence:** `metaopt.gwo.minimize(..., population_size=3, iterations=5)` runs, nfev = 15.
- **Correction:** "Thus, the algorithm requires at least three wolves (K≥3); in practice K>3, so that ω-wolves exist."
- **Status:** APPLIED
- **Why this status:** Restriction stated as the code enforces it.

### C3-07 Exercise 2 is not runnable with only steps 1–2 of Exercise 1
- **Location:** ¶2154; ¶2170–¶2172
- **Original:** "perform steps 1 and 2 of Exercise 1 and obtain the initialized pack Pack"
- **Issue:** Step 4 uses `XAlpha`, `XBeta`, `XDelta` from steps 3–5 of Exercise 1 → `NameError`.
- **Evidence:** names traced through ¶2122–¶2144 and ¶2164–¶2172.
- **Correction:** "1) perform steps 1–5 of Exercise 1 and obtain the initialized pack Pack and the leader positions XAlpha, XBeta, XDelta;"
- **Status:** APPLIED
- **Why this status:** Certain from the printed listings; text only.

### C3-08 "Average position of the α, β, δ wolves" misstates the update
- **Location:** ¶1738
- **Original:** "the agent's new position is determined as the average position between the positions of the α, β, and δ wolves"
- **Issue:** The code averages x1, x2, x3 = leader − A·D; averaging the leaders would collapse the pack.
- **Evidence:** ¶1936 `X = np.mean([X1, X2, X3], axis=0)`; `gwo.py` `_gwo_update`.
- **Correction:** "… the average of three candidate positions, each obtained by moving from the α-, β-, or δ-wolf by a random fraction of the distance to it;"
- **Status:** APPLIED
- **Why this status:** Describes the listing.

### C3-09 Worked example names the domain array `Domain` and calls the objective "compiled"
- **Location:** ¶1899 vs ¶1959
- **Original:** "we will use the compiled function ObjectiveFunction … The feasible domain of the variables is represented by the array Domain"
- **Issue:** Nothing is compiled; `Domain` does not exist; ¶1959 uses `DomainVarsList` and `Vars`.
- **Evidence:** grep of Chapter 1 for `Domain = `, `lambdify`, `compiled`: none; ¶381–¶383.
- **Correction:** "… we will use the function ObjectiveFunction defined in Section 1.3 for the objective function (1.13), the variable list Vars, and the domain list DomainVarsList with the bounds xd.min=-20, xd.max=20 (D=10)."
- **Status:** APPLIED
- **Why this status:** Describes the listing's call.

### C3-10 a = 2 is never used by the loop; schedule starts at step 2
- **Location:** ¶1805; ¶1838/¶1916; ¶2160, ¶2284
- **Original:** "it is recommended to set: a_{i=1}=2 and a_{i=I}=0"; `a = 2 - 2 * (step / Iterations)` with `range(2, Iterations + 1)`; ¶2284 "a=2 – at the start of the iterations"
- **Issue:** The first update uses a = 2 − 4/I (1.98 for I = 200); iteration 1 is the initial sample — a convention the chapter never states.
- **Evidence:** `ch3_check.py`: a at step 2 = 1.980; first a < 1 at step 101 (linear), 142 (quadratic).
- **Correction:** Append to ¶1805 "Note that iteration 1 is the random initialization, so the position updates run for i = 2, …, I; with a = 2 − 2i/I as in the listings below, a takes the values from 2 − 4/I at the first update down to 0 at the last."; ¶2284 "a≈2 – at the first position update".
- **Status:** APPLIED
- **Why this status:** Adds the missing convention from the code.

### C3-11 Wolf index: prose is 1-based, code and Exercise 2 are 0-based
- **Location:** ¶1747, ¶1753; ¶1851, ¶2159; ¶2152
- **Original:** "the index of the k-th wolf belongs to the range of integers 1...K"; ¶2152 "for the first wolf (k = 0)"
- **Issue:** Same symbol k in two conventions without a bridge.
- **Evidence:** reasoning (medium).
- **Correction:** ¶1747 append "In the Python code the wolves are indexed 0…K−1."; ¶2152 "for the first wolf (index k = 0 in the code)" (paragraph carries an object; edited clause is away from it).
- **Status:** APPLIED
- **Why this status:** Bridging remark; certain.

### C3-12 Flowchart description: "dimensionality of the set of agents" and equation references
- **Location:** ¶1812
- **Original:** "setting the dimensionality of the set of agents (wolves, in the case of GWO) and the number of iterations I. Next, random initialization of the pack is performed (1.1), (1.2)"
- **Issue:** "Dimensionality" is D elsewhere; (1.1) is the position-vector definition.
- **Evidence:** Chapter 1 ¶174–¶180; ¶1746.
- **Correction:** "setting the population size (the pack size K, in the case of GWO) and the number of iterations I. Next, the pack is randomly initialized according to (1.2),"
- **Status:** APPLIED
- **Why this status:** Certain wording from the chapter's own definitions.

### C3-13 Exercise 3 listing prints once, after the loop
- **Location:** ¶2249–¶2250
- **Original:** `        clear_output(wait=True)` then `    print(...)` dedented.
- **Issue:** Prints "100.0 %" once; harmless but a typesetting slip.
- **Evidence:** compile succeeds; behaviour traced.
- **Correction:** Indent ¶2250 (or delete both lines).
- **Status:** PENDING
- **Why this status:** Code.

### C3-14 "Half of the pack" versus `PackSize // 2`; leaders used before the move
- **Location:** ¶1993; ¶2046; ¶2025–¶2027
- **Original:** "at each iteration the worst half of the pack is destroyed"; `worst_count = PackSize // 2`
- **Issue:** 12 wolves for K = 25; the leaders used for replacement are those before the GWO move.
- **Evidence:** listing; `gwoepd.py` docstring.
- **Correction:** "at each iteration the ⌊K/2⌋ worst wolves (12 for K=25, i.e., the wolves with the largest objective-function values) are destroyed. Newly initialized wolves are created in their place, around the positions that the α-, β-, and δ-wolves held at the start of the iteration, before the GWO position update."
- **Status:** APPLIED
- **Why this status:** Describes the listing.

### C3-15 Exercises 1 and 4 do not display what the task asks for
- **Location:** ¶2105 vs ¶2146–¶2148; ¶2350 vs ¶2352
- **Original:** `print(AlphaWolfNumber)` …; `OptimizationResult = GWO(...)` with no print.
- **Issue:** Positions are asked for, indices printed; Exercise 4 prints nothing once `clear_output`/`print` go.
- **Evidence:** reasoning (medium).
- **Correction:** Add `print(XAlpha, XBeta, XDelta)` and `print(OptimizationResult[0])`.
- **Status:** PENDING
- **Why this status:** Code additions.

### C3-16 Exercise 4: one run per setting cannot separate K/I effects from noise
- **Location:** ¶2287, ¶2354–¶2355
- **Original:** "compare the results obtained with each other and determine the effect of the factors K and I"
- **Issue:** Single runs; budget K·I not held fixed.
- **Evidence:** reasoning; ¶1964 (medium).
- **Correction:** Ask for 5–10 repetitions and the median; note K·I per setting.
- **Status:** PENDING
- **Why this status:** Changes the exercise (AD-06).

### C3-17 "once a < 1, the algorithms converge"
- **Location:** ¶1983
- **Original:** "once a<1, the algorithms converge."
- **Issue:** a < 1 only guarantees |A| < 1 (exploitation), not convergence of the best value.
- **Evidence:** `ch3_check.py` crossing points (medium).
- **Correction:** "once a < 1 every component of A satisfies |A| < 1, so all wolves move toward the leaders and the search contracts (exploitation only)."
- **Status:** PENDING
- **Why this status:** Changes the authors' interpretation; medium confidence.

### C3-18 Algorithm name: EPD-GWO / EPDGWO / GWO-EPD / GWOEPD
- **Location:** ¶1990, ¶1992, ¶2072; ¶2007; ¶2361; Chapter 5 tables; repo
- **Original:** heading "Evolutionary population dynamics GWO (EPD-GWO)"
- **Issue:** Four spellings for one algorithm across the book and the code map.
- **Evidence:** `docs/experiment-protocol.md`; `tests/test_gwo.py`.
- **Correction:** Pick one (GWO-EPD per [4]) and add "(`GWOEPD` in the companion code)" once at ¶1990.
- **Status:** PENDING
- **Why this status:** Naming decision touching Chapter 5 tables (AD-12).

### C3-19 Figure 3.6 described by colour only
- **Location:** ¶1983; Figure 3.6 ¶1985
- **Original:** "The red segments … exploration … green segments … exploitation"
- **Issue:** Stage split carried only by colour.
- **Evidence:** reasoning (low).
- **Correction:** Mark the a = 1 crossing on each curve.
- **Status:** NOTED
- **Why this status:** Figure change; recorded for the improvement plan.

### C3-20 References: formatting inconsistencies
- **Location:** ¶2358–¶2361
- **Original:** mixed dash styles, initials spacing, quoted vs unquoted titles; no [n] numbers in the extract.
- **Issue:** Formatting only; content looks correct.
- **Evidence:** reasoning.
- **Correction:** Normalise; confirm numbering in the typeset version.
- **Status:** NOTED
- **Why this status:** Copyedit.

### C3-23 Table 3.1 explanation cell is garbled
- **Location:** ¶1885
- **Original:** "Check: if the found on the iteration solution is better, that previous (CurrentBestCost < BestWolvesCost), then update BestWolvesCost as a CurrentBestCost"
- **Issue:** Unparseable explanation of the best-so-far bookkeeping.
- **Evidence:** reasoning.
- **Correction:** "If the best value found in this iteration is lower than the best so far (CurrentBestCost < BestWolvesCost), update BestWolvesCost and BestWolvesPosition."
- **Status:** APPLIED
- **Why this status:** Explanation cell (not code); meaning certain from the adjacent code rows.

### C3-24 "A review of several of its modifications"
- **Location:** ¶1742
- **Original:** "and a review of several of its modifications"
- **Issue:** Exactly two are covered.
- **Evidence:** headings ¶1968, ¶1990.
- **Correction:** "and a review of two of its modifications (mGWO and EPD-GWO)".
- **Status:** APPLIED
- **Why this status:** Certain.

---

## Chapter 4 — Benchmarks (with Appendices A and B)

### C4-01 Whitley: location and value cells swapped (errata 8)
- **Location:** ¶2703 (Table 4.1, location), ¶2704 (value)
- **Original:** `0`; `1`
- **Issue:** `WhitleyFunction` is 0 at the all-ones vector and D²(1/4000 − cos 1 + 1) at the origin (1.83979 for D=2).
- **Evidence:** `tests/test_benchmarks.py::test_whitley_minimum_is_zero_at_the_all_ones_vector`; `WhitleyFunction(np.zeros(2)) = 1.83979`, `WhitleyFunction(np.ones(30)) = 0.0`; `tests/test_manuscript_corrections.py` asserts `["1", "0"]`.
- **Correction:** ¶2703 → `1`; ¶2704 → `0`.
- **Status:** APPLIED
- **Why this status:** Cell values backed by a test.

### C4-02 Perm 0, d, β: location cell `i-1` (errata 8)
- **Location:** ¶2533
- **Original:** `i-1`
- **Issue:** Zero at x_i = 1/i; 29 (D=2) and 2.0e91 (D=30) at i−1.
- **Evidence:** `tests/test_benchmarks.py::test_known_reference_values`; `Perm0DBetaFunction(1/np.arange(1,31.)) = 3.1e-32`.
- **Correction:** ¶2533 → `1/i`.
- **Status:** APPLIED
- **Why this status:** Test-backed.

### C4-03 Rotated Hyper Ellipsoid: lower bound `-65.53` (errata 8)
- **Location:** ¶2575
- **Original:** `-65.53≤xi` (second line ¶2576 `xi≤65.536`)
- **Issue:** Appendix B registers (−65.536, 65.536).
- **Evidence:** `src/metaopt/benchmarks.py`; ¶7332; `test_manuscript_corrections.py` asserts `"-65.536≤xi"`.
- **Correction:** ¶2575 → `-65.536≤xi`.
- **Status:** APPLIED
- **Why this status:** Code-backed.

### C4-04 Xin-She Yang: noise described as normal on [0, 1] (errata 8)
- **Location:** ¶2707 (Table 4.1, text after the formula image)
- **Original:** `, εi – random value normaly distributed on the range [0, 1] `
- **Issue:** Appendix B uses `np.random.random` (uniform on [0, 1)); a normal draw is not confined to [0, 1].
- **Evidence:** ¶7274; `metaopt.benchmarks.uniform_noise`; `test_manuscript_corrections.py`.
- **Correction:** `, εi – random value uniformly distributed on [0, 1) ` (record carries `allow_object`; the ", εi – " adjacent to the image is unchanged).
- **Status:** APPLIED
- **Why this status:** Code-backed.

### C4-05 Schwefel 2.26: value is the mean, not the sum (errata 8)
- **Location:** ¶2626, ¶2625 (cells unchanged); note in ¶3109
- **Original:** `≈-418.983` at `≈420.969`
- **Issue:** Appendix B divides by D; readers used to the sum form expect −418.983·D.
- **Evidence:** `Schwefel226Function(np.full(30, 420.969)) = -418.983`; `results/reference_minima.csv`.
- **Correction:** Append to ¶3109 "The form used in this handbook (Appendix B) divides the sum by D, so the minimum value is ≈−418.983 for every D; the sum form found in many papers has the minimum −418.983·D."
- **Status:** APPLIED
- **Why this status:** Adds the missing convention.

### C4-06 Elliptic: D ≥ 2 restriction unstated (errata 8)
- **Location:** Table 4.1 row 12 (¶2475–¶2479); note in ¶3085
- **Original:** domain `-0.5≤xi≤0.5`, location `0`, value `0`
- **Issue:** Exponent i/(D−1) divides by zero at D=1.
- **Evidence:** `tests/test_benchmarks.py::test_domains_match_dimension_and_contain_finite_values`.
- **Correction:** Append to ¶3085 "The function is defined for D≥2 (the exponent i/(D−1) is undefined for D=1)." (a table footnote is layout work; the 4.2 sentence carries the restriction).
- **Status:** APPLIED
- **Why this status:** Adds a missing restriction.

### C4-07 Trid: location and value cells blank although the formula gives them (errata 8)
- **Location:** ¶2673, ¶2674
- **Original:** `*`, `**`
- **Issue:** Standard Trid; minimum at x_i = i(D+1−i), value −D(D+4)(D−1)/6.
- **Evidence:** `tests/test_benchmarks.py::test_known_reference_values` (D=6).
- **Correction:** ¶2673 → `i(D+1−i)`; ¶2674 → `−D(D+4)(D−1)/6`.
- **Status:** APPLIED
- **Why this status:** Test-backed closed form.

### C4-08 Paviani: box already inside the open interval; remark belongs in 4.2
- **Location:** ¶2513–¶2514 (unchanged); ¶3091
- **Original:** `2.0001≤xi` / `xi≤9.9999`
- **Issue:** log(x−2), log(10−x) defined only on (2, 10); the cell needs no edit.
- **Evidence:** `tests/test_benchmarks.py::test_paviani_warns_and_is_nonfinite_outside_the_open_interval`.
- **Correction:** Append to ¶3091 "The logarithms in the function are defined only on the open interval (2, 10), which is why the domain in Table 4.1 is [2.0001, 9.9999]."
- **Status:** APPLIED
- **Why this status:** Adds the missing definition.

### C4-09 Griewank separability and Powell differentiability flags (errata 8)
- **Location:** ¶2826 (Table 4.2 Griewank, Separability); ¶2877 (Powell, Differentiability); ¶3095
- **Original:** ¶2826 `+`; ¶2877 `-`; ¶3095 "Powell is a smooth, unimodal function … Its minimization is complicated by the absence of derivatives at the minimum point."
- **Issue:** The product of cosines is not separable. Powell as coded (`sum |x_i|^(i+1)`, i ≥ 1) is differentiable at the origin; ¶3095 contradicts itself.
- **Evidence:** `docs/errata.md` item 8; Appendix B ¶7088, ¶7140 (Powell: medium confidence pending the image formula).
- **Correction:** ¶2826 → `-`; ¶2877 → `+`; ¶3095 → "Powell is a smooth, unimodal function with a flat surface that grows with distance from the minimum." If the Table 4.1 image for Powell is not the Appendix B formula, the authors should reject the Powell records (AD-13).
- **Status:** APPLIED
- **Why this status:** Both flags follow the printed Appendix B code, which the whole Table 4.1/4.2 audit uses as the reference; the Powell image remains an author check.

### C4-10 Quintic: location cell omits the third real root
- **Location:** ¶2558
- **Original:** `-1 or 2`
- **Issue:** p(x) = (x+1)(x−2)(x³ − 2x² + 4x + 2) has a third real root ≈ −0.402628; 3^D global minima.
- **Evidence:** `np.roots([1,-3,4,2,-10,-4])` → 2, −1, −0.4026279411861239 (+ complex pair); `QuinticFunction(np.full(30, -0.40262794))` = 3.1e−7, 0 at full precision.
- **Correction:** ¶2558 → `-1, 2 or ≈-0.4026`.
- **Status:** APPLIED
- **Why this status:** Reproduced arithmetic.

### C4-11 Cosine Mixture: minimum is known for the Appendix B formula
- **Location:** ¶2446, ¶2447
- **Original:** `*`, `**`
- **Issue:** −0.1·cos(5πx) + x² ≥ −0.1 with equality only at 0, so the minimum is −0.1·D at the origin.
- **Evidence:** `CosineMixtureFunction(np.zeros(2)) = -0.2`, `(np.zeros(30)) = -3.0`; proof above.
- **Correction:** ¶2446 → `0`; ¶2447 → `-0.1D`.
- **Status:** APPLIED
- **Why this status:** Computed value with a one-line proof.

### C4-12 Quintic described as unimodal
- **Location:** ¶3098
- **Original:** "Quintic. It is a unimodal function, characterized by steeply increasing values, strong nonlinearity, and a flat bottom."
- **Issue:** Table 4.1 lists several minimizers per coordinate; Table 4.2 ¶2893 marks it multimodal.
- **Evidence:** C4-10; ¶2893.
- **Correction:** "Quintic. It is a multimodal function with several equivalent global minima in each coordinate (xi ∈ {−1, 2, ≈−0.4026}), characterized by …"
- **Status:** APPLIED
- **Why this status:** Description contradicted both tables; the correct description is certain.

### C4-13 Styblinski-Tang described as having several global minima
- **Location:** ¶3115
- **Original:** "A multimodal function with several deep global minima."
- **Issue:** One global minimum (all x_i = −2.903534) and 2^D − 1 local minima.
- **Evidence:** per-coordinate value −39.16617 at −2.903534 (matches ¶2662 `-39.166D`); −25.029 at +2.7468.
- **Correction:** "A multimodal function with one global minimum and 2^D − 1 local minima of similar depth."
- **Status:** APPLIED
- **Why this status:** Certain from Table 4.1 and the computation.

### C4-14 Qing: minimum is not at the centre
- **Location:** ¶3096
- **Original:** "Qing. It has a gently sloping bottom, at the center of which the minimum is located."
- **Issue:** 2^D minima at x_i = ±√i (Table 4.1 ¶2545); the origin gives Σi².
- **Evidence:** `QingFunction(np.sqrt(np.arange(1,31.))) = 1.2e-28`; `tests/test_benchmarks.py`.
- **Correction:** "Qing has 2^D equivalent global minima at xi = ±√i; between them the surface is nearly flat, which makes it difficult for gradient-based optimization methods. Away from the minima, the function grows sharply."
- **Status:** APPLIED
- **Why this status:** Certain from Table 4.1 and the code.

### C4-15 Deb No. 1: description does not match the formula
- **Location:** ¶3081
- **Original:** "…oscillating multimodal function with exponentially decaying amplitude. The global minimum lies in a narrow region with a high concentration of local extrema."
- **Issue:** −(1/D)·Σ sin⁶(5πx_i) has constant amplitude and 5^D equally deep minima.
- **Evidence:** `Deb1Function(np.full(D, 0.1)) = -1` for D = 2, 30 (medium confidence; image not read).
- **Correction:** "Deb No. 1 is a periodic multimodal function whose 5^D global minima of equal depth are evenly spaced in each coordinate; between them lie flat plateaus near zero."
- **Status:** PENDING
- **Why this status:** Medium confidence and the Table 4.1 image was not read; authors to confirm (AD-13).

### C4-16 Happy Cat: Table 4.2 says differentiable, 4.2 text and formula say not
- **Location:** ¶2835; ¶3088
- **Original:** ¶2835 `+`; ¶3088 "It is non-smooth …"
- **Issue:** |Σx² − D|^(1/4) has an unbounded one-sided derivative on the sphere containing the minimum.
- **Evidence:** ¶7093; `(1e-16)**(1/8) = 0.01`.
- **Correction:** ¶2835 → `-`.
- **Status:** APPLIED
- **Why this status:** Flag contradicted the authors' own text and the formula.

### C4-17 Periodic: Table 4.2 says unimodal, 4.2 text and formula say multimodal
- **Location:** ¶2857; ¶3092
- **Original:** ¶2857 `+`
- **Issue:** Local minima at x_i = kπ (value ≈ 1), global 0.9 at 0.
- **Evidence:** 1-D: f(0) = 0.9, f(π) = 0.9999948, f(π ± 0.1) = 1.00996.
- **Correction:** ¶2857 → `-`.
- **Status:** APPLIED
- **Why this status:** Computed.

### C4-18 Stretched V Sine Wave: Table 4.2 says unimodal, 4.2 text says multimodal
- **Location:** ¶2989; ¶3114
- **Original:** ¶2989 `+`
- **Issue:** sin²(50·r^0.1) + 0.1 oscillates; 23 strict local minima along x = (t, 0).
- **Evidence:** grid count on 200 001 points.
- **Correction:** ¶2989 → `-`.
- **Status:** APPLIED
- **Why this status:** Computed.

### C4-19 Quartic: 4.2 text says unimodal, Table 4.2 says multimodal
- **Location:** ¶3097; ¶2887
- **Original:** ¶3097 "Quartic is a smooth, unimodal function …"; ¶2887 `-`
- **Issue:** Convex quartic plus additive noise; convention for noisy functions unstated.
- **Evidence:** ¶7150 (medium).
- **Correction:** ¶2887 → `+` with a "noisy" footnote, or reword ¶3097.
- **Status:** PENDING
- **Why this status:** Convention choice (AD-13).

### C4-20 Rosenbrock: unimodal claim does not hold at D = 30
- **Location:** ¶2905; ¶3100
- **Original:** ¶2905 `+`; "Rosenbrock is a unimodal, with a curved valley function."
- **Issue:** For D ≥ 4 a second local minimum exists near (−1, 1, …, 1); the experiments use D = 30.
- **Evidence:** BFGS from (−1, 1, …, 1): f = 3.98662, gradient norm < 1e-10.
- **Correction:** ¶2905 → `-` with footnote "unimodal for D ≤ 3; one additional local minimum (f ≈ 3.99) for larger D"; adjust ¶3100.
- **Status:** PENDING
- **Why this status:** Brief lists it as an author decision (AD-13).

### C4-21 Schwefel 2.4 marked separable although every term contains x_1
- **Location:** ¶2928
- **Original:** `+`
- **Issue:** Σ[(x_i − 1)² + (x_1 − x_i²)²] couples x_1 with every coordinate.
- **Evidence:** ¶7179 (medium; image may differ).
- **Correction:** ¶2928 → `-` after checking the image.
- **Status:** PENDING
- **Why this status:** Depends on the image formula (AD-13).

### C4-22 Xin-She Yang No. 2 and No. 4 marked discontinuous
- **Location:** ¶3050, ¶3062; ¶3044
- **Original:** all `-`
- **Issue:** Both are compositions of continuous functions; only non-differentiable at x_i = 0. No. 1's `-` is defensible only by the noise.
- **Evidence:** ¶7274, ¶7278, ¶7289 (medium; probably copied from the Jamil–Yang survey).
- **Correction:** ¶3050, ¶3062 → `+`; state the noisy-function convention for ¶3044.
- **Status:** PENDING
- **Why this status:** Convention and source question (AD-13).

### C4-23 Weierstrass: 4.2 text "non-smooth" vs Table 4.2 differentiable
- **Location:** ¶3121; ¶3033
- **Original:** "This functions is a non-smooth, with a self-similar structure …"; ¶3033 `+`
- **Issue:** Implementation truncates at k = 20 (C∞); prose describes the limit function.
- **Evidence:** ¶7260–¶7263 (low).
- **Correction:** Add "the implemented version truncates the series at k = 20 and is therefore differentiable, but with very large derivatives".
- **Status:** NOTED
- **Why this status:** Neither statement is wrong on its own; low confidence.

### C4-24 Section 4.3 names `run_once()` and `Results`; the code names differ
- **Location:** ¶3141, ¶3142
- **Original:** "The run_once() function performs one independent optimization run."; "…stored in the Results dictionary"
- **Issue:** Appendix B defines `run_once_perf`/`run_once_time` and `PerfResults`/`TimeResults`.
- **Evidence:** ¶7964, ¶7973, ¶8102, ¶8120.
- **Correction:** "The run_once_perf() function …"; "… stored in the PerfResults dictionary (the timing cell of Section 5.2 uses TimeResults) …".
- **Status:** APPLIED
- **Why this status:** Names certain from the printed code.

### C4-25 Section 4.3 library list omits matplotlib; plotly (Exercise 1) is never installed
- **Location:** ¶3135; Appendix B ¶7014–¶7017; ¶3175
- **Original:** ¶3135 lists tqdm, joblib, openpyxl, ipywidgets, numpy, pandas; ¶7017 `%pip install matplotlib`; ¶3175 `import plotly.graph_objects as go`
- **Issue:** Prose omits matplotlib; no cell installs plotly.
- **Evidence:** the ¶idx above.
- **Correction:** Applied: ¶3135 "… pandas is used for organizing and exporting experimental results, and matplotlib is used for plotting." Pending: `%pip install plotly` in the LIBRARIES cell or Exercise 1 step 1 (code).
- **Status:** APPLIED
- **Why this status:** Prose part certain; the install line is a code cell (repository follow-up R-05).

### C4-26 Exercise 1 code does not run: `function` is undefined and has the wrong signature
- **Location:** ¶3185, ¶3210; ¶3177
- **Original:** `FunctionToShow = lambda x1, x2: …`; `Z = function(np.column_stack([X1.ravel(), X2.ravel()])).reshape(X1.shape)`
- **Issue:** `NameError`; renaming alone gives `TypeError`.
- **Evidence:** executed with plotly stubbed; with `Z = FunctionToShow(X1, X2)` the grid is (200, 200), min 0.0028.
- **Correction:** Replace both lines with `Z = FunctionToShow(X1, X2)`.
- **Status:** PENDING
- **Why this status:** Code lines.

### C4-27 Exercise 2: problem statement says 20 runs, code sets 100 (see also C5-20)
- **Location:** ¶3239 vs ¶3244 (code cell)
- **Original:** "for D=10, I=500, Runs=20, and Population = 25"; `Runs = 100`
- **Issue:** The two disagree; 100 runs makes the exercise the full 14 × 54 × 100 experiment (hours).
- **Evidence:** the ¶idx; timing cell ¶8061 and ¶3764 use 20.
- **Correction:** `Runs = 20` in ¶3244 (reviewers' reading) or "Runs=100" in ¶3239; add a run-time warning.
- **Status:** PENDING
- **Why this status:** The "code wins" rule would turn the exercise into a multi-hour run that both reviewers think unintended; ¶3244 is a code cell. Authors decide (AD-14).

### C4-28 Benchmark name spelled "Xin-She-Yang" only in Tables 4.1 and 4.2
- **Location:** ¶2706, ¶2712, ¶2718, ¶2724; ¶3041, ¶3047, ¶3053, ¶3059
- **Original:** `Xin-She-Yang`, `Xin-She-Yang №2`, …
- **Issue:** Section 4.2, Appendix A and the code labels write "Xin-She Yang"; the surname is Yang.
- **Evidence:** ¶3123–¶3126, ¶6988–¶7000, ¶7354–¶7357.
- **Correction:** `Xin-She Yang` (№2, №3, №4) in all eight cells.
- **Status:** APPLIED
- **Why this status:** Name certain; breaks text search otherwise.

### C4-29 Python and NumPy version mentions
- **Location:** Chapter 4 none; Appendix B ¶7015 (unpinned `%pip install numpy`), ¶8264–¶8265 (runtime recording)
- **Original:** as quoted.
- **Issue:** No literal version floor; `joblib.Parallel(return_as="generator")` needs joblib ≥ 1.3 but is guarded.
- **Evidence:** grep; ¶7991–¶7997.
- **Correction:** None required; reference the front-matter version (FM-02) from ¶3135 if desired.
- **Status:** NOTED
- **Why this status:** Inventory.

### C4-30 Sum of Squares described with variable interaction
- **Location:** ¶3116
- **Original:** "A unimodal function with a cumulative effect among its variables."
- **Issue:** Σ i·x_i² is separable; "cumulative" fits Schwefel 1.2.
- **Evidence:** ¶7233 (low).
- **Correction:** "A separable unimodal function whose i-th coordinate is weighted by i, giving elongated axis-aligned contours."
- **Status:** NOTED
- **Why this status:** Low confidence; wording.

### C4-31 Xin-She Yang (No. 1) described with exponential decay
- **Location:** ¶3123
- **Original:** "Xin-She Yang is a multimodal function with exponential decay. …"
- **Issue:** Σ ε_i·|x_i|^i contains no exponential; multimodality is not a property of the deterministic part.
- **Evidence:** ¶7274 (low).
- **Correction:** "Xin-She Yang is a separable, noisy function; each coordinate contributes |x_i|^i scaled by a random factor … Not differentiable at x_i = 0."
- **Status:** PENDING
- **Why this status:** Low confidence; image not read (AD-13).

---

## Chapter 5 — Efficiency analysis (with Appendices C and E)

### C5-01 Section 5.2 says the timing settings are "the same as Section 5.1 (20 runs …)"
- **Location:** ¶3764
- **Original:** "The experiment settings are the same as in Section 5.1 (20 runs, population 25, 500 iterations, D=30); fixed seeds are used for reproducibility, and the runs can optionally be executed in parallel via joblib."
- **Issue:** Section 5.1 and the B2 cell use 100 runs; the B3 timing cell uses 20 and runs sequentially.
- **Evidence:** ¶7922 `Runs = 100`; ¶8061 `Runs = 20`; ¶8068 `USE_PARALLEL = False`; ¶3310.
- **Correction:** "The experiment settings coincide with those of Section 5.1 except for the number of runs: 20 runs per benchmark–algorithm pair instead of 100 (population 25, 500 iterations, D=30), as set in the timing cell of Appendix B; fixed seeds are used for reproducibility, and the runs are executed sequentially (USE_PARALLEL = False) so that the timings are not distorted by CPU contention, although the code can optionally execute them in parallel via joblib."
- **Status:** APPLIED
- **Why this status:** The printed code's value wins and the sentence says so.

### C5-02 Appendix E header says "mean of 100 runs"
- **Location:** ¶12206
- **Original:** "(seconds per run, mean of 100 runs; D=30, I=500, population=25)"
- **Issue:** Contradicts ¶8061, ¶3764 and the title the B3 cell itself writes (`f"mean of {Runs} runs"`, ¶8196).
- **Evidence:** ¶8061, ¶8196, ¶8070.
- **Correction:** "(wall-clock seconds per run, time.perf_counter; mean of 20 sequential runs; D=30, I=500, population=25; Intel Core i9-14900KF, see Section 5.2)" (also closes C5-03 for the header). If the table was in fact produced with 100 runs, ¶8061 and ¶3764 must change instead (AD-15).
- **Status:** APPLIED
- **Why this status:** Code value wins; the alternative is logged.

### C5-03 Appendix E does not say whether the cells are wall-clock or CPU time
- **Location:** ¶12206; ¶3765
- **Original:** "(seconds per run, …)"
- **Issue:** `TIME_METRIC = "wall"` (¶8070) is stated nowhere in the text.
- **Evidence:** ¶8070, ¶8105–¶8109, ¶8158, ¶8277.
- **Correction:** Header as in C5-02; append to ¶3765 "The table reports wall-clock time (time.perf_counter); the CPU time (time.process_time) is stored in raw_timing_results.npz but is not printed."
- **Status:** APPLIED
- **Why this status:** Adds a missing unit/definition from the code.

### C5-04 Table captions referenced in Chapter 5 do not exist in Appendices C and E
- **Location:** ¶3311 ("Tables C.1–C.4"), ¶3770 ("Table E.1"); Appendix C headings ¶8407, ¶9451, ¶10433, ¶11477; Appendix E ¶12205
- **Original:** all four C blocks headed "C2. Numerical representation …"; Appendix E has a title line, no "Table E.1".
- **Issue:** Cited captions are absent.
- **Evidence:** grep for "Table C." and "Table E.1" in the appendix extracts: none.
- **Correction:** Caption the blocks "Table C.1 — … (f1–f16)" … "Table C.4 — … (f48–f54)" and Appendix E "Table E.1 — …"; update the end TOC.
- **Status:** PENDING
- **Why this status:** Caption numbering is a structure/layout change handled with the TOC rebuild (structure pass), not a word-level correction.

### C5-05 Hardware and software environment incomplete; scope ambiguous
- **Location:** ¶3766
- **Original:** "… PC with Intel Core i9-14900KF (3.2 GH), 128 RAM."
- **Issue:** Units missing; no OS, Python, NumPy, joblib versions; not said whether Appendix C used the same PC or how many workers.
- **Evidence:** ¶3766; ¶7925, ¶7991, ¶8068.
- **Correction:** Applied: "(3.2 GHz), 128 GB RAM". Pending: "Both experiments (Appendix C and Appendix E) were run on one PC: … <OS>, Python <x.y.z>, NumPy <x.y.z>, joblib <x.y.z>. The search experiment used joblib with all cores; the timing experiment ran sequentially." — values must come from the authors.
- **Status:** PENDING (partially applied)
- **Why this status:** Versions cannot be invented (AD-16).

### C5-06 Seed policy and random stream not described in the protocol paragraph
- **Location:** ¶3310
- **Original:** "every independent run used its own fixed seed of the random number generator (the base seed 12345), so that the results are reproducible."
- **Issue:** The per-run seed rule and the legacy global stream are unstated; the reproducibility claim does not hold for the Generator-based companion library.
- **Evidence:** ¶7965, ¶7985, ¶8103, ¶8139; `docs/reproducibility.md`.
- **Correction:** Append: "The seed of run r on benchmark p with algorithm a is 12345 + 100000·p + 1000·a + r (0-based indices), set with np.random.seed before the run; all optimizers of Appendix B draw from NumPy's legacy global generator, so re-running the Appendix B listings reproduces the saved file, whereas code that uses numpy.random.Generator (including the companion library) does not reproduce these traces." (one record with C5-07 and C5-08 on ¶3310).
- **Status:** APPLIED
- **Why this status:** Rule copied from the printed code; honest qualifier.

### C5-07 Evaluation budget "12,500 for the other algorithms" is not exact for ME-D-PSO; budget not in the protocol
- **Location:** ¶3770; ¶3310
- **Original:** "GWOEPD performs about 18,500 objective-function evaluations per run (versus 12,500 for the other algorithms)"
- **Issue:** GWOEPD: 25 + 499·37 = 18,488 (correct). ME-D-PSO restarts re-sample and re-evaluate the swarm (+26 per restart). ¶3310 never states the budget or the stopping rule.
- **Evidence:** ¶7568–¶7582, ¶7604–¶7619, ¶7880–¶7900; `docs/experiment-protocol.md`.
- **Correction:** ¶3310 insert "Every run stops after 500 iterations; there is no target-error stopping. With population 25 this is 12,500 objective-function evaluations per run for all algorithms except GWOEPD (18,488, because the replaced half of the pack is re-evaluated every iteration) and ME-D-PSO (12,500 plus 26 evaluations per restart)."; ¶3770 "(versus 12,500 for the other algorithms; ME-D-PSO slightly more, depending on the number of restarts)".
- **Status:** APPLIED
- **Why this status:** Counts reproduced from the printed code.

### C5-08 Ranks in Tables 5.1/5.2 are computed on the rounded printed values; no ranking code is given
- **Location:** ¶3315, ¶3310, ¶3707, ¶3757
- **Original:** ¶3310 "only this file is used for the statistical indicators, the plots, and the ranks"; ¶3315 "Dense ranking is used …"
- **Issue:** Dense ranks of the 3-significant-digit cells reproduce every Table 5.1 entry and Table 5.2 sum exactly; ties (seven algorithms at rank 1 on f7, eleven on f13) are impossible on raw doubles, so the ranks came from the printed tables, contrary to ¶3310. No ranking code in B or D.
- **Evidence:** recomputation: 0 of 324 cells and 0 of 28 sums differ; grep "rank" in Appendix B/D: none.
- **Correction:** ¶3315 add "Ranks are assigned to the values of Tables C.1–C.4, i.e., after rounding to three significant digits; algorithms whose rounded values coincide share a rank."; ¶3310 "… only this file is used for the statistical indicators and the plots; the ranks are then taken from the rounded tables (see below)." Adding the `DataFrame.rank(method="dense")` snippet to Appendix B/D is a repository/code follow-up (R-06).
- **Status:** APPLIED
- **Why this status:** The ranking rule stated is the one that reproduces the printed tables.

### C5-09 Notch overlap is presented as a statistical test; no formal test is used
- **Location:** ¶3271 (paragraph carries the CI formula image; the edited sentences are away from it); ¶3785
- **Original:** "If these intervals overlap (are superimposed on one another at some point), then the medians are statistically similar; if they do not overlap, they are different."
- **Issue:** Notches are a rough visual guide; overlap does not establish equality; no hypothesis test anywhere.
- **Evidence:** reasoning; Appendix D ¶12128–¶12138; no `scipy.stats` in any listing.
- **Correction:** "If the intervals of two medians do not overlap, the medians differ with roughly 95% confidence; overlapping intervals do not prove that the medians are equal. The comparison in this chapter is descriptive (medians, minima, ranks, and their sums); no formal hypothesis test is applied, and differences in rank sums of a few units should not be read as significant." Review question ¶3785 left to the copyedit.
- **Status:** APPLIED
- **Why this status:** Honest qualifier; the book's own method is unchanged.

### C5-10 The median confidence-interval formula is an image
- **Location:** ¶3271 (formula object)
- **Original:** "The values of these levels are computed using the expression: [image] (the "+" sign …) [2]"
- **Issue:** Cannot be checked against matplotlib's notch Me ± 1.57·IQR/√n (computed in log10 space on log panels, ¶12128).
- **Evidence:** `paragraphs.jsonl` idx 3271 `has_object: true`; `word/document.xml` `w:object`.
- **Correction:** Authors to confirm the image reads Me ± 1.57·IQR/√n and add "This is the notch drawn by matplotlib.pyplot.boxplot(notch=True); on logarithmic plots it is computed from log10 of the values."
- **Status:** PENDING
- **Why this status:** Equation image (AD-17).

### C5-11 "GWO and mGWO show similar results … either one can be chosen" holds for rank sums, not medians
- **Location:** ¶3770
- **Original:** "The latter two algorithms show similar results on the benchmarks evaluated, so either one can be chosen."
- **Issue:** Rank sums 266/261 and 290/298 are close; medians differ by > 10× on 16 benchmarks, mostly in favour of mGWO (f3, f45, f50 …); GWO wins f2, f8.
- **Evidence:** recomputation over all 54 median rows (¶8584/¶8585, ¶11314/¶11315, ¶11654/¶11655, ¶8520/¶8521, ¶8904/¶8905).
- **Correction:** "The two algorithms have almost equal rank sums, but mGWO reaches markedly smaller medians on many unimodal and separable functions (f3, f5, f6, f12, f45, f50), while GWO is ahead on f2, f8, f9 and f15–f18. Either can be chosen as a starting point; mGWO when high precision near the optimum matters."
- **Status:** PENDING
- **Why this status:** Changes a recommendation (AD-18).

### C5-12 Tier assignment does not state its criterion; GWOEPD and DE/best excluded without saying why
- **Location:** ¶3770, ¶3776
- **Original:** "vonNeumann-PSO, GWO and mGWO algorithms (the first tier …) … DE/best and SADE algorithms (the second tier …)"
- **Issue:** GWOEPD (268) is two units behind GWO; DE/best has the best minimum rank sum (217); only execution time separates them, which the text never says.
- **Evidence:** Table 5.2 ¶3741, ¶3751, ¶3756; Appendix E Σ ¶13042–¶13048.
- **Correction:** "Taking the rank sums and the execution times together: vN-PSO, GWO and mGWO combine the best rank sums with the shortest run times (first tier). GWOEPD matches them in rank but costs 1.5× the evaluations; DE/best has the best minimum rank sum and SADE a good median sum, but both take 1.7× longer in total (second tier)."
- **Status:** PENDING
- **Why this status:** Recommendation wording (AD-18).

### C5-13 "this difference practically disappears" on expensive functions overstates an 8–13% gap
- **Location:** ¶3775; ¶3770
- **Original:** "but this difference practically disappears for expensive objective functions"
- **Issue:** DE/best over PSO: 1.10, 1.08, 1.12, 1.13, 1.11 on f20, f21, f37–f39.
- **Evidence:** ¶12518/¶12510, ¶12533/¶12525, ¶12773/¶12765, ¶12788/¶12780, ¶12803/¶12795.
- **Correction:** "… on the five most expensive functions (f20, f21, f37–f39) the DE variants are only 8–13% slower than PSO." (one record with C5-14).
- **Status:** APPLIED
- **Why this status:** Reproduced arithmetic from the printed cells.

### C5-14 Two-decimal timing cells make the "about 3 times" statement coarse
- **Location:** ¶3775; Appendix E cells; ¶8162, ¶8220
- **Original:** "The DE-based algorithms are about 3 times slower than PSO on inexpensive functions"
- **Issue:** Claim holds (2.2–4.25, median 3.17 over 43 cheap benchmarks) but 122 of 756 cells are ≤ 0.05 s printed to 0.01 s.
- **Evidence:** recomputation over Appendix E.
- **Correction:** Applied: "about 3 times (2–4 times across benchmarks)". Pending: print Table E.1 with three decimals (`round(..., 3)`, `"0.000"`) — code and a regenerated table.
- **Status:** PENDING (partially applied)
- **Why this status:** Table regeneration needs the raw file the repository does not have (AD-19).

### C5-15 Appendix E uses decimal commas
- **Location:** ¶12225–¶13048 (770 cells)
- **Original:** "0,07", "9,96", "15,22"
- **Issue:** Locale artefact; the export writes "0.00".
- **Evidence:** ¶8220.
- **Correction:** Replace "," by "." in all Appendix E cells.
- **Status:** NOTED
- **Why this status:** Mechanical 770-cell change; to be generated as a separate bulk record set by the copyedit tooling rather than hand-listed here.

### C5-16 One indicator label reads "Max"
- **Location:** ¶9472
- **Original:** "Max"
- **Issue:** All other 215 labels are "max".
- **Evidence:** parse of the indicator column.
- **Correction:** "max".
- **Status:** APPLIED
- **Why this status:** Certain.

### C5-17 "DE/rand is the worst and is not recommended" should be tied to the rank sums
- **Location:** ¶3774
- **Original:** "DE/rand is the worst and is not recommended."
- **Issue:** Supported by the rank sums (538, 562) but DE/rand has the single largest median on only 7 of 54 benchmarks.
- **Evidence:** ¶3737, ¶3752; recomputation.
- **Correction:** "DE/rand has the largest rank sums by both indicators (538 and 562) and the longest run times, and is therefore not recommended for this benchmark set."
- **Status:** APPLIED
- **Why this status:** Adds the evidence the claim rests on; no change of verdict.

### C5-18 "Efficiency" is used throughout but never defined
- **Location:** ¶3258, ¶3261, ¶3269, ¶3314, ¶3762, ¶3780
- **Original:** ¶3261 "Optimization algorithms can be evaluated using solution-quality statistics and computational cost."
- **Issue:** No definition to point the review question at.
- **Evidence:** reasoning.
- **Correction:** After ¶3261: "In this chapter the efficiency of an algorithm means the quality of the final objective-function value it reaches with a fixed budget …, summarised over independent runs by the median and the minimum, considered together with the execution time needed for that budget."
- **Status:** PENDING
- **Why this status:** Definition is the authors' to give (AD-18).

### C5-19 Reproduction-status paragraph missing
- **Location:** after ¶3311, before ¶3312
- **Original:** none (front matter ¶70 carries a one-line note only).
- **Issue:** Readers are not told at the tables that Appendix C/E are historical legacy-stream results that were not recomputed, nor that the repository's reduced study is a different protocol.
- **Evidence:** `docs/experiment-protocol.md`; `docs/final-audit.md` F3/F4; `results/full_experiment_cost_estimate.json` (8.75–65.6 h); `results/reduced_comparison_summary.json` (`matches_appendix_c: false`); `notebooks/05_fair_comparisons.ipynb`.
- **Correction:** Insert the "Reproduction status." paragraph drafted in the review (record `C5-19`, `insert_after` ¶3311).
- **Status:** APPLIED
- **Why this status:** Brief names this paragraph; every statement in it is sourced from repository files.

### C5-20 Chapter 4 Exercise 2 requires the full-size run and contradicts itself on the run count
- **Location:** ¶3239, ¶3244 (Chapter 4)
- **Original:** see C4-27.
- **Issue:** With 100 runs the exercise is the complete experiment at D = 10; no time warning.
- **Evidence:** Appendix E Σ row (167.27 s per full sweep at D = 30).
- **Correction:** `Runs = 20` in ¶3244 and a warning "With 20 runs this exercise executes 15,120 optimisation runs and takes on the order of an hour …; use USE_PARALLEL = True."
- **Status:** PENDING
- **Why this status:** Same decision as C4-27 (AD-14).

### C5-21 Timing classes: "moderate" GWOEPD is closer to the "slow" class
- **Location:** ¶3767–¶3769
- **Original:** "“fast” — all PSO-based algorithms, GWO, mGWO;" / "“moderate” — GWOEPD;" / "“slow” — all DE-based algorithms;"
- **Issue:** Σ: fast 9.95–10.58 s, GWOEPD 15.22 s, DE 16.89–17.29 s; the labels hide the gap sizes.
- **Evidence:** Appendix E Σ row ¶13035–¶13048.
- **Correction:** Add the Σ values in each line: "(Σ ≈ 10.0–10.6 s over the 54 benchmarks, Table E.1)", "(Σ = 15.2 s)", "(Σ = 16.9–17.3 s)".
- **Status:** APPLIED
- **Why this status:** Numbers copied from the printed table.

### C5-22 Repository protocol note misattributes the "20 runs" sentence to Chapter 6
- **Location:** `docs/experiment-protocol.md`, Appendix E section
- **Original:** "Chapter 6 prose once says the timing settings are "the same as in Section 5.1 (20 runs...)"."
- **Issue:** The sentence is ¶3764 in Chapter 5.
- **Evidence:** grep of `06-chapter-6.md`.
- **Correction:** "Section 5.2 (Chapter 5)".
- **Status:** REPO
- **Why this status:** Repository file only (R-01).

---

## Chapter 6 — Control problems (with Appendix D)

### C6-01 Cart-pole listing simulates the opposite task to the one formulated
- **Location:** ¶4051, ¶4056 (Problem 5 formulation); ¶4492 (`CartPoleStep`); ¶4544 (initial state `[np.pi, 0, 0, 0]`); ¶4556 (`reached` tests |S| < TOL); worked values ¶4565; Figures 6.11, 6.12, 6.23; Table 6.2 row 5
- **Original:** ¶4056 "The initial conditions … the pendulum in the lower stable equilibrium position … The final (desired) conditions … the upper unstable equilibrium position"; listing starts at φ=π and targets φ=0 with gravity entering as `phi_acc = (-(m+M)*g*s - …)/den`.
- **Issue:** Linearising the printed map at φ=0 gives a restoring torque: φ=0 is the hanging position, φ=π the upright one, so the listing swings the pendulum down, the reverse of the swing-up described. The Furuta listing of Exercise 4 is self-consistent (checked numerically); Problem 5 is not.
- **Evidence:** `metaopt.applications.cart_pole.step` (verbatim port): free motion from φ=0.05 stays bounded (max |φ| = 1.67 rad), from φ=π−0.05 diverges (99 rad); Furuta listing gives the opposite, correct result. (6.22) is an image.
- **Correction:** (a) keep the listing and numbers and rewrite the prose (φ from the downward vertical; swing-down task; rename Figure 6.11 a/b and the title) or (b) keep the prose, reverse the sign of every `g` term in `CartPoleStep`, and recompute ¶4565, Table 6.2 row 5, Tables 6.3/6.4 entries, Figures 6.12, 6.23, 6.24 g.
- **Status:** PENDING
- **Why this status:** Either option changes a result table or the problem statement (AD-20).

### C6-02 Cart-pole mass symbols: the listing uses m as the cart mass and M as the pendulum mass
- **Location:** ¶4051; ¶4492 (`m, M, length, g = 0.3, 0.2, 0.5, 9.81`)
- **Original:** "m and M are the reduced masses of the load and the cart, respectively (m=0.3 kg, M=0.2 kg)"
- **Issue:** In the listing M multiplies the ω² and g·sinφ·cosφ terms and the denominator is m + M·sin²φ, so M is the pendulum mass and m the cart mass — the reverse of the prose. (6.22) could not be checked.
- **Evidence:** algebraic form of ¶4492 against the standard cart-pole equations.
- **Correction:** "M and m are the reduced masses of the load and the cart, respectively (M=0.2 kg, m=0.3 kg), as in the listing CartPoleStep below". No numerical result changes.
- **Status:** APPLIED
- **Why this status:** Describes the roles the printed listing assigns; the brief lists it; the authors should check (6.22) carries the same assignment (AD-20).

### C6-03 Tolerances mislabelled as the components of the target vector XT
- **Location:** ¶4241
- **Original:** "the components of the vector XT are set equal to 10-2, 10-4, and 10-4 ‒ for each of the state variables x1, x2, and x3, respectively (XT={10^-2, 10^-4, 10^-4};)."
- **Issue:** XT = (1, 0, 0) (¶3892); the three numbers are the admissible deviations of (6.30), stored as `tolerances` (¶4230).
- **Evidence:** ¶4230–¶4235; ¶3892; ¶4148.
- **Correction:** "In addition, the admissible deviations Δx1, Δx2, Δx3 of (6.30) are set equal to 10⁻², 10⁻⁴, and 10⁻⁴ for the state variables x1, x2, and x3, respectively (tolerances = [1e-2, 1e-4, 1e-4]), while XT = (1, 0, 0)." (one record with C6-23 on ¶4241; superscripts restored with Unicode).
- **Status:** APPLIED
- **Why this status:** Certain from the listing.

### C6-04 Practical Exercise 1 uses a different plant and objective from Problem 1a
- **Location:** ¶5230 (task); ¶5234; ¶5261–¶5275
- **Original:** "Task: for a controlled plant described by the transfer function, perform optimal tuning of the PID controller coefficients with the requirement of zero overshoot and minimum control duration (settling time); plot the output of the closed-loop system."
- **Issue:** Errata item 2: Problem 1a is plant 1/((s+1)(1+s/5+s²)) with ITAE; the exercise is 1/(1+s)³ with a 2% settling-time criterion and overshoot not divided by r. The task names no plant.
- **Evidence:** `results/published_comparison.json` row "Problem 1a settling-time on the Problem 1a plant" (16.3, unmatched by design); exercise listing executed: `ObjectiveFunction(1,1,1)` = 650774.3635100485 = `pid.objective_chapter6_exercise1_settling(1,1,1)`.
- **Correction:** "Task: for a controlled plant described by the transfer function Gp(s) = 1/(1+s)³ ‒ note that this is a different plant from the one in Problem 1a ‒ perform optimal tuning … (settling time). Unlike Problem 1a, the control-quality criterion here is the 2% settling time of the step response, not the ITAE integral, and the overshoot term is max(0, max y − r), which for r = 1 coincides with the relative overshoot used in Problem 1a; the objective function below therefore differs from ObjectiveFunction1a in both the plant and the criterion. Plot the output of the closed-loop system."
- **Status:** APPLIED
- **Why this status:** Brief names it; wording fixed by the printed listing.

### C6-05 Description of ObjectiveFunction1b claims a "large penalty" the listing does not contain
- **Location:** ¶4275
- **Original:** "If alpha is non-negative, the system is unstable or marginally stable, and the function returns alpha, a large penalty that still increases with the degree of instability."
- **Issue:** The listing returns `alpha = max(poles.real)` unconditionally; for the Figure 6.1 d gains alpha = +0.651.
- **Evidence:** `pid.objective_1b(6, 0.5, 0.5)` = 0.65132.
- **Correction:** "If alpha is non-negative, the closed loop is unstable or marginally stable; the function still returns alpha, and because the search minimizes alpha, such points are automatically ranked worse than every stable point (no separate penalty is needed)."
- **Status:** APPLIED
- **Why this status:** Describes the listing.

### C6-06 Problem 5 "reached" is an any-time test; the printed feasible solution does not satisfy the final conditions at t = T
- **Location:** ¶4477–¶4485; ¶4554–¶4557; ¶4565
- **Original:** `reached = np.any(np.all(np.abs(S) < TOL, axis=1))`
- **Issue:** The formulation describes conditions at T; the listing accepts any sampled state inside the box. For the printed feasible vector the state is inside only at steps 182–197 and the last x exceeds Δx.
- **Evidence:** `cart_pole.simulate(WORKED_FEASIBLE)`: first inside step 182, 16 inside states, last state (0.00085, −0.0023, 0.00113, 0.00147).
- **Correction:** State the any-time rule in the prose and (6.45), or change to `np.all(np.abs(S[-1]) < TOL)` and recompute.
- **Status:** PENDING
- **Why this status:** Either a formula/prose rule change or a rerun (AD-20).

### C6-07 Cart-pole and Furuta models are explicit-Euler maps whose energy grows
- **Location:** ¶4494, ¶4492 (dt = 0.025), ¶5558 (dt = 0.02), ¶5196–¶5199
- **Original:** "The function CartPoleStep returns the updated values (i.e., those predicted by model (6.22) after 0.025 s)"
- **Issue:** Forward Euler amplifies free oscillations ≈1% per step (≈7× over the horizon); results are properties of the map, not of (6.22). No limitation stated.
- **Evidence:** free-motion test: max |φ| = 1.665 from φ₀ = 0.05 with F = 0.
- **Correction:** After ¶4494: "The map is a first-order (explicit Euler) discretisation of (6.22). It is not energy-conserving: with F=0 the amplitude of free oscillations grows by about 1% per step. All Problem 5 results refer to this discrete model …"; add a limitations sentence to the summary.
- **Status:** PENDING
- **Why this status:** Reviewer category author-decision; it qualifies the whole Problem 5 result set and belongs with C6-01/C6-06 (AD-20).

### C6-08 Exercise 3: prose describes a thresholded penalty, code applies a proportional one; resistance force not in the task
- **Location:** ¶5408, ¶5409, ¶5421, ¶5474–¶5478, ¶5506
- **Original:** ¶5409 "if they differ significantly, a penalty is imposed …; if not, there is no penalty component."; listing `1e8*(abs(x1-x2) + abs(v1-v_t) + abs(v2-v_t))`
- **Issue:** No tolerance; W = 0.01·g·(m1+m2) and the stick–slip logic are unmentioned; φ sign convention opposite to Problem 3.
- **Evidence:** `ObjectiveFunction(0.8,1.2,0.6)` = 2.096e8.
- **Correction:** Add a tolerance to the code or rewrite ¶5409 as proportional; add W and the dry-friction rule to ¶5408; note the φ convention after ¶5507.
- **Status:** PENDING
- **Why this status:** Code-or-prose choice (AD-21).

### C6-09 Exercise 4 listing states that it does not implement (6.47) as printed
- **Location:** ¶5534, ¶5559–¶5564, ¶5540 (image)
- **Original:** ¶5563 "Compared with the original formulas, the sign of every term containing g is reversed."
- **Issue:** The docstring disclaims the printed equation; ¶5542 "for the first system" has no second system.
- **Evidence:** free-motion test on the listing: consistent with ¶5534 (φ from the upward vertical).
- **Correction:** Print (6.47) in the code's convention and delete ¶5563, or keep (6.47) and add the convention sentence to ¶5538; delete "for the first system". ("Figure 6.26" → "Figure 6.25" is applied under C6-10.)
- **Status:** PENDING
- **Why this status:** Equation image and docstring (code) (AD-20).

### C6-10 Wrong figure, table and equation cross-references (13 places)
- **Location / Original / Correction:**
  1. ¶3903 "instability (the variant in Figure 6.1, c)" → "Figure 6.1, d" — APPLIED (a–c stable, d unstable: max Re pole −0.099, −0.069, −0.054, +0.651).
  2. ¶4032 "illustrated in Figure 6.10" → "Figure 6.9" — APPLIED.
  3. ¶4110 "Based on Figure 6.14" → "Figure 6.13" — APPLIED.
  4. ¶4120 "(Figure 6.15). In Figure 6.15" → "(Figure 6.14). In Figure 6.14" — APPLIED.
  5. ¶4122 caption "(6.27)" → "(6.28)" — APPLIED (¶4120 itself calls (6.28) the objective function).
  6. ¶4164 "Figure6.17" → "Figure 6.16" — APPLIED.
  7. ¶4280 "Figure 6.18 shows … (Figure 17, a)" → "Figure 6.17, b shows … (Figure 6.17, a)" — APPLIED (¶4275 ends "(Fig. 6.17)").
  8. ¶4284 "i.e. [image] (Fig. 6.19). In Fig. 6.18" → first reference "Fig. 6.18" — NOT applied: the wrong reference is the text immediately after the equation object; manual edit.
  9. ¶4294 "i.e. [image] (Fig. 6.18)" → "Fig. 6.19" — NOT applied, same reason.
  10. ¶4454 "penalty (6.41a)" → "(6.42a)"; "function (6.20a)" → "the objective function (6.43) for Problem 4a" — NOT applied: equation numbers are images and ¶4454 itself uses (6.43) for both problems; authors to confirm.
  11. ¶4565 "(left column of plots in Fig. 6.24)" → "Fig. 6.23" — APPLIED.
  12. ¶4606 "(Tables 6.2 and 6.3)" → "(Tables 6.3 and 6.4)" — APPLIED (with C6-13).
  13. ¶5534 "(Figure 6.26)" → "(Figure 6.25)" — APPLIED.
- **Issue:** Off-by-one references after a late renumbering.
- **Evidence:** figure captions ¶3908, ¶4040, ¶4102, ¶4122, ¶4152, ¶4162, ¶4278, ¶4286, ¶4296, ¶4474, ¶4576, ¶4621, ¶5536; table captions ¶4581, ¶4623, ¶5092, ¶5140.
- **Status:** APPLIED (10 of 13; items 8, 9, 10 pending)
- **Why this status:** Figure/table targets certain from the captions; the three exceptions sit next to equation objects or depend on equation numbering (AD-22).

### C6-11 Numerical bounds and the control-cost definition appear only in code comments
- **Location:** ¶4011, ¶4051, ¶4065–¶4067, ¶4070–¶4072 (images); listing ¶4439, ¶4527–¶4528, ¶4536–¶4537
- **Original:** "The control aτ is bounded in absolute value"; "F … bounded in absolute value"; code `a in [-1, 1]`, `F_MAX = 5.0`, `X_MAX = 0.7`, `Cr = sqrt(integral of F^2 dt)`
- **Issue:** |a| ≤ 1, |F| ≤ 5 N, |x| ≤ 0.7 m and √∫F²dt are only in code; units absent.
- **Evidence:** text and listing comments (medium; images not auditable).
- **Correction:** Write the bounds and units into ¶4011, ¶4051, ¶4065, ¶4070; state Problem 2 units.
- **Status:** PENDING
- **Why this status:** The images (6.19), (6.24), (6.25) may already carry them (AD-22).

### C6-12 Recommendations omit ME-D-PSO although its rank sums equal those of recommended algorithms; one "lowest minimum" claim is a tie
- **Location:** ¶5189, ¶5190–¶5192, ¶5199, Table 6.4
- **Original:** "For Problem 3, ME-D-PSO achieves the lowest minimum value"; ¶5191–¶5192 tiers.
- **Issue:** ME-D-PSO median-rank sum 29 = LDW-PSO (first tier), minimum-rank sum 30 = GWO (second tier); Problem 3 minimum 2.41E-1 shared with LDW-PSO. Tier criterion unstated.
- **Evidence:** Table 6.4 ¶5159–¶5187; Table 6.2 ¶4870, ¶4874.
- **Correction:** Applied: ¶5189 "ME-D-PSO and LDW-PSO share the lowest minimum value". Pending: state the tier rule in ¶5190 and place ME-D-PSO or explain its exclusion.
- **Status:** PENDING (partially applied)
- **Why this status:** The tie is table-backed; the tiers are the authors' recommendation (AD-23).

### C6-13 Table 6.4 is reproducible from Table 6.2 only with competition ("min") tie ranking, which the text does not state
- **Location:** ¶5140, ¶4606, ¶5189
- **Original:** "Table 6.4 — Sum of algorithm ranks by median and minimum values"
- **Issue:** Ties are frequent (all 14 on Problem 1b); only `rankdata(method="min")` over all seven problems reproduces both rows exactly.
- **Evidence:** `c6/ranks.py`; printed rows ¶5159–¶5187 (max difference 0; average/dense/ordinal differ by 12–15).
- **Correction:** Append to ¶4606 "Ranks are assigned per problem from the values in Table 6.2 at the printed precision; tied algorithms receive the same (best) rank and the next rank is skipped (competition ranking); Problem 1b, on which all algorithms tie, contributes rank 1 to every sum."
- **Status:** APPLIED
- **Why this status:** The rule stated is the one that reproduces the printed table.

### C6-14 Problem 1b: −0.3 is the analytic global minimum
- **Location:** ¶3914–¶3923, Table 6.2 rows 1b, ¶4621, ¶5109–¶5111, ¶5137
- **Original:** ¶5137 "* all algorithms showed almost the same result."
- **Issue:** The closed-loop polynomial is 5s⁴ + 6s³ + …, so the pole sum is −1.2 for any gains and max Re(p) ≥ −0.3; every algorithm found the optimum, which is non-unique. The chapter presents this as coincidence.
- **Evidence:** `sp.Poly(den, s).all_coeffs()` = [5, 6, 5Kd+6, 5Kp+5, 5Ki]; Vieta.
- **Correction:** After ¶3923 add the bound; replace ¶5137 with "* all algorithms reach the analytic minimum −0.3 of criterion (6.6); the ranks for Problem 1b are therefore all equal."; mention the asterisk under Figure 6.24.
- **Status:** PENDING
- **Why this status:** Adds a mathematical result to the authors' problem statement; their call (AD-23).

### C6-15 Errata item 1 (conditional expressions) confirmed; second location is Practical Exercise 1
- **Location:** ¶4557; ¶5272
- **Original:** `penalty_terminal = 0.0 if reached else W_TERMINAL * np.linalg.norm(S[-1])`; ¶5272 one 131-character line.
- **Issue:** Both parse; a wrap starting a line with `else` breaks them. `docs/errata.md` item 1 names the wrong second location.
- **Evidence:** `ast.parse` of all 46 blocks; line length of ¶5272.
- **Correction:** Parenthesise/split both lines; update the errata location text.
- **Status:** PENDING
- **Why this status:** Code lines; the errata text fix is a repository follow-up (R-02).

### C6-16 Errata item 3 (crane roundoff) confirmed: prose says the penalty is absent
- **Location:** ¶4385; ¶4375–¶4376
- **Original:** "In this case there are no penalty components, since the crane's velocity satisfies constraint (6.16) (Figure 6.21, b)."
- **Issue:** `dx1.max()` = 1.2000000000000635, penalty 6.35e-8 is included in 0.4209773021079328.
- **Evidence:** `crane.polynomial_profiles(WORKED_POLY_FEASIBLE)["penalty"]` = 6.350475700855895e-08; `results/published_comparison.json`.
- **Correction:** "In this case the penalty components vanish up to floating-point roundoff (the computed maximum velocity exceeds 1.2 m/s by about 6·10⁻⁸ m/s), so the value is essentially the criterion alone; the crane's velocity satisfies constraint (6.16) (Figure 6.21, b)."
- **Status:** APPLIED
- **Why this status:** Brief names it; value reproduced.

### C6-17 Errata item 6 confirmed; setup cell comment contains untranslated Cyrillic
- **Location:** ¶4128; ¶4130–¶4141; ¶4238
- **Original:** ¶4238 `# np.trapz для NumPy < 2`; ¶4141 `subprocess.check_call([... "pip", "install", *missing])`
- **Issue:** As errata item 6; "для" untranslated; `np.trapz` no longer exists in NumPy 2.5.
- **Evidence:** extract; `hasattr(np, "trapz")` False in NumPy 2.5.4.
- **Correction:** Comment → `# np.trapz for NumPy < 2`; consider moving the subprocess cell to a footnote.
- **Status:** PENDING
- **Why this status:** Code paragraphs (comment included).

### C6-18 Table 6.1 loses the domain-to-problem mapping and the exponent; run seeds not stated
- **Location:** ¶4580–¶4604
- **Original:** domain row with five cells ("10-5…5", "0…10", "-500…500", "-1.5…1.5") against eight iteration cells.
- **Issue:** Merged cells invisible in the extract; "10-5" lost its superscript; no seeds or generator for the 30 runs; illustrative vectors in 6.2 lie outside −1.5…1.5.
- **Evidence:** extract; ¶3310.
- **Correction:** Make merged cells explicit; 10⁻⁵; add the seed sentence and the remark on hand-chosen vectors.
- **Status:** PENDING
- **Why this status:** Table structure must be checked in the DOCX; seeds are author information (AD-24).

### C6-19 Table 6.3 rows for Problems 1a, 3 and 4b have fewer cells than the header
- **Location:** ¶5099–¶5108, ¶5115–¶5120, ¶5124–¶5129
- **Original:** 1a: 3 cells; 3: 5 cells; 4b: 5 cells of 6.
- **Issue:** From Table 6.2 the missing entries are: 1a median third VCT-PSO; 1a minimum second ME-D-PSO, Ring-PSO, vN-PSO, SADE; 1a minimum third VCT-PSO, DE/rand; 3 minimum third Ring-PSO, GWOEPD; 4b minimum third LDW-PSO, Ring-PSO.
- **Evidence:** Table 6.2 ¶4660–¶4690, ¶4868–¶4882, ¶4996–¶5010 (medium: merged cells cannot be seen).
- **Correction:** Check the DOCX table; fill the cells.
- **Status:** PENDING
- **Why this status:** May be merged cells; result-table change (AD-24).

### C6-20 Appendix D: hard-coded sandbox paths, misleading header, no link from Chapter 6
- **Location:** ¶11952, ¶11954, ¶11974–¶11976, ¶12085, ¶11963–¶11965; ¶4606
- **Original:** `UPLOADS_DIR = "/mnt/user-data/uploads"`, `OUT_DIR = "/mnt/user-data/outputs"`
- **Issue:** Sandbox paths fail on a reader's machine; "LIBRARIES INSTALLATION" header only imports; `sys` unused; Chapter 6 never says what produced Figure 6.24; `\mathbfit` needs Matplotlib ≥ 3.7.
- **Evidence:** Appendix D runs end to end after replacing the two paths.
- **Correction:** Relative paths, header "# IMPORTS", drop `import sys`, state Matplotlib ≥ 3.7; add to ¶4606 which file/code produced the box plots.
- **Status:** PENDING
- **Why this status:** Code paragraphs; the ¶4606 sentence depends on the authors naming the results file (AD-24).

### C6-21 Paragraph styles: prose set as code and code set as prose
- **Location:** ¶4001, ¶4009, ¶4024 (prose tagged `MathematicaCellInput`); ¶4349–¶4376, ¶4403–¶4464, ¶4496–¶4520 and Appendix D ¶11952–¶12199 (code without the code style)
- **Original:** e.g. ¶4001 "[MathematicaCellInput] The mountain car control problem …"
- **Issue:** Wrong wrapping and font in print.
- **Evidence:** style tags.
- **Correction:** Reassign styles.
- **Status:** NOTED
- **Why this status:** Typesetting; structure/copyedit pass (set_style records).

### C6-22 Listings define variables that are never used, and duplicate imports
- **Location:** ¶4314, ¶4318, ¶4322, ¶5246–¶5251, ¶5317, ¶5323, ¶5327
- **Original:** `obstacle_count`, `start`, `end`, `domain` unused; duplicate `from scipy.interpolate import CubicSpline`.
- **Issue:** Editing the "problem data" block has no effect on `ObjectiveFunction2`.
- **Evidence:** listing text.
- **Correction:** Consume `p`, `r`, `domain` in the objective or drop the names; remove duplicate imports.
- **Status:** PENDING
- **Why this status:** Code.

### C6-23 Problem 1a listing contains a 1e12 instability guard that neither (6.32) nor the prose mentions
- **Location:** ¶4217–¶4218, ¶4224–¶4225; ¶4241
- **Original:** `if np.any(np.roots(den).real >= 0): return 1e12`; `if not np.all(np.isfinite(y)): return 1e12`
- **Issue:** A fourth component of the objective; for the Figure 6.1 d gains the value is exactly 1e12.
- **Evidence:** `pid.objective_1a_itae(6, 0.5, 0.5)` = 1e12.
- **Correction:** Add to ¶4241 "If the closed loop is unstable (a pole with a non-negative real part) or the step response is not finite, the function returns the constant 10¹² without evaluating (6.32); this keeps the search away from the unstable region." (same record as C6-03).
- **Status:** APPLIED
- **Why this status:** Describes the listing.

### C6-24 Problem 4a: "90 is the global minimum" is asserted, not shown
- **Location:** ¶4454
- **Original:** "gives 90 (the number 90 is the global minimum of function (6.20a))"
- **Issue:** No argument; Table 6.2 is consistent but not a proof.
- **Evidence:** `mountain_car.objective_4a(WORKED_4A_FEASIBLE)` = 90 (medium).
- **Correction:** "gives 90; none of the optimization runs in Section 6.3 found a smaller value, so 90 is taken as the minimum …" or supply the argument.
- **Status:** PENDING
- **Why this status:** Author's claim (AD-23).

### C6-25 Chapter Summary and Section 6.3 do not state the method's limitations
- **Location:** ¶5189, ¶5194–¶5199
- **Original:** no limitations paragraph.
- **Issue:** Penalty-weight dependence, most runs on 4b/5 ending in the penalty region, fixed integrators, Problem 1b non-unique optimum.
- **Evidence:** Table 6.2 rows 4b and 5.
- **Correction:** Add a "Limitations" paragraph before ¶5194 and one review question.
- **Status:** PENDING
- **Why this status:** New authorial content (AD-23).

### C6-26 Reference name misspelt
- **Location:** ¶5701
- **Original:** "Åströn K.J., Hägglund T."
- **Issue:** The author is Åström.
- **Evidence:** well-known reference; ¶3886 cites it as [2].
- **Correction:** "Åström K.J., Hägglund T."
- **Status:** APPLIED
- **Why this status:** Certain.

### C6-27 Python/NumPy/library version and installation mentions (inventory)
- **Location:** ¶4128, ¶4130–¶4141, ¶4134, ¶4238; Appendix D none
- **Original:** "NumPy ≥ 2.0 is required for np.trapezoid"; `%pip install "numpy>=2.0" scipy sympy matplotlib`
- **Issue:** No Python version; `\mathbfit` needs Matplotlib ≥ 3.7; `np.allclose` with array `atol` works but is undocumented.
- **Evidence:** extract; NumPy 2.5.4 tests.
- **Correction:** State the environment once ("Python 3.12, NumPy ≥ 2.0, SciPy, SymPy, Matplotlib ≥ 3.7").
- **Status:** NOTED
- **Why this status:** Inventory; FM-02 fixes the Python version in the front matter.

---

## Chapter 7 — Optimal design problems

### C7-01 Both Problem 4 worked values were computed with 2.9·As instead of the listing's 29.4·As
- **Location:** ¶5859; listing ¶5851
- **Original:** "ObjectiveFunction(np.array([7, 35, 8])) returns 37500188.3. Thus, in this case one or two penalties are imposed. … ObjectiveFunction(np.array([8.4,29.6562,7.5])) returns the number 159.36"
- **Issue:** The listing (`29.4 * As + 0.6 * b * h`) returns 37500373.8 and 381.96; the printed numbers reproduce exactly with coefficient 2.9. 29.4 is the published (Amir–Hasegawa/Gandomi) cost and the only version consistent with Table 7.1 (minimum 3.59E2 = 359.208). At (7, 35, 8) only g1 is active.
- **Evidence:** `concrete_beam_components`: 37500373.8, 381.96000000000004, 359.20799999999997; listing with 2.9 → 37500188.3, 159.36; g1 = 0.375, g2 = −19.83.
- **Correction:** "returns 37500373.8. Thus, in this case the penalty for the constraint g1 is imposed."; "returns the number 381.96".
- **Status:** APPLIED
- **Why this status:** Brief names the values; reproduced from the printed listing.

### C7-02 I-beam listing uses `tw` where the flange area needs `tf`; the chapter's optimum is half the literature value
- **Location:** ¶5769, ¶5770; Table 7.1 Problem 2 (¶6211–¶6256); ¶5781
- **Original:** `g1 = 2 * b * tw + tw * (h - 2 * tf) - 300`; `… + 2 * b * tw * (4 * tf**2 + …)`; `… + 2 * tw * b**3`
- **Issue:** Physical area and inertias use tf in those places (the objective ¶5772 does); the listing's optimum is 0.006626 (= Table 7.1 6.63E-3) versus 0.0130741 in the literature; the literature design is infeasible under the listing.
- **Evidence:** SLSQP from five starts on both formulations; `engineering_design.py` lines 18–20 reproduce the listing.
- **Correction:** (a) fix the three terms and re-run Problem 2 (Table 7.1/7.2/7.3, Figure 7.6d, worked value) or (b) keep the listing and state that g1–g2 follow [2, 3] with tw in the flange terms, so results are not comparable with 0.0130741. Check image (7.4).
- **Status:** PENDING
- **Why this status:** Changes a result table or the formulation (AD-25).

### C7-03 Problem 2 prose constants (L = 5200 cm, E = 5.23·10⁶ kN/cm²) contradict the listing's `5000 / I`
- **Location:** ¶5760
- **Original:** "… the maximum vertical deflection of the beam is PL3/48EI, when the beam length is L=5200 cm and the beam material's modulus of elasticity is E=5.23*106 kN/cm2."
- **Issue:** 5000, 18·10⁴·h and 15·10³·b in the listing correspond to P = 600 kN, Q = 50 kN, L = 200 cm, E = 2·10⁴ kN/cm²; no P makes both constants match the printed L and E. The bounds sentence is followed by nothing.
- **Evidence:** 600·200³/(48·2·10⁴) = 5000; (600·200/4)·12/2 = 180000; (50·200/4)·12/2 = 15000.
- **Correction:** "… when P = 600 kN, Q = 50 kN, the beam length is L = 200 cm and the modulus of elasticity is E = 2·10⁴ kN/cm²" (verify against [2, 3]); supply the bounds (b ∈ [10, 50], h ∈ [10, 80], tw, tf ∈ [0.9, 5]).
- **Status:** PENDING
- **Why this status:** Brief lists the Problem 2 constants as an author decision (AD-25).

### C7-04 Chapter summary recommends GWO and GWOEPD, which Table 7.3 ranks 11th and 13th of 14
- **Location:** ¶6577; Table 7.3 ¶6541–¶6570
- **Original:** "… recommend the use of the Ring-PSO, vonNeumann-PSO, LDW-PSO, ME-D-PSO, GWO, GWOEPD, and SADE algorithms."
- **Issue:** Median rank sums: Ring 14, vN 18, LDW 22, ME-D 32, PSO 34, BB 36, SADE 36, DE/best 38, VCT 51, DE/rand 57, GWO 61, GWOEPD 63, IA 65, mGWO 81; GWO and GWOEPD are among the four worst.
- **Evidence:** Table 7.3 values; recomputed from Table 7.1.
- **Correction:** "… recommend Ring-PSO, von Neumann-PSO and LDW-PSO first, then ME-D-PSO, PSO, BB-PSO, SADE and DE/best; the GWO family and IA-PSO ranked lowest on these problems." or drop GWO/GWOEPD.
- **Status:** PENDING
- **Why this status:** Brief lists the Chapter 7 recommendation as an author decision (AD-26).

### C7-05 Problem 4 iteration count: 200 in Section 7.1, 100 in Section 7.2
- **Location:** ¶5862 (listing `IterationNumber = 200`) vs ¶5968 ("for Problem 4, I=100")
- **Original:** as quoted.
- **Issue:** The two disagree on the budget behind Table 7.1; Problems 2, 3, 5 agree.
- **Evidence:** text comparison.
- **Correction:** Make one match the actual experiment.
- **Status:** PENDING
- **Why this status:** Which value produced Table 7.1 is unknown; the reviewer does not apply the "code wins" rule here and neither does this log (AD-26).

### C7-06 Robot gripper bounds: prose and code disagree on f and δ; the δ symbol is missing
- **Location:** ¶5882 (paragraph carries an object; a glyph is lost between "1 ≤" and "≤ 3") vs ¶5957
- **Original:** prose "0 ≤ f ≤ 100, 0 ≤ l ≤ 300, 1 ≤  ≤ 3"; code `[0, 150]` for f, `[1, np.pi]` for δ
- **Issue:** Upper bounds differ (100 vs 150; 3 vs π); literature has 10 ≤ f ≤ 150, 1 ≤ δ ≤ 3.14.
- **Evidence:** text; `examples/robot_gripper.py` line 15 comment is stale.
- **Correction:** Applied: "0 ≤ f ≤ 150". Pending: the δ bound ("≤ 3" → "≤ π") sits immediately after the lost glyph/object and must be edited by hand together with restoring the δ symbol.
- **Status:** PENDING (partially applied)
- **Why this status:** One bound is certain from the listing; the other is adjacent to an object (AD-27).

### C7-07 The gripper "equality constraints" are satisfied identically by construction
- **Location:** ¶5890–¶5891, ¶5893 (image), ¶5925–¶5926, ¶5937–¶5938, ¶5946–¶5947
- **Original:** `h1 = np.min(h1_values)`; `penalty8 = h1 if h1 > 10**-6 else 0`
- **Issue:** h1, h2 are the loop-closure equations from which α, β are computed, so they vanish identically unless `np.clip` has clamped an argument (then penalty10/11 fire too); `np.min` over z is the wrong aggregate for an equality that must hold at every z.
- **Evidence:** Monte Carlo over the box (seed 0, 20 000 draws): max residual 2.8·10⁻¹² on 5602 unclamped designs; printed feasible design h1 = h2 = 0.
- **Correction:** State that (7.12) holds by construction and keep penalty8/9 as a safeguard (then (7.13) is illustrative), or remove them; change `np.min` to `np.max` if kept.
- **Status:** PENDING
- **Why this status:** Formulation decision (AD-27).

### C7-08 Problem 5 ranks mix feasible and penalized medians; "PSO-based … especially well on Problem 4" is not what Table 7.2 shows
- **Location:** ¶5973; Table 7.1 ¶6418–¶6464; Table 7.2 ¶6512–¶6521
- **Original:** "PSO-based algorithms perform especially well on Problems 1 and 4"
- **Issue:** Every algorithm's Problem 5 maximum ≥ 6.57E5 (penalised runs; GWO/mGWO medians positive); on Problem 4 the median first group is "all algorithms except PSO, IA-PSO, mGWO".
- **Evidence:** Table 7.1/7.2 values.
- **Correction:** "The results vary by problem: PSO-based algorithms perform especially well on Problem 1; on Problem 4 all algorithms except PSO, IA-PSO, and mGWO reach the same median; DE/rand performs strongly on the median value for Problem 3, and SADE performs strongly on Problem 5. On Problem 5 a share of the runs of every algorithm terminated with an active penalty (see the maximum values in Table 7.1); for GWO and mGWO this was the majority of runs."
- **Status:** APPLIED
- **Why this status:** Restates what the printed tables show; adds the feasibility qualifier.

### C7-09 Wrong equation cross-references (five places)
- **Location:** ¶5724, ¶5895, ¶5953, ¶5959, ¶6696
- **Original:** "We will solve problem (7.1)"; "problem (7.8)-(7.12)"; "inequality constraints (7.10) and the equality constraints (7.11)"; "constraints (7.10) and (7.11)"; "minimizing the gearbox (7.14) while satisfying the constraints (7.14)"
- **Issue:** (7.1) is the kinematics, (7.2) the objective; (7.8) belongs to Problem 4; the gripper inequalities are (7.11), equalities (7.12); the gearbox objective is (7.15).
- **Evidence:** equation labels ¶5716, ¶5720, ¶5884, ¶5887, ¶6682, ¶6692.
- **Correction:** Applied: ¶5724 "(7.2)"; ¶5953 "(7.11) … (7.12)"; ¶5959 "(7.11) and (7.12)"; ¶6696 "minimizing function (7.15) while satisfying the constraints (7.14)". Pending: ¶5895 "(7.8)-(7.12)" → "(7.10a)–(7.12)" (the reviewer's "(7.10a)" label could not be confirmed from the extract).
- **Status:** APPLIED (4 of 5)
- **Why this status:** Targets confirmed by the equation-label paragraphs; the one unconfirmed label is left.

### C7-10 Three unparenthesized long expressions give a silently wrong result if wrapped
- **Location:** ¶5770 (164 chars), ¶5812 (90), ¶6713 (162)
- **Original:** `g2 = (18 * 10**4 * h) / (…) + (15 * 10**3 * b) / (…) - 6` etc.
- **Issue:** A break before `+`/`-` leaves a valid but truncated statement (for ¶5770 the "- 6" would be dropped).
- **Evidence:** `ast.parse` succeeds on all 29 blocks; hazard is at typesetting.
- **Correction:** Wrap the right-hand sides in outer parentheses and break over lines.
- **Status:** PENDING
- **Why this status:** Code lines.

### C7-11 Pressure-vessel thickness upper bound 1600 × 0.0625 in = 100 in; repo uses 99
- **Location:** ¶5797, ¶5819
- **Original:** "1x0.0625 ≤ Ts, Th ≤ 1600x0.0625"; `[[1, 1600], [1, 1600], [10, 200], [10, 240]]`
- **Issue:** Refs [3, 4] bound by 99 × 0.0625; the optimum is interior either way; example/notebook use [1, 99] and L ≤ 200.
- **Evidence:** `pressure_vessel_components([12, 6, 38.8601, 221.36553])` → 5850.3836 feasible (needs L > 200).
- **Correction:** `[1, 99]` and "99x0.0625", or keep 1600 and say why; align the repository examples to the manuscript (R-03).
- **Status:** PENDING
- **Why this status:** Search-box choice (AD-27).

### C7-12 Problem 2 narrative: objective described as deformation "caused by P and Q", but only P enters the objective
- **Location:** ¶5753, ¶5760
- **Original:** "This deformation is caused by the action of vertical force P and horizontal force Q."
- **Issue:** 5000/I is the deflection under P alone; Q enters g2; g1, g2 are never described.
- **Evidence:** ¶5770–¶5772.
- **Correction:** "The objective is the vertical deflection under the vertical force P; the horizontal force Q enters only the bending-stress constraint. The constraints limit the cross-sectional area to 300 cm² and the combined bending stress to 6 kN/cm²."
- **Status:** APPLIED
- **Why this status:** Describes the listing.

### C7-13 Gripper box admits a = 0, b = 0 and (e = 0, l = z), which divide by zero
- **Location:** ¶5957; ¶5910, ¶5913, ¶5923–¶5924
- **Original:** `RobotGripperDomain = [[0, 150], [0, 150], …]`; `value = (a**2 + g(z)**2 - b**2) / (2 * g(z) * a)`
- **Issue:** ±inf/nan with warnings at the box corners.
- **Evidence:** `gripper_components([0,50,200,20,30,100,2.])` → inf, 104 warnings.
- **Correction:** Raise the lower bounds (a, b ≥ 10, l ≥ 100 as in [6–8]) or guard the denominators.
- **Status:** PENDING
- **Why this status:** Code/bounds change (AD-27).

### C7-14 Exercise 3: constraint descriptions mis-assign g3–g6
- **Location:** ¶6689
- **Original:** "The constraints g1...g4 arise from … the transverse deflection of the shafts (g3), and the stress in the shafts (g4)."
- **Issue:** In the listing (¶6703–¶6706) and the Golinski benchmark g3, g4 are the deflections and g5, g6 the stresses.
- **Evidence:** ¶6701–¶6711 against the standard formulation.
- **Correction:** "The constraints g1...g6 arise from … the transverse deflection of the shafts (g3, g4), and the stress in the shafts (g5, g6); g7...g11 are dimensional and space limits."
- **Status:** APPLIED
- **Why this status:** Certain from the printed listing.

### C7-15 Units not stated for Problems 4 and 5; "proportional to" for the discrete thicknesses
- **Location:** ¶5797, ¶5833, ¶5837, ¶5869–¶5882
- **Original:** "The variables Ts, Th are proportional to 0.0625 inches"; no units for As, b, h, cost; none for Problem 5.
- **Issue:** Ts, Th are integer multiples; Problem 4 is in in², in, USD; Problem 5 constants z_max = 25, Y_min = 70, Y_max = 150 appear only in code.
- **Evidence:** text; listing ¶5899–¶5900.
- **Correction:** Applied: "integer multiples of 0.0625 inches". Pending: units sentence for ¶5837 and the Problem 5 constants in ¶5882.
- **Status:** PENDING (partially applied)
- **Why this status:** Units come from the cited sources, which the authors should confirm (AD-27).

### C7-16 Printed "feasible" gripper design sits on a dead-point configuration; y(0) unbounded above
- **Location:** ¶5959; ¶5932–¶5933
- **Original:** "… returns -26.603621311081888"
- **Issue:** Value reproduces, but links a and b are collinear at one z and y(0) = 668.7; the standard formulation also bounds y(0) above (Y_G).
- **Evidence:** components at the printed point: g2 = 0.000997, g8 = 1.000000, g6 = 518.7.
- **Correction:** Confirm (7.11) intentionally has no upper limit on y(x, 0) or add Y_G and re-run.
- **Status:** PENDING
- **Why this status:** Formulation question (AD-27).

### C7-17 Problem 1 passes `list(range(5))` as the variable list
- **Location:** ¶5749
- **Original:** `PSO(ObjectiveFunction5, list(range(5)), Domain5Vars, SwarmPopulation, IterationNumber)`
- **Issue:** Works, but inconsistent with every other call.
- **Evidence:** `n = len(Vars)` in the PSO listings.
- **Correction:** `Vars5 = [f"alpha{i}" for i in range(1, 6)]`.
- **Status:** PENDING
- **Why this status:** Code.

### C7-18 Summary's iteration guidance contradicts the chapter's own settings
- **Location:** ¶6576 vs ¶5968
- **Original:** "If the problem is not complex, it is recommended to set the number of iterations I<100."
- **Issue:** No problem used fewer than 100 iterations.
- **Evidence:** text (medium).
- **Correction:** "… I ≈ 100 was sufficient for Problems 2 and 4; Problems 1 and 5 needed 200–500" or delete.
- **Status:** PENDING
- **Why this status:** Author's recommendation (AD-26).

### C7-19 Exercise 1: tolerance test uses `>=` where the chapter uses `>`; superscripts lost
- **Location:** ¶6601, ¶6609, ¶6628, ¶6638 vs ¶5946–¶5947
- **Original:** `penalty_output = abs(h) if abs(h) >= delta else 0` vs `h1 if h1 > 10**-6 else 0`; "Δ=10-10"
- **Issue:** Immaterial numerically (all four printed outputs reproduce); superscripts flattened in the extract.
- **Evidence:** `Penalty1([0.1,0.1,-0.5])` → 730000.0 etc.
- **Correction:** Same comparison in both places; verify superscripts in the typeset copy.
- **Status:** PENDING
- **Why this status:** Code; superscripts to the copyedit/visual check.

### C7-20 Footnote: box plots "not possible" when the minimum is zero
- **Location:** ¶5991
- **Original:** "Thus constructing Box-and-Whisker charts is not possible;"
- **Issue:** What is impossible is the logarithmic axis, not the plot.
- **Evidence:** reasoning.
- **Correction:** "Thus the logarithmic Box-and-Whisker charts used elsewhere cannot be drawn for these cases;"
- **Status:** APPLIED
- **Why this status:** Certain.

---

## Open author decisions

| ID | Question | Evidence in hand | If yes | If no |
| --- | --- | --- | --- | --- |
| AD-01 | Replace the legacy `np.random` stream by `default_rng` and drop `clear_output` in all listings (errata 4, 5; XC-01, XC-02)? | Repository already does both; `docs/manuscript-replacements.md` items 3, 5 | All chapter listings and Appendix B change; Appendix C/E become explicitly historical (C5-19 paragraph already says so) | Keep the listings; the applied notes (¶363, ¶460, ¶1376, ¶1964) stand |
| AD-02 | Replace single-run judgements (¶492, ¶572, ¶698, ¶966, ¶1511, ¶1987, ¶2072) by a small multi-seed table, and delete "in many cases"/"one of the most refined" in ¶966? | 20-seed and 30-seed medians in the Chapter 1/3 reviews | New table(s) and rewritten sentences; XC-03 qualifiers can then go | Qualifiers stay as applied |
| AD-03 | IA-PSO: make the perturbation translation-invariant (`Position + Velocity*(1-rho)`) and re-run Figure 1.11 (C1-01)? | Shift test: IA-PSO median 8.99 vs PSO 9.7e-07 on (1.13) shifted by 10 | Listing, repository `ia_pso.py`, Figure 1.11 and ¶572 value change | Applied ¶509/¶572 wording stands; algorithm stays as cited from [9] |
| AD-04 | von Neumann neighbourhood: include the particle itself (Chapter 1) or not (Appendix B, repository, Chapter 5 benchmark) (C1-03)? | Medians 6.8e-05 vs 2.9e-04 over 20 seeds | Chapter 1 listing changes if Appendix B wins; Appendix B, repository and possibly Appendix C change if Chapter 1 wins | — |
| AD-05 | VCT-PSO: is the swap of the cognitive attractor meant to be temporary (as coded) or a permanent overwrite of PBest (C1-05)? | Listing and `vct_pso.py` are temporary | Listing and repository change; ¶636/¶640 revert | Applied wording stands |
| AD-06 | Exercises that ask for conclusions from single runs (Ch1 Ex 5, Ch3 Ex 4, Ch2 Ex 4): add "repeat ≥10 times, compare medians" and fix the log-scale/`Vars` issues (C1-12, C3-16)? | `checks.py` section G: seed spread −2.5…26.75 exceeds the K/I effect | Exercise text and one code line change | Exercises stay |
| AD-07 | Figure 1.6: what D, box and seeds were used for the Griewank curves (C1-18)? | None in the manuscript | Caption gains D, box, "three independent runs" | Figure stays unreproducible |
| AD-08 | Sources: (0.72, 1.19, 1.19) in ¶259 (C1-19); PSO advantages ¶466 (C1-29); DE parameter ranges and CR = 0.3 attributed to [2] (C2-26) | Reviewer reasoning only | Citations added or wording softened | — |
| AD-09 | Table 2.1: print DE/rand/1 (matching 2.1 and the flowchart) or keep DE/best/1 and say so in ¶1304/¶1305 and the caption (C2-01)? | ¶1332 `i1 = BestDotNumber`; Appendix B has both | Listing/explanation cells change; 2.4.1 derivation reordered | Two prose sentences and the caption change |
| AD-10 | SADE: implement the jDE rule of [5] or add the "unlike [5]" sentence after ¶1521 and consider renaming (C2-03)? | `sade.py` docstring; Brest et al. 2006 | Listing, Appendix B, repository and Appendix C column change | One sentence added |
| AD-11 | DE/rand-to-best/1: does Table 2.2 state the standard x_r1 + F(x_best − x_r1) form? Then fix ¶1483–¶1487 (C2-10) | Listing uses (x_best − x_k) | Listing and Figure 2.6 panel change | Add a sentence to ¶1406 |
| AD-12 | One spelling for EPD-GWO / GWOEPD / GWO-EPD across chapters, tables and code (C3-18) | Four spellings in use | Chapter 3 prose, Chapter 5/7 tables and code map change | — |
| AD-13 | Table 4.1/4.2 items that depend on the formula images or a convention: Powell (C4-09, applied — reject if the image differs), Deb 1 (C4-15), Quartic noisy/unimodal (C4-19), Rosenbrock at D=30 (C4-20), Schwefel 2.4 separability (C4-21), Xin-She Yang continuity (C4-22), Xin-She Yang No. 1 description (C4-31) | Appendix B code and reviewer computations | Flags/descriptions change as proposed | Current cells stay |
| AD-14 | Chapter 4 Exercise 2: 20 runs (task text) or 100 runs (code) (C4-27, C5-20)? | Timing cell uses 20; 100 runs ≈ the full experiment at D=10 | Code cell ¶3244 → `Runs = 20` plus a run-time warning | ¶3239 → "Runs=100" plus a strong run-time warning |
| AD-15 | Was Appendix E produced with 20 runs (code) or 100 (old header)? (C5-01, C5-02 applied on the code's value) | ¶8061 `Runs = 20`; ¶8196 writes "mean of {Runs} runs" | Applied text stands | Revert ¶3764/¶12206 records and change ¶8061 instead |
| AD-16 | Supply OS, Python, NumPy, joblib versions and core count for the Appendix C/E machine; confirm both experiments ran on the same PC (C5-05) | None in the manuscript | ¶3766 gains the environment sentence | Only the unit fix stands |
| AD-17 | Confirm the median-CI formula image reads Me ± 1.57·IQR/√n and add the matplotlib sentence (C5-10) | Appendix D ¶12128–¶12137 | One sentence added | — |
| AD-18 | Chapter 5 recommendations: qualify "GWO ≈ mGWO" (C5-11), state the tier criterion (C5-12), define "efficiency" (C5-18) | Recomputed medians, rank sums and Σ times | ¶3770/¶3776/¶3261 change | Applied qualifiers (C5-09, C5-13, C5-17) stand |
| AD-19 | Reprint Table E.1 with three decimals (`round(..., 3)`) (C5-14)? | 122 of 756 cells ≤ 0.05 s | Needs `raw_timing_results.npz`, which the repository does not have | Two-decimal table stays; applied "(2–4 times)" wording stands |
| AD-20 | Cart-pole Problem 5: swing-up prose vs swing-down listing (C6-01); any-time vs final-state test (C6-06); Euler-map limitation sentence (C6-07); Furuta (6.47) convention vs docstring (C6-09); check (6.22) for the M/m roles (C6-02 applied) | `cart_pole.step` free-motion tests; `simulate(WORKED_FEASIBLE)` | Option (b): listing sign change and recompute ¶4565, Table 6.2 row 5, Tables 6.3/6.4, Figures 6.12/6.23/6.24g | Option (a): rewrite ¶4056, Figure 6.11 caption and the Problem 5 title |
| AD-21 | Exercise 3 (crane): add a tolerance to the penalty or rewrite ¶5409 as proportional; mention W and dry friction (C6-08) | `ObjectiveFunction(0.8,1.2,0.6)` = 2.096e8 | Code line changes | ¶5409 and ¶5408 change |
| AD-22 | Confirm equation numbers in ¶4454 ((6.41a)/(6.42a), (6.20a)/(6.43)), hand-edit the two figure references next to equation objects (¶4284, ¶4294), and whether (6.19)/(6.24)/(6.25) carry |a| ≤ 1, |F| ≤ 5 N, |x| ≤ 0.7 m, √∫F²dt (C6-10 items 8–10, C6-11) | Captions and listing comments | Three references and the bounds sentences change | — |
| AD-23 | Chapter 6 claims: tier rule and ME-D-PSO placement (C6-12); Problem 1b analytic minimum −0.3 (C6-14); "90 is the global minimum" (C6-24); limitations paragraph (C6-25) | Table 6.4 sums; SymPy coefficients; Table 6.2 | New sentences/paragraph | — |
| AD-24 | Table 6.1 merged cells and seeds (C6-18); Table 6.3 missing cells (C6-19); which file/code produced Figure 6.24 (C6-20) | Table 6.2 values for the missing cells | Cells filled; seed sentence; ¶4606 sentence | — |
| AD-25 | I-beam: fix `tw`→`tf` in g1/g2 and re-run Problem 2, or keep and state non-comparability (C7-02); replace L = 5200 cm, E = 5.23·10⁶ by the data consistent with the listing (C7-03) | SLSQP optima 0.006626 vs 0.013074; constants 5000/180000/15000 | Table 7.1/7.2/7.3, Figure 7.6d, worked value change | One sentence; prose constants corrected |
| AD-26 | Chapter 7 summary: which algorithms are "recommended" (C7-04); Problem 4 iterations 100 or 200 (C7-05); "I<100" guidance (C7-18) | Table 7.3 sums | ¶6577, ¶5968 or ¶5862, ¶6576 change | — |
| AD-27 | Gripper and vessel formulation: δ bound (C7-06), equality constraints by construction and `np.min`→`np.max` (C7-07), lower bounds that divide by zero (C7-13), units and constants (C7-15), Y_G bound (C7-16), vessel thickness bound 99 vs 1600 (C7-11) | Monte Carlo residuals; component evaluations | Listings and possibly Problem 3/5 results change | Prose notes only |

## Repository follow-ups

- **R-01** `docs/experiment-protocol.md`: "Chapter 6 prose" → "Section 5.2 (Chapter 5)" for the 20-runs sentence (C5-22).
- **R-02** `docs/errata.md` item 1: second location is Practical Exercise 1 (¶5272), not the Problem 1a solving section (C6-15); add an erratum entry for the Exercise 2 per-component dRAND so the `book-code-map.md` tag T072 has a target (C2-02).
- **R-03** `examples/pressure_vessel.py`, `notebooks/10_engineering_design.ipynb`: align bounds with the manuscript (`[1,1600]`/`[10,240]` or whatever AD-27 decides) (C7-11); `examples/robot_gripper.py` docstring and line-15 comment are stale — the manuscript prints both bounds and a worked value (C7-06).
- **R-04** `scripts/compare_published_values.py` / `results/published_comparison.json`: add the Chapter 7 worked scalars (with the corrected Problem 4 values 37500373.8 and 381.96) and the Chapter 1 printed-vector value 7.662417638614574e-07; optionally add the third Quintic root to `tests/test_benchmarks.py` and Cosine Mixture −0.1·D to `results/reference_minima.csv` (C4-10, C4-11, C7-01).
- **R-05** Appendix B / Chapter 4 Exercise 1: `%pip install plotly` (C4-25) and the `Z = FunctionToShow(X1, X2)` fix (C4-26) when the code pass runs.
- **R-06** Add the ranking snippet (`DataFrame.rank(method="dense")` for Chapter 5; `scipy.stats.rankdata(method="min")` for Chapters 6–7) to Appendix B or D so Tables 5.1/5.2, 6.4 and 7.3 can be regenerated (C5-08, C6-13).
- **R-07** `docs/methodology.md`, `docs/experiment-protocol.md`: note that the manuscript EPD-GWO listing re-evaluates the whole pack (9975 evaluations for K=25, I=200), while `gwoepd.py` re-evaluates only the replaced half (7388) (C3-01).
- **R-08** `docs/book-code-map.md` rows T181–T190: mark verified per the Chapter 7 review (T185 worked values: mismatch, now corrected in the manuscript).
- **R-09** Code-side errata already in the library (ME-D-PSO history guard, IA-PSO scale guard, SADE indentation, von Neumann square check) stay as documented; the manuscript listings are updated only when AD-01 is decided.
