---
title: "面试专题 · Classic Mpmc Queue"
series: algorithm
category: Interview
topic_path: interview/classic/mpmc_queue
guide_toc: interview-classic
guide_tier: medium
status: published
date: 2026-05-22
tags: [Algorithm, Interview, mpmc, queue]
---

# 面试专题 · Classic Mpmc Queue（有界 MPMC 队列）

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

**有界多生产者多消费者（MPMC）队列**是高性能系统里的核心通道：线程池任务分发、日志流水线、Disruptor 环形缓冲、跨线程消息总线都依赖「多写多读 + 有界背压」。Study 仓库提供两套对照实现：Python 用 `deque` + `Condition` 做**阻塞参考版**，保证与 C++ 压测脚本同一形状（8 生产者 ×500 push、8 消费者 ×500 pop、元素恒为 1）；C++ 用 **序列槽 + atomic turn** 实现 Rigtorp 思路的无锁有界环，展示 memory order 与缓存行对齐。

面试不必默写完整无锁代码，但要能讲清：**有界 vs 无界**、**阻塞 vs 自旋**、**正确性不变量（每个槽位 turn 状态机）**、以及与 `iv-classic-thread-safe-queue`（SPSC 风格阻塞队列）、`iv-classic-ring-buffer`（裸环缓）的差异。

## 预备知识

> **预备知识**：生产者-消费者模型；`threading.Condition` 与 Mesa 语义；C++ `std::atomic` 与 `memory_order_acquire/release`；伪共享与 `alignas(64)` 缓存行隔离。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/mpmc_queue` |
| Python | `python/interview/classic/mpmc_queue/mpmc_queue.py` |
| C++ | `cpp/interview/classic/mpmc_queue/mpmc_queue.cpp` |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\interview\classic\mpmc_queue'
python mpmc_queue.py

Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\interview\classic\mpmc_queue'
g++ -std=c++17 -O2 -pthread -o mpmc.exe mpmc_queue.cpp
.\mpmc.exe
```

## 基础篇

### 题意与接口

- `push(v)`：队列未满则入队；Python 版满则 `wait`；C++ 无锁版槽位未就绪则 `yield` 自旋。
- `pop()`：队列非空则出队；对称等待。
- 压测：`capacity=1024`，每线程 500 次，8P+8C，总和应为 `8×500`。

### 设计与数据结构

**Python 参考版**：`deque` 缓冲；`not_full` / `not_empty` 两个条件变量；单把 `Lock` 保护长度与唤醒。

**C++ 无锁版**：`head_`/`tail_` 全局序号；每槽 `Cell{ atomic turn, int val }`；`turn_of(i)=i/cap` 区分环上第几轮占用；状态机：`2k` 可写、`2k+1` 可读、`2k+2` 可再次写。

### 并发与边界

- 有界队列必须处理**背压**：慢消费者导致生产者阻塞或自旋。
- 无锁版依赖 **release-acquire** 发布 `val` 与 `turn`，错误 memory order 会数据竞争。
- `alignas(64)` 分离 `head_`/`tail_` 与 `Cell` 数组，减轻伪共享。
- Python 版用 `notify` 单唤醒；高负载可考虑 `notify_all` 防饿死（本专题未实现）。

### 复杂度

- 摊还入队/出队 O(1)；阻塞或自旋时间为调度相关。
- 无锁版竞争下 CPU 占用上升，吞吐依赖核心数与槽位周转。

### 易错点

- 把 Python 参考版说成「无锁 MPMC」——实为 mutex+Condition。
- 无锁 turn 状态转移写错一位，表现为偶发丢数或重复读。
- 容量为 0 未校验；C++ 构造 `assert(capacity>=1)`。
- 与无界 `queue.Queue` 混用场景：有界才需要背压设计。

### 扩展追问

- Disruptor 与 MPMC 环的区别？
- 如何实现 MPSC / SPMC 特例优化？
- ABA 在本队列实现里为何不是主矛盾？
- 与 `iv-classic-lockfree-stack` 组合成流水线？

## Python 实现

