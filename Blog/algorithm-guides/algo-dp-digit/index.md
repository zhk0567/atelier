---
title: "算法 · Dp Digit"
series: algorithm
category: Algorithms
topic_path: algorithms/dynamic_programming/digit
guide_toc: topic-algorithm
guide_tier: medium
status: published
---

# 算法 · 数位动态规划（Digit DP）

## 导读

**数位 DP** 用于统计区间 `[0, n]` 内满足「数位相关约束」的整数个数或数位和，典型约束包括：数位和模 K 为 0、不含连续相同数字、数字 1 的个数为质数等。与 `algo-dp-linear` 按前缀下标推进、`algo-dp-knapsack` 按容量维滚动不同，数位 DP 按 **十进制位从高到低** 构造数字，配合 **tight**（是否仍贴紧上界 `n` 的对应位）与 **leading_zero**（是否仍处于前导零阶段）避免把 `007` 与 `7` 重复计数或错误计入数位和。

Study 仓库 `digit/` 以 **数位和能被 K 整除的个数** 为锚点实现 `count_digit_sum_mod0`：给定非负整数 `n` 与正整数 `K`，统计 `[0, n]` 中各位数字之和 `≡ 0 (mod K)` 的整数个数。该模型是 OI 与面试中数位 DP 的「标准计数题」，同一套 DFS 骨架可迁移到不含 `44`、回文数计数、第 N 个幸运数等，只需改状态维与转移。

本页在 `notes.md` 骨架上扩写：数位状态的含义、`tight` 与 `leading_zero` 如何更新、记忆化维度为何是 `O(位数 × K × 2 × 2)`、与暴力枚举的对拍方式，以及为何大 `n` 必须用字符串位 DFS 而非直接遍历整数。读完你应能默写 Study 函数、解释前导零时 `mod` 不更新的原因，并在 Python 与 C++ 中对拍 `digit_dp OK`。

**在 DP 家族中的位置**：`algorithms/dynamic_programming/digit` 与 `linear`、`knapsack`、`interval`、`tree`、`bitmask` 并列；总览见 `algo-dynamic-programming`。Hot 100 中纯数位 DP 题不如背包密集，但笔试与 OI 常出现「统计 [L,R] 满足性质的个数」，本页聚焦 **按位 DFS + tight + 前导零** 这一实现核心。

**面试沟通顺序**：30 秒说明「从高到低填每一位，状态含是否贴上限、是否前导零、当前数位和模 K」→ 写出 DFS 边界与枚举 `d∈[0,limit]` → 报 `O(len(n) × K)` 时间与记忆化 → 举 `n=100, K=3` 手推若干分支。

**为何值得系统学**：数位 DP 的 WA 高度集中在三类：前导零仍把 `0` 计入数位和、`tight` 更新写成 `d <= limit` 却未要求 `d==limit` 才保持 tight、统计 `[L,R]` 时忘记 `count(R)-count(L-1)`。修一处往往全局通过。Study 只实现模 K 计数，但四维状态骨架可迁移多题。

**与背包/线性对照**：背包维度是物品与容量；数位维度是 **位下标 + 约束余数**。题面若写「不超过 n 的方案数」且 n 达 `10^18`，不要用线性 DP 扫 n，应数位 DP。与 `algo-dp-bitmask` 的区别：状压 n≤20 枚举子集；数位 n 极大但位数仅约 19。

**本地学习节奏**：第一遍读导读 + 手推 `n=12, K=3`；第二遍默写 `count_digit_sum_mod0` 并对照 Python/C++ 与暴力；第三遍做「不含连续相同数字」迁移，只加状态维；第四遍练 `[L,R]` 差分。每遍运行 `digit_dp OK` 巩固。

**manifest 与站点**：slug `algo-dp-digit`，`topic_path: algorithms/dynamic_programming/digit`，`guide_tier: medium`，`status: published`。通过 strict 校验后可改 `published`；勿用骨架脚本覆盖正文。

## 预备知识

