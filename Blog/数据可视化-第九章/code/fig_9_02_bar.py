"""图 9-2 柱形图示例（基础写法 + 链式写法等价）。"""

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker

from _paths import HTML_DIR, ensure_dirs


def build_bar() -> Bar:
    clothes = ["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"]
    sales_a = [5, 20, 36, 10, 75, 90, 50]
    return (
        Bar(init_opts=opts.InitOpts(width="600px", height="300px"))
        .add_xaxis(clothes)
        .add_yaxis("商家A", sales_a)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="柱形图示例"),
            yaxis_opts=opts.AxisOpts(
                name="销售额(万元)",
                name_location="center",
                name_gap=30,
            ),
        )
        .set_series_opts(label_opts=opts.LabelOpts(position="top"))
    )


def main() -> None:
    ensure_dirs()
    build_bar().render(str(HTML_DIR / "fig_9_02_bar.html"))


if __name__ == "__main__":
    main()
