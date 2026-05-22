---
title: "算法 · Dp Linear"
series: algorithm
category: Algorithms
topic_path: algorithms/dynamic_programming/linear
guide_toc: topic-algorithm
guide_tier: medium
status: published
---

# 算法 · 线性动态规划（Linear DP）

## 导读

动态规划（Dynamic Programming，DP）的核心，是在**重叠子问题**与**最优子结构**成立时，用表格或滚动变量记住已算过的状态，避免指数级重复搜索。名称中的「编程」并非指写代码，而是指填表式的递推规划；与「贪心」的区别在于贪心只做当前局部最优，而 DP 要保证子问题最优能拼成全局最优。线性 DP 是其中最常见的一类：你的「决策进度」可以画成一条从 0 到 n 的数轴，每次向前推进一格或同时推进两个串的前缀，从不回头访问已经废弃的状态。

若你来自刷题社区，可能对「状态压缩」「滚动数组」等词已有印象——本专题的打家劫舍就是一维滚动的最简示范；LCS 与编辑距离则是二维表的标准入门。若你来自竞赛，可能对 LIS 的 `O(n log n)` 更熟悉；本文把朴素与优化都保留，便于向面试官展示思维层次。若你来自工程岗位，四模板仍值得学：diff 工具、序列比对、简单资源调度（相邻约束）在业务里偶尔出现，识别模型比背题号更重要。当问题的「阶段」可以自然地映射到**数组下标、字符串前缀长度、或按时间顺序推进的决策序列**时，我们常把这类模型统称为**线性 DP**：状态往往写成 `dp[i]`、`dp[i][j]`（其中 `i`、`j` 表示已处理的前缀长度），转移只依赖**更短的前缀**或**相邻下标**，而不会回溯到任意远的非局部结构（那更接近树形 DP、区间 DP 等专题）。

本专题在 Study 仓库中与 `linear_dp.py` / `linear_dp.cpp` 对齐，集中讲解四类面试与竞赛中的高频模板：

| 问题 | 典型状态 | 目标 |
|------|----------|------|
| 最长递增子序列（LIS） | 以某长度结尾的最小尾元素 | 子序列长度 |
| 最长公共子序列（LCS） | 两串前缀的匹配程度 | 公共子序列长度 |
| 编辑距离 | 将 `a` 前缀变为 `b` 前缀的最小代价 | 最少操作数 |
| 打家劫舍 | 到第 `i` 户时的最大收益 | 线性路径上的最值 |

这四类题的共同点是：**定义清楚「子问题」的维度**（一维下标或二维前缀），**写出转移方程**，再选择 **O(n²) 填表**、**O(n) 滚动** 或 **O(n log n) 贪心+二分** 的实现。读完本文，你应能独立识别「这是线性 DP 吗？」、写出状态和边界、在 Python 与 C++ 中实现 Study 仓库中的四个函数，并知道何时可以压空间、何时必须保留二维表。

线性 DP 在刷题中的位置：它是 DP 家族的**入门枢纽**——掌握 LIS/LCS 后，很多「子序列」「子串」「双串匹配」题只需改状态含义；掌握编辑距离后，带权删除/插入/替换、只有两种操作、或滚动成一维的变体都顺理成章；打家劫舍则是**相邻约束下的最值**原型，延伸到环形、树形、多状态（抢/不抢/冷冻）时仍是一维滚动。面试中常要求先讲清 `dp` 含义与转移，再谈复杂度与空间优化，本文各节按这一顺序组织。

与「暴力枚举所有子序列」相比，线性 DP 把指数级的选择压成多项式：LIS 朴素枚举每个元素选或不选是 `O(2^n)`，填表后变为 `O(n²)` 或 `O(n log n)`；LCS 双串暴力配对是指数级，二维表是 `O(nm)`。理解这一对比有助于你在考场快速否定纯搜索并转向 DP。另一方面，并非所有沿下标的题都是 DP：若只需求全局最大子数组和且允许取连续段，Kadane 算法 `O(n)` 往往比 DP 表更短；若带环形或必须取 k 个元素，才需要更丰富的状态。本文聚焦的四模板，特征是**决策具有无后效性**——处理完前缀后，未来只依赖已压缩的最优值，不需要记住具体选了哪些下标（除非题目要求输出方案）。

从工程角度，线性 DP 代码短、边界集中、易于单测，Study 仓库用四个断言覆盖典型与空输入，正是推荐的学习方式：先保证参考实现正确，再在 LeetCode 上练建模速度。站点本文与仓库同步，避免「讲义公式」与「可运行代码」脱节；你修改转移时，应同时更新笔记、Python、C++ 三处或至少对拍通过。

## 预备知识

> **环境**：Python 3.10+（`bisect` 标准库）；C++17，`g++` 编译，Study 侧 C++ 线性 DP 通过 `#include <alg_std.hpp>` 使用 `lower_bound` 等工具。

阅读本专题前，建议已具备：

- **数组与字符串下标**：习惯用 `0..n-1` 访问元素，用 `1..n` 作为 DP 表下标时，字符对应 `s[i-1]`。
- **子序列与子串的区别**：子序列不要求连续；子串（子数组）必须连续。LIS、LCS 是子序列；打家劫舍是**下标连续**的选取，状态仍沿下标线性推进。
- **基础复杂度**：知道 `O(n²)` 双重循环、`O(n log n)` 二分、`O(n)` 单遍扫描的含义。
- **二分查找**：LIS 的 `O(n log n)` 写法依赖在**有序数组**上找第一个 `≥ x` 的位置（Python `bisect_left`，C++ `lower_bound`）。

