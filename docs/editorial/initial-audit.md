# Initial editorial audit

> Editorial tooling note: the scripts named in this report (`scripts/editorial/…`, `tests/test_editorial_tools.py`) and the edit records are the editor's working tools. They are kept on the fork branch `dtkachenko:editorial/manuscript-edit-2026-10-27` and are not part of this pull request; the manuscript binaries are never committed.

Phase: Discovery. Date: 2026-10-27. Branch `editorial/manuscript-edit-2026-10-27` on the fork `dtkachenko/Metaheuristic-Optimization-with-Python`, started from upstream `main` at `a3725fe`.

Scope agreed for this pass: professional copyedit of the whole manuscript delivered as Word tracked changes, a traceable technical-correction log, the `docs/editorial/` reports, and alignment of the book and repository on Python 3.12. Chapter restructuring, new figures, editable equations and e-book layout are recorded in `book-improvement-plan.md` as follow-ups and are not done here.

## Authoritative manuscript

| File | Bytes | SHA-256 | Core dates | Role |
| --- | --- | --- | --- | --- |
| `~/Downloads/Metaheuristic_Optimization_with_Python_Copyedited.docx` | 29914925 | `67c4bbf4b2c9b4a92da114db4c292899d3c346d865081edcb9342b22ebce4014` | created 2026-09-18, modified 2026-10-25 23:36 | **source for this pass**; copied to `manuscript/Metaheuristic_Optimization_with_Python_source_2026-10-25.docx` (gitignored) |
| `~/Downloads/…_Editorial_Edition.docx` (2026-10-15) | 29201623 | `d34a1841…` | — | review source of the 2026-10-20 audit; no longer present in `~/Downloads` |
| `~/Downloads/Telegram Lite/HANDBOOK_Python.docx` | 29779307 | `d9a0770e…` | — | not present on this machine today |
| `~/Documents/HANDBOOK.docx` (2026-08-05) | 27975659 | `07c7517f…` | — | not present on this machine today |

Provenance of the 2026-10-25 file, from its text: it carries the three-author title page and copyright line, the AI-translation disclosure, "Independently published", the `Companion Code and Reproducibility` block with eight `/blob/main/` repository links, and a `Reader Prerequisites` section. Those are the additions `scripts/prepare_reviewed_manuscript.py` makes, plus further front-matter work. It is therefore downstream of the 2026-10-20 review copy and is the newest edition on this machine. It was not overwritten; every edit in this pass goes to a new file.

What it does **not** carry: the four Table 4.1 cell corrections the review script applies. Checked on 2026-10-27 in the extracted text: Whitley location `0` / value `1` (¶2703, ¶2704), Perm 0 location `i-1` (¶2533), rotated hyper-ellipsoid lower bound `-65.53` (¶2575), Xin-She Yang noise "normaly distributed on the range [0, 1]" (¶2707). These go into `scientific-corrections.md` and are applied as tracked changes so the authors can accept them.

## Structure inventory

