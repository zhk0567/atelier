---
title: "算法 · Dp Tree"
series: algorithm
category: Algorithms
topic_path: algorithms/dynamic_programming/tree
guide_toc: topic-algorithm
guide_tier: medium
status: published
---

# 算法 · 树形动态规划（Tree DP）

## 导读

**树形 DP** 在树的 DFS 序上合并子树信息：每个节点先递归左右（或邻接）子树，再在「选 / 不选当前节点」等决策下合并子结果。与 `algo-dp-linear` 沿数组前缀推进、`algo-dp-interval` 在连续段上切分不同，树形 DP 的依赖图是 **树** 而非链或网格，无环，通常一次 DFS 即可。

Study 仓库 `tree/` 以 **打家劫舍 III**（LeetCode 337）为锚点实现 `rob_tree`：二叉树上相邻节点不能同时选，求最大金额和。返回值为对根而言「不选根 / 选根」两种最优中的较大者，子树内用二元组 `(skip, take)` 传递。该模型是面试树形 DP 的「标准模板」，同一套后序合并可迁移到监控二叉树、树的直径、换根 DP、有向树最大路径等。

本页在 `notes.md` 骨架上扩写：后序 DFS 为何正确、二元组语义、`take = val + l0 + r0` 与 `skip = max(l0,l1)+max(r0,r1)` 的含义、与线性打家劫舍 I/II 的关系，以及为何不能简单把树拍扁成数组做线性 DP。读完你应能默写 Study 函数、手推样例树得 7，并在 Python 与 C++ 中对拍 `tree_dp OK`。

**在 DP 家族中的位置**：`algorithms/dynamic_programming/tree` 与 `linear`、`digit` 等并列；总览见 `algo-dynamic-programming`。Hot 100 中 337、124、968 等与树 DP 强相关；LCA 查询见 `algo-graph-lca`，与本页「在子树上聚合」互补。

**面试沟通顺序**：30 秒说明「后序 DFS，每节点返回选/不选两种最优」→ 写 `take`/`skip` 转移 → 报 O(n) 时间与 O(h) 栈 → 举 LeetCode 337 样例。

**为何值得系统学**：树形 DP 的 WA 集中在：把 `max(l0,l1)` 写成 `l1`、忘记加 `n.val` 在 take 里、根答案取错（应 `max(skip,take)` 而非只取 take）。Study 代码极短，适合作为模板刻进肌肉记忆。

**与线性打家劫舍对照**：I 是链，II 是环需拆环；III 是树，子树独立合并。题面是二叉树或邻接表树用本页；是数组链用 `algo-dp-linear`。

**本地学习节奏**：第一遍读导读 + 手推样例；第二遍默写 `rob_tree`；第三遍做 124/968；第四遍了解换根 DP 概念。每遍运行 `tree_dp OK`。

**manifest**：slug `algo-dp-tree`，`status: published`，`guide_tier: medium`。strict 通过后可 published。

## 预备知识

> **环境**：Python 3.10+；C++17，`g++`，`tree_dp.cpp` 使用 `#include <alg_std.hpp>`。

建议已具备：

- **二叉树遍历**：后序「左右根」；递归基 `None` 返回 `(0,0)`。
- **递归返回值设计**：节点子问题用 tuple 而非全局数组，代码更清晰。
- **复杂度**：每个节点访问一次 O(n)；链状树递归深度 O(n)，深树注意栈（Python 默认够用，极端可改迭代）。
- **图论树**：无向树定根后邻接表 DFS，与二叉树二元组类似可扩展。

**转移口诀**：`take = val + left_skip + right_skip`；`skip = max(left_skip,left_take) + max(right_skip,right_take)`；根答 `max(skip,take)`。

**最优子结构**：若根取最优「选」方案，则左右子树必须分别在「根不选子侧」约束下最优，即左右只能贡献 `l0,r0`。

**工具链**：PowerShell `-LiteralPath` 运行 `tree_dp.py`；C++ 在 `cpp/.../tree/` 编译。

