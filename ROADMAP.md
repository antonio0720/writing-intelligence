# Roadmap

Writing Intelligence is a living project. **v5.0 shipped August 2026.** Here's where it goes next.

Built by **Antonio T. Smith Jr. / Density6 LLC**

---

## The version narrative

Each version proved one thing and then made the next thing necessary.

| | Proved |
|---|---|
| **v1.0** | Prose compilation. AI-sounding writing is defeated by compiling it, not by cleaning it up. |
| **v2.0** | Narrative systems. Fiction is engineering — chapters, roles, tension and canon are architecture. |
| **v3.0** | Governed authorship. Writing can be governed without being flattened: passes, engines, schemas, benchmarks. |
| **v4.0** | Accountable authorship. What may be *claimed* about the writing is itself governed — support means a verbatim span or it is `needs_source`. |
| **v5.0** | Proof-carrying authorship. The account travels with the document and survives the absence of everything that made it. |

v4 verifies a document at a moment. v5 keeps the verification bound to what it depended on, so an edit made three weeks after a check cannot inherit the check's result — and packages the account into an artifact a stranger can verify offline, with no model and no network.

---

## v5.0 — Released (August 2026)

**The Proof-Carrying Authorship OS.** Six new system laws (G–L) above the six preserved v4 laws. All of it in one stdlib-only Python file, offline, Python 3.8+.

**Executable today:**

- [x] Content-addressed source ingestion with immutable source versions — `wi ingest`, raw bytes hashed before any normalization
- [x] Canonical serialization and domain-separated state digests — `wi-state-v5`, NFC, sorted keys, RFC 8785-shaped
- [x] A persistent `.wi/` workspace — SQLite index plus content-addressed object store, plus `wi.lock`
- [x] Claim atomization — a compound sentence becomes independently checkable atoms — `wi atomize`
- [x] Evidence anchors with byte spans and quote digests — `wi anchor`, `text_span` only
- [x] Deterministic checks — anchor integrity, verbatim quotation, numeric value, date range, entity presence, citation resolution
- [x] `span_supported` — every checkable component of a claim found co-located inside one span of one source; distinct from `supported` and from `candidate_support`
- [x] The authorship graph — `wi graph`, nodes and edges with a content-derived logical id and an immutable state digest
- [x] Staleness and the minimum repair frontier — `wi impact`, which reports what a changed source broke **and how many nodes it provably did not**, with a costed repair plan
- [x] Deterministic semantic diff — `wi diff --semantic`, classifying `may reduce → reduces` as `certainty_strengthened` and `11,800 → 12,400` as `quantity_changed`
- [x] Writing tests — `wi test`: evidence coverage with a denominator, forbidden terminology, concept drift, required sections, orphan citations
- [x] Proof-carrying release bundles in three profiles — `wi bundle` at `full` / `hash-only` / `redacted`
- [x] Offline verification — `wi verify-release`, recomputing every digest with no model and no network, rejecting a tampered artifact with `WI_RELEASE_TAMPERED`
- [x] `wi explain path:line`, `wi doctor` capability negotiation, `wi preserve` into the workspace
- [x] The whole v4 floor unchanged — `preserve` · `scan-sources` · `extract-claims` · `verify` · `gate`
- [x] Regression: `tests/v4/test_wi.sh` (3 checks) and `tests/v5/test_wi5.sh` (32 checks, each with a negative twin)
- [x] 20 doctrine documents in `references/v5/`, 15 JSON Schemas in `schemas/v5/`

**Specified in v5.0 and not executable anywhere:** a compiled Rust/WASM core; PDF, DOCX, XLSX, image, audio and video anchors; any judgment provider; proposal and decision objects as persisted records; external signing; the Workbench; the MCP server; REST v5; multi-actor authority policy; at-rest encryption; `wi migrate`. Every one is labelled at the point of description, and `wi doctor` reports the live list on any machine.

> **Note on numbering.** Earlier roadmaps reserved v5.0 for *Multimodal Writing Intelligence*. The graph had to come first: multimodal anchors without dependency-aware proof would have produced more kinds of evidence that nothing could invalidate. Multimodal work is **v5.2** and is unchanged in scope.

