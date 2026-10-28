"""Apply paragraph-level edits to ``word/document.xml`` as Word tracked changes.

Input is JSON Lines. Each record names a paragraph by the ``idx`` that
``extract_paragraphs.py`` printed and says what should happen to it::

    {"idx": 312, "new": "…full replacement text…", "old": "…optional check…", "note": "why"}
    {"idx": 312, "op": "delete"}
    {"idx": 312, "op": "insert_after", "new": "…", "style": "a8"}
    {"idx": 312, "op": "set_style", "style": "1"}
    {"idx": 13149, "op": "delete_table"}
    {"idx": 156, "op": "join_next", "append": ". "}
    {"idx": 52, "op": "insert_toc_after", "heading": "Contents"}

``op`` defaults to ``replace``. A replace is diffed at word level against the
current text and written as ``w:del``/``w:ins`` runs that keep the formatting
of the run they came from, so the authors see a readable redline and can
accept or reject each change. ``old``, when given, must match the current
paragraph text after whitespace normalisation; otherwise the record is
rejected. Paragraphs that look like code, contain an embedded object or a
field are refused unless the record carries ``"allow_code": true`` /
``"allow_object": true`` / ``"allow_field": true``.

``delete`` marks every run and the paragraph mark deleted. ``insert_after``
adds a new paragraph (style copied from the target unless ``style`` is
given) whose runs and mark are marked inserted. ``set_style`` changes the
paragraph style and records the previous paragraph properties in a
``w:pPrChange``. ``delete_table`` marks every row of the table that contains
the paragraph deleted, together with every run in it. ``join_next`` marks
the paragraph mark deleted (so the paragraph merges into the next one when
accepted) after inserting ``append`` at its end. ``insert_toc_after`` adds a
heading paragraph and a ``TOC \\o "1-3" \\h \\z \\u`` field that Word fills in on
update, both marked inserted.

Every revision carries ``w:author`` (default ``Editorial (Claude)``), a UTC
``w:date`` and a ``w:id`` unique in the document. The script never touches
images, equations, or run properties.

Usage::

    python scripts/editorial/apply_tracked_edits.py manuscript_extract/unpacked/word/document.xml \
        edits.jsonl --out manuscript_extract/edited/word/document.xml [--author NAME] [--report report.json]
"""

from __future__ import annotations

import argparse
import copy
import difflib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editorial_docx import Paragraph, W, collect, paragraph_runs, paragraph_text, register_namespaces, write_document  # noqa: E402

XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
_TOKEN = re.compile(r"\s+|\w+|[^\w\s]")
_SKIP_RUN_CHILDREN = {f"{W}t", f"{W}tab", f"{W}br", f"{W}cr", f"{W}rPr"}

# Children of w:pPr in schema order; w:pPrChange must come last.
_PPR_ORDER = [
    "pStyle",
    "keepNext",
    "keepLines",
    "pageBreakBefore",
    "framePr",
    "widowControl",
    "numPr",
    "suppressLineNumbers",
    "pBdr",
    "shd",
    "tabs",
    "suppressAutoHyphens",
    "kinsoku",
    "wordWrap",
    "overflowPunct",
    "topLinePunct",
    "autoSpaceDE",
    "autoSpaceDN",
    "bidi",
    "adjustRightInd",
    "snapToGrid",
    "spacing",
    "ind",
    "contextualSpacing",
    "mirrorIndents",
    "suppressOverlap",
    "jc",
    "textDirection",
    "textAlignment",
    "textboxTightWrap",
    "outlineLvl",
    "divId",
    "cnfStyle",
    "rPr",
    "sectPr",
    "pPrChange",
]


@dataclass
class Revisions:
    author: str
    date: str
    next_id: int
    applied: list[dict] = field(default_factory=list)
    rejected: list[dict] = field(default_factory=list)

    def attrs(self) -> dict[str, str]:
        rid = self.next_id
        self.next_id += 1
        return {f"{W}id": str(rid), f"{W}author": self.author, f"{W}date": self.date}


def _normalise(text: str) -> str:
    return " ".join(text.split())


