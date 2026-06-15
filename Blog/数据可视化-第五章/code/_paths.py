"""Paths for blog assets (run scripts from repo root or this folder)."""

from __future__ import annotations

from pathlib import Path

CHAPTER_ROOT = Path(__file__).resolve().parents[1]
HTML_DIR = CHAPTER_ROOT / "assets" / "html"
PNG_DIR = CHAPTER_ROOT / "assets" / "png"
STATIC_BLOG_DIR = CHAPTER_ROOT.parents[1] / "static" / "blog" / "dataviz-ch05"


def ensure_dirs() -> None:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_BLOG_DIR.mkdir(parents=True, exist_ok=True)
