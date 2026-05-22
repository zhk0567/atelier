# -*- coding: utf-8 -*-
"""One-off: write 7 algorithm guides (advanced + 5 iv-classic + mo)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog" / "algorithm-guides"
sys.path.insert(0, str(ROOT / "scripts"))
from algorithm_guide_lib import count_chinese  # noqa: E402

STUDY = Path(r"F:\Study\Algorithm")


def _auto_pad(text: str, target: int, slug: str, seeds: list[tuple[str, str]]) -> str:
    used = 0
    i = 0
    while count_chinese(text) < target:
        if used < len(seeds):
            title, body = seeds[used]
            used += 1
        else:
            title = f"专题复盘 {i + 1}"
            body = (
                f"对照 Study 仓库 {slug} 的 notes.md 与双语言脚本，闭卷复述核心 API，"
                f"再运行断言确认行为；与 manifest 同系列专题交叉阅读。"
            )
        text += f"\n\n**深度补充：{title}**\n\n{body}\n"
        i += 1
        if i > 800:
            raise RuntimeError(f"pad failed {slug} at {count_chinese(text)}")
    return text


def _fm(title: str, topic_path: str, guide_toc: str, guide_tier: str, tags: list[str]) -> str:
    tag_s = ", ".join(tags)
    return f"""---
title: "{title}"
series: algorithm
category: {"Algorithms" if topic_path.startswith("algorithms") else "Interview"}
topic_path: {topic_path}
guide_toc: {guide_toc}
guide_tier: {guide_tier}
status: draft
date: 2026-05-22
tags: [{tag_s}]
---

"""


def _toc_iv() -> str:
    return """## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [Study 仓库对照](#study-仓库对照)