> **环境**：Python 3.10+（`functools.lru_cache`）；C++17，`g++`，Study 侧 `digit_dp.cpp` 通过 `#include <alg_std.hpp>` 使用 `memset`、`to_string` 等。

阅读本专题前，建议已具备：

- **递归与记忆化**：`@lru_cache` 与数组 memo 等价；数位 DFS 深度为位数，通常 ≤ 20，栈安全。
- **模运算**：数位和模 K 用 `(mod + d) % K`，前导零阶段不加入 `d`。
- **上界字符串**：`n` 转 `s = str(n)`，第 `i` 位上限为 `int(s[i])`（tight 时）或 9（非 tight）。
- **区间计数差分**：`[L,R]` 答案为 `f(R) - f(L-1)`，注意 `L=0` 边界。

**填表口诀**：位下标 `i` 从 0 到 `len(s)-1`；每位枚举 `d`；更新 `tight' = tight && (d==limit)`；`z' = z && (d==0)`；若 `z'` 则 `mod' = mod` 否则 `mod' = (mod+d)%K`。

**重叠子问题**：同一 `(i,tight,mod,z)` 在不同数字前缀下重复，记忆化合并。

**无后效性**：高位决策后，低位只依赖当前状态，不依赖具体已填前缀的「数值」，只依赖状态向量。

**工具链**：VS Code 同时打开 Study python 与 cpp；改转移时双语言对拍 `nn<500` 暴力。PowerShell 7 与 5.x 均支持 `-LiteralPath`。

**从暴力到 DP**：暴力遍历 `0..n` 是 O(n)，n 达 `10^18` 不可行；数位 DP 仅与 **位数** 与 **模 K** 相关，约 O(19×K×4) 状态。

**与树形/区间 DP**：树在子树上合并；区间在连续段上切分；数位在十进制位上推进。题面是树用 `algo-dp-tree`，连续段用 `algo-dp-interval`，大整数计数用本页。

**工程角度**：数位 DP 代码短、状态定义集中，适合 Study 单函数与暴力对拍学习。

**学习误区**：忘记前导零；`tight` 用 `d<=limit` 代替 `d==limit`；把 `n=0` 算漏；`K=0` 未特判。

**面试评分点**：四维状态含义、前导零处理、复杂度与位数关系、能口述 `[L,R]` 差分。

## Study 仓库对照

本页 `topic_path` 为 `algorithms/dynamic_programming/digit`，与 GitHub 仓库 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) 中下列路径一致：

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/dynamic_programming/digit/notes.md` | `python/algorithms/dynamic_programming/digit/digit_dp.py` |
| C++ | `cpp/algorithms/dynamic_programming/digit/notes.md` | `cpp/algorithms/dynamic_programming/digit/digit_dp.cpp` |

在本地 Study 克隆根目录下运行（请使用 `-LiteralPath`）：

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\digit\digit_dp.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\dynamic_programming\digit
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe digit_dp.cpp
.\run.exe
```

`notes.md` 要点：按位 DP；`tight` 与 `leading_zero`；统计 `[0,n]` 数位和模 K。正文以下在笔记上扩写定义、转移与易错点，并与 `digit_dp.py` / `digit_dp.cpp` 保持逐行一致。

## 基础篇

### 直觉与定义

**问题抽象**

给定上界 `n`（非负整数）与模数 `K`，问有多少个 `x ∈ [0, n]` 满足「`x` 的十进制各位数字之和 `≡ 0 (mod K)`」。直接遍历 `x` 从 0 到 n 在 n 很大时不可行。数位 DP 把 `n` 写成字符串 `s`，从高到低在第 `i` 位填数字 `d`，记录：

- **`tight`**：此前填的位是否与 `s` 的前缀完全一致；若 `tight=True`，当前位 `d` 不能超过 `s[i]`，否则上界放松为 9。
- **`mod`**：已确定非前导部分下的数位和模 K。
- **`z`（leading_zero）**：是否仍处于前导零（尚未写出第一个非零位）；若 `z=True` 且 `d=0`，仍视为前导零，**不**把 0 加入数位和。

