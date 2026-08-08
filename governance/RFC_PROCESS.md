# RFC Process — Writing Intelligence

The Request for Comments process governs substantive additions to Writing Intelligence.
The goal is to keep contribution velocity high while protecting the doctrine from drift.

Since v6 the system carries state that outlives the release: digests other people hold,
grants that authorize acts, decisions bound to exact states, capsules verified on machines
this project cannot reach. An RFC that touches that layer carries obligations an RFC about
a genre pack does not, and [section 3](#3-additional-obligations-for-the-meaning-runtime)
states them.

---

## 1. When you need an RFC

You need an RFC for:

- New genre packs
- New voiceprints
- New schemas, or schema-breaking changes in any family
- New rewrite operators
- New scoring systems or scoring-rubric changes
- New agents
- Changes to the 11-pass kernel
- **Changes to any of the eighteen laws A–R** (`references/v6/CONSTITUTION.md`)
- **Any change that moves a digest** — see [`VERSIONING.md`](VERSIONING.md)
- **Any addition to a closed vocabulary** — a capability, a delta class, a conflict kind,
  an actor kind, a scope kind, a graph constraint, a reliability basis
- **Any change to how required authority is derived from a semantic delta**
- **Any change to which comparisons produce a merge conflict, or what kind**
- Any change to the meaning of `verified`, `stale`, `BLOCK`, `permitted` or
  `source quarantine`

You do **not** need an RFC for:

- Bug fixes
- Typo fixes
- Doc clarifications
- Additional benchmark cases inside existing categories
- Additional examples inside existing folders

If you are unsure, open an issue and ask. The process exists to make contribution welcome
and high-quality, not to gatekeep.

---

## 2. Lifecycle

1. **Draft.** Open a GitHub issue with the `rfc` label and the title `RFC: <one-line summary>`.
2. **Specification.** Use the template in section 4. Be specific.
3. **Comment period.** Minimum 7 days. Maintainers and community discuss.
4. **Resolution.** Maintainer marks the issue `accepted`, `rejected` or `needs-revision`.
5. **Implementation.** An accepted RFC becomes a PR. The PR must link the RFC.
6. **Merge gates.** The PR must pass the gates in [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md)
   and ship its negative fixture.

---

## 3. Additional obligations for the meaning runtime

An RFC that touches the v6 layer answers five more questions. They are separate sections
in the template, not a paragraph, because each one is a different failure and a reviewer
needs to be able to find the one they are qualified to judge.

### 3.1 Which of the eighteen laws does this touch

Name them by letter, and say whether the RFC *implements*, *constrains* or *changes* each.

A law is changed by accretion far more often than by decision. Widening `verified` to cover
one more thing does not look like a breaking change in a diff — it looks like an improvement
to a sentence. Naming the law makes each widening cost something and leaves a record of who
paid.

An RFC that changes a law is MAJOR and maintainer-led. An RFC that implements one is
ordinary work.

### 3.2 What negative fixture proves the new check can fail

Every new check, constraint, refusal or gate ships with a fixture that **fails when the
implementation is disabled**, in the same PR, wired into the suite.

State in the RFC:

- what the fixture asserts
- which line of `scripts/wi.py` you disable to make it go red
- what the output looks like when it does

This is not a testing preference. The v6 layer exists to *refuse* things, so a suite that
only walks the happy path stays green with every refusal deleted — which is worse than no
suite, because it certifies nothing while looking like assurance. `tests/v6/test_wi6.sh`
is built on this pattern throughout: an unauthorized acceptance is refused *and* the
refusal names `WI_AUTHORITY_DENIED`; a conflicted merge stops *and* the specific averaged
values are absent from its output; a tampered capsule is rejected *and* never prints
`VERDICT VERIFIED`.

CI goes one step further and inverts two controls on every run, requiring the suite to go
red. An RFC that adds a control of comparable weight should say whether it belongs in that
set.

### 3.3 Does this add a capability string, and what delta class requires it

`V6_CAPABILITIES` is a closed vocabulary of sixteen. `wi authority issue` refuses anything
outside it, because a capability nothing checks is a string in a database.

If the RFC adds one, state:

- the exact dotted name, and where it sits in the containment hierarchy
  (`claim.accept` covers `claim.accept.*`)
- which delta classes map to it in `V6_DELTA_CAPABILITY`
- **the test for a seventeenth capability**: not whether it names something real, but
  whether any organization would grant one of a pair and withhold the other. If nobody
  would ever split them, they are one capability
- what happens to existing grants — a grant naming a capability that has been renamed is
  a grant nothing recognises, which is why renaming is MAJOR

If the RFC adds a delta class, state which capability it requires and why. Required
authority is the **strongest** capability across an edit's classes: a rewrite that changes
wording and a number is a number change, and it does not become a wording change because
most of the diff was cosmetic. An RFC that adds a class must not weaken that rule for its
own case.

### 3.4 Does this move a digest

Answer one of three, explicitly:

| Answer | Then |
|---|---|
| **No digest moves.** | Say how you know. `wi canon` on the fixture world before and after is the check |
| **A v6 state digest, a graph root or a capsule closure root moves.** | The RFC is MAJOR. It must state which object kinds move, what happens to artifacts already in circulation, and what this release cannot do for their holders |
| **A new digest domain is introduced.** | Name the domain tag. It must be distinct from `wi-state-v5`, `wi-state-v6`, `wi-closure-node-v6` and `wi-closure-empty-v6`, and it must be reproducible byte-for-byte by any future core |

Silence here is treated as an unanswered question, not as *no*. The failure this exists to
prevent is a capsule that reports `VERDICT TAMPERED` after an upgrade — the correct words
for the check that ran, and the wrong words for what happened, on a machine where nobody
can tell the difference.

### 3.5 What does this cost a reader who already has an artifact

Not what it costs to implement. What it costs somebody holding a `.wic`, a `.wiab`, a
decision record or a workspace produced before the change. If the answer is *nothing*, say
so and say why.

---

## 4. A merge resolution policy is rejected by default

**Law Q: semantic disagreement is preserved until resolved. An RFC proposing that a merge
resolve a semantic conflict automatically is rejected on submission.**

This is the one place in this document where the default is *no*. It is stated as a
default rather than a prohibition because the request is reasonable, will be made
repeatedly, and is easy to implement — *ours*, *theirs*, *newest wins*, *prefer the longer
text*, *prefer the branch with more approvals* are all defensible-sounding and all trivial.
An operator will ask for one by the second week.

The reason it is refused: in source code an automatic merge is checked downstream by a
compiler and a test suite, which object. **In meaning there is nothing downstream that
objects.** A scope that silently widened, an obligation that silently softened and a figure
that silently changed all produce a document that reads well and is wrong, and the change
is invisible in a character diff because it is small. Last-writer-wins is a correctness
policy nobody would choose if asked — it means whoever saved second was right, about a
question neither knew they were answering.

Averaging is worse than either. The mean of 11,240 and 12,400 is 11,820; round it and you
get "approximately 12,000", which reads beautifully, survives every review, and is a claim
neither branch asserted and no source supports. It would arrive wearing the authority of
a machine that checked things.

**An RFC in this area must argue against the law explicitly, not around it.** Specifically,
it must:

1. Quote Law Q and `references/v6/NON_GOALS.md` §10, and say which sentence it disputes.
2. Name the semantic dimension it wants resolved automatically — `quantity`, `unit`,
   `scope`, `time`, `entity`, `attribution`, `certainty`, `causality`, `definition`,
   `obligation`, `legal_force`, `canon`, `evidence` — and explain what downstream check
   would object if the resolution were wrong.
3. Show the fabricated output the current engine refuses to produce, and state what its
   proposal produces instead.
4. Explain why the friction it removes is not the feature. The two conflict lines a person
   reads are the two decisions somebody has to make, surfaced at the moment they are cheap.

An RFC that proposes a configuration flag, an opt-in, a policy setting, a strategy
parameter or a "power user mode" for the same behaviour is the same RFC and is refused on
the same terms. The absence of the flag is the feature.

**What is not refused, and is welcome:** work on the *composing* half. A merge that stopped
on everything would be a merge nobody runs, and it already composes cleanly on disjoint
dimensions — two editors, one adding a temporal bound and one correcting an attribution,
produce a merged state carrying both changes and no conflict, which no line-based tool can
do. Proposals that widen the provably-disjoint set, or that improve `wi conflicts` as a
surface a human reads, are ordinary RFCs.

The same standing default applies, for the same reason, to: any path that lets a model
produce a record typed `verified`; any path that constructs a citation; and any blended
quality score. `references/v6/NON_GOALS.md` and `references/v5/NON_GOALS.md` carry the
full list.

---

## 5. RFC template

```markdown
# RFC: <title>

**Author**: <github handle>
**Date**: YYYY-MM-DD
**Status**: draft | discussion | accepted | rejected | needs-revision
**Tracking issue**: #
**Touches the meaning runtime**: yes | no

## Summary

One paragraph describing what is being proposed.

## Motivation

Why does this need to exist? Who is asking for it? What problem does it solve?
What is the failure mode today?

## Detailed Design

What changes. Where. Why this design rather than alternatives.

If proposing a new genre pack: follow the Domain Pack Schema (15 sections) in
`docs/DOMAIN_PACK_GUIDE.md`.

If proposing a new voiceprint: follow the Voiceprint Schema in
`docs/VOICEPRINT_GUIDE.md`. Must include a measurable fingerprint, not only a
description.

If proposing a new schema or schema change: provide the JSON Schema and a
migration note. State whether the schema id or version is bound into a digest
preimage.

If proposing a new agent: declare the agent's job, artifact, schema,
dependencies and conflict-resolution rules.

If proposing a kernel change: explain why the existing kernel cannot handle
this.

---

## Meaning-runtime obligations

Delete this whole block only if **Touches the meaning runtime** is `no`.

### Laws touched

| Law | Implements / constrains / changes | Note |
|---|---|---|
| | | |

### Negative fixture

- What it asserts:
- Line to disable in `scripts/wi.py` to make it fail:
- Output when it fails:
- Belongs in the CI mutation set: yes | no

### Capability and delta impact

- New capability string(s):
- Delta class(es) that require it:
- The pair test — would any organization grant one and withhold the other:
- Effect on existing grants:

### Digest impact

- [ ] No digest moves. Evidence: `wi canon` on the fixture world, before and after
- [ ] A v6 state digest / graph root / capsule closure root moves (MAJOR)
- [ ] A new digest domain is introduced. Tag:

If a digest moves: which object kinds, what happens to artifacts already in
circulation, and what this release cannot do for their holders.

### Cost to an existing artifact holder

What this costs somebody holding a `.wic`, a `.wiab`, a decision record or a
workspace produced before the change. If nothing, say why.

---

## Alternatives Considered

What other designs were rejected and why.

## Drawbacks

What could go wrong. What this costs.

## Backwards Compatibility

Does this break anything? If yes, what is the migration path?

## Benchmark Requirement

Every RFC must propose at least one benchmark case demonstrating that the
addition improves measurable outcomes. The PR cannot merge until it passes.

## Documentation Requirement

What docs need to change. List them. Every new capability is marked
*executable in `scripts/wi.py`* or *specified* — "specified" means designed and
normatively described here and **not executable anywhere**.

## Open Questions

Things the author is not sure about and wants community input on.
```

---

## 6. Decision rights

**Maintainer (currently Antonio T. Smith Jr.) holds final decision on:**

- Kernel changes
- The eighteen laws A–R
- Canonical serialization, digest preimages and domain separation
- The meaning of the five protocol words
- Anything that would let a model produce a record typed `verified`
- License terms
- Public positioning

**Community and maintainer jointly decide:**

- New genre packs
- New voiceprints
- New schemas
- New agents
- New deterministic checks and graph constraints
- New members of a closed vocabulary that leave existing members untouched
- Benchmark cases

---

## 7. The spirit

Open source grows by attracting talented contributors. This governance exists to make
contribution welcome and high-quality, not to gatekeep.

Three laws bind every contribution:

- **The v3 Law** — if a rule cannot be applied, audited, scored, tested or explained, it
  is not a rule yet.
- **The v4 Law** — if a claim cannot be pointed at, it has not been verified, and fluent
  prose must never be allowed to look like checked prose.
- **The v6 Law** — no consequential state transition may become authoritative unless the
  system can identify the exact prior state, the proposed next state, the semantic delta
  between them, the dependency impact of that delta, the acting authority, the decision
  basis and the resulting proof closure.

The RFC process exists to keep all three alive.
