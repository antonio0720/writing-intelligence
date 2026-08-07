# Architecture

**Status: v5.0 ships the Python core; the compiled core and the surfaces below are roadmap and labelled as such.**

This is the engineering plan. It is the document a contributor reads before writing code, and its first job is to be honest about what exists, because a plan that reads like a feature list is the failure this project exists to catch, one level up.

Two statements before anything else, both repeated from [`CONSTITUTION.md`](CONSTITUTION.md) because they are the ones most likely to be lost in a summary:

- **The canonical deterministic core of v5.0 is `scripts/wi.py`.** There is no compiled core, no Rust crate, no daemon and no binary. Every `crates/` path in §4 is a target, not a directory that exists.
- **The judgment tier is not implemented.** Where this document describes what a judgment provider must record, it is describing a contract that binds a future implementation.

---

**Contents:** the diagnosis · the five planes · what ships · target layout and module contracts · the check registry · the migration path · the five milestones · the Workbench · the CI matrix · golden fixtures · the build principle.

---

## 1. The diagnosis

**Status: findings against the current tree, as of v5.0.**

v5 exists as architecture rather than as features because of five specific conditions in this repository. Each is concrete and each is checkable by reading the tree.

**Finding 1 — There are two runtime truths.** [`../../services/api/`](../../services/api/) is a Node/TypeScript implementation of the v3 craft kernel: eleven passes, scoring, voice metrics, arena repackaging, thirty-one tests, deterministic, no ML. `scripts/wi.py` is a Python implementation of the v4 accountability tier: span lock, claim ledger, injection scanning, the gate. They do not overlap today, which is why nothing is broken yet, and the service's own README says so deliberately. But the correct fix is not to port one into the other. **The correct fix is one canonical verification core embedded in every surface.** A port produces a second implementation of evidence truth in a second language, and Law K exists because two implementations of `verified` mean one of them is wrong and nobody knows which. The core becomes a library with bindings; the surfaces call it; the craft kernel stays where it is and calls it too.

**Finding 2 — The deterministic verifier cannot natively ingest the formats v5 governs.** `wi verify` compares strings, numbers, dates and citations in text. v5 governs PDFs, spreadsheets, images, audio and video. Bolting format support onto the verifier as an outer feature layer — decode to text, then run the text checks — throws away the only thing that makes non-text evidence inspectable: the region, the cell, the interval. **Multimodal must be a formal subsystem with typed anchors**, defined in [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md), where a decoder's output is a derived object with its own digest and its own extractor identity, and never the source itself.

**Finding 3 — The proof doctrine is more granular than the implementation.** The doctrine says support points at a location. The implementation verifies a sentence. A sentence asserting three things gets one status, which means an author told `needs_source` cannot tell which third of their sentence failed, and a partially supported sentence has no representation at all. **The claim atom, not the sentence, must be the canonical verification unit** — verified separately, invalidated separately, repaired separately. This is Law G, and [`SEMANTIC_IR.md`](SEMANTIC_IR.md) is its specification.

**Finding 4 — The v3 schemas are artifacts of separate passes, not a unified state model.** Eleven schemas, each correct, each the output of one pass, each assigning its own identity to the same underlying things. A claim is `c0002` in the ledger, an unnamed sentence in the architecture graph and a string in the delivery bundle. Nothing joins them, so nothing propagates. The pass boundaries were right; the identity model was missing. [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) supplies it and keeps the schemas as views.

**Finding 5 — Storyworld memory is conceptually persistent and the reference runtime is intentionally stateless.** [`../compiler/storyworld_memory.md`](../compiler/storyworld_memory.md) promises that a writer can return after six months and resume mid-chapter. The REST service holds no state between requests, by design, and that design is correct for a craft kernel. The two cannot both be true without **a first-class workspace store**, which is what `.wi/` is: a SQLite index and a content-addressed object store that lives beside the manuscript and can be committed, mailed, or opened in an air-gapped room.

---

## 2. The five planes

Every component in v5 belongs to exactly one plane. The plane is not a layer diagram; it is the question that component answers.

