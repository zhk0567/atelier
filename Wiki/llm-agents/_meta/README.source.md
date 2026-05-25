# llm-agents — 多语言主流 AI Agent 框架探索


在**当前仓库目录**内对比并实现主流 Agent 框架，统一基准任务 + 本地 **Ollama**（模型存放在 `./models/ollama`）。


## 项目状态


**14 个框架**已通过 Ollama live smoke（Python 13 + TypeScript 2）。dotnet / Java 为参考代码，未纳入 live 验证。详见 [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)。


## 前置条件（Windows）


1. 安装 [Ollama](https://ollama.com/download)

2. Python 3.11+、Node.js 20+（必选）

3. .NET 8 SDK、JDK 17+、Maven（仅运行 `dotnet/`、`java/` **参考示例**时需要；live smoke 不依赖）


## 快速开始


```powershell

cd f:\commercial\llm-agents


# 一键初始化（venv、npm、依赖）

.\scripts\bootstrap.ps1


# 将 Ollama 模型目录指向本项目（可选，已有模型可不拉取）

. .\scripts\setup-ollama.ps1


# 启动 Ollama（另开终端）

ollama serve


# 检查本机已安装模型（不下载）

.\scripts\pull-models.ps1


# 检查连通性与默认模型

.\scripts\check-ollama.ps1

```


默认模型见 [`config/ollama.json`](config/ollama.json)（当前：`nemotron-3-super:cloud`）。**不会自动下载**，请使用 `ollama list` 中已有的聊天模型。


```powershell

# 真机 smoke（使用已安装模型）

.\scripts\run-smoke-live.ps1

# 或指定：.\scripts\run-smoke-live.ps1 -Model nemotron-3-super:cloud

```


## Python 环境


```powershell

cd python

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -e ".[all]"

# 或：.\scripts\install-all.ps1

```


运行示例：


```powershell

cd python\langgraph

..\.venv\Scripts\python main.py "Rust 与 Go 在 CLI 工具中的取舍"

```


## 目录结构


| 路径 | 说明 |

|------|------|

| `shared/` | 统一任务规格与 mock 工具 |

| `config/ollama.json` | 模型与 API 端点 |

| `config/agent.json` | 重试、超时、默认主题、mock 检索开关 |

| `python/` | LangGraph、CrewAI、LlamaIndex、Haystack、DSPy 等 |

| `typescript/` | LangGraph.js、OpenAI Agents SDK |

| `dotnet/` | Microsoft Agent Framework / Semantic Kernel（参考） |

| `java/` | LangChain4j、Google ADK（参考） |

| `docs/` | 对比矩阵与各框架笔记 |


## 选型决策树


- 要强状态/可恢复 → **LangGraph**

- 要快做角色化团队 → **CrewAI**

- 要强 RAG → **LlamaIndex**

- 要类型与校验 → **Pydantic AI**

- Azure/.NET → **dotnet/**（参考代码）

- JVM → **java/langchain4j**（参考代码）


详见 [docs/FRAMEWORK_MATRIX.md](docs/FRAMEWORK_MATRIX.md)、[docs/COMPARISON_REPORT.md](docs/COMPARISON_REPORT.md)、[docs/CONFIG.md](docs/CONFIG.md)。


## 工具链与真机 smoke


- 读者自行扩展 dotnet/java：[docs/INSTALL_TOOLCHAIN.md](docs/INSTALL_TOOLCHAIN.md)

- 使用已有 Ollama 模型跑 smoke：`.\scripts\run-smoke-live.ps1 -Model <模型名>`

- 回填矩阵：`.\scripts\update-matrix-from-smoke.ps1`


## 文档


- [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) — 交付范围与 smoke 结果

- [docs/NEXT_TASKS.md](docs/NEXT_TASKS.md) — 已完成清单


## Smoke 测试


```powershell

.\scripts\run-all-smoke.ps1

# 或（推荐，使用已安装 Ollama 模型）：

.\scripts\run-smoke-live.ps1

```


结果写入 `docs/smoke-log.txt`、`docs/benchmarks.md`。


## 约束


- 虚拟环境、依赖缓存、Ollama 权重均在项目根下，不使用用户目录外的绝对路径。

- 示例默认使用 mock `search_topic`，无需外网。
