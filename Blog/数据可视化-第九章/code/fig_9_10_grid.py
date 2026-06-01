"""图 9-10 Grid 并行多图（柱形 + 折线）。"""

from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line

from _paths import HTML_DIR, ensure_dirs

PHONES = ["小米", "荣耀", "华为", "中兴", "魅族", "vivo", "OPPO"]
SALES_A = [107, 36, 102, 91, 51, 113, 45]
SALES_B = [104, 60, 33, 138, 105, 111, 91]


def main() -> None:
    ensure_dirs()
    bar = (
        Bar(init_opts=opts.InitOpts(width="700px", height="260px"))
        .add_xaxis(PHONES)
        .add_yaxis("商家A", SALES_A)
        .add_yaxis("商家B", SALES_B)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="柱形图", pos_top="2%"),
            legend_opts=opts.LegendOpts(pos_top="12%"),
        )
    )
    line = (
        Line(init_opts=opts.InitOpts(width="700px", height="260px"))
        .add_xaxis(PHONES)
        .add_yaxis("商家A", SALES_A, is_smooth=True)
        .add_yaxis("商家B", SALES_B, is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="折线图", pos_top="52%"),
            legend_opts=opts.LegendOpts(pos_top="62%"),
        )
    )
    grid = (
        Grid(init_opts=opts.InitOpts(width="720px", height="520px"))
        .add(bar, grid_opts=opts.GridOpts(pos_bottom="58%"))
        .add(line, grid_opts=opts.GridOpts(pos_top="58%"))
    )
    grid.render(str(HTML_DIR / "fig_9_10_grid.html"))


if __name__ == "__main__":
    main()
