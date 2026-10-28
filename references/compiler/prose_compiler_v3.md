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

## Rhythm From Meaning

These replace the retired v8 length and vocabulary quotas, which aimed at detector
statistics. There are no length, vocabulary or transition quotas.

- When several consecutive sentences do the same job at the same weight, find
  the one that carries the point and let the others support, qualify or go.
- Length changes where the thought changes shape — a turn, a concession, a
  consequence, a step in a mechanism — and nowhere else.
- Use the subject's own exact terms where it has them; never add rare or
  "surprising" words to meet a count, and never swap synonyms for a term that
  names the same thing.
- A transition earns its place by stating a real logical relation (because,
  although, unless). Remove transitions that announce rather than connect.
- Leave a sentence alone when it already carries its meaning well.
- Never target, predict or report an AI-detector score as a reason for a change.

---

## v3.0 Transformation Operations

| Op | Effect |
|---|---|
| `hard_ban_removed` | Removed a phrase from the hard-ban list |
| `soft_ban_removed` | Removed a soft-ban phrase (with earned-exception override possible) |
| `rhythm_repaired` | Reshaped sentences so rhythm follows meaning (point, support, turn) |
| `variance_injected` | **Legacy v8 name.** Accepted when reading old logs; never emitted by v9 |
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

---

## v9 Meaning-First Order (proposed) — This pass (Sentence Surgeon)

("v9 editorial pass N" names the passes of `references/v9/ENGINEERING_HANDOFF.md` §25, distinct from the numbered compiler passes.) This pass is v9 editorial passes 4 to 8 in miniature, and it runs only after claim integrity.

- **Order.** Do not rewrite a paragraph whose claims have not cleared the Epistemic Ledger (v9 editorial pass 5). Polishing an unsupported first-person claim hides it; it does not fix it.
- **Edit classes.** Every log entry also declares what kind of change it was: mechanical proofreading, suggested edit, authored revision or substantive generation (v9 principle I). `hard_ban_removed` and `compression` are normally mechanical or suggested; `specificity_added` and `abstract_to_scene` change meaning and need a source card, never invention.
- **Rhythm.** `rhythm_repaired` is logged only with the meaning reason (the thought changed shape, a transition stated no relation). The legacy `variance_injected` name stays readable in old logs and is never emitted. Do not insert typos, fragments or "imperfections" the author did not write.
- **Phrase lint as questions.** A hit from the 334-rule catalog (`prototypes/wi9/wi9_hotphrases.py`) is an editorial question: what does this sentence claim, and what evidence would make it stronger? It is not proof of anything about who wrote the text and never triggers an automatic rewrite. A kept phrase is logged `preserved` with its reason.
- **Voice and decision.** `voice_restored` is judged against consented human-origin samples (three or more per genre, 500+ words each), and a negative `voice_fidelity_delta` goes to the author, not to a model, to resolve. Semantic edits (anything beyond copyedit) wait for the author's accept or reject.
- **Not a release.** A clean rewrite log, zero hard-ban hits and an editorial score are separate from the release gate (v9 editorial pass 9). No detector score is a reason for, or evidence about, any change.
