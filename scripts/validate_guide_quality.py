# -*- coding: utf-8 -*-
"""Quality lint for Framework official guides (structure, pollution, duplicates)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from guide_lib import (  # noqa: E402
    BLOG_FRAMEWORK,
    MANIFEST_PATH,
    load_toc,
    strip_frontmatter,
)

FORBIDDEN_HEADING = re.compile(r"^####\s+学习要点", re.M)
FORBIDDEN_TEMPLATE = re.compile(r"学习要点：")
FORBIDDEN_H2 = re.compile(
    r"^##\s+(附录|常见问题|PowerShell\s+实验|源码阅读索引|子工程要点|术语速查|精读)",
    re.M,
)
FORBIDDEN_FRAMEWORK_BLOCK = re.compile(r"\*\*Framework\s+对照\*\*")
TEMPLATE_FILLER = re.compile(r"围绕「[^」]+」理解 \*\*")
TEMPLATE_FILLER2 = re.compile(
    r"深入 \*\*[^*]+\*\* 的延伸练习（\d+）："
)
MAX_TEMPLATE_FILLER = 2
# Bulk-regen padding from write_vue_style_guide._unique_paragraphs
PADDING_SUFFIX = re.compile(r"（[^）]{2,40}-\d+·\d+）\s*$")
GENERIC_STUDY = re.compile(
    r"学习「[^」]+」时，请打开子工程.*再对照.*官方文档"
)
PLACEHOLDER_CODE = re.compile(
    r"```(?:typescript|go|python|javascript)\s*\n//\s*(?:参阅|见)\s+"
)
MAX_GENERIC_STUDY = 3
MAX_PLACEHOLDER_CODE = 2

# (repo_path_substr, required_in_quickstart, forbidden_unless_also_present)
STACK_QUICKSTART_RULES: list[tuple[str, str, str, str]] = [
    ("/DotNet/", "dotnet", "npm run start:dev", "dotnet run"),
    ("/Go/", "go run", "uvicorn main:app", ""),
    ("/Python/", "python", "npm run", "uvicorn"),
]

CODE_FENCE = re.compile(r"```(\w+)?\n([\s\S]*?)```", re.M)
SECTION_H3 = re.compile(r"^###\s+(.+)$", re.M)

# Terms that should not appear outside Python/FastAPI guides
PYTHON_POLLUTION = [
    "uvicorn",
    "Pydantic",
    "Depends(",
    "TestClient",
    "CORSMiddleware",
    "from fastapi",
]

ESSENTIALS_BLOCK = re.compile(
    r"^##\s+基础篇\s*$(.*?)(?=^##\s+|\Z)", re.M | re.S
)


def _is_python_stack(entry: dict) -> bool:
    rel = (entry.get("source_rel") or "").lower()
    slug = entry.get("slug", "").lower()
    return "python" in rel or "fastapi" in slug or "flask" in slug or "django" in slug


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


def validate_quality(body: str, toc: dict, entry: dict) -> list[str]:
    errors: list[str] = []

    if FORBIDDEN_HEADING.search(body):
        errors.append("forbidden heading: #### 学习要点")
    if FORBIDDEN_TEMPLATE.search(body):
        errors.append("forbidden template phrase: 学习要点：")
    if FORBIDDEN_H2.search(body):
        errors.append("forbidden ## section (appendix/FAQ/experiment index)")
    if FORBIDDEN_FRAMEWORK_BLOCK.search(body):
        errors.append("forbidden standalone **Framework 对照** block (embed in prose)")

    n_filler = len(TEMPLATE_FILLER.findall(body)) + len(TEMPLATE_FILLER2.findall(body))
    if n_filler > MAX_TEMPLATE_FILLER:
        errors.append(f"template filler paragraphs: {n_filler} (max {MAX_TEMPLATE_FILLER})")

    if len(PADDING_SUFFIX.findall(body)) > 5:
        errors.append("bulk padding suffix paragraphs detected (e.g. （节名-0·1）)")
    if len(GENERIC_STUDY.findall(body)) > MAX_GENERIC_STUDY:
        errors.append(f"generic study filler lines: {len(GENERIC_STUDY.findall(body))} (max {MAX_GENERIC_STUDY})")
    if len(PLACEHOLDER_CODE.findall(body)) > MAX_PLACEHOLDER_CODE:
        errors.append("too many placeholder-only code blocks (// 参阅 / // 见)")

    repo = (entry.get("repo_path") or "").replace("\\", "/")
    qs = ""
    mqs = re.search(r"^##\s+快速上手\s*$(.*?)(?=^##\s+|\Z)", body, re.M | re.S)
    if mqs:
        qs = mqs.group(1)
    for substr, required, forbidden, alt in STACK_QUICKSTART_RULES:
        if substr.lower() in repo.lower():
            block = qs + body[:2000]
            if required and required not in block:
                errors.append(f"quickstart/stack: expected '{required}' for {substr}")
            if forbidden and forbidden in block and (not alt or alt not in block):
                errors.append(f"quickstart/stack: suspicious '{forbidden}' for {substr}")

    m = ESSENTIALS_BLOCK.search(body)
    if m:
        ess = m.group(1)
        if re.search(r"^####\s+", ess, re.M):
            errors.append("#### headings under ## 基础篇 (use ### only)")

        expected = [ch.get("title", "") for ch in toc.get("essentials", [])]
        found = SECTION_H3.findall(ess)
        for title in expected:
            if title and title not in found:
                errors.append(f"essentials missing ### {title}")

        for title in found:
            if title not in expected:
                errors.append(f"unexpected ### in essentials: {title}")

        for title in expected:
            if not title:
                continue
            sec = re.search(
                rf"^###\s+{re.escape(title)}\s*$(.*?)(?=^###\s+|\Z)",
                ess,
                re.M | re.S,
            )
            if not sec:
                continue
            sec_text = sec.group(1)
            fences = CODE_FENCE.findall(sec_text)
            has_real = any(
                lang and lang.lower() not in ("text", "txt", "")
                for lang, _ in fences
            )
            if not has_real:
                errors.append(f"section lacks non-text code block: {title}")

    if not _is_python_stack(entry):
        low = body.lower()
        for term in PYTHON_POLLUTION:
            if term.lower() in low or term in body:
                errors.append(f"cross-stack pollution: {term}")

    body_no_code = CODE_FENCE.sub("", body)
    paras = _paragraphs(body_no_code)
    seen: dict[str, int] = {}
    for p in paras:
        if len(p) < 50:
            continue
        seen[p] = seen.get(p, 0) + 1
    dupes = [p[:60] + "…" for p, n in seen.items() if n >= 2]
    if len(dupes) > 25:
        errors.append(f"duplicate paragraphs ({len(dupes)}): e.g. {dupes[0]}")

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
        wanted = set(args.slug)
        posts = [p for p in posts if p["slug"] in wanted]
    elif args.all_published:
        posts = [p for p in posts if p.get("status") == "published"]
    elif args.all_drafts:
        posts = [p for p in posts if p.get("status") == "draft"]
    else:
        parser.error("Specify --slug, --all-published, or --all-drafts")

    failed = 0
    for entry in posts:
        slug = entry["slug"]
        path = BLOG_FRAMEWORK / slug / "index.md"
        if not path.is_file():
            print(f"FAIL {slug}: missing index.md")
            failed += 1
            continue
        raw = path.read_text(encoding="utf-8")
        body = strip_frontmatter(raw)
        toc_id = entry.get("guide_toc", "generic-backend")
        try:
            toc = load_toc(toc_id)
        except FileNotFoundError:
            print(f"FAIL {slug}: unknown guide_toc {toc_id}")
            failed += 1
            continue
        errors = validate_quality(body, toc, entry)
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
