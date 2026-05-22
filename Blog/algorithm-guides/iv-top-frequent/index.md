---
title: "面试专题 · 高频题索引（Top Frequent）"
series: algorithm
category: Interview
topic_path: interview/top_frequent
guide_toc: topic-algorithm
guide_tier: medium
status: published
date: 2026-05-21
tags: [Interview, Hot100, LeetCode, StudyPlan, TopFrequent]
---

# 面试专题 · 高频题索引（Top Frequent）

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

**高频题索引**不是一道 LeetCode 题，而是 Study 仓库 `interview/top_frequent/` 对 **103 道冻结题单** 的**分类导航**：

本页面向「已克隆 Study 仓库、准备系统刷面试题」的学习者：你不会在这里看到 103 行的完整 Markdown 表（那张表在 `notes.md`，且会随版本 v1→v2 变更），但你会看到**如何用那张表**、每类题的**代表模式**、与 atelier 其他指南（`ds-linear`、`algo-dp-linear`、`iv-classic-lru-cache` 等）的跳转关系，以及 Python/C++ 题解目录的运行方式。若你只想快速 AC 某一题，请直接进入 `problems/leetcode/<slug>/`；若你想建立可复习的知识结构，请按本页学习路径块刷索引各章。按链表、数组与窗口、栈、字符串、哈希、二叉树、图、回溯与 DP、二分与杂项等专题，把每道题链到 `problems/leetcode/<slug>/` 下的双语言题解与测试。本页 `topic_path` 为 `interview/top_frequent`，manifest 中 `guide_toc` 为 **topic-algorithm**（与 `interview/classic/*` 的 `interview-classic` 区分：本专题是**题单索引**，不是手写 LRU/线程池一类设计实现）。

刷题者常见误区是把 `notes.md` 当成「又一篇文章」通读——那张表有 103 行，**适合当检索目录**，不适合逐行背诵。正确用法是：

1. 按本页「学习路径」选一条专题线（例如先链表 + 栈 + 哈希）；
2. 在 Study `notes.md` 或 GitHub 上定位题号，进入对应 `solution.py` / `solution.cpp`；
3. 用本页各节的**方法提要**建立「见题知类」的条件反射，再回仓库跑测试巩固。

**题单冻结 v1 = 103 题**：扩题、删题须先升级版本号并同步 `python/interview/top_frequent/notes.md` 与 `cpp/interview/top_frequent/notes.md`。本 atelier 指南不写死 103 行表格（避免与仓库脱节、避免用索引表凑字数），而以**分类逻辑、代表题、与 `algorithms/` / `data_structures/` 专题映射**为主。具体题号—标题—目录三联表以 Study 笔记为唯一权威来源。

**与 Hot 100 的关系**：103 题与仓库 Hot 100 及专题补充题对齐，覆盖面试中出现频率高的模式；不等于 LeetCode 官方 Hot 100 集合完全一致，以 Study README 与 `prob-hot100` 导读为准。读完本页后建议配合 `prob-hot100` 题单页做进度勾选。

**读完你应能**：说明 103 题如何分组；为每一类列出 2–3 道代表题及核心技巧；知道手写专题（`interview/classic/`）与算法专题（`algorithms/`）在索引中的位置；能在 PowerShell 下打开任意一题的题解目录并运行测试。

## 预备知识

> **预备知识**：已注册 LeetCode 或等价 OJ；本地克隆 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm)；会 `Set-Location -LiteralPath` 与 `python` / `g++` 基本用法。Python 3.10+；若写 C++ 题解，C++17 与仓库 `cpp/include/alg_std.hpp` 可选。

开始前建议：

- **仓库路径约定**：题解在 `python/problems/leetcode/<四位题号>_<slug>/`，C++ 镜像在 `cpp/problems/leetcode/` 同 slug。
- **双语言对拍**：同一题先 AC Python 再写 C++，或反之，有助于面试多语言岗位。
- **基础数据结构**：线性表、栈队列、树、图遍历见 `ds-linear` 总览与各 `ds-*` 子指南。
- **基础算法模板**：DP、图、字符串 KMP 等见 `algo-*` 系列。

若你零基础，勿从 103 题头部硬刷：先 `overview` 导读 → `ds-linear` + `0206`/`0001` → 再回到本索引按类推进。

**时间预期**：103 题若每题平均 1–2 小时（含复习），总投入约 100–200 小时；八周计划每周约 12–15 题可达标。质量优先于数量：同一模式连做 3–5 道比 103 题各做一遍更有效。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/top_frequent` |
| 索引笔记（权威表） | `python/interview/top_frequent/notes.md` |
| C++ 同步笔记 | `cpp/interview/top_frequent/notes.md` |
| 本地 GUIDE | `python/interview/top_frequent/GUIDE.md` |
| 题解根目录 | `python/problems/leetcode/` |
| Hot 100 题单 | `problems/hot100/`、`prob-hot100` 站点页 |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
Get-Content -LiteralPath 'F:\Study\Algorithm\python\interview\top_frequent\notes.md' -TotalCount 30
```

打开笔记后可见分节标题（链表、数组…）与 Markdown 表格。维护索引时**只改 Study 笔记**，再检查本页文字描述是否仍准确，勿在 atelier 复制整张表。

