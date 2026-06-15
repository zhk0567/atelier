"""Shared Markdown → HTML pipeline for Wiki and Blog."""

from __future__ import annotations

import re

import markdown

from app.markdown.mermaid import apply_mermaid_blocks

MD_EXTENSIONS = ["tables", "fenced_code", "nl2br"]

_IMG_TAG_RE = re.compile(r"<img\s+([^>]*?)>", re.I)
_IMG_P_CAPTION_RE = re.compile(
    r"(<img\s[^>]*?/?>)\s*(?:<br\s*/>\s*)?<p>\s*<em>([^<]+)</em>\s*</p>",
    re.I,
)
_IMG_IN_P_CAPTION_RE = re.compile(
    r"<p>\s*(<img\s[^>]*?/?>)\s*<br\s*/>\s*<em>([^<]+)</em>\s*</p>",
    re.I,
)
_HEADING_TAG_RE = {
    "h2": re.compile(r"<h2(?:\s+id=\"[^\"]+\")?>([^<]+)</h2>", re.I),
    "h3": re.compile(r"<h3(?:\s+id=\"[^\"]+\")?>([^<]+)</h3>", re.I),
}
_HEADING_PLAIN_RE = {
    "h2": re.compile(r"<h2>([^<]+)</h2>", re.I),
    "h3": re.compile(r"<h3>([^<]+)</h3>", re.I),
}
_H1_RE = re.compile(r"<h1>([^<]*)</h1>", re.I)
_EXTERNAL_LINK_RE = re.compile(
    r'<a\s+href="(https?://[^"]+)"([^>]*)>',
    re.I,
)
_WIKI_DETAILS_RE = re.compile(
    r"<details>[\s\S]*?Relevant\s+source\s+files[\s\S]*?</details>",
    re.I,
)
_WIKI_REL_LINK_MD_RE = re.compile(r"\[([^\]]+)\]\(\./([^)]+)\)")
_WIKI_REL_LINK_HTML_RE = re.compile(
    r'<a\s+href="\./([^"]+)"([^>]*)>([^<]*)</a>',
    re.I,
)
_DUP_HEADING_MD_RE = re.compile(r"^(#{1,3})\s+(.+)$", re.M)


def heading_anchor(title: str) -> str:
    anchor = re.sub(r"\s+", "-", title.strip())
    anchor = re.sub(r"[^\w\u4e00-\u9fff\-]+", "", anchor)
    return anchor or "section"


def markdown_to_html(raw: str) -> str:
    return markdown.markdown(raw, extensions=MD_EXTENSIONS)


def _unique_anchor(title: str, used: set[str]) -> str:
    base = heading_anchor(title)
    aid = base
    n = 2
    while aid in used:
        aid = f"{base}-{n}"
        n += 1
    used.add(aid)
    return aid


def add_heading_ids(html: str, *tags: str) -> str:
    used: set[str] = set()
    for tag in tags or ("h2", "h3"):
        pattern = _HEADING_PLAIN_RE.get(tag)
        if not pattern:
            continue

        def repl(match: re.Match[str], t: str = tag) -> str:
            title = match.group(1)
            aid = _unique_anchor(title, used)
            return f'<{t} id="{aid}">{title}</{t}>'

        html = pattern.sub(repl, html)
    return html


def demote_extra_h1(html: str) -> str:
    """Keep first h1; later h1 become h2."""
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        inner = match.group(1)
        if count == 1:
            return f"<h1>{inner}</h1>"
        return f"<h2>{inner}</h2>"

    return _H1_RE.sub(repl, html)


def wrap_all_tables(html: str) -> str:
    parts: list[str] = []
    pos = 0
    for match in re.finditer(r"<table\b[\s\S]*?</table>", html, re.I):
        start = match.start()
        prefix = html[max(0, start - 50) : start]
        parts.append(html[pos:start])
        chunk = match.group(0)
        if "wiki-table-scroll" not in prefix:
            chunk = f'<div class="wiki-table-scroll">{chunk}</div>'
        parts.append(chunk)
        pos = match.end()
    parts.append(html[pos:])
    return "".join(parts)


