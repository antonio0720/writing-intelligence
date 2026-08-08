# Tier Requirements

What each tier requires, and what evidence satisfies it.

## How these lines are marked

The v6 constraint engine reports `pass`, `fail` or `not_evaluated`. There is no fourth status and no aggregate score, because a constraint that quietly did nothing is worse than a constraint that is missing.

Certification uses the same three marks and the same rule.

| Mark | Meaning |
|---|---|
| `ok` | The reviewer looked at the named artifact and the check held. |
| `FAIL` | The reviewer looked at the named artifact and the check did not hold. |
| `--` | Not evaluated. Always carries the reason. |

A tier is awarded when every line for that tier is `ok`. A single `FAIL` blocks the tier. A `--` blocks the tier too — an unevaluated check is not a passed one — but it is reported separately from a `FAIL`, because "the candidate did not submit a high-stakes deliverable" and "the candidate fabricated a citation" call for different responses.

There is no total, no percentage and no weighting. A candidate cannot average past a fabricated number.

The one exception is the craft floor. Prose quality is scored 0–100 against `references/diagnostics/scorecard.md`, because prose quality is a judgement with a rubric and pretending otherwise would be its own dishonesty. Everything about the runtime is pass/fail, because a merge either fabricated a value or it did not.

---

## Apprentice

Craft. Every line is marked against the three submitted deliverables.

| # | Check | Artifact the reviewer opens | `ok` when |
|---|---|---|---|
| A1 | Intake contract exists per deliverable | The submitted contract | Mode, intent, audience, voice and genre stack are all declared, not inferred |
| A2 | Kernel passes are traceable | Pass artifacts | The artifacts a pass emits are present for the passes the candidate claims to have run |
| A3 | Voiceprint declared | Contract + final draft | A named voiceprint is declared before drafting, not attributed afterwards |
| A4 | Scorecard present and independent | Candidate scorecard vs reviewer re-score | Reviewer's total is within 7 points of the candidate's, per deliverable |
| A5 | Craft floor | Reviewer's scorecard | 80 or above on all three deliverables |
| A6 | No automatic fail condition | Reviewer's scorecard | None of the eight conditions in `references/diagnostics/scorecard.md` fires |
| A7 | No fabricated citation, statistic, quote or study | Final drafts and sources | Every named source resolves to something that exists and says what the draft says it says |
| A8 | Output modes | Delivery bundles | At least two distinct output modes across the three deliverables |
| A9 | Arena breadth | The three contracts | At least two distinct arenas |
| A10 | Doctrine literacy | Cover note | The candidate states the v6 Law in their own words and names one thing it forbids |

**A4 is the honesty check.** A candidate whose self-score is consistently 12 points above the reviewer's is not being audited for prose; they are being audited for scoring, and that is the thing this tier is measuring. Direction matters: a candidate who scores themselves low is not failed by A4. Inflation is.

**A7 is not scored.** It is pass/fail because a fabricated statistic does not average out.

---

## Operator

Accountability and proof. Lines are marked against the submitted portfolio and one live workspace exercise.

| # | Check | Artifact the reviewer opens | `ok` when |
|---|---|---|---|
| O1 | Apprentice confirmed | Roster | Awarded |
| O2 | Portfolio depth | Five or more deliverables | Each meets A5 and A6 |
| O3 | Arena breadth | The contracts | Three or more distinct arenas, at least one high-stakes |
| O4 | Claim status is earned | The atom ledger | Every atom marked `supported` carries an anchor that resolves against an ingested source |
| O5 | `needs_source` was resolved, not routed around | Ledger before and after, plus `wi diff --semantic` output | At least one atom moved from `needs_source` to `supported` by anchoring. The reviewer checks the semantic diff for the alternative: the claim being softened until it stopped needing a source |
| O6 | Gate reaches RELEASE honestly | `wi gate --exit-code` on the submitted workspace | Exit 0, at a mode of `standard` or stricter, with no `--allow-block` anywhere in the build |
| O7 | Bundle verifies offline | The `.wiab` and `wi verify-release` | Verifies on the reviewer's machine with no model and no network |
| O8 | Bundle scope is honest | `wi verify-release --json` | What the bundle proves matches what the cover note says it proves |
| O9 | Simulation read correctly | A `wi simulate` report on a workspace the candidate did not build | The candidate names the repair frontier and the provably-unaffected count, and both match the report |
| O10 | No over-repair | The candidate's repair plan | The plan touches the frontier and does not touch the provably-unaffected set |
| O11 | Simulation understood as non-mutating | Cover note | The candidate states that `wi simulate` committed nothing, and can say how they know |

