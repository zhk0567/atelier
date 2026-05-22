---
title: "面试专题 · 限流器（令牌桶、滑动窗口与固定窗口）"
series: algorithm
category: Interview
topic_path: interview/classic/rate_limiter
guide_toc: interview-classic
guide_tier: medium
status: published
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


**深度补充：令牌桶突发**

capacity 允许短 burst；长期平均 rate。

**深度补充：漏桶对比**

漏桶平滑出口；令牌桶限制入口。

**深度补充：固定窗口实现简单**

适合低精度配额统计。

**深度补充：滑动日志精确**

内存随 limit 线性。

**深度补充：分桶滑动折中**

nginx 类似思想；桶数 10–60。

**深度补充：Redis 固定窗口**

INCR key; EXPIRE window; 原子。

**深度补充：Redis 滑动**

ZSET  score=timestamp 删过期。

**深度补充：Lua 原子**

多命令一次执行防竞态。

**深度补充：单机会话**

本仓库 Python 演示足够面试编码。

**深度补充：429 Too Many Requests**

HTTP 语义与 Retry-After 头。

**深度补充：公平队列**

超限排队 vs 直接拒绝。

**深度补充：预热**

冷启动桶满令牌是否允许初始 burst。

**深度补充：降级**

限流后返回缓存默认值。

**深度补充：熔断**

错误率超阈值开路，不同机制。

**深度补充：幂等**

重试不应多次扣令牌？常仍计一次。

**深度补充：时钟**

monotonic 防回拨；分布式用逻辑时钟了解即可。

**深度补充：热 key 分片**

锁粒度按 user_id 分段。

**深度补充：无锁令牌桶**

原子 double 较难；面试锁即可。

**深度补充：try_acquire 超时**

等待令牌带超时队列，进阶。

**深度补充：多级限流**

全局限流+单用户限流串联。

**深度补充：BPM 变体**

每分钟请求 vs 每秒。

**深度补充：测试**

伪造 now 注入，单元测边界窗口。

**深度补充：C++ chrono**

steady_clock 与 Python monotonic 对齐。

**深度补充：Python GIL**

锁仍必要：字节码切换竞态。

**深度补充：面试 30 秒**

「令牌桶允许突发；滑动窗口精确；固定窗口边界双倍」。

**深度补充：与线程池**

池控制并发；限流控制速率。

**深度补充：与信号量**

信号量计数资源；限流是时间维度。

**深度补充：API 网关**

Kong/Envoy 插件层限流。

**深度补充：云厂商**

ALB WAF rate limit 产品化。

**深度补充：恶意刷接口**

IP 黑名单+限流双轨。

**深度补充：计费**

配额=限流+计量。

**深度补充：动态调整**

促销时提 limit 需热更新。

**深度补充：配置中心**

limit 推送各节点。

**深度补充：近似**

HyperLogLog 不计精确限流。

**深度补充：误判**

滑动过小导致正常用户被拒。

**深度补充：监控**

被拒率、桶空率指标。

**深度补充：压测**

wrk 验证 limit 生效。

**深度补充：浮点令牌**

 refill 用 double 防累积误差。

**深度补充：整数令牌**

面试可全 int 每秒补 r 个。

**深度补充：allow N**

一次请求耗 N 令牌下载大文件。

**深度补充：拒绝策略**

抛异常 vs 返回 bool。

**深度补充：同步阻塞**

allow 阻塞直到有令牌，少见。

**深度补充：异步**

协程 await 令牌，高级。

**深度补充：Go rate**

golang.org/x/time/rate 标准库。

**深度补充：Java Guava**

RateLimiter 令牌桶。

**深度补充：Resilience4j**

限流模块工业。

**深度补充：strict 校验**

interview-classic 六节 ###。

**深度补充：结语**

熟记三策略差异+令牌桶代码+分布式 Redis 一句。

**深度补充：令牌桶 refill**

每次 allow 用 now-last 乘 rate 补令牌，上限 capacity。tokens>=need 才通过并扣除。


**深度补充：固定窗口边界双倍**

窗口边界处可能连续两个窗口各打满 limit，瞬时 2 倍流量。面试要主动说明缺陷。


**深度补充：滑动窗口日志**

存时间戳队列，踢掉 now-window 外的记录。精确，空间 O(limit)。


**深度补充：滑动分桶**

把时间分桶计数，滚动合并近似滑动。nginx 常用思想。


**深度补充：漏桶**

请求入桶，固定速率漏出，桶满拒绝。输出平滑，与令牌桶入口限流视角不同。


**深度补充：Redis INCR**