**Evidence — *what exists outside this document, and in exactly what state?*** Ingestion, digests, versions, segments, quarantine, anchors, extractors. This plane is the only one that touches material the author did not write, and everything it produces is either raw bytes or a derived object with a named producer.

**Meaning — *what is being asserted, independent of how it is worded?*** Claim atoms, premises, definitions, terms, constraints, promises, obligations. Realms live here. This plane is what survives a reformat, and it is the reason a change to a grant narrative can raise a question about a contract.

**Authorship — *who decided this, against what, and when?*** Snapshots, proposals, decisions, waivers, protected spans, voice constraints. This plane is the difference between a document someone approved and a document nobody objected to, and it is the first thing asked when a document is challenged.

**Expression — *how does this meaning appear, here, in this medium?*** Structure nodes, renderers, media nodes, target constraints. This plane is deliberately downstream of Meaning: a document is a rendering, and a rendering may be regenerated without any assertion changing.

**Release — *what may leave, and what does it carry with it?*** Targets, builds, artifacts, proof closures, attestations, bundles, gates. This plane answers to a reader who was never in the room, which is the entire premise of the version.

Where each plane is specified:

| Plane | Governing documents |
|---|---|
| Evidence | [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) · [`MULTIMODAL.md`](MULTIMODAL.md) · [`SECURITY_MODEL.md`](SECURITY_MODEL.md) |
| Meaning | [`SEMANTIC_IR.md`](SEMANTIC_IR.md) · [`CONCEPT_REGISTRY.md`](CONCEPT_REGISTRY.md) · [`SEMANTIC_DIFF.md`](SEMANTIC_DIFF.md) · [`STORYWORLD_OS.md`](STORYWORLD_OS.md) |
| Authorship | [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) · [`RIGHTS_AND_CONSENT.md`](RIGHTS_AND_CONSENT.md) · [`../v4/PROPOSAL_PROTOCOL.md`](../v4/PROPOSAL_PROTOCOL.md) |
| Expression | [`SEMANTIC_IR.md`](SEMANTIC_IR.md) §5 · [`SURFACES.md`](SURFACES.md) |
| Release | [`PROOF_CARRYING_RELEASE.md`](PROOF_CARRYING_RELEASE.md) · [`POLICY_AS_CODE.md`](POLICY_AS_CODE.md) · [`STALENESS.md`](STALENESS.md) |

**Why planes rather than layers.** A layer diagram implies that everything above depends on everything below and that a component may be moved up or down. Neither is true here. Meaning does not sit on top of Evidence — a claim atom exists whether or not any anchor supports it, and that independence is what makes `needs_source` representable. The planes are five different questions asked of the same graph, and a component that cannot state which question it answers is a component whose boundary has not been decided yet.

---

## 3. What ships in v5.0

**Status: this section is the honest inventory.**

| Ships | Form |
|---|---|
| The canonical deterministic core | `scripts/wi.py` — stdlib-only, offline, Python 3.8+, single file |
| The `.wi/` workspace | SQLite index plus content-addressed object store |
| The authorship graph | Nodes, edges, logical id / state digest identity, invalidation policy |
| Atomization | `wi atomize` — claim atoms with stable identity |
| Anchors | `wi anchor` — `text_span` anchors, integrity and staleness checks |
| Staleness and impact | `wi impact`, `wi graph`, `wi explain` — dependency-aware invalidation, repair frontier |
| Deterministic semantic diff | `wi diff --semantic` — the Law H axis classification |
| Writing tests | `wi test` — declarative rules over graph state, including canon rules |
| Proof-carrying bundles | `wi bundle`, `wi verify-release` — `.wiab`, verifiable offline with no model |
| Capability reporting | `wi doctor` |
| The retained v4 commands | `preserve` · `scan-sources` · `extract-claims` · `verify` · `gate` |

| Does not ship | Status |
|---|---|
| A compiled core in any language | Roadmap. Nothing in this release is written in Rust. |
| Binary format adapters — PDF, DOCX, XLSX, image, audio, video | Specified, with adapter contracts |
| A judgment provider | Specified. No judgment tier is implemented. |
| The Workbench | Roadmap |
| MCP server | Roadmap |
| REST v5 | Roadmap. [`../../services/api/`](../../services/api/) remains the v3 craft surface. |

