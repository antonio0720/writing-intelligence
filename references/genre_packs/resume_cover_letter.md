# Genre Pack — Resume / Cover Letter

**v3.0 Domain Pack Schema**

## Purpose

Produce ATS-clean, evidence-of-impact career documents that compress a person's work history into a 6-second hiring decision.

## When to Use

- Traditional resumes (1-2 pages)
- LinkedIn profile copy
- Cover letters (3-4 paragraphs)
- Executive bios
- Portfolio summaries

## When Not to Use

- Long-form personal branding (use `linkedin_post` + `newsletter.md`)
- Speaker bios for an event (use `speech.md`)
- Memoir / personal essay (use `creative writing`)

## Audience Model

- A recruiter with 6 seconds per page
- A hiring manager with 30 seconds per candidate
- An ATS (Applicant Tracking System) parsing keywords
- A future manager who will read it more carefully

## Required Evidence

- Quantified impact (numbers, percentages, dollar amounts, time-saved)
- Named systems / technologies / methodologies
- Specific role responsibilities (not generic)
- Dates (months + years, not just years)
- Verifiable degrees and certifications

## Forbidden Claims

- "Results-oriented" / "team player" / "detail-oriented" (generic adjectives)
- "Synergize" / "leverage" / "ideate" / "blue-sky" / "circle back"
- "Responsible for" without outcome
- Achievements that cannot be quantified
- Skills without evidence of use
- Job titles inflated beyond the actual role

## Voice Weighting

- Compression: **30** (highest — every word earns)
- Specificity: **25**
- Evidence: **15**
- ATS keyword fit: **15**
- Voice: **10** (professional, confident)
- Authority posture: **65-75**

## Structure Templates

### Resume

1. **Name + contact + LinkedIn** (1 line)
2. **One-line professional summary** (8-12 words)
3. **Experience** (reverse chronological, 3-5 bullets per role)
4. **Skills** (grouped, ATS-keyword-aligned)
5. **Education + certifications**
6. **Projects** (if applicable)

Each bullet:

`Action verb` + `what you did` + `how you did it` + `measurable outcome`

### Cover Letter

1. **Opening** — why this role, why this company (1-2 sentences)
2. **Evidence** — 2-3 specific accomplishments from your work that match what they need
3. **Connection** — what you'd bring that's distinct
4. **Close** — request for next step

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Quantified outcomes per role | 25 |
| Action verb specificity | 20 |
| ATS keyword alignment | 15 |
| Compression (no filler) | 15 |
| Evidence-to-claim ratio | 15 |
| Voice (confident, not arrogant) | 10 |

## Failure Modes

- Generic adjectives in summary → automatic flag
- "Responsible for" without outcome → flag
- Unquantified achievement → flag (target: 80%+ quantified)
- Job titles inflated beyond actual role → trust damage
- ATS keyword stuffing visible to human reader → reduces credibility

## Before/After Example

**Before**:

> Detail-oriented marketing professional with a passion for driving results. Responsible for managing campaigns and helping the team succeed. Synergized with cross-functional partners to leverage best practices.

**After**:

> Led 14 lifecycle email campaigns reaching 240K subscribers (FY25). Improved click-through 31% over baseline by rewriting subject lines using A/B-validated patterns. Mentored 3 junior writers; two earned promotions within 12 months.

## Stress Tests

- For every bullet: does it have a quantified outcome?
- For every adjective: cut. If it survives the cut, keep it.
- For every job title: verify against actual scope.
- ATS scan: do the keywords match the JD without keyword-stuffing?
- Six-second test: hand to a stranger; can they say what you do?

## Delivery Formats

- ATS-friendly .docx (single-column, simple formatting)
- Designed PDF (for human review)
- LinkedIn copy (parallel structure)
- Plain text (for online forms)

## Schema Hooks

- `intake_contract.arena: memo` (resume) or `email` (cover letter)
- `corpus_map`: user-provided work history is `user-provided`; cannot be verified without their input
- `epistemic_ledger`: every quantified claim must be `user-provided` with `fabrication_risk: none`

## Benchmark Cases

`RESUME-01` through `RESUME-05` in `benchmarks/cases/resume_cover_letter.md`.

## Stack Combinations

- + `email.md`: cover letters
- + `small_business_operator.md`: founder bios
- + `academic.md`: CVs
- + `linkedin_post`: LinkedIn summaries
