"""Apply evidence-backed text corrections to a local copy of the editorial DOCX.

The manuscript is all rights reserved. This script writes a review copy under
``manuscript/`` and does not put that binary in git. It does not change
equations that are images, authorship, or the license.

Corrections, each checked against the paragraph sequence before it is applied:

- Whitley, Table 4.1: location ``0`` and value ``1`` become location ``1`` and
  value ``0``. Appendix B and Jamil and Yang have the minimum 0 at the all-ones
  vector. The formula is not rewritten.
- Perm 0, d, β location ``i-1`` becomes ``1/i``. The Appendix B formula is 0
  at ``x_i = 1/i`` and is not 0 at ``i-1``.
- Rotated hyper-ellipsoid lower endpoint ``-65.53`` becomes ``-65.536``,
  matching the upper endpoint and Appendix B.
- Xin-She Yang noise text ``normaly distributed on the range [0, 1]`` becomes
  uniform on ``[0, 1)``, matching ``np.random.random`` in Appendix B.

A short companion-code block with repository links is inserted after the
heading ``Companion Code and Reproducibility``. Links use ``/blob/main/``
because no release tag exists.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
XMLNS = "{http://www.w3.org/2000/xmlns/}"

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path.home() / "Downloads" / "Metaheuristic_Optimization_with_Python_Editorial_Edition.docx"
DEFAULT_DESTINATION = ROOT / "manuscript" / "Metaheuristic_Optimization_with_Python_reviewed.docx"
REPO = "https://github.com/dmitruyk/Metaheuristic-Optimization-with-Python/blob/main"

COMPANION_LINKS = [
    ("Chapter 1. PSO and its variants", f"{REPO}/notebooks/01_particle_swarm.ipynb"),
    ("Chapter 2. Differential Evolution and SADE", f"{REPO}/notebooks/02_differential_evolution.ipynb"),
    ("Chapter 3. Grey Wolf Optimizer", f"{REPO}/notebooks/03_grey_wolf_optimizer.ipynb"),
    ("Chapter 4. Benchmark functions", f"{REPO}/notebooks/04_benchmarks.ipynb"),
    ("Chapter 5. Statistical comparisons", f"{REPO}/notebooks/05_fair_comparisons.ipynb"),
    ("Chapter 6. PID, robot, crane, and cart-pole examples", f"{REPO}/notebooks/06_pid_tuning.ipynb"),
    ("Chapter 6. Robot path example", f"{REPO}/notebooks/07_robot_path_planning.ipynb"),
    ("Chapter 6. Crane example", f"{REPO}/notebooks/08_crane_control.ipynb"),
    ("Chapter 6. Cart-pole example", f"{REPO}/notebooks/09_cart_pole.ipynb"),
    ("Chapter 7. Engineering design problems", f"{REPO}/notebooks/10_engineering_design.ipynb"),
    ("Appendix B. Benchmark implementations", f"{REPO}/src/metaopt/benchmarks.py"),
    ("Appendix C. Reproduction status and protocol", f"{REPO}/docs/experiment-protocol.md"),
    ("Appendix E. Timing protocol", f"{REPO}/docs/reproducibility.md"),
]


def _register_namespaces(root: ET.Element) -> None:
    for key, value in root.attrib.items():
        if key.startswith(XMLNS):
            ET.register_namespace(key[len(XMLNS) :], value)
    ET.register_namespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
    ET.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join((node.text or "") for node in paragraph.iter(f"{W}t")).strip()


def set_paragraph_text(paragraph: ET.Element, text: str) -> None:
    nodes = list(paragraph.iter(f"{W}t"))
    if not nodes:
        raise ValueError("paragraph has no text node")
    nodes[0].text = text
    for extra in nodes[1:]:
        extra.text = ""


def _nonempty_from(texts: list[str], start: int, count: int) -> list[int]:
    found = []
    for index in range(start, len(texts)):
        if texts[index]:
            found.append(index)
            if len(found) == count:
                break
    return found


def apply_table_corrections(paragraphs: list[ET.Element]) -> list[str]:
    """Return a log of edits. Raise if a required sequence is missing or ambiguous.

    Empty paragraphs between table cells are skipped. The Whitley row in the
    editorial DOCX has one.
    """

    texts = [paragraph_text(paragraph) for paragraph in paragraphs]
    log = []

    whitley = []
    for index, text in enumerate(texts):
        if text != "Whitley":
            continue
        window = _nonempty_from(texts, index, 4)
        if len(window) == 4 and [texts[item] for item in window[1:]] == ["0≤xi≤2", "0", "1"]:
            whitley.append(window)
    if len(whitley) != 1:
        raise ValueError(f"expected one Whitley location/value pair, found {len(whitley)}")
    _name, _domain, location, value = whitley[0]
    set_paragraph_text(paragraphs[location], "1")
    set_paragraph_text(paragraphs[value], "0")
    log.append("Table 4.1 Whitley location 0 -> 1 and value 1 -> 0")

    perm = []
    for index, text in enumerate(texts):
        if text != "Perm 0 d, β":
            continue
        window = _nonempty_from(texts, index, 4)
        if len(window) == 4 and [texts[item] for item in window[1:]] == ["-D≤xi≤D", "i-1", "0"]:
            perm.append(window)
    if len(perm) != 1:
        raise ValueError(f"expected one Perm 0 location cell, found {len(perm)}")
    set_paragraph_text(paragraphs[perm[0][2]], "1/i")
    log.append("Table 4.1 Perm 0, d, β location i-1 -> 1/i")

    rotated = [index for index, text in enumerate(texts) if text == "-65.53≤xi"]
    if len(rotated) != 1:
        raise ValueError(f"expected one rotated-hyper-ellipsoid lower bound, found {len(rotated)}")
    set_paragraph_text(paragraphs[rotated[0]], "-65.536≤xi")
    log.append("Table 4.1 rotated hyper-ellipsoid lower bound -65.53 -> -65.536")

    noise = [index for index, text in enumerate(texts) if "normaly distributed on the range [0, 1]" in text]
    if len(noise) != 1:
        raise ValueError(f"expected one Xin-She Yang noise sentence, found {len(noise)}")
    updated = texts[noise[0]].replace(
        "normaly distributed on the range [0, 1]",
        "uniformly distributed on [0, 1)",
    )
    set_paragraph_text(paragraphs[noise[0]], updated)
    log.append("Table 4.1 Xin-She Yang noise described as uniform on [0, 1)")
    return log


def _hyperlink_paragraph(text: str, relationship_id: str) -> ET.Element:
    paragraph = ET.Element(f"{W}p")
    hyperlink = ET.SubElement(paragraph, f"{W}hyperlink", {f"{R}id": relationship_id})
    run = ET.SubElement(hyperlink, f"{W}r")
    properties = ET.SubElement(run, f"{W}rPr")
    ET.SubElement(properties, f"{W}rStyle", {f"{W}val": "Hyperlink"})
    node = ET.SubElement(run, f"{W}t")
    node.text = text
    return paragraph


def _text_paragraph(text: str) -> ET.Element:
    paragraph = ET.Element(f"{W}p")
    run = ET.SubElement(paragraph, f"{W}r")
    node = ET.SubElement(run, f"{W}t")
    node.text = text
    return paragraph


def _replace_once(xml: str, old: str, new: str, label: str) -> str:
    count = xml.count(old)
    if count != 1:
        raise ValueError(f"{label}: expected 1 occurrence of {old!r}, found {count}")
    return xml.replace(old, new, 1)


def apply_editorial_xml(xml: str) -> tuple[str, list[str]]:
    """Edit the editorial document.xml without rewriting namespace prefixes.

    ElementTree serialization renames prefixes, and LibreOffice then refuses
    the package. These replacements stay inside existing ``w:t`` nodes or
    insert sibling paragraphs as text.
    """

    log = []
    marker = ">Whitley</w:t>"
    start = xml.find(marker)
    if start < 0 or "<w:t>0≤</w:t>" not in xml[start : start + 8000]:
        raise ValueError("Whitley table row was not found")
    head, tail = xml[:start], xml[start:]
    location = tail.find("<w:t>0</w:t>")
    value = tail.find("<w:t>1</w:t>", location + 1)
    if location < 0 or value < 0 or value > 8000:
        raise ValueError("Whitley location and value cells were not found")
    tail = tail[:location] + "<w:t>1</w:t>" + tail[location + len("<w:t>0</w:t>") :]
    # The value cell was `<w:t>1</w:t>`. Replacing the earlier location shifted nothing
    # before `value` because the two tags have the same length.
    value = tail.find("<w:t>1</w:t>", location + len("<w:t>1</w:t>"))
    if value < 0:
        raise ValueError("Whitley value cell disappeared")
    tail = tail[:value] + "<w:t>0</w:t>" + tail[value + len("<w:t>1</w:t>") :]
    xml = head + tail
    log.append("Table 4.1 Whitley location 0 -> 1 and value 1 -> 0")

    perm = xml.find("Perm 0 ")
    if perm < 0 or "<w:t>d</w:t>" not in xml[perm : perm + 2500]:
        raise ValueError("Perm 0 table row was not found")
    region = xml[perm : perm + 12000]
    pair = region.find("<w:t>i</w:t>")
    # The first i is the subscript in xi. The location is the i followed by -1.
    pair = region.find("<w:t>-1</w:t>")
    if pair < 0:
        raise ValueError("Perm 0 location cell was not found")
    local_i = region.rfind("<w:t>i</w:t>", 0, pair)
    if local_i < 0:
        raise ValueError("Perm 0 location i was not found")
    absolute_i = perm + local_i
    absolute_minus = perm + pair
    xml = xml[:absolute_i] + "<w:t>1/i</w:t>" + xml[absolute_i + len("<w:t>i</w:t>") :]
    shift = len("<w:t>1/i</w:t>") - len("<w:t>i</w:t>")
    absolute_minus += shift
    xml = xml[:absolute_minus] + "<w:t></w:t>" + xml[absolute_minus + len("<w:t>-1</w:t>") :]
    log.append("Table 4.1 Perm 0, d, β location i-1 -> 1/i")

    xml = _replace_once(xml, "-65.53≤", "-65.536≤", "rotated hyper-ellipsoid")
    log.append("Table 4.1 rotated hyper-ellipsoid lower bound -65.53 -> -65.536")
    xml = _replace_once(
        xml,
        "normaly distributed on the range [0, 1]",
        "uniformly distributed on [0, 1)",
        "Xin-She Yang noise",
    )
    log.append("Table 4.1 Xin-She Yang noise described as uniform on [0, 1)")

    heading = "<w:t>Companion Code and Reproducibility</w:t></w:r></w:p>"
    if xml.count(heading) != 1:
        raise ValueError("companion heading was not found once")
    paragraphs = []
    intro = (
        "Companion code. Python 3.11 or 3.12. Install with python -m pip install -e '.[dev,notebooks]'. "
        "No release tag exists, so the links follow main and will move when main moves.",
        "The optimizers use numpy.random.Generator. Printed Appendix C and Appendix E traces used np.random.seed "
        "and are historical. The quick validation study is not those appendices.",
        "Problem 1a in Section 6.3 minimizes ITAE. Practical Exercise 1 minimizes settling time for the different plant 1/(1+s)^3.",
    )
    for line in intro:
        paragraphs.append(f"<w:p><w:r><w:t>{line}</w:t></w:r></w:p>")
        log.append(line[:60])
    for index, (label, url) in enumerate(COMPANION_LINKS, start=1):
        relationship_id = f"rIdReviewLink{index}"
        visible = f"{label} ({url})"
        paragraphs.append(
            '<w:p><w:hyperlink r:id="'
            + relationship_id
            + '"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t>'
            + visible
            + "</w:t></w:r></w:hyperlink></w:p>"
        )
        log.append(relationship_id)
    xml = xml.replace(heading, heading + "".join(paragraphs), 1)
    return xml, log


def _append_relationships(rels_xml: str) -> str:
    if "</Relationships>" not in rels_xml:
        raise ValueError("relationships root was not found")
    extra = []
    for index, (_label, url) in enumerate(COMPANION_LINKS, start=1):
        relationship_id = f"rIdReviewLink{index}"
        if relationship_id in rels_xml:
            raise ValueError(f"{relationship_id} already exists")
        extra.append(
            f'<Relationship Id="{relationship_id}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
            f'Target="{url}" TargetMode="External"/>'
        )
    return rels_xml.replace("</Relationships>", "".join(extra) + "</Relationships>", 1)


def _parent_and_index(root: ET.Element, child: ET.Element) -> tuple[ET.Element, int]:
    for parent in root.iter():
        for index, item in enumerate(list(parent)):
            if item is child:
                return parent, index
    raise ValueError("paragraph is not in the document")


def insert_companion_block(
    root: ET.Element,
    body_paragraphs: list[ET.Element],
    next_relationship: int,
) -> tuple[list[str], int]:
    texts = [paragraph_text(paragraph) for paragraph in body_paragraphs]
    matches = [index for index, text in enumerate(texts) if text == "Companion Code and Reproducibility"]
    if len(matches) != 1:
        raise ValueError(f"expected one companion heading, found {len(matches)}")
    anchor = body_paragraphs[matches[0]]
    intro = [
        (
            "Companion code. Python 3.11 or 3.12. Install with "
            "python -m pip install -e '.[dev,notebooks]'. "
            "No release tag exists, so the links follow main and will move when main moves."
        ),
        (
            "The optimizers use numpy.random.Generator. "
            "Printed Appendix C and Appendix E traces used np.random.seed and are historical. "
            "The quick validation study is not those appendices."
        ),
        ("Problem 1a in Section 6.3 minimizes ITAE. Practical Exercise 1 minimizes settling time for the different plant 1/(1+s)^3."),
    ]
    created = []
    cursor = anchor
    for line in intro:
        paragraph = _text_paragraph(line)
        parent, index = _parent_and_index(root, cursor)
        parent.insert(index + 1, paragraph)
        cursor = paragraph
        created.append(line[:60])
    for label, url in COMPANION_LINKS:
        relationship_id = f"rIdCompanion{next_relationship}"
        next_relationship += 1
        paragraph = _hyperlink_paragraph(f"{label} ({url})", relationship_id)
        parent, index = _parent_and_index(root, cursor)
        parent.insert(index + 1, paragraph)
        cursor = paragraph
        created.append(relationship_id)
    return created, next_relationship


def _next_relationship_index(rels_root: ET.Element) -> int:
    highest = 0
    for node in rels_root:
        value = node.get("Id") or ""
        digits = "".join(character for character in value if character.isdigit())
        if digits:
            highest = max(highest, int(digits))
    return highest + 1


def prepare(source: Path, destination: Path) -> list[str]:
    if not source.is_file():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8")
        rels_xml = archive.read("word/_rels/document.xml.rels").decode("utf-8")
        document_xml, log = apply_editorial_xml(document_xml)
        rels_xml = _append_relationships(rels_xml)
        payload = {name: archive.read(name) for name in archive.namelist()}
    payload["word/document.xml"] = document_xml.encode("utf-8")
    payload["word/_rels/document.xml.rels"] = rels_xml.encode("utf-8")
    temporary = destination.with_suffix(".docx.tmp")
    with zipfile.ZipFile(temporary, "w") as out:
        # ZipFile needs the original compression for the bulk of the package.
        with zipfile.ZipFile(source) as archive:
            for info in archive.infolist():
                compress = zipfile.ZIP_STORED if info.compress_type == zipfile.ZIP_STORED else zipfile.ZIP_DEFLATED
                out.writestr(info, payload[info.filename], compress_type=compress)
    temporary.replace(destination)
    return log


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    args = parser.parse_args(argv)
    log = prepare(args.source, args.destination)
    print(f"wrote {args.destination}")
    for line in log:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
