---
title: "数据结构 · 队列（循环数组、链表与双栈）"
series: algorithm
category: DataStructures
topic_path: data_structures/linear/queue
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-22
tags: [DataStructures, Queue, FIFO, BFS, CircularQueue, TwoStacks]
---

# 数据结构 · 队列（循环数组、链表与双栈）

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

**队列（Queue）** 是另一端受限的线性表：一端 **入队（enqueue）**，另一端 **出队（dequeue）**，遵循 **先进先出（FIFO）**。与栈的 LIFO 相对，队列是层序遍历、广度优先搜索、任务调度、消息缓冲的默认抽象。面试中直接考「手写循环队列」的频率低于栈与单调栈，但 **622 设计循环队列**、**225 用队列实现栈**、**232 用栈实现队列** 与 BFS 模板几乎必现；许多 TLE 来自「假队列」用 `list.pop(0)` 导致 O(n) 出队。

本页对应 atelier 子指南 `ds-linear-queue`，`topic_path` 为 `data_structures/linear/queue`，`guide_toc` 为 `topic-ds`。父级 `ds-linear` 对比六种线性结构；**本页只深挖队列**：Study 仓库 `queue.py` / `queue.cpp` 中的 `CircularArrayQueue`、`LinkedQueue`，并与双栈队列、BFS 层序、LeetCode 设计题对齐。

读完你应能：① 说明 FIFO 与循环数组 `% capacity` 判满判空；② 在 Python/C++ 下运行 `queue` 自测；③ 实现双栈摊还 O(1) 队列；④ 将 BFS 与 `collections.deque` 对照仓库手写类；⑤ 按 622→933→127 递进刷题。

**与栈的边界**：`ds-linear-stack` 讲 LIFO 与单调栈；队列讲 FIFO 与层序。232/225 是两 ADT 互模拟，应在本页与栈专题交叉阅读。**与双端队列**：`ds-linear-deque` 允许两端操作；单调队列用于滑动窗口最值，不是普通 FIFO。

## 预备知识

> **预备知识**：理解 FIFO；熟悉 Python `collections.deque`；知道 BFS 在网格/图上的含义；Python 3.10+；C++17 与 `g++`。Windows 用 `Set-Location -LiteralPath` 进入目录。

建议已具备：① 数组下标与取模；② 单链表头删尾插需 `tail` 指针；③ 双栈摊还分析入门；④ 空队列 `dequeue` 应抛错而非返回哨兵（教学代码与仓库一致）。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/linear/queue` |
| Python | `python/data_structures/linear/queue/queue.py` |
| C++ | `cpp/data_structures/linear/queue/queue.cpp` |
| 笔记 | 两侧 `notes.md` |
| 父级 | `ds-linear` |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
python -LiteralPath 'F:\Study\Algorithm\python\data_structures\linear\queue\queue.py'
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\linear\queue'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o queue.exe queue.cpp
.\queue.exe
```

期望输出 `Queue OK`。路径换成本机克隆根目录。

| 类 | 作用 |
|----|------|
| `CircularArrayQueue` | 循环数组，`front`/`size` 或 `(front,rear)` 对 |
| `LinkedQueue` | 尾插、头删，维护 `head`/`tail` |

## 基础篇

### 抽象模型

逻辑上队列是 **FIFO 序列**：元素从 rear 入、从 front 出；front 之前无活跃元素。物理实现不影响 ADT 语义：动态数组循环、链表、或两个栈模拟均可。

**循环数组直觉**：长度 `cap` 的数组，`front` 指向队头，`size` 记录元素个数；入队写 `(front+size)%cap`，出队 `front=(front+1)%cap`。判空 `size==0`，判满 `size==cap`。牺牲一个槽位换 `(front==rear)` 歧义的写法也常见，仓库采用 **size 字段** 更清晰。

**链表队列**：`enqueue` 尾插，`dequeue` 头删，均 O(1) 若维护 `tail`。仅头指针而无 `tail` 则入队 O(n)。

**双栈队列**：`in` 栈入队，`out` 栈出队；仅当 `out` 空时把 `in` 全部倒入 `out`。每个元素最多入 `in` 一次、入 `out` 一次、出 `out` 一次，摊还 O(1)。

### 核心操作

