# Writing Intelligence v6.0.0 — Benchmarks

Two classes of benchmark, measured two different ways, because they answer two different questions.

**Class A — prose quality.** Scored 0–100 against `references/diagnostics/scorecard.md`. This is the craft floor and it is unchanged in kind from v3. Prose quality is a judgement against a rubric, and pretending it is a measurement would be its own dishonesty.

**Class B — runtime correctness.** Pass or fail. Not scored, not weighted, never averaged. A merge either fabricated a number or it did not. There is no 87% of not fabricating a number.

A release passes the benchmark gate only when every Class A gate is met **and** every Class B case passes. Class B is not a tiebreaker and does not contribute to an average. One Class B failure blocks the release on its own.

## Why the split

Aggregating them would destroy the thing Class B exists to detect.

A release with a strong prose delta and one merge that split the difference between two sources would score well. The averaged number would go up. The system would have produced a value no one asserted, in a record that attests a human decided it, and the benchmark report would say the release improved.

So Class B is counted, not scored, and it is reported as a count of failures rather than a rate. This is the same discipline the constraint engine uses: `wi constraints` reports `pass`, `fail` or `not_evaluated` per constraint, emits no aggregate score, and prints `N evaluated, N not evaluated, N failed`.

## Structure

```
benchmarks/
├── README.md                        # This file
├── benchmark_manifest.yaml          # Canonical case list and gates
├── runbook.md                       # How to run both classes
└── cases/
    ├── _template.md                 # Case structure
    ├── ai_slop_rewrite.md           # Class A, 5 cases
    ├── grant_narrative.md           # Class A, 5 cases
    ├── conflict_preservation.md     # Class B, 4 cases
    └── simulation_fidelity.md       # Class B, 4 cases
```

`reports/` does not exist. It is created by the first run that writes one.

## What is authored

The manifest reserves 60 Class A case slots across 12 categories. **Ten are authored.** The other 50 are reserved placeholders, disclosed in `cases/_template.md` and carried forward here rather than quietly counted.

A benchmark suite that reports 60 cases and runs 10 is the same defect as a certification that certifies nothing. The manifest now separates `authored_cases` from `reserved_cases` so no report can present the reserved count as work done.

Class B ships 8 authored cases and reserves none.

## Class A gates — prose quality

Unchanged from v3. These are the craft floor.

| Gate | Requirement |
|---|---|
| Score improvement | The release must beat the prior baseline by **≥ 5 points on ≥ 70%** of authored cases |
| No regression | No case may drop more than **3 points** without a documented reason |
| Evidence safety | **100%** of fabricated-source traps must be flagged |
| Voice preservation | Voice drift cases identify the correct drift direction **≥ 80%** of the time |
| Genre collision | Mixed-genre tasks produce a declared `genre_stack` with `collision_resolutions` |
| Narrative audit | Story cases identify dead props, flat setting, missing payoff |
| Output packaging | Every case produces a `delivery_bundle` that validates against `schemas/delivery_bundle.schema.json` |

Percentages here are over **authored** cases. Computing them over reserved slots would make the denominator a fiction.

## Class B gates — runtime correctness

Six gates. Every one targets a mechanism that exists in `scripts/wi.py`, and each was exercised against the running tool before it was written here.

`tests/v6/test_wi6.sh` already covers most of this ground and is the better place to look first: it asserts conflict preservation by absence, digest stability and domain separation, both authority refusals, and that a tampered capsule never reports `VERDICT VERIFIED`. The benchmarks add two things the suite does not have. **B2's fidelity equality is not asserted anywhere in the suite** — it checks that a simulation *reports* a frontier, not that its predicted root is the root that lands. And no gate here duplicates a suite assertion for its own sake; where the suite already covers a property, the benchmark case exists to hold it across a release boundary rather than a commit.

### B1 — Conflict preservation

**Assertion.** No value appears in a merge output that is absent from base, ours and theirs.

**How it is checked.** Build a three-way divergence over one logical id. Run `wi merge <branch> --json`. Compute the values a splitting engine would have produced — the arithmetic mean, the midpoint, a range spanning both, the more recent value presented as the answer — and assert each is absent from the output bytes.

**Also asserted.** `clean` is `false`, `merge_commit` is `null`, and both input summaries appear in the conflict record.

**The failure this prevents.** An averaged number reads exactly like a decision. Nothing downstream can tell the difference, and the record will later attest that an authorized human chose it.

Law Q: *semantic disagreement is preserved until resolved.*

### B2 — Simulation fidelity

**Assertion.** The `candidate_root` reported by `wi simulate --json` equals the `root` reported by the `wi commit --json` that subsequently applies the same proposals.

**Also asserted.** `committed` is `false` in the simulation. `base_root` is byte-identical across two consecutive simulations of the same pending change, so the simulation did not move the branch it simulated against. `commit.prior_root` equals `simulate.base_root`.

**The failure this prevents.** A preview that does not predict the thing it previews. If the roots differ, every decision made on the strength of a simulation was made about a state that never existed, and nobody would find out until the commit.

### B3 — Impact precision

**Assertion.** On a known-damage graph, `provably_unaffected` is exact — not conservative, not approximate.

**How it is checked.** Build a graph whose damage set is known by construction: a changed node, a node that depends on it, and n independent nodes. Assert `changed_nodes`, `stale_frontier` and `hard_stale_frontier` by **set equality**, not by count, and assert `provably_unaffected == n`.

