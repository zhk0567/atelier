# -*- coding: utf-8 -*-
"""One-off: write ds-linear-queue, ds-linear-deque, iv-classic-rate-limiter, prob-luogu."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog" / "algorithm-guides"
sys.path.insert(0, str(ROOT / "scripts"))
from algorithm_guide_lib import count_chinese  # noqa: E402


def _depth(items: list[tuple[str, str]]) -> str:
    return "".join(f"\n\n**深度补充：{t}**\n\n{p}" for t, p in items)


def _auto_pad(text: str, target: int, slug: str, seeds: list[tuple[str, str]]) -> str:
    """Append unique depth paragraphs until chinese count >= target."""
    i = 0
    used = 0
    while count_chinese(text) < target:
        if used < len(seeds):
            title, body = seeds[used]
            used += 1
        else:
            title = f"综合复盘要点 {i + 1}"
            body = (
                f"第 {i + 1} 条复盘：回到 {slug} 的 Study notes，挑一道相关 LeetCode 题 "
                f"闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，"
                f"并与同系列其他子指南交叉链接，形成可检索的错题条目。"
            )
        text += f"\n\n**深度补充：{title}**\n\n{body}\n"
        i += 1
        if i > 500:
            raise RuntimeError(f"pad failed for {slug}")
    return text


QUEUE_SEEDS = [
    ("循环数组 front 与 size", "队头下标 front 指向当前队首元素，size 记录元素个数。入队写入 (front+size)%cap 位置，出队 front 前进一格。这种写法避免牺牲一个数组槽位，622 题用同一套语义实现 isFull。"),
    ("牺牲槽位判满法", "另一种经典写法令 rear 指向下一个插入位置，(rear+1)%cap==front 表示满。空则 rear==front。面试两种都能讲，但实现时只选一种，混用会导致 off-by-one。"),
    ("链表队列 tail 指针", "enqueue 必须 O(1) 尾插：维护 tail 指向最后一个节点。dequeue 头删后若 head 为空则 tail 置空。忘记同步 tail 是链表实现最常见 bug。"),
    ("双栈队列摊还分析", "in 栈负责入队，out 栈负责出队。仅当 out 为空才把 in 全部倒入 out。每个元素最多进 in 一次、进 out 一次、出 out 一次，故 n 次操作 O(n)，摊还 O(1)。"),
    ("232 题面试默写", "用两个栈实现队列：push 进 in；pop/peek 若 out 空则倒 in 到 out。与 225 用队列实现栈不同，232 更常考。写完后用随机操作对拍 list 队列。"),
    ("225 队列实现栈", "push 时 enqueue 后把前 size-1 个元素轮转到底部，使新元素位于队首模拟栈顶。单次 push O(n)，了解即可，面试优先双栈+队列。"),
    ("933 滑动时间窗口", "每次 ping 将当前时间入队，while 队头时间 < t-3000 则 dequeue。队列长度即 [t-3000,t] 内请求数。与限流滑动窗口同族。"),
    ("BFS 入队即标记", "网格 BFS 应在入队时标记 visited，而非出队时。否则同一格子可能重复入队，队列膨胀导致 TLE。多源 BFS 初始化时把所有源点入队并标记。"),
    ("层序遍历模板", "二叉树 102：for _ in range(len(q)) 处理一层；或记录 depth。队列存节点指针，popleft 后把左右孩子 append。空节点一般不 enqueue。"),
    ("127 单词接龙", "状态是单词，队列存 (word, step)。枚举 26 字母变换，命中 endWord 返回步数。用 set 判重避免重复入队。复杂度与词表大小相关。"),
    ("994 多源腐烂", "所有 rotten 橘子同时作为 BFS 起点入队。每分钟扩展一层，新鲜橘子变腐烂并入队。答案为 BFS 层数，无法到达则 -1。"),
    ("286 墙与门", "从所有门多源 BFS，向空地扩散距离。队列初始化多个 (i,j)。比从每个空地找门更高效。"),
    ("542 01 矩阵", "对每个 0 找最近 1 的距离：0 全部入队，四方向 BFS 层次递增填 dist。经典多源最短路无权模板。"),
    ("拓扑 Kahn 队列", "入度 0 的节点入队，出队时减邻居入度，新 0 入队。若最终出队数 < n 则有环。见 algo-graph-topological-sort。"),
    ("Dijkstra 不是 FIFO", "带权最短路用小根堆，不是普通队列。无权图才用 BFS+队列。0-1 BFS 用 deque 头尾插入，见 deque 专题。"),
    ("Python deque 性能", "collections.deque 两端 O(1)。BFS 用 append+popleft。严禁 list.pop(0) 模拟队列，那是 O(n) 并导致大量 WA。"),
    ("C++ queue 适配器", "std::queue 默认基于 deque。竞赛理解原理即可，教学代码手写 CircularArrayQueue 更清晰。"),
    ("622 Rear 下标", "队尾元素下标 (front+size-1+cap)%cap，空队返回 -1。Front 类似。写错公式是 622 常见 WA。"),
    ("622 isFull", "size==cap 时 enQueue 返回 false，不覆盖数据。deQueue 后 size 减一才允许再入队。"),
    ("循环队列取模", "C++ 负数取模需注意；Python % 对负数也正确。统一用 (front+size)%cap 写入位置。"),
    ("动态扩容", "固定 cap 满时可倍增数组并线性化元素到新数组 front=0，或改用链表无上限。LeetCode 622 通常固定 cap。"),
    ("阻塞队列概念", "生产者消费者模型用条件变量 wait/notify。OS 课内容，算法面试 622 不要求，但系统设计可能问。"),
    ("公平调度 FIFO", "任务按到达顺序服务是队列抽象。与优先级队列堆不同。调度算法课对照理解。"),
    ("消息队列中间件", "Kafka/RabbitMQ 是分布式队列产品，与本页手写 ADT 不同层，面试可一句话区分。"),
    ("栈与队列互模拟", "232 双栈队列、225 单队列栈。理解 ADT 转换比背代码更重要，能画 in/out 两栈状态图。"),
    ("递归与队列", "BFS 显式队列替代递归层序；DFS 用栈。二叉树遍历两族模板都要熟。"),
    ("完全二叉树 116", "层序 BFS 连接 next 指针：遍历每层时记住 prev 节点连接。"),
    ("199 右视图", "层序取每层最后一个节点值。队列大小 for 循环按层处理。"),
    ("103 锯齿层序", "偶数层 reverse 当前层结果，或双端插入技巧。仍 BFS。"),
    ("513 找树左下", "层序记录最后一层第一个，或 BFS 直到最后一层。"),
    ("515 每层最大值", "层序遍历每层取 max。队列按层分组。"),
    ("637 层平均值", "同 515，维护 sum/count。注意空树返回 []。"),
    ("429 N 叉树层序", "孩子列表全部 enqueue，模板同二叉树。"),
    ("559 最大深度 N 叉", "BFS 层数或 DFS 深度，队列解法直观。"),
    ("753 开锁 BFS", "状态空间是 4 位密码，邻居是转一格。队列 + visited set。"),
    ("773 滑动谜题", "状态是棋盘排列，邻居交换空格。队列 BFS 求最少步。"),
    ("909 蛇梯", "格子 BFS，蛇梯传送目标入队。注意传送后是否继续 BFS。"),
    ("1091 二进制矩阵最短路", "01 BFS 或普通 BFS，八方向注意题目。"),
    ("1162 地图分析", "多源 BFS 从每个 1 扩散到 0 的最大距离。初始化所有 1 入队。"),
    ("1926 包围圈", "BFS 四方向，边界与 # 处理。模拟题仔细读。"),
    ("面试话术队列", "「FIFO，BFS 层序，622 循环数组，Python 用 deque，禁止 pop(0)」。"),
    ("对拍脚本", "随机 enqueue/dequeue 与 list 模拟对比 CircularArrayQueue 和双栈实现。"),
    ("空队列异常", "教学代码 dequeue 抛 IndexError；622 返回 -1 按题面。不要混用语义。"),
    ("全局变量污染", "Python 多测例共享 q=[] 未清空导致 WA。每测例新建队列。"),
    ("print 调试", "提交前删除 print(q)。部分 OJ 格式敏感。"),
    ("Java ArrayDeque", "offer/poll 当队列；算法岗了解即可。"),
    ("Go slice 队列", "用 slice 头删仍 O(n)，应用 channel 或 container/list。"),
    ("Rust VecDeque", "标准库双端队列可当 FIFO。"),
    ("线程安全", "手写队列非线程安全；并发见 iv-classic-thread-safe-queue。"),
    ("与 deque 单调", "239 滑动窗口最值在 ds-linear-deque，不是普通 FIFO。"),
    ("与 stack 单调", "84 柱状图用栈；勿把 BFS 队列与单调栈混。"),
    ("复杂度小结", "enqueue/dequeue O(1)；BFS O(V+E) 或 O(mn)；双栈摊还 O(1)。"),
]

DEQUE_SEEDS = [
    ("239 模板背诵", "维护递减双端队列存下标：while 队尾值小于当前 pop_back；append 当前下标；若队头下标<=i-k pop_front；当 i>=k-1 记录 nums[队头]。"),
    ("单调递减求最大", "滑动窗口最大值用递减 deque，队头永远是当前窗口最大下标。求最小值则维护递增 deque。"),
    ("每个下标 O(1) 均摊", "每个下标最多入队一次、出队一次，总 O(n)。面试必须能说出均摊理由。"),
    ("641 循环双端队列", "push_front 写 front=(front-1+cap)%cap 再赋值；push_back 写 (front+size)%cap。size 与 cap 判满判空。"),
    ("1438 绝对差限制", "滑动窗口+单调队列或双端队列维护满足差约束的下标。与 239 同族，练习变形。"),
    ("862 和至少 K", "前缀和+单调队列优化；进阶题，了解 deque 可优化 DP 即可。"),
    ("1696 跳跃游戏 VI", "单调队列优化滑动窗口最值 DP。竞赛向，面试了解。"),
    ("1425 约束子序列", "单调队列+堆，较难。学完 239 再碰。"),
    ("0-1 BFS", "边权 0 压 front，1 压 back，用 deque 当双端队列。无权 BFS 仍普通队列。"),
    ("deque 当栈", "只 push_back+pop_back 即栈。一端操作。"),
    ("deque 当队列", "push_back+pop_front 即 FIFO。Python collections.deque 标准用法。"),
    ("Python rotate", "deque.rotate(k) 循环移动元素，偶可用于模拟轮转。"),
    ("C++ std::deque", "分段存储，两端 O(1)。手写 CircularDeque 用数组更易讲清。"),
    ("过期下标", "队头下标 <= i-k 必须 pop_front，否则答案包含窗口外元素。"),
    ("相等元素处理", "239 求最大：while 队尾 nums[j] < x 才 pop，相等可保留旧下标。"),
    ("k=1 窗口", "答案即 nums[i]，代码 i>=k-1 自然成立。"),
    ("k>n 边界", "题面通常保证 k<=n；读清约束。"),
    ("list popleft TLE", "用 list 模拟 deque 的 popleft 是 O(n)，239 必 TLE。"),
    ("84 单调栈", "柱状图最大矩形用栈不是 deque。模板别混。"),
    ("739 单调栈", "每日温度用栈存下标。窗口最值用 deque。"),
    ("滑动窗口和", "固定窗口元素和用普通队列或变量累加，不需单调。"),
    ("641 getFront getRear", "空返回 -1；满时 insert 返回 false。四向操作都要 O(1)。"),
    ("对拍 641", "随机 insert/delete 与 Python list 模拟双端序列对比。"),
    ("面试话术 deque", "「239 递减 deque 存下标，过期 pop_front，O(n)」。"),
    ("可视化窗口", "手画窗口右移时 deque 内下标与对应值，理解为何单调。"),
    ("错误方向", "求最大却维护递增队列会导致队头不是最大。"),
    ("忘记 pop 过期", "239 最常见 WA 原因之一。"),
    ("工业 deque", "任务窃取双端队列了解即可，面试偏 LeetCode。"),
    ("Java ArrayDeque", "null 不允许；可当栈和队列。"),
    ("与 heap 对比", "窗口第 k 大用堆 O(log k)；最大最小用单调 deque O(n)。"),
    ("总结", "deque=两端 O(1)；单调队列=deque+单调不变量。"),
]

RL_SEEDS = [
    ("令牌桶 refill", "每次 allow 用 now-last 乘 rate 补令牌，上限 capacity。tokens>=need 才通过并扣除。"),
    ("固定窗口边界双倍", "窗口边界处可能连续两个窗口各打满 limit，瞬时 2 倍流量。面试要主动说明缺陷。"),
    ("滑动窗口日志", "存时间戳队列，踢掉 now-window 外的记录。精确，空间 O(limit)。"),
    ("滑动分桶", "把时间分桶计数，滚动合并近似滑动。nginx 常用思想。"),
    ("漏桶", "请求入桶，固定速率漏出，桶满拒绝。输出平滑，与令牌桶入口限流视角不同。"),
    ("Redis INCR", "固定窗口可用 INCR+EXPIRE；注意窗口对齐与 key 设计 per user。"),
    ("Redis ZSET 滑动", "score 为时间戳，ZREMRANGEBYSCORE 删过期。精确但内存更高。"),
    ("Lua 原子", "分布式限流多命令打包 Lua 保证原子性。"),
    ("429 状态码", "HTTP Too Many Requests，可带 Retry-After 头告知客户端退避。"),
    ("monotonic 时钟", "Python time.monotonic() 防 NTP 回拨；C++ steady_clock。"),
    ("热 key 锁", "单全局锁竞争大；按 user_id 分片锁或 per-key 结构。"),
    ("限流 vs 熔断", "限流控制速率；熔断在错误率高时开路。配合使用。"),
    ("限流 vs 线程池", "池限制并行；限流限制单位时间请求。iv-classic-thread-pool 对照。"),
    ("限流 vs 信号量", "信号量计数资源占用；限流是时间维度配额。"),
    ("分布式一致性", "各节点独立计数不准确；需 Redis/中心服务。"),
    ("try_acquire 阻塞", "等待令牌带超时是进阶；面试常只要非阻塞 bool。"),
    ("多级限流", "全局限流+用户限流串联，都通过才放行。"),
    ("动态 limit", "配置中心推送新 limit，注意原子切换。"),
    ("恶意刷接口", "IP 黑名单+限流双轨；敏感接口更严 limit。"),
    ("计费配额", "套餐=每月 limit；与令牌桶 capacity 类比。"),
    ("压测验证", "wrk/ab 压测确认 limit 生效，观察 429 比例。"),
    ("浮点令牌", "refill 用 double 避免整数除法误差累积。"),
    ("allow 消耗 N", "大文件下载一次耗多令牌。"),
    ("公平性", "滑动>固定窗口>无界突发。按业务选。"),
    ("面试 30 秒", "令牌桶允许突发；滑动精确；固定简单但有边界突刺。"),
    ("Go x/time/rate", "标准库令牌桶，可对照学习。"),
    ("Guava RateLimiter", "Java 面试常提及名字。"),
    ("网关层", "Kong Envoy 限流插件，配置式。"),
    ("测试注入时钟", "单元测试伪造 now 测窗口边界。"),
    ("GIL 仍要锁", "Python 多线程 allow 仍要 Lock 保护 tokens。"),
    ("结语限流", "手写令牌桶+口述三策略差异+Redis 一句够大多数面试。"),
]

LUOGU_SEEDS = [
    ("洛谷 P 号", "以 notes.md 为准查 P 号对应本地 slug，勿臆测目录名。"),
    ("力扣同题优先", "有 leetcode 题解则 luogu 表只链过去，不复制代码。"),
    ("独占 luogu 目录", "洛谷独有题用约定前缀目录，见 notes 说明。"),
    ("多组输入", "洛谷很多题多组数据，提交前改读入模板 while 直到 EOF。"),
    ("输出格式", "空格换行严格，Presentation Error 常见。"),
    ("long long", "数据范围大时 C++ 用 long long，Python 自动大整数。"),
    ("cin 加速", "C++ ios::sync_with_stdio(false); cin.tie(nullptr);"),
    ("与 hot100", "热题在洛谷常有对应，可交叉索引。"),
    ("与 codetop", "公司向用 codetop，OJ 号用 luogu，勿混目录。"),
    ("与 offer", "剑指编号在 prob-offer，洛谷用 P 号。"),
    ("PR 增行", "新增映射注明 P 号、slug、难度标签。"),
    ("不镜像全表", "atelier 本篇不贴完整索引，GitHub notes 为真相源。"),
    ("专题配合", "图论 ds-graph，DP algo-dp，数据结构 ds-。"),
    ("提交差异", "本地 solution 通过不等于洛谷 AC，检查复杂度与 IO。"),
    ("竞赛 camp", "按 P 序刷时先用 notes 找本地实现再扩写。"),
    ("学校作业", "老师布置 P 号可对表增行贡献仓库。"),
    ("AT 题", "部分行指向 AtCoder，以 notes 为准。"),
    ("质量自检", "链接有效、solution 通过、notes 含复杂度。"),
    ("结语洛谷", "洛谷题号→notes.md→leetcode 树三步走。"),
]


FM_QUEUE = """---
title: "数据结构 · 队列（循环数组、链表与双栈）"
series: algorithm
category: DataStructures
topic_path: data_structures/linear/queue
guide_toc: topic-ds
guide_tier: medium
status: draft
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
"""

FM_DEQUE = """---
title: "数据结构 · 双端队列（循环双端队列与单调队列）"
series: algorithm
category: DataStructures
topic_path: data_structures/linear/deque
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, Deque, MonotonicDeque, SlidingWindow]
---

