---
title: "算法 · Graph Traversal"
series: algorithm
category: Algorithms
topic_path: algorithms/graph/traversal
guide_toc: topic-algorithm
guide_tier: medium
status: published
---

# 算法 · 图遍历（Graph Traversal）

## 导读

**图遍历**是在图或网格上按规则访问顶点的过程，两大经典实现是 **深度优先搜索（DFS）** 与 **广度优先搜索（BFS）**。二者共享同一套「已访问」标记（`visited` / `seen`），区别仅在于**待访问集合**的取出顺序：DFS 用栈（或递归隐式栈）后进先出，沿一条路径走到底再回溯；BFS 用队列先进先出，按**层**向外扩展。

Study 仓库 `graph/traversal/` 在**邻接表**上给出 `dfs_order` 与 `bfs_order`，返回从 `start` 出发的**访问序**（非完整全图连通分量枚举）。本页在仓库实现之上，系统补充**网格四连通/八连通**、多源 BFS、连通块计数、二分图染色、环检测等面试高频模式，并说明与最短路、拓扑排序的边界。

| 方法 | 数据结构 | 访问序特点 | 典型用途 |
|------|----------|------------|----------|
| DFS | 栈 / 递归 | 深先；依赖邻接表顺序 | 连通块、回溯、环检测、路径存在 |
| BFS | 队列 `deque` | 层序；距源边数递增（无权） | 最短路步数、最少变换、多源扩散 |

**与最短路的关系**：边权均为 1（或 0/1 双权）时，BFS 第一次到达某点的层数即最短路长度；边权任意非负时需 **Dijkstra**，可有负权用 **Bellman–Ford**，全源小图用 **Floyd**。站点第 1 批专题 [**algo-graph-shortest-path**（图最短路）](../algo-graph-shortest-path/) 已覆盖 Dijkstra / BF / Floyd 与网格建模分流；读完本篇 BFS 层数语义后，应能判断「继续 BFS」还是「转最短路专题」。

**与拓扑排序**：有向无环图（DAG）的拓扑序常用 DFS 后序或 Kahn 的 BFS 入度；有环则无法拓扑。拓扑独立在 `graph/topological_sort/`，不在本篇展开。

**面试中的「图」并不总是显式邻接表**：二维矩阵、字符串变换、状态压缩棋盘、课程依赖表，都可建模为顶点 + 边的图。识别图模型后，90% 的连通/最短路/分层题会落在 DFS 或 BFS 两套模板上；剩余带权题交给 [**algo-graph-shortest-path**](../algo-graph-shortest-path/)。

读完本文，你应能：在邻接表与二维网格上默写 DFS/BFS；正确在**入队时**或**入栈时**标记 `visited`；口述 **O(V+E)** / **O(m·n)** 复杂度；识别岛屿、腐烂橘子、单词接龙、二分图等题型并选型；知道何时从 BFS 层数升级到 Dijkstra。

## 预备知识

> **环境**：Python 3.10+（`collections.deque`）；C++17，`g++`，`graph_traversal.cpp` 通过 `#include <alg_std.hpp>` 使用 `queue`、`function`。

建议已掌握：

- **图的表示**：邻接表 `adj[u] = [v, ...]`；无向边存双向；有向题只加单向。网格题把每个 `(r,c)` 当作顶点，四方向连边。
- **队列与栈**：BFS 用 `deque` 的 `popleft` / `append`；DFS 递归或显式 `stack` 的 `pop` / `append`。
- **visited 语义**：每个顶点在**整个搜索过程中**至多扩展一次；标记时机错误会导致重复入队或死循环。
- **坐标系**：`DIRS = [(0,1),(0,-1),(1,0),(-1,0)]`；边界 `0 <= nr < m and 0 <= nc < n`；水域/障碍用题面字符判断。

**无权最短路（BFS 层数）**：`dist[src]=0`，从队列弹出 `u` 时遍历邻居 `v`，若 `v` 未访问则 `dist[v]=dist[u]+1` 并入队。网格「最少步数」即此模板。**多源 BFS**：初始把所有源点入队并标 `dist=0`，其余同上。

**parent 与路径还原**：BFS 中 `parent[v]=u` 在首次发现 `v` 时记录；从终点 `t` 沿 `parent` 回溯到源即一条最短路径（边权 1）。DFS 同理，但回溯得到的路径未必最短。面试若只要长度，用 `dist` 即可；若要输出路径，维护 `parent` 并在回溯时 `reverse`。

**状态空间图**：单词接龙、开锁、水壶问题等，顶点不是 `0..n-1`，而是字符串或元组。用 `set`/`dict` 存 `seen`，哈希 O(1) 判重。边隐式生成：对每个状态尝试所有操作，合法则入队。复杂度取决于状态总数与分支因子，不是邻接表输入规模。

**0/1 BFS 预告**：边权仅为 0 或 1 时，双端队列可在 O(V+E) 求最短路，仍属「层数扩展」家族，完整模板在 [**algo-graph-shortest-path**](../algo-graph-shortest-path/)。本篇 BFS 是 0/1 BFS 在权全 1 时的特例。

**工具链**：PowerShell 使用 `Set-Location -LiteralPath` 与 `python -LiteralPath`，避免路径通配符。

## Study 仓库对照

本页 `topic_path` 为 `algorithms/graph/traversal`，与 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) 一致：

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/graph/traversal/notes.md` | `graph_traversal.py` |
| C++ | `cpp/algorithms/graph/traversal/notes.md` | `graph_traversal.cpp` |

在 Study 克隆根目录运行（请使用 `-LiteralPath`）：

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\traversal\graph_traversal.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\graph\traversal
g++ -std=c++17 -O2 -Wall -Wextra -o graph_traversal.exe graph_traversal.cpp
.\graph_traversal.exe
```

成功输出 `graph_traversal OK`。

**断言含义**：无向图 4 点，边 `(0,1)(0,2)(1,3)`。从 0 出发 DFS 序 `[0,1,3,2]`（先走 1 再深到 3，再回溯到 2）；BFS 序 `[0,1,2,3]`（层 0 → 层 1 的 1,2 → 层 2 的 3）。邻接表 `adj[u]` 的**邻居顺序**会影响 DFS 序，但不影响 BFS 的层序性质。

**本地调试建议**：在 `if __name__` 中打印 `adj` 与两种序，改边集观察 DFS 序变化；加边 `2-3` 后访问序可能变化而 BFS 层序仍按距离分层。理解「DFS 序不唯一、BFS 层数唯一」可避免争论输出顺序。

**从 notes.md 扩写**：Study 笔记仅给出 O(V+E) 一句，本篇系统补充网格四连通、多源 BFS、visited 时机、面试题映射，以及到 [**algo-graph-shortest-path**](../algo-graph-shortest-path/) 的升级路径；实现以仓库断言为准。

## 基础篇

### 直觉与定义

