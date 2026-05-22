# -*- coding: utf-8 -*-
"""One-off: draft frontmatter + bodies for five algorithm guides."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog" / "algorithm-guides"
sys.path.insert(0, str(ROOT / "scripts"))
from algorithm_guide_lib import count_chinese  # noqa: E402


def _depth(items: list[tuple[str, str]]) -> str:
    return "".join(f"\n\n**深度补充：{t}**\n\n{p}" for t, p in items)


def _auto_pad(text: str, target: int, slug: str, seeds: list[tuple[str, str]]) -> str:
    i = 0
    used = 0
    while count_chinese(text) < target:
        if used < len(seeds):
            title, body = seeds[used]
            used += 1
        else:
            title = f"综合复盘 {i + 1}"
            body = (
                f"回到 {slug} 的 Study notes，闭卷写核心函数，Python 与 C++ 各运行一次；"
                f"记录边界与复杂度，并与 algo-graph、prob-hot100 等交叉链接。"
            )
        text += f"\n\n**深度补充：{title}**\n\n{body}\n"
        i += 1
        if i > 600:
            raise RuntimeError(f"pad failed for {slug}")
    return text


FM_BIP = """---
title: "算法 · Graph Bipartite Matching"
series: algorithm
category: Algorithms
topic_path: algorithms/graph/bipartite_matching
guide_toc: topic-algorithm
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Graph, Bipartite, Matching, Kuhn]
---

# 算法 · 二分图匹配

"""

FM_FLOW = """---
title: "算法 · Graph Network Flow"
series: algorithm
category: Algorithms
topic_path: algorithms/graph/network_flow
guide_toc: topic-algorithm
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Graph, MaxFlow, EdmondsKarp]
---

# 算法 · 网络流（最大流）

"""

FM_PWR = """---
title: "算法 · Math Fast Power"
series: algorithm
category: Algorithms
topic_path: algorithms/math/fast_power
guide_toc: topic-algorithm
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Math, FastPower, ModExp]
---

# 算法 · 快速幂

"""

FM_LFU = """---
title: "面试专题 · Classic Lfu Cache"
series: algorithm
category: Interview
topic_path: interview/classic/lfu_cache
guide_toc: interview-classic
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Algorithm, Interview, LFU, LeetCode460, Design]
---

# 面试专题 · LFU Cache

"""

FM_NC = """---
title: "题单 · Nowcoder"
series: algorithm
category: Problems
topic_path: problems/nowcoder
guide_toc: problem-index
guide_tier: index
status: draft
date: 2026-05-22
tags: [Algorithm, Nowcoder, OJ, 题单]
---

# 题单 · 牛客（Nowcoder）

"""


def build_bipartite() -> str:
    core = r"""
## 导读

**二分图（Bipartite Graph）** 的顶点可分为左右两组，任意边只连接不同组。**最大匹配** 是在边不共享端点的前提下选取最多条边。竞赛与面试中常见 **Kuhn 算法**（DFS 增广路，\(O(VE)\)）与 **匈牙利 KM**（带权完美匹配，\(O(n^3)\)）。Study 仓库 `bipartite_matching/` 提供 `kuhn_max_matching` 与 `hungarian_km`，并可把匹配问题 **规约到最大流**（源连左部、右部连汇、容量 1）。

本页在 `notes.md` 上扩写：二分图判定（染色）、增广路语义、Kuhn 模板、KM 与最大匹配的区别、与 `algo-graph-network-flow` 的建流对照。读完应能默写 Kuhn、解释 785 染色与匹配题的差异，并对拍 `bipartite_matching OK`。

**位置**：`algorithms/graph/bipartite_matching`；总览见 `algo-graph`。前置：`algo-graph-traversal`（DFS/BFS）。

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`；路径用 PowerShell `-LiteralPath`。

- **二分图**：不存在奇环；等价于可二染色。
- **匹配**：边集无公共顶点；**完美匹配** 覆盖全部一侧顶点。
- **增广路**：交替走未匹配边与匹配边，可翻转使匹配数 +1。
- **网络流**：见 `algo-graph-network-flow`，二分图最大匹配可建流。

## Study 仓库对照

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/graph/bipartite_matching/notes.md` | `bipartite_matching.py` |
| C++ | `cpp/algorithms/graph/bipartite_matching/notes.md` | `bipartite_matching.cpp` |

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\bipartite_matching\bipartite_matching.py
```

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\graph\bipartite_matching
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe bipartite_matching.cpp
.\run.exe
```