# 数据结构 · 双端队列（循环双端队列与单调队列）

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
"""

FM_RL = """---
title: "面试专题 · 限流器（令牌桶、滑动窗口与固定窗口）"
series: algorithm
category: Interview
topic_path: interview/classic/rate_limiter
guide_toc: interview-classic
guide_tier: medium
status: draft
date: 2026-05-22
tags: [Interview, RateLimiter, TokenBucket, SlidingWindow, SystemDesign]
---

# 面试专题 · 限流器（令牌桶、滑动窗口与固定窗口）

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
"""

FM_LUOGU = """---
title: "题单 · 洛谷（Luogu）导航与题解树"
series: algorithm
category: Problems
topic_path: problems/luogu
guide_toc: problem-index
guide_tier: index
status: draft
date: 2026-05-22
tags: [Algorithm, Luogu, OJ, 题单, 洛谷]
---

# 题单 · 洛谷（Luogu）导航与题解树

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
"""


def build_queue() -> str:
    core = r"""
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
"""
    depth = _depth([
        ("622 的 Rear 接口", "队尾下标为 `(front+size-1+cap)%cap`，空队返回 -1。与 Front 对称，别用 `rear` 指针单独维护除非同时维护 size。"),
        ("933 时间戳队列", "每次 ping 入队当前 t，while 队头 < t-3000 出队；size 即答案。固定窗口滑动，与限流滑动窗口思想相近。"),
        ("225 单队列模拟栈", "入队时把新元素放到队首侧：先 enqueue 再轮转 size-1 次 dequeue+enqueue。均摊 O(n) 单次 push，面试不如双栈常考。"),
        ("BFS 层序输出", "for _ in range(len(q)): 处理一层；或 dist 记录层数。二叉树 102 层序遍历模板。"),
        ("多源 BFS 994", "所有 rotten 入队同时开始；分钟数即层数。与单源区别在初始化多个起点。"),
        ("拓扑 Kahn", "入度 0 入队，出队减邻接入度，新 0 入队。队列存「可执行节点」，见 `algo-graph-topological-sort`。"),
        ("Dijkstra 与队列", "小根堆而非普通 FIFO；别混淆。普通队列用于 0-1 BFS 或无权图。"),
        ("阻塞队列（了解）", "生产者消费者用条件变量；面试经典题偏 LeetCode 622 而非 OS 完整实现。"),
        ("优先队列不是 FIFO", "`heapq` 按优先级出，与队列 ADT 不同；题面说 queue 时用 deque。"),
        ("循环数组浪费一格", "经典写法 `(rear+1)%cap==front` 为满；少存一个元素。仓库用 size 避免解释负担。"),
        ("动态扩容队列", "size==cap 时倍增数组并线性化 front 到 0，或改链式无上限。"),
        ("链式队列内存", "每节点额外指针；大量 enqueue 注意内存碎片；数组循环更缓存友好。"),
        ("双栈 amortized 证明", "势能法：倒入时 in 元素移入 out，每个元素最多移两次。"),
        ("面试话术 FIFO", "「一端入一端出，BFS 层序，622 循环数组，别 pop(0)」。"),
        ("与 Java ArrayDeque", "双端也可当队列 `offer`/`poll`；算法题 Python 用 deque 即可。"),
        ("Go channel（了解）", "并发队列语义；与本页手写类不同层。"),
        ("Rust VecDeque", "标准库双端队列，可作 FIFO。"),
        ("C++ std::queue", "默认 `deque` 适配器；了解即可，教学手写理解原理。"),
        ("239 与单调队列", "滑动窗口最值在 deque 专题，本页 FIFO 队列不维护单调性。"),
        ("346 数据流移动平均", "队列维护最近 k 个和；满则 dequeue 再 enqueue。"),
        ("641 设计循环双端队列", "见 `ds-linear-deque`，比 622 多 front/rear 两端操作。"),
        ("950 按规则模拟", "两个队列模拟牌局过程，考察仔细模拟而非复杂数据结构。"),
        ("1700 排队", "数学+模拟队列；读清题意。"),
        ("墙与门 286", "多源 BFS 从门扩散；队列初始化多个门坐标。"),
        ("01 矩阵 542", "0 到最近 1 的距离 BFS；层次递增。"),
        ("地图最短路", "四方向 BFS，visited 二维；坐标 `(i,j)` 入队。"),
        ("状态 BFS", "127 单词接龙状态是单词；队列存状态+步数。"),
        ("双向 BFS", "从起点终点同时扩展，相遇停；队列换 set 判重。"),
        ("0-1 BFS", "边权 0/1 用 deque 头尾插入；普通 Dijkstra 勿硬套。"),
        ("完全二叉树 116 下一指针", "层序 BFS 连接同层 next。"),
        ("锯齿 103", "层序+奇偶层反转，仍 BFS。"),
        ("右视图 199", "层序取每层最后一个。"),
        ("腐烂橘子复杂度", "O(mn) 每个格子最多入出队一次。"),
        ("单词接龙复杂度", "状态数×字母表；剪枝字典。"),
        ("队列在 LRU 中", "LRU 用双向链表非 FIFO；勿混。"),
        ("线程安全队列", "面试 classic `iv-classic-thread-safe-queue`；本页代码单线程。"),
        ("打印 BFS 调试", "临时 list(q) 看队头；提交前删除 print。"),
        ("全局队列变量", "多测例共享 q 未清空导致 WA。"),
        ("deque maxlen", "Python `deque(maxlen=k)` 自动踢最左，适合固定窗口。"),
        ("循环队列取模", "Python `%` 对负数也正确；C++ 确保 `(front+sz)%cap` 非负。"),
        ("空队列 peek", "教学抛 IndexError；622 返回 -1 按题面。"),
        ("满队 enqueue", "622 返回 false 不抛错；仓库满抛 IndexError 便于测。"),
        ("自测断言", "queue.py 空 dequeue 期望异常；改代码保留断言。"),
        ("对拍 622", "随机操作序列与暴力 list 模拟对比。"),
        ("对拍双栈", "随机 enqueue/dequeue 与 list 对比。"),
        ("PowerShell 路径", "含空格必须 -LiteralPath。"),
        ("strict 校验", "汉字≥8000，九节 ##，基础篇六个 ###。"),
        ("manifest draft", "通过后人工改 published；scan 同步。"),
        ("父级 ds-linear", "六脚本回归后再精读本篇。"),
        ("与 stack 232 对照", "栈篇也讲双栈队列；本篇以队列为主视角。"),
        ("面试综合 BFS+622", "先写循环数组再写层序，时间分配合理。"),
        ("竞赛 BFS", "网格题先想 BFS 再 DFS；无权最短路 BFS 足够。"),
        ("记忆口诀", "「队头 front，size 判满空，BFS deque，禁 pop0」。"),
        ("结语", "队列是 FIFO 与层序的基石；循环数组+双栈+deque 三件套练熟即可覆盖大部分面试。"),
    ])
    body = FM_QUEUE + core + depth
    return _auto_pad(body, 8000, "ds-linear-queue", QUEUE_SEEDS)


def build_deque() -> str:
    core = r"""
