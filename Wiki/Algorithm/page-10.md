<!-- wiki_page_id: page-10 -->

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [cpp/interview/classic/lru_cache/lru_cache.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/interview/classic/lru_cache/lru_cache.cpp)
- [cpp/interview/classic/lfu_cache/lfu_cache.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/interview/classic/lfu_cache/lfu_cache.cpp)
- [cpp/interview/classic/thread_pool/thread_pool.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/interview/classic/thread_pool/thread_pool.cpp)
- [cpp/interview/classic/semaphore/semaphore.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/interview/classic/semaphore/semaphore.cpp)
- [cpp/interview/classic/rwlock/rwlock.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/interview/classic/rwlock/rwlock.cpp)
- [cpp/interview/classic/rwlock_writer_pref/rwlock_writer_pref.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/interview/classic/rwlock_writer_pref/rwlock_writer_pref.cpp)
- [cpp/interview/classic/tas_spinlock/tas_spinlock.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/interview/classic/tas_spinlock/tas_spinlock.cpp)
- [cpp/interview/classic/ticket_lock/ticket_lock.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/interview/classic/ticket_lock/ticket_lock.cpp)
- [cpp/interview/classic/mpmc_queue/mpmc_queue.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/interview/classic/mpmc_queue/mpmc_queue.cpp)
- [cpp/interview/classic/thread_safe_queue/thread_safe_queue.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/interview/classic/thread_safe_queue/thread_safe_queue.cpp)
</details>

# 面试高频题与并发实现

## 概述

本文档详细介绍了在 Algorithm 项目中实现的几种经典面试高频题及并发编程实现，包括缓存淘汰算法（LRU、LFU）、线程池、信号量、读写锁、自旋锁以及各种并发队列。这些实现均基于现代 C++ 标准，具有良好的封装性和可读性，适用于学习和面试准备。

## LRU 缓存（Least Recently Used Cache）

### 实现原理

LRU 缓存根据访问时间淘汰最久未使用的数据。核心思想是使用双向链表维护访问顺序，哈希表提供 O(1) 查找能力。

### 关键实现细节

- 使用 `std::list` 维护访问顺序，最近访问的节点在表头，最久未使用的在表尾
- 使用 `std::unordered_map` 存储 key 到 list 节点的映射，实现 O(1) 访问
- `get` 操作：如果 key 存在，将对应节点移到表头并返回值；否则返回 -1
- `put` 操作：如果 key 存在，更新值并移到表头；如果不存在且缓存已满，删除表尾节点（最久未使用）；然后在表头插入新节点

### 代码结构

```cpp
class LRUCache {
private:
    struct Node {
        int key, value;
        Node* prev;
        Node* next;
        Node(int k, int v) : key(k), value(v), prev(nullptr), next(nullptr) {}
    };

    int capacity;
    std::unordered_map<int, Node*> cache;
    Node* head;  // 虚拟头节点
    Node* tail;  // 虚拟尾节点

    void addToHead(Node* node);
    void removeNode(Node* node);
    void moveToHead(Node* node);
    Node* removeTail();

public:
    LRUCache(int capacity);
    int get(int key);
    void put(int key, int value);
};
```

### 时间复杂度

- `get`: O(1)
- `put`: O(1)
- 空间复杂度: O(capacity)

## LFU 缓存（Least Frequently Used Cache）

### 实现原理

LFU 缓存根据访问频率淘汰使用频率最低的数据。当频率相同时，采用 LRU 策略作为 tie-breaker。

### 关键实现细节

- 使用三层结构：
  1. `key_table`: 存储 key 到 (value, frequency) 的映射
  2. `freq_table`: 存储 frequency 到 key 链表的映射（使用 LRU 顺序）
  3. `min_freq`: 记录当前最小频率
- 频率增加时：将 key 从旧频率链表移到新频率链表头部
- 淘汰时：从 `min_freq` 对应的链表尾部删除 key（最久未使用的最低频率元素）

### 代码结构

```cpp
class LFUCache {
private:
    struct CacheNode {
        int value, freq;
        CacheNode(int v, int f) : value(v), freq(f) {}
    };

    int capacity;
    int minFreq;
    std::unordered_map<int, CacheNode> keyTable;      // key -> {value, freq}
    std::unordered_map<int, std::list<int>> freqTable; // freq -> keys list
    std::unordered_map<int, std::list<int>::iterator> keyIter; // key -> iterator in freqTable

    void updateFreq(int key);

public:
    LFUCache(int capacity);
    int get(int key);
    void put(int key, int value);
};
```

