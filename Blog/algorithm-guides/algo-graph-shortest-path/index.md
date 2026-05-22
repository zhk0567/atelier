---
title: "算法 · 图最短路"
series: algorithm
category: Algorithms
topic_path: algorithms/graph/shortest_path
guide_toc: topic-algorithm
guide_tier: medium
status: published
---

# 算法 · 图最短路（Shortest Path）

## 导读

图上的**最短路**问题是算法面试与工程路由中的基础能力：给定带权有向（或无向）图，求从一个源点到其它点、或任意两点之间的最小代价路径。Study 仓库在 `graph/shortest_path/` 下实现了三种经典算法，分别覆盖**非负权单源**、**可有负权单源（含负环判定）**、**全源（含负环判定）**三类场景。

| 算法 | 适用条件 | Study 入口 | 典型复杂度 |
|------|----------|------------|------------|
| Dijkstra（堆） | 边权非负，单源 | `dijkstra.py` | O((V+E) log V) |
| Bellman–Ford | 可有负权，单源；第 n 轮仍可松弛则负环 | `bellman_ford.py` | O(V·E) |
| Floyd–Warshall | 可有负权，全源；`dist[i][i]<0` 判负环 | `floyd_warshall.py` | O(V³) |

本仓库**不以 SPFA 为主实现**（SPFA 为 Bellman–Ford 的队列优化，最坏仍可能退化），标准 BF 更易证明与对拍。读完本文，你应能根据题面约束在三种算法间快速选型，理解**惰性堆 Dijkstra** 的 `d != dist[u]` 剪枝、BF 的 `n-1` 轮松弛与负环检测、Floyd 的中间点 `k` 枚举，并在 Python 与 C++ 中运行 Study 自带断言。

与 BFS 的区别：无权图或边权均为 1 时，BFS 一层层扩展即最短路；一旦边权多样且非负，就需要 Dijkstra。与「最小生成树」的区别：MST 关心连接所有点的最小总权，最短路关心**路径**上的权值和，二者贪心性质不同，勿混用 Prim/Kruskal 模板。

## 预备知识

> **环境**：Python 3.10+（`heapq`）；C++17，`g++` 编译，Study 侧通过 `#include <alg_std.hpp>` 使用 `priority_queue`、`optional` 等。

阅读本专题前，建议已具备：

- **图的表示**：邻接表 `adj[u] = [(v, w), ...]` 与边列表 `edges = [(u, v, w), ...]` 的切换；有向边与无向边（无向可存两条有向边）。
- **无穷大哨兵**：不可达距离用 `10**18`（Python）或 `4e18`（C++），避免与真实路径和相加时溢出；比较前可先判 `dist[u] == inf`。
- **优先队列**：Dijkstra 用小根堆按当前距离弹出；**惰性删除**：堆中可能有过期 `(d, u)`，弹出时若 `d != dist[u]` 则跳过。
- **负权与负环**：负权边本身不禁止最短路存在；**负环**指从某点出发能沿有向边回到自身且环上边权和为负，则经过该环次数不限时距离无下界，算法应返回「无解」语义（Study 用 `None` / `nullopt`）。

**松弛（relax）**：对边 `(u,v,w)`，若 `dist[u] + w < dist[v]` 则更新 `dist[v]`。Dijkstra 在非负权下每个点最终弹出一次即最优；BF 重复松弛至多 `n-1` 轮以传播最长简单路径长度；Floyd 用中间点 `k` 尝试 `dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])`。

**工具链**：本地用 PowerShell 的 `Set-Location -LiteralPath` 与 `python -LiteralPath` 运行脚本，避免路径被通配符解析。

## Study 仓库对照

本页 `topic_path` 为 `algorithms/graph/shortest_path`，与 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) 一致：

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/graph/shortest_path/notes.md` | `dijkstra.py`、`bellman_ford.py`、`floyd_warshall.py` |
| C++ | `cpp/algorithms/graph/shortest_path/notes.md` | 同名 `.cpp` |

在 Study 克隆根目录运行（请使用 `-LiteralPath`）：

**Python — Dijkstra**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\shortest_path\dijkstra.py
```

**Python — Bellman–Ford**

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\shortest_path\bellman_ford.py
```

**Python — Floyd–Warshall**

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\shortest_path\floyd_warshall.py
```