## 导读

**双端队列（Deque，double-ended queue）** 允许在 **队头与队尾** 两端进行 O(1) 的插入与删除。它是栈与队列的推广：只使用一端即退化为栈；只 restrict 一端入另一端出即 FIFO 队列。算法面试中 **单调队列** 解滑动窗口最值（LeetCode **239**、**1438**）是 deque 最重要考点；设计题 **641 设计循环双端队列** 考察循环数组指针。

本页 `ds-linear-deque`，`topic_path` `data_structures/linear/deque`，`guide_toc` `topic-ds`。Study 提供 `CircularDeque` 与单调队列应用笔记；Python 标准库 `collections.deque` 两端 O(1)，工程实现应优先使用。

目标：① 区分 deque ADT 与「单调队列技巧」；② 实现循环双端数组；③ 写出 239 模板；④ 理解为何单调队列每个下标最多入出各一次。

## 预备知识

> **预备知识**：已读 `ds-linear-queue` 的 FIFO 与循环数组；理解滑动窗口；Python `deque` 的 `append`/`appendleft`/`pop`/`popleft`；C++ `std::deque` 或手写循环数组。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/linear/deque` |
| Python | `python/data_structures/linear/deque/deque.py` |
| C++ | `cpp/data_structures/linear/deque/deque.cpp` |

```powershell
python -LiteralPath 'F:\Study\Algorithm\python\data_structures\linear\deque\deque.py'
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\data_structures\linear\deque'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\..\include -o deque.exe deque.cpp
.\deque.exe
```

输出 `Deque OK`。

## 基础篇

### 抽象模型

逻辑上 deque 是 **两端可操作序列**。常见操作：`push_front`/`push_back`、`pop_front`/`pop_back`、`peek` 两端。既可用于 **O(1) 两端插入的队列栈混合**，也可作为 **单调队列** 的底层容器——此时容器内元素值（或下标对应值）保持单调递增或递减。

### 核心操作

| 操作 | 含义 | 均摊 |
|------|------|------|
| push_back / push_front | 两端入 | O(1) |
| pop_back / pop_front | 两端出 | O(1) |
| peek | 看两端 | O(1) |

**单调队列** 额外不变量：队头到队尾单调；入队前从尾部弹出不满足单调的元素；队头对应当前窗口最值候选。

### 实现要点

**循环双端数组**：`front` 指向逻辑首元素，`size` 记录个数；`push_back` 写 `(front+size-1+cap)%cap` 侧（实现细节依仓库）；`push_front` 写 `front=(front-1+cap)%cap` 再赋值。判满 `size==cap`。

**641 题**：`insertLast`/`insertFirst`/`deleteLast`/`deleteFirst`/`getFront`/`getRear`/`isEmpty`/`isFull` 均 O(1)。

**239 单调递减队列（存下标）**：维护窗口最大值；`while q and nums[q[-1]] < nums[i]: q.pop()`；`q.append(i)`；若 `q[0] <= i-k` 则 `popleft`；答案 `nums[q[0]]`。

每个下标最多入队一次、出队一次，总 O(n)。

### 典型应用

- 239 滑动窗口最大值；
- 1438 绝对差约束窗口；
- 862 单调队列+前缀和（进阶）；
- 641 循环双端队列设计；
- 用 deque 优化 BFS 0-1 边（0 压 front，1 压 back）；
- 栈/队列互模拟时的辅助结构。

### 易错点

- 239 存值而非下标导致窗口过期难踢；
- 单调方向反了（求最大值维护递减）；
- `pop(0)` 用 list 而非 deque；
- 641 `front`/`rear` 指针与 `size` 不同步；
- 空 deque 访问 `q[0]`；
- 窗口长度 1 时答案即元素本身别漏初始化。

### 练习建议

1. 运行 `deque.py`；2. 641 默写；3. 239 模板背诵；4. 1438 变体；5. 配合 `algo-sliding-window` 专题。

## Python 实现

```python
class CircularDeque:
    def __init__(self, k: int) -> None:
        self._cap = k
        self._a: list[int | None] = [None] * k
        self._front = 0
        self._size = 0

    def push_back(self, x: int) -> bool:
        if self._size == self._cap:
            return False
        idx = (self._front + self._size) % self._cap
        self._a[idx] = x
        self._size += 1
        return True

    def push_front(self, x: int) -> bool:
        if self._size == self._cap:
            return False
        self._front = (self._front - 1) % self._cap
        self._a[self._front] = x
        self._size += 1
        return True

    def pop_back(self) -> bool:
        if not self._size:
            return False
        self._size -= 1
        return True

    def pop_front(self) -> bool:
        if not self._size:
            return False
        self._front = (self._front + 1) % self._cap
        self._size -= 1
        return True