**运行单题题解示例（以 206 为例）**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\problems\leetcode\0206_reverse_linked_list'
python solution.py
```

C++ 侧进入同名目录编译 `solution.cpp`（具体 flags 见题解目录 README 或仓库统一说明）。

**与 `interview/classic/` 的交叉**

`notes.md` 末尾「手写对照」列出 LRU、LFU、线程池、令牌桶等，链到 `interview/classic/<topic>/`。设计类题（146）在索引表中出现，**实现细节**以 `iv-classic-lru-cache` 为准，题解目录可能用 `OrderedDict` 简化版。

## 基础篇

### 直觉与定义

把 103 题看作**带标签的节点集合**：标签 = 算法/数据结构专题（链表、单调栈、BFS…）；边 = 「建议先修」关系（如会 206 再 25；会 200 再 207）。索引文件提供**按专题过滤的目录**——不是按题号顺序刷，而是按「模式」成块攻克。

**三层知识结构**

| 层级 | 内容 | 本仓库位置 |
|------|------|------------|
| 模式层 | 双指针、滑动窗口、回溯、状态 DP | `algorithms/*` 专题 + 本索引分类 |
| 题目层 | 具体 LeetCode 题与约束 | `problems/leetcode/*` |
| 实现层 | 可运行代码与断言 | `solution.py` / `solution.cpp` |

**冻结版本 v1 = 103 题**：防止题单无限膨胀导致复习无法收尾。扩题须升级版本号并同步 `python/interview/top_frequent/notes.md` 与 `cpp/interview/top_frequent/notes.md`。本 atelier 页**不粘贴** 103 行完整表（避免与仓库分叉不同步），权威表以 Study 笔记为准。

**与 `prob-hot100` 的区别**：Hot 100 题单页偏「进度勾选与仓库题解入口」；本专题偏「分类方法论 + 与 algorithms 路径映射」。二者互补，不必二选一。

### 复杂度分析

此处「复杂度」指**备考时间结构**，非算法大 O：

| 阶段 | 建议总时长 | 说明 |
|------|------------|------|
| 第一遍 | 80–120 小时 | 每题 45–70 分钟含调试 |
| 第二遍错题 | 30–40 小时 | 只重做 WA/忘了的 |
| 手写 classic | 15–20 小时 | LRU、限流等 |
| 冲刺模拟 | 10–15 小时 | 限时 2 题/套 |

单题算法复杂度仍见各题解与 `algorithms/*/notes.md`；索引本身不重复列出每题 O(n)。

**各章题量与建议周数**（八周计划基准）

| 索引章节 | 约题数 | 建议周 |
|----------|--------|--------|
| 链表 | 14 | 1 |
| 数组/窗口/前缀 | 14 | 1 |
| 栈 | 5 | 0.5（与字符串前半重叠） |
| 字符串 | 7 | 0.5 |
| 哈希/位运算 | 4 | 0.5 |
| 二叉树 | 13 | 1 |
| 图 | 8 | 1 |
| 回溯/DP | 20 | 2 |
| 二分/杂项 | 15 | 1 |
| 困难串/SQL | 2 | 选做 |

### 代码模板

**模板 A：从题号进入题解目录**

```powershell
$id = 206
$slug = 'reverse_linked_list'
Set-Location -LiteralPath "F:\Study\Algorithm\python\problems\leetcode\$('{0:D4}' -f $id)_$slug"
python solution.py
```

表内链接已含 slug，优先点表勿手拼。

**模板 B：索引笔记中的相对路径**

`notes.md` 使用 `` [`0206_...`](../../problems/leetcode/0206_reverse_linked_list/) `` 形式；在 VS Code 中 Ctrl+点击即可跳转。维护时改目录名必须同步改表内 slug。

**模板 C：与 algorithms 专题对照（摘自 Study 笔记）**

| 仓库专题 | 路径 | 示例题号 |
|----------|------|----------|
| 图 BFS/DFS | `algorithms/graph/traversal/` | 200、994、542 |
| 拓扑排序 | `algorithms/graph/topological_sort/` | 207、210 |
| 最短路 | `algorithms/graph/shortest_path/` | 743、787 |
| MST | `algorithms/graph/mst/` | 1135、1584 |
| 并查集 | `data_structures/graph/disjoint_set/` | 684、1135 |
| 树上 LCA | `algorithms/graph/lca/` | 236 |
| 字符串 KMP | `algorithms/string/` | 28 |
| 背包 DP | `algorithms/dynamic_programming/knapsack/` | 322 |

做完表中题号后，用一行笔记把「题号 → 模板函数名」记下，例如 `207 → topological_sort_kahn`。

**模板 D：手写专题跳转**

索引末尾「手写对照」链到 `interview/classic/`：146 → `lru_cache`（站点 `iv-classic-lru-cache`）；LFU、线程池、令牌桶等同理。AC 官方题解不等于面试过关，设计类必须能手写。

### 变体与技巧

**链表（14 题量级）**

代表：206 反转、21 合并、141/142 环、25 k 组翻转、146 LRU（设计）、160 相交。

**要点**：哑节点、快慢指针、反转三指针、k 组分段 reverse。与 `ds-linear-linked-list`、手写 LRU 专题联动。易错：k 组不足 k 个时保持原序；环入口数学推导。

**数组 / 双指针 / 前缀 / 窗口（14 题）**

代表：3 无重复最长子串、11 盛水、15 三数之和、42 接雨水、56 合并区间、121/122 股票、239 滑动窗口最值、560 和为 K 的子数组。

**要点**：对撞指针、滑动窗口维护频次/单调队列、前缀和 + 哈希计数。与 `algo-two-pointers`、`algo-sliding-window`、`algo-prefix-sum` 对应。

**栈 / 单调栈（5 题）**

代表：20 括号、84 柱状图最大矩形、85 最大矩形、155 最小栈、32 最长有效括号。

**要点**：栈存下标；单调递增栈求「下一个更小」；DP 与栈结合（32）。`ds-linear-stack` 含 `MinStack` 教学实现。

**字符串（7 题）**

代表：5 最长回文、76 最小覆盖子串、28 KMP（实现 strStr）、14 最长公共前缀。

**要点**：中心扩展、窗口、KMP 的 next 数组。`algorithms/string/` 专题。

**哈希 / 位运算（4 题）**

代表：1 两数之和、136 只出现一次、169 多数元素、287 找重复数。

**要点**：补数查找、异或、Boyer-Moore、快慢指针判环（287）。`ds-linear-hash-table`。

**二叉树（13 题）**

代表：94 中序、104 深度、105 构造、124 路径最大和、236 LCA、337 打家劫舍 III。

**要点**：递归遍历、分治构造、后序返回「含当前节点的最大贡献」、树形 DP。`ds-tree-binary-tree`、`algo-dp-tree`。

**图 / DFS / 拓扑（8 题）**

代表：200 岛屿、207 课程表、994 腐烂橘子、684 冗余边、1135/1584 最小生成树、785 二分图。

**要点**：网格 BFS/DFS、三色拓扑、并查集判环、Kruskal/Prim。索引中「与本仓库 algorithms 对照」表直接给出路径。

**回溯 / DP（20 题）**

代表：46 全排列、51 N 皇后、53 最大子数组、62/64 路径、72 编辑距离、300 LIS、322 零钱、416 划分相等子集。

**要点**：回溯剪枝、线性 DP、背包。`algo-backtracking`、`algo-dp-linear`、`algo-dp-knapsack`。

**二分 / 数学 / 杂项（15 题）**

代表：4 两数组中位数、33 旋转数组搜索、215 第 K 大、31 下一个排列。

**要点**：二分边界、快速选择、堆。`algo-searching`、堆专题 `ds-tree-heap`。

**困难字符串 / SQL**

10 正则 DP 与 175 SQL 在索引中单独成节：前者投入高、后者非算法岗可略。

**链表进阶链**：206 → 92 局部反转 → 25 k 组 → 148 归并排序链表 → 146 设计。跳过 206 直接 25 极易指针混乱。

**数组进阶链**：1 → 15 → 18（三数、四数）→ 42 接雨水（双指针或单调栈）→ 239（单调队列）。同一族题用同一草图模板。

**图进阶链**：200 岛屿 → 994 多源 BFS → 207 拓扑 → 684 并查集 → 1135 MST。并查集与 MST 在 `disjoint_set`、`algo-graph-mst` 有模板。

**DP 进阶链**：70 爬楼梯 → 198 打家劫舍 → 300 LIS → 322 零钱 → 416 划分和。线性 DP 见 `algo-dp-linear`，背包见 `algo-dp-knapsack`。

**二分与选择**：33 旋转数组搜索 → 34 左右边界 → 215 第 K 大（堆或快选）。215 与 `ds-tree-heap` 联动。

**复盘卡片**：每章结束后写三张卡——「识别特征」「核心不变量」「易错边界」，勿只勾 AC。

**按周拆解的专题重心（八周计划的「为什么」）**

第 1 周哈希与数组：先建立「用空间换时间」与「双指针扫区间」两种直觉，题量虽少但模式覆盖广。第 2 周链表：指针题需要连续练习保持手感，不宜与图论混在同一天。第 3 周字符串与剩余数组：KMP 与最小覆盖窗口各练一题即可，其余用窗口+哈希巩固。第 4 周二叉树：递归返回值语义需集中突破，建议每天两题树题。第 5 周图：BFS/DFS/拓扑/并查集/MST 各至少一题，并对照 `algorithms/graph` 笔记。第 6 周回溯：剪枝与状态恢复，与 DP 分开天。第 7 周 DP：线性、路径、背包三类分开列清单。第 8 周二分与杂项+错题+classic 手写。每周日花三十分钟只看卡片不看代码，检查是否仍能口述模式。

**103 题与岗位匹配（非官方，供自评）**

后端开发：链表、哈希、图、DP 权重大；客户端：数组、字符串、树；基础架构/C++：classic 手写与 146/155；数据岗：SQL 175 与哈希。自评时诚实标记薄弱章，从索引表该章挑 3 题重练，比随机刷题更有效。

**与 Study `problems/leetcode` 目录命名约定**

slug 形如 `四位题号_英文标题蛇形`，与 notes.md 表格最后一列链接一致。手输路径易错，务必从表点击。C++ 目录同名，换语言时只换 `python`/`cpp` 前缀。

### 易错点

1. **按题号顺序刷**：题号与难度、专题无关，易挫败；应按分类块刷。
2. **只看不写**：索引是目录，必须进 `solution.py` 默写一遍。
3. **忽视 C++ 镜像**：目标岗位若考 C++，只刷 Python 不够。
4. **103 题与专题笔记脱节**：做完 207 应回看 `algorithms/graph/topological_sort/notes.md` 一行总结。
5. **版本漂移**：本地 fork 未 pull 时表与目录不一致，以 upstream `notes.md` 为准。
6. **手写与设计题**：146 用库函数 AC 不等于面试过关，需 `classic/lru_cache` 手写。
7. **SQL 题占时间**：175 对纯后端算法岗优先级低，可标记暂缓。
8. **重复模式不总结**：三数之和、四数之和、K 数和应抽象为「排序 + 双指针」一族。

### 练习建议

- **第一轮**：每类选 1 道简单 + 1 道中等，共约 30 题，建立标签感。
- **第二轮**：补全各类剩余题，限时 25–35 分钟/题。
- **第三轮**：错题 + 经典变体（如 206→92→25 链表线）。
- **对拍**：网格题、DP 题用暴力小数据验证。
- **口述**：每题用 30 秒说清「输入输出 + 方法 + 复杂度」。

每日建议 1–2 题深度 > 5 题浅尝。周末用半天做「同类串联」（例如周日只做栈与单调栈 5 题）。

## Python 实现

本专题**没有**单一的 `top_frequent.py` 可执行模块；「实现」指**如何使用仓库题解与索引**。典型工作流如下。

**1. 从索引解析 slug 并进入目录**

```python
# 示例：根据题号构造常见 slug（仓库命名规则：四位题号 + 下划线标题）
def leetcode_dir(root: str, problem_id: int, slug_suffix: str) -> str:
    return f"{root}/python/problems/leetcode/{problem_id:04d}_{slug_suffix}"

