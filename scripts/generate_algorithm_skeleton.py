# -*- coding: utf-8 -*-
"""Generate empty Algorithm guide skeleton (headings only)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from algorithm_guide_lib import BLOG_ALGORITHM, MANIFEST_PATH, load_toc  # noqa: E402


def skeleton(entry: dict) -> str:
    toc = load_toc(entry.get("guide_toc", "topic-algorithm"))
    tier = entry.get("guide_tier") or toc.get("tier", "medium")
    ess_lines = "\n".join(f"  - [{ch['title']}](#{ch['title'].replace(' ', '-')})" for ch in toc.get("essentials", []))
    ess_body = "\n\n".join(f"### {ch['title']}\n\n（待撰写）\n" for ch in toc.get("essentials", []))
    return f"""---
title: "{entry.get('title', entry['slug'])}"
series: algorithm
category: {entry.get('category', '')}
topic_path: {entry.get('topic_path', '')}
guide_toc: {entry.get('guide_toc', '')}
guide_tier: {tier}
status: draft
date: {date.today().isoformat()}
tags: [Algorithm]
---

# {entry.get('title', entry['slug'])}

## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [Study 仓库对照](#study-仓库对照)
- [基础篇](#基础篇)
{ess_lines}
- [Python 实现](#python-实现)
- [C++ 实现](#c-实现)
- [练习与延伸](#练习与延伸)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)

## 导读

（待撰写）

## 预备知识

> **预备知识**：（待撰写）

## Study 仓库对照

（待撰写）

## 基础篇

{ess_body}

## Python 实现

（待撰写）

## C++ 实现

（待撰写）

## 练习与延伸

（待撰写）

## 学习路径

（待撰写）

## 延伸阅读

（待撰写）
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", action="append", required=True)
    args = parser.parse_args()

    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    by_slug = {p["slug"]: p for p in data.get("posts", [])}
    for slug in args.slug:
        entry = by_slug.get(slug)
        if not entry:
            print(f"Skip unknown slug: {slug}")
            continue
        out_dir = BLOG_ALGORITHM / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / "index.md"
        path.write_text(skeleton(entry), encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
