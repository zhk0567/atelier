"""Private SQLite storage for quiz attempts."""

from __future__ import annotations

import json
import os
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any

from app.config import ATELIER_ROOT

DB_PATH = Path(
    os.environ.get(
        "ATELIER_QUIZ_DB",
        str(ATELIER_ROOT / "instance" / "neurosis.sqlite3"),
    )
)

_LOCK = Lock()
_READY = False

_SCHEMA = """
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    name TEXT NOT NULL,
    identifier TEXT NOT NULL DEFAULT '',
    score INTEGER NOT NULL,
    max_score INTEGER NOT NULL,
    band_title TEXT NOT NULL,
    band_range TEXT NOT NULL,
    top_dimensions_json TEXT NOT NULL,
    attention_choice TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL DEFAULT 0,
    answers_json TEXT NOT NULL,
    group_scores_json TEXT NOT NULL,
    user_agent TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_created
    ON quiz_attempts(created_at DESC, id DESC);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_name
    ON quiz_attempts(name);
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


def ensure_db() -> None:
    global _READY
    if _READY:
        return
    with _LOCK:
        if _READY:
            return
        with _db() as connection:
            connection.executescript(_SCHEMA)
        try:
            DB_PATH.parent.chmod(0o700)
            DB_PATH.chmod(0o600)
        except OSError:
            pass
        _READY = True


def _new_token() -> str:
    return secrets.token_urlsafe(14)


def save_attempt(
    *,
    name: str,
    identifier: str,
    answers: dict[str, str],
    result: dict[str, Any],
    duration_seconds: int,
    user_agent: str,
) -> str:
    ensure_db()
    band = result["band"]
    created_at = datetime.now().astimezone().isoformat(timespec="seconds")
    for _ in range(5):
        token = _new_token()
        try:
            with _db() as connection:
                connection.execute(
                    """
                    INSERT INTO quiz_attempts (
                        token, created_at, name, identifier, score, max_score,
                        band_title, band_range, top_dimensions_json,
                        attention_choice, duration_seconds, answers_json,
                        group_scores_json, user_agent
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        token,
                        created_at,
                        name,
                        identifier,
                        int(result["total"]),
                        int(result["max_score"]),
                        str(band["title"]),
                        str(result["band_range"]),
                        json.dumps(result["top_dimensions"], ensure_ascii=False),
                        str(result["attention_choice"]),
                        max(0, min(int(duration_seconds), 86400)),
                        json.dumps(answers, ensure_ascii=False, sort_keys=True),
                        json.dumps(result["group_scores"], ensure_ascii=False, sort_keys=True),
                        user_agent[:300],
                    ),
                )
            return token
        except sqlite3.IntegrityError:
            continue
    raise RuntimeError("Could not allocate a unique result token")


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    for key, target in (
        ("answers_json", "answers"),
        ("group_scores_json", "group_scores"),
        ("top_dimensions_json", "top_dimensions"),
    ):
        raw = item.pop(key, "{}")
        try:
            item[target] = json.loads(raw)
        except (TypeError, ValueError):
            item[target] = {} if target != "top_dimensions" else []
    return item


def get_attempt_by_token(token: str) -> dict[str, Any] | None:
    ensure_db()
    with _db() as connection:
        row = connection.execute(
            "SELECT * FROM quiz_attempts WHERE token = ?",
            (token,),
        ).fetchone()
    return _row_to_dict(row) if row else None


def get_attempt_by_id(attempt_id: int) -> dict[str, Any] | None:
    ensure_db()
    with _db() as connection:
        row = connection.execute(
            "SELECT * FROM quiz_attempts WHERE id = ?",
            (int(attempt_id),),
        ).fetchone()
    return _row_to_dict(row) if row else None


def list_attempts(
    *,
    query: str = "",
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[dict[str, Any]], int]:
    ensure_db()
    limit = max(1, min(int(limit), 200))
    offset = max(0, int(offset))
    where = ""
    params: list[Any] = []
    if query.strip():
        needle = f"%{query.strip()}%"
        where = "WHERE name LIKE ? OR identifier LIKE ? OR band_title LIKE ?"
        params = [needle, needle, needle]
    with _db() as connection:
        total = int(
            connection.execute(
                f"SELECT COUNT(*) FROM quiz_attempts {where}",
                params,
            ).fetchone()[0]
        )
        rows = connection.execute(
            f"""
            SELECT * FROM quiz_attempts
            {where}
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            [*params, limit, offset],
        ).fetchall()
    return [_row_to_dict(row) for row in rows], total


def all_attempts() -> list[dict[str, Any]]:
    ensure_db()
    with _db() as connection:
        rows = connection.execute(
            "SELECT * FROM quiz_attempts ORDER BY id DESC"
        ).fetchall()
    return [_row_to_dict(row) for row in rows]


def dashboard_stats() -> dict[str, Any]:
    ensure_db()
    today = datetime.now().astimezone().date().isoformat()
    with _db() as connection:
        summary = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                COALESCE(AVG(score), 0) AS average,
                COALESCE(MAX(score), 0) AS highest,
                COALESCE(SUM(CASE WHEN created_at LIKE ? THEN 1 ELSE 0 END), 0) AS today
            FROM quiz_attempts
            """,
            (f"{today}%",),
        ).fetchone()
        distribution = connection.execute(
            """
            SELECT band_title, COUNT(*) AS count
            FROM quiz_attempts
            GROUP BY band_title
            ORDER BY count DESC, band_title
            """
        ).fetchall()
    return {
        "total": int(summary["total"]),
        "average": round(float(summary["average"]), 1),
        "highest": int(summary["highest"]),
        "today": int(summary["today"]),
        "distribution": [dict(row) for row in distribution],
    }
