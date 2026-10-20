"""Check relative links in the repository docs, and optional DOCX hyperlinks.

Repository markdown links are checked against the checkout. A manuscript path
is optional because the editorial DOCX is not stored in this repository.
Hyperlinks that point at this GitHub repository are checked as repo-relative
paths. Other URLs are listed and are not fetched.
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REPO_BLOB = re.compile(r"https://github\.com/dmitruyk/Metaheuristic-Optimization-with-Python/(?:blob|tree)/[^/]+/(.+)")
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def markdown_targets() -> list[tuple[Path, str]]:
    found = []
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in {".venv", ".git", "manuscript_extract"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip().split()[0]
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            found.append((path, target.split("#", 1)[0]))
    return found


def check_markdown() -> list[str]:
    missing = []
    for path, target in markdown_targets():
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            missing.append(f"{path.relative_to(ROOT)} -> {target}")
    return missing


def docx_hyperlinks(docx: Path) -> list[str]:
    urls = []
    with zipfile.ZipFile(docx) as archive:
        names = [name for name in archive.namelist() if name.startswith("word/_rels/") and name.endswith(".rels")]
        for name in names:
            root = ET.fromstring(archive.read(name))
            for node in root.findall(f"{REL}Relationship"):
                target = node.get("Target")
                if target and node.get("TargetMode") == "External":
                    urls.append(target)
    return urls


def check_docx(docx: Path) -> tuple[list[str], list[str]]:
    broken = []
    external = []
    for url in docx_hyperlinks(docx):
        match = REPO_BLOB.match(url)
        if match is None:
            external.append(url)
            continue
        relative = match.group(1)
        if not (ROOT / relative).exists():
            broken.append(url)
    return broken, external


def main() -> int:
    missing = check_markdown()
    print(f"markdown relative links missing: {len(missing)}")
    for item in missing:
        print(f"  {item}")
    if len(sys.argv) == 2:
        broken, external = check_docx(Path(sys.argv[1]))
        print(f"docx repo links missing: {len(broken)}")
        for item in broken:
            print(f"  {item}")
        print(f"docx external links not fetched: {len(external)}")
    else:
        print("docx hyperlinks: not checked; pass the editorial DOCX path to check them")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