### 时间复杂度

- `get`: O(1)
- `put`: O(1)
- 空间复杂度: O(capacity)

## 线程池（Thread Pool）

### 实现原理

线程池通过复用固定数量的工作线程来减少线程创建和销毁的开销。工作线程从任务队列中获取并执行任务。

### 关键实现细节

- 使用 `std::queue<std::function<void()>>` 存储待执行任务
- 使用 `std::mutex` 保护任务队列的并发访问
- 使用 `std::condition_variable` 实现线程等待和通知机制
- 工作线程在无任务时进入等待状态，有任务时被唤醒
- 提供优雅停机机制：设置停止标志后，等待所有任务完成再退出

### 代码结构

```cpp
class ThreadPool {
private:
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queueMutex;
    std::condition_variable condition;
    bool stop;

public:
    ThreadPool(size_t threads);
    template<class F>
    auto enqueue(F&& f) -> std::future<decltype(f())>;
    ~ThreadPool();
};
```

### 使用示例

```cpp
ThreadPool pool(4);
auto result = pool.enqueue([] {
    return std::accumulate(std::begin(vec), std::end(vec), 0.0);
});
double sum = result.get();
```

## 信号量（Semaphore）

### 实现原理

信号量是一种同步原语，用于控制对共享资源的访问。内部维护一个计数器，`acquire` 减少计数器（可能阻塞），`release` 增加计数器（可能唤醒等待线程）。

### 关键实现细节

- 使用 `std::mutex` 保护内部计数器
- 使用 `std::condition_variable` 实现等待/通知机制
- `acquire`：当计数器 > 0 时减计数器并返回；否则等待直到计数器 > 0
- `release`：增加计数器并通知一个等待的线程

### 代码结构

```cpp
class Semaphore {
private:
    std::mutex mtx;
    std::condition_variable cv;
    int count;

public:
    explicit Semaphore(int count_ = 0);
    void acquire();
    void release();
};
```

## 读写锁（Read-Write Lock）

### 实现原理

读写锁允许多个读线程同时访问共享资源，但写线程需要独占访问。适用于读多写少的场景。

### 关键实现细节

- 使用 `std::mutex` 保护内部状态
- 使用两个 `std::condition_variable`：读等待队列和写等待队列
- 跟踪活跃读取者数量、等待读取者数量、等待写取者数量和写入状态
- 读取锁：如果没有写入活动且没有等待的写入者，则授予读取锁
- 写入锁：只有在没有活跃读取者和写入者时才授予写入锁

### 代码结构

```cpp
class ReadWriteLock {
private:
    std::mutex mtx;
    std::condition_variable cv_read;
    std::condition_variable cv_write;
    int readers;           // 活跃读取者数量
    int waiting_readers;   // 等待读取者数量
    int waiting_writers;   // 等待写取者数量
    bool writing;          // 是否有写入活动

public:
    ReadWriteLock();
    void read_lock();
    void read_unlock();
    void write_lock();
    void write_unlock();
};
```

## 写优先读写锁（Writer-Preferring Read-Write Lock）

### 实现原理

写优先读写锁在有写入请求时优先授予写入锁，即使此时有活跃的读取者。这可以防止写入者饥饿，但可能导致读取者饥饿。

### 关键实现细节

- 与标准读写锁类似，但修改了读取锁的获取条件
- 读取锁只有在：没有写入活动、没有等待的写入者 且 没有等待的读取者（或采用其他策略防止饥饿）时才授予
- 写入锁逻辑保持不变：只有在没有活跃读取者和写入者时才授予

### 代码结构

```cpp
class ReadWriteLockWriterPref {
private:
    std::mutex mtx;
    std::condition_variable cv_read;
    std::condition_variable cv_write;
    int readers;
    int waiting_readers;
    int waiting_writers;
    bool writing;

public:
    ReadWriteLockWriterPref();
    void read_lock();
    void read_unlock();
    void write_lock();
    void write_unlock();
};
```

## 自旋锁（Test-and-Set Spinlock）