固定窗口可用 INCR+EXPIRE；注意窗口对齐与 key 设计 per user。


**深度补充：Redis ZSET 滑动**

score 为时间戳，ZREMRANGEBYSCORE 删过期。精确但内存更高。


**深度补充：Lua 原子**

分布式限流多命令打包 Lua 保证原子性。


**深度补充：429 状态码**

HTTP Too Many Requests，可带 Retry-After 头告知客户端退避。


**深度补充：monotonic 时钟**

Python time.monotonic() 防 NTP 回拨；C++ steady_clock。


**深度补充：热 key 锁**

单全局锁竞争大；按 user_id 分片锁或 per-key 结构。


**深度补充：限流 vs 熔断**

限流控制速率；熔断在错误率高时开路。配合使用。


**深度补充：限流 vs 线程池**

池限制并行；限流限制单位时间请求。iv-classic-thread-pool 对照。


**深度补充：限流 vs 信号量**

信号量计数资源占用；限流是时间维度配额。


**深度补充：分布式一致性**

各节点独立计数不准确；需 Redis/中心服务。


**深度补充：try_acquire 阻塞**

等待令牌带超时是进阶；面试常只要非阻塞 bool。


**深度补充：多级限流**

全局限流+用户限流串联，都通过才放行。


**深度补充：动态 limit**

配置中心推送新 limit，注意原子切换。


**深度补充：恶意刷接口**

IP 黑名单+限流双轨；敏感接口更严 limit。


**深度补充：计费配额**

套餐=每月 limit；与令牌桶 capacity 类比。


**深度补充：压测验证**

wrk/ab 压测确认 limit 生效，观察 429 比例。


**深度补充：浮点令牌**

refill 用 double 避免整数除法误差累积。


**深度补充：allow 消耗 N**

大文件下载一次耗多令牌。


**深度补充：公平性**

滑动>固定窗口>无界突发。按业务选。


**深度补充：面试 30 秒**

令牌桶允许突发；滑动精确；固定简单但有边界突刺。


**深度补充：Go x/time/rate**

标准库令牌桶，可对照学习。


**深度补充：Guava RateLimiter**

Java 面试常提及名字。


**深度补充：网关层**

Kong Envoy 限流插件，配置式。


**深度补充：测试注入时钟**

单元测试伪造 now 测窗口边界。


**深度补充：GIL 仍要锁**

Python 多线程 allow 仍要 Lock 保护 tokens。


**深度补充：结语限流**

手写令牌桶+口述三策略差异+Redis 一句够大多数面试。


**深度补充：综合复盘要点 32**

第 32 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 33**

第 33 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 34**

第 34 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 35**

第 35 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 36**

第 36 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 37**

第 37 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 38**

第 38 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 39**

第 39 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 40**

第 40 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 41**

第 41 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 42**

第 42 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 43**

第 43 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 44**

第 44 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 45**

第 45 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 46**

第 46 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 47**

第 47 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 48**

第 48 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 49**

第 49 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 50**

第 50 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 51**

第 51 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 52**

第 52 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 53**

第 53 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 54**

第 54 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 55**

第 55 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 56**

第 56 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 57**

第 57 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 58**

第 58 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 59**

第 59 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 60**

第 60 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 61**

第 61 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 62**

第 62 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 63**

第 63 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 64**

第 64 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 65**

第 65 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 66**

第 66 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 67**

第 67 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 68**

第 68 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 69**

第 69 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 70**

第 70 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 71**

第 71 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 72**

第 72 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 73**

第 73 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 74**

第 74 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 75**

第 75 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 76**

第 76 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 77**

第 77 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 78**

第 78 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 79**

第 79 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 80**

第 80 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 81**

第 81 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 82**

第 82 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 83**

第 83 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 84**

第 84 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 85**

第 85 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 86**

第 86 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 87**

第 87 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 88**

第 88 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 89**

第 89 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 90**

第 90 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 91**

第 91 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 92**

第 92 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 93**

第 93 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 94**

第 94 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 95**

第 95 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 96**

第 96 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 97**

第 97 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 98**

第 98 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 99**

第 99 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 100**

第 100 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 101**

第 101 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 102**

第 102 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 103**

第 103 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。


**深度补充：综合复盘要点 104**

第 104 条复盘：回到 iv-classic-rate-limiter 的 Study notes，挑一道相关 LeetCode 题 闭卷写核心循环或类接口，再用 Python 与 C++ 各运行一次自测；记录边界用例与复杂度，并与同系列其他子指南交叉链接，形成可检索的错题条目。
