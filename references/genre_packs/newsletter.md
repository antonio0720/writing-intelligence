# Genre Pack — Newsletter

**v3.0 Domain Pack Schema**

## Purpose

Produce email newsletters readers actually open — recurring sections, voice consistency, scannable architecture, single argument flow.

## When to Use

- Substack / Beehiiv / Ghost newsletters
- B2B / B2C marketing newsletters
- Founder / creator newsletters
- Internal company newsletters
- Investor / community updates

## When Not to Use

- One-off campaign emails (use `email.md`)
- Press releases (use `press_release`)
- Sales sequences (use `sales.md` + `email.md`)

## Audience Model

- A subscriber on email round 4 of their morning (3-5 seconds to decide)
- A subscriber on mobile, two-handed
- A skimmer who only reads bold and the P.S.
- A loyalist who reads every word

## Required Evidence

- For data claims: source + date
- For "I" statements: actually the speaker's experience
- For recommendations: tried, used, or verified personally

## Forbidden Claims

- "Happy Monday!" / "Hey friends!" (filler open)
- "Hope you had a great weekend" (no signal)
- "In this issue, we'll cover…" (cold preamble)
- Composite reader stories as "a subscriber wrote in"
- Subject lines that don't match the content

## Voice Weighting

- Subject-line force: **25**
- Open-paragraph hook: **20**
- Voice consistency: **15**
- Scannability: **15**
- Compression: **15**
- Specificity: **10**

## Structure Templates

### Standard Newsletter

1. **Subject line** (40-60 chars, no clickbait, signals content honestly)
2. **Preview text** (the line that shows under subject in inbox; 90-100 chars)
3. **Opening hook** (one paragraph, value-first, never "Hey friends")
4. **Main piece** (1 idea, 2-3 sub-sections, 600-1,200 words)
5. **Recurring sections** (e.g., "What I'm reading," "Three numbers," "One question")
6. **CTA** (one only — paid sub, share, reply, click)
7. **P.S.** (second-most-read part of the email)

### Substack-Style Long Read

1. **Subject + preview** (signals depth, not summary)
2. **Cold open** (the moment of recognition)
3. **The argument** (organized, scannable, with section headers)
4. **The evidence** (sources, data, citations)
5. **The implication** (what this means for the reader)
6. **CTA** (subscribe, share, comment)
7. **P.S.** (sidebar, recommendation, callback)

### B2B Marketing Newsletter

1. **Subject line** (data-led or curiosity-led)
2. **Hook** (1 surprising fact or claim)
3. **Body** (problem → insight → application)
4. **Tool / resource** (one link)
5. **CTA** (book / demo / reply)

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Subject line + preview text | 20 |
| Open-paragraph hook | 20 |
| Scannability (bold, sections, breaks) | 15 |
| Voice consistency with prior issues | 15 |
| Single CTA discipline | 15 |
| P.S. value | 10 |
| Compression | 5 |

## Failure Modes

- "Hey friends" opener → flagged
- Multiple CTAs → reader takes none
- Subject line that lies about content → unsubscribe spike
- 4+ paragraphs without scannability break → mobile read dies
- Inconsistent voice across issues → loyalty damage
- P.S. as throwaway → wasted attention

## Before/After Example

**Before** (subject + opener):

> Subject: Some thoughts for your week
>
> Hey friends! Hope you had a great weekend. In this week's newsletter, we'll be covering some interesting ideas about productivity, including some tips and tricks that might help you out. Let's dive in!

**After**:

> Subject: The 4 PM crash isn't about caffeine
> Preview: It's about the meeting you stopped having with yourself.
>
> Every day at 4 PM, I used to lose 90 minutes.
>
> Coffee didn't fix it. A walk didn't fix it. Calendaring didn't fix it. The thing that fixed it was so small I felt embarrassed when I figured it out: I had stopped writing my one-sentence end-of-day note.

## Stress Tests

- Subject line in 6 words: does it earn the open?
- First paragraph: does it open without preamble?
- Identify the CTA. Is there exactly one?
- Read on mobile. Does it scan?
- Compare voice metrics to last 3 issues. Drift?

## Delivery Formats

- HTML (Substack, Beehiiv, Mailchimp, etc.)
- Plain text alternative
- Web archive version
- Companion social post (one excerpt)

## Schema Hooks

- `intake_contract.arena: newsletter`
- `delivery_bundle.channel_constraints`: subject_max=60, preview_max=100, single_cta=true

## Benchmark Cases

`NEWSLETTER-01` through `NEWSLETTER-05` in `benchmarks/cases/newsletter.md`.

## Stack Combinations

- + `small_business_operator.md`: founder newsletters
- + `church_leadership.md`: weekly devotionals
- + `journalism.md`: deep-dive Substacks
- + `social_media.md`: cross-pollination
