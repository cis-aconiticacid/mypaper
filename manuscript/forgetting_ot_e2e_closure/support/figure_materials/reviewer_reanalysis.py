"""Read-only reanalysis of frozen training and width data; prints a JSON packet.

Usage: python reviewer_reanalysis.py --evidence-root PATH
No GPU runs. Standard deviations use ddof=1 across three training seeds.
Width padding is W * max(n_t) / sum(n_t), evaluated per recorded window.
"""
import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean, stdev


def analyze(root):
    quality_source = Path('studies/campaigns/C63_semantic_latent_OTFM_feature_training/analysis.json')
    training = json.loads((root / quality_source).read_text(encoding='utf-8'))['summary']
    quality = []
    for metric in ('curvature_mean', 'random_projection_frechet_diagonal', 'heldout_strict_coupling_fm_mse'):
        for arm in ('project_cold_static', 'project_cold_active'):
            for nfe in ('4', '8', '16'):
                values = [r['methods'][arm]['fixed_update_evaluation_by_nfe'][nfe][metric] for r in training['raw_rows']]
                frozen = training['quality_by_nfe'][nfe][metric][arm]
                assert len(values) == 3
                assert math.isclose(mean(values), frozen['mean'], rel_tol=1e-10)
                assert math.isclose(stdev(values), frozen['sample_std'], rel_tol=1e-10)
                quality.append(dict(metric=metric, execution='Fixed' if arm.endswith('static') else 'Compacted',
                                    nfe=int(nfe), values=values, mean=mean(values), sample_sd=stdev(values)))
    width_source = Path('studies/raw_results/server_runs/20260824_c35_imagenet32_width_sweep_04d0f5c')
    with (root / width_source / 'analysis/width_sweep.csv').open(encoding='utf-8-sig', newline='') as stream:
        speed = {int(r['width']): r for r in csv.DictReader(stream)}
    widths = []
    for width in (1, 2, 4, 8, 16):
        windows = []
        for path in sorted((root / width_source / f'w{width}/local-active').glob('node*/results/tasks/*/result.json')):
            run = json.loads(path.read_text(encoding='utf-8'))
            assert run['config']['width'] == width
            for row in run['windows']:
                result = row['result']
                nt = result['iterations']
                assert len(nt) == width and result['all_converged']
                assert sum(nt) == result['candidate_slots'] == sum(result['active_width_trace'])
                windows.append(dict(seed=row['seed'], start_frame=row['start_frame'], completion_iterations=nt,
                                    padding_ratio=width*max(nt)/sum(nt)))
        assert len(windows) == 40
        assert len({(w['seed'], w['start_frame']) for w in windows}) == 40
        r = speed[width]
        assert math.isclose(float(r['steady_speedup']), float(r['baseline_steady_seconds'])/float(r['candidate_steady_seconds']))
        widths.append(dict(width=width, windows=windows, mean_padding_ratio=mean(w['padding_ratio'] for w in windows),
                           steady_speedup=float(r['steady_speedup']), deployment_speedup=float(r['deployment_speedup']),
                           source=str(width_source / 'analysis/width_sweep.csv').replace('\\','/')))
    return dict(kind='descriptive reanalysis of existing frozen records; no new performance runs',
                quality_source=str(quality_source).replace('\\','/'), quality=quality, widths=widths,
                width_comparison='project-adapter sequential projected carry / shared-anchor active execution; full configuration comparison',
                width_hardware='two hosts, eight A100-SXM4-80GB workers; n4096, epsilon0.1, tolerance0.001, check interval5',
                predictor_status='application prediction not computed: available primitive costs have unmatched dimensions, tiles and control costs')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence-root', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(analyze(args.evidence_root), separators=(',', ':')))
