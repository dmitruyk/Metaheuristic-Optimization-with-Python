# Book improvement plan

Phase: Discovery. Date: 2026-10-27. Companion to `initial-audit.md`. Items marked **this pass** are done on branch `editorial/manuscript-edit-2026-10-27`; items marked **follow-up** are proposed with their cost and the decision they need. Nothing here changes a scientific claim without an entry in `scientific-corrections.md`.

## Priorities

| # | Improvement | Impact | Status |
| --- | --- | --- | --- |
| 1 | Apply the evidence-backed Table 4.1 corrections and the Chapter 5/6 labelling fixes as tracked changes | correctness | **this pass** |
| 2 | Professional American-English copyedit of all prose, captions, explanation cells, exercises, glossary; consistent terminology per `style-guide.md` | readability, consistency | **this pass** |
| 3 | Front matter: approved subtitle, full author names, Python 3.12, introduction completed against brief §14 (audience, prerequisites, what you will learn, organisation, how to use the repository, what the book does not cover) | positioning | **this pass** (short tracked insertions only) |
| 4 | Navigation: Heading 1/2/3 on every chapter, section and subsection; TOC field at the front; stale back-of-book TOC deleted | usability, EPUB, KDP | **this pass** (tracked formatting changes; the TOC field is refreshed in Word) |
| 5 | Chapter 5 reproduction-status paragraph pointing at `docs/experiment-protocol.md` and `results/reduced_comparison_summary.json`, tables labelled historical | scientific honesty | **this pass** |
| 6 | Chapter architecture: add to each algorithm chapter (1–3) a short "What you will learn" opener, a "Practical considerations" subsection (parameter tuning, stagnation, boundary handling, budget), and a "Further reading" pointer; align Chapters 6–7 problem write-ups to the same Motivation → Formulation → Reduction → Implementation → Results → Limitations order | instructional design | **follow-up A**: 2–3 author-days of new text per chapter; needs author approval because it adds content |
| 7 | Exercises: tag each with a level (Understanding / Implementation / Experimentation / Engineering application / Research extension), add learning objective, inputs, deliverable and reproducibility requirement; solutions guidance in the repository `docs/` | educational effectiveness | **follow-up B**: editorial, 1 day; solutions need the authors |
| 8 | Equations: convert 229 Equation Editor 3.0 objects to editable Word math (OMML) or to LaTeX for a typeset edition; without this the equations are frozen pictures, not accessible, and do not reflow in EPUB | accessibility, maintainability, EPUB | **follow-up C**: 229 objects; MathType can batch-convert Equation 3.0 → OMML if a licensed copy is available; otherwise retyping, about 2 days, plus a symbol-by-symbol check; authors must approve the retyped forms |
| 9 | Figures: regenerate convergence and benchmark plots from `scripts/reproduce_figures.py` at print resolution with grayscale-safe palettes; add the figure source paths to captions; add the missing diagrams the brief suggests only where a chapter lacks one (particle update geometry in 1.1; exploration/exploitation schedule in 3.1) | visual quality, reproducibility | **follow-up D**: figures stay unverified against the book until the Appendix C protocol is rerun; new diagrams need author review |
| 10 | Appendix C and E: either rerun under the documented protocol (8.8–65.6 h) with the Generator stream and republish, or keep as historical with the label applied in item 5 | scientific reproducibility | **author decision**, due 2026-11-16 per `docs/author-decisions.md` |
| 11 | Print layout: choose KDP trim (7 × 10 in suits the code tables), set margins and gutter from the KDP calculator for ~350 pages, running headers, widow/orphan control, keep-with-next on captions and listing headers, table header rows repeating, page-by-page proof | print readiness | **follow-up E**: 2–3 days in Word or InDesign after the copyedit is accepted; a PDF must then be inspected page by page |
| 12 | Digital edition: EPUB/Kindle build from the heading-styled DOCX; code tables must become preformatted blocks; equations need item 8 | digital readiness | **follow-up F**: blocked on items 4 and 8 |
| 13 | Links: replace `/blob/main/` with a release tag once one exists; add the companion repository URL to every chapter opener | reproducibility | **follow-up G**, after the authors tag a release |
| 14 | Licensing and authorship: name the software license, state copyright shares | legal | **author decision**, due 2026-11-02 |

## Sequencing

This pass delivers items 1–5 as one tracked-changes DOCX plus the reports. The natural next passes are A + B (content additions, author-led), then C + D (equations and figures), then E + F (layout), with item 10's decision taken before any figure or table is regenerated. Items 13 and 14 need no editorial time, only decisions.

## What is deliberately not proposed

- Shortening chapters or removing derivations, negative results or limitations (brief rules 7, 11).
- Replacing the handbook's PSO/DE/GWO with library implementations in the text; the book's listings stay the teaching code, the repository stays the tested code (brief §6).
- Marketing language in chapters; the positioning work is confined to the front matter.
