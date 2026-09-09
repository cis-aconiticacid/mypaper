"""Build the standalone Chinese results table; never changes LaTeX or PDF."""
import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]

# Curated prose/table results, transcribed from manuscript e5222fa.
# Seven fields: group, setting, contrast, metric, result, unit/scope, source.
STATIC = r"""
主应用|MetroPT-3，n=16384，W=16，4 workers|Fixed → DC|E2 时间；Fixed/DC|14.9 → 8.56 s；1.75×|一个 failure-window；3 orders 的 median makespan 几何均值|T2
主应用|MetroPT-3，同一主应用|Fixed → DC|问题更新数；能耗比|5696 → 3128；Fixed/DC 能耗 1.78×|能耗与更新数属于该主应用，不与八 worker 结果拼接|S5:5.2
主应用|Packer19 components，n=16384，W=8|LM → DC|E1 时间；LM/DC|2.03 → 1.32 s；1.54×|24 host/order/GPU 配对单位；各单位先扣 consumer 再汇总|T2
主应用|Packer19，同一组件实验|LM → DC|E2 时间；LM/DC|3.89 → 3.18 s；1.22×|与上一行相同 24 单位；时间为中位数，比值单独配对汇总|T2
主应用|ImageNet-32，n=1024，W=8|Fixed → DC|E1 时间；Fixed/DC|122 → 116 s；1.05×，seed 范围 1.03–1.07×|3 paired training seeds；时间/比值几何均值|T2
主应用|ImageNet-32，同一训练|Fixed → DC|E3 全训练时间；Fixed/DC|188 → 182 s；1.04×，seed 范围 1.03–1.04×|3 seeds；每 run 50000 updates、6250 width-eight solves|T2
不确定性|MetroPT-3，另一个两 host 实验|Fixed / DC|E2；E1|E2=1.74×；E1=1.75×；E2 的 100(S−1) 区间 [74.3,74.7]%|6 host/plan 单位；区间为 stratified bootstrap；不是主四 worker 的区间|A:A.1
不确定性|Packer19 components|LM / DC|100(S−1) bootstrap 区间|E1 [53.9,54.0]%；E2 [22.4,22.5]%|固定输入的 timing uncertainty，不是跨任务泛化区间|A:A.1
消融|Packer19，τ=1e−3，固定宽度|逐问题双边缘 preliminary audit → batched 双边缘 audit|E1 基线/改动|1.13×；24/24 配对获益|共同四周期检查和 upstream two-marginal release verifier；扣 consumer|T5
消融|Packer19，同一设置|batched 双边缘 preliminary audit → row screen|E1 基线/改动|1.11×；24/24 配对获益|固定宽度不变；release verifier 不变|T5
消融|Packer19，同一设置|Fixed width + row screen → LM + row screen|E1 基线/改动|1.00×；100(S−1) 区间 [−0.019,0.033]%|LM 冻结状态但仍全宽更新；24 配对；近零收益|T5+A:A.1
消融|Packer19，同一设置|LM + row screen → DC + row screen|E1；问题更新|1.54×；256 → 156 updates|两臂关闭 buffer reuse、相同 verifier/check interval/width-one tail|T5+S5:5.4
资源|Packer19 components|LM → DC|GPU energy；peak allocated memory|880 → 688 J；80.8 → 107 MiB；额外 peak 26.1 MiB|paired-observation medians；增加峰值显存是代价|S5:5.4+S6
分项耗时|Packer19 components|LM → DC|Sinkhorn updates|1706 → 1071 ms|各 phase 单独中位数；不得加总替代 paired whole-path ratio|T9
分项耗时|Packer19 components|LM → DC|Row screen|639 → 401 ms|同上|T9
分项耗时|Packer19 components|LM → DC|Two-marginal verifier|105 → 105 ms|同上；四舍五入显示相同|T9
分项耗时|Packer19 components|LM → DC|Mask / compact|0.306 → 3.37 ms|同上；状态搬移开销更高|T9
容差补充|Packer19 独立 stopping sweep，τ=1e−3|LM → DC|E1 绝对中位数|2.04 → 1.30 s|独立于主组件实验；不可用此行替换 Table 2 时间|A:A.2
容差补充|Packer19 stopping sweep，τ=1e−2|LM / DC|同步完成；时间不确定性|8 个问题均 update 8 首次通过；R=0；100(S−1) 区间 [−0.134,0.032]%|24 配对；区间跨过等时；具体比值见下方 Figure 3 点|S5:5.4+A:A.1
分组|MetroPT-3，32 个固定问题，Homogeneous|该分组内 Fixed / DC|时间比；DC/Fixed 更新比例|1.10×；0.892|固定问题多重集，仅改变分组；不是不同输入采样|T6
分组|同一问题集，Heterogeneous|该分组内 Fixed / DC|时间比；更新比例|1.22×；0.802|同上|T6
分组|同一问题集，Random 1|该分组内 Fixed / DC|时间比；更新比例|1.26×；0.776|同上|T6
分组|同一问题集，Random 2|该分组内 Fixed / DC|时间比；更新比例|1.23×；0.789|同上|T6
分组|同一问题集，Random 3|该分组内 Fixed / DC|时间比；更新比例|1.27×；0.764|同上|T6
OTT-JAX|ImageNet-32，n=4096，W=16，τ=1e−3，q=20|Fixed-phase / DC；Native / DC|执行时间比|1.58×；2.64×|一个固定输入；10 repeats；q 匹配；Native 比较包含 phase 改变|T3
OTT-JAX|同上，τ=3e−3，q=10|Fixed-phase / DC；Native / DC|执行时间比|1.56×；2.62×|同上|T3
OTT-JAX|同上，τ=5e−3，q=10|Fixed-phase / DC；Native / DC|执行时间比|1.37×；2.30×|同上|T3
OTT-JAX|同上，τ=1e−2，q=10|Fixed-phase / DC；Native / DC|执行时间比|0.995×；1.73×|所有问题第一 phase 完成；匹配 compaction 对比略慢|T3
OTT-JAX 历史|较早的 6-repeat 实验|Native / DC；Fixed-phase / DC|执行时间比|2.60×；1.55×|与上述 10-repeat tolerance study 分开|A:A.3
PyKeOps 匹配|ImageNet-32，n=2048，W=4，check=1|Static / DC；Mask / DC|Coupling preparation 时间比|0.999×；1.00×|3 inputs × 3 orders；每输入配对中位数再求均值|T3
PyKeOps 匹配|ImageNet-32，n=16384，W=4，check=1|Static / DC；Mask / DC|Coupling preparation 时间比|1.02×；1.02×|3 inputs × 3 orders；全部方法 13 batch rounds|T3+S5:5.2
PyKeOps 匹配|n=16384 的三个输入|Static → DC|问题更新数|52 → 50、51、52；第三输入时间比约 1.00×|不同输入分别对应；包含同时完成的无收益输入|S5:5.2
PyKeOps 匹配|两种 n 的所有计时 runs|Backend residual 对 τ=1e−3|输出检查|54/54 runs 通过；一个小输入 order 的 Static/Mask 有额外 strict fallback|18 paired rounds × 3 methods；fallback 保留在汇总内|A:A.3
PyKeOps 历史|ImageNet-32，n=16384，W=4，Static check=1|Sequential / Static batch|时间比；max marginal L1|1.55×，范围 1.45–1.69×；8.80e−4|3 inputs；完整配置对比|T12
PyKeOps 历史|同上，LM check=1|Sequential / LM|时间比；max marginal L1|1.55×，范围 1.45–1.69×；8.93e−4|3 inputs；LM 为本文控制实现|T12
PyKeOps 历史|同上，DC check=2|Sequential / DC|时间比；max marginal L1|1.51×，范围 1.43–1.59×；8.93e−4|平均 14 rounds，Static 为 13；频率与压缩同时变化|T12+A:A.3
PyKeOps 历史|同上，DC check=4|Sequential / DC|时间比；max marginal L1|1.42×，范围 1.36–1.45×；8.93e−4|平均 16 rounds；Static 完整配置更快|T12+A:A.3
其他任务|A2D2，PyKeOps，n=8192，W=8|Sequential carry / DC|时间比；max marginal residual|3.17×，clip 范围 2.18–3.94×；9.97e−4|3 LiDAR clips；不是上述 ImageNet 输入|A:A.3
共享初始化|ImageNet features 构造流，90% overlap|同共享初始化下 Static / DC|Warm replay 时间比；移除更新|1.42×；30.6%|40 controlled windows；计入 descriptor/transfer/init/correction/verify|A:A.3
Worker scaling|MetroPT-3 held-out routes，1 → 4 workers|每 worker 固定工作量|Throughput scaling|3.97–3.98×|吞吐扩展，不是固定总工作 strong scaling；无 Sinkhorn collective|A:A.4
Worker endpoint|MetroPT-3，8 workers，higher workload|Fixed → DC|E2 时间；时间比；能耗比；更新数|12.5 → 4.03 s；3.11×；3.44×；4736 → 1276|同 worker 数下完整配置对比；不同于主应用|T10
Worker endpoint|MetroPT-3，8 workers，lower workload|Fixed → DC|E2 时间；时间比；能耗比；更新数|8.00 → 3.71 s；2.16×；2.29×；3008 → 1244|同上|T10
Support size|MetroPT-3，1 worker，n=8192|Fixed / DC|时间比|2.32×；绝对时间未在稿中给出|equal-host 几何均值；consumer criteria 两 hosts 均通过|T10+A:A.4
Support size|MetroPT-3，1 worker，n=32768|Fixed / DC|时间比|1.62×；绝对时间未在稿中给出|同上|T10+A:A.4
应用正确性|MetroPT-3 主应用|Fixed 与 DC；backend residual 对容差|最大 row/column residual；ROC AUC|row 9.5e−4；column 1.3e−6；两臂 AUC 均 1.0|backend 数值检查；不是独立 FP64 检查|S5:5.6
应用正确性|MetroPT-3 主应用|配对 Fixed 与 DC 输出|收敛；最大输出差|48/48 worker repeats 收敛；cost 差 2.79e−2，barycentric shift 差 3.47e−3|固定 failure-window consumer|A:A.2
Screen 检查|Packer19 components|screen-negative events 对 full-verifier replay|漏掉已完成问题数|0 / 1488 events|筛选延迟检查，不等于独立 FP64 输出检查|S5:5.6
释放一致性|Packer19 components|LM 与 DC|Release decisions；consumer TV 差|释放决策一致；TV=0|同一 transition workload、同 verifier|S5:5.6
实际输出 FP64|MetroPT-3 competitive|实际释放 potentials 的 FP64 marginals 对 1e−3|通过数；最大 residual；输出一致性|96/96 method–problem checks 通过；max 9.5e−4；各 batch 跨方法 potentials bitwise 一致|16 targets 共享 source；首个 timed run 输出，计时后 replay|S5:5.6
精度 stress|独立近阈值/运行时压力测试|Raw FP32、TF32、guard 对 FP64 replay|False accepts|FP32=3；TF32=3；guard=0|84 near-threshold + 16 runtime cases；1/2/4/8 GPUs；guard 未用于主应用计时|A:A.6
执行策略|MetroPT-3 competitive|Indexed、entry skip、DC|相对运行时间差|均低于 0.1%|同一组输入、复用 buffers；不是已证明统计等效|S5:5.7
模型消融|MetroPT-3，3 transferred groups|Width lookup 与线性 αa+β；都对实际时间|Mean absolute percentage error|0.853% vs 1.05%|36 method–repeat records；同 calibration，仅替换 update-cost 项|S5:5.7
模型方向|MetroPT-3，post-hoc|预测 Indexed/DC、entry-skip/DC 与实测比值方向|方向一致数|配对 median 6/6；逐 repeat 23/24；效应均 <0.1%|3 transferred groups × 2 contrasts；不是新输入覆盖|A:A.7
完成轨迹|MetroPT-3 competitive，四个 width-four groups|targets 0–3、4–7、8–11、12–15|各问题完成迭代|分别 (356,312,320,272)、(140,32,32,32)、(28,32,100,172)、(288,336,328,348)|共享 source；不同 targets 可能含重叠 sensor observations；不是计时 repeats 数|A:A.7
较早调度|MetroPT-3，W=16，四周期 graph blocks|Immediate DC、graph replay、bucketed|Steady-state solver time|8.43、8.42、9.24 s|同 prepared inputs；不包括 compile/graph capture/calibration|A:A.7
图示更新轨迹|ImageNet-32，Figure 1b，W=4|假设 fixed width 与 observed active trajectory|完成迭代；更新面积|nt=(130,75,90,70)；固定 520；active 365；R=155|一个记录窗口；更新数量，不是时间比|F1
Wave 估计|合成 width study，n=1024/4096/16384|bm×SM/n，bm=64，SM=108|单 block/SM 的 wave-width 估计|6.75、1.69、0.42|理论估计，不是实测加速；实测曲线全部点见后续行|S5:5.3
Width 曲线观察|合成 width study，n=1024/4096/16384|不同 active widths|阶梯位置|n1024：1–6 近似平台，6→7 跃升；n4096：1→2 首次大跃升；n16384：从 width 1 起响应|同合成配置；不能直接代入不同应用 kernel 的时间模型|S5:5.3
"""

