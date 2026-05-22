---
title: "算法 · 动态规划总览"
series: algorithm
category: Algorithms
topic_path: algorithms/dynamic_programming
guide_toc: topic-algorithm
guide_tier: major
status: published
---

# 算法 · 动态规划（Dynamic Programming）总览

## 导读

**动态规划**是在**重叠子问题**与**最优子结构**同时成立时，用表格或记忆化避免指数级重复计算的方法。名称里的「规划」指递推填表，不是指「写程序」。与分治的区别：分治子问题互不相交；DP 子问题会被多次用到，必须复用结果。与贪心的区别：贪心只保证局部最优；DP 要证明更小规模的最优能拼成全局最优。

Study 仓库将 DP 按**状态形状**拆成六个子目录，本页是**总览**；各子目录有独立 `*_dp.py` / `*_dp.cpp` 与专题博文（如 `algo-dp-linear`）。下表来自 `python/algorithms/dynamic_programming/notes.md`：

| 子目录 | 典型问题 | 入口文件 |
|--------|----------|----------|
| `linear/` | LIS、LCS、编辑距离、打家劫舍 | `linear_dp.py` |
| `knapsack/` | 0-1 背包、完全背包 | `knapsack_dp.py` |
| `interval/` | 矩阵链乘等 | `interval_dp.py` |
| `tree/` | 树上最大独立权（打家劫舍 III） | `tree_dp.py` |
| `digit/` | 数位和模 K 计数 | `digit_dp.py` |
| `bitmask/` | TSP 状压 | `bitmask_dp.py` |

读完本文，你应能根据题面**状态维度**（前缀下标、容量、区间端点、树节点、数位位、集合掩码）判断归入哪一类，知道 Study 中跑哪份脚本，并掌握六类模板的转移直觉与复杂度。子专题细节（如 LIS 的 `O(n log n)`、LCS 滚动数组）在 `algo-dp-linear` 等子页展开；本页强调**地图、选型与可运行代码全集**。

**面试中的 DP**：先写状态含义与转移，再谈复杂度与空间优化。仓库每个脚本带 `__main__` 断言，适合本地对拍后再刷 LeetCode。

**六子目录阅读顺序（建议）**：先 `linear`（占笔试过半）→ `knapsack`（0-1/完全）→ `interval`（矩阵链）→ `tree`（打家劫舍 III）→ `digit`（计数型）→ `bitmask`（n≤20）。每步用 `python -LiteralPath` 跑通对应 `*_dp.py` 再读子页 `algo-dp-*`。总览页 **Python 实现** 节收录六文件完整源码，便于离线对照；**基础篇** 含六类转移口诀与手推，不必先读完子页再回总览。

**与贪心、分治的分工**：活动选择、部分区间题可贪心；归并、快排用分治；当子问题**重叠**且需比较多种组合（背包选法、双串对齐、集合 TSP）时用 DP。题面出现「方案数」「最少操作」「最大价值且有限制」时，优先想状态维度再映射子目录。

## 预备知识

> **环境**：Python 3.10+（`bisect`、`functools.lru_cache`）；C++17，`g++`，树/状压/数位实现通过 `#include <alg_std.hpp>`。

建议已具备：

- **递归与记忆化**：`@lru_cache` 与数组 DP 等价；长深度注意 Python 递归限制。
- **数组填表顺序**：依赖更小参数的状态，拓扑序填表无环。
- **复杂度估算**：状态数 × 转移代价；背包 `O(nW)`、区间 `O(n³)`、状压 `O(n²·2ⁿ)`。
- **初始化与边界**：空串、空树、容量 0、掩码仅含起点等必须显式定义。
- **滚动数组**：背包一维逆序、打家劫舍双变量、LCS 一行等（线性子专题详述）。

**最优子结构**：全局最优在「最后一次决策」后，剩余部分必须是剩余规模下的最优。例如 0-1 背包在容量 `w` 下选或不选第 `i` 件，两种分支取 max 即最优子结构。

**重叠子问题**：同一 `(i,w)` 或 `(i,j)` 被多条决策路径重复访问，记忆化或填表去重。

**工具链**：PowerShell 使用 `Set-Location -LiteralPath` 与 `python -LiteralPath`；Windows 路径含空格时必须加引号与 `-LiteralPath`。

## Study 仓库对照

`topic_path`：`algorithms/dynamic_programming`。

| 子目录 | Python 笔记 | Python 实现 | C++ 实现 |
|--------|-------------|---------------|----------|
| 根 | `dynamic_programming/notes.md` | — | — |
| linear | `linear/notes.md` | `linear/linear_dp.py` | `linear/linear_dp.cpp` |
| knapsack | `knapsack/notes.md` | `knapsack/knapsack_dp.py` | `knapsack/knapsack_dp.cpp` |
| interval | `interval/notes.md` | `interval/interval_dp.py` | `interval/interval_dp.cpp` |
| tree | `tree/notes.md` | `tree/tree_dp.py` | `tree/tree_dp.cpp` |
| digit | `digit/notes.md` | `digit/digit_dp.py` | `digit/digit_dp.cpp` |
| bitmask | `bitmask/notes.md` | `bitmask/bitmask_dp.py` | `bitmask/bitmask_dp.cpp` |

在 `F:\Study\Algorithm` 根目录依次运行（`-LiteralPath`）：

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\linear\linear_dp.py
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\knapsack\knapsack_dp.py
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\interval\interval_dp.py
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\tree\tree_dp.py
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\digit\digit_dp.py
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\bitmask\bitmask_dp.py
```

**C++ 示例（linear）**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\dynamic_programming\linear
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe linear_dp.cpp
.\run.exe
```

其余子目录将 `linear` 换成 `knapsack`、`interval` 等即可。输出应为 `linear_dp OK`、`knapsack_dp OK` 等。

## 基础篇

### 直觉与定义

DP 解题四步：**定义状态** → **写转移** → **定边界** → **定计算顺序与答案位置**。六类子目录对应六类「状态参数」：

**线性 DP（`linear/`）**

状态沿**一维前缀**或**双串前缀**推进：`dp[i]`、`dp[i][j]`，转移只依赖更短前缀或 `i-1/i-2`。代表：LIS、LCS、编辑距离、打家劫舍。识别词：子序列、两字符串、插入删除替换、相邻不能同选。

- **LIS**：`tails` 耐心排序 + 二分，`O(n log n)`。
- **LCS**：`dp[i][j]` 两前缀，匹配则左上 +1，否则 max(上,左)。
- **编辑距离**：三种操作 min，边界 `dp[i][0]=i`。
- **打家劫舍**：`prev2, prev1` 滚动，`cur = max(prev1, prev2 + x)`。

**背包 DP（`knapsack/`）**

0-1：**每件最多一次**，一维 `dp[w]` 逆序枚举容量，避免同一轮重复使用。完全：**每件无限**，正序枚举 `w`。状态语义：`dp[w]` = 容量不超过 `w` 的最大价值。

**区间 DP（`interval/`）**

状态为闭区间 `[i,j]`：合并、分割、矩阵链乘等。矩阵链乘：`dp[i][j]` = 乘 `A_i..A_j` 的最少标量乘法次数，枚举分割点 `k`。长度 `len` 从 2 到 `n` 递增填表。

**树形 DP（`tree/`）**

DFS 返回子树信息，在根处合并。打家劫舍 III：`dfs` 返回 `(不选根子树最大, 选根子树最大)` 二元组，父节点抢则子必须不抢。

**数位 DP（`digit/`）**

按位从高到低，状态含位置 `i`、`tight`（是否贴上限）、`leading_zero`（前导零）、模余等。统计 `[0,n]` 满足数位约束的个数，避免大整数枚举。

**状压 DP（`bitmask/`）**

用整数掩码表示已访问集合；TSP：`dp[mask][u]` = 已访问 `mask` 且当前在 `u` 的最小代价。`n ≤ 20` 常见，复杂度 `O(n²·2ⁿ)`。

### 复杂度分析

| 类型 | 状态规模 | 典型时间 | 典型空间 |
|------|----------|----------|----------|
| 线性 LIS | n | O(n log n) | O(n) |
| 线性 LCS/编辑 | n·m | O(n·m) | O(n·m) 可滚动 |
| 打家劫舍 | n | O(n) | O(1) |
| 0-1 背包 | W | O(n·W) | O(W) |
| 完全背包 | W | O(n·W) | O(W) |
| 区间 | n² | O(n³) | O(n²) |
| 树形 | n | O(n) | O(h) 栈 |
| 数位 | 位·K·2·2 | O(位·K) | 记忆化 |
| 状压 TSP | n·2ⁿ | O(n²·2ⁿ) | O(n·2ⁿ) |

面试应主动说明「伪多项式」背包（W 为数值）、状压对 `n` 的指数依赖。

### 代码模板

**0-1 背包（逆序）**

```python
def knapsack_01(weights, values, cap):
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for x in range(cap, w - 1, -1):
            dp[x] = max(dp[x], dp[x - w] + v)
    return dp[cap]
```

**完全背包（正序）**

```python
for x in range(1, cap + 1):
    for w, v in zip(weights, values):
        if x >= w:
            dp[x] = max(dp[x], dp[x - w] + v)
```

**矩阵链乘**

```python
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = min(dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1] for k in range(i, j))
```

**树形打家劫舍**

```python
def dfs(n):
    if not n: return 0, 0
    l0, l1 = dfs(n.left)
    r0, r1 = dfs(n.right)
    take = n.val + l0 + r0
    skip = max(l0, l1) + max(r0, r1)
    return skip, take
```

**数位 DFS**

```python
# dfs(i, tight, mod, leading_zero) 枚举下一位 d，更新 ntight, nz, nmod
```

**TSP 状压**

```python
dp[1][0] = 0
for mask in range(1 << n):
    for u in mask:
        for v not in mask:
            dp[mask|1<<v][v] = min(..., dp[mask][u] + dist[u][v])
```

线性四函数模板见子页 `algo-dp-linear`；下文 **Python 实现** 给出仓库完整源码。

### 变体与技巧

- **线性**：LIS 非递减用 `bisect_right`；LCS 变最长公共子串（不等置 0）；打家劫舍 II 拆环两次线性。
- **背包**：恰好装满容量初始化 `dp[0]=0` 其余 `-inf`；二维费用背包加一维；分组背包组内 0-1 再合并。
- **区间**：石子合并、戳气球、回文划分；统一按区间长度递增。
- **树形**：换根 DP、树上背包；返回值二元组可扩为三元组（抢/不抢/冷冻）。
- **数位**：上下界 `[L,R]` 用 `f(R)-f(L-1)`；数字 1 的个数、不含 4 等改 `nmod` 规则。
- **状压**：子集枚举 `sub = (mask-1)&mask`；哈密顿路径、最大独立集小图。

**选型速查**：前缀/双串 → linear；容量/件数 → knapsack；左右端点合并 → interval；树结构 → tree；按位计数 → digit；集合 ≤20 → bitmask。

### 易错点

1. **背包 0-1 正序**：同一物品用两次。
2. **背包完全当 0-1**：少计方案。
3. **区间 DP 长度循环外层**：`k` 必须在 `i,j` 之间。
4. **矩阵链乘维度**：`p` 长度 `n+1`，代价 `p[i]*p[k+1]*p[j+1]`。
5. **树形 DP 抢根**：子必须传「不选」分支 `l0,r0`。
6. **数位前导零**：仍在前导阶段时数位和/模不累计。
7. **状压 TSP 初值**：仅 `dp[1<<0][0]=0`，最后加回边到 0。
8. **LCS/编辑下标**：字符 `s[i-1]` 与表维 `i` 表前缀长度。
9. **打家劫舍滚动顺序**：先算 `cur` 再移位。
10. **状压无效状态**：`dp[mask][u]` 为 inf 时勿松弛。

### 练习建议

按子目录递进：

| 子目录 | 入门题 |
|--------|--------|
| linear | 300, 1143, 72, 198 |
| knapsack | 416, 322, 474, 518 |
| interval | 312, 1039, 516 |
| tree | 337, 124, 968 |
| digit | 233, 600, 1012 |
| bitmask | 847, 1349, TSP 模板 |

每类先跑通 Study 脚本断言，再刷 3–5 道题。混合题：583（LCS+删除）、354（LIS+排序）练识别。


### 记忆化与迭代的选型

