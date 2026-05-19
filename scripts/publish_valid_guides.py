# -*- coding: utf-8 -*-
"""Run validate_guide + validate_guide_quality; publish passing slugs."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "Blog" / "Framework" / "manifest.json"
SCRIPTS = ROOT / "scripts"


def _run(cmd: list[str]) -> bool:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
    return r.returncode == 0


def main() -> None:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else None
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    posts = data["posts"]
    if slugs:
        posts = [p for p in posts if p["slug"] in slugs]
    ok_slugs: list[str] = []
    for p in posts:
        slug = p["slug"]
        if not _run(
            [sys.executable, str(SCRIPTS / "validate_guide.py"), "--slug", slug, "--strict"]
        ):
            print(f"SKIP {slug}: validate_guide failed")
            continue
        if not _run(
            [
                sys.executable,
                str(SCRIPTS / "validate_guide_quality.py"),
                "--slug",
                slug,
                "--strict",
            ]
        ):
            print(f"SKIP {slug}: validate_guide_quality failed")
            continue
        p["status"] = "published"
        ok_slugs.append(slug)
        print(f"PUBLISH {slug}")
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Published {len(ok_slugs)} / {len(posts)}")


if __name__ == "__main__":
    main()
