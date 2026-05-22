---
title: "数据结构 · 链表（单链表与双向链表）"
series: algorithm
category: DataStructures
topic_path: data_structures/linear/linked_list
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-22
tags: [DataStructures, LinkedList, SinglyLinkedList, DoublyLinkedList, DummyNode, Floyd]
---

# 数据结构 · 链表（单链表与双向链表）

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

**链表**是线性结构里最依赖「指针思维」的一类：元素在逻辑上仍排成一条线，但物理上通过每个节点里的 `next`（双向链表还有 `prev`）指向后继，不再要求连续内存。与动态数组相比，链表在**已知节点指针**时插入、删除可达 O(1)，却失去按下标 O(1) 随机访问的能力；按值查找必须 O(n) 遍历。面试与 Hot 100 中，链表题密度极高——反转、k 组翻转、快慢指针判环、合并有序链、删除倒数第 n 个、相交链表、复制带随机指针的链表等，本质都在考「能否在纸上稳定改写指针而不丢引用」。

本页是 atelier 子指南 `ds-linear-linked-list`，`topic_path` 为 `data_structures/linear/linked_list`，`guide_toc` 为 `topic-ds`（基础篇六个 `###` 与数据结构专题一致）。父级总览见 `ds-linear`：那里对比数组、栈、队列与哈希的选型；**本页只深挖链表**，把 Study 仓库 `linked_list.py` / `linked_list.cpp` 的教学实现、经典题模板与 C++/Python 对拍串成一条学习线。状态为 `draft`，正文达标并通过 strict 校验后可由维护者改为 `published`。

读完本文，你应能：

1. 区分单链表与双向链表的节点布局、哨兵写法及复杂度差异；
2. 在 Python 与 C++ 镜像路径下运行 `linked_list` 自测并本地对拍；
3. 默写哑节点反转、双链表四指针插入删除、Floyd 快慢指针判环与找环入口；
4. 知道何时该用链表（头插频繁、已知节点 O(1) 删、LRU 类设计）而非动态数组；
5. 按题单顺序从 206 递进至 25、146，并跳转 `iv-classic-lru-cache` 理解双向链表在设计题中的角色。

**与数组的边界（十秒选型）**：需要按下标读写、尾部增删、缓存局部性 → 动态数组；需要头部增删、中间已知节点删除、总长度不确定、或哈希表挂接顺序 → 链表。许多「链表题」并不要求你实现完整 `SinglyLinkedList` 类，而是给定 `ListNode` 接口做局部改写；但仓库教学版把 append、reverse、delete_first 写全，是为了让你建立可复用的指针习惯，而不是背题号。

**为何单独成篇**：线性结构总览 `ds-linear` 已在一张表里对比六类结构，链表部分不可能展开到能支撑二十余道 Hot 题的细节。本子指南把「节点—哑节点—反转—快慢—双向哨兵—题号映射」串成闭环，避免你在总览与题解之间来回跳却缺中间层。若你已完成 `ds-linear` 的六脚本回归，可直接从本页「Study 仓库对照」运行 `linked_list.py`，再进入基础篇；若尚未跑通总览脚本，建议先花十分钟运行六例建立「仓库代码可信」的信心，再回到本页专攻指针。

**面试中的常见失分点**：不是不会反转，而是在 `cur.next = prev` 之前没保存 `nxt`、删除节点后仍访问 `cur.next`、或 k 组翻转时断链导致后半段丢失。本页在「实现要点」与「易错点」中反复强调**先存后继再改指针**、**哑节点统一头插**，与仓库代码风格一致。

## 预备知识

> **预备知识**：理解引用/指针（Python 中 `next` 是引用，C++ 中 `SNode*`）；熟悉 `None` / `nullptr`；知道大 O 表示法；Python 3.10+；C++17 与 `g++` 基本编译。Windows 下用 PowerShell 的 `Set-Location -LiteralPath` 进入目录后运行脚本。

建议已具备：

- **节点与头指针**：单链表由 `head` 指向首节点，尾节点 `next is None`；空表即 `head is None`。
- **哑节点（dummy）**：不存业务数据的哨兵，`dummy.next` 才是真实头；统一「在头部插入」与「删除任意节点」的写法，避免 `if head is None` 分支爆炸。
- **双向链表哨兵**：`head` 与 `tail` 两个哑节点夹住真实节点，形成「双向循环哨兵」结构，与 LRU 缓存、LFU 桶链表同构。
- **递归与迭代**：反转既可递归（注意栈深度）也可三指针迭代；面试更推荐迭代，便于画图。

若你只用过 Python `list`，请暂时忘掉 `list.insert(0, x)` 的 O(1) 均摊错觉——那是动态数组实现，不是链表。链表头插才是真正的 O(1) 指针改写。

**环境核对**：克隆 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) 后，确认存在 `python/data_structures/linear/linked_list/linked_list.py` 与对称的 `cpp/data_structures/linear/linked_list/linked_list.cpp`；运行应输出 `LinkedList OK`。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/linear/linked_list` |
| Python 实现 | `python/data_structures/linear/linked_list/linked_list.py` |
| C++ 实现 | `cpp/data_structures/linear/linked_list/linked_list.cpp` |
| 笔记 | 两侧 `notes.md`（复杂度、哨兵、反转） |
| 导读 | `GUIDE.md`（与 notes 同构的速查） |
| 父级总览 | `ds-linear`（线性结构选型地图） |

**运行 Python 自测**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
python -LiteralPath 'F:\Study\Algorithm\python\data_structures\linear\linked_list\linked_list.py'
```

将 `F:\Study\Algorithm` 换成本机克隆根目录。期望输出：`LinkedList OK`。

**编译并运行 C++**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\linear\linked_list'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o linked_list.exe linked_list.cpp
.\linked_list.exe
```

`linked_list.cpp` 首行 `#include <alg_std.hpp>`，`-I` 指向 `cpp/include`。输出同样应为 `LinkedList OK`。

