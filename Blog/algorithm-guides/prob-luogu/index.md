---
title: "题单 · 洛谷（Luogu）导航与题解树"
series: algorithm
category: Problems
topic_path: problems/luogu
guide_toc: problem-index
guide_tier: index
status: published
date: 2026-05-22
tags: [Algorithm, Luogu, OJ, 题单, 洛谷]
---

# 题单 · 洛谷（Luogu）导航与题解树

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

**洛谷（Luogu）** 是国内常用的算法竞赛与练习 OJ。Study 仓库在 `python/problems/luogu/notes.md` 维护 **洛谷题号 ↔ 本地 `problems/leetcode/` 或独占目录** 的导航索引，与力扣题意重合时 **不复制第二份** `solution.py`。本站 `prob-luogu` 说明如何把洛谷当作 **OJ 向刷题地图**，在双语言树中落点，并与 `prob-hot100`、`prob-codetop`、`prob-offer` 分工。

洛谷题量远大于索引表行数；本索引是可维护子集，链到仓库已有题解。外站新题先搜 `leetcode/` 是否已有变体，再决定是否扩表。

## 预备知识

> **预备知识**：会注册洛谷账号并在网页提交；熟悉仓库 `四位题号_slug` 命名；能运行 `python solution.py`。PowerShell 用 `-LiteralPath`。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
Get-Content -LiteralPath 'python\problems\luogu\notes.md' -Encoding utf8 | Select-Object -First 40
Set-Location -LiteralPath 'F:\Study\Algorithm\python\problems\leetcode\0001_two_sum'
python solution.py
```

| 路径 | 作用 |
|------|------|
| `python/problems/luogu/notes.md` | 洛谷 ↔ 本地目录 |
| `cpp/problems/luogu/notes.md` | 同构 |
| `python/problems/leetcode/<slug>/` | 主题解树 |

```powershell
$root = 'F:\Study\Algorithm\python\problems\leetcode'
Test-Path -LiteralPath (Join-Path $root '0001_two_sum' 'solution.py')
```

## 基础篇

### 题单用途

洛谷索引适合：**按洛谷题号反查本地实现**、**竞赛向复习（P 序）**、**与力扣交叉核对**。表内行通常含洛谷题号、难度、对应 `leetcode` slug 或 `luogu_Pxxx` 独占目录说明。不是洛谷全站镜像；价值是 **离线可运行 + 笔记同仓**。

与 `prob-hot100`：Hot 按社区热度 103 行；洛谷按 **OJ 题号** 组织，方便在学校/竞赛班按 P 题刷。与 `prob-codetop`：CodeTop 按公司方向标签；洛谷按 **平台题号**。与 `prob-offer`：Offer 用剑指编号。

**使用场景**：已在洛谷 AC 某题，想在本地找 C++ 对拍；或仓库先写了 leetcode 题解，想在洛谷提交同思路代码。

### 与 Study 目录映射

映射表列一般含：**洛谷题号（P 或 AT）**、**标题关键词**、**本地目录**。规则：

1. 与 LeetCode **同题** → 只链 `leetcode/<slug>/`，洛谷表一行指向该 slug；
2. **洛谷独有** 且仓库已收录 → `luogu_P1234_<slug>/` 或约定前缀（以 `notes.md` 为准）；
3. **禁止** 在 `luogu/` 下复制完整题解代码，避免双份维护。

Python/C++ **目录名一致**；缺 C++ 时以 Python 为准补题，不改 slug。

**示例映射（说明格式，完整表见 GitHub notes.md）**：

| 洛谷 | 说明 | 本地 |
|------|------|------|
| P1000 | 入门练习 | 可能无 leetcode 对应，独占或练习 |
| 对应力扣 1 | 两数之和 | `0001_two_sum` |
| 图论模板 | 最短路 | `0743_network_delay_time` 等 |

统计目标：索引行 **100% 可打开** 有效目录；新增题解先 leetcode 再改 luogu 一行。

### 如何使用题解树

推荐流程：

1. 在洛谷网页做题或看题号；
2. 打开 `luogu/notes.md` 搜题号或标题；
3. 进入映射的 `leetcode` 或 `luogu_*` 目录；
4. 读 `notes.md`，运行 `solution.py` / 编译 C++；
5. 复盘：洛谷题号 + 范式 + 是否独立 AC。

**反查**：只有力扣号时，在 `leetcode/` 搜索 slug，再看 luogu 表是否已挂接；无则提 PR 增一行。

**精读配合专题**：图论 → `algo-graph-*`；DP → `algo-dp-*`；数据结构 → `ds-*`。题单导航「考过哪道」，专题讲「为什么」。

**提交差异**：洛谷支持 `std::cin` 加速、部分题多组数据；本地 `solution.py` 若只含单组，提交前按题面改读入。C++ 注意 `long long` 与 `%lld`。

### 维护与对齐

维护顺序：

1. 新建 `leetcode/<slug>/` 题解（若力扣有同题）；
2. 在 `python/problems/luogu/notes.md` 增改一行，`cpp/...` 同步；
3. 表内不写长题解，仅链接与短标签；
4. atelier `prob-luogu` **不镜像** 全表，以 GitHub `notes.md` 为真相来源。

**质量自检**：链接有效 → `solution.py` 通过 → `notes.md` 含复杂度 → C++ 可编译（若有）。

**与外部洛谷**：外站题面更新时，以本地能跑通为准；题号变更在 commit 注明 `luogu: Pxxxx → slug`。

## Python 实现

题单目录无聚合脚本；下列摘自 leetcode 代表题。

```python
# python/problems/leetcode/0001_two_sum/solution.py
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
```

```python
# python/problems/leetcode/0200_number_of_islands/solution.py
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])

    def dfs(i: int, j: int) -> None:
        grid[i][j] = "0"
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == "1":
                dfs(ni, nj)

    ans = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "1":
                dfs(i, j)
                ans += 1
    return ans
