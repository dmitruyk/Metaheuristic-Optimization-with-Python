# ruff: noqa: E501
"""Fixture tests for the editorial scripts (extract + apply tracked edits).

The real manuscript is not in git, so these tests build a tiny WordprocessingML
body with the same constructs the manuscript uses: a plain paragraph, a
two-column listing table (code left, explanation right), a run with an
embedded object, and a hyperlink.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts" / "editorial"
sys.path.insert(0, str(SCRIPTS))

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"

DOCUMENT = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W_NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<w:body>
<w:p><w:pPr><w:pStyle w:val="a8"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">Install </w:t></w:r><w:r><w:t>Python 3.11 or newer and clone the companion repository.</w:t></w:r></w:p>
<w:p><w:r><w:t>Chapter 2</w:t></w:r></w:p>
<w:p><w:r><w:t>The matrix Position is generated, which contains the particles.</w:t></w:r></w:p>
<w:tbl><w:tblPr/><w:tblGrid><w:gridCol/><w:gridCol/></w:tblGrid>
<w:tr><w:tc><w:p><w:r><w:t>w, c1, c2 = 0.72, 1.19, 1.19</w:t></w:r></w:p></w:tc>
<w:tc><w:p><w:r><w:t>Setting the values of the inertia coefficient w.</w:t></w:r></w:p></w:tc></w:tr>
</w:tbl>
<w:p><w:r><w:t xml:space="preserve">Equation </w:t></w:r><w:r><w:object><v:shape/></w:object></w:r><w:r><w:t xml:space="preserve"> gives the velocity.</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">See </w:t></w:r><w:hyperlink r:id="rId9"><w:r><w:rPr><w:u w:val="single"/></w:rPr><w:t>the repository</w:t></w:r></w:hyperlink><w:r><w:t xml:space="preserve"> for code.</w:t></w:r></w:p>
<w:p><w:r><w:t>Glossary</w:t></w:r></w:p>
<w:tbl><w:tblPr/><w:tblGrid><w:gridCol/><w:gridCol/></w:tblGrid>
<w:tr><w:tc><w:p><w:r><w:t>Chapter 1. THE PSO METHOD</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>5</w:t></w:r></w:p></w:tc></w:tr>
</w:tbl>
<w:sectPr/>
</w:body></w:document>
"""


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module  # dataclasses resolve annotations through sys.modules
    spec.loader.exec_module(module)
    return module


def _visible(p: ET.Element) -> str:
    """Text as Word shows it with all changes accepted: w:t only, inside w:del excluded."""
    out = []
    for el in p.iter():
        if el.tag == f"{W}delText":
            continue
        if el.tag == f"{W}t":
            out.append(el.text or "")
    return "".join(out)


def _original(p: ET.Element) -> str:
    """Text with all changes rejected: w:delText kept, w:ins excluded."""
    out = []
    skip = set()
    for ins in p.iter(f"{W}ins"):
        for el in ins.iter():
            skip.add(el)
    for el in p.iter():
        if el in skip:
            continue
        if el.tag in {f"{W}t", f"{W}delText"}:
            out.append(el.text or "")
    return "".join(out)


def test_extract_flags_and_sections(tmp_path: Path) -> None:
    doc = tmp_path / "document.xml"
    doc.write_text(DOCUMENT, encoding="utf-8")
    editorial_docx = _load("editorial_docx")
    _, paragraphs, _ = editorial_docx.collect(doc)
    by_text = {p.text: p for p in paragraphs}
    assert by_text["w, c1, c2 = 0.72, 1.19, 1.19"].code_like
    assert by_text["w, c1, c2 = 0.72, 1.19, 1.19"].cell_col == 0
    assert not by_text["Setting the values of the inertia coefficient w."].code_like
    assert by_text["Equation  gives the velocity."].has_object
    assert by_text["Chapter 2"].section == "02-chapter-2"
    assert by_text["Chapter 1. THE PSO METHOD"].section == "99-end-toc"
    assert by_text["Glossary"].section == "20-glossary"


