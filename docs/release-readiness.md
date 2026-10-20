# Release-readiness checklist

Phase: Validation. Date: 2026-10-19.

**Go / no-go: no-go for a tagged public release, and no-go for a KDP-ready claim.**

Rationale: the license is unnamed, author-order confirmation against the manuscript copyright line is still required, Appendix C and Appendix E were not reproduced, Whitley and the Problem 1a objective are unresolved, and the 346-page DOCX has not had a page-by-page visual check. Data used: `docs/validation-report.md`, `docs/errata.md`, `docs/coverage-matrix.md`, and `results/reduced_comparison_summary.json` after the review commands in the validation report. Stakeholders: Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk. This file does not speak for them.

KDP-ready is not claimed. A high-resolution PDF and a visual check of equations, code tables, and captions are still required.

| # | Check | State | Evidence |
| --- | --- | --- | --- |
| 1 | Author order and license confirmed in writing by the credited authors | 🔴 open | `LICENSE` records repository-creation approval and no open-source license |
| 2 | Whitley table and Appendix B reconciled together | 🔴 open | `docs/manuscript-replacements.md` |
| 3 | Problem 1a criterion named in Section 6.3 | 🔴 open | both functions remain in `src/metaopt/applications/pid.py` |
| 4 | Appendix C tables reproduced or explicitly labeled historical | 🔴 open | full study not run; reduced study is labeled `matches_appendix_c: false` |
| 5 | Appendix E timings reproduced or explicitly labeled historical | 🔴 open | full timing workbook not run |
| 6 | Python 3.11 and 3.12 unit tests green on GitHub-hosted Linux | 🟡 waiting on this pull request's Actions run | local runs are in `docs/validation-report.md`; Linux is not local evidence |
| 7 | Notebooks 01–10 execute from a clean checkout on Linux | 🟡 waiting on the notebook job | local execution is in the validation report |
| 8 | Book links resolve | 🟡 repository markdown checked; DOCX hyperlinks need the manuscript file | `python scripts/validate_doc_links.py` |
| 9 | Every published figure and table marked verified or unverified | 🟢 recorded | `docs/book-code-map.md` and `docs/coverage-matrix.md`; figures stay unverified |
| 10 | Dependency pins from the validation environments | 🟢 recorded as platform-specific locks, not as a cross-platform solver | `requirements/lock-py311.txt`, `requirements/lock-py312.txt` |
| 11 | Tagged release, then replace `/blob/main/` links | 🔴 not started | do this only after items 1–7 are accepted |
| 12 | Page-by-page visual QC of the print PDF | 🔴 not done | do not call the DOCX KDP-ready |

## Next steps

| Step | Owner | Target date | Rolled forward |
| --- | --- | --- | --- |
| Confirm author order against the manuscript copyright line and name a license, or state that the companion stays all-rights-reserved | Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk | 2026-11-02 | open |
| Choose Whitley option A or B in `docs/manuscript-replacements.md` and apply both the table and the code together | Handbook authors, then the repository maintainer for the code half | 2026-11-02 | open |
| Name the Problem 1a objective in Section 6.3 | Handbook authors | 2026-11-02 | open |
| Read the GitHub Actions log for this pull request on Python 3.11 and 3.12 and on the notebook job | Dmytro Komarchuk | 2026-10-26 | open until the checks are green on `ubuntu-latest` |
| Decide whether Appendix C and Appendix E stay historical legacy-stream results or are replaced by a new Generator study large enough to republish | Handbook authors | 2026-11-16 | open; the reduced study does not close this |
| After items above, tag a release and update book links from `/blob/main/` to that tag | Dmytro Komarchuk, after author approval | no date until the no-go items close | open |
| Render a print PDF and check equations, listings, and captions page by page | Editor designated by the authors | no date until the DOCX is frozen | open |

Incomplete rows stay on this list until they close. No row authorizes a license edit or an author-order edit by the maintainer alone.
