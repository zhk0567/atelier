"""Wiki page markdown sanitization and HTML rendering."""

from __future__ import annotations

import re
from pathlib import Path

from fastapi import HTTPException

from app.config import ATELIER_ROOT
from app.markdown.page_cache import file_cache_key, render_cached
from app.markdown.render import (
    dedupe_duplicate_headings,
    extract_wiki_index_body,
    markdown_to_html,
    postprocess_content_html,
    rewrite_wiki_links_markdown,
    strip_wiki_details_blocks,
    wiki_inpage_toc_from_html,
)

WIKI_DIR = ATELIER_ROOT / "Wiki"

_WIKI_BOILERPLATE_RES = (
    re.compile(r"基于.*README.*生成", re.I),
    re.compile(r"请参考源仓库", re.I),
    re.compile(r"如需最新详细信息", re.I),
    re.compile(r"wiki\s*页面基于", re.I),
    re.compile(r"此\s*wiki\s*页面基于", re.I),
    re.compile(r"本文档基于.*仓库", re.I),
    re.compile(r"文档内容生成", re.I),
)
_WIKI_SKIP_SECTION_RE = re.compile(
    r"^##\s*(相关文件|相关链接|Relevant\s*Files?|Source\s*Files?|参考资料)\s*$",
    re.I,
)
_WIKI_GITHUB_LINK_RE = re.compile(
    r"\[([^\]]+)\]\((https?://(?:www\.)?(?:github|gitee)\.com/[^)]+)\)",
    re.I,
)
_WIKI_DETAILS_MD_RE = re.compile(
    r"<details>[\s\S]*?</details>\s*",
    re.I,
)


def sanitize_wiki_markdown(raw: str, wiki_slug: str) -> str:
    raw = strip_wiki_details_blocks(raw)
    raw = _WIKI_DETAILS_MD_RE.sub("", raw)
    out: list[str] = []
    skip_section = False
    for line in raw.splitlines():
        if _WIKI_SKIP_SECTION_RE.match(line.strip()):
            skip_section = True
            continue
        if skip_section:
            if line.startswith("## "):
                skip_section = False
            else:
                continue
        stripped = line.strip()
        if any(p.search(stripped) for p in _WIKI_BOILERPLATE_RES):
            continue
        if re.match(r"^\*?\s*Sources?:", stripped, re.I):
            continue
        if re.match(r"^[-*]\s*\[README\.md\]", stripped, re.I):
            continue
        if re.match(r"^[-*]\s*\[.*README\.md.*\]\(https?://", stripped, re.I):
            continue
        line = _WIKI_GITHUB_LINK_RE.sub(r"\1", line)
        out.append(line)
    text = "\n".join(out).strip()
    text = rewrite_wiki_links_markdown(text, wiki_slug)
    text = dedupe_duplicate_headings(text)
    return text + "\n" if text else ""


def sanitize_wiki_html(html: str) -> str:
    html = re.sub(
        r"<details>[\s\S]*?Relevant\s+source\s+files[\s\S]*?</details>\s*",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<p>[^<]*(?:基于|参考).*README[^<]*(?:生成|源仓库)[^<]*</p>",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<p>\s*<em>?Sources?:[^<]*</em>?\s*</p>",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<a\s+href="https?://(?:www\.)?(?:github|gitee)\.com/[^"]*"[^>]*>(.*?)</a>',
        r"\1",
        html,
        flags=re.I,
    )
    html = re.sub(r"<p>\s*</p>", "", html)
    return html


def _read_wiki_raw(wiki_slug: str, page: str) -> str:
    safe = Path(page).name
    file_path = WIKI_DIR / wiki_slug / safe
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Wiki page not found")
    if file_path.resolve().parent != (WIKI_DIR / wiki_slug).resolve():
        raise HTTPException(status_code=404, detail="Wiki page not found")
    return file_path.read_text(encoding="utf-8")


def _render_wiki_markdown_impl(wiki_slug: str, page: str) -> dict:
    safe = Path(page).name
    raw = _read_wiki_raw(wiki_slug, page)
    is_index = safe == "index.md"

    if is_index:
        body_raw = extract_wiki_index_body(raw)
    else:
        body_raw = raw

    body_raw = re.sub(r"<!--\s*wiki_page_id:[^>]*-->", "", body_raw, flags=re.I)
    body_raw = strip_wiki_details_blocks(body_raw)
    body_raw = sanitize_wiki_markdown(body_raw, wiki_slug)
    html = markdown_to_html(body_raw)
    html = sanitize_wiki_html(html)
    html, _ = postprocess_content_html(
        html, wiki_slug=wiki_slug, demote_h1=not is_index
    )

    inpage_toc = [] if is_index else wiki_inpage_toc_from_html(html)

    return {
        "content_html": html,
        "wiki_is_index": is_index,
        "wiki_inpage_toc": inpage_toc,
    }


def render_wiki_markdown(wiki_slug: str, page: str) -> dict:
    """Return content_html and template flags (index mode, in-page TOC)."""
    safe = Path(page).name
    file_path = WIKI_DIR / wiki_slug / safe
    key = file_cache_key(file_path)
    return render_cached(
        key,
        f"wiki:{wiki_slug}:{safe}",
        lambda: _render_wiki_markdown_impl(wiki_slug, page),
    )


def _list_wiki_pages_impl(wiki_slug: str) -> list[dict[str, str]]:
    index_path = WIKI_DIR / wiki_slug / "index.md"
    if not index_path.is_file():
        return []
    link_re = re.compile(r"^- \[(.+?)\]\(\./(.+?)\)\s*$")
    pages: list[dict[str, str]] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = link_re.match(line.strip())
        if match:
            page_file = match.group(2)
            pages.append({
                "title": match.group(1),
                "page": page_file,
                "view_url": f"/docs/{wiki_slug}/{page_file}",
            })
    return pages


def list_wiki_pages(wiki_slug: str) -> list[dict[str, str]]:
    index_path = WIKI_DIR / wiki_slug / "index.md"
    key = file_cache_key(index_path)
    return render_cached(
        key,
        f"wiki-index:{wiki_slug}",
        lambda: _list_wiki_pages_impl(wiki_slug),
    )


def build_wiki_doc_nav(wiki_slug: str, page: str) -> dict:
    """Current wiki TOC, prev/next links, and index URL for doc templates."""
    pages = list_wiki_pages(wiki_slug)
    index_url = f"/docs/{wiki_slug}/index.md"
    safe_page = Path(page).name
    idx = next((i for i, p in enumerate(pages) if p["page"] == safe_page), None)

    doc_pages: list[dict[str, str | bool]] = []
    for i, entry in enumerate(pages):
        doc_pages.append({**entry, "is_current": i == idx})

    wiki_prev = pages[idx - 1] if idx is not None and idx > 0 else None
    wiki_next = pages[idx + 1] if idx is not None and idx < len(pages) - 1 else None
    doc_title = pages[idx]["title"] if idx is not None else safe_page.removesuffix(".md")

    return {
        "wiki_doc_pages": doc_pages,
        "wiki_prev": wiki_prev,
        "wiki_next": wiki_next,
        "wiki_index_url": index_url,
        "wiki_doc_title": doc_title,
    }