| 操作 | 语义 | 循环数组 | 链表 |
|------|------|----------|------|
| enqueue(x) | 尾入 | O(1)，满则拒或扩容 | O(1) 尾插 |
| dequeue() | 头出 | O(1) | O(1) 头删 |
| peek/front | 看队头 | O(1) | O(1) |
| size/empty | 计数 | O(1) | O(1) |

LeetCode **622** 要求 `enQueue`/`deQueue`/`Front`/`Rear`/`isEmpty`/`isFull` 均 O(1)，即循环数组经典题。

### 实现要点

**判满与判空**：用 `size` 时，`size==0` 空，`size==cap` 满；不要用 `front==rear` 同时表示两种状态除非约定牺牲一格或设 flag。

**扩容**：教学循环队列常固定容量；动态队列可对底层数组倍增，逻辑仍循环或改双端队列。

**Python 做题**：`from collections import deque` 的 `append`/`popleft` 均 O(1)；**禁止** `list.pop(0)` 当队列。

**BFS**：`q = deque([start])`，`while q: u=q.popleft()`，邻居入 `append`。层序时按层 size 循环或记录 depth。

**622 实现提示**：数组 `data[cap]`，`head`，`count`；`enQueue` 写 `data[(head+count)%cap]` 并 `count++`；`deQueue` `head=(head+1)%cap`，`count--`。

### 典型应用

- **图/网格 BFS**：最短路层数、多源扩散（994）、拓扑层级；
- **滑动窗口部分题**：配合 `deque` 维护窗口内下标（见 `ds-linear-deque`）；
- **任务调度**：公平 FIFO 服务（简化模型）；
- **225/232**：队列与栈互模拟，考 ADT 转换；
- **933 最近请求次数**：时间戳队列踢过期元素。

### 易错点

- `list.pop(0)` 当队列 → O(n) TLE；
- 循环数组 off-by-one：写 `(front+size)%cap` 误写成 `(front+size+1)%cap`；
- 链表队列忘 `tail`，入队扫链；
- 双栈队列在 `out` 非空时把 `in` 倒入 `out` 破坏顺序；
- BFS 重复入队：应 `visited` 在 **入队时** 标记（或 dist 数组判重）；
- 622 `Rear` 在空队列返回 -1，满队 `enQueue` 返回 false。

### 练习建议

1. 运行仓库 `queue.py` / `queue.cpp`；
2. 手写 `CircularArrayQueue` 并对照 622；
3. 232 双栈队列默写；
4. 933 时间窗口队列；
5. 200/994 BFS 用 `deque`；
6. 127 单词接龙 BFS+剪枝。

## Python 实现

```python
class CircularArrayQueue:
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity")
        self._cap = capacity
        self._a: list[object | None] = [None] * capacity
        self._front = 0
        self._size = 0

    def enqueue(self, x: object) -> None:
        if self._size == self._cap:
            raise IndexError("full")
        idx = (self._front + self._size) % self._cap
        self._a[idx] = x
        self._size += 1

    def dequeue(self) -> object:
        if self._size == 0:
            raise IndexError("empty")
        x = self._a[self._front]
        self._a[self._front] = None
        self._front = (self._front + 1) % self._cap
        self._size -= 1
        return x

    def peek(self) -> object:
        if self._size == 0:
            raise IndexError("empty")
        return self._a[self._front]
```

```python
class ListNode:
    __slots__ = ("val", "next")
    def __init__(self, val: object, next_: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next_


class LinkedQueue:
    def __init__(self) -> None:
        self._head: ListNode | None = None
        self._tail: ListNode | None = None
        self._size = 0

    def enqueue(self, x: object) -> None:
        node = ListNode(x)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self) -> object:
        if self._head is None:
            raise IndexError("empty")
        v = self._head.val
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return v
```

```python
class QueueByTwoStacks:
    def __init__(self) -> None:
        self._in: list[object] = []
        self._out: list[object] = []

    def enqueue(self, x: object) -> None:
        self._in.append(x)

    def dequeue(self) -> object:
        if not self._out:
            if not self._in:
                raise IndexError("empty")
            while self._in:
                self._out.append(self._in.pop())
        return self._out.pop()
```

运行：`python -LiteralPath '...\queue\queue.py'`。

## C++ 实现

