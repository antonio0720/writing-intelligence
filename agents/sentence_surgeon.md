# Sentence Surgeon

**Pass**: 6
**Artifact**: `ProseRewriteLogV3` (`schemas/prose_rewrite_log.schema.json`)
**Doctrine**: `references/compiler/prose_compiler_v3.md`

## Job

Repair prose sentence-by-sentence while preserving authorial voice. Log every transformation. Implement softening / qualification decisions from Pass 5. Inject variance.

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
2. Run the variance injection rules (sentence-length variance, transition variety, vocabulary tier).
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
