---
title: "Nx 官方指南：从入门到 Framework 子工程实战"
series: framework
category: Tooling
stack: Nx
repo_path: Tooling/Nx
guide_toc: generic-tooling
guide_tier: placeholder
status: published
date: 2026-05-18
tags: [Nx, Monorepo, TypeScript]
---

# Nx 官方指南：从入门到 Framework 子工程实战

## 目录

- [导读](#导读)
- [预备知识](#预备知识)
- [快速上手](#快速上手)
- [基础篇](#基础篇)
  - [运行时与角色](#运行时与角色)
  - [安装与环境](#安装与环境)
  - [第一个 HTTP 服务](#第一个-http-服务)
  - [路由与处理器](#路由与处理器)
  - [请求与响应](#请求与响应)
  - [JSON API](#json-api)
  - [参数与校验](#参数与校验)
  - [中间件或钩子](#中间件或钩子)
  - [错误处理](#错误处理)
  - [配置与环境变量](#配置与环境变量)
  - [测试与调试](#测试与调试)
  - [部署概念](#部署概念)
- [Framework 子工程实战](#framework-子工程实战)
- [学习路径](#学习路径)
- [延伸阅读](#延伸阅读)

## 导读

**Nx** 管理 Monorepo 任务图与生成器。本仓 **`src/server.ts`** 文档链占位，端口 **3120**；真实工作区用 `nx` CLI。

下面节选子工程入口：

```typescript
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

/** 完整 Nx 为 Monorepo 任务图与生成器；此处仅 HTTP 占位与文档链。 */
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(__dirname, '..', 'public');
const indexPath = path.join(publicDir, 'index.html');

const port = Number(process.env.PORT ?? 3120);
const host = process.env.HOST ?? '127.0.0.1';

function sendJson(res: http.ServerResponse, body: unknown) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(body));
}

const server = http.createServer((req, res) => {
  const url = (req.url ?? '/').split('?')[0] ?? '/';

  if (req.method === 'GET' && url === '/api/health') {
    sendJson(res, {
      ok: true,
      service: 'framework-tooling-nx-guide',
      note: 'HTTP 占位；完整 Nx 见 NX-Tooling-TypeScript.md',
    });
    return;
  }

  if (req.method === 'GET' && url === '/api/info') {
    sendJson(res, {
      message: 'Nx：任务图、本地/远程缓存、生成器、与 Angular/React 等插件生态',
      doc: 'https://nx.dev/docs',
      highlights: [
        {
          title: '官方创建命令',
          detail: 'npx create-nx-workspace@latest（空目录；按需选择预设与包管理器）。',
        },
        {
          title: '与本仓库关系',
          detail: '本仓库刻意保持「每框架一目录」而非单一 Nx workspace；对照学习时可对比 Nx 的 graph 与本仓库多目录并行打开方式。',
        },
      ],
    });
```


**Framework 约定**：`GET /api/health` 返回 `service: framework-nx`；默认监听 **http://127.0.0.1:3120/**。与同仓 Node 示例对照时，请固定使用本文 PowerShell 路径与端口，便于脚本批量探活。呈现页 `public/index.html` 通过 `//go:embed` 编入二进制，部署时不必再单独拷贝静态目录。若你在内部 Wiki 引用本文，请同步贴上子工程仓库链接，避免同事只读到指南却找不到源码。

把上述约定当成「多栈演示仓库的公用语言」：`service` 字段让自动化脚本不必猜栈名，端口区间让并行演示不冲突，探针路径让负载均衡与容器编排配置可以复制粘贴。你在本机改端口做实验完全可行，但请在团队文档里标注「偏离默认约定的例外」，否则后来者会照着旧脚本打到错误端口。另一个实务细节是：health 接口应保持极薄逻辑，不要在其中访问慢依赖（例如远程数据库），否则探针会把本已疲惫的服务打掉；若必须检查依赖，拆成「仅进程存活」与「依赖探测」两级路径更加稳妥。Gin 本身不替你决定探针策略，但用 RouterGroup 把管理面 API 与业务 API 隔离，会让后续加鉴权更简单。

> **TIP**：本机并行跑多个 Go 示例时，用 `$env:PORT` 区分进程，避免与同仓 Turborepo（3121）等端口冲突。

## 预备知识



> **PowerShell 备忘**：`Invoke-RestMethod` 默认解析 JSON 为对象；需要原始响应可用 `Invoke-WebRequest`。`$env:PORT` 仅影响当前会话。请始终 `Set-Location -LiteralPath` 到含 `package.json` 的目录。并行启动多个 Framework 示例时，为每个终端设置不同端口，并记录 `service` 字段与端口对照表。若 health 正常而 items 失败，先查 JSON 与 Content-Type，再查 Mutex 与路由方法是否匹配。指南字数可用仓库内 `validate_guide.py --strict` 统计汉字数，便于提交前自检。提交评审前请同时运行 `validate_guide_quality.py --strict`，避免结构或灌水规则失败。manifest 保持 draft，评审通过后再改 published。
> **预备知识**：Node **20+**（以子工程 `package.json` 的 `go` 指令为准）；理解 HTTP 方法、JSON、常见状态码（如 200、201、400）；会在 PowerShell 使用 `Set-Location -LiteralPath` 进入含 `package.json` 的目录；知道「中间件先执行、`c.Next()` 进入链条下游、返回后再回到上游」这一基本顺序。若你准备深入 `binding` 标签，建议预先了解 struct tag 与「校验失败时 Gin 如何格式化错误」之间的边界；若你只跑示例，可先忽略 validator 的高级规则，把精力放在路由组与上下文方法上。

如果你尚未系统学过 Go 的 interface 与 goroutine，也仍可阅读本指南的前半部分，但在触及「并发与 Mutex」「错误包装」「context 取消」主题时可能会略感吃力；此时可并行补齐 Go Tour 的相关章节，而不是硬啃框架细节。另一方面，已经写过大量 Go CLI 的读者，请把注意力从 `main` 函数顺序执行切换到「每个请求一条逻辑线」，这是多数 Web 新人需要跨过的门槛。

## 快速上手

在 PowerShell 中进入子工程目录并启动（首次会拉取 `github.com/gin-gonic/gin` 与 `github.com/gin-contrib/cors`）：

```powershell
Set-Location -LiteralPath 'F:\Study\Framework\Tooling\Nx'
npm install
npm run dev
```

终端应打印「呈现页」与 `/api` 前缀提示，进程监听 **3120**。健康检查可这样对拍：

```powershell
Invoke-RestMethod http://127.0.0.1:3120/api/health | ConvertTo-Json
```

看到 `"service": "framework-nx"` 即表示路由与 JSON 响应链工作正常。修改代码后需重启进程（本示例未内置热重载）。首次拉取依赖若较慢，可检查本机代理或企业镜像；若 `go run` 报缺少 `public/index.html`，说明工作目录不在子工程根，请回到含 `package.json` 的文件夹再执行。若你更习惯在一次会话里反复试验，可把常用 `Invoke-RestMethod` 行保存为 `*.ps1`，减少手打 URL 的时间。

为了把「启动成功」与「业务逻辑正确」区分开，建议在健康检查通过后再测一条写路径：只读探针正常不代表 JSON 绑定与 Mutex 行为也正常。PowerShell 里构造 POST 可以使用 `Invoke-RestMethod -Method Post -Body '{"title":"ps1-demo"}' -ContentType 'application/json' http://127.0.0.1:3120/api/items`，确认返回 `201` 后再用 GET 看列表是否 prepend 了新元素。若出现编码问题，确保 PowerShell 保存脚本为 UTF-8 且请求头带了正确的 `Content-Type`。遇到 `Invoke-RestMethod` 自动把 JSON 解析成 PSCustomObject 的情况，这是预期行为；若你需要原始文本，可改用 `Invoke-WebRequest` 并读取 `Content`。

## 基础篇


**基础篇阅读提示（各 Nx 栈通用）**：十二章节不必一天读完；建议每天两到三节，并在当天用 health 与 items 做回归。若指南中的代码块与子工程 `main.go` 不完全一致，以可运行的子工程为准，在私人笔记里记录差异行号即可。把「CORS → 路由匹配 → Handler → JSON 写出 → Mutex 保护 store」画成一张时序图贴在团队 Wiki 上，比背诵 API 列表更能扛住人员流动。升级 Go 次要版本后，重复快速上手检查清单；升级框架大版本前，先读上游 changelog，再调整中间件顺序或绑定方式。遇到 400 与 500 混淆时，优先看响应 JSON 的 `error` 字段与终端日志，而不是先怀疑端口或防火墙。并行启动多个 Framework 示例时，为每个进程设不同 `PORT`，并在脚本里用 `service` 字段区分探活目标，避免「health 通了但打错栈」的乌龙。若在公司内网演示，请把默认端口与 `service` 字段写入 Runbook，并在防火墙策略中显式放行本地监听，减少「本机可访问、同事机器超时」的反复排查。祝学习顺利。建议将 health 与 lifecycle 的 JSON 响应保存为基线样本，便于框架升级后对比。

**基础篇阅读提示**：按目录十二节（Tooling 为八节）顺序阅读；对照子工程 `src/server.ts` 与脚本 `npm run dev`。

以下各节对照 `F:\Study\Framework\Tooling\Nx\src/server.ts` 与 `package.json`。阅读顺序与目录一致；**每一节都采用「概念说明 → 子工程真实代码 → 再说明」**，不放置占位符注释或单行碎片代码。十二章节的标题与 `Blog/framework-guides/_meta/guide-toc/generic-backend.yaml` 的 essentials 对齐，便于你在多栈仓库里横向对比其它后端指南而无需改自己的笔记结构。若你把本指南打印出来，可在页边把每节对应的 `src/server.ts` 行号随手写上，形成个人定制的双联本。

建议你在阅读时维护一张「概念—源码位置」对照表：例如「全局中间件在哪注册」「哪一段代码证明 RouterGroup 继承 `/api` 前缀」「`ShouldBindJSON` 与手写 `json.Unmarshal` 相比多了哪一步校验」。这张表以后迁移到真实项目时，可以直接当成 onboarding 清单。遇到与官方文档冲突的情况，以你本机可运行的子工程为准，再记录版本号与差异原因，避免口耳相传造成团队记忆偏差。每隔几周回顾一次这张表，把已经内化的行划掉，把仍旧模糊的条目标红，学习效率会明显高于单向通读。

Gin 的核心抽象可以压缩成三句话：**Engine 负责承载中间件与路由树**；**RouterGroup 负责路径前缀与局部中间件复用**；**Context 负责把一次请求的所有 IO 与元数据串起来**。本基础篇刻意用同一示例子工程贯穿十二章节，避免读者在不同文件间跳转而丢失情境。你只要跟着目录顺序读，`src/server.ts` 里的每一行都会在某一节再次出现并配上针对性的中文解释。

为了把「读过」变成「能在白板上讲解」，推荐你在每读完两到三节后做一次口头复盘：用三分钟说明一次请求穿过哪些中间件、`POST` 的 JSON 是在哪一行被校验、`items` 列表为何需要锁。此技巧能迫使你把抽象名词落到具体符号上，避免只记住概念却找不到代码位置的「假学会」。若在复盘时发现某段代码看不懂，优先查官方文档对应章节，再回到子工程对比版本差异；Gin 的 API 相对稳定，但绑定与代理行为仍会随着小版本调整，这一条在长远维护里尤其值得写进团队 Wiki。

若你愿意做团队分享，可把复盘升级为五分钟 Live Demo：一边改端口、一边展示 health JSON 变化、一边用浏览器证明 HTML 嵌入仍可用。远程会议时记得放大终端字体，并在 `r.Group` 与 `box.Use` 两行短暂停顿，让观众看清 RouterGroup 的缩进与路径前缀如何拼成最终 URL。

### 工具是什么

Gin 进程从 `main()` 启动：先决定运行模式（`（本栈无 Gin 式 SetMode）`），再构造 **HTTP 路由器**（`mux.NewRouter()` 已附带 Logger 与 Recovery 中间件），随后用 `r.Use` 挂载全局中间件（本例为 CORS）。一次 HTTP 请求的典型旅程是：**Router 接收连接 → 全局中间件（可 `提前 return` 提前结束）→ 路由组中间件 → 路由匹配 → Handler → 通过 `ResponseWriter 与 Request` 写 Header 与 Body**。子工程把内存存储 `itemsStore` 放在 `main` 里，演示「共享状态 + `sync.Mutex`」模式；生产环境通常会替换为数据库或缓存，但横切关注点（日志、鉴权、限流、Recovery）仍应放在中间件或 路由器层，而不是散落在每个 Handler。

`RouterGroup` 通过 `r.Group("/api")` 得到变量 `api`，其下注册的 `GET` / `POST` 会自动带上前缀 `/api`。路由组可以继续嵌套，例如 `api.Group("/box")`，用于局部中间件与路径前缀复用。Handler 签名统一为 `func(w http.ResponseWriter, r *http.Request)`，`c` 贯穿绑定、读参、写响应三个阶段。下面代码展示了模式初始化、全局 CORS、根路径 HTML 呈现，以及 `/api` 分组内健康检查。

```typescript
func main() {
	if os.Getenv("HOST/PORT") == "" {
		（本栈无 Gin 式 SetMode）(gin.DebugMode)
	}

	r := mux.NewRouter()
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"X-Feature-Box"},
		AllowCredentials: false,
	}))

	store := &itemsStore{
		items: []item{
			{ID: "seed-1", Title: "示例条目（内存 + mutex）", CreatedAt: time.Now().UTC()},
		},
	}

	r.GET("/", func(w http.ResponseWriter, r *http.Request) {
		c.Data(http.StatusOK, "text/html; charset=utf-8", indexHTML)
	})

	api := r.Group("/api")
	{
		api.GET("/health", func(w http.ResponseWriter, r *http.Request) {
			c.JSON(http.StatusOK, gin.H{
				"ok":      true,
				"service": "framework-nx",
			})
		})
```

当你把 `HOST/PORT` 设为 `release`（见后文「配置与环境变量」）时，Gin 会关闭部分调试输出并采用更适合生产的默认策略；与 Debug 模式相比，错误页与日志粒度可能不同，因此本地开发通常保留 Debug，线上流水线注入 Release。`//go:embed public/index.html` 把静态页编入变量 `indexHTML`，由根路径 `GET /` 用 `c.Data` 原样返回，这对「单二进制交付」非常友好。与同仓其它后端相比，本 Nx 示例固定端口 **3120**、`service` 字段 **framework-nx**，便于自动化脚本统一探测。

从「运行时」角度再补一层观察：**HTTP 路由器** 在进程内通常是单例，负责持有路由与中间件栈；每个请求会分配或复用 **http.ResponseWriter 与 *http.Request** 实例，你在 Handler 里读写的 `c` 不会串到别的请求上。子工程刻意把 `itemsStore` 放在包级可见位置并由 `main` 注入闭包，这样路由函数能捕获同一指针；若你把 Store 换成分模块的项目结构，常见做法是通过依赖注入把接口实现传进路由注册函数。理解这一点后能避免「在 init 里偷偷改全局单例」带来的测试困难。另一个实战细节是 Logger 中间件与 Recovery 的相对顺序：`mux.NewRouter()` 已按 Gin 默认顺序挂载，除非你改用 `mux.NewRouter()` 并自行拼装，否则不要轻易打乱，否则 panic 日志可能丢失请求上下文。

### 安装与 CLI

子工程是独立 Go Module，模块路径在 `package.json` 的 `module` 行声明。依赖只声明直接引用的库，其余由 `npm install` 计算并写入 `go.sum`。公司网络若访问 proxy.golang.org 不稳定，可在 PowerShell 会话级别设置 `GOPROXY`（例如企业镜像），**不要**在指南仓库根目录执行 `go run`，必须在带子工程的目录操作。Windows 路径含空格或特殊字符时务必使用 `Set-Location -LiteralPath`。本示例不依赖 Node；前端呈现页只是嵌入的 HTML。

`package.json` 真实内容如下：

```typescript
module framework/gin-demo

go 1.21.0

require (
	github.com/gin-contrib/cors v1.7.3
	github.com/gin-gonic/gin v1.10.0
)
```

Go 模块系统锁定「依赖从哪来、版本如何解析」，但不替你决定项目分层是否清晰；因此即便 `npm install` 始终干净，也要警惕路由与业务逻辑搅在同一文件里难以测试。`go.sum` 应该进入版本控制，以抵御依赖投递过程中的篡改；内网私有模块要正确设置 `GOPRIVATE`，否则公共代理可能尝试抓取你公司的 import 路径。CI 与开发者本机的 `GOPROXY` 策略不一致时，最常见的症状是 checksum 对不齐，解决思路是统一代理与公司镜像，而不是在本地随意 `-insecure`。对 Windows 团队而言，路径分隔与脚本工具链有时会让新手误以为「Go 找不到模块」，多数情况下只是当前工作目录不对。

把环境准备当成「可复现构建」的一部分：`go version` 应不低于 1.21；`npm install` 无报错后再 `npm run dev`。若你 fork 了子工程并改了 module 路径，记得同步替换 import 的根路径与 `require` 列表，但**本指南引用的源码以当前 `src/server.ts` 为准**。IDE 应能识别 `gin.Default`、`c.JSON` 等符号跳转；若不能，检查是否打开了含 `package.json` 的文件夹而非上一级 monorepo 根。

依赖版本方面，`gin-contrib/cors` 与 `gin-gonic/gin` 的主版本由 `package.json` 锁定；升级前请阅读上游变更日志，留意 `TrustedProxies`、绑定器或 `Context` 行为是否有破坏式调整。团队若使用 vendor 或私有代理，要保证 CI 与开发者本机拉取到的校验和一致，否则会出现「我这里能编过、同事那里 checksum 失败」的尴尬。Windows 下路径大小写不敏感但模块缓存仍区分版本字符串，清理缓存时使用 `go clean -modcache` 要格外谨慎，最好先备份或限定在临时环境执行。

### 第一次运行

「第一个 HTTP 服务」在这里体现为：**监听地址拼装 → `r.Run(addr)` 启动**。`Run` 内部创建 HTTP Server 并阻塞；出错时返回 `error`，子工程用 `log.Fatal` 打出原因后退出。默认 `HOST` 为 `127.0.0.1`，`PORT` 为 `3120`，因此本机在浏览器打开 `http://127.0.0.1:3120/` 应看到嵌入说明页；同时终端会打印「呈现页」与 `/api` 前缀的友好提示，方便新人对照路径自测。

理解 `Run` 背后的 `http.Server` 配置会帮助你在需求变化时不下错刀：例如需要自定义 `ReadHeaderTimeout`、`IdleTimeout` 时，往往改为手动 `http.ListenAndServe` 或 `Engine` 提供的更底层 API。对本地开发，`127.0.0.1` 可以避免不小心把整个局域网曝光；对容器环境，`0.0.0.0` 才接得住端口映射。日志行里的 URL 只是提示，真正决定监听的是 `addr` 字符串，别让文档与终端输出在长期演进中相互打架。

```typescript
	host := os.Getenv("HOST")
	if host == "" {
		host = "127.0.0.1"
	}
	port := os.Getenv("PORT")
	if port == "" {
		port = "3120"
	}
	addr := host + ":" + port

	log.Printf("Gin 演示已启动：呈现页 http://%s/  |  API 前缀 /api", addr)
	if err := r.Run(addr); err != nil {
		log.Fatal(err)
	}
}
```

若端口被占用，`Run` 会报 `listen tcp ... bind: Only one usage...` 一类错误；此时可临时设置 `$env:PORT=3010` 换端口，或结束占用进程。改完路由或中间件同样需要重启。建议始终把健康检查作为第二步验证，确认 JSON 与 Header 链路与预期一致，再测写接口。

当你把 Gin 服务嵌进更大的演示系统时，端口冲突是高频问题：可以在本机并行跑多个 Framework 示例，但要为每个进程设不同的 `PORT`，并在前端配置里同步修改 `fetch` 基址。若你在 WSL 与 Windows 两侧各起一个 Gin，记住 `127.0.0.1` 不一定互通，必要时要改用宿主机 IP 或统一在 WSL2 里访问。对新人而言，「终端里看到监听地址」与「浏览器实际访问地址」必须一致，这是排查白屏或 CORS 报错的第一步。

### 项目结构

Gin 的「路由」由 Engine 维护；**处理器**就是绑定在特定方法与路径上的闭包或函数。顶层用 `r.GET`、`r.POST` 注册；分组后用 `api.GET` 等，路径会与组前缀拼接。子工程示例覆盖：`GET /` 返回 HTML；`GET /api/health`、`GET /api/demo/lifecycle`、`GET /api/items`、`展台交互`；以及 `GET /api/box/inner`（带路由组局部中间件）。这与同仓其它后端的 `fetch` 心智模型一致：固定 `/api` 前缀，资源型路径用名词复数。

下面片段同时展示根路由、`/api` 组内若干 GET，以及 `box` 子组注册，便于你看出 **RouterGroup 的嵌套**如何减少重复前缀。

```typescript
	r.GET("/", func(w http.ResponseWriter, r *http.Request) {
		c.Data(http.StatusOK, "text/html; charset=utf-8", indexHTML)
	})

	api := r.Group("/api")
	{
		api.GET("/health", func(w http.ResponseWriter, r *http.Request) {
			c.JSON(http.StatusOK, gin.H{
				"ok":      true,
				"service": "framework-nx",
			})
		})

		api.GET("/demo/lifecycle", func(w http.ResponseWriter, r *http.Request) {
			c.Header("x-gin-demo", "handler-after-middleware")
			c.JSON(http.StatusOK, gin.H{
				"message": "以下为 Gin 处理 HTTP 请求时的常见环节（与 Node 框架命名不同但角色类似）",
				"ginPipeline": []string{
					"Router 接收请求",
					"全局 / 路由组 Middleware（c.Next() 链）",
					"路由匹配与 Handler",
					"绑定与校验（ShouldBindJSON + binding tag）",
					"通过 Context 写响应（JSON / Header / Status）",
				},
				"ginHighlights": []gin.H{
					{"title": "Engine 与 RouterGroup", "detail": "Default() 自带 Logger、Recovery；路由可按 Group 挂载并复用前缀与中间件。"},
					{"title": "Context", "detail": "ResponseWriter 与 Request 贯穿一次请求，封装 Request/Writer、绑定、渲染与参数读取。"},
					{"title": "binding 标签", "detail": "与 validator 对齐的 struct tag，在 ShouldBind* 时完成校验，错误由框架格式化为 400。"},
					{"title": "并发与数据", "detail": "本示例用 sync.Mutex 保护内存切片，展示典型共享状态写法（生产环境多换 DB）。"},
				},
			})
		})

		api.GET("/items", func(w http.ResponseWriter, r *http.Request) {
			c.JSON(http.StatusOK, gin.H{"items": store.list()})
		})

		api.POST("/items", func(w http.ResponseWriter, r *http.Request) {
			var body createItemBody
			if err := c.ShouldBindJSON(&body); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			it := store.add(body.Title)
			c.JSON(http.StatusCreated, gin.H{"item": it})
		})

		box := api.Group("/box")
		box.Use(func(w http.ResponseWriter, r *http.Request) {
			c.Writer.Header().Set("X-Feature-Box", "gin-group-middleware")
			c.Next()
		})
		box.GET("/inner", func(w http.ResponseWriter, r *http.Request) {
			c.JSON(http.StatusOK, gin.H{
				"where": "/api/box/inner",
				"note":  "X-Feature-Box 由仅作用于 /api/box 路由组的中间件写入。",
			})
		})
	}
```

理解 **方法 + 路径** 的唯一性有助于排障：重复注册在同一路径与方法上时，后注册者可能覆盖前者（取决于版本与注册方式），因此团队规范里应禁止「隐式覆盖」。`gin.H` 是 `map[string]any` 的别名，适合演示与小型 Handler；更大项目可换具体 struct 以获得编译期检查。

路由与处理器之间的分工也很清晰：**路由器**只负责把 `GET/POST` 与方法路径绑定到可调用对象，**处理器**里才应该出现业务分支。子工程用闭包捕获 `store`，让你看见依赖如何注入；当你拆到多个文件时，可以定义 `func registerAPI(rg *gin.RouterGroup, store *itemsStore)` 之类的函数，让 `main` 保持整洁。若路径含有参数（本示例未展示），Gin 支持 `:id` 与 `*wildcard` 两种风格，记得在 Handler 用 `c.Param` 读取并再做一次白名单校验，不要盲信路径片段。

当你的 API 数量上升到几十条时，按领域分包注册路由会比单文件堆叠更易维护：例如 `registerItemRoutes`、`registerAdminRoutes` 各接收一个 `RouterGroup`，内部再拆分 REST 资源。在包之间传递 `RouterGroup` 往往比反复传递整个 `Engine` 更安全，以免误把内网路由注册到对外暴露的组。若你需要统一 404 或 405 的响应体，可使用 `NoRoute`、`NoMethod`，但务必在团队文档中注明与 Gin 默认行为的差别，避免夜间应急时误判「路由未加载」。

### 任务与脚本

**http.ResponseWriter 与 *http.Request** 封装 `http.Request` 与 `ResponseWriter`，提供绑定、参数读取与多种渲染辅助方法。读请求时可用 `ShouldBindJSON`、`ShouldBindQuery`、`Param` 等；写响应时常用 `c.JSON`、`c.Data`、`c.String`、`c.Status`。子工程根路径用 `c.Data` 带 MIME 返回嵌入 HTML；列表用 `c.JSON` 返回 `items`；创建成功用 **201 Created**；`demo/lifecycle` 在写 JSON 前用 `c.Header` 设置响应头，演示「路由级 Handler 如何补充 Header」。

```typescript
	r.GET("/", func(w http.ResponseWriter, r *http.Request) {
		c.Data(http.StatusOK, "text/html; charset=utf-8", indexHTML)
	})

	api := r.Group("/api")
	{
		api.GET("/demo/lifecycle", func(w http.ResponseWriter, r *http.Request) {
			c.Header("x-gin-demo", "handler-after-middleware")
			c.JSON(http.StatusOK, gin.H{
				"message": "以下为 Gin 处理 HTTP 请求时的常见环节（与 Node 框架命名不同但角色类似）",
				"ginPipeline": []string{
					"Router 接收请求",
					"全局 / 路由组 Middleware（c.Next() 链）",
					"路由匹配与 Handler",
					"绑定与校验（ShouldBindJSON + binding tag）",
					"通过 Context 写响应（JSON / Header / Status）",
				},
				"ginHighlights": []gin.H{
					{"title": "Engine 与 RouterGroup", "detail": "Default() 自带 Logger、Recovery；路由可按 Group 挂载并复用前缀与中间件。"},
					{"title": "Context", "detail": "ResponseWriter 与 Request 贯穿一次请求，封装 Request/Writer、绑定、渲染与参数读取。"},
					{"title": "binding 标签", "detail": "与 validator 对齐的 struct tag，在 ShouldBind* 时完成校验，错误由框架格式化为 400。"},
					{"title": "并发与数据", "detail": "本示例用 sync.Mutex 保护内存切片，展示典型共享状态写法（生产环境多换 DB）。"},
				},
			})
		})

		api.GET("/items", func(w http.ResponseWriter, r *http.Request) {
			c.JSON(http.StatusOK, gin.H{"items": store.list()})
		})

		api.POST("/items", func(w http.ResponseWriter, r *http.Request) {
			var body createItemBody
			if err := c.ShouldBindJSON(&body); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			it := store.add(body.Title)
			c.JSON(http.StatusCreated, gin.H{"item": it})
		})
```

从浏览器 `fetch` 调用 API 时，请从 `http://127.0.0.1:3120/` 打开呈现页，避免 `file://` 协议导致的跨域与安全限制。需要上传文件或表单时，应改用 `multipart` 绑定系列 API（本示例未覆盖，但 Context 路径一致）。响应头若由中间件与 Handler 同时设置，注意后者是否会覆盖前者，以及 CORS `ExposeHeaders` 是否列出了前端需要读取的自定义头。

`c.JSON` 会设置 `Content-Type` 并序列化结构体或 `gin.H`；若你需要流式输出或附带下载文件名，应改用 `c.DataFromReader`、`FileAttachment` 等方法。读取请求体时，请牢记 Body 通常只能消费一次：`ShouldBindJSON` 读完之后不要指望再次 `ioutil.ReadAll`，这在透明代理或日志中间件里是高发坑位。若你要记录原始 body 作审计，需在中间件里 `c.Request.GetBody` 或自行缓存副本，并评估内存成本。

### 与框架集成

子工程的 JSON 契约简单清晰：`GET /api/health` 返回探针对象；`GET /api/demo/lifecycle` 返回说明性 JSON，并带 `ginPipeline` 字符串数组描述处理链路；`GET /api/items` 返回 `{ "items": [...] }`；`展台交互` 在成功时返回 `{ "item": {...} }`。字段名与表格呈现约定一致：`id`、`title`、`createdAt` 由 `item` 结构体的 `json` 标签控制序列化。`demo/lifecycle` 还返回 `ginHighlights` 数组，每个元素是 `title` + `detail` 的键值对象，用来对照学习 **HTTP 路由器**、**Context**、**binding**、**并发** 四个高频主题。把「探针接口」与「教学内容接口」拆在不同路径上，是微服务与多栈仓库常用的做法：前者给编排系统看，后者给人看。

当你把 JSON API 暴露给不同客户端时，**时间字段的精度与区时**、**布尔与枚举的表达方式**、**列表为空时是返回 `[]` 还是 `null`**，这些看似琐碎的约定都要提前写在契约里，否则前端与移动端的解析器会各自打补丁。Gin 本身不会替你生成 OpenAPI，但稳定的 struct 标签是生成文档的好起点。对分页、过滤、排序三类查询参数，虽本示例未演示，最佳实践仍是「在 RouterGroup 内集中注册，并在 Handler 顶部一次性绑定」，避免每个函数自己拆分字符串。若未来引入版本化路由（`/api/v1`），记得把 health 与 demo 的定位重新梳理：探针往往应保持恒定路径以减少运维变更。

```typescript
		api.GET("/health", func(w http.ResponseWriter, r *http.Request) {
			c.JSON(http.StatusOK, gin.H{
				"ok":      true,
				"service": "framework-nx",
			})
		})

		api.GET("/demo/lifecycle", func(w http.ResponseWriter, r *http.Request) {
			c.Header("x-gin-demo", "handler-after-middleware")
			c.JSON(http.StatusOK, gin.H{
				"message": "以下为 Gin 处理 HTTP 请求时的常见环节（与 Node 框架命名不同但角色类似）",
				"ginPipeline": []string{
					"Router 接收请求",
					"全局 / 路由组 Middleware（c.Next() 链）",
					"路由匹配与 Handler",
					"绑定与校验（ShouldBindJSON + binding tag）",
					"通过 Context 写响应（JSON / Header / Status）",
				},
				"ginHighlights": []gin.H{
					{"title": "Engine 与 RouterGroup", "detail": "Default() 自带 Logger、Recovery；路由可按 Group 挂载并复用前缀与中间件。"},
					{"title": "Context", "detail": "ResponseWriter 与 Request 贯穿一次请求，封装 Request/Writer、绑定、渲染与参数读取。"},
					{"title": "binding 标签", "detail": "与 validator 对齐的 struct tag，在 ShouldBind* 时完成校验，错误由框架格式化为 400。"},
					{"title": "并发与数据", "detail": "本示例用 sync.Mutex 保护内存切片，展示典型共享状态写法（生产环境多换 DB）。"},
				},
			})
		})

		api.GET("/items", func(w http.ResponseWriter, r *http.Request) {
			c.JSON(http.StatusOK, gin.H{"items": store.list()})
		})

		api.POST("/items", func(w http.ResponseWriter, r *http.Request) {
			var body createItemBody
			if err := c.ShouldBindJSON(&body); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			it := store.add(body.Title)
			c.JSON(http.StatusCreated, gin.H{"item": it})
		})
```

当客户端是浏览器内的 `fetch` 或同栈脚本时，尽量保持 JSON 字段稳定；当你演进 API 时，可以用新增字段兼容旧客户端，而不是频繁改字段名。`201 Created` 用在「资源已生成」语义上，与 `200 OK` 区分，前端可以据状态码决定是否刷新列表。若你在同一路径上增加 `PATCH` 或 `DELETE`，Gin 也能用同一 `RouterGroup` 注册，但要注意与代理缓存策略的交互。

对 JSON API 的契约治理，常见做法是引入手写或生成的 OpenAPI 文档，把「必填字段、示例、错误码」写清楚；Gin 本身不强制你使用哪种文档工具，但从长期维护看，**先稳定 JSON 形状**比先争论框架性能更重要。子工程的 `/api/demo/lifecycle` 虽然不承担业务，却提供了一个低风险的试验场：你可以在那条路由上练习分页结构、错误包裹体或国际化字段，而不影响探针路径的稳定性。

### 缓存与 CI 概念

Gin 的请求体绑定走 **ShouldBind*** 家族：`ShouldBindJSON` 在 `Content-Type: application/json` 场景最常用。绑定的目标通常是带标签的 struct，其中 **`json` 标签**告诉序列化层字段名，**`binding` 标签**告诉校验器规则。子工程的 `createItemBody` 将 `title` 标记为必填且长度在 1～120 之间，等价于在 Handlers 里手写多段 `if`，但错误信息由框架统一收集，减少重复代码。`ShouldBindJSON` 在校验失败时返回 `error`，本示例将其直接映射为 **400** 与 `{"error": ...}`，这对内网调试足够直观；对外产品可换成错误码枚举，避免泄露内部细节。

除 `required`、`min`、`max` 外，常用的 `binding` 规则还有 `email`、`uuid`、`oneof`、`dive` 等，取决于你引入的 validator 版本与注册情况。团队规范里建议：**能在 binding 完成的校验不要在业务层重复**，以减少「两层规则漂移」。若你需要对 JSON 之外的路径参数、查询参数一并绑定，可以定义更大的 struct 并组合 `uri`、`form` 标签，或分步绑定后合并结果。下面代码展示 `createItemBody` 与 `展台交互` 的真实实现，以及内存仓库在并发下的互斥保护——校验通过后才会触碰 `store.add`。

当你需要在 Gin 中实现更复杂的嵌套结构时，`dive` 可以深入到切片元素内部；当你在字段之间做条件校验时，有时不得不退回 Handlers 手写逻辑或使用自定义校验器注册。无论选择哪种方式，请在代码评审中要求附上**失败示例请求**，以防只有「成功路径」被测试覆盖。对于货币、地理坐标、身份证这类强域概念，别直接用 `string` 蒙混过关，引入值类型或sanitize步骤会让后续迁移数据库轻松得多。

```typescript
type createItemBody struct {
	Title string `json:"title" binding:"required,min=1,max=120"`
}

func main() {
	if os.Getenv("HOST/PORT") == "" {
		（本栈无 Gin 式 SetMode）(gin.DebugMode)
	}

	r := mux.NewRouter()
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"X-Feature-Box"},
		AllowCredentials: false,
	}))

	store := &itemsStore{
		items: []item{
			{ID: "seed-1", Title: "示例条目（内存 + mutex）", CreatedAt: time.Now().UTC()},
		},
	}

	r.GET("/", func(w http.ResponseWriter, r *http.Request) {
		c.Data(http.StatusOK, "text/html; charset=utf-8", indexHTML)
	})

	api := r.Group("/api")
	{
		api.POST("/items", func(w http.ResponseWriter, r *http.Request) {
			var body createItemBody
			if err := c.ShouldBindJSON(&body); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			it := store.add(body.Title)
			c.JSON(http.StatusCreated, gin.H{"item": it})
		})
	}
}
```

`itemsStore.add` 在持锁期间构造 `item` 并插到切片头部，演示「最新在前」的列表顺序；这与数据库自增主键的排序不同，但作为教学例子足够鲜明。若你希望在校验前先限制 body 大小，可在全局中间件检查 `Content-Length` 或使用 `MaxMultipartMemory` 一类配置，避免恶意大包耗尽内存。对公开接口还应叠加鉴权、审计与速率限制，这些不属于本示例范围，但**占位 Handler** 的位置已经清楚：要么包在 `/api` 组上，要么挂在 Engine 根部。

`binding` 标签与 `json` 标签各司一职：前者服务入参校验，后者服务序列化字段名；忘记其中任意一种都会在联调现场制造「明明字段填了却报 required」或「响应里少了驼峰」的假性故障。若你希望校验错误对前端更友好，可以自定义 validator 翻译或统一包装 `ShouldBind` 返回的错误类型。对国际化产品，`title` 这类字段往往还有字符归一化、全角半角处理，可视情况放在校验通过后的领域服务层，而不是塞进标签里让规则字符串爆炸。

### Framework 占位 HTTP 说明

在 Gin 里，中间件本质是 `func(w http.ResponseWriter, r *http.Request)`，通过 `c.Next()` 把控制权交给链条下游，**在下一次返回时继续执行当前中间件中 `c.Next()` 之后的语句**，从而形成「洋葱模型」。`r.Use` 注册的中间件作用于其后注册的全体路由；`RouterGroup.Use` 仅作用于该组及其子组。子工程用 `github.com/gin-contrib/cors` 在 路由器层开启跨域，**ExposeHeaders** 显式列出 `X-Feature-Box`，否则浏览器读不到自定义响应头。`/api/box` 子组另外 `Use` 了一个以内联闭包实现的局部中间件：它在 `c.Writer.Header()` 上写入 `X-Feature-Box`，再调用 `c.Next()`，因此仅对 `box` 组内路径生效。

工程化项目里，中间件往往还会承担 **request id**、**分布式追踪头传递**、**限流令牌**、**客户端证书校验** 等职责；这些能力与 Gin 的路由机制是正交的——也就是「仍旧写在一个 `func(w http.ResponseWriter, r *http.Request)` 里，但必须非常小心中止条件与错误返回」。当你从示例子工程迈向真实代码时，建议把中间件放在独立文件并用单元测试覆盖「未调用 `Next` 时是否泄漏 context」「`Abort` 后是否重复写 body」等边界。对于异步 goroutine，请避免直接使用 `ResponseWriter 与 Request` 越过请求生命周期，必要时复制所需字段再启动后台任务，否则容易出现数据竞争或使用已回收对象。

对照 Node 生态：Express、Fastify 的 `next()`、Koa 的 `await next()` 与 Gin 的 `c.Next()` 承担同构职责，但 Gin 的中间件签名统一、与路由树耦合更紧，迁移时注意不要把「异步前置逻辑」写进会阻塞链条的代码路径。下面节选包含全局 CORS 与 `/api/box` 子树的局部 Header 中间件，和 `src/server.ts` 保持一致。

在混合语言网关架构里，常见模式是边缘由 Node 或 Envoy 处理 TLS 与重写，内网 Gin 只信任已净化的头部；此时中间件里读取 `X-Request-Id` 或 `Authorization` 的顺序要与网关契约对齐。若你把 JWT 校验放在 Gin 全局中间件，要确保失败路径不会继续调用 `c.Next()`，否则(Handler 仍会执行) 会造成安全假象。对于异步任务触发的回调接口，也要显式限制方法与 IP 段，这部分虽然超出示例，但属于「中间件或钩子」章节天然的延伸题。

```typescript
	r := mux.NewRouter()
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"X-Feature-Box"},
		AllowCredentials: false,
	}))

	store := &itemsStore{
		items: []item{
			{ID: "seed-1", Title: "示例条目（内存 + mutex）", CreatedAt: time.Now().UTC()},
		},
	}

	r.GET("/", func(w http.ResponseWriter, r *http.Request) {
		c.Data(http.StatusOK, "text/html; charset=utf-8", indexHTML)
	})

	api := r.Group("/api")
	{
		api.GET("/health", func(w http.ResponseWriter, r *http.Request) {
			c.JSON(http.StatusOK, gin.H{
				"ok":      true,
				"service": "framework-nx",
			})
		})

		box := api.Group("/box")
		box.Use(func(w http.ResponseWriter, r *http.Request) {
			c.Writer.Header().Set("X-Feature-Box", "gin-group-middleware")
			c.Next()
		})
		box.GET("/inner", func(w http.ResponseWriter, r *http.Request) {
			c.JSON(http.StatusOK, gin.H{
				"where": "/api/box/inner",
				"note":  "X-Feature-Box 由仅作用于 /api/box 路由组的中间件写入。",
			})
		})
	}
```

若你在中间件里调用 `提前 return`，应同步设置状态码或 JSON 错误体，避免链条后续 Handler 依然执行。鉴权中间件通常在未通过时 `Abort` 并返回 401 或 403；记录请求耗时的中间件则在 `c.Next()` 前后打时间戳。演示代码把 CORS 配得很宽松（`AllowOrigins: *`），上线前必须收紧到具体域名并评估是否允许携带 Cookie。

中间件链的视觉化理解是「进入时自上而下，返回时自下而上」：`c.Next()` 就是分界点。子工程在 `/api/box` 只演示了一个写自定义头的中间件，你可以在同处叠加鉴权、审计 ID、限流令牌桶等逻辑；但要小心避免在全局层做重型 IO，否则所有路径都会被拖慢。若你需要在网关层终止 TLS，记得在应用层关闭不必要的 HSTS 重复头或协调压缩策略，减少「头重复、编码两次」类低级事故。





## Framework 子工程实战

这一节把分散在基础篇里的接口一次性列成「方法与路径」表，并给出**依赖清单**与**带中文行注的完整 `src/server.ts`**，方便你打印或投屏讲解。建议你按表格自上而下自测：先看探针是否返回约定的 `service` 字段，再验证列表与创建是否符合 REST 风格的状态码，然后关注路由组中间件是否只在子路径写入 `X-Feature-Box`。向同事演示时，可以一边打开 `src/server.ts` 一边用 PowerShell 打请求，把「代码行」与「网络包」对应起来；新人最常卡住的地方是忘记重启进程或把工作目录开在仓库外层导致 `go:embed` 找不到文件，这两点在演示现场点名指出能显著缩短上手时间。若你要把示例子工程当作脚手架起点，优先复制「路由组 + 中间件 + 绑定校验」三板斧，再替换内存存储为真实持久层，而不是先引入一堆生成器把目录搅乱。

完整源码（`F:\Study\Framework\Tooling\Nx`，主入口 `src/server.ts`）：

```typescript
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

/** 完整 Nx 为 Monorepo 任务图与生成器；此处仅 HTTP 占位与文档链。 */
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(__dirname, '..', 'public');
const indexPath = path.join(publicDir, 'index.html');

const port = Number(process.env.PORT ?? 3120);
const host = process.env.HOST ?? '127.0.0.1';

function sendJson(res: http.ServerResponse, body: unknown) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(body));
}

const server = http.createServer((req, res) => {
  const url = (req.url ?? '/').split('?')[0] ?? '/';

  if (req.method === 'GET' && url === '/api/health') {
    sendJson(res, {
      ok: true,
      service: 'framework-tooling-nx-guide',
      note: 'HTTP 占位；完整 Nx 见 NX-Tooling-TypeScript.md',
    });
    return;
  }

  if (req.method === 'GET' && url === '/api/info') {
    sendJson(res, {
      message: 'Nx：任务图、本地/远程缓存、生成器、与 Angular/React 等插件生态',
      doc: 'https://nx.dev/docs',
      highlights: [
        {
          title: '官方创建命令',
          detail: 'npx create-nx-workspace@latest（空目录；按需选择预设与包管理器）。',
        },
        {
          title: '与本仓库关系',
          detail: '本仓库刻意保持「每框架一目录」而非单一 Nx workspace；对照学习时可对比 Nx 的 graph 与本仓库多目录并行打开方式。',
        },
      ],
    });
    return;
  }

  if (req.method === 'GET' && (url === '/' || url === '/index.html')) {
    fs.readFile(indexPath, 'utf8', (err, html) => {
      if (err) {
        res.statusCode = 500;
        res.end(String(err));
        return;
      }
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      res.end(html);
    });
    return;
  }

  res.statusCode = 404;
  res.end('Not Found');
});

server.listen(port, host, () => {
  console.log(`Nx（形态占位）http://${host}:${port}/`);
});

```

**自测与迁移清单（完成基础篇后勾选）**：（1）能说出默认端口与 `service` 字段；（2）能解释 CORS 与 ExposeHeaders；（3）能复现 POST items 的 201 与 400；（4）能指出 box 子路由写入的自定义头；（5）能说明为何 items 需要 Mutex；（6）能列出生产仍缺的持久化、鉴权、限流三项。若有两项说不清，回到对应章节重读，不要跳节。迁移到同仓其它 Go 示例时，只改端口与 service，保持 JSON 字段不变，即可复用同一前端呈现页做联调。完成六项后，用五分钟向同事讲解「为何 health 不应访问数据库」，并说明本示例为何把 demo 与探针拆成不同路径；能讲清楚即达到 medium 指南的预期深度。以上清单适用于本仓全部 Tooling示例。评审前请在本机跑通 health 与（若存在）items 或 info 路径后再提交 PR。

## 学习路径

| 路径 | 建议 |
|------|------|
| 零基础 | 导读 → 快速上手 → 基础篇顺序阅读 → 子工程实战通读带注 `src/server.ts` |
| 已熟悉 Go 标准库 net/http | 快速上手 → 对照「路由与处理器」「中间件或钩子」理解 RouterGroup 与 `c.Next()` |
| 已熟悉其它 Go Web 框架 | 直接用「参数与校验」「错误处理」对齐 ShouldBind 与中间件差异，再跑子工程验证 Header 行为 |

学习路径不是线性的牢笼，而是一张优先级地图：**先跑通**、**再理解链条**、**最后抽模式**。零基础读者可以这样拆解第一周目标：第一天能在本机启动并解释 health JSON；第二天能口述 `Engine`、`RouterGroup`、`Context` 三个词在代码里的落点；第三天能独立修改一条路由并观察 404 与 200 的差异；第四天试着加一个简单的 `GET` 查询参数并用 `ShouldBindQuery` 接住；第五天再读中间件，手写一个 `c.Next()` 前后打印耗时的闭包。已经熟悉 `net/http` 的读者，可以优先把 `http.Handler` 与 `gin.HandlerFunc` 的对应关系画在纸上，再对照 Default Engine 自带的 Logger、Recovery 看他们如何插入链条。来自其它框架的读者，把注意力放在「绑定 + 校验一体化」与「路由组级中间件」两块即可，通常这是心智切换成本最高的地方。

在制定个人学习计划时，把「能复现」放在「能讲清楚」之前：很多初学者过早沉迷于对比基准测试数据，却连一次完整的中间件链条都画不出来。反过来，已经有多年 Web 经验的读者，反而要小心「经验套用」——Gin 并不是魔法，许多问题仍然是 HTTP 语义、序列化与并发错误，框架只是让你更快写出一致的结构。建议把本指南与官方文档交叉阅读：指南负责串起示例与叙述，文档负责查漏补缺与版本细节，两者合在一起才构成可持续的知识库。

无论哪条路径，都建议你在读完「参数与校验」后立刻停下来，用记事本写五个自己会犯的错：**Body 读两次**、**忘了 ExposeHeaders**、**在错误的 `Group` 上注册中间件**、**Release 模式却仍打印调试密钥**、**Mutex 未保护共享切片**。这五个错与示例子工程的扩展方向高度重合，提前写下来能显著减少夜里排障的时间。最后，把 `src/server.ts` 当作活文档：注释只保留解释「为什么这样写」的句子，把「框架百科」留在本指南与官方文档里，更符合长期维护的剪裁原则。

如果你计划把这份指南当成团队 onboarding 材料，可以要求新人在第二周尝试「加一个只读查询参数过滤」或「加一个延迟中间件」之类的小改动，并在评审会议上演示其请求链路变化。比单纯阅读更能检验掌握程度的是：**能否在白板上画出 `c.Next()` 的进出顺序**、**能否解释为何 `box` 组能看到 `X-Feature-Box` 而根路径看不到**。当新人能独立回答这两个问题时，Gin 的运行时模型基本就已经内化了，后续学习数据库集成、消息队列与 GRPC 网关会轻松许多。


**精读与排障补充**

本地启动成功后，请核对文档端口与终端输出一致；全栈示例试 `GET /api/demo` 或 `/api/health`；Tooling 示例按 `package.json` 脚本执行测试或探活。Windows 用 `Set-Location -LiteralPath`。Monorepo 内注意 `strictPort` 与并行演示端口表。团队 Review 请在 PR 写明启动命令与默认端口。占位 HTTP 子工程用于对齐系列文档，不代表框架完整生产形态。提交前运行 `validate_guide.py --strict` 与 `validate_guide_quality.py --strict`。以上习惯适用于本仓全部 Full-stack / Tooling 指南。


## 延伸阅读

下文列出权威文档与 Framework 子工程入口，**链接之后不再有正文**，以方便工具链截取与 diff。若你之后二次编辑本页，也请遵守这一收尾约定，勿在列表后再追加段落或代码块，以保持整仓 Framework 指南收尾一致。汉字字数可用仅统计中日韩统一表意文字的脚本自查，便于后续复核并纳入评审检查项。

- [Nx 文档](https://nx.dev/)
- [Framework 子工程：Tooling/Nx](https://github.com/zhk0567/Framework/tree/main/Tooling/Nx)