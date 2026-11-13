# atelier 架构说明

## 内容分工

| 路径 | 体裁 | 站点 URL |
|------|------|----------|
| `Blog/framework-guides/` | 124 篇技术栈**官方指南**（人工精写） | `/blog/series/framework`、`/blog/{slug}` |
| `Blog/algorithm-guides/` | 82 篇 Algorithm **专题双语指南** | `/blog/series/algorithm`、`/blog/{slug}` |
| `Blog/standalone/manifest.json` | 课程笔记、专题等独立博文索引 | `/blog/series/course-notes`、`/blog/series/topics`、`/blog/{slug}` |
| `Blog/数据可视化-第九章/` 等 | 课程章节正文（manifest 注册，文件夹可位于 `Blog/` 根下） | `/blog/dataviz-ch09` 等 |
| `Blog/hotspot/` | 热点观察 | `/blog/series/hotspot` |
| `Wiki/{project}/` | DeepWiki 导出的**项目文档** | `/docs/{wiki_slug}/{page}` |
| `zhita_settings.xlsx` | 证书、爱好、书籍等表格 | `/browse/{hub_id}` |
| `data/personal.json` | 个人要求与未来任务（人工整理、姓名首拼化） | `/personal` |
| `instance/personal_wishes.sqlite3` | 访客愿望（运行时 SQLite，不进仓库） | `/personal`、`/ops/.../wishes` |

**易混点**：`Wiki/Framework/` 与 `Blog/framework-guides/` 都关于 GitHub `zhk0567/Framework`，但前者是 Wiki 分页导出，后者是读者向教程；URL 与目录均已分离。Algorithm 专题教程在 `Blog/algorithm-guides/`，源码在 GitHub `zhk0567/Algorithm`；单题 LeetCode 题解不在 atelier 展开。

## 运行时结构

```
main.py              → uvicorn 入口
app/
  config.py          → config/*.json + FRAMEWORK_ROOT
  constants.py       → UI 文案、站点身份
  context.py         → Jinja 公共 context、壁纸
  projects.py        → config/projects.json + xlsx 合并
  routes/            → FastAPI 路由
  markdown/          → 博客 / Wiki 渲染
site_data.py         → xlsx 解析、manifest 聚合
data/personal.json   → 个人要求 / 未来任务（人工维护）
app/wishes_store.py  → 访客愿望（instance/personal_wishes.sqlite3，待审/公开/驳回）
config/
  site.example.json
  projects.json
templates/  static/
```

**愿望流**：`/personal` 右下角按钮 → 弹窗（或 `/personal/wish` 表单）→ `POST /personal/wish` → `personal_wishes`（pending）→ 管理员 `/ops/.../wishes` 编辑 / 通过 → `/personal` 的「03 新收到的愿望」。公开列表每次请求直接读 SQLite，`/personal` 因此使用 `no-cache`。

## Framework 指南流水线

```mermaid
flowchart LR
  study[F_Study_Framework]
  manifest[manifest.json]
  index[index.md per slug]
  validate[validate_guide.py]
  site[FastAPI /blog]
  study --> scan[scan_framework_docs]
  scan --> manifest
  manifest --> index
  index --> validate
  validate --> site
```

维护命令见 [Blog/framework-guides/README.md](../Blog/framework-guides/README.md)。

## Standalone 博文（课程笔记 / 专题）

独立博文在 [Blog/standalone/manifest.json](../Blog/standalone/manifest.json) 注册，字段含 `series`、`features`（如 `toc`、`pyecharts`）、`toc_depth`、`chapter`。新增章节只需追加 manifest 条目与对应 `Blog/{folder}/index.md`，无需改 Python 路由。

## 配置

复制 `config/site.example.json` 为 `config/site.local.json`（已 gitignore），设置本机 `framework_root`。环境变量 `FRAMEWORK_ROOT` 优先级最高。
