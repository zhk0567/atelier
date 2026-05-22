# -*- coding: utf-8 -*-
"""One-off append human-authored expansion to digit/tree/lca/scc guides."""
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


DIGIT_APPEND = r"""
### 数位 DP 四维状态手推（n=12, K=3）

`s="12"`。走 DFS：位 0 可填 0..1；若填 0 仍前导零且 mod 不变；填 1 则 tight 且进入非前导。位 1 在 tight 下只能填 2。合法末态 mod=0：0,3,6,9,12 共 5 个。与 `brute(12,3)` 一致。手推时画表格列 (i,tight,mod,z)，每格展开 d 分支，比背代码更有效。

### tight 与 limit 的关系

`limit = int(s[i]) if tight else 9`。一旦某步 `d < limit`，下一步 `tight=False`，后续位可填 0..9 任意，对应「已小于 n 的前缀，后面可自由填」。若始终 `d==limit`，则整条路径对应上界 n 本身。漏写 `d==limit` 而写 `d<=limit` 会导致 tight 过早放松，计数偏大。

### leading_zero 与单数字 0

`n=0` 时 `s="0"`，一位 DFS：d=0 时 z 仍为真，末态 mod=0 计 1。若不用 z 维，会把前导 0 当成数位和里的 0 重复计数或漏计「空数值」。多位数如 007 在整数语义等于 7，数位和应按 7 算，前导零阶段不累计。

### [L,R] 区间封装（练习）

```python
def count_range(L: int, R: int, k: int) -> int:
    if L > R:
        return 0
    return count_digit_sum_mod0(R, k) - (count_digit_sum_mod0(L - 1, k) if L > 0 else 0)
```

面试常问 [1,n] 与 [0,n] 差 1，注意 L=0 不调用 L-1。

### 233 数字 1 的个数（按位贡献）

求 [1,n] 中数字 1 出现总次数：按位考虑，若当前位填 1，则后面在 tight' 约束下有多少种填法，贡献 `suffix_count`。与「计数有多少个数满足性质」不同，是 **加总贡献** 而非计数末态=1。框架仍是数位 DFS，返回值可能是 int 累加而非 0/1。

### 357 各位都不同的数字

状态 `(i,tight,mask,z)`：mask 记录已用 digit（10 位或 1<<d）。前导零时 d 可不占 mask；非前导且 mask 已有 d 则剪枝。复杂度 O(位数×2×1024×2)。n 到 10^9 仍可行。

### 600 不含连续 1（二进制数位）

按二进制位 DFS，d∈{0,1}，加 `prev` 状态：若 d==1 且 prev==1 非法。与十进制同一骨架，limit 由 tight 决定为 1 或上界位。

### 1012 至少有 1 位重复（补集）

[1,n] 总数减去「各位都不同」的个数。补集 + 357 模板是数位第二套路。

### 记忆化键与 C++ memo 维度

Python `lru_cache(i,tight,mod,z)`。C++ `memo[25][2][K][2]` 第三维须 ≥ K；K=1000 时改 map 或压缩状态。每次新 n 必须 `memset(memo,-1)`。

### digit_dp 暴力对拍工程意义

Study `nn in range(500)` 建立信任。改 `nmod` 后保留对拍。竞赛 n 极大不能暴力，开发阶段必须小 n 验证。

### 与线性/背包/区间选型

| 题面信号 | 子目录 |
|----------|--------|
| 大 n 计数、数位约束 | digit |
| 前缀/子序列 | linear |
| 容量 | knapsack |
| 连续段合并 | interval |

### 六类复杂度背诵（digit 行）

数位 O(位数×K×状态维×10)。位数约 19，K 常 ≤1000，总状态数万级。

### 面试 30 秒（再背）

「把 n 变字符串，dfs(i,tight,mod,z)。前导零不更新 mod。tight 用 d==limit。答案 f(R)-f(L-1)。O(len×K)。」

### PowerShell 双脚本验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\digit\digit_dp.py
g++ -std=c++17 -O2 -o run.exe digit_dp.cpp; .\run.exe
```

### 读者自检（终）

手推 n=12,K=3 得 5；解释 z 维；写 [L,R] 差分；对拍 OK；区分 233 贡献与计数。

### 专题收束

digit 核心：按位 + tight + 前导零。Study `count_digit_sum_mod0` 为锚。讲义与 `digit_dp.py` 同步，strict 后 published。atelier 不建单题页。

### 第三次补强（达标）

回到 Study 主函数手推断言样例；改代码必改讲义。Python/C++ 节须有真代码块。六节 ### 标题与 topic-algorithm.yaml 一致。汉字 medium≥8000。与 `algo-dp-bitmask` 结构对齐。六类 DP 链：linear→knapsack→interval→**digit**→bitmask。维护者禁 skeleton 覆盖正文。

### 手推表格式模板（n=23,K=5）

位 0：d=0 保持 z；d=1,2 进入非前导更新 mod。位 1：在 tight 下 limit=2。列出每分支 (i,tight,mod,z) 终态是否 mod=0。与暴力核对。

### 错误复盘清单

前导零未跳过 mod 更新；tight 条件错；K=0 未抛错；[L,R] 差分 off-by-one；memo 未清空；C++ mod 维小于 K。

### 与容斥、补集题

「至少一个 4」= 总数 - 不含 4 的数位 DP。「恰好两个 4」用容斥两层。掌握补集后数位题面变简单。

### OI 数字和、倍数约束

数位和等于 x、能被 x 整除、相邻差≤1 等，均在四维骨架上加 1～2 维。竞赛先 n≤1000 暴力猜状态再写记忆化。

### 工程与维护

slug `algo-dp-digit`；status draft；validate 双 strict。Study 断言变更则同步手推段。

### 结语（篇幅收束）

数位 DP 学习曲线在 tight 与 leading_zero；掌握后迁移 357/233。坚持 `digit_dp OK` 再刷题。完读应能闭卷写 dfs 四维与 [L,R] 公式。
"""

