# v6 Constitution

The constitutional layer of Writing Intelligence v6.0 — the Sovereign Meaning Runtime.

v3 governs *how well* the writing is built. v4 governs *what may be claimed about it*. v5 governs *what a finished document can prove about itself to a reader who does not trust the author, the tools, or the model that helped*. v6 governs *how a body of meaning changes over time when more than one person, process and machine is allowed to change it* — and refuses to let a state become authoritative without an identifiable prior state, an identified actor, and a computable consequence.

This document is the highest authority in the repository. Where any other document, schema, adapter, wrapper or surface disagrees with it, this document wins and the other document is a defect.

Created by **[Antonio T. Smith Jr.](https://densitysix.com)** — Founder & CEO, Density6 LLC.

---

## Table of contents

1. How to read this document
2. The v4 laws — A through F, in force unamended
3. The v5 laws — G through L, in force unamended
4. The six v6 system laws — M through R
5. The v6 law
6. The twelve-layer runtime
7. The actor model, extended
8. The v6 failure codes
9. What v6 does not change
10. Amendment
11. What a v6 release promises

---

## 1. How to read this document

Every law has three parts: the law itself, why it is load-bearing, and what it requires mechanically. The law is the rule. The reasoning is why the rule survives contact with someone who wants to break it. The mechanical requirement is what an implementation must actually do, so that a future implementer cannot satisfy the law by agreeing with it.

Every section that describes a **mechanism** carries a status marker on its first line. There are exactly two:

| Marker | Meaning |
|---|---|
| **Status: executable in `scripts/wi.py`.** | The mechanism runs today, offline, on stdlib-only Python 3.8+. You can execute it and read its output. |
| **Status: specified.** | The mechanism is designed and normatively described. It does not run yet. Nothing in this repository executes it. |

The marker is not a formality. Law C — *never report work not done* — is the constitutional root of this project, and a specification document that reads like a feature list is the exact failure the project exists to catch, one level up. A reader must be able to tell, per section and without a changelog, whether they are reading about a thing that runs or a thing that is written down.

### 1.1 What executes at v6.0

The canonical deterministic core of v6.0 is `scripts/wi.py`. It is a single stdlib-only Python file. The v6 commands it executes are exactly these and no others:

| Command | What it does |
|---|---|
| `wi canon <path>` | Canonical JSON and a domain-separated state digest for a state document |
| `wi branch create \| list \| switch \| delete` | Named movable pointers into the immutable object store |
| `wi commit` | A semantic commit: graph root, delta, actor, optional decision reference |
| `wi log` | Semantic commit history |
| `wi propose` | A proposal bound to an exact target state digest |
| `wi proposals` | Proposals and their status |
| `wi simulate` | Counterfactual evaluation: candidate root, semantic deltas, stale frontier, provably-unaffected count, conflicts, repair plan — mutating nothing |
| `wi decide` | An authorized decision; refuses on a stale target binding |
| `wi merge` | Conflict-preserving semantic three-way merge |
| `wi conflicts` | Unresolved semantic conflicts |
| `wi authority` | Issue, delegate, revoke and check capability grants |
| `wi obligations` | Proof obligations derived from typed state, release target and policy |
| `wi as-of` | Bitemporal query by `--valid-at` and `--known-at` |
| `wi constraints` | The graph constraint engine, C001 through C020 |
| `wi capsule create \| inspect \| verify` | Merkle proof closure, selective disclosure, inclusion proofs |
| `wi why` | Explain a node backward to its basis |

The v5 commands remain executable and unchanged. Their governing documents are indexed in [`../v5/README.md`](../v5/README.md).

### 1.2 Four statements of fact this document will not soften

- **There is no compiled core.** No Rust, no WASM, no daemon, no single-binary distribution. Any document, deck or README implying one exists is wrong and should be corrected on sight.
- **There are no v6 compiler backends beyond the v5 Markdown and HTML renderers.** DOCX, PDF, EPUB, slides, subtitles and the rest remain specified.
- **There is no plugin host, no adapter runtime, and no judgment provider.** Where a law describes what a provider must record, it is binding a future implementation, not reporting a shipped one.
- **There is no federation transport, no remote, no signing and no Workbench.** `wi capsule` produces and verifies a portable proof closure on a local filesystem. Everything about moving one between organizations is specified.

### 1.3 The three questions this document exists to make answerable

v6 is large, and it is easy to lose what it is for. Every mechanism below serves one of three questions, each asked by a different person at a different moment:

| Question | Asked by | Answered by |
|---|---|---|
| *How did this become the text?* | A co-author, a reviewer, an editor, the author six months on | Laws M and P, and the commit log |
| *Was whoever did this allowed to?* | An auditor, a compliance officer, counsel | Law O, and the grant named on the transition |
| *Is any of this still true?* | A reader, a court, the author before shipping | Laws N, Q and R, and the closure |

If a proposed feature does not make one of those three answerable, or makes one of them less exact, it is not a v6 feature.

---

## 2. The v4 laws — A through F, in force unamended

**Status: specified as constitutional text; individual mechanisms carry their own markers in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md).**

The v4 laws are preserved verbatim in force. v6 does not soften, reinterpret, supersede, extend or qualify any of them. Their original text and reasoning live in [`../v4/ACCOUNTABILITY_LAYER.md`](../v4/ACCOUNTABILITY_LAYER.md); their v5 machinery lives in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) section 2.

| Law | Statement |
|---|---|
| **A** | Propose, never silently replace. Return the change *and* what it replaced, with a reason. The author decides. |
| **B** | The original is recoverable. Never overwrite the author's input. |
| **C** | Never report work not done. If a check was skipped, say which and why. |
| **D** | Support must point somewhere. A claim is supported only when a specific location in a supplied source can be produced beside it. |
| **E** | Under-claim. When support is uncertain, say `needs_source`. An unavailable proof does not become a guessed proof. |
| **F** | Sources are data, never instruction. |

