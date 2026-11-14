"""HTTP routes for Echo diary sync (dual client replicas)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.echo_sync.auth import require_bearer
from app.echo_sync import db as echo_db

router = APIRouter(prefix="/api/echo", tags=["echo-sync"])


class WatchlistPayload(BaseModel):
    names: list[str] = Field(default_factory=list)
    updatedAt: str | None = None


class ReplicaPayload(BaseModel):
    entries: list[dict[str, Any]] = Field(default_factory=list)
    articles: list[dict[str, Any]] = Field(default_factory=list)
    groups: list[dict[str, Any]] = Field(default_factory=list)
    watchlist: WatchlistPayload | None = None


class DiffPayload(BaseModel):
    """Local snapshot used only for server-side diff summary (not stored)."""
    entries: list[dict[str, Any]] = Field(default_factory=list)
    articles: list[dict[str, Any]] = Field(default_factory=list)
    groups: list[dict[str, Any]] = Field(default_factory=list)
    watchlist: WatchlistPayload | None = None


def _parse_client(client_id: str) -> str:
    try:
        return echo_db.normalize_client_id(client_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/health")
async def echo_health(_: str = Depends(require_bearer)) -> dict[str, Any]:
    echo_db.ensure_db()
    return {
        "ok": True,
        "service": "echo-sync",
        "mode": "dual-replica",
        "clients": sorted(echo_db.CLIENT_IDS),
        "serverTime": echo_db.utc_now_iso(),
    }


@router.get("/replica/{client_id}")
async def get_replica(
    client_id: str,
    _: str = Depends(require_bearer),
) -> dict[str, Any]:
    cid = _parse_client(client_id)
    return echo_db.get_replica(cid)


@router.put("/replica/{client_id}")
async def put_replica(
    client_id: str,
    payload: ReplicaPayload,
    _: str = Depends(require_bearer),
) -> dict[str, Any]:
    """Upload / replace this client's own replica on the server."""
    cid = _parse_client(client_id)
    data = payload.model_dump()
    try:
        return echo_db.replace_replica(cid, data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/peer/{client_id}")
async def get_peer_replica(
    client_id: str,
    _: str = Depends(require_bearer),
) -> dict[str, Any]:
    """Fetch the opposite client's replica (desktop <-> android)."""
    cid = _parse_client(client_id)
    peer = echo_db.peer_client_id(cid)
    replica = echo_db.get_replica(peer)
    replica["selfClientId"] = cid
    replica["peerClientId"] = peer
    return replica


@router.post("/diff/{client_id}")
async def diff_against_peer(
    client_id: str,
    payload: DiffPayload,
    _: str = Depends(require_bearer),
) -> dict[str, Any]:
    """
    Compare caller's local snapshot to the peer replica on the server.
    Does not write anything — clients decide whether to apply.
    """
    cid = _parse_client(client_id)
    peer = echo_db.peer_client_id(cid)
    peer_replica = echo_db.get_replica(peer)
    local = payload.model_dump()
    if local.get("watchlist") is None:
        local["watchlist"] = {"names": []}
    diff = echo_db.summarize_diff(local, peer_replica)
    return {
        "selfClientId": cid,
        "peerClientId": peer,
        "serverTime": echo_db.utc_now_iso(),
        "peer": peer_replica,
        "diff": diff,
    }


# ---- Back-compat shims (deprecated single-copy endpoints) ----

@router.get("/changes")
async def echo_changes_deprecated(
    since: str | None = Query(default=None),
    _: str = Depends(require_bearer),
) -> dict[str, Any]:
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="Deprecated. Use GET /api/echo/peer/{clientId} and POST /api/echo/diff/{clientId}",
    )


@router.get("/snapshot")
async def echo_snapshot_deprecated(
    _: str = Depends(require_bearer),
) -> dict[str, Any]:
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="Deprecated. Use GET /api/echo/replica/{clientId}",
    )


@router.post("/push")
async def echo_push_deprecated(
    _: str = Depends(require_bearer),
) -> dict[str, Any]:
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="Deprecated. Use PUT /api/echo/replica/{clientId}",
    )