def enhance_external_links(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        href = match.group(1)
        rest = match.group(2)
        if 'target=' in rest.lower():
            return match.group(0)
        return (
            f'<a href="{href}"{rest} target="_blank" '
            f'rel="noopener noreferrer">'
        )

    return _EXTERNAL_LINK_RE.sub(repl, html)


def enhance_lazy_images(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        attrs = match.group(1)
        if "loading=" in attrs.lower():
            return match.group(0)
        return f'<img loading="lazy" decoding="async" {attrs}>'

    return _IMG_TAG_RE.sub(repl, html)


def wrap_figure_captions(html: str) -> str:
    """Turn img + following em (or nl2br em in same p) into figure/figcaption."""

    def figure_block(img: str, cap: str) -> str:
        cap = cap.strip()
        if not cap.startswith("图"):
            return img
        return (
            f'<figure class="wiki-figure">{img}'
            f'<figcaption class="wiki-figure__caption">{cap}</figcaption></figure>'
        )

    def repl_p(match: re.Match[str]) -> str:
        return figure_block(match.group(1), match.group(2))

    def repl_block(match: re.Match[str]) -> str:
        block = figure_block(match.group(1), match.group(2))
        return block if block.startswith("<figure") else match.group(0)

    html = _IMG_IN_P_CAPTION_RE.sub(repl_p, html)
    return _IMG_P_CAPTION_RE.sub(repl_block, html)


def rewrite_wiki_links(html: str, wiki_slug: str) -> str:
    def repl(match: re.Match[str]) -> str:
        page = match.group(1)
        label = match.group(3)
        href = f"/docs/{wiki_slug}/{page}"
        return f'<a href="{href}"{match.group(2)}>{label}</a>'

    return _WIKI_REL_LINK_HTML_RE.sub(repl, html)


def rewrite_wiki_links_markdown(raw: str, wiki_slug: str) -> str:
    def repl(match: re.Match[str]) -> str:
        label, page = match.group(1), match.group(2)
        return f"[{label}](/docs/{wiki_slug}/{page})"

    return _WIKI_REL_LINK_MD_RE.sub(repl, raw)


def postprocess_content_html(
    html: str,
    *,
    wiki_slug: str | None = None,
    heading_tags: tuple[str, ...] = ("h2", "h3"),
    demote_h1: bool = False,
) -> tuple[str, bool]:
    if wiki_slug:
        html = rewrite_wiki_links(html, wiki_slug)
    if demote_h1:
        html = demote_extra_h1(html)
    html = add_heading_ids(html, *heading_tags)
    html = wrap_all_tables(html)
    html = enhance_external_links(html)
    html = wrap_figure_captions(html)
    html = enhance_lazy_images(html)
    html, has_mermaid = apply_mermaid_blocks(html)
    return html, has_mermaid


def render_fragment_markdown(raw: str) -> str:
    """Small markdown snippets (project features, etc.)."""
    if not raw.strip():
        return ""
    text = raw.strip()
    if not re.search(r"^[-*#]|\n[-*]|\*\*", text, re.M):
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if len(lines) > 1:
            text = "\n".join(f"- {ln}" if not ln.startswith(("-", "*")) else ln for ln in lines)
    html = markdown_to_html(text)
    html, _ = postprocess_content_html(html, heading_tags=())
    return html


def dedupe_duplicate_headings(raw: str) -> str:
    seen: set[tuple[str, str]] = set()
    out: list[str] = []
    for line in raw.splitlines():
        m = _DUP_HEADING_MD_RE.match(line)
        if m:
            key = (m.group(1), m.group(2).strip())
            if key in seen:
                continue
            seen.add(key)
        out.append(line)
    return "\n".join(out)


def strip_wiki_details_blocks(raw: str) -> str:
    return re.sub(
        r"<details>[\s\S]*?Relevant\s+source\s+files[\s\S]*?</details>\s*",
        "",
        raw,
        flags=re.I,
    )


def extract_wiki_index_body(raw: str) -> str:
    """Remove page index list from index.md; keep intro paragraphs."""
    out: list[str] = []
    skip_list = False
    for line in raw.splitlines():
        stripped = line.strip()
        if re.match(r"^##\s*页面索引", stripped):
            skip_list = True
            continue
        if skip_list:
            if stripped.startswith("## "):
                skip_list = False
                out.append(line)
            continue
        out.append(line)
    return "\n".join(out).strip()


def wiki_inpage_toc_from_html(html: str) -> list[dict[str, str]]:
    nav: list[dict[str, str]] = []
    for tag in ("h2", "h3"):
        for match in re.finditer(rf"<{tag}\s+id=\"([^\"]+)\"[^>]*>([^<]+)</{tag}>", html, re.I):
            nav.append({
                "title": match.group(2).strip(),
                "anchor": match.group(1),
                "level": tag,
            })
    return nav


def filter_inpage_toc(nav: list[dict[str, str]], depth: int = 2) -> list[dict[str, str]]:
    if depth >= 3:
        return nav
    return [item for item in nav if item.get("level") == "h2"]


# Blog helpers
_BLOG_FRONTMATTER_RE = re.compile(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n", re.DOTALL)
_BLOG_INLINE_TOC_RE = re.compile(r"^## 目录\s*\n(?:.*?\n)*?(?=^## )", re.MULTILINE)
_BLOG_EDITORIAL_SECTION_RE = re.compile(
    r"^##\s*(?:发布备忘|编辑备忘|内部备忘)\s*\n[\s\S]*?(?=^## |\Z)",
    re.MULTILINE,
)


def strip_blog_frontmatter(raw: str) -> str:
    return _BLOG_FRONTMATTER_RE.sub("", raw, count=1)


def strip_blog_editorial_sections(raw: str) -> str:
    return _BLOG_EDITORIAL_SECTION_RE.sub("", raw)


def strip_guide_inline_toc(raw: str) -> str:
    return _BLOG_INLINE_TOC_RE.sub("", raw, count=1)


def rewrite_blog_image_paths(raw: str, slug: str) -> str:
    return re.sub(
        r"!\[([^\]]*)\]\(images/([^)]+)\)",
        rf"![\1](/static/blog/{slug}/\2)",
        raw,
    )


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