**O9 and O10 are the v6 additions and they are the point of the tier.** The pre-v6 Operator proved they could produce a defensible document. The v6 Operator proves they can respond to a change *proportionally*. Re-verifying the whole document after one source moves is the behaviour that gets integrity tooling switched off, because it makes every small correction expensive. The repair frontier exists to make the response cheap and exact.

**O10 fails in one direction only.** Under-repair is caught by O9. O10 catches the candidate who repairs nodes the report proved were unaffected — which looks like diligence and is the reason nobody trusts the report next time.

---

## Steward

Authority. Lines are marked against a workspace the candidate operates during the audit.

| # | Check | Artifact the reviewer opens | `ok` when |
|---|---|---|---|
| S1 | Operator confirmed | Roster | Awarded |
| S2 | Holds a grant issued by someone else | `wi authority list` | The grant's issuer is not the subject |
| S3 | Exercises it correctly | The transaction record | The accepted decision names the grant it ran under |
| S4 | Delegates narrower | `wi authority delegate` output and the parent grant | The child grant is narrower in capability, scope or window. Equal or broader is `FAIL` |
| S5 | Explains the narrowing | Application thread | The candidate says which axis they narrowed and why that axis |
| S6 | Recognises a correct refusal | The refusal output | An expired grant is presented, the transition is attempted, and the candidate reports the refusal as correct behaviour |
| S7 | Distinguishes the refusals | Application thread | The candidate distinguishes absent authority from expired authority and names what each tells an operator to do next |
| S8 | Produces a real conflict | `wi merge` exiting non-zero | Two branches changed the same logical id from a common base, and the merge preserved both values |
| S9 | Refuses the middle value | The merge output | No value appears in the output that is absent from base, ours and theirs |
| S10 | Explains the refusal | Application thread | The candidate names the logical id, the conflict kind, and why the engine did not choose |
| S11 | Resolves by taking a side | `wi conflicts --resolve --take` output | Resolution names the grant it ran under |
| S12 | Records why | The resolution record and the application thread | A stated reason that a third party could disagree with. "Took theirs" alone is `FAIL` |

**S6 is the line most likely to be failed by a strong candidate.** Someone fluent in the craft tiers reads `WI_AUTHORITY_EXPIRED` as an obstacle and looks for the flag that removes it. There is no such flag. The tier is testing whether the candidate treats a refusal as information about the state of the world rather than as a defect in the tool.

**S9 is marked on absence.** The reviewer searches the merge output for a value that appears in neither input. Finding one is `FAIL`, and it is the only line here that can fail silently — an averaged number reads as a decision.

**S12 exists because a resolution without a reason is indistinguishable from a coin toss six months later**, and the record will attest that an authorized human decided it either way.

---

## Architect

Extension.

| # | Check | Artifact the reviewer opens | `ok` when |
|---|---|---|---|
| X1 | Steward confirmed, or Operator with a recorded waiver | Roster and application thread | Awarded, or the waiver is stated in the thread by the maintainer |
| X2 | Accepted RFC | The RFC and its thread | Accepted per `CONTRIBUTING.md` |
| X3 | Merged contribution | The PR | Merged: a genre pack, voiceprint, schema, constraint or capability |
| X4 | Negative fixture present | The test file | A test exists whose subject is the new mechanism |
| X5 | Negative fixture can fail | The suite, run by the reviewer with the mechanism defeated | The suite goes red |
| X6 | Contribution does not weaken an existing guarantee | The full suite before and after | No previously red-capable assertion becomes unfailable |
| X7 | Documented limits | The contribution's own docs | The contribution states what it does not check |

**X5 is the tier.** Everything above it is procedure. The reviewer deletes the mechanism — comments out the check, removes the constraint from the list, drops the field from the schema — and runs the suite. Green means the contribution shipped a check that cannot fail, and a check that cannot fail is decoration.

**X6 catches the subtler version.** A contribution can pass X5 and still make an older assertion vacuous: widening an allowlist so a negative test now matches nothing, or renaming a field so a `hasnt` assertion greps for a string that is no longer emitted. The reviewer diffs which assertions are still capable of failing, not just which ones pass.

---

## Recertification

None. A certificate records what was true of a submitted portfolio on a date.

This is a limit, not a feature, and it is stated in `README.md` under "What certification cannot tell you". An Apprentice certificate from a v3 portfolio says nothing about v6 practice. Tiers are not withdrawn when the runtime changes, because withdrawing them would imply the roster tracks current competence, and it does not.
