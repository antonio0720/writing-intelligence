# Intake Contract Engine — Pass 0

**Purpose**: Convert every chaotic request into a governed task object before any writing begins.

**Schema**: `schemas/intake_contract.schema.json` (`IntakeContractV3`)

**Agent**: Intake Architect (`agents/intake_architect.md`)

---

## Why Pass 0 Matters

v2.0 trusted the user request. v3.0 governs it. Pass 0 is the first checkpoint: every downstream pass reads the contract emitted here. If the contract is wrong, every later pass is wrong.

The Intake Architect's job is to detect ambiguity, lock constraints, and refuse to start work on an underspecified request without first asking.

---

## The Contract

Every contract must declare:

1. **task_id** — unique identifier (`wi_v3_YYYY_NNNNNN`)
2. **mode** — `draft | rewrite | score | redline | compress | expand | audit | convert | certify`
3. **intent** — `inform | convert | warn | teach | dignify | dominate | comfort | reveal | mobilize | persuade | entertain | defend | terrify | disorient`
4. **audience** — free-form or audience archetype ID
5. **voice** — voiceprint identifier or `custom` + fingerprint reference
6. **genre_stack** — at least one genre pack ID
7. **constraints** — word counts, citation requirements, forbidden changes, output modes
8. **source_policy** — user_text_priority, memory_allowed, web_required, citations_required, fabrication_tolerance
9. **arena** — delivery arena (memo, grant, sermon, social, etc.)
10. **high_stakes** — boolean; if true, Pass 5 (Epistemic Ledger) is mandatory
11. **success_condition** — one sentence describing what "worked" looks like
12. **ambiguity_flags** — anything the architect cannot resolve

---

## Detection Rules

The Intake Architect runs the following checks:

### Mode Detection

| Signal | Inferred Mode |
|---|---|
| "Write me…" / "Draft…" / "Compose…" | `draft` |
| "Rewrite…" / "Fix…" / "Edit…" / "Clean this up" | `rewrite` |
| "Score this" / "Grade…" / "How good is…" | `score` |
| "Track changes" / "Redline" | `redline` |
| "Cut to N words" / "Make this shorter" | `compress` |
| "Expand…" / "Add detail" | `expand` |
| "Audit…" / "Review for issues" | `audit` |
| "Turn this into…" / "Convert for…" | `convert` |
| "Test me" / "Certify…" | `certify` |

### Intent Detection

Look for action verbs the writing must accomplish. Defaults to `inform` when ambiguous. Multiple intents allowed but one must be primary.

### Audience Detection

Look for: pronouns directed at the reader, level of jargon, expected familiarity. If the request says "executives" → calibrate vocabulary, abstraction, evidence expectations. If "kindergartners" → reset everything.

### High-Stakes Detection

A task is high-stakes if any of these are present:

- Academic context (paper, thesis, dissertation, peer review)
- Medical context (clinical, diagnostic, pharmaceutical)
- Legal context (filing, brief, memorandum, contract)
- Government context (federal, agency, regulatory, statutory)
- Grant context (NOFO, RFP, foundation, federal grant)
- Financial context (SEC, investor, board, audit, disclosure)
- Public release with attribution to a real person
- Any context where a false claim causes measurable harm

When high-stakes is true, `source_policy.fabrication_tolerance` defaults to `zero` and `citations_required` defaults to `true`.

### Arena Detection

| Signal | Inferred Arena |
|---|---|
| "Memo" / "internal note" | `memo` |
| "Grant" / "NOFO" / "RFP response" | `grant_response` |
| "Sermon" / "homily" / "devotional" | `sermon` |
| "Post" / "caption" / "Instagram" | `caption` / `instagram_caption` |
| "Article" / "blog post" | `article` / `blog_post` |
| "Chapter" / "scene" / "fiction" | `chapter` |
| "Email" / "reply" | `email` |
| "Pitch" / "slide" / "deck copy" | `pitch_slide` |
| "YouTube script" / "video script" | `youtube_script` |
| "Newsletter" / "Substack" | `newsletter` |
| "Brief" / "BLUF" / "agency memo" | `government_brief` |
| "SOP" / "runbook" / "procedure" | `sop` |
| "Speech" / "keynote" / "address" | `speech` |
| "Landing page" / "hero copy" | `landing_page` |
| "LinkedIn post" | `linkedin_post` |
| "Twitter thread" / "X thread" | `twitter_thread` |
| "Press release" | `press_release` |
| "Case study" | `case_study` |

---

## Ambiguity Triage

When the Intake Architect cannot infer a required field, it does NOT guess. It emits an `ambiguity_flags` entry and pauses.

**Examples that trigger ambiguity flags:**

- "Write something for my audience" — audience unspecified
- "Make it better" — mode and success condition unspecified
- "A doc for the board" — high_stakes unclear, audience precision missing
- "A long-form thing about the new product" — intent, audience, arena all unspecified

The architect's response in these cases is a structured clarification request, batched into one message:

```
Before I start, I need:
1. [missing field]: [options]
2. [missing field]: [options]
3. [missing field]: [options]
```

**User sovereignty rule**: user-provided constraints override auto-detection at every point. If the user says "use plain language" and the auto-detected genre is academic, plain language wins.

---

## Example Contract

```json
{
  "task_id": "wi_v3_2026_000001",
  "version": "3.0.0",
  "mode": "rewrite",
  "intent": "persuade",
  "audience": "small_business_owner",
  "voice": "courageous_builder",
  "genre_stack": ["sales", "email", "small_business_operator"],
  "constraints": {
    "word_count_max": 300,
    "preserve_user_claims": true,
    "allow_new_claims": false,
    "citations_required": false,
    "output_mode": ["clean", "scorecard"]
  },
  "source_policy": {
    "user_text_priority": "highest",
    "memory_allowed": true,
    "web_required": false,
    "citations_required": false,
    "fabrication_tolerance": "zero"
  },
  "arena": "email",
  "high_stakes": false,
  "success_condition": "The reader understands the offer, trusts the speaker, and knows the next step.",
  "ambiguity_flags": [],
  "created_at": "2026-05-26T14:00:00Z"
}
```

---

## Definition of Done

A v3.0-conforming Intake Architect produces a contract that:

- Validates against `intake_contract.schema.json`
- Carries a non-empty `success_condition`
- Resolves or surfaces every ambiguity
- Sets `high_stakes` correctly per the detection rules
- Specifies at least one `output_mode`
- Specifies an `arena`

If any of the above fails, Pass 0 has not completed.