---

## v5.1 — The Judgment Tier (Target: Q1 2027)

The deterministic tier says outright that it cannot judge paraphrase. That is the largest remaining gap and closing it is the next priority. The whole design constraint is that adding judgment must not weaken `verified`.

### The provider ABI

- [ ] A stable provider interface — request, response, error taxonomy, timeout and refusal semantics
- [ ] Providers are named, versioned and swappable. No provider is bundled, privileged or default
- [ ] The gateway has **no write path into the graph**. A provider returns a record; the core decides what, if anything, becomes a node

### Paraphrase entailment as a typed, replaceable record

- [ ] Entailment classification for a claim supported by a source that does not share its wording
- [ ] Every judgment record carries `provider`, `model_identifier`, `prompt_policy_hash`, `input_hashes`, `output` verbatim, `calibration_basis` and `currency` — per Law L
- [ ] A judgment emits `judged`. It may never emit `verified`. There is no threshold and no provider quality that promotes one into the other
- [ ] A judgment record is dependency-bound like any other proof and goes stale under Law I

### Disagreement as a first-class outcome

- [ ] Two providers that disagree produce a **conflict**, not an average. Averaging two opinions manufactures a third opinion nobody holds
- [ ] Conflicts surface at the gate with both records and both provenance chains attached
- [ ] Conflict between two *supplied sources* surfaced at intake rather than at gate

### Calibration published honestly

- [ ] Calibration results are `measured`, and publish their **benchmark set and their N** on the same line
- [ ] No naked confidence percentage anywhere. A percentage without a denominator is authority theater
- [ ] An uncalibrated provider reports `calibration_basis: none` rather than omitting the field

Governing document: `references/v5/JUDGMENT_TIER.md`, written to bind an implementation that does not exist yet.

---

## v5.2 — Multimodal anchors (Target: Q2–Q3 2027)

Six of the seven anchor kinds are specified and none execute. They ship in this order, because the order is the order of evidentiary value per unit of decoder risk.

- [ ] **PDF page/region** — page number plus bounding box, with a **page-image digest** so the anchor survives a re-extraction and a human can see the region they are being pointed at
- [ ] **XLSX cell/range** — sheet name plus cell range, with **formula dependencies** recorded, so a figure that is computed from three other cells has three dependencies and goes stale when any of them moves
- [ ] **DOCX paragraphs** — paragraph identity that survives a reflow
- [ ] **Image regions** — bounding box or mask reference
- [ ] **Audio timecode** — start and end, with sample rate
- [ ] **Video frame intervals** — frame index or time range, optional bounding box

### The rules every adapter inherits

- [ ] **The raw-bytes rule.** The source is the bytes. A decoder's output is a *derived object* with its own digest and its own named extractor identity, and never the source itself. An extractor upgrade is a visible change
- [ ] **Sandbox.** Decoders run with no network, no filesystem write outside a scratch directory, and no ability to reach the graph. A malicious PDF is a normal Tuesday
- [ ] **Limits.** Declared ceilings on size, page count, decode time, memory and recursion depth, with the limit that tripped named in the failure
- [ ] **Quarantine before context.** Ingestion produces a quarantined object; the object is scanned; only then may any surface build a model-facing representation. Law F holds at the adapter boundary, not at a delimiter
- [ ] **An unavailable anchor never degrades into a text-span anchor built from recollection.** Law E, stated as a code path

Governing documents: `references/v5/EVIDENCE_ANCHORS.md`, `references/v5/MULTIMODAL.md`, `references/v5/SECURITY_MODEL.md`.

---

## v5.3 — Proposals and decisions as records (Target: Q4 2027)

Laws A and J are conduct today. This makes them persisted objects in the store.

