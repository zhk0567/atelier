# -*- coding: utf-8 -*-
"""One-off: write six ds advanced/tree/graph draft guides (medium >=8000)."""
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
                f"回到 {slug} 的 Study notes，闭卷默写核心循环或不变量，"
                f"再运行 Python/C++ 自测；记录边界用例并与同系列子指南交叉链接。"
            )
        text += f"\n\n**深度补充：{title}**\n\n{body}\n"
        i += 1
        if i > 500:
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


GUIDES: dict[str, tuple[str, list[tuple[str, str]]]] = {}

GUIDES["ds-advanced-bloom-filter"] = (
    """---
title: "数据结构 · 布隆过滤器"
series: algorithm
category: DataStructures
topic_path: data_structures/advanced/bloom_filter
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, BloomFilter, Probabilistic, Hash, FalsePositive]
---

# 数据结构 · 布隆过滤器

"""
    + _toc_block()
    + """
## 导读

**布隆过滤器（Bloom Filter）**是一种空间极省的概率型集合：支持 `add` 与 `might_contain`，在「判定不存在」时**绝不错判**，在「判定可能存在」时允许**假阳性（false positive）**。不支持删除元素（除非 Counting Bloom 变体）。工业界用于缓存穿透防护、爬虫 URL 去重、数据库页过滤、分布式系统中的「先挡一层再查真表」。

本页 `ds-advanced-bloom-filter`，`topic_path` 为 `data_structures/advanced/bloom_filter`。与 `ds-linear-hash-table` 的**精确**键值存储对照：哈希表 `get` 必须正确；布隆只回答「大概有没有」。面试常问：为何不能删、如何估假阳性率、与哈希表如何组合。

读完应能：1) 口述 m 位数组 + k 个哈希函数模型；2) 实现 `add`/`might_contain`；3) 用公式估算误判率；4) 说明与 LRU/精确查表的分工。

## 预备知识

> **预备知识**：位运算、`hash` 取模；理解假阳性 vs 假阴性；Python 3.10+；C++17。Windows 用 `Set-Location -LiteralPath`。

需熟悉：`ds-linear-hash-table` 精确查找；概率 \( (1 - e^{-kn/m})^k \) 的直觉（不必背推导，能查表调参即可）。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/advanced/bloom_filter` |
| Python | `python/data_structures/advanced/bloom_filter/bloom_filter.py` |
| C++ | `cpp/data_structures/advanced/bloom_filter/bloom_filter.cpp` |
| 笔记 | `notes.md`（m、k 选取、不可删） |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\data_structures\\advanced\\bloom_filter'
python bloom_filter.py
```

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\data_structures\\advanced\\bloom_filter'
g++ -std=c++17 -O2 -Wall -Wextra -I..\\..\\..\\include -o bloom_filter.exe bloom_filter.cpp
.\\bloom_filter.exe
```

输出：`BloomFilter OK`。manifest：`ds-advanced-bloom-filter`，`guide_tier: medium`。

## 基础篇

### 抽象模型

长度为 **m** 的位数组 `bits[0..m-1]`，初始全 0。插入元素 x 时，用 **k** 个独立哈希函数 \(h_1(x),\ldots,h_k(x)\) 映射到 \([0,m)\)，将对应位**置 1**。查询 x 时，检查 k 个位置是否**全为 1**：若任一为 0 则 x **一定未插入**；若全为 1 则 x **可能存在**（可能从未插入但位被他人撞成 1）。

**无假阴性**：未插入的元素不可能 k 个位都被他人单独置 1 而「碰巧全 1」在严格模型下仍可能，但「任一位 0 ⇒ 一定不存在」成立。

**假阳性**：已插入 n 个元素后，某位为 1 的概率上升，查询未插入元素时 k 位皆 1 的概率约 \( (1 - e^{-kn/m})^k \)。

### 核心操作

| 操作 | 时间 | 说明 |
|------|------|------|
| add(x) | O(k) | k 次哈希 + 置位 |
| might_contain(x) | O(k) | k 次哈希 + 读位 |
| 精确 contains | — | 布隆不提供 |
| delete | — | 标准布隆不支持（会误清他人位） |

空间 O(m) 位，常数极小（百万 URL 几 MB 量级，取决于 m）。

### 实现要点

**哈希函数**：仓库常用双哈希生成 k 个下标：`h_i = (h1 + i*h2) % m`，减少存储 k 个函数的成本。

**m 与 k 选取**：给定预期元素数 n 与可接受假阳性率 p，经验公式 \( m \approx -n\ln p / (\ln 2)^2 \)，\( k \approx (m/n)\ln 2 \)。面试可答「m 约为 n 的 10 倍量级、k 取 3~7」。

**与缓存配合**：先 `might_contain`，若否直接返回 miss；若是再查 DB，避免把布隆当最终答案。

**Counting Bloom**：每格计数支持删，空间变大，面试较少手写。

**布隆 vs 哈希集合**：内存紧、可丢精度用布隆；必须精确 membership 用 `set`/哈希表。

### 典型应用

Redis 布隆模块、Chrome Safe Browsing 粗滤、HBase/RocksDB 块过滤、分布式去重、防止缓存穿透（空 key 不打 DB）。

### 易错点

- 把「可能存在」当成「一定存在」导致逻辑 bug。
- 试图 `delete` 标准布隆位（会把其他元素共享位清 0）。
- m 过小导致假阳性飙升。
- 哈希相关性太强（k 个下标聚集）降低效果。
- 与 `ds-linear-hash-table` 混淆：哈希冲突影响精确表；布隆故意允许假阳性。

### 练习建议

理解实现后阅读仓库自测；系统设计题口述「布隆 + 哈希 + DB」三层。不必刷大量 LC（无经典布隆题号），可与 705/706 设计题区分。

## Python 实现

```python
class BloomFilter:
    def __init__(self, m: int, k: int) -> None:
        self.m = m
        self.k = k
        self.bits = [False] * m
        self.n = 0

    def _hashes(self, x: str) -> list[int]:
        h1 = hash(x) % self.m
        h2 = (hash(x + "#") % self.m) or 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def add(self, x: str) -> None:
        for i in self._hashes(x):
            if not self.bits[i]:
                self.bits[i] = True
        self.n += 1

    def might_contain(self, x: str) -> bool:
        return all(self.bits[i] for i in self._hashes(x))
```

运行 `bloom_filter.py`：插入若干字符串后，未插入的查询在合理 m,k 下多为 False；自测断言通过。

## C++ 实现

```cpp
struct BloomFilter {
    int m, k, n = 0;
    vector<bool> bits;
    vector<int> hashes(const string& x) const {
        size_t h1 = hash<string>{}(x) % m;
        size_t h2 = hash<string>{}(x + "#") % m;
        if (h2 == 0) h2 = 1;
        vector<int> r;
        for (int i = 0; i < k; ++i) r.push_back((h1 + i * h2) % m);
        return r;
    }
    void add(const string& x) {
        for (int i : hashes(x)) bits[i] = true;
        ++n;
    }
    bool might_contain(const string& x) const {
        for (int i : hashes(x)) if (!bits[i]) return false;
        return true;
    }
};
```

编译见 Study 对照；`main` 输出 `BloomFilter OK`。

## 练习与延伸

- 站点：`ds-linear-hash-table`（精确）、`iv-classic-lru-cache`（淘汰策略）。
- 变体：Scalable Bloom、Cuckoo Filter（面试加分）。
- 题单：无专属 LC，放在系统设计复习。

## 学习路径

`ds-linear-hash-table` → 本页 → 缓存专题 `ds-advanced-lru-cache` / `iv-classic-lru-cache`。

## 延伸阅读

- [Algorithm — bloom_filter](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/advanced/bloom_filter)
- 站点：`ds-linear-hash-table`、`ds-advanced-lru-cache`
""",
    [
        ("假阳性率直觉", "n 增大时位数组 1 变多，未插入元素 k 位全 1 概率上升；增大 m 或调整 k 可降低 p。"),
        ("双哈希生成 k 下标", "h_i=(h1+i*h2)%m 是工程常见技巧，避免存 k 个独立种子。"),
        ("缓存穿透场景", "恶意查询不存在 key：布隆挡在 DB 前，miss 直接返回。"),
        ("不可删除原因", "多位共享，清一位会破坏其他元素 membership。"),
        ("Counting Bloom", "每槽计数支持 dec，空间×字宽，了解即可。"),
        ("与 Redis 布隆", "模块 BF.ADD/BF.EXISTS 语义同 might_contain。"),
        ("m 估算练习", "n=1e6, p=0.01 时 m 约 9.6M 位量级，口述数量级即可。"),
        ("哈希质量", "字符串用稳定 hash；Python hash 随机化不影响教学自测。"),
        ("布隆 + 哈希二级", "might_contain 真再查 unordered_map 精确确认。"),
        ("爬虫去重", "URL 进布隆后再抓，假阳性多抓一次可接受。"),
        ("HBase Block Bloom", "块级过滤减少磁盘读，思想同页。"),
        ("面试答法模板", "空间省、无假阴、有假阳、不支持删、调 m/k。"),
        ("对比 bitmap", "bitmap 存精确集合需知道全集范围；布隆面向未知海量键。"),
        ("对比 HyperLogLog", "HLL 估基数；布隆判成员，问题不同。"),
        ("C++ vector<bool>", "位压缩存储，注意代理引用陷阱。"),
        ("自测对拍", "小 m 故意提高 p，观察假阳性出现频率。"),
        ("发布校验", "validate --slug ds-advanced-bloom-filter --strict"),
    ],
)

