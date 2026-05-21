<!-- wiki_page_id: page-8 -->

# 图算法与字符串处理

## 概述

本文档介绍了Algorithm仓库中图算法和字符串处理模块的实现细节。图算法部分涵盖了图遍历、最短路径、最小生成树、拓扑排序、LCA、强连通分量、二分图匹配和网络流等核心算法；字符串处理部分包括字符串匹配、KMP、Z算法、AC自动机和Manacher算法等。

## 图算法

### 图遍历

图遍历是图算法的基础，主要包括深度优先搜索（DFS）和广度优先搜索（BFS）。

#### 深度优先搜索（DFS）

DFS通过递归或栈实现，按照深度优先的顺序遍历图的节点。

```cpp
void dfs(int u, vector<bool>& visited, const vector<vector<int>>& graph) {
    visited[u] = true;
    for (int v : graph[u]) {
        if (!visited[v]) {
            dfs(v, visited, graph);
        }
    }
}
```

#### 广度优先搜索（BFS）

BFS使用队列实现，按照广度优先的顺序遍历图的节点。

```cpp
void bfs(int start, vector<bool>& visited, const vector<vector<int>>& graph) {
    queue<int> q;
    q.push(start);
    visited[start] = true;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : graph[u]) {
            if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            }
        }
    }
}
```

### 最短路径算法

最短路径算法用于查找图中两个顶点之间的最短路径。

#### Dijkstra算法

Dijkstra算法适用于非负权重图的单源最短路径问题。

```cpp
vector<int> dijkstra(int start, const vector<vector<pair<int, int>>>& graph) {
    int n = graph.size();
    vector<int> dist(n, INT_MAX);
    vector<bool> visited(n, false);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    
    dist[start] = 0;
    pq.push({0, start});
    
    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();
        
        if (visited[u]) continue;
        visited[u] = true;
        
        for (const auto& edge : graph[u]) {
            int v = edge.first;
            int weight = edge.second;
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    
    return dist;
}
```

#### Floyd-Warshall算法

Floyd-Warshall算法用于求解所有顶点对之间的最短路径，适用于稠密图。

```cpp
vector<vector<int>> floydWarshall(const vector<vector<int>>& graph) {
    int n = graph.size();
    vector<vector<int>> dist = graph;
    
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (dist[i][k] != INT_MAX && dist[k][j] != INT_MAX && 
                    dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }
    
    return dist;
}
```

### 最小生成树算法

最小生成树算法用于在加权无向图中寻找权重最小的生成树。

#### Kruskal算法

Kruskal算法基于并查集，按边的权重从小到大选择边。

```cpp
struct Edge {
    int u, v, weight;
    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};

int find(vector<int>& parent, int x) {
    if (parent[x] != x) {
        parent[x] = find(parent, parent[x]);
    }
    return parent[x];
}

void unionSet(vector<int>& parent, vector<int>& rank, int x, int y) {
    int rx = find(parent, x);
    int ry = find(parent, y);
    if (rx != ry) {
        if (rank[rx] < rank[ry]) {
            parent[rx] = ry;
        } else if (rank[rx] > rank[ry]) {
            parent[ry] = rx;
        } else {
            parent[ry] = rx;
            rank[rx]++;
        }
    }
}

vector<Edge> kruskal(vector<Edge>& edges, int n) {
    sort(edges.begin(), edges.end());
    vector<int> parent(n);
    vector<int> rank(n, 0);
    for (int i = 0; i < n; i++) {
        parent[i] = i;
    }
    
    vector<Edge> mst;
    for (const Edge& edge : edges) {
        if (find(parent, edge.u) != find(parent, edge.v)) {
            unionSet(parent, rank, edge.u, edge.v);
            mst.push_back(edge);
        }
    }
    
    return mst;
}
```

#### Prim算法

Prim算法从一个顶点开始，逐步添加最近的顶点来构建最小生成树。