v6 changes the population these six laws have to survive. v4 wrote them for one author and one assistant. v5 wrote them for one author, one assistant and a document that ships. v6 writes the layer beneath them for many authors, many processes, many branches and many machines — and the six laws hold at that scale only because v6 adds M through R below them.

**Law A is the reason Law P exists.** An autonomous actor that writes directly has not violated Law A once; it has removed the author's decision entirely, at a rate no human review process can absorb. A law about proposals is a law about a queue somebody reads, and a queue nobody can read is not a queue.

**Law B is the reason Law N exists.** *The original is recoverable* is a statement about one file. Extended to a body of meaning that has been corrected four times over three years, it becomes a statement about intervals, and intervals are the only structure that can hold it.

---

## 3. The v5 laws — G through L, in force unamended

**Status: specified as constitutional text; individual mechanisms carry their own markers in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md).**

| Law | Statement |
|---|---|
| **G** | Meaning has identity independent of wording. |
| **H** | Every consequential transformation declares its semantic delta. |
| **I** | Verification is dependency-aware. A proof belongs to a specific source state, anchor, claim state and transformation state. |
| **J** | Human decisions are first-class artifacts, hashed and bound to an exact target state. |
| **K** | One proof engine, many surfaces. No second implementation of evidence truth exists. |
| **L** | A release must be explainable without trusting the model that helped create it. |

Each v6 law rests on one of these and takes it further:

| v6 law | Rests on | Takes it |
|---|---|---|
| **M** — the semantic state is canonical | G — meaning has identity | from *meaning has an identity* to *meaning is the only writable thing* |
| **N** — time is part of meaning | G and I | from *a state* to *a state that holds over an interval and was believed over an interval* |
| **O** — authority is explicit | J — decisions are artifacts | from *decisions are recorded* to *decisions require a grant that could have been absent* |
| **P** — autonomy produces proposals | A and J | from *one assistant proposes* to *any number of processes propose and none of them writes* |
| **Q** — disagreement is preserved | H and I | from *a change is classified* to *two incompatible changes are both kept* |
| **R** — freshness is a property of dependencies | I — verification is dependency-aware | from *a proof goes stale* to *nothing anywhere is fresh by assertion* |

---

## 4. The six v6 system laws — M through R

These are new in v6. They govern the runtime, not the graph.

---

### Law M — The semantic state is canonical; renderings are builds

**Status: specified.** `wi canon` computes the canonical serialization and domain-separated digest of a state document today. The renderer boundary and the round-trip proposal path that make a rendering unwritable are specified.

The authoritative work is the semantic state in the graph. Every document — Markdown, DOCX, PDF, deck, podcast script, subtitle track, API reference — is a build artifact produced from a named graph root by a named renderer under a named policy. **No rendering is an input to meaning.** An edit made inside a rendering is a proposal against the graph, never a change to it.

**Why it is load-bearing.**

v5 already said the document is a rendering and the graph is the system. It said so as an architectural preference and then left the draft file writable, because there was no other way to work. That leaves two sources of truth in the same workspace, and two sources of truth do not announce their divergence — they diverge quietly, on the day somebody opens the DOCX to fix a typo and fixes a number on the way past.

The failure has a shape worth naming exactly, because it is the most common way a governed document becomes ungoverned. Nobody decides to abandon the graph. Somebody is on a deadline, the graph is one step away, and the file is right there. The edit is small. It is also now the only place that content exists, and the graph's version of that paragraph is silently wrong — while every check the system runs still passes, because the checks run against the graph and the graph was not touched.

Making the rendering non-authoritative is the only version of this rule that survives a deadline. A rule that says *please edit in the graph* is obeyed until it is inconvenient. A rule that says *an edit in a rendering is a proposal, and the next build will overwrite it* is enforced by the build, and nobody has to be diligent.

**What it requires mechanically.**

1. Every rendering carries a `built_from` edge to an exact graph root digest, a renderer identity and version, and the policy digest in force at build time. A rendering with none of these is `WI_RENDERING_UNGOVERNED`, and no gate may treat it as an output of this system.
2. A build is a pure function of `(graph_root, renderer_id, renderer_version, policy_digest)`. Two builds from the same tuple produce byte-identical artifacts, or the renderer is defective.
3. An edit detected in a rendering is parsed back to a candidate semantic delta and emitted as a **reverse proposal** against the graph node it targets. It is never applied. Where the round-trip parser cannot map the edit to a semantic node, the proposal is emitted as `unmapped` with the raw before and after, and a human decides — the system does not guess a target.
4. A renderer may change expression and may not change a quantity, a scope, a modality, a hedge, a negation, a causal force, an enumerated exception or a legal force. Where a target constraint makes the semantically complete rendering impossible, the renderer raises a proposal and renders nothing. That is the v5 rule in [`../v5/SEMANTIC_IR.md`](../v5/SEMANTIC_IR.md) section 5.1, and v6 does not relax it.
5. The graph root, not the file tree, is what a release attests to. An attestation names a root digest; the artifacts are what that root compiled to.

**What the reverse proposal looks like.** An editor opens the built DOCX and changes one sentence. The round-trip parser maps the paragraph back to its claim atom and reports what the edit did to meaning, rather than what it did to characters:

```
$ python3 scripts/wi.py propose --from-rendering dist/narrative.docx

dist/narrative.docx  built_from root sha256:8c31…07a4  ·  renderer docx@0  (specified)
1 divergence from the built artifact.

PROPOSAL pr-0341  ·  reverse proposal from a rendering
  target    c-0002 @ sha256:9f2c1d47…      (current)
  before    "Between 2019 and 2022, the program served 11,800 households."
  after     "Since 2019 the program has served nearly 12,000 households."
  delta     quantity   11800 → ~12000        consequential
            time       closed_range → open   consequential
            certainty  asserted → asserted   unchanged
  effect    2 deterministic checks against anchor a-0114 would fail
  status    open — no decision

Nothing applied. The graph is unchanged. Next build will overwrite this file.
```

