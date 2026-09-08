# DrainSinkhorn：ICLR 2027 四问自审

更新时间：2026-09-07

依据：[ICLR 2027 Reviewer Guide](https://iclr.cc/Conferences/2027/ReviewerGuidelines) 与
[ICLR 2027 Call for Papers](https://iclr.cc/Conferences/2027/CallForPapers)。官方要求审稿人判断论文是否为社区带来足够价值和新知识，并依次回答问题、动机与文献定位、主张支持、意义与社区价值四个问题。ICLR 也明确接收 optimization、infrastructure、software libraries 与 hardware 方向的工作。

## 1. 论文解决的具体问题是什么

快速内核降低了单次 Sinkhorn update 的成本，但固定宽度批处理仍会让已经收敛的问题跟随最慢问题继续执行。DrainSinkhorn 研究如何在不改变 EOT 目标和最终 residual contract 的条件下，将通过当前验证的问题安全排出批次，并让后续 kernel 真实变窄。

审稿人应当在摘要和 Introduction 前两段读到同一个问题：

> Fast kernels make each Sinkhorn update cheaper; DrainSinkhorn removes future updates from verified-finished problems.

## 2. 方法是否有充分动机，并正确放进文献

论文将相关工作分成三层：

1. matrix-free、vectorized 与 fused kernels 优化单次 update；
2. automatic batching、Orca、Ginkgo 和 jaxipm 说明不同迭代深度可以被系统并行；
3. POT `solve_batch` 与 OTT-JAX `vmap` 已提供普通多问题 Sinkhorn batching；单边缘预检和已配置双边边缘停止检查也不是本文的方法贡献。DrainSinkhorn 的贡献从问题通过该停止规则之后开始：动态压缩全部逐问题 OT 状态，使后续 kernel 按存活批宽执行。

论文把普通 batching 与停止规则作为已有起点，把贡献限定为停止规则触发的动态压缩及其工作量与运行时间证据。生存曲线给出可移除的问题更新槽位；实测后端宽度成本曲线与增量控制开销共同决定这些槽位能否转化为墙钟收益。

## 3. 论文是否严谨支持主张

| 主张 | 直接证据 | 结论 |
|---|---|---|
| batched audit 有独立收益 | C80 Packer19，同输入与 verifier，consumer-subtracted OT stage，24 个 paired units | 1.133x，24/24 获胜 |
| Sinkhorn-specific screen 有独立收益 | C80，row screen 对 matched two-sided audit，consumer-subtracted OT stage | 1.105x static |
| logical masking 是否真正省计算 | C80-LM Packer19，fixed-width/logical-mask matched control | 1.00007x，95% CI [0.99981,1.00033]，中性 |
| dynamic compaction 有独立收益及边界 | C82 与 C66 MetroPT-3 matched fixed/dynamic；C80-LM 与 EXP-PACKER19 logical-mask/dynamic-compaction | C82 E2 为 1.745535x，C66 E1 为 1.753803x；Packer19 为 1.480--1.638x，$10^{-2}$ 时 0.9995x 中性 |
| 后端迁移 | 独立的 OTT-JAX 与 PyKeOps 单元 | 在各自匹配后端家族内均取得正执行收益；这些轻量适配仍有后端协同优化空间 |
| 深度异质性产生可删除工作 | M3 固定问题集合与总 correction work，只改变分组 | 1.105x 提升到 1.217--1.271x |
| 宽度缩减转化为墙钟收益 | A100 packed Triton `shifted_step` 原语诊断；固定 $n$、只改变 physical width | $n=1024$ 的 A1--6 中位数跨度 1.004x、A6--7 跃升 1.602x；$n=4096$ 首次跃升位于 A1--2；source：`studies/local_results/A100_WIDTH_COST_ENGINEERING_20260907T205000Z_73aec294/REPORT_ZH.md` 第 7--16 行 |
| screen 不改变释放语义 | C80 shadow replay | 1,488 个 screen-negative 事件中 0 个已满足 full verifier |
| 收益到达真实消费者 | MetroPT-3 alarm、Packer19 cell transition | wall time、能耗与 consumer contract 同时报告 |
| MetroPT 修正两臂复验 | C82 单主机四 worker；每个 plan 先汇总两次 timing repeat | E2 为 1.745535x，3/3 plan wins，描述性范围 1.745273--1.745975x |
| 收益到达训练端到端 | C63 real ImageNet-32 PCA500 feature-space OT-FM | matched fixed/dynamic-compaction 为 1.03556x；NFE 4/8/16 质量门通过 |
| 完整问题可跨 GPU 扩展 | C67 complete-device workers | 4-worker throughput 3.965--3.979x |

所有速度比统一写成 baseline time / proposed time。论文以 matched paths 为主证据；核心数字由 C82、C66、C80、C80-LM、M3、C63 和 C67 构成。

EXP-PACKER19 用同一冻结输入、两台主机和 768 个正式单元测量
current-residual controller 在
$10^{-4},3\times10^{-4},10^{-3},3\times10^{-3},10^{-2}$ 上的 OT 时间、
consumer TV 与执行收益。TV 只表示数值输出偏差，不是外部生物学性能标准。
正文以五点 same-controller Pareto 为 Packer19 主证据。

主表逐行公开计时范围：C82 直接报告 E2 ready-arrays-to-consumer；C66 与旧 C80 在每个 paired unit
内先从 E2 减去 consumer，再形成 E1 倍率和区间；EXP-PACKER19 直接记录 E1；
C63 读取 E3 记录中的 solver 字段；OTT-JAX 与 PyKeOps 直接计时 E1。GPU placement 和 timing repeat
用于稳定计时，不作为独立 workload 样本。C10 的 strict guard + FP64
escalation 只登记正确性，没有可比性能计时，论文不声称其 overhead。
正式 campaign 在计时前冻结 mode、width、audit interval 与 fallback；
M3 提供 operating-regime 证据，不再把失败的在线 selector 写成已闭合
router。OTT-JAX 与 PyKeOps 只共享 verified active retirement 原则，各自的
audit、rebucketing 和 packing 实现保持独立。

## 4. 工作带来了什么新知识和社区价值

DrainSinkhorn 提供三条可迁移结论：

1. 更快的 inner kernel 会把 stopping control 暴露为新的主要优化对象；
2. 对 Sinkhorn，已有停止规则提供完成信号；本文测量动态压缩如何把该信号转化为更窄的后续批次；
3. release-depth survival curve 与 backend 对 physical width 的经验响应共同决定 safe elimination 是否获利。

这些结论既是算法知识，也是部署知识。它们适用于 industrial EOT endpoints、scientific transition consumers 和 OT coupling preparation，并与 packed Triton 内核、matrix-free backend、warm start 与单问题 acceleration 组合。

## 当前审稿定位

当前版本已经形成一条完整的 ICLR 叙事：

> fast update -> heterogeneous release depth -> Sinkhorn-specific safe elimination -> eliminated candidate slots -> endpoint and training gains.

最重要的写作纪律是持续区分 component attribution 与 full deployment，同时把 safe elimination 作为核心算法概念放在摘要、Introduction、方法图和 Conclusion 的同一位置。