def _max_revision_id(root: ET.Element) -> int:
    best = 0
    for el in root.iter():
        value = el.get(f"{W}id")
        if value and value.isdigit():
            best = max(best, int(value))
    return best


def _text_children(text: str) -> list[ET.Element]:
    """``w:t`` / ``w:tab`` / ``w:br`` elements for a piece of text."""
    out: list[ET.Element] = []
    for part in re.split(r"([\t\n])", text):
        if part == "\t":
            out.append(ET.Element(f"{W}tab"))
        elif part == "\n":
            out.append(ET.Element(f"{W}br"))
        elif part:
            t = ET.SubElement(ET.Element("dummy"), f"{W}t")
            t.text = part
            t.set(XML_SPACE, "preserve")
            out.append(t)
    return out


def _make_run(template: ET.Element | None, text: str, deleted: bool) -> ET.Element:
    run = ET.Element(f"{W}r")
    if template is not None:
        rpr = template.find(f"{W}rPr")
        if rpr is not None:
            run.append(copy.deepcopy(rpr))
    for child in _text_children(text):
        if deleted and child.tag == f"{W}t":
            child.tag = f"{W}delText"
        run.append(child)
    return run


def _run_has_special(run: ET.Element) -> bool:
    return any(child.tag not in _SKIP_RUN_CHILDREN for child in run)


def _parent_map(root: ET.Element) -> dict[ET.Element, ET.Element]:
    return {child: parent for parent in root.iter() for child in parent}


def _run_text_only(run: ET.Element) -> str:
    parts = []
    for child in run:
        if child.tag == f"{W}t":
            parts.append(child.text or "")
        elif child.tag == f"{W}tab":
            parts.append("\t")
        elif child.tag in {f"{W}br", f"{W}cr"}:
            parts.append("\n")
    return "".join(parts)


def _guard(p: Paragraph, element: ET.Element, record: dict, rev: Revisions) -> str | None:
    if p.code_like and not record.get("allow_code"):
        return "paragraph looks like code; set allow_code to edit it"
    if p.has_object and not record.get("allow_object"):
        return "paragraph contains an embedded object; set allow_object to edit it"
    if element.find(f".//{W}fldChar") is not None and not record.get("allow_field"):
        return "paragraph contains a field; set allow_field to edit it"
    if element.find(f".//{W}ins") is not None or element.find(f".//{W}del") is not None:
        return "paragraph already carries tracked changes"
    if "old" in record and _normalise(record["old"]) != _normalise(p.text):
        return "old text does not match the current paragraph text"
    return None