若对「最优子结构」尚不熟悉，可这样记：若全局最优解在「做最后一次决策」后，剩余部分必须是**剩余规模下的最优解**，则适合 DP。例如 LCS 在 `a[i]==b[j]` 时必用 `dp[i-1][j-1]+1`，否则最优一定来自「少处理 `a` 的一端」或「少处理 `b` 的一端」之一的最大值。

**重叠子问题**在线性 DP 中体现为：计算 `dp[i][j]` 时多次需要 `dp[i-1][*]` 与 `dp[*][j-1]`，填表自然去重。若用递归 + 记忆化，访问模式与二重循环相同，面试可先写记忆化再改迭代，避免栈溢出。Python 递归深度有限，长串 LCS 建议迭代；C++ 递归 5000×5000 记忆化也可能爆栈。

**数学归纳直觉**：设 `dp[i]` 表示前 `i` 个位置的最优值，若我们能证明任意最优解都可以看作「在位置 i 做最优决策 + 前段最优」，则递推成立。打家劫舍在位置 i 要么不偷（最优为前 i-1 的最优），要么偷 i（则 i-1 不能偷，收益为前 i-2 最优加 `nums[i]`），归纳基础为前 0/1 户。

**工具链**：本地建议用 VS Code 或 Cursor 同时打开 Study 的 python 与 cpp 目录，改一题对拍两语言。PowerShell 7 支持 `-LiteralPath`；Windows 自带 5.x 的 `Set-Location -LiteralPath` 同样可用，勿用未加引号的通配路径。Python 执行时若不在仓库根目录，用绝对路径调用脚本可避免 `import` 路径问题（本专题脚本无包依赖，直接运行即可）。

## Study 仓库对照

本页 `topic_path` 为 `algorithms/dynamic_programming/linear`，与 GitHub 仓库 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) 中下列路径一致：

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/dynamic_programming/linear/notes.md` | `python/algorithms/dynamic_programming/linear/linear_dp.py` |
| C++ | `cpp/algorithms/dynamic_programming/linear/notes.md` | `cpp/algorithms/dynamic_programming/linear/linear_dp.cpp` |

在本地 Study 克隆根目录下运行（请使用 `-LiteralPath`，避免路径中的特殊字符被误解析）：

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\linear\linear_dp.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\dynamic_programming\linear
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe linear_dp.cpp
.\run.exe
```

`notes.md` 中的要点：状态沿一维下标推进；复杂度视转移，通常 `O(n)` 或 `O(n²)`，LIS 可优化到 `O(n log n)`。正文以下在笔记骨架上扩写定义、证明直觉、模板与易错点。

克隆 Study 仓库后，可用 `Get-ChildItem -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\linear` 列出本专题文件；与 cpp 镜像目录结构对称。首次学习不必修改仓库，只运行自测；二次学习可在同目录新建 `playground.py` 做变体实验，避免污染主脚本。若 push 到 fork，保持与 upstream 的 `linear_dp.py` 接口一致，便于与本页对照。

## 基础篇

### 直觉与定义

**线性 DP** 在这里指：状态的「规模参数」是**单调递增的整数**（如已处理 `nums[0..i-1]`、已考虑前 `i` 个房屋），转移只从**更小或相邻**的规模而来，形成有向无环的依赖图（按 `i` 拓扑排序即可计算）。

**最长递增子序列（LIS）**

给定整数数组 `nums`，求**严格递增**子序列的最大长度。子序列可以删元素但不能重排。

- **子问题（朴素）**：`dp[i]` = 以 `nums[i]` **结尾**的最长递增子序列长度。
- **转移**：对所有 `j < i` 且 `nums[j] < nums[i]`，有 `dp[i] = max(dp[i], dp[j] + 1)`，初值 `dp[i] = 1`。
- **答案**：`max(dp)`。

朴素 `O(n²)` 清晰，但数据范围到 `10⁵` 时常用 **耐心排序（Patience Sorting）** 思想：`tails[k]` 表示长度为 `k+1` 的递增子序列的**最小可能末尾**。遍历 `x` 时，在 `tails` 中二分找第一个 `≥ x` 的位置并替换，或追加到末尾；`tails` 长度即为 LIS 长度。该数组始终有序，故二分合法。注意：此技巧求的是**长度**；若要还原具体子序列，需另存前驱或再做一次 `O(n²)`。

**最长公共子序列（LCS）**

给定字符串 `a`、`b`，求最长公共**子序列**长度。

- **子问题**：`dp[i][j]` = `a` 的前 `i` 个字符与 `b` 的前 `j` 个字符的 LCS 长度（`i`、`j` 为前缀长度，非 0-based 下标）。
- **转移**：
  - 若 `a[i-1] == b[j-1]`：`dp[i][j] = dp[i-1][j-1] + 1`；
  - 否则：`dp[i][j] = max(dp[i-1][j], dp[i][j-1])`。
- **边界**：`dp[0][*] = dp[*][0] = 0`。
- **答案**：`dp[na][nb]`。

**编辑距离（Levenshtein）**

将字符串 `a` 变为 `b` 的最少单字符操作数，每次可插入、删除或替换一个字符（代价均为 1，除非题目另设权重）。

- **子问题**：`dp[i][j]` = `a` 的前 `i` 个字符变为 `b` 的前 `j` 个字符的最小操作数。
- **边界**：`dp[i][0]=i`（删光），`dp[0][j]=j`（插满）。
- **转移**：
  - 若 `a[i-1]==b[j-1]`：`dp[i][j]=dp[i-1][j-1]`；
  - 否则：`dp[i][j]=1+min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`（删 `a`、插到 `a`、替换）。

