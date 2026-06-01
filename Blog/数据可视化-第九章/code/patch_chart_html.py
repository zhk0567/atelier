"""Rewrite pyecharts HTML to use same-origin ECharts assets (CSP + cache)."""

from __future__ import annotations

import re
from pathlib import Path

from _paths import HTML_DIR, STATIC_BLOG_DIR, ensure_dirs

CDN_ECHARTS = "https://assets.pyecharts.org/assets/v5/echarts.min.js"
CDN_GL = "https://assets.pyecharts.org/assets/v5/echarts-gl.min.js"
LOCAL_ECHARTS = "/static/vendor/echarts.min.js"
LOCAL_GL = "/static/vendor/echarts-gl.min.js"

_REPLACEMENTS = (
    (CDN_ECHARTS, LOCAL_ECHARTS),
    (CDN_GL, LOCAL_GL),
)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new = text
    for old, new_url in _REPLACEMENTS:
        new = new.replace(old, new_url)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def patch_all() -> int:
    ensure_dirs()
    n = 0
    for directory in (HTML_DIR, STATIC_BLOG_DIR):
        if not directory.is_dir():
            continue
        for path in directory.glob("*.html"):
            if patch_file(path):
                n += 1
    return n


if __name__ == "__main__":
    print(f"patched {patch_all()} html file(s)")
