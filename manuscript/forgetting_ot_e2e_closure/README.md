# DrainSinkhorn 英文论文目录

本目录是当前英文论文的唯一真源。入口为 [main.tex](main.tex)，交付文件为 [main.pdf](main.pdf)。

## 章节导航

1. [Introduction](sections/1_introduction.tex)：问题、关键观察与三项贡献。
2. [Background and Motivation](sections/2_setting_related.tex)：EOT、实测完成项开销与相关系统；明确 logical mask 等是本文在 OT 后端中构建的实验对照，相关文献提供执行思想而非外部 OT 基线。
3. [DrainSinkhorn](sections/3_method.tex)：screen、verify、compact 与状态一致性。
4. [Hardware-Aware Performance Model](sections/4_cost_and_hypothesis.tex)：更新数、独立校准的条件时间重构与 GPU wave。
5. [Experiments](sections/5_experiments.tex)：设置、应用、宽度、组件、grouping、实际输出精度、无状态搬移对照及模型验证。
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
| Table 7 / Section 5.7 | [FIG-controls.tex](figures/FIG-controls.tex)：无状态搬移对照的绝对 solver 时间与独立校准误差 |
| Table 8 | [FIG-seeds.tex](figures/FIG-seeds.tex) |
| Table 9 | [FIG-phases.tex](figures/FIG-phases.tex) |
| Table 10 | [FIG-additional.tex](figures/FIG-additional.tex) |

图表来源、设计与检查记录见 [visual review](support/audits/VISUAL_REVIEW.md)；可复现图形脚本见 [render_figures.py](support/figure_materials/render_figures.py)。其他原始图表数据与历史支持材料在 support/figure_materials/，不是论文真源。

新版审稿意见的逐条核验及当前状态见 [review disposition](support/audits/REVIEW_DISPOSITION.md)。MetroPT-3 无状态搬移对照、条件时间重构、实际计时输出 FP64 回放和 PyKeOps 每更新检查结果已经并入英文正文；新增分组复用旧调度实验输入，不计作新增窗口覆盖。Packer19 直接无搬移对照、广泛输入分布和更强底层内核的匹配性能比较仍未闭合。

[competitive_reanalysis.py](support/figure_materials/competitive_reanalysis.py) 从证据仓库重算五组条件时间分析，核对 FP64 记录、旧输入身份和 PyKeOps 汇总，并生成 Table 7；[competitive_data.json](support/figure_materials/competitive_data.json) 保存来源、数值和原始文件身份。来源与正文位置映射见 review disposition 的 2026-09-09 更新。此核验为本地 CPU 重算，不是新 GPU 测量或作者最终审批。[reviewer_reanalysis.py](support/figure_materials/reviewer_reanalysis.py) 和 [review_data.json](support/figure_materials/review_data.json) 保留既有质量与宽度数据的复现入口。

## 构建

```powershell
python support/figure_materials/render_figures.py
python support/figure_materials/competitive_reanalysis.py --evidence-root <evidence-repository> --check
latexmk -pdf -interaction=nonstopmode -halt-on-error -auxdir=support/build main.tex
```

编号以编译 PDF 和 support/build/main.aux 为准。

最新行文修订：Section 2.3 在具体系统先例后明确执行层适配可构成独立系统贡献；Section 3 补充 host 同步、buffer、tail 路径和 OTT 编译缓存；Section 5 补全训练与残差配置，并报告条件模型的执行选择方向重算。Appendix A.6 更正精度压力测试为三次误接收及 guarded 路径零误接收，不再将其表述为零决策分歧。原始来源及未闭合项见 review disposition 最后一节；grouping 的既有绝对时间原始包仍待定位。
