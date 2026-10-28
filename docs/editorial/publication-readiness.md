# Publication readiness

Phase: Final quality assurance of the editorial pass. Date: 2026-10-27. Branch `editorial/manuscript-edit-2026-10-27` on `dtkachenko/Metaheuristic-Optimization-with-Python` (fork of `dmitruyk/…`).

**Go / no-go: no-go for publication; go for author review of the redline.** The manuscript now has a complete professional copyedit and the evidence-backed text corrections as tracked changes, but 77 scientific items need an author decision, the equations are frozen Equation 3.0 objects, no print layout exists, the page-by-page PDF check has not been done, and the licensing/author-share decisions from `docs/release-readiness.md` are still open. Nothing below is a claim that a target score was reached.

## Deliverables of this pass

| File | What it is |
| --- | --- |
| `~/Downloads/Metaheuristic_Optimization_with_Python_Edited_2026-10-27.docx` (also `manuscript/`, gitignored) | the 2026-10-25 manuscript with 1,011 tracked edits by `Editorial (Claude)`: copyedit, scientific corrections, headings, TOC |
| `~/Downloads/Metaheuristic_Optimization_with_Python_Edited_2026-10-27_clean.docx` | the same with every change accepted |
| `~/Downloads/Metaheuristic_Optimization_with_Python_Technical_Review_2026-10-27.md` = `docs/editorial/scientific-corrections.md` | 180 technical findings with evidence, status and the open author decisions |
| `docs/editorial/initial-audit.md`, `book-improvement-plan.md`, `style-guide.md`, `chapter-review.md`, `code-validation.md`, this file | editorial record |
| `scripts/editorial/` + `tests/test_editorial_tools.py` | extract, check, merge, apply-as-tracked-changes, accept-all |

How to review the redline in Word: Review → Track Changes → All Markup; accept or reject per change; right-click the table of contents after the copyright page → Update Field. Formatting changes (heading styles) are tracked too and can be rejected paragraph by paragraph.

## Gates from the brief (§22)

| Gate | State | Evidence |
| --- | --- | --- |
| Approved title and subtitle on the manuscript | 🟢 applied as a tracked change (FM-01) | title page ¶19 |
| Three authors represented consistently | 🟡 full names on the title page (FM-03); copyright line unchanged because shares are an open author decision | `docs/author-decisions.md` |
| Chapter structure coherent | 🟡 every chapter, section, subsection and end-matter heading now carries a heading style; chapter titles on one line in title case; stale back TOC removed, TOC field added. The A–M learning progression is not applied (`book-improvement-plan.md` follow-up A) | `chapter-review.md` |
| Technical content reviewed | 🟢 all seven chapters and the appendices reviewed against `src/metaopt`; 180 findings | `scientific-corrections.md` |
| Mathematical corrections documented | 🟡 every finding has evidence and a status; 86 text-only corrections applied; 77 pending author decisions (equation images, algorithm choices, claims) | same |
| Executable code examples validated | 🟡 repository tests (137) and notebooks (10) pass on Python 3.12; printed listings parse (75 of 76; the `%pip` cell is a notebook magic). Listings that cannot run as printed are logged (SADE fragment, Chapter 4 Exercise 1, Table 3.1 as extracted) and not changed in this pass | `code-validation.md` |
| Scientific results accurately characterised | 🟡 Appendix C/E labelled historical with the protocol and a reproduction-status paragraph; single-run qualifiers added; ranking rule stated. The Appendix C/E rerun remains an author decision (8.8–65.6 h) | C5-19, XC-03 |
| Terminology consistent | 🟢 style-guide table applied across chapters; one open choice: `vonNeumann-PSO` (function name) vs "von Neumann PSO" in prose | `style-guide.md`, `chapter-review.md` |
| English editing complete | 🟢 826 copyedit records over all prose, captions, explanation cells, exercises and glossary; checker: 0 errors; sampled manual read | `chapter-review.md` |
| Figures and tables checked | 🟡 tables: numbers in Chapter 5/6/7 and Appendices C/E recomputed and consistent; Table 4.1/4.2 corrected. Figures: only names, numbering and cross-references checked; images not auditable; colour-only figures noted (C3-19) | reviews |
| Cross-references functional | 🟡 wrong figure/table/equation numbers corrected (Chapters 2, 6, 7); references are typed text, not fields, so they will not renumber automatically | C2-05/06, C6-10, C7-09 |
| Manuscript professionally formatted | 🔴 not done: no trim size, no running headers, widow/orphan and table-break control not set; equations are Equation 3.0 pictures (229) | `initial-audit.md`, follow-ups C and E |
| PDF pages visually inspected | 🟡 sampled, not page by page. LibreOffice 26.8.1 rendered the accepted copy to 348 pages (US Letter; the untouched source renders to 356). Inspected at 55 dpi: title page, Contents, Chapter 1 opener, Table 1.2 listing page, Table 4.1 (corrected cells visible), Table 4.2, Chapter 6 opener with Equation 3.0 objects, a Chapter 6 listing page, Appendix C plot pages, Appendix E, glossary. Text-free pages are the same figure pages as in the source; two trailing blank pages left by the removed TOC were fixed by deleting the empty paragraphs around it. Not a print proof: no trim size, running headers or widow control | `manuscript/render/` (gitignored) |
| Digital output validated | 🔴 not attempted; blocked on heading styles (done), editable equations (not done) and code-table conversion | follow-up F |
| Remaining limitations documented | 🟢 this file, `scientific-corrections.md` ("Open author decisions"), `book-improvement-plan.md` | — |

