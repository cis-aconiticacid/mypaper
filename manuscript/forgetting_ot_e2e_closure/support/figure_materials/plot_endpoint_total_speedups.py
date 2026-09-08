"""Render matched application endpoint ratios.

The display is deliberately separate from OT-stage and component attribution:
it answers only whether the complete accelerated OT path transfers to its
consumer without violating the registered output checks.
"""

from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


HERE = Path(__file__).resolve().parent
ROWS = list(csv.DictReader((HERE / "ENDPOINT_TOTAL_SPEEDUPS.csv").open(encoding="utf-8")))
OUT = HERE / "ENDPOINT_TOTAL_SPEEDUPS.pdf"

WIDTH, HEIGHT = 252.0, 157.0
LEFT, RIGHT = 86.0, 34.0
BOTTOM, TOP = 24.0, 126.0
MAX_X = 2.0
BLUE = HexColor("#4477AA")
GREEN = HexColor("#228833")
ORANGE = HexColor("#CC6677")
GRID = HexColor("#D9D9D9")
TEXT = HexColor("#222222")


def x_position(value: float) -> float:
    return LEFT + value / MAX_X * (WIDTH - LEFT - RIGHT)


pdf = canvas.Canvas(str(OUT), pagesize=(WIDTH, HEIGHT))
pdf.setTitle("DrainSinkhorn matched endpoint speedups")

pdf.setFillColor(TEXT)
pdf.setFont("Helvetica-Oblique", 6.2)
pdf.drawCentredString(WIDTH / 2, 148,
                      "Each ratio uses its registered endpoint scope")

for tick in (0, 0.5, 1, 1.5, 2):
    x = x_position(float(tick))
    pdf.setStrokeColor(GRID)
    pdf.setLineWidth(0.4)
    pdf.line(x, BOTTOM, x, TOP)
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica", 6.5)
    pdf.drawCentredString(x, 13, str(tick))

colors = (BLUE, GREEN, ORANGE)
bar_height = 18.0
row_gap = 35.0
start_y = 100.0

for index, (row, color) in enumerate(zip(ROWS, colors)):
    value = float(row["speedup"])
    y = start_y - index * row_gap
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Bold", 6.8)
    pdf.drawRightString(LEFT - 5, y + 5, row["application"])
    pdf.setFillColor(color)
    pdf.rect(LEFT, y, x_position(value) - LEFT, bar_height, stroke=0, fill=1)
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Bold", 7.1)
    pdf.drawString(x_position(value) + 3, y + 5, f"{value:.3f}x")

pdf.setFillColor(TEXT)
pdf.setFont("Helvetica", 6.6)
pdf.drawCentredString((LEFT + WIDTH - RIGHT) / 2, 2.5, "Endpoint speedup (matched baseline / compacted)")
pdf.save()
