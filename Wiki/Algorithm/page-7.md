<!-- wiki_page_id: page-7 -->

# 高级算法专题

## 动态规划

### 线性动态规划

线性动态规划问题通常涉及一维数组，状态转移方程仅依赖于前一个或几个前的状态。典型问题包括斐波那契数列、股票买卖等。

#### 核心思想
- 定义状态 `dp[i]` 表示前 `i` 个元素的最优解
- 状态转移方程：`dp[i] = f(dp[i-1], dp[i-2], ...)`
- 初始条件：`dp[0]`, `dp[1]` 等基础情况

#### 示例代码
```cpp
// 斐波那契数列
int fib(int n) {
    if (n <= 1) return n;
    vector<int> dp(n + 1);
    dp[0] = 0;
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    return dp[n];
}
```

### 区间动态规划

区间动态规划用于解决区间内的最优化问题，如矩阵链乘法、回文串划分等。状态通常定义为 `dp[l][r]` 表示区间 `[l, r]` 的最优解。

#### 核心思想
- 状态：`dp[l][r]` 表示区间 `[l, r]` 的最优值
- 转移：枚举分割点 `k`，`dp[l][r] = min/max(dp[l][k] + dp[k+1][r] + cost(l, k, r))`
- 初始化：`dp[i][i] = 0` 或基础情况
- 计算顺序：按区间长度从小到大

#### 示例代码（矩阵链乘法）
```cpp
int matrixChainMultiplication(vector<int>& dims) {
    int n = dims.size() - 1;
    vector<vector<int>> dp(n, vector<int>(n, 0));
    
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i <= n - len; i++) {
            int j = i + len - 1;
            dp[i][j] = INT_MAX;
            for (int k = i; k< j; k++) {
                int cost = dp[i][k] + dp[k+1][j] + dims[i] * dims[k+1] * dims[j+1];
                dp[i][j] = min(dp[i][j], cost);
            }
        }
    }
    return dp[0][n-1];
}
```

### 树上动态规划

树上动态规划用于在树结构上求解最优化问题，如最大独立集、树的直径等。状态通常依赖于子树的信息。

#### 核心思想
- 状态：`dp[u][0/1]` 表示以 `u` 为根的子树中，`u` 未被选取/被选取的最优值
- 转移：通过递归合并子树的信息
- 初始化：叶子节点的基础情况
- 遍历方式：深度优先搜索（DFS）

#### 示例代码（最大独立集）
```cpp
void dfs(int u, int parent, vector<vector<int>>& tree, vector<vector<int>>& dp) {
    dp[u][0] = 0;  // u 不选
    dp[u][1] = 1;  // u 选
    
    for (int v : tree[u]) {
        if (v == parent) continue;
        dfs(v, u, tree, dp);
        dp[u][0] += max(dp[v][0], dp[v][1]);  // u 不选，v 可选可不选
        dp[u][1] += dp[v][0];                 // u 选，v 必须不选
    }
}
```

### 背包动态规划

背包问题是动态规划的经典应用，包括0/1背包、完全背包、多重背包等变体。核心是在容量限制下最大化价值。

#### 0/1背包
- 状态：`dp[i][w]` 表示前 `i` 个物品在容量 `w` 下的最大价值
- 转移：`dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i]] + value[i])`
- 空间优化：可滚动数组降至一维

#### 完全背包
- 状态转移：`dp[w] = max(dp[w], dp[w-weight[i]] + value[i])`（正序遍历）
- 适用于物品无限量使用的情况

#### 示例代码（0/1背包）
```cpp
int knapsack01(vector<int>& weight, vector<int>& value, int capacity) {
    vector<int> dp(capacity + 1, 0);
    for (int i = 0; i < weight.size(); i++) {
        for (int w = capacity; w >= weight[i]; w--) {
            dp[w] = max(dp[w], dp[w - weight[i]] + value[i]);
        }
    }
    return dp[capacity];
}
```

### 位运算动态规划

位运算动态规划（状压DP）用于处理状态可以用二进制位表示的问题，如旅行商问题、集合覆盖等。状态通常表示为 `dp[state]`，其中 `state` 的每一位代表某个元素是否被选取。

#### 核心思想
- 状态压缩：用整数的二进制位表示集合状态
- 状态转移：枚举子状态或增量更新
- 常用技巧：`state & (state - 1)` 清除最低位1，`lowbit = state & -state` 获取最低位1

