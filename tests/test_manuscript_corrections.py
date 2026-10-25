"""Table-correction rules for the reviewed manuscript copy."""

from __future__ import annotations

from xml.etree import ElementTree as ET

import pytest
from scripts.prepare_reviewed_manuscript import (
    W,
    apply_editorial_xml,
    apply_revised_authors,
    apply_table_corrections,
    paragraph_text,
)


def _paragraph(text: str) -> ET.Element:
    paragraph = ET.Element(f"{W}p")
    run = ET.SubElement(paragraph, f"{W}r")
    node = ET.SubElement(run, f"{W}t")
    node.text = text
    return paragraph


def _table_paragraphs() -> list[ET.Element]:
    rows = [
        "Whitley",
        "",
        "0≤xi≤2",
        "0",
        "1",
        "Perm 0 d, β",
        "-D≤xi≤D",
        "i-1",
        "0",
        "-65.53≤xi",
        ", εi – random value normaly distributed on the range [0, 1]",
    ]
    return [_paragraph(text) for text in rows]


def test_table_corrections_match_the_appendix_b_definitions():
    paragraphs = _table_paragraphs()
    log = apply_table_corrections(paragraphs)
    texts = [paragraph_text(paragraph) for paragraph in paragraphs]
    assert texts[3:5] == ["1", "0"]
    assert texts[7] == "1/i"
    assert texts[9] == "-65.536≤xi"
    assert "uniformly distributed on [0, 1)" in texts[10]
    assert len(log) == 4


def test_editorial_xml_edits_preserve_the_surrounding_markup():
    xml = (
        "<w:document><w:t>Whitley</w:t><w:t>0≤</w:t><w:t>0</w:t><w:t>1</w:t>"
        "Perm 0 <w:t>d</w:t><w:t>i</w:t><w:t>-1</w:t>"
        "<w:t>-65.53≤</w:t>"
        "<w:t> – random value normaly distributed on the range [0, 1] </w:t>"
        "<w:t>Companion Code and Reproducibility</w:t></w:r></w:p></w:document>"
    )
    updated, log = apply_editorial_xml(xml)
    assert "<w:t>1</w:t><w:t>0</w:t>" in updated
    assert "<w:t>1/i</w:t><w:t></w:t>" in updated
    assert "-65.536≤" in updated
    assert "uniformly distributed on [0, 1)" in updated
    assert updated.count("rIdReviewLink") == 13
    assert updated.startswith("<w:document>")
    assert len(log) > 4


def test_revised_authors_are_added_without_stating_shares():
    xml = (
        '<w:p w:rsidR="1"><w:r><w:t>Viatcheslav Loveikin</w:t></w:r></w:p>'
        "<w:t>© Yuriy Romasevych, Viatcheslav Loveikin, 2026</w:t>"
        "<w:t>Romasevych Yu., Loveikin V., Makarets V.</w:t>"
    )
    updated, log = apply_revised_authors(xml)
    assert updated.count("<w:t>Dmytro Komarchuk</w:t>") == 1
    assert "© Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk, 2026" in updated
    assert "Makarets" in updated
    assert "equal" not in " ".join(log).lower()
    assert updated.startswith('<w:p w:rsidR="1">')


def test_a_missing_whitley_pair_is_not_silently_skipped():
    with pytest.raises(ValueError, match="Whitley"):
        apply_table_corrections([_paragraph("Whitley"), _paragraph("other")])