```cpp
vector<Edge> prim(const vector<vector<pair<int, int>>>& graph, int start) {
    int n = graph.size();
    vector<bool> inMST(n, false);
    vector<int> key(n, INT_MAX);
    vector<int> parent(n, -1);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    
    key[start] = 0;
    pq.push({0, start});
    
    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();
        
        if (inMST[u]) continue;
        inMST[u] = true;
        
        for (const auto& edge : graph[u]) {
            int v = edge.first;
            int weight = edge.second;
            if (!inMST[v] && weight < key[v]) {
                key[v] = weight;
                parent[v] = u;
                pq.push({key[v], v});
            }
        }
    }
    
    vector<Edge> mst;
    for (int i = 1; i < n; i++) {
        if (parent[i] != -1) {
            mst.push_back({parent[i], i, key[i]});
        }
    }
    
    return mst;
}
```

### 拓扑排序

拓扑排序用于有向无环图（DAG）的线性排序。

#### Kahn算法

Kahn算法基于入度表，逐步删除入度为0的节点。

```cpp
vector<int> topologicalSortKahn(const vector<vector<int>>& graph) {
    int n = graph.size();
    vector<int> inDegree(n, 0);
    for (int u = 0; u < n; u++) {
        for (int v : graph[u]) {
            inDegree[v]++;
        }
    }
    
    queue<int> q;
    for (int i = 0; i < n; i++) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }
    
    vector<int> result;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        result.push_back(u);
        
        for (int v : graph[u]) {
            inDegree[v]--;
            if (inDegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    return result;
}
```

### 最低公共祖先（LCA）

LCA算法用于查找树中两个节点的最近公共祖先。

```cpp
class LCA {
private:
    int n, LOG;
    vector<vector<int>> up;
    vector<int> depth;
    vector<vector<int>> graph;
    
    void dfs(int u, int parent) {
        up[u][0] = parent;
        for (int i = 1; i < LOG; i++) {
            if (up[u][i-1] != -1) {
                up[u][i] = up[up[u][i-1]][i-1];
            }
        }
        for (int v : graph[u]) {
            if (v != parent) {
                depth[v] = depth[u] + 1;
                dfs(v, u);
            }
        }
    }
    
public:
    LCA(const vector<vector<int>>& tree, int root = 0) {
        n = tree.size();
        LOG = 0;
        while ((1 << LOG) <= n) LOG++;
        up.assign(n, vector<int>(LOG, -1));
        depth.assign(n, 0);
        graph = tree;
        
        depth[root] = 0;
        dfs(root, -1);
    }
    
    int lca(int u, int v) {
        if (depth[u]< depth[v]) swap(u, v);
        
        int diff = depth[u] - depth[v];
        for (int i = 0; i < LOG; i++) {
            if (diff & (1 << i)) {
                u = up[u][i];
            }
        }
        
        if (u == v) return u;
        
        for (int i = LOG - 1; i >= 0; i--) {
            if (up[u][i] != up[v][i]) {
                u = up[u][i];
                v = up[v][i];
            }
        }
        
        return up[u][0];
    }
    
    int distance(int u, int v) {
        int ancestor = lca(u, v);
        return depth[u] + depth[v] - 2 * depth[ancestor];
    }
};
```

### 强连通分量（SCC）

Tarjan算法用于查找有向图的强连通分量。

```cpp
class TarjanSCC {
private:
    int n, time;
    vector<vector<int>> graph;
    vector<int> disc, low;
    vector<bool> inStack;
    stack<int> st;
    vector<vector<int>> sccs;
    
    void dfs(int u) {
        disc[u] = low[u] = ++time;
        st.push(u);
        inStack[u] = true;
        
        for (int v : graph[u]) {
            if (disc[v] == -1) {
                dfs(v);
                low[u] = min(low[u], low[v]);
            } else if (inStack[v]) {
                low[u] = min(low[u], disc[v]);
            }
        }
        
        if (low[u] == disc[u]) {
            vector<int> scc;
            while (true) {
                int v = st.top();
                st.pop();
                inStack[v] = false;
                scc.push_back(v);
                if (v == u) break;
            }
            sccs.push_back(scc);
        }
    }
    
public:
    TarjanSCC(const vector<vector<int>>& graph) {
        this->graph = graph;
        n = graph.size();
        disc.assign(n, -1);
        low.assign(n, 0);
        inStack.assign(n, false);
        time = 0;
        
        for (int i = 0; i < n; i++) {
            if (disc[i] == -1) {
                dfs(i);
            }
        }
    }
    
    const vector<vector<int>>& getSCCs() const {
        return sccs;
    }
    
    int getSCCCount() const {
        return sccs.size();
    }
};
```

