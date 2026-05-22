# -*- coding: utf-8 -*-
"""Shared helpers for Algorithm guide validation."""

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
    algorithm_guide_toc_dir,
    algorithm_manifest_path,
    blog_algorithm_path,
)

GUIDE_TOC_DIR = algorithm_guide_toc_dir()
MANIFEST_PATH = algorithm_manifest_path()
BLOG_ALGORITHM = blog_algorithm_path()

TIER_MIN_CHARS = {
    "major": 15_000,
    "medium": 8_000,
    "index": 4_000,
}

SECTION_MARKERS = {
    "intro": re.compile(r"^##\s+导读", re.M),
    "prereq": re.compile(r"^##\s+预备知识", re.M),
    "study": re.compile(r"^##\s+Study\s+仓库对照", re.M),
    "essentials": re.compile(r"^##\s+基础篇", re.M),
    "python_impl": re.compile(r"^##\s+Python\s+实现", re.M),
    "cpp_impl": re.compile(r"^##\s+C\+\+\s+实现", re.M),
    "practice": re.compile(r"^##\s+练习与延伸", re.M),
    "paths": re.compile(r"^##\s+学习路径", re.M),
    "refs": re.compile(r"^##\s+延伸阅读", re.M),
}

_CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")


def load_toc(toc_id: str) -> dict[str, Any]:
    path = GUIDE_TOC_DIR / f"{toc_id}.yaml"
    if not path.is_file():
        raise FileNotFoundError(path)
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        m = re.match(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n", text, re.DOTALL)
        if m:
            return text[m.end() :]
    return text


def count_chinese(text: str) -> int:
    return len(_CHINESE_RE.findall(strip_frontmatter(text)))


def essential_heading_pattern(title: str) -> re.Pattern[str]:
    escaped = re.escape(title)
    return re.compile(rf"^###\s+{escaped}\s*$", re.M)


def assign_guide_toc(topic_path: str) -> str:
    if not topic_path or topic_path == "notes":
        return "overview"
    if topic_path.startswith("problems/"):
        return "problem-index"
    if topic_path.startswith("data_structures/"):
        return "topic-ds"
    if topic_path.startswith("interview/classic/"):
        return "interview-classic"
    return "topic-algorithm"


def assign_guide_tier(topic_path: str, guide_toc: str) -> str:
    if guide_toc == "overview":
        return "major"
    if guide_toc == "problem-index":
        return "index"
    if guide_toc == "interview-classic":
        return "medium"
    if topic_path.startswith("algorithms/") and topic_path.count("/") == 1:
        return "major"
    if topic_path.startswith("data_structures/") and topic_path.count("/") == 1:
        return "major"
    return "medium"


def slug_from_topic_path(topic_path: str) -> str:
    if not topic_path or topic_path in ("notes",):
        return "overview"
    parts = topic_path.split("/")
    head = parts[0]
    rest = parts[1:]
    if head == "data_structures":
        return "ds-" + "-".join(r.replace("_", "-") for r in rest)
    if head == "algorithms":
        if rest == ["dynamic_programming"]:
            return "algo-dynamic-programming"
        segs: list[str] = []
        for r in rest:
            segs.append("dp" if r == "dynamic_programming" else r.replace("_", "-"))
        return "algo-" + "-".join(segs)
    if head == "interview":
        return "iv-" + "-".join(r.replace("_", "-") for r in rest)
    if head == "problems":
        return "prob-" + "-".join(r.replace("_", "-") for r in rest)
    return "topic-" + "-".join(p.replace("_", "-") for p in parts)


def topic_path_from_notes(rel_posix: str) -> str:
    p = rel_posix.replace("\\", "/")
    if p.startswith("python/"):
        p = p[len("python/") :]
    if p.endswith("/notes.md"):
        p = p[: -len("/notes.md")]
    elif p.endswith("notes.md"):
        p = p[: -len("notes.md")].rstrip("/")
    return p


def category_from_topic_path(topic_path: str) -> str:
    if not topic_path or topic_path == "notes":
        return "Overview"
    head = topic_path.split("/")[0]
    return {
        "algorithms": "Algorithms",
        "data_structures": "DataStructures",
        "interview": "Interview",
        "problems": "Problems",
    }.get(head, "Other")


def blog_title(topic_path: str, slug: str) -> str:
    if slug == "overview":
        return "Algorithm 仓库导读：双语言算法与刷题"
    name = slug.split("-", 1)[-1].replace("-", " ").title()
    if slug.startswith("ds-"):
        return f"数据结构 · {name}"
    if slug.startswith("algo-"):
        return f"算法 · {name}"
    if slug.startswith("iv-"):
        return f"面试专题 · {name}"
    if slug.startswith("prob-"):
        return f"题单 · {name}"
    return f"Algorithm · {name}"


def validate_guide_body(body: str, toc: dict[str, Any], *, slug: str | None = None) -> list[str]:
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
    min_chars = TIER_MIN_CHARS.get(tier, 8_000)
    n = count_chinese(body)
    if n < min_chars:
        errors.append(f"chinese chars {n} < {min_chars} (tier={tier})")

    if slug == "overview":
        if "python" not in body.lower() or "c++" not in body.lower():
            errors.append("overview should mention both Python and C++")
    else:
        if not SECTION_MARKERS["python_impl"].search(body) or not SECTION_MARKERS["cpp_impl"].search(body):
            pass  # already checked above

    return errors