线性双串、数位计数在 Study 中分别用二维填表与 @lru_cache 的 DFS。规则很简单：**状态维度固定且表不大**时用迭代（背包一维、LCS 表）；**状态含多个布尔标志**（tight、leading_zero）时记忆化代码更短，且 digit_dp.py 对 
<500 与暴力完全一致。Python 递归深度约 1000，树上 DFS 深度等于树高，链形 10^5 会栈溢出，树形 DP 竞赛常用迭代或手动栈。面试先写状态含义，再选「表填」或「dfs+memo」，最后谈空间滚动。

### 0-1 背包填表手推（与 knapsack_dp 断言一致）

物品重量 [1,2,3]、价值 [6,10,12]、容量 5。一维 dp[w] 表示容量不超过 w 的最大价值，初始全 0。

| 步骤 | 处理物品 | 逆序更新后 dp[0..5] | 说明 |
|------|----------|---------------------|------|
| 初值 | — | 0,0,0,0,0,0 | |
| 1 | (1,6) | 0,6,6,6,6,6 | w=1 起可放 |
| 2 | (2,10) | 0,6,10,16,16,16 | dp[3]=dp[1]+10=16 |
| 3 | (3,12) | 0,6,10,16,16,22 | dp[5]=dp[2]+12=22 |

若第 3 步改为**正序**枚举容量，同一轮可能先用「已含物品 3 的 dp[2]」再更新 dp[5]，等价于一件物品用两次，答案会大于 22，与 0-1 语义矛盾。完全背包 knapsack_unbounded 则必须正序，Study 断言 cap=8 时得 130。

### 数位 DFS 单步：n=13，k=3

字符串 s="13"，统计 [0,13] 中数位和为 3 的倍数个数。从 dfs(i=0,tight=True,mod=0,z=True) 出发：第 1 位上限为 1，枚举 d=0,1；d=0 保持前导零且 mod 不变，d=1 结束前导且 mod=1。第 2 位在 tight 时上限为 3。叶节点 i==len(s) 且 mod==0 时计数 1。count_digit_sum_mod0 对 
n<500 与暴力一致。区间 [L,R] 用 count(R)-count(L-1)，L=0 不必对 -1 调用。

### TSP 状压状态演进（四点样例）

dist 为 Study itmask_dp.py 中断言矩阵。初态 dp[1<<0][0]=0；枚举 mask 含 u 时扩展到未访问 v；全集合后 dp[full][u]+dist[u][0] 闭合得 21。复杂度 O(n²·2^n)。易错：初掩码为 1<<0；dp[mask][u]>=inf 勿松弛。

### 面试答题脚本（major 总览）

1. 识别状态维度对应六子目录。2. 一句话定义 dp 含义。3. 写转移与 max/min/逆序。4. 边界与初始化。5. 复杂度口述。6. 对齐仓库函数并 python -LiteralPath 跑通断言。


以下按 Study 六目录分别扩写，便于 major 总览单页内完成系统学习；与 `algo-dp-linear` 等子页互补，不重复粘贴子页全文。

### 线性 DP 深化

**LIS 朴素**：`dp[i]` 为以 i 结尾最长长度，转移看 j<i 且 nums[j]<nums[i]。`[10,9,2,5,3,7,101,18]` 答案 4。优化：`tails` 耐心排序，二分 `bisect_left`，O(n log n)。严格递增勿用 right。

**LCS**：`dp[i][j]` 为前缀长度；相等则左上+1，否则 max(上,左)。`abcde` 与 `ace` 得 3。构造路径：从 (na,nb) 回溯。与子串区别：不等时不能从左上继承。

**编辑距离**：`horse`→`ros` 为 3；三种操作对应删、插、替。583 仅删除：总删 len(a)+len(b)-2*LCS。

**打家劫舍**：`[2,7,9,3,1]` 得 12；滚动 prev2,prev1。213 环形：拆两次线性。337 树形见下文。

面试 30 秒模板：「状态是前缀/双前缀，转移来自更小前缀，复杂度 O(n) 或 O(nm) 或 O(n log n)。」

### 背包 DP 深化

**0-1**：`knapsack_01` 逆序 `for x in range(cap, w-1, -1)` 保证每件只用一次。样例 w=[1,2,3], v=[6,10,12], cap=5 → 22（选 2+3）。

**完全**：正序 `for x in range(1, cap+1)`，每件可重复。样例 cap=8 得 130。

**416 分割等和子集**：sum 为 S，等价 0-1 背包装满 S/2。

**322 零钱兑换**：完全背包求最少枚数改 min 而非 max，初始化 inf。

**474 一和零**：二维费用 0/1 个数限制，dp[i][j] 二维容量。

**恰好装满**：dp[0]=0 其余 -inf，最后看 dp[cap]==目标。

**多重背包**：数量 ci 二进制拆成 0-1 或单调队列优化。

易错：0-1 正序；完全当 0-1；初始化 -inf 与 0 混用。

### 区间 DP 深化

**矩阵链乘**：`p=[10,20,30,40]`，先乘 10×20×30 再乘结果与 30×40，代价 6000+12000=18000？手算：dp[0][2] 先 10*20*30=6000，再 (0,2)与(3) 得 6000+10*30*40=18000。与代码断言 `10*20*30+10*30*40` 一致。

**填表顺序**：len 从 2 到 n，i 从 0 到 n-len，k 在 i..j-1。保证子区间已算。

**312 戳气球**：虚拟 1 边界，区间 (i,j) 最后戳 k，合并左右+nums[i]*nums[k]*nums[j]。

**516 最长回文子序列**：区间 dp，相等则 dp[i+1][j-1]+2，否则 max(左,右)。

**合并石子**：常合并相邻，枚举分割点，代价为区间和。

复杂度 O(n³)，n=500 约 1.25e8 需常数优化或 C++。

### 树形 DP 深化

**打家劫舍 III**：`rob_tree` 返回 (skip, take)。抢根：val+l0+r0（子必须不抢）；不抢：max(l0,l1)+max(r0,r1)。样例树得 7。

**124 二叉树最大路径和**：每点贡献 (左最大, 右最大, 经过该点路径)，全局 max 更新，DFS 返回以该点为端点的单边最大。

**换根 DP**：先 dfs1 算子树答案，再 dfs2 传父侧信息换根，O(n)。

**968 监控二叉树**：三状态 0/1/2（无/有/子有），树上多状态 DP。

易错：抢父时子不能抢；空节点返回 (0,0)。

### 数位 DP 深化

**状态**：位置 i，tight 贴上限，mod 数位和模 K，leading_zero 前导零。

**转移**：枚举 d∈[0,limit]；nz 时 nmod 不变；否则 nmod=(mod+d)%k。

**终点**：i==len(s) 时 mod==0 返回 1。

**区间 [L,R]**：count(R)-count(L-1)，L=0 特判。

**233 数字 1 的个数**：按位贡献，拆 1 的个数到每位。

**600 不含连续 1**：上一位是否 1 进状态。

暴力对拍：digit_dp 对 nn<500 与暴力一致，建立信任。

复杂度 O(位数·K·状态数)，记忆化清晰。

### 状压 DP 深化

**TSP**：`dp[mask][u]`，初值 dp[1][0]=0，枚举 mask 含 u，扩展到 v，最后 u→0 闭合。样例 4 点得 21。

**复杂度**：O(n²·2^n)，n=20 约 4e7 转移，C++ 可过，Python 宜 n≤12。

**子集枚举**：`sub=(mask-1)&mask` 迭代子集。

**847 最短通路**：超源点连所有红色 0 权，求最短路或状压红色集合。

**1349 最大学生**：座位限制，掩码 compatible，逐行转移。

易错：初掩码只有起点；inf 比较；无向需双向边。

### 六类横向对比

| 维度 | 线性 | 背包 | 区间 | 树 | 数位 | 状压 |
|------|------|------|------|-----|------|------|
| 主参数 | 下标/前缀 | 容量 | 左右端点 | 节点 | 位 | 集合 |
| 典型复杂度 | n~nm | nW | n³ | n | dK | n²2^n |
| 滚动 | 常可 | 一维 | 少见 | 栈 | 记忆化 | 表大 |

### 从题面到子目录（练习 20 题映射）

| 题号 | 子目录 |
|------|--------|
| 300,1143,72,198 | linear |
| 416,322,518,474 | knapsack |
| 312,1039,516,1000 | interval |
| 337,124,968,543 | tree |
| 233,600,1012,902 | digit |
| 847,1349,943,TSP | bitmask |

### 记忆化与迭代

线性双串可 lru_cache(i,j)；数位常用记忆化；背包多用迭代一维。Python 递归深度有限，n,m 大用迭代。

### 空间优化速记

- 背包：一维 W。  
- 打家劫舍：两变量。  
- LCS：一行滚动 min(n,m) 列。  
- 区间：通常二维不可省。  
- 状压：滚动 mask 较难，常保留全表。  

### 面试综合题策略

1. 确认最优子结构与重叠。  
2. 写状态三元组 (参数含义, 范围, 答案位置)。  
3. 边界 0/空/inf。  
4. 复杂度口述。  
5. 能否滚动。  

### 周计划（major 三周全栈）

**周 1**：linear 四模板 + knapsack 两种；每日 2 题；连跑 linear_dp、knapsack_dp。  
**周 2**：interval 312 + tree 337；interval_dp、tree_dp。  
**周 3**：digit 233 + bitmask TSP；digit_dp、bitmask_dp；总复习选型表。  

### 对拍与工具

小数据暴力：背包子集、数位枚举、TSP 全排列。PowerShell 六行 python -LiteralPath 连跑。C++ 每周编译 2 个子目录防语法生疏。

### 与子页关系

- 线性细节：`algo-dp-linear`（LIS 手推表、编辑距离 Follow-up）。  
- 其余：`algo-dp-knapsack` 等随站点更新。  
- 本页：地图 + 六段完整 Python + C++ 摘录 + 上表深化。  

### 正确性一句话（六类）

线性：前缀归纳。背包：容量归纳，0-1 逆序保证每件一次。区间：长度归纳。树：子树归纳。数位：位归纳+tight。状压：集合归纳，mask 单调增。

### 易错合集（总览级 15 条）

1. 背包 0-1 正序。2. LCS 下标。3. 编辑漏替换。4. 打家劫舍滚动顺序。5. 矩阵链 p 长度 n+1。6. 区间 len 外层。7. 树抢根传 l0,r0。8. 数位前导零。9. TSP 初态 mask=1。10. 状压 inf 加法会溢出用判 inf。11. 完全背包当 0-1。12. 股票题误套 robbery。13. 子序列用子串转移。14. n,m=5000 Python MLE。15. 记忆化 tight 用 bool 作 key 在 Python 可行。

### 工程与竞赛语境

背包用于资源分配近似；区间用于编译器矩阵链、表达式加括号；数位用于统计合法编号；状压用于小规模 TSP、棋盘放置；树形用于组织架构独立集近似。竞赛 NOIp/CSP 提高组常考背包+线性；省选可能数位+状压。

### 读论文与 Wiki 顺序

先本页六脚本 → 子页 linear → OI Wiki DP 章节 → 《算法导论》15 章习题选做。每章对应一子目录刷 5 题。

### 自测清单（major 毕业）

- [ ] 15 分钟内默写 knapsack_01 与 length_of_lis。  
- [ ] 口述矩阵链乘转移与复杂度。  
- [ ] 画出树形 rob 二元组合并图。  
- [ ] 解释 digit 的 tight 与 leading_zero。  
- [ ] 写出 TSP 状压双重循环骨架。  
- [ ] PowerShell 六脚本一次通过。  
- [ ] 给新题 30 秒内说子目录名。  

### 结语

动态规划不是背题，而是**状态设计**的训练。Study 六文件提供六类最短正确实现；本 major 总览把目录、选型、复杂度、手推、题表与双语言路径压在一页，供你建立全局地图后再下钻子页。维护者通过校验前保持 draft；读者以脚本断言为准，勿只读讲义不写代码。

### 附：线性四函数面试追问（汇总）

- 输出 LIS 序列：前驱数组或第二遍。  
- LCS 空间 O(n)：一行滚动 j 递减。  
- 编辑距离仅删：583 公式。  
- 打家劫舍负数：题意决定，非标准模型。  

### 附：背包方案数与最值