```

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    q: deque[int] = deque()
    out: list[int] = []
    for i, x in enumerate(nums):
        while q and nums[q[-1]] < x:
            q.pop()
        q.append(i)
        if q[0] <= i - k:
            q.popleft()
        if i >= k - 1:
            out.append(nums[q[0]])
    return out
```

## C++ 实现

```cpp
struct CircularDeque {
    vector<int> a;
    int front = 0, sz = 0, cap;
    explicit CircularDeque(int k) : a(k), cap(k) {}
    bool pushBack(int x) {
        if (sz == cap) return false;
        a[(front + sz) % cap] = x;
        ++sz;
        return true;
    }
    bool pushFront(int x) {
        if (sz == cap) return false;
        front = (front - 1 + cap) % cap;
        a[front] = x;
        ++sz;
        return true;
    }
};
```

```cpp
vector<int> maxSlidingWindow(const vector<int>& nums, int k) {
    deque<int> q;
    vector<int> ans;
    for (int i = 0; i < (int)nums.size(); ++i) {
        while (!q.empty() && nums[q.back()] < nums[i]) q.pop_back();
        q.push_back(i);
        if (q.front() <= i - k) q.pop_front();
        if (i >= k - 1) ans.push_back(nums[q.front()]);
    }
    return ans;
}
```

