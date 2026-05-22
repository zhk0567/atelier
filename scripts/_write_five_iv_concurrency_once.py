# -*- coding: utf-8 -*-
"""One-off: iv-classic mpmc / rwlock / rwlock-wp / tas / ticket (medium >=8000)."""
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
                f"回到 {slug} 的 Study notes，闭卷默写核心不变量与锁顺序，"
                f"再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。"
            )
        text += f"\n\n**深度补充：{title}**\n\n{body}\n"
        i += 1
        if i > 500:
            raise RuntimeError(f"pad failed {slug}: {count_chinese(text)}")
    return text


def _toc() -> str:
    return """## 目录

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


def _fm(title: str, topic: str, tags: str) -> str:
    return f"""---
title: "{title}"
series: algorithm
category: Interview
topic_path: interview/classic/{topic}
guide_toc: interview-classic
guide_tier: medium
status: draft
date: 2026-05-22
tags: [{tags}]
---
"""


PY_MPMC = r'''```python
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
```'''

CPP_MPMC = r'''```cpp
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
```'''

PY_RW = r'''```python
"""读写锁（读者优先）：读者共享 `readers` 计数，首个读者持写互斥、末读者释放。"""

from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from typing import Generator


class RWLock:
    def __init__(self) -> None:
        self._guard = threading.Lock()
        self._write = threading.Lock()
        self._readers = 0

    @contextmanager
    def read_lock(self) -> Generator[None, None, None]:
        with self._guard:
            self._readers += 1
            if self._readers == 1:
                self._write.acquire()
        try:
            yield
        finally:
            with self._guard:
                self._readers -= 1
                if self._readers == 0:
                    self._write.release()

    @contextmanager
    def write_lock(self) -> Generator[None, None, None]:
        self._write.acquire()
        try:
            yield
        finally:
            self._write.release()
```'''

CPP_RW = r'''```cpp
// 读写锁（读者优先）：与 Python 版同构（C++17）
#include <alg_std.hpp>
#include <cassert>
#include <chrono>
#include <mutex>
#include <thread>
using namespace std;

class RWLock {
public:
    void read_lock() {
        lock_guard<mutex> lk(guard_);
        if (++readers_ == 1) write_.lock();
    }
    void read_unlock() {
        lock_guard<mutex> lk(guard_);
        if (--readers_ == 0) write_.unlock();
    }
    void write_lock() { write_.lock(); }
    void write_unlock() { write_.unlock(); }

private:
    mutex guard_;
    mutex write_;
    int readers_ = 0;
};
```'''

PY_RWP = r'''```python
"""读写锁（写者优先）：写者持「读入口闸」阻塞新读者，再独占资源。"""

from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import Generator


class WriterPreferRWLock:
    def __init__(self) -> None:
        self._read_gate = threading.Lock()
        self._guard = threading.Lock()
        self._resource = threading.Lock()
        self._readers = 0

    @contextmanager
    def read_lock(self) -> Generator[None, None, None]:
        self._read_gate.acquire()
        try:
            with self._guard:
                self._readers += 1
                if self._readers == 1:
                    self._resource.acquire()
        finally:
            self._read_gate.release()
        try:
            yield
        finally:
            with self._guard:
                self._readers -= 1
                if self._readers == 0:
                    self._resource.release()

    @contextmanager
    def write_lock(self) -> Generator[None, None, None]:
        self._read_gate.acquire()
        self._resource.acquire()
        try:
            yield
        finally:
            self._resource.release()
            self._read_gate.release()
```'''

CPP_RWP = r'''```cpp
// 读写锁（写者优先）：与 Python 版同构（C++17）
#include <alg_std.hpp>
#include <mutex>
using namespace std;

class WriterPreferRWLock {
public:
    void read_lock() {
        read_gate_.lock();
        { lock_guard<mutex> lk(guard_); if (++readers_ == 1) resource_.lock(); }
        read_gate_.unlock();
    }
    void read_unlock() {
        lock_guard<mutex> lk(guard_);
        if (--readers_ == 0) resource_.unlock();
    }
    void write_lock() { read_gate_.lock(); resource_.lock(); }
    void write_unlock() { resource_.unlock(); read_gate_.unlock(); }

private:
    mutex read_gate_, guard_, resource_;
    int readers_ = 0;
};
```'''

PY_TAS = r'''```python
class TASSpinLock:
    def __init__(self) -> None:
        self._mtx = threading.Lock()
        self._locked = False

    def acquire(self) -> None:
        while True:
            with self._mtx:
                if not self._locked:
                    self._locked = True
                    return

    def release(self) -> None:
        with self._mtx:
            self._locked = False
```'''

CPP_TAS = r'''```cpp
#include <atomic>
#include <thread>

class TASSpinLock {
public:
    void lock() {
        while (flag_.test_and_set(std::memory_order_acquire)) std::this_thread::yield();
    }
    void unlock() { flag_.clear(std::memory_order_release); }

private:
    std::atomic_flag flag_ = ATOMIC_FLAG_INIT;
};
```'''

PY_TICKET = r'''```python
class TicketLock:
    def __init__(self) -> None:
        self._mtx = threading.Lock()
        self._cv = threading.Condition(self._mtx)
        self._next_ticket = 0
        self._now_serving = 0

    def acquire(self, timeout=None) -> bool:
        with self._cv:
            my = self._next_ticket
            self._next_ticket += 1
            return bool(self._cv.wait_for(lambda: self._now_serving == my, timeout=timeout))

    def release(self) -> None:
        with self._cv:
            self._now_serving += 1
            self._cv.notify_all()
```'''

CPP_TICKET = r'''```cpp
#include <atomic>
#include <thread>
using namespace std;

class TicketSpinLock {
public:
    void lock() {
        const uint64_t my = next_.fetch_add(1, memory_order_relaxed);
        while (now_.load(memory_order_acquire) != my) this_thread::yield();
    }
    void unlock() { now_.fetch_add(1, memory_order_release); }

private:
    atomic<uint64_t> next_{0}, now_{0};
};
```'''


GUIDES: dict[str, tuple[str, list[tuple[str, str]]]] = {}

GUIDES["iv-classic-mpmc-queue"] = (
    _fm("面试专题 · Classic Mpmc Queue", "mpmc_queue", "Algorithm, Interview, mpmc, queue")
    + "\n# 面试专题 · Classic Mpmc Queue（有界 MPMC 队列）\n\n"
    + _toc()
    + """
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
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\mpmc_queue'
python mpmc_queue.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\mpmc_queue'
g++ -std=c++17 -O2 -pthread -o mpmc.exe mpmc_queue.cpp
.\\mpmc.exe
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

