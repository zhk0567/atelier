"""图 9-15 Timeline 时间线轮播柱形图。"""

from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline
from pyecharts.faker import Faker

from _paths import HTML_DIR, ensure_dirs


def main() -> None:
    ensure_dirs()
    tl = Timeline(init_opts=opts.InitOpts(width="700px", height="400px"))
    for year in range(2020, 2025):
        bar = (
            Bar()
            .add_xaxis(Faker.choose())
            .add_yaxis("销售额", Faker.values())
            .set_global_opts(title_opts=opts.TitleOpts(title=f"{year}年销售"))
        )
        tl.add(bar, f"{year}年")
    tl.add_schema(
        play_interval=2000,
        is_auto_play=True,
        symbol="diamond",
        symbol_size=15,
    )
    tl.render(str(HTML_DIR / "fig_9_15_timeline.html"))


if __name__ == "__main__":
    main()