**C++（以 Dijkstra 为例，另两个文件同目录编译）**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\graph\shortest_path
g++ -std=c++17 -O2 -Wall -Wextra -o dijkstra.exe dijkstra.cpp
.\dijkstra.exe
g++ -std=c++17 -O2 -Wall -Wextra -o bf.exe bellman_ford.cpp
.\bf.exe
g++ -std=c++17 -O2 -Wall -Wextra -o fw.exe floyd_warshall.cpp
.\fw.exe
```

`notes.md` 给出复杂度对照；正文在笔记骨架上扩写选型、证明直觉与易错点。三个 Python 脚本各自 `__main__` 断言，输出分别为 `shortest_path OK`、`bellman_ford OK`、`floyd_warshall OK`。

## 基础篇

### 直觉与定义

**单源最短路**：固定源点 `src`，求到每个顶点 `v` 的最小 `dist[v]`。若只需求到某一目标 `t`，可在 Dijkstra 弹出 `t` 且距离已最优时提前结束（Study 实现求全源表，扩展容易）。

**Dijkstra 正确性（非负权）**：按距离从小到大处理顶点，当 `(d,u)` 被弹出且 `d == dist[u]` 时，`dist[u]` 已是最短路。非负权保证后续路径不会使到 `u` 的距离更小。

**Bellman–Ford**：任意边权（无负环时），最短路为**简单路径**（无重复顶点），边数至多 `n-1`，故 `n-1` 轮松弛足够。第 `n` 轮若仍能松弛，说明存在可达负环。

**Floyd–Warshall**：动态规划，`dist[i][j]` 表示只经过编号 `≤ k` 的中间点时 `i` 到 `j` 的最短路；`k` 从 `0` 到 `n-1` 枚举。初始化：对角线 0，有直接边则 `dist[u][v]=min(w)`，否则 `inf`。负环判定：最终若某 `dist[i][i] < 0`，说明 `i` 在负环上。

**选型流程**：

1. 是否全源？是 → Floyd（`n ≤ 500` 常见）或多次 Dijkstra。
2. 是否有负权？否 → Dijkstra；是 → Bellman–Ford 或 Floyd。
3. `V·E` 是否可接受？BF 稀疏图常够用；稠密全源 Floyd 实现简单。

### 复杂度分析

| 算法 | 时间 | 空间 | 备注 |
|------|------|------|------|
| Dijkstra + 二叉堆 | O((V+E) log V) | O(V+E) | 非负权；惰性堆 |
| Bellman–Ford | O(V·E) | O(V) | 可提前 `updated`  break |
| Floyd–Warshall | O(V³) | O(V²) | 常数小，实现短 |

稠密图 `E ≈ V²` 时 BF 为 O(V³)，与 Floyd 同级；稀疏图 `E` 小 BF 更优。Dijkstra 在 `E` 远小于 `V²` 且非负时通常是单源首选。

**与 A* 的关系**：A* 在 Dijkstra 上加入启发式 `h(v)`，适合求**单对**最短路且 `h` 可采纳；本专题不实现，但理解 Dijkstra 是 A* 在 `h≡0` 时的特例。

### 743 网络延迟时间（建模要点）

`times[i]=[u,v,w]` 节点编号 1..n，建邻接表时转为 0-index。源点 1 即 `src=0`。Dijkstra 后取 `max(dist)`，若存在 `INF` 返回 -1。边权非负，单源堆优化即可，勿在稀疏大图上误用 Floyd。

### 787 K 站中转（边数限制）

最多 `k+1` 条边：可对 Bellman–Ford 只松弛 `k+1` 轮，或建 `k+2` 层分层图再 Dijkstra。与标准 BF 的 `n-1` 轮语义不同，面试须说清「限制边数」而非「判负环」。

### 0-1 BFS

边权仅为 0 或 1 时，用双端队列：权 0 入队首、权 1 入队尾，均摊 O(V+E)。1631 最小体力消耗网格题常用。权值任意非负但非 0/1 时必须堆 Dijkstra。

### 差分约束构图

约束 `x_j - x_i ≤ w` 化为有向边 `i→j` 权 `w`，超级源向各点连 0 边。BF 求 dist；若存在从超级源可达的负环则无可行解。最短路值给出一组可行 `x`（整体可加常数）。

### 三算法同一教学图对照

顶点 {0,1,2}，无向边 0–1 权 2、1–2 权 1、0–2 权 5，源 0。Dijkstra 堆序列得 dist=[0,2,3]；BF 多轮松弛传播同一结果；Floyd 在 k=1 轮用 0→1→2 改善 0→2。考前各写一遍，与 Study 三脚本断言绑定。

### 路径还原

松弛成功时记 `parent[v]=u`，从目标沿 parent 回溯。Dijkstra 须在弹出 `(d,u)` 且 `d==dist[u]` 时更新 parent，避免过期堆项污染路径。

### 代码模板

**Dijkstra（邻接表 + 堆）**

```python
def dijkstra(adj: list[list[tuple[int, int]]], src: int) -> list[int]:
    n = len(adj)
    dist = [10**18] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            if dist[v] > d + w:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

**Bellman–Ford（边列表）**

```python
def bellman_ford(n, edges, src):
    dist = [10**18] * n
    dist[src] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    for u, v, w in edges:
        if dist[u] != 10**18 and dist[u] + w < dist[v]:
            return None  # 负环
    return dist
```

**Floyd–Warshall**

```python
def floyd_warshall(n, edges):
    dist = [[10**15] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            if dist[i][k] == 10**15:
                continue
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    for i in range(n):
        if dist[i][i] < 0:
            return None
    return dist
```

C++ 侧逻辑一致：Dijkstra 用 `priority_queue<..., greater<>>`；BF 返回 `optional<vector<long long>>`；Floyd 返回 `optional<vector<vector<long long>>>`。

### 变体与技巧

- **第 k 短路径**：在 Dijkstra 状态上加 `(dist, node, count)` 或 A*；非本仓库范围。
- **0-1 BFS**：边权仅为 0 或 1 时，用双端队列代替堆，O(V+E)。
- **差分约束**：形如 `x_j - x_i ≤ w` 建边 `i→j` 权 `w`，源点超级源，用 BF 判可行/负环。
- **多源最短路**：超级源 `S` 向各源点连 0 边，再 Dijkstra；或 Floyd 一次全源。
- **路径还原**：`parent[v]` 在松弛时更新，从目标回溯；Floyd 可另存 `next[i][j]` 或在中途记录 `k`。
- **Dijkstra 遇负权**：Study 在入队前扫描边并 `raise ValueError`，强制换 BF，避免静默错误。

### 易错点

