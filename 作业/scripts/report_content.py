#!/usr/bin/env python3
"""Report body blocks for homework docx (plain text, no Markdown)."""

from __future__ import annotations

COVER = {
    "student_id": "B23070426",
    "name": "张浩坤",
    "major": "数据科学与大数据技术",
    "title": "基于 FastAPI 的个人站点在阿里云 ECS 上的部署与实现",
    "school": "洛阳理工学院",
}

SHOT_FILES = [
    "01-ECS实例概览.png",
    "02-安全组规则.png",
    "03-域名DNS解析.png",
    "04-SSH与系统版本.png",
    "05-git-clone与目录.png",
    "06-venv与pip安装.png",
    "07-systemctl-atelier.png",
    "08-nginx-t.png",
    "09-https证书.png",
    "10-curl本机探活.png",
    "11-浏览器首页.png",
    "12-浏览器Wiki或博客.png",
]

FIGURE_TITLES = [
    "阿里云 ECS 实例概览",
    "安全组入方向规则",
    "域名 DNS 解析",
    "SSH 登录与系统版本",
    "代码克隆与目录结构",
    "虚拟环境与依赖安装",
    "systemd 服务状态",
    "Nginx 配置检测",
    "HTTPS 证书配置",
    "本机服务探活",
    "公网访问站点首页",
    "Framework 博客系列页",
]

REFS = [
    "[1] 刘鹏. 云计算（第三版）[M]. 北京: 电子工业出版社, 2019.",
    "[2] FastAPI. FastAPI Documentation[EB/OL]. https://fastapi.tiangolo.com/, 2024.",
    "[3] NGINX Inc. NGINX Documentation[EB/OL]. https://nginx.org/en/docs/, 2024.",
    "[4] 阿里云. 云服务器 ECS 快速入门[EB/OL]. https://help.aliyun.com/product/25365.html, 2024.",
    "[5] Let's Encrypt. Certbot Instructions[EB/OL]. https://certbot.eff.org/, 2024.",
    "[6] Uvicorn. Uvicorn Deployment[EB/OL]. https://www.uvicorn.org/, 2024.",
    "[7] Python Software Foundation. Python 3.11 Documentation[EB/OL]. https://docs.python.org/3.11/, 2024.",
    "[8] Jinja. Jinja2 Documentation[EB/OL]. https://jinja.palletsprojects.com/, 2024.",
    "[9] systemd. systemd.service Manual[EB/OL]. https://www.freedesktop.org/software/systemd/man/systemd.service.html, 2024.",
    "[10] 课程讲义. 云计算技术[M]. 2025-2026 学年.",
]


