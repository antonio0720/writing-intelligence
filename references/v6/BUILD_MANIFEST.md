# Build Manifest

**The v6 implementation program as an inspectable object rather than a promise.**

**Status: specified.** Nothing in this document is executable. The v6 program described here has not been built, `plans/v6.manifest.yaml` does not exist in this repository, and no CI job validates one. §4 states that plainly and describes what the file must contain when it is created.

A roadmap is a list of intentions in date order. A build manifest is different in kind: it is a dependency graph with declared exit conditions, in which the *order* is an argument and every wave states what would prove it finished. The distinction matters here because the failure mode of a large specification is not that the wrong things get built — it is that the right things get built in the wrong order, and each one is completed against a substrate that has not settled, so each is rewritten twice.

[`../../ROADMAP.md`](../../ROADMAP.md) states the release intentions and their targets. This document states the order and why it cannot be permuted.

---

## Table of contents

1. What this document is, and what it is not
2. The dependency order
3. The four that must not be built first
4. The wave manifest
5. Year One — finish the v5 promises, build the substrate
6. Year Two — semantic version control and compilation
7. Year Three — portability, federation, migration
8. The v6.0 release-candidate requirements
9. The parity gate
10. The dual-core window
11. Migration, and the cut
12. What is executable and what is specified

---

## 1. What this document is, and what it is not

**It is** the ordering argument for the v6 program, the schema of the machine-readable wave manifest that encodes it, and the release-candidate requirements that decide when v6.0 may be cut.

**It is not** a schedule. There are no engineer-months here, no team allocations and no confidence intervals on dates. The three-year map in §§5–7 groups waves into years because dependency depth makes some grouping honest — a wave whose prerequisites are three waves deep cannot start in the first month — but the years are consequences of the order, not commitments about the calendar.

**It is not a feature list.** Every wave below is described by what it must *make possible*, and every wave declares what would prove it done. A wave with no exit condition is not a wave; it is an aspiration with an identifier, and the manifest schema in §4 refuses one.

**The document that binds each wave is named.** Where a wave has a governing document in this reference set, the wave points at it. The governing document is normative; this manifest states only when it gets built and what it depends on.

---

## 2. The dependency order

**Status: specified.**

Twenty-three waves. Each depends on those above it, and the reason is stated because a reason is what survives an argument to reorder.

