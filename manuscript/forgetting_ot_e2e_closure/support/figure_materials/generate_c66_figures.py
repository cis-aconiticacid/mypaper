#!/usr/bin/env python3
"""Generate C66 publication figures and machine-readable summaries.

The only data input is the C66 companion telemetry JSON. Missing telemetry is
reported explicitly and never replaced by an inferred value.
"""
import argparse, csv, hashlib, json, statistics
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Figure requirements: vector PDF; no in-plot title; colorblind-safe palette;
# self-contained captions; no interpolation when telemetry is unavailable.
FIGURE_REQUIREMENTS = {"format": "pdf", "title": False, "palette": "colorblind-safe", "fail_closed": True}

ARMS = ["official", "ls", "la", "cs", "ca"]
LABELS = {"official":"Official", "ls":"LS", "la":"LA", "cs":"CS", "ca":"CA"}
COLORS = {"official":"#4C566A", "ls":"#D55E00", "la":"#E69F00", "cs":"#0072B2", "ca":"#009E73"}
WORKLOAD_LABELS = {"metropt": "MetroPT", "packer19": "Packer19"}
WORKLOAD_SLUGS = {"metropt": "metro", "packer19": "packer"}

def style():
    matplotlib.rcParams.update({"font.size":9, "font.family":"serif", "axes.labelsize":9,
        "xtick.labelsize":8, "ytick.labelsize":8, "legend.fontsize":8,
        "figure.dpi":300, "savefig.dpi":300, "savefig.bbox":"tight",
        "savefig.pad_inches":0.04, "axes.spines.top":False, "axes.spines.right":False,
        "axes.grid":False, "text.usetex":False, "mathtext.fontset":"stix"})

def write_csv(path, rows, fields):
    with path.open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(rows)

