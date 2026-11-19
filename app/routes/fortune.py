"""Temple fortune sticks — immersive one-screen ritual (entertainment)."""

from __future__ import annotations

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.constants import HTML_CACHE_HEADERS, SITE_NAME, SITE_TITLE, UI
from app.context import load_wiki_assets, templates
from app.fortune_data import (
    FORTUNE_PATH,
    FORTUNE_TITLE,
    draw_any,
    fortune_bootstrap,
)

router = APIRouter()


def _resolve_icons() -> dict[str, str]:
    assets = load_wiki_assets() or {}
    fallback = assets.get("crafting_table", "/static/img/wiki/crafting_table.png")
    return {
        "planks": assets.get("oak_planks", fallback),
        "stone": assets.get("stone", fallback),
        "cobble": assets.get("cobblestone", fallback),
        "grass": assets.get("grass_block", fallback),
        "dirt": assets.get("dirt", fallback),
        "book": assets.get("item_book", fallback),
        "compass": assets.get("item_compass", fallback),
        "seal": assets.get("item_book", fallback),
    }


@router.get(FORTUNE_PATH, response_class=HTMLResponse)
async def fortune_page(request: Request):
    icons = _resolve_icons()
    boot = fortune_bootstrap()
    client_boot = {
        "disclaimer": boot["disclaimer"],
        "levels": boot["levels"],
        "draw_url": f"{FORTUNE_PATH}/api/draw",
    }
    return templates.TemplateResponse(
        request=request,
        name="fortune.html",
        context={
            "site_name": SITE_NAME,
            "site_title": SITE_TITLE,
            "ui": UI,
            "fortune_title": FORTUNE_TITLE,
            "fortune_path": FORTUNE_PATH,
            "fortune_boot": client_boot,
            "fortune_icons": icons,
            "fortune_disclaimer": boot["disclaimer"],
        },
        headers=HTML_CACHE_HEADERS,
    )


@router.get(f"{FORTUNE_PATH}/api/draw")
async def fortune_draw(theme: str = Query("", max_length=64)):
    # theme query ignored — 摇到什么是什么
    del theme
    payload = draw_any()
    if not payload:
        return JSONResponse({"ok": False, "error": "empty_pool"}, status_code=500)
    return JSONResponse(
        {"ok": True, **payload},
        headers={"Cache-Control": "no-store"},
    )
