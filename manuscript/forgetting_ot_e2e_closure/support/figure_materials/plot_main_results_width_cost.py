"""Build the normalized three-panel packed-update width-cost figure.

Each panel reads the corresponding D15 machine summary directly. Registered
matched results are kept in the adjacent LaTeX table and its source CSV. The
plotted quantity is the measured median ratio c(W, xi) / c(a, xi).
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
WIDTH_ROOT = Path(
    os.environ.get(
        "DRAINSINKHORN_WIDTH_ROOT",
        REPO / "studies/local_results/A100_WIDTH_COST_ENGINEERING_20260907T205000Z_73aec294",
    )
)
COMMON_WIDTHS = np.array([1, 2, 3, 4, 6, 8, 12, 16])
STATIC_WIDTHS = (8, 16)
STATIC_STYLES = {
    8: {"color": "#D55E00", "marker": "s"},
    16: {"color": "#0072B2", "marker": "o"},
}


def load_width_curve(n: int) -> list[dict[str, float]]:
    path = WIDTH_ROOT / f"n{n}" / "width_cost_curve.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for width, values in payload["per_width_summary_seconds"].items():
        rows.append(
            {
                "width": int(width),
                "median_ms": 1000.0 * values["median"],
                "q1_ms": 1000.0 * values["q1"],
                "q3_ms": 1000.0 * values["q3"],
            }
        )
    return sorted(rows, key=lambda row: row["width"])


def configure_style(language: str) -> None:
    font = "Microsoft YaHei" if language == "zh" else "DejaVu Serif"
    mpl.rcParams.update(
        {
            "font.family": font,
            "font.size": 7.2,
            "axes.titlesize": 8.2,
            "axes.titleweight": "bold",
            "axes.labelsize": 7.4,
            "xtick.labelsize": 6.6,
            "ytick.labelsize": 6.4,
            "legend.fontsize": 6.5,
            "axes.linewidth": 0.7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "mathtext.fontset": "stix",
        }
    )


def draw_width_panel(ax: plt.Axes, n: int, language: str) -> None:
    by_width = {row["width"]: row for row in load_width_curve(n)}
    missing = [int(a) for a in COMMON_WIDTHS if int(a) not in by_width]
    if missing:
        raise ValueError(f"n={n} is missing common widths {missing}")

    for static_width in STATIC_WIDTHS:
        widths = COMMON_WIDTHS[COMMON_WIDTHS <= static_width]
        baseline = by_width[static_width]
        median = np.array([baseline["median_ms"] / by_width[int(a)]["median_ms"] for a in widths])
        lower = np.array([baseline["q1_ms"] / by_width[int(a)]["q3_ms"] for a in widths])
        upper = np.array([baseline["q3_ms"] / by_width[int(a)]["q1_ms"] for a in widths])
        style = STATIC_STYLES[static_width]
        ax.fill_between(widths, lower, upper, color=style["color"], alpha=0.12, linewidth=0)
        ax.plot(
            widths,
            median,
            color=style["color"],
            marker=style["marker"],
            ms=3.2,
            lw=1.35,
        )

    delta = 64 * 108 / n
    ax.axhline(1.0, color="#555555", lw=0.8, ls=(0, (3, 2)))
    ax.set_xticks(COMMON_WIDTHS)
    ax.set_xlim(0.5, 16.5)
    ax.grid(True, which="both", color="#b8b8b8", alpha=0.42, linewidth=0.45)
    ax.set_axisbelow(True)
    ax.set_title(f"$n={n:,},\\quad \\Delta={delta:.2f}$")
    ax.set_xlabel("Active batch width $a$" if language == "en" else "存活宽度 $a$")
    if n == 1024:
        ax.set_ylabel(
            "Measured static-width speedup  $c(W,\\xi)/c(a,\\xi)$"
            if language == "en"
            else "相对静态宽度的实测加速  $c(W,\\xi)/c(a,\\xi)$"
        )


def build(output: Path, language: str) -> None:
    configure_style(language)
    fig = plt.figure(figsize=(7.15, 2.60))
    grid = fig.add_gridspec(1, 6, wspace=0.95)

    width_axes = [
        fig.add_subplot(grid[0, 0:2]),
        fig.add_subplot(grid[0, 2:4]),
        fig.add_subplot(grid[0, 4:6]),
    ]
    for ax, n in zip(width_axes, (1024, 4096, 16384)):
        draw_width_panel(ax, n, language)
    for ax in width_axes:
        ax.set_ylim(0.75, 12.7)

    legend = [
        Line2D([0], [0], color=STATIC_STYLES[w]["color"], marker=STATIC_STYLES[w]["marker"], lw=1.35, label=f"static $W={w}$")
        for w in STATIC_WIDTHS
    ]
    fig.legend(handles=legend, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.535, 1.02))

    fig.subplots_adjust(left=0.105, right=0.985, top=0.82, bottom=0.22)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=("en", "zh"), default="en")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.output, args.language)
