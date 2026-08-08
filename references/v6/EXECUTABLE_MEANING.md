# Executable Meaning

The thesis of v6, stated once and then derived.

> **A work is a versioned, typed, bitemporal, authority-governed semantic program. A document is a build artifact. A source is an immutable input. An edit is a typed state transition. A release is a compiled artifact plus a proof closure.**

Five sentences. Every mechanism in `references/v6/` is a consequence of one of them, and the twelve-step derivation in section 4 shows how each one forces the next.

Read [`CONSTITUTION.md`](CONSTITUTION.md) first. This document explains why the six v6 laws are the laws they are; the constitution states them and binds them.

---

**Contents:** the five sentences · the lineage · the twelve-step derivation · one sentence through all twelve steps · what "executable" means and what it does not · where the program analogy breaks · executable versus specified.

---

## 1. The five sentences

**Status: specified as thesis; the mechanisms named in the right-hand column carry their own markers throughout `references/v6/`.**

Each sentence replaces an assumption that every writing tool ever built has made without stating it.

| The unstated assumption | The v6 sentence | The mechanism |
|---|---|---|
| A work is a file | A work is a versioned, typed, bitemporal, authority-governed semantic program | The graph root, and `wi commit` |
| The document is the thing | A document is a build artifact | Law M, and the `built_from` root |
| A source is a reference | A source is an immutable input, addressed by the digest of its raw bytes | [`../v5/EVIDENCE_ANCHORS.md`](../v5/EVIDENCE_ANCHORS.md) section 4 |
| An edit is a change to text | An edit is a typed state transition | Law H's delta classes, and `wi propose` |
| A release is a file you send | A release is a compiled artifact plus a proof closure | `wi capsule`, and [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) |

### 1.1 Reading the first sentence carefully

Four adjectives, and none of them is decoration.

**Versioned** means the work has a history of states rather than a history of files, and any prior state can be named exactly rather than approximately. A filename with a date in it is a version in the way a sticky note is a database.

**Typed** means the objects in it have kinds that determine what checks apply. A promise is not a claim is not a definition is not a forecast, and the difference is not stylistic — it determines what would count as evidence and what would count as a breach.

**Bitemporal** means every state knows both when the thing it asserts holds in the world and when this system believed it. That is two clocks, and collapsing them into one is the failure Law N exists to prevent.

**Authority-governed** means a transition needs a grant. Not a role, not ownership, not possession of the file. A grant with a scope and an expiry.

### 1.2 Why "program" and not "database"

A database holds state. A program holds state *and the rules by which state may change*, and it is the second half that matters here. The interesting properties of v6 are all properties of transitions: what a change is allowed to be, who may make it, what it invalidates, what it must prove afterwards. A database with a governance document beside it has none of those properties; it has a document nobody reads and a table anybody can write.

The word also sets an expectation worth setting: a program has an execution model, and an execution model can be wrong in ways a schema cannot. Most of this release is about that execution model.

### 1.3 Why the third sentence is separate from the first two

*A source is an immutable input* looks like a restatement of *a document is a build artifact*. It is the opposite claim, and the two together are what make the system closed.

A build artifact is downstream: produced by the system, overwritable, never authoritative. A source is upstream: produced by somebody else, never touched, and authoritative about its own bytes and nothing else. The rule that follows is the one in [`../v5/EVIDENCE_ANCHORS.md`](../v5/EVIDENCE_ANCHORS.md) — a `source.version` is `sha256(raw bytes)` with no normalization of any kind, because the moment the system normalizes before hashing, the fixed point of the whole apparatus depends on the normalizer.

Everything in a v6 workspace is therefore one of exactly three things: an immutable input, a governed state, or a build artifact. There is no fourth category, and a file that claims to be one is `WI_RENDERING_UNGOVERNED`.

---

## 2. The lineage

**Status: specified as a statement of what each release did.**

Each version solved the problem the previous one made visible.

