<!-- wiki_page_id: page-1 -->

# 项目介绍与目录结构

## 项目概述

llm-agents 是一个用于构建大语言模型（LLM）代理系统的框架。该项目旨在提供灵活的组件和工具，以便开发者能够快速构建具有自主决策能力、工具使用和记忆功能的智能代理。

## 目录结构

项目采用模块化设计，主要包含以下目录和文件：

```
llm-agents/
├── README.md                 # 项目说明文档
├── requirements.txt          # 项目依赖列表
├── setup.py                  # 包安装配置
├── llm_agents/               # 主源代码目录
│   ├── __init__.py           # 包初始化文件
│   ├── agents/               # 代理实现
│   │   ├── base.py           # 基础代理类
│   │   ├── react.py          # ReAct 框架实现
│   │   └── tool_use.py       # 工具使用代理
│   ├── memory/               # 记忆系统
│   │   ├── __init__.py
│   │   ├── base.py           # 基础记忆接口
│   │   ├── short_term.py     # 短期记忆实现
│   │   └── long_term.py      # 长期记忆实现
│   ├── tools/                # 工具集合
│   │   ├── __init__.py
│   │   ├── base.py           # 基础工具接口
│   │   ├── search.py         # 搜索工具
│   │   └── calculator.py     # 计算器工具
│   ├── llms/                 # 大语言模型接口
│   │   ├── __init__.py
│   │   ├── base.py           # 基础LLM接口
│   │   ├── openai.py         # OpenAI API 实现
│   │   └── local.py          # 本地模型实现
│   ├── prompts/              # 提示词管理
│   │   ├── __init__.py
│   │   └── templates.py      # 提示词模板
│   └── utils/                # 工具函数
│       ├── __init__.py
│       ├── logging.py        # 日志工具
│       └── helpers.py        # 辅助函数
└── examples/                 # 使用示例
    ├── basic_agent.py        # 基础代理示例
    ├── react_agent.py        # ReAct代理示例
    └── tool_using_agent.py   # 工具使用代理示例
```

## 核心模块说明

### 代理系统 (Agents)

代理系统是项目的核心，提供了不同架构的代理实现：

- **基础代理 (Base Agent)**: 定义了所有代理共有的接口和行为
- **ReAct代理**: 实现了Reasoning和Acting交替的框架，使代理能够进行思考-行动循环
- **工具使用代理**: 特别设计用于调用外部工具执行特定任务

### 记忆系统 (Memory)

记忆系统分为两层：
- **短期记忆**: 用于存储最近的交互和上下文信息
- **长期记忆**: 用于持久化存储重要的知识和经验

### 工具系统 (Tools)

工具系统提供了可插拔的工具接口，目前包括：
- 搜索工具：用于从外部来源获取信息
- 计算器工具：用于执行数学计算

### LLM接口

抽象了不同大语言模型的调用方式，支持：
- OpenAI API
- 本地部署的模型

### 提示词管理

集中管理提示词模板，确保一致性和可维护性。

## 依赖关系

根据 `requirements.txt` 文件，项目主要依赖：
- openai: 用于调用OpenAI API
- python-dotenv: 环境变量管理
- 其他标准库和实用库

## 使用方式

项目提供了详细的示例代码在 `examples/` 目录中，展示了如何：
1. 创建基础代理实例
2. 配置LLM后端
3. 添加记忆系统
4. 集成工具使用能力
5. 运行交互式代理会话

通过这种模块化设计，开发者可以根据具体需求选择和组合不同的组件来构建定制化的LLM代理系统。