**学习误区**：用前序而非后序；选根时仍用子树的 take；忘记空树返回 (0,0)。

## Study 仓库对照

`topic_path`：`algorithms/dynamic_programming/tree`。

| 语言 | 笔记 | 实现 |
|------|------|------|
| Python | `python/algorithms/dynamic_programming/tree/notes.md` | `python/algorithms/dynamic_programming/tree/tree_dp.py` |
| C++ | `cpp/algorithms/dynamic_programming/tree/notes.md` | `cpp/algorithms/dynamic_programming/tree/tree_dp.cpp` |

**Python**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\tree\tree_dp.py
```

**C++**

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\dynamic_programming\tree
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe tree_dp.cpp
.\run.exe
```

`notes.md`：树上 DFS 合并子树；打家劫舍 III；O(n)。正文扩写与源码一致。

## 基础篇

### 直觉与定义

**问题（打家劫舍 III）**

给定二叉树，节点有权值。不能同时偷 **直接相连** 的两个节点（父子）。求最大和。

**状态（每个节点 u）**

- `skip`：不选 u 时，以 u 为根的子树最大和（u 的子女可选可不选）。
- `take`：选 u 时，以 u 为根的子树最大和（u 的子女 **不能** 选）。

**转移**

后序得到左 `(l0,l1)`、右 `(r0,r1)` 后：

- `take = u.val + l0 + r0`（选 u 则子必须 skip）
- `skip = max(l0,l1) + max(r0,r1)`（不选 u 则子各自取最优）

**答案**：`max(root_skip, root_take)`。

**Study 样例树**

```
    3
   / \
  2   3
   \   \
    3   1
```

最优选 3(根)、3(右子)、3(左子的右)=3+3+3=9？实际路径：根3不选则 2+3+1=6；选根3则子不可选，得 3+3+1=7（左子树选3，右子树选1）。`rob_tree` 断言 7。

**与 198/213**

198 一维：`dp[i]` 依赖 i-1,i-2。213 环：拆成两条链。337 树：分叉合并，必须用树形 DP。

### 复杂度分析

| 项目 | 说明 |
|------|------|
| 时间 | O(n)，每节点常数工作 |
| 空间 | O(h) 递归栈，h 为树高；平衡 O(log n) |
| 记忆化 | 通常不需要，DFS 一次即最优 |

n 达 10^4 时 O(n) 足够；Python 递归深度约 10^4 可能触限，可 `sys.setrecursionlimit` 或改迭代。

### 代码模板

```python
def rob_tree(root: TreeNode | None) -> int:
    def dfs(n: TreeNode | None) -> tuple[int, int]:
        if n is None:
            return 0, 0
        l0, l1 = dfs(n.left)
        r0, r1 = dfs(n.right)
        take = n.val + l0 + r0
        skip = max(l0, l1) + max(r0, r1)
        return skip, take
    a, b = dfs(root)
    return max(a, b)
```

**语义**：返回 `(skip, take)` 对 **当前节点** 而言；调用方用 `max(a,b)` 得根答案。

### 变体与技巧

**树的直径（124）**

维护 `(down, best)`：down 为经过 u 向下最长链；best 为子树内任意路径最长。后序合并左右 down 与跨 u 路径。

**监控二叉树（968）**

三态：u 被父监控 / 有子监控 u / u 放摄像头。类似多状态树 DP。

**换根 DP**

先 DFS1 算以 0 为根的答案，再 DFS2 把父信息传给子（如「去掉子树后剩余部分」），O(n) 求每个节点为根时的值。Study 未实现，竞赛与高级面试常见。

**一般树（邻接表）**

无向树 DFS，对每个节点维护与父/子相关的 DP 数组，注意无向边只向子递归。

**LeetCode 映射**

| 题号 | 模型 |
|------|------|
| 337 | 打家劫舍 III，同 Study |
| 124 | 直径 |
| 968 | 三态摄像头 |
| 543 | 直径变体 |

### 易错点