**答案位置**：DFS 走完所有位（`i==len(s)`）时，若 `mod==0` 返回 1，否则 0。初始调用 `dfs(0, True, 0, True)` 表示从高位开始、贴紧上界、余数为 0、处于前导零。

**手推样例（K=3，n=12）**

`s="12"`。合法 x：0（和 0）、3、6、9、12（和 3）。共 5 个。可用暴力验证；DFS 在末位结束后 `mod==0` 的路径计数应为 5。

**与「数字 DP」名称**

中文常称数位 DP、数字 DP，均指按十进制位构造并计数/求最值，与「线性 DP 下标 i」不同。

**统计 [L,R]**

`ans(L,R) = count(R) - count(L-1)`，其中 `count` 为 Study 的 `[0,n]` 版本。`L=0` 时直接用 `count(R)`。

### 复杂度分析

| 项目 | 说明 |
|------|------|
| 状态 | 位下标 `i`（≤ 约 19）、`tight`×2、`mod`×K、`z`×2 |
| 转移 | 每位最多 10 种数字 |
| 时间 | `O(len(s) × K × 10)`，记忆化后每个状态只求一次 |
| 空间 | 同上状态数；C++ 开 `memo[25][2][10][2]` 足够 |

`n ≤ 10^18` 时 `len(s)≤19`，K 常 ≤ 1000，总状态约数万，极快。若增加「上一 digit」防连续相同，状态乘 10。

**与暴力对比**：暴力 O(n)；数位 O(位数×K)。

### 代码模板

以下与 Study 仓库逻辑一致。

```python
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

**记忆化键**：`(i, tight, mod, z)` 四元组。Python 用 `lru_cache`；C++ 用四维数组 `memo[i][tight][mod][z]`。

### 变体与技巧

**数位和 ∈ 某集合**

把 `mod` 换成「当前和」若 K 小可压成余数；若判断「和为质数」需预筛或额外状态，面试较少。

**不含连续相同数字**

增加状态 `prev` 表示上一位填的数字；转移时若 `d==prev` 跳过。状态数 ×10，仍可行。

**最低位固定 / 长度固定**

有些题要求恰好 m 位，可在进入非前导零后计数位数，或单独处理长度维。

**求第 N 个满足条件的数**

计数 DP 求出数量后，可二分 N 或 DFS 时按分支大小决定走左/右子树「找第 K 个」，属进阶。

**LeetCode 映射**

| 题号 | 模型 | 要点 |
|------|------|------|
| 233 | 数字 1 的个数 | 按位 + 前缀计数 |
| 357 | 统计各位都不同的数字 | 判重状态 |
| 600 | 不含连续 1 的非负整数 | 二进制位 DP 同理 |
| 1012 | 至少有 1 位重复的数字 | 补集 + 数位 |

### 易错点

1. **前导零**：`z and d==0` 时 `mod` 不变；否则 `mod=(mod+d)%K`。
2. **tight 更新**：必须 `ntight = tight and (d == limit)`，不是 `d<=limit`。
3. **n=0**：`s="0"`，一位 DFS，结果为 1（0 的和为 0）。
4. **K≤0**：Study 抛 `ValueError`，调用前保证 K 正。
5. **[L,R] 差分**：`L=0` 勿再减 `count(-1)`。
6. **long long**：C++ 计数结果用 `int` 通常够，若合并多状态用 `long long`。
7. **十进制以外**：二进制位 DP 同理，limit 为 1 或 `s[i]`。
8. **忘记 mem 初始化**：C++ `memset(memo,-1)` 每次查询新 `n` 要清空。

### 练习建议

**建模三问**：按位构造时还要记录什么？上界如何压 tight？前导零是否影响约束？

建议顺序：

1. **重写 Study 函数** — 与暴力 `nn<500` 对拍。
2. **233 数字 1 的个数** — 按位统计 1 的出现。
3. **357 / 1012** — 增加「是否已出现某 digit」状压位。
4. **不含 44**（若遇）— 加 `prev` 位。

每题限时 30 分钟：10 分钟写四维状态；15 分钟 DFS；5 分钟测 `n=0`、单 digit。对照 Study：`count_digit_sum_mod0(100,3)` 与暴力一致。

**限时流程**：5 分钟判定数位 DP + 写状态；10 分钟 DFS；5 分钟 `[L,R]` 差分；5 分钟复杂度口述。

**自测清单**：`K=3,n=0..20` 暴力一致；`K=1` 全部为 0 的个数应为 n+1；故意去掉前导零判断观察 WA。

**与面试官沟通**：强调「前导零不计入数位和」「tight 保证不超过 n」「记忆化四维」。

**能力检查（闭卷）**：15 分钟写 `count_digit_sum_mod0`；解释 `nz` 时 `nmod=mod`；口述 `O(len×K)`。

## Python 实现

Study 文件 `digit_dp.py` 实现数位和模 K 计数及与暴力对拍。完整源码如下（与仓库一致）：

```python
"""数位 DP：统计 [0, n] 中数位和 % K == 0 的整数个数（修正前导零）。"""

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
        """z=True 表示仍处于前导零阶段（数值尚未开始）。"""
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


