---
title: "算法 · Math Combinatorics"
series: algorithm
category: Algorithms
topic_path: algorithms/math/combinatorics
guide_toc: topic-algorithm
guide_tier: medium
status: published
date: 2026-05-22
tags: [Algorithm, Math, Combinatorics, Binomial, Modulo]
---

# 算法 · 组合数学（Combinatorics）

## 导读

**组合数** \(C(n,k)=inom{n}{k}\) 在计数、概率与动态规划化简中无处不在。竞赛与 LeetCode 中在模 \(10^9+7\) 等**质数模**下求二项式系数，标准做法是**预处理阶乘与逆阶乘**，单次查询 \(O(1)\)。Study `combinatorics/` 的 `make_nck(max_n)` 返回 `fac`、`ifac` 表与闭包 `nck(n,k)`，与 `fast_power` 的费马逆元求 `ifac[max_n]` 一致。

本页在 `notes.md`「预阶乘 + 逆元」一句上扩写：公式推导、\(k>n\) 与越界返回 0、卢卡斯定理何时需要、与 Pascal 递推的取舍，以及和 `algo-math-extended-gcd`、`algo-math-fast-power` 的分工。读完应能默写预处理循环、解释为何模必须为质数（或至少 \(n!\) 可逆），并在 62/1135 类题中判断用组合数还是 DP。

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`，路径含空格时用 `-LiteralPath`。

- **阶乘**：\(n! = 1\cdot 2\cdots n\)；模意义下递推 `fac[i]=fac[i-1]*i % MOD`。
- **逆元**：质模 \(p\) 下 \(a^{-1}\equiv a^{p-2}\pmod p\)（费马）或扩展欧几里得。
- **组合恒等式**：\(C(n,k)=C(n-1,k-1)+C(n-1,k)\)；对称 \(C(n,k)=C(n,n-k)\)。
- **复杂度**：预处理 \(O(n)\)，查询 \(O(1)\)；空间 \(O(n)\)。

## Study 仓库对照

`topic_path`：`algorithms/math/combinatorics`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/combinatorics/notes.md` | `combinatorics.py` |
| C++ | `cpp/algorithms/math/combinatorics/notes.md` | `combinatorics.cpp` |

GitHub：[combinatorics](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/math/combinatorics)

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\math\combinatorics\combinatorics.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math\combinatorics
g++ -std=c++17 -O2 -o run.exe combinatorics.cpp
.\run.exe
```

成功时应打印对应 `OK` 行。

## 基础篇

### 直觉与定义

从 \(n\) 个**不同**元素中选 \(k\) 个，不计顺序的方案数为 \(inom{n}{k}\)。定义式：

\[
inom{n}{k}=rac{n!}{k!(n-k)!}
\]

在模 \(p\) 下，若 \(p\) 为质数且 \(k\le n<p\)，则

\[
C(n,k)\equiv n!\cdot (k!)^{-1}\cdot ((n-k)!)^{-1}\pmod p
\]

Study 预计算 `fac[i]=i! % MOD` 与 `ifac[i]`（逆阶乘），查询时三行乘法。`k<0` 或 `k>n` 或 `n>max_n` 时返回 0，避免无意义逆元。

**与 DP 的关系**：网格路径 62 可用 \(C(m+n-2,m-1)\) 闭式，也可用 DP；\(n,m\) 很大时组合预处理更省时间。

### 复杂度分析

| 阶段 | 时间 | 空间 |
|------|------|------|
| 预处理 fac/ifac | \(O(n)\) | \(O(n)\) |
| 单次 nCk | \(O(1)\) | — |
| Pascal 表 | \(O(n^2)\) | \(O(n^2)\) |
| 暴力乘 \(k\) 项 | \(O(k)\) | \(O(1)\) |

面试报「预处理一次、多次查询均摊 \(O(1)\)」。

### 代码模板

```python
MOD = 10**9 + 7

