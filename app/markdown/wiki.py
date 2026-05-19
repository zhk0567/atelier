"""Wiki page markdown sanitization and HTML rendering."""

from __future__ import annotations

import re
from pathlib import Path

import markdown
from fastapi import HTTPException

from app.config import ATELIER_ROOT

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


def sanitize_wiki_markdown(raw: str) -> str:
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
        line = re.sub(r"\[([^\]]+)\]\(\./[^)]+\)", r"\1", line)
        out.append(line)
    return "\n".join(out).strip() + "\n"


def sanitize_wiki_html(html: str) -> str:
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


def render_wiki_markdown(wiki_slug: str, page: str) -> str:
    safe = Path(page).name
    file_path = WIKI_DIR / wiki_slug / safe
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Wiki page not found")
    if file_path.resolve().parent != (WIKI_DIR / wiki_slug).resolve():
        raise HTTPException(status_code=404, detail="Wiki page not found")
    raw = file_path.read_text(encoding="utf-8")
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
    raw = sanitize_wiki_markdown(raw)
    html = markdown.markdown(raw, extensions=["tables", "fenced_code", "nl2br"])
    return sanitize_wiki_html(html)


def list_wiki_pages(wiki_slug: str) -> list[dict[str, str]]:
    index_path = WIKI_DIR / wiki_slug / "index.md"
    if not index_path.is_file():
        return []
    link_re = re.compile(r"^- \[(.+?)\]\(\./(.+?)\)\s*$")
    pages: list[dict[str, str]] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = link_re.match(line.strip())
        if match:
            pages.append({
                "title": match.group(1),
                "view_url": f"/docs/{wiki_slug}/{match.group(2)}",
            })
    return pages
