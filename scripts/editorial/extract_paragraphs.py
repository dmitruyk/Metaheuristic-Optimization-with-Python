"""Dump the manuscript's paragraphs for editorial review.

Writes ``paragraphs.jsonl`` (one record per paragraph: idx, style, in_table,
has_object, section, xml_hash, text) and one Markdown file per section under
``sections/``. The Markdown line format is::

    ¶<idx> [<style>|T<col>/<ncols>|O|C] <text>

``T0/2`` marks a table cell (column 0 of 2), ``O`` a paragraph with an embedded
object (equation image, figure), ``C`` a line that looks like code. Listings in
Chapters 1–5 are two-column tables: code on the left, explanation on the right.
Output goes under ``manuscript_extract/`` which is gitignored.

Usage::

    python scripts/editorial/extract_paragraphs.py manuscript_extract/unpacked/word/document.xml \
        --out manuscript_extract
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editorial_docx import CODE_STYLES, collect  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("document_xml", type=Path)
    parser.add_argument("--out", type=Path, default=Path("manuscript_extract"))
    args = parser.parse_args(argv)

    _, paragraphs, _ = collect(args.document_xml)
    args.out.mkdir(parents=True, exist_ok=True)
    sections_dir = args.out / "sections"
    sections_dir.mkdir(exist_ok=True)
    for old in sections_dir.glob("*.md"):
        old.unlink()

    with (args.out / "paragraphs.jsonl").open("w", encoding="utf-8") as fh:
        for p in paragraphs:
            fh.write(json.dumps(p.__dict__, ensure_ascii=False) + "\n")

    by_section: dict[str, list] = {}
    for p in paragraphs:
        by_section.setdefault(p.section, []).append(p)
    words = Counter()
    for name, items in by_section.items():
        with (sections_dir / f"{name}.md").open("w", encoding="utf-8") as fh:
            for p in items:
                if not p.text.strip() and not p.has_object:
                    continue
                flags = p.style or "-"
                if p.in_table:
                    flags += f"|T{p.cell_col}/{p.table_cols}"
                if p.has_object:
                    flags += "|O"
                if p.code_like:
                    flags += "|C"
                fh.write(f"¶{p.idx} [{flags}] {p.text}\n")
                if p.style not in CODE_STYLES and not p.in_table:
                    words[name] += len(p.text.split())
    print(f"{len(paragraphs)} paragraphs")
    for name in sorted(by_section):
        items = by_section[name]
        code = sum(1 for p in items if p.style in CODE_STYLES)
        table = sum(1 for p in items if p.in_table)
        objects = sum(1 for p in items if p.has_object)
        line = f"  {name:22s} paragraphs={len(items):5d} code={code:4d} table_cells={table:5d}"
        print(f"{line} objects={objects:4d} prose_words={words[name]:6d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