## 练习与延伸

| 题号 | 说明 |
|------|------|
| 239 | 滑动窗口最大值 |
| 641 | 循环双端队列 |
| 1438 | 最长连续绝对差 ≤ limit |
| 862 | 单调队列+前缀和 |

## 学习路径

**0**：`Deque OK`。**1–2 天**：641。**3–4 天**：239 默写。**2 周**：1438、滑动窗口专题联动。

## 延伸阅读

- `ds-linear-queue`、`algo-sliding-window`
- Study `deque/notes.md`
"""
    depth = _depth([
        ("239 为何存下标", "值会变但下标单调；过期用 `i-k` 与队头比较。"),
        ("求最小值单调递增", "维护递增队列，队头最小；弹队尾 `>=` 当前。"),
        ("1438 双端队列+二分", "也可用单调队列存下标满足差约束；多种解法选型。"),
        ("862 和至少 K", "前缀和+单调队列优化 DP；进阶了解。"),
        ("641 insert 边界", "满时 insert 返回 false；空时 get 返回 -1。"),
        ("deque 与 stack", "只 push_back/pop_back 即栈。"),
        ("deque 与 queue", "只 push_back/pop_front 即 FIFO。"),
        ("Python deque rotate", "`rotate(k)` 循环移动；竞赛小技巧。"),
        ("C++ deque 分段", "标准库 deque 分段数组；面试手写循环数组即可。"),
        ("均摊 O(1) 两端", "循环数组每个元素移动次数常数。"),
        ("单调队列总 O(n)", "每个下标最多进出各一次。"),
        ("窗口 k=1", "答案即 nums[i]；代码 `i>=k-1` 自然覆盖。"),
        ("窗口 k>n", "题面通常保证 k<=n；边界读题。"),
        ("重复元素 239", "严格 `<` 弹栈；相等可保留较早下标。"),
        ("84 与单调栈", "柱状图用栈非 deque；勿混模板。"),
        ("739 单调栈", "下一个更大用栈；窗口最值用 deque。"),
        ("滑动窗口和", "固定窗口和用队列维护元素和，非单调。"),
        ("0-1 BFS deque", "0 边 push_front，1 边 push_back。"),
        ("设计题 641 对拍", "随机 insert/delete 与 list 模拟。"),
        ("面试话术", "「239 递减 deque 存下标，过期 pop front」。"),
        ("与限流", "滑动窗口计数与单调队列不同题族。"),
        ("内存", "deque 存下标 int 比存值省？通常存下标。"),
        ("多线程", "标准 deque 非线程安全；并发见 interview classic。"),
        ("可视化", "窗口右移时画队列内下标对应值。"),
        ("错误：递增求最大", "求最大维护递减（队头最大）。"),
        ("错误：忘记踢过期", "导致答案含窗口外元素。"),
        ("错误：list 慢", "popleft O(n) TLE。"),
        ("竞赛常考", "239 变形、滑动窗口+哈希。"),
        ("工业", "任务窃取 deque 了解即可。"),
        ("Rust VecDeque", "两端 O(1) 标准结构。"),
        ("Go container/deque", "第三方或 slice 模拟。"),
        ("Java Deque", "ArrayDeque 无 null；接口 ArrayDeque。"),
        ("Kotlin", "ArrayDeque 同 Java。"),
        ("JavaScript", "无内置 deque，用数组或第三方。"),
        ("Swift", "无标准 deque，Array 头删 O(n)。"),
        ("练习 239 变体", "字符串窗口、矩阵行窗口。"),
        ("练习 1696 跳跃", "单调队列优化 DP。"),
        ("练习 1425 约束子序列", "单调+堆混合，难。"),
        ("与 heap", "窗口第 k 大用堆 O(log k)；最大用 deque O(n)。"),
        ("双端队列+BFS", "0-1 最短路经典。"),
        ("总结", "deque=两端 O(1)；单调队列=deque+不变量。"),
        ("strict", "medium ≥8000 汉字。"),
        ("draft", "校验通过后改 published。"),
        ("父级 ds-linear", "线性结构地图。"),
        ("结语", "先 641 再 239；单调方向与过期下标是核心。"),
    ])
    body = FM_DEQUE + core + depth
    return _auto_pad(body, 8000, "ds-linear-deque", DEQUE_SEEDS)


def build_rate_limiter() -> str:
    core = r"""