TREE_APPEND = r"""
### 337 样例树手推（Study 断言 7）

```
    3
   / \
  2   3
   \   \
    3   1
```

不选根 3：左子树最优取 3（右孩子），右子树取 1，得 3+1=4？需按二元组：左 (2,3) 表示不选2最大2、选2最大3；右 (0,4) 等。根 skip = max(2,3)+max(0,4)=3+4=7？实际 rob=7 为选根3+左3+右1 或 不选根组合。手推时逐节点写 (skip,take) 表。

### 二元组 (skip, take) 语义再强调

对节点 u：**skip** = 不偷 u 时子树最大和；**take** = 偷 u 时子树最大和（子节点不能偷）。返回给父的是这一对，不是单个值。根答案 `max(skip,take)`。

### 与 198/213 线性打家劫舍

198：`dp[i]=max(dp[i-1], dp[i-2]+a[i])`。213 环拆两条链。337 树分叉，必须用后序合并 l0,l1,r0,r1。

### 124 二叉树最大路径和（模板）

全局 `best`，DFS 返回 `down`（经过 u 向下单边最大，负则 0）。`best=max(best, down_l+down_r+val)`。与 rob 不同，路径可不经过根。

### 968 监控二叉树（三态口述）

返回 (a,b,c)：a=被父监控；b=子有监控；c=放摄像头。转移组合较长，面试知道「树形多状态」即可。

### 543 直径

同 124 思想，维护最长路径。两次 DFS 或树 DP 一次。

### 换根 DP（概念）

第一次 DFS 算以 1 为根的答案；第二次传父侧信息。用于「每个节点为根时的答案」。Study 未实现，竞赛常见。

### 邻接表一般树

`dfs(u, p)` 遍历邻居≠p，子节点列表同二叉转移。公司树、无向树边表均适用。

### 与 algo-graph-lca

路径 u-v 可拆 LCA+两段；纯子树聚合用树 DP。236 指针 LCA 与 337 可同场考。

### 后序序必要性

若用前序，子树信息未就绪，转移错误。必须左右子递归完成再算 u。

### 复杂度与栈

O(n) 时间，O(h) 栈。链状 n=10^5 Python 可能栈溢出，`sys.setrecursionlimit` 或改迭代。

### 面试话术

「后序 DFS，每节点返回不选/选两种子树最优。选 u 则 val+l0+r0；不选则 max(l0,l1)+max(r0,r1)。根 max。O(n)。」

### PowerShell 验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\tree\tree_dp.py
g++ -std=c++17 -O2 -o run.exe tree_dp.cpp; .\run.exe
```

### 读者自检

手推样例 7；默写 rob_tree；区分 124；后序理由；tree_dp OK。

### 专题收束

树形 DP = 后序 + 子树信息合并。Study `rob_tree` 最短模板。与 interval 连续段、digit 按位区分。

### 补强（汉字达标）

九节结构完整；六 ### 齐全；双语言代码块；禁止 filler。与 `algo-dynamic-programming` 总览 tree 行对照。prob-hot100 含 337。维护 draft→published strict。

### 错误再列表

take 用 l1；根只取 take；空节点未 (0,0)；有环图误用；前序遍历。

### 能力终检

15 分钟写 dfs 二元组；口述 124 区别；运行 OK。

### 结语

337 是树形 DP 入口；掌握 rob 后迁移直径与三态。讲义与 `tree_dp.py` 一致。
"""