The last line is the enforcement. The editor is not being scolded; they are being told, before they invest in a second edit, which direction the data flows.

---

### Law N — Time is part of meaning

**Status: `wi as-of` executable in `scripts/wi.py`; interval arithmetic on contradiction detection specified.**

Every consequential state carries two intervals: **valid time** — the period during which the asserted thing holds in the world — and **knowledge time** — the period during which this system held this state as its belief. Neither may be inferred from the other. Neither may be dropped by a renderer. A claim with no declared temporal frame is under-specified, not timeless.

**Why it is load-bearing.**

Consequential documents are written about a world that revises itself. An agency publishes a figure, then republishes it. A partner corrects a count. A regulation takes effect on a date that is not the date it was signed. Every one of those is normal, and every one destroys an overwrite-based system, because overwriting answers the wrong question.

Two different people ask two different questions about the same number, and only a bitemporal record answers both:

| Who asks | What they ask | Answered by |
|---|---|---|
| A reader, a court, an analyst | *What do we now believe was true in 2026?* | valid time |
| An auditor, a reviewer, the author's own defence | *What did we know when we filed this in March 2027?* | knowledge time |

An overwrite answers the first and destroys the second. A change log answers the second badly and the first not at all. Only two independent intervals answer both — and once they are independent, a third thing becomes possible that is worth more than either: **contradiction detection stops producing false alarms.**

That is the practical argument. A corporate tax rate of 21% through 2028 and 24% from 2029 are not a contradiction; they are a schedule. A system that flags them is a system whose contradiction report is noise, and a noisy report is one that gets switched off — taking the real contradictions with it. Interval intersection is what separates a schedule from a conflict, and without valid time there is no interval to intersect.

**What it requires mechanically.**

1. Intervals are half-open, `[from, until)`. An unbounded end is `null` and means *open*, never *forever* — the distinction matters when two open intervals meet, which is exactly the case that is a genuine contradiction.
2. A correction **appends**. It closes the prior state's knowledge interval at the moment the correction was learned and opens a new one. It never rewrites a stored state, and it never deletes one.
3. A contradiction between two states of the same logical node requires their valid intervals to intersect **and** their knowledge intervals to intersect. Where either fails to intersect, the states are a sequence, not a conflict, and the system says so rather than staying silent.
4. `wi as-of --valid-at D --known-at K` reconstructs the state the system held at knowledge time `K` about valid time `D`. Both default to now; neither may be inferred from the other; and a query supplying only one gets the other's default stated in the output rather than silently applied.
5. A release records the knowledge time it was built at. *This document was correct on what we knew on 14 March 2027* is a checkable statement. *This document is correct* is not.

Full treatment, including the worked revision case and the archival-versus-overwrite argument: [`BITEMPORAL_STATE.md`](BITEMPORAL_STATE.md).

---

### Law O — Authority is explicit, scoped and expiring

**Status: `wi authority` executable in `scripts/wi.py`.**

No actor holds authority by virtue of what it is. Not by being the owner, not by being a person, not by having created the workspace, not by holding the filesystem. Authority is a **capability grant**: a named capability, a bounded scope, an issuer, a subject, a validity interval and an optional condition set. It expires. It can be revoked. A delegated grant may never exceed its parent in capability, in scope or in lifetime.

**Why it is load-bearing.**

The v5 actor model answered *who did this*. It did not answer *were they allowed to*, and in a single-author workspace those questions collapse, which is why v5 could leave it. They stop collapsing the moment a second identity exists — a co-author, a reviewer, a CI job, a scheduled task, an agent — and the gap between them is where every real governance failure lives. Nobody is surprised to learn who made a change. They are surprised to learn that person could.

Ambient authority is invisible until it is misused, and then it is unbounded. *The author can do anything* is not a policy anyone chose; it is the absence of one, and it is indistinguishable from a policy until the day it matters. Every other control in this system — the proposal, the decision record, the gate, the attestation — is decorative if any actor can perform any transition on any node whenever it holds the file.

Expiry is the part people want to drop and the part that pays for itself. A grant that expires converts *we forgot to revoke access* from a permanent hole into a bounded one, without anyone having to remember. The reviewer who helped for two weeks in March does not still hold acceptance authority in November — not because someone was diligent, but because the grant said `not_after`.

**A grant, in full.**

```json
{
  "node_type": "authority.grant",
  "logical_id": "0193a7c2-11b4-7d3e-8f02-6a1c4e9b0d55",
  "state_digest": "sha256:2b91f0ac47d3e5860c1b9a4f7e206d38ca5f1904b7e2c8d0f3a6b9c1d4e7f205",
  "capability": "claim.accept.wording_only",
  "subject": {"actor_id": "act-0007", "actor_kind": "team_member"},
  "issuer":  {"actor_id": "act-0001", "actor_kind": "human"},
  "scope": {
    "kind": "structure_subtree",
    "root": "structure.chapter:ch-02",
    "realms": ["external_fact"],
    "branch": "main"
  },
  "not_before": "2027-03-01T00:00:00Z",
  "not_after":  "2027-03-15T00:00:00Z",
  "conditions": [
    {"kind": "requires_no_open_conflicts", "value": true},
    {"kind": "max_quantity_delta_bps", "value": 0}
  ],
  "delegable": false,
  "parent_grant": null,
  "revoked_at": null
}
```

Read the capability carefully. It is not `claim.accept`. A reviewer brought in to tighten prose in one chapter for two weeks holds the authority to accept a wording change and does not hold the authority to accept a change to a number — and the grant says so in a field, not in an onboarding email.

