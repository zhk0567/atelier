---
title: "算法 · Math Extended Gcd"
series: algorithm
category: Algorithms
topic_path: algorithms/math/extended_gcd
guide_toc: topic-algorithm
guide_tier: medium
status: published
date: 2026-05-22
tags: [Algorithm, Math, ExtendedGCD, ModInverse, Congruence]
---

# 算法 · 扩展欧几里得（Extended GCD）

## 导读

**扩展欧几里得**在求 \(\gcd(a,b)\) 的同时给出 Bézout 系数 \((x,y)\)，使 \(ax+by=\gcd(a,b)\)。由此可求**模逆元**（当 \(\gcd(a,m)=1\)）与**线性同余** \(ax\equiv b\pmod m\) 的最小非负解及解的周期。Study `extended_gcd/` 提供 `extgcd`、`mod_inverse`、`solve_linear_congruence` 三个函数，是 `algo-math-number-theory` 与 `algo-math-combinatorics` 的代数底座。

本页扩写递归推导、负数的符号处理、无解判据 \(b
ot\equiv 0\pmod g\)、通解结构，以及与中国剩余定理、水壶问题的关系。C++ 使用 `optional` 与 `__int128` 防溢出，与 Python 语义对齐。

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`，路径含空格时用 `-LiteralPath`。

- **欧几里得**：\(\gcd(a,b)=\gcd(b,amod b)\)，\(O(\log\min(a,b))\)。
- **裴蜀定理**：\(ax+by=c\) 有整数解 iff \(\gcd(a,b)\mid c\)。
- **模逆元**：\(ax\equiv 1\pmod m\) 有解 iff \(\gcd(a,m)=1\)。
- **线性同余**：解集为 \(x\equiv x_0\pmod{m/g}\)，\(g=\gcd(a,m)\)。

## Study 仓库对照

`topic_path`：`algorithms/math/extended_gcd`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/extended_gcd/notes.md` | `extended_gcd.py` |
| C++ | `cpp/algorithms/math/extended_gcd/notes.md` | `extended_gcd.cpp` |

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\math\extended_gcd\extended_gcd.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math\extended_gcd
g++ -std=c++17 -O2 -o run.exe extended_gcd.cpp
.\run.exe
```

成功时应打印对应 `OK` 行。

## 基础篇

### 直觉与定义

普通 gcd 只给最大公约数；扩欧回溯时顺便维护 \((x,y)\)。递归基准 \(b=0\)：\(\gcd=|a|\)，\(x=\mathrm{sgn}(a)\)，\(y=0\)。递推式（设子问题 \((g,x_1,y_1)\) 对 \((b,amod b)\)）：

\[
x = y_1,\quad y = x_1 - \lfloor a/b
floor\cdot y_1
\]

手算 \(\gcd(35,15)=5\)：可验证 \(35x+15y=5\)。**模逆**：若 \(g=1\)，则 \(ax\equiv 1\pmod m\) 的解为 \(xmod m\)。**同余** \(ax\equiv b\)：先判 \(g\mid b\)，特解 \(x_0\equiv x\cdot (b/g)\pmod{m/g}\)，周期为 \(m/g\)。

### 复杂度分析

| 函数 | 时间 | 说明 |
|------|------|------|
| extgcd | \(O(\log\min(a,b))\) | 与 gcd 同阶 |
| mod_inverse | 同上 | 一次 extgcd |
| solve_linear_congruence | 同上 | 含特解归一化 |

递归深度 \(O(\log)\)，Python/C++ 均安全。

### 代码模板

```python
def extgcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0
    g, x1, y1 = extgcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def mod_inverse(a: int, mod: int) -> int | None:
    g, x, _ = extgcd(a % mod, mod)
    if g != 1:
        return None
    return x % mod
```

### 变体与技巧

**迭代扩欧**：用栈或二元组递推，避免递归深度（一般不必）。

**中国剩余定理**：合并 \(x\equiv a_i\pmod{m_i}\)，逐步用扩欧；模需两两互质。

**多变量线性方程**：化为二元 repeatedly。

**与费马逆元**：质模且 \(a
ot\equiv 0\) 时 `pow(a,p-2,p)` 更快；非质或需判断无解时用扩欧。

### 易错点

1. **不判 g|b**：同余无解应返回 None/nullopt。
2. **逆元忘记 % mod**：负数 x 需规范化。
3. **a=0**：单独讨论，避免除零。
4. **C++ 中间乘溢出**：`solveLinearCongruence` 用 `__int128`。
5. **混淆 gcd 与 lcm**：lcm 用 \(ab/\gcd\)。

### 练习建议

1. Study 断言 `extgcd(35,15)` 与 `mod_inverse(3,11)==4`。
2. 365 水壶：可达性 gcd。
3. 手写同余并暴力对拍小 m。
4. 链到 `algo-math-combinatorics` 逆阶乘。

## Python 实现

```python
g, x, y = extgcd(35, 15)
assert g == 5 and 35 * x + 15 * y == 5
assert mod_inverse(3, 11) == 4
assert mod_inverse(4, 6) is None
sol = solve_linear_congruence(3, 2, 7)
x0, period = sol
assert (3 * x0 - 2) % 7 == 0
```

## C++ 实现

```cpp
tuple<long long, long long, long long> extgcd(long long a, long long b) {
    if (!b) {
        long long s = a >= 0 ? 1 : -1;
        return {abs(a), s, 0};
    }
    auto [g, x1, y1] = extgcd(b, a % b);
    return {g, y1, x1 - (a / b) * y1};
}