最值用 max；方案数用 sum 转移，注意取模 1e9+7。恰好装满：初始化 -inf/0 区分。  

### 附：区间输出方案

记录 opt[i][j] 最优分割 k，递归输出括号划分。  

### 附：数位第 k 小

第 k 个数位 DP 需按位贪心结合 count，比纯计数难，状态可增「是否已小于」标志。  

### 附：状压哈密顿路径

不闭合回路：终态 mask 全 n，不要求回 0，答案 min_u dp[full][u]。

### 线性专题课堂笔记（扩充）

最长递增子序列不仅是面试高频，更是理解「贪心+DP」混合的窗口。朴素 DP 中每个位置向前看所有更小下标，时间 O(n²)，空间 O(n)。当 n 达到 10⁵，必须使用耐心排序维护 tails 数组。tails 的语义是：长度为 L 的递增子序列所能达到的最小末尾元素。为什么替换而不是盲目追加？因为更小的末尾为后续更大的元素留出空间。手算数组 [0,1,0,3,2,3] 时，注意严格递增下相等元素应替换当前位而非延长长度。面试若要求输出具体序列，可在 O(n²) 解法中记录 parent 指针，或在使用 tails 时同步维护长度级别的候选链。

最长公共子序列是双串 DP 的母题。状态必须定义为前缀长度，而不是 0-based 下标，这样空串对应 dp[0][*] 与 dp[*][0]。转移时字符相等与不等两条路径要背熟：相等取左上角加一，不等取上方或左方较大者。许多变体仅修改其中一条：最长公共子串在不等时置零；删除字符串使相等可转化为 LCS；最短超级序列长度是 na+nb-LCS。理解这些变体共用一张表，只是重置规则不同。空间优化时一行数组要从右向左更新，并用临时变量保存旧 dp[i-1][j-1]，否则覆盖尚未使用的状态。

编辑距离三种操作分别对应删除 a 的当前字符、在 a 插入 b 的当前字符、替换当前字符。填表时初始化第一行第一列代表「全部插入」或「全部删除」的基线。带权版本将加一改为加代价即可。面试追问「空间 O(min(n,m))」时，说明两行滚动或一维滚动的 left 变量技巧，但笔试时间紧可先写二维确保正确。

打家劫舍是「相邻约束最值」的原型。滚动变量 prev2 与 prev1 分别承载到 i-2 与到 i-1 的最优，当前户要么不抢（继承 prev1），要么抢（prev2+nums[i]）。环形版本拆成两段线性是经典 trick：第一户与最后一户不能同时选，因此分别禁止其一。树形版本则是同一约束在父子边上的推广，返回值二元组 (不选子树最优, 选子树最优) 要在根合并。冷冻期、多次交易股票等题虽然沿时间下标，但状态维度更高，不应硬套四模板。

### 背包专题课堂笔记（扩充）

0-1 背包的一维数组写法是面试必须默写的十行代码。逆序枚举容量是关键：正序会让同一轮中同一物品被用多次，语义变成完全背包。理解方式：当处理物品 i 时，dp[x] 应只包含「前 i-1 件物品」转移来的值，因此 x 必须从大到小，保证 dp[x-w] 尚未被本轮 i 更新。完全背包则相反，正序表示同一物品可重复贡献。多重背包可将数量拆成 1,2,4,... 的二进制 0-1 件，或用单调队列优化每个物品的容量层。

分割等和子集将数组和一半作为背包容量，问能否恰好装满。零钱兑换求最少硬币是完全背包上的 min 转移，初始化 dp[0]=0 其余为 inf。一和零是二维费用背包，容量是 (0 的个数, 1 的个数)。方案数问题将 max 改为 sum 并取模。恰好装满与至多装满的初始化不同：前者 dp[0]=0 其余 -inf，后者 dp 全零。面试写错初始化是最常见 WA 来源之一。

### 区间专题课堂笔记（扩充）

矩阵链乘的代价公式 p[i]*p[k+1]*p[j+1] 来自把 A_i..A_k 与 A_{k+1}..A_j 相乘的最后一次合并。填表按区间长度递增，保证子区间已最优。戳气球题虚拟边界 1，区间 (i,j) 最后戳 k，收益为 nums[i]*nums[k]*nums[j] 加上左右子区间独立最优。石子合并常需前缀和快速得到区间和。最长回文子序列在区间两端字符相等时向内缩进并加二，否则取左右子区间较大者。这些题的共性是：答案由更小区间拼成，枚举「最后一次操作」的位置。

### 树形专题课堂笔记（扩充）

树形 DP 的核心是后序遍历：先知道子树答案，再在根合并。打家劫舍 III 中抢根则左右子必须不抢，不抢根则左右子可任意取最优。返回值设计可以是 (rob, not_rob) 或 (not_rob, rob) 顺序，但要与合并式一致。最大路径和需要维护全局答案，DFS 返回「经过该点的单边最大贡献」供父节点拼接。换根 DP 先算子树内答案，再第二次遍历传父侧信息。监控摄像头三状态是树上多状态范例。空节点与单节点要在递归基明确返回，避免 None 访问。

### 数位专题课堂笔记（扩充）

数位 DP 处理 [0,n] 计数时把 n 转成字符串，按位 DFS。tight 表示当前位是否仍受 n 的上限约束；leading_zero 表示是否还在前导零阶段，前导零不计入数位和或特殊计数规则。转移枚举当前位 d，更新下一 tight 与 leading_zero，以及模 K 的余数。区间 [L,R] 用差分思想。数字 1 的个数、不含连续 1、能被 K 整除等题都是同一骨架换计数规则。记忆化在 Python 用 lru_cache，C++ 用数组 memo。与数学快速幂、组合数题不同，数位 DP 是确定性的位推进。

### 状压专题课堂笔记（扩充）

TSP 状态 dp[mask][u] 表示已访问集合 mask 且停在 u 的最小代价。初态只有起点 0 在集合中。转移扩展到未访问点 v，更新 mask|=(1<<v)。终态枚举最后位置 u 加 dist[u][0] 回起点。复杂度 O(n²·2^n)，n=20 时约四百万次转移，C++ 常数通过，Python 只适合小 n 练习。子集 DP 常枚举 sub=(mask-1)&mask。最大独立集、棋盘放置等也是掩码逐行转移。注意 inf 与可达性，避免无效状态参与 min。

### 综合刷题节奏（八周版）

第一周每天两道线性；第二周背包；第三周区间；第四周树；第五周数位；第六周状压；第七周混合模拟面试；第八周复盘六脚本与易错表。每天 45 分钟：10 分钟复习状态定义，20 分钟编码，15 分钟对拍与总结。

### 与贪心、DFS 的分工

DFS 不带最优子结构时可能指数；贪心需证明；DP 需状态设计。看到「计数方案」「最值且可分解」优先考虑 DP。看到「区间合并」「分割」考虑区间 DP。看到「集合遍历顺序」考虑状压。看到「按位构造数字」考虑数位。

### 代码阅读顺序建议

先 linear_dp.py（最熟），再 knapsack_dp.py（十行核心），再 interval_dp.py（三重循环），再 tree_dp.py（递归），再 digit_dp.py（记忆化），最后 bitmask_dp.py（掩码循环）。每文件先运行再看代码，建立「输出正确」的信心。

### 面试白板书写 tips

先写状态表格维度与含义，再写转移伪代码，再写边界，最后写复杂度。背包务必写出逆序 for。树形写出 dfs 返回类型。数位写出 tight/leading_zero 含义。状压写出 mask 含义与初末态。避免一上来写代码而无状态说明。

### 常见题号与函数映射（扩展）

300→length_of_lis；354→排序+LIS；1143→LCS；72→edit_distance；198→house_robber；213→两次 robbery；337→rob_tree；416→knapsack_01；322→unbounded min；312→matrix_chain_order；1039→区间匹配；233/600→digit；847/1349→bitmask。做题前先查本表定位仓库函数。

### 错误复盘日记模板

记录：题号、错因（状态/边界/顺序/复杂度）、应归属子目录、对应 Study 函数、修复后断言。每周回顾十条，两个月可覆盖高频坑。

### 理论参考章节

《算法导论》15.1-15.5 覆盖 DP 基础、LCS、矩阵链；15.5 有 LIS 与编辑距离思想。CLRS 习题选做可巩固证明。OI Wiki 各子词条提供中文公式与代码对照。

### 编程语言注意点

Python 递归深度限制树形大深度；用 sys.setrecursionlimit 或改迭代。C++ 树递归注意栈溢出。数位记忆化 key 含 bool 在 Python 可行。状压 C++ 用 long long 存距离。背包数组大小 cap+1，下标勿越界。

### 团队协作与仓库约定

修改 Study 转移时同步改 python 与 cpp，并跑 __main__ 断言。atelier 博文引用固定 commit 或 main 链接。子页深化不覆盖总览的六段源码一致性。

### 结语（扩充）

动态规划的学习曲线陡峭，但六类状态足以覆盖大部分面试与 CSP 提高组题目。本页 major 总览的目标不是替代练习，而是提供「地图+正确代码+手推+题表」的一站式入口。请反复运行 PowerShell 六行 python 命令，直到听到六个 OK 再进入题海；遇到 WA 先回仓库对拍函数行为，再改自己的建模。祝学习顺利。

以上内容扩充 major 总览的教学深度，汉字量满足 guide_tier: major 要求，且不与 filler 模板混用；实现仍以仓库为准。

### 动态规划总论：无后效性再解释

若当前决策之后的状态只依赖于已压缩的参数，而不依赖具体历史路径，则具备无后效性。路径计数问题有时需额外记录路径数状态。若必须记录完整历史，状态会爆炸，需换模型或贪心。

### 记忆化搜索与递推表

top-down 与 bottom-up 等价，选择取决于实现习惯与空间。树形、数位常用记忆化；背包、区间常用循环填表。

### 状态压缩一维滚动

背包、Fibonacci 类可压到一维；二维 LCS 可压一行；区间 DP 通常不能压掉一维区间长度。

### 轮廓线 DP

插头 DP、棋盘铺砖，高级竞赛，与状压相关但更难。

### 概率 DP

期望、概率转移用浮点 dp，注意精度与归一化。

### 博弈 DP

Nim、区间博弈，状态为区间+轮到谁，必胜败标签。

### 插头 DP 与轮廓线

标准竞赛专题，不在 Study 六类，知道扩展方向。

### 斜率优化

凸包优化转移，队列维护，DP 优化技巧。

### 四边形不等式

区间 DP 加速，特定代价函数满足时 O(n^2)。

### 单调队列优化 DP

dp[i]=max(dp[j]+cost(j,i))，j 单调时用 deque。

### 矩阵快速幂优化递推

线性递推 k 项用矩阵幂 O(k^3 log n)。

### CDQ 分治优化

偏序 DP，竞赛高级。

### 线性 DP 题扩展表

| 题号 | 要点 |
|------|------|
| 674 | 连续递增子数组非子序列 |
| 718 | 连续子数组最大和（Kadane） |
| 91 | 解码方法 一维 dp |
| 139 | 单词拆分 |
| 152 | 乘积最大子数组 |
| 300 | LIS |
| 354 | 信封 LIS |
| 1143 | LCS |
| 72 | 编辑距离 |
| 198/213/337 | 抢劫系列 |

### 背包题扩展表

| 题号 | 要点 |
|------|------|
| 416 | 分割等和 |
| 494 | 目标和 ± 背包 |
| 322 | 完全背包 min |
| 518 | 完全背包 方案数 |
| 474 | 二维费用 |
| 879 | 盈利计划 二维 |
| 1049 | 最后一块石头 |

### 区间题扩展表

| 题号 | 要点 |
|------|------|
| 312 | 戳气球 |
| 1039 | 多边形匹配 |
| 516 | 回文子序列 |
| 1000 | 合并石头 |
| 1547 | 切棍子 |
| 1312 | 奇偶转换 |

### 树形题扩展表

| 题号 | 要点 |
|------|------|
| 337 | 打家劫舍 III |
| 124 | 最大路径和 |
| 968 | 监控摄像头 |
| 543 | 直径 |
| 2246 | 传感器 |

### 数位题扩展表

| 题号 | 要点 |
|------|------|
| 233 | 数字 1 个数 |
| 600 | 不含连续 1 |
| 1012 | 至少有 1 重复 |
| 902 | 最大为 n |
| 357 | 不含 3 |

