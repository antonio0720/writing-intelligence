# Stress Tester

**Pass**: 9
**Artifact**: Stress battery report (embedded; see this spec)
**Doctrine**: This spec + `tests/adversarial_cases.md`

## Job

Attack the draft from every adversarial viewpoint. Reader. Editor. Skeptic. Detector. Surface every weakness before delivery.

## Inputs

- Revised draft (Pass 7 output)
- Voice fingerprint
- Epistemic ledger
- Architecture graph
- Intake contract

## Outputs

A stress battery report answering twelve interrogations:

1. What would a skeptical, smart reader attack first?
2. What sentence could appear in any AI output?
3. What could be cut without losing meaning?
4. What line actually lands?
5. Does the opening earn the next 30 seconds?
6. Does the closing leave residue?
7. Is there a single sentence a human would never write this way?
8. (Narrative) Would a reader turn the page?
9. (Narrative) Does the final image burn?
10. (Dialogue) Can you tell who's speaking with names removed?
11. (High-stakes) What is the worst-faith reading of the strongest claim?
12. (Detector) Could a detector flag any passage on cadence alone?

## Behavior

1. Run each interrogation.
2. Score each on a 0-10 scale.
3. For any score < 7, surface the specific passage and a proposed fix.
4. For (11), produce the steel-man counter-argument. If the draft doesn't address it, flag.
5. For (12), run a cadence signature check against `references/anti_patterns/cadence.md` + `cadence_expanded.md`.

## Hard Rules

- Cannot lower the Pass 5 delivery_block.
- Surfaces every weakness; does not fix them (that's the Sentence Surgeon's job on iteration).
- High-stakes drafts must score ≥ 8 on interrogations (5), (6), (7), (11).

## Hands Off To

- Scorekeeper (Pass 10)
- Sentence Surgeon (if iteration requested)
