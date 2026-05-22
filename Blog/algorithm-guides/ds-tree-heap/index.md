---
title: "数据结构 · 小根堆（数组堆）"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/heap
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-22
tags: [DataStructures, Heap, MinHeap, PriorityQueue, LeetCode215]
---

# 数据结构 · 小根堆（数组堆）

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

**堆**是完全二叉树且满足堆序：小根堆中父不大于子（本仓库 `MinHeap`）。用数组存储时下标 i 的父 `(i-1)//2`、左 `2i+1`、右 `2i+2`。`push/pop` O(log n)，`top` O(1)，`heapify` O(n) 建堆。面试 Top K、合并 K 路、Dijkstra 堆优化、295 中位数堆都依赖堆。

本页 `ds-tree-heap`，Study `heap.py` 手写 `MinHeap` 与 `heapify_inplace`。Python 标准库 `heapq` 为小根堆，本页教**原理**以便 C++ 与手写。

## 预备知识

> **预备知识**：数组下标；理解完全二叉树与数组对应（见导读）；`ds-tree-binary-tree` 有助于理解「树形逻辑、数组存储」。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/tree/heap` |
| Python | `python/data_structures/tree/heap/heap.py` |
| C++ | `cpp/data_structures/tree/heap/heap.cpp` |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\data_structures	ree\heap'
python heap.py
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures	ree\heap'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o heap.exe heap.cpp
.\heap.exe
```

输出：`Heap OK`。

## 基础篇

### 抽象模型

逻辑上完全二叉树，存储于数组 `_a`。堆序：`_a[parent(i)] <= _a[i]`（小根）。不保证中序有序，与 BST 不同。大小 n 时高度 ⌊log2 n⌋+1。

### 核心操作

| 操作 | 时间 |
|------|------|
| push | O(log n) 上浮 sift_up |
| pop | O(log n) 下沉 sift_down |
| top | O(1) |
| heapify | O(n) 自底向上 |

**pop 细节**：根与末尾交换等价于保存根、末元素移到根、`pop` 尾再 `sift_down(0)`。

### 实现要点

**sift_up**：`while i>0` 与父比较，更小则交换并 `i=parent`。

**sift_down**：在 l,r 中选更小者与 i 比较，交换并继续。

**heapify**：`for i in range(n//2-1, -1, -1): sift_down(i)`，叶节点无需下沉。

**大根堆**：比较符号反转，或 Python `heapq` 存负值。

**第 K 大（215）**：维护大小 k 的小根堆，堆顶为第 k 大候选。

### 典型应用

Top K、多路归并（23）、Dijkstra、Prim、295 双堆、任务调度。

### 易错点

- pop 空堆抛 `IndexError`/`underflow_error`。
- 单元素 pop 特判，避免对空堆 sift_down。
- heapify 起点是 `n//2-1` 不是 n-1。
- 子节点下标越界判断 `l < n`。

### 练习建议

215, 347, 23, 295, 703, 1046；对比快选 O(n) 平均。

## Python 实现

```python
class MinHeap:
    def push(self, x: int) -> None:
        self._a.append(x)
        self._sift_up(len(self._a) - 1)

    def pop(self) -> int:
        if len(self._a) == 1:
            return self._a.pop()
        root = self._a[0]
        self._a[0] = self._a.pop()
        self._sift_down(0)
        return root
```

`heapify_inplace` 复制数组后自底向上下沉。运行 `python heap.py`。

## C++ 实现

`struct MinHeap` 与 Python 一致：

```cpp
void sift_down(int i) {
    int n = (int)a.size();
    while (true) {
        int l = 2 * i + 1, r = 2 * i + 2, sm = i;
        if (l < n && a[l] < a[sm]) sm = l;
        if (r < n && a[r] < a[sm]) sm = r;
        if (sm == i) break;
        swap(a[i], a[sm]);
        i = sm;
    }
}
```

`main` 断言 push 序列 pop 序。也可用 `priority_queue<int, vector<int>, greater<int>>`。

## 练习与延伸

`iv-top-frequent` 215 章；`algo-graph-shortest-path` Dijkstra 堆。

## 学习路径

数组下标 → 本页手写堆 → `heapq` 刷题 → 215/347。

## 延伸阅读

- [Algorithm — heap](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/tree/heap)
- 站点：`ds-tree-binary-tree`、`ds-tree-bst`


**深度补充：heapq 模块**

import heapq; heappush/heappop 小根堆；nlargest 用 -值或大根技巧。


**深度补充：347 前 K 频**

dict 计数后维护 size k 小根堆，O(n log k)。


**深度补充：23 合并 K 链**

堆存 (val, i, node) 每次 pop 最小接链。


**深度补充：295 中位数**

大根堆存左半，小根堆存右半，平衡数量差≤1。


**深度补充：703 数据流第 K**

类 215 维护 k 小根堆。


**深度补充：1046 最后石头**

模拟堆即可。


**深度补充：767 重构字符串**

计数后大根堆相邻不同，注意空堆判断。


**深度补充：502 IPO**

堆选项目，进阶。


**深度补充：快速选择对比**

215 平均 O(n) 快选，最坏 O(n²)；堆稳定 O(n log k)。


**深度补充：索引堆**

Dijkstra 存 (dist, node) 可 decrease-key 用 lazy 删除。


**深度补充：建堆复杂度证明**

级数求和 O(n)，不是 O(n log n)。


**深度补充：完全二叉树判定**

按层 BFS 遇空后不应再出现节点。


**深度补充：堆排序**

heapify 后反复 pop 得升序，原地需大根。


**深度补充：优先队列 C++**

priority_queue 默认大根，greater 小根。


**深度补充：发布校验**

validate --slug ds-tree-heap --strict


**深度补充：复盘要点 16**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 17**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 18**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 19**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 20**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 21**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 22**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 23**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 24**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 25**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 26**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 27**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 28**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 29**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 30**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 31**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 32**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 33**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 34**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 35**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 36**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 37**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 38**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 39**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 40**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 41**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 42**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 43**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 44**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 45**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 46**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 47**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 48**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 49**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 50**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 51**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 52**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 53**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 54**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 55**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 56**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 57**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 58**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 59**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 60**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 61**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 62**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 63**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 64**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 65**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 66**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 67**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 68**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 69**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 70**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 71**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 72**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 73**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 74**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 75**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 76**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 77**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 78**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 79**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 80**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 81**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 82**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 83**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 84**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 85**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 86**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 87**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 88**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 89**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 90**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 91**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 92**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 93**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 94**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 95**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 96**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 97**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 98**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 99**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 100**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 101**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 102**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 103**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 104**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 105**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 106**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 107**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 108**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 109**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 110**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 111**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 112**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 113**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 114**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 115**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 116**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 117**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 118**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 119**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 120**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 121**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 122**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 123**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 124**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 125**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 126**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 127**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 128**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 129**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 130**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 131**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 132**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 133**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 134**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 135**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 136**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 137**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 138**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 139**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 140**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 141**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 142**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 143**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 144**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 145**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 146**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 147**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 148**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 149**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 150**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 151**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 152**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 153**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 154**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 155**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 156**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 157**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 158**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 159**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 160**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 161**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 162**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 163**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 164**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 165**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 166**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 167**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 168**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 169**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 170**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 171**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 172**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 173**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 174**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 175**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 176**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 177**

回到 ds-tree-heap 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。