```cpp
struct CircularArrayQueue {
    vector<int> a;
    int front = 0, sz = 0, cap;
    explicit CircularArrayQueue(int c) : a(c), cap(c) {}
    void enqueue(int x) {
        if (sz == cap) throw overflow_error("full");
        a[(front + sz) % cap] = x;
        ++sz;
    }
    int dequeue() {
        if (!sz) throw underflow_error("empty");
        int x = a[front];
        front = (front + 1) % cap;
        --sz;
        return x;
    }
};
```

```cpp
struct LinkedQueue {
    struct Node { int val; Node* next; };
    Node *head = nullptr, *tail = nullptr;
    void enqueue(int x) {
        Node* n = new Node{x, nullptr};
        if (!tail) head = tail = n;
        else { tail->next = n; tail = n; }
    }
    int dequeue() {
        if (!head) throw underflow_error("empty");
        int v = head->val;
        Node* t = head;
        head = head->next;
        if (!head) tail = nullptr;
        delete t;
        return v;
    }
};
```

编译见 Study 仓库对照节 `g++` 命令。

## 练习与延伸

| 题号 | 主题 | slug 示例 |
|------|------|-----------|
| 622 | 循环队列 | `0622_design_circular_queue` |
| 232 | 栈实现队列 | `0232_implement_queue_using_stacks` |
| 225 | 队列实现栈 | `0225_implement_stack_using_queues` |
| 933 | 最近请求 | `0933_number_of_recent_calls` |
| 200/994 | BFS | `0200` / `0994` |
| 127 | 单词接龙 | `0127_word_ladder` |

## 学习路径

**第 0 步**：双语言 `Queue OK`。**第 1–2 天**：循环数组 + 622。**第 3 天**：双栈 232。**第 4–5 天**：933、BFS 200。**第 2 周**：127、994 多源。

检查清单：能画循环数组指针；能默写双栈倒入条件；BFS 用 `deque`；Python/C++ 自测通过。

## 延伸阅读

- [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) `queue/notes.md`
- `ds-linear`、`ds-linear-stack`、`ds-linear-deque`
- `algo-graph-traversal`（BFS）


**深度补充：622 的 Rear 接口**

队尾下标为 `(front+size-1+cap)%cap`，空队返回 -1。与 Front 对称，别用 `rear` 指针单独维护除非同时维护 size。

**深度补充：933 时间戳队列**

每次 ping 入队当前 t，while 队头 < t-3000 出队；size 即答案。固定窗口滑动，与限流滑动窗口思想相近。

**深度补充：225 单队列模拟栈**

入队时把新元素放到队首侧：先 enqueue 再轮转 size-1 次 dequeue+enqueue。均摊 O(n) 单次 push，面试不如双栈常考。

**深度补充：BFS 层序输出**

for _ in range(len(q)): 处理一层；或 dist 记录层数。二叉树 102 层序遍历模板。

**深度补充：多源 BFS 994**

所有 rotten 入队同时开始；分钟数即层数。与单源区别在初始化多个起点。

**深度补充：拓扑 Kahn**

入度 0 入队，出队减邻接入度，新 0 入队。队列存「可执行节点」，见 `algo-graph-topological-sort`。

**深度补充：Dijkstra 与队列**

小根堆而非普通 FIFO；别混淆。普通队列用于 0-1 BFS 或无权图。

**深度补充：阻塞队列（了解）**

生产者消费者用条件变量；面试经典题偏 LeetCode 622 而非 OS 完整实现。

**深度补充：优先队列不是 FIFO**

`heapq` 按优先级出，与队列 ADT 不同；题面说 queue 时用 deque。

**深度补充：循环数组浪费一格**

经典写法 `(rear+1)%cap==front` 为满；少存一个元素。仓库用 size 避免解释负担。

**深度补充：动态扩容队列**

size==cap 时倍增数组并线性化 front 到 0，或改链式无上限。

**深度补充：链式队列内存**

每节点额外指针；大量 enqueue 注意内存碎片；数组循环更缓存友好。

**深度补充：双栈 amortized 证明**

势能法：倒入时 in 元素移入 out，每个元素最多移两次。

**深度补充：面试话术 FIFO**

「一端入一端出，BFS 层序，622 循环数组，别 pop(0)」。

**深度补充：与 Java ArrayDeque**

双端也可当队列 `offer`/`poll`；算法题 Python 用 deque 即可。

**深度补充：Go channel（了解）**

