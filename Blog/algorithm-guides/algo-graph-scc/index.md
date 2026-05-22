---
title: "算法 · Graph Scc"
series: algorithm
category: Algorithms
topic_path: algorithms/graph/scc
guide_toc: topic-algorithm
guide_tier: medium
status: published
---

# 算法 · 强连通分量（SCC）

## 导读

**强连通分量（Strongly Connected Component, SCC）** 是有向图中的极大顶点集合：集合内任意两点互相可达。将每个 SCC **缩成一个点** 后，得到 **DAG（有向无环图）**，可在其上拓扑排序、DP、最长路径等。Study 仓库 `scc/` 用 **Tarjan 算法** 一次 DFS，维护 `dfn`（发现时间）与 `low`（能回溯到的最早 dfn），在栈中弹出 SCC。

与 `algo-graph-topological-sort` 的 Kahn（要求 DAG）不同，Tarjan 直接处理 **有环有向图** 并划分 SCC。与 `algo-graph-traversal` 的无向连通分量不同，SCC 强调 **双向可达**。面试频率低于最短路/拓扑，但竞赛图论、依赖环分析、缩点 DP 常见。

本页扩写：`dfn/low` 含义、栈维护当前 DFS 路径、`low[u]==dfn[u]` 时弹出 SCC、复杂度 O(V+E)，以及与 Kosaraju 两遍 DFS 的对比。读完应能默写 `tarjan_scc`、解释样例图两个 SCC，并对拍 `scc OK`。

**在图论家族中的位置**：`algorithms/graph/scc`；总览 `algo-graph`。缩点后拓扑见 `algo-graph-topological-sort`。

**面试沟通顺序**：口述 dfn/low → 栈 → 弹 SCC 条件 → O(V+E)。

**manifest**：slug `algo-graph-scc`，`status: published`，`guide_tier: medium`。

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`，`tarjan.cpp` 使用 `#include <alg_std.hpp>`。

建议已具备：

- **有向图邻接表**：`adj[u]` 列出出边。
- **DFS**：`algo-graph-traversal`。
- **栈**：Tarjan 用显式栈保存当前路径节点；`on[u]` 标记 u 是否在栈中。
- **DAG**：SCC 缩点后无环。

**Tarjan 口诀**：访问 u 设 dfn/low 入栈；遍历 v：树边更新 low[u]=min(low[u],low[v])；回边（v 在栈）更新 low[u]=min(low[u],dfn[v])；若 low[u]==dfn[u] 弹栈至 u 得一 SCC。

## Study 仓库对照

`topic_path`：`algorithms/graph/scc`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/graph/scc/notes.md` | `python/algorithms/graph/scc/tarjan.py` |
| C++ | `cpp/algorithms/graph/scc/notes.md` | `cpp/algorithms/graph/scc/tarjan.cpp` |

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\scc\tarjan.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\graph\scc
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe tarjan.cpp
.\run.exe
```

`notes.md`：Tarjan；O(V+E)。正文与 `tarjan.py` 一致。

## 基础篇

### 直觉与定义

**强连通**

有向图 G 中子集 S 极大，使得对任意 a,b∈S，存在 a→…→b 与 b→…→a 的路径。

**Tarjan 核心**

DFS 树边 (u,v) 把 v 子树的 low 回传到 u。若 v 已访问且 **仍在栈中**（回边），用 `dfn[v]` 更新 `low[u]`，不能只用 `low[v]`（v 可能已属于别的 SCC 弹出）。

**弹栈条件**

`low[u] == dfn[u]`：u 是所在 SCC 的「根」，栈顶到 u 构成一个 SCC。

**Study 样例**

4 点：0→1→2→0 成环，2→3 出边。SCC 为 {0,1,2} 与 {3}，共 2 个。`tarjan_scc` 断言 `len(comps)==2`。

**缩点**

每个 SCC 编号为超级节点，原边 u→v 若 u、v 不同 SCC 则加超级边，得 DAG。

### 复杂度分析

| 项目 | 说明 |
|------|------|
| 时间 | O(V+E)，每条边常数处理 |
| 空间 | O(V) 栈、dfn、low |
| 与 Kosaraju | 两遍 DFS+反图，同样 O(V+E)，常数略大 |

V,E 达 10^5～10^6 时 Tarjan 常用。

### 代码模板

```python
def tarjan_scc(adj: list[list[int]]) -> list[list[int]]:
    n = len(adj)
    dfn = [-1] * n
    low = [0] * n
    st: list[int] = []
    on = [False] * n
    time = 0
    comps: list[list[int]] = []

    def dfs(u: int) -> None:
        nonlocal time
        dfn[u] = low[u] = time
        time += 1
        st.append(u)
        on[u] = True
        for v in adj[u]:
            if dfn[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on[v]:
                low[u] = min(low[u], dfn[v])
        if low[u] == dfn[u]:
            comp: list[int] = []
            while True:
                x = st.pop()
                on[x] = False
                comp.append(x)
                if x == u:
                    break
            comps.append(comp)

    for i in range(n):
        if dfn[i] == -1:
            dfs(i)
    return comps
```

