"""Shared Jinja context: hubs, wallpapers, wiki nav."""

from __future__ import annotations

import json
import re
from datetime import datetime
from functools import lru_cache
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
# 全站导航与数据分类入口中不展示（/browse/* 仍可直链访问）
NAV_EXCLUDED_HUB_IDS = frozenset({"certs", "hobbies", "school", "articles", "projects"})

PROJECT_THUMB_STEMS: tuple[str, ...] = (
    "crafting_table",
    "bookshelf",
    "item_compass",
    "item_map",
    "oak_planks",
    "cobblestone",
)

HUB_ICON_FILES: dict[str, str] = {
    "projects": "crafting_table",
    "hobbies": "item_compass",
    "books": "item_book",
    "anime": "bookshelf",
    "movies": "bookshelf",
    "games": "item_compass",
    "school": "oak_planks",
}

templates = Jinja2Templates(directory=TEMPLATES_DIR)


def _jinja_project_thumb(project: dict) -> str:
    return project_thumb_url(project, load_wiki_assets())


templates.env.filters["project_thumb"] = _jinja_project_thumb


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


_WALLPAPER_MANIFEST = DATA_DIR / "wallpapers.json"
_WALLPAPER_SLUG_RE = re.compile(r"^wallpaper-\d{2}-[a-z0-9-]+$", re.I)


def _wallpaper_label_from_stem(stem: str) -> str:
    if _WALLPAPER_SLUG_RE.match(stem):
        slug = stem.split("-", 2)[-1] if stem.count("-") >= 2 else stem
        return slug.replace("-", " ").title()
    return stem


