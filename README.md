# DrainSinkhorn paper

This repository contains one current manuscript: the English DrainSinkhorn
paper. The links below are the authoritative navigation entry points.

- [Compiled PDF](manuscript/forgetting_ot_e2e_closure/main.pdf)
- [LaTeX entry point](manuscript/forgetting_ot_e2e_closure/main.tex)
- [Section sources](manuscript/forgetting_ot_e2e_closure/sections)
- [Current figures and tables](manuscript/forgetting_ot_e2e_closure/figures)
- [Detailed manuscript navigator](manuscript/forgetting_ot_e2e_closure/README.md)

Build commands:

```powershell
cd manuscript/forgetting_ot_e2e_closure
latexmk -pdf -interaction=nonstopmode -halt-on-error -auxdir=support/build main.tex
```

Updated: 2026-09-08
