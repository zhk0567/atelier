---
title: "题单 · Offer"
series: algorithm
category: Problems
topic_path: problems/offer
guide_toc: problem-index
guide_tier: index
status: published
date: 2026-05-22
tags: [Algorithm, 剑指Offer, LeetCode, 面试]
---

# 题单 · 剑指 Offer

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

**《剑指 Offer》** 是国内技术面试长期引用的一套题集，题号与书名章节对应，与 LeetCode 国际站题号并不一一相同。许多题目在力扣上已有同名或等价变体，本仓库在 `python/problems/offer/notes.md` 与 `cpp/problems/offer/notes.md` 维护 **30 行**「剑指题号 ↔ 本地题解目录」索引，其中 **27 行**直接指向 `problems/leetcode/<四位题号>_<slug>/`，**3 行**为剑指独占说明（尚未或不必单独建 `offer_*` 目录）。

本站 Algorithm 系列**不为每道剑指题单独发博文**。题解正文、可运行代码与复杂度分析放在 Study 仓库的 `leetcode` 子目录；本篇说明如何把 Offer 当作**国内面试语境下的复习清单**，并在 Python/C++ 双语言树中快速落点，避免在 `offer/` 下重复维护第二套 `solution`。

与 `prob-hot100`（按社区热度排序）相比，Offer 更贴近**经典教材章节顺序**与**国内面试官的口头题号**（例如「Offer 42」常指连续子数组最大和）。三者可交叉使用：Hot 100 保覆盖面，Offer 保章节记忆，CodeTop 可按公司标签补强。

原书共七十余题，本仓库索引是**可维护子集**：优先收录「已有 leetcode 题解、面试仍常问」的条目。你若在书中遇到表外题号，应先在 `python/problems/leetcode/` 按题名或题号搜索，再考虑是否向 `offer/notes.md` 提 PR 增行。增行标准不是「做过就算」，而是「双语言题解已就绪且映射稳定」。

本站不把剑指当作第二套 OJ：无在线判题、无讨论区。价值在于**离线可运行**、**笔记与代码同仓**、**Python/C++ 目录名一致**。面试展示 GitHub 时，可打开 `offer/notes.md` 说明映射策略，再点开任一 `leetcode` 子目录演示 `solution.py`，比仅展示力扣 AC 截图更有说服力。

## 预备知识

> **预备知识**：熟悉链表、二叉树、栈队列、二分与双指针、基础 DP；能在题目录运行 `python solution.py` 或 `g++ solution.cpp`。Windows 下使用 PowerShell，`Set-Location -LiteralPath` 进入含中文或空格的路径。

