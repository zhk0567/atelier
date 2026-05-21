"""Blog post markdown rendering."""

from __future__ import annotations

import re

import markdown
from fastapi import HTTPException

from app.markdown.mermaid import apply_mermaid_blocks
from site_data import BLOG_DIR, get_blog_post

_BLOG_FRONTMATTER_RE = re.compile(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n", re.DOTALL)
_BLOG_INLINE_TOC_RE = re.compile(r"^## 目录\s*\n(?:.*?\n)*?(?=^## )", re.MULTILINE)
_BLOG_EDITORIAL_SECTION_RE = re.compile(
    r"^##\s*(?:发布备忘|编辑备忘|内部备忘)\s*\n[\s\S]*?(?=^## |\Z)",
    re.MULTILINE,
)


def heading_anchor(title: str) -> str:
    return re.sub(r"\s+", "-", title.strip())


def strip_guide_inline_toc(raw: str) -> str:
    return _BLOG_INLINE_TOC_RE.sub("", raw, count=1)


def framework_guide_nav(raw: str) -> list[dict[str, str]]:
    skip = {"目录"}
    nav: list[dict[str, str]] = []
    for line in raw.splitlines():
        if line.startswith("## ") and not line.startswith("### "):
            title = line[3:].strip()
            if title in skip:
                continue
            nav.append({"title": title, "anchor": heading_anchor(title)})
    return nav


def render_blog_markdown(slug: str) -> tuple[dict[str, str], str]:
    post = get_blog_post(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    folder = post.get("folder", "")
    index_path = BLOG_DIR / folder / "index.md"
    if not index_path.is_file():
        raise HTTPException(status_code=404, detail="Blog post not found")
    raw = index_path.read_text(encoding="utf-8")
    raw = _BLOG_FRONTMATTER_RE.sub("", raw, count=1)
    raw = _BLOG_EDITORIAL_SECTION_RE.sub("", raw)
    if post.get("series") == "framework":
        raw = strip_guide_inline_toc(raw)
    raw = re.sub(
        r"!\[([^\]]*)\]\(images/([^)]+)\)",
        rf"![\1](/static/blog/{slug}/\2)",
        raw,
    )
    html = markdown.markdown(raw, extensions=["tables", "fenced_code", "nl2br"])

    def add_heading_ids(markup: str, tag: str) -> str:
        def repl(match: re.Match[str]) -> str:
            title = match.group(1)
            aid = heading_anchor(title)
            return f'<{tag} id="{aid}">{title}</{tag}>'

        return re.sub(rf"<{tag}>([^<]+)</{tag}>", repl, markup)

    html = add_heading_ids(add_heading_ids(html, "h2"), "h3")
    html = re.sub(
        r"<img ",
        '<img loading="lazy" decoding="async" ',
        html,
    )
    html, _ = apply_mermaid_blocks(html)
    return post, html
