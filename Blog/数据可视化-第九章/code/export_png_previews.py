"""为博文生成静态 PNG 预览（与教材图一致的数据，Matplotlib 绘制）。"""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np

from _paths import PNG_DIR, ensure_dirs
from fig_9_10_grid import PHONES, SALES_A, SALES_B

CLOTHES = ["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"]
SALES_CLOTHES_A = [5, 20, 36, 10, 75, 90, 50]


def _setup_cn():
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False


def _save(name: str) -> None:
    path = PNG_DIR / name
    plt.tight_layout()
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    print("wrote", path.name)


def fig_9_02_bar():
    _setup_cn()
    plt.figure(figsize=(7, 3.8))
    plt.bar(CLOTHES, SALES_CLOTHES_A, color="#4a6fa5")
    plt.title("柱形图示例")
    plt.ylabel("销售额(万元)")
    for i, v in enumerate(SALES_CLOTHES_A):
        plt.text(i, v + 1, str(v), ha="center", fontsize=9)
    _save("fig_9_02_bar.png")


def fig_9_03_line():
    _setup_cn()
    plt.figure(figsize=(7, 4))
    plt.plot(CLOTHES, [120, 132, 101, 134, 90, 230, 210][: len(CLOTHES)], marker="D", label="商家A")
    plt.plot(CLOTHES, [220, 182, 191, 234, 290, 330, 310][: len(CLOTHES)], marker="^", label="商家B")
    plt.title("折线图示例")
    plt.ylabel("销售额(万元)")
    plt.legend()
    _save("fig_9_03_line.png")


def fig_9_04_pie():
    _setup_cn()
    labels = ["小米", "华为", "OPPO", "vivo", "荣耀"]
    sizes = [150, 120, 95, 88, 70]
    plt.figure(figsize=(5.5, 5.5))
    plt.pie(sizes, labels=labels, autopct="%1.0f")
    plt.title("饼图示例")
    _save("fig_9_04_pie.png")


def fig_9_05_donut():
    _setup_cn()
    labels = ["小米", "华为", "OPPO", "vivo", "荣耀"]
    sizes = [150, 120, 95, 88, 70]
    plt.figure(figsize=(5.5, 5.5))
    plt.pie(sizes, labels=labels, autopct="%1.0f", wedgeprops=dict(width=0.45))
    plt.title("圆环图示例")
    _save("fig_9_05_donut.png")


def fig_9_06_scatter():
    _setup_cn()
    rng = np.random.default_rng(42)
    x = np.arange(1, 21)
    y = rng.integers(10, 41, size=20)
    plt.figure(figsize=(6, 4))
    plt.scatter(x, y, c="#c44e52")
    plt.title("散点图示例")
    plt.xlabel("X")
    plt.ylabel("Y")
    _save("fig_9_06_scatter.png")


def fig_9_16_roma():
    _setup_cn()
    x = np.arange(len(PHONES))
    w = 0.35
    plt.figure(figsize=(7.5, 4))
    plt.bar(x - w / 2, SALES_A, width=w, label="商家A", color="#5d4e37")
    plt.bar(x + w / 2, SALES_B, width=w, label="商家B", color="#8c7b5d")
    plt.xticks(x, PHONES, rotation=20)
    plt.title("柱形图-ROMA主题（示意）")
    plt.ylabel("销售额(万元)")
    plt.legend()
    _save("fig_9_16_theme_roma.png")


def hupu_bars():
    _setup_cn()
    sections = ["篮球", "足球", "汽车", "NBA", "影视", "数码", "步行街", "国际足球"]
    counts = [1280, 860, 540, 990, 430, 380, 720, 310]
    plt.figure(figsize=(8, 4))
    plt.bar(sections, counts, color="#e67e22")
    plt.title("虎扑各板块发帖量（示例）")
    plt.xticks(rotation=25)
    _save("hupu_section_bar.png")


def hupu_hourly():
    _setup_cn()
    hours = list(range(24))
    all_site = [42, 28, 18, 12, 10, 15, 38, 62, 88, 95, 102, 110, 118, 125, 130, 128, 135, 148, 156, 142, 120, 98, 72, 55]
    nba = [18, 12, 8, 6, 5, 7, 16, 28, 40, 44, 48, 52, 55, 58, 60, 58, 62, 68, 72, 65, 52, 42, 30, 22]
    plt.figure(figsize=(9, 4))
    plt.plot(hours, all_site, label="全站", marker="o", markersize=3)
    plt.plot(hours, nba, label="NBA", marker="s", markersize=3)
    plt.title("虎扑 24 小时发帖量（示例）")
    plt.xlabel("小时")
    plt.ylabel("帖子数")
    plt.legend()
    plt.grid(True, alpha=0.3)
    _save("hupu_hourly_line.png")


def ex05_frame():
    _setup_cn()
    x = np.linspace(0, 2 * math.pi, 200)
    y = np.sin(x)
    px = float(x[66])
    py = float(np.sin(px))
    plt.figure(figsize=(8, 4))
    plt.plot(x, y, color="steelblue")
    plt.plot(px, py, "ro", markersize=10)
    plt.text(0.72, 0.92, f"x={px:.3f}, y={py:.3f}", transform=plt.gca().transAxes)
    plt.title("正弦曲线动点（第五大题示意帧）")
    plt.grid(True, alpha=0.3)
    _save("ex05_sine_frame.png")


def main() -> None:
    ensure_dirs()
    fig_9_02_bar()
    fig_9_03_line()
    fig_9_04_pie()
    fig_9_05_donut()
    fig_9_06_scatter()
    fig_9_16_roma()
    hupu_bars()
    hupu_hourly()
    ex05_frame()


if __name__ == "__main__":
    main()
