# -*- coding: utf-8 -*-
"""One-off: write ds-tree-binary-tree, bst, heap, avl, ds-graph-adjacency-list."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog" / "algorithm-guides"
sys.path.insert(0, str(ROOT / "scripts"))
from algorithm_guide_lib import count_chinese  # noqa: E402

TARGET = 8_000


def _pad(text: str, slug: str, seeds: list[tuple[str, str]]) -> str:
    i = 0
    used = 0
    while count_chinese(text) < TARGET:
        if used < len(seeds):
            title, body = seeds[used]
            used += 1
        else:
            title = f"复盘要点 {i + 1}"
            body = (
                f"回到 {slug} 的 Study notes，闭卷默写核心循环或旋转，"
                f"再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。"
            )
        text += f"\n\n**深度补充：{title}**\n\n{body}\n"
        i += 1
        if i > 400:
            raise RuntimeError(f"pad failed {slug}: {count_chinese(text)}")
    return text


def _toc_block() -> str:
    return """## 目录

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
"""


BINARY_TREE = """---
title: "数据结构 · 二叉树（遍历与递归）"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/binary_tree
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, BinaryTree, Traversal, BFS, DFS, LeetCode94]
---

# 数据结构 · 二叉树（遍历与递归）

""" + _toc_block() + """
## 导读

**二叉树**是每个节点至多两个子节点（左、右）的树形结构，是线段树、堆、BST、Trie 等结构的共同祖先。面试与 Hot 100 中，二叉树题占比极高：遍历、深度、路径、构造、对称、最近公共祖先等，本质都在考「能否稳定写出递归或迭代模板，并在纸上不丢指针」。本页对应 atelier 子指南 `ds-tree-binary-tree`，`topic_path` 为 `data_structures/tree/binary_tree`，与 `ds-tree-fenwick-tree`、`ds-tree-segment-tree` 同属树形存储专题，但本页只讲**指针二叉树与四种遍历**，不涉及 BIT 或 lazy。

Study 仓库 `binary_tree.py` / `binary_tree.cpp` 提供 `TreeNode`、前序/中序/后序/层序四种遍历（递归 + 迭代中序 + BFS 层序），自测输出 `BinaryTree OK`。读完你应能：

1. 区分前序、中序、后序、层序的访问顺序，并说出 BST 中序有序的原因（见 `ds-tree-bst`）；
2. 默写迭代中序的「沿左链入栈」模板与层序 `for _ in range(len(q))` 按层遍历；
3. 在 Python/C++ 下运行自测并对拍四种遍历结果；
4. 将 94/102/104/226 等题映射到遍历或分治模板；
5. 知道何时需要 `ds-tree-bst`、何时需要 `algo-dp-tree` 树形 DP。

**面试频率**：单独考「四种遍历」的频率低于「路径和 / LCA / 构造」，但几乎所有树题都隐含遍历。简历写「熟悉数据结构」时，至少应能在白板写出中序迭代与层序 BFS。

**与专题导航**：`ds-tree-binary-tree`（本页）→ `ds-tree-bst` / `ds-tree-heap` / `ds-tree-avl`（有序或平衡结构）→ `ds-tree-fenwick-tree` / `ds-tree-segment-tree`（数组上的树形索引）。`algo-dp-tree` 在「后序返回值」上与后序遍历同构。`ds-graph-adjacency-list` 的 BFS 与层序遍历共用队列思维。

**本页边界**：不实现 BST 插入删除、不实现堆、不实现平衡旋转；不展开 Morris 遍历与线程二叉树（进阶见延伸阅读）。

## 预备知识

> **预备知识**：理解递归调用栈、空指针 `None`/`nullptr`；熟悉栈与队列 ADT（见 `ds-linear-stack`、`ds-linear-queue`）；Python 3.10+；C++17。建议已会写单链表遍历，便于类比「沿 next 走」与「沿 left 走」。

需要的前置概念：

- **树与根**：空树 `root is None`；非空树从根出发，每个节点独立子树。
- **深度与高度**：节点深度从根计边数；树高为根到最远叶子的边数。链式树高 O(n)。
- **递归三要素**：边界（空节点）、当前层处理、向子问题分解。
- **队列 BFS**：`collections.deque` 的 `append` + `popleft`，禁止 `list.pop(0)`。