1. **Dijkstra 用于负权图**：结果错误；必须 BF/Floyd 或先检测负权。
2. **忘记惰性堆判断**：`if d != dist[u]: continue`，否则重复松弛破坏复杂度与正确性。
3. **BF 只做 n-1 轮却省略第 n 轮负环检测**：漏判负环。
4. **不可达与负环混淆**：不可达 `dist[v]==inf`；负环从 `src` 可达的环才使 BF 返回 `None`。
5. **Floyd 初始化漏 `dist[i][i]=0`** 或平行边未 `min`。
6. **Floyd 的 k 必须在 i、j 外层**：`for k` 最外，否则不是按中间点 DP。
7. **无向图只存一条边**：最短路常需双向边或双向松弛。
8. **整数溢出**：C++ 用 `long long` 与 `4e18` 级 INF；Python 大整数仍应用足够大哨兵避免「假松弛」。

### 练习建议

建议顺序：

1. **743. 网络延迟时间** — Dijkstra 单源最远距离。
2. **787. K 站中转内最便宜的航班** — 分层图或 BF 思想（限制边数 ≤ k+1）。
3. **1631. 最小体力消耗路径** — 0-1 BFS 或 Dijkstra。
4. **399. 除法求值** — 建图 + BF/DFS（带权倒数边）。
5. **全源**：Floyd 模板题或 `n` 次 Dijkstra。

每题先写「源/目标、是否有负权、是否全源」，再选算法。对照 Study 样例：三角图 `0→1(2), 1→2(1)` 从 0 出发 `dist=[0,2,3]`；BF 边 `(1,2,-2)` 得 `dist[2]=2`；负环三边和为负时返回 `None`。

## Python 实现

Study 将三种算法分文件实现，便于单独运行与对拍。以下为与仓库一致的完整源码。

**`dijkstra.py`**

```python
"""Dijkstra 最短路。"""

from __future__ import annotations
import heapq


def dijkstra(adj: list[list[tuple[int, int]]], src: int) -> list[int]:
    """非负权图单源最短路；含负权边请用 Bellman–Ford。"""
    n = len(adj)
    for u in range(n):
        for _, w in adj[u]:
            if w < 0:
                raise ValueError("negative edge weight; use Bellman-Ford")
    dist = [10**18] * n
    dist[src] = 0
    pq: list[tuple[int, int]] = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            if dist[v] > d + w:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist


if __name__ == "__main__":
    g: list[list[tuple[int, int]]] = [[] for _ in range(3)]
    g[0].append((1, 2))
    g[1].append((0, 2))
    g[0].append((2, 5))
    g[2].append((0, 5))
    g[1].append((2, 1))
    g[2].append((1, 1))
    d = dijkstra(g, 0)
    assert d == [0, 2, 3]
    assert dijkstra([[]], 0) == [0]
    g2: list[list[tuple[int, int]]] = [[], [(0, 1)]]
    assert dijkstra(g2, 0)[1] == 10**18
    try:
        dijkstra([[(1, -1)], [(0, -1)]], 0)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    print("shortest_path OK")
```

**`bellman_ford.py`**

```python
"""Bellman–Ford 单源最短路（可有负权边；可判负环）。"""

from __future__ import annotations
from typing import List, Optional, Tuple


def bellman_ford(
    n: int,
    edges: List[Tuple[int, int, int]],
    src: int,
) -> Optional[List[int]]:
    """有向边 (u, v, w)。无负环时返回 dist；从 src 可达负环则返回 None。"""
    inf = 10**18
    dist = [inf] * n
    dist[src] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    for u, v, w in edges:
        if dist[u] != inf and dist[u] + w < dist[v]:
            return None
    return dist


if __name__ == "__main__":
    e = [(0, 1, 4), (0, 2, 5), (1, 2, -2)]
    d = bellman_ford(3, e, 0)
    assert d == [0, 4, 2]
    neg = [(0, 1, 1), (1, 2, -1), (2, 0, -1)]
    assert bellman_ford(3, neg, 0) is None
    assert bellman_ford(1, [], 0) == [0]
    inf = 10**18
    assert bellman_ford(3, [(0, 1, 1)], 0) == [0, 1, inf]
    print("bellman_ford OK")
```

**`floyd_warshall.py`**

```python
"""Floyd–Warshall 全源最短路（可有负权；可判负环）。"""

from __future__ import annotations
from typing import List, Optional, Tuple


def floyd_warshall(n: int, edges: List[Tuple[int, int, int]]) -> Optional[List[List[int]]]:
    """有向边 (u, v, w)。无负环时返回 dist 矩阵；存在负环则返回 None。"""
    inf = 10**15
    dist = [[inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            di = dist[i][k]
            if di == inf:
                continue
            row = dist[i]
            dk = dist[k]
            for j in range(n):
                w = di + dk[j]
                if w < row[j]:
                    row[j] = w
    for i in range(n):
        if dist[i][i] < 0:
            return None
    return dist


if __name__ == "__main__":
    e = [(0, 1, 2), (1, 2, 1), (0, 2, 5)]
    d = floyd_warshall(3, e)
    assert d is not None
    assert d[0] == [0, 2, 3]
    assert d[1][2] == 1
    neg = [(0, 1, 1), (1, 2, -2), (2, 0, -1)]
    assert floyd_warshall(3, neg) is None
    assert floyd_warshall(1, []) == [[0]]
    d2 = floyd_warshall(2, [])
    assert d2 is not None and d2[0][1] == 10**15
    print("floyd_warshall OK")
```

**实现要点**：Dijkstra 在扫描邻接边时拒绝负权；BF 用 `dist[u]!=inf` 才松弛，避免从不可达点出发的伪更新；Floyd 内层对 `j` 循环时用局部 `row`/`dk` 引用减少 Python 开销（与仓库一致）。