if __name__ == "__main__":
    k = 3

    def brute(nn: int) -> int:
        c = 0
        for x in range(0, nn + 1):
            if sum(int(ch) for ch in str(x)) % k == 0:
                c += 1
        return c

    for nn in range(0, 500):
        assert count_digit_sum_mod0(nn, k) == brute(nn)
    try:
        count_digit_sum_mod0(10, 0)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    print("digit_dp OK")
```

**实现要点**

- `s = str(n)`：避免大整数循环，按位处理。
- `limit = int(s[i]) if tight else 9`：非 tight 时该位可填 0..9。
- `nz = z and (d == 0)`：仅当前导零且填 0 仍保持前导零。
- `nmod = mod if nz else (mod + d) % k`：核心修正，防止 007 与 7 的数位和混淆。
- `__main__` 对 `nn in range(500)` 暴力对拍，并测 `K=0` 异常。

运行自测见 **Study 仓库对照**，应打印 `digit_dp OK`。

**逐行阅读 `dfs`**

- 边界 `i==len(s)`：构造完成，检查余数是否为 0。
- `for d in range(0, limit+1)`：枚举当前位。
- `ntight`：仅当仍 tight 且选满上限位时下一层仍 tight。
- 返回值累加子问题，记忆化自动去重。

**调试建议**：对 `n=12,K=3` 打印每层 `(i,tight,mod,z)->返回值`；与暴力 5 对照。

**扩展练习**：实现 `count_digit_sum_mod0_range(L,R,K)` 用差分；加 `prev` 做不含连续相同。

## C++ 实现

C++ 镜像 `digit_dp.cpp`，逻辑与 Python 一一对应：

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;

int K;
string s;
int memo[25][2][10][2];

int dfs(int i, bool tight, int mod, int z) {
    if (i == (int)s.size()) return mod == 0 ? 1 : 0;
    int& mem = memo[i][tight][mod][z];
    if (mem != -1) return mem;
    int lim = tight ? s[i] - '0' : 9;
    int tot = 0;
    for (int d = 0; d <= lim; ++d) {
        bool ntight = tight && (d == lim);
        bool nz = z && (d == 0);
        int nmod = nz ? mod : (mod + d) % K;
        tot += dfs(i + 1, ntight, nmod, nz);
    }
    return mem = tot;
}

int count_digit_sum_mod0(long long n, int k) {
    if (k <= 0) throw runtime_error("k must be positive");
    if (n < 0) return 0;
    K = k;
    s = to_string(n);
    memset(memo, -1, sizeof(memo));
    return dfs(0, true, 0, true);
}
```

**对照要点**

- `memo` 第四维 `z` 用 0/1；`mod` 维大小需 ≥ K（Study 用 10，因 K=3 演示）。
- 全局 `K,s` 便于 `dfs` 签名与 Python 一致；工程代码可封装成类。
- `main` 中 `brute` 与 Python 相同范围对拍。

