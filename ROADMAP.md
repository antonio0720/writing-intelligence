# Roadmap

Writing Intelligence is a living project. **v6.0 shipped August 2026.** Here's where it goes next.

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
| **v6.0** | Executable meaning. A body of meaning can be changed by several people across time, under scoped authority, without anyone losing track of what is still true — and without the system inventing an answer when they disagree. |

v5 answers *is this supported?* v6 answers *what changed, what did that break, who was allowed to do it, and what would it cost to accept?* The second set of questions is not a bigger version of the first. It requires the system to hold state across time and to have an opinion about who may move it, and neither is a feature that can be bolted onto a verifier.

---

## Shipped in 6.0.0 — the first tier of the runtime

Sixteen new commands beside the seventeen from v4 and v5, for thirty-three in total. All of it in one stdlib-only Python file, offline, Python 3.8+, no model, no network.

**Canonicalization**

- [x] `wi canon` — canonical JSON under `wi-json-v1` and a domain-separated state digest, emitted **beside** the v5 digest rather than in place of it, so nothing computed under v5 is silently reassigned an identity

**Semantic version control**

- [x] `wi branch` — create, list, switch and delete named movable pointers into the immutable object store
- [x] `wi propose` — a change bound to an exact target state digest. Nothing moves, and the command says so on every run
- [x] `wi proposals` — open, accepted, rejected, deferred, superseded, applied
- [x] `wi decide` — an authorized decision bound to the state the actor actually reviewed; a target that has moved is refused with `WI_DECISION_STALE` rather than re-attached
- [x] `wi commit` — every accepted proposal applies as one transaction, recording prior root, next root, actor and decisions
- [x] `wi log` — semantic commit history

**Counterfactual simulation**

- [x] `wi simulate` — deltas, required authority and whether the actor holds it, the stale frontier, the conflicts a change would cause, a costed repair plan, and the **provably unaffected count reported with the same prominence as the breakage**. It writes nothing and says so

**Conflict-preserving merge**

- [x] `wi merge` — a semantic three-way merge that preserves a typed conflict instead of averaging it. Exits 2, does not move the root, shows both values verbatim
- [x] `wi conflicts` — unresolved conflicts, and resolution under a named grant with a stated reason

**Authority**

- [x] `wi authority` — issue, delegate, revoke and check capability grants over subject, capability, scope and window. Delegation is monotone: a child may narrow and may never widen, and an attempt exits with `WI_GRANT_SCOPE_EXCEEDED`. Absence of a grant is a refusal, never a default-allow

**Proof planning**

- [x] `wi obligations` — what must be proved before this ships, **derived from typed state, release target and policy** rather than read off a hard-coded checklist

**Bitemporal query**

- [x] `wi as-of` — `--valid-at` and `--known-at` queried independently, so *what did we believe in March about what was true in 2019* is a query rather than an act of memory

**The graph constraint engine**

- [x] `wi constraints` — C001 through C020, where a constraint that could not run says so and says why. Three outcomes, no fourth status, and no aggregate score

**Merkle closure and selective disclosure**

- [x] `wi capsule` — create, inspect and verify a `.wic` closure with per-leaf disclosure across four profiles. A redacted leaf proves membership and nothing about its content, and the artifact declares that itself

**Backward explanation**

- [x] `wi why` — a node backward to its basis, its two time intervals, the commit that introduced it, the actor and the grant that permitted it

**And the substrate under all of it**

- [x] Six new system laws — M through R — in `references/v6/CONSTITUTION.md`
- [x] 24 doctrine documents in `references/v6/`, every mechanism section marked *executable* or *specified*
- [x] 20 JSON Schemas in `schemas/v6/`
- [x] `tests/v6/test_wi6.sh` — 70 assertions, every one with a negative twin
- [x] The v4 floor and the whole v5 graph, unchanged: every earlier fixture still verifies

The v5.0 tier — content-addressed ingestion, claim atoms, evidence anchors, the authorship graph, staleness and the minimum repair frontier, semantic diff, writing tests, `.wiab` bundles and offline verification — is unchanged and in force. Its detail lives in [`references/v5/README.md`](references/v5/README.md).

---

## v6.1 → v6.3 — judgment, evidence, and compilation (Target: 2027)

The deterministic tier says outright that it cannot judge paraphrase, that six of its seven anchor kinds do not execute, and that meaning does not compile to anything but Markdown and HTML. Those are the three largest remaining gaps and they close in this order, because the order is the order of evidentiary value per unit of risk.

### v6.1 — The judgment tier

The whole design constraint is that adding judgment must not weaken `verified`.

