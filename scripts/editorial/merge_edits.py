"""Merge several edit files into one, resolving paragraphs edited more than once.

Files are given in priority order (scientific corrections first, copyedits
after). When two ``replace`` records target the same paragraph, the later
file's record becomes the base text and the earlier (higher-priority) record's
token-level changes are re-applied on top of it: each changed token run of the
correction is located in the copyedited text together with up to two tokens
of context; if it is found exactly once the change is applied. If that fails,
the copyedit's changes are re-applied onto the corrected text instead. If
both fail, the pair is written to ``--unresolved`` and the higher-priority
record alone is kept. Non-replace operations pass through.

Usage::

    python scripts/editorial/merge_edits.py --out merged.jsonl --unresolved unresolved.md \
        corrections.jsonl 01-chapter-1.jsonl …
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path

TOKEN = re.compile(r"\s+|\w+|[^\w\s]")


def rebase(old: str, correction_new: str, base_new: str) -> tuple[str | None, str]:
    """Re-apply the old→correction_new changes onto base_new."""
    a, b, base = TOKEN.findall(old), TOKEN.findall(correction_new), TOKEN.findall(base_new)
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    result = list(base)
    for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):
        if tag == "equal":
            continue
        k = None
        for ctx in (2, 1, 0):
            ctx_before = a[max(0, i1 - ctx) : i1]
            ctx_after = a[i2 : i2 + ctx]
            needle = ctx_before + a[i1:i2] + ctx_after
            if not needle:
                break
            hits = [h for h in range(len(result) - len(needle) + 1) if result[h : h + len(needle)] == needle]
            if len(hits) == 1:
                k = hits[0] + len(ctx_before)
                break
        if k is None:
            return None, f"{tag} of {''.join(a[i1:i2])!r} not found exactly once in the copyedited text"
        result[k : k + (i2 - i1)] = b[j1:j2]
    return "".join(result), "ok"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("files", type=Path, nargs="+", help="edit files, highest priority first")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--unresolved", type=Path)
    args = parser.parse_args(argv)
    replace_by_idx: dict[int, dict] = {}
    others: list[dict] = []
    notes: list[str] = []
    merged = rebased = 0
    for path in args.files:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                if not line.strip() or line.startswith("#"):
                    continue
                record = json.loads(line)
                record.setdefault("source", path.name)
                if record.get("op", "replace") != "replace":
                    others.append(record)
                    continue
                idx = int(record["idx"])
                if idx not in replace_by_idx:
                    replace_by_idx[idx] = record
                    continue
                first = replace_by_idx[idx]  # higher priority (earlier file)
                text, status = rebase(first.get("old", ""), first["new"], record["new"])
                if text is None:
                    # Second attempt: re-apply the copyedit's changes onto the corrected text.
                    text, status2 = rebase(record.get("old", ""), record["new"], first["new"])
                    status = f"{status}; reverse: {status2}"
                if text is None:
                    notes.append(
                        f"### ¶{idx} — kept {first['source']} ({first.get('ref', first.get('note', ''))}); "
                        f"dropped {record['source']} ({record.get('note', '')}): {status}\n\n"
                        f"- correction new: {first['new']}\n- copyedit new: {record['new']}\n"
                    )
                    merged += 1
                    continue
                combined = dict(record)
                combined["new"] = text
                combined["note"] = f"{record.get('note', '')} + {first.get('ref', first.get('note', ''))}".strip(" +")
                combined["source"] = f"{record['source']}+{first['source']}"
                for flag in ("allow_object", "allow_code", "allow_field"):
                    if first.get(flag) or record.get(flag):
                        combined[flag] = True
                replace_by_idx[idx] = combined
                rebased += 1
    with args.out.open("w", encoding="utf-8") as fh:
        for record in sorted(replace_by_idx.values(), key=lambda r: int(r["idx"])):
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        for record in others:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    if args.unresolved:
        args.unresolved.write_text("# Unresolved overlaps\n\n" + "\n".join(notes), encoding="utf-8")
    print(f"{len(replace_by_idx) + len(others)} records written; {rebased} rebased; {merged} unresolved (kept priority record)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
