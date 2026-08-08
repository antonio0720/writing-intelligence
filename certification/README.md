# Certification

Writing Intelligence v6.0.0 is a runtime. Someone operates it, under authority, and the decisions they record become permanent state. Certification is an optional way to show you can do that without corrupting the record.

Certification is **not required to use Writing Intelligence**. The skill is free and open under MIT. It costs nothing, it gates nothing, and nothing in the tool checks for it.

## The hard rule

**No tier grants any authority inside anyone's workspace.**

Authority in this system is a capability grant: a subject, a capability, a scope and a window, issued by someone who already holds it, recorded in the graph, revocable, and expiring. `wi authority issue` is the only thing that creates one. `wi authority check` is the only thing that reads one. A certificate does not create a grant, cannot be presented in place of one, and is invisible to the runtime.

This is a doctrinal position, not modesty. A certificate is a claim about a person. This project's entire argument is that a claim you cannot point at has not been verified — and a person is not an artifact. So certification points at artifacts instead. It says: *these specific outputs exist, and they held up when someone else re-derived them.* Whether the person who produced them should hold `claim.accept.quantity_change` in your workspace is your decision, issued by your issuer, recorded in your graph, and revocable by you.

## The failure mode this design exists to prevent

Certification that certifies nothing is the worst artifact this project could ship. It would be a scored claim with no evidence pointer — the exact thing the runtime refuses to render as `supported`.

Three ways a certification scheme becomes that, and the countermeasure taken here:

| Failure | How it happens | Countermeasure |
|---|---|---|
| Unfalsifiable rubric | Lines like "demonstrates system thinking" cannot be marked wrong | Every rubric line in `exam_rubrics.md` names an artifact and a check. A line a reviewer cannot fail by looking at a file is not a rubric line. |
| Aggregate score hides a hole | A candidate averages 87 while fabricating one number | Runtime checks are pass / fail / `--`, never summed. `wi constraints` emits no aggregate score and neither does this. |
| Certificate drifts from the tool | Tiers name capabilities the CLI never had | Every command, flag, capability string and error code named in these files was read out of `scripts/wi.py` or `tests/v6/test_wi6.sh` before it was written down. |

## The four tiers

| Tier | What it demonstrates | The artifact that proves it |
|---|---|---|
| **Apprentice** | Craft. The 11-pass kernel, a declared voiceprint, anti-slop discipline, on real deliverables. | Three deliverables with intake contracts and scorecards that survive re-scoring. |
| **Operator** | Accountability. Claim status is earned, not asserted; a release is proof-carrying; a simulation is read correctly and acted on narrowly. | A `.wiab` bundle that verifies offline, plus a repair frontier that was worked rather than bypassed. |
| **Steward** | Authority. Grants held and issued within scope; conflicts resolved by taking a side and recording why; refusals explained. | A conflict resolution record naming a grant id and a reason, and a merge refusal the candidate can account for. |
| **Architect** | Extension. A new check, pack, schema or capability — with the negative fixture that proves the new check can fail. | A merged contribution whose test suite goes red when the mechanism is removed. |

Tiers are cumulative. Steward assumes Operator; Operator assumes Apprentice.

## Why Steward is a separate tier and not part of Operator

This was the open question in the design. Both readings are defensible.

**The case for folding it into Operator.** Authority is accountability with a signature on it. An Operator already resolves `needs_source`, already produces a bundle that someone else can verify, already understands that a claim without an anchor does not get to be `supported`. Adding a fourth tier adds surface for a reviewer pool of one to maintain, and certification schemes that proliferate tiers stop meaning anything.

**The case for separating it.** The failure modes are different in kind, and so are the artifacts.

An Operator who mis-scores a deliverable ships weaker prose. That is recoverable by rewriting.

A Steward who resolves a conflict wrongly writes a value into permanent state *under a grant*, and the record then attests that an authorized human decided it. `wi conflicts --resolve --take ours|theirs` is the one command in the runtime that converts an unresolved disagreement into an authoritative value. Constraint C015 — `semantic-conflict-cannot-be-rendered-as-resolved` — exists because that transition is the one place a fabrication would be indistinguishable from a decision after the fact.

The second competence is also different: a Steward has to explain why the tool *refused*. `wi merge` exiting 2 with a preserved conflict is the system working. Someone who reads that as a defect will reach for the middle value, and the middle value is the thing Law Q forbids. Explaining a refusal is a different skill from producing a good document, and nothing in the Operator tier tests it.

**Decision: separate tier.** The rule that settles it comes from the hard rule above — certification points at artifacts. The artifact that proves Steward is a conflict record carrying a grant id and a stated reason. No Operator artifact contains one. Where the artifact differs, the tier differs.

## Apprentice

Craft. Unchanged in substance from v3; restated because the surrounding runtime changed.

**Requirements**

- Read `SKILL.md`, `README.md`, `USER_GUIDE.md`.
- Three real deliverables produced with the 11-pass kernel.
- Each submitted with its intake contract, its scorecard, and the pass artifacts it generated.
- Each scores 80 or above on the 100-point scorecard in `references/diagnostics/scorecard.md`, and triggers none of the eight automatic fail conditions.
- At least two distinct arenas.

