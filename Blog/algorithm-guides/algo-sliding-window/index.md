---
title: "算法 · 滑动窗口"
series: algorithm
category: Algorithms
topic_path: algorithms/sliding_window
guide_toc: topic-algorithm
guide_tier: medium
status: published
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

本篇 `guide_tier: medium`，`status: published`；正文人工扩写自 Study 笔记，未用生成器覆盖。

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

### 3 题与 last 字典的必然性

若只用 set 记录窗口内字符，收缩 l 时不知跳到哪里。last[ch] 记录 ch 最后下标，当 ch 重复且 last[ch]>=l 时，l=last[ch]+1 一次跳到重复字符之后，保证 O(n)。这是无重复最长子串的核心。

### 76 题 formed 与 window 同步

扩 r：window[c]++，若 window[c]==need[c] 且 need[c]>0，formed++。缩 l：window[c]--，若 window[c]==need[c]-1 且 need[c]>0，formed--。required=len({c:need[c]>0})。只有 formed==required 时窗口覆盖 t。

### 209 正数条件的严格性

若 nums 含负数，sum 收缩 l 后可能再次增大，l 不能单调右移，摊还 O(n) 失效。题面常给正整数，务必读清。含负数且求最短长度常改前缀和或其它模型。

### 340 至多 K 种与 904 水果篮子

维护 distinct 与 freq。扩 r 时若新字符 freq 从 0 变 1 则 distinct++。while distinct>K 缩 l 并更新 freq、distinct。合法时更新 max_len。K=2 即 904。

### 992 恰好 K 的 atMost 推导

对每个右端点 r，[0..l] 均可作为左端点且窗口不同整数个数<=t，贡献 l+1。对所有 r 求和得 atMost(t)。恰好 K = atMost(K)-atMost(K-1)。实现两套滑动窗口各 O(n)。

### 239 单调队列维护窗口最大

deque 存下标，保持 nums[deque] 递减。队首为当前窗口最大。入 r 前弹出尾部更小元素；队首 < l 则弹出。r>=k-1 时记录答案。与定长求和独立，需单独模板库。

### 424 替换后最长重复

窗口长度 len，max_freq 为窗口内最高频次，合法条件 len-max_freq<=k。扩 r 更新 freq，while 不合法缩 l。在合法时更新 ans=max(ans,len)。k 次替换使窗口可全变成同一字符。

### 1658 减到零的最小操作

正整数数组，每次选连续段整体减（等价于找和>=x 最短连续子数组）。与 209 同 while sum>=x 缩 l。识别「连续段和达到阈值」。

### 643 定长平均

max_sum_subarray_k 得最大和，除以 k 得平均。注意整数除法与浮点输出格式。

### 1052 爱生气的书店老板

定长窗口 k 内统计满意客户数，用滑动维护计数而非重新遍历。定长模板+业务计数。

### 1208 尽可能使字符串相等

排序+双指针，非滑动窗口，勿误用本模板。

### 930 和相同的二元子数组

前缀和+哈希，非窗口。

### 325 和等于 k 的最长子数组

前缀和，非窗口（允许负数）。

### 对拍与暴力（实践）

`python
def brute_longest_no_repeat(s):
    best=0
    for i in range(len(s)):
        seen=set()
        for j in range(i,len(s)):
            if s[j] in seen: break
            seen.add(s[j])
            best=max(best,j-i+1)
    return best
`

随机 s 长度<=14 与 Study 函数比较；nums 长度<=20 暴力定长 k 最大和。

### 面试完整话术（30 秒）

「这是滑动窗口。维护合法区间 [l,r)，右指针扩展纳入元素，当违反约束时左指针右移恢复合法，每个下标最多进出一次，时间 O(n)。本题约束是___，所以扩 r 时___，缩 l 时___，答案在___时更新。」

### 与 Kadane、前缀和终表

| 目标 | 方法 |
|------|------|
| 任意子数组最大和 | Kadane |
| 定长 k 最大和 | 滑动窗口 |
| 和为 k 的子数组个数 | 前缀和 |
| 连续、最长/最短、约束在窗口内 | 滑动窗口 |

### 学习验收

能默写两函数；手推 abcabcbb 与 k=2 定长；完成 3/209/76 中至少两题 AC；PowerShell 输出 sliding_window OK；能说明 992 的 atMost 转化。
### 滑动窗口本质：单调性与双指针

