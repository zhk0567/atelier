"""In-memory cache for rendered markdown keyed by source file mtime."""

from __future__ import annotations

from pathlib import Path

_RENDER_CACHE: dict[tuple, object] = {}
_MAX_ENTRIES = 512


def file_cache_key(path: Path) -> tuple[str, int, int]:
    if not path.is_file():
        return ("", 0, 0)
    st = path.stat()
    return (str(path.resolve()), st.st_mtime_ns, st.st_size)


def render_cached(cache_key: tuple[str, int, int], bucket: str, factory):
    key = (bucket, cache_key)
    hit = _RENDER_CACHE.get(key)
    if hit is not None:
        return hit
    value = factory()
    if len(_RENDER_CACHE) >= _MAX_ENTRIES:
        _RENDER_CACHE.clear()
    _RENDER_CACHE[key] = value
    return value


def clear_render_cache() -> None:
    _RENDER_CACHE.clear()
