"""Regenerate MC_Vtuber icons from texture_00.png (replaces bread placeholder ico)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TEXTURE = ROOT / "MC_Vtuber" / "MC_Vtuber.2048" / "texture_00.png"
OUT_AVATAR = ROOT / "MC_Vtuber" / "fallback_avatar.png"
OUT_ICO = ROOT / "MC_Vtuber" / "ico_MC_Vtuber.png"


def main() -> None:
    if not TEXTURE.is_file():
        raise SystemExit(f"missing {TEXTURE}")
    src = Image.open(TEXTURE).convert("RGBA")
    # 64x64 skin layout on 2048 atlas -> scale 32; head front UV (8,8)+8x8
    scale = src.width // 64
    x0, y0 = 8 * scale, 8 * scale
    side = 8 * scale
    face = src.crop((x0, y0, x0 + side, y0 + side)).resize((128, 128), Image.NEAREST)
    face.save(OUT_AVATAR, optimize=True)
    face.save(OUT_ICO, optimize=True)
    print("wrote", OUT_AVATAR)
    print("wrote", OUT_ICO)


if __name__ == "__main__":
    main()
