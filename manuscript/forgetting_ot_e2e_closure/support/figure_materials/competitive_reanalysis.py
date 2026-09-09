"""Reconcile frozen records and render the competitive-controls table (CPU only)."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import sys

sys.dont_write_bytecode = True
METHODS = ("active_index", "entry_skip", "physical_compaction")


def build(root):
    sources = {}

    def read(relative):
        data = (root / relative).read_bytes()
        sources[relative] = hashlib.sha256(data).hexdigest()
        return json.loads(data)

    code = root / "studies/code/analyze_compaction_competitive_controls.py"
    spec = importlib.util.spec_from_file_location("competitive_analysis", code)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sources[str(code.relative_to(root))] = hashlib.sha256(code.read_bytes()).hexdigest()
    prefix = "studies/campaigns/EXP_Compaction_Competitive_Controls_20260908/raw/"
    calibrations = {w: read(prefix + f"metro_n16384_w{w}_offset0.json") for w in (4, 8)}
    cells = []
    residuals = []
    decisions = []
    linear_comparisons = []
    for width, offset in ((4, 0), (4, 4), (4, 8), (4, 12), (8, 0)):
        name = f"metro_n16384_w{width}_offset{offset}"
        packet = read(prefix + name + ".json")
        result = module.analyze(packet, calibrations[width])
        suffix = "_heldout_analysis.json" if offset else "_analysis.json"
        assert result == read(prefix + name + suffix), name
        assert result["evidence_eligible"]
        if result["model"]["input_heldout"]:
            for method in METHODS:
                calibration_rows = [r for r in calibrations[width]["width_calibration"] if r["method"] == method]
                widths = sorted({r["active"] for r in calibration_rows})
                costs = {a: statistics.median(r["update_seconds"] for r in calibration_rows if r["active"] == a) for a in widths}
                xmean, ymean = statistics.mean(widths), statistics.mean(costs.values())
                alpha = sum((a - xmean) * (costs[a] - ymean) for a in widths) / sum((a - xmean) ** 2 for a in widths)
                beta = ymean - alpha * xmean
                residual = [costs[a] - alpha * a - beta for a in widths]
                assert abs(sum(residual)) < 1e-10
                assert abs(sum(a * r for a, r in zip(widths, residual))) < 1e-10
                assert all(alpha * a + beta > 0 for a in widths)
                predictions = {r["repeat"]: r for r in result["model"]["methods"][method]}
                for run in (r for r in packet["runs"] if r["method"] == method):
                    trajectory = [t["active_width"] for t in run["trace"]]
                    assert sum(trajectory) == sum(run["depths"])
                    assert len(trajectory) == max(run["depths"])
                    full = predictions[run["repeat"]]["estimated_seconds"]
                    control = full - sum(costs[a] for a in trajectory)
                    simple = control + alpha * sum(trajectory) + beta * len(trajectory)
                    linear_comparisons.append({"offset": offset, "method": method, "repeat": run["repeat"],
                        "alpha": alpha, "beta": beta, "calibration_widths": widths,
                        "calibration_update_seconds": [costs[a] for a in widths],
                        "control_seconds": control, "observed_seconds": run["solver_seconds"],
                        "lookup_seconds": full, "linear_seconds": simple,
                        "lookup_error_percent": 100 * (full / run["solver_seconds"] - 1),
                        "linear_error_percent": 100 * (simple / run["solver_seconds"] - 1)})
        errors = [100 * p["relative_error"] for m in METHODS for p in result["model"]["methods"][m]]
        if result["model"]["input_heldout"]:
            pc = {r["repeat"]: r for r in result["model"]["methods"]["physical_compaction"]}
            for method in METHODS[:2]:
                estimated, measured = [], []
                for row in result["model"]["methods"][method]:
                    reference = pc[row["repeat"]]
                    estimated.append(row["estimated_seconds"] / reference["estimated_seconds"])
                    measured.append(row["actual_seconds"] / reference["actual_seconds"])
                decisions.append({"offset": offset, "control": method,
                                  "estimated_ratios": estimated, "measured_ratios": measured,
                                  "median_direction_agrees": (statistics.median(estimated) > 1) == (statistics.median(measured) > 1),
                                  "repeat_directions_agree": sum((a > 1) == (b > 1) for a, b in zip(estimated, measured))})
        for method in result["methods"].values():
            for row in method["fp64"]:
                assert row["passes_external_tolerance"]
                residuals.extend((row["row_l1_fp64"], row["column_l1_fp64"]))
        cells.append({"width": width, "offset": offset,
                      "seconds": {m: result["methods"][m]["solver_seconds_median"] for m in METHODS},
                      "error_percent": [min(errors), max(errors)],
                      "target_heldout": result["model"]["input_heldout"],
                      "paired_ratios": result["primary_contrasts"],
                      "source": prefix + name + suffix})
    old = read("studies/local_results/FLASH_COMPACTION_SCHEDULER_METROPT3_20260908_A100/raw_results.json")
    assert old["data"]["npz_sha256"] == calibrations[4]["provenance"]["data_sha256"]
    keops = read("studies/campaigns/EXP_KeOps_Check_Interval_20260908/analysis/summary.json")
    assert keops["paired_records"] == 18 and keops["timed_arms"] == 54
    assert keops["all_residual_checks_pass"]
    for group in keops["across_seeds"]:
        for key in ("static_padded_over_active_T_total", "masked_batch_over_active_T_total"):
            values = [r[key] for r in keops["seed_medians"] if r["n"] == group["n"]]
            assert statistics.mean(values) == group[key]["mean_seed_median"]
    stress = read("studies/raw_results/server_runs/20260808_p4_finite_precision_8gpu_multinode/analysis.json")
    assert stress["aggregate"]["raw_fp32_false_accepts"] == 3
    assert stress["aggregate"]["raw_tf32_false_accepts"] == 3
    assert stress["aggregate"]["production_false_accepts"] == 0
    training = read("studies/campaigns/C63_semantic_latent_OTFM_feature_training/analysis.json")
    assert len(linear_comparisons) == 36
    training_times = []
    for row in training["summary"]["raw_rows"]:
        fixed, active = (row["methods"][m] for m in ("project_cold_static", "project_cold_active"))
        assert fixed["steps"] == active["steps"] == 50000
        assert fixed["windows"] == active["windows"] == 6250
        training_times.append({"seed": row["seed"], "fixed_total_seconds": fixed["total_seconds"],
                               "active_total_seconds": active["total_seconds"],
                               "saved_seconds": fixed["total_seconds"] - active["total_seconds"],
                               "windows": active["windows"], "steps": active["steps"]})
    return {"verification": "agent CPU reconciliation; human author review pending",
            "sources_sha256": sources, "cells": cells,
            "heldout_ordering": decisions,
            "linear_model_comparison": {"fit": "unweighted OLS on per-width calibration medians; update term only; identical control costs",
                "rows": linear_comparisons,
                "lookup_mean_absolute_error_percent": statistics.mean(abs(r["lookup_error_percent"]) for r in linear_comparisons),
                "linear_mean_absolute_error_percent": statistics.mean(abs(r["linear_error_percent"]) for r in linear_comparisons)},
            "training_times": training_times,
            "guarded_stress": {"aggregate": stress["aggregate"], "by_world_size": stress["by_world_size"]},
            "fp64_method_problem_checks": len(residuals) // 2,
            "fp64_max_residual": max(residuals),
            "same_prepared_input_as_scheduler": True,
            "keops_across_seeds": keops["across_seeds"]}


def render(data):
    lines = [r"% Generated by support/figure_materials/competitive_reanalysis.py.",
             r"\begin{table*}[!t]", r"\centering",
             r"\caption{MetroPT-3 compute-skipping controls and conditional runtime reconstruction on one A100. Times are median continuous solver wall times over four cyclic orders, in seconds. Error ranges span three methods and four repeats and use $100(\widehat T/T-1)$. Calibration uses targets 0--3 at $W=4$ and 0--7 at $W=8$ in separate runs. Transfer rows hold the target group out of calibration; all groups share one source.}",
             r"\label{tab:execution-controls}", r"\small",
             r"\setlength{\tabcolsep}{7pt}", r"\renewcommand{\arraystretch}{1.15}",
             r"\begin{tabular}{@{}lrrrrll@{}}", r"\toprule",
             r"Targets & $W$ & Indexed (s) & Entry skip (s) & DC (s) & Error (\%) & Calibration use \\",
             r"\midrule"]
    for row in data["cells"]:
        label = f'{row["offset"]}--{row["offset"] + row["width"] - 1}'
        times = " & ".join(f'{row["seconds"][m]:#.3g}' for m in METHODS)
        low, high = row["error_percent"]
        kind = "Target-group transfer" if row["target_heldout"] else "Same input, separate runs"
        lines.append(f'{label} & {row["width"]} & {times} & $+{low:.3g}$--$+{high:.3g}$ & {kind} ' + r"\\")
    lines.extend((r"\bottomrule", r"\end{tabular}", r"\end{table*}"))
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build(args.evidence_root)
    here = Path(__file__).resolve().parent
    outputs = {here / "competitive_data.json": json.dumps(data, indent=2) + "\n",
               here.parent.parent / "figures/FIG-controls.tex": render(data)}
    for path, text in outputs.items():
        if args.check:
            assert path.read_text(encoding="utf-8") == text, path
        else:
            path.write_text(text, encoding="utf-8", newline="\n")
    print("PASS: five reconstructions, 36 matched linear-model comparisons, three training totals, paired controls, input reuse, FP64 and PyKeOps checks")


if __name__ == "__main__":
    main()
