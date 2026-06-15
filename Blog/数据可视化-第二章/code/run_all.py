"""Generate chapter assets and sync to static/blog/."""

from __future__ import annotations

import shutil
from pathlib import Path

from _paths import HTML_DIR, PNG_DIR, STATIC_BLOG_DIR, ensure_dirs


def _sync_static() -> None:
    ensure_dirs()
    for src_dir, pattern in ((HTML_DIR, "*.html"), (PNG_DIR, "*.png"), (PNG_DIR, "*.gif")):
        for path in src_dir.glob(pattern):
            shutil.copy2(path, STATIC_BLOG_DIR / path.name)
    print(f"[sync] -> {STATIC_BLOG_DIR}")


def main() -> None:
    ensure_dirs()
    _sync_static()
    print("[ok] scaffold: add figure scripts under code/ then re-run")


if __name__ == "__main__":
    main()