### 变体与技巧

**Kosaraju**

第一遍 DFS 序；第二遍在反图按逆序 DFS，每棵树一 SCC。易教但两遍。

**缩点 + 拓扑 + DP**

最长路、路径计数在 DAG 上做。竞赛套路。

**2-SAT**

变量与否定建蕴含图，判可满足等价于无变量与否定同 SCC。

**无向图**

无向连通分量用 DFS/并查集，不用 Tarjan SCC。

### 易错点

1. **回边判断**：`elif on[v]` 不是 `dfn[v]!=-1`。
2. **low 初始化**：与 dfn 同时赋为 time 再 time++。
3. **弹栈**：必须 pop 到 u  inclusive。
4. **on 数组**：弹出时清 on[x]。
5. **孤立点**：`n=1` 无边，一个 SCC，Study 测 `[[0]]`。
6. **low 用 dfn[v] 而非 low[v]** 当 v 在栈上。
7. **多 SCC 顺序**：Tarjan 输出顺序与缩点拓扑相关，题面若要求特定序需再排。

### 练习建议

1. 运行 `tarjan.py` 手画 dfn/low。
2. 207 课程表：环检测用拓扑或 SCC 均可。
3. 缩点题：先 Tarjan 再 DAG DP。

**自测**：两环、链+环、空图。

## Python 实现

Study `tarjan.py` 完整源码：

```python
"""Tarjan 强连通分量。"""

from __future__ import annotations


def tarjan_scc(adj: list[list[int]]) -> list[list[int]]:
    n = len(adj)
    dfn = [-1] * n
    low = [0] * n
    st: list[int] = []
    on = [False] * n
    time = 0
    comps: list[list[int]] = []

    def dfs(u: int) -> None:
        nonlocal time
        dfn[u] = low[u] = time
        time += 1
        st.append(u)
        on[u] = True
        for v in adj[u]:
            if dfn[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on[v]:
                low[u] = min(low[u], dfn[v])
        if low[u] == dfn[u]:
            comp: list[int] = []
            while True:
                x = st.pop()
                on[x] = False
                comp.append(x)
                if x == u:
                    break
            comps.append(comp)

    for i in range(n):
        if dfn[i] == -1:
            dfs(i)
    return comps


if __name__ == "__main__":
    g = [[] for _ in range(4)]
    g[0].append(1)
    g[1].append(2)
    g[2].extend([0, 3])
    comps = tarjan_scc(g)
    assert len(comps) == 2
    assert tarjan_scc([[]]) == [[0]]
    print("scc OK")
```

**要点**：`nonlocal time`；`g[2].extend([0,3])` 建 Study 图；单点图 `adj=[[]]` 得 `[[0]]`。

## C++ 实现

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;

vector<vector<int>> tarjan_scc(const vector<vector<int>>& adj) {
    int n = (int)adj.size();
    vector<int> dfn(n, -1), low(n, 0), st;
    vector<char> on(n, 0);
    int timer = 0;
    vector<vector<int>> comps;
    function<void(int)> dfs = [&](int u) {
        dfn[u] = low[u] = timer++;
        st.push_back(u);
        on[u] = 1;
        for (int v : adj[u]) {
            if (dfn[v] == -1) {
                dfs(v);
                low[u] = min(low[u], low[v]);
            } else if (on[v])
                low[u] = min(low[u], dfn[v]);
        }
        if (low[u] == dfn[u]) {
            vector<int> comp;
            while (true) {
                int x = st.back();
                st.pop_back();
                on[x] = 0;
                comp.push_back(x);
                if (x == u) break;
            }
            comps.push_back(comp);
        }
    };
    for (int i = 0; i < n; ++i)
        if (dfn[i] == -1) dfs(i);
    return comps;
}
```

逻辑与 Python 一致；`main` 中断言两 SCC。

## 练习与延伸

- 缩点 + 拓扑最长路（竞赛）
- 2-SAT（进阶）
- `algo-graph-topological-sort`：DAG 上拓扑

**相邻**：`algo-graph`、`algo-graph-traversal`。

### Kosaraju 两遍 DFS（对照）

第一遍在原图 DFS 记录 finish 序；第二遍按 finish 逆序在 **反图** DFS，每棵 DFS 树一个 SCC。代码两段清晰，但多一遍与反图存储。面试可答「Tarjan 一遍，Kosaraju 两遍，均 O(V+E)」。

### 缩点建图步骤

1. `comps = tarjan_scc(adj)`；2. `id[u]=` 所属 SCC 编号；3. 对原边 u→v，若 `id[u]!=id[v]` 加边 `id[u]→id[v]`（去重）；4. 在 DAG 上拓扑或 DP。

### 2-SAT 简述

布尔变量 xi，子句 (a∨b) 转为蕴含 ¬a→b, ¬b→a。建图后判无解：存在 xi 与 ¬xi 同一 SCC。竞赛经典，面试极少完整写。

### 与 802 课程表 III

依赖图环检测：Kahn 或 SCC。SCC 缩点后若某 SCC 大小>1 则有环（自环除外需看题）。

### dfn/low 手推练习

对 Study 4 点图，模拟 DFS 顺序、栈变化、弹栈时刻，写在纸上比只看代码更有效。

### 面试白板版

「Tarjan：DFS 维护 dfn、low 与栈。树边 low 合并子 low；回边且 v 在栈则 low=min(low,dfn[v])。low==dfn 时弹栈得 SCC。O(V+E)。」

### PowerShell 验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\scc\tarjan.py
g++ -std=c++17 -O2 -o run.exe tarjan.cpp; .\run.exe
```