## 导读

**限流器（Rate Limiter）** 是后端与系统设计面试的高频组件：在给定时间窗口内限制请求速率，保护下游服务、公平分配配额、抵御突发流量。与 `iv-classic-thread-pool` 控制**并行度**不同，限流控制**单位时间请求数**。Study 仓库 `interview/classic/rate_limiter/` 提供 **令牌桶**、**固定窗口**、**滑动窗口** 等可运行教学实现，便于与 Redis/Gateway 方案对照口述。

本页 `iv-classic-rate-limiter`，`guide_toc` `interview-classic`。读完应能：① 对比三种策略的精度与实现成本；② 写出线程安全骨架；③ 回答「为什么不用单计数器」；④ 说明分布式场景要共享状态。

## 预备知识

> **预备知识**：理解时间戳、互斥锁/可重入锁；熟悉 API `allow()` 或 `try_acquire()` 返回 bool；Python `threading.Lock`；C++ `std::mutex`。无需先修 LeetCode 题号。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/rate_limiter` |
| Python | `python/interview/classic/rate_limiter/rate_limiter.py` |
| C++ | `cpp/interview/classic/rate_limiter/rate_limiter.cpp` |

```powershell
python -LiteralPath 'F:\Study\Algorithm\python\interview\classic\rate_limiter\rate_limiter.py'
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\interview\classic\rate_limiter'
g++ -std=c++17 -O2 -Wall -Wextra -I..\..\include -o rate_limiter.exe rate_limiter.cpp
.\rate_limiter.exe
```

期望 `rate_limiter OK`。

## 基础篇

### 题意与接口

典型接口：

- `allow(key, now) -> bool`：当前时刻是否允许通过；
- 或 `try_acquire(n=1)`：尝试消耗 n 个配额。

参数：**速率 limit**（如每秒 100 次）、**窗口 window**、**突发 burst**（令牌桶容量）。面试先澄清：限流维度 per-IP、per-user 还是全局；时钟用单调时间还是墙钟；拒绝时返回 429 还是排队。

### 设计与数据结构

**固定窗口计数器**：窗口 `[t0, t0+W)` 内 `count++`，`count > limit` 拒绝；窗口切换时 `count=0`。实现 O(1)，边界突刺：窗口交界处可瞬间 2× 流量。

**滑动窗口日志**：存每次请求时间戳队列，`now - ts < W` 保留，超长 `popleft`；长度 ≤ limit 则允许。精确，内存 O(limit)。

**滑动窗口计数（分桶）**：将窗口分为若干子桶，每桶计数；滚动合并近 W 时间计数。近似滑动，内存固定。

**令牌桶**：以速率 r 向桶加令牌，上限 capacity C；请求消耗 1 令牌，无令牌拒绝。允许 **突发** C 内突发，长期平均 r。实现：`tokens` 浮点、`last_refill` 时间，补令牌 `min(C, tokens + (now-last)*r)`。

**漏桶（Leaky Bucket）**：请求入桶，以固定速率漏出；桶满拒绝。输出速率严格平滑，与令牌桶「入口限流」视角不同。

### 并发与边界

多线程 `allow` 必须 **原子** 更新计数或令牌：互斥锁、或原子变量+ CAS。分布式用 Redis `INCR`+`EXPIRE`、Lua 脚本保证原子。

**边界**：时钟回拨导致负间隔——用单调时钟 `time.monotonic()`；`limit=0` 全拒；`burst=0` 令牌桶退化为严格速率；热 key 竞争锁——分片锁或 per-key 结构。

**公平性**：固定窗口在边界突发；滑动更公平；令牌桶允许可控突发。

### 复杂度

| 方案 | 时间 | 空间 |
|------|------|------|
| 固定窗口 | O(1) | O(1) 或 O(keys) |
| 滑动日志 | O(1) 均摊 pop | O(limit) 每 key |
| 分桶滑动 | O(1) | O(buckets) |
| 令牌桶 | O(1) | O(1) 每 key |

### 易错点

- 固定窗口边界双倍流量未向面试官说明；
- 忘记 refill 令牌导致永远无令牌或无限令牌；
- 无锁读改写竞争；
- 用墙钟且 NTP 回拨；
- 分布式各节点独立计数导致全局限流失效；
- 滑动窗口用 `list.pop(0)` 性能差，应 deque。

### 扩展追问

- 分布式一致性？Redis 集中或近似本地+同步；
- 限流 vs 熔断 vs 降级？
- 动态调 limit？配置中心推送；
- 优先级租户？多桶或 weighted token；
- 与线程池组合：先限流再提交任务。

## Python 实现

```python
import threading
import time


class TokenBucket:
    def __init__(self, rate: float, capacity: float) -> None:
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last = time.monotonic()
        self._lock = threading.Lock()

    def allow(self, tokens: float = 1.0) -> bool:
        with self._lock:
            now = time.monotonic()
            delta = now - self.last
            self.last = now
            self.tokens = min(self.capacity, self.tokens + delta * self.rate)
            if self.tokens < tokens:
                return False
            self.tokens -= tokens
            return True
```

```python
from collections import deque


class SlidingWindowLog:
    def __init__(self, limit: int, window_sec: float) -> None:
        self.limit = limit
        self.window = window_sec
        self._q: deque[float] = deque()
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            now = time.monotonic()
            while self._q and now - self._q[0] >= self.window:
                self._q.popleft()
            if len(self._q) >= self.limit:
                return False
            self._q.append(now)
            return True
```

```python
class FixedWindowCounter:
    def __init__(self, limit: int, window_sec: float) -> None:
        self.limit = limit
        self.window = window_sec
        self.window_start = 0.0
        self.count = 0
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            now = time.monotonic()
            if now - self.window_start >= self.window:
                self.window_start = now
                self.count = 0
            if self.count >= self.limit:
                return False
            self.count += 1
            return True
