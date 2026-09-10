# DrainSinkhorn paper

This repository contains one current manuscript: the English DrainSinkhorn
paper. The links below are the authoritative navigation entry points.

- [Compiled PDF](manuscript/forgetting_ot_e2e_closure/main.pdf)
- [LaTeX entry point](manuscript/forgetting_ot_e2e_closure/main.tex)
- [Section sources](manuscript/forgetting_ot_e2e_closure/sections)
- [Current figures and tables](manuscript/forgetting_ot_e2e_closure/figures)
- [Detailed manuscript navigator](manuscript/forgetting_ot_e2e_closure/README.md)
- [Standalone English results comparison table](manuscript/forgetting_ot_e2e_closure/ALL_RESULTS.md) — all reported experimental results and plotted points, with contrasts, timing scopes and sources; not included in the manuscript PDF.
- [Batching implementation audit](BATCHING_IMPLEMENTATION_AUDIT.md) — pinned source-level comparison plus the executed POT/GeomLoss release audit and direct POT solver modification.
- [Batching/completion-aware revision TODO](BATCHING_COMPLETION_AWARE_TODO.md) — executed checklist and remaining evidence gaps.

Build commands:

```powershell
cd manuscript/forgetting_ot_e2e_closure
latexmk -pdf -interaction=nonstopmode -halt-on-error -auxdir=support/build main.tex
```

Updated: 2026-09-10. The English manuscript presents batching as the enabling
capability, identifies the fixed-width/common-stop mechanisms actually audited,
and positions completion-aware execution as retaining joint execution while
avoiding later work on verified-complete problems. It now reports official POT
and GeomLoss release configurations under a common endpoint and a separate
same-backend experiment that directly modifies POT's own batch loop; Drain is
not the modification target in that causal comparison. See the source audit
and detailed navigator for evidence and remaining scope.
