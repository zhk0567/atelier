"""
Apply a Minecraft skin to MC_Vtuber Live2D textures.

Usage:
  python scripts/apply_minecraft_skin.py --username zhk0567
  python scripts/apply_minecraft_skin.py --skin path/to/skin.png

Writes MC_Vtuber/MC_Vtuber.2048/texture_00.png (2048x2048, nearest upscale)
and regenerates ico_MC_Vtuber.png via gen_mc_vtuber_fallback_avatar.py.
"""

from __future__ import annotations

import argparse
import base64
import json
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TEXTURE_OUT = ROOT / "MC_Vtuber" / "MC_Vtuber.2048" / "texture_00.png"
GEN_AVATAR = ROOT / "scripts" / "gen_mc_vtuber_fallback_avatar.py"
UA = "atelier-mc-skin/1.0 (personal site; contact via GitHub zhk0567)"


def _fetch(url: str) -> bytes:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            return resp.read()
    except urllib.error.URLError:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            return resp.read()


def download_skin_by_username(username: str) -> bytes:
    username = username.strip()
    prof_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        prof = json.loads(_fetch(prof_url).decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise SystemExit(
                f"Mojang 上找不到玩家 {username!r}（404）。"
                "请用 --skin 指定本地皮肤 PNG，或换正确的游戏 ID。"
            ) from e
        raise
    raw_id = prof["id"]
    uid = (
        f"{raw_id[:8]}-{raw_id[8:12]}-{raw_id[12:16]}"
        f"-{raw_id[16:20]}-{raw_id[20:]}"
    )
    session_url = (
        f"https://sessionserver.mojang.com/session/minecraft/profile/{uid}"
    )
    session = json.loads(_fetch(session_url).decode("utf-8"))
    for prop in session.get("properties", []):
        if prop.get("name") != "textures":
            continue
        payload = json.loads(base64.b64decode(prop["value"]))
        skin = payload.get("textures", {}).get("SKIN", {})
        url = skin.get("url")
        if not url:
            break
        return _fetch(url)
    raise SystemExit(f"no SKIN URL in Mojang profile for {username!r}")


def upscale_to_2048(img: Image.Image) -> Image.Image:
    img = img.convert("RGBA")
    w, h = img.size
    if w <= 0 or h <= 0:
        raise SystemExit(f"invalid skin size {w}x{h}")
    # 配布说明：标准 MC 皮肤整图放大到 2048×2048（最近邻，保持像素感）
    if w == h:
        return img.resize((2048, 2048), Image.NEAREST)
    target_w = 2048
    scale = max(1, target_w // w)
    target_h = h * scale
    up = img.resize((target_w, target_h), Image.NEAREST)
    if target_h == 2048:
        return up
    canvas = Image.new("RGBA", (2048, 2048), (0, 0, 0, 0))
    canvas.paste(up, (0, 0))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply MC skin to MC_Vtuber texture_00")
    parser.add_argument("--username", help="Mojang account name (e.g. zhk0567)")
    parser.add_argument("--skin", type=Path, help="Local skin PNG (64x64 or 64x32)")
    args = parser.parse_args()
    if not args.username and not args.skin:
        parser.error("provide --username or --skin")
    if args.username and args.skin:
        parser.error("use only one of --username or --skin")

    if args.skin:
        if not args.skin.is_file():
            raise SystemExit(f"missing {args.skin}")
        raw = args.skin.read_bytes()
        source = str(args.skin)
    else:
        raw = download_skin_by_username(args.username)
        source = f"Mojang:{args.username}"

    img = Image.open(BytesIO(raw))
    out = upscale_to_2048(img)
    TEXTURE_OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(TEXTURE_OUT, optimize=True)
    print(f"[ok] texture_00.png <= {source} ({img.size[0]}x{img.size[1]} -> 2048x2048)")

    if GEN_AVATAR.is_file():
        subprocess.run([sys.executable, str(GEN_AVATAR)], check=True)


if __name__ == "__main__":
    main()