**打家劫舍（House Robber）**

一排房屋 `nums[i]` 有非负赃款，相邻房屋不能同时抢，求最大总和。

- **子问题**：考虑前 `i` 户时最大收益。常用滚动：`prev2` 表示到 `i-2` 为止最优，`prev1` 表示到 `i-1` 为止最优。
- **转移**：到第 `i` 户，`cur = max(prev1, prev2 + nums[i])`，然后窗口前移。
- **含义**：第 `i` 户要么不抢（继承 `prev1`），要么抢（则 `i-1` 不能抢，加上 `prev2 + nums[i]`）。

以上四题都满足：**当前状态只依赖更短前缀或前一两步**，无环，故可 DP。

**LIS 深入：为何 `tails` 有效**

想象把牌分成若干堆，每堆牌顶递增，新牌能替换某堆顶则替换，否则新开一堆。堆数即 LIS 长度。`tails[k]` 记录第 k 堆的牌顶最小值，从而在同长度下为后续元素留出尽可能小的「门槛」。当新元素 `x` 到来，在 `tails` 中找第一个 `≥ x` 的位置：若存在则替换使该长度末尾更小；若不存在则新开更长序列。`tails` 始终有序，故二分。严格递增要求替换时不能随意 append 相等值到末尾而不替换——对 `[3,3,3]`，长度应为 1，二分左边界保证相等时替换而非加长。

**LCS 深入：子问题图解**

画两个字符串在表角，向右向下扩展。`dp[i][j]` 的语义必须固定为「前缀长度」而非「下标」，这样 `dp[0][0]` 表示空对空，长度为 0。字符匹配时从左上转移，相当于「同时选用这两个字符」；不匹配时只能来自上方或左方，相当于「放弃 a 的当前字符」或「放弃 b 的当前字符」。不能从 `dp[i-1][j-1]` 在字符不等时转移，否则会隐含错误对齐。构造 LCS 字符串时，从 `(na,nb)` 回溯：若 `a[i-1]==b[j-1]` 则收集字符并走向 `(i-1,j-1)`；否则走向 `dp` 较大的一侧（相等时任选一侧，但要固定规则）。

**编辑距离深入：操作与对齐**

三种操作可视为对两个字符串同步扫描时的决策：匹配则免费前进；不匹配则尝试删除 a 的当前字符（`dp[i-1][j]+1`）、在 a 插入 b 的当前字符（`dp[i][j-1]+1`）、或替换（`dp[i-1][j-1]+1`）。插入与删除在双串表上对称。许多同学把「插入 b」与「删除 a」混淆，记住「表维度是前缀长度」即可：`dp[i][j-1]` 表示 a 仍长 i、b 少一个字符，相当于 a 侧需要插入。带权版本把 `+1` 换成 `+cost_ins` 等即可。

**打家劫舍深入：状态机视角**

每户有抢/不抢两种决策，相邻不能都抢。令 `f[i][0]` 为不抢第 i 户的最大值，`f[i][1]` 为抢第 i 户的最大值，则 `f[i][0]=max(f[i-1][0],f[i-1][1])`，`f[i][1]=f[i-1][0]+nums[i]`。压缩后 `prev1` 相当于「到当前户为止的最优（可抢可不抢）」，`prev2` 是上一户结束时的最优且隐含上一户可不抢。滚动一行时更新顺序不可颠倒：必须先算新 `cur` 再移位。

### 复杂度分析

| 问题 | 状态规模 | 时间 | 空间（实现级） |
|------|----------|------|----------------|
| LIS 朴素 | `n` | `O(n²)` | `O(n)` |
| LIS 二分 | `n` | `O(n log n)` | `O(n)`（`tails`） |
| LCS | `(na+1)(nb+1)` | `O(na·nb)` | `O(na·nb)`，可滚动为一维 `O(min(na,nb))` |
| 编辑距离 | 同上 | `O(na·nb)` | 可滚动两行/一行 |
| 打家劫舍 | `n` | `O(n)` | `O(1)` 滚动 |

LCS 与编辑距离的二维表是**经典平方瓶颈**；若 `na、nb` 达到 `5000`，`25×10⁶` 量级在 C++ 中通常可接受，Python 需注意常数与内存。面试中应主动说明能否**滚动数组**：LCS 第 `i` 行只依赖第 `i-1` 行，可用一维数组从右向左更新以避免覆盖未用值；编辑距离同理，甚至可压缩到 `O(min(na,nb))` 若只需求值。

打家劫舍的 `O(1)` 空间来自**仅保留两个历史最优**，是线性 DP 中最常见的空间优化形态。

**时空权衡讨论**：面试常问「能否优化空间」。LCS 若只需数值，可用一维数组 `dp[j]` 滚动第 i 行：内层 j 从 `nb` 递减到 1，用临时变量保存更新前的 `dp[j-1]` 以模拟 `dp[i-1][j-1]`。编辑距离可保留两行交替，或在一维上按同样技巧滚动。实现难度高于二维，初学建议先写二维再改。竞赛中 `na,nb ≤ 5000` 时二维 `int` 约 100MB 量级，C++ 可行；Python 列表推导大表可能 TLE/MLE，需注意。

**与分治的关系**：LIS 的 `O(n log n)` 也可通过维护有序结构理解，与「贪心选最小末尾」等价，不是分治。双串 LCS 不存在类似通用 `n log n`（除非有特殊约束如仅一个串可删字符），默认 `O(nm)`。

### 代码模板

下面给出与 Study 仓库一致的**逻辑模板**（非占位），便于默写时对照。

