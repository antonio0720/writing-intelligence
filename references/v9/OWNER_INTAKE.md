# Writing Intelligence v9 — what only the owner can supply

**Project owner:** Antonio T. Smith Jr. — Density6 LLC. **Status:** waiting on the owner. Nothing in this file has been collected.

Two v9 gates cannot be met by code, and must not be met by invention: a blinded editorial benchmark (WI9-07) and an independent human review (WI9-09). The tools to receive each are built and tested. This page says exactly what to provide and what runs on it.

**Voice samples are not on this list.** v9 is built for every writer, and each writer measures their own voice from their own writing on their own machine ([`VOICE_BASELINE.md`](VOICE_BASELINE.md)). The owner's writing is never required, never committed and never shipped.

## 1. The 60-case editorial benchmark (WI9-07)

The design is [`QUALITY_BENCHMARK.md`](QUALITY_BENCHMARK.md): 15 cases each for journalism and expert commentary, executive correspondence, fiction, and technical or institutional work; arms v8 and v9 on identical source material; blinded, randomized labels; the eight 1–5 criteria.

**Decide before any score is seen** (record the decision with a date, in this repository, and do not change it afterwards): the number of independent reviewers per case, what counts as an improvement (for example a median v9-minus-v8 delta above zero on evidence integrity and original thought with no criterion worse), and the zero-tolerance invariants (no invented firsthand event, no human-only venue violation, no silent consequential change).

**Provide:** the consented source material for each case, from contributors who agreed to it, kept private and out of the repository; the reviewers, who did not build v9 and are not shown which arm is which; and their ratings in this shape:

```json
{"ratings": [
  {"case_id": "journalism-01", "reviewer_id": "R1", "arm": "v8",
   "scores": {"original_thought": 3, "evidence_integrity": 4, "voice_fidelity": 3,
              "argument_consequence": 3, "reader_usefulness": 4, "natural_phrasing": 4,
              "uncertainty_discipline": 3, "editorial_restraint": 4},
   "critical_violations": 0}
]}
```

**Run:**

```bash
python3 prototypes/wi9/wi9_core.py benchmark --root ~/wi9-private/benchmark --input ratings.json
```

It holds until 60 distinct cases each have a matched v8 and v9 rating from the same reviewer, holds on any critical violation, and reports the median and quartiles of the v9-minus-v8 difference per criterion. It never reports a detector score. A failed pilot is a valid, reportable outcome.

## 2. Independent review (WI9-09)

An automated security and correctness review of the v9 code was run from a fresh context and its findings recorded in [`defects.md`](defects.md). That is not the review WI9-09 requires. WI9-09 needs a person who did not build v9 to read the code, the receipts and this program and record a decision. Name the reviewer; their findings are added to `defects.md` and their decision to a receipt.

## What is not waiting on the owner

Everything else in [`WAVES.yaml`](WAVES.yaml) marked open is engineering work: the private vault (WI9-02), the thought-fidelity pass (WI9-04), and the last WI9-08 items listed there.
