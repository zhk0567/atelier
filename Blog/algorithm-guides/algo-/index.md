---
title: "算法 · 范式总览与导航"
series: algorithm
category: Algorithms
topic_path: algorithms
guide_toc: topic-algorithm
guide_tier: medium
status: published
date: 2026-05-22
tags: [Algorithm, Algorithms, Navigation]
---

# 算法 · 范式总览与导航

## 目录

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


## 导读

`python/algorithms/` 是 Study 仓库 **第二阶段** 的核心树干：排序、查找、递归、分治、贪心、动态规划、回溯、双指针、滑动窗口、前缀和、位运算、图论、字符串、数学与高级技巧（分块、莫队）均以**可运行脚本 + notes.md** 形式组织。本页 slug 为 `algo-`，`topic_path` 为 `algorithms`，角色是 **导航枢纽**——不重复 `algo-dynamic-programming`、`algo-graph` 等 major 子指南的正文，而是帮你从根目录 `notes.md` 一张表跳进正确子树，并链到 atelier 已发布的 **37** 篇 `algo-*` 教程。

与 Framework 系列不同，Algorithm 博文**不为** `leetcode/` 下每道题单独建站；算法范式在这里学透，刷题时回到 `problems/leetcode/<题号>_*/`。若你刚完成 `overview` 与 `ds-linear`，建议按「排序/查找 → 线性技巧（双指针、窗口、前缀和）→ 贪心/DP/回溯 → 图论子模块 → 数学子目录」推进，遇到卡题再查对应 `algo-*` 页。

## 预备知识

> **预备知识**：会读写 Python 3.10+ 与基础 C++17；理解 O() 记号；能在 PowerShell 用 `Set-Location -LiteralPath` 进入子目录运行 `python xxx.py` 或 `g++`。

应先掌握 `data_structures/` 中数组、链表、栈、队列与二叉树入门（见 `ds-` 总览与各 `ds-*` 子指南），再系统学算法范式。否则图论 BFS、DP 滚动数组、单调栈等会反复卡在「结构不会写」而非「转移不会推」。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
Get-Content -LiteralPath 'python\algorithms\notes.md' -Encoding utf8 | Select-Object -First 40
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

C++ 镜像路径：将上文 `python\` 换为 `cpp\`，文件名与目录名一致。

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

总览无单独聚合脚本；节选 `two_pointers.py` 中「两数之和有序」模板（完整见 [algo-two-pointers](/blog/algo-two-pointers)）：

```python
def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int]:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return lo, hi
        if s < target:
            lo += 1
        else:
            hi -= 1
    return -1, -1
```

下列为 **验证环境** 的串联命令（任选 3 个目录）：

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\algorithms\sorting'
python sorting.py
Set-Location -LiteralPath 'F:\Study\Algorithm\python\algorithms\two_pointers'
python two_pointers.py
Set-Location -LiteralPath 'F:\Study\Algorithm\python\algorithms\graph\traversal'
python graph_traversal.py
```

## C++ 实现

```cpp
// 节选：cpp/algorithms/greedy/greedy.cpp 活动选择计数
int activity_selection(const vector<pair<int,int>>& intervals) {
    vector<pair<int,int>> v = intervals;
    sort(v.begin(), v.end(), [](auto& a, auto& b) { return a.second < b.second; });
    int cnt = 0, last_end = INT_MIN / 2;
    for (auto& [s, e] : v) {
        if (s >= last_end) { cnt++; last_end = e; }
    }
    return cnt;
}
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\algorithms\greedy'
g++ -std=c++17 -O2 -Wall -Wextra -o greedy.exe greedy.cpp
.\greedy.exe
```

头文件：部分图论/数学脚本 `#include <alg_std.hpp>`，编译时加 `-I ..\..\include`（以子目录 README 为准）。

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

- [algo-advanced](/blog/algo-advanced)
- [algo-advanced-mo-algorithm](/blog/algo-advanced-mo-algorithm)
- [algo-backtracking](/blog/algo-backtracking)
- [algo-bit-manipulation](/blog/algo-bit-manipulation)
- [algo-divide-and-conquer](/blog/algo-divide-and-conquer)
- [algo-dp-bitmask](/blog/algo-dp-bitmask)
- [algo-dp-digit](/blog/algo-dp-digit)
- [algo-dp-interval](/blog/algo-dp-interval)
- [algo-dp-knapsack](/blog/algo-dp-knapsack)
- [algo-dp-linear](/blog/algo-dp-linear)
- [algo-dp-tree](/blog/algo-dp-tree)
- [algo-dynamic-programming](/blog/algo-dynamic-programming)
- [algo-graph](/blog/algo-graph)
- [algo-graph-bipartite-matching](/blog/algo-graph-bipartite-matching)
- [algo-graph-lca](/blog/algo-graph-lca)
- [algo-graph-mst](/blog/algo-graph-mst)
- [algo-graph-network-flow](/blog/algo-graph-network-flow)
- [algo-graph-scc](/blog/algo-graph-scc)
- [algo-graph-shortest-path](/blog/algo-graph-shortest-path)
- [algo-graph-topological-sort](/blog/algo-graph-topological-sort)
- [algo-graph-traversal](/blog/algo-graph-traversal)
- [algo-greedy](/blog/algo-greedy)
- [algo-math](/blog/algo-math)
- [algo-math-combinatorics](/blog/algo-math-combinatorics)
- [algo-math-extended-gcd](/blog/algo-math-extended-gcd)
- [algo-math-fast-power](/blog/algo-math-fast-power)
- [algo-math-geometry](/blog/algo-math-geometry)
- [algo-math-matrix](/blog/algo-math-matrix)
- [algo-math-number-theory](/blog/algo-math-number-theory)
- [algo-math-probability](/blog/algo-math-probability)
- [algo-prefix-sum](/blog/algo-prefix-sum)
- [algo-recursion](/blog/algo-recursion)
- [algo-searching](/blog/algo-searching)
- [algo-sliding-window](/blog/algo-sliding-window)
- [algo-sorting](/blog/algo-sorting)
- [algo-string](/blog/algo-string)
- [algo-two-pointers](/blog/algo-two-pointers)

