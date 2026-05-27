# Genre Pack — Social Media

**v3.0 Domain Pack Schema**

## Purpose

Produce platform-native posts that earn attention in a feed, earn engagement, and drive a measurable next step — without sacrificing voice fidelity.

## Sub-Arenas

- LinkedIn post
- Twitter / X thread
- Instagram caption
- TikTok caption
- Facebook post
- Threads post
- Bluesky post

## When to Use

- Single-platform posts
- Multi-platform repackaging from one source piece
- Founder / creator / brand voice posts
- Campaign launches

## When Not to Use

- Press releases (use `press_release` arena)
- Long-form newsletters (use `newsletter.md`)
- Internal Slack / Teams posts (different register, see `email.md`)

## Audience Model

- A scroller giving 1-3 seconds before deciding to keep reading
- A reader on mobile, two-thumbed, distracted
- An algorithm scoring engagement velocity

## Required Evidence

- For data claims: source named (link or citation)
- For "I" statements: actually the speaker's experience
- For client/result claims: permission to share
- For statistics: real numbers with date

## Forbidden Claims

- "100x" / "10x" without numbers behind them
- "Most people" / "everyone" — universal quantifiers
- Composite client stories presented as one
- Stolen quotes without attribution
- Fake "I built X in a weekend" narratives

## Voice Weighting

- Hook force: **25**
- Compression: **20**
- Specificity: **15**
- Voice fidelity: **15**
- CTA discipline: **15**
- Authority posture: variable by platform and audience

## Platform-Specific Constraints

| Platform | Char Limit | Hook Cutoff | Optimal Length | Hashtag Norm |
|---|---|---|---|---|
| LinkedIn post | 3,000 | ~210 chars | 1,200-1,500 | ≤ 5 |
| Twitter / X | 280 per tweet | first tweet | 4-12 tweets per thread | ≤ 3 |
| Instagram caption | 2,200 | ~125 chars | 1,200-1,500 | up to 30 |
| TikTok caption | 4,000 | ~100 chars | 100-300 | 3-8 trending |
| Facebook post | 63,206 | ~250 chars | 100-250 | minimal |
| Threads | 500 | first 80 chars | 200-400 | minimal |

## Structure Templates

### LinkedIn Post (1,200 chars)

```
[Hook: 1-2 lines, must work above the "see more" fold]
[White space]
[Story or insight: 3-5 short paragraphs]
[Specific takeaway or number]
[CTA: comment, share, or DM-trigger]
[Hashtags: ≤ 5]
```

### Twitter Thread (8 tweets)

```
Tweet 1: The hook. Must stand alone. Surprising claim or vivid image.
Tweet 2: The setup. Context for why this matters.
Tweet 3-6: The body. One idea per tweet. Numbered if helpful.
Tweet 7: The turn. The insight or reversal.
Tweet 8: The close. CTA, link, or punchline.
```

### Instagram Caption

```
[Hook in first line — preview cutoff]
[White space]
[Story or value: paragraphs with line breaks every 1-2 sentences]
[Specific takeaway]
[CTA: comment trigger, save, or DM]
[Hashtags: up to 30, grouped at bottom or first comment]
```

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Hook force (first 1-2 lines) | 25 |
| Platform-native formatting | 20 |
| Compression | 15 |
| Specificity | 15 |
| CTA clarity | 15 |
| Voice fidelity | 10 |

## Failure Modes

- Hook that doesn't survive preview cutoff → post dies
- Generic "Most people don't realize…" opener → scroll-past
- Multiple CTAs (DM me + comment + click + share) → no action taken
- Hashtag stuffing visible in body → spam signal
- Universal quantifiers in claims → trust damage

## Before/After Example

**Before** (LinkedIn):

> 🚀 Excited to share some thoughts about leadership! Most people don't realize how important it is to be a good leader. Here are 5 game-changing tips that will transform your career. Comment below if you agree!

**After**:

> The hardest moment in my last six months wasn't a launch. It was telling a senior I trusted that the role I'd promised him didn't exist anymore.
>
> I almost wrote him a memo. He deserved a call.
>
> Three things I learned in that call:
>
> 1. The truth doesn't get easier by waiting.
> 2. People remember tone more than content.
> 3. "I'm sorry" is a complete sentence.
>
> If you're leading something hard right now, the next conversation is probably the one you've been postponing.
>
> What's the call you've been putting off?

## Stress Tests

- Cut the hook to its first 8 words. Does it still earn attention?
- Read the post on mobile, scrolling fast. Does it hold?
- Show it to a stranger. Can they say what the post is about?
- Count CTAs. More than 1 → consolidate.

## Delivery Formats

- Native platform-ready text (correct char count, hashtag count, format)
- Image caption (if image-anchored)
- Alt-text for accessibility
- Companion DM template (for inbound responses)

## Schema Hooks

- `intake_contract.arena`: one of `linkedin_post`, `twitter_thread`, `instagram_caption`, `caption`, etc.
- `delivery_bundle.channel_constraints`: char_max, hashtag_max, headline_variants_required

## Benchmark Cases

`SOCIAL-01` through `SOCIAL-05` in `benchmarks/cases/social_media.md`.

## Stack Combinations

- + `sales.md`: sales-led social posts
- + `small_business_operator.md`: founder voice
- + `church_leadership.md`: ministry social
- + `newsletter.md`: cross-pollination