**The failure this prevents.** A report that flags everything is a report that gets switched off. The whole value of the repair frontier is that it is small and defensible; an engine that pads it to be safe has produced a number nobody will act on, and the next correction gets made without running the tool at all.

Set equality matters more than the count here. Two wrong sets can have the right size.

### B4 — Authority

**Assertion.** A transition attempted without a grant is refused, and an expired grant refuses identically in outcome while remaining distinguishable in cause.

**How it is checked.** Attempt the same `wi decide --accept` as three actors: one holding a live grant, one holding an expired grant, one holding none.

| Actor | Outcome | Code |
|---|---|---|
| Live grant | Accepted | — |
| Expired grant | Refused, exit 2 | `WI_AUTHORITY_EXPIRED` |
| No grant | Refused, exit 2 | `WI_AUTHORITY_DENIED` |

**Also asserted.** The two refusals carry different repair guidance, and neither transition is applied. Assert on the state, not only on the message: the node is unchanged in both refused cases.

**The failure this prevents.** Two failure modes, opposite directions. An expired grant that still works makes the window decorative, and a window that does nothing means revocation is the only control left. Two refusals that read identically make expiry undiagnosable, and an operator who cannot tell why they were refused re-issues blindly.

### B5 — Digest stability

**Assertion, both directions.**

Reformatting does not move the digest:

- Reordering object keys → same digest
- Reindenting → same digest
- Unicode normalization form NFD → same digest, because canonicalization normalizes to NFC

Changing a value does move it:

- One coefficient changed → different digest

**How it is checked.** `wi canon <file> --json` and compare `content_digest` and `state_digest_v6`.

**Also asserted.** Domain separation. The same canonical bytes produce different digests under different domain tags, so a digest computed for one purpose cannot be replayed as a digest for another.

**The failure this prevents.** Both halves are load-bearing and each is useless alone. A digest that moves on reformatting makes every proof brittle and trains people to ignore mismatches. A digest that does not move on a changed value is not a digest.

The second direction is the one benchmarks usually forget. A checker that only asserts stability passes on a function that returns a constant.

### B6 — Capsule verification

**Assertion.** A tampered capsule is rejected, and rejected for the right reason.

**How it is checked.** Take a capsule that verifies. Tamper it in three distinct places, one at a time, and assert the *named check* that fails.

| Tamper | Failing check |
|---|---|
| A disclosed state payload value | `state.digest` |
| A recorded `leaf_digest` | `leaf.digest` |
| The format marker | `capsule.format` |

**Also asserted.** Every tampered capsule reports `VERDICT TAMPERED` and exits 2, and no tampered capsule ever prints `VERDICT VERIFIED`. The clean capsule reports `VERDICT VERIFIED` and exits 0.

**The failure this prevents.** A verifier that rejects everything is as useless as one that accepts everything, and both pass a benchmark that only asserts "tampering is rejected". Naming the failing check is what distinguishes a verifier from a coin. Asserting on the absence of `VERDICT VERIFIED` is what catches a verifier that prints its failures and its verdict independently.

## What these gates do not cover

Stated because a gate list read as exhaustive is worse than no gate list.

- **Adversarial input.** No Class B case attempts to construct a payload designed to defeat canonicalization or the conflict classifier. These cases prove the mechanisms work on honest input.
- **Concurrency.** Nothing here exercises two writers against one workspace.
- **Scale.** The known-damage graphs are small enough to check by hand, which is the point, and says nothing about behaviour at thousands of nodes.
- **The specified-but-not-running surface.** `README.md` carries a table of what runs and what is specification only. Class B benchmarks only what runs.
- **Result recording.** `schemas/benchmark_result.schema.json` (`BenchmarkResultV3`) has a `category` enum locked to the twelve Class A categories and required fields that assume a score. It cannot represent a Class B result. Until a schema RFC lands, Class B results are recorded in the report text and are not machine-readable. This is a gap, not a design.

## Adding a case

**Class A.** Follow `cases/_template.md`. Register it in `benchmark_manifest.yaml` under `categories` and increment `authored_cases`.

**Class B.** Follow `cases/_template.md` for structure, and additionally:

- Name the exact command that produces the artifact.
- State every assertion as something a script can check: a field equality, a string presence, a string **absence**, or an exit code.
- Include at least one assertion on an absence. A merge case that only asserts what is present cannot detect a fabricated value.
- Include the negative twin: the mutation that makes the case fail. A case that cannot fail is decoration.

Register it under `runtime_cases` and increment `authored_runtime_cases`.

## Report format

```text
Writing Intelligence v6.0.0 Benchmark Report
============================================

Class A — prose quality (scored)
  Authored cases run: 10
  Reserved slots not run: 50
  Passed: 9
  Conditional pass: 1
  Failed: 0
  Mean score delta vs prior baseline: +N.N

Class B — runtime correctness (pass/fail)
  B1 conflict preservation    4 cases   0 failed
  B2 simulation fidelity      4 cases   0 failed
  B3 impact precision         --        not evaluated: no authored case yet
  B4 authority                --        not evaluated: no authored case yet
  B5 digest stability         --        not evaluated: no authored case yet
  B6 capsule verification     --        not evaluated: no authored case yet

  8 evaluated, 4 not evaluated, 0 failed.

Release decision: <PASS | BLOCKED>
```

A gate with no authored case reports `--` with the reason. It never reports as passed. An unevaluated gate blocks the release the same as a failing one, and is listed separately, because "nobody wrote the case" and "the mechanism is broken" call for different work.

The report never prints a combined figure across the two classes.

## Author

Antonio T. Smith Jr. / Density6 LLC
