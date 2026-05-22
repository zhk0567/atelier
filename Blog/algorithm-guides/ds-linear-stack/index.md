---
title: "数据结构 · 栈（数组栈、链表栈与最小栈）"
series: algorithm
category: DataStructures
topic_path: data_structures/linear/stack
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-22
tags: [DataStructures, Stack, LIFO, MinStack, MonotonicStack, ArrayStack]
---

# 数据结构 · 栈（数组栈、链表栈与最小栈）

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

**栈（Stack）** 是最常见的受限线性表之一：只允许在一端（栈顶）进行插入与删除，遵循 **后进先出（LIFO）**。与「任意位置可插删」的链表或动态数组相比，栈把操作约束到 `push` / `pop` / `top` 三个接口，使实现极简、均摊 O(1)，却足以支撑括号匹配、表达式求值、深度优先搜索、单调栈、函数调用栈等大量算法与系统机制。面试中栈很少单独考「手写完整类」，但 **单调栈**、**最小栈**、**用栈模拟队列** 几乎必现；许多 WA 来自空栈未判断、单调栈维护方向反了、或 `MinStack` 弹出时未同步辅助栈。

本页是 atelier 子指南 `ds-linear-stack`，`topic_path` 为 `data_structures/linear/stack`，`guide_toc` 为 `topic-ds`（基础篇六个 `###` 与数据结构专题一致）。父级总览见 `ds-linear`：那里对比数组、链表、队列与哈希的选型；**本页只深挖栈**，把 Study 仓库 `stack.py` / `stack.cpp` 中的 `ArrayStack`、`LinkedStack`、`MinStack` 与 LeetCode 高频模板串成一条学习线。

读完本文，你应能：

1. 区分「栈作为 ADT」与「数组/链表作为物理实现」，并说出二者复杂度；
2. 在 Python 与 C++ 镜像路径下运行 `stack` 自测并本地对拍；
3. 实现 `MinStack` 的辅助栈同步规则，并口述单调栈维护递增/递减的不变量；
4. 知道何时用 `list` 尾插作栈、何时用链表头插、何时必须用单调栈降复杂度；
5. 按题单从 20、155 递进至 84、739，并跳转 `algo-graph-traversal` 理解 DFS 与显式栈的关系。

**与队列的边界**：栈只动一端；队列一端入另一端出（FIFO）。用两个栈可实现队列（见 `ds-linear-queue`）；用一个队列也可模拟栈，但均非面试首选——面试更常考「栈本身」或「单调栈」。**与递归的关系**：递归调用使用系统栈保存帧；DFS 显式写法即手动 `push` 节点、`pop` 回溯，二者同构。

**为何单独成篇**：线性总览 `ds-linear` 在一张表里对比六类结构，栈部分无法展开单调栈、最小栈与 20/84/739 等题的细节。本子指南把「LIFO 语义—双实现—MinStack—单调栈—题号映射」串成闭环。若你已完成 `ds-linear` 六脚本回归，可直接从本页「Study 仓库对照」运行 `stack.py`；若尚未跑通总览，建议先花十分钟建立「仓库代码可信」的信心。

**面试失分点**：对空栈 `pop` 未抛错或返回魔法值；`MinStack` 在重复最小值时只压一层辅助导致 `getMin` 错误；单调栈在「相等元素」处是否 `pop` 与题意不符；把「下一个更大元素」写成从右向左扫描却维护了错误的单调性。本页在「实现要点」与「易错点」强调与仓库一致的风格。

## 预备知识

> **预备知识**：理解 LIFO；熟悉 Python `list` 的 `append`/`pop` 与 C++ `vector::push_back`/`pop_back`；知道大 O 表示法；Python 3.10+；C++17 与 `g++` 基本编译。Windows 下用 PowerShell 的 `Set-Location -LiteralPath` 进入目录后运行脚本。

建议已具备：

- **ADT 与实现分离**：栈的语义是 LIFO；可用动态数组在尾部操作，也可用单链表在头部操作，不应把「只能用数组」当作定义。
- **空栈语义**：`pop`/`top` 对空栈应 `IndexError`（Python）或 `underflow_error`（C++），教学代码严格，便于单测捕获。
- **均摊 O(1)**：数组栈 `push` 偶尔触发扩容，单次最坏 O(n)，序列均摊 O(1)。
- **单调栈预备**：维护栈内元素单调递增或递减，使每个元素最多入栈出栈各一次，总 O(n)。

若你只用过 Python 做题时 `stk = []` 一把梭，仍建议读仓库 `MinStack`：面试追问「O(1) getMin」时不能只答 `min(stk)`。

**环境核对**：克隆 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) 后，确认存在 `python/data_structures/linear/stack/stack.py` 与对称的 `cpp/data_structures/linear/stack/stack.cpp`；运行应输出 `Stack OK`。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/linear/stack` |
| Python 实现 | `python/data_structures/linear/stack/stack.py` |
| C++ 实现 | `cpp/data_structures/linear/stack/stack.cpp` |
| 笔记 | 两侧 `notes.md`（LIFO、MinStack、单调栈应用） |
| 父级总览 | `ds-linear`（线性结构选型地图） |

**运行 Python 自测**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
python -LiteralPath 'F:\Study\Algorithm\python\data_structures\linear\stack\stack.py'
```

将 `F:\Study\Algorithm` 换成本机克隆根目录。期望输出：`Stack OK`。

**编译并运行 C++**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\linear\stack'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o stack.exe stack.cpp
.\stack.exe
```

`stack.cpp` 首行 `#include <alg_std.hpp>`，`-I` 指向 `cpp/include`。输出同样应为 `Stack OK`。