把图想象成城市与道路：DFS 是「选一条路一直走，走不通再回头」；BFS 是「同时向四周扩散一圈，再扩散下一圈」。在**无权**图上，BFS 第 `k` 轮处理的顶点集合，正是距源点恰好 `k` 条边的顶点（边权均为 1 时）。

**邻接表上的遍历**：从 `start` 出发，只访问与 `start` 在同一连通分量内的点。若需遍历**全图**所有分量，外层 `for i in range(n): if not seen[i]: dfs(i)` 或 `bfs(i)`。

**网格上的遍历**：`grid[r][c]` 为陆地 `'1'` 或水域 `'0'` 时，仅在陆地上四连通扩展；每访问一格标记 `visited` 或原地改 `'0'` 避免重复。网格图顶点数 `V=m·n`，边数 `E≈4V`，故 DFS/BFS 均为 **O(m·n)**。

**访问序 vs 最短路**：`dfs_order` / `bfs_order` 返回的是**发现顺序**，不是路径栈。求路径需另存 `parent[u]`，从目标沿 parent 回溯。无权最短路长度用 BFS 的 `dist` 数组，详见下文模板与 [**algo-graph-shortest-path**](../algo-graph-shortest-path/) 中「无权用 BFS」一节。

**邻接表建图套路**：边列表 `edges = [(u,v)]` 无向时 `adj[u].append(v); adj[v].append(u)`。有向只加 `u→v`。点数 `n` 已知时 `adj = [[] for _ in range(n)]`；点数由边推断时 `max_id+1`。网格不建显式邻接表，四方向循环即隐式邻接。面试「节点数 10^5、边数 10^6」几乎必用邻接表，邻接矩阵 O(V^2) 会 MLE。

**DFS 的三种常见语义**：（1）输出访问序，如 Study `dfs_order`；（2）统计连通块大小/面积，遇未访问则启动一次 DFS；（3）回溯搜索，路径栈 push/pop，`seen` 可能撤销。三者代码骨架相似，但（2）不撤销标记、（3）要撤销，混用导致 WA。

**BFS 的三种常见语义**：（1）层序访问序 `bfs_order`；（2）单源最短步数 `dist`；（3）多源同时扩散（腐烂橘子、多源最短路）。（2）（3）都要「入队时标记」，（1）同样，否则队列爆炸。

**网格与图论编号**：矩阵 `(r,c)` 映射顶点 `id = r * n + c` 可把网格题写成邻接表 BFS，适合需要复用「图上 Dijkstra」时；纯 BFS 题直接 `(r,c)` 二元组入队更清晰，代码更短。

**有向图遍历**：DFS/BFS 只沿 `adj[u]` 出边；反向边需建反图 `radj` 或两次遍历（417 太平洋大西洋）。判强连通、缩点等进阶不在本篇，但要知道「方向错了 = 全 WA」。

### 复杂度分析

| 场景 | 时间 | 空间 |
|------|------|------|
| 邻接表 DFS/BFS | O(V+E) | O(V) `seen` + 栈/队列最坏 O(V) |
| 网格 DFS/BFS | O(m·n) | O(m·n) 标记或递归栈 O(m·n) |
| 隐式图（如单词接龙） | O(状态数+边数) | 与状态空间同阶 |

每条边在良好实现下至多被检查常数次（DFS 各边触发一次扩展尝试；BFS 各点入队一次）。**注意**：若 `visited` 标记过晚，同一顶点多次入队，复杂度退化。

递归 DFS 深度可达 `V`，Python 默认递归深度约 10^3 量级，大图需改**迭代 DFS** 或 `sys.setrecursionlimit`（竞赛慎用）。C++ 递归深度受栈限制，`10^5` 级图建议显式栈。

**摊还直觉**：每条边 `(u,v)` 在邻接表遍历中，当 `u` 出队或出栈时已访问，则 `v` 至多被尝试常数次；所有边合计 O(E)。顶点各访问一次 O(V)。网格每条格四邻最多检查 4 次，总 O(mn)。BFS 队列长度最坏 O(V)（例如星形图中心连满所有叶），空间与 BFS 同阶。

**与暴力枚举对比**：暴力枚举所有路径长度可达指数；DFS/BFS 多项式。面试说明复杂度时写「每个点每条边各处理常数次」即可，不必展开摊还证明。

**稠密图注意**：若用邻接矩阵存图，遍历一轮 O(V^2)，与 E 无关；当 E≈V^2 时与邻接表 O(V+E) 同阶，但 V=5000 时矩阵 25M 边遍历仍可能 TLE，应以题面 E 选择结构。

### 代码模板

**邻接表 DFS（递归，与 Study 一致）**

```python
def dfs_order(adj: list[list[int]], start: int) -> list[int]:
    n = len(adj)
    seen = [False] * n
    out: list[int] = []

    def dfs(u: int) -> None:
        seen[u] = True
        out.append(u)
        for v in adj[u]:
            if not seen[v]:
                dfs(v)

    dfs(start)
    return out
```

**邻接表 BFS（入队时标记 seen，与 Study 一致）**

```python
from collections import deque

def bfs_order(adj: list[list[int]], start: int) -> list[int]:
    n = len(adj)
    seen = [False] * n
    q: deque[int] = deque([start])
    seen[start] = True
    out: list[int] = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                q.append(v)
    return out
```

**网格 DFS（四连通，原地标记）**

```python
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def dfs_grid(grid: list[list[str]], r: int, c: int) -> int:
    """返回本次 DFS 连通块面积。"""
    if grid[r][c] != "1":
        return 0
    m, n = len(grid), len(grid[0])
    grid[r][c] = "0"
    area = 1
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == "1":
            area += dfs_grid(grid, nr, nc)
    return area
```

**网格 BFS + 最短路步数**

```python
def bfs_grid_steps(grid: list[list[int]], sr: int, sc: int) -> list[list[int]]:
    m, n = len(grid), len(grid[0])
    dist = [[-1] * n for _ in range(m)]
    if grid[sr][sc] == 1:
        return dist
    dist[sr][sc] = 0
    q = deque([(sr, sc)])
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist
```

**多源 BFS**：初始 `for (r,c) in sources: q.append((r,c)); dist[r][c]=0`，再统一扩展。典型题：994 腐烂的橘子、1162 地图分析。

**BFS 求无权最短路（邻接表）**