### 二分图匹配

匈牙利算法用于求解二分图的最大匹配。

```cpp
class BipartiteMatching {
private:
    int n, m;
    vector<vector<int>> graph;
    vector<int> matchL, matchR;
    vector<bool> visited;
    
    bool dfs(int u) {
        for (int v : graph[u]) {
            if (!visited[v]) {
                visited[v] = true;
                if (matchR[v] == -1 || dfs(matchR[v])) {
                    matchL[u] = v;
                    matchR[v] = u;
                    return true;
                }
            }
        }
        return false;
    }
    
public:
    BipartiteMatching(const vector<vector<int>>& graph) {
        this->graph = graph;
        n = graph.size();
        m = 0;
        for (const auto& row : graph) {
            for (int v : row) {
                m = max(m, v + 1);
            }
        }
        matchL.assign(n, -1);
        matchR.assign(m, -1);
        visited.assign(m, false);
    }
    
    int maxMatching() {
        int result = 0;
        for (int u = 0; u < n; u++) {
            fill(visited.begin(), visited.end(), false);
            if (dfs(u)) {
                result++;
            }
        }
        return result;
    }
    
    const vector<int>& getMatchL() const {
        return matchL;
    }
    
    const vector<int>& getMatchR() const {
        return matchR;
    }
};
```

### 网络流

Edmonds-Karp算法是Ford-Fulkerson方法的一种实现，使用BFS寻找增广路。

```cpp
class EdmondsKarp {
private:
    struct Edge {
        int to, rev;
        long long cap;
        Edge(int to, int rev, long long cap) : to(to), rev(rev), cap(cap) {}
    };
    
    int n;
    vector<vector<Edge>> graph;
    vector<int> level, ptr;
    
    bool bfs(int s, int t) {
        fill(level.begin(), level.end(), -1);
        queue<int> q;
        level[s] = 0;
        q.push(s);
        
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            
            for (const Edge& e : graph[u]) {
                if (e.cap > 0 && level[e.to] == -1) {
                    level[e.to] = level[u] + 1;
                    q.push(e.to);
                }
            }
        }
        
        return level[t] != -1;
    }
    
    long long dfs(int u, int t, long long flow) {
        if (u == t) return flow;
        
        for (int& i = ptr[u]; i < graph[u].size(); i++) {
            Edge& e = graph[u][i];
            if (e.cap > 0 && level[e.to] == level[u] + 1) {
                long long pushed = dfs(e.to, t, min(flow, e.cap));
                if (pushed > 0) {
                    e.cap -= pushed;
                    graph[e.to][e.rev].cap += pushed;
                    return pushed;
                }
            }
        }
        
        return 0;
    }
    
public:
    EdmondsKarp(int n) : n(n), graph(n), level(n), ptr(n) {}
    
    void addEdge(int u, int v, long long cap) {
        graph[u].push_back(Edge(v, graph[v].size(), cap));
        graph[v].push_back(Edge(u, graph[u].size() - 1, 0));
    }
    
    long long maxFlow(int s, int t) {
        long long flow = 0;
        while (bfs(s, t)) {
            fill(ptr.begin(), ptr.end(), 0);
            while (long long pushed = dfs(s, t, LLONG_MAX)) {
                flow += pushed;
            }
        }
        return flow;
    }
};
```

## 字符串处理

### 字符串匹配算法