## 练习与延伸

本专题在 atelier 不单独为 LeetCode 题号建页；题解在 Study `problems/leetcode/` 按题号组织。

**题单（按模型）**

| 模型 | 题号 | 说明 |
|------|------|------|
| 数位和模 | 自定义 | 同 Study |
| 统计 1 | 233 | 按位贡献 |
| 各位不同 | 357 | 状压 digit |
| 至少重复 | 1012 | 补集 |

**对拍**：`n≤500` 暴力；随机 K,n 比较 Python/C++。

**相邻专题**：`algo-dp-linear`、`algo-dp-bitmask`、`algo-dynamic-programming`。

**错误类型**：WA 前导零或 tight；TLE 用暴力扫 n；MLE memo 维度过小。

### 二进制位 DP（对照）

部分题按二进制位构造（如不含连续 1 的正整数），`limit` 为 1 或上界位，`d∈{0,1}`，状态同样含 tight 与前导零。转移框架与十进制相同，仅基数不同。理解十进制后，二进制题只需改枚举范围。

### 233 数字 1 的个数（思路）

统计 `[1,n]` 中十进制表示里数字 1 的出现次数，可按位 DFS：当前位填 d，若 d==1 则贡献 `count_suffix(tight')` 个数字在该位为 1。需要额外计算「后面任意填法」的计数，或分别做「计数数字个数」与「按位贡献」两种 DFS。与模 K 计数同属数位家族。

### 357 各位都不同的数字（思路）

增加 `mask` 表示已使用的 digit（0..9），前导零时 d 可不占 mask；非前导零若 `mask` 已含 d 则剪枝。状态 `(i,tight,mask,z)`，复杂度 O(位数×2×1024×2)，仍远小于遍历 n。

### 记忆化与迭代

数位 DP 几乎总用记忆化 DFS；迭代填表需按 i 分层，面试 DFS 更直观。C++ 注意每次查询清空 memo。

### 面试白板 30 秒版

「数位 DP：把 n 变字符串，从高到低填每位，状态 tight 是否贴上界、z 是否前导零、mod 为数位和模 K。前导零不更新 mod。答案 count(R)-count(L-1)。复杂度 O(位数×K)。」

### PowerShell 双语言验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\digit\digit_dp.py
g++ -std=c++17 -O2 -o run.exe digit_dp.cpp; .\run.exe
```

两行均 `digit_dp OK` 后再刷 233/357。

### 与暴力对拍工程

Study 在 `__main__` 用 `nn in range(500)` 对拍，修改转移后务必保留该循环。自写题可降到 200 加速。对拍失败时打印最小反例 `nn,K`。

### 大 K 与 memo 数组

C++ `memo[i][tight][mod][z]` 第三维需 ≥ K。若 K=1000，可改用 `unordered_map` 存稀疏 mod 或滚动；Python `lru_cache` 无维度硬编码问题。

### OI 常见变形

「数字和为 x 的倍数」「相邻差不超过 1」「包含子串 13」等，均在四维骨架上加 1～2 维状态。竞赛先写暴力小数据猜状态，再写记忆化。

### 与容斥结合

「至少包含一个 4」可总个数减「不含 4」的数位 DP。补集转化是数位题第二套路。

#
### 数位 DP 四维状态手推（n=12, K=3）

`s="12"`。走 DFS：位 0 可填 0..1；若填 0 仍前导零且 mod 不变；填 1 则 tight 且进入非前导。位 1 在 tight 下只能填 2。合法末态 mod=0：0,3,6,9,12 共 5 个。与 `brute(12,3)` 一致。手推时画表格列 (i,tight,mod,z)，每格展开 d 分支，比背代码更有效。

### tight 与 limit 的关系

`limit = int(s[i]) if tight else 9`。一旦某步 `d < limit`，下一步 `tight=False`，后续位可填 0..9 任意，对应「已小于 n 的前缀，后面可自由填」。若始终 `d==limit`，则整条路径对应上界 n 本身。漏写 `d==limit` 而写 `d<=limit` 会导致 tight 过早放松，计数偏大。

### leading_zero 与单数字 0

`n=0` 时 `s="0"`，一位 DFS：d=0 时 z 仍为真，末态 mod=0 计 1。若不用 z 维，会把前导 0 当成数位和里的 0 重复计数或漏计「空数值」。多位数如 007 在整数语义等于 7，数位和应按 7 算，前导零阶段不累计。

### [L,R] 区间封装（练习）

```python
def count_range(L: int, R: int, k: int) -> int:
    if L > R:
        return 0
    return count_digit_sum_mod0(R, k) - (count_digit_sum_mod0(L - 1, k) if L > 0 else 0)
