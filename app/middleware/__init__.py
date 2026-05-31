"""Security middleware registration."""

from __future__ import annotations

from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.config import block_probe_paths, is_production, trusted_hosts
from app.middleware.probe import ProbeBlockMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware


def register_security_middleware(app: FastAPI) -> None:
    """Register middleware (outermost first on request): TrustedHost → Probe → RateLimit → Headers."""
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitMiddleware)
    if block_probe_paths():
        app.add_middleware(ProbeBlockMiddleware)
    if is_production():
        hosts = trusted_hosts()
        if hosts:
            app.add_middleware(TrustedHostMiddleware, allowed_hosts=hosts)