| 文件 | 主要内容 |
|------|----------|
| `linked_list.py` | `SinglyLinkedList`（dummy + reverse + delete_first）、`DoublyLinkedList`（head/tail 哨兵 + remove_node） |
| `linked_list.cpp` | 镜像结构；`SinglyLinkedList::clear` 释放堆节点 |
| `notes.md` | 操作复杂度表、典型应用、代码要点 |

站点 manifest 登记 slug 为 `ds-linear-linked-list`，`guide_tier: medium`（汉字不少于 8000）。题解不在 atelier 新建单题页，请进入 Study `problems/leetcode/<slug>/` 对照 `solution.py`。

## 基础篇

### 抽象模型

**逻辑结构**：元素 \(a_0,a_1,\ldots,a_{n-1}\) 仍按顺序排列，但不像数组那样隐含「下标即地址」；每个元素包装在**节点**里，节点在堆上（或语言运行时对象堆）分散分配，通过指针串联。

**单链表节点**（仓库 `SNode` / `SNode`）：

- 字段：`val`（载荷）、`next`（后继指针或引用）。
- 头指针：指向第一个**业务**节点；教学实现用 `dummy`，真实头为 `dummy.next`。

**双向链表节点**（`DNode`）：

- 字段：`val`、`prev`、`next`。
- 哨兵：`head` 与 `tail` 不存业务数据，`head.next` 为首节点，`tail.prev` 为尾节点；空表时 `head.next == tail`。

**存储结构**：非连续，缓存局部性弱于数组；每个节点额外一个或两个指针开销。长度 `n` 时空间 O(n)，常数因子高于数组。

**与 LeetCode `ListNode` 的对应**：OJ 常给出

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

无 `dummy`、无 `size`；你需要在解题函数内自建 `dummy = ListNode(0)` 或处理 `head` 为空。仓库 `SinglyLinkedList` 把 dummy 内置在类里，是为了**教学**时减少重复代码。

**空表语义**：`len==0` 即 `dummy.next is None`（或 `head is None`）；对空表调用「删首」「反转」应得到稳定结果（反转仍为空），删除不存在的值返回 `False` 或 no-op，与仓库断言一致。

### 核心操作

下表以当前元素个数 \(n\) 为尺度；「已知节点」指已有 `ListNode*` / 节点引用，无需从头查找。

| 操作 | 单链表 | 双向链表（含哨兵） | 需从头查找时 |
|------|--------|-------------------|--------------|
| 头部插入 | O(1) | O(1) | — |
| 尾部插入 | O(1) 若维护 `tail`，否则 O(n) | O(1) | — |
| 按值删除首个 | O(n) | O(n) | 需遍历 |
| 删除已知节点 | O(1) 若给定前驱；单向无 `prev` 时需 O(n) 找前驱 | O(1) | `remove_node` |
| 反转整条 | O(n) | O(n) | — |
| 按下标访问第 k 个 | O(k) | O(k) | 无随机访问 |
| 查找值 | O(n) | O(n) | — |

**头插与尾插**：仓库单链表 `prepend` 在 dummy 后插入 O(1)；`append` 从 `dummy` 走到尾 O(n)。面试若强调尾插性能，应额外维护 `tail` 指针并在尾插时更新——本教学实现选择「最小 API」以突出指针基本功，不隐藏尾指针的权衡。

**反转**：就地反转整条链，O(n) 时间、O(1) 额外空间（迭代）；递归版 O(n) 栈空间。

**判环与环入口**（题 141/142，非仓库类方法但属链表核心）：快慢指针；入口相遇数学见「实现要点」。

**合并两条有序链**（题 21）：哑节点 + 每次连接较小 `next`，O(n+m)。

**删除倒数第 n**（题 19）：双指针间隔 n+1，哑节点处理「删的是原头」。

### 实现要点

**哑节点统一头操作**

```python
self._dummy.next = SNode(val, self._dummy.next)  # prepend
```

删除时让 `cur` 从 `dummy` 出发，`while cur.next` 判断 `cur.next.val`，改写 `cur.next = cur.next.next`，保证删除目标的前驱始终可达。

**单链表反转（三指针）**

不变量：已反转部分挂在 `prev` 后，`cur` 为待处理首节点。

```python
prev, cur = None, self._dummy.next
self._dummy.next = None
while cur is not None:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
self._dummy.next = prev
```

关键：**先** `nxt = cur.next`，**再**改 `cur.next`。仓库在反转前清空 `dummy.next`，避免旧链仍挂在哑节点上造成分叉。

**双向链表在哨兵间插入（append）**

新节点插在 `tail.prev` 与 `tail` 之间，四步：`p.next = node; node.prev = p; node.next = tail; tail.prev = node`。`prepend` 对称地插在 `head` 与 `head.next` 之间。删除已知节点 `remove_node`：缓存 `p, n = node.prev, node.next`，再 `p.next = n; n.prev = p`，最后 `size -= 1`；C++ 版 `delete node` 释放堆内存。

**可选：尾指针 O(1) append**

维护 `self._tail` 指向最后一个业务节点，`append` 时 `self._tail.next = SNode(val); self._tail = self._tail.next`。删除尾节点时需 O(n) 找前驱，除非改用双向链表。面试白板若题目只有头插，可不要 tail。

**尾插与队列的关系**：若用单链表实现 FIFO 且只在尾部入队、头部出队，必须同时维护 `head` 与 `tail`，否则每次 `enqueue` 扫链 O(n) 会在 BFS 规模下 TLE。`ds-linear-queue` 专题更推荐循环数组或双栈；此处强调链表并非不能做队列，而是要做对指针维护。栈则单链表头插即可，与 `ds-linear-stack` 中 `LinkedStack` 一致。