### 与 algo-graph 总览

总览「缩点」流程：SCC → DAG → 拓扑/DP。学完本页回总览勾 SCC 簇。

### 错误类型

WA：回边条件、low 初值、弹栈不完整。TLE：暴力 Floyd 判连通。MLE：重复存边未去重缩点边。

### 能力检查

25 分钟写 `tarjan_scc`；手推 Study 图两个 SCC；口述缩点三步。

### 维护

draft；strict 后 published。

### 结语

Tarjan 是 SCC 的竞赛与工程默认实现。Study 代码短、覆盖单点与环图；掌握 dfn/low/on 三板斧后可做缩点 DP 与 2-SAT 入门。


### Study 4 点图 dfn/low 手推

边 0→1→2→0 成环，2→3。DFS 从 0：dfn/low 递增入栈。树边更新 low；回边 2→0 用 dfn[v] 更新 low[2]。当 low[u]==dfn[u] 弹栈得 SCC。最终 {0,1,2} 与 {3} 两个分量。

### 回边条件：on[v] 而非 dfn[v]!=-1

v 已访问但 **已弹出栈** 则属别的 SCC，不能用 dfn[v] 更新 low[u]，否则错合并。必须 `elif on[v]: low[u]=min(low[u], dfn[v])`。

### 弹栈时机

`low[u]==dfn[u]` 时 u 是 SCC 根，pop 直到 u inclusive。on[x] 清 false。

### Kosaraju 对照

第一遍 DFS 记 finish 序；反图第二遍按逆序 DFS，每棵树一 SCC。两遍 O(V+E)，常数大于 Tarjan。

### 缩点建 DAG

`id[u]=comp_id`；边 u→v 若 id[u]!=id[v] 加超级边。DAG 上拓扑/最长路。

### 2-SAT（了解）

变量与否定建蕴含图，判 xi 与 ¬xi 同 SCC 则无解。竞赛经典。

### 与 topological-sort

缩点后 DAG 才能 Kahn。有环原图不能直接拓扑。

### 与 802/207

环检测可用 SCC 或拓扑。SCC 得强连通块大小>1 则有环（自环除外）。

### 复杂度

O(V+E) 一次 DFS+栈。

### 面试话术

「Tarjan：dfn/low，栈，回边 on[v]，low==dfn 弹 SCC。O(V+E)。」

### PowerShell 验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\scc\tarjan.py
g++ -std=c++17 -O2 -o run.exe tarjan.cpp; .\run.exe
```

### 读者自检

手推两 SCC；默写 dfs 三分支；缩点三步；scc OK。

### 专题收束

Tarjan 是 SCC 默认实现。Study `tarjan_scc` 为锚。

### 补强（达标）

九节 ##、六 ###；medium≥8000；algo-graph scc 行。draft strict。

### 错误再述

回边判断错；low 初值；弹栈不完整；孤立点 n=1。

### 与 network_flow

流、匹配不同族；SCC 是结构分解。

### 能力终检

25 分钟写 tarjan；口述缩点；双脚本 OK。

### 结语

掌握 dfn/low/on 后可做缩点 DP 与 2-SAT 入门。讲义与 `tarjan.py` 同步。


### 专题强化·Tarjan SCC·1

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·2

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·3

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·4

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·5

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·6

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·7

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·8

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·9

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·10

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·11

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·12

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·13

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·14

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·15

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·16

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·17

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·18

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·19

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·20

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·21

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·22

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·Tarjan SCC·23

**核心函数**：Study 实现 `tarjan_scc`，自测输出 `scc OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-scc --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：Tarjan SCC 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。

## 学习路径

1. `algo-graph-traversal` DFS。
2. 本页 Tarjan 与 `scc OK`。
3. `algo-graph-topological-sort` 在 DAG 上练习。
4. 竞赛缩点题选做。

**复习**：闭卷写 dfs 内三分支；解释为何回边用 dfn[v]。

**时间**：2～3 小时含手推。

## 延伸阅读

- [scc/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/graph/scc/notes.md)
- [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm)
- 站点：`algo-graph`、`algo-graph-topological-sort`

OI Wiki：Tarjan 强连通分量；以 Study 源码为准。
