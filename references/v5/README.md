# Writing Intelligence v5 — Doctrine Index

Twenty documents. They define what v5 is, what it refuses to be, and where the line sits between the parts that execute today and the parts that are contracts written in advance so the first implementation does not get to define the terms.

Everything here is written to one rule: **a status line at the top of every section says whether that section is executable or specified.** No document in this directory describes a capability as though it ships when it does not.

The executable core is [`../../scripts/wi.py`](../../scripts/wi.py) — stdlib-only Python, offline, no model, no network. The machine-readable state schemas derived from it are in [`../../schemas/v5/`](../../schemas/v5/README.md).

---

## What is executable today

Run `python3 scripts/wi.py doctor` for the live answer, including the `unavailable` map with a reason for every entry. This table is the summary.

| Command | What it does | Governing document |
|---|---|---|
| `wi init` | Create a `.wi/` workspace: SQLite index, content-addressed object store, project file | [WORKSPACE.md](WORKSPACE.md) |
| `wi preserve` | Snapshot a file before editing, so the original is always recoverable | [CONSTITUTION.md](CONSTITUTION.md) — Law B |
| `wi ingest` | Content-address sources; hash raw bytes; record an immutable version per byte state | [CANONICAL_HASHING.md](CANONICAL_HASHING.md) |
| `wi scan-sources` | Flag prompt-injection indicators and hidden text in supplied sources | [SECURITY_MODEL.md](SECURITY_MODEL.md) |
| `wi atomize` | Split sentences into independently checkable claim atoms with a structured proposition | [SEMANTIC_IR.md](SEMANTIC_IR.md) |
| `wi anchor` | Bind atoms to `text_span` evidence anchors and run the deterministic check set | [EVIDENCE_ANCHORS.md](EVIDENCE_ANCHORS.md) |
| `wi graph` | Show the authorship graph — nodes, edges, current states | [AUTHORSHIP_GRAPH.md](AUTHORSHIP_GRAPH.md) |
| `wi impact` | Compute the exact stale set and the exact provably-unaffected set for a changed source | [STALENESS.md](STALENESS.md) |
| `wi diff --semantic` | Classify what a rewrite did to meaning, and which proofs it breaks | [SEMANTIC_DIFF.md](SEMANTIC_DIFF.md) |
| `wi test` | Run writing tests and concept contracts | [CONCEPT_REGISTRY.md](CONCEPT_REGISTRY.md) |
| `wi gate` | Emit `RELEASE` / `HOLD` / `BLOCK` with repair routes | [POLICY_AS_CODE.md](POLICY_AS_CODE.md) |
| `wi explain` | Answer "why is this sentence here" for a `path:line` | [SURFACES.md](SURFACES.md) |
| `wi bundle` | Build a `.wiab` proof-carrying release at profile `full` or `hash-only` | [PROOF_CARRYING_RELEASE.md](PROOF_CARRYING_RELEASE.md) |
| `wi verify-release` | Verify a `.wiab` offline, with no model and no trust in the producer | [PROOF_CARRYING_RELEASE.md](PROOF_CARRYING_RELEASE.md) |
| `wi doctor` | Report what this surface can and cannot do, and why | [RELIABILITY_TYPES.md](RELIABILITY_TYPES.md) |

Not executable in v5.0, and reported as such rather than approximated: paraphrase entailment and every other judgment-tier question (no provider ships); the `pdf_region`, `sheet_range`, `image_region`, `audio_time`, `video_time` and `data_pointer` anchor types; external signing.

---

## Constitution

The laws, the vocabulary and the boundaries. Read these first — every other document assumes them.

**[CONSTITUTION.md](CONSTITUTION.md)** — The governing laws: propose never overwrite, the original is recoverable, the four reliability types, the actor model, the six epistemic realms, and the five protocol words whose meaning may only change by RFC. Read it before writing any code or doctrine that touches this system, and re-read section 7 before anyone proposes widening what `verified` covers.

**[NON_GOALS.md](NON_GOALS.md)** — What v5 deliberately does not do and will not be extended to do. Read it when a feature request sounds obviously useful, because most of the things listed here sounded obviously useful too.

**[RELIABILITY_TYPES.md](RELIABILITY_TYPES.md)** — The operational manual for `verified`, `measured`, `judged` and `human-declared`, with right and wrong renderings of each. Read it before writing any output line that reports a result to a human.

---

## Graph and meaning

How the system represents what a document asserts, what supports it, and how any of it is identified.

**[AUTHORSHIP_GRAPH.md](AUTHORSHIP_GRAPH.md)** — The central architecture: the document is a rendering and the graph is the system. Defines every node family, every edge family, the identity model and the proof closure. Read it before anything else in this directory except the constitution; the anchors, the IR and the hashing rules all assume the identity model defined here.

**[SEMANTIC_IR.md](SEMANTIC_IR.md)** — The structured representation of a claim: quantity, unit, temporal scope, modality, negation, attribution, entities, causality, realm. Read it when you need to know why a rewrite counted as a semantic change, or why two differently worded sentences are the same claim.

**[EVIDENCE_ANCHORS.md](EVIDENCE_ANCHORS.md)** — The seven anchor types, their adapter contracts, the raw-bytes rule, and why retrieval is not proof. Read it before implementing any adapter, and before assuming that locating a passage is the same as proving a claim.

