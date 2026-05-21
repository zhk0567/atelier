# atelier

个人站点（FastAPI + Jinja2）：首页、项目 Wiki、Framework 技术栈指南、数据浏览（来自 `zhita_settings.xlsx`）。

线上：<https://zhkun.xyz>（源码 [Gitee](https://gitee.com/zhk567/atelier)）

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
├── data/                   # 动态壁纸（wallpaper-NN-slug.ext + wallpapers.json）
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

依赖见 [`requirements.txt`](requirements.txt)（需 **Python 3.9+**，推荐 3.11）。

## 服务器部署（阿里云 ECS + Nginx + HTTPS）

环境示例：Alibaba Cloud Linux 3、域名 `zhkun.xyz` 解析到 ECS 公网 IP、安全组放行 `22` / `80` / `443`。

### 首次部署

```bash
sudo dnf install -y python3.11 python3.11-pip git nginx certbot python3-certbot-nginx firewalld
sudo systemctl enable --now firewalld
sudo firewall-cmd --permanent --add-service={ssh,http,https}
sudo firewall-cmd --reload

sudo git clone https://gitee.com/zhk567/atelier.git /opt/atelier
cd /opt/atelier
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

> 系统默认 `python3` 若为 3.6，**必须用 `python3.11`（或 3.9+）** 创建虚拟环境，否则无法安装 FastAPI。

**systemd**（`/etc/systemd/system/atelier.service`）：

```ini
[Unit]
Description=atelier personal site
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/atelier
Environment=PATH=/opt/atelier/.venv/bin
ExecStart=/opt/atelier/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now atelier
```

**Nginx**（`/etc/nginx/conf.d/atelier.conf`）反代到 `127.0.0.1:8000`，`server_name` 填你的域名后：

```bash
sudo nginx -t && sudo systemctl enable --now nginx
sudo certbot --nginx -d zhkun.xyz -d www.zhkun.xyz
curl -I http://127.0.0.1:8000
```

### 性能说明

- 默认壁纸为「无壁纸」，避免全站 MP4 解码导致卡顿；可在顶栏手动切换动态壁纸。
- 手机端（≤720px）自动禁用视频壁纸。
- Wiki/博客 Markdown 渲染结果会缓存在内存；静态资源带 7 天浏览器缓存。

### 更新站点

Gitee 推送后，在服务器执行：

```bash
cd /opt/atelier
git pull
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart atelier
```

### 动态壁纸命名

- 视频文件：`data/wallpaper-NN-<slug>.mp4`（如 `wallpaper-01-preview.mp4`）
- 清单与中文显示名：`data/wallpapers.json`（`id` / `file` / `label`，`default` 指定默认项）
- 新增壁纸：按上述格式放入 `data/`，在 `wallpapers.json` 的 `items` 中追加一项

## Framework 指南维护

```powershell
python scripts\assign_guide_toc.py
python scripts\validate_guide.py --all-published --strict
```

详见 [Blog/framework-guides/README.md](./Blog/framework-guides/README.md)。

## Wiki 维护

见 [Wiki/README.md](./Wiki/README.md)。