def test_apply_tracked_edits_round_trip(tmp_path: Path) -> None:
    doc = tmp_path / "document.xml"
    doc.write_text(DOCUMENT, encoding="utf-8")
    apply_mod = _load("apply_tracked_edits")
    edits = [
        {
            "idx": 0,
            "old": "Install Python 3.11 or newer and clone the companion repository.",
            "new": "Install Python 3.12 and clone the companion repository.",
            "note": "version",
        },
        {"idx": 2, "new": "The position matrix, Position, is generated; it holds one row per particle."},
        {"idx": 3, "new": "w, c1, c2 = 0.5, 1, 1"},  # code cell: must be refused
        {"idx": 4, "new": "Sets the inertia weight w."},
        {"idx": 5, "new": "Equation  gives the velocity update.", "allow_object": True},
        {"idx": 6, "new": "See the repository for the tested code."},
        {"idx": 1, "op": "set_style", "style": "1"},
        {"idx": 1, "op": "insert_after", "new": "This chapter introduces DE.", "style": "a8"},
        {"idx": 8, "op": "delete_table"},
        {"idx": 1, "op": "join_next", "append": ". "},
        {"idx": 0, "op": "insert_toc_after", "heading": "Contents"},
    ]
    out = tmp_path / "out" / "document.xml"
    rev = apply_mod.apply(doc, edits, "Editorial (Claude)", out)
    assert [r["idx"] for r in rev.rejected] == [3]
    assert "allow_code" in rev.rejected[0]["reason"]
    assert len(rev.applied) == 10

    root = ET.parse(out).getroot()
    body = root.find(f"{W}body")
    paragraphs = list(body.iter(f"{W}p"))
    # TOC heading + field inserted right after paragraph 0; drop them for the index checks below.
    assert _visible(paragraphs[1]) == "Contents"
    assert paragraphs[2].find(f".//{W}instrText").text.strip().startswith("TOC")
    assert paragraphs[2].find(f"{W}pPr/{W}rPr/{W}ins") is not None
    del paragraphs[1:3]
    # Accepted view
    assert _visible(paragraphs[0]) == "Install Python 3.12 and clone the companion repository."
    assert _visible(paragraphs[3]) == "The position matrix, Position, is generated; it holds one row per particle."
    assert _visible(paragraphs[6]) == "Equation  gives the velocity update."
    assert _visible(paragraphs[7]) == "See the repository for the tested code."
    # Rejected view equals the original text
    assert _original(paragraphs[0]) == "Install Python 3.11 or newer and clone the companion repository."
    assert _original(paragraphs[3]) == "The matrix Position is generated, which contains the particles."
    assert _original(paragraphs[7]) == "See the repository for code."
    # Formatting of the touched run is kept (bold on the first run).
    first_runs = paragraphs[0].findall(f"{W}r")
    assert first_runs[0].find(f"{W}rPr/{W}b") is not None
    # Object run survives untouched.
    assert paragraphs[6].find(f".//{W}object") is not None
    # Hyperlink run keeps its underline and stays inside the hyperlink.
    link = paragraphs[7].find(f"{W}hyperlink")
    assert link is not None and link.find(f".//{W}u") is not None
    # Inserted paragraph: marked inserted, placed after 'Chapter 2', style set.
    inserted = paragraphs[2]
    assert _visible(inserted) == "This chapter introduces DE."
    assert inserted.find(f"{W}pPr/{W}rPr/{W}ins") is not None
    assert inserted.find(f"{W}pPr/{W}pStyle").get(f"{W}val") == "a8"
    # Style change recorded with the previous properties.
    heading = paragraphs[1]
    assert heading.find(f"{W}pPr/{W}pStyle").get(f"{W}val") == "1"
    assert heading.find(f"{W}pPr/{W}pPrChange") is not None
    # join_next: appended text inserted, paragraph mark deleted.
    assert _visible(heading) == "Chapter 2. "
    assert heading.find(f"{W}pPr/{W}rPr/{W}del") is not None
    # Table deletion: row marked deleted, cell text in delText.
    tables = body.findall(f"{W}tbl")
    assert tables[1].find(f"{W}tr/{W}trPr/{W}del") is not None
    assert tables[1].find(f".//{W}delText").text == "Chapter 1. THE PSO METHOD"
    # Every revision has an author, a date and a unique id.
    ids = [el.get(f"{W}id") for el in root.iter() if el.tag in {f"{W}ins", f"{W}del", f"{W}pPrChange"}]
    assert len(ids) == len(set(ids)) and all(ids)
    for el in root.iter():
        if el.tag in {f"{W}ins", f"{W}del", f"{W}pPrChange"}:
            assert el.get(f"{W}author") == "Editorial (Claude)"
            assert el.get(f"{W}date", "").endswith("Z")


def test_apply_rejects_mismatched_old_text(tmp_path: Path) -> None:
    doc = tmp_path / "document.xml"
    doc.write_text(DOCUMENT, encoding="utf-8")
    apply_mod = _load("apply_tracked_edits")
    out = tmp_path / "out.xml"
    rev = apply_mod.apply(doc, [{"idx": 2, "old": "Something else.", "new": "X."}], "E", out)
    assert rev.applied == [] and "old text" in rev.rejected[0]["reason"]
    report = json.loads(json.dumps({"applied": rev.applied, "rejected": rev.rejected}))
    assert report["rejected"][0]["idx"] == 2


def test_accept_changes_matches_visible_text(tmp_path: Path) -> None:
    doc = tmp_path / "document.xml"
    doc.write_text(DOCUMENT, encoding="utf-8")
    apply_mod = _load("apply_tracked_edits")
    accept_mod = _load("accept_changes")
    edits = [
        {"idx": 0, "new": "Install Python 3.12 and clone the companion repository."},
        {"idx": 1, "op": "join_next", "append": ". "},
        {"idx": 1, "op": "set_style", "style": "1"},
        {"idx": 2, "new": "The position matrix is generated."},
        {"idx": 8, "op": "delete_table"},
        {"idx": 7, "op": "insert_after", "new": "New closing paragraph."},
    ]
    out = tmp_path / "out.xml"
    apply_mod.apply(doc, edits, "E", out)
    root = ET.parse(out).getroot()
    expected = [_visible(p) for p in root.find(f"{W}body").iter(f"{W}p")]
    counts = accept_mod.accept(root)
    body = root.find(f"{W}body")
    texts = ["".join(t.text or "" for t in p.iter(f"{W}t")) for p in body.iter(f"{W}p")]
    assert "Chapter 2. The matrix Position is generated, which contains the particles." not in texts
    assert "Chapter 2. The position matrix is generated." in texts
    assert "Install Python 3.12 and clone the companion repository." in texts
    assert "New closing paragraph." in texts
    assert len(body.findall(f"{W}tbl")) == 1  # the stale TOC table is gone
    assert counts["deleted_rows"] == 1 and counts["merged_paragraphs"] == 1
    assert root.find(f".//{W}ins") is None and root.find(f".//{W}del") is None
    assert root.find(f".//{W}pPrChange") is None
    # Every non-merged paragraph keeps its accepted text.
    for text in expected:
        if text and text != "Chapter 2. ":
            assert text in texts or any(text in t for t in texts)
