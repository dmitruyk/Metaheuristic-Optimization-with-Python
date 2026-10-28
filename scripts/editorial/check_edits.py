"""Sanity checks for copyedit records before they become tracked changes.

For every ``replace`` record the script compares ``old`` and ``new`` and flags:

- numbers that disappeared or appeared (digits, decimals, exponents);
- citation keys ``[n]`` and figure/table/equation references that changed;
- code identifiers (CamelCase, snake_case, dotted names) that disappeared;
- length ratio outside 0.5–1.8, or an edit that touches a code-like or
  object paragraph without the matching ``allow_*`` flag;
- ``old`` not matching the manuscript text (whitespace-normalised).

It prints one line per flag and a word-level diff for flagged records with
``--diff``. Exit code 1 if any record is flagged as an error (mismatch,
guard), 0 otherwise; warnings do not change the exit code.

Usage::

    python scripts/editorial/check_edits.py manuscript_extract/paragraphs.jsonl manuscript_extract/edits/*.jsonl [--diff]
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

NUMBER = re.compile(r"(?<![\w.])[-−]?\d+(?:[.,]\d+)*(?:[eE][-+]?\d+)?(?![\w])")
CITATION = re.compile(r"\[\d+(?:[,–-]\s*\d+)*\]")
XREF = re.compile(r"\b(?:Fig(?:ure)?\.?|Table|Problem|Exercise|Chapter|Section|Appendix)\s*[A-Z]?\d+(?:\.\d+)*[a-z]?|\(\d+\.\d+\)")
IDENT = re.compile(r"\b(?:[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_.]*|[A-Za-z]+_[A-Za-z0-9_]+|[A-Z][a-z]+[A-Z][A-Za-z0-9]*)\b")
WORD_TOKEN = re.compile(r"\s+|\w+|[^\w\s]")


def normalise(text: str) -> str:
    return " ".join(text.split())


def comparable(text: str) -> str:
    """Neutralise differences that are pure typography before counting tokens."""
    text = re.sub(r"\b(Fig(?:ure)?\.?|Table|Chapter|Section)(\d)", r"\1 \2", text)
    text = text.replace("...", "–").replace("…", "–")
    text = re.sub(r"\b(i\.e|e\.g|et\.al|vs)\.?", "", text)
    text = re.sub(r"(\d),(\d{3})\b", r"\1\2", text)  # thousands separators
    return text


def word_diff(old: str, new: str) -> str:
    a, b = WORD_TOKEN.findall(old), WORD_TOKEN.findall(new)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            out.append("".join(a[i1:i2]))
        elif tag == "delete":
            out.append("[-" + "".join(a[i1:i2]) + "-]")
        elif tag == "insert":
            out.append("{+" + "".join(b[j1:j2]) + "+}")
        else:
            out.append("[-" + "".join(a[i1:i2]) + "-]{+" + "".join(b[j1:j2]) + "+}")
    return "".join(out)


def check(record: dict, para: dict | None) -> list[tuple[str, str]]:
    flags: list[tuple[str, str]] = []
    op = record.get("op", "replace")
    if para is None:
        return [("error", "no such paragraph")]
    if op != "replace":
        return flags
    old, new = record.get("old"), record.get("new", "")
    if old is not None and normalise(old) != normalise(para["text"]):
        flags.append(("error", "old text does not match the manuscript"))
    if para.get("code_like") and not record.get("allow_code"):
        flags.append(("error", "code-like paragraph edited without allow_code"))
    if para.get("has_object") and not record.get("allow_object"):
        flags.append(("error", "object paragraph edited without allow_object"))
    base = para["text"]
    cbase, cnew = comparable(base), comparable(new)
    old_nums, new_nums = NUMBER.findall(cbase), NUMBER.findall(cnew)
    missing = sorted(set(old_nums) - set(new_nums))
    added = sorted(set(new_nums) - set(old_nums))
    if missing or added:
        flags.append(("warn", f"numbers changed: -{missing} +{added}"))
    if sorted(CITATION.findall(base)) != sorted(CITATION.findall(new)):
        flags.append(("warn", f"citations changed: {CITATION.findall(base)} -> {CITATION.findall(new)}"))
    old_x, new_x = sorted(normalise(x) for x in XREF.findall(cbase)), sorted(normalise(x) for x in XREF.findall(cnew))
    if old_x != new_x:
        flags.append(("warn", f"cross-references changed: {old_x} -> {new_x}"))
    lost = sorted(set(IDENT.findall(cbase)) - set(IDENT.findall(cnew)))
    if lost:
        flags.append(("warn", f"identifiers lost: {lost}"))
    if base.strip():
        ratio = len(new) / max(len(base), 1)
        if ratio < 0.5 or ratio > 1.8:
            flags.append(("warn", f"length ratio {ratio:.2f}"))
    if normalise(new) == normalise(base):
        flags.append(("warn", "no change"))
    return flags


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paragraphs", type=Path)
    parser.add_argument("edits", type=Path, nargs="+")
    parser.add_argument("--diff", action="store_true", help="print a word diff for flagged records")
    parser.add_argument("--all", action="store_true", help="print a word diff for every record")
    args = parser.parse_args(argv)
    paragraphs = {}
    with args.paragraphs.open(encoding="utf-8") as fh:
        for line in fh:
            p = json.loads(line)
            paragraphs[p["idx"]] = p
    errors = warnings = total = 0
    seen: dict[int, list[str]] = {}
    for path in args.edits:
        with path.open(encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                if not line.strip() or line.startswith("#"):
                    continue
                record = json.loads(line)
                total += 1
                idx = int(record["idx"])
                if record.get("op", "replace") == "replace":
                    seen.setdefault(idx, []).append(f"{path.name}:{n}")
                flags = check(record, paragraphs.get(idx))
                for level, text in flags:
                    print(f"{level.upper():5s} {path.name}:{n} ¶{idx} {record.get('ref', '')} {text}")
                    if level == "error":
                        errors += 1
                    else:
                        warnings += 1
                if (flags and args.diff) or args.all:
                    if record.get("op", "replace") == "replace" and idx in paragraphs:
                        print("      " + word_diff(paragraphs[idx]["text"], record.get("new", "")))
    for idx, where in seen.items():
        if len(where) > 1:
            print(f"ERROR duplicate edits for ¶{idx}: {', '.join(where)}")
            errors += 1
    print(f"{total} records, {errors} errors, {warnings} warnings", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
