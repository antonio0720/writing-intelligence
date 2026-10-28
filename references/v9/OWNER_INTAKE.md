# Writing Intelligence v9 — what only the owner can supply

**Project owner:** Antonio T. Smith Jr. — Density6 LLC. **Status:** waiting on the owner. Nothing in this file has been collected.

Three v9 gates cannot be met by code, and must not be met by invention: a consented voice corpus (WI9-03), a blinded editorial benchmark (WI9-07), and an independent human review (WI9-09). The tools to receive each are built and tested. This page says exactly what to provide and what runs on it.

## 1. Voice samples (WI9-03)

**Provide, per genre you want a voiceprint for:** at least three pieces you wrote yourself, without model drafting or substantive model rewriting, each at least 500 words. Different occasions within one genre are better than three parts of one piece. Mixed genres are refused; build one baseline per genre.

**Keep them private.** Put them outside this repository, for example `~/wi9-private/voice/<genre>/`. They never go into a commit, a PR, CI or a bundle.

**Record consent and digests** in `~/wi9-private/voice/<genre>/voice.json`:

```json
{
  "samples": [
    {"id": "essay-2025-03", "path": "essay-2025-03.txt", "genre": "essay",
     "origin": "human_authored", "consent": true,
     "sha256": "<output of: shasum -a 256 essay-2025-03.txt>"}
  ]
}
```

**Run:**

```bash
python3 prototypes/wi9/wi9_core.py voice --root ~/wi9-private/voice/essay --input voice.json
```

It returns `REVIEW` with per-sample and mean measurements when the samples qualify, and `HOLD` naming each problem otherwise (`VOICE_SAMPLE_SHORT`, `VOICE_SAMPLE_COUNT`, `VOICE_GENRE_MIX`, `VOICE_DIGEST_MISMATCH`, `VOICE_DUPLICATED_SAMPLE`). The measurements are a diagnostic of your style; they never prove who wrote anything. Withdrawal: delete the folder; nothing else holds a copy.

**Then the author review:** read the measurements, mark which describe you and which do not, and approve the baseline for that genre in writing. Only after that may WI9-03 move past PROTOTYPE.

## 2. The 60-case editorial benchmark (WI9-07)

The design is [`QUALITY_BENCHMARK.md`](QUALITY_BENCHMARK.md): 15 cases each for journalism and expert commentary, executive correspondence, fiction, and technical or institutional work; arms v8 and v9 on identical source material; blinded, randomized labels; the eight 1–5 criteria.

**Decide before any score is seen** (record the decision with a date, in this repository, and do not change it afterwards): the number of independent reviewers per case, what counts as an improvement (for example a median v9-minus-v8 delta above zero on evidence integrity and original thought with no criterion worse), and the zero-tolerance invariants (no invented firsthand event, no human-only venue violation, no silent consequential change).

**Provide:** the consented source material for each case, kept private like the voice samples; the reviewers, who did not build v9 and are not shown which arm is which; and their ratings in this shape:

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

## 3. Independent review (WI9-09)

An automated security and correctness review of the v9 code was run from a fresh context and its findings recorded in [`defects.md`](defects.md). That is not the review WI9-09 requires. WI9-09 needs a person who did not build v9 to read the code, the receipts and this program and record a decision. Name the reviewer; their findings are added to `defects.md` and their decision to a receipt.

## What is not waiting on the owner

Everything else in [`WAVES.yaml`](WAVES.yaml) marked open is engineering work: a `wi.py` subcommand, the v9 manifest in `plans/`, API and MCP exposure, the private vault (WI9-02) and the thought-fidelity pass (WI9-04).