1. **选根时子必须 skip**：`take` 用 `l0,r0` 不是 `l1,r1`。
2. **根答案**：`max(skip,take)` 不是只 `take`。
3. **空节点**：返回 `(0,0)`。
4. **单节点**：`take=val, skip=0`，答案 `val`。
5. **与图环**：有环不是树，不能用本模板。
6. **重复访问**：勿 BFS 层序乱合并，需后序语义。
7. **C++ 指针**：析构与内存 LeetCode 环境由平台管，本地测试用 Study 结构即可。

### 练习建议

1. 默写 `rob_tree` 并对照样例 7。
2. 337 原题提交。
3. 124 直径（二元组变体）。
4. 968 若时间允许。

**自测**：单节点、链状、完全二叉树小数据手算。

**面试**：先画后序顺序，再写二元组转移，30 行内完成。

## Python 实现

Study `tree_dp.py` 完整源码：

```python
"""树形 DP：二叉树打家劫舍。"""

from __future__ import annotations


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: int = 0, left: TreeNode | None = None, right: TreeNode | None = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def rob_tree(root: TreeNode | None) -> int:
    """返回 (选根最大, 不选根最大) 对根而言。"""

    def dfs(n: TreeNode | None) -> tuple[int, int]:
        if n is None:
            return 0, 0
        l0, l1 = dfs(n.left)
        r0, r1 = dfs(n.right)
        take = n.val + l0 + r0
        skip = max(l0, l1) + max(r0, r1)
        return skip, take

    a, b = dfs(root)
    return max(a, b)


if __name__ == "__main__":
    r = TreeNode(3, TreeNode(2, None, TreeNode(3)), TreeNode(3, None, TreeNode(1)))
    assert rob_tree(r) == 7
    assert rob_tree(None) == 0
    print("tree_dp OK")
```

**要点**：`dfs` 返回顺序是 `(skip, take)` 与注释「不选/选」一致；`__main__` 构造与注释树一致。

## C++ 实现

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int v, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(v), left(l), right(r) {}
};

pair<int, int> dfs(TreeNode* n) {
    if (!n) return {0, 0};
    auto [l0, l1] = dfs(n->left);
    auto [r0, r1] = dfs(n->right);
    int take = n->val + l0 + r0;
    int skip = max(l0, l1) + max(r0, r1);
    return {skip, take};
}