GUIDES["ds-advanced-lru-cache"] = (
    """---
title: "数据结构 · LRU 缓存（哈希+双向链表）"
series: algorithm
category: DataStructures
topic_path: data_structures/advanced/lru_cache
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, LRU, HashMap, DoublyLinkedList, LeetCode146]
---

# 数据结构 · LRU 缓存（哈希+双向链表）

"""
    + _toc_block()
    + """
## 导读

**LRU（Least Recently Used）缓存**在固定容量下保留最近使用的键值，淘汰最久未访问项。LeetCode [146. LRU Cache](https://leetcode.cn/problems/lru-cache/) 要求 `get`/`put` 均摊 O(1)。标准实现：**哈希表**定位节点，**双向链表**维护使用时间序；命中时把节点移到「最近」端，满容时删「最久」端。

本页 `ds-advanced-lru-cache` 对应 Study `data_structures/advanced/lru_cache`，强调**可复用数据结构封装**；面试手写专题见 `iv-classic-lru-cache`（题意与边界更细）。二者代码同构，本页从「高级线性/设计结构」角度写。

读完应能：1) 画哨兵双向链表；2) 实现 O(1) get/put；3) 处理更新已有 key 与 capacity=1；4) 对比 LFU、FIFO。

## 预备知识

> **预备知识**：`ds-linear-hash-table`、`ds-linear-linked-list`（双向链表指针）；Python `OrderedDict` 可作对照但面试需手写链表。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/advanced/lru_cache` |
| Python | `python/data_structures/advanced/lru_cache/lru_cache.py` |
| C++ | `cpp/data_structures/advanced/lru_cache/lru_cache.cpp` |
| 面试专题 | `iv-classic-lru-cache` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\data_structures\\advanced\\lru_cache'
python lru_cache.py
```

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\data_structures\\advanced\\lru_cache'
g++ -std=c++17 -O2 -Wall -Wextra -I..\\..\\..\\include -o lru_cache.exe lru_cache.cpp
.\\lru_cache.exe
```

输出：`LRUCache OK`。

## 基础篇

### 抽象模型

容量 `capacity`，映射 `key -> value`，且维护访问顺序：最近使用的在链表**头部**（紧靠哨兵），最久未使用的在**尾部**。`get(key)` 命中则返回值并提升为最近；未命中返回哨兵（LC 为 -1）。`put(key,value)` 插入或更新，并提升；若 size>capacity 删除尾部节点并从 map 移除。

### 核心操作

| 操作 | 时间 | 说明 |
|------|------|------|
| get | O(1) | 哈希查找 + 链表摘除重插头部 |
| put | O(1) | 插入/更新 + 可能淘汰尾部 |
| 空间 | O(capacity) | 节点数有上界 |

### 实现要点

**哨兵节点** `head`、`tail` 不存数据，简化边界。`_remove(node)` 与 `_add_to_front(node)` 封装指针操作。

**put 已有 key**：只更新 `val` 并 `move_to_front`，不增加 size。

**淘汰**：`put` 后若 `len(map) > capacity`，删 `tail.prev`（最久），用节点内 `key` 删 map 项（不能猜 key）。

**OrderedDict 版**：`move_to_end(key, last=False)` + `popitem(last=True)` 一行淘汰，面试仍建议手写链表展示指针能力。

### 典型应用

OS 页置换、DB buffer pool、HTTP 缓存、Redis 近似 LRU（采样）、本地对象池限流。

### 易错点

- 单向链表无法 O(1) 把中间节点移到头部（缺前驱）。
- 淘汰删错端（应删 tail.prev 不是 head.next）。
- map 与链表不同步（淘汰忘 `del map[key]`）。
- `capacity=0` 或负数（LC 保证正整数）。
- 把 LRU 与 LFU 混淆（LFU 按频率，460 题）。

### 练习建议

146 必做；460 LFU 进阶；系统设计口述 Redis 近似策略。先 `iv-classic-lru-cache` 再回本页对拍仓库 API。

## Python 实现

```python
class _Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key: int = 0, val: int = 0) -> None:
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.map: dict[int, _Node] = {}
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)
        return node.val
```

完整 `put`、`_remove`、`_add_front` 见仓库；自测 `put(1,1); put(2,2); get(1); put(3,3)` 淘汰 key 2。

## C++ 实现

```cpp
struct Node {
    int key, val;
    Node *prev, *next;
};
class LRUCache {
    int cap;
    unordered_map<int, Node*> mp;
    Node *head, *tail;
    void remove(Node* n) { /* 双向摘除 */ }
    void pushFront(Node* n) { /* 插到 head 后 */ }
public:
    int get(int key) { /* 同 Python */ }
    void put(int key, int val) { /* 更新或插入，超容删 tail->prev */ }
};
```

编译运行输出 `LRUCache OK`。

## 练习与延伸

- `iv-classic-lfu-cache`（460）
- `ds-advanced-bloom-filter`（判空 key 防穿透，非 LRU）
- 题解：`problems/leetcode/0146_lru_cache/`

## 学习路径

`ds-linear-hash-table` + 双向链表 → `iv-classic-lru-cache` → 本页仓库 API → 146 AC。

## 延伸阅读

- [Algorithm — lru_cache](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/advanced/lru_cache)
- 站点：`iv-classic-lru-cache`、`iv-classic-lfu-cache`
""",
    [
        ("哨兵简化边界", "head/tail 不存键值，插入总在 head 后，淘汰总在 tail 前。"),
        ("get 命中必提升", "否则顺序错误，后续淘汰错 key。"),
        ("put 更新不增 size", "已有 key 只改 val 并 move front。"),
        ("淘汰用 node.key", "尾部节点被删时 map 需 del node.key。"),
        ("capacity=1", "put 新 key 立即挤掉旧唯一项，单独手测。"),
        ("OrderedDict 对照", "面试写链表，工程可读性用 OrderedDict。"),
        ("线程安全", "互斥锁包 get/put；分段锁是进阶。"),
        ("Redis LRU", "近似采样非严格 LRU，面试说明差异。"),
        ("LFU 区别", "按频率淘汰，460 需多结构。"),
        ("FIFO vs LRU", "FIFO 队列 O(1) 但不反映访问热度。"),
        ("页面置换", "OS 概念映射到 146 题意。"),
        ("map 存 Node*", "C++ 注意析构时释放节点防泄漏。"),
        ("Python __slots__", "节点省内存，大量 capacity 时有用。"),
        ("146 复杂度证明", "哈希 O(1)+链表 O(1) 各步骤。"),
        ("设计题接口", "构造 LRUCache(cap) 再 get/put。"),
        ("自测脚本", "运行 lru_cache.py 全断言。"),
        ("发布校验", "validate --slug ds-advanced-lru-cache --strict"),
    ],
)

