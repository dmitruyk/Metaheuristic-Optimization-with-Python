"""CITATION.cff stays a Citation File Format 1.2 record without invented identifiers."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_citation_cff_names_the_three_co_authors_and_invents_nothing():
    text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert text.startswith("cff-version: 1.2.0\n")
    assert "title: " in text
    assert "message: " in text
    assert "type: software" in text
    assert "type: book" in text
    assert "Algorithms, Engineering Applications, and Practical Examples" in text.split("preferred-citation:")[1]
    assert "Algorithms, Reproducible Experiments, and Engineering Applications" not in text
    assert text.split("preferred-citation:")[0].count("title:") == 1
    lowered = text.lower()
    assert "doi:" not in lowered
    assert "isbn:" not in lowered
    assert "license:" not in lowered
    assert "Do not describe it as MIT-licensed." in text
    software = text.split("preferred-citation:")[0]
    book = text.split("preferred-citation:")[1]
    for block in (software, book):
        romasevych = block.index("family-names: Romasevych")
        loveikin = block.index("family-names: Loveikin")
        komarchuk = block.index("family-names: Komarchuk")
        assert romasevych < loveikin < komarchuk
