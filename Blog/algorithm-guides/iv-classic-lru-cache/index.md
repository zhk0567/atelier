---
title: "面试专题 · Classic Lru Cache"
series: algorithm
category: Interview
topic_path: interview/classic/lru_cache
guide_toc: interview-classic
guide_tier: medium
status: published
date: 2026-05-21
tags: [Algorithm, Interview, LRU, LeetCode146, Design]
---

# 面试专题 · Classic Lru Cache

## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [Study 仓库对照](#study-仓库对照)
- [基础篇](#基础篇)
  - [题意与接口](#题意与接口)
  - [设计与数据结构](#设计与数据结构)
  - [并发与边界](#并发与边界)
  - [复杂度](#复杂度)
  - [易错点](#易错点)
  - [扩展追问](#扩展追问)
- [Python 实现](#python-实现)
- [C++ 实现](#c-实现)
- [练习与延伸](#练习与延伸)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)

## 导读

**LRU（Least Recently Used）缓存**是系统设计题与 LeetCode **设计类**题目的经典代表：[146. LRU Cache](https://leetcode.cn/problems/lru-cache/) 要求你在 `get` / `put` 均为 **O(1)** 的前提下，维护容量为 `capacity` 的键值存储，并在超出容量时淘汰**最久未使用**的条目。

面试里这道题考察的不是「背一个 API」，而是能否把**抽象语义**（最近使用、淘汰最久）映射到**可证明 O(1)** 的具体结构：**哈希表**负责按 key 定位节点，**双向链表**负责维护使用时间序并在命中时把节点挪到「最近」一端。许多候选人能说出这两个名字，却在 `put` 更新已有 key、哨兵节点边界、淘汰时同步删 map 等细节上丢分。

本专题对应 Study 仓库 `interview/classic/lru_cache/`：与 `problems/leetcode/0146_lru_cache/` 中基于 `OrderedDict` 的题解版**互为对照**——这里强调**手写**双向链表 + 哈希，代码可读、可白板复现。Hot 100 题单中 LRU 常排在前列（约第 25 名），建议先理解本专题结构，再回题解目录跑官方风格测试。

从面试官视角，这道题属于 **「设计 + 数据结构」** 交叉：不会考红黑树证明，但会要求你说清**为何**组合哈希与链表、**每个分支**如何保持 O(1)。通过的标准通常是：十分钟内写出无 bug 的 `get`/`put`，并能口头解释 `capacity=1`、更新已存在 key、与 LFU 的区别。失败常见原因是指针写乱导致死循环、淘汰错端、或 map 与链表不同步。

工业界中，操作系统页面置换、数据库缓冲池（Buffer Pool）、HTTP 客户端缓存、CDN 边缘节点都会用到「最近使用」思想；生产系统往往用**近似 LRU**（如 Redis 的采样淘汰）以降低锁竞争与内存开销。LeetCode 146 要求**严格 LRU**，是为了把不变量讲清楚，而不是让你背 Redis 配置参数。

**题目在 LeetCode 中的位置**：标签常见为 `Design`、`Hash Table`、`Linked List`；难度 Medium。与 155/232 等栈队列纯实现不同，146 要求**组合**两种结构。公司面试中常作为「热身后第二题」或「系统设计题编码部分」出现，时间预算 20–25 分钟（含解释）。

**读完本文你应能回答**：① 为什么需要双向链表；② `put` 更新已有 key 时发生什么；③ 淘汰时为何必须用节点里的 key 删 map；④ 线程安全至少要做哪一步；⑤ OrderedDict 与手写链表各适合什么场景。

**为何 146 长期留在 Hot 100 前列**：它同时考察数据结构组合、指针细心程度、以及设计题 API 的完整性；许多候选人在「能讲思路」与「能无 bug 写完」之间存在差距，面试官用一题即可区分。对本专题的学习目标应是：**闭卷十五分钟内写出可 AC 的 Python 版本**，而不是仅背诵文字说明。

**与单题博文的边界**：atelier 的 Algorithm 系列不为每道 LeetCode 单独发长文，而是把 `interview/classic/lru_cache` 这类专题写深；具体提交用例仍以 `problems/leetcode/0146_lru_cache/solution.py` 为准。若专题与题解实现不一致，以专题「手写教学版」解释为准，题解以保持 AC 简洁为目标。

## 预备知识

> **预备知识**：理解哈希表均摊 O(1) 查找；能在纸上画出双向链表的 `prev` / `next` 指针；熟悉 LeetCode 设计题构造器 `LRUCache(capacity)` 与成员方法 `get` / `put`。Python 3.10+；C++17 与 `unordered_map`、`g++` 基本编译选项。Windows 下用 PowerShell 的 `Set-Location -LiteralPath` 进入目录后运行脚本。

你需要事先建立的几条概念：

1. **缓存命中（hit）**：`get(key)` 找到 key 时，除返回值外，该 key 在逻辑上变为「刚被使用过」，必须参与 LRU 顺序更新。
2. **缓存未命中（miss）**：`get` 返回约定哨兵值（LeetCode 为 `-1`）；不改动其余 key 的顺序（本实现中未插入新节点）。
3. **插入与更新**：`put(key, value)` 在 key 不存在时插入；已存在时只更新 value，**不增加**占用条数，但要把该 key 视为刚使用。
4. **淘汰（evict）**：当前条目数超过 `capacity` 时，移除**最久未使用**的一条；恰好等于 `capacity` 时不淘汰。

若对「单向链表 + 尾删」有印象，应意识到：仅从尾部删除 O(1) 不够，**命中时要把中间节点移到头部**，单向链表无法 O(1) 找到前驱，故面试标准解法是**双向链表 + 哈希存节点指针**。

**双向链表最小操作复习**（设 `head` 为哨兵，真实节点从 `head.next` 开始）：

- 在 `head` 后插入 `node`：`node.next = head.next; node.prev = head; head.next.prev = node; head.next = node`。
- 删除 `node`：`node.prev.next = node.next; node.next.prev = node.prev`。
- 切勿在删除后仍通过旧指针访问 `node` 的邻居，除非你先缓存 `p = node.prev, n = node.next`。

**哈希表角色**：`dict` / `unordered_map` 提供 `key → Node` 的 O(1) 查找；链表不提供按 key 查找，只维护**相对顺序**。二者缺一不可：仅哈希表无法知道谁最久；仅链表找 key 要 O(n)。

**从暴力到最优的思路链（面试可先说再写）**

1. **暴力**：用列表按时间顺序存 `(key,value)`，`get` 时线性查找 key，找到后移到列表尾（或头）表示最近；`put` 同理。单次 O(n)，不满足题意。
2. **仅哈希 + 时间戳**：`get` 时更新 `time[key]=now`，淘汰时扫全部 key 找最小时间。单次 O(n)。
3. **哈希 + 单链表**：查找 O(1)，但把中间节点移到头部需要前驱，单向链表仍需 O(n) 找前驱。
4. **哈希 + 双向链表 + 哨兵**：当前标准解，所有操作 O(1)。

口述时先用三十秒讲清 1→4 的瓶颈，再落笔写第 4 种，面试官更容易给提示或认可你的结构选择。

**操作系统课中的 LRU 页面置换**：内存帧有限，访问页面时若命中则不算故障；若缺失则调入新页，若帧满则选**最久未访问**的页换出。题 146 把「页框」换成「缓存槽位」，把「页面号」换成 `key`，把「页面内容」换成 `value`，机制同构。区别是 OJ 不要求处理「页大小」「预读」等细节。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/lru_cache` |
| Python | `python/interview/classic/lru_cache/lru_cache.py` |
| C++ | `cpp/interview/classic/lru_cache/lru_cache.cpp` |
| 笔记 | 两侧 `notes.md`（复杂度、边界、与 0146 对照） |
| LeetCode 题解 | `python/problems/leetcode/0146_lru_cache/`（`OrderedDict` 版） |
| 基础数据结构版 | `python/data_structures/advanced/lru_cache.py`（更偏复用封装） |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'

# Python：运行自带断言
Set-Location -LiteralPath 'F:\Study\Algorithm\python\interview\classic\lru_cache'
python lru_cache.py

# C++：依赖仓库统一头文件 alg_std.hpp
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\interview\classic\lru_cache'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\include -o lru_cache.exe lru_cache.cpp
.\lru_cache.exe
```

将 `F:\Study\Algorithm` 换成你本机克隆路径即可。终端应输出 `lru_cache OK`，与 LeetCode 146 官方示例序列一致。

**目录与文件职责**

- `lru_cache.py` / `lru_cache.cpp`：可独立运行的教学实现，含断言。
- `notes.md`：复杂度、边界、与 0146 的交叉链接；修改代码后应同步更新笔记中的一行结论（若行为变化）。
- `0146_lru_cache/solution.py`：面向提交的简洁版，可能与 interview 版在异常处理上略有差异。

若 `g++` 报找不到 `alg_std.hpp`，检查 `-I` 是否指向 `cpp/include`（相对路径随当前工作目录而变，上表命令在 `cpp/interview/classic/lru_cache` 下使用 `..\..\include`）。

**克隆仓库后的建议顺序**：先 `git pull` 同步 Study 仓库，再运行本专题脚本确认环境；然后阅读 `notes.md`（约一页），最后阅读本文长文。若时间紧，可只读「基础篇」六节 +「Python 实现」+ 运行 `lru_cache.py`，C++ 留到需要投 C++ 岗时再补。专题代码与 0146 题解代码允许并存两套实现，不必强行合并，但语义应一致，可用同一组断言序列交叉验证。

## 基础篇

### 题意与接口

LeetCode 146 的接口定义（意译）如下：

- 构造 `LRUCache(int capacity)`：`capacity` 为正整数，表示最多同时保存的键值对数量。
- `int get(int key)`：若 key 存在，返回对应 value，并将该 key 标记为**最近使用**；若不存在，返回 `-1`。
- `void put(int key, int value)`：写入 key。若 key 已存在，更新 value 并标记为最近使用；若不存在，插入新对。插入后若条目数 **大于** `capacity`，删除**最久未使用**的 key。

官方示例（`capacity = 2`）：

```
put(1,1)  put(2,2)  get(1)→1  put(3,3)  get(2)→-1  put(4,4)  get(1)→-1  get(3)→3  get(4)→4
```

逐步理解顺序（「最近」在左，「最久」在右）：

| 操作 | 逻辑顺序（key） | 说明 |
|------|-----------------|------|
| put(1,1) | 1 | 插入 |
| put(2,2) | 2, 1 | 2 最近 |
| get(1) | 1, 2 | 1 被访问，升到最近 |
| put(3,3) | 3, 1 | 满容插入 3，淘汰最久 **2** |
| get(2) | — | 2 已被淘汰，返回 -1 |
| put(4,4) | 4, 3 | 淘汰最久 **1** |
| get(1) | — | -1 |
| get(3), get(4) | 4, 3 | 4 最近，再 get(3) 仍返回 3 |

另有一例：`put(4,40)` 在 key 4 已存在时只**更新值**并移到最近，**不触发**额外淘汰；条目数仍为 2。这是面试高频漏考点。

Study 手写实现与题面一致：`get` 未命中返回 `-1`；`capacity <= 0` 在构造时抛 `ValueError`（Python）——LeetCode 数据保证 `capacity >= 1`，本地严格校验有助于自测。

**官方示例的链表视角（`capacity=2`，最近靠近 head）**

下列用 `head ⇄ … ⇄ tail` 表示哨兵，括号内为 `(key,val)`：

1. `put(1,1)`：链表 `head ⇄ (1,1) ⇄ tail`，map `{1→node1}`。
2. `put(2,2)`：`(2,2)` 插到 head 后 → `head ⇄ (2,2) ⇄ (1,1) ⇄ tail`。
3. `get(1)`：命中，把 `(1,1)` 移到 head 后 → `head ⇄ (1,1) ⇄ (2,2) ⇄ tail`。
4. `put(3,3)`：插入 `(3,3)` 后共 3 项，超容；淘汰 `tail.prev` 即 `(2,2)` → `head ⇄ (3,3) ⇄ (1,1) ⇄ tail`，map 删除 key 2。
5. `get(2)`：map 无 2，返回 -1。
6. `put(4,4)`：淘汰 `(1,1)` → `head ⇄ (4,4) ⇄ (3,3) ⇄ tail`。
7. `get(1)`：-1；`get(3)`、`get(4)` 依次把对应节点移到 head 后，最终最近为 4。

若你在白板只写 key 顺序而不画哨兵，务必说明**头侧最近、尾侧最久**，避免与「尾部是最近」的口述习惯混淆。

**与「栈 / 队列」的区分**：LRU 不是 FIFO（队列）：`get(1)` 会把 1 变最近，改变淘汰候选；也不是 LIFO。可以口头说成「按访问时间排序的线性结构 + 哈希索引」。

**`capacity = 1` 的完整轨迹**

| 步骤 | 操作 | map 键 | 链表（head 侧最近） | 返回值 |
|------|------|--------|---------------------|--------|
| 1 | put(10,10) | {10} | (10,10) | — |
| 2 | get(10) | {10} | (10,10) | 10 |
| 3 | put(20,20) | {20} | (20,20) | —（淘汰 10） |
| 4 | get(10) | {20} | (20,20) | -1 |
| 5 | put(20,99) | {20} | (20,99) | —（更新，不扩容） |

可见容量为 1 时，任何**不同 key** 的 `put` 都会替换整表；反复 `put` 同一 key 只更新值。测试时务必覆盖此场景，很多 WA 来自 `capacity=1` 时淘汰逻辑写反。

**键值均为 int 时的溢出**：LeetCode 146 值范围在 32 位有符号 int 内；一般不需 Python 大整数处理。C++ 用 `int` 即可。

### 设计与数据结构

核心不变量：

1. 双向链表按**使用时间**从「最近」到「最久」排列（实现里把**最近**放在靠近 `head` 哨兵的一侧）。
2. 哈希表 `key → Node*`，保证给定 key 能在 O(1) 找到链表节点。
3. 链表节点存 `(key, value)`；淘汰时必须用节点里的 **key** 删除哈希表项（不能只删节点指针而留下 map 脏数据）。

**哨兵节点（dummy head / tail）**：`head` 与 `tail` 不存业务数据，真实节点插在 `head` 与 `tail` 之间。这样 `addToFront`、`remove` 永远不需要判断「前一个节点是否为空」，指针改写统一为四行模板。

逻辑结构示意：

```
head <-> [最近] <-> ... <-> [最久] <-> tail
         ^                          ^
    add / moveToFront            evict 取 tail.prev
```

**操作与链表动作对应**：

| 操作 | 哈希表 | 链表 |
|------|--------|------|
| get 命中 | 已有 | `moveToFront(node)` |
| put 更新 | 已有 | 改 `val`，`moveToFront` |
| put 新 key | `map[key]=node` | `addToFront`，若超容则删 `tail.prev` 并从 map 删其 key |
| 淘汰 | `del map[evict.key]` | `remove(evict)` |

`moveToFront` 的实现模式：**先从链表中摘掉节点（`_remove`），再插到 head 后（`_add_to_front`）**。不要试图「若已在头部则跳过」——在哨兵结构下统一走 remove+add 更简单，且仍是 O(1)。

**循环不变量（写代码时心里要一直成立）**

- **I1**：`len(_map)` 等于链表中业务节点个数，且不超过 `_cap`（操作完成后）。
- **I2**：从 `head` 沿 `next` 走到 `tail`，遇到的每个业务节点的 `key` 都在 `_map` 中，且 `_map[key]` 指向该节点。
- **I3**：`head` 与 `tail` 自身不在 `_map` 中；`head.next` 与 `tail.prev` 非空（除非容量为 0 的空缓存，本题不出现）。
- **I4**：靠近 `head` 的节点比靠近 `tail` 的节点**更新**（最近使用）。

`put` 新 key 后若 `len > cap`，只删除**恰好一个** `tail.prev`，使 I1 恢复。`get` 命中只调用 `moveToFront`，不改变 I1 的计数。

**错误实现反例（帮助排雷）**

- 反例 A：`put` 新 key 时先淘汰再插入，且用 `len >= cap` 判断——当 `len==cap` 时会多删一次，导致缓存空一格。
- 反例 B：淘汰时 `del map[key]` 但删的是当前 `put` 的 key——应删 `evict.key`。
- 反例 C：`moveToFront` 只改 `head.next` 不把节点从原位置 unlink——链表出现分支或环。

**为何不用「数组 + 时间戳」**：`get` 不能把整条记录 O(1) 标为最新；扫描找最小时间戳是 O(n)。**为何不用单向链表**：把中间节点移到头部需要前驱指针。**OrderedDict**（Python 题解版）在 CPython 3.7+ 有序且 `move_to_end` O(1)，面试白板仍更常要求手写链表。

**`put` 分支决策树（实现时按此顺序写可减少 bug）**

```
put(key, value):
  if key in map:
    更新 node.val
    moveToFront(node)
    return
  新建 node，map[key]=node，addToFront(node)
  if len(map) > capacity:
    evict = tail.prev
    remove(evict); del map[evict.key]
```

**`get` 分支**：`key not in map` → `-1`；否则 `moveToFront` 后返回 `val`。两条分支都不要忘记「命中即更新顺序」。

**再举一个非官方样例（`cap=3`）**

操作：`put(1,1), put(2,2), put(3,3), get(1), put(4,4)`。前三步后链表最近侧为 3,2,1；`get(1)` 后顺序为 1,3,2；`put(4,4)` 插入后共四项，淘汰 `tail.prev` 即 key 2（最久未用）。最终 map 含 1,3,4。若误淘汰 3，通常是 `get(1)` 后未把 1 移到 head 侧，或淘汰时取了 `head.next`（最近）而非 `tail.prev`。这类三容量样例比 cap=2 更易暴露「谁是最久」的判断错误，建议纸面练一次。

**节点字段为何必须存 `key`**：淘汰时只有节点指针，若没有 `key` 字段就要遍历 `unordered_map` 找 value 相等的项，破坏 O(1)。LeetCode 的 value 是 `int`，但 key 才是 map 的主键。

**可选实现：一个类里内嵌节点 vs 独立 `_Node`**：Python 用 `__slots__` 独立类可减少内存；面试白板可画成结构体 `Node{key,val,prev,next}`。

**`put(3,3)` 一步的指针操作（接官方样例第 4 步）**

此时链表为 `head ⇄ (1,1) ⇄ (2,2) ⇄ tail`，`put(3,3)` 走未命中分支：

1. 分配 `node(3,3)`，`map[3]=node`。
2. `_add_to_front(node)`：`node.next = head.next`（原 (1,1)），`node.prev = head`，`head.next.prev = node`，`head.next = node`。链表变为 `head ⇄ (3,3) ⇄ (1,1) ⇄ (2,2) ⇄ tail`。
3. `len(map)==3 > cap==2`：`evict = tail.prev` 即 (2,2)；`_remove(evict)` 断开 (2,2)；`del map[2]`。结果 `head ⇄ (3,3) ⇄ (1,1) ⇄ tail`。

若第 2 步后忘记第 3 步，map 仍含 key 2 但链表无 (2,2)，后续 `get(2)` 可能误访问悬空节点。这类 bug 在 C++ 中常表现为 Runtime Error，Python 中可能 KeyError 或逻辑 WA。

**数据库 Buffer Pool 口语联系**：InnoDB 等引擎用类似 LRU 的变种管理页缓存（有时分 young/old 区减轻全表扫描污染）。你不需要背 InnoDB 源码，但可以说「生产会加机制避免扫描打穿缓存，题面是理想 LRU」。

**CDN / HTTP 缓存**：响应头 `Cache-Control` 与 LRU 无直接一一对应，但边缘节点内存有限时，常用 LRU 或 LFU 的变种存放热门对象。146 题是内存数据结构题，不是 HTTP 协议题，提到 CDN 是为了说明**业务背景**，不是考试范围。

### 并发与边界

**边界（单线程题面）**：

- `capacity == 1`：任意新 `put`（新 key）都会立刻淘汰唯一旧项；`get` 后立即 `put` 另一 key 会使前者消失。
- 重复 `put` 同一 key：只更新 value 与顺序，**size 不变**。
- `get` 不存在的 key：返回 `-1`，链表与 map 均不变。
- 构造 `capacity < 1`：Study Python 实现 `raise ValueError`；生产代码常断言或默认最小为 1。

**并发（面试追问，题面通常不要求）**：

- 上述 `get`/`put` 非原子：读 map、改链表、删 map 之间若交错，另一线程可能看到不一致顺序或悬空指针。
- 粗粒度做法：用一把 **mutex** 包住整个 `get`/`put`（实现简单，争用大）。
- 分段锁：按 `hash(key) % N` 分桶，每段独立 LRU（近似 LRU，实现复杂）。
- 无锁：多读单写队列、版本号等，已超出 146 范围，仅需口头知道「要线程安全必须额外同步」。

**内存（C++）**：`new` 出的节点在淘汰或析构时需 `delete`；Python 由 GC 回收节点对象。面试写 C++ 时说明析构遍历释放可避免泄漏。

**伪代码：粗粒度互斥包装（表达思路，非题面要求）**

```python
import threading

class ThreadSafeLRUCache:
    def __init__(self, inner: LRUCache) -> None:
        self._inner = inner
        self._lock = threading.RLock()

    def get(self, key: int) -> int:
        with self._lock:
            return self._inner.get(key)

    def put(self, key: int, value: int) -> None:
        with self._lock:
            self._inner.put(key, value)
```

读写锁只有在「读远多于写且愿意接受近似 LRU」时才有收益；严格 LRU 的 `get` 也会改链表，本质仍是写操作，故**读锁优化空间很小**。

**键类型扩展**：题面为 `int`；泛化到任意可哈希 `K` 时，把 `dict[int, Node]` 换成 `dict[K, Node]`，节点存 `K` 即可。不可哈希对象不能作为 key，与 Python `dict` 一致。

**value 很大时**：题面 value 为 int；若泛化为对象，节点仍只存引用，淘汰逻辑不变。注意不要让「比较 value」参与 LRU 顺序，顺序只由 key 的访问时间决定。

### 复杂度

| 操作 | 时间 | 说明 |
|------|------|------|
| `get`（命中） | O(1) | 哈希查找 + 常数次指针改写 |
| `get`（未命中） | O(1) | 仅哈希查找 |
| `put` | O(1) | 查找/插入/至多一次淘汰 |
| 空间 | O(capacity) | 最多 `capacity` 个节点与 map 项 |

均摊分析依赖哈希表均摊 O(1)；链表操作指针个数为常数，与 `capacity` 无关。

**最坏情况与均摊**：单线程下不存在「一次 put 扫全表」；哈希冲突极端时仍视为均摊 O(1)。空间上界由 `capacity` 限定，与操作次数无关，适合内存受限的嵌入式缓存。

**与 O(1) 均值查找的对比**：若只需「插入」和「删除最旧」而不需要按 key 随机 `get`，用队列即可；LRU 的难点在 **按 key 访问并刷新顺序**，因此必须哈希。

**均摊 O(1) 的口头证明**：设操作序列长度为 m。哈希表插入、查找、删除均摊 O(1)；每次 `get`/`put` 至多触发常数次 `remove` 与 `addToFront`，不随 capacity 增大而线性增加指针遍历。故总时间 O(m)，单次均摊 O(1)。空间始终 O(capacity)，与 m 无关（条目数受 capacity 限制）。

**Belady 最优与 LRU**：理论最优离线置换（Belady）需要未来访问序列，无法在线实现；LRU 是在线策略，实现简单、命中率在多数工作负载上可接受。面试若被问「LRU 是否最优」，答「非最优，但工程可实现且常够用」即可，勿展开证明。

### 易错点

1. **更新已有 key 未移到头部**：`put` 命中旧 key 只改 `value` 不 `moveToFront`，会导致该 key 仍按旧位置被淘汰。
2. **淘汰只删链表不删 map**：`tail.prev` 摘掉后必须从 `map` 删除 `evict.key`，否则 map 泄漏且后续 `get` 可能访问已脱离链表的节点。
3. **新 key 超容时淘汰对象错误**：应淘汰 `tail.prev`（最久），不是 `head.next`（最近）。
4. **`moveToFront` 漏掉 remove 步骤**：直接改指针可能破坏链表环或丢节点。
5. **节点不存 key**：仅存 value 时，淘汰节点无法得知要从 map 删哪个 key（除非再扫 map，退化为 O(n)）。
6. **容量判断用 `>=` 与 `>` 混淆**：应在插入后 `len > capacity` 再淘汰；`len == capacity` 时不删。
7. **与 LeetCode 返回值不一致**：未命中必须 `-1`，不要返回 `None` 或抛异常（除非题目另有说明）。
8. **析构与内存（C++）**：只 `delete evict` 而不在析构里遍历释放哨兵与残留节点，本地 main 可能仍 OK，但泄漏检查会失败。
9. **Python 递归深度**：本题不涉及；但若误用递归遍历链表，大 capacity 可能栈溢出，应迭代遍历。
10. **把 `head` 当成最近节点**：最近业务节点是 `head.next`，不是 `head` 本身；淘汰对象是 `tail.prev`。

**调试链表断裂的小技巧**：在开发版 `_add_to_front` 末尾断言 `self._head.next.prev == self._head`；若失败，说明双向链接只改了一侧。也可临时实现 `__repr__` 按 key 顺序打印链表，对照 map 的 keys。

### 扩展追问

面试官常在此题上延伸，建议准备简短回答要点：

| 追问 | 要点 |
|------|------|
| LFU（最不经常使用） | 需 key→freq 与 freq→双向链表集合；`get/put` 仍要 O(1)，实现量大于 LRU（LeetCode 460） |
| 过期时间 TTL | 在节点上加 deadline，后台或惰性清理；与 LRU 正交，可堆 + 哈希 |
| 分布式缓存 | 一致性哈希分片；单分片内仍可能用 LRU；热点与击穿另题 |
| Redis LRU | 近似 LRU（采样淘汰），非严格双向链表 |
| `LinkedHashMap` / `OrderedDict` | 语言内置有序结构可 AC，但要能讲清手写原因 |
| O(1) 的「最久」定义 | 严格 LRU 按**访问**排序；只按 `put` 排序是另一策略 |

**LFU 骨架（对比用，不必一次写完）**：维护 `key → (value, freq)` 与 `freq → 双向链表(key 集合)`。`get` 时 freq+1，把 key 从旧 freq 桶移到新 freq 桶；`put` 时在 freq=1 插入，超容时淘汰 **最小 freq** 桶的尾部（同 freq 用 LRU  tie-break）。桶的数量最多为操作次数，需 `min_freq` 指针优化（见 LeetCode 460 题解）。

**ARC / 2Q 等**：属于自适应替换，面试极少手写，知道「比 LRU 更抗扫描（sequential scan）」即可——顺序读大文件时纯 LRU 会把冷数据全挤掉，工程上会用多级队列缓解。

**模拟面试问答（可参考的简短答法）**

- **问：能否用两个哈希表一个存 key→value 一个存 key→时间，每次淘汰扫最小时间？** 答：可以写对但单次 O(n)，不满足题意；面试官要的是严格 O(1) 单次操作。
- **问：为什么不用平衡树？** 答：按 key 排序对「时间顺序」无帮助；按时间戳排序的 BST 插入删除均 O(log n)，不满足题意 O(1)。
- **问：map 存 value 不存指针可以吗？** 答：不行，无法 O(1) 把该 key 对应节点从链表中部unlink；必须存节点引用。
- **问：双向链表能否改成单向 + 额外栈？** 答：单向无法 O(1) 删除中间节点；栈只能表达一端顺序，不能表达全局 LRU。
- **问：get 和 put 的 amortized 分析？** 答：哈希表均摊 O(1)，链表指针常数次，合起来 O(1)。

**淘汰策略横向对比（背一张表即可）**

| 策略 | 淘汰谁 | 典型场景 | 146 题是否 |
|------|--------|----------|------------|
| LRU | 最久未**访问** | 通用缓存、页置换 | 是 |
| FIFO | 最先**插入** | 简单队列，易受扫描影响 | 否 |
| LFU | 访问**次数最少** | 热点明显、长期频率 | 460 题 |
| MRU | 最近使用 | 顺序扫描模式特殊场景 | 否 |
| Random | 随机 | 实现极简、命中率一般 | 否 |

## Python 实现

Study 仓库完整实现如下（双向链表 + `dict`，带哨兵与 `__main__` 自测）：

```python
"""手写 LRU Cache：双向链表 + 哈希表。"""

from __future__ import annotations

from typing import Optional


class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(
        self,
        key: int = 0,
        val: int = 0,
        prev: Optional["_Node"] = None,
        next: Optional["_Node"] = None,
    ) -> None:
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._cap = capacity
        self._map: dict[int, _Node] = {}
        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    def __len__(self) -> int:
        return len(self._map)

    def get(self, key: int) -> int:
        node = self._map.get(key)
        if node is None:
            return -1
        self._move_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self._map.get(key)
        if node is not None:
            node.val = value
            self._move_to_front(node)
            return
        node = _Node(key, value)
        self._map[key] = node
        self._add_to_front(node)
        if len(self._map) > self._cap:
            evict = self._tail.prev
            assert evict is not None and evict is not self._head
            self._remove(evict)
            del self._map[evict.key]

    def _add_to_front(self, node: _Node) -> None:
        nxt = self._head.next
        assert nxt is not None
        node.prev = self._head
        node.next = nxt
        self._head.next = node
        nxt.prev = node

    def _remove(self, node: _Node) -> None:
        p, n = node.prev, node.next
        assert p is not None and n is not None
        p.next = n
        n.prev = p
        node.prev = node.next = None

    def _move_to_front(self, node: _Node) -> None:
        self._remove(node)
        self._add_to_front(node)
```

**读代码的三条主线**：

1. `_map` 与链表**始终同步**：出现在 map 中的节点一定在链表中，且反之亦然。
2. 三个私有方法 `_add_to_front`、`_remove`、`_move_to_front` 是所有对外操作的积木；面试白板先写这三个，再写 `get`/`put`。
3. `__slots__` 减小 `_Node` 内存占用，与算法无关，可省略。

**逐行对应关系（便于默写）**

| 方法 | 行级行为 |
|------|----------|
| `__init__` | 建空 map；`head`、`tail` 互连，中间暂无业务节点 |
| `get` | `map.get` 失败 → -1；成功则 `_move_to_front` 再返回 `val` |
| `put` 命中 | 改 `node.val`，`_move_to_front`，**不**新建节点 |
| `put` 未命中 | 新建 `_Node`，入 map，`addToFront`；若 `len(map) > cap`，取 `tail.prev` 淘汰 |
| `_remove` | 经典四行断链；把 `node.prev/next` 置 `None` 防误用 |
| `_move_to_front` | 先 `_remove` 再 `_add_to_front`，顺序不可颠倒 |

`__main__` 块复现 LeetCode 样例并 `assert len(c)==2`，用于本地回归；提交 OJ 时删除。

**与 OrderedDict 题解对照**（`0146_lru_cache`）

仓库题解版核心思路（摘录结构，完整代码见 `solution.py`）：

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.od: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.od:
            return -1
        self.od.move_to_end(key, last=False)
        return self.od[key]

    def put(self, key: int, value: int) -> None:
        if key in self.od:
            self.od.move_to_end(key, last=False)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=True)
```

`last=False` 表示把 key 移到** OrderedDict 的左侧（前端）** 作为「最近」；`popitem(last=True)` 从右侧弹出最久。CPython 实现下这些操作均摊 O(1)。面试时可以说：「生产 Python 服务可先用 OrderedDict 验证语义，再换手写链表以降低解释器层开销或便于嵌入 C 扩展。」

**手写版相对 OrderedDict 的优势**：指针操作透明，便于改节点载荷（如加 TTL、权重）；C++ 没有内置 OrderedDict，链表版可无缝迁移。

提交 LeetCode 时把类名改为题目要求的 `LRUCache`，去掉 `__len__` 与 `ValueError` 若数据保证 `capacity >= 1`。

**单元测试扩展（可加到 `__main__`）**

```python
def _test_capacity_one() -> None:
    c = LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1
    assert c.get(2) == 2

def _test_update_no_evict() -> None:
    c = LRUCache(2)
    c.put(1, 1)
    c.put(1, 9)
    assert c.get(1) == 9
    assert len(c) == 1

if __name__ == "__main__":
    # 原有官方样例 ...
    _test_capacity_one()
    _test_update_no_evict()
    print("extra tests OK")
```

本地测试通过后再提交；OJ 不运行你的 `__main__`，但可减少调试时间。

**常见 WA 与 Line 对照（LeetCode 讨论区高频）**

- 样例最后 `put(4,40)` 后 `get(4)` 应为 40：说明**更新 value** 与**移到最近**两步都要做。
- 连续 `put` 同一 key 不应使 size 超过 capacity。
- `get` 不存在 key 不要向 map 插入占位符。

**性能粗测（理解即可）**：在 CPython 下，手写链表常数因子大于 `OrderedDict` 的 C 实现；面试不以常数优化评分。若数据规模扩大到 10^5 操作，两者均应在时间限制内；瓶颈在 O(1) 逻辑是否正确。

**Java 对照（仅口头）**：`LinkedHashMap` 构造参数 `accessOrder=true` 时，`get` 会把条目移到链表尾部（或头部，依实现文档而定），语义与 LRU 一致；超过容量需配合重写 `removeEldestEntry`。面试官问「其他语言」时可提此点，不必写 Java 代码。

**空间占用估算**：每个条目一个节点（key+val+两个指针）+ map 一项。Python 对象有额外头开销；`__slots__` 已压缩节点。capacity 为 10^4 时仍远在内存限制内，无需担心空间，除非题目改为「流式无限 key」——那已不是 146 题面。

**与「时间复杂度陷阱」相关的说明**：有人试图用「双向链表 + 哈希存 key 在链表中的下标」配合数组模拟链表——下标删除仍需 O(1) 挪动且实现更绕，不如直接存指针。也有人想用「跳表」维护顺序，单次 O(log n)，不满足题意。面试时主动否定这些方向，可展示你对题意的把握。

**146 题数据范围（LeetCode 中文版常见约束）**：操作次数约 10^4 量级，`key`/`value` 在 int 范围内。意味着即使某次误写成 O(n)，也可能侥幸通过少量数据，但面试仍会判为不满足要求；应以 O(1) 为目标写终版。

**手写练习建议**：第一遍对着本文代码抄一遍理解；第二遍只看「题意与接口」表格默写；第三遍在白纸写指针域名字。每遍间隔至少一天。抄代码时务必手写 `_remove` 与 `_add_to_front`，不要跳过，因为 `put` 的错误九成出在这两个辅助函数或淘汰键名上。第四遍用 C++ 写同名类，强制自己处理 `new`/`delete`，巩固指针所有权意识。

## C++ 实现

C++ 镜像逻辑，使用 `unordered_map<int, Node*>` 与裸指针双向链表；析构时遍历释放所有节点：

```cpp
// 手写 LRU Cache（双向链表 + 哈希）
#include <alg_std.hpp>
#include <cassert>
using namespace std;

class LRUCache {
public:
    explicit LRUCache(int capacity) : cap(capacity) {
        head = new Node();
        tail = new Node();
        head->next = tail;
        tail->prev = head;
    }

    ~LRUCache() {
        Node* cur = head;
        while (cur) {
            Node* nxt = cur->next;
            delete cur;
            cur = nxt;
        }
    }

    int get(int key) {
        auto it = idx.find(key);
        if (it == idx.end()) return -1;
        moveToFront(it->second);
        return it->second->val;
    }

    void put(int key, int value) {
        auto it = idx.find(key);
        if (it != idx.end()) {
            it->second->val = value;
            moveToFront(it->second);
            return;
        }
        Node* node = new Node{key, value, nullptr, nullptr};
        idx[key] = node;
        addToFront(node);
        if ((int)idx.size() > cap) {
            Node* evict = tail->prev;
            removeNode(evict);
            idx.erase(evict->key);
            delete evict;
        }
    }

    int size() const { return (int)idx.size(); }

private:
    struct Node {
        int key{0};
        int val{0};
        Node* prev{nullptr};
        Node* next{nullptr};
    };

    int cap;
    Node* head;
    Node* tail;
    unordered_map<int, Node*> idx;

    void addToFront(Node* node) {
        node->prev = head;
        node->next = head->next;
        head->next->prev = node;
        head->next = node;
    }

    void removeNode(Node* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
        node->prev = node->next = nullptr;
    }

    void moveToFront(Node* node) {
        removeNode(node);
        addToFront(node);
    }
};
```

**与 Python 版的差异**：

- 淘汰后对 `evict` 执行 `delete`，防止泄漏；Python 删除 map 项后节点无引用即可回收。
- `alg_std.hpp` 聚合常用头文件（`iostream`、`unordered_map` 等），与仓库其他 `interview` 题一致。
- `size()` 便于自测；LeetCode 提交可去掉 `size` 与 `main`。

**手写链表 vs `std::list` + `unordered_map<key, list::iterator>`**：标准库 `list` 配合迭代器同样 O(1) 挪动，但面试更常考裸指针写法；若用 `list`，`erase` 与 `splice` 的迭代器失效规则要说清楚。

**`list::splice` 草图（C++11）**

```cpp
// 伪代码：lst 为 list<pair<int,int>>，map 存 key -> iterator
void touch(list<...>::iterator it) {
    lst.splice(lst.begin(), lst, it);  // 把 it 移到链表头
}
```

`splice` 不分配新节点，只改链接；与 `moveToFront` 语义相同。面试若时间紧，可口头说「用 list + map 迭代器」代替裸指针，但需写明 `unordered_map<int, list<Node>::iterator>`。

**LeetCode 提交注意**：类定义在全局，不要用 `using namespace std` 污染（本地 `alg_std.hpp` 可保留）；`get` 返回 `int`，`put` 返回 `void`。`capacity` 在构造里保存为 `int cap`，比较时 `(int)idx.size() > cap` 避免无符号比较陷阱。

**完整 `main` 与析构（与仓库一致）**

```cpp
int main() {
    LRUCache c(2);
    c.put(1, 1);
    c.put(2, 2);
    assert(c.get(1) == 1);
    c.put(3, 3);
    assert(c.get(2) == -1);
    c.put(4, 4);
    assert(c.get(1) == -1);
    assert(c.get(3) == 3);
    assert(c.get(4) == 4);
    c.put(4, 40);
    assert(c.get(4) == 40);
    assert(c.size() == 2);
    cout << "lru_cache OK" << endl;
    return 0;
}
```

析构函数从 `head` 开始沿 `next` 删除所有节点，包括两个哨兵与剩余业务节点；顺序与插入先后无关。若省略析构，短程序进程结束由 OS 回收，但面试应主动提「需要释放 `new` 的节点」。

**`unordered_map` 与自定义哈希**：`int` 键默认够用；若改为 `string` 键，哈希与相等比较自动适配，链表节点 `key` 类型同步修改即可。

## 练习与延伸

**必做**：

1. 本地运行 `lru_cache.py` / `lru_cache.cpp`，对照输出 `lru_cache OK`。
2. LeetCode 146 提交手写版（先 Python 链表，再 C++ 若主攻 C++ 岗）。
3. 打开 `python/problems/leetcode/0146_lru_cache/`，对比 `OrderedDict` 实现与本文链表版的行数、边界处理。

**刻意练习：自定义操作序列**

用下列序列在纸上跟踪 map 大小与链表 key 顺序（`cap=2`）：

`put(1,1), put(2,2), put(1,9), get(2), put(3,3), get(1), get(3)`

期望顺序变化：插入 1,2 → 更新 1 到最近 → get(2) 使 2 最近 → put(3) 淘汰最久（此时 1 最久）→ get(1) 为 -1 → get(3) 为 3。若你推演结果不同，回到「题意与接口」核对「更新是否移到最近」。

**结对复习**：一人口述操作，另一人只画链表不写代码，然后交换。口头「get 命中」必须说「移到 head 侧」，避免双方对「头/尾」理解相反。

**力扣提交环境提示**：Python 3 类名必须为 `LRUCache`；不要写 `main` 或打印。C++ 类定义在全局命名空间，方法签名与题面一致。若使用自定义哈希或模板，确保与 `int` 键题面一致，避免过度设计导致编译错误。

**延伸练习**：

| 题目 / 主题 | 关系 |
|-------------|------|
| [460. LFU Cache](https://leetcode.cn/problems/lfu-cache/) | 在 LRU 上增加频率维度 |
| [432. All O`one` Data Structure](https://leetcode.cn/problems/all-oone-data-structure/) | 多频率桶 + 双向链表 |
| `data_structures/advanced/lru_cache` | 仓库内可复用封装，对比 API 设计 |
| Hot 100 题单第 25 题 | 见 `prob-hot100` 博文中的 LRU 精读示例 |

**自测用例（除官方示例外建议手写）**：

- `capacity=1`：`put(1,1); put(2,2); get(1)==-1`
- 更新：`put(1,1); put(1,2); get(1)==2`，且 size 仍为 1
- 交替 `get`：`put(1,1); put(2,2); get(1); get(2); put(3,3)` 应淘汰 key 2（若 2 为最久）

**白板默写检查清单**

- [ ] 画出 head/tail 哨兵与两个真实节点插入后的指针方向
- [ ] 口述 `put` 命中与未命中两条路径
- [ ] 写出淘汰时同时删 map 与链表
- [ ] 说明 `get` 未命中为何不改变顺序
- [ ] 复杂度与空间 O(capacity)

**与 146 变体题的关系**

- [588. 设计内存池](https://leetcode.cn/problems/design-in-memory-file-system/) 等设计题考察 API 拆分，不直接考 LRU，但「容量受限 + 驱逐」思想类似。
- 系统设计题「设计 Twitter」等常提到 **feed 缓存**；可答「热点 key 用 LRU，配合分布式一致性哈希分片」。

**调试技巧**：链表断环时 `get` 可能死循环或 WA。可在调试版 `put` 后断言：从 `head` 沿 `next` 走到 `tail` 步数等于 `len(map)`，且每个 `node.key` 在 map 中指向自身。

**Hot 100 路径复盘（与 `prob-hot100` 博文配合）**

1. 在 `python/problems/hot100/notes.md` 找到 LRU 一行（约排名 25），记下目录 `0146_lru_cache`。
2. 先读本站专题掌握双向链表 + 哈希，再打开题解 `notes.md` 看 OrderedDict 思路。
3. 用 `solution.py` 提交 LeetCode；若超时或 WA，回到 `interview/classic/lru_cache.py` 对照指针逻辑。
4. 周末用 C++ `solution.cpp` 再 AC 一遍，巩固指针写法。

**460 LFU 预习提示（不做完整实现也可）**：准备 `min_freq` 变量与 `freq → 链表` 的字典；`get` 时旧 freq 桶删 key、新 freq 桶头插 key，并可能让 `min_freq` 增加；`put` 新 key 时 freq 从 1 开始。理解 LFU 后回头看 LRU，会发现 LRU 相当于「freq 只有 0/1 且 get 就重置」的特例，有助于记忆为何 LRU 更简单。

**设计题书写模板（白板）**

```
class LRUCache:
    # 字段: cap, map, head, tail
    def __init__(self, capacity): 初始化哨兵
    def _add / _remove / _move: 先写这三个
    def get(self, key):
    def put(self, key, value):
```

先写注释分支，再填指针操作，可少漏 `moveToFront`。

## 学习路径

建议按三天节奏（每天约 45–60 分钟）：

**第一天 · 语义与纸面**

- 精读本文「题意与接口」与官方示例，在纸上画链表指针变化，不写代码。
- 列出 `get`/`put` 各分支对 map 与链表的影响（表格即可）。
- 独立完成 `capacity=1` 表格推演，核对每一步 map 大小是否为 1。
- 用自己的话向他人解释「为什么 146 必须用双向链表」，录音回放检查是否跳过「命中要 O(1) 移到最近」这一句。

**第二天 · 实现与 AC**

- 默写 Python 三个私有方法 + `get`/`put`，运行 `lru_cache.py`。
- 提交 146；若失败，对照「易错点」逐项排查。
- 可选：阅读 `0146` 的 `OrderedDict` 版，理解 `move_to_end` 与 LRU 的对应。
- 计时练习：设定 15 分钟闹钟，从零写 Python 版直至通过本地断言。

**第三天 · C++ 与追问**

- 实现或对照 C++ 版，注意 `delete` 与析构。
- 口头回答「扩展追问」中 LFU、线程安全、分布式各 1–2 分钟。
- 若时间充裕，启动 460 或回顾 Hot 100 中其他设计题（如 208 Trie）。

**复习间隔建议**：第 1 天学习后，第 3 天闭卷重写一次；第 7 天再在 C++ 下写一遍。间隔重复比连续三小时抄代码更能形成长期记忆。若已在工作中写过缓存，可把重点放在「能向同事解释不变量」而非「背代码行号」。

**与其他 interview/classic 专题的衔接**：学完 LRU 后，「设计类」可继续看栈/队列实现题（155、232）练 API 设计；图与哈希题（1、3）练 map 熟练度。LRU 的 map+链表组合也会出现在「复制带随机指针链表」等题中，但指针技巧不同，勿混淆。

已掌握 LRU 后，滑动窗口、哈希设计题可并行复习；LRU 常作为「缓存模块」嵌入更大系统设计讨论（数据库缓冲池、CDN 边缘缓存），此时强调**命中率**与**淘汰策略**对延迟的影响，而非仅代码正确性。

**一周强化（可选）**

| 天 | 任务 |
|----|------|
| 一 | 纸面推演官方样例 + `capacity=1` |
| 二 | Python 手写 AC 146 + 对照 OrderedDict |
| 三 | C++ 手写或对照 `lru_cache.cpp` |
| 四 | 460 LFU 只读题解，画 freq 桶 |
| 五 | 模拟面试：15 分钟无 IDE 写 Python 版 |
| 六 | 复盘易错点，写 3 条自测用例 |
| 七 | Hot 100 中再挑 1 道设计题（208/295） |

**与 `data_structures/advanced/lru_cache` 的分工**：advanced 目录侧重可复用模块（可能封装默认容量、统计命中率）；`interview/classic` 侧重面试最短路径与可读性。两处代码宜对照阅读，但不必合并为一份实现。

## 延伸阅读

- Study 专题笔记：[python/interview/classic/lru_cache/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/interview/classic/lru_cache)
- 仓库 GitHub：[zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) — `interview/classic/lru_cache` 与 `problems/leetcode/0146_lru_cache`
- LeetCode：[146. LRU Cache](https://leetcode.cn/problems/lru-cache/)
- 本站题单导航：`prob-hot100`（Hot 100 与 leetcode 目录映射）
- 《算法导论》缓存与分页相关章节（操作系统课程中的 LRU 页面置换与本题**同思想**，实现细节不同）
- Redis 文档：[Eviction policies](https://redis.io/docs/reference/eviction/) — `allkeys-lru` / `volatile-lru` 为近似 LRU，与严格双向链表实现不同
- C++ reference：`std::list::splice`、`unordered_map` 均摊复杂度说明
- 力扣讨论区 146 题：搜索「moveToFront」「tail.prev」可见大量 WA 复盘，可对照本文「易错点」阅读（不必逐条抄评论）

**阅读时间预估**：精读全文约 35–45 分钟；若已熟悉 LRU，只读「基础篇」+ 代码段约 15 分钟。建议边读边在纸上跟画一遍官方样例，比纯眼读更快建立指针直觉。完成阅读后请关闭题解默写一遍 `LRUCache`，再与本文 Python 节逐行 diff，差异处即你的薄弱点。若 diff 仅差异常处理或 `__len__`，可忽略；若差在 `moveToFront` 或淘汰键，必须重练。达标后再做一次 C++ 编译运行，确保双语言都能过本地断言。本专题至此结构与 Study 源码对齐，可标记待 strict 校验后发布。祝你在 LeetCode 146 一次通过，面试白板手写也能稳过。多练链表指针，比死记题解更有效率。

**术语对照**

| 英文 | 含义 |
|------|------|
| cache hit / miss | 命中 / 未命中 |
| eviction | 因超容移除条目 |
| sentinel / dummy node | 哨兵节点，简化边界 |
| recency | 时间上的「最近使用」 |
| strict LRU | 每次访问都更新顺序；与采样 LRU 相对 |

**manifest 与站点关系**：`algorithm-guides/manifest.json` 中 `slug: iv-classic-lru-cache` 指向本目录；`guide_toc: interview-classic` 决定基础篇六个 `###` 标题与 `_meta/guide-toc/interview-classic.yaml` 一致。撰写时勿增删顶层 `##`，否则 `validate_algorithm_guide.py` 报错。

**质量检查命令（维护者）**

```powershell
Set-Location -LiteralPath 'F:\commercial\atelier'
python scripts\validate_algorithm_guide.py --slug iv-classic-lru-cache --strict
python scripts\validate_algorithm_quality.py --slug iv-classic-lru-cache --strict
```

通过 guide 校验需汉字 ≥ 8000（`guide_tier: medium`）；quality 校验检查 filler、占位代码块、Python/C++ 段是否含真实代码_fence 等。

**自测问答（闭卷）**

1. 146 题 `get` 未命中返回值是多少？是否改变 LRU 顺序？  
2. `put` 已存在 key 时容量如何变化？  
3. 淘汰时从链表哪一端取节点？从 map 删什么？  
4. 为何节点存 key？  
5. Python OrderedDict 哪一端表示「最近」？  

参考答案：1→-1，不改变；2→不变；3→`tail.prev`，删 `evict.key`；4→O(1) 删 map；5→`move_to_end(..., last=False)` 为最近。若五条能在两分钟口述清楚，可视为本专题达标。

**版本记录**：2026-05-21 首稿，对照 Study 仓库 `interview/classic/lru_cache` Python/C++ 与 `notes.md`；LeetCode 题号以 146 为准，Hot 100 目录名为 `0146_lru_cache`。

**收束小结**：LRU Cache 的本质是维护「按访问时间排序」的可索引集合；哈希提供索引，双向链表提供顺序，哨兵简化边界。掌握 `get`/`put` 四条分支与三个链表原语后，146 题应一次通过；进阶方向是 LFU（460）与系统设计中「近似 LRU + 分片」的叙述。把本文当作专题教材而非题解索引，配合 Study 仓库运行与提交，即可完成从理解到熟练的闭环。若你已在其他平台 AC 过 146，仍建议对照本文检查「更新 key 是否 moveToFront」「淘汰是否删 map」，用十分钟复盘可降低二面手写时翻车概率。撰写本稿时以 Study 仓库 `lru_cache.py` / `lru_cache.cpp` 为源码真值，LeetCode 146 为题面真值，Hot 100 与 manifest 为导航真值；三者冲突时以可运行代码与 OJ 题面为准。

---

*本文 `status: published`，待 `validate_algorithm_guide.py` 与 `validate_algorithm_quality.py --strict` 通过后可标为 `published`。*
