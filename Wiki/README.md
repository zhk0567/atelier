# DeepWiki 本地导出文档

本目录存放通过 DeepWiki 生成的仓库 Wiki（Markdown），按仓库分文件夹。

| 仓库 | 目录 | 说明 |
|------|------|------|
| [Framework](https://github.com/zhk0567/Framework) | [Framework](./Framework/) | 多技术栈框架示例 |
| [Clothing---Classification](https://github.com/zhk0567/Clothing---Classification) | [Clothing-Classification](./Clothing-Classification/) | 服装图像深度学习分类 |
| [English-Speaking-Trainer](https://github.com/zhk0567/English-Speaking-Trainer) | [English-Speaking-Trainer](./English-Speaking-Trainer/) | Android 英语口语训练应用 |
| [Intelligent-Learning-Terminal](https://github.com/zhk0567/Intelligent-Learning-Terminal) (`guyunxinchuan`) | [Intelligent-Learning-Terminal-guyunxinchuan](./Intelligent-Learning-Terminal-guyunxinchuan/) | 智能学习终端（古云心传分支） |
| [NEXUS](https://github.com/zhk0567/NEXUS) | [NEXUS](./NEXUS/) | NEXUS 项目 |
| [Algorithm](https://github.com/zhk0567/Algorithm) | [Algorithm](./Algorithm/) | 算法学习与实现 |

每个子目录包含：

- `index.md` — 总目录与页面链接
- `page-*.md` — 各专题页面（站点导航只暴露这些）
- `_source/` — 部分仓库的原始完整导出
- `_meta/` — DeepWiki 生成元数据（`wiki_structure.xml`、模型原文等），**不参与** `/docs/...` 导航，可忽略阅读

读者只需打开 `index.md` 与 `page-*.md`；维护或重新生成 Wiki 时再查看 `_meta/`。

重新生成示例（在 `api` 目录；`--out-dir` 相对仓库根，推荐 `Wiki/...`）：

```powershell
cd F:\commercial\deepwiki-open\api
python -m poetry run python ..\scripts\export_wiki_md.py `
  --repo-url https://github.com/zhk0567/Intelligent-Learning-Terminal/tree/guyunxinchuan `
  --out-dir Wiki/Intelligent-Learning-Terminal-guyunxinchuan `
  --language zh --comprehensive
# 若已有 wiki_structure_model_raw.txt，仅生成页面：
#   ... --pages-only
python ..\scripts\organize_wikis.py
```
