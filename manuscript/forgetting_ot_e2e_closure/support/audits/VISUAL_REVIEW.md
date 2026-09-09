# Manuscript restructuring and visual review

## Scope and writing decisions

The current English manuscript was rebuilt from title through appendix. The starting checkpoint is 795cb6c. All old figure/table files in figures/ were removed; Git retains their previous contents. Source CSVs, frozen analyses, and numerical macros remain available.

The paper now proceeds from measured wasted work to screen/verify/compact, then a hardware-aware performance model, followed by application results and mechanism experiments. This ordering draws on AI Metropolis, Sections 2.2, 3, and 4 (https://proceedings.mlsys.org/paper_files/paper/2025/file/4f31327e046913c7238d5b671f5d820e-Paper-Conference.pdf). The application domains and mechanisms remain those of DrainSinkhorn.

Source-level scope:
- Central mechanism: sections/3_method.tex, equations for the screen, verifier, and independent packed update.
- Runtime model: sections/4_cost_and_hypothesis.tex. Completion counts, calibrated kernel costs, and overhead are retained; elementary consequences are expressed in prose rather than separate propositions.
- Main results: sections/5_experiments.tex, based on existing result macros and frozen CSVs.
- Timing and numerical boundaries: sections/A_appendix.tex, preserving per-study observation units, consumer subtraction, separate stopping/component studies, and separate guarded precision tests.
- No new experimental runs or new statistical estimates were performed.

User-supplied skills applied:
- Downloads/SKILL (1).md: academic-writing, paragraph purpose and evidence-led section structure.
- Downloads/SKILL (2).md: anti-defensive-writing, direct claims and concentrated scope conditions.
- Downloads/SKILL (3).md: research-paper-figures, claim-specific visuals, reproducible vectors, explicit provenance, and visual QA.
Their referenced companion files and an academic-self-check package were not available in the supplied directory. The checks below are the explicit local drafting/rendering review, not a claim of having executed those missing workflows.

## Visual inventory and sources

Paths below are relative to the manuscript directory. Git paths use the repository root. Historical source level is identified explicitly; unchanged manuscript values are not presented as newly verified raw experiments.

| ID / PDF number | Purpose and encoding | Input and source level | Caption / insertion |
|---|---|---|---|
| FIG-work / Figure 1 | Show executed work; two independent horizontal-bar panels with zero baselines | figure_spec.json work rows; manuscript registry at 795cb6c:manuscript/forgetting_ot_e2e_closure/figures/RESULT_MACROS.tex, CMetroSlotsStatic/Active and CPackerSlotsStatic/Active | sections/2_setting_related.tex; total updates, no inferred completion trajectory |
| FIG-width / Figure 2 | Show stepwise kernel cost; absolute-time line panels with W=8/16 guides | figure_spec.json width data; direct machine summaries from studies/local_results/A100_WIDTH_COST_ENGINEERING_20260907T205000Z_73aec294/n{n}/width_cost_curve.json | sections/5_experiments.tex; milliseconds, 30-repeat medians and IQR, independent y-scales stated |
| FIG-stopping / Figure 3 | Relate benefit to tolerance and output error; forest plot plus log-log error panel | support/figure_materials/PACKER19_STOPPING_METRICS.csv, frozen analysis rows | sections/5_experiments.tex; bootstrap 95% intervals, 24 units per tolerance |
| FIG-setup / Table 1 | Lookup primary configurations | 795cb6c:manuscript/forgetting_ot_e2e_closure/sections/5_experiments.tex, experimental setup; current manuscript source | figures/FIG-setup.tex, Section 5.1 |
| FIG-endpoints / Table 2 | Compare within explicit E1/E2/E3 scopes | support/figure_materials/MAIN_RESULTS_BY_WIDTH.csv; ENDPOINT_TOTAL_SPEEDUPS.csv; RESULT_MACROS.tex for training range | figures/FIG-endpoints.tex, Section 5.2 |
| FIG-backends / Table 3 | State implementation-specific baselines and results | 795cb6c:manuscript/forgetting_ot_e2e_closure/figures/table7_cross_backend_results.tex; manuscript summaries | figures/FIG-backends.tex, Section 5.2 |
| FIG-quality / Table 4 | Lookup training quality; metric rows, NFE columns | 795cb6c:manuscript/forgetting_ot_e2e_closure/figures/table4_imagenet_quality.tex; three-seed means | figures/FIG-quality.tex, Section 5.2 |
| FIG-components / Table 5 | Isolate four execution changes; one ratio and evidence column | 795cb6c:manuscript/forgetting_ot_e2e_closure/figures/table5_packer19_attribution.tex; frozen matched summaries | figures/FIG-components.tex, Section 5.4 |
| FIG-grouping / Table 6 | Pair dynamic-update fraction with runtime ratio | 795cb6c:manuscript/forgetting_ot_e2e_closure/figures/table6_grouping_intervention.tex; grouping summary on 32 problems | figures/FIG-grouping.tex, Section 5.5 |
| FIG-seeds / Table 7 | Inspect absolute solver times by seed | support/figure_materials/C63_SOLVER_ATTRIBUTION.csv; frozen seed-level analysis | figures/FIG-seeds.tex, Appendix A.2 |
| FIG-phases / Table 8 | Inspect each component's median cost | 795cb6c:manuscript/forgetting_ot_e2e_closure/figures/table12_packer19_phase_costs.tex; manuscript phase medians | figures/FIG-phases.tex, Appendix A.2; seconds multiplied by 1000, no sum used as total |
| FIG-additional / Table 9 | Inspect eight-worker absolute endpoints and support-size ratios | 795cb6c:manuscript/forgetting_ot_e2e_closure/figures/table3_eight_gpu_decomposition.tex; MAIN_RESULTS_BY_WIDTH.csv | figures/FIG-additional.tex, Appendix A.4 |

The old prior-system table is replaced by related-work prose. The old omnibus results table is split into endpoint and backend views. The old attribution ledger table is replaced by this support-level source map and focused appendix measurements. The old Pareto and stopping charts are replaced by the tolerance figure. No old graphic is inserted in the new PDF.

## Figure contract

- Backend: Python 3 with matplotlib and numpy; support/figure_materials/render_figures.py.
- Specification: support/figure_materials/figure_spec.json. Width summaries are stored with source paths so regeneration does not depend on another checkout.
- Exports: figures/FIG-{work,width,stopping}.{pdf,svg,png}; PDF and SVG retain vector text. Final LaTeX inserts PDF, not PNG.
- Dimensions: work plot 3.45 inches wide; width and stopping plots 7.15 inches wide, scaled to the manuscript column/page width.
- Typography: DejaVu Sans, 9-point base; final table type is 8–9 points.
- Palette: blue #0072B2 and orange #D55E00; grey baselines. Shapes, panel titles, and line styles supplement color.
- Uncertainty: work bars are totals; width whiskers are IQR; stopping whiskers are bootstrap 95% intervals. Tight intervals may be narrower than the plotted markers.
- Units: width seconds converted to milliseconds by multiplication by 1000; phase-table seconds converted by the same factor. Ratios remain baseline/candidate.
- No architecture schematic or generated-image reference is used. draw.io/Visio replication and C2PA checks for generated bitmaps are not applicable.

## Scientific and readability review

Manual figure-style and chart-encoding review:
- Work-count panels have explicit zero baselines and separate task labels/scales.
- Width panels use the same x coordinates and units, with independent y-scales explicitly stated. Initial W is a visible guide in every panel.
- The stopping plot uses a line at ratio 1; maxima and confidence intervals preserve their distinct statistical meanings.
- Tables identify comparisons and statistical units; missing absolute support-size timings remain dashes.
- No cross-task aggregate, predicted trajectory, pixel-space FID, new equivalence test, or new hardware measurement is introduced.

Readability review:
- Examined all three exported plots and rendered manuscript pages at final insertion size.
- Reworked float placement to remove nearly empty intermediate pages.
- Changed narrow result tables to single-column placement and supplementary tables to a single-column appendix.
- Checked headers, captions, legends, table row alignment, numeric labels, and bibliography separation.
- Table 5 remains the component test in Section 5.4; Table 6 remains the grouping test in Section 5.5.
- Main and appendix prose contain no displayed campaign codes or project-maintainer instructions.

Build validation is recorded in support/build/main.log; page renders are in support/qa/. These are local manuscript/render checks, not GPU performance validation.