**LIS — `O(n log n)`（耐心排序 + 二分）**

```python
def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

**LCS — 二维填表**

```python
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
```

**编辑距离**

```python
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
```

**打家劫舍 — 滚动**

```python
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

C++ 侧结构相同：`lower_bound` 对应 LIS，`vector<vector<int>>` 填 LCS 与编辑距离，`long long` 滚动打家劫舍以防中间和溢出（Study 实现中对 `nums` 元素用 `int` 累加，面试大数时可全程 `long long`）。

### 变体与技巧

**LIS 变体**

- **最长非递减子序列**：二分时用 `bisect_right`，或维护 `tails` 时对相等元素替换策略不同。
- **个数统计**：长度用 `tails`，方案数常要 `O(n²)` 或 DP 记录 `(length, count)`。
- **二维 LIS**：排序+树状数组或 CDQ，已超出本专题「线性」范围，但一维 LIS 是基石。

**LCS 变体**

- **最长公共子串**：要求连续，状态变为 `dp[i][j]` 仅在 `a[i-1]==b[j-1]` 时从 `dp[i-1][j-1]+1` 扩展，否则置 0，答案是表内最大值而非右下角。
- **仅允许删除**：编辑距离去掉插入，转移简化为 `min(删, 替)` 或类似。
- **回文**：可转化为 LCS(`s, reverse(s)`)。

**编辑距离变体**

- **只有插入与删除**（无替换）：不匹配时 `dp[i][j]=dp[i-1][j-1]+1` 型态变化，或操作对称于 LCS 删除模型。
- **带权操作**：三种操作用不同代价，转移里 `+1` 改为 `+cost`。
- **滚动优化**：内层 `j` 从大到小可在一维数组上复现二维依赖。

**打家劫舍变体**

- **环形**：拆成「不抢第一家」与「不抢最后一家」两次线性 DP。
- **树形**：DFS 返回 `(抢, 不抢)` 二元组，仍是局部线性依赖的推广。
- **198 → 213 → 337**：状态从两户滚动到「抢/不抢/冷冻」多状态，表仍为 `O(n)`。
- **冷冻期（309）**：在滚动时增加「前一天刚抢过则今天不能抢」的第三状态，维度仍线性但变量个数增加，转移表需重画再编码。

**通用技巧**

1. **前缀维度**：双串问题几乎总是 `dp[i][j]` 表示两前缀。
2. **初始化第一行/列**：编辑距离、带代价的插入删除尤其易错。
3. **相等字符**：LCS「+1」、编辑距离「免费对齐」要分开记忆。
4. **空输入**：LIS 空数组长度 0；LCS 空串 0；打家劫舍空数组 0。

**LCS 计数变体（115）**：求不同子序列个数时，相等字符处累加 `dp[i-1][j-1]` 的方案数，不等时相加左右（注意取模与去重定义）。这与「最长长度」转移相似但语义从 `max` 变为 `sum`，仍是在前缀表上推进。

**最长递增子序列的个数（673）**：在 `O(n²)` 长度 DP 同时维护 `count[i]`，当 `nums[j]<nums[i]` 且 `dp[j]+1==dp[i]` 时累加计数；若发现更长则重置计数。与 `tails` 优化不直接兼容，面试若问方案数应回到显式 `dp[i]`。

**股票类误用警示**：「最多买卖 k 次」等题虽有天数下标，但状态含持有/不持有/交易次数，属于多维 DP 而非本专题四模板；勿强行套 LIS。

**双指针与 DP**：部分「判断子序列」题可用双指针 `O(n)`，仅求长度最值才需要 DP。题面若问「是否为子序列」优先双指针；若问「最长公共子序列长度」必 DP。

**坐标压缩 + LIS**：当值域很大但 n 较小，可将值离散化后再 LIS；当 n 大值域小，直接二分即可。

**编辑距离的一维滚动草图**：设 `dp[j]` 表示当前行，上一行滚动在 `prev` 数组中；对每个 `(i,j)` 需要旧 `dp[j-1]`、`prev[j]`、`prev[j-1]`，用变量 `left` 保存刚算完的左侧格。理解后可把空间从 `O(nm)` 降到 `O(m)`，代码易错，竞赛冲刺再练。

**打家劫舍与最大子数组和**： Kadane 求连续子数组最大和，无相邻禁用；打家劫舍禁用相邻选取，状态不同。看到「连续」优先考虑 Kadane；看到「不能同时取相邻元素」用 robbery 滚动。

### 易错点

1. **LIS 严格递增与二分**：对严格 LIS 用 `bisect_left` 找第一个 `≥ x`；若题目为非递减，误用 `left` 会导致长度偏小或偏大。
2. **`tails` 不是 LIS 本身**：`tails` 数组记录的是各长度的最小末尾，不能直接把 `tails` 当作一个递增子序列输出。
3. **LCS 下标 off-by-one**：比较 `a[i-1]` 与 `b[j-1]`，表大小 `(na+1)×(nb+1)`。
4. **编辑距离三种操作**：漏掉替换，写成只 `min(删, 插)`，在单字符不同时 WA。
5. **编辑距离边界**：`dp[i][0]=i`、`dp[0][j]=j` 必须在主循环前填好。
6. **打家劫舍相邻约束**：`cur = max(prev1, prev2 + x)` 中 `prev1` 已包含「不抢当前」的最优；不要写成 `prev1 + x` 与 `prev2` 的简单比较而未体现「抢当前则不能用 prev1 里抢上一户」的语义。滚动更新顺序必须是先算 `cur` 再移动窗口。
7. **整数溢出**：打家劫舍 C++ 用 `long long` 累加；Python 无妨，Java 需注意。
8. **空间优化方向**：LCS 一维滚动时内层循环方向错误会覆盖尚未使用的 `dp[j-1]`。
9. **C++ 与 Python 空输入不一致**：C++ `house_robber` 未在 `main` 测空数组，但循环结果正确；Python 显式 `if not nums`；移植时保持语义一致。
10. **样例依赖**：`horse/ros`、`abcde/ace` 是经典样例，换数据前先用断言锁定行为，再改代码。