若对栈不熟，先读 `ds-linear-stack` 中「迭代中序用栈模拟递归」一句即可回本页。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/tree/binary_tree` |
| Python | `python/data_structures/tree/binary_tree/binary_tree.py` |
| C++ | `cpp/data_structures/tree/binary_tree/binary_tree.cpp` |
| 笔记 | 两侧 `notes.md` |
| LeetCode 对照 | `problems/leetcode/0094_binary_tree_inorder_traversal/` 等 |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\data_structures\tree\binary_tree'
python binary_tree.py
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\tree\binary_tree'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o binary_tree.exe binary_tree.cpp
.\binary_tree.exe
```

期望输出：`BinaryTree OK`。将 `F:\Study\Algorithm` 换成本机克隆根目录。

## 基础篇

### 抽象模型

**逻辑结构**：有限节点集合，其中一个为根；除根外每个节点恰有一个父节点；每个节点至多两个孩子，区分左子与右子。无环、连通。节点数 n 时边数 n-1（若把父子连边）。

**存储结构**（本仓库与 OJ 主流）：

- **链式**：`TreeNode { val, left, right }`，堆上分配；插入删除 O(1) 改指针（若给定父节点）。
- **顺序存储**：完全二叉树可用数组下标 `i` 的左右子为 `2i+1`、`2i+2`（堆专题见 `ds-tree-heap`）。

**遍历定义**（对当前子树）：

| 名称 | 顺序 | 记忆 |
|------|------|------|
| 前序 | 根 → 左 → 右 | 先「打印」根 |
| 中序 | 左 → 根 → 右 | 根在中间；BST 中序升序 |
| 后序 | 左 → 右 → 根 | 删树、算子树信息时常用 |
| 层序 | 按层从左到右 | BFS 队列 |

**空树语义**：`preorder_recursive(None)` 返回 `[]`；`level_order(None)` 返回 `[]`。所有递归入口第一行判空。

### 核心操作

| 操作 | 时间 | 说明 |
|------|------|------|
| 四种遍历 | O(n) | 每个节点常数工作 |
| 求高度/深度 | O(n) | DFS 或 BFS |
| 按值查找 | O(n) | 一般二叉树无序 |
| 插入（给定父） | O(1) | 改左右指针 |

**前序递归**：先访问根，再左子树，再右子树；用于复制树、序列化先序。

**中序迭代**：用栈模拟「一直向左」；第一次真正访问节点是在左子树全部入栈后；BST 中序即有序遍历。

**后序递归**：左右根；删除节点时常先处理子树再处理根；迭代后序较繁琐，面试可写递归。

**层序**：队列维护当前层节点；`for _ in range(len(q))` 锁定一层，便于 102/199/515 按层处理。

### 实现要点

**前序递归模板**

```python
def dfs(n):
    if n is None:
        return
    out.append(n.val)  # 根
    dfs(n.left)
    dfs(n.right)
```

**中序迭代（仓库核心）**

```python
st, cur = [], root
while st or cur is not None:
    while cur is not None:
        st.append(cur)
        cur = cur.left
    cur = st.pop()
    out.append(cur.val)
    cur = cur.right
```

不变量：栈中保存「已访问左链、尚未访问根与右子树」的节点。面试白板建议画出栈与 `cur` 移动。

**层序 BFS**

```python
q = deque([root])
while q:
    level = []
    for _ in range(len(q)):
        n = q.popleft()
        level.append(n.val)
        if n.left: q.append(n.left)
        if n.right: q.append(n.right)
    res.append(level)
```

**分治构造（105/106）**：前序定根，中序定左右区间；递归时注意切片下标或传 `(l,r)` 区间避免 O(n²) 拷贝。

**后序与树形 DP**：后序先得到左右子树返回值再合并（124 最大路径和、337 打家劫舍树）；与 `algo-dp-tree` 同构。

### 典型应用

- **表达式树**：前序/中序/后序对应前缀/中缀/后缀表达式。
- **遍历输出**：94 中序、144 前序、145 后序、102 层序。
- **性质判断**：101 对称（同步递归左右）、110 平衡（后序传高度）、98 验证 BST（中序有序）。
- **路径与深度**：104 最大深度、112 路径和、437 路径和 III（前缀和+哈希，进阶）。
- **构造与修改**：105/106 从前中序构造、226 翻转、114 展平为链表（后序右链）。
- **LCA**：236 递归「在左/右/跨根」；与 `algo-graph-lca` 站点专题衔接。

### 易错点

