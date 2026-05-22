---
title: "题单与刷题归档 · 总览"
series: algorithm
category: Problems
topic_path: problems
guide_toc: problem-index
guide_tier: medium
status: published
date: 2026-05-22
tags: [Problems, LeetCode, Index]
---

# 题单与刷题归档 · 总览

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

## 导读

`problems/` 收纳 **LeetCode 题解树** 与 **题单索引**（Hot 100、剑指 Offer、CodeTop、牛客、洛谷等）。atelier **不为** 每道题建博文；本页 `prob-` 说明如何用工单导航到 `leetcode/<四位编号>_<slug>/`，并链到 **5** 篇题单指南。

## 预备知识

> **预备知识**：会运行 `solution.py`；理解题单与题解目录分离。

## Study 仓库对照

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm'
Get-Content -LiteralPath 'python\problems\notes.md' -Encoding utf8
```

| 子目录 | 类型 | 指南 |
|--------|------|------|
| `leetcode/` | 单题实现 | 无独立博文，用索引进入 |
| `hot100/` | 热题表 | [prob-hot100](/blog/prob-hot100) |
| `offer/` | 剑指 | [prob-offer](/blog/prob-offer) |
| `codetop/` | CodeTop | [prob-codetop](/blog/prob-codetop) |
| `nowcoder/` | 牛客 | [prob-nowcoder](/blog/prob-nowcoder) |
| `luogu/` | 洛谷 | [prob-luogu](/blog/prob-luogu) |

## 基础篇

### 题单用途

索引表回答「下一道刷哪题」；`notes.md` + `solution.py` 回答「怎么做」。

### 与 Study 目录映射

命名：`0001_two_sum`；SQL 题用 `solution.sql`。题单行内相对路径 `../leetcode/...`。

### 如何使用题解树

1. 选题单页 → 2. 进 leetcode 子目录 → 3. 读 notes 跑 solution → 4. 对照 `algo-*`/`ds-*` 范式。

### 维护与对齐

改题单时同步 Python/C++ 索引；atelier 题单博文只扩写用法，不复制全表。

## Python 实现

```python
# 节选：0001_two_sum/solution.py
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\python\problems\leetcode\0001_two_sum'
python solution.py
```

## C++ 实现

```cpp
// 节选：0001_two_sum/solution.cpp
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int,int> seen;
    for (int i = 0; i < (int)nums.size(); ++i) {
        int need = target - nums[i];
        auto it = seen.find(need);
        if (it != seen.end()) return {it->second, i};
        seen[nums[i]] = i;
    }
    return {};
}
```

```powershell
Set-Location -LiteralPath 'F:\Study\Algorithm\cpp\problems\leetcode\0001_two_sum'
g++ -std=c++17 -O2 -I ..\..\include -o run.exe solution.cpp
.\run.exe
```

## 练习与延伸

按 [prob-hot100](/blog/prob-hot100) 周计划；Offer/CodeTop 作二轮查漏。

## 学习路径

Hot 100 → Offer 30 → CodeTop 30 → 专项弱项回范式指南。

## 延伸阅读

- [prob-codetop](/blog/prob-codetop)
- [prob-hot100](/blog/prob-hot100)
- [prob-luogu](/blog/prob-luogu)
- [prob-nowcoder](/blog/prob-nowcoder)
- [prob-offer](/blog/prob-offer)


**深度补充：单题边界**

专题博文在 algorithm-guides；单题只在 Study。


**深度补充：独占题**

Offer 少数无 leetcode 目录的题，见 prob-offer 说明。


**深度补充：导航复盘 3**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 4**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 5**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 6**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 7**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 8**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 9**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 10**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 11**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 12**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 13**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 14**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 15**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 16**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 17**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 18**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 19**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 20**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 21**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 22**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 23**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 24**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 25**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 26**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 27**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 28**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 29**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 30**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 31**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 32**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 33**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 34**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 35**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 36**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 37**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 38**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 39**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 40**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 41**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 42**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 43**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 44**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 45**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 46**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 47**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 48**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 49**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 50**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 51**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 52**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 53**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 54**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 55**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 56**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 57**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 58**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 59**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 60**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 61**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 62**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 63**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 64**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 65**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 66**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 67**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 68**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 69**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 70**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 71**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 72**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 73**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 74**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 75**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 76**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 77**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 78**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 79**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 80**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 81**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 82**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 83**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 84**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 85**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 86**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 87**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 88**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 89**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 90**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 91**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 92**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 93**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 94**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 95**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 96**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 97**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 98**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 99**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 100**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 101**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 102**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 103**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 104**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 105**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 106**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 107**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 108**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 109**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 110**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 111**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 112**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 113**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 114**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 115**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 116**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 117**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 118**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 119**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 120**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 121**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 122**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 123**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 124**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 125**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 126**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 127**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 128**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 129**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 130**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 131**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 132**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 133**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 134**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 135**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 136**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 137**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 138**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。


**深度补充：导航复盘 139**

以 prob- 为入口：在 Study 打开对应 notes.md，选一篇已发布的 atelier 子指南 对照阅读，再跑通一个子目录脚本；记录「子路径 → 站内 slug → 代表题号」三列卡片。