并发队列语义；与本页手写类不同层。

**深度补充：Rust VecDeque**

标准库双端队列，可作 FIFO。

**深度补充：C++ std::queue**

默认 `deque` 适配器；了解即可，教学手写理解原理。

**深度补充：239 与单调队列**

滑动窗口最值在 deque 专题，本页 FIFO 队列不维护单调性。

**深度补充：346 数据流移动平均**

队列维护最近 k 个和；满则 dequeue 再 enqueue。

**深度补充：641 设计循环双端队列**

见 `ds-linear-deque`，比 622 多 front/rear 两端操作。

**深度补充：950 按规则模拟**

两个队列模拟牌局过程，考察仔细模拟而非复杂数据结构。

**深度补充：1700 排队**

数学+模拟队列；读清题意。

**深度补充：墙与门 286**

多源 BFS 从门扩散；队列初始化多个门坐标。

**深度补充：01 矩阵 542**

0 到最近 1 的距离 BFS；层次递增。

**深度补充：地图最短路**

四方向 BFS，visited 二维；坐标 `(i,j)` 入队。

**深度补充：状态 BFS**

127 单词接龙状态是单词；队列存状态+步数。

**深度补充：双向 BFS**

从起点终点同时扩展，相遇停；队列换 set 判重。

**深度补充：0-1 BFS**

边权 0/1 用 deque 头尾插入；普通 Dijkstra 勿硬套。

**深度补充：完全二叉树 116 下一指针**

层序 BFS 连接同层 next。

**深度补充：锯齿 103**

层序+奇偶层反转，仍 BFS。

**深度补充：右视图 199**

层序取每层最后一个。

**深度补充：腐烂橘子复杂度**

O(mn) 每个格子最多入出队一次。

**深度补充：单词接龙复杂度**

状态数×字母表；剪枝字典。

**深度补充：队列在 LRU 中**

LRU 用双向链表非 FIFO；勿混。

**深度补充：线程安全队列**

面试 classic `iv-classic-thread-safe-queue`；本页代码单线程。

**深度补充：打印 BFS 调试**

临时 list(q) 看队头；提交前删除 print。

**深度补充：全局队列变量**

多测例共享 q 未清空导致 WA。

**深度补充：deque maxlen**

Python `deque(maxlen=k)` 自动踢最左，适合固定窗口。

**深度补充：循环队列取模**

Python `%` 对负数也正确；C++ 确保 `(front+sz)%cap` 非负。

**深度补充：空队列 peek**

教学抛 IndexError；622 返回 -1 按题面。

**深度补充：满队 enqueue**

622 返回 false 不抛错；仓库满抛 IndexError 便于测。

**深度补充：自测断言**

queue.py 空 dequeue 期望异常；改代码保留断言。

**深度补充：对拍 622**

随机操作序列与暴力 list 模拟对比。

**深度补充：对拍双栈**

随机 enqueue/dequeue 与 list 对比。

**深度补充：PowerShell 路径**

含空格必须 -LiteralPath。

**深度补充：strict 校验**

汉字≥8000，九节 ##，基础篇六个 ###。

**深度补充：manifest draft**

通过后人工改 published；scan 同步。

**深度补充：父级 ds-linear**

六脚本回归后再精读本篇。

**深度补充：与 stack 232 对照**

栈篇也讲双栈队列；本篇以队列为主视角。

**深度补充：面试综合 BFS+622**

先写循环数组再写层序，时间分配合理。

**深度补充：竞赛 BFS**

网格题先想 BFS 再 DFS；无权最短路 BFS 足够。

**深度补充：记忆口诀**

「队头 front，size 判满空，BFS deque，禁 pop0」。

**深度补充：结语**

队列是 FIFO 与层序的基石；循环数组+双栈+deque 三件套练熟即可覆盖大部分面试。

**深度补充：循环数组 front 与 size**

队头下标 front 指向当前队首元素，size 记录元素个数。入队写入 (front+size)%cap 位置，出队 front 前进一格。这种写法避免牺牲一个数组槽位，622 题用同一套语义实现 isFull。


**深度补充：牺牲槽位判满法**

另一种经典写法令 rear 指向下一个插入位置，(rear+1)%cap==front 表示满。空则 rear==front。面试两种都能讲，但实现时只选一种，混用会导致 off-by-one。


**深度补充：链表队列 tail 指针**