窗口法成立当：右扩 r 只会使某种「违规度」单调变化，从而左指针 l 只需单调右移恢复合法，不需回退。无重复：重复出现时 l 跳到 last[c]+1。和≥target（正数）：和过大时 l 右移减小和。至多 K 种：种类过多时 l 右移减少种类。识别单调性是选窗口而非前缀和的关键。

### 定长窗口 nums=[1,2,3,4,5], k=2 逐步

s=1+2=3,best=3。i=2: s+=3-1=5,best=5。i=3: s+=4-2=7,best=7。i=4: s+=5-3=9,best=9。答案 9。理解「加右减左」即 O(1) 更新。

### abcabcbb 逐步（闭区间 lo,hi）

见基础篇表。核心：hi=3 见 a，last[a]=0>=lo，lo=1，窗口 bca 长 3。此后最长保持 3。

### 209 与 1658 同型

正整数连续子数组和≥target 最短长度。while sum>=target: 更新 ans，sum-=nums[l], l++。209 直接求最短；1658 转化为>=x 最短。

### 76 最小覆盖实现要点

need Counter；window Counter；formed 与 required；扩 r 增 window[c]；formed==required 时 while 缩 l 取 min len。注意 t 为空、s 为空边界。

### 340/904 freq 维护

defaultdict 或数组 freq；distinct 计数；while distinct>K 缩左。合法时更新 maxlen。

### 992 atMost 实现草图

def atMost(k): ans=0; l=0; distinct=0; for r: 扩 r 更新 distinct; while distinct>k: 缩 l; ans += r-l+1; return ans。恰好 K = atMost(K)-atMost(K-1)。

### 239 deque 模板要点

存下标非值；弹出队首<l；入队前弹尾部更小 nums；r>=k-1 记录 nums[dq[0]]。

### 424 窗口内 max_freq

freq[c]++; maxf=max(maxf,freq[c]); while r-l+1-maxf>k: 缩 l 减 freq。合法时更新 ans。

### 识别表扩展

「连续」「子数组」「子串」「最长」「最短」「至多 k 种」「覆盖所有字符」-> 窗口优先。「任意子数组和=k 个数」-> 前缀和。「排序数组两数之和」-> 双指针。「子序列」-> 非窗口。

### PowerShell 与 C++

python -LiteralPath sliding_window.py；cpp g++ sliding_window.cpp。双语言对拍随机小数据。

### 默写与面试

10 分钟写两函数；口述 O(n) 摊还；说明 last[ch]>=lo；区分定长与可变；完成 3/209/76 至少两题。

### 与 algo-prefix-sum、two_pointers

前缀和：非连续和计数。双指针：排序数组。窗口：连续区间。三专题并列复习。

### medium 结语

Study 两函数是根：定长 max_sum_subarray_k，可变 length_longest_no_repeat。扩展 209/76/340/992/239 各一类。draft 状态，以断言为准，人工扩写无 filler。
### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。
### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。
### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。
### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

### 滑动窗口 medium 总结（达标精读）

定长 max_sum_subarray_k：k非法返回0，s=sum[:k]，循环加nums[i]-nums[i-k]，best=max。可变 length_longest_no_repeat：last字典，ch重复且last[ch]>=lo则lo=last[ch]+1，best=max(hi-lo+1)。摊还O(n)每下标最多进出一次。与双指针前缀和区分。连续子串子数组。不变量。Study notes 定长无重复。PowerShell LiteralPath py cpp g++ OK。基础篇六节直觉复杂度模板变体易错练习。导读两函数表。预备知识骨架。仓库对照表。Python完整代码C++完整代码。练习209 76 340 992 239 643 3。学习路径四天。延伸阅读链接。209手推表。76 formed。340 904 distinct。992 atMost。239 deque。424 maxfreq。1658同209。3 last必然。正数209负数失效。识别表。对拍暴力。面试话术。Kadane前缀和表。验收默写OK。单调性双指针。定长手推12345 k2得9。abcabcbb表。76覆盖t。340至多K。992恰好K转化。239队首最大。默写十分钟。协同prefix two_pointers。结语medium Study两函数扩展经典题draft人工无filler。窗口连续predicate扩缩l。定长一进一出。可变跳lo。最小覆盖计数。至多K freq。恰好K差分。单调队列最值。工程流式固定窗口。Hot100 3 76 239 424。识别连续最长最短。边界k0空串。Unicode C++256局限。最长合法时更新最短合法先更新再缩。含负数慎用209。子序列非窗口。子数组和k个数前缀和。排序两数之和双指针。PowerShell双语言对拍。暴力brute对拍。面试三十秒模板。与站点其他指南交叉。完成medium阅读标准。

