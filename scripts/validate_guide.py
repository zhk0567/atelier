"""Validate Framework official-guide blog posts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from guide_lib import (  # noqa: E402
    BLOG_FRAMEWORK,
    MANIFEST_PATH,
    load_toc,
    strip_frontmatter,
    validate_guide_body,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", action="append")
    parser.add_argument("--all-published", action="store_true")
    parser.add_argument("--all-drafts", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any failure")
    args = parser.parse_args()

    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    posts = data.get("posts", [])
    if args.slug:
        wanted = set(args.slug)
        posts = [p for p in posts if p["slug"] in wanted]
    elif args.all_published:
        posts = [p for p in posts if p.get("status") == "published"]
    elif args.all_drafts:
        posts = [p for p in posts if p.get("status") == "draft"]
    else:
        parser.error("Specify --slug, --all-published, or --all-drafts")

    failed = 0
    for entry in posts:
        slug = entry["slug"]
        path = BLOG_FRAMEWORK / slug / "index.md"
        if not path.is_file():
            print(f"FAIL {slug}: missing index.md")
            failed += 1
            continue
        raw = path.read_text(encoding="utf-8")
        body = strip_frontmatter(raw)
        toc_id = entry.get("guide_toc", "generic-backend")
        try:
            toc = load_toc(toc_id)
        except FileNotFoundError:
            print(f"FAIL {slug}: unknown guide_toc {toc_id}")
            failed += 1
            continue
        errors = validate_guide_body(body, toc, slug=slug)
        if errors:
            print(f"FAIL {slug}:")
            for e in errors:
                print(f"  - {e}")
            failed += 1
        else:
            print(f"OK {slug}")

    if failed and args.strict:
        sys.exit(1)
    print(f"Done: {len(posts) - failed} ok, {failed} failed")


if __name__ == "__main__":
    main()
