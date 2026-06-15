"""Standalone demo pages (embedded static apps)."""

from __future__ import annotations

from urllib.parse import urlencode

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response

from app.config import nyxviz_data_base, nyxviz_static_figures_only, nyxviz_video_path
from app.constants import HTML_CACHE_HEADERS

router = APIRouter()


@router.get("/static/nyxviz/runtime-config.js", include_in_schema=False)
async def nyxviz_runtime_config():
    """Runtime Nyx config: static figures mode and optional .dat base URL."""
    static_only = nyxviz_static_figures_only()
    base = nyxviz_data_base()
    safe = base.replace("\\", "\\\\").replace('"', '\\"')
    static_js = "true" if static_only else "false"
    body = (
        f"window.__NYX_STATIC_ONLY__={static_js};\n"
        f'window.__NYX_DATA_BASE__="{safe}";\n'
    )
    return Response(
        content=body,
        media_type="application/javascript",
        headers=HTML_CACHE_HEADERS,
    )


@router.get("/demo/nyxviz-video")
async def nyxviz_video_demo(request: Request):
    """Redirect to the Vite-built NyxViz page (full viewport, no site chrome)."""
    params = dict(request.query_params)
    params.setdefault("record", "1")
    params.setdefault("browse", "1")
    params.setdefault("scene", "intro")
    target = nyxviz_video_path() + "?" + urlencode(params)
    return RedirectResponse(url=target, status_code=302)