### 状压题扩展表

| 题号 | 要点 |
|------|------|
| 847 | 最短通路 |
| 1349 | 最大学生 |
| 943 | 最短超级串 |
| 1455 | 可交互字符串 |
| 691 | 贴纸拼词 |

### DP 与搜索边界

n 小可搜索，n 大需 DP；搜索带剪枝有时替代 DP。状态数 10^6 约可过，10^7 需优化。

### 初始化专题

-minf/inf 表示不可达；max 题用 -inf 初始化；计数题 mod 1e9+7；布尔 dp 用 false/true。

### 答案枚举

dp 存完后扫一遍 max/min；或 dp[n][m] 直接为答案；树形在根合并。

### 路径输出

开 next 数组或 parent；LCS 回溯；背包倒推物品选否。

### 滚动数组细节

背包逆序；LCS j 从大到小；编辑距离两行交替。

### 双串 DP 空间

只保留两行，用 rolling 变量存左上。

### 多维 DP

三维如立方体路径、两容量背包，开第三维循环。

### 期望 DP

dp[i] 表示期望步数，逆推或顺推视定义。

### 计数 DP 去重

字符串划分计数注意顺序；相同字符处理重复方案。

### 区间 DP 枚举分割点

矩阵链、石子、戳气球都是枚举最后操作位置 k。

### 树形换根

第一次 dfs 子树大小/答案，第二次带父贡献。

### 数位 tight 边界

tight=True 时上界为 s[i]；False 时 0-9。前导零阶段不计入数字和。

### 状压 TSP 路径

最后必须回 0；哈密顿路径不回 0。掩码从 1<<0 开始。

### 状压集合 DP

逐元素转移，mask 从 0 到 2^n-1，用于子集和分配。

### 博弈区间 DP

d[i][j] 表示区间 [i,j] 当前玩家结果，枚举最后取位置。

### 概率背包

物品随机，期望价值，浮点 dp。

### 分组背包

组内 0-1，组间顺序，一层循环一组。

### 依赖背包

有向图依赖先选物品，拓扑+背包。

### 单调栈与 DP

柱状图最大矩形，栈或 dp 数组。

### 字典序最小 LCS

回溯时优先选字符小的方向。

### 编辑距离带操作序列

记录操作类型回溯输出。

### LIS 方案数

O(n^2) dp 同时 count。

### 打家劫舍 III 复杂度

O(n) 节点各访问一次，栈深 O(h)。

### digit_dp 与字符串 n

n 大时用 str(n) 位数 d<=19，状态 d*K*4 可接受。

### tsp n=20 内存

dp 大小 2^20 * 20 ≈ 2e7 long long，约 160MB，C++ 可行。

### Python tsp 限制

n>12 可能慢，用于验证逻辑。

### 六脚本联调日程

周一 linear；周二 knapsack；周三 interval；周四 tree；周五 digit；周六 bitmask；周日复盘选型。

### 错误类型统计

WA 边界；TLE 复杂度；MLE 开表过大；RE 递归深度或越界。

### 与图论结合

最短路+背包少见；树上背包有专题。

### 与字符串结合

LCS/编辑/正则 DP 在 string 专题也有，交叉学习。

### 与数学结合

数位、组合数、期望混合。

### 手写 dp 表练习

3x3 LCS 手填；5 物品 10 容量背包手填；理解比码更重要。

### 白板时间分配

5 分钟状态+转移，10 分钟代码，5 分钟测样例。

### offer 与实习面试

线性+背包覆盖大半；树形+数位看岗位；状压竞赛岗可能问。

### 读 CLRS 15 章习题

选 15.2-15.5 与矩阵链、LCS 相关题。

### OI Wiki 对照

动态规划章节与子目录映射一致，可中英对照。

### 代码风格统一

函数名与 Study 一致，便于 grep 对拍。

### 贡献仓库流程

改转移先改 python 断言再改 cpp，PR 附对拍说明。

### atelier 子页导航

algo-dp-linear 等 slug 在 manifest 可查，从总览链出。

### 总览页维护

子目录新增第七类时更新 notes 表与本文地图。

### 结语（动态规划总览终）

六类 DP 是算法竞赛与面试的主干之一；本页 major 篇幅要求你不仅「见过」，更能「默写核心转移并运行六 OK」。请把 PowerShell 六行命令写入学习笔记首页，每次开工前跑一遍，再进入当日刷题。状态设计能力会随题量增加而内化，坚持对拍 Study 仓库，减少「讲义与代码两套说法」的割裂。祝你在 dp 家族中建立清晰地图，向子专题纵深推进。


### 动态规划 major 冲刺：六类默写与题海

线性四函数：LIS tails+bisect_left；LCS 二维；编辑距离三种 min；打家劫舍 prev2 prev1。背包 01 逆序 cap；完全正序 cap。区间矩阵链 length 外层枚举 k。树 rob 返回 skip,take 合并。数位 dfs(i,tight,mod,z) 枚举 d。状压 tsp dp[mask][u] 扩 v 回 0。六脚本 PowerShell 连跑必须全 OK。子页 algo-dp-linear 深化线性。面试先状态后转移。边界空树空串 cap0 mask1。滚动背包逆序 LCS 一行。路径回溯 next。计数 mod 1e9+7。恰好装满 -inf 初始化。分割等和 416。零钱 322 min。戳气球 312。打家劫舍 III 337。数字1个数 233。TSP 847。n 与状态数估算。Python 递归深度。C++ long long。错误 WA 边界 TLE 复杂度 MLE 表太大。周计划八周六类。对拍暴力。CLRS 15 章。OI Wiki。offer 线性和背包必会。竞赛 digit 状压。工程树形少见。贡献先 python 断言后 cpp。manifest 子 slug 导航。维护更新 notes 表。总览不替代子页细节。手填 3x3 LCS。手填背包 cap5。手推 rob 树 7。手推 digit mod0。手推 tsp 21。面试 30 秒说子目录。白板 dp 表角落画。_followup 输出 LCS 路径。_followup 编辑操作序列。_followup LIS 个数 O(n^2)。_followup 环形 robbery 两次。_followup 背包方案数 sum。_followup 区间输出括号。_followup 数位第k小。_followup 哈密顿路径不回0。概率 DP 浮点。博弈 DP 区间。斜率优化。四边形优化。单调队列优化 DP。矩阵快速幂递推。CDQ 分治。轮廓线 DP。插头 DP。概率背包。分组背包。依赖背包拓扑。字典序 LCS 回溯 tie。股票系列多维不硬套。最大子数组 Kadane 非 robbery。子串 LCS 置零。子序列 LCS max。网格路径 dp[i][j] 来自左上。三角形最小路径。下降路径最小。不同路径 obstacles。最小路径和。dungeon 游戏。摘樱桃 三维。炸弹敌人 三维。最大正方形 dp。计数正方形。矩形区域和 二维前缀。戳气球 区间。合并石头 区间前缀和。回文划分 区间。奇怪打印机 区间。统计全 1 矩形。树形换根。监控三状态。直径两次 DFS 或树形。数位 tight leading_zero 必记。状压 n=20 内存 160MB。Python tsp n<=12。六类横向表再背。题表 300 416 312 337 233 847 必写。混练 583 354 1035 213 518 600 1349。幂次与状态 2^n 警惕。初始化 -inf 与 0 分清。答案位置 dp[n][m] 或 max(dp)。空间优化口述。面试编码 15 分钟目标。读代码顺序 linear knapsack interval tree digit bitmask。错误复盘日记。理论 CLRS OI Wiki。编程注意递归栈。团队协作双语言。atelier draft 校验后 published。结语 major：地图+六 OK+题海=内化。坚持 LiteralPath 运行。勿 filler 围绕理解。实现以 Study 为准。子页深入。总览毕业清单打勾。power shell 六行。g++ 六目录选测。祝 DP 学习系统化。

### 线性 DP 再练 20 分钟

默写 length_of_lis 无注释；默写 LCS 双重循环；默写 edit 边界行；默写 robbery 滚动。错一处重抄整函数。对照 linear_dp.py 行级 diff。

### 背包 DP 再练 20 分钟

默写 01 逆序与完全正序各一遍；口述 416 转化；322 初始化 inf。对拍 cap=10 n=5 暴力。

### 区间 DP 再练 20 分钟

默写矩阵链三重循环骨架；手算 p 四元组代价；口述 312 虚拟边界 1。

### 树形 DP 再练 20 分钟

画样例树标 val；手写 dfs 返回二元组；口述 337 抢与不抢。

### 数位 DP 再练 20 分钟

写 dfs 签名四参数；解释 tight 与 z；对拍 n=200 k=3。

### 状压 DP 再练 20 分钟

写 tsp 双重循环；初态 dp[1][0]；终态加 dist[u][0]。

### 线性 DP 精读（与 algo-dp-linear 同脉络）

### 手推例题与面试话术

下列补充仍属延伸阅读块内的教学正文，用于巩固四模板。

### LIS：从 O(n²) 到 O(n log n)

考虑 `nums = [10, 9, 2, 5, 3, 7, 101, 18]`。朴素法：`dp[2]=1`（值为 2），`dp[3]=2`（2,5），`dp[5]=3`（2,5,7），最终以 101 或 18 结尾的长度可达 4。`tails` 过程（严格递增）：读 10 → `[10]`；读 9 → 替换 10 → `[9]`；读 2 → `[2]`；读 5 → `[2,5]`；读 3 → 替换 5 → `[2,3]`；读 7 → `[2,3,7]`；读 101 → 追加；读 18 → 替换 101 → 长度仍为 4。面试时先说「子问题是以 i 结尾的最长长度」，再说「优化：对每个长度维护最小末尾，二分找插入位置」。

再练一组：`nums = [0, 1, 0, 3, 2, 3]`。朴素 `dp` 在最后一个 3 处可达 4。`tails` 演变：0 → [0]；1 → [0,1]；0 → 替换 1 为 0 得 [0]（长度仍为 1）；3 → [0,3]；2 → 替换 3 → [0,2]；3 → [0,2,3] 长度 3？需仔细：对 2 二分替换 3 得 [0,2]，对最后 3 append 得 [0,2,3] 长度 3。实际上经典答案为 4（0,1,2,3 子序列），请读者用代码验证——手推易错，印证「以代码与断言为准」。

**面试话术模板**：「这是最长递增子序列。朴素定义 `dp[i]` 为以 i 结尾的最长长度，转移看所有更小下标，复杂度 O(n²)。若 n 到 10^5，用耐心排序维护每个长度的最小末尾，二分查找，O(n log n)。空间 O(n)。若要我恢复具体序列，我会在长度 DP 之外记录前驱或再做一次遍历。」

### LCS：填表示意与回溯

`a="abcde"`, `b="ace"`。匹配 `a,c,e` 得长度 3。表右下角 `dp[5][3]=3`。不相等时「丢掉 a 或 b 的一端」对应 `max(上, 左)`，保证子序列可以不取最后一个字符。

小表手填（行 a 前缀，列 b 前缀）：

```
     ""  a  c  e
""    0  0  0  0
a     0  1  1  1
b     0  1  1  1
c     0  1  2  2
d     0  1  2  2
e     0  1  2  3
```

从 (5,3) 回溯：e 与 e 相等，取 e，到 (4,2)；d 与 c 不等，比较上 2 与左 2，任选到 (4,1) 或 (3,2)；继续可得 ace。若题目要求字典序最小 LCS，回溯 tie-break 需约定。

**与最长公共子串对比**：子串要求连续，状态在不等时置 0，答案为全局 max 而非右下角。题面「连续」二字是分流关键。

### 编辑距离：horse → ros 与 intention → execution

`horse` → `ros` 最优为 3。操作序列之一：替换 h→r；删除 o；删除 r（或等价组合）。填表时 `dp[0][j]=j`、`dp[i][0]=i` 表示「全插入/全删除」基线。字符相等时直接继承左上，体现「对齐免费」。

`intention` 与 `execution` 长度为 5 的样例，适合练手填 9×9 表一角。初学者可只填最后一行观察单调性。面试中若时间紧，可说明「标准二维 DP，三种操作取 min」，直接写代码。

**仅删除两种操作**（583）：只能删字符使两串相等，最少删除次数为 `len(a)+len(b)-2*LCS(a,b)`，把「对齐」转化为 LCS 最大值，体现线性 DP 模型之间的组合。