**How.** Open an issue with the `apprentice-application` label, linking three deliverables that a reviewer can read.

**What the tier does not claim.** That the work is good. An 80 is a B. It claims the candidate can run the kernel and score honestly.

## Operator

Accountability and proof.

**Requirements**

- Apprentice confirmed.
- Five or more shipped deliverables across three or more arenas, at least one high-stakes (grant, legal, medical, academic, government, financial).
- One workspace where `wi gate --exit-code` reaches RELEASE, with the ledger showing that at least one atom moved off `needs_source` by anchoring it to a source — not by downgrading the claim's wording until it no longer needed one.
- One `.wiab` bundle built with `wi bundle` that a reviewer verifies offline with `wi verify-release`, on a machine with no model and no network.
- **New for v6:** given a `wi simulate` report on a workspace the candidate did not build, the candidate identifies the repair frontier and the provably-unaffected set, and repairs only the frontier.

**How.** Open an issue with the `operator-application` label.

**The failure mode this tier catches.** Re-verifying everything after a source changes. It looks diligent and it is the reason people switch the tooling off — a report that flags the whole document is a report nobody reads twice. `wi simulate` and `wi impact` exist to make the affected set small and exact. An Operator who ignores that number has the runtime and is still working like it is not there.

**The second failure mode.** Reaching RELEASE by softening. Deleting the number is a valid repair, and it is not the same repair as finding the source; `wi diff --semantic` classifies the difference and the reviewer looks at that classification.

## Steward

Authority.

**Requirements**

- Operator confirmed.
- Hold at least one grant issued by someone else, exercise it, and show the transaction that names it.
- Issue a narrower grant by delegation with `wi authority delegate` — narrower in capability, scope or window — and explain in the application why the narrowing is the one they chose.
- Let a grant expire, attempt the transition, and submit the refusal. `WI_AUTHORITY_EXPIRED` is a correct outcome; a Steward candidate who reports it as a bug has failed the tier.
- Produce a genuine semantic conflict, resolve it with `wi conflicts --resolve --take`, and record why that side was taken. The resolution record must name the grant the resolution ran under.
- Explain a `wi merge` refusal in writing: which logical id, which conflict kind, why the engine preserved both values instead of choosing.

**How.** Open an issue with the `steward-application` label.

**What this tier is for.** This is the tier that can be trusted with `wi conflicts --resolve` in a workspace whose record other people rely on.

**What it does not grant.** See the hard rule. It does not issue the candidate a grant anywhere.

## Architect

Extension.

**Requirements**

- Steward confirmed, or Operator confirmed with a maintainer waiver recorded in the application thread.
- One accepted RFC through the process in `CONTRIBUTING.md`.
- One merged contribution: a genre pack, a voiceprint, a schema, a constraint, or a capability.
- **The negative fixture.** The contribution ships with a test that fails when the new mechanism is removed or weakened. A check that cannot fail is decoration, and the project does not merge decoration.

**How.** By invitation, after the contribution is merged.

**How the negative fixture is graded.** The reviewer deletes or defeats the mechanism and runs the suite. If it stays green, the tier is not awarded and the contribution is reopened. This mirrors how the project's own suite is written: `tests/v6/test_wi6.sh` asserts on absences — that a merge output does not contain `12100`, that a tampered capsule never prints `VERDICT VERIFIED` — because those are the assertions that go red when the guarantee stops holding.

## What certification cannot tell you

Stated plainly, because a credential that hides its limits is the failure mode above.

- It is a snapshot. It says what was true of a portfolio on a date. There is no recertification and no expiry, so an old certificate says nothing about current practice.
- It measures submitted work. A candidate chooses what to submit.
- The reviewer pool is one person. Calibration across reviewers has not been demonstrated because there is only one reviewer.
- No tier tests behaviour under commercial pressure, which is where evidence discipline usually fails.
- Apprentice and Operator craft scores are human judgements against a rubric, not measurements. The scorecard's own protocol says it: *a score is only as honest as the scorer's willingness to give low numbers.*

## What certification is not

- Not a paid product. There is no fee, at any tier.
- Not a gate to using the skill. Use it freely, forever.
- Not exclusive to professionals. A student can be an Apprentice.
- Not an Anthropic credential. Anthropic does not endorse this skill. It is community-run, authored by Antonio T. Smith Jr.
- Not a substitute for a capability grant. Repeating this because it is the one that will be tested.

## Files

- `certification/operator_levels.md` — what each tier requires, and what evidence satisfies it.
- `certification/exam_rubrics.md` — the audit procedure and the pass/fail lines a reviewer marks.

`certification/operators.md` is referenced by both files as the roster of awarded tiers. It does not exist yet; nobody has been certified. It will be created when the first tier is awarded, and not before, because an empty roster file implies a scheme that has run.

## Author

Antonio T. Smith Jr. / Density6 LLC
