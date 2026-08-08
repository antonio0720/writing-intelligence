# Non-Goals

What Writing Intelligence v6 refuses to do, and why each refusal is load-bearing rather than decorative.

A non-goal is not a gap in the roadmap. It is a decision that has already been made, with reasoning attached, so that it does not have to be re-litigated every time someone arrives with a plausible reason to cross the line. **The plausible reason is the point.** None of these refusals exist to block bad ideas. They exist to block good-sounding ones, and every entry below has been proposed by a competent person with a real problem.

v6 makes the refusals more urgent rather than less, and for a specific reason: v5 could only produce a reading, and a wrong reading is corrected by reading again. v6 writes — it merges, delegates, decides, seals and acts. A refusal that fails in v6 does not produce a bad report. It produces a state transition that is now part of the history everything downstream reasons from.

---

## Table of contents

**Carried forward**

1. From v4 and v5 — summarized, with the originals linked

**New in v6**

2. No universal truth score
3. No RAG as proof
4. No model as sovereign author
5. No silent citation generation
6. No cloud dependency in the constitutional path
7. No blockchain
8. No global ontology monopoly
9. No "overall health" gauge
10. No hidden auto-merge of consequential state
11. No ambient plugin power
12. No renderer-side facts
13. No history rewriting

**Operating with refusals**

14. How to decline without being useless
15. What a non-goal is not

---

## 1. Carried forward from v4 and v5

**Status: in force. Full reasoning at [`../v5/NON_GOALS.md`](../v5/NON_GOALS.md) and [`../v4/NON_GOALS.md`](../v4/NON_GOALS.md).**

Every prior refusal carries into v6 unchanged. They are summarized here in one line each so that a reader of this document knows the full set; the argument for each lives where it was made, and is not restated at length because a refusal restated is a refusal available for re-negotiation at every restatement.

| Refusal | One line | Origin |
|---|---|---|
| **Detector evasion** | A system built to produce a machine-checkable account of how a document came to exist cannot also conceal how it came to exist. | v4 |
| **Source generation** | No citation is ever constructed. There is no code path producing a well-formed anchor into a source that was never ingested. | v4 |
| **Truth verification** | Support within supplied sources is not truth. A bundle that verifies on a stranger's machine proves the anchors resolve; it proves nothing about whether the sources are right. | v4 |
| **Absolute quality scores** | There is no universal writing number. Counts with visible denominators are legitimate; a number that stands in for the counts is not. | v4 |
| **Ghostwriting that erases authorship** | Every change is a proposal with a recorded decision. An author who cannot see what changed is not the author. | v4 |
| **Unauthorized voice modeling** | Modeling a real, named person's voice requires a stated consent basis. | v4 |
| **Silent memory** | Preferences inferred across a session are stated before they are applied. | v4 |
| **No hosted-account dependency** | Nothing constitutional requires a server. A proof that expires when a vendor does is not a proof. | v5 |
| **No proprietary-model dependency** | The deterministic tier is model-independent by construction; providers are named and replaceable. | v5 |
| **No vector database as the truth layer** | Embeddings are candidate retrieval, never evidence. Restated and sharpened in §3. | v5 |
| **No public transparency log by default** | Publishing a digest proves possession at a time, which is disclosive. Opt-in per workspace. | v5 |
| **No autonomous source approval** | A discovered source is `candidate`, never `approved`, until a human approves it. An automated approver is an unbounded prompt-injection surface. | v5 |
| **No automatic legal or medical adjudication** | The system extracts obligations and flags unsupported claims. It does not produce a compliance verdict. | v5 |
| **No claim of invention over prior art** | v6 combines existing ideas; the ideas have names and owners and are listed. | v5 |

Three of these acquire new machinery in v6 and are therefore restated in full below rather than by reference: source generation becomes §5, the vector-database refusal becomes §3, and the hosted-account refusal becomes §6. The restatement is not a softening. In each case v6 opens a *new* route to the same failure, and a refusal that names only the old route is one the new route walks around.