**[CANONICAL_HASHING.md](CANONICAL_HASHING.md)** — Canonical JSON, the two digests, domain separation, hash migration, and the full error taxonomy with a repair route on every code. Read it before you write anything that computes or compares a digest.

**[CONCEPT_REGISTRY.md](CONCEPT_REGISTRY.md)** — Concepts as first-class objects, allowed and forbidden aliases, document contracts, writing tests and epistemic CI. Read it when the same number or term appears in more than one artifact and you need it to mean one thing.

---

## Change intelligence

What happens when something moves — a draft, a source, a policy, a definition.

**[SEMANTIC_DIFF.md](SEMANTIC_DIFF.md)** — The delta classes, what each one does to existing proof, the deterministic/judged boundary, and the auto-accept policy. Read it before changing how a rewrite is classified, and whenever a diff looks cosmetic but the gate disagrees.

**[STALENESS.md](STALENESS.md)** — Invalidation, propagation policy per edge, the minimum repair frontier, and the rule that an anchor outside every changed byte range is provably unaffected. Read it when an edit produces more red than you expected, or less.

**[JUDGMENT_TIER.md](JUDGMENT_TIER.md)** — The provider contract, the judgment record format, the ban on naked confidence percentages, and the gateway that has no write path into the graph. Read it before integrating any inference service; the contract is written to bind implementations that do not exist yet.

---

## Release and policy

Turning a verified workspace into something a stranger can check.

**[PROOF_CARRYING_RELEASE.md](PROOF_CARRYING_RELEASE.md)** — The `.wiab` bundle layout, the manifest, the ten verification steps, the three privacy profiles and the reproducibility rules. Read it before shipping anything to a reader who has no reason to trust you.

**[POLICY_AS_CODE.md](POLICY_AS_CODE.md)** — The policy file, the five evidence modes as presets, automatic escalation, authority policy for teams, waivers and offline mode. Read it when deciding how strict a project should be, and before changing a `block_on` condition into a `hold_on` one.

**[WORKSPACE.md](WORKSPACE.md)** — The `.wi/` directory: index, object store, snapshots, confidentiality labels, encryption posture and multi-machine behavior. Read it before touching persistence or export.

---

## World and safety

Constructed worlds, non-text sources, the people in them, and the adversaries.

**[STORYWORLD_OS.md](STORYWORLD_OS.md)** — Canon as governed truth inside a declared realm: characters, timelines, plants and payoffs, continuity checking, and why a canon check must never render as an external fact check. Read it for fiction, memoir, and any narrative that mixes documented and dramatized material.

**[MULTIMODAL.md](MULTIMODAL.md)** — Media nodes, renderings across formats, and the rule that an image which illustrates a claim contributes nothing to its proof. Read it before wiring a deck, a video or a chart into the graph.

**[RIGHTS_AND_CONSENT.md](RIGHTS_AND_CONSENT.md)** — Rights basis, scope and expiry; identifiable persons and consent basis; deletion as a recorded event; what a bundle profile may lawfully carry. Read it before ingesting anything you did not create, and before building a `full` bundle.

**[SECURITY_MODEL.md](SECURITY_MODEL.md)** — The trust boundary, source quarantine, prompt-injection defense, ingestion limits, and what may cross the network. Read it before accepting a source from anyone, which is every time.

---

## Engineering

How it is built and where it runs.

**[ARCHITECTURE.md](ARCHITECTURE.md)** — The component map, the deterministic core, the adapter boundaries, and how the pieces are allowed to depend on one another. Read it before adding a component or moving a responsibility between two.

**[SURFACES.md](SURFACES.md)** — CLI, library, MCP and chat surfaces; capability negotiation; what a reduced surface must say when it cannot do something. Read it before exposing v5 anywhere new, because the honest-degradation rules are the point.

---

## Reading orders

**New to v5:** [CONSTITUTION.md](CONSTITUTION.md) → [AUTHORSHIP_GRAPH.md](AUTHORSHIP_GRAPH.md) → [EVIDENCE_ANCHORS.md](EVIDENCE_ANCHORS.md) → [PROOF_CARRYING_RELEASE.md](PROOF_CARRYING_RELEASE.md).

**Implementing an adapter:** [EVIDENCE_ANCHORS.md](EVIDENCE_ANCHORS.md) → [CANONICAL_HASHING.md](CANONICAL_HASHING.md) → [SECURITY_MODEL.md](SECURITY_MODEL.md) → [RIGHTS_AND_CONSENT.md](RIGHTS_AND_CONSENT.md).

**Setting a project's standard:** [POLICY_AS_CODE.md](POLICY_AS_CODE.md) → [CONCEPT_REGISTRY.md](CONCEPT_REGISTRY.md) → [RELIABILITY_TYPES.md](RELIABILITY_TYPES.md).

**Debugging a verdict you disagree with:** [SEMANTIC_DIFF.md](SEMANTIC_DIFF.md) → [STALENESS.md](STALENESS.md) → [SEMANTIC_IR.md](SEMANTIC_IR.md) → [NON_GOALS.md](NON_GOALS.md).

**Fiction and mixed-realm narrative:** [STORYWORLD_OS.md](STORYWORLD_OS.md) → [SEMANTIC_IR.md](SEMANTIC_IR.md) section 6 → [CONSTITUTION.md](CONSTITUTION.md) section 6.

## Author

Antonio T. Smith Jr. / Density6 LLC