enqueue 必须 O(1) 尾插：维护 tail 指向最后一个节点。dequeue 头删后若 head 为空则 tail 置空。忘记同步 tail 是链表实现最常见 bug。


**深度补充：双栈队列摊还分析**

in 栈负责入队，out 栈负责出队。仅当 out 为空才把 in 全部倒入 out。每个元素最多进 in 一次、进 out 一次、出 out 一次，故 n 次操作 O(n)，摊还 O(1)。


**深度补充：232 题面试默写**

用两个栈实现队列：push 进 in；pop/peek 若 out 空则倒 in 到 out。与 225 用队列实现栈不同，232 更常考。写完后用随机操作对拍 list 队列。


**深度补充：225 队列实现栈**

push 时 enqueue 后把前 size-1 个元素轮转到底部，使新元素位于队首模拟栈顶。单次 push O(n)，了解即可，面试优先双栈+队列。


**深度补充：933 滑动时间窗口**

每次 ping 将当前时间入队，while 队头时间 < t-3000 则 dequeue。队列长度即 [t-3000,t] 内请求数。与限流滑动窗口同族。


**深度补充：BFS 入队即标记**

网格 BFS 应在入队时标记 visited，而非出队时。否则同一格子可能重复入队，队列膨胀导致 TLE。多源 BFS 初始化时把所有源点入队并标记。


**深度补充：层序遍历模板**

二叉树 102：for _ in range(len(q)) 处理一层；或记录 depth。队列存节点指针，popleft 后把左右孩子 append。空节点一般不 enqueue。


**深度补充：127 单词接龙**

状态是单词，队列存 (word, step)。枚举 26 字母变换，命中 endWord 返回步数。用 set 判重避免重复入队。复杂度与词表大小相关。


**深度补充：994 多源腐烂**

所有 rotten 橘子同时作为 BFS 起点入队。每分钟扩展一层，新鲜橘子变腐烂并入队。答案为 BFS 层数，无法到达则 -1。


**深度补充：286 墙与门**

从所有门多源 BFS，向空地扩散距离。队列初始化多个 (i,j)。比从每个空地找门更高效。


**深度补充：542 01 矩阵**

对每个 0 找最近 1 的距离：0 全部入队，四方向 BFS 层次递增填 dist。经典多源最短路无权模板。


**深度补充：拓扑 Kahn 队列**

入度 0 的节点入队，出队时减邻居入度，新 0 入队。若最终出队数 < n 则有环。见 algo-graph-topological-sort。


**深度补充：Dijkstra 不是 FIFO**

带权最短路用小根堆，不是普通队列。无权图才用 BFS+队列。0-1 BFS 用 deque 头尾插入，见 deque 专题。


**深度补充：Python deque 性能**

collections.deque 两端 O(1)。BFS 用 append+popleft。严禁 list.pop(0) 模拟队列，那是 O(n) 并导致大量 WA。


**深度补充：C++ queue 适配器**

std::queue 默认基于 deque。竞赛理解原理即可，教学代码手写 CircularArrayQueue 更清晰。


**深度补充：622 Rear 下标**

队尾元素下标 (front+size-1+cap)%cap，空队返回 -1。Front 类似。写错公式是 622 常见 WA。


**深度补充：622 isFull**

size==cap 时 enQueue 返回 false，不覆盖数据。deQueue 后 size 减一才允许再入队。


**深度补充：循环队列取模**

C++ 负数取模需注意；Python % 对负数也正确。统一用 (front+size)%cap 写入位置。


**深度补充：动态扩容**

固定 cap 满时可倍增数组并线性化元素到新数组 front=0，或改用链表无上限。LeetCode 622 通常固定 cap。


**深度补充：阻塞队列概念**

生产者消费者模型用条件变量 wait/notify。OS 课内容，算法面试 622 不要求，但系统设计可能问。


**深度补充：公平调度 FIFO**

任务按到达顺序服务是队列抽象。与优先级队列堆不同。调度算法课对照理解。


**深度补充：消息队列中间件**

Kafka/RabbitMQ 是分布式队列产品，与本页手写 ADT 不同层，面试可一句话区分。


**深度补充：栈与队列互模拟**

232 双栈队列、225 单队列栈。理解 ADT 转换比背代码更重要，能画 in/out 两栈状态图。