---

## New in v6

### 2. No universal truth score

**The refusal.** There is no number that says how true a document is, how reliable a workspace is, how trustworthy a claim is, or how confident the system is in any of it. Not on a dashboard, not in a capsule, not in an API response, not as an optional field.

**Why it is tempting.** v6 has more countable things than any previous version — nodes, obligations, constraints, branches, proofs, conflicts, grants. Every one of them is a number, and a system holding that many numbers is one aggregation away from a single figure that fits on a slide. The request always arrives with a legitimate need behind it: a director has eleven grant narratives and four hours, and wants to know which one to read first. That need is real.

**What the system does instead.** It answers the question the number was standing in for, which is always a different and better question. Not *how good is this* but *what is outstanding, of what population, at what basis*:

```
draft.md @ state sha256:71b4e8…

  blocking            2 of 41 claim atoms
                      c0004  citation does not resolve to a supplied source
                      c0019  scope widened without a supporting anchor
  holding             3 of 41
  obligations unmet   1 of 7   O-3  "quarterly report" has no discharge record
  conflicts open      0
  decisions missing   1        the merge at m-0117 carries no decision
  proofs stale        6 of 38  needs_assessment.txt moved; run `wi impact`
```

Six numbers, every one with a denominator, every one resolvable to the exact set it counts. A director reading that knows which document to open and why. A director reading `Trust: 82/100` knows nothing, including whether the two blocking items are typographical or fatal.

**The structural reason, not the aesthetic one.** A single score must combine the four reliability bases, and combining them destroys the only information they carry. Once a string comparison, a benchmark measurement, a model opinion and an author assertion are one number, nobody — including the person who computed it — can decompose it. See [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md) §2.

---

### 3. No RAG as proof

**The refusal.** Retrieval finds candidates. It does not prove support. No record typed `Verified` may cite a similarity value, a retrieval rank or an embedding distance as its basis, and no such value may be rendered as a confidence, a coverage figure or a support strength.

**Why it is tempting.** Retrieval works, visibly and immediately. It finds the right passage most of the time, it scales over a corpus no human will read, and the score it returns is a number between zero and one that looks exactly like a confidence. The pipeline that ends at the retrieval score is dramatically cheaper than the pipeline that continues past it, and it produces an output nobody can immediately tell apart from the expensive one.

**What the system does instead.** Retrieval occupies exactly one row of the pipeline and its score does not propagate past that row:

```
retrieval (embedding / BM25)   find plausible passages, fast, over a large corpus
        ↓                      output: candidates, ranked. Not evidence.
candidate anchor               a proposed pointer into a specific source version
        ↓                      output: a hypothesis to be tested
exact locator                  byte offsets · page + bbox · sheet + range · time interval
        ↓                      output: a resolvable, inspectable location
deterministic checks           exact string, numeric, date, citation resolution, digest match
        ↓                      output: Verified / failed. Support is decided here.
judgment, only if required     entailment and paraphrase, provider named, basis Judged
        ↓                      output: a reasoned opinion, never a verification
proof record                   typed, dependency-bound, invalidated under Law I
```

**Right:**

```
candidate  c0002  →  needs_assessment.txt @ bytes 4102–4260   (retrieval rank 1 of 8)
  status: unverified. Retrieval proposed this passage; nothing has checked it.
  next:   `wi anchor` to bind, then run the deterministic set.
```

**Wrong:**

```
c0002 — supported (similarity 0.94)
```

**Why the failure is directional and not merely weak.** Embedding proximity measures distributional similarity, which is not entailment and is frequently its opposite. "The program served 12,400 households" and "the program served 11,800 households" are neighbors in embedding space and are a career-ending difference in a grant narrative. Negation barely moves a vector. Attribution swaps barely move a vector. Date shifts barely move a vector. Every failure this system exists to catch is a small distance in exactly the space a similarity search is scoring — which makes similarity not a weak proxy for support but a proxy that is **blind in the specific direction of the risk**.

---

### 4. No model as sovereign author

