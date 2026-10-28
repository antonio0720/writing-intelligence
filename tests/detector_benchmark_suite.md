# Detector Scores — Retired as a Benchmark

**Status:** retired in v9 (P0-12 / WI9-05A). Project owner: Antonio T. Smith Jr.

Earlier versions of this file described a methodology for running compiler
output through commercial AI detectors and treating a "human" classification
as a pass, with compiler changes tuned against what those tools measure.
That methodology is withdrawn. It contradicted Writing Intelligence's own
refusals (`references/v4/NON_GOALS.md`, `references/v7/README.md`): a system
built to give a checkable account of how a document came to exist cannot also
be a system for concealing how it came to exist.

## The rule

1. **Never a target.** No pass, operator, rule or rewrite is tuned to raise,
   lower or predict an AI-detector score.
2. **Never a gate.** No release, review or quality decision depends on a
   detector result, and a "human" classification is never evidence that a
   person wrote a passage.
3. **Never a claim.** No document or output may claim that it evades,
   passes or fools a detector, or that a detector classified it as a
   person's writing.
4. **Archive only.** If someone runs a detector, the result may be recorded as
   an external observation — tool, version if known, date, raw output — and it
   changes no finding and no fix. A commercial score is not a calibrated
   probability of authorship; its configuration and validation data are
   usually unknown.

## What replaces it

Writing quality is judged by people, against the author's own material:

- **Track A — deterministic integrity:** source anchors, claim coverage,
  pinned digests, venue authorship rules
  (`scripts/wi-authorship.py`, `scripts/wi.py verify`).
- **Track B — reader and author judgment:** the blinded editorial protocol in
  [`references/v9/QUALITY_BENCHMARK.md`](../references/v9/QUALITY_BENCHMARK.md)
  and the editorial gates in
  [`references/v9/EDITORIAL_PROTOCOL.md`](../references/v9/EDITORIAL_PROTOCOL.md).

The editorial adversarial cases in [`adversarial_cases.md`](adversarial_cases.md)
attack a draft the way a hard reader would; none of them reads a detector.
