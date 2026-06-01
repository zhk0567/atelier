"""图 9-13 / 9-14 Tab 选项卡多图。"""

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Tab

from _paths import HTML_DIR, ensure_dirs
from fig_9_10_grid import PHONES, SALES_A, SALES_B


def main() -> None:
    ensure_dirs()
    bar = (
        Bar()
        .add_xaxis(PHONES)
        .add_yaxis("商家A", SALES_A)
        .add_yaxis("商家B", SALES_B)
        .set_global_opts(title_opts=opts.TitleOpts(title="柱形图"))
    )
    line = (
        Line()
        .add_xaxis(PHONES)
        .add_yaxis("商家A", SALES_A, is_smooth=True)
        .add_yaxis("商家B", SALES_B, is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="折线图"))
    )
    tab = Tab()
    tab.add(bar, "柱形图")
    tab.add(line, "折线图")
    tab.render(str(HTML_DIR / "fig_9_13_tab.html"))


if __name__ == "__main__":
    main()
