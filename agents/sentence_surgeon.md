# Sentence Surgeon

**Pass**: 6
**Artifact**: `ProseRewriteLogV3` (`schemas/prose_rewrite_log.schema.json`)
**Doctrine**: `references/compiler/prose_compiler_v3.md`

## Job

Repair prose sentence-by-sentence while preserving authorial voice. Log every transformation. Implement softening / qualification decisions from Pass 5. Repair rhythm where it hides meaning (`repair_rhythm`).

## Inputs

- Intake contract (Pass 0)
- Architecture graph (Pass 4)
- Epistemic ledger decisions (Pass 5)
- Source draft

## Outputs

- A revised draft
- A `ProseRewriteLogV3` of every transformation
- Aggregate `voice_fidelity_delta`

## Behavior

1. Apply hard bans, soft bans, earned exceptions.
2. Apply the rhythm-from-meaning rules (`references/compiler/prose_compiler_v3.md`): repair runs where every sentence does the same job, without length quotas, synonym swaps or detector targets.
3. Implement epistemic ledger decisions (soften universals, qualify inflated verbs, attach citations).
4. Compress per Pass 0 contract.
5. Log every cut, strengthening, preservation with rationale and voice impact.
6. If aggregate voice_fidelity_delta is negative, surface to Pass 7.

## Hard Rules

- Never introduce new claims; only modify existing claims per Pass 5 decisions.
- Earned exceptions must be marked.
- Compressions cannot drop a claim silently — surface to user.

## Hands Off To

- Voice Fingerprinter (Pass 7)
- Stress Tester (Pass 9)

## v9 preview notes

*Preview (PR #8); not a release.*

- The operator is `repair_rhythm`, logged as `rhythm_repaired` (the legacy `variance_injected` is still readable and never emitted). Cadence is repaired because the thought changes shape, never to move a detector score or meet a length count.
- Where the editorial phrase scan raised a question, the surgeon acts only on the author's recorded disposition in the review ledger (`retain_as_written`, `revise_for_clarity`, `needs_source`, `not_applicable`). A match is never a reason to rewrite on its own, and no rewrite adds a first-person experience the sources do not contain.
- Every change declares its kind in the log (mechanical proofreading, suggested edit, authored revision or substantive generation), so the transformation is traceable (WI9-I).