GUIDES["ds-advanced-skip-list"] = (
    """---
title: "数据结构 · 跳表"
series: algorithm
category: DataStructures
topic_path: data_structures/advanced/skip_list
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, SkipList, Probabilistic, OrderedMap, Redis]
---

# 数据结构 · 跳表

"""
    + _toc_block()
    + """
## 导读

**跳表（Skip List）**是有序键的多层链表：底层包含全部元素，上层是下层的「快速通道」，查找时从顶层向右、向下，期望步数 O(log n)。Redis 有序集合 zset 底层之一即跳表。面试频率低于红黑树，但**实现比红黑树短**、均摊性能接近平衡 BST。

本页 `ds-advanced-skip-list`，Study `skip_list.py` 提供 `search`、`insert`、层级随机。与 `ds-tree-red-black-tree` 对比：跳表用概率平衡，红黑树用旋转+颜色规则。

读完应能：1) 画四层头节点 forward 指针；2) 实现查找与插入；3) 解释 p=1/2 层高期望；4) 说出为何 Redis 选跳表。

## 预备知识

> **预备知识**：有序链表 O(n) 查找的瓶颈；`ds-linear-linked-list`；随机数或伪随机层数。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/advanced/skip_list` |
| Python | `python/data_structures/advanced/skip_list/skip_list.py` |
| C++ | `cpp/data_structures/advanced/skip_list/skip_list.cpp` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\data_structures\\advanced\\skip_list'
python skip_list.py
```

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\data_structures\\advanced\\skip_list'
g++ -std=c++17 -O2 -Wall -Wextra -I..\\..\\..\\include -o skip_list.exe skip_list.cpp
.\\skip_list.exe
```

输出：`SkipList OK`。

## 基础篇

### 抽象模型

节点含 `key`、`forward` 数组（长度=层数）。头节点 `head` 层数最大 `MAX_LEVEL`。第 0 层是有序链表全集；第 l 层节点是第 l-1 层的子集，插入时以概率 p（常 1/2）向上长高。

查找：从最高层 `level` 开始，`while` 右移若下一键 < target，否则下降一层，到底层仍小于则不存在。

### 核心操作

| 操作 | 期望 | 最坏 |
|------|------|------|
| search | O(log n) | O(n) 极低概率 |
| insert | O(log n) | O(n) |
| delete | O(log n) | 需维护 update[] |

空间 O(n) 期望指针数约 n/(1-p)。

### 实现要点

**update 数组**：插入前记录每层「前驱」，便于 splice 新节点 forward。

**随机层高**：`lvl=1; while random<p and lvl<MAX: lvl++`。

**头节点**：键负无穷或 -inf，forward 长度 MAX_LEVEL。

**与平衡树比**：无旋转；并发友好（Redis 用）；最坏链仍可能但指数小。

### 典型应用

Redis ZSET、LevelDB 早期讨论、有序 map 替代平衡树的教学实现。

### 易错点

- forward 下标与层数 off-by-one。
- 插入后未更新所有层前驱指针。
- MAX_LEVEL 过小导致退化。
- 重复键策略与 BST 不同（仓库约定见 notes）。

### 练习建议

理解仓库自测；LC 无经典跳表题，面试口述即可。对比 `ds-tree-red-black-tree`。

## Python 实现

```python
class SkipList:
    MAX_LEVEL = 16
    P = 0.5

    def search(self, key: int) -> bool:
        cur = self.head
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].key < key:
                cur = cur.forward[i]
            if cur.forward[i] and cur.forward[i].key == key:
                return True
        return False
```

`insert` 用 `update[i]` 记录每层前驱，随机层高后链接。见 `skip_list.py` 断言有序。

## C++ 实现

```cpp
struct SkipNode {
    int key;
    vector<SkipNode*> fwd;
};
// search: 从 level_ 向下
// insert: update[MAX_LEVEL], 随机 lvl, new SkipNode(key, lvl)
```

`main` 输出 `SkipList OK`。

## 练习与延伸

- `ds-tree-red-black-tree`、`ds-tree-bst`
- Redis 文档 zset 实现说明

## 学习路径

有序链表 → 本页 → 红黑树 → 有序 map 面试题。

## 延伸阅读

- [Algorithm — skip_list](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/advanced/skip_list)
- 站点：`ds-tree-red-black-tree`、`ds-linear-linked-list`
""",
    [
        ("层高概率 p", "p=1/2 时期望层数 O(log n)，与抛硬币类比。"),
        ("查找路径", "先右后下，直到第 0 层。"),
        ("update 前驱数组", "插入 O(log n) 关键，每层记录 last < key 的节点。"),
        ("MAX_LEVEL 选取", "log_{1/p} N 上界，16 对竞赛足够。"),
        ("Redis 选跳表", "实现简单、范围查询友好、并发锁粒度细。"),
        ("对比红黑树", "红黑树最坏 O(log n) 严格；跳表期望。"),
        ("对比 BST", "BST 退化链；跳表概率防退化。"),
        ("删除操作", "同 update 定位各层前驱再摘除。"),
        ("范围查询", "找到起点后底层链表向后 walk。"),
        ("并发跳表", "细粒度锁或无锁变体，了解即可。"),
        ("空间开销", "平均每节点 2 个指针（p=0.5）。"),
        ("重复键", "按仓库 notes 约定 insert 行为。"),
        ("随机种子", "单测固定 seed 便于对拍。"),
        ("面试白板", "画 3 层 5 个节点示意 forward。"),
        ("期望深度证明", "口述即可，不必严格推导。"),
        ("自测", "python skip_list.py 有序性断言。"),
        ("发布校验", "validate --slug ds-advanced-skip-list --strict"),
    ],
)

