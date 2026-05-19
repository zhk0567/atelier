"""Export Framework subproject file tree and key sources for blog writing (read-only)."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import sys

ATELIER_ROOT = Path(__file__).resolve().parent.parent
if str(ATELIER_ROOT) not in sys.path:
    sys.path.insert(0, str(ATELIER_ROOT))

sys.path.insert(0, str(ATELIER_ROOT / "scripts"))
from guide_lib import BLOG_FRAMEWORK, MANIFEST_PATH  # noqa: E402

from app.config import framework_root  # noqa: E402

OUT_ROOT = BLOG_FRAMEWORK / "_meta" / "sources"

SKIP_DIRS = frozenset({
    "node_modules",
    ".git",
    "dist",
    "build",
    ".next",
    "__pycache__",
    ".venv",
    "venv",
})

KEY_GLOBS = (
    "main.py",
    "app.py",
    "main.ts",
    "main.go",
    "requirements.txt",
    "package.json",
    "package-lock.json",
    "public/index.html",
    "index.html",
    "vite.config.ts",
    "next.config.ts",
    "tsconfig.json",
    ".gitignore",
    "app/page.tsx",
    "app/layout.tsx",
    "app/**/route.ts",
    "src/main.ts",
    "src/server.ts",
    "*.md",
)


def _tree_lines(root: Path, prefix: str = "") -> list[str]:
    lines: list[str] = []
    try:
        entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except OSError:
        return lines
    for i, child in enumerate(entries):
        if child.name in SKIP_DIRS:
            continue
        connector = "└── " if i == len(entries) - 1 else "├── "
        lines.append(f"{prefix}{connector}{child.name}{'/' if child.is_dir() else ''}")
        if child.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            lines.extend(_tree_lines(child, prefix + extension))
    return lines


def _collect_key_files(repo: Path) -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()
    for pattern in KEY_GLOBS:
        for p in repo.glob(pattern):
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            if p.is_file() and p not in seen:
                seen.add(p)
                found.append(p)
    return sorted(found, key=lambda p: str(p).lower())


def extract_one(entry: dict, framework_root: Path, *, force: bool) -> None:
    slug = entry["slug"]
    repo_path = entry.get("repo_path", "")
    repo = framework_root / repo_path.replace("/", "\\") if repo_path else framework_root
    out_dir = OUT_ROOT / slug
    if out_dir.exists() and not force:
        print(f"skip (exists): {out_dir}")
        return
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "slug": slug,
        "repo_path": repo_path,
        "repo_abs": str(repo),
        "exists": repo.is_dir(),
    }
    (out_dir / "_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if not repo.is_dir():
        print(f"missing repo: {repo}")
        return

    tree_text = f"{repo_path}/\n" + "\n".join(_tree_lines(repo))
    (out_dir / "TREE.txt").write_text(tree_text, encoding="utf-8")

    for src in _collect_key_files(repo):
        rel = src.relative_to(repo)
        dest = out_dir / "files" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    print(f"exported {slug} -> {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", action="append")
    parser.add_argument("--all-pilots", action="store_true")
    parser.add_argument("--framework-root", type=Path, default=framework_root())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    posts = manifest.get("posts", [])
    pilot_slugs = {
        "fastapi-python",
        "nestjs-node-typescript",
        "react-vite-typescript",
        "nextjs-fullstack-typescript",
        "nx-tooling-typescript",
    }
    if args.all_pilots:
        posts = [p for p in posts if p["slug"] in pilot_slugs]
    elif args.slug:
        wanted = set(args.slug)
        posts = [p for p in posts if p["slug"] in wanted]
    else:
        parser.error("Specify --slug or --all-pilots")

    for entry in posts:
        extract_one(entry, args.framework_root, force=args.force)


if __name__ == "__main__":
    main()