**The refusal.** A model may propose. It may never decide, approve, delegate, merge, seal, revoke or sign. There is no record shape in v6 in which a `judgment_provider` appears as the actor on a decision, a grant, a merge resolution, a capsule seal or an acceptance — not as a configuration, not with an operator's consent, not under an autonomy setting.

**Why it is tempting.** This is the single most requested crossing, it arrives from the most sympathetic direction, and the argument is good: the model is right most of the time, the human is a bottleneck, and the changes waiting for approval are overwhelmingly trivial. A person approving four hundred `wording_only` proposals is not exercising judgment; they are clicking, and clicking teaches them to click.

**What the system does instead.** It makes the *rule* approvable rather than the model. A project may declare that a class of change accepts without a person present, and the acting party is recorded as `automated_policy` — a real actor with real authority that is honestly not a human:

```yaml
# .wi/policy.yaml
auto_accept:
  - delta_class: wording_only
    scope: "docs/**"
    requires:
      proof_impact: none        # no existing proof is invalidated
      realm_unchanged: true
      conflicts: 0
    actor: automated_policy
    review: quarterly           # the rule is re-approved, not the changes
```

The person approves the rule, once, with its conditions visible. Four hundred changes then proceed under it and every one names the rule that permitted it. That is the legitimate need met — and the record still answers *who approved this line*, because `automated_policy` is a truthful answer and "the model decided" is not an answer at all.

**Why the line does not move under autonomy.** [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) grants agents real latitude: an agent may plan, retrieve, atomize, anchor, run checks, compute impact, draft proposals and open branches without asking. What it may never do is take the decision. The distinction is not about capability or trust; it is that a decision record's entire value is the identity attached to it, and an identity that can be created by the component with the most output is not an identity. See [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) §5.

---

### 5. No silent citation generation

**The refusal.** The system will not construct a citation, ever. It will not repair a broken one by guessing what it meant. It will not fill a `needs_source` from a model's recollection. It will not upgrade a candidate to an anchor because the passage looked right.

**Why it is tempting in v6 specifically.** v5 refused this at one boundary: a generator asked for a reference. v6 opens four more, and each is a place where the fabrication does not look like fabrication:

| New route | How it arrives |
|---|---|
| **Obligation discharge** | An obligation needs evidence; the planner has a retrieval hit; discharging it automatically closes the item and clears the board |
| **Merge repair** | A merge leaves an anchor pointing into a span that no longer exists; re-anchoring to "the equivalent passage" resolves the conflict |
| **Federation** | A peer's record cites a source this workspace does not hold; synthesizing a local anchor makes the import clean |
| **Migration** | v5 anchors are byte offsets; a v6 migration that recomputes an offset against changed bytes is inventing a location |

**What the system does instead.** In all four cases, the honest outcome and the visible gap:

- An obligation with no evidence stays `unmet` and names what evidence would discharge it.
- A merge whose anchor no longer resolves produces `WI_ANCHOR_UNRESOLVED` and a conflict, not a new anchor.
- A federated record whose source is absent imports as a chain of custody, explicitly not as evidence.
- A migration that cannot preserve a location preserves the *claim* and marks the anchor unresolved, so the human re-anchors it. [`MIGRATION_V5_TO_V6.md`](MIGRATION_V5_TO_V6.md) treats a silently recomputed offset as a migration defect.

**Why a fabricated citation is uniquely destructive.** It is self-concealing. It looks exactly like a real one, it survives casual review, and it is usually found by the one reader who was going to decide something. Every other error in this system announces itself eventually; this one is discovered by the person you least wanted to discover it.

---

### 6. No cloud dependency in the constitutional path

**The refusal.** No constitutional guarantee requires a network, an account, a subscription, a registry or a running service. The path from *a source arrived* to *a stranger verified the capsule offline* contains no remote call, on any surface, under any configuration.

**Why it is tempting in v6.** v5 was one file and the refusal cost nothing. v6 has packs, federation, judgment providers and a registry, and every one of them is naturally hosted. A registry that resolves packs, a service that runs constraints, a coordinator that arbitrates merges — each is easier to build hosted and each would work well.

