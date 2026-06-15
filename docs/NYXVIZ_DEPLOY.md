# NyxViz 录屏页静态部署（atelier）

录屏三栏页 `video.html` 以静态资源托管在 atelier，Nyx 体数据（~800MB）放在外部 OSS/CDN。

## 目录

| 路径 | 内容 |
|------|------|
| `static/nyxviz/video.html` | Vite 构建入口 |
| `static/nyxviz/assets/` | JS/CSS/workers |
| `static/nyxviz/stats/` | precompute JSON |
| `static/nyxviz/figures/` | 配图 PNG |
| OSS `nyx/*.dat` | 100 步体数据 |

## 构建与同步

```powershell
Set-Location F:\commercial\atelier

# 1) 上传体数据到 OSS（首次）
$env:NYXVIZ_ROOT = "F:\commercial\NyxViz"
$env:OSS_BUCKET = "oss://your-bucket/nyx"
.\scripts\upload_nyx_to_oss.ps1

# 2) 构建并同步前端 + figures 到 static/
$env:VITE_NYX_DATA_BASE = "https://data.zhkun.xyz/nyx/"
.\scripts\sync_nyxviz_video.ps1

# 3) 校验本地 bundle 完整
.\scripts\verify_nyxviz_static.ps1
```

### Git 与生产部署

| 路径 | 是否入库 | 说明 |
|------|----------|------|
| `static/nyxviz/video.html` | 是 | 与 assets 哈希需同步更新 |
| `static/nyxviz/assets/` | **是**（~1.3MB） | 缺此目录会导致 JS/CSS 404，浏览器报 MIME `application/json` |
| `static/nyxviz/stats/` | 是 | |
| `static/nyxviz/figures/` | **否**（~178MB） | 部署时必须单独上传到服务器 |

**生产 ECS 上传（推荐）** — 在本机构建后 scp 整包：

```powershell
$env:VITE_NYX_DATA_BASE = "https://data.zhkun.xyz/nyx/"
$env:ATELIER_SSH = "root@你的ECS公网IP"
$env:ATELIER_REMOTE = "/opt/atelier"
.\scripts\publish_nyxviz_to_server.ps1
```

或在服务器上手动 rsync/scp 本机 `static/nyxviz/figures/` 与 `assets/`（若 `git pull` 后仍缺 figures）。

应用启动时会打印 `[atelier] WARNING: nyxviz: ...` 若 bundle 不完整。

## OSS CORS

在阿里云 OSS 控制台为 bucket 配置跨域：

- **AllowedOrigin**: `https://zhkun.xyz`, `http://127.0.0.1:8000`
- **AllowedMethod**: `GET`, `HEAD`
- **AllowedHeader**: `*`

## 站点配置

`config/site.local.json`:

```json
{
  "nyxviz": {
    "video_path": "/static/nyxviz/video.html",
    "nyx_data_origin": "https://data.zhkun.xyz"
  }
}
```

`nyx_data_origin` 会写入 CSP `connect-src`，允许录屏页 fetch `.dat`。

## 访问入口

- 直接：`/static/nyxviz/video.html?record=1&scene=intro`
- 壳页：`/demo/nyxviz-video`（全屏 iframe）
- 项目页：`/project/nyxviz` → 「录屏演示」

## 11 个 scene

`intro`, `task1-tf`, `task1-morph`, `task2-evolution`, `task2-void`, `task2-cases`, `task2-spatial`, `task3-hist`, `task4-brush`, `task4-validate`, `findings`

示例：`?record=1&scene=task4-brush`