阅读 `offer/notes.md` 前，建议已刷过若干 `leetcode` 目录并理解本仓库命名：`四位题号 + snake_case 英文标题`。剑指表中的「力扣目录」列是相对路径 `../leetcode/...`，从 `python/problems/offer/` 出发解析。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
# 查看剑指索引（前 40 行含表头）
Get-Content -LiteralPath 'python\problems\offer\notes.md' -Encoding utf8 | Select-Object -First 40
# 示例：Offer 3 → 力扣 287 寻找重复数
Set-Location -LiteralPath 'F:\Study\Algorithm\python\problems\leetcode\0287_find_the_duplicate_number'
python solution.py
```

| 路径 | 作用 |
|------|------|
| `python/problems/offer/notes.md` | 剑指 30 题 ↔ `leetcode/` 或独占说明 |
| `cpp/problems/offer/notes.md` | 与 Python 版同构，仅语言根路径不同 |
| `python/problems/leetcode/0287_find_the_duplicate_number/` | 单题 `notes.md` + `solution.py` |
| `cpp/problems/leetcode/0287_find_the_duplicate_number/` | 对称 C++ 实现 |

`offer/` 目录**没有**聚合的 `solution.py`：索引文件记录导航约定与映射表，实现一律在 `leetcode`（或极少数未来的 `offer_<编号>_<slug>/`）中。`python/problems/offer/GUIDE.md` 描述若将来为剑指独占题建目录时的命名建议，与当前「以 leetcode 为主」策略并存。

批量检查本地是否已有实现（PowerShell 思路，不写入仓库）：从 `notes.md` 复制 `leetcode` 目录名，循环 `Test-Path` 对应 `python\problems\leetcode\<slug>\solution.py`，缺失项记入个人 TODO。此脚本仅本地自测，不修改 Git 历史。

```powershell
# 示例：检查 Offer 42 对应目录是否存在 solution.py
$slug = '0053_maximum_subarray'
$root = 'F:\Study\Algorithm\python\problems\leetcode'
Test-Path -LiteralPath (Join-Path $root $slug 'solution.py')
```

## 基础篇

### 题单用途

Offer 索引适合三类场景：**按教材章节复盘**、**面试时被报剑指题号时快速定位**、**检查本仓库是否已有等价题解**。表内 30 题覆盖数组、链表、树、栈、二分、位运算、DP、字符串与图论经典，与国内「剑指」刷题顺序接近，但不强求按 1～75 全书刷完——本仓库只收录已对齐到 `leetcode` 或标明独占的 30 行，是**可维护子集**而非全书镜像。

使用时应牢记仓库首要原则：**与力扣题意重合的不重复建题**。因此你会看到 Offer 6、24 都指向 `0206_reverse_linked_list`，Offer 10-I 指向 `0070_climbing_stairs`（斐波那契与爬楼梯同族）。这样做的好处是：改一处 `solution.py`，剑指与力扣编号两侧同时受益；代价是读表时要理解「一剑指行可能对应多道力扣语义」。

独占三行（约 10%）当前为说明性条目：**Offer 5** 替换空格、**Offer 51** 数组逆序对、**Offer 64** 求 1+2+…+n。约定是：确需代码且力扣无同题时，才新建 `offer_<编号>_<slug>/`，全库此类目录建议不超过 5 个。在目录未建之前，应以专题笔记或临时练习稿完成，不要把大段代码塞进 `offer/notes.md`。

**Offer 5（替换空格）**：原题常在字符串末尾压缩空格，与力扣部分「字符串处理」题相似但不完全等同。仓库未建 `leetcode` 链接时，可在纸上实现双指针从后向前填充，注意空格数量与数组长度关系。若日后力扣收录同题，应优先迁入 `leetcode` 并改索引行，而非长期保留独占目录。

**Offer 51（逆序对）**：经典解法为归并排序统计，时间复杂度 O(n log n)。学习时可对照 `algorithms` 目录排序专题，理解「合并时计数跨越」的不变量。面试常问复杂度与稳定性，需能脱离代码口述。

**Offer 64（1+…+n）**：考察循环与递归边界、除零与溢出意识。部分公司用其替代「简单循环题」，不宜轻视。实现时注意 Python 递归深度与 C++ 栈限制，工程上更推荐迭代求和公式 n(n+1)/2 并讨论 int 溢出。

### 与 Study 目录映射

索引表四列信息可概括为：**剑指编号**、**常见中文题名**、**力扣目录或独占说明**、（隐含）**范式标签**。下面按范式归纳 30 行中的高频落点，便于记忆而非死记整张表。

**数组与双指针**：Offer 3（重复数字）→ `0287_find_the_duplicate_number`；Offer 11（旋转数组最小值）→ `0033_search_in_rotated_sorted_array`；Offer 42（最大子数组和）→ `0053_maximum_subarray`；Offer 48（最长无重复子串）→ `0003_longest_substring_without_repeating_characters`；Offer 53（排序数组中数字出现次数）→ `0034_find_first_and_last_position_of_element_in_sorted_array`；Offer 39（超过一半的数字）→ `0169_majority_element`。

**链表**：Offer 6、24 → `0206_reverse_linked_list`；Offer 22（倒数第 k 个）→ `0019_remove_nth_node_from_end_of_list`；Offer 23（环入口）→ `0142_linked_list_cycle_ii`；Offer 25（合并有序链表）→ `0021_merge_two_sorted_lists`；Offer 34（相交链表）→ `0160_intersection_of_two_linked_lists`；Offer 35（复杂链表复制）→ `0138_copy_list_with_random_pointer`。

**树与层次遍历**：Offer 26 → `0101_symmetric_tree`；Offer 27 → `0226_invert_binary_tree`；Offer 28 → `0102_binary_tree_level_order_traversal`；Offer 55-I → `0104_maximum_depth_of_binary_tree`；Offer 68-II → `0236_lowest_common_ancestor_of_a_binary_tree`。树题建议先画三种遍历顺序，再写代码；LCA 题需分清「二叉搜索树」与「普通二叉树」版本，本表 68-II 为普通二叉树。

**栈、DP、字符串与其它**：Offer 31（栈 min）→ `0155_min_stack`；Offer 12（矩阵路径）→ `0062_unique_paths`；Offer 47（礼物最大价值）→ `0064_minimum_path_sum`；Offer 46（数字译码）→ `0091_decode_ways`；Offer 19（正则匹配）→ `0010_regular_expression_matching`；Offer 63（股票利润）→ `0121_best_time_to_buy_and_sell_stock`；Offer 66（乘积数组）→ `0238_product_of_array_except_self`；Offer 67（字符串转整数）→ `0008_string_to_integer_atoi`；Offer 15（二进制 1 的个数）→ `0136_single_number`（位运算同类）。

Python 与 C++ 使用**相同** `leetcode` 目录名；从 `cpp/problems/offer/notes.md` 跳转到 `cpp/problems/leetcode/...` 即可。若 C++ 侧尚未补某题，以 `python/problems/leetcode/` 是否存在 `solution.py` 为准，补题时保持 slug 一致。

### 如何使用题解树

推荐流程与 Hot 100 相同，但选题来源改为**剑指行**：

1. 在 `offer/notes.md` 根据今日计划选定剑指编号，沿「力扣目录」列进入 `leetcode` 子目录。
2. 阅读该目录 `notes.md`：输入输出、不变量、复杂度、边界（空链表、单节点、溢出）。
3. 运行 `python solution.py` 或编译运行 C++，直到本地断言通过。
4. 在个人复盘笔记中记录「剑指号 + 力扣号 + 范式 + 是否独立 AC」，便于面试前按剑指号检索。

**精读示例（Offer 35 复杂链表）**：打开 `0138_copy_list_with_random_pointer`，读 `notes.md` 是否说明 O(1) 空间的原地交织或哈希辅助两种路线；画图列出 `next` 与 `random` 指针；Python 通过后再看 C++ 是否需要额外注意指针别名。复盘一句话：「复制节点如何保持 random 对应关系」。

**精读示例（Offer 19 正则匹配）**：对应 `0010_regular_expression_matching`，与 Offer 46 数字译码同属字符串 DP，但状态转移更繁。建议先掌握「`.` 与 `*`」语义的手算样例，再写代码；勿与通配符题 `0044_wildcard_matching` 混淆，打开目录前核对 slug。

**精读示例（Offer 68-II LCA）**：`0236_lowest_common_ancestor_of_a_binary_tree` 需能解释「从根向下」与「后序向上返回」两种写法。面试追问深度时，连带复习 Offer 55-I 最大深度，形成树专题闭环。

**按剑指号沟通**：面试官说「Offer 23」时，打开表定位 `0142_linked_list_cycle_ii`，先口述快慢指针找相遇点、再讲入环点数学推导，最后写代码。不要先在 `offer/` 下找 `solution.py`——那里只有索引。

**与专题指南配合**：链表题多可对照 `ds-linear`；树题对照仓库内树专题；DP 类（Offer 46、47）对照 `algo-dynamic-programming` 或 `algo-dp-linear`；滑动窗口类（Offer 48）对照 `algo-sliding-window`。题单负责「考过哪道题」，专题负责「这一类为什么这么做」。

**独占题处理**：遇 Offer 5、51、64 等无 `leetcode` 链接的行，先查力扣是否已上新等价题；若有，优先在 `leetcode` 建目录并**回写**索引表，而不是长期留在独占说明。若确无同题，再评估是否值得占用「≤5 个 `offer_*` 目录」配额。

### 维护与对齐

维护 Offer 索引时，按以下顺序操作可减少链接失效：

1. **新增 leetcode 题解**：先创建 `python/problems/leetcode/<slug>/` 与 `notes.md`、`solution.py`，C++ 可选同步。
2. **更新映射表**：在 `python/problems/offer/notes.md` 增加或修改一行，并在 `cpp/problems/offer/notes.md` 保持同构（C++ 文件可简短指向 Python 版）。
3. **禁止**在索引表粘贴长篇题解或调试日志；表行只保留链接与简短独占标记。
4. **合并重复**：多道剑指指向同一 `leetcode` 目录时，在 commit message 中注明「offer: map #6,#24 → 0206」，避免后人误以为漏题。

本 atelier 博文**不镜像**完整 30 行表格，避免双份维护；以 GitHub 上 `notes.md` 为题号真相来源。若你向远程仓库提交映射变更，无需同步改本站除非题单结构或约定本身变化。

**质量自检（单行）**：索引链接可打开 → `solution.py` 通过 → `notes.md` 含复杂度 → C++ 可编译（若有）→ 能闭卷复述剑指题意。五项齐全再在个人打卡表勾选。

**剑指 30 行速查（打印用，目录名为本地入口）**：3→`0287`；5→独占；6/24→`0206`；10-I→`0070`；11→`0033`；12→`0062`；15→`0136`；19→`0010`；22→`0019`；23→`0142`；25→`0021`；26→`0101`；27→`0226`；28→`0102`；31→`0155`；34→`0160`；35→`0138`；39→`0169`；42→`0053`；46→`0091`；47→`0064`；48→`0003`；51→独占；53→`0034`；55-I→`0104`；63→`0121`；64→独占；66→`0238`；67→`0008`；68-II→`0236`。打印后可在纸面勾选派系，不必抄整张 Markdown 表。

**与力扣「剑指 Offer」专题的关系**：力扣 App 内专题题号与本表剑指列大体相近，但平台会增删改题；本仓库以**能稳定打开本地目录**为准。若力扣新增题而表内尚无，先在 `leetcode` 搜索是否已有同 slug，再决定是否扩表。不要把力扣讨论区代码粘贴进 `offer/notes.md`——讨论区版本往往缺断言、难 diff。

**错误定位习惯**：`python solution.py` 失败时，先读 Traceback 行号，再对照子目录 `notes.md` 的边界说明；逻辑错误用最小样例手算。C++ 编译失败优先检查 `-std=c++17` 与 `alg_std.hpp` 路径。调试记录写在个人笔记或 leetcode 子目录 issue，不要污染索引文件。

**时间盒建议**：每题 25 分钟独立思考 + 10 分钟复盘；超时则标记「需重试」次日再来。30 题完整双语言跑通约需二十至三十小时量级，按每周 6 题约五周，可按基础加减。

**协作约定**：多人共用仓库时，约定「只改 leetcode 子目录实现，改 offer 表需两人确认」；合并冲突以能跑通 `solution` 的一侧为准，再手工对齐映射行。

**反模式**：在 `offer/` 下为已有 leetcode 题再建 `offer_03_` 重复实现；把 30 行表按力扣题号排序（破坏剑指记忆）；在索引里贴长篇代码。 **正向模式**：leetcode 小目录 + 短笔记 + 可运行 solution；offer 表只做导航；本站专题做范式沉淀。

## Python 实现

题单目录无聚合脚本；下列节选来自映射表中的代表性 `leetcode` 题解，完整代码与断言在 Study 仓库对应目录。

**Offer 3 → 287 寻找重复数（快慢指针 / 原地思想）**

```python
# python/problems/leetcode/0287_find_the_duplicate_number/solution.py
def find_duplicate(nums: list[int]) -> int:
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
```

**Offer 42 → 53 最大子数组和（Kadane）**

```python
# python/problems/leetcode/0053_maximum_subarray/solution.py
def max_sub_array(nums: list[int]) -> int:
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
```

**Offer 23 → 142 环入口（Floyd + 重置指针）**

```python
# python/problems/leetcode/0142_linked_list_cycle_ii/solution.py
from __future__ import annotations

