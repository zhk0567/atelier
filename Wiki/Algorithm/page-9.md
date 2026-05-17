<!-- wiki_page_id: page-9 -->

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [cpp/problems/notes.md](https://github.com/zhk0567/Algorithm/blob/main/cpp/problems/notes.md)
- [cpp/problems/hot100/notes.md](https://github.com/zhk0567/Algorithm/blob/main/cpp/problems/hot100/notes.md)
- [cpp/problems/leetcode/0001_two_sum/solution.cpp](https://github.com/zhk0567/Algorithm/blob/main/cpp/problems/leetcode/0001_two_sum/solution.cpp)</details>

# LeetCode 题解与刷题指南

## 项目结构概览

本仓库以 C++ 为主要实现语言，系统地收录了 LeetCode 题目的解题代码与学习笔记。代码组织遵循以下约定：

- 每道题目对应一个独立的目录，命名格式为 `{题号}_{题目名称}`（如 `0001_two_sum`）
- 每个题目目录下包含 `solution.cpp` 实现文件
- 题目笔记统一存放在 `notes.md` 文件中，按难度和主题分类

## 刷题路线建议

根据仓库中的 `hot100/notes.md`，推荐以下学习路径：

### 基础阶段
1. **数组与字符串**：掌握双指针、滑动窗口技巧
2. **链表**：熟悉快慢指针、原地修改技术
3. **哈希表**：理解时间空间权衡，重点掌握一遍哈希

### 提高阶段
1. **树与图**：掌握递归遍历、BFS/DFS 应用
2. **动态规划**：从状态定义入手，练习背包类、序列类问题
3. **堆与栈**：掌握优先队列应用场景

### 冲刺阶段
1. **高频题目**：重点刷取 Hot 100 题单
2. **时间复杂度分析**：每道题练习说出最优解的时间空间复杂度
3. **举一反三**：变形题目练习，培养举一反三能力

## 核心算法模板

### 数组双指针技巧
```cpp
// 左右指针
int left = 0, right = n - 1;
while (left < right) {
    // 处理逻辑
    if (condition) left++;
    else right--;
}

// 快慢指针
int slow = 0;
for (int fast = 0; fast < n; fast++) {
    if (condition) {
        // 处理逻辑
        nums[slow++] = nums[fast];
    }
}
```

### 哈希表应用
```cpp
// 一遍哈希
unordered_map<int, int> map;
for (int i = 0; i < nums.size(); i++) {
    int complement = target - nums[i];
    if (map.find(complement) != map.end()) {
        // 找到解
        return {map[complement], i};
    }
    map[nums[i]] = i;
}
```

### 链表操作
```cpp
// 快慢指针查找中间节点
ListNode* slow = head;
ListNode* fast = head;
while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
}

// 原地反转链表
ListNode* prev = nullptr;
ListNode* curr = head;
while (curr) {
    ListNode* nextTemp = curr->next;
    curr->next = prev;
    prev = curr;
    curr = nextTemp;
}
```

## 题目分类与解题策略

### 简单难度题目
以 `0001_two_sum` 为例，解题思路如下：
- **暴力解法**：两层循环 O(n²) 时间复杂度
- **优化方案**：使用哈希表将时间复杂度降至 O(n)
- **关键点**：空间换时间，建立值到索引的映射

### 中等难度题目
参考 Hot 100 题单中的典型题型：
- **滑动窗口**：用于子数组/子字符串问题
- **二分查找**：在有序数组中查找特定元素
- **栈的应用**：有效括号、每日温度等问题

### 困难难度题目
通常需要综合运用多种技巧：
- **动态规划 + 状态压缩**
- **贪心算法 + 堆优化**
- **图论算法 + 剪枝技巧**

## 代码质量与规范

### 命名约定
- 变量命名采用驼峰式（camelCase）
- 常量使用全大写加下划线（UPPER_SNAKE_CASE）
- 函数命名采用动词短语，如 `findTargetSumWays`

### 注释规范
- 复杂算法前添加简要说明
- 关键变量说明其含义
- 特殊处理逻辑添加注释说明原因

### 错误处理
- 输入参数合法性检查
- 边界条件特殊处理
- 异常情况的优雅降级

## 学习资源与进阶建议

### 必读资料
1. 《算法导论》 - 基础算法理论
2. 《编程珠玑》 - 算法设计思路
3. LeetCode 官方题解 - 不同语言实现参考

### 练习平台推荐
- LeetCode 中文官网：题目分类完整，讨论区活跃
- 现在编程（NowCoder）：校招真题较多
- CodeTop：高频面试题集合

### 进阶方向
1. **算法竞赛**：参考《挑战程序设计竞赛》
2. **系统设计**：学习分布式系统原理
3. **性能优化**：深入理解 CPU 缓存、内存对齐等知识

## 常见问题解答

### Q：如何快速定位题目解法？
A：仓库采用 `{题号}_{题目名称}` 的目录命名方式，可直接通过题号查找。例如想看两数之和的解法，进入 `cpp/problems/leetcode/0001_two_sum/` 目录。

### Q：代码是否支持最新 C++ 标准？
A：代码主要使用 C++11 及以上特性，如 auto 类型推导、范围for循环、lambda 表达式等。

### Q：如何贡献自己的题解？
A： fork 本仓库，在 `cpp/problems/leetcode/` 下创建新的题目目录，遵循现有目录结构和命名规范提交 Pull Request。

### Q：刷题过程中遇到瓶颈怎么办？
A：建议：
1. 先看官方题解理解思路
2. 不看代码尝试自己实现
3. 对比实现差异，总结不足
4. 相似题目进行变形练习

## 更新日志

- 2024-01-15：初始化仓库结构，添加基础题目解法
- 2024-02-01：完成 Hot 100 前 50 题的解题笔记
- 2024-03-10：添加算法模板和刷题建议章节
- 2024-04-20：更新 C++17 特性使用示例</details>