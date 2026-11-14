#!/usr/bin/env python3
"""Ensure media meta JSON contains every xlsx row key (resume-safe skeleton)."""

from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META_DIR = ROOT / "data" / "media_meta"
IMG_ROOT = ROOT / "static" / "img" / "media"

import sys

sys.path.insert(0, str(ROOT / "scripts"))
from fetch_media_covers import _slug, load_anime, load_books, load_games  # noqa: E402


def _load(kind: str) -> dict:
    path = META_DIR / f"{kind}.json"
    if not path.is_file():
        return {"updated": "", "items": {}}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        return {"updated": "", "items": {}}
    if not isinstance(data.get("items"), dict):
        data["items"] = {}
    return data


def _save(kind: str, data: dict) -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    data["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (META_DIR / f"{kind}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _link_cover(kind: str, title: str, rec: dict) -> None:
    img_dir = IMG_ROOT / kind
    if not img_dir.is_dir():
        return
    slug = _slug(title)
    for path in img_dir.glob(f"{slug}.*"):
        if path.is_file() and path.stat().st_size >= 800:
            rec["cover_path"] = f"/static/img/media/{kind}/{path.name}"
            if not rec.get("matched"):
                rec["matched"] = True
            if not rec.get("source"):
                rec["source"] = "local"
            return


def sync_kind(kind: str, rows: list[dict]) -> tuple[int, int]:
    data = _load(kind)
    items = data["items"]
    for row in rows:
        key = row["key"]
        rec = items.get(key) if isinstance(items.get(key), dict) else {}
        base = {
            "title": key,
            "series": row.get("series") or "",
            "author": row.get("author") or "",
            "category": row.get("category") or "",
            "platform": row.get("platform") or "",
            "matched": False,
            "cover_path": "",
            "subtitle": "",
            "score": None,
            "episodes": None,
            "year": None,
            "date": "",
            "tags": [],
            "source": "",
            "source_id": "",
        }
        merged = {**base, **rec, "title": key}
        for field in ("series", "author", "category", "platform"):
            if row.get(field) and not merged.get(field):
                merged[field] = row[field]
        _link_cover(kind, key, merged)
        items[key] = merged
    # drop orphan keys not in xlsx? keep extras but report
    wanted = {r["key"] for r in rows}
    extras = [k for k in list(items) if k not in wanted]
    data["items"] = items
    _save(kind, data)
    covers = sum(1 for v in items.values() if v.get("cover_path"))
    return len(wanted), covers


def main() -> int:
    a_n, a_c = sync_kind("anime", load_anime())
    g_n, g_c = sync_kind("games", load_games())
    b_n, b_c = sync_kind("books", load_books())
    print(f"anime keys={a_n} covers={a_c}")
    print(f"games keys={g_n} covers={g_c}")
    print(f"books keys={b_n} covers={b_c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
