"""Fixed administrator credential and signed-cookie session helpers."""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import time
from pathlib import Path
from threading import Lock

from fastapi import Request
from fastapi.responses import Response

from app.config import ATELIER_ROOT, is_production

ADMIN_PATH = "/ops/neurosis-7f3c9a2e"
ADMIN_USERNAME = "zhk"

# The requested fixed password is 209187. Only a salted PBKDF2 digest is kept
# in source, so the credential still works without storing the plaintext.
_PASSWORD_SALT = bytes.fromhex("c7913e8040ac7ccef324f5a1116b46ae")
_PASSWORD_DIGEST = bytes.fromhex(
    "090664f311a28a035b659665e4d544aaa22e39ee9cffca910615cbb0627b4060"
)
_PBKDF2_ITERATIONS = 240_000

SESSION_COOKIE = "atelier_admin_session"
CSRF_COOKIE = "atelier_admin_csrf"
SESSION_TTL_SECONDS = 8 * 60 * 60

_SECRET_LOCK = Lock()
_SECRET: bytes | None = None

_FAILED_LOCK = Lock()
_FAILED_ATTEMPTS: dict[str, list[float]] = {}
_FAILURE_WINDOW = 10 * 60
_MAX_FAILURES = 6


def _secret_path() -> Path:
    return ATELIER_ROOT / "instance" / ".admin_secret"


def _load_or_create_secret() -> bytes:
    global _SECRET
    if _SECRET is not None:
        return _SECRET
    with _SECRET_LOCK:
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


def verify_credentials(username: str, password: str) -> bool:
    candidate = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        _PASSWORD_SALT,
        _PBKDF2_ITERATIONS,
    )
    username_ok = hmac.compare_digest(username, ADMIN_USERNAME)
    password_ok = hmac.compare_digest(candidate, _PASSWORD_DIGEST)
    return username_ok and password_ok


def _sign(payload: str) -> str:
    return hmac.new(_load_or_create_secret(), payload.encode("utf-8"), hashlib.sha256).hexdigest()


def create_session_token() -> str:
    expires = int(time.time()) + SESSION_TTL_SECONDS
    payload = f"admin:{expires}"
    return f"{expires}.{_sign(payload)}"


def session_token_valid(token: str | None) -> bool:
    if not token or "." not in token:
        return False
    expires_raw, signature = token.split(".", 1)
    try:
        expires = int(expires_raw)
    except ValueError:
        return False
    if expires < int(time.time()):
        return False
    expected = _sign(f"admin:{expires}")
    return hmac.compare_digest(signature, expected)


def admin_session_ok(request: Request) -> bool:
    return session_token_valid(request.cookies.get(SESSION_COOKIE))


def set_admin_session(response: Response, request: Request) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        create_session_token(),
        max_age=SESSION_TTL_SECONDS,
        httponly=True,
        samesite="lax",
        secure=is_production(),
        path="/",
    )


def clear_admin_session(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE, path="/")


def admin_csrf_token() -> str:
    return _sign("admin-csrf")[:40]


def set_csrf_cookie(response: Response) -> None:
    response.set_cookie(
        CSRF_COOKIE,
        admin_csrf_token(),
        max_age=SESSION_TTL_SECONDS,
        httponly=True,
        samesite="lax",
        secure=is_production(),
        path="/",
    )


def csrf_valid(request: Request, submitted: str) -> bool:
    expected = request.cookies.get(CSRF_COOKIE, "")
    return bool(expected and submitted) and hmac.compare_digest(expected, submitted)


def client_ip(request: Request) -> str:
    if is_production():
        forwarded = request.headers.get("x-forwarded-for", "")
        if forwarded:
            return forwarded.split(",")[0].strip() or "unknown"
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def login_limited(ip: str) -> bool:
    now = time.monotonic()
    with _FAILED_LOCK:
        attempts = [stamp for stamp in _FAILED_ATTEMPTS.get(ip, []) if now - stamp < _FAILURE_WINDOW]
        _FAILED_ATTEMPTS[ip] = attempts
        return len(attempts) >= _MAX_FAILURES


def record_login_failure(ip: str) -> None:
    now = time.monotonic()
    with _FAILED_LOCK:
        attempts = [stamp for stamp in _FAILED_ATTEMPTS.get(ip, []) if now - stamp < _FAILURE_WINDOW]
        attempts.append(now)
        _FAILED_ATTEMPTS[ip] = attempts[-_MAX_FAILURES:]


def clear_login_failures(ip: str) -> None:
    with _FAILED_LOCK:
        _FAILED_ATTEMPTS.pop(ip, None)
