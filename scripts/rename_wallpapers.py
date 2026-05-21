"""一次性将 data/ 下旧壁纸文件名规范为 wallpaper-NN-slug.ext（见 wallpapers.json）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

RENAMES = {
    "preview.mp4": "wallpaper-01-preview.mp4",
    "preview (1).mp4": "wallpaper-02-preview-alt.mp4",
    "【哲风壁纸】Minecraft-我的世界.mp4": "wallpaper-03-minecraft.mp4",
    "【哲风壁纸】云朵-像素风-光影.mp4": "wallpaper-04-cloud-pixel.mp4",
}


def main() -> int:
    manifest = DATA / "wallpapers.json"
    if not manifest.is_file():
        print("missing wallpapers.json", file=sys.stderr)
        return 1
    expected = {item["file"] for item in json.loads(manifest.read_text(encoding="utf-8"))["items"]}
    for old, new in RENAMES.items():
        src = DATA / old
        dst = DATA / new
        if dst.is_file():
            continue
        if not src.is_file():
            if new in {p.name for p in DATA.iterdir() if p.is_file()}:
                continue
            print(f"skip missing: {old}")
            continue
        src.rename(dst)
        print(f"{old} -> {new}")
    present = {p.name for p in DATA.iterdir() if p.is_file() and p.suffix.lower() in {".mp4", ".webm", ".mov"}}
    missing = expected - present
    if missing:
        print("still missing:", ", ".join(sorted(missing)), file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