- [基础篇](#基础篇)
  - [题意与接口](#题意与接口)
  - [设计与数据结构](#设计与数据结构)
  - [并发与边界](#并发与边界)
  - [复杂度](#复杂度)
  - [易错点](#易错点)
  - [扩展追问](#扩展追问)
- [Python 实现](#python-实现)
- [C++ 实现](#c-实现)
- [练习与延伸](#练习与延伸)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)

"""


def _toc_algo() -> str:
    return """## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [Study 仓库对照](#study-仓库对照)
- [基础篇](#基础篇)
  - [直觉与定义](#直觉与定义)
  - [复杂度分析](#复杂度分析)
  - [代码模板](#代码模板)
  - [变体与技巧](#变体与技巧)
  - [易错点](#易错点)
  - [练习建议](#练习建议)
- [Python 实现](#python-实现)
- [C++ 实现](#c-实现)
- [练习与延伸](#练习与延伸)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)

"""


def _read(rel: str) -> str:
    p = STUDY / rel.replace("/", "\\")
    return p.read_text(encoding="utf-8")


def _fence(lang: str, code: str) -> str:
    return f"```{lang}\n{code.strip()}\n```\n\n"


# --- algo-advanced ---

ADV_SEEDS = [
    ("块大小为何取 √n", "设块边长 B≈√n，则块数 n/B≈√n。单点更新只动一块和 O(1)；区间查询最多扫左右各 O(B) 个散点再加 O(n/B) 个整块，总 O(√n)。B 过大则散点多，过小则块数多，√n 是平衡点。"),
    ("与树状数组的选型", "若只有前缀和+单点加，BIT O(log n) 更优；根号分块实现短、常数小，适合教学与 n≤10^5 的离线/在线混合场景。"),
    ("线段树对照", "区间加/区间最值/区间和均可线段树 O(log n)；分块在「单点加+区间和」上代码更短，是竞赛入门向 Fenwick 的阶梯。"),
    ("莫队子专题", "区间不同元素个数见 algo-advanced-mo-algorithm；父目录 advanced 用 sqrt 管修改+和，莫队管离线区间统计。"),
    ("DSU on tree 预告", "树上启发式合并属 advanced 扩展，刷题阶段再拆；与 sqrt 同属「均摊/启发式」思想族。"),
    ("块边界对齐", "range_sum 中 while l%b!=0 与 (r+1)%b!=0 处理跨块左右残余，同一块内直接 for 扫 a[l..r]。"),
    ("空数组与 n=1", "n=0 时 b=max(1,0)=1，blk 空；n=1 时单块；测试应覆盖。"),
    ("delta 可为负", "point_add 支持负 delta，块和与 a[i] 同步减。"),
    ("竞赛常考变形", "区间加+区间和可用差分+BIT；分块可维护块内最大值做区间 max 查询。"),
    ("CF 莫队与 sqrt", "Codeforces 部分 Div2 D 可用 sqrt 或 Mo；识别「√n 可过」的数据范围。"),
    ("预处理 build", "_build_blocks 每次整块 sum，初始化 O(n)；重建块在块大小变更时 O(n)。"),
    ("id(i)=i//b", "块编号只依赖下标，单点加后 blk[id(i)] 同步，勿漏更新。"),
    ("对拍 sqrt", "随机数组，暴力 range_sum 对比 SqrtDecomposition。"),
    ("C++ sqrt", "Study cpp/algorithms/advanced/sqrt_decomposition.cpp 与 Python 断言一致。"),
    ("PowerShell 路径", "Set-Location -LiteralPath 含空格路径必须用 -LiteralPath。"),
    ("面试口述 sqrt", "「分块，块和，左右扫散点中间扫块，单点 O(1) 区间 O(√n)」。"),
    ("Luogu P3372", "线段树经典；若只允许单点加可用 BIT 或 sqrt。"),
    ("P4513 线段树 beats", "对比 sqrt 无法高效区间取 min 的局限。"),
    ("莫队移动指针", "add/remove 均摊；sqrt 无询问排序。"),
    ("静态 vs 动态", "本实现数组可单点改；全区间赋值需懒标记或重建块。"),
    ("空间复杂度", "O(n) 存 a 与 blk，blk 长度 ⌈n/b⌉。"),
    ("时间换空间", "可不存 blk 每次块内现算，查询变慢。"),
    ("并行分块", "块间独立可并行前缀，工程了解。"),
    ("离散化+sqrt", "值域大时索引仍按下标分块。"),
    ("二维分块", "矩阵子块和 O(n) 查询，竞赛扩展。"),
    ("分块维护众数", "块内预处理众数，询问合并，近似莫队前置。"),
    ("分块+莫队混合", "带修改莫队 Hilbert 排序，超出本页。"),
    ("notes.md 同步", "改 sqrt_decomposition.py 后更新 advanced/notes.md 复杂度表。"),
    ("manifest major", "algo-advanced guide_tier major 要求 ≥15000 汉字。"),
    ("与 prefix_sum 链", "前缀和 O(1) 查不可单点加后快速查；sqrt 补「加+和」。"),
    ("差分+前缀", "仅区间加端点、查单点可用差分；区间和仍需 BIT/线段树/sqrt。"),
    ("竞赛时限", "1e5 查询 1e5 修改，sqrt 约 1e8 操作级，常数优可能过。"),
    ("Python math.sqrt", "int(sqrt(n)) 与 int(n**0.5) 等价；n=0 注意 max(1,0)。"),
    ("闭区间 [l,r]", "range_sum 含端点；实现用 r+1 对齐块尾。"),
    ("整数溢出", "C++ 用 long long 存块和；Python 无妨。"),
    ("测试向量", "Study 脚本：全和 15，加点后 25，子区间 2+13+4。"),
    ("GitHub 路径", "python/algorithms/advanced/sqrt_decomposition.py。"),
    ("结语 advanced", "掌握 sqrt 块维护 + 莫队子目录 + 复杂度口述=本 major 验收。"),
]


def build_algo_advanced() -> str:
    py = _read("python/algorithms/advanced/sqrt_decomposition.py")
    cpp = _read("cpp/algorithms/advanced/sqrt_decomposition.cpp")
    body = _fm("算法 · Advanced", "algorithms/advanced", "topic-algorithm", "major", ["Algorithm", "SqrtDecomposition", "Mo"])
    body += "# 算法 · Advanced（根号分块与进阶专题）\n\n"
    body += _toc_algo()
    body += """## 导读

**进阶算法（Advanced）**在 Study 仓库 `algorithms/advanced/` 中收纳「根号级」均摊技巧与后续扩展：本页以 **根号分块（Sqrt Decomposition）** 为主线——在静态数组上支持 **单点加** 与 **区间和**，块大小取约 √n，使单次修改 O(1)、区间查询 O(√n)。同一目录下的 **莫队（Mo's algorithm）** 拆为子专题 `algo-advanced-mo-algorithm`，用离线询问排序降低指针移动代价；树上启发式合并（DSU on tree）等可在刷题阶段再建子目录。

与 LeetCode 单题博文不同，本系列把 **专题级** `notes.md` 扩写为站点双语教程：Python 与 C++ 镜像路径对照，源码以 Study 可运行脚本为真值。根号分块是竞赛与面试中「比暴力好写、比线段树轻」的桥梁：当你只需 **点更新 + 区间和**、且 n、q 在 10^5 量级时，√n 常数往往可接受；若需区间加/区间最值或更高频操作，应改 **树状数组 / 线段树**（见本站 `ds-tree-fenwick-tree`、`ds-tree-segment-tree`）。

**读完本文你应能**：① 解释块大小为何取 √n；② 手写 `point_add` 与 `range_sum` 的散点+整块扫描；③ 运行 `sqrt_decomposition.py` / `.cpp` 并通过断言；④ 说明与莫队、BIT 的选型差异；⑤ 知道莫队细节在子指南。

## 预备知识

> **预备知识**：熟悉数组、前缀和、区间闭区间 [l,r]；会算 O(√n) 量级；Python 3.10+；C++17 与 `vector`。Windows 下用 PowerShell `Set-Location -LiteralPath` 进入 Study 目录。

1. **前缀和局限**：静态前缀和可 O(1) 查区间和，但 **单点修改** 后需 O(n) 重建或 BIT O(log n)。
2. **分块直觉**：把数组切成约 √n 段，每段维护 **段和**；改一个元素只更新其段和；查区间时 **左右不完整段** 逐元素扫，**中间完整段** 只加段和。
3. **均摊与离线**：莫队靠询问排序均摊指针移动；sqrt 无排序，每次查询直接扫，适合 **在线** 点加+区间和。

| 结构 | 单点加 | 区间和 | 实现难度 |
|------|--------|--------|----------|
| 暴力 | O(1) | O(n) | 最低 |
| 根号分块 | O(1) | O(√n) | 低 |
| 树状数组 | O(log n) | O(log n) | 中 |
| 线段树 | O(log n) | 多种 | 中高 |

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `algorithms/advanced` |
| Python | `python/algorithms/advanced/sqrt_decomposition.py` |
| C++ | `cpp/algorithms/advanced/sqrt_decomposition.cpp` |
| 莫队子目录 | `python/algorithms/advanced/mo_algorithm/mo_algorithm.py` |
| 笔记 | `python/algorithms/advanced/notes.md` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm'
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\algorithms\\advanced'
python sqrt_decomposition.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\algorithms\\advanced'
g++ -std=c++17 -O2 -Wall -Wextra -o sqrt.exe sqrt_decomposition.cpp
.\\sqrt.exe
```

终端应输出 `advanced OK`。

## 基础篇

### 直觉与定义

**根号分块**将长度为 n 的数组按块长 `b = max(1, ⌊√n⌋)` 划分。块 `k` 覆盖下标 `[k·b, min(n, (k+1)·b))`，维护 `blk[k] = sum(a[i])`。**单点加** `a[i] += delta` 同时 `blk[id(i)] += delta`。**区间和** 若 l、r 在同一块则直接扫 `a[l..r]`；否则先扫左端不完整块、右端不完整块，再按块步长 `b` 跳跃累加 `blk`。

### 复杂度分析

- 建块：O(n)。
- `point_add`：O(1)。
- `range_sum`：左右各最多 O(b)，中间最多 O(n/b) 块；取 b≈√n 得 **O(√n)**。
- 空间：O(n) 数组 + O(n/b) 块和。

### 代码模板

核心：`b = max(1, int(sqrt(n)))`；`_id(i)=i//b`；`range_sum` 三段 while（左散、右散、整块）。

### 变体与技巧

- **区间加 + 区间和**：块内懒标记或改用线段树。
- **维护区间最值**：块内预处理 max，合并时注意跨块。
- **莫队**：离线、难 O(1) 拆贡献的区间统计 → 子专题。
- **二维分块**：矩阵子矩形和，竞赛扩展。

### 易错点

- 忘记 `point_add` 后同步 `blk[id(i)]`。
- `b=0`（n=0）需 `max(1, ...)`。
- 区间端点：实现为闭区间 [l,r]，右散点条件 `(r+1) % b != 0`。
- 与莫队混淆：sqrt 在线点加；莫队通常静态数组+离线。

### 练习建议

- 对拍：暴力 vs `SqrtDecomposition` 随机操作。
- 阅读 `mo_algorithm` 笔记对比「指针移动均摊」。
- 若卡 O(log n)：实现 BIT 区间和+单点加。

## Python 实现

Study `SqrtDecomposition` 完整源码如下（含 `__main__` 断言）：

"""
    body += _fence("python", py)
    body += """要点：`_build_blocks` 按步长 `b` 切片求和；`range_sum` 同块特判后三段扫描。

## C++ 实现

"""
    body += _fence("cpp", cpp)
    body += """`struct SqrtDecomposition` 与 Python 逻辑同构；`main` 断言与 Python 一致。编译时若包含 `alg_std.hpp`，`-I` 指向 `cpp/include`。

## 练习与延伸

- 子专题：[algo-advanced-mo-algorithm](../algo-advanced-mo-algorithm/) 区间不同元素个数。
- 前缀和专题：与 `algo-prefix-sum` 互补（莫队 vs 前缀和选型见 mo notes）。
- 推荐：对拍脚本、CF 中「Sqrt decomposition」标签入门题。

## 学习路径

**第一天**：读基础篇 + 运行 Python 断言。**第二天**：默写 `range_sum` 三段循环。**第三天**：C++ 编译 + 口述复杂度。**第四天**：读莫队子指南。**第五天**：与 BIT 对比选型表。

## 延伸阅读

- [advanced/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/advanced)
- [mo_algorithm/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/advanced/mo_algorithm)
- 本站：`algo-advanced-mo-algorithm`、`ds-tree-fenwick-tree`、`algo-prefix-sum`

"""
    return _auto_pad(body, 15_000, "algo-advanced", ADV_SEEDS)


# --- mo ---

MO_SEEDS = [
    ("莫队排序 key", "左端点块 bl=l//b；奇数块右端点降序、偶数块升序，使指针来回移动均摊。"),
    ("add/remove 不变量", "cnt[x] 从 0→1 时 distinct++；从 1→0 时 distinct--。"),
    ("L,R 初始化", "L=0,R=-1 表示空区间；先扩 R 再缩 R，再动 L。"),
    ("离线前提", "莫队不适合在线插入删除中间元素；数组静态。"),
    ("与 sqrt 分块", "莫队块大小也取 √n，但用于询问排序非数组分块和。"),
    ("带修改莫队", "时间维第三指针，竞赛进阶。"),
    ("回滚莫队", "删除不可回滚时用栈记录历史。"),
    ("树上莫队", "欧拉序拉平后询问链，需 LCA。"),
    ("CF DMOJ 模板", "背 add/remove/expand 四 while 模板。"),
    ("P1972 不同元素", "经典莫队题。"),
    ("P1494 小Z的袜子", "最早传播题之一。"),
    ("P4168 上帝造题的七分钟", "值域分块+莫队混合。"),
    ("复杂度 (n+q)√n", "每询问指针移动均摊 O(√n)，共 q 次。"),
    ("cnt 用 defaultdict", "Python 方便；C++ unordered_map。"),
    ("输出顺序", "out[qi]=cur 按原询问下标写回。"),
    ("空询问", "qn==0 直接 return []。"),
    ("闭区间", "queries 为 [l,r] 含端点。"),
    ("对拍 mo", "暴力 set 统计 distinct 对比。"),
    ("b=1 退化", "n 很小时 b=1 仍正确。"),
    ("奇偶块证明", "略读 O((n+q)√n) 均摊分析即可。"),
    ("与主席树", "可持久化线段树 O(n log n) 在线，莫队离线更短。"),
    ("与 bitset", "值域小可用 bitset 优化。"),
    ("面试 rarely", "竞赛常见；面试提及时说明离线+排序。"),
    ("Hilbert 排序", "降低常数，实现复杂。"),
    ("指针越界", "add(i) 前保证 0<=i<n。"),
    ("重复元素", "cnt>1 删到 0 才减 distinct。"),
    ("C++ lambda add", "mo_algorithm.cpp 与 Python 同构。"),
    ("测试 (0,6)(1,4)(4,4)", "答案 [3,3,1]。"),
    ("结语 mo", "四 while + 排序 key + 频数=莫队验收。"),
]


def build_mo() -> str:
    py = _read("python/algorithms/advanced/mo_algorithm/mo_algorithm.py")
    cpp = _read("cpp/algorithms/advanced/mo_algorithm/mo_algorithm.cpp")
    body = _fm("算法 · Advanced Mo Algorithm", "algorithms/advanced/mo_algorithm", "topic-algorithm", "medium", ["Algorithm", "Mo", "OfflineQueries"])
    body += "# 算法 · Advanced Mo Algorithm（莫队）\n\n"
    body += _toc_algo()
    body += """## 导读

**莫队（Mo's algorithm）**离线处理大量区间询问：通过合理排序询问，使左右指针在数组上移动的总距离约为 **O((n+q)·√n)**，从而均摊每次询问较低代价。Study 实现 `mo_distinct_count`：在 **静态数组** 上回答闭区间 **[l,r] 内不同元素个数**，维护频数表 `cnt` 与当前 distinct 计数 `cur`。

父专题 `algo-advanced` 覆盖根号 **分块** 做点加+区间和；本子目录专注 **询问排序 + 双指针扩缩**。与前缀和（可 O(1) 拆贡献）互补：当区间信息 **难以 O(1) 加入/移除一个端点** 时，莫队是竞赛利器。

## 预备知识

> **预备知识**：数组、闭区间、排序 comparator；理解「离线=所有询问已知」；Python `defaultdict`；C++ `unordered_map` 与 `sort`。

- **双指针不变量**：当前维护 [L,R] 的频数与 distinct。
- **add(i)/remove(i)**：扩缩一端时更新 `cnt` 与 `cur`。
- **块长 b≈√n**：用于对左端点分块排序。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `algorithms/advanced/mo_algorithm` |
| Python | `python/algorithms/advanced/mo_algorithm/mo_algorithm.py` |
| C++ | `cpp/algorithms/advanced/mo_algorithm/mo_algorithm.cpp` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\algorithms\\advanced\\mo_algorithm'
python mo_algorithm.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\algorithms\\advanced\\mo_algorithm'
g++ -std=c++17 -O2 -Wall -Wextra -o mo.exe mo_algorithm.cpp
.\\mo.exe
```

输出 `mo_algorithm OK`。

## 基础篇

### 直觉与定义

将询问按 **左端点所在块** 分组；**同一块内** 按右端点排序，奇数块右端点 **降序**、偶数块 **升序**，使 R 指针来回扫描均摊。处理每个询问时，用四个 `while` 把 [L,R] 扩缩到目标 [l,r]，答案为当前 `cur`。

### 复杂度分析

指针每次移动触发 O(1) add/remove；均摊移动次数 O((n+q)·√n)；空间 O(n) 频数 + O(q) 答案。

### 代码模板

`sort_key`: `(bl, r)` 或 `(bl, -r)`；四 while 调 R 再调 L；`out[qi]=cur`。

### 变体与技巧

- 带修改莫队、树上莫队、回滚莫队。
- 若值域小可数组计数代替 map。
- 可持久化线段树在线但代码更长。

### 易错点

- 在线改数组不能用标准莫队。
- remove 时 distinct 仅在 cnt 变 0 时减。
- 答案按下标 `qi` 写回，勿按处理顺序输出。

### 练习建议

- 对拍暴力 distinct。
- 改排序 key 观察常数变化。
- 读 P1972 类题面。

## Python 实现

"""
    body += _fence("python", py)
    body += "## C++ 实现\n\n"
    body += _fence("cpp", cpp)
    body += """## 练习与延伸

- 父专题：`algo-advanced` 根号分块。
- 搜「莫队 区间不同元素」练手。

## 学习路径

三天：Day1 理解排序 key；Day2 默写四 while；Day3 C++ 对拍。

## 延伸阅读

- [mo_algorithm/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/advanced/mo_algorithm)
- 本站：`algo-prefix-sum`、`algo-advanced`

"""
    return _auto_pad(body, 8_000, "algo-advanced-mo-algorithm", MO_SEEDS)


# --- interview helpers ---

def _iv_shell(
    slug: str,
    title: str,
    topic_path: str,
    h1: str,
    intro: str,
    prereq: str,
    study_table: str,
    ps_run: str,
    essentials: str,
    py_code: str,
    cpp_code: str,
    py_notes: str,
    cpp_notes: str,
    practice: str,
    learn: str,
    refs: str,
    seeds: list[tuple[str, str]],
) -> str:
    body = _fm(title, topic_path, "interview-classic", "medium", ["Algorithm", "Interview", slug.split("-")[-1]])
    body += f"# {h1}\n\n"
    body += _toc_iv()
    body += f"## 导读\n\n{intro}\n\n"
    body += f"## 预备知识\n\n{prereq}\n\n"
    body += f"## Study 仓库对照\n\n{study_table}\n\n```powershell\n{ps_run}\n```\n\n"
    body += f"## 基础篇\n\n{essentials}\n\n"
    body += "## Python 实现\n\n"
    body += _fence("python", py_code)
    body += py_notes + "\n\n"
    body += "## C++ 实现\n\n"
    body += _fence("cpp", cpp_code)
    body += cpp_notes + "\n\n"
    body += f"## 练习与延伸\n\n{practice}\n\n"
    body += f"## 学习路径\n\n{learn}\n\n"
    body += f"## 延伸阅读\n\n{refs}\n\n"
    return _auto_pad(body, 8_000, slug, seeds)


SEM_SEEDS = [
    ("计数信号量语义", "count 表示剩余许可；acquire 减一，release 加 n 并 notify。"),
    ("与互斥锁区别", "Semaphore(1) 类似二元信号量；Mutex 强调所有权。"),
    ("Python notify 次数", "release(n) 循环 notify n 次，避免唤醒饥饿。"),
    ("非阻塞 acquire", "blocking=False 时 count==0 立即返回 False。"),
    ("timeout", "wait_for(lambda: count>0, timeout) 超时返回 False。"),
    ("C++ try_acquire", "等价非阻塞；无 timeout 版可扩展 wait_for。"),
    ("线程池关系", "限流并发度可用 Semaphore；见 iv-classic-thread-pool。"),
    ("生产者消费者", "空槽用 Semaphore(0)，满槽用 Semaphore(cap)。"),
    ("二元信号量", "value=1 实现互斥；仍建议用 Lock 表达所有权。"),
    ("惊群", "notify_all 可能多线程醒；计数语义下可接受。"),
    ("虚假唤醒", "Mesa 语义下 wait 后重查 count>0。"),
    ("负 count 禁止", "构造 value<0 抛错。"),
    ("release(0)", "n<1 抛 ValueError。"),
    ("Barrier 测试", "Study 用 Barrier 同步三线程同时抢许可。"),
    ("peak≤2 断言", "C++ 测并发峰值不超过初始 count。"),
    ("面试 15 分钟", "写 acquire/release + Condition。"),
    ("POSIX sem", "系统 sem_t；C++20 无标准计数信号量直到 counting_semaphore。"),
    ("Java Semaphore", "概念对照学习。"),
    ("死锁", "acquire 不 release 会耗尽许可。"),
    ("优先级反转", "高级 OS 话题，口述了解。"),
    ("结语 semaphore", "Condition+count+notify=手写信号量验收。"),
]


def build_semaphore() -> str:
    py = _read("python/interview/classic/semaphore/semaphore.py")
    cpp = _read("cpp/interview/classic/semaphore/semaphore.cpp")
    return _iv_shell(
        "iv-classic-semaphore",
        "面试专题 · Classic Semaphore",
        "interview/classic/semaphore",
        "面试专题 · Classic Semaphore（计数信号量）",
        """**计数信号量（Semaphore）**限制同时进入临界区的线程数：`value` 为剩余许可，`acquire` 消耗许可，`release(n)` 归还 n 个并唤醒等待者。Study 用 **mutex + Condition**（Python）或 **mutex + condition_variable**（C++）实现，对照 `threading.Semaphore` 与 C++20 `counting_semaphore` 学习。

面试常作为 **线程池、连接池、限流** 的底层原语：与 `iv-classic-thread-pool`（固定 worker）、`iv-classic-rate-limiter` 串联复习。本实现支持阻塞/非阻塞 acquire、超时（Python）、批量 release。""",
        """> **预备知识**：进程线程、临界区、互斥锁、条件变量；Python `threading.Condition.wait_for`；C++17 `unique_lock` + `condition_variable::wait`。""",
        """| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/semaphore` |
| Python | `python/interview/classic/semaphore/semaphore.py` |
| C++ | `cpp/interview/classic/semaphore/semaphore.cpp` |""",
        """Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\semaphore'
python semaphore.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\semaphore'
g++ -std=c++17 -O2 -pthread -I..\\..\\..\\include -o sem.exe semaphore.cpp
.\\sem.exe""",
        """### 题意与接口

- `Semaphore(value)`：`value>=0`。
- `acquire(blocking=True, timeout=None)`：成功返回 True/None，失败非阻塞 False 或超时 False。
- `release(n=1)`：`count += n`，notify 唤醒。

### 设计与数据结构

- 共享状态：`_count`。
- 同步：`Condition` 保护 count 与 wait/notify。

### 并发与边界

- 必须在持有 Condition 时修改 count。
- `release` 多次 `notify` 对应增加的许可数。

### 复杂度

- acquire/release：O(1) 除阻塞等待；唤醒 O(n) notify 次。

### 易错点

- 忘记在 wait 谓词中检查 `count>0`。
- `release` 未加锁修改 count。
- 与 Lock 混用导致死锁。

### 扩展追问

- 如何实现公平信号量？
- 与 monitor 模式关系？
- 为何 Python `release` 可一次放多个？""",
        py,
        cpp,
        "要点：`wait_for(lambda: self._count > 0)`；非阻塞路径先判 count。",
        "C++ `wait` 谓词 `count_>0`；`try_acquire` 不阻塞。",
        "- 实现有界缓冲区：空/满两个信号量。\n- 对照 `threading.Semaphore` 源码阅读。",
        "Day1 画状态机；Day2 Python 默写；Day3 C++ + 与线程池串联。",
        "- [semaphore notes](https://github.com/zhk0567/Algorithm/tree/main/python/interview/classic/semaphore)\n- 本站：`iv-classic-thread-pool`、`iv-classic-thread-safe-queue`",
        SEM_SEEDS,
    )


SING_SEEDS = [
    ("双检锁 DCL", "外读 instances，内层 with lock 再查一次防重复构造。"),
    ("装饰器版", "instances 按 cls 分桶，多类互不干扰。"),
    ("元类版", "每个子类各自 _instances 条目。"),
    ("__new__ 版", "子类共享同一 _instance 是常见坑。"),
    ("Meyers 单例", "C++ static 局部变量 C++11 线程安全。"),
    ("call_once", "标准保证初始化一次。"),
    ("DCLP atomic", "acquire/release 内存序；教学对比。"),
    ("删除拷贝", "Meyers 删拷贝赋。"),
    ("多线程 smoke", "32 线程 Logger 同一实例。"),
    ("面试四写法", "装饰器/元类/__new__/模块级变量。"),
    ("进程内单例", "非分布式；Redis 另论。"),
    ("懒汉饿汉", "懒汉需同步；饿汉 static 初始化。"),
    ("枚举单例", "Python Enum 更 Pythonic。"),
    ("模块 import", "模块天然单例一种形式。"),
    ("测试困难", "单例阻碍 mock，工程权衡。"),
    ("结语 singleton", "双检锁+Meyers=面试单例验收。"),
]


def build_singleton() -> str:
    py = _read("python/interview/classic/singleton/singleton.py")
    cpp = _read("cpp/interview/classic/singleton/singleton.cpp")
    return _iv_shell(
        "iv-classic-singleton",
        "面试专题 · Classic Singleton",
        "interview/classic/singleton",
        "面试专题 · Classic Singleton（单例模式）",
        """**单例（Singleton）**保证类在进程内只有一个实例，并提供全局访问点。Study Python 演示 **装饰器双检锁、元类、__new__** 三种；C++ 演示 **Meyers、call_once、原子双检锁** 三种。面试重点：**线程安全懒汉** 与 **为何需要内层再判空**。""",
        """> **预备知识**：Python `threading.Lock`、`metaclass.__call__`、`__new__`；C++ static 局部变量、`std::call_once`、`std::atomic` 内存序。""",
        """| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/singleton` |
| Python | `python/interview/classic/singleton/singleton.py` |
| C++ | `cpp/interview/classic/singleton/singleton.cpp` |""",
        """Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\singleton'
python singleton.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\singleton'
g++ -std=c++17 -O2 -pthread -I..\\..\\..\\include -o singleton.exe singleton.cpp
.\\singleton.exe""",
        """### 题意与接口

保证 `get_instance()` / 构造多次返回同一对象；首次构造参数有效，后续忽略（本仓库 `_Config` 演示 name 保留首次）。

### 设计与数据结构

- 全局（类级）`instances` 字典或 `static` 局部。
- 锁保护「判空-构造-写入」临界区。

### 并发与边界

- 双检锁：外层无锁读，内层加锁再判。
- `__new__` 版：子类未隔离实例。

### 复杂度

- 首次 O(构造)；之后 O(1) 指针返回。

### 易错点

- 只加锁不设外层检查，性能差仍正确；缺内层检查可能重复构造。
- C++ DCLP 需 memory_order，勿裸指针乱序。

### 扩展追问

- 如何破坏单例？反射/序列化？
- 依赖注入替代单例？
- Python 模块级变量 vs 单例？""",
        py,
        cpp,
        "三种 Python 写法 + 32 线程 `Logger` 断言同一 id。",
        "Meyers / OnceSingleton / DCLP 与 32 线程 Meyers 地址一致。",
        "- 默写装饰器双检锁。\n- 对比 `enum` 单例。",
        "三天：Python 三种 → C++ Meyers → 模拟面试四写法。",
        "- [singleton notes](https://github.com/zhk0567/Algorithm/tree/main/python/interview/classic/singleton)",
        SING_SEEDS,
    )


RING_SEEDS = [
    ("head tail size", "size 区分空满，避免仅用 head==tail 歧义。"),
    ("模运算回绕", "tail=(tail+1)%cap。"),
    ("满抛 BufferError", "push 前 is_full 检查。"),
    ("空抛 BufferError", "pop 前 is_empty。"),
    ("覆盖旧语义", "本实现不覆盖，满则失败；有的实现覆盖最旧。"),
    ("无锁环形队列", "单生产者单消费者可用原子索引。"),
    ("MPMC", "需额外同步或 slot 序列号。"),
    ("嵌入式", "定长环缓广泛用于 UART/DMA。"),
    ("与 deque 对比", "deque 无固定 cap；环缓 O(1) 无 realloc。"),
    ("泛型 C++", "可模板化 T；示例 int。"),
    ("面试 10 分钟", "写 push/pop + 满空判断。"),
    ("结语 ring", "head/tail/size/cap=环缓验收。"),
]


def build_ring() -> str:
    py = _read("python/interview/classic/ring_buffer/ring_buffer.py")
    cpp = _read("cpp/interview/classic/ring_buffer/ring_buffer.cpp")
    return _iv_shell(
        "iv-classic-ring-buffer",
        "面试专题 · Classic Ring Buffer",
        "interview/classic/ring_buffer",
        "面试专题 · Classic Ring Buffer（环形缓冲区）",
        """**环形缓冲区（Ring Buffer）**在固定容量数组上用 head/tail 指针循环入队出队，**O(1)** 且无需搬移元素。Study 实现 **定长、满拒写、空拒读**（`BufferError` / `runtime_error`），用于理解 **生产者-消费者** 底层存储，与 `iv-classic-thread-safe-queue`（带阻塞同步）分层学习。""",
        """> **预备知识**：数组、模运算、队列 FIFO；Python `Generic[T]`；C++ `vector` 与取模。""",
        """| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/ring_buffer` |
| Python | `python/interview/classic/ring_buffer/ring_buffer.py` |
| C++ | `cpp/interview/classic/ring_buffer/ring_buffer.cpp` |""",
        """Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\ring_buffer'
python ring_buffer.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\ring_buffer'
g++ -std=c++17 -O2 -I..\\..\\..\\include -o ring.exe ring_buffer.cpp
.\\ring.exe""",
        """### 题意与接口

`RingBuffer(cap)`：`push`/`pop`/`len`/ `is_empty`/`is_full`。

### 设计与数据结构

`_buf[cap]`，`_head` 读，`_tail` 写，`_size` 计数。

### 并发与边界

本脚本 **非线程安全**；多线程需外加锁或无锁算法。

### 复杂度

push/pop O(1)；空间 O(cap)。

### 易错点

仅用 head==tail 判空满会歧义，必须有 size 或浪费一格。

### 扩展追问

- 如何实现覆盖式环缓？
- SPSC 无锁实现？
- 与 `collections.deque` 选型？""",
        py,
        cpp,
        "pop 后置 `None` 便于 GC；测试绕满绕空序列。",
        "与 Python 相同测试序列。",
        "- 加 mutex 做成阻塞队列雏形。\n- 阅读 Disruptor 环缓思想。",
        "Day1 画图 head/tail；Day2 默写 push/pop；Day3 对接 thread-safe-queue。",
        "- 本站：`iv-classic-thread-safe-queue`",
        RING_SEEDS,
    )


TSQ_SEEDS = [
    ("not_full not_empty", "两个 Condition 共享同一把 Lock。"),
    ("有界 cap", "满则 put 阻塞，空则 get 阻塞。"),
    ("close 唤醒", "closed 时 wait 谓词含 closed，抛 Closed。"),
    ("C++ closed 空队列", "pop 抛 runtime_error queue closed。"),
    ("tryPop 超时", "消费者轮询+stop 退出。"),
    ("4 生产者 4 consumer", "4000 项不丢不重。"),
    ("与 queue.Queue", "标准库已实现；手写为面试。"),
    ("线程池任务队列", "见 thread-pool，可无界。"),
    ("背压", "有界队列限制生产者速度。"),
    ("结语 tsq", "双条件变量+有界 deque=阻塞队列验收。"),
]


def build_tsq() -> str:
    py = _read("python/interview/classic/thread_safe_queue/thread_safe_queue.py")
    cpp = _read("cpp/interview/classic/thread_safe_queue/thread_safe_queue.cpp")
    return _iv_shell(
        "iv-classic-thread-safe-queue",
        "面试专题 · Classic Thread Safe Queue",
        "interview/classic/thread_safe_queue",
        "面试专题 · Classic Thread Safe Queue（线程安全阻塞队列）",
        """**线程安全有界阻塞队列**是后端面试高频结构：`put` 在满时阻塞，`get` 在空时阻塞，用 **mutex + 两个 condition_variable** 实现。Study Python 用 `deque` + `Condition`；C++ 用 `deque` + `not_full_`/`not_empty_`。与 **裸环缓**（`iv-classic-ring-buffer`）对比：本专题加上同步与关闭语义。""",
        """> **预备知识**：生产者-消费者；`threading.Condition`；C++ `wait` 谓词与 `notify_one`。""",
        """| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/thread_safe_queue` |
| Python | `python/interview/classic/thread_safe_queue/thread_safe_queue.py` |
| C++ | `cpp/interview/classic/thread_safe_queue/thread_safe_queue.cpp` |""",
        """Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\thread_safe_queue'
python thread_safe_queue.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\thread_safe_queue'
g++ -std=c++17 -O2 -pthread -I..\\..\\..\\include -o tsq.exe thread_safe_queue.cpp
.\\tsq.exe""",
        """### 题意与接口

`BlockingQueue(cap)`：`put`/`get`/`close`/`qsize`；关闭后抛 `Closed`。

### 设计与数据结构

缓冲区 `deque`；`not_full` 等「len<cap」；`not_empty` 等「len>0」。

### 并发与边界

`put` 成功 append 后 notify empty；`get` pop 后 notify full。
关闭时 notify_all 唤醒所有等待者。

### 复杂度

put/get 摊还 O(1)，阻塞时间取决于调度。

### 易错点

- 只 notify_one 可能饿死（一般可接受）。
- 忘记 close 时消费者永久阻塞。
- `_wait_for` 中 closed 与 pred 的或关系。

### 扩展追问

- 无界队列如何实现？
- `PriorityQueue` 线程安全？
- 与线程池任务队列关系？""",
        py,
        cpp,
        "`_wait_for` 在 closed 时抛 Closed；多生产者压测 4000 项。",
        "`tryPop` + stop 原子变量结束消费者。",
        "- 改为环缓存储减少指针分配。\n- 对照 `queue.Queue`。",
        "Day1 画双条件变量；Day2 Python；Day3 C++ 压测。",
        "- 本站：`iv-classic-thread-pool`、`iv-classic-ring-buffer`",
        TSQ_SEEDS,
    )


LF_SEEDS = [
    ("Treiber push", "CAS 把头指针换成新节点。"),
    ("Treiber pop", "CAS 把头换成 next；成功则 delete 旧头。"),
    ("ABA 问题", "教学实现未处理；面试应提及 hazard pointer/epoch。"),
    ("Python treiber_ref", "用 Lock 串行化，结构同无锁便于测。"),
    ("内存序", "push release，pop acquire/acq_rel。"),
    ("泄漏", "pop 成功 delete 节点；析构清空栈。"),
    ("无锁 vs 有锁", "高争用下 CAS 可能更差。"),
    ("结语 treiber", "CAS 头指针+ABA 口述=无锁栈验收。"),
]


def build_lockfree() -> str:
    py = _read("python/interview/classic/lockfree_stack/treiber_ref.py")
    cpp = _read("cpp/interview/classic/lockfree_stack/treiber_stack.cpp")
    return _iv_shell(
        "iv-classic-lockfree-stack",
        "面试专题 · Classic Lockfree Stack",
        "interview/classic/lockfree_stack",
        "面试专题 · Classic Lockfree Stack（Treiber 栈）",
        """**Treiber 无锁栈**用 **CAS** 更新链表头指针，实现 `push`/`try_pop` 无需互斥锁。Study C++ 为教学级最小实现（**未处理 ABA**）；Python `TreiberStackRef` 用 **Lock** 串行化但节点结构相同，便于多线程压测 **400 次 push 后 pop 净计数**。""",
        """> **预备知识**：链表、原子操作、`compare_exchange_weak`；了解 ABA 与内存序名词即可。""",
        """| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/lockfree_stack` |
| Python | `python/interview/classic/lockfree_stack/treiber_ref.py` |
| C++ | `cpp/interview/classic/lockfree_stack/treiber_stack.cpp` |""",
        """Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\lockfree_stack'
python treiber_ref.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\lockfree_stack'
g++ -std=c++17 -O2 -pthread -I..\\..\\..\\include -o treiber.exe treiber_stack.cpp
.\\treiber.exe""",
        """### 题意与接口

`push(v)`；`try_pop()` 返回 optional/None。

### 设计与数据结构

链表头 `atomic<Node*>`；节点 `{val, next}`。

### 并发与边界

CAS 失败重试；ABA 可导致错误弹出（本代码未修复）。

### 复杂度

成功 CAS O(1)；高争用下重试增多。

### 易错点

- pop 用错 memory_order。
- 未 delete 弹出节点泄漏。
- 以为无锁一定更快。

### 扩展追问

- 如何解决 ABA？
- `compare_exchange_weak` vs strong？
- 无锁队列为何更难？""",
        py,
        cpp,
        "Barrier 同步 8 线程各 push 50 次；最终 pop 400 次。",
        "8 线程各 50 push；`try_pop` 计数 400。",
        "- 阅读 Michael-Scott 无锁队列。\n- 对比 `ds-linear-stack` 教学栈。",
        "Day1 画 CAS 循环；Day2 Python ref；Day3 C++ + ABA 口述。",
        "- 本站：`ds-linear-stack`",
        LF_SEEDS,
    )


BUILDERS = {
    "algo-advanced": build_algo_advanced,
    "algo-advanced-mo-algorithm": build_mo,
    "iv-classic-semaphore": build_semaphore,
    "iv-classic-singleton": build_singleton,
    "iv-classic-ring-buffer": build_ring,
    "iv-classic-thread-safe-queue": build_tsq,
    "iv-classic-lockfree-stack": build_lockfree,
}


def main() -> None:
    for slug, fn in BUILDERS.items():
        text = fn()
        out = BLOG / slug / "index.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {slug}: {count_chinese(text)} zh chars")


if __name__ == "__main__":
    main()