---

## 4. The target workspace layout

**Status: roadmap. None of the directories below exist in this repository.**

```
crates/
  wi-core/        deterministic checks, canonicalization, digests, gate evaluation
  wi-ir/          the semantic IR: claim atoms, dimensions, atomization, renderers
  wi-graph/       node and edge store, closure walks, impact walks, invalidation
  wi-ingest/      adapters, sandboxing, quarantine, extractor identity
  wi-policy/      policy documents, evidence modes, gate rules, waivers
  wi-attest/      bundles, attestations, closure digests, offline verification
  wi-cli/         the native CLI, reproducing every wi.py command
  wi-bench/       benchmark harness, calibration sets, parity runner

packages/
  wi-wasm/        the core compiled for browser and edge surfaces
  wi-sdk-js/      typed client over the core, no checks of its own
  wi-schema/      generated JSON Schema and type definitions, single source
  wi-mcp/         MCP server exposing the core as tools
  wi-renderers/   target renderers: markdown, html, docx, pdf, subtitle, slide

apps/workbench/   the authoring surface
services/api/     REST, v3 craft kernel today, v5 core adapter later
adapters/         external provenance: repositories, ledgers, DAM, CMS
schemas/v3/       the eleven v3 schemas, unchanged, under an explicit namespace
schemas/v5/       generated from wi-schema, never hand-edited
policies/         shipped policy documents, content-addressed
language-packs/   per-language metric availability and tier declarations
genre-packs/      the 27 packs, unchanged
voiceprints/      profiles and the fingerprint engine
references/       doctrine, versioned by tier
agents/           the 12 specialist agents and the manifest
benchmarks/       cases, harness, published Ns
tests/
  fixtures/       golden worlds
  conformance/    surface conformance against the core
  security/       the adversarial suite
  invalidation/   staleness gold
  multimodal/     per-format anchor gold
governance/       RFC, ADR, versioning, release checklist
certification/    operator levels and rubrics
release/          notes, checklists, published bundles
```

> **The v3 and v4 documentation is not deleted during migration. Old contracts move into explicit versioned namespaces.**

**Why that rule is stated as a rule.** Every migration is tempted to delete the previous generation's documents on the grounds that they are superseded, and every one that does it discovers within a year that somebody's compliance process, CI job, contract or teaching material referenced a document that now 404s. Worse, the deletion destroys the only record of what a term used to mean, which is exactly what an RFC under [`CONSTITUTION.md`](CONSTITUTION.md) §7 requires in order to show that a widening happened. `schemas/v3/` is not an archive folder. It is the live, addressable definition of what a v3 artifact is, and a v3 artifact produced in 2026 must still validate in 2036.

### 4.1 Module contracts

Short, because the value is in the boundary rather than the signature.

```
CanonicalState
  canonical_bytes() -> bytes      # the exact serialization a digest is taken over
  state_digest()    -> Digest     # sha256 over canonical_bytes, nothing else
```

Everything hashed in this system implements exactly this. One serialization, one digest rule, no per-type variation — the reason a digest computed by a server backend and a digest computed from a local file are the same string.

```
DeterministicCheck
  id()      -> CheckId            # stable, registry-listed
  version() -> Version            # bumping this invalidates prior results
  run(subject, context) -> CheckResult
```

`version()` is not decoration. A check whose logic changed is a different check, and results produced by the old version must not silently carry forward under the new one.

```
GraphStore
  get_node(logical_id)            -> Node
  put_state(logical_id, payload)  -> StateDigest
  put_edge(edge)                  -> EdgeStateDigest
  outgoing(logical_id, relation)  -> Iterator<Edge>
  incoming(logical_id, relation)  -> Iterator<Edge>
  transaction()                   -> Transaction
```

`outgoing` and `incoming` are separate methods because closure walks and impact walks are the same cost in either direction only if both adjacency indexes exist. `transaction()` is in the contract because a partial ingest must roll back whole.

