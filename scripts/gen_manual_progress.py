# -*- coding: utf-8 -*-
"""Regenerate Blog/framework-guides/_meta/人工撰写进度.md from manifest + manual_wave_map."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from app.config import framework_manifest_path  # noqa: E402

MANIFEST = framework_manifest_path()
OUT = MANIFEST.parent / "_meta" / "人工撰写进度.md"
from manual_wave_map import WAVE_SLUGS, slug_wave  # noqa: E402


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    lines = [
        "# Framework 人工撰写进度",
        "",
        f"更新：精写阶段；**网页已发布 {len(data['posts'])} 篇**（manifest 中 status=published 的条目）。",
        "",
        "| slug | 波次 | 撰写状态 | manifest | 备注 |",
        "|------|-----:|----------|----------|------|",
    ]
    for p in sorted(data["posts"], key=lambda x: (slug_wave(x["slug"]) or 99, x["slug"])):
        slug = p["slug"]
        w = slug_wave(slug)
        wtxt = str(w) if w is not None else "?"
        st = p.get("status", "draft")
        note = "波次0标杆" if slug == "beego-go" else ""
        write_st = "已发布" if st == "published" else ("待验收" if slug != "beego-go" else "待验收(标杆)")
        lines.append(f"| {slug} | {wtxt} | {write_st} | {st} | {note} |")
    lines.extend(
        [
            "",
            "验收（每波）：",
            "",
            "```powershell",
            "Set-Location 'f:\\commercial\\atelier'",
            "python scripts/validate_guide.py --slug <slug> --strict",
            "python scripts/validate_guide_quality.py --slug <slug> --strict",
            "```",
            "",
            "精写稿已去除模板灌水句；manifest `status: published` 后站点 `/blog/series/framework` 可见。",
            "",
        ]
    )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