### 实现原理

自旋锁是一种忙等待锁，线程在获取锁失败时不进入睡眠状态，而是不断尝试获取锁。适用于锁持有时间非常短的场景。

### 关键实现细节

- 使用 `std::atomic<bool>` 作为锁状态标志
- `test_and_set` 操作：原子地将锁设置为已占用状态并返回旧值
- 获取锁：使用自旋循环反复调用 `test_and_set` 直到成功
- 释放锁：将锁状态设置为未占用

### 代码结构

```cpp
class TASSpinlock {
private:
    std::atomic<bool> flag;

public:
    TASSpinlock() : flag(false) {}
    void lock();
    void unlock();
};
```

### 性能特点

- 优点：实现简单，无上下文切换开销
- 缺点：在锁竞争激烈时会消耗大量 CPU 周期
- 适用场景：锁持有时间极短（如几个指令），且竞争不激烈

## 票据锁（Ticket Lock）

### 实现原理

票据锁是一种公平的自旋锁，通过发放排队号码来确保先来先服务的顺序，解决普通自旋锁可能出现的饥饿问题。

### 关键实现细节

- 使用两个 `std::atomic<size_t>`：
  - `next_ticket`: 下一个要发放的票号
  - `now_serving`: 当前正在服务的票号
- 获取锁：原子获取并递增 `next_ticket` 得到我的票号，然后自旋等待直到 `now_serving` 等于我的票号
- 释放锁：递增 `now_serving`

### 代码结构

```cpp
class TicketLock {
private:
    std::atomic<size_t> next_ticket;
    std::atomic<size_t> now_serving;

public:
    TicketLock() : next_ticket(0), now_serving(0) {}
    void lock();
    void unlock();
};
```

### 性能特点

- 保证公平性：先申请的线程先获得锁
- 相比 TAS 自旋锁：减少了缓存一致性流量（所有等待者都在同一个变量上自旋）
- 适用场景：需要公平性且锁持有时间短的场景

## 多生产者多消费者队列（MPMC Queue）

### 实现原理

MPMC（Multi-Producer Multi-Consumer）队列允许多个线程同时安全地生产和消费数据。采用环形缓冲区实现，通过头尾指针协调生产和消费。

### 关键实现细节

- 使用固定大小的数组作为环形缓冲区
- 使用两个 `std::atomic<size_t>`：`head_`（消费位置）和 `tail_`（生产位置）
- 生产者：检查是否有空间（`tail_ - head_< capacity`），如果有则写入并递增 `tail_`
- 消费者：检查是否有数据（`head_ < tail_`），如果有则读取并递增 `head_`
- 使用 `std::memory_order_acquire` 和 `std::memory_order_release` 确保内存可见性

### 代码结构

```cpp
template<typename T>
class MPMCQueue {
private:
    std::vector<T> buffer_;
    std::atomic<size_t> head_;
    std::atomic<size_t> tail_;
    const size_t capacity_;

public:
    explicit MPMCQueue(size_t capacity);
    bool enqueue(const T& item);
    bool dequeue(T& item);
};
```

### 性能特点

- 无锁实现：生产和消费操作不使用互斥锁
- 有界等待：队列满时生产者会失败返回（非阻塞）
- 适用场景：高并发场景中的事件处理、日志系统等

## 线程安全队列（Thread-Safe Queue）

### 实现原理

线程安全队列在标准队列基础上添加同步机制，确保多线程环境下的安全访问。与 MPMC 队列不同，该实现使用互斥锁和条件变量提供阻塞式接口。

### 关键实现细节

- 使用 `std::queue<T>` 作为底层容器
- 使用 `std::mutex` 保护队列访问
- 使用 `std::condition_variable` 实现不等待时的线程休眠和唤醒
- `push`：将元素加入队列后通知一个等待的消费者
- `pop`：如果队列为空则等待，直到有元素可用后移除并返回队首元素
- 提供 `try_pop` 非阻塞版本

### 代码结构

```cpp
template<typename T>
class ThreadSafeQueue {
private:
    std::queue<T> queue_;
    std::mutex mutex_;
    std::condition_variable cond_;

public:
    void push(const T& value);
    bool try_pop(T& value);
    void wait_and_pop(T& value);
    bool empty() const;
};
```

### 使用场景

