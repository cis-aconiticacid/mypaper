# DrainSinkhorn 英文论文目录

本目录是当前英文论文的唯一真源。入口为 [main.tex](main.tex)，交付文件为 [main.pdf](main.pdf)。

独立交付件：[全部实验结果对照总表](ALL_RESULTS.md)。汇总正文、附录和图中数据点，逐行给出比较双方、数值、统计口径与 source；不进入论文 PDF。由 [build_results_inventory.py](support/figure_materials/build_results_inventory.py) 从当前论文摘录和已有冻结数据生成，可用 `--check` 核对。表头注明对应论文提交，避免与后续修订混用。

## 章节导航

当前标题为 DrainSinkhorn: Completion-Aware Execution for Batched Entropic Optimal Transport。最新审稿增量：A.2 补指标公式与输入构造；Table 2 补同 campaign 的绝对时间；Table 5 明列消融两端；Table 9 区分 row screen 与 verifier；A.6 补 guard 上界及假设；历史 PyKeOps 配置移入 Table 12。Table 7 与 Section 5.7 同在第 10 页。已完成 anti-defensive-writing 审计；必要的统计与精度边界保留。完整精度结果在 competitive_data.json 的 endpoint_times_seconds/linear_model_comparison/training_times。处理状态见 review disposition 顶部 Latest review。

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
| Table 2 | [FIG-endpoints.tex](figures/FIG-endpoints.tex)：E1/E2/E3，同组比值与绝对时间；聚合方式见 caption |
| Table 3 | [FIG-backends.tex](figures/FIG-backends.tex)：OTT 同阶段／native 对照及 PyKeOps 每更新检查的匹配比较 |
| Table 4 | [FIG-quality.tex](figures/FIG-quality.tex)：三 seed 的 mean ± sample SD |
| Table 5 / Section 5.4 | [FIG-components.tex](figures/FIG-components.tex) |
| Table 6 / Section 5.5 | [FIG-grouping.tex](figures/FIG-grouping.tex) |
| Table 7 / Section 5.7 | [FIG-controls.tex](figures/FIG-controls.tex)：无状态搬移对照的绝对 solver 时间与独立校准误差 |
| Table 8 | [FIG-seeds.tex](figures/FIG-seeds.tex) |
| Table 9 | [FIG-phases.tex](figures/FIG-phases.tex) |
| Table 10 | [FIG-additional.tex](figures/FIG-additional.tex) |
| Table 11 | [FIG-execution-settings.tex](figures/FIG-execution-settings.tex)：主要 Triton 对照的 buffer 策略、共同精度/初始化/检查/tail 设置和计时端点 |
| Table 12 | [FIG-backend-history.tex](figures/FIG-backend-history.tex)：历史 PyKeOps 完整配置，保留静态批处理快于压缩的结果 |

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

实验复现补充：Section 5.1 定义 cost 与边缘分布；Appendix A.2 给出距离缩放取样和共享 PCA 特征坐标。Section 5.7 的执行顺序比较明确为 post-hoc 分析。剩余证据项与原始包定位状态见 review disposition 的 Resumed workflow 小节。

最新行文修订：Section 2.3 在具体系统先例后明确执行层适配可构成独立系统贡献；Section 3 补充 host 同步、buffer、tail 路径和 OTT 编译缓存；Section 5 补全训练与残差配置，并报告条件模型的执行选择方向重算。Appendix A.6 更正精度压力测试为三次误接收及 guarded 路径零误接收，不再将其表述为零决策分歧。原始来源及未闭合项见 review disposition 最后一节；grouping 的既有绝对时间原始包仍待定位。