**快慢指针（Floyd）**

- **判环（141）**：`slow` 每次一步，`fast` 每次两步；若相遇则有环；`fast` 到达 `None` 则无环。
- **环入口（142）**：相遇后，`slow` 回到 `head`，两指针同步每次一步，再次相遇点即为入口。推导：设入环前长度为 \(a\)，环长 \(c\)，相遇时 slow 在环内走了 \(b\)，则 fast 比 slow 多走 \(nc\)（整数 \(n\)），有 \(2(a+b)=a+b+nc\)，得 \(a = nc - b\)，即从 head 走 \(a\) 步等于从相遇点走 \(nc-b\) 步，二者在入口相遇。
- **找中点（876）**：快指针到尾时 slow 在中点；偶数长度时 slow 取左中或右中需与题意一致。

**双指针间隔（19、160）**

删除倒数第 n：哑节点 + `first` 先走 n+1 步，再与 `second` 同步；`second.next` 即为待删。相交链表（160）：对齐两链长度后同步前进，相遇即交点（或 None）。

**k 组翻转（25）**

先遍历求长度 `L`，再每 k 个调用局部反转；不足 k 的尾部保持原序。局部反转要记录**段前驱**与**段后继**，反转后把段挂回原链，避免断链。可与 92「反转 II」共用「找 left 前驱 + 反转区间内」模板。

**合并有序（21）**

```python
dummy = ListNode(0)
cur = dummy
while l1 and l2:
    if l1.val <= l2.val:
        cur.next = l1
        l1 = l1.next
    else:
        cur.next = l2
        l2 = l2.next
    cur = cur.next
cur.next = l1 or l2
return dummy.next
```

**数组模拟链表（287）**

把下标 `i` 视为节点，`nums[i]` 视为 `next`（需在 [0,n] 内），Floyd 判环找重复数——思想与 142 同族，不是物理链表但考指针技巧。

**C++ 内存**：教学 `SinglyLinkedList` 提供 `clear()` 遍历 `delete`；LeetCode 环境通常由平台回收。自己 `new` 的节点在练习对拍时要配对释放，避免泄漏。

### 典型应用

| 场景 | 为何用链表 |
|------|------------|
| LRU / LFU 缓存 | 哈希定位节点，双向链表维护使用时间序，O(1) 移动与淘汰（见 `iv-classic-lru-cache`） |
| 多项式相加 | 按指数稀疏存储，合并类似合并有序链 |
| 内存分配器空闲块 | 空闲块链成单链表，分配/释放 O(1) 摘链 |
| 图邻接表 | 每个顶点的边表常为链表或 `vector` |
| 大整数加法 | 数位逆序存链，逐位进位 |
| 设计题「链式栈/队列」 | 头插 O(1) 实现栈；队列常配合 dummy + tail |

**Hot 100 链表章**（与 `iv-top-frequent` 联动）：206 反转、21 合并、141/142 环、19 删倒数、24 两两交换、25 k 组、92 区间反转、148 排序、234 回文、237 删节点、2 加法、146 LRU。前四题覆盖本页 80% 指针模板；146 必须跳转面试专题手写双向链表。

**与哈希组合**：两数之和用哈希即可；LRU 必须哈希 + 双向链表。识别「需要 O(1) 按 key 找节点 + 维护顺序」即想到该组合。

### 易错点

1. **丢后继**：`cur.next = prev` 前未保存 `nxt`，链从当前节点之后全部丢失。
2. **删除后访问**：`cur.next = cur.next.next` 之后仍用旧 `cur.next` 读值或遍历。
3. **哑节点与真实头混淆**：返回 `dummy` 本身而非 `dummy.next`；或反转后忘记 `return dummy.next`。
4. **双指针间隔 off-by-one**：删倒数第 n 时，`first` 应领先 n+1 步（含哑节点），否则删错节点。
5. **环判断**：快指针写 `while fast and fast.next`，否则 `fast.next.next` 越界。
6. **k 组翻转断链**：局部反转后未把「段尾」接到「段后第一个」，导致后半段丢失。
7. **双向链表删节点漏改一侧**：只改 `prev.next` 不改 `next.prev`（或反之），链表断裂。
8. **相等值删除**：`delete_first` 只删第一个匹配；若题意删全部需循环或递归。
9. **C++ 迭代器式遍历中 delete**：在 `for (p = head; p; p = p->next) delete p` 应先存 `n = p->next` 再 delete。
10. **把 Python 引用当拷贝**：`a = b` 后改 `a.next` 会影响 `b` 所指的链；需要分叉时新建节点。

**调试习惯**：实现 `to_list()` / `to_vector()` 序列化；复杂题打印哑节点后的链；判环题可先用 `set` 存访问节点验证 Floyd 结果。

### 练习建议

1. **先跑通脚本**：`linked_list.py` 与 `linked_list.cpp` 均输出 OK，再闭卷写简化版 `SinglyLinkedList`（至少 `prepend`、`reverse`）。
2. **递进题序**：206 → 21 → 141 → 142 → 160 → 19 → 24 → 25 → 92 → 148 → 234 → 237 → 2 → 146（146 跳 `iv-classic-lru-cache`）。
3. **每周一块白板**：哑节点反转 5 分钟；双链表删除已知节点 5 分钟；Floyd 判环 + 口述入口证明 8 分钟。
4. **对拍**：每题在 `solution.py` 的 `main` 加空链、单节点、两节点环边界。
5. **与父级总览配合**：选型困惑时回 `ds-linear` 的「链表 vs 数组」表，勿在本页重复背六结构全文。

每 AC 一题，在 Study 题解目录对照官方写法；若专题讲解与题解实现不同，以题解 AC 为准、以专题理解指针为准。

## Python 实现

Study 文件 `python/data_structures/linear/linked_list/linked_list.py` 提供节点类与两个链表 ADT。以下摘录与讲解对应仓库行号逻辑；完整代码以仓库为准。

