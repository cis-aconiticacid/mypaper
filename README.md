# DrainSinkhorn paper

This repository contains one current manuscript: the English DrainSinkhorn
paper. The links below are the authoritative navigation entry points.

- [Compiled PDF](manuscript/forgetting_ot_e2e_closure/main.pdf)
- [LaTeX entry point](manuscript/forgetting_ot_e2e_closure/main.tex)
- [Section sources](manuscript/forgetting_ot_e2e_closure/sections)
- [Current figures and tables](manuscript/forgetting_ot_e2e_closure/figures)
- [Detailed manuscript navigator](manuscript/forgetting_ot_e2e_closure/README.md)
- [Standalone English results comparison table](manuscript/forgetting_ot_e2e_closure/ALL_RESULTS.md) — all reported experimental results and plotted points, with contrasts, timing scopes and sources; not included in the manuscript PDF.

Build commands:

```powershell
cd manuscript/forgetting_ot_e2e_closure
latexmk -pdf -interaction=nonstopmode -halt-on-error -auxdir=support/build main.tex
```

Updated: 2026-09-09. The English manuscript now includes compute-skipping controls,
conditional runtime reconstruction, actual-output FP64 replay, and matched-check
PyKeOps results. See the detailed navigator for evidence and remaining scope.