**What it requires mechanically.**

1. A grant is a first-class node with a state digest, exactly like a claim. It is issued, recorded, and checkable after the fact.
2. Every authoritative transition names the grant that permitted it. A transition with no valid grant at its moment of application is `WI_AUTHORITY_ABSENT` and does not apply. Absence of a grant is a refusal, never a default-allow.
3. Delegation is monotone. `child.capabilities ⊆ parent.capabilities`, `child.scope ⊆ parent.scope`, `child.validity ⊆ parent.validity`. A delegation that widens any of the three is refused at issue time, not detected at use time.
4. Revocation is effective from its recorded instant and does not rewrite history. Decisions taken under a grant while it was valid remain valid decisions; the revocation is a fact with its own knowledge interval.
5. **A judgment provider is categorically denied write and decision capability.** Not by policy, not by configuration, not by default — by constitutional constraint, checked at issue time. A grant naming a `judgment_provider` subject together with any of `claim.accept`, `canon.modify`, `proof.waive`, `release.approve`, `release.sign` or `authority.delegate` is refused. There is no flag that permits it and no phrasing of a request that produces it.
6. Actor kind is descriptive. It narrows what may be granted; it never grants. A human with no grant cannot commit.

Full treatment, including the capability vocabulary and the delegation validator: [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md).

---

### Law P — Autonomy produces replayable proposals, not invisible mutations

**Status: `wi propose`, `wi proposals`, `wi simulate` and `wi decide` executable in `scripts/wi.py`; the agent runtime that would call them is specified.**

An autonomous actor may read the graph, compute over it, simulate against it and emit proposals. **It may not write an authoritative state.** Every autonomous act is recorded with enough for a stranger to replay it: its inputs by digest, the policy it ran under by digest, the proposal it produced, and the decision the proposal is waiting on.

**Why it is load-bearing.**

Law A was written for one model helping one author, where the author reads every proposal because there are eleven of them. That premise does not hold at v6 scale. A system with autonomous actors produces changes faster than any human can review after the fact, which means review happens before application or it does not happen at all. The distinction between *the author approved this* and *the author did not object to this* survives only if application is a separate, authorized act.

The failure mode is not a rogue agent. It is an ordinary, well-behaved, useful agent that fixes four hundred small things correctly and one thing wrongly, and by the time anyone notices, the wrong one has three hundred commits on top of it and no record of why it was made. Attribution after the fact is not attribution; it is archaeology.

Replayability is the second half, and it is what makes an autonomous change contestable. A proposal that cannot be reproduced from its recorded inputs is an assertion. A proposal that can be — same inputs, same policy, same output — is a computation somebody can disagree with on the merits.

**What it requires mechanically.**

1. `wi propose` is the only entry point an autonomous actor has to the graph. There is no code path by which an actor of kind `automated_policy`, `judgment_provider` or any future agent kind produces an authoritative state.
2. Every proposal binds to an exact target state digest. When the target moves, the proposal is `WI_PROPOSAL_STALE` — it does not re-attach to the new state, because a proposal computed against one state is not evidence about a different one.
3. Every proposal carries `produced_by`: the actor, the actor kind, the digest of every input it read, the policy digest it ran under, and — where a judgment was involved — the full judgment record from [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md).
4. `wi simulate` exists so an actor can evaluate a candidate without touching anything. It mutates nothing, writes nothing, and its output is a report: the candidate root, the semantic deltas, the stale frontier, the provably-unaffected count, the conflicts and a repair plan.
5. A decision is a separate act by an actor holding the relevant grant. Acceptance and application are two events, and the system never collapses them — see [`SEMANTIC_VERSION_CONTROL.md`](SEMANTIC_VERSION_CONTROL.md) section 7 for why an `Applied` status does not exist.
6. Batch acceptance is permitted and is shown as a batch. An operator accepting sixty proposals in one act has taken one decision over sixty targets, and the record says so rather than manufacturing sixty independent approvals.

**Simulation, which is the shape of a bounded autonomous act.**

```
$ python3 scripts/wi.py simulate --proposal pr-0341

Candidate root  sha256:d4f0…22ce   (not written)

Semantic deltas               2 consequential, 0 wording_only
  c-0002  quantity  11800 → 12000        consequential
  c-0002  time      closed_range → open  consequential

Stale frontier                4 nodes
  a-0114   anchor into needs_assessment.txt@v2   WI_ANCHOR_STALE
  c-0002   claim atom loses support               WI_CLAIM_UNSUPPORTED
  p-0031   paragraph asserting c-0002             WI_REVIEW_REQUIRED
  slide-07 rendering of c-0002                    WI_REVIEW_REQUIRED

Provably unaffected           1,914 nodes
  basis: no anchor outside bytes 8,912–9,144 intersects the changed region

Conflicts                     0
Repair plan                   re-anchor c-0002 against @v3, or restate the
                              closed period in the sentence

Nothing written. 0 states changed.
```

The provably-unaffected line is not a courtesy. It is what stops the report being a wall of red, and a report that is a wall of red is a report an author stops reading — at which point the mechanism has cost more than it returned.

---

### Law Q — Semantic disagreement is preserved until resolved

**Status: `wi merge` and `wi conflicts` executable in `scripts/wi.py`.**

When two branches, two sources, two authors or two knowledge intervals assert incompatible states of the same logical node, the system records a conflict and keeps **both** states. It does not pick. Not by recency, not by branch precedence, not by longest text, not by author seniority, not by a similarity score, and not by any rule that would let the merge complete without a human.

**Why it is load-bearing.**

Text merge tools resolve by position, and position is not meaning. Two people editing the same paragraph produce a textual conflict the tool cannot resolve, which is fine — it stops and asks. The dangerous case is the opposite one: two people editing *different* paragraphs that assert incompatible things. Every text merge tool in existence completes that merge cleanly, and the document that comes out contains a contradiction nobody introduced and nobody will find.

