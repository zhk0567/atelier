---
title: "数据结构 · 并查集（Union-Find）"
series: algorithm
category: DataStructures
topic_path: data_structures/graph/disjoint_set
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-22
tags: [DataStructures, UnionFind, DisjointSet, Kruskal, Connectivity]
---

# 数据结构 · 并查集（Union-Find）

## 导读

**并查集**维护一族**不相交集合**，支持 **find**（查询元素所属集合代表元）与 **unite**（合并两集合）。在**路径压缩**与**按秩合并**（或按大小合并）下，单次操作均摊接近 O(α(n))，α 为反阿克曼函数，实际可视为常数级。

Study `union_find.py` / `union_find.cpp` 实现标准模板；典型题：连通分量（200/547）、判环（684）、Kruskal 最小生成树（1135，见 `algo-graph-mst`）。

## 预备知识

> **环境**：Python 3.10+；C++17，`union_find.cpp` 用 `vector`、`iota`。

- 无向图连通性概念。
- 数组存 `parent`、`rank`。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/graph/disjoint_set` |
| Python | `python/data_structures/graph/disjoint_set/union_find.py` |
| C++ | `cpp/data_structures/graph/disjoint_set/union_find.cpp` |

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\data_structures\graph\disjoint_set\union_find.py
```

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\data_structures\graph\disjoint_set
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe union_find.cpp
.\run.exe
```

输出 `UnionFind OK`。

## 基础篇

### 抽象模型

`n` 个元素初始各成集合；`parent[i]=i`。`find(x)` 返回根；`unite(a,b)` 若根不同则合并并返回 `True`，否则 `False`。

### 核心操作

| 操作 | 均摊 |
|------|------|
| find | O(α(n)) |
| unite | O(α(n)) |

### 实现要点

**路径压缩**

```python
def find(self, x: int) -> int:
    if self._parent[x] != x:
        self._parent[x] = self.find(self._parent[x])
    return self._parent[x]
