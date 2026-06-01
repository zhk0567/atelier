"""图 9-3 双系列折线图。"""

from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker

from _paths import HTML_DIR, ensure_dirs


def main() -> None:
    ensure_dirs()
    clothes = Faker.clothes
    line = (
        Line(init_opts=opts.InitOpts(width="700px", height="380px"))
        .add_xaxis(clothes)
        .add_yaxis(
            "商家A",
            [102, 132, 105, 52, 90, 111, 95],
            symbol="diamond",
            symbol_size=15,
        )
        .add_yaxis(
            "商家B",
            [86, 108, 128, 66, 136, 122, 105],
            symbol="triangle",
            symbol_size=15,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="折线图示例"),
            yaxis_opts=opts.AxisOpts(name="销售额(万元)"),
            legend_opts=opts.LegendOpts(pos_top="8%"),
        )
    )
    line.render(str(HTML_DIR / "fig_9_03_line.html"))


if __name__ == "__main__":
    main()