#### 示例代码（旅行商问题）
```cpp
int tsp(vector<vector<int>>& dist) {
    int n = dist.size();
    int totalStates = 1 << n;
    vector<vector<int>> dp(totalStates, vector<int>(n, INT_MAX));
    
    // 初始化：从每个城市出发
    for (int i = 0; i < n; i++) {
        dp[1 << i][i] = 0;
    }
    
    // 状态转移
    for (int state = 0; state< totalStates; state++) {
        for (int i = 0; i < n; i++) {
            if (!(state & (1 << i))) continue;  // i 不在 state 中
            for (int j = 0; j < n; j++) {
                if (state & (1 << j)) continue;  // j 已在 state 中
                int nextState = state | (1 << j);
                dp[nextState][j] = min(dp[nextState][j], dp[state][i] + dist[i][j]);
            }
        }
    }
    
    // 返回到起点
    int res = INT_MAX;
    int fullState = (1 << n) - 1;
    for (int i = 0; i < n; i++) {
        res = min(res, dp[fullState][i] + dist[i][0]);
    }
    return res;
}
```

### 数位动态规划

数位动态规划用于处理与数字位相关的问题，如计算满足某些条件的数字个数（例如：不含连续1的数字、数字和等于S等）。核心是从高位到低位逐位处理，同时维护是否受限的状态。

#### 核心思想
- 状态：`dp[pos][state][limit]` 表示处理到第 `pos` 位，当前状态为 `state`，是否受原数字限制的方案数
- `pos`：当前处理的位置（从高位到低位）
- `state`：问题相关的状态（如是否前一位是1、当前和等于多少等）
- `limit`：布尔值，表示当前前缀是否等于原数字对应前缀（受限）或已小于（不受限）
- 转移：枚举当前位可以放置的数字，更新状态和限制条件

#### 示例代码（计算不含连续1的非负整数个数）
```cpp
int findIntegers(int n) {
    string s = bitset<32>(n).to_string();
    s = s.substr(s.find_first_not_of('0'));  // 去掉前导零
    if (s.empty()) s = "0";
    
    int len = s.size();
    // dp[pos][state]: state=0 表示前一位不是1，state=1 表示前一位是1
    vector<vector<int>> dp(len + 1, vector<int>(2, 0));
    dp[0][0] = 1;  // 初始状态：没有放置任何数字，前一位视为不是1
    
    for (int i = 0; i < len; i++) {
        int digit = s[i] - '0';
        for (int state = 0; state < 2; state++) {
            if (dp[i][state] == 0) continue;
            int up = limit ? digit : 1;  // 当前位可放置的最大数字
            for (int d = 0; d <= up; d++) {
                if (state == 1 && d == 1) continue;  // 前一位是1且当前放1，则形成连续1
                int nextState = (d == 1) ? 1 : 0;
                bool nextLimit = limit && (d == up);
                dp[i+1][nextState] += dp[i][state];
                // 这里需要根据limit维度来更新，简化处理实际应使用三维DP
            }
        }
    }
    // 实际实现中需要考虑limit维度，此处为简化展示
    // 完整实现请参考代码库中的 digit_dp.cpp
    return dp[len][0] + dp[len][1];
}
```

## 贪心算法

贪心算法通过在每一步选择当前最优的解，希望由此得到全局最优解。适用于具有贪心选择性质和最优子结构的问题。

#### 核心思想
- 贪心选择性质：全局最优解可以通过在每一步做出局部最优选择来得到
- 最优子结构：问题的最优解包含其子问题的最优解
- 实现步骤：将问题分解为子问题，对每个子问题做出贪心选择，然后解决剩余的子问题

#### 适用条件
- 问题具有贪心选择性质
- 问题具有最优子结构

#### 示例代码（活动选择问题）
```cpp
struct Activity {
    int start, finish;
};

vector<Activity> activitySelection(vector<Activity>& activities) {
    // 按结束时间排序
    sort(activities.begin(), activities.end(), [](const Activity& a, const Activity& b) {
        return a.finish < b.finish;
    });
    
    vector<Activity> result;
    result.push_back(activities[0]);  // 选择第一个活动
    
    int lastFinish = activities[0].finish;
    for (int i = 1; i< activities.size(); i++) {
        if (activities[i].start >= lastFinish) {  // 不冲突
            result.push_back(activities[i]);
            lastFinish = activities[i].finish;
        }
    }
    return result;
}
```

## 双指针技术

双指针技术通过使用两个指针来遍历数组或字符串，以线性时间解决问题。常用于数组、字符串、链表等线性结构。

#### 常见模式
- **对撞指针**：两个指针从两端向中间移动（如二分查找、对撞窗口）
- **同向指针**：两个指针同方向移动，快指针在前，慢指针在后（如快慢指针查找环、删除重复元素）
- **快慢指针**：一快一慢，用于检测循环或查找中间节点

