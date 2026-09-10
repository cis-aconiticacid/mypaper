# Batching to completion-aware execution revision

Status date: 2026-09-10. Scope: English manuscript plus the dedicated research
campaign `EXP-NATIVE-BATCH-SOLVERS-20260909`. Authorized GPU execution used
`gpumachine`; all campaign processes exited and the pre-existing `fwd` screen
was left untouched.

- [x] 1. Establish the value of batched EOT before describing its limitation.
  Reworked the abstract, introduction, background, and conclusion around joint
  execution of independent couplings.
- [x] 2. Audit concrete batching mechanisms rather than treating batching as a
  single baseline. Recorded the audited interfaces, stopping behavior, and
  output/state implications for POT, GeomLoss, OTT-JAX, LogSinkhornGPU,
  FlashSinkhorn, and PyKeOps in `BATCHING_IMPLEMENTATION_AUDIT.md`.
- [x] 3. State the central systems question explicitly. The introduction now
  asks how joint execution can be retained while further expensive updates to
  completed problems are avoided.
- [x] 4. Keep official implementations separate from study-built controls.
  Section 5.1 identifies the native OTT `jit(vmap(single solve))` reference and
  labels fixed-phase, logical-mask, active, and PyKeOps variants as study
  implementations.
- [x] 5. Run actual official-release native batch configurations. POT
  0.9.6.post1 `ot.solve_batch` and GeomLoss 0.2.6 `SamplesLoss` were run on
  frozen real ImageNet-32 PCA500 inputs under a common external output audit.
  Cross-backend values are labeled complete-configuration endpoints, including
  the result that unmodified POT is fastest in the measured cells.
- [x] 6. Directly modify the other solver rather than DrainSinkhorn. POT's own
  batched log-Sinkhorn loop now detects completion per problem and physically
  compacts its live cost, marginals, and dual state. Five paired unmodified /
  modified POT rounds were run at both sizes; DrainSinkhorn is excluded from
  this causal comparison.
- [x] 7. Preserve failures and costs. GeomLoss interface and residual failures,
  its one-run 508 s representative feasibility result, the nearly neutral
  small-POT modification result, and the modified path's higher peak memory
  all remain in the campaign, results inventory, and manuscript.
- [x] 8. Audit the manuscript for defensive/rebuttal language and internal
  evidence codes. Necessary numerical, timing, hardware, and statistical
  boundaries are retained; implementation-context prose is stated directly.
- [x] 9. Regenerate/check derived material, compile, inspect the rendered PDF,
  and deliver through the English-paper repository. `ALL_RESULTS.md` and Table
  3 now include the official-native and direct-POT-modification results.

Open evidence gaps after this revision:

- A matched same-backend POT timing is now available for a direct modification
  of POT 0.9.6.post1. The two measured input cells do not estimate a workload
  population or other POT versions.
- GeomLoss 0.2.6 does not expose resumable iteration state or a tolerance
  through the released `SamplesLoss` surface. A direct GeomLoss source
  modification remains unmeasured; the development `geomloss.ot.solve_batch`
  interface is not represented as a released feature.
- LogSinkhornGPU and the upstream FlashSinkhorn kernel remain unmeasured in the
  new common-endpoint campaign.
- The paper's native OTT comparison bundles the official solver interface with
  a phase-control change; the fixed-phase/active comparison is therefore the
  narrower completion-removal contrast.
- PyKeOps supplies the batched operator; static, masking, and active retirement
  are study-built solver/executor variants.
- The existing real-workload experiments do not estimate the population
  frequency of favorable completion heterogeneity.
