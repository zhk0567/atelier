# Framework 技术栈学习笔记

将 [zhk0567/Framework](https://github.com/zhk0567/Framework) 各子工程整理为 **官方指南体例**（导读、基础篇、子工程实战），无配图。

| 资源 | 说明 |
|------|------|
| [manifest.json](./manifest.json) | 124 篇 slug 索引 |
| [写作规范](./_meta/写作规范.md) | 文风与章节结构 |
| [人工撰写进度](./_meta/人工撰写进度.md) | 发布与端口备注 |
| 站点目录 | [/blog/series/framework](/blog/series/framework) |

**当前状态**：124 篇已在 manifest 中标记 `published`，站点可浏览。

日常维护（在 atelier 根目录）：

```powershell
Set-Location -LiteralPath 'F:\commercial\atelier'

# 结构 + 字数
python scripts/validate_guide.py --all-published --strict
python scripts/validate_guide_quality.py --all-published --strict

# 单篇改稿后发布
python scripts/publish_valid_guides.py <slug>

# 对照 Study 仓库扫描文档
python scripts/scan_framework_docs.py
```