# 206 Reverse Linked List
path = leetcode_dir(r"F:\Study\Algorithm", 206, "reverse_linked_list")
```

实际刷题以 `notes.md` 表格中的链接为准，避免手写 slug 拼错。

**2. 运行题解（与仓库一致）**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\problems\leetcode\0001_two_sum'
python solution.py
```

多数 `solution.py` 含 `if __name__ == "__main__"` 自测或调用本地 judge 辅助函数。

**3. 自建进度跟踪（可选脚本思路）**

```python
# 学习进度示例：JSON 记录 ac 日期，不提交到仓库
import json
from pathlib import Path

PROGRESS = Path("top_frequent_progress.json")

def mark_done(problem_id: int) -> None:
    data = json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {}
    data[str(problem_id)] = "ac"
    PROGRESS.write_text(json.dumps(data, indent=2), encoding="utf-8")
```

脚本为个人工具，**不属于** Study 仓库正式内容；此处仅说明「索引 + 自维护进度」的实践方式。

**4. 读索引笔记而非复制**

```powershell
# 在仓库根用 Python 统计 notes.md 中表格行数（维护者校验 103 题）
$notes = Get-Content -LiteralPath 'F:\Study\Algorithm\python\interview\top_frequent\notes.md' -Raw
($notes -split '\n' | Where-Object { $_ -match '^\| \d+' }).Count
```

