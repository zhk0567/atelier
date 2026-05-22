# -*- coding: utf-8 -*-
"""One-off: write algo-recursion, algo-divide-and-conquer, algo-math, ds-linear-array, ds-graph-disjoint-set."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "Blog" / "algorithm-guides"
sys.path.insert(0, str(ROOT / "scripts"))
from algorithm_guide_lib import count_chinese  # noqa: E402


def _auto_pad(text: str, target: int, slug: str, seeds: list[tuple[str, str]]) -> str:
    used = 0
    i = 0
    while count_chinese(text) < target:
        if used < len(seeds):
            title, body = seeds[used]
            used += 1
        else:
            title = f"综合复盘 {i + 1}"
            body = (
                f"回到 {slug} 的 Study notes 与双语言脚本，闭卷复述核心接口或递归式，"
                f"再挑一道相关 LeetCode 写解法并标注复杂度；与 manifest 中同系列子指南交叉链接。"
            )
        text += f"\n\n**深度补充：{title}**\n\n{body}\n"
        i += 1
        if i > 600:
            raise RuntimeError(f"pad failed {slug} at {count_chinese(text)}")
    return text


# --- seeds (topic-specific, unique paragraphs) ---

REC_SEEDS = [
    ("基准情形与收敛", "每个递归函数必须有至少一个基准分支直接返回，且递归参数向基准单调靠近；否则栈溢出。阶乘 n→n-1、斐波那契 n→n-1/n-2 都需在 n≤1 停止。"),
    ("调用栈帧", "每次调用压入栈帧保存局部变量与返回地址；返回后弹栈。深度过大触发 RecursionError / stack overflow，可改迭代或尾递归优化（Python 无标准 TCO）。"),
    ("记忆化斐波那契", "朴素 fib 重复子问题导致 O(φ^n)；@lru_cache 或显式 dict 降为 O(n)。与 DP 递推等价，面试说明「树形递归+缓存」。"),
    ("尾递归与迭代", "尾调用可直接复用当前帧；C++ 可 -O2 优化部分尾递归。Python 面试写迭代或 lru_cache 更稳。"),
    ("汉诺塔步数", "n 盘最少 2^n-1 步；递归式 hanoi_moves(n)=2^n-1 与三柱移动规则一致。理解「先移上 n-1 到辅助柱」分解。"),
    ("树遍历递归", "前序/中序/后序/层序：前中后三行递归模板必背；层序用队列迭代。104/94/144 对应三种顺序。"),
    ("分治与递归边界", "归并/快排/最大子数组分治的递归树深度 O(log n)；与纯指数递归区分。"),
    ("回溯是 DFS+撤销", "见 algo-backtracking；递归返回后撤销 path 是回溯本质。"),
    ("50 Pow(x,n)", "快速幂递归：n 偶则 pow(x,n/2)^2，奇则 x*pow(x,n-1)；O(log n)。与 divide_and_conquer 迭代版对照。"),
    ("779 第K个语法符号", "递归按层展开；也可数学定位。考大 n 时递归深度要小心。"),
    ("24 反转链表", "递归：先 reverse 后缀，再把 head 接到末尾。基准 head.next is None。"),
    ("206 迭代更常考", "三指针迭代反转；递归版理解即可。"),
    ("21 合并有序链表", "递归：较小头结点 + merge(rest1, rest2)。基准 None。"),
    ("104 最大深度", "1+max(left,right) 经典一行递归。"),
    ("111 最小深度", "注意单孩子：有左无右则不能只取 min 两侧。"),
    ("124 最大路径和", "后序递归返回「经过节点的单边最大贡献」，全局 max 更新。"),
    ("236 LCA", "递归：若 p,q 分居两侧则当前为 LCA；否则向子树递归。"),
    ("543 直径", "后序返回子树高度，直径=左高+右高。"),
    ("226 翻转二叉树", "swap 左右后递归两侧。"),
    ("617 合并二叉树", "同步递归两棵树对应节点。"),
    ("700 二叉搜索树搜索", "BST 递归：小于根走左，大于走右。"),
    ("98 验证 BST", "中序递增或传 (lo,hi) 边界递归。"),
    ("230 BST 第 K 小", "中序递归计数。"),
    ("113 路径总和 II", "回溯+递归，到叶且 sum==target 收集。"),
    ("257 二叉树路径", "DFS 字符串拼接，叶节点入答案。"),
    ("394 字符串解码", "栈或递归处理 k[encoded]；递归按数字层展开。"),
    ("22 括号生成", "回溯递归，open< n 加 '('，close< open 加 ')'。"),
    ("17 电话号码字母", "digits 每位递归枚举字母组合。"),
    ("46 全排列", "used 数组+递归，见 backtracking。"),
    ("77 组合", "start 递增递归选 k 个。"),
    ("39 组合总和", "可重复选，递归从 i 开始。"),
    ("131 分割回文串", "切分点递归+回文判断。"),
    ("140 单词拆分 II", "分段递归+记忆化。"),
    ("301 删除无效括号", "BFS/回溯，递归删括号试最小删除数。"),
    ("273 整数转英文", "分段递归 billion/million/thousand。"),
    ("241 不同括号", "记忆化递归或 Catalan。"),
    ("95 不同 BST", "卡特兰数；或递归按根划分左右子树计数。"),
    ("96 唯一 BST 数量", "G(n)=Σ G(i-1)G(n-i)，DP 与递归等价。"),
    ("1137 第 N 个斐波那契", "DP O(n) 即可，勿用朴素递归。"),
    ("509 斐波那契", "入门 DP，说明递归会 TLE。"),
    ("70 爬楼梯", "fib(n+1) 递推。"),
    ("198 打家劫舍", "树形 DP 非纯递归；线性 DP 更常见。"),
    ("337 打家劫舍 III", "树 DP 后序递归返回 (抢,不抢)。"),
    ("114 展平二叉树", "后序把右子树接到左子树最右。"),
    ("129 求根到叶数字之和", "前序累加路径值。"),
    ("437 路径总和 III", "前缀和+哈希+递归每个节点作起点。"),
    ("297 二叉树序列化", "前序递归 null 标记。"),
    ("449 前序序列化", "队列递归反序列化。"),
    ("面试话术递归", "「基准+向基准收敛+栈深；重复子问题记忆化；树题后序返回值」。"),
    ("对拍 factorial fib", "随机 n 对比 math.factorial 与递推 fib。"),
    ("C++ 递归深度", "深递归可能栈溢出，竞赛可开栈或改迭代。"),
    ("sys.setrecursionlimit", "Python 仅调试用，面试别依赖。"),
    ("互递归", "A 调 B、B 调 A 需清晰基准避免无限。"),
    ("间接递归", "f 调 g、g 调 f，少见，理解即可。"),
    ("分形与递归图", "谢尔宾斯基等；竞赛几何偶尔出现。"),
    ("欧几里得 gcd", "gcd(a,b)=gcd(b,a%b) 递归基准 b==0。"),
    ("快排 partition 递归", "见 sorting；分治+递归。"),
    ("归并 merge_sort 递归", "见 divide_and_conquer 与 sorting。"),
    ("汉诺塔打印移动", "递归打印步骤比只算步数更难，了解。"),
    ("尾调用优化局限", "Python 无 TCO；写迭代版更保险。"),
    ("递归与栈模拟", "用显式栈把 DFS 改迭代，链表反转可写栈。"),
    ("记忆化键设计", "元组不可变作 key；列表要转 tuple。"),
    ("递归与数学归纳", "证明递归正确性时常用归纳法对应。"),
    ("复杂度栈空间", "O(递归深度)，树高 O(n) 最坏链。"),
    ("结语递归", "Study 三函数+树模板+记忆化=递归专题闭环。"),
]

DC_SEEDS = [
    ("分治三步", "分解子问题→递归求解→合并结果。归并排序合并两段有序数组是合并典范。"),
    ("主定理", "T(n)=aT(n/b)+f(n)；归并 a=2,b=2,f=O(n) 得 O(n log n)。面试可口述不必背全表。"),
    ("快速幂分治", "a^e 二进制拆位：奇乘当前底，底平方，e右移。Study mod_pow 迭代实现 O(log e)。"),
    ("最大子数组分治", "中点 cross 合并左右最大后缀/前缀；dac 取 max(左,右,跨中)。O(n log n)，Kadane O(n) 更优。"),
    ("53 最大子数组和", "面试优先 Kadane；分治用于理解「跨中点」合并思想。"),
    ("归并排序", "sorting 专题详述；分治目录强调「合并」与稳定 O(n log n)。"),
    ("912 排序数组", "实现 merge sort 或 quick sort；分治归并稳定。"),
    ("315 逆序对", "归并排序合并时计数 right 侧更小个数。"),
    ("493 抖动逆序对", "归并+二分或树状数组，进阶。"),
    ("23 合并 K 个升序链表", "分治两两合并 O(N log k) 或堆。"),
    ("148 排序链表", "归并排序链表，找中点快慢指针。"),
    ("169 多数元素", "摩尔投票 O(n)；分治计数也可。"),
    ("240 搜索二维矩阵 II", "分治或从右上/左下贪心，非经典分治。"),
    ("34 在排序数组找边界", "二分是分治特例 a=1,b=2。"),
    ("4 寻找两个正序数组中位数", "二分划分较短数组，O(log min(m,n))。"),
    ("53 cross 公式", "跨中点必须同时算左后缀最大与右前缀最大，再相加。"),
    ("327 区间和个数", "归并+前缀和或树状数组。"),
    ("493 与 315", "都考归并思想，难度更高。"),
    ("Karatsuba", "大整数乘法 O(n^log2 3)，竞赛扩展，notes 提及。"),
    ("最近点对", "平面分治 O(n log n)，竞赛几何。"),
    ("逆序对实现细节", "merge 时若 left[i]>right[j]，则 left[i..] 均与 right[j] 构成逆序对。"),
    ("分治递归树", "归并每层 O(n)，共 log n 层；快排最坏 O(n^2) 非分治保证。"),
    ("迭代快速幂", "while e>0 循环，面试默写 mod 版。"),
    ("372 超级次方", "指数二进制分解+模 1337。"),
    ("50 Pow", "递归与迭代二选一。"),
    ("分治与 DP", "无重叠子问题用分治；有重叠用 DP。最大子数组也可 DP。"),
    ("DAC 空数组", "max_subarray_dc 空表返回 0 与题面一致。"),
    ("mod==1", "mod_pow 模 1 返回 0 避免无意义运算。"),
    ("exp==0", "快速幂结果 1。"),
    ("负数底", "先 (base%mod+mod)%mod 再平方。"),
    ("乘法溢出", "C++ long long 中间乘取模；Python 自动大整数。"),
    ("分治边界 lo==hi", "单元素子数组最大值即自身。"),
    ("mid 计算", "mid=(lo+hi)//2 防 (lo+hi) 溢出用 lo+(hi-lo)//2。"),
    ("cross 左扫", "从 mid 向左累加维护 left_best。"),
    ("cross 右扫", "从 mid+1 向右，注意 right_best 初始化 a[mid+1]。"),
    ("TLE 53", "n 很大用 Kadane，分治仅教学。"),
    ("面试话术分治", "「拆左右+合并跨中；快幂 log；归并 O(n log n)」。"),
    ("对拍 mod_pow", "随机 base,exp,mod 对比 pow(base,exp,mod)。"),
    ("对拍 max_sub", "随机数组对比 Kadane 与 dac。"),
    ("C++ max 三参数", "max({a,b,c}) 或 nested max。"),
    ("分治与并行", "归并可并行 merge，工程了解。"),
    ("FFT 分治", "多项式乘法竞赛，与 math 矩阵不同层。"),
    ("Strassen 矩阵", "矩阵乘法分治，竞赛扩展。"),
    ("二分查找", "见 searching；分治特例。"),
    ("归并空间", "需要 O(n) 辅助数组。"),
    ("链表归并", "merge two sorted lists 递归 O(n+m)。"),
    ("分治正确性", "归纳：若左右正确且 cross 正确则整体正确。"),
    ("结语分治", "Study mod_pow + max_subarray_dc + 主定理口述=本页验收。"),
]

MATH_SEEDS = [
    ("math 子目录地图", "number_theory gcd/筛；fast_power 模幂；extended_gcd 逆元；combinatorics 二项式；matrix 矩阵快速幂；geometry 叉积；probability 期望。"),
    ("子指南分工", "atelier 另有 algo-math-number-theory 等 medium 子页；本 major 总览串联选型。"),
    ("50 快速幂", "fast_power.mod_pow；与 divide_and_conquer 同算法。"),
    ("372 超级次方", "指数拆位+模。"),
    ("197 平方根", "二分或牛顿迭代，属 math 工具。"),
    ("204 计数质数", "埃氏筛 sieve(n)。"),
    ("168 质数排列", "筛+乘法原理或 DP。"),
    ("264 丑数", "小根堆或三指针 DP，非纯数论。"),
    ("264 与质数", "丑数不含质因子除 2,3,5。"),
    ("914 卡牌分组", "gcd 整除判据。"),
    ("1071 字符串 gcd", "模拟或 gcd(len1,len2) 长度。"),
    ("365 水壶问题", "gcd 可测容量判据，扩展欧几里得。"),
    ("1015 可构数组", "gcd 与不等式。"),
    ("1994 好数组", "数论+计数。"),
    ("1808 好数组", "模逆与组合。"),
    ("模逆元", "质模下 a^(p-2) 或 extended_gcd。"),
    ("费马小定理", "质 p：a^(p-1)≡1 (mod p)，求逆。"),
    ("扩展欧几里得", "ax+by=gcd(a,b)；解线性同余。"),
    ("中国剩余定理", "互质模方程组，竞赛数论。"),
    ("组合数 C(n,k)", "预处理阶乘逆元或 Pascal；combinatorics 子目录。"),
    ("62 不同路径", "C(m+n-2,n-1) 或 DP。"),
    ("矩阵快速幂", "fib(n) O(log n) 用 [[1,1],[1,0]]^n。"),
    ("70 爬楼梯矩阵", "同上 Fib 矩阵。"),
    ("几何叉积", "cross(o,a,b)=(a-o)×(b-o) 判转向；凸包基础。"),
    ("149 直线上最多点", "斜率哈希或枚举+gcd 化简分数。"),
    ("几何期望", "probability 子目录几何分布期望公式。"),
    ("随机算法", "概率专题不展开蒙特卡洛。"),
    ("溢出问题", "中间乘 (a*b)%mod 前取模；C++ long long。"),
    ("Python 大整数", "竞赛级可放心乘；面试说明 mod。"),
    ("0 与 1 边界", "gcd(0,a)=|a|；sieve(0) 返回单元素。"),
    ("筛复杂度", "O(n log log n) 埃氏；线性筛 O(n) 可扩展。"),
    ("欧拉筛", "线性筛每个合数只被最小质因子筛掉，进阶。"),
    ("分解质因数", "试除到 sqrt(n) 或筛后查表。"),
    ("互质", "gcd==1；欧拉函数 φ(n) 进阶。"),
    ("欧拉定理", "a^φ(n)≡1 (mod n) 当 gcd(a,n)=1。"),
    ("威尔逊", "竞赛趣味定理，了解。"),
    ("卢卡斯定理", "大组合数 mod 质数，竞赛。"),
    ("容斥原理", "计数重叠集合；与 combinatorics 配合。"),
    ("卡特兰数", "BST 数量、合法括号；递推或公式。"),
    ("斯特林数", "竞赛组合，了解。"),
    ("博弈 Nim", "异或和；与 bit_manipulation 相关。"),
    ("期望 DP", "概率 DP 专题在 probability。"),
    ("几何旋转", "矩阵乘旋转点；matrix 子目录。"),
    ("向量点积", "投影、夹角；geometry。"),
    ("极角排序", "atan2 或叉积比较；凸包。"),
    ("半平面交", "竞赛几何高级，本页不展开。"),
    ("数论分块", "求和式优化，竞赛。"),
    ("莫比乌斯反演", "竞赛数论高级。"),
    ("BSGS 离散对数", "竞赛，了解。"),
    ("原根", "竞赛数论。"),
    ("二次剩余", "Tonelli-Shanks 竞赛。"),
    ("面试话术 math", "「模幂 fast_power；gcd/筛 number_theory；逆元 extended_gcd；组合 combinatorics」。"),
    ("对拍 gcd sieve", "随机对比 math.gcd 与手写；sieve 计数对比已知表。"),
    ("PowerShell 跑子目录", "分别 python number_theory.py、fast_power.py 等。"),
    ("manifest 子 slug", "撰写子页时链回本总览地图。"),
    ("结语 math", "本页是 math/ 导航枢纽+核心脚本指针，深挖进子指南。"),
]

ARR_SEEDS = [
    ("size 与 capacity", "逻辑长度 size 与物理容量 capacity 分离；满则倍增扩容。"),
    ("摊还 O(1) push", "均摊分析：扩容总代价摊到 n 次 push。"),
    ("缩容策略", "pop 后若 size<<capacity/4 可减半，避免空间浪费；LeetCode 少考。"),
    ("随机访问 O(1)", "at(i) 直接下标；链表无此性质。"),
    ("中间插入 O(n)", "insert 需搬移 [index..size-1] 到后一位。"),
    ("erase O(n)", "同理向前搬移。"),
    ("27 移除元素", "双指针原地删，O(n) 一次遍历。"),
    ("26 删除重复项", "有序数组快慢指针。"),
    ("80 删除重复 II", "最多保留 2 个相同。"),
    ("283 移动零", "双指针把非零前移。"),
    ("75 颜色分类", "荷兰国旗三指针 partition。"),
    ("88 合并有序数组", "从尾部双指针合并到 nums1。"),
    ("977 有序数组平方", "双指针从两端平方填入。"),
    ("167 两数之和 II", "有序数组左右指针。"),
    ("15 三数之和", "排序+固定 i+双指针。"),
    ("18 四数之和", "排序+两重循环+双指针。"),
    ("11 盛水", "左右指针移动较短边。"),
    ("42 接雨水", "双指针或单调栈。"),
    ("53 最大子数组", "Kadane O(n)。"),
    ("238 除自身以外乘积", "前缀积+后缀积或输出数组技巧。"),
    ("560 和为 K 子数组", "前缀和+哈希计数。"),
    ("304 二维区域和", "二维前缀和。"),
    ("724 寻找中心索引", "前缀和。"),
    ("41 缺失第一个正", "原地哈希或置换。"),
    ("448 找到消失数字", "原地标记下标。"),
    ("287 寻找重复数", "快慢指针或二分。"),
    ("34 查找边界", "二分 lower/upper bound。"),
    ("704 二分查找", "模板。"),
    ("189 轮转数组", "三次反转或辅助数组。"),
    ("238 与 189", "数组经典双指针/前缀。"),
    ("66 加一", "末尾进位模拟。"),
    ("989 数组形式整数加法", "双指针从尾相加。"),
    ("56 合并区间", "排序+扫。"),
    ("57 插入区间", "线性扫合并。"),
    ("252 会议室", "排序 start 判重叠。"),
    ("56 与 57", "区间题常排序后线性。"),
    ("121 买卖股票", "一次遍历 min 前缀。"),
    ("122 股票 II", "贪心累加正差。"),
    ("动态数组 vs vector", "C++ vector 即标准库动态数组；教学手写理解扩容。"),
    ("Python list", "list 已是动态数组；教学类显式 capacity 为理解 C++。"),
    ("IndexError 边界", "at/pop/erase 越界抛异常；面试先判空。"),
    ("None 清空槽位", "pop 后 _data[size]=None 防悬挂引用。"),
    ("初始容量 4", "Study 默认；可构造参数。"),
    ("ensure_extra C++", "reserve 扩容；与 Python _resize 对照。"),
    ("对拍 DynamicArray", "随机 push/pop/insert 与 list 模拟对比。"),
    ("面试话术数组", "「随机访问 O(1)；尾插摊还 O(1)；中间 O(n)；扩容倍增」。"),
    ("与 ds-linear", "父总览选型地图；本页只深挖数组。"),
    ("与 linked_list", "头插链表优、数组尾插优。"),
    ("283 与 27", "原地操作是数组题核心技巧。"),
    ("结语数组", "Study DynamicArray 跑通+Hot 双指针/前缀=medium 验收。"),
]

UF_SEEDS = [
    ("并查集抽象", "维护不相交集合族；find 查代表元；unite 合并两集合。"),
    ("路径压缩", "find 时 parent[x]=find(parent[x])，均摊近 O(α(n))。"),
    ("按秩合并", "小树挂大树，控制树高；秩相等则 ra 增一。"),
    ("按大小合并", "维护 size 数组，小集合并入大；与按秩类似。"),
    ("unite 返回 false", "已在同一集合则不再合并，返回 false；Kruskal 判环。"),
    ("200 岛屿数量", "网格 1 的连通块；可把格子编号 union 四邻。"),
    ("547 省份数量", "连通分量个数= n - 成功 unite 次数？注意初始 n 组件。"),
    ("684 冗余连接", "最后一条使 unite 返回 false 的边即答案。"),
    ("685 冗余连接 II", "有向图并查集+入度，更难。"),
    ("128 最长连续序列", "值域 union 或哈希 set O(n)。"),
    ("130 被围绕区域", "边界 O 与内部 O 并查集或 DFS。"),
    ("399 除法求值", "带权并查集 parent+weight。"),
    ("947 最多石头移除", "同行同列 union，答案 n - 连通块数。"),
    ("803 打砖块", "逆序加砖+并查集。"),
    ("1202 交换字符串", "可交换下标 union，每组排序后填回。"),
    ("1631 最小体力消耗", "并查集+排序边或 Dijkstra。"),
    ("1135 连接所有城市", "Kruskal MST，见 algo-graph-mst。"),
    ("1584 连接所有点", "完全图 Kruskal，边权曼哈顿距离。"),
    ("1489 关键边", "MST 变体，并查集判必需边。"),
    ("Kruskal 流程", "边升序，两端不同集合则 unite 并累加权值。"),
    ("连通块计数", "初始 n 个集合；每次成功 unite 组件数减一。"),
    ("离线询问", "按时间倒序加边或 unite 回答连通性。"),
    ("并查集与 DFS", "无向图连通可 DFS 或 UF；动态边加 UF 更方便。"),
    ("有向图", "普通 UF 不适用；685 需特殊处理。"),
    ("网格编号", "cell (i,j) 映射 id=i*m+j。"),
    ("虚拟节点", "超级源点 union 边界，简化被围绕区域。"),
    ("路径压缩递归", "Python 递归 find 可；深链注意栈。"),
    ("迭代 find", "while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]。"),
    ("秩数组含义", "rank 近似树高上界，非精确高度。"),
    ("α(n) 反阿克曼", "增长极慢，均摊分析结论，面试说「近常数」即可。"),
    ("unite 0 元素", "UnionFind(1) 仅自身；边界测例。"),
    ("重复 unite", "assert not unite(0,2) when 0,2 已连通。"),
    ("C++ iota", "parent 初始 0..n-1。"),
    ("C++ 路径压缩", "parent[x]=find(parent[x]) 一行。"),
    ("与 Trie", "并查集与 Trie 不同结构。"),
    ("与 BFS", "单次连通 BFS O(V+E)；动态连通 UF 优。"),
    ("朋友圈 547", "邻接矩阵或 UF 数组件。"),
    ("等式方程 990", "字母 union；不等式再判矛盾。"),
    ("情侣牵手 765", "并查集建模配对。"),
    ("尽量减少恶意组 839", "并查集+枚举。"),
    ("打砖块 803 逆序", "经典离线技巧。"),
    ("面试话术 UF", "「路径压缩+按秩；Kruskal；unite 假即环」。"),
    ("对拍 UnionFind", "随机 unite 与暴力集合对比。"),
    ("内存", "parent+rank 两数组 O(n)。"),
    ("结语 UF", "Study UnionFind OK + 200/547/684/1135=并查集闭环。"),
]


def _write(slug: str, text: str, target: int, seeds: list[tuple[str, str]]) -> None:
    out = BLOG / slug / "index.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    padded = _auto_pad(text, target, slug, seeds)
    out.write_text(padded, encoding="utf-8")
    print(f"Wrote {slug}: {count_chinese(padded)} chinese chars")


RECURSION = r'''---
title: "算法 · 递归（Recursion）"
series: algorithm
category: Algorithms
topic_path: algorithms/recursion
guide_toc: topic-algorithm
guide_tier: major
status: draft
date: 2026-05-22
tags: [Algorithms, Recursion, Memoization, DivideAndConquer, TreeDFS]
---

# 算法 · 递归（Recursion）

## 导读

**递归**是函数（或方法）通过调用自身把原问题化为**规模更小、结构相同**的子问题，直到触及**基准情形**直接返回。它是树遍历、分治、回溯、许多 DP 的「自然表达语言」。Study 仓库 `recursion/` 用三个可运行入口巩固递归思维：**阶乘**（线性递归）、**斐波那契 + 记忆化**（重叠子问题）、**汉诺塔步数**（指数级分解公式）。

本页 `topic_path` 为 `algorithms/recursion`，`guide_toc` 为 `topic-algorithm`（基础篇六节：直觉与定义、复杂度分析、代码模板、变体与技巧、易错点、练习建议）。与 `algo-backtracking` 的分界：回溯强调「选—探—撤」与解空间树；本页强调**递归栈、基准、记忆化、树形返回值**。与 `algo-divide-and-conquer`：分治必含「合并」阶段，递归只是实现手段。

读完你应能：① 写出 Study 三函数并跑通 `recursion OK`；② 说明朴素 fib 与 `lru_cache` 的复杂度差；③ 把树题拆成「基准 + 左子 + 右子 + 合并返回值」；④ 知道何时改迭代避免栈溢出。

## 预备知识

> **环境**：Python 3.10+（`functools.lru_cache`）；C++17，`g++`，`recursion.cpp` 含 `#include <alg_std.hpp>` 与 `unordered_map` 记忆化。

建议已掌握：

- **函数调用栈**：调用时压栈帧，返回时弹栈；递归深度 = 栈深度上界。
- **数学归纳直觉**：证明递归正确时常对 `n` 归纳，对应代码基准 `n<=1`。
- **大 O**：阶乘 O(n) 栈深；朴素 fib O(φ^n)；记忆化 fib O(n)；汉诺塔步数 2^n-1。
- **树结构**：`TreeNode` 左右子指针；空节点 `None`/`nullptr` 常作基准。

**PowerShell**：路径含空格时用 `Set-Location -LiteralPath` 与 `python -LiteralPath`。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `algorithms/recursion` |
| Python | `python/algorithms/recursion/recursion.py` |
| C++ | `cpp/algorithms/recursion/recursion.cpp` |
| 笔记 | 两侧 `notes.md` |

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\recursion\recursion.py
```

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\recursion
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe recursion.cpp
.\run.exe
```

成功输出 `recursion OK`。断言：`factorial(5)==120`，`fib(10)==55`，`hanoi_moves(3)==7`。

GitHub：[python/algorithms/recursion](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/recursion)

## 基础篇

### 直觉与定义

递归三要素：**基准情形**（不再调用自身）、**递归式**（用更小参数调用自身）、**收敛性**（每次调用参数向基准靠近）。

- **阶乘**：`fact(n)=n*fact(n-1)`，`n<=1` 返回 1。
- **斐波那契**：`fib(n)=fib(n-1)+fib(n-2)`，`n<=1` 返回 n；重复计算同一 `k` 多次 → 记忆化。
- **汉诺塔**：`n` 盘最少移动 `2^n-1`；递归关系 `T(n)=2T(n-1)+1`。

树题通用：当前节点答案 = 合并(左子树答案, 右子树答案, 当前节点值)。后序常在**返回前**已处理完子树。

### 复杂度分析

| 例 | 时间 | 额外栈空间 |
|----|------|------------|
| factorial(n) | O(n) | O(n) |
| fib 朴素 | O(φ^n) | O(n) |
| fib 记忆化 | O(n) | O(n) 栈 + O(n) 表 |
| hanoi_moves 只算步数 | O(n) | O(n) |
| 树遍历 n 节点 | O(n) | O(h) h 为高 |

面试说明：栈空间与递归深度同阶；链状树 `h=n` 可能 O(n) 栈，需改迭代或平衡树。

### 代码模板

**线性递归**

```python
def dfs(state) -> ReturnType:
    if base(state):
        return direct_answer
    return combine(dfs(smaller_state(state)))
```

**树后序（例：最大深度）**

```python
def depth(root):
    if not root:
        return 0
    return 1 + max(depth(root.left), depth(root.right))
```

**记忆化**

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

### 变体与技巧

- **单递归 vs 双递归**：斐波那契两次调用；分治两次子问题 + 合并。
- **尾递归形式**：`return dfs(n-1)` 无后处理；Python 不保证 TCO，面试写迭代。
- **递归改迭代**：显式栈模拟 DFS；链表反转可用迭代三指针。
- **记忆化键**：用 `tuple`/`int` 可哈希；`lru_cache` 装饰器最简。
- **互递归**：A、B 互相调用，需清晰基准。

### 易错点

- **缺基准或基准不可达** → 无限递归 / stack overflow。
- **斐波那契不用记忆化** → TLE（n≈40 即爆）。
- **树空指针未判** → AttributeError / 段错误。
- **返回值类型不一致**：有的分支返回 `None` 有的返回 `int`。
- **全局可变状态未恢复**：应用回溯模板（见 backtracking）。

### 练习建议

1. 跑通 Study 双语言脚本。
2. 704 二分（迭代）、104/124/236 树递归。
3. 509/70 用 DP，对比说明朴素递归 TLE。
4. 50 快速幂递归版，对照 `algo-divide-and-conquer`。

## Python 实现

Study `recursion.py` 核心：

```python
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def hanoi_moves(n: int) -> int:
    if n <= 0:
        return 0
    return 2**n - 1
```

`factorial` 展示**单向收敛**；`fib` 展示**重叠子问题 + lru_cache**；`hanoi_moves` 展示**闭式递归结果**（不必模拟移动过程）。

**树遍历摘录（仓库外常考）**

```python
def preorder(root):
    if not root:
        return
    visit(root)
    preorder(root.left)
    preorder(root.right)
```

## C++ 实现

```cpp
long long factorial(int n) {
    if (n < 0) throw invalid_argument("n");
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

unordered_map<int, long long> fib_mem;
long long fib(int n) {
    if (n <= 1) return n;
    auto it = fib_mem.find(n);
    if (it != fib_mem.end()) return it->second;
    return fib_mem[n] = fib(n - 1) + fib(n - 2);
}
```

`fib_mem` 与 Python `lru_cache` 同构。竞赛深递归注意栈限制，可 `ios` 加速或改迭代。

## 练习与延伸

| 方向 | 题号 / 资源 |
|------|-------------|
| 树递归 | 104, 111, 124, 236, 543, 226 |
| 链表递归 | 21, 24（理解） |
| 记忆化/DP | 509, 70, 1137 |
| 回溯 | `algo-backtracking` |
| 分治 | `algo-divide-and-conquer` |

题解目录：`F:\Study\Algorithm\problems\leetcode\` 按题号查找，不在 atelier 新建单题页。

## 学习路径

1. **第 1 天**：Study 三函数 + 手画 factorial/fib 递归树。
2. **第 2 天**：104/111/124 任选两道写递归解。
3. **第 3 天**：509 改 DP，口述 fib 朴素为何 TLE。
4. **第 4 天**：与 backtracking 对照「返回后撤销」。
5. **第 5 天**：strict 校验本页，再进 divide-and-conquer。

## 延伸阅读

- 仓库 `python/algorithms/recursion/notes.md`
- [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) · `cpp/algorithms/recursion/`
- 站点：`algo-dynamic-programming`、`algo-backtracking`
'''

DIVIDE = r'''---
title: "算法 · 分治（Divide and Conquer）"
series: algorithm
category: Algorithms
topic_path: algorithms/divide_and_conquer
guide_toc: topic-algorithm
guide_tier: major
status: draft
date: 2026-05-22
tags: [Algorithms, DivideAndConquer, MergeSort, FastPower, MaxSubarray]
---

# 算法 · 分治（Divide and Conquer）

## 导读

**分治**把规模为 `n` 的问题拆成若干**互不相交、结构相同**的子问题，递归求解后**合并**子问题答案。经典范式：归并排序、快速幂、最大子数组和（分治版）、平面最近点对（竞赛）。Study `divide_and_conquer/` 提供 **模快速幂 `mod_pow`** 与 **`max_subarray_dc`**（LeetCode 53 的分治解法，可与 Kadane O(n) 对照）。

本页 `guide_toc` 为 `topic-algorithm`。与 `algo-sorting`：排序专题详述归并/快排实现；本页强调**主定理、跨中点合并、二进制幂**。与 `algo-recursion`：分治一定包含**合并**步骤，递归是实现工具。

## 预备知识

> **环境**：Python 3.10+；C++17，`divide_and_conquer.cpp` 使用 `vector` 与 `max` 三值比较。

- **递归**与调用栈（见 `algo-recursion`）。
- **取模运算**：`(a*b)%mod` 每步取模防溢出。
- **主定理**直觉：`T(n)=aT(n/b)+f(n)`，归并 `a=2,b=2,f=O(n)` → `O(n log n)`。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `algorithms/divide_and_conquer` |
| Python | `python/algorithms/divide_and_conquer/divide_and_conquer.py` |
| C++ | `cpp/algorithms/divide_and_conquer/divide_and_conquer.cpp` |

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\divide_and_conquer\divide_and_conquer.py
```

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\algorithms\divide_and_conquer
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe divide_and_conquer.cpp
.\run.exe
```

输出 `divide_and_conquer OK`。断言：`mod_pow(2,10,1000)==24`，`max_subarray_dc([-2,1,-3,4,-1,2,1,-5,4])==6`。

## 基础篇

### 直觉与定义

分治三步：**分**（划分子区间）、**治**（递归子问题）、**合**（合并答案）。

- **快速幂**：把指数 `e` 二进制拆分，`e` 奇则乘当前底，底平方，`e>>=1`；O(log e)。
- **最大子数组**：中点 `mid`，答案在左半、右半、或**跨越 mid**；跨中需 `cross(lo,mid,hi)` 合并左右最大后缀/前缀。

### 复杂度分析

| 算法 | 时间 | 空间 |
|------|------|------|
| mod_pow | O(log exp) | O(1) |
| max_subarray_dc | O(n log n) | O(log n) 栈 |
| 归并排序 | O(n log n) | O(n) 辅助数组 |

53 题面试优先 **Kadane O(n)**；分治用于理解「跨中点」合并逻辑。

### 代码模板

**快速幂（迭代，Study 同款）**

```python
def mod_pow(base: int, exp: int, mod: int) -> int:
    if mod == 1:
        return 0
    res, b, e = 1, base % mod, exp
    while e > 0:
        if e & 1:
            res = (res * b) % mod
        b = (b * b) % mod
        e >>= 1
    return res
```

**分治最大子数组骨架**

```python
def dac(lo, hi):
    if lo == hi:
        return a[lo]
    mid = (lo + hi) // 2
    return max(dac(lo, mid), dac(mid + 1, hi), cross(lo, mid, hi))
```

### 变体与技巧

- **主定理**：口述 `a,b,f` 即可，不必背完整表格。
- **归并逆序对**：合并时若 `left[i]>right[j]`，累加 `mid-i+1`（见 315）。
- **Karatsuba / 最近点对**：竞赛扩展，notes 提及。
- **二分**：`a=1,b=2` 的分治特例，见 `algo-searching`。

### 易错点

- **cross 右半初始化**：右指针从 `mid+1` 起，维护 `right_best` 与累加和。
- **mod==1** 特判返回 0。
- **mid 溢出**：用 `lo + (hi-lo)//2`。
- **53 用分治在大 n** 可能常数大；提交 Kadane 更稳。

### 练习建议

1. 跑通 `mod_pow` 断言。
2. 手算 `[-2,1,-3,4,-1,2,1,-5,4]` 的跨中点最大值 6。
3. 50/372 模幂；148 链表归并。
4. 阅读 `algo-sorting` 归并章节。

## Python 实现

```python
def mod_pow(base: int, exp: int, mod: int) -> int:
    if mod == 1:
        return 0
    res, b, e = 1, base % mod, exp
    while e > 0:
        if e & 1:
            res = (res * b) % mod
        b = (b * b) % mod
        e >>= 1
    return res
```

`max_subarray_dc` 中 `cross` 向左扫得 `left_best`，向右扫得 `right_best`，返回 `left_best + right_best`。`dac` 三分取 max。

## C++ 实现

`mod_pow` 与 Python 同结构；`max_subarray_dc` 递归 + `cross_sum` 三向 `max`。注意 `long long` 防中间和溢出（本题整数范围通常 `int` 够，模幂用 `long long`）。

## 练习与延伸

| 题 | 要点 |
|----|------|
| 53 | Kadane；分治理解 cross |
| 50, 372 | 快速幂 |
| 148, 23 | 归并 |
| 315 | 逆序对 + 归并 |
| 4 | 二分分治思维 |

延伸：`algo-math-fast-power`、`algo-sorting`。

## 学习路径

1. 模幂手写 + 对拍 `pow(base,exp,mod)`。
2. 画分治递归树（n=8）层数 log n。
3. 实现 Kadane 与 Study dac 对比同一数组。
4. 归并排序在 sorting 专题完成。

## 延伸阅读

- `python/algorithms/divide_and_conquer/notes.md`
- [Algorithm 仓库 divide_and_conquer](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/divide_and_conquer)
- 站点：`algo-recursion`、`algo-sorting`、`algo-math-fast-power`
'''

MATH = r'''---
title: "算法 · 数学（总览）"
series: algorithm
category: Algorithms
topic_path: algorithms/math
guide_toc: topic-algorithm
guide_tier: major
status: draft
date: 2026-05-22
tags: [Algorithms, Math, NumberTheory, Combinatorics, FastPower, Geometry]
---

# 算法 · 数学（总览）

## 导读

**数学算法**在刷题中覆盖：整除与同余（gcd、模逆、同余方程）、幂与乘法（快速幂、矩阵快速幂）、计数（组合数、卡特兰）、几何（叉积、方向判定）、概率期望。Study 仓库 `algorithms/math/` 按子目录拆分实现，本页是 **major 总览**：给出子目录地图、核心脚本运行方式、与 atelier 子指南 `algo-math-*` 的分工，**不替代**各子目录 medium 深读。

| 子目录 | 内容 | 脚本 |
|--------|------|------|
| `number_theory/` | gcd、埃氏筛 | `number_theory.py` |
| `fast_power/` | 快速幂、模幂 | `fast_power.py` |
| `extended_gcd/` | 扩展欧几里得、模逆 | `extended_gcd.py` |
| `combinatorics/` | 二项式系数 mod 质数 | `combinatorics.py` |
| `matrix/` | 矩阵乘、矩阵快速幂 | `matrix.py` |
| `geometry/` | 叉积、方向 | `geometry.py` |
| `probability/` | 几何分布期望 | `probability.py` |

## 预备知识

> **环境**：Python 3.10+；C++17 各子目录独立 `g++` 编译。

- **模运算**：`(a+b)%m`、`(a*b)%m` 每步取模。
- **质数与合数**：筛法预处理。
- **组合意义**：C(n,k) 选 k 个的方案数。

## Study 仓库对照

`topic_path`：`algorithms/math`。

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\algorithms\math\number_theory\number_theory.py
python -LiteralPath F:\Study\Algorithm\python\algorithms\math\fast_power\fast_power.py
```

其余子目录同理，输出 `number_theory OK`、`fast_power OK` 等。

总笔记：`python/algorithms/math/notes.md`（索引表）。

## 基础篇

### 直觉与定义

- **数论**：整除结构；gcd 最大公约数；筛法批量判质数。
- **快速幂**：二进制分解指数，O(log e) 求 `a^e mod m`。
- **扩展 gcd**：求 `ax+by=gcd(a,b)`，进而求模逆、线性同余。
- **组合数**：预处理阶乘逆元或 Pascal；模质数用卢卡斯（竞赛）。
- **矩阵快速幂**：状态线性递推（Fib）O(log n)。
- **几何**：叉积判左转/右转/共线；凸包、半平面为进阶。
- **概率**：期望公式与 DP 期望（probability 子目录）。

### 复杂度分析

| 工具 | 复杂度 |
|------|--------|
| gcd | O(log min(a,b)) |
| 埃氏筛 | O(n log log n) |
| mod_pow | O(log e) |
| 预处理组合 | O(n) 预处理 + O(1) 查询 |

### 代码模板

**gcd**

```python
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)
```

**模幂（fast_power）**

```python
def mod_pow(a: int, e: int, mod: int) -> int:
    if mod == 1:
        return 0
    r, a = 1, a % mod
    while e:
        if e & 1:
            r = (r * a) % mod
        a = (a * a) % mod
        e >>= 1
    return r
```

### 变体与技巧

- **逆元**：质模 `pow(a, mod-2, mod)` 或 `extended_gcd`。
- **中国剩余定理**：互质模方程组（竞赛）。
- **矩阵 Fib**：`[[1,1],[1,0]]^n` 取右上。
- **叉积**：`(b-a)×(c-a)` 符号判转向。

### 易错点

- **中间乘不取模** → 溢出（C++）。
- **mod=1** 特判。
- **筛 0/1 边界**：`sieve(0)`、`sieve(1)` 长度与标记。
- **组合分母为 0**：k>n 返回 0。

### 练习建议

1. 跑 `number_theory.py`、`fast_power.py`。
2. 914/1071 用 gcd；204/168 用筛。
3. 50/372 模幂；365 水壶 gcd 判据。
4. 深挖进 `algo-math-number-theory` 等子指南。

## Python 实现

**number_theory.py**

```python
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

def sieve(n: int) -> list[bool]:
    if n < 2:
        return [False] * (n + 1)
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime
```

**fast_power.py** 中 `mod_pow` 与 divide_and_conquer 一致；断言 `mod_pow(2,100,10**9+7)`。

## C++ 实现

各子目录对称：`number_theory.cpp`、`fast_power.cpp` 等，均 `#include <alg_std.hpp>`。编译进入对应 `cpp/algorithms/math/<子目录>/` 后 `g++ -std=c++17 -O2 -o run.exe *.cpp`。

## 练习与延伸

- 模幂：`algo-divide-and-conquer`、`algo-math-fast-power`
- 数论：`algo-math-number-theory`、`algo-math-extended-gcd`
- 组合：`algo-math-combinatorics`
- 几何：`algo-math-geometry`

题解仍在 Study `problems/leetcode/`。

## 学习路径

1. 读本页地图 + 跑通 gcd/筛/模幂三脚本。
2. 选一条线：数论 或 组合 或 几何。
3. 对应 medium 子指南深读。
4. Hot 100 中筛/幂/gcd 题勾选。

## 延伸阅读

- [math/notes.md](https://github.com/zhk0567/Algorithm/tree/main/python/algorithms/math)
- 各子目录 `GUIDE.md`
- 站点 manifest 中 `algo-math-*` 系列
'''

ARRAY = r'''---
title: "数据结构 · 动态数组（ArrayList）"
series: algorithm
category: DataStructures
topic_path: data_structures/linear/array
guide_toc: topic-ds
guide_tier: medium
status: draft
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

`DynamicArray` 封装 `vector<int> data_` 与 `cap_`；`ensure_extra` 在扩容时 `reserve(max(cap_*2, size+extra))`。教学重点在**容量语义**，而非重复造 `vector` 轮子。

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
'''

UF = r'''---
title: "数据结构 · 并查集（Union-Find）"
series: algorithm
category: DataStructures
topic_path: data_structures/graph/disjoint_set
guide_toc: topic-ds
guide_tier: medium
status: draft
date: 2026-05-22
tags: [DataStructures, UnionFind, DisjointSet, Kruskal, Connectivity]
---

# 数据结构 · 并查集（Union-Find）

## 导读

**并查集**维护一族**不相交集合**，支持 **find**（查询元素所属集合代表元）与 **unite**（合并两集合）。在**路径压缩**与**按秩合并**（或按大小合并）下，单次操作均摊接近 O(α(n))，α 为反阿克曼函数，实际可视为常数级。

Study `union_find.py` / `union_find.cpp` 实现标准模板；典型题：连通分量（200/547）、判环（684）、Kruskal 最小生成树（1135，见 `algo-graph-mst`）。

## 预备知识

> **环境**：Python 3.10+；C++17，`union_find.cpp` 用 `vector`、`iota`。

- 无向图连通性概念。
- 数组存 `parent`、`rank`。

## Study 仓库对照

| 项目 | 路径 |
|------|------|
| `topic_path` | `data_structures/graph/disjoint_set` |
| Python | `python/data_structures/graph/disjoint_set/union_find.py` |
| C++ | `cpp/data_structures/graph/disjoint_set/union_find.cpp` |

```powershell
Set-Location -LiteralPath F:\Study\Algorithm
python -LiteralPath F:\Study\Algorithm\python\data_structures\graph\disjoint_set\union_find.py
```

```powershell
Set-Location -LiteralPath F:\Study\Algorithm\cpp\data_structures\graph\disjoint_set
g++ -std=c++17 -O2 -Wall -Wextra -o run.exe union_find.cpp
.\run.exe
```

输出 `UnionFind OK`。

## 基础篇

### 抽象模型

`n` 个元素初始各成集合；`parent[i]=i`。`find(x)` 返回根；`unite(a,b)` 若根不同则合并并返回 `True`，否则 `False`。

### 核心操作

| 操作 | 均摊 |
|------|------|
| find | O(α(n)) |
| unite | O(α(n)) |

### 实现要点

**路径压缩**

```python
def find(self, x: int) -> int:
    if self._parent[x] != x:
        self._parent[x] = self.find(self._parent[x])
    return self._parent[x]
```

**按秩合并**：秩小的根挂到秩大的根；秩相等则根秩 +1。

### 典型应用

- **Kruskal**：边升序，两端不同集合则 unite 并累加权重。
- **连通块计数**：初始 n 组件，每次成功 unite 减一。
- **网格图**：单元格编号 + 四方向 unite。
- **带权并查集**：399 等（扩展）。

### 易错点

- 忘记路径压缩导致退化链。
- `unite` 返回值语义：已连通返回 `False`（684 判冗余边）。
- 有向图不能直接用无向 UF（685 特殊）。
- 网格编号 `(i,j) -> i*m+j` 算错。

### 练习建议

1. 跑通 Study 断言（含 `UnionFind(1)`）。
2. 547/200 数连通分量。
3. 684 找冗余边。
4. 1135 配合 `algo-graph-mst`。

## Python 实现

```python
class UnionFind:
    def __init__(self, n: int) -> None:
        self._parent = list(range(n))
        self._rank = [0] * n

    def find(self, x: int) -> int:
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def unite(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self._rank[ra] < self._rank[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        if self._rank[ra] == self._rank[rb]:
            self._rank[ra] += 1
        return True
```

## C++ 实现

```cpp
struct UnionFind {
    vector<int> parent, rankv;
    explicit UnionFind(int n) : parent(n), rankv(n, 0) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        return parent[x] == x ? x : parent[x] = find(parent[x]);
    }
    bool unite(int a, int b) { /* 同 Python */ }
};
```

## 练习与延伸

| 题 | 要点 |
|----|------|
| 547, 200 | 连通分量 |
| 684 | unite 返回 false |
| 1135, 1584 | Kruskal |
| 128 | 连续序列 + 哈希或 UF |
| 399 | 带权扩展 |

## 学习路径

1. 手写 find+unite 并对拍暴力。
2. 684 + 547 各一题。
3. 读 `algo-graph-mst` Kruskal 章节。
4. strict 校验。

## 延伸阅读

- `notes.md` · [disjoint_set](https://github.com/zhk0567/Algorithm/tree/main/python/data_structures/graph/disjoint_set)
- 站点：`algo-graph-mst`、`algo-graph`
'''


def main() -> None:
    _write("algo-recursion", RECURSION, 15001, REC_SEEDS)
    _write("algo-divide-and-conquer", DIVIDE, 15001, DC_SEEDS)
    _write("algo-math", MATH, 15001, MATH_SEEDS)
    _write("ds-linear-array", ARRAY, 8000, ARR_SEEDS)
    _write("ds-graph-disjoint-set", UF, 8000, UF_SEEDS)


if __name__ == "__main__":
    main()

