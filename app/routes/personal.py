from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.constants import HTML_CACHE_HEADERS
from app.context import site_context, templates
from app.personal import load_personal, personal_stats

router = APIRouter()


@router.get("/personal", response_class=HTMLResponse)
async def personal_page(request: Request):
    personal = load_personal()
    return templates.TemplateResponse(
        request=request,
        name="personal.html",
        context={
            **site_context(),
            "page_personal": True,
            "personal": personal,
            "personal_stats": personal_stats(personal),
        },
        headers=HTML_CACHE_HEADERS,
    )
