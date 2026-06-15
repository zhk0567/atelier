#!/usr/bin/env python3
"""Generate architecture diagram PNGs for homework report (ch1/ch2/ch4/ch6 + ch3 placeholders)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHOTS = ROOT / "作业" / "screenshots"


def _setup_matplotlib():
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    candidates = ["Microsoft YaHei", "SimHei", "SimSun", "STSong"]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name]
            break
    plt.rcParams["axes.unicode_minus"] = False
    return plt


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    import matplotlib.pyplot as plt

    plt.close(fig)
    print("wrote", path)


def fig1_1_cloud_models(plt) -> None:
    from matplotlib.patches import FancyBboxPatch

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    layers = [
        ("SaaS", "开箱即用软件", "Office 365、钉钉", 3.8),
        ("PaaS", "托管运行时", "Railway、App Engine", 2.5),
        ("IaaS", "虚拟机与网络", "阿里云 ECS、华为云 ECS", 1.2),
    ]
    for title, scope, example, y in layers:
        box = FancyBboxPatch((0.8, y), 8.4, 0.9, boxstyle="round,pad=0.04", fc="#E8F4FC", ec="#2E86AB", lw=1.5)
        ax.add_patch(box)
        ax.text(1.2, y + 0.45, title, fontsize=13, fontweight="bold", va="center")
        ax.text(2.8, y + 0.45, f"用户管理：{scope}", fontsize=11, va="center")
        ax.text(6.8, y + 0.45, f"例：{example}", fontsize=10, va="center")
    ax.text(5, 4.6, "云计算服务模型对比（atelier 选用 IaaS）", ha="center", fontsize=14, fontweight="bold")
    _save(fig, SHOTS / "ch1" / "01-服务模型.png")


def fig1_2_motivation(plt) -> None:
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.axis("off")
    steps = [
        "多仓库分散\nGitHub/Gitee/Wiki",
        "统一门户\natelier / zhkun.xyz",
        "课程选题二\n云平台部署网站",
    ]
    xs = [1.5, 5.0, 8.5]
    for x, text in zip(xs, steps):
        ax.add_patch(plt.Rectangle((x - 1.1, 1.0), 2.2, 1.4, fc="#FFF3E0", ec="#E65100", lw=1.5))
        ax.text(x, 1.7, text, ha="center", va="center", fontsize=11)
    ax.annotate("", xy=(3.4, 1.7), xytext=(2.6, 1.7), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate("", xy=(7.4, 1.7), xytext=(6.6, 1.7), arrowprops=dict(arrowstyle="->", lw=2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.5)
    ax.text(5, 2.9, "个人站点建设动机与课程对应关系", ha="center", fontsize=14, fontweight="bold")
    _save(fig, SHOTS / "ch1" / "02-建设动机.png")


def fig2_1_architecture(plt) -> None:
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.axis("off")
    boxes = [
        (0.5, 2.8, "公网用户"),
        (2.3, 2.8, "DNS\nzhkun.xyz"),
        (4.1, 2.8, "Nginx\n443/80 TLS"),
        (6.0, 2.8, "uvicorn\nFastAPI :8000"),
        (8.0, 2.8, "内容文件\nmd/xlsx/json/static"),
    ]
    for x, y, t in boxes:
        ax.add_patch(plt.Rectangle((x, y), 1.5, 0.9, fc="#E3F2FD", ec="#1565C0", lw=1.5))
        ax.text(x + 0.75, y + 0.45, t, ha="center", va="center", fontsize=10)
    for x1, x2 in [(2.0, 2.3), (3.8, 4.1), (5.6, 6.0), (7.5, 8.0)]:
        ax.annotate("", xy=(x2, 3.25), xytext=(x1, 3.25), arrowprops=dict(arrowstyle="->", lw=1.8))
    ax.text(5, 4.2, "atelier 总体部署架构", ha="center", fontsize=14, fontweight="bold")
    ax.text(5, 0.6, "Certbot 维护 Let's Encrypt 证书自动续期", ha="center", fontsize=10, color="#555")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.8)
    _save(fig, SHOTS / "ch2" / "01-总体架构.png")


def fig2_2_request_lifecycle(plt) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis("off")
    steps = [
        "浏览器发起 HTTPS",
        "Nginx 解密 TLS 并限流",
        "反代至 FastAPI",
        "路由读取磁盘数据",
        "Markdown/Jinja2 渲染",
        "HTML 经 Nginx 返回",
    ]
    y = 4.2
    for i, s in enumerate(steps):
        ax.add_patch(plt.Rectangle((1.5, y - 0.35), 7.0, 0.55, fc="#F1F8E9", ec="#558B2F", lw=1.2))
        ax.text(1.8, y - 0.08, f"{i + 1}. {s}", fontsize=11, va="center")
        if i < len(steps) - 1:
            ax.annotate("", xy=(5, y - 0.45), xytext=(5, y - 0.75), arrowprops=dict(arrowstyle="->", lw=1.5))
        y -= 0.75
    ax.text(5, 4.85, "单次 HTTPS 请求生命周期", ha="center", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    _save(fig, SHOTS / "ch2" / "02-请求生命周期.png")


def fig4_1_modules(plt) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis("off")
    modules = [
        ("home.py", "/"),
        ("projects.py", "/projects"),
        ("blog.py", "/blog"),
        ("wiki.py", "/docs"),
        ("browse.py", "/browse"),
        ("travel.py", "/travel"),
        ("assets.py", "/wallpaper"),
    ]
    ax.add_patch(plt.Rectangle((3.5, 4.0), 3.0, 0.7, fc="#FFE0B2", ec="#EF6C00", lw=1.5))
    ax.text(5, 4.35, "create_app() / main.py", ha="center", va="center", fontsize=12, fontweight="bold")
    cols = [1.0, 3.2, 5.4, 7.6]
    for i, (name, path) in enumerate(modules):
        x = cols[i % 4]
        y = 2.8 - (i // 4) * 1.5
        ax.add_patch(plt.Rectangle((x, y), 1.8, 0.9, fc="#E8EAF6", ec="#3949AB", lw=1.2))
        ax.text(x + 0.9, y + 0.55, name, ha="center", fontsize=9, fontweight="bold")
        ax.text(x + 0.9, y + 0.25, path, ha="center", fontsize=8)
        ax.annotate("", xy=(x + 0.9, y + 0.9), xytext=(5, 4.0), arrowprops=dict(arrowstyle="->", lw=0.8, color="#888"))
    ax.text(5, 0.4, "FastAPI 路由模块划分", ha="center", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    _save(fig, SHOTS / "ch4" / "01-模块划分.png")


def fig4_2_dataflow(plt) -> None:
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.axis("off")
    parts = ["磁盘文件\nmd/xlsx/json", "site_data.py\n解析聚合", "routes\n业务路由", "Jinja2\n模板", "HTML\n响应"]
    xs = [0.6, 2.5, 4.6, 6.6, 8.5]
    for x, t in zip(xs, parts):
        ax.add_patch(plt.Rectangle((x, 1.2), 1.6, 1.0, fc="#FFFDE7", ec="#F9A825", lw=1.3))
        ax.text(x + 0.8, 1.7, t, ha="center", va="center", fontsize=10)
    for i in range(len(xs) - 1):
        ax.annotate("", xy=(xs[i + 1], 1.7), xytext=(xs[i] + 1.6, 1.7), arrowprops=dict(arrowstyle="->", lw=2))
    ax.text(5, 3.0, "数据流：文件 → 渲染 → HTML", ha="center", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.5)
    _save(fig, SHOTS / "ch4" / "02-数据流.png")


def fig4_3_security(plt) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis("off")
    layers = [
        "Nginx limit_req / limit_conn",
        "TrustedHost 中间件",
        "slowapi IP 限流",
        "探测路径拦截 /.env",
        "Wiki slug / 路径校验",
    ]
    y = 4.0
    colors = ["#FFEBEE", "#FCE4EC", "#F3E5F5", "#E8EAF6", "#E0F2F1"]
    for i, (layer, c) in enumerate(zip(layers, colors)):
        ax.add_patch(plt.Rectangle((2.0, y), 6.0, 0.55, fc=c, ec="#555", lw=1.2))
        ax.text(5, y + 0.28, f"第{i + 1}层  {layer}", ha="center", va="center", fontsize=11)
        if i < len(layers) - 1:
            ax.annotate("", xy=(5, y), xytext=(5, y - 0.15), arrowprops=dict(arrowstyle="->", lw=1.5))
        y -= 0.7
    ax.text(5, 4.7, "安全分层防御模型", ha="center", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    _save(fig, SHOTS / "ch4" / "03-安全分层.png")


def fig6_1_maintenance(plt) -> None:
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.axis("off")
    steps = ["本地编辑\nBlog/Wiki/xlsx", "git push\nGitee", "SSH\ngit pull", "pip install\n依赖", "systemctl\nrestart"]
    xs = [0.8, 2.8, 4.8, 6.8, 8.8]
    for x, t in zip(xs, steps):
        ax.add_patch(plt.Rectangle((x, 1.0), 1.6, 1.2, fc="#E0F7FA", ec="#00838F", lw=1.3))
        ax.text(x + 0.8, 1.6, t, ha="center", va="center", fontsize=9)
    for i in range(len(xs) - 1):
        ax.annotate("", xy=(xs[i + 1], 1.6), xytext=(xs[i] + 1.6, 1.6), arrowprops=dict(arrowstyle="->", lw=1.8))
    ax.text(5, 2.9, "线上内容更新与发布流程", ha="center", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.5)
    _save(fig, SHOTS / "ch6" / "01-维护流程.png")


def ch3_placeholders(plt) -> None:
    items = [
        ("01-全站导航.png", "图3-1  请替换为 zhkun.xyz 顶栏与侧栏截图"),
        ("02-首页.png", "图3-2  请替换为首页置顶项目截图"),
        ("03-项目详情.png", "图3-3  请替换为 /project 或 /projects 截图"),
        ("04-博客系列.png", "图3-4  请替换为 /blog/series/framework 截图"),
        ("05-Wiki分页.png", "图3-5  请替换为 /docs/NEXUS/page-6 截图"),
        ("06-browse.png", "图3-6  请替换为 /browse/anime 截图"),
        ("07-旅行相册.png", "图3-7  请替换为 /travel 截图"),
        ("08-壁纸Live2D.png", "图3-8  请替换为壁纸或 Live2D 截图"),
    ]
    out_dir = SHOTS / "ch3"
    out_dir.mkdir(parents=True, exist_ok=True)
    for fname, label in items:
        path = out_dir / fname
        if path.is_file():
            print("skip existing", path)
            continue
        fig, ax = plt.subplots(figsize=(10, 5.5))
        ax.set_facecolor("#F5F5F5")
        ax.text(0.5, 0.5, label + "\n\nscreenshots/ch3/" + fname, ha="center", va="center", fontsize=14, color="#666")
        ax.axis("off")
        _save(fig, path)


def main() -> None:
    plt = _setup_matplotlib()
    fig1_1_cloud_models(plt)
    fig1_2_motivation(plt)
    fig2_1_architecture(plt)
    fig2_2_request_lifecycle(plt)
    fig4_1_modules(plt)
    fig4_2_dataflow(plt)
    fig4_3_security(plt)
    fig6_1_maintenance(plt)
    ch3_placeholders(plt)
    print("done:", SHOTS)


if __name__ == "__main__":
    main()