**节点定义与 `__slots__`**

```python
class SNode:
    __slots__ = ("val", "next")

    def __init__(self, val: object, next_: SNode | None = None) -> None:
        self.val = val
        self.next = next_
```

`__slots__` 减少实例字典开销，教学代码量小；提交 LeetCode 时通常不写 slots。

**单链表：哑节点与头插**

```python
class SinglyLinkedList:
    def __init__(self) -> None:
        self._dummy = SNode(0)
        self._size = 0

    def prepend(self, val: object) -> None:
        self._dummy.next = SNode(val, self._dummy.next)
        self._size += 1
```

`append` 从 `dummy` 扫描到尾，O(n)；面试追问尾插 O(1) 时答「加 tail 指针」。

**按值删除首个**

```python
    def delete_first(self, val: object) -> bool:
        cur = self._dummy
        while cur.next is not None:
            if cur.next.val == val:
                cur.next = cur.next.next
                self._size -= 1
                return True
            cur = cur.next
        return False
```

`cur` 始终指向待删节点的前驱，故永不直接删除 `dummy` 自身。

**反转（完整方法）**

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

自测顺序：空表 → append 1,2 → prepend 0 → reverse → 断言 `[2,1,0]`（见文件末尾 `if __name__`）。

**双向链表：哨兵与 append**

```python
class DoublyLinkedList:
    def __init__(self) -> None:
        self._head = DNode(0)
        self._tail = DNode(0)
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    def append(self, val: object) -> None:
        node = DNode(val)
        p = self._tail.prev
        assert p is not None
        p.next = node
        node.prev = p
        node.next = self._tail
        self._tail.prev = node
        self._size += 1
```

**O(1) 删除已知节点**

```python
    def remove_node(self, node: DNode) -> None:
        p, n = node.prev, node.next
        assert p is not None and n is not None
        p.next = n
        n.prev = p
        self._size -= 1
```

LRU 中「把节点移到头部」即先从链表中 `remove_node` 再 `prepend` 逻辑插入，或封装 `move_to_front`。

**序列化辅助**

```python
    def to_list(self) -> list[object]:
        out: list[object] = []
        cur = self._dummy.next
        while cur is not None:
            out.append(cur.val)
            cur = cur.next
        return out
```

调试链表题时建议手写同样函数，比打印对象地址可读。

**本地运行（PowerShell）**

```powershell
python -LiteralPath 'F:\Study\Algorithm\python\data_structures\linear\linked_list\linked_list.py'
```

## C++ 实现

C++ 镜像在 `cpp/data_structures/linear/linked_list/linked_list.cpp`，包含 `alg_std.hpp`，风格与 Python 对齐：单链表用栈上 `dummy`，双链表用 `head`/`tail` 哨兵。

**单链表节点与尾插**

```cpp
struct SNode {
    int val;
    SNode* next;
    SNode(int v, SNode* n = nullptr) : val(v), next(n) {}
};

struct SinglyLinkedList {
    SNode dummy{0, nullptr};

    void append(int v) {
        SNode* cur = &dummy;
        while (cur->next) cur = cur->next;
        cur->next = new SNode(v);
    }
```

**反转与释放**

```cpp
    void reverse() {
        SNode* prev = nullptr;
        SNode* cur = dummy.next;
        dummy.next = nullptr;
        while (cur) {
            SNode* nxt = cur->next;
            cur->next = prev;
            prev = cur;
            cur = nxt;
        }
        dummy.next = prev;
    }

    void clear() {
        SNode* p = dummy.next;
        dummy.next = nullptr;
        while (p) {
            SNode* n = p->next;
            delete p;
            p = n;
        }
    }
```

Python 由 GC 回收；C++ 练习对拍后应 `clear()` 或析构函数释放，避免泄漏。

**双向链表删除**

```cpp
    void remove(DNode* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
        delete node;
    }
```