**What the system does instead.** It draws the line at the constitutional path and lets the conveniences sit outside it:

| Inside — never requires a network | Outside — may be hosted, never required |
|---|---|
| Canonicalization, digests, state identity | Pack registry (packs resolve from a local lock and a local cache) |
| Ingestion, quarantine, anchoring, deterministic checks | Judgment providers (absent means `Judged` results are unavailable, not guessed) |
| Branch, commit, merge, conflict preservation | Federation peers (absent means no imports, not a broken workspace) |
| Authority resolution, delegation, revocation | Transparency logs and timestamping |
| Proposals, decisions, obligations, constraints | Telemetry, webhooks, collaboration |
| Simulation, impact, semantic diff, `as-of` | Hosted Workbench sessions |
| Capsule build, seal, verify | Remote signing, if a local signer exists as an alternative |

**The test that keeps it honest.** A workspace with every hosted component removed still ingests, checks, branches, decides, seals and verifies. If a feature cannot be described that way, it does not go inside the line. The reason is unchanged from v5 and has only become more concrete: the documents that most need this system are the ones that cannot leave the building — sealed bids, pre-publication investigations, patient material, privileged work — and a company between an author and their own evidence is a company that can be acquired, change terms, deprecate an endpoint or close.

---

### 7. No blockchain

**The refusal.** No distributed ledger in the core, and no ledger operation required for any guarantee.

**Why it is tempting.** v6 seals capsules and signs manifests. It has digests, closures, revocation and a real need for third-party attestation. The vocabulary overlaps almost completely, and the request — *prove this existed before that date* — is legitimate.

**What the system does instead.** It produces the digest and stops there. A capsule digest is an ordinary hash; any timestamping authority, notary, ledger or witness an organization already trusts can attest to it, and the core neither knows nor cares which. The seam is deliberate: attestation is somebody else's business and should be replaceable in an afternoon.

**Why the core does not absorb it.** Every hard problem in this system is semantic — does the source support the claim, did the rewrite move the meaning, who approved it, which obligations are unmet, what does a merge do to a proof. A ledger addresses ordering and tamper-evidence, which were the tractable parts, solved by a hash and a signature. Adopting it as the core would import a network dependency, a cost model and an operational surface into a system whose central promise is that it runs offline, and would buy none of the guarantees anybody wanted. Tamper-evidence answers *was this changed*. This project answers *is this supported*, and a perfectly preserved record of an unsupported claim is still an unsupported claim.

---

### 8. No global ontology monopoly

**The refusal.** v6 does not ship a canonical vocabulary of the world, does not require projects to map their terms onto one, and does not treat concept identity as global. A concept is identified within a workspace. Federation aligns concepts explicitly, with the alignment recorded as a decision by a named actor.

**Why it is tempting.** Federation is much easier if everyone means the same thing by `household`. A shared ontology makes cross-workspace queries work immediately, makes imports clean, and makes obligations comparable across organizations. The pull is strongest precisely where the value looks highest.

**What the system does instead.** Alignment is an explicit, recorded, contestable act:

```json
{
  "kind": "concept.alignment",
  "local":  {"id": "cn-household", "definition_state": "sha256:4a1c…"},
  "remote": {"peer": "county-health", "id": "cn-household-unit",
             "definition_state": "sha256:9e07…"},
  "relation": "narrower_than",
  "note": "Their unit counts a shared kitchen as one household; ours does not.",
  "actor": {"type": "team_member", "id": "a.rivera"},
  "decided_at": "2026-08-04T15:22:09Z"
}
```

Four properties, each of which the global-ontology design loses: the alignment is `narrower_than` rather than `same_as`, so the difference survives; the note records what the difference *is*; a named human owns it; and it binds the definition states, so a change to either definition raises the alignment for review rather than silently invalidating every query that crossed it.