FILES = {f"T{k}": f"figures/FIG-{name}.tex" for k, name in {
    2: "endpoints", 3: "backends", 5: "components", 6: "grouping", 9: "phases",
    10: "additional", 12: "backend-history"}.items()}
FILES.update(S5="sections/5_experiments.tex", S6="sections/6_scope.tex",
             A="sections/A_appendix.tex", F1="figures/FIG-method.tex")


def link(path, label):
    assert (PAPER / path).is_file(), path
    return f"[{label}]({path})"


def source(tags):
    return "；".join(link(FILES[tag.split(':')[0]], tag) for tag in tags.split('+'))


def fmt(value):
    return f"{value:.3g}"


def build():
    rows = []
    for line in STATIC.strip().splitlines():
        fields = line.split('|')
        assert len(fields) == 7, line
        fields[-1] = "论文当前表述：" + source(fields[-1])
        rows.append(fields)
    review = json.loads((HERE / 'review_data.json').read_text(encoding='utf-8'))
    comp = json.loads((HERE / 'competitive_data.json').read_text(encoding='utf-8'))
    spec = json.loads((HERE / 'figure_spec.json').read_text(encoding='utf-8'))
    review_source = link('support/figure_materials/review_data.json', '冻结数据 review_data.json')
    comp_source = link('support/figure_materials/competitive_data.json', '重算数据 competitive_data.json')
    # Quality: one comparison per metric/NFE, not a separate result for each arm.
    for metric, name in [('curvature_mean', 'Curvature'),
                         ('random_projection_frechet_diagonal', 'Projected Fréchet'),
                         ('heldout_strict_coupling_fm_mse', 'FM MSE')]:
        for nfe in ([4] if name == 'FM MSE' else [4, 8, 16]):
            values = [next(x for x in review['quality'] if x['metric'] == metric and
                           x['nfe'] == nfe and x['execution'] == arm) for arm in ('Fixed', 'Compacted')]
            result = ' → '.join(f"{fmt(x['mean'])} ± {fmt(x['sample_sd'])}" for x in values)
            rows.append(['训练质量', 'ImageNet-32 PCA500；' + ('NFE-independent' if name == 'FM MSE' else f'NFE={nfe}'),
                         'Fixed → DC，lower is better', name, result,
                         '3 paired seeds；mean ± sample SD；定义见 A.2；不是原图 FID',
                         review_source + f'：quality/{metric}/{nfe}；' + link('figures/FIG-quality.tex', 'Table 4')])
    for x in comp['training_times']:
        rows.append(['训练逐 seed', f"ImageNet-32 seed={x['seed']}", 'Fixed → DC', 'E3 全训练时间；配对节省',
                     f"{fmt(x['fixed_total_seconds'])} → {fmt(x['active_total_seconds'])} s；节省 {fmt(x['saved_seconds'])} s",
                     '50000 updates；6250 solves；节省由未舍入时间相减', comp_source + ': training_times；A.2'])
    # Table 8 and diagnostic values are displayed in the manuscript by seed.
    for seed, baseline, dc, ratio, diagnostic, counts in zip(
            [20260891, 20260892, 20260893], [123, 124, 119], [117, 116, 115],
            ['1.06', '1.07', '1.03'], ['1.16', '1.08', '1.08'], ['64/52', '64/56', '64/56']):
        rows.append(['训练逐 seed', f'ImageNet-32 seed={seed}', 'Fixed → DC', 'E1 solver 时间；Fixed/DC',
                     f'{baseline} → {dc} s；{ratio}×', '单 seed 训练内 solver 累计时间',
                     '论文当前表述：' + link('figures/FIG-seeds.tex', 'Table 8')])
        rows.append(['Coupling diagnostic', f'ImageNet-32 seed={seed}', 'Fixed / DC', '独立 coupling-preparation ratio；updates',
                     f'{diagnostic}×；{counts}', '与整段训练的 E1/E3 分开', '论文当前表述：' + source('A:A.2')])
    for x in comp['cells']:
        low, high = x['error_percent']
        rows.append(['执行与模型', f"MetroPT-3 targets {x['offset']}–{x['offset']+x['width']-1}，W={x['width']}",
                     'Indexed / entry skip / DC；模型对实际时间', '连续 E1 中位数；signed error range',
                     ' / '.join(fmt(x['seconds'][m]) for m in ('active_index','entry_skip','physical_compaction')) +
                     f' s；+{fmt(low)}% 至 +{fmt(high)}%',
                     ('目标组迁移' if x['target_heldout'] else '同输入，独立 calibration runs') + '；4 orders；共享 source',
                     comp_source + f": cells offset={x['offset']},W={x['width']}；Table 7"])
    for world, x in comp['guarded_stress']['by_world_size'].items():
        rows.append(['精度 stress 分 GPU 数', f'{world} GPUs', 'Guard release 与 FP64 replay release',
                     '21 near-threshold cases 的接受数',
                     f"{x['outward_releases']} vs {x['fp64_replay_releases']}",
                     '保守拒绝可能通过 replay 的候选；不是接受集一致', comp_source + f': guarded_stress/by_world_size/{world}；A.6'])
    with (HERE / 'PACKER19_STOPPING_METRICS.csv').open(encoding='utf-8-sig', newline='') as f:
        stopping = list(csv.DictReader(f))
    assert len(stopping) == 5
    for x in stopping:
        v = {k: float(z) for k,z in x.items()}
        lo, hi = (100*(v[k]-1) for k in ('lm_over_pc_ci_low','lm_over_pc_ci_high'))
        rows.append(['Figure 3 全部点', f"Packer19 τ={fmt(v['tolerance'])}", 'LM / DC；consumer 对 τ=1e−6 reference',
                     'E1 ratio；95% CI；max residual；max TV',
                     f"{fmt(v['lm_over_pc'])}×；100(S−1) CI [{fmt(lo)},{fmt(hi)}]% ；residual={fmt(v['max_actual_residual'])}；TV={fmt(v['max_consumer_tv'])}",
                     '24 配对/τ；equal-host stratified bootstrap；独立 stopping campaign',
                     link('support/figure_materials/PACKER19_STOPPING_METRICS.csv', '冻结 CSV') + f": tolerance={x['tolerance']}；Figure 3"])
    width_count = 0
    for n, points in spec['width']['data'].items():
        for a, x in sorted(points.items(), key=lambda p:int(p[0])):
            width_count += 1
            rows.append(['Figure 2 全部点', f'合成张量 n={n}，active width={a}', '同 n 下比较 active width；无应用基线',
                         '两个 update kernels 时间，median [Q1,Q3]',
                         f"{fmt(1000*x['median'])} [{fmt(1000*x['q1'])},{fmt(1000*x['q3'])}] ms",
                         f"{x['count']} calls；A100；d=500，column tile=64，cost scale=1；IQR 非 CI",
                         link('support/figure_materials/figure_spec.json', '机器 timing summary') + f': width/data/{n}/{a}；Figure 2'])
    windows = 0
    for x in review['widths']:
        w = x['width']
        rows.append(['Figure 4 汇总曲线', f'ImageNet-32 n=4096，W={w}', 'Sequential projected carry / shared-init active',
                     '平均 padding；steady time ratio；含 startup time ratio',
                     f"{fmt(x['mean_padding_ratio'])}；{fmt(x['steady_speedup'])}×；{fmt(x['deployment_speedup'])}×",
                     '40 windows/width；8 workers critical path；完整配置收益，非单变量 DC 收益',
                     review_source + f': widths/W={w}；Figure 4'])
        for i, window in enumerate(x['windows']):
            windows += 1
            nt = window['completion_iterations']
            fixed, active = w*max(nt), sum(nt)
            rows.append(['Figure 4 全部散点', f"W={w}；seed={window['seed']}；start={window['start_frame']}",
                         '该 active run 的假设 fixed-width work / 实际 active work',
                         '问题更新数及 padding ratio', f'{fixed} / {active} = {fmt(window["padding_ratio"])}',
                         '一个窗口；nt=(' + ','.join(map(str,nt)) + ')；不是实测时间比',
                         review_source + f': widths/W={w}/windows/{i}；Figure 4a'])
    assert windows == 200
    assert width_count == sum(len(v) for v in spec['width']['data'].values())
    assert all(len(row) == 7 for row in rows)
    intro = f'''# 论文全部实验结果对照总表（独立交付件）

对应英文论文提交 **e5222fa**（2026-09-09）。本表不被 `main.tex` 引用，不进入论文正文或附录 PDF。

共 **{len(rows)} 行**：去重汇总正文、附录和全部结果表；包含 Figure 2 的 {width_count} 个统计点、Figure 3 的 5 个容差点、Figure 4 的 5 组汇总及 200 个散点。Figure 1 的实测轨迹也单列。Table 1/11 是配置表，已分配到对应结果的条件栏，不作为新结果。理论公式、超参数、外部文献结果及未被当前稿使用的历史宏不作为本论文实验结果。

读法：Fixed 是固定宽度；LM 是本文实现的全宽更新后冻结状态控制；DC 是物理压缩；Indexed 只缩短 active-ID 网格；entry skip 在原布局内跳过 inactive 计算。时间比一律写清分子/分母，**大于 1 表示分母更快**。`A → B` 是两臂实测值，不自动表示单变量归因。E1=solver，E2=solver+consumer，E3=全训练/任务；不同 campaign、初始化、分配策略和统计单位不合并。

“论文当前表述”行按当前源码摘录，不把本次整理冒充重新核验远端原始实验。“冻结/重算数据”行直接读取仓库现有 JSON/CSV；数值来源链见 [审计记录](support/audits/REVIEW_DISPOSITION.md) 和数据文件中的 source 字段。未报告的绝对值不从其他实验补齐。输出值通常三位有效数字，小量用科学记数法；高精度原数保留在来源文件，窄 CI 用 100(S−1)% 避免显示为零宽。无收益、变慢、额外内存及 false accepts 均保留。

本地生成与一致性检查：`python support/figure_materials/build_results_inventory.py --check`。这是结果整理/复核材料，不是新增实验或作者最终科学审批。

| 序号 | 结果类别 | 任务与配置 | 比较双方／方向 | 指标 | 结果 | 统计单位与解释边界 | Source（同一行） |
|---|---|---|---|---|---|---|---|
'''
    return intro + ''.join('| ' + ' | '.join([str(i)] + [v.replace('|', r'\|').replace('\n',' ') for v in row]) + ' |\n'
                           for i,row in enumerate(rows,1))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = build()
    target = PAPER / 'ALL_RESULTS.md'
    if args.check:
        assert target.read_text(encoding='utf-8') == text, 'Inventory differs; regenerate and review.'
    else:
        target.write_text(text, encoding='utf-8', newline='\n')
    print('PASS: complete result inventory, local source links, graph-point counts and deterministic regeneration')