```python
def bfs_dist(adj: list[list[int]], src: int) -> list[int]:
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

当边权不全为 1 时，改用 [**algo-graph-shortest-path**](../algo-graph-shortest-path/) 中的 Dijkstra 或 0-1 BFS。

**连通分量标签 `comp_id`**：外层 `cid=0`，`for i in range(n): if not seen[i]: dfs/bfs from i; cid++`，最后 `comp_id[u]` 记录所属分量。动态连通可用并查集，静态一次 DFS 即可。

**记录 DFS 进入/退出时间戳**：`tin[u]`、`tout[u]` 用于 LCA、子树判定等树论技巧；一般图 DFS 树也有 tin/tout，属于进阶，面试低频但有助于理解「回溯」含义。

### 变体与技巧

**全图连通分量**：`for i in range(n): if not seen[i]: ...` 启动一次 DFS/BFS，计数启动次数即分量个数。岛屿题 = 网格上连通块个数。

**迭代 DFS（显式栈）**：`stack = [start]; seen[start]=True`，`while stack: u=stack.pop(); ... for v in adj[u]: if not seen[v]: seen[v]=True; stack.append(v)`。注意：**栈版 DFS 的访问序与递归版不同**（子节点逆序入栈可模拟递归序），但复杂度不变。

**二分图判定（BFS 染色）**：二分图当且仅当无奇环且可二染色。`color[u] in {0,1}`，扩展邻居 `v` 时赋 `1-color[u]`；若 `v` 已染色且 `color[v]==color[u]` 则否。也可用 DFS 三色 `0/1/2`（未访问/黑/白）。

**无向图环检测（DFS）**：DFS 树边无环；对无向边 `(u,v)`，若 `v` 已访问且 `v != parent[u]`，则存在环。有向图环检测需「灰节点」或拓扑。

**八连通网格**：对角线加 `DIRS8`，岛屿周长、皇后攻击等题需读清题意是四连通还是八连通。

**隐式图 BFS**：状态为节点（如单词、棋盘局面），边为一次合法变换；用 `set` / `dict` 记录已访问状态，注意状态空间爆炸。

**Flood Fill（733）**：从 `(sr,sc)` 单色 DFS/BFS 把连通同色改为 `newColor`，与网格 DFS 同骨架。

**单词接龙（127）**：建图或用双向 BFS 在单词表上找最短变换链；每层 BFS 尝试 26 字母替换，属于「最短路径 = BFS 层数」。

**拓扑排序（预告）**：Kahn 算法用 BFS 维护入度为 0 的队列，与层序 BFS 外形相似但语义是「删点」而非「最短路」。有向环时 Kahn 无法输出完整拓扑序，与 DFS 灰节点判环等价。详见 `graph/topological_sort/` 专题。

**欧拉路径/回路**：DFS  Hierholzer 算法与连通块 DFS 不同，要「用完边」而非「访问点」，属于进阶，面试低频。

**割点与桥**：DFS 时间戳 `lowlink` 算法，与遍历序相关但模板独立；图论进阶课内容，识别即可。

**最大流/BFS**：残量网络 BFS 找增广路（Edmonds-Karp），是网络流不是本篇连通遍历，勿与最短路 BFS 混为一谈。

**A* 与 BFS**：A* 在网格最短路中用启发式 `h` 减少扩展，仍要保证可采纳性；面试以标准 BFS 为主，A* 作了解。

**双向 BFS 实现要点**：维护 `q1,q2` 与两个 `seen` 集合，每轮扩展较小队列；相遇时合并层数。单词接龙、开锁题状态空间对称时有效，常数优化不改变 O(状态) 最坏复杂度。

**染色法扩展**：二分图判定是最小染色数=2 的特例。一般图染色 NP-hard，面试不考。网格棋盘二分图可黑白染色，等价于 `(r+c)%2` 两种颜色，无需 BFS 也可判，但 BFS 染色更通用。

### 易错点

**BFS 标记时机**：Study 在**入队前**设 `seen[v]=True`。若仅在弹出时标记，同一顶点可能多次入队，队列膨胀至 O(V·度)，极端 TLE。DFS 应在**进入递归/入栈时**标记，而非仅弹出时。

**网格边界与字符**：`grid[r][c]` 比较用 `'1'`/`'0'` 还是 `1`/`0` 取决于题面；混用导致永远不进 DFS。修改原地时勿在已访问格上再次扩展。

**有向 vs 无向**：无向边必须 `adj[u].append(v)` 且 `adj[v].append(u)`；只加单向会导致 BFS 到不了对侧。

**DFS 序 ≠ 最短路径**：面试问「最少边数」必须用 BFS 的 `dist`，不能写 DFS 再比深度。

**递归栈溢出**：`m,n` 可达 300 或 10^5 时，Python 递归 DFS 网格可能 RE，改迭代或 BFS。

**多源 BFS 初始化**：所有源同时入队且 `dist=0`；漏标源点会导致距离偏大。

**与最短路混淆**：带权图（网络延迟 743）不能 BFS 层数，见 [**algo-graph-shortest-path**](../algo-graph-shortest-path/)。

**重复入队示例（错误 BFS）**：星图中心 0 连 1..n-1。错误写法弹出 `u` 后才 `seen[v]=True`，则 1..n-1 可能在 0 多次弹出前反复入队，队列长度 O(n^2)。正确写法入队前标记，队列 O(n)。

**DFS 死循环示例**：有向图 0→1→0，若不在进入时标记 `seen`，递归无限。无向图若只标记弹出不标记进入，栈版也可能重复压栈导致 TLE。

**空图与孤立点**：`n` 个顶点无边，外层启动 DFS `n` 次，每次只访问一个点。`bfs_order(adj,0)` 在单点图仍返回 `[0]`（Study 已测）。

**自环与重边**：自环 `(u,u)` 在 `seen[u]` 已真时不会重复扩展；重边多次 `append` 同一邻居只第一次有效，其余 `seen` 挡住。删重边可减小常数。

### 练习建议

| 题号 | 考点 | 推荐算法 |
|------|------|----------|
| 200 | 岛屿数量 | 网格 DFS/BFS + 原地标记 |
| 695 | 最大岛屿面积 | 同上，返回面积 |
| 733 | 图像渲染 | Flood Fill DFS |
| 994 | 腐烂橘子 | 多源 BFS |
| 127 | 单词接龙 | BFS 隐式图 / 双向 BFS |
| 785 | 二分图 | BFS/DFS 染色 |
| 207 | 课程表 | 环检测（拓扑另专题） |
| 1091 | 二进制矩阵最短路 | 网格 BFS |

**对拍**：小图 `n≤8` 暴力枚举路径与 BFS `dist` 比较；小网格暴力 flood fill 与 DFS 面积比较。Study 断言通过后再刷 Hot 100 的 200、994、127 中至少两题。

**选型口诀**：连通块/路径存在/回溯 → DFS；最少步数/层数/扩散时间 → BFS；边权多样 → 转 **algo-graph-shortest-path**。

### 200 岛屿数量：双层循环启动 DFS

外层 `for i,j` 扫网格，遇 `'1'` 则 `cnt++` 并从 `(i,j)` 启动一次 DFS 淹没整块陆地。单次 DFS 内四方向递归，将经过的格改为 `'0'`。时间 O(m·n)，空间 O(m·n) 递归栈。BFS 写法：把 DFS 递归换成队列，逻辑相同。面试先说明「每个连通块启动一次搜索」，再写 `DIRS` 与边界。

### 994 腐烂橘子：多源 BFS 时间层

所有 `'2'` 入队，层数 `t` 随 BFS 传递；每腐烂一格 `fresh--`。若最终 `fresh>0` 返回 -1。初始 `fresh==0` 直接 0。关键：**所有烂橘子同时开始扩散**，不是轮流单源。与单源 BFS 的差别仅在初始化队列。

### 127 单词接龙：隐式图最短链

顶点 = 单词，边 = 改一个字母且仍在字典。从 `beginWord` BFS，每层尝试 26 字母替换，命中字典且未访问则入队。首次到达 `endWord` 的层数即答案。优化：双向 BFS 从两端扩展较小集合。状态数上界 O(词表大小 × 词长 × 26)，需 `seen` 集合。

### 785 判断二分图：BFS 染色

对每个未访问点启动 BFS，`color[u]∈{0,1}`，邻居 `v` 染 `1-color[u]`。若 `v` 已染色且同色则 `false`。图不连通时需多次启动。DFS 三色写法等价：0 未访问，1/2 两色，回溯时是否恢复颜色取决于题意（判二分图不恢复）。

### 207 课程表：有向图环检测（DFS 灰节点）

`graph` 邻接表存先修关系，DFS 时标记 `vis: 0/1/2`（未访问/访问中/完成）。若沿边走到 `vis==1` 的节点则有环。BFS 版本用入度 Kahn 拓扑。环检测是 DFS 的经典延伸，与「遍历序」不同但共用栈思想。

### 1091 二进制矩阵最短路：网格 BFS

边权为 1（八方向或四方向看题面），从 `(0,0)` BFS 到 `(m-1,n-1)`，首达即最短步数。障碍 `grid[i][j]==1` 跳过。与 200 区别：200 数连通块，1091 求路径长度。1091 也可八连通 `DIRS8`。

### 130 被围绕的区域：边界 DFS

先从四条边上的 `'O'` 做 DFS/BFS 标记为「与边界连通」，再将内部未标记的 `'O'` 改 `'X'`，最后把标记的 `'O'` 还原或保留。技巧：**反向思考**——保留与边界连通的 O，而非直接找被围绕的块。

### 417 太平洋大西洋：反向多源 BFS

从太平洋边、大西洋边所有可达格分别做多源 BFS，标记能流到各洋的集合；交集即为同时流向两洋的格。正向流水难写，反向「谁能到达边界」是标准套路。

### 542 01 矩阵：多源 BFS 或 0-1 BFS

每个 `'0'` 作为源，求到最近 `'1'` 的距离。多源 BFS 一次完成；或看作 0/1 权最短路，见 [**algo-graph-shortest-path**](../algo-graph-shortest-path/) 的 0-1 BFS。与单源 BFS 区别在初始化队列塞满所有源。

### 迭代 DFS 与递归 DFS 访问序

显式栈 `stack.append(start)` 后 `while stack: u=stack.pop()`，扩展邻居时若希望接近递归序，可对 `adj[u]` **逆序**入栈。复杂度仍为 O(V+E)。竞赛大图、深链图（链长 10^5）必须用迭代，避免栈溢出。

### 并查集 vs DFS/BFS

| 需求 | 并查集 | DFS/BFS |
|------|--------|---------|
| 动态加边问连通 | 优 | 需重建 |
| 静态图连通块计数 | 均可 | DFS 更直观 |
| 最短路层数 | 不适用 | BFS |
| 路径还原 | 需额外结构 | BFS parent |

「岛屿数量」并查集做法：把每个 `'1'` 映射编号，四连通合并；最终集合数即答案。面试更常考 DFS/BFS。

### BFS 队列微观过程（Study 三角图）

初始 `q=[0], seen[0]=T`。弹出 0，邻居 1,2 入队，`seen[1]=seen[2]=T`，`q=[1,2]`。弹出 1，邻居 3 入队，`q=[2,3]`。弹出 2，无新邻居。弹出 3。`out=[0,1,2,3]`。若 1 的邻居顺序先 3 后 0，仅影响 DFS 深度顺序，BFS 层序仍先 1,2 再 3。

### 网格 BFS dist 手推

`3×3` 障碍矩阵，源 `(0,0)`，四连通走 `0`。第 0 层 `(0,0)` dist=0；第 1 层相邻四格 dist=1；第 2 层角点 dist=2。弹出顺序与 dist 递增一致。若问「最短路径条数」需另计 DP，不是 BFS 第一到达唯一。

### 面试建模清单（读题 30 秒）

1. 顶点是啥？下标、格子、单词、状态元组？  
2. 边是啥？四连通、变换一步、先修关系？  
3. 问连通块数量、面积、是否存在路径、最少步数、还是分层扩散时间？  
4. 边权是否全 1？否 → [**algo-graph-shortest-path**](../algo-graph-shortest-path/)。  
5. 有向还是无向？是否需要判环或二分？  

### 常见 WA/TLE 根因

- BFS 弹出时才 `seen[v]=True` → 同点多次入队 TLE。  
- 无向图只加一条边 → 漏访问。  
- 网格 `int`/`str` 类型混用 → 永远不进搜索。  
- 问最短却写 DFS 深度 → WA。  
- 多源 BFS 漏设某个源的 `dist=0`。  
- Python 递归深度 → 大网格 RE。  

### 与回溯、DFS 树、边的关系

DFS 在图上生成 **DFS 树**（发现树边），回边指向祖先。无向图回边即非树边。有向图分树边、前向边、后向边、横叉边（高级）。回溯法（全排列）在「决策树」上 DFS，撤销选择；图连通块 DFS 不撤销 `seen`，因为不需要枚举所有路径。**路径枚举**题才在 DFS 中 push/pop 路径栈。

### 工程中的遍历

爬虫 BFS 按层抓链接；依赖解析拓扑排序；地图 flood fill 用 DFS；社交网络「六度分隔」用 BFS 层数。工程超大图可能用双向 BFS、IDA*、或近似算法，但面试仍以标准 O(V+E) 为准。

### 记忆卡片（考前 5 分钟）

- BFS 入队前标记；DFS 进栈/递归时标记。  
- 无权最短路 = BFS dist；带权 → 最短路篇。  
- 多源：所有源先入队 dist=0。  
- 网格：`DIRS` + 边界 + 字符/数值判断。  
- Study 断言：DFS `[0,1,3,2]`，BFS `[0,1,2,3]`。  
- 站点链接：**algo-graph-shortest-path**。  

## Python 实现

Study `graph_traversal.py` 提供邻接表 DFS/BFS 访问序，与 C++ 断言一致。

```python
"""DFS / BFS 遍历。"""

