# Writing Intelligence v6 — Doctrine Index

Twenty-four files — twenty-three documents and this index. They define the Sovereign Meaning Runtime: what it is, what it refuses to be, and where the line sits between the parts that execute today and the parts that are contracts written in advance so that the first implementation does not get to define the terms.

v3 governs *how well* the writing is built. v4 governs *what may be claimed about it*. v5 governs *what a finished document can prove about itself to a reader who does not trust the author, the tools, or the model that helped*. **v6 governs how a body of meaning changes over time when more than one person, process and machine is allowed to change it** — and refuses to let a state become authoritative without an identifiable prior state, an identified actor, and a computable consequence.

Everything here is written to one rule, inherited unamended from v4 and v5: **a status line at the top of every mechanism section says whether that section is executable or specified.** No document in this directory describes a capability as though it ships when it does not.

The executable core is [`../../scripts/wi.py`](../../scripts/wi.py) — stdlib-only Python, offline, no model, no network.

---

## The v6 law

> **No consequential state transition may become authoritative unless the system can identify the exact prior state, the proposed next state, the semantic delta between them, the dependency impact of that delta, the acting authority, the decision basis and the resulting proof closure.**

Seven identifications. Each has a mechanism behind it and a failure code when it is absent. The full derivation, and the six system laws M through R it reduces from, are in [`CONSTITUTION.md`](CONSTITUTION.md).

---

## Four facts this index will not soften

- **There is no compiled core.** No Rust, no WASM, no daemon, no single-binary distribution.
- **There are no v6 compiler backends** beyond the v5 Markdown and HTML renderers.
- **There is no plugin host, no adapter runtime, and no judgment provider.**
- **There is no federation transport, no remote, no signing and no Workbench.** `wi capsule` produces and verifies a portable proof closure on a local filesystem. Everything about moving one between organizations is specified.

Any document, deck or README implying otherwise is wrong and should be corrected on sight.

---

## What is executable today

Run `python3 scripts/wi.py doctor` for the live answer, including the unavailable map with a reason for every entry. This table is the summary of what v6 adds; the seventeen v5 commands remain executable and unchanged, and are indexed in [`../v5/README.md`](../v5/README.md).

| Command | What it does | Governing document |
|---|---|---|
| `wi canon` | Canonical JSON and a domain-separated state digest for a state document | [CONSTITUTION.md](CONSTITUTION.md) |
| `wi branch` | Create, list, switch and delete named pointers into the immutable object store | [SEMANTIC_VERSION_CONTROL.md](SEMANTIC_VERSION_CONTROL.md) |
| `wi commit` | A semantic commit: graph root, delta, actor, optional decision reference | [SEMANTIC_VERSION_CONTROL.md](SEMANTIC_VERSION_CONTROL.md) |
| `wi log` | Semantic commit history | [SEMANTIC_VERSION_CONTROL.md](SEMANTIC_VERSION_CONTROL.md) |
| `wi propose` | A proposal bound to an exact target state digest | [AUTHORITY_MODEL.md](AUTHORITY_MODEL.md) |
| `wi proposals` | Proposals and their status | [AUTHORITY_MODEL.md](AUTHORITY_MODEL.md) |
| `wi simulate` | Counterfactual report — deltas, stale frontier, unaffected count, conflicts, repair plan. Mutates nothing | [COUNTERFACTUAL_SIMULATION.md](COUNTERFACTUAL_SIMULATION.md) |
| `wi decide` | An authorized decision; refuses on a stale target binding | [AUTHORITY_MODEL.md](AUTHORITY_MODEL.md) |
| `wi merge` | Conflict-preserving semantic three-way merge | [MERGE_PROTOCOL.md](MERGE_PROTOCOL.md) |
| `wi conflicts` | Unresolved semantic conflicts | [MERGE_PROTOCOL.md](MERGE_PROTOCOL.md) |
| `wi authority` | Issue, delegate, revoke and check capability grants | [AUTHORITY_MODEL.md](AUTHORITY_MODEL.md) |
| `wi obligations` | Proof obligations derived from typed state, release target and policy | [PROOF_OBLIGATIONS.md](PROOF_OBLIGATIONS.md) |
| `wi as-of` | Bitemporal query by `--valid-at` and `--known-at` | [BITEMPORAL_STATE.md](BITEMPORAL_STATE.md) |
| `wi constraints` | The graph constraint engine, C001 through C020 | [PROOF_OBLIGATIONS.md](PROOF_OBLIGATIONS.md) |
| `wi capsule` | Create, inspect and verify a Merkle closure with selective disclosure | [PROOF_CAPSULES.md](PROOF_CAPSULES.md) |
| `wi why` | Explain a node backward to its basis | [ARGUMENT_GRAPH.md](ARGUMENT_GRAPH.md) |