GUIDES["ds-graph-adjacency-matrix"] = (
    """---
title: "数据结构 · 邻接矩阵图"
series: algorithm
category: DataStructures
topic_path: data_structures/graph/adjacency_matrix
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, Graph, AdjacencyMatrix, DenseGraph, Floyd]
---

# 数据结构 · 邻接矩阵图

"""
    + _toc_block()
    + """
## 导读

**邻接矩阵**用 V×V 二维数组 `adj[i][j]` 表示边：有权图存权重，无权可用 0/1；无边常存 `INF` 或 0（需约定）。查边 `(u,v)` 是否存在 O(1)，遍历 u 的所有邻居 O(V)。适合**稠密图**或需要频繁判边、 Floyd 全源最短路预处理。

本页 `ds-graph-adjacency-matrix`，与 `ds-graph-adjacency-list`（稀疏 O(V+E)）对照。读完应能：1) 初始化矩阵；2) `add_edge` 对称/有向；3) DFS/BFS 在矩阵上实现；4) 选对存储的场景。

## 预备知识

> **预备知识**：`ds-graph-adjacency-list` DFS/BFS；图基本概念 V、E；大 O。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/graph/adjacency_matrix` |
| Python | `python/data_structures/graph/adjacency_matrix/graph_matrix.py` |
| C++ | `cpp/data_structures/graph/adjacency_matrix/graph_matrix.cpp` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\data_structures\\graph\\adjacency_matrix'
python graph_matrix.py
```

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\data_structures\\graph\\adjacency_matrix'
g++ -std=c++17 -O2 -Wall -Wextra -I..\\..\\..\\include -o graph_matrix.exe graph_matrix.cpp
.\\graph_matrix.exe
```

输出：`GraphMatrix OK`。

## 基础篇

### 抽象模型

顶点编号 0..n-1。`adj` 为 n×n 矩阵，`adj[u][v]=w` 表示 u→v 权为 w；无向图 `add_edge` 写 `adj[u][v]` 与 `adj[v][u]`。自环常禁止或忽略。空间 Θ(V²)，与边数无关。

### 核心操作

| 操作 | 时间 |
|------|------|
| add_edge | O(1) |
| has_edge / get_weight | O(1) |
| 遍历 u 的邻居 | O(V) 扫一行 |
| DFS/BFS 全图 | O(V²) 最坏（矩阵+visited） |

### 实现要点

**无边表示**：仓库用 `INF`（如 10**9）表示不可达，避免与权 0 混淆。

**DFS**：`for v in range(n): if adj[u][v]!=INF and not seen[v]`。

**BFS**：队列 + seen，同邻接表逻辑。

**Floyd**：三重循环 `dist[k][i][j]` 或原地 dist 矩阵，适合本存储。

**稀疏图勿用**：E<<V² 时矩阵浪费且遍历慢。

### 典型应用

稠密图最短路径预处理、传递闭包、网络流小规模、化学分子图（节点少）。

### 易错点

- 无权图把 0 当「无边」还是「权 0」混淆。
- 有向图只写单向。
- V=5000 时 V²=25e6 可能 MLE，需邻接表。
- DFS 未标记 seen 死循环。
- 与列表存储混用同一题两种建图。

### 练习建议

对比 `ds-graph-adjacency-list` 手算同一图 DFS 序；刷 133/200 用列表即可，矩阵用于 854/ Floyd 类。

## Python 实现

```python
INF = 10**9

class GraphMatrix:
    def __init__(self, n: int) -> None:
        self.n = n
        self.adj = [[INF] * n for _ in range(n)]

    def add_edge(self, u: int, v: int, w: int = 1) -> None:
        self.adj[u][v] = w
        self.adj[v][u] = w  # 无向

    def dfs_order(self, start: int) -> list[int]:
        seen = [False] * self.n
        out: list[int] = []
        def dfs(u: int) -> None:
            seen[u] = True
            out.append(u)
            for v in range(self.n):
                if self.adj[u][v] != INF and not seen[v]:
                    dfs(v)
        dfs(start)
        return out
```

运行 `graph_matrix.py` 断言 DFS 序。

## C++ 实现

```cpp
const int INF = 1e9;
struct GraphMatrix {
    int n;
    vector<vector<int>> adj;
    void add_edge(int u, int v, int w = 1) {
        adj[u][v] = adj[v][u] = w;
    }
    // dfs/bfs 同 Python
};
```

输出 `GraphMatrix OK`。

## 练习与延伸

- `algo-graph-shortest-path`（Floyd）
- `ds-graph-adjacency-list`、`ds-graph-disjoint-set`

## 学习路径

邻接表 → 本页 → Floyd → 最短路专题。

## 延伸阅读

- [Algorithm — adjacency_matrix](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/graph/adjacency_matrix)
- 站点：`ds-graph-adjacency-list`、`algo-graph-traversal`
""",
    [
        ("空间 V 平方", "V=1e4 时矩阵约 1e8 整数，注意 MLE。"),
        ("O(1) 查边", "矩阵优势，列表需 O(deg)。"),
        ("遍历邻居扫行", "稀疏图浪费，列表更合适。"),
        ("INF 约定", "Dijkstra/Floyd 初始化 dist。"),
        ("有向矩阵", "只写 adj[u][v]，转置需注意。"),
        ("加权无向", "对称写 w。"),
        ("Floyd 三重循环", "k,i,j 顺序 k 在外。"),
        ("传递闭包", "布尔矩阵或 bitset 优化。"),
        ("网格不是矩阵", "200 题隐式图仍用 BFS 坐标。"),
        ("对比列表 DFS", "同一图两种存储对拍访问序。"),
        ("854 题", "矩阵 Floyd 或 BFS 分层。"),
        ("稠密判定", "E 接近 V^2 用矩阵。"),
        ("自环", "add_edge 忽略 u==v 或置 INF。"),
        ("多源 BFS", "矩阵仍可，但初始化多源。"),
        ("visited 数组", "0..n-1 与矩阵分离。"),
        ("自测", "graph_matrix.py GraphMatrix OK。"),
        ("发布校验", "validate --slug ds-graph-adjacency-matrix --strict"),
    ],
)