class ListNode:
    def __init__(self, val: int = 0, nxt: ListNode | None = None):
        self.val = val
        self.next = nxt

def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            ptr = head
            while ptr is not slow:
                ptr = ptr.next
                slow = slow.next
            return ptr
    return None
```

**Offer 11 → 33 旋转数组最小值（二分变种）**

```python
# python/problems/leetcode/0033_search_in_rotated_sorted_array/solution.py
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

**Offer 48 → 3 无重复最长子串（滑动窗口）**

```python
# python/problems/leetcode/0003_longest_substring_without_repeating_characters/solution.py
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

运行方式：对每题 `Set-Location -LiteralPath` 到该 `leetcode` 子目录后执行 `python solution.py`。不要在仓库根目录运行，以免 import 路径错误。部分题目 `__main__` 中带断言，通过即视为本地用例 OK。

## C++ 实现

C++ 题解位于 `cpp/problems/leetcode/<相同 slug>/`，多数包含 `#include <alg_std.hpp>`。与 Python 对照阅读时，重点看容器选择、`long long` 与边界。

**Offer 42 → 53 最大子数组和**

```cpp
// cpp/problems/leetcode/0053_maximum_subarray/solution.cpp
#include <alg_std.hpp>
using namespace std;

int maxSubArray(vector<int>& nums) {
    int best = nums[0], cur = nums[0];
    for (size_t i = 1; i < nums.size(); ++i) {
        cur = max(nums[i], cur + nums[i]);
        best = max(best, cur);
    }
    return best;
}
```

