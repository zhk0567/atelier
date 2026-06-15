from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.constants import HTML_CACHE_HEADERS
from app.context import framework_stack_thumb_url, site_context, templates
from app.markdown.blog import render_blog_markdown
from app.markdown.render import (
    filter_inpage_toc,
    framework_guide_nav,
    strip_blog_frontmatter,
    wiki_inpage_toc_from_html,
)
from site_data import (
    BLOG_DIR,
    course_notes_chapter_nav,
    list_algorithm_posts,
    list_framework_posts,
    list_hotspot_posts,
    list_standalone_series_posts,
    load_all_blog_posts,
    load_hotspot_manifest,
    standalone_series_label,
    standalone_series_meta,
    standalone_series_url,
)

router = APIRouter()

_KNOWN_BLOG_SERIES = frozenset({"framework", "algorithm", "hotspot", "course-notes", "topics"})


@router.get("/blog", response_class=HTMLResponse)
async def blog_index(request: Request):
    posts = load_all_blog_posts()
    framework = [p for p in posts if p.get("series") == "framework"]
    algorithm = [p for p in posts if p.get("series") == "algorithm"]
    hotspot = [p for p in posts if p.get("series") == "hotspot"]
    course_notes = [p for p in posts if p.get("series") == "course-notes"]
    topics = [p for p in posts if p.get("series") == "topics"]
    other = [
        p
        for p in posts
        if p.get("series") not in _KNOWN_BLOG_SERIES
    ]
    algo_all = list_algorithm_posts(include_draft=True)
    return templates.TemplateResponse(
        request=request,
        name="blog_index.html",
        context={
            **site_context(),
            "posts_other": other,
            "course_notes_posts": sorted(
                course_notes,
                key=lambda p: (p.get("chapter") or 0, p.get("title", "")),
            ),
            "topics_posts": topics,
            "framework_count": len(framework),
            "framework_series_url": "/blog/series/framework",
            "algorithm_count": len(algo_all),
            "algorithm_published_count": len(algorithm),
            "algorithm_series_url": "/blog/series/algorithm",
            "hotspot_posts": hotspot,
            "hotspot_count": len(hotspot),
            "hotspot_series_url": "/blog/series/hotspot",
            "course_notes_count": len(course_notes),
            "course_notes_series_url": "/blog/series/course-notes",
            "topics_count": len(topics),
            "topics_series_url": "/blog/series/topics",
        },
        headers=HTML_CACHE_HEADERS,
    )


def _group_framework_posts(posts: list[dict]) -> list[tuple[str, list[tuple[str, list[dict]]]]]:
    tree: dict[str, dict[str, list[dict]]] = {}
    for p in posts:
        cat = p.get("category", "Other")
        stack = p.get("stack", "Other")
        tree.setdefault(cat, {}).setdefault(stack, []).append(p)
    out: list[tuple[str, list[tuple[str, list[dict]]]]] = []
    for cat in sorted(tree.keys()):
        stacks: list[tuple[str, list[dict]]] = []
        for stack in sorted(tree[cat].keys()):
            items = sorted(tree[cat][stack], key=lambda x: x.get("title", ""))
            stacks.append((stack, items))
        out.append((cat, stacks))
    return out


@router.get("/blog/series/framework", response_class=HTMLResponse)
async def blog_series_framework(request: Request):
    posts = list_framework_posts(include_draft=True)
    ctx = site_context()
    assets = ctx["wiki_assets"]
    published_n = sum(1 for p in posts if p.get("status") == "published")
    draft_n = len(posts) - published_n
    series_lead = (
        f"共 {len(posts)} 篇指南（已发布 {published_n} 篇"
        + (f"，连载稿 {draft_n} 篇" if draft_n else "")
        + "）。按分类与技术栈浏览；正文含侧栏目录与章节锚点。"
    )
    by_category = _group_framework_posts(posts)
    return templates.TemplateResponse(
        request=request,
        name="blog_series.html",
        context={
            **ctx,
            "series_title": "Framework 技术栈",
            "series_lead": series_lead,
            "series_note": "单页含完整基础篇与 Framework 子工程实战。",
            "by_category": by_category,
            "series_mode": "framework",
            "framework_stack_thumb": lambda stack, cat: framework_stack_thumb_url(
                stack, cat, assets
            ),
            "wiki_overview_url": "/docs/Framework/index.md",
            "github_repo_url": "https://github.com/zhk0567/Framework",
        },
        headers=HTML_CACHE_HEADERS,
    )


def _group_algorithm_posts(posts: list[dict]) -> list[tuple[str, list[tuple[str, list[dict]]]]]:
    tree: dict[str, dict[str, list[dict]]] = {}
    for p in posts:
        cat = p.get("category", "Other")
        tp = p.get("topic_path", "") or "overview"
        parts = tp.split("/")
        if len(parts) >= 2:
            group = "/".join(parts[:2])
        elif parts:
            group = parts[0]
        else:
            group = "overview"
        tree.setdefault(cat, {}).setdefault(group, []).append(p)
    out: list[tuple[str, list[tuple[str, list[dict]]]]] = []
    for cat in sorted(tree.keys()):
        groups: list[tuple[str, list[dict]]] = []
        for group in sorted(tree[cat].keys()):
            items = sorted(tree[cat][group], key=lambda x: x.get("title", ""))
            groups.append((group, items))
        out.append((cat, groups))
    return out