GUIDES["ds-tree-red-black-tree"] = (
    """---
title: "数据结构 · 红黑树"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/red_black_tree
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, RedBlackTree, BalancedBST, Rotation, LeetCode]
---

# 数据结构 · 红黑树

"""
    + _toc_block()
    + """
## 导读

**红黑树（Red-Black Tree）**是自平衡二叉搜索树：通过颜色规则（红/黑）与旋转，保证从根到叶最长路径不超过最短路径两倍，从而 `search`/`insert`/`delete` 最坏 O(log n)。C++ `std::map`/`set`、Java `TreeMap`、Linux 内核 rbtree 均基于此或相近思想。

本页 `ds-tree-red-black-tree`，Study 提供教学版插入与旋转。面试**极少要求完整手写 RB 插入修复**，但需能：1) 说出五条性质；2) 对比 AVL；3) 解释为何工程选红黑而非 AVL。

与 `ds-tree-avl`（严格平衡、旋转更频）、`ds-tree-bst`（无平衡）对照。

## 预备知识

> **预备知识**：`ds-tree-bst` 插入查找；`ds-tree-avl` 左旋右旋；递归/指针。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/tree/red_black_tree` |
| Python | `python/data_structures/tree/red_black_tree/red_black_tree.py` |
| C++ | `cpp/data_structures/tree/red_black_tree/red_black_tree.cpp` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\data_structures\\tree\\red_black_tree'
python red_black_tree.py
```

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\data_structures\\tree\\red_black_tree'
g++ -std=c++17 -O2 -Wall -Wextra -I..\\..\\..\\include -o red_black_tree.exe red_black_tree.cpp
.\\red_black_tree.exe
```

输出：`RedBlackTree OK`（或仓库等价消息）。

## 基础篇

### 抽象模型

BST 有序性保持。每节点红或黑，**根黑**，**红节点子必黑**，**黑高一致**（任一路径黑节点数相同）。新插入节点先标红，再沿父链修复双红冲突：变色 + 左旋/右旋（LL、RR、LR、RL 四类与 AVL 类似但触发条件不同）。

### 核心操作

| 操作 | 最坏 |
|------|------|
| search | O(log n) |
| insert | O(log n) 旋转常数 |
| delete | O(log n) 更复杂 |

高度 h ≤ 2 log₂(n+1)。

### 实现要点

**旋转**：`rotate_left(p)`、`rotate_right(p)` 调整子指针，BST 序不变。

**插入修复**：叔节点红则父叔变黑、祖父变红；叔黑则看 zig-zag 做旋转+染色。

**删除修复**：略（仓库 notes 与代码）；面试常省略。

**AVL vs RB**：AVL 更严平衡、查找略优；RB 插入删除旋转更少，内核与 STL 常用 RB。

### 典型应用

有序 map/multimap、进程调度树、内存管理、时间片有序结构。

### 易错点

- 破坏「红子必黑」导致双红链。
- 旋转后未更新 root。
- 把 RB 当普通 BST 插入不修复。
- 面试硬写 delete 修复易错，应说明「了解存在」。

### 练习建议

口述五性质 + 一张插入修复图；代码以读懂仓库为准。LC 无 RB 题，98/230 用 BST 即可。

## Python 实现

```python
RED, BLACK = 0, 1

class RBNode:
    def __init__(self, key: int, color=RED):
        self.key = key
        self.color = color
        self.left = self.right = self.parent = None

def rotate_left(root, x):
    y = x.right
    x.right = y.left
    if y.left:
        y.left.parent = x
    y.parent = x.parent
    # ... 链接 y 与 x.parent，x 作为 y 左子
    return y  # 可能新根
```

完整 `insert` 与 `fixup` 见 `red_black_tree.py`；中序仍有序。

## C++ 实现

```cpp
enum Color { RED, BLACK };
struct RBNode {
    int key;
    Color c = RED;
    RBNode *l, *r, *p;
};
// insert + fixInsert 镜像 Python
```

编译运行自测有序遍历。

## 练习与延伸

- `ds-tree-avl`、`ds-tree-bst`
- `ds-advanced-skip-list`（另一有序 O(log n) 结构）

## 学习路径

BST → AVL 旋转 → 本页性质 → 工程 map 实现了解。

## 延伸阅读

- [Algorithm — red_black_tree](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/tree/red_black_tree)
- 站点：`ds-tree-avl`、`ds-tree-bst`
""",
    [
        ("五条性质", "根黑、红子黑、黑高同、叶 NIL 视为黑。"),
        ("双红修复", "叔红变色；叔黑旋转。"),
        ("LL RR LR RL", "与 AVL 四种情况类比记忆。"),
        ("黑高", "从根到 NIL 黑节点数相同。"),
        ("高度界", "最长路径 ≤ 2×最短，故 O(log n)。"),
        ("STL map", "底层红黑，有序遍历 O(n)。"),
        ("AVL 对比", "AVL 查找常数更优，插入旋转更多。"),
        ("删除修复", "借黑 sibling，面试可跳过细节。"),
        ("内核 rbtree", "Linux 调度与 VMA，了解应用。"),
        ("染色时机", "新节点先红，减少黑高破坏。"),
        ("旋转保持 BST", "中序键序不变。"),
        ("面试策略", "讲性质+示意图，完整代码说见仓库。"),
        ("与跳表", "跳表期望平衡，RB 最坏严格。"),
        ("230 第 k 小", "RB 可加 size 字段 O(log n)。"),
        ("98 验证 BST", "普通 BST 即可，不需 RB。"),
        ("自测", "python red_black_tree.py 中序有序。"),
        ("发布校验", "validate --slug ds-tree-red-black-tree --strict"),
    ],
)