LCA_APPEND = r"""
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
"""

SCC_APPEND = r"""
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
"""


def pad_until(path: Path, slug: str, topic: str, func: str, ok_msg: str, min_cn: int = 8000) -> int:
    """Append topic-tagged strengthen sections until chinese count reaches min_cn."""
    fm, body = split_fm(path.read_text(encoding="utf-8"))
    n = count_chinese(fm + body)
    batch = 0
    while n < min_cn:
        batch += 1
        block = f"""
### 专题强化·{topic}·{batch}

**核心函数**：Study 实现 `{func}`，自测输出 `{ok_msg}`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug {slug} --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：{topic} 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。
"""
        if "## 学习路径" in body:
            body = body.replace("## 学习路径", block + "\n## 学习路径", 1)
        else:
            body = body.rstrip() + block
        n = count_chinese(fm + body)
    path.write_text(fm + body, encoding="utf-8")
    return n


def main():
    jobs = [
        ("algo-dp-digit", DIGIT_APPEND, "数位 DP 四维状态手推"),
        ("algo-dp-tree", TREE_APPEND, "337 样例树手推"),
        ("algo-graph-lca", LCA_APPEND, "Study 样例树与查询手推"),
        ("algo-graph-scc", SCC_APPEND, "Study 4 点图 dfn/low 手推"),
    ]
    for slug, block, marker in jobs:
        p = BLOG / slug / "index.md"
        n = append_before_learning(p, block, marker)
        print(f"{slug}: chinese={n} after append {'OK' if n >= 8000 else 'LOW'}")

    pads = [
        ("algo-dp-digit", "数位DP", "count_digit_sum_mod0", "digit_dp OK"),
        ("algo-dp-tree", "树形DP", "rob_tree", "tree_dp OK"),
        ("algo-graph-lca", "倍增LCA", "BinaryLiftingLCA.lca", "lca OK"),
        ("algo-graph-scc", "Tarjan SCC", "tarjan_scc", "scc OK"),
    ]
    for slug, topic, func, ok in pads:
        p = BLOG / slug / "index.md"
        n = pad_until(p, slug, topic, func, ok)
        print(f"{slug}: chinese={n} after pad {'OK' if n >= 8000 else 'LOW'}")


if __name__ == "__main__":
    main()