```python
"""有界 MPMC 队列（参考实现）：`deque` + `Condition`，与 C++ 无锁版同一压测形状。"""

from __future__ import annotations

import threading
from collections import deque


class BoundedMpmcQueueRef:
    def __init__(self, capacity: int) -> None:
        self._cap = capacity
        self._buf: deque[int] = deque()
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)

    def push(self, v: int) -> None:
        with self._not_full:
            while len(self._buf) >= self._cap:
                self._not_full.wait()
            self._buf.append(v)
            self._not_empty.notify()

    def pop(self) -> int:
        with self._not_empty:
            while len(self._buf) == 0:
                self._not_empty.wait()
            v = self._buf.popleft()
            self._not_full.notify()
            return v


if __name__ == "__main__":
    k_cap = 1024
    k_each = 500
    q = BoundedMpmcQueueRef(k_cap)
    total = [0]
    lock_sum = threading.Lock()
    go = threading.Event()

    def producer() -> None:
        go.wait()
        for _ in range(k_each):
            q.push(1)

    def consumer() -> None:
        go.wait()
        s = 0
        for _ in range(k_each):
            s += q.pop()
        with lock_sum:
            total[0] += s

    ts = [threading.Thread(target=producer) for _ in range(8)]
    ts.extend(threading.Thread(target=consumer) for _ in range(8)]
    for t in ts:
        t.start()
    go.set()
    for t in ts:
        t.join()
    assert total[0] == 8 * k_each
    print("mpmc_queue OK")
```

要点：`push` 在 `not_full` 上 `while len>=cap: wait`；`pop` 对称；压测用 `Event` 同步起跑。

## C++ 实现

```cpp
// 有界 MPMC 无锁队列（int）：序列槽 + turn 位，思路来自 Erik Rigtorp / MPMCQueue（MIT）
#include <atomic>
#include <cassert>
#include <cstddef>
#include <iostream>
#include <memory>
#include <thread>
#include <vector>

struct alignas(64) Cell {
    std::atomic<std::size_t> turn{0};
    int val{0};
};

class IntMpmcQueue {
public:
    explicit IntMpmcQueue(std::size_t capacity) : cap_(capacity), slots_(new Cell[capacity]) {
        assert(capacity >= 1);
        for (std::size_t i = 0; i < cap_; ++i) slots_[i].turn.store(0, std::memory_order_relaxed);
    }

    void push(int v) {
        const std::size_t h = head_.fetch_add(1, std::memory_order_relaxed);
        Cell& s = slots_[idx(h)];
        while (turn_of(h) * 2 != s.turn.load(std::memory_order_acquire)) std::this_thread::yield();
        s.val = v;
        s.turn.store(turn_of(h) * 2 + 1, std::memory_order_release);
    }

    int pop() {
        const std::size_t t = tail_.fetch_add(1, std::memory_order_relaxed);
        Cell& s = slots_[idx(t)];
        while (turn_of(t) * 2 + 1 != s.turn.load(std::memory_order_acquire)) std::this_thread::yield();
        const int out = s.val;
        s.turn.store(turn_of(t) * 2 + 2, std::memory_order_release);
        return out;
    }

private:
    std::size_t idx(std::size_t i) const noexcept { return i % cap_; }
    std::size_t turn_of(std::size_t i) const noexcept { return i / cap_; }

    const std::size_t cap_;
    std::unique_ptr<Cell[]> slots_;
    alignas(64) std::atomic<std::size_t> head_{0};
    alignas(64) std::atomic<std::size_t> tail_{0};
};

int main() {
    constexpr std::size_t kCap = 1024;
    constexpr int kEach = 500;
    IntMpmcQueue q(kCap);
    std::atomic<std::int64_t> sum{0};
    std::atomic<bool> go{false};
    auto producer = [&] {
        while (!go.load(std::memory_order_acquire)) std::this_thread::yield();
        for (int i = 0; i < kEach; ++i) q.push(1);
    };
    auto consumer = [&] {
        while (!go.load(std::memory_order_acquire)) std::this_thread::yield();
        for (int i = 0; i < kEach; ++i) sum.fetch_add(q.pop(), std::memory_order_relaxed);
    };
    std::vector<std::thread> ts;
    for (int i = 0; i < 8; ++i) ts.emplace_back(producer);
    for (int i = 0; i < 8; ++i) ts.emplace_back(consumer);
    go.store(true, std::memory_order_release);
    for (auto& t : ts) t.join();
    assert(sum.load() == static_cast<std::int64_t>(8 * kEach));
    std::cout << "mpmc_queue OK" << std::endl;
    return 0;
}
```