**Offer 25 → 21 合并两个有序链表**

```cpp
// cpp/problems/leetcode/0021_merge_two_sorted_lists/solution.cpp
#include <alg_std.hpp>
using namespace std;

ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
    ListNode dummy(0);
    ListNode* tail = &dummy;
    while (l1 && l2) {
        if (l1->val <= l2->val) {
            tail->next = l1;
            l1 = l1->next;
        } else {
            tail->next = l2;
            l2 = l2->next;
        }
        tail = tail->next;
    }
    tail->next = l1 ? l1 : l2;
    return dummy.next;
}
```

编译示例：

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\problems\leetcode\0053_maximum_subarray'
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe solution.cpp
.\run.exe
```

**Offer 23 → 142 环入口（与 Python 同思路）**

```cpp
// cpp/problems/leetcode/0142_linked_list_cycle_ii/solution.cpp
#include <alg_std.hpp>
using namespace std;

ListNode* detectCycle(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            ListNode* ptr = head;
            while (ptr != slow) {
                ptr = ptr->next;
                slow = slow->next;
            }
            return ptr;
        }
    }
    return nullptr;
}
```

Offer 索引中约九成题目可按上表路径在 C++ 树找到对称实现；若无，先完成 Python 侧再补 C++，目录名勿自创别名。编码文件请保存为 UTF-8；路径含中文时 PowerShell 必须用 `-LiteralPath`。

## 练习与延伸

- **按剑指章节**：每周完成表中 6～8 行，周末用「剑指号 + 范式」做口述复盘，不追求一次抄完 30 行。
- **与 Hot 100 交叉**：例如 Offer 48 与 Hot 100 第 3 题同为无重复最长子串，第二次做应计时并比较两次解法差异。
- **面试高频**：表末指向 `interview/top_frequent/notes.md`，适合在 Offer 子集刷完一轮后加码。
- **独占题预习**：Offer 51（逆序对）可先读归并排序专题再在纸上实现；Offer 64（1+…+n）注意递归终止与除零，与 `algorithms` 目录笔记对照。
- **专题加深**：栈 min（Offer 31）可结合 `0155_min_stack` 与手写栈专题；复杂链表（Offer 35）建议画图再写 `0138_copy_list_with_random_pointer`。
- **八周计划示例**：第 1～2 周数组/二分（3、11、39、42、48、53、66）；第 3 周链表全表；第 4 周树（26、27、28、55、68）；第 5 周栈与字符串（31、19、67）；第 6 周 DP（12、46、47、63）；第 7 周独占题+归并预习（51、64、5）；第 8 周混合模拟+口述剑指号。
- **复盘模板**：日期 / 剑指号 / 力扣号 / 范式 / 是否独立 AC / 易错点 / 次日能否重写。坚持复盘比多刷十题更能应对「报 Offer 号」的面试。
- **离线阅读**：地铁上可读各 `leetcode/notes.md` 复习思路，有电脑再跑代码；`offer/notes.md` 纯 Markdown，不依赖会员。
- **面试沟通**：可说明「按剑指号映射到本地双语言题解树，重合题不重复维护，重范式复盘」。配合 `interview/classic` 设计题展示体系化积累。

## 学习路径

| 阶段 | 建议 |
|------|------|
| 入门 | 先刷 `overview`，再完成 Offer 表中链表 5 题（6/22/23/25/34） |
| 巩固 | 按本表 30 行整轮，标记薄弱范式（树、DP、字符串） |
| 冲刺 | Offer 随机抽题 + `prob-hot100` + `iv-top-frequent` 混合模拟 |

若时间紧，优先**链表 + 树 + 数组 DP** 三类，它们在国内面试中出现频率高于孤立字符串题。每完成一题，在索引表对应行尾做个人标记（勿提交无意义勾选到公共仓库）。

**入门周（仅链表）**：按映射表依次 6→22→23→25→34→35，每天 1～2 题，周末用白纸默画指针变化。第二周再进入数组题，避免同时开太多范式导致记忆混乱。

**巩固周（树+栈）**：26、27、28、55、31 五题可在四天内完成，剩余时间做 68-II。栈 min 与设计题 LRU 不同，勿混用模板。

**冲刺周**：从 30 行中随机抽 8 题，每题 20 分钟写骨架 + 5 分钟口述；配合 `iv-top-frequent` 中手写题对照。冲刺阶段少看新题，多看已 AC 题的 `notes.md` 不变量。

## 延伸阅读

- [Study：python/problems/offer/notes.md](https://github.com/zhk0567/Algorithm/blob/main/python/problems/offer/notes.md)
- [Study：cpp/problems/offer/notes.md](https://github.com/zhk0567/Algorithm/blob/main/cpp/problems/offer/notes.md)
- [《剑指 Offer》原书](https://book.douban.com/subject/25907339/)（题号与书中章节对照）
- 仓库根 [README](https://github.com/zhk0567/Algorithm/blob/main/README.md) 与 [algorithms 专题](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms)
- 本站：`prob-hot100`（热度题单）、`iv-top-frequent`（面试高频手写）

---

**发布前自检**：导读是否说明「不做单题博文」；是否给出 PowerShell `-LiteralPath`；是否区分 python/cpp 路径；Python/C++ 节是否含可运行代码围栏；基础篇是否仅用 `###` 而无 `####`。五项满足后，在 atelier 运行 `validate_algorithm_guide.py` 与 `validate_algorithm_quality.py` 的 `--strict` 校验。