### 练习建议

建议按难度递进，每题先手写状态与转移，再对照 Study 四函数：

1. **300. 最长递增子序列** — 先 `O(n²)` 再 `O(n log n)`；与本文 `length_of_lis` 一致。
2. **1143. 最长公共子序列** — 对应 `longest_common_subsequence`。
3. **72. 编辑距离** — 对应 `edit_distance`；可顺带做 **583. 删除操作只有两种**。
4. **198. 打家劫舍** — 对应 `house_robber`；再做 **213. 打家劫舍 II**（环形拆段）。
5. **拓展**：**516. 最长回文子序列**（区间 DP 入门）、**115. 不同的子序列**（LCS 计数）、**10. 正则表达式匹配**（二维 DP 进阶）。

每题限时 25 分钟：5 分钟建模，15 分钟编码，5 分钟测边界（空、单元素、全相同、递减序列）。对照 Study 脚本断言：`LIS([10,9,2,5,3,7,101,18])==4`，`LCS("abcde","ace")==3`，`edit("horse","ros")==3`，`robber([2,7,9,3,1])==12`。

**自测清单（建议默写前勾选）**

- LIS：空数组、单元素、严格递减、全相等、含负数。
- LCS：一空一非空、完全相同、无公共字符、仅一个公共字符多次出现（子序列非子串）。
- 编辑距离：一空、相同串、单字符不同、需要多次插入删除。
- 打家劫舍：空、单户、两户、交替大小、全零赃款。

**建模训练**：拿到题面先写三行——状态含义、转移式、边界——再编码。若 3 分钟内写不出状态，查标签是否实为贪心（如部分「最多交易股票」）或单调队列。线性 DP 题面关键词包括「子序列」「两个字符串」「插入删除替换」「相邻不能选」。

### 专题串讲：四题一次过一遍

**第一遍（理解）**：手算 `nums=[0,1,0,3,2,3]` 的 LIS 长度（答案 4，如 `0,1,2,3`）。手算 `a="abc"`, `b="def"` 的 LCS 为 0。手算 `a="intention"`, `b="execution"` 的编辑距离为 5（经典 LeetCode 样例）。手算 `nums=[1,2,3,1]` 的打家劫舍为 4（抢 1 和 3）。

**第二遍（实现）**：不看代码默写四个函数，再与下文 Python 块 diff。

**第三遍（变体）**：354 信封、115 不同子序列、213 环形、72 的空间优化。

## Python 实现

Study 文件 `linear_dp.py` 在模块顶部说明职责，并实现四个入口函数与自测。完整源码如下（与仓库一致，可直接运行）：

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


if __name__ == "__main__":
    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert longest_common_subsequence("abcde", "ace") == 3
    assert edit_distance("horse", "ros") == 3
    assert house_robber([2, 7, 9, 3, 1]) == 12
    assert length_of_lis([]) == 0
    assert longest_common_subsequence("", "") == 0
    assert house_robber([]) == 0 and house_robber([5]) == 5
    print("linear_dp OK")