Last-writer-wins is the default when nobody chooses, and it is a correctness policy nobody would choose if asked. It means the person who pressed save second was right, about a question neither of them knew they were answering. Applied to a wording change, that is a nuisance. Applied to a quantity, a legal force, a scope or an obligation, it is how a document acquires a claim its authors would both reject.

The signal being destroyed is the valuable one. Two states of the same node, both supported, both defensible, held by two people who each had a reason — that is the single most informative thing a governed workspace can surface, and auto-resolution deletes it before anyone sees it. **A conflict is not a failure of the merge. It is the merge's most useful output.**

**What it requires mechanically.**

1. `wi merge` performs a three-way merge over **semantic deltas**, not text. Two changes to the same node that are `wording_only` and do not intersect on any semantic dimension are not a conflict, and the merge composes them.
2. Any intersection on a consequential dimension — quantity, scope, time, entity, attribution, certainty, causality, legal force, obligation, definition, canon — is a conflict. Both states are retained with their full provenance.
3. A conflict is a node with a state digest, a cause, the two competing states and an open status. It is not a message printed during a merge.
4. An unresolved conflict blocks release under policy. It does not block work, and it does not block the merge from completing on unaffected nodes — a merge that refuses everything because one node conflicts is a merge nobody runs.
5. Resolution is an authorized decision naming the surviving state, the rejected state and a reason. **The rejected state is retained.** *Somebody chose* is a different fact from *only one option existed*, and the record must be able to tell them apart years later.
6. There is no configuration option that enables automatic semantic resolution. Requests for one are refused on the grounds stated above, permanently.

**A merge that completes and still stops.**

```
$ python3 scripts/wi.py merge --into main --from review/counsel

base  sha256:8c31…07a4    main  sha256:a002…b71f    from  sha256:6e4d…9130

Composed cleanly                31 nodes
  27 wording_only · 4 disjoint semantic dimensions

Conflicts retained               1
  cf-0004  c-0117  legal_force
      main            "the grantee will provide quarterly reports"
                      legal_force = obligation      accepted d-0088
      review/counsel  "the grantee may provide quarterly reports"
                      legal_force = permission      accepted d-0091
      valid   both [2027-01-01, null)      intervals intersect
      known   both [2027-03-04, null)      intervals intersect

Merge committed. 1 conflict open. Gate consequence under `strict`: HOLD.
Resolve with: wi decide --conflict cf-0004 --keep <state> --reason "..."
```

Both people were right about their own job. Counsel weakened a binding commitment on purpose; the author strengthened it on purpose. No automatic rule produces the right answer here, and every automatic rule produces *an* answer.

---

### Law R — Freshness is a property of dependencies, not a green badge

**Status: `wi simulate` and `wi constraints` executable in `scripts/wi.py`; cached closure keys specified.**

No state is fresh because it was recently checked. A state is fresh if and only if every dependency in its proof closure is at the state it was checked against, and the system can name the ones that are not. Freshness is **computed**, per query, from the closure — and it is reported with the basis on which it was computed.

**Why it is load-bearing.**

A timestamp is not a dependency. *Verified three days ago* is a fact about a clock, and the reader hears it as a fact about the document. v5 removed that lie at claim level with the state-digest binding. v6 has to remove it everywhere else it reappears, because it reappears constantly: on a branch, on a release, on an imported capsule, on a dashboard, on a cached view, on a badge in a README.

The pressure toward a stored freshness flag is real and it comes from performance. Walking a closure costs something; a boolean column costs nothing. But a stored flag is a cache that can be wrong, and a cache that can be wrong about freshness lies at exactly the moment freshness matters — which is when something upstream just changed. The system cannot hold one.

The compromise that works is the one v5 already established: cache keyed by state digest. A digest-keyed cache cannot go stale, because a changed state produces a changed key and a changed key cannot hit the old entry. That is not a discipline anyone maintains; it is a property of the key.

**What it requires mechanically.**

1. Freshness is derived at read time from the closure, or from a cache whose key is the closure digest. No other cache may answer a freshness question.
2. Any surface reporting freshness reports its **basis**: the root it was computed against, the number of dependencies walked, and the count that could not be walked. A badge with no basis is a badge with no meaning.
3. Where a closure cannot be walked — a missing source version, an unavailable adapter, an unreachable remote — the answer is `WI_FRESHNESS_UNCOMPUTED` with the reason. It is never `fresh`, and it is never `stale`. Those are both claims, and neither was earned.
4. `wi simulate` reports the **provably-unaffected count** beside the stale frontier. That number is the honest half of the report and it is what keeps the mechanism usable.
5. Background indexing may make freshness faster. It may never make it different. If an index is incomplete, absent, corrupt or mid-rebuild, every verdict must be the same verdict, more slowly.

**Freshness with its basis, which is the only form permitted.**

```
$ python3 scripts/wi.py why --node release:dist/narrative.pdf --freshness

release.artifact  dist/narrative.pdf   sha256:4c1e…9b3a
  attested at   2027-03-14T11:02:19Z   knowledge time 2027-03-14
  root          sha256:8c31…07a4

Freshness  NOT FRESH
  basis     1,918 of 1,919 closure states walked
  moved     1   source.version needs_assessment.txt  @v2 → @v3
  unwalked  1   sheet_range anchor a-0233   WI_CAPABILITY_UNAVAILABLE
                (no spreadsheet adapter on this surface)

The artifact's bytes are unchanged. The claim that it was verified is not
current, and one dependency could not be checked at all.
```

The last two lines are Law C at release level. The system distinguishes *this broke* from *this could not be checked*, and refuses to let the second quietly become the first.

---

