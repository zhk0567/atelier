# atelier

个人站点（FastAPI + Jinja2）：首页、项目 Wiki、Framework 技术栈指南、数据浏览（来自 `zhita_settings.xlsx`）。

## 目录结构

```
atelier/
├── main.py                 # uvicorn 入口
├── app/                    # FastAPI 应用（路由、渲染、配置）
├── site_data.py            # xlsx 与博客 manifest 数据
├── config/
│   ├── site.example.json   # 路径模板（复制为 site.local.json）
│   └── projects.json       # 首页项目卡片
├── site_identity.json
├── zhita_settings.xlsx
├── run.ps1
├── Blog/
│   ├── framework-guides/   # 124 篇 Framework 官方指南
│   └── 认识简谱/
├── Wiki/                   # 项目 DeepWiki 导出
├── docs/ARCHITECTURE.md    # Wiki vs Blog 分工说明
├── scripts/                # 指南校验与站点工具
├── static/
├── data/                   # 首页壁纸
└── templates/
```

## 内容分工

| 目录 | 用途 | 站点访问 |
|------|------|----------|
| `Blog/framework-guides/` | Framework 官方指南（124 篇） | `/blog/series/framework`、`/blog/{slug}` |
| `Wiki/` | 按仓库分的项目 Wiki | `/docs/{wiki_slug}/{page}` |
| `zhita_settings.xlsx` | 证书、爱好等 | `/browse/{hub_id}` |

详见 [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)。

## 本地配置

```powershell
Copy-Item config\site.example.json config\site.local.json
# 编辑 framework_root 为本机 Framework 源码路径
```

或设置环境变量：`$env:FRAMEWORK_ROOT = 'F:\Study\Framework'`

## 本地运行

```powershell
Set-Location -LiteralPath 'F:\commercial\atelier'
.\run.ps1
```

浏览器打开 `http://127.0.0.1:8000`。

## Framework 指南维护

```powershell
python scripts\assign_guide_toc.py
python scripts\validate_guide.py --all-published --strict
```

详见 [Blog/framework-guides/README.md](./Blog/framework-guides/README.md)。

## Wiki 维护

见 [Wiki/README.md](./Wiki/README.md)。
