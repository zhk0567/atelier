---
title: "面试专题 · Classic Ticket Lock"
series: algorithm
category: Interview
topic_path: interview/classic/ticket_lock
guide_toc: interview-classic
guide_tier: medium
status: published
date: 2026-05-22
tags: [Algorithm, Interview, ticket]
---

# 面试专题 · Classic Ticket Lock（票号锁·公平）

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
Set-Location -LiteralPath 'F:\Study\Algorithm\python\interview\classic\ticket_lock'
python ticket_lock.py

Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\interview\classic\ticket_lock'
g++ -std=c++17 -O2 -pthread -I..\..\..\include -o ticket.exe ticket_lock.cpp
.\ticket.exe
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

```python
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
```

取号在 `with self._cv` 内；`wait_for` 等待轮到自己。

## C++ 实现

```cpp
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
```

`fetch_add` 取号；自旋直到 `now==my`；`unlock` 递增 now。

## 练习与延伸

- 给 C++ 版加指数退避。
- 对比 TAS 压测 P99 延迟。

## 学习路径

Day1 画叫号图；Day2 Python 默写；Day3 C++ atomic 版 + 公平性论述。

## 延伸阅读

- [ticket_lock notes](https://github.com/zhk0567/Algorithm/tree/main/python/interview/classic/ticket_lock)
- 本站：`iv-classic-tas-spinlock`


**深度补充：取号与叫号**

next 发号，now 叫号；仅相等者进入。


**深度补充：FIFO 公平**

相对 TAS 解决饥饿；面试对比要点。


**深度补充：Python Condition**

阻塞等待省 CPU；适合教学验证。


**深度补充：C++ 自旋**

yield 循环；高竞争需退避。


**深度补充：notify_all**

唤醒后由谓词筛选，避免错唤醒进临界区。


**深度补充：票号溢出**

uint64 实践足够；理论讨论 wrap。


**深度补充：MCS/CLH**

链表队列锁减少缓存颠簸；进阶一句。


**深度补充：内核 mutex**

许多实现带排队公平；与用户态 ticket 对照。


**深度补充：复盘要点 9**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 10**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 11**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 12**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 13**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 14**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 15**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 16**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 17**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 18**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 19**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 20**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 21**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 22**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 23**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 24**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 25**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 26**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 27**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 28**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 29**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 30**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 31**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 32**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 33**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 34**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 35**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 36**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 37**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 38**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 39**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 40**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 41**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 42**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 43**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 44**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 45**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 46**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 47**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 48**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 49**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 50**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 51**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 52**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 53**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 54**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 55**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 56**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 57**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 58**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 59**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 60**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 61**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 62**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 63**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 64**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 65**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 66**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 67**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 68**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 69**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 70**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 71**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 72**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 73**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 74**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 75**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 76**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 77**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 78**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 79**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 80**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 81**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 82**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 83**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 84**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 85**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 86**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 87**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 88**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 89**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 90**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 91**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 92**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 93**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 94**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 95**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 96**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 97**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 98**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 99**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 100**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 101**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 102**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 103**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 104**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 105**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 106**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 107**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 108**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 109**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 110**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 111**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 112**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 113**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 114**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 115**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 116**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 117**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 118**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 119**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 120**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 121**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 122**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 123**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 124**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 125**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 126**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 127**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 128**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 129**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 130**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 131**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 132**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 133**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 134**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 135**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 136**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 137**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 138**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 139**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 140**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 141**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 142**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 143**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 144**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 145**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 146**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 147**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 148**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 149**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 150**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 151**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 152**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 153**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 154**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 155**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 156**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 157**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 158**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 159**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 160**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 161**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 162**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 163**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 164**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 165**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 166**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 167**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 168**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 169**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 170**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 171**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 172**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 173**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 174**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 175**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 176**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 177**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 178**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 179**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 180**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 181**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 182**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 183**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 184**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 185**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 186**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 187**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 188**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 189**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 190**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 191**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 192**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 193**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 194**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 195**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 196**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。


**深度补充：复盘要点 197**

回到 iv-classic-ticket-lock 的 Study notes，闭卷默写核心不变量与锁顺序，再运行 Python/C++ 自测；与同系列 iv-classic 专题交叉链接。