- [ ] A stable provider ABI — request, response, error taxonomy, timeout and refusal semantics. Providers are named, versioned and swappable; **no provider is bundled, privileged or default**
- [ ] **The gateway has no write path into the graph.** A provider returns a record; the core decides what, if anything, becomes a node
- [ ] Entailment classification for a claim supported by a source that does not share its wording
- [ ] Every judgment record carries `provider`, `model_identifier`, `prompt_policy_hash`, `input_hashes`, `output` verbatim, `calibration_basis` and `currency` — per Law L
- [ ] A judgment emits `judged`. It may never emit `verified`. There is no threshold and no provider quality that promotes one into the other
- [ ] A judgment record is dependency-bound like any other proof and goes stale under Law I
- [ ] **Two providers that disagree produce a conflict, not an average** — the same rule `wi merge` already enforces on branches, applied to opinions. Averaging two opinions manufactures a third opinion nobody holds
- [ ] Calibration published with its benchmark set and its N on the same line. No naked confidence percentage anywhere; a percentage without a denominator is authority theater
- [ ] A judgment provider may never sign a decision record, act on an acceptance, or write a record typed `human`, `team_member` or `authorized_editor`

Governing documents: [`references/v5/JUDGMENT_TIER.md`](references/v5/JUDGMENT_TIER.md), [`references/v6/AUTHORITY_MODEL.md`](references/v6/AUTHORITY_MODEL.md).

### v6.2 — Multimodal evidence adapters

Six of the seven anchor kinds are specified and none execute. They ship in this order.

- [ ] **PDF page/region** — page number plus bounding box, with a **page-image digest** so the anchor survives a re-extraction and a human can see the region they are being pointed at
- [ ] **XLSX cell/range** — sheet plus cell range, with **formula dependencies recorded**, so a figure computed from three other cells has three dependencies and goes stale when any of them moves
- [ ] **DOCX paragraphs** — paragraph identity that survives a reflow
- [ ] **Image regions** — bounding box or mask reference
- [ ] **Audio timecode** — start and end, with sample rate
- [ ] **Video frame intervals** — frame index or time range, optional bounding box

Every adapter inherits five rules:

- [ ] **The raw-bytes rule.** The source is the bytes. A decoder's output is a *derived object* with its own digest and named extractor identity, never the source itself. An extractor upgrade is a visible change
- [ ] **Sandbox.** No network, no filesystem write outside a scratch directory, no reach into the graph. A malicious PDF is a normal Tuesday
- [ ] **Declared limits** on size, page count, decode time, memory and recursion depth, with the limit that tripped named in the failure
- [ ] **Quarantine before context.** Ingestion produces a quarantined object; it is scanned; only then may any surface build a model-facing representation. Law F holds at the adapter boundary, not at a delimiter
- [ ] **An unavailable anchor never degrades into a text-span anchor built from recollection.** Law E, stated as a code path

Governing documents: [`references/v5/EVIDENCE_ANCHORS.md`](references/v5/EVIDENCE_ANCHORS.md), [`references/v5/MULTIMODAL.md`](references/v5/MULTIMODAL.md), [`references/v6/CAPABILITY_SECURITY.md`](references/v6/CAPABILITY_SECURITY.md).

### v6.3 — Compiler backends and render source maps

Law M says the semantic state is canonical and every document is a build. Today that is true of Markdown and HTML and specified for everything else.

- [ ] **DOCX, PDF, EPUB, slides and subtitle backends**, each a pure function of `(graph_root, renderer_id, renderer_version, policy_digest)` — two builds from the same tuple produce byte-identical artifacts, or the renderer is defective
- [ ] **Render source maps.** Every emitted artifact carries a map from its bytes back to the meaning that produced them, so a reader can point at a line in a PDF and get the claim atom behind it
- [ ] **`built_from` on every artifact** — graph root digest, renderer identity and version, policy digest. An artifact with none of these is `WI_RENDERING_UNGOVERNED` and no gate may treat it as an output of this system
- [ ] **The reverse-proposal round trip.** An edit made inside a built DOCX is parsed back to a candidate semantic delta and emitted as a proposal against the graph. It is never applied, and where the parser cannot map the edit to a node the proposal is emitted as `unmapped` with the raw before and after — the system does not guess a target
- [ ] **A renderer may change expression and may not change a quantity, a scope, a modality, a hedge, a negation, a causal force, an enumerated exception or a legal force.** Where a target constraint makes the semantically complete rendering impossible, the renderer raises a proposal and renders nothing

Governing documents: [`references/v6/COMPILER_MODEL.md`](references/v6/COMPILER_MODEL.md), [`references/v6/SEMANTIC_SOURCE_MAPS.md`](references/v6/SEMANTIC_SOURCE_MAPS.md).

---

## v6.4 → v6.6 — the compiled core, signing, and federation (Target: 2028)

### v6.4 — The compiled Rust core, behind a parity gate

