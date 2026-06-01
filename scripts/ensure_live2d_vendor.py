"""Download Live2D Web runtime into static/vendor/live2d/ (run once)."""

from __future__ import annotations

import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "static" / "vendor" / "live2d"

ASSETS = (
    (
        "live2dcubismcore.min.js",
        "https://cubism.live2d.com/sdk-web/cubismcore/live2dcubismcore.min.js",
    ),
    (
        "pixi.min.js",
        "https://cdn.jsdelivr.net/npm/pixi.js@6.5.10/dist/browser/pixi.min.js",
    ),
    (
        "unsafe-eval.min.js",
        "https://cdn.jsdelivr.net/npm/@pixi/unsafe-eval@6.5.10/dist/browser/unsafe-eval.min.js",
    ),
    (
        "cubism4.min.js",
        "https://cdn.jsdelivr.net/npm/pixi-live2d-display@0.4.0/dist/cubism4.min.js",
    ),
)


def _download(url: str, dest: Path) -> None:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def fetch(ctx: ssl.SSLContext) -> bytes:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
            return resp.read()

    ctx = ssl.create_default_context()
    try:
        data = fetch(ctx)
    except urllib.error.URLError:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        data = fetch(ctx)
    dest.write_bytes(data)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, url in ASSETS:
        dest = OUT / name
        if dest.is_file() and dest.stat().st_size > 1000:
            print(f"[skip] {name}")
            continue
        print(f"[get] {name}")
        _download(url, dest)
        print(f"  -> {dest}")


if __name__ == "__main__":
    main()
