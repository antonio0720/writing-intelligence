# Epistemic Ledger Engine — Pass 5

**Purpose**: Make factual integrity a first-class system primitive. Every major claim in a v3.0 draft is classified, sourced, and accountable.

**Schema**: `schemas/epistemic_ledger.schema.json` (`EpistemicLedgerV3`)

**Agent**: Evidence Prosecutor (`agents/evidence_prosecutor.md`)

---

## Why an Epistemic Ledger

v2.0 had an epistemic integrity *layer*. v3.0 has an epistemic *ledger*. The distinction matters: a layer applies pressure; a ledger keeps receipts. Pass 5 produces a structured record that can be audited, cited, contested, and improved.

**Mandatory domains** (Pass 5 cannot be skipped):

- Academic (paper, thesis, dissertation, peer review)
- Medical (clinical, diagnostic, pharmaceutical)
- Legal (filing, brief, memorandum, contract, public statement)
- Government (federal, agency, regulatory, statutory)
- Grant / NOFO / RFP
- Financial (SEC, investor, board, audit, disclosure)
- Any high-stakes public release

For other domains, Pass 5 is recommended but skippable.

---

## Claim Classes

Every major sentence is one of:

| Class | Definition | Required Support |
|---|---|---|
| `observed_fact` | The writer witnessed or measured it | None beyond plausibility |
| `sourced_fact` | Attributed to a named, verifiable source | Citation |
| `inference` | Logical derivation from stated facts | Premises identified |
| `synthesis` | Combination of multiple sources into a new claim | Source chain identified |
| `recommendation` | Prescriptive statement | Basis stated |
| `rhetoric` | Persuasive move not grounded in evidence | Marked as such; cannot masquerade as fact |

---

## Source Status

| Status | Meaning | Effect |
|---|---|---|
| `verified` | Independently confirmed | Pass |
| `user-provided` | User asserted it | Pass with attribution |
| `assumed` | Reasonable assumption | Pass with qualification |
| `inferred` | Derived | Pass with chain |
| `missing` | Required but absent | Surfaces to user |
| `unsafe` | Wrong, stale, or risky | **Blocks delivery** |

---

## Universal Quantifier Discipline

Sentences containing: *all, every, none, never, always, must, cannot, every single, no one, anybody, everybody, everywhere, nowhere* — require evidence or qualification. The ledger flags them with `universal_quantifier_flag: true`.

The Evidence Prosecutor offers three resolutions:

1. **Evidence** — find sourced fact that supports the universal
2. **Soften** — replace with *most, many, often, typically, rarely, in our experience*
3. **Scope** — narrow to a specific domain or population

---

## Inflated Verb Discipline

Sentences containing: *revolutionize, transform, redefine, disrupt, reimagine, unleash, harness, supercharge, optimize, leverage, empower, enable, unlock* — require concrete backing. Flag with `inflated_verb_flag: true`. Replace with concrete action verb + measurable outcome.

---

## Fabrication Blockers (Hard Rules)

The Evidence Prosecutor refuses delivery if any of:

- Invented citation, statistic, quote, study, court case, scripture reference
- Invented institutional name, person name, date, monetary figure
- Invented historical event
- Misattributed quote (real quote, wrong attribution)
- "Studies show…" without identifying the studies
- "Experts agree…" without identifying experts
- "Research has demonstrated…" without identifying research

Each becomes `fabrication_risk: blocked` and `delivery_block: true` on the ledger. Pass 10 will not produce a delivery bundle until resolved.

---

## Decisions

Every flagged claim gets a decision:

- `cite_added` — source found, citation inserted
- `claim_softened` — universal quantifier or inflated verb replaced with scoped equivalent
- `claim_removed` — couldn't support; removed
- `claim_qualified` — kept with explicit hedge
- `user_clarification_required` — needs user input

Decisions are logged. The user can audit every move.

---

## Example Ledger

```json
{
  "task_id": "wi_v3_2026_000003",
  "version": "3.0.0",
  "claims": [
    {
      "claim_id": "c1",
      "text": "Our model produces measurable outcomes per dollar.",
      "location": {"paragraph": 2, "sentence": 1},
      "class": "sourced_fact",
      "source_status": "verified",
      "sources": ["fy25_results_report"],
      "fabrication_risk": "none"
    },
    {
      "claim_id": "c2",
      "text": "Every other model in this field fails.",
      "location": {"paragraph": 2, "sentence": 3},
      "class": "rhetoric",
      "source_status": "missing",
      "universal_quantifier_flag": true,
      "fabrication_risk": "high"
    }
  ],
  "summary": {
    "total_claims": 14,
    "verified_pct": 71.4,
    "sourced_pct": 14.3,
    "inference_pct": 7.1,
    "rhetoric_pct": 7.1,
    "missing_source_count": 1,
    "unsafe_count": 0,
    "fabrication_blocks": 0
  },
  "delivery_block": false,
  "decisions": [
    {"claim_id": "c2", "action": "claim_softened", "rationale": "Universal quantifier replaced with scoped comparative."}
  ]
}
```

---

## Scoring

The Epistemic Integrity scorecard (100 points) measures:

| Dimension | Points |
|---|---|
| Claim classification coverage | 20 |
| Source verification rate | 20 |
| Citation honesty | 20 |
| Universal-quantifier discipline | 15 |
| Inflated-verb discipline | 10 |
| Hallucination resistance | 15 |

Any `delivery_block` caps the score at 30 until resolved.

---

## Definition of Done

The Evidence Prosecutor emits a ledger that:

- Validates against `epistemic_ledger.schema.json`
- Classifies every major claim
- Resolves every fabrication risk
- Surfaces every `unsafe` source
- Sets `delivery_block` correctly
- Records every decision with rationale

If any of the above fails, Pass 5 has not completed.
