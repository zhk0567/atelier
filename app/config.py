"""Site paths and settings loaded from config/*.json + environment."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

ATELIER_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ATELIER_ROOT / "config"
DEFAULT_FRAMEWORK_ROOT = Path(r"F:\Study\Framework")
DEFAULT_BLOG_FRAMEWORK_DIR = "framework-guides"


def _deep_merge(base: dict, overlay: dict) -> dict:
    out = dict(base)
    for key, val in overlay.items():
        if isinstance(val, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], val)
        else:
            out[key] = val
    return out


def _load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_site_settings() -> dict:
    settings: dict = {}
    example = _load_json(CONFIG_DIR / "site.example.json")
    settings = _deep_merge(settings, example)
    settings = _deep_merge(settings, _load_json(CONFIG_DIR / "site.json"))
    settings = _deep_merge(settings, _load_json(CONFIG_DIR / "site.local.json"))
    env_root = os.environ.get("FRAMEWORK_ROOT", "").strip()
    if env_root:
        settings["framework_root"] = env_root
    return settings


def framework_root() -> Path:
    raw = load_site_settings().get("framework_root", "")
    if raw:
        return Path(str(raw)).expanduser()
    return DEFAULT_FRAMEWORK_ROOT


def blog_framework_dir_name() -> str:
    return str(
        load_site_settings().get("blog_framework_dir", DEFAULT_BLOG_FRAMEWORK_DIR)
    ).strip() or DEFAULT_BLOG_FRAMEWORK_DIR


def blog_framework_path() -> Path:
    return ATELIER_ROOT / "Blog" / blog_framework_dir_name()


def framework_manifest_path() -> Path:
    return blog_framework_path() / "manifest.json"


def guide_toc_dir() -> Path:
    return blog_framework_path() / "_meta" / "guide-toc"


@lru_cache(maxsize=1)
def load_projects_config() -> dict:
    path = CONFIG_DIR / "projects.json"
    if not path.is_file():
        return {"pinned_ids": [], "projects": []}
    return json.loads(path.read_text(encoding="utf-8"))


def pinned_project_ids() -> tuple[str, ...]:
    return tuple(load_projects_config().get("pinned_ids", []))


def all_projects_seed() -> list[dict]:
    return list(load_projects_config().get("projects", []))
