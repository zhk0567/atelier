from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.constants import HTML_NO_CACHE
from app.context import site_context, templates
from app.projects import get_all_projects, get_pinned_projects

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    pinned = get_pinned_projects()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            **site_context(),
            "projects": pinned,
            "project_count": len(pinned),
            "total_project_count": len(get_all_projects()),
        },
        headers=HTML_NO_CACHE,
    )
