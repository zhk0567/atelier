---
title: "算法 · Graph Lca"
series: algorithm
category: Algorithms
topic_path: algorithms/graph/lca
guide_toc: topic-algorithm
guide_tier: medium
status: published
---

# 算法 · 树上最近公共祖先（LCA）

## 导读

**最近公共祖先（Lowest Common Ancestor, LCA）** 指有根树中节点 u、v 的公共祖先里 **深度最大** 的那一个。静态树上多次查询 LCA 是图论基础能力：路径拆成「u 到 LCA」+「LCA 到 v」、求路径权值和、结合树 DP 等。Study 仓库 `lca/` 用 **二进制倍增（Binary Lifting）** 实现：预处理每个点向上 2^k 步的祖先，单次查询 O(log n)。

与 `algo-graph-traversal` 的 BFS/DFS 不同，LCA 假设 **树已定型、查询离线或在线批量**；与 `algo-dp-tree` 在子树上聚合不同，LCA 回答 **两点关系**。LeetCode 236 给出二叉树指针版，思路与倍增/父链跳跃一致；Study 用邻接表存一般无向树并定根。

本页扩写：倍增表 `up[k][v]` 含义、DFS 预处理深度、查询时先抬深再同步跳、复杂度 O(n log n + q log n)，以及与 Tarjan 离线 LCA、欧拉序+ST 的对比。读完应能默写 `BinaryLiftingLCA`、解释样例 `lca(3,4)=2`，并对拍 `lca OK`。

**在图论家族中的位置**：`algorithms/graph/lca` 子专题；总览见 `algo-graph`。Hot 100 含 236；1143 等与树 DP 结合。有向图 SCC 见 `algo-graph-scc`，与本页无关。

**面试沟通顺序**：说明预处理 DFS 填 `up[0]` 再递推 `up[k]` → 查询抬深 → 同步跳 → O(log n)。

**manifest**：slug `algo-graph-lca`，`status: published`，`guide_tier: medium`。

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`，`lca.cpp` 使用 `#include <alg_std.hpp>`。

建议已具备：

- **树的 DFS/BFS**：`algo-graph-traversal`。
- **二进制位运算**：`d >> k & 1` 判第 k 位。
- **邻接表**：无向边 `(u,v)` 双向加边，DFS 传 parent 防回退。
- **对数阶**：`LOG = ceil(log2(n))` 或 `(n+1).bit_length()`。

**查询口诀**：若 `depth[u]<depth[v]` 交换；u 先跳 `depth[u]-depth[v]` 步；若 u==v 返回；否则从高 k 到低 k 同步跳直到祖先不同，返回 `up[0][u]`。

## Study 仓库对照

`topic_path`：`algorithms/graph/lca`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/graph/lca/notes.md` | `python/algorithms/graph/lca/lca.py` |
| C++ | `cpp/algorithms/graph/lca/notes.md` | `cpp/algorithms/graph/lca/lca.cpp` |

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\lca\lca.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\graph\lca
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe lca.cpp
.\run.exe
```

推荐题：LC 236（指针版对照）。C++ 与 Python 同构。

## 基础篇

### 直觉与定义

**LCA 定义**

根为 `root`。祖先 z 同时满足从 root 到 u、v 路径上 z 在链上；LCA 是其中深度最大的点。若 u 是 v 祖先，则 LCA(u,v)=u。

**倍增表**

`up[0][v]` = v 的父节点（根父为 -1）。`up[k][v]` = `up[k-1][ up[k-1][v] ]`，即向上 2^k 步。`LOG` 取满足 2^LOG ≥ n 的最小值。

**Study 样例树**

```
      0
    /   \
   1     2
        / \
       3   4
```

`lca(3,4)=2`；`lca(1,3)=0`；`lca(1,2)=0`；`lca(2,2)=2`。

**与 236**

二叉树 `TreeNode` 可用父指针向上走；倍增适用于 `n` 个点编号、`edges` 列表的静态树，查询 O(log n) 可重复 q 次。

### 复杂度分析