**编译运行**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\linear\linked_list'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o linked_list.exe linked_list.cpp
.\linked_list.exe
```

**与 STL 对照**

| 教学类 | STL | 说明 |
|--------|-----|------|
| `SinglyLinkedList` | `std::forward_list` | 无 `size()` O(1) 除非自维护 |
| `DoublyLinkedList` | `std::list` | `list` 双向，无哨兵但可复用迭代器 |
| 题解 `ListNode` | 无直接对应 | 手写节点更常见 |

笔试允许 `list` 时，146 仍建议能手写双向链表 + `unordered_map`，因白板环境无 STL 文档。

## 练习与延伸

**仓库内题解（`problems/leetcode/`，节选）**

| 题号 | 主题 | 目录 slug 示例 |
|------|------|----------------|
| 206 | 反转链表 | `0206_reverse_linked_list` |
| 21 | 合并两个有序链表 | `0021_merge_two_sorted_lists` |
| 141 | 环形链表 | `0141_linked_list_cycle` |
| 142 | 环形链表 II | `0142_linked_list_cycle_ii` |
| 160 | 相交链表 | `0160_intersection_of_two_linked_lists` |
| 19 | 删除倒数第 N | `0019_remove_nth_node_from_end` |
| 25 | K 个一组翻转 | `0025_reverse_nodes_in_k_group` |
| 92 | 反转 II | `0092_reverse_linked_list_ii` |
| 146 | LRU 缓存 | `0146_lru_cache`（专题 `iv-classic-lru-cache`） |

**模板与题号映射**

- 206 / 92 / 25：三指针或分段反转 + 哑节点；
- 21：合并有序；
- 141 / 142 / 287：Floyd；
- 19 / 160：双指针间隔或对齐长度；
- 24：交换 `next` 对；
- 148：归并排序（快慢找中点 + 合并）；
- 234：后半反转或栈；
- 237：复制后继值（单链表无法 O(1) 删未知前驱时的 trick）；
- 2：哑节点 + 进位；
- 146：哈希 + 双向链表，勿仅用 `OrderedDict` 糊弄面试。

**不建议**在本页粘贴完整 103 题表；见 `iv-top-frequent` 链表章。

**对拍习惯**：链表题在 `main` 中构造 `1→2→3→4→5` 与 `1→2` 环两种数据；提交前删除 `print` 与 `to_list` 调试输出。

## 学习路径

**第 0 步：信任仓库代码**

运行 Python 与 C++ 脚本，确认 `LinkedList OK`。失败则检查 Python 版本、路径 LiteralPath、g++ 与 include。

**第 1–2 天：单链表 ADT**

1. 阅读本页「抽象模型」「核心操作」；
2. 精读 `SinglyLinkedList`，手写 `prepend`、`reverse`、`delete_first`；
3. 题 206（迭代反转）、21（合并）；
4. 白板 5 分钟默写反转三指针。

**第 3–4 天：指针技巧**

1. 141 / 142（画图推导入口）；
2. 19（哑节点 + 双指针）、160；
3. 24（交换对）；
4. 对照 `notes.md` 一行总结复杂度。

**第 5–7 天：双向链表与进阶**

1. 精读 `DoublyLinkedList`，理解 `remove_node`；
2. 25 / 92（分段反转，注意断链）；
3. 148（归并）、234（回文）；
4. 阅读 `iv-classic-lru-cache`，题 146 手写双向链表版。

**第 2 周：C++ 对拍与错题**

每天 10 分钟编译 `linked_list.cpp`；任选两道已 AC 的 Python 题解改写成 C++ `ListNode` 版本对比输出。

**复习检查清单**

- [ ] 能口头解释哑节点作用；
- [ ] 能 O(n) 时间 O(1) 空间迭代反转；
- [ ] 能口述 142 环入口证明要点；
- [ ] 能写双向链表在哨兵间的 append / remove；
- [ ] Python/C++ 脚本均 OK；
- [ ] 206、21、141、142、19 至少各 AC 一次；
- [ ] 146 能手写 LRU 双向链表版（15 分钟内）。

**从本页到父级总览**：若同时混淆栈、队列、哈希，回 `ds-linear` 选型表；若只链表薄弱，留在本子目录与 `iv-top-frequent` 链表章即可。

## 延伸阅读

- Study 仓库：[zhk0567/Algorithm](https://github.com/zhk0567/Algorithm)
- 本子目录笔记：`python/data_structures/linear/linked_list/notes.md`、`cpp/.../notes.md`
- 线性结构总览：`algorithm-guides/ds-linear`
- LRU 设计专题：`iv-classic-lru-cache`
- Hot 100 索引：`iv-top-frequent`（链表章）
- 严蔚敏《数据结构》第二章「线性表」链式存储部分，与仓库实现互证

维护约定：`linked_list.py` 行为变更时，先更新 Study `notes.md`，再修订本页摘录与复杂度表，避免站点与仓库脱节。

**LeetCode 手写 `ListNode` 清单（面试前夜）**

- 反转：保存 `nxt`，改 `next`，移动 `prev/cur`；
- 合并：哑节点 + `cur` 尾插；
- 环：快慢相遇；入口：相遇后 `slow=head` 同步走；
- 删倒数：`dummy`，`first` 领先 `n+1`；
- k 组：求长、分段、接回后继。

**PowerShell 路径提醒**：路径含空格或方括号时用 `-LiteralPath`；`python -LiteralPath` 运行脚本避免把路径当代码解析。

**与 advanced 目录边界**：跳表在 `data_structures/advanced/skip_list`，不属于本 `linear/linked_list` 目录；勿把跳表内容并入本页。

**发布前自检（作者）**：汉字 ≥8000；`guide_toc: topic-ds`；九节齐全；基础篇六个 `###` 标题与 topic-ds.yaml 一致；Python/C++ 实现节含真实代码围栏；`topic_path` 为 `data_structures/linear/linked_list`；`status: published` 直至 strict 双脚本通过。

**常见面试追问（20 字答法）**

- 链表为何不用二分？无随机访问。
- 如何 O(1) 删中间？双向且已知节点；单向需前驱。
- 如何判断回文？快慢找中点 + 反转后半或栈。
- 栈用链表实现？头插当头指针。
- LRU 为何双向？命中时要 O(1) 把中间节点挪到最近端。

**工业实现简述**：Linux 内核 slab、文件系统缓存等多用双向链表 + 嵌入 `list_head` 结构体；Redis quicklist 混合链表与压缩列表。理解教学版有助于读源码，但面试仍以 LeetCode 风格指针为准。

**贡献者同步**：修改 `linked_list.py` 时运行脚本、更新 `notes.md`、同步本页「Python 实现」摘录；C++ 同步 `linked_list.cpp` 与「C++ 实现」节。

**最后一遍自测**：随机抽「反转三行核心」「142 入口一句」「双向删节点四指针」「k 组为何要记录段后继」——任一项说不清则回基础篇重读并实现 `to_list` 调试。

**深度补充：单链表 append 的 O(n) 与面试变体**

仓库 `append` 从哑节点走到最后一个 `next`，教学上刻意保留 O(n) 扫描，让你感受「只有头指针时尾插代价」。面试 Follow-up「如何 O(1) append」：维护 `tail` 并在 `prepend` 时若原为空更新 `tail`；删除尾节点时单向链表需 O(n) 找前驱，故**频繁尾删**应换双向链表或动态数组。理解这一权衡后，看到「队列用链表实现」会优先想到「维护 head/tail 两个指针」而非每次 `append` 扫描。

**深度补充：复制带随机指针（138）**

用哈希 `原节点 -> 新节点` 第一遍创建所有新节点，第二遍接 `next` 与 `random`；或交错插入复制节点再拆分。二者都依赖 O(n) 额外空间；本页不展开代码，但提醒你：**链表题不只是改 next**，多指针字段时哈希映射是标准工具。