字符串匹配是字符串处理的基础问题。

#### KMP算法

KMP算法通过预处理模式串生成next数组来避免不必要的字符比较。

```cpp
vector<int> computeLPSArray(const string& pat) {
    int M = pat.length();
    vector<int> lps(M, 0);
    int len = 0;
    int i = 1;
    while (i < M) {
        if (pat[i] == pat[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
    return lps;
}

int KMPSearch(const string& pat, const string& txt) {
    int M = pat.length();
    int N = txt.length();
    
    vector<int> lps = computeLPSArray(pat);
    
    int i = 0;
    int j = 0;
    while (i < N) {
        if (pat[j] == txt[i]) {
            j++;
            i++;
        }
        
        if (j == M) {
            return i - j;
            j = lps[j - 1];
        } else if (i < N && pat[j] != txt[i]) {
            if (j != 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }
    
    return -1;
}
```

#### Z算法

Z算法通过计算Z数组来实现线性时间的字符串匹配。

```cpp
vector<int> computeZArray(const string& s) {
    int n = s.length();
    vector<int> Z(n, 0);
    int L = 0, R = 0;
    
    for (int i = 1; i< n; i++) {
        if (i > R) {
            L = R = i;
            while (R < n && s[R - L] == s[R]) {
                R++;
            }
            Z[i] = R - L;
            R--;
        } else {
            int k = i - L;
            if (Z[k]< R - i + 1) {
                Z[i] = Z[k];
            } else {
                L = i;
                while (R < n && s[R - L] == s[R]) {
                    R++;
                }
                Z[i] = R - L;
                R--;
            }
        }
    }
    
    return Z;
}

int ZAlgorithmSearch(const string& pat, const string& txt) {
    string concat = pat + "$" + txt;
    vector<int> Z = computeZArray(concat);
    
    for (int i = pat.length() + 1; i< concat.length(); i++) {
        if (Z[i] == pat.length()) {
            return i - pat.length() - 1;
        }
    }
    
    return -1;
}
```

### AC自动机

AC自动机（Aho-Corasick自动机）用于多模式串匹配。

```cpp
struct ACNode {
    vector<int> next;
    int fail;
    vector<int> output;
    ACNode() : next(26, -1), fail(0) {}
};

class ACAutomaton {
private:
    vector<ACNode> nodes;
    
public:
    ACAutomaton() {
        nodes.emplace_back();
    }
    
    void insert(const string& word) {
        int curr = 0;
        for (char c : word) {
            int idx = c - 'a';
            if (nodes[curr].next[idx] == -1) {
                nodes[curr].next[idx] = nodes.size();
                nodes.emplace_back();
            }
            curr = nodes[curr].next[idx];
        }
        nodes[curr].output.push_back(nodes[curr].output.size());
    }
    
    void buildFail() {
        queue<int> q;
        for (int i = 0; i< 26; i++) {
            if (nodes[0].next[i] != -1) {
                nodes[nodes[0].next[i]].fail = 0;
                q.push(nodes[0].next[i]);
            } else {
                nodes[0].next[i] = 0;
            }
        }
        
        while (!q.empty()) {
            int curr = q.front();
            q.pop();
            
            for (int i = 0; i < 26; i++) {
                int child = nodes[curr].next[i];
                if (child != -1) {
                    int fail = nodes[curr].fail;
                    while (nodes[fail].next[i] == -1) {
                        fail = nodes[fail].fail;
                    }
                    nodes[child].fail = nodes[fail].next[i];
                    
                    // Merge output
                    nodes[child].output.insert(nodes[child].output.end(), 
                                             nodes[nodes[child].fail].output.begin(),
                                             nodes[nodes[child].fail].output.end());
                    
                    q.push(child);
                } else {
                    nodes[curr].next[i] = nodes[nodes[curr].fail].next[i];
                }
            }
        }
    }
    
    vector<pair<int, int>> search(const string& text) {
        vector<pair<int, int>> result;
        int curr = 0;
        
        for (int i = 0; i< text.length(); i++) {
            int idx = text[i] - 'a';
            while (nodes[curr].next[idx] == -1 && curr != 0) {
                curr = nodes[curr].fail;
            }
            curr = nodes[curr].next[idx];
            
            for (int outputIdx : nodes[curr].output) {
                result.push_back({i, outputIdx});
            }
        }
        
        return result;
    }
};
```