```
GatePolicy
  evaluate(scope, graph) -> Verdict        # RELEASE | HOLD | BLOCK
                          + reasons        # each bound to a state digest
                          + repairs        # concrete routes, cheapest named
```

A verdict without reasons is authority theater, and a verdict without repairs is a dead end. Both are part of the return type so neither can be omitted by an implementation in a hurry.

```
IngestAdapter
  descriptor()          -> AdapterDescriptor   # id, version, formats, capabilities
  inspect(bytes)        -> InspectionReport    # static findings, quarantine routing
  extract(bytes, limits)-> ExtractionResult    # derived objects, each digested
```

`inspect` is separate from `extract` and runs first, always. That ordering is the quarantine boundary from [`SECURITY_MODEL.md`](SECURITY_MODEL.md) expressed as a type signature.

---

## 5. The required check registry

**Status: rows marked executable run in `scripts/wi.py` today.**

These are the check ids the core must implement. The list is a contract: a surface may not invent one, and a build missing one reports it through `wi doctor` rather than passing silently.

| Check id | Verifies | Status |
|---|---|---|
| `source.digest` | A source's bytes hash to its recorded `source.version` identity | Executable |
| `source.quarantine` | Hygiene findings were produced and routed before any grounding | Executable for text |
| `anchor.integrity` | The anchor resolves, its quote digest matches, its version is current | Executable for `text_span` |
| `quote.verbatim` | A quoted span appears verbatim in the anchored source state | Executable |
| `numeric.value` | A figure in the claim matches the figure in the source | Executable |
| `numeric.unit` | The unit and magnitude agree; no silent conversion | Executable |
| `date.point` | A stated date matches the source date | Executable |
| `date.range` | A stated period matches the source period, including open bounds | Executable |
| `entity.presence` | A named entity in the claim is present in the anchored region | Executable |
| `citation.resolution` | A citation-shaped reference resolves to a supplied source | Executable |
| `claim.atomization_integrity` | Atoms reconstruct the sentence and are independently checkable | Executable |
| `term.lock` | A registered term is used under its binding definition | Executable |
| `protected_span` | No pass altered a span the author protected | Executable |
| `graph.reference_integrity` | No dangling reference, missing blob or broken supersession chain | Executable |
| `verification.freshness` | Every result in scope binds to the current state of its dependencies | Executable |
| `decision.binding` | Every decision binds to a target state that is still current | Specified |
| `waiver.binding` | Every active waiver binds to the exact state it waived | Specified |
| `release.closure` | Every state in an artifact's proof closure is current and uninvalidated | Executable |
| `release.artifact_digest` | An artifact's bytes match the digest its attestation names | Executable |

---

## 6. The migration path, v4 → v5

**Status: roadmap. Phases 1–8 are the ones v5.0 executes against `scripts/wi.py`.**

1. **Freeze the constitutional layer.** Laws, realms, reliability types, actor model, protocol terms — settled before any code moves.
2. **Define identities and schemas.** `logical_id` / `state_digest`, node and edge families, canonicalization rules.
3. **Core parity with v4.** Every v4 deterministic check reproduced in the new core, same inputs, same outputs.
4. **Native CLI.** Every command reachable without a model, offline, with stable exit codes.
5. **Atomization.** The claim atom becomes the verification unit; the sentence becomes a rendering of atoms.
6. **Persistent graph.** `.wi/` workspace, object store, transactions, adjacency indexes.
7. **Source versioning and stale propagation.** Versions, anchors, invalidation policy, the repair frontier.
8. **Judgment plugin.** The provider contract, record fields, and the rule that a judgment never emits `verified`.
9. **API migration.** REST becomes an adapter over the core; it stops owning any check.
10. **MCP.** The core exposed as tools, with the same conformance suite as every other surface.
11. **Multimodal ingest contracts.** Adapters, sandboxes, typed anchors, derived-object digests.
12. **Workbench alpha.** Source Vault, Author Canvas, Proof Inspector against a real workspace.
13. **Semantic diff.** The Law H axes, deterministic, with gold cases.
14. **Cross-artifact contracts.** The same obligation asserted in three deliverables as one identity.
15. **Storyworld persistence.** Canon nodes, character state over time, canon writing tests.
16. **Proof-carrying releases.** Bundles, closures, attestations, offline verification.
17. **External provenance adapters.** Repositories, ledgers, DAM and CMS systems as sources with versions.