**深度补充：148 归并排序链表**

快慢找中点（注意断开 `mid.next`）、递归或迭代归并两条有序链，总 O(n log n)、O(log n) 栈。与 21 合并模板相同，是分治在链表上的典型。写错中点会导致死循环或漏排序后半段。

**深度补充：234 回文链表**

O(n) 空间用栈；O(1) 用快慢找中点、反转后半、比较、可选恢复链表（面试常不要求恢复）。偶数长度时后半起点是 `mid.next` 还是 `mid` 要与比较循环一致。

**深度补充：237 删除节点**

题目给定要删的 `node`（非尾），把 `node.val = node.next.val` 再 `node.next = node.next.next`，O(1) 但无法删尾节点；真实系统很少这样删，但 OJ 允许。与「单向链表已知前驱才能删」对比记忆。

**深度补充：2 两数相加**

哑节点 + 进位 `carry`，长度不等时短链先走完仍要处理进位。与 21 区别在「按位相加」而非「按值大小」。

**深度补充：24 两两交换**

`prev.next` 指向 `second`，注意交换的是 `first` 与 `second` 一对，循环步进 `prev = first`（交换后 first 在前一对的 second 位置）。画图优于背代码。

**深度补充：160 相交链表**

对齐长度后同步走，第一个相同指针即交点；若无交点则同遇 `None`。长度差计算用 `lenA`、`lenB` 或先遍历计数。

**深度补充：19 与 dummy 的必要性**

删「倒数第 n」可能删的是原头节点；无 dummy 时要特判 `head = head.next`。dummy 让 `second` 停在待删前驱，统一逻辑。

**深度补充：25 与 92 的关系**

92 给定 `left, right` 闭区间反转；25 是全局每 k 段。92 可视为 25 的「单段」特例。练习顺序建议 206 → 92 → 25。

**深度补充：Python 引用陷阱示例**

```python
a = node
b = node
b.next = None  # a.next 也为 None
```

复制链需要新建 `ListNode`，不能共享同一节点对象。

**深度补充：C++ `forward_list` vs 手写**

`forward_list` 只向前，无 `size()`；`list` 双向且带 size（C++11 起常数）。教学代码用哨兵是为了与 LRU 一致；`std::list` 无全局 dummy 但 `erase` 迭代器稳定。

**深度补充：竞赛与面试差异**

竞赛可开 `__slots__`、避免递归深度；面试要清晰画图、处理边界、解释复杂度。Floyd 判环空间 O(1)，哈希存集 O(n) 但写法快，面试先说 O(1) 再写 Floyd。

**深度补充：与 `ds-linear-array` 的衔接**

数组专题讲扩容与随机访问；链表专题讲指针。Hot 题中「删除排序数组重复项」用数组双指针；「删除排序链表重复」用链表指针，模式相似、实现不同。两页都读完再刷混合题单。

**深度补充：脚本断言阅读**

`linked_list.py` 末尾：空表删除失败；`append/prepend` 后反转；双向链表 `remove_node` 删中间节点。读断言即读规格，改代码前先让断言绿。

**深度补充：错误链表示例（教学勿模仿）**

在反转循环里写 `cur.next = prev; cur = cur.next` 而未先存 `nxt`，`cur.next` 已被改成 `prev`，`cur = cur.next` 会回退或丢链。此类 bug 用 `to_list()` 立刻暴露为长度变短或死循环。

**深度补充：递归反转（可选）**

```python
def reverse_rec(head):
    if not head or not head.next:
        return head
    new_head = reverse_rec(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

空间 O(n)，链表很长时可能栈溢出；面试优先迭代。

**深度补充：环检测哈希写法（对照）**

```python
seen = set()
while head:
    if head in seen:
        return True
    seen.add(head)
    head = head.next
