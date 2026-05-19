"""
Download Minecraft Wiki decorative textures into static/img/wiki/.

Usage (from project root):
  pip install requests
  python scripts/fetch_wiki_textures.py
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests: pip install requests", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "static" / "img" / "wiki"
MANIFEST = OUT_DIR / "manifest.json"
USER_AGENT = "atelier-local/1.0 (personal wiki; texture fetch)"
TIMEOUT = 30


def download_url(url: str, dest: Path) -> bool:
    headers = {"User-Agent": USER_AGENT, "Accept": "image/*,*/*"}
    try:
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        if len(r.content) < 80:
            return False
        dest.write_bytes(r.content)
        return True
    except Exception as exc:
        print(f"  fail {url}: {exc}")
        return False


def main() -> int:
    if not MANIFEST.is_file():
        print(f"Missing manifest: {MANIFEST}", file=sys.stderr)
        return 1

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assets = data.get("assets", [])
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    ok, skip, fail = 0, 0, 0

    for entry in assets:
        filename = entry["file"]
        dest = OUT_DIR / filename

        copy_from = entry.get("copy_from")
        if copy_from:
            src = OUT_DIR / copy_from
            if src.is_file():
                shutil.copy2(src, dest)
                print(f"copy {filename} <- {copy_from}")
                ok += 1
            else:
                print(f"skip copy {filename}: missing {copy_from}")
                fail += 1
            continue

        if dest.is_file() and dest.stat().st_size > 80:
            print(f"skip {filename} (exists)")
            skip += 1
            continue

        urls = entry.get("urls", [])
        if not urls:
            print(f"no urls for {filename}")
            fail += 1
            continue

        saved = False
        for url in urls:
            print(f"try {filename} <- {url}")
            if download_url(url, dest):
                print(f"  ok {dest.stat().st_size} bytes")
                ok += 1
                saved = True
                break
        if not saved:
            fail += 1
            print(f"FAILED {filename}")

    print(f"\nDone: {ok} saved/copied, {skip} skipped, {fail} failed")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
