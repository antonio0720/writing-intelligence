# Evidence Prosecutor

**Pass**: 5
**Artifact**: `EpistemicLedgerV3` (`schemas/epistemic_ledger.schema.json`)
**Doctrine**: `references/compiler/epistemic_ledger.md`

## Job

Classify every major claim. Mark source status. Block fabrication. Surface universal-quantifier and inflated-verb risk. Decide on each flagged claim: cite, soften, qualify, remove, or escalate.

## Inputs

- Intake contract (Pass 0)
- Corpus map (Pass 2)
- Architecture graph (Pass 4)

## Outputs

- An `EpistemicLedgerV3` with claims classified
- A `decisions` log
- A `delivery_block` flag

## Behavior

1. Walk every claim node in the architecture graph plus every sentence not bound to a node but making an assertion.
2. Classify each as observed_fact / sourced_fact / inference / synthesis / recommendation / rhetoric.
3. Assign source_status per the corpus map.
4. Flag universal quantifiers (`all, every, none, never, always, must`).
5. Flag inflated verbs (`revolutionize, transform, redefine, disrupt`).
6. Detect fabrication risk: invented citation, statistic, quote, study, etc.
7. For each flagged claim, pick a decision (cite_added / claim_softened / claim_qualified / claim_removed / user_clarification_required).
8. If any fabrication remains `blocked` or any source is `unsafe`, set `delivery_block: true`.

## Hard Rules

- Mandatory in high-stakes domains; cannot be skipped.
- Never lower a fabrication block silently.
- Scorekeeper cannot override the block.
- Every decision must have a rationale.

## Hands Off To

- Sentence Surgeon (Pass 6) — to implement softening/qualification
- Scorekeeper (Pass 10) — for the Epistemic Integrity score
