# -*- coding: utf-8 -*-
"""Quality lint for Algorithm guides."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from algorithm_guide_lib import BLOG_ALGORITHM, MANIFEST_PATH, strip_frontmatter  # noqa: E402

TEMPLATE_FILLER = re.compile(r"围绕「[^」]+」理解 \*\*")
PADDING_SUFFIX = re.compile(r"（走读·[^）]+·\d+）\s*$")
PLACEHOLDER_CODE = re.compile(
    r"```(?:python|cpp|c\+\+)\s*\n//\s*(?:参阅|见)\s+"
)
FORBIDDEN_H2 = re.compile(
    r"^##\s+(附录|常见问题|PowerShell\s+实验|源码阅读索引)",
    re.M,
)
CODE_FENCE = re.compile(r"```(\w+)?\n([\s\S]*?)```", re.M)
SECTION_H3 = re.compile(r"^###\s+(.+)$", re.M)


def _paragraphs(text: str) -> list[str]:
    parts: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        b = block.strip()
        if not b or b.startswith("```") or b.startswith("|"):
            continue
        if b.startswith(">") or b.startswith("#"):
            continue
        if len(b) < 40:
            continue
        parts.append(b)
    return parts


def validate_quality(body: str, entry: dict) -> list[str]:
    errors: list[str] = []
    if FORBIDDEN_H2.search(body):
        errors.append("forbidden ## section (appendix/FAQ)")
    if len(TEMPLATE_FILLER.findall(body)) > 2:
        errors.append("template filler paragraphs detected")
    if len(PADDING_SUFFIX.findall(body)) > 3:
        errors.append("bulk padding suffix (走读·…·N)")
    if len(PLACEHOLDER_CODE.findall(body)) > 2:
        errors.append("placeholder-only code blocks")

    m = re.search(r"^##\s+基础篇\s*$(.*?)(?=^##\s+|\Z)", body, re.M | re.S)
    if m:
        ess = m.group(1)
        if re.search(r"^####\s+", ess, re.M):
            errors.append("#### under ## 基础篇 (use ### only)")

    py_sec = re.search(r"^##\s+Python\s+实现\s*$(.*?)(?=^##\s+|\Z)", body, re.M | re.S)
    cpp_sec = re.search(r"^##\s+C\+\+\s+实现\s*$(.*?)(?=^##\s+|\Z)", body, re.M | re.S)
    if entry.get("slug") != "overview":
        for label, sec in (("Python", py_sec), ("C++", cpp_sec)):
            if not sec:
                errors.append(f"missing ## {label} 实现 section")
                continue
            fences = CODE_FENCE.findall(sec.group(1))
            if not any(lang and lang.lower() in ("python", "py", "cpp", "c++") for lang, _ in fences):
                errors.append(f"{label} 实现 lacks code fence")

    body_no_code = CODE_FENCE.sub("", body)
    seen: dict[str, int] = {}
    for p in _paragraphs(body_no_code):
        if len(p) < 50:
            continue
        seen[p] = seen.get(p, 0) + 1
    dupes = [p for p, n in seen.items() if n >= 2]
    if len(dupes) > 20:
        errors.append(f"duplicate paragraphs ({len(dupes)})")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", action="append")
    parser.add_argument("--all-published", action="store_true")
    parser.add_argument("--all-drafts", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    posts = data.get("posts", [])
    if args.slug:
        posts = [p for p in posts if p["slug"] in set(args.slug)]
    elif args.all_published:
        posts = [p for p in posts if p.get("status") == "published"]
    elif args.all_drafts:
        posts = [p for p in posts if p.get("status") == "draft"]
    else:
        parser.error("Specify --slug, --all-published, or --all-drafts")

    failed = 0
    for entry in posts:
        slug = entry["slug"]
        path = BLOG_ALGORITHM / slug / "index.md"
        if not path.is_file():
            print(f"FAIL {slug}: missing index.md")
            failed += 1
            continue
        body = strip_frontmatter(path.read_text(encoding="utf-8"))
        errors = validate_quality(body, entry)
        if errors:
            print(f"FAIL {slug}:")
            for e in errors:
                print(f"  - {e}")
            failed += 1
        else:
            print(f"OK {slug}")

    if failed and args.strict:
        sys.exit(1)
    print(f"Done: {len(posts) - failed} ok, {failed} failed")


if __name__ == "__main__":
    main()
