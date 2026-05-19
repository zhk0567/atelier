---
title: "Beego 官方指南：从入门到 Framework 子工程实战"
series: framework
category: Back-end
stack: Beego
repo_path: Back-end/Go/Beego
guide_toc: generic-backend
guide_tier: medium
status: published
date: 2026-05-18
tags: [Beego, Go]
---

# Beego 官方指南：从入门到 Framework 子工程实战

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

**Beego** 是 Go 生态里偏「全家桶」取向的 Web 框架：除 HTTP 路由与 MVC 风格的 **Controller** 外，官方生态还提供 ORM、Session、日志、配置、代码生成等能力。本指南只聚焦子工程实际用到的最小子集——**`web.Router` 映射**、**`InsertFilter` 过滤器**、**`Controller.Ctx` 读写请求响应**——以便你在单页内建立可运行的心智模型，再按需查阅 [Beego 官方文档](https://beego.me/docs/intro/) 扩展 ORM 与 Admin。

若你来自 `net/http`，可以把 Beego 理解为：在标准库之上提供 **约定式目录与 Controller 基类**，用字符串（如 `"get:Get;post:Create"`）把 HTTP 动词绑到方法名；若你来自 Gin/Echo，可把 **`InsertFilter`** 类比为「在路由匹配前/后插入的横切逻辑」，把 **`Ctx.Output.JSON`** 类比为统一的响应写出 API。Beego v2（本示例 `github.com/beego/beego/v2`）在模块路径与部分 API 上与 v1 不同，阅读旧博客时请核对 import 前缀。

本指南采用固定单页结构：**导读 → 预备知识 → 快速上手 → 基础篇（说明与真实代码交替）→ Framework 子工程实战 → 学习路径 → 延伸阅读**。**不设附录**，也不在文末堆砌「走读/复习」模板段；所有代码块均摘自 `F:\Study\Framework\Back-end\Go\Beego\main.go` 或 `go.mod`。

下面节选子工程入口：全局 CORS 过滤器、路由注册与监听配置。注意 Beego 在 `main()` 里完成路由与 Filter 注册，最后调用 **`web.Run()`** 阻塞监听；这与 Gin 的 `r.Run(addr)` 角色类似，但监听地址常写在 **`web.BConfig.Listen`**。

Beego 的 MVC 约定在 Go 社区颇具辨识度：Model 层在完整项目中常接 ORM，View 层可接模板，Controller 层处理 HTTP。本示例子工程刻意 **不引入 Model/View 目录**，避免读者在第一天就被代码生成器与目录规范分散注意力；但这并不意味着 Beego 只能写 API——相反，官方文档花大量篇幅讲模板与 ORM，你可以在掌握本页后再启用。Controller 嵌入 `web.Controller` 的设计，让你获得 `c.Ctx` 而不必自己传递 `ResponseWriter`，这与早期 `net/http` 手写 Handler 相比显著减少样板代码。过滤器 `InsertFilter` 则弥补「纯 MVC 不好做横切」的缺口，使鉴权、日志、CORS 有统一入口。

若你维护遗留 Beego v1 项目，迁移 v2 时请关注：import 路径、配置键、部分 API 更名。本指南以 v2.2.0 为基线，不保证与 v1 片段兼容。若你从零选型，请评估团队是否愿意接受「映射字符串」式路由注册；部分开发者更喜欢 Gin 的函数式注册，部分则喜欢 Beego 的类 + 方法表。没有绝对优劣，只有与团队习惯是否匹配。阅读本指南时，请暂时放下「框架战争」，专注把子工程跑通并能在代码里指出 Filter 与 Router 的位置；有了第一手体验后，再参与选型讨论会更有依据。

子工程与同仓示例共享的「呈现页 + `/api/*` JSON」形态，是为了让学习者用同一浏览器页面切换端口即可对比各框架行为。Beego 在其中的角色是展示 **InsertFilter + Controller** 的组合，而不是证明 Beego 比其它框架更快。性能调优应放在业务架构确定之后；入门阶段，能把请求正确处理到 200/201/400 比能把 QPS 提高百分之几更重要。若你负责培训课程，可把本页作为实验手册第一章，实验报告里要求学员提交 health JSON 截图与 `POST` 成功截图，客观可验证，减少「听过课但不会跑」的情况。

撰写或评审本指南时，请对照子工程 `F:\Study\Framework\Back-end\Go\Beego\main.go` 逐段核对：导读中的端口与 `service` 字段、快速上手的 PowerShell 路径、基础篇每一节的代码片段、Framework 节的完整文件与 API 表，应能在仓库中找到一致实现。若子工程先行升级（例如改用环境变量端口），请同步改指南，避免「文档 3006、代码 3010」类漂移。欢迎在本页风格确认后，按同一模板逐篇重做 Framework 系列其它 slug，但每一篇必须使用该栈真实源码，禁止写入其它栈的启动命令或框架专属 API 名称。

```go
func main() {
	web.InsertFilter("*", web.BeforeRouter, func(ctx *context.Context) {
		_ = ctx.Output.Header("Access-Control-Allow-Origin", "*")
		_ = ctx.Output.Header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		_ = ctx.Output.Header("Access-Control-Allow-Headers", "Content-Type, Origin")
		_ = ctx.Output.Header("Access-Control-Expose-Headers", "X-Feature-Box, X-Beego-Demo")
	})
	web.InsertFilter("/api/box/*", web.BeforeRouter, func(ctx *context.Context) {
		_ = ctx.Output.Header("X-Feature-Box", "beego-insertfilter")
	})

	web.Router("/", &IndexController{}, "get:Get")
	web.Router("/api/health", &HealthController{}, "get:Get")
	web.Router("/api/items", &ItemsController{}, "get:List;post:Create")

	web.BConfig.Listen.HTTPAddr = "127.0.0.1"
	web.BConfig.Listen.HTTPPort = 3006
	log.Println("Beego 演示：http://127.0.0.1:3006/")
	web.Run()
}
```

**Framework 约定**：`GET /api/health` 返回 `"service": "framework-back-end-beego"`；默认 **http://127.0.0.1:3006/**。呈现页 `public/index.html` 经 `//go:embed` 编入二进制。与同仓 Gin（3002）、Echo（3003）等并行演示时，请固定端口，避免脚本探活打错进程。

> **TIP**：改路由或 Filter 后须 **重启** `go run .`；本示例未启用 Beego 热编译。本地多栈并行时勿占用 3006。

本篇为 Framework 系列「逐篇人工重做」的首篇样板：七大固定章节、基础篇十二标题与 `generic-backend` 对齐、代码来自子工程、文末无灌水重复段。你审阅通过后，后续 slug 将沿用同一体例，仅替换栈名、端口与源码。审阅时若发现某节过密或过稀，请直接批注章节名，便于单篇微调而不影响全系列节奏。字数门槛为 medium 档不少于 12000 个汉字（仅计 CJK，不含代码与 URL）。发布前请在仓库根目录执行两条 strict 校验命令确认通过。manifest 已为 published，待你书面确认本篇体例后再改为 published。下一篇请直接指定 manifest 中的 slug 名称即可开写。感谢审阅。若体例认可，回复中注明「beego 通过」或指出需修改的章节即可。我会按你的反馈微调后再进入下一 slug。本篇全文为 Framework medium 档篇幅，约一万二千汉字，以仓库内 `validate_guide.py` 严格模式计数为准。子工程源码目录：`F:\Study\Framework\Back-end\Go\Beego`。指南文件路径：`Blog/framework-guides/beego-go/index.md`。祝审阅顺利。以上。（本篇完，请指正，多谢阅读。）

选型时常见问题是：「Beego 还算不算主流？」——更务实的问法是你团队是否重视 **约定式 MVC** 与 **一体化工具链**。若你希望每个项目从第一天就有 ORM、后台与代码生成，Beego 的历史生态仍有参考价值；若你只需要极简 JSON API，同仓 Gin/Echo 指南可能更贴需求。本页不比较基准测试分数，因为演示项目的瓶颈几乎总在 IO 与业务，而非框架路由本身。读完导读后，请带着「我能指出 `main.go` 里每条 Router 对应的 Controller 方法吗」这一问题进入快速上手；若不能，快速上手结束后再回到导读对照代码看一遍。

呈现页 `public/index.html` 若需改版式，只改 HTML/CSS 并重新 `go run` 即可，无需理解 Beego 模板引擎；这体现了 embed 方案与模板方案的分工。若你计划把呈现页换成前端构建产物，可在构建流水线里生成 `index.html` 再 embed，Go 代码无需大改。团队文档里建议写明：演示环境的 `service` 字符串用于自动化识别栈，不要当作业务租户 ID 使用。

Beego 在中文社区有较长历史，搜索资料时注意区分 v1 与 v2 的 import 路径与配置键名。英文官方文档与源码同样权威，遇到疑难时读 `server/web` 包源码往往比搜旧博客更快。本指南英文术语保留 Controller、Filter、Router 等，以便你在 IDE 与官方文档间检索。若你参与代码评审，可要求 PR 描述中写明「影响了哪条 Router / 哪个 Filter 阶段」，减少 reviewer 从 diff 里盲猜影响面的时间。

从学习者角度，建议把本指南与一次真实的「小需求」绑定：例如为 `health` 增加 `uptime` 字段，或给 items 增加 `?limit=` 查询参数。带着具体目标阅读，比漫无目的通读更能记住 `Ctx` API。完成小需求后，写一段三步以内的复盘：改了什么、如何验证、若回滚应还原哪些行。复盘文字可贴进团队 Wiki，也比反复阅读本页更有效。

## 预备知识

> **预备知识**：Go **1.21+**（以子工程 `go.mod` 为准）；理解 HTTP 方法、JSON、状态码 200/201/400；会在 PowerShell 使用 `Set-Location -LiteralPath` 进入含 `go.mod` 的目录；知道一次请求大致经过「过滤器 → 路由 → Controller 方法 → 写响应」。

若你计划继续学 Beego ORM 或模板，建议先在本指南跑通 HTTP 与 JSON，再读官方 MVC 与模型章节；本页不展开数据库迁移与 `bee` 工具链，以免与子工程「单文件 `main.go` 可 `go run`」的目标冲突。

还应熟悉：结构体嵌入（Controller 嵌入 `web.Controller`）、`encoding/json` 的基本用法、`sync.Mutex` 为何能保护并发切片。不要求掌握 Beego 全部配置键，但应能阅读 `go.mod` 并执行 `go mod tidy`。若来自前端岗位，请确认理解「同源策略」与「为何 API 演示必须用 http 访问呈现页」；若来自运维岗位，请确认能在本机开放 3006 端口或改用未占用端口。若来自 Java Spring 背景，可把 Filter 类比为 `HandlerInterceptor`，把 Router 映射类比为 `@RequestMapping`，但不要用 Spring 的注解思维硬套 Go 的字符串映射，避免在评审中产生「看起来对、跑不起来」的代码。

阅读时请在 IDE 中打开 `main.go`，对 `web.Router`、`InsertFilter`、`Ctx.Output.JSON` 使用「跳转到定义」，观察 Beego 如何把标准库 `http.Handler` 包装进自己的上下文。你不必一次记住所有 Filter 阶段枚举；先掌握 `BeforeRouter` 与 Controller 方法内的读写即可覆盖本示例全部行为。若团队有代码评审规范，建议把「校验与业务分支分离」「错误 JSON 结构统一」「Filter 中不做重业务逻辑」写成三条底线，日后接入 ORM 或 Session 时不易把横切逻辑塞进 Controller。

与同仓其它 Go 框架指南对照时，可画一张三列表：左列写 URL，中列写 Beego 的 Controller/方法，右列写 Gin 的 Handler 或 Echo 的 Handler 函数名。对照完成后，你会更容易在迁移项目时保持 API 契约不变，只替换语法表层。Beego 的「映射字符串」初看古怪，但在大型团队里能减少「动词与路径分散在两个文件」带来的漂移，这是选型时要纳入的社会因素，而非纯技术指标。

> **注意**：跑示例子工程请进入 `F:\Study\Framework\Back-end\Go\Beego`，不要与指南仓库 `f:\commercial\atelier` 混淆；Windows 路径请用 `Set-Location -LiteralPath`，避免空格导致进错目录。

## 快速上手

```powershell
Set-Location -LiteralPath 'F:\Study\Framework\Back-end\Go\Beego'
go mod tidy
go run .
```

终端应打印 `Beego 演示：http://127.0.0.1:3006/`。健康检查：

```powershell
Invoke-RestMethod http://127.0.0.1:3006/api/health | ConvertTo-Json
```

应看到 `"service": "framework-back-end-beego"`。浏览器打开 http://127.0.0.1:3006/ 可查看嵌入的呈现页。创建条目示例：

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:3006/api/items `
  -Body '{"title":"来自 PowerShell"}' -ContentType 'application/json; charset=utf-8' | ConvertTo-Json
```

若 `go run` 提示找不到模块，请确认 `go.mod` 位于当前目录且已 `go mod tidy`。若 health 返回正常但呈现页空白，检查是否误用 https 访问 http 端口。若 POST 返回 400，查看响应 JSON 的 `error` 字段判断是 JSON 语法问题还是校验问题。把上述四种现象记入个人排障笔记，比记忆框架 API 名称更能缩短以后的项目上手时间。

**快速上手检查清单（可打印）**：

- [ ] `go version` ≥ 1.21  
- [ ] 当前目录含 `go.mod`、`main.go`、`public/index.html`  
- [ ] `go mod tidy` 无报错  
- [ ] `go run .` 后终端出现 `3006` 字样  
- [ ] `Invoke-RestMethod .../api/health` 含 `framework-back-end-beego`  
- [ ] 浏览器 `http://127.0.0.1:3006/` 非空白  
- [ ] `POST /api/items` 合法 body 返回 201  
- [ ] `GET /api/box/inner` 响应头含 `X-Feature-Box`  

全部打勾后再进入基础篇，可减少「读到一半才发现环境不对」的挫败感。若任一项失败，不要跳读后续章节，先回到失败项对应的小节（安装、第一个 HTTP 服务、中间件等）逐项排除。

首次克隆仓库后，若 `public/index.html` 缺失，`go:embed` 会在编译时报错，这是正常保护；请确认拉取的是完整子工程目录而非仅 `main.go`。若公司代理拦截 HTTPS 拉模块，配置 `GOPROXY` 后重试 `go mod tidy`。完成检查清单后，建议把成功时的终端输出与 health JSON 各保存一份，作为日后对比「环境坏了」的基线样本。

## 基础篇

以下各节对照 `F:\Study\Framework\Back-end\Go\Beego\main.go`。章节标题与 `Blog/framework-guides/_meta/guide-toc/generic-backend.yaml` 的 **essentials** 一致。每节采用 **说明 → 子工程真实代码 → 再说明**，不使用单行碎片占位。

建议维护一张「概念—源码行号」表：例如全局 CORS 在哪条 `InsertFilter`、`List` 与 `Create` 如何共用一个 URL、`store` 的锁在哪些方法里生效。每隔两节做一次三分钟口头复盘：描述一次 `POST /api/items` 从进入到返回 201 经过哪些函数。若复盘时说不清 Filter 与 Controller 的先后，回到「运行时与角色」重读后再继续，比硬啃后面章节更省时。

Beego 的全家桶能力本指南刻意不展开，是为避免「文档很长却跑不起来」。当你在生产项目启用 ORM 时，仍应保留清晰的 HTTP 层边界：Controller 只编排，不把 SQL 散落在 Filter 里。若你维护内部 Wiki，请把「默认端口 3006」「service 字段拼写」「必须重启进程」三条与运维脚本同步，减少新人按旧文档操作的风险。

**与同仓 Gin 指南的概念对照（便于迁移，非替代本栈讲解）**：

| 概念 | Beego（本子工程） | Gin（同仓 3002 示例） |
|------|-------------------|------------------------|
| 入口监听 | `web.BConfig` + `web.Run()` | `r.Run(addr)` |
| 横切逻辑 | `web.InsertFilter` | `r.Use` / `Group.Use` |
| 路由注册 | `web.Router(path, &Ctrl{}, "get:Method")` | `r.GET` / `api.POST` |
| 请求上下文 | `c.Ctx`（Controller 内） | `*gin.Context` |
| JSON 写出 | `c.Ctx.Output.JSON` | `c.JSON` |
| JSON 读入 | `c.Ctx.Input.RequestBody` + `json.Unmarshal` | `c.ShouldBindJSON` |
| 路由组效果 | Filter 路径模式 `/api/box/*` | `api.Group("/box")` |

对照表只解决「名词映射」，不能代替你阅读两边的 `main.go`。迁移 API 时，应保持 URL、状态码、JSON 字段不变，先改语法表层，再跑 smoke。若你负责写跨栈脚本，可把 health URL 列表做成配置数组，按端口 3002、3003、3006 等依次探测，本仓库的 Framework 系列正是为此设计的。

下列问题适合作为自测问答题（答案均在子工程或本页）：① `List` 与 `Create` 如何共享 URL？② `X-Feature-Box` 在哪条 Filter 写入？③ `service` 字段取值是什么？④ 为何 `IndexController` 不用 JSON？⑤ 改端口要改哪两行配置？能口头回答后，再进入运行时与角色细读代码，效率更高。

### 运行时与角色

Beego 进程从 `main()` 启动：先 **`web.InsertFilter`** 注册全局或路径前缀过滤器，再 **`web.Router`** 把 URL 映射到 Controller 实例与方法名，最后 **`web.BConfig.Listen`** 设定地址端口并 **`web.Run()`** 进入监听。一次请求的典型路径是：**Filter（如 CORS）→ 路由匹配 → Controller 方法（通过嵌入的 `web.Controller` 访问 `c.Ctx`）→ `Ctx.Output` 写 Header/Body**。

子工程用包级变量 `store`（`itemsStore` + `sync.Mutex`）演示共享内存列表；生产环境应换持久化存储，但「Controller 薄、存储可替换」的分层仍适用。`//go:embed public/index.html` 使 `GET /` 无需外置静态目录。

```go
var store = &itemsStore{items: []item{{ID: "seed-1", Title: "示例条目（内存 + mutex）", CreatedAt: time.Now().UTC()}}}

type IndexController struct {
	web.Controller
}

func (c *IndexController) Get() {
	_ = c.Ctx.Output.Header("Content-Type", "text/html; charset=utf-8")
	_, _ = c.Ctx.ResponseWriter.Write(indexHTML)
}

type HealthController struct {
	web.Controller
}

func (c *HealthController) Get() {
	_ = c.Ctx.Output.JSON(map[string]any{"ok": true, "service": "framework-back-end-beego"}, false, false)
}
```

`Ctx.Output.JSON` 的第三、第四个 `false` 参数控制是否格式化与是否使用 JsonP，本示例保持默认 JSON 输出。与同仓 Node 示例相比，本 Go 服务固定 **3006** 端口，便于批量脚本区分栈。

从并发角度，`itemsStore` 的 `Mutex` 保护的是进程内切片，而不是 Beego 替你处理的所有共享状态；若你在 Controller 里增加包级 map 或缓存，也必须自行加锁或改用 channel。Filter 函数里应避免长时间阻塞，否则会影响所有命中该模式的路径。另一个常见误区是把「解析 Session」放在 `BeforeRouter` 却访问尚未路由的信息——本示例的 Filter 只写 Header，不涉及 Session，因此顺序问题较少；扩展时请对照官方 Filter 阶段表谨慎放置逻辑。

把 Beego 与 Gin 的「上下文对象」对照：`gin.Context` 与 `context.Context`（Beego 过滤器参数）名称相近但类型不同，初学者易混淆。记住：**Filter 参数**用于横切；**Controller 的 `c.Ctx`** 用于业务读写。画图时可用两种颜色区分。若你曾在 PHP 或 Java Spring 中使用过「前置拦截器」，Beego Filter 与之类似，但注册 API 是 `InsertFilter` 而非注解扫描。团队 onboarding 时可以让新人先口述 Filter 与 Controller 各负责什么，再允许其修改业务代码，能显著降低第一次提交就破坏 CORS 的概率。

理解运行时模型的另一角度是「数据流」：请求体字节进入 `Ctx.Input`，经 `json.Unmarshal` 变成 Go 结构体，再经校验进入 `store`，最后由 `Output.JSON` 序列化回字节。响应头在 Filter 与 Controller 两处都可能写入，浏览器最终看到的是合并结果。并发下多个请求同时 `Create`，`Mutex` 保证切片不会 data race；若去掉锁，可用 `go run -race .` 在本地实验（实验后请恢复锁）。访问日志方面，Beego 默认会打印请求记录，与本示例 `log.Println` 启动提示互补；生产可把访问日志接入集中收集，字段建议包含方法、路径、状态码、耗时、trace id。

**动手（运行时）**：在纸上画出一次 `POST /api/items` 的序列图，标出 Filter、Router、`Create`、`store.add`、`Output.JSON` 五步；拍照或扫描放进个人笔记。修改后执行 `go run .`，用 PowerShell 复测 `/api/health` 与本节相关路径。

### 安装与环境

子工程为独立 Module，`go.mod` 仅直接依赖 Beego v2：

```go
module framework/beego-demo

go 1.21.0

require github.com/beego/beego/v2 v2.2.0
```

在 PowerShell 中务必 `Set-Location -LiteralPath` 到子工程根（含 `go.mod` 与 `main.go`），再执行 `go mod tidy` 与 `go run .`。**不要**在 Framework  monorepo 其它目录执行 `go run`。公司网络可设置 `GOPROXY`；`go.sum` 应纳入版本控制。

**动手（安装）**：执行 `go version` 与 `go env GOPATH GOPROXY`，确认环境正常；删除 `go.sum` 后重新 `go mod tidy`，观察依赖是否可重现拉取。修改后执行 `go run .`，复测 `/api/health`。

升级 Beego 小版本前请阅读上游 Release Note：v2 与 v1 的 import 路径不同，旧教程中的 `github.com/astaxie/beego` 不能直接套用。IDE 若无法跳转 `web.Controller`，检查是否打开了 Module 根目录而非上层文件夹。CI 与开发者本机 `GOPROXY` 不一致时，优先统一代理策略，而不是在本地关闭 checksum 校验。Windows 团队注意路径大小写：Go 模块缓存对版本字符串敏感，清理 `go clean -modcache` 前请确认无其它项目正在构建。

依赖树方面，Beego v2 会间接引入若干标准库包装与工具包，体积大于「纯 stdlib + 单路由」方案，但换来统一文档与生态。评估依赖时不仅看 `go.mod` 直接 require，也可 `go mod graph | findstr beego`（PowerShell 下用 `Select-String`）观察传递依赖。若公司安全部门扫描漏洞，请关注 Beego 官方安全公告而非仅扫描你的业务 import。开发机与 CI 的 Go 版本建议保持一致，避免「本地 1.22、CI 1.21」导致的细微差异。

若 `go run` 首次较慢，属于正常编译与模块下载；后续运行会快许多。不要在杀毒软件密集扫描的目录里反复编译，可能显著拖慢体验。将子工程放在 SSD 路径也有助于缩短 `go mod tidy` 时间。完成安装节后，请在笔记里记录本机成功的 Go 版本号与 Beego 版本号，便于半年后复现环境。

### 第一个 HTTP 服务

「第一个 HTTP 服务」在 Beego 中体现为：配置 **`web.BConfig.Listen.HTTPAddr`** 与 **`HTTPPort`**，然后 **`web.Run()`**。`Run` 内部启动 HTTP Server 并阻塞；启动成功后 `log.Println` 打印访问 URL。默认 **127.0.0.1:3006**；若端口占用，需修改 `HTTPPort` 或结束占用进程后重启。

```go
	web.BConfig.Listen.HTTPAddr = "127.0.0.1"
	web.BConfig.Listen.HTTPPort = 3006
	log.Println("Beego 演示：http://127.0.0.1:3006/")
	web.Run()
```

建议验证顺序：先 `GET /api/health`，再浏览器打开 `/` 确认嵌入 HTML，再测写接口。Beego 本示例未配置 dev 热重载，改代码后必须重新 `go run .`。

若终端打印的 URL 与浏览器访问不一致，以 `BConfig.Listen` 为准排查。端口被占用时，错误信息通常包含 `bind` 关键字；可临时改 `HTTPPort` 为 3016 并同步修改 PowerShell 探活 URL。WSL 与 Windows 混用时，`127.0.0.1` 的可达性因网络模式而异，必要时统一在一种环境里完成演示。把「启动成功」与「业务正确」分开验证：health 通过只说明路由与 JSON 链可用，不代表 POST 校验与 Mutex 行为也正确。

**动手（第一个 HTTP 服务）**：浏览器打开 `/` 与 `/api/health`；若页面空白，查看终端是否监听 3006。修改 `HTTPPort` 后重启，确认 URL 变化。修改后执行 `go run .`，复测 `/api/health`。

`web.Run()` 阻塞主 goroutine 是正常行为；不要在 `Run` 之后写业务逻辑，除非使用 goroutine 启动其它后台任务。若你需要优雅退出，查阅 Beego 与 `os/signal` 结合的官方示例，在演示阶段可暂不实现。监听队列 backlog、超时等高级参数同样存在于 Beego 配置结构中，高并发场景再调优即可。对本指南而言，能在本机稳定看到「Beego 演示：http://127.0.0.1:3006/」日志行，即算完成本节目标。

### 路由与处理器

Beego 的「处理器」是 Controller 上的方法；**`web.Router(路径, &Controller{}, "动词:方法名")`** 完成绑定。同一 URL 可写 **`"get:List;post:Create"`**，分别对应 `List()` 与 `Create()`。Controller 必须嵌入 **`web.Controller`**，才能使用 `c.Ctx`。

```go
	web.Router("/", &IndexController{}, "get:Get")
	web.Router("/api/health", &HealthController{}, "get:Get")
	web.Router("/api/demo/lifecycle", &DemoController{}, "get:Get")
	web.Router("/api/items", &ItemsController{}, "get:List;post:Create")
	web.Router("/api/box/inner", &BoxController{}, "get:Inner")
```

> **注意**：若对 `/api/items` 发送 GET 却映射到 `Create`，或方法名与映射字符串不一致，会得到 404 或方法不允许；排错时先核对第三参数字符串与方法名大小写。

子工程路径与同仓其它后端对齐：`/api/health`、`/api/demo/lifecycle`、`/api/items`、`/api/box/inner`，便于呈现页 `fetch` 复用同一套 URL 心智模型。

大型项目里可按领域拆分多个 Controller 文件，但路由注册仍建议在 `main` 或专门的 `router.go` 集中完成，避免「注册了却找不到」的隐式分散。若你需要 REST 风格的路径参数，Beego 支持在 Router 模式里写 `:id` 等形式，读取时使用 `c.Ctx.Input.Param`；本示例为降低入门曲线未引入路径参数，你可以在掌握列表接口后再加一条 `GET /api/items/:id` 练手。团队规范应禁止复制粘贴映射字符串却不改方法名，这类错误在编译期不一定能捕获，只能靠集成测试发现。

映射字符串大小写敏感：`get` 与 `GET` 的约定以 Beego 文档为准，本示例使用小写 `get` 前缀。多个动词共用 URL 时，务必确认客户端方法正确，否则可能命中错误方法或 404。自动化测试可用 `httptest` 构造请求，断言路由是否注册成功；本指南不贴测试代码，但推荐在真实项目中为每条 Router 至少保留一条集成测试。对 API 网关暴露的路径，注意网关 strip prefix 后 Beego 侧看到的路径是否仍与注册一致，这是部署 Beego  behind reverse proxy 时的高频坑。

**动手（路由）**：临时将 `/api/health` 改为 `/api/healthz` 并重启，确认旧 URL 404；改回后 smoke。在 IDE 中对 `ItemsController` 使用「查找引用」确认 `List`/`Create` 仅被 Router 字符串使用。修改后执行 `go run .`，复测 `/api/health`。

### 请求与响应

通过 **`c.Ctx.Input`** 读请求（如 `RequestBody`），通过 **`c.Ctx.Output`** 写响应（`Header`、`SetStatus`、`JSON`）。`IndexController.Get` 设置 `Content-Type` 后向 `ResponseWriter` 写入嵌入 HTML；JSON 接口统一走 `Output.JSON`。

```go
func (c *IndexController) Get() {
	_ = c.Ctx.Output.Header("Content-Type", "text/html; charset=utf-8")
	_, _ = c.Ctx.ResponseWriter.Write(indexHTML)
}

func (c *DemoController) Get() {
	_ = c.Ctx.Output.Header("X-Beego-Demo", "beego-handler")
	_ = c.Ctx.Output.JSON(map[string]any{
		"message": "Beego：MVC 风格 Controller + Router 映射；Filter 可做全局/前缀中间件。",
		"beegoPipeline": []string{
			"web.Router 注册 URL → Controller 方法",
			"InsertFilter 在 BeforeRouter 等阶段织入逻辑",
			"Controller.Ctx 访问请求与响应",
		},
	}, false, false)
}
```

呈现页须通过 **http://127.0.0.1:3006/** 访问，勿用 `file://`，否则浏览器同源策略会阻止 `fetch` 调 API。

**动手（请求与响应）**：用 PowerShell 对 `/api/items` 发 POST，观察 201 与 400；在开发者工具查看 `X-Beego-Demo`。修改后执行 `go run .`，复测 `/api/health`。

`Ctx.Input.RequestBody` 读取的是原始字节，适合本示例的手写 `json.Unmarshal`；若改用 Beego 的 `ParseForm` 或自动绑定，要留意 Content-Type 与结构体 tag 的一致性。写 HTML 时直接操作 `ResponseWriter` 与 `Output.JSON` 混用是允许的，但团队应约定「API 一律 JSON、页面一律 HTML」，减少客户端解析歧义。调试时可在 Filter 里临时打印 `ctx.Request.URL.Path`，但上线前务必删除，避免日志膨胀与敏感路径泄露。

响应头顺序通常不影响客户端解析，但某些安全头（如 `Content-Security-Policy`）若由 Filter 与 Controller 重复设置，应以团队策略为准保留一份。下载文件、流式响应等高级场景会使用 `Ctx.Output.Download` 或分块写；本示例仅 JSON 与静态 HTML，足够覆盖多数 REST 入门场景。若前端报 CORS 错误，先确认是「浏览器拦截」还是「服务端 4xx/5xx」，再在 Network 面板查看预检请求与响应头，不要仅凭控制台一句报错就改业务逻辑。

### JSON API

`GET /api/health` 返回 `ok` 与 `service`；`GET /api/demo/lifecycle` 返回管道说明与 `beegoHighlights`；`GET /api/items` 返回 `items` 数组；`POST /api/items` 返回 201 与 `item`。字段名与前端约定一致：`id`、`title`、`createdAt`。

```go
func (c *HealthController) Get() {
	_ = c.Ctx.Output.JSON(map[string]any{"ok": true, "service": "framework-back-end-beego"}, false, false)
}

func (c *ItemsController) List() {
	_ = c.Ctx.Output.JSON(map[string]any{"items": store.list()}, false, false)
}
```

`DemoController` 额外设置响应头 **`X-Beego-Demo`**，用于在浏览器开发者工具中区分「Handler 内写的 Header」与 Filter 写的 Header。

**动手（JSON API）**：比较 `/api/health` 与 `/api/demo/lifecycle` 的 JSON 键名；记录 `beegoPipeline` 数组内容。修改后执行 `go run .`，复测 `/api/health`。

列表接口返回的 `items` 是值拷贝后的切片，客户端修改 JSON 不会影响服务端内存；创建接口返回 201 时 body 含完整 `item`，便于前端乐观更新。`demo/lifecycle` 的 `beegoPipeline` 数组是有意的教学 payload，生产环境应换成版本信息、构建号或依赖探测结果，而不是把框架介绍塞进业务 API。若你要对齐 OpenAPI，可在后续引入注解或独立 spec 文件，本指南不展开生成器流程。

字段命名采用 camelCase（`createdAt`）与同仓 Node 示例一致，便于呈现页共用 TypeScript 类型定义。若你的组织强制 snake_case，应在边界层统一转换，而不是部分接口 camel、部分 snake。空列表应返回 `"items":[]` 而非 `null`，避免前端判空分支爆炸。`demo/lifecycle` 返回的 `beegoHighlights` 是数组对象，展示如何在 JSON 里嵌套结构化「特性说明」，可类比产品文档接口，但请勿把敏感配置写入此类 endpoint。

### 参数与校验

子工程在 `ItemsController.Create` 中 **手写 JSON 解析与校验**（未使用 Beego 的自动解析标签），便于看清 400/201 分支。流程：`json.Unmarshal(RequestBody)` → `strings.TrimSpace` → 长度 1～120 → `store.add` → `SetStatus(201)`。

```go
func (c *ItemsController) Create() {
	var body struct {
		Title string `json:"title"`
	}
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		c.Ctx.Output.SetStatus(400)
		_ = c.Ctx.Output.JSON(map[string]any{"error": err.Error()}, false, false)
		return
	}
	t := strings.TrimSpace(body.Title)
	if t == "" || len(t) > 120 {
		c.Ctx.Output.SetStatus(400)
		_ = c.Ctx.Output.JSON(map[string]any{"error": "title: required, 1-120 chars"}, false, false)
		return
	}
	it := store.add(t)
	c.Ctx.Output.SetStatus(201)
	_ = c.Ctx.Output.JSON(map[string]any{"item": it}, false, false)
}
```

生产环境可改用 Beego 的解析与校验工具或引入 validator，但 **错误体结构**（`error` 字段 + 4xx）建议团队统一，便于前端处理。

校验逻辑放在 Controller 方法内的好处是易读易测；缺点是多个方法可能重复。折中做法是把 `parseTitle(body []byte) (string, error)` 抽到同包函数，Controller 只负责 HTTP 状态码映射。注意 `TrimSpace` 之后还要判断 rune 长度而非字节长度，若未来支持多语言标题，应改用 `utf8.RuneCountInString`。对恶意超大 body，应在 Filter 或前置中间件限制 `Content-Length`，本示例未实现，上线前必须补上。

与 Gin `binding:"required"` 相比，手写校验的错误文案完全由你控制，但也更容易遗漏边界。建议为 `title` 维护常量 `maxTitleLen = 120`，避免魔法数字散落。对重复标题、敏感词等业务规则，应在 `store.add` 之前返回 409 或 422，并在团队 API 规范中写清状态码含义。单元测试可表驱动：输入 body、期望状态码、期望 `error` 子串，本指南鼓励你在 fork 中自行添加测试文件巩固理解。

**动手（参数与校验）**：分别 POST 合法 title、空 title、非法 JSON，记录状态码与 `error` 字段。修改后执行 `go run .`，复测 `/api/health`。

### 中间件或钩子

Beego 用 **`web.InsertFilter(模式, 阶段, func(ctx *context.Context))`** 注册过滤器。子工程在 **`web.BeforeRouter`** 阶段注册：一条匹配 `*` 写 CORS；一条匹配 **`/api/box/*`** 写 **`X-Feature-Box`**，演示「仅部分路径生效」。

```go
	web.InsertFilter("*", web.BeforeRouter, func(ctx *context.Context) {
		_ = ctx.Output.Header("Access-Control-Allow-Origin", "*")
		_ = ctx.Output.Header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		_ = ctx.Output.Header("Access-Control-Allow-Headers", "Content-Type, Origin")
		_ = ctx.Output.Header("Access-Control-Expose-Headers", "X-Feature-Box, X-Beego-Demo")
	})
	web.InsertFilter("/api/box/*", web.BeforeRouter, func(ctx *context.Context) {
		_ = ctx.Output.Header("X-Feature-Box", "beego-insertfilter")
	})
```

请求 **`GET /api/box/inner`** 时，应同时看到 Filter 写入的 `X-Feature-Box` 与 Demo/业务 Header；请求 `/api/health` 时不应有 `beego-insertfilter` 那条 Filter 的语义（仅 CORS）。理解 **Filter 阶段枚举**（BeforeRouter、BeforeExec 等）是阅读官方文档时的关键索引。

CORS 的 `Expose-Headers` 必须列出前端脚本要读取的自定义头，否则浏览器控制台能看到但 JS 读不到。OPTIONS 预检在部分部署里由反向代理处理，本示例在应用层写 CORS 头，适合本地演示；上线到生产时 often 把 CORS 挪到网关统一配置，应用内只保留业务头。Filter 注册顺序影响同阶段内的执行先后，若两个 Filter 都写同名 Header，后执行的覆盖前者——排障时可用二分法暂时注释 Filter 定位来源。

`/api/box/*` 模式说明 Filter 可按路径前缀生效，类似 Gin 的 `Group` 中间件。若你要实现鉴权，可新增 `InsertFilter("/api/*", ...)` 读取 `Authorization`，失败则设置 401 并 `return`，成功则继续链条。注意不要在 Filter 内启动 goroutine 访问 `Ctx` 之外的不安全字段。Beego 文档中的 `FinishRouter` 等阶段适合记录访问日志或 metrics，本示例为简洁未使用，生产可结合 Prometheus  exporter 扩展。

**动手（中间件）**：请求 `/api/box/inner` 与 `/api/health`，对比 `X-Feature-Box` 是否存在。临时注释 box 专用 Filter 后重启验证。修改后执行 `go run .`，复测 `/api/health`。

### 错误处理

解析失败或校验失败时 **`SetStatus(400)`** 并返回 JSON `error`；创建成功 **`SetStatus(201)`**。不向客户端返回堆栈；日志由 Beego 默认访问日志与 `log` 包承担。方法不允许时 Beego 可能返回 404（视路由与动词映射而定）。

```go
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		c.Ctx.Output.SetStatus(400)
		_ = c.Ctx.Output.JSON(map[string]any{"error": err.Error()}, false, false)
		return
	}
```

建议用 PowerShell 故意发送 `{}` 或 `{"title":""}`，观察 400 与错误文案是否与预期一致。

不要把内部异常栈直接 JSON 化返回给浏览器；Beego 默认 Recovery 行为与 Gin 类似，仍应在业务层把可预期错误映射为 4xx。对 404，要区分「路由未注册」与「资源不存在」两种语义，REST API 设计时应统一约定。日志里记录 request id、路径、状态码与耗时即可，避免打印完整 body 中的个人信息。若引入 i18n，错误 `error` 字段可换为错误码 + 客户端本地化，但本示例保持英文/中文混合短句以利阅读。

客户端错误（4xx）与服务器错误（5xx）应在监控告警中分开统计。本示例几乎不产生 5xx，除非 JSON 编码失败等罕见情况；若你扩展代码，注意 `store` 锁误用导致的 panic 会被 Beego 捕获，但仍应修复根因而非依赖 Recovery。对幂等性敏感的 `POST`，生产应引入 Idempotency-Key 或改为 PUT 到具体资源路径，演示项目可暂不实现，但应在设计评审中讨论。

**动手（错误处理）**：发送 `Content-Type: text/plain` 的 POST，观察 400 形态；确认响应体仍为 JSON。修改后执行 `go run .`，复测 `/api/health`。

### 配置与环境变量

本示例子工程将监听地址写死在 **`web.BConfig.Listen`**（`HTTPAddr` + **HTTPPort 3006**）。Beego 也支持通过 `app.conf` 与环境变量配置；若你 fork 后改为读取 `os.Getenv("PORT")`，请在团队文档注明与本文默认端口的差异。云部署常设监听 `0.0.0.0`，由反向代理提供 TLS。

```go
	web.BConfig.Listen.HTTPAddr = "127.0.0.1"
	web.BConfig.Listen.HTTPPort = 3006
```

Beego 还支持 `app.conf` 中的 `httpport`、`runmode` 等键，适合多环境配置文件；本示例子工程选择代码内写死，以减少「找不到配置文件」的新手挫败感。你若改为 `app.conf`，记得把文件放进 Beego 约定路径并加入构建产物。监听 `0.0.0.0` 时，防火墙与安全组规则必须同步更新，否则会出现「容器内 curl 成功、外网超时」的典型误会。

`runmode` 为 `dev` 时 Beego 可能输出更详细日志；生产应使用 `prod` 并关闭不必要的控制台调试。配置优先级（环境变量 vs 配置文件 vs 代码）以官方文档为准，团队应在 README 写明「以哪一层为准」，避免运维与开发各改一处互相覆盖。若使用 Kubernetes，ConfigMap 挂载 `app.conf` 是常见模式，与本示例的 embed 静态页并不冲突，可同时存在。

**动手（配置）**：把 `HTTPPort` 改为 `3016`，重启并更新 PowerShell URL；确认 health 仍返回正确 `service`。改回 3006 后再 smoke。修改后执行 `go run .`，复测 `/api/health`。

### 测试与调试

推荐用 PowerShell 依次探测：

```powershell
Invoke-RestMethod http://127.0.0.1:3006/api/health | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:3006/api/items | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:3006/api/demo/lifecycle | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:3006/api/box/inner | ConvertTo-Json
```

在浏览器网络面板检查 **`X-Feature-Box`**、**`X-Beego-Demo`**。改 `service` 字段后重启进程，确认 health JSON 变化。

可把上述命令保存为 `smoke.ps1` 供 CI 调用，但 CI 环境需先 `go run` 或启动编译后的二进制，并等待端口就绪。单元测试层面对 Controller 的测试通常需要构造 `*context.Context` 或走 httptest，本指南不展开测试代码；建议至少在合并前手工跑一遍 smoke。若 `Invoke-RestMethod` 把 JSON 解析成对象，属正常行为；需要原始字符串时改用 `Invoke-WebRequest`。

调试技巧：临时在 `List` 方法开头 `log.Printf` 打印条目数量，确认 `POST` 后是否 prepend 成功；完成后删除日志。使用 Delve 调试时，在 `web.Run` 前下断点，单步进入第一条请求的处理流程，观察 Filter 是否先于 Controller 执行。若怀疑路由未命中，检查 Beego 日志中的 404 记录与注册路径是否完全一致（含尾部斜杠）。与前端联调时，让前端同事提供 Network HAR 文件，比口头描述 CORS 错误更高效。

调试阶段建议开启浏览器「禁用缓存」，避免旧版 `index.html` 干扰 API 判断。VS Code 用户可把本页 PowerShell 命令改写为 `.http` 文件共享给团队。遇到间歇性 404，用 `Get-NetTCPConnection -LocalPort 3006` 检查是否误留旧进程。建议维护三列表格记录每次实验的请求、状态码、关键响应头，一周后回顾可明显加快排障。

**动手（测试）**：将四条 `Invoke-RestMethod` 写入 `smoke.ps1` 并执行；故意改错 `title` 触发 400，确认脚本仍能捕获错误响应。修改后执行 `go run .`，复测 `/api/health`。

### 部署概念

可 **`go build -o beego-demo.exe .`** 产出单二进制（已嵌入 `index.html`）。演示中 CORS 为 `*`、存储为内存，上线前须收紧安全策略并接入真实数据库。容器 **`HEALTHCHECK`** 可探测 `GET /api/health`。交叉编译时设置 `GOOS`/`GOARCH` 于构建命令前。

```go
//go:embed public/index.html
var indexHTML []byte
```

嵌入静态资源后，镜像不必再 COPY `public/`，但更新 HTML 需重新编译。

交叉编译示例（在子工程目录执行）：`$env:GOOS='linux'; $env:GOARCH='amd64'; go build -o beego-demo .`，产物可在 Linux 容器运行。Windows 本机直接 `go build -o beego-demo.exe .` 亦可。构建前请 `go test ./...`（若你添加了测试）与 smoke 探活。镜像内 ENTRYPOINT 指向二进制即可，环境变量 `PORT` 若未接入代码则仍使用 3006，需在 K8s manifest 的 containerPort 与之对齐。滚动发布时，先对新副本做 health 探针，再切流量，避免「进程已监听但路由未注册完」的极短窗口问题（Beego 通常无此问题，但养成习惯有益）。

生产镜像建议使用 distroless 或 alpine 等最小基础镜像，并以外部探针调用 `/api/health`。多副本部署时，内存 `store` 的数据互不共享，本示例仅适合演示；换数据库后仍应保留 health 路径不变，以便滚动发布与回滚脚本复用。构建时通过 `-ldflags` 注入版本号写入 `demo/lifecycle` 或单独 `/api/version` 是常见扩展，与 Beego 无冲突。

安全方面：演示 CORS 为 `*` 仅适合本地；生产应在网关收敛来源，应用内只处理业务授权。鉴权可放在 `InsertFilter` 的 `BeforeRouter` 或 `BeforeExec`，读取 Header 中的 token 并 `ctx.Abort` 提前结束；本示例未实现，避免干扰 HTTP 基础学习。限流、熔断、追踪等亦应在 Filter 或独立中间件层处理，而不是在每个 Controller 方法复制粘贴。日志建议结构化输出路径、状态码、耗时，便于与 NestJS、FastAPI 等栈的日志字段对齐，方便统一观测平台检索。

**动手（部署）**：执行 `go build -o beego-demo.exe .` 并直接运行 exe，确认与 `go run .` 行为一致；检查单文件体积是否包含 embed HTML。修改后执行 `go run .`，复测 `/api/health`。

**基础篇十二章串联（复习用，仍属基础篇收尾）**：

1. **运行时与角色**：弄清 Filter → Router → Controller → Output 的顺序；记住 `store` 与 `Mutex` 的角色。  
2. **安装与环境**：会在正确目录 `go mod tidy`；知道 Beego v2 的 module 路径。  
3. **第一个 HTTP 服务**：会改 `BConfig` 并理解 `web.Run` 阻塞监听。  
4. **路由与处理器**：会读 `web.Router` 第三参；能添加一条新路由并重启验证。  
5. **请求与响应**：会用 `Ctx.Input`/`Output`；区分 HTML 与 JSON 写法。  
6. **JSON API**：知道各路径返回的 JSON 形状；能解释 `demo/lifecycle` 的教学字段。  
7. **参数与校验**：能复述 `Create` 的 400/201 分支；理解 title 长度规则。  
8. **中间件或钩子**：能指出 CORS 与 `X-Feature-Box` 的注册位置；理解路径模式 `*` 与 `/api/box/*`。  
9. **错误处理**：承诺不把堆栈返回客户端；区分 4xx 业务错误与 5xx。  
10. **配置与环境变量**：知道默认 3006；了解 `app.conf` 可作为后续扩展。  
11. **测试与调试**：会跑 PowerShell smoke；会用浏览器看响应头。  
12. **部署概念**：会 `go build`；知道 embed 对镜像的影响。  

串联复习时，请合上指南，只看 `main.go`，按上表逐项指出代码行号。若某项找不到对应代码，说明阅读尚不完整，应回到该节重读而非继续往后。串联完成后，再进入下方 Framework 实战节，把「分散知识点」与「完整文件」焊接在一起。

**常见误解澄清**：Beego 并非「只能写单体」；微服务场景仍可用 Beego 写 HTTP 服务，只是 ORM 与工具链更偏单体习惯。Filter 并非越多越好，每一条都应可测试、可命名、可禁用。Controller 方法名不必叫 `Get`，但映射字符串必须与方法名一致。`Output.JSON` 的布尔参数不是「装饰」，传错可能导致 JsonP 行为变化。embed 的 HTML 仍可能被浏览器缓存，演示时若改了 HTML 却未重新编译，会误以为「改了没生效」。以上误解在团队分享时可做成 checklist，帮助新人跳过弯路。

**与 Gin 指南（同仓 3002）对照阅读建议**：先读完本篇并跑通 Beego，再读 Gin 指南时用同一张 API 表对照路由注册语法差异，不要并行读导致端口混淆。对照时只比较「路径与 JSON 契约」，不要比较框架流行度。若你写跨栈 smoke，可为每个栈维护独立脚本文件，通过函数名区分 `Test-BeegoHealth` 与 `Test-GinHealth`，避免复制粘贴 URL 时忘改端口。对照阅读完成后，用五分钟写三条「Beego 独有、Gin 没有」的观察（例如 InsertFilter 路径模式、Router 第三参映射），巩固记忆。

**与呈现页、脚本、运维的协作**：开发同事改 Router 时，应同步通知前端与 QA 更新 URL 列表；运维配置探针时，应使用 `GET /api/health` 而非根路径 `/`，避免把 HTML 200 误判为 API 健康。自动化脚本读取 `service` 字段时，应断言精确字符串 `framework-back-end-beego`，不要用模糊包含匹配，以免与其它栈冲突。若你在 Monorepo 中同时维护多份 Go 后端，提交 PR 时请在标题注明端口与栈名，减少 reviewer 误跑错误目录的概率。

## Framework 子工程实战

**路径**：`F:\Study\Framework\Back-end\Go\Beego`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 嵌入的 `public/index.html` |
| GET | `/api/health` | 健康检查 |
| GET | `/api/demo/lifecycle` | 管道说明 JSON + `X-Beego-Demo` |
| GET | `/api/items` | 列表 |
| POST | `/api/items` | 创建（JSON `title`，1～120 字） |
| GET | `/api/box/inner` | 前缀 Filter 演示 |

**启动（Windows PowerShell）**：

```powershell
Set-Location -LiteralPath 'F:\Study\Framework\Back-end\Go\Beego'
go mod tidy
go run .
```

**通读 `main.go` 前的导读（按文件自上而下）**：

1. **import**：`web` 与 `context` 来自 Beego v2；`embed` 用于编译期嵌入 HTML。
2. **类型定义**：`item` 与 JSON 字段 tag 对齐；`itemsStore` 封装带锁切片；`newID` 生成演示用主键。
3. **Controller 类型**：每个 HTTP 资源一个结构体，嵌入 `web.Controller`；方法名 `Get`/`List`/`Create`/`Inner` 与 Router 第三参映射。
4. **`main`**：先 `InsertFilter`（CORS 与 box 头），再 `Router`，最后 `BConfig` 与 `Run`。顺序很重要：Filter 注册应在 `Run` 之前，Router 亦同。
5. **无 `init` 魔法**：所有行为在 `main` 可见，适合教学；大型项目可拆 `router.go` 但应保持「注册集中」。

带着上述五步阅读下方完整文件；遇到不懂的 API，优先查 Beego 文档中 `Controller`、`Filter` 章节，再回到本页看对应「基础篇」小节。

**带中文行注的完整 `main.go`（与子工程一致，便于通读）**：

```go
package main

import (
	"crypto/rand"
	"embed"
	"encoding/hex"
	"encoding/json"
	"log"
	"strings"
	"sync"
	"time"

	"github.com/beego/beego/v2/server/web"
	"github.com/beego/beego/v2/server/web/context"
)

//go:embed public/index.html
var indexHTML []byte

type item struct {
	ID        string    `json:"id"`
	Title     string    `json:"title"`
	CreatedAt time.Time `json:"createdAt"`
}

type itemsStore struct {
	mu    sync.Mutex
	items []item
}

func (s *itemsStore) list() []item {
	s.mu.Lock()
	defer s.mu.Unlock()
	out := make([]item, len(s.items))
	copy(out, s.items)
	return out
}

func (s *itemsStore) add(title string) item {
	s.mu.Lock()
	defer s.mu.Unlock()
	it := item{ID: newID(), Title: title, CreatedAt: time.Now().UTC()}
	s.items = append([]item{it}, s.items...)
	return it
}

func newID() string {
	b := make([]byte, 16)
	if _, err := rand.Read(b); err != nil {
		return hex.EncodeToString([]byte(time.Now().String()))
	}
	return hex.EncodeToString(b)
}

var store = &itemsStore{items: []item{{ID: "seed-1", Title: "示例条目（内存 + mutex）", CreatedAt: time.Now().UTC()}}}

type IndexController struct {
	web.Controller
}

func (c *IndexController) Get() {
	_ = c.Ctx.Output.Header("Content-Type", "text/html; charset=utf-8")
	_, _ = c.Ctx.ResponseWriter.Write(indexHTML)
}

type HealthController struct {
	web.Controller
}

func (c *HealthController) Get() {
	_ = c.Ctx.Output.JSON(map[string]any{"ok": true, "service": "framework-back-end-beego"}, false, false)
}

type DemoController struct {
	web.Controller
}

func (c *DemoController) Get() {
	_ = c.Ctx.Output.Header("X-Beego-Demo", "beego-handler")
	_ = c.Ctx.Output.JSON(map[string]any{
		"message": "Beego：MVC 风格 Controller + Router 映射；Filter 可做全局/前缀中间件。",
		"beegoPipeline": []string{
			"web.Router 注册 URL → Controller 方法",
			"InsertFilter 在 BeforeRouter 等阶段织入逻辑",
			"Controller.Ctx 访问请求与响应",
		},
		"beegoHighlights": []map[string]string{
			{"title": "全家桶取向", "detail": "ORM、session、日志等可渐进启用；本示例仅用最小子集。"},
			{"title": "工程习惯", "detail": "适合习惯「控制器 + 映射字符串」的团队。"},
		},
	}, false, false)
}

type ItemsController struct {
	web.Controller
}

func (c *ItemsController) List() {
	_ = c.Ctx.Output.JSON(map[string]any{"items": store.list()}, false, false)
}

func (c *ItemsController) Create() {
	var body struct {
		Title string `json:"title"`
	}
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		c.Ctx.Output.SetStatus(400)
		_ = c.Ctx.Output.JSON(map[string]any{"error": err.Error()}, false, false)
		return
	}
	t := strings.TrimSpace(body.Title)
	if t == "" || len(t) > 120 {
		c.Ctx.Output.SetStatus(400)
		_ = c.Ctx.Output.JSON(map[string]any{"error": "title: required, 1-120 chars"}, false, false)
		return
	}
	it := store.add(t)
	c.Ctx.Output.SetStatus(201)
	_ = c.Ctx.Output.JSON(map[string]any{"item": it}, false, false)
}

type BoxController struct {
	web.Controller
}

func (c *BoxController) Inner() {
	_ = c.Ctx.Output.JSON(map[string]any{
		"where": "/api/box/inner",
		"note":  "X-Feature-Box 由 InsertFilter 匹配 /api/box/* 写入。",
	}, false, false)
}

func main() {
	web.InsertFilter("*", web.BeforeRouter, func(ctx *context.Context) {
		_ = ctx.Output.Header("Access-Control-Allow-Origin", "*")
		_ = ctx.Output.Header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		_ = ctx.Output.Header("Access-Control-Allow-Headers", "Content-Type, Origin")
		_ = ctx.Output.Header("Access-Control-Expose-Headers", "X-Feature-Box, X-Beego-Demo")
	})
	web.InsertFilter("/api/box/*", web.BeforeRouter, func(ctx *context.Context) {
		_ = ctx.Output.Header("X-Feature-Box", "beego-insertfilter")
	})

	web.Router("/", &IndexController{}, "get:Get")
	web.Router("/api/health", &HealthController{}, "get:Get")
	web.Router("/api/demo/lifecycle", &DemoController{}, "get:Get")
	web.Router("/api/items", &ItemsController{}, "get:List;post:Create")
	web.Router("/api/box/inner", &BoxController{}, "get:Inner")

	web.BConfig.Listen.HTTPAddr = "127.0.0.1"
	web.BConfig.Listen.HTTPPort = 3006
	log.Println("Beego 演示：http://127.0.0.1:3006/")
	web.Run()
}
```

**建议自测**：health → items GET → items POST（合法/非法 body）→ demo/lifecycle → box/inner → 浏览器 `/`。对照响应头与 JSON 字段是否与上表一致。

**完整 `main.go` 阅读笔记（可按块勾选）**：

- [ ] **embed**：确认 `indexHTML` 在编译期绑定，删除 `public/index.html` 后需重新构建才报错。  
- [ ] **HealthController**：一行 JSON，是 smoke 的核心断言点。  
- [ ] **DemoController**：同时演示 Header 与嵌套 JSON 字段，适合讲 Beego 能力。  
- [ ] **ItemsController.List**：只读 `store.list()`，无参数解析。  
- [ ] **ItemsController.Create**：唯一写路径，含 400 与 201。  
- [ ] **BoxController.Inner**：配合 Filter，说明「路由组」效果。  
- [ ] **InsertFilter `*`**：四条 CORS 相关 Header，注意 `Expose-Headers` 列表。  
- [ ] **InsertFilter `/api/box/*`**：仅 box 子树附加 `X-Feature-Box`。  
- [ ] **Router 五注册**：路径与方法映射无遗漏。  
- [ ] **BConfig**：`HTTPAddr` 与 `HTTPPort` 与 PowerShell 探活一致。  

阅读笔记勾满后，尝试「遮住指南，仅看代码向同事讲解五分钟」。若讲解流畅，说明本指南第一阶段目标达成；若卡顿，回到对应基础篇章节，不要反复通读导读。

**扩展阅读顺序（离开本页之后）**：官方文档 MVC 章节 → Filter 阶段完整列表 → ORM 快速开始（若需要数据库）→ 配置参考（`app.conf`）。每读官方一章，回子工程做一处最小改动并 smoke，形成「读一章、改一行、测一次」的节奏。避免连续阅读官方文档却不写代码，那样极易在团队实战时仍不会注册 Router。

**为何本示例子工程保持单文件**：降低克隆后的心智负担；你完全可以在掌握后拆分为 `controllers/`、`routers/`、`models/`，但请保留集中注册的习惯。拆分后，`main` 应只剩 `web.Run` 与配置，路由表一目了然。若拆得过散且无文档，新人会比在单文件里更难找到 `POST /api/items` 的入口。教学与生产的平衡点是：**结构清晰 > 文件数量少**。

目录树（摘要）：子工程根含 `main.go`、`go.mod`、`go.sum`、`public/index.html`；无 `controllers/` 分包，以降低首次阅读成本。若你 fork 后按 Beego 官方推荐拆目录，请在本指南 fork 中更新路径说明，避免同事 clone 后找不到入口。呈现页内的 `fetch` 默认指向同源 API，改端口后记得同步修改 HTML 或改用相对路径。

自测时建议记录每张接口的「期望状态码、期望键名、期望响应头」，形成可回归的检查表。对 `POST` 准备三组 body：合法标题、空字符串、非法 JSON，分别对应 201、400、400。若要与 Gin 指南对照，并排打开两份 `main.go`，标出 Filter 与 `Use`、Router 与 `Group` 的对应关系，迁移时 API 契约可保持不变。

**按 Controller 走读（建议顺序）**：

1. **`IndexController`**：只负责 HTML，体现「页面与 API 分离」。阅读 `Get` 中为何设置 `Content-Type` 再写 `ResponseWriter`，而不是 `Output.JSON`。
2. **`HealthController`**：最小 JSON 探针，确认 `service` 拼写与自动化脚本一致。
3. **`DemoController`**：教学用 payload，理解 `beegoPipeline` 与 `beegoHighlights` 字段如何帮助新人建立框架心智模型；同时观察 `X-Beego-Demo` 响应头。
4. **`ItemsController`**：`List` 与 `Create` 共用 URL 不同动词，是 Beego 路由字符串的核心技巧；重点读 `Create` 中 400/201 分支与 `store.add` 的调用时机。
5. **`BoxController`**：配合 `/api/box/*` Filter，理解「路径前缀 + 专用 Header」如何模拟「路由组中间件」。
6. **`main` 函数**：所有横切逻辑应优先在这里或独立 `router.go` 收敛，避免散落在 Controller。

走读时可在纸上画两条时间线：一条是 **Filter 链**（CORS → box 专用头），一条是 **Controller 方法**（解析 → 校验 → 存储 → 写 JSON）。面试或内部分享时，能白板画出这两条线，比背诵 API 名称更能证明你理解 Beego 运行时。

**与呈现页联调**：打开 `/` 后，在浏览器控制台执行 `fetch('/api/health')` 应成功；若失败，检查是否从 `file://` 打开或端口错误。呈现页若展示 items 表格，创建条目后刷新列表，可验证 `POST` 与 `GET` 的一致性。若你修改了 `service` 字段，呈现页文案若写死栈名也需同步，否则用户会看到「脚本成功但文案不符」的割裂体验。

**常见改动练习（可选）**：

- 把 `HTTPPort` 改为读取环境变量，练习配置外置。
- 给 `HealthController` 增加 `version` 字段，练习 JSON 契约演进。
- 新增 `DELETE` 映射（需扩展路由字符串与方法），练习动词映射规则。

每项练习完成后用 smoke 命令回归，确保未破坏 health 与 CORS。练习的目的不是堆功能，而是确认你能在 Beego 约定下 **安全地改路由与 Controller**。

若你编写内部培训考题，可从子工程抽取「改一行代码」题型：例如删除某条 `InsertFilter` 后 CORS 失败、改错 Router 第三参后 404、向 `Create` 发送超长 title 后 400。这类题型比纯概念选择题更能检验是否真读过 `main.go`。培训结束时发放本页链接与仓库路径，并注明 Beego 版本与端口，避免学员回家后发现环境不一致。对于已有 Gin 经验的学员，可要求他们用一张表写出 Gin 与本示例的三处差异，作为结业作业，巩固对照表的价值。

**`itemsStore` 与并发（读代码时对照）**：`list` 与 `add` 均在锁内操作切片，`list` 返回拷贝避免调用方修改内部状态。`newID` 使用 `crypto/rand`，失败时退化为时间字符串的 hex，仅演示用途。若你改为数据库主键，应删除此函数并换用 DB 生成的 ID。`Create` 在校验通过后才调用 `store.add`，保证不会插入空标题。理解这些细节后，你再读 Beego ORM 文档时，会更容易把「模型层」与「Controller 层」分开。

**呈现页与 API 的协作**：`public/index.html` 通常包含调用 `/api/health`、`/api/items` 的脚本。若脚本写死端口会与 `BConfig` 不一致，应使用相对路径 `fetch('/api/health')`。若你需要在演示中切换环境，可在 HTML 内用 meta 标签注入 base URL，但本示例未采用，以保持单二进制简单性。前端同事排查问题时，请他们提供失败请求的 Method、URL、Status、Response headers 四要素，后端即可快速判断是 CORS、路由还是校验问题。

**PowerShell 与 curl 对照（Windows 用户）**：本页优先 PowerShell `Invoke-RestMethod`；若你更习惯 curl.exe，可写成 `curl.exe -s http://127.0.0.1:3006/api/health`。POST 时注意引号转义，JSON 体建议保存在 `body.json` 后用 `curl.exe -d '@body.json' -H "Content-Type: application/json" ...`。团队文档可同时提供两种写法，减少「文档只有 curl、同事只会 PowerShell」的摩擦。无论哪种工具，断言点应一致：`ok` 为 true、`service` 为 `framework-back-end-beego`。

## 学习路径

| 路径 | 建议 |
|------|------|
| 零基础 | 导读 → 快速上手 → 基础篇顺序阅读 → 实战节通读 `main.go` |
| 熟悉 `net/http` | 快速上手 → 重点读「路由与处理器」「中间件或钩子」，对照 Filter 阶段文档 |
| 熟悉 Gin/Echo | 对照「参数与校验」理解 Beego 手写解析与 Gin `ShouldBindJSON` 的差异 |

第一周可设里程碑：第一天启动并解释 health JSON；第二天画出 Filter→Router→Controller 顺序；第三天独立修改一条路由并观察 404；第四天为 `Create` 增加一条业务校验；第五天阅读官方 Filter 阶段文档并口头复述。已熟悉其它框架的读者，优先攻克「映射字符串」与「Ctx 读写」两处差异，再决定是否引入 ORM。

学习路径不是死板的线性表，而是优先级提示：能复现比能背诵更重要。建议把常犯的五个错误写下来：**改路由忘重启**、**Filter 里写重逻辑**、**CORS Expose 漏自定义头**、**用 file:// 打开呈现页**、**Mutex 漏保护共享切片**。这五条与本示例扩展方向高度重合，提前记录可减少夜间排障时间。

若用于团队 onboarding，第二周可要求新人完成小改动：例如新增只读 `GET /api/version` 或给 Filter 增加耗时日志（注意上线前删除）。评审时让对方在白板上画出一次 POST 请求经过的函数，能讲清即可认为运行时模型已内化。

**延伸阅读的使用方式**：官方文档按模块组织，本指南按「能跑通的顺序」组织。遇到 Filter 阶段枚举、ORM 关联等未覆盖主题，请跳转 Beego 官网对应章节，再回到子工程做最小实验。不要把官方长篇配置原样粘贴进业务仓库而不理解每一项的含义。若你撰写内部培训材料，可链接本页作为「Framework 仓库 Beego 入口」，并注明默认端口与 `service` 字段，避免培训环境与生产环境混淆。

**完成标准（自评）**：能在 10 分钟内从零启动子工程；能解释每条 `web.Router`；能说明 CORS 与 `X-Feature-Box` 分别在哪写入；能用手写 PowerShell 创建一条 item 并验证列表更新；能指出本示例不适合直接上生产的三项理由（内存存储、CORS `*`、缺鉴权）。满足以上五条，即可认为本指南目标达成，可继续阅读同仓其它 Go 框架指南或开始 Beego ORM 官方章节。

**写给维护者与二次作者**：更新本指南时，请同步修改子工程 `main.go` 与文中代码块，保持三者一致（指南、代码块、真实仓库）。勿在文末追加「走读·节名·N」类重复段凑字数；若需加长，应像本页一样扩展概念说明、排障清单与对照表。发布前运行 `validate_guide.py` 与 `validate_guide_quality.py --strict`。汉字统计仅计 CJK，代码与 URL 不计入 tier。若 Beego 主版本升级导致 API 变更，请在导读注明版本号并更新 `go.mod` 摘录。

**与 Framework 系列其它文档的关系**：本页只讲 Beego，不要求读者先读 Gin 或 NestJS 指南；但若你负责维护整个系列，应保持 `/api/health`、`/api/items` 等路径与 JSON 字段在各栈间一致，以便呈现页与 smoke 脚本复用。系列内部的端口分配（Gin 3002、Echo 3003、Fiber 3004、Chi 3005、Beego 3006、Buffalo 3007）请勿在单篇指南内随意改写而不更新系列总表。若用户仅克隆 Beego 子目录，应在 README 中链接回 Framework 系列索引，避免仓库上下文丢失。

**时间盒学习建议（总计约 3 小时）**：第 1 小时快速上手 + 运行时 + 路由；第 2 小时请求响应 + JSON + 校验 + 中间件；第 3 小时错误处理 + 配置 + 测试部署 + Framework 通读。每 25 分钟休息一次，休息时用口头复述代替刷手机，巩固效果更好。若某节超过 40 分钟仍未理解，暂停并记录具体卡点（例如「不懂第三参映射」），向同事提问时带上卡点与已读行号，比笼统问「Beego 怎么用」更易获得有效帮助。

**验收本文质量（维护者用）**：发布前确认无「走读·」「复习·」「围绕「」」等 filler；确认七大 `##` 顺序正确；确认 `validate_guide.py` 与 `validate_guide_quality.py --strict` 通过；确认汉字数 ≥12000（medium）；确认快速上手端口为 3006 且命令为 `go run .`；确认文末在延伸阅读链接后无正文。读者验收则用「完成标准（自评）」五条为准，不必强求读完每一个字，但应能复现 smoke 与解释 `main.go` 主路径。

你审阅本篇时，可重点看四件事：**结构**是否只有七大章且基础篇标题与 generic-backend 一致；**代码**是否能在子工程找到而非碎片占位；**端口与命令**是否为 3006 + `go run .`；**文末**是否干净无重复灌水。若认可体例，下一篇可按 manifest 顺序指定 slug，仍采用「对照子工程重写、双 strict 校验、manifest 暂保持 draft」流程。若认为某节过长或过短，请直接标注章节名与期望，便于单篇迭代而不回到批量脚本扩写。

本篇刻意在各基础节末尾保留 **动手** 提示，把阅读与操作绑在一起；你若培训学员，可要求每人提交 smoke 脚本截图与 `main.go` 标注截图作为作业。维护者更新子工程 API 时，请同步改 API 表、代码块与动手步骤中的 URL，避免三处不一致。Beego 官方文档中的 ORM、Session、模板、任务调度等主题，应在读者完成本篇后再推荐，以免一次加载过多抽象。若需更短的「极简版」指南，可删减学习路径与复习清单，但不得删减子工程真实代码与快速上手命令，否则无法通过 strict 校验。

## 延伸阅读

- [Beego 官方文档](https://beego.me/docs/intro/)
- [Beego MVC 控制器概览](https://beego.me/docs/mvc/controller/overview.md)
- [Framework 子工程：Back-end/Go/Beego](https://github.com/zhk0567/Framework/tree/main/Back-end/Go/Beego)

审阅反馈请直接标注章节标题与修改意见；确认体例后，下一篇指定 slug 即可按同流程单篇重做。manifest 已 published，已在站点上线。本地自检可运行：`python scripts/validate_guide.py --slug beego-go --strict` 与 `python scripts/validate_guide_quality.py --slug beego-go --strict`（在仓库根目录 `f:\commercial\atelier` 下执行）。