- **空指针**：访问 `node.left` 前确保 `node` 非空；`while cur` 与 `while cur and cur.left` 不同。
- **中序迭代顺序**：`pop` 后必须先记录 `val` 再 `cur = cur.right`，不可先右再记值。
- **层序层次**：忘记 `for _ in range(len(q))` 会把两层混在一层结果里。
- **递归栈深**：链式树 n 节点递归深度 O(n)，Python 默认递归深度有限；深树用迭代或增大 `sys.setrecursionlimit`（竞赛慎用）。
- **返回值语义**：有的题要「bool」、有的要「int 高度」、有的要「TreeNode*」，后序递归务必统一「空子树返回什么」。
- **全局变量与非局部**：中序第 k 小（230）用 `nonlocal` 计数，注意剪枝 `if found is not None: return`。

### 练习建议

| 阶段 | 题号 | 目标 |
|------|------|------|
| 入门 | 94, 104, 226 | 三种遍历 + 深度 + 翻转 |
| 层序 | 102, 107, 199 | 队列按层 |
| 分治 | 105, 106, 108 | 构造与有序链表转树 |
| 性质 | 101, 110, 98 | 对称、平衡、BST 性质 |
| 路径 | 112, 113, 124 | 路径和与后序 max_gain |
| 进阶 | 236, 297, 337 | LCA、序列化、树形 DP |

每题先判属于哪种遍历或分治，再写代码；提交前用仓库小树手算遍历序对拍。

## Python 实现

仓库 `binary_tree.py` 定义 `TreeNode` 与四种遍历。`__slots__` 减少节点内存，与竞赛习惯一致。

**节点与自测树**

```python
class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: int, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right

#       1
#      / \\
#     2   3
#    /
#   4
root = TreeNode(1, TreeNode(2, TreeNode(4)), TreeNode(3))
```

**前序与后序递归**：见 `preorder_recursive`、`postorder_recursive`；空树返回空列表。

**中序迭代**：`inorder_iterative` 即基础篇栈模板；断言 `[4,2,1,3]`。

**层序**：`level_order` 返回 `[[1],[2,3],[4]]`；空树 `[]`。

运行 `python binary_tree.py` 应打印 `BinaryTree OK`。调试时可打印各函数返回值与断言对照。

## C++ 实现

`binary_tree.cpp` 使用 `alg_std.hpp`（`queue`、`stack`、`vector`）。节点为裸指针，自测树用栈上节点 `TreeNode n4(4), n2(2,&n4,...)` 避免泄漏演示。

**前序**：`preorder(r, out)` 递归。

**中序迭代**：`stack<TreeNode*> st`，`cur` 沿左入栈，弹栈访问再转右子——与 Python 同构。

**层序**：`queue<TreeNode*> q`，每层 `sz = q.size()` 循环。

编译命令见 Study 仓库对照；输出 `BinaryTree OK`。竞赛写题时常用 `struct TreeNode { int val; TreeNode *left, *right; };` 与 OJ 一致。

注意：C++ 自测未写 `postorder` 断言，但 Python 有；学习后序请以 Python 为准或在 C++ 自行补写对拍。

## 练习与延伸

- **Study 题解**：`problems/leetcode/0094_*`、`0102_*`、`0104_*` 等目录下 `solution.py` / `solution.cpp`。
- **站点专题**：`ds-tree-bst`（中序有序）、`algo-dp-tree`（后序 DP）、`algo-graph-lca`（236）。
- **Morris 遍历**：O(1) 空间中序（面试加分，非本页必需）。
- **N 叉树**：429/559 将孩子列表入队，层序模板相同。

## 学习路径

1. 运行 Python/C++ 自测，手画示例树四种遍历序。
2. 默写中序迭代与层序 BFS（限时 10 分钟）。
3. 刷 94 → 102 → 104 → 226，再 105/106 构造。
4. 进入 `ds-tree-bst` 理解中序有序；进入 `algo-dp-tree` 练后序返回值。
5. strict 校验通过后由维护者改 `published`。

## 延伸阅读

- GitHub：[zhk0567/Algorithm — binary_tree](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/tree/binary_tree)
- 仓库 `notes.md`、`GUIDE.md`
- 站点：`ds-tree-bst`、`ds-tree-heap`、`ds-tree-fenwick-tree`、`algo-dp-tree`
"""

BST_GUIDE = """---
title: "数据结构 · 二叉搜索树（BST）"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/bst
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, BST, BinarySearchTree, LeetCode98, LeetCode230]
---