- [ ] **The proposal object** — `target` node and state digest, `before` / `after` verbatim, `why` in the operator's words, `semantic_delta` from Law H, `proof_impact` naming which proofs the change invalidates and which it leaves intact
- [ ] **The decision record** — actor and actor type, `accepted` / `rejected` / `deferred` / `accepted_with_modification`, the digest of the proposal, the digest of the target state, timestamp, optional reason — hashed and stored beside the content
- [ ] A decision binds to the **target state**, not to the document. A decision that says "approved" without saying what state it approved is a signature on a blank page
- [ ] A proposal with no decision is an **open proposal**, never a silent acceptance
- [ ] **Auto-accept policy** — a project may declare which delta classes accept without a person present, and the acting party is recorded as `automated_policy`, which is a real actor with real authority that is honestly not a human
- [ ] **Delegated authority** — `authorized_editor` with explicit, recorded, scoped and expiring authority
- [ ] A `judgment_provider` may never sign a decision record, may never be the actor on an acceptance, and may never write a record typed `human`, `team_member` or `authorized_editor`
- [ ] **The decision ledger in the bundle** — a `.wiab` carries who approved what, against which state, and when, so "the author approved this" becomes a checkable statement rather than an assumption

---

## v5.4 — The Workbench (Target: 2028)

A desktop authoring surface over the same core. Six panes:

- [ ] **Source Vault** — ingested sources, versions, digests, rights basis, consent basis, quarantine findings
- [ ] **Author Canvas with a proof margin** — you write; the margin shows, per sentence, the status, the anchor and what depends on it. The margin is the product
- [ ] **Proof Inspector** — `wi explain` as a pane: every anchor, every check, every reliability type, every dependency
- [ ] **Meaning Diff** — `wi diff --semantic` between any two states, with the proof-carry-forward verdict per change
- [ ] **Impact View** — the minimum repair frontier as a picture, showing the provably-unaffected set at the same weight as the stale set
- [ ] **Release Room** — gate verdict, outstanding items with their repair routes, bundle profile choice, and the offline verification command to hand a reader

### The no-dashboard-theater rule

**Every number on every pane has a visible denominator and a stated reliability type, or it does not appear.** No blended score, no health gauge, no percentage that averages a string comparison with a model opinion, no green badge over text that changed after it was checked. A dashboard is where a system with four honest reliability types quietly grows a fifth one called "overall," and that is the failure this project exists to prevent, pointed at its own UI.

The Workbench is a surface. Law K binds it: it calls the core, it does not implement a check.

---

## v5.5 — Surfaces (Target: 2028)

- [ ] **MCP server on the same core** — the deterministic commands exposed as tools, with capability negotiation so a reduced surface states what it cannot do rather than degrading quietly
- [ ] **REST v5 as a thin adapter** — HTTP in front of the core. `services/api/` remains the v3 craft kernel; the v5 tier arrives as an adapter beside it, not as a port of it
- [ ] **OpenAPI 3.1 generated in CI** — generated from the core's own schemas, never hand-written, and CI fails if the committed document does not match the generated one
- [ ] **Webhook event format** for CI/CD writing checks
- [ ] **Browser and edge surface** via the compiled core, once v6.0 lands

### Law K, stated plainly

**No surface reimplements proof rules.** A surface may add ergonomics, caching, presentation, batching and access control. A surface may **not** implement a check, re-implement a digest, define an anchor resolution rule, or emit a proof record it did not receive from the core.

The moment two implementations of `verified` exist, one of them is wrong and nobody knows which. They will not disagree loudly. They will disagree on the fifth edge case, in the surface with fewer tests, on the document that mattered — because one normalized whitespace differently or pinned an older parser. Adapters translate. They do not decide.

---

## v5.6 — The Storyworld graph (Target: 2029)

The graph already knows how to hold a fact, bind it to a location, and invalidate it when something moves. Canon is that machinery pointed at a constructed world.

- [ ] **Persistent canon** — characters, places, timelines, objects and rules as registered concepts inside the `fictional_canon` realm
- [ ] **Character state machines** — what is true of a character at a point in the timeline, so "she does not know yet" is a queryable state rather than an act of memory
- [ ] **The canon compiler** — plants and payoffs as edges; an orphaned plant is a graph query, and a contradiction three hundred pages later is a failing test
- [ ] **Transmedia invalidation** — a canon change in the novel raises the affected scenes in the audio drama, the game cutscene and the lore bible, using the same minimum repair frontier
- [ ] **Realm discipline enforced at the renderer.** A canon check is verified against canon only, inside the fictional realm, and **must never render as externally verified fact**. The realm is not metadata a renderer may drop for space

