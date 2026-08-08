# Writing Intelligence v6.0.0 — The Sovereign Meaning Runtime

**v3 governs how well the writing is built. v4 governs what may be claimed about it. v5 governs what a finished document can prove about itself. v6 governs what may become true, who is permitted to make it true, and what it costs.**

Free. Open source. MIT. Forever.

---

## The promise, in one line

> **Ask what a change would do before the change exists — then find out who is allowed to make it, what the acceptance was bound to, and what provably survived.**

v5 closed the gap between *this was checked* and *this is still true*. Point at a sentence and it told you what supported it, what depended on it, and what a changed source broke. That was a system that could describe the past accurately.

It could not tell you anything about a future. It had no answer to *what happens if we raise this figure*, because the only way to find out was to raise it. It had no answer to *was this person allowed to accept that*, because it recorded who acted and never whether they could. It had no answer to *what exactly did the reviewer see when they said yes*, because approval and application were the same event. And when two branches of the same document disagreed about a number, it had no answer at all, because nothing in it had ever been asked to merge meaning.

v6 is those four gaps closed. A change is **proposed** against an exact state and nothing moves. It is **simulated** and still nothing moves — the report names the semantic delta, the stale frontier, the repair plan, the authority required, and the count of nodes provably untouched. It is **decided** by an actor holding a scoped, expiring grant, and the decision is bound to the exact state digest that actor reviewed. It is **committed** as one transaction. And when two branches assert incompatible states of the same claim, the merge stops and keeps both — because a number neither branch asserted is not a compromise, it is a fabrication.

---

## What changed, at the level of what the system *is*

v5's unit was the claim atom and its structure was a graph. Both survive unchanged. What changed is that the graph acquired a **clock, a queue, a permission system and a history**.

A document in v5 was the thing you edited, with a graph describing it. A document in v6 is a **build** of governed meaning — the semantic state is the writable thing, and the `.md`, the deck and the filing are renderings of it. That single inversion is what makes everything else possible. You cannot simulate a change to a file. You can simulate a change to a state, because a state has an identity, and a candidate state has an identity too, and the two can be compared without either of them being written anywhere.

The practical consequence is that four questions became answerable that were not:

| Question | v5 | v6 |
|---|---|---|
| *What would this change break?* | Make the change, then run `wi impact` | `wi simulate` — reports the candidate root, the deltas, the stale frontier, the repair plan and the provably-unaffected count, and writes nothing |
| *Was this person allowed to do that?* | Records who acted | `wi authority` — a scoped, expiring grant is named on the transition, and absence of a grant is a refusal rather than a default-allow |
| *What exactly did the reviewer approve?* | An approval is a fact about a document | A decision binds to an exact state digest. When the target moves, the approval does not follow it — `WI_DECISION_STALE` |
| *These two versions disagree. Now what?* | Nothing | `wi merge` keeps both states as a typed conflict and refuses to produce a third |

---

## The v6 law

Quoted once, because it is the whole release compressed:

> **No consequential state transition may become authoritative unless the system can identify the exact prior state, the proposed next state, the semantic delta between them, the dependency impact of that delta, the acting authority, the decision basis and the resulting proof closure.**

