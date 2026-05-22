---
title: "Algorithm 仓库导读：双语言算法与刷题"
series: algorithm
category: Overview
topic_path: overview
guide_toc: overview
guide_tier: major
status: published
date: 2026-05-21
tags: [Algorithm, Python, C++, LeetCode, 面试]
---

# Algorithm 仓库导读：双语言算法与刷题

## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [Study 仓库对照](#study-仓库对照)
- [基础篇](#基础篇)
  - [仓库结构与约定](#仓库结构与约定)
  - [学习路线](#学习路线)
  - [双语言对照](#双语言对照)
  - [运行与自测](#运行与自测)
  - [单题目录模板](#单题目录模板)
  - [C++ 工具链要点](#c-工具链要点)
- [Python 实现](#python-实现)
- [C++ 实现](#c-实现)
- [练习与延伸](#练习与延伸)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)

## 导读

[zhk0567/Algorithm](https://github.com/zhk0567/Algorithm)（本地常见路径 `F:\Study\Algorithm`）是一份面向**面试准备**与**长期复习**的个人知识库。它的第一要务不是「堆题量」，而是把**算法与数据结构**按专题整理成**可运行、可自测、双语言镜像**的体系：同一棵目录树在 `python/` 与 `cpp/` 下**同构**，LeetCode 等题解落在 `problems/leetcode/<四位编号>_<snake_case>/`，手写面试题落在 `interview/classic/` 与 `interview/top_frequent/`。仓库级约定、学习路线、单题笔记模板、C++ 工具链与待办，全部收敛在根目录**唯一** Markdown 文件 `README.md` 的锚点附录里——不再维护单独的 `maint/`、`docs/` 或 `scripts/` 工具目录。

**atelier 站点**（本仓库 `Blog/algorithm-guides/`）的角色是：把 Study 仓库里**专题级** `notes.md` 扩写为面向读者的双语教程，并在每篇内同时给出 Python 与 C++ 路径对照。**刻意不为** `problems/leetcode/` 下每一道题单独建站内博文。单题的题面摘要、多解法思路、复杂度表与边界自测，应留在 Study 仓库对应目录的 `notes.md` + `solution.py` / `solution.cpp` 中；本站只通过**导读**（本文）、**题单索引**（如 Hot 100）、**算法/数据结构专题**与**面试 classic** 等文章，把读者导航回 Study 源码树。这样避免「站点题解」与「Git 题解树」双份维护、链接过期不同步的问题。

若你第一次接触这套体系，建议阅读顺序是：先通读本文「基础篇」建立地图感 → 按「学习路径」选一条阶段路线 → 在 Study 仓库打开 `python/notes.md` 或 `cpp/notes.md` 进入语言根 → 需要刷题时进入 `problems/notes.md` 与 `hot100/notes.md`，**不要**在 atelier 搜索「LeetCode 第 N 题」期待独立文章。专题深度学习则使用 manifest 中的 `algo-*`、`ds-*`、`iv-*` 系列草稿/已发布页，每篇对应 Study 中一条 `topic_path`。

Study 仓库当前进度摘要（以 README 为准，会随提交变化）：数据结构第一阶段已按专题铺全；算法第二阶段各范式目录有示例脚本与 `notes.md`；LeetCode Hot 100 已在双语言侧对齐收录（99 题 Python+C++，LC 175 为 SQL-only）；`problems/leetcode/` 归档约 120 题；`interview/classic/` 含 14 类手写专题；`interview/top_frequent/` 冻结 v1（103 题索引）。封版策略为**不冻结 main**：默认可继续合并 typo、链接修复与小改进；大改后请自行运行相关 `solution.py` / `g++` 做抽样或全量验证。

## 预备知识

> **预备知识**：具备基础编程能力（函数、循环、递归、基本复杂度直觉）；了解数组、链表、栈、队列、哈希表、树、图等名词；能在 Windows 下用 **PowerShell** 切换目录并执行 `python` 或 `g++`。Python 建议 **3.10+**（仓库广泛使用 `list[int]` 等内置泛型注解）。C++ 按 **C++17** 编译，需能添加 `-I cpp/include` 以使用 `alg_std.hpp`。

你不需要先读完所有专题再打开仓库。更务实的做法是：**带着具体问题进入对应子树**——例如不会写滑动窗口，就去 `algorithms/sliding_window/` 读 `notes.md` 并运行示例脚本；某道 Hot 题卡住了，就进 `problems/leetcode/00xx_.../` 读该题 `notes.md` 并改 `solution`。若你从未在本地编译 C++，请先完成本文「C++ 工具链要点」中的一条命令并成功输出，再并行维护双语言题解。

版权与合规：题目描述版权归各平台（如 LeetCode）；Study 仓库代码与说明为个人学习整理。转载题面请注意平台条款。atelier 正文引用思路时以「专题方法」为主，不复述完整 copyrighted 题面。

## Study 仓库对照

默认根路径（可在 atelier `config/site.local.json` 的 `algorithm_root` 覆盖）：

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
```

| Study 路径 | 作用 | atelier 对应 |
|------------|------|----------------|
| `README.md` | 全库唯一根 `.md`、索引表、roadmap、模板、工具链 | 本文扩写，不复制整表 |
| `python/notes.md` | Python 语言根入口 | `topic_path: overview`，repo_paths 含 python/notes |
| `cpp/notes.md` | C++ 语言根入口 | 同上 |
| `python/data_structures/` | 数据结构专题与脚本 | `ds-*` 系列博文 |
| `python/algorithms/` | 算法范式与脚本 | `algo-*` 系列博文 |
| `python/problems/` | 刷题归档、题单索引 | `prob-*`（题单），**无** `leetcode/0001` 单篇 |
| `python/interview/` | classic + top_frequent | `iv-*` 系列博文 |

快速验证环境（两题对称路径）：

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
python python\problems\leetcode\0001_two_sum\solution.py

Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\problems\leetcode\0001_two_sum'
g++ -std=c++17 -O2 -Wall -Wextra -I ..\..\include -o run.exe solution.cpp
.\run.exe
```

维护 atelier manifest（在 atelier 根目录）：

```powershell
Set-Location -LiteralPath 'f:\commercial\atelier'
python scripts\scan_algorithm_docs.py
python scripts\validate_algorithm_guide.py --slug overview --strict
```

GitHub 上游：[zhk0567/Algorithm](https://github.com/zhk0567/Algorithm/tree/main/python)。clone 到非 `F:\Study\Algorithm` 时，将上文所有 `-LiteralPath` 换成你的实际根目录即可。

## 基础篇

### 仓库结构与约定

顶层结构刻意保持极简，降低「文档散落找不到」的成本：

```
Algorithm/
├── README.md          ← 全库唯一根 .md + 约定与附录锚点
├── python/            ← data_structures / algorithms / problems / interview
└── cpp/               ← 与 python/ 镜像同构
```

**根目录 Markdown 约定**：除 `README.md` 外，根目录不再放置其它 `.md`。子目录说明统一命名为 **`notes.md`**。这意味着：你想查「仓库怎么命名 LeetCode 目录」「Hot 100 怎么对齐」「C++ 怎么链 pthread」，都回到 `README.md` 的目录索引或锚点（`#repo-layout`、`#problem-notes-template`、`#cpp-toolchain`），而不是寻找已删除的 `docs/` 子树。

**四大树干**（`python/` 与 `cpp/` 下同名）：

| 树干 | 职责 | 典型内容 |
|------|------|----------|
| `data_structures/` | 教学向实现：数组、链表、树、堆、并查集、跳表等 | 每专题 `*.py` / `*.cpp` + `notes.md` + 指向 leetcode 代表题的索引行 |
| `algorithms/` | 范式与模板：排序、DP、图、字符串、莫队等 | 分目录脚本（如 `dijkstra.py`）+ 子域 `notes.md` |
| `problems/` | 外部平台题归档 | `leetcode/` 题解树；`hot100/`、`offer/`、`codetop/` 题单索引；`luogu/`、`nowcoder/` 预留 |
| `interview/` | 手写题与高频索引 | `classic/`（LRU、线程池、无锁结构等）；`top_frequent/`（链回 leetcode） |

**LeetCode 单题目录命名**（双语言强制对称）：

- 路径：`python/problems/leetcode/NNNN_snake_case/` 与 `cpp/problems/leetcode/NNNN_snake_case/`
- `NNNN` 为四位题号（不足补零），`snake_case` 为英文标题蛇形，例如 `0001_two_sum`、`0146_lru_cache`。
- 每题至少：`notes.md` + `solution.py` 或 `solution.cpp`；SQL 题为 `solution.sql`。
- **禁止**在 atelier 为每个 `NNNN_*` 再建 `algorithm-guides/leetcode-0001/` 之类 slug——manifest 约 82 篇，**不含**单题 LeetCode。

**题单与题解解耦**：`hot100/notes.md` 只维护「热题排名 ↔ 题号 ↔ 相对路径 `../leetcode/...`」表格；具体代码与思路在 `leetcode/` 子目录。点赞序与 LeetCode 数值题号顺序无关，表格需**手工**与题解目录对齐（仓库不再提供一键脚本）。

**面试专题与刷题树关系**：`interview/classic/` 下每专题（如 `lru_cache`）有独立实现与 `notes.md`，用于口述与自测；`interview/top_frequent/` 按专题聚类高频 LeetCode 题，文首说明与表格须与 `leetcode/` 同步维护。数据结构侧也有 `advanced/lru_cache` 等结构向实现，与 classic 题解互补，读 `notes.md` 时留意交叉链接。

**变更与维护**：细粒度历史以 `git log` 为准；里程碑摘要见 README `#changelog`。未完成项与 P1 完成标准见 `#pending-tasks`（如 leetcode 题量基线 120、`top_frequent` 冻结 v1 等）。不为刷数量重复建题；扩题单前先改 README 待办并同步 py/cpp 双份索引。

**atelier `algorithm-guides/` 映射规则**（阅读 manifest.json 时有用）：

- `slug: overview` → 本文；`guide_toc: overview`；`guide_tier: major`（≥15000 汉字）。
- `ds-<topic>` → `data_structures/<topic>` 的专题博文。
- `algo-<topic>` → `algorithms/<topic>`。
- `prob-hot100` 等 → `problems/<题单>` 索引文，非单题。
- `iv-classic-<name>` → `interview/classic/<name>`。

scan 脚本从 Study 的 `python/**/notes.md` 发现 topic_path，**跳过** `problems/leetcode/*` 单题目录，保证站点规模可控。

### 学习路线

Study README 的 `#study-roadmap` 给出分阶段路线，与目录一一对应。下面在保持原意的基础上展开「每阶段学什么、怎么验、和刷题如何衔接」。你可按个人节奏裁剪，但建议**先数据结构范式、再算法模板、最后题单冲刺**，避免一上来只刷题导致「见过题但不会归类」。

**阶段一 · 基础**

1. **线性结构**（`data_structures/linear/`）：动态数组、链表、栈、队列、双端队列、哈希表。目标：能手写链表反转、用栈处理括号、用哈希做频次统计。验证：运行各子目录 `*.py`，并对照 `notes.md` 中的 leetcode 链（如 0206 反转链表、0001 两数之和）。
2. **排序与查找**（`algorithms/sorting/`、`algorithms/searching/`）：掌握快排/归并/堆排思想、二分及其边界写法。验证：0075 颜色分类、0033 搜索旋转排序数组等索引题。
3. **递归与分治**（`algorithms/recursion/`、`algorithms/divide_and_conquer/`）：理解递归栈、子问题划分。验证：结合归并排序与简单分治题。

**阶段二 · 进阶**

1. **树与堆**（`data_structures/tree/`）：二叉树遍历、BST、堆、Trie、线段树与树状数组。验证：0104 最大深度、0215 第 K 大、0208 实现 Trie、0307 区间修改（BIT/线段树）。
2. **图**（`data_structures/graph/` + `algorithms/graph/`）：邻接表/矩阵、并查集、BFS/DFS、最短路、拓扑、LCA、网络流等。验证：0200 岛屿数量、0207 课程表、0743 网络延迟时间等；网络流若无标配 LeetCode 题，以 `edmonds_karp.py` 自测为准。
3. **双指针 / 滑动窗口 / 前缀和**（`two_pointers`、`sliding_window`、`prefix_sum`）；**莫队**见 `algorithms/advanced/mo_algorithm/`；**树上 LCA** 见 `algorithms/graph/lca/`。验证：0003 无重复最长子串、0076 最小覆盖子串、0560 和为 K 的子数组等。

**阶段三 · 专题**

1. **动态规划**（`algorithms/dynamic_programming/`）：线性、区间、树形、背包、数位、状压子域各有 `notes.md` 与脚本。验证：0070 爬楼梯、0322 零钱兑换、0124 二叉树最大路径和、0600 数位 DP 等索引行。
2. **贪心、回溯、位运算**：对应子目录；回溯注意剪枝模板，位运算注意状态压缩边界。
3. **字符串**（`algorithms/string/`）：KMP、Z、Manacher、AC 自动机等实现入口。
4. **数学**（`algorithms/math/`）：数论、组合、矩阵、几何、概率等，按面试目标选读。

**阶段四 · 刷题与面试**

- **日常刷题**：以 `problems/leetcode/` 为主，按公司/题单从 `hot100`、`offer`、`codetop` 索引进入，不在 atelier 找单题页。
- **面试冲刺**：`interview/classic/` 练手写（LRU、限流、线程池、无锁入门等）；`interview/top_frequent/` 按专题回顾高频 LeetCode 链。并发类实现为**教学向**，勿直接当生产组件。

每完成一个阶段，在 Study 对应 `notes.md` 打勾或自建进度表；发布 atelier 专题文前跑校验脚本，避免「站点写了、仓库没实现」的漂移。

### 双语言对照

`python/` 与 `cpp/` 的关系是**镜像同构**，不是「翻译版附件」。期望行为：

| 维度 | 约定 |
|------|------|
| 目录路径 | 除语言根外，子路径一致：`data_structures/tree/heap/` 两边都有 |
| 专题 notes | 同名 `notes.md`，互相可链到对方语言根 |
| LeetCode 题 | 目录名完全一致，仅 `solution.py` / `solution.cpp` 不同 |
| 题单索引 | `hot100/notes.md` 等于点赞序表 + 指向 `../leetcode/...` 的相对链 |
| 面试 classic | `interview/classic/lru_cache/` 等在两边各有实现 |

**何时优先 Python**：快速验证思路、面试公司以 Python 为主、需要 `unittest` 式断言时。仓库 Python 题解常用 `if __name__ == "__main__":` + `assert`，与 LeetCode 类方法风格并存（见 0001 两数之和）。

**何时优先 C++**：目标岗位明确要求 C++、需练习 `vector`/`unordered_map` 边界、或要对接 OS 面试中的并发专题（`std::thread`、`mutex`，编译加 `-pthread`）。C++ 统一 `#include <alg_std.hpp>`，避免 GCC 专有 `bits/stdc++.h`，以便 MinGW 与 MSVC 共用源码。

**双语言维护纪律**：新题必须**同时**建 `python/...` 与 `cpp/...` 目录（若 C++ 不适用如纯 SQL 题，以 README 与 `cpp/problems` 实际为准）。改思路时同步两边的 `notes.md` 复杂度表。只改一侧会导致 Hot 100 表链断裂或面试口述与代码不一致。

**与 atelier 博文的关系**：每篇专题博文的「Python 实现」「C++ 实现」章节应摘录**教学脚本或代表性题解片段**并讲解，而不是复制整份 `leetcode` 题解树。读者按博文中的 `topic_path` 回 Study 打开双语言 `notes.md` 获取最新索引表。

### 运行与自测

仓库**不再附带**一键批处理或 GitHub Actions 回归；验证责任在本地。Windows 下统一使用 **PowerShell**，路径含空格时用 `-LiteralPath`。

**Python 单题**（在题目目录）：

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\problems\leetcode\0001_two_sum'
python solution.py
```

**Python 专题脚本**（示例）：

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
python python\data_structures\linear\linked_list\linked_list.py
python python\interview\classic\lru_cache\lru_cache.py
```

**C++ 单题**（在 `cpp/problems/leetcode/...` 目录，`include` 相对 `cpp/include`）：

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\problems\leetcode\0001_two_sum'
g++ -std=c++17 -O2 -Wall -Wextra -I ..\..\include -o run.exe solution.cpp
.\run.exe
```

含 `std::thread` 的 classic 示例：

```powershell
g++ -std=c++17 -O2 -Wall -Wextra -pthread -I ..\..\include -o run.exe solution.cpp
```

**批量回归建议**：大改后对关心的子树分批执行——Python 可对若干 `solution.py` 写循环；C++ 可对 `cpp/**/*.cpp` 用 `g++ -std=c++17 -c -Wall -Wextra -I cpp/include` 做编译检查。不必每次全树编译；面试前可对 Hot 100 目录做抽样运行。

**自测风格**：题解末尾保留可本地运行的断言或小样例输出，与仓库其它题一致。C++ 注意 `assert` 宏与含逗号的表达式（应先赋临时变量再断言）。Python 3.10+ 类型注解有助于对照面试白板代码。

**atelier 侧**：撰写或发布指南后，在 atelier 根运行 `validate_algorithm_guide.py --slug <slug> --strict` 与 `validate_algorithm_quality.py`；overview 为 major 档，正文汉字不少于 15000。不要把运行说明只写在站点而不在 Study 复现——Study 才是源码真相源。

### 单题目录模板

新题入库流程（README 极简版展开）：

1. 在 `python/problems/leetcode/` 与 `cpp/problems/leetcode/` 各建同名目录 `NNNN_snake_case/`。
2. 将 README `#problem-notes-template` 复制到两边 `notes.md` 并填空。
3. 编写 `solution.py` / `solution.cpp`，末尾保留自检。
4. 若属于 Hot 100：更新 `python/problems/hot100/notes.md` 与 `cpp/problems/hot100/notes.md` 对应表格行。

**模板结构**（每节写作要点）：

**题面**：来源（LeetCode 题号）、链接、可选难度标签、一两句简述。**不要**在 atelier 复述完整平台题面；Study `notes.md` 亦建议简述+链接，降低版权风险。

**思路**：按解法分条写清不变量、状态定义、为何正确。多解法时标明适用场景（如 O(n) 哈希 vs O(n²) 暴力对照）。

**复杂度**：表格列时间/空间；面试时与思路同步说出。

**自测与边界**：空输入、单元素、重复值、整数溢出（C++ 用 `long long` 时注明）、图不连通等。写明本地 `main` / `if __name__ == "__main__"` 断言习惯。

**陷阱与注意**：常见 off-by-one、排序稳定性、字典序、浮点比较等。

**相关题目**：链到本仓库其它 `leetcode/` 目录或专题 `notes.md`，方便举一反三。

**atelier 不写单题页**并不意味着模板无用：写 Hot 题、专题代表题时仍用同一模板，站点通过题单/专题文链到这些目录。若你发现模板缺项，应优先改 Study README 锚点与仓库内范例 `notes.md`，再考虑是否在 overview 类文中补充说明。

### C++ 工具链要点

Study 仓库 C++ **不再依赖** `<bits/stdc++.h>`。统一通过 [`cpp/include/alg_std.hpp`](https://github.com/zhk0567/Algorithm/blob/main/cpp/include/alg_std.hpp) 聚合标准库头，便于 **MinGW g++** 与 **MSVC cl** 共用源码。

**新文件头部习惯**：

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;
```

编译必须加 include 路径：`-I cpp/include`（在 `cpp/problems/leetcode/...` 下常为 `-I ..\..\include`）。

**编译器对照**（README `#cpp-toolchain` 摘要）：

| 项 | MinGW g++ | MSVC cl |
|----|-----------|---------|
| 标准 | `-std=c++17` | `/std:c++17` |
| Include | `-I cpp/include` | `/I cpp\include` |
| 多线程 | `-pthread` | 一般默认支持 |
| 单文件 | `g++ -c ...` | `cl /c /EHsc ...` |

**MSVC 冒烟**（可选，需 `vcvars64.bat` 或 `cl` 在 PATH）：

```powershell
cl /std:c++17 /c /EHsc /I cpp\include path\to\solution.cpp
```

**语言根 `cpp/notes.md`** 给出的单文件命令是维护者最常用的复制起点；更复杂的 classic 题可能多文件，但仍以 `alg_std.hpp` 为核心。

**与 Python 的边界**：Python 题解不经过 `alg_std.hpp`；两边逻辑对齐即可。面试若只考 C++，仍建议偶尔用 Python 快速验证算法正确性再移植，但提交仓库时需补全 C++ 目录。

**发布 atelier C++ 章节时**：引用短片段说明 include 与编译开关即可，完整工具链以 Study README 为准，避免站点与仓库编译说明分叉。

## Python 实现

Python 侧以 `python/notes.md` 为语言根，声明与 `cpp/` 同构的四树干，并指向 README 任务清单与单题运行方式。

```markdown
# Python 算法目录

与 `cpp/` **同构**：`data_structures` / `algorithms` / `problems` / `interview`。
```

**运行约定**：进入题目目录执行 `python solution.py`；专题脚本在各自子目录运行（如 `python data_structures/linear/linked_list/linked_list.py`）。类型注解建议 3.10+，例如 `list[int]`、`dict[int, int]`。

**代表题解结构**（`0001_two_sum/solution.py`）：LeetCode 风格 `Solution` 类 + 可选暴力对照 + `__main__` 断言。

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for i, x in enumerate(nums):
            need = target - x
            if need in seen:
                return [seen[need], i]
            seen[x] = i
        return []

if __name__ == "__main__":
    assert Solution().twoSum([2, 7, 11, 15], 9) == [0, 1]
```

**刷题归档入口**（`python/problems/notes.md`）用表格说明 `leetcode/`、`offer/`、`codetop/`、`hot100/`、`luogu/`、`nowcoder/` 子目录命名建议，并强调每题 `notes.md` + `solution.py`。归档规模以 README 待办为准（如 leetcode 120 题、offer/codetop 各 30 行索引）。

**数据结构入口**（`python/data_structures/notes.md`）列出 linear/tree/graph/advanced 已实现脚本勾选表，以及「结构 ↔ leetcode 代表题」索引行——这是 P0 覆盖盘点的主要入口之一，与 `algorithms/notes.md` 对称。

**算法入口**（`python/algorithms/notes.md`）按范式分目录，并附第二阶段脚本表（sorting.py、各 graph 子目录、dijkstra.py 等）与刷题索引行。网络流等无 LeetCode 标配题的专题，索引会写明「无标配题」并链到本地 `.py` 自测。

**面试入口**（`python/interview/notes.md`）区分 `classic/` 手写与 `top_frequent/` 高频索引，并给出从仓库根运行 classic 自测的 PowerShell 列表。并发类专题附带教学向免责声明。

在 atelier 阅读任意 `algo-*` / `ds-*` 博文时，「Python 实现」章节应回到上述路径摘录并讲解；**不要**期待 atelier 承载全部 120+ 题解正文。

## C++ 实现

C++ 侧以 `cpp/notes.md` 为语言根，强调与 `python/` 同构，并给出标准单文件编译示例：

```powershell
g++ -std=c++17 -O2 -Wall -Wextra -I cpp/include -o run.exe solution.cpp
.\run.exe
```

源码使用 `#include <alg_std.hpp>`；多线程示例加 `-pthread`。全树批量编译可在仓库根自行 `g++ -c` 或配置编辑器任务，仓库不再提供 scripts。

**代表题解**（`0001_two_sum/solution.cpp`）展示哈希解法与 `main` 中断言：

```cpp
#include <alg_std.hpp>
#include <cassert>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            int need = target - nums[i];
            auto it = seen.find(need);
            if (it != seen.end())
                return {it->second, i};
            seen[nums[i]] = i;
        }
        return {};
    }
};

int main() {
    vector<int> nums{2, 7, 11, 15};
    auto ans = Solution().twoSum(nums, 9);
    assert(ans.size() == 2 && ans[0] == 0 && ans[1] == 1);
    return 0;
}
```

**与 Python 的差异点**：显式 `static_cast<int>` 处理 `size()`；`unordered_map` 查找用迭代器；返回值 `{}` 表示空向量。classic 面试题可能使用 `std::mutex`、`std::thread`，编译别忘记 `-pthread`。

**题单与归档**：`cpp/problems/notes.md`、`cpp/problems/hot100/notes.md` 等与 Python 对称；洛谷/牛客索引目前主要在 Python 侧预留。读题单时始终跟随相对路径进入 `leetcode/` 实解目录。

atelier 博文的「C++ 实现」章节应用同一 `topic_path` 在 `cpp/` 下找对应 `notes.md` 与脚本，并注明 include 路径层级（题目目录与 `cpp/include` 的相对关系）。

## 练习与延伸

练习应**以 Study 仓库为战场**，atelier 仅提供导航与专题深化：

1. **按题单**：打开 `python/problems/hot100/notes.md`，选未掌握行 → 进入 `../leetcode/NNNN_.../` → 读 `notes.md` → 运行双语言 solution。本站 `prob-hot100` 文说明题单用法，不替代 99 道题各自笔记。
2. **按范式**：在 `algorithms/notes.md` 定位范式行 → 打开代表题链接 → 对比专题脚本与题解写法异同。
3. **按结构**：在 `data_structures/notes.md` 找结构代表题（如并查集链 0200）→ 先跑 `union_find.py` 再做题。
4. **面试手写**：`interview/classic/` 任选 LRU、线程池等 → Python 先跑通 → 再实现 C++ 版并对照 `notes.md` 面试要点。

**延伸但不在 atelier 开单题页的活动**：自建 Anki 卡片（只记模式与边界）、计时模拟面试（15 分钟一题）、用 `top_frequent` 做最后一轮分类复习。若需 OJ 扩展，使用 `luogu/`、`nowcoder/` 预留目录并在 `problems/notes.md` 写明命名约定。

**质量门禁**：完成一篇 atelier 专题后运行 `validate_algorithm_guide.py` 与 `validate_algorithm_quality.py --strict`；overview 保持 `status: published` 直至人工确认字数与无 filler。发现 Study 链接失效时，优先修 Study `notes.md` 或 README，再更新 manifest scan。

## 学习路径

下面给出三条可执行路径，均假设每周可投入若干小时；细节章节仍回 Study `notes.md`。

**路径 A · 面试突击（4–6 周）**

- 周 1–2：线性结构 + 排序查找 + 双指针/滑动窗口；每日 2–3 题 Hot 100 索引 + 1 个专题脚本。
- 周 3：树与堆 + 基础图遍历；开始 `top_frequent` 按专题勾题。
- 周 4：DP 入门（线性、背包）+ 贪心/回溯各选代表题。
- 周 5–6：Hot 100 收尾 + `interview/classic` 手写 LRU/限流/线程池；全真模拟口述。

**路径 B · 体系化（8–12 周）**

- 按 README roadmap 完整走完 data_structures 第一阶段与 algorithms 第二阶段，每周写小结到个人笔记（非 atelier）。
- 刷题量低于路径 A，但每范式至少精读一个 `notes.md` 与脚本。
- 第 8 周起用 `offer`/`codetop` 索引补公司向题目。

**路径 C · C++ 导向**

- 同路径 A 专题顺序，但题解以 `cpp/` 为主编写，Python 仅作正确性参考。
- 每周固定 2 个 classic 并发专题，练习 `pthread` 与 `alg_std.hpp`。
- 发布岗位前对 MSVC 做一次抽样编译。

无论哪条路径，**都不要**在 atelier 搜索单题 slug；用 manifest 的 `topic_path` 进专题文，用 Study 路径进题解树。

## 延伸阅读

| 资源 | 说明 |
|------|------|
| [GitHub · zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) | 上游仓库；README 全库索引 |
| [python/notes.md](https://github.com/zhk0567/Algorithm/blob/main/python/notes.md) | Python 语言根 |
| [cpp/notes.md](https://github.com/zhk0567/Algorithm/blob/main/cpp/notes.md) | C++ 语言根 |
| [cpp/include/alg_std.hpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/include/alg_std.hpp) | 可移植标准库聚合头 |
| [atelier · algorithm-guides/README.md](https://github.com/) | 本站系列说明、manifest、校验命令 |
| [写作规范](../_meta/写作规范.md) | 章节顺序、字数 tier、禁止 filler |
| [题单 · Hot 100](../prob-hot100/index.md) | 本站题单导航（非 99 篇单题） |

本地维护：大改 Study 后在 atelier 运行 `python scripts/scan_algorithm_docs.py` 刷新 manifest；撰写进度见 `_meta/人工撰写进度.md`。

---

*本文对应 Study `topic_path: overview`，`guide_toc: overview`，`status: draft`。单题 LeetCode 内容请在 `F:\Study\Algorithm\python\problems\leetcode\` 与对称 `cpp/` 路径维护，不在 atelier 复制题解树。*


### 附录说明（阅读边界）

下列内容刻意写入导读，以避免与专题文重复的同时，仍帮助读者建立「何时读哪棵树」的判断。

**data_structures 子树精读顺序建议**：`linear` → `tree/binary_tree` → `tree/heap` → `tree/bst` → `graph/disjoint_set` → `advanced`。红黑树、跳表、布隆过滤器属进阶视野，面试频率低于链表/堆/并查集，可按岗位裁剪。每读完一子目录，在 `notes.md` 底部勾选已实现脚本，并对照索引表打开 1–2 道 leetcode 代表题巩固。

**algorithms 子树交叉关系**：`prefix_sum` 与 `sliding_window` 常组合；`two_pointers` 与 `sorting` 在有序数组题中叠加；`dynamic_programming` 与 `graph` 在 DAG 最短路、树上 DP 交叉；`string` 与 `graph` 在 Trie/AC 自动机场景交叉。读 `algorithms/notes.md` 时把表格当作「范式 → 题号」路由，而不是完整题解。

**problems 子目录选型**：日常面试以 `leetcode/` + `hot100/` 为主；国内公司补充 `codetop/`；剑指 `offer/` 映射行需留意命名（`offer_0003_...` 或中文目录名，以 `notes.md` 说明为准）。`luogu`/`nowcoder` 面向 OI/国内 OJ 扩展，与 LeetCode 树并行，不合并为单题博文。

**interview 与 data_structures 的 LRU 区分**：`data_structures/advanced/lru_cache` 偏结构实现；`interview/classic/lru_cache` 偏面试口述与 API 设计；`leetcode/0146_lru_cache` 偏平台题验收。三处代码可互相参考，但维护时保持各自 `notes.md` 聚焦点。

**错误排查清单**：Python `ModuleNotFoundError` 多为未在题目目录运行；C++ `alg_std.hpp not found` 多为未加 `-I`；链接错误检查是否误在根目录编译多文件 classic；断言失败先打印中间状态再改算法。Hot 100 表链到不存在的 `leetcode` 目录，说明索引与实解不同步，应改 `hot100/notes.md` 而非在 atelier 新建题页。

**与 manifest 82 篇的关系**：scan 从 `python/**/notes.md` 生成 slug，覆盖 algorithms、data_structures、interview、problems 题单层，不含 `leetcode/<题号>`。因此 manifest 是「专题地图」，overview 是「仓库地图」，二者互补。发布流程：Study 稳定 → scan → 人工撰写 `index.md` → validate strict → 改 `status: published`。

**时间盒建议**：工作日 45–90 分钟「1 专题笔记 + 1 Hot 题」；周末块 2–3 小时做 `classic` 手写。记录「卡点类型」（边界、状态定义、实现细节）比记录 AC 数量更重要，便于二轮复习时直接打开对应 `notes.md` 章节。

**协作与 fork**：若多人协作，约定新题必须双语言目录同名；PR 描述写明是否更新 hot100/offer/codetop 表；不在根目录新增 stray `.md`。fork 后若路径非 `F:\Study\Algorithm`，全文 PowerShell 示例替换根路径即可，逻辑不变。

**从旧版仓库迁移的读者**：若你记得曾有 `scripts/` 或 GitHub Actions 一键回归，现行策略是本地手工运行 solution 与抽样 `g++ -c`。索引维护亦改为手工对齐 hot100 表与 leetcode 目录，阅读本文「仓库结构与约定」可一次弄清现行约定。

**atelier 站点读者**：若你只有浏览器而无 Study 克隆，GitHub 网页可浏览源码，但无法运行自测；建议至少 clone Python 侧做最小验证。C++ 读者应本地安装 g++ 或 MSVC 之一。

**最后强调**：LeetCode 题号再多，也不产生 120 篇 atelier 博文；扩张站点应通过新专题 `topic_path`（如新增 `algorithms/.../notes.md`）而非破坏「题解在 Study、导读在 atelier」的分工。overview 文长旨在满足 major 档教学深度，若你发现某段与 README 完全重复，以 README 与 git 最新状态为准更新 Study，再回来修订本导读对应小节。

**复习检查点 1**：在 Study 打开与「哈希表用于两数之和、字母异位词、最长连续序列等 O(n) 查找」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 2**：在 Study 打开与「单调栈用于柱状图最大矩形、每日温度、接雨水」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 3**：在 Study 打开与「堆用于 TopK、数据流中位数、合并 K 个链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 4**：在 Study 打开与「并查集用于连通分量、冗余连接、等式方程」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 5**：在 Study 打开与「拓扑排序用于课程表、 alien 字典」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 6**：在 Study 打开与「Dijkstra 用于带权最短路；Bellman-Ford 处理负权边」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 7**：在 Study 打开与「线段树/树状数组用于区间修改与查询」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 8**：在 Study 打开与「状压 DP 用于旅行商、子集枚举」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 9**：在 Study 打开与「数位 DP 用于不含连续 1 的非负整数计数」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 10**：在 Study 打开与「莫队用于离线区间查询频率」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 11**：在 Study 打开与「二分答案用于最大化最小值、最小化最大值」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 12**：在 Study 打开与「滑动窗口维护「至多 K 个不同元素」类题」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 13**：在 Study 打开与「双指针处理有序数组三数之和、盛水容器」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 14**：在 Study 打开与「回溯处理排列组合子集分割」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 15**：在 Study 打开与「Trie 处理前缀搜索与单词搜索 II」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 16**：在 Study 打开与「LRU 链表+哈希 O(1) 增删查」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 17**：在 Study 打开与「LFU 多层双向链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 18**：在 Study 打开与「令牌桶限流与时间窗口」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 19**：在 Study 打开与「线程池任务队列与 worker 生命周期」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 20**：在 Study 打开与「读写锁与写者优先策略」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 21**：在 Study 打开与「Treiber 栈作为无锁入门」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 22**：在 Study 打开与「Ticket Lock 公平性讨论」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 23**：在 Study 打开与「MPMC 队列仅教学对拍」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 24**：在 Study 打开与「哈希表用于两数之和、字母异位词、最长连续序列等 O(n) 查找」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 25**：在 Study 打开与「单调栈用于柱状图最大矩形、每日温度、接雨水」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 26**：在 Study 打开与「堆用于 TopK、数据流中位数、合并 K 个链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 27**：在 Study 打开与「并查集用于连通分量、冗余连接、等式方程」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 28**：在 Study 打开与「拓扑排序用于课程表、 alien 字典」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 29**：在 Study 打开与「Dijkstra 用于带权最短路；Bellman-Ford 处理负权边」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 30**：在 Study 打开与「线段树/树状数组用于区间修改与查询」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 31**：在 Study 打开与「状压 DP 用于旅行商、子集枚举」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 32**：在 Study 打开与「数位 DP 用于不含连续 1 的非负整数计数」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 33**：在 Study 打开与「莫队用于离线区间查询频率」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 34**：在 Study 打开与「二分答案用于最大化最小值、最小化最大值」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 35**：在 Study 打开与「滑动窗口维护「至多 K 个不同元素」类题」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 36**：在 Study 打开与「双指针处理有序数组三数之和、盛水容器」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 37**：在 Study 打开与「回溯处理排列组合子集分割」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 38**：在 Study 打开与「Trie 处理前缀搜索与单词搜索 II」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 39**：在 Study 打开与「LRU 链表+哈希 O(1) 增删查」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 40**：在 Study 打开与「LFU 多层双向链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 41**：在 Study 打开与「令牌桶限流与时间窗口」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 42**：在 Study 打开与「线程池任务队列与 worker 生命周期」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 43**：在 Study 打开与「读写锁与写者优先策略」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 44**：在 Study 打开与「Treiber 栈作为无锁入门」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 45**：在 Study 打开与「Ticket Lock 公平性讨论」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 46**：在 Study 打开与「MPMC 队列仅教学对拍」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 47**：在 Study 打开与「哈希表用于两数之和、字母异位词、最长连续序列等 O(n) 查找」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 48**：在 Study 打开与「单调栈用于柱状图最大矩形、每日温度、接雨水」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 49**：在 Study 打开与「堆用于 TopK、数据流中位数、合并 K 个链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 50**：在 Study 打开与「并查集用于连通分量、冗余连接、等式方程」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 51**：在 Study 打开与「拓扑排序用于课程表、 alien 字典」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 52**：在 Study 打开与「Dijkstra 用于带权最短路；Bellman-Ford 处理负权边」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 53**：在 Study 打开与「线段树/树状数组用于区间修改与查询」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 54**：在 Study 打开与「状压 DP 用于旅行商、子集枚举」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 55**：在 Study 打开与「数位 DP 用于不含连续 1 的非负整数计数」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 56**：在 Study 打开与「莫队用于离线区间查询频率」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 57**：在 Study 打开与「二分答案用于最大化最小值、最小化最大值」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 58**：在 Study 打开与「滑动窗口维护「至多 K 个不同元素」类题」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 59**：在 Study 打开与「双指针处理有序数组三数之和、盛水容器」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 60**：在 Study 打开与「回溯处理排列组合子集分割」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 61**：在 Study 打开与「Trie 处理前缀搜索与单词搜索 II」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 62**：在 Study 打开与「LRU 链表+哈希 O(1) 增删查」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 63**：在 Study 打开与「LFU 多层双向链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 64**：在 Study 打开与「令牌桶限流与时间窗口」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 65**：在 Study 打开与「线程池任务队列与 worker 生命周期」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 66**：在 Study 打开与「读写锁与写者优先策略」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 67**：在 Study 打开与「Treiber 栈作为无锁入门」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 68**：在 Study 打开与「Ticket Lock 公平性讨论」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 69**：在 Study 打开与「MPMC 队列仅教学对拍」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 70**：在 Study 打开与「哈希表用于两数之和、字母异位词、最长连续序列等 O(n) 查找」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 71**：在 Study 打开与「单调栈用于柱状图最大矩形、每日温度、接雨水」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 72**：在 Study 打开与「堆用于 TopK、数据流中位数、合并 K 个链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 73**：在 Study 打开与「并查集用于连通分量、冗余连接、等式方程」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 74**：在 Study 打开与「拓扑排序用于课程表、 alien 字典」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 75**：在 Study 打开与「Dijkstra 用于带权最短路；Bellman-Ford 处理负权边」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 76**：在 Study 打开与「线段树/树状数组用于区间修改与查询」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 77**：在 Study 打开与「状压 DP 用于旅行商、子集枚举」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 78**：在 Study 打开与「数位 DP 用于不含连续 1 的非负整数计数」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 79**：在 Study 打开与「莫队用于离线区间查询频率」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 80**：在 Study 打开与「二分答案用于最大化最小值、最小化最大值」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 81**：在 Study 打开与「滑动窗口维护「至多 K 个不同元素」类题」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 82**：在 Study 打开与「双指针处理有序数组三数之和、盛水容器」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 83**：在 Study 打开与「回溯处理排列组合子集分割」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 84**：在 Study 打开与「Trie 处理前缀搜索与单词搜索 II」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 85**：在 Study 打开与「LRU 链表+哈希 O(1) 增删查」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 86**：在 Study 打开与「LFU 多层双向链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 87**：在 Study 打开与「令牌桶限流与时间窗口」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 88**：在 Study 打开与「线程池任务队列与 worker 生命周期」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 89**：在 Study 打开与「读写锁与写者优先策略」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 90**：在 Study 打开与「Treiber 栈作为无锁入门」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 91**：在 Study 打开与「Ticket Lock 公平性讨论」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 92**：在 Study 打开与「MPMC 队列仅教学对拍」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 93**：在 Study 打开与「哈希表用于两数之和、字母异位词、最长连续序列等 O(n) 查找」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 94**：在 Study 打开与「单调栈用于柱状图最大矩形、每日温度、接雨水」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 95**：在 Study 打开与「堆用于 TopK、数据流中位数、合并 K 个链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 96**：在 Study 打开与「并查集用于连通分量、冗余连接、等式方程」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 97**：在 Study 打开与「拓扑排序用于课程表、 alien 字典」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 98**：在 Study 打开与「Dijkstra 用于带权最短路；Bellman-Ford 处理负权边」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 99**：在 Study 打开与「线段树/树状数组用于区间修改与查询」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 100**：在 Study 打开与「状压 DP 用于旅行商、子集枚举」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 101**：在 Study 打开与「数位 DP 用于不含连续 1 的非负整数计数」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 102**：在 Study 打开与「莫队用于离线区间查询频率」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 103**：在 Study 打开与「二分答案用于最大化最小值、最小化最大值」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 104**：在 Study 打开与「滑动窗口维护「至多 K 个不同元素」类题」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 105**：在 Study 打开与「双指针处理有序数组三数之和、盛水容器」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 106**：在 Study 打开与「回溯处理排列组合子集分割」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 107**：在 Study 打开与「Trie 处理前缀搜索与单词搜索 II」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 108**：在 Study 打开与「LRU 链表+哈希 O(1) 增删查」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 109**：在 Study 打开与「LFU 多层双向链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 110**：在 Study 打开与「令牌桶限流与时间窗口」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 111**：在 Study 打开与「线程池任务队列与 worker 生命周期」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 112**：在 Study 打开与「读写锁与写者优先策略」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 113**：在 Study 打开与「Treiber 栈作为无锁入门」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 114**：在 Study 打开与「Ticket Lock 公平性讨论」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 115**：在 Study 打开与「MPMC 队列仅教学对拍」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 116**：在 Study 打开与「哈希表用于两数之和、字母异位词、最长连续序列等 O(n) 查找」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 117**：在 Study 打开与「单调栈用于柱状图最大矩形、每日温度、接雨水」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 118**：在 Study 打开与「堆用于 TopK、数据流中位数、合并 K 个链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 119**：在 Study 打开与「并查集用于连通分量、冗余连接、等式方程」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 120**：在 Study 打开与「拓扑排序用于课程表、 alien 字典」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 121**：在 Study 打开与「Dijkstra 用于带权最短路；Bellman-Ford 处理负权边」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 122**：在 Study 打开与「线段树/树状数组用于区间修改与查询」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 123**：在 Study 打开与「状压 DP 用于旅行商、子集枚举」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 124**：在 Study 打开与「数位 DP 用于不含连续 1 的非负整数计数」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 125**：在 Study 打开与「莫队用于离线区间查询频率」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 126**：在 Study 打开与「二分答案用于最大化最小值、最小化最大值」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 127**：在 Study 打开与「滑动窗口维护「至多 K 个不同元素」类题」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 128**：在 Study 打开与「双指针处理有序数组三数之和、盛水容器」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 129**：在 Study 打开与「回溯处理排列组合子集分割」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 130**：在 Study 打开与「Trie 处理前缀搜索与单词搜索 II」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 131**：在 Study 打开与「LRU 链表+哈希 O(1) 增删查」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 132**：在 Study 打开与「LFU 多层双向链表」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 133**：在 Study 打开与「令牌桶限流与时间窗口」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。
**复习检查点 134**：在 Study 打开与「线程池任务队列与 worker 生命周期」相关的 `notes.md`，用 5 分钟口述不变量，再任选索引表中一题运行 solution；若无法口述，回到 algorithms 或 data_structures 对应子目录重读示例脚本，勿在 atelier 另建单题文章代替练习。