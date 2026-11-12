# Editorial style guide

Date: 2026-10-27. Applies to the manuscript copyedit on branch `editorial/manuscript-edit-2026-10-27` and to later passes. Where this guide and an author's scientific intent conflict, the intent wins and the question goes to `chapter-review.md`.

## Language

- American English spelling and punctuation: *optimization, minimize, behavior, color, modeling, analyze, center*. Serial comma. Double quotation marks. Periods and commas inside quotation marks.
- Register: professional technical prose. Present tense for what the algorithm or code does ("the velocity update adds…"). Second person only in instructions ("Run the script…"). No conversational filler ("it is worth mentioning", "as we can clearly see", "obviously", "in today's rapidly evolving world") and no marketing adjectives in chapters.
- Sentence length: split chained sentences joined by "which", "that is", "and also". One idea per sentence where the original stacks three.
- Translation artifacts to remove: definite articles before code names ("the matrix Position" → "the `Position` matrix" or "the position matrix `Position`"); "the given" for "this"; "it is necessary to" for "must"; "allows to" for "lets/allows one to"; "in the frame of" for "within"; "carried out" for "run/performed"; "obtained results" for "results".
- Numbers: numerals for all quantities with units and for counts ≥ 10; words for one to nine without units. Thousands separator in prose numbers (12,345) except in code and in tables that copy program output. Decimal point. Units with a space (`0.5 s`, `2 m/s`), degrees without. Ranges with an en dash (1–5). Negative numbers with a true minus in prose is not required; keep the hyphen-minus the source uses.
- Hyphenation: *objective-function value*, *population-based*, *real-valued*, *n-dimensional*, *decision-variable vector*; no hyphen after -ly adverbs.

## Terminology (use the left column; do not mix)

| Use | Instead of | Note |
| --- | --- | --- |
| objective function | cost function, fitness function, criterion function | *fitness* is reserved for evolutionary wording in Chapter 2 where the authors define it; "objective-function value" otherwise |
| objective-function value | fitness, cost, criterion value | |
| candidate solution | solution, point, individual, agent (generic) | the algorithm-specific noun is still used: *particle* (PSO), *vector*/*individual* (DE), *wolf*/*search agent* (GWO) |
| population | swarm (generic), pack (generic), set of agents | *swarm* in PSO and *pack* in GWO are kept when the text speaks about that algorithm |
| population size | swarm size, number of agents, number of particles (when generic) | symbol as the chapter defines it |
| search space | feasible region (when meaning the box), domain | *feasible region* only when constraints are meant |
| decision variable, decision-variable vector | design variable (Chapter 7 may keep *design variable*), optimization variable, argument | |
| exploration / exploitation | diversification / intensification, global/local search (as synonyms) | |
| convergence | stagnation (not a synonym), reaching the optimum | *premature convergence* and *stagnation* are distinct and both are kept |
| iteration | epoch (except ME-D-PSO's defined *epoch*), generation (DE may keep *generation* when the authors define it), step | |
| function evaluation, evaluation budget | number of calls, computations | |
| global optimum / local optimum | global/local extremum, minimum (when the sign is not meant) | |
| lower bound, upper bound; bounds | limits, borders, range (when meaning the box) | `lb`, `ub` in code |
| personal best, global best | pbest/gbest in prose | code names `PBest`, `GBest` unchanged |
| inertia weight, cognitive coefficient, social coefficient | inertia coefficient, cognitive/social factor | `w`, `c1`, `c2` |
| mutation factor `F`, crossover rate `CR` | scaling factor, crossover probability | DE |
| benchmark function | test function, benchmark | *benchmark* alone for the experiment |
| run (an independent run) | launch, experiment (when meaning one run) | |
| random seed, random-number generator | random state (except the NumPy class name) | |
| listing | code fragment, program, script (when meaning a printed listing) | |

Algorithm names: PSO, DE, GWO; variants as the chapters define them (LDW-PSO, IA-PSO, BB-PSO, VCT-PSO, ME-D-PSO, Ring-PSO, von Neumann PSO, DE/rand/1/bin, DE/best/1/bin, SADE, mGWO, GWOEPD). Spell out on first use in each chapter.

## Code and mathematics in prose

- Code identifiers in prose are set in the code font (Word style `Code Char` if present, otherwise Consolas) exactly as in the listing: `Position`, `np.random.default_rng`. Do not pluralize or inflect identifiers.
- Python, NumPy, SciPy, Jupyter, Matplotlib capitalised as the projects do. "Python 3.12" everywhere a version is given.
- Mathematical symbols in prose are italic single letters as the equations use them; vectors bold if the equation images use bold (they mostly do not — keep the chapter's convention). Define every symbol on first use in each chapter. Index conventions: *i* for the candidate, *j* for the coordinate, *t* for the iteration, *D* for the dimension, *N* for the population size, unless the chapter defines otherwise — do not retrofit the images.
- Equations are images and are not touched. Equation references stay as typed ("(1.3)").
- Code listings are not edited for style. Explanation cells next to a code line explain what the line does and why; they do not restate it.

## Structure conventions

- Headings: Chapter N title in title case; sections numbered N.M; subsections N.M.K. Word styles Heading 1/2/3.
- Chapter end matter in this order: Chapter Summary, Review Questions, Exercises, References.
- Captions: "Figure N.M – …" and "Table N.M – …" as the source uses (en dash); sentence case; end without a period unless the caption is a sentence.
- Callouts (follow-up passes): Key Concept, Implementation Note, Numerical Pitfall, Engineering Insight, Reproducibility Note. Not used in this pass.

## Tracked-change discipline

- Author name on every revision: `Editorial (Claude)`.
- One paragraph per edit record; the tool diffs at word level so accepted/rejected changes stay readable.
- Never edit a code cell, a number, a symbol, a citation key or a caption number in a copyedit record; such changes go through `scientific-corrections.md` with evidence.
