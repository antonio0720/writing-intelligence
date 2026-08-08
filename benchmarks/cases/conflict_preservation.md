# Benchmark Category — Conflict Preservation

Four cases. Each pressure-tests `wi merge` against the one thing a merge engine must never do: produce a value that nobody asserted.

Class B — runtime correctness. Pass or fail, never scored. The template's `**Expected Range**` line asks for a 0–100 score and a baseline delta; those do not apply here, so each case states its result as `PASS` / `FAIL` and carries an `## Assertions` and `## Negative Twin` section instead. Everything else follows `_template.md`.

Gate: `b1_conflict_preservation`. Law Q — *semantic disagreement is preserved until resolved.*

---

## CONF-01 — Quantity conflict, both branches moved

**Input**: A base commit asserting a household count. Two branches, each correcting it to a different figure from a different source. `main` says the intake log recounted to 11,240. `audit` says the auditor's figure is 12,400. Neither is wrong about its own source.

**Task Contract**:

```yaml
mode: audit
intent: inform
audience: release reviewer
voice: n/a
genre_stack: []
high_stakes: true
arena: runtime_correctness
success_condition: "The merge preserves both figures and asserts neither."
```

**Expected Detections**: `Quantity` conflict on logical id `hh`; delta class `quantity_changed`; `required_resolution: authorized_decision`; `status: unresolved`.

**Expected Result**: `PASS`. Exit code `2`.

---

## CONF-02 — Evidence conflict, untyped payload

**Input**: The same divergence, with payloads carrying only `text` and no typed `quantities` array. The prose still contains different numbers.

**Task Contract**:

```yaml
mode: audit
intent: inform
audience: release reviewer
voice: n/a
genre_stack: []
high_stakes: true
arena: runtime_correctness
success_condition: "An untyped disagreement is still preserved, and is not silently promoted to a quantity claim."
```

**Expected Detections**: `Evidence` conflict on `hh`; delta class `evidence_changed`; both summaries preserved.

**Expected Result**: `PASS`. Exit code `2`.

**Why this case exists.** The conflict kind is derived from typed fields, not from digits in prose. Getting `Evidence` here rather than `Quantity` is correct: the engine reports what it can compare structurally and does not infer a quantity from text. The case fails if the kind is `Quantity` — that would mean the classifier read the prose and guessed.

---

## CONF-03 — Clean merge, only one side moved

**Input**: A base commit. A branch is created and only `audit` changes the node. `main` is untouched.

**Task Contract**:

```yaml
mode: audit
intent: inform
audience: release reviewer
voice: n/a
genre_stack: []
high_stakes: true
arena: runtime_correctness
success_condition: "A merge with no disagreement merges cleanly and does not manufacture a conflict."
```

**Expected Detections**: `clean: true`; zero conflicts; a non-null `merge_commit`; the human output states `only THEIRS moved from the base`.

**Expected Result**: `PASS`. Exit code `0`.

**Why this case exists.** This is the negative control for the whole category. A merge engine that reports a conflict on every merge passes CONF-01 and CONF-02 and is useless. Without CONF-03 the category cannot tell a preserving engine from a paranoid one.

It is also the case that catches a badly built harness. Creating the branch *after* `main` has already moved leaves only one side diverged, so CONF-01 written that way silently becomes CONF-03: it merges cleanly, exits 0, and every absence assertion passes over an output with no conflict in it.

---

## CONF-04 — Resolution is authorized and attributed

**Input**: The unresolved conflict from CONF-01. An actor holding `claim.accept.quantity_change` takes one side.

**Task Contract**:

```yaml
mode: certify
intent: inform
audience: release reviewer
voice: n/a
genre_stack: []
high_stakes: true
arena: runtime_correctness
success_condition: "The resolution names the grant it ran under, and the value written is one of the two that were asserted."
```

**Expected Detections**: resolution output names the actor, the grant id and the capability; `unresolved` drops to `0`; `wi constraints` no longer reports `FAIL C015`.

**Expected Result**: `PASS`. Exit code `0`.

**Why this case exists.** Preservation is only half the guarantee. The other half is that the eventual resolution is attributable — that six months later the record says which human, under which grant, chose which side. A resolution that lands with no grant reference is indistinguishable from a value the engine picked.

---

## Assertions

Run against `wi merge <branch> --json` unless stated.

### CONF-01

