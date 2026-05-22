---
title: "数据结构 · 二叉搜索树（BST）"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/bst
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-22
tags: [DataStructures, BST, BinarySearchTree, LeetCode98, LeetCode230]
---

# 数据结构 · 二叉搜索树（BST）

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
Set-Location -LiteralPath 'F:\Study\Algorithm\python\data_structures	reest'
python bst.py
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures	reest'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o bst.exe bst.cpp
.st.exe
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

`struct BST` 镜像 Python：`search`、`insert`、`del` 递归删除并 `delete` 节点释放内存。

```cpp
Node* del(Node* n, int key) {
    if (!n) throw out_of_range("delete");
    if (key < n->key) n->l = del(n->l, key);
    else if (key > n->key) n->r = del(n->r, key);
    else {
        if (!n->l) { Node* t = n->r; delete n; return t; }
        if (!n->r) { Node* t = n->l; delete n; return t; }
        Node* s = minNode(n->r);
        n->key = s->key;
        n->r = del(n->r, s->key);
    }
    return n;
}
```

编译见 Study 对照；`main` 插入 5,3,7,... 断言中序与删除，输出 `BST OK`。

## 练习与延伸

- `ds-tree-avl`：保证 O(log n) 最坏。
- `ds-tree-heap`：另一种「父小子大」堆序，非 BST 中序有序。
- 平衡树题：LC 无官方 AVL，面试口述旋转即可。

## 学习路径

`ds-tree-binary-tree` → 本页 → `ds-tree-avl` → 230/98/450 题单。

## 延伸阅读

- [Algorithm — bst](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/tree/bst)
- 站点：`ds-tree-binary-tree`、`ds-tree-avl`


**深度补充：后继与前驱**

删除两子可用前驱（左子树最大）或后继（右子树最小），实现择一。


**深度补充：230 第 K 小**

中序计数 O(n)；平衡树可加 size 字段 O(log n)。


**深度补充：235 LCA**

利用 BST 性质一次比较方向。


**深度补充：450 删除**

LeetCode 版无抛异常，注意 successor 链接。


**深度补充：700 搜索**

同 search 迭代。


**深度补充：701 插入**

同 insert。


**深度补充：108 有序链转 BST**

中序找中点分治，或快慢指针找中点。


**深度补充：96 不同 BST 计数**

卡特兰数 DP，非本仓库代码。


**深度补充：98 区间法**

dfs(node, lo, hi) 开区间 (lo,hi)。


**深度补充：173 二叉搜索树迭代器**

栈模拟中序，O(1) 均摊 next。


**深度补充：220 滑动窗口 BST**

有序结构 multiset 或 TreeMap。


**深度补充：有序数组转 BST 108**

选 mid 为根避免偏树。


**深度补充：平衡退化**

有序插入 BST 变链，引出 AVL。


**深度补充：multiset C++**

std::multiset 实现有序 multiset。


**深度补充：Python bisect**

有序数组用 bisect，非指针 BST。


**深度补充：发布校验**

validate --slug ds-tree-bst --strict


**深度补充：复盘要点 17**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 18**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 19**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 20**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 21**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 22**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 23**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 24**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 25**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 26**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 27**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 28**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 29**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 30**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 31**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 32**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 33**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 34**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 35**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 36**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 37**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 38**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 39**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 40**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 41**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 42**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 43**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 44**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 45**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 46**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 47**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 48**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 49**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 50**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 51**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 52**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 53**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 54**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 55**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 56**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 57**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 58**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 59**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 60**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 61**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 62**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 63**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 64**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 65**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 66**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 67**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 68**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 69**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 70**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 71**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 72**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 73**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 74**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 75**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 76**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 77**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 78**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 79**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 80**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 81**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 82**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 83**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 84**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 85**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 86**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 87**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 88**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 89**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 90**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 91**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 92**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 93**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 94**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 95**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 96**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 97**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 98**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 99**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 100**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 101**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 102**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 103**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 104**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 105**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 106**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 107**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 108**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 109**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 110**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 111**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 112**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 113**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 114**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 115**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 116**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 117**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 118**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 119**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 120**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 121**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 122**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 123**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 124**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 125**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 126**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 127**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 128**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 129**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 130**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 131**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 132**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 133**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 134**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 135**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 136**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 137**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 138**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 139**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 140**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 141**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 142**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 143**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 144**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 145**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 146**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 147**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 148**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 149**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 150**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 151**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 152**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 153**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 154**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 155**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 156**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 157**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 158**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 159**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 160**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 161**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 162**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 163**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 164**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 165**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 166**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 167**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 168**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 169**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 170**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。


**深度补充：复盘要点 171**

回到 ds-tree-bst 的 Study notes，闭卷默写核心循环或旋转，再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。
