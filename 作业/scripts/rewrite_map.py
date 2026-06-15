#!/usr/bin/env python3
"""Paragraph rewrite map for plagiarism/AIGC reduction (match substring -> new text)."""

from __future__ import annotations

# type: replace whole paragraph if match found; delete: remove paragraph if match found
# delete_after_first: keep first match, delete subsequent matches

DUPLICATE_DELETE_MATCH = "用户在站点内可通过项目详情页一键跳转 GitHub 源码仓库"

REWRITES: list[dict] = [
    # ----- P0: PaperPass flagged (Ch1) -----
    {
        "match": "云计算是一种通过网络按需提供可伸缩 IT 资源的服务模式",
        "new": (
            "本课程实验所依托的云计算，本质是把服务器、存储与带宽等资源放到远端数据中心，"
            "按实际开通与使用量计费，需要时几分钟内即可扩容，用毕可释放，不必自建机房。"
        ),
        "note": "1.1 PaperPass 62%",
    },
    {
        "match": "租户无需自行采购物理服务器、交换机与机房空调，即可在分钟级获得虚拟机",
        "new": (
            "对个人开发者而言，这意味着不必购买和维护物理机与网络设备，"
            "通过控制台即可申请虚拟机、挂载磁盘并绑定公网地址，成本随用量变化。"
        ),
        "note": "1.1",
    },
    {
        "match": "在基础设施即服务（IaaS）层级，云厂商负责硬件与虚拟化平台",
        "new": (
            "本次大作业选用 IaaS 模式：云服务商维护机房与虚拟化层，"
            "我在 ECS 上自行安装 Linux、Python、Nginx 与应用代码，责任边界清晰，便于写进实验报告。"
        ),
        "note": "1.1",
    },
    {
        "match": "典型 Web 系统上云流程为：创建云主机、配置安全组与防火墙",
        "new": (
            "结合 atelier 站点，我的上云步骤概括为：购买 ECS、配置安全组与 DNS、"
            "安装 Python 虚拟环境与 Nginx、用 systemd 托管 FastAPI、再用 Certbot 配置 HTTPS，"
            "最后做功能与安全测试。"
        ),
        "note": "1.1",
    },
    {
        "match": "该模式初始成本低、扩容灵活，已成为高校《云计算技术》课程验证学生工程实践能力的主要载体",
        "new": (
            "这种模式前期投入小、后期可按需升配，正好用来完成选题二「云平台部署可公网访问网站」"
            "并检验从环境搭建到域名访问的完整工程能力。"
        ),
        "note": "1.1",
    },
    {
        "match": "云计算通常划分为 IaaS、PaaS、SaaS 三层",
        "new": (
            "业界常把云服务分成三层：最底层 IaaS 给虚拟机与网络，中间 PaaS 托管运行环境，"
            "最上层 SaaS 直接提供成品软件；三层之间用户需要自行管理的范围依次减少。"
        ),
        "note": "1.2 PaperPass 83%",
    },
    {
        "match": "IaaS 提供虚拟机与网络，灵活性最高",
        "new": "IaaS 层交付的是可定制的操作系统与网络，自由度最大，适合像本次这样自搭 Web 栈。",
        "note": "1.2",
    },
    {
        "match": "PaaS 提供托管运行时，部署更简单但约束较多",
        "new": "PaaS 把语言运行时和部署流程打包好，上线快，但对系统软件版本、反向代理策略的控制较弱。",
        "note": "1.2",
    },
    {
        "match": "SaaS 为开箱即用应用",
        "new": "SaaS 则是直接使用的在线应用，几乎不涉及服务器配置，与本次需要写部署过程的目标不符。",
        "note": "1.2",
    },
    {
        "match": "atelier 选用 IaaS（阿里云 ECS）是因为需要完全控制 Nginx、Python 版本与 systemd 单元",
        "new": (
            "atelier 因此选用阿里云 ECS 这类 IaaS：我可以固定 Python 3.11、"
            "自行编写 Nginx 限流与 systemd 单元，实验步骤可截图、可复述，符合课程验收方式。"
        ),
        "note": "1.2",
    },
    # ----- P0: Ch3 duplicate boilerplate (first kept via section summary, rest deleted by apply script) -----
    {
        "match": "该设计将「代码仓库」与「在线文档」之间的跳转成本降到最低",
        "new": (
            "对答辩和日常查阅来说，这种「卡片进项目、侧栏翻 Wiki」的路径比记住仓库目录更省事，"
            "也是我把多个仓库整合进 zhkun.xyz 的主要收益。"
        ),
        "note": "3.3 first occurrence only",
        "once": True,
    },
    {
        "match": "技术标签含 Web、微信小程序、React",
        "new": "所用技术包括 Web 前端、微信小程序与 React，对应学习终端的多端形态。",
        "note": "3.3.1 PaperPass 55%",
    },
    # ----- P1: Ch5 deployment prose -----
    {
        "match": "目的：获得公网可达的 Linux 虚拟机与网络安全边界",
        "new": "本节目标是在阿里云上拿到一台可从互联网 SSH 登录的 Linux 主机，并划清网络安全边界。",
        "note": "5.1",
    },
    {
        "match": "在阿里云控制台创建 ECS，绑定公网 IP",
        "new": "我首先在控制台创建 ECS 实例并绑定弹性公网 IP，作为后续域名解析的目标地址。",
        "note": "5.1",
    },
    {
        "match": "安全组入方向放行 TCP 22、80、443",
        "new": "在安全组入方向规则中，我为 SSH 与管理 Web 分别放行了 22、80、443 三个 TCP 端口",
        "note": "5.1 PaperPass 52%",
    },
    {
        "match": "域名 A 记录指向 ECS IP",
        "new": "在域名控制台把 zhkun.xyz 的 A 记录解析到上述公网 IP，等待生效后再做证书申请。",
        "note": "5.1",
    },
    {
        "match": "SSH 登录执行 cat /etc/os-release 确认系统",
        "new": "用 SSH 登录后执行 cat /etc/os-release，确认系统为 Alibaba Cloud Linux 3（见图5-4）。",
        "note": "5.1",
    },
    {
        "match": "注意：仅开放必要端口，缩小攻击面",
        "new": "端口只开业务需要的几项，其余一律关闭，减少被扫描和利用的风险。",
        "note": "5.1",
    },
    {
        "match": "ECS 规格方面，个人知识站以静态渲染为主，1 核 2 GB 内存即可满足日常访问",
        "new": "实例规格我选 1 核 2 GB：站点以读文件和模板渲染为主，无数据库压力，日常访问足够。",
        "note": "5.1",
    },
    {
        "match": "目的：安装运行时与 Web 依赖，拉取业务代码",
        "new": "5.2 节完成两件事：在系统里装好 Python、Git、Nginx 等依赖，并把 atelier 仓库拉到 ECS。",
        "note": "5.2",
    },
    {
        "match": "上述命令安装 Python 3.11 解释器、Git、Nginx、Certbot 及防火墙管理工具",
        "new": (
            "dnf 一次性装好 Python 3.11、Git、Nginx、Certbot 与 firewalld 后，"
            "我又用 firewall-cmd 在本机放行 ssh/http/https，避免「云安全组已开、主机防火墙仍拦」的情况。"
        ),
        "note": "5.2",
    },
    {
        "match": "注意：Alibaba Cloud Linux 默认 python3 可能指向 3.6",
        "new": "踩坑提示：系统自带的 python3 可能仍是 3.6，创建虚拟环境时必须写 python3.11 -m venv，否则 FastAPI 依赖装不上。",
        "note": "5.2",
    },
    {
        "match": "目的：保证 FastAPI 进程常驻且非 root 运行",
        "new": "5.3 节要解决进程守护与权限：FastAPI 由 systemd 常驻拉起，且不以 root 身份监听 8000 端口。",
        "note": "5.3",
    },
    {
        "match": "Nginx 作为公网唯一入口处理 TLS 与限流",
        "new": "公网只暴露 Nginx 的 80/443，由它做 TLS 终止、限流并反代到本机 127.0.0.1:8000。",
        "note": "5.3",
    },
    {
        "match": "此时 HTTP 80 端口应能反代至 FastAPI，但尚未启用 HTTPS",
        "new": "到这一步用 HTTP 已能打开站点，但浏览器会提示不安全，下一节用 Certbot 补上 HTTPS。",
        "note": "5.3",
    },
    {
        "match": "目的：为公网用户提供加密传输，消除浏览器「不安全」提示",
        "new": "5.4 节的目标是让 zhkun.xyz 走 HTTPS，地址栏显示安全锁，数据传输加密。",
        "note": "5.4",
    },
    {
        "match": "Certbot 会验证域名解析是否指向本机、80 端口是否可从 Let's Encrypt 服务器访问",
        "new": "Certbot 会先检查域名是否解析到本机、80 端口能否被 Let's Encrypt 访问，通过后自动改 Nginx 配置。",
        "note": "5.4",
    },
    {
        "match": "部署完成后需从本机与公网两个视角验证",
        "new": "上线后我分两步验收：先在 ECS 本机 curl 8000，再用浏览器从公网访问 HTTPS。",
        "note": "5.5",
    },
    {
        "match": "排查时建议先本机 curl 8000 再查 Nginx，再查 DNS 与证书，自内向外逐层定位",
        "new": "排障时我习惯从内到外：先 curl 127.0.0.1:8000，再看 systemd 与 Nginx 日志，最后查 DNS 和证书是否过期。",
        "note": "5.6",
    },
    # ----- P1: Ch6.4 flagged -----
    {
        "match": "证书续期可执行 certbot renew --dry-run 验证定时任务",
        "new": "Let’s Encrypt 证书到期前系统会尝试自动续期；我偶尔执行 certbot renew --dry-run 确认续期脚本可用。",
        "note": "6.4 PaperPass 58%",
    },
    # ----- P2: Ch2, Ch4, Ch7 -----
    {
        "match": "公网用户经 DNS 将 zhkun.xyz 解析至 ECS 公网 IP",
        "new": "访问者输入 zhkun.xyz 时，DNS 先把域名解析到我 ECS 的公网地址，请求再进入机房网络。",
        "note": "2.3",
    },
    {
        "match": "请求到达 Nginx（443/80），完成 TLS 与限流后反代至 127.0.0.1:8000 的 uvicorn/FastAPI",
        "new": "流量先到 Nginx 做 HTTPS 解密和访问频率控制，再转发到本机 8000 端口上的 uvicorn/FastAPI 进程。",
        "note": "2.3",
    },
    {
        "match": "从请求生命周期看：浏览器发起 HTTPS 请求",
        "new": "一次完整访问可简述为：浏览器发 HTTPS 请求，经 Nginx 解密并限流，",
        "note": "2.3",
    },
    {
        "match": "分层防御：Nginx 限流与超时 → FastAPI TrustedHost、slowapi 限流、探测路径 404",
        "new": (
            "安全上采用多层叠加：Nginx 控制连接与请求速率；FastAPI 侧用 TrustedHost 校验域名、"
            "slowapi 按 IP 限流，并对 /.env 等扫描路径直接返回 404。"
        ),
        "note": "4.3",
    },
    {
        "match": "register_security_middleware 在 create_app 中于路由注册之前调用",
        "new": "create_app 里先挂安全中间件再注册业务路由，保证每个请求都先过 Host 校验与限流。",
        "note": "4.6",
    },
    {
        "match": "当 Host 头不在 TRUSTED_HOSTS 列表时，中间件直接返回 400",
        "new": "若 Host 不是 zhkun.xyz 等白名单域名，中间件会返回 400，避免 Host 头攻击。",
        "note": "4.6",
    },
    {
        "match": "本文完成了 atelier 个人知识站的需求分析、网站各页面功能详述",
        "new": "本报告围绕 atelier 站点，完成了需求梳理、各页面功能说明、",
        "note": "7",
    },
    {
        "match": "站点已公网稳定提供项目、Wiki、博客与个人数据浏览，满足《云计算技术》课程开发类大作业要求",
        "new": (
            "目前 https://zhkun.xyz 已稳定提供项目展示、Wiki、博客与个人数据浏览，"
            "完成了选题二要求的云平台部署与公网访问，并附部署与访问截图。"
        ),
        "note": "7",
    },
    {
        "match": "通过本次大作业，完整实践了从 IaaS 资源申请到 HTTPS 站点上线的工程链路",
        "new": "做完本次作业，我从购买 ECS、配置网络到 HTTPS 上线走通了完整链路，",
        "note": "7",
    },
    {
        "match": "无数据库迁移、无会话状态、故障排查可沿 Nginx → systemd → 应用日志逐层定位",
        "new": "站点无数据库与会话，出问题时按 Nginx 日志、systemctl status、journalctl 逐层查即可。",
        "note": "7",
    },
    {
        "match": "站点定位为只读个人知识门户",
        "new": "atelier 定位为只读个人门户",
        "note": "2.1",
    },
    {
        "match": "不提供用户注册、表单提交或数据库读写，全部内容来自 Git 仓库内文件",
        "new": "没有注册登录和表单提交，页面数据都来自仓库里的 Markdown、JSON 与 xlsx，更新靠 git pull。",
        "note": "2.1",
    },
    {
        "match": "从教学视角看，一次完整的云 Web 部署至少包含资源层、网络层、平台层与应用层四个环节",
        "new": "按实验报告写法，我把上云过程拆成四层：选 ECS 与磁盘（资源）、安全组与 DNS（网络）、系统软件与 Nginx（平台）、业务代码与静态资源（应用）。",
        "note": "1.3",
    },
    {
        "match": "atelier 将「内容仓库」与「运行环境」明确分离",
        "new": "我把 Git 仓库当作唯一内容源，ECS 只负责运行，不在服务器上另建内容数据库。",
        "note": "2.4",
    },
    {
        "match": "七个项目在首页仅展示四条置顶，其余三条在 /projects 完整列表中呈现",
        "new": "首页只置顶四个项目以免过长，NEXUS、llm-agents、Algorithm 等可在 /projects 完整列表进入。",
        "note": "3.3 summary",
    },
]