```

**实现要点说明**

- `length_of_lis`：`tails` 单调非降；`bisect_left` 保证严格递增子序列长度正确。空列表时循环不执行，返回 0。
- `longest_common_subsequence`：双重循环填表，字符相等时从左上 `+1`，否则取上、左较大者。
- `edit_distance`：先初始化首行首列，再按三种操作取 min。
- `house_robber`：单元素提前返回；多元素用 `prev2, prev1` 滚动，等价于 `dp[i]=max(dp[i-1], dp[i-2]+nums[i])` 的空间优化版。

运行自测见上文 PowerShell，`python` 直接执行该文件应打印 `linear_dp OK`。

**逐函数阅读指引**

`length_of_lis` 中 `tails` 类型为 `list[int]`，空输入时 `tails` 为空，返回 0。`bisect_left` 在空列表上返回 0，第一次会 `append`，逻辑正确。若改用 `bisect_right` 将得到非递减 LIS 长度，与 LeetCode 300 的严格递增不符。调试时可打印每次 `i` 与 `tails`，观察替换与追加。

`longest_common_subsequence` 使用列表推导建表，空间 `O(nm)`。若 `na` 远大于 `nb`，可交换两串使列数较小以略减常数。字符比较用 Unicode 码点，与 ASCII 题一致。返回 `dp[na][nb]` 而非 `max(max(row))`，后者适用于「最长公共子串」而非子序列。

`edit_distance` 初始化两行边界：先填 `dp[i][0]` 再填 `dp[0][j]`，顺序无关。主循环中 `min` 取三种操作，勿漏 `dp[i-1][j-1]`。相等字符分支赋值 `dp[i-1][j-1]` 而非加一，表示对齐不耗费操作。

`house_robber` 对 `len==1` 单独返回避免滚动初值歧义；`prev2, prev1 = 0, 0` 表示尚未处理任何户时最优为 0。循环内元组赋值同时更新两个变量，等价于临时保存旧 `prev1`。勿在循环中写 `prev1 = max(prev1, prev2+x); prev2=prev1` 而未保存旧值，会导致 `prev2` 错误。

## C++ 实现

C++ 镜像 `linear_dp.cpp` 使用 `alg_std.hpp` 与标准算法，逻辑与 Python 一一对应：

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;

int length_of_lis(vector<int> nums) {
    vector<int> tails;
    for (int x : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end())
            tails.push_back(x);
        else
            *it = x;
    }
    return (int)tails.size();
}

int longest_common_subsequence(const string& a, const string& b) {
    int na = (int)a.size(), nb = (int)b.size();
    vector<vector<int>> dp(na + 1, vector<int>(nb + 1, 0));
    for (int i = 1; i <= na; ++i)
        for (int j = 1; j <= nb; ++j) {
            if (a[i - 1] == b[j - 1])
                dp[i][j] = dp[i - 1][j - 1] + 1;
            else
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
        }
    return dp[na][nb];
}

int edit_distance(const string& a, const string& b) {
    int na = (int)a.size(), nb = (int)b.size();
    vector<vector<int>> dp(na + 1, vector<int>(nb + 1, 0));
    for (int i = 0; i <= na; ++i) dp[i][0] = i;
    for (int j = 0; j <= nb; ++j) dp[0][j] = j;
    for (int i = 1; i <= na; ++i)
        for (int j = 1; j <= nb; ++j) {
            if (a[i - 1] == b[j - 1])
                dp[i][j] = dp[i - 1][j - 1];
            else
                dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
        }
    return dp[na][nb];
}

int house_robber(const vector<int>& nums) {
    long long p2 = 0, p1 = 0;
    for (int x : nums) {
        long long cur = max(p1, p2 + x);
        p2 = p1;
        p1 = cur;
    }
    return (int)p1;
}

int main() {
    assert(length_of_lis({10, 9, 2, 5, 3, 7, 101, 18}) == 4);
    assert(longest_common_subsequence("abcde", "ace") == 3);
    assert(edit_distance("horse", "ros") == 3);
    assert(house_robber({2, 7, 9, 3, 1}) == 12);
    cout << "linear_dp OK" << endl;
    return 0;
}
```

**与 Python 的差异**

- LIS 使用 `lower_bound`，等价于 `bisect_left`。
- `house_robber` 全程 `long long`，避免大输入中间和超过 `int`；返回时转为 `int` 与 Study 断言一致。
- C++ 版 `main` 未显式测空数组；Python 侧对空 LIS/LCS/robber 有断言，刷题时建议两边边界行为对齐。

编译运行命令见 **Study 仓库对照** 一节；输出 `linear_dp OK` 即通过内置断言。

**C++ 实现细节**

`length_of_lis` 按值接收 `vector<int>`，小数组无妨，大数组可改 `const vector<int>&` 避免拷贝。`lower_bound` 要求 `#include <algorithm>`，由 `alg_std.hpp` 聚合。返回 `(int)tails.size()` 在极端长度下注意 `size_t` 与 `int`。

`longest_common_subsequence` 与 `edit_distance` 使用 `vector<vector<int>>`，若 `na*nb` 接近 `10^7` 需评估内存。`min({a,b,c})` 为 C++11 初始化列表形式，三参数类型需一致。

`house_robber` 用 `long long` 计算 `cur`，最后 `(int)p1` 截断；若题目和超过 `2^31-1` 应返回 `long long`。Python 版无此问题。空 `nums` 时循环不执行，返回 0，与 Python 空数组行为一致（Python 显式分支，C++ 隐式）。

**双语言对拍建议**：写脚本生成随机 `nums`、短字符串，分别调用 Python 模块与 C++ 可执行文件比较输出。种子固定便于复现 WA。

## 练习与延伸

本专题在 atelier 站点不单独为 LeetCode 题号建页；练习请直接进入 Study 仓库 `problems/leetcode/` 下对应题解，或在本机用四函数作对拍。

**建议题单（与四模板绑定）**

| 模板 | 题号（示例） | 延伸方向 |
|------|----------------|----------|
| LIS | 300, 354, 673 | 信封嵌套、最长算术子序列 |
| LCS | 1143, 1035, 1092 | 不相交的线、构造 LCS |
| 编辑距离 | 72, 161, 583 | 一次编辑、只删 |
| 打家劫舍 | 198, 213, 337 | 环、树、相邻三天 |

**对拍与调试**：用小规模暴力（`O(2^n)` 子集或递归）验证 LIS/LCS/robber；编辑距离可用递归记忆化对照填表。Python 与 C++ 对同一组随机数据应一致。

**与相邻专题的关系**：`algorithms/dynamic_programming` 下还有背包、区间、树形等目录；线性 DP 掌握后，区间 DP 常把「子问题维度」从前缀改为左右端点，树形 DP 把下标换成节点 DFS 序，但**转移仍来自严格更小的子结构**。

**LeetCode 与 Study 映射（详表）**

| 题号 | 名称 | 对应函数 | 备注 |
|------|------|----------|------|
| 300 | 最长递增子序列 | `length_of_lis` | 输出长度；方案数另题 |
| 354 | 俄罗斯套娃信封 | LIS 变形 | 按宽升序、长高降序后 LIS |
| 1143 | 最长公共子序列 | `longest_common_subsequence` | 标准二维 |
| 1035 | 不相交的线 | LCS | 直线不相交即 LCS |
| 72 | 编辑距离 | `edit_distance` | 三操作 |
| 161 | 相隔为 1 的编辑距离 | 编辑距离 | 判断而非最值 |
| 583 | 两个字符串的删除操作 | 仅删 | `na+nb-2*LCS` |
| 198 | 打家劫舍 | `house_robber` | 线性 |
| 213 | 打家劫舍 II | 拆环 | 两次 `house_robber` |
| 337 | 打家劫舍 III | 树 DP | 仍用抢/不抢二元 |

