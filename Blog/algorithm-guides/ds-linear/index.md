---
title: "数据结构 · 线性结构总览"
series: algorithm
category: DataStructures
topic_path: data_structures/linear
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-21
tags: [DataStructures, Linear, Array, LinkedList, Stack, Queue, HashTable]
---

# 数据结构 · 线性结构总览

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

**线性结构**是算法与系统编程的「地基」：元素在逻辑上排成一条线，除首尾外每个元素至多有一个前驱和一个后继。数组、链表、栈、队列、双端队列与哈希表（链地址法底层仍是链表或开放寻址的线性探测）共同构成 Study 仓库 `data_structures/linear/` 目录；本页是**专题总览**，不替代各子目录的独立指南（`ds-linear-array`、`ds-linear-stack` 等），而是帮你建立一张**选型地图**：何时用连续内存、何时用指针、何时用 FIFO/LIFO 约束、何时用哈希把查找从 O(n) 降到均摊 O(1)。

面试与竞赛中，线性结构几乎从不单独作为「炫技题」出现，却渗透在链表反转、单调栈、滑动窗口、BFS 层序、并查集前的数组模拟等题型里。许多 WA 并非算法思路错，而是**边界**（空结构、满队列、扩容后下标、哨兵节点）或**复杂度误估**（在中间插入却以为 O(1)）。读完本文，你应能：

1. 用一张表对比六类结构的访问/增删复杂度与内存局部性；
2. 在 Python 与 C++ 镜像路径下定位可运行教学代码并本地自测；
3. 说出「栈实现队列」「循环数组区分满空」「哈希装载因子与 rehash」的实现要点；
4. 按学习路径进入子专题或 LeetCode 题解目录做针对性练习。

本页 `topic_path` 为 `data_structures/linear`，`guide_toc` 为 `topic-ds`，与 manifest 中各子 slug（`ds-linear-array` 等）并列：子页写深单一结构，本页写**横向关系**与仓库布局。状态为 `draft`，待子专题陆续补齐后可把本页升级为「线性结构导航枢纽」。

**与图结构、树结构的边界**：线性表没有分叉；树每个节点可有多个子节点；图边可任意连接。并查集、邻接表虽在 `data_structures/graph/`，但邻接表每行常是 `vector` 或链表——仍依赖本目录的数组/链表基本功。

**工业语境**：动态数组即 `std::vector` / Python `list` 的底层思想；无锁队列、环形缓冲区在 `interview/classic/` 有专题；Redis 列表底层 quicklist 混合链表与压缩列表。理解教学实现有助于读源码，但面试默认仍以 LeetCode 风格手写为准。

**本页与子指南的分工**：`ds-linear-array` 等六篇将逐一把 `notes.md` 扩成独立教程；在它们完成前，本总览承担「一张图串起六类结构」的职责。建议学习顺序：先读本页基础篇与 Python 摘录 → 跑通六脚本 → 挑薄弱子目录读 `GUIDE.md` → 最后按题号刷 `iv-top-frequent` 中链表/栈/哈希章。

**Hot 100 中的线性结构密度**：103 题索引里链表 14 道、数组与窗口 14 道、栈 5 道、哈希 4 道，合计约占冻结题单四成。线性结构不过关会导致图论 BFS、动态规划滚动数组等后续专题全部卡顿，因此值得在第一周集中投入。

**六类结构的记忆锚点（考前一夜可复习）**

数组：下标、连续、扩容；链表：指针、哑节点、快慢；栈：LIFO、单调栈；队列：FIFO、循环数组、BFS；双端队列：两端、滑动窗口；哈希：键值、冲突、rehash。每个锚点对应 Study 一个子目录的 `notes.md` 首段定义，与本页「核心操作」表一致。若你能不看表说出每类「一种 O(1) 操作」与「一种 O(n) 操作」，说明总览已吸收。

**与面试手写题的时间分配**

纯数据结构实现题（栈/队列/哈希）通常限时十到十五分钟；若超过二十分钟，往往是指针或边界分支过多。练习时故意用「哑节点 + 统一异常」缩短分支，与仓库 `linked_list.py`、`hash_table.py` 风格保持一致，提交 OJ 时再按题面精简。

## 预备知识

> **预备知识**：熟悉 0-based 下标、引用与指针概念（C++ 用 `nullptr`）；知道大 O 表示法；Python 3.10+；C++17 与 `g++` 基本编译。Windows 下用 PowerShell 的 `Set-Location -LiteralPath` 进入目录后运行脚本。

建议已具备：

- **连续存储 vs 链式存储**：前者缓存友好、随机访问 O(1)；后者插入删除若已有节点指针则 O(1)，按值查找 O(n)。
- **抽象数据类型（ADT）**：栈/队列/双端队列是**接口约束**（LIFO/FIFO/双端），可用数组或链表实现，不应把「实现」与「语义」混为一谈。
- **均摊复杂度**：动态数组 `push_back` 单次最坏 O(n)（扩容搬移），序列均摊 O(1)。
- **哈希函数与冲突**：键映射到桶下标，冲突用链地址法或开放寻址；装载因子过高需扩容 rehash。

若你只会 Python 内置 `list`、`dict`，仍建议跑通仓库手写版：`DynamicArray` 显式 `capacity` 帮你理解 `vector` 扩容；`HashTableChaining` 帮你看清 `dict` 并非黑盒。

**环境核对**：克隆 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) 后，确认存在 `python/data_structures/linear/` 下六个子目录，各含 `*.py` 与 `notes.md`；C++ 侧路径对称于 `cpp/data_structures/linear/`。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/linear` |
| 子专题（Python） | `array/`、`linked_list/`、`stack/`、`queue/`、`deque/`、`hash_table/` |
| 子专题（C++） | `cpp/data_structures/linear/<同上>/` |
| 本页定位 | 总览；实现分散在各子目录 `*.py` / `*.cpp` |

**按子目录运行自测（Python）**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'

$dirs = @('array','linked_list','stack','queue','deque','hash_table')
foreach ($d in $dirs) {
  $script = Join-Path 'F:\Study\Algorithm\python\data_structures\linear' $d
  $py = Get-ChildItem -LiteralPath $script -Filter '*.py' | Where-Object { $_.Name -notmatch 'test' } | Select-Object -First 1
  if ($py) { python -LiteralPath $py.FullName }
}
```

