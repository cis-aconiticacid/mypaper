"""Render the registered backend-matched execution speedups.

Panel A reports matched Flash controls. Panel B reports matched or same-backend
implementations over OTT-JAX and PyKeOps.
"""

from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


HERE = Path(__file__).resolve().parent
ROWS = list(csv.DictReader((HERE / "OT_TOTAL_SPEEDUPS.csv").open(encoding="utf-8")))
OUT = HERE / "OT_TOTAL_SPEEDUPS.pdf"

WIDTH, HEIGHT = 507.6, 155.0
PANEL_GAP = 22.0
PANEL_W = (WIDTH - PANEL_GAP) / 2
BOTTOM, TOP = 25.0, 126.0
LABEL_W = 91.0
RIGHT_PAD = 24.0
BAR_H = 17.0
ROW_GAP = 31.0
START_Y = 96.0

BLUE = HexColor("#4477AA")
GREEN = HexColor("#228833")
ORANGE = HexColor("#CC6677")
GRID = HexColor("#D9D9D9")
TEXT = HexColor("#222222")
BASELINE = HexColor("#777777")


def draw_panel(pdf: canvas.Canvas, left: float, rows: list[dict[str, str]],
               title: str, max_x: float, ticks: list[float], colors: list) -> None:
    plot_left = left + LABEL_W
    plot_right = left + PANEL_W - RIGHT_PAD

    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Bold", 8.4)
    pdf.drawCentredString(left + PANEL_W / 2, 141, title)

    def xpos(value: float) -> float:
        return plot_left + value / max_x * (plot_right - plot_left)

    for tick in ticks:
        xx = xpos(tick)
        pdf.setStrokeColor(GRID)
        pdf.setLineWidth(0.35)
        pdf.line(xx, BOTTOM, xx, TOP)
        pdf.setFillColor(TEXT)
        pdf.setFont("Helvetica", 5.8)
        pdf.drawCentredString(xx, 15, f"{tick:g}")

    one_x = xpos(1.0)
    pdf.setStrokeColor(BASELINE)
    pdf.setDash(2, 2)
    pdf.setLineWidth(0.7)
    pdf.line(one_x, BOTTOM, one_x, TOP)
    pdf.setDash()

    for index, (row, color) in enumerate(zip(rows, colors)):
        value = float(row["speedup"])
        yy = START_Y - index * ROW_GAP
        label = row["workload"]
        if row["group"] == "transfer":
            label = f"{label} / {row['backend']}"
        pdf.setFillColor(TEXT)
        pdf.setFont("Helvetica-Bold", 6.3)
        pdf.drawRightString(plot_left - 5, yy + 5, label)
        pdf.setFillColor(color)
        pdf.rect(plot_left, yy, xpos(value) - plot_left, BAR_H, stroke=0, fill=1)
        pdf.setFillColor(TEXT)
        pdf.setFont("Helvetica-Bold", 7.0)
        pdf.drawString(min(xpos(value) + 3, left + PANEL_W - 28), yy + 5,
                       f"{value:.3f}x")

    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica", 6.2)
    pdf.drawCentredString((plot_left + plot_right) / 2, 2.5,
                          "OT-stage speedup (baseline / DrainSinkhorn)")


pdf = canvas.Canvas(str(OUT), pagesize=(WIDTH, HEIGHT), invariant=1)
pdf.setTitle("DrainSinkhorn matched execution speedups")

flash_rows = [row for row in ROWS if row["group"] == "flash"]
transfer_rows = [row for row in ROWS if row["group"] == "transfer"]

draw_panel(pdf, 0.0, flash_rows, "(a) Matched Flash controls",
           2.0, [0, 0.5, 1, 1.5, 2], [BLUE, BLUE, BLUE])
draw_panel(pdf, PANEL_W + PANEL_GAP, transfer_rows,
           "(b) Same-backend realizations",
           3.5, [0, 1, 2, 3], [GREEN, ORANGE, GREEN])

pdf.save()
print(OUT)
