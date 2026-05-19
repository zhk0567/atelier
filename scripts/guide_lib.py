"""Shared helpers for Framework official-guide generation and validation."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import sys
import yaml

ATELIER_ROOT = Path(__file__).resolve().parent.parent
if str(ATELIER_ROOT) not in sys.path:
    sys.path.insert(0, str(ATELIER_ROOT))

from app.config import (  # noqa: E402
    blog_framework_path,
    framework_manifest_path,
    guide_toc_dir,
)

GUIDE_TOC_DIR = guide_toc_dir()
MANIFEST_PATH = framework_manifest_path()
BLOG_FRAMEWORK = blog_framework_path()

PILOT_SLUGS = frozenset({
    "fastapi-python",
    "nestjs-node-typescript",
    "react-vite-typescript",
    "nextjs-fullstack-typescript",
    "nx-tooling-typescript",
})

TIER_MIN_CHARS = {
    "major": 25_000,
    "medium": 12_000,
    "placeholder": 6_000,
}

SECTION_MARKERS = {
    "intro": re.compile(r"^##\s+导读", re.M),
    "prereq": re.compile(r"^##\s+预备知识", re.M),
    "quickstart": re.compile(r"^##\s+快速上手", re.M),
    "essentials": re.compile(r"^##\s+基础篇", re.M),
    "lab": re.compile(r"^##\s+Framework\s+子工程实战", re.M),
    "paths": re.compile(r"^##\s+学习路径", re.M),
    "refs": re.compile(r"^##\s+延伸阅读", re.M),
}

_CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")


def load_toc(toc_id: str) -> dict[str, Any]:
    path = GUIDE_TOC_DIR / f"{toc_id}.yaml"
    if not path.is_file():
        raise FileNotFoundError(path)
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def list_toc_ids() -> list[str]:
    return sorted(p.stem for p in GUIDE_TOC_DIR.glob("*.yaml"))


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        m = re.match(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n", text, re.DOTALL)
        if m:
            return text[m.end() :]
    return text


def count_chinese(text: str) -> int:
    return len(_CHINESE_RE.findall(strip_frontmatter(text)))


def assign_guide_toc_id(entry: dict) -> str:
    slug = entry.get("slug", "")
    stack = (entry.get("stack") or "").lower()
    cat = entry.get("category", "")
    rel = (entry.get("source_rel") or "").lower()

    if slug in {"fastapi-python"} or "fastapi" in slug:
        return "fastapi"
    if slug in {"nestjs-node-typescript"} or "nestjs" in slug:
        return "nestjs"
    if slug in {"react-vite-typescript"} or (cat == "Front-end" and "react" in slug):
        return "react"
    if slug in {"nextjs-fullstack-typescript"} or "nextjs" in slug or "nuxt" in slug:
        return "nextjs"
    if "flask" in slug:
        return "flask"
    if cat == "Tooling":
        return "generic-tooling"
    if cat == "Front-end":
        return "generic-frontend"
    if cat == "Full-stack":
        return "nextjs" if "next" in slug or "nuxt" in slug else "generic-frontend"
    if "python" in rel:
        return "fastapi" if "fastapi" in rel else "generic-backend"
    if "node" in rel or "typescript" in rel:
        return "nestjs" if "nest" in rel else "generic-backend"
    return "generic-backend"


def essential_heading_pattern(title: str) -> re.Pattern[str]:
    # Match ### title in essentials section
    escaped = re.escape(title)
    return re.compile(rf"^###\s+{escaped}\s*$", re.M)


def validate_guide_body(
    body: str, toc: dict[str, Any], *, slug: str | None = None
) -> list[str]:
    errors: list[str] = []
    for key, pat in SECTION_MARKERS.items():
        if key == "essentials":
            continue
        if not pat.search(body):
            errors.append(f"missing section: {key}")

    if not SECTION_MARKERS["essentials"].search(body):
        errors.append("missing section: essentials (## 基础篇)")

    for ch in toc.get("essentials", []):
        title = ch.get("title", "")
        if title and not essential_heading_pattern(title).search(body):
            errors.append(f"missing essential chapter: {title}")

    tier = toc.get("tier", "medium")
    min_chars = TIER_MIN_CHARS.get(tier, 12_000)
    n = count_chinese(body)
    if n < min_chars:
        errors.append(f"chinese chars {n} < {min_chars} (tier={tier})")

    return errors


def blog_title(stack: str, *, pilot: bool = False) -> str:
    return f"{stack} 官方指南：从入门到 Framework 子工程实战"