| # | Wave | Makes possible | Why it cannot come later |
|---|---|---|---|
| **W01** | Freeze the v5 behaviour contract | A fixed target for parity | Every subsequent wave is measured against v5 behaviour. A contract frozen after the work begins is a contract written to match what was built. |
| **W02** | Canonical primitives | Digests that mean one thing | `wi-json-v1`, NFC, key ordering, decimal normalization and domain separation are what every identity in the system is built from. A primitive changed later invalidates every digest ever computed. |
| **W03** | Parity harness | Proof that two cores agree | Built before there is a second core, so the second core is developed against it rather than validated by it afterwards. |
| **W04** | Immutable object store | State that can be referenced | Nothing can be committed to, branched from or merged into a store that rewrites. |
| **W05** | Semantic IR | Typed meaning | Claims, definitions, obligations, promises and forecasts must have types before a delta between two of them can be classified. [`SEMANTIC_IR.md`](SEMANTIC_IR.md) |
| **W06** | Bitemporal state | Valid time and knowledge time | Retrofitting time into an existing store means rewriting history to add intervals, which is the one operation [`BITEMPORAL_STATE.md`](BITEMPORAL_STATE.md) forbids. |
| **W07** | Constraints and closure | C001–C020, and a walkable dependency set | The closure is what freshness is computed over. Every proof result below depends on being able to walk it. [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) |
| **W08** | Authority | Grants, scope, delegation, expiry | Before anything can write. A write path built first acquires a default caller, and the default caller is ambient authority. [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md) |
| **W09** | Proposals and decisions | Laws A and J as objects | The only route by which a state may change. Built before branches so that a commit has something authorized to commit. |
| **W10** | Branches and merge | Divergence, and conflict retention | Requires a store (W04), a delta (W05) and a decision (W09) to resolve with. [`SEMANTIC_VERSION_CONTROL.md`](SEMANTIC_VERSION_CONTROL.md), [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) |
| **W11** | Simulation | Counterfactual evaluation that mutates nothing | Requires the closure walk (W07) and the merge engine (W10) to report conflicts a change would cause. [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) |
| **W12** | Deterministic proof engine | The L7 layer, as the only decider | Consolidates every check behind one interface, so that the surfaces built later have exactly one thing to call. |
| **W13** | Obligation planning | What a release target requires | Requires typed state (W05) and the proof engine (W12) to know what evidence would satisfy an obligation. |
| **W14** | Judgment gateway | `Judged` records, from named providers | Built after the proof engine so that judgment enters through a gateway with no write path, rather than beside a proof engine that does not yet exist. [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) |
| **W15** | Adapters | PDF, spreadsheet, image, audio, video anchors | Requires the sandbox and effect vocabulary from [`SECURITY_MODEL.md`](SECURITY_MODEL.md) §§5, 7. Every adapter is untrusted input handling. [`../v5/MULTIMODAL.md`](../v5/MULTIMODAL.md) |
| **W16** | Compiler backends | DOCX, PDF, EPUB, slides, subtitles | A rendering is a build from a graph root. Requires the root (W04) and the source maps that bind output back to meaning. [`COMPILER_MODEL.md`](COMPILER_MODEL.md), [`SEMANTIC_SOURCE_MAPS.md`](SEMANTIC_SOURCE_MAPS.md) |
| **W17** | Release signing and disclosure | Capsules, profiles, selective disclosure | Requires the closure (W07) to commit over and the key isolation boundary from [`SECURITY_MODEL.md`](SECURITY_MODEL.md) §4. [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) |
| **W18** | Continuous rebuild | Watch mode, incremental re-verification | Requires the closure walk to know what a change reached, and the compiler backends to rebuild what it reached. |
| **W19** | Surfaces | CLI, REST, MCP, SDK, WASM | Built against a settled core. A surface built earlier is a surface built against a moving facade, and it grows local logic to compensate. [`SURFACES.md`](SURFACES.md) |
| **W20** | Workbench | Twelve views over one core | The last consumer, because it is the one that reveals every gap and the one most expensive to rewrite when the substrate moves. |
| **W21** | Federation | Remotes, capsule exchange, import records | Requires capsules (W17) and authority (W08). Sending a closure to another organization before either exists is sending something whose meaning is not fixed. [`FEDERATION.md`](FEDERATION.md) |
| **W22** | Dual-core window | Both cores in CI, one release cycle | Cannot start before parity passes on every fixture (W03). §10. |
| **W23** | Migration | v5 state to v6 state, with auditable evidence | Last, because it must migrate the finished shape. A migration written against a moving target migrates to a state that no longer exists. [`MIGRATION_V5_TO_V6.md`](MIGRATION_V5_TO_V6.md) |

### 2.1 The three structural rules the order encodes

**Identity before storage.** W02 precedes W04. A store built before its digest rule has an implicit one, and the implicit rule is whatever the serializer did on the first day. Every object ever written under it is then stuck with it, because changing the rule changes every identity.

**Authority before writing.** W08 precedes W09 and W10. This is the most permutable-looking edge in the graph and the most costly to permute. A write path built first works, and it works by having a caller, and the caller is whoever invoked the process — which is ambient authority, arriving as a default rather than as a decision. Retrofitting grants onto a system whose writes already succeed means every existing call site must acquire one, and the pressure at that moment is to issue a broad grant to make the migration tractable. The broad grant is permanent.

**Deciding before translating.** W12 precedes W19. Surfaces built against an unsettled proof engine grow local logic — a small normalization here, a cached verdict there — and each one is a second implementation of `verified` that arrived as a workaround. By the time the engine settles, the workarounds are load-bearing.

### 2.2 What would change this order

An ordering argument that cannot be falsified is a preference. These are the things that would justify a permutation, stated in advance so that a proposal to reorder can be judged against them rather than against enthusiasm:

| Evidence | What it would justify |
|---|---|
| A demonstration that a decoder can run in a sandbox built independently of the effect vocabulary, with the same guarantees | Moving W15 earlier, ahead of W12 |
| A capsule format specified and frozen before the closure engine exists, with the closure walk proven to fit it afterwards | Moving W17 earlier |
| A Workbench built as a pure renderer over a frozen result-object schema, with a test that fails on any local computation | Moving W20 earlier — this is the one most worth trying |
| A migration that can be re-run idempotently against a changed target, with the previous run's evidence still auditable | Moving W23 earlier |

