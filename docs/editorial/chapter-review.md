# Chapter review

Phase: Chapter-by-chapter editing. Date: 2026-10-27. Source: `manuscript/Metaheuristic_Optimization_with_Python_source_2026-10-25.docx`; output: `Metaheuristic_Optimization_with_Python_Edited_2026-10-27.docx` (tracked changes, author `Editorial (Claude)`) and its accepted copy. Counts in the table are the records applied by `scripts/editorial/apply_tracked_edits.py`; each record is one paragraph.

For every chapter the pass was: technical review against the companion code (findings in `scientific-corrections.md`), copyedit of prose, captions, explanation cells, summaries, review questions and exercises under `style-guide.md`, a verification read of the edit records (`scripts/editorial/check_edits.py` plus a sampled manual read), then application as tracked changes. Code listings, numeric table cells, reference lists and equation images were not edited; the only code-adjacent changes are the explanation cells next to listings.

## Counts

| Section | Copyedit records | Scientific corrections | Both (merged) | Structure (headings, TOC) | Tracked segments |
| --- | ---: | ---: | ---: | ---: | ---: |
| Front matter | 14 | 5 | 0 | 3 | 150 |
| Chapter 1 | 156 | 6 | 16 | 10 | 2081 |
| Chapter 2 | 100 | 7 | 8 | 16 | 1303 |
| Chapter 3 | 91 | 12 | 5 | 15 | 996 |
| Chapter 4 | 83 | 28 | 5 | 6 | 935 |
| Chapter 5 | 42 | 8 | 5 | 11 | 598 |
| Chapter 6 | 172 | 8 | 9 | 15 | 1736 |
| Chapter 7 | 74 | 6 | 5 | 12 | 750 |
| Appendix B | 0 | 0 | 0 | 1 | 1 |
| Appendix C | 0 | 1 | 0 | 1 | 3 |
| Appendix D | 0 | 0 | 0 | 1 | 1 |
| Appendix E | 0 | 1 | 0 | 1 | 6 |
| Glossary | 50 | 0 | 0 | 1 | 340 |
| Back-of-book TOC | 0 | 0 | 0 | 1 | 488 |
| **Total** | **782** | **82** | **53** | **94** | **9388** |

Application run (`manuscript_extract/edits/merged.jsonl`): 1,017 records applied, 0 rejected, 9,395 tracked segments; the docx validator passes on the redlined file (XSD, and no text changed outside a revision by `Editorial (Claude)`) and on the accepted copy. Paragraph count 13,380 → 13,385 in the redline (two introduction insertions, the `Contents` heading, the TOC field, the Chapter 5 reproduction-status paragraph) and 13,102 after acceptance (the 111 rows of the stale back-of-book TOC and the empty paragraphs around it removed, 7 chapter titles joined).