def replace_paragraph(element: ET.Element, new_text: str, rev: Revisions, parents: dict) -> int:
    """Rewrite the paragraph's runs so that the visible text becomes ``new_text``.

    Returns the number of tracked segments written (deletions + insertions).
    """
    runs = paragraph_runs(element)
    old_text = "".join(_run_text_only(r) for r in runs)
    if old_text != paragraph_text(element):
        raise ValueError("runs inside w:ins/w:del or unsupported containers")
    old_tokens = _TOKEN.findall(old_text)
    new_tokens = _TOKEN.findall(new_text)
    matcher = difflib.SequenceMatcher(a=old_tokens, b=new_tokens, autojunk=False)
    offsets = [0]
    for tok in old_tokens:
        offsets.append(offsets[-1] + len(tok))

    deleted = [False] * len(old_text)
    inserts: dict[int, list[str]] = {}
    changed = False
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        changed = True
        a, b = offsets[i1], offsets[i2]
        for k in range(a, b):
            deleted[k] = True
        if j2 > j1:
            # Insertions sit right after the text they replace.
            inserts.setdefault(b, []).append("".join(new_tokens[j1:j2]))
    if not changed:
        return 0

    def ins_elements(template: ET.Element | None, offset: int) -> list[ET.Element]:
        out = []
        for text in inserts.pop(offset, []):
            wrapper = ET.Element(f"{W}ins", rev.attrs())
            wrapper.append(_make_run(template, text, deleted=False))
            out.append(wrapper)
        return out

    segments = 0
    pos = 0
    last_text_run: ET.Element | None = None
    for run in runs:
        text = _run_text_only(run)
        if not text:
            continue  # object, field or empty run: left exactly where it is
        if _run_has_special(run):
            raise ValueError("run mixes text with a non-text child; refusing to split it")
        last_text_run = run
        run_start, run_end = pos, pos + len(text)
        new_elements: list[ET.Element] = []
        piece_start = run_start
        cursor = run_start
        while cursor < run_end:
            if cursor in inserts:
                if cursor > piece_start:
                    new_elements.append(_piece(run, text, piece_start, cursor, run_start, deleted, rev))
                    segments += deleted[piece_start]
                    piece_start = cursor
                inserts_here = ins_elements(run, cursor)
                new_elements.extend(inserts_here)
                segments += len(inserts_here)
            nxt = cursor + 1
            if nxt < run_end and deleted[nxt] == deleted[cursor] and nxt not in inserts:
                cursor = nxt
                continue
            new_elements.append(_piece(run, text, piece_start, nxt, run_start, deleted, rev))
            segments += deleted[piece_start]
            piece_start = nxt
            cursor = nxt
        parent = parents[run]
        index = list(parent).index(run)
        parent.remove(run)
        for offset, el in enumerate(new_elements):
            parent.insert(index + offset, el)
        pos = run_end
    tail = ins_elements(last_text_run, len(old_text))
    if tail:
        anchor = last_text_run
        parent = parents[anchor] if anchor is not None else element
        if anchor is not None:
            # The anchor run was replaced by its pieces; append after the last piece.
            siblings = list(parent)
            index = len(siblings)
            for i, el in enumerate(siblings):
                if el is anchor or (el.tag == f"{W}del" and anchor in list(el)):
                    index = i + 1
            # anchor itself was removed; fall back to the end of its parent.
            index = min(index, len(siblings))
            for offset, el in enumerate(tail):
                parent.insert(index + offset, el)
        else:
            element.extend(tail)
        segments += len(tail)
    if inserts:
        raise ValueError(f"unplaced insertions at offsets {sorted(inserts)}")
    return segments


def _piece(run: ET.Element, text: str, start: int, end: int, run_start: int, deleted: list[bool], rev: Revisions) -> ET.Element:
    piece_text = text[start - run_start : end - run_start]
    is_deleted = deleted[start]
    piece_run = _make_run(run, piece_text, deleted=is_deleted)
    if not is_deleted:
        return piece_run
    wrapper = ET.Element(f"{W}del", rev.attrs())
    wrapper.append(piece_run)
    return wrapper


def _ppr(element: ET.Element) -> ET.Element:
    ppr = element.find(f"{W}pPr")
    if ppr is None:
        ppr = ET.Element(f"{W}pPr")
        element.insert(0, ppr)
    return ppr


def _ppr_rpr(element: ET.Element) -> ET.Element:
    ppr = _ppr(element)
    rpr = ppr.find(f"{W}rPr")
    if rpr is None:
        rpr = ET.Element(f"{W}rPr")
        # rPr goes before sectPr/pPrChange, after everything else.
        insert_at = len(ppr)
        for i, child in enumerate(ppr):
            if child.tag in {f"{W}sectPr", f"{W}pPrChange"}:
                insert_at = i
                break
        ppr.insert(insert_at, rpr)
    return rpr


def delete_paragraph(element: ET.Element, rev: Revisions, parents: dict) -> int:
    count = 0
    for run in paragraph_runs(element):
        parent = parents[run]
        index = list(parent).index(run)
        for t in run.findall(f"{W}t"):
            t.tag = f"{W}delText"
        wrapper = ET.Element(f"{W}del", rev.attrs())
        parent.remove(run)
        wrapper.append(run)
        parent.insert(index, wrapper)
        count += 1
    rpr = _ppr_rpr(element)
    rpr.insert(0, ET.Element(f"{W}del", rev.attrs()))
    return count + 1


