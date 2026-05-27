# Genre Pack — Journalism / Feature Writing

**v3.0 Domain Pack Schema**

## Purpose

Produce reported, evidence-disciplined narrative nonfiction — feature articles, investigations, profiles, explainers.

## When to Use

- Feature articles (1,200-3,500 words)
- Investigative pieces
- Profiles
- Explainers
- Long-form essays grounded in reporting
- Newsletter deep dives based on reporting

## When Not to Use

- Marketing posts pretending to be journalism (use `content_creation`)
- Op-eds (use `speech.md` or `essay`)
- Pure analysis (use `academic.md` or `strategy.md`)

## Audience Model

- A general reader who came for the headline
- A skeptical reader who came for the receipts
- A subject of the piece who will read every word
- A future fact-checker

## Required Evidence

- Named sources (or explicit anonymous-source justification)
- Recorded interviews / on-the-record statements
- Primary documents (court filings, FOIA returns, financial statements)
- Verified statistics with source and date
- Geographic / temporal specifics (where, when)
- Scene observation (when reporter was present)

## Forbidden Claims

- "Sources say" without enumeration
- "It is widely known" / "everyone agrees"
- Composite quotes (combining multiple statements into one)
- Composite scenes (combining multiple events into one without disclosure)
- Reconstructions without disclosure
- Unattributed reasoning ("the obvious conclusion")

## Voice Weighting

- Source discipline: **25** (highest)
- Specificity: **20**
- Narrative force: **15** (scene + reporting balance)
- Compression: **15**
- Warmth: **10** (humanity without sentimentality)
- Authority posture: **55-65** (confident reporter, not opinion columnist)

## Structure Templates

### Standard Feature

1. **Lede** — scene, anecdote, or surprising fact that earns next 30 seconds
2. **Nut graf** — what this piece is about, what's at stake, why now
3. **Reporting** — alternating scene and exposition
4. **Counter-perspective** — sources who disagree, on the record
5. **Stakes** — what changes if the situation changes
6. **Close** — image that crystallizes, returns to lede, or earns the question

### Investigation

1. **Cold open** — the moment of recognition
2. **What we found** — BLUF
3. **How we found it** — methodology (briefly)
4. **The trail** — documentary evidence
5. **The denials / responses** — sources who pushed back
6. **What it means** — stakes for affected populations
7. **What's next** — pending action, oversight, accountability

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Source attribution quality | 25 |
| Verifiability | 20 |
| Scene/reporting balance | 15 |
| Nut graf force | 15 |
| Counter-perspective inclusion | 15 |
| Voice (reporter, not advocate) | 10 |

## Failure Modes

- Unattributed claims → automatic flag
- Composite without disclosure → ethical violation, retraction risk
- Single-source piece on contested fact → score capped
- Lede that does not earn the read → reader bounces
- Missing nut graf → reader confused at paragraph 3
- No counter-perspective on contested issue → bias risk

## Before/After Example

**Before**:

> Many residents are concerned about the new development, which is widely seen as harmful to the community. Critics say it will gentrify the neighborhood.

**After**:

> At Tuesday's planning meeting, 14 of 19 speakers opposed the rezoning. Three — Lena Walker, Mike Brown, and Pastor Joel Hayes — said they had lived on Walnut Street for more than 30 years. "I'm not against new neighbors," Walker told the commission. "I'm against losing the ones I have." The developer's representative, Carter Lin, declined to comment after the meeting but had earlier told the *Free Press* the project includes "affordability set-asides," without specifying the income tiers.

## Stress Tests

- For every claim, name the source.
- For every quote, verify it was said.
- For every scene, verify the reporter was present or sourced.
- For every contested fact, identify the counter-perspective.
- For the lede: would a stranger keep reading?
- For the nut graf: would a stranger know what this is about?

## Delivery Formats

- Long-form web article
- Magazine PDF
- Newsletter deep dive
- Audio narration script (companion)

## Schema Hooks

- `intake_contract.arena: article`
- `intake_contract.high_stakes: true` (always; journalism is high-stakes)
- `epistemic_ledger`: mandatory; every claim and quote sourced

## Benchmark Cases

`JOURN-01` through `JOURN-05` in `benchmarks/cases/journalism.md`.

## Stack Combinations

- + `academic.md`: explanatory journalism with deeper research
- + `medical_writing.md`: health reporting
- + `legal_positioning.md`: court reporting
- + `cinematic_narration.md`: longform narrative nonfiction
