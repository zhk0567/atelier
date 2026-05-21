"""Static files with long-lived cache headers."""

from __future__ import annotations

from pathlib import Path

from starlette.responses import Response
from starlette.staticfiles import StaticFiles

from app.constants import STATIC_CACHE_HEADERS


class CachedStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):  # type: ignore[override]
        response: Response = await super().get_response(path, scope)
        if response.status_code == 200:
            suffix = Path(path).suffix.lower()
            if suffix in {
                ".css",
                ".js",
                ".png",
                ".jpg",
                ".jpeg",
                ".gif",
                ".webp",
                ".svg",
                ".ico",
                ".woff",
                ".woff2",
            }:
                response.headers.update(STATIC_CACHE_HEADERS)
        return response
