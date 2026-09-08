"""Render the Packer19 tolerance--speed/quality frontier after evidence gates pass.

This script intentionally refuses the historical C51 table: its consumer TV
was measured relative to the 1e-3 output. The paper frontier requires five
matched measurements, all compared directly with the 1e-6 consumer output.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "PACKER19_TOLERANCE_FRONTIER.csv"
OUT = HERE / "PACKER19_TOLERANCE_FRONTIER.pdf"
EXPECTED_TOLERANCES = (1e-6, 1e-3, 3e-3, 5e-3, 1e-2)
REQUIRED_COLUMNS = {
    "tolerance",
    "consumer_tv_vs_1e6",
    "ot_stage_seconds",
    "execution_path",
    "data_sha256",
    "timing_contract",
}


def load_and_validate() -> list[dict[str, str]]:
    if not SOURCE.exists():
        raise SystemExit(
            "Refusing to render: PACKER19_TOLERANCE_FRONTIER.csv is absent. "
            "C51_ACCURACY_SWEEP.csv is 1e-3-relative and is not a valid input."
        )

    with SOURCE.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or ())
        if missing:
            raise SystemExit(f"Refusing to render: missing columns {sorted(missing)}")
        rows = list(reader)

    if len(rows) != len(EXPECTED_TOLERANCES):
        raise SystemExit("Refusing to render: exactly five measured rows are required")

    rows.sort(key=lambda row: float(row["tolerance"]))
    measured = tuple(float(row["tolerance"]) for row in rows)
    if any(
        not math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-12)
        for actual, expected in zip(measured, EXPECTED_TOLERANCES)
    ):
        raise SystemExit(f"Refusing to render: unexpected tolerances {measured}")

    for field in ("execution_path", "data_sha256", "timing_contract"):
        values = {row[field] for row in rows}
        if len(values) != 1:
            raise SystemExit(f"Refusing to render: mixed {field}: {sorted(values)}")

    for row in rows:
        tv = float(row["consumer_tv_vs_1e6"])
        seconds = float(row["ot_stage_seconds"])
        if not (math.isfinite(tv) and tv >= 0.0):
            raise SystemExit("Refusing to render: invalid consumer TV")
        if not (math.isfinite(seconds) and seconds > 0.0):
            raise SystemExit("Refusing to render: invalid OT-stage time")
    if not math.isclose(float(rows[0]["consumer_tv_vs_1e6"]), 0.0, abs_tol=1e-12):
        raise SystemExit("Refusing to render: the 1e-6 reference must have consumer TV 0")
    return rows


def render(rows: list[dict[str, str]]) -> None:
    from reportlab.lib.colors import HexColor
    from reportlab.pdfgen import canvas

    width, height = 252.0, 174.0
    left, right, bottom, top = 42.0, 12.0, 34.0, 27.0
    plot_width = width - left - right
    plot_height = height - bottom - top
    blue = HexColor("#356AA0")
    ink = HexColor("#222222")
    grid = HexColor("#D9D9D9")

    tv = [float(row["consumer_tv_vs_1e6"]) for row in rows]
    times = [float(row["ot_stage_seconds"]) for row in rows]
    labels = ["1e-6", "1e-3", "3e-3", "5e-3", "1e-2"]
    x_hi = max(tv) * 1.10 if max(tv) > 0 else 1.0
    y_lo = min(times) * 0.90
    y_hi = max(times) * 1.08

    def xmap(value: float) -> float:
        return left + value / x_hi * plot_width

    def ymap(value: float) -> float:
        return bottom + (value - y_lo) / (y_hi - y_lo) * plot_height

    pdf = canvas.Canvas(str(OUT), pagesize=(width, height), invariant=1)
    pdf.setTitle("Tolerance-dependent OT speed-quality frontier")
    pdf.setFillColor(ink)
    pdf.setFont("Helvetica-Bold", 8.2)
    pdf.drawCentredString(width / 2, height - 13, "Tolerance-dependent OT speed-quality frontier")

    for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom + fraction * plot_height
        value = y_lo + fraction * (y_hi - y_lo)
        pdf.setStrokeColor(grid)
        pdf.setLineWidth(0.35)
        pdf.line(left, y, width - right, y)
        pdf.setFillColor(ink)
        pdf.setFont("Helvetica", 5.8)
        pdf.drawRightString(left - 4, y - 2, f"{value:.2g}")

    points = [(xmap(x), ymap(y)) for x, y in zip(tv, times)]
    pdf.setStrokeColor(blue)
    pdf.setFillColor(blue)
    pdf.setLineWidth(1.25)
    for first, second in zip(points, points[1:]):
        pdf.line(first[0], first[1], second[0], second[1])
    for index, ((x, y), label) in enumerate(zip(points, labels)):
        pdf.circle(x, y, 2.8, stroke=1, fill=1)
        dx = 5 if index < 4 else -13
        pdf.setFont("Helvetica", 5.8)
        pdf.drawString(x + dx, y + 4, label)

    pdf.setStrokeColor(ink)
    pdf.setLineWidth(0.55)
    pdf.line(left, bottom, width - right, bottom)
    pdf.line(left, bottom, left, height - top)
    pdf.setFont("Helvetica", 6.2)
    pdf.drawCentredString(left + plot_width / 2, 13, "Downstream consumer TV vs. 1e-6 reference")
    pdf.saveState()
    pdf.translate(12, bottom + plot_height / 2)
    pdf.rotate(90)
    pdf.drawCentredString(0, 0, "OT stage time (s)")
    pdf.restoreState()
    pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    render(load_and_validate())
    print(OUT)