**Why a shared vocabulary is the wrong shape for this problem.** The words that matter most are the ones organizations define differently on purpose, because the definition is where the policy lives. A county's `household`, a funder's `served`, a regulator's `material` and a publisher's `sourced` are not imprecise versions of a true meaning; they are decisions. A system that harmonized them would erase the disagreements it exists to surface, and it would do so at exactly the moment two organizations were about to rely on each other's numbers.

---

### 9. No "overall health" gauge

**The refusal.** No single indicator summarizes a document, a workspace, a branch or a project. No green/amber/red pill, no percentage healthy, no letter grade, no gauge.

**Why it is tempting.** It is the most reasonable request in this document. A workspace with two hundred documents needs an entry point, and a person opening the Workbench needs to know where to look. Every product with a dashboard has this control, and its absence reads as a missing feature rather than as a refusal.

**What the system does instead.** It sorts by consequence, and it puts the population beside the count:

```
Needs a person now                                    3 documents
  narrative.md          2 blocking · 1 unmet obligation · merged change with no decision
  budget-note.md        1 blocking (unit mismatch: percentage vs percentage points)
  appendix-c.md         4 proofs stale since needs_assessment.txt moved

Waiting on someone else                               2 documents
Proceeding                                           14 documents
Nothing changed since last review                   181 documents
```

Same entry point, same glance, and the reader learns which three and why. `Health: 94%` is the same information destroyed.

**The specific failure a gauge causes.** It survives its own inputs. A gauge is computed once, screenshotted, pasted into a status deck and read three weeks later, at which point every number under it has moved and nothing about the image says so. This is the green-badge problem at the level of a whole workspace: an artifact that carries confidence forward across exactly the changes it should have been invalidated by. [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md) §5 treats it as a rendering hazard; it is listed here because the correct fix is not to render it more carefully.

---

### 10. No hidden auto-merge of consequential state

**The refusal.** A merge never silently resolves a semantic conflict. Two changes combine automatically only when each is `wording_only` relative to the common ancestor and they touch disjoint nodes. Everything else is preserved as a conflict, and there is no strategy option that widens this.

**Why it is tempting.** Conflicts are friction and version control has spent forty years reducing it. "Ours", "theirs", "newest wins", "prefer the longer text" and "prefer the branch with more approvals" are all reasonable-sounding, all trivially implementable, and all things an operator will ask for by the second week.

**What the system does instead.** It records both sides and names what is in dispute:

```
$ python3 scripts/wi.py conflicts

2 unresolved semantic conflicts on branch `release/q3`

  m-0117  scope
    ours    "across the seven pilot counties"
    theirs  "statewide"
    ancestor "across the seven pilot counties"
    → proofs affected: c0002, c0009, c0031 (3 of 41)
    → no decision binds the merged state

  m-0118  obligation
    ours    "the grantee shall report quarterly"
    theirs  "the grantee may report quarterly"
    ancestor "the grantee shall report quarterly"
    → legal_force changed; O-3 discharge schedule depends on this
```

**Why "ours/theirs" is not a strategy but a policy about whose assertion becomes true.** In source code an automatic merge is checked downstream by a compiler and a test suite, which object. In meaning there is nothing downstream that objects. A scope that silently widened, an obligation that silently softened and a figure that silently changed all produce a document that reads well and is wrong, and the change is invisible in a character diff because it is small. The friction is the feature: the two lines above are the two decisions a person has to make, surfaced at the moment they are cheap.

---

### 11. No ambient plugin power

**The refusal.** A plugin has no capability it did not declare and was not granted. No ambient filesystem, no ambient network, no access to the graph beyond the subgraph it declared, no write path to any node, and no ability to loosen a hard invariant.

**Why it is tempting.** Declared capabilities are tedious. A plugin author who needs one more node type has to change a declaration and an operator has to re-grant, and the obvious relief is a broad grant given once. Every plugin system in history has taken this path, usually with a permission called something like `full` that exists for the two plugins that genuinely needed it and is then requested by all of them.