Governing document: `references/v5/STORYWORLD_OS.md`.

---

## v6.0 — The compiled core (Target: 2029+)

`scripts/wi.py` is the canonical core and it is a single stdlib-only Python file. That is why surface parity is achievable at all today: there is exactly one thing to call. A compiled core replaces it only under conditions strict enough that nobody has to take the swap on faith.

- [ ] **Rust core with a WASM build** for browser, edge and embedded surfaces
- [ ] **Parity gate.** The compiled core and the Python core run the **same shared fixtures** and must produce byte-identical canonical output, byte-identical digests and identical verdicts. **Nothing switches until parity is proven on every fixture**, and the parity runner ships as part of the release
- [ ] Both cores run in CI for at least one full release cycle after parity, so a divergence has somewhere to be caught
- [ ] **Single-binary distribution** — one file, no runtime, no dependencies, checksum published
- [ ] **Air-gapped verifier** — a minimal build that does nothing but `verify-release`, small enough to carry into a room with no network and audit by reading
- [ ] Language bindings generated from one schema source, never hand-maintained

Until every one of those boxes is checked, any document, deck or README implying a compiled core exists is wrong and should be corrected on sight.

---

## Permanent non-goals

These are not unbuilt features. They are refusals, and they do not move. Full reasoning in [`references/v5/NON_GOALS.md`](references/v5/NON_GOALS.md).

**Carried from v4**

- **Detector evasion.** Never. A system built to produce a machine-checkable account of how a document came to exist cannot also be a system for concealing how a document came to exist.
- **Source generation.** The system will not construct a citation, ever. There is no code path in which a well-formed anchor can be produced for a source that was never ingested.
- **Truth verification.** It verifies support within supplied sources. A `.wiab` that verifies offline on a stranger's machine proves the anchors resolve and nothing drifted. It proves nothing about whether the sources are correct.
- **Absolute quality scores.** There is no universal writing number. Counts with visible denominators are legitimate; a number that stands in for the counts is not.

**New in v5**

- **No hosted-account dependency.** Everything constitutional runs local-first and offline from one file. The documents that most need this system are the ones that cannot leave the building, and a proof that expires when a vendor does is not a proof.
- **No proprietary-model dependency.** The deterministic tier is model-independent by construction. Judgment providers, when they arrive, are named and replaceable in every record.
- **No vector database as the truth layer.** Embeddings are candidate retrieval; they are never evidence. Negation, attribution swaps and date shifts barely move a vector — every failure this system exists to catch is a small distance in exactly the space a similarity search is scoring.
- **No blockchain.** Every hard problem here is semantic. A ledger timestamps a digest, which this system already produces, and any timestamping authority an organization already trusts can attest to a `.wiab` hash without the core knowing or caring.
- **No autonomous source approval.** A discovered source is `candidate`, never `approved`, until a human approves it. `automated_policy` may filter, rank, deduplicate and reject. It may not approve — an automated approver is an unbounded prompt-injection surface.

---

## How to Influence the Roadmap

1. **Star the repo** — signals demand
2. **Open an issue** — describe what you need and why
3. **Open an RFC** — propose substantive additions per [`governance/RFC_PROCESS.md`](governance/RFC_PROCESS.md)
4. **Submit a PR** — build it yourself per [`CONTRIBUTING.md`](CONTRIBUTING.md)
5. **Share results** — run it on your writing, share what worked and what it got wrong

The roadmap is driven by community need, not a corporate product schedule. What gets built next depends on what people actually use and ask for.

Changes to the meaning of `verified`, `stale`, `BLOCK`, `permitted` or `source quarantine` are not roadmap items. They are constitutional amendments and go through the RFC process with a benchmark case that fails before the change and passes after it.

---

*[github.com/antonio0720/writing-intelligence](https://github.com/antonio0720/writing-intelligence)*
