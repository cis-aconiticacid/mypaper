# Citation metadata and context audit

Date: 2026-08-26 UTC

Scope: the 14 citation keys actually used by the endpoint-first draft.

Method: the main agent compared every entry and its citing sentence with the
canonical PMLR, JMLR, NeurIPS, arXiv, or official POT release page.  No reviewer
subagent was used because subagents are reserved for experiment monitoring in
this task.  This document therefore records a direct-source main-agent audit,
not the independent cross-model `citation-audit` assurance artifact.

## Result

- Existence: 14/14 verified.
- Metadata after correction: 14/14 consistent with the canonical source.
- Context: 14/14 citation uses support the surrounding method-family statement.
- Bibliography scope: `references.bib` contains exactly the 14 cited keys.

## Corrections applied

1. `pot2025batch`: replaced the synthesized title “POT 0.9.6 Release:
   Batch-Parallel Optimal Transport Solvers” with the source-faithful title
   “POT 0.9.6 Release Notes.”  The official release page states that 0.9.6 added
   `ot.batch` with batch-parallel Sinkhorn, GW, and FGW solvers.
2. `altschuler2017near`: restored the canonical author name Jonathan
   Niles-Weed and corrected the NeurIPS paper URL.
3. `cuturi2013sinkhorn`: added the canonical NeurIPS page range 2292--2300.

## Per-entry ledger

| Key | Canonical source | Existence / metadata | Citing claim | Context verdict |
|---|---|---|---|---|
| `cuturi2013sinkhorn` | [arXiv / NeurIPS 2013](https://arxiv.org/abs/1306.0895) | verified | entropic OT and Sinkhorn scaling | supports |
| `feydy2019sinkhorn` | [PMLR AISTATS 2019](https://proceedings.mlr.press/v89/feydy19a.html) | verified | large-scale GPU Sinkhorn computations | supports |
| `cuturi2022ott` | [arXiv 2201.12324](https://arxiv.org/abs/2201.12324) | verified | JAX/vectorized/accelerator OT toolbox | supports |
| `ye2026flashsinkhorn` | [arXiv 2602.03067](https://arxiv.org/abs/2602.03067) | verified | fused, tiled, linear-memory FlashSinkhorn | supports |
| `amos2023meta` | [PMLR ICML 2023](https://proceedings.mlr.press/v202/amos23a.html) | verified | learned/amortized OT proposals | supports |
| `thornton2023initialization` | [PMLR AISTATS 2023](https://proceedings.mlr.press/v206/thornton23a.html) | verified | Sinkhorn initialization affects runtime | supports |
| `zhang2025large` | [arXiv 2506.05526](https://arxiv.org/abs/2506.05526) | verified | large Sinkhorn couplings and Flow Matching | supports |
| `flamary2021pot` | [JMLR 22(78)](https://www.jmlr.org/papers/v22/20-451.html) | verified | POT solver toolbox | supports |
| `pot2025batch` | [official POT releases](https://pythonot.github.io/releases.html) | verified after title fix | batch-parallel POT interfaces | supports |
| `altschuler2017near` | [NeurIPS 2017](https://papers.nips.cc/paper_files/paper/2017/hash/491442df5f88c6aa018e86dac21d3606-Abstract.html) | verified after author/URL fix | Greenkhorn coordinate update family | supports |
| `thibault2017overrelaxed` | [arXiv 1711.01851](https://arxiv.org/abs/1711.01851) | verified | overrelaxed Sinkhorn family | supports |
| `scetbon2021lowrank` | [PMLR ICML 2021](https://proceedings.mlr.press/v139/scetbon21a.html) | verified | low-rank Sinkhorn family | supports |
| `kemertas2025truncated` | [arXiv 2504.02067](https://arxiv.org/abs/2504.02067) | verified | truncated-Newton OT family | supports |
| `pooladian2023multisample` | [PMLR ICML 2023](https://proceedings.mlr.press/v202/pooladian23a.html) | verified | minibatch couplings in Flow Matching | supports |

## Context boundary

The related-work paragraph cites these papers as method families or backend
interfaces.  It does not claim that they implement candidate-axis retirement,
nor that their independent speedups multiply with this paper's endpoint
results.