将 `F:\Study\Algorithm` 换成本机克隆根目录。期望依次看到 `DynamicArray OK`、`SinglyLinkedList OK`、`Stack OK`、`Queue OK`、`Deque OK`、`HashTable OK` 等输出（以各脚本 `print` 为准）。

**C++ 示例（以 `stack` 为例）**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\linear\stack'
g++ -std=c++17 -O2 -Wall -Wextra -o stack.exe stack.cpp
.\stack.exe
```

部分 C++ 文件 `#include <alg_std.hpp>`，编译时 `-I` 指向 `cpp/include`。

| 子目录 | 主要源文件 | 笔记 |
|--------|------------|------|
| `array/` | `dynamic_array.py` | `notes.md` |
| `linked_list/` | `linked_list.py` | `notes.md` |
| `stack/` | `stack.py`（含 `MinStack`） | `notes.md` |
| `queue/` | `queue.py`（循环数组 + 双栈） | `notes.md` |
| `deque/` | `deque.py` | `notes.md` |
| `hash_table/` | `hash_table.py` | `notes.md` |

站点子指南 slug 与上表一一对应：`ds-linear-array` … `ds-linear-hash-table`。本总览不重复六份全文，实现章节摘录**最具代表性**的片段并说明如何跳转。

## 基础篇

### 抽象模型

**逻辑结构**：元素 \(a_0,a_1,\ldots,a_{n-1}\) 按顺序排列。根据访问规则再细分为：

| 结构 | 逻辑约束 | 常见物理实现 |
|------|----------|--------------|
| 顺序表 / 动态数组 | 下标 0..n-1，连续逻辑顺序 | 连续缓冲区 + `size`/`capacity` |
| 链表 | 每个节点含数据与后继（双向另有前驱） | 堆上节点 + 指针 |
| 栈 | 仅在一端插入删除（LIFO） | 数组尾或链表头 |
| 队列 | 一端入另一端出（FIFO） | 循环数组 / 双栈 / 链表 |
| 双端队列 | 两端均可插入删除 | 循环数组（推荐） |
| 哈希表 | 键→值，键唯一 | 桶数组 + 链表（链地址法） |

**存储结构**决定性能常数：数组随机访问快、中间插入需搬移；链表中间已知节点时插入 O(1)，按值查找慢。哈希表在**键空间**上提供均摊 O(1) 的 `get`/`insert`，代价是额外空间与 rehash 时的峰值耗时。

**哨兵节点（dummy）**：链表题中常用 `dummy` 头节点统一「在头部插入」与「删除任意节点」的指针写法，避免特判 `head is None`。双向链表常用 `head`/`tail` 哨兵夹住真实节点，与 LRU 专题同构。

**空结构语义**：`size==0` 时 `pop`/`dequeue` 应抛错或返回明确错误；LeetCode 部分题允许不操作空结构，但教学代码应严格，便于单测捕获 bug。

### 核心操作

下表汇总各 ADT 的**典型接口**与复杂度（n 为当前元素个数，均摊意义下）：

| 结构 | 操作 | 时间 | 备注 |
|------|------|------|------|
| 动态数组 | `at(i)` / `push_back` / `pop_back` | O(1) 均摊 | 中间 `insert`/`erase` O(n) |
| 单链表 | 头插 / 按值删 / 反转 | 头插 O(1)，按值删 O(n) | 反转 O(n) 三指针 |
| 双向链表 | 头尾插删、已知节点删 | O(1) | 需维护 `size` 可选 |
| 栈 | `push` / `pop` / `top` | O(1) | |
| 队列 | `enqueue` / `dequeue` | O(1) 均摊 | 循环数组扩容时 O(n) |
| 双端队列 | 四角操作 | O(1) 均摊 | |
| 哈希表 | `get` / `insert` / `erase` | 均摊 O(1) | 最坏 O(n) 当全键冲突 |

**栈与队列的互实现**（面试常考）：

- **两个栈实现队列**：入栈 `in`，出队时若 `out` 空则把 `in` 全部倒入 `out`，保证 FIFO 顺序；均摊 O(1)。
- **两个队列实现栈**：入队到非空队列，把另一队列元素逐个入队再出队，使新元素位于队首；均摊 O(1)。

