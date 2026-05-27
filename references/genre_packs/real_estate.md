# Genre Pack — Real Estate

**v3.0 Domain Pack Schema**

## Purpose

Produce listing copy, investor memos, buyer education, neighborhood briefs, and broker / agent communication — specific, local, evidence-led, never generic.

## When to Use

- MLS listing descriptions
- Property brochures
- Investor memos for income properties
- Buyer education / first-time-buyer guides
- Neighborhood market briefs
- Open-house follow-up emails
- Listing presentations

## When Not to Use

- Pure marketing for an agent brand (use `sales.md` + `landing_page`)
- Legal disclosures (use `legal_positioning.md`)
- Mortgage / financing copy (use `loan_officer.md`)

## Audience Model

- A buyer with 30 seconds on a listing page
- An investor running cap-rate math
- A first-time buyer afraid to ask
- A relocating family scanning neighborhoods
- A seller comparing agent listings

## Required Evidence

- Square footage (verified)
- Property tax (current year)
- HOA fees (if applicable)
- School district (current rating, source named)
- Comparable sales (last 12 months)
- Cap rate / NOI / GRM (for investor copy)
- Days on market (for context)

## Forbidden Claims

- "Charming" / "cozy" / "must see" / "won't last" (clichés that signal nothing)
- "Best in the neighborhood" without evidence
- "Investor's dream" without numbers
- Income projections stated as facts
- "Up-and-coming" neighborhood without verifiable signals
- Implied fair-housing violations

## Voice Weighting

- Specificity: **25** (highest)
- Evidence: **20**
- Local knowledge: **15**
- Compression: **15**
- Compliance (fair housing, disclosure): **15**
- Warmth: **10**

## Structure Templates

### MLS Listing (150-300 words)

1. **One-sentence headline** — the move that makes this property singular
2. **What the buyer walks into** — concrete sensory detail
3. **The bones** — bedrooms, baths, square footage, lot
4. **The kitchen / living / primary suite** — what's specific, not generic
5. **The outdoor** — yard, view, garage, parking
6. **The neighborhood** — walk score, schools, commute, comps
7. **The numbers** — taxes, HOA, recent updates
8. **The CTA** — open house, agent, scheduling

### Investor Memo

1. **The deal** (1 sentence)
2. **The asset** (address, type, units, square footage)
3. **The numbers** (purchase price, NOI, cap rate, debt service, cash-on-cash)
4. **The risk** (vacancy assumption, deferred maintenance, market exposure)
5. **The thesis** (why this beats the next deal)
6. **The ask** (capital, timing)

### Open-House Follow-Up Email

1. **Thanks for coming**
2. **What you said you'd want to see again**
3. **The numbers refreshed**
4. **The next step**
5. **Your direct line**

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Specificity (every claim concrete) | 25 |
| Evidence (taxes, comps, square footage verified) | 20 |
| Local knowledge | 15 |
| Compliance (fair housing safe, disclosure clean) | 15 |
| Compression | 15 |
| CTA clarity | 10 |

## Failure Modes

- "Charming" / "cozy" / "must see" → automatic flag, replace with specific
- "Best schools" without rating + source → score capped
- Income projection stated as fact (vs. "projected" or "modeled") → liability risk
- "Up-and-coming neighborhood" → fair housing flag
- Cap rate without rent roll → investor distrust

## Before/After Example

**Before**:

> Charming 3BR/2BA in a wonderful neighborhood! This must-see home features a cozy living room, a beautiful kitchen, and a fantastic backyard. Won't last long! Schedule your showing today!

**After**:

> Renovated 1937 craftsman, 3BR / 2BA / 1,640 sqft on a 0.18-acre corner lot. Walnut floors original. Kitchen rebuilt 2023 (gas range, quartz, soft-close). Primary suite second floor, dual closets, en-suite. Detached garage + 220V EV outlet. Walk score 78; 6-minute walk to Compton Park; District 5 (rated 8/10 GreatSchools 2026). Taxes $4,820 / yr. No HOA. Last comp on this block: 412 Walnut, sold $487K, March 2026. Open Sunday 1-3 PM. Listing agent: [name + phone].

## Stress Tests

- Replace every adjective with a measurement. Survivors stay.
- For "best" / "biggest" / "newest" — name the source.
- For "investor's dream" — name the cap rate.
- For neighborhood claims — name the data.

## Delivery Formats

- MLS-ready (within field char limits)
- Brochure (print or PDF)
- Email (open-house follow-up, buyer outreach)
- Investor memo (1-2 page PDF)
- Companion social post

## Schema Hooks

- `intake_contract.arena: caption` (listing) or `memo` (investor)
- `epistemic_ledger`: every quantitative claim must have source
- `corpus_map`: comps and tax data must be `verified` with timestamp

## Benchmark Cases

`REALEST-01` through `REALEST-05` in `benchmarks/cases/real_estate.md`.

## Stack Combinations

- + `email.md`: follow-up
- + `social_media.md`: cross-channel
- + `small_business_operator.md`: solo agent brand
- + `legal_positioning.md`: disclosures