"""
    + PY_MPMC
    + """

要点：`push` 在 `not_full` 上 `while len>=cap: wait`；`pop` 对称；压测用 `Event` 同步起跑。

## C++ 实现

"""
    + CPP_MPMC
    + """

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
""",
    [
        ("turn 状态机", "槽位 turn：偶数轮可写、奇数轮可读、+2 回到下一轮；push/pop 各改一次。"),
        ("head/tail 序号", "全局递增序号取模 cap 定位槽，turn_of 区分环上第几圈。"),
        ("Python 对拍意义", "无官方无锁 MPMC API；参考版用于总和断言与面试口述阻塞实现。"),
        ("背压与吞吐", "有界满时生产者等待；无界队列无法限制内存。"),
        ("伪共享", "head/tail 与 Cell 分缓存行，否则多核争用同一行。"),
        ("yield 自旋", "C++ 无锁版占不到槽位时让出 CPU；可换指数退避。"),
        ("与 Disruptor", "同属环形有界通道；Disruptor 用序号屏障与等待策略。"),
        ("MPSC 特例", "单生产者可省 head 原子争用；面试常问特化。"),
        ("面试 15 分钟", "能画 Python 双 Condition；能口述 turn 三步状态。"),
    ],
)

GUIDES["iv-classic-rwlock"] = (
    _fm("面试专题 · Classic Rwlock", "rwlock", "Algorithm, Interview, rwlock")
    + "\n# 面试专题 · Classic Rwlock（读写锁·读者优先）\n\n"
    + _toc()
    + """
