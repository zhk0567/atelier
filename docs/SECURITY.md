# 网站安全与防御

atelier 为只读个人站（无登录、无上传、无数据库）。防御采用 **Nginx → FastAPI 中间件** 分层，首期不强制 CDN。

## 架构

```
客户端 → Nginx（连接/请求限流、超时、安全头兜底）
      → uvicorn / FastAPI（TrustedHost、探测拦截、应用限流、安全头）
      → 只读路由 + 静态资源
```

| 层级 | 能力 |
|------|------|
| Nginx | `limit_req` / `limit_conn`、`client_max_body_size`、代理超时、`server_tokens off` |
| FastAPI | 安全响应头、常见扫描路径 404、生产环境 IP 限流、Host 白名单 |
| 应用逻辑 | Wiki slug 白名单 + 目录校验、壁纸路径 `relative_to(DATA_DIR)` |

模板文件：

- [`deploy/nginx/nginx-http-snippet.conf`](../deploy/nginx/nginx-http-snippet.conf) — 放入 `nginx.conf` 的 `http {}`
- [`deploy/nginx/atelier.conf.example`](../deploy/nginx/atelier.conf.example) — 站点反代
- [`deploy/systemd/atelier.service.example`](../deploy/systemd/atelier.service.example) — systemd 单元
- [`deploy/fail2ban/`](../deploy/fail2ban/) — 可选 Fail2ban（大量 404/429 临时封 IP）

## 环境变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `ATELIER_ENV` | `development` | `production` 启用 TrustedHost、限流、`/api/site` 信息收敛 |
| `TRUSTED_HOSTS` | `zhkun.xyz,www.zhkun.xyz,127.0.0.1,localhost` | 逗号分隔 Host 白名单 |
| `RATE_LIMIT_DEFAULT` | `120/minute` | 普通页面每 IP 配额（仅 production） |
| `RATE_LIMIT_WALLPAPER` | `30/minute` | `/wallpaper/` 配额（仅 production） |
| `BLOCK_PROBE_PATHS` | `1` | `1`/`true` 拦截 `/.env`、`/wp-admin` 等探测路径 |

本地开发无需设置；生产 systemd 示例已包含 `ATELIER_ENV=production`。

## 生产部署检查清单

1. **systemd**：使用 [`deploy/systemd/atelier.service.example`](../deploy/systemd/atelier.service.example)，以非 root 用户 `atelier` 运行
2. **Nginx**：合并 http 片段 + 站点 conf，`sudo nginx -t && sudo systemctl reload nginx`
3. **HTTPS**：`certbot --nginx`（见 [README](../README.md)）
4. **防火墙**：仅开放 22 / 80 / 443
5. **Fail2ban**（可选）：复制 fail2ban example 并启用
6. **验证**：
   - `curl -I https://zhkun.xyz` 含 `X-Content-Type-Options`、`X-Frame-Options`
   - `curl https://zhkun.xyz/api/site` 仅含 `site_name`、`site_title`（无服务器路径）
   - `curl -I https://zhkun.xyz/.env` → 404

## 日志与排查

| 来源 | 命令 / 路径 |
|------|-------------|
| 应用 | `journalctl -u atelier -f` |
| Nginx 访问 | `/var/log/nginx/access.log` |
| Nginx 错误 | `/var/log/nginx/error.log` |
| 429 限流 | access.log 或应用响应 `Retry-After` |

开发环境 (`ATELIER_ENV=development`) 不限流，便于本地调试。

## 何时接入 CDN / WAF

在以下情况考虑 **Cloudflare 免费版**（DNS 代理）或阿里云 DDoS 高防：

- ECS 带宽或 CPU 长期打满
- 单一源 IP 无法靠 Nginx + 应用限流挡住
- 需要隐藏源站 IP

接入后保留 Nginx 限流作为第二道防线；`X-Forwarded-For` 将由 Cloudflare 传递，应用层限流仍按首段 IP 计数。

## 本地验证安全头

```powershell
Set-Location F:\commercial\atelier
$env:ATELIER_ENV = "production"
python -c "from app import app; print('ok')"
# 启动后:
curl.exe -I http://127.0.0.1:8000/
```

## 明确未覆盖（首期）

- 用户认证 / CSRF（站点无写操作）
- Redis 分布式限流（单实例 ECS 不需要）
- 严格 CSP nonce（模板含大量 inline style/script，当前为 pragmatic CSP）
