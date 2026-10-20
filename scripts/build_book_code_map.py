"""Build docs/book-code-map.md from the editorial DOCX.

Page numbers are rendered-page estimates: a paragraph increments the page by
max(lastRenderedPageBreak count, explicit page-break count). Word reports 346
pages; this counter finishes at 347. They are not the page numbers cited in
the implementation brief.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ROOT = Path(__file__).resolve().parents[1]


def paragraph_text(paragraph) -> tuple[str, int]:
    lr = br = 0
    parts = []
    for node in paragraph.iter():
        tag = node.tag.split("}")[-1]
        if tag == "lastRenderedPageBreak":
            lr += 1
        elif tag == "br" and node.get(f"{W}type") == "page":
            br += 1
        elif tag == "t" and node.text:
            parts.append(node.text)
        elif tag == "tab":
            parts.append(" ")
    return "".join(parts).strip(), max(lr, br)


def status_for_code(text: str) -> str:
    if text.lstrip().startswith("%"):
        return "not-applicable"
    if "clear_output" in text or "np.random.rand" in text or "np.random.seed" in text:
        return "corrected-with-erratum"
    markers = (
        "def ObjectiveFunction1a",
        "def ObjectiveFunction1b",
        "def ObjectiveFunction2",
        "def ObjectiveFunction3",
        "def MountainCarStep",
        "def ObjectiveFunction4a",
        "def ObjectiveFunction5",
        "def CartPoleStep",
        "12.3901",
        "def Ackley1Function",
        "# BENCHMARKS AND DOMAINS",
        "# OPTIMIZERS",
    )
    if any(marker in text for marker in markers):
        return "verified"
    if "def " in text or "import " in text:
        return "unverified"
    return "not-applicable"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/build_book_code_map.py MANUSCRIPT.docx")
    root = ET.fromstring(zipfile.ZipFile(sys.argv[1]).read("word/document.xml"))
    body = root.find(f"{W}body")
    page = 1
    rows = []
    figure_n = table_n = code_n = 0
    for child in list(body):
        tag = child.tag.split("}")[-1]
        if tag == "p":
            text, inc = paragraph_text(child)
            page += inc
            if text.startswith("Figure ") or text.startswith("Fig. ") or text.startswith("Table "):
                kind = "figure" if text.startswith("Fig") else "table"
                if kind == "figure":
                    figure_n += 1
                    ident = f"F{figure_n:03d}"
                else:
                    table_n += 1
                    ident = f"C{table_n:03d}"
                if "Appendix C" in text or "Appendix E" in text or "box" in text.lower():
                    status = "unverified"
                else:
                    status = "unverified"
                rows.append((ident, page, kind, status, text[:180].replace("|", "/")))
        elif tag == "tbl":
            inc_total = 0
            cell_text = []
            columns = 0
            for tr in child.findall(f"{W}tr"):
                cells = tr.findall(f"{W}tc")
                columns = max(columns, len(cells))
                for tc in cells:
                    bits = []
                    for p in tc.findall(f"{W}p"):
                        text, inc = paragraph_text(p)
                        inc_total += inc
                        if text:
                            bits.append(text)
                    cell_text.append(" ".join(bits))
            page += inc_total
            blob = "\n".join(cell_text)
            code_n += 1
            ident = f"T{code_n:03d}"
            first = next((line for line in blob.splitlines() if line.strip()), "")
            if columns >= 2 and cell_text and cell_text[0].strip() == "Code":
                status = "not-applicable"
                kind = "explanation-table"
            elif columns == 1 and ("def " in blob or "import " in blob or blob.lstrip().startswith("%") or "np." in blob):
                status = status_for_code(blob)
                kind = "code-listing"
            else:
                status = "unverified"
                kind = f"table-{columns}col"
            rows.append((ident, page, kind, status, first[:160].replace("|", "/")))
    lines = [
        "# Book code map",
        "",
        "Source file: `Metaheuristic_Optimization_with_Python_Editorial_Edition.docx`.",
        "Authors: Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk.",
        "",
        "Rendered-page estimates come from Word page-break markers. Word's document",
        "property says 346 pages; the counter used here ends at 347. The implementation",
        "brief's pages (p. 24, pp. 224–226, p. 231, pp. 289–298) do not match this file.",
        "In this DOCX the ten-variable worked value 12.3901 is on rendered page 21,",
        "Problem 1a is on rendered page 187, the cart-pole `penalty_terminal` line is",
        "on rendered page 203, and Appendix B begins on rendered page 272.",
        "",
        "Statuses: `verified` (executed and compared with a printed number, or parsed",
        "and covered by `tests/`), `corrected-with-erratum` (behavior preserved except",
        "for a documented change such as the random generator), `unverified` (present",
        "in the manuscript, not numerically matched), `not-applicable` (prose,",
        "explanation table, figure schematic, or Jupyter magic rather than a library function).",
        "",
        "No row is blank. Result plots in Appendices A, C, and E stay `unverified`:",
        "the full 100-run study was not repeated, and library figures are not substituted for the book's figures.",
        "",
        "| ID | Rendered page | Kind | Status | Repo path | First line or caption |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    path_for = {
        "verified": "see `src/metaopt/` and `tests/test_examples_smoke.py`",
        "corrected-with-erratum": "see `src/metaopt/` and `docs/errata.md`",
        "unverified": "not claimed to match a printed figure or table",
        "not-applicable": "no library object; explanation or non-Python content",
    }
    for ident, rendered, kind, status, preview in rows:
        lines.append(f"| {ident} | {rendered} | {kind} | {status} | {path_for[status]} | {preview} |")
    lines.append("")
    lines.append(f"Rows: {len(rows)}.")
    destination = ROOT / "docs" / "book-code-map.md"
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {destination} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
