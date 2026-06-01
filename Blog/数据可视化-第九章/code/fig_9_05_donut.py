"""图 9-5 圆环图示例。"""

from pyecharts import options as opts
from pyecharts.charts import Pie

from _paths import HTML_DIR, ensure_dirs


def main() -> None:
    ensure_dirs()
    data = [("小米", 150), ("华为", 120), ("OPPO", 95), ("vivo", 88), ("荣耀", 70)]
    pie = (
        Pie(init_opts=opts.InitOpts(width="600px", height="400px"))
        .add("", data, radius=["90px", "160px"])
        .set_global_opts(title_opts=opts.TitleOpts(title="圆环图示例"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    pie.render(str(HTML_DIR / "fig_9_05_donut.html"))


if __name__ == "__main__":
    main()