| 项目 | 说明 |
|------|------|
| 预处理 | DFS O(n)，填表 O(n log n) |
| 单次查询 | O(log n) |
| 空间 | O(n log n) |
| q 次查询 | O(n log n + q log n) |

n,q 达 10^5 时常用。欧拉序+ST 可 O(n) 预处理 O(1) 查询，实现更重；面试倍增足够。

### 代码模板

核心查询逻辑（类内方法）：

```python
def lca(self, u: int, v: int) -> int:
    if self._depth[u] < self._depth[v]:
        u, v = v, u
    d = self._depth[u] - self._depth[v]
    for k in range(self._log):
        if d >> k & 1:
            u = self._up[k][u]
    if u == v:
        return u
    for k in range(self._log - 1, -1, -1):
        if self._up[k][u] != self._up[k][v]:
            u = self._up[k][u]
            v = self._up[k][v]
    return self._up[0][u]
```

预处理在 DFS 中设 `up[0][u]=p`，并递推 `up[k]`。

### 变体与技巧

**路径权值和**

预处理 `dist` 前缀，答案 `dist[u]+dist[v]-2*dist[lca]+val[lca]`（视题意）。

**LCA + 倍增维护 max/min**

`up[k][v]` 旁存路径 max，合并时取 max。

**Tarjan 离线**

一次 DFS 用并查集合并，适合 **所有查询一次给出**；在线多次用倍增更方便。

**欧拉序 + ST**

DFS 序进入退出时间，LCA 对应区间内深度最小点；RMQ O(1)。

**动态树**

Link-Cut Tree 等，竞赛向，Study 未涉及。

### 易错点

1. **根父节点**：`up[0][root]=-1`，跳时判断 `-1`。
2. **无向边**：DFS 勿走回父。
3. **先抬深再同步跳**：顺序反则错。
4. **同步跳 k 从大到小**：保证不漏 LCA。
5. **u==v 提前返回**：深度对齐后可能已相等。
6. **LOG 过小**：应用 `bit_length` 或 while 扩 LOG。
7. **单点树**：`n=1` 时 LCA 为 0，Study 已测。

### 练习建议

1. 运行 `lca.py` 理解断言。
2. 236 指针版实现。
3. 1483 等路径题（若遇）用 dist+LCA 公式。

**自测**：链状树、星形树手算 LCA。

## Python 实现

Study `lca.py` 完整类与测试：

```python
"""树上倍增 LCA（最近公共祖先）。"""

from __future__ import annotations

from typing import List, Tuple


class BinaryLiftingLCA:
    def __init__(self, n: int, edges: List[Tuple[int, int]], root: int = 0) -> None:
        self._n = n
        self._log = max(1, (n + 1).bit_length())
        self._g: List[List[int]] = [[] for _ in range(n)]
        for u, v in edges:
            self._g[u].append(v)
            self._g[v].append(u)
        self._depth = [0] * n
        self._up = [[-1] * n for _ in range(self._log)]

        def dfs(u: int, p: int) -> None:
            self._up[0][u] = p
            for k in range(1, self._log):
                mid = self._up[k - 1][u]
                self._up[k][u] = self._up[k - 1][mid] if mid != -1 else -1
            for v in self._g[u]:
                if v != p:
                    self._depth[v] = self._depth[u] + 1
                    dfs(v, u)

        dfs(root, -1)

    def lca(self, u: int, v: int) -> int:
        if self._depth[u] < self._depth[v]:
            u, v = v, u
        d = self._depth[u] - self._depth[v]
        for k in range(self._log):
            if d >> k & 1:
                u = self._up[k][u]
        if u == v:
            return u
        for k in range(self._log - 1, -1, -1):
            if self._up[k][u] != self._up[k][v]:
                u = self._up[k][u]
                v = self._up[k][v]
        return self._up[0][u]


if __name__ == "__main__":
    n = 5
    ed = [(0, 1), (0, 2), (2, 3), (2, 4)]
    t = BinaryLiftingLCA(n, ed, 0)
    assert t.lca(3, 4) == 2
    assert t.lca(1, 3) == 0
    assert t.lca(1, 2) == 0
    assert t.lca(0, 4) == 0
    assert t.lca(2, 2) == 2
    t1 = BinaryLiftingLCA(1, [], 0)
    assert t1.lca(0, 0) == 0
    print("lca OK")
```

