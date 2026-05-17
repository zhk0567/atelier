# Algorithm · 双语言算法与刷题仓库

面向 **面试准备** 与 **长期复习** 的个人知识库：**第一要务**是把 **算法与数据结构** 按专题 **双语言、可运行自测** 成体系整理。同一套目录在 **Python** 与 **C++** 下 **镜像同构**；并含 LeetCode 归档、手写面试专题等。**约定、学习路线、单题模板、C++ 工具链、待办与变更日志**均写在**本 README 文末**对应锚点（不再使用单独 `maint/` / `docs/` 目录；**亦不保留 `scripts/` 工具目录**）。

---

## 全库入口索引

### 约定与附录（均在本文内）

| 锚点 | 说明 |
|------|------|
| [Study roadmap](#study-roadmap) | 学习顺序简表 |
| [Repo layout](#repo-layout) | 顶层目录一览 |
| [Problem notes template](#problem-notes-template) | 新题 `notes.md` 模板 |
| [C++ toolchain](#cpp-toolchain) | `alg_std.hpp`、g++/MSVC |
| [Coverage](#coverage) | 覆盖与总表入口（链到各 `notes.md`） |
| [Pending tasks](#pending-tasks) | P1 标准与封版提醒 |
| [Changelog](#changelog) | 里程碑摘要 |

### C++ 公共头

| 链接 | 说明 |
|------|------|
| [cpp/include/alg_std.hpp](cpp/include/alg_std.hpp) | 统一标准库聚合头（新代码请用它替代 `bits/stdc++.h`） |

### 语言总入口（`notes.md`）

| | Python | C++ |
|---|--------|-----|
| **语言根** | [python/notes.md](python/notes.md) | [cpp/notes.md](cpp/notes.md) |
| **数据结构** | [python/data_structures/notes.md](python/data_structures/notes.md) | [cpp/data_structures/notes.md](cpp/data_structures/notes.md) |
| **算法** | [python/algorithms/notes.md](python/algorithms/notes.md) | [cpp/algorithms/notes.md](cpp/algorithms/notes.md) |
| **刷题归档** | [python/problems/notes.md](python/problems/notes.md) | [cpp/problems/notes.md](cpp/problems/notes.md) |
| **面试专题** | [python/interview/notes.md](python/interview/notes.md) | [cpp/interview/notes.md](cpp/interview/notes.md) |

### 题单与题源索引

| | Python | C++ |
|---|--------|-----|
| **Hot 100** | [python/problems/hot100/notes.md](python/problems/hot100/notes.md) | [cpp/problems/hot100/notes.md](cpp/problems/hot100/notes.md) |
| **剑指 Offer 映射** | [python/problems/offer/notes.md](python/problems/offer/notes.md) | [cpp/problems/offer/notes.md](cpp/problems/offer/notes.md) |
| **CodeTop 映射** | [python/problems/codetop/notes.md](python/problems/codetop/notes.md) | [cpp/problems/codetop/notes.md](cpp/problems/codetop/notes.md) |
| **LeetCode 题解树** | `python/problems/leetcode/<slug>/` | `cpp/problems/leetcode/<slug>/`（命名见 [Repo layout](#repo-layout) 与下文 [Problem notes template](#problem-notes-template)） |
| **洛谷（预留）** | [python/problems/luogu/notes.md](python/problems/luogu/notes.md) | — |
| **牛客（预留）** | [python/problems/nowcoder/notes.md](python/problems/nowcoder/notes.md) | — |

### 面试 `interview/classic`（双语言）

| 专题 | Python | C++ |
|------|--------|-----|
| LRU | [classic/lru_cache](python/interview/classic/lru_cache/notes.md) | [classic/lru_cache](cpp/interview/classic/lru_cache/notes.md) |
| LFU | [classic/lfu_cache](python/interview/classic/lfu_cache/notes.md) | [classic/lfu_cache](cpp/interview/classic/lfu_cache/notes.md) |
| 单例 | [classic/singleton](python/interview/classic/singleton/notes.md) | [classic/singleton](cpp/interview/classic/singleton/notes.md) |
| 限流 | [classic/rate_limiter](python/interview/classic/rate_limiter/notes.md) | [classic/rate_limiter](cpp/interview/classic/rate_limiter/notes.md) |
| 环形缓冲 | [classic/ring_buffer](python/interview/classic/ring_buffer/notes.md) | [classic/ring_buffer](cpp/interview/classic/ring_buffer/notes.md) |
| 线程池 | [classic/thread_pool](python/interview/classic/thread_pool/notes.md) | [classic/thread_pool](cpp/interview/classic/thread_pool/notes.md) |
| 信号量 | [classic/semaphore](python/interview/classic/semaphore/notes.md) | [classic/semaphore](cpp/interview/classic/semaphore/notes.md) |
| 读写锁 | [classic/rwlock](python/interview/classic/rwlock/notes.md) | [classic/rwlock](cpp/interview/classic/rwlock/notes.md) |
| 写者优先 RWLock | [classic/rwlock_writer_pref](python/interview/classic/rwlock_writer_pref/notes.md) | [classic/rwlock_writer_pref](cpp/interview/classic/rwlock_writer_pref/notes.md) |
| Treiber 栈 | [classic/lockfree_stack](python/interview/classic/lockfree_stack/notes.md) | [classic/lockfree_stack](cpp/interview/classic/lockfree_stack/notes.md) |
| Ticket Lock | [classic/ticket_lock](python/interview/classic/ticket_lock/notes.md) | [classic/ticket_lock](cpp/interview/classic/ticket_lock/notes.md) |
| TAS 自旋锁 | [classic/tas_spinlock](python/interview/classic/tas_spinlock/notes.md) | [classic/tas_spinlock](cpp/interview/classic/tas_spinlock/notes.md) |
| MPMC 无锁队列 | [classic/mpmc_queue](python/interview/classic/mpmc_queue/notes.md) | [classic/mpmc_queue](cpp/interview/classic/mpmc_queue/notes.md) |
| 线程安全队列 | [classic/thread_safe_queue](python/interview/classic/thread_safe_queue/notes.md) | [classic/thread_safe_queue](cpp/interview/classic/thread_safe_queue/notes.md) |

### 面试高频题单 `top_frequent`

| | Python | C++ |
|---|--------|-----|
| 索引与题链 | [python/interview/top_frequent/notes.md](python/interview/top_frequent/notes.md) | [cpp/interview/top_frequent/notes.md](cpp/interview/top_frequent/notes.md) |

### 算法范式（一级目录，双语言）

| 范式 | Python | C++ |
|------|--------|-----|
| advanced（含莫队等） | [notes](python/algorithms/advanced/notes.md) | [notes](cpp/algorithms/advanced/notes.md) |
| backtracking | [notes](python/algorithms/backtracking/notes.md) | [notes](cpp/algorithms/backtracking/notes.md) |
| bit_manipulation | [notes](python/algorithms/bit_manipulation/notes.md) | [notes](cpp/algorithms/bit_manipulation/notes.md) |
| divide_and_conquer | [notes](python/algorithms/divide_and_conquer/notes.md) | [notes](cpp/algorithms/divide_and_conquer/notes.md) |
| dynamic_programming | [notes](python/algorithms/dynamic_programming/notes.md) | [notes](cpp/algorithms/dynamic_programming/notes.md) |
| graph | [notes](python/algorithms/graph/notes.md) | [notes](cpp/algorithms/graph/notes.md) |
| greedy | [notes](python/algorithms/greedy/notes.md) | [notes](cpp/algorithms/greedy/notes.md) |
| math | [notes](python/algorithms/math/notes.md) | [notes](cpp/algorithms/math/notes.md) |
| prefix_sum | [notes](python/algorithms/prefix_sum/notes.md) | [notes](cpp/algorithms/prefix_sum/notes.md) |
| recursion | [notes](python/algorithms/recursion/notes.md) | [notes](cpp/algorithms/recursion/notes.md) |
| searching | [notes](python/algorithms/searching/notes.md) | [notes](cpp/algorithms/searching/notes.md) |
| sliding_window | [notes](python/algorithms/sliding_window/notes.md) | [notes](cpp/algorithms/sliding_window/notes.md) |
| sorting | [notes](python/algorithms/sorting/notes.md) | [notes](cpp/algorithms/sorting/notes.md) |
| string | [notes](python/algorithms/string/notes.md) | [notes](cpp/algorithms/string/notes.md) |
| two_pointers | [notes](python/algorithms/two_pointers/notes.md) | [notes](cpp/algorithms/two_pointers/notes.md) |

### 动态规划子域

| 子域 | Python | C++ |
|------|--------|-----|
| linear | [notes](python/algorithms/dynamic_programming/linear/notes.md) | [notes](cpp/algorithms/dynamic_programming/linear/notes.md) |
| interval | [notes](python/algorithms/dynamic_programming/interval/notes.md) | [notes](cpp/algorithms/dynamic_programming/interval/notes.md) |
| tree | [notes](python/algorithms/dynamic_programming/tree/notes.md) | [notes](cpp/algorithms/dynamic_programming/tree/notes.md) |
| knapsack | [notes](python/algorithms/dynamic_programming/knapsack/notes.md) | [notes](cpp/algorithms/dynamic_programming/knapsack/notes.md) |
| digit | [notes](python/algorithms/dynamic_programming/digit/notes.md) | [notes](cpp/algorithms/dynamic_programming/digit/notes.md) |
| bitmask | [notes](python/algorithms/dynamic_programming/bitmask/notes.md) | [notes](cpp/algorithms/dynamic_programming/bitmask/notes.md) |

### 图算法子域

| 子域 | Python | C++ |
|------|--------|-----|
| traversal | [notes](python/algorithms/graph/traversal/notes.md) | [notes](cpp/algorithms/graph/traversal/notes.md) |
| shortest_path | [notes](python/algorithms/graph/shortest_path/notes.md) | [notes](cpp/algorithms/graph/shortest_path/notes.md) |
| mst | [notes](python/algorithms/graph/mst/notes.md) | [notes](cpp/algorithms/graph/mst/notes.md) |
| topological_sort | [notes](python/algorithms/graph/topological_sort/notes.md) | [notes](cpp/algorithms/graph/topological_sort/notes.md) |
| lca | [notes](python/algorithms/graph/lca/notes.md) | [notes](cpp/algorithms/graph/lca/notes.md) |
| scc | [notes](python/algorithms/graph/scc/notes.md) | [notes](cpp/algorithms/graph/scc/notes.md) |
| bipartite_matching | [notes](python/algorithms/graph/bipartite_matching/notes.md) | [notes](cpp/algorithms/graph/bipartite_matching/notes.md) |
| network_flow | [notes](python/algorithms/graph/network_flow/notes.md) | [notes](cpp/algorithms/graph/network_flow/notes.md) |

### 数据结构：一级目录

| 树干 | Python | C++ |
|------|--------|-----|
| linear | [notes](python/data_structures/linear/notes.md) | [notes](cpp/data_structures/linear/notes.md) |
| tree | [notes](python/data_structures/tree/notes.md) | [notes](cpp/data_structures/tree/notes.md) |
| graph（无一级 `notes`，从子域进入） | [adjacency_list](python/data_structures/graph/adjacency_list/notes.md) | [adjacency_list](cpp/data_structures/graph/adjacency_list/notes.md) |
| advanced | [notes](python/data_structures/advanced/notes.md) | [notes](cpp/data_structures/advanced/notes.md) |

### 数据结构：树专题（节选）

| 结构 | Python | C++ |
|------|--------|-----|
| binary_tree | [notes](python/data_structures/tree/binary_tree/notes.md) | [notes](cpp/data_structures/tree/binary_tree/notes.md) |
| bst | [notes](python/data_structures/tree/bst/notes.md) | [notes](cpp/data_structures/tree/bst/notes.md) |
| avl | [notes](python/data_structures/tree/avl/notes.md) | [notes](cpp/data_structures/tree/avl/notes.md) |
| red_black_tree | [notes](python/data_structures/tree/red_black_tree/notes.md) | [notes](cpp/data_structures/tree/red_black_tree/notes.md) |
| heap | [notes](python/data_structures/tree/heap/notes.md) | [notes](cpp/data_structures/tree/heap/notes.md) |
| trie | [notes](python/data_structures/tree/trie/notes.md) | [notes](cpp/data_structures/tree/trie/notes.md) |
| segment_tree | [notes](python/data_structures/tree/segment_tree/notes.md) | [notes](cpp/data_structures/tree/segment_tree/notes.md) |
| fenwick_tree | [notes](python/data_structures/tree/fenwick_tree/notes.md) | [notes](cpp/data_structures/tree/fenwick_tree/notes.md) |

### 数据结构：图表示与进阶（节选）

| | Python | C++ |
|---|--------|-----|
| adjacency_list | [notes](python/data_structures/graph/adjacency_list/notes.md) | [notes](cpp/data_structures/graph/adjacency_list/notes.md) |
| adjacency_matrix | [notes](python/data_structures/graph/adjacency_matrix/notes.md) | [notes](cpp/data_structures/graph/adjacency_matrix/notes.md) |
| disjoint_set | [notes](python/data_structures/graph/disjoint_set/notes.md) | [notes](cpp/data_structures/graph/disjoint_set/notes.md) |
| skip_list | [notes](python/data_structures/advanced/skip_list/notes.md) | [notes](cpp/data_structures/advanced/skip_list/notes.md) |
| bloom_filter | [notes](python/data_structures/advanced/bloom_filter/notes.md) | [notes](cpp/data_structures/advanced/bloom_filter/notes.md) |
| lru_cache（结构向） | [notes](python/data_structures/advanced/lru_cache/notes.md) | [notes](cpp/data_structures/advanced/lru_cache/notes.md) |

---

### 封版与后续维护（默认约定）

- **不冻结 `main`**：默认可继续合并 typo、链接修复与小改进；若你希望阶段性只读，请在 **本 README** 文首或本节自行写明策略并约束协作流程。
- **新题 / 新专题**：推荐在 **feature 分支** 开发后合并到 `main`。若将来拆到新仓库，再在 **本 README 最上方** 增加一行「继任仓库：`<URL>`」即可。
- **回归与快照**：请自行运行相关 `solution.py` / `g++` 编译；大改后可按需对 `python/`、`cpp/` 分批自测。不再提供仓库级一键脚本。

---

## 仓库约定（请先读）

| 约定 | 说明 |
|------|------|
| **根目录 Markdown** | **仅本文件 `README.md`**；不放其它 `.md`（约定、模板、工具链、待办、变更日志均写在本文附录锚点）。 |
| **子目录说明** | 各专题说明文件统一命名为 **`notes.md`**。 |
| **题目目录** | LeetCode 等：`python/problems/leetcode/<四位编号>_<snake_case>/` 与 `cpp/...` 对称；每题 **`notes.md` + `solution.py` / `solution.cpp`**（末尾自带简单断言或样例）；SQL 题为 `solution.sql`。 |
| **Hot 100 索引** | 点赞序题单表见 `python/problems/hot100/notes.md` 与 `cpp/problems/hot100/notes.md`（与题号数值顺序无关；**手工**与题解目录对齐维护）。 |
| **变更摘要** | 见本文 **[Changelog](#changelog)**（细粒度以 `git log` 为准） |

---

## 顶层目录一览

```
Algorithm/
├── README.md          ← 全库唯一 .md 入口（本文件）+ 约定与附录
├── python/            ← Python：data_structures / algorithms / problems / interview
└── cpp/               ← C++：与 python/ 同构
```

---

## 快速开始

### Python

```powershell
Set-Location F:\Study\Algorithm
python python\problems\leetcode\0001_two_sum\solution.py
```

建议 **Python 3.10+**（广泛使用 `list[int]` 等内置泛型注解）。语言总入口：[python/notes.md](python/notes.md)。

### C++（MinGW / LLVM）

```powershell
Set-Location F:\Study\Algorithm\cpp\problems\leetcode\0001_two_sum
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe solution.cpp
.\run.exe
```

含 `std::thread` 的示例需加 **`-pthread`**。习惯命令见 [cpp/notes.md](cpp/notes.md)。若无 `g++`、仅安装 **MSVC**，编译约定见本文 **[C++ toolchain](#cpp-toolchain)**。

---

## 你想快速去哪？

| 你想… | 去哪里 |
|--------|--------|
| 看数据结构专题与代码 | [python/data_structures/notes.md](python/data_structures/notes.md) / [cpp/data_structures/notes.md](cpp/data_structures/notes.md) |
| 看算法分类（DP、图、字符串等） | [python/algorithms/notes.md](python/algorithms/notes.md) / [cpp/algorithms/notes.md](cpp/algorithms/notes.md) |
| 刷题归档与题源约定 | [python/problems/notes.md](python/problems/notes.md) / [cpp/problems/notes.md](cpp/problems/notes.md) |
| Hot 100 点赞序索引 | [python/problems/hot100/notes.md](python/problems/hot100/notes.md) |
| 手写专题（并发与经典题） | [python/interview/notes.md](python/interview/notes.md) |
| 覆盖盘点（P0） | 见本文 [Coverage](#coverage) |
| 未完成待办 | 见本文 [Pending tasks](#pending-tasks) |

---

## 当前进度（摘要）

- **数据结构**：第一阶段已按专题铺全（双语言 + `notes.md`）。
- **算法**：第二阶段各子目录已有范式示例与说明。
- **LeetCode Hot 100**：已对齐收录（**99** 题 Python+C++，**LC 175** 为 SQL-only）；索引见上表 Hot 100 链接。
- **面试第四阶段**：`interview/classic/` 与 `interview/top_frequent/`（双语文首含与 `leetcode/` 同步说明）。

详细**未完成**与 P1 标准见本文 **[Pending tasks](#pending-tasks)**；**覆盖与总表入口**见 **[Coverage](#coverage)**。

---

## 新题入库流程（极简）

1. 在 `python/problems/leetcode/` 与 `cpp/problems/leetcode/` 下各建同名目录 `NNNN_snake_case/`。  
2. 复制本文 **[Problem notes template](#problem-notes-template)** 到两边的 **`notes.md`**。  
3. 编写 `solution.py` / `solution.cpp`，末尾保留可本地运行的自检。  
4. 若该题属于 Hot 100：同步更新 `python/problems/hot100/notes.md` 与 `cpp/problems/hot100/notes.md` 中对应表格行（点赞序与指向 `leetcode/` 的链接）。

---

## Study roadmap

可按个人节奏调整；路径与 `python/`、`cpp/` 下同构目录对应。

### 基础

1. **线性结构**：数组、链表、栈、队列、哈希表（`data_structures/linear/`）
2. **排序与查找**：`algorithms/sorting/`、`algorithms/searching/`
3. **递归与分治**：`algorithms/recursion/`、`algorithms/divide_and_conquer/`

### 进阶

1. **树与堆**：`data_structures/tree/`
2. **图**：表示、遍历、最短路、拓扑（`data_structures/graph/`、`algorithms/graph/`）
3. **双指针 / 滑动窗口 / 前缀和**：`two_pointers`、`sliding_window`、`prefix_sum`；**莫队**见 `algorithms/advanced/mo_algorithm/`；**树上 LCA** 见 `algorithms/graph/lca/`

### 专题

1. **动态规划**：线性、区间、树形、背包、数位、状压（`algorithms/dynamic_programming/`）
2. **贪心、回溯、位运算**：对应子目录
3. **字符串**：KMP、Trie 等（`algorithms/string/`）
4. **数学**：数论、组合、矩阵等（`algorithms/math/`）

### 刷题与面试

- 日常：`problems/leetcode/` 等按来源归档
- 面试：`interview/classic/`、`interview/top_frequent/`（表与 `leetcode/` 同步维护）

## Repo layout

```
Algorithm/
├── README.md          # 全库唯一 .md 入口（本文件）+ 约定与附录
├── python/            # data_structures / algorithms / problems / interview
└── cpp/               # 与 python/ 镜像同构
```

## Coverage

条目级「有哪些实现 / 缺口在哪」不再维护独立 Markdown 目录；请以 **双语言总入口表** 为准，并随代码更新：

- [python/algorithms/notes.md](python/algorithms/notes.md) / [cpp/algorithms/notes.md](cpp/algorithms/notes.md)
- [python/data_structures/notes.md](python/data_structures/notes.md) / [cpp/data_structures/notes.md](cpp/data_structures/notes.md)

## Problem notes template

复制到新题目目录，保存为 **`notes.md`** 后填空。

### 题面

- **来源**：（如 LeetCode 1）
- **链接**：
- **难度 / 标签**：（可选，便于检索）
- **简述**：

### 思路

1. 解法一：
2. 解法二（可选）：

### 复杂度

| 解法 | 时间 | 空间 |
|------|------|------|
| | | |

### 自测与边界

- 样例、小规模手造、极端（空、单点、全相同、上限）；（C++/Python）末尾 `main` / `if __name__ == "__main__"` 断言习惯与仓库其他题一致。

### 陷阱与注意

-

### 相关题目

-

## C++ toolchain

本仓库 C++ 源码**不再依赖** GCC 专有的 `<bits/stdc++.h>`，统一通过 [`cpp/include/alg_std.hpp`](cpp/include/alg_std.hpp) 引入常用标准库头，便于 **MSVC** 与 **MinGW g++** 共用同一套源码。

### 新文件 / 新题解

```cpp
#include <alg_std.hpp>
#include <cassert>  // 若写 assert 自测，建议保留（alg_std 已含，显式写更清晰）
using namespace std;
```

编译时加上 include 路径：`-I cpp/include`（`g++` / `cl` 均需显式传入，见下表）。

### 回归与批量编译

自行在仓库根用 PowerShell 或编辑器任务对关心的 `cpp/**/*.cpp` 执行 `g++ -std=c++17 -c -Wall -Wextra -I cpp/include`；对 Python 则直接 `python path\to\solution.py`。本仓库不再附带批处理脚本。

可选 MSVC（需 `cl` 在 PATH 或已运行 `vcvars64.bat`）：

```powershell
cl /std:c++17 /c /EHsc /I cpp\include path\to\solution.cpp
```

### 编译器对照

| 项 | MinGW g++（默认） | MSVC `cl` |
|----|-------------------|-----------|
| 标准 | `-std=c++17` | `/std:c++17` |
| Include | `-I cpp/include` | `/I cpp\include` |
| 多线程 | `-pthread` | 默认支持；链接时一般无需额外开关 |
| 单文件编译 | `g++ -c ...` | `cl /c /EHsc ...` |

### assert 自测注意

- `assert(表达式含逗号的初始化列表)` 会被宏按逗号拆参，应先赋给临时变量再断言。

## Pending tasks

> **项目第一目标**：把常见算法与数据结构 **成体系、双语言、可运行自测** 地整理进本仓库（`algorithms/` + `data_structures/`），并与刷题归档、面试专题形成闭环。

**完成标准（P1，全部满足即配套收口）**：

| 指标 | 基线（当前） | 目标 |
|------|----------------|------|
| `problems/leetcode/` 题量 | **120**（含 307 区间结构代表题） | **120** |
| `algorithms/notes` 刷题索引 | **已完成**（含莫队/网络流说明行 + **307** 区间结构） | **每行有链**或写明「无 LeetCode 标配」 |
| `data_structures/notes` 刷题索引 | **已完成**（含 **307** 线段树/树状数组） | 各结构均有代表题链 |
| `interview/top_frequent/` | **冻结 v1（103）** | 扩题须先改本 README [Pending tasks](#pending-tasks) 并**同步** py/cpp 两份 `interview/top_frequent/notes.md` 文首说明与表格 |
| `problems/offer/`、`codetop/` | **30+30** 行索引 | 各 **30** 行映射（≥90% 链到已有 `leetcode/`） |
| `interview/classic/` | **14** 份 `notes.md` 含「面试要点」 | 同上 |

**原则**：不为刷数量重复建题；大改后请自行运行相关 `solution.py` / `g++` 做抽样或全量验证。

### 封版收尾（须你本地完成）

- [ ] **提交 + 打 tag**：工作树干净 → `git tag` / `git push`（标签名自定）；可选 GitHub **Release**、MSVC 冒烟（见上文 [C++ toolchain](#cpp-toolchain)）。
- [ ] 上述完成后，**删除这两条**（本节只保留未完成项）。

## Changelog

以 **`git log`** 与**本 README** 为主变更说明；此处仅记里程碑摘要。

### [未发布]

- 已移除 **`scripts/`** 维护脚本目录及依赖该目录的 **GitHub Actions** workflow；回归与索引维护改为本地手工 / 自建命令。

### 里程碑（摘要）

- 双语言 **算法 / 数据结构** 与 `notes.md` 体系、`leetcode/` 归档、面试专题（`interview/classic`、`top_frequent`）。

---

## 许可与声明

题目版权归 respective 平台（如 LeetCode）；本仓库代码与文字说明为个人学习整理，按你本地习惯决定是否开源协议；转载题目描述请注意平台条款。

若你发现某处仍残留旧链接或命名，欢迎直接改 **`notes.md`** 或 **本 README** 并提交修正。
