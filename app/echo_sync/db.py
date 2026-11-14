"""SQLite storage for Echo diary sync — dual client replicas (desktop / android)."""

from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from app.config import ATELIER_ROOT

DB_PATH = Path(
    os.environ.get(
        "ATELIER_ECHO_DB",
        str(ATELIER_ROOT / "instance" / "echo_diary.sqlite3"),
    )
)

CLIENT_IDS = frozenset({"desktop", "android"})

_LOCK = Lock()
_READY = False

_SCHEMA = """
CREATE TABLE IF NOT EXISTS echo_entries (
    client_id TEXT NOT NULL,
    date TEXT NOT NULL,
    content TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    deleted_at TEXT,
    PRIMARY KEY (client_id, date)
);
CREATE INDEX IF NOT EXISTS idx_echo_entries_client_updated
    ON echo_entries(client_id, updated_at);

CREATE TABLE IF NOT EXISTS echo_articles (
    client_id TEXT NOT NULL,
    id TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    content TEXT NOT NULL DEFAULT '',
    group_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    deleted_at TEXT,
    PRIMARY KEY (client_id, id)
);
CREATE INDEX IF NOT EXISTS idx_echo_articles_client_updated
    ON echo_articles(client_id, updated_at);

CREATE TABLE IF NOT EXISTS echo_groups (
    client_id TEXT NOT NULL,
    id TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL,
    deleted_at TEXT,
    PRIMARY KEY (client_id, id)
);
CREATE INDEX IF NOT EXISTS idx_echo_groups_client_updated
    ON echo_groups(client_id, updated_at);

CREATE TABLE IF NOT EXISTS echo_meta (
    client_id TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (client_id, key)
);
"""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def normalize_client_id(raw: str | None) -> str:
    client = (raw or "").strip().lower()
    if client not in CLIENT_IDS:
        raise ValueError("clientId must be 'desktop' or 'android'")
    return client


def peer_client_id(client_id: str) -> str:
    cid = normalize_client_id(client_id)
    return "android" if cid == "desktop" else "desktop"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout=5000")
    connection.execute("PRAGMA journal_mode=WAL")
    return connection


@contextmanager
def _db():
    connection = _connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _migrate_legacy(connection: sqlite3.Connection) -> None:
    """If old single-copy tables exist without client_id, move rows into desktop."""
    cols = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(echo_entries)").fetchall()
    }
    if not cols:
        return
    if "client_id" in cols:
        return
    # Recreate with dual-copy schema: dump old → insert as desktop.
    entries = connection.execute("SELECT * FROM echo_entries").fetchall()
    articles = connection.execute("SELECT * FROM echo_articles").fetchall()
    groups = connection.execute("SELECT * FROM echo_groups").fetchall()
    meta = connection.execute("SELECT * FROM echo_meta").fetchall()
    connection.executescript(
        """
        DROP TABLE IF EXISTS echo_entries;
        DROP TABLE IF EXISTS echo_articles;
        DROP TABLE IF EXISTS echo_groups;
        DROP TABLE IF EXISTS echo_meta;
        """
    )
    connection.executescript(_SCHEMA)
    for row in entries:
        connection.execute(
            """
            INSERT INTO echo_entries(client_id, date, content, created_at, updated_at, deleted_at)
            VALUES ('desktop', ?, ?, ?, ?, ?)
            """,
            (
                row["date"],
                row["content"] or "",
                row["created_at"],
                row["updated_at"],
                row["deleted_at"],
            ),
        )
    for row in articles:
        connection.execute(
            """
            INSERT INTO echo_articles(
                client_id, id, title, content, group_id, created_at, updated_at, deleted_at
            ) VALUES ('desktop', ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["title"] or "",
                row["content"] or "",
                row["group_id"],
                row["created_at"],
                row["updated_at"],
                row["deleted_at"],
            ),
        )
    for row in groups:
        connection.execute(
            """
            INSERT INTO echo_groups(client_id, id, name, sort_order, updated_at, deleted_at)
            VALUES ('desktop', ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["name"] or "",
                row["sort_order"],
                row["updated_at"],
                row["deleted_at"],
            ),
        )
    for row in meta:
        connection.execute(
            """
            INSERT INTO echo_meta(client_id, key, value, updated_at)
            VALUES ('desktop', ?, ?, ?)
            """,
            (row["key"], row["value"], row["updated_at"]),
        )