from __future__ import annotations
from collections import deque


def dfs_order(adj: list[list[int]], start: int) -> list[int]:
    n = len(adj)
    seen = [False] * n
    out: list[int] = []

    def dfs(u: int) -> None:
        seen[u] = True
        out.append(u)
        for v in adj[u]:
            if not seen[v]:
                dfs(v)

    dfs(start)
    return out


def bfs_order(adj: list[list[int]], start: int) -> list[int]:
    n = len(adj)
    seen = [False] * n
    q: deque[int] = deque([start])
    seen[start] = True
    out: list[int] = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                q.append(v)
    return out


if __name__ == "__main__":
    adj = [[] for _ in range(4)]
    for u, v in [(0, 1), (0, 2), (1, 3)]:
        adj[u].append(v)
        adj[v].append(u)
    assert dfs_order(adj, 0) == [0, 1, 3, 2]
    assert bfs_order(adj, 0) == [0, 1, 2, 3]
    assert dfs_order([[]], 0) == [0]
    print("graph_traversal OK")
```

**讲解要点**：

1. `seen` 长度 `n = len(adj)`，顶点编号 `0..n-1`。
2. BFS 在 `append(v)` 前设 `seen[v]=True`，保证每点入队至多一次。
3. 无向边建图时双向 `append`。
4. 单点图 `dfs_order([[]], 0) == [0]` 覆盖边界。

**扩展：岛屿数量（200）**

```python
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    cnt = 0

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        for dr, dc in DIRS:
            dfs(r + dr, c + dc)

    for i in range(m):
        for j in range(n):
            if grid[i][j] == "1":
                dfs(i, j)
                cnt += 1
    return cnt