**What the system does instead.** Effects and subgraphs are declared, granted, printed and enforced out of process:

```yaml
# pack.yaml
name: grant-narrative
version: 1.4.0
effects: []                    # no network, no filesystem, nothing ambient
reads:
  - node: meaning.claim_atom
    where: {realm: external_fact}
  - node: source.version
    fields: [digest, mime, ingested_at]
emits: [finding]               # findings only — never a verdict, never a node
tightens:
  - constraint: C014           # every funding figure carries a period
severity_raises: [C007]
```

**Two properties that are easy to lose and are the whole design.** A plugin emits **findings**, never verdicts — the core decides what a finding means under the resolved policy, because a plugin that returns a verdict is the policy engine. And permission is **one-directional**: a plugin may add a constraint, raise a severity, narrow an evidence mode or forbid a construction, and may never widen `Verified`, downgrade a block to a hold, admit an unanchored claim or remove a required decision. A compromised plugin's maximum achievable outcome is a build stricter than intended. The alternative makes every plugin a full-trust component and the gate a suggestion.

---

### 12. No renderer-side facts

**The refusal.** A renderer displays state. It does not compute a fact, derive a status, infer a basis, resolve a conflict, aggregate a count or decide what a number means. Every value on every surface traces to a record the core produced.

**Why it is tempting.** It is almost always faster. The Workbench has the graph in memory; computing a coverage percentage in the UI is three lines and a round trip saved. A REST client has the claim list; counting the blocking ones locally is obviously correct. A browser build cannot reach the core for every value and has to hold *something*.

**What the system does instead.** The core emits result objects and every surface renders them. Where a surface cannot reach the core, it says so rather than computing a substitute:

```json
{
  "coverage": {
    "basis": "Measured",
    "numerator": 9,
    "denominator": 14,
    "population": "factual claim atoms in draft.md at state sha256:71b4e8…",
    "excluded": {"rhetorical": 3, "hypothetical": 2},
    "computed_by": "wi-core 6.0.0",
    "computed_at_state": "sha256:71b4e8…"
  }
}
```

The renderer prints `9 of 14`. It does not divide, does not round, does not colour by threshold and does not decide that five excluded atoms should have been in the denominator.

**Why this is Law K rather than a style rule.** The moment a surface computes a fact, there are two implementations of that fact and one is wrong. They will not disagree loudly. They will disagree on the fifth edge case, in the surface with fewer tests, on the document that mattered — because the UI counted a deferred proposal as open, or normalized whitespace differently, or included a realm the core excludes. A displayed number that the core never produced is unverifiable by definition: there is no record to point at when someone asks where it came from.

---

### 13. No history rewriting

**The refusal.** There is no `rebase`, no `squash`, no `amend`, no force push, no history edit and no administrative delete of a committed state. Corrections are appends. Retractions are events. Revocations are state changes. Nothing removes what happened.

**Why it is tempting.** The version-control vocabulary v6 borrows comes with these operations attached, and users will expect them. A messy branch is genuinely unpleasant to read. A decision taken in error looks, to the person who took it, like something that should be removable. A confidential fact ingested by mistake feels like something that must be removable.

**What the system does instead.**

| The need | The v6 answer |
|---|---|
| "This branch is messy" | Present a filtered view. The history is complete; the *reading* of it is configurable. Tidiness is a display concern and never a storage one. |
| "This decision was wrong" | Take a new decision. The record shows both, in order, with both actors. That sequence is the audit trail, and it is more informative than the corrected state alone. |
| "This was ingested by mistake" | A deletion event, recorded. The bytes go; the fact that a source existed, was ingested, and was deleted by a named actor at a named time remains. [`../v5/RIGHTS_AND_CONSENT.md`](../v5/RIGHTS_AND_CONSENT.md) treats deletion as an event for exactly this reason. |
| "A delegate acted and their grant is revoked" | Their actions stay, attributed, with the grant named. Revocation is forward-looking. |