## 5. The v6 law

The six laws above reduce to one sentence, stated here once:

> **No consequential state transition may become authoritative unless the system can identify the exact prior state, the proposed next state, the semantic delta between them, the dependency impact of that delta, the acting authority, the decision basis and the resulting proof closure.**

Seven identifications. Each is a question the system must answer mechanically, and each has an executable or specified mechanism behind it:

| # | The system must identify | Answered by | Failure code when absent |
|---|---|---|---|
| 1 | The exact prior state | The target state digest on the proposal | `WI_PROPOSAL_STALE` |
| 2 | The proposed next state | The candidate state, canonicalized by `wi canon` | `WI_INPUT_INVALID` |
| 3 | The semantic delta between them | `wi simulate` and `wi diff --semantic` under Law H | `WI_CLAIM_ATOMIZATION_FAILED` |
| 4 | The dependency impact | The stale frontier and provably-unaffected set from `wi simulate` | `WI_FRESHNESS_UNCOMPUTED` |
| 5 | The acting authority | The capability grant named by the transition | `WI_AUTHORITY_ABSENT` |
| 6 | The decision basis | The decision record from `wi decide`, bound to the target digest | `WI_DECISION_STALE` |
| 7 | The resulting proof closure | The closure over the new graph root and the obligations from `wi obligations` | `WI_REVIEW_REQUIRED` |

**Why the sentence is written as a refusal rather than a requirement.** A requirement is satisfied by trying. A refusal is satisfied only by succeeding, and it names what happens when the attempt fails: the transition does not become authoritative. There is no partial state in which six of the seven are known and the change is applied anyway with a note. Seven of seven, or the state does not move.

**Why *consequential* is in the sentence.** Not every transition is one. Creating a branch, switching a branch, running a query, building a rendering and inspecting a capsule change no meaning and require none of the seven. The word is doing real work: a system that demanded a decision record to run a report would be a system nobody runs. The line is drawn at the semantic delta — a transition is consequential when it changes a `meaning.*`, `canon.*`, `authority.*` or `release.*` state, and `wording_only` is consequential too, because Law H says the classification itself is a claim that has to be made rather than assumed.

**What the sentence does not claim.** It does not claim the change is correct. It does not claim the sources were right, the reasoning sound, or the author wise. It claims only that the change is *accountable* — that every question an auditor, a co-author, a reviewer, a court or the author at 2 a.m. two years later would ask has an answer that does not depend on anyone's memory. That boundary is inherited from [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md), and v6 does not relax it.

---

## 6. The twelve-layer runtime

**Status: L0 through L7 partially executable per the command table in section 1.1; L8 through L11 specified.**

v6 is a runtime, and a runtime has layers whose privileges differ. The table below is normative. Two columns are the whole point of it — **may decide proof** and **may write graph**. Every architectural argument in this project eventually reduces to one of those two answers being wrong in one row.

| Layer | Responsibility | May decide proof? | May write graph? |
|---|---|---|---|
| **L0** Canonicalization | Bytes to canonical form. NFC, key ordering, decimal normalization, domain-separated digests. `wi canon`. | No | No |
| **L1** Semantic IR | Typed meaning objects. Claim atoms, definitions, obligations, promises, forecasts. Construction and validation. | No | No — constructs candidate states only |
| **L2** Graph store | Nodes, edges, states, invalidations. The immutable object store and its index. | No | **Yes** — the only writer, reachable only inside an L4 transaction |
| **L3** Temporal | Valid and knowledge intervals. Interval arithmetic, `as-of` reconstruction, sequence-versus-conflict. | No | No |
| **L4** Version control | Branches, commits, graph roots, deltas. The commit transaction. | No | **Yes** — via L2, and only with an L6 authorization present |
| **L5** Semantic merge | Three-way merge over deltas. Conflict detection and retention. | No | No — emits a merge result and conflict set; L4 writes them |
| **L6** Authority | Capability grants, scope, delegation monotonicity, revocation, expiry. | No | **Yes** — `authority.*` nodes only |
| **L7** Proof and obligation | Checks, anchors, obligations, closures, staleness, constraints. | **Yes — the only layer that may** | **Yes** — `verification.*` nodes only |
| **L8** Bounded autonomy | Agent execution, simulation, proposal emission, replay records. | No | No — proposals only, and a proposal is not a state |
| **L9** Policy and release | Policy evaluation, gates, builds, attestations, capsules. | No — it reads L7 verdicts | **Yes** — `release.*` and `policy.*` nodes only |
| **L10** Surfaces | CLI, library, REST, MCP, Workbench, CI. Ergonomics, presentation, access control. | No | No — translates, never decides |
| **L11** Federation | Remotes, capsule exchange, selective disclosure, inclusion proofs, import records. | No | **Yes** — `remote.*` and import-record nodes only |

### 6.1 The four rules the table encodes

**One layer decides proof.** L7 and nothing else. A surface that computes a check, a policy engine that infers a verdict, a merge that marks something verified because both sides were, a federation import that carries a remote's verdict in as a local one — every one of those is a second implementation of `verified`, which Law K prohibits. The column exists so the prohibition is checkable by reading a diagram rather than by reading every file.

**Writes are narrow and typed.** Five layers may write, and each writes exactly one family. L6 cannot write a claim. L9 cannot write a grant. L11 cannot write a verification. This is what makes a compromised or defective layer bounded: a federation bug can produce a wrong import record and cannot produce a wrong proof.

**One transaction.** L2 is the only writer of graph state and is reachable only from an L4 commit. Every other writing layer produces its object and hands it to a commit; nothing writes around the transaction. The consequence is that *every* authoritative change appears in `wi log`, including grants, verifications, releases and imports. **A change that does not appear in the log did not happen.**

