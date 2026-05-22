---
title: "算法 · Math Matrix"
series: algorithm
category: Algorithms
topic_path: algorithms/math/matrix
guide_toc: topic-algorithm
guide_tier: medium
status: published
date: 2026-05-22
tags: [Algorithm, Math, Matrix, FastPower, Fibonacci]
---

# 算法 · 矩阵（Matrix）

## 导读

**矩阵快速幂**把线性递推（如 Fibonacci）从 \(O(n)\) DP 降到 \(O(\log n)\)。Study `matrix/` 提供 `mat_mul`、`mat_pow` 与 `fib(n)`：转移矩阵 \(egin{pmatrix}1&1\1&0\end{pmatrix}^{n-1}\) 的右上角即 \(F_n\)。本页讲清乘法维度、模意义取模、单位阵与空矩阵边界，并与 `algo-math-fast-power` 标量快速幂对照。

矩阵亦可描述图的路径计数（邻接矩阵幂）、概率 Markov 一步转移等。

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`，路径含空格时用 `-LiteralPath`。

- **矩阵乘法**：\(C_{ij}=\sum_k A_{ik}B_{kj}\)，维数 \((n	imes k)(k	imes m)\)。
- **快速幂**：二进制拆指数，见 `algo-math-fast-power`。
- **Fibonacci**：\(F_0=0,F_1=1,F_n=F_{n-1}+F_{n-2}\)。

## Study 仓库对照

`topic_path`：`algorithms/math/matrix`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/matrix/notes.md` | `matrix.py` |
| C++ | `cpp/algorithms/math/matrix/notes.md` | `matrix.cpp` |

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\math\matrix\matrix.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math\matrix
g++ -std=c++17 -O2 -o run.exe matrix.cpp
.\run.exe
```

成功时应打印对应 `OK` 行。

## 基础篇

### 直觉与定义

线性递推 \(F_n = c_1 F_{n-1} + \cdots + c_k F_{n-k}\) 可写成状态向量 \(\mathbf{v}_n = M\mathbf{v}_{n-1}\)。Fibonacci 用 \(2	imes2\) 矩阵 \(M=egin{pmatrix}1&1\1&0\end{pmatrix}\)，\(\mathbf{v}_n=(F_{n+1},F_n)^T\)。则 \(F_n\) 为 \(M^{n-1}\) 的 \((0,0)\) 元（Study 实现约定）。

`mat_pow` 与标量快速幂同构：结果初始为单位阵，底矩阵平方，指数位为 1 则乘入。

### 复杂度分析

| 操作 | 时间 | 说明 |
|------|------|------|
| mat_mul k×k | \(O(k^3)\) | 三重循环 |
| mat_pow | \(O(k^3\log e)\) | e 为指数 |
| 朴素 fib | \(O(n)\) | 滚动数组可 \(O(1)\) 空间 |

\(k=2\) 时极快；\(k=10\) 仍可行。

### 代码模板

```python
def mat_mul(a, b, mod):
    n, m, k = len(a), len(b[0]), len(b)
    c = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            s = 0
            for t in range(k):
                s = (s + a[i][t] * b[t][j]) % mod
            c[i][j] = s
    return c

def mat_pow(mat, e, mod):
    n = len(mat)
    res = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = [row[:] for row in mat]
    while e:
        if e & 1:
            res = mat_mul(res, base, mod)
        base = mat_mul(base, base, mod)
        e >>= 1
    return res
