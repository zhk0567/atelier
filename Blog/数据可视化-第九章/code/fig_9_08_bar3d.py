"""图 9-8 三维柱形图示例。"""

import random

from pyecharts import options as opts
from pyecharts.charts import Bar3D

from _paths import HTML_DIR, ensure_dirs


def main() -> None:
    ensure_dirs()
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    groups = ["A组", "B组", "C组", "D组", "E组"]
    raw = [[i, j, random.randint(0, 20)] for i in range(7) for j in range(5)]
    data = [[d[1], d[0], d[2]] for d in raw]
    chart = (
        Bar3D(init_opts=opts.InitOpts(width="900px", height="500px"))
        .add(
            "",
            data,
            xaxis3d_opts=opts.Axis3DOpts(type_="category", data=groups),
            yaxis3d_opts=opts.Axis3DOpts(type_="category", data=days),
            zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="三维柱形图示例"),
            visualmap_opts=opts.VisualMapOpts(max_=30),
        )
    )
    chart.render(str(HTML_DIR / "fig_9_08_bar3d.html"))


if __name__ == "__main__":
    main()