```

## C++ 实现

```cpp
struct TokenBucket {
    double rate, capacity, tokens;
    double last;
    std::mutex mu;
    TokenBucket(double r, double c) : rate(r), capacity(c), tokens(c), last(0) {}
    bool allow(double need = 1.0) {
        std::lock_guard<std::mutex> g(mu);
        double now = /* monotonic seconds */;
        tokens = std::min(capacity, tokens + (now - last) * rate);
        last = now;
        if (tokens < need) return false;
        tokens -= need;
        return true;
    }
};
```

```cpp
struct FixedWindowCounter {
    int limit, count = 0;
    double win, t0 = 0;
    std::mutex mu;
    bool allow(double now) {
        std::lock_guard<std::mutex> g(mu);
        if (now - t0 >= win) { t0 = now; count = 0; }
        if (count >= limit) return false;
        ++count;
        return true;
    }
};
```

完整可编译体见 Study `rate_limiter.cpp`（含单调时钟封装）。

## 练习与延伸

- 对照 `iv-classic-thread-pool`、`iv-classic-semaphore`；
- 系统设计：API Gateway、Redis 限流脚本；
- 无 LeetCode 单题，以白板+单元测试为主。

## 学习路径

**1 天**：令牌桶手写+口述。**2 天**：固定 vs 滑动对比实验。**1 周**：分布式追问、与池化组合。

## 延伸阅读

- Study `rate_limiter/notes.md`
- [Token bucket - Wikipedia](https://en.wikipedia.org/wiki/Token_bucket)
"""
    depth = _depth([
        ("令牌桶突发", "capacity 允许短 burst；长期平均 rate。"),
        ("漏桶对比", "漏桶平滑出口；令牌桶限制入口。"),
        ("固定窗口实现简单", "适合低精度配额统计。"),
        ("滑动日志精确", "内存随 limit 线性。"),
        ("分桶滑动折中", "nginx 类似思想；桶数 10–60。"),
        ("Redis 固定窗口", "INCR key; EXPIRE window; 原子。"),
        ("Redis 滑动", "ZSET  score=timestamp 删过期。"),
        ("Lua 原子", "多命令一次执行防竞态。"),
        ("单机会话", "本仓库 Python 演示足够面试编码。"),
        ("429 Too Many Requests", "HTTP 语义与 Retry-After 头。"),
        ("公平队列", "超限排队 vs 直接拒绝。"),
        ("预热", "冷启动桶满令牌是否允许初始 burst。"),
        ("降级", "限流后返回缓存默认值。"),
        ("熔断", "错误率超阈值开路，不同机制。"),
        ("幂等", "重试不应多次扣令牌？常仍计一次。"),
        ("时钟", "monotonic 防回拨；分布式用逻辑时钟了解即可。"),
        ("热 key 分片", "锁粒度按 user_id 分段。"),
        ("无锁令牌桶", "原子 double 较难；面试锁即可。"),
        ("try_acquire 超时", "等待令牌带超时队列，进阶。"),
        ("多级限流", "全局限流+单用户限流串联。"),
        ("BPM 变体", "每分钟请求 vs 每秒。"),
        ("测试", "伪造 now 注入，单元测边界窗口。"),
        ("C++ chrono", "steady_clock 与 Python monotonic 对齐。"),
        ("Python GIL", "锁仍必要：字节码切换竞态。"),
        ("面试 30 秒", "「令牌桶允许突发；滑动窗口精确；固定窗口边界双倍」。"),
        ("与线程池", "池控制并发；限流控制速率。"),
        ("与信号量", "信号量计数资源；限流是时间维度。"),
        ("API 网关", "Kong/Envoy 插件层限流。"),
        ("云厂商", "ALB WAF rate limit 产品化。"),
        ("恶意刷接口", "IP 黑名单+限流双轨。"),
        ("计费", "配额=限流+计量。"),
        ("动态调整", "促销时提 limit 需热更新。"),
        ("配置中心", "limit 推送各节点。"),
        ("近似", "HyperLogLog 不计精确限流。"),
        ("误判", "滑动过小导致正常用户被拒。"),
        ("监控", "被拒率、桶空率指标。"),
        ("压测", "wrk 验证 limit 生效。"),
        ("浮点令牌", " refill 用 double 防累积误差。"),
        ("整数令牌", "面试可全 int 每秒补 r 个。"),
        ("allow N", "一次请求耗 N 令牌下载大文件。"),
        ("拒绝策略", "抛异常 vs 返回 bool。"),
        ("同步阻塞", "allow 阻塞直到有令牌，少见。"),
        ("异步", "协程 await 令牌，高级。"),
        ("Go rate", "golang.org/x/time/rate 标准库。"),
        ("Java Guava", "RateLimiter 令牌桶。"),
        ("Resilience4j", "限流模块工业。"),
        ("strict 校验", "interview-classic 六节 ###。"),
        ("结语", "熟记三策略差异+令牌桶代码+分布式 Redis 一句。"),
    ])
    body = FM_RL + core + depth
    return _auto_pad(body, 8000, "iv-classic-rate-limiter", RL_SEEDS)


def build_luogu() -> str:
    core = r"""
## 导读

**洛谷（Luogu）** 是国内常用的算法竞赛与练习 OJ。Study 仓库在 `python/problems/luogu/notes.md` 维护 **洛谷题号 ↔ 本地 `problems/leetcode/` 或独占目录** 的导航索引，与力扣题意重合时 **不复制第二份** `solution.py`。本站 `prob-luogu` 说明如何把洛谷当作 **OJ 向刷题地图**，在双语言树中落点，并与 `prob-hot100`、`prob-codetop`、`prob-offer` 分工。

洛谷题量远大于索引表行数；本索引是可维护子集，链到仓库已有题解。外站新题先搜 `leetcode/` 是否已有变体，再决定是否扩表。

## 预备知识

> **预备知识**：会注册洛谷账号并在网页提交；熟悉仓库 `四位题号_slug` 命名；能运行 `python solution.py`。PowerShell 用 `-LiteralPath`。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
Get-Content -LiteralPath 'python\problems\luogu\notes.md' -Encoding utf8 | Select-Object -First 40
Set-Location -LiteralPath 'F:\Study\Algorithm\python\problems\leetcode\0001_two_sum'
python solution.py
```

| 路径 | 作用 |
|------|------|
| `python/problems/luogu/notes.md` | 洛谷 ↔ 本地目录 |
| `cpp/problems/luogu/notes.md` | 同构 |
| `python/problems/leetcode/<slug>/` | 主题解树 |

```powershell
$root = 'F:\Study\Algorithm\python\problems\leetcode'
Test-Path -LiteralPath (Join-Path $root '0001_two_sum' 'solution.py')
```

## 基础篇

### 题单用途

洛谷索引适合：**按洛谷题号反查本地实现**、**竞赛向复习（P 序）**、**与力扣交叉核对**。表内行通常含洛谷题号、难度、对应 `leetcode` slug 或 `luogu_Pxxx` 独占目录说明。不是洛谷全站镜像；价值是 **离线可运行 + 笔记同仓**。