### Manacher算法

Manacher算法用于在线性时间内找到字符串的最长回文子串。

```cpp
string preprocess(const string& s) {
    if (s.empty()) return "^$";
    string ret = "^";
    for (char c : s) {
        ret += "#";
        ret += c;
    }
    ret += "#$";
    return ret;
}

string longestPalindrome(const string& s) {
    string T = preprocess(s);
    int n = T.length();
    vector<int> P(n, 0);
    int C = 0, R = 0;
    
    for (int i = 1; i < n - 1; i++) {
        int i_mirror = 2 * C - i;
        
        if (R > i) {
            P[i] = min(R - i, P[i_mirror]);
        }
        
        while (T[i + 1 + P[i]] == T[i - 1 - P[i]]) {
            P[i]++;
        }
        
        if (i + P[i] > R) {
            C = i;
            R = i + P[i];
        }
    }
    
    int maxLen = 0;
    int centerIndex = 0;
    for (int i = 1; i < n - 1; i++) {
        if (P[i] > maxLen) {
            maxLen = P[i];
            centerIndex = i;
        }
    }
    
    int start = (centerIndex - maxLen) / 2;
    return s.substr(start, maxLen);
}
```

## 算法复杂度分析

| 算法 | 时间复杂度 | 空间复杂度 | 适用场景 |
|------|------------|------------|----------|
| DFS/BFS | O(V + E) | O(V) | 图遍历、连通性检查 |
| Dijkstra | O((V + E) log V) | O(V) | 单源最短路径（非负权重） |
| Floyd-Warshall | O(V³) | O(V²) | 所有顶点对最短路径 |
| Kruskal | O(E log E) | O(V) | 稀疏图的最小生成树 |
| Prim | O((V + E) log V) | O(V) | 稠密图的最小生成树 |
| Kahn拓扑排序 | O(V + E) | O(V) | DAG的线性排序 |
| LCA（倍增法） | O(log N) 查询，O(N log N) 预处理 | O(N log N) | 树上LCA查询 |
| Tarjan SCC | O(V + E) | O(V) | 有向图强连通分量 |
| 匈牙利算法 | O(VE) | O(V) | 二分图最大匹配 |
| Edmonds-Karp | O(VE²) | O(V + E) | 网络流最大流 |
| KMP | O(N + M) | O(M) | 单模式串匹配 |
| Z算法 | O(N + M) | O(N + M) | 单模式串匹配 |
| AC自动机 | O(总模式长度 + 文本长度 + 输出大小) | O(总模式长度) | 多模式串匹配 |
| Manacher | O(N) | O(N) | 最长回文子串 |

## 使用示例

### 图遍历示例

```cpp
#include<iostream>
#include<vector>
#include<queue>
using namespace std;

void dfs(int u, vector<bool>& visited, const vector<vector<int>>& graph) {
    visited[u] = true;
    cout << u << " ";
    for (int v : graph[u]) {
        if (!visited[v]) {
            dfs(v, visited, graph);
        }
    }
}

void bfs(int start, vector<bool>& visited, const vector<vector<int>>& graph) {
    queue<int> q;
    q.push(start);
    visited[start] = true;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        cout << u << " ";
        for (int v : graph[u]) {
            if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            }
        }
    }
}

int main() {
    // 创建一个简单的无向图
    vector<vector<int>> graph = {
        {1, 2},    // 节点0
        {0, 3, 4}, // 节点1
        {0, 4},    // 节点2
        {1, 5},    // 节点3
        {1, 2},    // 节点4
        {3}        // 节点5
    };
    
    int n = graph.size();
    vector<bool> visited(n, false);
    
    cout << "DFS遍历: ";
    dfs(0, visited, graph);
    cout << endl;
    
    fill(visited.begin(), visited.end(), false);
    cout << "BFS遍历: ";
    bfs(0, visited, graph);
    cout << endl;
    
    return 0;
}
```

