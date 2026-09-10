# Manuscript restructuring and visual review

## Latest review: definitions and table clarity (base dbf7e73)

Updated editable LaTeX tables, using the user-supplied figure skill. Its companion workflow/source-map/audit files remain unavailable; the local source-bound checks below cover this revision.

- Table 2: same-campaign absolute seconds beside existing ratios; caption defines geometric means versus paired-unit medians. CPU reanalysis checks displayed time pairs against full-precision aggregates (`competitive_data.json:endpoint_times_seconds`). No cross-campaign phase substitution.
- Table 5: explicit baseline/changed-configuration lookup, common verifier in caption. Table 9 separates Sinkhorn updates, row screen and two-marginal verifier. No phase numbers changed.
- Table 3: main matched PyKeOps comparison retained; Table 12 carries the four historical configurations unchanged. This is relocation, not removal of adverse results.
- Table 4: readable mean +/- sample SD with compact decimals; underlying observations unchanged. Small residuals use scientific notation rather than rounding to zero.
- Table 7: source insertion moved ahead of Section 5.7; final PDF places both on page 10. Tables 5 and 6 retain their numbers and source sections 5.4/5.5.
- Final 17-page PDF: inspected result tables on pages 7/8, controls on 10, metric equations and input construction on 13, phase headings on 14, bound equations on 16, and historical backend table on 17. No overlaps or clipping observed. LaTeX reports no overfull boxes or unresolved references. Validation is an agent source/render check, not human publication approval.

Sources, statistical units, unresolved metadata and anti-defensive-writing changes are itemized in the latest block of `REVIEW_DISPOSITION.md`.

## Latest review increment (base ab11094)

Added FIG-execution-settings as Table 11 in Appendix A.7, referenced from Section 3.4. Purpose: compare allocation policies and timing endpoints across the primary Triton contrasts. Contract: editable monochrome four-column lookup table, three source-bound rows, common initialization/precision/check interval/tail in caption; no uncertainty or new performance values because this is a configuration display. Sources and four-step review decisions are recorded at the top of REVIEW_DISPOSITION.md.

The user-supplied figure skill's companion workflow/source-map/final-audit references remain unavailable. Local review inspected the rendered Table 11 and title pages for readability, alignment and clipping; both are clear. The PDF is 16 pages with no overfull-box or undefined-reference warnings. Tables 5 and 6 retain their numbers and source insertion in Sections 5.4/5.5. Table 7 retains its absolute-time precision; fine ordering discussion is in A.7. These are agent source and visual checks, not an external design or human publication approval.

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
| FIG-method / Figure 1 | Execution loop and one recorded active-width trajectory | Section 3 state-selection contract and review_data.json W4 example; raw identity in REVIEW_DISPOSITION.md item 5 | figures/FIG-method.tex, Section 3; editable TikZ vector source |
| FIG-width / Figure 2 | Show stepwise kernel cost; absolute-time line panels with W=8/16 guides | figure_spec.json width data; direct machine summaries from studies/local_results/A100_WIDTH_COST_ENGINEERING_20260907T205000Z_73aec294/n{n}/width_cost_curve.json | sections/5_experiments.tex; milliseconds, 30-repeat medians and IQR, independent y-scales stated |
| FIG-stopping / Figure 3 | Relate benefit to tolerance and output error; forest plot plus log-log error panel | support/figure_materials/PACKER19_STOPPING_METRICS.csv, frozen analysis rows | sections/5_experiments.tex; bootstrap 95% intervals, 24 units per tolerance |
| FIG-setup / Table 1 | Lookup primary configurations | 795cb6c:manuscript/forgetting_ot_e2e_closure/sections/5_experiments.tex, experimental setup; current manuscript source | figures/FIG-setup.tex, Section 5.1 |
| FIG-endpoints / Table 2 | Compare within explicit E1/E2/E3 scopes | support/figure_materials/MAIN_RESULTS_BY_WIDTH.csv; ENDPOINT_TOTAL_SPEEDUPS.csv; RESULT_MACROS.tex for training range | figures/FIG-endpoints.tex, Section 5.2 |
| FIG-backends / Table 3 | Separate matched execution, complete configurations, and direct solver modification | OTT tolerance report, PyKeOps three-seed report, official-native campaign, and direct POT modification; see data-selection review below | figures/FIG-backends.tex, Section 5.2; four labeled blocks with distinct statistics and scope |
| FIG-quality / Table 4 | Compare quality with seed variability | review_data.json: 18 mean/sample-SD pairs recomputed from frozen per-seed training records | figures/FIG-quality.tex, Section 5.2; NFE rows, fixed/compacted pairs |
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

