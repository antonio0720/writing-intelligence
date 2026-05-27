# Genre Pack — Grant Writing / NOFO / RFP Response

**v3.0 Domain Pack Schema** — high-value, complex, evidence-heavy.

## Purpose

Convert a program, an organization, or a project into a funded proposal that satisfies the funder's RFP, withstands evidence review, and demonstrates measurable outcomes per dollar.

## When to Use

- Federal NOFO / RFP responses
- State and city grant applications
- Foundation grants
- Corporate philanthropy applications
- Multi-funder capital readiness packages
- Renewal proposals
- Capacity-building funding requests

## When Not to Use

- Pitch decks (use `pitch_deck.md`)
- Sponsorship asks (use `sales.md` + `email.md`)
- Pure storytelling fundraising appeals (use `email.md` + `church_leadership.md`)

## Audience Model

- The funder's program officer (primary reader)
- The review committee (secondary reader, often anonymous)
- A skeptical compliance reviewer (tertiary, gatekeeper)

Funders are not buyers. They are evidence-driven stewards of public, foundation, or institutional capital. Trust > excitement.

## Required Evidence

- Audited financial outcomes (prior period)
- Beneficiary counts with measurement methodology
- Independent evaluation results (if available)
- Letters of support, MOUs, partnership commitments
- Logic model (inputs → activities → outputs → outcomes → impact)
- Budget narrative aligned with program narrative
- Risk register with mitigation plan
- Sustainability plan

## Forbidden Claims

- Unsourced numbers ("we serve thousands" without a count)
- "Unique" or "first of its kind" without evidence
- "Transformative" / "revolutionary" / "groundbreaking" — inflated verbs flagged
- Universal beneficiary claims ("everyone in the community")
- Future outcomes stated as facts
- Comparison to other programs by name (without their consent)
- Outcomes not tied to the funder's stated priorities

## Voice Weighting

- Evidence discipline: **20** (highest)
- Compliance: **20** (highest)
- Compression: **15** (every word earns its place — funders read fast)
- Warmth: **10** (mission identity allowed; pity rejected)
- Authority posture: **70-80** (confident, not dramatic)
- Cadence: medium-formal, BLUF-led

## Structure Templates

### Standard NOFO Response

1. **Project Summary** (BLUF — 1 page)
2. **Statement of Need** (problem with evidence)
3. **Project Description** (intervention with logic model)
4. **Outcomes & Evaluation** (measurable, methodology stated)
5. **Organizational Capacity** (track record with evidence)
6. **Budget Narrative** (every line tied to program activity)
7. **Sustainability Plan**
8. **Appendices** (financials, partner letters, evaluation tools)

### Concept Paper / LOI

1. **The Problem** (specific, scoped, evidenced)
2. **The Move** (the intervention)
3. **The Lift** (measurable outcomes)
4. **The Receipt** (prior evidence)
5. **The Ask** (specific, calibrated to funder size)

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Compliance with RFP structure | 25 |
| Evidence-to-claim ratio | 25 |
| Logic model coherence | 15 |
| Budget-narrative alignment | 15 |
| Outcome measurability | 10 |
| Voice and warmth (mission identity) | 10 |

## Failure Modes

- RFP structure not matched 1:1 → automatic rejection
- Inflated verbs in outcome statements → score capped
- Missing logic model → score capped
- Budget detached from program narrative → reviewer flags
- Universal beneficiary claims → red flag, retraction needed
- "Transformative" stated without measurable transformation → reviewer cynicism

## Before/After Example

**Before** (typical):

> Our revolutionary approach to youth empowerment is transforming the lives of countless young people across the region. We are the leading provider of innovative programming and our impact speaks for itself.

**After** (v3.0):

> In FY25, our after-school program served 312 youth (ages 11-17) in three Delta-region counties. Independent evaluation by Mid-South Research Group documented 89% program retention at 12 months and a 0.74 GPA improvement among regularly attending participants. The proposed FY26-FY27 expansion adds two sites and 240 new participants while preserving the current per-participant cost of $2,140.

## Stress Tests

- Replace "transformative" with the measurable transformation. If you can't, cut it.
- Replace "countless" with the count. If you can't get the count, the program doesn't measure.
- For every claim, identify the source. If no source exists, claim is unsupported.
- Run the budget narrative against the program narrative. Every program activity needs a budget line. Every budget line needs a program activity.

## Delivery Formats

- Full proposal (Word / PDF)
- Cover letter (1 page)
- Executive summary (1 page)
- Logic model (1 page)
- Budget narrative (3-5 pages)
- Compliance matrix (table)

## Schema Hooks

- `intake_contract.arena: grant_response`
- `intake_contract.high_stakes: true`
- `epistemic_ledger`: mandatory; every numeric claim and beneficiary count must have source
- `delivery_bundle.channel_constraints`: per RFP requirements

## Benchmark Cases

Cases `GRANT-01` through `GRANT-05` in `benchmarks/cases/grant_narrative.md`.

## Stack Combinations

- + `church_leadership.md`: faith-based community programs
- + `government_brief.md`: federal NOFO responses
- + `small_business_operator.md`: SBA and community development capital
- + `medical_writing.md`: health services grants
- + `academic.md`: research grants (NIH, NSF)