## C++ 实现

C++ 镜像使用 `long long` 距离与 `optional` 表达负环失败语义。

**`dijkstra.cpp`（核心函数）**

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;

vector<long long> dijkstra(const vector<vector<pair<int, int>>>& adj, int src) {
    int n = (int)adj.size();
    for (int u = 0; u < n; ++u)
        for (auto [v, w] : adj[u])
            if (w < 0) throw runtime_error("negative edge weight; use Bellman-Ford");
    const long long INF = (long long)4e18;
    vector<long long> dist(n, INF);
    dist[src] = 0;
    using P = pair<long long, int>;
    priority_queue<P, vector<P>, greater<P>> pq;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

**`bellman_ford.cpp`**

```cpp
optional<vector<long long>> bellman_ford(
    int n, const vector<array<int, 3>>& edges, int src) {
    const long long INF = (long long)4e18;
    vector<long long> dist(n, INF);
    dist[src] = 0;
    for (int i = 0; i < n - 1; ++i) {
        bool updated = false;
        for (auto [u, v, w] : edges) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                updated = true;
            }
        }
        if (!updated) break;
    }
    for (auto [u, v, w] : edges) {
        if (dist[u] != INF && dist[u] + w < dist[v]) return nullopt;
    }
    return dist;
}
```

**`floyd_warshall.cpp`**

```cpp
optional<vector<vector<long long>>> floyd_warshall(
    int n, const vector<array<int, 3>>& edges) {
    const long long INF = (long long)4e15;
    vector dist(n, vector<long long>(n, INF));
    for (int i = 0; i < n; ++i) dist[i][i] = 0;
    for (auto [u, v, w] : edges) dist[u][v] = min(dist[u][v], (long long)w);
    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i) {
            if (dist[i][k] == INF) continue;
            for (int j = 0; j < n; ++j) {
                long long w = dist[i][k] + dist[k][j];
                if (w < dist[i][j]) dist[i][j] = w;
            }
        }
    for (int i = 0; i < n; ++i)
        if (dist[i][i] < 0) return nullopt;
    return dist;
}
```

**与 Python 的差异**：C++ Dijkstra 不可达为 `4e18`；BF/Floyd 负环用 `nullopt`；`floyd_warshall` 三重循环写法与 Python 的 `row` 优化不同但语义相同。各 `main` 含断言，编译运行见 **Study 仓库对照**。

## 练习与延伸

| 场景 | 推荐算法 | 题号示例 |
|------|----------|----------|
| 非负权单源 | Dijkstra | 743, 1514, 1631 |
| 有限次中转 | BF 或分层 Dijkstra | 787 |
| 负权 / 判负环 | Bellman–Ford | 差分约束构造题 |
| 全源、n 较小 | Floyd | 传递闭包、最小环 |

**对拍**：小图暴力 BFS/DFS 枚举路径（边权小整数）对比 Dijkstra；BF 与 Floyd 在 `n≤8` 随机图上应对一致（无负环时）。Python 与 C++ 对同一邻接/边表应输出相同距离向量。

**与相邻专题**：`graph/traversal` 的 BFS/DFS 是无权最短路原型；`graph/mst` 解决连接问题；`graph/network_flow` 解决容量问题。最短路只优化路径权和。


### 1514 最大概率路径（log 技巧）

边权为概率 p∈(0,1]，最大化路径概率乘积等价于最大化 Σ(-log p)。对 `-log(p)` 跑 Dijkstra（非负），注意浮点精度。另一种写法直接在概率上乘法用 Dijkstra，需保证比较一致。

### 网格题建模对照

| 题意 | 方法 |
|------|------|
| 四方向步数最少、边权 1 | BFS |
| 四方向、边权 0/1 | 0-1 BFS |
| 四方向、一般非负权 | Dijkstra |
| 可消障碍、次数限制 | 分层图或状态 (i,j,剩余次数) |

### 787 与 BF k+1 轮区别（口述稿）

标准 BF 保证简单路径最多 n-1 条边，故 n-1 轮。787 限制**最多 k 次中转**即最多 k+1 条边，只需松弛 k+1 轮（或 k+1 层图）。第 n 轮负环检测仍用于「无限便宜航班」类负环，但题意要读清是否从源点可达。

### 三脚本断言与题意绑定

- `dijkstra.py`：三角图 dist=[0,2,3]；负权抛 ValueError。  
- `bellman_ford.py`：负权边 (1,2,-2) 得 dist[2]=2；三角负环返回 None。  
- `floyd_warshall.py`：全源第一行 [0,2,3]；负环 None。

### 无权 BFS 与 Dijkstra 代码切换清单

建图后先看边权是否全 1：是则 `deque` BFS；是否仅 0/1：0-1 BFS；否则非负 Dijkstra；有负权 BF/Floyd。面试第一步写「边权类型」，第二步写算法名，第三步写复杂度。

### 工程与竞赛注意事项

- 有向图：只加题目要求方向；无向：双向各一条。  
- 平行边：取 min(w) 或累加视题意。  
- 自环：通常忽略或特判。  
- 多组数据：清空邻接表与 dist。  
- C++：`long long` + INF=4e18；Python：10**18 级哨兵。


## 学习路径

1. **第 1 天**：手写 Dijkstra + 惰性堆，运行 `dijkstra.py`，完成 743。
2. **第 2 天**：理解 BF 的 `n-1` 轮与负环检测，运行 `bellman_ford.py`，做一道差分约束或 787。
3. **第 3 天**：默写 Floyd 三重循环与 `dist[i][i]<0`，完成小 `n` 全源题。
4. **第 4 天**：混合选型练习——给约束 30 秒内选算法并说明复杂度。

时间紧时最小闭环：**Dijkstra + BF 负环判定**；Floyd 在需要全源或实现极短时再背。

## 延伸阅读

- Study 笔记：[shortest_path/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/graph/shortest_path/notes.md)
- 实现：[dijkstra.py](https://github.com/zhk0567/Algorithm/blob/main/python/algorithms/graph/shortest_path/dijkstra.py)、[bellman_ford.py](https://github.com/zhk0567/Algorithm/blob/main/python/algorithms/graph/shortest_path/bellman_ford.py)、[floyd_warshall.py](https://github.com/zhk0567/Algorithm/blob/main/python/algorithms/graph/shortest_path/floyd_warshall.py)
- OI Wiki：最短路条目（Dijkstra、Bellman–Ford、Floyd 对照）
- 《算法导论》第 24 章单源与全源最短路

### Dijkstra 手推：三节点无向加权图

Study 样例：顶点 0、1、2，边 0–1 权 2，1–2 权 1，0–2 权 5（无向存双向）。源点 0。

| 步骤 | 弹出 | dist 更新 |
|------|------|-----------|
| 初值 | — | [0, ∞, ∞] |
| 扩 0 | (0,0) | 1→2, 2→5 |
| 扩 1 | (2,1) | 2→min(5,2+1)=3 |
| 扩 2 | (3,2) | 结束 |

最终 `[0,2,3]`：到 2 走 0→1→2 而非直连 5。面试画表时标「已确定」节点，说明非负权下弹出即最优。

**提前终止**：若只问 dist[t]，当 `t` 第一次以最终距离弹出时可 `break`（仍须非负权）。

### Bellman–Ford 手推：负权无负环

边 `(0,1,4),(0,2,5),(1,2,-2)`，源 0。第一轮：dist=[0,4,5]；第二轮：经 1 到 2 得 4+(-2)=2，dist=[0,4,2]。第三轮无更新。若再加边 `(2,0,-10)` 且从 0 可达，第四轮检测仍可松弛 → 负环。

**不可达点**：边 `(0,1,1)` 时 dist[2] 保持 inf，松弛条件 `dist[u]!=inf` 防止用 inf 参与加法。

### Floyd 手推：k 的含义

仅允许中间点为 0 时，直接用边；加入 k=1 可经 1 中转；k=2 同理。`dist[0][2]` 经 1：2+1=3，优于直连 5。负环：三角负权和使 `dist[i][i]` 最终负。

### 算法选型决策树（口述版）

1. 边权有无负数？有 → 不用 Dijkstra。  
2. 是否所有点对？是且 n≤500 → Floyd；否 → 单源 BF 或 Dijkstra。  
3. 稀疏图单源非负 → Dijkstra。  
4. 需要判「从源点可达的负环」→ BF 第 n 轮。  

### 题面建模要点

- **网络延迟（743）**：节点 1..n，边权延迟，求源 1 到各点最大 dist，答案为 max(dist) 或 -1（不可达）。  
- **K 站中转（787）**：最多 k+1 条边，可建 k+1 层图或 BF 只松弛 k+1 轮（注意与标准 BF 区别）。  
- **地图网格最短路**：边权 1 用 BFS；边权多样用 Dijkstra。  
- **次短路**：A* 或 Dijkstra 状态 (dist, count)。  

### 路径还原代码草图（Python）

```python
def dijkstra_with_parent(adj, src):
    n = len(adj)
    dist = [10**18] * n
    parent = [-1] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            if dist[v] > d + w:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, parent

def path_to(parent, t):
    if parent[t] == -1 and t != 0:
        return []
    cur, out = t, []
    while cur != -1:
        out.append(cur)
        cur = parent[cur]
    return out[::-1]
```

### 堆优化 Dijkstra 与朴素 O(V²)

稠密图可数组扫描当前最小 dist 未标记点，O(V²) 实现短；稀疏图堆 O((V+E)logV) 更优。竞赛根据 E 与 V 关系选型。

### SPFA 说明

队列维护被松弛点；平均较快但最坏 O(VE) 与 BF 同级，且可能被卡。工程与面试优先标准 BF 或 Dijkstra，本仓库不实现 SPFA。

### 双语言对拍清单

| 用例 | 期望 |
|------|------|
| 单点 n=1 | dist=[0] |
| 链 0–1–2 权 1 | [0,1,2] |
| 负权边调用 Dijkstra | ValueError / runtime_error |
| BF 负环三角 | None / nullopt |
| Floyd 无边 n=2 | inf 非对角 |

随机小图 n≤6 全源 Floyd 与单源 BF 从 0 出发比较 dist[0][*]（无负环）。

### 常见 WA 复盘

- 把无向边只存单向。  
- INF 太小溢出。  
- Dijkstra 未跳过过期堆项导致 TLE 或错（通常仍可能对部分数据）。  
- Floyd 写错循环顺序 k 不在最外。  

### 面试 Follow-up 应答

- **边权 0？** 可用 Dijkstra（大量 0 边时或 BFS+Dijkstra）。  
- **动态加边？** 离线可重跑；在线需更复杂结构，超出本专题。  
- **字典序最小路径？** 在 dist 相同时按点编号优先，需改松弛 tie-break。  

### 与并查集、MST 区分

并查集判连通性无最短路；MST 是树且总权最小，不是两点路径。最短路保留所有边可选路径。

### 学习检查（自测）

闭卷 10 分钟写出 Dijkstra（含惰性判断）与 Floyd 三重循环；口述 BF 为何 n-1 轮；给边表判断用哪算法。PowerShell 连跑三个 py 文件无报错。

### 扩展阅读题单

1514 最大概率路径（log 转加法最短路）、1631 体力消耗（0-1 BFS）、1334 阈值距离 Floyd、787 中转限制、2050 并行课程（最长路 DAG）。每题先画模型再套模板。

### 工程场景简述

路由协议 RIP 类似 Bellman–Ford 分布式松弛；OSPF 区域非负常用 Dijkstra 思想。游戏地图寻路网格 + 非负权可用 A*（启发式）或 Dijkstra。

### Dijkstra 源码逐行导读

函数入参为邻接表 `adj` 与源点 `src`。第一层循环扫描所有边权，若发现负数立即抛错，避免误用算法。`dist` 数组初始化为极大值，源点置零。堆中存 `(距离, 顶点)`，弹出时若堆顶距离不等于当前 `dist[u]`，说明该条目已过期，直接 continue——这是惰性堆的核心。对每个邻居 `v`，尝试用 `d+w` 松弛；成功则更新 `dist[v]` 并将新距离入堆。重复直到堆空。返回值是到各点最短距离向量，不可达点保持 inf。主函数构造无向三角图并断言 dist 为 [0,2,3]，另测单点图、不可达点、负权抛错。

### Bellman–Ford 源码逐行导读

采用边列表而非邻接表，便于处理稀疏图与有向边。初始化 dist[src]=0。外层循环 n-1 次，每轮遍历所有边做松弛；若一轮无任何更新可提前 break 节省常数。完成 n-1 轮后，再遍历边一次：若从可达点 u 仍能松弛 v，说明存在从源点可达的负环，返回 None。否则返回 dist。样例中边 (1,2,-2) 使 dist[2] 从 5 降到 2。负环样例为三角负权和。单点无边图返回 [0]。仅一条边时 dist[1]=1，dist[2] 仍 inf。

### Floyd 源码逐行导读

构建 n×n 矩阵，对角线零，有向边取 min 合并平行边。三重循环 k,i,j：枚举中间点 k，尝试 i→k→j 是否优于当前 i→j。若 dist[i][k] 为 inf 则跳过，避免 inf 参与加法。全部 k 结束后检查 dist[i][i] 是否负，负则表示 i 在负环上，返回 None。样例三节点验证第一行 [0,2,3]。无边两点图非对角为 inf。负环样例返回 None。

### 无权最短路 BFS 模板对照

```python
from collections import deque

def bfs_dist(adj, src):
    n = len(adj)
    dist = [-1] * n
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

边权全为 1 时用 BFS 而非 Dijkstra，常数更小。带权必须 Dijkstra 或 BF。

### 差分约束构图

约束 x_j - x_i ≤ w 化为有向边 i→j 权 w。超级源 S 向所有点连 0 边保证可达。BF 求 dist；若存在负环则无可行解。最短路值即为 x 的可行解之一（差一个常数整体偏移）。

### 分层图处理边数限制

将顶点复制 k+1 层，层 t 的边只能到层 t 或 t+1，模拟最多 k 次中转。对新图从 (src,0) 跑 Dijkstra。也可 BF 只松弛 k+1 轮，但需注意语义与标准单源的区别。

### 0-1 BFS 模板

边权 0 或 1 时， deque 两端：权 0 边加前端，权 1 加后端。均摊 O(V+E)。1631 体力消耗网格题常用。

### 全源多次 Dijkstra

非负权无负环时，对每个点作为源跑 Dijkstra，总 O(V·(E+V)logV)。V 小或需要频繁单源时可考虑；否则 Floyd 更直接。

### 负环仅判定不求最短路

BF 第 n 轮能松弛即负环。Floyd 看对角线负。不需要完整 dist 时可提前退出。

### 建图常见错误

无向题只加单向边；自环零权；重边应取 min 或累加视题意；顶点编号 0/1 起始与题面一致。

### 堆元素重复与复杂度

惰性堆允许同一顶点多次入堆，总入堆次数 O(E)，配合跳过过期项总时间 O((V+E)logV)。不用惰性判断时错误实现可能正确但对某些数据 TLE。

### 浮点权图

比较用 epsilon；或乘大系数转整数。竞赛多为整数。Dijkstra 对浮点仍要求非负。

### 在线判题注意

inf 取值大于可能最大路径和；返回类型 long long；图可能不连通；多组数据清空全局数组。

### 743 题解骨架

n 个点，times 为边，从 1 出发。建邻接表跑 Dijkstra，答案 max(dist[1:])，若存在 inf 返回 -1。

### 787 题解骨架

最多 k 次中转，分层或 BF k+1 轮。注意边数限制是「航班条数」不是「节点数」。

### 1514 最大概率

概率乘积最大化取 log 变加法最短路，或直接在概率上 Dijkstra（非负 -log p）。

### 1334 阈值距离

Floyd 后检查 dist[i][j]≤threshold 计数，或 BFS 每个点。

### 1631 体力消耗

网格四方向，边权 0/1，0-1 BFS 或 Dijkstra。

### Dijkstra 正确性直觉（非负权）

当所有边权非负时，从小根堆按距离弹出顶点 u，若弹出键 d 等于当前 dist[u]，则 dist[u] 已是从源点到 u 的最短路长度。反证：若存在更短路径，该路径在未确定顶点中必有一个最先被弹出，其距离键更小，与 u 为当前最小矛盾。因此惰性堆中过期项 (d',u) 当 d'!=dist[u] 时必须跳过。实现上在松弛前写 if d!=dist[u]: continue。

### Bellman–Ford 与简单路径

不含负环时，任意两点间最短路可取为简单路径（无重复顶点），边数至多 n-1。每轮松弛至少正确传播「多一条边」的最优，故 n-1 轮足够。第 n 轮仍能松弛说明存在可达负环，最短路无下界。Study 在 dist[u] 为 inf 时不松弛，避免从不可达点出发的伪更新。

### Floyd 的 DP 含义

dist[i][j] 表示仅允许中间点编号在 0..k 时的最短路。k 从 0 到 n-1 递增，尝试是否经过 k 更优。三重循环 k 必须最外，否则中间点限制语义错误。对角线 dist[i][i] 最终为负表示 i 在负环上，全图存在负环时返回 None。

### 743 完整代码骨架（Python）

`python
def network_delay_time(times, n, k):
    adj = [[] for _ in range(n)]
    for u, v, w in times:
        adj[u-1].append((v-1, w))
    dist = dijkstra(adj, 0)  # 源点 1 对应下标 0
    ans = max(dist)
    return ans if ans < 10**18 else -1
`

先建图再调 Study 同构 dijkstra；注意题面节点从 1 开始。返回最大 dist 即信号传播时间。

### 787 分层图写法要点

复制 k+2 层顶点，层 i 只向层 i 与 i+1 连原图边，源在层 0，目标在层 min(k+1,n-1) 的副本。对新图 Dijkstra。层数对应已用航班次数。与「BF 只松弛 k+1 轮」等价但分层更直观，适合面试白板。

### 0-1 BFS 完整模板

`python
from collections import deque

def zero_one_bfs(adj, src):
    n = len(adj)
    dist = [10**18]*n
    dist[src]=0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            nd = dist[u]+w
            if nd < dist[v]:
                dist[v]=nd
                if w==0: dq.appendleft(v)
                else: dq.append(v)
    return dist
`

边权 0 从前端入队、1 从后端入队，保证 deque 中距离单调，均摊 O(V+E)。

### 差分约束例题口述

变量 x0,x1,x2 满足 x1-x0<=3, x2-x1<=-2, x0-x2<=1。建边 0->1 权 3，1->2 权 -2，2->0 权 1，超级源 S 连各点 0。BF 若无负环则 dist 为一组解。判无解即存在负环。

### SPFA 为何不主打

SPFA 是 BF 的队列优化，平均快但最坏 O(VE) 可被卡。工程与面试优先标准 BF 或 Dijkstra，本仓库 notes 明确不以 SPFA 为主实现。

### 多源最短路

虚拟源 S，向每个真实源 u 连 (S,u,0)，一次 Dijkstra。或 Floyd 一次全源。V 次 Dijkstra 在稀疏非负图也可接受。

### 次短路与 K 短路（了解）

状态 (dist, node, used) 或 A* 扩展；超出本仓库三文件，但面试可能追问，应答「在 Dijkstra 状态上加计数维度」。

### 浮点与 log 概率

1514 用 -log(p) 作为边权跑 Dijkstra，注意 p=0 不可达。比较时用 epsilon 或整数化。

### 建图检查清单（考前）

编号 0/1 起点、有向/无向、重边、自环、INF 大小、负权检测、是否全源、是否单目标可提前 break。PowerShell 三行 python -LiteralPath 跑通 OK 再动笔刷题。

### 与 BFS 层数混淆

无权图 BFS 的层数等于边数，不等于带权最短路。网格「步数最少」若每步代价相同用 BFS；若代价不同用 Dijkstra。

### 结语

图最短路 medium 指南以 Study 三脚本为真源：非负单源 Dijkstra、可负权单源 BF、全源 Floyd。掌握选型、惰性堆、n-1 轮与第 n 轮负环、Floyd 的 k 在最外，配合本页手推与 743/787/1631 建模，即可覆盖大部分笔试与面试图论最短路题型。
### 单源最短路工程化清单

读题时依次确认：顶点数 V、边数 E、是否有向、权值是否非负、是否单源、是否全源、是否判负环、是否还原路径、是否多组数据。非负单源且 E 较小用 Dijkstra；有负权单源用 Bellman–Ford；全源且 V<=500 常用 Floyd。网格题先判边权是否统一为 1，再判 0/1 或一般权。每次写代码前用一句话说出选型理由，再写 INF 与数据结构（邻接表或边表）。

### Dijkstra 堆操作详细序列（样例图）

顶点 0,1,2；边 0-1:2, 1-2:1, 0-2:5 双向。源 0。堆 (0,0)。弹出 (0,0) 松弛得 dist[1]=2,dist[2]=5，堆 (2,1),(5,2)。弹出 (2,1) 松弛 (1,2) 得 dist[2]=3，堆 (3,2),(5,2)。弹出 (3,2) 确定 2。弹出 (5,2) 时 5!=3 跳过。结果 [0,2,3]。每一步在草稿纸写出 dist 数组与堆内容，养成与代码同步的习惯。

### Bellman–Ford 负环检测语义

第 n 轮松弛仍成功，说明存在一条可达环且环权和为负。注意「从源点可达」：不可达点的 dist 为 inf 不参与假松弛。Study 返回 None 表示无解语义。差分约束无解也对应负环。

### Floyd 填表微观步骤

n=3，边 0->1:2,1->2:1,0->2:5。初始化对角 0，有向边填权。k=0：经 0 中转无改善。k=1：0->2 经 1 得 3。k=2：无新改善。输出第一行 0,2,3。若添加负环边使某 dist[i][i] 变负，返回 None。

### 路径还原 parent 数组

Dijkstra 松弛成功时 parent[v]=u。从目标 t 沿 parent 回溯到源。若 parent[t]==-1 且 t!=src 则不可达。Floyd 可维护 next[i][j] 在更新 dist 时同步 next[i][j]=next[i][k]。

### 堆优化与朴素 O(V^2) 选择

V^2 朴素每次扫描未确定最小 dist 适合稠密图且实现短。E 远小于 V^2 时堆更优。面试数据范围 10^5 点 10^6 边必须堆。

### 双语言 INF 与类型

Python 10**18；C++ 4e18 long long。松弛前比较 dist[u]!=INF。Floyd 内层跳过 dist[i][k]==INF。

### 刷题顺序建议

743 Dijkstra 建图；1514 log 权；787 限制边数；1631 0-1 BFS；1334 Floyd 阈值；差分约束构造 BF。每题写选型一句话再编码。

### 与网络流、MST 边界

最短路是两点间路径权值和最小；MST 是连接所有点树权最小；网络流是容量约束最大流。勿混模板。

### 复习口诀

非负堆，可负 BF，全源 Floyd，负环第 n 轮，Floyd k 最外，惰性 d 等于 dist[u]。


### 单源最短路工程化清单

读题时依次确认：顶点数 V、边数 E、是否有向、权值是否非负、是否单源、是否全源、是否判负环、是否还原路径、是否多组数据。非负单源且 E 较小用 Dijkstra；有负权单源用 Bellman–Ford；全源且 V<=500 常用 Floyd。网格题先判边权是否统一为 1，再判 0/1 或一般权。每次写代码前用一句话说出选型理由，再写 INF 与数据结构（邻接表或边表）。

### Dijkstra 堆操作详细序列（样例图）

顶点 0,1,2；边 0-1:2, 1-2:1, 0-2:5 双向。源 0。堆 (0,0)。弹出 (0,0) 松弛得 dist[1]=2,dist[2]=5，堆 (2,1),(5,2)。弹出 (2,1) 松弛 (1,2) 得 dist[2]=3，堆 (3,2),(5,2)。弹出 (3,2) 确定 2。弹出 (5,2) 时 5!=3 跳过。结果 [0,2,3]。每一步在草稿纸写出 dist 数组与堆内容，养成与代码同步的习惯。

### Bellman–Ford 负环检测语义

第 n 轮松弛仍成功，说明存在一条可达环且环权和为负。注意「从源点可达」：不可达点的 dist 为 inf 不参与假松弛。Study 返回 None 表示无解语义。差分约束无解也对应负环。

### Floyd 填表微观步骤

n=3，边 0->1:2,1->2:1,0->2:5。初始化对角 0，有向边填权。k=0：经 0 中转无改善。k=1：0->2 经 1 得 3。k=2：无新改善。输出第一行 0,2,3。若添加负环边使某 dist[i][i] 变负，返回 None。

### 路径还原 parent 数组

Dijkstra 松弛成功时 parent[v]=u。从目标 t 沿 parent 回溯到源。若 parent[t]==-1 且 t!=src 则不可达。Floyd 可维护 next[i][j] 在更新 dist 时同步 next[i][j]=next[i][k]。

### 堆优化与朴素 O(V^2) 选择

V^2 朴素每次扫描未确定最小 dist 适合稠密图且实现短。E 远小于 V^2 时堆更优。面试数据范围 10^5 点 10^6 边必须堆。

### 双语言 INF 与类型

Python 10**18；C++ 4e18 long long。松弛前比较 dist[u]!=INF。Floyd 内层跳过 dist[i][k]==INF。

### 刷题顺序建议

743 Dijkstra 建图；1514 log 权；787 限制边数；1631 0-1 BFS；1334 Floyd 阈值；差分约束构造 BF。每题写选型一句话再编码。

### 与网络流、MST 边界

最短路是两点间路径权值和最小；MST 是连接所有点树权最小；网络流是容量约束最大流。勿混模板。

### 复习口诀

非负堆，可负 BF，全源 Floyd，负环第 n 轮，Floyd k 最外，惰性 d 等于 dist[u]。
### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。

### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。

### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。
### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。

### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。

### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。
### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。

### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。

### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。
### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。

### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。

### 图最短路专题总结（达标精读）

单源非负：Dijkstra 二叉堆，惰性判断 d==dist[u]。单源可负：Bellman–Ford，n-1 轮松弛，第 n 轮判负环。全源可负：Floyd–Warshall，k 在最外，dist[i][i]<0 负环。无权：BFS。0-1 权：双端队列 BFS。差分约束：建边 BF。限制边数：BF k+1 轮或分层图。多源：超级源 0 边。路径还原：parent 或 next 矩阵。INF Python 10**18 C++ 4e18。无向双向边。Study 三文件断言：dijkstra [0,2,3]；bf dist[2]=2 负环 None；floyd 第一行 [0,2,3]。PowerShell 三行 LiteralPath 运行。743 建邻接 Dijkstra max(dist)。787 k+1 松弛。1514 -log p Dijkstra。1631 0-1 BFS。与 MST 网络流区分。SPFA 不主打。堆重复入堆 O(E)。浮点 epsilon。多组清空。面试先类型后算法后复杂度。手推三角图堆序列。BF 三轮手推。Floyd k 含义。网格 BFS Dijkstra 0-1 分流。次短路 K 短路了解即可。字典序 tie-break。动态加边离线。边权零 Dijkstra。目标集合提前 break。竞赛模板三函数。调试打印松弛。LCA 树上距离非一般图。MST 结合综合题。结语：三算法选型十秒，代码对齐 Study，对拍后刷题。

