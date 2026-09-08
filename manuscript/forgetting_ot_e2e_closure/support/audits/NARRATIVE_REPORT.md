# DrainSinkhorn narrative report

Updated: 2026-09-07

## Paper identity

**Title:** `DrainSinkhorn: Safe Elimination for Batched Entropic Optimal Transport`

**Retellable sentence:** Fast inner kernels make one Sinkhorn update cheaper;
DrainSinkhorn stops issuing updates to problems that have already completed.

The name is a drain/sink pun for the complete dynamic-compaction system, not the
name of any individual component or a reference to transported mass.

## Main story

A fast batched kernel still executes at full physical width until the deepest
solve finishes. Unequal completion depths therefore create a rectangle of
padded problem-update work. Standard batched execution applies the original
per-instance Sinkhorn map along a problem-batch dimension. DrainSinkhorn uses
the selected solver's stopping rule as the release authority and physically
removes passing problems from every per-problem tensor.

The numerical claims are empirical and follow four evidence levels:

1. algebra shows that standard fixed-width batching retains the per-instance update;
2. work identities quantify the updates removed by dynamic compaction;
3. parity, residual, and finite-precision stress tests measure numerical behavior;
4. consumer and training endpoints measure application-visible behavior.

## Mathematical spine

For completion depths \(\ell_1,\ldots,\ell_W\),

\[
S_{\mathrm{active}}=\sum_k A_k=\sum_t\ell_t,
\qquad
S_{\mathrm{static}}=W\ell_{\max}.
\]

The removed padding is

\[
R=W\ell_{\max}-\sum_t\ell_t.
\]

For a random window, \(\mathbb E[R]>0\) exactly when some depth level has
positive probability of containing both completed and unfinished lanes:

\[
\Pr(0<A_k<W)>0.
\]

The exact matched-path time difference is

\[
T_{\mathrm{fixed}}-T_{\mathrm{active}}
=\sum_k[c_k(W,\xi_k)-c_k(A_k,\xi_k)]-\Delta H.
\]

Depth heterogeneity creates removable work. The measured width-cost function
determines its hardware conversion, and the summed cost decrease must exceed
incremental control overhead. On the measured A100/Triton configuration, the
packed-update cost is wave-shaped: the first large increase occurs at width
6 to 7 for n=1024 and width 1 to 2 for n=4096, while n=16384 is responsive from
width one. Source: `studies/local_results/A100_WIDTH_COST_ENGINEERING_20260907T205000Z_73aec294/REPORT_ZH.md`, lines 7--16, and
`algorithm/src/sinkhorn_ops/_flash_packed_triton.py`, line 212.

## Evidence ladder

1. **Matched dynamic-compaction acceleration:** fixed-width/dynamic-compaction comparisons give
   1.745535x on the C82 four-worker MetroPT-3 E2 endpoint, 1.753803x in the
   separate C66 two-host E1 analysis, 1.054x on the ImageNet-32 solver field,
   and 1.616--3.110x in the registered MetroPT scale cells. OTT-JAX gives
   1.366--1.581x before the
   1e-2 synchronized-completion boundary. Packer19 LM/DC gives 1.480--1.638x
   before its synchronized-completion boundary.
2. **Implementation context:** POT `solve_batch` and OTT-JAX `vmap` establish
   ordinary multi-problem Sinkhorn batching. DrainSinkhorn's component
   comparison begins at fixed-width/dynamic-compaction or logical-mask/dynamic-compaction.
3. **Timing scope:** C82 measures the ready-arrays-to-consumer makespan across
   four complete-device workers. C66 separately reports a two-host E2 endpoint
   and a paired-consumer-subtracted E1 result. Each ratio stays within its own
   campaign and timing interval.
4. **Stopping-controller Pareto:** EXP-PACKER19 reports actual residual, output
   TV, OT time, and LM/DC at five common residual tolerances. TV is a numerical
   output-stability diagnostic.
5. **Dynamic compaction:** C80-LM first showed logical masking is neutral at
   1.00007x because the kernel width does not shrink, while dynamic compaction
   gives 1.540x at the registered 1e-3 cell. EXP-PACKER19 extends the matched
   comparison across tolerances: 1.480--1.638x before becoming neutral at 1e-2,
   where all lanes first pass on the same audit.
6. **Component attribution:** batched two-sided checking gives 1.133x and the
   one-marginal precheck gives 1.105x in the matched Packer19 paths.
7. **Mechanism intervention:** with the same 32 MetroPT problems and total
   correction work, stronger within-window depth heterogeneity increases the
   static/active ratio from 1.105x to 1.217x and 1.235--1.271x on random layouts.
8. **End-to-end transfer:** MetroPT-3, Packer19, and ImageNet-32 feature OT-FM
   endpoint campaigns show the measured effect after their registered consumer
   or training work. Their E2/E3 timing scopes are stated with each result.
9. **Numerical behavior:** shadow replay finds zero already-ready lanes among
   1488 screen-negative events; maximum screen/full-check row-residual discrepancy
   is 1.86e-7. C10 records three raw FP32 and three TF32 accept disagreements
   relative to FP64 replay, and zero disagreements for outward-bound plus FP64
   escalation across 100 stress cases. These are measured outcomes.
10. **Scale-out:** independent complete-device workers avoid per-update Sinkhorn
    collectives. One-to-four fixed-per-worker throughput scales 3.965--3.979x on
    held-out MetroPT routes.
11. **Cross-backend realization:** packed Triton, OTT-JAX, and
    PyKeOps adapters show positive backend-matched execution gains on the tested
    heterogeneous batched-EOT tasks. Kernel fusion, active-state layout,
    compaction, memory reuse, and backend-specific scheduling remain open
    optimization axes.

## Related-work boundary

POT `solve_batch` and OTT-JAX `vmap` establish fixed-width multi-problem
Sinkhorn execution. Orca, automatic batching, Ginkgo, and jaxipm establish
general heterogeneous iteration execution. The one-marginal precheck and the
configured two-marginal stopping rule are existing Sinkhorn mechanisms.
DrainSinkhorn contributes dynamic per-problem state compaction after that
release rule and a depth-to-work account for the resulting survivor batches.

`DrainSinkhorn = fewer and narrower updates across completed/unfinished problems`

## Claim hierarchy

- Lead with matched fixed-width/dynamic-compaction and logical-mask/dynamic-compaction evidence.
- Use matched logical-mask/dynamic-compaction controls for causal attribution.
- Lead Packer19 with the same-controller Pareto and compaction boundary.
- Do not report a speedup ratio across different stopping interfaces.
- Report endpoint ratios as application transfer, not as the primary OT speed.
- Treat parity, residual replay, and C10 as empirical numerical evidence.
- State the survivor-width and width-cost conditions together. Apply measured
  wave locations only to their recorded device, kernel path, and configuration.