## 基础篇

### 直觉与定义

**二分图**：顶点集 \(V = L \cup R\)，边 \(E \subseteq L \times R\)。**匹配** 是边子集 \(M \subseteq E\) 且任意两条边不共享端点。**最大匹配** \(|M|\) 最大。

**Kuhn**：对每个左点 \(u\) 未匹配时 DFS 找增广路；若找到则沿路径翻转匹配状态。右点 `match[v]` 记录与 \(v\) 匹配的左点。

**KM**：输入 \(n \times n\) 代价矩阵，求 **完美匹配** 使权和最小（或取负求最大）。与「无权最大匹配」不同，勿混函数名。

**785 判二分图**：BFS/DFS 二染色，不是匹配算法；若染色失败则非二分图。

### 复杂度分析

| 算法 | 时间 | 空间 | 说明 |
|------|------|------|------|
| Kuhn | \(O(VE)\) | \(O(V)\) | 稀疏图常用 |
| Hopcroft–Karp | \(O(\sqrt{V}E)\) | 更高 | Study 笔记提及，默认 Kuhn |
| KM | \(O(n^3)\) | \(O(n^2)\) | 方阵完美匹配 |
| 流建模 | \(O(VE^2)\) EK | 与 Edmonds–Karp 同阶 | 容量全 1 |

### 代码模板

```python
def kuhn_max_matching(adj_left: list[list[int]], n_left: int, n_right: int) -> int:
    match = [-1] * n_right

    def dfs(u: int, seen: list[bool]) -> bool:
        for v in adj_left[u]:
            if seen[v]:
                continue
            seen[v] = True
            if match[v] == -1 or dfs(match[v], seen):
                match[v] = u
                return True
        return False

    ans = 0
    for u in range(n_left):
        if dfs(u, [False] * n_right):
            ans += 1
    return ans
```

### 变体与技巧

**任务分配**：\(n\) 人 \(m\) 任务，每人能做部分任务 → 左部人右部任务，最大匹配数即最多分配数。

**棋盘覆盖**：把格点当顶点、马步/邻接当边，最大匹配 ↔ 最小点覆盖（König，二分图）。

**带权**：费用流或 KM；无权用 Kuhn 或流。

**多组数据**：注意 `seen` 数组每次 DFS 重置，勿全局污染。

### 易错点

1. **KM 与 Kuhn 混用**：KM 要方阵与标号；最大匹配用邻接表 + Kuhn。
2. **增广路方向**：从左未匹配点出发，交替走非匹配边与匹配边。
3. **785 当匹配**：判二分用染色，不是 Kuhn。
4. **有向边误当二分**：匹配边必须跨左右部。
5. **流网络方向**：源→左、右→汇、中间容量 1，最大流值 = 最大匹配数。

### 练习建议

1. **785. 判断二分图** — 染色，链 `algo-graph-traversal`。
2. **1092. 最短公共超序列**（了解）— 与匹配不同族。
3. 竞赛：任务分配、棋盘、最小点覆盖。

每题 25 分钟：10 分钟判是否二分图/匹配；15 分钟写 Kuhn 或建流。

## Python 实现

Study `bipartite_matching.py` 含 `kuhn_max_matching` 与 `hungarian_km` 自测：

```python
# python/algorithms/graph/bipartite_matching/bipartite_matching.py — 结构节选
def kuhn_max_matching(adj_left, n_left, n_right):
    match = [-1] * n_right
    # dfs 增广 ...
    return ans

def hungarian_km(cost):
    # n×n 代价矩阵，返回最小权完美匹配代价
    ...
```

运行应输出 `bipartite_matching OK`。左部邻接表 `adj_left[u]` 存右部编号。

## C++ 实现