| Version | What it made the system able to do | What it left unsolved |
|---|---|---|
| **v1 — compiled prose** | Treat a draft as something with a compilation pipeline: passes, checks, a build. Writing stopped being a single undifferentiated act. | The compiler had no memory of the work as a whole. Every run started from the text. |
| **v2 — narrative systems** | Hold a work's structure, voice and world as durable objects rather than as instructions repeated in every prompt. | Nothing governed whether the work's *claims* were true, or whether the system was honest about having checked. |
| **v3 — governed authorship** | Enforce craft: eleven passes, genre packs, voiceprints, anti-slop, measured against something rather than asserted. | Craft governance says nothing about evidence. A well-built sentence can be fabricated. |
| **v4 — accountable claims** | Bind a claim to a verbatim span in a supplied source, refuse to mark support that cannot be pointed at, and never report a check that did not run. | A verification was a photograph. It was true about a wording at a moment and had no way to notice when it stopped being true. |
| **v5 — proof-carrying dependency graph** | Give meaning an identity separate from wording, bind proofs to exact states, compute staleness, and ship a bundle a stranger verifies offline with no model. | The graph was single-writer, single-timeline and ungoverned. It could prove a finished thing; it could not survive being worked on by several people, several processes and several years. |
| **v6 — executable meaning** | Make the graph a runtime: versioned, branched, merged, timed, authorized, simulated, federated — with every transition accountable. | Stated in section 6. |

**The pattern is worth naming.** Every release solved a correctness problem and created a *scale* problem, and the scale problem was always the same one: the previous solution assumed a smaller population than the next situation contained. v4 assumed one document. v5 assumed one writer and one timeline. v6 assumes many of both, and its unsolved problems are named rather than deferred quietly.

**What did not change across six versions.** Law C. From v1's insistence that a pass report say which passes ran, through v4's five capability states, to v6's `WI_FRESHNESS_UNCOMPUTED`, the same rule has been re-implemented at every new layer: *the system must be able to distinguish did not pass, could not check, and chose not to check, and must never collapse them.* Every release has found a new place where that distinction was being lost. That is the through-line, and it is the reason the status markers in these documents exist at all.

---

## 3. How to read the derivation

**Status: specified.**

Section 4 is an argument, not a feature list. Each step is *forced* by the one before it — meaning that if you accept step *n*, refusing step *n+1* leaves you with a system that contradicts itself.

Each step therefore carries three lines beyond its reasoning:

| Line | What it says |
|---|---|
| **Forced by** | Which earlier step makes this one unavoidable |
| **Refusing it costs** | The concrete failure a system exhibits if it takes every prior step and stops here |
| **Mechanism** | What implements it, and whether that thing runs |

The middle line is the one that matters. A derivation with no stated cost of refusal is a preference presented as a proof.

---

## 4. The twelve-step derivation

---

### Step 1 — Meaning has identity

**Forced by:** v5's Law G, which v6 inherits.

If a claim is only its current wording, then every rewrite destroys the claim and creates a new one, and nothing downstream can be maintained. So a claim gets a `logical_id` that survives rewording and a `state_digest` that changes when meaning moves. That pair is the whole of v5's identity model, and it is the premise everything below rests on.

**Refusing it costs:** every guarantee in the system becomes a guarantee about a string, and every string is one rewrite away from being a different string. Moving a grant narrative into a board memo loses the thread entirely, because the sentence changed completely and the promise did not change at all.

**Mechanism:** [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) section 4. **Executable.**

---

### Step 2 — If meaning has identity, rendering becomes compilation

**Forced by:** step 1.

Once meaning exists independently of its wording, a document is no longer the work — it is *one expression* of the work. Six documents carrying the same claim are six renderings, and the question "did the deck and the narrative say the same thing" becomes a graph query rather than a proofreading task.

But an expression that can be edited independently is a second source of truth, and that is not a rendering. It is a fork nobody declared. So the compilation direction has to be one-way: state compiles to document, and a change to a document is a proposal against state.

