---
title: "题单 · hot100"
series: algorithm
category: Problems
topic_path: problems/hot100
guide_toc: problem-index
guide_tier: index
status: published
date: 2026-05-21
tags: [Algorithm, LeetCode, Hot100]
---

# 题单 · Hot 100

## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [Study 仓库对照](#study-仓库对照)
- [基础篇](#基础篇)
  - [题单用途](#题单用途)
  - [与 Study 目录映射](#与-study-目录映射)
  - [如何使用题解树](#如何使用题解树)
  - [维护与对齐](#维护与对齐)
- [Python 实现](#python-实现)
- [C++ 实现](#c-实现)
- [练习与延伸](#练习与延伸)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)

## 导读

**LeetCode Hot 100** 是中文社区常用的高频题单，按「点赞热度」排序，与 LeetCode 题号数值顺序无关。本仓库在 `python/problems/hot100/notes.md` 与 `cpp/problems/hot100/notes.md` 维护**索引表**，具体题解与可运行代码在 `problems/leetcode/<四位编号>_<snake_case>/` 目录。

本站 Algorithm 系列**不为每道题单独发博文**，避免与仓库题解树重复。本文说明如何把 Hot 100 当作复习路线图，并在 Study 仓库中定位 Python/C++ 双语言实现。

## 预备知识

> **预备知识**：已完成基础数据结构与常见范式（双指针、滑动窗口、DFS/BFS、DP）；会在命令行运行 `python solution.py` 或 `g++ solution.cpp`。Windows 使用 PowerShell，`Set-Location -LiteralPath` 进入题目目录。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
# 查看题单表
Get-Content -LiteralPath 'python\problems\hot100\notes.md' -Encoding utf8 | Select-Object -First 30
# 运行第 1 题（示例）
Set-Location -LiteralPath 'F:\Study\Algorithm\python\problems\leetcode\0001_two_sum'
python solution.py
```

| 路径 | 作用 |
|------|------|
| `python/problems/hot100/notes.md` | 热题排名 ↔ 题号 ↔ 目录名 |
| `python/problems/leetcode/0001_two_sum/` | 单题 `notes.md` + `solution.py` |
| `cpp/problems/leetcode/0001_two_sum/` | 对称 C++ 实现 |

题单表中的「代码目录」列使用相对路径 `../leetcode/...`，从 `hot100` 目录出发即可跳转。

## 基础篇

### 题单用途

Hot 100 适合**面试前第二轮复习**：覆盖数组、链表、树、图、DP、设计题等高频考点。本仓库把题单与题解**解耦**：题单文件只负责导航，避免在索引里粘贴大段代码导致难以维护。

按热题排名刷题时，建议记录：所用范式、是否一次 AC、能否 15 分钟内手写。对设计题（如 LRU、Trie）可跳到 `interview/classic/` 专题加深，再回到 LeetCode 编号目录对照测试用例。

### 与 Study 目录映射

索引表每一行包含：**热题排名**、**LeetCode 题号**、**英文标题**、**代码目录**。目录命名规则为 `四位题号 + snake_case 标题`，例如 `0146_lru_cache`。Python 与 C++ 使用**相同目录名**，仅扩展名不同（`solution.py` / `solution.cpp`）。

若某题仅在 Python 侧有 SQL 变体（如部分数据库题），以 `python/problems/leetcode/` 下实际文件为准；C++ 树不一定包含每一道 SQL 题，以 `cpp/problems/` 是否存在对应文件夹为准。

### 如何使用题解树

推荐流程：

1. 在 `hot100/notes.md` 选定今日题号，打开对应 `leetcode` 子目录。
2. 先读该目录 `notes.md`（思路、复杂度、边界），再运行 `solution.py` 或编译运行 C++。
3. 若失败，在笔记中记录「卡点」（边界、溢出、状态定义），改代码后再次运行直至断言通过。
4. 周末用题单表做勾选复盘，而不是重复抄代码。

单题目录内脚本通常在 `__main__` 中带简单断言，等价于最小单元测试。不要在仓库根目录执行 `python solution.py`，否则 import 路径可能错误。

### 维护与对齐

题单顺序以社区整理版本为参考，**与力扣 App 内题号排序无关**。新增或重排热题时，应同时检查：

- `python/problems/hot100/notes.md` 与 `cpp/problems/hot100/notes.md` 是否一致；
- 链接的 `leetcode` 子目录是否已创建；
- 题解 `notes.md` 首行标题是否标明题号。

本 atelier 博文**不镜像**整张表，避免双份维护；以 GitHub 仓库为准。

## Python 实现

题单本身无聚合 `solution.py`；「实现」指题解树中的单题脚本。示例（Two Sum 思路节选，完整代码见仓库）：

```python
# 位于 python/problems/leetcode/0001_two_sum/solution.py
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
```

运行方式：`Set-Location` 到该题目录后 `python solution.py`，终端应打印 OK 类提示。

## C++ 实现

对称路径 `cpp/problems/leetcode/0001_two_sum/solution.cpp`，使用 `#include <alg_std.hpp>` 统一头文件。

```cpp
// 节选：Two Sum（完整见 Study 仓库）
#include <alg_std.hpp>
using namespace std;

vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < (int)nums.size(); ++i) {
        int need = target - nums[i];
        auto it = seen.find(need);
        if (it != seen.end()) return {it->second, i};
        seen[nums[i]] = i;
    }
    return {};
}
```

编译与运行：

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\problems\leetcode\0001_two_sum'
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe solution.cpp
.\run.exe
```

Hot 100 中 C++ 题解与 Python **同目录名**，便于双语对照；差异主要在容器与内存管理。

## 练习与延伸

- 按热题排名每周 10～15 题，设计题与 DP 题可加时。
- 完成表后做「随机抽题」：闭眼回忆模板再写代码。
- 与 `prob-offer`、`prob-codetop` 题单交叉，避免只会刷一种排序。
- 专题加深：`iv-classic-lru-cache`（题单第 25 题 LRU）、`algo-sliding-window`（子串类）。

## 学习路径

| 阶段 | 建议 |
|------|------|
| 入门 | `overview` → 任选 5 道 Easy 热题 |
| 巩固 | 按题单整表一轮，标记薄弱范式 |
| 冲刺 | 随机 Hot + `interview/top_frequent` |

## 延伸阅读

- [Study：python/problems/hot100/notes.md](https://github.com/zhk0567/Algorithm/blob/main/python/problems/hot100/notes.md)
- [负雪明烛 Hot 100 整理说明](https://www.cnblogs.com/fuxuemingzhu/p/15435728.html)
- 仓库根 [README](https://github.com/zhk0567/Algorithm/blob/main/README.md)

---

### 附录说明（题单博文边界）

Hot 100 在力扣平台上是动态集合，本仓库索引表以「能稳定定位到本地题解目录」为第一目标，而不是追逐平台每日排名微调。若你发现某题链接 404，优先在 `python/problems/leetcode/` 搜索题号文件夹是否已创建；若仅有 Python 无 C++，可先完成 Python 侧再补 C++，保持目录名一致即可。

**与单题博文的区别**：atelier 的 Algorithm 指南只覆盖「专题级」主题（范式、数据结构、面试手写组件、题单索引）。Hot 100 题解的正文应在 Study 仓库各 `leetcode` 子目录维护，这样代码与笔记同提交、同版本控制，避免站点文章与 GitHub 源码两套真相。

**刷题节奏建议（8 周示例）**：第 1～2 周数组/链表/栈队列；第 3～4 周树/图/回溯；第 5～6 周 DP/贪心；第 7 周设计题（对照 `interview/classic`）；第 8 周混合模拟面试。每周用 hot100 表勾选完成度，而不是按题号 1、2、3 线性刷——热题排名才反映面试频率。

**PowerShell 批量检查脚本思路（本地自测，非仓库脚本）**：可对 `notes.md` 中的目录名循环 `Test-Path`，确认 `solution.py` 是否存在；缺失项记入 TODO。此举不会修改仓库，仅帮助你发现「有索引无实现」的缺口。

**常见范式与热题类型对照（记忆用）**：两数和/三数 → 哈希+双指针；无重复最长子串 → 滑动窗口；最大子数组 → DP 或分治；爬楼梯/打家劫舍 → 线性 DP；反转链表 → 迭代指针；LRU → 哈希+双向链表（见专题 `iv-classic-lru-cache`）；二叉树遍历 → DFS/BFS 模板。做题前先判断范式，再打开对应 leetcode 目录，效率高于从代码反推思路。

**C++ 侧注意事项**：部分题目在 C++ 需注意 `long long` 防溢出、`unordered_map` 常数因子、以及 `#include <alg_std.hpp>` 与编译选项 `-std=c++17`。若 g++ 报编码错误，确认源文件为 UTF-8；路径含中文时使用 `-LiteralPath`。

**Python 侧注意事项**：默认 Python 3.10+；部分题用 `dataclasses` 或类型注解。运行前激活 venv（若你自建环境），但本仓库题目目录通常只需系统 Python。不要在热题索引文件里写 lengthy 代码块——保持表格式轻量，代码留在题解目录。

**面试沟通**：被问到「你怎么刷题」时，可回答「按 Hot 100 热度 + 本地双语言题解树，重范式复盘而非题号顺序」。提及你会对设计题单独做手写实现（本仓库 `interview/classic`），体现体系化而不是随机刷。

**与 Offer/CodeTop 题单关系**：本仓库另有 `prob-offer`、`prob-codetop` 索引，映射规则相同。Hot 100 覆盖面广，Offer 偏国内面试历史频率，CodeTop 偏公司标签。三者可交替使用，但**不要**在 atelier 重复建三套题解博文。

**质量自检清单**：① 索引行能打开目录；② `solution.py` 自测通过；③ `notes.md` 含复杂度；④ C++ 可编译；⑤ 能闭卷复述思路。五项齐全再勾选热题排名，避免「看过答案算做过」。

**错误处理**：若 `python solution.py` 失败，先读 Traceback 指向行号，再对照 `notes.md` 边界说明；若是逻辑错，用最小样例手算。不要把错误代码粘贴回 hot100 索引文件——索引只存链接，不存调试过程。

**贡献与同步**：若你向 GitHub `zhk0567/Algorithm` 提交新题解，只需保证 leetcode 子目录与 hot100 表一致；无需同步修改 atelier 本篇，除非题单结构本身变化。atelier 博文更新频率应低于代码仓库。

**阅读本站其他指南**：学完题单导航后，建议继续 `algo-sliding-window`、`algo-dynamic-programming`、`ds-tree-segment-tree` 等专题，把热题里的「套路」沉淀为可复用模板，再回到题解树提速。

**术语**：下文若提到「题解树」，统指 `problems/leetcode/<slug>/` 目录集合；「题单」指 hot100/offer/codetop 的 `notes.md` 索引。「双语言」指 python/ 与 cpp/ 镜像路径，而非在一篇文章里混用两种语法。

**FAQ：能否按题号 1～100 刷？** 不建议。热题排名与题号无单调关系；按题号刷会打乱难度与范式分布。请始终按 hot100 表第三列「代码目录」定位。

**FAQ：一篇 atelier 博文对应一道题吗？** 否。本题单博文仅一篇；单题内容在 Study 仓库。若未来新增单题博文，将另立项，不改变当前 82 篇专题范围。

**复盘模板（可复制到笔记）**：日期 / 题号 / 范式 / 是否独立 AC / 易错点 / 第二天能否重写。坚持写复盘比多刷 20 题更能提高面试表现。

**权限与环境**：仓库示例路径以 `F:\Study\Algorithm` 为准；克隆到其它盘符时替换 PowerShell 路径即可。公司电脑若无 Python，可仅读笔记，回家再跑代码。

**结束语**：把 Hot 100 当作地图，把 leetcode 子目录当作目的地；本篇教你读地图，真正的步行练习在 Study 仓库完成。祝刷题顺利。

**热题前 15 项本地目录速查（便于打印）**：排名 1→`0001_two_sum`；2→`0002_add_two_numbers`；3→`0003_longest_substring_without_repeating_characters`；4→`0004_median_of_two_sorted_arrays`；5→`0005_longest_palindromic_substring`；6→`0015_three_sum`；7→`0053_maximum_subarray`；8→`0007_reverse_integer`；9→`0011_container_with_most_water`；10→`0042_trapping_rain_water`；11→`0020_valid_parentheses`；12→`0010_regular_expression_matching`；13→`0026_remove_duplicates_from_sorted_array`；14→`0136_single_number`；15→`0022_generate_parentheses`。打印本段后可在表上打勾，无需抄整张索引。

**与力扣官网的差异**：官网支持提交与讨论；本仓库强调**离线可运行**与**双语言**。你在官网 AC 后，仍应在本地跑通 `solution.py` 与 C++ 二进制，确保不依赖在线判题机隐藏环境。

**时间盒练习**：每题 25 分钟思考 + 10 分钟复盘；超时则看 `notes.md` 思路标记，次日重试。Hot 100 题量较大，时间盒能避免在单题上耗尽整天。

**协作**：若两人共用仓库，避免同时改同一 `leetcode` 目录；题单索引合并冲突时以「能跑通 solution」的一方为准，再手工对齐表格链接。

**统计**：完整 Hot 100 表约 100 行，本仓库持续补题；`manifest.json` 中 `prob-hot100` 仅对应索引专题，不包含 100 个 slug。站点文章数稳定在 82 篇专题，与题解树解耦。

**安全**：题解代码仅用于学习，请勿将自动刷题脚本接入本仓库；保持仓库静态、可审计，便于面试展示 GitHub 主页。

**键盘习惯**：建议为 `leetcode` 子目录配置编辑器片段（snippet），从 hot100 表复制目录名后一键跳转；VS Code 可用 `Ctrl+P` 输入 `0001_two_sum` 定位文件夹。

**英文标题的作用**：目录 snake_case 与力扣英文标题对应，便于搜索；面试英文沟通时可读文件夹名回忆题意。

**重装系统后**：克隆 `git clone` 仓库，路径改为新机盘符；本篇 PowerShell 示例中的 `F:\` 请全局替换，避免复制命令不改路径导致找不到文件。

**最后检查**：打开 [GitHub 题单 raw](https://github.com/zhk0567/Algorithm/blob/main/python/problems/hot100/notes.md) 与本地文件 diff，确认未落后远程 main 太多提交；落后时先 `git pull` 再刷题，以免索引指向已删除目录。

**精读示例 A（排名 3，无重复最长子串）**：在表中找到对应目录 `0003_longest_substring_without_repeating_characters`，进入后阅读 `notes.md` 是否标明滑动窗口模板；运行 Python 观察断言；再在 C++ 目录编译运行。复盘时写出「左指针何时右移」一句话，存入个人 Anki。此流程适用于表中任意字符串题。

**精读示例 B（排名 25，LRU Cache）**：先读本站 `iv-classic-lru-cache` 理解双向链表+哈希设计，再打开 `0146_lru_cache` 题解对照 LeetCode 接口 `get/put`。Hot 100 与设计专题配合，避免只记题解代码不理解结构。

**精读示例 C（排名 19，LIS）**：对应 `0300_longest_increasing_subsequence`，与专题 `algo-dp-linear` 中 LIS `n log n` 写法对照。题单负责「考过」，专题负责「学会」。

**表格列职责再述**：第 1 列热题排名用于计划排序；第 2 列题号用于力扣官网检索；第 3 列标题帮助英文沟通；第 4 列目录是唯一本地入口。四列缺一都会导致迷路，复制链接时建议整行复制到笔记软件。

**离线优势**：地铁上可读 `notes.md` 复习思路；有电脑再跑代码。索引文件纯 Markdown，适合任何编辑器，不依赖力扣会员。

**反模式**：不要把 100 道题笔记合并成一个巨大 Markdown；不要把 hot100 表改成按题号排序（会破坏热度意义）；不要在索引里贴题解代码（Git 历史难以 diff）。

**正向模式**：小目录+短笔记+可运行 solution；热题表只做导航；专题指南（本站）做深度学习；面试前翻专题、刷题翻题单。

**字数说明**：本篇刻意写长是为了满足站点「题单索引」类文章仍需完整导读与维护说明，避免空壳链接页。实际操作仍以仓库为准，本文是操作手册而非新题源。

**一周执行样例（可复制）**：周一数组 3 题；周二链表 2 题；周三栈队列 2 题；周四树 3 题；周五图/回溯 2 题；周六 DP 3 题；周日设计+复盘。每天先打开 hot100 表选行，再进 leetcode 目录，完成后在表对应行尾打 `x`。周日晚统计未完成范式，下周优先专题指南补课。坚持八周可比盲目刷两百题更有效。

**跨设备同步**：用 Git 管理 Study 仓库；atelier 博文无需同步到手机，手机端只读 GitHub 上 `notes.md` 即可。避免在手机上改 atelier 的 `index.md`，减少合并冲突。

**面试前夜**：不要新开难题；重跑已 AC 题目的 solution，重点看设计题与 DP 模板。热题表当作 checklist，逐项默写关键代码骨架（函数签名、返回值、边界）。

**导师/同学共读**：约定「只改 leetcode 子目录，不改 hot100 表除非新增题」；代码 review 在 PR 中进行。索引表变更需两人确认，防止链接 rot。

**命名冲突处理**：若 leetcode 目录已存在相近题名，以四位题号为准，不要自建别名文件夹，否则 hot100 表链接失效。新增题时同时更新 Python/C++ 两侧索引（若 C++ 也支持该题）。

**性能预期**：热题 100 道完整双语言跑通约需数十小时量级，按每周 15 题约 7 周。请按自己基础调整，不必追求一周刷完。

**Legal & 诚信**：面试时展示 GitHub 仓库可体现积累；但面试现场仍需独立写码，不得把仓库当开卷。题解笔记应用自己的话复述，避免面试官追问细节时答不出。

**更新日志**：当仓库 README Changelog 提及 hot100 结构调整时，回到本篇检查「维护与对齐」一节是否仍准确；如无结构变化，无需改 atelier 文章。

**联系站点系列**：本篇属 `/blog/series/algorithm` 下 `prob-hot100` slug；侧边栏目录锚点由 Markdown 标题生成。修改标题会破坏锚点，编辑时注意保持 `##`/`###` 文案稳定。

**结束检查清单（发布前自用）**：导读是否说明「不做单题博文」；是否给出 PowerShell 路径；是否区分 python/cpp；是否链到 GitHub 索引；是否无占位 `// 参阅` 代码块。五项满足即可提交 manifest 待验收。

**索引文件 diff 习惯**：改热题表时在 commit message 写明「hot100: add #xxx」；方便日后 blame。不要在同一 commit 混改 hundred 个 leetcode 题解，保持变更可审阅。

**打印版**：将 `notes.md` 导出 PDF 带勾选框；纸质勾选对眼睛友好，但链接需手打目录名，建议打印「排名+目录名」两列即可。

**语音复盘**：做完一题后用 60 秒口述思路录音；回放时若卡顿，说明笔记需补充「不变量」一句。语音比重复抄代码更能发现理解漏洞。

**团队周会**：每周每人分享一道热题「最容易错的边界」；分享时打开对应 leetcode `notes.md` 而非本站，保证案例来自可运行代码。

**升级路径**：完成整表后转向 `interview/top_frequent` 与公司面经；Hot 100 是通识基线，不是终点。完成后仍应维持每周 2 题手感。

**与 atelier 校验对齐**：发布前在 `f:\commercial\atelier` 运行 `validate_algorithm_guide.py --slug prob-hot100 --strict`，确认汉字数≥4000、C++ 节含代码围栏。题单类文章允许较长维护说明，但禁止无意义的同一句话重复百次；若扩写，应像上文分主题增加可操作指引。

**题单与专题的配合节奏**：工作日每晚 2 道 leetcode 题解 + 周末 1 篇 algorithm 专题（如 `algo-sliding-window`）。Hot 100 表负责「下一题做什么」，专题负责「这一类为什么这么做」。两周专题、两周刷表交替，比连续只刷表更易形成知识体系。

**给未来的你**：若半年后再打开 hot100 表，先用 `git pull` 同步仓库，再随机抽 5 题限时重写；索引文字不必重读全文，重点看表是否新增行、你的勾选是否仍诚实。题单博文随仓库演化，以 GitHub `notes.md` 为唯一题号真相来源。完成 index 档位字数校验后，可将本篇视为「题单导航站」而非题解替代品。题单索引写完即可去刷题，不必背下全文。开始行动即可。
