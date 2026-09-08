# 最终论文术语对照表

本表记录最终英文论文及对应中文论文的术语统一结果。原稿位置采用本次修改前
Git HEAD 中的行号；表内旧表达只用于核查，不进入论文 PDF。

规则来源：[术语修改.md](术语修改.md)。

| 原稿表达 | 最终英文表述 | 最终中文表述 | 原稿文件与位置（修改前） |
|---|---|---|---|
| active-set contraction | physical compaction，或直接说明从逐问题状态中物理移除已完成问题 | 物理压缩，或直接说明从逐问题状态中物理移除已完成问题 | [1_introduction.tex](sections/1_introduction.tex) 原第 82、90 行；[4_cost_and_hypothesis.tex](sections/4_cost_and_hypothesis.tex) 原第 32 行；[A_appendix.tex](sections/A_appendix.tex) 原第 79 行；中文对应章节 |
| active-batch compaction / active-batch effect | physical compaction；需要描述对照时直接写 release and compaction | 物理压缩；需要描述对照时直接写释放与压缩 | [1_introduction.tex](sections/1_introduction.tex) 原第 63、71 行；[3_method.tex](sections/3_method.tex) 原第 4 行；[5_experiments.tex](sections/5_experiments.tex) 原第 19、33、127、129 行；中文对应章节 |
| completion depth(s)、depth variation、depth heterogeneity | iteration number(s)、the required iteration numbers differ | 迭代编号、所需迭代次数存在差异 | [0_abstract.tex](sections/0_abstract.tex) 原第 12--18、27 行；[1_introduction.tex](sections/1_introduction.tex) 原第 17、37--53 行；[4_cost_and_hypothesis.tex](sections/4_cost_and_hypothesis.tex) 原第 1--8、52--67、107 行；[6_scope.tex](sections/6_scope.tex) 原第 5、18 行；[7_conclusion.tex](sections/7_conclusion.tex) 原第 4、22 行；中文对应章节 |
| \ell_t、\ell_{\max} | n_t、n_{\max}；n_t 是问题首次在已配置验证时点通过双边际验证器时的批量迭代编号 | n_t、n_{\max}，定义与英文一致 | [0_abstract.tex](sections/0_abstract.tex) 原第 13--15 行；[1_introduction.tex](sections/1_introduction.tex) 原第 38--40 行；[3_method.tex](sections/3_method.tex) 原第 7--13 行；[4_cost_and_hypothesis.tex](sections/4_cost_and_hypothesis.tex) 原第 13--52 行；[5_experiments.tex](sections/5_experiments.tex) 原第 164 行；中文对应章节 |
| M3 的 profile depth D_t / D_s | offline every-cycle iteration number q_t / q_s | 离线逐循环迭代编号 q_t / q_s | [5_experiments.tex](sections/5_experiments.tex) 原第 163--166 行；[table8_grouping_intervention.tex](figures/table8_grouping_intervention.tex) 原第 3--10 行；[A_appendix.tex](sections/A_appendix.tex) 原末段；中文对应章节与表格 |
| completion-depth profile | the iteration numbers required by the problems in the batched window | 批量窗口内各问题所需的迭代次数 | [1_introduction.tex](sections/1_introduction.tex) 原第 37、53 行；[3_method.tex](sections/3_method.tex) 原第 140 行；中文对应章节 |
| depth-to-work | 删除标签；章节改为描述性的 Counting removed problem-update slots | 删除标签；章节改为“计算被移除的问题更新槽位” | [1_introduction.tex](sections/1_introduction.tex) 原第 73 行；[4_cost_and_hypothesis.tex](sections/4_cost_and_hypothesis.tex) 原第 11 行；中文对应章节 |
| within-window completion disagreement | problems in a batched window require different numbers of iterations | 批量窗口内的问题需要不同数量的迭代 | [0_abstract.tex](sections/0_abstract.tex) 原第 16 行；[1_introduction.tex](sections/1_introduction.tex) 原第 75 行；[7_conclusion.tex](sections/7_conclusion.tex) 原第 22 行；中文对应章节 |
| production audit、configured audit、audit interval/grid | configured verifier check、check interval、verifier-check schedule | 已配置验证时点、检查间隔、验证检查时点 | [3_method.tex](sections/3_method.tex) 原第 9、103、141 行；[4_cost_and_hypothesis.tex](sections/4_cost_and_hypothesis.tex) 原第 14、48、76 行；[5_experiments.tex](sections/5_experiments.tex) 原第 9 行；[A_appendix.tex](sections/A_appendix.tex) 原第 36、76、87--91 行；[table10_workload_configurations.tex](figures/table10_workload_configurations.tex) 原第 11--15 行；中文对应章节与表格 |
| two-sided stopping check、two-marginal stopping check、full check | two-marginal verifier；需要展开时写明同时检查行、列残差 | 双边际验证器；需要展开时写明同时检查行、列边缘残差 | [3_method.tex](sections/3_method.tex) 原第 54、103--104、123--125 行；[4_cost_and_hypothesis.tex](sections/4_cost_and_hypothesis.tex) 原第 14 行；[5_experiments.tex](sections/5_experiments.tex) 原第 144--153、192 行；[A_appendix.tex](sections/A_appendix.tex) 原第 12、36 行；中文对应章节 |
| updated-marginal screen | a preliminary check using the current marginals | 使用当前边缘进行初步检查 | [1_introduction.tex](sections/1_introduction.tex) 原第 34 行；[2_setting_related.tex](sections/2_setting_related.tex) 原第 44--53 行；[5_experiments.tex](sections/5_experiments.tex) 原第 142--146 行；中文对应章节 |
| shadow replay | replaying the screened results and checking each with the verifier | 重放筛选结果并逐一使用验证器检查 | [3_method.tex](sections/3_method.tex) 原第 103--105 行；[5_experiments.tex](sections/5_experiments.tex) 原第 144--149 行；中文对应章节 |
| fixed-work grouping | grouping while holding total iteration counts fixed | 在保持总迭代次数不变的条件下进行分组 | [1_introduction.tex](sections/1_introduction.tex) 原第 81 行；[7_conclusion.tex](sections/7_conclusion.tex) 原第 22 行；中文对应章节 |
| width-cost curve | runtime as a function of batch width | 批宽与实测运行时间之间的关系 | [1_introduction.tex](sections/1_introduction.tex) 原第 44 行；[4_cost_and_hypothesis.tex](sections/4_cost_and_hypothesis.tex) 原第 138 行；[6_scope.tex](sections/6_scope.tex) 原第 5--7 行；中文对应章节 |
| phase-active | execution that processes only the remaining problems in each fixed phase | 每个固定阶段只处理剩余问题的执行 | [5_experiments.tex](sections/5_experiments.tex) 原第 76 行；[table9_cross_backend_results.tex](figures/table9_cross_backend_results.tex) 原第 14 行；中文对应章节与表格 |
| phase-boundary retirement | completed problems are removed only at phase boundaries | 只在阶段边界移除已完成问题 | [5_experiments.tex](sections/5_experiments.tex) 原第 78 行；中文对应章节 |
| projected-carry | initializing with the projected previous state | 以前一状态的投影值初始化 | [5_experiments.tex](sections/5_experiments.tex) 原第 174 行；[TABLE_OPERATING_REGIME.tex](figures/TABLE_OPERATING_REGIME.tex) 原第 3 行；[table10_workload_configurations.tex](figures/table10_workload_configurations.tex) 原第 3 行；中文对应章节与表格 |
| shared-anchor | using one initialization for multiple problems | 多个问题使用同一初始化 | [0_abstract.tex](sections/0_abstract.tex) 原第 24 行；[5_experiments.tex](sections/5_experiments.tex) 原第 62、175 行；[6_scope.tex](sections/6_scope.tex) 原第 11 行；[7_conclusion.tex](sections/7_conclusion.tex) 原第 13 行；相关英文、中文表格 |
| paired-consumer-subtracted | paired comparison after subtracting consumer time | 扣除消费者时间后的配对比较 | [table7_packer19_attribution.tex](figures/table7_packer19_attribution.tex) 原第 4 行；中文对应表格 |
| release-fair controls | controls using the same release rule | 使用相同释放规则的对照 | [A_appendix.tex](sections/A_appendix.tex) 原第 32 行；中文对应附录 |
| width-one | processing one problem at a time | 逐问题执行 | [TABLE_OPERATING_REGIME.tex](figures/TABLE_OPERATING_REGIME.tex) 原第 3 行；中文 [A_appendix.tex](../forgetting_ot_e2e_closure_zh/sections/A_appendix.tex) 原第 7 行与对应表格 |
| backend-matched | comparison using the same backend | 使用相同后端的比较 | [0_abstract.tex](sections/0_abstract.tex) 原第 20 行；[1_introduction.tex](sections/1_introduction.tex) 原第 85 行；中文对应章节 |
| inner-backend | the backend used for the inner OT updates | 内部 OT 更新使用的后端 | [5_experiments.tex](sections/5_experiments.tex) 原第 10 行；中文对应章节 |
| row-sharded / row sharding | partitioning the matrix by rows | 按行划分矩阵 | [A_appendix.tex](sections/A_appendix.tex) 原第 102--105 行；中文对应附录 |
| coupling-to-consumer boundary | the path from the OT coupling to the downstream consumer | 从 OT coupling 到下游消费者的路径 | [2_setting_related.tex](sections/2_setting_related.tex) 原第 60 行；中文对应章节 |
| output-deviation diagnostic | checking differences in outputs | 检查输出差异 | [5_experiments.tex](sections/5_experiments.tex) 原第 103 行；[A_appendix.tex](sections/A_appendix.tex) 原第 55 行；中文对应章节 |
| proposal alignment | the components of the initial error along the convergence modes | 初始误差在收敛模态上的分量 | [0_abstract.tex](sections/0_abstract.tex) 原第 18 行；[4_cost_and_hypothesis.tex](sections/4_cost_and_hypothesis.tex) 原第 98--100 行；中文对应章节 |
| weighted quotient | 保留 | 保留 | [4_cost_and_hypothesis.tex](sections/4_cost_and_hypothesis.tex) 的局部商空间线性化小节；中文对应章节 |
| rebucketing | 保留 | 保留 | [5_experiments.tex](sections/5_experiments.tex) 的 OTT-JAX 结果；[A_appendix.tex](sections/A_appendix.tex) 的独立后端实现 |
| physical compaction | 保留，指通过验证后从全部逐问题批量状态中物理移除问题并缩小后续批宽 | 保留，定义与英文一致 | [3_method.tex](sections/3_method.tex) 的方法定义与执行模式；中文对应章节 |

代码字段、campaign 名称、原始数据列名和冻结证据文件没有因论文术语统一而重命名。
这保证了实验溯源路径不变；论文可见文字使用本表右侧的统一表述。