**Refusing it costs:** two sources of truth in one workspace, diverging silently. Every check still passes, because the checks run against the graph and the edit happened in the file.

**Mechanism:** Law M. `wi canon` is executable; the renderer boundary and reverse-proposal path are **specified**.

---

### Step 3 — If rendering is compilation, the state needs version control

**Forced by:** step 2.

A compiler needs a source tree with a history. Not a backup, not a snapshot directory, and not a chat log — a history in which any prior state can be named exactly, two states can be compared, and work can proceed on two lines at once without one overwriting the other.

The file-level version control that already exists cannot do this job, and the reason is not that it is bad at it. `git` versions *bytes*. Two commits that reword one sentence identically are two different diffs; one commit that changes 11,800 to 12,000 inside a reflowed paragraph is a diff whose important part is invisible among the reflow. A history over meaning has to be a history over semantic states.

**Refusing it costs:** the only recoverable prior state is a file, so "what did this claim say before the review" is answerable only by reading old files and remembering which paragraph mattered.

**Mechanism:** `wi branch`, `wi commit`, `wi log`. **Executable.** Full treatment: [`SEMANTIC_VERSION_CONTROL.md`](SEMANTIC_VERSION_CONTROL.md).

---

### Step 4 — If there are branches, there must be a semantic merge

**Forced by:** step 3.

Branches that cannot be merged are forks, and a fork is two works. So merge is not optional once branching exists.

And a *text* merge is worse than no merge here, because of a specific asymmetry. Text merge conflicts on overlapping edits and completes cleanly on non-overlapping ones. But the dangerous case in a governed work is two edits in *different paragraphs* that assert incompatible things — a text merge completes that silently and the contradiction ships. The merge has to operate on semantic deltas, and when two deltas intersect on a consequential dimension it has to stop and keep both.

**Refusing it costs:** a merged document containing a contradiction neither author wrote, introduced by a tool that reported success.

**Mechanism:** Law Q. `wi merge` and `wi conflicts`. **Executable.**

---

### Step 5 — If states have history, they need time that is not their commit time

**Forced by:** step 4, and by the first correction anyone receives.

A commit timestamp says when the system was told. It does not say what period the claim covers, and those are different facts that behave differently. A revised unemployment figure for 2026, published in 2029, has a valid time in 2026 and a knowledge time in 2029, and a system with one clock has to discard one of them.

Discarding valid time makes contradiction detection useless: two tax rates for two different periods look like a conflict. Discarding knowledge time makes the audit impossible: nobody can reconstruct what was known when the document was filed. Both are required, so both are stored.

**Refusing it costs:** either a contradiction report full of false alarms that people stop reading, or an audit trail that cannot answer what the author knew on the day they signed.

**Mechanism:** Law N. `wi as-of --valid-at --known-at`. **Executable.** Full treatment: [`BITEMPORAL_STATE.md`](BITEMPORAL_STATE.md).

---

### Step 6 — If several actors write, authority must be explicit

**Forced by:** step 3, the moment a second identity exists.

Branching implies collaboration; collaboration implies more than one writer; more than one writer means *who did this* is no longer the same question as *were they allowed to*. In a single-author workspace those questions collapse, which is why v5 could answer only the first.

The default answer — whoever holds the file may do anything — is not a policy. It is the absence of one, and it makes every other control decorative, because a proposal system any actor may bypass is a suggestion box.

**Refusing it costs:** an accountability layer that records who made every change and cannot say that any of them was permitted, which is the shape of a system that satisfies an audit and prevents nothing.

**Mechanism:** Law O. `wi authority issue | delegate | revoke | check`. **Executable.** Full treatment: [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md).

---

### Step 7 — If authority is explicit, autonomy can be bounded rather than banned

**Forced by:** step 6, and by the fact that autonomous actors are useful.

