# Licensing audit

Phase: Validation. Date: 2026-10-25. Base commit `c803af2` on `main`. Data source: this checkout, `LICENSE`, and the editorial DOCX named in `docs/authorship-and-license.md`. Execution: local inspection. Not paper trading and not live execution.

**Go / no-go: no-go for replacing `LICENSE` with the MIT License.**

Rationale: the only written software permission in the repository is Dmytro Komarchuk's approval on 19 October 2026 to create the companion repository. That sentence does not name MIT. The 2026-10-25 publication task proposes MIT and also says that agreement to collaborate and publish is not proof of authorization to release every source file under MIT. Stakeholders: Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk. This file does not speak for them and does not invent a grant.

## Findings

| Item | What was found | MIT applied? |
| --- | --- | --- |
| `LICENSE` | Names the three co-authors. Records repository-creation approval. Says no open-source license has been selected | No |
| Python under `src/`, `tests/`, `examples/`, `scripts/` | No third-party copyright header, SPDX line, or "copied from" notice. Implementations follow the manuscript's algorithms and cited formulas (including Jamil and Yang for benchmarks). The listings are derived from the book, whose copyright holders have not granted MIT in this repository | No |
| `notebooks/01`–`10` | Generated companion notebooks. Same derivation issue as the Python package | No |
| `docs/` | Editorial and reproducibility notes, including quotations and restatements of the manuscript. Not treated as MIT | No |
| `figures/generated/` | Script output, gitignored except `.gitkeep`. Not the book's illustrations. Unverified against printed figures | No |
| Manuscript DOCX | All rights reserved. Not stored in git. Review copy is local only | No. See `BOOK_LICENSE.md` |
| Images, datasets, cover art | No book illustrations, cover files, or datasets are tracked | Not applicable |
| Dependencies | NumPy, SciPy, Matplotlib, and the optional Jupyter, pandas, SymPy, pytest, and ruff packages are installed from their own projects. They are not vendored and are not relicensed here | Their upstream licenses stay with them |

## Authorization that is not in the repository

Permission to create the repository is not permission to redistribute the handbook, and it is not an MIT grant for the source files that restate the handbook. A later MIT release needs a written grant that names MIT and identifies who is licensing the software. That grant is not in `LICENSE`.

Canonical MIT text was read as the text that would be used if that grant existed: <https://choosealicense.com/licenses/mit/>. It was not copied into `LICENSE`.

## Next step

| Step | Owner | Target date | Status |
| --- | --- | --- | --- |
| Write a grant that names MIT, or confirm that the companion stays all-rights-reserved | Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk | 2026-11-02 | open |
