# Writing Intelligence v3.0 — Benchmarks

The benchmark harness proves the system improves over time and prevents regression before releases.

## Structure

```
benchmarks/
├── README.md                        # This file
├── benchmark_manifest.yaml          # Canonical case list, weights, gates
├── runbook.md                       # How to run benchmarks
├── cases/                           # 60 cases across 12 categories
│   ├── ai_slop_rewrite.md
│   ├── business_strategy_memo.md
│   ├── founder_manifesto.md
│   ├── investor_update.md
│   ├── sales_email.md
│   ├── sermon_excerpt.md
│   ├── academic_paragraph.md
│   ├── grant_narrative.md
│   ├── government_brief.md
│   ├── fiction_scene.md
│   ├── dialogue_scene.md
│   └── longform_continuity_audit.md
└── reports/                         # Historical benchmark results
```

## Release Gates

A release cannot ship until aggregate benchmark results pass:

| Gate | Requirement |
|---|---|
| Score improvement | v3 must beat the prior version's baseline by **≥ 5 points on ≥ 70%** of benchmark cases |
| No regression | No case may drop more than **3 points** without documented reason |
| Evidence safety | **100%** of fabricated-source traps must be flagged |
| Voice preservation | Voice drift cases identify correct drift direction **≥ 80%** of the time |
| Genre collision | Mixed-genre tasks produce a declared `genre_stack` with `collision_resolutions` |
| Narrative audit | Story cases identify dead props, flat setting, missing payoff |
| Output packaging | Every benchmark produces a valid `delivery_bundle` |

## How to Add a Benchmark Case

Each case must include:

- `case_id` (category prefix + number, e.g., `GRANT-04`)
- `input` (the prompt or source draft)
- `task_contract` (the intake contract JSON)
- `expected_failure_detection` (which anti-patterns / failures the system should catch)
- `expected_score_range` (min, max)
- `v2_baseline_output` (with score)
- `v3_expected_output` (with score)
- `scoring_notes` (rubrics that apply, weights)
- `regression_hazards` (known ways this case could regress)

Add the case to the appropriate file in `cases/` and register it in `benchmark_manifest.yaml`.

## Public Benchmark Report Format

Every release ships a benchmark report:

```text
Writing Intelligence v3.0 Benchmark Report
==========================================
Cases run: 60
Passed: 56
Conditional pass: 4
Failed: 0
Average score delta vs. v2: +8.7

Top improvements:
- Epistemic ledger (+12.4 on high-stakes cases)
- Grant pack (+9.1)
- Voice drift detection (+11.0)
- Storyworld memory (+8.3)

Regression risks:
- Longer runtime per piece (+25% avg)
- More verbose audit output

Release decision: PASS
```

## Author

Antonio T. Smith Jr. / Density6 LLC
