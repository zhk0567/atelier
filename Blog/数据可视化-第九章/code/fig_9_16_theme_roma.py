"""图 9-16 ROMA 主题柱形图。"""

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

from _paths import HTML_DIR, ensure_dirs
from fig_9_10_grid import PHONES, SALES_A, SALES_B


def main() -> None:
    ensure_dirs()
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMA, width="700px", height="380px"))
        .add_xaxis(PHONES)
        .add_yaxis("商家A", SALES_A)
        .add_yaxis("商家B", SALES_B)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="柱形图-ROMA主题"),
            yaxis_opts=opts.AxisOpts(
                name="销售额(万元)",
                name_location="center",
                name_gap=30,
            ),
        )
        .set_series_opts(label_opts=opts.LabelOpts(position="top"))
    )
    bar.render(str(HTML_DIR / "fig_9_16_theme_roma.html"))


if __name__ == "__main__":
    main()
