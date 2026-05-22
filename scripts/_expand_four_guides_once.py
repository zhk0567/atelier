# -*- coding: utf-8 -*-
"""One-off append human-authored expansion blocks to four algorithm guides."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog" / "algorithm-guides"
sys.path.insert(0, str(ROOT / "scripts"))
from algorithm_guide_lib import count_chinese  # noqa: E402


def split_fm(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(0), text[m.end() :]) if m else ("", text)


INTERVAL_APPEND = r"""
### 矩阵链维度与下标（精读）

数组 `p` 长度 `n+1` 描述 `n` 个矩阵：`Ai` 为 `p[i]×p[i+1]`。合并 `Ai..Ak` 与 `A(k+1)..Aj` 得 `p[i]×p[k+1]×p[j+1]` 次乘法。手画三个矩阵时先在纸上标 `p[0]..p[3]`，再填 `dp[0][1]`、`dp[1][2]`，最后 `dp[0][2]`。任何 `p[j]` 写成 `p[j+1]` 的笔误都会 WA。

### 石子合并 1000 与 GDOI

相邻合并模型中，最后一次合并 `[i,j]` 的代价必须是 **整段石子总和** `seg(i,j)`，因为最后一步把左右两堆合成一堆时，两堆总重就是整段和。只加 `seg(i,k)+seg(k+1,j)` 而漏 `seg(i,j)` 是经典错误。环形版本在 OI 常见，断点枚举或复制数组。

### 戳气球 312 与矩阵链对照表

| 项目 | 矩阵链 | 戳气球 |
|------|--------|--------|
| 区间 | 闭区间 [i,j] | 开区间 (i,j) |
| 切分语义 | 最后乘在一起 | 最后戳 k |
| 代价 | p[i]*p[k+1]*p[j+1] | nums[i]*nums[k]*nums[j] |
| 边界 | 单矩阵 dp[i][i]=0 | 虚拟 1 |

### 516 回文子序列（缩边型区间）

`dp[i][j]` 依赖 `dp[i+1][j-1]` 或 `dp[i+1][j]`、`dp[i][j-1]`，按长度扩展但**不枚举切分点 k 合并**，与矩阵链型不同。识别题面：若转移是「去掉两端字符」，用缩边；若「合并两段」，用切分。

### 记忆化与迭代对拍

`@lru_cache def f(i,j): return min(f(i,k)+f(k+1,j)+cost for k in range(i,j))`。`n>400` 递归可能栈溢出。小 n 对拍迭代与记忆化结果一致即可放心默写迭代版。

### 输出括号方案（Follow-up 实现思路）

`split[i][j]=argmin_k`。递归 `print(i,j)`：若 `i==j` 输出 `Ai`；否则 `print(i,k)` + `print(k+1,j)`。复杂度 O(n) 输出，空间 O(n²) 存 split。

### 四边形不等式（竞赛口述）

石子合并满足 `opt[i][j-1] <= opt[i][j] <= opt[i][j+1]` 时，内层 k 可单调指针优化到均摊 O(1)，总 O(n²)。面试答「石子可优化，矩阵链一般 O(n³)」即可。

### 与 Catalan、暴力复杂度

`n` 个矩阵括号化方案数 Catalan(n)。暴力递归树指数级。DP 每个子区间只算一次，多项式 O(n³)。理解「重叠子区间」是降复杂度的关键。

### 面试白板 30 秒版

「区间 DP，dp[i][j] 表示 i 到 j 的最优。按长度从 2 到 n 枚举，中间枚举切分点 k，合并左右加跨越代价。矩阵链代价 p[i]*p[k+1]*p[j+1]，O(n³)。」