`scripts/wi.py` is the canonical core and it is a single stdlib-only Python file. That is why surface parity is achievable at all today: there is exactly one thing to call. A compiled core replaces it only under conditions strict enough that nobody has to take the swap on faith.

- [ ] **Rust core with a WASM build** for browser, edge and embedded surfaces
- [ ] **The parity harness is built first**, before there is a second core, so the second core is developed against it rather than validated by it afterwards
- [ ] **Parity gate.** The compiled core and the Python core run the **same shared fixtures** and must produce **byte-identical canonical output, byte-identical digests and identical verdicts**. Nothing switches until parity is proven on **every** fixture, and the parity runner ships as part of the release
- [ ] **Both cores run in CI for at least one full release cycle after parity**, so a divergence has somewhere to be caught
- [ ] **No silent fallback.** A surface that cannot reach the compiled core reports which core answered, or it refuses. A runtime that quietly drops back to the other implementation is two implementations of `verified` with the disagreement hidden — which is the exact failure Law K exists to prevent, arriving as a convenience
- [ ] **Single-binary distribution** — one file, no runtime, no dependencies, checksum published
- [ ] **Air-gapped verifier** — a minimal build that does nothing but `wi verify-release` and `wi capsule`, small enough to carry into a room with no network and audit by reading
- [ ] Language bindings generated from one schema source, never hand-maintained

Until every one of those boxes is checked, any document, deck or README implying a compiled core exists is wrong and should be corrected on sight.

### v6.5 — External signing

- [ ] **Sigstore, C2PA and PROV export** over the closure root a capsule already commits to
- [ ] **Key isolation.** Signing material never enters the process that computes proof. A core that can sign is a core that can be persuaded to sign
- [ ] **A signature attests to a digest and nothing else.** It says who published this closure, not that the closure is true — and the artifact says which of those it means
- [ ] An unsigned bundle keeps reporting `SKIP — unsigned bundle`, because absence of a signature is a fact and not a defect

### v6.6 — Semantic remotes and federation

Meaning across organizational boundaries, where trust is computed locally and never inherited.

- [ ] **Remotes** — push and pull a closure between workspaces
- [ ] **Signed graph deltas**, so what arrives can be checked against what was sent
- [ ] **Import records** naming the remote, the closure root, the moment and the local re-derivation
- [ ] **A remote's `verified` becomes a local `verified` only when this workspace re-derives it from the evidence.** Federation moves artifacts. It does not move authority, and it does not create trust
- [ ] **Continuous rebuild** — watch mode and incremental re-verification, which requires both the closure walk and the compiler backends and therefore cannot come earlier

Governing documents: [`references/v6/FEDERATION.md`](references/v6/FEDERATION.md), [`references/v6/SECURITY_MODEL.md`](references/v6/SECURITY_MODEL.md).

---

## v7.0 horizon — the full sovereign runtime (Target: 2029)

Everything above is one core and a command line. v7.0 is what that core is *for*: surfaces that translate without deciding, a canon graph pointed at constructed worlds, and a migration that can carry five years of state forward without rewriting any of it.

- [ ] **Surfaces** — REST, MCP, SDK and WASM as thin adapters over the same facade, with capability negotiation so a reduced surface states what it cannot do rather than degrading quietly. OpenAPI generated in CI from the core's own schemas, never hand-written
- [ ] **The Workbench** — twelve views over one core: source vault, author canvas with a proof margin, proof inspector, meaning diff, impact view, simulation, branch and merge, authority, obligations, capsule builder, release room, and the argument graph. **Every number on every pane has a visible denominator and a stated reliability type, or it does not appear.** No blended score, no health gauge, no green badge over text that changed after it was checked. A dashboard is where a system with four honest reliability types quietly grows a fifth one called *overall*, and the Workbench is where that failure would be easiest to commit
- [ ] **The storyworld graph** — persistent canon, character state machines, plants and payoffs as edges, and transmedia invalidation using the same minimum repair frontier. A canon check is verified against canon only, inside the fictional realm, and **must never render as externally verified fact**
- [ ] **Autonomous workers under Law P** — anything automated may plan, retrieve, draft, judge, simulate and propose, through the same proposal, impact and authority machinery a person uses. No accrual, no reputation score, no promotion path from proposing to deciding
- [ ] **Migration** — v5 state to v6 state with auditable evidence, re-runnable idempotently, with the previous run's evidence still auditable. It comes last because it must migrate the finished shape; a migration written against a moving target migrates to a state that no longer exists
- [ ] **`.wipack` packages** — genre packs, voiceprints and rule sets as pinned, effect-declaring content with no ambient power