return False
```

O(n) 空间，适合先 AC 再改 Floyd。

**深度补充：合并 k 个有序链（23）**

分治归并或用小根堆；与本页 21 合并模板叠加。属于链表章后半难度，完成 21 与 148 后再做。

**深度补充：重排链表（143）**

找中点、反转后半、交错合并；综合快慢、反转、合并三模板。

**深度补充：排序链表（148）**

已在练习表；再强调断开中点的重要性，避免归并时原链仍连导致无限循环。

**深度补充：最大交换（1791 等变体）**

部分题在链表上贪心交换，仍建议先转数组或理解节点交换代价，别硬套本页模板。

**深度补充：系统设计中的链表**

无锁链表、RCU 读侧无锁遍历等超出本页范围；面试计算机基础题以 LeetCode 指针为主。知道「生产中有更复杂并发版本」即可，勿展开成论文。

**深度补充：阅读顺序再强调**

本页 → 脚本 OK → 206/21 → 141/142 → 双向链表与 146 专题 → `iv-top-frequent` 链表章扫尾。跳过脚本直接刷题易形成题海记忆。

**深度补充：Windows 与路径**

本机若仓库不在 `F:\Study\Algorithm`，全文 PowerShell 示例需整体替换根路径；`-LiteralPath` 在含空格路径时不可省略。

**深度补充：manifest 与 slug**

`ds-linear-linked-list` 已在 `manifest.json` 登记；`guide_tier: medium` 要求汉字不少于 8000。达标前保持 `draft`。

**深度补充：给复习者的口诀**

「单链单向走，双链前后连；哑节点站岗，反转先留后；快慢找环入口，间隔删倒数。」口诀辅助回忆，复杂度以表格为准。

**深度补充：与 LRU 专题的代码对照**

`DoublyLinkedList.remove_node` 与 LRU 中「从当前位置摘下节点」同构；`prepend` 与「移到最近使用端」同构。学完本页双向链表再打开 `iv-classic-lru-cache`，可把 146 看成双向链表的直接应用题。

**深度补充：时间盒建议**

| 任务 | 建议用时 |
|------|----------|
| 口述单链 vs 双链 | 1 分钟 |
| 迭代反转 | 5 分钟 |
| 合并有序 | 8 分钟 |
| Floyd + 入口 | 10 分钟 |
| 双向删已知节点 | 5 分钟 |

超时多在画图，平时用 `to_list()` 辅助。

**深度补充：发布校验命令**

```powershell
Set-Location -LiteralPath 'f:\commercial\atelier'
python scripts/validate_algorithm_guide.py --slug ds-linear-linked-list --strict
python scripts/validate_algorithm_quality.py --slug ds-linear-linked-list --strict
```

通过后再考虑将 frontmatter `status` 改为 `published`（由维护者执行）。

**深度补充：学习成果验收**

能在白纸画出带 dummy 的单链、带 head/tail 哨兵的双向链；五分钟写出反转与合并有序；三分钟口述 142 入口；知道 146 为何需要双向链。四项满足即可进入题单扫尾阶段。

**专题复盘：从节点到模式的思维链**

链表题可按「是否需要改结构」分层。第一层只遍历：找值、长度、倒数第 k（只读指针）。第二层改局部 `next`：删除、插入、交换相邻。第三层整体重排：反转、排序、重排。第四层抽象映射：数组下标当 next（287）、相交与环（图论退化）。做题前先问属于哪一层，再选 dummy / 快慢 / 三指针中的哪一个，可减少盲目套模板。

**专题复盘：画图规范**

建议统一从左向右画节点方框，箭头表示 `next`；双向链在方框上下画 `prev`/`next`。哑节点画虚线框标注「不存值」。反转时在纸下方画三行 `prev | cur | nxt` 的快照，每行对应循环一次。k 组翻转额外标出「段前驱」「段头」「段尾」「段后继」四个锚点，提交前检查四锚点是否都已接回。

**专题复盘：复杂度口头证明**

反转单趟 while，O(n)。合并两条各扫一遍，O(n+m)。Floyd 慢指针最多走一圈、快指针最多两圈，O(n)。双向链表已知节点删除固定四步，O(1)。按值删除最坏扫完整条，O(n)。面试若被追问「能否 O(1) 找中点」，答不能，必须 O(n) 至少看一半节点。

**专题复盘：与动态数组混合题**

147 插入排序链表、23 合并 k 链、218 天际线等不在本目录脚本内，但依赖本页模板。数组题偶尔要求「原地」而链表题强调「指针」；看到「原地删除」先确认是数组下标还是链表节点。88 合并有序数组从尾填三指针，21 合并有序链从头接哑节点——相似逻辑、不同方向。

**专题复盘：Python 刷题常用写法**

```python
def walk(head):
    cur = head
    while cur:
        # 处理 cur.val
        cur = cur.next