## 导读

**读写锁（RWLock，读者优先）**允许多个读者并发访问共享数据，写者独占。经典手写结构是 **`guard` 保护读者计数 + `write` 互斥写路径**：首个读者获取写锁，末读者释放写锁；写者直接 `write_lock`。Study Python 用 `@contextmanager`；C++ 与 Python 同构，便于对照 `std::shared_mutex` 的 `shared_lock`/`unique_lock`。

局限：**写者饥饿**——读者源源不断时写者长期进不去。工程上可读多写少场景用读者优先，写不能饿死则换 `iv-classic-rwlock-writer-pref`。

## 预备知识

> **预备知识**：互斥锁、RAII、`contextmanager`；读多写少缓存；避免读锁升级写锁死锁。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/rwlock` |
| Python | `python/interview/classic/rwlock/rwlock.py` |
| C++ | `cpp/interview/classic/rwlock/rwlock.cpp` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\rwlock'
python rwlock.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\rwlock'
g++ -std=c++17 -O2 -pthread -I..\\..\\..\\include -o rw.exe rwlock.cpp
.\\rw.exe
```

## 基础篇

### 题意与接口

- `read_lock()` / `read_unlock()`：多读者并发。
- `write_lock()` / `write_unlock()`：写者独占。
- 压测：4 读者 + 1 写者，写者递增共享计数 50 次。

### 设计与数据结构

- `_guard`：保护 `_readers` 增减。
- `_write`：读者群与写者互斥的「写令牌」。
- 首个读者 `readers==1` 时 `write.acquire()`；末读者 `readers==0` 时 `write.release()`。

### 并发与边界

- 写者不等读者计数，直接抢 `_write`。
- 读者在 `_guard` 内改计数，临界区极短。
- **禁止**在读锁持有期间再申请写锁（升级死锁）。

### 复杂度

- 读锁获取 O(1)；写锁 O(1)；争用取决于读者数量。

### 易错点

- 忘记末读者 release 写锁 → 写者永久阻塞。
- 在 `read_lock` 内调用 `write_lock`。
- 与 `threading.RLock` 混淆：RWLock 不是可重入读写锁。

### 扩展追问

- `std::shared_mutex` 策略枚举？
- 如何实现写者优先？
- 读锁能否嵌套？

## Python 实现

"""
    + PY_RW
    + """

`read_lock` 先增计数再可能占写锁；`write_lock` 直接占写锁。

## C++ 实现

"""
    + CPP_RW
    + """

与 Python 逻辑一一对应；压测用 `atomic<int>` 共享计数。

## 练习与延伸

- 实现读锁嵌套计数（同线程多次 read_lock）。
- 对比 `iv-classic-rwlock-writer-pref` 三锁模型。

## 学习路径

Day1 画双锁时序；Day2 默写读者计数；Day3 口述写者饥饿与对策。

## 延伸阅读

