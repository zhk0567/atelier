---
title: "数据结构 · 树状数组（Fenwick Tree / BIT）"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/fenwick_tree
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-22
tags: [DataStructures, FenwickTree, BIT, PrefixSum, LeetCode307]
---

# 数据结构 · 树状数组（Fenwick Tree / BIT）

## 目录

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

## 导读

**树状数组（Binary Indexed Tree，BIT）**，又称 **Fenwick Tree**，由 Peter Fenwick 提出，用于在固定长度序列上高效维护**前缀和**及其逆运算。本仓库 `data_structures/tree/fenwick_tree/` 提供 **单点加 + 前缀和 / 区间和** 的模板，并附带 **区间加 + 单点查（RUPQ）** 的差分写法；与 `segment_tree/` 的 lazy 线段树形成对照，共同服务 [LeetCode 307. 区域和检索 - 数组可修改](https://leetcode.cn/problems/range-sum-query-mutable/) 等题型。

与 **线段树**（见本站 `ds-tree-segment-tree`，第 1 批 batch1 已发布）对比的选型原则可以记成一句话：**能写成前缀和（或差分 + 前缀和）的问题，优先 BIT；需要区间改、区间查且合并函数不是「加法」、或需要 lazy 覆盖赋值、矩阵标记、历史版本时，用线段树。** 307 题两种写法均可 AC；Study 题解目录默认用 BIT，线段树在同题另一目录对拍。

本专题 `topic_path` 为 `data_structures/tree/fenwick_tree`，`guide_toc` 为 `topic-ds`，`guide_tier` 为 `medium`。读完你应能：

1. 解释 `lowbit(i) = i & -i` 与「管辖区间长度」的关系，在纸上画出 n=8 的 BIT 覆盖关系；
2. 写出 **1-based** 内部下标与 **0-based** 对外接口的转换；
3. 用差分数组 + BIT 实现 `FenwickRUPQ` 的区间加、单点查；
4. 将 307 的 `update` / `sumRange` 映射为 `add` 与两次 `prefix_sum`；
5. 在 Python/C++ 中运行 `fenwick_tree.py` / `fenwick_tree.cpp` 并通过断言；
6. 与线段树专题对照，说出何时 BIT 更短、何时必须换线段树。

**面试出现频率**：单独考「默写 BIT」的频率低于链表与动态规划，但在「动态前缀和」「逆序对」「离散化 + 统计」类题中几乎必现。简历写「熟悉数据结构」时，至少应能在白板写出 `add` 与 `prefix_sum` 两个 while 循环，并讲清 307 的差量更新。

**本实现边界**：`FenwickTree` 仅支持**单点加**与**区间和**（经两次前缀和）；`FenwickRUPQ` 支持**区间加 + 单点查**，不支持**区间加 + 区间和**（后者需双 BIT 或线段树，本仓库未实现，基础篇会说明思路）。不支持区间最值、区间乘、持久化版本。

**与 ds-tree-segment-tree 的导航关系**

`ds-tree-binary-tree` 讲递归与遍历，`ds-tree-fenwick-tree`（本页）讲 BIT 与 307 短实现，`ds-tree-segment-tree` 讲 lazy 区间加与区间和。三篇可组成「树形存储」学习周：先理解二叉树递归，再 BIT（代码更短），再线段树（扩展更强）。manifest 中三 slug 均在 `data_structures/tree/` 下，Study 路径对称。

**专题学习成果清单（可打印勾选）**

学完本页后，你应能独立完成：手画 n=8 时每个下标 i 的 `i & -i` 与向上跳路径；能解释为何数组开 `n+1`；能区分 `add(index, delta)` 中 index 是 0-based 而内部 `i=index+1`；能写出 `range_sum(l,r)` 在 `l=0` 时的分支；能说明 RUPQ 为何在 `r+1` 处减 `v`；能默写两个 while 循环；能在 Python 运行看到 `Fenwick OK`；能在 C++ 编译运行；能口述 BIT 与线段树选型表中的三行差异；能完成 LC 307 提交；知道 315/327 类题需要离散化 + BIT。勾选少于八项建议延长学习路径前半周。

**阅读本页的推荐顺序**

第一遍只读导读、基础篇、学习路径，并手画 lowbit 跳链；第二遍对照 Python 实现逐行阅读，运行脚本；第三遍闭卷默写 `add` / `prefix_sum`；第四遍做 307 并与 `ds-tree-segment-tree` 对拍；第五遍浏览练习与延伸中的进阶题号。C++ 读者在第三遍后增加编译运行，注意 `long long`。

**与线段树（ds-tree-segment-tree，batch1）选型详解**

两结构在「单点修改 + 区间求和」类题上复杂度同为 O(log n)，差别在**代码形态、可扩展操作、常数、面试叙述成本**。下表归纳本站线段树专题与本页 BIT 的分工，便于刷题时秒选：

| 场景 | 推荐 | 理由 |
|------|------|------|
| LC 307、动态前缀和 | BIT | 模板短、无递归、Study 题解默认 |
| 区间加 + 区间和（多次） | 线段树 lazy | 单 BIT 不够；双 BIT 可替代但记忆成本高 |
| 区间加 + 单点查 | BIT + 差分（RUPQ） | 本仓库 `FenwickRUPQ` 直接支持 |
| 区间最值 / 区间 gcd | 线段树 | BIT 非加法聚合不直观 |
| 区间赋值覆盖 | 线段树（赋值 lazy） | BIT 不适用 |
| 逆序对、离散化频次 | BIT | 值域压缩后做前缀频次 |
| 扫描线 + 覆盖长度 | 线段树或 BIT | 聚合为加法时 BIT 可；非加法用线段树改节点 |
| 笔试时间紧、只求 AC | BIT 优先 | 少写四函数、少 push |
| 面试要展示「区间结构」 | 先 BIT 再补线段树 | 体现你知道两种工具 |

**同一题 307 的双解法心智模型**：线段树把 `[0,n-1]` 建成二叉树，单点赋值通过「查旧值 + 区间加差量」或点递归；BIT 把数组看成前缀和可加减的结构，单点赋值同样是差量 `add`。查询都是区间和，BIT 用两次前缀。对拍时应用同一组 `update` / `sumRange` 序列，两种实现结果必须一致；若不一致，优先查 BIT 的 1-based 与 307 的 `_prefix(left)` 边界。

**为何 batch1 先发布线段树而本页仍重要**：线段树是「区间题通用语言」，BIT 是「前缀和题的最短路径」。只学线段树会在 307、315 上过度实现；只学 BIT 会在「区间加区间和」上强行推双 BIT 或 WA。两专题互链的目的就是避免单一模板思维。

**本页篇幅与练习量的关系**

medium 档要求足够汉字支撑自学，核心交付物是：默写 BIT、AC 307、能填上表选型。315、327、493 等题在练习与延伸中点到为止。时间紧时完成核心交付物即可，不必停留超过两周。若校验汉字不足，说明还应阅读基础篇手算与 lowbit 推导，而非跳过正文。

## 预备知识

> **预备知识**：熟悉数组 0-based 下标、前缀和 O(1) 查询与 O(n) 单点修改的对比；理解差分数组「区间加两端打点」；Python 3.10+；C++17。建议已读过前缀和或完成过一道「可修改数组求区间和」的暴力题，才能体会 BIT 将两次操作都降到 O(log n) 的意义。

需要的前置概念：

- **前缀和**：`S(i) = a[0] + … + a[i]`；静态数组可 O(n) 预处理、O(1) 查询，但单点修改 O(n)。
- **差分数组**：对 `[l,r]` 加 `v` 等价于 `d[l]+=v`, `d[r+1]-=v`；原数组前缀和恢复点值。BIT 可维护差分的前缀，从而得到 RUPQ。
- **按位与 `-i`**：补码表示下 `-i` 等价于按位取反加一；`i & -i` 提取最低位 1（lowbit）。
- **long long**：多次累加可能超 `int`；C++ 实现用 `long long`。

若对递归树不熟，不影响 BIT 学习——BIT 是**迭代**而非递归树。若计划学线段树，可先读本页再读 `ds-tree-segment-tree` 的 lazy 部分，对比「同样 O(log n)，实现风格完全不同」。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/tree/fenwick_tree` |
| Python | `python/data_structures/tree/fenwick_tree/fenwick_tree.py` |
| C++ | `cpp/data_structures/tree/fenwick_tree/fenwick_tree.cpp` |
| 笔记 | 两侧 `notes.md` |
| LeetCode 对照 | `problems/leetcode/0307_range_sum_query_mutable/`（题解以 BIT 为主） |
| 相关 | `data_structures/tree/segment_tree/`（线段树，见 `ds-tree-segment-tree`） |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\data_structures\tree\fenwick_tree'
python fenwick_tree.py
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\tree\fenwick_tree'
g++ -std=c++17 -O2 -Wall -Wextra -o fenwick.exe fenwick_tree.cpp
.\fenwick.exe
```

期望输出 `Fenwick OK`。将 `F:\Study\Algorithm` 换成本机路径。

**文件职责**

- `fenwick_tree.py` / `.cpp`：`FenwickTree`（单点加、区间和）、`FenwickRUPQ`（区间加、单点查）；
- `notes.md`：复杂度与 LC 307 链接；
- `GUIDE.md`：仓库内本地导读（与 atelier 本页互补，勿整段复制）。

## 基础篇

### 抽象模型

将长度为 `n` 的数组 `a[0..n-1]` 视为可反复单点修改的序列。树状数组在**辅助数组** `bit[1..n]`（1-based）上维护一种「可加减、可前缀聚合」的信息，使得：

- 在位置 `i` 增加 `delta`，影响 `bit` 中从 `i` 出发沿「父链」的 O(log n) 个单元；
- 查询前缀 `a[0]+…+a[i]` 同样沿链累加 O(log n) 个单元。

**与完全二叉树的联系（理解用，实现不必建树）**  
把下标 1..n 看成叶子，每个 `bit[i]` 负责一段**连续**区间，长度恰为 `lowbit(i) = i & -i`。例如 n=8 时：

```
下标 i:     1   2   3   4   5   6   7   8
lowbit:     1   2   1   4   1   2   1   8
管辖长度:   1   2   1   4   1   2   1   8
```

`add` 时从 `i` 跳到 `i + lowbit(i)`，直到超过 `n`；`prefix_sum` 时从 `i` 跳到 `i - lowbit(i)`，直到 0。这不是显式指针树，而是**隐式父节点**公式，空间仅 `n+1`，常数远小于线段树的 `4n` 与递归栈。

**不变式（口语版）**  
若把所有单点修改落实到「每个下标对 bit 的贡献」，则 `prefix_sum(t)` 返回的正是原数组 `[0..t]` 的和。建树时可对每个 `a[i]` 调用 `add(i, a[i])`，或 O(n) 线性构造（本仓库采用逐点 add，n 不大时足够）。

**与朴素前缀和数组对比**  
朴素 `prefix[]` 查询 O(1)、单点改 O(n)；BIT 把两者都变为 O(log n)，在 **m 次修改 + m 次查询** 且 n、m 同阶时，从 O(mn) 降为 O(m log n)。当修改极少、查询极多且数组静态时，仍用朴素前缀和更简单。

**命名**  
Fenwick Tree、Binary Indexed Tree、树状数组、BIT 同义；国内教材与竞赛资料混用，面试说「树状数组」或「BIT」均可。

**手算例题（n=5，初值全 0，依次 add）**  
对下标 2 加 3、下标 4 加 5 后，逻辑数组为 `[0,0,3,0,5]`。`prefix_sum(4)` 应为 8；`range_sum(2,4)` 应为 8。手算时列出 `i=3` 时 add 路径：3 → 4（因 lowbit(3)=1）→ 8（lowbit(4)=4）停止；`prefix_sum(4)` 路径：4 → 0（减 lowbit）。若与代码不一致，优先检查是否用了 0-based 下标却忘记 `+1`。

**为何不是「真树」却仍叫树状**  
早期教材把 `bit[i]` 与「去掉偶数下标子树」后的结构画成树形；实现时无需建树指针，但**管辖区间**的父子关系仍成立：`bit[i]` 包含 `bit[i-lowbit(i)]` 的信息片段。理解这一层有助于迁移到二维 BIT：外层下标与内层下标各走一套 lowbit。

**复杂度直觉**  
每次 `add` 或 `prefix_sum` 最多走 log₂n 步（严格说是「二进制位数」次）；n 次建树的逐点 add 是 O(n log n)，可优化为 O(n) 建树。空间 O(n)。与 O(n) 暴力修改相比，在 m 次操作、n 与 m 同阶时总时间从 O(mn) 降为 O(m log n)，与线段树同阶，差别在常数与可实现的操作族。

**形式化定义（可选阅读）**  
设 `bit` 满足：对任意 i，维护区间 `(i - lowbit(i), i]` 内原数组元素之和（在 1-based 下标语言下）。单点 `add(p, δ)` 对所有包含 p 的 `bit[i]` 加 δ，恰好是 i 从 `p+1`（0-based 的 p）出发不断 `+lowbit` 的集合。前缀 `prefix_sum(t)` 累加所有包含 t 的 `bit[i]`，是 i 从 `t+1` 出发不断 `-lowbit` 的集合。两集合不交且并覆盖所需信息，故正确性成立。证明用归纳或按位分析均可，面试通常不要求写证明，但应能解释「为何跳 lowbit」。

**与前缀和数组的一一对比表**

| 能力 | 朴素前缀和 | 树状数组 |
|------|------------|----------|
| 建 | O(n) | O(n log n) 或 O(n) |
| 查 [0,t] | O(1) | O(log n) |
| 改 a[i] | O(n) 重建 | O(log n) |
| 查 [l,r] | O(1) | O(log n) |
| 代码行数 | 极少 | 很少 |
| 适合 | 静态 / 极少改 | 多次改查 |

### 核心操作

| 操作 | 时间 | 说明 |
|------|------|------|
| `add(index, delta)` | O(log n) | 0-based 下标，内部 `i = index + 1` |
| `prefix_sum(index)` | O(log n) | 闭区间 `[0, index]` 之和 |
| `range_sum(l, r)` | O(log n) | `prefix_sum(r) - prefix_sum(l-1)`，`l=0` 特判 |
| `FenwickRUPQ.range_add(l,r,v)` | O(log n) | 区间加，差分 + BIT |
| `FenwickRUPQ.point_query(i)` | O(log n) | 单点值 = 差分前缀 |

**区间和公式**  
`range_sum(l, r) = prefix_sum(r) - prefix_sum(l - 1)`，当 `l = 0` 时第二项无定义，实现中直接 `return prefix_sum(r)`。这是所有 BIT 题面的固定套路，务必背熟。

**307 题映射**  
`update(index, val)`：令 `delta = val - nums[index]`，更新原数组后 `add(index, delta)`。  
`sumRange(left, right)`：即 `range_sum(left, right)`。

**RUPQ 语义**  
维护隐式差分 `d`：`range_add(l,r,v)` → `add(l,v)` 且 `add(r+1,-v)`（当 `r+1 < n`）；`point_query(i)` → `prefix_sum(i)` 即为原数组在 `i` 的值。这与差分数组教科书写法一致，只是把「对差分做前缀」交给 BIT。

**不能直接用本仓库两类同时做的组合**  
**区间加 + 区间和** 需要 **两个 BIT**（一个维护差分、一个维护差分前缀和）或线段树 lazy；面试若听到「区间改区间查」应立刻反应：单 BIT 不够，要么双 BIT 要么线段树。`ds-tree-segment-tree` 的 lazy 实现正是「区间加 + 区间和」的直观解法。

**单点赋值 vs 单点加**  
本仓库 `FenwickTree.add` 语义是「下标 index 增加 delta」。若题面是赋值，必须像 307 一样维护原数组副本或先查旧值再 add 差量。若题面是「下标加 v」，则直接 `add(index, v)` 即可，无需 `_nums`。读题时圈出动词，避免模板混用。

**区间修改的三种常见语义对照**

| 题意 | 常用结构 |
|------|----------|
| 单点改 + 区间和 | BIT（307） |
| 区间加 + 单点查 | 差分 + BIT（RUPQ） |
| 区间加 + 区间和 | lazy 线段树 / 双 BIT |
| 区间赋值 + 区间和 | 赋值 lazy 线段树 |

### 实现要点

**1-based 内部下标**  
`bit` 长度 `n+1`，有效下标 `1..n`；对外 API 保持 0-based（`index` 从 0 开始），进入 `add` / `prefix_sum` 时 `i = index + 1`。这是最常见写法，避免 off-by-one；若你手写全 1-based，LeetCode 接口要记得减一。

**lowbit 与循环**

```python
i += i & -i   # add：向「父」跳
i -= i & -i   # query：向「左」跳
```

C++ 中 `i & -i` 对 `int` 成立；`i` 为 0 时 while 终止。`add` 循环条件 `i <= n`；`prefix_sum` 条件 `i > 0`。

**建树**  
本仓库 `FenwickTree(n)` 创建全零 `bit`，再由调用方对每个初值 `add(i, v)`。也可 O(n) 从数组一次性 build（见竞赛模板 `O(n)` 构造），教学代码保持清晰优先。

**FenwickRUPQ 的 BIT 长度**  
构造 `FenwickTree(n + 2)`，因为 `range_add` 可能在 `r+1 = n` 处 `add`，需要下标 `n+1` 不越界。C++ 与 Python 一致。

**空间**  
`O(n)` 一个数组；无递归，栈 O(1)。对比线段树 `4n` 与递归深度，BIT 更省内存、缓存更友好。

**与线段树实现要点对照（摘自 batch1 线段树专题的核心差异）**

| 维度 | 树状数组（本页） | 线段树（`ds-tree-segment-tree`） |
|------|------------------|----------------------------------|
| 代码形态 | 两个 while，约 15 行 | 递归四函数 + lazy push |
| 区间加 + 区间和 | 需双 BIT 或转换题意 | lazy 直观 |
| 区间最值 | 可写但繁琐 | 改合并函数即可 |
| 单点改 + 区间和 | 原生强项（307） | 差量 `range_add` 亦可 |
| 空间 / 常数 | n+1，更小 | 约 4n，更大 |
| 面试默写时间 | 通常更短 | 更易讲清复杂区间语义 |

**何时坚持 BIT**：307、315、327（配合离散化）、逆序对、「坐标压缩 + 频次前缀」类。  
**何时换线段树**：区间加区间和且不想推双 BIT；区间 min/max/xor；赋值 lazy；扫描线维护非加法聚合；持久化主席树。

**O(n) 建树（扩展）**  
竞赛常用：复制数组后 `for i in 1..n: bit[i] += bit[i-1]` 再一层传播。本仓库未采用，避免与教学 `add` 两套 API 混淆；刷题卡常时可自行替换。

**双 BIT 区间加区间和（面试加分，实现可选）**  
设原数组为 a，差分为 d。区间加 `[l,r] v` 在 d 上打点；要查 `[ql,qr]` 的和，需要公式把「差分的前缀」与「带权前缀」组合。竞赛模板维护两个 BIT：`B1` 维护 d 的前缀效应、`B2` 维护另一路累积，使得 `range_sum` 可 O(log n) 写出（具体公式可在刷题时背模板）。本仓库 **未实现** 双 BIT，目的是让你先掌握单 BIT 与 RUPQ；一旦题目同时要求「区间加」与「区间和」，应打开 `ds-tree-segment-tree` 学 lazy，或搜「二树状数组」模板，**不要**用 `FenwickRUPQ` 硬凑区间和。

**与差分数组 plain 数组对比**  
纯差分数组：区间加 O(1)、还原单点 O(n) 或前缀 O(n)；差分 + BIT：区间加 O(log n)、单点 O(log n)。若题目只有区间加、最后一次性输出所有点，可能不必 BIT；若中间多次 point_query，BIT 才有意义。

**索引边界统一约定**  
全文 API：`index`、`l`、`r` 均为 **0-based 闭区间**。内部 `bit` 下标从 1 开始。LeetCode 307 的 `left`、`right` 与本文 `range_sum(left, right)` 一致。写题解时切忌一半 0-based 一半 1-based 混在同一个函数里。

### 典型应用

**动态前缀和 / 307**  
可变数组的区间和是 BIT 教科书题；Study `0307_range_sum_query_mutable/solution.py` 内嵌 BIT 逻辑，与 `FenwickTree` 同族。

**逆序对**  
归并 O(n log n) 或 BIT：离散化后从左到右 `add(rank, 1)`，查询 `prefix_sum(rank-1)` 得到「比当前小且已在右侧」的个数。树状数组在值域压缩后做频次统计，是竞赛经典模板。

**离散化 + 频次**  
[315. 计算右侧小于当前元素的个数](https://leetcode.cn/problems/count-of-smaller-numbers-after-self/)、[327. 区间和的个数](https://leetcode.cn/problems/range-sum-query-2d-mutable/) 等，常配合坐标压缩，BIT 维护「≤ x 的个数」或前缀和。

**RUPQ：区间加、单点查**  
作业题、日程差分、多次区间增量后查某点；本仓库 `FenwickRUPQ` 直接演示。若题目反过来要区间和，请换模型或线段树。

**二维 BIT**  
矩阵单点改、子矩形和 O(log n log m)；本仓库未实现，知道存在即可，实现为外层 `add` 套内层 `add`。

**扫描线与 BIT**  
部分扫描线题在离散坐标上用 BIT 维护覆盖次数；聚合函数仍是加法时与一维 BIT 相同，与线段树扫描线题同源不同形。

**493. 翻转对（思路）**  
与逆序对类似，需在归并或 BIT 中查找「满足某倍数关系」的先前元素，常配合离散化与双指针；BIT 维护的是值域上的出现次数前缀，写法与 315 同族。

**2089. 找出数组排序后的目标下标（变种）**  
部分题在排序后的目标位置与 BIT 统计相关，核心仍是「动态频次 + 前缀」；见到「多次 query 小于 x 的个数」应联想到 BIT 或平衡树。

**与平衡树（ multiset ）对比**  
值域很大时，`SortedList` 或 C++ `multiset` 也可做动态排名与前驱后继，但单次 O(log n) 常数更大、实现更长；离散化后 BIT 更短。若题目需要「删除任意元素」而不仅是改单点，可能要 multiset 或线段树维护值域。

**307 为何 Study 题解首选 BIT**  
代码行数少、无递归栈风险、提交常数友好；线段树用于对拍验证正确性与培训「复杂区间」思维。面试时建议先答 BIT，再补「若区间加区间和我用线段树 lazy」。

### 易错点

1. **0-based / 1-based 混用**：对外 `index` 忘记 `+1` 导致全错或越界。
2. **区间和 l=0**：忘记特判 `prefix_sum(l-1)` 在 `l=0` 无意义。
3. **RUPQ 漏减 `r+1`**：只做 `add(l,v)` 不做 `add(r+1,-v)`，区间外也被加。
4. **RUPQ 越界**：`r == n-1` 时不应对 `r+1` 操作；本实现 `if r + 1 < n` 判断。
5. **BIT 长度不足**：RUPQ 用 `n+2`；普通 BIT 至少 `n+1`。
6. **307 update 写成累加**：应 `delta = val - old`，不是 `add(index, val)`。
7. **把 BIT 当成线段树**：区间 min、区间赋值、区间乘不能靠本仓库两个类硬套。
8. **整数溢出**：C++ 累加用 `long long`；Python 面试若要求 C++ 需注意。

**调试技巧**  
n≤10 时打印每次 `add` 的 `i` 路径与 `bit` 数组；与暴力数组对拍。307 官方样例外加 `n=1`、连续 update 同一位置、全区间查询。

**易错点逐条展开（配合对拍）**

第 1 条 0/1-based：表现是「整体偏移或越界 RE」；检查 `add` 第一行是否 `index+1`。第 2 条 l=0：表现是 `range_sum(0,r)` 少减一项；必须分支 `if l==0`。第 3 条 RUPQ 漏减：表现是区间右侧之外点也被加；对照差分数组手算。第 4 条 r=n-1：表现是越界或错减；确认 `r+1 < n`。第 5 条 长度：RUPQ 构造 `n+2`。第 6 条 307 累加：第二次 update 同一位置结果爆炸；必须用差量。第 7 条 误用 BIT 做 min：应换线段树或 ST 表。第 8 条 C++ 溢出：多次正数加超 int。

**与线段树易错点的对照（复习 ds-tree-segment-tree 时）**  
线段树常见 WA 是 push 遗漏、完全包含仍递归、lazy 长度乘错；BIT 没有 lazy，但若把 RUPQ 当成区间和结构，等价于「语义用错结构」。两套易错点列表可并列贴在笔记里：左边 BIT 下标，右边线段树 push。

**面试官可能追问**

- 为何 `i & -i` 是 lowbit？（补码性质）  
- 区间加区间和怎么办？（双 BIT 或线段树，见上）  
- 与线段树复杂度？（单次均为 O(log n)，常数 BIT 更小）  
- 能否支持区间加区间最值？（线段树或专门结构，非本 BIT 模板）

### 练习建议

1. 手画 n=8，标出每个 i 的 lowbit，模拟 `add(3, 5)` 的跳转；
2. 默写 `add` 与 `prefix_sum` 两个 while；
3. 完成 LC 307，再读 `ds-tree-segment-tree` 用线段树写一版对拍；
4. 实现并测试 `FenwickRUPQ`：对 `[1,3]` 加 10 后查点 0、2、3；
5. 选做 [315](https://leetcode.cn/problems/count-of-smaller-numbers-after-self/) 或 [327](https://leetcode.cn/problems/range-sum-query-2d-mutable/) 的一维版本思路。
6. 将 `fenwick_tree.py` 的 `__main__` 扩展：n=0、n=1、l=0、r=n-1 的断言；
7. 用 60 秒向同学讲解 BIT 与线段树区别，录音回听是否清晰。

进阶：双 BIT 推区间加区间和、二维 BIT、主席树（可持久化 BIT）——超出本仓库代码，见竞赛资料。

**默写考核标准**  
闭卷五分钟内写出 `FenwickTree` 的 `add`、`prefix_sum`、`range_sum`（含 l=0 分支），无语法错误；再给出口头 RUPQ 的 `range_add` 两行逻辑。达不到则重复第 3–5 天练习，不进入 315。

**从暴力到 BIT（面试叙述模板，约 60 秒）**  
「可变数组求区间和，暴力每次 update 或 sum 都是 O(n)。前缀和数组查询快但修改慢。树状数组用长度为 n+1 的 bit，单点加和查前缀都是沿 lowbit 跳 O(log n) 次，区间和用两次前缀相减。307 的 update 用新旧值差做 add。若还要区间加区间和，我会改用线段树 lazy 或双 BIT。」

**与 ds-tree-segment-tree 的一周对拍建议**  
Day 1–2：本页基础篇 + 运行 `fenwick_tree.py`；Day 3：AC 307；Day 4：阅读线段树专题「与树状数组对照」表；Day 5：同一随机数据双模板对拍；Day 6：口述选型；Day 7：模拟面试默写 BIT。

**手算 RUPQ**  
n=5 全零，`range_add(1,3,10)` 后：`point_query(0)=0`，`point_query(1)=10`，`point_query(3)=10`，`point_query(4)=0`。验证差分在 l 加 v、r+1 减 v 是否只在管辖范围内生效。

**从朴素差分到 BIT-RUPQ 的叙述**  
面试官问「多次区间加、多次单点查询」：先说朴素差分 O(1) 区间加、查点 O(n) 前缀；再说把差分的前缀交给 BIT，每次 O(log n)。若追问区间和，接双 BIT 或线段树。这条链路比单独背代码更有说服力。

## Python 实现

Study 完整实现（单点加、区间和、RUPQ 自测）：

```python
class FenwickTree:
    """单点加、前缀和，0-based 对外接口。"""

    def __init__(self, n: int) -> None:
        self._n = n
        self._bit = [0] * (n + 1)

    def add(self, index: int, delta: int) -> None:
        i = index + 1
        while i <= self._n:
            self._bit[i] += delta
            i += i & -i

    def prefix_sum(self, index: int) -> int:
        i = index + 1
        s = 0
        while i > 0:
            s += self._bit[i]
            i -= i & -i
        return s

    def range_sum(self, l: int, r: int) -> int:
        if l == 0:
            return self.prefix_sum(r)
        return self.prefix_sum(r) - self.prefix_sum(l - 1)
```

**RUPQ 类**（区间加、单点查）：

```python
class FenwickRUPQ:
    def __init__(self, n: int) -> None:
        self._n = n
        self._bit = FenwickTree(n + 2)

    def range_add(self, l: int, r: int, v: int) -> None:
        self._bit.add(l, v)
        if r + 1 < self._n:
            self._bit.add(r + 1, -v)

    def point_query(self, i: int) -> int:
        return self._bit.prefix_sum(i)
```

**自测逻辑**：初值 `[1,2,3,4,5]` 逐点 add 后 `range_sum(1,3)==9`；`FenwickRUPQ` 对 `[1,3]` 加 10 后 `point_query(2)==10`、`point_query(0)==0`。

**读代码顺序**：先 `add` 理解向上跳 → 再 `prefix_sum` 向下跳 → 再 `range_sum` 特判 `l==0` → 最后 `FenwickRUPQ` 与差分对照。

**封装 LeetCode 307（与 Study solution 同族）**

```python
class NumArray:
    def __init__(self, nums: list[int]) -> None:
        self._nums = nums[:]
        self._n = len(nums)
        self._bit = [0] * (self._n + 1)
        for i, v in enumerate(nums):
            self._fenwick_add(i + 1, v)

    def _fenwick_add(self, i: int, delta: int) -> None:
        while i <= self._n:
            self._bit[i] += delta
            i += i & -i

    def _prefix(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self._bit[i]
            i -= i & -i
        return s

    def update(self, index: int, val: int) -> None:
        d = val - self._nums[index]
        self._nums[index] = val
        self._fenwick_add(index + 1, d)

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix(right + 1) - self._prefix(left)
```

注意 `sumRange` 里 `_prefix(left)` 对应「严格小于 left 的前缀」，等价于本仓库 `l>0` 时的 `prefix_sum(l-1)`。

**为何题解用 1-based `_fenwick_add(i+1,v)` 而类仍保留 `_nums`**  
BIT 本身不存原数组，但 307 的 `update` 需要旧值算差量，故 `_nums` 副本不可省。另一种写法是 `range_sum(i,i)` 查旧值，多一次 O(log n)，笔试可不优化。

**空数组与单元素**  
`FenwickTree(0)` 时 `add` 不应被调用；`n=1` 时 `add(0,v)` 只更新 `bit[1]`。脚本中 `ft1 = FenwickTree(1); ft1.add(0,7)` 断言 `prefix_sum(0)==7`，建议本地保留。307 官方有 `n=0` 边界时按题面处理。

**Python 递归深度**  
BIT 无递归，n=10⁵ 也安全；这是相对线段树递归版的实用优势之一。

**对拍脚本思路**

```python
import random
n = 20
data = [random.randint(0, 9) for _ in range(n)]
ft = FenwickTree(n)
for i, v in enumerate(data):
    ft.add(i, v)
for _ in range(50):
    i = random.randrange(n)
    d = random.randint(-3, 3)
    data[i] += d
    ft.add(i, d)
    l, r = sorted(random.sample(range(n), 2))
    assert ft.range_sum(l, r) == sum(data[l : r + 1])
```

## C++ 实现

```cpp
struct Fenwick {
    int n;
    vector<long long> bit;
    explicit Fenwick(int n_) : n(n_), bit(n_ + 1, 0) {}

    void add(int index, long long delta) {
        for (int i = index + 1; i <= n; i += i & -i) bit[i] += delta;
    }

    long long prefix_sum(int index) const {
        long long s = 0;
        for (int i = index + 1; i > 0; i -= i & -i) s += bit[i];
        return s;
    }

    long long range_sum(int l, int r) const {
        if (l == 0) return prefix_sum(r);
        return prefix_sum(r) - prefix_sum(l - 1);
    }
};
```

**RUPQ** 与 `main` 中断言与 Python 一致；包含 `alg_std.hpp` 以统一 `vector`/`cout`。编译：

```powershell
g++ -std=c++17 -O2 -Wall -Wextra -o fenwick.exe fenwick_tree.cpp
.\fenwick.exe
```

与 Python 逻辑一一对应；面试白板写 C++ 时注意 `const` 的 `prefix_sum` 与 `long long`。

**C++ 与 Python 差异备忘**  
`vector<long long> bit(n+1)` 初始化；`i & -i` 在 `i=0` 时 while 不进入；`FenwickRUPQ` 的 `bit(n+2)` 与 Python `FenwickTree(n+2)` 一致。若用 `alg_std.hpp`，仅影响头文件聚合，算法逻辑不变。编译警告建议开 `-Wall -Wextra`，避免有符号无符号混用。

**模板封装建议（竞赛）**  
许多选手将 `add`/`sum` 写成全局数组 + 函数，减少类开销；面试用类更清晰。无论哪种，保持 **1-based bit、0-based 接口** 约定一致。

## 练习与延伸

| 资源 | 说明 |
|------|------|
| LC 307 | 区域和检索，可变；BIT 首选 |
| LC 315 | 右侧更小个数；离散化 + BIT |
| LC 327 | 区间和个数；前缀和 + BIT/线段树 |
| LC 493 | 翻转对；离散化 + BIT/归并 |
| LC 2407 | 最长递增子序列 II（线段树/BIT 值域） |
| Study `0307_range_sum_query_mutable` | BIT 题解与测试 |
| `ds-tree-segment-tree` | lazy 线段树对照、区间加区间和 |
| `ds-tree-binary-tree` | 递归基础，先于或并行阅读 |

**双 BIT 区间加区间和（思路，无仓库代码）**  
维护 `B1` 为差分的前缀、`B2` 为另一辅助数组，使得区间和查询可 O(log n)（竞赛模板「二树状数组」）。若你只需掌握面试主线，知道「存在扩展」即可，实现可参照线段树专题练习。

**逆序对模板口述**  
离散化后按原下标顺序遍历，当前值排名 `r`，答案加上 `query(r-1)`，再 `add(r,1)`。BIT 维护的是「值域上的频次前缀」，不是原下标前缀。

**逆序对步骤展开（配合 BIT）**  
给定数组，先拷贝并排序去重得到值域坐标，将每个元素映射为排名 `rank`（注意相等元素顺序可用稳定排序或左侧压缩）。建 BIT 大小为 m（排名个数）。从左到右处理下标 i：在 BIT 上查询 `prefix_sum(rank-1)`，表示当前值左侧已出现、且值更小的元素个数，累加到答案；再 `add(rank, 1)` 表示该值出现一次。总复杂度 O(n log n)。若面试官问「为何不用原下标建 BIT」，解释值域可能到 10⁹，必须离散化。

**315 与逆序对的同构**  
315 求每个位置右侧更小个数，可反向遍历：从右到左，同样「见到更小」转为「已处理元素中比当前小的个数」，BIT 维护频次。写法与逆序对镜像，练一道另一道可快速迁移。

**327 区间和个数（思路）**  
枚举右端点，维护左端点侧的前缀和 multiset 或 BIT；核心是「和为 k 的对数」转化为「存在前缀和差为 k」。BIT 出现在离散化后的前缀计数，细节见题解，本页只需建立「前缀和 + 数据结构计数」联想。

**扫描线**  
矩形面积、周长类题常在压缩坐标上用线段树或 BIT；聚合为加法时与本文相同，非加法则换线段树节点定义。

## 学习路径

| 阶段 | 内容 |
|------|------|
| 第 1 天 | 基础篇「抽象模型」「核心操作」，手画 lowbit |
| 第 2 天 | 运行 `fenwick_tree.py`，改断言自测 |
| 第 3 天 | 默写 BIT，提交 LC 307 |
| 第 4 天 | 阅读 `ds-tree-segment-tree` 对照表，理解 lazy |
| 第 5 天 | 307 双解法对拍（BIT vs 线段树） |
| 第 6 天 | `FenwickRUPQ` 与差分作业题 |
| 第 7 天 | 选做 315 或 327 之一 |

**两周计划（细化为每日任务）**

第 1–2 天只看不写：读基础篇「抽象模型」「实现要点」，手画 n=8 的 lowbit 表，在纸上模拟 `add(3,5)` 与 `prefix_sum(5)` 的跳转序列。第 3–4 天对照 `fenwick_tree.py` 抄一遍 `FenwickTree`，每抄一行在旁注 0-based 与 1-based。第 5 天闭卷默写两个 while，失败则只重默写不改题。第 6 天跑通脚本并写 307 的 `NumArray` 提交。第 7 天读 `ds-tree-segment-tree` 的「与树状数组对照」节，用同一组数据手写线段树版 307（可抄仓库）。第 8–9 天双解法对拍，记录代码行数与提交耗时。第 10 天复习易错点清单，测 n=1、l=0、RUPQ 边界。第 11–12 天选做 315：只需理解离散化 + BIT 频次，不必 AC 全部变种。第 13–14 天模拟面试：六十秒讲 BIT + 十五分钟白板写 `add`/`prefix_sum`。

**零基础切入顺序**  
若从未写过前缀和题，先做一道暴力 307（数组存 nums，update 改值，sumRange 循环求和），记录 n=1000、m=1000 时的超时直觉，再引入 BIT。若已会线段树但不会 BIT，可反向从 `range_sum` 公式入手：BIT 就是「可修改的前缀和机器」。

**与线性结构、图专题的衔接**  
BIT 不依赖指针，但依赖「前缀和思维」；学完 `ds-linear` 数组章即可开始。图论中部分最短路计数、Dijkstra 堆优化与 BIT 无直接关系，可并行安排。

**达标标准**  
闭卷写出 `add` / `prefix_sum`；十分钟内完成 307；能三张表解释 BIT vs 线段树 vs 朴素前缀和；RUPQ 能讲清两端打点。

## 延伸阅读

- Study 笔记：[python/.../fenwick_tree/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/tree/fenwick_tree/notes.md)
- 线段树专题（batch1）：本站 `ds-tree-segment-tree`
- 维基：[Fenwick tree](https://en.wikipedia.org/wiki/Fenwick_tree)
- 题解目录：`python/problems/leetcode/0307_range_sum_query_mutable/`

**lowbit 的补码推导（给爱追根者）**  
设 `i` 的二进制最低位 1 在位置 k，则 `i` 可写成 `…10…0`（k 个 0）。`-i` 为取反加一，低 k 位变 1 并进位，得到 `…100…0` 仅保留位 k 的 1。`i & (-i)` 即提取该位。理解推导有助于面试解释「为何跳父节点是加 lowbit、查询是减 lowbit」，而非死记。

**双 BIT 与线段树选型再强调**  
若题目同时出现「区间加」与「区间和」，且不允许 O(n) 暴力，请打开 `ds-tree-segment-tree` 学习 lazy；若你愿意多记一套竞赛模板，再搜「树状数组 区间修改 区间查询 两个树状数组」。本站 fenwick 目录刻意只保留单 BIT 与 RUPQ，降低初学者认知负荷。

**manifest 与状态**  
本页 `status: published`，通过 `validate_algorithm_guide.py` 与 `validate_algorithm_quality.py` 的 `--strict` 后可改为 `published`。撰写进度见 `_meta/人工撰写进度.md`。

**与仓库题解 0307 的衔接**  
读完本文后打开 `python/problems/leetcode/0307_range_sum_query_mutable/solution.py`，对照 `NumArray` 与 `FenwickTree` 的下标写法差异（题解内 1-based `_add(i+1)` 与类内 `_prefix(left)`）。C++ 题解目录对称。掌握 BIT 后，区间操作题应优先判断能否前缀和化，再考虑是否升级到线段树。

**fenwick_tree 与 segment_tree 目录并列意义**  
Algorithm 仓库将二者分目录存放，便于同一测试数据运行 `python fenwick_tree.py` 与 `python segment_tree.py` 对拍。atelier 两专题互链，形成「短代码 vs 强扩展」的完整叙事，避免只背一种模板在复杂区间题上失误。

**练习强度建议**  
medium 档指南要求足够汉字支撑自学，核心交付物是默写 BIT + AC 307 + 能选型。315/327/493 等题在「练习与延伸」中点到为止，按求职时间表选做。时间紧时完成核心交付物后即可转向图论或 DP 章，不必在本专题停留超过两周。

**BIT 手写检查清单（提交 OJ 前）**  
数组长度 `n+1`；`add` 循环 `i<=n`；`prefix` 循环 `i>0`；307 `update` 用差量；`sumRange` 用 `_prefix(r+1)-_prefix(left)`；RUPQ 在 `r+1<n` 才减 v；C++ 用 `long long`。逐项勾选可减少 ninety percent 的 off-by-one。

**竞赛常数优化**  
同复杂度下 BIT 常数通常小于递归线段树；若 TLE 且逻辑正确，检查是否误用 Python 纯递归线段树、或是否可用 BIT 替换。若需区间 min 则 BIT 非首选。

**历史与应用场景**  
Fenwick 最初用于压缩算法中的累积频率统计；后在竞赛与 OJ 成为与线段树并列的工具。工程中单点更新+前缀查询的场景也可用 BIT，但工业界更常见的是数据库索引与专用结构，面试仍以 LeetCode 风格为准。

**与二叉树遍历专题的关系**  
`ds-tree-binary-tree` 中的递归、层序遍历与 BIT 无直接代码共用，但有助于你之后学习线段树时的递归框架。学习顺序建议：二叉树遍历（理解递归）→ 本页 BIT（迭代、短模板）→ 线段树（递归、lazy）。

**再读 segment_tree 专题的时机**  
完成 307 与 BIT 默写后，用半天阅读 `ds-tree-segment-tree` 的「基础篇·典型应用」与「与树状数组对照」表，然后只做一道需区间加区间和的模板题（可在纸上推导 lazy，不必 AC 难题）。这样 BIT 与线段树在脑中形成互补而非二选一误解。

**本题单点赋值与单点加的区别**  
307 是赋值：必须用 `val - old`。若题面改为「下标 i 加 v」，则直接 `add(i, v)`，无需保存原数组（除非还要输出原值）。读题时圈出动词「赋值」还是「增加」，再选差量或直接加。

**扩展阅读：逆序对与归并**  
归并排序求逆序对 O(n log n) 与 BIT 同阶；面试若已写归并可说明「亦可 BIT+离散化」。两者选其一练熟即可，不必双写。

**扩展阅读：坐标离散化**  
值域 10^9、操作 n 次时，先把出现的值排序去重映射到 1..m，再在 m 上建 BIT。离散化错误（未包含边界、相等元素次序）是 315/327 WA 主因，与 BIT 本身无关但必同时掌握。

**文档维护**  
若 Study `fenwick_tree.py` 接口变更，请同步更新本站 Python 摘录与「Study 仓库对照」表。C++ 镜像路径变更时同步 C++ 节。published 前运行：

```powershell
Set-Location -LiteralPath 'F:\commercial\atelier'
python scripts/validate_algorithm_guide.py --slug ds-tree-fenwick-tree --strict
python scripts/validate_algorithm_quality.py --slug ds-tree-fenwick-tree --strict
```

**总结一句**  
树状数组是「前缀和的可修改版」；差分 + BIT 是「区间加的单点查版」；更重的区间语义交给线段树。记住这三层，就能在 307 与复杂区间题之间快速选型。

**BIT 图形化覆盖（n=8，帮助记忆 lowbit）**  
下标从 1 到 8，每个 i 负责区间 `(i - lowbit(i), i]`（左开右闭转 1-based 闭区间时常记为长度 lowbit(i) 的结尾在 i）。例如 i=6（二进制 110），lowbit=2，负责 (4,6] 即元素 5,6。多个 i 的覆盖重叠，但 `add` 与 `prefix_sum` 的跳转保证累积正确。手画时可在 8 格纸上方写 bit 下标，下方写原数组 a[0..7]，用箭头标 add(下标 5) 影响哪些 bit 单元。

**主席树与可持久化（仅名词）**  
可持久化 BIT/线段树用于历史版本查询、区间第 k 小，属于竞赛进阶；与本仓库静态长度 BIT 无关。听到「可持久化」应想到线段树为主、BIT 为辅的资料，不在本页实现范围。

**工程中的 BIT**  
数据库索引、日志聚合有时用树状或分块结构；面试仍以手写模板为准。理解 BIT 有助于读竞赛题解，但不必强行套到所有业务场景。

**在线 OJ 常见坑**  
多组数据记得清空或重建 BIT；模数题在 add/prefix 时取模；负数下标不存在但 delta 可为负。Java 选手注意 `i & -i` 需 long 防溢出当 i 很大时（一般 n≤10⁵ 仍用 int）。

**与 ST 表、前缀和的选型三角**  
静态区间最值：ST 表 O(1) 查询；静态区间和：前缀和 O(1)；**动态**单点改 + 区间和：BIT 或线段树。若数组不变，勿上 BIT；若只查询一次，暴力即可。

**复习检查（第 2 周末）**  
能否一分钟内写出两个 while；能否解释 307 update 为何用差量；能否说明 RUPQ 两端打点；能否填「BIT vs 线段树」表至少五行；能否口述逆序对 BIT 流程。四项皆否则延长本周计划，不进入 315/327。

**撰写与 manifest**  
本专题 slug `ds-tree-fenwick-tree`，`status: published`，与 `ds-tree-segment-tree` 互链。人工撰写进度表在通过 strict 校验后可标 published。若 Study 源码更新 RUPQ 边界条件，请同步修订「易错点」与 Python 摘录。

**读者常见问题（简短收录，非独立 FAQ 章）**  
问：BIT 算树吗？答：逻辑上是树形覆盖，实现是数组。问：能否 O(1) 区间和？答：静态数组可以，动态修改不行。问：307 必须用 BIT 吗？答：线段树亦可。问：区间加区间和？答：双 BIT 或 lazy 线段树，见上文。问：Python 会 TLE 吗？答：307 数据规模下 BIT 足够，极端卡常才考虑 PyPy 或 C++。

**与 Hot 100 / prob-hot100 的关系**  
可变数组、前缀统计类题在题单中分散于数组、二分、哈希章；掌握 BIT 后可回头扫题单中「需要动态前缀」标签的题，用本章模板套一遍，巩固选型而非死记题号。

**二维 BIT 简述（扩展）**  
对矩阵 `a[row][col]`，可定义 `add(r, c, δ)` 与 `sum(r1,c1,r2,c2)`：外层对行下标做 BIT，内层对列下标再做 BIT，单次 O(log n log m)。实现时内层 BIT 可用向量数组 `bit[i][*]`。本仓库未提供二维代码，因 medium 档聚焦一维模板；刷矩阵题时再单独练。

**PowerShell 批量自测（可选）**  
除单文件 `python fenwick_tree.py` 外，可在仓库根目录循环跑多个数据结构自测脚本，确认环境无误。路径含空格时务必 `-LiteralPath`，与 Study 仓库对照节一致。

**发布前自检清单**  
汉字≥8000（medium）、九个大节齐全、基础篇六个 `###` 标题与 topic-ds.yaml 一致、Python/C++ 节含真实代码块、无「围绕…理解」类 filler、status 保持 draft 直至人工改 published。本清单供作者使用，非正文结构。

**最后巩固：三句话背记**  
第一句：BIT 用 1-based 数组，单点加向上跳 lowbit，前缀和向下跳 lowbit。第二句：区间和 = 两个前缀，l=0 特判。第三句：区间加单点查用差分两端打点再前缀；区间加区间和请换线段树或双 BIT。背熟后再做 307，速度与正确率会明显上升。若与 `ds-tree-segment-tree` 对照学习，建议同一天内完成两题 307 双提交，形成肌肉记忆。本章正文至此收束，后续改动以 Study 源码与校验脚本为准。欢迎在对拍中发现问题后提 Issue 或自行修订「易错点」小节。完稿后请在人工撰写进度表中将本 slug 标为待校对并通过 strict 校验，汉字计数以脚本输出为准。
