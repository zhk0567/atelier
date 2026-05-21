"""Project catalog merged from config/projects.json and xlsx."""

from __future__ import annotations

from app.config import all_projects_seed, pinned_project_ids
from site_data import merge_projects_catalog

_projects_cache: list[dict] | None = None


def clear_projects_cache() -> None:
    global _projects_cache
    _projects_cache = None


def get_all_projects() -> list[dict]:
    global _projects_cache
    if _projects_cache is not None:
        return _projects_cache
    try:
        _projects_cache = merge_projects_catalog(all_projects_seed())
    except Exception as exc:
        print(f"[atelier] project merge failed: {exc}", flush=True)
        _projects_cache = list(all_projects_seed())
    return _projects_cache


def get_pinned_projects() -> list[dict]:
    by_id = {p["id"]: p for p in get_all_projects()}
    return [by_id[i] for i in pinned_project_ids() if i in by_id]


def get_project(project_id: str) -> dict | None:
    return next((p for p in get_all_projects() if p["id"] == project_id), None)
