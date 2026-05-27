# Domain Pack Guide

How to build a new genre pack that meets the v3.0 standard.

## Why Domain Packs Matter

v3.0 has 26 genre packs. The 27th and beyond come from the community. Every new pack expands the system's reach — but only if it meets the doctrine.

## The 15-Section Domain Pack Schema

Every pack must include all 15 sections:

1. **Purpose** — what the pack accomplishes
2. **When to use** — concrete trigger conditions
3. **When not to use** — non-applicability rules
4. **Audience model** — who reads the output
5. **Required evidence** — what backs claims
6. **Forbidden claims** — what cannot appear
7. **Voice weighting** — how the pack tunes the voice dial
8. **Structure templates** — at least 1 canonical template
9. **Scoring adjustments** — per-rubric weights
10. **Failure modes** — what reviewers catch
11. **Before/after example** — at least one transformation
12. **Stress tests** — how to verify the pack worked
13. **Delivery formats** — output mode hooks
14. **Schema hooks** — intake contract + epistemic ledger expectations
15. **Benchmark cases** — at least 5 cases with target ranges

## How to Author

1. Pick the domain. Real users with real needs only.
2. Read three v3.0 packs as references: `grant_nofo.md`, `small_business_operator.md`, `church_leadership.md`.
3. Write the 15 sections.
4. Author 5 benchmark cases. Each must have v2-baseline score, v3-target score, and expected detections.
5. Update `references/diagnostics/genre_collision_matrix.md` with the new pack's collision dimensions.
6. Open an RFC per `governance/RFC_PROCESS.md`.
7. After RFC acceptance, open the PR.
8. PR cannot merge until the benchmark suite passes for the new pack.

## What Makes a Good Pack

- Specific audience (not "professionals")
- Concrete forbidden claims (not "avoid generic language")
- Measurable scoring adjustments (not "value voice")
- Real benchmark cases (not "we'll add them later")
- Real before/after (not "imagine if…")

## Common Failures

- Pack reads like a style guide, not an operational doctrine
- Forbidden claims are wishful thinking ("don't be boring")
- Scoring weights add to more than 100
- Benchmark cases lack v2 baselines
- Voice weighting is qualitative ("warm but professional")
- Collision matrix not updated

## Examples to Read

- `references/genre_packs/grant_nofo.md` — high-stakes, evidence-heavy
- `references/genre_packs/small_business_operator.md` — voice-first, mass-market
- `references/genre_packs/loan_officer.md` — compliance-driven
- `references/genre_packs/church_leadership.md` — mission identity + pastoral warmth
- `references/genre_packs/social_media.md` — platform-native distribution

## Author

Antonio T. Smith Jr. / Density6 LLC