Once authority is a grant rather than an ambient property, an autonomous actor can be given a real and bounded place in the system: it holds read capability, it holds `claim.propose`, and it holds nothing else. That is a stronger position than banning it, because banning it produces the same work done outside the system with no record at all.

The bound has to be structural rather than behavioural. Not *the agent should not write* — *there is no code path by which an agent writes*. And because an autonomous act is not predictable from its configuration, the record has to carry enough to replay it: inputs by digest, policy by digest, output verbatim.

**Refusing it costs:** either the agent is banned and the work happens in an ungoverned tool, or the agent writes and the change rate exceeds anyone's ability to review, at which point attribution becomes archaeology.

**Mechanism:** Law P. `wi propose`, `wi proposals`, `wi decide`. **Executable.** The agent runtime that would call them is **specified**.

---

### Step 8 — If actors propose, they need counterfactuals

**Forced by:** step 7.

An actor that must not write still has to know what its change would do — and so does the human deciding on it. "Accept this?" is an unanswerable question without the consequence attached. The consequence is not a preview of the text; it is the dependency impact: what breaks, what does not, what is now unproven, what needs a person.

This is also the step that makes autonomy safe to run at volume. An agent that simulates before proposing can decline to propose things whose blast radius exceeds its objective, and it can say so.

**Refusing it costs:** every decision is taken blind, so reviewers approve on the readability of the sentence rather than on the consequence of the change — which is exactly the failure the whole stack exists to prevent, moved one level up.

**Mechanism:** `wi simulate` — candidate root, semantic deltas, stale frontier, provably-unaffected count, conflicts, repair plan, mutating nothing. **Executable.**

---

### Step 9 — If change is continuous, verification must be maintenance

**Forced by:** steps 3 through 8 together.

v4's verification was an audit: run it, get a verdict, ship. That model assumes work stops. Once a work has branches, agents, corrections and several people, work does not stop, and a verdict computed on Tuesday describes a graph that no longer exists on Thursday.

So freshness cannot be a stored flag or a date. It has to be computed from the closure, per query, with its basis stated — and the honest half of that report is the provably-unaffected count, because a maintenance system that only reports breakage produces a wall of red and gets switched off.

**Refusing it costs:** a green badge over an edited sentence, which the v4 doctrine already names as worse than no badge, now reproduced at branch, release and dashboard level where it is harder to notice.

**Mechanism:** Law R. `wi constraints`, `wi obligations`, and the freshness basis on `wi why`. **Executable.**

---

### Step 10 — If the work is portable, verification must be too

**Forced by:** step 9, and by the fact that consequential documents leave the building.

A proof closure that only verifies inside the workspace that produced it proves something to its author. The reader — a funder, a regulator, a counterparty, a court — has no access to that workspace and no reason to trust it. So the closure has to travel: a portable object carrying the states, the anchors, the decisions and a commitment over all of them, verifiable by a machine that has never seen the workspace.

And it has to travel *partially*, because most consequential work contains material that cannot be shared: a source under an agreement, an identifiable person, an unreleased figure. A commitment structure that permits proving membership without disclosing content is what makes redaction honest rather than lossy.

**Refusing it costs:** verification becomes a claim the author makes about their own work, which is the position every document was in before any of this existed.

**Mechanism:** `wi capsule create | inspect | verify` — Merkle proof closure, selective disclosure, inclusion proofs. **Executable** on a local filesystem. Remotes, transport and signing are **specified**.

---

### Step 11 — If closures cross organizations, policy must be portable

**Forced by:** step 10.

Two organizations exchanging capsules are exchanging evidence, not standards. An anchor that satisfies one organization's evidence policy may not satisfy another's, and a capsule that carries a verdict rather than its basis has moved the trust rather than transferred it.

So a capsule carries the policy digest it was built under, and the receiving workspace re-derives its own verdict under its own policy from the evidence in the capsule. Agreement between the two verdicts is informative. Adoption of the sender's verdict is not verification.