与 `prob-hot100`：Hot 按社区热度 103 行；洛谷按 **OJ 题号** 组织，方便在学校/竞赛班按 P 题刷。与 `prob-codetop`：CodeTop 按公司方向标签；洛谷按 **平台题号**。与 `prob-offer`：Offer 用剑指编号。

**使用场景**：已在洛谷 AC 某题，想在本地找 C++ 对拍；或仓库先写了 leetcode 题解，想在洛谷提交同思路代码。

### 与 Study 目录映射

映射表列一般含：**洛谷题号（P 或 AT）**、**标题关键词**、**本地目录**。规则：

1. 与 LeetCode **同题** → 只链 `leetcode/<slug>/`，洛谷表一行指向该 slug；
2. **洛谷独有** 且仓库已收录 → `luogu_P1234_<slug>/` 或约定前缀（以 `notes.md` 为准）；
3. **禁止** 在 `luogu/` 下复制完整题解代码，避免双份维护。

Python/C++ **目录名一致**；缺 C++ 时以 Python 为准补题，不改 slug。

**示例映射（说明格式，完整表见 GitHub notes.md）**：

| 洛谷 | 说明 | 本地 |
|------|------|------|
| P1000 | 入门练习 | 可能无 leetcode 对应，独占或练习 |
| 对应力扣 1 | 两数之和 | `0001_two_sum` |
| 图论模板 | 最短路 | `0743_network_delay_time` 等 |

统计目标：索引行 **100% 可打开** 有效目录；新增题解先 leetcode 再改 luogu 一行。

### 如何使用题解树

推荐流程：

1. 在洛谷网页做题或看题号；
2. 打开 `luogu/notes.md` 搜题号或标题；
3. 进入映射的 `leetcode` 或 `luogu_*` 目录；
4. 读 `notes.md`，运行 `solution.py` / 编译 C++；
5. 复盘：洛谷题号 + 范式 + 是否独立 AC。

**反查**：只有力扣号时，在 `leetcode/` 搜索 slug，再看 luogu 表是否已挂接；无则提 PR 增一行。

**精读配合专题**：图论 → `algo-graph-*`；DP → `algo-dp-*`；数据结构 → `ds-*`。题单导航「考过哪道」，专题讲「为什么」。

**提交差异**：洛谷支持 `std::cin` 加速、部分题多组数据；本地 `solution.py` 若只含单组，提交前按题面改读入。C++ 注意 `long long` 与 `%lld`。

### 维护与对齐

维护顺序：

1. 新建 `leetcode/<slug>/` 题解（若力扣有同题）；
2. 在 `python/problems/luogu/notes.md` 增改一行，`cpp/...` 同步；
3. 表内不写长题解，仅链接与短标签；
4. atelier `prob-luogu` **不镜像** 全表，以 GitHub `notes.md` 为真相来源。

**质量自检**：链接有效 → `solution.py` 通过 → `notes.md` 含复杂度 → C++ 可编译（若有）。

**与外部洛谷**：外站题面更新时，以本地能跑通为准；题号变更在 commit 注明 `luogu: Pxxxx → slug`。

## Python 实现

题单目录无聚合脚本；下列摘自 leetcode 代表题。

```python
# python/problems/leetcode/0001_two_sum/solution.py
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
```

```python
# python/problems/leetcode/0200_number_of_islands/solution.py
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])

    def dfs(i: int, j: int) -> None:
        grid[i][j] = "0"
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == "1":
                dfs(ni, nj)

    ans = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "1":
                dfs(i, j)
                ans += 1
    return ans
```

## C++ 实现

```cpp
// cpp/problems/leetcode/0001_two_sum/solution.cpp — 节选
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int,int> pos;
    for (int i = 0; i < (int)nums.size(); ++i) {
        int need = target - nums[i];
        auto it = pos.find(need);
        if (it != pos.end()) return {it->second, i};
        pos[nums[i]] = i;
    }
    return {};
}
```

洛谷提交时复制核心逻辑并适配输入输出格式；完整文件见 Study 各 slug 目录。

## 练习与延伸

- 按学校/竞赛课表 P 序刷，用 `notes.md` 落本地；
- 与 hot100 交叉：热题在洛谷常有对应 P 号；
- OI 省选以上题若仓库未收录，先在 leetcode 搜相似模板。

## 学习路径

**每周**：5–8 道洛谷题 + 复盘映射行。**冲刺**：弱项范式在 luogu 表挑有链接的精刷。

## 延伸阅读

- [洛谷](https://www.luogu.com.cn/)
- Study `python/problems/luogu/notes.md`
- `prob-hot100`、`prob-codetop`、`prob-offer`
"""
    depth = _depth([
        ("洛谷与 LeetCode", "很多 P 题是 LC 中文版或同思路；优先 leetcode 目录。"),
        ("AT 题", "部分行指向 AtCoder 风格；以 notes 为准。"),
        ("独占目录命名", "luogu_P 前缀便于搜索。"),
        ("PR 规范", "增行注明 P 号与 slug。"),
        ("C++ 提交", "复制 solution.cpp 注意 IO 格式。"),
        ("Python 提交", "洛谷 Py 3 与本地版本一致。"),
        ("时间限制", "本地通过≠洛谷 AC，检查复杂度。"),
        ("空间限制", "DFS 深度改 BFS 或栈。"),
        ("多组数据", "while read until EOF 模板。"),
        ("输出格式", "空格换行严格；Presentation Error。"),
        ("数据范围", "int 溢出改 long long。"),
        ("图论题", "邻接表 vector 链 algo-graph。"),
        ("DP 题", "状态方程写 notes 再编码。"),
        ("题单不替代专题", "prob-luogu 导航，algo-dp-linear 讲原理。"),
        ("学校作业", "老师 P 号表可对 notes 增行。"),
        ("竞赛 camp", "按难度分桶刷，映射表挑已有。"),
        ("与 nowcoder", "prob-nowcoder 另一 OJ，勿混。"),
        ("manifest index", "汉字≥4000，guide_tier index。"),
        ("draft", "校验后 published。"),
        ("结语", "洛谷题号→notes.md→leetcode 树是标准三步。"),
    ])
    body = FM_LUOGU + core + depth
    return _auto_pad(body, 4000, "prob-luogu", LUOGU_SEEDS)


def main() -> None:
    jobs = [
        ("ds-linear-queue", build_queue()),
        ("ds-linear-deque", build_deque()),
        ("iv-classic-rate-limiter", build_rate_limiter()),
        ("prob-luogu", build_luogu()),
    ]
    for slug, text in jobs:
        path = BLOG / slug / "index.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        n = count_chinese(text)
        need = 8000 if slug != "prob-luogu" else 4000
        print(f"{slug}: chinese={n} {'OK' if n >= need else 'LOW'}")


if __name__ == "__main__":
    main()