- 生产者-消费者模式
- 任务队列（如线程池的任务分发）
- 日志系统
- 事件处理系统

## 并发原语比较

| 原语 | 实现方式 | 公平性 | 适用场景 | 性能特点 |
|------|----------|--------|----------|----------|
| TAS 自旋锁 | 原子测试设置 | 不公平 | 锁持有时间极短 | 简单，但可能忙等待浪费 CPU |
| 票据锁 | 排队号码 | 公平 | 需要公平性且锁时间短 | 减少缓存一致性流量 |
| 互斥锁（在其他实现中） | 互斥量+条件变量 | 取决于调度器 | 一般场景 | 有上下文切换开销但CPU利用率高 |
| 信号量 | 计数器+条件变量 | 取决于调度器 | 资源计数控制 | 通用同步原语 |
| 读写锁 | 状态+条件变量 | 读优先/写优先变体 | 读多写少场景 | 允许并发读取 |
| 无锁队列（MPMC） | 原子指针 | 不保证 | 高并发生产消费 | 无阻塞，但可能失败 |
| 阻塞队列（线程安全队列） | 互斥量+条件变量 | 取决于调度器 | 需要等待的生产者-消费者 | 简单可靠，但可能线程切换 |

## 设计模式与最佳实践

### RAII 资源管理

所有并发原语均遵循 RAII 原则：
- 互斥锁使用 `std::lock_guard` 或 `std::unique_lock` 进行自动加锁/解锁
- 条件变量与互斥锁配合使用，确保正确的等待/通知语义

### 异常安全

- 所有操作在可能抛异常的点上都考虑了异常安全性
- 使用 RAII 包装器确保资源不会泄漏
- 临界区中的操作尽量不抛异常，或使用 noexcept 声明

### 内存顺序

- 在无锁实现（如 MPMC 队列）中，显式指定了适当的内存顺序（`memory_order_acquire/release`）
- 避免过度使用 `memory_order_seq_cst` 以获得更好性能
- 依赖于正确的同步原语来建立 happens-before 关系

### 可扩展性

- 线程池使用模板实现，支持任意可调用对象
- 队列实现为模板类，支持任意可拷贝/移动类型
- 缓存实现使用整数键值，但可轻松修改为模板以支持泛型

## 性能考量

### 缓存算法

- LRU 和 LFU 均提供 O(1) 时间复杂度
- LRU 实现更简单，LFU 需要额外维护频率信息但能更好地适应访问模式变化
- 两者空间复杂度均为 O(capacity)

### 并发原语

- 自旋锁（TAS、票据）：在锁竞争低且持有时间短时性能优于互斥锁（避免上下文切换）
- 互斥锁+条件变量：在锁竞争激烈或持有时间较长时更高效（让出CPU）
- 无锁队列：在高并发场景下避免锁竞争，但需要处理失败情况
- 读写锁：在读多写少场景下可显著提升并发度

### 选择建议

1. **锁选择**：
   - 极短临界区且竞争不激烈：考虑票据锁（公平）或 TAS 自旋锁（简单）
   - 一般场景：使用标准互斥锁
   - 读多写少：使用读写锁
   - 需要资源计数：使用信号量

2. **队列选择**：
   - 需要阻塞等待：使用线程安全队列
   - 高并发且可接受偶尔失败：使用 MPMC 队列
   - 需要优先级或特殊调度：考虑其他专用队列

3. **缓存选择**：
   - 访问有 locality：LRU
   - 访问频率有明显差异且不变：LFU
   - 简单实现优先：LRU

## 结论

本项目中的并发原语和经典算法实现展示了现代 C++ 在并发编程中的强大能力。通过结合 RAII、模板、原子操作和标准库并发原语，这些实现既具有生产级别的质量，又便于学习和理解核心概念。每个实现都经过精心设计，以平衡正确性、性能和可读性，适用于面试准备和实际项目中的学习参考。

这些实现不仅展示了如何构建特定的并发原语，还体现了更广泛的并发编程原则：
- 最小化临界区
- 正确使用内存顺序
- 避免活锁和死锁
- 公平性考虑
- 错误处理和异常安全
- 性能与复杂度的权衡

通过研究这些实现，开发者可以深入理解并发编程的基础概念，并将这些知识应用于构建更复杂的并发系统。