## Ledger-based data selection, 2026-09-08

This revision keeps the primary application, component, grouping, and neutral stopping results. It adds existing Packer19 pipeline evidence and replaces the backend table's isolated headline ratios with their comparison context. No experiments, confidence intervals, or cross-study aggregates were created. Evidence-repository paths below are relative to `C:/Users/ASUS/Documents/ai训练遗忘性研究`; manuscript paths are relative to this manuscript.

| Decision / manuscript location | Evidence and source level |
|---|---|
| Add Packer19 E2 1.2243 [1.2240, 1.2247] to FIG-endpoints, Section 5.2, and abstract; retain paired E1 | Frozen analysis: `archive/inspections/C80_LM_20260828/analysis_extracted/c80_lm_analysis_793c08c_20260828T1825Z/analysis.json`, primary LM/PC summary; formal manifest `studies/campaigns/C80_LM_logical_mask_attribution/manifest.json`, formal_result; ledger lines 848-855. Round existing estimates only. |
| Replace main OTT native-only headline with four matched-phase and native-reference pairs | Formal report: `studies/reports/OTT_IMAGENET_RELAXED_PHASE_ACTIVE_RESULTS_20260825_ZH.md`, lines 38-43; device-resident timing boundary lines 9-33. Earlier six-repeat values remain in Appendix A.3 under their own study identity. |
| Show all four ImageNet-32 PyKeOps configurations at n16384, including static and mask outperforming compaction | Formal report: `studies/reports/IMAGENET32_KEOPS_PACKED_RESULTS_20260808.md`, lines 29-46 and 58-61. Values are arithmetic means of paired seed ratios, not ratios of mean times. Implementation: `studies/code/imagenet32_repeated_eot.py`, lines 417 and 446, checks at fixed intervals 1/2/4. These are not exponentially increasing schedules. |
| Move coupling-preparation, shared-initialization, worker scaling, and guarded precision detail to appendix | Existing manuscript statements at 82456b1 in Sections 5 and A; ledger entries C33, C62, C67, and C10. Relocation preserves measurement scope and observations; no new numerical claims. |
| Delete tiled-log capacity sentence from Appendix A.3 | Ledger lines 474-480 identifies an independent tiled-log implementation. Previous manuscript wording incorrectly attached this result to PyKeOps. The capacity claim is removed, not reassigned to another paper result. |
| Identify FIG-width as synthetic-tensor primitive measurements; retain training settings as application context | `studies/local_results/A100_WIDTH_COST_ENGINEERING_20260907T205000Z_73aec294/REPORT_ZH.md`, Sections 1, 2, 4, 5. Different primitive/component configurations are not summed into an application prediction. |
| Keep stopping-study LM/DC including simultaneous-completion neutrality | Current ledger lines 865-873 distinguishes valid LM/DC from invalid historical static-arm comparisons; this revision adds no static-derived stopping results. |

Visual contract: FIG-endpoints remains a lookup table grouped by E1/E2/E3; FIG-backends uses four explicit comparison blocks with separate denominators and statistical definitions. Both use editable LaTeX, black text, booktabs rules, and existing manuscript typography. Caption text lives with each table. All three plot assets are unchanged; FIG-width's contextual caption is corrected.

Local QA: compiled with latexmk; inspected rendered main-result/backend pages and both appendix pages for readable labels, alignment, and overflow. Table 5 and Table 6 retain their order. No overfull boxes or undefined references were reported. The supplied skills' missing companion audits remain unavailable; this is a local scientific/source and visual-readability review.

## Previous writing-only review revision

