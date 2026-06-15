"""NyxViz static bundle presence checks."""

from __future__ import annotations

from pathlib import Path

from app.config import ATELIER_ROOT

NYXVIZ_DIR = ATELIER_ROOT / "static" / "nyxviz"
NYXVIZ_VIDEO = NYXVIZ_DIR / "video.html"
NYXVIZ_ASSETS = NYXVIZ_DIR / "assets"
NYXVIZ_FIGURES = NYXVIZ_DIR / "figures"


def nyxviz_bundle_status() -> dict[str, bool | int]:
    """Return which parts of the NyxViz bundle exist on disk."""
    assets_js = list(NYXVIZ_ASSETS.glob("*.js")) if NYXVIZ_ASSETS.is_dir() else []
    figures = list(NYXVIZ_FIGURES.rglob("*.png")) if NYXVIZ_FIGURES.is_dir() else []
    return {
        "video_html": NYXVIZ_VIDEO.is_file(),
        "assets_js_count": len(assets_js),
        "figures_png_count": len(figures),
    }


def nyxviz_bundle_warnings() -> list[str]:
    """Human-readable warnings when the bundle is incomplete."""
    status = nyxviz_bundle_status()
    warnings: list[str] = []
    if not status["video_html"]:
        return warnings
    if status["assets_js_count"] == 0:
        warnings.append(
            "nyxviz: video.html exists but static/nyxviz/assets/ is missing — "
            "run scripts/sync_nyxviz_video.ps1 and deploy assets to the server"
        )
    if status["figures_png_count"] == 0:
        warnings.append(
            "nyxviz: static/nyxviz/figures/ is missing — "
            "run sync script and copy figures to the server (see docs/NYXVIZ_DEPLOY.md)"
        )
    return warnings
