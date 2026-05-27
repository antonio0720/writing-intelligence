# Genre Pack — YouTube Script

**v3.0 Domain Pack Schema**

## Purpose

Produce video scripts that hold retention through every drop point — 7-second hook, 30-second promise, 90-second open loops, end-screen call to action.

## When to Use

- Long-form YouTube (5-30 minutes)
- YouTube Shorts (15-60 seconds)
- Companion explainer videos
- Tutorial videos
- Channel trailers

## When Not to Use

- Documentary narration (use `cinematic_narration.md`)
- Sales VSL (use `sales.md` + `landing_page` arena)
- Corporate training (use `sop` arena)

## Audience Model

- A viewer who clicked the thumbnail / title
- A viewer holding the next-video button at every retention drop
- A viewer on mobile, autoplay enabled, headphones in

## Required Evidence

- Retention curve assumption (typical drop points: 7s, 30s, 90s, 50% mark)
- Hook hypothesis (why this opens)
- Open loops (questions the script promises to answer)
- Visual / B-roll plan (when applicable)
- End-screen CTA

## Forbidden Claims

- "Subscribe!" without earned reason
- "Like the video!" begging
- "In this video we'll discuss" (lazy preamble that loses 30% retention)
- "Welcome back to the channel" (kills new-viewer experience)
- Content that doesn't match the title / thumbnail (clickbait penalty)

## Voice Weighting

- Hook force: **30** (highest — most YouTube retention dies in first 7 seconds)
- Pacing: **20**
- Open-loop discipline: **15**
- Specificity: **15**
- Voice fidelity: **10**
- CTA clarity: **10**

## Retention Architecture

| Mark | Risk | Move |
|---|---|---|
| 0-7 sec | 30-50% drop | Hook: surprise, image, or stakes |
| 7-30 sec | 10-20% drop | Promise: what the viewer gets |
| 30 sec - 90 sec | 5-10% drop | First payoff + first open loop |
| 90 sec - mid | gradual drop | Beat changes every 60-90 sec |
| 50% mark | 5-10% drop | Open new loop, raise stakes |
| End | bounce | Earn the subscribe |

## Structure Templates

### Long-Form (8-15 min)

1. **Hook** (0-7s) — surprise, image, or stakes
2. **Promise** (7-30s) — what the viewer will get
3. **Section 1** with first payoff (30s-3min)
4. **Open loop** at end of section 1
5. **Section 2** (3-6 min) — escalating stakes
6. **Open loop** at end of section 2
7. **Section 3** (6-10 min) — payoff and resolution
8. **Conclusion** with end-screen CTA (10-12 min)

### YouTube Short (60s)

1. **Hook** (0-2s) — visual + question
2. **Setup** (2-15s) — problem or stake
3. **Resolution** (15-50s) — answer or reveal
4. **CTA** (50-60s) — "follow for more on [topic]"

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Hook force (0-7s) | 30 |
| Promise clarity | 15 |
| Beat pacing | 15 |
| Open-loop discipline | 15 |
| Specificity | 10 |
| End-screen CTA earned | 10 |
| Voice fidelity | 5 |

## Failure Modes

- "In this video we'll discuss…" → 30% retention drop confirmed
- Promise unfulfilled → clickbait penalty, watch-time damage
- Single beat for 5+ minutes → drop
- "Subscribe!" without reason → flat conversion
- Title/thumbnail mismatch → algorithm penalty

## Before/After Example

**Before**:

> Hey guys! Welcome back to the channel! In this video, we're going to talk about productivity. So let's get into it!

**After**:

> The most productive day of my life ended with me crying in my car at 4 PM.
>
> It taught me that productivity isn't a system — it's a story you tell yourself about your worth.
>
> In the next eight minutes, I'll show you the three signals I missed, the rebuild I had to do, and the one daily move that holds when nothing else does.

## Stress Tests

- Read the first 7 seconds. Does it land without a thumbnail?
- Check the promise at 30 seconds. Is the viewer getting what they were promised?
- Identify every open loop. Each must close within the video.
- Check beat changes. Are they spaced 60-90 seconds apart?
- End-screen CTA: is it earned?

## Delivery Formats

- Script with timecodes
- Teleprompter-formatted version (line breaks for breath)
- Companion description (with chapters, links, hashtags)
- Title variants (3-5) for A/B testing

## Schema Hooks

- `intake_contract.arena: youtube_script`
- `delivery_bundle.channel_constraints`: word_count = minutes × 150

## Benchmark Cases

`YOUTUBE-01` through `YOUTUBE-05` in `benchmarks/cases/youtube_script.md`.

## Stack Combinations

- + `cinematic_narration.md`: documentary-style
- + `sales.md`: VSL-style
- + `church_leadership.md`: sermon clips
- + `small_business_operator.md`: founder voice