**What would not justify a permutation:** a demonstration deadline, a funding milestone, a competitor's release, or the observation that a later wave is more interesting than an earlier one. Each of those is a real pressure and none of them is evidence about dependency.

**The one edge that is not negotiable.** W08 before W09 and W10 — authority before writing. There is no evidence that would justify moving it, because the failure it prevents is not a technical one: it is that a system whose writes already succeed will be granted broad authority retroactively in order to keep them succeeding, and the breadth is permanent. That is a claim about what people do under deadline pressure rather than about software, and no demonstration falsifies it.

---

## 3. The four that must not be built first

Each of these is the thing a stakeholder asks for first, and each has a specific failure that follows from building it early. They are stated separately from §2 because the ordering argument is easy to accept in the abstract and hard to hold when someone is asking for a demo.

### 3.1 The Workbench

**Why it is asked for first.** It is the only wave that is visible. Everything before W20 is a library, a store or a command-line output, and none of it can be shown to anyone who does not already care.

**Why it must not be.** A UI built over an unsettled core becomes the specification. Every screen encodes an assumption about the shape of the data behind it, and when the core moves, the choice is to rewrite the screen or to keep the core still. The second choice is always cheaper in the moment and it means the UI has become the architecture — decided by layout constraints rather than by the twelve-layer table in [`CONSTITUTION.md`](CONSTITUTION.md) §6.

There is a second failure specific to this system. A Workbench built before the proof engine settles will compute something locally to make a pane responsive. That is L10 deciding proof, and it will not look like a violation; it will look like a loading state that got fixed.

### 3.2 Autonomous agents

**Why it is asked for first.** It is the capability that sounds like the future, and a demonstration of it is compelling in a way that a merge algorithm is not.

**Why it must not be.** An agent built before authority (W08) has no grant to act under, so it acts under whatever the process has — which is everything. An agent built before proposals (W09) has no object to emit, so it writes directly, which is exactly what Law P forbids. An agent built before simulation (W11) cannot show what its change would do before doing it.

Each of those gaps is filled at the time with the smallest thing that works, and the smallest thing that works is a write path. Removing a write path from an agent after the agent is useful is a conversation nobody wins. [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) describes an agent with no write capability at all, and that is only implementable if the agent is built after the things it is supposed to go through.

### 3.3 Federation

**Why it is asked for first.** It is the capability with the clearest commercial story, and it appears to be independent of the rest.

**Why it must not be.** Federation is not a transport problem. It is a trust-computation problem, and the trust is computed locally from a closure — so a federation built before capsules (W17) invents its own exchange format, and a format invented for transport is a format designed for the wire rather than for proof. The second failure is worse: a federation built before authority settles will carry grants across the boundary, because that is the obvious way to make a remote's work usable. [`FEDERATION.md`](FEDERATION.md) forbids it, and the forbidding only holds if the import path was never written to depend on it.

### 3.4 Multimodal adapters

**Why it is asked for first.** It is the most-requested missing capability. Six of the seven anchor kinds are specified and none execute, and a PDF is the format most evidence actually arrives in.

**Why it must not be.** Every adapter is an untrusted-input handler for a hostile file format, and it must run inside a sandbox whose limits, effect vocabulary and quarantine boundary are defined by [`SECURITY_MODEL.md`](SECURITY_MODEL.md). Built before that boundary exists, an adapter runs in-process with filesystem and network access, because that is the default. Retrofitting a sandbox around a decoder that already works means finding every capability it silently acquired, and the ones that are found are the ones that break loudly.

The ordering is not a judgement about value. Multimodal evidence is the highest-value missing capability in the system. It is at W15 because a decoder is the single most likely component to be attacked, and a decoder is only as safe as the boundary that was built before it.

---

## 4. The wave manifest

**Status: specified. `plans/v6.manifest.yaml` does not exist in this repository, and no CI job validates one. This section describes what must be true when it is created.**

The ordering argument in §2 is prose, and prose cannot be validated. The manifest is the machine-readable form of it, so that a dependency cycle or a missing exit gate fails a build rather than surviving a review.

### 4.1 Schema

Four fields per wave. All four are required.