**Refusing it costs:** a federation in which every organization inherits the weakest policy in the network, without any of them having agreed to it.

**Mechanism:** [`../v5/POLICY_AS_CODE.md`](../v5/POLICY_AS_CODE.md) as the policy object; the cross-organization re-derivation path is **specified**.

---

### Step 12 — The end state

**Forced by:** all of the above.

A work is a program. Its state is versioned and branchable. Its transitions are typed, authorized, simulated and decided. Its truth is bitemporal. Its disagreements are retained. Its freshness is computed. Its proof is portable and partially disclosable. Its renderings are builds.

The property that falls out — and the only one worth the machinery — is this: **the work can be maintained by people who were not there when it was written, and defended to people who were not there when it was checked.**

**Refusing it costs:** nothing, if the work is small, short-lived and has one author. That case is real and the machinery is not free. v6 is for the other case, and [`../v5/NON_GOALS.md`](../v5/NON_GOALS.md) is where features that serve neither go.

---

## 5. One sentence through all twelve steps

**Status: specified as an illustration; the individual commands shown carry the statuses given in section 7.**

The derivation is abstract. Here it is on one sentence, from a grant narrative, across three years.

**March 2027.** The author writes:

> Between 2019 and 2022, the program served 11,800 households.

| Step | What happens to it |
|---|---|
| 1 | It becomes claim atom `c-0002` with a `logical_id` and a `state_digest`. Quantity 11,800, unit households, valid `[2019-01-01, 2023-01-01)`. |
| 2 | The narrative, the deck and the board memo each `renders_as` it. Three expressions, one claim. Editing the deck's wording proposes against `c-0002`; it does not create a second number. |
| 3 | The commit that introduced it is in `wi log`, with a graph root. Nine months later, "what did this say before counsel reviewed it" is a lookup. |
| 4 | Counsel works on `review/counsel` and the author works on `main`. Counsel changes the modality of a nearby promise; the author tightens this sentence's rhythm. The merge composes both — the deltas do not intersect. |
| 6 | The intern who reformats chapter 2 holds `claim.accept.wording_only` scoped to `ch-02`, expiring in two weeks. They can tighten the sentence. They cannot change 11,800. |

**October 2028.** The partner issues a corrected assessment. The count for the period is 12,150.

| Step | What happens to it |
|---|---|
| 5 | The correction does not overwrite. `c-0002` keeps valid `[2019-01-01, 2023-01-01)` and gains a knowledge interval closing in October 2028; a new state opens with the same valid interval and quantity 12,150. Both are retained. |
| 9 | The March 2027 anchor is `WI_ANCHOR_STALE`. So is the board memo's attestation, and the deck's. The PDF's bytes have not changed; the claim that it was verified has. |
| 8 | `wi simulate` reports the frontier — four nodes — and, beside it, that 1,914 nodes are provably unaffected because no anchor outside the changed byte range intersects it. |
| 7 | An agent proposes the re-anchor and the numeric update. It writes nothing. `wi proposals` shows one open proposal with `produced_by` naming its inputs by digest. |

**January 2029.** The funder asks whether the filed narrative was accurate.

| Step | What happens to it |
|---|---|
| 5 | `wi as-of --valid-at 2022-06-01 --known-at 2027-03-14` returns 11,800 — what was believed when it was filed. `--known-at 2029-01-15` returns 12,150 — what is believed now. Both are answers, and they are different questions. |
| 12 | The answer does not depend on anyone remembering March 2027. |

**March 2029.** A second funder asks for evidence, and the assessment is under a confidentiality agreement.

| Step | What happens to it |
|---|---|
| 10 | `wi capsule create --profile redacted` carries the claim states, the decisions, the closure and a Merkle commitment. The source bytes are withheld and declared withheld. |
| 11 | The funder's workspace re-derives its own verdict under its own policy. Its policy requires two independent anchors where ours required one, so it returns `needs_source` — correctly, and visibly, rather than inheriting our answer. |

