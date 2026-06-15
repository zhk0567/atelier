# atelier 生产部署检查清单

供阿里云 ECS 首次部署与课程大作业第 4 章「部署与测试」对照使用。详细命令见仓库根目录 [README.md](../README.md)。

## 1. 云资源

- [ ] ECS 已创建（建议 Alibaba Cloud Linux 3，1 核 2G 及以上）
- [ ] 公网 IP 或弹性 IP 已绑定
- [ ] 安全组入方向：22（SSH）、80（HTTP）、443（HTTPS）
- [ ] 域名 A 记录指向 ECS 公网 IP

## 2. 系统软件

```bash
sudo dnf install -y python3.11 python3.11-pip git nginx certbot python3-certbot-nginx firewalld
sudo systemctl enable --now firewalld
sudo firewall-cmd --permanent --add-service={ssh,http,https}
sudo firewall-cmd --reload
```

## 3. 应用代码

```bash
sudo git clone https://gitee.com/zhk567/atelier.git /opt/atelier
cd /opt/atelier
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip && pip install -r requirements.txt
```

- [ ] 使用 **Python 3.9+**（推荐 3.11），勿用系统默认 3.6

## 4. 进程管理

```bash
sudo useradd -r -s /sbin/nologin -d /opt/atelier atelier
sudo chown -R atelier:atelier /opt/atelier
# 复制 deploy/systemd/atelier.service.example → /etc/systemd/system/atelier.service
sudo systemctl daemon-reload && sudo systemctl enable --now atelier
```

- [ ] `systemctl status atelier` 为 active (running)
- [ ] `ATELIER_ENV=production` 已设置

## 5. Nginx 反向代理

- [ ] `deploy/nginx/nginx-http-snippet.conf` 已合并进 `/etc/nginx/nginx.conf` 的 `http {}`
- [ ] `deploy/nginx/atelier.conf.example` 已复制为 `/etc/nginx/conf.d/atelier.conf` 并修改 `server_name`
- [ ] `sudo nginx -t` 通过
- [ ] `sudo systemctl enable --now nginx`

## 6. HTTPS

```bash
sudo certbot --nginx -d zhkun.xyz -d www.zhkun.xyz
```

- [ ] 浏览器可访问 `https://` 且证书有效

## 7. 功能与安全验证

| 检查项 | 命令或操作 | 期望 |
|--------|------------|------|
| 本机应用 | `curl -I http://127.0.0.1:8000/` | HTTP 200 |
| 站点元信息 | `curl https://zhkun.xyz/api/site` | 仅 JSON 站点名，无路径泄露 |
| 安全头 | `curl -I https://zhkun.xyz` | 含 `X-Content-Type-Options`、`X-Frame-Options` |
| 探测拦截 | `curl -I https://zhkun.xyz/.env` | 404 |
| 首页 | 浏览器打开 `https://zhkun.xyz` | 正常渲染 |
| Wiki | 打开 `/docs/...` 任一项目页 | Markdown 正常 |
| 博客 | 打开 `/blog/...` | 正常 |

详见 [docs/SECURITY.md](../docs/SECURITY.md)。

## 8. 日常更新

```bash
cd /opt/atelier && git pull
source .venv/bin/activate && pip install -r requirements.txt
sudo systemctl restart atelier
```

### NyxViz 录屏静态资源

`git pull` **不会** 带上 `static/nyxviz/figures/`（体积大，未入库）。若录屏页 JS/CSS 404 或样式 MIME 为 `application/json`，说明服务器缺少 `assets/` 或 `figures/`。

在本机 Windows 执行（需 OpenSSH）：

```powershell
$env:NYXVIZ_INCLUDE_DAT = "1"
$env:ATELIER_SSH = "root@39.106.117.118"
$env:ATELIER_REMOTE = "/opt/atelier"
.\scripts\publish_nyxviz_to_server.ps1
```

详见 [docs/NYXVIZ_DEPLOY.md](../docs/NYXVIZ_DEPLOY.md)。

## 9. 截图存档（大作业）

按 `作业/截图/README-截图说明.md` 将控制台与终端截图保存到 `作业/截图/`，文件名与报告图号一致。