**Why the refusal survives the confidentiality argument, which is the strongest one against it.** A record that can be rewritten is a record whose current contents depend on who has authority *today*, which destroys the property the whole system exists to provide: that a stranger can check what happened without trusting the party who is telling them. If history can be edited, every audit becomes an audit of the editing permissions, and the correct question stops being *what happened* and becomes *what does the current administrator want it to look like*. A deletion event answers the confidentiality need honestly — the material is gone, and the fact of its removal is not.

---

## 14. How to decline without being useless

**Status: specified.**

A refusal that stops at "no" has moved the problem to the author without moving it forward. Every non-goal above has a legitimate need behind it, and the need is usually serviceable by something adjacent. Three moves, in order: **name the line and why it exists**, in one sentence, without a lecture; **do the part that is legitimate**, without being asked twice; **say what would actually solve their problem**, including when the answer is a person rather than a tool.

| Request | What is declined | What is delivered instead |
|---|---|---|
| "Give me a trust score for this document." | The composite | The six-line outstanding-items block from §2, with denominators |
| "The retrieval found it — mark it supported." | Similarity as proof | The candidate anchor, bound and ready to check, with its rank shown as a rank |
| "Let the agent approve the trivial ones." | The model as decider | An `auto_accept` rule the human approves once, acting as `automated_policy` |
| "Just auto-merge; we can review later." | Silent semantic resolution | The conflict list with the affected proofs, which is the review, arriving earlier |
| "Give the pack full access, it is our own pack." | Ambient power | The declared subgraph it actually reads, printed, and a grant that takes one command |
| "Squash this branch before the audit." | History rewriting | A filtered view for reading, and the complete history for the audit |
| "Can the dashboard show one health number?" | The gauge | The consequence-sorted list, which answers the same question and survives being screenshotted |
| "Align our concepts with theirs automatically." | A global ontology | An explicit alignment record with the relation and the difference named |

**Why the pattern is load-bearing.** A refusal delivered badly gets routed around. The author goes to a tool with no refusals at all, and the line held here protects nobody. The objective is not purity; it is that the person leaves with the legitimate part of their need met and an accurate picture of what nothing can do for them.

---

## 15. What a non-goal is not

A non-goal is not a technical limitation, and the two must never be reported in the same words. A limitation says *not yet*. A refusal says *not ever*, and gives the reason.

| | Limitation | Non-goal |
|---|---|---|
| Example | Entailment is not checked — no judgment provider is configured | Citations will never be constructed |
| Example | PDF regions cannot be anchored on this build | A model will never sign a decision |
| Changes with | Time, work, a release | Nothing |
| Correct phrasing | "Not run — no judgment provider on this surface" | "This system does not do that, because —" |
| Where it lives | [`BUILD_MANIFEST.md`](BUILD_MANIFEST.md), [`../../ROADMAP.md`](../../ROADMAP.md), the disclosure block | This document |

Conflating them corrodes both. A limitation described as a refusal is an excuse. A refusal described as a limitation is a promise to cross the line later, and everyone who reads it will plan on that.

---

**These are refusals, not unbuilt features. They do not move.**

A refusal has no roadmap entry, no target release, no "planned for a future version" note and no conditions under which it is revisited. If a document, a deck, a README, a release note, an issue reply or a sales conversation implies that any line above is a gap awaiting work, **that document is a defect and should be corrected on sight** — with the same urgency as a code path that emitted `Verified` over something unverified, because it is the same failure: a claim made in a register that discourages checking.

---

Read next:

- [`CONSTITUTION.md`](CONSTITUTION.md) — the laws these refusals protect
- [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md) — why a basis cannot be coerced and a gauge cannot be rendered safely
- [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) — what an agent may do, and the line at §4
- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — conflict preservation as specified
- [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) — declared effects and the plugin host
- [`SECURITY_MODEL.md`](SECURITY_MODEL.md) — the threats these refusals close
- [`../v5/NON_GOALS.md`](../v5/NON_GOALS.md) · [`../v4/NON_GOALS.md`](../v4/NON_GOALS.md) — the originals
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
