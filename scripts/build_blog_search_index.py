"""Build static/blog/search-index.json from blog manifests (no FastAPI import)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog"
OUT = ROOT / "static" / "blog" / "search-index.json"

MANIFESTS = (
    BLOG / "standalone" / "manifest.json",
    BLOG / "framework-guides" / "manifest.json",
    BLOG / "algorithm-guides" / "manifest.json",
    BLOG / "hotspot" / "manifest.json",
)


def _entry_to_item(entry: dict) -> dict | None:
    if entry.get("status") != "published":
        return None
    slug = entry.get("slug", "")
    if not slug:
        return None
    return {
        "slug": slug,
        "title": entry.get("title", slug),
        "summary": entry.get("summary", ""),
        "series": entry.get("series", ""),
        "category": entry.get("category", ""),
        "url": f"/blog/{slug}",
    }


def load_index_items() -> list[dict]:
    items: list[dict] = []
    seen: set[str] = set()
    for path in MANIFESTS:
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for entry in data.get("posts", []):
            item = _entry_to_item(entry)
            if not item or item["slug"] in seen:
                continue
            seen.add(item["slug"])
            items.append(item)
    items.sort(key=lambda x: (x.get("series", ""), x.get("title", "")))
    return items


def main() -> None:
    items = load_index_items()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} entries -> {OUT}")


if __name__ == "__main__":
    main()
