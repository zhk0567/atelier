<!-- wiki_page_id: page-4 -->

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [cpp/data_structures/tree/binary_tree/binary_tree.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/data_structures/tree/binary_tree/binary_tree.cpp)
- [cpp/data_structures/tree/bst/bst.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/data_structures/tree/bst/bst.cpp)
- [cpp/data_structures/tree/avl/avl.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/data_structures/tree/avl/avl.cpp)
- [cpp/data_structures/tree/red_black_tree/red_black_tree.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/data_structures/tree/red_black_tree/red_black_tree.cpp)
- [cpp/data_structures/tree/heap/heap.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/data_structures/tree/heap/heap.cpp)
- [cpp/data_structures/tree/trie/trie.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/data_structures/tree/trie/trie.cpp)
- [cpp/data_structures/tree/segment_tree/segment_tree.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/data_structures/tree/segment_tree/segment_tree.cpp)
- [cpp/data_structures/tree/fenwick_tree/fenwick_tree.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/data_structures/tree/fenwick_tree/fenwick_tree.cpp)
</details>

# 树形数据结构

## 概述

树形数据结构是一种层次化的数据组织方式，由节点和边组成，其中每个节点可以有零个或多个子节点。树形结构在计算机科学中有广泛应用，如文件系统、数据库索引、编译器语法分析等。本文档介绍了项目中实现的各种树形数据结构及其特性。

## 二叉树 (Binary Tree)

### 基本概念

二叉树是每个节点最多有两个子节点的树形结构，通常称为左子节点和右子节点。

### 实现细节

根据 `binary_tree.cpp` 文件，二叉树的节点结构定义如下：

```cpp
struct Node {
    int data;
    Node* left;
    Node* right;
    Node(int val) : data(val), left(nullptr), right(nullptr) {}
};
```

主要操作包括：
- 插入节点
- 前序、中序、后序遍历
- 层序遍历
- 计算树的高度
- 判断是否为平衡二叉树

### 时间复杂度

| 操作 | 平均情况 | 最坏情况 |
|------|----------|----------|
| 插入 | O(h) | O(n) |
| 查找 | O(h) | O(n) |
| 删除 | O(h) | O(n) |
| 遍历 | O(n) | O(n) |

其中 h 为树的高度，n 为节点数。

## 二叉搜索树 (BST)

### 基本概念

二叉搜索树是一种特殊的二叉树，满足以下性质：
- 左子树上所有节点的值均小于根节点的值
- 右子树上所有节点的值均大于根节点的值
- 左右子树也分别为二叉搜索树

### 实现细节

根据 `bst.cpp` 文件，BST 的实现包括：
- 节点插入（保持 BST 性质）
- 节点查找
- 节点删除（考虑三种情况：叶子节点、单子节点、双子节点）
- 前序、中序、后序遍历
- 查找最小值和最大值
- 前驱和后继查找

### 时间复杂度

| 操作 | 平均情况 | 最坏情况 |
|------|----------|----------|
| 插入 | O(log n) | O(n) |
| 查找 | O(log n) | O(n) |
| 删除 | O(log n) | O(n) |
| 前驱/后继 | O(log n) | O(n) |

注：当 BST 退化为链表时（如按顺序插入），性能降至 O(n)。

## AVL 树

### 基本概念

AVL 树是一种自平衡二叉搜索树，其中任何节点的两个子树的高度差的绝对值不超过 1。

### 实现细节

根据 `avl.cpp` 文件，AVL 树的实现包括：
- 节点结构包含高度信息
- 插入后通过旋转操作维持平衡
- 删除后同样通过旋转维持平衡
- 四种旋转情况：左左（LL）、右右（RR）、左右（LR）、右左（RL）

### 平衡因子和平衡条件

平衡因子 = 左子树高度 - 右子树高度
AVL 树要求：|平衡因子| ≤ 1

### 时间复杂度

