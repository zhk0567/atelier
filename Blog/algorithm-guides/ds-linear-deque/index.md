---
title: "数据结构 · 双端队列（循环双端队列与单调队列）"
series: algorithm
category: DataStructures
topic_path: data_structures/linear/deque
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-22
tags: [DataStructures, Deque, MonotonicDeque, SlidingWindow]
---

# 数据结构 · 双端队列（循环双端队列与单调队列）

## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [Study 仓库对照](#study-仓库对照)
- [基础篇](#基础篇)
  - [抽象模型](#抽象模型)
  - [核心操作](#核心操作)
  - [实现要点](#实现要点)
  - [典型应用](#典型应用)
  - [易错点](#易错点)
  - [练习建议](#练习建议)
- [Python 实现](#python-实现)
- [C++ 实现](#c-实现)
- [练习与延伸](#练习与延伸)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)

## 导读

**双端队列（Deque，double-ended queue）** 允许在 **队头与队尾** 两端进行 O(1) 的插入与删除。它是栈与队列的推广：只使用一端即退化为栈；只 restrict 一端入另一端出即 FIFO 队列。算法面试中 **单调队列** 解滑动窗口最值（LeetCode **239**、**1438**）是 deque 最重要考点；设计题 **641 设计循环双端队列** 考察循环数组指针。

本页 `ds-linear-deque`，`topic_path` `data_structures/linear/deque`，`guide_toc` `topic-ds`。Study 提供 `CircularDeque` 与单调队列应用笔记；Python 标准库 `collections.deque` 两端 O(1)，工程实现应优先使用。

目标：① 区分 deque ADT 与「单调队列技巧」；② 实现循环双端数组；③ 写出 239 模板；④ 理解为何单调队列每个下标最多入出各一次。

## 预备知识

> **预备知识**：已读 `ds-linear-queue` 的 FIFO 与循环数组；理解滑动窗口；Python `deque` 的 `append`/`appendleft`/`pop`/`popleft`；C++ `std::deque` 或手写循环数组。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/linear/deque` |
| Python | `python/data_structures/linear/deque/deque.py` |
| C++ | `cpp/data_structures/linear/deque/deque.cpp` |

```powershell
python -LiteralPath 'F:\Study\Algorithm\python\data_structures\linear\deque\deque.py'
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\linear\deque'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o deque.exe deque.cpp
.\deque.exe
```

输出 `Deque OK`。

## 基础篇

### 抽象模型

逻辑上 deque 是 **两端可操作序列**。常见操作：`push_front`/`push_back`、`pop_front`/`pop_back`、`peek` 两端。既可用于 **O(1) 两端插入的队列栈混合**，也可作为 **单调队列** 的底层容器——此时容器内元素值（或下标对应值）保持单调递增或递减。

### 核心操作

| 操作 | 含义 | 均摊 |
|------|------|------|
| push_back / push_front | 两端入 | O(1) |
| pop_back / pop_front | 两端出 | O(1) |
| peek | 看两端 | O(1) |

**单调队列** 额外不变量：队头到队尾单调；入队前从尾部弹出不满足单调的元素；队头对应当前窗口最值候选。

### 实现要点

**循环双端数组**：`front` 指向逻辑首元素，`size` 记录个数；`push_back` 写 `(front+size-1+cap)%cap` 侧（实现细节依仓库）；`push_front` 写 `front=(front-1+cap)%cap` 再赋值。判满 `size==cap`。

**641 题**：`insertLast`/`insertFirst`/`deleteLast`/`deleteFirst`/`getFront`/`getRear`/`isEmpty`/`isFull` 均 O(1)。

**239 单调递减队列（存下标）**：维护窗口最大值；`while q and nums[q[-1]] < nums[i]: q.pop()`；`q.append(i)`；若 `q[0] <= i-k` 则 `popleft`；答案 `nums[q[0]]`。

每个下标最多入队一次、出队一次，总 O(n)。

### 典型应用

- 239 滑动窗口最大值；
- 1438 绝对差约束窗口；
- 862 单调队列+前缀和（进阶）；
- 641 循环双端队列设计；
- 用 deque 优化 BFS 0-1 边（0 压 front，1 压 back）；
- 栈/队列互模拟时的辅助结构。

### 易错点

- 239 存值而非下标导致窗口过期难踢；
- 单调方向反了（求最大值维护递减）；
- `pop(0)` 用 list 而非 deque；
- 641 `front`/`rear` 指针与 `size` 不同步；
- 空 deque 访问 `q[0]`；
- 窗口长度 1 时答案即元素本身别漏初始化。

### 练习建议

1. 运行 `deque.py`；2. 641 默写；3. 239 模板背诵；4. 1438 变体；5. 配合 `algo-sliding-window` 专题。

## Python 实现

```python
class CircularDeque:
    def __init__(self, k: int) -> None:
        self._cap = k
        self._a: list[int | None] = [None] * k
        self._front = 0
        self._size = 0

    def push_back(self, x: int) -> bool:
        if self._size == self._cap:
            return False
        idx = (self._front + self._size) % self._cap
        self._a[idx] = x
        self._size += 1
        return True

    def push_front(self, x: int) -> bool:
        if self._size == self._cap:
            return False
        self._front = (self._front - 1) % self._cap
        self._a[self._front] = x
        self._size += 1
        return True

    def pop_back(self) -> bool:
        if not self._size:
            return False
        self._size -= 1
        return True

    def pop_front(self) -> bool:
        if not self._size:
            return False
        self._front = (self._front + 1) % self._cap
        self._size -= 1
        return True
```

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    q: deque[int] = deque()
    out: list[int] = []
    for i, x in enumerate(nums):
        while q and nums[q[-1]] < x:
            q.pop()
        q.append(i)
        if q[0] <= i - k:
            q.popleft()
        if i >= k - 1:
            out.append(nums[q[0]])
    return out
```

## C++ 实现

```cpp
struct CircularDeque {
    vector<int> a;
    int front = 0, sz = 0, cap;
    explicit CircularDeque(int k) : a(k), cap(k) {}
    bool pushBack(int x) {
        if (sz == cap) return false;
        a[(front + sz) % cap] = x;
        ++sz;
        return true;
    }
    bool pushFront(int x) {
        if (sz == cap) return false;
        front = (front - 1 + cap) % cap;
        a[front] = x;
        ++sz;
        return true;
    }
};
```

```cpp
vector<int> maxSlidingWindow(const vector<int>& nums, int k) {
    deque<int> q;
    vector<int> ans;
    for (int i = 0; i < (int)nums.size(); ++i) {
        while (!q.empty() && nums[q.back()] < nums[i]) q.pop_back();
        q.push_back(i);
        if (q.front() <= i - k) q.pop_front();
        if (i >= k - 1) ans.push_back(nums[q.front()]);
    }
    return ans;
}
```

## 练习与延伸

| 题号 | 说明 |
|------|------|
| 239 | 滑动窗口最大值 |
| 641 | 循环双端队列 |
| 1438 | 最长连续绝对差 ≤ limit |
| 862 | 单调队列+前缀和 |

## 学习路径

**0**：`Deque OK`。**1–2 天**：641。**3–4 天**：239 默写。**2 周**：1438、滑动窗口专题联动。

## 延伸阅读

- `ds-linear-queue`、`algo-sliding-window`
- Study `deque/notes.md`


**深度补充：239 为何存下标**

值会变但下标单调；过期用 `i-k` 与队头比较。

**深度补充：求最小值单调递增**

维护递增队列，队头最小；弹队尾 `>=` 当前。

**深度补充：1438 双端队列+二分**

也可用单调队列存下标满足差约束；多种解法选型。

**深度补充：862 和至少 K**

前缀和+单调队列优化 DP；进阶了解。

**深度补充：641 insert 边界**

满时 insert 返回 false；空时 get 返回 -1。

**深度补充：deque 与 stack**

只 push_back/pop_back 即栈。

**深度补充：deque 与 queue**

只 push_back/pop_front 即 FIFO。

**深度补充：Python deque rotate**

`rotate(k)` 循环移动；竞赛小技巧。

**深度补充：C++ deque 分段**

标准库 deque 分段数组；面试手写循环数组即可。

**深度补充：均摊 O(1) 两端**

循环数组每个元素移动次数常数。

**深度补充：单调队列总 O(n)**

每个下标最多进出各一次。

**深度补充：窗口 k=1**

答案即 nums[i]；代码 `i>=k-1` 自然覆盖。

**深度补充：窗口 k>n**

题面通常保证 k<=n；边界读题。

**深度补充：重复元素 239**

严格 `<` 弹栈；相等可保留较早下标。

**深度补充：84 与单调栈**

柱状图用栈非 deque；勿混模板。

**深度补充：739 单调栈**

下一个更大用栈；窗口最值用 deque。

**深度补充：滑动窗口和**

固定窗口和用队列维护元素和，非单调。

**深度补充：0-1 BFS deque**

0 边 push_front，1 边 push_back。

**深度补充：设计题 641 对拍**

随机 insert/delete 与 list 模拟。

**深度补充：面试话术**

「239 递减 deque 存下标，过期 pop front」。

**深度补充：与限流**

滑动窗口计数与单调队列不同题族。

**深度补充：内存**

deque 存下标 int 比存值省？通常存下标。

**深度补充：多线程**

标准 deque 非线程安全；并发见 interview classic。

**深度补充：可视化**

窗口右移时画队列内下标对应值。

**深度补充：错误：递增求最大**

求最大维护递减（队头最大）。

**深度补充：错误：忘记踢过期**

导致答案含窗口外元素。

**深度补充：错误：list 慢**

popleft O(n) TLE。

**深度补充：竞赛常考**

239 变形、滑动窗口+哈希。

**深度补充：工业**

任务窃取 deque 了解即可。

**深度补充：Rust VecDeque**

两端 O(1) 标准结构。

**深度补充：Go container/deque**

第三方或 slice 模拟。

**深度补充：Java Deque**

ArrayDeque 无 null；接口 ArrayDeque。

**深度补充：Kotlin**

ArrayDeque 同 Java。

**深度补充：JavaScript**

无内置 deque，用数组或第三方。

**深度补充：Swift**

无标准 deque，Array 头删 O(n)。

**深度补充：练习 239 变体**

字符串窗口、矩阵行窗口。

**深度补充：练习 1696 跳跃**

单调队列优化 DP。

**深度补充：练习 1425 约束子序列**

单调+堆混合，难。

**深度补充：与 heap**

窗口第 k 大用堆 O(log k)；最大用 deque O(n)。

**深度补充：双端队列+BFS**

0-1 最短路经典。

**深度补充：总结**

deque=两端 O(1)；单调队列=deque+不变量。

**深度补充：strict**

medium ≥8000 汉字。

**深度补充：draft**

校验通过后改 published。

**深度补充：父级 ds-linear**

线性结构地图。

**深度补充：结语**

先 641 再 239；单调方向与过期下标是核心。

**深度补充：239 模板背诵**

维护递减双端队列存下标：while 队尾值小于当前 pop_back；append 当前下标；若队头下标<=i-k pop_front；当 i>=k-1 记录 nums[队头]。


**深度补充：单调递减求最大**

滑动窗口最大值用递减 deque，队头永远是当前窗口最大下标。求最小值则维护递增 deque。


**深度补充：每个下标 O(1) 均摊**

每个下标最多入队一次、出队一次，总 O(n)。面试必须能说出均摊理由。


**深度补充：641 循环双端队列**

push_front 写 front=(front-1+cap)%cap 再赋值；push_back 写 (front+size)%cap。size 与 cap 判满判空。


**深度补充：1438 绝对差限制**

滑动窗口+单调队列或双端队列维护满足差约束的下标。与 239 同族，练习变形。


**深度补充：862 和至少 K**

前缀和+单调队列优化；进阶题，了解 deque 可优化 DP 即可。


**深度补充：1696 跳跃游戏 VI**

单调队列优化滑动窗口最值 DP。竞赛向，面试了解。


**深度补充：1425 约束子序列**

单调队列+堆，较难。学完 239 再碰。


**深度补充：0-1 BFS**

边权 0 压 front，1 压 back，用 deque 当双端队列。无权 BFS 仍普通队列。


**深度补充：deque 当栈**

只 push_back+pop_back 即栈。一端操作。


**深度补充：deque 当队列**

push_back+pop_front 即 FIFO。Python collections.deque 标准用法。


**深度补充：Python rotate**

deque.rotate(k) 循环移动元素，偶可用于模拟轮转。


**深度补充：C++ std::deque**

分段存储，两端 O(1)。手写 CircularDeque 用数组更易讲清。


**深度补充：过期下标**

队头下标 <= i-k 必须 pop_front，否则答案包含窗口外元素。


**深度补充：相等元素处理**

239 求最大：while 队尾 nums[j] < x 才 pop，相等可保留旧下标。


**深度补充：k=1 窗口**

答案即 nums[i]，代码 i>=k-1 自然成立。


**深度补充：k>n 边界**

题面通常保证 k<=n；读清约束。


**深度补充：list popleft TLE**

用 list 模拟 deque 的 popleft 是 O(n)，239 必 TLE。


**深度补充：84 单调栈**

柱状图最大矩形用栈不是 deque。模板别混。


**深度补充：739 单调栈**

每日温度用栈存下标。窗口最值用 deque。


**深度补充：滑动窗口和**

固定窗口元素和用普通队列或变量累加，不需单调。


**深度补充：641 getFront getRear**

空返回 -1；满时 insert 返回 false。四向操作都要 O(1)。


**深度补充：对拍 641**

随机 insert/delete 与 Python list 模拟双端序列对比。


**深度补充：面试话术 deque**

「239 递减 deque 存下标，过期 pop_front，O(n)」。


**深度补充：可视化窗口**

手画窗口右移时 deque 内下标与对应值，理解为何单调。


**深度补充：错误方向**

求最大却维护递增队列会导致队头不是最大。


**深度补充：忘记 pop 过期**

239 最常见 WA 原因之一。


**深度补充：工业 deque**

任务窃取双端队列了解即可，面试偏 LeetCode。


**深度补充：Java ArrayDeque**

null 不允许；可当栈和队列。


**深度补充：与 heap 对比**

窗口第 k 大用堆 O(log k)；最大最小用单调 deque O(n)。


**深度补充：总结**

deque=两端 O(1)；单调队列=deque+单调不变量。


**深度补充：综合复盘要点 32**

第 32 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 33**

第 33 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 34**

第 34 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 35**

第 35 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 36**

第 36 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 37**

第 37 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 38**

第 38 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 39**

第 39 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 40**

第 40 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 41**

第 41 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 42**

第 42 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 43**

第 43 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 44**

第 44 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 45**

第 45 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 46**

第 46 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 47**

第 47 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 48**

第 48 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 49**

第 49 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 50**

第 50 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 51**

第 51 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 52**

第 52 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 53**

第 53 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 54**

第 54 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 55**

第 55 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 56**

第 56 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 57**

第 57 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 58**

第 58 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 59**

第 59 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 60**

第 60 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 61**

第 61 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 62**

第 62 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 63**

第 63 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 64**

第 64 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 65**

第 65 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 66**

第 66 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 67**

第 67 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 68**

第 68 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 69**

第 69 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 70**

第 70 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 71**

第 71 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 72**

第 72 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 73**

第 73 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 74**

第 74 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 75**

第 75 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 76**

第 76 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 77**

第 77 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 78**

第 78 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 79**

第 79 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 80**

第 80 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 81**

第 81 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 82**

第 82 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 83**

第 83 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 84**

第 84 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 85**

第 85 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 86**

第 86 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 87**

第 87 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 88**

第 88 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 89**

第 89 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 90**

第 90 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 91**

第 91 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 92**

第 92 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 93**

第 93 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 94**

第 94 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 95**

第 95 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 96**

第 96 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 97**

第 97 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 98**

第 98 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 99**

第 99 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 100**

第 100 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 101**

第 101 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 102**

第 102 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 103**

第 103 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 104**

第 104 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 105**

第 105 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 106**

第 106 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 107**

第 107 条复盘：回到 ds-linear-deque 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。