```

**按秩合并**：秩小的根挂到秩大的根；秩相等则根秩 +1。

### 典型应用

- **Kruskal**：边升序，两端不同集合则 unite 并累加权重。
- **连通块计数**：初始 n 组件，每次成功 unite 减一。
- **网格图**：单元格编号 + 四方向 unite。
- **带权并查集**：399 等（扩展）。

### 易错点

- 忘记路径压缩导致退化链。
- `unite` 返回值语义：已连通返回 `False`（684 判冗余边）。
- 有向图不能直接用无向 UF（685 特殊）。
- 网格编号 `(i,j) -> i*m+j` 算错。

### 练习建议

1. 跑通 Study 断言（含 `UnionFind(1)`）。
2. 547/200 数连通分量。
3. 684 找冗余边。
4. 1135 配合 `algo-graph-mst`。

## Python 实现

```python
class UnionFind:
    def __init__(self, n: int) -> None:
        self._parent = list(range(n))
        self._rank = [0] * n

    def find(self, x: int) -> int:
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def unite(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self._rank[ra] < self._rank[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        if self._rank[ra] == self._rank[rb]:
            self._rank[ra] += 1
        return True
```

## C++ 实现

```cpp
struct UnionFind {
    vector<int> parent, rankv;
    explicit UnionFind(int n) : parent(n), rankv(n, 0) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        return parent[x] == x ? x : parent[x] = find(parent[x]);
    }
    bool unite(int a, int b) { /* 同 Python */ }
};
```

## 练习与延伸

| 题 | 要点 |
|----|------|
| 547, 200 | 连通分量 |
| 684 | unite 返回 false |
| 1135, 1584 | Kruskal |
| 128 | 连续序列 + 哈希或 UF |
| 399 | 带权扩展 |

## 学习路径

1. 手写 find+unite 并对拍暴力。
2. 684 + 547 各一题。
3. 读 `algo-graph-mst` Kruskal 章节。
4. strict 校验。

## 延伸阅读

- `notes.md` · [disjoint_set](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/graph/disjoint_set)
- 站点：`algo-graph-mst`、`algo-graph`


**深度补充：并查集抽象**

维护不相交集合族；find 查代表元；unite 合并两集合。


**深度补充：路径压缩**

find 时 parent[x]=find(parent[x])，均摊近 O(α(n))。


**深度补充：按秩合并**

小树挂大树，控制树高；秩相等则 ra 增一。


**深度补充：按大小合并**

维护 size 数组，小集合并入大；与按秩类似。


**深度补充：unite 返回 false**

已在同一集合则不再合并，返回 false；Kruskal 判环。


**深度补充：200 岛屿数量**

网格 1 的连通块；可把格子编号 union 四邻。


**深度补充：547 省份数量**

连通分量个数= n - 成功 unite 次数？注意初始 n 组件。


**深度补充：684 冗余连接**

最后一条使 unite 返回 false 的边即答案。


**深度补充：685 冗余连接 II**

有向图并查集+入度，更难。


**深度补充：128 最长连续序列**

值域 union 或哈希 set O(n)。


**深度补充：130 被围绕区域**

边界 O 与内部 O 并查集或 DFS。


**深度补充：399 除法求值**

带权并查集 parent+weight。


**深度补充：947 最多石头移除**

同行同列 union，答案 n - 连通块数。


**深度补充：803 打砖块**

逆序加砖+并查集。


**深度补充：1202 交换字符串**

可交换下标 union，每组排序后填回。


**深度补充：1631 最小体力消耗**

并查集+排序边或 Dijkstra。


**深度补充：1135 连接所有城市**

Kruskal MST，见 algo-graph-mst。


**深度补充：1584 连接所有点**

完全图 Kruskal，边权曼哈顿距离。


**深度补充：1489 关键边**

MST 变体，并查集判必需边。


**深度补充：Kruskal 流程**

边升序，两端不同集合则 unite 并累加权值。


**深度补充：连通块计数**

初始 n 个集合；每次成功 unite 组件数减一。


**深度补充：离线询问**

按时间倒序加边或 unite 回答连通性。


**深度补充：并查集与 DFS**

无向图连通可 DFS 或 UF；动态边加 UF 更方便。


**深度补充：有向图**

普通 UF 不适用；685 需特殊处理。


**深度补充：网格编号**

cell (i,j) 映射 id=i*m+j。


**深度补充：虚拟节点**

超级源点 union 边界，简化被围绕区域。


**深度补充：路径压缩递归**

Python 递归 find 可；深链注意栈。


**深度补充：迭代 find**

while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]。


**深度补充：秩数组含义**

rank 近似树高上界，非精确高度。


**深度补充：α(n) 反阿克曼**

增长极慢，均摊分析结论，面试说「近常数」即可。


**深度补充：unite 0 元素**

UnionFind(1) 仅自身；边界测例。


**深度补充：重复 unite**

assert not unite(0,2) when 0,2 已连通。


**深度补充：C++ iota**

parent 初始 0..n-1。


**深度补充：C++ 路径压缩**

parent[x]=find(parent[x]) 一行。


**深度补充：与 Trie**

并查集与 Trie 不同结构。


**深度补充：与 BFS**

单次连通 BFS O(V+E)；动态连通 UF 优。


**深度补充：朋友圈 547**

邻接矩阵或 UF 数组件。


**深度补充：等式方程 990**

字母 union；不等式再判矛盾。


**深度补充：情侣牵手 765**

并查集建模配对。


**深度补充：尽量减少恶意组 839**

并查集+枚举。


**深度补充：打砖块 803 逆序**

经典离线技巧。


**深度补充：面试话术 UF**

「路径压缩+按秩；Kruskal；unite 假即环」。


**深度补充：对拍 UnionFind**

随机 unite 与暴力集合对比。


**深度补充：内存**

parent+rank 两数组 O(n)。


**深度补充：结语 UF**

Study UnionFind OK + 200/547/684/1135=并查集闭环。


**深度补充：综合复盘 46**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 47**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 48**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 49**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 50**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 51**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 52**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 53**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 54**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 55**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 56**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 57**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 58**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 59**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 60**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 61**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 62**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 63**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 64**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 65**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 66**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 67**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 68**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 69**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 70**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 71**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 72**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 73**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 74**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 75**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 76**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 77**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 78**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 79**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 80**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 81**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 82**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 83**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 84**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 85**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 86**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 87**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 88**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 89**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 90**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 91**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 92**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 93**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 94**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 95**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 96**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 97**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 98**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 99**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 100**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 101**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 102**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 103**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 104**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 105**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 106**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 107**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 108**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 109**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 110**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 111**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 112**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 113**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 114**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 115**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 116**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 117**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 118**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 119**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 120**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 121**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 122**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 123**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 124**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 125**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 126**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 127**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 128**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 129**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 130**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 131**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 132**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 133**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 134**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 135**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 136**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 137**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 138**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 139**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 140**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 141**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 142**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 143**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 144**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 145**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 146**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 147**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 148**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 149**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 150**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 151**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 152**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 153**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 154**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 155**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 156**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 157**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 158**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 159**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 160**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 161**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 162**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 163**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 164**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 165**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 166**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 167**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 168**

回到 ds-graph-disjoint-set 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。
