"""Bearer token auth for Echo sync API."""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from pathlib import Path
from threading import Lock

from fastapi import Header, HTTPException, status

from app.config import ATELIER_ROOT

_PBKDF2_ITERATIONS = 240_000
_LOCK = Lock()
_SALT: bytes | None = None
_DIGEST: bytes | None = None


def _secret_dir() -> Path:
    path = ATELIER_ROOT / "instance"
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    return path


def _salt_path() -> Path:
    return _secret_dir() / ".echo_sync_salt"


def _digest_path() -> Path:
    return _secret_dir() / ".echo_sync_digest"


def _load_salt() -> bytes:
    global _SALT
    if _SALT is not None:
        return _SALT
    with _LOCK:
        if _SALT is not None:
            return _SALT
        path = _salt_path()
        if not path.is_file():
            data = secrets.token_bytes(16)
            path.write_bytes(data)
            try:
                path.chmod(0o600)
            except OSError:
                pass
        else:
            data = path.read_bytes()
            if len(data) < 16:
                data = secrets.token_bytes(16)
                path.write_bytes(data)
        _SALT = data
        return data


def _load_digest() -> bytes | None:
    global _DIGEST
    if _DIGEST is not None:
        return _DIGEST
    with _LOCK:
        if _DIGEST is not None:
            return _DIGEST
        path = _digest_path()
        if not path.is_file():
            return None
        _DIGEST = path.read_bytes()
        return _DIGEST


def hash_token(token: str, salt: bytes | None = None) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        token.encode("utf-8"),
        salt or _load_salt(),
        _PBKDF2_ITERATIONS,
    )


def ensure_token_configured() -> bool:
    return _load_digest() is not None


def set_token(plaintext: str) -> None:
    """Store PBKDF2 digest of the sync token (never store plaintext)."""
    global _DIGEST
    token = plaintext.strip()
    if len(token) < 24:
        raise ValueError("token too short (min 24 chars)")
    digest = hash_token(token)
    path = _digest_path()
    path.write_bytes(digest)
    try:
        path.chmod(0o600)
    except OSError:
        pass
    _DIGEST = digest


def verify_token(token: str | None) -> bool:
    if not token:
        return False
    digest = _load_digest()
    if digest is None:
        return False
    candidate = hash_token(token.strip())
    return hmac.compare_digest(candidate, digest)


def require_bearer(authorization: str | None = Header(default=None)) -> str:
    if not ensure_token_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Echo sync token not configured on server",
        )
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization[7:].strip()
    if not verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


def generate_token() -> str:
    return secrets.token_urlsafe(32)