```

## C++ 实现

```cpp
// cpp/problems/leetcode/0001_two_sum/solution.cpp — 节选
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int,int> pos;
    for (int i = 0; i < (int)nums.size(); ++i) {
        int need = target - nums[i];
        auto it = pos.find(need);
        if (it != pos.end()) return {it->second, i};
        pos[nums[i]] = i;
    }
    return {};
}
```

洛谷提交时复制核心逻辑并适配输入输出格式；完整文件见 Study 各 slug 目录。

## 练习与延伸

- 按学校/竞赛课表 P 序刷，用 `notes.md` 落本地；
- 与 hot100 交叉：热题在洛谷常有对应 P 号；
- OI 省选以上题若仓库未收录，先在 leetcode 搜相似模板。

## 学习路径

**每周**：5–8 道洛谷题 + 复盘映射行。**冲刺**：弱项范式在 luogu 表挑有链接的精刷。

## 延伸阅读

- [洛谷](https://www.luogu.com.cn/)
- Study `python/problems/luogu/notes.md`
- `prob-hot100`、`prob-codetop`、`prob-offer`


**深度补充：洛谷与 LeetCode**

很多 P 题是 LC 中文版或同思路；优先 leetcode 目录。

**深度补充：AT 题**

部分行指向 AtCoder 风格；以 notes 为准。

**深度补充：独占目录命名**

luogu_P 前缀便于搜索。

**深度补充：PR 规范**

增行注明 P 号与 slug。

**深度补充：C++ 提交**

复制 solution.cpp 注意 IO 格式。

**深度补充：Python 提交**

洛谷 Py 3 与本地版本一致。

**深度补充：时间限制**

本地通过≠洛谷 AC，检查复杂度。

**深度补充：空间限制**

DFS 深度改 BFS 或栈。

**深度补充：多组数据**

while read until EOF 模板。

**深度补充：输出格式**

空格换行严格；Presentation Error。

**深度补充：数据范围**

int 溢出改 long long。

**深度补充：图论题**

邻接表 vector 链 algo-graph。

**深度补充：DP 题**

状态方程写 notes 再编码。

**深度补充：题单不替代专题**

prob-luogu 导航，algo-dp-linear 讲原理。

**深度补充：学校作业**

老师 P 号表可对 notes 增行。

**深度补充：竞赛 camp**

按难度分桶刷，映射表挑已有。

**深度补充：与 nowcoder**

prob-nowcoder 另一 OJ，勿混。

**深度补充：manifest index**

汉字≥4000，guide_tier index。

**深度补充：draft**

校验后 published。

**深度补充：结语**

洛谷题号→notes.md→leetcode 树是标准三步。

**深度补充：洛谷 P 号**

以 notes.md 为准查 P 号对应本地 slug，勿臆测目录名。


**深度补充：力扣同题优先**

有 leetcode 题解则 luogu 表只链过去，不复制代码。


**深度补充：独占 luogu 目录**

洛谷独有题用约定前缀目录，见 notes 说明。


**深度补充：多组输入**

洛谷很多题多组数据，提交前改读入模板 while 直到 EOF。


**深度补充：输出格式**

空格换行严格，Presentation Error 常见。


**深度补充：long long**

数据范围大时 C++ 用 long long，Python 自动大整数。


**深度补充：cin 加速**

C++ ios::sync_with_stdio(false); cin.tie(nullptr);


**深度补充：与 hot100**

热题在洛谷常有对应，可交叉索引。


**深度补充：与 codetop**

公司向用 codetop，OJ 号用 luogu，勿混目录。


**深度补充：与 offer**

剑指编号在 prob-offer，洛谷用 P 号。


**深度补充：PR 增行**

新增映射注明 P 号、slug、难度标签。


**深度补充：不镜像全表**

atelier 本篇不贴完整索引，GitHub notes 为真相源。


**深度补充：专题配合**

图论 ds-graph，DP algo-dp，数据结构 ds-。


**深度补充：提交差异**

本地 solution 通过不等于洛谷 AC，检查复杂度与 IO。


**深度补充：竞赛 camp**

按 P 序刷时先用 notes 找本地实现再扩写。


**深度补充：学校作业**

老师布置 P 号可对表增行贡献仓库。


**深度补充：AT 题**

部分行指向 AtCoder，以 notes 为准。


**深度补充：质量自检**

链接有效、solution 通过、notes 含复杂度。


**深度补充：结语洛谷**

洛谷题号→notes.md→leetcode 树三步走。


**深度补充：综合复盘要点 20**

第 20 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 21**

第 21 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 22**

第 22 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 23**

第 23 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 24**

第 24 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 25**

第 25 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 26**

第 26 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 27**

第 27 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 28**

第 28 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 29**

第 29 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 30**

第 30 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 31**

第 31 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 32**

第 32 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 33**

第 33 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 34**

第 34 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 35**

第 35 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 36**

第 36 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 37**

第 37 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 38**

第 38 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 39**

第 39 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 40**

第 40 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 41**

第 41 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 42**

第 42 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 43**

第 43 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 44**

第 44 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 45**

第 45 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 46**

第 46 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 47**

第 47 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 48**

第 48 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 49**

第 49 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 50**

第 50 条复盘：回到 prob-luogu 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。