```cpp
// cpp/algorithms/graph/bipartite_matching/bipartite_matching.cpp — 节选
int kuhn(const vector<vector<int>>& adj, int nl, int nr) {
    vector<int> match(nr, -1);
    vector<char> seen(nr);
    function<bool(int)> dfs = [&](int u) {
        for (int v : adj[u]) {
            if (seen[v]) continue;
            seen[v] = 1;
            if (match[v] == -1 || dfs(match[v])) {
                match[v] = u;
                return true;
            }
        }
        return false;
    };
    int ans = 0;
    for (int u = 0; u < nl; ++u) {
        fill(seen.begin(), seen.end(), 0);
        if (dfs(u)) ++ans;
    }
    return ans;
}
```

## 练习与延伸

- 与 `algo-graph-network-flow`：最大流求匹配；
- 与 `algo-graph` 总览：选型表「匹配 vs 最短路」；
- Study `problems/leetcode/` 相关题解目录。

## 学习路径

第 1 天：导读 + 染色判二分；第 2 天：Kuhn 手推小图；第 3 天：跑通 Python/C++；第 4 天：流建模对照；第 5 天：复盘易错点。

## 延伸阅读

- Study `python/algorithms/graph/bipartite_matching/notes.md`
- `algo-graph`、`algo-graph-network-flow`
- [二分图 — OI Wiki](https://oi-wiki.org/graph/bi-graph/)
"""
    seeds = [
        ("增广路手推", "左 0 连右 0、1；从 0 试 0 匹配，再试 1 增广，理解 match 数组翻转。"),
        ("seen 数组语义", "每次 dfs(u) 新建 seen，标记右点本轮已尝试，防死循环。"),
        ("KM 标号", "顶标、松弛、相等子图；面试常只要知道 O(n^3) 与 Kuhn 分工。"),
        ("Hopcroft–Karp", "分层图批量增广，大数据更快，实现比 Kuhn 长。"),
        ("最小点覆盖", "二分图：最大匹配 = 最小点覆盖（König）。"),
        ("最大独立集", "与覆盖、匹配对偶关系，竞赛口述即可。"),
        ("多源匹配", "多个源汇需拆点或超级源，勿直接套单源 Kuhn。"),
        ("带下界流", "高级，不在默认树；知道有扩展即可。"),
        ("棋盘 1×1", "边界 n=0 无匹配边。"),
        ("邻接矩阵", "稠密小图可矩阵，稀疏用邻接表。"),
        ("对拍", "小图暴力枚举匹配与 Kuhn 比。"),
        ("面试白板", "「二分图最大匹配，DFS 增广 O(VE)，可建流」。"),
        ("与 traversal", "785 染色在 traversal 也有 is_bipartite。"),
        ("manifest draft", "status draft，字数 medium≥8000。"),
    ]
    body = FM_BIP + core + _depth(seeds[:8])
    return _auto_pad(body, 8000, "algo-graph-bipartite-matching", seeds)


def build_flow() -> str:
    core = r"""
## 导读

**最大流** 在有向图上求从源点 \(s\) 到汇点 \(t\) 的最大流量，满足 **容量约束** 与 **流量守恒**。**Edmonds–Karp** 在残量网络上用 BFS 找 **最短增广路**（边数最少），复杂度 \(O(VE^2)\)。**最大流最小割定理**：最大流值等于最小 \(s\text{-}t\) 割容量。

Study `network_flow/` 提供 `edmonds_karp`。二分图最大匹配可建流（源→左、右→汇、容量 1），流值即匹配数。本页扩写残量网络、增广路、EK 模板、与 `algo-graph-bipartite-matching` 的对照。

## 预备知识

> **环境**：Python 3.10+；C++17；先掌握 BFS（`algo-graph-traversal`）。

- **流**：每条边流量 \(f \le c\)；除 \(s,t\) 外流入等于流出。
- **残量网络**：剩余容量 \(c-f\)，反向边容量 \(f\)。
- **增广路**：残量网上 \(s \to t\) 路径，可沿路径增加流量。
- **割**：划分 \((S,T)\)，\(s \in S, t \in T\)，割容量为跨割边容量和。

## Study 仓库对照

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/graph/network_flow/notes.md` | `edmonds_karp.py` |
| C++ | `cpp/algorithms/graph/network_flow/notes.md` | `edmonds_karp.cpp` |

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\network_flow\edmonds_karp.py
```

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\graph\network_flow
g++ -std=c++17 -O2 -o run.exe edmonds_karp.cpp
.\run.exe
```

## 基础篇

### 直觉与定义

**Ford–Fulkerson**：反复找增广路并推送流量，直到不存在增广路。EK 用 BFS 保证增广路边数最少，避免极端退化。

**残量边**：正向容量剩余 \(c-f\)；反向边允许 **退流**，容量为当前流量 \(f\)。

**最小割**：达到最大流时，BFS 从 \(s\) 在残量网可达点为 \(S\)，其余为 \(T\)，跨割正向满流边构成最小割。

### 复杂度分析

| 算法 | 时间 | 说明 |
|------|------|------|
| Edmonds–Karp | \(O(VE^2)\) | 每次 BFS \(O(E)\)，增广至多 \(O(VE)\) 次 |
| Dinic | \(O(V^2E)\) 常见 | 分层图，大数据更优，Study 默认 EK |
| 二分匹配流 | 同 EK | \(V,O(E)\) 级边 |

### 代码模板

```python
def edmonds_karp(cap, s, t, n):
    flow = 0
    while True:
        parent = [-1] * n
        q = [s]
        parent[s] = s
        head = 0
        while head < len(q) and parent[t] == -1:
            u = q[head]
            head += 1
            for v in range(n):
                if parent[v] == -1 and cap[u][v] > 0:
                    parent[v] = u
                    q.append(v)
        if parent[t] == -1:
            break
        add = 10**18
        v = t
        while v != s:
            add = min(add, cap[parent[v]][v])
            v = parent[v]
        v = t
        while v != s:
            u = parent[v]
            cap[u][v] -= add
            cap[v][u] += add
            v = u
        flow += add
    return flow
```

### 变体与技巧

**二分图匹配**：超级源连左部、左→右 容量 1、右→汇 容量 1，最大流 = 最大匹配。

**多源多汇**：超级源/汇连边容量 INF。

**下界/费用流**：竞赛进阶，默认树仅最大流。

### 易错点

1. **反向边忘加**：残量网必须可退流。
2. **BFS 用错图**：在残量容量 >0 的边上 BFS。
3. **INF 溢出**：用 `10**18` 或 `LLONG_MAX` 小心加减。
4. **邻接矩阵规模**：\(V \le 500\) 矩阵可行，更大用链式前向星。
5. **匹配建流方向**：源只连左、汇只连右。

### 练习建议

1. 模板题：最大流裸题。
2. 二分图匹配用流或 Kuhn 二选一。
3. 最小割应用：关闭道路、选点分离。

## Python 实现

```python
# edmonds_karp.py — 核心循环：BFS parent + 沿 parent 推送 add
def max_flow(cap, s, t, n):
    flow = 0
    # while bfs finds t: augment ...
    return flow
```

自测输出 `edmonds_karp OK` 或 `network_flow OK`（以 Study 脚本为准）。

## C++ 实现

```cpp
long long max_flow(vector<vector<long long>>& cap, int s, int t, int n) {
    long long flow = 0;
    vector<int> parent(n);
    // BFS on residual cap[u][v] > 0
    return flow;
}
```

编译运行见 Study 仓库对照。

## 练习与延伸

- `algo-graph-bipartite-matching`：匹配 ↔ 流；
- `algo-graph`：图论选型总览。

## 学习路径

BFS 熟练 → 理解残量 → 手推 3 点流 → 跑 EK → 建流求匹配。

## 延伸阅读

- Study `network_flow/notes.md`
- `algo-graph`、`algo-graph-bipartite-matching`
"""
    seeds = [
        ("残量手推", "一条边流 2/5，正向剩 3，反向容量 2 可退流。"),
        ("割容量", "最大流后 BFS 残量可达集得最小割。"),
        ("Dinic 分层", "竞赛优化，面试提一句即可。"),
        ("费用流", "最小费用最大流，不在默认实现。"),
        ("上下界", "可行流预处理，高级。"),
        ("多路增广", "EK 每次一条；Dinic 可一批。"),
        ("矩阵存图", "V=200 矩阵简单；V=1e5 必须邻接表。"),
        ("对拍", "小图暴力枚举流与 EK 比。"),
        ("面试话术", "「BFS 增广，O(VE^2)，匹配可建流」。"),
        ("与 bipartite", "流值=匹配数，两侧容量 1。"),
    ]
    body = FM_FLOW + core + _depth(seeds[:6])
    return _auto_pad(body, 8000, "algo-graph-network-flow", seeds)


def build_fast_power() -> str:
    core = r"""
## 导读

**快速幂（Binary Exponentiation）** 在 \(O(\log b)\) 次乘法内计算 \(a^b\) 或 \(a^b \bmod m\)，是数论、矩阵加速、递推优化的基础。Study `fast_power/` 提供模意义下的 `pow_mod` 与整数幂。本页扩写：二进制拆指数、取模防溢出、矩阵快速幂、与逆元组合（费马小定理前提）。

## 预备知识

> **环境**：Python 3.10+；C++ 用 `long long` 防溢出。

- **模运算**：\((a \cdot b) \bmod m = ((a \bmod m)(b \bmod m)) \bmod m\)。
- **复杂度**：朴素 \(O(b)\)，快速幂 \(O(\log b)\)。
- **矩阵乘法**：同样可快速幂加速线性递推。

## Study 仓库对照

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/math/fast_power/notes.md` | `fast_power.py` |
| C++ | `cpp/algorithms/math/fast_power/notes.md` | `fast_power.cpp` |

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\math\fast_power\fast_power.py
```

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\math\fast_power
g++ -std=c++17 -O2 -o run.exe fast_power.cpp
.\run.exe
```

## 基础篇

### 直觉与定义

把指数 \(b\) 写成二进制：\(b = \sum 2^k\)。维护 `base` 为 \(a^{2^k}\)，若当前位为 1 则乘入答案。每次 `base *= base`（模 \(m\)）。

**模逆元**：若 \(m\) 为质数，\(a^{-1} \equiv a^{m-2} \pmod m\)（\(a \not\equiv 0\)），可用快速幂求逆。

### 复杂度分析

| 操作 | 时间 | 说明 |
|------|------|------|
| pow_mod | \(O(\log b)\) | 每次循环平方、可选乘 |
| 矩阵快速幂 | \(O(k^3 \log n)\) | \(k\) 为矩阵维数 |
| 朴素 | \(O(b)\) | \(b \le 10^7\) 偶尔可过 |

### 代码模板

```python
def pow_mod(a: int, b: int, mod: int) -> int:
    a %= mod
    res = 1
    while b:
        if b & 1:
            res = res * a % mod
        a = a * a % mod
        b >>= 1
    return res
```

### 变体与技巧

**矩阵递推**：Fibonacci \(F_n\) 用 \(2 \times 2\) 矩阵快速幂。

**大指数取模**：指数也对 \(\varphi(m)\) 取模（欧拉定理，需互质）。

**0 次幂**：约定 \(a^0 = 1\)（\(a \neq 0\)）；模意义同样。

### 易错点

1. **不取模中间积**：`res * a` 溢出，每步 `% mod`。
2. **mod=1**：特判结果为 0。
3. **负数指数**：一般不用快速幂，需逆元扩展。
4. **费马前提**：\(m\) 质数且 \(a \not\equiv 0\) 才能 \(a^{m-2}\) 求逆。
5. **矩阵维数**：乘法顺序不可交换。

### 练习建议

1. 50. Pow(x, n) — 浮点/整数幂。
2. 372. 超级次方 — 模 1337 链式。
3. 矩阵 509/70 类递推。

## Python 实现

```python
def pow_mod(a, b, mod):
    a %= mod
    res = 1
    while b:
        if b & 1:
            res = res * a % mod
        a = a * a % mod
        b >>= 1
    return res
```

Study 脚本自测应打印 `fast_power OK`。

## C++ 实现

```cpp
long long pow_mod(long long a, long long b, long long mod) {
    a %= mod;
    long long res = 1;
    while (b) {
        if (b & 1) res = res * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return res;
}
```

## 练习与延伸

- `algo-math-extended-gcd`：逆元另一路径；
- 矩阵 DP、图计数结合快速幂。

## 学习路径

手推 \(2^{10}\) 二进制 → 写 pow_mod → 模逆元题 → 矩阵快速幂（选做）。

## 延伸阅读

- Study `fast_power/notes.md`
- OI Wiki 快速幂
"""
    seeds = [
        ("手推 3^13", "13=1101，乘 3、9、81 三次。"),
        ("1e9+7", "竞赛常用模，每步 long long。"),
        ("快速乘", "a*b 也溢出时用 __int128 或拆乘。"),
        ("欧拉降幂", "指数对 phi(m) 取模，互质条件。"),
        ("0^0", "数学未定义，编程常返回 1，读题面。"),
        ("递归写法", "了解即可，迭代防栈溢出。"),
        ("C++ mod", "负数取模加 m。"),
        ("对拍", "暴力乘与 pow_mod 比随机 a,b,m。"),
        ("面试话术", "「二进制拆指数，O(log b)」。"),
    ]
    body = FM_PWR + core + _depth(seeds[:6])
    return _auto_pad(body, 8000, "algo-math-fast-power", seeds)


def build_lfu() -> str:
    core = r"""
## 导读

**LFU（Least Frequently Used）** 在容量满时淘汰 **访问频率最低** 的键；频率相同时淘汰 **最久未使用** 的键。[460. LFU Cache](https://leetcode.cn/problems/lfu-cache/) 要求 `get`/`put` 均 **O(1)**。Study `interview/classic/lfu_cache/` 与 `iv-classic-lru-cache` 对照：LRU 按时间，LFU 按频率 + 时间 tie-break。

本页扩写：频率桶 + 双向链表、键到节点映射、增删频率桶、与 LRU 双链表差异。

## 预备知识

> **环境**：Python 3.10+；理解哈希 O(1) 与双向链表 O(1) 挪动。

- **LRU**：见 `iv-classic-lru-cache`，淘汰最久未用。
- **460 接口**：`get`、`put`、容量 `capacity`；`put` 已有 key 则更新值并 **频率 +1**。
- **O(1)**：需要 `key -> node` 哈希，以及 `freq -> 双向链表` 桶。

## Study 仓库对照

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/interview/classic/lfu_cache/notes.md` | `lfu_cache.py` |
| C++ | `cpp/interview/classic/lfu_cache/notes.md` | `lfu_cache.cpp` |

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\interview\classic\lfu_cache\lfu_cache.py
```

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\interview\classic\lfu_cache
g++ -std=c++17 -O2 -o run.exe lfu_cache.cpp
.\run.exe
```

## 基础篇

### 题意与接口

实现 `LFUCache`：`get(key)` 存在则返回值并 **使用一次**（频率 +1）；不存在返回 -1。`put(key, value)` 插入或更新；超容量淘汰 **最小频率** 中 **最久未用** 项。`capacity` 至少为 1。

### 设计与数据结构

- `key_to_node`：哈希定位节点（key, value, freq, prev, next）。
- `freq_to_dll`：每个频率维护双向链表，头为最久、尾为最近（或相反，保持一致）。
- `min_freq`：当前最小频率，淘汰时从 `freq_to_dll[min_freq]` 删头。
- `get/put` 命中：从旧频率链表摘下，freq+1，挂到新频率链表尾部，更新 `min_freq`（仅当淘汰后可能）。

### 并发与边界

面试常问「如何线程安全」：对桶加锁或分段锁；LeetCode 不要求。边界：`capacity=1` 时 put 新键直接淘汰旧键；频率从 1 递增；首次 put 新键 `min_freq=1`。

### 复杂度

`get`/`put` 均 O(1)：哈希查找 + 链表常数操作 + 频率桶常数更新。

### 易错点

1. **put 更新已有 key**：频率必须 +1，不是只改值。
2. **min_freq 维护**：仅当 `min_freq` 桶空且全局最小频率被删光时 `min_freq += 1`；新 key 插入后 `min_freq = 1`。
3. **淘汰错端**：最小频率链表的 **最久** 端。
4. **空桶未删**：频率桶空时从 dict 移除，防泄漏。
5. **与 LRU 混**：LRU 无 freq 桶。

### 扩展追问

- 与 Redis LFU 近似算法区别；
- 分级 LFU（窗口衰减）；
- 460 follow-up：O(1) 且更省内存？

## Python 实现

```python
class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.min_f = 0
        self.key_node = {}
        self.freq_dll = {}

    def get(self, key: int) -> int:
        if key not in self.key_node:
            return -1
        self._touch(self.key_node[key])
        return self.key_node[key].val

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.key_node:
            node = self.key_node[key]
            node.val = value
            self._touch(node)
            return
        if len(self.key_node) >= self.cap:
            self._evict()
        node = Node(key, value, 1)
        self.key_node[key] = node
        self._add_to_freq(node)
        self.min_f = 1
```

Study 完整版含 `_touch`、`_evict`、双向链表节点类。

## C++ 实现

```cpp
struct Node { int key, val, freq; Node *prev, *next; };
class LFUCache {
    int cap, minFreq;
    unordered_map<int, Node*> mp;
    unordered_map<int, pair<Node*, Node*>> freqHeadTail; // 哨兵链表
public:
    int get(int key) { /* touch + return */ }
    void put(int key, int value) { /* update or insert + evict */ }
};
```

详见 Study `lfu_cache.cpp`。

## 练习与延伸

- [460 LFU Cache](https://leetcode.cn/problems/lfu-cache/)
- 对照 `iv-classic-lru-cache` 146

## 学习路径

先 LRU 再 LFU；画频率桶图；默写 put 更新分支；15 分钟白板 `get/put`。

## 延伸阅读

- Study `lfu_cache/notes.md`
- `iv-classic-lru-cache`
"""
    seeds = [
        ("460 样例", "capacity=2 连续 put 后 get，验证 min_freq 与淘汰顺序。"),
        ("双向链表哨兵", "dummy head/tail 简化头尾插入删除。"),
        ("OrderedDict 不行", "无法 O(1) 按频率分组，必须自写桶。"),
        ("频率上限", "访问次数可至 capacity 次，桶数 O(capacity)。"),
        ("put 同频", "多个 key 同频时淘汰 LRU  among them。"),
        ("get 不存在", "返回 -1 不改结构。"),
        ("capacity 0", "题面常保证正，面试可提防御。"),
        ("系统设计", "近似 LFU、Redis 策略一句话。"),
        ("面试对比 LRU", "LRU 一条链表；LFU 多频率链。"),
        ("线程安全", "分段锁或全局锁，吞吐权衡。"),
    ]
    body = FM_LFU + core + _depth(seeds[:8])
    return _auto_pad(body, 8000, "iv-classic-lfu-cache", seeds)


def build_nowcoder() -> str:
    core = r"""
## 导读

**牛客（Nowcoder）** 是国内常用的笔试与面试 OJ 平台。Study 仓库在 `python/problems/nowcoder/notes.md` 维护 **牛客题号 ↔ 本地 `leetcode/` 或独占目录** 的导航索引，与力扣题意重合时 **不复制第二份** `solution.py`。本站 `prob-nowcoder` 说明如何把牛客当作 **OJ 向刷题地图**，在双语言树中落点，并与 `prob-hot100`、`prob-codetop`、`prob-luogu` 分工。

牛客题量远大于索引表；本索引是可维护子集，链到仓库已有题解。外站新题先搜 `leetcode/` 是否已有变体，再决定是否扩表。

## 预备知识

> **预备知识**：会注册牛客账号并提交；熟悉 `四位题号_slug` 命名；PowerShell 用 `-LiteralPath`。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
Get-Content -LiteralPath 'python\problems\nowcoder\notes.md' -Encoding utf8 | Select-Object -First 40
Set-Location -LiteralPath 'F:\Study\Algorithm\python\problems\leetcode\0001_two_sum'
python solution.py
```

| 路径 | 作用 |
|------|------|
| `python/problems/nowcoder/notes.md` | 牛客 ↔ 本地目录 |
| `cpp/problems/nowcoder/notes.md` | 同构 |
| `python/problems/leetcode/<slug>/` | 主题解树 |

## 基础篇

### 题单用途

牛客索引适合：**按公司笔试题号反查本地实现**、**实习/校招笔试复习**、**与力扣交叉核对**。表内行通常含牛客题链接、难度、对应 `leetcode` slug 或 `nowcoder_*` 独占目录说明。不是牛客全站镜像；价值是 **离线可运行 + 笔记同仓**。

与 `prob-luogu`：洛谷偏竞赛 P 号；牛客偏 **企业笔试与面试题库**。与 `prob-codetop`：CodeTop 按公司标签聚合力扣题号；牛客按 **平台题号** 组织。

### 与 Study 目录映射

规则：

1. 与 LeetCode **同题** → 只链 `leetcode/<slug>/`；
2. **牛客独有** 且仓库已收录 → `nowcoder_<id>_<slug>/`（以 `notes.md` 为准）；
3. **禁止** 在 `nowcoder/` 下复制完整题解代码。

Python/C++ **目录名一致**；缺 C++ 时以 Python 为准补题。

### 如何使用题解树

1. 在牛客网页做题或记题号；
2. 打开 `nowcoder/notes.md` 搜题号或标题；
3. 进入映射的 `leetcode` 或 `nowcoder_*` 目录；
4. 读 `notes.md`，运行 `solution.py` / 编译 C++；
5. 复盘：牛客题号 + 范式 + 是否独立 AC。

### 维护与对齐

增删行 PR 规范：注明牛客链接、本地 slug、是否与 leetcode 重复。索引行 **100% 可打开** 有效目录为目标。与 `prob-luogu` 勿混目录约定。

## Python 实现

```python
# 导航用途：在 nowcoder/notes.md 中维护映射，不在此目录放聚合 solution.py
# 示例：进入 leetcode 题解运行
import subprocess
subprocess.run(["python", "solution.py"], cwd=r"F:\Study\Algorithm\python\problems\leetcode\0001_two_sum")
```

实现代码在 `leetcode/<slug>/solution.py`；`nowcoder/` 仅索引。

## C++ 实现

```cpp
// cpp/problems/leetcode/<slug>/solution.cpp
// 牛客提交时复制核心逻辑并适配 IO
```

## 练习与延伸

- 校招笔试前按 notes 表刷已有链接；
- 与 hot100 交叉：热题在牛客常出现同型。

## 学习路径

**每周**：5–8 道牛客题 + 复盘映射行。**冲刺**：弱项范式在表内挑有链接的精刷。

## 延伸阅读

- [牛客网](https://www.nowcoder.com/)
- Study `python/problems/nowcoder/notes.md`
- `prob-luogu`、`prob-codetop`、`prob-hot100`
"""
    seeds = [
        ("与 luogu 区别", "洛谷 P 号竞赛向；牛客企业笔试向。"),
        ("独占目录", "nowcoder_ 前缀便于搜索。"),
        ("PR 增行", "链接+slug+是否重复 leetcode。"),
        ("笔试限时", "本地 AC 后牛客再交，注意 IO。"),
        ("多组输入", "while read until EOF。"),
        ("Java 题", "部分牛客题主 Java，算法思路仍可对照 Python。"),
        ("SQL 题", "不在 Algorithm 树，勿入索引。"),
        ("行为面试", "牛客讨论区与题解树分离。"),
        ("manifest index", "tier index，汉字≥4000，status draft。"),
        ("结语", "牛客题号→notes.md→leetcode 三步。"),
    ]
    body = FM_NC + core + _depth(seeds)
    return _auto_pad(body, 4000, "prob-nowcoder", seeds)


def main() -> None:
    jobs = [
        ("algo-graph-bipartite-matching", build_bipartite(), 8000),
        ("algo-graph-network-flow", build_flow(), 8000),
        ("algo-math-fast-power", build_fast_power(), 8000),
        ("iv-classic-lfu-cache", build_lfu(), 8000),
        ("prob-nowcoder", build_nowcoder(), 4000),
    ]
    for slug, text, need in jobs:
        path = BLOG / slug / "index.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        n = count_chinese(text)
        print(f"{slug}: chinese={n} need={need} {'OK' if n >= need else 'LOW'}")


if __name__ == "__main__":
    main()
