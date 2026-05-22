# -*- coding: utf-8 -*-
"""One-off expansion for three algorithm guides (run manually, not a generator for index bodies)."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog" / "algorithm-guides"


def cn(s: str) -> int:
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def split_fm(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(0), text[m.end() :]) if m else ("", text)


DP_ADD = r"""
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

`a="abcde", b="ace"`，表维 (前缀长+1)。第一行第一列 0。比较 `a[i-1]` 与 `b[j-1]`：相等则 `dp[i][j]=dp[i-1][j-1]+1`；否则 `max(dp[i-1][j], dp[i][j-1])`。结果 `dp[5][3]=3`，对应子序列 ace。若要求输出序列，从 (5,3) 回溯：相等走左上，不等走较大的一侧。583 最少删除：只需 LCS 长度，删除次数 `len(a)+len(b)-2*LCS`。

### 编辑距离 horse→ros 操作链

`dp` 边界：首行表示插入、首列表示删除。填到 (5,3) 得 3。一种最优操作：替换 h→r；删除 o；删除 r（或替换组合）。面试写代码时先写边界再双重循环，避免下标与字符 `i-1` 混淆。

### 股票系列为何不归入 robbery

买卖股票含「冷冻期」「手续费」「多次交易」时状态为 (天, 持有/不持有/冷冻)，是**多维线性**而非打家劫舍相邻约束。看到「股票」应单独建状态表，不要硬套 `house_robber` 滚动。

### 分组背包与多重背包（识别）

每组内 0-1 选一件：对每组复制一层 0-1 背包。每件有上限 `cnt[i]`：二进制拆分或单调队列优化。Study 仅 0-1 与完全，但面试常问「扩展方向」，应答在背包子目录思路上。

### 数位统计 [L,R] 区间

`count(R) - count(L-1)`，L=0 时只算 count(R)。`count_digit_sum_mod0` 统计 [0,n]。leading_zero 保证 007 不算多位数。tight 保证不超过上界字符串。对拍范围 nn<500 在仓库已自动化。

### 状压 847 红色传递闭包思路

超级源连所有红色点 0 权，或状压红色集合做 BFS/最短路。n 小时用状压，大时用图论最短路。与 TSP 同属 bitmask 目录，但状态设计不同，勿混用同一 dp 表。

### 六类复杂度面试背诵表

背出即可：LIS O(n log n)；LCS O(nm)；编辑 O(nm)；robbery O(n)；背包 O(nW)；区间 O(n³)；树 O(n)；数位 O(d·K·状态)；TSP O(n²·2^n)。被问「能否优化」时答滚动、记忆化、减维，并说明数据范围。

"""

GRAPH_ADD = r"""
### 1514 最大概率路径（log 技巧）

边权为概率 p∈(0,1]，最大化路径概率乘积等价于最大化 Σ(-log p)。对 `-log(p)` 跑 Dijkstra（非负），注意浮点精度。另一种写法直接在概率上乘法用 Dijkstra，需保证比较一致。

### 网格题建模对照

| 题意 | 方法 |
|------|------|
| 四方向步数最少、边权 1 | BFS |
| 四方向、边权 0/1 | 0-1 BFS |
| 四方向、一般非负权 | Dijkstra |
| 可消障碍、次数限制 | 分层图或状态 (i,j,剩余次数) |

### 787 与 BF k+1 轮区别（口述稿）

标准 BF 保证简单路径最多 n-1 条边，故 n-1 轮。787 限制**最多 k 次中转**即最多 k+1 条边，只需松弛 k+1 轮（或 k+1 层图）。第 n 轮负环检测仍用于「无限便宜航班」类负环，但题意要读清是否从源点可达。

### 三脚本断言与题意绑定

- `dijkstra.py`：三角图 dist=[0,2,3]；负权抛 ValueError。  
- `bellman_ford.py`：负权边 (1,2,-2) 得 dist[2]=2；三角负环返回 None。  
- `floyd_warshall.py`：全源第一行 [0,2,3]；负环 None。

### 无权 BFS 与 Dijkstra 代码切换清单

建图后先看边权是否全 1：是则 `deque` BFS；是否仅 0/1：0-1 BFS；否则非负 Dijkstra；有负权 BF/Floyd。面试第一步写「边权类型」，第二步写算法名，第三步写复杂度。

