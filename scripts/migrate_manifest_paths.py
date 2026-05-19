# -*- coding: utf-8 -*-
"""One-time: slim manifest (drop source_abs), fix folder paths, optional framework_root."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import blog_framework_dir_name, framework_manifest_path  # noqa: E402

DIR_NAME = blog_framework_dir_name()


def main() -> None:
    path = framework_manifest_path()
    data = json.loads(path.read_text(encoding="utf-8"))
    data.pop("framework_root", None)
    data.pop("source_abs", None)
    for entry in data.get("posts", []):
        entry.pop("source_abs", None)
        slug = entry.get("slug", "")
        entry["folder"] = f"{DIR_NAME}/{slug}"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {path} ({len(data.get('posts', []))} posts, folder={DIR_NAME}/{{slug}})")


if __name__ == "__main__":
    main()