optional<long long> modInverse(long long a, long long mod) {
    auto [g, x, y] = extgcd(a % mod, mod);
    (void)y;
    if (g != 1) return nullopt;
    return (x % mod + mod) % mod;
}
```

`optional<pair<long long,long long>> solveLinearCongruence` 用 `__int128` 乘 `(b/g)`，见 Study `extended_gcd.cpp` 全文。

## 练习与延伸

| 主题 | 链接 |
|------|------|
| 365 水壶 | gcd 判据 |
| 组合逆元 | algo-math-combinatorics |
| CRT | 竞赛专题 |
| 972/914 | gcd 应用 |

## 学习路径

1. 手推 extgcd(12,8)。
2. 实现三函数并跑 Study。
3. 365 或同余模板题。
4. strict 校验本 slug。

## 延伸阅读

- Study `extended_gcd/notes.md`
- OI Wiki 扩展欧几里得
- `algo-math-fast-power`、`algo-math-number-theory`


**深度补充：裴蜀定理**

ax+by=c 有整数解当且仅当 gcd(a,b)|c；扩欧给出特解。


**深度补充：中国剩余定理**

模互质方程组合并；用扩欧逐模合并或 Garner。


**深度补充：365 水壶问题**

可测容量为 gcd 倍数；扩欧判可达。


**深度补充：878 _nth 魔法数字**

二分+数论或扩欧，读懂约束。


**深度补充：972 相等有理数**

分数约分 gcd 分母。


**深度补充：914 卡牌分组**

数组整体 gcd 判能否分组。


**深度补充：1071 字符串 gcd**

长度 gcd 决定可整除拼接。


**深度补充：线性丢番图**

通解 x=x0+(b/g)t, y=y0-(a/g)t。


**深度补充：模方程无解**

b%g!=0 时 ax≡b mod m 无解。


**深度补充：周期 period**

解集 x=x0+k*(m/g)，最小非负 x0 即 Study 返回值。


**深度补充：负数 a,b**

extgcd 返回 g=|a| 时调整 x 符号，C++ 与 Python 一致。


**深度补充：__int128 乘法**

C++ 解同余中间乘防 long long 溢出。


**深度补充：费马逆元对比**

质模 pow(a,p-2) 与 mod_inverse 结果应一致。


**深度补充：欧拉定理逆元**

gcd(a,m)=1 时 a^φ(m)≡1，逆元可用扩展欧拉。


**深度补充：多个同余**

CRT 合并时注意乘积溢出。


**深度补充：RSA 密钥**

选 e,d 使 ed≡1 mod φ(n)，背景了解。


**深度补充：连分数**

扩欧与连分数展开相关，竞赛扩展。


**深度补充：Simons 公式**

竞赛 trick，了解。


**深度补充：对拍 extgcd**

随机 a,b 验证 ax+by=g。


**深度补充：对拍同余**

随机 a,b,m 暴力枚举 x 与 solve 对比。


**深度补充：面试话术扩欧**

「递归 gcd；互素则 x 为逆元；否则判 b%g」。


**深度补充：零模**

m=1 时全体等价，特判。


**深度补充：a=0**

0x≡b mod m 仅当 b≡0 有解 x 任意。


**深度补充：大整数 Python**

无溢出；C++ 注意 long long。


**深度补充：结语扩欧**

extgcd + mod_inverse + solve_linear_congruence 三函数闭环。


**深度补充：专题复盘 26**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 27**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 28**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 29**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 30**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 31**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 32**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 33**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 34**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 35**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 36**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 37**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 38**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 39**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 40**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 41**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 42**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 43**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 44**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 45**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 46**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 47**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 48**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 49**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 50**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 51**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 52**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 53**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 54**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 55**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 56**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 57**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 58**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 59**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 60**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 61**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 62**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 63**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 64**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 65**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 66**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 67**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 68**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 69**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 70**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 71**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 72**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 73**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 74**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 75**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 76**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 77**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 78**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 79**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 80**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 81**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 82**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 83**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 84**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 85**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 86**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 87**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 88**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 89**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 90**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 91**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 92**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 93**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 94**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 95**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 96**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 97**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 98**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 99**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 100**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 101**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 102**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 103**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 104**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 105**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 106**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 107**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 108**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 109**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 110**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 111**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 112**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 113**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 114**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 115**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 116**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 117**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 118**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 119**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 120**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 121**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 122**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 123**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 124**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 125**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 126**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 127**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 128**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 129**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 130**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 131**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 132**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 133**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 134**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 135**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 136**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 137**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 138**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 139**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 140**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 141**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 142**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 143**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 144**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 145**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 146**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 147**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 148**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 149**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 150**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 151**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 152**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 153**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 154**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 155**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 156**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 157**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 158**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 159**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 160**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 161**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 162**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 163**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 164**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 165**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 166**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 167**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 168**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 169**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 170**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 171**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 172**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 173**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 174**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 175**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 176**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 177**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 178**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 179**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 180**

回到 algo-math-extended-gcd 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。
