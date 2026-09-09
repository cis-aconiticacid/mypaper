"""Render manuscript figures from frozen summaries; no experimental runs."""
import csv
import io
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]
OUT = PAPER / "figures"
SPEC = json.loads((HERE / "figure_spec.json").read_text(encoding="utf-8"))
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.titlesize": 10, "axes.labelsize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "pdf.fonttype": 42,
    "svg.fonttype": "none", "svg.hashsalt": "drainsinkhorn-paper", "axes.spines.top": False,
    "axes.spines.right": False, "axes.linewidth": .7,
})
BLUE, ORANGE = SPEC["style"]["colors"]

def save(fig, stem):
    OUT.mkdir(parents=True, exist_ok=True)
    for extension in ("pdf", "svg", "png"):
        target = OUT / f"{stem}.{extension}"
        if extension == "svg":
            stream = io.StringIO()
            fig.savefig(stream, format="svg", bbox_inches="tight", metadata={"Date": None})
            text = "\n".join(line.rstrip() for line in stream.getvalue().splitlines()) + "\n"
            target.write_text(text, encoding="utf-8", newline="\n")
        else:
            fig.savefig(target, dpi=200, bbox_inches="tight", metadata=({"CreationDate": None, "ModDate": None} if extension == "pdf" else None))
    plt.close(fig)

fig, axes = plt.subplots(1, 3, figsize=(7.15, 2.9), layout="constrained")
for ax, n, letter in zip(axes, (1024, 4096, 16384), "abc"):
    rows = SPEC["width"]["data"][str(n)]
    widths = sorted(map(int, rows))
    median = np.array([rows[str(a)]["median"] * 1000 for a in widths])
    q1 = np.array([rows[str(a)]["q1"] * 1000 for a in widths])
    q3 = np.array([rows[str(a)]["q3"] * 1000 for a in widths])
    ax.errorbar(widths, median, yerr=[median-q1, q3-median],
                color=BLUE, marker="o", ms=3.5, lw=1.2, capsize=2)
    for W, color in ((8, "#777777"), (16, ORANGE)):
        ax.axvline(W, color=color, linestyle="--", lw=.9)
        ax.text(W-.3, .94, f"W={W}", transform=ax.get_xaxis_transform(),
                ha="right", va="top", fontsize=8, color=color)
    ax.set_title(f"({letter}) n = {n:,}", loc="left")
    ax.set_xlabel("Active batch width")
    ax.set_ylabel("Update time (ms)")
    ax.set_xlim(.5, 16.6)
    ax.set_ylim(bottom=0)
    ax.set_xticks([1, 4, 8, 12, 16])
    ax.grid(axis="y", color="#dddddd", lw=.5)
save(fig, "FIG-width")

with (HERE / "PACKER19_STOPPING_METRICS.csv").open(newline="", encoding="utf-8-sig") as stream:
    rows = [{k: float(v) for k, v in row.items()} for row in csv.DictReader(stream)]
tol = np.array([r["tolerance"] for r in rows])
ratio = np.array([r["lm_over_pc"] for r in rows])
lo = np.array([r["lm_over_pc_ci_low"] for r in rows])
hi = np.array([r["lm_over_pc_ci_high"] for r in rows])
fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.15, 3.0), layout="constrained")
y = np.arange(len(rows))
ax.errorbar(ratio, y, xerr=[ratio-lo, hi-ratio], fmt="o",
            color=BLUE, ms=5, capsize=3, lw=1.2)
ax.set_yticks(y, [r"$10^{-4}$", r"$3\,10^{-4}$", r"$10^{-3}$", r"$3\,10^{-3}$", r"$10^{-2}$"])
ax.invert_yaxis()
ax.set_xlim(.9, 1.83)
ax.axvline(1, color="#777777", linestyle="--", lw=.9)
for yy, value in zip(y, ratio):
    ax.text(value+.035, yy, f"{value:.3g}", va="center", fontsize=8)
ax.set_xlabel("Logical-mask / compacted time")
ax.set_ylabel("Stopping tolerance")
ax.set_title("(a) Runtime", loc="left")
ax.grid(axis="x", color="#dddddd", lw=.5)
bx.loglog(tol, [r["max_actual_residual"] for r in rows], "o-", color=BLUE, label="Marginal residual", ms=4)
bx.loglog(tol, [r["max_consumer_tv"] for r in rows], "s-", color=ORANGE, label="Consumer TV", ms=4)
bx.loglog(tol, tol, "--", color="#777777", lw=.9, label="Residual = tolerance")
bx.set_xlabel("Stopping tolerance")
bx.set_ylabel("Maximum error")
bx.set_title("(b) Output checks", loc="left")
bx.legend(frameon=False, fontsize=7.5)
bx.grid(which="major", color="#dddddd", lw=.5)
save(fig, "FIG-stopping")
review = json.loads((HERE / "review_data.json").read_text(encoding="utf-8"))
fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.15, 2.8), layout="constrained")
widths = [r["width"] for r in review["widths"]]
for row in review["widths"]:
    values = [w["padding_ratio"] for w in row["windows"]]
    ax.scatter([row["width"]]*len(values), values, color=BLUE, s=9, alpha=.25)
ax.plot(widths, [r["mean_padding_ratio"] for r in review["widths"]], "o-", color=BLUE, ms=4, label="Mean over 40 windows")
ax.set_ylabel(r"Fixed-width slots / executed slots")
ax.set_title("(a) Padding within each batch", loc="left")
ax.legend(frameon=False, fontsize=7)
bx.plot(widths, [r["steady_speedup"] for r in review["widths"]], "o-", color=BLUE, ms=4, label="Steady-state")
bx.plot(widths, [r["deployment_speedup"] for r in review["widths"]], "s--", color=ORANGE, ms=4, label="Including startup")
bx.set_ylabel("Sequential / compacted execution time")
bx.set_title("(b) Complete-configuration comparison", loc="left")
bx.legend(frameon=False, fontsize=7)
for panel in (ax, bx):
    panel.set_xscale("log", base=2)
    panel.set_xticks(widths, [str(w) for w in widths])
    panel.set_xlabel("Initial batch width W")
    panel.axhline(1, color="#777777", lw=.8, linestyle=":")
    panel.set_ylim(.8, 2.1)
    panel.grid(axis="y", color="#dddddd", lw=.5)
save(fig, "FIG-scaling")
print("Rendered width, stopping, and scaling figures as PDF, SVG, PNG.")