> **Parity rule: the new core must reproduce every existing deterministic check before adding new behavior, and both cores run on the same fixtures until parity is demonstrated.**

**Why parity comes before features.** A rewrite that adds capability while replacing an implementation has two variables and no way to attribute a difference to either. When the new core disagrees with the old one about a fixture, the only useful question is *which is right*, and that question is answerable only if nothing else changed. Running both against one fixture set for as long as it takes is slower, and it is the only version of this migration in which a silent behavior change is detectable at all. A verification system that quietly starts verifying differently has broken its central promise while every test stays green.

Three properties of the ordering are worth naming, because each of them is the kind of thing a schedule erodes first.

**Phases 1 and 2 come before any code.** Identity, canonicalization and the protocol terms are the things that cannot be changed later without invalidating every artifact already produced. Everything after them is replaceable; they are not, which is why they are frozen at the top of the list and amended only under [`../../governance/RFC_PROCESS.md`](../../governance/RFC_PROCESS.md).

**Phase 8 sits before phase 9, not after it.** The judgment provider contract is defined while the only consumer is a local CLI, deliberately. A provider interface first exercised across a network surface acquires network assumptions — retries, partial results, timeouts treated as absences — and those assumptions leak into the record format, where they become permanent. The record must be defined by what a judgment *is*, not by how it was delivered.

**Phase 11 comes after phase 7, never before it.** Multimodal ingest is the most requested capability in this version and the most dangerous to land early. Adapters built before source versioning and stale propagation exist will bind proofs to decoder output rather than to source bytes, because there is nothing else to bind to yet, and the raw-bytes rule in [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) §4 becomes unimplementable after the fact.

---

## 7. The five engineering milestones

**Status: roadmap. M1 is the gate on everything after it.**

A milestone without a demo is a wish. Each of these is defined by something a skeptic can watch.

**M1 — Proof Core Parity.**
*Exit demo:* the v4 hostile fixture in [`../../tests/v4/`](../../tests/v4/) runs against the new core and produces an equivalent `RELEASE` / `HOLD` / `BLOCK` verdict, byte-identical canonical JSON outputs, and stable state digests across runs and machines — offline, with no model involved at any point.

**M2 — Real Staleness.**
*Exit demo:* ingest a source set, verify, build an artifact. Alter one number in one source. Re-ingest. The claim that rested on it goes stale, the release goes `HOLD`, and every unrelated claim in the document stays green. The last clause is the demo. Anything can turn a document red.

**M3 — Multimodal Proof.**
*Exit demo:* click a sentence and see the exact PDF region or the exact spreadsheet cells behind it. Edit the source. The sentence goes stale. **No model is required to demonstrate the chain** — the whole path from bytes to region to anchor to claim to verdict is deterministic, and the demo proves it by running with no inference available.

**M4 — Meaning-Aware Authorship.**
*Exit demo:* change `may` to `will` in a sentence. The system reports `certainty` strengthened, marks the proof stale, and requires human approval. Not a diff showing three changed characters — a classification, a consequence and a decision.

**M5 — Proof-Carrying Release.**
*Exit demo:* take a `.wiab` bundle to a different machine that has never seen the workspace, with no model and no network, and verify it. This is the version's thesis reduced to a single command that either exits zero or does not.

---

## 8. The Workbench

**Status: roadmap. `apps/workbench/` does not exist.**

| Surface | Answers |
|---|---|
| **Source Vault** | What is supplied, in what version, with what hygiene findings and what rights state |
| **Author Canvas** | The draft, with a per-sentence proof margin |
| **Proof Inspector** | For one selection: every anchor, check, result, decision and waiver behind it |
| **X-Ray mode** | The whole document coloured by proof state, with membership on every band |
| **Meaning Diff** | Two states compared on the Law H axes, not on characters |
| **Impact View** | What a proposed change breaks, and the minimum repair frontier |
| **Release Room** | Targets, gates, closures, bundle profiles, and the verdict with its reasons |