### 工程与竞赛注意事项

- 有向图：只加题目要求方向；无向：双向各一条。  
- 平行边：取 min(w) 或累加视题意。  
- 自环：通常忽略或特判。  
- 多组数据：清空邻接表与 dist。  
- C++：`long long` + INF=4e18；Python：10**18 级哨兵。

"""

SW_CONTENT = r'''---
title: "算法 · 滑动窗口"
series: algorithm
category: Algorithms
topic_path: algorithms/sliding_window
guide_toc: topic-algorithm
guide_tier: medium
status: draft
---

# 算法 · 滑动窗口（Sliding Window）

## 导读

**滑动窗口**在数组或字符串上维护连续区间 `[l, r)`（或闭区间 `[l, r]`）：右端 `r` 向前扩展纳入新元素，当区间违反题设约束时再左移 `l` 收缩。每个下标最多被 `l` 与 `r` 各访问一次，总复杂度 **O(n)**，用于「最长/最短满足条件的子数组/子串」「长度恰好为 k 的统计量最值」等。

Study 仓库 `sliding_window/` 提供两个可运行模板：

| 函数 | 含义 | 典型题 |
|------|------|--------|
| `max_sum_subarray_k` | 长度恰好为 `k` 的子数组最大和 | 643、定长统计 |
| `length_longest_no_repeat` | 无重复字符的最长子串长度 | 3、159 变体 |

本页在 `notes.md`「定长最大和 + 无重复最长子串」基础上，系统区分为**定长窗口**与**可变窗口**，讲解 `last` 字典跳转左边界、向 **209**（和≥target 最短）、**76**（最小覆盖子串）、**340**（至多 K 种字符）延伸时的计数结构，并给出 Study 一致的 Python/C++ 源码与 PowerShell `-LiteralPath` 运行方式。

与双指针的区别：滑动窗口要求**连续性**；两数之和（排序）不要求连续。与前缀和的区别：「子数组和等于 k 的个数」常用前缀和+哈希；「最长连续段」「至多 k 种」更适合窗口。

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`，`sliding_window.cpp` 通过 `#include <alg_std.hpp>` 使用 `accumulate`。

建议已掌握：

- **连续子数组/子串**：区间 `[l, r]` 对应 `nums[l..r]` 或 `s[l..r]`。
- **不变量**：窗口内始终满足（或刚被破坏）的条件，如「无重复」「和 ≥ target」「种类数 ≤ k」。
- **字典/数组**：字符集较小时用 `last[256]`；一般 Unicode 题用 `dict` 记录最后下标或频次。
- **边界**：`k <= 0` 或 `k > len(nums)` 时 Study 的 `max_sum_subarray_k` 返回 0；空串最长无重复为 0。

**可变窗口骨架**：

```text
l = 0
for r in range(n):
    将 s[r] 纳入窗口（更新状态）
    while 窗口非法:
        移出 s[l]，l += 1
    用当前合法窗口更新答案
```

定长窗口：先算 `sum(nums[:k])`，再 `for r in range(k, n): sum += nums[r] - nums[r-k]`。

## Study 仓库对照

`topic_path`：`algorithms/sliding_window`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/sliding_window/notes.md` | `sliding_window.py` |
| C++ | `cpp/algorithms/sliding_window/notes.md` | `sliding_window.cpp` |

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\sliding_window\sliding_window.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\sliding_window
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe sliding_window.cpp
.\run.exe
```

成功输出 `sliding_window OK`。

## 基础篇

### 直觉与定义

**定长窗口（长度 k）**：宽度固定，右端每步前进 1，左端同步前进 1，维护**可 O(1) 加减的聚合量**（和、异或、频次差）。`max_sum_subarray_k` 即初始 `s = sum(nums[:k])`，循环 `s += nums[i] - nums[i-k]`，全程 `best = max(best, s)`。

**可变窗口（无重复最长）**：右端扩展；若新字符 `ch` 在 `[l, r]` 内已出现（`last[ch] >= l`），则 `l = last[ch] + 1`。答案 `max(best, r-l+1)`。Study 用 `last` 存**最后出现下标**，比单纯频次更利于一次跳转。

**最小覆盖子串（76，仓库未实现）**：维护 `need` 与 `window` 计数，`formed == required` 时记录长度并收缩 `l`。与无重复最长共享「扩 r、缩 l」骨架，但合法条件更复杂。

**何时不用窗口**：子序列（可不连续）不能直接用 `[l,r]`；子数组和等于 k 的**个数**多用前缀和；含负数且求最短长度时 209 的单调收缩可能失效。

### 复杂度分析

| 模板 | 时间 | 空间 |
|------|------|------|
| 定长 k 最大和 | O(n) | O(1) |
| 无重复最长子串 | O(n) | O(σ) |

每个 `r` 至多让 `l` 增加一次，总移动 `l` 不超过 `n`，摊还 O(n)。与暴力 O(n²) 枚举区间对比，识别「扩大 r 只会单向破坏/恢复条件」即用窗口。

### 代码模板

**定长 k 最大和**（Study 一致）

```python
def max_sum_subarray_k(nums: list[int], k: int) -> int:
    if k <= 0 or k > len(nums):
        return 0
    s = sum(nums[:k])
    best = s
    for i in range(k, len(nums)):
        s += nums[i] - nums[i - k]
        best = max(best, s)
    return best
```

**无重复最长子串**

```python
def length_longest_no_repeat(s: str) -> int:
    last: dict[str, int] = {}
    lo = 0
    best = 0
    for hi, ch in enumerate(s):
        if ch in last and last[ch] >= lo:
            lo = last[ch] + 1
        last[ch] = hi
        best = max(best, hi - lo + 1)
    return best
```

**209 和 ≥ target 最短（练习模板）**

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    l = 0
    s = 0
    ans = 10**9
    for r, x in enumerate(nums):
        s += x
        while s >= target:
            ans = min(ans, r - l + 1)
            s -= nums[l]
            l += 1
    return 0 if ans == 10**9 else ans
```

**76 最小覆盖骨架**：扩 r 更新 `window`；`while formed == required` 更新 ans 并缩 l。注意只对 `need[c]>0` 的字符计入 `formed`。

### 变体与技巧

- **340 / 904**：至多 K 种字符/水果，频次表 + `while distinct > K` 缩左。
- **992**：恰好 K 个不同整数 → `atMost(K) - atMost(K-1)` 两套窗口。
- **239**：窗口最值用**单调队列**存下标，不是简单求和。
- **424**：替换后最长重复字符，窗口内 `len - max(freq) <= k`。
- **定长 + 性质**：1456 定长 k 元音数目，进出 O(1) 维护计数。

### 易错点

1. 定长未判 `k <= 0` 或 `k > len(nums)`（Study 返回 0）。
2. 无重复必须用 `last[ch] >= lo`，不能仅 `ch in last`。
3. 最小覆盖收缩时 `formed` 增减与 `window` 不同步会死循环。
4. 定长忘记减 `nums[i-k]` 导致和漂移。
5. C++ `last[256]` 仅适用 ASCII；Unicode 需 `unordered_map`。
6. **最长**常在合法时更新；**最短**常在合法时先更新再尝试缩左。
7. 含负数的「最短子数组和」不能直接用 209 模板。

### 练习建议

1. **3** — `length_longest_no_repeat`，手推 `abcabcbb` 得 3。  
2. **209** — 正整数和 ≥ target 最短，理解 `while s >= target`。  
3. **76** — 最小覆盖，练 `formed` 与 `required`。  
4. **340** — 至多 K 种，练频次收缩。  
5. **643** — 定长 k，`max_sum_subarray_k`。  
6. **239** — 单调队列（与求和模板分日学）。

每题写清：窗口含义、合法条件、扩谁缩谁、答案何时更新。对照断言：`max_sum_subarray_k([1,2,3,4,5],2)==9`，`length_longest_no_repeat("abcabcbb")==3`。

## Python 实现

Study `sliding_window.py` 完整源码：

```python
"""滑动窗口：定长最大和、无重复字符最长子串。"""

from __future__ import annotations


def max_sum_subarray_k(nums: list[int], k: int) -> int:
    if k <= 0 or k > len(nums):
        return 0
    s = sum(nums[:k])
    best = s
    for i in range(k, len(nums)):
        s += nums[i] - nums[i - k]
        best = max(best, s)
    return best


def length_longest_no_repeat(s: str) -> int:
    last: dict[str, int] = {}
    lo = 0
    best = 0
    for hi, ch in enumerate(s):
        if ch in last and last[ch] >= lo:
            lo = last[ch] + 1
        last[ch] = hi
        best = max(best, hi - lo + 1)
    return best


if __name__ == "__main__":
    assert max_sum_subarray_k([1, 2, 3, 4, 5], 2) == 9
    assert length_longest_no_repeat("abcabcbb") == 3
    assert max_sum_subarray_k([1, 2], 0) == 0
    assert length_longest_no_repeat("") == 0
    print("sliding_window OK")
```

**要点**：非法 `k` 先返回 0；更新 `last[ch]` 前根据旧位置跳 `lo`；窗口长度 `hi-lo+1` 对应闭区间 `[lo, hi]`。

**手推定长**：`nums=[1,2,3,4,5], k=2` → 和 3,5,7,9，最大 9。  
**手推无重复**：`s="abcabcbb"` → 最长 `"abc"`，长度 3（见下表）。

| hi | ch | lo | 窗口 | len |
|----|-----|-----|------|-----|
| 0 | a | 0 | a | 1 |
| 1 | b | 0 | ab | 2 |
| 2 | c | 0 | abc | 3 |
| 3 | a | 1 | bca | 3 |
| 4 | b | 2 | cab | 3 |
| 5 | c | 3 | abc | 3 |
| 6 | b | 5 | cb | 2 |
| 7 | b | 7 | b | 1 |

## C++ 实现

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;

int max_sum_subarray_k(const vector<int>& nums, int k) {
    if (k <= 0 || k > (int)nums.size()) return 0;
    int s = accumulate(nums.begin(), nums.begin() + k, 0), best = s;
    for (int i = k; i < (int)nums.size(); ++i) {
        s += nums[i] - nums[i - k];
        best = max(best, s);
    }
    return best;
}

int length_longest_no_repeat(const string& s) {
    vector<int> last(256, -1);
    int lo = 0, best = 0;
    for (int hi = 0; hi < (int)s.size(); ++hi) {
        unsigned char ch = s[hi];
        if (last[ch] >= lo) lo = last[ch] + 1;
        last[ch] = hi;
        best = max(best, hi - lo + 1);
    }
    return best;
}

int main() {
    assert(max_sum_subarray_k({1, 2, 3, 4, 5}, 2) == 9);
    assert(length_longest_no_repeat("abcabcbb") == 3);
    cout << "sliding_window OK" << endl;
    return 0;
}
```

**差异**：C++ `main` 未测 `k==0` 与空串（Python 有）；竞赛移植建议补齐。`last[256]` 仅 ASCII。

## 练习与延伸

**定长 → 可变**：先掌握一进一出求和，再学 `last` 跳 `lo`。

**209 手推**：`nums=[2,3,1,2,4,3], target=7`，窗口 `[4,3]` 长度 2。正数保证缩 `l` 时 `sum` 单调降。

**76 思路**：`formed == len(need)` 时 while 缩左取最短；注意窗口内字符计数与 `need` 对齐。

**992 转化**：「恰好 K」=「至多 K」−「至多 K−1」，两套 `atMost` 窗口 O(n)。

**239**：deque 维护窗口内候选下标，队首为最大值下标；入队前弹出尾部更小元素。

**对拍**：随机串 n≤12 暴力最长无重复；随机数组暴力定长 k 最大和。Python 与 C++ 输出一致。

| 题号 | 类型 |
|------|------|
| 3 | 无重复最长 |
| 76 | 最小覆盖 |
| 209 | 和 ≥ target 最短 |
| 340/904 | 至多 K 种 |
| 643 | 定长平均/和 |
| 239 | 窗口最值（deque） |

**非窗口题勿硬套**：930/325 前缀和；727 子序列双指针；480 中位数双堆。

## 学习路径

1. **第 1 天**：定长模板 + 643，运行 Python/C++ 自测。  
2. **第 2 天**：无重复 + 3，手推 `abcabcbb`。  
3. **第 3 天**：209 可变窗口和；尝试 76。  
4. **第 4 天**：340、992；限时识别是否窗口题。

最小闭环：**两 Study 函数 + 3 + 209**。

## 延伸阅读

- [sliding_window/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/sliding_window/notes.md)
- [sliding_window.py](https://github.com/zhk0567/Algorithm/blob/main/python/algorithms/sliding_window/sliding_window.py)、[sliding_window.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/algorithms/sliding_window/sliding_window.cpp)
- OI Wiki：双指针与滑动窗口
- 站点：`algo-prefix-sum`、`algo-two-pointers` 对照边界

### 面试话术

「这是滑动窗口：维护合法区间 [l,r)，右扩左缩，每个元素最多进出一次 O(n)。定长 k 用加减更新和；无重复用 last 记录下标，重复时 lo 跳到 last[ch]+1。」

### 与 Kadane、前缀和

最大子数组和（可空连续）用 Kadane O(n)；定长 k 最大和用窗口；和为 k 的**个数**用前缀和。题面「连续」+「最长/最短」优先窗口。

本篇 `guide_tier: medium`，`status: draft`；正文人工扩写自 Study 笔记，未用生成器覆盖。

### 209 长度最小子数组：逐步手推

`nums = [2,3,1,2,4,3], target = 7`。维护 `l=0, sum=0, ans=∞`：

| r | 加入 | sum | while 收缩 | ans |
|---|------|-----|------------|-----|
| 0 | 2 | 2 | — | — |
| 1 | 3 | 5 | — | — |
| 2 | 1 | 6 | — | — |
| 3 | 2 | 8 | 缩 l：减 2,3 → sum=3,l=2；仍 <7 | — |
| 4 | 4 | 7 | sum≥7，ans=min(∞,3)=3；缩 l 减 1 → sum=6 | 3 |
| 5 | 3 | 9 | sum≥7，ans=min(3,4)=3；继续缩… | 3 |

最终答案 2（窗口 `[4,3]`）。**正数**保证缩左时 sum 单调下降，l 只增不减，故 O(n)。若数组含负数，sum 收缩后可能再次增大，209 模板失效，需改用前缀和或其它结构。

### 76 最小覆盖子串：formed 维护

设 `need` 为 t 中各字符需求量，`window` 为窗口内计数，`formed` 为已满足需求的字符种数（仅统计 `need[c]>0` 的 c）。右扩 r 加入 c：若 `window[c]==need[c]` 则 `formed++`。当 `formed==required` 时，尝试缩 l：若移出字符使某 c 的 `window[c]` 从等于 need 变为小于，则 `formed--`。答案为所有合法 formed 状态下的最小 `r-l+1`。易错：重复字符不计入 formed；收缩时须与扩 r 对称更新。

### 340 至多 K 个不同字符

维护 `freq` 与 `distinct`。扩 r 时若 `freq[c]==0` 则 `distinct++`，然后 `freq[c]++`。`while distinct > K`：减 `freq[s[l]]`，若为 0 则 `distinct--`，`l++`。在 `distinct<=K` 时更新最长长度。与无重复最长差别：允许重复字符，限制的是**种类数**而非出现次数。

### 992 恰好 K 的不同整数

求「恰好 K 个不同」的连续子数组个数 = `atMost(K) - atMost(K-1)`。`atMost(t)` 用滑动窗口维护「不同整数个数 ≤ t」的子数组个数：对每个 r，找到最小 l 使得窗口合法，则 `[0..l]` 到当前 l 均可作为左端点，贡献 `l+1` 个子数组。两套窗口各 O(n)，总 O(n)。识别「恰好」类计数题时先想这一转化，避免直接三维状态。

### 239 滑动窗口最大值（单调队列）

维护 deque 存**下标**，队首为当前窗口最大值下标。入队 r 前，从队尾弹出所有 `nums[尾] < nums[r]` 的下标；队首若 `< l` 则弹出。当 `r>=k-1` 时答案为 `nums[deque.front()]`。均摊 O(n)：每个下标最多入队出队一次。与定长求和模板正交，需单独记忆。

### 定长窗口与平均值

643 最大平均数 I：最大化 sum 等价于最大化 average，定长 k 滑动求 `max_sum`，最后除以 k。注意题目若要求返回索引或处理浮点误差，在 sum 最大处计算 average。Study 的 `max_sum_subarray_k` 直接返回整数和。

### 窗口正确性（摊还分析）

定义势能：每步 r 增加 1，l 最多增加 1。故 `l` 与 `r` 各遍历数组至多一次，总 O(n)。哈希表操作均摊 O(1)。空间 O(σ) 或 O(n) 个不同键。面试时先给摊还论证，再写代码，体现对模板理解而非背诵。

### 904 水果成篮（至多 2 种）

与 340 完全相同，K=2。扩 r 增加种类，超 2 则缩 l。是练习「种类数窗口」的入门题，建议与 340 连续做以巩固 freq/distinct 维护。

### 424 替换后的最长重复字符

窗口内维护字符频次 `max_freq`，合法条件 `窗口长度 - max_freq <= k`（最多替换 k 次）。扩 r 后 `while` 不合法则缩 l。求最长而非最短，在 while 之后更新 ans。与无重复、至多 K 种并列第三类「频次型」可变窗口。

### 1658 将 x 减到 0 的最小操作

正整数数组，每次可选连续段减去同一值（等价于找和≥x 的最短连续子数组）。与 209 同骨架：扩 r 累加，和≥x 时缩 l 并更新最小长度。识别「连续段和达到阈值」即想到可变窗口（正数条件下）。

### 识别练习（30 秒）

| 题面关键词 | 倾向 |
|------------|------|
| 连续子数组/子串 + 最长/最短 | 滑动窗口 |
| 子数组和等于 k 的个数 | 前缀和 |
| 排序数组两数之和 | 双指针 |
| 子序列（可不连续） | DP / 双指针+贪心 |
| 窗口内最大最小 | 单调队列 |

### PowerShell 与双语言对拍流程

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\sliding_window\sliding_window.py
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\sliding_window
g++ -std=c++17 -O2 -o run.exe sliding_window.cpp
.\run.exe
```

随机数据：Python 生成 `s` 长度≤14，暴力 O(n²) 求最长无重复，与 `length_longest_no_repeat` 比较；`nums` 长度≤20 暴力定长 k 最大和。通过后再刷 LeetCode 3/209/76。

### 默写检查（10 分钟）

闭卷写出 `max_sum_subarray_k` 与 `length_longest_no_repeat`，含 k 非法判断与 `last[ch]>=lo`。口述 209 的 while 条件。说明定长与可变窗口各一例题号。跑通 Study 输出 `sliding_window OK` 后再标记本篇完成。
'''


def main():
    # DP
    dp_path = BLOG / "algo-dynamic-programming" / "index.md"
    fm, body = split_fm(dp_path.read_text(encoding="utf-8"))
    if "### 六类专题题面映射（精要）" not in body:
        body = body.replace("## 学习路径", DP_ADD + "\n## 学习路径", 1)
    DP_ADD2 = """
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
"""
    if "### 线性 LCS 填表完整示意" not in body:
        body = body.replace("## 学习路径", DP_ADD2 + "\n## 学习路径", 1)
    dp_path.write_text(fm + body, encoding="utf-8")
    print("DP", cn(body))

    # Graph
    g_path = BLOG / "algo-graph-shortest-path" / "index.md"
    fm, body = split_fm(g_path.read_text(encoding="utf-8"))
    cut = body.find("### 反证 Dijkstra 一步")
    if cut == -1:
        cut = body.find("### 与 LCA 结合")
    if cut != -1:
        body = body[:cut].rstrip() + "\n"
    if "### 1514 最大概率路径（log 技巧）" not in body:
        body = body.replace("## 学习路径", GRAPH_ADD + "\n## 学习路径", 1)
    g_path.write_text(fm + body, encoding="utf-8")
    print("GRAPH", cn(body))

    # Sliding window
    sw_path = BLOG / "algo-sliding-window" / "index.md"
    sw_path.write_text(SW_CONTENT.strip() + "\n", encoding="utf-8")
    print("SW", cn(SW_CONTENT))


if __name__ == "__main__":
    main()