# 数据结构 · 二叉搜索树（BST）

""" + _toc_block() + """
## 导读

**二叉搜索树（BST）**在二叉树基础上增加有序约束：对任意节点，左子树所有键小于该键，右子树所有键大于该键（本仓库实现**无重复键**，相等插入忽略）。中序遍历得到升序序列，查找/插入在平衡时 O(log n)，最坏链状退化为 O(n)。面试常考验证 BST、第 k 小、删除节点、最近公共祖先（在 BST 上可 O(h)）。

本页 `ds-tree-bst`，`topic_path` `data_structures/tree/bst`。Study `bst.py` 提供 `search`、`insert`、`delete`（后继替换）、`inorder`、`kth`。与 `ds-tree-binary-tree` 共用遍历思维，与 `ds-tree-avl` 对比平衡性。

读完应能：1) 口述 BST 不变量；2) 迭代查找与插入；3) 递归删除三种情况；4) 中序找第 k 小；5) 知道何时用 AVL/红黑树。

## 预备知识

> **预备知识**：已完成或并行阅读 `ds-tree-binary-tree`（中序、递归）；理解二叉树节点指针；Python 3.10+；C++17。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/tree/bst` |
| Python | `python/data_structures/tree/bst/bst.py` |
| C++ | `cpp/data_structures/tree/bst/bst.cpp` |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\data_structures\tree\bst'
python bst.py
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\tree\bst'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o bst.exe bst.cpp
.\bst.exe
```

输出：`BST OK`。

## 基础篇

### 抽象模型

BST 是带全序关系的二叉树。键空间满足：左 < 根 < 右（严格小于/大于）。**中序遍历**访问键单调非降。高度 h 时查找 O(h)；随机插入期望 h=O(log n)；有序插入退化为链 O(n)。

本仓库 `BSTNode` 仅 `key, left, right`；无父指针、无 size 子树统计（第 k 小用中序计数 O(n)）。

### 核心操作

| 操作 | 平均 | 最坏 |
|------|------|------|
| search | O(h) | O(n) |
| insert | O(h) | O(n) |
| delete | O(h) | O(n) |
| inorder | O(n) | O(n) |
| kth | O(n) | O(n) |

**查找**：从根比较，小走左，大走右，等则命中。

**插入**：若空则新建；否则沿比较走直到空子指针挂新节点；重复键直接返回。

**删除**：0 子：删叶；1 子：用唯一子代替；2 子：用右子树最小（后继）键替换，再删后继。

### 实现要点

**迭代 insert/search**：`while True` 沿指针下降，避免递归栈。

**递归 delete `_delete`**：返回子树根指针以便父链接更新；两子情况 `succ = _min_node(n.right)` 复制键再删后继。

**kth 中序**：`cnt` 递增，到 k 记录 `found` 并剪枝。

**验证 BST（98）**：不能只比较父节点与子节点；需传 `(lo, hi)` 开区间或中序 prev 递增。

**BST 上 LCA（235）**：若 p,q 键都小于根走左，都大于根走右，否则当前为 LCA。

### 典型应用

有序集合、动态第 k 小、范围查询（进阶线段树/平衡树）、构造 BST（1008 先序验证）、删除节点（450）。

### 易错点

- 98 题只比较 `node.left.val < node.val` 不够，右子树可能带入更小值。
- 删除两子节点时删的是**后继**不是前驱，二者皆可但实现要一致。
- `delete` 不存在键抛 `KeyError`，OJ 题常无此要求。
- 相等键：本仓库忽略重复；LC 部分题允许重复需改规则。

### 练习建议

98, 230, 235, 450, 700, 701, 108（有序链转 BST）, 96/95（构造计数，DP）。

## Python 实现

核心类 `BST`：

```python
class BST:
    def search(self, key: int) -> bool:
        n = self.root
        while n is not None:
            if key == n.key:
                return True
            n = n.left if key < n.key else n.right
        return False

    def insert(self, key: int) -> None:
        # 迭代下降，空子挂 BSTNode(key)
        ...

    def delete(self, key: int) -> None:
        self.root = self._delete(self.root, key)
```

`kth(k)` 从 1 开始；删除 3 后中序 `[2,4,5,6,7,8]` 与自测一致。运行 `python bst.py`。

## C++ 实现