The last row is the point of step 11 and it looks like a failure. It is the system working: two organizations disagreed about what counts as sufficient evidence, and the disagreement surfaced as a verdict instead of being resolved by whoever exported first.

---

## 6. What "executable" means here, and what it does not

**Status: specified.**

The title of this document is a claim, and claims in this project carry their limits with them.

**It means:** meaning is held in structures a machine can evaluate — typed states with digests, edges with invalidation policies, intervals with arithmetic, grants with scopes, obligations with satisfaction conditions. Questions that were previously matters of memory or judgment become traversals: *what depends on this*, *what did we know then*, *who approved this*, *what breaks if this moves*.

**It does not mean the work runs itself.** There is no execution in which the system writes the document. Every consequential transition still ends at a human decision under a grant, and the constitution's entire architecture exists to keep it there.

**It does not mean meaning is formalized.** The semantic IR holds the dimensions along which consequential changes are mechanically detectable. It is not an ontology of language and must not become one — that boundary is stated in [`SEMANTIC_IR.md`](SEMANTIC_IR.md) section 1 and in [`../v5/SEMANTIC_IR.md`](../v5/SEMANTIC_IR.md) section 3, and it is the single most important limit in the design. A dependency model that works for quantities, dates, modality, scope and negation is worth more than a complete theory of meaning that never ships.

**It does not mean the output is true.** The system verifies support within supplied sources and the integrity of its own state transitions. It does not verify the world. A capsule that verifies proves the anchors resolve, the digests match and nothing drifted. It proves nothing about whether the sources were right, and no amount of machinery in this repository changes that.

---

## 7. Where the program analogy breaks

**Status: specified.**

Analogies are load-bearing until they are not, and this one has five places where following it further would produce a worse system. They are stated here so nobody has to discover them by building the wrong thing.

**A program has one correct output; a work has many acceptable ones.** A compiler that produces two different binaries from one source is broken. A renderer that produces two different sentences from one claim is doing its job — expression is genuinely free where meaning is fixed. This is why the renderer contract constrains semantic dimensions and says nothing about word choice, and why any attempt to make rendering deterministic at the sentence level should be refused. Determinism belongs to the build tuple, not to the prose.

**A program's semantics are total; a work's are not.** Every construct in a programming language has defined behaviour. Most sentences in a real document carry dimensions the IR cannot extract, and the correct response is a null field and a statement that it is null — not an inferred value. The system is a partial function over meaning, and pretending otherwise is how a governance layer starts producing confident nonsense.

**A program can be tested exhaustively against a specification; a work cannot.** There is no specification of a grant narrative against which it can be checked. `wi test` runs *writing tests* — contracts the author declared, invariants over concepts, constraints over the graph. It does not and cannot check that the document is good, and no quality score will be added. That refusal is permanent and is in [`../v5/NON_GOALS.md`](../v5/NON_GOALS.md).

**A program's failures are crashes; a work's failures are plausible.** This is the one that matters most. A defective program usually stops. A defective document reads perfectly and is wrong, which is why every mechanism here is built around making the invisible failure visible rather than around preventing an obvious one. It is also why Law C sits at the root: the worst state this system can reach is not an error. It is a green report over something nobody checked.

**A program's dependencies are declared; a work's are discovered.** A build file lists what it needs. A document's real dependencies — the source that a figure came from, the definition a later chapter relies on, the assumption a forecast rests on — are latent in the prose and have to be extracted, and extraction is incomplete. This is why an undeclared dependency is a named state rather than an absence: the system reports what it could not resolve rather than assuming a clean graph, and `wi obligations` exists to say what a target requires that nothing currently satisfies.

---

## 8. Which law each step became

**Status: specified.**

The derivation is not a narrative written after the laws. The laws are what the steps hardened into once it became clear which of them could be violated quietly.

