"""Render the registered Packer19 dynamic-compaction speed--output frontier."""

from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


HERE = Path(__file__).resolve().parent
ROWS = list(csv.DictReader((HERE / "PACKER19_PARETO.csv").open(encoding="utf-8")))
OUT = HERE / "PACKER19_PARETO.pdf"

WIDTH, HEIGHT = 244.0, 150.0
LEFT, RIGHT, BOTTOM, TOP = 39.0, 12.0, 28.0, 13.0
PLOT_W = WIDTH - LEFT - RIGHT
PLOT_H = HEIGHT - BOTTOM - TOP
BLUE = HexColor("#4477AA")
GRID = HexColor("#D9D9D9")
TEXT = HexColor("#222222")


def xpos(value: float) -> float:
    return LEFT + value / 0.005 * PLOT_W


def ypos(value: float) -> float:
    return BOTTOM + (value - 0.4) / (2.6 - 0.4) * PLOT_H


pdf = canvas.Canvas(str(OUT), pagesize=(WIDTH, HEIGHT), invariant=1)
pdf.setTitle("Packer19 tolerance-dependent OT speed-output frontier")

for tick in [0, 1, 2, 3, 4, 5]:
    xx = xpos(tick * 1e-3)
    pdf.setStrokeColor(GRID)
    pdf.setLineWidth(0.35)
    pdf.line(xx, BOTTOM, xx, HEIGHT - TOP)
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica", 6.3)
    pdf.drawCentredString(xx, 17, str(tick))

for tick in [0.5, 1.0, 1.5, 2.0, 2.5]:
    yy = ypos(tick)
    pdf.setStrokeColor(GRID)
    pdf.setLineWidth(0.35)
    pdf.line(LEFT, yy, WIDTH - RIGHT, yy)
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica", 6.3)
    pdf.drawRightString(LEFT - 4, yy - 2, f"{tick:.1f}")

points = [(xpos(float(r["consumer_tv"])), ypos(float(r["ot_stage_seconds"])), r)
          for r in ROWS]
pdf.setStrokeColor(BLUE)
pdf.setLineWidth(1.2)
for (x0, y0, _), (x1, y1, _) in zip(points, points[1:]):
    pdf.line(x0, y0, x1, y1)

offsets = [(5, 4), (5, 4), (5, 4), (5, -9), (-24, 5)]
for (xx, yy, row), (dx, dy) in zip(points, offsets):
    pdf.setFillColor(BLUE)
    pdf.circle(xx, yy, 2.8, stroke=0, fill=1)
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Bold", 6.5)
    pdf.drawString(xx + dx, yy + dy, row["tolerance"])

pdf.setFillColor(TEXT)
pdf.setFont("Helvetica", 6.7)
pdf.drawCentredString(LEFT + PLOT_W / 2, 5,
                      "Consumer TV vs. 1e-6 reference (x1e-3)")
pdf.saveState()
pdf.translate(9, BOTTOM + PLOT_H / 2)
pdf.rotate(90)
pdf.drawCentredString(0, 0, "Dynamic-compaction OT stage (s)")
pdf.restoreState()
pdf.save()
print(OUT)