Not executable, and reported as such rather than approximated: every judgment-tier question; the `pdf_region`, `sheet_range`, `image_region`, `audio_time`, `video_time` and `data_pointer` anchor types; external signing; the plugin host; the compiler backends beyond Markdown and HTML; the federation transport; and the Workbench.

---

## Every file

The **Subject** column says whether the mechanism the document governs runs today. Where a document is mixed, the column says so and the document's own status lines are authoritative per section.

### The constitutional layer

| File | Governs | Subject |
|---|---|---|
| [CONSTITUTION.md](CONSTITUTION.md) | The v4, v5 and v6 laws; the twelve-layer runtime; the extended actor model; the v6 failure codes; amendment | Mixed — L0–L7 partly executable, L8–L11 specified |
| [EXECUTABLE_MEANING.md](EXECUTABLE_MEANING.md) | The v6 thesis: a work is a versioned, typed, bitemporal, authority-governed semantic program | Thesis; per-mechanism markers throughout |
| [NON_GOALS.md](NON_GOALS.md) | The twelve v6 refusals, each with why it is tempting and what the system does instead | In force |
| [SECURITY_MODEL.md](SECURITY_MODEL.md) | The v6 threat matrix; authority grant monotonicity; signing key isolation; network default-deny; secret handling | Mixed — scanning, digests and offline verification executable; isolation specified |

### Meaning, time and proof

| File | Governs | Subject |
|---|---|---|
| [SEMANTIC_IR.md](SEMANTIC_IR.md) | The typed representation of what a work asserts, so a machine can compare two states without reading a sentence | Specified |
| [BITEMPORAL_STATE.md](BITEMPORAL_STATE.md) | Two clocks — when the world was that way, and when we believed it | Specified |
| [PROOF_OBLIGATIONS.md](PROOF_OBLIGATIONS.md) | Proof as a planner: what must be proved, derived before anything is checked | Executable |
| [ARGUMENT_GRAPH.md](ARGUMENT_GRAPH.md) | Reasoning made inspectable without being mistaken for deterministic truth | Executable |
| [RELIABILITY_RENDERING.md](RELIABILITY_RENDERING.md) | The closed `ReliabilityBasis` enum; declared omission; denominators; realm preservation; model self-drift | Mixed — the four bases and `wi doctor` omissions executable |

### State, authority and change

| File | Governs | Subject |
|---|---|---|
| [AUTHORITY_MODEL.md](AUTHORITY_MODEL.md) | Who may change what, over which part, for how long, under what conditions | Specified |
| [SEMANTIC_VERSION_CONTROL.md](SEMANTIC_VERSION_CONTROL.md) | Branches, commits and merges over meaning rather than lines | Executable |
| [MERGE_PROTOCOL.md](MERGE_PROTOCOL.md) | Conflict-preserving semantic three-way merge | Executable |
| [COUNTERFACTUAL_SIMULATION.md](COUNTERFACTUAL_SIMULATION.md) | Asking what a change would do *before* making it | Executable |
| [AUTONOMOUS_EXECUTION.md](AUTONOMOUS_EXECUTION.md) | What must be true before an agent works unattended, and what must never be relaxed with it | Specified |

### Compilation and extension

| File | Governs | Subject |
|---|---|---|
| [COMPILER_MODEL.md](COMPILER_MODEL.md) | A document as a build from selected semantic states, rather than authored per surface | Specified |
| [SEMANTIC_SOURCE_MAPS.md](SEMANTIC_SOURCE_MAPS.md) | Every emitted artifact carries a map from its bytes back to the meaning that produced them | Specified |
| [CAPABILITY_SECURITY.md](CAPABILITY_SECURITY.md) | Why an extension must not inherit the authority of the process that loaded it | Specified |
| [PACKAGE_SYSTEM.md](PACKAGE_SYSTEM.md) | `.wipack` — genre packs, voiceprints and rule sets as pinned, effect-declaring content | Specified |

