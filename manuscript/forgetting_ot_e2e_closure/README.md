# DrainSinkhorn 英文论文目录

本目录是仓库内当前英文论文的唯一真源，包含编译入口、正文、参考文献、实际引用的图表和交付 PDF。

## 论文入口

- [`main.tex`](main.tex)：英文 LaTeX 入口。
- [`main.pdf`](main.pdf)：当前英文 PDF。
- [`sections/`](sections/)：按编译顺序拆分的正文和附录。
- [`figures/`](figures/)：当前论文实际 `\input` 或 `\includegraphics` 的图表文件。
- [`math_commands.tex`](math_commands.tex)：数学命令。
- [`references.bib`](references.bib)：参考文献。

## 支持材料

不直接进入论文编译的材料统一放在 [`support/`](support/)：

- [`support/audits/`](support/audits/)：主张审计、证据范围、术语和写作检查材料。
- [`support/figure_materials/`](support/figure_materials/)：图表数据、生成脚本和当前未引用的历史表格源码。
- [`support/build/`](support/build/)：LaTeX 中间文件、构建日志和脚本缓存。
- [`support/qa/`](support/qa/)：页面渲染与目视检查截图。

这些支持材料不是第二套论文真源。论文内容只在 `main.tex`、`sections/` 和当前实际引用的
`figures/` 文件中修改。

## 当前表格位置

| PDF 编号 | 英文 TeX |
|---|---|
| Table 1 | [`figures/table1_prior_systems.tex`](figures/table1_prior_systems.tex) |
| Table 2 | [`figures/table2_main_results_by_width.tex`](figures/table2_main_results_by_width.tex) |
| Table 3 | [`figures/table3_eight_gpu_decomposition.tex`](figures/table3_eight_gpu_decomposition.tex) |
| Table 4 | [`figures/table4_imagenet_quality.tex`](figures/table4_imagenet_quality.tex) |
| Table 5 | [`figures/table5_packer19_attribution.tex`](figures/table5_packer19_attribution.tex) |
| Table 6 | [`figures/table6_grouping_intervention.tex`](figures/table6_grouping_intervention.tex) |
| Table 7 | [`figures/table7_cross_backend_results.tex`](figures/table7_cross_backend_results.tex) |
| Table 8 | [`figures/table8_workload_configurations.tex`](figures/table8_workload_configurations.tex) |
| Table 9 | [`figures/table9_absolute_ot_times.tex`](figures/table9_absolute_ot_times.tex) |
| Table 10 | [`figures/table10_attribution_map.tex`](figures/table10_attribution_map.tex) |
| Table 11 | [`figures/table11_imagenet_solver_pairs.tex`](figures/table11_imagenet_solver_pairs.tex) |
| Table 12 | [`figures/table12_packer19_phase_costs.tex`](figures/table12_packer19_phase_costs.tex) |

编号以最新编译 PDF 和 `support/build/main.aux` 为准。

## 构建

在本目录运行：

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -auxdir=support/build main.tex
```

交付前检查 PDF 的章节、公式、图表、引用、数字和限定条件。