```yaml
waves:
  - id: W02
    name: Canonical primitives
    depends_on: [W01]
    exit:
      - "wi canon emits wi-json-v1 with NFC, sorted keys and normalized decimals"
      - "every digest is domain-separated; two objects of different kinds with
         identical bytes produce different digests"
      - "the v4 and v5 fixture corpora canonicalize byte-identically to the
         frozen v5 contract from W01"

  - id: W08
    name: Authority
    depends_on: [W04]
    exit:
      - "wi authority issue | delegate | revoke | check executes"
      - "delegation monotonicity refuses all eight widening cases in SECURITY_MODEL.md §3"
      - "a revoked grant fails a check at the next transition, not at the next expiry"
      - "no write path in the core is reachable without a resolved grant"

  - id: W09
    name: Proposals and decisions
    depends_on: [W04, W05, W08]
    exit:
      - "wi propose binds a proposal to an exact target state digest"
      - "wi decide refuses WI_DECISION_STALE when the target digest has moved"
      - "an open proposal is never a silent acceptance"
      - "a judgment_provider actor is refused on every decision record"

  - id: W11
    name: Simulation
    depends_on: [W07, W10]
    exit:
      - "wi simulate reports candidate root, semantic deltas, stale frontier,
         provably-unaffected count, conflicts and repair plan"
      - "a simulate run leaves the object store byte-identical, verified by
         digesting the store before and after"
      - "the provably-unaffected count is rendered with its denominator"

  - id: W15
    name: Adapters
    depends_on: [W05, W12]
    exit:
      - "each adapter runs with no network, no filesystem write outside a
         scratch directory, and no reachable graph handle"
      - "a declared ceiling on size, page count, decode time, memory and
         recursion depth exists, and the limit that tripped is named in the failure"
      - "an unavailable anchor never degrades into a text_span built from recollection"
      - "the decompression-bomb and formula-execution fixtures fail closed"
```

| Field | Type | Rule |
|---|---|---|
| `id` | string | Unique. Stable for the life of the program — a wave that is split keeps its id and gains a suffixed sibling, so that a reference in a commit message stays resolvable. |
| `name` | string | Human-readable. Not load-bearing. |
| `depends_on` | list of `id` | Every id must exist. The graph must be acyclic. |
| `exit` | list of string | Non-empty. Each entry states an observable condition, in a form somebody other than the author can check. |

### 4.2 What CI must validate

Five checks, and each one exists because the corresponding failure is invisible in prose:

1. **Every `depends_on` id exists.** A typo in a dependency is a wave with one fewer prerequisite than intended, and nothing about the document looks wrong.
2. **The graph is acyclic.** Two waves that each list the other are a deadlock that reads perfectly well in a table.
3. **Every wave has a non-empty `exit`.** This is the load-bearing check. A wave with no exit condition can be declared finished by assertion, and a program of such waves finishes on schedule every time.
4. **Every `exit` entry is a condition rather than an activity.** *"Authority implemented"* is not an exit condition; *"no write path in the core is reachable without a resolved grant"* is. CI cannot judge this fully, and it can reject the obvious failures: an entry that is only a wave name, an entry under a stated minimum length, an entry that is a restatement of the `name` field.
5. **Ids referenced elsewhere resolve.** A wave id in a commit message, a document or an issue must name a wave that exists.

### 4.3 Why the exit conditions carry the weight

A dependency order is a claim about what must be true before something else starts. An exit condition is what makes *"before"* checkable. Without them the manifest is a list in an order somebody chose, and the order is enforced by memory — which means it is enforced until the first quarter in which a demo is needed and W20 looks tractable.

The condition style matters as much as the presence. Every entry above names something observable: a command that runs, a refusal that fires, a case that fails. None of them names an intention. A wave is finished when a stranger can run the conditions and get the stated answers, which is the same standard this project applies to a claim in a document.

### 4.4 How a wave is declared finished

Not by assertion. A wave closes when every entry in its `exit` list has evidence attached, and the evidence is of one of three kinds:

| Evidence kind | What it is | Where it lives |
|---|---|---|
| **A command transcript** | The command in the condition, run, with its output | The wave's record, verbatim rather than summarized |
| **A fixture result** | A named fixture, and the pass or fail it produces | The test suite, referenced by fixture name |
| **A refusal that fired** | The adversarial case, and the code it returned | The adversarial suite, referenced by case identifier |

A condition with no evidence of one of those three kinds is not met, however obviously true it is. *"No write path in the core is reachable without a resolved grant"* is the kind of statement that is easy to believe and hard to establish, and the only thing that establishes it is a test that attempts a write without a grant and is refused.

