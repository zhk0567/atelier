# -*- coding: utf-8 -*-
"""One-off: replace #### with **bold** inside ## 基础篇 only."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Blog" / "algorithm-guides"


def fix(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(r"^##\s+基础篇\s*$(.*?)(?=^##\s+|\Z)", re.M | re.S)
    m = pat.search(text)
    if not m:
        return False
    ess = m.group(0)
    new_ess = re.sub(r"^####\s+(.+)$", r"**\1**", ess, flags=re.M)
    if new_ess == ess:
        return False
    path.write_text(text[: m.start()] + new_ess + text[m.end() :], encoding="utf-8")
    return True


def main() -> None:
    slugs = sys.argv[1:] or ["algo-dp-linear", "ds-tree-segment-tree", "iv-top-frequent"]
    for slug in slugs:
        p = ROOT / slug / "index.md"
        print(slug, fix(p))


if __name__ == "__main__":
    main()