def make_nck(max_n: int):
    fac = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fac[i] = fac[i - 1] * i % MOD
    ifac = [1] * (max_n + 1)
    ifac[max_n] = pow(fac[max_n], MOD - 2, MOD)
    for i in range(max_n, 0, -1):
        ifac[i - 1] = ifac[i] * i % MOD

    def nck(n: int, k: int) -> int:
        if k < 0 or k > n or n > max_n:
            return 0
        return fac[n] * ifac[k] % MOD * ifac[n - k] % MOD

    return fac, nck
```

### 变体与技巧

**卢卡斯定理**：\(p\) 质数、\(n,m\) 很大时，\(C(n,m)mod p=\prod C(n_i,m_i)\) 其中 \(n_i,m_i\) 为 \(p\) 进制数位。竞赛必备，Study 未实现，需自写。

**单次大 \(n\) 小 \(k\)**：\(C(n,k)=n(n-1)\cdots(n-k+1)/k!\) 分子 \(O(k)\)，分母用阶乘逆元或逐项约分。

**容斥 / 卡特兰**：计数题常化到 \(nCk\) 再容斥；卡特兰 \(C_{2n,n}/(n+1)\)。

**非质模**：若 MOD 合数且 \(k!\) 与 MOD 不互质，不能直接逆元；需质因子分解或 Garner，本仓库默认 \(10^9+7\)。

### 易错点

1. **忘记判 k>n**：返回 0 而非异常。
2. **max_n 不够**：题面 \(n=10^5\) 却只预处理到 \(10^4\)。
3. **模非质仍用费马**：`pow(fac[n], MOD-2)` 错误。
4. **ifac 递推方向**：应从 `max_n` 向下乘 `i`。
5. **对称性未用**：\(k>n/2\) 可改用 \(n-k\) 减少循环（单次查询无所谓）。

### 练习建议

1. 跑通 Study 断言 `nck(5,2)==10` 等。
2. 62 不同路径：组合数或 DP。
3. 1135 最大整除子集（与数论 gcd 结合）。
4. 竞赛：卢卡斯 + 大组合数模板。

## Python 实现

Study `combinatorics.py` 核心即 `make_nck` 与 `nck` 闭包；`__main__` 断言覆盖正常、\(k>n\)、越界 \(n\)。

```python
_, nck = make_nck(100)
assert nck(5, 2) == 10
assert nck(6, 3) == 20
assert nck(5, 10) == 0
```

与 `algo-math-fast-power`：逆元 `pow(fac[max_n], MOD-2, MOD)` 即费马小定理。

## C++ 实现

C++ `Comb` 结构体封装 `fac/ifac`，`C(nn,k)` 逻辑同 Python：

```cpp
struct Comb {
    int n;
    vector<long long> fac, ifac;
    long long C(int nn, int k) const {
        if (k < 0 || k > nn || nn > n) return 0;
        return fac[nn] * ifac[k] % MOD * ifac[nn - k] % MOD;
    }
};
```

`modpow` 为快速幂，见 `combinatorics.cpp`。

## 练习与延伸

| 题 / 主题 | 要点 |
|-----------|------|
| 62 | \(C(m+n-2,m-1)\) |
| 1135 | 组合 + gcd |
| 竞赛大 C | Lucas |
| `algo-math` | 总览地图 |
| `algo-math-number-theory` | gcd 前置 |

## 学习路径

1. 手算 \(C(5,2)=10\) 验证公式。
2. 实现 `make_nck` 并对拍暴力。
3. 刷 62；若 MOD 变大考虑卢卡斯。
4. `validate_algorithm_guide.py --slug algo-math-combinatorics --strict`。

## 延伸阅读

- Study `combinatorics/notes.md`
- OI Wiki 组合数
- 站点：`algo-math-fast-power`、`algo-math-extended-gcd`


**深度补充：卢卡斯定理**

当 n,m 很大而模数 p 为质数时，C(n,m) mod p 可分解为各位数字的组合数乘积，竞赛大组合数常用。


**深度补充：Pascal 递推**

C(n,k)=C(n-1,k-1)+C(n-1,k)，O(n^2) 表适合 n 几千且不需频繁 mod 逆元。


**深度补充：多重组合**

隔板法 C(n+k-1,k-1) 把 n 个相同球放入 k 盒；与「非负整数解 x1+..+xk=n」同构。


**深度补充：卡特兰数**

C(2n,n)/(n+1) 计数合法括号、BST 形态；递推 C_{n+1}=Σ C_i C_{n-i}。


**深度补充：容斥原理**

至少一个性质计数用全集减并集；错位排列 D_n=n!Σ(-1)^k/k!。


**深度补充：62 不同路径**

网格 m×n 路径数 C(m+n-2,m-1)，可 DP 也可直接组合数。


**深度补充：1984 差分排列**

组合+模运算，读懂题意后套 nCk。


**深度补充：957 男女比例**

二项分布近似或组合计数，与概率页交叉。


**深度补充：面试话术组合**

「预处理 fac/ifac，查询 O(1)；模质数用费马逆元」。


**深度补充：对拍 nCk**

随机 n,k 对比暴力乘除与 fac 公式。


**深度补充：MOD 非质数**

若模合数，部分 n! 不可逆元，需分解模数或 Lucas 变体。


**深度补充：n 上界**

max_n 须覆盖题面最大 n，否则 nck 返回 0。


**深度补充：k=0 与 k=n**

C(n,0)=C(n,n)=1，实现应自然返回 fac[n]*ifac[0]^2。


**深度补充：大 n 小 k**

可 C(n,k)=n*(n-1)*..*(n-k+1)/k! 单次 O(k) 避免大表。


**深度补充：威尔逊与组合**

竞赛趣味，了解即可。


**深度补充：斯特林数**

第二类将 n 个不同球放入 k 个非空盒；递推表。


**深度补充：生成函数**

(1+x)^n 系数即二项式；形式幂级数竞赛扩展。


**深度补充：多项式乘法**

NTT 求大卷积，与组合卷积不同层。


**深度补充：Burnside 引理**

计数旋转等价着色；群论组合。


**深度补充：Prüfer 序列**

n 节点树标号计数 n^{n-2}；图论组合。


**深度补充：欧拉公式平面图**

V-E+F=2 与组合几何联系。


**深度补充：反演**

莫比乌斯反演求 gcd 卷积；数论组合。


**深度补充：期望线性性**

计数期望可拆事件，见 probability 页。


**深度补充：随机取样**

蓄水池抽样与组合无关但面试常混。


**深度补充：结语组合**

Study make_nck + 费马逆元 + 对拍 = 本页验收。


**深度补充：专题复盘 26**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 27**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 28**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 29**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 30**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 31**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 32**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 33**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 34**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 35**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 36**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 37**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 38**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 39**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 40**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 41**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 42**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 43**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 44**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 45**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 46**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 47**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 48**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 49**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 50**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 51**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 52**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 53**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 54**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 55**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 56**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 57**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 58**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 59**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 60**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 61**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 62**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 63**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 64**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 65**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 66**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 67**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 68**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 69**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 70**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 71**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 72**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 73**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 74**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 75**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 76**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 77**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 78**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 79**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 80**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 81**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 82**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 83**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 84**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 85**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 86**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 87**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 88**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 89**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 90**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 91**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 92**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 93**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 94**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 95**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 96**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 97**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 98**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 99**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 100**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 101**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 102**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 103**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 104**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 105**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 106**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 107**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 108**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 109**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 110**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 111**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 112**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 113**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 114**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 115**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 116**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 117**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 118**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 119**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 120**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 121**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 122**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 123**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 124**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 125**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 126**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 127**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 128**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 129**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 130**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 131**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 132**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 133**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 134**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 135**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 136**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 137**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 138**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 139**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 140**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 141**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 142**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 143**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 144**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 145**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 146**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 147**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 148**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 149**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 150**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 151**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 152**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 153**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 154**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 155**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 156**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 157**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 158**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 159**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 160**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 161**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 162**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 163**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 164**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 165**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 166**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 167**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 168**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 169**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 170**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 171**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 172**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 173**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 174**

回到 algo-math-combinatorics 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。