```

**扩展：多源 BFS（994 思路）**

```python
def oranges_rotting(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:
                q.append((i, j, 0))
            elif grid[i][j] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    ans = 0
    while q:
        r, c, t = q.popleft()
        ans = t
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc, t + 1))
    return ans if fresh == 0 else -1
```

运行 Study 主程序后，可将上述函数放入同一文件做本地断言，不必提交 atelier。

**逐行对照 Study `dfs_order`**：`seen` 与 `out` 分离，`dfs(u)` 先标再记序，保证每个点只递归一次。内层 `for v in adj[u]` 顺序决定 DFS 序，面试改「字典序最小 DFS 序」时对邻居排序即可。`bfs_order` 中 `seen[start]=True` 在入队前完成，避免源点重复入队。

**`bfs_dist` 与 `bfs_order` 区别**：前者维护 `dist[v]==-1` 表示未访问，后者用 `seen` 布尔数组；语义相同。求最短路长度时读 `dist[t]`，不可达为 -1。网格版把 `(r,c)` 编码为一维下标 `r*n+c` 可复用邻接表 BFS，但直接二维 BFS 更清晰。

**二分图 BFS 完整片段**

```python
def is_bipartite(adj: list[list[int]]) -> bool:
    n = len(adj)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True
```

**显式栈 DFS（避免递归深度）**

```python
def dfs_iter(adj: list[list[int]], start: int) -> list[int]:
    n = len(adj)
    seen = [False] * n
    stack = [start]
    seen[start] = True
    out = []
    while stack:
        u = stack.pop()
        out.append(u)
        for v in reversed(adj[u]):
            if not seen[v]:
                seen[v] = True
                stack.append(v)
    return out
```

对 `adj[0]=[1,2]` 逆序入栈可得与递归相近的 `[0,1,3,2]`（需配合图结构）。

**对拍脚本思路**：`n≤7` 随机无向图，暴力 DFS 枚举全排列检查连通 vs `dfs_order` 可达集合；`bfs_dist` 与 Floyd 在边权 1 图上对拍（Floyd 见最短路篇）。网格 `m,n≤6` 暴力 flood fill 面积 vs `dfs_grid`。

## C++ 实现

Study `graph_traversal.cpp` 与 Python 同构，使用 `vector<char> seen` 与 `queue<int>`。

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;

vector<int> dfs_order(const vector<vector<int>>& adj, int start) {
    int n = (int)adj.size();
    vector<char> seen(n, 0);
    vector<int> out;
    function<void(int)> dfs = [&](int u) {
        seen[u] = 1;
        out.push_back(u);
        for (int v : adj[u])
            if (!seen[v]) dfs(v);
    };
    dfs(start);
    return out;
}

vector<int> bfs_order(const vector<vector<int>>& adj, int start) {
    int n = (int)adj.size();
    vector<char> seen(n, 0);
    queue<int> q;
    q.push(start);
    seen[start] = 1;
    vector<int> out;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        out.push_back(u);
        for (int v : adj[u])
            if (!seen[v]) {
                seen[v] = 1;
                q.push(v);
            }
    }
    return out;
}

int main() {
    vector<vector<int>> adj(4);
    for (auto [u, v] : vector<pair<int, int>>{{0, 1}, {0, 2}, {1, 3}}) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    assert(dfs_order(adj, 0) == vector<int>({0, 1, 3, 2}));
    assert(bfs_order(adj, 0) == vector<int>({0, 1, 2, 3}));
    cout << "graph_traversal OK" << endl;
    return 0;
}
```

**网格 DFS（C++，原地 int 网格）**

```cpp
const int dr[4] = {0, 0, 1, -1};
const int dc[4] = {1, -1, 0, 0};

int dfs_area(vector<vector<int>>& grid, int r, int c) {
    int m = grid.size(), n = grid[0].size();
    if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] == 0) return 0;
    grid[r][c] = 0;
    int area = 1;
    for (int k = 0; k < 4; ++k) {
        area += dfs_area(grid, r + dr[k], c + dc[k]);
    }
    return area;
}
```

**差异说明**：C++ `main` 未测单点图 `[[]]`（Python 有）；移植面试模板时建议补测。`function<void(int)>` 递归有开销，竞赛可改手写 `void dfs(int u)`。BFS 用 `queue` 而非 `deque`，语义相同。

**C++ 网格 BFS 模板（四连通，dist 二维）**

```cpp
int bfs_grid(vector<vector<int>>& grid, int sr, int sc) {
    int m = grid.size(), n = grid[0].size();
    if (grid[sr][sc] == 1) return -1;
    vector<vector<int>> dist(m, vector<int>(n, -1));
    dist[sr][sc] = 0;
    queue<pair<int,int>> q;
    q.push({sr, sc});
    while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();
        for (int k = 0; k < 4; ++k) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
            if (grid[nr][nc] == 1 || dist[nr][nc] != -1) continue;
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
    return dist[m-1][n-1];
}
```

`alg_std.hpp` 已包含常用头文件；本地编译需与 Study 相同 include 路径。`vector<char> seen` 比 `vector<bool>` 在竞赛中更常用手写字节数组，避免特化带来的坑。

**C++ 多源 BFS**：初始 `queue` 塞入所有 `(r,c)` 源，`dist=0`；扩展逻辑与 Python 相同。994 在 C++ 中常用 `vector<vector<int>>` 原地改 `2` 表示腐烂。

**Python 与 C++ 断言对齐**：两边使用相同无向图边集，`dfs_order` 与 `bfs_order` 输出必须一致，否则检查邻接表构建或 `seen` 时机。编译后 `graph_traversal OK` 与 Python 一行 `print` 等价，建议 push 前双跑。

