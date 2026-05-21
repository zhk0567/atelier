from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.constants import HTML_CACHE_HEADERS
from app.context import projects_with_thumbs, site_context, templates
from app.projects import get_all_projects, get_pinned_projects

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    ctx = site_context()
    pinned = projects_with_thumbs(get_pinned_projects(), ctx["wiki_assets"])
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            **ctx,
            "page_home": True,
            "projects": pinned,
            "project_count": len(pinned),
            "total_project_count": len(get_all_projects()),
        },
        headers=HTML_CACHE_HEADERS,
    )
