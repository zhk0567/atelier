"""HTTP security response headers."""

from __future__ import annotations

import re

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# pyecharts chapter: chart HTML must be embeddable in same-origin blog iframes.
_BLOG_CHART_HTML = re.compile(
    r"^/static/blog/dataviz-ch09/[a-z0-9_.-]+\.html$",
    re.I,
)
def _is_blog_chart_embed(path: str) -> bool:
    return bool(_BLOG_CHART_HTML.match(path))


def _content_security_policy(*, frame_ancestors: str = "'none'") -> str:
    connect_src = "'self'"
    worker_src = "'self' blob:"
    return (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "media-src 'self' blob:; "
        "font-src 'self'; "
        f"connect-src {connect_src}; "
        f"worker-src {worker_src}; "
        "frame-src 'self'; "
        f"frame-ancestors {frame_ancestors}; "
        "base-uri 'self'; "
        "form-action 'self'"
    )


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        path = request.url.path
        embeddable_chart = _is_blog_chart_embed(path)

        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        if embeddable_chart:
            # Same-origin iframe/embed for blog charts.
            response.headers["X-Frame-Options"] = "SAMEORIGIN"
            response.headers["Content-Security-Policy"] = _content_security_policy(
                frame_ancestors="'self'"
            )
        else:
            response.headers.setdefault("X-Frame-Options", "DENY")
            response.headers.setdefault(
                "Content-Security-Policy",
                _content_security_policy(),
            )
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=(), payment=()",
        )
        response.headers.setdefault("X-Permitted-Cross-Domain-Policies", "none")
        return response
