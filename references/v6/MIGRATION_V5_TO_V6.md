# Migrating v5 → v6

**Status: specified.** `wi migrate` does not exist in `scripts/wi.py` at v6.0.0. Neither does the Rust core, the parity runner or the compatibility report. Everything below describes what a migration must do and what must be true before a core swap; none of it runs. The v5 commands continue to work unchanged, which is the only reason it is safe for this document to describe a migration that has not been built.

A migration is the one operation that touches every historical record at once, and it is the one operation whose failure is least visible. A migration that drops a field produces an error somebody notices. A migration that *fills* a field produces a workspace that reads as richer than the one it came from, verifies cleanly, and asserts things nobody ever asserted.

v6 adds intervals, authority grants, proposals, disagreement records and richer semantic dimensions. A v5 workspace has none of those, and there is no honest way to derive most of them from what v5 stored. The whole of this document is the consequence of that.

Read this with [`CONSTITUTION.md`](CONSTITUTION.md) for the v6 laws that introduce the new state, [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md) for the digest rules that must survive the crossing, and [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) for the release verification that has to happen before anything moves.

**Contents:** [1 The migration law](#1-the-migration-law) · [2 What v5 has](#2-what-v5-has-and-what-it-does-not) · [3 The dry run](#3-wi-migrate---dry-run) · [4 Verify releases first](#4-verify-every-existing-release-first) · [5 The migration receipt](#5-the-migration-receipt) · [6 Your existing commands](#6-your-existing-commands) · [7 What is new](#7-what-is-new-at-v6) · [8 The dual-core window](#8-the-dual-core-window) · [9 Rolling back](#9-rolling-back) · [10 Executable and specified](#10-what-is-executable-and-what-is-specified)

---

## 1. The migration law

**Status: specified.**

> **Migration may create new state. It may never silently reinterpret old state.**

Three consequences, and each one closes a specific way migrations go wrong.

**A v5 value keeps its v5 meaning.** A `verified` result from v5 means a deterministic comparison ran under v5's rules against v5's anchors. It does not become a v6 `verified` by being copied into a v6 workspace; it becomes a v6 record *of a v5 verification*, carrying the version of the rules that produced it. If v6 tightened what `verified` requires, the migrated result is not silently upgraded to the stricter standard it never met, and it is not silently downgraded either — it is marked with the standard it did meet.

**A field v5 did not have is absent, not defaulted.** v6's `certainty` dimension has a value for every claim in a native v6 workspace. A migrated claim has no value, because nobody stated one. Writing the default — the most common, most reasonable-looking value — manufactures an assertion. This is the same rule the schema-downgrade control in [`FEDERATION.md`](FEDERATION.md) §9.2 applies at an organizational boundary, applied here at a version boundary.

**History that was not persisted is not reconstructed.** v5 did not persist proposal or decision history in the form v6 uses. A migration could infer plausible decision records from timestamps and file modification times. It must not. An inferred decision record is indistinguishable, once written, from one a person actually made, and the entire authority model of [Law O](CONSTITUTION.md) rests on being able to tell those apart.

**Why the law is stated as a prohibition rather than a goal.** Every pressure during a migration runs the other way. A workspace with `absent_from_source_version` on four dimensions per claim looks broken. Somebody will ask why the new version has *less* information than the old one. The answer is that it has exactly the same information, correctly labelled, and that the alternative is a workspace that appears complete and is partly fabricated. A goal bends under that pressure. A prohibition is something you have to argue your way past in writing.

---

## 2. What v5 has, and what it does not

**Status: specified.**

| v6 concept | v5 equivalent | Migration outcome |
|---|---|---|
| Source identity and raw bytes | `source.artifact`, `source.version` | Preserved exactly, digests unchanged |
| Claim atoms | `meaning.claim_atom` | Imported; v5 dimensions preserved, v6-only dimensions absent |
| Evidence anchors | `text_span` anchors | Preserved with locator and quote digest intact |
| Verification results | `verification.result` | Preserved with reliability basis and the rule version that produced them |
| Judgment records | `verification.judgment` | Preserved, including provider identity and the `judged` basis |
| Decisions | `authorship.decision` | Preserved where v5 persisted them |
| Waivers | `authorship.waiver` | Preserved, including scope and expiry |
| Policy state | policy profile at build | Preserved as a recorded fact |
| Releases | `.wiab` bundles | Not migrated. Verified in place — see section 4 |
| **Intervals** (Law N) | — | Absent. A v5 state has a digest and no interval over which it was believed |
| **Authority grants** (Law O) | — | Absent. v5 recorded decisions, not the grants that permitted them |
| **Proposals** (Law P) | — | Absent as objects. v5 proposed and did not persist a proposal graph |
| **Disagreement records** (Law Q) | — | Absent. v5 had no way to hold two incompatible states |
| **Branches and commits** | — | Absent. The migrated workspace has one initial commit |
| `certainty`, `causal_force`, `legal_force` | partially, informally | Absent unless v5 recorded the specific field |

**The bottom seven rows are the migration.** Everything above them is a copy with digest preservation. Everything below is state that does not exist and is not going to be invented, which means a migrated workspace is a v6 workspace with an honest hole where its history would be if v5 had kept one.

**The migrated workspace has one commit, and its parent is nothing.** It is not a reconstruction of the v5 workspace's evolution; it is a statement that this is where v6 history begins for this material. Synthesizing commits from file timestamps would produce a history a `wi log` reader would treat as a record of what happened.

### 2.1 Migration is one crossing, not a gradual adoption

A workspace is v5 or it is v6. There is no mode in which some claims carry intervals and others do not because the migration has reached them and not the rest.

**Why a gradual migration is worse than a slow one.** The v6 gate evaluates a graph, and a graph half of whose claims have `certainty` and half of which have nothing is not a graph with a known interpretation — a rule requiring `certainty` on regulated claims would apply to some claims and not to others for reasons that have nothing to do with the claims. The set it applies to would be *the set migrated so far*, which is a fact about a process rather than about the material, and no rule should ever be parameterized by that.

**The migration is still resumable**, which is a different property. A crossing interrupted partway leaves the `--to` workspace incomplete and unusable, and re-running resumes it. What it does not leave is a workspace that is usable and partial. The distinction is that an incomplete migration refuses to open; a partial one opens and answers questions wrongly.

**Scale is not a reason to gradually adopt.** The dry run in section 3 is a read of the entire v5 workspace and completes in the time a full graph walk takes. For a workspace large enough that this is a genuine constraint, the answer is a longer single crossing, not a workspace with two interpretations in it.

---

## 3. `wi migrate --dry-run`

**Status: specified.**

The dry run is the default and the only mode that runs without an explicit acknowledgement. It writes nothing.

```
wi migrate --dry-run --from ./workspace-v5 --to ./workspace-v6

PRE-FLIGHT
  v5 workspace version           5.0.1
  v5 verifier available          yes  (scripts/wi.py, 5.0.1)
  releases found                 3
  releases verified under v5     3 of 3   VALID
  refusing to proceed on any release that is not VALID   [not triggered]

PRESERVED EXACTLY  — digests unchanged, bytes unchanged
  source.artifact                   47
  source.version                    91
  raw source bytes                  91   total 214.7 MB
  text_span anchors                418
  quote digests                    418   all recompute correctly

IMPORTED  — carried into v6 objects, v5 meaning retained
  meaning.claim_atom              1,204
  verification.result               882
    of which basis = verified       611   marked produced_under: wi-rules/5
    of which basis = measured       147
    of which basis = judged         124
  verification.judgment             124   provider identity preserved
  authorship.decision                63
  authorship.waiver                   9   2 expired, retained as expired
  policy state                        1   profile: standard

ABSENT FROM SOURCE VERSION  — not inferred, not defaulted
  claim.certainty               1,204 of 1,204
  claim.causal_force            1,204 of 1,204
  claim.legal_force             1,204 of 1,204
  claim.validity_interval       1,204 of 1,204
  authority grant on decision      63 of 63
  proposal object                   0 available in source

NOT INVENTED  — v5 did not persist these; v6 will not create them
  proposal history           v5 proposed without persisting a proposal graph
  decision authority grants  v5 recorded who decided, not what permitted it
  branch and commit history  migrated workspace begins at one initial commit
  disagreement records       v5 could not hold two incompatible states

RESULT
  Would create 1,204 claim atoms with 4,816 fields marked
  absent_from_source_version. That is expected and is not data loss:
  those fields did not exist in the source workspace.

  Nothing was written. Run without --dry-run to proceed.
```

**`absent_from_source_version` is a distinct wire value, not a null.** A null is ambiguous between *nobody stated this*, *this was stated as nothing* and *this was lost*. The marked value says which, and downstream code can branch on it: a gate can require that a field be present-or-explicitly-absent rather than merely non-null, and a renderer can decline to display a dimension whose absence is a fact about the migration rather than about the claim.

**The counts are always denominated.** `1,204 of 1,204` rather than `1,204`, because a reader needs to know whether the absence is universal or partial. This is the denominator rule from [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) applied to a migration report.

**`produced_under: wi-rules/5` on every migrated verification result** is what preserves the section 1 distinction. The result says `verified`, and it says which rule set produced that word. A v6 gate that requires v6 rules can see that this result does not meet them, and report it as such rather than either trusting it or discarding it.

**A retained expired waiver is not a contradiction.** Two of the nine waivers had expired before the migration. Dropping them would remove the record that a waiver was once in force over a state, which is exactly what somebody auditing an old release needs. They migrate as expired.

### 3.1 The first v6 gate over migrated material

The report above is a statement about the crossing. This is what the crossing costs, on the first gate run afterwards, and it is the number worth looking at before deciding to migrate at all.

```
wi gate --profile regulated

  1,204 claim atoms evaluated

  PASS                                              1,041
  BLOCK                                                14
    d6.quantity.denominator_required                    9
    sec.disclosure.proximity                            5

  CANNOT EVALUATE                                     149
    rule requires claim.certainty
      field is absent_from_source_version            112
    rule requires claim.causal_force
      field is absent_from_source_version             37

  A rule that cannot be evaluated is not a rule that passed. These 149
  states carry no verdict for those rules, and a release built from them
  will say so rather than counting them as clear.

  To resolve: state the missing dimension on the affected claims. There
  is no bulk default, and one is not offered.
```

**`CANNOT EVALUATE` is a third column, not a subdivision of either neighbour.** Folding it into `PASS` reports 1,190 clear claims and is [Law C](../v5/CONSTITUTION.md). Folding it into `BLOCK` reports 163 problems and is false in the other direction — nothing is wrong with those claims; a dimension the old version did not have was not stated. The two mistakes have opposite consequences and both are avoided by refusing to pick one.

**There is no `--fill-defaults` flag and it is not an omission.** Somebody will want one, because 149 claims needing a dimension stated by hand is real work. A flag that wrote `certainty: asserted` across all of them would complete in a second and would produce 149 assertions nobody made, indistinguishable afterwards from stated ones. The work is the honest cost of a version that knows more than its predecessor did.

---

## 4. Verify every existing release first

**Status: specified.**

The pre-flight block runs before anything else and refuses on any release that is not `VALID` under the **v5** verifier.

**Why the v5 verifier and not v6.** A v5 release's attestation was produced by v5 rules over a v5 closure. The authority on whether it is intact is the implementation that made it. Verifying it with v6 answers a different question — whether v6 considers it valid — and if the answer differs, there is no way to tell whether the release drifted or the verifier changed.

**Why refusal rather than a warning.** A release that fails verification before migration has already drifted, in the v5 workspace, for a reason that exists independently of the migration. Migrating first means investigating that drift afterwards, in a workspace whose object identities have moved, with the migration itself as a suspect. The order matters more than the strictness: establish the pre-state is sound, then change it.

**Releases are not migrated.** A `.wiab` bundle is a finished, self-contained artifact whose attestation covers its own closure. Rewriting it into a v6 format would produce a bundle whose attestation no longer matched what was signed and shipped. The v5 bundles stay v5 bundles, verified by the v5 verifier, for as long as anybody needs to check them — which is the first of several reasons `scripts/wi.py` does not get deleted (section 8.4).

---

## 5. The migration receipt

**Status: specified.**

The receipt is the migration's own evidence. It is a content-addressed object, retained in the v6 workspace, and it is the only record of what the crossing did.

```json
{
  "format": "wimigration/1",
  "migration_id": "01HQ8M2K7VXN4T9RPD6WBZC03F",
  "from": {"version": "5.0.1", "core": "python", "workspace_root": "sha256:9f14ac6e0b7d5382..."},
  "to":   {"version": "6.0.0", "core": "python", "workspace_root": "sha256:41c0d7b39e582af6..."},
  "performed_at": "2026-10-02T08:41:19Z",
  "performed_by": "actor:human:antonio",

  "preflight": {
    "releases_found": 3,
    "releases_verified_under_v5": 3,
    "all_valid": true,
    "verifier": "scripts/wi.py 5.0.1"
  },

  "preserved": {
    "source_versions": 91,
    "raw_byte_digests_unchanged": 91,
    "anchors": 418,
    "quote_digests_recomputed_ok": 418
  },

  "imported": {"claim_atoms": 1204, "verification_results": 882, "decisions": 63, "waivers": 9},

  "absent_from_source_version": {
    "claim.certainty": 1204,
    "claim.causal_force": 1204,
    "claim.legal_force": 1204,
    "claim.validity_interval": 1204,
    "decision.authority_grant": 63
  },

  "not_invented": [
    "proposal_history", "decision_authority_grants",
    "branch_and_commit_history", "disagreement_records"
  ],

  "v5_verifiable_portion": {
    "description": "Source identities, raw-byte digests, anchor locators and quote digests are unchanged and remain checkable by the v5 verifier.",
    "manifest": "migration/v5-checkable.json",
    "manifest_digest": "sha256:b7e34a0f9c12d658a4e0b7f31c5d9280..."
  },

  "receipt_digest": "sha256:2f9a41c7e0b83d56194ca7e0f28b3d51..."
}
```

**`v5_verifiable_portion` is what makes the receipt more than a log.** The preserved half of the migration — source identities, raw-byte digests, anchor locators, quote digests — is exactly the material the v5 verifier already knows how to check. The manifest lists it, and the v5 verifier can be pointed at the v6 workspace to confirm that the preserved portion is genuinely unchanged. A migration that claims to have preserved digests is checkable by the implementation that computed them, using no code written for the migration.

**The receipt is retained, not printed.** A report that scrolls past in a terminal is not evidence. The receipt is an object in the graph with a digest, and it belongs in the proof closure of anything produced from migrated material — because a claim whose four semantic dimensions are `absent_from_source_version` has a property that a reader of a later release needs to be able to trace back to a cause.

---

## 6. Your existing commands

**Status: specified.**

Every v5 command continues to work with the same arguments and the same output. v6 adds; it does not rename.

| v5 command | At v6 |
|---|---|
| `preserve`, `scan-sources`, `extract-claims` | Unchanged |
| `ingest`, `atomize`, `anchor` | Unchanged |
| `verify`, `gate`, `test` | Unchanged behavior on unmigrated material. On migrated material, results referencing `absent_from_source_version` fields report that rather than failing |
| `graph`, `impact`, `diff`, `explain` | Unchanged |
| `bundle`, `verify-release` | Unchanged. v5 bundles verify as v5 bundles |
| `init`, `doctor` | `doctor` gains the core-identity output in section 8.3 |

**The one behavior change is in the third row and it is deliberate.** A v6 rule that requires `certainty` on a regulated claim, evaluated against a migrated claim with no `certainty`, has three options: fail the claim, pass the claim, or report that the rule could not be evaluated. It reports. Failing punishes material for having been created before the field existed. Passing reports a check that did not run, which is [Law C](../v5/CONSTITUTION.md).

---

## 7. What is new at v6

**Status: `wi capsule` and `wi constraints` executable in `scripts/wi.py`. Every other command in this list is specified.**

| Command | Introduces |
|---|---|
| `wi canon` | Registered concepts and canonical facts inside a realm |
| `wi branch`, `wi commit`, `wi log` | Versioned semantic state (Law M) |
| `wi propose`, `wi proposals` | Proposals as first-class objects (Law P) |
| `wi simulate` | Evaluating a change before committing it |
| `wi decide` | Recording an authority decision against an exact state |
| `wi merge`, `wi conflicts` | Semantic merge and preserved disagreement (Law Q) |
| `wi authority` | Scoped, expiring authority grants (Law O) |
| `wi obligations` | Proof obligations attached to states |
| `wi as-of` | Querying what was believed over an interval (Law N) |
| `wi constraints` | The graph constraint engine |
| `wi capsule` | Portable proof closures with selective disclosure |
| `wi why` | The explanation path behind a state or a verdict |

**None of these are populated by migration.** A migrated workspace has `wi log` with one commit, `wi proposals` empty, `wi authority` empty and `wi conflicts` empty. They fill as the workspace is used at v6. A migration that pre-populated them would be inventing exactly what section 1 forbids.

---

## 8. The dual-core window

**Status: specified.** No Rust core exists. This section states the conditions under which one would replace `scripts/wi.py`, and they are not met.

### 8.1 The seven conditions

Every one must hold before a compiled core becomes the default. They are checkable, and none of them is a judgement call.

1. **The Rust core passes every v4 and v5 fixture**, the negative fixtures included. A core that passes only the positive suite has not been shown to refuse anything.
2. **Byte-identical canonical state and byte-identical digests on the shared fixture set.** Not equivalent, not semantically the same — identical bytes. A digest computed by either core over the same input is the same string, or the parity gate has failed.
3. **Independent verification of every v5 release fixture.** The Rust core verifies each archived release and reaches the same verdict the Python core reaches, from the bundle alone.
4. **The v5 verifier can verify the preserved portions of migration evidence.** Section 5's `v5_verifiable_portion` checks out under `scripts/wi.py`, unmodified.
5. **Every intentional divergence is listed in an ADR-backed compatibility report.** Divergences are permitted; unlisted divergences are not. Each entry names what differs, why the difference is correct, and what a user relying on the old behavior should do. The template is [`../../governance/ADR_TEMPLATE.md`](../../governance/ADR_TEMPLATE.md).
6. **No silent fallback to Python inside the Rust CLI.** Section 8.2.
7. **`wi doctor` names which core produced each result.** Section 8.3.

**Both cores run in CI for at least one full release cycle after parity is proven**, so that a divergence that only appears under real use has somewhere to be caught before the Python core stops running.

**Condition 2 is the one that will be argued with.** Byte-identical output is a stronger requirement than correctness, and a reviewer will point out that two canonical serializations differing only in key order or float formatting are equally correct. They are, and that is the problem: the digest is computed over the bytes, so two correct serializations produce two digests, and every attestation, every capsule root and every lockfile becomes implementation-dependent. Semantic equivalence is not sufficient anywhere a hash is taken, which in this system is everywhere.

### 8.1.1 What the parity runner compares

Not verdicts. Verdicts agreeing is the weakest useful signal, because two implementations can reach the same `PASS` through different closures.

| Compared | Why it and not the verdict |
|---|---|
| Canonical serialization, byte for byte | The input to every digest |
| Every state digest | The identity of every object |
| The closure membership set | Two cores can pass a release while disagreeing about what the release depended on |
| The Merkle root over that closure | Catches an ordering difference the membership set alone would not |
| Refusal reason codes, not just refusal | Two cores refusing for different reasons have found different defects |
| Output of the negative fixtures | A core that passes the positive suite and mishandles a negative one has not been shown to refuse |

The runner ships with the release. A parity claim whose runner is internal is a claim nobody outside can check, in a project whose position is that a claim nobody can check is not evidence.

### 8.2 No silent fallback

**A Rust CLI that cannot perform an operation must fail, naming the operation. It must not shell out to `scripts/wi.py` and return the result as its own.**

**Why this is load-bearing.** A fallback is the reasonable engineering decision and it destroys the only thing the parity gate produces. With a fallback, a passing test suite no longer tells you the Rust core implements the operation — it tells you that *something* implemented it. The gap between what the compiled core does and what users believe it does grows silently, and it is discovered on the platform where the fallback is unavailable: the WASM build, the air-gapped verifier, the embedded surface. Those are precisely the environments a compiled core exists for.

An explicit, named delegation is different and is permitted, because it appears in output and in `doctor`. What is forbidden is the invisible one.

### 8.3 `wi doctor` names the core

```
wi doctor

  wi 6.1.0
  core            rust 6.1.0        (parity: 4,118 / 4,118 fixtures)
  python core     present           scripts/wi.py 5.0.1
  dual-core mode  active            both cores run in CI

  canonicalization  rust    byte-parity verified 2026-11-04
  digests           rust    byte-parity verified 2026-11-04
  gate              rust    byte-parity verified 2026-11-04
  verify-release    rust    byte-parity verified 2026-11-04
  capsule           rust    byte-parity verified 2026-11-04
  pdf anchors       unavailable in this build — no adapter present

  divergences from python core   2, both listed in
    governance/adr/0031-v6-compatibility.md
```

**Per-operation attribution, not a single core banner.** During the window the honest answer to *which implementation produced this* varies by operation, and a single line at the top would be a claim about the whole binary that is true of most of it. The last row is the same discipline: an operation nothing implements says so, rather than being absent from a list where absence reads as *fine*.

### 8.4 Keep `scripts/wi.py`

**`scripts/wi.py` stays in the repository after the Rust core becomes the default.**

> **Do not delete the thing that can independently tell you whether the replacement changed the past.**

Four things it does that nothing else can:

- **It verifies v5 releases as v5 releases.** Every `.wiab` produced before the swap has an attestation made by that implementation, and it remains the authority on whether one is intact.
- **It is the parity oracle.** A digest disagreement between two implementations has no resolution unless one of them is normative. The Python core computed every historical digest; where they differ, it is right by definition — a position [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) already takes for the local file against a server backend.
- **It checks the migration receipt.** Section 5, condition 4.
- **It is auditable by reading.** A single stdlib-only Python file can be read end to end by somebody who needs to satisfy themselves about what a verification means. A compiled binary cannot, and no amount of published checksum substitutes for it.

**The pressure to delete it will be real.** It will be described as dead code, as a maintenance burden, as a confusing second implementation. It is a second implementation, and that is what it is for.

---

## 9. Rolling back

**Status: specified.**

**The v5 workspace is not modified.** `wi migrate` reads from `--from` and writes to `--to`. Rolling back is deleting the v6 workspace and continuing to use the v5 one, and the v5 tooling is unchanged and still installed.

**What is lost on rollback** is anything created at v6 after the migration: commits, proposals, decisions, authority grants, conflict resolutions, capsules. That is real work and it does not migrate backwards — v5 has nowhere to put a proposal object or an interval.

**What is not lost** is any v5 release. They were never migrated (section 4), they verify under the v5 verifier, and rolling back does not touch them.

**Migrate a copy.** The dry run writes nothing and should be run first, read, and disagreed with before anything proceeds. The report in section 3 is designed to be argued with — its `NOT INVENTED` block exists so that somebody can look at four categories of missing history and decide whether the migration is worth doing at all.

---

## 10. What is executable and what is specified

| Mechanism | State at v6.0.0 |
|---|---|
| Every v5 command listed in section 6 | Executable in `scripts/wi.py`, unchanged |
| `wi constraints`, `wi capsule create \| inspect \| verify` | Executable in `scripts/wi.py` |
| `wi migrate`, `--dry-run`, the migration report | Specified. No migration command exists |
| `absent_from_source_version` as a wire value | Specified |
| The `wimigration/1` receipt and `v5_verifiable_portion` | Specified |
| Every other command in section 7 | Specified |
| The Rust core, the WASM build, the single-binary distribution | Specified. Nothing compiled exists |
| The parity runner and the seven conditions | Specified |
| The ADR-backed compatibility report | Specified. [`../../governance/ADR_TEMPLATE.md`](../../governance/ADR_TEMPLATE.md) exists; no compatibility ADR does |
| `wi doctor` core attribution | Specified. `wi doctor` is executable and does not yet report per-operation core identity |

---

## Related documents

- [`CONSTITUTION.md`](CONSTITUTION.md) — Laws M through R, the state a migration cannot create
- [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md) — the digest rules byte-parity is measured against
- [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) — the release verification that runs before migration
- [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) — the normativity of the local implementation
- [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — Laws A through L, the reliability types migrated results retain
- [`FEDERATION.md`](FEDERATION.md) — the schema-downgrade control, which is this law at an organizational boundary
- [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) — what a capsule over migrated material must disclose about its absent fields
- [`../../governance/ADR_TEMPLATE.md`](../../governance/ADR_TEMPLATE.md) — the record every intentional divergence needs
- [`../../docs/MIGRATION_v4_to_v5.md`](../../docs/MIGRATION_v4_to_v5.md) — the previous crossing

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