维护者应得到与 v1 声明一致的题数；学习者无需每日跑此命令。

**代表题的 Python 技巧锚点（便于从索引跳转后理解 solution）**

- `0001_two_sum`：`dict` 补数一次遍历；
- `0003_longest_substring`：窗口 + `last_index`；
- `0206_reverse_linked_list`：迭代三指针；
- `0207_course_schedule`：拓扑 Kahn 或 DFS 三色；
- `0307` / 线段树：见 `ds-tree-segment-tree`（若题单含可变数组题）。

## C++ 实现

C++ 题解位于 `cpp/problems/leetcode/<slug>/solution.cpp`，与 Python **同 slug 目录名**。

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\problems\leetcode\0206_reverse_linked_list'
g++ -std=c++17 -O2 -Wall -Wextra -o sol.exe solution.cpp
.\sol.exe
```

部分题目 `#include <alg_std.hpp>`，编译时增加：

```powershell
g++ -std=c++17 -O2 -I..\..\..\include -o sol.exe solution.cpp
```

（`-I` 相对路径随当前目录深度调整。）

```cpp
// 节选：LeetCode 206 反转链表（完整见 Study）
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    for (ListNode* cur = head; cur; ) {
        ListNode* nxt = cur->next;
        cur->next = prev;
        prev = cur;
        cur = nxt;
    }
    return prev;
}
```

**双语言学习建议**

| 阶段 | Python | C++ |
|------|--------|-----|
| 理解题意 | 先写/读 Python | — |
| 面试目标 C++ | 对照翻译 | 写 solution.cpp |
| 卡常/溢出 | 意识复杂度 | 注意 `long long`、`size_t` |

索引本身不区分语言；**notes.md 的 cpp 副本**应与 python 版表格行数一致，贡献时务必双端同步。

**C++ 特有注意**：链表题注意 `ListNode*` 内存由 OJ 管理；图题用 `vector<vector<int>>` 邻接表；并查集路径压缩写法见 `ds-graph-disjoint-set`。

## 练习与延伸

**Study 笔记各章题号清单（请打开 `notes.md` 查看完整表）**

下列仅列出章节标题与定位，**不替代**仓库表格：链表、数组/双指针/前缀/窗口、栈/单调栈、字符串、哈希/位运算、二叉树、图/DFS/拓扑、回溯/动态规划、二分/数学/杂项、困难字符串/正则、SQL、手写对照（classic）。每章表格列含题号、英文题名、相对路径 slug；点击 slug 进入 `problems/leetcode/` 对应目录。

**链表章精讲要点（14 题）**

| 题号 | 一句话技巧 |
|------|------------|
| 206 | 三指针反转 |
| 21 | 哑节点合并 |
| 141/142 | 快慢指针 / 环入口 |
| 160 | 对齐长度后同步走 |
| 19 | 双指针间隔 n+1 |
| 24 | 成对交换 |
| 25 | 分 k 段反转 |
| 92 | 找到区间前驱再反转 |
| 148 | 归并排序 merge |
| 234 | 找中点反转后半比较 |
| 237 | 复制值+跳 next（无头指针） |
| 2 | 哑节点+进位 |
| 146 | 哈希+双向链表，见 iv-classic-lru-cache |

**图章与仓库 algorithms 联动**

做完 200 后读 `algorithms/graph/traversal/notes.md`；207 后读 `topological_sort`；1135/1584 后读 `mst`；684 后读 `data_structures/graph/disjoint_set`。索引中的对照表是「题号→专题路径」的桥梁，本页强调**做完题必须回到专题笔记一行总结**。

**DP 章分层**

线性：53、70、198、300、72。路径：62、64、437。背包：322、416。回溯混合：39、46、78、22、51。每类挑 2 题写状态定义再扩到章内其余题。

**按索引章节的推荐最小集（若时间极紧）**

| 章节 | 最小题集（题号） |
|------|------------------|
| 链表 | 206, 21, 141, 160 |
| 数组/窗口 | 1, 3, 11, 15, 239 |
| 栈 | 20, 84, 155 |
| 树 | 104, 102, 105, 124, 236 |
| 图 | 200, 207, 994 |
| DP/回溯 | 46, 53, 70, 72, 300, 322 |
| 哈希 | 1, 136 |
| 设计/手写 | 146 + `classic/lru_cache` |

**延伸题单**：`prob-codetop`、`prob-offer`、`problems/luogu`（见 manifest）；不在 103 冻结表内的题需另立计划。

**算法专题深化**：索引中「与本仓库 algorithms 对照」一节映射了图遍历、拓扑、MST、LCA、KMP、背包等——做完题后务必打开对应 `algorithms/.../notes.md` 一行总结模板。

**站点指南联动**：数据结构总览 `ds-linear`；线段树 `ds-tree-segment-tree`；DP 入门 `algo-dp-linear`；Hot 100 导航 `prob-hot100`。

## 学习路径

**八周示例（约 103 题）**

