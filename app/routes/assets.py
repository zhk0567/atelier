"""Favicon, API probe, wallpapers."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse

from app.config import ATELIER_ROOT
from app.constants import HTML_NO_CACHE, SITE_NAME, SITE_TITLE
from app.constants import WALLPAPER_CACHE_HEADERS
from app.context import DATA_DIR, list_wallpapers, media_type_for_path, wallpaper_paths

router = APIRouter()


@router.get("/api/site", include_in_schema=False)
@router.get("/atelier-site.json", include_in_schema=False)
async def api_site():
    return JSONResponse(
        {
            "site_name": SITE_NAME,
            "site_title": SITE_TITLE,
            "main_py": str((ATELIER_ROOT / "main.py").resolve()),
            "identity_json": str((ATELIER_ROOT / "site_identity.json").resolve()),
        },
        headers=HTML_NO_CACHE,
    )


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.svg", status_code=301)


@router.get("/wallpaper/{wp_id}", include_in_schema=False)
async def serve_wallpaper(wp_id: str):
    path = wallpaper_paths().get(wp_id)
    if not path or not path.is_file():
        raise HTTPException(status_code=404, detail="Wallpaper not found")
    try:
        path.resolve().relative_to(DATA_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=404, detail="Wallpaper not found") from None
    return FileResponse(
        path,
        media_type=media_type_for_path(path),
        headers=WALLPAPER_CACHE_HEADERS,
    )
