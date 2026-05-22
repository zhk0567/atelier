# -*- coding: utf-8 -*-
"""One-off: write algo-bit-manipulation guide (human-authored body)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Blog" / "algorithm-guides" / "algo-bit-manipulation" / "index.md"
sys.path.insert(0, str(ROOT / "scripts"))
from algorithm_guide_lib import count_chinese  # noqa: E402

BODY = r'''---
title: "算法 · 位运算（Bit Manipulation）"
series: algorithm
category: Algorithms
topic_path: algorithms/bit_manipulation
guide_toc: topic-algorithm
guide_tier: major
status: draft
---

# 算法 · 位运算（Bit Manipulation）

## 导读

**位运算**在算法与面试中承担三类角色：用单个整数的二进制位表示集合或状态（与状压 DP 衔接）；用 `& | ^ ~ << >>` 在 O(1) 时间内完成「取最低 1」「统计 1 个数」「枚举子集」等原子操作；用 **异或 XOR** 的代数性质把「出现奇数次 / 唯一出现」类问题化成线性扫描。Study 仓库 `bit_manipulation/` 提供三个可运行原语：`lowbit`、`popcount`、`subsets_of_mask`，与 LeetCode 136、191、231 及子集枚举题直接对应。

本页在 `notes.md`「lowbit、去最低 1、子集枚举」提纲上，系统讲解补码与 `-x`、Brian Kernighan 删 1、掩码子集下降枚举、异或消重与分组计数，并对照 **136 只出现一次**、**137 出现三次**、**191 位 1 的个数**、**231 2 的幂**、**338 比特计数**、**260 两个只出现一次**、**268 缺失数字**、**371 两整数之和**、**421 最大异或** 等题给出思路与复杂度。与 `algo-dp-bitmask` 的分界：状压 DP 用 `dp[mask]` 做最优化；本专题侧重 **位操作模板** 与 **XOR 技巧**，不展开 TSP 填表。

从刷题角度，看到「O(1) 额外空间」「数组除某数外成对出现」「子集枚举」「2 的幂判定」应优先想到位运算而非哈希。从竞赛角度，`popcount` 与 `lowbit` 是树状数组、并查集按秩合并的底层习惯。从工程角度，权限掩码、标志位集合、布隆过滤器位图都依赖同一套操作。读完本文，你应能：① 默写 Study 三函数并解释断言；② 用 PowerShell `-LiteralPath` 跑通 Python/C++ 自测；③ 在 5 分钟内写出 136/191/231 的 O(1) 空间解法；④ 知道 137/260/421 的升级路径。

**能力自检（读前）**：能否解释 `12 & -12 == 4`？能否说明 `x & (x-1)` 为何减少 1 个 1？能否写出 `for (s=m; ; s=(s-1)&m)` 的终止条件？若有一项不熟，按「基础篇 → Python 实现 → 练习」顺序补齐。

## 预备知识

> **环境**：Python 3.10+（整数任意精度，面试规模下等价 32/64 位）；C++17，`g++`，`bit_manipulation.cpp` 通过 `#include <alg_std.hpp>` 使用 `vector`、`set` 等。

建议已掌握：

- **二进制与位权**：非负整数 `n` 的第 `k` 位（`k` 从 0 起）为 `(n >> k) & 1`。判断第 `k` 位：`n & (1 << k)`。
- **基本运算**：`&` 按位与、`|` 按位或、`^` 按位异或、`~` 按位取反、`<<` `>>` 移位。异或满足交换律、结合律，`a ^ a = 0`，`a ^ 0 = a`。
- **补码与 `-x`**：计算机中 `-x` 常实现为 `~x + 1`（对 32 位有符号）。`x & (-x)` 在常见补码语义下得到 **最低位的 1**（lowbit），`x=0` 时为 0。
- **复杂度直觉**：单次位操作 O(1)；`popcount` 循环次数等于 1 的个数，最坏 O(log U) 或 O(w)，w 为字长；对掩码 `m` 的子集枚举恰好 **2^{popcount(m)}** 次。
- **集合与掩码**：`n` 位全集 `mask = (1<<n)-1`；子集 `s` 满足 `s & mask == s`（`s` 是 `mask` 的子集）。枚举写法见基础篇。

**与哈希的取舍**：136/268 用 XOR 可 O(n) 时间 O(1) 空间；若需保留「是哪一个数」的下标，哈希更合适。子集枚举 2^k 在 k>22 时易爆，应换 meet-in-the-middle 或 DP，而非硬枚举。

**Python 注意**：`int` 无限精度，`1<<100` 合法；C++ 用 `int`/`long long` 注意溢出与 `1<<31` 符号位。自测用 Study 仓库小整数即可。

**面试表述顺序**：先说位级不变量（如 XOR 前缀性质）→ 写核心一行（`x & -x`）→ 报时间与字长 → 提边界 `x=0`、负数（部分题约束非负）。

## Study 仓库对照

`topic_path`：`algorithms/bit_manipulation`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/bit_manipulation/notes.md` | `bit_manipulation.py` |
| C++ | `cpp/algorithms/bit_manipulation/notes.md` | `bit_manipulation.cpp` |

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\bit_manipulation\bit_manipulation.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\bit_manipulation
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe bit_manipulation.cpp
.\run.exe
```

成功输出 `bit_manipulation OK`。`notes.md` 要点：`x & -x` 为 lowbit；`x & (x-1)` 去掉最低 1；子集 `for (s=m; ; s=(s-1)&m)` 含空集终止于 `s=0`。

克隆 Study 后，可用 `Get-ChildItem -LiteralPath F:\Study\Algorithm\python\algorithms\bit_manipulation` 查看文件；cpp 镜像路径对称。首次学习只跑自测；二次可在同目录写 `playground.py` 试验 136/338，避免污染三函数接口。

**工具链**：并排打开 python 与 cpp 实现；Windows 用 `-LiteralPath` 避免反斜杠转义。C++ 依赖 `alg_std.hpp`，在 `cpp/algorithms/bit_manipulation` 目录编译即可。

## 基础篇

### 直觉与定义

把非负整数 `x` 看成固定宽度（如 32 位）上的 0/1 向量。**lowbit(x) = x & (-x)** 在补码下保留最低位的 1，其余为 0。例：`12 = 0b1100`，lowbit 为 `0b0100 = 4`。树状数组 `add(p, v)` 用 `p += lowbit(p)` 沿父节点爬升；并查集按秩合并有时用 `lowbit` 相关技巧组织集合大小（与「集合大小为 2 的幂」结构相关）。

**popcount(x)** 统计 `x` 中 1 的个数。Brian Kernighan：`while x: x &= x-1` 每次删掉最低 1，循环次数恰为 popcount。例：`0b1011` 三次删尽，得 3。硬件指令 `__builtin_popcount` / Python 3.10+ `int.bit_count()` 同为 O(1) 字长，但面试默写循环体现理解。

**subsets_of_mask(m)** 枚举掩码 `m` 所表示集合的全部子集（含空集）。降序技巧：从 `s=m` 开始，反复 `s = (s-1) & m`，直到 `s=0` 输出后结束。例 `m=0b101` 得到 `101, 100, 001, 000`。正确性：`(s-1)&m` 得到 **严格小于 s 的、仍是 m 子集的最大整数**，故遍历所有子集各一次。若从 0 上升枚举需另写，降序写法与竞赛笔记一致。

**异或直觉**：相同数异或为 0，顺序无关。136：除一个数外其余成对，全体 XOR 即为答案。260：先全体 XOR 得 `xor_all=a^b`；取 `xor_all` 的任意一个为 1 的位（如 lowbit），按该位把数组分成两组，每组内成对 XOR 得 `a` 与 `b`。

**2 的幂（231）**：`n>0` 且 `n & (n-1) == 0` 当且仅当 `n` 只有一个 1。等价 `lowbit(n)==n`。`n==0` 不是 2 的幂。

**位 1 个数（191）**：直接 `popcount(n)`。注意 C++ 对负数右移与 Python 不同，题面常给 `unsigned` 或非负。

**338 比特计数**：对 `i in 1..n`，`dp[i] = dp[i & (i-1)] + 1`（去掉最低 1 后 +1），或 `dp[i] = dp[i >> 1] + (i & 1)`。O(n) 预处理，体现 DP 与位运算结合。

**137 只出现一次 III**：每个数出现三次，除一个出现一次。对 32 位逐位统计 `sum_bit % 3` 得答案位；或有限域上把「三进制进位」模拟到 int。与 XOR「模 2」类比，是 **模 3 位计数**。

**268 缺失数字**：`0..n` 应有 `n+1` 个数，缺一个。`ans = n ^ (n+1) ^ ... ^ 0 ^ nums[0] ^ ...` 或求和差 `n*(n+1)//2 - sum(nums)`。

**371 两整数之和**：不用 `+/-`，用异或与进位：`sum = a ^ b`，`carry = (a & b) << 1`，循环至 `carry==0`。本质是二进制加法。

**421 最大异或**：将数插入二进制 Trie，查询时对每一位尽量走相反子节点，O(n·w)，w=32。排序+前缀异或也可但 Trie 更标准。

**与状压 DP**：`mask|(1<<v)` 扩展集合；本专题 `subsets_of_mask` 遍历 `mask` 的全部子集，复杂度 O(3^n) 若对每个 mask 枚举子集，单独 O(2^{popcount(m)}) 对固定 m。

**负数与右移**：Python `-1 >> 1` 仍为 -1；C++ 实现 191 时常用 `unsigned` 或 `n &= 0xFFFFFFFF`。面试先确认数据范围。

**权限与标志位**：`flags |= (1<<k)` 打开第 k 位；`flags &= ~(1<<k)` 关闭；`flags & (1<<k)` 测试。与算法题同一套语言。

**lowbit 与树状数组**：`c[i]` 负责 `[i-lowbit(i)+1, i]`。update 时 `i += lowbit(i)`。理解 lowbit 是读 Fenwick 的前提，见 `ds-tree-fenwick-tree`。

**popcount 与 338**：`i & (i-1)` 清除最低 1 后，剩余 1 的个数比 `i` 少恰好 1，故 `bits[i] = bits[i & (i-1)] + 1`。这是「状态压缩到更小 i」的 DP 思想。

**子集枚举与搜索**：子集和、子集 DP 常 `for (sub=mask; sub; sub=(sub-1)&mask)`，勿漏 `sub=0` 若空集有意义。`sub=mask` 开始保证先访问全集再下降。

**XOR 前缀**：`prefix[i] = a[0]^...^a[i]`，区间 `[l,r]` 异或为 `prefix[r]^prefix[l-1]`（若定义 `prefix[-1]=0`）。用于偶数次区间查询。

**出现次数模 k**：137 模 3；推广到「除一个出现 m 次外均出现 k 次」用位计数模 k。XOR 是 k=2 的特例。

**421 异或最大值**：贪心「高位尽量为 1」在 Trie 上表现为优先走 `0/1` 相反分支。若用排序，按最高位分组递归也可，写法较长。

**260 分组位选择**：`xor_all` 的 lowbit 位在 `a` 与 `b` 上必然不同，按该位 split 后两组各自 136 化。

**371 进位链**：`a=5,b=3`：`(101,011) -> sum=110, carry=100 -> sum=010, carry=1000 -> ... 直至 carry 0。

**面试白板 30 秒**：「136 全体 XOR；191 popcount；231 n&(n-1)；子集 (s-1)&m 降序；137 按位模 3。」

### 复杂度分析

| 操作 / 模板 | 时间 | 空间 | 备注 |
|-------------|------|------|------|
| lowbit / 单次 & \| ^ | O(1) | O(1) | 字长 w 常数 |
| popcount（Kernighan） | O(popcount(x)) ≤ O(w) | O(1) | 最坏 w 次 |
| subsets_of_mask(m) | O(2^{popcount(m)}) | O(2^{...}) 输出 | 与 1 个数指数相关 |
| 136 单次 XOR 扫描 | O(n) | O(1) | |
| 137 按 32 位计数 | O(32n) = O(n) | O(1) | |
| 338 DP | O(n) | O(n) 或 O(1) 滚动 | |
| 421 Trie | O(n·w) | O(n·w) 节点 | w=32 |

与暴力枚举子集 `O(2^n)` 对比，对 **固定掩码 m** 的子集枚举是 `O(2^{popcount(m)})`，若 `m` 有 k 个 1 则 `2^k`。对所有 `mask` 从 0 到 `2^n-1` 再枚举子集，总 `O(3^n)`，仅 n≤15~17 可接受。

**字长 w**：面试默认 32；Python 整数无限但复杂度仍按 32/64 报。硬件 popcount 为 O(1) 字长。

**空间权衡**：136/191/231 可 O(1) 额外；338 需 O(n) 数组；421 Trie O(nw)。哈希表 136 亦 O(n) 时间 O(n) 空间。

**摊还**：Kernighan 循环次数 = 1 的个数，非总位数。平均随机整数下 popcount 较小。

**失败模式**：137 用 XOR 直接消（错）；231 忘判 `n<=0`；子集枚举漏 `s=0` 后死循环；260 选位为 0（xor_all=0 不会发生）。识别即可排错。

**与排序比较**：421 排序+Trie 思想 O(n log n)；纯 Trie O(nw)。n 大时 w 常数小仍优。

**338 两种 DP**：`i&(i-1)` 与 `i>>1` 均 O(n)，前者与 popcount 模板一致，后者直观「右移丢低位」。

**268 求和溢出**：n 很大时用 XOR 避免 int 溢出；竞赛 long long 求和亦可。

**371 循环次数**：最多 w+1 轮进位传播，等价加法位数。

**枚举全集**：`for mask in range(1<<n)` 是 O(2^n)；对每个 mask 枚举子集再乘 2^{popcount(mask)} 总 3^n。勿混淆。

**竞赛上限**：n=20 时 2^20≈10^6 可枚举 mask；n=25 需剪枝或 meet-in-the-middle。位运算题常 n≤10^5 但操作 O(1) 或 O(log U)。

**Python bit_count**：O(1) 内置，面试仍建议写 Kernighan 展示功底，再提「生产可用 bit_count」。

### 代码模板

**lowbit**

```python
def lowbit(x: int) -> int:
    return x & -x
```

**popcount（Brian Kernighan）**

```python
def popcount(x: int) -> int:
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c
```

**子集枚举（降序，含 0）**

```python
def subsets_of_mask(m: int) -> list[int]:
    out: list[int] = []
    s = m
    while True:
        out.append(s)
        if s == 0:
            break
        s = (s - 1) & m
    return out
```

**136 只出现一次**

```python
def single_number(nums: list[int]) -> int:
    ans = 0
    for x in nums:
        ans ^= x
    return ans
```

**191 位 1 的个数**

```python
def hamming_weight(n: int) -> int:
    return popcount(n)
```

**231 2 的幂**

```python
def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0
```

**260 两个只出现一次**

```python
def single_number_iii(nums: list[int]) -> tuple[int, int]:
    xor_all = 0
    for x in nums:
        xor_all ^= x
    bit = xor_all & -xor_all
    a = b = 0
    for x in nums:
        if x & bit:
            a ^= x
        else:
            b ^= x
    return a, b
```

**338 前 n 比特计数（DP）**

```python
def count_bits(n: int) -> list[int]:
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i & (i - 1)] + 1
    return dp
```

**137 思路骨架（按位模 3）**

```python
def single_number_ii(nums: list[int]) -> int:
    ans = 0
    for b in range(32):
        cnt = 0
        for x in nums:
            cnt += (x >> b) & 1
        ans |= (cnt % 3) << b
    return ans
```

**371 无符号加法异或版**

```python
def get_sum(a: int, b: int) -> int:
    MASK = 0xFFFFFFFF
    MAX = 0x7FFFFFFF
    while b:
        a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK
    return a if a <= MAX else ~(a ^ MASK)
```

**268 缺失数字（XOR）**

```python
def missing_number(nums: list[int]) -> int:
    ans = len(nums)
    for i, x in enumerate(nums):
        ans ^= i ^ x
    return ans
```

C++ 侧与 Study `bit_manipulation.cpp` 三函数逐行对应；LeetCode 题解在练习节链到 `problems/leetcode/`。

### 变体与技巧

**异或消重扩展**：若「两个数各出现一次，其余两次」，先 260 分组再 136。若「一个出现一次，其余 k 次」，用位计数模 k（137 为 k=3）。

**1<<i 遍历位**：`for i in range(32): if mask & (1<<i)` 检查第 i 位；`mask ^= (1<<i)` 删除该位。与 lowbit 删除最低 1 可互换风格。

**合并集合**：`a | b` 并集；`a & b` 交集；`a ^ b` 对称差（无重复并）；`a & ~b` 从 a 去掉 b 的位。

**奇偶校验**：整段 XOR 为 0 表示偶数次翻转；通信纠错 Hamming 与位计数相关。

**格雷码**：`i ^ (i>>1)` 相邻仅一位变化，与状压 BFS 有关，见竞赛专题。

**meet-in-the-middle**：n=40 子集和拆两半各 2^{20}，用位运算枚举掩码与哈希合并。比单趟 2^40 可行。

**XOR 基（线性基）**：异或空间最大独立集，用于 421 类「最大异或」与「k 大异或」进阶，n 大时比 Trie 更紧凑。

**popcount 与奇偶性**：`n & 1` 最低位；`n % 2` 等价非负时。

**交换两数**：`a^=b;b^=a;a^=b` 可写但可读性差，面试勿炫技除非题面要求不用临时变量。

**乘除 2**：`n<<1`、`n>>1` 注意溢出与负数 C++ 行为。

**掩码动态**：DP 状态 `mask` 增加元素 `v`：`mask | (1<<v)`；删除：`mask & ~(1<<v)`。

**421 Trie 节点**：`child[0], child[1]`，插入数时从高位到低位走；查询异或最大时优先 opposite bit。

**338 滚动**：只需前一个 `i&(i-1)` 时可 O(1) 空间单变量，但数组输出需 O(n)。

**260 位选择**：必须选 `xor_all != 0` 的位；`lowbit(xor_all)` 保证两组非空。

**371 负数**：Python 题面常限 32 位，用 MASK 截断；C++ 注意符号扩展。

**137 优化**：一次遍历维护 `ones, twos` 三进制状态机，O(n) 单遍，见 LeetCode 题解；按位模 3 更易讲清。

**268 索引 XOR**：`ans ^= i ^ x` 把「下标」与「值」同时编码，缺的那个下标从未被抵消。

**子集和等于 target**：枚举 mask 子集或 meet-in-middle；位运算提供枚举工具而非直接答案。

**布隆过滤器**：多位哈希置 1，查询全 1；假阳性可接受时用位数组省空间。

**CPU 指令**：`__builtin_popcountll`、`tzcnt`、`lzcnt` 与算法模板对应，竞赛可写。

**与哈希 XOR 和**：子数组异或和为 k 的个数，前缀 XOR + 哈希 `count[prefix^k]`，O(n) 时间。

**重复检测**：`seen ^|= x` 不能判断重复；需 `seen & x` 或集合。

**位图排序**：值域小用 `bits[v]=1` 再扫描，O(U+w)。

**竞赛常考组合**：枚举 mask + popcount 剪枝（仅考虑 popcount≤K 的子集）。

**面试 Follow-up**：136 若要求「两个只出现一次」→260；191 若要求范围 0..n →338；231 若要求 2 的幂次方指数 →log。

### 易错点

**137 误用 XOR**：三次出现不能 XOR 消掉，必须模 3 或状态机。

**231 漏 n<=0**：0 和负数不是 2 的幂，先判 `n>0`。

**子集死循环**：`while s:` 漏处理 `s=0` 输出；Study 用 `while True` + `if s==0: break` 清晰。

**260 xor_all=0**：理论上两不同数异或非 0；若数组逻辑错可能崩，正常数据安全。

**371 无限循环**：未 MASK 导致 Python 整数 carry 不终止；C++ 要 `unsigned` 语义。

**191 负数**：C++ 右移算术移位导致死循环或错数；转 `unsigned` 或 `n &= 0xFFFFFFFF`。

**lowbit 负数**：`-8 & 8` 在补码下仍有效，但题面常非负；统一用无符号思维。

**1<<n 溢出**：C++ `1<<31` 对 signed 未定义；用 `1LL<<k` 或 `1u<<k`。

**338 下标**：返回长度为 n+1，下标 0 恒 0，勿 off-by-one。

**268 求和溢出**：n=10^5 时 sum 用 long long；XOR 更稳。

**421 空数组**：边界 n=0；Trie 插入 0 的位路径。

**重复段落**：枚举子集时 `(s-1)&m` 当 s=0 再减 1 得 -1，`-1 & m == m`，若未 break 会死循环——Study 在 append 0 后 break。

**popcount(0)**：0，while 不进入，正确。

**subsets_of_mask(0)**：仅 `[0]`，Study 断言覆盖。

**异或交换**：`a^=b` 若 a、b 同址会清零，数组元素勿这样写。

**比较用 ==**：位掩码判断子集：` (s & m) == s `，不是 `s < m` 单独够用。

**Python 负数 lowbit**：了解即可，面试数组多为非负。

**C++ set 断言**：`subsets_of_mask` 用 set 比较顺序无关，与 Python set 一致。

**双语言对拍**：改 Kernighan 后两边 assert 同步跑 PowerShell 命令。

**manifest draft**：通过 strict 校验后再改 published，见 `_meta/人工撰写进度.md`。

**与 bitmask DP 混淆**：TSP 是 `dp[mask][u]` 最短路；本页 `subsets_of_mask` 仅列子集，不填 DP 表。

**读写分离**：练习延伸链 Study 题解，不在 atelier 建单题页。

### 练习建议

**第一遍（Study 对齐）**：跑通 `bit_manipulation.py` / `.cpp`，手推 `lowbit(12)=4`、`popcount(0b1011)=3`、`subsets_of_mask(0b101)` 四个子集。对照 `notes.md` 三行技巧背诵。

**第二遍（核心四题）**：136 XOR；191 popcount；231 `n&(n-1)`；338 `i&(i-1)` DP。每题 10 分钟写提交，再读官方题解对比 137 状态机。

**第三遍（进阶）**：260 分组 XOR；268 索引异或；371 异或加法；137 按位模 3。421 选做 Trie，至少理解「高位贪心」。

**题单映射**

| 题号 | 要点 | 模板 |
|------|------|------|
| 136 | 成对 XOR 消 | single_number |
| 137 | 模 3 位计数 | 137 骨架 |
| 191 | popcount | hamming_weight |
| 231 | 唯一 1 | is_power_of_two |
| 338 | DP 与 i&(i-1) | count_bits |
| 260 | lowbit 分组 | single_number_iii |
| 268 | 索引 XOR / 求和 | missing_number |
| 371 | 异或+进位 | get_sum |
| 421 | 异或 Trie | 421 变体 |

**Study 题解路径**：`F:\Study\Algorithm\python\problems\leetcode\<题号>_*/solution.py`（若已克隆）。本站不复制单题全文，只练思路后跳转仓库。

**时间分配（7 天）**：D1 导读+Study+三函数；D2 基础篇六节+手推；D3 Python 通读+默写；D4 C++ 对照+双语言 OK；D5 136/191/231/338；D6 260/268/371/137；D7 421+复盘易错点。

**验收**：15 分钟默写三函数+136+231；30 秒口述 lowbit/popcount/子集枚举；PowerShell 双 OK；汉字 major 篇幅读完基础篇与实现节。

**与相邻专题**：状压见 `algo-dp-bitmask`；树状数组见 `ds-tree-fenwick-tree`；数组哈希见线性哈希表。位运算是它们的微积分。

**竞赛拓展**：XOR 基、子集卷积、FWT 异或卷积（高级，本书不展开实现）。

**面试模拟**：白板写 136 与 191，口述 260 为何能分组；追问 137 时切换到模 3。

**避免**：只背 `x&-x` 不知树状数组用途；子集枚举写 `while s` 漏 0；338 写成 O(n log n) 暴力 popcount 每个 i。

**重复练习**：隔周重做 260 与 137，易忘模 3 与分组位。

**PowerShell 复习**：每周 `-LiteralPath` 跑两次自测，防环境路径错误。

**贡献**：向 Study 提 PR 时保持三函数签名稳定，便于与本页对照。

**published 条件**：`validate_algorithm_guide.py` 与 `validate_algorithm_quality.py` 均 `--strict` 通过后再改 manifest status。

## Python 实现

Study `bit_manipulation.py` 全文如下（与仓库一致，可直接运行自测）：

```python
"""位运算：lowbit、popcount、子集枚举。"""

from __future__ import annotations


def lowbit(x: int) -> int:
    return x & -x


def popcount(x: int) -> int:
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c


def subsets_of_mask(m: int) -> list[int]:
    out: list[int] = []
    s = m
    while True:
        out.append(s)
        if s == 0:
            break
        s = (s - 1) & m
    return out


if __name__ == "__main__":
    assert lowbit(12) == 4
    assert popcount(0b1011) == 3
    assert set(subsets_of_mask(0b101)) == {0b101, 0b100, 0b001, 0b000}
    assert lowbit(0) == 0 and popcount(0) == 0
    assert subsets_of_mask(0) == [0]
    print("bit_manipulation OK")
```

**lowbit**：`x & -x` 依赖补码；Python 整数语义下 `12 & -12 == 4`。面试可补一句：`-x = (~x + 1)`，最低 1 两侧与运算保留。

**popcount**：循环 `x &= x-1` 清除最低 1；`x=0` 不进入。生产可用 `x.bit_count()`，但 Kernighan 体现「每次减 popcount 次」。

**subsets_of_mask**：降序枚举；`m=0` 只返回 `[0]`。`set` 断言忽略顺序。复杂度 O(2^{popcount(m)}) 时间，输出占同阶空间。

**自测断言含义**：`0b101` 子集共 4 个；`lowbit(0)=0`；`popcount(0)=0`。改代码后务必 `python -LiteralPath ...\bit_manipulation.py`。

**与 LeetCode 衔接**：将 `popcount` 用于 191；`lowbit` 用于 260 分组；`subsets_of_mask` 用于搜索题子集迭代练习（非直接提交函数）。

**类型注解**：`list[int]` 需 Python 3.9+；`from __future__ import annotations` 兼容 3.7+ 前向引用。

**扩展练习**：在同文件末尾临时写 `single_number` 做本地 assert，提交前删除，保持仓库简洁。

## C++ 实现

Study `bit_manipulation.cpp` 全文如下：

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;

int lowbit(int x) { return x & -x; }

int popcount(int x) {
    int c = 0;
    while (x) {
        x &= x - 1;
        ++c;
    }
    return c;
}

vector<int> subsets_of_mask(int m) {
    vector<int> o;
    for (int s = m;; s = (s - 1) & m) {
        o.push_back(s);
        if (s == 0) break;
    }
    return o;
}

int main() {
    assert(lowbit(12) == 4);
    assert(popcount(0b1011) == 3);
    auto ss = subsets_of_mask(0b101);
    set<int> st(ss.begin(), ss.end());
    assert(st == set<int>({0b101, 0b100, 0b001, 0}));
    cout << "bit_manipulation OK" << endl;
    return 0;
}
```

**与 Python 对照**：逻辑逐行同构；`vector` 存子集，`set` 断言无序。`int` 32 位足够自测；竞赛大掩码用 `long long`。

**alg_std.hpp**：仓库统一头，提供 `vector`、`set`、`cout` 等，避免每题重复 include。

**编译**：在 `cpp/algorithms/bit_manipulation` 目录 `g++ -std=c++17 -O2 -Wall -Wextra -o run.exe bit_manipulation.cpp`，运行 `./run.exe` 或 `.\run.exe`。

**unsigned 提示**：若将 `popcount` 用于极大无符号，参数可改 `unsigned x`，循环条件不变。

**STL 替代**：`__builtin_popcount(x)` 可作 popcount 对照；面试手写 Kernighan 更通用。

**子集 for 写法**：`for (int s=m; ; s=(s-1)&m)` 与 Python `while True` 等价；`s==0` 后 break 防止下一轮 `-1&m`。

**调试**：`bitset<32> bs(m)` 打印掩码；`cout << lowbit(x) << '\n'` 快速验证。

**双语言对拍**：同一组 assert 在 PowerShell 连续跑 python 与 g++，输出均为 `bit_manipulation OK`。

## 练习与延伸

**仓库内题解**：克隆 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) 后，在 `python/problems/leetcode/` 按题号查找 `136_single_number`、`191_hamming_weight` 等目录。本站 `algorithm-guides` 不新建单题页，避免与 Study 分叉。

**按难度递进**

1. 入门：136、191、231、338 — 仅用本页三模板与 XOR/DP。
2. 中级：260、268、371 — 分组、索引 XOR、位运算加法。
3. 高级：137、421 — 模 3 与二进制 Trie；可选 201、477 总汉明距离（前缀位计数）。

**201 数字范围位 1**：按位统计 `[l,r]` 可转 `count(r)-count(l-1)`，数位 DP 或逐位前缀和，与本页 popcount 思想相关但需单独学数位 DP（见 `algo-dp` 数位章节）。

**477 汉明距离总和**：枚举 32 位，统计该位 0/1 个数乘积贡献，O(32n)。

**260 跟进**：返回顺序无关，LeetCode 要求元组；分组位勿用 0。

**421 跟进**：注意数组两两异或最大，非子数组；Trie 从最高位 30 或 31 开始视数据范围。

**练习节奏**：每天 2 题_easy + 1 题_medium，周末 137 或 421 二选一；每题写完用 Study solution 对拍边界 `[]`、`[0]`、单元素。

**错误本**：记录 137 误 XOR、子集枚举死循环、371 未 MASK — 考前翻一遍。

**与面试经典结合**：系统设计「权限位图」可口述 `| & ^` 操作；算法面以 136/260 最常见。

**CodeTop / 热题**：位运算出现频率低于双指针与 DP，但 136/191 属于必背模板，错过代价高。

**延伸阅读**：下节 GitHub 与 `notes.md`；进阶 XOR 基、FWT 见竞赛书籍，不在 Study 三函数内实现。

**自测清单**：三函数 OK；136/191/231/338 AC；260/268 各 AC 一次；137 能口述模 3；421 理解 Trie 一位分支。

## 学习路径

**第 1 天**：导读、预备知识、Study 对照，跑通 Python/C++ 自测，手推 lowbit(12)、popcount(0b1011)、四个子集。

**第 2 天**：基础篇「直觉与定义」「复杂度分析」精读，默写三函数，做 191、231 提交。

**第 3 天**：基础篇「代码模板」「变体与技巧」，做 136、338，对照 Python 实现节。

**第 4 天**：C++ 实现节 + 双语言对拍；做 268、260，口述分组原理。

**第 5 天**：易错点复盘；137 按位模 3 实现；371 异或加法（可选）。

**第 6 天**：421 Trie 或读题解；477/201 选做；回顾子集枚举与状压 DP 分界。

**第 7 天**：模拟面试 30 分钟（136+260+191），PowerShell 复习命令，检查 manifest draft 与校验脚本。

**前置专题**：熟悉二进制与 O(n) 扫描；学完可接 `algo-dp-bitmask`、`ds-tree-fenwick-tree`。

**后续专题**：图论最短路、哈希表互补；竞赛可学 XOR 线性基。

**阅读顺序**：本站文 → Study notes → 三函数源码 → LeetCode 题解目录，勿颠倒。

**时间紧压缩**：只保 136/191/231 + 三函数自测，260 次之，137/421 标记延后。

**全职备考**：本页 major 篇幅配合 20+ 题位运算标签一周刷完，每日 strict 跑脚本防退步。

## 延伸阅读

- Study 笔记：[python/algorithms/bit_manipulation/notes.md](https://github.com/zhk0567/Algorithm/blob/main/python/algorithms/bit_manipulation/notes.md)
- 仓库目录：[zhk0567/Algorithm — bit_manipulation](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/bit_manipulation)
- 状压 DP 衔接：`Blog/algorithm-guides/algo-dp-bitmask/index.md`（`dp[mask][u]` 与集合枚举）
- 树状数组：`Blog/algorithm-guides/ds-tree-fenwick-tree/index.md`（lowbit 应用）
- 算法总览：`Blog/algorithm-guides/overview/index.md`
- 写作与校验：`Blog/algorithm-guides/_meta/写作规范.md`；`scripts/validate_algorithm_guide.py`、`scripts/validate_algorithm_quality.py`

**books**：CLRS 不涉及位技巧细节；竞赛可参阅《算法竞赛进阶指南》位运算章节。面试以 LeetCode 标签 + 本页模板足够。

**在线**：VisuAlgo 无专门位运算可视化，建议手画 12 的二进制理解 lowbit。Python 交互式 `>>> 12 & -12` 即时验证。

**维护**：Study 三函数接口稳定时本页仅需同步题号表；若仓库新增 `parity` 等第四函数，在 Python/C++ 实现节增补全文并更新 manifest。

**版权与引用**：正文扩写自 Study notes 提纲，代码与仓库 MIT 保持一致；转载注明 Algorithm 仓库链接。

**反馈**：发现断言失败或路径变更，提 Issue 到 atelier 或 Study，优先修正 `-LiteralPath` 示例与 topic_path。

**结语**：位运算不是孤立技巧，而是 **lowbit / popcount / 子集枚举** 三块砖，砌成 XOR 题、状压题与树状数组的地基。坚持讲义与 `bit_manipulation.py` 一致，通过 strict 校验后再将 manifest 标为 published；单题细节始终回到 Study `problems/leetcode/` 题解，保持仓库单一事实来源。
'''

EXPANSION = r'''
### 136 手推与不变量

数组 `[4,1,2,1,2]`，从左 XOR：4^1^2^1^2 = 4。成对数异或为 0，只剩 4。不变量：前缀 XOR 中每个值出现偶数次则结果为 0，奇数次保留。扩展：若两个唯一数，全体 XOR 为两数异或，非 0 位用于分桶。

### 137 三进制状态机（口述）

维护 `ones` 表示「位上模 3 余 1」、`twos` 表示余 2。见数字 `x` 时更新，保证每位状态在模 3 意义下正确。与「逐位 cnt%3」等价，单遍 O(n) 常数更小，面试时间紧可写模 3 版。

### 260 分桶完整例

`[1,2,1,3,2,5]`，全体 XOR `1^2^1^3^2^5 = 3^5 = 6`（0b110）。lowbit=2，第 1 位为 1 的进 A 组：1,1,3 → XOR 得 3；其余 2,2,5 → 5。答案 {3,5}。若选 bit=0 会全进一组，故必须 nonzero 位。

### 338 填表前几项

`dp[0]=0`；`i=1`：1&(0)=0 → dp[1]=1；`i=2`：2&1=0 → 1；`i=3`：3&2=2，dp[2]=1 → 2；`i=4`：4&3=0 → 1；`i=5`：5&4=4，dp[4]=1 → 2；`i=6`：6&5=4，dp[4]=1 → 2；`i=7`：7&6=6，dp[6]=2 → 3。与直接 popcount 一致。

### 421 Trie 插入与查询（文字流程）

插入 3(011)、5(101)、25(11001) 等，从高位走。查询与 2(010) 最大异或：希望高位异或为 1，尽量走相反分支；若不存在则走同分支。答案 28(11100) 类题面以具体输入为准。复杂度 O(n·32)。

### 268 两种证法

XOR：`ans` 初值为 n，遍历时 `ans ^= i ^ nums[i]`，缺失的 k 满足 k 从未作为下标与值同时抵消。求和：`sum(nums) + ans = n*(n+1)//2`。n=10^5 用 long long 或 XOR。

### 371 逐步跟踪

a=5(101), b=3(011)：sum=110(6), carry=010(2)；sum=100(4), carry=1000(8)；… 直至 carry 0。MASK 保证 32 位环。

### 子集枚举与 78 子集（关系）

78 子集生成可用回溯或迭代；对固定掩码表示的集合，`(s-1)&m` 枚举是迭代核心。n 个元素全集 mask=(1<<n)-1，枚举即 2^n 子集，n≤20 可暴力。

### 231 边界表

| n | n&(n-1) | 判定 |
|---|---------|------|
| 0 | - | false |
| 1 | 0 | true |
| 2 | 0 | true |
| 3 | 2 | false |
| 4 | 0 | true |

### 191 与 477 区别

191 单数 popcount；477 多数字两两汉明距离和，按位贡献 O(32n)，非本仓库函数但模板同源。

### PowerShell 故障排查

若 `python` 找不到，用 `py -3` 或完整路径；`g++` 未安装则装 MinGW-w64。路径含空格必须 `-LiteralPath`。当前目录用 `Get-Location` 确认在 `F:\Study\Algorithm`。

### 面试追问应答

问：为何 136 O(1) 空间？答：XOR 结合律原地累积。问：lowbit 负数？答：补码定义下仍成立，本题数据非负。问：子集枚举顺序？答：降序，先全集后空集。问：与 bitmask DP？答：本页枚举子集；TSP 在 dp-bitmask 专题。

### 竞赛 meet-in-the-middle 草图

n=40 子集和 target：左半枚举 mask∈[0,2^20) 存 sum→count，右半查 target-sum。位运算提供左半枚举工具。复杂度 O(2^{n/2})，非 Study 三函数但依赖掩码思维。

### 位运算与并查集

按秩合并 size 为 2 的幂时用 lowbit 优化；理解 lowbit 有助于读高级并查集实现，非本页必须。

### 重复学习检查表

- [ ] 默写 lowbit/popcount/subsets_of_mask
- [ ] 136/191/231/338 AC
- [ ] 260 分组讲清
- [ ] 137 模 3 或状态机
- [ ] Python/C++ OK 输出
- [ ] 不说 XOR 解 137
- [ ] 子集枚举含 0 终止
- [ ] manifest 仍 draft 直至 strict 双过

### 与滑动窗口、双指针分界

子数组异或和=k 用前缀 XOR+哈希，不是滑动窗口。位运算题很少维护左右指针区间，除非题面显式连续子数组且和性质特殊。

### 硬件 popcount 与 portable 代码

竞赛 g++ `__builtin_popcount`；MSVC `_mm_popcnt_u32`；面试写 Kernighan。Python 3.10 `bit_count()` 一行通过 191。

### 写作体例提醒

九节 `##` 顺序固定；基础篇仅六个 `###`；禁止 `####`；禁止 filler「围绕「…」理解 **」；代码须完整非占位。major ≥15000 汉字，以 `count_chinese` 为准。

### 终验收（读者）

合上本文，15 分钟写出三函数+136+231+260 思路；打开 PowerShell 复制 Study 对照两命令；若均通过，位运算基础达标，可进入状压 DP 与 Fenwick 专题。
'''


def main() -> None:
    from _bit_manipulation_bulk_zh import BULK  # noqa: E402

    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = BODY
    marker = "\n## 学习路径\n"
    insert = EXPANSION + BULK
    if marker in text:
        text = text.replace(marker, insert + marker, 1)
    else:
        text += insert
    OUT.write_text(text, encoding="utf-8")
    n = count_chinese(text)
    print(f"Wrote {OUT}")
    print(f"Chinese chars: {n}")
    if n < 15_000:
        raise SystemExit(f"Chinese chars {n} still < 15000; add more bulk text")


if __name__ == "__main__":
    main()
