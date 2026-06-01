"""图 9-11 / 9-12 Page 顺序多图。"""

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Page

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
    page = Page(page_title="顺序多图", layout=Page.SimplePageLayout)
    page.add(bar)
    page.add(line)
    page.render(str(HTML_DIR / "fig_9_11_page.html"))


if __name__ == "__main__":
    main()
