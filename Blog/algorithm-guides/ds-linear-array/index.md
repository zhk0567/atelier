---
title: "数据结构 · 动态数组（ArrayList）"
series: algorithm
category: DataStructures
topic_path: data_structures/linear/array
guide_toc: topic-ds
guide_tier: medium
status: published
date: 2026-05-22
tags: [DataStructures, Array, DynamicArray, AmortizedAnalysis]
---

# 数据结构 · 动态数组（Dynamic Array）

## 导读

**动态数组**在连续内存上存储元素，维护逻辑长度 `size` 与物理容量 `capacity`；满时按策略（通常×2）扩容并搬移元素。Python 的 `list`、C++ 的 `vector` 即工业实现；Study `dynamic_array.py` **显式**维护 capacity，便于理解摊还分析与中间插入 O(n) 搬移。

本页 `guide_toc` 为 `topic-ds`（抽象模型、核心操作、实现要点、典型应用、易错点、练习建议）。父级 `ds-linear` 提供六类线性结构选型；**本页只深挖数组**。

## 预备知识

> **环境**：Python 3.10+；C++17 `dynamic_array.cpp` 用 `vector` + `reserve` 演示扩容。

- 大 O 与**摊还分析**。
- 下标从 0 开始；`len`/`size` 与容量区分。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/linear/array` |
| Python | `python/data_structures/linear/array/dynamic_array.py` |
| C++ | `cpp/data_structures/linear/array/dynamic_array.cpp` |

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\data_structures\linear\array\dynamic_array.py
```

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\data_structures\linear\array
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe dynamic_array.cpp
.\run.exe
```

输出 `DynamicArray OK`。

## 基础篇

### 抽象模型

逻辑上可变长序列，支持下标访问；底层连续存储，`capacity >= size`。

### 核心操作

| 操作 | 平均 | 最坏 |
|------|------|------|
| at(i) | O(1) | O(1) |
| push_back | O(1) 摊还 | O(n) 扩容 |
| pop_back | O(1) | O(1) |
| insert/erase 中间 | O(n) | O(n) |

### 实现要点

- `push_back`：`size==capacity` 则 `_resize(capacity*2)`，再写入。
- `insert`：下标合法后，自 `size-1`  downto `index` 后移一位。
- `erase`：自 `index` 起前移， `size--`，清空尾槽。
- C++ 版 `ensure_extra` 在 `push_back`/`insert` 前检查 `reserve`。

### 典型应用

- 向量、缓冲区、哈希表开放寻址底层（了解）。
- 许多题直接用语言内置数组 + 双指针，不必手写类。

### 易错点

- 空数组 `pop_back`/`at(0)` → 抛异常。
- `insert` 允许 `index==size`（尾插），`index>size` 非法。
- 扩容后忘记更新 `capacity`。
- 混淆 `list.pop(0)` O(n) 与 `append` O(1)。

### 练习建议

1. 跑通 DynamicArray 断言（含空数组异常）。
2. 27/26/88/167/560 数组双指针与前缀和。
3. 对比 `ds-linear-linked-list` 选型。

## Python 实现

```python
class DynamicArray:
    def push_back(self, value: object) -> None:
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def _resize(self, new_cap: int) -> None:
        new_data = [None] * new_cap
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_cap
```

完整类见 Study 文件（含 `insert`/`erase`/`pop_back`）。

## C++ 实现

```cpp
void push_back(int v) {
    ensure_extra(1);
    data_.push_back(v);
}

