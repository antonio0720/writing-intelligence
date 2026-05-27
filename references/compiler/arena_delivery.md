# Arena Delivery Engine — Pass 8

**Purpose**: Convert the same intelligence into the exact delivery format where it must perform.

**Schema**: `schemas/delivery_bundle.schema.json` (`DeliveryBundleV3`)

**Agent**: Delivery Packager (`agents/delivery_packager.md`)

---

## The Arena Premise

The same content fails or wins based on the arena it arrives in. A 1,500-word memo that earns a CEO's attention becomes useless on Instagram. A grant narrative that wins a federal funder dies in a board meeting. A sermon that moves a congregation falls flat in a podcast feed.

Pass 8 is where one approved piece of content becomes many delivery bundles — each tuned to the constraints of its arena.

---

## Supported Arenas

| Arena | Constraints |
|---|---|
| `memo` | 500-2,000 words, BLUF, exec-readable, action items |
| `grant_response` | RFP-mapped, compliance matrix, outcome logic, budget alignment |
| `sermon` | 15-40 minutes spoken, cadence, scripture, call-response, applause architecture |
| `caption` | Platform char limit, hook + CTA, single image alignment |
| `article` | 800-2,500 words, headline + dek + body + close, scannable |
| `chapter` | 2,500-6,000 words, scene graph, button close |
| `email` | 50-300 words, subject + open + ask + sign |
| `pitch_slide` | 20-60 words per slide, one idea per slide, image-anchored |
| `youtube_script` | Word count = minutes × 150, hook-first, beat-paced |
| `newsletter` | 600-1,500 words, recurring sections, voice consistency |
| `government_brief` | BLUF + summary + recommendation + appendix, plain language |
| `sop` | Procedural, numbered, action-verb-led, exception-handled |
| `speech` | Spoken cadence, applause architecture, audience calibration |
| `landing_page` | Hero + proof + offer + CTA, scannable, mobile-first |
| `linkedin_post` | 800-1,500 chars, hook + proof + CTA, single-thread |
| `twitter_thread` | Multiple tweets, each ≤ 280 chars, threaded narrative |
| `instagram_caption` | Hook + value + CTA, 1,200-1,500 chars sweet spot |
| `press_release` | Headline + dek + dateline + lede + body + boilerplate |
| `case_study` | Problem + intervention + outcome + lesson, evidence-led |
| `blog_post` | 1,200-2,500 words, SEO-aware, scannable, internal links |

---

## Channel Constraints

Every arena ships with channel constraints. The Delivery Packager enforces:

- `char_max` — hard ceiling per platform (Twitter 280, LinkedIn 3,000, Instagram 2,200, etc.)
- `hashtag_max` — platform conventions (Instagram ≤ 30, LinkedIn ≤ 5 recommended, Twitter ≤ 3)
- `headline_variants_required` — multiple headlines for testing
- `cta_required` — explicit call-to-action mandatory
- `readability_level` — target Flesch-Kincaid / SMOG grade

Constraints come from `references/output_modes/platform_formats.md`.

---

## Single-Content-Multi-Arena Repackaging

A common v3.0 workflow: one approved memo → six arenas.

```
Source: 1,500-word strategic memo (approved, scored, ledgered)

Pass 8 emits delivery bundles for:
1. LinkedIn post (1,200 chars, hook + insight + CTA)
2. Twitter thread (8 tweets, narrative arc)
3. YouTube short script (90 seconds, 225 words)
4. Newsletter section (450 words, scannable)
5. Internal Slack announcement (200 words, BLUF)
6. Investor update paragraph (180 words, evidence-led)
```

Voice fingerprint is preserved across all six. Claims classified in Pass 5 remain classified. No new claims are introduced — the Delivery Packager **cannot invent content**; it formats approved content only.

---

## Channel-Specific Rules

### LinkedIn Post

- Hook in the first 2 lines (preview cutoff)
- 1 insight, 1-2 examples, 1 CTA
- ≤ 5 hashtags
- No more than 1 link (drops reach)
- Line breaks every 1-2 sentences (mobile readability)

### Twitter / X Thread

- Tweet 1 is the hook (must stand alone)
- Tweet N is the close (must reward the read)
- Each tweet a single idea
- Number tweets ("1/", "2/") only if thread length > 5
- Final tweet: CTA or punchline

### Instagram Caption

- Hook in line 1 (preview cutoff varies; assume ≤ 125 chars)
- Story / value in middle
- CTA in close
- Hashtags at bottom, separated by line break

### YouTube Script

- 0-7 seconds: hook (retention curve drops here)
- 7-30 seconds: promise / setup
- 30s-end: payoff with beat changes every 30-60 seconds
- Open loops every 90 seconds
- Outro: CTA + subscribe ask

### Newsletter

- Open with a value snippet (not "Hey friends")
- One main idea, 2-3 sub-sections
- Embedded link strategy: 2-4 links, all earning their place
- P.S. line is the second-most-read part of the email

### Sermon

- Cold open (hook the room before the scripture)
- Scriptural grounding
- 3 movements with applause architecture
- Call-and-response cadence points
- Close that releases

### Grant Response

- Must map 1:1 to the funder's RFP structure
- Every claim sourced or flagged
- Outcome logic chain visible
- Budget narrative aligned with program narrative
- See `references/genre_packs/grant_nofo.md` for full doctrine

### Government Brief

- BLUF (bottom line up front)
- Plain language (8th-12th grade reading level)
- Recommendations bolded
- Appendix carries the detail
- See `references/genre_packs/government_brief.md`

---

## Delivery Decision Gate

The Delivery Packager outputs a `delivery_decision`:

- `release` — all constraints met, no Pass 5 blocks, voice fidelity preserved
- `hold_for_review` — constraints met but Pass 5 had `claim_softened` or `claim_qualified` actions that the user should re-read
- `block` — Pass 5 had `delivery_block: true`, or a hard channel constraint violated, or fabrication risk unresolved

When `block`, `blocking_reasons` lists every reason.

---

## Definition of Done

The Delivery Packager emits a delivery bundle that:

- Validates against `delivery_bundle.schema.json`
- Contains every requested output mode from the intake contract
- Meets every channel constraint
- Carries the scorecard summary
- Carries a clear `delivery_decision`
- Contains no content not present in approved upstream artifacts

If any of the above fails, Pass 8/10 has not completed.
