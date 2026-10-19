"""Signed, short-lived access grants for private quiz result pages."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import os
import secrets
import time
from pathlib import Path
from threading import Lock

from fastapi import Request
from fastapi.responses import Response

from app.config import ATELIER_ROOT, is_production

COOKIE_NAME = "atelier_quiz_access"
ACCESS_TTL_SECONDS = 6 * 60 * 60
MAX_GRANTS = 60

_LOCK = Lock()
_SECRET: bytes | None = None


def _secret_path() -> Path:
    return ATELIER_ROOT / "instance" / ".quiz_access_secret"


def _load_or_create_secret() -> bytes:
    global _SECRET
    if _SECRET is not None:
        return _SECRET
    with _LOCK:
        if _SECRET is not None:
            return _SECRET
        path = _secret_path()
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if not path.is_file():
            try:
                fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(fd, "wb") as handle:
                    handle.write(secrets.token_bytes(32))
            except FileExistsError:
                pass
        data = path.read_bytes()
        if len(data) < 32:
            data = secrets.token_bytes(32)
            path.write_bytes(data)
            try:
                path.chmod(0o600)
            except OSError:
                pass
        _SECRET = data
        return data


def _sign(body: str) -> str:
    return hmac.new(
        _load_or_create_secret(),
        body.encode("ascii"),
        hashlib.sha256,
    ).hexdigest()


def _encode(tokens: list[str], expires: int) -> str:
    payload = json.dumps(
        {"tokens": tokens[-MAX_GRANTS:], "exp": expires},
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")
    body = base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")
    return f"{body}.{_sign(body)}"


def _decode(value: str) -> list[str]:
    if not value or "." not in value:
        return []
    body, signature = value.split(".", 1)
    if not hmac.compare_digest(signature, _sign(body)):
        return []
    try:
        padded = body + "=" * (-len(body) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
        expires = int(payload.get("exp", 0))
        tokens = payload.get("tokens", [])
    except (TypeError, ValueError, binascii.Error, json.JSONDecodeError):
        return []
    if expires < int(time.time()) or not isinstance(tokens, list):
        return []
    return [token for token in tokens if isinstance(token, str) and token]


def granted_tokens(request: Request) -> list[str]:
    return _decode(request.cookies.get(COOKIE_NAME, ""))


def has_result_access(request: Request, token: str) -> bool:
    return token in granted_tokens(request)


def grant_result_access(
    response: Response,
    request: Request,
    tokens: list[str],
) -> None:
    merged: list[str] = []
    for token in [*granted_tokens(request), *tokens]:
        if token and token not in merged:
            merged.append(token)
    if not merged:
        return
    expires = int(time.time()) + ACCESS_TTL_SECONDS
    response.set_cookie(
        COOKIE_NAME,
        _encode(merged, expires),
        max_age=ACCESS_TTL_SECONDS,
        httponly=True,
        samesite="lax",
        secure=is_production(),
        path="/quiz/neurosis",
    )
