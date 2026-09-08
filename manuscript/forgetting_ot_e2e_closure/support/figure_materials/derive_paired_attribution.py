"""Supplementary descriptive reanalysis of frozen timing records (no new runs)."""
import csv
import hashlib
import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
C63 = ROOT / 'studies/campaigns/C63_semantic_latent_OTFM_feature_training/analysis.json'

def gm(values):
    assert values and all(math.isfinite(x) and x > 0 for x in values)
    return math.exp(statistics.fmean(map(math.log, values)))

def write_csv(name, rows):
    with (HERE / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def main():
    summary = json.loads(C63.read_text(encoding='utf-8'))['summary']
    crows = []
    for row in sorted(summary['raw_rows'], key=lambda r: r['seed']):
        methods = row['methods']
        s = methods['project_cold_static']['solver_seconds']
        a = methods['project_cold_active']['solver_seconds']
        crows.append(dict(seed=row['seed'], static_solver_seconds=s, active_solver_seconds=a, static_over_active=s/a))
    assert [r['seed'] for r in crows] == summary['seeds']
    write_csv('C63_SOLVER_ATTRIBUTION.csv', crows)
    ratios = [r['static_over_active'] for r in crows]
    result = dict(analysis_kind='supplementary descriptive paired reanalysis; no new runs or confidence intervals',
        c63=dict(by_seed=crows, geometric_mean=gm(ratios), observed_range=[min(ratios),max(ratios)]),
        sources={str(C63.relative_to(ROOT)): hashlib.sha256(C63.read_bytes()).hexdigest()})
    (HERE / 'PAIRED_ATTRIBUTION.json').write_bytes((json.dumps(result, indent=2)+'\n').encode('utf-8'))
    print(json.dumps(result['c63'], indent=2))

if __name__ == '__main__':
    main()