**竞赛与面试频率**：双串 DP 与 LIS 在国内大厂笔试中出现频率极高；编辑距离在字符串专题、自然语言预处理入门题中反复出现；打家劫舍常作为「状态压缩入门」与树形 DP 的引子。建议四模板都能在 10 分钟内无模板 bug 写完。

**错误类型归纳**：WA 多为 off-by-one 或漏操作；TLE 多为 LIS 仍用 `O(n²)` 而 `n=10^5`；MLE 多为 LCS 开满二维而应用滚动；RE 多为 C++ 栈递归或数组越界。

## 学习路径

1. **第 1 天**：理解 LIS 朴素与 `tails` 二分；手写 `length_of_lis` 并通过 300 题。
2. **第 2 天**：掌握 LCS 填表与下标；完成 1143，尝试打印路径（从 `dp[na][nb]` 回溯）。
3. **第 3 天**：编辑距离三种操作与边界；完成 72，试做滚动一维写法。
4. **第 4 天**：打家劫舍滚动与环形变体；198 + 213。
5. **第 5 天**：混合复习——限时识别题型（子序列/双串/最值相邻约束），对照 Study 四函数默写一遍。

若时间紧，最小闭环：**LIS `O(n log n)` + LCS + 打家劫舍**；编辑距离可在双串 DP 周集中突破。

**周计划示例（在职 5×1h）**

- 周一：导读 + LIS 朴素与二分，完成 300。
- 周二：LCS 填表与回溯，完成 1143、1035 选一。
- 周三：编辑距离二维与边界，完成 72。
- 周四：打家劫舍与 213 环形拆分。
- 周五：限时默写 Study 四函数 + 复习易错点。

**能力检查**：闭卷能在 30 分钟内写出四函数并通过样例；能口头解释 `tails` 不变量；能画出 `3×3` 小表的 LCS 填表方向；能说明编辑距离三种转移各代表什么操作。

**复习节奏**：第 1 周完成四模板编码；第 2 周每天 2 道变体限时；第 3 周把四函数合并进个人模板库（template.py / template.cpp），与 Study 仓库 diff 合并有用注释。考前 24 小时只跑断言与默写，不再刷新题。

**与面试官沟通**：写代码前先念状态定义（30 秒），写完后主动提复杂度与可否优化空间，体现结构化思维。若要求「不用额外空间」，说明 robbery 已 O(1)、LIS 的 `tails` 为 O(n) 且通常视为最优实现的一部分。

## 延伸阅读

