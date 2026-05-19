from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.config import pinned_project_ids
from app.constants import HTML_NO_CACHE
from app.context import site_context, templates
from app.markdown.wiki import list_wiki_pages
from app.projects import get_all_projects, get_project

router = APIRouter()


@router.get("/projects", response_class=HTMLResponse)
async def projects_list(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="projects.html",
        context={
            **site_context(),
            "projects": get_all_projects(),
            "pinned_ids": set(pinned_project_ids()),
            "project_count": len(get_all_projects()),
        },
        headers=HTML_NO_CACHE,
    )


@router.get("/project/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        request=request,
        name="project.html",
        context={
            **site_context(),
            "project": project,
            "wiki_pages": list_wiki_pages(project["wiki_slug"]),
            "wiki_index_url": f"/docs/{project['wiki_slug']}/index.md",
        },
        headers=HTML_NO_CACHE,
    )
