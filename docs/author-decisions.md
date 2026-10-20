# Author decisions still open

Phase: Validation. Date: 2026-10-20.

Work that does not need these decisions has continued. Nothing in this list was guessed.

| Decision | Evidence already in hand | Owner | Target date |
| --- | --- | --- | --- |
| Name a license, or confirm that the companion stays all-rights-reserved | `LICENSE`, `docs/authorship-and-license.md` | Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk | 2026-11-02 |
| Confirm author order against the two-author copyright line | same file. Komarchuk is in the repository and absent from the DOCX text | the same three authors | 2026-11-02 |
| Accept the Table 4.1 review copy for publication (Whitley location/value, Perm 0 location `1/i`, rotated lower bound `-65.536`, Xin-She Yang uniform noise) | `docs/manuscript-replacements.md`, `scripts/prepare_reviewed_manuscript.py` | handbook authors, then the editor | 2026-11-02 |
| Keep Appendix C and Appendix E as historical legacy-stream results, or schedule a Generator replacement | `docs/experiment-protocol.md`, `results/full_experiment_cost_estimate.json` (945000000 nominal evaluations, about 8.8–65.6 hours) | handbook authors | 2026-11-16 |
| Page-by-page visual acceptance of the print PDF | rendering note in `docs/release-readiness.md` | editor designated by the authors | 2026-11-09, or later if the PDF is not yet accepted |
| Tag a release and only then retarget book links from `/blob/main/` | no tag exists | Dmytro Komarchuk, after the rows above | no date until the no-go items close |

Incomplete rows stay open. A row does not authorize a license edit or an author-order edit by the maintainer alone.
