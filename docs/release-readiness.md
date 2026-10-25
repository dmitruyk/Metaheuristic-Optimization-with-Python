# Release-readiness checklist

Phase: Validation. Date: 2026-10-19.

**Go / no-go: no-go for a tagged public release, no-go for applying the MIT License, and no-go for a KDP-ready claim.**

Rationale, updated 2026-10-25: `LICENSE` still has no MIT grant (`docs/licensing-audit.md`). The revised-edition co-author order is Yuriy Romasevych, Viatcheslav Loveikin, Dmytro Komarchuk, without a statement of copyright shares. Appendix C and Appendix E were not reproduced, and the print PDF has not had page-by-page visual acceptance. Whitley and Problem 1a stay as recorded in `docs/manuscript-replacements.md`. Data used: `docs/licensing-audit.md`, `docs/validation-report.md`, `results/published_comparison.json`, `results/full_experiment_cost_estimate.json`, and GitHub Actions run 39380621540 on `c803af2`. Stakeholders: Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk. This file does not speak for them.

KDP-ready is not claimed. A high-resolution PDF and a visual check of equations, code tables, and captions are still required.

| # | Check | State | Evidence |
| --- | --- | --- | --- |
| 1 | Author order and license confirmed in writing by the credited authors | 🟡 co-author order recorded; MIT not applied | `docs/licensing-audit.md`, `docs/authorship-and-license.md` |
| 2 | Whitley table and Appendix B reconciled together | 🟡 formula and review-copy cells agree; publication acceptance open | `docs/manuscript-replacements.md` |
| 3 | Problem 1a criterion named in Section 6.3 | 🟢 ITAE, matched to the printed scalars. Exercise 1 is a different plant | `results/published_comparison.json` |
| 4 | Appendix C tables reproduced or explicitly labeled historical | 🟡 labeled historical. Cost estimated. Not run | `results/full_experiment_cost_estimate.json` |
| 5 | Appendix E timings reproduced or explicitly labeled historical | 🟡 labeled historical. Not run | `docs/experiment-protocol.md` |
| 6 | Python 3.11 and 3.12 unit tests green on GitHub-hosted Linux | 🟢 run 39380621540 on merge `c803af2`. `publish-results` skipped on `main` by the workflow condition | `docs/validation-report.md` |
| 7 | Notebooks 01–10 execute from a clean checkout on Linux | 🟢 the notebooks job in that run succeeded | same Actions run |
| 8 | Book links resolve | 🟡 repository markdown links resolve. The review DOCX adds chapter links to `main`. The Downloads source still has no repository links | `python scripts/validate_doc_links.py` |
| 9 | Every published figure and table marked verified or unverified | 🟢 recorded | `docs/book-code-map.md` and `docs/coverage-matrix.md`; figures stay unverified |
| 10 | Dependency pins from the validation environments | 🟢 recorded as platform-specific locks, not as a cross-platform solver | `requirements/lock-py311.txt`, `requirements/lock-py312.txt` |
| 11 | Tagged release, then replace `/blob/main/` links | 🔴 not started | do this only after items 1–7 are accepted |
| 12 | Page-by-page visual QC of the print PDF | 🔴 not done | LibreOffice 6.3.4.2 aborts with signal 6 on this Mac before loading the editorial DOCX or the review copy. No PDF was written |

## Next steps

| Step | Owner | Target date | Rolled forward |
| --- | --- | --- | --- |
| Name MIT in a written software grant, or keep the companion all-rights-reserved | Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk | 2026-11-02 | open. Co-author order for the revised edition is recorded. MIT was not applied on 2026-10-25 |
| Accept the Table 4.1 review copy (Whitley, Perm 0, rotated bound, Xin-She Yang noise) | Handbook authors | 2026-11-02 | open; the scientific correction is already in the local review copy |
| Confirm that Section 6.3 stays the ITAE objective and that Practical Exercise 1 stays a separate plant | Handbook authors | 2026-11-02 | identification recorded; no deletion was made |
| Confirm the workflow commit that adds `results/ci/summary.json` after the next push | Dmytro Komarchuk | 2026-10-26 | closed for this branch by `d37e243`, which records run 39379558457 |
| Decide whether Appendix C and Appendix E stay historical legacy-stream results or are replaced by a new Generator study large enough to republish | Handbook authors | 2026-11-16 | open; the reduced study does not close this |
| After items above, tag a release and update book links from `/blob/main/` to that tag | Dmytro Komarchuk, after author approval | no date until the no-go items close | open |
| Render a print PDF on a host where LibreOffice does not abort, then check equations, listings, and captions page by page | Editor designated by the authors | 2026-11-09, blocked here by LibreOffice 6.3.4.2 signal 6 | open |

Incomplete rows stay on this list until they close. No row authorizes a license edit or an author-order edit by the maintainer alone.