@router.get("/blog/series/algorithm", response_class=HTMLResponse)
async def blog_series_algorithm(request: Request):
    posts = list_algorithm_posts(include_draft=True)
    ctx = site_context()
    assets = ctx["wiki_assets"]
    published_n = sum(1 for p in posts if p.get("status") == "published")
    draft_n = len(posts) - published_n
    series_lead = (
        f"共 {len(posts)} 篇专题指南（已发布 {published_n} 篇"
        + (f"，连载稿 {draft_n} 篇" if draft_n else "")
        + "）。Python 与 C++ 镜像同篇；单题 LeetCode 题解见 GitHub 仓库。"
    )
    by_category = _group_algorithm_posts(posts)
    recommended_slugs = (
        "overview",
        "algo-graph",
        "algo-dynamic-programming",
        "algo-sliding-window",
        "algo-sorting",
        "ds-linear",
        "algo-graph-shortest-path",
        "iv-top-frequent",
    )
    posts_by_slug = {p["slug"]: p for p in posts}
    recommended_starts = [posts_by_slug[s] for s in recommended_slugs if s in posts_by_slug]
    return templates.TemplateResponse(
        request=request,
        name="blog_series.html",
        context={
            **ctx,
            "series_title": "Algorithm 算法与刷题",
            "series_lead": series_lead,
            "series_note": "专题级双语教程，对照 zhk0567/Algorithm 仓库 notes.md 扩写；不含逐题博文。",
            "by_category": by_category,
            "series_mode": "algorithm",
            "recommended_starts": recommended_starts,
            "wiki_overview_url": "https://github.com/zhk0567/Algorithm",
            "github_repo_url": "https://github.com/zhk0567/Algorithm",
            "framework_stack_thumb": lambda stack, cat: assets.get("item_book", ""),
        },
        headers=HTML_CACHE_HEADERS,
    )


@router.get("/blog/series/hotspot", response_class=HTMLResponse)
async def blog_series_hotspot(request: Request):
    manifest = load_hotspot_manifest()
    posts = list_hotspot_posts(include_draft=False)
    ctx = site_context()
    ui = ctx["ui"]
    assets = ctx["wiki_assets"]
    return templates.TemplateResponse(
        request=request,
        name="blog_series_list.html",
        context={
            **ctx,
            "series_title": manifest.get("title") or ui.get("label_blog_hotspot", "热点"),
            "series_lead": manifest.get("description") or ui.get("blog_hotspot_lead", ""),
            "posts": posts,
            "thumb_url": assets.get("item_map", ""),
        },
        headers=HTML_CACHE_HEADERS,
    )


def _standalone_series_page(
    request: Request,
    series_id: str,
    *,
    thumb_key: str,
) -> HTMLResponse:
    meta = standalone_series_meta().get(series_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Series not found")
    posts = list_standalone_series_posts(series_id, include_draft=False)
    ctx = site_context()
    assets = ctx["wiki_assets"]
    return templates.TemplateResponse(
        request=request,
        name="blog_series_list.html",
        context={
            **ctx,
            "series_title": meta.get("title") or series_id,
            "series_lead": meta.get("description") or "",
            "posts": posts,
            "thumb_url": assets.get(thumb_key, assets.get("item_book", "")),
        },
        headers=HTML_CACHE_HEADERS,
    )


@router.get("/blog/series/course-notes", response_class=HTMLResponse)
async def blog_series_course_notes(request: Request):
    return _standalone_series_page(request, "course-notes", thumb_key="item_book")


@router.get("/blog/series/topics", response_class=HTMLResponse)
async def blog_series_topics(request: Request):
    return _standalone_series_page(request, "topics", thumb_key="item_book")


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str):
    post, html_body = render_blog_markdown(slug)
    series = post.get("series", "")
    series_url = ""
    series_label = ""
    if series == "framework":
        series_url = "/blog/series/framework"
        series_label = "Framework"
    elif series == "algorithm":
        series_url = "/blog/series/algorithm"
        series_label = "Algorithm"
    elif series == "hotspot":
        series_url = "/blog/series/hotspot"
        series_label = standalone_series_label("hotspot") or "热点"
    elif series:
        series_url = standalone_series_url(series)
        series_label = standalone_series_label(series)

    guide_nav: list[dict[str, str]] = []
    if series in ("framework", "algorithm"):
        folder = post.get("folder", "")
        index_path = BLOG_DIR / folder / "index.md"
        if index_path.is_file():
            raw = index_path.read_text(encoding="utf-8")
            raw = strip_blog_frontmatter(raw)
            guide_nav = framework_guide_nav(raw)
    elif "toc" in post.get("features", []):
        depth = int(post.get("toc_depth") or 2)
        guide_nav = filter_inpage_toc(wiki_inpage_toc_from_html(html_body), depth)

    chapter_prev, chapter_next = course_notes_chapter_nav(slug, post)

    return templates.TemplateResponse(
        request=request,
        name="blog_post.html",
        context={
            **site_context(),
            "post": post,
            "content_html": html_body,
            "series_url": series_url,
            "series_label": series_label,
            "guide_nav": guide_nav,
            "is_framework_guide": series == "framework",
            "is_algorithm_guide": series == "algorithm",
            "is_hotspot": series == "hotspot",
            "is_course_notes": series == "course-notes",
            "is_topics": series == "topics",
            "chapter_prev": chapter_prev,
            "chapter_next": chapter_next,
        },
        headers=HTML_CACHE_HEADERS,
    )