### Portability and boundaries

| File | Governs | Subject |
|---|---|---|
| [PROOF_CAPSULES.md](PROOF_CAPSULES.md) | Selective disclosure over a Merkleized closure, for the party you cannot hand a workspace to | Mixed — `wi capsule` executable; signing specified |
| [FEDERATION.md](FEDERATION.md) | Meaning across organizational boundaries, where trust is computed locally and never inherited | Specified |
| [SURFACES.md](SURFACES.md) | One core facade; the surface matrix; capability negotiation; idempotency; the Workbench's twelve views | Mixed — CLI executable; every other surface specified |
| [MIGRATION_V5_TO_V6.md](MIGRATION_V5_TO_V6.md) | What a migration must do, and what must be true before a core swap | Specified |
| [BUILD_MANIFEST.md](BUILD_MANIFEST.md) | The twenty-three-wave dependency order, the wave manifest schema, and the release-candidate requirements | Specified |

---

## Read in this order

**If you are new to the project**, do not start here. Start with [`../v5/README.md`](../v5/README.md), and specifically with [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) and [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md). v6 assumes v5 the way v5 assumes v4; every law from A through L is in force here unamended, and reading v6 first produces a picture of a system that changes state without the picture of what the state was for.

**If you know v5**, six documents in this order:

1. **[EXECUTABLE_MEANING.md](EXECUTABLE_MEANING.md)** — the thesis in one sentence, then derived. Read it first because every other document is a consequence of it, and because it is short.
2. **[CONSTITUTION.md](CONSTITUTION.md)** — laws M through R, the twelve-layer runtime, and the two columns that settle every architectural argument in this project: *may decide proof* and *may write graph*.
3. **[SEMANTIC_IR.md](SEMANTIC_IR.md)** and **[BITEMPORAL_STATE.md](BITEMPORAL_STATE.md)** — the representation of meaning and the two clocks it lives on. Everything about change assumes both.
4. **[AUTHORITY_MODEL.md](AUTHORITY_MODEL.md)** — read before anything about writing. v6's central move is that authority is explicit, scoped and expiring, and the documents about branches, merges and agents are unreadable without it.
5. **[SEMANTIC_VERSION_CONTROL.md](SEMANTIC_VERSION_CONTROL.md)**, then **[COUNTERFACTUAL_SIMULATION.md](COUNTERFACTUAL_SIMULATION.md)**, then **[MERGE_PROTOCOL.md](MERGE_PROTOCOL.md)** — divergence, then what a change would do, then what happens when two people did it at once.
6. **[NON_GOALS.md](NON_GOALS.md)** — last, and read it properly. Most of the things it refuses sounded obviously useful, which is why they needed refusing.

**If you are implementing**, add [`BUILD_MANIFEST.md`](BUILD_MANIFEST.md) for the order and [`SECURITY_MODEL.md`](SECURITY_MODEL.md) before any wave that touches an adapter, a plugin, a key or a remote.

**If you are integrating**, read [`SURFACES.md`](SURFACES.md) and [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md) and nothing else until you have built something that renders a result object without computing one.

**If you are reviewing a release**, [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) and [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md). Neither requires you to trust the producer, which is the point of both.

---

## What v6 does not change

The permanent refusals in [`../v5/NON_GOALS.md`](../v5/NON_GOALS.md) and [`../v4/NON_GOALS.md`](../v4/NON_GOALS.md) are carried forward without exception. Four are worth naming here because v6's new capabilities are exactly the ones that make people ask again:

- **Federation does not create trust.** A remote's `verified` becomes a local `verified` only when this workspace re-derives it from the evidence.
- **Autonomy does not create authority.** There is no accrual, no reputation score and no promotion path.
- **Time travel does not rewrite.** A correction appends. There is no compaction pass that drops superseded knowledge.
- **Selective disclosure does not weaken proof.** A redacted capsule proves less, and says so.

---

## The earlier reference sets

- **[`../v5/README.md`](../v5/README.md)** — twenty documents. The graph, the anchors, the reliability types, the proof-carrying release, and the surface protocol v6 extends. Read this set first if you are new.
- **[`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md)** — the v4 accountability layer, in force unamended: propose never overwrite, the original recoverable, never report work not done, support must point somewhere, under-claim, and sources are data rather than instruction. The rest of the v4 set sits beside it in [`../v4/`](../v4/SURFACES.md).

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