The proof margin carries six states, and they are not interchangeable: **verified · partially supported · judged · needs source · conflict · stale**. `partially supported` exists because a sentence is several atoms and some of them can pass. `judged` is visually distinct from `verified` at every zoom level, because the one thing a margin must never do is let a model's opinion adopt the appearance of a string comparison.

> **No dashboard theater.** Every number needs a denominator and clickable membership.

"Evidence coverage 98%" is not a permitted rendering. The permitted rendering is **1,784 of 1,820 required claim atoms**, and the 36 must be openable — one click, a list, each row a claim the author can go and fix. A percentage with no denominator is a number that cannot be acted on, cannot be audited and cannot be wrong in any detectable way, which is precisely why it is the number every dashboard reaches for. The rule is enforced in the component layer: a metric component that cannot supply a membership query does not render.

**The state principle: the UI is not authoritative.** It renders graph state and it sends commands. It does not compute a verdict, does not decide whether a proof is current, and does not apply a proposal. The core decides whether a decision is valid against the current target digest — and that is what stops a stale browser tab, left open across a lunch break, from applying an approval to text that has moved underneath it. The tab's proposal targets a state digest that no longer exists, the core answers `WI_PROPOSAL_STALE`, and the author is shown what changed. A UI that held authority would have applied it.

---

## 9. The CI matrix

**Status: roadmap for the v5 jobs; the v4 jobs run today in [`../../.github/workflows/ci.yml`](../../.github/workflows/ci.yml).**

- `core-linux` · `core-macos` · `core-windows` — the deterministic core, identical outputs on all three
- `schema-generate` — schemas regenerate from source and match what is committed
- `schema-conformance` — every shipped artifact validates against its schema
- `v4-parity` — old and new cores on the same fixtures, differences fail the build
- `invalidation-gold` — staleness propagation against expected invalidation sets
- `atomization-gold` — atom sets against expected atoms, including over-split detection
- `semantic-diff-gold` — Law H classifications against expected axes
- `multimodal-pdf` · `multimodal-xlsx` · `multimodal-image` · `multimodal-audio` · `multimodal-video` — per-format anchor resolution
- `security-ingest` — sandbox limits, archive and decompression controls, parser kill
- `security-injection` — the adversarial fixtures, each proving it can fail
- `api-contract` — REST responses against the published contract
- `mcp-conformance` — MCP tools against the surface conformance suite
- `workbench-typecheck` · `workbench-e2e` — types and the demo paths from §7
- `bundle-reproducibility` — the same graph state builds a byte-identical bundle twice
- `wiab-offline-verify` — verification on a runner with no network and no model
- `release-version-consistency` — version strings agree across every file that carries one
- `docs-links` — `scripts/check-links.py`, every relative link resolves

---

## 10. Golden fixtures

**Status: roadmap. `tests/fixtures/worlds/` does not exist; [`../../tests/v4/`](../../tests/v4/) is its ancestor.**

A directory of tiny, fully known projects — small enough to read end to end, complete enough to exercise the whole chain.

| World | Exercises |
|---|---|
| `grant-small` | Strict mode, numeric claims, citation resolution, the hostile-fixture lineage |
| `policy-book-small` | Definitions, term locks, obligations, cross-section dependencies |
| `research-report-small` | Tables, figures, dimensional claims, derived numbers |
| `fiction-series-small` | Canon states, character knowledge, plants and payoffs, a retcon |
| `multimodal-small` | PDF regions, image regions, audio intervals, the `illustrates` / `supports` split |
| `spreadsheet-small` | Formula dependency, display vs. raw value, an unresolvable external link |
| `adversarial-source-small` | Injection, hidden text, bidi, poisoned metadata, a conflicting version |

Every world ships: **raw sources · expected source digests · expected anchors · expected claim atoms · expected graph · expected conflicts · expected invalidation sets · expected release verdict.**

