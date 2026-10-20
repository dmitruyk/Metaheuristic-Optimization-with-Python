# Final change summary

Phase: Validation. Date: 2026-10-20. Base commit `0fc55d5` on `main`. Data source: this checkout, local Python 3.11.7, and GitHub Actions run 39377458555. Execution is local computation plus that Linux run. Not paper trading and not live execution.

| Area | Before | After | Evidence | Remaining issues |
| --- | --- | --- | --- | --- |
| Scientific accuracy | Whitley table and Appendix B disagreed, and Problem 1a was recorded as an open choice between ITAE and settling time | Whitley formula kept; table cells in the review copy set to location 1, value 0. Problem 1a identified as ITAE. Exercise 1 kept as a separate plant | `tests/test_benchmarks.py`, `tests/test_examples_smoke.py`, `docs/errata.md` | Authors still accept the review copy before KDP. Printed Appendix C cells were not recomputed |
| Code quality | Library already used Generator, result objects, and boundary checks | Descriptive PID names, full-job schedule, public comparison and cost scripts. No license or author edit | `src/metaopt/applications/pid.py`, `src/metaopt/reproduction.py` | No approved open-source license |
| Test coverage | 60 passed on 2026-10-19 | 132 passed locally on Python 3.11.7 (13.29 s) and 3.12.13 (14.89 s). Linux CI passed on `e6940ba` and on `87d7c01` | runs 39379558457 and 39379892358 | `results/ci/summary.json` is the workflow log of the later run, not a third test |
| Reproducibility | Reduced 5-run study, correctly labeled as not Appendix C | Quick profile plus a full-protocol cost estimate of 945000000 evaluations (about 8.8–65.6 hours). 11 worked scalars matched | `results/quick_validation_summary.json`, `results/full_experiment_cost_estimate.json`, `results/published_comparison.json` | Appendix C and Appendix E remain unmatched historical results |
| Book-code consistency | Chapter map existed. Downloads DOCX had no repository links | Chapter-to-notebook table in `docs/book-code-map.md`. Review DOCX inserts those links. Three DOCX files compared | `docs/final-audit.md` manuscript table | Links use `/blob/main/` until a tag exists. The review DOCX is not in git |
| Documentation | Release checklist was a no-go, and the validation report still said Linux CI was unobserved | Current status separates that historical sentence from run 39377458555. Authorship comparison written | `docs/validation-report.md`, `docs/authorship-and-license.md` | License and author order remain author decisions |
| Publishing readiness | No visual proof, no license | Review DOCX generated with `w:` markup preserved. LibreOffice 6.3.4.2 aborts with signal 6 on this Mac for the source and the review copy, so no PDF exists | `manuscript/README.md`, `docs/release-readiness.md` | Page-by-page visual acceptance is open. No-go for KDP |

## Scores

These scores use the evidence column above. They are not the 9.5 target.

| Score | Value | Why it is not higher |
| --- | --- | --- |
| Repository | 8.4/10 | 132 local tests passed on Python 3.11.7 and 3.12.13. Linux CI passed for `e6940ba` (run 39379558457) and for `87d7c01` (run 39379892358). The repository still has no approved license, and Appendix C was not rerun |
| Manuscript | 7.6/10 | Scientific table corrections and companion links are in a review copy. The copy has not had page-by-page visual acceptance, and the copyright line still disagrees with the repository |
| Scientific reproducibility | 5.5/10 | Worked scalars match. The manuscript's 945000000-evaluation study was estimated and not run. Quick results are labeled as a different experiment |
| Amazon KDP readiness | 3.5/10 | No-go. License, author line, and historical appendices are open. LibreOffice 6.3.4.2 signal 6 means this session produced no PDF and no page inspection |

## Go / no-go

No-go for a tagged GitHub release and no-go for Amazon KDP. Stakeholders: Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk. Data: the table above. A release tag was not created.