**The negative conditions are the ones that decay.** A condition of the form *"X executes"* is proven by running X, and it stays proven because a regression breaks the build. A condition of the form *"Y is refused"* is proven by a test that attempts Y — and if that test is ever deleted, weakened or accidentally made unreachable, the condition silently stops being checked while the wave stays closed. This is the same failure [`SECURITY_MODEL.md`](SECURITY_MODEL.md) §14 describes for the adversarial suite, and requirement G in §8 is where it is caught at release time.

### 4.5 When an exit condition cannot be met

Three responses, and only three:

1. **Narrow the wave.** If a condition cannot be met because it belongs to work the wave does not actually contain, split the wave. The id is stable and gains a suffixed sibling, so the reference in a commit message still resolves.
2. **Record the condition as unmet and hold the wave open.** A wave with one unmet condition is open. It is not *mostly closed*, and nothing downstream may treat it as a dependency that has been satisfied.
3. **Amend the condition, in the open, with a reason.** If the condition was wrong — testing something the wave was never meant to establish — it is changed by an edit that states what it was and why it moved. A condition edited silently is a condition that was met by lowering it.

**What is not a response:** closing the wave and noting the gap in prose elsewhere. That converts a dependency the manifest enforces into a caveat somebody has to remember, which is precisely the substitution this document exists to prevent.

---

## 5. Year One — finish the v5 promises, build the substrate

**Status: specified.**

Two tracks, running in parallel, because they touch different parts of the system and because finishing v5 is what keeps the project honest while v6 is unfinished.

**Track A — the v5 promises.** The v5 documents describe three mechanisms that do not run, and each is a stated promise:

- **The judgment tier (W14).** The deterministic tier says outright that it cannot judge paraphrase. That is the largest remaining gap. The constraint is that adding judgment must not weaken `verified`: a provider ABI with no write path into the graph, records carrying provider, model identifier, prompt/policy hash, input hashes, verbatim output, calibration basis and currency, and disagreement between two providers producing a conflict rather than an average.
- **Multimodal evidence (W15).** PDF region, spreadsheet range, DOCX paragraph, image region, audio interval, video frame — in that order, which is the order of evidentiary value per unit of decoder risk. Every adapter inherits the raw-bytes rule, the sandbox, the declared limits, and quarantine-before-context.
- **Proposals and decisions as records (W09).** Laws A and J are conduct today and become persisted objects: the proposal bound to a target state digest, the decision record naming an actor and an outcome, the decision ledger carried in the bundle.

**Track B — the compiled compatibility substrate.** W01, W02 and W03. Freeze the v5 behaviour contract, settle the canonical primitives, and build the parity harness before there is a second core to test with it.

**Why the two tracks share a year.** Track A produces the fixtures Track B needs. A parity harness with nothing but v4 fixtures proves parity over the subset of behaviour that existed before the interesting parts were built. Every judgment record, every multimodal anchor and every decision object written in Track A becomes a parity fixture, and a fixture written for a feature is a better parity test than one written for parity.

**Year One exit.** The judgment tier, multimodal anchors and decision records execute. The parity harness runs both cores over the full fixture set — with one core present — and the fixture set covers every mechanism that executes.

---

## 6. Year Two — semantic version control and compilation

**Status: specified.**

Waves W04 through W13, plus W16 and W18. This is the year the system stops being a verifier and becomes a runtime.

**The store, the IR and time (W04–W06).** The immutable object store, the typed semantic IR, and bitemporal state. These three are the substrate everything above them assumes, and none of them can be added later without rewriting what is already stored.

**Constraints, authority, proposals, branches, merge, simulation (W07–W11).** The v6 laws become mechanisms. This is the block that is most tempting to reorder and least survivable when reordered — see §2.1.

**The proof engine and obligations (W12–W13).** Every check behind one interface, and the derivation of what a release target requires from typed state and policy.

**Compilation and continuous rebuild (W16, W18).** A rendering becomes a build from a graph root, with source maps binding output back to meaning, and a change to a source rebuilds what it reached rather than everything.

**What "becomes a runtime" means concretely.** At the end of Year One the system answers *is this supported?* At the end of Year Two it answers *what changed, what did that break, who is allowed to fix it, and what would it cost to accept?* The difference is not scope. It is that the second set of questions requires the system to hold state across time and to have an opinion about who may move it, and neither is a feature that can be added to a verifier — they are properties of a different kind of program.

