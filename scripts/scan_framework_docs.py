"""Scan F:\\Study\\Framework stack guide markdown files and write Blog/Framework/manifest.json."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

import sys

ATELIER_ROOT = Path(__file__).resolve().parent.parent
if str(ATELIER_ROOT) not in sys.path:
    sys.path.insert(0, str(ATELIER_ROOT))

from app.config import blog_framework_dir_name, framework_root  # noqa: E402

SCAN_ROOTS = ("Front-end", "Back-end", "Full-stack", "Tooling")
SKIP_FILENAMES = frozenset({"README.md", "AGENTS.md", "CHANGELOG.md", "LICENSE.md"})


def _is_stack_guide(name: str) -> bool:
    if name in SKIP_FILENAMES:
        return False
    if not name.endswith(".md"):
        return False
    stem = name[:-3]
    if "-" not in stem or not stem[0].isupper():
        return False
    return bool(re.match(r"^[A-Z][A-Za-z0-9-]+$", stem))


GITHUB_BASE = "https://github.com/zhk0567/Framework/tree/main"

sys.path.insert(0, str(ATELIER_ROOT / "scripts"))
from guide_lib import MANIFEST_PATH  # noqa: E402

PILOT_SLUGS = frozenset({
    "fastapi-python",
    "nestjs-node-typescript",
    "react-vite-typescript",
    "nextjs-fullstack-typescript",
    "nx-tooling-typescript",
})


def _slug_from_path(rel: Path) -> str:
    base = rel.stem.lower().replace("_", "-")
    return base


def _parse_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _stack_name_from_filename(stem: str) -> str:
    parts = stem.split("-")
    if len(parts) >= 2 and parts[-1] in {
        "Python", "TypeScript", "Java", "Kotlin", "Go", "Rust", "Ruby", "PHP",
        "DotNet", "Dart", "Clojure", "Scala", "Elixir", "Deno", "Mobile", "Web",
    }:
        return parts[0].title() if parts[0].isupper() else parts[0]
    return stem.split("-")[0].title()


def scan(framework_root: Path) -> list[dict]:
    posts: list[dict] = []
    slug_seen: dict[str, str] = {}

    for root_name in SCAN_ROOTS:
        layer_dir = framework_root / root_name
        if not layer_dir.is_dir():
            continue
        skip_parts = {"node_modules", ".git", "dist", "build", ".venv", "_tmp-mikro"}
        for path in sorted(layer_dir.rglob("*.md")):
            if any(part in skip_parts for part in path.parts):
                continue
            if path.name == "README.md" or path.name.lower() == "readme.md":
                continue
            if not _is_stack_guide(path.name):
                continue
            rel = path.relative_to(framework_root)
            rel_posix = rel.as_posix()
            slug = _slug_from_path(rel)
            if slug in slug_seen:
                parent = path.parent.name.lower()
                slug = f"{parent}-{slug}"
            if slug in slug_seen:
                raise SystemExit(f"Slug conflict: {slug} for {rel_posix} and {slug_seen[slug]}")
            slug_seen[slug] = rel_posix

            repo_path = path.parent.relative_to(framework_root).as_posix()
            text = path.read_text(encoding="utf-8")
            stack = _stack_name_from_filename(path.stem)
            title = f"{stack} 学习笔记"

            posts.append({
                "slug": slug,
                "title": title,
                "series": "framework",
                "category": root_name,
                "stack": stack,
                "repo_path": repo_path,
                "source_rel": rel_posix,
                "github": f"{GITHUB_BASE}/{repo_path}",
                "folder": f"{blog_framework_dir_name()}/{slug}",
                "status": "draft",
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
        elif p["slug"] in PILOT_SLUGS:
            pass  # keep draft until index exists


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan Framework stack guides into manifest.json")
    parser.add_argument(
        "--framework-root",
        type=Path,
        default=framework_root(),
    )
    parser.add_argument("--out", type=Path, default=MANIFEST_PATH)
    args = parser.parse_args()

    posts = scan(args.framework_root)
    merge_existing_status(posts, args.out)

    payload = {
        "series": "framework",
        "github_repo": "https://github.com/zhk0567/Framework",
        "scanned_at": date.today().isoformat(),
        "count": len(posts),
        "posts": posts,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(posts)} posts to {args.out}")


if __name__ == "__main__":
    main()