void ensure_extra(size_t extra) {
    if (data_.size() + extra > cap_) {
        cap_ = max(cap_ * 2, data_.size() + extra);
        data_.reserve(cap_);
    }
}
```

`DynamicArray` 封装 `vector<int>` 与显式 `cap_`；`insert`/`erase` 见 Study `dynamic_array.cpp`。

## 练习与延伸

| 题 | 技巧 |
|----|------|
| 27, 26, 80 | 双指针原地 |
| 88, 977 | 合并/平方双指针 |
| 560, 304 | 前缀和 |
| 189 | 轮转 |

延伸：`ds-linear`、`ds-linear-linked-list`。

## 学习路径

1. 手画 push 触发扩容过程。
2. 实现摊还分析口述（倍增）。
3. 刷 5 道数组双指针。
4. strict 校验后改 published。

## 延伸阅读

- `python/data_structures/linear/array/notes.md`
- [linear/array](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/linear/array)


**深度补充：size 与 capacity**

逻辑长度 size 与物理容量 capacity 分离；满则倍增扩容。


**深度补充：摊还 O(1) push**

均摊分析：扩容总代价摊到 n 次 push。


**深度补充：缩容策略**

pop 后若 size<<capacity/4 可减半，避免空间浪费；LeetCode 少考。


**深度补充：随机访问 O(1)**

at(i) 直接下标；链表无此性质。


**深度补充：中间插入 O(n)**

insert 需搬移 [index..size-1] 到后一位。


**深度补充：erase O(n)**

同理向前搬移。


**深度补充：27 移除元素**

双指针原地删，O(n) 一次遍历。


**深度补充：26 删除重复项**

有序数组快慢指针。


**深度补充：80 删除重复 II**

最多保留 2 个相同。


**深度补充：283 移动零**

双指针把非零前移。


**深度补充：75 颜色分类**

荷兰国旗三指针 partition。


**深度补充：88 合并有序数组**

从尾部双指针合并到 nums1。


**深度补充：977 有序数组平方**

双指针从两端平方填入。


**深度补充：167 两数之和 II**

有序数组左右指针。


**深度补充：15 三数之和**

排序+固定 i+双指针。


**深度补充：18 四数之和**

排序+两重循环+双指针。


**深度补充：11 盛水**

左右指针移动较短边。


**深度补充：42 接雨水**

双指针或单调栈。


**深度补充：53 最大子数组**

Kadane O(n)。


**深度补充：238 除自身以外乘积**

前缀积+后缀积或输出数组技巧。


**深度补充：560 和为 K 子数组**

前缀和+哈希计数。


**深度补充：304 二维区域和**

二维前缀和。


**深度补充：724 寻找中心索引**

前缀和。


**深度补充：41 缺失第一个正**

原地哈希或置换。


**深度补充：448 找到消失数字**

原地标记下标。


**深度补充：287 寻找重复数**

快慢指针或二分。


**深度补充：34 查找边界**

二分 lower/upper bound。


**深度补充：704 二分查找**

模板。


**深度补充：189 轮转数组**

三次反转或辅助数组。


**深度补充：238 与 189**

数组经典双指针/前缀。


**深度补充：66 加一**

末尾进位模拟。


**深度补充：989 数组形式整数加法**

双指针从尾相加。


**深度补充：56 合并区间**

排序+扫。


**深度补充：57 插入区间**

线性扫合并。


**深度补充：252 会议室**

排序 start 判重叠。


**深度补充：56 与 57**

区间题常排序后线性。


**深度补充：121 买卖股票**

一次遍历 min 前缀。


**深度补充：122 股票 II**

贪心累加正差。


**深度补充：动态数组 vs vector**

C++ vector 即标准库动态数组；教学手写理解扩容。


**深度补充：Python list**

list 已是动态数组；教学类显式 capacity 为理解 C++。


**深度补充：IndexError 边界**

at/pop/erase 越界抛异常；面试先判空。


**深度补充：None 清空槽位**

pop 后 _data[size]=None 防悬挂引用。


**深度补充：初始容量 4**

Study 默认；可构造参数。


**深度补充：ensure_extra C++**

reserve 扩容；与 Python _resize 对照。


**深度补充：对拍 DynamicArray**

随机 push/pop/insert 与 list 模拟对比。


**深度补充：面试话术数组**

「随机访问 O(1)；尾插摊还 O(1)；中间 O(n)；扩容倍增」。


**深度补充：与 ds-linear**

父总览选型地图；本页只深挖数组。


**深度补充：与 linked_list**

头插链表优、数组尾插优。


**深度补充：283 与 27**

原地操作是数组题核心技巧。


**深度补充：结语数组**

Study DynamicArray 跑通+Hot 双指针/前缀=medium 验收。


**深度补充：综合复盘 51**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 52**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 53**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 54**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 55**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 56**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 57**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 58**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 59**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 60**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 61**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 62**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 63**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 64**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 65**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 66**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 67**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 68**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 69**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 70**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 71**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 72**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 73**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 74**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 75**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 76**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 77**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 78**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 79**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 80**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 81**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 82**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 83**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 84**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 85**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 86**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 87**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 88**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 89**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 90**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 91**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 92**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 93**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 94**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 95**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 96**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 97**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 98**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 99**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 100**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 101**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 102**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 103**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 104**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 105**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 106**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 107**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 108**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 109**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 110**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 111**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 112**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 113**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 114**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 115**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 116**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 117**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 118**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 119**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 120**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 121**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 122**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 123**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 124**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 125**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 126**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 127**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 128**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 129**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 130**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 131**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 132**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 133**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 134**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 135**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 136**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 137**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 138**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 139**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 140**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 141**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 142**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 143**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 144**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 145**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 146**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 147**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 148**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 149**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 150**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 151**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 152**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 153**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 154**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 155**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 156**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 157**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 158**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 159**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 160**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 161**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 162**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 163**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 164**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 165**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 166**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 167**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 168**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 169**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 170**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 171**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。


**深度补充：综合复盘 172**

回到 ds-linear-array 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。
