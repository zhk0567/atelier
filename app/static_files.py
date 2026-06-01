"""Static files with long-lived cache headers."""

from __future__ import annotations

from pathlib import Path

from starlette.responses import Response
from starlette.staticfiles import StaticFiles

from app.constants import STATIC_CACHE_HEADERS


class CachedStaticFiles(StaticFiles):
    def __init__(
        self,
        *args,
        cache_headers: dict[str, str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._cache_headers = cache_headers or STATIC_CACHE_HEADERS

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
                response.headers.update(self._cache_headers)
        return response
