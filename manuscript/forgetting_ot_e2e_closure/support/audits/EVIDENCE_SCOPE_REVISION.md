# Evidence-scope revision, 2026-09-05

This local revision binds the English paper and its corresponding Chinese
translation to the experiment ledger and the sources hashed in
`EVIDENCE_SCOPE_REVISION.json`. It does not add GPU runs or change frozen raw
records. No arXiv, GitHub, SSH, or other remote update was performed.

## Changes

- Correct C35 to projected-carry project width-one versus complete
  shared-anchor active packed execution. Correct its proposal configuration
  and distinguish it from a matched static/active ablation.
- Add a scope table for C66, C62/C63, C67, C55, C33, C80-LM and EXP-PACKER19,
  retaining neutral results, timing scopes, sample/replication units, and the
  exclusion boundaries of the contributing campaigns.
- Reanalyze existing C63 per-seed solver fields: static/active ratios
  1.057667531, 1.071587200, 1.033062456; geometric mean 1.053984982.
  These are separate from the complete-training 1.035560919 ratio.
- Reanalyze existing EXP-PACKER19 paired records with equal host weights:
  static/PC 1.000393455, 1.000080489, 1.000033725, 0.999711663,
  0.999634918 at the five ordered tolerances. Plot these alongside LM/PC.
  No new confidence interval or equivalence claim is made.
- Include C80-LM phase medians with an explicit prohibition on treating their
  sum as the paired total or transferring them to EXP-PACKER19.
- Express break-even using incremental overhead relative to the static path,
  which has its own checking costs. Preserve the distinction between
  removable work, net runtime savings, and a validated predictive scheduler.
- Bound headline uncertainty to timing reproducibility and remove repeated
  claims of unspecified state-of-the-art performance.

## Reproduction

From the repository root:

```powershell
python manuscript/forgetting_ot_e2e_closure/support/figure_materials/derive_paired_attribution.py
python manuscript/forgetting_ot_e2e_closure/support/figure_materials/plot_packer19_stopping_metrics.py
```

Compile `main.tex` in the English manuscript directory and `main_zh.tex` in
the Chinese directory with pdfLaTeX, repeating until references settle.
Figure hashes are recorded in `figures/provenance.json`; the new paired
analysis records source hashes in `figures/PAIRED_ATTRIBUTION.json`.

## Remaining evidence boundaries

- The cost responsible for the newer Packer19 static/PC near-unity result
  remains unidentified by this revision; old phase timings are not an answer.
- C33 uses controlled overlapping supports. It is not a warm-start ablation
  in independently resampled OT-FM training.
- M3's locally available source-bound summary does not provide the absolute
  arm-time and width-trajectory records needed for a new survival-curve plot.
  No such records were reconstructed from ratios.
- C68 and EXP-M5 do not establish a deployable depth predictor. Reproducible
  timing on frozen cells does not establish universal workload gains.
- This revision retains the current article layout. It is not a conversion
  to an anonymous venue-specific submission template.

## Local validation and delivery

Both corresponding PDFs were compiled with settled cross-references and
visually inspected, including the updated plots, scope table, and appendix.
The English PDF has 14 pages; the Chinese PDF has 12 pages. A pre-existing
0.69 pt Chinese table overfull warning and italic-font substitution remain;
no clipped content was observed. Source hashes and paired-record counts were
checked. These are local document and analysis checks, not new GPU evidence.

- `output/pdf/DrainSinkhorn_20260905.pdf`
- `output/pdf/DrainSinkhorn_20260905_zh.pdf`

## Selective anti-defensive pass

Applied anti-defensive-writing after commit `615be07b`. Removed repeated
negative disclaimers and condensed experiment, discussion, conclusion, and
appendix prose by approximately 530 English words. Retained paired contrasts,
timing and statistical units, neutral results, calibration exclusions, and the
unresolved EXP-PACKER19 cost attribution. Updated the corresponding Chinese
translation. Removed the English experiment-end float barrier to avoid a
large blank area after shortening. Both final PDFs were rebuilt and visually
inspected: English 13 pages, Chinese 11 pages. Labels, citations and result
macros match across the revised bilingual passages. No measurements changed.

## Focused scope restoration

Reviewed the deletions in `60007ba8`. Restored affirmative conditions for
timing intervals, campaign-local interpretation, phase-summary aggregation,
and M3 fixed-depth accounting. Changed Packer19 runtime matching to observed
ratios close to one. Clarified that M3 measures grouping effects. Other
already-explicit scope statements were retained. Both corresponding PDFs
were compiled and visually checked (13 English / 11 Chinese pages).