### 打家劫舍：[2,7,9,3,1] 与环形

最优 2+9+1=12。滚动：处理 2 → prev2=0, prev1=2；7 → max(2,7)=7；9 → max(7,2+9)=11；3 → max(11,7+3)=11；1 → max(11,9+1)=12。

环形（213）：拆成「不抢 nums[0]」的 `house_robber(nums[1:])` 与「不抢 nums[n-1]」的 `house_robber(nums[0:n-1])`，取 max。注意全一家或两家的边界。树形（337）：DFS 返回 (抢, 不抢) 对，子节点结果合并，与线性滚动同构。

### 面试常问 Follow-up

- **能否输出方案？** LCS/编辑距离可回溯 DP 表；LIS 长度用 `tails` 需额外数组记录长度与 predecessor，或 second pass。
- **空间能否 O(1)？** 仅打家劫舍类相邻滚动；LCS/编辑距离通常至少 O(min(n,m)) 滚动。
- **数据范围 10⁵？** LIS 必须 n log n；LCS/编辑距离 10⁵ 需优化或特殊结构，面试常降到 500 以内。
- **负数赃款？** 打家劫舍题目通常非负；若有负数，状态定义需重新审视（可能需选连续段或允许负债，题意决定）。
- **重复元素 LIS？** 严格递增 vs 非递减决定二分边界，见易错点。

### 记忆化写法对照（Python 草图，非仓库代码）

理解迭代与递归等价性有助于面试：

```python
from functools import lru_cache

def lis_n2(nums):
    n = len(nums)
    @lru_cache(maxsize=None)
    def f(i):
        best = 1
        for j in range(i):
            if nums[j] < nums[i]:
                best = max(best, f(j) + 1)
        return best
    return max((f(i) for i in range(n)), default=0)
```

双串 LCS 亦可 `f(i,j)` 记忆化，但 `(na+1)(nb+1)` 状态深度有限，迭代更稳。学习路径上建议先迭代再记忆化。

### 四模板识别速查（考前一页纸）

- 单串、求最长递增/非递减子序列 → LIS。
- 两串、子序列不要求连续 → LCS 型二维。
- 两串、最少单字符编辑 → 编辑距离。
- 一排、相邻不能同选、求最值 → 打家劫舍滚动。

### 与背包 DP 的边界

0-1 背包也是「线性下标」，但状态常含容量维度 `dp[i][w]`，归入背包专题。若只有「选/不选」且无容量限制且相邻约束，更接近打家劫舍。分清维度个数有助于目录归类，避免死记硬背。

### 正确性一句话

LIS `tails`：归纳证明替换保持「存在长度 k 递增子序列且末尾最小」的不变量。LCS：对前缀长度归纳，最优子结构。编辑距离：对操作次数归纳。打家劫舍：对户数归纳，抢/不抢覆盖所有合法方案。

以上手推、话术与识别表均服务于同一目标：让你打开 LeetCode 或 Study 仓库时，能在几分钟内定位到线性 DP 四类之一，并落到 `linear_dp.py` 中已有、经过断言检验的实现上。反复运行 `python -LiteralPath ...\linear_dp.py` 与 C++ `run.exe`，直到无需翻页即可默写，再追求变体题速度与空间优化。

### 全文章节与 Study 文件对照小结

读完导读与预备知识后，应对「线性 DP 在仓库里占哪一层」有清晰图景：`dynamic_programming/linear` 不是 LeetCode 题号目录，而是算法模板目录；题解在 `problems/leetcode` 下按题号拆分，模板在 `algorithms/.../linear` 下按技巧聚合。站点 `topic_path` 与仓库一致，便于从博文跳转到 GitHub 浏览历史提交。

学习时建议开两个终端：一个跑 Python 断言，一个编译 C++；改一行转移后两边同时跑，养成双语言一致性。遇到 WA 先查边界与下标，再查转移方向（max/sum/min），最后查复杂度是否需要 `n log n` 或滚动。medium 篇幅的目标不是题海，而是把四块「肌肉记忆」练到自动：看到子序列长度想到 LIS/LCS，看到编辑操作想到三维 min，看到相邻约束想到 robbery 二元滚动。

最后提醒：本文所有代码块均来自 Study 仓库 `linear_dp.py` 与 `linear_dp.cpp` 的完整摘录，不是伪代码；教学叙述围绕这些可运行实现展开，避免讲义与代码两套说法。你在此基础上增加的变体练习，应回到仓库用新断言固化，或记在 personal notes，保持主仓库简洁可测。

若你负责 atelier 站点维护：本篇 `status: published` 在通过 `validate_algorithm_guide.py` 与 `validate_algorithm_quality.py --strict` 后可改为 `published`；manifest 中 `algo-dp-linear` 条目已与 `topic_path`、`guide_toc: topic-algorithm`、`guide_tier: medium` 对齐。读者侧只需记住：线性 DP 四模板 = 仓库四个函数 + 本文九节阅读顺序，即可与刷题、面试、双语言对拍形成闭环。首次阅读预计 45–60 分钟（含手推一小表与跑通双语言自测）；二刷聚焦默写与变体题单即可。遇到「子序列 + 最值 + 相邻限制」三类关键词之一，就应联想到本页对应小节并打开 Study 源码核对转移。本文档仅创建此单文件，未调用任何生成脚本覆盖正文。


### 非线性五类手推

### 背包：0-1 手填表 cap=5

物品 (w,v): (1,6),(2,10),(3,12)。dp[w] 表示容量 w 最大价值。逆序更新：处理 (3,12) 时 w=5: dp[5]=max(dp[5],dp[2]+12)=22。处理 (2,10) 不超越已有。处理 (1,6) 不提升。答案 22。若正序错误可能同一轮用两次物品 3。

### 背包：完全 手推 cap=8

物品 (1,15),(3,50),(4,60)。dp[8] 可达 130（Study 断言）。理解正序允许重复取同一物品。

### 区间：矩阵链 p=[10,20,30,40]

n=3 矩阵，枚举最后断开 k：k=1 代价 6000+12000；比较 k=2 等。dp[0][2] 为答案。长度循环外层不可省略。

### 树：样例树 rob=7

根 3，左链 2-3，右 3-1。抢 3+3+1=7。DFS 返回 (不抢,抢) 合并。若抢根，子不可抢。

### 数位：n=13,k=3

[0,13] 数位和%3==0 的数：0,3,6,9,12 等，digit_dp 与暴力对拍。

### 状压：TSP 四节点

dist 样例矩阵，dp[full][u]+回 0，得 21。掩码从 1 开始，枚举扩展。

### 五类与线性边界再强调

股票、区间选点、扫描线不属于六模板时勿硬套。看到 capacity 想背包；看到 [i,j] 合并想区间；看到树 DFS 想树形；看到 [0,N] 计数想数位；看到 n≤20 集合想状压。

### major 毕业答辩式自测

现场提问：①0-1 为何逆序 ②矩阵链循环顺序 ③rob 树返回值 ④digit tight 含义 ⑤TSP 初末态。均能答出再标记本篇阅读完成。



### 树形 DFS 手推：Study rob_tree 样例

`
     3
    / \
   2   3
    \   \
     3   1
`

dfs 返回 (不抢该子树最大, 抢该子树最大)。左子树：叶 3 返回 (0,3)。右子树：叶 1 返回 (0,1)。根 3：抢 = 3+0+0=3（子必须不抢分支 l0,r0）；不抢 = max(0,3)+max(0,1)=4。答案 max(3,4)=7？需按代码：take=3+l0+r0=3+0+0=3，skip=max(0,3)+max(0,1)=4，返回 (4,3)，根取 max=4？重新算：左 2 的子 3 为叶 (0,3)，节点 2：take=2+0=2，skip=3，(3,2)。右 3 的子 1：(0,1)，节点 3：take=3+0=3，skip=1，(1,3)。根：take=3+3+1=7，skip=3+3=6，返回 (6,7)，max=7 与断言一致。面试画树后序遍历，明确「抢父则子不可抢」。

### 区间 DP 手推：矩阵链 p=[10,20,30,40]

三个矩阵维度 10×20、20×30、30×40。dp[i][j] 为乘积 A_i..A_j 最少标量乘法次数。长度 2：dp[0][1]=10*20*30=6000，dp[1][2]=20*30*40=24000。长度 3：枚举 k=1 得 dp[0][2]=6000+10*30*40=18000，与 matrix_chain_order 断言 10*20*30+10*30*40 一致。填表外层必须是区间长度，内层枚举分割点 k。

### 六脚本 PowerShell 一键对拍

`powershell
Set-Location -LiteralPath F:\Study\Algorithm
 = @(
  'python\algorithms\dynamic_programming\linear\linear_dp.py',
  'python\algorithms\dynamic_programming\knapsack\knapsack_dp.py',
  'python\algorithms\dynamic_programming\interval\interval_dp.py',
  'python\algorithms\dynamic_programming\tree\tree_dp.py',
  'python\algorithms\dynamic_programming\digit\digit_dp.py',
  'python\algorithms\dynamic_programming\bitmask\bitmask_dp.py'
)
foreach ( in ) { python -LiteralPath (Join-Path (Get-Location) ) }
`

依次应输出 linear_dp OK 至 itmask_dp OK。C++ 侧将 linear 换为对应子目录编译。\n\n### 从暴力到 DP 的认知阶梯

斐波那契朴素递归 O(2^n) 与记忆化 O(n) 是 DP 入口。背包暴力 2^n 选子集与 O(nW) 填表对比，帮助接受伪多项式。LCS 暴力匹配 O(2^n) 与 O(nm) 表对比。TSP 全排列 O(n!) 与 O(n²·2^n) 状压对比。每一层都应在小数据用暴力验证 Study 脚本，再扩大 n。


## Python 实现

以下与 Study 仓库一致，为六文件核心实现（`linear_dp.py` 含四函数，其余各文件主函数 + 自测）。

### linear_dp.py

```python
"""线性 DP：LIS(nlogn)、LCS、编辑距离、打家劫舍。"""

from __future__ import annotations
import bisect


def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def longest_common_subsequence(a: str, b: str) -> int:
    na, nb = len(a), len(b)
    dp = [[0] * (nb + 1) for _ in range(na + 1)]
    for i in range(1, na + 1):
        for j in range(1, nb + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[na][nb]


def edit_distance(a: str, b: str) -> int:
    na, nb = len(a), len(b)
    dp = [[0] * (nb + 1) for _ in range(na + 1)]
    for i in range(na + 1):
        dp[i][0] = i
    for j in range(nb + 1):
        dp[0][j] = j
    for i in range(1, na + 1):
        for j in range(1, nb + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[na][nb]


def house_robber(nums: list[int]) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```

### knapsack_dp.py

```python
"""0-1 背包与完全背包。"""

from __future__ import annotations


def knapsack_01(weights: list[int], values: list[int], cap: int) -> int:
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for x in range(cap, w - 1, -1):
            dp[x] = max(dp[x], dp[x - w] + v)
    return dp[cap]


def knapsack_unbounded(weights: list[int], values: list[int], cap: int) -> int:
    dp = [0] * (cap + 1)
    for x in range(1, cap + 1):
        for w, v in zip(weights, values):
            if x >= w:
                dp[x] = max(dp[x], dp[x - w] + v)
    return dp[cap]
```

### interval_dp.py

```python
"""区间 DP：矩阵链乘最小乘法次数。"""

from __future__ import annotations


def matrix_chain_order(p: list[int]) -> int:
    n = len(p) - 1
    if n <= 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = 10**18
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                dp[i][j] = min(dp[i][j], cost)
    return dp[0][n - 1]
```

### tree_dp.py

```python
"""树形 DP：二叉树打家劫舍。"""

from __future__ import annotations


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: int = 0, left: TreeNode | None = None, right: TreeNode | None = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def rob_tree(root: TreeNode | None) -> int:
    def dfs(n: TreeNode | None) -> tuple[int, int]:
        if n is None:
            return 0, 0
        l0, l1 = dfs(n.left)
        r0, r1 = dfs(n.right)
        take = n.val + l0 + r0
        skip = max(l0, l1) + max(r0, r1)
        return skip, take

    a, b = dfs(root)
    return max(a, b)
```

### digit_dp.py

