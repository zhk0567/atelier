<!-- wiki_page_id: page-8 -->

# 配置文件说明

## 概述

本项目的配置系统采用分层设计，支持多语言（Python和TypeScript）和多环境（开发、测试、生产）配置管理。配置文件主要分为两类：模型服务配置（如Ollama）和智能体配置。

## 配置文件结构

项目中的核心配置文件位于`config/`目录下，包含：

- `ollama.json`：Ollama大语言模型服务的连接和参数配置
- `agent.json`：智能体（Agent）的行为、角色和能力配置

这些配置被统一加载到代码中，通过语言特定的配置模块提供类型安全的访问接口。

## Ollama配置详解 (`ollama.json`)

Ollama配置文件定义了与本地Ollama服务的交互参数：

```json
{
  "host": "http://localhost:11434",
  "model": "llama3",
  "temperature": 0.7,
  "max_tokens": 2048,
  "timeout": 30
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| host | string | http://localhost:11434 | Ollama服务的地址 |
| model | string | llama3 | 使用的模型名称 |
| temperature | number | 0.7 | 采样温度，控制随机性（0-2） |
| max_tokens | number | 2048 | 生成文本的最大token数 |
| timeout | number | 30 | 请求超时时间（秒） |

## 智能体配置详解 (`agent.json`)

智能体配置定义了Agent的核心行为特征和能力边界：

```json
{
  "name": "助手",
  "role": "你是一个有帮助的AI助手",
  "capabilities": ["对话", "问题解答", "代码生成"],
  "memory_size": 10,
  "response_style": "友好且专业"
}
```


| 配置项 | 类型 | 说明 |
|--------|------|------|
| name | string | 智能体的名称标识 |
| role | string | 系统提示词，定义Agent的角色和行为准则 |
| capabilities | string[] | Agent具备的功能能力列表 |
| memory_size | number | 对话历史保留的轮数 |
| response_style | string | 响应风格描述，影响语气和表达方式 |

## 配置加载机制

### Python端配置加载 (`llm_agents_common/config.py`)

Python端通过`config.py`模块统一管理配置加载：

```python
import json
import os
from typing import Dict, Any

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_configs()
        return cls._instance
    
    def _load_configs(self):
        base_path = os.path.join(os.path.dirname(__file__), '../../config')
        self.ollama = self._load_json(os.path.join(base_path, 'ollama.json'))
        self.agent = self._load_json(os.path.join(base_path, 'agent.json'))
    
    def _load_json(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_ollama_config(self) -> Dict[str, Any]:
        return self.ollama
    
    def get_agent_config(self) -> Dict[str, Any]:
        return self.agent

# 单例实例
config = Config()
```

### TypeScript端配置加载 (`shared/config.ts`)

TypeScript端提供类型安全的配置访问：

```typescript
export interface OllamaConfig {
  host: string;
  model: string;
  temperature: number;
  maxTokens: number;
  timeout: number;
}

export interface AgentConfig {
  name: string;
  role: string;
  capabilities: string[];
  memorySize: number;
  responseStyle: string;
}

export class Config {
  private static ollamaConfig: OllamaConfig;
  private static agentConfig: AgentConfig;

  static async load() {
    const [ollamaRes, agentRes] = await Promise.all([
      fetch('/config/ollama.json'),
      fetch('/config/agent.json')
    ]);
    
    Config.ollamaConfig = await ollamaRes.json();
    Config.agentConfig = await agentRes.json();
  }

  static getOllamaConfig(): OllamaConfig {
    return Config.ollamaConfig;
  }

  static getAgentConfig(): AgentConfig {
    return Config.agentConfig;
  }
}
```

## 配置使用示例

### Python端使用

```python
from llm_agents_common.config import config

# 获取Ollama配置
ollama_config = config.get_ollama_config()
print(f"Connecting to {ollama_config['host']} using model {ollama_config['model']}")

# 获取智能体配置
agent_config = config.get_agent_config()
system_prompt = agent_config['role']
```

### TypeScript端使用

```typescript
import { Config } from './shared/config';

// 初始化加载配置
await Config.load();

// 使用配置
const ollamaConfig = Config.getOllamaConfig();
console.log(`Using model: ${ollamaConfig.model}`);

const agentConfig = Config.getAgentConfig();
console.log(`Agent name: ${agentConfig.name}`);
```

## 环境变量覆盖

虽然当前实现主要依赖JSON文件，但配置系统设计支持通过环境变量覆盖：

- `OLLAMA_HOST` 可覆盖 `ollama.json` 中的 `host`
- `OLLAMA_MODEL` 可覆盖 `ollama.json` 中的 `model`
- `AGENT_NAME` 可覆盖 `agent.json` 中的 `name`
- `AGENT_ROLE` 可覆盖 `agent.json` 中的 `role`

在生产环境中，建议通过环境变量管理敏感信息和环境特定配置。

## 最佳实践

1. **分离关注点**：将模型服务配置与智能体行为配置分离，便于独立管理
2. **类型安全**：在TypeScript端使用接口确保配置访问的类型正确性
3. **单例模式**：Python端采用单例模式避免重复加载配置文件
4. **异步加载**：TypeScript端使用异步加载适应前端环境
5. **编码统一**：所有JSON文件使用UTF-8编码确保中文字符正确显示

## 配置更新与重载

当前实现中，配置在应用启动时加载一次。如需在运行时更新配置：

1. 修改对应的JSON文件
2. 重启应用以重新加载配置
3. 生产环境可考虑实现配置热重载机制（如文件监听或消息通知）

对于频繁变更的配置项（如温度参数），建议通过运行时API动态调整，而非修改配置文件。
