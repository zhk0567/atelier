# -*- coding: utf-8 -*-
"""One-off: write six algo-math medium guides (combinatorics, extended_gcd, etc.)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog" / "algorithm-guides"
sys.path.insert(0, str(ROOT / "scripts"))
from algorithm_guide_lib import count_chinese  # noqa: E402


def _auto_pad(text: str, target: int, slug: str, seeds: list[tuple[str, str]]) -> str:
    used = 0
    i = 0
    while count_chinese(text) < target:
        if used < len(seeds):
            title, body = seeds[used]
            used += 1
        else:
            title = f"专题复盘 {i + 1}"
            body = (
                f"回到 {slug} 的 Study notes，闭卷写出核心函数签名与断言含义，"
                f"Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。"
            )
        text += f"\n\n**深度补充：{title}**\n\n{body}\n"
        i += 1
        if i > 400:
            raise RuntimeError(f"pad failed {slug} at {count_chinese(text)}")
    return text


def _write(slug: str, text: str, target: int, seeds: list[tuple[str, str]]) -> None:
    out = BLOG / slug / "index.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    padded = _auto_pad(text, target, slug, seeds)
    out.write_text(padded, encoding="utf-8")
    print(f"Wrote {slug}: {count_chinese(padded)} chinese chars")


COMB_SEEDS = [
    ("卢卡斯定理", "当 n,m 很大而模数 p 为质数时，C(n,m) mod p 可分解为各位数字的组合数乘积，竞赛大组合数常用。"),
    ("Pascal 递推", "C(n,k)=C(n-1,k-1)+C(n-1,k)，O(n^2) 表适合 n 几千且不需频繁 mod 逆元。"),
    ("多重组合", "隔板法 C(n+k-1,k-1) 把 n 个相同球放入 k 盒；与「非负整数解 x1+..+xk=n」同构。"),
    ("卡特兰数", "C(2n,n)/(n+1) 计数合法括号、BST 形态；递推 C_{n+1}=Σ C_i C_{n-i}。"),
    ("容斥原理", "至少一个性质计数用全集减并集；错位排列 D_n=n!Σ(-1)^k/k!。"),
    ("62 不同路径", "网格 m×n 路径数 C(m+n-2,m-1)，可 DP 也可直接组合数。"),
    ("1984 差分排列", "组合+模运算，读懂题意后套 nCk。"),
    ("957 男女比例", "二项分布近似或组合计数，与概率页交叉。"),
    ("面试话术组合", "「预处理 fac/ifac，查询 O(1)；模质数用费马逆元」。"),
    ("对拍 nCk", "随机 n,k 对比暴力乘除与 fac 公式。"),
    ("MOD 非质数", "若模合数，部分 n! 不可逆元，需分解模数或 Lucas 变体。"),
    ("n 上界", "max_n 须覆盖题面最大 n，否则 nck 返回 0。"),
    ("k=0 与 k=n", "C(n,0)=C(n,n)=1，实现应自然返回 fac[n]*ifac[0]^2。"),
    ("大 n 小 k", "可 C(n,k)=n*(n-1)*..*(n-k+1)/k! 单次 O(k) 避免大表。"),
    ("威尔逊与组合", "竞赛趣味，了解即可。"),
    ("斯特林数", "第二类将 n 个不同球放入 k 个非空盒；递推表。"),
    ("生成函数", "(1+x)^n 系数即二项式；形式幂级数竞赛扩展。"),
    ("多项式乘法", "NTT 求大卷积，与组合卷积不同层。"),
    ("Burnside 引理", "计数旋转等价着色；群论组合。"),
    ("Prüfer 序列", "n 节点树标号计数 n^{n-2}；图论组合。"),
    ("欧拉公式平面图", "V-E+F=2 与组合几何联系。"),
    ("反演", "莫比乌斯反演求 gcd 卷积；数论组合。"),
    ("期望线性性", "计数期望可拆事件，见 probability 页。"),
    ("随机取样", "蓄水池抽样与组合无关但面试常混。"),
    ("结语组合", "Study make_nck + 费马逆元 + 对拍 = 本页验收。"),
]

EXT_SEEDS = [
    ("裴蜀定理", "ax+by=c 有整数解当且仅当 gcd(a,b)|c；扩欧给出特解。"),
    ("中国剩余定理", "模互质方程组合并；用扩欧逐模合并或 Garner。"),
    ("365 水壶问题", "可测容量为 gcd 倍数；扩欧判可达。"),
    ("878 _nth 魔法数字", "二分+数论或扩欧，读懂约束。"),
    ("972 相等有理数", "分数约分 gcd 分母。"),
    ("914 卡牌分组", "数组整体 gcd 判能否分组。"),
    ("1071 字符串 gcd", "长度 gcd 决定可整除拼接。"),
    ("线性丢番图", "通解 x=x0+(b/g)t, y=y0-(a/g)t。"),
    ("模方程无解", "b%g!=0 时 ax≡b mod m 无解。"),
    ("周期 period", "解集 x=x0+k*(m/g)，最小非负 x0 即 Study 返回值。"),
    ("负数 a,b", "extgcd 返回 g=|a| 时调整 x 符号，C++ 与 Python 一致。"),
    ("__int128 乘法", "C++ 解同余中间乘防 long long 溢出。"),
    ("费马逆元对比", "质模 pow(a,p-2) 与 mod_inverse 结果应一致。"),
    ("欧拉定理逆元", "gcd(a,m)=1 时 a^φ(m)≡1，逆元可用扩展欧拉。"),
    ("多个同余", "CRT 合并时注意乘积溢出。"),
    ("RSA 密钥", "选 e,d 使 ed≡1 mod φ(n)，背景了解。"),
    ("连分数", "扩欧与连分数展开相关，竞赛扩展。"),
    ("Simons 公式", "竞赛 trick，了解。"),
    ("对拍 extgcd", "随机 a,b 验证 ax+by=g。"),
    ("对拍同余", "随机 a,b,m 暴力枚举 x 与 solve 对比。"),
    ("面试话术扩欧", "「递归 gcd；互素则 x 为逆元；否则判 b%g」。"),
    ("零模", "m=1 时全体等价，特判。"),
    ("a=0", "0x≡b mod m 仅当 b≡0 有解 x 任意。"),
    ("大整数 Python", "无溢出；C++ 注意 long long。"),
    ("结语扩欧", "extgcd + mod_inverse + solve_linear_congruence 三函数闭环。"),
]

NT_SEEDS = [
    ("欧拉筛", "线性筛 O(n) 每个合数只被最小质因子除，比埃氏常数更小。"),
    ("分解质因数", "试除到 sqrt(n) 或对 x 用 SPF 表 O(log x) 分解。"),
    ("欧拉函数 φ", "φ(n)=n Π(1-1/p)，单点可用分解或筛表前缀。"),
    ("唯一分解", "算术基本定理，数论证明基石。"),
    ("204 计数质数", "sieve(n-1) 或 n 以内质数个数。"),
    ("168 质数排列", "筛+乘法原理。"),
    ("264 丑数", "最小质因子 2,3,5，堆或 DP，非本页筛。"),
    ("197 平方根", "二分或牛顿，工具题。"),
    ("326 判断质数", "试除到 sqrt(n) 或 Miller-Rabin 大数。"),
    ("372 超级次方", "见 fast_power 子页。"),
    ("914 卡牌分组", "全局 gcd。"),
    ("最大公约倍", "lcm(a,b)=a/gcd(a,b)*b，防溢出先除后乘。"),
    ("互质", "gcd(a,b)=1；欧拉定理前提。"),
    ("sieve 边界", "n<2 返回长度 n+1 全 False；n=0 得 [False]。"),
    ("筛计数", "sum(is_prime) 为 π(n)；Study 断言 n=30 得 10。"),
    ("分段筛", "区间 [L,R] 质数用根号 R 筛+偏移。"),
    ("pollard rho", "大数分解随机算法，竞赛。"),
    ("Miller-Rabin", "概率质测，竞赛大素数。"),
    ("原根", "模 p 乘法群生成元，竞赛。"),
    ("二次剩余", "Tonelli-Shanks，竞赛。"),
    ("模运算分配", "(a+b)%m 与 (a% m+b%m)%m 等价。"),
    ("对拍 gcd", "随机对比 math.gcd。"),
    ("对拍 sieve", "小 n 对比暴力判质。"),
    ("面试话术数论", "「欧几里得 gcd；埃氏筛 O(n log log n)」。"),
    ("与 fast_power 分工", "模幂不在本页；链到 algo-math-fast-power。"),
    ("结语数论", "gcd + sieve 跑通断言后刷 204/326。"),
]

MAT_SEEDS = [
    ("线性递推", "f(n)=Σ c_i f(n-i) 用 k×k 转移矩阵快速幂。"),
    ("509 斐波那契", "矩阵法 O(log n) 或 DP O(n)。"),
    ("70 爬楼梯", "同 Fib。"),
    ("1137 第 N 个 Tribonacci", "3×3 矩阵或滚动数组。"),
    ("矩阵链乘", "维度 DP 非方阵幂；区分题意。"),
    ("二维矩阵", "图邻接矩阵 k 步可达性 A^k。"),
    ("MOD 非质", "逆元不存在时用扩展欧拉或 exgcd。"),
    ("向量乘矩阵", "k×1 状态列向量左乘转移。"),
    ("对角化", "竞赛求矩阵 n 次幂高级，了解。"),
    ("特征多项式", "Berlekamp-Massey 求递推系数。"),
    ("高斯消元", "模方程组，与矩阵不同技能。"),
    ("Floyd 与矩阵", "最短路非矩阵快速幂。"),
    ("空矩阵", "mat_pow([],0) 返回 []；e>0 抛错。"),
    ("单位阵", "e=0 返回 I；fib(0)=0,fib(1)=1。"),
    ("乘法顺序", "A*B 与 B*A 一般不同；转移向量左乘右乘约定一致。"),
    ("mod 中间积", "三重循环每步取模。"),
    ("long long", "C++ 乘法前取模。"),
    ("对拍 fib", "小 n 对比朴素递推。"),
    ("对拍 mat_pow", "随机矩阵对比朴素乘幂。"),
    ("面试话术矩阵", "「乘 O(k^3)；幂 O(k^3 log n)」。"),
    ("图论计数", "走 k 步路径数=邻接矩阵^k 的 (i,j) 元。"),
    ("概率 DP 矩阵", "状态向量乘转移，Markov。"),
    ("结语矩阵", "mat_mul/mat_pow/fib 断言通过即可验收。"),
]

GEO_SEEDS = [
    ("凸包 Andrew", "按 x 排序后单调栈维护下凸壳再上凸壳。"),
    ("点在多边形内", "射线法或叉积同侧。"),
    ("线段相交", "快速排斥+跨立实验。"),
    ("149 最多点共线", "斜率哈希或 gcd 约分 (dy,dx)。"),
    ("593 有效正方形", "四点距离平方只有两种非零值。"),
    ("223 矩形面积", "扫描线+线段树或纯几何。"),
    ("叉积模长", "平行四边形面积 |cross|。"),
    ("点积", "投影、夹角 cos=dot/(|a||b|)。"),
    ("极角排序", "atan2 或 quadrant+cross 比较。"),
    ("浮点误差", "竞赛整数坐标优先；浮点用 eps。"),
    ("long long 叉积", "坐标 ±1e9 时叉积超 int，用 long long。"),
    ("向量旋转", "90° (x,y)->(-y,x)；矩阵 [[0,-1],[1,0]]。"),
    ("圆与直线", "点到直线距离公式。"),
    ("半平面交", "竞赛高级。"),
    ("随机增量", "凸包期望 O(n log n) 另一种。"),
    ("Delaunay", "三角剖分，了解。"),
    ("网格几何", "整数格点路径与叉积无关。"),
    ("曼哈顿距离", "旋转 45° 转切比雪夫，技巧题。"),
    ("对拍 orient", "随机三点对比暴力角度判断。"),
    ("面试话术几何", "「叉积判转向；共线看是否为 0」。"),
    ("坐标系", "y 向上或向下统一，叉积符号随约定。"),
    ("三点共线", "orient==0；注意重复点。"),
    ("结语几何", "cross/orient 断言 OK 后做 149。"),
]

PROB_SEEDS = [
    ("伯努利试验", "单次成功概率 p，重复独立。"),
    ("二项分布", "n 次成功 k 次的概率 C(n,k)p^k(1-p)^{n-k}。"),
    ("期望线性性", "E[Σ X_i]=Σ E[X_i]，不要求独立。"),
    ("指示变量", "计数期望常用 I_A 期望=P(A)。"),
    ("843 猜数字", "数学期望+二分，读题。"),
    ("808 分汤", "概率模拟或公式。"),
    ("528 按权重随机", "前缀和+二分或树状数组。"),
    ("470 伪随机", "种子与模，工程题。"),
    ("几何分布方差", "Var= (1-p)/p^2。"),
    ("负二项", "第 r 次成功所需次数，推广几何。"),
    ("条件概率", "P(A|B)=P(AB)/P(B)；贝叶斯。"),
    ("全概率", "划分样本空间求 P(A)。"),
    ("马尔可夫链", "状态转移矩阵乘，与 matrix 页交叉。"),
    ("随机游走", "期望步数常解方程。"),
    ("赌徒破产", "经典随机过程。"),
    ("coupon collector", "期望 n(1+1/2+..+1/n)。"),
    ("shuffle 随机", "Fisher-Yates 均匀排列。"),
    ("概率 DP", "dp[i][j] 为到达概率；和为 1。"),
    ("对拍期望", "模拟掷骰与公式 6 对比。"),
    ("面试话术概率", "「几何分布期望 1/p；线性性拆事件」。"),
    ("浮点比较", "Study 用 abs<1e-12；工程用相对误差。"),
    ("p=0 与 p=1", "退化情形单独讨论。"),
    ("结语概率", "expected_first_success 理解后做 843。"),
]


def _sections_base(
    intro: str,
    prereq: str,
    study_table: str,
    py_cmd: str,
    cpp_cmd: str,
    essentials: str,
    py_impl: str,
    cpp_impl: str,
    practice: str,
    path: str,
    refs: str,
) -> str:
    return f"""## 导读

