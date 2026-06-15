# NyxViz 录屏页静态部署（atelier）

录屏三栏页 `video.html` 以静态资源托管在 atelier。Nyx 体数据（~800MB）可 **同站自托管** 或 **外部 OSS**。

## 目录

| 路径 | 内容 |
|------|------|
| `static/nyxviz/video.html` | Vite 构建入口 |
| `static/nyxviz/assets/` | JS/CSS/workers |
| `static/nyxviz/stats/` | precompute JSON |
| `static/nyxviz/figures/` | 配图 PNG（~178MB，**不入 git**） |
| `static/nyxviz/Nyx/` | 体数据 `.dat`（可选，同站托管时） |
| `/static/nyxviz/runtime-config.js` | **运行时** Nyx URL（由 FastAPI 从 `site.local.json` 生成） |

## 构建与同步

```powershell
Set-Location F:\commercial\atelier

# 构建 + 同步 figures/assets（figures 必须上传到生产）
.\scripts\sync_nyxviz_video.ps1

# 同站托管 .dat（约 800MB，无需 OSS / 子域名）
$env:NYXVIZ_INCLUDE_DAT = "1"
.\scripts\sync_nyxviz_video.ps1

.\scripts\verify_nyxviz_static.ps1
```

## 站点配置（`config/site.local.json`）

`.dat` 地址由 **`nyxviz.nyx_data_base`** 控制，**无需重新构建前端**即可切换。

### 方案 A：同站自托管（推荐，无需 `data.zhkun.xyz` DNS）

```json
{
  "nyxviz": {
    "video_path": "/static/nyxviz/video.html",
    "nyx_data_base": "/static/nyxviz/Nyx/",
    "nyx_data_origin": ""
  }
}
```

服务器上需存在 `static/nyxviz/Nyx/0000.dat` … `0099.dat`（`NYXVIZ_INCLUDE_DAT=1` 同步，或 scp 上传）。

### 方案 B：阿里云 OSS 公网地址

```json
{
  "nyxviz": {
    "video_path": "/static/nyxviz/video.html",
    "nyx_data_base": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/nyx/",
    "nyx_data_origin": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com"
  }
}
```

上传脚本：`.\scripts\upload_nyx_to_oss.ps1`（需配置 `OSS_BUCKET`）。

### 方案 C：自定义 CDN 域名

仅当 **DNS 已解析** 时使用，例如 `data.zhkun.xyz` CNAME 到 OSS：

```json
{
  "nyxviz": {
    "nyx_data_base": "https://data.zhkun.xyz/nyx/",
    "nyx_data_origin": "https://data.zhkun.xyz"
  }
}
```

若浏览器报 `ERR_NAME_NOT_RESOLVED`，说明该域名未配置，请改用方案 A 或 B。

## OSS CORS（仅方案 B/C）

- **AllowedOrigin**: `https://zhkun.xyz`, `http://127.0.0.1:8000`
- **AllowedMethod**: `GET`, `HEAD`
- **AllowedHeader**: `*`

同站方案 A 走 `'self'`，无需 CORS。

## 生产 ECS 上传

`git pull` **不会** 带上 `figures/` 与 `Nyx/`。在本机执行：

```powershell
$env:NYXVIZ_INCLUDE_DAT = "1"   # 若同站托管 .dat
$env:ATELIER_SSH = "root@39.106.117.118"
$env:ATELIER_REMOTE = "/opt/atelier"
.\scripts\publish_nyxviz_to_server.ps1
```

并在服务器 `/opt/atelier/config/site.local.json` 写入正确的 `nyx_data_base`。

## 常见错误

| 现象 | 原因 | 处理 |
|------|------|------|
| JS/CSS MIME `application/json` | 缺 `assets/` | `git pull` + publish 脚本 |
| `task1_evo_*.png` 404 | 缺 `figures/` | publish 脚本上传 figures |
| `data.zhkun.xyz` ERR_NAME_NOT_RESOLVED | 子域名未解析 | 改 `nyx_data_base` 为同站或 OSS 直链 |
| `.dat` CORS 错误 | OSS 未配 CORS 或 CSP 缺 origin | 配 CORS + `nyx_data_origin` |

## 访问入口

- 直接：`/static/nyxviz/video.html?record=1&scene=intro`
- 跳转：`/demo/nyxviz-video`
- 项目页：`/project/nyxviz`

## 11 个 scene

`intro`, `task1-tf`, `task1-morph`, `task2-evolution`, `task2-void`, `task2-cases`, `task2-spatial`, `task3-hist`, `task4-brush`, `task4-validate`, `findings`