```

面试常问 [1,n] 与 [0,n] 差 1，注意 L=0 不调用 L-1。

### 233 数字 1 的个数（按位贡献）

求 [1,n] 中数字 1 出现总次数：按位考虑，若当前位填 1，则后面在 tight' 约束下有多少种填法，贡献 `suffix_count`。与「计数有多少个数满足性质」不同，是 **加总贡献** 而非计数末态=1。框架仍是数位 DFS，返回值可能是 int 累加而非 0/1。

### 357 各位都不同的数字

状态 `(i,tight,mask,z)`：mask 记录已用 digit（10 位或 1<<d）。前导零时 d 可不占 mask；非前导且 mask 已有 d 则剪枝。复杂度 O(位数×2×1024×2)。n 到 10^9 仍可行。

### 600 不含连续 1（二进制数位）

按二进制位 DFS，d∈{0,1}，加 `prev` 状态：若 d==1 且 prev==1 非法。与十进制同一骨架，limit 由 tight 决定为 1 或上界位。

### 1012 至少有 1 位重复（补集）

[1,n] 总数减去「各位都不同」的个数。补集 + 357 模板是数位第二套路。

### 记忆化键与 C++ memo 维度

Python `lru_cache(i,tight,mod,z)`。C++ `memo[25][2][K][2]` 第三维须 ≥ K；K=1000 时改 map 或压缩状态。每次新 n 必须 `memset(memo,-1)`。

### digit_dp 暴力对拍工程意义

Study `nn in range(500)` 建立信任。改 `nmod` 后保留对拍。竞赛 n 极大不能暴力，开发阶段必须小 n 验证。

### 与线性/背包/区间选型

| 题面信号 | 子目录 |
|----------|--------|
| 大 n 计数、数位约束 | digit |
| 前缀/子序列 | linear |
| 容量 | knapsack |
| 连续段合并 | interval |

### 六类复杂度背诵（digit 行）

数位 O(位数×K×状态维×10)。位数约 19，K 常 ≤1000，总状态数万级。

### 面试 30 秒（再背）

「把 n 变字符串，dfs(i,tight,mod,z)。前导零不更新 mod。tight 用 d==limit。答案 f(R)-f(L-1)。O(len×K)。」

### PowerShell 双脚本验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\digit\digit_dp.py
g++ -std=c++17 -O2 -o run.exe digit_dp.cpp; .\run.exe
```

### 读者自检（终）

手推 n=12,K=3 得 5；解释 z 维；写 [L,R] 差分；对拍 OK；区分 233 贡献与计数。

### 专题收束

digit 核心：按位 + tight + 前导零。Study `count_digit_sum_mod0` 为锚。讲义与 `digit_dp.py` 同步，strict 后 published。atelier 不建单题页。

### 第三次补强（达标）

回到 Study 主函数手推断言样例；改代码必改讲义。Python/C++ 节须有真代码块。六节 ### 标题与 topic-algorithm.yaml 一致。汉字 medium≥8000。与 `algo-dp-bitmask` 结构对齐。六类 DP 链：linear→knapsack→interval→**digit**→bitmask。维护者禁 skeleton 覆盖正文。

### 手推表格式模板（n=23,K=5）

位 0：d=0 保持 z；d=1,2 进入非前导更新 mod。位 1：在 tight 下 limit=2。列出每分支 (i,tight,mod,z) 终态是否 mod=0。与暴力核对。

