import re

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.constants import HTML_NO_CACHE
from app.context import site_context, templates
from app.markdown.blog import framework_guide_nav, render_blog_markdown
from site_data import BLOG_DIR, list_framework_posts, load_all_blog_posts

router = APIRouter()
_BLOG_FRONTMATTER_RE = re.compile(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n", re.DOTALL)


@router.get("/blog", response_class=HTMLResponse)
async def blog_index(request: Request):
    posts = load_all_blog_posts()
    framework = [p for p in posts if p.get("series") == "framework"]
    other = [p for p in posts if p.get("series") != "framework"]
    return templates.TemplateResponse(
        request=request,
        name="blog_index.html",
        context={
            **site_context(),
            "posts_other": other,
            "framework_count": len(framework),
            "framework_series_url": "/blog/series/framework",
        },
        headers=HTML_NO_CACHE,
    )


@router.get("/blog/series/framework", response_class=HTMLResponse)
async def blog_series_framework(request: Request):
    posts = list_framework_posts()
    by_category: dict[str, list[dict]] = {}
    for p in posts:
        cat = p.get("category", "Other")
        by_category.setdefault(cat, []).append(p)
    for items in by_category.values():
        items.sort(key=lambda x: x.get("title", ""))
    n = len(posts)
    series_lead = (
        f"已发布 {n} 篇官方指南（单页含基础篇与子工程实战）。"
        "左侧导航进入各栈；正文采用侧栏目录 + 章节锚点。"
    )
    return templates.TemplateResponse(
        request=request,
        name="blog_series.html",
        context={
            **site_context(),
            "series_title": "Framework 技术栈",
            "series_lead": series_lead,
            "by_category": sorted(by_category.items(), key=lambda x: x[0]),
            "wiki_overview_url": "/docs/Framework/index.md",
        },
        headers=HTML_NO_CACHE,
    )


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str):
    post, html_body = render_blog_markdown(slug)
    series_url = ""
    guide_nav: list[dict[str, str]] = []
    if post.get("series") == "framework":
        series_url = "/blog/series/framework"
        folder = post.get("folder", "")
        index_path = BLOG_DIR / folder / "index.md"
        if index_path.is_file():
            raw = index_path.read_text(encoding="utf-8")
            raw = _BLOG_FRONTMATTER_RE.sub("", raw, count=1)
            guide_nav = framework_guide_nav(raw)
    return templates.TemplateResponse(
        request=request,
        name="blog_post.html",
        context={
            **site_context(),
            "post": post,
            "content_html": html_body,
            "series_url": series_url,
            "guide_nav": guide_nav,
            "is_framework_guide": post.get("series") == "framework",
        },
        headers=HTML_NO_CACHE,
    )
