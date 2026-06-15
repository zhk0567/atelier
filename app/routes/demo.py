"""Standalone demo pages (embedded static apps)."""

from __future__ import annotations

from urllib.parse import urlencode

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.config import nyxviz_video_path
from app.constants import HTML_CACHE_HEADERS
from app.context import site_context, templates

router = APIRouter()


@router.get("/demo/nyxviz-video", response_class=HTMLResponse)
async def nyxviz_video_demo(request: Request):
    params = dict(request.query_params)
    params.setdefault("record", "1")
    params.setdefault("scene", "intro")
    iframe_src = nyxviz_video_path() + "?" + urlencode(params)
    ctx = site_context()
    return templates.TemplateResponse(
        request=request,
        name="nyxviz_video.html",
        context={
            **ctx,
            "iframe_src": iframe_src,
            "scene": params.get("scene", "intro"),
        },
        headers=HTML_CACHE_HEADERS,
    )
