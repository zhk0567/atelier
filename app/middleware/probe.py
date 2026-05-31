"""Block common scanner / probe paths with a fast 404."""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_PROBE_PREFIXES = (
    "/.env",
    "/.git",
    "/.svn",
    "/.hg",
    "/.aws",
    "/.docker",
    "/wp-admin",
    "/wp-login",
    "/wp-content",
    "/wordpress",
    "/phpmyadmin",
    "/pma",
    "/mysql",
    "/administrator",
    "/admin.php",
    "/xmlrpc.php",
    "/actuator",
    "/server-status",
    "/cgi-bin",
    "/shell",
    "/vendor/phpunit",
    "/telescope",
    "/debug",
    "/_profiler",
    "/config.php",
    "/web.config",
)

_PROBE_EXACT = frozenset(
    {
        "/robots.txt",  # legitimate — do not block
    }
)


def _is_probe_path(path: str) -> bool:
    lower = path.lower()
    if lower in _PROBE_EXACT:
        return False
    for prefix in _PROBE_PREFIXES:
        if lower == prefix or lower.startswith(prefix + "/") or lower.startswith(prefix + "?"):
            return True
    if lower.endswith((".php", ".asp", ".aspx", ".jsp")):
        return True
    return False


class ProbeBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if _is_probe_path(request.url.path):
            return Response(status_code=404)
        return await call_next(request)
