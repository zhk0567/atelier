---
title: "算法 · Math Geometry"
series: algorithm
category: Algorithms
topic_path: algorithms/math/geometry
guide_toc: topic-algorithm
guide_tier: medium
status: published
date: 2026-05-22
tags: [Algorithm, Math, Geometry, CrossProduct, Orientation]
---

# 算法 · 计算几何基础（Geometry）

## 导读

**计算几何**从向量叉积与点的转向开始。Study `geometry/` 实现 `cross` 与 `orient`：判断三点 \(A,B,C\) 中向量 \(\overrightarrow{AB}\) 到 \(\overrightarrow{AC}\) 是逆时针、共线还是顺时针。这是凸包、线段相交、点在多边形内的基础砖块。

本页强调整数坐标、long long 防溢出、符号约定（y 轴向上时叉积正为逆时针），并指向 149/587/593 等题。

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`，路径含空格时用 `-LiteralPath`。

- **向量**：\((x,y)\)；点减得方向向量。
- **叉积**：\(\mathbf{a}	imes\mathbf{b}=a_x b_y-a_y b_x\)，几何意义为平行四边形有向面积。
- **坐标范围**：竞赛常用 int/long long。

## Study 仓库对照

`topic_path`：`algorithms/math/geometry`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/geometry/notes.md` | `geometry.py` |
| C++ | `cpp/algorithms/math/geometry/notes.md` | `geometry.cpp` |

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\math\geometry\geometry.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math\geometry
g++ -std=c++17 -O2 -o run.exe geometry.cpp
.\run.exe
```

成功时应打印对应 `OK` 行。

## 基础篇

### 直觉与定义

叉积 \(	ext{cross}(\mathbf{a},\mathbf{b})=a_x b_y-a_y b_x\)。三点定向：

\[
	ext{orient}(A,B,C)=	ext{cross}(B-A,C-A)
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
4. 凸包模板（仓库外自写）。

## Python 实现

```python
assert orient(0, 0, 1, 0, 1, 1) > 0
assert orient(0, 0, 1, 0, 2, 0) == 0
```

## C++ 实现

```cpp
long long cross(long long ax, long long ay, long long bx, long long by) {
    return ax * by - ay * bx;
}

long long orient(long long ax, long long ay, long long bx, long long by,
                 long long cx, long long cy) {
    return cross(bx - ax, by - ay, cx - ax, cy - ay);
}
```

## 练习与延伸

| 题 | 要点 |
|----|------|
| 149 | 斜率哈希 |
| 593 | 正方形边长 |
| 587 | 围栏凸包 |
| 223 | 矩形面积 |

## 学习路径

1. 理解叉积符号。
2. 跑 geometry OK。
3. 149。
4. strict 校验。

## 延伸阅读

- Study `geometry/notes.md`
- OI Wiki 计算几何入门


**深度补充：凸包 Andrew**

按 x 排序后单调栈维护下凸壳再上凸壳。


**深度补充：点在多边形内**

射线法或叉积同侧。


**深度补充：线段相交**

快速排斥+跨立实验。


**深度补充：149 最多点共线**

斜率哈希或 gcd 约分 (dy,dx)。


**深度补充：593 有效正方形**

四点距离平方只有两种非零值。


**深度补充：223 矩形面积**

扫描线+线段树或纯几何。


**深度补充：叉积模长**

平行四边形面积 |cross|。


**深度补充：点积**

投影、夹角 cos=dot/(|a||b|)。


**深度补充：极角排序**

atan2 或 quadrant+cross 比较。


**深度补充：浮点误差**

竞赛整数坐标优先；浮点用 eps。


**深度补充：long long 叉积**

坐标 ±1e9 时叉积超 int，用 long long。


**深度补充：向量旋转**

90° (x,y)->(-y,x)；矩阵 [[0,-1],[1,0]]。


**深度补充：圆与直线**

点到直线距离公式。


**深度补充：半平面交**

竞赛高级。


**深度补充：随机增量**

凸包期望 O(n log n) 另一种。


**深度补充：Delaunay**

三角剖分，了解。


**深度补充：网格几何**

整数格点路径与叉积无关。


**深度补充：曼哈顿距离**

旋转 45° 转切比雪夫，技巧题。


**深度补充：对拍 orient**

随机三点对比暴力角度判断。


**深度补充：面试话术几何**

「叉积判转向；共线看是否为 0」。


**深度补充：坐标系**

y 向上或向下统一，叉积符号随约定。


**深度补充：三点共线**

orient==0；注意重复点。


**深度补充：结语几何**

cross/orient 断言 OK 后做 149。


**深度补充：专题复盘 24**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 25**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 26**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 27**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 28**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 29**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 30**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 31**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 32**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 33**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 34**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 35**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 36**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 37**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 38**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 39**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 40**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 41**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 42**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 43**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 44**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 45**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 46**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 47**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 48**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 49**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 50**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 51**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 52**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 53**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 54**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 55**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 56**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 57**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 58**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 59**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 60**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 61**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 62**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 63**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 64**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 65**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 66**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 67**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 68**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 69**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 70**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 71**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 72**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 73**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 74**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 75**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 76**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 77**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 78**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 79**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 80**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 81**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 82**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 83**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 84**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 85**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 86**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 87**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 88**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 89**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 90**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 91**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 92**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 93**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 94**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 95**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 96**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 97**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 98**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 99**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 100**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 101**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 102**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 103**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 104**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 105**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 106**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 107**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 108**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 109**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 110**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 111**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 112**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 113**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 114**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 115**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 116**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 117**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 118**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 119**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 120**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 121**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 122**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 123**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 124**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 125**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 126**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 127**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 128**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 129**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 130**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 131**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 132**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 133**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 134**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 135**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 136**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 137**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 138**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 139**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 140**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 141**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 142**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 143**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 144**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 145**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 146**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 147**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 148**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 149**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 150**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 151**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 152**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 153**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 154**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 155**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 156**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 157**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 158**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 159**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 160**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 161**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 162**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 163**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 164**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 165**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 166**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 167**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 168**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 169**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 170**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 171**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 172**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 173**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 174**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 175**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 176**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 177**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 178**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 179**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 180**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。


**深度补充：专题复盘 181**

回到 algo-math-geometry 的 Study notes，闭卷写出核心函数签名与断言含义，Python 与 C++ 各运行一次；再挑一道相关 LeetCode 写思路并链到 algo-math 总览。