| 操作 | 时间复杂度 |
|------|------------|
| 插入 | O(log n) |
| 查找 | O(log n) |
| 删除 | O(log n) |
| 遍历 | O(n) |

由于始终保持平衡，AVL 树保证了 O(log n) 的时间复杂度。

## 红黑树 (Red-Black Tree)

### 基本概念

红黑树是一种自平衡二叉搜索树，通过在每个节点上增加颜色属性（红色或黑色）来确保树在插入和删除过程中保持近似平衡。

### 实现细节

根据 `red_black_tree.cpp` 文件，红黑树满足以下性质：
1. 每个节点要么是红色，要么是黑色
2. 根节点是黑色
3. 所有叶子节点（NIL）是黑色
4. 每个红色节点的两个子节点一定是黑色
5. 从任意节点到其每个叶子的所有简单路径都包含相同数量的黑色节点

### 实现操作

- 插入：通过颜色翻转和旋转恢复红黑性质
- 删除：通过颜色调整和旋转恢复红黑性质
- 查找：标准 BST 查找
- 遍历：前序、中序、后序遍历

### 时间复杂度

| 操作 | 时间复杂度 |
|------|------------|
| 插入 | O(log n) |
| 查找 | O(log n) |
| 删除 | O(log n) |
| 遍历 | O(n) |

红黑树提供了良好的均摊性能，在实际应用中广泛使用（如 C++ STL 的 map 和 set）。

## 堆 (Heap)

### 基本概念

堆是一种特殊的完全二叉树，满堆性质：父节点的值总是不大于（或不小于）其子节点的值。

### 实现细节

根据 `heap.cpp` 文件，实现了最大堆（Max Heap）：
- 使用数组存储，父子节点关系：父节点 i 的左子节点为 2i+1，右子节点为 2i+2
- 堆化操作（Heapify）：维持堆性质
- 插入操作：将元素添加到末尾并上浮
- 删除操作：移除根节点，将最后元素移到根位置并下沉
- 建堆操作：从最后一个非叶子节点开始上堆化

### 时间复杂度

| 操作 | 时间复杂度 |
|------|------------|
| 插入 | O(log n) |
| 删除最大值 | O(log n) |
| 查看最大值 | O(1) |
| 建堆 | O(n) |
| 堆排序 | O(n log n) |

## 字典树 (Trie)

### 基本概念

字典树（Trie），也称为前缀树，是一种用于高效检索多个字符串中 key 的树形数据结构。

### 实现细节

根据 `trie.cpp` 文件，Trie 的特点：
- 每个节点代表一个字符
- 从根到某个节点的路径代表一个字符串的前缀
- 节点包含子节点指针数组和是否为单词结束的标记
- 支持插入、查找和前缀匹配操作

### 实现操作

- 插入：逐字符遍历，必要时创建新节点
- 查找：逐字符匹配，检查结束标记
- 前缀查询：检查是否存在以给定前缀开头的单词
- 删除：标记节点非结束状态，必要时回收节点

### 时间复杂度

| 操作 | 时间复杂度 |
|------|------------|
| 插入 | O(L) |
| 查找 | O(L) |
| 前缀查询 | O(L) |
| 删除 | O(L) |

其中 L 为字符串长度。Trie 在处理大量字符串的前缀查询时效率很高。

## 线段树 (Segment Tree)

### 基本概念

线段树是一种用于存储区间或段的树形数据结构，支持高效的区间查询和修改操作。

### 实现细节

根据 `segment_tree.cpp` 文件，线段树的特点：
- 每个节点代表一个区间
- 叶子节点代表单个元素
- 内部节点代表其子节点区间的并
- 支持区间求和、区间最值等查询
- 支持单点更新和区间更新

### 实现操作

- 建树：递归构建，叶子节点为原始数组元素
- 区间查询：递归查询相交区间
- 单点更新：递归更新受影响的节点
- 区间更新：通过懒惰传播优化（如果实现了）

