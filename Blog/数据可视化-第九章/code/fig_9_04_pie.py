"""图 9-4 饼图示例。"""

from pyecharts import options as opts
from pyecharts.charts import Pie

from _paths import HTML_DIR, ensure_dirs


def main() -> None:
    ensure_dirs()
    data = [("小米", 150), ("华为", 200), ("荣耀", 100), ("魅族", 60), ("vivo", 145), ("OPPO", 160)]
    pie = (
        Pie(init_opts=opts.InitOpts(width="600px", height="400px"))
        .add("", data)
        .set_global_opts(title_opts=opts.TitleOpts(title="饼图示例"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    pie.render(str(HTML_DIR / "fig_9_04_pie.html"))


if __name__ == "__main__":
    main()