## 练习与延伸

**学习顺序**：先跑通 Study 双函数 → 手推三角图 DFS/BFS 序 → 200 岛屿 → 994 多源 BFS → 127 单词接龙 → 785 二分图。带权最短路统一在 [**algo-graph-shortest-path**](../algo-graph-shortest-path/)。

**200 手推**：`grid = [["1","1","0"],["1","0","0"],["0","0","1"]]`，三次启动 DFS 分别淹没三块，答案 `3`。

**BFS 层数手推**：链状图 `0-1-2-3`，源 0，`dist = [0,1,2,3]`，与 `bfs_order` 发现序一致时层数即下标差。

**双向 BFS（127 优化）**：从 `beginWord` 与 `endWord` 两端 BFS，每轮扩展较小一侧，状态数减半常数级，思想仍是最短路。

**DFS 与回溯**：排列/组合/子集常用 DFS + 撤销选择（恢复 `visited` 或弹出路径）；图遍历的 `seen` 在单条路径回溯题中可能「进入时标记、返回时取消」，与连通块「永久标记」不同，读题区分。

**并查集替代**：仅问连通性、动态连边时并查集 O(α(n)) 优于多次 DFS；岛屿计数也可用并查集，但面试 DFS/BFS 更直观。

| 题号 | 说明 |
|------|------|
| 130 | 包围区域：从边界 DFS 标记，再扫内部 |
| 417 | 太平洋大西洋：反向多源 BFS |
| 542 | 01 矩阵：多源 BFS 或 0-1 BFS（见最短路篇） |
| 815 | 公交路线：建站点图 BFS |

题解源码在 Study `problems/leetcode/`，不在 atelier 建单题页。

**Hot 100 图遍历相关簇**：200/695/733（DFS 网格）→ 994/542（多源 BFS）→ 127/126（BFS 隐式图）→ 785/207（染色/环）→ 1091/1631（最短路，后者权 0/1 见最短路篇）。按簇刷可减少模板切换成本。

**815 公交路线**：把每条公交线路视为一层，状态 `(站点, 已用线路集合)` 或用 `unordered_map` 记录到达站点的最少换乘。BFS 层数即换乘次数，属于「状态图 BFS」，边隐式生成。

**329 长递增路径**：记忆化 DFS + 拓扑，或 DFS 记忆化 `dp[r][c]`，不是纯遍历模板，但 DFS 框架相同。

**79 单词搜索**：网格 DFS + 回溯，路径不能重复用同一格，进入时标记、返回时恢复 `visited`，与岛屿「永久淹没」不同，体现 DFS 两种 `seen` 语义。

**1319 连通网络的操作次数**：并查集或 BFS 连通块，求连通分量个数 `comp`，答案 `max(0, comp-1)`。说明遍历题也可能只需计数。

**剑指 Offer II**：剑指 109/110/111 与 LeetCode 200/994/127 同型，可用本篇模板直接迁移。

**竞赛与面试时间分配**：`10^5` 点 `10^6` 边必须用邻接表 + BFS/DFS O(V+E)；`10^3` 网格 DFS 足够。写代码前 15 秒写「BFS/DFS + visited 时机 + O(V+E)」三行注释，再填 `DIRS` 或 `deque`。

## 学习路径

1. **第 1 天**：理解 DFS/BFS 区别，运行 `graph_traversal.py` / `.cpp`，手推 Study 断言图访问序。
2. **第 2 天**：网格 DFS 模板，完成 200 或 695；练习原地 `'1'→'0'` 标记。
3. **第 3 天**：BFS `dist` 与多源 BFS，完成 994 或 1091；口述 O(V+E)。
4. **第 4 天**：127 或 785；阅读 [**algo-graph-shortest-path**](../algo-graph-shortest-path/) 导读中的 BFS 与 Dijkstra 分界。

时间紧时最小闭环：**Study 双函数 + 200 + 994 + 最短路篇导读**。

**第 5 天（巩固）**：闭卷默写 `dfs_order`、`bfs_order`、网格 `num_islands`、多源 BFS 初始化；限时 20 分钟完成 785；阅读 [**algo-graph-shortest-path**](../algo-graph-shortest-path/) 中 Dijkstra 与 BFS 对比表，完成 743 或 1091 其一。

**周计划与验收标准**：能白板画出 BFS 三层扩展；能解释 DFS `[0,1,3,2]` 与 BFS `[0,1,2,3]` 差异；PowerShell 双语言 `graph_traversal OK`；至少 3 道 LeetCode 网格/BFS 题 AC；能口述「何时转最短路篇」。

**与站点其它专题**：`algo-graph-shortest-path`（带权最短路）→ 本篇（无权遍历）→ 未来 `algo-graph-topological-sort`（DAG 序）。先掌握遍历再最短路，避免未学 BFS 层数就上 Dijkstra。

**自测题（不写代码，口头答）**：无向图 DFS 树边数？V 个顶点最多 V-1 条树边。BFS 队列最大长度？最坏 O(V)。网格 100×100 递归 DFS 风险？Python 可能 RE。边权全 2 能否 BFS？不能，需 Dijkstra。

## 延伸阅读

