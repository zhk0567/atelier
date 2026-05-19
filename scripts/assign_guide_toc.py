"""Sync guide_toc / guide_tier from index.md frontmatter into manifest.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from guide_lib import (  # noqa: E402
    BLOG_FRAMEWORK,
    MANIFEST_PATH,
    assign_guide_toc_id,
    load_toc,
)

_FM_TOC_RE = re.compile(r"^guide_toc:\s*(\S+)\s*$", re.M)
_FM_TIER_RE = re.compile(r"^guide_tier:\s*(\S+)\s*$", re.M)


def read_frontmatter_guide_fields(slug: str) -> tuple[str | None, str | None]:
    path = BLOG_FRAMEWORK / slug / "index.md"
    if not path.is_file():
        return None, None
    raw = path.read_text(encoding="utf-8")
    toc_m = _FM_TOC_RE.search(raw)
    tier_m = _FM_TIER_RE.search(raw)
    return (toc_m.group(1) if toc_m else None, tier_m.group(1) if tier_m else None)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--category",
        help="Only update manifest entries with this category (e.g. Front-end)",
    )
    args = parser.parse_args()

    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    updated = 0
    for entry in data.get("posts", []):
        if args.category and entry.get("category") != args.category:
            continue
        slug = entry["slug"]
        fm_toc, fm_tier = read_frontmatter_guide_fields(slug)
        toc_id = fm_toc or assign_guide_toc_id(entry)
        entry["guide_toc"] = toc_id
        if fm_tier:
            entry["guide_tier"] = fm_tier
        else:
            try:
                toc = load_toc(toc_id)
                entry["guide_tier"] = toc.get("tier", "medium")
            except FileNotFoundError:
                entry["guide_tier"] = "medium"
        updated += 1
    MANIFEST_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated guide_toc for {updated} posts" + (f" (category={args.category})" if args.category else ""))


if __name__ == "__main__":
    main()