**The hardest wave in the year is W06.** Bitemporal state is the one that looks like a schema change and is not. Valid time and knowledge time have to be present on every state from the first one, because a state written without them has no honest interval to acquire later: nobody knows when it was true, and backdating what was known is the one operation [`BITEMPORAL_STATE.md`](BITEMPORAL_STATE.md) forbids outright. It sits at W06 rather than later for that reason alone, and it is the wave most likely to be deferred on the grounds that nothing needs it yet.

**Two gates in this year:**

- **v6.0-alpha** — the semantic runtime executes end to end on one core. A state can be canonicalized, committed, branched, proposed against, simulated, decided, merged and released, with authority enforced at every write and the closure walked for every verdict. No second core, no surfaces beyond the CLI, no Workbench.
- **v6.0-beta** — the compiled core exists and passes parity on every fixture. Not switched to. Passing.

**Year Two exit.** The alpha and beta gates are met, and the parity harness reports byte-identical canonical output, byte-identical digests and identical verdicts across both cores on every shared fixture.

---

## 7. Year Three — portability, federation, migration

**Status: specified.**

Waves W17, W19 through W23.

**Capsules and disclosure (W17).** Merkle closure, selective disclosure profiles, inclusion proofs. This is the wave that makes a proof portable, and it precedes federation because federation is the transport for something that must already exist.

**Surfaces (W19).** CLI, REST, MCP, SDK, WASM — built against a core that has been settled for a year, with the conformance rules in [`SURFACES.md`](SURFACES.md) §15 as the acceptance criteria.

**The Workbench (W20).** Twelve views, each backed by a command that already runs.

**Federation (W21).** Remotes, capsule exchange, import records. Trust computed locally, never inherited.

**Packs (W17–W19, alongside).** Pinned by digest, effects declared, tightening only, with the project floor not overridable. [`PACKAGE_SYSTEM.md`](PACKAGE_SYSTEM.md)

**The dual-core window (W22)** and **migration (W23)** close the year, and §§10–11 describe both.

**Why portability precedes federation, restated.** A capsule is a proof that survives leaving the building. A remote is a place it goes. Building the second first produces a wire format designed for transport — optimized for size, for streaming, for the shape of the API that carries it — and a format optimized for transport is a format in which the proof closure is an attachment rather than the subject. The capsule format is designed for one reader: a person with the file, a verifier and no trust in whoever sent it. That reader's needs and a wire protocol's needs diverge immediately, and the capsule wins.

**Why the Workbench is in the last year and not the last wave.** W20 precedes W21 deliberately. The Workbench is the surface that reveals every gap in the layers below it, and it is better to discover those gaps before federation is built on top of the same layers than after. It is the last *consumer* rather than the last thing built.

**What Year Three does not contain.** No new proof capability. Every check that will exist at v6.0 exists by the end of Year Two, and the third year is portability, presentation, exchange and migration. A year that added a new check would be a year in which the parity fixture set was still growing, which would push the dual-core window into the year after.

**Year Three exit.** The v6.0 release-candidate requirements in §8, all ten.

---

## 8. The v6.0 release-candidate requirements

**Status: specified.**

Ten requirements, A through J. Every one is a condition somebody other than the author can check. v6.0 is not cut until all ten hold.

| | Requirement | How it is checked |
|---|---|---|
| **A** | **Parity on every shared fixture.** The compiled core and the Python core produce byte-identical canonical output, byte-identical digests and identical verdicts. | Run the parity harness. A divergence is a failure, not a rounding difference. |
| **B** | **Both cores in CI for one full release cycle.** A divergence introduced after parity has somewhere to be caught. | The CI history shows both cores running on every commit for the cycle. |
| **C** | **Single-binary distribution.** One file, no runtime, no dependencies, checksum published. | Download it onto a machine with nothing installed and run it. |
| **D** | **An air-gapped verifier.** A minimal build that does nothing but verify a capsule, small enough to audit by reading. | Read it. The requirement is that reading it is feasible. |
| **E** | **Language bindings generated from one schema source.** Never hand-maintained. | Regenerate in CI and fail if the committed bindings differ. |
| **F** | **Every wave's exit conditions met and recorded.** | The manifest in §4, with each wave's conditions evidenced. |
| **G** | **The adversarial suite passes, and every fixture is proven able to fail.** | Invert each control and confirm the corresponding fixture fails. A suite that cannot fail has not been shown to test anything. |
| **H** | **Every mechanism section in `references/v6/` carries an accurate status marker.** | Cross-check each `**Status: executable…**` claim against the command set that actually runs. |
| **I** | **Migration evidence is auditable by the v5 verifier.** | §11. |
| **J** | **The v5 core remains executable after the cut**, and continues to verify v5 bundles. | Run `verify-release` on a v5 bundle with the v5 core, after v6.0 ships. |