def sha256_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""): h.update(block)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source", type=Path, required=True); ap.add_argument("--out", type=Path, required=True); a=ap.parse_args()
    d=json.loads(a.source.read_text()); a.out.mkdir(parents=True, exist_ok=True); style()
    workload=d.get("workload")
    if workload not in WORKLOAD_LABELS:
        raise ValueError(f"unsupported C66 workload: {workload!r}")
    workload_label=WORKLOAD_LABELS[workload]
    workload_slug=WORKLOAD_SLUGS[workload]
    arms=d["arms"]
    gaps=[]
    # Endpoint, slots, and energy are emitted observation-by-observation.
    endpoint=[]; slots=[]; energy=[]; width_traces=[]; release_depths=[]
    for arm in ARMS:
        x=arms[arm]
        for o in x["observations"]:
            ep=o.get("endpoint_wall",{})
            if ep.get("available"):
                endpoint.append({"arm":arm,"label":LABELS[arm],"seed":o["seed"],"gpu":o["gpu"],"repeat":o["repeat"],"endpoint_wall_seconds":ep["value"]})
            else:
                gaps.append(f"{arm}: one endpoint observation unavailable ({ep.get('reason','unspecified')}).")
            e=o.get("gpu_energy",{}); 
            if e.get("available"):
                energy.append({"arm":arm,"label":LABELS[arm],"seed":o["seed"],"gpu":o["gpu"],"repeat":o["repeat"],"gpu_energy_joules":e["value"],"endpoint_wall_seconds":ep.get("value") if ep.get("available") else None,"joules_per_window_second":e["value"]/ep["value"] if ep.get("available") else None})
            c=o.get("candidate_slots",{});
            if c.get("available"): slots.append({"arm":arm,"label":LABELS[arm],"seed":o["seed"],"gpu":o["gpu"],"repeat":o["repeat"],"candidate_slots":c["value"]})
        # Use only explicit aggregate values for the compact machine-readable summary.
        m=x["metrics"]
        for k in ("candidate_slots","endpoint_wall_seconds","gpu_energy_joules"):
            if not m[k].get("available"): gaps.append(f"{arm}: {k} unavailable ({m[k].get('reason','unspecified')}).")
        for key in ("active_width_trace","production_release_depth"):
            if not x[key].get("available"):
                gaps.append(f"{arm}: {key} unavailable ({x[key].get('reason','unspecified')}).")
        if x["D_s"].get("available") is not True: gaps.append(f"{arm}: D_s unavailable ({x['D_s'].get('reason','unspecified')}); no D_s distribution plotted.")
        for o in x["observations"]:
            aw=o.get("active_width_trace",{}); rd=o.get("production_release_depth",{})
            if aw.get("available"):
                for i,w in enumerate(aw["value"]): width_traces.append({"arm":arm,"label":LABELS[arm],"seed":o["seed"],"gpu":o["gpu"],"repeat":o["repeat"],"iteration":i,"active_width_lanes":w})
            if rd.get("available"):
                zvals=rd["value"]["values"] if isinstance(rd["value"],dict) else rd["value"]
                for i,z in enumerate(zvals): release_depths.append({"arm":arm,"label":LABELS[arm],"seed":o["seed"],"gpu":o["gpu"],"repeat":o["repeat"],"candidate_index":i,"production_release_ell_s":z})
    write_csv(a.out/"endpoint_observations.csv",endpoint,list(endpoint[0]))
    write_csv(a.out/"candidate_slots_observations.csv",slots,list(slots[0]) if slots else ["arm","label","seed","gpu","repeat","candidate_slots"])
    write_csv(a.out/"energy_observations.csv",energy,list(energy[0]))
    write_csv(a.out/"active_width_observations.csv",width_traces,list(width_traces[0]) if width_traces else ["arm","label","seed","gpu","repeat","iteration","active_width_lanes"])
    write_csv(a.out/"production_release_depth_observations.csv",release_depths,list(release_depths[0]) if release_depths else ["arm","label","seed","gpu","repeat","candidate_index","production_release_ell_s"])
    summary={"source":str(a.source),"source_sha256":sha256_file(a.source),"schema":d.get("schema"),"status":d.get("status"),"workload":workload,"workload_label":workload_label,"arms":{},"gaps":gaps}
    for arm in ARMS:
        m=arms[arm]["metrics"]; ep=m["endpoint_wall_seconds"].get("value",{}).get("p50"); en=m["gpu_energy_joules"].get("value",{}).get("p50"); arm_power=[r["joules_per_window_second"] for r in energy if r["arm"]==arm and r["joules_per_window_second"] is not None]; summary["arms"][arm]={"label":LABELS[arm],"endpoint_wall_seconds_p50":ep,"gpu_energy_joules_p50":en,"median_observation_energy_per_endpoint_watts":statistics.median(arm_power) if arm_power else None,"candidate_slots_p50":m["candidate_slots"].get("value",{}).get("p50") if m["candidate_slots"].get("available") else None}
    (a.out/f"c66_{workload_slug}_figure_data.json").write_text(json.dumps(summary,indent=2)+"\n")
    (a.out/"DATA_GAPS.md").write_text(f"# C66 {workload_label} figure data gaps\n\n"+"\n".join("- "+g for g in gaps)+"\n")
    # Fig 1: endpoint wall time, all requested arms.
    fig,ax=plt.subplots(figsize=(4.8,2.8)); vals=[summary["arms"][k]["endpoint_wall_seconds_p50"] for k in ARMS]; ax.bar(range(5),vals,color=[COLORS[k] for k in ARMS]); ax.set_xticks(range(5),[LABELS[k] for k in ARMS]); ax.set_ylabel("Endpoint wall time (s)"); ax.set_ylim(0,max(vals)*1.16); fig.savefig(a.out/"fig_c66_endpoint.pdf"); plt.close(fig)
    # Fig 2: problem-update slots, only observed arms (official is fail-closed gap).
    fig,ax=plt.subplots(figsize=(4.8,2.8)); ks=[k for k in ARMS if summary["arms"][k]["candidate_slots_p50"] is not None]; vv=[summary["arms"][k]["candidate_slots_p50"] for k in ks]; ax.bar(range(len(ks)),vv,color=[COLORS[k] for k in ks]); ax.set_xticks(range(len(ks)),[LABELS[k] for k in ks]); ax.set_ylabel("Problem-update slots (p50)"); fig.savefig(a.out/"fig_c66_candidate_slots.pdf"); plt.close(fig)
    # Fig 3: active width and production release ell_s distributions by observation.
    if width_traces and release_depths:
        by_width={k:[] for k in ["ca","la"]}; by_depth={k:[] for k in ["ca","la"]}
        for r in width_traces: by_width[r["arm"]].append(r["active_width_lanes"])
        for r in release_depths: by_depth[r["arm"]].append(r["production_release_ell_s"])
        fig,ax=plt.subplots(1,2,figsize=(7.6,2.8),constrained_layout=True);
        ax[0].boxplot([by_width[k] for k in by_width], tick_labels=[LABELS[k] for k in by_width], patch_artist=True, boxprops=dict(facecolor="#D9D9D9")); ax[0].set_ylabel("Active width (lanes)")
        ax[1].boxplot([by_depth[k] for k in by_depth], tick_labels=[LABELS[k] for k in by_depth], patch_artist=True, boxprops=dict(facecolor="#D9D9D9")); ax[1].set_ylabel("Production release $\\ell_s$ (iterations)")
        fig.savefig(a.out/"fig_c66_active_release_distributions.pdf"); plt.close(fig)
    else: gaps.append("No active-width + production release observations available; distribution figure omitted.")
    # Fig 4: endpoint wall and GPU joules, all arms (official slots remain unavailable separately).
    fig,ax=plt.subplots(1,3,figsize=(9.2,2.7),constrained_layout=True);
    for j,(key,ylabel) in enumerate([("endpoint_wall_seconds_p50","Endpoint wall time (s)"),("gpu_energy_joules_p50","GPU energy (J)"),("median_observation_energy_per_endpoint_watts","Median per-observation energy / endpoint (W)")]):
        vals=[summary["arms"][k][key] for k in ARMS]
        ax[j].bar(range(5),vals,color=[COLORS[k] for k in ARMS]); ax[j].set_xticks(range(5),[LABELS[k] for k in ARMS]); ax[j].set_ylabel(ylabel)
    fig.savefig(a.out/"fig_c66_wall_gpu_energy.pdf"); plt.close(fig)
    # Captions are self-contained and explicitly preserve missing-data semantics.
    tex=f'''% C66 {workload_label} figures (C66-only; source telemetry is recorded in CSV/JSON).\n'''
    tex+=f'''\\begin{{figure}}[t]\\centering\\includegraphics[width=.48\\linewidth]{{fig_c66_endpoint.pdf}}\\caption{{C66 {workload_label} endpoint wall time (median over 36 seed--GPU--repeat observations). Official is the public Flash API; LS/LA are legacy static/active execution; CS/CA are current static/active execution. The endpoint is the registered ready-arrays-to-consumer window.}}\\label{{fig:c66-{workload_slug}-endpoint}}\\end{{figure}}\n'''
    tex+=f'''\\begin{{figure}}[t]\\centering\\includegraphics[width=.48\\linewidth]{{fig_c66_candidate_slots.pdf}}\\caption{{C66 {workload_label} candidate-iteration slots (median over observed repeats) for legacy static/active (LS/LA) and current static/active (CS/CA) execution. Official slots are not exposed by the public API and are intentionally omitted (see DATA_GAPS.md).}}\\label{{fig:c66-{workload_slug}-slots}}\\end{{figure}}\n'''
    tex+=f'''\\begin{{figure}}[t]\\centering\\includegraphics[width=.72\\linewidth]{{fig_c66_active_release_distributions.pdf}}\\caption{{C66 {workload_label} active width over recorded correction cycles (left) and production release $\\ell_s$ over problem instances (right) for CA and LA. LA and CA share the same recorded schedule/release profile; their implementation-generation difference appears in timing rather than these counts. Production $\\ell_s$ is not $D_s$; an independent $D_s$ profile was not supplied.}}\\label{{fig:c66-{workload_slug}-release}}\\end{{figure}}\n'''
    tex+=f'''\\begin{{figure}}[t]\\centering\\includegraphics[width=.95\\linewidth]{{fig_c66_wall_gpu_energy.pdf}}\\caption{{C66 {workload_label} endpoint wall time, measured GPU energy per window, and median per-observation energy divided by endpoint wall time (medians over 36 observations per arm). The endpoint is the registered ready-arrays-to-consumer window; the third panel is a median ratio, not median energy divided by median endpoint.}}\\label{{fig:c66-{workload_slug}-energy}}\\end{{figure}}\n'''
    (a.out/"latex_includes.tex").write_text(tex)
    rows = ["\\begin{table}[t]\\centering", f"\\caption{{C66 {workload_label} endpoint and GPU-energy medians over 36 observations per arm. Official problem-update slots are unavailable from its public API and are shown as --.}}", f"\\label{{tab:c66-{workload_slug}-endpoint-energy}}", "\\begin{tabular}{lrrr}\\toprule", "Arm & Endpoint (s) & GPU energy (J) & Problem-update slots \\\\\\midrule"]
    for arm in ARMS:
        s=summary["arms"][arm]; slot="--" if s["candidate_slots_p50"] is None else f"{s['candidate_slots_p50']:.0f}"
        rows.append(f"{LABELS[arm]} & {s['endpoint_wall_seconds_p50']:.3f} & {s['gpu_energy_joules_p50']:.1f} & {slot} \\\\")
    rows += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    (a.out/"TABLE_c66_endpoint_energy.tex").write_text("\n".join(rows))
    # Rewrite gaps after any late omission was added.
    (a.out/"DATA_GAPS.md").write_text(f"# C66 {workload_label} figure data gaps\n\n"+"\n".join("- "+g for g in gaps)+"\n")
if __name__ == "__main__": main()
