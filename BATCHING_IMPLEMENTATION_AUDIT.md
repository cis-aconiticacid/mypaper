# Source-backed batching implementation audit

Audited 2026-09-09 for the DrainSinkhorn manuscript. This record distinguishes
an API that accepts a batch, the mechanism that executes that batch, its
stopping rule, and whether completed problems stop receiving expensive work.
Claims are scoped to the pinned revisions below.

## Interface and execution comparison

| System (pinned source) | Independent-problem input | How batching is constructed | Stopping and completed-problem behavior | Output/state implication | Role in the manuscript |
|---|---|---|---|---|---|
| [POT `6372a66`](https://github.com/PythonOT/POT/tree/6372a66b732c440967e5a943d67b03a58ace5243) | `solve_batch` accepts a cost tensor `(B, n, m)` and batch marginals `(B, n)` and `(B, m)`; `dist_batch` can build distinct costs from distinct source and target samples. | Native batch API; the Sinkhorn projection updates whole batch tensors in one Python loop. | The audited Sinkhorn and log-Sinkhorn paths compute per-item marginal norms, take their batch maximum, and break the common loop only when that scalar is below tolerance. No per-problem skip, retirement, or active-width reduction appears in these paths. | Returns a `(B, n, m)` plan and one iteration count for the batch. | Unmodified release 0.9.6.post1 is an actual complete-configuration baseline. A separate experiment directly modifies this POT loop for per-problem retirement; unmodified POT is its same-backend control. |
| [GeomLoss release 0.2.6](https://pypi.org/project/geomloss/0.2.6/) and development source [`00e493f`](https://github.com/jeanfeydy/geomloss/tree/00e493f36bd6cc8471526e59afc07193a1926e47) | Release 0.2.6 accepts batch-shaped weights and point clouds through `SamplesLoss`. The distinct-cost `geomloss.ot.solve_batch` interface exists in the audited development source but is absent from 0.2.6. | Released `SamplesLoss` carries the batch through its tensorized reductions; the development matrix path is a separate native batch API. | Release 0.2.6 uses a shared epsilon-scaling schedule with no tolerance argument. The development path also advances a shared schedule and does not support a non-null rigorous stopping tolerance. Neither audited path retires individual batch members. | The measured release returns batch dual potentials. Development `solve_batch` returns an `OTResult`. | Release 0.2.6 is an actual complete-configuration baseline; `.99` and `.999` residual failures and the passing `.9999` schedule are all reported. Development `geomloss.ot.solve_batch` is not called a released interface. |
| [OTT-JAX `98612bd`](https://github.com/ott-jax/ott/tree/98612bd1ba4b7c1217e28215905e8117439cc57c) | The official tutorial constructs multiple independent histogram pairs and maps the single-problem Sinkhorn function over their batch axes. | `jax.jit(jax.vmap(...))`, not a separate native `solve_batch` entry point in the audited tutorial. | The single solver has its own convergence loop, but the official batching tutorial warns that differing termination behavior is detrimental to compiled parallel execution and compares it with a common fixed iteration count. The tutorial does not compact active problem state. | Vectorized outputs retain the mapped batch axes; JAX controls the lowered storage. | The paper's only timed official/native batch reference: `jit(vmap(full Sinkhorn))`. The fixed-phase and active variants are study implementations, so native/active is descriptive while fixed-phase/active isolates retirement more narrowly. |
| [LogSinkhornGPU `58ac43c`](https://github.com/OTGroupGoe/LogSinkhornGPU/tree/58ac43cce9cbbda66381f7c47ab05443edc8049c) | The Torch path accepts `(B, M, N)` costs (or a shared cost); the KeOps path accepts batch-specific or shared source/target coordinates. | Batch-shaped Torch or KeOps operations inside one solver object and one outer iteration loop. | The audited error function reduces marginal error to one scalar sum across all dimensions, including batch, and the outer loop uses that scalar for a common stop. No completed-problem skip or active-width reduction is present. | Potentials and marginals retain the original batch dimension. | Source-level mechanism comparison only; no performance claim against DrainSinkhorn. |
| [FlashSinkhorn `82a6d32`](https://github.com/ot-triton-lab/flash-sinkhorn/tree/82a6d32f43f136c5db195b27be474c477a28f37f) | The high-level samples API accepts separate `x` and `y` tensors shaped `(B, N, D)` and batch weights. | At the audited wrapper, batched inputs are iterated with Python `zip`; each problem calls the single-problem implementation and results are stacked. | Each call follows its per-problem schedule. This wrapper avoids a common-stop fused batch, but it is sequential at the problem level and does not maintain a compacted active batch. | Stacked per-problem costs or potentials; temporary state is per call. | Strong fused per-problem update prior art; not an official native multi-problem execution baseline for the paper's completion-aware comparison. |
| [PyKeOps `ef72bc9`](https://github.com/getkeops/keops/tree/ef72bc907df78cd18bff866d3dc7cb6375f11a4d) | `LazyTensor` supports broadcasting and arbitrary batch dimensions for symbolic reductions, allowing each batch element to carry distinct supports or parameters. | Native batched operator/reduction layer, not a complete EOT solver with a stopping policy. | Completion detection and retirement belong to the caller. The static, logical-mask, and active PyKeOps solvers timed in the paper were built for this study. | Materialized tensors appear only at reductions/results; solver state layout is caller-defined. | Backend-transfer evidence for the completion-aware executor, not an official PyKeOps solver baseline. |

## Direct source locations

- POT batch interface: [`ot/batch/_linear.py` lines 245-425](https://github.com/PythonOT/POT/blob/6372a66b732c440967e5a943d67b03a58ace5243/ot/batch/_linear.py#L245-L425). Common Sinkhorn loop and batch-maximum error: [`ot/batch/_utils.py` lines 137-171 and 279-301](https://github.com/PythonOT/POT/blob/6372a66b732c440967e5a943d67b03a58ace5243/ot/batch/_utils.py#L137-L171).
- GeomLoss batch contract: [`matrix.py` lines 520-681](https://github.com/jeanfeydy/geomloss/blob/00e493f36bd6cc8471526e59afc07193a1926e47/src/geomloss/ot/_implementations/matrix.py#L520-L681). Shared iteration schedule: [`sinkhorn_ot.py` lines 221-272](https://github.com/jeanfeydy/geomloss/blob/00e493f36bd6cc8471526e59afc07193a1926e47/src/geomloss/ot/_abstract_solvers/sinkhorn_ot.py#L221-L272). Stopping-tolerance status: [`_arguments.py` lines 43-49](https://github.com/jeanfeydy/geomloss/blob/00e493f36bd6cc8471526e59afc07193a1926e47/src/geomloss/_arguments.py#L43-L49).
- OTT official batching tutorial: [`000_One_Sinkhorn.ipynb`](https://github.com/ott-jax/ott/blob/98612bd1ba4b7c1217e28215905e8117439cc57c/docs/tutorials/linear/000_One_Sinkhorn.ipynb), including the double-`vmap` construction and the discussion of heterogeneous termination. Study-native wrapper provenance: research source `studies/code/ottjax_phase_active_core.py`, `NativeFactory`, read-only audit on 2026-09-09.
- LogSinkhornGPU batch shapes, error reduction, and loop: [`sinkhorn.py`](https://github.com/OTGroupGoe/LogSinkhornGPU/blob/58ac43cce9cbbda66381f7c47ab05443edc8049c/LogSinkhornGPU/sinkhorn.py).
- FlashSinkhorn high-level batch loop and stack: [`samples_loss.py` lines 638-682](https://github.com/ot-triton-lab/flash-sinkhorn/blob/82a6d32f43f136c5db195b27be474c477a28f37f/torch-ext/flash_sinkhorn/samples_loss.py#L638-L682).
- PyKeOps batch dimensions: [`lazy_tensors.rst` lines 183-190](https://github.com/getkeops/keops/blob/ef72bc907df78cd18bff866d3dc7cb6375f11a4d/doc/engine/lazy_tensors.rst#L183-L190).

## Evidence admissibility for the current paper

- Direct causal comparisons remain within a backend and hold stopping and
  checking semantics fixed: Packer19 logical mask versus compaction, OTT
  fixed-phase versus active, matched PyKeOps static/mask versus active, the
  MetroPT-3 physical/indexed/in-place controls, and unmodified POT versus the
  direct completion-aware modification of POT's own native batch loop.
- The native OTT ratio is retained as a complete-configuration reference. It
  changes the solver interface and phase control in addition to active
  retirement, so it is not the compaction-only estimate.
- The new POT/GeomLoss/Drain experiment uses frozen real inputs, a common
  verified endpoint, FP32 with TF32 disabled, and separately recorded H2D and
  warmup. Its cross-backend seconds rank complete configurations only: POT is
  fastest in the measured cells. They are not a compaction-only estimate.
- The direct POT modification imports no DrainSinkhorn implementation. At
  `n=4096,W=16` it reduces logical problem-iterations by 25.5% and yields a
  five-pair unmodified/modified geometric mean of 1.292x. At `n=1024,W=8`,
  15.9% fewer logical slots yield only 1.023x and the paired range crosses one.
  Peak allocated memory rises at both sizes.
- LogSinkhornGPU, upstream FlashSinkhorn, and an official PyKeOps solver remain
  unmeasured in the new common-endpoint campaign.

## Executed campaign and provenance

The authoritative run record is the research campaign
`studies/campaigns/EXP-NATIVE-BATCH-SOLVERS-20260909`. It contains 56 result
JSON files (52 valid, three residual failures, one interface failure), frozen
input sidecars, execution-order plans, exact installed POT source files, a
direct POT modification with SHA-256 identity, package RECORD hashes, commands,
H2D/warmup separation, per-problem residuals, memory measurements, and the
analysis summary. The paper-side transcription is
`manuscript/forgetting_ot_e2e_closure/support/figure_materials/native_batch_results.json`.