### 最短路径示例

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <climits>
using namespace std;

vector<int> dijkstra(int start, const vector<vector<pair<int, int>>>& graph) {
    int n = graph.size();
    vector<int> dist(n, INT_MAX);
    vector<bool> visited(n, false);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    
    dist[start] = 0;
    pq.push({0, start});
    
    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();
        
        if (visited[u]) continue;
        visited[u] = true;
        
        for (const auto& edge : graph[u]) {
            int v = edge.first;
            int weight = edge.second;
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    
    return dist;
}

int main() {
    // 创建一个加权有向图
    vector<vector<pair<int, int>>> graph = {
        {{1, 4}, {2, 1}},    // 节点0
        {{3, 1}},            // 节点1
        {{1, 2}, {3, 5}},    // 节点2
        {}                   // 节点3
    };
    
    vector<int> dist = dijkstra(0, graph);
    
    cout << "从节点0出发的最短路径: ";
    for (int i = 0; i< dist.size(); i++) {
        if (dist[i] == INT_MAX) {
            cout << "∞ ";
        } else {
            cout << dist[i] << " ";
        }
    }
    cout << endl;
    
    return 0;
}
```

### 字符串匹配示例

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

vector<int> computeLPSArray(const string& pat) {
    int M = pat.length();
    vector<int> lps(M, 0);
    int len = 0;
    int i = 1;
    while (i < M) {
        if (pat[i] == pat[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
    return lps;
}

int KMPSearch(const string& pat, const string& txt) {
    int M = pat.length();
    int N = txt.length();
    
    vector<int> lps = computeLPSArray(pat);
    
    int i = 0;
    int j = 0;
    while (i< N) {
        if (pat[j] == txt[i]) {
            j++;
            i++;
        }
        
        if (j == M) {
            return i - j;
            j = lps[j - 1];
        } else if (i < N && pat[j] != txt[i]) {
            if (j != 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }
    
    return -1;
}

int main() {
    string txt = "ABABDABACDABABCABAB";
    string pat = "ABABCABAB";
    
    int index = KMPSearch(pat, txt);
    if (index != -1) {
        cout << "模式串在文本中的起始位置: " << index << endl;
    } else {
        cout << "未找到匹配" << endl;
    }
    
    return 0;
}
```

## 参考实现

所有算法的完整实现可以在以下文件中找到：

- 图遍历：`cpp/algorithms/graph/traversal/graph_traversal.cpp`
- 最短路径：`cpp/algorithms/graph/shortest_path/dijkstra.cpp` 和 `cpp/algorithms/graph/shortest_path/floyd_warshall.cpp`
- 最小生成树：`cpp/algorithms/graph/mst/kruskal.cpp` 和 `cpp/algorithms/graph/mst/prim.cpp`
- 拓扑排序：`cpp/algorithms/graph/topological_sort/kahn.cpp`
- LCA：`cpp/algorithms/graph/lca/lca.cpp`
- 强连通分量：`cpp/algorithms/graph/scc/tarjan.cpp`
- 二分图匹配：`cpp/algorithms/graph/bipartite_matching/bipartite_matching.cpp`
- 网络流：`cpp/algorithms/graph/network_flow/edmonds_karp.cpp`
- 字符串算法：`cpp/algorithms/string/string_algorithms.cpp`
- KMP算法：`cpp/algorithms/string/kmp.cpp`
- Z算法：`cpp/algorithms/string/z_algorithm.cpp`
- AC自动机：`cpp/algorithms/string/ac_automaton.cpp`
- Manacher算法：`cpp/algorithms/string/manacher.cpp`

这些实现提供了高效、易于理解的算法实现，适用于学习和实际应用。