**Why G is on the list.** Every other requirement is a property of the thing built. G is a property of the tests, and it is the one that decays silently: a suite grows by addition, and an added test that passes on the first run is a test nobody has seen fail. [`SECURITY_MODEL.md`](SECURITY_MODEL.md) §14 states the same rule for the adversarial fixtures, and it is repeated here because a release gate is where it gets checked.

**Why J is on the list.** A migration that strands v5 bundles has broken the promise those bundles carry: that a reader with the file and a Python interpreter can verify it, offline, with no model and no prior knowledge of the project. That promise has no expiry date in it, so the cut cannot introduce one.

---

## 9. The parity gate

**Status: specified.**

`scripts/wi.py` is the canonical core, and it is a single stdlib-only Python file. That is why surface parity is achievable at all today: there is exactly one thing to call. A compiled core replaces it only under conditions strict enough that nobody has to take the swap on faith.

**The gate, stated as a refusal:** nothing switches until parity is proven on every fixture, and the parity runner ships as part of the release.

Three properties must match, and they are listed separately because they fail separately:

1. **Byte-identical canonical output.** Same NFC normalization, same key ordering, same decimal representation, same escaping. A difference here is a difference in every digest computed downstream.
2. **Byte-identical digests.** Including domain separation. Two cores that canonicalize identically and separate domains differently produce different identities for the same object.
3. **Identical verdicts.** Same gate result, same status per claim, same disclosure block, same codes. A verdict that differs while the digests match is a difference in the proof engine, which is the most consequential of the three and the hardest to see.

**Why the parity harness is W03 rather than W22.** A harness built after the second core is a harness built to accommodate it. Every ambiguity it encounters — a whitespace difference, a float representation, an ordering that was never specified — gets resolved in whichever direction makes the existing implementations agree, and the resolution is then the specification. Built first, the same ambiguities are resolved against the frozen v5 contract from W01, before either implementation has an opinion.

### 9.1 The fixture corpus

Parity is only as strong as the corpus it runs over, and a corpus assembled at the end is a corpus of the cases somebody remembered. Three rules keep it honest:

1. **Every wave contributes fixtures.** A wave's exit conditions name commands, refusals and cases; each becomes a parity fixture. The corpus grows with the system rather than being written against it.
2. **Every adversarial case is a parity case.** A hostile source, a malformed capsule, a widened delegation, a stale decision — each must produce the *same refusal* on both cores, not merely a refusal on each. Two cores that refuse for different reasons have diverged in the place divergence matters most.
3. **The corpus includes the boring cases.** Empty inputs, single-element collections, a claim with no anchors, a graph with one node, a capsule with nothing withheld. These are the cases where implementations differ by accident, because neither author thought about them and each defaulted to what their language did.

**What parity does not establish.** That either core is correct. Two cores that agree on every fixture agree; if the frozen contract from W01 encoded a mistake, they agree on the mistake. Parity is a statement about substitutability, and it is the only thing a swap requires — but it is not a proof of anything else, and a release note that implies otherwise is wrong.

---

## 10. The dual-core window

**Status: specified.**

After parity passes and before the Python core is retired, both cores run in CI for at least one full release cycle.

**What the window is for.** Parity proves agreement on the fixture set that exists on the day it is run. The window catches divergence introduced afterwards — by a change to one core, by a dependency update under the compiled one, by a platform difference that no fixture happened to exercise. A divergence found in the window is a bug; the same divergence found after the retirement is a bug nobody can bisect, because there is no longer a second answer to compare against.

**What the window costs, stated honestly.** Every change must be made twice, and every fixture runs twice. That is the price of being able to detect a divergence at all, and it is the reason the window has a stated end rather than being indefinite.

**What ends it.** Requirement B in §8: one full release cycle with both cores running on every commit, no unexplained divergence. Not a date.

---

## 11. Migration, and the cut

**Status: specified.**

Migration is W23 — last — because it must migrate the finished shape. A migration written against a moving target migrates to a state that no longer exists by the time it runs, and the second version of it is written under pressure.