**重装系统或换盘**：克隆仓库后把示例中的 `F:\Study\Algorithm` 全局替换为新路径；本篇路径仅作演示。`git pull` 后再刷题，避免索引指向已删除目录。

**统计说明**：本表 30 行、27 行直链 `leetcode`、3 行独占，比例约 90% / 10%；与仓库 README 中「剑指 ↔ leetcode」策略一致。atelier `manifest.json` 中 `prob-offer` 仅对应本篇索引专题，不包含 30 个独立 slug。站点 Algorithm 指南数保持专题级，与题解树解耦。

**给未来的你**：半年后再打开 Offer 表，先 `git pull`，再随机抽 5 个剑指号限时重写；不必重读全文，重点看表是否新增行、个人勾选是否诚实。题单博文随仓库演化，以 GitHub `notes.md` 为唯一映射真相来源。读完本篇即可去 `leetcode` 目录动手，不必背下全文。

**术语统一**：「题解树」指 `problems/leetcode/<slug>/` 集合；「题单」指 offer/hot100/codetop 的 `notes.md`；「双语言」指 `python/` 与 `cpp/` 镜像路径。「直链」指索引行中的 `../leetcode/...` 相对链接，从 `offer/` 目录点击即可在编辑器中跳转。

**安全与诚信**：仓库代码仅供学习，勿接入自动刷题或批量提交脚本；面试现场须独立写码。笔记请用自己的话写，避免面试官追问细节时无法解释。

**键盘工作流**：在 VS Code 中 `Ctrl+P` 输入 `0142_linked_list` 可直达文件夹；从 `notes.md` 复制 slug 比记忆四位题号更快。英文 slug 与力扣英文标题对应，便于在国际面试中沟通题意。

**与单题博文的边界**：atelier Algorithm 系列 82 篇为专题级；剑指每一道题的正文只在 Study 仓库维护。若未来单独立项某题博文，将不改变本题单索引的定位。

**贡献流程**：向 `zhk0567/Algorithm` 提 PR 时，若只改 `leetcode` 题解，无需改 atelier；若调整 30 行映射结构，可在 PR 描述中 @ 维护者并同步检查本篇「维护与对齐」是否仍准确。站点 `prob-offer` 更新频率应低于代码仓库。