Seven identifications. Each has a mechanism behind it and a failure code when it is absent. The derivation is in [`references/v6/CONSTITUTION.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/CONSTITUTION.md).

---

## The six new laws

Six from v4, six from v5, six new. None of the twelve older ones has been softened, reinterpreted or qualified.

### Law M — The semantic state is canonical; renderings are builds

*A `.docx`, a deck, a site or a filing is a rendering of governed meaning. A renderer may change expression. It may not silently change what it renders.*

**Why it is load-bearing.** v5 already preferred this architecturally and then left the draft file writable, because there was no other way to work. Two writable sources of truth in one workspace do not announce their divergence. They diverge quietly, on the day somebody opens the built document to fix a typo and fixes a number on the way past — at which point every check the system runs still passes, because the checks run against the graph and the graph was not touched. A rule that says *please edit in the graph* is obeyed until it is inconvenient. A rule that says *an edit in a rendering is a proposal, and the next build overwrites it* is enforced by the build, and nobody has to be diligent.

### Law N — Time is part of meaning

*Valid time is when a claim holds in the world. Knowledge time is when this workspace believed it. A correction supersedes; it does not erase.*

**Why it is load-bearing.** Two people ask two different questions about the same number and only two independent clocks answer both. A reader or a court asks *what do we now believe was true in 2022*. An auditor asks *what did we know when we filed this in March 2028*. An overwrite answers the first and destroys the second. A change log answers the second badly and the first not at all. And once the two intervals are independent, contradiction detection stops crying wolf: a tax rate of 21% through 2028 and 24% from 2029 is a schedule, not a conflict, and a system that flags it is a system whose contradiction report gets switched off — taking the real contradictions with it.

### Law O — Authority is explicit, scoped and expiring

*Nobody holds authority because of what they are. A grant names subject, capability, scope and a window, and delegation may narrow it but never widen it.*

**Why it is load-bearing.** Nobody is surprised to learn who made a change. They are surprised to learn that person *could*. Ambient authority — *the author can do anything* — is not a policy anybody chose; it is the absence of one, and it is indistinguishable from a policy until the day it matters. Every other control in the system is decorative if any actor can perform any transition whenever it holds the file. Expiry is the part people want to drop and the part that pays for itself: the reviewer who helped for two weeks in March does not still hold acceptance authority in November, not because somebody was diligent but because the grant said so.

### Law P — Autonomy produces replayable proposals, not invisible mutations

*Anything automated may plan, retrieve, draft, judge, simulate and propose. It may not bypass the proposal, impact and authority machinery a person uses.*

**Why it is load-bearing.** Law A was written for one model helping one author, where the author reads every proposal because there are eleven of them. That premise does not survive scale. The failure mode is not a rogue process. It is an ordinary, well-behaved, useful one that fixes four hundred small things correctly and one thing wrongly — and by the time anybody notices, the wrong one has three hundred commits on top of it. Attribution after the fact is not attribution; it is archaeology. Review happens before application or it does not happen.

### Law Q — Semantic disagreement is preserved until resolved

*A merge may never manufacture consensus by averaging, smoothing or generalizing two incompatible states.*

**Why it is load-bearing.** Every text merge tool resolves by position, and position is not meaning. Two people editing the same paragraph produce a conflict the tool stops on, which is fine. The dangerous case is the opposite: two people editing *different* paragraphs that assert incompatible things. Every text tool completes that merge cleanly, and what comes out contains a contradiction nobody introduced and nobody will find. Last-writer-wins is a correctness policy nobody would choose if asked — it means whoever saved second was right, about a question neither knew they were answering. **A conflict is not a failure of the merge. It is the merge's most useful output.**

### Law R — Freshness is a property of dependencies, not a green badge

*Time passing does not make a verified thing false, and a stale dependency may not hide behind an artifact that was once green.*

**Why it is load-bearing.** A timestamp is not a dependency. *Verified three days ago* is a fact about a clock and a reader hears it as a fact about the document. v5 removed that lie at claim level; v6 has to remove it everywhere it reappears — on a branch, a release, an imported capsule, a cached view, a badge in a README. The pressure toward a stored freshness flag is real and comes from performance, and a stored flag is a cache that can be wrong about freshness at exactly the moment freshness matters. The answer that works is the one v5 already established: cache keyed by state digest, because a changed state produces a changed key and a changed key cannot hit the old entry. That is not a discipline anybody maintains; it is a property of the key.

---

## What is new, command by command

Sixteen new commands. Every transcript below was produced by running the tool, in a scratch workspace, on the session this document was written from. Nothing is illustrative.

### `wi canon` — canonical form and a domain-separated digest

Meaning needs an identity that survives reformatting, or staleness fires at random and a rewrite that changed nothing invalidates a proof.

```
$ wi canon households.json

canonical bytes  251
content digest   sha256:b06f6428e9d0c23a824e1271badaa5ef91559c81a55966b7b0fde62b2b515e34
v6 state digest  sha256:660710f61809d278cd8109016e5e0ad9db865bb86b15ee73c5202dd60b79f8fd
v5 state digest  sha256:1d3ba16cf8359c47a3ad4732f942dacddb672a539330c3238f9c84e8ab37f175

The two state digests differ by domain separation, on purpose:
a byte-identical payload must never be ambiguously readable as
both a v5 and a v6 object.
```

Key order and Unicode normalization do not move the digest; a changed value does. Both directions are asserted in the suite, because a digest that never moves and a digest that always moves are equally useless and only one of them looks broken.

### `wi propose` — a change bound to an exact state

```
$ wi propose --node households --payload households-v2.json \
    --why "the agency republished its 2022 count" --actor antonio

PROPOSED on main

  5a4cfd4c-d14c-5c45-98bc-00d0392af0ad
    node      households
    delta     quantity_changed
    requires  claim.accept.quantity_change
    bound to  sha256:27a2826b8efb24acd608eb45eacb7aa67e4f50d5213ccfef4401ed32d4734bff

Nothing has changed on main. A proposal is not an edit — run
`wi simulate` to see what accepting it would do.
```

Three fields carry the release. **`delta`** is what the change did to meaning, computed by comparing typed state rather than characters. **`requires`** is the capability that follows from that delta — a wording change and a number change land in the same sentence and require different authority, and a system that cannot tell them apart is not enforcing anything. **`bound to`** is the exact state digest this proposal was written against; when the target moves, this proposal does not follow it.

### `wi proposals` — the queue

```
$ wi proposals

PROPOSALS on main

  [open     ] 511bb95c-ba90-5c1e-af2d-632128566b74
      households       ->  node_created
      requires claim.accept   proposed by antonio
      baseline figure from the outcomes report
```

Status moves `open` → `accepted` / `rejected` → `applied`. Accepted and applied are separate because they are separate events, and a system that collapses them cannot tell you the difference between *the reviewer said yes* and *it is in the document*.

### `wi simulate` — what a change would do, before it exists

```
$ wi simulate --actor antonio

SIMULATION ONLY — main is unchanged

Semantic change
  households
    class   quantity_changed
    proof   invalidates: quantity_changed

Authority required
  households                               claim.accept.quantity_change  [held]

Impact
     1 node(s) directly changed
     0 node(s) become stale
     0 node(s) stale through an invalidated proof

Minimum safe repair frontier
  1. reverify           households
     delta class quantity_changed does not carry a prior proof forward

  ordering: lexicographic: human_reviews > deterministic_runs > judgment_calls > external_dependencies > changed_renderings

Provably unaffected
     3 of 4 node(s) on main

candidate root  sha256:4be47dc732df34854d2ae4f651c2adff6af3f98f52006b7067733f4bff094af1
Nothing was written. This root exists only to be compared.
```

Read the last two blocks together, because they are the argument.

**Provably unaffected** is the same load-bearing negative v5 established with `wi impact` and it matters more here, because a simulation runs on every consequential edit rather than only after a source moves. A report that is a wall of red is a report an author stops reading, at which point the mechanism has cost more than it returned. Three of four nodes are not *probably* fine — the comparison over typed state found no intersection, and that is arithmetic.

**The candidate root** is the sharper half. It is the graph root the commit *would* produce, computed without writing anything. In the walkthrough later in this document the simulate line reads `candidate root sha256:c78acd5adab21ec2…` and the commit that follows reports `next root sha256:c78acd5adab21ec2…`. The same value. A simulation that produces a different root than the commit is not a preview, it is a guess with formatting — and the equality is checkable rather than promised.

### `wi authority` — grants that expire

```
$ wi authority issue --subject antonio --capability claim.accept \
    --scope workspace --issuer antonio --expires 2030-01-01T00:00:00+00:00

issued e322307b-57f3-5158-8108-67c315933eb2
  antonio -> claim.accept in scope workspace

$ wi authority list

CAPABILITY GRANTS

  e322307b-57f3-5158-8108-67c315933eb2  [active]
      antonio -> claim.accept
      scope workspace
      issued by antonio  expires 2030-01-01T00:00:00
```

Sixteen capabilities, seven scope kinds and seven actor kinds. The full treatment is in [Authority](#authority) below.

### `wi decide` — an authorized decision bound to what was reviewed

```
$ wi decide 511bb95c-ba90-5c1e-af2d-632128566b74 --accept --actor antonio

DECISION ACCEPTED
  proposal   511bb95c-ba90-5c1e-af2d-632128566b74
  bound to   (new node)
  actor      antonio
  grant      e322307b-57f3-5158-8108-67c315933eb2 (claim.accept)

Accepted is a decision, not an application. Run `wi commit`
to apply every accepted proposal as one transaction.
```

The decision names the grant it exercised. That is the difference between an audit trail that says *antonio accepted this* and one that says *antonio accepted this, under a grant issued by antonio on this date, scoped to the workspace, expiring in 2030* — and only the second is answerable to somebody asking whether he could.

And when the target has moved since the proposal was written:

```
$ wi decide 8b12… --accept --actor antonio

WI_DECISION_STALE: the target moved after this proposal was written
    branch_now_holds: sha256:8c314913c949c90edde1a52fd73a6c5cf944cda283058990da4df3ef434add1e
    proposal_bound_to: sha256:4b8e4cb7e077692b3d7688c636e5c1573fb2892b42b6a9b47ae7bca129353f2d
  repair:
    - re-read the current state and open a new proposal
    - the system will not reattach an approval to a state the reviewer never saw
```

Re-attaching would be the convenient behaviour and it is the one that silently launders an approval onto text nobody read.

### `wi commit` — accepted proposals apply as one transaction

```
$ wi commit -m "baseline figures from the outcomes report" --actor antonio

COMMIT 923c8decae77
  branch      main
  prior root  sha256:87e2f3219580cb3db904fddc9669a3d7ecbe313f745923700b41a9bd8d60eae7
  next root   sha256:15f9a6e30b025284520591f3aa1f11b99aa9b05d6d1aac2e3c8110aa0ac879cd
  applied     4 accepted proposal(s)

  households       node_created
  waittime         node_created
  counties         node_created
  staffing         node_created
```

### `wi log` — semantic history

```
$ wi log

HISTORY of main

  c281235d523a  wait time: 21 days
      root d522d0f1ae9cd6457e30
      2026-08-08T00:58:09 by antonio   1 decision(s)   4 node(s)
  aff95ef97b5c  agency correction: 11,240 households
      root ac4184e99ec2da3d07be
      2026-08-08T00:56:05 by antonio   1 decision(s)   4 node(s)
  923c8decae77  baseline figures from the outcomes report
      root 15f9a6e30b0252845205
      2026-08-08T00:55:28 by antonio   4 decision(s)   4 node(s)
  2514e1f98077  initialize the v6 semantic layer
      root 87e2f3219580cb3db904
      2026-08-08T00:55:27 by author   0 decision(s)   0 node(s)
```

### `wi branch` — named pointers, nothing copied

```
$ wi branch create audit

created audit at 923c8decae77
A branch is a ref. Nothing was copied: the objects are immutable
and shared, so this cost one row.

$ wi branch list

BRANCHES
    audit                    98142482d94e     4 nodes  audit reconciliation: 12,400 households
    legal                    dbc5fb1fb9fa     5 nodes  notice obligation
  * main                     c281235d523a     4 nodes  wait time: 21 days
```

### `wi merge` and `wi conflicts` — see [The conflict-preserving merge](#the-conflict-preserving-merge)

### `wi obligations` — what must be proved, derived rather than listed

```
$ wi obligations --node notice

PROOF OBLIGATIONS — legal, mode strict

  notice           [meaning.obligation / external_fact / human_declared]
      required   anchor.integrity                 an external fact with no anchor is an assertion wearing a ci...
      required   citation.resolution              every citation resolves to an ingested source
      required   realm.preservation               the epistemic realm is carried into every rendering
      required   entity.presence                  every named entity appears in a supporting source
      required   modality.no-strengthening        certainty did not increase beyond the source
      required   negation.preservation            polarity survives the rewrite
      required   obligation.exception-preservation no declared exception was dropped
      required   authority.grant-valid            the acting grant was active and in scope

8 obligation(s) across 1 node(s).
These were derived from typed state, release target and policy —
not from a checklist hard-coded inside a command.
```

That last line is the whole design. A node carrying an obligation owes `obligation.exception-preservation` and owes no numeric check, because it states no quantity. A claim atom carrying two quantities owes `numeric.value`, `numeric.unit`, `numeric.dimension`, `date.range`, `scope.temporal` and `scope.spatial` — twelve obligations, none of which anybody wrote down for that node. The suite asserts both directions: that a quantity generates a numeric obligation, and that a node with no quantity owes none. A checklist that fires the same items on every node is a checklist that gets skimmed.

### `wi as-of` — the two clocks

```
$ wi as-of --valid-at 2019-06-01

AS OF
  branch      main
  known at    now
  valid at    2019-06-01
  commit      aff95ef97b5c

  counties         Services reached seven counties.
      valid 2019-01-01 -> 2023-01-01
      known 2026-08-08T00:55:27
  waittime         Median intake wait time fell from 42 days to 26 days.
      valid 2019-01-01 -> 2023-01-01
      known 2026-08-08T00:55:27

This is what the workspace held then, not today's corrected
state wearing an old date.
```

The households figure and the staffing figure are absent, correctly — both are valid from 2022 and neither held in 2019. And a knowledge-time query before the workspace existed returns the honest answer rather than an empty list that looks like a result:

```
$ wi as-of --known-at 2000-01-01T00:00:00+00:00

AS OF
  branch      main
  known at    2000-01-01T00:00:00+00:00
  valid at    any instant
  commit      (none)

  no state satisfies both clocks
  this workspace knew nothing at that instant
```

### `wi constraints` — twenty graph constraints, and what could not be evaluated

```
$ wi constraints

GRAPH CONSTRAINTS — main

  ok   C001 source-version-raw-digest-unique
       0 duplicate source digest(s)
  ...
  ok   C007 decision-target-state-not-superseded
       3 decision(s) bound to a state this branch has since moved past; each is retained as history, none authorizes the current state
  ok   C008 provider-has-no-authority-grants
       0 grant(s) issued to a judgment provider
  --   C009 release-closure-is-complete
       no v6 release closure in this workspace; `wi verify-release` checks the v5 closure of an existing .wiab
  --   C011 claim-realm-cannot-disappear-in-rendering
       no render source maps in this workspace; the compiler backends that produce them are specified and do not ship in 6.0.0
  FAIL C015 semantic-conflict-cannot-be-rendered-as-resolved
       1 unresolved semantic conflict(s) on main
         - eb0c0529-bc35-5350-a0c9-5e069e31f582
  ok   C020 actor-cannot-exercise-revoked-or-expired-grant
       0 decision(s) exercised a grant after it was revoked

15 evaluated, 5 not evaluated, 1 failed.
A constraint that could not run says so and says why. There is no
fourth status and no aggregate score.

VERDICT FAIL
```

Three things are worth reading twice. **`--` is not `ok`.** Five constraints could not be evaluated in this workspace and each names its reason; folding them into a pass would be the exact failure this project exists to catch. **C007 passes while reporting three superseded decisions**, which is the correct reading: a decision bound to a state the branch has moved past is history, not a defect, and it authorizes nothing today. And **there is no percentage anywhere**, asserted by the suite — a constraint engine that emits a score has averaged across kinds of failure that are not commensurable, and the number would be quoted.

### `wi capsule` — proof of one claim without the whole vault

```
$ wi capsule create --out households.wic --select households --profile selective

wrote households.wic
  profile        selective
  closure root   sha256:99ae33d4bd15b7b5bd728416071404b6d4571b4dd91b325312e365fe757d5f9e
  leaves         4 total, 1 disclosed, 3 redacted

A redacted leaf proves it was inside the producer's closure.
It does not prove you inspected its content, and this capsule
does not say otherwise.
```

```
$ wi capsule verify households.wic

CAPSULE VERIFICATION — households.wic

  ok   capsule.format         format is 'wic/1'
  ok   leaf.digest            1 disclosed leaf digest(s) recomputed
  ok   state.digest           1 disclosed state(s) hash to the digest the leaf names
  ok   inclusion.proof        1 leaf/leaves proved to belong to closure root sha256:99ae33d4bd15
  ok   closure.count          1 disclosed + 3 redacted against a declared 4 leaves

  closure root sha256:99ae33d4bd15b7b5bd728416071404b6d4571b4dd91b325312e365fe757d5f9e

VERDICT VERIFIED

  this capsule proves membership in the producer's closure and the integrity of what it disclosed; it proves nothing about whether the sources are correct
```

Move one byte of a disclosed payload and it says so:

```
$ wi capsule verify tampered.wic

  ok   capsule.format         format is 'wic/1'
  FAIL state.digest           disclosed state for households does not match the digest its leaf names; the bytes in this capsule are not the bytes that were attested
  ok   leaf.digest            1 disclosed leaf digest(s) recomputed
  ok   inclusion.proof        1 leaf/leaves proved to belong to closure root sha256:99ae33d4bd15
  ok   closure.count          1 disclosed + 3 redacted against a declared 4 leaves

VERDICT TAMPERED
```

Exit code `2`. A verifier that cannot fail is decoration, so the suite tampers with a capsule on every run and asserts that the word `VERIFIED` never appears in the output.

### `wi why` — backward from a sentence to its basis

```
$ wi why households

WHY

  The program served 11240 households in 2022.

NODE
  logical id  households
  state       sha256:3ecaa1e4ca65157cff98a465fb169a950fa64f803bd13260dad66f30839c934f
  type        meaning.claim_atom
  realm       external_fact

BASIS
  human_declared
      actor: antonio

TIME
  valid       2022-01-01 -> 2023-01-01
  known from  2026-08-08T00:56:05

INTRODUCED BY
  commit aff95ef97b5c  agency correction: 11,240 households
  actor  antonio at 2026-08-08T00:56:05
  delta  quantity_changed

AUTHORIZED BY
  antonio decided accepted
  under grant e322307b-57f3-5158-8108-67c315933eb2 (claim.accept.quantity_change)
  bound to state sha256:27a2826b8efb24acd608eb45eacb7aa67e4f50d5213ccfef4401ed32d4734bff

PROOF OBLIGATIONS
  required   anchor.integrity
  required   citation.resolution
  required   realm.preservation
  required   numeric.value
  ...

DEPENDED ON BY
  0 node(s)
```

`BASIS` is the reliability type, and it is `human_declared` because a person asserted it — not `verified`, which names a deterministic comparison that executed. The two words are not interchangeable and v6 does not let them become so. `AUTHORIZED BY` names the grant *and* the state digest the decision was bound to, which is what makes the record answerable years later to somebody asking what was in front of the person who said yes.

---

## The four things to reach for first

Sixteen commands is a lot. These four are where the version pays for itself.

**`wi simulate`** is the command that changes how the work feels. Everything else in v6 is machinery that makes it possible; this is the thing you actually run. It answers *what would this do* before the change exists, it reports the provably-unaffected remainder with the same prominence as the breakage, and it writes nothing. Run it before every consequential edit. The candidate root it prints is the root the commit will produce, which means the preview is the thing, not a picture of the thing.

**`wi merge`** on a quantity disagreement will stop and show both numbers. Do not look for a flag that makes it pick one. There isn't one, on purpose, and the reasoning is permanent.

**`wi why`** runs backward from a sentence to its reliability basis, the commit that introduced it, the grant that permitted it, and what still has to be proved about it. It is the fastest way to answer a reviewer who is pointing at a line and asking where it came from.

**`wi capsule`** hands a regulator, funder or partner cryptographic proof of one claim without handing them the whole source vault — and states, inside the artifact, exactly what a redacted leaf does and does not prove.

---

<a id="the-conflict-preserving-merge"></a>
## The conflict-preserving merge

This is the section to read if you read only one.

Two branches. `main` took the agency's correction — the 2022 count was republished at 11,240 after deduplication. `audit` reconciled against county intake logs and arrived at 12,400. Both branches diverged from a common base of 11,800. Both people were doing their jobs, and both were right about the job they were doing.

```
$ wi merge audit --actor antonio

MERGE audit into main

  base commit  923c8decae77

Conflicts — preserved, not resolved
  Quantity     households
      base    The program served 11800 households in 2022.
      ours    The program served 11240 households in 2022.
      theirs  The program served 12400 households in 2022.
      status  unresolved, requires an authorized decision

The engine did not average, soften or generalize these.
Neither branch asserted a middle value, so there is none.
```

Exit code `2`.

**The number that does not appear is the point.** The mean of 11,240 and 12,400 is 11,820. Round it and you get "approximately 12,000", which reads beautifully, survives every review, and is a claim **neither branch asserted and no source supports**. It would be the single most damaging sentence this system could produce, because it would be produced by the component whose entire purpose is to protect the document from exactly that — and it would arrive wearing the authority of a machine that checked things.

So the suite does not merely assert that the merge stops. It asserts that specific fabricated values are **absent from the output**, on every run:

```bash
hasnt "the merge did not invent 12100" "$OUT" "12100"
hasnt "the merge did not invent 12000" "$OUT" "12000"
```

Delete the conflict-preservation logic and those two assertions go red. That is what makes them worth having: a suite that only checks the happy path would stay green with the whole control removed.

The conflict is a first-class object, not a message printed during a merge:

```
$ wi conflicts

SEMANTIC CONFLICTS on main

  [unresolved] Quantity     eb0c0529-bc35-5350-a0c9-5e069e31f582
      node    households
      ours    The program served 11240 households in 2022.
      theirs  The program served 12400 households in 2022.

1 unresolved. A branch carrying an unresolved conflict
cannot be rendered as agreed (C015).
```

It fails constraint C015 and the branch cannot be released while it stands. Resolution is a decision, taken by a named actor, under a named grant:

```
$ wi conflicts --resolve eb0c0529-bc35-5350-a0c9-5e069e31f582 --take ours --actor antonio

resolved eb0c0529-bc35-5350-a0c9-5e069e31f582 by taking ours
  actor antonio under grant e322307b-57f3-5158-8108-67c315933eb2 (claim.accept.quantity_change)
```

```
$ wi constraints

15 evaluated, 5 not evaluated, 0 failed.

VERDICT PASS
```

**The rejected state is retained.** *Somebody chose 11,240 over 12,400* is a different historical fact from *only 11,240 ever existed*, and a record that cannot tell them apart three years later is not a record of a decision.

**A merge that stopped on everything would be a merge nobody runs.** It composes cleanly on every node that does not conflict — wording changes and disjoint semantic dimensions merge without asking. Only an intersection on a consequential dimension stops it: quantity, scope, time, entity, attribution, certainty, causality, legal force, obligation, definition, canon.

---

<a id="authority"></a>
## Authority

Four refusals, and the fact that they are four rather than one is the design. Each sends a person somewhere different, and a single "permission denied" sends them nowhere.

**No grant at all.** The default state of every actor, including the one who created the workspace.

```
$ wi decide 511bb95c-… --accept --actor antonio

WI_AUTHORITY_DENIED: antonio holds no capability grant
    required_capability: claim.accept
  repair:
    - issue one: wi authority issue --subject antonio --capability claim.accept --scope workspace
```

**A grant that has expired.** A different failure, and the repair is different: the person had authority, the window closed.

```
$ wi decide c11b01e2-… --accept --actor reviewer-march

WI_AUTHORITY_EXPIRED: reviewer-march holds claim.accept.quantity_change but the grant is not active at 2026-08-08T00:54:51.881986+00:00
    grants: ['230e4164-b6eb-5265-88f6-7f95d0320741']
  repair:
    - re-issue the grant with a current window
```

**A grant that does not reach.** The capability is right and the scope is wrong — a copyeditor granted acceptance on `review/prose` deciding on `main`.

```
$ wi decide c11b01e2-… --accept --actor copyeditor

WI_GRANT_SCOPE_EXCEEDED: copyeditor holds claim.accept.quantity_change but not in this scope
    grants: ['0e55da5f-8b01-5697-8bde-71f966741401']
    requested_scope: {'kind': 'branch', 'value': 'main'}
  repair:
    - widen the scope, or decide on a branch you hold
```

**A grant that was revoked.** Deliberately withdrawn, and the message says what survives the revocation and what does not.

```
$ wi authority revoke --grant 532aeeaa-a0d4-55e4-848b-f80a6b7cbd8f

revoked 532aeeaa-a0d4-55e4-848b-f80a6b7cbd8f (ex-contractor -> claim.accept)
Existing decisions keep their receipts. Nothing new may be
authorized under this grant from now on (C020).

$ wi decide c11b01e2-… --accept --actor ex-contractor

WI_AUTHORITY_REVOKED: every grant ex-contractor holds for claim.accept.quantity_change has been revoked
    revoked_grants: ['532aeeaa-a0d4-55e4-848b-f80a6b7cbd8f']
  repair:
    - issue a new grant
    - or have a different actor decide
```

Revocation is effective from its recorded instant and does not rewrite history. Decisions taken while the grant was valid remain valid decisions; the revocation is its own fact with its own clock.

### A judgment provider may never hold a grant

This one fails at issue time rather than at decision time, because it is constitutional rather than configurable.

```
$ wi authority issue --subject some-model --subject-kind judgment_provider \
    --capability claim.accept --scope workspace --issuer antonio

WI_AUTHORITY_DENIED: a judgment_provider may never hold a capability grant
    constraint: C008
  repair:
    - a judgment provider returns values; it does not decide, approve or sign
```

There is no flag that permits it and no phrasing of a request that produces it. A judgment provider returns a value. It is never an author, a contributor, a co-signer or a decision-maker, and the constraint engine checks the whole workspace for grants that would violate it (C008) on every run.

### Delegation is monotonic

A child grant may narrow its parent in capability, in scope and in lifetime. It may never widen any of the three, and the check happens at issue time rather than being detected at use time.

**Narrowing is accepted.** `claim.accept.wording_only` sits below `claim.accept`:

```
$ wi authority delegate --subject deputy --capability claim.accept.wording_only \
    --scope workspace --issuer antonio --parent e322307b-… --expires 2029-01-01T00:00:00+00:00

delegated 6cc24680-0ad0-535c-9e9b-d853f7f8a783
  deputy -> claim.accept.wording_only in scope workspace
  narrowed from e322307b-57f3-5158-8108-67c315933eb2; a child grant can never widen its parent
```

**Widening in capability is refused.** `canon.modify` is not below `claim.accept`:

```
$ wi authority delegate --subject deputy --capability canon.modify \
    --scope workspace --issuer antonio --parent e322307b-… --expires 2029-01-01T00:00:00+00:00

WI_GRANT_SCOPE_EXCEEDED: the delegated capability exceeds the parent grant
    child: canon.modify
    parent: claim.accept
  repair:
    - delegate a capability at or below claim.accept
```

**Outliving the parent is refused.** The parent expires in 2030; the child asked for 2040:

```
$ wi authority delegate --subject deputy2 --capability claim.accept.wording_only \
    --scope workspace --issuer antonio --parent e322307b-… --expires 2040-01-01T00:00:00+00:00

WI_GRANT_SCOPE_EXCEEDED: the delegated grant outlives its parent
    child_expires_at: 2040-01-01T00:00:00+00:00
    parent_expires_at: 2030-01-01T00:00:00+00:00
  repair:
    - set an expiry at or before 2030-01-01T00:00:00+00:00
```

Without lifetime monotonicity, a two-week grant delegates a ten-year one and the expiry that made the parent safe is gone. It is the least obvious of the three and the one most often left out.

### Authority follows the delta, not the diff

The capability a change requires is computed from what the edit did to meaning:

```
$ wi propose --node notice --type meaning.obligation --payload shall.json \
    --why "counsel asked for shall" --actor antonio

PROPOSED on legal

  03cdf351-222b-5ec9-ac0a-92211adeae88
    node      notice
    delta     certainty_strengthened, legal_force_strengthened
    requires  obligation.create
    bound to  sha256:2dd7e0aa26385c3ceb6d9e46cb444ee479e234128bb6d57382ce09aea1023be4
```

`should` → `shall` is five characters and a different legal instrument. An actor holding `claim.accept` cannot accept it:

```
$ wi decide 03cdf351-… --accept --actor antonio

WI_AUTHORITY_DENIED: antonio holds no grant covering obligation.create
    holds: ['claim.accept']
    required_capability: obligation.create
```

Meanwhile a genuine reordering — same modality, same subject, same bound actor, new sentence shape — classifies as `wording_only`:

```
$ wi propose --node notice --type meaning.obligation --payload reworded.json \
    --why "reorder the clause for readability" --actor antonio

PROPOSED on legal

  f745e85e-7f6c-58d7-826b-cf02b9d1deeb
    node      notice
    delta     wording_only
    requires  claim.accept
```

That is a conclusion the comparison reached over typed state, never an assumption it started from. And when an edit carries several delta classes at once, the required capability is the **strongest** of them — a rewrite that changes wording and a number is a number change, and it does not become a wording change because most of the diff was cosmetic.

---

## What is specified and does not run

This section is a feature of the release. A version that ships an architecture and describes it as though the architecture were features has committed the exact failure the project exists to catch, one level up. Law C applies to this document as strictly as to anything it governs.

**Shipping in 6.0.0:** the v4 deterministic floor, unchanged. The v5 graph, anchors, staleness, semantic diff, tests and proof-carrying release, unchanged. The sixteen new commands `canon` through `why`, listed above with real output.

**Specified, normatively described in [`references/v6/`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/README.md), and executing nowhere:**

| Not executable | Status |
|---|---|
| A compiled Rust core and its WASM build | There is no compiled core, no daemon and no single-binary distribution. `scripts/wi.py` is the canonical core and it is stdlib Python |
| Compiler backends | Meaning does not compile to `.docx`, PDF, EPUB, slides or subtitles. The v5 Markdown and HTML renderers are all that exist |
| Render source maps and the reverse-proposal path | The mechanism that makes a rendering unwritable — parse an edit in a built artifact back to a semantic delta and emit it as a proposal — is designed and does not run. Law M's enforcement is specified |
| The judgment tier | No provider ships. Paraphrase entailment is evaluated by nothing. Where doctrine describes what a provider must record, it binds a future implementation rather than reporting one |
| Sandboxed ingestion adapters and the WASM plugin host | `pdf_region`, `sheet_range`, `image_region`, `audio_time`, `video_time` and `data_pointer` anchors are specified. `text_span` is the one anchor kind that runs |
| External signing — Sigstore, C2PA, PROV export | Specified. A capsule declares `signature` in `declared_omissions` rather than implying it was checked |
| Semantic remotes, signed graph deltas, federation | Specified. `wi capsule` produces and verifies a portable proof closure on a local filesystem; everything about moving one between organizations is design |
| Watch mode | Specified |
| The Workbench desktop app, REST v6, MCP v6 | Specified. [`services/api/`](https://github.com/antonio0720/writing-intelligence/blob/main/services/api/) remains the v3 craft surface and does not expose the v5 or v6 verification tier — that is Law K, not an oversight |
| Interval arithmetic on contradiction detection | `wi as-of` runs. The interval-intersection contradiction detector Law N describes is specified |

**"Specified" means designed and normatively described in this repository, and not executable anywhere.** It is not a roadmap tease. It is the honest label on a contract that binds a future implementation, written in advance so the first implementation does not get to define the terms.

Five of the twenty graph constraints report `--` rather than `ok` for exactly this reason — C009, C010, C011, C016 and C019 depend on subsystems that do not ship, and each names its reason on every run. `wi doctor` reports the live unavailable map on any machine.

---

## The distribution split

**v6 ships as two bundles.**

| Bundle | Contents | Files |
|---|---|---|
| `writing-intelligence.skill` | The runtime — `SKILL.md`, `scripts/wi.py`, the v4/v5/v6 doctrine, the schemas, the agents, the docs, and the regression fixtures that prove the verifier works | 150 |
| `writing-intelligence-craft.skill` | The craft library — 27 genre packs, 10 voiceprints, 19 compiler references, 7 anti-pattern and 6 positive-pattern detectors, 6 diagnostics, 2 academic references, plus its own `SKILL.md` and `LICENSE` | 79 |

**A skill bundle may contain at most 200 files.** That is not a style preference and not a soft budget. **A bundle over the ceiling does not degrade — it does not load.** The upload is rejected outright, which would turn every install instruction in this repository into a false claim, on the surface where a reader has the least ability to check.

The v5 payload was 182 files with 18 to spare. v6 adds 24 doctrine documents, 20 schemas and a regression suite. The combined payload is 227. There was no version of this release that shipped as one bundle, and the arithmetic was not close.

Given that, there were two honest options: cut something, or split. Cutting the craft library would have been the quiet choice and the wrong one — the 11 passes, the genre packs and the voiceprints are the reason the writing is good, and the governance layer exists to protect writing that is worth protecting. Splitting the runtime from the library keeps both under the ceiling with real headroom, and the build enforces the limit rather than trusting anybody to remember it.

**This is not a downgrade and the runtime is not a stub.** The full craft doctrine is summarized inside `SKILL.md` and governs whether or not the second bundle is installed. What the craft bundle adds is the *corpus* — the packs, the measured voiceprints, the detector inventories — which is reference material a `git clone` away rather than in context.

**Install both.** They share one doctrine and one author, and the runtime cites the library rather than duplicating it.

---

## Verify this release

Do not take any of the above on faith. That is the entire point of the version.

**1. The core loads and reports its version.**

```bash
python3 scripts/wi.py --version        # wi 6.0.0
```

**2. The v4 adversarial floor still holds.**

```bash
bash tests/v4/test_wi.sh
```

```
PASS injection detected
PASS gate BLOCK
PASS statuses
```

Three passes means the verifier still catches a prompt injection, a fabricated citation, an inflated figure and a reshaped quotation. Unchanged since v4 and still asserted on every build.

**3. The v5 core — 32 assertions.**

```bash
bash tests/v5/test_wi5.sh
```

Ends in `v5 regression complete`. Every assertion has a negative twin: the tampered bundle is rejected *and* rejected for the right reason; the concept registry accepts the governing figure *and* fails on the forbidden alias; the changed sentence is classified *and* the unchanged sentences are left alone; the bundle is byte-reproducible across two builds, because otherwise a published checksum means nothing.

**4. The v6 core — 70 assertions.**

```bash
bash tests/v6/test_wi6.sh
```

Ends in `v6 regression complete`. The same rule applies and it matters more here, because **the v6 layer exists to refuse things**. An unauthorized acceptance, a stale approval, a merge that would invent a number nobody asserted, a capsule whose bytes moved. A suite that only checked the happy path would stay green with every one of those refusals deleted — and a green suite that survives the removal of the control it claims to test is worse than no suite, because it certifies nothing while looking like assurance.

So [`tests/v6/test_wi6.sh`](https://github.com/antonio0720/writing-intelligence/blob/main/tests/v6/test_wi6.sh) checks that each refusal actually fires, with the correct error code:

- acceptance without a grant is refused, and the refusal names `WI_AUTHORITY_DENIED`
- an expired grant authorizes nothing (`WI_AUTHORITY_EXPIRED`) — a different code from having none
- a grant out of scope authorizes nothing (`WI_GRANT_SCOPE_EXCEEDED`)
- a revoked grant authorizes nothing (`WI_AUTHORITY_REVOKED`)
- a judgment provider cannot be granted authority at all
- a delegation that widens capability, or outlives its parent, is refused at issue time
- a decision on a moved target is refused (`WI_DECISION_STALE`) and explains it will not reattach
- simulation does not move the branch root — asserted by comparing the root before and after
- a proposal does not move the branch root either
- the merge preserves both quantities and **specific averaged values are absent from the output**
- a tampered capsule is rejected, and never prints `VERDICT VERIFIED`
- the constraint engine emits no aggregate score

**5. What your machine can and cannot do.**

```bash
python3 scripts/wi.py doctor
```

```
Writing Intelligence 6.0.0 — capability report

python            3.11.15
schema            5.0.0
canonicalization  wi-json-v1
network           disabled

Deterministic checks available (11):
  source.digest
  source.quarantine
  anchor.integrity
  quote.verbatim
  numeric.value
  date.range
  entity.presence
  citation.resolution
  graph.reference_integrity
  release.closure
  release.artifact_digest

Evidence anchor types available: text_span

Not available here — and therefore never reported as done:
  audio_time             adapter specified, not executable in this build
  external_signing       Sigstore and C2PA paths are specified, not executable
  image_region           adapter specified, not executable in this build
  paraphrase_entailment  no judgment provider is configured
  pdf_region             adapter specified, not executable in this build
  sheet_range            adapter specified, not executable in this build
  video_time             adapter specified, not executable in this build

This report is Law C as protocol: a surface states what it cannot do
rather than degrading quietly into looking like it did it.
```

**6. The bundle checksums.**

```bash
shasum -a 256 -c writing-intelligence.skill.sha256
shasum -a 256 -c writing-intelligence-craft.skill.sha256
```

The build normalizes file order and mtimes, so the same tree produces the same bytes and CI fails if two builds of one tree differ. Without that, a published checksum is a number with no meaning attached.

**7. A `.wiab` verified offline, by somebody who was never in the room.**

```bash
python3 wi.py verify-release delta.wiab
```

Two files carried into a room with no network: `wi.py` and the bundle. Every `PASS` line is a recomputation rather than a lookup — the verifier does not read a field saying the digests matched, it computes them again and compares. Change one number inside the sealed artifact and it reports `WI_RELEASE_TAMPERED` and exits `2`. The v5 suite proves that failure on every run.

CI runs the v4 suite on Python 3.8, 3.11, 3.12 and 3.13, on Linux and macOS, **with no dependencies installed on purpose**, and asserts the PASS *count* separately from the exit code — an exit code cannot tell you the script stopped early and skipped checks it never ran. It also runs a mutation check: it disables the artifact-digest assertion and requires the suite to go red. A suite that stays green when you break the control it tests was never testing anything.

---

## Compatibility

**Nothing from v4 or v5 changed.**

- **v4 fixtures and ledgers.** `preserve`, `scan-sources`, `extract-claims`, `verify` and `gate` take the same arguments and produce the same verdict words. A v4 sentence ledger is still valid input to `verify` and `gate`, forever. There is no converter and none is needed.
- **v5 fixtures, workspaces and graphs.** The v5 suite is unchanged at 32 assertions and passes against the v6 core. `wi ingest`, `wi atomize`, `wi anchor`, `wi impact`, `wi diff --semantic`, `wi explain`, `wi test`, `wi graph`, `wi bundle` and `wi verify-release` behave identically.
- **Digests.** The v5 canonicalization is unchanged and `wi doctor` still reports `canonicalization wi-json-v1`. The v6 state digest is **domain-separated** from the v5 digest, so a byte-identical payload hashes differently as a v5 object and a v6 object. That is deliberate: without domain separation the same bytes would be ambiguously readable as both, which is the kind of ambiguity that becomes a security property later.
- **Error codes.** Every v5 code means what it meant. v6 adds `WI_AUTHORITY_DENIED`, `WI_AUTHORITY_EXPIRED`, `WI_AUTHORITY_REVOKED`, `WI_GRANT_SCOPE_EXCEEDED`, `WI_DECISION_STALE`, `WI_PROPOSAL_STALE`, `WI_SEMANTIC_CONFLICT`, `WI_TRANSACTION_CONFLICT` and `WI_POLICY_REJECTED`. Nothing was renamed or repurposed.
- **`.wiab` bundles.** The release bundle format is unchanged and v5 bundles verify against a v6 core. The v6 capsule is a **different artifact** with a different extension (`.wic`) and a different job — a `.wiab` is a whole release, a `.wic` is a selectively-disclosed proof of part of one.
- **Exit codes.** `gate --exit-code` still returns 0 RELEASE, 1 HOLD, 2 BLOCK. A refused v6 transition exits `2` as well, and names the code. That is the same number the gate uses for BLOCK, deliberately — a refused transition is a blocking condition, not a usage error, and CI that treats 2 as "stop" needs no change.

---

## Upgrading

**The upgrade is `git pull`.** There is no schema migration, no config file to write, no re-authoring, and no migration command — because no migration is required, and a command that exists and does nothing is worse than one that does not exist.

**What happens when a v6 core opens a v5 workspace.** The v6 tables are created lazily, on first use. Nothing that v5 attested to is rewritten, re-hashed or re-keyed. Your object store, your source versions, your anchors, your verification records and your existing `.wiab` bundles are untouched, and a v5 command run against that workspace produces exactly what it produced before.

Running `wi branch list` in a workspace that has never seen v6 creates the semantic layer and reports one commit:

```
BRANCHES
  * main                     b20ead41dcfa     0 nodes  initialize the v6 semantic layer
```

Zero nodes, because the v6 semantic graph starts empty. The v5 authorship graph beneath it is unaffected — `wi graph` still reports what it reported.

**Adopt in this order, which is the order it pays off:**

1. **`wi authority issue`** for yourself. One grant, workspace scope, an expiry you will actually renew. Until you do, every decision is refused, which is correct and is the first thing that will surprise you.
2. **`wi propose` → `wi simulate` → `wi decide` → `wi commit`** on one consequential change. Four commands where you used to have none. Step two is where it stops being ceremony.
3. **`wi branch`** the first time somebody else needs to work on the same document, and **`wi merge`** when they are done.
4. **`wi obligations`** before a release, to see what the typed state says must be proved rather than what a checklist says.
5. **`wi capsule`** when a funder, regulator or partner needs proof of one claim and may not see the rest.

**What will surprise you first**, in the order it usually does: an acceptance is refused because nobody has issued you a grant; a proposal you wrote yesterday is refused today because the target moved; a merge stops on a number instead of completing. All three are the system working. The third one is the reason it exists.

Full path, including what a migration must do before a core swap: [`references/v6/MIGRATION_V5_TO_V6.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/MIGRATION_V5_TO_V6.md). Further back: [`docs/MIGRATION_v4_to_v5.md`](https://github.com/antonio0720/writing-intelligence/blob/main/docs/MIGRATION_v4_to_v5.md).

---

## What it refuses to do

Refusals, not unbuilt features. They do not move. Full reasoning: [`references/v6/NON_GOALS.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/NON_GOALS.md)

- **Hidden auto-merge of consequential state.** There is no configuration option that enables automatic semantic resolution, and requests for one are refused permanently. If meaning conflicts, the conflict is preserved.
- **Autonomy does not create authority.** There is no accrual, no reputation score and no promotion path. A process that has behaved well for a year holds exactly what its grant says it holds.
- **Federation does not create trust.** A remote's `verified` becomes a local `verified` only when this workspace re-derives it from the evidence. That is why federation is specified rather than shipped with a trust-on-first-use default.
- **Time travel does not rewrite.** A correction appends. There is no compaction pass that drops superseded knowledge, and there will not be one.
- **Selective disclosure does not weaken proof.** A redacted capsule proves less, and says so, in the artifact, in a field named `does_not_prove`.
- **Renderer-side facts.** A renderer that needs new meaning emits a proposal and stops. It does not invent a sentence to satisfy a layout.
- **Source generation.** It will never construct a citation. There is no code path in which a well-formed anchor can be produced for a source that was never ingested.
- **Truth verification.** It verifies support within the sources supplied. It cannot tell you the source is right, and every output that could have hidden that says so instead.
- **Detector evasion.** Anti-slop is a craft objective — prose that does not pattern-match to machine writing because it is genuinely better built. It is not a laundering service, and a system built to produce a machine-checkable account of how a document came to exist cannot also be a system for concealing it.
- **Absolute quality scores.** There is no overall health gauge, no percentage on the constraint engine, and no blended number that would have to average across reliability types that are not commensurable.

---

## Honest limits

- **Paraphrase is still not verified.** No judgment provider ships. A well-paraphrased claim with no verbatim span and no co-located span reads `needs_source`. Every command that could have used a judgment says so on its own output.
- **Six of seven anchor kinds do not run.** A PDF, spreadsheet, image, audio file or video is not anchorable today. `wi doctor` names each with its reason.
- **The rendering boundary is a rule, not a lock.** Law M says an edit in a built artifact is a proposal. The round-trip parser that would enforce it is specified. Today the discipline holds because you are working in the graph, not because the file system stops you.
- **Five of twenty constraints cannot be evaluated** in a workspace with no v6 release closure, no render source maps and no declared protected spans. They report `--` with a reason rather than `ok`.
- **`services/api/` is still the v3 craft kernel.** The verification tier has exactly one implementation and stays that way — two implementations of `verified` disagree on the fifth edge case, in the surface with fewer tests, on the document that mattered.

---

## Install

Full capability matrix: [`docs/INSTALL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/docs/INSTALL.md)

**Terminal agents that load skills from a directory** — the fullest surface. Clone the repository into your agent's skills directory; the exact path for each one is in [`docs/INSTALL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/docs/INSTALL.md).

```bash
git clone https://github.com/antonio0720/writing-intelligence \
  <your-skills-directory>/writing-intelligence
```

**Hosted skill surfaces** — download the bundle and upload it through the surface's own skills setting.

```bash
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence.skill
shasum -a 256 writing-intelligence.skill
```

Any surface with a filesystem and a shell gets the whole deterministic core. A surface with neither still gets the craft kernel, and says so rather than pretending the checks ran.

**CLI only — no model, no dependencies, air-gapped.**

```bash
curl -O https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/scripts/wi.py
python3 wi.py --version        # wi 6.0.0
python3 wi.py doctor
```

**CI** — nothing to install beyond Python:

```yaml
- name: Writing gate
  run: |
    python3 scripts/wi.py ingest sources/
    python3 scripts/wi.py atomize drafts/narrative.md
    python3 scripts/wi.py anchor .wi/graph/ledger-*.json sources/
    python3 scripts/wi.py constraints
    python3 scripts/wi.py gate .wi/graph/ledger-*.json --exit-code
```

**Air-gapped review** — carry two files into the room and run `python3 wi.py verify-release delta.wiab`, or `python3 wi.py capsule verify claim.wic`.

---

## Full detail

[`CHANGELOG.md`](https://github.com/antonio0720/writing-intelligence/blob/main/CHANGELOG.md) · [`ROADMAP.md`](https://github.com/antonio0720/writing-intelligence/blob/main/ROADMAP.md) · [`USER_GUIDE.md`](https://github.com/antonio0720/writing-intelligence/blob/main/USER_GUIDE.md) · [`CHEATSHEET.md`](https://github.com/antonio0720/writing-intelligence/blob/main/CHEATSHEET.md) · [`docs/INSTALL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/docs/INSTALL.md) · [`CONTRIBUTING.md`](https://github.com/antonio0720/writing-intelligence/blob/main/CONTRIBUTING.md)

The v6 doctrine — twenty-four documents: [`references/v6/README.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/README.md) · [`CONSTITUTION.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/CONSTITUTION.md) · [`EXECUTABLE_MEANING.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/EXECUTABLE_MEANING.md) · [`AUTHORITY_MODEL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/AUTHORITY_MODEL.md) · [`SEMANTIC_VERSION_CONTROL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/SEMANTIC_VERSION_CONTROL.md) · [`COUNTERFACTUAL_SIMULATION.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/COUNTERFACTUAL_SIMULATION.md) · [`MERGE_PROTOCOL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/MERGE_PROTOCOL.md) · [`BITEMPORAL_STATE.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/BITEMPORAL_STATE.md) · [`PROOF_OBLIGATIONS.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/PROOF_OBLIGATIONS.md) · [`PROOF_CAPSULES.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/PROOF_CAPSULES.md) · [`SECURITY_MODEL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/SECURITY_MODEL.md) · [`NON_GOALS.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v6/NON_GOALS.md)

The v6 schemas — twenty documents: [`schemas/v6/README.md`](https://github.com/antonio0720/writing-intelligence/blob/main/schemas/v6/README.md)

Still authoritative for their own subject matter: [`references/v5/README.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v5/README.md) · [`references/v4/ACCOUNTABILITY_LAYER.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v4/ACCOUNTABILITY_LAYER.md)

---

*v1.0 proved AI-sounding prose can be defeated by compilation instead of cosmetic cleanup. v2.0 proved fiction can be engineered as a living architecture. v3.0 proved authorship can be governed without being flattened. v4.0 proved it can be held accountable. v5.0 proved the account can be carried, checked and re-checked by someone who was never in the room. **v6.0 proves the account can survive the document continuing to change — under many hands, over years, with every transition naming what it did, who was allowed to do it, and what it cost.***

Free. MIT. Free forever — no account, no server, no key, no telemetry, and nothing that stops working if the author does. **Antonio T. Smith Jr.** — Founder & CEO, [Density6 LLC](https://densitysix.com).