def _load_wallpaper_manifest() -> tuple[str | None, list[dict]]:
    if not _WALLPAPER_MANIFEST.is_file():
        return None, []
    try:
        data = json.loads(_WALLPAPER_MANIFEST.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None, []
    default_id = data.get("default")
    raw_items = data.get("items")
    if not isinstance(raw_items, list):
        return default_id if isinstance(default_id, str) else None, []
    items: list[dict] = []
    for entry in raw_items:
        if not isinstance(entry, dict):
            continue
        wid = entry.get("id")
        filename = entry.get("file")
        if not isinstance(wid, str) or not isinstance(filename, str):
            continue
        path = DATA_DIR / filename
        if not path.is_file() or path.suffix.lower() not in WALLPAPER_EXTS:
            continue
        if path.suffix.lower() in WALLPAPER_VIDEO_EXTS:
            continue
        label = entry.get("label")
        if not isinstance(label, str) or not label.strip():
            label = _wallpaper_label_from_stem(path.stem)
        items.append({
            "id": wid,
            "file": filename,
            "label": label.strip(),
            "path": path,
        })
    return default_id if isinstance(default_id, str) else None, items


def _build_wallpaper_catalog() -> tuple[list[dict], dict[str, Path]]:
    if not DATA_DIR.is_dir():
        return [], {}

    default_id, manifest_items = _load_wallpaper_manifest()
    items: list[dict] = []
    paths: dict[str, Path] = {}

    if manifest_items:
        for entry in manifest_items:
            wid = entry["id"]
            path = entry.get("path")
            if path is None:
                continue
            paths[wid] = path
            items.append({
                "id": wid,
                "label": entry["label"],
                "url": f"/wallpaper/{wid}",
                "is_video": path.suffix.lower() in WALLPAPER_VIDEO_EXTS,
                "default": default_id == wid if default_id else False,
            })
        if items and not any(i["default"] for i in items):
            items[0]["default"] = True
        return items, paths

    image_exts = WALLPAPER_EXTS - WALLPAPER_VIDEO_EXTS
    files = sorted(
        (p for p in DATA_DIR.iterdir() if p.is_file() and p.suffix.lower() in image_exts),
        key=lambda p: p.name.lower(),
    )
    for i, path in enumerate(files):
        wid = path.stem if _WALLPAPER_SLUG_RE.match(path.stem) else f"wallpaper-{i:02d}"
        paths[wid] = path
        items.append({
            "id": wid,
            "label": _wallpaper_label_from_stem(path.stem),
            "url": f"/wallpaper/{wid}",
            "is_video": path.suffix.lower() in WALLPAPER_VIDEO_EXTS,
            "default": i == 0,
        })
    return items, paths


@lru_cache(maxsize=1)
def _wallpaper_catalog() -> tuple[tuple[dict, ...], dict[str, str]]:
    items, paths = _build_wallpaper_catalog()
    path_index = {wid: str(path) for wid, path in paths.items()}
    return tuple(items), path_index


def list_wallpapers() -> tuple[dict, ...]:
    return _wallpaper_catalog()[0]


def wallpaper_paths() -> dict[str, Path]:
    return {wid: Path(p) for wid, p in _wallpaper_catalog()[1].items()}


@lru_cache(maxsize=1)
def load_wiki_assets() -> dict[str, str]:
    out: dict[str, str] = {}
    if WIKI_IMG_DIR.is_dir():
        for path in WIKI_IMG_DIR.glob("*.png"):
            out[path.stem] = f"/static/img/wiki/{path.name}"
        for path in WIKI_IMG_DIR.glob("*.gif"):
            out[path.stem] = f"/static/img/wiki/{path.name}"
    return dict(out)


def build_hub_icons(assets: dict[str, str]) -> dict[str, str]:
    fallback = assets.get("crafting_table", "/static/img/wiki/crafting_table.png")
    return {hub_id: assets.get(stem, fallback) for hub_id, stem in HUB_ICON_FILES.items()}


FRAMEWORK_CATEGORY_ICONS: dict[str, str] = {
    "Back-end": "crafting_table",
    "Front-end": "bookshelf",
    "Mobile": "item_compass",
    "Tooling": "item_map",
    "Data": "oak_planks",
    "Other": "cobblestone",
}


def framework_stack_thumb_url(stack: str, category: str, assets: dict[str, str]) -> str:
    fallback = assets.get("crafting_table", "/static/img/wiki/crafting_table.png")
    stem = FRAMEWORK_CATEGORY_ICONS.get(category) or FRAMEWORK_CATEGORY_ICONS.get("Other")
    if stem and stem in assets:
        return assets[stem]
    if stack:
        idx = sum(ord(c) for c in stack) % len(PROJECT_THUMB_STEMS)
        return assets.get(PROJECT_THUMB_STEMS[idx], fallback)
    return fallback


def project_thumb_url(project: dict, assets: dict[str, str]) -> str:
    fallback = assets.get("crafting_table", "/static/img/wiki/crafting_table.png")
    thumb = project.get("thumb", 1)
    try:
        idx = (int(thumb) - 1) % len(PROJECT_THUMB_STEMS)
    except (TypeError, ValueError):
        idx = 0
    stem = PROJECT_THUMB_STEMS[idx]
    return assets.get(stem, fallback)


def projects_with_thumbs(projects: list[dict], assets: dict[str, str]) -> list[dict]:
    return [{**p, "thumb_url": project_thumb_url(p, assets)} for p in projects]


def build_wiki_nav(hubs: list[dict]) -> list[dict]:
    # 项目入口仅在「站点」下；数据分类不重复展示应用项目 /projects
    portal_children = [
        {"label": h["label"], "url": h["url"], "external": False}
        for h in hubs
        if h.get("id") not in NAV_EXCLUDED_HUB_IDS
        and h.get("url") not in ("/projects", "/browse/projects")
    ]
    return [
        {
            "label": "站点",
            "children": [
                {"label": "主页面", "url": "/", "external": False},
                {"label": "项目", "url": "/projects", "external": False},
                {"label": UI["label_blog"], "url": "/blog", "external": False},
            ],
        },
        {"label": "数据分类", "children": portal_children},
    ]


def clear_context_cache() -> None:
    _wallpaper_catalog.cache_clear()
    load_wiki_assets.cache_clear()
    _site_context_core.cache_clear()


@lru_cache(maxsize=1)
def _site_context_core() -> dict:
    hubs: list[dict] = []
    sheet: dict = {}
    try:
        data = load_site_data()
        sheet = get_spreadsheet_context()
        all_hubs = build_data_hubs(data, len(get_all_projects()))
        hubs = [h for h in all_hubs if h["id"] not in NAV_EXCLUDED_HUB_IDS]
    except Exception as exc:
        print(f"[atelier] zhita_settings.xlsx load failed: {exc}", flush=True)
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
        "ui": ui,
        "stats": sheet.get("stats", STATS),
        "data_hubs": hubs,
        "wiki_nav": build_wiki_nav(hubs),
        "wiki_assets": wiki_assets,
        "hub_icons": build_hub_icons(wiki_assets),
        "wallpapers": list(list_wallpapers()),
        "books_featured": sheet.get("books_featured", []),
        "games_count": sheet.get("games_count", 0),
    }


def site_context() -> dict:
    return {
        **_site_context_core(),
        "location": LOCATION,
        "email": EMAIL,
        "github": GITHUB,
        "twitter": TWITTER,
        "year": datetime.now().year,
        "highlights": HIGHLIGHTS,
    }