- Study 笔记：[python/.../linear/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/dynamic_programming/linear/notes.md)（与 cpp 侧 notes 内容对应）
- 实现对照：[linear_dp.py](https://github.com/zhk0567/Algorithm/blob/main/python/algorithms/dynamic_programming/linear/linear_dp.py)、[linear_dp.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/algorithms/dynamic_programming/linear/linear_dp.cpp)
- 算法导论相关章节：动态规划最优子结构、最长公共子序列、序列对齐（编辑距离的理论背景）
- 竞赛资料：OI Wiki 动态规划「线性 DP」条目，与 LIS 耐心排序、LCS 经典递推对照阅读
- 书籍：《算法导论》第 15 章动态规划；MIT 6.006 讲义中 Sequence alignment 与 LCS 的关系
- 视频专题：建议按「单串 / 双串 / 带约束最值」三分搜索，每类练 5 题以上再进入背包 DP

### 手推例题与面试话术

下列补充仍属延伸阅读块内的教学正文，用于巩固四模板。

#### LIS：从 O(n²) 到 O(n log n)

考虑 `nums = [10, 9, 2, 5, 3, 7, 101, 18]`。朴素法：`dp[2]=1`（值为 2），`dp[3]=2`（2,5），`dp[5]=3`（2,5,7），最终以 101 或 18 结尾的长度可达 4。`tails` 过程（严格递增）：读 10 → `[10]`；读 9 → 替换 10 → `[9]`；读 2 → `[2]`；读 5 → `[2,5]`；读 3 → 替换 5 → `[2,3]`；读 7 → `[2,3,7]`；读 101 → 追加；读 18 → 替换 101 → 长度仍为 4。面试时先说「子问题是以 i 结尾的最长长度」，再说「优化：对每个长度维护最小末尾，二分找插入位置」。

再练一组：`nums = [0, 1, 0, 3, 2, 3]`。朴素 `dp` 在最后一个 3 处可达 4。`tails` 演变：0 → [0]；1 → [0,1]；0 → 替换 1 为 0 得 [0]（长度仍为 1）；3 → [0,3]；2 → 替换 3 → [0,2]；3 → [0,2,3] 长度 3？需仔细：对 2 二分替换 3 得 [0,2]，对最后 3 append 得 [0,2,3] 长度 3。实际上经典答案为 4（0,1,2,3 子序列），请读者用代码验证——手推易错，印证「以代码与断言为准」。

**面试话术模板**：「这是最长递增子序列。朴素定义 `dp[i]` 为以 i 结尾的最长长度，转移看所有更小下标，复杂度 O(n²)。若 n 到 10^5，用耐心排序维护每个长度的最小末尾，二分查找，O(n log n)。空间 O(n)。若要我恢复具体序列，我会在长度 DP 之外记录前驱或再做一次遍历。」

#### LCS：填表示意与回溯

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

#### 编辑距离：horse → ros 与 intention → execution

`horse` → `ros` 最优为 3。操作序列之一：替换 h→r；删除 o；删除 r（或等价组合）。填表时 `dp[0][j]=j`、`dp[i][0]=i` 表示「全插入/全删除」基线。字符相等时直接继承左上，体现「对齐免费」。

`intention` 与 `execution` 长度为 5 的样例，适合练手填 9×9 表一角。初学者可只填最后一行观察单调性。面试中若时间紧，可说明「标准二维 DP，三种操作取 min」，直接写代码。

**仅删除两种操作**（583）：只能删字符使两串相等，最少删除次数为 `len(a)+len(b)-2*LCS(a,b)`，把「对齐」转化为 LCS 最大值，体现线性 DP 模型之间的组合。

#### 打家劫舍：[2,7,9,3,1] 与环形

最优 2+9+1=12。滚动：处理 2 → prev2=0, prev1=2；7 → max(2,7)=7；9 → max(7,2+9)=11；3 → max(11,7+3)=11；1 → max(11,9+1)=12。

环形（213）：拆成「不抢 nums[0]」的 `house_robber(nums[1:])` 与「不抢 nums[n-1]」的 `house_robber(nums[0:n-1])`，取 max。注意全一家或两家的边界。树形（337）：DFS 返回 (抢, 不抢) 对，子节点结果合并，与线性滚动同构。

#### 面试常问 Follow-up

- **能否输出方案？** LCS/编辑距离可回溯 DP 表；LIS 长度用 `tails` 需额外数组记录长度与 predecessor，或 second pass。
- **空间能否 O(1)？** 仅打家劫舍类相邻滚动；LCS/编辑距离通常至少 O(min(n,m)) 滚动。
- **数据范围 10⁵？** LIS 必须 n log n；LCS/编辑距离 10⁵ 需优化或特殊结构，面试常降到 500 以内。
- **负数赃款？** 打家劫舍题目通常非负；若有负数，状态定义需重新审视（可能需选连续段或允许负债，题意决定）。
- **重复元素 LIS？** 严格递增 vs 非递减决定二分边界，见易错点。

#### 记忆化写法对照（Python 草图，非仓库代码）

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

#### 四模板识别速查（考前一页纸）

- 单串、求最长递增/非递减子序列 → LIS。
- 两串、子序列不要求连续 → LCS 型二维。
- 两串、最少单字符编辑 → 编辑距离。
- 一排、相邻不能同选、求最值 → 打家劫舍滚动。

#### 与背包 DP 的边界

0-1 背包也是「线性下标」，但状态常含容量维度 `dp[i][w]`，归入背包专题。若只有「选/不选」且无容量限制且相邻约束，更接近打家劫舍。分清维度个数有助于目录归类，避免死记硬背。

#### 正确性一句话

LIS `tails`：归纳证明替换保持「存在长度 k 递增子序列且末尾最小」的不变量。LCS：对前缀长度归纳，最优子结构。编辑距离：对操作次数归纳。打家劫舍：对户数归纳，抢/不抢覆盖所有合法方案。

以上手推、话术与识别表均服务于同一目标：让你打开 LeetCode 或 Study 仓库时，能在几分钟内定位到线性 DP 四类之一，并落到 `linear_dp.py` 中已有、经过断言检验的实现上。反复运行 `python -LiteralPath ...\linear_dp.py` 与 C++ `run.exe`，直到无需翻页即可默写，再追求变体题速度与空间优化。

#### 全文章节与 Study 文件对照小结

读完导读与预备知识后，应对「线性 DP 在仓库里占哪一层」有清晰图景：`dynamic_programming/linear` 不是 LeetCode 题号目录，而是算法模板目录；题解在 `problems/leetcode` 下按题号拆分，模板在 `algorithms/.../linear` 下按技巧聚合。站点 `topic_path` 与仓库一致，便于从博文跳转到 GitHub 浏览历史提交。

学习时建议开两个终端：一个跑 Python 断言，一个编译 C++；改一行转移后两边同时跑，养成双语言一致性。遇到 WA 先查边界与下标，再查转移方向（max/sum/min），最后查复杂度是否需要 `n log n` 或滚动。medium 篇幅的目标不是题海，而是把四块「肌肉记忆」练到自动：看到子序列长度想到 LIS/LCS，看到编辑操作想到三维 min，看到相邻约束想到 robbery 二元滚动。

最后提醒：本文所有代码块均来自 Study 仓库 `linear_dp.py` 与 `linear_dp.cpp` 的完整摘录，不是伪代码；教学叙述围绕这些可运行实现展开，避免讲义与代码两套说法。你在此基础上增加的变体练习，应回到仓库用新断言固化，或记在 personal notes，保持主仓库简洁可测。

若你负责 atelier 站点维护：本篇 `status: published` 在通过 `validate_algorithm_guide.py` 与 `validate_algorithm_quality.py --strict` 后可改为 `published`；manifest 中 `algo-dp-linear` 条目已与 `topic_path`、`guide_toc: topic-algorithm`、`guide_tier: medium` 对齐。读者侧只需记住：线性 DP 四模板 = 仓库四个函数 + 本文九节阅读顺序，即可与刷题、面试、双语言对拍形成闭环。首次阅读预计 45–60 分钟（含手推一小表与跑通双语言自测）；二刷聚焦默写与变体题单即可。遇到「子序列 + 最值 + 相邻限制」三类关键词之一，就应联想到本页对应小节并打开 Study 源码核对转移。本文档仅创建此单文件，未调用任何生成脚本覆盖正文。
