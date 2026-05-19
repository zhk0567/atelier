from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.constants import HTML_NO_CACHE
from app.context import site_context, templates
from site_data import get_browse_page

router = APIRouter()


@router.get("/browse/{hub_id}", response_class=HTMLResponse)
async def browse_hub(request: Request, hub_id: str):
    page = get_browse_page(hub_id)
    if not page:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        request=request,
        name="browse.html",
        context={
            **site_context(),
            **page,
            "item_count": sum(
                len(s.get("items", [])) for s in page.get("sections", [])
            )
            if page.get("sections")
            else len(page.get("items", [])),
        },
        headers=HTML_NO_CACHE,
    )
