# DrainSinkhorn paper

Latest compiled manuscripts:

- [English PDF](DrainSinkhorn_EN.pdf)
- [中文 PDF](DrainSinkhorn_ZH.pdf)

Complete LaTeX projects:

- [`manuscript/forgetting_ot_e2e_closure`](manuscript/forgetting_ot_e2e_closure)
- [`manuscript/forgetting_ot_e2e_closure_zh`](manuscript/forgetting_ot_e2e_closure_zh)

Build commands:

```powershell
cd manuscript/forgetting_ot_e2e_closure
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

cd ../forgetting_ot_e2e_closure_zh
latexmk -pdf -interaction=nonstopmode -halt-on-error main_zh.tex
```

Updated: 2026-09-08