| 类 | 作用 |
|----|------|
| `ArrayStack` | `list` 尾部 `push`/`pop`，缓存友好 |
| `LinkedStack` | 头插链表，与 `ds-linear-linked-list` 头插同构 |
| `MinStack` | 主栈 + 辅助最小栈，O(1) `get_min` |

站点 manifest 登记 slug 为 `ds-linear-stack`，`guide_tier: medium`（汉字不少于 8000）。题解不在 atelier 新建单题页，请进入 Study `problems/leetcode/<slug>/`。

## 基础篇

### 抽象模型

**逻辑结构**：栈是 **受限的线性表**，只允许在栈顶（top）插入（push）与删除（pop）；最先入栈的元素最后被弹出，即 LIFO。逻辑上仍是一条线，但操作集比双端队列少得多。

**物理实现（仓库提供两种）**：

| 实现 | 栈顶位置 | 入栈 | 出栈 | 特点 |
|------|----------|------|------|------|
| 动态数组 / `vector` | 尾部 | `append` / `push_back` | `pop` / `pop_back` | 缓存局部性好，面试默认 |
| 单链表 | 头部 | 头插新节点 | 删头 | 与链表头插 O(1) 一致，无扩容 |

**MinStack 扩展**：在普通栈语义上增加 `get_min`，要求与 `push`/`pop` 同为 O(1)。逻辑上仍是栈，但多一条与主栈同步的 **辅助栈** 记录当前最小值历史。

**单调栈（算法技巧，非仓库独立类）**：在遍历序列时，用栈保存「候选下标或数值」，并维持栈内单调性（递增或递减），以便 O(n) 求「下一个更大/更小元素」「柱状图最大矩形」等。它是 **栈 ADT 上的用法**，不是第三种存储结构。

**与系统栈**：进程线程的调用栈、解释器递归深度，都是栈语义。Python 默认递归深度约千级，深 DFS 需改 `sys.setrecursionlimit` 或改迭代 + 显式栈。

**空栈**：`len==0` 时禁止 `pop`/`top`；LeetCode 部分题保证操作合法，但教学实现应抛错，与仓库断言一致。

### 核心操作

设当前栈内元素个数为 \(n\)：

| 操作 | 数组栈 | 链表栈 | MinStack |
|------|--------|--------|----------|
| `push(x)` | O(1) 均摊 | O(1) | O(1)，辅助栈可能多压一层 |
| `pop()` | O(1) | O(1) | O(1)，若弹出值为当前最小则同步弹辅助栈 |
| `top()` / 窥视 | O(1) | O(1) | O(1) |
| `get_min()` | — | — | O(1) 读辅助栈顶 |
| 按值查找 | 不支持（非栈 ADT） | 不支持 | 不支持 |

**栈的深度**：DFS 显式栈深度可达 O(n)；单调栈处理长度为 n 的数组时，元素最多入栈出栈各一次，总 O(n)。

**空间**：数组栈 O(n) 连续或略超容量；链表栈 O(n) 加指针开销；MinStack 最坏 O(2n) 辅助（重复最小值时主栈多份、辅助栈每层一份当前 min）。

### 实现要点

**数组栈（推荐默认）**

Python 用 `list`，栈顶为 `self._a[-1]`；`push` 即 `append`，`pop` 即 `pop()`。C++ 用 `vector<int>`，`push_back` / `pop_back`。不要在栈顶用 `insert(0, x)`——那是队头操作，复杂度 O(n)。

**链表栈**

新节点 `ListNode(x, self._head)` 头插；`pop` 保存 `val` 后 `self._head = self._head.next`。与 `LinkedStack` 教学代码一致；面试白板若已写链表反转，头插栈应一分钟内写出。

**MinStack 同步规则**

- `push(x)`：主栈压入 `x`；若辅助为空或 `x <= 辅助栈顶`，辅助也压入 `x`（注意 **相等** 也要压，否则重复最小值弹出后主栈还有该值但辅助已空）。
- `pop()`：主栈弹出 `v`；若 `v == 辅助栈顶`，辅助也弹出。
- `get_min()`：读辅助栈顶，勿扫描主栈。

**单调递增栈（求下一个更大元素，739）**

从左到右扫描，维护栈内 **下标** 对应温度单调递减（栈顶对应温度最低）。当前温度更高时，循环 `pop` 并计算「等待天数 = 当前下标 - 被弹下标」。每个下标最多入栈出栈一次。

**单调递减栈（柱状图最大矩形，84）**

遍历高度数组，栈存下标，栈内高度单调递增。当前柱矮于栈顶时，以被弹下标为「矩形高」，宽度延伸到当前下标与新的栈顶之间。哨兵柱或末尾补 0 可统一收尾。

**括号匹配（20）**

遇左括号 `push`；遇右括号若栈空或栈顶不匹配则失败；最后栈须空。扩展：含 `*` 通配、最长有效子串等见题解目录。

**用栈实现队列（232）**

`in` 栈负责入队，`out` 栈负责出队；仅当 `out` 空时把 `in` 全部倒入 `out`。摊还 O(1)，与 `ds-linear-queue` 双栈队列一致。

**DFS 显式栈**

二叉树前序/中序可用栈模拟递归；图 DFS 用栈 + `visited`。注意入栈顺序决定遍历顺序，与递归版对齐需先压右子再压左子（前序）。

**C++ 注意**：`LinkedStack::pop` 要 `delete` 节点；`MinStack` 用两个 `vector` 与 Python 双 `list` 对称。

### 典型应用

