# Prose Compiler v3 — Pass 6

**Purpose**: Preserve v2.0's sentence-level excellence while making every transformation testable, logged, and voice-impact-aware.

**Schema**: `schemas/prose_rewrite_log.schema.json` (`ProseRewriteLogV3`)

**Agent**: Sentence Surgeon (`agents/sentence_surgeon.md`)

---

## What Changed from v2.0

v2.0 applied anti-pattern rules and trusted the user to inspect results. v3.0 logs every transformation in a structured rewrite log so the user can audit decisions and so regression tests can compare runs.

Every cut, strengthening, and preservation is recorded with:

- The transformation operation
- The before-text and the after-text
- The rule that triggered it
- The rationale
- The voice impact (`increased_fidelity`, `neutral`, `decreased_fidelity`)

---

## Tier System (Preserved from v2.0)

### Hard Bans

Never use under any circumstances:

- "Here's the thing" / "Let's be clear" / "It's worth noting"
- "In today's [anything]" / "In an era of" / "In a world where"
- "At its core" / "At the end of the day" / "When all is said and done"
- "Game-changer" / "Paradigm shift" / "Double-edged sword"
- "It's not just X — it's Y" / "Not only X, but Y"
- "The question isn't X — it's Y"
- "Think about it" / "Let that sink in" / "Read that again"
- "Spoiler alert" / "Plot twist" / "Here's the kicker"
- "Full stop" / "Period" / "Mic drop"
- Stacked rhetorical questions as pseudo-argument
- "I" as first word of the piece (unless personal essay requires it)

### Soft Bans

Remove unless they earn their place:

- Adverbs (keep only when removal changes factual meaning)
- Em dashes (allow only when they improve timing more than comma/colon)
- Semicolons in casual prose
- "However" as sentence opener (prefer structural contrast)
- Parenthetical asides longer than 8 words
- Sentences beginning with "And" or "But" more than once per 500 words

### Earned Exceptions

Allowed when they serve a real function:

- Rhetorical questions that open genuine tension (not fake insight)
- One-sentence paragraphs that deliver impact (not manufactured drama)
- Fragment sentences for rhythm (not lazy construction)
- Repetition for rhetorical force (not padding)

---

## Variance Injection Rules

- No three consecutive sentences within ±5 words of each other in length
- No two consecutive paragraphs with the same opening syntactic structure
- Vocabulary must include at least 2 domain-specific or uncommon words per 300 words
- Transition variety: no single transition word/phrase used more than twice per 1000 words
- At least one sentence per 500 words must be ≤ 6 words
- At least one sentence per 500 words must be ≥ 30 words

---

## v3.0 Transformation Operations

| Op | Effect |
|---|---|
| `hard_ban_removed` | Removed a phrase from the hard-ban list |
| `soft_ban_removed` | Removed a soft-ban phrase (with earned-exception override possible) |
| `variance_injected` | Modified sentence length / structure to break repetition |
| `compression` | Removed words without losing meaning |
| `specificity_added` | Replaced abstraction with concrete actor / number / example |
| `abstract_to_scene` | Converted conceptual passage into grounded narrative |
| `voice_restored` | Restored authorial fingerprint signal after cleanup |
| `preserved` | Explicitly kept against a soft-ban (earned-exception override) |
| `rhetorical_question_kept_earned` | Kept rhetorical question because it opens genuine tension |
| `fragment_kept_earned` | Kept fragment because it serves rhythm |
| `transition_replaced` | Swapped overused transition for variety |
| `metaphor_added` | Added metaphor where prose was floating abstract |
| `metaphor_removed` | Removed metaphor that was decorative, not load-bearing |
| `claim_softened` | Resolved universal-quantifier flag from Pass 5 |
| `claim_qualified` | Added explicit hedge to a claim |
| `evidence_attached` | Inserted citation per Pass 5 decision |

---

## Voice Impact Tracking

Every transformation declares its impact on voice fidelity:

- `increased_fidelity` — the change made the prose sound more like the target voice
- `neutral` — no fidelity change
- `decreased_fidelity` — the change made the prose less like the target voice (sometimes necessary for clarity / compliance / accuracy)

The summary aggregates `voice_fidelity_delta`. A negative delta is allowed but flagged for the Voice Fingerprinter (Pass 7) to address.

---

## Compression Discipline

When the intake contract specifies `compress(N%)`:

- Target: reduce word count by exactly N% ± 5%.
- Constraint: no meaning loss. Every claim, premise, and concrete detail in the source must survive (compressed, not deleted).
- Rule: if a claim cannot survive compression, surface to the user — do not silently drop it.
- Log every removed sentence with rationale.

---

## Paragraph Physics (Preserved)

Every paragraph is audited for:

- **Entry force** — does the first sentence compel continuation?
- **Sentence variety** — length, structure, rhythm within the paragraph
- **Midpoint turn** — does something shift, deepen, complicate mid-paragraph?
- **Exit type** — Launch (propels to next), Land (resolves), Hang (creates tension)
- **Purpose** — define / prove / contrast / narrate / warn / persuade / operationalize / close
- **Overlap** — does it repeat what the previous paragraph already said?
- **Compression opportunity** — can it lose 20%+ without damage?

---

## Example Rewrite Log Entry

```json
{
  "transformation_id": "t14",
  "op": "hard_ban_removed",
  "before": "Here's the thing — our model produces results.",
  "after": "Our model produces results.",
  "rationale": "Hard-ban phrase 'Here's the thing' removed. Sentence carries the same meaning with less filler.",
  "rule_id": "hb_001",
  "voice_impact": "increased_fidelity"
}
```

---

## Definition of Done

The Sentence Surgeon emits a rewrite log that:

- Validates against `prose_rewrite_log.schema.json`
- Contains a transformation entry for every detectable edit
- Reports a non-negative aggregate voice fidelity delta (or surfaces the negative delta for Pass 7 to resolve)
- Leaves zero unaddressed hard-ban hits

If any of the above fails, Pass 6 has not completed.
