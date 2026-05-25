<!-- wiki_page_id: page-11 -->

# 快速开始与环境搭建

## 前置条件

在开始之前，请确保您的系统满足以下要求：
- Windows 10 或更高版本
- PowerShell 5.1 或更高版本
- Git 已安装并可在命令行中使用
- 具有管理员权限的终端

## 一键安装脚本

本项目提供了 PowerShell 脚本来自动化环境搭建过程。主要脚本包括：

### bootstrap.ps1

此脚本负责初始化环境，包括：
- 检查系统要求
- 设置执行策略
- 下载必要的依赖

### install-all.ps1

此脚本执行完整的安装流程，包括：
- 安装 Python 依赖
- 配置虚拟环境
- 验证安装

## 安装步骤

### 步骤 1：克隆仓库

```powershell
git clone https://github.com/zhk0567/llm-agents.git
cd llm-agents
```

### 步骤 2：设置执行策略（如需要）

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 步骤 3：运行安装脚本

```powershell
.\scripts\install-all.ps1
```

此脚本将：
1. 自动调用 `bootstrap.ps1` 进行环境初始化
2. 创建 Python 虚拟环境
3. 安装 `python/requirements.txt` 中列出的所有依赖
4. 运行验证脚本确保安装成功

## 手动安装选项

如果您更喜欢手动安装，可以按照以下步骤操作：

### 创建虚拟环境

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 安装依赖

```powershell
pip install -r python/requirements.txt
```

### 验证安装

```powershell
python python/scripts/validate_stdout.py
```

## 依赖说明

项目依赖列表见 `python/requirements.txt`，主要包括：
- LLM 相关库（如 openai, anthropic）
- 数据处理工具
- 验证和测试框架

## 常见问题

### 执行策略错误

如果遇到执行策略错误，请以管理员身份运行 PowerShell 并执行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```

### 路径问题

确保在项目根目录下运行所有脚本，因为脚本依赖于相对路径来定位文件。

## 验证安装

安装完成后，运行验证脚本以确保一切正常工作：

```powershell
python python/scripts/validate_stdout.py
```

成功运行将显示验证通过的消息，表明环境已正确搭建。