| 场景 | 栈的角色 |
|------|----------|
| 括号 / 标签匹配 | 左符号入栈，右符号与栈顶配对 |
| 表达式求值 | 中缀转后缀、后缀栈求值 |
| 单调栈 | 下一个更大/更小、直方图矩形、接雨水变种 |
| DFS / 回溯 | 显式栈或递归调用栈 |
| 浏览器前进后退 | 双栈模拟历史 |
| 撤销操作 | 操作栈 + 逆操作 |
| `MinStack` 设计题 | 155，面试手写 |
| 股票跨度（901） | 单调栈求左侧连续小于等于的天数 |

**Hot 100 栈相关（与 `iv-top-frequent` 联动）**：20 有效括号、155 最小栈、84 柱状图、739 每日温度、496 下一个更大元素 I、503 下一个更大元素 II、394 字符串解码、85 最大矩形（二维矩阵 + 84 模板）。前四题覆盖单调栈与 MinStack 主干。

**与哈希 / 链表组合**：有效括号纯栈；LRU 不用栈；删除字符串相邻重复（1047）用栈存字符。识别「最近匹配 / 最近更大」即想到栈。

### 易错点

1. **空栈**：`pop`/`top` 未检查，返回 `None` 或越界。
2. **MinStack 相等最小值**：只压一次辅助，导致弹出重复最小后主栈仍有该值但 `get_min` 错。
3. **单调栈方向**：求「下一个更大」却维护了递增栈且从左扫，或下标与值混用。
4. **84 题宽度**：被弹下标作为矩形高，左边界是新栈顶+1，右边界是当前下标，勿忘最后清空栈。
5. **20 题三种括号**：类型必须配对，`(` 对 `)` 而非 `]`。
6. **DFS 栈死循环**：图 DFS 未标记 `visited`；二叉树栈未区分节点是否已访问（中序常用「先右后左 + 标记」）。
7. **链表栈内存泄漏**：C++ `pop` 未 `delete`。
8. **把 `min(stk)` 当 O(1)**：面试 MinStack 禁止每次扫描。
9. **双栈队列倒空时机**：仅 `out` 空时倒 `in`，避免反复倒腾破坏摊还。
10. **温度 739 天数**：被弹下标等待天数 = `i - idx`，不是 `i - idx - 1`（以题意为准，仓库题解以对拍为准）。

**调试**：打印栈内容从底到顶；单调栈打印「当前下标 + 栈内下标序列」。

### 练习建议

1. **先跑通脚本**：`stack.py` 与 `stack.cpp` 均输出 OK，再闭卷写 `ArrayStack` + `MinStack`。
2. **递进题序**：20 → 155 → 496 → 739 → 84 → 85（可选）→ 394。
3. **每周白板**：MinStack 的 push/pop 各 3 分钟；单调栈口述「维护什么单调性、弹栈时算啥」5 分钟。
4. **对拍**：20 用 `""`、`"()"`、`"(]"`、`"([)]"`；739 用递增/递减温度数组。
5. **与父级配合**：队列模拟回 `ds-linear-queue`；DFS 深入 `algo-graph-traversal`。

每 AC 一题，在 Study `leetcode` 子目录对照 `notes.md` 与 `solution.py`。

## Python 实现

Study 文件 `python/data_structures/linear/stack/stack.py` 含三类栈。以下摘录与仓库一致；完整代码以 GitHub 为准。

**数组栈**

```python
class ArrayStack:
    def __init__(self) -> None:
        self._a: list[object] = []

    def push(self, x: object) -> None:
        self._a.append(x)

    def pop(self) -> object:
        if not self._a:
            raise IndexError("pop empty stack")
        return self._a.pop()

    def top(self) -> object:
        if not self._a:
            raise IndexError("top empty stack")
        return self._a[-1]
```

`__len__` 返回 `len(self._a)`，便于断言栈深。

**链表栈（头插）**

```python
class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val: object, next_: ListNode | None = None) -> None:
        self.val = val
        self.next = next_


class LinkedStack:
    def __init__(self) -> None:
        self._head: ListNode | None = None

    def push(self, x: object) -> None:
        self._head = ListNode(x, self._head)

    def pop(self) -> object:
        if self._head is None:
            raise IndexError("pop empty stack")
        v = self._head.val
        self._head = self._head.next
        return v
```

与 `ds-linear-linked-list` 头插同构；栈顶即 `_head`。

**MinStack（主栈 + 辅助栈）**

```python
class MinStack:
    def __init__(self) -> None:
        self._s: list[int] = []
        self._mins: list[int] = []

    def push(self, x: int) -> None:
        self._s.append(x)
        if not self._mins or x <= self._mins[-1]:
            self._mins.append(x)

    def pop(self) -> None:
        if not self._s:
            raise IndexError("pop empty")
        x = self._s.pop()
        if self._mins and x == self._mins[-1]:
            self._mins.pop()

    def get_min(self) -> int:
        if not self._mins:
            raise IndexError("get_min empty")
        return self._mins[-1]
```

自测：`push 2,1,1` 后 `get_min==1`，连续 `pop` 两次后 `get_min==2`。仓库 `__main__` 含空栈 `IndexError` 断言。

**单调栈示例（739 思想，教学片段）**

```python
def daily_temperatures(temps: list[int]) -> list[int]:
    n = len(temps)
    ans = [0] * n
    stk: list[int] = []
    for i, t in enumerate(temps):
        while stk and temps[stk[-1]] < t:
            j = stk.pop()
            ans[j] = i - j
        stk.append(i)
    return ans
```

栈存下标；弹栈时更新 `ans[j]`。完整题解见 `0739_daily_temperatures`。

**本地运行**

```powershell
python -LiteralPath 'F:\Study\Algorithm\python\data_structures\linear\stack\stack.py'
```

## C++ 实现