### 11.1 The migration requirement

> **v6.0 is not cut until the v5 verifier can independently audit the migration evidence.**

Migration produces a record: which v5 objects became which v6 objects, under what rule, with what digest on each side. That record must be verifiable by the *old* core — the one that has no v6 concepts and no stake in the migration having gone well.

**Why the old verifier rather than the new one.** A migration audited by the system that performed it is a system agreeing with itself. Every migration bug that survives to production survives because the tool that would have caught it shares the assumption that caused it. The v5 verifier cannot read a v6 state, and that is exactly the property that makes it useful: it can confirm that every v5 object it knew about is accounted for, that every digest it can compute still matches, and that nothing it could verify before has become unverifiable.

**What that means concretely.** The migration record carries, for every migrated object, the v5 digest and the v5 canonical form. The v5 core recomputes the digest from the carried form and confirms it matches. Anything that fails is a migration that lost or altered something, and it fails before the cut rather than being discovered afterwards by a reader whose bundle no longer verifies.

The record has four required parts, and the fourth is the one that is usually missing:

| Part | Carries | Audited by |
|---|---|---|
| **The inventory** | Every v5 object, by digest, that existed at the migration boundary | The v5 core, by recomputing each digest from the carried canonical form |
| **The mapping** | v5 digest → v6 digest, one row per object, with the rule applied | The v6 core, by re-deriving the v6 digest from the v5 form under the named rule |
| **The rules** | Every transformation rule, named, with its inputs and outputs | Read by a person. A rule that cannot be stated in a sentence is a rule nobody can audit. |
| **The unmigrated set** | Every v5 object that was *not* migrated, with a reason per object | The v5 core, by confirming each named object existed and is accounted for |

**Why the unmigrated set is the part that matters.** A migration report listing what moved is a report that cannot distinguish an object that was deliberately left behind from one that was dropped. Both render as absence. An explicit unmigrated set with a reason per object turns the second into a visible failure, and it is the same argument as declared omission in [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md) §3 applied to a one-time event with no second chance.

### 11.2 What migration does not do

It does not rewrite history. A v5 state that migrates into v6 acquires a valid interval and a knowledge interval, and the knowledge interval says *known since migration* rather than being backdated to when the state was written. Backdating would be more convenient and it would be a claim the system cannot support: nobody knew, at the time the v5 state was written, what a v6 knowledge interval was.

It does not upgrade a basis. A v5 `verified` becomes a v6 `Verified` with the same closure and the same evidence. It does not become verified *under the v6 constraint engine* unless the v6 constraint engine has actually run over it, and where it has not, the state is `invalidated_by_edit` against the new closure — which is the honest answer and the inconvenient one.

It does not strand v5 bundles. Requirement J.

---

## 12. What is executable and what is specified

**Status: specified.**

| Subject | State |
|---|---|
| Everything in this document | Specified |
| `plans/v6.manifest.yaml` | **Does not exist.** No such file is in this repository. |
| CI validation of a wave manifest | **Does not exist.** The workflows in `.github/workflows/` validate the verifier, the schemas, the documentation links, the bundle and the API. None validates a manifest. |
| The parity harness | Specified. No second core exists to run it against. |
| The compiled core | Specified. There is no Rust, no WASM, no daemon and no single-binary distribution. |
| Waves W01 through W23 | Specified. None is complete. |
| The three-year map | Specified, and it is an ordering argument rather than a schedule. |

**The honest summary.** This document describes a program that has not started, in an order that is argued rather than assumed, with exit conditions that would let somebody else tell whether a wave finished. Its own status marker is the one it hands to every wave below it: **specified**, and that word means the same thing here as it does everywhere else in this reference set.

---

Read next:

- [`CONSTITUTION.md`](CONSTITUTION.md) — the laws these waves implement, and the twelve-layer table the order follows
- [`SECURITY_MODEL.md`](SECURITY_MODEL.md) — why authority and process isolation precede autonomy
- [`SURFACES.md`](SURFACES.md) — the acceptance criteria for W19
- [`MIGRATION_V5_TO_V6.md`](MIGRATION_V5_TO_V6.md) — the migration this manifest schedules last
- [`NON_GOALS.md`](NON_GOALS.md) — what will not be built, in any wave, in any year
- [`../../ROADMAP.md`](../../ROADMAP.md) — the release intentions and their targets

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