def ensure_db() -> None:
    global _READY
    if _READY:
        return
    with _LOCK:
        if _READY:
            return
        with _db() as connection:
            connection.executescript(_SCHEMA)
            _migrate_legacy(connection)
            connection.executescript(_SCHEMA)
        _READY = True


def _row_entry(row: sqlite3.Row) -> dict[str, Any]:
    deleted_at = row["deleted_at"]
    return {
        "date": row["date"],
        "content": row["content"] or "",
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
        "deleted": bool(deleted_at),
        "deletedAt": deleted_at,
    }


def _row_article(row: sqlite3.Row) -> dict[str, Any]:
    deleted_at = row["deleted_at"]
    return {
        "id": row["id"],
        "title": row["title"] or "",
        "content": row["content"] or "",
        "groupId": row["group_id"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
        "deleted": bool(deleted_at),
        "deletedAt": deleted_at,
    }


def _row_group(row: sqlite3.Row) -> dict[str, Any]:
    deleted_at = row["deleted_at"]
    return {
        "id": row["id"],
        "name": row["name"] or "",
        "order": row["sort_order"],
        "updatedAt": row["updated_at"],
        "deleted": bool(deleted_at),
        "deletedAt": deleted_at,
    }


def _count_chars(content: str) -> int:
    return len(content.replace("\r\n", "\n").replace("\r", "\n").replace("\n", ""))


def get_watchlist(client_id: str) -> dict[str, Any]:
    ensure_db()
    cid = normalize_client_id(client_id)
    with _db() as connection:
        row = connection.execute(
            "SELECT value, updated_at FROM echo_meta WHERE client_id = ? AND key = 'watchlist'",
            (cid,),
        ).fetchone()
    if not row:
        return {"names": [], "updatedAt": None}
    try:
        data = json.loads(row["value"])
        names = data.get("names", []) if isinstance(data, dict) else []
    except json.JSONDecodeError:
        names = []
    return {"names": names, "updatedAt": row["updated_at"]}


def get_replica(client_id: str) -> dict[str, Any]:
    ensure_db()
    cid = normalize_client_id(client_id)
    with _db() as connection:
        entries = [
            _row_entry(row)
            for row in connection.execute(
                "SELECT * FROM echo_entries WHERE client_id = ? ORDER BY date ASC",
                (cid,),
            )
        ]
        articles = [
            _row_article(row)
            for row in connection.execute(
                "SELECT * FROM echo_articles WHERE client_id = ? ORDER BY updated_at DESC",
                (cid,),
            )
        ]
        groups = [
            _row_group(row)
            for row in connection.execute(
                "SELECT * FROM echo_groups WHERE client_id = ? ORDER BY sort_order ASC",
                (cid,),
            )
        ]
    return {
        "clientId": cid,
        "serverTime": utc_now_iso(),
        "entries": entries,
        "articles": articles,
        "groups": groups,
        "watchlist": get_watchlist(cid),
    }


def replace_replica(client_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Replace one client's full replica with the uploaded snapshot."""
    ensure_db()
    cid = normalize_client_id(client_id)
    entries = payload.get("entries") or []
    articles = payload.get("articles") or []
    groups = payload.get("groups") or []
    if len(entries) > 5000 or len(articles) > 2000 or len(groups) > 500:
        raise ValueError("replica too large")

    now = utc_now_iso()
    with _db() as connection:
        connection.execute("DELETE FROM echo_entries WHERE client_id = ?", (cid,))
        connection.execute("DELETE FROM echo_articles WHERE client_id = ?", (cid,))
        connection.execute("DELETE FROM echo_groups WHERE client_id = ?", (cid,))
        connection.execute("DELETE FROM echo_meta WHERE client_id = ?", (cid,))

        for item in entries:
            if not isinstance(item, dict):
                continue
            date = str(item.get("date", "")).strip()
            if not date:
                continue
            updated_at = str(item.get("updatedAt") or item.get("updated_at") or now)
            created_at = str(item.get("createdAt") or item.get("created_at") or updated_at)
            deleted = bool(item.get("deleted"))
            deleted_at = item.get("deletedAt") or item.get("deleted_at")
            if deleted and not deleted_at:
                deleted_at = updated_at
            if not deleted:
                deleted_at = None
            content = "" if deleted else str(item.get("content") or "")
            connection.execute(
                """
                INSERT INTO echo_entries(client_id, date, content, created_at, updated_at, deleted_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (cid, date, content, created_at, updated_at, deleted_at),
            )

        for item in articles:
            if not isinstance(item, dict):
                continue
            article_id = str(item.get("id", "")).strip()
            if not article_id:
                continue
            updated_at = str(item.get("updatedAt") or item.get("updated_at") or now)
            created_at = str(item.get("createdAt") or item.get("created_at") or updated_at)
            deleted = bool(item.get("deleted"))
            deleted_at = item.get("deletedAt") or item.get("deleted_at")
            if deleted and not deleted_at:
                deleted_at = updated_at
            if not deleted:
                deleted_at = None
            title = "" if deleted else str(item.get("title") or "")
            content = "" if deleted else str(item.get("content") or "")
            group_id = None if deleted else item.get("groupId", item.get("group_id"))
            connection.execute(
                """
                INSERT INTO echo_articles(
                    client_id, id, title, content, group_id, created_at, updated_at, deleted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (cid, article_id, title, content, group_id, created_at, updated_at, deleted_at),
            )

        for item in groups:
            if not isinstance(item, dict):
                continue
            group_id = str(item.get("id", "")).strip()
            if not group_id:
                continue
            updated_at = str(item.get("updatedAt") or item.get("updated_at") or now)
            deleted = bool(item.get("deleted"))
            deleted_at = item.get("deletedAt") or item.get("deleted_at")
            if deleted and not deleted_at:
                deleted_at = updated_at
            if not deleted:
                deleted_at = None
            name = "" if deleted else str(item.get("name") or "")
            sort_order = int(item.get("order", item.get("sort_order", 0)) or 0)
            connection.execute(
                """
                INSERT INTO echo_groups(client_id, id, name, sort_order, updated_at, deleted_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (cid, group_id, name, sort_order, updated_at, deleted_at),
            )

        watch = payload.get("watchlist")
        if isinstance(watch, dict) and "names" in watch:
            names_raw = watch.get("names") or []
            cleaned: list[str] = []
            seen: set[str] = set()
            if isinstance(names_raw, list):
                for raw in names_raw:
                    name = str(raw).strip()
                    if not name or name in seen or len(name) > 8:
                        continue
                    seen.add(name)
                    cleaned.append(name)
            stamp = str(watch.get("updatedAt") or watch.get("updated_at") or now)
            connection.execute(
                """
                INSERT INTO echo_meta(client_id, key, value, updated_at)
                VALUES (?, 'watchlist', ?, ?)
                """,
                (cid, json.dumps({"names": cleaned}, ensure_ascii=False), stamp),
            )

    return {
        "ok": True,
        "clientId": cid,
        "serverTime": utc_now_iso(),
        "counts": {
            "entries": len(entries),
            "articles": len(articles),
            "groups": len(groups),
        },
    }


def summarize_diff(local: dict[str, Any], peer: dict[str, Any]) -> dict[str, Any]:
    """Compare local snapshot vs peer replica; return human-readable change list."""
    local_entries = {
        str(e.get("date")): e
        for e in (local.get("entries") or [])
        if isinstance(e, dict) and e.get("date")
    }
    peer_entries = {
        str(e.get("date")): e
        for e in (peer.get("entries") or [])
        if isinstance(e, dict) and e.get("date")
    }
    entry_changes: list[dict[str, Any]] = []
    for date, peer_e in sorted(peer_entries.items()):
        local_e = local_entries.get(date)
        peer_deleted = bool(peer_e.get("deleted"))
        peer_chars = _count_chars(str(peer_e.get("content") or ""))
        if local_e is None:
            if peer_deleted:
                continue
            entry_changes.append(
                {
                    "kind": "added",
                    "date": date,
                    "peerChars": peer_chars,
                    "summary": f"新增日记 {date}（{peer_chars} 字）",
                }
            )
            continue
        local_deleted = bool(local_e.get("deleted"))
        local_chars = _count_chars(str(local_e.get("content") or ""))
        local_updated = str(local_e.get("updatedAt") or "")
        peer_updated = str(peer_e.get("updatedAt") or "")
        if peer_deleted and not local_deleted:
            entry_changes.append(
                {
                    "kind": "deleted",
                    "date": date,
                    "localChars": local_chars,
                    "summary": f"对端删除日记 {date}（本地仍有 {local_chars} 字）",
                }
            )
        elif not peer_deleted and (
            local_deleted
            or peer_updated > local_updated
            or str(peer_e.get("content") or "") != str(local_e.get("content") or "")
        ):
            if local_deleted:
                kind = "added"
                summary = f"对端有日记 {date}（{peer_chars} 字），本地已删"
            else:
                kind = "modified"
                summary = f"修改日记 {date}：{local_chars} → {peer_chars} 字"
            entry_changes.append(
                {
                    "kind": kind,
                    "date": date,
                    "localChars": local_chars,
                    "peerChars": peer_chars,
                    "summary": summary,
                }
            )

    local_articles = {
        str(a.get("id")): a
        for a in (local.get("articles") or [])
        if isinstance(a, dict) and a.get("id")
    }
    peer_articles = {
        str(a.get("id")): a
        for a in (peer.get("articles") or [])
        if isinstance(a, dict) and a.get("id")
    }
    article_changes: list[dict[str, Any]] = []
    for aid, peer_a in sorted(peer_articles.items(), key=lambda x: str(x[1].get("title") or x[0])):
        local_a = local_articles.get(aid)
        peer_deleted = bool(peer_a.get("deleted"))
        title = str(peer_a.get("title") or "无标题")
        if local_a is None:
            if peer_deleted:
                continue
            article_changes.append(
                {
                    "kind": "added",
                    "id": aid,
                    "title": title,
                    "summary": f"新增文章《{title}》",
                }
            )
            continue
        local_deleted = bool(local_a.get("deleted"))
        local_title = str(local_a.get("title") or "无标题")
        local_updated = str(local_a.get("updatedAt") or "")
        peer_updated = str(peer_a.get("updatedAt") or "")
        if peer_deleted and not local_deleted:
            article_changes.append(
                {
                    "kind": "deleted",
                    "id": aid,
                    "title": local_title,
                    "summary": f"对端删除文章《{local_title}》",
                }
            )
        elif not peer_deleted and (
            local_deleted
            or peer_updated > local_updated
            or str(peer_a.get("content") or "") != str(local_a.get("content") or "")
            or title != local_title
        ):
            article_changes.append(
                {
                    "kind": "modified",
                    "id": aid,
                    "title": title,
                    "summary": f"修改文章《{local_title}》→《{title}》",
                }
            )

    local_watch = set((local.get("watchlist") or {}).get("names") or [])
    peer_watch = set((peer.get("watchlist") or {}).get("names") or [])
    watch_added = sorted(peer_watch - local_watch)
    watch_removed = sorted(local_watch - peer_watch)
    watchlist_summary = None
    if watch_added or watch_removed:
        parts = []
        if watch_added:
            parts.append("新增 " + "、".join(watch_added))
        if watch_removed:
            parts.append("移除 " + "、".join(watch_removed))
        watchlist_summary = "人名关注：" + "；".join(parts)

    lines: list[str] = []
    lines.extend(c["summary"] for c in entry_changes[:80])
    lines.extend(c["summary"] for c in article_changes[:40])
    if watchlist_summary:
        lines.append(watchlist_summary)
    if len(entry_changes) > 80:
        lines.append(f"…另有 {len(entry_changes) - 80} 条日记变更未展开")
    if len(article_changes) > 40:
        lines.append(f"…另有 {len(article_changes) - 40} 条文章变更未展开")

    return {
        "hasChanges": bool(entry_changes or article_changes or watchlist_summary),
        "entryChanges": entry_changes,
        "articleChanges": article_changes,
        "watchlist": {
            "added": watch_added,
            "removed": watch_removed,
            "summary": watchlist_summary,
        },
        "lines": lines,
        "counts": {
            "entries": len(entry_changes),
            "articles": len(article_changes),
            "watchlistTouched": bool(watchlist_summary),
        },
    }
