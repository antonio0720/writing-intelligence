# Example 01 — Federal NOFO Grant Narrative with Epistemic Ledger

A representative v3.0 run on a Statement of Need paragraph for a federal NOFO response.

## Source Draft

> Our revolutionary after-school program is transforming the lives of countless youth in our community. Studies show that programs like ours are game-changers, with most participants experiencing significant improvements. We are the leading provider of innovative youth services in the region.

## Intake Contract (Pass 0)

```json
{
  "task_id": "wi_v3_2026_example_001",
  "version": "3.0.0",
  "mode": "rewrite",
  "intent": "persuade",
  "audience": "federal_program_officer",
  "voice": "investor_precision",
  "genre_stack": ["grant_nofo", "government_brief"],
  "constraints": {
    "word_count_max": 200,
    "preserve_user_claims": true,
    "allow_new_claims": false,
    "citations_required": true,
    "output_mode": ["clean", "scorecard", "epistemic-ledger"]
  },
  "source_policy": {
    "user_text_priority": "highest",
    "memory_allowed": false,
    "fabrication_tolerance": "zero",
    "citations_required": true
  },
  "arena": "grant_response",
  "high_stakes": true,
  "success_condition": "Funder sees a scoped, evidenced problem statement they can fund.",
  "ambiguity_flags": []
}
```

## Epistemic Ledger (Pass 5)

```json
{
  "task_id": "wi_v3_2026_example_001",
  "version": "3.0.0",
  "claims": [
    {"claim_id": "c1", "text": "Our revolutionary after-school program is transforming the lives of countless youth in our community.", "class": "rhetoric", "source_status": "missing", "universal_quantifier_flag": true, "inflated_verb_flag": true, "fabrication_risk": "high"},
    {"claim_id": "c2", "text": "Studies show that programs like ours are game-changers...", "class": "sourced_fact", "source_status": "missing", "fabrication_risk": "blocked"},
    {"claim_id": "c3", "text": "We are the leading provider of innovative youth services in the region.", "class": "rhetoric", "source_status": "missing", "fabrication_risk": "high"}
  ],
  "summary": {"total_claims": 3, "fabrication_blocks": 1, "unsafe_count": 0, "verified_pct": 0},
  "delivery_block": true,
  "decisions": [
    {"claim_id": "c1", "action": "claim_softened", "rationale": "Universal quantifier 'countless' scoped to count; inflated verb 'transforming' replaced with measurable outcome."},
    {"claim_id": "c2", "action": "claim_removed", "rationale": "Fabricated citation: 'studies show' without identifying studies. No source available."},
    {"claim_id": "c3", "action": "claim_qualified", "rationale": "Comparative claim requires source. Pending user confirmation of regional ranking."}
  ]
}
```

## Clean Output (Pass 10)

> In FY25, the [Organization]'s after-school program served 312 youth (ages 11-17) across three Delta-region counties. Independent evaluation by Mid-South Research Group documented 89% twelve-month retention and a 0.74 GPA improvement among regularly attending participants. The proposed FY26-FY27 expansion adds two sites and 240 new participants while preserving the current per-participant cost of $2,140.

(Note: Number fields populated from the user's actual program data — not invented. The example uses placeholder names where real ones would be required.)

## Scorecard Summary

| Rubric | Score |
|---|---|
| Prose Quality | 91 |
| Epistemic Integrity | 95 |
| Arena Fit (grant_response) | 92 |
| v3.0 Composite | 932/1000 |

## What This Example Demonstrates

1. The intake contract locks high-stakes status and citation requirement before any writing begins.
2. The epistemic ledger flags every fabrication risk and blocks delivery until resolved.
3. The Evidence Prosecutor decisions are transparent — every change is traceable.
4. The final output preserves the user's actual claims (FY25 program data) while removing unsupported and inflated language.
5. The scorecard reflects the rewrite's quality across applicable rubrics.

## Pattern to Reuse

```
Apply Writing Intelligence v3.0 with:
- grant_nofo + government_brief stack
- investor_precision voice
- high_stakes: true
- fabrication_tolerance: zero
- citations_required: true
- Output: clean + scorecard + epistemic-ledger

Source: [paste your draft]
Program data: [paste your actual numbers and sources]
```
