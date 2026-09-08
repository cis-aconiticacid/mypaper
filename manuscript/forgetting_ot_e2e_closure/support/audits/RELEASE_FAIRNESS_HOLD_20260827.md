# Release-fairness evidence hold

Status: `ACTIVE / DO NOT CITE C59-C60 ACTIVE-STATIC TIMINGS`

The 2026-08-27 audit found that the static controls in C59, C60, and the first
C61 scaling run performed `2W-1` upstream release-verifier calls per window,
while the active arm performed `W`.  The extra static calls were used to record
verified early first passage even though static execution does not release a
lane early.  This contaminates the active/static timing comparison.

The fail-closed evidence rule is now:

- active: each lane is verified once when it retires;
- static: no early per-lane verification; all lanes are verified exactly once
  at the common final boundary;
- every timed result must have
  `release_verified_candidate_count == candidate_width`.

The corrected implementation begins at commit
`5d057deeede068c250789fa9d3425998e2707a87`.  C59/C60 remain useful as
deployment and systems diagnostics, but their active/static timing values are
on hold.  The hold may be removed only after the replacement C65/C66 raw data,
consumer gates, hashes, and fail-closed analyzers pass.