Overlaps: 135 scientific-correction records and 826 copyedit records targeted 86 common paragraphs. `scripts/editorial/merge_edits.py` combined 53 of them (the correction's token changes re-applied onto the copyedited text, or the reverse); for the remaining 40 the scientific correction alone was applied and the copyedit polish of that paragraph was dropped — they are listed in `manuscript_extract/edits/unresolved.md` (not committed; regenerate with the merge command in `publication-readiness.md`). `scripts/verify_book_code.py` parses 75 one-column listings in the source and in the accepted copy alike; the one unparsed block is the `%pip` Jupyter magic cell in Appendix B, as before.

## Front matter

- Edited: back-cover text, reproducibility notes, companion-code paragraphs, reader prerequisites, introduction (12 paragraphs); two short paragraphs inserted in the introduction: how the book is organised (chapters and appendices) and what the book does not cover (gradient-based, multi-objective and combinatorial optimization; constraints only through the penalty reductions of Chapters 6–7; no Python/NumPy introduction).
- Applied from the brief: approved subtitle (¶19), full author names on the title page (¶0–¶2; the copyright line is untouched because shares are undecided), "Install Python 3.12" (¶58).
- Structure: `Reader Prerequisites` and `Introduction` given Heading 1; a `Contents` heading and a TOC field inserted after the copyright page (refresh in Word: right-click → Update Field); the hand-typed table of contents at the back of the book, which used the old chapter titles, deleted.
- Author questions: ¶70 ends with a hyperlink run ("Corrections / errata") glued to the paragraph; it should be its own line like ¶68–¶69 — a layout fix in Word, not a text edit. ¶65 and ¶109 still refer to `/blob/main/` links; they change when a release is tagged.

## Chapter 1. Particle Swarm Optimization (PSO)

- Copyedit: translation scaffolding ("let us", "it is necessary to", "makes it possible to") removed in about 45 paragraphs; all 24 explanation cells of Table 1.2 rewritten to explain rather than restate, with the equation numbers (1.2)–(1.12) tied to the lines; nine-line sentences in the BB-PSO and ME-D-PSO sections split; captions trimmed ("Plot of the decrease of …" → "Decrease of …"); terminology unified on *inertia weight* `w`, *cognitive/social coefficient*, *canonical PSO*, *search space*/*bounds*.
- Terminology decisions: the three velocity-update terms are "inertia / cognitive / social factor" (the chapter's majority usage and the wording of its review questions), distinct from the inertia weight. `vonNeumann-PSO` is kept as the chapter's algorithm name because the function is `vonNeumannPSO`; prose elsewhere uses "von Neumann PSO" — a global decision for the authors (see Chapter 5 and 6 notes).
- Scientific items applied as tracked changes (see `scientific-corrections.md`): Clerc–Kennedy inertia value, wrong equation cross-reference for the ME-D-PSO stagnation condition, prose descriptions aligned with the printed listings (IA-PSO, VCT-PSO, ME-D-PSO, boundary rule), the von Neumann square-population restriction, single-run qualifiers.
- Pending for the authors: the IA-PSO headline result (5.99e-16) depends on the optimum lying at the origin; Chapter 1 and Appendix B implement different von Neumann neighbourhoods (with/without the particle itself); Exercise 5's objective is not bounded below by zero, so the log-scale plot does not apply.

## Chapter 2. The Differential Evolution Method (DE)

- Copyedit: "differential weight" → *mutation factor* `F`, "crossover probability" → *crossover rate* `CR`; figure panels referenced as "Figure 2.6a"; en-dash ranges; guillemets replaced; code lead-ins rewritten so sentences split across code blocks read as one; explanation cells of Table 2.1 explain the DE/best/1 base vector, `j_rand` and the greedy replacement; captions in sentence case.
- Terminology decision needing confirmation: "binomial crossover" for `z = bin` (standard DE term; the source said "binary operation").
- Scientific items applied: wrong figure/table cross-references (Figure 2.4 → 2.3, Table 2.1 → 2.2), the evaluation-budget note for Table 2.1, minimum population per mutation scheme, single-run qualifier.
- Pending for the authors: Sections 2.1/2.3 describe DE/rand/1 but Table 2.1 implements DE/best/1; "SADE" is a simplified jDE and the name collides with Qin–Suganthan's SaDE; Exercise 2 redraws the random index per component; DE/current-to-best/1 derivation starts from the DE/best/2 block; Exercise 4 names no objective function; the unindented SADE fragment (code, not edited here).

## Chapter 3. The Grey Wolf Optimizer (GWO)

- Copyedit: 32 Table 3.1 explanation/header cells rewritten (including the garbled cell ¶1885); "Figure3.x" spacing; ranges; captions normalised to the Chapter 1 pattern; a 180-word paragraph tightened; duplicate definition of the mean removed; "wolf"/"pack" used when the text speaks about GWO, "population" kept for generic statements; zero-based indexing of the code stated where prose counts from 1.
- Meaning-level alignments made in the copyedit and logged in `scientific-corrections.md`: the update is the mean of three leader-derived positions (not "the average position of the leaders"); the worked example calls `ObjectiveFunction` from Chapter 1 with `DomainVarsList`; "two modifications", not "several"; `** 2` rather than "^2".
- Pending for the authors: EPD-GWO is compared with GWO/mGWO on roughly twice the evaluation budget; the EPD replacement offset spans the whole box, not a neighbourhood; mGWO superiority rests on one run; Table 3.1 lacks the `lb`/`ub` lines and its code column does not parse as extracted; Exercise 2 needs steps 1–5 of Exercise 1.

## Chapter 4. Benchmarks

- Copyedit: all 54 Section 4.2 descriptions put in one pattern ("Name. One or two sentences."); garbled sentences repaired; "relief" → *landscape*, "admissible region" → *search space*, "extrema" → *local optima*; Section 4.3 cell names and parameters in parentheses; summary de-duplicated; BB-PSO spelling.
- Scientific items applied as tracked changes to Table 4.1/4.2 cells (each with its test or computed value): Whitley location/value, Perm 0 location, rotated hyper-ellipsoid lower bound, Xin-She Yang noise wording, Griewank separability, Powell differentiability, Happy Cat differentiability, Periodic and Stretched V modality, Trid location/value, Cosine Mixture minimum, Quintic third root; Section 4.2 descriptions corrected where the formula is unambiguous (Quintic, Styblinski–Tang, Qing, Deb 1, Xin-She Yang); Exercise 2 run count; Exercise 1 undefined `function` noted.
- Pending for the authors: Rosenbrock unimodality in D = 30, Schwefel 2.4 separability, Xin-She Yang 2/4 continuity flags, Quartic description vs table, the Section 4.3 prose names (`run_once`/`Results` vs the code's `run_once_perf`/`PerfResults`).

## Chapter 5. Analysis of Algorithm Efficiency on Benchmarks

- Copyedit: numerals per the style guide; "bounds"/"population size"/"benchmark function"; comma splices and missing colons before code; hardware sentence made grammatical with units (GHz, GB); "Fig." → "Figure"; no superiority claim strengthened.
- Scientific items applied: run-count contradiction for the timing experiment (20 runs in the code; the sentence now says so), the protocol sentence (per-run seeds derived from 12345), the reproduction-status paragraph after ¶3311 pointing at `docs/experiment-protocol.md` and `results/reduced_comparison_summary.json`, the ranking rule (competition ranking on the printed three-significant-digit values), wall-clock time and hardware, Appendix C/E captions.
- Pending for the authors: ¶3310 says ranks come from `raw_benchmark_results.npz` but they reproduce only from the printed values; "difference practically disappears" overstates an 8–13 % gap; GWO/mGWO "similar" holds for rank sums but not medians; "efficiency" is never defined; the notch overlap is presented as a statistical test.

## Chapter 6. Control Problems

- Copyedit (6.1–6.2): "let us" imperatives made declarative; wordiness ("makes it possible to obtain", "must be executed"); faulty parallelism in the condition lists; "Figure6.x" spacing and "Fig." → "Figure"; symbol lists after "where" punctuated consistently; SymPy, "acceleration due to gravity". Three prose paragraphs carry the code style (`MathematicaCellInput`: ¶4001, ¶4009, ¶4024) and were left unedited; the style swap is listed in `scientific-corrections.md` (C6-21).
- Copyedit (6.3, summary, questions, exercises): translation artifacts ("connect the spline package"), chained results paragraph split, dangling modifiers, "von Neumann PSO" in prose, caption wording, exercise step wording unified; thousands separators in prose values (`m1=20,000 kg`) — reject if code-style digits are preferred.
- Scientific items applied: Exercise 1 plant made explicit (1/(1+s)^3, settling-time criterion, not Problem 1a's ITAE); thirteen off-by-one figure/table/equation cross-references; crane roundoff sentence; Table 6.3 missing third-rank cells; ranking rule; conditional-expression wrap note; mass-parameter roles in the cart-pole listing described as printed.
- Pending for the authors (meaning): the printed cart-pole step has gravity signed so that φ = 0 is the hanging position — the listing solves a swing-down, the reverse of ¶4056 and Figure 6.11 (the Furuta listing in Exercise 4 uses the correct convention); the tolerance vector called "components of XT"; the "large penalty" ObjectiveFunction1b does not have; Problem 5's `reached` is an any-step test and the printed feasible vector ends outside the box; ME-D-PSO omitted from the tiers despite equal rank sums; Problem 4a "90 is the global minimum" unverified; the `subprocess pip install` setup cell and the Cyrillic comment in ¶4238.

## Chapter 7. Optimal Design Problems

- Copyedit: register ("We begin with a problem from robotics"), passive lead-ins to code, filler, dangling dashes, "bounds"; "von Neumann PSO"; 500 and 25 as numerals.
- Scientific items applied: Problem 4 worked values (37500373.8 and 381.96, from the printed listing); gripper bounds in prose aligned with the code (f ≤ 150, δ ≤ π); Problem 4 iteration count; five equation cross-references; g3–g6 roles in Exercise 3; (7.15) for the gearbox mass.
- Pending for the authors: the I-beam listing uses `2*b*tw` where the physical formulation needs `tf` (results then differ from the cited literature); Problem 2 prose constants (L, E) inconsistent with the listing; the chapter summary recommends GWO and GWOEPD although Table 7.3 ranks them 11th/13th; Problem 5 ranks mix penalised and feasible medians; gripper equality penalties are identically zero by construction.

## Glossary

- 50 definitions edited for one- or two-sentence precision and style-guide terminology (candidate solution, decision variables, inertia weight / cognitive and social coefficients); term names unchanged.

## Structure and navigation

- Heading 1 on the seven chapter titles (now "Chapter N. Title" on one line, title case), the appendices, the glossary and the two front-matter sections; Heading 2 on every N.M section and on Chapter Summary / Review Questions / References; Heading 3 on every N.M.K subsection and every Exercise heading that is its own paragraph (Chapter 3's "Exercise 4" sits inside the previous paragraph after a line break and keeps that form).
- All formatting changes are tracked (`w:pPrChange`), so a reviewer can reject them paragraph by paragraph.

## Not done in this pass

A–M chapter architecture, new intros and practical-considerations subsections, exercise levelling, figure regeneration, editable equations, EPUB/KDP layout: see `book-improvement-plan.md`.
