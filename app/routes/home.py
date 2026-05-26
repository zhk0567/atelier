from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.constants import HTML_CACHE_HEADERS
from app.context import projects_with_thumbs, site_context, templates
from app.projects import get_all_projects, get_pinned_projects
from site_data import list_algorithm_posts, list_framework_posts, list_hotspot_posts

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    ctx = site_context()
    pinned = projects_with_thumbs(get_pinned_projects(), ctx["wiki_assets"])
    framework_posts = list_framework_posts(include_draft=True)
    algorithm_posts = list_algorithm_posts(include_draft=True)
    algorithm_published = sum(
        1 for p in algorithm_posts if p.get("status") == "published"
    )
    hotspot_posts = list_hotspot_posts(include_draft=False)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            **ctx,
            "page_home": True,
            "projects": pinned,
            "project_count": len(pinned),
            "total_project_count": len(get_all_projects()),
            "framework_series_url": "/blog/series/framework",
            "algorithm_series_url": "/blog/series/algorithm",
            "framework_count": len(framework_posts),
            "algorithm_count": len(algorithm_posts),
            "algorithm_published_count": algorithm_published,
            "hotspot_series_url": "/blog/series/hotspot",
            "hotspot_count": len(hotspot_posts),
        },
        headers=HTML_CACHE_HEADERS,
    )
