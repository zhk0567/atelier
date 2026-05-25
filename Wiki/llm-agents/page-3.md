<!-- wiki_page_id: page-3 -->

# Python 框架实现：LangGraph

## 概述

LangGraph 是一个基于有向无环图（DAG）的框架，用于构建状态化的多智能体工作流。它通过图结构定义智能体之间的交互和数据流，支持条件分支、循环和人机交互（HITL），适用于复杂的任务规划和执行场景。

## 核心概念

### 状态管理

LangGraph 中的每个节点（智能体或操作）都可以读取和修改共享状态。状态通过 `State` 类进行定义和传递，确保数据在工作流中的一致性。

### 节点类型

- **智能体节点**：封装 LLM 调用逻辑，负责决策和内容生成。
- **工具节点**：执行具体操作，如网络搜索、数据查询等。
- **条件节点**：基于当前状态决定工作流的下一步走向。
- **人机交互节点**：暂停工作流等待人工输入或审批。

### 边（Edge）

边定义了节点之间的转换规则，支持：
- 固定转换：无条件跳转到指定节点
- 条件转换：基于状态判断选择不同路径
- 循环边：允许工作流返回之前的节点进行迭代

## 系统架构

### 主要组件

1. **StateGraph**：工作流的核心构建类，用于定义节点、边和入口点。
2. **Node**：抽象基类，所有工作流节点的父类。
3. **AgentNode**：封装 LLM 交互的具体节点实现。
4. **ToolNode**：执行外部工具调用的节点。
5. **ConditionalEdge**：实现基于状态的条件跳转逻辑。

### 工作流执行流程

1. 初始化 StateGraph 并定义所有节点
2. 添加节点之间的有向边（包括条件边）
3. 设置入口节点
4. 编译工作流为可执行的图
5. 传入初始状态并启动执行
6. 按照边的规则遍历节点直到达到终止条件

## 关键实现细节

### 状态持久化

状态在每个节点执行后会被自动更新并传递给下一个节点。内部使用字典结构存储状态键值对，支持嵌套结构和自定义数据类型。

### 人机交互（HITL）

根据 HITL.md 文档，LangGraph 支持在特定节点插入人工审核点：
- 工作流在 HITL 节点处暂停
- 系统等待人工输入或决策
- 人工确认后继续执行后续节点
- 适用于需要人工判断的关键决策点

### 错误处理

框架提供异常捕获机制：
- 单个节点失败不会导致整个工作流崩溃
- 可配置重试策略和失败回退路径
- 错误信息会被记录到状态中供后续节点参考

## 使用示例

### 基础工作流构建

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    input: str
    output: str
    decision: str

def agent_node(state: AgentState) -> AgentState:
    # LLM 处理逻辑
    state["output"] = f"Processed: {state['input']}"
    return state

def decision_node(state: AgentState) -> AgentState:
    # 基于输出做决策
    state["decision"] = "approve" if len(state["output"]) > 10 else "reject"
    return state

# 构建图
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("decision", decision_node)
workflow.add_edge("agent", "decision")
workflow.add_conditional_edges(
    "decision",
    lambda state: state["decision"],
    {
        "approve": END,
        "reject": "agent"
    }
)
workflow.set_entry_point("agent")

app = workflow.compile()
result = app.invoke({"input": "Hello World"})
```

### CrewResearch 多智能体协作

在 crew_research.py 中展示了多智能体研究工作流：
- Researcher 负责信息收集
- Analyst 负责数据分析
- Writer 负责报告撰写
- 通过条件边实现智能体之间的协作和迭代

## 配置与扩展

### 自定义节点

用户可以通过继承 `Node` 类实现自定义逻辑：
```python
class CustomNode(Node):
    def __init__(self, name: str):
        super().__init__(name)
    
    def execute(self, state: dict) -> dict:
        # 自定义处理逻辑
        return state
```

### 集成外部工具

通过 `ToolNode` 包装外部函数：
```python
from langgraph.nodes import ToolNode

def search_tool(query: str) -> str:
    # 实际搜索实现
    return f"Results for {query}"

search_node = ToolNode("search", search_tool)
```

## 最佳实践

1. **状态设计**：保持状态结构扁平化，避免深层嵌套提高可读性
2. **节点职责单一**：每个节点只负责一个明确的功能
3. **错误容错**：在关键节点添加重试机制和 fallback 路径
4. **可视化调试**：利用图结构优势，通过可视化工具监控工作流执行路径
5. **渐进式构建**：先建立基本流程，再逐步添加条件分支和人机交互点

## 参考资料

- 项目主文档：python/langgraph/README.md
- 核心实现：python/langgraph/main.py
- 多智能体示例：python/langgraph/crew_research.py
- 人机交互指南：python/langgraph/HITL.md

</details>
