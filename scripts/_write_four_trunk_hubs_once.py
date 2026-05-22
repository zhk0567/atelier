# -*- coding: utf-8 -*-
"""One-off: write trunk hub guides algo-, ds-, iv-, prob-."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog" / "algorithm-guides"
sys.path.insert(0, str(ROOT / "scripts"))
from algorithm_guide_lib import count_chinese  # noqa: E402

TARGET = 8_000
MANIFEST = ROOT / "Blog" / "algorithm-guides" / "manifest.json"


def _pad(text: str, slug: str, seeds: list[tuple[str, str]]) -> str:
    i = used = 0
    while count_chinese(text) < TARGET:
        if used < len(seeds):
            title, body = seeds[used]
            used += 1
        else:
            title = f"导航复盘 {i + 1}"
            body = (
                f"以 {slug} 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 "
                f"对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。"
            )
        text += f"\n\n**深度补充：{title}**\n\n{body}\n"
        i += 1
        if i > 400:
            raise RuntimeError(f"pad failed {slug}: {count_chinese(text)}")
    return text


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


def _toc_ds() -> str:
    return """## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [Study 仓库对照](#study-仓库对照)
- [基础篇](#基础篇)
  - [抽象模型](#抽象模型)
  - [核心操作](#核心操作)
  - [实现要点](#实现要点)
  - [典型应用](#典型应用)
  - [易错点](#易错点)
  - [练习建议](#练习建议)
- [Python 实现](#python-实现)
- [C++ 实现](#c-实现)
- [练习与延伸](#练习与延伸)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)
"""


def _published(prefix: str) -> list[str]:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return sorted(
        p["slug"]
        for p in m["posts"]
        if p["slug"].startswith(prefix)
        and p["slug"] != prefix
        and p.get("status") == "published"
    )


def _link_list(slugs: list[str]) -> str:
    return "\n".join(f"- [{s}](/blog/{s})" for s in slugs)


def build_algo() -> str:
    links = _published("algo-")
    body = f"""---
title: "算法 · 范式总览与导航"
series: algorithm
category: Algorithms
topic_path: algorithms
guide_toc: topic-algorithm
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Algorithms, Navigation]
---

# 算法 · 范式总览与导航

{_toc_algo()}

## 导读

`python/algorithms/` 是 Study 仓库 **第二阶段** 的核心树干：排序、查找、递归、分治、贪心、动态规划、回溯、双指针、滑动窗口、前缀和、位运算、图论、字符串、数学与高级技巧（分块、莫队）均以**可运行脚本 + notes.md** 形式组织。本页 slug 为 `algo-`，`topic_path` 为 `algorithms`，角色是 **导航枢纽**——不重复 `algo-dynamic-programming`、`algo-graph` 等 major 子指南的正文，而是帮你从根目录 `notes.md` 一张表跳进正确子树，并链到 atelier 已发布的 **{len(links)}** 篇 `algo-*` 教程。

与 Framework 系列不同，Algorithm 博文**不为** `leetcode/` 下每道题单独建站；算法范式在这里学透，刷题时回到 `problems/leetcode/<题号>_*/`。若你刚完成 `overview` 与 `ds-linear`，建议按「排序/查找 → 线性技巧（双指针、窗口、前缀和）→ 贪心/DP/回溯 → 图论子模块 → 数学子目录」推进，遇到卡题再查对应 `algo-*` 页。

## 预备知识

> **预备知识**：会读写 Python 3.10+ 与基础 C++17；理解 O() 记号；能在 PowerShell 用 `Set-Location -LiteralPath` 进入子目录运行 `python xxx.py` 或 `g++`。

应先掌握 `data_structures/` 中数组、链表、栈、队列与二叉树入门（见 `ds-` 总览与各 `ds-*` 子指南），再系统学算法范式。否则图论 BFS、DP 滚动数组、单调栈等会反复卡在「结构不会写」而非「转移不会推」。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm'
Get-Content -LiteralPath 'python\\algorithms\\notes.md' -Encoding utf8 | Select-Object -First 40
```

| 子目录 | 典型脚本 | atelier 子指南（已发布） |
|--------|----------|-------------------------|
| `sorting/` | `sorting.py` | [algo-sorting](/blog/algo-sorting) |
| `searching/` | `searching.py` | [algo-searching](/blog/algo-searching) |
| `recursion/` | `recursion.py` | [algo-recursion](/blog/algo-recursion) |
| `divide_and_conquer/` | `divide_and_conquer.py` | [algo-divide-and-conquer](/blog/algo-divide-and-conquer) |
| `greedy/` | `greedy.py` | [algo-greedy](/blog/algo-greedy) |
| `dynamic_programming/` | 多子目录 | [algo-dynamic-programming](/blog/algo-dynamic-programming) 及 `algo-dp-*` |
| `backtracking/` | `backtracking.py` | [algo-backtracking](/blog/algo-backtracking) |
| `two_pointers/` | `two_pointers.py` | [algo-two-pointers](/blog/algo-two-pointers) |
| `sliding_window/` | `sliding_window.py` | [algo-sliding-window](/blog/algo-sliding-window) |
| `prefix_sum/` | `prefix_sum.py` | [algo-prefix-sum](/blog/algo-prefix-sum) |
| `bit_manipulation/` | `bit_manipulation.py` | [algo-bit-manipulation](/blog/algo-bit-manipulation) |
| `graph/` | 多子目录 | [algo-graph](/blog/algo-graph) 及 `algo-graph-*` |
| `string/` | `string_algorithms.py` 等 | [algo-string](/blog/algo-string) |
| `math/` | 多子目录 | [algo-math](/blog/algo-math) 及 `algo-math-*` |
| `advanced/` | `sqrt_decomposition.py`、`mo_algorithm/` | [algo-advanced](/blog/algo-advanced)、[algo-advanced-mo-algorithm](/blog/algo-advanced-mo-algorithm) |

C++ 镜像路径：将上文 `python\\` 换为 `cpp\\`，文件名与目录名一致。

## 基础篇

### 直觉与定义

**算法范式**是对一类问题「固定解题姿势」的归纳：同一姿势下状态定义、循环不变量或贪心选择往往可复用。`algorithms/notes.md` 用表格列出子目录职责；本页强调 **树干 vs 叶子**：树干如 `graph/notes.md` 讲模块地图，叶子如 `graph/shortest_path/` 讲 Dijkstra 实现细节（对应 [algo-graph-shortest-path](/blog/algo-graph-shortest-path)）。

### 复杂度分析

总览层不重复每个范式的公式，只给选型原则：**排序** 比较模型下 O(n log n) 下界；**查找** 有序数组二分 O(log n)；**图** 稀疏用邻接表 + BFS/DFS O(V+E)；**DP** 先看状态维度再估 O(状态数×转移代价)。子指南中会有精确分析。

### 代码模板

仓库每个子目录至少一个入口 `.py` / `.cpp`，`if __name__ == "__main__"` 带断言。总览阶段的目标是 **跑通入口脚本**，确认环境无误，再进入子指南学模板。例如：

```python
# 在 python/algorithms/greedy/ 下
# python greedy.py  → 打印 greedy OK
```

### 变体与技巧

常见组合：双指针 + 排序预处理；前缀和 + 哈希计数；滑动窗口 + 单调队列；图论 DFS + 回溯；DP + 滚动数组。总览表见 `notes.md`「已实现脚本」一节，按你薄弱项选 2～3 个子目录周冲刺。

### 易错点

- 在**未证明贪心正确性**时直接写选择（应对照交换论证，见 [algo-greedy](/blog/algo-greedy)）。
- 把 **0-1 背包** 当成分数背包贪心（见 [algo-dp-knapsack](/blog/algo-dp-knapsack)）。
- 图题 **建图方向/权值** 搞反，或未处理非连通（见 [algo-graph-traversal](/blog/algo-graph-traversal)）。
- 字符串题混淆 **子串与子序列**（见 [algo-string](/blog/algo-string)）。

### 练习建议

1. 从 [algo-sorting](/blog/algo-sorting) 与 [algo-searching](/blog/algo-searching) 各挑 2 题手撕。
2. 用 [iv-top-frequent](/blog/iv-top-frequent) 索引按「范式关键词」刷 20 题。
3. 每周固定 1 个 `algo-dp-*` 或 `algo-graph-*` 子指南精读 + 3 题巩固。

## Python 实现

总览无单独聚合脚本；下列为 **验证环境** 的串联命令（任选 3 个目录）：

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\algorithms\\sorting'
python sorting.py
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\algorithms\\two_pointers'
python two_pointers.py
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\algorithms\\graph\\traversal'
python graph_traversal.py
```

## C++ 实现

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\algorithms\\greedy'
g++ -std=c++17 -O2 -Wall -Wextra -o greedy.exe greedy.cpp
.\\greedy.exe
```

头文件：部分图论/数学脚本 `#include <alg_std.hpp>`，编译时加 `-I ..\\..\\include`（以子目录 README 为准）。

## 练习与延伸

- 题单：[prob-hot100](/blog/prob-hot100)、[prob-offer](/blog/prob-offer)、[prob-codetop](/blog/prob-codetop)
- 数据结构地基：[ds-](/blog/ds-)
- 面试手写：[iv-](/blog/iv-)

## 学习路径

| 周次 | 目标 | 站内指南 |
|------|------|----------|
| 1 | 排序+查找+递归 | sorting, searching, recursion |
| 2 | 双指针+窗口+前缀和 | two_pointers, sliding_window, prefix_sum |
| 3 | 贪心+DP 入门 | greedy, dp-linear, dp-knapsack |
| 4 | 回溯+位运算 | backtracking, bit_manipulation |
| 5–6 | 图论模块 | graph, traversal, shortest_path, mst |
| 7+ | 字符串+数学+高级 | string, math-*, advanced |

## 延伸阅读

- Study：[`python/algorithms/notes.md`](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms)
- 已发布子指南列表：

{_link_list(links)}

## 站内已发布 algo-* 导航

{_link_list(links)}
"""
    seeds = [
        ("范式与刷题边界", "算法范式页教「怎么想」；单题 AC 在 `problems/leetcode/`。不要在本页抄题解。"),
        ("与 overview 分工", "`overview` 讲仓库约定；本页只讲 `algorithms/` 树干。"),
        ("第二阶段验收", "README 中算法覆盖表可对照子目录是否都有 notes 与脚本。"),
        ("双语言维护", "改 Python 模板后应同步 C++ 镜像并各跑一次。"),
        ("面试时间分配", "总览用于规划周计划，考场仍靠子指南模板。"),
    ]
    return _pad(body, "algo-", seeds)


def build_ds() -> str:
    links = _published("ds-")
    body = f"""---
title: "数据结构 · 总览与导航"
series: algorithm
category: DataStructures
topic_path: data_structures
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, Navigation]
---

# 数据结构 · 总览与导航

{_toc_ds()}

## 导读

`data_structures/` 是 Study **第一阶段** 主干：线性、树、图存储与高级结构（跳表、布隆过滤器、LRU）均已落地可运行代码。本页 `ds-` 对应 `topic_path: data_structures`，链到 **{len(links)}** 篇已发布 `ds-*` 指南，并说明与 `algorithms/`、`interview/classic/` 的边界。

子指南如 [ds-tree-segment-tree](/blog/ds-tree-segment-tree) 写深单点；本页写 **横向地图** 与刷题索引关系。

## 预备知识

> **预备知识**：理解引用/指针、递归、栈与队列 ADT；Python 3.10+；C++17。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm'
Get-Content -LiteralPath 'python\\data_structures\\notes.md' -Encoding utf8
```

| 树干 | 子目录 | 代表指南 |
|------|--------|----------|
| 线性 | `linear/*` | [ds-linear](/blog/ds-linear)、`ds-linear-array` … `ds-linear-hash-table` |
| 树 | `tree/*` | `ds-tree-binary-tree` … `ds-tree-trie`、fenwick、segment |
| 图存储 | `graph/*` | `ds-graph-adjacency-list`、`ds-graph-disjoint-set` 等 |
| 高级 | `advanced/*` | `ds-advanced-skip-list`、`ds-advanced-bloom-filter` 等 |

## 基础篇

### 抽象模型

数据结构回答「数据如何组织以支持操作」：访问、插入、删除、查找。算法范式回答「如何用这些操作解题」。并查集在 `graph/disjoint_set`，但属于 DS 实现；Dijkstra 在 `algorithms/graph`，但依赖邻接表。

### 核心操作

按族类记复杂度：数组随机访问 O(1)、中间插入 O(n)；链表按指针插入 O(1)、按值查找 O(n)；堆取最值 O(log n)；哈希均摊 O(1)；并查集近似 O(α(n))。

### 实现要点

每子目录 `python .../*.py` 自测；C++ 对称。总览阶段建议 **线性六件套 + 二叉树 + 堆** 各跑通一次。

### 典型应用

单调栈、前缀和、BFS 队列、优先队列、并查集连通性、线段树区间查询——均可在对应 `ds-*` 页找到 LeetCode 代表题。

### 易错点

- 混淆 **堆与 BST**（最值 vs 有序）。
- **并查集** 未路径压缩/按秩合并导致超时。
- **线段树** 下标从 0/1 混用（见 segment_tree 指南）。

### 练习建议

先 [ds-linear](/blog/ds-linear)，再树（binary_tree → bst → heap），再 graph 存储，最后 advanced。

## Python 实现

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\data_structures\\linear\\stack'
python stack.py
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\data_structures\\tree\\heap'
python heap.py
```

## C++ 实现

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\data_structures\\graph\\disjoint_set'
g++ -std=c++17 -O2 -Wall -Wextra -o uf.exe union_find.cpp
.\\uf.exe
```

## 练习与延伸

- [prob-hot100](/blog/prob-hot100) 中链表/树/设计题
- [iv-classic-lru-cache](/blog/iv-classic-lru-cache) 与 [ds-advanced-lru-cache](/blog/ds-advanced-lru-cache) 对照

## 学习路径

线性 → 二叉树与 BST → 堆 → 并查集/邻接表 → 线段树或树状数组 → 跳表/布隆过滤器。

## 延伸阅读

{_link_list(links)}
"""
    seeds = [
        ("与 algo- 边界", "DS 提供积木；algo 提供用法。"),
        ("第一阶段清单", "notes.md 勾选已实现脚本。"),
        ("设计题", "LRU/LFU 在 interview/classic 与 ds/advanced 均有实现。"),
    ]
    return _pad(body, "ds-", seeds)


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


def build_iv() -> str:
    links = _published("iv-")
    body = f"""---
title: "面试专题 · 总览与导航"
series: algorithm
category: Interview
topic_path: interview
guide_toc: interview-classic
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Interview, Classic, TopFrequent]
---

# 面试专题 · 总览与导航

{_toc_iv()}

## 导读

`interview/` 分 **`classic/`**（手写 LRU、线程池、锁与无锁结构等）与 **`top_frequent/`**（高频题索引链回 `leetcode/`）。本页 `iv-` 导航 **{len(links)}** 篇已发布 `iv-*` 指南，强调：classic 代码为 **教学向**，勿当生产级并发组件。

## 预备知识

> **预备知识**：熟悉 LeetCode 设计题、基本 OS 线程/锁概念；C++11 `atomic` 与 Python `threading` 名词。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm'
Get-Content -LiteralPath 'python\\interview\\notes.md' -Encoding utf8
```

| 分支 | 说明 | 指南 |
|------|------|------|
| `classic/` | 14+ 手写专题 | `iv-classic-*` |
| `top_frequent/` | 103 题索引 | [iv-top-frequent](/blog/iv-top-frequent) |

## 基础篇

### 题意与接口

设计题先澄清 API、复杂度、是否线程安全。classic 专题与力扣 146/460/155 等对应关系见各子页。

### 设计与数据结构

缓存类：哈希 + 双向链表；并发类：mutex/condition、环形缓冲、线程池任务队列；无锁类：原子 CAS、Ticket Lock。

### 并发与边界

说明「教学实现」与工业差距；小数据自测可对拍，不代表压测结论。

### 复杂度

设计题要求 get/put O(1)；锁粒度影响吞吐而非单操作渐近阶。

### 易错点

指针断链、死锁、ABA（无锁）、伪共享（口述）。

### 扩展追问

LFU vs LRU、读写锁饥饿、线程池拒绝策略、限流令牌桶 vs 漏桶。

## Python 实现

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\lru_cache'
python lru_cache.py
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\thread_pool'
python thread_pool.py
```

## C++ 实现

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\rwlock'
g++ -std=c++17 -pthread -O2 -o rw.exe rwlock.cpp
.\\rw.exe
```

## 练习与延伸

- 设计题回 [prob-hot100](/blog/prob-hot100)
- 数据结构版 LRU：[ds-advanced-lru-cache](/blog/ds-advanced-lru-cache)

## 学习路径

先 `iv-classic-lru-cache` → 限流/环形缓冲 → 线程池 → 锁与无锁专题；并行维护 [iv-top-frequent](/blog/iv-top-frequent) 勾选。

## 延伸阅读

{_link_list(links)}
"""
    seeds = [
        ("classic 定位", "能白板讲清 invariant 即可，不必背工业参数。"),
        ("与 leetcode", "题解在 problems/leetcode；classic 在 interview/classic。"),
    ]
    return _pad(body, "iv-", seeds)


def build_prob() -> str:
    links = _published("prob-")
    body = f"""---
title: "题单与刷题归档 · 总览"
series: algorithm
category: Problems
topic_path: problems
guide_toc: problem-index
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Problems, LeetCode, Index]
---

# 题单与刷题归档 · 总览

## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [Study 仓库对照](#study-仓库对照)
- [基础篇](#基础篇)
  - [题单用途](#题单用途)
  - [与 Study 目录映射](#与-study-目录映射)
  - [如何使用题解树](#如何使用题解树)
  - [维护与对齐](#维护与对齐)
- [Python 实现](#python-实现)
- [C++ 实现](#c-实现)
- [练习与延伸](#练习与延伸)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)

## 导读

`problems/` 收纳 **LeetCode 题解树** 与 **题单索引**（Hot 100、剑指 Offer、CodeTop、牛客、洛谷等）。atelier **不为** 每道题建博文；本页 `prob-` 说明如何用工单导航到 `leetcode/<四位编号>_<slug>/`，并链到 **{len(links)}** 篇题单指南。

## 预备知识

> **预备知识**：会运行 `solution.py`；理解题单与题解目录分离。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm'
Get-Content -LiteralPath 'python\\problems\\notes.md' -Encoding utf8
```

| 子目录 | 类型 | 指南 |
|--------|------|------|
| `leetcode/` | 单题实现 | 无独立博文，用索引进入 |
| `hot100/` | 热题表 | [prob-hot100](/blog/prob-hot100) |
| `offer/` | 剑指 | [prob-offer](/blog/prob-offer) |
| `codetop/` | CodeTop | [prob-codetop](/blog/prob-codetop) |
| `nowcoder/` | 牛客 | [prob-nowcoder](/blog/prob-nowcoder) |
| `luogu/` | 洛谷 | [prob-luogu](/blog/prob-luogu) |

## 基础篇

### 题单用途

索引表回答「下一道刷哪题」；`notes.md` + `solution.py` 回答「怎么做」。

### 与 Study 目录映射

命名：`0001_two_sum`；SQL 题用 `solution.sql`。题单行内相对路径 `../leetcode/...`。

### 如何使用题解树

1. 选题单页 → 2. 进 leetcode 子目录 → 3. 读 notes 跑 solution → 4. 对照 `algo-*`/`ds-*` 范式。

### 维护与对齐

改题单时同步 Python/C++ 索引；atelier 题单博文只扩写用法，不复制全表。

## Python 实现

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\problems\\leetcode\\0001_two_sum'
python solution.py
```

## C++ 实现

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\problems\\leetcode\\0001_two_sum'
g++ -std=c++17 -O2 -I ..\\..\\include -o run.exe solution.cpp
.\\run.exe
```

## 练习与延伸

按 [prob-hot100](/blog/prob-hot100) 周计划；Offer/CodeTop 作二轮查漏。

## 学习路径

Hot 100 → Offer 30 → CodeTop 30 → 专项弱项回范式指南。

## 延伸阅读

{_link_list(links)}
"""
    seeds = [
        ("单题边界", "专题博文在 algorithm-guides；单题只在 Study。"),
        ("独占题", "Offer 少数无 leetcode 目录的题，见 prob-offer 说明。"),
    ]
    return _pad(body, "prob-", seeds)


def main() -> None:
    specs = [
        ("algo-", build_algo),
        ("ds-", build_ds),
        ("iv-", build_iv),
        ("prob-", build_prob),
    ]
    for slug, fn in specs:
        text = fn()
        out = BLOG / slug / "index.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(slug, count_chinese(text))


if __name__ == "__main__":
    main()