#### 示例代码（两数之和 - 有序数组）
```cpp
vector<int> twoSum(vector<int>& numbers, int target) {
    int left = 0, right = numbers.size() - 1;
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) {
            return {left + 1, right + 1};  // 返回1-based索引
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
    return {};  // 未找到
}
```

## 滑动窗口

滑动窗口技术通过维护一个满足特定条件的窗口，并不断滑动它来遍历数组或字符串，以线性时间解决问题。适用于求满足某些条件的子数组或子字符串的最小长度、最大长度或个数等问题。

#### 核心思想
- 使用两个指针 `left` 和 `right` 表示窗口的左右边界
- `right` 指针向右扩展窗口，直到窗口满足某个条件
- 然后移动 `left` 指针收缩窗口，以寻找更优的解
- 在过程中记录满足条件的窗口的最优值（如最小长度、最大长度等）

#### 示例代码（最小覆盖子串）
```cpp
string minWindow(string s, string t) {
    vector<int> tCount(128, 0), sCount(128, 0);
    for (char c : t) tCount[c]++;
    
    int required = 0;
    for (int count : tCount) {
        if (count > 0) required++;
    }
    
    int formed = 0, left = 0, right = 0;
    int minLen = INT_MAX, minLeft = 0;
    
    while (right < s.size()) {
        char c = s[right];
        sCount[c]++;
        if (tCount[c] > 0 && sCount[c] == tCount[c]) {
            formed++;
        }
        
        while (left <= right && formed == required) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                minLeft = left;
            }
            
            char leftChar = s[left];
            sCount[leftChar]--;
            if (tCount[leftChar] > 0 && sCount[leftChar] < tCount[leftChar]) {
                formed--;
            }
            left++;
        }
        right++;
    }
    
    return minLen == INT_MAX ? "" : s.substr(minLeft, minLen);
}
```

## 前缀和

前缀和技术通过预处理数组的前缀和，能够在O(1)时间内查询任意区间的和。是处理区间求和问题的基础工具。

#### 核心思想
- 定义前缀和数组 `prefix[i] = nums[0] + nums[1] + ... + nums[i-1]`，其中 `prefix[0] = 0`
- 则区间 `[l, r]` 的和为 `prefix[r+1] - prefix[l]`
- 预处理时间：O(n)，查询时间：O(1)

#### 示例代码（区间和查询）
```cpp
class NumArray {
private:
    vector<int> prefix;
public:
    NumArray(vector<int>& nums) {
        int n = nums.size();
        prefix.resize(n + 1, 0);
        for (int i = 0; i< n; i++) {
            prefix[i+1] = prefix[i] + nums[i];
        }
    }
    
    int sumRange(int left, int right) {
        return prefix[right+1] - prefix[left];
    }
};
```

## Mo's Algorithm

Mo's Algorithm（莫队算法）是一种用于处理离线区间查询的技术，通过将查询按照特定顺序排序来减少调整代价，从而将时间复杂度降低到O((n + q)√n)。适用于静态数组上的区间查询问题，如区间众数、区间不同元素个数等。

#### 核心思想
- 将数组分块，每块大小为约 √n
- 查询排序规则：首先按左端点所属的块排序，同一块内按右端点排序（奇偶块采用不同顺序以优化）
- 维护当前区间 [curL, curR]，并通过移动端点来调整到目标查询区间
- 每次移动端点时更新答案（如增加/删除一个元素的贡献）
- 总调整次数：O((n + q)√n)

#### 示例代码（区间不同元素个数）
```cpp
struct Query {
    int l, r, idx;
    bool operator<(const Query& other) const {
        int block_size = sqrt(n);
        if (l / block_size != other.l / block_size) 
            return l / block_size< other.l / block_size;
        return (l / block_size) % 2 == 0 ? r < other.r : r > other.r;
    }
};

vector<int> moAlgorithm(vector<int>& nums, vector<Query>& queries) {
    int n = nums.size();
    int q = queries.size();
    int block_size = sqrt(n);
    
    sort(queries.begin(), queries.end());
    
    vector<int> cnt(MAXN, 0);
    vector<int> res(q);
    int distinctCount = 0;
    int curL = 0, curR = -1;  // 当前区间 [curL, curR]
    
    auto add = [&](int pos) {
        int val = nums[pos];
        if (cnt[val] == 0) distinctCount++;
        cnt[val]++;
    };
    
    auto remove = [&](int pos) {
        int val = nums[pos];
        cnt[val]--;
        if (cnt[val] == 0) distinctCount--;
    };
    
    for (const Query& q : queries) {
        while (curL > q.l) add(--curL);
        while (curR< q.r) add(++curR);
        while (curL < q.l) remove(curL++);
        while (curR > q.r) remove(curR--);
        res[q.idx] = distinctCount;
    }
    
    return res;
}
```</details>
