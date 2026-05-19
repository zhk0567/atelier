"""FastAPI application factory."""

from __future__ import annotations

import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import ATELIER_ROOT
from app.constants import SITE_NAME, SITE_TITLE
from app.routes import assets, blog, browse, home, projects, wiki


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
    app.include_router(assets.router)
    app.include_router(home.router)
    app.include_router(browse.router)
    app.include_router(projects.router)
    app.include_router(blog.router)
    app.include_router(wiki.router)
    static_dir = ATELIER_ROOT / "static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    return app


app = create_app()