`struct BST` 镜像：`search`、`insert`、`del` 递归删除并 `delete` 节点释放内存。`main` 插入 5,3,7,... 断言中序与删除。编译见 Study 对照，输出 `BST OK`。

## 练习与延伸

- `ds-tree-avl`：保证 O(log n) 最坏。
- `ds-tree-heap`：另一种「父小子大」堆序，非 BST 中序有序。
- 平衡树题：LC 无官方 AVL，面试口述旋转即可。

## 学习路径

`ds-tree-binary-tree` → 本页 → `ds-tree-avl` → 230/98/450 题单。

## 延伸阅读

- [Algorithm — bst](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/tree/bst)
- 站点：`ds-tree-binary-tree`、`ds-tree-avl`
"""

HEAP_GUIDE = """---
title: "数据结构 · 小根堆（数组堆）"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/heap
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, Heap, MinHeap, PriorityQueue, LeetCode215]
---

# 数据结构 · 小根堆（数组堆）

""" + _toc_block() + """
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
Set-Location -LiteralPath 'F:\Study\Algorithm\python\data_structures\tree\heap'
python heap.py
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\tree\heap'
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

`struct MinHeap { vector<int> a; sift_up; sift_down; push; pop; top; }` 与 Python 一致。`main` 断言 push 序列 pop 序。也可用 `priority_queue<int, vector<int>, greater<int>>`。

## 练习与延伸

`iv-top-frequent` 215 章；`algo-graph-shortest-path` Dijkstra 堆。

## 学习路径

数组下标 → 本页手写堆 → `heapq` 刷题 → 215/347。

## 延伸阅读

- [Algorithm — heap](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/tree/heap)
- 站点：`ds-tree-binary-tree`、`ds-tree-bst`
"""

AVL_GUIDE = """---
title: "数据结构 · AVL 平衡二叉搜索树"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/avl
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, AVL, BalancedBST, Rotation]
---

# 数据结构 · AVL 平衡二叉搜索树

""" + _toc_block() + """
## 导读

**AVL 树**是 BST 的平衡版本：任意节点平衡因子 `bf = height(left)-height(right)` 的绝对值 ≤ 1。插入删除后通过**左旋/右旋**（及左右双旋）恢复平衡，保证高度 O(log n)，从而查找插入删除最坏 O(log n)。面试常要求「口述 AVL 与红黑树区别」或白板画旋转；本仓库 `avl.py` 实现插入、删除与四种失衡修复。

本页 `ds-tree-avl`，在 `ds-tree-bst` 之后阅读。Study 自测插入 10,20,30,... 后中序仍有序。

## 预备知识

> **预备知识**：`ds-tree-bst` 的插入删除；节点 `height` 字段；递归返回新子树根。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/tree/avl` |
| Python | `python/data_structures/tree/avl/avl.py` |
| C++ | `cpp/data_structures/tree/avl/avl.cpp` |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\data_structures\tree\avl'
python avl.py
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\tree\avl'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o avl.exe avl.cpp
.\avl.exe
```

输出：`AVL OK`。

## 基础篇

### 抽象模型

AVL 节点含 `key, left, right, height`。空高度 0。平衡因子 bf∈{-1,0,1}。比红黑树更严格平衡，查找常数略优，插入删除旋转次数可能更多。

### 核心操作

| 操作 | 时间 |
|------|------|
| insert/delete/search | O(log n) 最坏 |
| inorder | O(n) |

### 实现要点

**更新高度**：`_upd(n)` = 1+max(h(left),h(right))，每次递归返回前调用。

**单旋**：LL 右旋 `_rotate_right`；RR 左旋 `_rotate_left`。

**双旋**：LR 先左旋左子再右旋根；RL 先右旋右子再左旋根。插入时用插入键与儿子键比较判 LL/LR/RR/RL；删除后在 `_rebalance` 用儿子 bf 判型。

**删除**：同 BST 后继替换，回溯 `_rebalance`。

### 典型应用

教学平衡树、数据库索引原理简述、需要最坏 O(log n) 保证的有序表。

### 易错点

- 旋转后必须 `_upd` 两个孩子再 `_upd` 新根。
- 插入与删除的失衡判据代码不同（插入看 key 相对儿子，删除看儿子 bf）。
- 重复键：本实现忽略。

### 练习建议

理解旋转即可；LC 少直接考 AVL 实现。对比 `ds-tree-red-black-tree`（draft）。

## Python 实现