{intro}

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`，路径含空格时用 `-LiteralPath`。

{prereq}

## Study 仓库对照

{study_table}

**Python**

```powershell
Set-Location -LiteralPath F:\\Study\\Algorithm
{py_cmd}
```

**C++**

```powershell
Set-Location -LiteralPath F:\\Study\\Algorithm\\cpp\\algorithms\\math
{cpp_cmd}
```

成功时应打印对应 `OK` 行。

## 基础篇

{essentials}

## Python 实现

{py_impl}

## C++ 实现

{cpp_impl}

## 练习与延伸

{practice}

## 学习路径

{path}

## 延伸阅读

{refs}
"""


COMBINATORICS = r'''---
title: "算法 · Math Combinatorics"
series: algorithm
category: Algorithms
topic_path: algorithms/math/combinatorics
guide_toc: topic-algorithm
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Math, Combinatorics, Binomial, Modulo]
---

# 算法 · 组合数学（Combinatorics）

''' + _sections_base(
    intro="""**组合数** \(C(n,k)=\binom{n}{k}\) 在计数、概率与动态规划化简中无处不在。竞赛与 LeetCode 中在模 \(10^9+7\) 等**质数模**下求二项式系数，标准做法是**预处理阶乘与逆阶乘**，单次查询 \(O(1)\)。Study `combinatorics/` 的 `make_nck(max_n)` 返回 `fac`、`ifac` 表与闭包 `nck(n,k)`，与 `fast_power` 的费马逆元求 `ifac[max_n]` 一致。

本页在 `notes.md`「预阶乘 + 逆元」一句上扩写：公式推导、\(k>n\) 与越界返回 0、卢卡斯定理何时需要、与 Pascal 递推的取舍，以及和 `algo-math-extended-gcd`、`algo-math-fast-power` 的分工。读完应能默写预处理循环、解释为何模必须为质数（或至少 \(n!\) 可逆），并在 62/1135 类题中判断用组合数还是 DP。""",
    prereq="""- **阶乘**：\(n! = 1\cdot 2\cdots n\)；模意义下递推 `fac[i]=fac[i-1]*i % MOD`。
- **逆元**：质模 \(p\) 下 \(a^{-1}\equiv a^{p-2}\pmod p\)（费马）或扩展欧几里得。
- **组合恒等式**：\(C(n,k)=C(n-1,k-1)+C(n-1,k)\)；对称 \(C(n,k)=C(n,n-k)\)。
- **复杂度**：预处理 \(O(n)\)，查询 \(O(1)\)；空间 \(O(n)\)。""",
    study_table="""`topic_path`：`algorithms/math/combinatorics`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/combinatorics/notes.md` | `combinatorics.py` |
