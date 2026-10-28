"""Accept every tracked change in a DOCX without LibreOffice.

Standard-library counterpart of the docx skill's ``accept_changes.py``:
``w:del`` runs are removed, ``w:ins`` wrappers are unwrapped, property-change
records (``w:pPrChange``, ``w:rPrChange``, ``w:tblPrChange`` …) are dropped,
rows whose ``w:trPr`` carries ``w:del`` are removed (and an emptied table with
them), a paragraph whose mark is deleted is merged into the following
paragraph (the merged paragraph keeps the following paragraph's properties,
as Word does), and inserted paragraph marks lose their marker.

Usage::

    python scripts/editorial/accept_changes.py edited.docx clean.docx
"""

from __future__ import annotations

import argparse
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editorial_docx import W, register_namespaces, write_document  # noqa: E402

_CHANGE_RECORDS = {
    f"{W}pPrChange",
    f"{W}rPrChange",
    f"{W}tblPrChange",
    f"{W}tblGridChange",
    f"{W}trPrChange",
    f"{W}tcPrChange",
    f"{W}sectPrChange",
    f"{W}numberingChange",
}


def _parents(root: ET.Element) -> dict[ET.Element, ET.Element]:
    return {child: parent for parent in root.iter() for child in parent}


def accept(root: ET.Element) -> dict[str, int]:
    counts = {"deleted_runs": 0, "inserted_runs": 0, "deleted_rows": 0, "merged_paragraphs": 0}
    # 1. Deleted rows (before paragraphs, so their paragraphs vanish with them).
    for table in list(root.iter(f"{W}tbl")):
        for row in list(table.findall(f"{W}tr")):
            trpr = row.find(f"{W}trPr")
            if trpr is not None and trpr.find(f"{W}del") is not None:
                table.remove(row)
                counts["deleted_rows"] += 1
        if table.find(f"{W}tr") is None:
            parent = _parents(root)[table]
            parent.remove(table)
    # 2. Deleted runs and inserted wrappers.
    parents = _parents(root)
    for el in list(root.iter(f"{W}del")):
        parent = parents.get(el)
        if parent is None or parent.tag in {f"{W}rPr", f"{W}trPr"}:
            continue
        parent.remove(el)
        counts["deleted_runs"] += 1
    parents = _parents(root)
    for el in list(root.iter(f"{W}ins")):
        parent = parents.get(el)
        if parent is None or parent.tag == f"{W}rPr":
            continue
        index = list(parent).index(el)
        parent.remove(el)
        for offset, child in enumerate(list(el)):
            parent.insert(index + offset, child)
        counts["inserted_runs"] += 1
    # 3. Property-change records.
    parents = _parents(root)
    for el in list(root.iter()):
        if el.tag in _CHANGE_RECORDS and el in parents:
            parents[el].remove(el)
    # 4. Paragraph marks.
    for p in list(root.iter(f"{W}p")):
        rpr = p.find(f"{W}pPr/{W}rPr")
        if rpr is None:
            continue
        for marker in rpr.findall(f"{W}ins"):
            rpr.remove(marker)
        if rpr.find(f"{W}del") is None:
            continue
        rpr.remove(rpr.find(f"{W}del"))
        parents = _parents(root)
        parent = parents[p]
        siblings = list(parent)
        index = siblings.index(p)
        nxt = next((s for s in siblings[index + 1 :] if s.tag == f"{W}p"), None)
        if nxt is None:
            continue
        content = [c for c in p if c.tag != f"{W}pPr"]
        insert_at = 1 if (len(nxt) and nxt[0].tag == f"{W}pPr") else 0
        for offset, child in enumerate(content):
            nxt.insert(insert_at + offset, child)
        parent.remove(p)
        counts["merged_paragraphs"] += 1
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(args.source) as zf:
            zf.extractall(tmp_path)
        document = tmp_path / "word" / "document.xml"
        root_tag = register_namespaces(document)
        tree = ET.parse(document)
        counts = accept(tree.getroot())
        write_document(tree, document, root_tag)
        if args.destination.exists():
            args.destination.unlink()
        with zipfile.ZipFile(args.destination, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(tmp_path.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(tmp_path).as_posix())
    print(counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