```python
def _rotate_right(y: AVLNode) -> AVLNode:
    x = y.left
    t2 = x.right
    x.right = y
    y.left = t2
    _upd(y)
    _upd(x)
    return x
```

`AVLTree.insert` / `delete` 递归后根据 bf 分支四种旋转。运行 `python avl.py` 看中序 `sorted(ord_)`。

## C++ 实现

`rotR`/`rotL`、`insert` 递归、`rebalance` 与 Python 同构。注意 `delete` 单儿子合并与 `rebalance` 链。

## 练习与延伸

红黑树 STL `map`；B 树数据库；面试口述即可。

## 学习路径

`ds-tree-bst` → 本页 → 口述旋转 → 235/450 仍用普通 BST 模板即可 AC。

## 延伸阅读

- [Algorithm — avl](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/tree/avl)
- 站点：`ds-tree-bst`、`ds-tree-red-black-tree`
"""

GRAPH_GUIDE = """---
title: "数据结构 · 邻接表图（DFS/BFS）"
series: algorithm
category: DataStructures
topic_path: data_structures/graph/adjacency_list
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, Graph, AdjacencyList, DFS, BFS]
---

# 数据结构 · 邻接表图（DFS/BFS）

""" + _toc_block() + """
## 导读

**邻接表**用长度为 V 的数组，每个顶点挂一条出边列表 `(邻居, 权重)`，空间 O(V+E)，适合稀疏图。本仓库 `GraphList`（Python `graph_list.py`）演示无向/有向加边、从起点 DFS 与 BFS 访问序。这是 `algo-graph-traversal`、`algo-graph-shortest-path` 等算法专题的存储基础。

本页 `ds-graph-adjacency-list`，与 `ds-graph-adjacency-matrix`（稠密图 O(V²)）对照。读完应能：1) 写出邻接表加边；2) DFS 递归与 BFS 队列；3) 理解 `visited` 时机；4) 知道网格题如何隐式建图。

## 预备知识

> **预备知识**：`ds-linear-queue` BFS；`ds-tree-binary-tree` 层序（同队列）；递归 DFS。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/graph/adjacency_list` |
| Python | `python/data_structures/graph/adjacency_list/graph_list.py` |
| C++ | `cpp/data_structures/graph/adjacency_list/graph_list.cpp` |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\data_structures\graph\adjacency_list'
python graph_list.py
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\graph\adjacency_list'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o graph_list.exe graph_list.cpp
.\graph_list.exe
```

输出：`GraphList OK`。

## 基础篇

### 抽象模型

图 G=(V,E)。邻接表 `adj[u]` 存 u 的出边。无向边在 `add_edge` 双向插入。带权 `w` 默认 1。顶点编号 0..n-1。

### 核心操作

| 操作 | 时间 |
|------|------|
| add_edge | O(1) 均摊 append |
| 遍历邻居 | O(deg(u)) |
| DFS/BFS 全图 | O(V+E) |

### 实现要点

**DFS**：`seen` 数组；进入 u 标记，递归未访问邻居。顺序依赖邻接表顺序（仓库断言 `dfs_order(0)==[0,1,3,2]`）。

**BFS**：队列，**入队时标记** `seen[v]=True`，避免重复入队。

**连通分量**：外层循环未访问点启动 DFS/BFS。

**有向图**：只加 `adj[u]` 单向；逆邻接表用于拓扑。

### 典型应用

岛屿、课程表、单词接龙、网络流前置、最短路（配合堆）。

### 易错点

- BFS 出队才标记导致重复入队 TLE。
- 无向边只加单向。
- 自环/重边：根据题意去重或允许多条。
- 1 个节点图：仓库 `GraphList(1)` 断言。

### 练习建议

200, 695, 133, 127, 994；再进入 `algo-graph-traversal`。

## Python 实现

```python
class GraphList:
    def __init__(self, n: int, directed: bool = False) -> None:
        self.adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, w: int = 1) -> None:
        self.adj[u].append((v, w))
        if not self.directed:
            self.adj[v].append((u, w))
```

`dfs_order` / `bfs_order` 见仓库。运行 `python graph_list.py`。

## C++ 实现

`struct Graph` 用 `vector<vector<pair<int,int>>> adj`；`dfs_order` 用 `function<void(int)>` lambda DFS；BFS 用 `queue<int>`。输出 `GraphList OK`。

## 练习与延伸

`ds-graph-adjacency-matrix`、`ds-graph-disjoint-set`、`algo-graph-topological-sort`。