| # | Assertion | Kind |
|---|---|---|
| 1 | `clean == false` | field |
| 2 | `merge_commit == null` | field |
| 3 | `conflicts[0].kind == "Quantity"` | field |
| 4 | `conflicts[0].logical_id == "hh"` | field |
| 5 | `conflicts[0].classes == ["quantity_changed"]` | field |
| 6 | `conflicts[0].required_resolution == "authorized_decision"` | field |
| 7 | `conflicts[0].status == "unresolved"` | field |
| 8 | `stored_conflicts` has length 1 | field |
| 9 | output contains `11240` | presence |
| 10 | output contains `12400` | presence |
| 11 | output contains `11800` | presence |
| 12 | output does **not** contain `11820` | **absence** — mean of ours and theirs |
| 13 | output does **not** contain `12100` | **absence** — midpoint of base and theirs |
| 14 | output does **not** contain `11813` | **absence** — mean of all three |
| 15 | output does **not** contain `approximately` | **absence** |
| 16 | output does **not** contain `between` | **absence** |
| 17 | output does **not** contain `around` | **absence** |
| 18 | output does **not** contain `roughly` | **absence** |
| 19 | exit code is `2` | exit |

Assertions 12–18 are the case. Everything above them is scaffolding that confirms the conflict was real.

The forbidden values are computed from the inputs at setup time, not hardcoded. A case that hardcodes `11820` stops testing anything the moment somebody changes the fixture figures and forgets to recompute.

### CONF-02

| # | Assertion | Kind |
|---|---|---|
| 1 | `conflicts[0].kind == "Evidence"` | field |
| 2 | `conflicts[0].classes == ["evidence_changed"]` | field |
| 3 | `conflicts[0].kind != "Quantity"` | field |
| 4 | both summaries appear in the output | presence |
| 5 | no interpolated value appears | **absence** |
| 6 | exit code is `2` | exit |

### CONF-03

| # | Assertion | Kind |
|---|---|---|
| 1 | `clean == true` | field |
| 2 | `conflicts` is empty | field |
| 3 | `merge_commit` is not null | field |
| 4 | human output contains `only THEIRS moved from the base` | presence |
| 5 | exit code is `0` | exit |

### CONF-04

Run against `wi conflicts --resolve <id> --take theirs --actor <actor>` and then `wi conflicts --json`.

| # | Assertion | Kind |
|---|---|---|
| 1 | output contains `under grant` | presence |
| 2 | output names the capability `claim.accept.quantity_change` | presence |
| 3 | output names the actor | presence |
| 4 | `unresolved == 0` afterwards | field |
| 5 | `wi constraints` no longer reports `FAIL C015` | absence |
| 6 | the resolved value equals the `theirs` value exactly | field |
| 7 | exit code is `0` | exit |

Assertion 6 is not redundant with CONF-01. Preservation could hold at merge time and a resolution could still write a third value.

---

## Negative Twin

Each twin must be run and must fail. A case whose twin has not been run has not been shown to fail.

| Case | Mutation | Assertion that must go red |
|---|---|---|
| CONF-01 | Inject the mean of the two values into the merge output before assertion | 12 |
| CONF-01 | Build the divergence with the branch created after `main` moved | 1, 2, 3 — the merge goes clean and the conflict assertions fail |
| CONF-02 | Add a typed `quantities` array to both payloads | 1, 2, 3 — kind becomes `Quantity` |
| CONF-03 | Move `main` as well, so both sides diverge | 1, 2, 3, 5 |
| CONF-04 | Resolve as an actor holding no grant | the resolution is refused; 1–4 unreachable |

The second CONF-01 twin is the important one. It is the only twin that catches a harness that constructed the wrong scenario, and it is the mistake that produces a green suite proving nothing.

---

## Scoring Rubrics Applied

None. This is a runtime-correctness case and is not scored.

`references/diagnostics/scorecard.md` does not apply: there is no prose here to evaluate, and a merge output is not addressed to a reader. Applying a prose rubric would produce a number, and a number here would eventually be averaged with the Class A results, which is the thing the two-class split exists to prevent.

---

## Regression Hazards

- **A "smart" merge.** The most likely regression is somebody adding recency, source-priority or numeric-proximity heuristics to reduce conflict volume. Every one of them produces an output value from a rule rather than from an assertion. CONF-01 catches it only through assertions 12–18; the rest of the case would still pass.
- **Fixture drift.** If the figures change and the forbidden set is not recomputed, assertions 12–14 test nothing while continuing to pass. Compute them from the inputs.
- **Kind inference from prose.** A future classifier that reads digits out of `text` would make CONF-02 report `Quantity`. That is a regression even though it looks like an improvement: it means the delta classifier is guessing rather than comparing typed fields, and the guess would drive an authority requirement.
- **Silent clean merges.** Any change to branch or ref handling that makes divergence harder to construct turns CONF-01 into CONF-03 without failing anything. The twin is the only defence.
- **Resolution without attribution.** A convenience flag that resolves conflicts without an actor would pass CONF-01 through CONF-03 and break the record.