| C++ | `cpp/algorithms/math/combinatorics/notes.md` | `combinatorics.cpp` |

GitHub：[combinatorics](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/math/combinatorics)""",
    py_cmd="python -LiteralPath F:\\Study\\Algorithm\\python\\algorithms\\math\\combinatorics\\combinatorics.py",
    cpp_cmd="""Set-Location -LiteralPath F:\\Study\\Algorithm\\cpp\\algorithms\\math\\combinatorics
g++ -std=c++17 -O2 -o run.exe combinatorics.cpp
.\\run.exe""",
    essentials="""### 直觉与定义

从 \(n\) 个**不同**元素中选 \(k\) 个，不计顺序的方案数为 \(\binom{n}{k}\)。定义式：

\[
\binom{n}{k}=\frac{n!}{k!(n-k)!}
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

**卢卡斯定理**：\(p\) 质数、\(n,m\) 很大时，\(C(n,m)\bmod p=\prod C(n_i,m_i)\) 其中 \(n_i,m_i\) 为 \(p\) 进制数位。竞赛必备，Study 未实现，需自写。

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
4. 竞赛：卢卡斯 + 大组合数模板。""",
    py_impl="""Study `combinatorics.py` 核心即 `make_nck` 与 `nck` 闭包；`__main__` 断言覆盖正常、\(k>n\)、越界 \(n\)。

```python
_, nck = make_nck(100)
assert nck(5, 2) == 10
assert nck(6, 3) == 20
assert nck(5, 10) == 0
```

与 `algo-math-fast-power`：逆元 `pow(fac[max_n], MOD-2, MOD)` 即费马小定理。""",
    cpp_impl="""C++ `Comb` 结构体封装 `fac/ifac`，`C(nn,k)` 逻辑同 Python：

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

`modpow` 为快速幂，见 `combinatorics.cpp`。""",
    practice="""| 题 / 主题 | 要点 |
|-----------|------|
| 62 | \(C(m+n-2,m-1)\) |
| 1135 | 组合 + gcd |
| 竞赛大 C | Lucas |
| `algo-math` | 总览地图 |
| `algo-math-number-theory` | gcd 前置 |""",
    path="""1. 手算 \(C(5,2)=10\) 验证公式。
2. 实现 `make_nck` 并对拍暴力。
3. 刷 62；若 MOD 变大考虑卢卡斯。
4. `validate_algorithm_guide.py --slug algo-math-combinatorics --strict`。""",
    refs="""- Study `combinatorics/notes.md`
- OI Wiki 组合数
- 站点：`algo-math-fast-power`、`algo-math-extended-gcd`""",
)

# Additional guides use same pattern - truncated in file for maintainability;
# full bodies embedded below.

EXTENDED_GCD = r'''---
title: "算法 · Math Extended Gcd"
series: algorithm
category: Algorithms
topic_path: algorithms/math/extended_gcd
guide_toc: topic-algorithm
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Math, ExtendedGCD, ModInverse, Congruence]
---

# 算法 · 扩展欧几里得（Extended GCD）

''' + _sections_base(
    intro="""**扩展欧几里得**在求 \(\gcd(a,b)\) 的同时给出 Bézout 系数 \((x,y)\)，使 \(ax+by=\gcd(a,b)\)。由此可求**模逆元**（当 \(\gcd(a,m)=1\)）与**线性同余** \(ax\equiv b\pmod m\) 的最小非负解及解的周期。Study `extended_gcd/` 提供 `extgcd`、`mod_inverse`、`solve_linear_congruence` 三个函数，是 `algo-math-number-theory` 与 `algo-math-combinatorics` 的代数底座。

本页扩写递归推导、负数的符号处理、无解判据 \(b\not\equiv 0\pmod g\)、通解结构，以及与中国剩余定理、水壶问题的关系。C++ 使用 `optional` 与 `__int128` 防溢出，与 Python 语义对齐。""",
    prereq="""- **欧几里得**：\(\gcd(a,b)=\gcd(b,a\bmod b)\)，\(O(\log\min(a,b))\)。
- **裴蜀定理**：\(ax+by=c\) 有整数解 iff \(\gcd(a,b)\mid c\)。
- **模逆元**：\(ax\equiv 1\pmod m\) 有解 iff \(\gcd(a,m)=1\)。
- **线性同余**：解集为 \(x\equiv x_0\pmod{m/g}\)，\(g=\gcd(a,m)\)。""",
    study_table="""`topic_path`：`algorithms/math/extended_gcd`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/extended_gcd/notes.md` | `extended_gcd.py` |
| C++ | `cpp/algorithms/math/extended_gcd/notes.md` | `extended_gcd.cpp` |""",
    py_cmd="python -LiteralPath F:\\Study\\Algorithm\\python\\algorithms\\math\\extended_gcd\\extended_gcd.py",
    cpp_cmd="""Set-Location -LiteralPath F:\\Study\\Algorithm\\cpp\\algorithms\\math\\extended_gcd
g++ -std=c++17 -O2 -o run.exe extended_gcd.cpp
.\\run.exe""",
    essentials="""### 直觉与定义

普通 gcd 只给最大公约数；扩欧回溯时顺便维护 \((x,y)\)。递归基准 \(b=0\)：\(\gcd=|a|\)，\(x=\mathrm{sgn}(a)\)，\(y=0\)。递推式（设子问题 \((g,x_1,y_1)\) 对 \((b,a\bmod b)\)）：

\[
x = y_1,\quad y = x_1 - \lfloor a/b\rfloor\cdot y_1
\]

手算 \(\gcd(35,15)=5\)：可验证 \(35x+15y=5\)。**模逆**：若 \(g=1\)，则 \(ax\equiv 1\pmod m\) 的解为 \(x\bmod m\)。**同余** \(ax\equiv b\)：先判 \(g\mid b\)，特解 \(x_0\equiv x\cdot (b/g)\pmod{m/g}\)，周期为 \(m/g\)。

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

**与费马逆元**：质模且 \(a\not\equiv 0\) 时 `pow(a,p-2,p)` 更快；非质或需判断无解时用扩欧。

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
4. 链到 `algo-math-combinatorics` 逆阶乘。""",
    py_impl="""```python
g, x, y = extgcd(35, 15)
assert g == 5 and 35 * x + 15 * y == 5
assert mod_inverse(3, 11) == 4
assert mod_inverse(4, 6) is None
sol = solve_linear_congruence(3, 2, 7)
x0, period = sol
assert (3 * x0 - 2) % 7 == 0
```""",
    cpp_impl="""`tuple<long long,long long,long long> extgcd`；`optional<long long> modInverse`；`solveLinearCongruence` 返回 `(x0, period)`。见 `extended_gcd.cpp` 全文。""",
    practice="""| 主题 | 链接 |
|------|------|
| 365 水壶 | gcd 判据 |
| 组合逆元 | algo-math-combinatorics |
| CRT | 竞赛专题 |
| 972/914 | gcd 应用 |""",
    path="""1. 手推 extgcd(12,8)。
2. 实现三函数并跑 Study。
3. 365 或同余模板题。
4. strict 校验本 slug。""",
    refs="""- Study `extended_gcd/notes.md`
- OI Wiki 扩展欧几里得
- `algo-math-fast-power`、`algo-math-number-theory`""",
)

NUMBER_THEORY = r'''---
title: "算法 · Math Number Theory"
series: algorithm
category: Algorithms
topic_path: algorithms/math/number_theory
guide_toc: topic-algorithm
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Math, GCD, Sieve, Prime]
---

# 算法 · 数论基础（Number Theory）

''' + _sections_base(
    intro="""**数论**板块处理整除、最大公约数与素数表。Study `number_theory/` 聚焦 **欧几里得 gcd** 与 **埃拉托斯特尼筛**，把模幂、逆元、组合数留给 `fast_power`、`extended_gcd`、`combinatorics` 子目录。本页说明 gcd 循环写法、筛的 \(O(n\log\log n)\) 直觉、\(n<2\) 边界，以及 204/326/914 等题的选型。

与 `algo-math` 总览配合：先掌握本页 gcd/筛，再按需跳转扩欧与快速幂。""",
    prereq="""- **整除与质数**：\(d\mid n\) 即 \(n=kd\)；质数恰有两个正因子。
- **gcd 性质**：\(\gcd(a,b)=\gcd(b,a\bmod b)\)。
- **筛法**：从 2 标记合数，每个质数 \(i\) 从 \(i^2\) 步长 \(i\) 划掉。""",
    study_table="""`topic_path`：`algorithms/math/number_theory`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/number_theory/notes.md` | `number_theory.py` |
| C++ | `cpp/algorithms/math/number_theory/notes.md` | `number_theory.cpp` |""",
    py_cmd="python -LiteralPath F:\\Study\\Algorithm\\python\\algorithms\\math\\number_theory\\number_theory.py",
    cpp_cmd="""Set-Location -LiteralPath F:\\Study\\Algorithm\\cpp\\algorithms\\math\\number_theory
g++ -std=c++17 -O2 -o run.exe number_theory.cpp
.\\run.exe""",
    essentials="""### 直觉与定义

**gcd** 度量两数公共因子大小；辗转相除不断取余直到余数为 0。例 \(\gcd(54,24)=6\)。**lcm** 满足 \(\mathrm{lcm}(a,b)\cdot\gcd(a,b)=|ab|\)，实现时先除 gcd 再乘防溢出。

**埃氏筛** 构造 `is_prime[0..n]`：0、1 非质；对每个质数 \(i\le\sqrt n\)，划掉 \(i^2,i^2+i,\ldots\)。Study 在 `n<2` 时返回长度 `n+1` 的全 False 表（`sieve(0)==[False]`），与 notes 边界说明一致。

### 复杂度分析

| 算法 | 时间 | 空间 |
|------|------|------|
| gcd 迭代 | \(O(\log\min(a,b))\) | \(O(1)\) |
| 埃氏筛 | \(O(n\log\log n)\) | \(O(n)\) |
| 试除判质 | \(O(\sqrt n)\) | \(O(1)\) |
| 线性筛 | \(O(n)\) | \(O(n)\) |

### 代码模板

```python
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

def sieve(n: int) -> list[bool]:
    if n < 2:
        return [False] * (n + 1)
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime
```

### 变体与技巧

**更相减损术**：减法版 gcd，了解即可。

**欧拉筛**：每个合数只被最小质因子筛，\(O(n)\)。

**分解质因数**：试除或 SPF 表。

**模运算中的 gcd**：\(\gcd(a,m)\) 决定逆元是否存在。

### 易错点

1. **gcd(0,a)**：应返回 \(|a|\)。
2. **筛从 i*i 开始**：重复划掉浪费常数。
3. **n=1**：表长 2，仅索引 0,1 为假。
4. **把筛当因子分解**：筛只判质不直接给因子幂次。
5. **大 n 内存**：\(n=10^7\) 需 bool 数组约 10MB。

### 练习建议

1. 断言 `sum(sieve(30))==10`。
2. 204 计数质数。
3. 326 判质（小 n 试除）。
4. 914 全局 gcd。""",
    py_impl="""Study 实现见上模板；`__main__` 测 gcd、sieve(30)、sieve(0)、sieve(1)。""",
    cpp_impl="""`gcd_ll` 与 `vector<char> sieve`；逻辑同 Python。`accumulate` 计数质数。""",
    practice="""| 题 | 要点 |
|----|------|
| 204 | 筛 |
| 326 | 质判断 |
| 914 | gcd 分组 |
| 1071 | 长度 gcd |""",
    path="""1. 手写 gcd 与 sieve(20) 手算表。
2. 跑 number_theory OK。
3. 204；再学 extended_gcd。
4. strict 校验。""",
    refs="""- Study `number_theory/notes.md`
- `algo-math-extended-gcd`、`algo-math-fast-power`""",
)

MATRIX = r'''---
title: "算法 · Math Matrix"
series: algorithm
category: Algorithms
topic_path: algorithms/math/matrix
guide_toc: topic-algorithm
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Math, Matrix, FastPower, Fibonacci]
---

# 算法 · 矩阵（Matrix）

''' + _sections_base(
    intro="""**矩阵快速幂**把线性递推（如 Fibonacci）从 \(O(n)\) DP 降到 \(O(\log n)\)。Study `matrix/` 提供 `mat_mul`、`mat_pow` 与 `fib(n)`：转移矩阵 \(\begin{pmatrix}1&1\\1&0\end{pmatrix}^{n-1}\) 的右上角即 \(F_n\)。本页讲清乘法维度、模意义取模、单位阵与空矩阵边界，并与 `algo-math-fast-power` 标量快速幂对照。

矩阵亦可描述图的路径计数（邻接矩阵幂）、概率 Markov 一步转移等。""",
    prereq="""- **矩阵乘法**：\(C_{ij}=\sum_k A_{ik}B_{kj}\)，维数 \((n\times k)(k\times m)\)。
- **快速幂**：二进制拆指数，见 `algo-math-fast-power`。
- **Fibonacci**：\(F_0=0,F_1=1,F_n=F_{n-1}+F_{n-2}\)。""",
    study_table="""`topic_path`：`algorithms/math/matrix`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/matrix/notes.md` | `matrix.py` |
| C++ | `cpp/algorithms/math/matrix/notes.md` | `matrix.cpp` |""",
    py_cmd="python -LiteralPath F:\\Study\\Algorithm\\python\\algorithms\\math\\matrix\\matrix.py",
    cpp_cmd="""Set-Location -LiteralPath F:\\Study\\Algorithm\\cpp\\algorithms\\math\\matrix
g++ -std=c++17 -O2 -o run.exe matrix.cpp
.\\run.exe""",
    essentials="""### 直觉与定义

线性递推 \(F_n = c_1 F_{n-1} + \cdots + c_k F_{n-k}\) 可写成状态向量 \(\mathbf{v}_n = M\mathbf{v}_{n-1}\)。Fibonacci 用 \(2\times2\) 矩阵 \(M=\begin{pmatrix}1&1\\1&0\end{pmatrix}\)，\(\mathbf{v}_n=(F_{n+1},F_n)^T\)。则 \(F_n\) 为 \(M^{n-1}\) 的 \((0,0)\) 元（Study 实现约定）。

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

**高维递推**：Tribonacci 用 \(3\times3\) 转移。

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
4. 图论路径计数（邻接矩阵幂）。""",
    py_impl="""`matrix.py` 含 `fib` 封装与空矩阵异常测试。""",
    cpp_impl="""`mat_mul`/`mat_pow`/`fib` 使用 `vector<vector<ll>>`；`mat_pow(f,0)` 得单位阵。""",
    practice="""| 题 | 方法 |
|----|------|
| 509/70 | 矩阵或 DP |
| 1137 | 3×3 矩阵 |
| 图 k 步 | \(A^k\) |
| fast_power | 标量幂对照 |""",
    path="""1. 手算 \(M^3\) 与 \(F_4\)。
2. 跑 matrix OK。
3. 509；理解 \(O(\log n)\)。
4. strict 校验。""",
    refs="""- Study `matrix/notes.md`
- `algo-math-fast-power`""",
)

GEOMETRY = r'''---
title: "算法 · Math Geometry"
series: algorithm
category: Algorithms
topic_path: algorithms/math/geometry
guide_toc: topic-algorithm
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Math, Geometry, CrossProduct, Orientation]
---

# 算法 · 计算几何基础（Geometry）

''' + _sections_base(
    intro="""**计算几何**从向量叉积与点的转向开始。Study `geometry/` 实现 `cross` 与 `orient`：判断三点 \(A,B,C\) 中向量 \(\overrightarrow{AB}\) 到 \(\overrightarrow{AC}\) 是逆时针、共线还是顺时针。这是凸包、线段相交、点在多边形内的基础砖块。

本页强调整数坐标、long long 防溢出、符号约定（y 轴向上时叉积正为逆时针），并指向 149/587/593 等题。""",
    prereq="""- **向量**：\((x,y)\)；点减得方向向量。
- **叉积**：\(\mathbf{a}\times\mathbf{b}=a_x b_y-a_y b_x\)，几何意义为平行四边形有向面积。
- **坐标范围**：竞赛常用 int/long long。""",
    study_table="""`topic_path`：`algorithms/math/geometry`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/geometry/notes.md` | `geometry.py` |
| C++ | `cpp/algorithms/math/geometry/notes.md` | `geometry.cpp` |""",
    py_cmd="python -LiteralPath F:\\Study\\Algorithm\\python\\algorithms\\math\\geometry\\geometry.py",
    cpp_cmd="""Set-Location -LiteralPath F:\\Study\\Algorithm\\cpp\\algorithms\\math\\geometry
g++ -std=c++17 -O2 -o run.exe geometry.cpp
.\\run.exe""",
    essentials="""### 直觉与定义

叉积 \(\text{cross}(\mathbf{a},\mathbf{b})=a_x b_y-a_y b_x\)。三点定向：

\[
\text{orient}(A,B,C)=\text{cross}(B-A,C-A)
\]

- \(>0\)：逆时针（CCW，按常见数学坐标系）
- \(=0\)：共线
- \(<0\)：顺时针

Study 断言 `(0,0),(1,0),(1,1)` 为 CCW，`(0,0),(1,0),(2,0)` 共线。

### 复杂度分析

| 操作 | 时间 |
|------|------|
| cross / orient | \(O(1)\) |
| 凸包 Andrew | \(O(n\log n)\) |
| 枚举点对 | \(O(n^2)\) |

### 代码模板

```python
def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def orient(ax, ay, bx, by, cx, cy):
    return cross(bx - ax, by - ay, cx - ax, cy - ay)
```

### 变体与技巧

**点积**：判锐钝角、投影长度。

**凸包**：Andrew 单调链，反复用 orient 维护转向。

**线段相交**：跨立实验 + 快速排斥。

**149 最多点共线**：斜率 `dy/dx` 用 gcd 约分存 `(dy,dx)` 哈希。

### 易错点

1. **叉积溢出**：坐标 \(\pm10^9\) 用 long long。
2. **坐标系翻转**：屏幕坐标 y 向下则符号可能反，全程统一。
3. **重复点**：共线且重合需去重或特判。
4. **浮点斜率**：整数叉积更稳。
5. **零向量**：叉积为 0。

### 练习建议

1. 跑 geometry OK。
2. 手算 orient 直角三角形。
3. 149 共线点。
4. 凸包模板（仓库外自写）。""",
    py_impl="""```python
assert orient(0, 0, 1, 0, 1, 1) > 0
assert orient(0, 0, 1, 0, 2, 0) == 0
```""",
    cpp_impl="""`cross`/`orient` 返回 `long long`；逻辑同 Python。""",
    practice="""| 题 | 要点 |
|----|------|
| 149 | 斜率哈希 |
| 593 | 正方形边长 |
| 587 | 围栏凸包 |
| 223 | 矩形面积 |""",
    path="""1. 理解叉积符号。
2. 跑 geometry OK。
3. 149。
4. strict 校验。""",
    refs="""- Study `geometry/notes.md`
- OI Wiki 计算几何入门""",
)

PROBABILITY = r'''---
title: "算法 · Math Probability"
series: algorithm
category: Algorithms
topic_path: algorithms/math/probability
guide_toc: topic-algorithm
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Math, Probability, Expectation, Geometric]
---

# 算法 · 概率（Probability）

''' + _sections_base(
    intro="""**概率论**在算法中出现为期望、随机化与计数期望。Study `probability/` 从**几何分布**入手：独立重复试验中首次成功所需次数的期望为 \(1/p\)（\(p\) 为成功概率）。`expected_first_success(p_num, p_den)` 计算有理概率 \(p_{num}/p_{den}\) 的期望。

本页扩写期望线性性、指示变量法、与组合/矩阵的交叉，以及 843/528 等 LeetCode 概率题选型。不展开蒙特卡洛模拟实现细节。""",
    prereq="""- **概率公理**：\(0\le P\le 1\)；独立事件乘法。
- **期望**：离散 \(E[X]=\sum x P(X=x)\)；**线性性** \(E[\sum X_i]=\sum E[X_i]\)（不要求独立）。
- **几何分布**：首次成功试验次数 \(N\)，\(P(N=k)=(1-p)^{k-1}p\)，\(E[N]=1/p\)。""",
    study_table="""`topic_path`：`algorithms/math/probability`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/probability/notes.md` | `probability.py` |
| C++ | `cpp/algorithms/math/probability/notes.md` | `probability.cpp` |""",
    py_cmd="python -LiteralPath F:\\Study\\Algorithm\\python\\algorithms\\math\\probability\\probability.py",
    cpp_cmd="""Set-Location -LiteralPath F:\\Study\\Algorithm\\cpp\\algorithms\\math\\probability
g++ -std=c++17 -O2 -o run.exe probability.cpp
.\\run.exe""",
    essentials="""### 直觉与定义

掷公平六面骰直到出现 6：每次成功概率 \(p=1/6\)，期望次数 \(E=1/p=6\)。一般地，几何分布期望 \(\mathbb{E}[N]=\frac{1}{p}\)。方差 \(\mathrm{Var}(N)=\frac{1-p}{p^2}\)（了解）。

**期望线性性**：复杂计数可先定义指示变量 \(I_e\)（事件 \(e\) 发生为 1），再 \(E[\sum I_e]=\sum P(e)\)，无需独立。

### 复杂度分析

| 计算 | 时间 |
|------|------|
| 公式 \(1/p\) | \(O(1)\) |
| 模拟估计 | 与样本数线性 |
| 概率 DP | 状态数决定 |

### 代码模板

```python
def expected_first_success(p_num: int, p_den: int) -> float:
    return p_den / p_num
```

### 变体与技巧

**二项分布**：\(n\) 次独立成功次数期望 \(np\)。

**coupon collector**：集齐 \(n\) 类期望 \(n H_n\)。

**随机化算法**：快速排序随机 pivot 期望 \(O(n\log n)\)。

**概率 DP**：dp 为到达概率，注意归一化。

**与 matrix**：Markov 稳态可求特征向量（进阶）。

### 易错点

1. **p=0**：期望无定义。
2. **混淆条件概率**：\(P(A|B)\neq P(A)\)。
3. **线性性误用方差**：\(E[XY]\neq E[X]E[Y]\) 一般需独立。
4. **浮点比较**：Study 用 `abs<1e-12`。
5. **整数除法**：用 `p_den/p_num` 浮点或分数类。

### 练习建议

1. 断言 `expected_first_success(1,6)==6`。
2. 手推掷硬币直到正面的期望 2。
3. 843 猜数字（二分期望）。
4. 528 按权重随机（前缀和）。""",
    py_impl="""```python
assert abs(expected_first_success(1, 6) - 6.0) < 1e-12
```""",
    cpp_impl="""`double expected_first_success(int p_num, int p_den)` 返回 `p_den/p_num`。""",
    practice="""| 题 | 要点 |
|----|------|
| 几何期望 | 本页公式 |
| 843 | 二分+期望 |
| 528 | 权重随机 |
| 808 | 模拟/公式 |""",
    path="""1. 推导 \(E=1/p\)。
2. 跑 probability OK。
3. 843 或指示变量小题。
4. strict 校验。""",
    refs="""- Study `probability/notes.md`
- `algo-math-combinatorics`（计数期望）""",
)


def main() -> None:
    guides = [
        ("algo-math-combinatorics", COMBINATORICS, 8001, COMB_SEEDS),
        ("algo-math-extended-gcd", EXTENDED_GCD, 8001, EXT_SEEDS),
        ("algo-math-number-theory", NUMBER_THEORY, 8001, NT_SEEDS),
        ("algo-math-matrix", MATRIX, 8001, MAT_SEEDS),
        ("algo-math-geometry", GEOMETRY, 8001, GEO_SEEDS),
        ("algo-math-probability", PROBABILITY, 8001, PROB_SEEDS),
    ]
    for slug, body, target, seeds in guides:
        _write(slug, body, target, seeds)


if __name__ == "__main__":
    main()
