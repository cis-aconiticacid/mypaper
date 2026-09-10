# Batching to completion-aware execution revision

Status date: 2026-09-10. Scope: the English manuscript and research campaign
`studies/campaigns/EXP-NATIVE-BATCH-SOLVERS-20260909` (research paths below).
The central comparison applies completion-aware execution directly inside a
third-party solver, with that solver's corresponding full-width control.

- [x] Establish batching's value and explain the audited common-stop or
  fixed-schedule mechanisms. Source: `sections/0_abstract.tex`,
  `sections/1_introduction.tex`, `sections/2_setting_related.tex` and
  `BATCHING_IMPLEMENTATION_AUDIT.md`.
- [x] Audit upstream inputs, actual update loops, stopping, state and outputs.
  Source: pinned links in `BATCHING_IMPLEMENTATION_AUDIT.md`.
- [x] Run the original official-release feasibility and accuracy tests;
  preserve all cross-backend A results in `ALL_RESULTS.md` and
  `support/figure_materials/native_batch_results.json`. Their absolute times
  no longer occupy the main within-backend comparison table or contribution
  argument. Source: campaign `analysis/summary.json` and `REPORT_ZH.md`, A.
- [x] B: modify POT 0.9.6.post1's native loop directly and compare with
  unmodified POT. Five pairs at each size; retain the nearly neutral small
  case and increased peak allocation. Source: campaign
  `code/pot_batch_completion_aware.py` and `analysis/summary.json`.
- [x] C: inspect the GeomLoss release and development paths before choosing
  a modification. Both audited paths use a schedule, and the development
  argument check rejects a non-null tolerance. Source: audit source links and
  campaign `provenance/upstream_geomloss_0.2.6/`.
- [x] C: insert residual refinement directly inside official GeomLoss 0.2.6
  after unchanged annealing, with the same refinement in both full-width and
  compacted controls. This is explicitly a method extension relative to
  official GeomLoss. Source: campaign
  `provenance/geomloss_completion_aware_plan.json`,
  `code/geomloss_completion_aware.py` and
  `raw/geomloss_completion/geomloss_executed_loop.py`.
- [x] Verify official/no-op bitwise equivalence, then run five matched pairs
  at both sizes. All twenty formal arm outputs pass the unchanged external
  residual gate; all ten pairs return identical potentials and completion
  depths. Source: campaign `analysis/geomloss_completion_summary.json`,
  including raw paths and hashes. Source-insertion failure, original `.99`
  residual failures, and large-input memory increase are retained.
- [x] Update the evidence ledger and navigation, this TODO, the English
  all-results inventory, Table 3, and evidence-supported prose. Source:
  campaign `REPORT_ZH.md`, paper-side `geomloss_completion_results.json`,
  `FIG-backends.tex`, and `sections/5_experiments.tex`.
- [x] Run anti-defensive-writing review, compile and inspect the PDF, and
  commit/push the related paper changes. Source: current-turn entry in
  `support/audits/VISUAL_REVIEW.md` and the corresponding Git commit.

Remaining scope, not unfinished promised measurements:

- A pure scheduling-only GeomLoss original/modified residual-stop contrast
  does not exist for the audited fixed-schedule path. C identifies the
  incremental benefit inside the common residual extension. No original/C
  ratio is called compaction-only acceleration.
- C covers balanced, non-debiased, tensorized FP32 inference on two fixed
  batches, not autograd, online/KeOps, multiscale or a workload population.
  Original caller cost tensors remain resident for final extrapolation.
- LogSinkhornGPU and the upstream FlashSinkhorn wrapper remain source-audited
  but unmeasured in this campaign. They were optional, and no missing timing
  claim is imputed to them.
- Native OTT/active includes a phase-control change; matched fixed-phase/active
  is the narrower contrast. PyKeOps variants are study-built solver controls.

Sources for these scope statements: `BATCHING_IMPLEMENTATION_AUDIT.md`,
campaign `REPORT_ZH.md`, C, and `analysis/geomloss_completion_summary.json`.
