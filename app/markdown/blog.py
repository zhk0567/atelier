"""Blog post markdown rendering."""

from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException

from app.markdown.page_cache import file_cache_key, render_cached
from app.markdown.render import (
    framework_guide_nav,
    markdown_to_html,
    postprocess_content_html,
    rewrite_blog_image_paths,
    strip_blog_editorial_sections,
    strip_blog_frontmatter,
    strip_guide_inline_toc,
)
from site_data import BLOG_DIR, get_blog_post


def _render_blog_markdown_impl(slug: str) -> tuple[dict[str, str], str]:
    post = get_blog_post(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    folder = post.get("folder", "")
    index_path = BLOG_DIR / folder / "index.md"
    if not index_path.is_file():
        raise HTTPException(status_code=404, detail="Blog post not found")
    raw = index_path.read_text(encoding="utf-8")
    raw = strip_blog_frontmatter(raw)
    raw = strip_blog_editorial_sections(raw)
    if post.get("series") == "framework":
        raw = strip_guide_inline_toc(raw)
    raw = rewrite_blog_image_paths(raw, slug)
    html = markdown_to_html(raw)
    html, _ = postprocess_content_html(html)
    return post, html


def render_blog_markdown(slug: str) -> tuple[dict[str, str], str]:
    post = get_blog_post(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    folder = post.get("folder", "")
    index_path = BLOG_DIR / folder / "index.md"
    key = file_cache_key(index_path)
    return render_cached(
        key,
        f"blog:{slug}",
        lambda: _render_blog_markdown_impl(slug),
    )
