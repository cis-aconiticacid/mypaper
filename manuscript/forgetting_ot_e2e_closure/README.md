# DrainSinkhorn 英文论文目录

本目录是当前英文论文的唯一真源。入口为 [main.tex](main.tex)，交付文件为 [main.pdf](main.pdf)。

## 章节导航

1. [Introduction](sections/1_introduction.tex)：问题、关键观察与三项贡献。
2. [Background and Motivation](sections/2_setting_related.tex)：EOT、实测完成项开销与相关系统。
3. [DrainSinkhorn](sections/3_method.tex)：screen、verify、compact 与状态一致性。
4. [Hardware-Aware Performance Model](sections/4_cost_and_hypothesis.tex)：更新数、运行时间与 GPU wave。
5. [Experiments](sections/5_experiments.tex)：设置、应用、宽度、组件、grouping、正确性。
6. [Discussion](sections/6_scope.tex)：适用条件与运行成本。
7. [Conclusion](sections/7_conclusion.tex)。
8. [Measurement Details](sections/A_appendix.tex)：计时与统计单位、训练输出、后端补充结果、worker 扩展、W 扫描、独立精度压力测试与复现信息。

## 新图表

所有图表已重新设计；旧图表可通过 Git 提交 795cb6c 查看，不参与当前编译。

| PDF | 源码 / 数据图 |
|---|---|
| Figure 1 | [FIG-method.tex](figures/FIG-method.tex)：执行循环及真实窗口的 active-width 轨迹；可编辑 TikZ 矢量源码 |
| Figure 2 | [FIG-width.pdf](figures/FIG-width.pdf)：绝对 kernel 时间与 active width |
| Figure 3 | [FIG-stopping.pdf](figures/FIG-stopping.pdf)：容差、speedup 与输出误差 |
| Figure 4 / Appendix A.5 | [FIG-scaling.pdf](figures/FIG-scaling.pdf)：已有 W=1/2/4/8/16 的 padding 与完整配置时间比 |
| Table 1 | [FIG-setup.tex](figures/FIG-setup.tex) |
| Table 2 | [FIG-endpoints.tex](figures/FIG-endpoints.tex)：E1/E2/E3，包含同组 Packer19 的 solver 与 pipeline 结果 |
| Table 3 | [FIG-backends.tex](figures/FIG-backends.tex)：OTT 同阶段／native 对照及 PyKeOps 完整配置比较 |
| Table 4 | [FIG-quality.tex](figures/FIG-quality.tex)：三 seed 的 mean ± sample SD |
| Table 5 / Section 5.4 | [FIG-components.tex](figures/FIG-components.tex) |
| Table 6 / Section 5.5 | [FIG-grouping.tex](figures/FIG-grouping.tex) |
| Table 7 | [FIG-seeds.tex](figures/FIG-seeds.tex) |
| Table 8 | [FIG-phases.tex](figures/FIG-phases.tex) |
| Table 9 | [FIG-additional.tex](figures/FIG-additional.tex) |

图表来源、设计与检查记录见 [visual review](support/audits/VISUAL_REVIEW.md)；可复现图形脚本见 [render_figures.py](support/figure_materials/render_figures.py)。其他原始图表数据与历史支持材料在 support/figure_materials/，不是论文真源。

新版审稿意见的逐条核验、处理及未完成实验见 [review disposition](support/audits/REVIEW_DISPOSITION.md)。应用级预测验证、PyKeOps 每更新检查的配对实验尚未完成；不要把文字修改或已有 W 扫描图视为这些实验已闭合。[reviewer_reanalysis.py](support/figure_materials/reviewer_reanalysis.py) 从证据仓库重算质量统计与宽度数据，[review_data.json](support/figure_materials/review_data.json) 保存本次派生结果。

## 构建

```powershell
python support/figure_materials/render_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -auxdir=support/build main.tex
```

编号以编译 PDF 和 support/build/main.aux 为准。