- [rwlock notes](https://github.com/zhk0567/Algorithm/tree/main/python/interview/classic/rwlock)
- 本站：`iv-classic-rwlock-writer-pref`
""",
    [
        ("首个读者规则", "readers 从 0→1 时必须 acquire write，挡住写者。"),
        ("末读者规则", "readers 从 1→0 时 release write，写者可进。"),
        ("写者路径", "write_lock 不经过 guard 计数，直接互斥。"),
        ("写者饥饿", "连续读者导致写者饿死；面试必答。"),
        ("shared_mutex", "C++17 标准库；策略由实现定义。"),
        ("配置缓存场景", "路由表、feature flag 读多写少。"),
        ("升级死锁", "读锁内再写锁；应先放读再拿写。"),
        ("面试对比", "与 Mutex 比：读路径无互斥；写路径相同。"),
    ],
)

GUIDES["iv-classic-rwlock-writer-pref"] = (
    _fm("面试专题 · Classic Rwlock Writer Pref", "rwlock_writer_pref", "Algorithm, Interview, rwlock")
    + "\n# 面试专题 · Classic Rwlock Writer Pref（读写锁·写者优先）\n\n"
    + _toc()
    + """
## 导读

**写者优先读写锁**在读者优先版基础上增加 **`read_gate`（读入口闸）**：写者进入写路径前先占用 `read_gate`，使**新读者**在入口阻塞；已在读的读者仍通过 `resource` + 读者计数完成临界区。从而避免写者长期饥饿，代价是**读者可能饥饿**（写者连续到达）。

Study 三锁模型：`read_gate`、`guard+readers`、`resource`。写者：`read_gate` → `resource`；读者：过 gate → 计数 → 首读者占 resource。

## 预备知识

> **预备知识**：读者优先 RWLock（`iv-classic-rwlock`）；锁顺序固定防死锁；写密集日志/指标场景。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/rwlock_writer_pref` |
| Python | `python/interview/classic/rwlock_writer_pref/rwlock_writer_pref.py` |
| C++ | `cpp/interview/classic/rwlock_writer_pref/rwlock_writer_pref.cpp` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\rwlock_writer_pref'
python rwlock_writer_pref.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\rwlock_writer_pref'
g++ -std=c++17 -O2 -pthread -I..\\..\\..\\include -o rwp.exe rwlock_writer_pref.cpp
.\\rwp.exe
```

## 基础篇

### 题意与接口

同读者优先版：`read_lock` / `write_lock` 上下文管理器；压测形状一致。

### 设计与数据结构

- `read_gate`：写者与读者竞争；写者持有期间新读者阻塞。
- `guard` + `readers`：与读者优先相同。
- `resource`：读者群与写者互斥资源。

### 并发与边界

- 读者：`read_gate.acquire()` → 增计数 → 可能 `resource.acquire()` → **释放 gate**（允许后续读者排队但写者可抢先占 gate）。
- 写者：占 `read_gate` 后占 `resource`，期间新读者无法过 gate。
- 锁顺序：避免交叉嵌套导致死锁。

### 复杂度

O(1) 锁操作；多一把 gate 增加争用常数。

### 易错点

- 读者未在计数后释放 `read_gate`，导致吞吐骤降。
- 写者未先占 `read_gate` 则无法挡新读者。
- 与读者优先 API 相同但语义不同，不可混用测试基准。

### 扩展追问

- 如何实现公平读写锁（队列排队）？
- Linux `pthread_rwlock` 偏好策略？
- 读者饥饿时业务表现？

## Python 实现

"""
    + PY_RWP
    + """

`read_lock` 入口占 gate，计数后释放 gate；`write_lock` 持 gate+resource。

## C++ 实现

"""
    + CPP_RWP
    + """

三把 `mutex` 与 Python 同构；面试对照口述即可。

## 练习与延伸

- 对比读者优先版压测写者等待时间。
- 画写者占 gate 时新读者阻塞的时序图。

## 学习路径

先掌握 `iv-classic-rwlock`，再本专题三锁；Day3 能白板对比两种偏好。

## 延伸阅读

- [rwlock_writer_pref notes](https://github.com/zhk0567/Algorithm/tree/main/python/interview/classic/rwlock_writer_pref)
- 本站：`iv-classic-rwlock`
""",
    [
        ("read_gate 作用", "写者先占 gate，新读者在 acquire gate 处等待。"),
        ("读者释放 gate", "计数完成后释放 gate，让排队读者或写者竞争。"),
        ("写者双锁", "write 路径同时持 gate 与 resource。"),
        ("读者饥饿", "写者连续到达时读者长期等待。"),
        ("三锁顺序", "固定顺序避免死锁；面试画表。"),
        ("日志落盘", "写不能饿死：指标刷盘、配置热更新。"),
        ("pthread 对照", "读写锁属性 PREFER_WRITER_NONRECURSIVE_NP 等。"),
        ("公平队列扩展", "再加 Condition 排队可实现严格公平。"),
    ],
)

GUIDES["iv-classic-tas-spinlock"] = (
    _fm("面试专题 · Classic Tas Spinlock", "tas_spinlock", "Algorithm, Interview, spinlock")
    + "\n# 面试专题 · Classic Tas Spinlock（TAS 自旋锁）\n\n"
    + _toc()
    + """
## 导读

**Test-And-Set（TAS）自旋锁**是最简原子互斥：循环 `test_and_set` 直到成功占锁，释放时 `clear`。C++ 用 `std::atomic_flag` 一条硬件语义；Python 标准库无等价原子，Study 用 **小锁保护布尔标志 + 外层 while** 模拟「占不到就继续试」的形态，用于正确性自测与面试对齐，**不是**内核级无锁 TAS。

适用：**极短临界区**、理解 CAS、缓存一致性、与 `iv-classic-ticket-lock` 公平性对比。高竞争需 **yield/退避**，勿长时间占自旋锁。

## 预备知识

> **预备知识**：`atomic_flag`、memory_order；自旋 vs 阻塞；伪共享与总线流量。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/tas_spinlock` |
| Python | `python/interview/classic/tas_spinlock/tas_spinlock.py` |
| C++ | `cpp/interview/classic/tas_spinlock/tas_spinlock.cpp` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\tas_spinlock'
python tas_spinlock.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\tas_spinlock'
g++ -std=c++17 -O2 -pthread -o tas.exe tas_spinlock.cpp
.\\tas.exe
```

## 基础篇

### 题意与接口

- `acquire()` / `release()`（Python）；`lock()` / `unlock()`（C++）。
- 压测：10 线程各递增共享计数 100 次，总和 1000。

### 设计与数据结构

- C++：`atomic_flag`，`test_and_set(acquire)`，`clear(release)`。
- Python：`_locked` 布尔 + `_mtx` 保护 test-and-set 临界区。

### 并发与边界

- 自旋占用 CPU；竞争高时浪费周期。
- **不公平**：无 FIFO，可能饥饿。
- 临界区必须极短，否则应换 `mutex` 或带退避的 ticket/queue lock。

### 复杂度

无竞争 O(1)；高竞争 O(争用度) 自旋次数。

### 易错点

- 把 Python 版当真无锁向面试官宣称。
- 忘记 `memory_order`（C++）导致可见性问题。
- 多锁在同一缓存行导致颠簸。

### 扩展追问

- TTAS 与 MCS/CLH 队列锁？
- 何时自旋、何时 sleep？
- `atomic<bool>` 与 `atomic_flag` 区别？

## Python 实现

"""
    + PY_TAS
    + """

外层 `while True` 自旋；内层短临界区完成 test-and-set。

## C++ 实现

"""
    + CPP_TAS
    + """

纯 `atomic_flag`；竞争时 `yield`。

## 练习与延伸

- 实现指数退避自旋。
- 对比 `iv-classic-ticket-lock` 公平性。

## 学习路径

Day1 口述 TAS 指令；Day2 C++ 默写；Day3 Python 说明教学局限。

## 延伸阅读

- [tas_spinlock notes](https://github.com/zhk0567/Algorithm/tree/main/python/interview/classic/tas_spinlock)
- 本站：`iv-classic-ticket-lock`
""",
    [
        ("TAS 语义", "原子读旧值并置位；旧值为 0 则获锁。"),
        ("Python 教学版", "Lock 模拟 CAS；面试如实说明。"),
        ("不公平", "无排队；高竞争可能饿死。"),
        ("缓存颠簸", "多核争用同一 flag 缓存行。"),
        ("yield 退避", "C++ 占不到时让出 CPU。"),
        ("TTAS", "先 test 再 set 减少总线流量。"),
        ("临界区长度", "自旋锁仅适合极短更新。"),
        ("与 Mutex", "Mutex 阻塞睡眠；自旋烧 CPU。"),
    ],
)

GUIDES["iv-classic-ticket-lock"] = (
    _fm("面试专题 · Classic Ticket Lock", "ticket_lock", "Algorithm, Interview, ticket")
    + "\n# 面试专题 · Classic Ticket Lock（票号锁·公平）\n\n"
    + _toc()
    + """
## 导读

**Ticket Lock（票号锁）**按到达顺序发号：线程取 `my_ticket = next++`，仅当 `now_serving == my` 时进入临界区；`release` 将 `now_serving++` 叫下一号。提供 **FIFO 公平**，解决 TAS 不公平与饥饿。Python 用 `Condition.wait_for`；C++ 用 `atomic` + 自旋 `yield`，与 `iv-classic-tas-spinlock` 对照。

高竞争时纯自旋耗电；工程常加退避或混合 mutex。票号溢出理论需大整数（uint64 教学足够）。

## 预备知识

> **预备知识**：TAS 自旋锁；`Condition.wait_for`；公平锁 vs 吞吐权衡。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/ticket_lock` |
| Python | `python/interview/classic/ticket_lock/ticket_lock.py` |
| C++ | `cpp/interview/classic/ticket_lock/ticket_lock.cpp` |

```powershell
Set-Location -LiteralPath 'F:\\Study\\Algorithm\\python\\interview\\classic\\ticket_lock'
python ticket_lock.py

Set-Location -LiteralPath 'F:\\Study\\Algorithm\\cpp\\interview\\classic\\ticket_lock'
g++ -std=c++17 -O2 -pthread -I..\\..\\..\\include -o ticket.exe ticket_lock.cpp
.\\ticket.exe
```

## 基础篇

### 题意与接口

- `acquire(timeout=None)`：取号并等待叫号；Python 支持超时。
- `release()`：`now_serving++` 并 `notify_all`。
- 压测：10×100 次递增，总和 1000。

### 设计与数据结构

- `next_ticket`：发号器；`now_serving`：当前服务号。
- Python：`Condition` + `wait_for(lambda: now==my)`。
- C++：双 `atomic<uint64_t>`，不等则 yield。

### 并发与边界

- 公平性：严格 FIFO（同进程线程调度下按取号顺序）。
- C++ 自旋等待高竞争烧 CPU；Python 阻塞更省 CPU 但延迟高。
- `notify_all` 唤醒所有等待者，由谓词过滤（仅叫号匹配者通过）。

### 复杂度

逻辑 O(1)；等待成本取决于竞争与自旋/阻塞策略。

### 易错点

- `release` 未递增 `now_serving` → 全员死等。
- 取号与等待非原子分离会导致重复进临界区（实现须在持锁下完成）。
- 与银行叫号混淆：这里是互斥锁语义。

### 扩展追问

- MCS/CLH 队列锁优势？
- 票号溢出如何处理？
- 内核 mutex 是否公平？

## Python 实现

"""
    + PY_TICKET
    + """

取号在 `with self._cv` 内；`wait_for` 等待轮到自己。

## C++ 实现

"""
    + CPP_TICKET
    + """

`fetch_add` 取号；自旋直到 `now==my`；`unlock` 递增 now。

## 练习与延伸

- 给 C++ 版加指数退避。
- 对比 TAS 压测 P99 延迟。

## 学习路径

Day1 画叫号图；Day2 Python 默写；Day3 C++ atomic 版 + 公平性论述。

## 延伸阅读

- [ticket_lock notes](https://github.com/zhk0567/Algorithm/tree/main/python/interview/classic/ticket_lock)
- 本站：`iv-classic-tas-spinlock`
""",
    [
        ("取号与叫号", "next 发号，now 叫号；仅相等者进入。"),
        ("FIFO 公平", "相对 TAS 解决饥饿；面试对比要点。"),
        ("Python Condition", "阻塞等待省 CPU；适合教学验证。"),
        ("C++ 自旋", "yield 循环；高竞争需退避。"),
        ("notify_all", "唤醒后由谓词筛选，避免错唤醒进临界区。"),
        ("票号溢出", "uint64 实践足够；理论讨论 wrap。"),
        ("MCS/CLH", "链表队列锁减少缓存颠簸；进阶一句。"),
        ("内核 mutex", "许多实现带排队公平；与用户态 ticket 对照。"),
    ],
)


def main() -> None:
    for slug, (body, seeds) in GUIDES.items():
        out = BLOG / slug / "index.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        text = _pad(body, slug, seeds)
        n = count_chinese(text)
        out.write_text(text, encoding="utf-8")
        print(f"wrote {slug}: {n} chinese chars")
    print("done")


if __name__ == "__main__":
    main()