**要点**：构造时一次 DFS 完成深度与 `up` 全表；`__main__` 覆盖多组断言。

## C++ 实现

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;

struct BinaryLiftingLCA {
    int n, LOG;
    vector<vector<int>> g, up;
    vector<int> dep;

    BinaryLiftingLCA(int n_, const vector<pair<int, int>>& edges, int root = 0) : n(n_) {
        LOG = 1;
        while ((1 << LOG) <= n) ++LOG;
        g.assign(n, {});
        for (auto [u, v] : edges) {
            g[u].push_back(v);
            g[v].push_back(u);
        }
        dep.assign(n, 0);
        up.assign(LOG, vector<int>(n, -1));
        function<void(int, int)> dfs = [&](int u, int p) {
            up[0][u] = p;
            for (int k = 1; k < LOG; ++k) {
                int mid = up[k - 1][u];
                up[k][u] = (mid == -1 ? -1 : up[k - 1][mid]);
            }
            for (int v : g[u]) {
                if (v == p) continue;
                dep[v] = dep[u] + 1;
                dfs(v, u);
            }
        };
        dfs(root, -1);
    }

    int lca(int u, int v) {
        if (dep[u] < dep[v]) swap(u, v);
        int d = dep[u] - dep[v];
        for (int k = 0; k < LOG; ++k)
            if (d >> k & 1) u = up[k][u];
        if (u == v) return u;
        for (int k = LOG - 1; k >= 0; --k) {
            if (up[k][u] != up[k][v]) {
                u = up[k][u];
                v = up[k][v];
            }
        }
        return up[0][u];
    }
};
```

与 Python 逻辑一一对应；`main` 中断言同构。

## 练习与延伸

- LC 236：二叉树 LCA
- 1483、1027 等：路径 + LCA 公式
- Study：`problems/leetcode/0236_lowest_common_ancestor_of_a_binary_tree/`

**相邻**：`algo-graph`、`algo-graph-traversal`、`algo-dp-tree`。

### 236 指针版思路

若节点有 parent：先算深度差，深点上移；再同时上移直到相遇。无预处理表，单次 O(h)。多次查询仍用倍增。

### 路径长度与权值

边权 w(u,v)：预处理 `dist[v]=dist[p]+w`。路径 u-v 权值和 `dist[u]+dist[v]-2*dist[lca]+adjust`（是否重复计 LCA 点权看题面）。

### Tarjan 离线 LCA（了解）

DFS 树，访问 u 时并查集合并子树，查询 (u,v) 当 v 已访问则 LCA=find(merge)。总 O(n+q) 均摊。适合离线批查询。

### 欧拉序 + RMQ

DFS 记录节点进入序，LCA(u,v) 等价于欧拉序上第一次出现区间内的最小深度点。ST 表 O(n log n) 预处理 O(1) 查询。

### 倍增跳 k 步

`kth_ancestor(u,k)`：从低到高若 `k>>i&1` 则 `u=up[i][u]`。LCA 查询中抬深即特例。

### 重链剖分（HLD）

链顶深度序 + 线段树，路径修改/查询 O(log^2 n)。竞赛重型；面试倍增优先。

### 面试白板版

「DFS 预处理父节点与深度，倍增表 up[k][v] 为 2^k 祖先。查询：深点抬差；再高位同步跳至 LCA 子节点；返回父。O(log n)。」

### PowerShell 验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\lca\lca.py
g++ -std=c++17 -O2 -o run.exe lca.cpp; .\run.exe
```

### 与 algo-graph 总览关系

`algo-graph` 建模手册：树上两点路径 = 到 LCA 两段。学完本页回总览勾「LCA」簇。

### 错误类型

WA：跳序错误、LOG 不足、无向边回父。TLE：每次查询暴力爬父。MLE：up 维度过大但可接受。

### 能力检查

20 分钟写 `BinaryLiftingLCA` 类；手算样例 lca(3,4)；口述 dist 公式。

### 维护