### 时间复杂度

| 操作 | 时间复杂度 |
|------|------------|
| 建树 | O(n) |
| 区间查询 | O(log n) |
| 单点更新 | O(log n) |
| 区间更新 | O(log n) |

线段树在处理动态区间查询问题时非常有用。

## 树状数组 (Fenwick Tree / Binary Indexed Tree)

### 基本概念

树状数组（Fenwick Tree）是一种用于高效计算前缀和的数据结构，支持点更新和前缀和查询。

### 实现细节

根据 `fenwick_tree.cpp` 文件，树状数组的特点：
- 使用数组存储，但语义不同于普通数组
- 每个位置存储一定范围内的和
- 通过低bit操作定位父节点和子节点
- 支持前缀和查询和点更新

### 实现操作

- 初始化：根据原始数组构建
- 前缀和查询：从索引 i 开始，不断去掉最后一个1bit
- 点更新：从索引 i 开始，不断加上最后一个1bit
- 区间和查询：利用前缀和的差求得

### 时间复杂度

| 操作 | 时间复杂度 |
|------|------------|
| 初始化 | O(n log n) |
| 前缀和查询 | O(log n) |
| 点更新 | O(log n) |
| 区间和查询 | O(log n) |

树状数组相比线段树实现更简单，空间占用更小，但在功能上略有限制（主要用于和的查询）。

## 各树形结构对比

| 数据结构 | 平衡性 | 查找效率 | 插入/删除效率 | 特殊功能 | 空间复杂度 |
|----------|--------|----------|---------------|----------|------------|
| 二叉树 | 无保证 | O(n) | O(n) | 基础树操作 | O(n) |
| 二叉搜索树 | 无保证 | O(n) | O(n) | 有序性 | O(n) |
| AVL 树 | 平衡 | O(log n) | O(log n) | 自平衡 | O(n) |
| 红黑树 | 准平衡 | O(log n) | O(log n) | 自平衡 | O(n) |
| 堆 | 完全二叉树 | O(n) | O(log n) | 优先队列 | O(n) |
| 字典树 | 无 | O(L) | O(L) | 前缀匹配 | O(ALPHABET_SIZE * N * L) |
| 线段树 | 平衡 | O(log n) | O(log n) | 区间查询 | O(4n) |
| 树状数组 | 平衡 | O(log n) | O(log n) | 前缀和 | O(n) |

## 应用场景

### 二叉树
- 表达式求值
- 语法树
- 决策树

### 二叉搜索树
- 动态集合操作
- 符号表
- 多路查找的基础

### AVL 树
- 需要严格平衡的场景
- 频繁查询且更新不频繁的情况

### 红黑树
- 通用平衡树需求
- STL 的 map/set 实现
- 高频插入删除且需要有序性的场景

### 堆
- 优先队列
- 堆排序
- 图算法（Dijkstra、Prim）

### 字典树
- 自动补全
- 拼写检查
- IP 路由表
- 字符串统计

### 线段树
- 区间求和/最值/计数
- 动态区间修改查询
- 计算几何中的区间问题

### 树状数组
- 前缀和查询与点更新
- 树状数组逆序对
- 离散化后的频率统计

## 实现注意事项

1. **内存管理**：所有基于指针的树形结构需要注意内存释放，防止内存泄漏
2. **边界条件**：空树、单节点树、重复值处理需要特别注意
3. **递归深度**：对于非常深的树，递归实现可能导致栈溢出，可考虑迭代实现
4. **性能权衡**：不同结构在时间和空间上有不同特点，应根据具体场景选择
5. **线程安全**：当前实现均为非线程安全，多线程使用需要额外同步措施

## 参考实现

所有树形数据结构的实现均位于 `cpp/data_structures/tree/` 目录下，每种结构有独立的.cpp文件，包含完整的类定义和方法实现。实现遵循现代 C++ 规范，使用了适当的封装和错误处理。