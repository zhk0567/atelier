---
title: "面试专题 · 总览与导航"
series: algorithm
category: Interview
topic_path: interview
guide_toc: interview-classic
guide_tier: medium
status: published
date: 2026-05-22
tags: [Interview, Classic, TopFrequent]
---

# 面试专题 · 总览与导航

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

`interview/` 分 **`classic/`**（手写 LRU、线程池、锁与无锁结构等）与 **`top_frequent/`**（高频题索引链回 `leetcode/`）。本页 `iv-` 导航 **15** 篇已发布 `iv-*` 指南，强调：classic 代码为 **教学向**，勿当生产级并发组件。

## 预备知识

> **预备知识**：熟悉 LeetCode 设计题、基本 OS 线程/锁概念；C++11 `atomic` 与 Python `threading` 名词。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
Get-Content -LiteralPath 'python\interview\notes.md' -Encoding utf8
```

| 分支 | 说明 | 指南 |
|------|------|------|
| `classic/` | 14+ 手写专题 | `iv-classic-*` |
| `top_frequent/` | 103 题索引 | [iv-top-frequent](/blog/iv-top-frequent) |

## 基础篇

### 题意与接口

设计题先澄清 API、复杂度、是否线程安全。classic 专题与力扣 146/460/155 等对应关系见各子页。

### 设计与数据结构

缓存类：哈希 + 双向链表；并发类：mutex/condition、环形缓冲、线程池任务队列；无锁类：原子 CAS、Ticket Lock。

### 并发与边界

说明「教学实现」与工业差距；小数据自测可对拍，不代表压测结论。

### 复杂度

设计题要求 get/put O(1)；锁粒度影响吞吐而非单操作渐近阶。

### 易错点

指针断链、死锁、ABA（无锁）、伪共享（口述）。

### 扩展追问

LFU vs LRU、读写锁饥饿、线程池拒绝策略、限流令牌桶 vs 漏桶。

## Python 实现

```python
# 节选：LRU get/put 骨架（classic/lru_cache/lru_cache.py）
def get(self, key: int) -> int:
    if key not in self._map:
        return -1
    node = self._map[key]
    self._move_to_front(node)
    return node.val
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\interview\classic\lru_cache'
python lru_cache.py
Set-Location -LiteralPath 'F:\Study\Algorithm\python\interview\classic\thread_pool'
python thread_pool.py
```

## C++ 实现

```cpp
// 节选：读写锁读者入口（classic/rwlock/rwlock.cpp 概念层）
void read_lock() {
    std::unique_lock<std::mutex> lk(guard);
    while (write) readers_cv.wait(lk);
    ++readers;
}
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\interview\classic\rwlock'
g++ -std=c++17 -pthread -O2 -o rw.exe rwlock.cpp
.\rw.exe
```

## 练习与延伸

- 设计题回 [prob-hot100](/blog/prob-hot100)
- 数据结构版 LRU：[ds-advanced-lru-cache](/blog/ds-advanced-lru-cache)

## 学习路径

先 `iv-classic-lru-cache` → 限流/环形缓冲 → 线程池 → 锁与无锁专题；并行维护 [iv-top-frequent](/blog/iv-top-frequent) 勾选。

## 延伸阅读

- [iv-classic-lfu-cache](/blog/iv-classic-lfu-cache)
- [iv-classic-lockfree-stack](/blog/iv-classic-lockfree-stack)
- [iv-classic-lru-cache](/blog/iv-classic-lru-cache)
- [iv-classic-mpmc-queue](/blog/iv-classic-mpmc-queue)
- [iv-classic-rate-limiter](/blog/iv-classic-rate-limiter)
- [iv-classic-ring-buffer](/blog/iv-classic-ring-buffer)
- [iv-classic-rwlock](/blog/iv-classic-rwlock)
- [iv-classic-rwlock-writer-pref](/blog/iv-classic-rwlock-writer-pref)
- [iv-classic-semaphore](/blog/iv-classic-semaphore)
- [iv-classic-singleton](/blog/iv-classic-singleton)
- [iv-classic-tas-spinlock](/blog/iv-classic-tas-spinlock)
- [iv-classic-thread-pool](/blog/iv-classic-thread-pool)
- [iv-classic-thread-safe-queue](/blog/iv-classic-thread-safe-queue)
- [iv-classic-ticket-lock](/blog/iv-classic-ticket-lock)
- [iv-top-frequent](/blog/iv-top-frequent)


**深度补充：classic 定位**

能白板讲清 invariant 即可，不必背工业参数。


**深度补充：与 leetcode**

题解在 problems/leetcode；classic 在 interview/classic。


**深度补充：导航复盘 3**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 4**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 5**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 6**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 7**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 8**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 9**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 10**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 11**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 12**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 13**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 14**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 15**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 16**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 17**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 18**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 19**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 20**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 21**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 22**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 23**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 24**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 25**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 26**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 27**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 28**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 29**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 30**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 31**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 32**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 33**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 34**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 35**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 36**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 37**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 38**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 39**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 40**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 41**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 42**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 43**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 44**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 45**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 46**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 47**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 48**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 49**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 50**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 51**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 52**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 53**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 54**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 55**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 56**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 57**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 58**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 59**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 60**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 61**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 62**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 63**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 64**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 65**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 66**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 67**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 68**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 69**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 70**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 71**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 72**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 73**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 74**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 75**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 76**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 77**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 78**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 79**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 80**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 81**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 82**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 83**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 84**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 85**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 86**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 87**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 88**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 89**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 90**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 91**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 92**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 93**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 94**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 95**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 96**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 97**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 98**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 99**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 100**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 101**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 102**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 103**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 104**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 105**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 106**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 107**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 108**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 109**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 110**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 111**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 112**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 113**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 114**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 115**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 116**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 117**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 118**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 119**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 120**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 121**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 122**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 123**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 124**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 125**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 126**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 127**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 128**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 129**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 130**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 131**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 132**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 133**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 134**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 135**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 136**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 137**

以 iv- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。