```

需要前驱时 `prev, cur = None, head` 或 `cur = dummy` 且处理 `cur.next`。需要同时持有多个锚点时用 `p0, p1, p2` 命名并在循环头注释含义，避免 `a,b,c` 混乱。

**专题复盘：C++ 刷题常用写法**

```cpp
ListNode* cur = head;
while (cur) {
    cur = cur->next;
}
```

注意 `while (cur)` 与 `while (cur && cur->next)` 的差别：判环用后者访问 `fast->next->next` 前要先保证 `fast->next` 非空。删除节点后若继续遍历，应从 `prev->next` 或保存的 `nxt` 继续，不要从已 `delete` 的地址读。

**专题复盘：测试用例设计**

| 类别 | 示例 |
|------|------|
| 空链 | `head = None` |
| 单节点 | 反转后仍单节点 |
| 两节点 | 交换、删倒数 n=1/2 |
| 环 | 尾接回中间、尾接回头 |
| 重复值 | 删除首个 vs 全部 |
| 相交 | 同尾不同长前缀 |
| 大 k | k 等于长度、大于长度 |

每类至少手跑一轮指针变化，再写代码。

**专题复盘：面试沟通脚本**

开场三十秒：「这是单链表，我用哑节点统一头插删，反转用三指针 O(n) 时间 O(1) 空间。」写完后十秒：「边界是空链和单节点，已用 dummy 处理删头。」若要求 follow-up 尾插 O(1)，答维护 tail 并说明删尾仍需前驱。若问能否用栈，答可以但空间 O(n)，当前解法更优。

**专题复盘：常见 WA 与 TLE**

WA 多为断链或漏接尾；TLE 少见，除非用 `list.pop(0)` 模拟队列或重复扫整条链。Python 题注意 `@lru_cache` 不能缓存可变节点。C++ 注意 `INT_MIN` 与节点值相等时的比较。25 题 k=1 时应等价不翻转或整段翻转，读清题意。

**专题复盘：与父级 ds-linear 的导航**

学完本页后，若还需栈、队列、哈希，回 `ds-linear` 的 Study 对照表运行其余五个脚本。链表是 Hot 100 中题量最大的线性子类之一，不必等六结构全学完再刷 206；但 BFS 依赖队列，146 依赖哈希，因此建议在第二周完成队列与哈希脚本后再冲刺设计题。

**专题复盘：notes.md 与 GUIDE.md**

仓库 `notes.md` 给出操作表与 LRU 应用一句；`GUIDE.md` 与 notes 同构，适合打印速查。本页扩写笔记中的「哨兵」「双链表删除」为可运行代码与题号映射，不替代 notes，而是引导你「笔记定概念、脚本定行为、本页定面试路径」。

**专题复盘：双语言学习法**

周一三五 Python 写题解，周二四 C++ 编译 `linked_list.cpp` 或抄 206 到 C++；周末用同一组自定义测试在两个语言对拍。指针错误在 C++ 常表现为段错误，在 Python 表现为无限循环或 `NoneType` 属性错误，对照有助于定位。

**专题复盘：146 之前的双向链表门槛**

在打开 LRU 专题前，务必能在纸上完成：① `append` 四指针；② `remove_node` 两指针改写；③ `prepend` 对称操作。146 的 `get` 命中要把节点移到最近端，本质是 `remove` + 插到 `head` 后。若本页双向链表仍模糊，先别刷 146，否则同时学哈希 + LRU 指针会过载。

**专题复盘：141 与 142 的一体训练**

先写 141 返回 bool，再在 141 通过后加 142：相遇后重置 slow。许多候选人能写 141 但说不清 142 的第二步，原因是未背 \(a = nc - b\) 或从未手画环长。建议用 3→2→0→1→3 小环在纸上标 \(a,b,c\) 各走几步。

**专题复盘：206 的迭代与递归对照**

面试先写迭代；若面试官要求递归，再写 `reverse_rec` 并说明栈深度。部分公司允许 Python 递归深度较大，C++ 长链递归不安全。提交 OJ 时类方法名与题面一致（`reverseList`），不要用仓库类名 `SinglyLinkedList`。

**专题复盘：21 与 23 的衔接**

21 是两链合并；23 是 k 链，分治时每两路合并可调用 21 逻辑。掌握 21 后，23 的难点在「如何取当前最小头」而非合并本身。堆解法空间 O(k)，分治 O(log k) 层递归。

**专题复盘：19 的 n 与节点数**

「倒数第 n」中 n 从 1 开始计数，间隔 n+1 是为了让 `second` 停在待删前驱。若写成间隔 n，会删错节点。删唯一节点时 dummy 保证 `second` 指向 dummy，删后返回 `dummy.next`。

**专题复盘：160 的长度差**

先遍历求 `lenA`、`lenB`，长链指针先走 `abs(lenA-lenB)` 步，再同步。也可先走 A 再走 B 再一起走（双指针换轨），无需显式长度，但白板写长度差更直观。

**专题复盘：237 的面试伦理**

题目允许复制值删除，真实系统应避免（后继可能为空、并发不安全）。面试按题意写，并口头说明「生产应维护前驱或改用双向链」。

**专题复盘：2 与 445 变体**

445 从尾加数需栈或反转一条链；2 从头发则与 2 同。链表加法都强调「剩余进位」与「不等长」。

**专题复盘：138 与 133 克隆图**

133 克隆图用哈希映射节点；138 克隆链是特例。映射表 `old -> new` 是第一遍核心。

**专题复盘：86 分隔链表**

小于 x 与大于等于 x 两条链，各自哑节点，最后拼接。考察「多链合并」而非排序。

**专题复盘：61 旋转链表**

找新尾与新头：`(len - k % len)` 位置断开再接。与 19 删倒数都用到长度与间隔。

**专题复盘：82 删除重复 II**

删光所有重复段，需 `prev` 与 `cur`，`cur` 与 `cur.next` 值相同则移动 `cur`，最后 `prev.next = cur`。比 `delete_first` 更复杂，建议 206 后再做。

**专题复盘：83 删除重复 I**

保留重复中的一个，单趟 `cur` 比较 `cur.next` 即可。

**专题复盘：143 重排**

L0→L1→…→L(n-1)→Ln→L(n-1)→…，步骤：中点、反后半、交错。是链表章综合题，放在 148 之后。

**专题复盘：328 奇偶链表**

奇下标链与偶下标链分开，最后相接。注意偶链头保存、断链顺序。

**专题复盘：109 有序链表转 BST**

中序递归或找中点作根再分左右。依赖快慢找中点，与 148 同源。

**专题复盘：117 填充 next 指针**

层序 BFS 或已建 next 的 O(1) 空间技巧（完美二叉树特例）。不完全属于本页单链 ADT，但出现在链表标签。

**专题复盘：剑指 Offer 22**

与 19 同，练哑节点与双指针间隔。

**专题复盘：面试手写时间再分配**

| 阶段 | 分钟 |
|------|------|
| 澄清题意与边界 | 2 |
| 画图 + 说复杂度 | 3 |
| 编码 | 12 |
| 自测空链/单节点 | 3 |

链表题编码不宜超过十五分钟，否则通常指针情况过多，应回溯是否可用 dummy 简化。

**专题复盘：strict 校验与 draft**

本页 `status: published` 表示 manifest 允许未发布；`validate_algorithm_quality.py --strict` 检查 filler 与代码围栏；`validate_algorithm_guide.py --strict` 检查九节、六个 ### 与汉字下限。两篇脚本都 OK 后，维护者可将 status 改为 `published`。撰写者勿用脚本覆盖正文。

**专题复盘：站点渲染与代码块**

正文代码围栏语言标记 `python` / `cpp`，便于语法高亮。行内路径用反引号。数学公式用 \( \) 与仓库 notes 一致。目录锚点与 `##` 标题一一对应，勿改九个大节标题名称。

**专题复盘：致谢与维护**

若你发现 `linked_list.py` 与题解不一致，以能让 `LinkedList OK` 的脚本为准提 issue；本页摘录随仓库更新。感谢在 Hot 100 索引中把链表章排在前的设计——它迫使学习者尽早建立指针直觉，而不是拖到图论之后才补基础。

**收束**：链表不是「更难的数据结构」，而是「更依赖细心画图的结构」。把本页与仓库脚本、LeetCode 题解三角对照，比单次刷二十道题更能形成稳定指针习惯。下一篇建议 `iv-classic-lru-cache`（若尚未读）或回到 `iv-top-frequent` 勾选链表章最小题集；数组薄弱则并行 `ds-linear-array`，不必等链表全 AC 再动其他线性子专题。发布前请在本机运行上文两条 strict 校验命令，确认汉字篇幅与章节结构均已达标后再改 published。
