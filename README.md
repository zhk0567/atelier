# atelier

个人站点（FastAPI + Jinja2）：首页、项目 Wiki、数据浏览（来自 `zhita_settings.xlsx`）。

## 目录结构

```
atelier/
├── main.py                 # 应用入口
├── site_data.py            # 从 xlsx 加载站点数据
├── site_identity.json      # 站点名称 / 标题
├── zhita_settings.xlsx     # 证书、爱好、书籍、文章等表格数据
├── run.ps1                 # 本地启动（默认 http://127.0.0.1:8000）
├── Blog/                   # 博客 Markdown 源稿（读者向）
├── Wiki/                   # 项目技术 Wiki（DeepWiki 导出）
├── static/                 # CSS / JS / 图片（运行时静态资源）
├── data/                   # 首页壁纸等媒体（勿放博客配图）
├── scripts/                # 证书图拉取、Wiki 纹理等工具脚本
└── templates/              # Jinja2 模板
```

## 内容分工

| 目录 | 用途 | 站点访问 |
|------|------|----------|
| `Blog/` | 博客文章 `index.md` + `images/` | `/blog/{slug}`（如 `/blog/jianpu`） |
| `Wiki/` | 按 GitHub 仓库分的项目文档 | `/docs/{wiki_slug}/{page}` |
| `zhita_settings.xlsx` | 竞赛证书、爱好、文章摘要等 | `/browse/{hub_id}` |

## 本地运行

```powershell
cd F:\commercial\atelier
.\run.ps1
```

浏览器打开 `http://127.0.0.1:8000`。

## 博客发布（可选）

1. 源稿在 `Blog/<文章名>/index.md`，配图在同目录 `images/`。  
2. 上线时可复制图片到 `static/blog/<slug>/`，并在 xlsx「文章」表增加摘要行。  
3. 详见 [Blog/README.md](./Blog/README.md)。

## Wiki 维护

见 [Wiki/README.md](./Wiki/README.md)。
