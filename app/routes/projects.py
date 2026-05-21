from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.config import pinned_project_ids
from app.constants import HTML_CACHE_HEADERS
from app.context import projects_with_thumbs, project_thumb_url, site_context, templates
from app.markdown.render import render_fragment_markdown
from app.markdown.wiki import list_wiki_pages
from app.projects import get_all_projects, get_project

router = APIRouter()


@router.get("/projects", response_class=HTMLResponse)
async def projects_list(request: Request):
    ctx = site_context()
    return templates.TemplateResponse(
        request=request,
        name="projects.html",
        context={
            **ctx,
            "projects": projects_with_thumbs(get_all_projects(), ctx["wiki_assets"]),
            "pinned_ids": set(pinned_project_ids()),
            "project_count": len(get_all_projects()),
        },
        headers=HTML_CACHE_HEADERS,
    )


@router.get("/project/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404)
    ctx = site_context()
    enriched = {**project, "thumb_url": project_thumb_url(project, ctx["wiki_assets"])}
    features = enriched.get("feature_lines") or enriched.get("highlights") or []
    if isinstance(features, list) and features:
        raw = "\n".join(
            ln if ln.strip().startswith(("-", "*")) else f"- {ln}"
            for ln in features
            if str(ln).strip()
        )
        enriched["features_html"] = render_fragment_markdown(raw)
    else:
        enriched["features_html"] = ""
    return templates.TemplateResponse(
        request=request,
        name="project.html",
        context={
            **ctx,
            "project": enriched,
            "wiki_pages": list_wiki_pages(project["wiki_slug"]),
            "wiki_index_url": f"/docs/{project['wiki_slug']}/index.md",
        },
        headers=HTML_CACHE_HEADERS,
    )
