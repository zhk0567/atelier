"""Generate official-guide skeleton (headings + placeholders) for Framework slugs."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from guide_lib import (  # noqa: E402
    BLOG_FRAMEWORK,
    MANIFEST_PATH,
    PILOT_SLUGS,
    assign_guide_toc_id,
    blog_title,
    load_toc,
)

PLACEHOLDER = "（待撰写：按写作规范补充概念说明、完整代码示例、TIP 与 Framework 对照段落。）"


def _read_source(entry: dict) -> str:
    path = Path(entry.get("source_abs", ""))
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


def _extract_intro_from_source(source: str, stack: str) -> str:
    lines = source.splitlines()
    buf: list[str] = []
    in_intro = False
    for line in lines:
        if line.startswith("## 框架简介") or line.startswith("## 工具简介"):
            in_intro = True
            continue
        if in_intro:
            if line.startswith("## "):
                break
            if line.strip():
                buf.append(line)
    if buf:
        return "\n".join(buf)
    return f"**{stack}** 是本教程的主题。请在此补充：它解决什么问题、与相近技术相比的核心差异。"


def build_skeleton(entry: dict, toc: dict, source: str) -> str:
    stack = entry.get("stack", "Framework")
    slug = entry["slug"]
    repo_path = entry.get("repo_path", "")
    github = entry.get("github", "")
    title = blog_title(stack)
    essentials = toc.get("essentials", [])

    toc_lines = [
        "- [导读](#导读)",
        "- [预备知识](#预备知识)",
        "- [快速上手](#快速上手)",
        "- [基础篇](#基础篇)",
    ]
    for ch in essentials:
        cid = ch.get("id", "")
        t = ch.get("title", "")
        toc_lines.append(f"  - [{t}](#基础篇-{cid})")
    toc_lines.extend([
        "- [Framework 子工程实战](#framework-子工程实战)",
        "- [学习路径](#学习路径)",
        "- [延伸阅读](#延伸阅读)",
    ])

    parts = [
        f"""---
title: "{title}"
series: framework
category: {entry.get("category", "")}
stack: {stack}
language: {entry.get("language", "")}
repo_path: {repo_path}
source: {entry.get("source_rel", "")}
github: {github}
guide_toc: {toc.get("id", entry.get("guide_toc", ""))}
guide_tier: {toc.get("tier", "medium")}
status: draft
date: {date.today().isoformat()}
tags: [{stack}]
---

# {title}

## 目录

{chr(10).join(toc_lines)}

## 导读

{_extract_intro_from_source(source, stack)}

下面是一个最小示例（请替换为可运行代码）：

```python
# TODO: minimal hello example for {stack}
```

## 预备知识

> **预备知识**：请列出语言版本、Node/Python 版本、HTTP 基础等。

## 快速上手

```powershell
Set-Location -LiteralPath 'F:\\Study\\Framework\\{repo_path.replace("/", "\\\\")}'
# TODO: install and run commands from stack guide
```

## 基础篇

以下章节与官方教程目录对齐。{PLACEHOLDER}

""",
    ]

    for ch in essentials:
        cid = ch.get("id", "")
        t = ch.get("title", "")
        off = ch.get("official_slug", "")
        off_link = ""
        if off and toc.get("official"):
            base = toc["official"].rstrip("/")
            off_link = f"\n\n官方章节：<{base}/{off}/>" if "fastapi" in toc.get("id", "") else ""
        parts.append(f"""### {t}

{PLACEHOLDER}

**Framework 对照**：本仓 `{repo_path}` 中{PLACEHOLDER}{off_link}

""")

    parts.append(f"""## Framework 子工程实战

路径：`{repo_path}` · [GitHub]({github})

{PLACEHOLDER}

## 学习路径

- **初学者**：导读 → 快速上手 → 基础篇前半 → 子工程实战
- **有经验**：快速上手 → 子工程实战 → 按需查阅基础篇章节

## 延伸阅读

- [Framework 系列索引](/blog/series/framework)
- 官方文档：{toc.get("official") or "（请补充）"}
""")

    return "".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", action="append")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--skip-pilot", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    posts = data.get("posts", [])
    if args.slug:
        posts = [p for p in posts if p["slug"] in set(args.slug)]
    elif args.all:
        pass
    else:
        parser.error("Specify --all or --slug")

    if args.skip_pilot:
        posts = [p for p in posts if p["slug"] not in PILOT_SLUGS]

    n = 0
    for entry in posts:
        if entry["slug"] in PILOT_SLUGS and not args.force:
            continue
        out = BLOG_FRAMEWORK / entry["slug"] / "index.md"
        if out.is_file() and not args.force:
            continue
        toc_id = entry.get("guide_toc") or assign_guide_toc_id(entry)
        toc = load_toc(toc_id)
        source = _read_source(entry)
        content = build_skeleton(entry, toc, source)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        n += 1
        print(f"wrote skeleton {entry['slug']}")

    print(f"Generated {n} skeletons")


if __name__ == "__main__":
    main()
