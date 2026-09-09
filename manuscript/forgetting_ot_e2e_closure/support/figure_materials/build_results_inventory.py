"""Build the standalone English results table; never changes LaTeX or PDF."""
import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]

# Curated prose/table results, transcribed from manuscript e5222fa.
# Seven fields: group, setting, contrast, metric, result, unit/scope, source.
STATIC = r"""
Main application|MetroPT-3, n=16384, W=16, 4 workers|Fixed → DC|E2 time; Fixed/DC|14.9 → 8.56 s; 1.75×|One failure-window workload; geometric mean of median makespans across 3 orders|T2
Main application|MetroPT-3, same primary application|Fixed → DC|Problem updates; energy ratio|5696 → 3128; Fixed/DC energy 1.78×|Counts and energy belong to this primary application, separately from the eight-worker study|S5:5.2
Main application|Packer19 components, n=16384, W=8|LM → DC|E1 time; LM/DC|2.03 → 1.32 s; 1.54×|24 paired host/order/GPU units; subtract consumer time within each unit before aggregation|T2
Main application|Packer19, same component study|LM → DC|E2 time; LM/DC|3.89 → 3.18 s; 1.22×|Same 24 units as above; median times and separately aggregated paired ratios|T2
Main application|ImageNet-32, n=1024, W=8|Fixed → DC|E1 time; Fixed/DC|122 → 116 s; 1.05×, seed range 1.03–1.07×|3 paired training seeds; geometric means of times and ratios|T2
Main application|ImageNet-32, same training study|Fixed → DC|E3 full-training time; Fixed/DC|188 → 182 s; 1.04×, seed range 1.03–1.04×|3 seeds; 50000 updates and 6250 width-eight solves per run|T2
Uncertainty|MetroPT-3, separate two-host study|Fixed / DC|E2; E1|E2=1.74×; E1=1.75×; E2 interval for 100(S−1): [74.3,74.7]%|6 host/plan units; stratified bootstrap interval; separate from the primary four-worker interval|A:A.1
Uncertainty|Packer19 components|LM / DC|Bootstrap intervals for 100(S−1)|E1 [53.9,54.0]%; E2 [22.4,22.5]%|Timing uncertainty on fixed inputs, not a cross-workload generalization interval|A:A.1
Ablation|Packer19, τ=1e−3, fixed width|Per-problem two-marginal preliminary audit → batched two-marginal audit|E1 baseline/changed configuration|1.13×; 24/24 paired observations favor the change|Shared four-cycle checking and upstream two-marginal release verifier; consumer-subtracted time|T5
Ablation|Packer19, same setting|Batched two-marginal preliminary audit → row screen|E1 baseline/changed configuration|1.11×; 24/24 paired observations favor the change|Fixed width and release verifier unchanged|T5
Ablation|Packer19, same setting|Fixed width + row screen → LM + row screen|E1 baseline/changed configuration|1.00×; interval for 100(S−1): [−0.019,0.033]%|LM freezes state after full-width updates; 24 pairs; near-zero benefit|T5+A:A.1
Ablation|Packer19, same setting|LM + row screen → DC + row screen|E1; problem updates|1.54×; 256 → 156 updates|Both arms disable buffer reuse and share verifier, check interval and width-one tail|T5+S5:5.4
Resources|Packer19 components|LM → DC|GPU energy; peak allocated memory|880 → 688 J; 80.8 → 107 MiB; additional peak 26.1 MiB|Paired-observation medians; higher peak memory is a cost|S5:5.4+S6
Phase timing|Packer19 components|LM → DC|Sinkhorn updates|1706 → 1071 ms|Separate phase medians; their sum does not replace the paired whole-path ratio|T9
Phase timing|Packer19 components|LM → DC|Row screen|639 → 401 ms|Separate phase medians|T9
Phase timing|Packer19 components|LM → DC|Two-marginal verifier|105 → 105 ms|Separate phase medians; equal at displayed precision|T9
Phase timing|Packer19 components|LM → DC|Mask / compact|0.306 → 3.37 ms|Separate phase medians; state movement has higher overhead|T9
Tolerance supplement|Packer19, separate stopping sweep, τ=1e−3|LM → DC|Absolute E1 medians|2.04 → 1.30 s|Separate from the primary component study; these times do not replace Table 2|A:A.2
Tolerance supplement|Packer19 stopping sweep, τ=1e−2|LM / DC|Simultaneous completion; timing uncertainty|All 8 problems first pass at update 8; R=0; interval for 100(S−1): [−0.134,0.032]%|24 pairs; interval spans equal time; the ratio is listed with the Figure 3 points below|S5:5.4+A:A.1
Grouping|MetroPT-3, 32 fixed problems, Homogeneous|Fixed / DC within this grouping|Time ratio; DC/Fixed update fraction|1.10×; 0.892|Fixed problem multiset; only grouping changes, not the sampled inputs|T6
Grouping|Same problem set, Heterogeneous|Fixed / DC within this grouping|Time ratio; update fraction|1.22×; 0.802|Fixed problem multiset; only grouping changes|T6
Grouping|Same problem set, Random 1|Fixed / DC within this grouping|Time ratio; update fraction|1.26×; 0.776|Fixed problem multiset; only grouping changes|T6
Grouping|Same problem set, Random 2|Fixed / DC within this grouping|Time ratio; update fraction|1.23×; 0.789|Fixed problem multiset; only grouping changes|T6
Grouping|Same problem set, Random 3|Fixed / DC within this grouping|Time ratio; update fraction|1.27×; 0.764|Fixed problem multiset; only grouping changes|T6
OTT-JAX|ImageNet-32, n=4096, W=16, τ=1e−3, q=20|Fixed-phase / DC; Native / DC|Execution-time ratios|1.58×; 2.64×|One fixed input; 10 repeats; matched q; Native comparison includes the phase change|T3
OTT-JAX|Same setting, τ=3e−3, q=10|Fixed-phase / DC; Native / DC|Execution-time ratios|1.56×; 2.62×|One fixed input; 10 repeats; matched q; Native comparison includes the phase change|T3
OTT-JAX|Same setting, τ=5e−3, q=10|Fixed-phase / DC; Native / DC|Execution-time ratios|1.37×; 2.30×|One fixed input; 10 repeats; matched q; Native comparison includes the phase change|T3
OTT-JAX|Same setting, τ=1e−2, q=10|Fixed-phase / DC; Native / DC|Execution-time ratios|0.995×; 1.73×|All problems finish in the first phase; compaction is slightly slower in the matched comparison|T3
Earlier OTT-JAX|Earlier 6-repeat study|Native / DC; Fixed-phase / DC|Execution-time ratios|2.60×; 1.55×|Separate from the 10-repeat tolerance study above|A:A.3
Matched PyKeOps|ImageNet-32, n=2048, W=4, check=1|Static / DC; Mask / DC|Coupling-preparation time ratios|0.999×; 1.00×|3 inputs × 3 orders; mean of per-input paired medians|T3
Matched PyKeOps|ImageNet-32, n=16384, W=4, check=1|Static / DC; Mask / DC|Coupling-preparation time ratios|1.02×; 1.02×|3 inputs × 3 orders; all methods take 13 batch rounds|T3+S5:5.2
Matched PyKeOps|Three inputs at n=16384|Static → DC|Problem updates|52 → 50, 51, 52; third-input time ratio approximately 1.00×|Values correspond to the three inputs; includes simultaneous completion without a gain|S5:5.2
Matched PyKeOps|All timed runs at both support sizes|Backend residual against τ=1e−3|Output checks|54/54 runs pass; Static/Mask require an extra strict fallback in one small-input order|18 paired rounds × 3 methods; summaries include the fallback|A:A.3
Earlier PyKeOps|ImageNet-32, n=16384, W=4, Static check=1|Sequential / Static batch|Time ratio; maximum marginal L1|1.55×, range 1.45–1.69×; 8.80e−4|3 inputs; complete-configuration comparison|T12
Earlier PyKeOps|Same setting, LM check=1|Sequential / LM|Time ratio; maximum marginal L1|1.55×, range 1.45–1.69×; 8.93e−4|3 inputs; LM is the control implemented in this study|T12
Earlier PyKeOps|Same setting, DC check=2|Sequential / DC|Time ratio; maximum marginal L1|1.51×, range 1.43–1.59×; 8.93e−4|Mean 14 rounds versus 13 for Static; checking frequency and compaction both change|T12+A:A.3
Earlier PyKeOps|Same setting, DC check=4|Sequential / DC|Time ratio; maximum marginal L1|1.42×, range 1.36–1.45×; 8.93e−4|Mean 16 rounds; the complete Static configuration is faster|T12+A:A.3
Additional task|A2D2, PyKeOps, n=8192, W=8|Sequential carry / DC|Time ratio; maximum marginal residual|3.17×, clip range 2.18–3.94×; 9.97e−4|3 LiDAR clips; separate from the ImageNet inputs above|A:A.3
Shared initialization|Constructed ImageNet-feature stream, 90% overlap|Static / DC under shared initialization|Warm-replay time ratio; removed updates|1.42×; 30.6%|40 controlled windows; includes descriptor/transfer/init/correction/verify|A:A.3
Worker scaling|MetroPT-3 held-out routes, 1 → 4 workers|Fixed work per worker|Throughput scaling|3.97–3.98×|Throughput scaling, not fixed-total-work strong scaling; no Sinkhorn collective|A:A.4
Worker endpoint|MetroPT-3, 8 workers, higher workload|Fixed → DC|E2 time; time ratio; energy ratio; updates|12.5 → 4.03 s; 3.11×; 3.44×; 4736 → 1276|Complete-configuration comparison at the same worker count; separate from the primary application|T10
Worker endpoint|MetroPT-3, 8 workers, lower workload|Fixed → DC|E2 time; time ratio; energy ratio; updates|8.00 → 3.71 s; 2.16×; 2.29×; 3008 → 1244|Complete-configuration comparison at the same worker count; separate from the primary application|T10
Support size|MetroPT-3, 1 worker, n=8192|Fixed / DC|Time ratio|2.32×; absolute times not reported in the manuscript|Equal-host geometric mean; consumer criteria pass on both hosts|T10+A:A.4
Support size|MetroPT-3, 1 worker, n=32768|Fixed / DC|Time ratio|1.62×; absolute times not reported in the manuscript|Equal-host geometric mean; consumer criteria pass on both hosts|T10+A:A.4
Application correctness|Primary MetroPT-3 application|Fixed and DC; backend residual against tolerance|Maximum row/column residual; ROC AUC|Row 9.5e−4; column 1.3e−6; AUC 1.0 in both arms|Backend numerical checks, separately from independent FP64 checks|S5:5.6
Application correctness|Primary MetroPT-3 application|Paired Fixed and DC outputs|Convergence; maximum output differences|48/48 worker repeats converge; cost difference 2.79e−2, barycentric-shift difference 3.47e−3|Fixed failure-window consumer|A:A.2
Screen checks|Packer19 components|Screen-negative events against full-verifier replay|Completed problems missed|0 / 1488 events|Screening-delay check, separately from independent FP64 output checks|S5:5.6
Release agreement|Packer19 components|LM and DC|Release decisions; consumer TV difference|Release decisions agree; TV=0|Same transition workload and verifier|S5:5.6
Actual-output FP64|Competitive MetroPT-3 study|FP64 marginals of released potentials against 1e−3|Pass count; maximum residual; output agreement|96/96 method–problem checks pass; maximum 9.5e−4; potentials agree bitwise across methods within each batch|16 targets share one source; first timed-run outputs replayed after timing|S5:5.6
Precision stress|Independent near-threshold/runtime stress test|Raw FP32, TF32 and guard against FP64 replay|False accepts|FP32=3; TF32=3; guard=0|84 near-threshold + 16 runtime cases; 1/2/4/8 GPUs; guard excluded from primary application timing|A:A.6
Execution strategy|Competitive MetroPT-3 study|Indexed, entry skip and DC|Relative runtime differences|All below 0.1%|Same input groups and reused buffers; not a statistical equivalence result|S5:5.7
Model ablation|MetroPT-3, 3 transferred groups|Width lookup and linear αa+β, each against actual time|Mean absolute percentage error|0.853% vs 1.05%|36 method–repeat records; same calibration; only the update-cost term changes|S5:5.7
Model direction|MetroPT-3, post hoc|Predicted versus measured directions of Indexed/DC and entry-skip/DC ratios|Direction agreements|Paired medians 6/6; individual repeats 23/24; all effects <0.1%|3 transferred groups × 2 contrasts; no additional input coverage|A:A.7
Completion trajectories|Competitive MetroPT-3, four width-four groups|Targets 0–3, 4–7, 8–11, 12–15|Per-problem completion iterations|Respectively (356,312,320,272), (140,32,32,32), (28,32,100,172), (288,336,328,348)|Shared source; targets can contain overlapping sensor observations; these are not timing-repeat counts|A:A.7
Earlier scheduling|MetroPT-3, W=16, four-cycle graph blocks|Immediate DC, graph replay, bucketed execution|Steady-state solver time|8.43, 8.42, 9.24 s|Same prepared inputs; excludes compile/graph capture/calibration|A:A.7
Illustrated update trajectory|ImageNet-32, Figure 1b, W=4|Hypothetical fixed width versus observed active trajectory|Completion iterations; update areas|nt=(130,75,90,70); fixed 520; active 365; R=155|One recorded window; update counts, not a time ratio|F1
Wave estimate|Synthetic width study, n=1024/4096/16384|bm×SM/n, bm=64, SM=108|Wave-width estimate with one block per SM|6.75, 1.69, 0.42|Theoretical estimates, not measured speedups; all measured curve points follow below|S5:5.3
Width-curve observations|Synthetic width study, n=1024/4096/16384|Different active widths|Step locations|n1024: approximately flat at 1–6, jump at 6→7; n4096: first large jump at 1→2; n16384: responds from width 1|Same synthetic configuration; application kernels require their own timing calibration|S5:5.3
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
    return "; ".join(link(FILES[tag.split(':')[0]], tag) for tag in tags.split('+'))


def fmt(value):
    return f"{value:.3g}"


def build():
    rows = []
    for line in STATIC.strip().splitlines():
        fields = line.split('|')
        assert len(fields) == 7, line
        fields[-1] = "Current manuscript: " + source(fields[-1])
        rows.append(fields)
    review = json.loads((HERE / 'review_data.json').read_text(encoding='utf-8'))
    comp = json.loads((HERE / 'competitive_data.json').read_text(encoding='utf-8'))
    spec = json.loads((HERE / 'figure_spec.json').read_text(encoding='utf-8'))
    review_source = link('support/figure_materials/review_data.json', 'Frozen data: review_data.json')
    comp_source = link('support/figure_materials/competitive_data.json', 'Reanalysis: competitive_data.json')
    # Quality: one comparison per metric/NFE, not a separate result for each arm.
    for metric, name in [('curvature_mean', 'Curvature'),
                         ('random_projection_frechet_diagonal', 'Projected Fréchet'),
                         ('heldout_strict_coupling_fm_mse', 'FM MSE')]:
        for nfe in ([4] if name == 'FM MSE' else [4, 8, 16]):
            values = [next(x for x in review['quality'] if x['metric'] == metric and
                           x['nfe'] == nfe and x['execution'] == arm) for arm in ('Fixed', 'Compacted')]
            result = ' → '.join(f"{fmt(x['mean'])} ± {fmt(x['sample_sd'])}" for x in values)
            rows.append(['Training quality', 'ImageNet-32 PCA500; ' + ('NFE-independent' if name == 'FM MSE' else f'NFE={nfe}'),
                         'Fixed → DC, lower is better', name, result,
                         '3 paired seeds; mean ± sample SD; definitions in A.2; feature-space metrics, not pixel-space FID',
                         review_source + f' : quality/{metric}/{nfe}; ' + link('figures/FIG-quality.tex', 'Table 4')])
    for x in comp['training_times']:
        rows.append(['Training by seed', f"ImageNet-32 seed={x['seed']}", 'Fixed → DC', 'E3 full-training time; paired saving',
                     f"{fmt(x['fixed_total_seconds'])} → {fmt(x['active_total_seconds'])} s; saving {fmt(x['saved_seconds'])} s",
                     '50000 updates; 6250 solves; savings subtract unrounded times', comp_source + ': training_times; A.2'])
    # Table 8 and diagnostic values are displayed in the manuscript by seed.
    for seed, baseline, dc, ratio, diagnostic, counts in zip(
            [20260891, 20260892, 20260893], [123, 124, 119], [117, 116, 115],
            ['1.06', '1.07', '1.03'], ['1.16', '1.08', '1.08'], ['64/52', '64/56', '64/56']):
        rows.append(['Training by seed', f'ImageNet-32 seed={seed}', 'Fixed → DC', 'E1 solver time; Fixed/DC',
                     f'{baseline} → {dc} s; {ratio}×', 'Cumulative solver time within one training seed',
                     'Current manuscript: ' + link('figures/FIG-seeds.tex', 'Table 8')])
        rows.append(['Coupling diagnostic', f'ImageNet-32 seed={seed}', 'Fixed / DC', 'Separate coupling-preparation ratio; updates',
                     f'{diagnostic}×; {counts}', 'Separate from whole-training E1/E3', 'Current manuscript: ' + source('A:A.2')])
    for x in comp['cells']:
        low, high = x['error_percent']
        rows.append(['Execution and model', f"MetroPT-3 targets {x['offset']}–{x['offset']+x['width']-1}, W={x['width']}",
                     'Indexed / entry skip / DC; model against actual time', 'Continuous E1 median; signed error range',
                     ' / '.join(fmt(x['seconds'][m]) for m in ('active_index','entry_skip','physical_compaction')) +
                     f' s; +{fmt(low)}% to +{fmt(high)}%',
                     ('Target-group transfer' if x['target_heldout'] else 'Same input, separate calibration runs') + '; 4 orders; shared source',
                     comp_source + f": cells offset={x['offset']},W={x['width']}; Table 7"])
    for world, x in comp['guarded_stress']['by_world_size'].items():
        rows.append(['Precision stress by GPU count', f'{world} GPUs', 'Guard release versus FP64 replay release',
                     'Accepted candidates among 21 near-threshold cases',
                     f"{x['outward_releases']} vs {x['fp64_replay_releases']}",
                     'The guard can reject candidates accepted by replay; acceptance sets differ', comp_source + f': guarded_stress/by_world_size/{world}; A.6'])
    with (HERE / 'PACKER19_STOPPING_METRICS.csv').open(encoding='utf-8-sig', newline='') as f:
        stopping = list(csv.DictReader(f))
    assert len(stopping) == 5
    for x in stopping:
        v = {k: float(z) for k,z in x.items()}
        lo, hi = (100*(v[k]-1) for k in ('lm_over_pc_ci_low','lm_over_pc_ci_high'))
        rows.append(['Figure 3: all points', f"Packer19 τ={fmt(v['tolerance'])}", 'LM / DC; consumer against the τ=1e−6 reference',
                     'E1 ratio; 95% CI; max residual; max TV',
                     f"{fmt(v['lm_over_pc'])}×; 100(S−1) CI [{fmt(lo)},{fmt(hi)}]% ; residual={fmt(v['max_actual_residual'])}; TV={fmt(v['max_consumer_tv'])}",
                     '24 pairs per τ; equal-host stratified bootstrap; separate stopping campaign',
                     link('support/figure_materials/PACKER19_STOPPING_METRICS.csv', 'Frozen CSV') + f": tolerance={x['tolerance']}; Figure 3"])
    width_count = 0
    for n, points in spec['width']['data'].items():
        for a, x in sorted(points.items(), key=lambda p:int(p[0])):
            width_count += 1
            rows.append(['Figure 2: all points', f'Synthetic tensors n={n}, active width={a}', 'Active widths at fixed n; no application baseline',
                         'Time for two update kernels, median [Q1,Q3]',
                         f"{fmt(1000*x['median'])} [{fmt(1000*x['q1'])},{fmt(1000*x['q3'])}] ms",
                         f"{x['count']} calls; A100; d=500, column tile=64, cost scale=1; IQR, not CI",
                         link('support/figure_materials/figure_spec.json', 'Machine timing summary') + f': width/data/{n}/{a}; Figure 2'])
    windows = 0
    for x in review['widths']:
        w = x['width']
        rows.append(['Figure 4: summary curves', f'ImageNet-32 n=4096, W={w}', 'Sequential projected carry / shared-init active',
                     'Mean padding; steady-state time ratio; time ratio including startup',
                     f"{fmt(x['mean_padding_ratio'])}; {fmt(x['steady_speedup'])}×; {fmt(x['deployment_speedup'])}×",
                     '40 windows/width; 8-worker critical path; complete-configuration benefit, not a single-component DC effect',
                     review_source + f': widths/W={w}; Figure 4'])
        for i, window in enumerate(x['windows']):
            windows += 1
            nt = window['completion_iterations']
            fixed, active = w*max(nt), sum(nt)
            rows.append(['Figure 4: all scatter points', f"W={w}; seed={window['seed']}; start={window['start_frame']}",
                         'Hypothetical fixed-width work / executed active work within this active run',
                         'Problem updates and padding ratio', f'{fixed} / {active} = {fmt(window["padding_ratio"])}',
                         'One window; nt=(' + ','.join(map(str,nt)) + '); not a measured time ratio',
                         review_source + f': widths/W={w}/windows/{i}; Figure 4a'])
    assert windows == 200
    assert width_count == sum(len(v) for v in spec['width']['data'].values())
    assert all(len(row) == 7 for row in rows)
    intro = f'''# Complete Experimental Results Comparison Table (Standalone)

Based on English manuscript commit **e5222fa** (2026-09-09). This table is a standalone companion: it is not referenced by `main.tex` and does not enter the manuscript or appendix PDF.

The **{len(rows)} rows** consolidate results from the main text, appendix and result tables, including all {width_count} statistical points in Figure 2, all 5 tolerance points in Figure 3, and the 5 summary groups and 200 scatter points in Figure 4. The recorded trajectory in Figure 1 is also listed. Tables 1 and 11 specify configurations; their settings accompany the relevant results rather than adding result rows. Theory equations, hyperparameters, external literature results and unused historical macros are outside this experimental inventory.

Definitions: Fixed retains the original batch width; LM is this study's control that freezes completed state after full-width updates; DC physically compacts state; Indexed narrows the active-ID launch grid; entry skip bypasses inactive computation in the original layout. Each time ratio specifies its numerator and denominator: **a ratio above 1 means the denominator is faster**. `A → B` lists the two measured values and does not by itself establish single-component attribution. E1=solver, E2=solver plus consumer, E3=full training or task. Campaigns, initializations, allocation policies and statistical units remain separate.

Rows marked “Current manuscript” transcribe the cited source text. Rows marked “Frozen data” or “Reanalysis” read the repository's existing JSON/CSV records. The [review disposition](support/audits/REVIEW_DISPOSITION.md) and source fields in those records provide the evidence chain. Missing absolute times remain unreported. Displayed values generally use three significant digits, with scientific notation for small quantities; source files retain full precision. Narrow confidence intervals use 100(S−1)% to retain their resolution. Null results, slowdowns, additional memory costs and false accepts are included.

Local regeneration and consistency check: `python support/figure_materials/build_results_inventory.py --check`. This inventory organizes existing results; it adds no experiments and does not constitute final scientific approval by the authors.

| No. | Result category | Task and configuration | Compared methods / direction | Metric | Result | Statistical unit and scope | Source |
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