**Why fixtures are the priority they are.** This project expects fast, automated contribution — that is the environment it was built in and the environment it will be extended in. Fast contribution is very good at producing changes that pass every test and quietly alter a behavior no test named. Prose review does not catch it; the diff looks reasonable and the reasoning is plausible. A fixture world catches it, because the expected invalidation set for `fiction-series-small` is a specific list of node ids, and a change that alters propagation changes that list whether or not anybody understood why. Golden worlds are the strongest available defense against regressions introduced by contribution that is faster than review.

---

## 11. The build principle

When choosing between two v5 features, prefer the one that makes this question easier to answer:

> **Can a skeptical third party inspect why this artifact is in its present state, without trusting the system that helped produce it?**

If yes, the feature belongs near the center of the architecture and deserves core placement, a check id, a fixture and a CI job. If it only makes generation more convenient, it is secondary — legitimate, worth building, and correctly placed at the edge where it can be replaced without disturbing anything that carries a proof.

The test is not a preference for austerity. It is the only ordering rule that survives contact with a roadmap, because convenience features always argue better in the moment: they demo well, they are asked for, and their cost is invisible until the day someone asks a question the system cannot answer. Inspectability compounds. Convenience does not.

---

## 12. What is executable and what is roadmap

| Mechanism | Status |
|---|---|
| `scripts/wi.py` as the canonical deterministic core | Executable |
| `.wi/` workspace, graph identity, atomization, anchors, staleness, semantic diff, writing tests, bundles, offline release verification | Executable in `scripts/wi.py` |
| The check registry rows marked executable in §5 | Executable in `scripts/wi.py` |
| `docs-links` and the v4 adversarial CI jobs | Executable |
| `crates/`, `packages/`, `apps/workbench/`, `adapters/`, `tests/fixtures/worlds/` | Roadmap. None of these directories exist. |
| A compiled core, WASM build, SDK, MCP server, REST v5 | Roadmap |
| Binary format adapters and the judgment provider | Specified, with contracts |
| Milestones M1–M5 | Roadmap, each defined by its exit demo |

---

## Related documents

- [`CONSTITUTION.md`](CONSTITUTION.md) — the laws this architecture implements
- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — node and edge families, identity, the proof closure, storage
- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — the claim atom and the renderer contract
- [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) — anchor types and the adapter contracts
- [`CANONICAL_HASHING.md`](CANONICAL_HASHING.md) — canonicalization, digests, the error taxonomy
- [`WORKSPACE.md`](WORKSPACE.md) — the `.wi/` store phase 6 delivers
- [`STALENESS.md`](STALENESS.md) — the invalidation engine phase 7 delivers
- [`JUDGMENT_TIER.md`](JUDGMENT_TIER.md) — the provider contract phase 8 defines
- [`POLICY_AS_CODE.md`](POLICY_AS_CODE.md) — the policy documents `GatePolicy` evaluates
- [`PROOF_CARRYING_RELEASE.md`](PROOF_CARRYING_RELEASE.md) — bundles, closures and attestations
- [`SECURITY_MODEL.md`](SECURITY_MODEL.md) — the ingestion sandbox and the adversarial suite
- [`STORYWORLD_OS.md`](STORYWORLD_OS.md) — storyworld persistence, phase 15
- [`RIGHTS_AND_CONSENT.md`](RIGHTS_AND_CONSENT.md) — rights state as a gate condition
- [`SURFACES.md`](SURFACES.md) — Law K conformance per surface
- [`../compiler/storyworld_memory.md`](../compiler/storyworld_memory.md) — the persistence promise finding 5 names
- [`../../services/api/README.md`](../../services/api/README.md) — the v3 craft runtime
- [`../../governance/VERSIONING.md`](../../governance/VERSIONING.md) and [`../../governance/RFC_PROCESS.md`](../../governance/RFC_PROCESS.md) — versioning and amendment
- [`../../ROADMAP.md`](../../ROADMAP.md) and [`../../README.md`](../../README.md) — the roadmap and the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
