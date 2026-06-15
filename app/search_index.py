"""Site-wide search index for header search."""

from __future__ import annotations

from functools import lru_cache

from app.constants import UI
from app.markdown.wiki import list_wiki_pages
from app.projects import get_all_projects
from app.travel_catalog import load_travel_trips
from site_data import build_data_hubs, load_all_blog_posts, load_site_data


def _item(
    title: str,
    url: str,
    group: str,
    *,
    subtitle: str = "",
    keywords: str = "",
) -> dict[str, str]:
    kw_parts = [title, subtitle, keywords, group]
    return {
        "title": title.strip(),
        "url": url,
        "group": group,
        "subtitle": subtitle.strip(),
        "keywords": " ".join(p for p in kw_parts if p).lower(),
    }


@lru_cache(maxsize=1)
def build_site_search_index() -> tuple[dict, ...]:
    items: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    def add(**kwargs) -> None:
        entry = _item(**kwargs)
        url = entry["url"]
        if not url or url in seen_urls:
            return
        seen_urls.add(url)
        items.append(entry)

    from app.context import build_wiki_nav

    try:
        data = load_site_data()
        hubs = build_data_hubs(data, len(get_all_projects()))
        nav = build_wiki_nav(hubs)
    except Exception:
        hubs = []
        nav = build_wiki_nav([])

    for group in nav:
        g_label = group.get("label", "导航")
        for link in group.get("children") or []:
            add(
                title=link.get("label", ""),
                url=link.get("url", ""),
                group=g_label,
            )

    for hub in hubs:
        if hub.get("url"):
            add(
                title=hub.get("label", hub.get("id", "")),
                url=hub["url"],
                group=UI.get("label_data_portal", "数据分类"),
                subtitle=hub.get("description", "") or hub.get("id", ""),
            )

    add(title=UI["label_all_projects_page"], url="/projects", group="项目")
    add(
        title=UI["link_framework_guides"],
        url="/blog/series/framework",
        group="博客",
        subtitle="Framework 技术栈",
    )
    add(
        title=UI.get("link_algorithm_guides", "Algorithm 算法与刷题"),
        url="/blog/series/algorithm",
        group="博客",
        subtitle="Algorithm 专题",
    )
    add(
        title=UI.get("link_hotspot_series", "热点专题"),
        url="/blog/series/hotspot",
        group="博客",
        subtitle=UI.get("label_blog_hotspot", "热点"),
    )

    for project in get_all_projects():
        tags = " ".join(project.get("tags") or [])
        add(
            title=project.get("title", project.get("id", "")),
            url=f"/project/{project['id']}",
            group="项目",
            subtitle=project.get("summary", "") or project.get("category", ""),
            keywords=f"{project.get('category', '')} {tags}",
        )
        demo_url = project.get("demo_url")
        if demo_url:
            add(
                title=f"{project.get('title', project.get('id', ''))} · 录屏演示",
                url=demo_url,
                group="演示",
                subtitle=project.get("summary", ""),
                keywords=f"nyxviz demo {tags}",
            )
        wiki_slug = project.get("wiki_slug")
        if not wiki_slug:
            continue
        for page in list_wiki_pages(wiki_slug):
            add(
                title=page.get("title", ""),
                url=page.get("view_url", ""),
                group="Wiki",
                subtitle=project.get("title", wiki_slug),
                keywords=wiki_slug,
            )

    for trip in load_travel_trips():
        add(
            title=trip.get("title", ""),
            url=trip.get("url", ""),
            group=UI.get("label_travel", "个人旅游"),
            subtitle=trip.get("summary", "") or trip.get("date", ""),
        )

    for post in load_all_blog_posts():
        slug = post.get("slug")
        if not slug:
            continue
        series = post.get("series", "")
        series_label = {"framework": "Framework", "algorithm": "Algorithm"}.get(
            series, series
        )
        add(
            title=post.get("title", slug),
            url=f"/blog/{slug}",
            group="博客",
            subtitle=f"{series_label} · {post.get('category', '')}".strip(" ·"),
            keywords=f"{series} {post.get('stack', '')} {post.get('topic_path', '')}",
        )

    return tuple(items)


def clear_search_index_cache() -> None:
    build_site_search_index.cache_clear()
