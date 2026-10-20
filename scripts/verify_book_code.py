"""Syntax-check the code tables extracted from the editorial DOCX.

The DOCX path is an argument because the manuscript is not stored in this
repository. Listings that are explanation tables or Jupyter magics are reported
and are not expected to parse as Python.
"""

from __future__ import annotations

import ast
import sys
import zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def paragraph_text(paragraph) -> str:
    parts = []
    for node in paragraph.iter():
        tag = node.tag.split("}")[-1]
        if tag == "t" and node.text:
            parts.append(node.text)
        elif tag == "tab":
            parts.append("\t")
        elif tag == "br" and node.get(f"{W}type") != "page":
            parts.append("\n")
    return "".join(parts)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/verify_book_code.py PATH/TO/manuscript.docx")
        return 2
    root = ET.fromstring(zipfile.ZipFile(sys.argv[1]).read("word/document.xml"))
    body = root.find(f"{W}body")
    parsed = 0
    failed = []
    for child in list(body):
        if child.tag.split("}")[-1] != "tbl":
            continue
        rows = []
        for tr in child.findall(f"{W}tr"):
            cells = []
            for tc in tr.findall(f"{W}tc"):
                cells.append("\n".join(paragraph_text(p) for p in tc.findall(f"{W}p")))
            rows.append(cells)
        if not rows:
            continue
        columns = max(len(row) for row in rows)
        if columns != 1:
            continue
        code = "\n".join(row[0] for row in rows)
        if any(line.lstrip().startswith("%") for line in code.splitlines()):
            failed.append(("jupyter-magic", code.splitlines()[0][:80]))
            continue
        if "def " not in code and "import " not in code:
            continue
        try:
            ast.parse(code)
        except SyntaxError as exc:
            failed.append((f"line {exc.lineno}: {exc.msg}", code.splitlines()[0][:80]))
            continue
        parsed += 1
    print(f"parsed one-column listings: {parsed}")
    print(f"not parsed: {len(failed)}")
    for reason, first in failed:
        print(f"  {reason} | {first}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