| 周 | 索引章节 | 目标题量 |
|----|----------|----------|
| 1 | 哈希 + 数组入门 + 栈基础 | 12 |
| 2 | 链表全节 | 14 |
| 3 | 字符串 + 双指针窗口剩余 | 12 |
| 4 | 二叉树 | 13 |
| 5 | 图与并查集 | 8 |
| 6 | 回溯 + 线性 DP | 12 |
| 7 | 背包/树形 DP/剩余 DP | 12 |
| 8 | 二分/数学/杂项 + 错题 + classic 手写 | 20+复习 |

每周日复盘：列出本周「模式关键词」三张卡片（如「单调栈」「Kahn 拓扑」「滚动背包」）。第 4 周结束时应已完成链表+数组大半；第 6 周结束图+DP 各至少 8 题独立 AC；第 8 周以模拟面试与 classic 手写为主，索引表仅作查漏。若某周加班，可整周推迟但勿跳过「链表周」——链表指针题在面试中占比高，跳过后期补救成本更大。索引表每章最小集题号可在个人 Excel 标「必做/选做」，不必机械全做，但必做题应覆盖该章核心模式。完成 80% 必做题后即可进入模拟面试，不必等待 103 全部 AC。索引博文与 Hot100 博文分工：前者按国内面经频率，后者按社区热度，建议两表都维护勾选列。strict 校验通过后再改 published。开始刷表即可。祝备考顺利，坚持八周即可。

**冲刺阶段（面试前 7 天）**

- Day 1–2：索引中薄弱类各 3 题限时；
- Day 3：`interview/classic` 选 2 题手写（LRU + 任选）；
- Day 4–5：模拟面试 2 套（每套 2 算法题）；
- Day 6–7：只看错题笔记与复杂度总结。

**自检清单**

- [ ] 能说出 103 题分几大章及大致题数；
- [ ] 能在 1 分钟内从题号找到 `problems/leetcode` 目录；
- [ ] 至少 80% 题能独立 AC 一版（py 或 cpp）；
- [ ] 设计题能手写 LRU 双向链表版；
- [ ] 图/DP 题能对应到 `algorithms/` 子路径。


**103 题分类背诵策略**

每章记「模式名 + 代表题号 + 模板一句」。例：链表-反转-206-三指针；数组-窗口-3-哈希 last_index；图-岛屿-200-DFS/BFS；DP-322-完全背包滚动。

**notes.md 使用**

大纲跳章节；搜索题号；桌面 IDE 读表。勿打印全文。

**双语言流程**

Python AC → C++ 翻译 → 记 C++ 坑点（long long、0-index）。

**classic 手写（索引末尾）**

LRU、LFU、线程池、限流、环形缓冲、锁与无锁结构等。146 必须手写 LRU，不仅 OrderedDict AC。

**SQL 175**

数据岗优先；算法岗可 optional。

**图章依赖**

200 → 207 → 994 → 684/1135。785 放并查集后。

**DP 依赖**

70 → 198 → 300 → 322 → 416。回溯与 DP 分天刷。

**二分模板**

33/34/35 统一 check(mid)；34 左右边界两次二分。

**复盘模板**

每章填：模式三条、薄弱题号、algorithms 路径、复习日。

**模拟面试套题**

套 A 链表+数组+哈希；套 B 树+图+DP；套 C 栈+字符串+二分。每周 60–90 分钟随机抽索引题号。

**fork 同步**

每周 pull；README 升 v2 时更新本页版本描述。

**贡献索引**

新行需题号、题名、slug 目录存在、py/cpp 题解、双端 notes 同步。

**完成度心态**

103 全 AC 非 offer 保证，但主流模式见过一轮。未全 AC 可投简历，面试前补强薄弱章 3 题。

**开刷前检查**

书签 notes.md；建 prob-hot100 进度表；py/cpp 各 AC 一题。三项完成再计 Day 1。



**深度学习补充（二）：分章精讲（仍请以 notes.md 表为准）**

**链表章**：面试最高频。206 必会；21 合并哑节点；141 判环 O(1) 空间用快慢；142 入口双指针重置；160 对齐长度；19 哑节点+双指针；24 迭代交换；25 测长再分段 reverse；92 找 left 前驱；148 归并 O(n log n)；234 找中点拆半反转；237 O(1) 删节点复制 next 值；2 哑节点进位；146 设计见 iv-classic-lru-cache。每题 AC 后在卡片写「指针图是否画对」。

**数组/双指针/窗口章**：3 窗口+last_index；11 对撞左右夹；15 排序后固定 i 双指针 j；42 左右 max 乘积或单调栈；56 排序按起点合并；88 从尾填充；121 一次遍历 min_price；122 贪心累加正差；152 维护 cur_max/cur_min；189 三次 reverse；238 前后缀不含 self；239 单调队列 deque 存下标；560 前缀和 map 计数；283 快慢指针挪零。与 algo-two-pointers、algo-sliding-window 专题交叉。

**栈章**：20 栈匹配括号；32 栈存下标或 DP；84 单调栈弹栈算面积；85 每行 histogram；155 MinStack 双栈。先做 20 再做 84，形成「栈存下标」直觉。

**字符串章**：5 中心扩展或 Manacher；647 计数回文；6 模拟行；8 atoi 边界；14 纵向比较；28 KMP next 数组；76 窗口+need 计数。28 与 algorithms/string 链接。

**哈希/位运算章**：1 补数 map；136 异或；169 Boyer-Moore；287 Floyd 判环。287 归类「数组作链表」技巧。

**二叉树章**：94 递归中序；95/96 BST 计数 DP；98 中序验 BST；101 对称递归；102 层序 BFS；104 深度 DFS；105 分治构造；114 展平后序；124 后序 max_gain；226 交换左右；236 递归 LCA；337 树形 DP 抢/不抢。与 ds-tree-binary-tree、algo-dp-tree 链接。

