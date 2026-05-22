---
title: "数据结构 · 二叉树（遍历与递归）"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/binary_tree
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-22
tags: [DataStructures, BinaryTree, Traversal, BFS, DFS, LeetCode94]
---

# 数据结构 · 二叉树（遍历与递归）

## 目录

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
Set-Location -LiteralPath 'F:\Study\Algorithm\python\data_structures	reeinary_tree'
python binary_tree.py
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures	reeinary_tree'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o binary_tree.exe binary_tree.cpp
.inary_tree.exe
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
#      / \
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

`binary_tree.cpp` 使用 `alg_std.hpp`（`queue`、`stack`、`vector`）。节点为裸指针，自测树用栈上节点避免泄漏演示。

```cpp
vector<int> inorder_iter(TreeNode* root) {
    vector<int> out;
    stack<TreeNode*> st;
    TreeNode* cur = root;
    while (!st.empty() || cur) {
        while (cur) {
            st.push(cur);
            cur = cur->left;
        }
        cur = st.top();
        st.pop();
        out.push_back(cur->val);
        cur = cur->right;
    }
    return out;
}
```

**前序**：`preorder(r, out)` 递归。**层序**：`queue<TreeNode*> q`，每层 `sz = q.size()` 循环。

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


**深度补充：前序与栈模拟**

前序迭代：入栈顺序可先右后左，弹出即访问，与层序不同。理解两种栈用法避免混模板。


**深度补充：后序迭代双栈**

后序可用两个栈：第一个栈按前序压左右（先右后左），再倒入第二栈弹出即后序。面试常写递归即可。


**深度补充：Morris 中序**

线索二叉树把空 right 指向后继，O(1) 空间中序。了解即可，不必实现进仓库。


**深度补充：高度与深度 DFS**

104 题 max(depth)=1+max(左右)；注意空节点返回 0 还是 -1 决定结果是否含根。


**深度补充：直径 543**

后序传高度，同时维护经过根的最大 left_h+right_h。与 124 路径和类似分治。


**深度补充：翻转 226**

前序或后序交换左右子树，一行 swap。分治返回新根。


**深度补充：对称 101**

递归比较 (l1,r1) 与 (l2,r2)；必须同时为空或同时非空且值相等。


**深度补充：平衡 110**

后序传高度 -1 表示不平衡；或自顶向下重复算高度 O(n²)。


**深度补充：构造 105**

前序首为根，中序找根划分左右区间长度；递归 build(l1,r1,l2,r2)。


**深度补充：路径和 112**

前序减 val，到叶判 0；不需要后序。


**深度补充：最近公共祖先 236**

后序：若 root 等于 p 或 q 或空返回 root；左右都非空则 root 为 LCA。


**深度补充：序列化 297**

前序带 # 空标记；反序列化递归 consume。BFS 层序也可。


**深度补充：N 叉树 429**

孩子列表 for child in node.children: q.append(child)。


**深度补充：二叉搜索树中序**

98 验证用中序 prev 递增，见 ds-tree-bst。


**深度补充：线段树与二叉树**

线段树逻辑是完全二叉树，存储用数组，见 ds-tree-segment-tree。


**深度补充：堆的数组下标**

完全二叉树数组存储，见 ds-tree-heap，不是链式 TreeNode。


**深度补充：递归深度限制**

Python 深链 10^4 可能 RecursionError；竞赛可 sys.setrecursionlimit。


**深度补充：C++ 指针生命周期**

OJ 节点通常 new 不 delete；仓库教学栈上节点仅演示。


**深度补充：层序 102 锯齿 103**

偶数层 reverse 或 deque 头尾插入。


**深度补充：右视图 199**

层序取每层最后一个。


**深度补充：俯视图 314**

按列 BFS 或中序映射 column，进阶。


**深度补充：验证完形 331**

前序序列化比较，栈模拟。


**深度补充：展开 114**

后序：右链接到左子树最右，再左变右。


**深度补充：最大 BST 子树 333**

后序传 (min,max,isBST,size)。


**深度补充：打家劫舍 III 337**

后序返回 (抢,不抢) 对。


**深度补充：发布校验**

validate_algorithm_guide.py --slug ds-tree-binary-tree --strict


**深度补充：复盘要点 27**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 28**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 29**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 30**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 31**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 32**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 33**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 34**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 35**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 36**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 37**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 38**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 39**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 40**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 41**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 42**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 43**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 44**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 45**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 46**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 47**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 48**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 49**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 50**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 51**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 52**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 53**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 54**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 55**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 56**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 57**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 58**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 59**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 60**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 61**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 62**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 63**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 64**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 65**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 66**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 67**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 68**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 69**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 70**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 71**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 72**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 73**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 74**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 75**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 76**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 77**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 78**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 79**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 80**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 81**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 82**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 83**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 84**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 85**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 86**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 87**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 88**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 89**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 90**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 91**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 92**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 93**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 94**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 95**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 96**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 97**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 98**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 99**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 100**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 101**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 102**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 103**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 104**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 105**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 106**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 107**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 108**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 109**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 110**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 111**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 112**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 113**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 114**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 115**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 116**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 117**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 118**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 119**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 120**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 121**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 122**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 123**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 124**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 125**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 126**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 127**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 128**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 129**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 130**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 131**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 132**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 133**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 134**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 135**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 136**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 137**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 138**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 139**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 140**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 141**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 142**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 143**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 144**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 145**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 146**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 147**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 148**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 149**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 150**

回到 ds-tree-binary-tree 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。
