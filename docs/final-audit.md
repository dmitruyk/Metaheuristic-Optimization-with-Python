# Final audit

Phase: Validation. Date: 2026-10-20. Branch `quality/final-repository-2026-10-19`, started from `main` at `0fc55d5`.

**Go / no-go: no-go for a tagged release, and no-go for Amazon KDP.**

Rationale: the license is unnamed, the copyright line and the repository author list disagree, Appendix C and Appendix E were not reproduced, and the print PDF has not had a page-by-page visual acceptance. Data: this file, `docs/validation-report.md`, `results/ci/summary.json`, GitHub Actions run 39377458555, `results/published_comparison.json`, `results/full_experiment_cost_estimate.json`. Stakeholders: Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk. This file does not speak for them.

## What was already done, and was not repeated

The companion library, notebooks 01–10, benchmark guards, Generator seeding, and the Linux workflow were already on `main`. Run 39377458555 on `0fc55d5` passed pytest on Python 3.11 and 3.12 and the notebook job. `results/ci/summary.json` records the earlier push run 39377284980 for `e85e014`, because the workflow does not commit CI logs onto `main`.

Run 39377406220, a pull request for `d0b5c29609`, is a recorded failure with zero jobs in the API. Logs returned HTTP 403 in this session. It is disclosed and not treated as a pytest failure.

## Findings

| ID | Severity | Evidence | Recommended fix | Verification | Status |
| --- | --- | --- | --- | --- | --- |
| F1 | High | Table 4.1 Whitley cells were location 0, value 1. Appendix B and evaluation give 0 at all ones. Origin value is `D^2 (1/4000 - cos(1) + 1)`, not 1 | Correct the two cells. Do not change the formula | `test_whitley_minimum_is_zero_at_the_all_ones_vector`; review DOCX cells read back as location 1, value 0 | Resolved in code and in the local review copy. Publication acceptance still open |
| F2 | High | Settling-time listing is Practical Exercise 1 on `1/(1+s)**3`. Section 6.3 Problem 1a is ITAE. Earlier errata called the exercise the solving section | Keep both criteria, name them, do not swap them | `test_pid_worked_values`; `results/published_comparison.json` matches ITAE and leaves settling unmatched | Resolved as an identification. No printed optimizer table was recomputed |
| F3 | High | Appendix C is 14 algorithms, 54 functions, D=30, population 25, 500 iterations, 100 runs, legacy `RandomState`. The stored study is a smaller Generator smoke test | Document the protocol, estimate the cost, do not label the smoke test as Appendix C | `results/full_experiment_cost_estimate.json` (`executed: false`); `results/quick_validation_summary.json` (`matches_appendix_c: false`) | Open. Cost reported. Run not started |
| F4 | High | Appendix E is the same sizes with 20 runs and wall/CPU time | Same as F3 | same estimate, timing hour range about 1.75–13.1 hours | Open. Historical |
| F5 | High | `LICENSE` names no open-source license. Copyright line has two authors; repository files have three | Record the discrepancy. Do not choose a license or reorder authors | `docs/authorship-and-license.md` | Open. Author decision |
| F6 | Medium | Perm 0 table location `i-1` is not a minimizer; `1/i` is 0. Rotated lower bound printed `-65.53` against Appendix B `-65.536`. Xin-She Yang text said a normal draw on `[0, 1]` | Correct those table texts. Leave the formulas | manuscript script log; Perm test `Perm0DBetaFunction` at `i-1` is greater than 1 | Applied in the local review copy |
| F7 | Medium | `results/ci/summary.json` is one commit behind the green `main` run, because publish-results skips `main` | Say so in the validation report. Do not describe Linux CI as unverified | run 39377458555 | Documented |
| F8 | Medium | CI lacked an explicit doc-link check and a wheel build | Add both, plus the quick profile, to `.github/workflows/ci.yml` | workflow diff. This branch's Actions run is pending until the branch is pushed | Implemented locally. Not yet observed on GitHub |
| F9 | Medium | Downloads editorial DOCX, Telegram DOCX, and `Documents/HANDBOOK.docx` are three files | Compare them before editing | hashes in `docs/final-change-summary.md`. No DOCX is in the GitHub repository | Compared. Editorial file is the review source |
| F10 | Low | Print PDF and page-by-page visual QA | Render if a working converter is available, and do not call the DOCX KDP-ready without a visual pass | LibreOffice 6.3.4.2 exits with signal 6 on macOS 26.6.2 before opening either DOCX. No PDF file | Open. Environment limitation, not a reviewed page |

## Numerical audit

All 54 benchmarks were evaluated at the midpoint of the registered domain in dimension 2 (`test_every_benchmark_is_finite_at_the_domain_midpoint`). Elliptic rejects dimension 1. Paviani warns outside `(2, 10)`. Alpine No. 2 is non-finite for a negative coordinate. Schwefel 2.23 at `1e40` is infinite and does not raise. Empty points and dimension 0 are rejected by the domain helpers. DE rejects a population below 4. GWO rejects a pack below 3. A budget smaller than the initial population raises. Non-finite objectives are not kept as the reported best when a finite value exists. These checks did not change formulas.

## Manuscript files compared

| File | Bytes | SHA-256 | Modified | Role |
| --- | --- | --- | --- | --- |
| `~/Downloads/Metaheuristic_Optimization_with_Python_Editorial_Edition.docx` | 29201623 | `d34a1841d68a5d1dd64322be5cbe5a499c8e36f9bdac72d5aa695ea81dbef16f` | 2026-10-15 | review source. Title matches the repository. Eight citation links, no repository links |
| `~/Downloads/Telegram Lite/HANDBOOK_Python.docx` | 29779307 | `d9a0770e765bbb48c191587cca051c8f81303aca1df139f22bad9b83c5c18afb` | 2026-10-15 | same core dates, paragraph ratio 0.9993. Title is *FOR ENGINEERING*. Drops the editorial front-matter notes |
| `~/Documents/HANDBOOK.docx` | 27975659 | `07c7517f16ef75ba9c26909029f57a56277dfc3af4a5d64c81976c60a49b928c` | 2026-08-05 | older manuscript, paragraph ratio about 0.28, no `BASE_SEED` |
| GitHub repository | no `.docx` |  |  | there is no GitHub-linked manuscript file |

The review copy is `manuscript/Metaheuristic_Optimization_with_Python_reviewed.docx` on this machine. It is gitignored.

## Next steps

| Step | Owner | Target date | Rolled forward |
| --- | --- | --- | --- |
| Confirm license and author order | Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk | 2026-11-02 | open from `docs/release-readiness.md` |
| Accept or reject the Table 4.1 review copy | handbook authors | 2026-11-02 | new |
| Decide whether Appendix C and Appendix E stay historical | handbook authors | 2026-11-16 | open |
| Visual acceptance of the print PDF | editor designated by the authors | 2026-11-09 | open |
| Confirm GitHub Actions on this branch after it is pushed | Dmytro Komarchuk | 2026-10-26 | open |
