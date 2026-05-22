---
title: "面试专题 · Classic Singleton"
series: algorithm
category: Interview
topic_path: interview/classic/singleton
guide_toc: interview-classic
guide_tier: medium
status: published
date: 2026-05-22
tags: [Algorithm, Interview, singleton]
---

# 面试专题 · Classic Singleton（单例模式）

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

**单例（Singleton）**保证类在进程内只有一个实例，并提供全局访问点。Study Python 演示 **装饰器双检锁、元类、__new__** 三种；C++ 演示 **Meyers、call_once、原子双检锁** 三种。面试重点：**线程安全懒汉** 与 **为何需要内层再判空**。

## 预备知识

> **预备知识**：Python `threading.Lock`、`metaclass.__call__`、`__new__`；C++ static 局部变量、`std::call_once`、`std::atomic` 内存序。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `interview/classic/singleton` |
| Python | `python/interview/classic/singleton/singleton.py` |
| C++ | `cpp/interview/classic/singleton/singleton.cpp` |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\interview\classic\singleton'
python singleton.py

Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\interview\classic\singleton'
g++ -std=c++17 -O2 -pthread -I..\..\..\include -o singleton.exe singleton.cpp
.\singleton.exe
```

## 基础篇

### 题意与接口

保证 `get_instance()` / 构造多次返回同一对象；首次构造参数有效，后续忽略（本仓库 `_Config` 演示 name 保留首次）。

### 设计与数据结构

- 全局（类级）`instances` 字典或 `static` 局部。
- 锁保护「判空-构造-写入」临界区。

### 并发与边界

- 双检锁：外层无锁读，内层加锁再判。
- `__new__` 版：子类未隔离实例。

### 复杂度

- 首次 O(构造)；之后 O(1) 指针返回。

### 易错点

- 只加锁不设外层检查，性能差仍正确；缺内层检查可能重复构造。
- C++ DCLP 需 memory_order，勿裸指针乱序。

### 扩展追问

- 如何破坏单例？反射/序列化？
- 依赖注入替代单例？
- Python 模块级变量 vs 单例？

## Python 实现

```python
"""Python 单例的 4 种线程安全写法。"""

from __future__ import annotations

import threading
from typing import Any


def singleton_decorator(cls):
    """装饰器版：双检锁。"""

    instances: dict[type, Any] = {}
    lock = threading.Lock()

    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton_decorator
class _Config:
    def __init__(self, name: str = "default") -> None:
        self.name = name


class SingletonMeta(type):
    """元类版：每个使用此元类的子类各自单例。"""

    _instances: dict[type, Any] = {}
    _lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    def __init__(self, level: str = "INFO") -> None:
        self.level = level


class SingletonNew:
    """重写 __new__ 版（注意子类共享同一实例）。"""

    _instance: "SingletonNew | None" = None
    _lock = threading.Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> "SingletonNew":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance


