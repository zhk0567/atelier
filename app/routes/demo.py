"""Standalone demo pages (embedded static apps)."""

from __future__ import annotations

from urllib.parse import urlencode

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.config import nyxviz_video_path

router = APIRouter()


@router.get("/demo/nyxviz-video")
async def nyxviz_video_demo(request: Request):
    """Redirect to the Vite-built NyxViz page (full viewport, no site chrome)."""
    params = dict(request.query_params)
    params.setdefault("record", "1")
    params.setdefault("scene", "intro")
    target = nyxviz_video_path() + "?" + urlencode(params)
    return RedirectResponse(url=target, status_code=302)