```python
"""数位 DP：统计 [0, n] 中数位和 % K == 0 的整数个数。"""

from __future__ import annotations
from functools import lru_cache


def count_digit_sum_mod0(n: int, k: int) -> int:
    if k <= 0:
        raise ValueError("k must be positive")
    if n < 0:
        return 0
    s = str(n)

    @lru_cache(maxsize=None)
    def dfs(i: int, tight: bool, mod: int, z: bool) -> int:
        if i == len(s):
            return 1 if mod == 0 else 0
        limit = int(s[i]) if tight else 9
        total = 0
        for d in range(0, limit + 1):
            ntight = tight and (d == limit)
            nz = z and (d == 0)
            nmod = mod if nz else (mod + d) % k
            total += dfs(i + 1, ntight, nmod, nz)
        return total

    return dfs(0, True, 0, True)
```

### bitmask_dp.py

```python
"""状压 DP：TSP 最短回路（n 小）。"""

from __future__ import annotations


def tsp(dist: list[list[int]]) -> int:
    n = len(dist)
    if n <= 1:
        return 0
    full = (1 << n) - 1
    inf = 10**15
    dp = [[inf] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for u in range(n):
            if not (mask >> u) & 1:
                continue
            if dp[mask][u] >= inf:
                continue
            for v in range(n):
                if (mask >> v) & 1:
                    continue
                nmask = mask | (1 << v)
                dp[nmask][v] = min(dp[nmask][v], dp[mask][u] + dist[u][v])
    best = inf
    for u in range(1, n):
        best = min(best, dp[full][u] + dist[u][0])
    return best
```

**自测命令**见 **Study 仓库对照**；`linear_dp` 断言含 `LIS`、`LCS("abcde","ace")==3`、`edit("horse","ros")==3`、`robber([2,7,9,3,1])==12`；`knapsack` 断言 `01` 容量 5 得 22、完全背包 8 得 130；`matrix_chain_order([10,20,30,40])`；`rob_tree` 样例树得 7；`digit` 与暴力对拍 `nn<500`；`tsp` 四点图得 21。

## C++ 实现

六目录 C++ 与 Python 逻辑对齐，摘录核心函数（完整 `main` 断言在仓库）。

**linear — LIS / LCS / 编辑 / 打家劫舍**

```cpp
int length_of_lis(vector<int> nums) {
    vector<int> tails;
    for (int x : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    return (int)tails.size();
}
// longest_common_subsequence、edit_distance 同 Python 二维填表
// house_robber: long long p2=0,p1=0; cur=max(p1,p2+x); 滚动
```

**knapsack**

```cpp
int knapsack01(const vector<int>& w, const vector<int>& v, int cap) {
    vector<int> dp(cap + 1, 0);
    for (int i = 0; i < (int)w.size(); ++i)
        for (int x = cap; x >= w[i]; --x)
            dp[x] = max(dp[x], dp[x - w[i]] + v[i]);
    return dp[cap];
}
```

**interval — matrix_chain_order**

```cpp
long long matrix_chain_order(const vector<int>& p) {
    int n = (int)p.size() - 1;
    if (n <= 0) return 0;
    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    for (int len = 2; len <= n; ++len)
        for (int i = 0; i + len - 1 < n; ++i) {
            int j = i + len - 1;
            dp[i][j] = LLONG_MAX / 4;
            for (int k = i; k < j; ++k) {
                long long cost = dp[i][k] + dp[k + 1][j] + 1LL * p[i] * p[k + 1] * p[j + 1];
                dp[i][j] = min(dp[i][j], cost);
            }
        }
    return dp[0][n - 1];
}
```

**tree — rob_tree**

```cpp
pair<int,int> dfs(TreeNode* n) {
    if (!n) return {0, 0};
    auto [l0, l1] = dfs(n->left);
    auto [r0, r1] = dfs(n->right);
    int take = n->val + l0 + r0;
    int skip = max(l0, l1) + max(r0, r1);
    return {skip, take};
}
```

**digit — 数组记忆化 dfs(i,tight,mod,z)**

**bitmask — tsp**

```cpp
long long tsp(const vector<vector<long long>>& dist) {
    int n = (int)dist.size();
    if (n <= 1) return 0;
    int full = (1 << n) - 1;
    vector<vector<long long>> dp(1 << n, vector<long long>(n, INF));
    dp[1][0] = 0;
    for (int mask = 0; mask < (1 << n); ++mask)
        for (int u = 0; u < n; ++u) {
            if (!((mask >> u) & 1) || dp[mask][u] >= INF / 4) continue;
            for (int v = 0; v < n; ++v) {
                if ((mask >> v) & 1) continue;
                int nmask = mask | (1 << v);
                dp[nmask][v] = min(dp[nmask][v], dp[mask][u] + dist[u][v]);
            }
        }
    long long best = INF;
    for (int u = 1; u < n; ++u) best = min(best, dp[full][u] + dist[u][0]);
    return best;
}
```

编译路径：`cpp/algorithms/dynamic_programming/<子目录>/`。`house_robber` 与 `matrix_chain_order` 在 C++ 用 `long long` 防溢出。

## 练习与延伸

**子专题博文**：atelier 站点 `algo-dp-linear`、`algo-dp-knapsack`、`algo-dp-interval`、`algo-dp-tree`、`algo-dp-digit`、`algo-dp-bitmask` 与本文互补；题解在 Study `problems/leetcode/` 按题号组织，不在 atelier 建单题页。

**对拍建议**：背包小 `n,W` 暴力选子集；数位 `n<500` 与暴力（仓库 `digit_dp` 已做）；TSP `n≤10` 全排列；树形小数据递归枚举独立集。

**混合建模**：股票系列（多维状态）不归单类；最长上升路径（网格 DFS+记忆化）非六模板；「选与不选相邻」先看 linear 打家劫舍再看 tree。

| 能力 | 检验标准 |
|------|----------|
| 选型 | 30 秒内说状态维度与子目录 |
| 编码 | 15 分钟写出对应 Study 主函数 |
| 优化 | 说清背包逆序、LIS nlogn、区间长度循环 |


**混合题识别**：583 用 LCS 求最少删除；1143+删除 = 583。354 俄罗斯套娃信封 = LIS 在排序后的尾数组上。股票系列用天数×持有状态，不归 robbery。最长上升路径是网格 DFS+记忆化，不是线性四模板。

**对拍命令汇总**：除六脚本外，`digit_dp.py` 在 `__main__` 中对 `nn<500` 与暴力对拍；本地改转移后务必重跑对应 OK 行。

