"""Content for the personal requirements / future tasks page.

The page is intentionally hand-curated: its source material is a private diary and
a group-chat export that never enter the repository.  Only the distilled content
below is published, with every real name replaced by its pinyin initials.
"""

from __future__ import annotations

import json
from datetime import date
from functools import lru_cache

from app.config import ATELIER_ROOT

PERSONAL_JSON = ATELIER_ROOT / "data" / "personal.json"

_EMPTY: dict = {
    "updated": "",
    "deadline": "",
    "deadline_label": "十年内",
    "countdown_label": "十年之约",
    "requirements_intro": "",
    "requirements_source": "",
    "requirements": [],
    "tasks_intro": "",
    "tasks_source": "",
    "tasks": [],
    "task_categories": [],
    "category_counts": {},
    "notes": [],
}


def _empty_payload() -> dict:
    return {
        key: (value.copy() if isinstance(value, (dict, list)) else value)
        for key, value in _EMPTY.items()
    }


def _text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _rows(payload: dict, key: str) -> list[dict]:
    rows = payload.get(key)
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


@lru_cache(maxsize=1)
def load_personal() -> dict:
    """Return the normalized page payload (cached until restart)."""
    try:
        payload = json.loads(PERSONAL_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[atelier] personal.json load failed: {exc}", flush=True)
        return _empty_payload()

    if not isinstance(payload, dict):
        print("[atelier] personal.json must contain an object", flush=True)
        return _empty_payload()

    requirements: list[dict] = []
    for row in _rows(payload, "requirements"):
        title = _text(row.get("title"))
        if not title:
            continue
        requirements.append({
            "id": _text(row.get("id")) or f"rule-{len(requirements) + 1}",
            "index": len(requirements) + 1,
            "title": title,
            "subtitle": _text(row.get("subtitle")),
            "why": _text(row.get("why")),
            "quote": _text(row.get("quote")),
            "quote_date": _text(row.get("quote_date")),
            "note": _text(row.get("note")),
        })

    categories: list[dict] = []
    seen_categories: set[str] = set()
    for row in _rows(payload, "task_categories"):
        cid = _text(row.get("id"))
        if not cid or cid in seen_categories:
            continue
        seen_categories.add(cid)
        categories.append({"id": cid, "label": _text(row.get("label")) or cid})
    labels = {c["id"]: c["label"] for c in categories}
    fallback_category = {"id": "other", "label": "其他"}

    tasks: list[dict] = []
    category_counts: dict[str, int] = {}
    for row in _rows(payload, "tasks"):
        text = _text(row.get("text"))
        if not text:
            continue
        category = _text(row.get("category")) or fallback_category["id"]
        if category not in labels:
            labels[category] = category
            categories.append({"id": category, "label": category})
        proposer = _text(row.get("proposer"))
        tasks.append({
            "id": _text(row.get("id")) or f"task-{len(tasks) + 1}",
            "text": text,
            "category": category,
            "category_label": labels[category],
            "proposer": proposer,
            "note": _text(row.get("note")),
            "deadline": _text(row.get("deadline")),
        })
        category_counts[category] = category_counts.get(category, 0) + 1

    notes = [_text(n) for n in (payload.get("notes") or []) if _text(n)]
    deadline_label = _text(payload.get("task_deadline_label")) or _EMPTY["deadline_label"]

    return {
        "updated": _text(payload.get("updated")),
        "deadline": _text(payload.get("deadline")),
        "deadline_label": deadline_label,
        "countdown_label": _text(payload.get("countdown_label")) or _EMPTY["countdown_label"],
        "requirements_intro": _text(payload.get("requirements_intro")),
        "requirements_source": _text(payload.get("requirements_source")),
        "requirements": requirements,
        "tasks_intro": _text(payload.get("tasks_intro")),
        "tasks_source": _text(payload.get("tasks_source")),
        "tasks": tasks,
        "task_categories": [c for c in categories if category_counts.get(c["id"])],
        "category_counts": category_counts,
        "notes": notes,
    }


def personal_stats(personal: dict | None = None) -> dict:
    data = personal or load_personal()
    deadline = data.get("deadline") or ""
    days_left = None
    if deadline:
        try:
            days_left = max(0, (date.fromisoformat(deadline) - date.today()).days)
        except ValueError:
            days_left = None
    return {
        "requirement_count": len(data.get("requirements") or []),
        "task_count": len(data.get("tasks") or []),
        "days_left": days_left,
    }


def clear_personal_cache() -> None:
    load_personal.cache_clear()