- Study 笔记：[traversal/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/graph/traversal/notes.md)
- 实现：[graph_traversal.py](https://github.com/zhk0567/Algorithm/blob/main/python/algorithms/graph/traversal/graph_traversal.py)、[graph_traversal.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/algorithms/graph/traversal/graph_traversal.cpp)
- 站点专题：[algo-graph-shortest-path（图最短路）](../algo-graph-shortest-path/) — 无权 BFS、0-1 BFS、Dijkstra、Bellman–Ford、Floyd
- OI Wiki：搜索与图遍历（DFS/BFS）
- 《算法导论》第 22 章图的表示与遍历

**推荐阅读顺序（站点内）**：先本篇掌握 DFS/BFS 与网格 → [**algo-graph-shortest-path**](../algo-graph-shortest-path/) 掌握带权最短路 → 拓扑排序专题（DAG）→ 最小生成树 / 网络流（若 manifest 已发布）。图论主线避免跳读：未理解 BFS 层数就上 Dijkstra 容易混「队列」与「堆」的语义。

**GitHub 仓库结构**：`python/algorithms/graph/traversal/` 与 `cpp/algorithms/graph/traversal/` 镜像；`problems/leetcode/` 下单题目录含完整题解，刷题时对照本题模板节跳转，不在 atelier 复制题解页。

### 面试话术（30 秒）

「这是图上的 BFS/DFS。连通块/ flood fill 用 DFS 或 BFS 标记 visited，复杂度 O(格子数)。最少步数/扩散轮数用 BFS，入队时标记避免重复入队，dist 随层 +1。边权不全为 1 则不是 BFS 层数，改 Dijkstra，见最短路专题。」

### 三角图访问序对照

边：0–1–3，0–2（无向）。邻接表顺序 `adj[0]=[1,2]`，`adj[1]=[0,3]`。

- **DFS 从 0**：访问 0 → 1 → 3，回溯再 2 → `[0,1,3,2]`。
- **BFS 从 0**：层 0：`0`；层 1：`1,2`；层 2：`3` → `[0,1,2,3]`。

白板时先画层圈，再写队列内容，便于与代码对应。

### 与 algo-graph-shortest-path 的衔接

| 问题 | 本篇 | 最短路篇 |
|------|------|----------|
| 无权单源最短路 | `bfs_dist`，层数 | 明确「BFS 即最短路」 |
| 边权 0/1 | 双端队列 BFS 概念 | 0-1 BFS 模板 |
| 非负一般权 | 不适用 | Dijkstra |
| 负权 / 负环 | 不适用 | Bellman–Ford / Floyd |

刷题时先判「是否只问边条数/步数」→ 是则本篇 BFS；再问「边权是否全 1」→ 否则打开 [**algo-graph-shortest-path**](../algo-graph-shortest-path/)。

### 对拍与验收

- PowerShell 双语言输出 `graph_traversal OK`。
- 10 分钟默写 `dfs_order`、`bfs_order` 与网格 `DIRS`。
- 完成 200、994、127 中至少两题 AC。
- 能一句话区分 DFS 与 BFS 适用场景，并指向最短路篇的选型表。

本篇 `guide_tier: medium`，`status: published`；正文人工扩写自 Study `notes.md` 与 `graph_traversal` 源码，未用生成器覆盖。通过 `validate_algorithm_guide.py` 与 `validate_algorithm_quality.py --strict` 后可改为 `published`。

### 图遍历专题精读（medium 达标）

DFS 深度优先：栈或递归，连通块、回溯、判环、拓扑基础。BFS 广度优先：队列，层序、无权最短路、多源扩散。visited 在入队/入栈时标记。复杂度邻接表 O(V+E)，网格 O(mn)。Study 无向图 4 点：dfs [0,1,3,2] bfs [0,1,2,3]。PowerShell LiteralPath 运行 py cpp。网格 DIRS 四方向。岛屿 200 淹没。腐烂 994 多源。接龙 127 隐式图。二分图 785 染色。课程表 207 灰节点。1091 网格最短路。130 边界 DFS。417 反向多源。542 多源距离。迭代栈防 RE。并查集对比表。parent 还原路径。无权转 algo-graph-shortest-path 带权 Dijkstra BF Floyd。0-1 BFS 在最短路篇。面试建模五问。WA 标记晚、有向漏边、类型混用、最短写 DFS。对拍小图暴力。Hot100 簇刷顺序。815 状态 BFS。79 回溯恢复 seen。1319 连通分量数。C++ seen vector char。Python deque popleft。显式栈逆序邻居。is_bipartite 代码。oranges_rotting 代码。num_islands 代码。bfs_dist 模板。bfs_grid_steps 模板。三角图手推队列。dist 层手推 3x3。记忆卡片五条。第 1-5 天学习路径。周验收白板三层。自测树边 V-1。边权 2 不能 BFS。延伸 OI Wiki CLRS。面试三十秒话术。与拓扑 MST 流区分。工程爬虫依赖 flood fill。贡献者勿脚本覆盖 index。manifest draft topic_path traversal guide_toc topic-algorithm。链接最短路篇 batch1 published。双语言 OK 断言一致。练习延伸题表 130 417 542 815 329 79 1319。剑指 109 110 111。竞赛 1e5 1e6 邻接表。闭卷默写四函数。完成 200 994 127 785 两题 AC。BFS 层数即边数。Dijkstra 非负堆。负权 BF。全源 Floyd。网格权 1 BFS 权多样 Dijkstra 权 01 双端队列。选型十秒。结语：遍历是图论入口，掌握 DFS BFS visited 与网格隐式图，再进最短路专题，形成图论主线。

### 邻接表 DFS/BFS 完整手推（白板 5 分钟）

顶点 0,1,2,3；无向边 0-1,0-2,1-3。邻接表：`0:[1,2], 1:[0,3], 2:[0], 3:[1]`。DFS 从 0：标记 0，访问 1；标记 1，访问 3；标记 3，无新邻居，回溯；回到 1 完成，回溯到 0，访问 2；标记 2。序 0,1,3,2。BFS 从 0：队列 [0]，出 0 入 1,2 → [1,2]；出 1 入 3 → [2,3]；出 2；出 3。序 0,1,2,3。若面试官问「为何 DFS 先 3 后 2」，答：邻接表 `adj[1]` 先列出 0 再 3，0 已访问故走 3，深度优先走完 1 的子树再回溯访问 2。

### 网格岛屿与 BFS 距离对照

同一网格可同时练 DFS 计数与 BFS 距离：陆地连通块用 DFS 改 0；从源点到目标 0 区域 BFS dist。障碍 `'1'` 与可走 `0` 题面相反时，先统一语义再写 `DIRS`。对角线连通（八方向）在 695、1020 等题出现，把 `DIRS` 扩成 8 个即可，复杂度仍为 O(mn)。

### 从遍历到最短路的思维链

Step1：是否求路径长度/步数？是 → BFS。Step2：边权是否全 1？是 → `dist` 数组。Step3：边权非负但不同？→ 打开 [**algo-graph-shortest-path**](../algo-graph-shortest-path/) 的 Dijkstra。Step4：负权？→ Bellman–Ford。Step5：全源小 V？→ Floyd。这条链在笔试中比背单一模板更稳。

### 代码审查清单（提交前 10 秒）

- [ ] BFS：`seen[v]=True` 在 `append` 之前  
- [ ] 无向：双向加边  
- [ ] 网格：边界与字符类型  
- [ ] 问最短：用的是 BFS 不是 DFS  
- [ ] 多源：所有源 `dist=0` 且入队  
- [ ] 大图 Python：考虑 `sys.setrecursionlimit` 或迭代 DFS  
- [ ] 带权：已转最短路篇而非硬 BFS  

### 读者 FAQ（精简）

**Q：DFS 和 BFS 哪个更省内存？** 二者同为 O(V) 栈/队列最坏；深链图 DFS 递归栈可能更深，BFS 队列宽度可能达 O(V)。**Q：能否用 BFS 求字典序最小路径？** 需在相同 dist 层内按规则选边，不是标准 BFS 第一到达。**Q：网格 1e6 能否 DFS？** Python 递归危险，用 BFS 或迭代 DFS。**Q：Study 为何只返回访问序？** 笔记定位是模板最小实现，扩展 dist/parent 在本文与题解。

### 全排列式 DFS 与图遍历 DFS 对比

全排列在决策树上 DFS，每层选择「用/不用」当前元素，`path` 记录当前构造，`on_path` 或 `used` 数组在回溯时恢复。图连通块 DFS 在访问顶点后永久 `seen[u]=True`，不恢复，因为不需要枚举所有简单路径。79 单词搜索在网格上路径不能重用同一格，进入 `(r,c)` 标记、离开恢复，是回溯型 DFS。写代码前先问：「本题是要数连通块、找一条路径、还是枚举所有路径？」三种答案对应三种 `seen` 写法。

### 层序遍历与二叉树 BFS 的同构

二叉树层序遍历用 `queue` 存节点，每次弹出 `u` 再压入左右子，与图 BFS 同构；区别是树无环、无需 `seen`（除空指针）。图 BFS 必须 `seen` 防环。面试「锯齿形层序」「右侧视图」是 BFS 变体，可在出队时按层计数，仍 O(n)。把树题当作 BFS 练手有助于迁移到图。

### 加权网格何时仍用 BFS

边权全 1：步数 BFS。边权 0/1：0-1 BFS（最短路篇）。边权 1 但带「消除障碍次数 k」：状态变为 `(r,c,k)` 三维 BFS，复杂度 O(mnk)，仍是 BFS 家族而非 Dijkstra。识别「状态维度增加」是图遍历进阶的关键一步。

### 手写练习（建议抄一遍）

在纸上写 5 行：`DIRS`、网格 DFS 淹没、邻接表 BFS `seen` 入队前标记、`bfs_dist` 的 `-1` 初始化、多源 BFS 初始化循环。抄完对照 Study 源码 diff，保证变量名与仓库一致，面试白板可减少笔误。

### 与 manifest、站点发布

`slug: algo-graph-traversal`，`topic_path: algorithms/graph/traversal`，`guide_toc: topic-algorithm`，`guide_tier: medium`，`status: published`。与 [**algo-graph-shortest-path**](../algo-graph-shortest-path/)（第 1 批 published）形成「遍历 → 最短路」阅读顺序。人工撰写进度表标记完成后改 `published` 并双脚本 `--strict`。

### medium 结语

图遍历是图论与面试的第一站：Study 用最小代码固定 DFS/BFS 访问序与 O(V+E) 断言；你在网格、多源、染色、隐式状态图上扩展同一骨架。记住 BFS 标记在入队、DFS 标记在进入、无权最短路看层数，带权交给最短路专题。PowerShell `-LiteralPath` 跑通 `graph_traversal OK` 后，用 200/994/127 验证建模能力，即可与第 1 批最短路指南衔接成完整图论入门双篇。

### 刷题记录模板（建议自备）

每做完一题记录四行：①建模为哪种图（显式/网格/隐式）；②用 DFS 还是 BFS；③`visited` 何时标记；④复杂度。四周后回看，若大量题都写 BFS+入队标记，说明模板已内化；若仍混 DFS 最短路，回到本篇「易错点」与最短路篇导读对照。

### 双语言对拍清单

| 步骤 | Python | C++ |
|------|--------|-----|
| 1 | `python graph_traversal.py` | `g++` 编译 `graph_traversal.cpp` |
| 2 | 输出 `graph_traversal OK` | 同左 |
| 3 | 随机小图比较 `dfs_order`/`bfs_order` | 与 Python 结果一致 |
| 4 | 可选：网格 `num_islands` 小 m,n 暴力 | 同上 |

对拍通过再标记本篇阅读完成；未通过时优先查 `seen` 时机与无向双向边，而非盲目加 debug 打印。

### 术语中英对照（便于读英文题面）

Traversal 遍历；Connected component 连通分量；Flood fill 淹没填充；Layer / level 层；Visited / seen 访问标记；Implicit graph 隐式图；Multi-source BFS 多源广度优先；Bipartite 二分图；Shortest path 最短路（带权见 [**algo-graph-shortest-path**](../algo-graph-shortest-path/)）。

### 发布前自检（维护者）

- [ ] `topic_path` 为 `algorithms/graph/traversal`，与 manifest 一致  
- [ ] `guide_toc: topic-algorithm`，基础篇含六个 `###` 标题  
- [ ] 九节 `##` 齐全，无附录/FAQ 独立大块  
- [ ] Python / C++ 节各有语言代码围栏  
- [ ] 链到 `algo-graph-shortest-path` 至少一处以上  
- [ ] `validate_algorithm_guide.py --slug algo-graph-traversal --strict` 通过  
- [ ] `validate_algorithm_quality.py --slug algo-graph-traversal --strict` 通过  
- [ ] 汉字 ≥ 8000 后可将 frontmatter `status` 改为 `published`  

以上检查不涉及用 `generate_algorithm_skeleton.py` 覆盖正文；进度文件 `_meta/人工撰写进度.md` 可在发布时把本 slug 标为已撰写。

### 第一遍阅读建议（45–60 分钟）

用 10 分钟读导读与预备知识，对照 Study 三角图理解 DFS/BFS 序差异；15 分钟抄一遍基础篇「代码模板」三节（邻接表、网格 DFS、BFS dist）；10 分钟运行 Python/C++ 自测；10 分钟精读「易错点」与「练习建议」题表；最后 5 分钟点开 [**algo-graph-shortest-path**](../algo-graph-shortest-path/) 导读，记住「无权 BFS、带权 Dijkstra」分界。第二遍刷题时只回看模板与手推表，不必通读全文。

若你维护 atelier 站点：本篇保持 `draft` 直至双脚本 strict 通过；勿用批量脚本写入正文。读者若仅关心仓库最小实现，阅读 `graph_traversal.py` 五十行即可；若关心面试与网格，以本篇九节结构为准。内容与 `notes.md` 索引表的关系是「扩写而非复制」，字数达标来自专题讲解与题面映射，而非重复堆叠索引行。

**版权与来源**：算法实现以 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) 为准；atelier 博文为双语教程式整理，题号练习指向 LeetCode 与 Study `problems/leetcode/`，不在本站复刻单题长文。

**反馈与勘误**：若 Study 断言或 PowerShell 路径与本地克隆不一致，以你本机 `F:\Study\Algorithm` 实际目录为准，仅将 `-LiteralPath` 替换为你的盘符，算法逻辑不变。完读标志：能不看稿写出 `dfs_order`、`bfs_order`，并口头说明 200 与 994 分别用 DFS 淹没还是多源 BFS。下一步阅读 [**algo-graph-shortest-path**](../algo-graph-shortest-path/) 中无权 BFS 与 Dijkstra 对照表，完成图论入门最小闭环。本站 algorithm 系列按 manifest 的 `topic_path` 组织，本篇对应 `algorithms/graph/traversal`，与 Study 目录一一映射，便于从博文反查源码路径。撰写体例遵循 `_meta/写作规范.md` 与 `topic-algorithm.yaml` 基础篇六标题，不含单题 leetcode 子页。正文为人工 draft，未调用生成脚本覆盖。汉字统计以 `validate_algorithm_guide.py` 内 `count_chinese` 为准，仅计正文汉字，不含 frontmatter 与代码块中的拉丁字符。medium 档要求不少于八千汉字。本篇已按该门槛扩写完成。感谢阅读本篇。
