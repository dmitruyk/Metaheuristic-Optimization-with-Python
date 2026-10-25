# Local manuscript copies

Phase: Validation. Date: 2026-10-20.

`*.docx` and `*.pdf` in this directory are gitignored. The handbook says all rights are reserved, and `LICENSE` does not grant redistribution, so the review binary is not committed.

Generate the review copy from the editorial DOCX:

```bash
python scripts/prepare_reviewed_manuscript.py \
  --source "$HOME/Downloads/Metaheuristic_Optimization_with_Python_Editorial_Edition.docx" \
  --destination manuscript/Metaheuristic_Optimization_with_Python_reviewed.docx
```

The script changes four Table 4.1 text cells, inserts companion links, and adds Dmytro Komarchuk after Viatcheslav Loveikin on the title page and the copyright line. That line does not state copyright shares. It edits the WordprocessingML as text so the `w:` prefixes stay as Word wrote them. It does not change equation images and it does not apply the MIT License. Details are in `docs/manuscript-replacements.md`.

On 2026-10-20, LibreOffice 6.3.4.2 on this Mac (`macOS-26.6.2`) aborted with signal 6 before opening the editorial source and before opening the review copy. No PDF was produced. A later visual pass needs a converter that actually loads the file.
