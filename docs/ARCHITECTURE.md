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
config/
  site.example.json
  projects.json
templates/  static/
```

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

## NyxViz 录屏静态 Demo

NyxViz 录屏三栏页（`video.html`，11 scene）以 Vite 静态产物接入，不依赖 Node 运行时：

| 资源 | 位置 | 说明 |
|------|------|------|
| HTML/JS/CSS | `static/nyxviz/` | `npm run build:atelier` + `scripts/sync_nyxviz_video.ps1` |
| figures / stats | `static/nyxviz/figures/`、`stats/` | 站点 static 托管 |
| Nyx `*.dat` | 外部 OSS/CDN | `VITE_NYX_DATA_BASE` 构建注入；CSP `connect-src` 见 `nyx_data_origin` |

入口：`/demo/nyxviz-video`（iframe 壳）、`/static/nyxviz/video.html?record=1&scene=intro`（直链）。部署步骤见 [NYXVIZ_DEPLOY.md](NYXVIZ_DEPLOY.md)。
