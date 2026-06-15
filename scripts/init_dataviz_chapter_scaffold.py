"""Create data visualization course chapter scaffolds (ch01–ch08) and update standalone manifest."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog"
MANIFEST = BLOG / "standalone" / "manifest.json"

CHAPTER_CN = {
    1: "一",
    2: "二",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
    8: "八",
    9: "九",
}


def index_md(ch: int) -> str:
    cn = CHAPTER_CN[ch]
    return f"""---
title: 数据可视化技术 · 第{cn}章（筹备中）
category: 数据可视化
status: draft
---

# 第{cn}章（筹备中）

> 本章笔记筹备中。目录与脚本脚手架已就绪，正文撰写完成后将 manifest 中 `status` 改为 `published`。

## 下一步

1. 按教材章节撰写 `index.md` 正文。
2. 在 `code/` 下补充图表脚本，运行 `python code/run_all.py` 同步静态资源。
3. 在 [standalone/manifest.json](../standalone/manifest.json) 更新标题、摘要与 `features`（如 `toc`、`pyecharts`）。
"""


def paths_py(slug: str) -> str:
    return f'''"""Paths for blog assets (run scripts from repo root or this folder)."""

from __future__ import annotations

from pathlib import Path

CHAPTER_ROOT = Path(__file__).resolve().parents[1]
HTML_DIR = CHAPTER_ROOT / "assets" / "html"
PNG_DIR = CHAPTER_ROOT / "assets" / "png"
STATIC_BLOG_DIR = CHAPTER_ROOT.parents[1] / "static" / "blog" / "{slug}"


def ensure_dirs() -> None:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_BLOG_DIR.mkdir(parents=True, exist_ok=True)
'''


def run_all_py() -> str:
    return '''"""Generate chapter assets and sync to static/blog/."""

from __future__ import annotations

import shutil

from _paths import HTML_DIR, PNG_DIR, STATIC_BLOG_DIR, ensure_dirs


def _sync_static() -> None:
    ensure_dirs()
    for src_dir, pattern in ((HTML_DIR, "*.html"), (PNG_DIR, "*.png"), (PNG_DIR, "*.gif")):
        for path in src_dir.glob(pattern):
            shutil.copy2(path, STATIC_BLOG_DIR / path.name)
    print(f"[sync] -> {STATIC_BLOG_DIR}")


def main() -> None:
    ensure_dirs()
    _sync_static()
    print("[ok] scaffold: add figure scripts under code/ then re-run")


if __name__ == "__main__":
    main()
'''


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    base_posts = [
        p for p in manifest.get("posts", [])
        if not str(p.get("slug", "")).startswith("dataviz-ch")
    ]
    ch09_entry = next(
        (p for p in manifest.get("posts", []) if p.get("slug") == "dataviz-ch09"),
        None,
    )
    course_posts: list[dict] = []

    for ch in range(1, 10):
        slug = f"dataviz-ch{ch:02d}"
        cn = CHAPTER_CN[ch]
        folder = f"数据可视化-第{cn}章"
        chapter_dir = BLOG / folder

        if ch == 9:
            if ch09_entry:
                course_posts.append(ch09_entry)
            continue

        code_dir = chapter_dir / "code"
        code_dir.mkdir(parents=True, exist_ok=True)
        if not (chapter_dir / "index.md").is_file():
            (chapter_dir / "index.md").write_text(index_md(ch), encoding="utf-8")
        (code_dir / "_paths.py").write_text(paths_py(slug), encoding="utf-8")
        (code_dir / "run_all.py").write_text(run_all_py(), encoding="utf-8")

        course_posts.append(
            {
                "slug": slug,
                "folder": folder,
                "title": f"数据可视化技术 · 第{cn}章（筹备中）",
                "series": "course-notes",
                "category": "数据可视化",
                "chapter": ch,
                "status": "draft",
                "summary": f"《Python 数据可视化（第 2 版）》第 {ch} 章笔记筹备中。",
            }
        )

    manifest["posts"] = base_posts + sorted(course_posts, key=lambda p: p.get("chapter", 0))
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {MANIFEST} with {len(course_posts)} course-notes entries")


if __name__ == "__main__":
    main()
