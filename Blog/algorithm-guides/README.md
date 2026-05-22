# Algorithm 算法与刷题指南

将 [zhk0567/Algorithm](https://github.com/zhk0567/Algorithm) 专题 `notes.md` 整理为站点双语教程（Python + C++ 同篇）。

| 资源 | 说明 |
|------|------|
| [manifest.json](./manifest.json) | 专题 slug 索引（约 82 篇，不含单题 LeetCode） |
| [写作规范](./_meta/写作规范.md) | 章节与字数 |
| [人工撰写进度](./_meta/人工撰写进度.md) | draft / published |
| 站点 | [/blog/series/algorithm](/blog/series/algorithm) |

维护（在 atelier 根目录，PowerShell）：

```powershell
Set-Location -LiteralPath 'f:\commercial\atelier'

# 从 Study 仓库刷新 manifest
python scripts/scan_algorithm_docs.py

# 结构 + 字数
python scripts/validate_algorithm_guide.py --slug <slug> --strict
python scripts/validate_algorithm_quality.py --slug <slug> --strict

# 仅生成空章节骨架（不填正文）
python scripts/generate_algorithm_skeleton.py --slug <slug>
```

默认 Study 路径：`F:\Study\Algorithm`（见 `config/site.local.json` 的 `algorithm_root`）。