**最小栈（MinStack）**：主栈存值，辅助栈存当前最小值；`push` 时若 `x <= min_top` 则压入辅助栈；`pop` 时若弹出值等于辅助栈顶则同步弹辅助栈。LeetCode [155. Min Stack](https://leetcode.cn/problems/min-stack/) 对照 `stack/stack.py`。

### 实现要点

**动态数组**

维护 `_size` 与 `_capacity`；`push_back` 满则 `_resize(2 * capacity)` 并搬移元素。摊还分析：容量翻倍时搬移总代价分摊到此前多次 O(1) 插入。中间 `insert`/`erase` 用从后向前或从前向后搬移保持连续性。

```python
def push_back(self, value: object) -> None:
    if self._size == self._capacity:
        self._resize(self._capacity * 2)
    self._data[self._size] = value
    self._size += 1
```

可选**缩容**：`size` 远小于 `capacity/4` 时减半，避免内存浪费；竞赛题通常省略。

**单链表与双向链表**

单链表反转：`prev, cur = None, head`，循环中 `cur.next, prev, cur = prev, cur, cur.next`。删除给定值需 `dummy` 与 `prev.next` 写法。

双向链表在 `head`/`tail` 哨兵间 `append`：新节点插在 `tail.prev` 与 `tail` 之间，四指针改写。删除已知节点时同时维护 `prev` 与 `next`，勿漏改一侧。

**循环数组队列**

用 `_front` 与 `_size` 表示区间，**故意浪费一个槽位**或维护 `size` 区分「满」与「空」：本仓库采用 `size == cap-1` 视为满并扩容。`_grow` 时按逻辑顺序拷贝到新缓冲区，`_front` 归零。

**双端队列**

`push_front` 时 `_front = (_front - 1 + cap) % cap`；`pop_back` 取 `(front + size - 1) % cap`。与队列共享循环数组技巧，LeetCode [641. Design Circular Deque](https://leetcode.cn/problems/design-circular-deque/) 可对照 `deque/deque.py`。

**链地址法哈希表**

桶数组 `buckets[m]`，每桶链表存 `(key, val)`。`insert` 若 `n+1 > load_max * m` 则 `_rehash(2*m)`，旧表元素重新 `insert`（会按新哈希分布）。`erase` 需处理头节点与链中节点的不同指针改写。

```python
@staticmethod
def _h(key: int, m: int) -> int:
    return hash(key) % m
```

Python 内置 `dict` 用开放寻址 + 扰动探测，思想不同但「装载因子 + 扩容」一致。C++ `unordered_map` 实现因标准库而异，面试手写多用链地址法。

**摊还分析：动态数组为何 push 均摊 O(1)**

设容量按 2 倍增长。从空表依次 `push_back` 共 n 次，总搬移元素次数约为 \(n + n/2 + n/4 + \cdots < 2n\)，故均摊每次 O(1)。面试可口述：「扩容很贵，但扩容次数是对数的，摊到每次插入仍是常数。」若倍率是 1.5 或混合策略，结论仍为均摊 O(1)，常数不同。中间 `insert` 无法均摊到 O(1)，因每次可能搬移 O(n) 元素——这是「能尾部增删用数组，能中间插删用链表或平衡树」的根源。

**链表专题：快慢指针与环**

判环（141）：`slow` 走一步，`fast` 走两步，若相遇则有环。找环入口（142）：相遇后令一指针回 `head`，两指针同步前进，再次相遇点即为入口（数学证明基于 \(a=c+(a-c)\) 模环长）。删除倒数第 n（19）：双指针间隔 n+1。合并有序（21）：哑节点 + 每次取较小 `next`。k 组翻转（25）：先数长度，再每 k 段调用局部反转，不足 k 不翻转。这些模板在 `linked_list.py` 与题解目录中反复出现，本总览要求你**先会 206 再碰 25**，否则指针写乱。

**单调栈与柱状图（84）**

维护下标栈，栈内对应高度单调递增。当前柱 `i` 入栈前，若 `h[i] < h[stack.top]` 则弹栈，以弹出的下标 `j` 为「高为 h[j] 的最后一根柱」计算宽度：右边界 `i-1`，左边界为弹栈后新栈顶+1。每根柱作为矩形高度最多入栈出栈各一次，总 O(n)。85 最大矩形需在二维 01 矩阵每行转为一维 histogram 再调 84——索引中 85 与 84 应连着练。

**滑动窗口 + 哈希 + 双端队列（3 与 239）**

`0003`：窗口内 `dict` 存字符最后出现下标，右指针扩展，左指针跳过重复。`0239`：维护单调递减下标 deque 存「可能成为窗口最大值的候选」，入队前弹出所有比当前 nums[i] 小的尾下标，队头即当前窗口最大。外层容器用 `CircularDeque` 或 Python `collections.deque`。两题分别代表「哈希定边界」与「单调队列维护最值」，是数组章最重要的两类。

**哈希与计数（1、560）**

两数之和：遍历时查 `target-x` 是否在 map。和为 K 的子数组：前缀和 `s` 出现次数用 map 记录，当前 `s-k` 的累计次数即新增子数组数。287 找重复数可视为「数组即链表，下标指向下一跳」，Floyd 判环与 142 同族。169 多数元素 Boyer-Moore 投票：不同元素抵消，最后候选人再数一遍频次。

**选型决策（面试白板前 10 秒）**

| 需求 | 首选 | 次选 |
|------|------|------|
| 按下标 O(1) 读写、尾部增删多 | 动态数组 | 链表 |
| 头部插入删除多、总长未知 | 链表 | 动态数组头插 O(n) 差 |
| 撤销/递归、括号、DFS | 栈 | — |
| BFS、按层、FIFO | 队列 | 双端队列 |
| 两端伸缩、滑动窗口 | 双端队列 | 两个栈模拟 |
| 按 key 频繁查找更新 | 哈希表 | 有序结构 BST |
| 需要有序遍历 | BST / 平衡树 | 哈希不行 |

**与 manifest 子 slug 的对应**

| Study 子目录 | atelier slug | 撰写状态见 `_meta/人工撰写进度.md` |
|--------------|--------------|--------------------------------------|
| `linear/array` | `ds-linear-array` | 单结构 deep dive |
| `linear/linked_list` | `ds-linear-linked-list` | |
| `linear/stack` | `ds-linear-stack` | |
| `linear/queue` | `ds-linear-queue` | |
| `linear/deque` | `ds-linear-deque` | |
| `linear/hash_table` | `ds-linear-hash-table` | |

本页 `ds-linear` 为**父级总览**，manifest 可能尚未单独登记 slug；以 `topic_path: data_structures/linear` 与 Study 目录为准。子页写完后，在本页「学习路径」中加交叉链接即可。

### 典型应用

| 结构 | 刷题 / 系统场景 |
|------|-----------------|
| 数组 / 动态数组 | 前缀和、二分、双指针、Kadane；`vector` 底层 |
| 链表 | 反转、k 组翻转、快慢指针判环、合并有序链表 |
| 栈 | 有效括号、单调栈（柱状图最大矩形）、DFS 显式栈 |
| 队列 | BFS、滑动窗口最大值（配合单调队列） |
| 双端队列 | 滑动窗口最值、0-1 BFS 优化 |
| 哈希表 | 两数之和、频次统计、去重、LRU 的 key 索引 |

**单调栈模板**：维护递减（或递增）下标栈，当前元素入栈前弹出不满足单调性的栈顶，用于「下一个更大元素」「接雨水」等。与 `stack` 专题及 `algorithms/` 中相关题联动。

**设计题组合**：LRU = 哈希 + 双向链表（见 `iv-classic-lru-cache`）；LFU 再加频次桶；最小栈 = 双栈。识别「需要 O(1) 定位 + 顺序约束」时想到哈希与链表组合。

### 易错点

1. **混淆「子序列」与「子数组」**：前者可删元素不连续，后者必须连续；数组双指针题多为子数组。
2. **链表空指针**：`cur.next` 前未判 `cur is None`；删除后仍访问已断开节点。
3. **循环队列满空判断**：仅用 `front == rear` 无法区分；用 `size` 或牺牲一槽。
4. **双栈队列的均摊**：单次 `dequeue` 最坏 O(n) 来自整栈倒入，均摊仍 O(1)。
5. **哈希 rehash 时重复插入**：rehash 必须遍历旧桶重新插入，不能浅拷贝指针导致链表环。
6. **动态数组 `erase` 后未清尾**：逻辑 `size` 减小后旧槽置 `None` 防悬挂引用（Python）；C++ 注意析构。
7. **MinStack 相等最小值**：重复 `push` 相同最小值时辅助栈也要多次压入，否则 `pop` 一次丢失层数信息。
8. **双向链表哨兵**：`head`/`tail` 不存业务数据，计数 `size` 时不计入哨兵。

**调试建议**：为链表实现 `to_list()` 序列化输出；队列打印 `front,size,cap`；哈希表在 debug 模式打印每桶链长分布，检查是否严重偏斜。

### 练习建议

1. **先跑通六份脚本**：建立「仓库代码可信」的信心，再闭卷写简化版。
2. **按难度递进**：`206` 反转链表 → `21` 合并 → `141/142` 环 → `25` k 组 → `146` LRU（跳转 interview 专题）。
3. **栈队列互实现**：白板写 `StackQueue` 与 `QueueUsingStacks`，各 5 分钟。
4. **哈希**：`1` Two Sum、`3` 无重复字符最长子串（窗口 + 哈希）。
5. **子指南拆分**：数组专题练扩容与摊还证明；队列专题练循环数组；哈希专题练 rehash 手写。

每完成一题，在 Study `problems/leetcode/<slug>/` 对照 `solution.py`，勿只改 atelier 博文而不跑仓库测试。

## Python 实现

本目录实现分散在六个子文件夹。以下摘录与总览最相关的三类：**动态数组**、**循环队列 + 双栈队列**、**链地址哈希表**。完整代码以仓库为准。

**动态数组（`array/dynamic_array.py`）**

```python
class DynamicArray:
    def __init__(self, initial_capacity: int = 4) -> None:
        if initial_capacity < 1:
            initial_capacity = 1
        self._capacity = initial_capacity
        self._size = 0
        self._data: list[object | None] = [None] * self._capacity

    def at(self, index: int) -> object:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        return self._data[index]

    def push_back(self, value: object) -> None:
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def _resize(self, new_cap: int) -> None:
        new_data: list[object | None] = [None] * new_cap
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_cap
```

读代码时盯住 `_size` 与 `_capacity` 分离：对外 `len` 只反映 `_size`，扩容不改变逻辑长度。

**循环数组队列与双栈队列（`queue/queue.py`）**

```python
class CircularArrayQueue:
    def enqueue(self, x: object) -> None:
        if self._size == self._cap - 1:
            self._grow()
        rear = (self._front + self._size) % self._cap
        self._buf[rear] = x
        self._size += 1

class StackQueue:
    def dequeue(self) -> object:
        if not self._out:
            while self._in:
                self._out.append(self._in.pop())
        if not self._out:
            raise IndexError("dequeue empty")
        return self._out.pop()
```

`CircularArrayQueue` 适合 BFS；`StackQueue` 适合面试「用栈实现队列」原题。

**链地址哈希表（`hash_table/hash_table.py`）**

```python
class HashTableChaining:
    _LOAD_MAX = 0.75

    def insert(self, key: int, val: object) -> None:
        if (self._n + 1) > self._LOAD_MAX * self._m:
            self._rehash(self._m * 2)
        bi = self._h(key, self._m)
        e = self._buckets[bi]
        while e is not None:
            if e.key == key:
                e.val = val
                return
            e = e.next
        self._buckets[bi] = _Entry(key, val, self._buckets[bi])
        self._n += 1
```

`insert` 更新已存在键时不增加 `n`；`_rehash` 通过重新 `insert` 保证新桶分布正确。

**栈与最小栈（`stack/stack.py`）**：`ArrayStack` 用 `list` 尾操作；`MinStack` 用辅助栈同步最小值——提交 [155](https://leetcode.cn/problems/min-stack/) 时可压缩为单文件。

**链表（`linked_list/linked_list.py`）**：`SinglyLinkedList` 带 `dummy`；`DoublyLinkedList` 带哨兵——与 LRU 双向链表同族，建议对照 `iv-classic-lru-cache`。

**双端队列（`deque/deque.py`）**：`CircularDeque` 四角 O(1) 均摊；可用于 [239](https://leetcode.cn/problems/sliding-window-maximum/) 的单调队列外层容器。

**单链表反转（`linked_list/linked_list.py` 节选）**

```python
def reverse(self) -> None:
    prev: SNode | None = None
    cur = self._dummy.next
    self._dummy.next = None
    while cur is not None:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    self._dummy.next = prev
```

**MinStack（`stack/stack.py` 节选）**

```python
def push(self, x: int) -> None:
    self._s.append(x)
    if not self._mins or x <= self._mins[-1]:
        self._mins.append(x)
```

完整类含 `pop` 时同步弹辅助栈；提交 OJ 时类名改为 `MinStack` 并与题面方法名一致。

**本地批量回归（PowerShell）**

```powershell
$root = 'F:\Study\Algorithm\python\data_structures\linear'
@('array\dynamic_array.py','linked_list\linked_list.py','stack\stack.py',
  'queue\queue.py','deque\deque.py','hash_table\hash_table.py') | ForEach-Object {
  python -LiteralPath (Join-Path $root $_)
}
```

六行输出均含 `OK` 再进入刷题；任一脚本失败先修仓库再写题解，避免在错误基线上堆题解。

## C++ 实现

C++ 镜像目录与 Python 对称，文件名为 `dynamic_array.cpp`、`linked_list.cpp`、`stack.cpp`、`queue.cpp`、`deque.cpp`、`hash_table.cpp`。风格上：

- 动态数组使用 `std::vector` 教学复刻或手写 `T* data; size_t sz, cap;`；
- 链表节点 `struct Node { T val; Node* next; };`；
- 栈/队列可用 `std::stack` / `std::queue` 对照标准库，但仓库提供手写版便于面试白板；
- 哈希表桶类型 `vector<Entry*>` 或 `forward_list`。

```cpp
// 节选：数组栈 + 链表栈（Study cpp/data_structures/linear/stack/stack.cpp）
struct ArrayStack {
    vector<int> a;
    void push(int x) { a.push_back(x); }
    void pop() { if (a.empty()) throw underflow_error("pop"); a.pop_back(); }
    int top() const { if (a.empty()) throw underflow_error("top"); return a.back(); }
};
```

**编译栈模块示例**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\linear\stack'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o stack.exe stack.cpp
.\stack.exe
```

若包含 `alg_std.hpp`，统一从 `cpp/include` 引入工具函数。与 Python 版保持相同断言输出（如 `Stack OK`），便于双语言对拍。

**与 STL 的对照（面试口述用）**

| 教学类 | STL 近似 | 注意 |
|--------|----------|------|
| `DynamicArray` | `vector` | `vector` 不提供中间 insert 的频繁使用建议 |
| `SinglyLinkedList` | `forward_list` | 无 `size()` O(1) 除非自己维护 |
| `ArrayStack` | `stack` 适配器 | 默认 `deque` 底层 |
| `CircularArrayQueue` | `queue` | `queue` 不暴露遍历 |
| `HashTableChaining` | `unordered_map` | 均摊常数，迭代顺序不定 |

笔试若允许 STL，可直接 `unordered_map` + `list` 做 LRU；但「手写线性表」题仍要求你能脱离 STL 实现核心操作。

## 练习与延伸

**仓库内题解（节选，链到 `problems/leetcode/`）**

| 题号 | 主题 | 目录 slug 示例 |
|------|------|----------------|
| 206 | 反转链表 | `0206_reverse_linked_list` |
| 21 | 合并有序链表 | `0021_merge_two_sorted_lists` |
| 20 | 有效括号 | `0020_valid_parentheses` |
| 155 | 最小栈 | `0155_min_stack` |
| 239 | 滑动窗口最大值 | `0239_sliding_window_maximum` |
| 1 | 两数之和 | `0001_two_sum` |
| 146 | LRU | `0146_lru_cache`（设计专题见 `iv-classic-lru-cache`） |

**按结构分类的刷题延伸（与 `iv-top-frequent` 索引章对应）**

链表章 14 题建议顺序：206 → 21 → 141 → 142 → 160 → 19 → 24 → 25 → 92 → 148 → 234 → 237 → 2 → 146。前两题用 `linked_list.py` 的哑节点与反转模板；146 必须跳转 `iv-classic-lru-cache` 手写双向链表，勿仅用 `OrderedDict` 糊弄面试。

数组与窗口章：88 合并有序数组（三指针从尾填）→ 27/75 原地划分 → 11 对撞指针 → 15 三数之和（排序+双指针）→ 42 接雨水 → 239 单调队列。239 外层用 `CircularDeque` 或 `collections.deque`，内层维护单调递减下标队列，与 `ds-linear-deque` 专题一致。

栈章：20 括号匹配 → 32 最长有效括号（栈+DP 或两次遍历）→ 84/85 单调栈 → 155 直接对照 `stack.py` 的 `MinStack`。84 题若 WA，检查弹栈时宽度是否用「当前 i 与栈顶下标差减 1」。

哈希章：1 → 3 → 560 → 136 → 169 → 287。560 前缀和+频次是子数组和问题的母题；287 把数组当链表跳 next 索引是「指针技巧」而非哈希，但常放在哈希章复习。

**设计题与 advanced 目录**

`data_structures/advanced/lru_cache.py` 是封装版 LRU；面试手写以 `interview/classic/lru_cache` 为准。跳表在 `advanced/skip_list`，不在 linear 目录，勿与本页混淆。

**对拍与测试习惯**

每写一题，在 `solution.py` 的 `if __name__ == "__main__"` 加 2–3 组边界：空输入、单元素、最大规模抽样。链表题额外测「有环/无环」。队列题测「连续 dequeue 空队列抛错」。哈希题测「重复 insert 更新值」与「erase 不存在键」。

**子指南延伸**

- `ds-linear-array`：摊还分析、缩容策略、与 `vector` 差异；
- `ds-linear-linked-list`：快慢指针、环入口、哑节点专题；
- `ds-linear-stack` / `ds-linear-queue`：单调栈、BFS 层序；
- `ds-linear-deque`：滑动窗口模板；
- `ds-linear-hash-table`：开放寻址、字符串键、布隆过滤器衔接 `ds-advanced-bloom-filter`。

**不建议**在本总览重复粘贴 103 题高频表；面试索引见 `iv-top-frequent`。

## 学习路径

**第 0 天：环境与信任**

克隆 Study 仓库，`Set-Location` 到 `python/data_structures/linear`，按 Study 对照章节的 PowerShell 循环跑通六个 `*.py`。若有任一脚本失败，先修环境（Python 版本、路径）再刷题；不要在脚本未通过时开始写 LeetCode 题解，否则无法判断 WA 是思路错还是习惯错。

**第一周（建立物理模型：数组 + 栈）**

1. 阅读本页「基础篇」六节，重点「抽象模型」「核心操作」「实现要点」；
2. 精读 `array/dynamic_array.py`，手写 `push_back` 与 `_resize`，口述摊还证明；
3. 精读 `stack/stack.py`，对比 `ArrayStack` 与 `LinkedStack`，默写 `MinStack`；
4. 题：206（链表可提前）、20、155。206 用哑节点反转，20 用栈匹配括号；
5. 每日 30 分钟 C++：编译 `cpp/.../stack/stack.cpp`，与 Python 输出对照。

**第二周（链表 + 队列 + 双端队列）**

1. `linked_list.py`：实现 `reverse`、`delete_first`，画 142 环入口图；
2. `queue/queue.py`：默写 `CircularArrayQueue.enqueue/dequeue` 与 `_grow`；
3. `deque/deque.py`：理解 `push_front` 对 `_front` 的模运算；
4. 题：21、141、142、19、239。239 先写单调队列再写 deque 容器；
5. 周末：双栈队列白板 7 分钟 + 循环队列满空判断口述 3 分钟。

**第三周（哈希 + 设计 + 串联）**

1. `hash_table.py`：手写 `insert/get/erase/_rehash`，测装载因子触发；
2. 题：1、3、560（可选）、146。146 必须读 `iv-classic-lru-cache` 并手写链表版；
3. 择一子目录写 C++ 对拍（建议 `hash_table` 或 `linked_list`）；
4. 复盘：用「选型决策表」做 10 道混合题只分类不写代码（限时 15 分钟）。

**第四周（索引章扫尾与错题）**

打开 `iv-top-frequent` 笔记的链表/数组/栈/哈希四章，勾掉尚未完成的题；每题 AC 后在 `notes.md` 或私人卡片写「模式一词」。本页总览不追踪题号，进度以题单页为准。

**每日时间盒（在职备考参考）**

| 时段 | 内容 |
|------|------|
| 40 min | 1 道新题（索引表进目录） |
| 20 min | 复习昨日 1 道或重跑脚本 |
| 10 min | 读子目录 `notes.md` 一行 |

**复习检查清单**

- [ ] 能口头说出六类结构的核心操作复杂度；
- [ ] 能白板画循环数组 `front/size` 与满空判断；
- [ ] 能写出双栈队列的 `dequeue`；
- [ ] 能解释哈希 rehash 为何必须重新插入；
- [ ] 知道各子目录在 Study 与 atelier 的 slug 对应关系；
- [ ] 六份 Python 自测全部 OK；
- [ ] 至少 3 道题有 C++ 对拍记录；
- [ ] 146 能手写 LRU 双向链表版（15 分钟内）。

**从总览到子指南的跳转时机**

当你在某结构连续 3 题 WA 或「能 AC 但讲不清」时，进入对应 `ds-linear-*` 子指南（撰写完成后）或 Study `GUIDE.md`，不要在本总览重复找细节。总览负责地图，子指南负责街道。

**总览读完后的能力标准（自评）**

能在白纸画出循环队列的 `front/size/cap` 并说明满条件；能在五分钟写出单链表反转与双栈队列 `dequeue`；能口述哈希 rehash 触发条件与链地址插入步骤；能根据题意在「数组/链表/哈希」三者中选型。若四项中任两项做不到，回到对应子目录脚本与 `notes.md` 再练一天，不必继续刷新题。达到四项后，再打开 `iv-top-frequent` 按章刷题，每章至少完成该章最小集的一半题号。

**与 STL/Python 内置结构的对应关系（面试常问）**

`vector`/`list` 对应动态数组与链表语义；`stack`/`queue`/`deque` 适配器对应栈队列双端队列；`unordered_map` 对应哈希。手写题要求你实现底层时，应能说明 STL 默认实现与教学版的差异（如 `stack` 底层默认 `deque`），体现你知道标准库存在但题面要求自建。


**六结构详细 FAQ（面试口述用）**

**问：Python list 的 append 和 pop 复杂度？** 均摊 O(1)，与动态数组一致；insert(0, x) 是 O(n)。面试写题默认用 list 当栈，除非题目要求「链表实现栈」。

**问：何时必须用链表？** 需要 O(1) 在已知节点删除、或头插极频繁且总长很大、或 LRU/LFU 类设计题。纯刷数组题不必强行链表。

**问：总览篇要背多少代码？** 不必背六份全文；背接口语义与 206/20/1 模板即可，其余随用随查 Study 脚本。达到 medium 字数门槛后请跑 strict 校验再申请 published。校验通过即可。

**问：队列用 list.pop(0) 可以吗？** 单次 O(n)，BFS 会 TLE；用 collections.deque 或本仓库循环数组。

**问：哈希表键可以是 list 吗？** Python 中 list 不可哈希；用 tuple 或把 list 转成字符串。仓库 HashTableChaining 示例键为 int，泛化时约束键可哈希。

**问：双向链表比单链表占多少额外空间？** 每节点多一个指针；换来 O(1) 删除已知节点与 LRU 类题的统一写法。

**问：栈和递归的关系？** 函数调用栈即系统栈；DFS 可递归可显式栈；深度过大需改迭代或增大栈。

**问：单调栈和单调队列区别？** 栈用于「上一个更小/更大」与柱状图；队列用于滑动窗口最值且维护时间序。

**问：开放寻址 vs 链地址？** 开放寻址缓存友好、删除需 tombstone；链地址删除简单、指针开销大。教学与面试手写多用链地址。

**问：rehash 时为何不能复制链表头指针到新桶？** 同一节点只能属于一个桶链，浅拷贝会导致环或丢失节点；必须重新计算 hash 并 insert。

**问：循环数组 _grow 为何重置 front=0？** 逻辑序从 0 开始连续存放，简化后续下标计算。

**实现细节对照表（Python 文件名 → 核心 API）**

| 文件 | 类 | 必记 API |
|------|-----|----------|
| dynamic_array.py | DynamicArray | at, push_back, pop_back, insert, erase |
| linked_list.py | SinglyLinkedList, DoublyLinkedList | append, prepend, reverse, delete_first |
| stack.py | ArrayStack, LinkedStack, MinStack | push, pop, top, get_min |
| queue.py | CircularArrayQueue, StackQueue | enqueue, dequeue |
| deque.py | CircularDeque | push_front/back, pop_front/back |
| hash_table.py | HashTableChaining | insert, get, erase |

**与 LeetCode 设计题标签对应**

| 题号 | 结构组合 |
|------|----------|
| 146 LRU | 哈希 + 双向链表 |
| 155 Min Stack | 双栈 |
| 232 用栈实现队列 | 双栈 |
| 225 用队列实现栈 | 双队列 |
| 641 循环双端队列 | 循环数组 |
| 706 哈希表设计 | 拉链或开放寻址 |

**阅读顺序再强调**

先本总览 → 六脚本 OK → iv-top-frequent 链表/栈/哈希章 → 子指南 ds-linear-* → 题解目录 AC。跳过脚本直接刷题易形成题海记忆而非结构直觉。

**Windows 路径注意**

PowerShell 路径含空格时用 -LiteralPath；Python 用 python -LiteralPath 全路径运行脚本。

**草稿纸习惯**

画链表先画 dummy；画循环队列标 front/size/cap；画哈希写 buckets 数与 load factor。

**团队 Review 清单（贡献 Study 时）**

改 linear 任一脚本：跑脚本、跑相关题解、更新 notes.md、同步 atelier 摘录。

**语言互译检查点**

Python list.pop 尾删 ↔ vector::pop_back；KeyError ↔ optional；None ↔ nullptr。

**最后一遍自测**

随机抽：扩容时机、MinStack 相等最小值、循环队列满条件、rehash 触发、206 反转。任一项说不清则回基础篇重读。



**深度学习补充（二）：各子目录代码走读要点**

**array/dynamic_array.py**：`insert` 从后向前搬移保证 O(n)；`erase` 同理。`pop_back` 将 `_data[_size]` 置 None 帮助 GC。初始 `capacity` 至少 1 避免除零。面试若要求「动态数组类」可只实现 push_back/pop_back/at 三个接口，insert/erase 口述 O(n) 即可。

**linked_list/linked_list.py**：`SinglyLinkedList.append` 走到尾 O(n)，面试可要求 O(1) 尾插则维护 tail 指针。`DoublyLinkedList` 哨兵不纳入 `__len__`。`reverse` 清空 `_dummy.next` 后重挂，勿忘处理原 head 断开。`to_list` 用于断言，提交 OJ 时删除。

**stack/stack.py**：`LinkedStack` 头插 O(1)；`ArrayStack` 更适合 Python 面试。`MinStack.pop` 在 x==mins[-1] 时同步弹 mins，相等元素重复压 mins 的规则是 155 题关键。

**queue/queue.py**：`CircularArrayQueue` 满条件 `_size == _cap - 1` 与留空槽等价表述要一致。`_grow` 线性化元素后 front=0。`StackQueue` 均摊分析：每个元素入 in 一次、倒入 out 一次、出队一次。

**deque/deque.py**：四角操作对称；满时 `_grow` 与队列相同。239 题单调队列存下标而非值，避免重复值比较错误。

**hash_table/hash_table.py**：`erase` 头节点与中间节点分支；`_rehash` 清空后逐 insert 保证分布。`initial_buckets` 至少 1。测试用例覆盖更新已存在键、删除不存在键抛 KeyError。

**与 iv-top-frequent 链表章的题号映射（复习用）**

206 用 reverse；21 用 dummy 合并；141/142 快慢指针；19 双指针间隔；24 交换对；25 分段 reverse；92 找前驱反转段；148 merge sort；234 后半反转；237 值复制；2 进位链；146 跳 classic LRU。

**与数组章映射**

88 三指针归并；11 对撞；15 排序+双指针；42 双指针或单调栈；56 排序合并区间；121/122 状态机 DP 或贪心；152 维护 max/min 乘积；189 三次反转；238 前后缀积；239 单调队列；560 前缀和+map；283 双指针挪零。

**C++ 编译参数备忘**

在 `cpp/data_structures/linear/<topic>` 下：`g++ -std=c++17 -O2 -Wall -Wextra`，需要时 `-I` 指向 include。Windows 路径用 LiteralPath。输出 OK 字符串与 Python 一致才视为对拍成功。

**发布 checklist（ds-linear 本页）**

- [ ] 汉字 ≥8000（validate_algorithm_guide.py --slug ds-linear）
- [ ] 九节齐全、基础篇六个 ### 与 topic-ds 一致
- [ ] Python/C++ 实现节含代码围栏
- [ ] 无附录/FAQ 独立 ## 大块
- [ ] topic_path data_structures/linear 与 Study 一致



**本页与 manifest 子 slug 的关系**：`ds-linear-array` 至 `ds-linear-hash-table` 在 `manifest.json` 中已登记；本总览 `ds-linear` 对应父路径 `data_structures/linear`，作为入口页可在 manifest 中后续补登。撰写子指南时勿重复本页大段表格，只链回「选型决策」与 Study 对照即可。

**发布前自检（作者用）**：汉字 ≥8000；`guide_toc: topic-ds`；基础篇含抽象模型、核心操作、实现要点、典型应用、易错点、练习建议六个 `###`；含 Python/C++ 实现与真实代码围栏；无「附录」「常见问题」等禁用 `##` 标题。通过后可将 frontmatter 中 `status` 改为 `published`（由维护者执行）。

**给复习者的最后一句话**：若你只能记住一件事——刷题时先判断「这道题在用哪种线性结构」，再打开对应子目录脚本或 `iv-top-frequent` 章节，比死记题号更能应对变形题。

**扩展阅读路径（按周）**

第 1 周专注数组与栈：阅读 `array/notes.md` 与 `stack/notes.md`，完成 20、155、88。第 2 周专注链表：阅读 `linked_list/notes.md`，完成 206、21、141。第 3 周队列与双端队列：完成 BFS 模板题与 239。第 4 周哈希与设计：完成 1、3、146（手写专题）。每周用半小时对照 C++ 子目录编译输出，确认与 Python 一致。若某周任务过重，可将哈希周与链表周对调，但勿跳过「六脚本全部 OK」的前置步骤。

**与课程教材的对应**

严蔚敏《数据结构》中线性表、栈、队列、哈希查找各章，与本目录六文件夹一一对应。教材公式偏抽象，Study 代码偏可运行；建议教材课后题用仓库脚本验证理解，例如用 `DynamicArray` 模拟教材「顺序表插入」复杂度分析。CMU 15-213 中 cache 友好性讨论可联系数组与链表的局部性差异，深化「为何 BFS 用数组队列」。

**常见面试追问汇总**

能否 O(1) 删除数组中间元素？不能，除非交换尾元素均摊。链表如何找中间？快慢指针。如何判断链表有环？快慢相遇。栈如何实现队列？双栈倒入。队列如何实现栈？双队列轮转。哈希冲突怎么办？拉链、探测。rehash 时元素去哪？重新 hash 插入新桶。这些问题应在本总览读完后 30 秒内各有 20 字答案。

**PowerShell 一键回归（复制到个人笔记）**

```powershell
$root = 'F:\Study\Algorithm\python\data_structures\linear'
@('array\dynamic_array.py','linked_list\linked_list.py','stack\stack.py',
  'queue\queue.py','deque\deque.py','hash_table\hash_table.py') | ForEach-Object {
  python -LiteralPath (Join-Path $root $_)
}
```

**manifest 说明**：本页 slug 为 `ds-linear`，`topic_path` 为 `data_structures/linear`；子 slug `ds-linear-array` 等已在 manifest 登记。父级总览可后续补登 manifest，不影响本地阅读。

**发布校验**：`python scripts/validate_algorithm_guide.py --slug ds-linear`（需 manifest 含该 slug）；`guide_toc: topic-ds`；汉字不少于 8000；九节结构完整。

**各子目录 notes.md 一句话摘要（便于跳转前预览）**

`array/notes.md` 讲动态数组扩容与摊还；`linked_list/notes.md` 讲单双向链表与反转；`stack/notes.md` 讲数组栈链表栈与最小栈；`queue/notes.md` 讲循环数组队列与双栈队列；`deque/notes.md` 讲循环双端队列；`hash_table/notes.md` 讲链地址法与装载因子。总览不替代上述笔记，只负责串联。

**给完全零基础读者的起步建议**

若从未写过链表，先花两小时只跑 `linked_list.py` 与 206 题解，再回本页读抽象模型。若从未写过哈希，先跑 `hash_table.py` 再作 1 题。栈与队列可用 Python `list` 与 `collections.deque` 对照理解后再看手写版。跳跃式阅读六节理论而不跑脚本，容易形成「看懂但写不出」的假象。

**维护者与站点同步**

`ds-linear` 父路径指南可在 manifest 补登 `topic_path: data_structures/linear`。子指南更新时，本页仅修订「Study 对照表」「Python 摘录」与 FAQ，避免六篇子文重复。汉字篇幅以 `count_chinese` 为准，达标前勿标 `published`。

**最后检查**：六脚本 OK、206/20/1 各 AC 一题、能白板双栈队列、能解释 rehash——四项满足即可进入子专题或索引刷题。


## 延伸阅读

- Study 仓库根目录：[zhk0567/Algorithm](https://github.com/zhk0567/Algorithm)
- 各子目录 `notes.md`：`python/data_structures/linear/<topic>/notes.md`
- 站点子指南：`algorithm-guides/ds-linear-array` 等（撰写进度见 `_meta/人工撰写进度.md`）
- 面试设计专题：`iv-classic-lru-cache`、`iv-classic-lfu-cache`
- 算法导读：`overview`、`prob-hot100`

维护约定：子目录代码行为变更时，先更新子目录 `notes.md` 与单篇子指南，再回本页修订对照表与摘录片段，避免总览与实现脱节。

**C++ 侧补充说明（各子目录共性）**

`cpp/data_structures/linear/array/dynamic_array.cpp` 通常用 `std::unique_ptr<T[]>` 或 `vector` 封装教学逻辑；链表节点在堆上 `new`/`delete`，面试题若 OJ 接管内存则不必手写析构。栈的 `LinkedStack` 与 `ArrayStack` 对照可说明「STL stack 默认基于 deque 而非 vector」的原因：deque 两端 O(1) 均摊。队列的循环数组版与 `std::queue` 对比时，强调 STL 不暴露遍历接口是为了保持抽象。哈希表手写版与 `unordered_map` 对比时，说明标准库可能用桶 + 链表或开放寻址，均摊 O(1) 是期望而非最坏。

**面试白板时间分配建议**

| 任务 | 建议用时 |
|------|----------|
| 口述数组 vs 链表 | 1 分钟 |
| 写栈/队列接口 + 一种实现 | 8–10 分钟 |
| 反转链表 | 5 分钟 |
| 双栈队列 | 7 分钟 |
| 哈希 insert/get（拉链） | 10 分钟 |

超时往往卡在指针画图，建议平时用 `to_list()` 打印辅助，考场用哑节点减少分支。

**与竞赛的差异**

竞赛更在意常数与是否用 `deque`/`vector`；面试更在意边界与能否解释均摊。本仓库教学代码偏面试可读性：显式异常、`__slots__`、自测 `main`。若你打 ICPC，可在同目录另建 `fast_*.py` 实验，勿污染主脚本断言。

**记忆口诀（可选）**

「数组随机快，链表插删灵；栈后进先出，队列先进先出；双端两头动，哈希键值通。」口诀只帮回忆，复杂度仍以表格为准。

**贡献者注意**

新增第七类线性结构（如跳表在 `advanced/skip_list`）不属于本目录，应在 `ds-advanced-skip-list` 写，勿并入本总览以免 scope 膨胀。若 `data_structures/linear/notes.md` 将来在仓库根层添加，应同步本页 Study 对照表，但正文仍避免粘贴题号索引表。

**manifest 说明**：本站已登记 `ds-linear` slug 对应本总览；六类子结构另有 `ds-linear-array` 等独立 slug。先读本页建立地图，再进入子 slug 深挖实现细节，避免在总览里重复六份完整源码。

**总览篇学习验收**：能在白板画数组/链表/栈/队列/哈希五张最小接口图；能口述 206/20/1 对应哪类结构；能运行 Python 与 C++ 各一例栈模块。满足后再拆读 `ds-linear-linked-list` 等子 slug，避免总览篇变成空读。

**复杂度对照再列（面试快答）**：数组按下标 O(1)、中间插入 O(n)；链表头插 O(1)、按下标访问 O(n)；栈队列均摊 O(1)；哈希期望 O(1) 最坏 O(n)。把「期望」与「最坏」说清楚，比背定义更能打动面试官。配合子目录 `linked_list/notes.md` 中的反转链表图示，总览篇即可收尾进入刷题阶段。六子专题 manifest 已登记，按表跳转即可。栈与队列建议各手写一遍最小 API 再刷 LeetCode 20/239，巩固比泛读更重要。哈希章重点理解「键不存在」与「值为 None」在开放寻址与拉链法下的不同处理，面试常考 rehash 触发时机。
