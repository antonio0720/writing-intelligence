# Genre Pack — Loan Officer / Banking Communication

**v3.0 Domain Pack Schema**

## Purpose

Produce borrower-facing communication — pre-approval letters, rate-sheet explanations, closing-table guidance, refinance pitches — that builds trust, stays compliant, and explains numbers clearly.

## When to Use

- Pre-approval letters
- Rate-lock explanations
- Closing-table communications
- Refinance outreach
- Borrower education (FHA, VA, USDA, conventional, jumbo)
- Realtor partnership updates
- Co-marketing materials

## When Not to Use

- Pure marketing (use `sales.md`)
- Legal disclosures (use `legal_positioning.md`)
- Investor / capital-markets memos (use `pitch_deck.md`)

## Audience Model

- A first-time borrower confused by jargon
- A repeat borrower confident but cost-sensitive
- A realtor partner watching response time
- A compliance reviewer checking TRID and ECOA

## Required Evidence

- APR vs. interest rate (both stated when comparing)
- Discount points and their dollar cost
- Closing-cost itemization
- Loan term and amortization specifics
- DTI calculation (when relevant)
- Tax / insurance escrow estimate

## Forbidden Claims

- "Lowest rate in town" (compliance violation if unverifiable)
- "Guaranteed approval" (RESPA / ECOA risk)
- Predicting rate movements as facts
- Omitting APR when stating rate
- "No-cost refinance" without explaining how (costs rolled into rate or balance)
- Steering language (favoring one loan type over another without reason)

## Voice Weighting

- Compliance: **25** (highest — TRID, RESPA, ECOA, Fair Housing)
- Clarity: **20**
- Specificity (numbers): **15**
- Trust posture: **15**
- Compression: **15**
- Warmth: **10**

## Structure Templates

### Pre-Approval Letter

1. **Greeting** (name + date)
2. **Approval scope** (program, loan amount, property type)
3. **Conditions** (verifiable income, assets, credit)
4. **Validity period** (expiration date)
5. **Contact** (loan officer + NMLS)
6. **Required disclosure language** (per state and program)

### Rate Lock Explanation

1. **The rate locked** (with APR)
2. **The lock period**
3. **Points paid** (dollar cost)
4. **What changes if the lock expires**
5. **What changes if the lock is broken** (e.g., float-down provisions)
6. **Next milestone**

### Refinance Outreach

1. **Current loan** (rate, balance, payment)
2. **Proposed loan** (rate, term, payment, closing costs)
3. **Break-even point** (months until savings cover closing costs)
4. **Lifetime savings or cost** (clear, both directions)
5. **Considerations** (extending term, equity changes, escrow impact)
6. **Next step** (no pressure)

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Compliance (TRID / RESPA / ECOA / Fair Housing) | 25 |
| Numbers clarity (APR + rate always paired) | 20 |
| Borrower education quality | 15 |
| Trust posture (no pressure) | 15 |
| Compression | 15 |
| CTA clarity | 10 |

## Failure Modes

- Rate stated without APR → compliance flag
- "Guaranteed" / "lowest" / "best" → automatic flag
- Predicting rates → trust + compliance risk
- "Just sign here" / urgency manufactured → ECOA risk
- Steering toward one program without borrower-fit reason → fair housing risk

## Before/After Example

**Before**:

> Hey Sarah! I can get you the lowest rate in town — guaranteed! Lock it in today before rates go up. This is a no-brainer!

**After**:

> Sarah, based on your file (660 credit, 23% DTI, 10% down), the program that fits is FHA at 6.625% (6.85% APR), 30-year fixed.
>
> If you lock today at 0 points, your monthly P&I on $310K is $1,985. Adding tax and insurance escrow, your full payment is approximately $2,420.
>
> The lock is good through May 31. If rates drop more than 0.25% in the next 30 days, our float-down provision lets you re-lock once.
>
> No urgency. Want me to send the rate sheet, the GFE, and a side-by-side with the conventional option you asked about?
>
> — Marcus Bell, NMLS #123456

## Stress Tests

- Every rate quoted has APR alongside.
- No "guaranteed" / "lowest" / "best" appears.
- Every "we recommend" carries the borrower-fit reason.
- Every cost is itemized.
- Compliance language present per program and state.

## Delivery Formats

- Pre-approval letter (PDF on letterhead)
- Rate-lock explanation (email or PDF)
- Refinance comparison (table)
- Disclosure-compliant follow-up email

## Schema Hooks

- `intake_contract.arena: email` or `memo`
- `intake_contract.high_stakes: true` (compliance)
- `epistemic_ledger`: mandatory; every rate, fee, and APR sourced
- `genre_stack`: add `legal_positioning.md` as modulator for required language

## Benchmark Cases

`LOAN-01` through `LOAN-05` in `benchmarks/cases/loan_officer.md`.

## Stack Combinations

- + `email.md`: borrower outreach
- + `real_estate.md`: co-marketing with realtors
- + `legal_positioning.md`: disclosure language
- + `small_business_operator.md`: solo loan officer brand