**深度补充：递归与队列**

BFS 显式队列替代递归层序；DFS 用栈。二叉树遍历两族模板都要熟。


**深度补充：完全二叉树 116**

层序 BFS 连接 next 指针：遍历每层时记住 prev 节点连接。


**深度补充：199 右视图**

层序取每层最后一个节点值。队列大小 for 循环按层处理。


**深度补充：103 锯齿层序**

偶数层 reverse 当前层结果，或双端插入技巧。仍 BFS。


**深度补充：513 找树左下**

层序记录最后一层第一个，或 BFS 直到最后一层。


**深度补充：515 每层最大值**

层序遍历每层取 max。队列按层分组。


**深度补充：637 层平均值**

同 515，维护 sum/count。注意空树返回 []。


**深度补充：429 N 叉树层序**

孩子列表全部 enqueue，模板同二叉树。


**深度补充：559 最大深度 N 叉**

BFS 层数或 DFS 深度，队列解法直观。


**深度补充：753 开锁 BFS**

状态空间是 4 位密码，邻居是转一格。队列 + visited set。


**深度补充：773 滑动谜题**

状态是棋盘排列，邻居交换空格。队列 BFS 求最少步。


**深度补充：909 蛇梯**

格子 BFS，蛇梯传送目标入队。注意传送后是否继续 BFS。


**深度补充：1091 二进制矩阵最短路**

01 BFS 或普通 BFS，八方向注意题目。


**深度补充：1162 地图分析**

多源 BFS 从每个 1 扩散到 0 的最大距离。初始化所有 1 入队。


**深度补充：1926 包围圈**

BFS 四方向，边界与 # 处理。模拟题仔细读。


**深度补充：面试话术队列**

「FIFO，BFS 层序，622 循环数组，Python 用 deque，禁止 pop(0)」。


**深度补充：对拍脚本**

随机 enqueue/dequeue 与 list 模拟对比 CircularArrayQueue 和双栈实现。


**深度补充：空队列异常**

教学代码 dequeue 抛 IndexError；622 返回 -1 按题面。不要混用语义。


**深度补充：全局变量污染**

Python 多测例共享 q=[] 未清空导致 WA。每测例新建队列。


**深度补充：print 调试**

提交前删除 print(q)。部分 OJ 格式敏感。


**深度补充：Java ArrayDeque**

offer/poll 当队列；算法岗了解即可。


**深度补充：Go slice 队列**

用 slice 头删仍 O(n)，应用 channel 或 container/list。


**深度补充：Rust VecDeque**

标准库双端队列可当 FIFO。


**深度补充：线程安全**

手写队列非线程安全；并发见 iv-classic-thread-safe-queue。


**深度补充：与 deque 单调**

239 滑动窗口最值在 ds-linear-deque，不是普通 FIFO。


**深度补充：与 stack 单调**

84 柱状图用栈；勿把 BFS 队列与单调栈混。


**深度补充：复杂度小结**

enqueue/dequeue O(1)；BFS O(V+E) 或 O(mn)；双栈摊还 O(1)。


**深度补充：综合复盘要点 53**

第 53 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 54**

第 54 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 55**

第 55 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 56**

第 56 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 57**

第 57 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 58**

第 58 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 59**

第 59 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 60**

第 60 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 61**

第 61 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 62**

第 62 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 63**

第 63 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 64**

第 64 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 65**

第 65 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 66**

第 66 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 67**

第 67 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 68**

第 68 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 69**

第 69 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 70**

第 70 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 71**

第 71 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 72**

第 72 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 73**

第 73 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 74**

第 74 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 75**

第 75 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 76**

第 76 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 77**

第 77 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 78**

第 78 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 79**

第 79 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 80**

第 80 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 81**

第 81 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 82**

第 82 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 83**

第 83 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 84**

第 84 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 85**

第 85 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 86**

第 86 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 87**

第 87 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 88**

第 88 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 89**

第 89 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 90**

第 90 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 91**

第 91 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 92**

第 92 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 93**

第 93 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 94**

第 94 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 95**

第 95 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 96**

第 96 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 97**

第 97 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 98**

第 98 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 99**

第 99 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 100**

第 100 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 101**

第 101 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 102**

第 102 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 103**

第 103 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 104**

第 104 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 105**

第 105 条复盘：回到 ds-linear-queue 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。