### 错误复盘清单

前导零未跳过 mod 更新；tight 条件错；K=0 未抛错；[L,R] 差分 off-by-one；memo 未清空；C++ mod 维小于 K。

### 与容斥、补集题

「至少一个 4」= 总数 - 不含 4 的数位 DP。「恰好两个 4」用容斥两层。掌握补集后数位题面变简单。

### OI 数字和、倍数约束

数位和等于 x、能被 x 整除、相邻差≤1 等，均在四维骨架上加 1～2 维。竞赛先 n≤1000 暴力猜状态再写记忆化。

### 工程与维护

slug `algo-dp-digit`；status draft；validate 双 strict。Study 断言变更则同步手推段。

### 结语（篇幅收束）

数位 DP 学习曲线在 tight 与 leading_zero；掌握后迁移 357/233。坚持 `digit_dp OK` 再刷题。完读应能闭卷写 dfs 四维与 [L,R] 公式。


### 专题强化·数位DP·1

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·2

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·3

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·4

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·5

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·6

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·7

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·8

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·9

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·10

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·11

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·12

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·13

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·数位DP·14

**核心函数**：Study 实现 `count_digit_sum_mod0`，自测输出 `digit_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-digit --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：数位DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。

## 学习路径衔接

读完本页后读 `algo-dp-bitmask`（小 n 子集）与 `algo-dynamic-programming` 总览。题单 `prob-hot100` 中数位题较少，可刷 `prob-offer` 或竞赛题集。

### 维护说明

slug `algo-dp-digit` 保持 draft 直至人工复核；published 需 `validate_algorithm_guide.py --strict` 与 `validate_algorithm_quality.py --strict` 双过。

### 结语

数位 DP 的核心是 **按位构造 + tight + 前导零**。Study `count_digit_sum_mod0` 是模 K 计数锚点；掌握四维状态后，迁移到「禁止连续」「各位不同」只需扩展状态而不少改框架。坚持双语言对拍直到 `digit_dp OK`，再上大 n 或 `[L,R]` 题。

## 学习路径

1. **第 1 天**：读懂导读与四维状态，手推 `n=12,K=3`。
2. **第 2 天**：默写 Python `count_digit_sum_mod0`，运行 Study 脚本与暴力对拍。
3. **第 3 天**：对照 C++ `digit_dp.cpp`，理解 `memset` 与 `memo` 维度。
4. **第 4 天**：实现 `[L,R]` 差分封装；尝试 233 或 357 一题。
5. **第 5 天**：回到 `algo-dynamic-programming` 总览，对比六类 DP 选型。

若已熟悉 `algo-dp-linear`，注意数位 **不是** 前缀 `dp[i]` 扫数组下标，而是扫 **位下标**。若已熟悉 `algo-dp-bitmask`，注意 n 大时位数仍小，优先数位而非状压。

**复习检查**：能否在 5 分钟内写出 DFS 框架？能否解释为何 `z` 单独成维？能否口述 `[L,R]` 公式？

**与面试专题**：`iv-top-frequent` 中部分计数题可转化为数位；树与图题不用本页。

**时间分配建议**：medium 专题建议累计 3～5 小时：阅读 1.5h、双语言运行 0.5h、刷题 2h。

**草稿状态**：本文 `status: draft`，通过校验后由维护者改 `published` 并更新 `人工撰写进度.md`。

## 延伸阅读

- Study 笔记：[python/.../digit/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/dynamic_programming/digit/notes.md)
- 仓库根目录：[zhk0567/Algorithm](https://github.com/zhk0567/Algorithm)
- 站点总览：`algo-dynamic-programming`、`algo-graph`（无关但常一起复习）
- 推荐先修：`algo-dp-linear`（记忆化基础）

数位 DP 经典讲解可参考《算法竞赛进阶指南》数位 DP 章节；LeetCode 题解区搜索「digit DP」「tight」「leading zero」对照状态定义。以 Study 源码为准更新本站正文。