**Autonomy is above the write line.** L8 sits between the proof layer and the policy layer and holds no write capability at all. That placement is Law P as a picture: an autonomous actor has more read access than almost anything in the system and no write access whatsoever.

### 6.2 Where a layer violation actually shows up

Layer violations do not arrive as architecture proposals. They arrive as small, reasonable requests, each of which is a privilege escalation in the shape of a convenience:

| The request | The layer it moves | Why it is refused |
|---|---|---|
| "The MCP surface should cache verdicts so the editor is fast" | L10 decides proof | A cache that computes a verdict is a second engine. A cache keyed by closure digest is not, and is permitted. |
| "The merge should keep the verified side automatically" | L5 decides proof | The merge would be choosing which claim is true, on the grounds of which one had a check run against it. |
| "Import should trust our partner's attestation" | L11 decides proof | Their verdict, our badge. The evidence travels; the verdict does not. |
| "The gate should mark trivially-passing claims verified" | L9 decides proof | The gate reads verdicts. A gate that writes them has no independent reading left. |
| "The agent should apply changes it is highly confident about" | L8 writes graph | Confidence is not authority, and there is no threshold at which it becomes authority. |
| "Grants should be inferred from repository permissions" | L6 grants ambiently | An inferred grant is exactly the ambient authority Law O removes. |

### 6.3 What this changes about v5

v5's architecture in [`../v5/ARCHITECTURE.md`](../v5/ARCHITECTURE.md) described a core with adapters around it. That remains true and is now the L10 row. What v6 adds is that the core itself has an internal privilege structure, and the interesting failures are not at the adapter boundary — they are inside, where a merge is tempted to decide a proof and a policy engine is tempted to write a claim.

---

## 7. The actor model, extended

**Status: specified.**

The v5 actor types are carried forward unchanged. v6 adds two, and constrains one further.

| Actor type | Is | New in v6 |
|---|---|---|
| `human` | A named individual acting on their own authority | |
| `team_member` | A named individual acting under a project's policy | |
| `authorized_editor` | A delegate with explicit, recorded authority to accept changes | |
| `automated_policy` | A rule the project configured, acting without a person present | |
| `deterministic_engine` | The core, executing a check | |
| `judgment_provider` | A third-party inference service, named | |
| `external_import` | State that arrived from outside this workspace | |
| `autonomous_agent` | A process that reads, computes and emits proposals under a recorded objective | **yes** |
| `remote_workspace` | Another v6 workspace, identified by its root and its capsule commitments | **yes** |

**`autonomous_agent` is not a stronger `automated_policy`.** An `automated_policy` is a rule somebody wrote out: *when a source version changes, re-run the numeric checks.* Its behaviour is fully described by its configuration, and it can be read. An `autonomous_agent` is a process whose specific outputs are not predictable from its configuration, which is exactly why Law P denies it write capability and requires a replay record. The two are separate types so that a policy is never mistaken for an agent, and — more importantly — so that an agent is never quietly filed as a policy in order to inherit whatever the project decided policies could do.

**`remote_workspace` exists so a foreign assertion has a type.** Without it, imported state either loses its origin or borrows a local actor's identity, and both are worse than an honest name for *this came from somewhere else*.

**Actor kind narrows what may be granted; it never grants.** This is the sentence that separates v6's authority model from every access-control system that ties permissions to roles. A `human` who holds no grant can do nothing. An `authorized_editor` is not authorized because of the name; the name describes an actor that has been given a grant, and if the grant expires the name is a description of history.

**The constitutional denials, restated as a table**, because they are the ones an implementation will be asked to soften:

| Actor kind | May never hold | Regardless of |
|---|---|---|
| `judgment_provider` | `claim.accept`, `canon.modify`, `proof.waive`, `release.approve`, `release.sign`, `authority.delegate` | who invoked it, how the request was phrased, how good the provider is |
| `autonomous_agent` | any capability whose name begins `*.accept`, `*.approve`, `*.sign`, or `authority.*` | its track record, its confidence, its objective |
| `automated_policy` | `source.approve` — a discovered source is `candidate` until a human approves it | any configuration flag |
| `external_import` | any capability at all | the exporting workspace's own grants |

The last row is the federation rule in its shortest form. A capsule can carry a grant *record*, so that a reader can see what authority the exporting workspace claimed. It cannot carry the authority itself.

---

## 8. The v6 failure codes

**Status: specified; the codes emitted by the executable commands in section 1.1 are executable.**

v5's error taxonomy in [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md) is carried forward. v6 adds the codes below. Every one names a refusal, and every one has a repair route — a code with no route is a dead end, and a dead end is where people learn to pass `--force`.

| Code | Raised when | Repair route |
|---|---|---|
| `WI_AUTHORITY_ABSENT` | A transition names no grant, or names one that is expired, revoked or out of scope | Obtain a grant with `wi authority issue`, or ask the issuer to widen scope |
| `WI_AUTHORITY_EXCEEDED` | A delegation would widen capability, scope or lifetime beyond its parent | Narrow the child grant, or delegate from a wider parent that already exists |
| `WI_CONFLICT_OPEN` | A gate or release is attempted with an unresolved semantic conflict in scope | Resolve with `wi decide --conflict`, naming the surviving state and a reason |
| `WI_FRESHNESS_UNCOMPUTED` | A closure could not be fully walked, so freshness has no answer | Restore the missing source version, or install the adapter, or accept the unwalked count explicitly |
| `WI_TEMPORAL_UNDEFINED` | A consequential claim carries no valid interval and policy requires one | Declare the period the claim covers; `null` end means open, and is a declaration |
| `WI_TEMPORAL_INCOHERENT` | An interval ends before it begins, or a knowledge interval precedes the state it describes | Correct the interval; a correction appends rather than rewrites |
| `WI_RENDERING_UNGOVERNED` | An artifact is presented as an output of this system with no `built_from` root | Rebuild from a graph root, or stop treating the file as an output |
| `WI_MERGE_BASE_ABSENT` | A three-way merge has no common ancestor | Name a base explicitly, or import the missing history before merging |
| `WI_CAPSULE_INCOMPLETE` | A capsule's Merkle commitment covers leaves the capsule does not carry, and the profile does not declare them withheld | Rebuild the capsule at a profile that declares the withheld set |
| `WI_OBLIGATION_UNMET` | A proof obligation derived from typed state and release target has no satisfying evidence | Satisfy it, waive it under a `proof.waive` grant, or lower the release target |