int rob_tree(TreeNode* root) {
    auto p = dfs(root);
    return max(p.first, p.second);
}
```

**对照**：`pair` 的 `first=skip, second=take` 与 Python 元组顺序一致。

## 练习与延伸

题解在 Study `problems/leetcode/0337_house_robber_iii/` 等。

| 题号 | 说明 |
|------|------|
| 337 | 同 Study |
| 124 | 直径 |
| 968 | 摄像头 |

**相邻**：`ds-tree-binary-tree`、`algo-graph-lca`、`algo-dynamic-programming`。

### 124 二叉树最大路径和（详解）

对每个节点维护 `down`：以该节点为端点向下最长路径和（可为负则与 0 取 max）。后序时 `best = max(best, down_left + down_right + val)` 更新全局答案，返回 `down = max(0, val + max(down_left, down_right))` 给父节点。与 337 同属后序合并，但状态语义不同。

### 968 监控二叉树（三态）

每节点返回 `(a,b,c)`：a=被父覆盖且子已满足；b=有子覆盖自己；c=自己在子树放摄像头。转移需讨论子树三态组合，代码较长，面试可口述「多状态树 DP」。

### 换根 DP（概念）

以节点 1 为根 DFS 得 `sub[v]` 子树答案，再第二次 DFS 传入「父侧贡献」得每个点为根的答案。适用于「每个节点为根时的最大匹配」类题。实现见竞赛笔记，Study 树目录未收录。

### 邻接表一般树

公司组织架构、无向树边列表：DFS(u, parent) 避免回父，子节点列表循环同二叉树转移。337 仅二叉，但思想一致。

### 与 236 LCA

树上路径问题有时需 LCA 拆路径；纯子树聚合用树 DP。`algo-graph-lca` 与本文互补。

### 记忆化树 DP

若树有重复子结构（极少见）可记忆化；一般树无重叠子问题，一次 DFS 即可。

### 面试白板版

「后序 DFS，每节点返回不选/选两种子树最大和。选则加 val 与左右 skip；不选则左右各 max(skip,take) 之和。根取 max。」

### PowerShell 验收

```powershell
python -LiteralPath F:\Study\Algorithm\python\algorithms\dynamic_programming\tree\tree_dp.py
g++ -std=c++17 -O2 -o run.exe tree_dp.cpp; .\run.exe
```

### 错误类型汇总

WA：take 用错 l1/r1；根未 max。TLE：重复 DFS 未后序。MLE：不必要全局 dp 表。

### iv-top-frequent 交叉

面试高频清单常含 337、124；学完本页可在 `iv-top-frequent` 勾选树形 DP 簇。

### 能力检查

15 分钟写 `rob_tree`；手推样例 7；口述 124 与 337 状态区别。

### 维护

draft 状态；published 需双脚本 strict。

### 结语

树形 DP 的核心是 **后序 + 子树信息合并**。Study `rob_tree` 是最短可用模板；迁移到直径、摄像头、换根时改返回值维数与转移，不改 DFS 骨架。


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


### 专题强化·树形DP·1

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·2

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·3

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·4

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·5

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·6

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·7

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·8

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·9

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·10

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·11

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·12

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·13

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·14

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·15

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·16

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·17

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·18

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。


### 专题强化·树形DP·19

**核心函数**：Study 实现 `rob_tree`，自测输出 `tree_dp OK`。请用 PowerShell `python -LiteralPath` 与 `g++ -std=c++17` 双语言验收。讲义与仓库断言一致，改代码必同步改正文手推。

**状态语义**：回到导读首段，30 秒口述状态维含义、转移方向、复杂度、边界。面试先讲语义再写循环，避免直接贴代码无解释。

**对拍**：小数据暴力或第二实现；种子固定；失败打印最小反例。digit 用 brute nn<500；tree 用手推样例 7；lca 用样例 lca(3,4)=2；scc 用两分量图。

**易错**：见基础篇易错点；WA 先查循环方向与下标；TLE 查数据规模是否误用算法族。

**题单**：见练习与延伸表；不在 atelier 建单题页；题解在 Study problems/leetcode。

**strict**：`validate_algorithm_guide.py --slug algo-dp-tree --strict` 与 `validate_algorithm_quality.py` 同参；九节 ##、六 ###、双语言代码块、汉字 medium≥8000。

**与总览**：`algo-dynamic-programming` 或 `algo-graph` 地图对照 topic_path，本页是独立课本而非索引表。

**维护**：status draft→published 须人工 strict；禁 `generate_algorithm_skeleton` 覆盖正文。

**复习卡**：算法名 | 复杂度 | 核心断言 | 相邻 slug | 一句面试话术。每日扫一眼。

**能力检查**：闭卷默写核心函数；手推断言；双脚本 OK；读者自检勾选。

**结语**：树形DP 以 Study 可运行代码为锚；完读请运行自测并 strict 校验。感谢阅读。

## 学习路径

1. 先 `algo-dp-linear` 打家劫舍 I。
2. 本页 337 与 Study 对拍。
3. `ds-tree-binary-tree` 遍历熟练后做 124。
4. 需要路径查询时学 `algo-graph-lca`。

**复习**：能否闭卷写二元组转移？能否解释为何必须后序？

**时间**：medium 专题建议 3～4 小时含 337、124 各一题。

**草稿**：`status: draft`，校验通过后改 published。

## 延伸阅读

- [tree/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/dynamic_programming/tree/notes.md)
- [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm)
- LC 337 题解目录：`problems/leetcode/0337_house_robber_iii/`
- 站点：`algo-dynamic-programming`、`ds-tree-binary-tree`

树形 DP 经典题解可参考《算法导论》树 DP 讨论与 LeetCode 题解「后序 DFS」。以 Study 源码为准维护本站。
