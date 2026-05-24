"""JPEG derivatives for wallpapers and travel photos (faster first paint)."""

from __future__ import annotations

import json
from pathlib import Path

from app.config import ATELIER_ROOT

DATA_DIR = ATELIER_ROOT / "data"
TRAVEL_MANIFEST = ATELIER_ROOT / "data" / "travel" / "trips.json"
TRAVEL_UPLOAD_ROOT = ATELIER_ROOT / "static" / "uploads" / "travel"
GENERATED_WP_DIR = ATELIER_ROOT / "static" / "generated" / "wallpapers"

THUMB_MAX_WIDTH = 480
WEB_MAX_WIDTH = 1400
WALLPAPER_PREVIEW_MAX = 1600
JPEG_QUALITY_THUMB = 78
JPEG_QUALITY_WEB = 82

_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def thumb_filename(original: str) -> str:
    return f"{Path(original).stem}.thumb.jpg"


def web_filename(original: str) -> str:
    return f"{Path(original).stem}.web.jpg"


def wallpaper_preview_url(wid: str) -> str:
    return f"/static/generated/wallpapers/{wid}.jpg"


def _needs_regenerate(src: Path, dest: Path) -> bool:
    if not dest.is_file():
        return True
    try:
        return src.stat().st_mtime > dest.stat().st_mtime
    except OSError:
        return True


def _save_jpeg(im, dest: Path, quality: int) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=quality, optimize=True)


def _to_rgb(im):
    from PIL import Image

    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        alpha = im.split()[-1]
        bg.paste(im.convert("RGBA"), mask=alpha)
        return bg
    if im.mode == "P":
        return _to_rgb(im.convert("RGBA"))
    if im.mode != "RGB":
        return im.convert("RGB")
    return im


def ensure_derivative(src: Path, dest: Path, max_width: int, quality: int) -> bool:
    if not src.is_file() or src.suffix.lower() not in _IMAGE_EXTS:
        return False
    if not _needs_regenerate(src, dest):
        return True
    try:
        from PIL import Image
    except ImportError:
        return dest.is_file()
    try:
        with Image.open(src) as im:
            im = _to_rgb(im)
            if im.width > max_width:
                height = max(1, int(im.height * max_width / im.width))
                im = im.resize((max_width, height), Image.Resampling.LANCZOS)
            _save_jpeg(im, dest, quality)
        return dest.is_file()
    except OSError:
        return False


def ensure_travel_derivatives(base_dir: Path, filename: str) -> tuple[str | None, str | None]:
    src = base_dir / filename
    if not src.is_file():
        return None, None
    thumb_name = thumb_filename(filename)
    web_name = web_filename(filename)
    thumb_ok = ensure_derivative(
        src, base_dir / thumb_name, THUMB_MAX_WIDTH, JPEG_QUALITY_THUMB
    )
    web_ok = ensure_derivative(src, base_dir / web_name, WEB_MAX_WIDTH, JPEG_QUALITY_WEB)
    return (thumb_name if thumb_ok else None, web_name if web_ok else None)


def ensure_wallpaper_preview(wid: str, src: Path) -> bool:
    dest = GENERATED_WP_DIR / f"{wid}.jpg"
    return ensure_derivative(src, dest, WALLPAPER_PREVIEW_MAX, JPEG_QUALITY_WEB)


def warmup_media_derivatives() -> dict[str, int]:
    """Generate missing derivatives at startup."""
    stats = {"wallpapers": 0, "travel_photos": 0}
    try:
        from app.context import _build_wallpaper_catalog

        _, paths = _build_wallpaper_catalog()
        for wid, path in paths.items():
            if ensure_wallpaper_preview(wid, path):
                stats["wallpapers"] += 1
    except Exception:
        pass

    if TRAVEL_MANIFEST.is_file():
        try:
            raw = json.loads(TRAVEL_MANIFEST.read_text(encoding="utf-8"))
            trips = raw.get("trips") if isinstance(raw, dict) else raw
            if isinstance(trips, list):
                for trip in trips:
                    if not isinstance(trip, dict):
                        continue
                    trip_id = trip.get("id")
                    if not trip_id:
                        continue
                    base_dir = TRAVEL_UPLOAD_ROOT / str(trip_id)
                    for photo in trip.get("photos") or []:
                        if not isinstance(photo, dict):
                            continue
                        filename = photo.get("file") or ""
                        if not filename:
                            continue
                        thumb, web = ensure_travel_derivatives(base_dir, filename)
                        if thumb or web:
                            stats["travel_photos"] += 1
        except (json.JSONDecodeError, OSError):
            pass

    return stats