**Why every code carries a route.** A refusal an operator cannot act on is a refusal they route around. The route is not customer service; it is the mechanism that keeps the refusal enforceable, because the alternative to a stated repair is an invented one.

---

## 9. What v6 does not change

**Status: specified.**

The permanent refusals in [`../v5/NON_GOALS.md`](../v5/NON_GOALS.md) are carried forward without exception. Four are worth restating here, because v6's new capabilities are exactly the ones that make people ask again:

**Federation does not create trust.** A capsule imported from another organization carries that organization's assertions and their proof closure. It does not carry their authority. A remote's `verified` becomes a local `verified` only when this workspace's own L7 re-derives it from the evidence in the capsule. An import that adopts a remote verdict has outsourced the one thing this system exists to keep local.

**Autonomy does not create authority.** An agent that produces a thousand correct proposals holds exactly the authority its grants name, which is none by default. There is no accrual, no reputation score, no promotion path, and no configuration in which an actor earns write capability through performance.

**Time travel does not rewrite.** `wi as-of` reconstructs what was believed. It does not offer a mode in which a past state is edited so the record reads better. A correction appends. There is no compaction pass that drops superseded knowledge intervals, and requests for one are refused.

**Selective disclosure does not weaken proof.** A redacted capsule proves less, and it says so. It never proves the same thing with fewer bytes. An inclusion proof over a withheld leaf demonstrates that a commitment covered something; it does not demonstrate what.

---

## 10. Amendment

**Status: specified.**

v5 named five terms as protocol rather than copy. v6 adds five more. All ten are load-bearing in other people's compliance processes, other people's CI pipelines, other people's contracts and other people's editorial standards.

| Term | From | What it names |
|---|---|---|
| `verified` | v5 | A deterministic comparison that executed and passed |
| `stale` | v5 | A proof whose dependency moved |
| `BLOCK` | v5 | A gate verdict that stops a release |
| `permitted` | v5 | A policy allowance |
| `source quarantine` | v5 | The boundary before source content reaches model context |
| `authoritative` | **v6** | A state that has become the workspace's answer, having satisfied all seven identifications of the v6 law |
| `authorized` | **v6** | An act performed under a valid, unexpired, unrevoked, in-scope capability grant |
| `fresh` | **v6** | A state whose entire closure is at the state it was checked against, computed at read time |
| `conflict` | **v6** | Two retained, incompatible states of one logical node, unresolved |
| `capsule` | **v6** | A portable proof closure with a Merkle commitment, verifiable without the workspace that produced it |

**Any change to the meaning of any of them requires an RFC and a benchmark update.** Not a pull request. Not a documentation clarification. An RFC with a comment period, and a benchmark case that fails before the change and passes after it. Process: [`../../governance/RFC_PROCESS.md`](../../governance/RFC_PROCESS.md).

**Why it is load-bearing.** Loosening happens by accretion, never by decision. Each individual widening is defensible; the sum is a system where `authoritative` means "we saved it" and `fresh` means "nothing has obviously broken." The RFC requirement exists to make each widening cost something and to leave a record of who paid.

`fresh` is the one to watch. It is under the most pressure, because computing it honestly is slower than asserting it, and every performance conversation about this system will arrive at a proposal to store it. The correct answer to that proposal is a digest-keyed cache. The incorrect answer that will be proposed first is a boolean column with a refresh job.

`authorized` is the second one to watch, and it fails differently. Nobody proposes weakening it. It weakens when a convenience grant is issued wide because narrowing it was fiddly, and then a second one is issued wide because the first one was, and eventually every actor holds `claim.accept` over the whole workspace and the model is a formality. That erosion is invisible in a diff and visible in `wi authority check`, which is why the command exists.

Renaming a command, adding a capability to the vocabulary, adding a node type, adding a constraint to the C001–C020 set, or extending a schema with an optional field does not require a constitutional amendment. Changing what a word *promises* does.

---

## 11. What a v6 release promises

v5 promised that a reader could interrogate a finished document. v6 promises something about the process that produced it:

> **Every state in a v6 workspace can name the state it came from, the delta that produced it, the authority that permitted it, the decision that accepted it and the dependencies it now rests on — and any of those answers can be checked by a machine that was never in the room, at any point in the past, without trusting the workspace that produced them.**

Everything in this document exists to make that sentence true, and to make it clear exactly which parts of it run today.

Read next:

- [`EXECUTABLE_MEANING.md`](EXECUTABLE_MEANING.md) — the thesis, and the twelve-step derivation from v5 to v6
- [`SEMANTIC_VERSION_CONTROL.md`](SEMANTIC_VERSION_CONTROL.md) — branches, commits, proposals, decisions
- [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md) — Law O in operation
- [`BITEMPORAL_STATE.md`](BITEMPORAL_STATE.md) — Law N in operation
- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — the v6 intermediate representation
- [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — the laws this document rests on
- [`../v5/NON_GOALS.md`](../v5/NON_GOALS.md) — the permanent refusals
- [`../../README.md`](../../README.md) — the project

---

*v4.0 proved authorship can be held accountable. v5.0 proved the account can be carried, checked and re-checked by someone who was never in the room. v6.0 proves the account holds while the work is still moving.*

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
