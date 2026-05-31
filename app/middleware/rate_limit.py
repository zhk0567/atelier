"""In-memory per-IP rate limiting (single-instance ECS)."""

from __future__ import annotations

import math
import time
from collections import defaultdict
from threading import Lock

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import (
    is_production,
    parse_rate_limit,
    rate_limit_default,
    rate_limit_wallpaper,
)

_BUCKETS: dict[str, tuple[float, float]] = {}
_LOCK = Lock()
_LAST_GC = 0.0
_GC_INTERVAL = 300.0


def _client_ip(request: Request) -> str:
    if is_production():
        forwarded = request.headers.get("x-forwarded-for", "")
        if forwarded:
            return forwarded.split(",")[0].strip() or "unknown"
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def _bucket_key(ip: str, scope: str) -> str:
    return f"{ip}:{scope}"


def _gc_buckets(now: float) -> None:
    global _LAST_GC
    if now - _LAST_GC < _GC_INTERVAL:
        return
    _LAST_GC = now
    stale = [k for k, (_, reset) in _BUCKETS.items() if reset <= now]
    for k in stale:
        _BUCKETS.pop(k, None)


def _take_token(key: str, limit: int, window: float) -> tuple[bool, float]:
    now = time.monotonic()
    with _LOCK:
        _gc_buckets(now)
        remaining, reset_at = _BUCKETS.get(key, (float(limit), now + window))
        if now >= reset_at:
            remaining, reset_at = float(limit), now + window
        if remaining < 1:
            retry_after = max(1, math.ceil(reset_at - now))
            _BUCKETS[key] = (remaining, reset_at)
            return False, retry_after
        remaining -= 1
        _BUCKETS[key] = (remaining, reset_at)
        return True, max(0, math.ceil(reset_at - now))


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if not is_production():
            return await call_next(request)

        path = request.url.path
        if path.startswith("/wallpaper/"):
            limit, window = parse_rate_limit(rate_limit_wallpaper())
            scope = "wallpaper"
        else:
            limit, window = parse_rate_limit(rate_limit_default())
            scope = "default"

        ip = _client_ip(request)
        ok, retry_after = _take_token(_bucket_key(ip, scope), limit, window)
        if not ok:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
                headers={"Retry-After": str(retry_after)},
            )

        response = await call_next(request)
        response.headers.setdefault("X-RateLimit-Scope", scope)
        return response