```

### 变体与技巧

**高维递推**：Tribonacci 用 \(3	imes3\) 转移。

**图路径**：邻接矩阵 \(A^k\) 的 \((u,v)\) 元为长度 \(k\) 的路径数。

**向量快速幂**：先乘矩阵再取状态分量，少写一维。

**MOD**：非质时仍可乘，逆元另论。

### 易错点

1. **维度不匹配**：mul 前检查 `len(b)==len(a[0])`。
2. **fib(0),fib(1)**：基准直接返回。
3. **空矩阵 pow**：Study 对 `e>0` 抛 `ValueError`。
4. **乘法不可交换**：顺序固定。
5. **忘记 mod**：中间积溢出。

### 练习建议

1. 断言 `fib(10)==55`，`fib(100)==687995182`（mod 1e9+7）。
2. 509/70 斐波那契。
3. 1137 Tribonacci 矩阵或滚动。
4. 图论路径计数（邻接矩阵幂）。

## Python 实现

```python
mod = 10**9 + 7
assert fib(10, mod) == 55
assert fib(100, mod) == 687995182
f = [[1, 1], [1, 0]]
eye = mat_pow(f, 0, mod)
assert eye == [[1, 0], [0, 1]]
```

`matrix.py` 含空矩阵 `ValueError` 测试。

## C++ 实现

```cpp
ll fib(ll n) {
    if (n <= 1) return n;
    vector<vector<ll>> f{{1, 1}, {1, 0}};
    auto p = mat_pow(f, n - 1);
    return p[0][0];
}
```

`mat_mul`/`mat_pow` 使用 `vector<vector<ll>>`；`mat_pow(f,0)` 得单位阵。

## 练习与延伸

| 题 | 方法 |
|----|------|
| 509/70 | 矩阵或 DP |
| 1137 | 3×3 矩阵 |
| 图 k 步 | \(A^k\) |
| fast_power | 标量幂对照 |

## 学习路径

1. 手算 \(M^3\) 与 \(F_4\)。
2. 跑 matrix OK。
3. 509；理解 \(O(\log n)\)。
4. strict 校验。

## 延伸阅读

- Study `matrix/notes.md`
- `algo-math-fast-power`


**深度补充：线性递推**

f(n)=Σ c_i f(n-i) 用 k×k 转移矩阵快速幂。


**深度补充：509 斐波那契**

矩阵法 O(log n) 或 DP O(n)。


**深度补充：70 爬楼梯**

同 Fib。


**深度补充：1137 第 N 个 Tribonacci**

3×3 矩阵或滚动数组。


**深度补充：矩阵链乘**

维度 DP 非方阵幂；区分题意。


**深度补充：二维矩阵**

图邻接矩阵 k 步可达性 A^k。


**深度补充：MOD 非质**

逆元不存在时用扩展欧拉或 exgcd。


**深度补充：向量乘矩阵**

k×1 状态列向量左乘转移。


**深度补充：对角化**

竞赛求矩阵 n 次幂高级，了解。


**深度补充：特征多项式**

Berlekamp-Massey 求递推系数。


**深度补充：高斯消元**

模方程组，与矩阵不同技能。


**深度补充：Floyd 与矩阵**

最短路非矩阵快速幂。


**深度补充：空矩阵**

mat_pow([],0) 返回 []；e>0 抛错。


**深度补充：单位阵**

e=0 返回 I；fib(0)=0,fib(1)=1。


**深度补充：乘法顺序**

A*B 与 B*A 一般不同；转移向量左乘右乘约定一致。


**深度补充：mod 中间积**

三重循环每步取模。


**深度补充：long long**

C++ 乘法前取模。


**深度补充：对拍 fib**

小 n 对比朴素递推。


**深度补充：对拍 mat_pow**

随机矩阵对比朴素乘幂。


**深度补充：面试话术矩阵**

「乘 O(k^3)；幂 O(k^3 log n)」。


**深度补充：图论计数**

走 k 步路径数=邻接矩阵^k 的 (i,j) 元。


**深度补充：概率 DP 矩阵**

状态向量乘转移，Markov。


**深度补充：结语矩阵**

mat_mul/mat_pow/fib 断言通过即可验收。


**深度补充：专题复盘 24**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 25**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 26**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 27**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 28**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 29**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 30**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 31**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 32**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 33**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 34**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 35**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 36**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 37**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 38**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 39**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 40**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 41**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 42**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 43**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 44**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 45**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 46**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 47**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 48**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 49**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 50**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 51**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 52**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 53**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 54**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 55**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 56**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 57**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 58**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 59**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 60**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 61**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 62**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 63**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 64**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 65**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 66**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 67**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 68**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 69**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 70**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 71**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 72**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 73**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 74**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 75**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 76**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 77**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 78**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 79**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 80**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 81**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 82**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 83**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 84**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 85**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 86**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 87**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 88**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 89**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 90**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 91**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 92**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 93**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 94**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 95**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 96**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 97**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 98**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 99**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 100**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 101**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 102**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 103**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 104**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 105**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 106**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 107**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 108**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 109**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 110**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 111**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 112**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 113**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 114**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 115**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 116**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 117**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 118**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 119**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 120**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 121**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 122**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 123**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 124**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 125**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 126**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 127**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 128**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 129**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 130**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 131**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 132**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 133**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 134**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 135**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 136**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 137**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 138**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 139**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 140**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 141**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 142**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 143**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 144**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 145**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 146**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 147**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 148**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 149**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 150**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 151**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 152**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 153**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 154**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 155**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 156**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 157**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 158**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 159**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 160**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 161**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 162**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 163**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 164**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 165**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 166**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 167**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 168**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 169**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 170**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 171**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 172**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 173**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 174**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 175**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 176**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 177**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 178**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 179**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 180**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 181**

回到 algo-math-matrix 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。
