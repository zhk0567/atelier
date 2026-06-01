"""课后第五大题：正弦曲线与沿曲线运动的红点动画（Matplotlib）。"""

from __future__ import annotations

import math

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from _paths import PNG_DIR, ensure_dirs

FRAMES = 100
INTERVAL_MS = 100


def main() -> None:
    ensure_dirs()
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    x = np.linspace(0, 2 * math.pi, 200)
    y = np.sin(x)
    x_track = np.linspace(0, 2 * math.pi, FRAMES)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y, color="steelblue", linewidth=2, label="sin(x)")
    (point,) = ax.plot([], [], "ro", markersize=10)
    coord_text = ax.text(
        0.98,
        0.95,
        "",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=11,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )
    ax.set_xlim(0, 2 * math.pi)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("正弦曲线与动点坐标")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="upper left")

    def update(frame: int):
        px = float(x_track[frame])
        py = float(np.sin(px))
        point.set_data([px], [py])
        coord_text.set_text(f"x={px:.3f}, y={py:.3f}")
        return point, coord_text

    preview_path = PNG_DIR / "ex05_sine_frame.png"
    update(FRAMES // 3)
    fig.savefig(preview_path, dpi=120, bbox_inches="tight")

    gif_path = PNG_DIR / "ex05_sine_animation.gif"
    anim = animation.FuncAnimation(
        fig,
        update,
        frames=FRAMES,
        interval=INTERVAL_MS,
        blit=True,
    )
    try:
        anim.save(str(gif_path), writer=animation.PillowWriter(fps=10))
    except Exception as exc:
        print("gif skip:", exc)
    plt.close(fig)


if __name__ == "__main__":
    main()
