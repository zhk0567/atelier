# -*- coding: utf-8 -*-
"""Scan F:\\Study\\Algorithm topic notes.md into Blog/algorithm-guides/manifest.json."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

import sys

ATELIER_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ATELIER_ROOT))
sys.path.insert(0, str(ATELIER_ROOT / "scripts"))

from app.config import algorithm_root, blog_algorithm_dir_name  # noqa: E402
from algorithm_guide_lib import (  # noqa: E402
    MANIFEST_PATH,
    assign_guide_toc,
    assign_guide_tier,
    blog_title,
    category_from_topic_path,
    slug_from_topic_path,
    topic_path_from_notes,
)

GITHUB_BASE = "https://github.com/zhk0567/Algorithm/tree/main"
LEETCODE_TOPIC_RE = re.compile(r"problems/leetcode/\d", re.I)


def scan(algo_root: Path) -> list[dict]:
    posts: list[dict] = []
    slug_seen: dict[str, str] = {}
    py_root = algo_root / "python"
    if not py_root.is_dir():
        raise SystemExit(f"Missing python/ under {algo_root}")

    for path in sorted(py_root.rglob("notes.md")):
        rel = path.relative_to(algo_root)
        rel_posix = rel.as_posix()
        if LEETCODE_TOPIC_RE.search(rel_posix):
            continue
        topic_path = topic_path_from_notes(rel_posix)
        slug = slug_from_topic_path(topic_path)
        if slug in slug_seen:
            raise SystemExit(f"Slug conflict: {slug} for {rel_posix} and {slug_seen[slug]}")
        slug_seen[slug] = rel_posix

        cpp_notes = algo_root / "cpp" / Path(topic_path) / "notes.md" if topic_path else algo_root / "cpp" / "notes.md"
        repo_paths = [rel_posix.replace("\\", "/")]
        if topic_path:
            cpp_rel = f"cpp/{topic_path}/notes.md"
        else:
            cpp_rel = "cpp/notes.md"
        if (algo_root / cpp_rel.replace("/", "\\")).is_file():
            repo_paths.append(cpp_rel)

        guide_toc = assign_guide_toc(topic_path)
        guide_tier = assign_guide_tier(topic_path, guide_toc)
        category = category_from_topic_path(topic_path)

        posts.append({
            "slug": slug,
            "title": blog_title(topic_path, slug),
            "series": "algorithm",
            "category": category,
            "topic_path": topic_path or "overview",
            "repo_paths": repo_paths,
            "github": f"{GITHUB_BASE}/{repo_paths[0].rsplit('/', 1)[0]}",
            "folder": f"{blog_algorithm_dir_name()}/{slug}",
            "status": "draft",
            "guide_toc": guide_toc,
            "guide_tier": guide_tier,
        })

    posts.sort(key=lambda p: (p["category"], p["slug"]))
    return posts


def merge_existing_status(posts: list[dict], manifest_path: Path) -> None:
    if not manifest_path.is_file():
        return
    old = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_slug = {p["slug"]: p.get("status", "draft") for p in old.get("posts", [])}
    for p in posts:
        if p["slug"] in by_slug:
            p["status"] = by_slug[p["slug"]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan Algorithm topic notes into manifest.json")
    parser.add_argument("--algorithm-root", type=Path, default=algorithm_root())
    parser.add_argument("--out", type=Path, default=MANIFEST_PATH)
    args = parser.parse_args()

    posts = scan(args.algorithm_root)
    merge_existing_status(posts, args.out)

    payload = {
        "series": "algorithm",
        "github_repo": "https://github.com/zhk0567/Algorithm",
        "scanned_at": date.today().isoformat(),
        "count": len(posts),
        "posts": posts,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(posts)} posts to {args.out}")


if __name__ == "__main__":
    main()