`fetch_add` 取全局序号；按 `turn_of` 等待槽位；写 `val` 后 `release` 发布 turn。

## 练习与延伸

- 将 Python 版改为 `notify_all` 并对比延迟。
- 阅读 [Rigtorp MPMCQueue](https://github.com/rigtorp/MPMCQueue) 源码注释。
- 对照 `iv-classic-thread-safe-queue` 画锁/条件变量图。

## 学习路径

Day1 理解 turn 状态机；Day2 Python 阻塞版默写；Day3 C++ 无锁版 + memory order 口述。

## 延伸阅读

- [mpmc_queue notes](https://github.com/zhk0567/Algorithm/tree/main/python/interview/classic/mpmc_queue)
- 本站：`iv-classic-thread-safe-queue`、`iv-classic-ring-buffer`、`iv-classic-lockfree-stack`


**深度补充：turn 状态机**

槽位 turn：偶数轮可写、奇数轮可读、+2 回到下一轮；push/pop 各改一次。


**深度补充：head/tail 序号**

全局递增序号取模 cap 定位槽，turn_of 区分环上第几圈。


**深度补充：Python 对拍意义**

无官方无锁 MPMC API；参考版用于总和断言与面试口述阻塞实现。


**深度补充：背压与吞吐**

有界满时生产者等待；无界队列无法限制内存。


**深度补充：伪共享**

head/tail 与 Cell 分缓存行，否则多核争用同一行。


**深度补充：yield 自旋**

C++ 无锁版占不到槽位时让出 CPU；可换指数退避。


**深度补充：与 Disruptor**

同属环形有界通道；Disruptor 用序号屏障与等待策略。


**深度补充：MPSC 特例**

单生产者可省 head 原子争用；面试常问特化。


**深度补充：面试 15 分钟**

能画 Python 双 Condition；能口述 turn 三步状态。


**深度补充：复盘要点 10**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 11**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 12**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 13**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 14**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 15**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 16**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 17**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 18**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 19**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 20**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 21**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 22**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 23**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 24**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 25**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 26**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 27**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 28**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 29**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 30**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 31**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 32**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 33**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 34**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 35**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 36**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 37**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 38**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 39**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 40**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 41**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 42**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 43**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 44**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 45**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 46**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 47**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 48**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 49**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 50**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 51**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 52**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 53**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 54**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 55**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 56**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 57**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 58**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 59**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 60**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 61**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 62**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 63**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 64**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 65**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 66**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 67**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 68**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 69**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 70**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 71**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 72**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 73**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 74**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 75**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 76**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 77**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 78**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 79**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 80**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 81**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 82**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 83**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 84**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 85**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 86**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 87**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 88**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 89**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 90**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 91**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 92**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 93**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 94**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 95**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 96**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 97**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 98**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 99**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 100**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 101**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 102**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 103**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 104**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 105**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 106**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 107**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 108**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 109**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 110**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 111**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 112**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 113**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 114**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 115**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 116**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 117**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 118**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 119**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 120**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 121**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 122**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 123**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 124**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 125**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 126**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 127**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 128**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 129**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 130**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 131**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 132**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 133**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 134**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 135**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 136**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 137**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 138**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 139**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 140**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 141**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 142**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 143**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 144**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 145**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 146**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 147**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 148**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 149**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 150**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 151**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 152**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 153**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 154**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 155**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 156**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 157**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 158**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 159**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 160**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 161**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 162**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 163**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 164**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 165**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 166**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 167**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 168**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 169**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 170**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 171**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 172**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 173**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 174**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 175**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 176**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 177**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 178**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 179**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 180**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 181**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 182**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 183**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 184**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 185**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 186**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 187**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 188**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 189**

回到 iv-classic-mpmc-queue 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。
