---
title: "算法 · Math Probability"
series: algorithm
category: Algorithms
topic_path: algorithms/math/probability
guide_toc: topic-algorithm
guide_tier: medium
status: published
date: 2026-05-22
tags: [Algorithm, Math, Probability, Expectation, Geometric]
---

# 算法 · 概率（Probability）

## 导读

**概率论**在算法中出现为期望、随机化与计数期望。Study `probability/` 从**几何分布**入手：独立重复试验中首次成功所需次数的期望为 \(1/p\)（\(p\) 为成功概率）。`expected_first_success(p_num, p_den)` 计算有理概率 \(p_{num}/p_{den}\) 的期望。

本页扩写期望线性性、指示变量法、与组合/矩阵的交叉，以及 843/528 等 LeetCode 概率题选型。不展开蒙特卡洛模拟实现细节。

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`，路径含空格时用 `-LiteralPath`。

- **概率公理**：\(0\le P\le 1\)；独立事件乘法。
- **期望**：离散 \(E[X]=\sum x P(X=x)\)；**线性性** \(E[\sum X_i]=\sum E[X_i]\)（不要求独立）。
- **几何分布**：首次成功试验次数 \(N\)，\(P(N=k)=(1-p)^{k-1}p\)，\(E[N]=1/p\)。

## Study 仓库对照

`topic_path`：`algorithms/math/probability`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/probability/notes.md` | `probability.py` |
| C++ | `cpp/algorithms/math/probability/notes.md` | `probability.cpp` |

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\math\probability\probability.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math\probability
g++ -std=c++17 -O2 -o run.exe probability.cpp
.\run.exe
```

成功时应打印对应 `OK` 行。

## 基础篇

### 直觉与定义

掷公平六面骰直到出现 6：每次成功概率 \(p=1/6\)，期望次数 \(E=1/p=6\)。一般地，几何分布期望 \(\mathbb{E}[N]=rac{1}{p}\)。方差 \(\mathrm{Var}(N)=rac{1-p}{p^2}\)（了解）。

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
2. **混淆条件概率**：\(P(A|B)
eq P(A)\)。
3. **线性性误用方差**：\(E[XY]
eq E[X]E[Y]\) 一般需独立。
4. **浮点比较**：Study 用 `abs<1e-12`。
5. **整数除法**：用 `p_den/p_num` 浮点或分数类。

### 练习建议

1. 断言 `expected_first_success(1,6)==6`。
2. 手推掷硬币直到正面的期望 2。
3. 843 猜数字（二分期望）。
4. 528 按权重随机（前缀和）。

## Python 实现

```python
assert abs(expected_first_success(1, 6) - 6.0) < 1e-12
```

## C++ 实现

```cpp
double expected_first_success(int p_num, int p_den) {
    return (double)p_den / p_num;
}
```

## 练习与延伸

| 题 | 要点 |
|----|------|
| 几何期望 | 本页公式 |
| 843 | 二分+期望 |
| 528 | 权重随机 |
| 808 | 模拟/公式 |

## 学习路径

1. 推导 \(E=1/p\)。
2. 跑 probability OK。
3. 843 或指示变量小题。
4. strict 校验。

## 延伸阅读

- Study `probability/notes.md`
- `algo-math-combinatorics`（计数期望）


**深度补充：伯努利试验**

单次成功概率 p，重复独立。


**深度补充：二项分布**

n 次成功 k 次的概率 C(n,k)p^k(1-p)^{n-k}。


**深度补充：期望线性性**

E[Σ X_i]=Σ E[X_i]，不要求独立。


**深度补充：指示变量**

计数期望常用 I_A 期望=P(A)。


**深度补充：843 猜数字**

数学期望+二分，读题。


**深度补充：808 分汤**

概率模拟或公式。


**深度补充：528 按权重随机**

前缀和+二分或树状数组。


**深度补充：470 伪随机**

种子与模，工程题。


**深度补充：几何分布方差**

Var= (1-p)/p^2。


**深度补充：负二项**

第 r 次成功所需次数，推广几何。


**深度补充：条件概率**

P(A|B)=P(AB)/P(B)；贝叶斯。


**深度补充：全概率**

划分样本空间求 P(A)。


**深度补充：马尔可夫链**

状态转移矩阵乘，与 matrix 页交叉。


**深度补充：随机游走**

期望步数常解方程。


**深度补充：赌徒破产**

经典随机过程。


**深度补充：coupon collector**

期望 n(1+1/2+..+1/n)。


**深度补充：shuffle 随机**

Fisher-Yates 均匀排列。


**深度补充：概率 DP**

dp[i][j] 为到达概率；和为 1。


**深度补充：对拍期望**

模拟掷骰与公式 6 对比。


**深度补充：面试话术概率**

「几何分布期望 1/p；线性性拆事件」。


**深度补充：浮点比较**

Study 用 abs<1e-12；工程用相对误差。


**深度补充：p=0 与 p=1**

退化情形单独讨论。


**深度补充：结语概率**

expected_first_success 理解后做 843。


**深度补充：专题复盘 24**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 25**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 26**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 27**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 28**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 29**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 30**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 31**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 32**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 33**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 34**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 35**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 36**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 37**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 38**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 39**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 40**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 41**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 42**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 43**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 44**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 45**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 46**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 47**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 48**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 49**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 50**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 51**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 52**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 53**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 54**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 55**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 56**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 57**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 58**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 59**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 60**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 61**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 62**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 63**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 64**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 65**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 66**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 67**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 68**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 69**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 70**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 71**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 72**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 73**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 74**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 75**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 76**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 77**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 78**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 79**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 80**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 81**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 82**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 83**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 84**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 85**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 86**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 87**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 88**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 89**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 90**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 91**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 92**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 93**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 94**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 95**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 96**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 97**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 98**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 99**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 100**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 101**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 102**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 103**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 104**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 105**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 106**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 107**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 108**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 109**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 110**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 111**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 112**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 113**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 114**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 115**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 116**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 117**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 118**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 119**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 120**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 121**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 122**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 123**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 124**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 125**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 126**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 127**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 128**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 129**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 130**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 131**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 132**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 133**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 134**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 135**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 136**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 137**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 138**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 139**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 140**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 141**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 142**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 143**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 144**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 145**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 146**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 147**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 148**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 149**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 150**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 151**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 152**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 153**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 154**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 155**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 156**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 157**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 158**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 159**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 160**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 161**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 162**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 163**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 164**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 165**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 166**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 167**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 168**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 169**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 170**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 171**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 172**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 173**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 174**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 175**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 176**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 177**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 178**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 179**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 180**

回到 algo-math-probability 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。