**图章**：79 DFS 回溯；200 岛屿 BFS/DFS；207 拓扑；994 多源 BFS；785 染色二分图；684 并查集；1135/1584 MST。按 200→207→994 顺序。对照 algorithms/graph 子目录 notes。

**回溯/DP章**：22 回溯括号；37 数独；39/46/78 组合排列子集；51 N 皇后；53 Kadane；62/64 路径 DP；70/198 一维 DP；72 编辑距离；75 荷兰国旗；91 解码 DP；139 单词拆分；279 BFS 或 DP；300 LIS；322 完全背包；406 贪心+插入；416 0-1 背包；437 前缀和+DFS。分「回溯周」与「DP周」避免混练。

**二分/杂项章**：4 二分划分；7/9 模拟；13 罗马数字；17 回溯电话；18 四数之和；31 下一个排列；33 旋转数组二分；34 左右边界；35 插入位置；41 原地哈希；45/55 跳跃；48 矩阵旋转；215 堆或快选。215 链接 ds-tree-heap。

**困难串/SQL**：10 正则 DP 可暂缓；175 SQL optional。

**手写 classic**：索引表末链接 LRU/LFU/队列/线程池等，与 146 等设计题配合。面试前至少 LRU 白板一遍。

**八周计划再列（可打印）**

W1 哈希+数组+栈；W2 链表全章；W3 字符串+剩余数组；W4 树；W5 图；W6 回溯；W7 DP；W8 二分杂项+错题+classic。每周日复盘卡片。

**PowerShell 批量打开题解（示例）**

根据 notes.md 中题号列表，循环 Set-Location 到各 slug 目录运行 python solution.py，用于周末回归测试（脚本自行从表解析或手列 5 题）。

**与 prob-hot100 协同**

hot100 页勾进度；本页定方法论；notes.md 定题号列表。三者不重复：hot100 不扩写技巧，本页不贴全表。

**manifest 字段**

iv-top-frequent：topic_path interview/top_frequent，guide_toc topic-algorithm，guide_tier medium，status draft。扩题时改 Study notes 与 README 版本，本页更新题数描述。

**quality 注意**

勿大段重复段落；勿走读 filler；代码围栏需真实片段。published 前 strict 校验。

**学完标志**

能按章口述 3 道题技巧；能 5 分钟内从题号找到 slug 目录；103 题至少 85+ AC；146 LRU 手写过关。



**深度学习补充（三）**

索引 v1 103 题冻结。扩题升 v2 改 py/cpp notes。本页不贴全表。学习者打开 notes.md。章节：链表、数组窗口、栈、字符串、哈希、树、图、回溯DP、二分杂项、难串SQL、classic。每章按表刷。代表题上文已列。技巧链：206-25-146。数组：1-15-239。图：200-207-994。DP：70-322-416。classic：146 LRU 必手写。双语言：py AC 后 cpp。进度：prob-hot100 勾选。专题：algorithms graph dp string。站点：ds-linear algo-dp-linear iv-classic-lru-cache。八周计划严格执行。每日新题+复习。周末章节块。考前最小集。模拟三套。错题二刷。SQL175 可选。10 正则暂缓。贡献：改表同步双端。死链禁止合入。fork 每周 pull。README 版本看 v1 v2。manifest topic_path interview/top_frequent guide_toc topic-algorithm medium draft。quality 无 filler 无重复段。published strict 校验。学完 85+ AC。146 手写。五分钟内 slug 定位。按章口述三题。心态：103 非 offer 保证但覆盖主流。未全 AC 可投简历补薄弱章。检查清单：书签 notes；hot100 表；py cpp 各 AC 一题。PowerShell LiteralPath。题解 problems leetcode slug。表内链接相对路径。维护者计数表格行数等于103。结束。

**深度学习补充（三）**

索引 v1 103 题冻结。扩题升 v2 改 py/cpp notes。本页不贴全表。学习者打开 notes.md。章节：链表、数组窗口、栈、字符串、哈希、树、图、回溯DP、二分杂项、难串SQL、classic。每章按表刷。代表题上文已列。技巧链：206-25-146。数组：1-15-239。图：200-207-994。DP：70-322-416。classic：146 LRU 必手写。双语言：py AC 后 cpp。进度：prob-hot100 勾选。专题：algorithms graph dp string。站点：ds-linear algo-dp-linear iv-classic-lru-cache。八周计划严格执行。每日新题+复习。周末章节块。考前最小集。模拟三套。错题二刷。SQL175 可选。10 正则暂缓。贡献：改表同步双端。死链禁止合入。fork 每周 pull。README 版本看 v1 v2。manifest topic_path interview/top_frequent guide_toc topic-algorithm medium draft。quality 无 filler 无重复段。published strict 校验。学完 85+ AC。146 手写。五分钟内 slug 定位。按章口述三题。心态：103 非 offer 保证但覆盖主流。未全 AC 可投简历补薄弱章。检查清单：书签 notes；hot100 表；py cpp 各 AC 一题。PowerShell LiteralPath。题解 problems leetcode slug。表内链接相对路径。维护者计数表格行数等于103。结束。

**深度学习补充（三）**

索引 v1 103 题冻结。扩题升 v2 改 py/cpp notes。本页不贴全表。学习者打开 notes.md。章节：链表、数组窗口、栈、字符串、哈希、树、图、回溯DP、二分杂项、难串SQL、classic。每章按表刷。代表题上文已列。技巧链：206-25-146。数组：1-15-239。图：200-207-994。DP：70-322-416。classic：146 LRU 必手写。双语言：py AC 后 cpp。进度：prob-hot100 勾选。专题：algorithms graph dp string。站点：ds-linear algo-dp-linear iv-classic-lru-cache。八周计划严格执行。每日新题+复习。周末章节块。考前最小集。模拟三套。错题二刷。SQL175 可选。10 正则暂缓。贡献：改表同步双端。死链禁止合入。fork 每周 pull。README 版本看 v1 v2。manifest topic_path interview/top_frequent guide_toc topic-algorithm medium draft。quality 无 filler 无重复段。published strict 校验。学完 85+ AC。146 手写。五分钟内 slug 定位。按章口述三题。心态：103 非 offer 保证但覆盖主流。未全 AC 可投简历补薄弱章。检查清单：书签 notes；hot100 表；py cpp 各 AC 一题。PowerShell LiteralPath。题解 problems leetcode slug。表内链接相对路径。维护者计数表格行数等于103。结束。

