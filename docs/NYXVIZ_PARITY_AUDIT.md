# NyxViz 录屏页非体渲染对齐审计

对照基准：本地 `video.html?record=1&scene=<id>`（有 `.dat`）  
部署目标：`static_figures_only` + `figures/` PNG 回退（中栏体渲染不在范围）

差异类型：**A** 静态 PNG 映射 · **B** 布局/CSS · **C** 图表尺寸/图例 · **D** 刷选读数/交互降级

| scene | 区域 | 差异类型 | 优先级 | 状态 |
|-------|------|----------|--------|------|
| intro | 左栏直方图+迷你趋势 | C | P2 | 图例已移右上角；待验收 |
| intro | 右栏刷选四卡 | A,D | P0 | band PNG 同源导出 + stats 读数 |
| intro | 底栏发现卡 | A,B | P1 | 04 验证图 1:1 + 映射统一 |
| task1-tf | 右光照图 | — | P4 | figures 一致 |
| task1-morph | 右缩略图 | — | P4 | evo PNG 已入库 |
| task2-evolution | 右四 panel | — | P3 | figures 一致 |
| task2-void | void 图 | — | P3 | figures 一致 |
| task2-cases | 三案例卡 | — | P3 | figures 一致 |
| task2-spatial | 四宫格+宽图 | B | P3 | dedicated 布局待 browse 验收 |
| task3-hist | 左 bin + 右指标图 | C | P3 | 图表来自 stats |
| task4-brush | 四卡预览 | A | P0 | task4_band_*_t99.png |
| task4-brush | 预设读数 | D | P0 | histogram/stats 降级 |
| task4-brush | 右栏 grid | B | P0 | 已改两列（task4-brush） |
| task4-validate | 左三验证图 | — | P3 | figures 一致 |
| findings | 2×2 四卡 | B | P1 | flex 撑满已修 |
| findings | 04 验证比例 | B | P1 | aspect-ratio 1:1 已修 |
| 全局 | browse 条文案 | — | P4 | sceneBrowseLabel 已修 |

## URL 注意

- 录屏 OBS：`?record=1&scene=<id>`（无 browse）
- 站点 demo：`?record=1&browse=1&scene=<id>` — browse 条占用 `vd-main-stack` 高度，需单独验收

## 验证命令

```powershell
cd F:\commercial\NyxViz\tools\python
python export_band_previews.py

cd F:\commercial\atelier
.\scripts\sync_nyxviz_video.ps1
.\scripts\verify_nyxviz_static.ps1
```