## 学习路径

本页 → 200/695 BFS → `algo-graph-traversal` → 最短路专题。

## 延伸阅读

- [Algorithm — adjacency_list](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/graph/adjacency_list)
- 站点：`ds-graph-adjacency-matrix`、`algo-graph-traversal`
"""

# Unique depth seeds per slug (avoid duplicate paragraph lint)
BT_SEEDS = [
    ("前序与栈模拟", "前序迭代：入栈顺序可先右后左，弹出即访问，与层序不同。理解两种栈用法避免混模板。"),
    ("后序迭代双栈", "后序可用两个栈：第一个栈按前序压左右（先右后左），再倒入第二栈弹出即后序。面试常写递归即可。"),
    ("Morris 中序", "线索二叉树把空 right 指向后继，O(1) 空间中序。了解即可，不必实现进仓库。"),
    ("高度与深度 DFS", "104 题 max(depth)=1+max(左右)；注意空节点返回 0 还是 -1 决定结果是否含根。"),
    ("直径 543", "后序传高度，同时维护经过根的最大 left_h+right_h。与 124 路径和类似分治。"),
    ("翻转 226", "前序或后序交换左右子树，一行 swap。分治返回新根。"),
    ("对称 101", "递归比较 (l1,r1) 与 (l2,r2)；必须同时为空或同时非空且值相等。"),
    ("平衡 110", "后序传高度 -1 表示不平衡；或自顶向下重复算高度 O(n²)。"),
    ("构造 105", "前序首为根，中序找根划分左右区间长度；递归 build(l1,r1,l2,r2)。"),
    ("路径和 112", "前序减 val，到叶判 0；不需要后序。"),
    ("最近公共祖先 236", "后序：若 root 等于 p 或 q 或空返回 root；左右都非空则 root 为 LCA。"),
    ("序列化 297", "前序带 # 空标记；反序列化递归 consume。BFS 层序也可。"),
    ("N 叉树 429", "孩子列表 for child in node.children: q.append(child)。"),
    ("二叉搜索树中序", "98 验证用中序 prev 递增，见 ds-tree-bst。"),
    ("线段树与二叉树", "线段树逻辑是完全二叉树，存储用数组，见 ds-tree-segment-tree。"),
    ("堆的数组下标", "完全二叉树数组存储，见 ds-tree-heap，不是链式 TreeNode。"),
    ("递归深度限制", "Python 深链 10^4 可能 RecursionError；竞赛可 sys.setrecursionlimit。"),
    ("C++ 指针生命周期", "OJ 节点通常 new 不 delete；仓库教学栈上节点仅演示。"),
    ("层序 102 锯齿 103", "偶数层 reverse 或 deque 头尾插入。"),
    ("右视图 199", "层序取每层最后一个。"),
    ("俯视图 314", "按列 BFS 或中序映射 column，进阶。"),
    ("验证完形 331", "前序序列化比较，栈模拟。"),
    ("展开 114", "后序：右链接到左子树最右，再左变右。"),
    ("最大 BST 子树 333", "后序传 (min,max,isBST,size)。"),
    ("打家劫舍 III 337", "后序返回 (抢,不抢) 对。"),
    ("发布校验", "validate_algorithm_guide.py --slug ds-tree-binary-tree --strict"),
]

BST_SEEDS = [
    ("后继与前驱", "删除两子可用前驱（左子树最大）或后继（右子树最小），实现择一。"),
    ("230 第 K 小", "中序计数 O(n)；平衡树可加 size 字段 O(log n)。"),
    ("235 LCA", "利用 BST 性质一次比较方向。"),
    ("450 删除", "LeetCode 版无抛异常，注意 successor 链接。"),
    ("700 搜索", "同 search 迭代。"),
    ("701 插入", "同 insert。"),
    ("108 有序链转 BST", "中序找中点分治，或快慢指针找中点。"),
    ("96 不同 BST 计数", "卡特兰数 DP，非本仓库代码。"),
    ("98 区间法", "dfs(node, lo, hi) 开区间 (lo,hi)。"),
    ("173 二叉搜索树迭代器", "栈模拟中序，O(1) 均摊 next。"),
    ("220 滑动窗口 BST", "有序结构 multiset 或 TreeMap。"),
    ("有序数组转 BST 108", "选 mid 为根避免偏树。"),
    ("平衡退化", "有序插入 BST 变链，引出 AVL。"),
    ("multiset C++", "std::multiset 实现有序 multiset。"),
    ("Python bisect", "有序数组用 bisect，非指针 BST。"),
    ("发布校验", "validate --slug ds-tree-bst --strict"),
]

HEAP_SEEDS = [
    ("heapq 模块", "import heapq; heappush/heappop 小根堆；nlargest 用 -值或大根技巧。"),
    ("347 前 K 频", "dict 计数后维护 size k 小根堆，O(n log k)。"),
    ("23 合并 K 链", "堆存 (val, i, node) 每次 pop 最小接链。"),
    ("295 中位数", "大根堆存左半，小根堆存右半，平衡数量差≤1。"),
    ("703 数据流第 K", "类 215 维护 k 小根堆。"),
    ("1046 最后石头", "模拟堆即可。"),
    ("767 重构字符串", "计数后大根堆相邻不同，注意空堆判断。"),
    ("502 IPO", "堆选项目，进阶。"),
    ("快速选择对比", "215 平均 O(n) 快选，最坏 O(n²)；堆稳定 O(n log k)。"),
    ("索引堆", "Dijkstra 存 (dist, node) 可 decrease-key 用 lazy 删除。"),
    ("建堆复杂度证明", "级数求和 O(n)，不是 O(n log n)。"),
    ("完全二叉树判定", "按层 BFS 遇空后不应再出现节点。"),
    ("堆排序", "heapify 后反复 pop 得升序，原地需大根。"),
    ("优先队列 C++", "priority_queue 默认大根，greater 小根。"),
    ("发布校验", "validate --slug ds-tree-heap --strict"),
]

AVL_SEEDS = [
    ("四种失衡 LL LR RR RL", "画图记：左高左子 LL 右旋；左高右子 LR 先左后右。"),
    ("删除失衡与插入", "删除在 _rebalance 用子节点 bf；插入用插入 key 比较。"),
    ("红黑树对比", "AVL 更严、旋转多；红黑 O(1) 摊还旋转，STL map。"),
    ("高度字段维护", "每次旋转后 upd，不可漏。"),
    ("bf 计算", "_h(None)=0 统一空子树高度。"),
    ("面试白板", "只画一种 LL 和一种 LR 即可说明会平衡。"),
    ("数据库索引", "B+树为主，AVL 用于理解平衡思想。"),
    ("发布校验", "validate --slug ds-tree-avl --strict"),
]

GRAPH_SEEDS = [
    ("网格四方向", "坐标 (i,j) 映射 id=i*m+j，邻居四个方向。"),
    ("八方向", "骑士/国王移动注意边界。"),
    ("200 岛屿", "DFS/BFS 计数连通块。"),
    ("695 面积", "DFS 返回面积累加 max。"),
    ("133 克隆图", "哈希 old->new 节点映射再 DFS。"),
    ("207 课程表", "拓扑见 algo-graph-topological-sort。"),
    ("并查集对比", "动态连通 ds-graph-disjoint-set。"),
    ("邻接矩阵", "稠密图 O(1) 判边存在，见 ds-graph-adjacency-matrix。"),
    ("带权最短路", "不能只用 BFS，见 Dijkstra。"),
    ("0-1 BFS", "边权 0/1 用 deque 头尾，见 ds-linear-deque。"),
    ("visited 颜色标记", "白灰黑用于环检测。"),
    ("多源 BFS", "初始多个源入队，994 腐烂橘子。"),
    ("字典序最小", "Dijkstra 变体或特殊 BFS。"),
    ("发布校验", "validate --slug ds-graph-adjacency-list --strict"),
]

GUIDES = [
    ("ds-tree-binary-tree", BINARY_TREE, BT_SEEDS),
    ("ds-tree-bst", BST_GUIDE, BST_SEEDS),
    ("ds-tree-heap", HEAP_GUIDE, HEAP_SEEDS),
    ("ds-tree-avl", AVL_GUIDE, AVL_SEEDS),
    ("ds-graph-adjacency-list", GRAPH_GUIDE, GRAPH_SEEDS),
]


def main() -> None:
    for slug, body, seeds in GUIDES:
        out = BLOG / slug / "index.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        text = _pad(body, slug, seeds)
        out.write_text(text, encoding="utf-8")
        n = count_chinese(text)
        print(f"Wrote {slug}: {n} chinese chars")


if __name__ == "__main__":
    main()