Extraction: `python scripts/editorial/extract_paragraphs.py manuscript_extract/unpacked/word/document.xml --out manuscript_extract` on the run-merged `document.xml` (1399 runs merged with the docx skill's `merge_runs.py`). 13,380 paragraphs.

| Section | Paragraphs | Table cells | Code paragraphs (`MathematicaCellInput`) | Objects (equation/figure) | Prose words |
| --- | ---: | ---: | ---: | ---: | ---: |
| Front matter (title, copyright, reproducibility notes, companion code, prerequisites, introduction) | 156 | 0 | 0 | 2 | 1,131 |
| Chapter 1. PSO (1.1–1.5, summary, review questions, 5 exercises, references) | 1,078 | 615 | 0 | 54 | 7,820 |
| Chapter 2. DE (2.1–2.4, summary, review questions, 4 exercises, references) | 494 | 201 | 0 | 25 | 4,442 |
| Chapter 3. GWO (3.1–3.4, summary, review questions, 3 exercises, references) | 657 | 380 | 0 | 25 | 4,073 |
| Chapter 4. Benchmarks (4.1 Table 4.1/4.2, 4.2 descriptions, 4.3 code, summary, review questions, 2 exercises, references) | 872 | 722 | 0 | 58 | 4,010 |
| Chapter 5. Efficiency analysis (5.1 statistics, 5.2 execution time, summary, 3 exercises, references) | 611 | 470 | 0 | 3 | 3,868 |
| Chapter 6. Control problems (6.1–6.3, summary, review questions, 4 exercises, references) | 1,836 | 1,188 | 500 | 106 | 9,452 |
| Chapter 7. Optimal design (7.1–7.2, summary, review questions, 4 exercises, references) | 1,071 | 752 | 183 | 48 | 3,786 |
| Appendix A. Benchmark plots | 234 | 229 | 0 | 108 | 36 |
| Appendix B. Benchmark code (54 functions, as table cells) | 1,288 | 1,269 | 0 | 0 | 26 |
| Appendix C. Experimental results (14 algorithms × 54 functions) | 3,651 | 3,532 | 0 | 54 | 90 |
| Appendix D. Plotting code | 256 | 237 | 0 | 0 | 9 |
| Appendix E. Execution times | 847 | 841 | 0 | 0 | 23 |
| Glossary | 98 | 8 | 0 | 0 | 1,519 |
| Table of contents, placed **after** the glossary, as a two-column table | 231 | 228 | 0 | 0 | 0 |

Prose outside tables: about 40,300 words; including table text and listings the document is about 66,000 words. Word reported 346 pages for the 2026-10-15 edition.

Observations on structure:

- Chapter 1 and Chapter 4 headings use the Word heading styles (`1`, `2`, `3` — the Ukrainian-locale style ids for Heading 1–3). Chapters 2, 3, 5, 6, 7 and the appendices use plain paragraphs for their titles, so the navigation pane, a TOC field and EPUB conversion see only two chapters. The end-of-book table of contents is typed by hand with page numbers and uses the **old** chapter titles (for example "Chapter 1. THE PARTICLE SWARM OPTIMIZATION METHOD (PSO)", "4.3 Code Implementation of the Benchmarks") that no longer match the body ("4.3 Python Code Development for Experiments Implementation"). It is stale and sits at the wrong end of the book.
- No bookmarks, no cross-reference fields, no TOC field, no caption fields. Figure and table numbers are typed text. There are 24, 8, 8, 0, 2, 29, 8 figure captions in Chapters 1–7 and 2, 4, 1, 2, 2, 4, 3 table captions.
- Code listings in Chapters 1–5 are two-column tables (code left, explanation right), one line of code per row. Chapters 6–7 and Appendix D use the `MathematicaCellInput` paragraph style for code. Both forms are kept; the copyedit tool refuses to touch code cells unless an edit is explicitly flagged.
- Equations: 229 `Equation.3` OLE objects (Microsoft Equation Editor 3.0, removed from Office in January 2018 — these cannot be edited in current Word and render as pictures) and 33 Visio drawings; 261 PNG, 222 WMF, 33 EMF images in `word/media`. The notation audit therefore covers prose, captions and table text only; the formula images are not auditable from the file. Converting them to OMML or LaTeX is a separate project (`book-improvement-plan.md`, item 4).
- Page setup: US Letter (12240 × 15840 twips), margins 1 in top/bottom, 0.75 in sides, 0.25 in gutter, one section, footers with page numbers, no running headers. KDP trim size has not been chosen; the file is not laid out for a 6 × 9 in or 7 × 10 in trim.
- Front matter: title page uses initials (`Y. Romasevych`, `V. Loveikin`, `D. Komarchuk`); the approved author line uses full names. The subtitle on the title page (¶19) is "Algorithms, Python Implementations, and Engineering Applications"; the approved subtitle is "Algorithms, Engineering Applications, and Practical Examples" (repository `README.md`, `CITATION.cff`). The setup text says "Install Python 3.11 or newer" (¶58); the repository will say 3.12.
- Bibliography: per-chapter reference lists, numbered, cited in text as `[n]`. Entry style is consistent within a chapter (author-initial order, journal, year, pages, DOI where present). No book-level bibliography.
- Exercises: every chapter ends with Chapter Summary, Review Questions (Chapter 5 has none) and numbered exercises; Chapter 6 also has "Practical Exercise No. 1" on a different plant from Problem 1a (`docs/manuscript-replacements.md`).
- Translation state: the text is already fluent American English; very few British spellings remain (`Optimisation`, `minimise`, `Modelling`, one each) and the filler phrases the brief lists ("it is worth mentioning", "as we can clearly see", "obviously") do not occur. The remaining work is sentence-level: long chained sentences, literal constructions ("the matrix Position", "the vector of the lower bound"), inconsistent terminology (see `style-guide.md`), and explanation cells that restate the code line instead of explaining it.

## Repository inventory (unchanged in this audit)

Read from the clone: `src/metaopt` (pso, de, gwo, variants, benchmarks, constraints, applications, experiments, reproduction, plotting), `tests/` (134 tests, pass on Python 3.12.13 / NumPy 2.5.4 / SciPy 1.18.1 on this Mac in 34 s), `notebooks/01–10`, `examples/`, `scripts/` (including `verify_book_code.py`, `prepare_reviewed_manuscript.py`, `compare_published_values.py`), `results/` (CI records, reduced comparison, published-value comparison, cost estimate), `docs/` (errata, manuscript replacements, book-code map, coverage matrix, experiment protocol, reproducibility, validation report, final audit, release readiness, licensing audit, author decisions). CI: pytest on 3.11 and 3.12, notebooks on 3.11, doc-link check, wheel build; last green run recorded for `a36d610`.

Known scientific limitations carried forward, not closed here: Appendix C and Appendix E are historical legacy-stream results and were not reproduced (`results/full_experiment_cost_estimate.json`: 945,000,000 nominal evaluations, 8.8–65.6 h); the software license is unnamed; copyright shares are not stated; no release tag exists, so book links point at `/blob/main/`.

## Major concerns, in priority order

1. **Uncorrected Table 4.1 cells** in the current manuscript (Whitley, Perm 0, rotated bound, Xin-She Yang noise). Evidence-backed since 2026-10-19; must be applied as tracked changes and accepted by the authors.
2. **Protocol and claim honesty in Chapter 5**: the chapter must state the Appendix C/E protocol (population 25, 500 iterations, 100 runs, D = 30, legacy seed stream) and label the tables historical. Reviewed in `scientific-corrections.md`.
3. **Problem 1a objective vs Practical Exercise 1** (Chapter 6): the text must make the two plants and the two criteria explicit.
4. **Navigation**: heading styles missing on five chapters; stale hand-typed TOC at the back; no TOC at the front.
5. **Front matter**: subtitle, author names, Python version, and an introduction that does not yet say what the book does not cover or how it is organised (brief §14).
6. **Terminology drift** across chapters (particle/agent/individual/wolf used for the same role; fitness vs objective-function value; iteration vs epoch vs generation). Fixed by the style guide and the copyedit.
7. **Equation Editor 3.0 objects**: not editable, not accessible, not reflowable for EPUB. Out of scope; recorded.
8. **Print readiness**: no trim size, gutter 0.25 in, no running headers, widows/orphans not controlled, table breaks not checked. Out of scope beyond a sampled render.

## Tooling added in this pass

- `scripts/editorial/editorial_docx.py` — shared paragraph model (index, style, table cell column, embedded-object and code-like flags, section).
- `scripts/editorial/extract_paragraphs.py` — dumps `manuscript_extract/paragraphs.jsonl` and per-section Markdown for reviewers.
- `scripts/editorial/apply_tracked_edits.py` — applies paragraph-level before/after edits as `w:del`/`w:ins` tracked changes (author "Editorial (Claude)"), refusing code cells unless flagged. See `chapter-review.md` for the counts.

Rendering: LibreOffice, pandoc and poppler are not installed on this Mac and Homebrew is blocked until the Xcode license is accepted (`sudo xcodebuild -license accept`). The visual check in `publication-readiness.md` records what was and was not rendered.
