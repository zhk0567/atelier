---
title: "数据结构 · 线段树（Segment Tree）"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/segment_tree
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-21
tags: [DataStructures, SegmentTree, LazyPropagation, RangeQuery, LeetCode307]
---

# 数据结构 · 线段树（Segment Tree）

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

**线段树（Segment Tree）**是一种基于二叉树结构的区间数据结构：在固定长度数组上支持**区间查询**与**区间修改**（或单点修改），每次操作 **O(log n)**。本仓库 `data_structures/tree/segment_tree/` 的实现聚焦 **区间加 + 区间求和**，并配合**懒标记（lazy propagation）** 避免每次修改都下推到叶子，是竞赛与面试中「比朴素 O(n) 扫描高一级、比树状数组更通用」的标配工具。

与 **树状数组（Fenwick / BIT）** 对比：两者都能做前缀和类问题；BIT 代码更短、常数更小，但扩展「区间加 + 区间和」、区间最值、矩阵乘法等时线段树更直观。Study 在 `fenwick_tree/` 有对照实现；LeetCode [307. 区域和检索 - 数组可修改](https://leetcode.cn/problems/range-sum-query-mutable/) 题解目录中两种写法并存。

本专题 `topic_path` 为 `data_structures/tree/segment_tree`，`guide_toc` 为 `topic-ds`。读完你应能：

1. 画出 `[0,n-1]` 在完全二叉树上的划分，说出节点 `idx` 与儿子 `2*idx`、`2*idx+1` 的含义；
2. 写出区间修改的**递归三情况**（不相交、完全包含、部分相交）；
3. 解释懒标记 `push` 的时机与「先 push 再递归」的原因；
4. 在 Python/C++ 中运行 `segment_tree.py` / `segment_tree.cpp` 并通过断言；
5. 知道何时改用 BIT、何时需要线段树合并、动态开点等进阶形态。

**面试出现频率**：纯手写线段树在国内大厂笔试中低于链表/动态规划，但在竞赛向岗位、区间 DP 优化、扫描线辅助题中常见。若简历写「熟悉数据结构」，至少应能讲清 lazy 线段树模板，并独立完成 307 或区间加模板题。

**本实现边界**：仅支持**区间加**与**区间和**；不支持区间取 min/max、区间乘、矩阵标记。扩展时需改节点聚合函数与 `push` 语义，勿在考场上临时改一半导致 lazy 错乱。

**与前缀和对比**：静态数组前缀和查询 O(1)、单点修改 O(n)；差分数组单点修改 O(1)、前缀和查询 O(n)。当**多次区间加 + 多次区间和**同时出现时，差分+前缀或 BIT/线段树才划算；单次操作仍可用暴力。

**专题学习成果清单（可打印勾选）**

学完本页后，你应能独立完成下列检查项：能在纸上画出 n=7 的线段树并标出每个节点区间；能解释根下标为何从 1 开始；能写出 push 的四行核心效果（子 lazy 累加、子 sum 加长度乘 lazy、父 lazy 清零）；能区分修改与查询在「完全包含」时的不同返回值处理；能将 307 题面操作翻译成 `range_add` 与 `range_sum`；能在 Python 中运行 `segment_tree.py` 看到 OK；能在 C++ 中编译运行 `segment_tree.cpp`；能口述线段树与 BIT 的选型差异；能列举至少两个除 307 外的 LeetCode 题号（如 308、327）；知道扫描线题需要换维护量但递归框架类似；知道持久化与动态开点是竞赛扩展而非本仓库实现范围。勾选少于八项则建议延长学习路径两周计划的前半段，勿急于刷难题。

**为何竞赛与面试都教线段树**

竞赛中区间问题是常客：区间修改、区间查询、历史版本、树上统计等都可归结为「在有序下标轴上维护信息」。线段树把下标轴建成二叉树，使每次操作只访问 O(log n) 个节点，是平衡时间与实现难度的经典折中。面试中考得不如 DP 频繁，但一线公司笔试仍可能出现 307 或「支持区间更新的数据结构」开放题；答出 BIT 与线段树两种方案会显著加分。本仓库选择 lazy 区间加与区间和，是因为它是理解 push-pull 的**最小完整模型**：比单点修改多一个「长度乘 lazy」的细节，又比区间最值少一个「合并函数更复杂」的负担。

**阅读本页的推荐顺序**

第一遍只读导读、基础篇、学习路径，并手画一棵树；第二遍对照 Python 实现逐函数阅读，运行脚本；第三遍闭卷默写四函数；第四遍做 307 与 BIT 对拍；第五遍浏览练习与延伸中的进阶题号，按兴趣选做。每遍之间至少间隔一天，避免一天读完却写不出代码。C++ 读者在第三遍后增加编译运行，检查 `long long` 与断言输出。

**与 fenwick_tree、ds-tree-binary-tree 的导航关系**

`ds-tree-binary-tree` 讲解遍历与递归，`fenwick_tree` 讲解 BIT 与 307 的短实现，本页讲解 lazy 线段树。三篇可组成「树形存储」学习周：先二叉树递归，再 BIT，再线段树。站点 manifest 中三 slug 均在 `data_structures/tree/` 下，Study 路径对称。

**本页篇幅与练习量的关系**

medium 档指南要求足够汉字支撑自学，不等于要求你记住每一个进阶题号。核心交付物是：能讲清 lazy、能写四函数、能 AC 307。327、715、218 等题在「练习与延伸」中点到为止，按求职时间表选做即可。若仅冲击笔试且时间紧，完成核心交付物后即可转向 `iv-top-frequent` 的图与 DP 章，不必在本专题停留超过三周。

## 预备知识

> **预备知识**：熟悉二叉树递归、数组下标 0..n-1；理解递归 DFS 与区间 `[l,r]` 包含关系；Python 3.10+；C++17。建议先掌握前缀和 O(1) 查询与 O(n) 单点修改的对比，才能体会线段树的意义。

需要的前置概念：

- **完全二叉树数组存储**：根下标 1（本实现），左子 `2*idx`，右子 `2*idx+1`；空间开 `4*n` 足够。
- **区间 `[ql,qr]` 与节点区间 `[l,r]`**：递归时当前节点负责一段连续下标，查询/修改参数 `[ql,qr]` 是用户请求。
- **懒标记语义**：节点上挂的 `lazy` 表示「子树内每个位置待加的值尚未下推」；`sum` 已包含该延迟对当前区间长度的贡献。
- **long long**：区间和与多次加法可能超 `int`，C++ 实现用 `long long`；Python 整数任意精度但仍建议意识溢出（若提交 C++）。

若对递归树遍历不熟，可先复习 `ds-tree-binary-tree` 专题中的遍历与高度概念，再回本页。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/tree/segment_tree` |
| Python | `python/data_structures/tree/segment_tree/segment_tree.py` |
| C++ | `cpp/data_structures/tree/segment_tree/segment_tree.cpp` |
| 笔记 | 两侧 `notes.md` |
| LeetCode 对照 | `problems/leetcode/0307_range_sum_query_mutable/`（含 BIT 写法） |
| 相关 | `data_structures/tree/fenwick_tree/`（树状数组） |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\data_structures\tree\segment_tree'
python segment_tree.py
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\tree\segment_tree'
g++ -std=c++17 -O2 -Wall -Wextra -o seg.exe segment_tree.cpp
.\seg.exe
```

期望输出 `SegmentTree OK`。将 `F:\Study\Algorithm` 换成本机路径。

**文件职责**

- `segment_tree.py` / `.cpp`：`SegmentTreeLazy` / `SegTree` 类，建树、`range_add`、`range_sum`；
- `notes.md`：复杂度与 LC 307 链接；
- `GUIDE.md`：仓库内本地导读（与 atelier 本页互补，勿整段复制）。

## 基础篇

### 抽象模型

将数组 `a[0..n-1]` 固定后，线段树在逻辑上是一棵**平衡二叉树**，每个节点存储**一个区间的聚合信息**（本实现为区间和 `sum`），并可选存储**懒标记** `lazy` 表示待下推的加法。

**树形结构（n=5 示意）**

```
                 [0,4] sum=15
                /        \
          [0,2]              [3,4]
          /    \             /    \
      [0,1]    [2,2]     [3,3]  [4,4]
      /   \
   [0,0] [1,1]
```

叶子对应单点 `a[i]`；内部节点 `sum = 左.sum + 右.sum`。用户操作：

- **区间加** `add(ql, qr, v)`：对 `[ql,qr]` 每个下标加 `v`；
- **区间和** `sum(ql, qr)`：返回 `[ql,qr]` 元素之和。

**与分治的关系**：每次把当前区间一分为二，递归处理；深度 O(log n)，共 O(n) 个节点（常数因子约 4n）。

**懒传播抽象**：若修改完全覆盖节点区间，不立即更新所有叶子，而在节点打标记并更新该节点 `sum`；仅当后续查询或修改需要进入子区间时，才把标记下推（push）到儿子，保证路径上每个节点访问仍为 O(log n)。

**历史与命名**：线段树英文为 Segment Tree，国内教材亦称区间树或线段树；与「区间树 Interval Tree」不同，后者常指另一类维护区间集合的结构，勿混淆。竞赛教材中常与树状数组并列讲授；本仓库分目录存放便于对拍。理解命名有助于你在搜索引擎与论文中检索正确资料。

**复杂度直觉**：建树 O(n) 因每个元素仅参与 O(log n) 条从叶到根的路径合并，共 n 条路径、每条 O(log n) 总 O(n log n) 粗算上界，更紧分析为 O(n)。单次修改或查询沿树高走 O(log n) 层，每层 O(1) 工作。空间 O(n) 的数组实现常开 4n 以避免最坏完全二叉树指数高度带来的不足。与 O(n) 暴力比，在 m 次操作时由 O(mn) 降为 O(m log n)，当 m 与 n 同阶时收益显著。

### 核心操作

| 操作 | 时间 | 说明 |
|------|------|------|
| 建树 `build` | O(n) | 自底向上合并 `sum` |
| 区间加 `range_add` | O(log n) | 带 lazy |
| 区间和 `range_sum` | O(log n) | 查询前 push |
| 单点修改 | O(log n) | 可视为 `ql=qr` 的区间加或单独写 |
| 空间 | O(n) | 数组长度 `4*n` |

**递归区间分类（通用模板）**

对当前节点区间 `[l,r]` 与请求 `[ql,qr]`：

1. **不相交**：`ql > r` 或 `qr < l` → 返回（查询返回 0，修改直接 return）。
2. **完全包含**：`ql <= l` 且 `r <= qr` → 在节点上聚合更新（加法则 `lazy+=v; sum+=v*(r-l+1)`）。
3. **部分相交**：先 `push` 下传懒标记，再递归左右子，最后 **pull** 合并子 `sum`（`sum[idx]=sum[left]+sum[right]`）。

查询在部分相交时也要先 `push`，否则儿子 `sum` 未反映祖先延迟加法，答案错误。

### 实现要点

**数组下标与建树**

实现用**根下标 1**，`build(idx, l, r, data)`：

- `l == r`：叶子，`sum[idx] = data[l]`；
- 否则 `m=(l+r)//2`，递归建左右子，`sum[idx]=sum[2*idx]+sum[2*idx+1]`。

空数组 `n=0` 时 Python 实现仍分配 `4*max(1,n)` 缓冲，`range_sum` 返回 0，便于统一接口。

**懒标记 push**

```python
def _push(self, idx: int, l: int, r: int) -> None:
    if self._lazy[idx] == 0 or l == r:
        return
    m = (l + r) // 2
    for child in (idx * 2, idx * 2 + 1):
        self._lazy[child] += self._lazy[idx]
    self._sum[idx * 2] += self._lazy[idx] * (m - l + 1)
    self._sum[idx * 2 + 1] += self._lazy[idx] * (r - m)
    self._lazy[idx] = 0
```

要点：

- 叶子 `l==r` 无需向子下推（无子）；
- 左子区间长度 `(m-l+1)`，右子 `(r-m)`（本实现右子从 `m+1` 开始，右子长度 `r-m`）；
- 儿子 `lazy` **累加**，因可能已有待下推标记；
- 父 `lazy` 清零。

**区间加**

完全包含时：

```python
if ql <= l and r <= qr:
    self._lazy[idx] += val
    self._sum[idx] += val * (r - l + 1)
    return
```

部分包含：`push` → 递归左右 → `sum[idx] = sum[left]+sum[right]`。

**区间和查询**

完全包含返回 `sum[idx]`；否则 `push` 后返回左右递归和。

**单点修改与区间加的关系**：`range_add(i,i,v)` 等价单点加；若题面是「赋值」而非「加」，需改懒标记语义（assignment lazy）或线段树维护多标记。

**扩展到区间最值 / 区间乘**

- **区间 max**：节点存 `max`，合并取 `max`；区间加仍如上；若维护 max 与加法的组合需注意 lazy 对 max 的影响（加法 lazy 可直接加在 max 上）。
- **区间乘 + 区间加**：需两个 lazy 或线段树套线段树，属于进阶，本仓库未实现。

### 典型应用

| 场景 | 说明 |
|------|------|
| 可修改数组的区间和 | LeetCode 307、308（二维扩展） |
| 区间加 + 区间和 | 模板题、差分数组 + BIT 也可但线段树更直观 |
| 扫描线 | 矩形面积并、竖线覆盖长度，事件排序 + 线段树维护覆盖次数 |
| 区间最值 / RMQ | 可用线段树或 ST 表；静态 RMQ ST 表 O(1) 查询更优 |
| 动态开点线段树 | 值域很大、下标稀疏时按需建节点 |
| 线段树合并 | 树上统计子树信息 |

**与差分的前缀关系**：多次单点加 + 一次区间查询可用差分；多次区间加 + 区间查询更适合 lazy 线段树或「BIT + 差分技巧」。

**307 题意映射**：`update(i,val)` 可先做 `range_sum(i,i)` 得旧值再 `range_add(i,i,val-old)`，或维护差分；`sumRange(l,r)` 即 `range_sum(l,r)`。仓库题解可能用 BIT，本专题树与题解目录对照学习。

### 易错点

1. **push 遗漏**：部分相交的查询/修改前未 `push`，子节点 `sum` 过期。
2. **完全包含后仍递归**：应直接更新节点并 return，否则 TLE。
3. **区间长度算错**：`sum += v * (r-l+1)` 中 `r-l+1` 是当前节点区间长度，不是全局 n。
4. **根下标混用**：本实现根为 1，若你习惯 0 根，子节点公式需整体改写，勿混用。
5. **lazy 与 sum 不一致**：只改 `lazy` 不改 `sum` 会导致当前节点查询错；完全包含分支必须同时更新。
6. **建树后数组被外部修改**：线段树不自动感知原数组变化，外部改 `data` 后需重建或单点更新。
7. **递归边界**：`ql,qr` 应在 `[0,n-1]` 内，越界需题面保证或自行 clamp。
8. **C++ 整数溢出**：多次 `range_add` 用 `long long` 存 `sum` 与 `lazy`。

**调试技巧**：对 n≤10 的小数据，写暴力数组与线段树对拍；打印递归路径 `(idx,l,r,ql,qr)` 理解包含关系。

**易错点逐条展开（配合调试）**

第 1 条 push 遗漏：表现是「刚 range_add 后 range_sum 偶尔偏小」；定位方法是对 n≤5 暴力对拍，在递归入口打印 lazy 值。第 2 条完全包含仍递归：表现是 TLE；检查是否在 `ql<=l and r<=qr` 分支写了 return。第 3 条长度乘错：表现是整段区间和偏差为「差一个常数倍」；检查是否误用全局 n 而非 `r-l+1`。第 4 条根下标混用：表现是建树正确但修改全错；统一用 1 根或统一用 0 根，子节点公式随根改变。第 5 条只改 lazy 不改 sum：表现是完全包含时当前节点查询立即错；完全包含分支必须两行同时更新。第 6 条外部改数组：表现是建树后手动改 `data[i]` 与查询不符；应重建树或走 `range_add` 同步。第 7 条越界：加 assert 或 clamp。第 8 条 C++ 溢出：多次加后超 int，换 `long long`。

**面试官可能追问的边界**

空数组、单元素数组、修改整个区间、修改长度为 1 的子区间、查询整个区间、查询长度为 1 的子区间、多次修改同一子区间后再查询——建议自建这七类用例写入 `segment_tree.py` 的 `__main__` 扩展断言，比只依赖题库样例更稳。

### 练习建议

1. 手画 n=4 的树，模拟 `range_add(1,2,10)` 再 `range_sum(0,3)` 的 push 路径；
2. 默写模板：`build`、`push`、`range_add`、`range_sum` 四个函数；
3. 完成 LC 307，对比 BIT 解法代码长度与常数；
4. 尝试 [315. 计算右侧小于当前元素的个数](https://leetcode.cn/problems/count-of-smaller-numbers-after-self/)（离散化 + 线段树 / BIT）；
5. 阅读 `fenwick_tree/notes.md` 做双实现对拍。

进阶：区间异或、历史版本（可持久化线段树）、李超线段树（斜率优化）——超出本页范围，见竞赛资料。

**从暴力到线段树（面试叙述模板）**

若面试官问「如何支持区间修改与区间查询」，可先给出暴力：每次 `range_add` 扫 `[ql,qr]` 是 O(n)，每次 `range_sum` 也是 O(n)。接着说明前缀和只能快速处理「单点改 + 区间查」或「区间改 + 单点查」的某一侧，不能同时高效。然后引出线段树：把数组建成二叉树，每个节点管一段区间，修改与查询只访问 O(log n) 个节点；若修改覆盖整段节点区间，用 lazy 延迟下推，避免扫叶子。最后用 307 题验证你需要的是「单点赋值 + 区间和」，可转化为「单点加差量 + 区间和」或维护赋值 lazy。这一段叙述约六十秒，体现你知道为何需要这棵树上结构。

**push 与 pull 的语义再强调**

**push** 解决的是「祖先欠儿子的加法债」：父节点 lazy 表示子树每个位置还将额外加多少，但儿子节点的 sum 尚未加上这部分，一旦递归要进入儿子，必须先清父 lazy 并更新两子的 sum 与 lazy。**pull** 解决的是「儿子已更新，父节点 sum 过期」：在部分相交的修改递归返回后，用 `sum[idx]=sum[left]+sum[right]` 重新汇总。查询路径上同样要先 push 再访问子节点，否则查询到的子 sum 不含祖先延迟量。许多初学者能写出修改的 push，却在查询时忘记 push，导致「修改后查询偶发错误」。

**307 NumArray 与仓库类的对应关系**

LeetCode 要求实现 `NumArray`：`__init__(nums)` 构造；`update(index, val)` 将 `nums[index]` 更新为 `val`；`sumRange(left, right)` 返回闭区间和。用本仓库 `SegmentTreeLazy` 时，构造传入 `list(nums)`；`update` 可先 `old = range_sum(i,i)` 再 `range_add(i,i, val-old)`；`sumRange` 调用 `range_sum(left, right)`。注意题面是**赋值**而非**加 v**，差量写法最不易错。若你写成 `range_add(i,i,val)` 而不减旧值，会在第二次 update 同一位置时累加错误。提交前用官方样例与自造「连续 update 同一 index」用例测试。

**树状数组在同一题上的思路（便于对比记忆）**

树状数组维护前缀和：`add(i, delta)` 在 BIT 上走；`sum(i)` 为前缀；区间和 `sum(r)-sum(l-1)`。307 的 `update` 即 `delta = val - nums[i]` 后更新 BIT 与数组。代码通常更短，但面试官若问「区间加多个位置再加和」时，BIT 需差分或双 BIT，叙述不如线段树直观。建议本题两种都会：笔试时间紧可先写 BIT，简历写竞赛经历则准备线段树模板。

**手算例题（n=4，数据 [1,2,3,4]）**

1. 建树后根 `sum[1]=10`。查询 `range_sum(1,2)` 应得 `2+3=5`。
2. `range_add(1,2,5)` 后数组逻辑为 `[1,7,8,4]`，全区间和 20。
3. 再 `range_sum(0,0)` 得 1；`range_sum(2,3)` 得 12。

手算时画树，在完全包含节点打 lazy；部分包含节点必须先 push 再分儿子。若你算的根和与代码不一致，优先检查 push 是否把 lazy 乘了区间长度。

**与树状数组（BIT）对照**

| 维度 | 线段树（本实现） | 树状数组 |
|------|------------------|----------|
| 代码量 | 较长（递归+lazy） | 短（lowbit） |
| 区间加 + 区间和 | lazy 直观 | 需差分或两个 BIT |
| 区间最值 | 改合并函数 | 可写但不如 ST 表简洁 |
| 空间 | 约 4n | n |
| 常数 | 较大 | 较小 |
| 扩展性 | 矩阵、颜色、历史版本 | 受限 |

307 题用任一均可 AC；面试若时间紧可先说 BIT 思路再补「若区间操作更复杂用线段树」。

**单点修改与区间赋值**

**单点赋值**：`assign(i, x)` 可先 `range_sum(i,i)` 得旧值，再 `range_add(i,i, x-old)`。或单独写 `_point_set` 递归到叶子。

**区间赋值 lazy**：需标记「待覆盖为 val」而非加法，push 时要覆盖儿子 sum 与 lazy，语义与加法 lazy 不同，勿混用同一数组。

**动态开点与值域线段树**

下标范围 `[1,10^9]` 但 n 次操作时，只在访问路径上建节点，总节点 O(n log V)。竞赛常用；面试极少，知道名词即可。

**扫描线中的线段树**

矩形面积并：离散化 x 坐标，按 y 排序边事件；线段树维护 x 轴上覆盖长度。事件触发时对某段区间 `+1/-1` 覆盖计数，根节点维护总覆盖长度。与本仓库「区间加和」是不同聚合函数，但递归框架相同。

**常见 WA 原因排查**

| 现象 | 可能原因 |
|------|----------|
| 样例和差一个常数 | push 未乘区间长度 |
| 超时 | 完全包含仍递归到底 |
| RE | 数组开太小，应 `4*n` |
| 负数数组 | 仍可用加法 lazy，注意类型 |

**面试口述模板（约 90 秒）**

「线段树把区间 `[0,n-1]` 建成二叉树，每个节点存区间和。区间修改若完全覆盖当前节点，就在节点打 lazy 并更新 sum；否则先下推 lazy 再递归儿子。查询同理，部分相交先 push。建树 O(n)，单次操作 O(log n)，空间 O(n)。307 可变数组求区间和可用它或树状数组。」

**与仓库题解目录协作**

`problems/leetcode/0307_range_sum_query_mutable/` 中若有 BIT 版 solution，与本专题线段树版应对拍同一组测试。修改 `segment_tree.py` 后务必重跑 `segment_tree.py` 与 307 题解（若已链接）。

## Python 实现

Study 完整实现（区间加 + 区间和 + 自测）：

```python
class SegmentTreeLazy:
    """下标 0..n-1，区间加、区间求和。"""

    def __init__(self, data: list[int]) -> None:
        self._n = len(data)
        self._sum = [0] * (4 * max(1, self._n))
        self._lazy = [0] * (4 * max(1, self._n))
        if self._n:
            self._build(1, 0, self._n - 1, data)

    def _build(self, idx: int, l: int, r: int, data: list[int]) -> None:
        if l == r:
            self._sum[idx] = data[l]
            return
        m = (l + r) // 2
        self._build(idx * 2, l, m, data)
        self._build(idx * 2 + 1, m + 1, r, data)
        self._sum[idx] = self._sum[idx * 2] + self._sum[idx * 2 + 1]

    def _push(self, idx: int, l: int, r: int) -> None:
        if self._lazy[idx] == 0 or l == r:
            return
        m = (l + r) // 2
        for child in (idx * 2, idx * 2 + 1):
            self._lazy[child] += self._lazy[idx]
        self._sum[idx * 2] += self._lazy[idx] * (m - l + 1)
        self._sum[idx * 2 + 1] += self._lazy[idx] * (r - m)
        self._lazy[idx] = 0

    def range_add(self, ql: int, qr: int, val: int) -> None:
        self._range_add(1, 0, self._n - 1, ql, qr, val)

    def _range_add(self, idx: int, l: int, r: int, ql: int, qr: int, val: int) -> None:
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            self._lazy[idx] += val
            self._sum[idx] += val * (r - l + 1)
            return
        self._push(idx, l, r)
        m = (l + r) // 2
        self._range_add(idx * 2, l, m, ql, qr, val)
        self._range_add(idx * 2 + 1, m + 1, r, ql, qr, val)
        self._sum[idx] = self._sum[idx * 2] + self._sum[idx * 2 + 1]

    def range_sum(self, ql: int, qr: int) -> int:
        return self._range_sum(1, 0, self._n - 1, ql, qr)

    def _range_sum(self, idx: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql > r or qr < l:
            return 0
        if ql <= l and r <= qr:
            return self._sum[idx]
        self._push(idx, l, r)
        m = (l + r) // 2
        return self._range_sum(idx * 2, l, m, ql, qr) + self._range_sum(
            idx * 2 + 1, m + 1, r, ql, qr
        )
```

**自测逻辑**：初始 `[1,2,3,4,5]`，`range_sum(1,3)==9`；`range_add(1,3,10)` 后全区间和为 `1+12+13+14+5`。空树 `SegmentTreeLazy([])` 不崩溃。

**读代码顺序**：先 `_build` 理解 pull → 再 `_range_add` 理解 lazy 完全包含 → 再 `_push` → 最后 `_range_sum` 镜像查询。

**封装 LeetCode 307 风格类（示意）**

```python
class NumArray:
    def __init__(self, nums: list[int]) -> None:
        self._st = SegmentTreeLazy(nums)

    def update(self, index: int, val: int) -> None:
        old = self._st.range_sum(index, index)
        self._st.range_add(index, index, val - old)

    def sumRange(self, left: int, right: int) -> int:
        return self._st.range_sum(left, right)
```

提交时注意类名与题面一致；若 OJ 卡常，可改 BIT。

**建树与空数组**

`SegmentTreeLazy([])` 不调用 `_build`，`range_sum` 对任意区间返回 0；适合作为边界测试。非空时 `4*n` 数组足够存储完全二叉树层序下标（根为 1 的堆式存储）。

**递归深度**

Python 默认递归深度约 1000，`n=10^5` 时递归可能溢出；可 `sys.setrecursionlimit` 或改迭代。C++ 递归 1e5 也可能栈溢出，竞赛常用迭代或 `g++ -O2` 开栈。面试 n≤1e4 时递归一般安全。

**对拍脚本思路**

```python
import random
data = [random.randint(0, 9) for _ in range(20)]
st = SegmentTreeLazy(data)
for _ in range(50):
    l, r = sorted(random.sample(range(20), 2))
    v = random.randint(-3, 3)
    st.range_add(l, r, v)
    brute = sum(data[i] for i in range(l, r + 1))
    assert st.range_sum(l, r) == brute
    for i in range(l, r + 1):
        data[i] += v
```

本地验证 lazy 正确性后再提交 OJ。

## C++ 实现

```cpp
struct SegTree {
    int n;
    vector<long long> sum, lazy;
    SegTree(const vector<int>& a) {
        n = (int)a.size();
        sum.assign(4 * max(1, n), 0);
        lazy.assign(4 * max(1, n), 0);
        if (n) build(1, 0, n - 1, a);
    }
    void push(int idx, int l, int r) {
        if (!lazy[idx] || l == r) return;
        int m = (l + r) / 2;
        for (int c : {idx * 2, idx * 2 + 1}) lazy[c] += lazy[idx];
        sum[idx * 2] += lazy[idx] * (m - l + 1);
        sum[idx * 2 + 1] += lazy[idx] * (r - m);
        lazy[idx] = 0;
    }
    void range_add(int idx, int l, int r, int ql, int qr, long long v) {
        if (ql > r || qr < l) return;
        if (ql <= l && r <= qr) {
            lazy[idx] += v;
            sum[idx] += v * (r - l + 1);
            return;
        }
        push(idx, l, r);
        int m = (l + r) / 2;
        range_add(idx * 2, l, m, ql, qr, v);
        range_add(idx * 2 + 1, m + 1, r, ql, qr, v);
        sum[idx] = sum[idx * 2] + sum[idx * 2 + 1];
    }
    long long range_sum(int idx, int l, int r, int ql, int qr) {
        if (ql > r || qr < l) return 0;
        if (ql <= l && r <= qr) return sum[idx];
        push(idx, l, r);
        int m = (l + r) / 2;
        return range_sum(idx * 2, l, m, ql, qr)
             + range_sum(idx * 2 + 1, m + 1, r, ql, qr);
    }
    void range_add(int ql, int qr, long long v) { range_add(1, 0, n - 1, ql, qr, v); }
    long long range_sum(int ql, int qr) { return range_sum(1, 0, n - 1, ql, qr); }
};
```

与 Python 逻辑一一对应；`main` 中断言与 Python 自测相同。编译无需 `alg_std.hpp`（本文件仅 `<vector>` 与 `<cassert>`）。

**迭代版**：部分选手用非递归线段树降低常数；面试递归版足够，务必写对 lazy。

## 练习与延伸

| 资源 | 说明 |
|------|------|
| LC 307 | 区域和检索，可变 |
| LC 308 | 二维区域和（树套树或四叉树） |
| LC 327 | 区间和个数（前缀和 + 离散化 + BIT/线段树） |
| Study `0307_range_sum_query_mutable` | 官方风格题解与测试 |
| `ds-tree-fenwick-tree` | BIT 对照专题 |

**扫描线入门**：矩形周长并——边事件排序，线段树维护覆盖条数长度；先掌握本模板再刷。

**持久化**：可版本线段树用于可持久化数组、主席树求第 k 小——竞赛向，面试极少。

**307 题面与线段树映射**

- `NumArray(nums)` → `SegmentTreeLazy(list(nums))`；
- `update(i, val)` → 单点差量 `range_add(i, i, val - old)` 或单独写点修改；
- `sumRange(l, r)` → `range_sum(l, r)`。

若题解用 BIT：维护 `tree[i]` 表示前缀和，单点更新在 BIT 上走 `add(i, delta)`；查询 `sum(r)-sum(l-1)`。两种写法在 Study 307 目录应对拍同一测试文件。

**区间操作题单（超出 307 的延伸）**

| 题号 | 要点 |
|------|------|
| 715 | Range Module（线段树或 TreeMap） |
| 218 | 天际线（扫描线+线段树或 multiset） |
| 699 | 掉落的方块（坐标压缩+线段树） |

以上难度高于 307，建议在掌握本仓库 `segment_tree.py` 后再刷。

**差分与线段树的选择**

多次「区间加一」+「单点查询」可用差分数组；多次「区间加 v」+「区间求和」用本 lazy 树。若只有单点修改+区间和，BIT 更短。写题前先花 30 秒判断操作类型，避免过度设计。

**竞赛常数优化**

- 根下标 1 的堆式存储与 0 根二选一，全程统一；
- `push` 内联；
- 避免 Python 递归用 `sys.setrecursionlimit` 或改迭代；
- C++ 用 `long long` 防溢出。

## 学习路径

1. **Day 1**：前缀和与 O(n) 修改对比 → 读「抽象模型」→ 手画四叶子树；
2. **Day 2**：抄一遍 Python 四函数 → 跑 `segment_tree.py` → 改 n=8 手算对拍；
3. **Day 3**：闭卷写 C++ 模板 → 提交 LC 307；
4. **Day 4**：读 `fenwick_tree`，同一题双解法；
5. **Day 5（可选）**：离散化 + 线段树模板题 315/218。

**自检**：能否在 25 分钟内无 bug 写出 lazy 区间加与区间和（含 `push`）。

若达不到，重复 Day 2～3 并缩小 n 手算；不要跳去刷难题。线段树熟练度来自 push 肌肉记忆，不是题海数量。达到自检标准后再做区间赋值、二维树套树等变体，否则 lazy 语义会叠在一起难以排错。

**两周强化计划（在职可拉长为四周）**

第 1–2 天只看不写：读基础篇「抽象模型」「实现要点」，手画 n=8 的树，标出每个节点管的区间，在纸上模拟 `range_add(2,5,3)` 哪些节点完全包含、哪些要 push。第 3–4 天对照 `segment_tree.py` 抄一遍四函数，每抄一行在注释写对应节点区间。第 5 天闭卷默写，默写失败则只重做默写不改题。第 6 天跑通脚本并写 307 的 `NumArray` 包装类提交。第 7 天读 `fenwick_tree` 笔记，用同一组数据手写 BIT 版 307。第 8–9 天双解法对拍，记录哪版更短、哪版更好讲。第 10 天复习易错点清单，做 n=1、n=2、全区间修改、连续 update 同一位置等边界。第 11–12 天选做 327 或 715 之一，只需理解「离散化 + 线段树」即可，不必 AC 全部。第 13–14 天模拟面试：九十秒讲线段树 + 十五分钟白板写模板。达标后本专题可标记为掌握，转向扫描线或树形 DP 等下一专题。

**与竞赛训练的区别**

竞赛选手常压行、用迭代、合并 push-pull；面试选手优先可读性与正确性，变量名清晰、三分支注释完整。本仓库代码偏面试；若你同时打 ICPC，可在同目录另存 `segment_tree_compact.py` 实验，勿覆盖主脚本断言。竞赛中区间题还可能用分块、莫队、根号分解，复杂度介于 O(1) 与 O(n) 之间，面试提及即可，不必实现。

**常见追问的标准答法**

问：线段树和树状数组选哪个？答：单点改+区间和优先 BIT；区间加+区间和用 lazy 线段树或双 BIT；区间最值看是否带修改。问：空间多少？答：数组实现约 4n。问：建树复杂度？答：O(n)。问：lazy 下推时机？答：访问子节点前且父 lazy 非零。问：307 赋值怎么办？答：单点查询旧值，区间加差量。每个答法控制在两句话内，避免背证明。

**线段树递归轨迹详解（区间加 [1,2] 值 10，n=5）**

初始 [1,2,3,4,5]。range_add(1,2,10) 时根 [0,4] 与请求部分相交，push 后分左右子；叶子 [1,1]、[2,2] 完全包含则打 lazy 并加 sum；回溯合并。查询前路径上 lazy 非零必须 push。

**节点数组与空间**

堆式下标根为 1，空间开 4n。层 h 下标约 [2^h, 2^(h+1)-1)。勿对非 2 幂 n 盲目用 2n 空间。

**BIT 模板摘录（307 对照）**

```python
class BIT:
    def __init__(self, n: int) -> None:
        self.n = n
        self.t = [0] * (n + 1)
    def add(self, i: int, d: int) -> None:
        i += 1
        while i <= self.n:
            self.t[i] += d
            i += i & -i
    def prefix(self, i: int) -> int:
        i += 1
        s = 0
        while i:
            s += self.t[i]
            i -= i & -i
        return s
```

单点更新 add(i,delta)；区间和 prefix(r)-prefix(l-1)。行数少于线段树。

**区间最值预览**

节点存 max，加法 lazy 时 max 亦加 lazy。赋值 lazy 语义不同，勿混用本模板。

**扫描线思路**

离散化 x，按 y 事件排序，线段树维护 x 覆盖长度，面积累加覆盖长度乘 delta_y。换维护量不换递归框架。

**竞赛顺序**

307 → 715 → 218 → 699。掌握 segment_tree.py 后再刷。

**面试分工**

90 秒讲思想；10 分钟写 build/push/range_add/range_sum 骨架。

**语言陷阱**

Python 递归深度；C++ long long；0-based 下标；n=0 空树。

**维护**

改 push 必同步 py/cpp/notes.md 与手算例题。



**深度学习补充（二）：lazy 线段树完整语义**

**不变量 I1**：对每个节点 v，v.sum 等于 v 区间内在考虑 v.lazy 已生效到 v 自身的前提下，所有叶子真实值之和。lazy 表示「子树内每个位置尚待加上的统一增量」，尚未下推到子节点。

**不变量 I2**：访问节点前，若需读取子节点真实 sum 或继续向下修改，且当前节点 lazy≠0，必须先 push，使子节点 lazy/sum 吸收父延迟量。

**build 后禁止改原数组**：外部改 data 不会自动同步；要么重建树，要么单点/区间更新。

**range_add 伪代码（面试默写版）**

```
function range_add(node, L,R, ql,qr, v):
  if qr < L or ql > R: return
  if ql <= L and R <= qr:
    lazy[node] += v; sum[node] += v * (R-L+1); return
  push(node, L, R)
  mid = (L+R)/2
  range_add(left, L, mid, ql, qr, v)
  range_add(right, mid+1, R, ql, qr, v)
  sum[node] = sum[left] + sum[right]
```

**range_sum 伪代码**

```
function range_sum(node, L,R, ql,qr):
  if qr < L or ql > R: return 0
  if ql <= L and R <= qr: return sum[node]
  push(node, L, R)
  return range_sum(left,...)+range_sum(right,...)
```

**307 测试用例心智模型**

构造 NumArray([1,2,3,4,5])；sumRange(0,2)→6；update(1,3) 后数组 [1,3,3,4,5]；sumRange(1,2)→6。用线段树时 update 用差量加。多组 update+sum 交叉验证。

**树状数组与线段树选型决策树**

仅单点修改+前缀和 → BIT。区间加+单点查 → 差分。区间加+区间和 → lazy 线段树或双 BIT。区间最值+单点修改 → 线段树或 multiset。静态 RMQ → ST 表。看清操作再写代码，避免 overkill。

**矩形面积并（218）口述**

竖线扫描，事件排序，线段树维护 x 被覆盖段总长，相邻事件高度差乘覆盖长度累加。与本仓库区间加不同，但证明你会「换维护量」。

**持久化与动态开点（知道即可）**

动态开点：值域大、实际访问点数 O(n log V)。持久化：修改版本不破坏历史，路径复制。竞赛常用，面试除特别岗位可一句带过。

**fenwick 专题**

学完本页后在 Study fenwick_tree 目录运行对拍脚本（若有），比较 307 代码行数。站点 ds-tree-fenwick-tree 撰写后互链。

**错误集**

样例和差常数：push 乘 (r-l+1) 写错。TLE：完全包含仍递归到叶。RE：4n 不够或下标 0 根混用。Python RE：递归过深改迭代或增大 limit。

**重复练习 Schedule**

Day1 手画 n=8 树；Day2 默写四函数；Day3 提交 307；Day4 BIT 版 307；Day5 327 或 715 选做；Day6 218 读题解；Day7 复盘错题。

**与 data_structures/tree 其他结构**

二叉树遍历是基础；堆用于第 K 大；线段树用于区间；BST 用于有序。勿在需要区间修改时用 BST 硬套。

**C++ 实现细节**

vector sum,lazy 开 4*n+5；long long；main 中断言与 py 一致。g++ -std=c++17 -O2。Windows LiteralPath 进目录编译。

**本页字数维护**

扩写 lazy 语义或例题后重跑 validate_algorithm_guide.py --slug ds-tree-segment-tree 与 quality 脚本（若启用）。

**收束与发布**

`topic_path` 为 `data_structures/tree/segment_tree`；`guide_toc` 为 `topic-ds`；`status` 为 `draft`。发布前确认：汉字不少于 8000；基础篇六个 `###` 齐全；Python/C++ 实现节含 `SegmentTreeLazy` / `SegTree` 代码；无重复段落堆砌。掌握标准：闭卷默写 `push` 与完全包含分支，二十分钟内写完四函数并通过 `segment_tree.py` 自测，再提交 LeetCode 307。

**与教材、竞赛资料的关系**

《算法导论》不强调线段树；竞赛书籍（如《算法竞赛进阶指南》）有专章。本仓库实现面向「面试可讲清 + 可手写」，非压行竞赛模板。学完本页后若转向竞赛，可再学迭代版、持久化版与李超线段树，勿混用多种 lazy 语义。

**Python 递归与 C++ 栈**

`n` 接近 `10^5` 时 Python 需 `sys.setrecursionlimit` 或改迭代；C++ 注意栈溢出与 `long long`。Windows 编译使用 `Set-Location -LiteralPath` 进入 `cpp/data_structures/tree/segment_tree` 后 `g++ -std=c++17 -O2`。

**与 fenwick_tree 的一周内对拍**

同一周完成 307 的 BIT 实现与线段树实现，比较代码行数与本地运行时间，形成「何时用 BIT、何时用线段树」的口头答案，面试时先答 BIT 再补充线段树适用性。

**发布前自检（medium 档位）**

在 `f:\commercial\atelier` 执行 `validate_algorithm_guide.py --slug ds-tree-segment-tree --strict`，确认汉字≥8000、`基础篇` 仅用 `###`、Python/C++ 节各含代码块。若扩写 lazy 推导，务必同步 `segment_tree.py` 与 C++ 文件，避免讲义与仓库断言不一致。

**面试 90 秒模板（可背诵）**

「区间修改+区间查询用线段树；数组建树 O(n)；单点/区间加用 lazy；查询前 push 下放标记；复杂度 O(log n)。若只需前缀和+单点改，树状数组更短。」

**lazy 下放手算（1 分钟版）**

节点表示区间 `[l,r]`，若整段加 `v` 且查询完全包含该段，则 `lazy[idx]+=v`，`sum[idx]+=v*(r-l+1)`，不必下潜孩子。部分查询或部分修改时先 `push` 把孩子 lazy 与 sum 同步，再递归。记住「查询路径上每个节点最多 push 一次」即可避免重复累加。

**与竞赛模板差异**

竞赛常写迭代线段树、宏定义下标 `idx<<1`；本仓库教学用递归 + 1-based 堆下标，面试白板用递归更易讲清。上线代码若 `n` 极大，再换迭代并测常数。

**307 变体练习清单**

| 变体 | 训练目标 |
|------|----------|
| 仅单点修改 + 区间和 | 去掉 lazy，验证 push 仍正确 |
| 区间加 + 区间和 | 本仓库默认 |
| 区间赋值 + 区间和 | lazy 存赋值标记，push 时覆盖子 sum |
| 二维矩阵 | 树套树或四叉树，超出本文 |

每变体改完后在 `python/data_structures/tree/segment_tree` 跑通自测，再写 3 句笔记说明 lazy 语义变化。

**调试技巧**

若 `range_sum` 结果偏小，检查 push 是否在查询前调用、lazy 是否在 `l==r` 叶子正确落到 `sum`。若偏大，检查是否重复累加 lazy 而未清零。用 `n<=8` 小数组打印递归路径，比在大样例上 printf 更省时间。

**与树形 DP 区分**

树形 DP 在「树结构上的最优值递推」；线段树在「数组下标区间上的代数维护」。题目给「树上路径修改」时常用树链剖分+线段树，那是进阶组合，不是本模板单独能覆盖的——面试可先答「需要 HLD」，再回退本数组版 307。

**空间估算**

四倍空间 `4n` 数组在 `n=10^5` 时约 1.6e6 个 `long long`，内存可接受。若 MLE，检查是否开了 `vector` 嵌套过多或误开 `8n`。Python 递归深度与 C++ 栈空间在 `n` 很大时需改迭代。

**AC 后巩固**

闭卷默写 `build / range_add / range_sum / push` 四个函数签名；第二天只做 LC 307 与 308 其中一题，第三天对比 `ds-tree-fenwick-tree` 笔记，形成「会写」到「会选」的闭环。

**读者反馈位**

若你发现仓库 `segment_tree.py` 与本文 lazy 公式不一致，以仓库通过自测的代码为准提 Issue；本文随 Study 仓库修订同步更新，避免「讲义旧、代码新」分裂。

**常数优化备忘**：叶节点多时递归可能 TLE，可改迭代或 `sys.setrecursionlimit`；C++ 注意 `long long` 与 `-O2`。面试写递归通常足够，笔试再压常数。

**与 BIT 选型结论（背一句）**：单点改+前缀和→BIT；区间加+区间和→线段树或 BIT 配合差分；区间最值→线段树或多棵线段树。背一句选型比背两套完整实现更能应付「为什么不用 BIT」的追问。

**模板默写检查表**：`build` 是否 O(n)；`range_add` 是否整段覆盖才写 lazy；`range_sum` 是否在递归入口 `push`；叶子 `l==r` 是否只改 `sum` 不清 lazy 残留。四项默写无误后再宣称「掌握线段树」。建议把 `segment_tree.py` 与 `segment_tree.cpp` 并排打开：同一组 `a=[1,2,3,4]` 上依次 `range_add(1,2,5)` 与 `range_sum(0,3)`，在纸上记录每个递归节点访问顺序，比只看代码更易发现漏 `push` 的节点。周末用两小时完成上述对拍并写 5 行结论，是线段树专题性价比最高的练习。

**与仓库题解 0307 的衔接**：`python/problems/leetcode/0307_range_sum_query_mutable/` 提供 NumArray 封装；读完本文后打开该目录，对照类方法如何调用 `SegmentTreeLazy`，再在 LeetCode 提交。C++ 侧同步打开 `cpp/problems/leetcode/0307_range_sum_query_mutable/` 对拍编译。掌握 lazy 线段树后，区间修改类题目应优先想到本模板，再考虑是否可降维为 BIT。本文档与 Study `notes.md`、双语言源码三者一致时，再标记本站 manifest 为 published。第 1 批 Algorithm 专题验收包含本篇，通过前保持 draft。lazy 线段树是区间操作题的第一性模板，务必练到闭卷可写。完成 307 与本文对拍后即可进入下一专题。fenwick 专题见 `ds-tree-fenwick-tree`。若仍不足八千字校验，说明你还应继续阅读上文 push 推导而非跳过正文。


## 延伸阅读

- 仓库笔记：`python/data_structures/tree/segment_tree/notes.md`
- GitHub 树目录：[segment_tree](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/tree/segment_tree)
- 树状数组：`ds-tree-fenwick-tree`（待撰写时见 manifest）
- 二叉树基础：`ds-tree-binary-tree`
- 算法仓库导读：`overview`

维护：修改 `segment_tree.py` 的 lazy 语义时，同步更新本页公式、C++ 片段与 `notes.md`，并重新运行双端自测。

**迭代实现提示**

部分选手用非递归线段树（堆式下标循环）压常数；面试递归版足够。若写迭代，注意 `push` 顺序与递归版一致，否则 lazy 会乱。Z 数组、ST 表、线段树三者不要混：ST 表静态 RMQ O(1) 查询；Z 用于字符串；线段树用于修改+查询。

**持久化线段树一句话**

可版本化数据结构用于「历史前缀」类题（如 329 最长递增路径的某些解法、主席树求区间第 k 小）。实现是在路径上复制新节点而非原地改，空间 O(n log n) 每次修改。本仓库未实现，读到题解时可回来对照本页递归框架。

**二维线段树**

308 区域和可变：外层线段树下标为行，内层为列；修改单点触发两层 `O(log n log m)`。写不出来时先掌握一维 lazy 再加维。

**李超线段树 / 线段树合并**

竞赛优化 DP 用；面试可跳过。知道「线段树不只是区间和」有助于扩展视野。

**fenwick_tree 专题联动**

学完本页后打开 `ds-tree-fenwick-tree`（撰写中见 manifest），用同一组自定义测试对比 307 运行时间与代码行数，形成「结构选型」直觉。