def insert_paragraph_after(element: ET.Element, text: str, style: str | None, rev: Revisions, parents: dict) -> int:
    new_p = ET.Element(f"{W}p")
    old_ppr = element.find(f"{W}pPr")
    if old_ppr is not None:
        ppr = copy.deepcopy(old_ppr)
        for tag in (f"{W}sectPr", f"{W}pPrChange", f"{W}rPr"):
            for child in ppr.findall(tag):
                ppr.remove(child)
        new_p.append(ppr)
    ppr = _ppr(new_p)
    if style is not None:
        existing = ppr.find(f"{W}pStyle")
        if existing is None:
            ppr.insert(0, ET.Element(f"{W}pStyle", {f"{W}val": style}))
        else:
            existing.set(f"{W}val", style)
    rpr = _ppr_rpr(new_p)
    rpr.insert(0, ET.Element(f"{W}ins", rev.attrs()))
    template_runs = paragraph_runs(element)
    template = template_runs[0] if template_runs else None
    wrapper = ET.Element(f"{W}ins", rev.attrs())
    wrapper.append(_make_run(template, text, deleted=False))
    new_p.append(wrapper)
    parent = parents[element]
    parent.insert(list(parent).index(element) + 1, new_p)
    return 1


def join_next(element: ET.Element, append: str, rev: Revisions, parents: dict) -> int:
    count = 0
    if append:
        runs = paragraph_runs(element)
        template = runs[-1] if runs else None
        wrapper = ET.Element(f"{W}ins", rev.attrs())
        wrapper.append(_make_run(template, append, deleted=False))
        element.append(wrapper)
        count += 1
    rpr = _ppr_rpr(element)
    rpr.insert(0, ET.Element(f"{W}del", rev.attrs()))
    return count + 1


def _field_run(kind: str) -> ET.Element:
    run = ET.Element(f"{W}r")
    ET.SubElement(run, f"{W}fldChar", {f"{W}fldCharType": kind})
    return run


def insert_toc_after(element: ET.Element, heading: str, rev: Revisions, parents: dict) -> int:
    parent = parents[element]
    at = list(parent).index(element) + 1
    count = 0
    if heading:
        head = ET.Element(f"{W}p")
        ppr = ET.SubElement(head, f"{W}pPr")
        ET.SubElement(ppr, f"{W}pStyle", {f"{W}val": "ad"})  # Title style: not collected by the TOC
        rpr = ET.SubElement(ppr, f"{W}rPr")
        rpr.insert(0, ET.Element(f"{W}del", rev.attrs()))  # placeholder, replaced below
        rpr.remove(rpr[0])
        rpr.insert(0, ET.Element(f"{W}ins", rev.attrs()))
        wrapper = ET.SubElement(head, f"{W}ins", rev.attrs())
        wrapper.append(_make_run(None, heading, deleted=False))
        parent.insert(at, head)
        at += 1
        count += 1
    toc = ET.Element(f"{W}p")
    ppr = ET.SubElement(toc, f"{W}pPr")
    rpr = ET.SubElement(ppr, f"{W}rPr")
    rpr.insert(0, ET.Element(f"{W}ins", rev.attrs()))
    wrapper = ET.SubElement(toc, f"{W}ins", rev.attrs())
    wrapper.append(_field_run("begin"))
    instr = ET.Element(f"{W}r")
    it = ET.SubElement(instr, f"{W}instrText")
    it.set(XML_SPACE, "preserve")
    it.text = ' TOC \\o "1-3" \\h \\z \\u '
    wrapper.append(instr)
    wrapper.append(_field_run("separate"))
    wrapper.append(_make_run(None, "Table of contents: right-click here and choose Update Field (or press F9).", deleted=False))
    wrapper.append(_field_run("end"))
    parent.insert(at, toc)
    return count + 1


def set_style(element: ET.Element, style: str, rev: Revisions) -> int:
    ppr = _ppr(element)
    old_copy = copy.deepcopy(ppr)
    for tag in (f"{W}sectPr", f"{W}pPrChange", f"{W}rPr"):
        for child in old_copy.findall(tag):
            old_copy.remove(child)
    existing = ppr.find(f"{W}pStyle")
    if existing is None:
        ppr.insert(0, ET.Element(f"{W}pStyle", {f"{W}val": style}))
    else:
        existing.set(f"{W}val", style)
    change = ET.Element(f"{W}pPrChange", rev.attrs())
    change.append(old_copy)
    for child in ppr.findall(f"{W}pPrChange"):
        ppr.remove(child)
    ppr.append(change)
    return 1


