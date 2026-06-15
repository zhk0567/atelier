"""Site paths and settings loaded from config/*.json + environment."""

from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from pathlib import Path

ATELIER_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ATELIER_ROOT / "config"
DEFAULT_FRAMEWORK_ROOT = Path(r"F:\Study\Framework")
DEFAULT_ALGORITHM_ROOT = Path(r"F:\Study\Algorithm")
DEFAULT_BLOG_FRAMEWORK_DIR = "framework-guides"
DEFAULT_BLOG_ALGORITHM_DIR = "algorithm-guides"
DEFAULT_BLOG_HOTSPOT_DIR = "hotspot"
DEFAULT_BLOG_STANDALONE_DIR = "standalone"

WIKI_DIR = ATELIER_ROOT / "Wiki"
DEFAULT_TRUSTED_HOSTS = "zhkun.xyz,www.zhkun.xyz,127.0.0.1,localhost"
DEFAULT_RATE_LIMIT = "120/minute"
DEFAULT_RATE_LIMIT_WALLPAPER = "30/minute"


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    return raw in ("1", "true", "yes", "on")


def atelier_env() -> str:
    raw = os.environ.get("ATELIER_ENV", "development").strip().lower()
    return raw if raw in ("development", "production") else "development"


def is_production() -> bool:
    return atelier_env() == "production"


def trusted_hosts() -> list[str]:
    raw = os.environ.get("TRUSTED_HOSTS", DEFAULT_TRUSTED_HOSTS).strip()
    return [h.strip() for h in raw.split(",") if h.strip()]


def rate_limit_default() -> str:
    return os.environ.get("RATE_LIMIT_DEFAULT", DEFAULT_RATE_LIMIT).strip() or DEFAULT_RATE_LIMIT


def rate_limit_wallpaper() -> str:
    return (
        os.environ.get("RATE_LIMIT_WALLPAPER", DEFAULT_RATE_LIMIT_WALLPAPER).strip()
        or DEFAULT_RATE_LIMIT_WALLPAPER
    )


def block_probe_paths() -> bool:
    return _env_bool("BLOCK_PROBE_PATHS", default=True)


def parse_rate_limit(spec: str) -> tuple[int, float]:
    """Parse '120/minute' -> (120, 60.0 seconds window)."""
    spec = spec.strip().lower()
    if "/" not in spec:
        return 120, 60.0
    count_s, unit = spec.split("/", 1)
    try:
        count = max(1, int(count_s.strip()))
    except ValueError:
        count = 120
    unit = unit.strip().rstrip("s")
    windows = {
        "second": 1.0,
        "minute": 60.0,
        "hour": 3600.0,
        "day": 86400.0,
    }
    window = windows.get(unit, 60.0)
    return count, window


def wiki_slug_is_valid(wiki_slug: str) -> bool:
    if not wiki_slug or not re.fullmatch(r"[a-zA-Z0-9_-]+", wiki_slug):
        return False
    wiki_path = (WIKI_DIR / wiki_slug).resolve()
    try:
        wiki_path.relative_to(WIKI_DIR.resolve())
    except ValueError:
        return False
    return wiki_path.is_dir()


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
    env_algo = os.environ.get("ALGORITHM_ROOT", "").strip()
    if env_algo:
        settings["algorithm_root"] = env_algo
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


def algorithm_root() -> Path:
    raw = load_site_settings().get("algorithm_root", "")
    if raw:
        return Path(str(raw)).expanduser()
    return DEFAULT_ALGORITHM_ROOT


def blog_algorithm_dir_name() -> str:
    return str(
        load_site_settings().get("blog_algorithm_dir", DEFAULT_BLOG_ALGORITHM_DIR)
    ).strip() or DEFAULT_BLOG_ALGORITHM_DIR


def blog_algorithm_path() -> Path:
    return ATELIER_ROOT / "Blog" / blog_algorithm_dir_name()


def algorithm_manifest_path() -> Path:
    return blog_algorithm_path() / "manifest.json"


def algorithm_guide_toc_dir() -> Path:
    return blog_algorithm_path() / "_meta" / "guide-toc"


def blog_hotspot_dir_name() -> str:
    return str(
        load_site_settings().get("blog_hotspot_dir", DEFAULT_BLOG_HOTSPOT_DIR)
    ).strip() or DEFAULT_BLOG_HOTSPOT_DIR


def blog_hotspot_path() -> Path:
    return ATELIER_ROOT / "Blog" / blog_hotspot_dir_name()


def hotspot_manifest_path() -> Path:
    return blog_hotspot_path() / "manifest.json"


def blog_standalone_dir_name() -> str:
    return str(
        load_site_settings().get("blog_standalone_dir", DEFAULT_BLOG_STANDALONE_DIR)
    ).strip() or DEFAULT_BLOG_STANDALONE_DIR


def blog_standalone_path() -> Path:
    return ATELIER_ROOT / "Blog" / blog_standalone_dir_name()


def standalone_manifest_path() -> Path:
    return blog_standalone_path() / "manifest.json"


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


MC_VTUBER_DIR = ATELIER_ROOT / "MC_Vtuber"


@lru_cache(maxsize=1)
def mc_vtuber_live2d_ready() -> bool:
    """True when Cubism model assets exist under MC_Vtuber/."""
    textures = MC_VTUBER_DIR / "MC_Vtuber.2048"
    return (
        (MC_VTUBER_DIR / "MC_Vtuber.model3.json").is_file()
        and (MC_VTUBER_DIR / "MC_Vtuber.moc3").is_file()
        and (textures / "texture_00.png").is_file()
        and (textures / "texture_01.png").is_file()
        and (textures / "texture_02.png").is_file()
    )


MC_VTUBER_STATIC_PREFIX = "/static/MC_Vtuber"


def mc_vtuber_model_url() -> str:
    return f"{MC_VTUBER_STATIC_PREFIX}/MC_Vtuber.model3.json"


def nyxviz_settings() -> dict:
    raw = load_site_settings().get("nyxviz", {})
    return raw if isinstance(raw, dict) else {}


def nyxviz_video_path() -> str:
    return str(nyxviz_settings().get("video_path", "/static/nyxviz/video.html")).strip()


def nyxviz_data_origin() -> str:
    """OSS/CDN origin for Nyx .dat fetch (no trailing slash). Empty when same-origin."""
    settings = nyxviz_settings()
    explicit = str(settings.get("nyx_data_origin", "")).strip().rstrip("/")
    if explicit:
        return explicit
    base = nyxviz_data_base()
    if base.startswith("http://") or base.startswith("https://"):
        from urllib.parse import urlparse

        parsed = urlparse(base)
        if parsed.scheme and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}"
    return ""


def nyxviz_static_figures_only() -> bool:
    """Serve pre-rendered PNG figures only; skip Nyx .dat volume fetch."""
    settings = nyxviz_settings()
    if "static_figures_only" in settings:
        return bool(settings.get("static_figures_only"))
    from app.nyxviz_bundle import nyxviz_bundle_status

    status = nyxviz_bundle_status()
    return int(status.get("nyx_dat_count", 0) or 0) == 0


def nyxviz_data_base() -> str:
    """Public URL prefix for Nyx .dat files (trailing slash). Empty when static-only."""
    if nyxviz_static_figures_only():
        return ""
    settings = nyxviz_settings()
    raw = str(settings.get("nyx_data_base", "")).strip()
    if raw:
        return raw if raw.endswith("/") else f"{raw}/"
    return "/static/nyxviz/Nyx/"