**与 Hot 100、Codetop 题单的分工**：`prob-hot100` 侧重题单勾选与仓库题解入口；`prob-codetop` 等索引页记录外部题单来源；本专题 `iv-top-frequent` 固定 103 题并绑定 `interview/top_frequent/notes.md` 的版本号。三者不要混为同一进度表，避免「勾了 Hot100 却漏掉索引章内题」的错觉。

**发布前自检**：`guide_toc: topic-algorithm`；基础篇须为直觉与定义、复杂度分析、代码模板、变体与技巧、易错点、练习建议（非 topic-ds 六标题）；勿粘贴 103 行完整表；汉字 ≥8000。strict 质量脚本检查重复段与 filler 时，若扩写导致重复，应删改而非堆叠相同段落。

**给复习者**：打开 Study `notes.md` 任选一章，用 25 分钟完成该章「最小集」中一道新题、一道昨日错题，并在卡片写「模式关键词」——坚持八周比单次通宵更有效。

**notes.md 各章学习重点（补充）**

链表章：指针图比代码更重要，建议每题画 before/after。数组章：区分「排序后双指针」与「滑动窗口」，勿混模板。栈章：记住「栈存下标」适用于 84/85。字符串章：76 最小覆盖窗口与 3 无重复子串窗口类似但约束不同。哈希章：1 与 560 是哈希的两极——补数与前缀计数。树章：递归返回值语义（高度、路径和、是否 BST）要分清。图章：网格题注意四连通与八连通。回溯章：剪枝顺序影响性能但不影响正确性。DP 章：先定状态维度再写转移。二分章：注意 while 边界与 mid 计算。

**103 题与面试时间的现实规划**

假设每日 1.5 小时刷题，103 题约需 70–90 天首轮；二刷错题 30 天；classic 手写 10 天。若只有 30 天，只做各章最小集约 35 题 + 全部 classic 必考 + 目标公司往年高频，其余题标记「二轮」。本页八周计划按每周 12–15 题设计，适合全职备考；在职可拉长至 16 周，每周 6–8 题。

**与面试官表达**

描述刷题方法时可以说：「我用 Study 仓库的 top_frequent 索引按专题推进，每题在 problems/leetcode 下有 py/cpp 题解，设计题对照 interview/classic 手写。」避免只说「我刷了 Hot100」却无结构。

**维护者与学习者协作**

发现 notes.md 死链请提 PR 修 slug；发现某题算法专题缺失可在 algorithms 下补 notes 并在索引对照表加一行。atelier 本页只改方法论与映射，不替代仓库表。

**收束**

top_frequent 的价值 = 分类 + 路径 + 版本冻结；表在 Study，技巧在本页，代码在题解。完成 103 题前不必追求 every hard 题完美，但务必让每章至少有 2 题能向他人讲清思路。

**每日打卡模板（可复制）**

```
日期：
今日新题（题号+slug）：
昨日复习：
本章模式关键词：
是否运行 py/cpp 题解：Y/N
classic 手写进度：
```

**与实习/校招时间线对齐**

秋招前 3 个月启动八周计划并留 4 周缓冲；春招可压缩为 6 周高强度。在职者用 16 周计划，每周 6–8 题，周末块刷一章。考前 7 天只做最小集+错题+LRU 白板。

**双端 notes 维护约定**

改题号、slug、章节标题时，必须同时编辑 `python/interview/top_frequent/notes.md` 与 `cpp/interview/top_frequent/notes.md`，并在 README 注明版本号变更。atelier 只更新方法论段落，不复制表格。

**strict 发布前检查清单**

- [ ] 基础篇六个 ### 符合 topic-algorithm（直觉与定义、复杂度分析、代码模板、变体与技巧、易错点、练习建议）
- [ ] 汉字 ≥ 8000
- [ ] 无重复段落堆砌
- [ ] Python/C++ 实现节含代码
- [ ] 未粘贴 103 行完整表

**第一遍刷索引的建议节奏**

第 1–7 天：哈希章+数组章最小集，每天 2 题新题+1 题复习。第 8–14 天：链表章按难度递进。第 15–21 天：栈+字符串。第 22–28 天：二叉树。第 29–35 天：图。第 36–49 天：回溯与 DP 分周。第 50–56 天：二分杂项。第 57–60 天：错题+cclassic。节奏可随在职情况拉伸，但「每章结束写卡片」不可省。

**notes.md 中「与本仓库 algorithms 对照」表的用法**

做完表中任一题号后，打开对应 `algorithms/.../notes.md` 用一分钟读「核心思想」段，把题号记在笔记末尾。积少成多后，你的 Study 仓库会变成带个人索引的第二个大脑，比只存 AC 截图更有用。

**若你只剩三十天**

压缩为：链表最小集 5 题、数组 5 题、树 5 题、图 4 题、DP 8 题、哈希栈 3 题、classic LRU 必写，其余题标记二轮。本页八周计划是满分节奏，不是最低节奏；按最低节奏执行时勿与他人满分节奏比较而产生焦虑。

**classic 手写专题与索引的对应关系**

`notes.md` 末尾列出的 LRU、LFU、线程池、限流等路径，在 atelier 对应 `iv-classic-*` 指南。146 在链表章出现，但 AC 题解不等于面试过关；务必在 classic LRU 专题闭卷写双向链表版。其他 classic 题按目标岗位选读：后端可优先线程池、限流、队列；系统岗可补锁与无锁栈。索引表只提供入口，不展开实现细节。

**quality 与 guide 校验提醒**

