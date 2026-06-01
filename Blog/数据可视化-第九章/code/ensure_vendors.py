"""Download ECharts assets into static/vendor/ if missing."""

from __future__ import annotations

import urllib.request
from pathlib import Path

VENDOR_DIR = Path(__file__).resolve().parents[3] / "static" / "vendor"

ASSETS: tuple[tuple[str, str], ...] = (
    (
        "echarts.min.js",
        "https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js",
    ),
    (
        "echarts-gl.min.js",
        "https://cdn.jsdelivr.net/npm/echarts-gl@2.0.9/dist/echarts-gl.min.js",
    ),
)


def _download(url: str, dest: Path) -> None:
    import ssl

    def fetch(ctx: ssl.SSLContext) -> bytes:
        with urllib.request.urlopen(url, context=ctx, timeout=120) as resp:
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
    VENDOR_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in ASSETS:
        dest = VENDOR_DIR / name
        if dest.is_file() and dest.stat().st_size > 10_000:
            continue
        print(f"[vendor] download {name} ...")
        _download(url, dest)
        print(f"[vendor] -> {dest}")


if __name__ == "__main__":
    main()
