# Judgment, Independent Readers and Deliberate Deviations

**Status:** human workflow specified; machine-checkable report and reader study schema included. No actual human study conducted.

## Three non-commuting evaluations

1. **Structural/mechanical:** referents resolve, known-at and valid-at intervals are coherent, histories are reconstructable, no dependency cycle exists, no ambiguous result is silently coerced. This can be computed from a trusted export.
2. **Editorial interpretation:** characters are credible, the want/need tension feels earned, choices produce consequences, and an exception to a craft guideline works. Human editor records manuscript spans, rationale and rival interpretations. This remains judgment, not “verified.”
3. **Reader reception:** blinded readers report what they understood, where their interest changed, what they felt, and whether they experienced closure. A study must keep raw disagreements; averaging does not manufacture unanimity.

A prose algorithm can perform #1 without establishing #2. A declared intention for #2 cannot substitute for #3. Even #3 is evidence about sampled readers, not universal quality.

## Calibration protocol

Recruit readers across the actual intended genre/audience, declare inclusion criteria and prior familiarity, blind them to the writer's intended quadrant and arc family, identify the exact manuscript revision/digest, collect responses independently, and retain verbatim confusion/attachment observations. Compare *false-positive* and *false-negative* diagnostics against independently coded spans; report sample counts and variation rather than unearned global accuracy percentages. Collect consent and avoid claiming reader anonymity when it has not been assured.

## Reader form (JSON schema)

`schemas/v8/arc_reader_review.schema.json` records `source_digest`, `protocol_id`, `reader_id`, blind status, observed time, understanding, attachment and ending satisfaction. This is a data-entry contract. The existence of a conforming JSON object is **not** verification of reader identity, independence, authenticity, or consent. The local publication gate therefore always returns `HOLD` even when a matching form exists.

## Override form (JSON schema)

`schemas/v8/arc_override.schema.json` captures author, reason, rule, source graph root, affected nodes, effective period and proposed status. The only admissible local `status` is **proposed**. Acceptance must pass through `wi propose → simulate → authority check → decide → commit` in the canonical core, including exact-source bindings, stale-state rejection and audit receipt. A user can override an artistic heuristic; cannot override a factual continuity contradiction by silently changing text.