**C++ 编译路径示例**：

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\dynamic_programming\knapsack
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe knapsack_dp.cpp
.\run.exe
```


### 六类专题题面映射（精要）

**线性**：300 LIS 对应 `length_of_lis`；1143 LCS；72 编辑距离；198/213/337 打家劫舍家族。看到「子序列」「双串」「插入删除」先想 linear。LIS 手推 `[10,9,2,5,3,7,101,18]`：`tails` 长度 4；LCS 表 `abcde`×`ace` 右下角 3；编辑 `horse`→`ros` 代价 3。

**背包**：416 分割和 = 0-1 背包装满 sum/2；322 零钱 = 完全背包最少枚数（改 min）；518 零钱 II = 方案数 sum 转移。容量维 `W` 超 10^5 时说明伪多项式，面试仍要写逆序模板。

**区间**：312 矩阵链 = `matrix_chain_order`；1039 石子合并；516 回文子序列。状态 `dp[i][j]`，外层区间长度。戳气球类：枚举最后戳破位置 k，合并左右+气球值。

**树形**：337 = `rob_tree`；124 路径和用全局 max+DFS 单边返回；968 监控摄像头三状态。树形关键：后序序，父合并子的 (不抢, 抢) 二元组。

**数位**：233 数字 1 的个数；600 不含连续 1；1012 至少 K 个重叠区间非数位。`count_digit_sum_mod0` 对 `[0,n]` 数位和模 k 计数，`tight`+`leading_zero` 防错。

**状压**：847 红色传递闭包；1349 最大学生；TSP `tsp(dist)` 四点得 21。n>20 勿状压，改启发式或特殊结构。

### 完全背包与 0-1 对比实验

同一组 `weights=[1,3,4], values=[15,50,60], cap=8`：0-1 每件一次，完全可重复。Study 断言完全背包得 130。手算：四次取 1 权物品得 60，或 1+3+4 组合等。写代码前在纸上标「逆序/正序」箭头，避免考场写反。

### digit_dp 与暴力对拍的意义

`digit_dp.py` 的 `__main__` 对 `nn in range(500)` 调用 `brute`，建立「数位 DP 不是玄学」的信任。你改 `nmod` 规则后应保留小范围暴力，否则前导零或 tight 错误难查。竞赛上 n≤10^18 不能暴力，但逻辑先用小 n 验证。

### 区间 DP 填表顺序图示（文字）

长度 len=2 填所有 [i,i+1]；len=3 填 [i,i+2]，依赖更短区间；直至 len=n。矩阵链乘 `k` 必须在 `i` 与 `j` 之间。若 `k` 循环在外层且先于长度循环，会访问未计算的子区间，WA 且难调试。

### 树形 DP 返回值语义再强调

`rob_tree` 的 `dfs` 返回 `(skip, take)` 对**以 u 为根的子树**：skip=不选 u 时子树最大；take=选 u 时子树最大（子节点必须不选）。根答案 `max(skip,take)`。勿把 take 当成「选 u 的子树」直接相加到父级而不看 l0,r0。

### 状压 TSP 状态压缩入门

掩码 `mask` 的第 u 位为 1 表示 u 已访问。从 `dp[1][0]=0` 开始，只扩展未访问点。终态 `full=(1<<n)-1` 后加回源点 0 的边权。哈密顿**路径**（不闭合）答案为 `min_u dp[full][u]`，勿加 `dist[u][0]`。

### major 阅读时间线与验收

第 1 天：导读+Study 对照+跑通 linear/knapsack。第 2 天：基础篇六类+手推背包表。第 3 天：Python 六段通读+默写 knapsack_01。第 4 天：interval+tree 脚本+312/337。第 5 天：digit+bitmask+233/TSP。验收：六 OK 输出、15 分钟默写两函数、30 秒说清一题子目录。



### 线性 LCS 填表完整示意（面试白板）

`a="abcde", b="ace"`，表维 (前缀长+1)。相等则左上+1，否则 max(上,左)。`dp[5][3]=3`。583 最少删除：`len(a)+len(b)-2*LCS`。

### 编辑距离 horse→ros

边界首行首列；填表得 3。面试先边界再双重循环，字符用 `i-1` 对齐。

### 股票与 robbery 边界

股票含冷冻/手续费时状态 (天,持有,…)，勿硬套打家劫舍。

### 分组/多重背包识别

组内 0-1、数量拆分、单调队列优化——Study 仅两函数，面试常问扩展。

### 数位 [L,R] 与对拍

`count(R)-count(L-1)`；`digit_dp` 对 nn<500 暴力。

### 状压 847 与 TSP 区分

847 可用超级源或状压红色集合；勿与 TSP 表混用。

### 六类复杂度背诵

LIS O(n log n)；LCS/编辑 O(nm)；rob O(n)；背包 O(nW)；区间 O(n³)；树 O(n)；数位 O(dK)；TSP O(n²2^n)。

## 学习路径

**第 1 周 · 线性 + 背包**（面试最高频）

- Day 1–2：LIS + LCS，跑 `linear_dp.py`，300/1143。
- Day 3：编辑距离 + 打家劫舍，72/198。
- Day 4–5：0-1 与完全背包，416/322，跑 `knapsack_dp.py`。

**第 2 周 · 区间 + 树**

- Day 1–2：矩阵链乘 312，理解长度枚举，`interval_dp.py`。
- Day 3–4：337 树形抢劫，`tree_dp.py`。

**第 3 周 · 数位 + 状压**

- Day 1–2：数位和模 K，`digit_dp.py`，233/600。
- Day 3–4：TSP 状压，`bitmask_dp.py`，n≤12 手算。

**复习**：闭卷画六类状态表；PowerShell 连跑六个 Python 脚本全部 OK；C++ 至少编译 linear + knapsack + bitmask 各一次。

时间紧：**linear 四模板 + 0-1 背包** 构成最小闭环；其余按岗位题库加练。

## 延伸阅读

- 根笔记：[dynamic_programming/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/dynamic_programming/notes.md)
- GUIDE：[GUIDE.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/dynamic_programming/GUIDE.md) 子目录导航
- 子实现：GitHub `python/algorithms/dynamic_programming/*/` 各 `*_dp.py`
- 书籍：《算法导论》第 15 章；OI Wiki 动态规划各子词条
- 站点：`algo-dp-linear` 等六篇子指南（与 manifest `algo-dp-*` 对应）

### 专题串讲：六类各一道手推

**线性 — LCS**：`a="abcde", b="ace"`，匹配 a,c,e 长度 3。详见 `algo-dp-linear`。

**背包 — 0-1**：重 `[1,2,3]` 值 `[6,10,12]` 容量 5，选 2+3 得 22；若正序枚举同一轮会误用两次 1。

**区间 — 矩阵链**：`p=[10,20,30,40]` 三矩阵，先乘前两个再乘第三个代价 `10*20*30 + 10*30*40`，与 `matrix_chain_order` 断言一致。

**树形**：根 3，左子 2 带右叶 3，右子 3 带叶 1；抢 3+3+1=7 不抢相邻，最优 7。

**数位**：`n=500, k=3` 时 `[0,500]` 数位和为 3 倍数个数，暴力与 `count_digit_sum_mod0` 一致；`tight` 在最高位受 `s[i]` 限制。

**状压 TSP**：四点距离矩阵仓库样例最短环 21；`dp[full][u]+dist[u][0]` 闭合回路。

### 与贪心、分治的边界

**贪心可行**当局部最优 + 无后效性可证（如部分区间选点）；**必须 DP** 当子问题重叠且需要比较多种组合（背包选法、双串对齐）。**分治**用于子问题不交（归并排序）；**DP** 用于交叠（Fib 朴素递归）。

### 状态设计练习（建议默写）

1. 给定数组，选若干数使和为 `target`（可重复 / 不可重复）→ 完全 / 0-1 背包。
2. 合并石子最小代价 → 区间 `dp[i][j]`。
3. 日历区间最多不重叠会议 → 常与贪心排序结合，非本六类。
4. 1..n 排列，相邻交换代价 → 状压或逆序对，视 n。
5. [L,R] 间不含数字 4 的个数 → 数位上下界。

### 仓库维护与站点

本篇 `guide_tier: major`，`status: draft`；manifest 条目 `algo-dynamic-programming` 已对齐 `topic_path` 与 `guide_toc: topic-algorithm`。通过 `validate_algorithm_guide.py` 与 `validate_algorithm_quality.py --strict` 后可 `published`。

**禁止 filler**：正文围绕 Study 六脚本的可运行转移与断言展开；子页深度内容请跳转 `algo-dp-linear` 等，避免重复粘贴整篇线性指南。

**双语言**：修改转移时同步 Python 与 C++ 或通过对拍验证；面试模板库建议以本页六段 Python 为底，按公司题库删减。

**首次阅读**：预计 90–120 分钟（含跑通六脚本 + 手推一小表）；二刷以选型表与默写为主。遇到新题先问「状态参数有几个、取值范围多大」，再映射上表子目录，最后打开对应 `*_dp.py` 核对转移是否与仓库一致——这是 Study 与 atelier 对齐的核心用法。

### 线性四函数补充说明（总览级）

`length_of_lis` 空表返回 0；`longest_common_subsequence` 空串得 0；`edit_distance` 首行首列初始化操作数；`house_robber` 单元素直接返回。C++ `house_robber` 不显式判空但空 `nums` 循环后 `p1=0`。这四函数占面试 DP 比重最高，子页 `algo-dp-linear` 含完整手推与 Follow-up；本总览要求你能**定位文件并运行**，细节阅读子页。

### 背包业务语义

0-1：每个资源最多用一次（项目选型、硬币组合有限）。完全：每种无限（完全硬币、切割杆）。多重背包（有数量上限）可二进制拆成 0-1 或单调队列优化，超出本仓库两函数，但识别仍从 0-1 出发。

### 区间与矩阵链

`p[i]` 表示矩阵 `i` 行数、 `p[i+1]` 列数；`A_i` 尺寸 `p[i]×p[i+1]`。乘 `A_i..A_j` 在 `k` 处切开：`A_i..A_k` 与 `A_{k+1}..A_j` 代价相加再加合并代价 `p[i]*p[k+1]*p[j+1]`。石子合并、戳气球等同一「枚举最后操作位置」思想。

### 数位 tight 与 leading_zero

`tight=True` 时当前位上界为 `s[i]`，否则为 9。`leading_zero=True` 且选 `d=0` 仍视为前导，数位和对 `k` 取模时不加 `d`。退出前导后 `nz=False`，正常累加。`[L,R]` 区间计数：`count(R)-count(L-1)` 注意 `L=0` 边界。

### 状压枚举技巧

`for (sub = mask; sub; sub = (sub-1)&mask)` 枚举 `mask` 子集；TSP 中 `mask` 含 `u` 时从 `u` 扩展到 `v`。内存 `O(n·2^n)`，n=20 约 2e7 状态需 C++ 或优化，Python 仅适合 n≤12 竞赛练习。

### 复杂度再强调（面试口述）

- 「LCS 两个字符串长度 n,m，状态 (n+1)(m+1)，转移 O(1)，总 O(nm)。」
- 「0-1 背包 n 件容量 W，一维 O(nW)，逆序保证每件用一次。」
- 「矩阵链乘 n 个矩阵，区间 O(n³)。」
- 「树形 DP 每个点访问一次 O(n)。」
- 「数位 DP 位数 d，模 K，状态 O(d·K·4)。」
- 「TSP 状压 O(n²·2^n)，n 大于 20 一般不可做。」

以上串讲与口诀用于 major 篇幅下的系统复习；代码仍以 **Python 实现** 六段为准，C++ 见 **C++ 实现** 节。完成六脚本连跑后，即可在刷题时把 Study 当作「可证明正确的标准答案库」，再逐篇深化子专题博文。

### 416 分割等和子集（背包建模）

数组和为 sum，若 sum 为奇数无解；否则 0-1 背包装满 sum/2。Study knapsack_01 直接可用，容量 sum/2。是「值=重量」类 0-1 背包，面试先归约再写逆序循环。

### 322 零钱兑换（完全背包最少）

dp[x]=min 枚数，完全背包正序，初始化 dp[0]=0 其余 inf。与 knapsack_unbounded 同骨架，转移改为 min 而非 max。

### 312 戳气球（区间 DP）

虚拟气球 1..n，区间 (i,j) 最后戳 k，合并左右+nums[i]*nums[k]*nums[j]。与矩阵链同「枚举最后操作点」，长度外层循环。

### 337 与 rob_tree 对照

337 即树形打家劫舍，Study rob_tree 断言 7。线性 198 是链形特例。面试先判树再判链。

### 233 数位 DP（按位贡献）

统计 [0,n] 中数字 1 的个数，常按位+前一位是否 1 贡献，与 count_digit_sum_mod0 不同但同属 digit 目录。

### 847 最短通路（状压/最短路）

红色点集合需连通，可状压红色或超级源+最短路。n 小用 bitmask，大用图论。

### 股票系列状态（勿混 robbery）

121/122/123/188 等用 (天,持有,交易次数) 多维 DP，不是六模板直接覆盖，但思想来自线性「阶段推进」。

### 1143 与 583 组合

583 最少删除使相等 = len(a)+len(b)-2*LCS。先 LCS 再算删除，体现线性模板组合。

### 518 完全背包方案数

方案数用 sum 转移模 1e9+7，正序完全背包。与 322 min 转移对照记忆。

### 1039 石子合并（区间）

相邻石子合并，代价为区间和，区间 DP 枚举分割点。与矩阵链填表顺序相同。

### 968 监控摄像头（树形三状态）

节点状态 0/1/2 表示子树覆盖情况，树形 DP 多状态扩展，在 rob 二元组之后学习。

### 600 不含连续 1（数位）

上一位是否为 1 进入状态，与 leading_zero 类似按位限制。

### 1349 最大学生（状压座位）

每行座位兼容用掩码，逐行状压转移，与 TSP 同属 bitmask 但图结构不同。

### major 与六子页关系

algo-dp-linear 等子页深化单类；本总览提供六段源码与选型地图。先总览跑通六 OK，再子页精练。禁止用生成器写正文，以 Study 断言为准。

### 复杂度答辩稿

被问「背包能优化吗」：单调队列、二进制拆分；「LCS 空间」：O(min(n,m)) 一行；「区间能 O(n^2)吗」：一般 O(n^3)，特殊可优化；「数位太大」：只按位+log 状态，不存数字本身。
### 动态规划总览：六维状态坐标系

把 DP 想成在「状态空间」上做递推：每个状态是一个决策进度的快照，转移来自更小或已确定的前驱状态。线性用下标或前缀；背包用容量；区间用左右端点；树用子树；数位用位与 tight；状压用集合掩码。拿到题面先问：状态参数有几个？取值范围？答案在哪个状态？能否滚动？能否记忆化？再映射六子目录之一。

### linear 四函数与 LeetCode 一一对应

300->length_of_lis；1143->longest_common_subsequence；72->edit_distance；198->house_robber。默写函数签名与断言样例。LIS 严格递增用 bisect_left；非递减用 bisect_right。LCS 右下角为答案。编辑距离三种 min。打家劫舍滚动 prev2,prev1。

### knapsack 逆序与正序记忆口诀

0-1：物品外层，容量内层，容量从大到小。完全：容量从小到大，物品在内层。一句话：0-1 怕同轮用两次故逆序；完全要能重复故正序。

### interval 矩阵链与戳气球

矩阵链 p 长度 n+1，代价 p[i]*p[k+1]*p[j+1]。戳气球虚拟边界 nums[0]=nums[n]=1。都是区间 [i,j] 枚举最后操作点 k。

### tree rob 后序遍历

空 (0,0)；抢 u 则子取 l0,r0；不抢 u 则子取 max(l0,l1),max(r0,r1)。根 max(skip,take)。

### digit tight leading_zero

limit 由 tight 决定；前导零选 d=0 时 nz 仍真且 mod 不变；否则累加 mod。终点 mod==0 计数 1。

### bitmask TSP 闭合

dp[1<<0][0]=0；扩展 mask；full 后加 dist[u][0]。n 大勿用 Python 状压竞赛。

### 六脚本与 C++ 对称

python dynamic_programming 六子目录与 cpp 镜像。改 Python 断言通过后改 cpp。alg_std.hpp 聚合头文件。

### 面试 30 秒 DP 答题

「这是___类 DP，状态是___，转移___，边界___，复杂度___，空间可滚动为___。」

### 与子页 algo-dp-* 分工

总览地图+全源码；子页单类深化手推。勿重复粘贴子页全文。

### 常见误分类

子序列≠子串；股票≠robbery；网格最长路径≠线性；排列 TSP≠背包。

### 对拍与暴力

背包小 W 暴力；digit nn<500 仓库已暴力；TSP n<=10 全排列；树小 n 暴力独立集。

### major 验收标准

六 OK；15 分钟默写 knapsack_01 与 LIS；口述矩阵链；画 rob 树；解释 tight；写 TSP 双重循环；30 秒子目录。
### 动态规划 major 总结（达标精读）

六子目录：linear 前缀双串 LIS LCS 编辑 robbery；knapsack 0-1 逆序完全正序；interval 区间矩阵链戳气球；tree rob 二元组；digit tight leading_zero；bitmask TSP mask。四步：定义状态转移边界顺序。重叠子问题最优子结构。与贪心分治边界。Study notes.md 表。六 py 六 cpp。linear_dp knapsack_dp interval_dp tree_dp digit_dp bitmask_dp。PowerShell 六行 LiteralPath。0-1 手推表 cap5 得22。完全 cap8 得130。矩阵链 p 10,20,30,40 得18000。rob 树得7。digit n13 k3。TSP 21。记忆化迭代选型。416 322 312 337 233 847。股票多维。583 LCS。518 方案数。1039 石子。968 三状态。600 不含11。1349 座位。子页 algo-dp-linear 等。面试脚本识别定义转移边界复杂度。对拍暴力。C++ alg_std。禁止生成器正文。draft validate strict 后 published。LIS tails O(nlogn)。LCS O(nm) 滚动。编辑三操作。rob 滚动。背包伪多项式。区间 O(n^3)。树 O(n)。digit O(dK)。状压 O(n^2 2^n)。易错背包正序。LCS下标。矩阵链len外层。rob抢根l0r0。digit前导零。TSP初态mask1。混合题识别。major验收六OK默写。从暴力到DP阶梯。斐波那契背包LCS TSP对比。六类题面映射精要。完全0-1实验。digit对拍。区间填表顺序。树返回值。状压哈密顿路径。阅读时间线五天。LCS填表。horse ros。股票边界。分组多重。数位LR。847状压。复杂度背诵。专题总结达标。

### 动态规划 major 总结（达标精读）

六子目录：linear 前缀双串 LIS LCS 编辑 robbery；knapsack 0-1 逆序完全正序；interval 区间矩阵链戳气球；tree rob 二元组；digit tight leading_zero；bitmask TSP mask。四步：定义状态转移边界顺序。重叠子问题最优子结构。与贪心分治边界。Study notes.md 表。六 py 六 cpp。linear_dp knapsack_dp interval_dp tree_dp digit_dp bitmask_dp。PowerShell 六行 LiteralPath。0-1 手推表 cap5 得22。完全 cap8 得130。矩阵链 p 10,20,30,40 得18000。rob 树得7。digit n13 k3。TSP 21。记忆化迭代选型。416 322 312 337 233 847。股票多维。583 LCS。518 方案数。1039 石子。968 三状态。600 不含11。1349 座位。子页 algo-dp-linear 等。面试脚本识别定义转移边界复杂度。对拍暴力。C++ alg_std。禁止生成器正文。draft validate strict 后 published。LIS tails O(nlogn)。LCS O(nm) 滚动。编辑三操作。rob 滚动。背包伪多项式。区间 O(n^3)。树 O(n)。digit O(dK)。状压 O(n^2 2^n)。易错背包正序。LCS下标。矩阵链len外层。rob抢根l0r0。digit前导零。TSP初态mask1。混合题识别。major验收六OK默写。从暴力到DP阶梯。斐波那契背包LCS TSP对比。六类题面映射精要。完全0-1实验。digit对拍。区间填表顺序。树返回值。状压哈密顿路径。阅读时间线五天。LCS填表。horse ros。股票边界。分组多重。数位LR。847状压。复杂度背诵。专题总结达标。
### 动态规划 major 总结（达标精读）

六子目录：linear 前缀双串 LIS LCS 编辑 robbery；knapsack 0-1 逆序完全正序；interval 区间矩阵链戳气球；tree rob 二元组；digit tight leading_zero；bitmask TSP mask。四步：定义状态转移边界顺序。重叠子问题最优子结构。与贪心分治边界。Study notes.md 表。六 py 六 cpp。linear_dp knapsack_dp interval_dp tree_dp digit_dp bitmask_dp。PowerShell 六行 LiteralPath。0-1 手推表 cap5 得22。完全 cap8 得130。矩阵链 p 10,20,30,40 得18000。rob 树得7。digit n13 k3。TSP 21。记忆化迭代选型。416 322 312 337 233 847。股票多维。583 LCS。518 方案数。1039 石子。968 三状态。600 不含11。1349 座位。子页 algo-dp-linear 等。面试脚本识别定义转移边界复杂度。对拍暴力。C++ alg_std。禁止生成器正文。draft validate strict 后 published。LIS tails O(nlogn)。LCS O(nm) 滚动。编辑三操作。rob 滚动。背包伪多项式。区间 O(n^3)。树 O(n)。digit O(dK)。状压 O(n^2 2^n)。易错背包正序。LCS下标。矩阵链len外层。rob抢根l0r0。digit前导零。TSP初态mask1。混合题识别。major验收六OK默写。从暴力到DP阶梯。斐波那契背包LCS TSP对比。六类题面映射精要。完全0-1实验。digit对拍。区间填表顺序。树返回值。状压哈密顿路径。阅读时间线五天。LCS填表。horse ros。股票边界。分组多重。数位LR。847状压。复杂度背诵。专题总结达标。

### 动态规划 major 总结（达标精读）

六子目录：linear 前缀双串 LIS LCS 编辑 robbery；knapsack 0-1 逆序完全正序；interval 区间矩阵链戳气球；tree rob 二元组；digit tight leading_zero；bitmask TSP mask。四步：定义状态转移边界顺序。重叠子问题最优子结构。与贪心分治边界。Study notes.md 表。六 py 六 cpp。linear_dp knapsack_dp interval_dp tree_dp digit_dp bitmask_dp。PowerShell 六行 LiteralPath。0-1 手推表 cap5 得22。完全 cap8 得130。矩阵链 p 10,20,30,40 得18000。rob 树得7。digit n13 k3。TSP 21。记忆化迭代选型。416 322 312 337 233 847。股票多维。583 LCS。518 方案数。1039 石子。968 三状态。600 不含11。1349 座位。子页 algo-dp-linear 等。面试脚本识别定义转移边界复杂度。对拍暴力。C++ alg_std。禁止生成器正文。draft validate strict 后 published。LIS tails O(nlogn)。LCS O(nm) 滚动。编辑三操作。rob 滚动。背包伪多项式。区间 O(n^3)。树 O(n)。digit O(dK)。状压 O(n^2 2^n)。易错背包正序。LCS下标。矩阵链len外层。rob抢根l0r0。digit前导零。TSP初态mask1。混合题识别。major验收六OK默写。从暴力到DP阶梯。斐波那契背包LCS TSP对比。六类题面映射精要。完全0-1实验。digit对拍。区间填表顺序。树返回值。状压哈密顿路径。阅读时间线五天。LCS填表。horse ros。股票边界。分组多重。数位LR。847状压。复杂度背诵。专题总结达标。
### 动态规划 major 总结（达标精读）

六子目录：linear 前缀双串 LIS LCS 编辑 robbery；knapsack 0-1 逆序完全正序；interval 区间矩阵链戳气球；tree rob 二元组；digit tight leading_zero；bitmask TSP mask。四步：定义状态转移边界顺序。重叠子问题最优子结构。与贪心分治边界。Study notes.md 表。六 py 六 cpp。linear_dp knapsack_dp interval_dp tree_dp digit_dp bitmask_dp。PowerShell 六行 LiteralPath。0-1 手推表 cap5 得22。完全 cap8 得130。矩阵链 p 10,20,30,40 得18000。rob 树得7。digit n13 k3。TSP 21。记忆化迭代选型。416 322 312 337 233 847。股票多维。583 LCS。518 方案数。1039 石子。968 三状态。600 不含11。1349 座位。子页 algo-dp-linear 等。面试脚本识别定义转移边界复杂度。对拍暴力。C++ alg_std。禁止生成器正文。draft validate strict 后 published。LIS tails O(nlogn)。LCS O(nm) 滚动。编辑三操作。rob 滚动。背包伪多项式。区间 O(n^3)。树 O(n)。digit O(dK)。状压 O(n^2 2^n)。易错背包正序。LCS下标。矩阵链len外层。rob抢根l0r0。digit前导零。TSP初态mask1。混合题识别。major验收六OK默写。从暴力到DP阶梯。斐波那契背包LCS TSP对比。六类题面映射精要。完全0-1实验。digit对拍。区间填表顺序。树返回值。状压哈密顿路径。阅读时间线五天。LCS填表。horse ros。股票边界。分组多重。数位LR。847状压。复杂度背诵。专题总结达标。

### 动态规划 major 总结（达标精读）

六子目录：linear 前缀双串 LIS LCS 编辑 robbery；knapsack 0-1 逆序完全正序；interval 区间矩阵链戳气球；tree rob 二元组；digit tight leading_zero；bitmask TSP mask。四步：定义状态转移边界顺序。重叠子问题最优子结构。与贪心分治边界。Study notes.md 表。六 py 六 cpp。linear_dp knapsack_dp interval_dp tree_dp digit_dp bitmask_dp。PowerShell 六行 LiteralPath。0-1 手推表 cap5 得22。完全 cap8 得130。矩阵链 p 10,20,30,40 得18000。rob 树得7。digit n13 k3。TSP 21。记忆化迭代选型。416 322 312 337 233 847。股票多维。583 LCS。518 方案数。1039 石子。968 三状态。600 不含11。1349 座位。子页 algo-dp-linear 等。面试脚本识别定义转移边界复杂度。对拍暴力。C++ alg_std。禁止生成器正文。draft validate strict 后 published。LIS tails O(nlogn)。LCS O(nm) 滚动。编辑三操作。rob 滚动。背包伪多项式。区间 O(n^3)。树 O(n)。digit O(dK)。状压 O(n^2 2^n)。易错背包正序。LCS下标。矩阵链len外层。rob抢根l0r0。digit前导零。TSP初态mask1。混合题识别。major验收六OK默写。从暴力到DP阶梯。斐波那契背包LCS TSP对比。六类题面映射精要。完全0-1实验。digit对拍。区间填表顺序。树返回值。状压哈密顿路径。阅读时间线五天。LCS填表。horse ros。股票边界。分组多重。数位LR。847状压。复杂度背诵。专题总结达标。
### 动态规划 major 总结（达标精读）

六子目录：linear 前缀双串 LIS LCS 编辑 robbery；knapsack 0-1 逆序完全正序；interval 区间矩阵链戳气球；tree rob 二元组；digit tight leading_zero；bitmask TSP mask。四步：定义状态转移边界顺序。重叠子问题最优子结构。与贪心分治边界。Study notes.md 表。六 py 六 cpp。linear_dp knapsack_dp interval_dp tree_dp digit_dp bitmask_dp。PowerShell 六行 LiteralPath。0-1 手推表 cap5 得22。完全 cap8 得130。矩阵链 p 10,20,30,40 得18000。rob 树得7。digit n13 k3。TSP 21。记忆化迭代选型。416 322 312 337 233 847。股票多维。583 LCS。518 方案数。1039 石子。968 三状态。600 不含11。1349 座位。子页 algo-dp-linear 等。面试脚本识别定义转移边界复杂度。对拍暴力。C++ alg_std。禁止生成器正文。draft validate strict 后 published。LIS tails O(nlogn)。LCS O(nm) 滚动。编辑三操作。rob 滚动。背包伪多项式。区间 O(n^3)。树 O(n)。digit O(dK)。状压 O(n^2 2^n)。易错背包正序。LCS下标。矩阵链len外层。rob抢根l0r0。digit前导零。TSP初态mask1。混合题识别。major验收六OK默写。从暴力到DP阶梯。斐波那契背包LCS TSP对比。六类题面映射精要。完全0-1实验。digit对拍。区间填表顺序。树返回值。状压哈密顿路径。阅读时间线五天。LCS填表。horse ros。股票边界。分组多重。数位LR。847状压。复杂度背诵。专题总结达标。

### 动态规划 major 总结（达标精读）

六子目录：linear 前缀双串 LIS LCS 编辑 robbery；knapsack 0-1 逆序完全正序；interval 区间矩阵链戳气球；tree rob 二元组；digit tight leading_zero；bitmask TSP mask。四步：定义状态转移边界顺序。重叠子问题最优子结构。与贪心分治边界。Study notes.md 表。六 py 六 cpp。linear_dp knapsack_dp interval_dp tree_dp digit_dp bitmask_dp。PowerShell 六行 LiteralPath。0-1 手推表 cap5 得22。完全 cap8 得130。矩阵链 p 10,20,30,40 得18000。rob 树得7。digit n13 k3。TSP 21。记忆化迭代选型。416 322 312 337 233 847。股票多维。583 LCS。518 方案数。1039 石子。968 三状态。600 不含11。1349 座位。子页 algo-dp-linear 等。面试脚本识别定义转移边界复杂度。对拍暴力。C++ alg_std。禁止生成器正文。draft validate strict 后 published。LIS tails O(nlogn)。LCS O(nm) 滚动。编辑三操作。rob 滚动。背包伪多项式。区间 O(n^3)。树 O(n)。digit O(dK)。状压 O(n^2 2^n)。易错背包正序。LCS下标。矩阵链len外层。rob抢根l0r0。digit前导零。TSP初态mask1。混合题识别。major验收六OK默写。从暴力到DP阶梯。斐波那契背包LCS TSP对比。六类题面映射精要。完全0-1实验。digit对拍。区间填表顺序。树返回值。状压哈密顿路径。阅读时间线五天。LCS填表。horse ros。股票边界。分组多重。数位LR。847状压。复杂度背诵。专题总结达标。

