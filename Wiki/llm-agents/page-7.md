<!-- wiki_page_id: page-7 -->

# dotnet 和 Java 参考实现

## 概述

本文档描述了 llm-agents 仓库中 dotnet 和 Java 两种语言的参考实现。这些实现演示了如何使用不同的 LLM 框架构建主题研究代理（Topic Research Agent），展示了跨语言和跨框架的一致性设计。

## 目录结构

```
llm-agents/
├── dotnet/
│   ├── README.md
│   └── src/
│       └── TopicResearchAgent/
│           └── Program.cs
└── java/
    ├── README.md
    ├── google-adk/
    │   └── src/
    │       └── main/
    │           └── java/
    │               └── com/
    │                   └── llmagents/
    │                       └── adk/
    │                           └── TopicResearchApp.java
    └── langchain4j/
        └── src/
            └── main/
                └── java/
                    └── com/
                        └── llmagents/
                            └── TopicResearchApp.java
```

## 功能特性

### 核心功能

所有参考实现共同提供以下功能：
- 主题研究工作流程
- LLM 集成接口
- 结果输出和展示
- 错误处理和日志记录

### 框架特异性实现

| 语言 | 框架 | 关键特性 |
|------|------|----------|
| .NET | 原生 SDK | 使用官方 .NET LLM SDK 进行模型调用 |
| Java | Google ADK | 集成 Google Agent Development Kit，支持工具使用和代理编排 |
| Java | LangChain4j | 使用 LangChain4j 框架，提供模型抽象和提示模板 |

## 详细实现

### .NET 实现 (TopicResearchAgent)

**文件位置**: `dotnet/src/TopicResearchAgent/Program.cs`

**关键组件**：
- 主程序入口点
- LLM 客户端初始化
- 主题研究流程控制
- 结果处理和输出

**工作流程**：
1. 初始化 LLM 客户端
2. 接收研究主题输入
3. 调用 LLM 进行主题分析
4. 处理和格式化返回结果
5. 输出研究报告

### Java 实现 (Google ADK)

**文件位置**: `java/google-adk/src/main/java/com/llmagents/adk/TopicResearchApp.java`

**关键组件**：
- Agent 定义和配置
- 工具集成（如搜索工具）
- 状态管理和记忆
- 交互式研究流程

**工作流程**：
1. 配置 Google ADK 环境
2. 定义研究代理及其能力
3. 注册必要的工具（如网络搜索）
4. 启动代理交互循环
5. 处理用户查询并生成研究结果

### Java 实现 (LangChain4j)

**文件位置**: `java/langchain4j/src/main/java/com/llmagents/TopicResearchApp.java`

**关键组件**：
- 聊天语言模型抽象
- 提示模板管理
- 输出解析器
- 链式调用编排

**工作流程**：
1. 配置 LLM 提供商和模型
2. 创建研究提示模板
3. 构建处理链（提示 → 模型 → 输出解析）
4. 执行研究查询
5. 返回格式化的研究结果

## 架构对比

### 相似点
- 所有实现都遵循相同的核心研究工作流程
- 统一的输入/输出接口设计
- 相似的错误处理策略
- 可配置的模型参数

### 差异点

| 方面 | .NET 实现 | Java Google ADK | Java LangChain4j |
|------|-----------|-----------------|------------------|
| 抽象级别 | 底层 SDK 调用 | 高级代理框架 | 中级链式抽象 |
| 工具使用 | 需要手动实现 | 内置工具支持 | 通过集成实现 |
| 状态管理 | 简单变量 | 内置状态持久化 | 外部管理 |
| 扩展性 | 需要更多样板代码 | 插件式架构 | 模块化组件 |

## 依赖要求

### .NET
- .NET 6.0 或更高版本
- 相应的 LLM SDK 包（取决于提供商）

### Java (Google ADK)
- Java 17+
- Google ADK 依赖
- 相应的 LLM 提供商 SDK

### Java (LangChain4j)
- Java 17+
- LangChain4j 核心库
- 所需的模型提供商集成

## 使用说明

### 运行 .NET 实现
```bash
cd dotnet/src/TopicResearchAgent
dotnet run
```

### 运行 Java Google ADK 实现
```bash
cd java/google-adk
./mvnw compile exec:java -Dexec.mainClass=com.llmagents.adk.TopicResearchApp
```

### 运行 Java LangChain4j 实现
```bash
cd java/langchain4j
./mvnw compile exec:java -Dexec.mainClass=com.llmagents.TopicResearchApp
```

## 配置选项

所有实现支持通过环境变量或配置文件进行以下配置：
- LLM 提供商选择（OpenAI, Azure, 本地模型等）
- API 密钥和端点
- 模型参数（温度、最大令牌等）
- 输出格式和详细程度

## 错误处理

每个实现都包含：
- 网络和 API 错误捕获
- 无效输入验证
- 优雅降级机制
- 日志记录用于调试

## 未来扩展方向

基于当前实现，可考虑：
- 添加更多 LLM 框架的对比实现
- 实现统一的配置接口
- 添加 Web API 包装器
- 集成高级研究技术（如树状思考、自我反思）
- 添加单元测试和集成测试

## 结论

dotnet 和 Java 的参考实现展示了如何在不同生态系统中构建等效的 LLM 应用程序。虽然具体实现细节因框架而异，但所有版本都保持了核心功能的一致性，为开发者提供了多种选择来构建 LLM 驱动的主题研究代理。这些实现不仅作为功能示例，还作为理解不同 LLM 框架范式和权衡的教育资源。
