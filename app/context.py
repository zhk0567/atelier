"""Shared Jinja context: hubs, wallpapers, wiki nav."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi.templating import Jinja2Templates

from app.config import ATELIER_ROOT
from app.constants import (
    AVAILABILITY,
    BIO,
    EMAIL,
    FOCUS,
    GITHUB,
    HIGHLIGHTS,
    LINKEDIN,
    LOCATION,
    SITE_NAME,
    SITE_TITLE,
    STATS,
    TAGLINE,
    TWITTER,
    UI,
    HERO_SUBTITLE,
)
from app.projects import get_all_projects
from site_data import build_data_hubs, get_spreadsheet_context, load_site_data

TEMPLATES_DIR = ATELIER_ROOT / "templates"
STATIC_DIR = ATELIER_ROOT / "static"
DATA_DIR = ATELIER_ROOT / "data"
WIKI_IMG_DIR = STATIC_DIR / "img" / "wiki"

WALLPAPER_EXTS = {".mp4", ".webm", ".mov", ".jpg", ".jpeg", ".png", ".webp", ".gif"}
WALLPAPER_VIDEO_EXTS = {".mp4", ".webm", ".mov"}
_WALLPAPER_PATHS: dict[str, Path] = {}

HUB_ICON_FILES: dict[str, str] = {
    "projects": "crafting_table",
    "certs": "item_map",
    "hobbies": "item_compass",
    "books": "item_book",
    "anime": "bookshelf",
    "movies": "bookshelf",
    "games": "item_compass",
    "school": "oak_planks",
    "articles": "item_book",
}

templates = Jinja2Templates(directory=TEMPLATES_DIR)


def media_type_for_path(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".mov": "video/quicktime",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "application/octet-stream")


def list_wallpapers() -> list[dict]:
    global _WALLPAPER_PATHS
    _WALLPAPER_PATHS.clear()
    if not DATA_DIR.is_dir():
        return []
    files = sorted(
        (p for p in DATA_DIR.iterdir() if p.is_file() and p.suffix.lower() in WALLPAPER_EXTS),
        key=lambda p: p.name.lower(),
    )
    items: list[dict] = []
    for i, path in enumerate(files):
        wid = f"wp-{i}"
        _WALLPAPER_PATHS[wid] = path
        items.append({
            "id": wid,
            "label": path.stem,
            "url": f"/wallpaper/{wid}",
            "is_video": path.suffix.lower() in WALLPAPER_VIDEO_EXTS,
        })
    return items


def wallpaper_paths() -> dict[str, Path]:
    return _WALLPAPER_PATHS


def load_wiki_assets() -> dict[str, str]:
    out: dict[str, str] = {}
    if WIKI_IMG_DIR.is_dir():
        for path in WIKI_IMG_DIR.glob("*.png"):
            out[path.stem] = f"/static/img/wiki/{path.name}"
        for path in WIKI_IMG_DIR.glob("*.gif"):
            out[path.stem] = f"/static/img/wiki/{path.name}"
    return out


def build_hub_icons(assets: dict[str, str]) -> dict[str, str]:
    fallback = assets.get("crafting_table", "/static/img/wiki/crafting_table.png")
    return {hub_id: assets.get(stem, fallback) for hub_id, stem in HUB_ICON_FILES.items()}


def build_wiki_nav(hubs: list[dict]) -> list[dict]:
    portal_children = [{"label": h["label"], "url": h["url"], "external": False} for h in hubs]
    return [
        {
            "label": "站点",
            "children": [
                {"label": "主页面", "url": "/", "external": False},
                {"label": "全部项目", "url": "/projects", "external": False},
                {"label": UI["label_blog"], "url": "/blog", "external": False},
                {
                    "label": UI["link_framework_guides"],
                    "url": "/blog/series/framework",
                    "external": False,
                },
            ],
        },
        {"label": "数据分类", "children": portal_children},
    ]


def site_context() -> dict:
    hubs: list[dict] = []
    try:
        data = load_site_data()
        sheet = get_spreadsheet_context()
        hubs = build_data_hubs(data, len(get_all_projects()))
    except Exception as exc:
        print(f"[atelier] zhita_settings.xlsx load failed: {exc}", flush=True)
        sheet = {}
    site_name = sheet.get("site_name", SITE_NAME)
    sn = (site_name or "").strip()
    mark = sn[:4] if sn else "?"
    ui = {**UI, **sheet.get("ui", {})}
    wiki_assets = load_wiki_assets()
    return {
        "site_name": site_name,
        "brand_mark": mark,
        "site_title": sheet.get("site_title", SITE_TITLE),
        "tagline": sheet.get("tagline", TAGLINE),
        "hero_subtitle": sheet.get("hero_subtitle", HERO_SUBTITLE),
        "bio": sheet.get("bio", BIO),
        "focus": sheet.get("focus", FOCUS),
        "availability": sheet.get("availability", AVAILABILITY),
        "location": LOCATION,
        "email": EMAIL,
        "github": GITHUB,
        "linkedin": LINKEDIN,
        "twitter": TWITTER,
        "year": datetime.now().year,
        "ui": ui,
        "stats": sheet.get("stats", STATS),
        "data_hubs": hubs,
        "wiki_nav": build_wiki_nav(hubs),
        "wiki_assets": wiki_assets,
        "hub_icons": build_hub_icons(wiki_assets),
        "wallpapers": list_wallpapers(),
        "highlights": sheet.get("highlights", HIGHLIGHTS),
        "certificates": sheet.get("certificates", []),
        "education_line": sheet.get("education_line", ""),
        "reading_line": sheet.get("reading_line", ""),
        "books_featured": sheet.get("books_featured", []),
        "games_count": sheet.get("games_count", 0),
    }