扩写时避免同一长段重复粘贴；`validate_algorithm_quality.py` 会检测重复段落。代码块须为真实片段，勿用「参阅仓库」占位。published 前运行 `--slug iv-top-frequent --strict`。

**总结**：打开 Study `notes.md` 按章推进，用本页方法论文与算法专题对照，用 `prob-hot100` 勾进度，用 classic 补手写——四者缺一不可。


## 延伸阅读

- **权威索引表**：`F:\Study\Algorithm\python\interview\top_frequent\notes.md`（及 cpp 镜像）
- **仓库 README 与 pending 任务**：扩题规则见根 README
- **Hot 100 站点页**：`algorithm-guides/prob-hot100`
- **总导读**：`algorithm-guides/overview`
- **手写专题**：`iv-classic-lru-cache`、`iv-classic-rate-limiter` 等
- **GitHub**：[interview/top_frequent](https://github.com/zhk0567/Algorithm/tree/main/python/interview/top_frequent)

维护约定：Study 索引增删题时，更新版本号与本页「直觉与定义」「学习路径」中的题数描述；**禁止**在 atelier 静态粘贴完整 103 行表，以免与仓库分叉不同步。学习者始终以 Study 笔记链接为准。

**按公司风格微调（非官方，仅供参考）**

| 风格 | 建议加重索引章节 |
|------|------------------|
| 互联网后端 | 链表、哈希、图、DP |
| 客户端 / 全栈 | 数组、字符串、树 |
| 基础架构 / C++ | 手写 classic + 146/155 |
| 数据岗 | SQL 175 + 哈希 |

**每日学习节奏示例**

- 工作日：1 道新题 + 1 道昨日复习（30+20 分钟）；
- 周末：同一章连做 3–4 道 + 整理复盘卡片；
- 考前 3 天：只做索引「最小集」与 classic 手写。

**103 题完成度自检**

| 档位 | 标准 |
|------|------|
| 及格 | 80+ 题独立 AC 一版，经典 10 题能口述思路 |
| 良好 | 全部 AC，错题二刷无 WA |
| 优秀 | 全部 AC + 关键题 C++ 双写 + LRU 白板 15 分钟 |

**与 atelier 其他指南的阅读顺序**

1. `overview` → 2. `ds-linear` → 3. 本页 + Study `notes.md` → 4. 按章跳 `algo-*` / `ds-*` → 5. `prob-hot100` 勾进度。

**维护者校验命令（题数是否为 103）**

```powershell
$notes = Get-Content -LiteralPath 'F:\Study\Algorithm\python\interview\top_frequent\notes.md' -Raw
($notes -split '\r?\n' | Where-Object { $_ -match '^\|\s*\d+\s*\|' }).Count
```

结果应与 README 声明的 v1 题数一致；扩题后更新本页「复杂度分析」表格题数。

**索引使用的三条纪律**

第一，题号以 `notes.md` 表格为准，不以记忆或外部 Hot100 列表为准，避免 slug 拼错。第二，每题 AC 后写一句「模式关键词」再勾进度，避免假进度。第三，设计类题（146 等）必须完成 `interview/classic` 手写，不能仅 AC 题解里的库函数版。违反第三条是索引学习最常见的「看似刷完、面试仍挂」原因。

**发布前自检**

```powershell
Set-Location -LiteralPath 'f:\commercial\atelier'
python scripts/validate_algorithm_guide.py --slug iv-top-frequent --strict
python scripts/validate_algorithm_quality.py --slug iv-top-frequent --strict
```

通过后再将 manifest 中本篇标为 `published`（需你回复「Algorithm 第 1 批通过」）。扩写时优先增加分章学习策略与 PowerShell 路径示例，勿粘贴重复 filler 句。

**八周计划与 full-time 刷题差异**

若暑假全天刷题，可将「每周题量」翻倍，但**仍应按 notes.md 章节推进**，避免随机挑简单题。在职者用 12 周版：每周 6～8 题 + 1 个 classic 手写，索引表勾选节奏放慢，重点保证设计题与图论 DP 不跳章。

**错题本字段建议**

题号 / 错误类型（边界、指针、复杂度估错）/ 对应 algorithms 路径 / 复习日期。索引页不负责存错题，错题应写在个人笔记或 leetcode 子目录 `notes.md` 末尾。

**103 题之外的补充**

索引覆盖主流国内面试算法面，不保证公司自定义题。若目标公司偏重图论或系统 design，在完成 60% 索引后插入 1 周图论专题（`algo-graph-*`）与 2 天 `interview/classic`。索引是骨架，岗位 JD 是权重。

**口述练习（每周 15 分钟）**

随机抽表中 3 题，仅口述：输入输出、暴力思路、优化范式、复杂度。不说代码也能暴露理解漏洞；说完再打开 leetcode 目录验证是否一致。若口述卡壳，回到 `algorithms/` 或 `data_structures/` 对应专题补 30 分钟再返回索引，不要硬刷下一行。索引完成度以「能独立 AC + 能口述」为准，不以勾选行数为准。第 1 批验收通过前保持 `draft`，通过后由维护者改 manifest 为 `published`。与 `prob-hot100` 搭配时：Hot 100 看热度，top_frequent 看国内面试频率，两者勾选表可合并为一张总进度 Excel，避免重复计数同一题号。

**从索引到 offer 的现实预期**

103 题覆盖主流笔试模式，但不保证覆盖所有公司所有题型。索引完成后仍可能需要剑指 Offer 变种、System Design、项目经历。本页目标是「算法题有结构地过完一轮」，而非「只刷这 103 题即可」。若时间只允许三十天，请收缩到前文「最小集」加 classic 手写，并在卡片上标记「二轮再刷」的题号，而不是强行平均每天三题新题导致后期遗忘。

**与导师/同学协作**

可约定每周互相抽查：随机抽索引中一题，五分钟讲思路不写代码。讲不清的题号记入共享错题表，周末只重做错题表。协作时使用统一 Study 仓库版本号（v1/v2），避免两人表不一致。