def get_blocks() -> list:
    b: list = []

    # ========== 第1章 ==========
    b.append(("h1", "第1章 绪论"))
    b.append(("h2", "1.1 研究背景"))
    b.append(("body",
        "云计算是一种通过网络按需提供可伸缩 IT 资源的服务模式。租户无需自行采购物理服务器、"
        "交换机与机房空调，即可在分钟级获得虚拟机、块存储与公网带宽，并按实际使用量计费。"
        "在基础设施即服务（IaaS）层级，云厂商负责硬件与虚拟化平台，用户负责操作系统之上的全部软件栈，"
        "包括语言运行时、Web 服务器、业务代码与域名证书。典型 Web 系统上云流程为：创建云主机、"
        "配置安全组与防火墙、安装依赖、部署应用、绑定域名、配置 HTTPS、进行功能与安全测试。"
        "该模式初始成本低、扩容灵活，已成为高校《云计算技术》课程验证学生工程实践能力的主要载体。"))
    b.append(("body",
        "本人为洛阳理工学院数据科学与大数据技术专业学生，长期开展 Python 后端、Kotlin Android、"
        "计算机视觉与语音交互等方向的开发与竞赛实践。已完成的代表性工作包括：智能学习终端（Web 与微信小程序）、"
        "服装图像深度学习分类（PyTorch 训练至 Android ONNX 推理）、Framework 多技术栈对照仓库、"
        "英语口语训练应用、NEXUS 智能语音平台、llm-agents 框架探索以及 Algorithm 算法与数据结构库。"
        "这些成果原先分散在多个 GitHub/Gitee 仓库中，答辩或求职时需要反复切换链接，Wiki 与教程难以统一检索。"
        "因此建设 atelier 个人站点并绑定域名 https://zhkun.xyz，将项目卡片、DeepWiki 文档、"
        "系列技术博客、Excel 个人记录与旅行相册聚合到同一 Web 入口，并部署于阿里云 ECS 对外提供服务。"
        "该站点同时作为本课程开发类选题二「在云平台部署可公网访问网站」的完整交付实例。"))
    b.append(("h2", "1.2 云计算服务模型与选型"))
    b.append(("body",
        "云计算通常划分为 IaaS、PaaS、SaaS 三层。IaaS 提供虚拟机与网络，灵活性最高；"
        "PaaS 提供托管运行时，部署更简单但约束较多；SaaS 为开箱即用应用。"
        "atelier 选用 IaaS（阿里云 ECS）是因为需要完全控制 Nginx、Python 版本与 systemd 单元，"
        "以便在报告中完整呈现从操作系统到应用层的部署链路，符合课程对「配置过程可截图、可复述」的要求。"))
    b.append(("table", "表1-1 云计算服务模型对比", ["模型", "代表产品", "用户管理范围", "适用场景"], [
        ["IaaS", "阿里云 ECS、华为云 ECS", "OS 及以上", "自定义 Web 栈、课程实验"],
        ["PaaS", "Railway、App Engine", "应用与数据", "快速上线、少运维"],
        ["SaaS", "Office 365、钉钉", "账号与配置", "直接使用成品软件"],
    ]))
    b.append(("h2", "1.3 本文结构"))
    b.append(("body",
        "第2章给出功能与非功能需求及总体架构；第3章重点说明线上网站各 URL 与页面模块（全文篇幅最大）；"
        "第4章介绍 FastAPI 实现与安全设计；第5章记录阿里云 ECS 部署、HTTPS 配置与测试；"
        "第6章说明本地开发与线上维护；第7章总结；附录 A 给出部署检查清单。"))
    b.append(("body",
        "各章导读如下。第2章从「站点要做什么」出发，将首页、项目、博客、Wiki、browse、旅行与辅助功能"
        "逐条写成可验收的需求条目，并给出非功能指标表与 URL 路由一览，为第3章页面说明提供索引。"
        "第3章面向答辩观众，用用户视角描述打开每个链接所见内容与可操作项，"
        "并对七个代表性项目分别撰写分节，是报告篇幅最大的章节。"
        "第4章面向实现细节，说明 FastAPI 模块划分、Markdown 渲染数据流与安全中间件。"
        "第5章面向云平台实践，按 ECS、软件安装、systemd、Nginx、HTTPS、测试与排障顺序展开，"
        "嵌入十二张部署与访问截图。第6章与附录 A 供日后运维对照使用。"))
    b.append(("h2", "1.4 云计算与 Web 部署的关键环节"))
    b.append(("body",
        "从教学视角看，一次完整的云 Web 部署至少包含资源层、网络层、平台层与应用层四个环节。"
        "资源层指 ECS 规格、磁盘与公网 IP 的选择；网络层指安全组、防火墙与 DNS 解析；"
        "平台层指操作系统补丁、Python 虚拟环境、Nginx 与 systemd；应用层指业务代码、静态资源与内容文件。"
        "任一环节缺失都会导致「本地能跑、公网不可达」或「HTTP 可访问、HTTPS 失败」等问题。"
        "本报告第5章按上述顺序展开，并在 5.6 节汇总常见问题，便于对照排查。"))
    b.append(("body",
        "atelier 作为只读站点，没有数据库主从、消息队列等复杂中间件，"
        "因此部署拓扑相对清晰：单台 ECS 单实例 FastAPI 即可支撑个人站流量。"
        "当访问量增大时，可通过垂直扩容 ECS、接入 CDN 或增加 Nginx 缓存策略优化，"
        "这些可作为课程之外的扩展方向在第七章简要讨论。"))
    b.append(("h2", "1.5 个人站点建设动机与课程对应"))
    b.append(("body",
        "在建设统一门户之前，本人的项目文档分散在 GitHub、Gitee、DeepWiki 导出目录与本地 Excel 中。"
        "答辩时需要同时打开多个浏览器标签页，检索 Framework 某技术栈的端口约定或 Algorithm 某专题教程时，"
        "往往要在仓库 README、Wiki 分页与博客 manifest 之间反复切换。"
        "建设 atelier 的动机可以概括为三点：第一，用单一域名聚合七个代表性项目，形成可对外展示的作品集入口；"
        "第二，将 Wiki 架构文档与 Blog 读者教程分层呈现，降低 Framework 与 Algorithm 两类内容的混淆；"
        "第三，把书籍、番剧、电影、游戏等个人记录纳入 browse 模块，使站点兼具技术展示与生活记录功能。"))
    b.append(("body",
        "课程开发类选题二要求「在云平台部署可公网访问网站」，并提交不少于二十页报告与十张以上部署截图。"
        "本报告在实现层面选用阿里云 IaaS，完整走通 ECS 创建、安全组、DNS、Python 虚拟环境、"
        "systemd 托管、Nginx 反代与 Certbot 证书链路；在内容层面选用真实线上站点 zhkun.xyz，"
        "使第3章页面说明与第5章测试结果均可在答辩现场即时打开验证，而非虚构 Demo 页面。"
        "因此本文既是课程大作业文档，也是站点长期运维的说明材料。"))

    # ========== 第2章 ==========
    b.append(("h1", "第2章 需求分析与总体设计"))
    b.append(("h2", "2.1 功能需求"))
    b.append(("body",
        "站点定位为只读个人知识门户：不提供用户注册、表单提交或数据库读写，全部内容来自 Git 仓库内文件，"
        "更新以 git pull 为主。具体功能需求如下。"))
    b.append(("body",
        "（1）首页：展示个人标语、学校信息、四条置顶项目卡片、博客系列入口（Framework 124 篇、Algorithm 83 篇、热点专题）、"
        "个人概览侧栏与数据分类快捷块，支持动态壁纸与明暗主题切换。"))
    b.append(("body",
        "（2）项目：/projects 列出全部七个项目；/project/{id} 展示摘要、亮点列表与 Wiki 分页导航。"))
    b.append(("body",
        "（3）博客：/blog 总索引；/blog/series/framework 与 /blog/series/algorithm 系列页；"
        "/blog/{slug} 单篇阅读，支持代码高亮与页内目录。"))
    b.append(("body",
        "（4）Wiki：/docs/{wiki_slug}/{page} 阅读七套 DeepWiki 导出，侧栏分页导航，slug 白名单校验。"))
    b.append(("body",
        "（5）数据浏览：/browse/books、/browse/anime、/browse/movies、/browse/games 等，解析 zhita_settings.xlsx。"))
    b.append(("body",
        "（6）旅行：/travel 行程列表，/travel/{trip_id} 照片网格与说明。"))
    b.append(("body",
        "（7）辅助：顶栏全站搜索、壁纸切换、Live2D 模型、/api/site 最小 JSON 接口。"))
    b.append(("body",
        "上述功能均可在 https://zhkun.xyz 上逐项验证。用户无需登录即可浏览全部公开内容，"
        "降低了运维复杂度（无会话、无 CSRF、无密码存储），"
        "也使课程大作业的安全分析可以集中在网络层与应用层只读防御，而不涉及账号体系设计。"))
    b.append(("h2", "2.1.1 用户典型访问场景"))
    b.append(("body",
        "场景一：答辩展示。打开首页展示四个置顶项目，点击进入 /project/nexus 阅读 Wiki 分页，"
        "或进入 /blog/series/framework 展示 124 篇指南组织能力。"
        "场景二：求职作品集。通过单一域名向面试官展示 CV、语音、Agent 等多方向项目卡片与 GitHub 链接。"
        "场景三：自学查阅。在 Framework 指南中检索某技术栈的 PORT 与 health 约定，"
        "或在 Algorithm 系列中阅读专题教程。站点搜索框支持跨模块关键字过滤。"))
    b.append(("h2", "2.2 非功能需求"))
    b.append(("table", "表2-2 非功能需求与实现", ["维度", "目标", "实现手段"], [
        ["可用性", "7×24 公网访问", "systemd 托管 uvicorn，FailureAction=restart"],
        ["安全性", "抗扫描、限流", "TrustedHost、probe 拦截、Nginx limit_req"],
        ["性能", "首屏可接受", "Markdown 缓存、静态 Cache-Control、移动禁视频壁纸"],
        ["可维护性", "内容易更新", "无数据库，git pull + restart"],
        ["兼容性", "HTTPS + 移动端", "Certbot、响应式 CSS"],
    ]))
    b.append(("h2", "2.3 总体架构"))
    b.append(("body",
        "公网用户经 DNS 将 zhkun.xyz 解析至 ECS 公网 IP。请求到达 Nginx（443/80），"
        "完成 TLS 与限流后反代至 127.0.0.1:8000 的 uvicorn/FastAPI。"
        "FastAPI 匹配路由，读取 Markdown/xlsx/json，经 Jinja2 渲染 HTML，或通过 StaticFiles 返回静态资源。"
        "Certbot 维护 Let’s Encrypt 证书自动续期。"))
    b.append(("body",
        "从请求生命周期看：浏览器发起 HTTPS 请求 → Nginx 解密 TLS 并限流 →"
        "反代至 FastAPI → 路由函数读取磁盘 → Markdown 渲染或模板渲染 → HTML 响应 →"
        "Nginx 返回客户端。静态文件 /static/ 同样经 Nginx 转发，由 CachedStaticFiles 设置缓存头。"
        "壁纸视频 /wallpaper/ 路径因文件较大，在 Nginx 与 FastAPI 双侧配置更严格的限流阈值。"))
    b.append(("table", "表2-3 主要 URL 路由一览", ["URL 模式", "模块", "数据来源"], [
        ["/", "首页", "projects.json、manifest"],
        ["/projects", "项目列表", "projects.json"],
        ["/project/{id}", "项目详情", "projects.json + Wiki 索引"],
        ["/blog/series/framework", "Framework 指南", "Blog/framework-guides/"],
        ["/docs/{slug}/{page}", "Wiki", "Wiki/{slug}/"],
        ["/browse/{hub_id}", "数据浏览", "zhita_settings.xlsx"],
        ["/travel/{trip_id}", "旅行相册", "static/uploads/travel/"],
    ]))
    b.append(("table", "表2-4 主要技术选型", ["类别", "选型", "说明"], [
        ["云平台", "阿里云 ECS", "Alibaba Cloud Linux 3"],
        ["框架", "FastAPI + Jinja2", "ASGI + SSR"],
        ["服务器", "uvicorn + systemd", "生产常驻"],
        ["代理", "Nginx + Certbot", "HTTPS 与限流"],
        ["内容", "md / xlsx / json", "无关系型数据库"],
    ]))
    b.append(("h2", "2.4 内容与部署边界"))
    b.append(("body",
        "atelier 将「内容仓库」与「运行环境」明确分离：全部页面数据来自 Git 跟踪的文件，"
        "ECS 上不单独维护 MySQL 或 Redis。Wiki 与 Blog 的 Markdown、projects.json、"
        "zhita_settings.xlsx、wallpapers.json 与 static/uploads 均在 clone 后随代码一并存在。"
        "更新流程为开发者本地编辑 → push 至 Gitee → SSH 至 ECS 执行 git pull 与 systemctl restart。"
        "该边界使备份策略简化为「备份 Git 远程仓库 + 定期快照 ECS 磁盘」，"
        "也使本报告第6章维护说明可以围绕文件编辑而非数据库迁移展开。"))
    b.append(("body",
        "安全边界方面，生产环境关闭 FastAPI 自带 Swagger，不暴露 /docs 与 /redoc；"
        "Nginx 作为唯一公网入口，uvicorn 仅监听 127.0.0.1:8000，"
        "即使应用层存在漏洞，攻击者也无法直接绕过 Nginx 访问后端端口。"
        "TrustedHost 中间件限制 Host 头为 zhkun.xyz 等合法域名，"
        "配合 BLOCK_PROBE_PATHS 拦截对 /.env、/.git 等常见扫描路径的请求。"
        "上述设计在第二章以非功能需求表概括，在第四章以中间件与环境变量表展开。"))

    # ========== 第3章（重点） ==========
    b.append(("h1", "第3章 网站功能与页面详细说明"))
    b.append(("body",
        "本章结合线上 https://zhkun.xyz 的实际结构，说明用户在各 URL 下看到的内容、可执行的操作与数据来源。"
        "部署到云服务器的并非演示用单页，而是涵盖项目展示、技术文档、系列教程与个人数据的综合门户。"))

    b.append(("h2", "3.1 全站布局与导航"))
    b.append(("body",
        "站点采用 Minecraft 像素风视觉语言：工作台、书橱等方块图标、半透明内容卡片、"
        "可选全屏动态视频壁纸（春泽、栖野、渊光等系列，配置于 data/wallpapers.json）。"
        "顶栏左侧为站点标识 zhk；中部为搜索 combobox，可检索项目标题、Wiki 页名与博客 slug；"
        "右侧为壁纸下拉与明暗主题切换。侧栏分「站点」与「数据分类」两组："
        "站点含主页面、项目、博客、个人旅游；数据分类含书籍、番剧、电影、游戏等 browse 入口。"
        "页脚标注版权与第三方图标协议。全站 header/footer 由 app/context.py 的 site_context() 统一注入，保证各页导航一致。"))
    b.append(("body",
        "搜索功能在应用启动 lifespan 阶段调用 build_site_search_index，将项目、Wiki 与博客标题索引到内存。"
        "用户在顶栏输入关键字即可过滤并跳转，避免在 124 篇 Framework 指南与多套 Wiki 之间手工查找。"))

    b.append(("h2", "3.2 首页"))
    b.append(("body",
        "访问 / 时，Hero 区展示标语「用数据与工程，把算法做成能上线的产品」以及「洛阳理工学院·本科」。"
        "「特色项目」区展示 config/projects.json 中 pinned_ids 指定的四条置顶卡片，"
        "每条含 category 标签、摘要、技术 tags 与 GitHub/Wiki 链接。"
        "其下「博客」区块列出 Framework 技术栈指南 124 篇、Algorithm 算法专题 83 篇、热点专题 1 篇的系列入口。"
        "右侧「个人概览」含开发方向（AI、CV、语音、OCR 等）、联系邮箱与统计数字；"
        "「数据分类」快捷块可跳转 browse 各 hub。图5-11 为公网首页截图，可见上述模块同时在线运行。"))
    b.append(("body",
        "首页右侧「统计」区展示应用项目数量与数据分类数量，"
        "与侧栏 books/anime/movies/games 条目数一致，形成对整个站点内容规模的直观印象。"
        "首页项目卡片使用 Minecraft 风格缩略图（工作台、书架等），"
        "由 app/context.py 中 PROJECT_THUMB_STEMS 与 wiki_assets 映射生成，"
        "使视觉风格与全站 UI 统一。点击「进入博客」或系列链接可无缝跳转至对应系列页，"
        "URL 变化但 header/footer 保持不变，用户体验连贯。"))
    b.append(("body",
        "首页加载时，lifespan 已预热的壁纸列表与搜索索引使首屏响应时间在可接受范围内。"
        "若用户切换壁纸，前端请求 /wallpaper/ 路由，后端按 wallpapers.json 返回对应媒体流。"
        "暗色主题下卡片背景与文字对比度经 CSS 变量调整，保证长时间阅读 Wiki 或博客时的可读性。"))

    b.append(("h2", "3.3 项目展示模块"))
    b.append(("body",
        "/projects 以卡片网格展示全部七个项目；/project/{id} 展示更完整摘要，"
        "并将 highlights 字段渲染为 HTML 列表，同时列出该 wiki_slug 下 Wiki 全部分页链接。"
        "以下分述各项目在站点中的入口与文档关系。"))

    projects_detail = [
        ("3.3.1 古韵薪传·智能学习终端",
         "多端智能学习终端，Web 与微信小程序协同，覆盖故事内容管理、主题系统、状态管理与构建部署。"
         "技术标签含 Web、微信小程序、React。站点入口 /project/learning-terminal，"
         "Wiki 路径 /docs/Intelligent-Learning-Terminal-guyunxinchuan/page-*，"
         "可查阅组件库、导航路由与数据流设计说明。首页置顶展示，便于答辩时快速进入文档。"),
        ("3.3.2 服装图像深度学习分类",
         "基于 ResNet18 与 DeepFashion 的服饰识别系统，含训练流水线、模型导出与 Android 端 ONNX 推理。"
         "标签含 PyTorch、ResNet18、Kotlin。Wiki：/docs/Clothing-Classification/page-* 描述训练、"
         "后端 API 与移动端 Material3 界面。站点卡片链向 GitHub 源码，适合展示 CV 从训练到端侧落地路径。"),
        ("3.3.3 Framework 多技术栈示例",
         "汇集 Laravel、Symfony、Go、Node、Python 等后端与 React Native、Svelte、Astro 等前端对照实现。"
         "Wiki：/docs/Framework/page-* 说明 monorepo 结构；Blog：/blog/series/framework 提供 124 篇读者向指南。"
         "Wiki 偏仓库结构，Blog 偏安装部署教程，URL 空间分离避免混淆。"),
        ("3.3.4 英语口语训练应用",
         "基于 TED Talks 与 Psych2Go 的 Android 口语训练，含跟读、倍速、段落同步、悬浮查词，版本 v0.1.1。"
         "Wiki：/docs/English-Speaking-Trainer/page-*。站点摘要强调 Kotlin 与 Gson、协程等技术栈。"),
        ("3.3.5 NEXUS Unified 智能语音交互平台",
         "企业级语音交互：Dolphin ASR、DeepSeek 对话、Edge-TTS 合成，Jetpack Compose UI，"
         "支持连续对话、故事阅读与监控。Wiki：/docs/NEXUS/page-* 含 ASR 模块、WebSocket 对话服务、"
         "Android UI 等分页，是站点中最复杂的 AI 类项目文档集之一。"),
        ("3.3.6 llm-agents 框架探索",
         "多语言 AI Agent 框架对比与实现，覆盖 LangGraph、CrewAI、LlamaIndex 等，支持 Ollama 本地模型。"
         "Wiki：/docs/llm-agents/page-* 含框架对比矩阵与 Python/TypeScript 参考实现说明。"),
        ("3.3.7 Algorithm 算法与数据结构",
         "Python/C++ 双语言算法库，含数据结构、LeetCode 专题与面试指南。"
         "Wiki：/docs/Algorithm/page-*；Blog：/blog/series/algorithm 为 83 篇专题教程系列，"
         "与 GitHub 单题题解区分，站点侧重复展开 LeetCode 逐题文档。"),
    ]
    for h, text in projects_detail:
        b.append(("h3", h))
        b.append(("body", text))
        b.append(("body",
            "用户在站点内可通过项目详情页一键跳转 GitHub 源码仓库，"
            "并通过 Wiki 侧栏逐页阅读架构说明，无需在浏览器中记忆 DeepWiki 或仓库目录结构。"
            "该设计将「代码仓库」与「在线文档」之间的跳转成本降到最低，"
            "也是 atelier 区别于普通静态主页的核心价值之一。"))

    b.append(("body",
        "七个项目在首页仅展示四条置顶，其余三条在 /projects 完整列表中呈现，"
        "避免首页信息过载，同时保证 NEXUS、llm-agents、Algorithm 等同样获得 Wiki 与详情页入口。"))

    b.append(("table", "表3-1 七个项目站点入口一览", ["项目", "详情页", "Wiki slug"], [
        ["智能学习终端", "/project/learning-terminal", "Intelligent-Learning-Terminal-guyunxinchuan"],
        ["服装分类", "/project/clothing-classification", "Clothing-Classification"],
        ["Framework", "/project/framework", "Framework"],
        ["口语训练", "/project/english-speaking-trainer", "English-Speaking-Trainer"],
        ["NEXUS", "/project/nexus", "NEXUS"],
        ["llm-agents", "/project/llm-agents", "llm-agents"],
        ["Algorithm", "/project/algorithm", "Algorithm"],
    ]))

    b.append(("h2", "3.4 博客模块"))
    b.append(("body",
        "/blog 为博客总索引，按 series 分为 framework、algorithm、hotspot 与其余独立文章。"
        "/blog/series/framework 按 Back-end、Front-end 等大类分组展示 124 篇 stack 指南，"
        "每篇 slug 对应 Blog/framework-guides 下 index.md，正文含 PORT 环境变量、health 探针路径、"
        "本地启动与生产部署命令，服务于 Framework monorepo 读者。"
        "/blog/series/algorithm 展示 83 篇算法专题双语教程。"
        "/blog/{slug} 由 render_blog_markdown 渲染，支持代码块高亮、页内 TOC、系列 prev/next 导航。"
        "渲染结果进程内缓存，减轻 ECS 重复解析长文的 CPU 压力。"
        "图5-12 为 /blog/series/framework 公网截图，可见 Actixweb、Adonisjs、Gin 等条目与 Minecraft 风格卡片。"))
    b.append(("body",
        "Framework 指南的维护流程为：在 Framework 源码仓更新文档 → 扫描生成 manifest →"
        "atelier 侧 Blog/framework-guides 下 index.md 与 validate_guide.py 校验 → git push →"
        "ECS git pull 重启服务。Algorithm 系列同理。"
        "单篇博客 URL 形如 /blog/fastapi-python，页面内可显示所属系列与相邻文章链接，"
        "方便读者连续阅读同一技术栈的多章节内容。"))
    b.append(("body",
        "除系列外，站点还支持独立博文（如认识简谱等），在 /blog 索引的「其他」区展示，"
        "证明博客管道不仅服务 124+83 篇系列，也可挂载单篇 Markdown 文章。"))

    b.append(("h2", "3.5 Wiki 模块"))
    b.append(("body",
        "Wiki 路由 /docs/{wiki_slug}/{page} 读取 Wiki 目录下 Markdown。"
        "wiki_slug_is_valid 校验 slug 合法性；build_wiki_doc_nav 生成侧栏分页；正文支持 Mermaid。"
        "七套 Wiki 与第七章项目一一对应。Wiki 侧重仓库架构与模块接口；"
        "Blog 侧重面向读者的教程步骤；二者关于 Framework 仓库的内容分工不同但互补。"))
    b.append(("body",
        "以 NEXUS 为例，Wiki 中包含 page-1 项目简介、page-6 AI 对话服务（WebSocket、JWT、消息流水线）、"
        "Android Compose UI 说明等分页，每页经 render_wiki_markdown 转为 HTML 并在 wiki.html 模板中渲染。"
        "访问 /docs/NEXUS/page-6 时，侧栏高亮当前页，底部可切换同项目其他 page。"
        "若 slug 不在白名单或 page 文件不存在，服务器返回 404，防止路径遍历读取任意 Markdown。"))

    b.append(("h2", "3.6 数据浏览 browse"))
    b.append(("body",
        "site_data.py 解析 zhita_settings.xlsx，build_data_hubs 生成多个 hub。"
        "/browse/{hub_id} 以 browse.html 分节展示表格行。"
        "导航默认展示：书籍 66 条、番剧 287 条、电影 67 条、游戏 131 条（数量为线上统计示例）。"
        "证书、爱好等 hub 可通过直链访问但不在侧栏重复展示。"))
    b.append(("table", "表3-2 数据 hub 统计", ["hub_id", "导航标签", "约条数"], [
        ["books", "书籍", "66"],
        ["anime", "番剧", "287"],
        ["movies", "电影", "67"],
        ["games", "游戏", "131"],
    ]))
    b.append(("body",
        "browse 页面采用分节表格布局：每个 hub 对应 xlsx 中一个工作表或命名区域，"
        "列标题经 site_data 映射为中文标签，行数据原样渲染为 HTML 表格。"
        "用户可在 /browse/books 浏览书名、作者、阅读状态等字段，"
        "在 /browse/anime 浏览番剧名称、进度与评分。"
        "因数据来自同一份 xlsx，更新 Excel 后重启服务即可全站同步，"
        "无需编写 SQL 或管理后台表单。"))

    b.append(("h2", "3.7 旅行相册"))
    b.append(("body",
        "travel_catalog 扫描 static/uploads/travel，/travel 列出行程卡片，"
        "/travel/{trip_id} 展示照片网格与说明。图片含 thumb、web 等衍生尺寸，"
        "降低公网带宽消耗，证明站点除技术文档外亦支持富媒体静态内容分发。"))
    b.append(("body",
        "旅行模块与 Wiki、博客并列出现在侧栏「个人旅游」入口。"
        "列表页每张卡片展示行程标题、日期范围与封面缩略图；"
        "详情页以网格排列原图与说明文字，点击可查看较大尺寸的 web 衍生图。"
        "图片文件不存入数据库，而是按目录结构组织，"
        "新增一次旅行只需在 uploads/travel 下增加子目录与 meta 描述，"
        "重启或刷新 catalog 缓存后即可在 /travel 出现新卡片。"
        "该模块在答辩中可展示站点除技术文档外的多媒体承载能力。"))

    b.append(("h2", "3.8 壁纸、Live2D 与 API"))
    b.append(("body",
        "壁纸：data/wallpapers.json 维护 id、file、label；/wallpaper/ 路由单独限流；"
        "客户端宽度 ≤720px 时不加载视频壁纸。"
        "Live2D：MC_Vtuber 模型挂全站右下角，点击切换表情。"
        "生产环境 /api/site 仅返回 site_name、site_title，不暴露服务器路径。"))
    b.append(("body",
        "主题切换通过前端 JavaScript 写入 localStorage，刷新后保持用户选择的明暗模式。"
        "壁纸切换通过顶栏下拉修改当前 session 的壁纸 id，后端 /wallpaper/ 路由按 id 返回对应 mp4 或图片流。"
        "Live2D 模块依赖 scripts/ensure_live2d_vendor.py 安装 Cubism Web 运行时，"
        "模型文件位于 MC_Vtuber/ 目录，由 create_app 在检测到 model3.json 存在时挂载静态路由。"
        "这些交互功能不影响核心文档阅读，但提升了个人站的品牌识别度与浏览体验。"))
    b.append(("table", "表3-3 主要 URL 与功能对照", ["URL", "用户可见内容", "数据"], [
        ["/", "简介、置顶项目、博客入口", "projects.json"],
        ["/blog/series/framework", "124 篇指南分组", "Blog/"],
        ["/docs/NEXUS/page-6", "AI 对话 Wiki", "Wiki/NEXUS"],
        ["/browse/anime", "番剧记录表", "xlsx"],
        ["/travel", "旅行列表", "uploads/travel"],
    ]))
    b.append(("h2", "3.9 全站搜索与响应式体验"))
    b.append(("body",
        "顶栏搜索框是跨模块导航的关键入口。应用启动时 build_site_search_index 将七个项目标题、"
        "各 Wiki 分页文件名、Framework 与 Algorithm 系列博客 slug 汇总为内存索引。"
        "用户输入「NEXUS」「FastAPI」「ResNet」等关键字时，前端过滤候选项并生成直达链接，"
        "点击后跳转至 /project/nexus、/blog/fastapi-python 或 /docs/Clothing-Classification/page-* 等目标页。"
        "该机制在 Wiki 分页数量多、博客篇数过百时显著降低查找成本，"
        "也是静态文件驱动站点替代全文检索引擎的轻量实现。"))
    b.append(("body",
        "响应式方面，模板使用 CSS 变量控制明暗主题与卡片透明度，"
        "窄屏下侧栏折叠为可展开菜单，browse 表格允许横向滚动。"
        "移动网络下禁用全屏视频壁纸，仅保留静态背景或轻量图片，"
        "避免在蜂窝数据环境下自动加载数十 MB 的 mp4 文件。"
        "Live2D 模型在触控设备上仍可点击切换表情，但不遮挡正文阅读区域。"
        "上述体验细节共同保证站点在答辩用笔记本与观众手机浏览器上均可正常浏览。"))

    # ========== 第4章 ==========
    b.append(("h1", "第4章 系统设计与实现"))
    b.append(("h2", "4.1 应用入口与路由"))
    b.append(("body",
        "main.py 为 uvicorn 入口；create_app() 构建 FastAPI，关闭 /docs 与 /redoc，"
        "register_security_middleware 注册安全中间件，按模块挂载路由："
        "assets（壁纸等）、home（/）、browse、projects、blog、travel、wiki；"
        "mount /static 与可选 /static/MC_Vtuber。lifespan 预热 site_data、Wiki 索引、壁纸、旅行与搜索。"))
    b.append(("table", "表4-1 路由模块职责", ["模块文件", "主要路径", "职责"], [
        ["home.py", "/", "首页、置顶项目、博客入口统计"],
        ["projects.py", "/projects, /project/{id}", "项目列表与详情"],
        ["blog.py", "/blog, /blog/series/*, /blog/{slug}", "博客索引与渲染"],
        ["wiki.py", "/docs/{slug}/{page}", "Wiki 渲染与导航"],
        ["browse.py", "/browse/{hub_id}", "Excel hub 浏览"],
        ["travel.py", "/travel, /travel/{id}", "旅行相册"],
        ["assets.py", "/wallpaper/*, /api/site", "壁纸与元信息 API"],
    ]))
    b.append(("h2", "4.2 数据流与渲染"))
    b.append(("body",
        "数据流：磁盘文件（Markdown/xlsx/json）→ site_data.py 解析与 manifest 聚合 →"
        "routes 调用 markdown 子包渲染 → Jinja2 模板输出 HTML。"
        "app/markdown/blog.py、wiki.py、render.py 统一处理 frontmatter、代码高亮、Mermaid 与 TOC。"
        "app/context.py 注入 SITE_NAME、wiki_nav、wallpapers、data_hubs 等全局变量。"))
    b.append(("body",
        "以浏览一篇 Framework 指南为例：用户请求 /blog/fastapi-python → blog.py 定位 slug →"
        "render_blog_markdown 读取 Blog/framework-guides/fastapi-python/index.md →"
        "解析 frontmatter 与 Markdown 正文 → 生成 HTML 与页内 TOC →"
        "blog_post.html 模板注入 site_context 与文章内容 → 返回带缓存头的 HTML。"
        "Wiki 流程类似，但增加 wiki_slug 校验与 doc_nav 侧栏生成。"
        "browse 流程则跳过 Markdown，直接由 get_browse_page 将 xlsx 解析结果传给 browse.html。"))
    b.append(("h2", "4.3 安全设计"))
    b.append(("body",
        "分层防御：Nginx 限流与超时 → FastAPI TrustedHost、slowapi 限流、探测路径 404 →"
        "应用层 Wiki slug 白名单、壁纸路径 relative_to(DATA_DIR) 校验。"))
    b.append(("table", "表4-2 生产环境变量", ["变量", "典型值", "作用"], [
        ["ATELIER_ENV", "production", "启用安全中间件与限流"],
        ["TRUSTED_HOSTS", "zhkun.xyz,...", "Host 白名单"],
        ["RATE_LIMIT_DEFAULT", "120/minute", "普通页面 IP 配额"],
        ["RATE_LIMIT_WALLPAPER", "30/minute", "壁纸路径配额"],
        ["BLOCK_PROBE_PATHS", "1", "拦截 /.env 等扫描"],
    ]))
    b.append(("h2", "4.4 关键实现片段"))
    b.append(("body", "应用工厂核心逻辑（节选）："))
    b.append(("code",
        "def create_app() -> FastAPI:\n"
        "    app = FastAPI(docs_url=None, redoc_url=None, lifespan=_lifespan)\n"
        "    register_security_middleware(app)\n"
        "    app.include_router(home.router)\n"
        "    app.include_router(projects.router)\n"
        "    app.include_router(blog.router)\n"
        "    app.include_router(wiki.router)\n"
        "    app.mount(\"/static\", CachedStaticFiles(...))\n"
        "    return app"))
    b.append(("body",
        "Nginx 侧定义 upstream atelier_backend { server 127.0.0.1:8000; }，"
        "按 /、/static/、/wallpaper/ 配置不同 limit_req 与 proxy_read_timeout，"
        "并传递 X-Forwarded-Proto 使应用感知 HTTPS。"))
    b.append(("h2", "4.5 配置与扩展点"))
    b.append(("body",
        "config/site.example.json 定义路径模板，复制为 site.local.json 后可设置本机 framework_root，"
        "供本地调试 Framework 指南生成脚本。环境变量 FRAMEWORK_ROOT 优先级更高。"
        "config/projects.json 驱动首页与项目页卡片，pinned_ids 控制置顶顺序。"
        "site_identity.json 与 constants.py 定义站点名称、标语、邮箱等 UI 文案。"
        "zhita_settings.xlsx 由 site_data.py 解析，无需改代码即可更新书籍、番剧等表格数据。"))
    b.append(("body",
        "性能方面，Wiki 与博客 Markdown 渲染结果缓存在进程内存，静态资源通过 CachedStaticFiles 设置 Cache-Control。"
        "手机端模板检测 viewport 宽度，自动禁用视频壁纸，减少移动网络流量消耗。"
        "这些策略使单台 1 核 2G ECS 即可稳定承载个人站日常访问。"))
    b.append(("h2", "4.6 中间件执行顺序与异常处理"))
    b.append(("body",
        "register_security_middleware 在 create_app 中于路由注册之前调用，"
        "保证每个 HTTP 请求先经过 TrustedHost 校验，再进入 slowapi 限流计数，"
        "最后才匹配 home、blog、wiki 等业务路由。"
        "当 Host 头不在 TRUSTED_HOSTS 列表时，中间件直接返回 400，"
        "避免 Host 头攻击导致缓存污染或密码重置链接伪造。"
        "当同一 IP 在 RATE_LIMIT_DEFAULT 窗口内请求次数超限时，返回 429 与 Retry-After 提示，"
        "壁纸路径 /wallpaper/ 使用更严格的 RATE_LIMIT_WALLPAPER 配额，"
        "防止恶意脚本高频拉取大体积视频文件占用带宽。"))
    b.append(("body",
        "探测路径拦截由 BLOCK_PROBE_PATHS 环境变量控制："
        "对 /.env、/wp-admin、/.git/config 等常见扫描 URL 统一返回 404，"
        "不在 access log 中泄露文件是否存在的信息。"
        "Wiki 与 browse 路由在业务层再次校验 slug 与 hub_id，"
        "非法参数返回 404 而非 500，避免向客户端暴露 Python 堆栈。"
        "生产环境 uvicorn 以 atelier 系统用户运行，进程无权读取 /root 目录，"
        "即使代码存在路径拼接缺陷，也受操作系统权限进一步约束。"))

    # ========== 第5章 ==========
    b.append(("h1", "第5章 云平台部署与测试"))
    b.append(("body", "部署环境：阿里云 ECS，Alibaba Cloud Linux 3，域名 zhkun.xyz，安全组 22/80/443。"))

    b.append(("h2", "5.1 云资源与网络"))
    b.append(("body",
        "目的：获得公网可达的 Linux 虚拟机与网络安全边界。"
        "在阿里云控制台创建 ECS，绑定公网 IP；安全组入方向放行 TCP 22、80、443；"
        "域名 A 记录指向 ECS IP；SSH 登录执行 cat /etc/os-release 确认系统。"
        "注意：仅开放必要端口，缩小攻击面。"))
    b.append(("body",
        "ECS 规格方面，个人知识站以静态渲染为主，1 核 2 GB 内存即可满足日常访问；"
        "系统盘建议 40 GB 以上，以容纳 Wiki、Blog 大量 Markdown 与 static 媒体。"
        "地域选择应靠近主要访问人群以降低延迟，本实例面向国内访问，选用华北或华东节点。"
        "公网带宽按量计费或固定带宽均可，答辩期间流量峰值有限，"
        "但 HTTPS 与壁纸视频仍建议预留至少 1 Mbps 上行。"
        "图5-1 至图5-3 分别对应实例概览、安全组规则与 DNS 解析配置界面。"))
    b.append(("figures", 5, [0, 1, 2, 3]))

    b.append(("h2", "5.2 系统软件与代码部署"))
    b.append(("body",
        "目的：安装运行时与 Web 依赖，拉取业务代码。"
        "在 ECS 上依次执行：sudo dnf install -y python3.11 python3.11-pip git nginx certbot python3-certbot-nginx firewalld；"
        "sudo systemctl enable --now firewalld；"
        "sudo firewall-cmd --permanent --add-service=ssh --add-service=http --add-service=https；"
        "sudo firewall-cmd --reload。"
        "上述命令安装 Python 3.11 解释器、Git、Nginx、Certbot 及防火墙管理工具，"
        "并确保主机级防火墙与云安全组策略一致，避免「安全组已放行但本机 firewalld 仍拦截」的情况。"))
    b.append(("body",
        "代码部署：sudo git clone https://gitee.com/zhk567/atelier.git /opt/atelier；"
        "cd /opt/atelier；python3.11 -m venv .venv；source .venv/bin/activate；"
        "pip install -U pip；pip install -r requirements.txt。"
        "仓库体积包含 Wiki、Blog 大量 Markdown 与 static 媒体，首次 clone 可能耗时数分钟。"
        "注意：Alibaba Cloud Linux 默认 python3 可能指向 3.6，若用其创建 venv 将导致 FastAPI 依赖解析失败，"
        "必须使用 python3.11 -m venv 显式指定解释器版本。"))
    b.append(("figures", 5, [4, 5]))

    b.append(("h2", "5.3 systemd 与 Nginx"))
    b.append(("body",
        "目的：保证 FastAPI 进程常驻且非 root 运行；Nginx 作为公网唯一入口处理 TLS 与限流。"
        "创建系统用户：sudo useradd -r -s /sbin/nologin -d /opt/atelier atelier；"
        "sudo chown -R atelier:atelier /opt/atelier。"
        "复制 deploy/systemd/atelier.service.example 为 /etc/systemd/system/atelier.service，"
        "确认 Environment=ATELIER_ENV=production，ExecStart 指向 .venv/bin/uvicorn main:app。"
        "执行 sudo systemctl daemon-reload && sudo systemctl enable --now atelier，"
        "systemctl status atelier 应显示 active (running)。"))
    b.append(("body",
        "Nginx 配置分两步：其一，将 deploy/nginx/nginx-http-snippet.conf 中 limit_req_zone、"
        "limit_conn_zone 合并进 /etc/nginx/nginx.conf 的 http 块；"
        "其二，复制 deploy/nginx/atelier.conf.example 为 /etc/nginx/conf.d/atelier.conf，"
        "修改 server_name 为 zhkun.xyz www.zhkun.xyz，upstream 指向 127.0.0.1:8000。"
        "sudo nginx -t 语法检查通过后 systemctl enable --now nginx。"
        "此时 HTTP 80 端口应能反代至 FastAPI，但尚未启用 HTTPS，下一步由 Certbot 完成。"))
    b.append(("figures", 5, [6, 7]))

    b.append(("h2", "5.4 HTTPS"))
    b.append(("body",
        "目的：为公网用户提供加密传输，消除浏览器「不安全」提示，并满足现代 HTTPS 最佳实践。"
        "在 Nginx 已能正确反代 HTTP 80 的前提下，执行："
        "sudo certbot --nginx -d zhkun.xyz -d www.zhkun.xyz。"
        "Certbot 会验证域名解析是否指向本机、80 端口是否可从 Let's Encrypt 服务器访问，"
        "验证通过后自动修改 /etc/nginx/conf.d/atelier.conf，插入 ssl_certificate 指令，"
        "并配置 HTTP 至 HTTPS 的 301 跳转。"))
    b.append(("body",
        "注意事项：证书签发前必须确保 DNS A 记录已生效，且安全组与 firewalld 均已放行 80 端口；"
        "若先前手动编写过冲突的 SSL 配置，应先 nginx -t 修复语法错误再运行 certbot。"
        "签发成功后可用 openssl s_client -connect zhkun.xyz:443 -servername zhkun.xyz 查看证书链。"
        "系统通常已安装 certbot 定时任务，到期前自动 renew；"
        "维护人员可执行 certbot renew --dry-run 验证续期流程，避免证书过期导致全站不可用。"))
    b.append(("figures", 5, [8]))

    b.append(("h2", "5.5 功能与安全测试"))
    b.append(("body",
        "部署完成后需从本机与公网两个视角验证。本机：curl -I http://127.0.0.1:8000/ 期望 HTTP/1.1 200，"
        "证明 uvicorn 监听正常且未被防火墙阻断 loopback。"
        "公网：浏览器访问 https://zhkun.xyz，应看到首页四条置顶项目、博客入口与个人概览（图5-11）；"
        "访问 https://zhkun.xyz/blog/series/framework 应看到 Framework 指南分组列表（图5-12）。"
        "API：curl https://zhkun.xyz/api/site 返回 JSON 仅含 site_name、site_title，不含服务器绝对路径。"
        "安全：curl -I https://zhkun.xyz 响应头应含 X-Content-Type-Options、X-Frame-Options 等；"
        "curl -I https://zhkun.xyz/.env 应 404，表明探测路径拦截生效。"
        "Wiki：随机打开 /docs/Clothing-Classification/page-1 确认 Markdown 渲染与侧栏正常。"))
    b.append(("figures", 5, [9, 10, 11]))
    b.append(("table", "表5-1 部署测试结果", ["编号", "测试项", "方法", "结果"], [
        ["T1", "本机应用", "curl -I :8000", "通过"],
        ["T2", "HTTPS 首页", "浏览器", "通过"],
        ["T3", "Framework 博客", "/blog/series/framework", "通过"],
        ["T4", "Wiki 子路径", "/docs/NEXUS/page-1", "通过"],
        ["T5", "API 收敛", "curl /api/site", "通过"],
        ["T6", "安全头", "curl -I https", "通过"],
        ["T7", "探测拦截", "curl /.env", "404 通过"],
        ["T8", "browse 数据", "/browse/books", "通过"],
    ]))

    b.append(("h2", "5.6 常见问题排查"))
    b.append(("body",
        "（1）pip 安装失败：检查是否误用 python3.6 创建 venv，改用 python3.11 -m venv。"
        "（2）外网无法访问：检查安全组、firewalld 与 Nginx 是否 listen 80/443。"
        "（3）502 Bad Gateway：systemctl status atelier 确认 8000 端口进程 active。"
        "（4）证书失败：确认域名已解析至本机公网 IP 且 80 端口可从公网访问。"
        "日志：journalctl -u atelier -f；/var/log/nginx/error.log。"))
    b.append(("body",
        "（5）429 Too Many Requests：可能触发 Nginx 或 FastAPI 限流，检查是否短时间大量刷新或脚本压测，"
        "生产环境 RATE_LIMIT_DEFAULT 默认为 120/minute，正常浏览不应触发。"
        "（6）Wiki 404：确认 Wiki 目录存在且 slug 在白名单内，page 文件名与 URL 一致。"
        "排查时建议先本机 curl 8000 再查 Nginx，再查 DNS 与证书，自内向外逐层定位。"))
    b.append(("table", "表5-2 常见问题与处理", ["现象", "可能原因", "处理步骤"], [
        ["pip 依赖失败", "venv 基于 Python 3.6", "删除 .venv，python3.11 -m venv 重建"],
        ["外网超时", "安全组或 firewalld", "检查 80/443 放行与 firewall-cmd"],
        ["502 Bad Gateway", "uvicorn 未运行", "systemctl status/restart atelier"],
        ["证书申请失败", "DNS 未生效", "dig 域名，等待解析后再 certbot"],
        ["429 限流", "短时间大量请求", "降低刷新频率，检查 RATE_LIMIT"],
        ["Wiki 404", "slug 或 page 不存在", "核对 Wiki 目录与白名单"],
    ]))

    b.append(("code",
        "sudo dnf install -y python3.11 python3.11-pip git nginx certbot python3-certbot-nginx firewalld\n"
        "sudo git clone https://gitee.com/zhk567/atelier.git /opt/atelier\n"
        "cd /opt/atelier && python3.11 -m venv .venv && source .venv/bin/activate\n"
        "pip install -r requirements.txt\n"
        "sudo systemctl enable --now atelier\n"
        "sudo certbot --nginx -d zhkun.xyz -d www.zhkun.xyz"))

    # ========== 第6章 ==========
    b.append(("h1", "第6章 使用与维护说明"))
    b.append(("h2", "6.1 本地开发"))
    b.append(("body",
        "Windows：复制 config/site.example.json 为 site.local.json，执行 run.ps1，"
        "访问 http://127.0.0.1:8000。本地 ATELIER_ENV=development，不限流，便于调试模板与 Markdown。"))
    b.append(("h2", "6.2 线上更新"))
    b.append(("body",
        "推送 Gitee 后 SSH 至 ECS：cd /opt/atelier && git pull && source .venv/bin/activate && "
        "pip install -r requirements.txt && sudo systemctl restart atelier。"
        "仅改 Nginx：nginx -t && systemctl reload nginx。"))
    b.append(("h2", "6.3 内容维护"))
    b.append(("body",
        "博客：Blog/ 下维护 md，运行 validate_guide.py 校验。"
        "Wiki：更新 Wiki/ 导出。项目：config/projects.json。"
        "个人数据：zhita_settings.xlsx。壁纸：data/wallpapers.json 与 mp4 文件。"))
    b.append(("body",
        "以新增 Framework 指南为例：在 Framework 源码仓编写 stack 文档 → 运行扫描脚本更新 manifest →"
        "在 atelier 的 Blog/framework-guides 下同步 index.md → 本地 run.ps1 预览 /blog/series/framework →"
        "确认分组与 slug 正确后 push → ECS git pull 并 restart。"
        "Wiki 更新通常来自 DeepWiki 或手工 Markdown 导出，需保证 wiki_slug 与 projects.json 中字段一致，"
        "否则项目详情页的 Wiki 分页链接会出现 404。"))
    b.append(("h2", "6.4 日志与监控"))
    b.append(("body",
        "生产环境应用日志通过 journalctl -u atelier 查看，Nginx 访问与错误日志位于 /var/log/nginx/。"
        "出现 502 时优先检查 atelier 服务是否 active；出现 429 时检查是否触发限流。"
        "证书续期可执行 certbot renew --dry-run 验证定时任务。"
        "内容更新后若页面未变化，确认 git pull 成功且已 systemctl restart atelier，"
        "必要时清除浏览器缓存或使用无痕窗口验证。"))
    b.append(("h2", "6.5 与课程大作业的对应关系"))
    b.append(("body",
        "本站点满足开发类选题二「在云平台部署可公网访问网站」："
        "设计体现在第2章需求与架构；实现体现在第4章 FastAPI 模块；"
        "部署与截图体现在第5章；使用说明体现在本章。"
        "报告中的图5-1 至图5-12 对应从云资源创建到浏览器访问的全过程，"
        "其中图5-11、5-12 已为公网真实页面，图5-1 至5-10 建议在提交前替换为本人阿里云控制台与 SSH 终端截图。"))

    # ========== 第7章 ==========
    b.append(("h1", "第7章 总结与展望"))
    b.append(("body",
        "本文完成了 atelier 个人知识站的需求分析、网站各页面功能详述（含七个项目分节）、"
        "FastAPI 实现说明、阿里云 ECS 部署测试与使用维护文档。"
        "站点已公网稳定提供项目、Wiki、博客与个人数据浏览，满足《云计算技术》课程开发类大作业要求。"
        "图5-1 至图5-10 建议替换为本人阿里云控制台与 ECS 终端操作截图；"
        "后续可开展华为云对照部署、Docker 化与 CI 自动发布。"))
    b.append(("body",
        "通过本次大作业，完整实践了从 IaaS 资源申请到 HTTPS 站点上线的工程链路，"
        "并认识到只读静态内容站点在运维上的优势：无数据库迁移、无会话状态、"
        "故障排查可沿 Nginx → systemd → 应用日志逐层定位。"
        "这些经验可直接迁移至后续课程设计或实习中的 Web 服务项目部署。"))

    # ========== 附录 ==========
    b.append(("h1", "附录A  部署检查清单"))
    b.append(("body", "以下为生产环境首次部署与验收对照项，可按顺序勾选。"))
    b.append(("body", "云资源：ECS 已创建（建议 1 核 2G+）；公网 IP 已绑定；安全组 22/80/443 已放行；域名 A 记录已指向 ECS。"))
    b.append(("body", "系统软件：python3.11、git、nginx、certbot、firewalld 已安装；firewall 已放行 ssh/http/https。"))
    b.append(("body", "应用代码：仓库已 clone 至 /opt/atelier；venv 已创建；pip install -r requirements.txt 成功；使用 Python 3.9+。"))
    b.append(("body", "进程管理：atelier 系统用户已创建；systemd 单元已 enable；systemctl status 为 active；ATELIER_ENV=production。"))
    b.append(("body", "Nginx：http 片段已合并；站点 conf 已部署；nginx -t 通过；Nginx 已 enable。"))
    b.append(("body", "HTTPS：certbot 已执行；浏览器可 https 访问且证书有效。"))
    b.append(("body", "验证：curl 127.0.0.1:8000 为 200；首页/Wiki/博客浏览器正常；/api/site 无路径泄露；/.env 为 404；安全响应头存在。"))
    b.append(("body", "日常更新：git pull → pip install → systemctl restart atelier。"))
    b.append(("body",
        "权限最小化：atelier 系统用户对 /opt/atelier 仅有读写执行权，"
        "不加入 wheel 组；SSH 登录使用普通用户 + sudo，禁止 root 直接登录。"
        "密钥管理：ECS 绑定 SSH 公钥，关闭密码登录（若云厂商支持）。"
        "备份：除 Git 远程仓库外，可对 /etc/nginx/conf.d 与 systemd 单元做快照备份，"
        "以便重建实例时快速恢复反代配置。"))
    b.append(("body",
        "验收标准对照：本机 8000 端口 200；HTTPS 首页与 Wiki/博客可打开；"
        "/api/site 不泄露路径；/.env 404；安全响应头存在。"
        "以上与第5章表5-1 测试项一致，可在答辩前逐项勾选。"))
    b.append(("body",
        "可选增强：配置 deploy/fail2ban 示例对大量 404/429 的 IP 临时封禁；"
        "接入 Cloudflare 隐藏源站 IP；使用 Docker 封装 uvicorn 环境以简化迁移。"
        "这些超出课程基本要求，可作为个人运维能力提升方向。"))
    b.append(("body",
        "回滚策略：若 git pull 后站点异常，可执行 git log 查看最近提交，"
        "git checkout 上一稳定版本后 systemctl restart atelier 快速恢复。"
        "Nginx 配置变更前建议 cp atelier.conf atelier.conf.bak，"
        "nginx -t 失败时用备份文件还原再 reload。"
        "磁盘空间：Wiki 与 Blog 体量较大，应定期 df -h 检查 /opt 分区，"
        "必要时清理 journal 日志或扩容云盘，避免 pip 安装或 git 操作因磁盘满而失败。"))
    b.append(("body",
        "答辩前自检顺序建议：本机 curl 8000 → 本机 curl HTTPS → 手机蜂窝网络打开首页 →"
        "随机点开三个 Wiki 分页与一个 browse 表格 → 确认图5-1 至5-10 已替换为本人操作截图。"
        "该顺序与附录勾选项、第5章表5-1 测试矩阵一一对应，"
        "可在十分钟内完成部署正确性与内容完整性的双重确认。"))

    b.append(("h1", "参考文献"))
    for ref in REFS:
        b.append(("body", ref))

    return b


def char_count() -> int:
    total = 0
    for block in get_blocks():
        if block[0] in ("body", "h1", "h2", "h3", "code"):
            total += len(block[1])
        elif block[0] == "table":
            total += len(block[1])
            for row in block[3]:
                total += sum(len(c) for c in row)
    return total


if __name__ == "__main__":
    print("blocks", len(get_blocks()), "chars", char_count())
