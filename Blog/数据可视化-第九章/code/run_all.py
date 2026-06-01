"""生成第九章全部 HTML 图表与 PNG 预览，并同步到 static/blog/dataviz-ch09/。"""

from __future__ import annotations

import importlib
import shutil
import sys
from pathlib import Path

from _paths import HTML_DIR, PNG_DIR, STATIC_BLOG_DIR, ensure_dirs

SCRIPTS = [
    "fig_9_02_bar",
    "fig_9_03_line",
    "fig_9_04_pie",
    "fig_9_05_donut",
    "fig_9_06_scatter",
    "fig_9_07_effect_scatter",
    "fig_9_08_bar3d",
    "fig_9_09_sankey",
    "fig_9_10_grid",
    "fig_9_11_page",
    "fig_9_13_tab",
    "fig_9_15_timeline",
    "fig_9_16_theme_roma",
    "fig_9_17_django_embed",
    "hupu_section_bar",
    "hupu_hourly_line",
    "ex05_sine_animation",
]


def _run_module(name: str) -> None:
    mod = importlib.import_module(name)
    mod.main()
    print(f"[ok] {name}")


def _sync_static() -> None:
    ensure_dirs()
    for src_dir, pattern in ((HTML_DIR, "*.html"), (PNG_DIR, "*.png"), (PNG_DIR, "*.gif")):
        for path in src_dir.glob(pattern):
            shutil.copy2(path, STATIC_BLOG_DIR / path.name)
    print(f"[sync] -> {STATIC_BLOG_DIR}")


def main() -> None:
    code_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(code_dir))
    ensure_dirs()
    for name in SCRIPTS:
        _run_module(name)
    import export_png_previews
    import ensure_vendors
    import patch_chart_html

    export_png_previews.main()
    _sync_static()
    try:
        ensure_vendors.main()
    except Exception as exc:
        print(f"[vendor] warn: {exc}")
    n = patch_chart_html.patch_all()
    print(f"[patch] {n} html -> local echarts")
    print("done.")


if __name__ == "__main__":
    main()