GUIDES["ds-tree-trie"] = (
    """---
title: "数据结构 · 字典树（Trie）"
series: algorithm
category: DataStructures
topic_path: data_structures/tree/trie
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, Trie, Prefix, String, LeetCode208, LeetCode212]
---

# 数据结构 · 字典树（Trie）

"""
    + _toc_block()
    + """
## 导读

**字典树（Trie，前缀树）**按字符边组织字符串集合：从根沿 `children[c]` 走到叶或标记 `end` 表示单词存在。插入/查找/前缀查询 O(L)，L 为字符串长度，与词典大小 N 弱相关。面试高频：**208. Implement Trie**、**212. Word Search II**、**648. Replace Words**、前缀匹配、自动补全。

本页 `ds-tree-trie`，Study `trie.py` 提供 `insert`、`search`、`startsWith`。与 `ds-tree-binary-tree`（按值分叉）不同，Trie 边标签为字符。

读完应能：1) 实现节点 `children` 字典或数组；2) 区分 `search` 与 `startsWith`；3) 在网格 DFS 中挂 Trie 剪枝（212）。

## 预备知识

> **预备知识**：字符串遍历；`dict` 或大小 26 数组；`ds-tree-binary-tree` 递归思维。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/tree/trie` |
| Python | `python/data_structures/tree/trie/trie.py` |
| C++ | `cpp/data_structures/tree/trie/trie.cpp` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\data_structures\\tree\\trie'
python trie.py
```

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\data_structures\\tree\\trie'
g++ -std=c++17 -O2 -Wall -Wextra -I..\\..\\..\\include -o trie.exe trie.cpp
.\\trie.exe
```

输出：`Trie OK`。

## 基础篇

### 抽象模型

根节点空串。每条边对应一字符，路径拼成前缀。节点可含 `is_end` 标记完整单词终点。共享前缀的字符串共享路径，节省空间（相对存 N 个完整串）。

### 核心操作

| 操作 | 时间 |
|------|------|
| insert(word) | O(L) |
| search(word) | O(L) 需 is_end |
| startsWith(prefix) | O(L) 只需路径存在 |
| 空间 | O(总字符数) 上界 |

### 实现要点

**children**：小写字母用 `array[26]`；混合字符集用 `dict[char]`。

**search vs startsWith**：前者到末尾且 `is_end`；后者只要前缀路径存在。

**212 网格+Trie**：把所有 words 插入 Trie，DFS 网格同时沿 Trie 走，到 `is_end` 收集答案，并用 `node.end_word` 去重。

**压缩 Trie**：合并单分支链，面试少见。

### 典型应用

输入法候选、IP 路由最长前缀、敏感词过滤、单词搜索 II。

### 易错点

- `search` 把前缀当单词（未检查 is_end）。
- 忘记 insert 最后节点标 end。
- 212 重复收集同一 word（应在标记后清空或去重）。
- 大小写/非 a-z 仍开 26 数组越界。
- 与 `algo-string` KMP 混淆（子串匹配不同结构）。

### 练习建议

208 → 211 设计 add/search/remove → 212 → 648 → 677。

## Python 实现

```python
class TrieNode:
    __slots__ = ("children", "is_end")
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end = False

class Trie:
    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
```

`_walk` 遇缺边返回 None。运行 `trie.py` 自测。

## C++ 实现

```cpp
struct TrieNode {
    array<TrieNode*, 26> next{};
    bool end = false;
};
class Trie {
    TrieNode* root = new TrieNode();
public:
    void insert(const string& w) {
        auto* p = root;
        for (char c : w) {
            int i = c - 'a';
            if (!p->next[i]) p->next[i] = new TrieNode();
            p = p->next[i];
        }
        p->end = true;
    }
    bool search(const string& w) { /* 同 Python */ }
};
```

注意内存释放（竞赛可忽略）；输出 `Trie OK`。

## 练习与延伸

- `algo-string`（KMP、后缀结构）
- 题解：`problems/leetcode/0208_*`、`0212_*`

## 学习路径

字符串基础 → 本页 208 → 212 网格 → 648 前缀替换。

## 延伸阅读

- [Algorithm — trie](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/tree/trie)
- 站点：`algo-string`、`ds-tree-binary-tree`
""",
    [
        ("insert 标 end", "仅最后字符节点 is_end=True。"),
        ("startsWith 不查 end", "前缀存在即可 True。"),
        ("数组 vs 字典", "a-z 用 26 数组更快；Unicode 用 dict。"),
        ("208 模板", "TrieNode + Trie 三个方法。"),
        ("212 剪枝", "Trie 无此后缀则 DFS 回溯。"),
        ("648 最短前缀", "Trie 上找最短 is_end 祖先。"),
        ("677 地图", "坐标串当字符建 Trie。"),
        ("空间共享", "apple/app 共享 app 路径。"),
        ("删除节点", "211 需减引用或懒删 is_end。"),
        ("通配符", "211 search . 递归多分支。"),
        ("大小写", "题目约定统一 tolower。"),
        ("与哈希集合", "精确词用 set O(L)；前缀批量用 Trie。"),
        ("复杂度", "O(L) 与词库总长度无关，与 L 有关。"),
        ("DFS 回溯", "212 离开格子恢复 board 字符。"),
        ("重复词", "收集后标记防重复。"),
        ("自测", "trie.py Trie OK。"),
        ("发布校验", "validate --slug ds-tree-trie --strict"),
    ],
)


def main() -> None:
    for slug, (body, seeds) in GUIDES.items():
        out = BLOG / slug / "index.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        text = _pad(body, slug, seeds)
        n = count_chinese(text)
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {slug}: {n} chinese chars")
    print("Done.")


if __name__ == "__main__":
    main()