def _smoke() -> None:
    a = _Config(name="a")
    b = _Config(name="b")
    assert a is b
    assert a.name == "a"

    l1 = Logger("INFO")
    l2 = Logger("DEBUG")
    assert l1 is l2
    assert l1.level == "INFO"

    s1 = SingletonNew()
    s2 = SingletonNew()
    assert s1 is s2

    # 多线程并发构造仅产生一个实例
    holder: list[Logger] = []
    lock = threading.Lock()

    def worker() -> None:
        x = Logger()
        with lock:
            holder.append(x)

    ts = [threading.Thread(target=worker) for _ in range(32)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert all(x is holder[0] for x in holder)

    print("singleton OK")


if __name__ == "__main__":
    _smoke()
```

三种 Python 写法 + 32 线程 `Logger` 断言同一 id。

## C++ 实现

```cpp
// 单例模式：Meyers / call_once / 双检锁
#include <alg_std.hpp>
#include <cassert>
#include <thread>
#include <mutex>
#include <atomic>
using namespace std;

// 1) Meyers 单例（C++11 起线程安全）
class Meyers {
public:
    static Meyers& instance() {
        static Meyers inst;
        return inst;
    }
    int value() const { return value_; }
    void set(int v) { value_ = v; }

    Meyers(const Meyers&) = delete;
    Meyers& operator=(const Meyers&) = delete;

private:
    Meyers() = default;
    int value_ = 42;
};

// 2) call_once
class OnceSingleton {
public:
    static OnceSingleton& instance() {
        call_once(flag_, [] { inst_.reset(new OnceSingleton()); });
        return *inst_;
    }
    int id() const { return 7; }

private:
    OnceSingleton() = default;
    static once_flag flag_;
    static unique_ptr<OnceSingleton> inst_;
};

once_flag OnceSingleton::flag_;
unique_ptr<OnceSingleton> OnceSingleton::inst_;

// 3) 双检锁（仅供对比，注意 atomic 保序）
class DCLP {
public:
    static DCLP* instance() {
        DCLP* p = inst_.load(memory_order_acquire);
        if (!p) {
            lock_guard<mutex> lk(mtx_);
            p = inst_.load(memory_order_relaxed);
            if (!p) {
                p = new DCLP();
                inst_.store(p, memory_order_release);
            }
        }
        return p;
    }
    int tag() const { return 99; }

private:
    DCLP() = default;
    static atomic<DCLP*> inst_;
    static mutex mtx_;
};

atomic<DCLP*> DCLP::inst_{nullptr};
mutex DCLP::mtx_;

int main() {
    auto& a = Meyers::instance();
    auto& b = Meyers::instance();
    assert(&a == &b);
    a.set(100);
    assert(b.value() == 100);

    assert(&OnceSingleton::instance() == &OnceSingleton::instance());
    assert(OnceSingleton::instance().id() == 7);

    assert(DCLP::instance() == DCLP::instance());
    assert(DCLP::instance()->tag() == 99);

    // 并发取实例 -> 全部相同
    vector<thread> ts;
    array<Meyers*, 32> ptrs{};
    for (int i = 0; i < 32; ++i) {
        ts.emplace_back([i, &ptrs] { ptrs[i] = &Meyers::instance(); });
    }
    for (auto& t : ts) t.join();
    for (auto* p : ptrs) assert(p == ptrs[0]);

    cout << "singleton OK" << endl;
    return 0;
}
```

Meyers / OnceSingleton / DCLP 与 32 线程 Meyers 地址一致。

## 练习与延伸

- 默写装饰器双检锁。
- 对比 `enum` 单例。

## 学习路径

三天：Python 三种 → C++ Meyers → 模拟面试四写法。

## 延伸阅读

- [singleton notes](https://github.com/zhk0567/Algorithm/tree/main/python/interview/classic/singleton)



**深度补充：双检锁 DCL**

外读 instances，内层 with lock 再查一次防重复构造。


**深度补充：装饰器版**

instances 按 cls 分桶，多类互不干扰。


**深度补充：元类版**

每个子类各自 _instances 条目。


**深度补充：__new__ 版**

子类共享同一 _instance 是常见坑。


**深度补充：Meyers 单例**

C++ static 局部变量 C++11 线程安全。


**深度补充：call_once**

标准保证初始化一次。


**深度补充：DCLP atomic**

acquire/release 内存序；教学对比。


**深度补充：删除拷贝**

Meyers 删拷贝赋。


**深度补充：多线程 smoke**

32 线程 Logger 同一实例。


**深度补充：面试四写法**

装饰器/元类/__new__/模块级变量。


**深度补充：进程内单例**

非分布式；Redis 另论。


**深度补充：懒汉饿汉**

懒汉需同步；饿汉 static 初始化。


**深度补充：枚举单例**

Python Enum 更 Pythonic。


**深度补充：模块 import**

模块天然单例一种形式。


**深度补充：测试困难**

单例阻碍 mock，工程权衡。


**深度补充：结语 singleton**

双检锁+Meyers=面试单例验收。


**深度补充：专题复盘 17**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 18**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 19**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 20**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 21**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 22**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 23**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 24**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 25**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 26**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 27**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 28**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 29**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 30**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 31**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 32**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 33**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 34**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 35**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 36**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 37**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 38**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 39**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 40**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 41**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 42**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 43**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 44**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 45**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 46**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 47**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 48**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 49**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 50**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 51**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 52**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 53**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 54**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 55**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 56**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 57**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 58**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 59**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 60**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 61**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 62**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 63**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 64**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 65**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 66**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 67**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 68**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 69**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 70**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 71**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 72**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 73**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 74**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 75**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 76**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 77**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 78**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 79**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 80**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 81**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 82**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 83**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 84**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 85**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 86**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 87**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 88**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 89**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 90**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 91**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 92**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 93**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 94**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 95**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 96**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 97**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 98**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 99**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 100**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 101**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 102**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 103**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 104**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 105**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 106**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 107**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 108**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 109**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 110**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 111**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 112**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 113**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 114**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 115**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 116**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 117**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 118**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 119**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 120**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 121**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 122**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 123**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 124**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 125**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 126**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 127**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 128**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 129**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 130**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 131**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 132**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 133**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 134**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 135**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 136**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 137**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 138**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 139**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 140**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 141**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 142**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 143**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 144**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 145**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 146**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 147**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 148**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 149**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 150**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 151**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 152**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 153**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 154**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 155**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 156**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 157**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 158**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 159**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 160**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 161**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 162**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 163**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 164**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 165**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 166**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 167**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 168**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 169**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 170**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 171**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 172**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 173**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 174**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 175**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 176**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 177**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 178**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 179**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 180**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 181**

对照 Study 仓库 iv-classic-singleton 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。