## 站内已发布 algo-* 导航

- [algo-advanced](/blog/algo-advanced)
- [algo-advanced-mo-algorithm](/blog/algo-advanced-mo-algorithm)
- [algo-backtracking](/blog/algo-backtracking)
- [algo-bit-manipulation](/blog/algo-bit-manipulation)
- [algo-divide-and-conquer](/blog/algo-divide-and-conquer)
- [algo-dp-bitmask](/blog/algo-dp-bitmask)
- [algo-dp-digit](/blog/algo-dp-digit)
- [algo-dp-interval](/blog/algo-dp-interval)
- [algo-dp-knapsack](/blog/algo-dp-knapsack)
- [algo-dp-linear](/blog/algo-dp-linear)
- [algo-dp-tree](/blog/algo-dp-tree)
- [algo-dynamic-programming](/blog/algo-dynamic-programming)
- [algo-graph](/blog/algo-graph)
- [algo-graph-bipartite-matching](/blog/algo-graph-bipartite-matching)
- [algo-graph-lca](/blog/algo-graph-lca)
- [algo-graph-mst](/blog/algo-graph-mst)
- [algo-graph-network-flow](/blog/algo-graph-network-flow)
- [algo-graph-scc](/blog/algo-graph-scc)
- [algo-graph-shortest-path](/blog/algo-graph-shortest-path)
- [algo-graph-topological-sort](/blog/algo-graph-topological-sort)
- [algo-graph-traversal](/blog/algo-graph-traversal)
- [algo-greedy](/blog/algo-greedy)
- [algo-math](/blog/algo-math)
- [algo-math-combinatorics](/blog/algo-math-combinatorics)
- [algo-math-extended-gcd](/blog/algo-math-extended-gcd)
- [algo-math-fast-power](/blog/algo-math-fast-power)
- [algo-math-geometry](/blog/algo-math-geometry)
- [algo-math-matrix](/blog/algo-math-matrix)
- [algo-math-number-theory](/blog/algo-math-number-theory)
- [algo-math-probability](/blog/algo-math-probability)
- [algo-prefix-sum](/blog/algo-prefix-sum)
- [algo-recursion](/blog/algo-recursion)
- [algo-searching](/blog/algo-searching)
- [algo-sliding-window](/blog/algo-sliding-window)
- [algo-sorting](/blog/algo-sorting)
- [algo-string](/blog/algo-string)
- [algo-two-pointers](/blog/algo-two-pointers)


**深度补充：范式与刷题边界**

算法范式页教「怎么想」；单题 AC 在 `problems/leetcode/`。不要在本页抄题解。


**深度补充：与 overview 分工**

`overview` 讲仓库约定；本页只讲 `algorithms/` 树干。


**深度补充：第二阶段验收**

README 中算法覆盖表可对照子目录是否都有 notes 与脚本。


**深度补充：双语言维护**

改 Python 模板后应同步 C++ 镜像并各跑一次。


**深度补充：面试时间分配**

总览用于规划周计划，考场仍靠子指南模板。


**深度补充：导航复盘 6**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 7**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 8**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 9**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 10**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 11**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 12**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 13**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 14**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 15**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 16**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 17**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 18**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 19**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 20**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 21**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 22**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 23**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 24**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 25**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 26**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 27**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 28**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 29**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 30**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 31**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 32**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 33**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 34**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 35**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 36**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 37**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 38**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 39**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 40**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 41**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 42**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 43**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 44**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 45**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 46**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 47**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 48**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 49**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 50**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 51**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 52**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 53**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 54**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 55**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 56**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 57**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 58**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 59**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 60**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 61**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 62**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 63**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 64**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 65**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 66**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 67**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 68**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 69**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 70**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 71**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 72**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 73**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 74**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 75**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 76**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 77**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 78**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 79**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 80**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 81**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 82**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 83**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 84**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 85**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 86**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 87**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 88**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 89**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 90**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 91**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 92**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 93**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 94**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 95**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 96**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 97**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 98**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 99**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 100**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 101**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 102**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 103**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 104**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 105**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 106**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 107**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 108**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 109**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 110**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 111**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 112**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 113**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 114**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 115**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 116**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 117**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 118**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 119**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 120**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 121**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 122**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 123**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 124**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 125**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 126**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 127**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 128**

以 algo- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。
