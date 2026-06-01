"""图 9-7 涟漪特效散点图示例。"""

import numpy as np
from pyecharts import options as opts
from pyecharts.charts import EffectScatter

from _paths import HTML_DIR, ensure_dirs


def main() -> None:
    ensure_dirs()
    x = list(range(1, 21))
    rng = np.random.default_rng(7)
    y = rng.integers(10, 41, size=20).tolist()
    chart = (
        EffectScatter(init_opts=opts.InitOpts(width="600px", height="380px"))
        .add_xaxis(x)
        .add_yaxis("涟漪点", y, symbol="pin")
        .set_global_opts(title_opts=opts.TitleOpts(title="涟漪特效散点图示例"))
    )
    chart.render(str(HTML_DIR / "fig_9_07_effect_scatter.html"))


if __name__ == "__main__":
    main()
