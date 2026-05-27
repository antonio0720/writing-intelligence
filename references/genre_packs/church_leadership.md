# Genre Pack — Church Leadership

**v3.0 Domain Pack Schema**

## Purpose

Produce communication that serves the local church — sermons, study guides, devotionals, announcements, pastoral letters, ministry newsletters — with theological care, voice dignity, and pastoral warmth.

## When to Use

- Sermon preparation
- Bible study guides
- Daily / weekly devotionals
- Sunday announcements / bulletins
- Pastoral letters
- Ministry newsletters
- Capital campaign communication
- Member outreach

## When Not to Use

- Pure sermon prose (use `sermon.md` from v2.0 — this pack extends, not replaces)
- Para-church marketing (use `sales.md` + church_leadership as modulator)
- Academic theology (use `academic.md`)

## Audience Model

- The congregation present on Sunday
- The member reading mid-week alone
- The visitor who scanned the bulletin
- The neighbor who got the email forward
- The leader / board / elder team

## Required Evidence

- Scripture references (verified, version named — ESV, NIV, KJV, NRSV, etc.)
- Historical or doctrinal citations (when invoked)
- Local context (this church, this community, this season)
- Verifiable events (services, ministries, schedules)

## Forbidden Claims

- Universal "all Christians believe…" without theological grounding
- Composite member testimonials presented as one
- Predictions about specific outcomes ("God will heal you of…")
- Doctrinal claims presented as personal preference
- "God told me…" framing in published communication without significant care
- Comparison to other churches in ways that diminish them

## Voice Weighting

- Theological care: **20** (highest)
- Pastoral warmth: **20**
- Specificity (this congregation, this week): **15**
- Cadence (oral / written depending on use): **15**
- Compression: **15**
- Voice fidelity to the speaker / pastor: **15**

## Structure Templates

### Sermon Notes (Companion to v2.0 sermon.md)

1. **Title** (memorable, descriptive)
2. **Scripture** (primary text + supporting texts)
3. **The big idea** (one sentence)
4. **Movement 1** (with application)
5. **Movement 2** (with application)
6. **Movement 3** (with application)
7. **Close + invitation**

### Bible Study Guide

1. **Opening reflection** (1-2 paragraphs)
2. **Scripture reading** (text printed, version named)
3. **Discussion questions** (3-5, scaffolded from observation to application)
4. **Practical application** (this week)
5. **Closing prayer prompt**

### Weekly Devotional (300-500 words)

1. **Scripture** (one verse, version named)
2. **Reflection** (3-4 short paragraphs)
3. **Application** (one specific move this week)
4. **Prayer prompt** (1-2 sentences)

### Announcement (Bulletin / Email)

1. **What's happening** (event name + date + time)
2. **Why it matters** (one sentence)
3. **Who it's for**
4. **How to participate / RSVP**
5. **Contact** (name + phone or email)

### Pastoral Letter (Hard News, Grief, Encouragement)

1. **Direct opening** (no "I hope this finds you well")
2. **The matter at hand**
3. **The pastoral framing** (Scripture, encouragement, presence)
4. **The action** (gathering, prayer chain, resources)
5. **Closing** (with the speaker's voice fingerprint)

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Theological care | 20 |
| Pastoral warmth | 20 |
| Specificity (this congregation) | 15 |
| Voice fidelity to the speaker | 15 |
| Compression | 15 |
| Compliance with denominational language norms | 10 |
| CTA clarity | 5 |

## Failure Modes

- Generic "God is good" framing without specificity → flat
- Composite testimony → ethical violation
- "God told me to tell you X" → pastoral care risk
- Doctrinal certainty stated where Scripture is silent → flag
- Comparison that diminishes other congregations → division risk

## Before/After Example

**Before** (sermon notes):

> Today we'll talk about faith. Faith is so important in our walk with God. We all need more faith. When we have faith, anything is possible! Let's pray that God gives us more faith this week.

**After**:

> **Title**: The Mustard Seed Was Smaller Than Yours
> **Scripture**: Matthew 17:14-20 (ESV)
>
> **The big idea**: Faith does not require size. It requires direction.
>
> **Movement 1 — The Father's Honest Ask**: He didn't pretend his faith was big. He said, "Lord, I believe; help my unbelief."
>
> **Application**: This week, write down the thing you've been telling God you believe but haven't acted on. Bring it Sunday.
>
> **Movement 2 — The Disciples' Quiet Failure**: They couldn't heal him. Then they asked the right question: Why?
>
> **Application**: The right "why?" beats the right answer. What are you not asking?
>
> **Movement 3 — Jesus' Answer About Size**: Faith the size of a mustard seed.
>
> **Application**: Stop asking for more faith. Use the faith you have.
>
> **Close**: Whatever you brought today — bring it to the altar. Not for size. For direction.

## Stress Tests

- Every Scripture reference verified (book, chapter, verse, version).
- Every doctrinal claim tied to text or tradition.
- Every "us / we / our" framing — is it earned by the speaker's authority in this congregation?
- Cadence: read aloud. Does it preach?
- Specificity: does this only fit this Sunday at this church?

## Delivery Formats

- Sermon notes / outline
- Bible study handout (PDF)
- Email devotional
- Bulletin announcement
- Pastoral letter (PDF / email)
- Social ministry post

## Schema Hooks

- `intake_contract.arena: sermon` (sermon) or `email` (devotional / letter) or `caption` (announcement)
- `genre_stack`: typically primary `church_leadership` + secondary `sermon` (v2.0) + modulator `email` or `social_media`
- `epistemic_ledger`: every Scripture reference and doctrinal claim sourced

## Benchmark Cases

`CHURCH-01` through `CHURCH-05` in `benchmarks/cases/church_leadership.md`.

## Stack Combinations

- + `sermon.md` (v2.0 Black church tradition voice)
- + `grant_nofo.md`: faith-based community grants
- + `newsletter.md`: weekly devotional series
- + `youtube_script.md`: sermon clips for digital
- + `social_media.md`: church social presence
