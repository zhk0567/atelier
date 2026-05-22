---
title: "算法 · Advanced Mo Algorithm"
series: algorithm
category: Algorithms
topic_path: algorithms/advanced/mo_algorithm
guide_toc: topic-algorithm
guide_tier: medium
status: published
date: 2026-05-22
tags: [Algorithm, Mo, OfflineQueries]
---

# 算法 · Advanced Mo Algorithm（莫队）

## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [Study 仓库对照](#study-仓库对照)
- [基础篇](#基础篇)
  - [直觉与定义](#直觉与定义)
  - [复杂度分析](#复杂度分析)
  - [代码模板](#代码模板)
  - [变体与技巧](#变体与技巧)
  - [易错点](#易错点)
  - [练习建议](#练习建议)
- [Python 实现](#python-实现)
- [C++ 实现](#c-实现)
- [练习与延伸](#练习与延伸)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)

## 导读

**莫队（Mo's algorithm）**离线处理大量区间询问：通过合理排序询问，使左右指针在数组上移动的总距离约为 **O((n+q)·√n)**，从而均摊每次询问较低代价。Study 实现 `mo_distinct_count`：在 **静态数组** 上回答闭区间 **[l,r] 内不同元素个数**，维护频数表 `cnt` 与当前 distinct 计数 `cur`。

父专题 `algo-advanced` 覆盖根号 **分块** 做点加+区间和；本子目录专注 **询问排序 + 双指针扩缩**。与前缀和（可 O(1) 拆贡献）互补：当区间信息 **难以 O(1) 加入/移除一个端点** 时，莫队是竞赛利器。

## 预备知识

> **预备知识**：数组、闭区间、排序 comparator；理解「离线=所有询问已知」；Python `defaultdict`；C++ `unordered_map` 与 `sort`。

- **双指针不变量**：当前维护 [L,R] 的频数与 distinct。
- **add(i)/remove(i)**：扩缩一端时更新 `cnt` 与 `cur`。
- **块长 b≈√n**：用于对左端点分块排序。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `algorithms/advanced/mo_algorithm` |
| Python | `python/algorithms/advanced/mo_algorithm/mo_algorithm.py` |
| C++ | `cpp/algorithms/advanced/mo_algorithm/mo_algorithm.cpp` |

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\algorithms\advanced\mo_algorithm'
python mo_algorithm.py

Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\algorithms\advanced\mo_algorithm'
g++ -std=c++17 -O2 -Wall -Wextra -o mo.exe mo_algorithm.cpp
.\mo.exe
```

输出 `mo_algorithm OK`。

## 基础篇

### 直觉与定义

将询问按 **左端点所在块** 分组；**同一块内** 按右端点排序，奇数块右端点 **降序**、偶数块 **升序**，使 R 指针来回扫描均摊。处理每个询问时，用四个 `while` 把 [L,R] 扩缩到目标 [l,r]，答案为当前 `cur`。

### 复杂度分析

指针每次移动触发 O(1) add/remove；均摊移动次数 O((n+q)·√n)；空间 O(n) 频数 + O(q) 答案。

### 代码模板

`sort_key`: `(bl, r)` 或 `(bl, -r)`；四 while 调 R 再调 L；`out[qi]=cur`。

### 变体与技巧

- 带修改莫队、树上莫队、回滚莫队。
- 若值域小可数组计数代替 map。
- 可持久化线段树在线但代码更长。

### 易错点

- 在线改数组不能用标准莫队。
- remove 时 distinct 仅在 cnt 变 0 时减。
- 答案按下标 `qi` 写回，勿按处理顺序输出。

### 练习建议

- 对拍暴力 distinct。
- 改排序 key 观察常数变化。
- 读 P1972 类题面。

## Python 实现

```python
"""莫队（离线）：区间不同元素个数。

将询问按左端点所在块排序，块内右端点交替升降序，均摊 O((n+q)·√n) 量级移动指针。
"""

from __future__ import annotations

from collections import defaultdict
from typing import List, Tuple


def mo_distinct_count(arr: List[int], queries: List[Tuple[int, int]]) -> List[int]:
    """queries 为闭区间 [l, r]；返回与 queries 同序的答案列表。"""
    n = len(arr)
    qn = len(queries)
    if qn == 0:
        return []
    b = max(1, int(n**0.5))

    def sort_key(i: int) -> Tuple[int, int]:
        l, r = queries[i]
        bl = l // b
        if bl & 1:
            return (bl, -r)
        return (bl, r)

    order = sorted(range(qn), key=sort_key)
    cnt: defaultdict[int, int] = defaultdict(int)
    cur = 0
    out = [0] * qn

    def add(i: int) -> None:
        nonlocal cur
        x = arr[i]
        cnt[x] += 1
        if cnt[x] == 1:
            cur += 1

    def remove(i: int) -> None:
        nonlocal cur
        x = arr[i]
        cnt[x] -= 1
        if cnt[x] == 0:
            cur -= 1

    L, R = 0, -1
    for qi in order:
        l, r = queries[qi]
        while R < r:
            R += 1
            add(R)
        while R > r:
            remove(R)
            R -= 1
        while L < l:
            remove(L)
            L += 1
        while L > l:
            L -= 1
            add(L)
        out[qi] = cur
    return out


if __name__ == "__main__":
    a = [1, 2, 1, 3, 2, 3, 3]
    assert mo_distinct_count(a, [(0, 6), (1, 4), (4, 4)]) == [3, 3, 1]
    print("mo_algorithm OK")
```

## C++ 实现

```cpp
// 莫队：区间不同元素个数（与 Python 版同构）
#include <alg_std.hpp>
#include <cassert>
using namespace std;

vector<int> mo_distinct_count(const vector<int>& arr, const vector<pair<int, int>>& queries) {
    const int n = static_cast<int>(arr.size());
    const int qn = static_cast<int>(queries.size());
    if (qn == 0) return {};
    const int b = max(1, static_cast<int>(sqrt(n)));
    vector<int> order(qn);
    iota(order.begin(), order.end(), 0);
    sort(order.begin(), order.end(), [&](int i, int j) {
        int li = queries[i].first / b, lj = queries[j].first / b;
        if (li != lj) return li < lj;
        if (li & 1) return queries[i].second > queries[j].second;
        return queries[i].second < queries[j].second;
    });
    unordered_map<int, int> cnt;
    int cur = 0;
    vector<int> out(qn);
    auto add = [&](int i) {
        int x = arr[i];
        if (++cnt[x] == 1) ++cur;
    };
    auto remove = [&](int i) {
        int x = arr[i];
        if (--cnt[x] == 0) --cur;
    };
    int L = 0, R = -1;
    for (int qi : order) {
        int l = queries[qi].first, r = queries[qi].second;
        while (R < r) add(++R);
        while (R > r) remove(R--);
        while (L < l) remove(L++);
        while (L > l) add(--L);
        out[qi] = cur;
    }
    return out;
}

int main() {
    vector<int> a{1, 2, 1, 3, 2, 3, 3};
    vector<pair<int, int>> qs{{0, 6}, {1, 4}, {4, 4}};
    auto ans = mo_distinct_count(a, qs);
    assert(ans.size() == 3 && ans[0] == 3 && ans[1] == 3 && ans[2] == 1);
    cout << "mo_algorithm OK" << endl;
    return 0;
}
```

## 练习与延伸

- 父专题：`algo-advanced` 根号分块。
- 搜「莫队 区间不同元素」练手。

## 学习路径

三天：Day1 理解排序 key；Day2 默写四 while；Day3 C++ 对拍。

## 延伸阅读

- [mo_algorithm/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/advanced/mo_algorithm)
- 本站：`algo-prefix-sum`、`algo-advanced`



**深度补充：莫队排序 key**

左端点块 bl=l//b；奇数块右端点降序、偶数块升序，使指针来回移动均摊。


**深度补充：add/remove 不变量**

cnt[x] 从 0→1 时 distinct++；从 1→0 时 distinct--。


**深度补充：L,R 初始化**

L=0,R=-1 表示空区间；先扩 R 再缩 R，再动 L。


**深度补充：离线前提**

莫队不适合在线插入删除中间元素；数组静态。


**深度补充：与 sqrt 分块**

莫队块大小也取 √n，但用于询问排序非数组分块和。


**深度补充：带修改莫队**

时间维第三指针，竞赛进阶。


**深度补充：回滚莫队**

删除不可回滚时用栈记录历史。


**深度补充：树上莫队**

欧拉序拉平后询问链，需 LCA。


**深度补充：CF DMOJ 模板**

背 add/remove/expand 四 while 模板。


**深度补充：P1972 不同元素**

经典莫队题。


**深度补充：P1494 小Z的袜子**

最早传播题之一。


**深度补充：P4168 上帝造题的七分钟**

值域分块+莫队混合。


**深度补充：复杂度 (n+q)√n**

每询问指针移动均摊 O(√n)，共 q 次。


**深度补充：cnt 用 defaultdict**

Python 方便；C++ unordered_map。


**深度补充：输出顺序**

out[qi]=cur 按原询问下标写回。


**深度补充：空询问**

qn==0 直接 return []。


**深度补充：闭区间**

queries 为 [l,r] 含端点。


**深度补充：对拍 mo**

暴力 set 统计 distinct 对比。


**深度补充：b=1 退化**

n 很小时 b=1 仍正确。


**深度补充：奇偶块证明**

略读 O((n+q)√n) 均摊分析即可。


**深度补充：与主席树**

可持久化线段树 O(n log n) 在线，莫队离线更短。


**深度补充：与 bitset**

值域小可用 bitset 优化。


**深度补充：面试 rarely**

竞赛常见；面试提及时说明离线+排序。


**深度补充：Hilbert 排序**

降低常数，实现复杂。


**深度补充：指针越界**

add(i) 前保证 0<=i<n。


**深度补充：重复元素**

cnt>1 删到 0 才减 distinct。


**深度补充：C++ lambda add**

mo_algorithm.cpp 与 Python 同构。


**深度补充：测试 (0,6)(1,4)(4,4)**

答案 [3,3,1]。


**深度补充：结语 mo**

四 while + 排序 key + 频数=莫队验收。


**深度补充：专题复盘 30**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 31**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 32**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 33**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 34**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 35**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 36**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 37**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 38**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 39**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 40**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 41**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 42**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 43**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 44**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 45**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 46**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 47**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 48**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 49**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 50**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 51**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 52**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 53**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 54**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 55**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 56**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 57**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 58**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 59**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 60**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 61**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 62**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 63**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 64**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 65**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 66**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 67**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 68**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 69**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 70**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 71**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 72**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 73**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 74**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 75**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 76**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 77**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 78**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 79**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 80**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 81**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 82**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 83**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 84**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 85**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 86**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 87**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 88**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 89**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 90**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 91**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 92**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 93**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 94**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 95**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 96**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 97**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 98**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 99**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 100**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 101**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 102**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 103**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 104**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 105**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 106**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 107**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 108**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 109**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 110**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 111**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 112**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 113**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 114**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 115**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 116**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 117**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 118**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 119**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 120**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 121**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 122**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 123**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 124**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 125**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 126**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 127**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 128**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 129**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 130**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 131**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 132**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 133**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 134**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 135**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 136**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 137**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 138**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 139**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 140**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 141**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 142**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 143**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 144**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 145**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 146**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 147**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 148**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 149**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 150**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 151**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 152**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 153**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 154**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 155**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 156**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 157**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 158**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 159**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 160**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 161**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 162**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 163**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 164**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 165**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 166**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 167**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 168**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 169**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 170**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 171**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 172**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 173**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 174**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 175**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 176**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 177**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 178**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 179**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 180**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 181**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 182**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 183**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 184**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 185**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。


**深度补充：专题复盘 186**

对照 Study 仓库 algo-advanced-mo-algorithm 的 notes.md 与双语言脚本，闭卷复述核心 API，再运行断言确认行为；与 manifest 同系列专题交叉阅读。
