# Genre Pack — Small Business Operator

**v3.0 Domain Pack Schema**

## Purpose

Produce copy for the operator at the kitchen table — the solopreneur, the local owner, the founder of a five-person team — that converts without sounding corporate, hedges without sounding scared, and respects the customer's intelligence.

## When to Use

- Service business landing pages
- Local business outreach
- Founder-to-customer email
- Sales pages for solo / small-team services
- Operator newsletters
- Hiring posts (solo founder hiring first / second / third person)
- "About" pages
- Investor / lender outreach for small business capital

## When Not to Use

- Enterprise B2B (use `sales.md` + `pitch_deck.md`)
- Pure marketing for an established brand (use `sales.md`)
- Personal brand / creator copy (use `social_media.md` + `linkedin_post`)

## Audience Model

- A potential customer who's been burned before
- A potential customer comparing 3-4 options
- A small business peer reading for ideas
- An investor / lender (small ticket, local capital)

## Required Evidence

- Real results (named customers when permitted)
- Real numbers (revenue, time-saved, jobs completed, customers served)
- Real geography (where the operator actually works)
- Real timeline (how long the business has been running)
- Real guarantee (what the operator will actually do if it fails)

## Forbidden Claims

- "Game-changing" / "industry-leading" / "revolutionary" (inflated verbs)
- "We provide the highest quality" without evidence
- "World-class" anything for a local business
- Composite customer stories presented as one
- "Trusted by thousands" without count
- "10x" / "100x" without numbers

## Voice Weighting

- Trust posture: **25** (highest)
- Specificity: **20**
- Compression: **15**
- Warmth: **15** (kitchen-table register, never corporate)
- Evidence: **15**
- CTA discipline: **10**

## Structure Templates

### Service Landing Page

1. **Hero** (what you do + who for + the move)
2. **The proof** (3-5 specific outcomes with numbers or names)
3. **The how** (your method, in plain language)
4. **The friction removal** (price, timeline, guarantee, what's NOT included)
5. **The objection** (the thing the customer is afraid to ask)
6. **The CTA** (one, specific, with name + phone or form)

### Founder Outreach Email

1. **The opening** (specific, not "I hope this finds you well")
2. **The why-you** (what you noticed about them)
3. **The move** (what you do)
4. **The proof** (one specific story or number)
5. **The ask** (small, scoped)
6. **The close** (signed by the human)

### "About" Page

1. **Who** (the operator, by name)
2. **What** (what they do, in plain language)
3. **Why** (the moment they started this)
4. **For whom** (the specific customer)
5. **The promise** (what doesn't change)
6. **Contact** (real channel, real human)

### Hiring Post (First / Second / Third Hire)

1. **What we are** (in plain language, no "we're a stealth-mode startup")
2. **What this role does** (specific, concrete)
3. **Who fits** (real traits, not "passionate self-starter")
4. **What pays** (range disclosed)
5. **What the first 90 days look like**
6. **How to apply** (specific, human)

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Trust posture (no corporate hedging) | 25 |
| Specificity | 20 |
| Evidence (real numbers, names, results) | 15 |
| Compression | 15 |
| Warmth (kitchen-table register) | 15 |
| CTA clarity | 10 |

## Failure Modes

- Corporate hedging ("dedicated to providing world-class…") → flat
- Generic adjectives without evidence → trust damage
- "We" without identifying the team size → mismatched authority
- "Trusted by…" without count → unverifiable
- Multiple CTAs → no action
- Composite testimonial as singular → ethical risk

## Before/After Example

**Before**:

> At Smith & Co., we're dedicated to providing world-class plumbing services to our valued customers. Our team of highly trained professionals leverages decades of combined experience to deliver game-changing results. Contact us today for a free consultation!

**After**:

> I'm Marcus Smith. I've been a plumber in East Memphis for 14 years. I run this with my brother Dave and one apprentice.
>
> Last year we did 412 service calls. Average response time on emergencies: 47 minutes. We're licensed and bonded in Tennessee (#TN-PL-04621). We charge $145 for the first hour, parts at cost, and we give you the receipt.
>
> If we can't fix it in the time we quoted, you don't pay the labor.
>
> Call me direct: (901) 555-0142. Mon-Fri 7 AM - 6 PM. Saturdays for emergencies.

## Stress Tests

- Cut every adjective. What survives is what was real.
- Replace every "we" with the operator's name. Does the authority still hold?
- For every result, name a customer or a number.
- Read it aloud. Does it sound like someone you'd hire?

## Delivery Formats

- Landing page (hero + sections)
- Email (founder outreach, customer follow-up)
- LinkedIn post (operator voice)
- "About" page
- Hiring post (LinkedIn, Indeed, Craigslist)
- Investor / lender memo (for small business capital)

## Schema Hooks

- `intake_contract.arena`: variable per use (`landing_page`, `email`, `linkedin_post`, etc.)
- `voice`: typically `courageous_builder` or a custom operator fingerprint
- `epistemic_ledger`: every result claim must be `user-provided` with permission, or `verified` against operational records

## Benchmark Cases

`SMALLBIZ-01` through `SMALLBIZ-05` in `benchmarks/cases/small_business_operator.md`.

## Stack Combinations

- + `sales.md`: when conversion is primary
- + `email.md`: outreach
- + `loan_officer.md`: small business capital
- + `real_estate.md`: solo agent operator
- + `grant_nofo.md`: small business / community development capital
- + `social_media.md`: founder voice across channels
