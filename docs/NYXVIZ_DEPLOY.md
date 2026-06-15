# NyxViz 录屏页静态部署（atelier）

录屏三栏页 `video.html` 以静态资源托管在 atelier。**默认仅使用预渲染 PNG 配图**，不部署 Nyx `.dat` 体数据（~800MB）。

## 目录

| 路径 | 内容 |
|------|------|
| `static/nyxviz/video.html` | Vite 构建入口 |
| `static/nyxviz/assets/` | JS/CSS/workers |
| `static/nyxviz/stats/` | precompute JSON |
| `static/nyxviz/figures/` | 配图 PNG（~178MB，**已入库**） |
| `/static/nyxviz/runtime-config.js` | 运行时模式（由 FastAPI 从 `site.local.json` 生成） |

`.dat` 体数据目录 `static/nyxviz/Nyx/` **不入 git**，静态配图模式下也不需要。

## 构建与同步

```powershell
Set-Location F:\commercial\atelier

# 构建 NyxViz 并同步 assets/stats/figures 到 static/nyxviz/
.\scripts\sync_nyxviz_video.ps1

.\scripts\verify_nyxviz_static.ps1
```

figures 来自 NyxViz 仓库 `docs/figures/`，同步脚本会自动复制。

## 站点配置（`config/site.local.json`）

默认 **静态配图模式**（无需 `.dat`、无需 OSS）：

```json
{
  "nyxviz": {
    "video_path": "/static/nyxviz/video.html",
    "static_figures_only": true,
    "nyx_data_base": "",
    "nyx_data_origin": ""
  }
}
```

`runtime-config.js` 会设置 `window.__NYX_STATIC_ONLY__=true`，录屏页中栏显示 `figures/task1_vol_tXXXX.png`，不再请求 `.dat`。

### 可选：交互式体渲染（需 .dat）

若需要实时 VTK 体渲染，关闭静态模式并配置 `.dat` 来源：

```json
{
  "nyxviz": {
    "static_figures_only": false,
    "nyx_data_base": "/static/nyxviz/Nyx/",
    "nyx_data_origin": ""
  }
}
```

同站托管时在本机执行 `$env:NYXVIZ_INCLUDE_DAT = "1"; .\scripts\sync_nyxviz_video.ps1`，再 scp 上传 `Nyx/`（见 `scripts/upload_nyxviz_dat.ps1`）。

或使用 OSS 公网地址：

```json
{
  "nyxviz": {
    "static_figures_only": false,
    "nyx_data_base": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/nyx/",
    "nyx_data_origin": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com"
  }
}
```

## 生产部署

**推荐**：`git pull` 即可拿到 `figures/` 与 `assets/`（静态配图模式）。

```powershell
# 服务器
cd /opt/atelier
git pull
# 确认 config/site.local.json 中 static_figures_only: true
```

若仅更新了 NyxViz 前端 bundle（无 figures 变更），本地构建后 commit + push 即可。

## 常见错误

| 现象 | 原因 | 处理 |
|------|------|------|
| JS/CSS MIME `application/json` | 缺 `assets/` | `git pull` 或运行 sync 脚本 |
| `task1_evo_*.png` 404 | 缺 `figures/` | `git pull`（figures 已入库） |
| `0000.dat` 404 | 仍为体渲染模式 | 设 `static_figures_only: true` |
| 中栏一直「加载密度场…」 | 未加载 runtime-config | 确认 `video.html` 引用了 `/static/nyxviz/runtime-config.js` |

## 访问入口

- 直接：`/static/nyxviz/video.html?record=1&scene=intro`
- 跳转：`/demo/nyxviz-video`
- 项目页：`/project/nyxviz`

## 11 个 scene

`intro`, `task1-tf`, `task1-morph`, `task2-evolution`, `task2-void`, `task2-cases`, `task2-spatial`, `task3-hist`, `task4-brush`, `task4-validate`, `findings`