Ordering argument, dependency graph and the exit condition for every wave: [`references/v6/BUILD_MANIFEST.md`](references/v6/BUILD_MANIFEST.md). The one edge in that graph that is not negotiable is **authority before writing** — a write path built first acquires a default caller, the default caller is ambient authority, and the broad grant issued later to keep existing calls working is permanent.

---

## Permanent non-goals

These are not unbuilt features. They are refusals, and they do not move. Full reasoning in [`references/v6/NON_GOALS.md`](references/v6/NON_GOALS.md).

**Carried from v4**

- **Detector evasion.** Never. A system built to produce a machine-checkable account of how a document came to exist cannot also be a system for concealing how a document came to exist.
- **Source generation.** The system will not construct a citation, ever. There is no code path in which a well-formed anchor can be produced for a source that was never ingested.
- **Truth verification.** It verifies support within supplied sources. A capsule that verifies offline on a stranger's machine proves the anchors resolve and nothing drifted. It proves nothing about whether the sources are correct.
- **Absolute quality scores.** There is no universal writing number. Counts with visible denominators are legitimate; a number that stands in for the counts is not.

**Carried from v5**

- **No hosted-account dependency.** The documents that most need this system are the ones that cannot leave the building, and a proof that expires when a vendor does is not a proof.
- **No proprietary-model dependency.** The deterministic tier is model-independent by construction. Judgment providers, when they arrive, are named and replaceable in every record.
- **No vector database as the truth layer.** Negation, attribution swaps and date shifts barely move a vector — every failure this system exists to catch is a small distance in exactly the space a similarity search is scoring.
- **No autonomous source approval.** A discovered source is `candidate`, never `approved`, until a human approves it. An automated approver is an unbounded prompt-injection surface.

**New in v6**

- **No universal truth score.** Not per claim, not per document, not per author. A single number is the artifact people quote, and it is the one output that cannot carry a denominator, a realm or a reliability type with it.
- **No RAG as proof.** Retrieval finds candidates. Only comparison produces proof. A retrieved passage that reads like support is the most convincing wrong answer this system could give, and no amount of embedding turns similarity into evidence.
- **No model as sovereign author.** A model may propose, draft, judge and simulate. It may never sign a decision, hold a grant that decides, appear as an author, or be recorded as a contributor. Authorship is a claim about a person.
- **No cloud dependency in the constitutional path.** Everything that decides — canonicalization, digests, obligations, constraints, merge, capsule verification — runs local-first and offline from one file. A network call in the path that decides is a dependency on somebody else's uptime for your ability to prove what you wrote.
- **No global ontology monopoly.** Concepts are registered per workspace and per federation, and terms are reconciled at boundaries by explicit mapping. A single canonical vocabulary imposed on every user is a governance claim wearing a schema.
- **No overall health gauge.** No blended score across reliability types, no percentage that averages a string comparison with a model opinion, no green badge over text that changed after it was checked. This is the failure the project exists to prevent, pointed at its own UI.
- **No hidden auto-merge of consequential state.** If meaning conflicts, the conflict is preserved. There is no averaging flag, no last-writer-wins rule for quantities, and no setting that turns either on.
- **No ambient plugin power.** An extension does not inherit the authority of the process that loaded it. Effects are declared, granted and revocable; a package that wants a capability asks for it, and a package that has not asked cannot have it.
- **No renderer-side facts.** A renderer may change expression. It may not change a quantity, a scope, a modality, a hedge, a negation, a causal force, an enumerated exception or a legal force. A renderer that needs new meaning emits a proposal and renders nothing.
- **No history rewriting.** A correction supersedes an old state; it does not falsify the record of what was known and when. There is no compaction pass that drops superseded knowledge, because the value of a bitemporal record is precisely the part somebody would want removed.
- **No blockchain** — restated from v5 rather than carried quietly, because v6's Merkle closures and capsules are exactly what make people ask again. Every hard problem here is semantic. A ledger timestamps a digest, which this system already produces, and any timestamping authority an organization already trusts can attest to a closure root without the core knowing or caring.

---

## How to Influence the Roadmap

1. **Star the repo** — signals demand
2. **Open an issue** — describe what you need and why
3. **Open an RFC** — propose substantive additions per [`governance/RFC_PROCESS.md`](governance/RFC_PROCESS.md)
4. **Submit a PR** — build it yourself per [`CONTRIBUTING.md`](CONTRIBUTING.md)
5. **Share results** — run it on your writing, share what worked and what it got wrong

The roadmap is driven by community need, not a corporate product schedule. What gets built next depends on what people actually use and ask for.

Changes to the meaning of `verified`, `stale`, `BLOCK`, `permitted`, `authoritative` or `source quarantine` are not roadmap items. They are constitutional amendments and go through the RFC process with a benchmark case that fails before the change and passes after it.

---

*[github.com/antonio0720/writing-intelligence](https://github.com/antonio0720/writing-intelligence)*