The current figure inventory is method/trace (Figure 1), primitive width cost (Figure 2), stopping/quality (Figure 3), and initial-width sensitivity (Figure 4, Appendix A.5). The old FIG-work assets were retired; Git retains them. Earlier design notes above describe the preceding revision where explicitly historical.

The three supplied skills guide the source-to-claim revisions, direct prose, and figure contracts. Scientific-critical-thinking was used to evaluate each requested change before accepting it; REVIEW_DISPOSITION.md records premise, impact, scope, action, and sources. The supplied figure skill's companion references and draw.io executable are unavailable. The method panel therefore uses editable TikZ and the manuscript's existing vector typography, based on the user's specified loop/trajectory layout rather than an AI-generated bitmap. This is a documented renderer fallback, not a claim of draw.io export or an external design audit.

Method figure contract: two panels, execution loop at left and recorded trajectory at right; black labels, blue executed-work area and grey removable-work area, complete passing-output branch and unfinished-state return. Exact counts come from the selected raw window. Width-scaling contract: 40 individual padding observations per W plus their mean; separate complete-configuration time ratios, reference line at one, logarithmic W axis with every tested width labeled. All points fit the displayed limits. The data packet preserves full-precision values; displayed labels use three significant digits. SVG text remains editable and export metadata is deterministic.

Table 4 now shows mean and sample SD rather than long decimal means. Point ratios in all tables/prose use three significant digits; narrow intervals retain resolution on the percent-ratio-change scale in Appendix A.1. Exact counts and software/input identities are not rounded. Table 5 and Table 6 retain their order and source insertion in Sections 5.4/5.5. Source and numeric QA includes all 18 quality summaries and all 200 width-window slot identities; see reviewer_reanalysis.py. Predicted application accuracy and the missing PyKeOps matched cell remain open, not implied by these figures.

## Current experiment integration: 2026-09-09

- Table 3 adds a third, explicitly separate PyKeOps block for every-update checking. Purpose: separate the matched execution comparison from older interval-two/four configurations. Inputs: matched campaign `analysis/summary.json:across_seeds` and seed medians; source mapping and aggregation are in `REVIEW_DISPOSITION.md`. Editable booktabs table, black text, original typography, no small-difference color coding. Caption identifies all denominators and statistical units.
- The 2026-09-10 Table 3 revision appends two labeled blocks: official POT/GeomLoss/Drain complete configurations and a direct completion-aware modification of POT 0.9.6.post1. The former is explicitly cross-backend and descriptive; the latter uses five paired same-backend rounds. The table retains absolute time, residual, memory, logical-work, and repeat-count cues so adverse and feasibility results remain visible.
- Table 7 is new: `FIG-controls.tex`, generated by `competitive_reanalysis.py` from five raw/analysis packets. Purpose: show absolute solver costs of indexed execution, entry skipping and DC beside independently calibrated model error. The displayed medians are rounded to three significant digits, while the prose reports sub-0.1% paired differences. Error ranges are descriptive across three methods/four repeats, not confidence intervals. Same-input and target-transfer rows are labeled. Source identities and full precision are preserved in `competitive_data.json`.
- Figure 2's caption now lists the synthetic dimension, tile and cost scale. Its plot is unchanged. Application time reconstruction uses its own calibration; no synthetic/application times are joined.
- Table 5/Section 5.4 and Table 6/Section 5.5 remain unchanged in numbering. New Table 7 belongs to Section 5.7; appendix tables shift to 8--10. Four existing figures keep their numbering. The navigator follows these labels.

Local visual review: rendered pages 4, 6, 9, 10 and 15 inspected at 1400-pixel page height. Table columns, comparison blocks, model equation, units and captions are readable without clipping or overlap. Black-on-white encoding does not depend on color. No graph axes are used to exaggerate the near-unity effects. This is an agent source/visual-readability check, not an external Product Design or Nature-style certification; the supplied figure skill's companion files remain unavailable. The 15-page PDF build has no overfull-box or undefined-reference warnings; full-text checks found no rendered campaign codes or the prohibited defensive boilerplate. Tables 1--10 and Figures 1--4 retain sequential numbering. Author approval remains separate from these checks.
