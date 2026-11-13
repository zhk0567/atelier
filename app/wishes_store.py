"""SQLite storage for visitor wishes / requirements on /personal.

A wish is submitted from the public page, reviewed in the admin console, and —
once approved — rendered on /personal.  The database lives under instance/ so it
never enters the repository.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any

from app.config import ATELIER_ROOT

DB_PATH = Path(
    os.environ.get(
        "ATELIER_WISHES_DB",
        str(ATELIER_ROOT / "instance" / "personal_wishes.sqlite3"),
    )
)

_LOCK = Lock()
_READY = False

STATUSES = {"pending", "approved", "rejected"}

_SCHEMA = """
CREATE TABLE IF NOT EXISTS personal_wishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT '',
    name TEXT NOT NULL DEFAULT '',
    wish TEXT NOT NULL,
    note TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    published_at TEXT NOT NULL DEFAULT '',
    source TEXT NOT NULL DEFAULT '',
    user_agent TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_personal_wishes_status
    ON personal_wishes(status, id DESC);
CREATE INDEX IF NOT EXISTS idx_personal_wishes_created
    ON personal_wishes(created_at DESC, id DESC);
"""


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=5)
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


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def ensure_db() -> None:
    global _READY
    if _READY:
        return
    with _LOCK:
        if _READY:
            return
        with _db() as connection:
            connection.executescript(_SCHEMA)
        _READY = True


def save_wish(
    *,
    name: str,
    wish: str,
    source: str = "",
    user_agent: str = "",
) -> int:
    ensure_db()
    now = _now()
    with _db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO personal_wishes (
                created_at, updated_at, name, wish, source, user_agent
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                now,
                now,
                name.strip()[:20],
                wish.strip()[:280],
                source.strip()[:300],
                user_agent[:300],
            ),
        )
        return int(cursor.lastrowid)


def approved_wishes(limit: int = 100) -> list[dict[str, Any]]:
    """Published wishes, newest first; never raises into the public page."""
    try:
        ensure_db()
        limit = max(1, min(int(limit), 200))
        with _db() as connection:
            rows = connection.execute(
                """
                SELECT * FROM personal_wishes
                WHERE status = 'approved'
                ORDER BY
                    CASE WHEN published_at = '' THEN created_at ELSE published_at END DESC,
                    id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]
    except Exception as exc:  # a broken DB must not take the page down
        print(f"[atelier] approved_wishes failed: {exc}", flush=True)
        return []


def list_wishes(
    *,
    query: str = "",
    status: str = "",
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[dict[str, Any]], int]:
    ensure_db()
    limit = max(1, min(int(limit), 200))
    offset = max(0, int(offset))
    conditions: list[str] = []
    params: list[Any] = []
    if query.strip():
        needle = f"%{query.strip()[:80]}%"
        conditions.append("(name LIKE ? OR wish LIKE ? OR note LIKE ?)")
        params.extend([needle, needle, needle])
    if status in STATUSES:
        conditions.append("status = ?")
        params.append(status)
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    with _db() as connection:
        total = int(
            connection.execute(
                f"SELECT COUNT(*) FROM personal_wishes {where}",
                params,
            ).fetchone()[0]
        )
        rows = connection.execute(
            f"""
            SELECT * FROM personal_wishes
            {where}
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            [*params, limit, offset],
        ).fetchall()
    return [dict(row) for row in rows], total


def get_wish(wish_id: int) -> dict[str, Any] | None:
    ensure_db()
    with _db() as connection:
        row = connection.execute(
            "SELECT * FROM personal_wishes WHERE id = ?",
            (int(wish_id),),
        ).fetchone()
    return dict(row) if row else None


def update_wish(
    wish_id: int,
    *,
    name: str,
    wish: str,
    note: str,
    status: str,
) -> bool:
    if status not in STATUSES:
        return False
    ensure_db()
    now = _now()
    with _db() as connection:
        row = connection.execute(
            "SELECT published_at FROM personal_wishes WHERE id = ?",
            (int(wish_id),),
        ).fetchone()
        if row is None:
            return False
        published_at = row["published_at"] or ""
        if status == "approved" and not published_at:
            published_at = now
        cursor = connection.execute(
            """
            UPDATE personal_wishes
            SET name = ?, wish = ?, note = ?, status = ?, published_at = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                name.strip()[:20],
                wish.strip()[:280],
                note.strip()[:300],
                status,
                published_at,
                now,
                int(wish_id),
            ),
        )
        return cursor.rowcount > 0


def set_wish_status(wish_id: int, status: str) -> bool:
    if status not in STATUSES:
        return False
    ensure_db()
    now = _now()
    with _db() as connection:
        row = connection.execute(
            "SELECT published_at FROM personal_wishes WHERE id = ?",
            (int(wish_id),),
        ).fetchone()
        if row is None:
            return False
        published_at = row["published_at"] or ""
        if status == "approved" and not published_at:
            published_at = now
        cursor = connection.execute(
            "UPDATE personal_wishes SET status = ?, published_at = ?, updated_at = ? WHERE id = ?",
            (status, published_at, now, int(wish_id)),
        )
        return cursor.rowcount > 0


def delete_wish(wish_id: int) -> bool:
    ensure_db()
    with _db() as connection:
        cursor = connection.execute(
            "DELETE FROM personal_wishes WHERE id = ?",
            (int(wish_id),),
        )
        return cursor.rowcount > 0


def wish_stats() -> dict[str, int]:
    try:
        ensure_db()
        today = datetime.now().astimezone().date().isoformat()
        with _db() as connection:
            row = connection.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    COALESCE(SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END), 0) AS pending,
                    COALESCE(SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END), 0) AS approved,
                    COALESCE(SUM(CASE WHEN created_at LIKE ? THEN 1 ELSE 0 END), 0) AS today
                FROM personal_wishes
                """,
                (f"{today}%",),
            ).fetchone()
        return {
            "total": int(row["total"]),
            "pending": int(row["pending"]),
            "approved": int(row["approved"]),
            "today": int(row["today"]),
        }
    except Exception as exc:
        print(f"[atelier] wish_stats failed: {exc}", flush=True)
        return {"total": 0, "pending": 0, "approved": 0, "today": 0}
