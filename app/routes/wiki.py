from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.constants import HTML_CACHE_HEADERS
from app.context import site_context, templates
from app.markdown.wiki import build_wiki_doc_nav, render_wiki_markdown
from app.projects import get_all_projects

router = APIRouter()


@router.get("/docs/{wiki_slug}/{page}", response_class=HTMLResponse)
async def wiki_doc(request: Request, wiki_slug: str, page: str):
    project = next((p for p in get_all_projects() if p["wiki_slug"] == wiki_slug), None)
    rendered = render_wiki_markdown(wiki_slug, page)
    doc_nav = build_wiki_doc_nav(wiki_slug, page)
    return templates.TemplateResponse(
        request=request,
        name="wiki.html",
        context={
            **site_context(),
            "wiki_slug": wiki_slug,
            "page": page,
            **rendered,
            "project": project,
            "project_url": f"/project/{project['id']}" if project else "/",
            **doc_nav,
        },
        headers=HTML_CACHE_HEADERS,
    )


@router.get("/wiki", include_in_schema=False)
@router.get("/wiki/{path:path}", include_in_schema=False)
async def wiki_raw_forbidden(path: str = ""):
    raise HTTPException(status_code=404, detail="Not found")