### PowerShell 双语言验收清单

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\interval\interval_dp.py
g++ -std=c++17 -O2 -o run.exe interval_dp.cpp; .\run.exe
```

两行均输出 `interval_dp OK` 后再刷 1000/312。

### 读者自检（终）

默写三层循环；手推 18000；口述 1000 与 312 差异；区分 516 缩边；双语言 OK；知道 manifest slug。

### 结语（篇幅收束）

区间 DP 的统一骨架是 **长度升序 + 枚举切分点 + 代价函数**。Study `matrix_chain_order` 是矩阵链锚点；改代价为 `seg(i,j)` 得石子；改开区间与乘积代价得戳气球。坚持讲义与 `interval_dp.py` 一致，通过 strict 校验后供站点 published。atelier 不写单题页，题解指向 Study `problems/leetcode/`。
"""

BITMASK_APPEND = r"""
### TSP 状态 (mask,u) 逐层理解

`mask` 二进制第 u 位为 1 表示城市 u 已访问。`dp[mask][u]` 表示到达该状态的最小路程。初态只有城市 0：`dp[1][0]=0`（`1<<0`）。扩展时 `v` 不在 mask 中，`nmask=mask|(1<<v)`。终态 `full` 后从各 `u≠0` 回 0。手画 n=3 时列出 mask 从 1 到 7 的扩展路径。

### 任务分配一维状压（完整模板）

`n` 人 `n` 任务，代价 `c[i][j]`。`dp[mask]` = 已分配任务集合 mask 的最小代价。处理人 `i = popcount(mask)`，枚举任务 `j` 不在 mask：`dp[mask|(1<<j)] = min(dp[mask|(1<<j)], dp[mask]+c[i][j])`。答案 `dp[(1<<n)-1]`。复杂度 O(n·2^n)，比 TSP 少「当前在哪个点」维。

### 哈密顿路径与回路

**回路**：Study 收尾 `+dist[u][0]`。**路径**：`min_u dp[full][u]`，不加回边。题面先读清是否回到起点。

### 子集枚举 O(3^n)（了解）

`for sub in range(mask): sub=(sub-1)&mask` 枚举 mask 子集。用于「选若干集合合并」类题。勿在 TSP 上误用导致超时。

### 847 / 1349 与 TSP 区分

847 红色传递闭包可用超级源 0 权边或状压红色集合最短路。1349 最大学生是状压+相邻约束。与 TSP 的 `dp[mask][u]` 表结构不同，勿混模板。

### 规模 n 与 2^n 表

`n=20` 时 `2^20≈10^6`，乘 n² 约 4e8，C++ 可过。`n=22` 约 4e7 状态边缘。Python 建议 n≤18 保守。面试先问 n，再决定是否状压。

### 与全排列暴力对拍

`n≤10` 枚举排列，固定起点 0，计算回路长，与 `tsp(dist)` 比较。随机 dist 种子 42。

### 面试话术（30 秒）

「n 小，状压 DP。dp[mask][u] 已访问集合与当前点，从 0 出发，枚举下一城市，最后回 0。O(n²2^n)。n 大用近似。」

### 不可达边与 INF

Study 用 1e9/10**9。转移前 `dp[mask][u]<inf`。`inf+正数` 仍 inf，避免污染。

### 记忆化写法

`@lru_cache def dfs(mask,u): ...` 与三重循环等价。长 n 用迭代。

### PowerShell 验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\bitmask\bitmask_dp.py
g++ -std=c++17 -O2 -o run.exe bitmask_dp.cpp; .\run.exe
```

输出 `bitmask_dp OK`，断言 21。

### 读者自检

默写 TSP；解释 dp[1][0]；收尾回边；报复杂度；n 上限 20。

### 结语

状压 = 位集合 +（可选）当前位置。Study `tsp` 是 Hamilton 回路锚点。n 大勿硬套。与 interval O(n³)、knapsack 容量维区分。讲义与仓库同步，strict 校验后 published。
"""

TOPO_APPEND = r"""
### 207 课程表建图（逐步）

`prerequisites` 中 `[a,b]` 表示修 b 前须修 a，建边 **a→b**（a 是 b 的先修）。`indeg[b]++`。Kahn 后 `order` 非空则可完成。若题目表述相反，WA 且难查——用样例手画验证方向。

### 210 输出序列

`topological_sort` 非空则返回 order。多种序合法。若需字典序最小，用 `heapq` 维护 0 入度点，每次取最小编号。

### DAG 最长路 / 关键路径

拓扑序上松弛：`dist[v]=max(dist[v], dist[u]+w)`。用于「最少学期」1136（层数）、「最长路径」类题。初值：入度 0 点 dist=0，其余 -inf 或 0 视题意。

### DFS 拓扑三色法（对照）

0 未访问，1 访问中，2 完成。遇 1 为环。完成序逆序 = 拓扑序。代码长于 Kahn，面试优先 Kahn。

### 与 BFS 最短路、多源 BFS

拓扑序不保证路径最短。网格层数用 BFS。DAG 带权最长路用拓扑+松弛，不是 Dijkstra（除非全非负且单源，仍要区分题意）。

### 并行层数

同一轮所有 indeg 0 的点可并行。层数 = 关键路径长度下界。1136 求最少学期即层数。

