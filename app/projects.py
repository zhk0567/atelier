"""Project catalog merged from config/projects.json and xlsx."""

from __future__ import annotations

from app.config import all_projects_seed, pinned_project_ids
from site_data import merge_projects_catalog


def get_all_projects() -> list[dict]:
    try:
        return merge_projects_catalog(all_projects_seed())
    except Exception as exc:
        print(f"[atelier] project merge failed: {exc}", flush=True)
        return list(all_projects_seed())


def get_pinned_projects() -> list[dict]:
    by_id = {p["id"]: p for p in get_all_projects()}
    return [by_id[i] for i in pinned_project_ids() if i in by_id]


def get_project(project_id: str) -> dict | None:
    return next((p for p in get_all_projects() if p["id"] == project_id), None)
