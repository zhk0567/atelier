"""
Batch-clean Wiki markdown sources (remove auto-gen boilerplate).

Usage (from project root):
  python scripts/site/clean_wiki_sources.py           # dry-run
  python scripts/site/clean_wiki_sources.py --write   # write files
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_DIR = ROOT / "Wiki"

_DETAILS_RE = re.compile(
    r"<details>[\s\S]*?Relevant\s+source\s+files[\s\S]*?</details>\s*",
    re.I,
)
_DUP_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$", re.M)
_REPEAT_H2_H1_RE = re.compile(
    r"^##\s+(.+?)\s*-\s*\1\s*$",
    re.M,
)


def clean_wiki_source(text: str) -> tuple[str, list[str]]:
    """Return (cleaned_text, list of change descriptions)."""
    changes: list[str] = []
    original = text

    new, n = _DETAILS_RE.subn("", text)
    if n:
        changes.append(f"removed {n} details block(s)")
    text = new

    text = re.sub(
        r"<details>[\s\S]*?</details>\s*",
        "",
        text,
        flags=re.I,
    )

    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = _REPEAT_H2_H1_RE.match(line.strip())
        if m and i + 1 < len(lines):
            title = m.group(1).strip()
            next_stripped = lines[i + 1].strip()
            if next_stripped == f"# {title}" or next_stripped.startswith(f"# {title} "):
                changes.append(f"drop duplicate h2 before h1: {title[:40]}")
                i += 1
                continue
        out.append(line)
        i += 1
    text = "\n".join(out)

    seen: set[tuple[str, str]] = set()
    deduped: list[str] = []
    for line in text.splitlines():
        m = _DUP_HEADING_RE.match(line)
        if m:
            key = (m.group(1), m.group(2).strip())
            if key in seen:
                changes.append(f"dedupe heading: {key[1][:40]}")
                continue
            seen.add(key)
        deduped.append(line)
    text = "\n".join(deduped)

    text = re.sub(r"\n{4,}", "\n\n\n", text).strip()
    if text:
        text += "\n"

    if text != original.strip() + ("\n" if original.endswith("\n") else ""):
        if not changes:
            changes.append("normalized whitespace")
    return text, changes


def iter_wiki_pages() -> list[Path]:
    paths: list[Path] = []
    for path in sorted(WIKI_DIR.rglob("*.md")):
        rel = path.relative_to(WIKI_DIR)
        parts = rel.parts
        if "_source" in parts:
            continue
        if path.name == "README.md":
            continue
        paths.append(path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write cleaned files")
    args = parser.parse_args()

    changed = 0
    for path in iter_wiki_pages():
        raw = path.read_text(encoding="utf-8")
        cleaned, notes = clean_wiki_source(raw)
        if not notes:
            continue
        changed += 1
        rel = path.relative_to(ROOT)
        print(f"{rel}: {', '.join(notes)}")
        if args.write:
            path.write_text(cleaned, encoding="utf-8")

    print(f"\n{'Wrote' if args.write else 'Would update'} {changed} file(s).")
    if not args.write and changed:
        print("Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