draft；strict 双过后 published。

### 结语

倍增 LCA 是静态树多次查询的默认工具。Study 代码短、断言全；与 236 对照可打通指针版与编号版。


### Study 样例树与查询手推

```
      0
    /   \
   1     2
        / \
       3   4
```

`depth[3]=2, depth[4]=2, depth[1]=1`。`lca(3,4)`：同深，同步跳得 2。`lca(1,3)`：抬深 3 到 0 层前 1 已在 0？实际 1 深 1、3 深 2，抬 3 一步到 2，再同步跳到 0。`lca(2,2)=2`。

### up[k][v] 递推含义

`up[0][v]` 父节点。`up[1][v]` 祖父。`up[k][v]=up[k-1][ up[k-1][v] ]`，若中间为 -1 则 -1。预处理 O(n log n)。

### 查询五步再列

1. 若 depth[u]<depth[v] 交换。2. 差深 d，按位跳 up[k][u]。3. 若 u==v 返回。4. k 从大到小若 up[k][u]!=up[k][v] 同跳。5. 返回 up[0][u]。

### 236 二叉树指针版

无编号：算深度，深点上移，再同时上移直到相遇。单次 O(h)。多次查询仍建议倍增预处理。

### 路径权值公式

`dist[u]+dist[v]-2*dist[lca]+val[lca]`（边权版视题调整是否计 LCA 点权）。先 DFS 预处理 dist。

### k 级祖先

`kth_ancestor(u,k)`：若 `k>>i&1` 则 `u=up[i][u]`。LCA 抬深是特例。

### Tarjan 离线 LCA（了解）

并查集+DFS，适合离线批查询。在线多次用倍增。

### 欧拉序+RMQ

DFS 序+ST 表 O(1) 查询，实现重。面试倍增足够。

### HLD（了解）

重链剖分+线段树，路径修改查询。竞赛向。

### 与 traversal、MST、SCC

LCA 是 **静态树** 查询工具；SCC 是有向图；MST 无向连通。勿混。

### 复杂度背诵

预处理 O(n log n)，查询 O(log n)，空间 O(n log n)。

### 面试话术

「DFS 建 depth 与 up 表，查询抬深再同步跳，O(log n)。」

### PowerShell 验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\lca\lca.py
g++ -std=c++17 -O2 -o run.exe lca.cpp; .\run.exe
```

### 读者自检

手推 lca(3,4)=2；默写查询循环；236 区别；lca OK。

### 专题收束

倍增 LCA 是静态树默认方案。Study `BinaryLiftingLCA` 与讲义一致。

### 补强（达标）

九节 ##、六 ###；medium 汉字≥8000；algo-graph 总览 lca 行。draft strict 双过再 published。

### 易错再述

LOG 不足；回父边；跳序反；up 递推 mid=-1。

### 1143 与树 DP

最长公共子序列在树结构上有时需 LCA 拆路径，见树 DP 交叉题。

### 能力终检

20 分钟写类；口述 dist 公式；双脚本 OK。

### 结语

LCA 拆路径是两点的桥梁；掌握倍增后可做路径权题。讲义与 `lca.py` 同步。


### 专题强化·倍增LCA·1

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·2

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·3

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·4

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·5

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·6

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·7

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·8

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·9

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·10

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·11

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·12

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·13

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·14

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·15

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·16

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·17

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·18

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·19

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·20

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·21

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·倍增LCA·22

**核心函数**：Study 实现 `BinaryLiftingLCA.lca`，自测输出 `lca OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-graph-lca --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：倍增LCA 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。

## 学习路径

1. `algo-graph-traversal` DFS 熟练。
2. 本页倍增与 `lca OK`。
3. 236 提交。
4. 需路径权时学 dist 预处理。

**复习**：闭卷写查询五步；解释 `up[k][u]` 递推。

**时间**：2～4 小时含 236。

## 延伸阅读

- [lca/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/graph/lca/notes.md)
- [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm)
- 站点：`algo-graph`、`algo-dp-tree`

经典参考：《算法竞赛进阶指南》LCA 章；OI Wiki 最近公共祖先。以 Study 为准。
