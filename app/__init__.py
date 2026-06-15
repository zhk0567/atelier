"""FastAPI application factory."""

from __future__ import annotations

import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from app.config import ATELIER_ROOT, MC_VTUBER_DIR, mc_vtuber_live2d_ready
from app.static_files import CachedStaticFiles
from app.constants import MC_VTUBER_CACHE_HEADERS, SITE_NAME, SITE_TITLE
from app.middleware import register_security_middleware
from app.routes import assets, blog, browse, demo, home, projects, travel, wiki


def _win_asyncio_exception_handler(loop: asyncio.AbstractEventLoop, context: dict) -> None:
    if isinstance(context.get("exception"), ConnectionResetError):
        return
    loop.default_exception_handler(context)


@asynccontextmanager
async def _lifespan(app: FastAPI):
    main_path = Path(__file__).resolve().parent.parent / "main.py"
    print(f"[atelier] loaded app from: {main_path}", flush=True)
    print(f"[atelier] SITE_NAME={SITE_NAME!r} SITE_TITLE={SITE_TITLE!r}", flush=True)
    prev_handler = None
    if sys.platform == "win32":
        loop = asyncio.get_running_loop()
        prev_handler = loop.get_exception_handler()
        loop.set_exception_handler(_win_asyncio_exception_handler)
    try:
        from app.context import clear_context_cache, list_wallpapers, load_wiki_assets
        from app.media_derivatives import warmup_media_derivatives
        from app.projects import get_all_projects
        from app.travel_catalog import load_travel_trips
        from site_data import load_site_data

        media_stats = warmup_media_derivatives()
        if media_stats["wallpapers"] or media_stats["travel_photos"]:
            print(
                f"[atelier] media derivatives: "
                f"{media_stats['wallpapers']} wallpapers, "
                f"{media_stats['travel_photos']} travel photos",
                flush=True,
            )
        clear_context_cache()
        load_site_data()
        load_travel_trips()
        get_all_projects()
        load_wiki_assets()
        wallpapers = list_wallpapers()
        if wallpapers:
            default = next((w for w in wallpapers if w.get("default")), wallpapers[0])
            print(
                f"[atelier] wallpapers: {len(wallpapers)} static, default={default['id']!r}",
                flush=True,
            )
        else:
            print("[atelier] wallpapers: none", flush=True)
        print("[atelier] warmed caches", flush=True)
        yield
    finally:
        if sys.platform == "win32" and prev_handler is not None:
            asyncio.get_running_loop().set_exception_handler(prev_handler)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Personal Site",
        docs_url=None,
        redoc_url=None,
        lifespan=_lifespan,
    )
    register_security_middleware(app)
    app.include_router(assets.router)
    app.include_router(home.router)
    app.include_router(browse.router)
    app.include_router(projects.router)
    app.include_router(blog.router)
    app.include_router(travel.router)
    app.include_router(demo.router)
    app.include_router(wiki.router)
    static_dir = ATELIER_ROOT / "static"
    if mc_vtuber_live2d_ready():
        app.mount(
            "/static/MC_Vtuber",
            CachedStaticFiles(
                directory=MC_VTUBER_DIR,
                cache_headers=MC_VTUBER_CACHE_HEADERS,
            ),
            name="mc-vtuber-model",
        )
    app.mount("/static", CachedStaticFiles(directory=static_dir), name="static")
    return app


app = create_app()