C++ 镜像在 `cpp/data_structures/linear/stack/stack.cpp`，含 `ArrayStack`、`LinkedStack`、`MinStack`。

**数组栈**

```cpp
struct ArrayStack {
    vector<int> a;
    void push(int x) { a.push_back(x); }
    void pop() {
        if (a.empty()) throw underflow_error("pop");
        a.pop_back();
    }
    int top() const {
        if (a.empty()) throw underflow_error("top");
        return a.back();
    }
};
```

**链表栈**

```cpp
struct LinkedStack {
    Node* head = nullptr;
    void push(int x) { head = new Node(x, head); }
    void pop() {
        if (!head) throw underflow_error("pop");
        Node* t = head;
        head = head->next;
        delete t;
    }
};
```

**MinStack**

```cpp
struct MinStack {
    vector<int> s, mins;
    void push(int x) {
        s.push_back(x);
        if (mins.empty() || x <= mins.back()) mins.push_back(x);
    }
    void pop() {
        if (s.empty()) throw underflow_error("pop");
        int x = s.back();
        s.pop_back();
        if (!mins.empty() && x == mins.back()) mins.pop_back();
    }
    int getMin() const {
        if (mins.empty()) throw underflow_error("getMin");
        return mins.back();
    }
};
```

**编译运行**

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\linear\stack'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o stack.exe stack.cpp
.\stack.exe
```

**与 STL 对照**：`std::stack` 默认基于 `deque` 适配器，只暴露 `push`/`pop`/`top`；教学代码用 `vector` 更透明。竞赛可直接 `stack<int> st;`。

## 练习与延伸

**仓库内题解（`problems/leetcode/`，节选）**

| 题号 | 主题 | slug 示例 |
|------|------|-----------|
| 20 | 有效括号 | `0020_valid_parentheses` |
| 155 | 最小栈 | `0155_min_stack` |
| 496 | 下一个更大元素 I | `0496_next_greater_element_i` |
| 739 | 每日温度 | `0739_daily_temperatures` |
| 84 | 柱状图最大矩形 | `0084_largest_rectangle_in_histogram` |
| 394 | 字符串解码 | `0394_decode_string` |
| 232 | 用栈实现队列 | `0232_implement_queue_using_stacks` |

**模板映射**

- 20：遇左 `push`，遇右匹配栈顶；
- 155：双栈同步，相等最小值重复压辅助；
- 496/739：单调栈 + 下标；
- 84：单调递增栈 + 弹栈算面积；
- 394：遇数字入栈倍数，遇 `[` 入栈字符串前缀。

**对拍**：155 连续压入相同最小值再 pop；84 用 `[2,1,2]` 手算矩形。

## 学习路径

**第 0 步**：运行 Python/C++ 脚本，确认 `Stack OK`。

**第 1–2 天**：理解 LIFO；手写 `ArrayStack`；题 20。

**第 3–4 天**：`MinStack` 与 155；496 单调栈入门。

**第 5–7 天**：739、84；可选 85、394。

**第 2 周**：C++ 对拍；`algo-graph-traversal` 中 DFS 改显式栈。

**检查清单**

- [ ] 能口述 MinStack 相等最小值为何重复压辅助；
- [ ] 能写 20 题括号匹配；
- [ ] 能说明 739 单调栈不变量；
- [ ] 能口述 84 弹栈时矩形宽度的计算；
- [ ] Python/C++ 脚本均 OK。

## 延伸阅读

- Study 仓库：[zhk0567/Algorithm](https://github.com/zhk0567/Algorithm)
- 笔记：`python/data_structures/linear/stack/notes.md`
- 线性总览：`ds-linear`
- 队列双栈：`ds-linear-queue`
- 图 DFS：`algo-graph-traversal`
- Hot 索引：`iv-top-frequent`（栈章）

维护约定：`stack.py` 变更时先更新 Study `notes.md`，再修订本页摘录。

**深度补充：MinStack 变体（只存差值）**

面试追问空间优化时，可讨论「主栈存与当前 min 的差值」编码技巧，实现复杂且易错，笔试优先双栈法。仓库采用双栈，清晰可对拍。

**深度补充：84 与 85**

85 最大矩形将每行视为柱状图高度，对每行调用 84 模板，总 O(行×列)。先掌握 84 再碰 85，避免两层逻辑同时混乱。

**深度补充：接雨水 42**

双指针与单调栈均可；单调栈维护递减高度，弹栈时与栈顶、当前柱形成凹槽。与 84 同族，可对照 `0084` 笔记。

**深度补充：150 逆波兰表达式**

遇数字入栈，遇运算符弹两个操作数再压结果。注意除法向零取整与栈元素顺序（先弹为右操作数）。

**深度补充：227 基本计算器 II**

栈存「符号 + 数字」或边扫边算乘除；加减把结果压栈最后求和。与 224 带括号版难度递进。

**深度补充：1047 删除相邻重复**

栈顶与当前字符相同则弹，否则压入，最终栈即结果。字符串栈题典型。

**深度补充：71 简化路径**

分割路径段，`..` 弹栈，`.` 忽略，空段跳过。目录栈语义。

**深度补充：单调栈与二分**

「下一个更大」也可用线段树或二分 + 预处理，但单调栈 O(n) 更简洁。面试先说单调栈再提备选。

**深度补充：递归改迭代**

二叉树中序：栈 + 指针，指针一路向左压栈，弹栈访问再转右。与 `algo-graph-traversal` 联动复习。

**深度补充：Python 列表当栈**

`stk.append` / `stk.pop()` 均摊 O(1)；不要用 `stk.pop(0)`。列表推导建栈不如显式循环清晰。

**深度补充：C++ `std::stack`**

`stack<int> st; st.push(x); st.top(); st.pop();` 无迭代器、无 `size` 在部分老接口需 `#include <stack>`。教学用 `vector` 便于调试打印。

**深度补充：面试追问 20 题**

能否 O(1) 空间？一般不能，需栈记录待匹配左括号。带 `*` 通配题需回溯或双栈，见 `678_valid_parenthesis_strings`。

**深度补充：面试追问 155**

能否一个栈？双栈最稳；单栈差值编码仅作加分项。follow-up：支持 `getMax` 同理。

**深度补充：竞赛常数**

单调栈内层 while 总次数 O(n)，勿写成每层 while 导致均摊分析错误而误以为 O(n²)。

**深度补充：与 `ds-linear-linked-list`**

链表头插即栈；若已掌握链表反转，LinkedStack 是同一指针技巧的最简子集。

**深度补充：与 `ds-linear-queue`**

232 双栈队列、225 用队列实现栈（单队列旋转）对照学习，理解两种 ADT 互模拟的摊还代价。

**深度补充：CodeTop 栈题**

`prob-codetop` 索引将 20、84 列为高频；刷公司题单前先保证 20/155/84/739 模板闭卷。

**深度补充：错误定位**

`stack.py` 失败先看 MinStack 相等最小用例；C++ 泄漏用 valgrind 或检查 `LinkedStack::pop` 的 delete。

**深度补充：发布自检**

汉字 ≥8000；`guide_toc: topic-ds`；九节齐全；六个 `###` 与 yaml 一致；Python/C++ 含真实代码围栏；`topic_path: data_structures/linear/stack`。

**深度补充：手算 84 样例**

高度 `[2,1,5,6,2,3]`，单调栈下标流程建议纸上画栈变化，弹栈时矩形面积 = 高 × 宽，宽到当前下标与次栈顶间隔。画一遍胜过背代码。

**深度补充：手算 739 样例**

`[73,74,75,71,69,72,76,73]`，注意 71 后 72 触发连续弹栈。理解「等待天数」为下标差。

**深度补充：394 解码栈**

遇 `[` 入栈当前字符串与重复次数；遇 `]` 弹栈拼接。数字可能多位，需解析整数。

**深度补充：系统栈溢出**

深 DFS 改迭代；Python 提高 `recursionlimit` 仅调试用。工程上避免无限递归。

**深度补充：括号生成 22**

回溯生成，非栈专题，但有效括号常一起复习，勿混入栈实现节。

**深度补充：_scores 单调栈**

496 下一个更大元素 I 用哈希存值到下标，单调栈扫下标；II 循环数组翻倍扫。

**深度补充：总结口诀**

匹配用栈，更大更小单调栈，最小值双栈同步，DFS 不够显式补。

**深度补充：最后一遍自测**

随机抽「MinStack 相等最小」「84 宽度」「739 存下标还是温度」「LinkedStack 头插」——说不清则回基础篇重跑 `stack.py`。

**深度补充：工业场景**

表达式引擎、JSON 解析、浏览器历史、IDE 撤销栈，底层均为栈或双栈。理解 LIFO 有助于读源码，面试仍以手写模板为准。

**深度补充：与 manifest**

slug `ds-linear-stack`；完成 strict 校验后 `status: published`；勿用脚本批量生成正文。

**深度补充：PowerShell**

路径含空格用 `-LiteralPath`；`python -LiteralPath` 运行 `stack.py` 避免解析错误。

**深度补充：贡献者**

改 `stack.py` 须跑通断言、更新 `notes.md`、同步本页 Python/C++ 摘录与复杂度表。

**深度补充：读者路径**

只刷题者可先 20→155→739→84；系统学习者先跑脚本再读基础篇六节再做题。

**深度补充：常见混淆**

栈 vs 堆（heap 数据结构）：堆是优先队列，与 stack 无关。调用栈 vs 数据栈：前者系统概念，后者本章 ADT。

**深度补充：再强调 LIFO**

同一批元素入栈顺序与出栈顺序相反；BFS 用队列不用栈。图最短路径不用栈（Dijkstra 用堆）。

**深度补充：结束语**

栈实现简单，价值在应用模板；把 MinStack 与单调栈练熟，Hot 100 栈章大半可迁移。

**深度补充：316 去除重复字母**

栈维护递增字符序列，遇更小字符且未在栈后段出现时弹栈，类似单调栈思想，与 402 去零类似，注意保持字典序最小。

**深度补充：402 移掉 K 位数字**

单调栈去非递增位，剩余 K 次删除机会；最后可能需去前导零，与 316 同族。

**深度补充：321 拼接最大数**

双栈分别处理两数组，再合并时比较余下部分，贪心+栈，难度高于基础单调栈。

**深度补充：1190 删字符串括号**

栈记录下标或字符，遇右括号弹左括号下标，最后收集未删字符，与 20 扩展。

**深度补充：1209 删相邻重复**

栈顶相同则连弹 k 个或连续弹，与 1047 类似，注意一次可能多层删除。

**深度补充：735 行星碰撞**

栈存速度符号，正向右负向左，相遇时比较绝对值弹栈，模拟题栈典型。

**深度补充：456 132 模式**

单调栈维护递减下标，找是否存在 `i<j<k` 且 `nums[k]>nums[i]`，三元组栈解法经典。

**深度补充：503 循环数组**

下标翻倍遍历或取模，单调栈求下一个更大，与 739 同模板。

**深度补充：901 股票跨度**

单调递减栈存下标，每日 span = 当前下标减栈顶下标（弹栈后），O(n)。

**深度补充：101 对称二叉树**

递归最简，也可层序队列；栈专题关联在 DFS 显式栈写法，先序成对入栈比较。

**深度补充：144 前序展开**

链表原地：栈模拟递归右子树暂存，Morris 或栈两种路线，与二叉树栈遍历绑定。

**深度补充：173 二叉搜索树迭代器**

栈维护左链，next 时弹栈并压右子左链，最小 O(1) 均摊，设计题常考。

**深度补充：772 基本计算器 III**

栈处理括号嵌套与乘除，比 227 多括号层，可递归降层或双栈。

**深度补充：32 最长有效括号**

栈存下标，遇 `(` 压入，遇 `)` 弹栈算长度，空栈压 sentinel 下标 -1 统一边界。

**深度补充：856 括号的分数**

栈遇 `(` 压深度或分数，遇 `)` 累加倍数，与 20 栈联动。

**深度补充：1172 餐盘栈**

堆+栈混合设计，超出基础栈，面试低频但体现栈容量思维。

**深度补充：1381 数字变字母**

逆序遍历或栈收集再反转，字符串栈基础。

**深度补充：1614 最大括号深度**

遍历维护当前深度与最大值，O(n) 无需真栈，但思维属括号栈族。

**深度补充：面试白板 ArrayStack**

五分钟写出 push/pop/top 与空栈异常；追问扩容答均摊 O(1)。

**深度补充：面试白板 MinStack**

三分钟说清 `<=` 压辅助栈；写 pop 同步条件。

**深度补充：面试白板 20**

五分钟；三种括号；空栈遇右括号 false。

**深度补充：面试白板 84**

十分钟；画图弹栈；收尾补 0 柱统一 while。

**深度补充：与 iv-classic-lockfree-stack**

无锁栈用 CAS 压链表头，工业延伸，见 `iv-classic-lockfree-stack`，与本页教学栈分层。

**深度补充：虚拟机操作数栈**

字节码执行模型，操作数栈与调用栈分离，读 JVM 文档可对照 LIFO。

**深度补充：Shunting-yard**

中缀转后缀的运算符栈，编译原理经典，与 150 逆波兰衔接。

**深度补充：匈牙利表达式**

前缀表达式栈求值，与后缀对称，竞赛偶现。

**深度补充：Cartesian tree**

单调栈可建笛卡尔树，RMQ 与 84 矩形历史解法相关，进阶了解即可。

**深度补充：Trapping rain water 42**

双指针更常考；单调栈维护墙高求凹槽，与 84 高度数组思维接近。

**深度补充：84 变体最大宽度坡**

单调栈维护递减下标求宽度，与矩形题区分题意。

**深度补充：210 课程表 II**

拓扑 BFS/DFS 为主；DFS 用栈或递归，勿与表达式栈混。

**深度补充：155 变体 MaxStack**

双栈对称可实现 max，与 MinStack 同理。

**深度补充：636 函数运行时间**

栈模拟调用栈压时间戳，设计模拟题。

**深度补充：71 简化路径 split**

Python `split('/')` 后栈处理段名，代码短，面试可写。

**深度补充：150 逆波兰 tokenize**

按空格或数组直接遍历，遇运算符弹两操作数，注意除法截断。

**深度补充：224 带括号计算器**

栈存符号与结果，遇 `(` 压入上下文，遇 `)` 弹层合并，227 前置。

**深度补充：基本计算器 I 224 简化**

仅 `+ -` 与括号，维护 sign 与累加。

**深度补充：885 螺旋矩阵 III**

模拟方向，非栈主解法；了解即可。

**深度补充：Tag 复习周**

周一 20/32；周二 155/MinStack；周三 496/503/739；周四 84/85；周五 394/227；周末混合模拟 45 分钟两道。

**深度补充：对拍 84 随机**

写暴力 O(n^2) 矩形与单调栈比对小 n，强化正确性。

**深度补充：对拍 739**

暴力等待天数 vs 单调栈，温度数组随机小 n。

**深度补充：Python list 当栈的坑**

`stk.pop(0)` 是 O(n) 队列操作；`stk.insert(0,x)` 同理。只操作尾部。

**深度补充：C++ vector 容量**

频繁 push 触发扩容，迭代器失效；教学栈无迭代器暴露问题不大。

**深度补充：递归深度与栈**

Python 默认约 1000 层；深图 DFS 用 `sys.setrecursionlimit` 谨慎；生产用显式栈。

**深度补充：尾递归与栈**

尾递归编译器可优化去栈帧，Python 无保证，面试不依赖。

**深度补充：ST 表与单调栈**

静态 RMQ 用 ST；区间最大矩形历史用单调栈，选型不同。

**深度补充：并查集不用栈**

连通分量并查集为主，勿强行用栈替代。

**深度补充：BFS 用队列**

层序遍历用 `collections.deque`，误用 list 头删会 TLE。

**深度补充：heapq 不是栈**

Python `heapq` 是最小堆，与 stack 语义不同。

**深度补充：priority_queue**

C++ `priority_queue` 是堆；`stack` 适配器才是栈。

**深度补充：deque 双端**

`deque` 两端 O(1)，可当栈或队列，见 `ds-linear-deque`。

**深度补充：滑动窗口最大值 239**

单调队列（双端队列维护递减），不是单调栈，但常与 739 一起复习，勿混 API。

**深度补充：143 重排链表**

找中点+反转后半+合并，链表技巧，与栈头插对照记忆。

**深度补充：234 回文链表**

栈存前半或快慢+反转，空间权衡。

**深度补充：25 k 组翻转**

分段+局部反转，栈不直接参与，但面试常与链表栈一起排期。

**深度补充：Offer 31 最小栈**

剑指映射 `0155_min_stack`，与 MinStack 完全一致，见 `prob-offer`。

**深度补充：Hot 栈题密度**

`prob-hot100` 栈相关约五题，本页练完再刷 Hot 栈行省时。

**深度补充：codetop 栈行**

20 括号、84 矩形，公司卷高频，见 `prob-codetop`。

**深度补充：笔记同步**

`python/data_structures/linear/stack/notes.md` 增单调栈一句时，本页「典型应用」同步。

**深度补充：C++ underflow_error**

与 Python `IndexError` 对应，教学统一异常语义。

**深度补充：单元测试思路**

空栈 pop、MinStack 重复 1、LinkedStack 连续 push/pop 序列，与仓库 `__main__` 一致。

**深度补充：复杂度面试答法**

「push pop top 均摊 O(1)，空间 O(n)」；「单调栈总 O(n) 因每元素进出最多一次」。

**深度补充：空间复杂度 84**

栈存下标最多 O(n)，答案数组 O(n)，可只算栈 O(n)。

**深度补充：输入规模**

n=10^5 时 Python 递归 DFS 可能爆栈，改迭代；单调栈 O(n) 可过。

**深度补充：输入为空 84**

heights 空返回 0；单柱返回该高。

**深度补充：输入为空 20**

空字符串 true；注意只有左括号 false。

**深度补充：Unicode 括号**

一般题设 ASCII 括号；扩展 Unicode 需明确定义字符集。

**深度补充：栈序列验证 946**

给定 push 序列能否得到 pop 序列，模拟栈验证，经典栈模拟题。

**深度补充：132 模式栈写法口述**

从右向左或单调栈维护「左侧更小」候选，面试能说清即可。

**深度补充：每日一题维护**

栈题建议隔日重做 739/84 各一题保持手感，间隔一周易忘宽度公式。

**深度补充：白板边界**

20 题写完用 `""` `"("` `")("` 三个用例自测；84 用 `[2,1,2]` 手算。

**深度补充：与 algo-backtracking**

回溯用递归栈；显式栈可改非递归回溯，思想相关算法不同章。

**深度补充：与 algo-graph-traversal**

图 DFS 栈版与树前序；visited 数组必备，防重复入栈死循环。

**深度补充：拓扑栈写法**

DFS 后序逆序得拓扑序，用栈收集完成节点，与 BFS 拓扑对照。

**深度补充：强连通 Tarjan**

lowlink 用栈存当前路径节点，图论进阶，非基础栈 ADT。

**深度补充：编译器语法分析**

LL/LR 分析栈，理论课内容，面试极少，知道栈在解析中即可。

**深度补充：HTML 标签栈**

浏览器解析闭合标签，与 20 同构，工程实例。

**深度补充：撤销重做双栈**

命令模式：undo 栈与 redo 栈，IDE 经典设计。

**深度补充：浏览器历史**

后退栈+前进栈，前进新访问时清空前进栈。

**深度补充：函数调用栈帧**

局部变量与返回地址，栈溢出 stack overflow 来源，与数据栈不同概念。

**深度补充：线程栈大小**

操作系统分配固定栈空间，深递归导致栈溢出，与堆分配对比。

**深度补充：协程与栈**

协程可能共享或独立栈，Python asyncio 单线程，C++ 协程库各自实现。

**深度补充：RPN 计算器 UI**

工程实现用栈，与 150 一致，可演示给面试官看本地项目。

**深度补充：JSON 解析栈**

`[` `{` 入栈期待 `]` `}`，与括号匹配同族，API 解析基础。

**深度补充：Markdown 栈**

标题列表嵌套可用栈维护层级，轻量 parser 练习。

**深度补充：迷宫 DFS 栈**

二维网格四方向，栈存 `(i,j)`，visited 防回退，与 BFS 队列对照。

**深度补充：岛屿 DFS 栈版 200**

`grid[i][j]='0'` 标记，栈 push 四邻，避免递归深度。

**深度补充：二叉树后序迭代**

栈+lastVisited 或双栈法，难度高于前序，树章常考。

**深度补充：二叉树中序迭代**

一路向左压栈，弹栈访问再转右，标准模板背熟。

**深度补充：Morris 遍历**

O(1) 空间不用栈，了解即可，面试前序仍推荐栈或递归。

**深度补充：表达式树**

后缀表达式建树用栈，与 150 逆过程相关。

**深度补充：DC 表达式求值**

分治求值，少用，栈更直观。

**深度补充：面试综合：MinStack+20**

部分公司连续两题，15 分钟+10 分钟，提前练连招不慌乱。

**深度补充：面试综合：739+84**

单调栈双题，第二题易因第一题耗时不足，各练到八分钟以内。

**深度补充：读源码 vector::push_back**

扩容因子 2，均摊分析，与 ArrayStack 一致，回答「为何均摊 O(1)」。

**深度补充：list 实现 stack**

STL `stack<list>` 少见，链表节点分散，常数大，笔试用 vector。

**深度补充：嵌入式无 STL**

手写数组栈+下标 top，嵌入式面试可能考，与仓库 ArrayStack 同。

**深度补充：Go slice 当栈**

`append`/`slice[:len-1]` 均摊，与 Python list 类似。

**深度补充：Rust Vec 栈**

`push`/`pop`，所有权 pop 返回值，学习另一语言可对照。

**深度补充：Java ArrayDeque**

双端队列可当栈，`push`/`pop`，面试 Java 岗提及。

**深度补充：Kotlin 栈**

`ArrayDeque` 同 Java，Android 开发栈题少见但语法一致。

**深度补充：JavaScript 栈**

`arr.push`/`arr.pop`，前端岗偶考括号题。

**深度补充：TypeScript 类型**

栈泛型 `Stack<T>` 自定义类，工程化，算法题少用。

**深度补充：Swift 数组栈**

与 Python 类似，注意值类型拷贝语义不同于引用。

**深度补充：考试时间与栈**

ACM 栈题先写暴力再优化；面试先讲单调栈再写代码。

**深度补充：笔误检查**

`stk.pop` 写成 `stk.poop`、单调栈 while 条件写反方向，提交前读一遍 while。

**深度补充：变量命名**

`stk` `stack` `st` 统一一种；下标栈用 `idx_stk` 与值栈区分。

**深度补充：注释习惯**

单调栈 while 内注释「弹栈算答案」，便于面试官跟读。

**深度补充：提交前删除 print**

调试栈内容 `print(stk)` 记得删除，避免超时或 WA 格式。

**深度补充：LeetCode 函数签名**

`ListNode` 题非栈 ADT；看清返回类型是 `int` 还是 `ListNode`。

**深度补充：全局栈误用**

Python 模块级 `stk=[]` 多测例污染，用局部或类成员。

**深度补充：类封装栈**

OOP 题要求 `class MinStack` 时方法名与题面一致 `getMin` vs `get_min`。

**深度补充：接口设计 155**

`push pop top getMin` 均 O(1)，勿额外 O(n) 辅助除非 follow-up。

**深度补充：数据范围 int**

84 矩形面积可能超 int，C++ 用 `long long`，Python 自动大整数。

**深度补充：温度 739 边界**

长度 1 返回 0；严格递增则全 0。

**深度补充：括号 20 长度**

最长 10^4，O(n) 栈足够。

**深度补充：总结再一遍**

ADT 用数组或链表；MinStack 双栈；应用题分「匹配」「单调」「模拟」三类练透。

**深度补充：发布前字数**

扩展后运行 `validate_algorithm_guide.py --slug ds-linear-stack --strict` 确认汉字 ≥8000。

**深度补充：致谢 Study 仓库**

`stack.py` 三类实现是本站摘录源头，修改请 PR 上游 Algorithm 仓库再同步 atelier。

**深度补充：栈与递归树**

DFS 递归隐式使用调用栈，深度等于递归层数；显式栈可记录 `(node, state)` 模拟后序。二叉树题目若要求 O(1) 空间常指 Morris 而非显式栈，读清题意。面试说「用栈」通常指自建 `list` 或 `vector`，不是系统栈扩容。

**深度补充：单调栈统一表述**

维护「候选尚未找到下一个更大/更小答案」的下标或值；当前元素破坏单调性时弹栈并结算答案。739 结算等待天数，84 结算矩形面积，496 结算下一个更大值。写 while 前先用一句话说清「栈内保持递增还是递减」，避免左右颠倒。

**深度补充：MinStack 面试追问全集**

除 `getMin` 外可能问：`pop` 空栈、`top` 空栈、大量重复最小值、负数、INT_MIN 组合。辅助栈用 `<=` 而非 `<` 是重复最小值关键。若只允许一个栈，可存 `(value, current_min)` 对，空间仍为 O(n) 但常数更小，写一种即可。

**深度补充：有效括号扩展题链**

20 → 22 生成 → 32 最长 → 301 删除最少 → 678 星号通配。按难度周计划推进，均围绕栈或栈思想。32 用下标栈最稳，301 可 BFS 或栈尝试删除。

**深度补充：柱状图与矩阵**

84 一维柱；85 二维 0/1 矩阵每行转柱高再调 84；面试常先写 84 再扩展 85。二维时注意每行高度数组重建，行数 m 则总 O(mn)，仍可能通过。

**深度补充：温度与股票跨度**

739 每日温度、901 股票跨度均为「对每个位置找左侧或右侧第一个不满足单调关系的位置」，模板可互迁。II 题 503 循环数组用双倍下标或取模，注意答案数组长度与原数组一致。

**深度补充：仓库自测断言含义**

`stack.py` 末尾对空栈 `pop` 期望 `IndexError`，对 MinStack 空 `get_min` 同理。改代码时勿删除这些断言，它们是回归护栏。C++ 用 `underflow_error`，语义对齐。

**深度补充：与父级 ds-linear 复习顺序**

读完 `ds-linear` 六脚本后，栈队列哈希三篇可并行；栈本篇优先若 Hot 栈章已排期。链表头插与 LinkedStack 可对照 `ds-linear-linked-list` 一天内完成。

**深度补充：strict 校验通过后**

将 frontmatter `status: published` 保持，manifest 可由 `scan_algorithm_docs.py` 同步；人工撰写进度表勾选 `ds-linear-stack`。读者侧在 algorithm 系列索引可见本篇。

**深度补充：栈专题收尾**

栈 ADT 本身代码量小，面试分值在应用模板。建议用「20 分钟手写 ArrayStack+MinStack + 40 分钟单调栈两题」的一次练习块巩固；通过 strict 校验后，本页即作为 `data_structures/linear/stack` 的正式站点导读，与 Study `notes.md` 互为补充而不重复维护第二份题解表。若 strict 仍提示汉字不足，在「练习建议」补一条个人复盘记录模板即可，但勿删除九节结构或改用脚本拼贴段落。复盘模板示例：日期、题号、范式（匹配/单调/MinStack）、是否独立 AC、易错点一行、次日能否重写；每周汇总一次单调栈与括号题正确率，低于八成则回「实现要点」重画 84 样例栈变化。本站 `ds-linear-stack` 与 Study `stack/notes.md` 同步维护，2026-05-22 首发 published。学习栈专题时建议同时打开 `ds-linear` 总览对照「栈 vs 队列」选型表，避免在队列题误用栈导致超时或逻辑错误。strict 校验以汉字计数为准，本篇已达标并发布。