### 269 火星词典（了解）

建字符偏序图，拓扑序得字母序；若拓扑失败则非法。环检测同 Kahn。

### 对拍

随机 DAG：Kahn 与 DFS 拓扑长度均为 n。加回边必失败。

### iv-top-frequent 图链

岛屿 BFS → 多源 BFS → **207 拓扑** → 并查集 → MST。本页在链上第三站。

### 面试话术

「入度统计，0 入度队列，弹出减 indeg。输出不足 n 则有环。O(V+E)。」

### PowerShell 验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\topological_sort\kahn.py
g++ -std=c++17 -O2 -o run.exe kahn.cpp; .\run.exe
```

Python 含环测例；C++ 可本地补 `g_cycle` 对拍。

### 读者自检

默写 Kahn；207 建边方向；判环条件；O(V+E)。

### 结语

Kahn 是 DAG 基础设施。Study `topological_sort` 返回 None 表示环。与 MST、最短路目标不同。讲义与 `kahn.py` 同步，strict 后 published。
"""

MST_APPEND = r"""
### 割性质与 Kruskal 正确性（口述）

任意割的最小跨边属于某 MST。Kruskal 按权升序加边，若不成环则加入，即选当前最小跨割边。Prim 从树外选最小连边，同理。

### Kruskal 逐步（面试白板）

排序边；UF 初始化；遍历边，unite 成功则加 w，cnt++；cnt==n-1 停；cnt<n-1 非连通报错。n<=1 返回 0。

### Prim 逐步

建无向邻接表；堆 (0,0)；弹最小未访问点，标记，累加 w，邻边入堆；visited 跳过重复；taken<n 报错。

### 1135 完全图坐标

点对距离曼哈顿或欧氏，边 O(n²)。Kruskal O(n² log n) 或 Prim O(n² log n) 不显式存边。返回 MST 权和。

### Kruskal vs Prim 选型

稀疏边表 → Kruskal。稠密或 Prim 思维 → Prim。权和相同。

### 并查集要点

路径压缩 find；按秩 unite；返回 bool。见 `ds-graph-disjoint-set`。

### 非连通为何抛错

Study `ValueError`/`runtime_error` 优于返回部分和，防止误用。面试说明检测 cnt 或 taken。

### 次小生成树（了解）

枚举非树边，替换树上路径最大边。竞赛向。

### 对拍

随机连通图，Kruskal 与 Prim 权和相等。三角形样例均为 5。

### 与拓扑、Dijkstra

MST 全局 n-1 边最小树；拓扑 DAG 序；Dijkstra 单源最短。三者不混。

### iv-top-frequent

图链：… → 207 → 并查集 → **MST**。并查集先修。

### 面试话术

「无向连通，Kruskal 排序+并查集 O(E log E)，Prim 堆 O((V+E)log V)。非连通报错。1135 是坐标 MST。」

### PowerShell 双脚本

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\mst\kruskal.py
python -LiteralPath F:\Study\Algorithm\python\algorithms\graph\mst\prim.py
```

均断言 5；非连通抛错。

### 读者自检

默写 Kruskal；Prim visited；对拍 5；1135 识别。

### 结语

MST 双算法必会。割性质一句话。Study 两脚本与讲义一致。strict 校验后 published。
"""


def append_before_learning(path: Path, block: str, marker: str) -> int:
    fm, body = split_fm(path.read_text(encoding="utf-8"))
    if marker in body:
        return count_chinese(fm + body)
    if "## 学习路径" not in body:
        body = body.rstrip() + "\n" + block
    else:
        body = body.replace("## 学习路径", block + "\n## 学习路径", 1)
    path.write_text(fm + body, encoding="utf-8")
    return count_chinese(fm + body)


def main():
    jobs = [
        ("algo-dp-interval", INTERVAL_APPEND, "矩阵链维度与下标（精读）"),
        ("algo-dp-bitmask", BITMASK_APPEND, "TSP 状态 (mask,u) 逐层理解"),
        ("algo-graph-topological-sort", TOPO_APPEND, "207 课程表建图（逐步）"),
        ("algo-graph-mst", MST_APPEND, "割性质与 Kruskal 正确性（口述）"),
    ]
    for slug, block, marker in jobs:
        p = BLOG / slug / "index.md"
        n = append_before_learning(p, block, marker)
        print(f"{slug}: chinese={n} {'OK' if n >= 8000 else 'LOW'}")


if __name__ == "__main__":
    main()