## Open author decisions (summary; the full table AD-01…AD-27 is in `scientific-corrections.md`)

1. Chapter 6 cart-pole: the printed step function has gravity signed for a swing-down; fix the prose or flip the dynamics and recompute Problem 5.
2. Chapter 2: make Table 2.1 DE/rand/1 as described, or state DE/best/1 up front; rename or re-describe "SADE" (simplified jDE).
3. Chapter 7: I-beam `tw` vs `tf`; Problem 2 constants; which algorithms the summary recommends; Problem 4 iteration count.
4. Chapter 3: EPD-GWO comparison on an unequal evaluation budget; whether the EPD offset should be a neighbourhood.
5. Chapter 1: IA-PSO's origin-dependent result; the two von Neumann neighbourhoods (Chapter 1 vs Appendix B).
6. Chapter 4: Table 4.1 corrections to accept (Whitley, Perm 0, rotated bound, Yang noise, Trid, Cosine Mixture, Quintic) and the Table 4.2 flag changes; Exercise 2 run count.
7. Chapter 5: Appendix C/E rerun or historical label; ranks computed on printed values.
8. License, copyright shares, release tag (`docs/author-decisions.md`).

## Repository state

- Commits on the branch: editorial audit/plan/style guide; Python 3.12 standardisation; tracked-change tooling; checker and code validation; corrections log, chapter review and readiness. The manuscript binaries are not committed (`BOOK_LICENSE.md`).
- CI: GitHub Actions run [40630835480](https://github.com/dtkachenko/Metaheuristic-Optimization-with-Python/actions/runs/40630835480) on the fork branch (push of `2f0c0c1`): success on the 3.12-only matrix (tests, notebooks, doc links, wheel). Upstream PR #5 shows no checks until a maintainer approves workflow runs for the fork.
- Regenerate the redline from the source: unzip the source, `merge_runs.py`, `extract_paragraphs.py`, then `merge_edits.py` over `manuscript_extract/edits/*.jsonl` (corrections first, structure last) and `apply_tracked_edits.py`; the edit files are not committed because they quote the all-rights-reserved text.

## Next steps

| Step | Owner | Target |
| --- | --- | --- |
| Author review of the redline: accept/reject; answer AD-01…AD-27 | Yuriy Romasevych, Viatcheslav Loveikin, Dmytro Komarchuk | 2026-11-16 |
| Apply the decisions (second editorial pass), then follow-ups A–B (chapter openers, practical considerations, exercise levels) | editor + authors | after the review |
| Equations to editable math (follow-up C); figure regeneration (D) | editor | after the decisions on Appendix C/E |
| Print layout and page-by-page PDF proof (E); EPUB (F) | production | after C |
| License, shares, release tag; retarget `/blob/main/` links | authors | `docs/author-decisions.md` dates |
