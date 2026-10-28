"""Shared helpers for the editorial scripts: paragraph iteration and text.

The manuscript DOCX is all rights reserved and is never committed. These
helpers read ``word/document.xml`` with the standard library only, so that
``extract_paragraphs.py`` and ``apply_tracked_edits.py`` agree exactly on
paragraph numbering and on what the text of a paragraph is.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"

NAMESPACES = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "v": "urn:schemas-microsoft-com:vml",
    "o": "urn:schemas-microsoft-com:office:office",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
}

CODE_STYLES = {"MathematicaCellInput"}

# Section boundaries are detected from exact paragraph text.
_CHAPTER = re.compile(r"^Chapter ([1-7])$")
_APPENDIX = re.compile(r"^Appendix ([A-E])$")
_END_TOC = re.compile(r"^Chapter 1\. ")
_CODE_LINE = re.compile(
    r"^\s*(import |from \S+ import|def |class |for .* in .*:|while .*:|if .*:|elif .*:|else:|try:|except|"
    r"return\b|with .*:|#|@|\w[\w.\[\], ]*\s*=\s*\S|print\(|np\.|plt\.|\)$|\]$|\}$|\w[\w.]*\(.*\)\s*$|break$|continue$|pass$)"
)


def looks_like_code(text: str) -> bool:
    """Heuristic for a code line in a listing cell (no sentence punctuation, code tokens)."""
    stripped = text.strip()
    if not stripped:
        return False
    if _CODE_LINE.match(stripped):
        return True
    return stripped.endswith((":", "(", ",", "\\")) and not stripped.endswith(". ")


@dataclass
class Paragraph:
    idx: int
    style: str
    in_table: bool
    has_object: bool
    text: str
    section: str
    xml_hash: str
    cell_col: int = -1
    table_cols: int = 0
    code_like: bool = False


def register_namespaces() -> None:
    for prefix, uri in NAMESPACES.items():
        ET.register_namespace(prefix, uri)


def run_text(run: ET.Element) -> str:
    """Text of one ``w:r``: ``w:t`` as is, ``w:tab`` as a tab, ``w:br`` as a newline."""
    parts: list[str] = []
    for child in run:
        if child.tag == f"{W}t":
            parts.append(child.text or "")
        elif child.tag == f"{W}tab":
            parts.append("\t")
        elif child.tag in {f"{W}br", f"{W}cr"}:
            parts.append("\n")
    return "".join(parts)


def paragraph_text(paragraph: ET.Element) -> str:
    """Visible text of a paragraph. Deleted (``w:del``) text is not included."""
    parts: list[str] = []
    for element in paragraph.iter():
        if element.tag == f"{W}r":
            parts.append(run_text(element))
    return "".join(parts)


def paragraph_runs(paragraph: ET.Element) -> list[ET.Element]:
    """Direct and hyperlink-nested runs, in document order (not inside w:del/w:ins)."""
    runs: list[ET.Element] = []
    for child in paragraph:
        if child.tag == f"{W}r":
            runs.append(child)
        elif child.tag in {f"{W}hyperlink", f"{W}smartTag", f"{W}sdt"}:
            runs.extend(paragraph_runs(child))
    return runs


def iter_paragraphs(root: ET.Element) -> list[ET.Element]:
    """Every ``w:p`` in the body, in document order, including table cells."""
    body = root.find(f"{W}body")
    if body is None:
        raise ValueError("document.xml has no w:body")
    return list(body.iter(f"{W}p"))


def _ancestry(root: ET.Element) -> dict[ET.Element, ET.Element]:
    return {child: parent for parent in root.iter() for child in parent}


def collect(document_xml: Path) -> tuple[ET.ElementTree, list[Paragraph], list[ET.Element]]:
    register_namespaces()
    tree = ET.parse(document_xml)
    root = tree.getroot()
    parents = _ancestry(root)
    elements = iter_paragraphs(root)
    paragraphs: list[Paragraph] = []
    section = "00-front-matter"
    after_glossary = False
    for idx, p in enumerate(elements):
        text = paragraph_text(p)
        style_el = p.find(f"{W}pPr/{W}pStyle")
        style = style_el.get(f"{W}val", "") if style_el is not None else ""
        in_table = False
        cell_col, table_cols = -1, 0
        node = p
        while node in parents:
            node = parents[node]
            if node.tag == f"{W}tc":
                in_table = True
                row = parents[node]
                cells = [c for c in row if c.tag == f"{W}tc"]
                cell_col = cells.index(node)
                table_cols = len(cells)
                break
        has_object = any(el.tag in {f"{W}object", f"{W}drawing", f"{M}oMath", f"{M}oMathPara", f"{W}pict"} for el in p.iter())
        stripped = text.strip()
        if not in_table:
            m = _CHAPTER.match(stripped)
            if m and not after_glossary:
                section = f"0{m.group(1)}-chapter-{m.group(1)}"
            m = _APPENDIX.match(stripped)
            if m:
                section = f"1{ord(m.group(1)) - 64}-appendix-{m.group(1).lower()}"
            if stripped == "Glossary" and not after_glossary:
                section = "20-glossary"
                after_glossary = True
        if after_glossary and _END_TOC.match(stripped):
            section = "99-end-toc"
        code_like = style in CODE_STYLES or (in_table and looks_like_code(text))
        xml_hash = hashlib.sha1(ET.tostring(p, encoding="utf-8")).hexdigest()[:12]
        paragraphs.append(Paragraph(idx, style, in_table, has_object, text, section, xml_hash, cell_col, table_cols, code_like))
    return tree, paragraphs, elements
