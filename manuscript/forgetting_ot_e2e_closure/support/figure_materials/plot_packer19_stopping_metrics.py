"""Render the Packer19 table metrics as a compact two-panel figure."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "PACKER19_STOPPING_METRICS.csv"
OUT = HERE / "PACKER19_STOPPING_METRICS.pdf"
EXPECTED = (1e-4, 3e-4, 1e-3, 3e-3, 1e-2)

WIDTH, HEIGHT = 507.6, 220.0
LEFT, RIGHT, GAP = 42.0, 16.0, 25.0
PANEL_W = (WIDTH - LEFT - RIGHT - GAP) / 2
BOTTOM, TOP = 35.0, 28.0
PLOT_H = HEIGHT - BOTTOM - TOP
BLUE = HexColor("#4477AA")
GREEN = HexColor("#228833")
ORANGE = HexColor("#CC6677")
INK = HexColor("#222222")
GRID = HexColor("#D9D9D9")


def load_rows() -> list[dict[str, float]]:
    with SOURCE.open(encoding="utf-8", newline="") as stream:
        rows = [{k: float(v) for k, v in row.items()} for row in csv.DictReader(stream)]
    rows.sort(key=lambda row: row["tolerance"])
    if tuple(row["tolerance"] for row in rows) != EXPECTED:
        raise ValueError("unexpected tolerance grid")
    required = {
        "lm_over_pc",
        "lm_over_pc_ci_low", "lm_over_pc_ci_high", "max_actual_residual",
        "max_consumer_tv",
    }
    if not rows or not required.issubset(rows[0]):
        raise ValueError("missing stopping-metric columns")
    for row in rows:
        if not all(math.isfinite(row[key]) for key in required):
            raise ValueError("non-finite stopping metric")
        if row["lm_over_pc_ci_low"] > row["lm_over_pc"] or row["lm_over_pc_ci_high"] < row["lm_over_pc"]:
            raise ValueError("invalid LM/DC interval")
    return rows


def xmap(value: float, left: float) -> float:
    # log-spaced tolerance axis keeps the multiplicative grid readable.
    lo, hi = math.log10(EXPECTED[0]), math.log10(EXPECTED[-1])
    return left + (math.log10(value) - lo) / (hi - lo) * PANEL_W


def draw_x_axis(pdf: canvas.Canvas, left: float, panel_title: str) -> None:
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 8.0)
    pdf.drawCentredString(left + PANEL_W / 2, HEIGHT - 13, panel_title)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(0.55)
    pdf.line(left, BOTTOM, left + PANEL_W, BOTTOM)
    labels = ("1e-4", "3e-4", "1e-3", "3e-3", "1e-2")
    for value, label in zip(EXPECTED, labels):
        xx = xmap(value, left)
        pdf.setStrokeColor(GRID)
        pdf.setLineWidth(0.35)
        pdf.line(xx, BOTTOM, xx, HEIGHT - TOP)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 5.8)
        pdf.drawCentredString(xx, 24, label)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 6.2)
    pdf.drawCentredString(left + PANEL_W / 2, 14, "Residual tolerance (tau)")


def render(rows: list[dict[str, float]]) -> None:
    pdf = canvas.Canvas(str(OUT), pagesize=(WIDTH, HEIGHT), invariant=1)
    pdf.setTitle("Packer19 stopping execution metrics")
    left_a = LEFT
    left_b = LEFT + PANEL_W + GAP
    draw_x_axis(pdf, left_a, "(a) Speedup ratios")
    draw_x_axis(pdf, left_b, "(b) Output checks")

    # Panel A: ratios and the equal-host bootstrap interval.
    y_lo, y_hi = 0.9, 1.72
    def ya(value: float) -> float:
        return BOTTOM + (value - y_lo) / (y_hi - y_lo) * PLOT_H
    for tick in (1.0, 1.25, 1.5, 1.7):
        yy = ya(tick)
        pdf.setStrokeColor(GRID)
        pdf.setLineWidth(0.35)
        pdf.line(left_a, yy, left_a + PANEL_W, yy)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 5.8)
        pdf.drawRightString(left_a - 4, yy - 2, f"{tick:.2g}")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 6.2)
    pdf.saveState(); pdf.translate(11, BOTTOM + PLOT_H / 2); pdf.rotate(90)
    pdf.drawCentredString(0, 0, "LM time / DC time")
    pdf.restoreState()
    series = (("LM / DC", "lm_over_pc", ORANGE, "d"),)
    for label, key, color, marker in series:
        points = [(xmap(row["tolerance"], left_a), ya(row[key])) for row in rows]
        pdf.setStrokeColor(color); pdf.setLineWidth(1.1)
        for p0, p1 in zip(points, points[1:]): pdf.line(*p0, *p1)
        pdf.setFillColor(color)
        for xx, yy in points:
            if marker == "s": pdf.rect(xx - 2.3, yy - 2.3, 4.6, 4.6, stroke=0, fill=1)
            elif marker == "d": pdf.wedge(xx - 2.8, yy - 2.8, xx + 2.8, yy + 2.8, 0, 360, stroke=0, fill=1)
            else: pdf.circle(xx, yy, 2.5, stroke=0, fill=1)
    for row in rows:
        xx = xmap(row["tolerance"], left_a)
        pdf.setStrokeColor(ORANGE); pdf.setLineWidth(0.7)
        pdf.line(xx, ya(row["lm_over_pc_ci_low"]), xx, ya(row["lm_over_pc_ci_high"]))
        pdf.line(xx - 2, ya(row["lm_over_pc_ci_low"]), xx + 2, ya(row["lm_over_pc_ci_low"]))
        pdf.line(xx - 2, ya(row["lm_over_pc_ci_high"]), xx + 2, ya(row["lm_over_pc_ci_high"]))
    # Legend.
    for i, (label, _, color, marker) in enumerate(series):
        lx = left_a + 4 + i * 103
        ly = HEIGHT - 28
        pdf.setFillColor(color)
        pdf.rect(lx, ly - 1, 7, 4, stroke=0, fill=1)
        pdf.setFillColor(INK); pdf.setFont("Helvetica", 5.6)
        pdf.drawString(lx + 10, ly, label)
    pdf.setFillColor(INK); pdf.setFont("Helvetica", 5.3)
    pdf.drawString(left_a + 4, HEIGHT - 47, "Whiskers: LM / DC equal-host bootstrap 95% CI")

    # Panel B: residual and consumer TV on a log scale.
    y_min, y_max = 1e-5, 2e-2
    def yb(value: float) -> float:
        return BOTTOM + (math.log10(value) - math.log10(y_min)) / (math.log10(y_max) - math.log10(y_min)) * PLOT_H
    for tick in (1e-5, 1e-4, 1e-3, 1e-2):
        yy = yb(tick)
        pdf.setStrokeColor(GRID); pdf.setLineWidth(0.35); pdf.line(left_b, yy, left_b + PANEL_W, yy)
        pdf.setFillColor(INK); pdf.setFont("Helvetica", 5.8); pdf.drawRightString(left_b - 4, yy - 2, f"{tick:.0e}")
    pdf.setFillColor(INK); pdf.setFont("Helvetica", 6.2)
    pdf.saveState(); pdf.translate(left_b - 31, BOTTOM + PLOT_H / 2); pdf.rotate(90)
    pdf.drawCentredString(0, 0, "Maximum value (log scale)")
    pdf.restoreState()
    for label, key, color, marker in (("Actual residual", "max_actual_residual", BLUE, "o"), ("Consumer TV", "max_consumer_tv", ORANGE, "s")):
        points = [(xmap(row["tolerance"], left_b), yb(row[key])) for row in rows]
        pdf.setStrokeColor(color); pdf.setLineWidth(1.1)
        for p0, p1 in zip(points, points[1:]): pdf.line(*p0, *p1)
        pdf.setFillColor(color)
        for xx, yy in points:
            if marker == "s": pdf.rect(xx - 2.4, yy - 2.4, 4.8, 4.8, stroke=0, fill=1)
            else: pdf.circle(xx, yy, 2.6, stroke=0, fill=1)
    lx, ly = left_b + 4, HEIGHT - 28
    for label, color in (("Actual residual", BLUE), ("Consumer TV", ORANGE)):
        pdf.setFillColor(color); pdf.rect(lx, ly - 1, 7, 4, stroke=0, fill=1)
        pdf.setFillColor(INK); pdf.setFont("Helvetica", 5.8); pdf.drawString(lx + 10, ly, label); lx += 78
    pdf.save()


if __name__ == "__main__":
    render(load_rows())
    print(OUT)