def delete_table(element: ET.Element, rev: Revisions, parents: dict) -> int:
    node = element
    table = None
    while node in parents:
        node = parents[node]
        if node.tag == f"{W}tbl":
            table = node
            break
    if table is None:
        raise ValueError("paragraph is not inside a table")
    count = 0
    for row in table.findall(f"{W}tr"):
        trpr = row.find(f"{W}trPr")
        if trpr is None:
            trpr = ET.Element(f"{W}trPr")
            tblprex = row.find(f"{W}tblPrEx")
            row.insert(1 if tblprex is not None else 0, trpr)
        trpr.append(ET.Element(f"{W}del", rev.attrs()))
        for p in row.iter(f"{W}p"):
            count += delete_paragraph(p, rev, parents)
    return count


def apply(document_xml: Path, edits: list[dict], author: str, out: Path) -> Revisions:
    root_tag = register_namespaces(document_xml)
    tree, paragraphs, elements = collect(document_xml)
    root = tree.getroot()
    rev = Revisions(
        author=author,
        date=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        next_id=_max_revision_id(root) + 1,
    )
    by_idx = {p.idx: p for p in paragraphs}
    # Apply in descending idx order so inserted paragraphs do not shift later targets.
    ordered = sorted(enumerate(edits), key=lambda item: (-int(item[1]["idx"]), -item[0]))
    for position, record in ordered:
        idx = int(record["idx"])
        op = record.get("op", "replace")
        p = by_idx.get(idx)
        if p is None:
            rev.rejected.append({"line": position + 1, "idx": idx, "reason": "no such paragraph"})
            continue
        element = elements[idx]
        parents = _parent_map(root)
        try:
            if op == "replace":
                reason = _guard(p, element, record, rev)
                if reason:
                    rev.rejected.append({"line": position + 1, "idx": idx, "reason": reason})
                    continue
                if _normalise(record["new"]) == _normalise(p.text):
                    rev.rejected.append({"line": position + 1, "idx": idx, "reason": "no change"})
                    continue
                n = replace_paragraph(element, record["new"], rev, parents)
            elif op == "delete":
                n = delete_paragraph(element, rev, parents)
            elif op == "insert_after":
                n = insert_paragraph_after(element, record["new"], record.get("style"), rev, parents)
            elif op == "set_style":
                n = set_style(element, record["style"], rev)
            elif op == "delete_table":
                n = delete_table(element, rev, parents)
            elif op == "join_next":
                n = join_next(element, record.get("append", ""), rev, parents)
            elif op == "insert_toc_after":
                n = insert_toc_after(element, record.get("heading", "Contents"), rev, parents)
            else:
                raise ValueError(f"unknown op {op!r}")
        except ValueError as exc:
            rev.rejected.append({"line": position + 1, "idx": idx, "reason": str(exc)})
            continue
        rev.applied.append({"line": position + 1, "idx": idx, "op": op, "segments": n, "section": p.section})
    out.parent.mkdir(parents=True, exist_ok=True)
    write_document(tree, out, root_tag)
    return rev


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("document_xml", type=Path)
    parser.add_argument("edits", type=Path, nargs="+", help="JSON Lines edit files")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--author", default="Editorial (Claude)")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    edits: list[dict] = []
    for path in args.edits:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    edits.append(json.loads(line))
    rev = apply(args.document_xml, edits, args.author, args.out)
    summary = {
        "applied": len(rev.applied),
        "rejected": len(rev.rejected),
        "segments": sum(a["segments"] for a in rev.applied),
        "first_revision_id": rev.applied and min(a["idx"] for a in rev.applied),
    }
    if args.report:
        args.report.write_text(
            json.dumps({"summary": summary, "applied": rev.applied, "rejected": rev.rejected}, indent=2, ensure_ascii=False)
        )
    print(json.dumps(summary))
    for r in rev.rejected:
        print(f"rejected line {r['line']} ¶{r['idx']}: {r['reason']}", file=sys.stderr)
    return 0 if not rev.rejected else 2


if __name__ == "__main__":
    raise SystemExit(main())