| Step | Became | Because the failure it prevents is invisible |
|---|---|---|
| 1, 2 | Law M — the semantic state is canonical, renderings are builds | A rendering that drifted from the state it was compiled from still reads correctly, and the drift is only detectable if one of them is authoritative. |
| 5 | Law N — time is part of meaning | A correction that overwrites its predecessor leaves a workspace unable to say what it reported, and the inability is not noticed until somebody asks. |
| 6 | Law O — authority is explicit, scoped and expiring | Permission inherited from a role is permission nobody stated, so nothing can check it and every audit reconstructs intent from a job title. |
| 7, 8 | Law P — autonomy produces replayable proposals, not invisible mutations | An automated change that is correct today is indistinguishable, in the record, from one that was never reviewed. |
| 4 | Law Q — semantic disagreement is preserved until resolved | An auto-resolved merge produces a document nobody wrote and nobody would defend, and it produces it silently. |
| 3, 9 | Law R — freshness is a property of dependencies, not a green badge | A verification that stayed green after its source moved is worse than no verification, because it was believed. |

Steps 10, 11 and 12 did not become laws. They are consequences: federation, portable policy and the end state all follow from M through R holding across a boundary rather than adding a new obligation of their own. A step that produces no new way to be quietly wrong does not need a law, and adding one would dilute the six that do.

**Why the mapping is worth stating.** A law without a derivation is a rule somebody has to be persuaded of. A derivation without laws is an argument nobody is bound by. The pairing means every rule in [`CONSTITUTION.md`](CONSTITUTION.md) can be traced back to the specific failure that motivated it, and every step above can be checked against something enforceable.

---

## 9. What is executable and what is specified

| Mechanism | Status |
|---|---|
| Canonical serialization and domain-separated state digests — `wi canon` | Executable in `scripts/wi.py` |
| Semantic version control — `wi branch`, `wi commit`, `wi log` | Executable in `scripts/wi.py` |
| Proposals and decisions — `wi propose`, `wi proposals`, `wi decide` | Executable in `scripts/wi.py` |
| Counterfactual evaluation — `wi simulate` | Executable in `scripts/wi.py` |
| Conflict-preserving semantic merge — `wi merge`, `wi conflicts` | Executable in `scripts/wi.py` |
| Capability grants — `wi authority` | Executable in `scripts/wi.py` |
| Proof obligations — `wi obligations` | Executable in `scripts/wi.py` |
| Bitemporal query — `wi as-of` | Executable in `scripts/wi.py` |
| Graph constraints C001–C020 — `wi constraints` | Executable in `scripts/wi.py` |
| Proof capsules with inclusion proofs — `wi capsule` | Executable in `scripts/wi.py` |
| Backward explanation — `wi why` | Executable in `scripts/wi.py` |
| The renderer boundary and reverse proposals from a rendering | Specified |
| Compiler backends beyond Markdown and HTML | Specified |
| The agent runtime, the plugin host, judgment providers | Specified |
| Remotes, capsule transport, cross-organization policy re-derivation | Specified |
| Signing, watch mode, the Workbench, REST and MCP v6 | Specified |
| A compiled core in another language | Roadmap. Nothing in this release is written in Rust, and no part of the system requires it. |

---

## Related documents

- [`CONSTITUTION.md`](CONSTITUTION.md) — the six v6 laws this thesis derives
- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — the typed objects the program operates on
- [`SEMANTIC_VERSION_CONTROL.md`](SEMANTIC_VERSION_CONTROL.md) — steps 3, 4, 7 and 8 in operation
- [`BITEMPORAL_STATE.md`](BITEMPORAL_STATE.md) — step 5 in operation
- [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md) — step 6 in operation
- [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) — step 1, and the identity model everything rests on
- [`../v5/STALENESS.md`](../v5/STALENESS.md) — step 9 as it exists today
- [`../v5/NON_GOALS.md`](../v5/NON_GOALS.md) — the refusals that keep the analogy from being followed too far
- [`../../ROADMAP.md`](../../ROADMAP.md) — what is scheduled and what is not
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
