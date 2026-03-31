---
name: writing-intelligence
author: Antonio T. Smith Jr. / Density6 LLC
version: "1.0"
license: MIT
repository: https://github.com/writing-intelligence/writing-intelligence
description: >
  Sovereign Writing Intelligence Compiler — 6-pass pipeline producing signature-grade
  prose with authorial sovereignty and zero AI residue. Use whenever writing, editing,
  rewriting, drafting, or revising ANY text: essays, strategy docs, sermons, fiction,
  sales copy, investor memos, speeches, academic papers, manifestos, dialogue, emails,
  or any prose. Trigger on: write, rewrite, edit, draft, revise, ghostwrite, clean up,
  prose, essay, chapter, sermon, speech, pitch, copy, memo, manifesto, report, narrative,
  dialogue, score draft, grade writing, audit prose, voice, tone, style, anti-slop,
  human-sounding, AI detection, writing quality, remove AI voice, improve writing,
  strengthen, make it sound human.
---

# Writing Intelligence Compiler v1.0

## Purpose

This skill is a multi-pass writing compiler. It does not merely remove AI tells.
It produces prose with authorial identity, argument force, epistemic discipline,
structural unpredictability, and sentence-level variance that no statistical
detector can flag — because the output is genuinely well-written by human
standards, not merely cleaned of machine patterns.

**Center of gravity**: Produce signature-grade writing with force, truth
discipline, and authorial sovereignty.

---

## Architecture: 6-Pass Compilation Pipeline

Every piece of writing processed by this skill runs through six sequential
passes. Passes may be skipped only when explicitly irrelevant (e.g., Pass 5
stress-test on a casual email). The default is ALL passes.

### Pass 0 — Mission Lock

Before writing a single word, declare:

- **Intent**: What must this text DO? (inform / convert / warn / teach / dignify / dominate / comfort / reveal / mobilize / persuade / entertain / defend)
- **Audience**: Who reads this? (calibrate vocabulary, abstraction, evidence expectations)
- **Voice**: Which voiceprint applies? (read `references/voiceprints/`)
- **Genre**: Which genre pack governs? (read `references/genre_packs/`)
- **Success condition**: One sentence describing what "worked" looks like

### Pass 1 — Diagnostic Scan

Read `references/anti_patterns/phrases.md`, `references/anti_patterns/structures.md`,
`references/anti_patterns/cadence.md`, and `references/anti_patterns/fake_depth.md`.

Identify:
- AI residue (phrases, structures, cadence patterns)
- Contradictions within the text
- Vagueness (claims without actors, actions, stakes, or specifics)
- Cadence repetition (sentence-length uniformity, transition homogeneity)
- Argument gaps (unsupported claims, missing premises)
- Evidence gaps (assertions without backing)
- Tone drift (sections that shift register without cause)
- Perplexity flatness (vocabulary predictability across paragraphs)
- Burstiness deficit (lack of sentence-length variance)

### Pass 2 — Structural Rewrite

Read `references/positive_patterns/paragraph_shapes.md` and
`references/compiler/section_architecture.md`.

Fix:
- Section order (does the argument build or meander?)
- Paragraph sequence (does each paragraph earn its position?)
- Thesis placement (is the core claim findable and load-bearing?)
- Redundancy collapse (merge paragraphs saying the same thing differently)
- Entry/exit strength (do sections open with force and close with resolve?)

### Pass 3 — Sentence Surgery (Anti-Slop Layer)

Apply the rules from the anti-pattern references. Key principles:

**Hard Bans** — never use under any circumstances:
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

**Soft Bans** — remove unless they earn their place:
- Adverbs (keep only when removal changes factual meaning)
- Em dashes (allow only when they improve timing more than comma/colon)
- Semicolons in casual prose
- "However" as sentence opener (prefer structural contrast)
- Parenthetical asides longer than 8 words
- Sentences beginning with "And" or "But" more than once per 500 words

**Earned Exceptions** — allowed when they serve a real function:
- Rhetorical questions that open genuine tension (not fake insight)
- One-sentence paragraphs that deliver impact (not manufactured drama)
- Fragment sentences for rhythm (not lazy construction)
- Repetition for rhetorical force (not padding)

**Variance Injection Rules**:
- No three consecutive sentences within ±5 words of each other in length
- No two consecutive paragraphs with the same opening syntactic structure
- Vocabulary must include at least 2 domain-specific or uncommon words per 300 words
- Transition variety: no single transition word/phrase used more than twice in 1000 words
- At least one sentence per 500 words must be ≤6 words
- At least one sentence per 500 words must be ≥30 words

### Pass 4 — Voice Restoration

Read the applicable voiceprint from `references/voiceprints/`.

After cleanup, prose often flattens. This pass reinjects:
- Sentence aggression level
- Abstraction tolerance
- Metaphor density
- Emotional temperature
- Cadence profile (short-long patterns, paragraph rhythm)
- Humor allowance
- Directness ceiling
- Authority posture

The voiceprint is the author's fingerprint. Without it, clean prose is still
generic prose. The detector sees generic. The reader sees nobody.

### Pass 5 — Stress Test

Before finalizing, interrogate:

1. What would a skeptical, smart reader attack first?
2. What sentence feels like it could appear in any AI output?
3. What could be cut without losing meaning?
4. What line actually lands — would someone underline it?
5. Does the opening earn the reader's next 30 seconds?
6. Does the closing leave residue in the reader's mind?
7. Is there a single sentence a human would never write this way?

If any answer reveals weakness, return to the relevant pass.

### Pass 6 — Output Modes

Return the requested output(s):

- **clean**: Final draft, no markup
- **annotated**: Draft with margin notes explaining decisions
- **redline**: Original with tracked changes
- **scorecard**: Full 100-point evaluation (see Diagnostics)
- **violations**: List of every rule triggered and how it was resolved
- **next-pass**: Recommendations for further improvement

Default output is **clean** unless the user requests otherwise.

---

## Scoring System (100 Points)

Read `references/diagnostics/scorecard.md` for full rubric.

| Category | Points | What It Measures |
|---|---|---|
| Clarity | 10 | Can a reader parse every sentence on first read? |
| Specificity | 10 | Named actors, actions, stakes, numbers, examples? |
| Rhythm | 10 | Sentence-length variance, paragraph cadence, musicality? |
| Voice Integrity | 10 | Does it sound like a specific author, not a model? |
| Argument Strength | 15 | Premises support conclusions? Logic holds under pressure? |
| Evidence Discipline | 15 | Claims backed? Sources real? Quantifiers honest? |
| Density | 10 | Every sentence earns its place? No filler? |
| Audience Fit | 10 | Register, vocabulary, and depth match the reader? |
| Memorability | 5 | Any line a reader would quote or remember? |
| Structural Control | 5 | Sections do their declared jobs? Arc resolves? |

**Grade Thresholds**:
- Below 70: Weak — significant revision required
- 70–79: Usable but soft — tighten argument and voice
- 80–89: Strong — publishable with minor polish
- 90–94: Elite — distinctive, defensible, memorable
- 95–100: Signature-grade — this could only have come from this author

**Automatic Fail Conditions** (score capped at 65 regardless of other marks):
- Three or more hard-ban phrases detected
- Perplexity flatness across 5+ consecutive sentences
- Zero domain-specific vocabulary in 500+ words
- Argument contains unsupported universal claim
- Fabricated citation, statistic, or quote

---

## Voiceprint System

Read the applicable file from `references/voiceprints/`. Available profiles:

- `sovereign_commander.md` — Cold authority, strategic compression, zero filler
- `literary_recursive.md` — Layered, subtext-rich, image-driven, temporal loops
- `sermon_black_church.md` — Cadence, dignity, scriptural grounding, call-response
- `investor_precision.md` — Data-forward, risk-aware, actionable, no adjectives
- `founder_manifesto.md` — Vision-heavy, conviction-dense, future-claiming
- `academic_rigorous.md` — Evidence-first, qualification-aware, citation-dense
- `casual_sharp.md` — Conversational but intelligent, no hand-holding
- `custom` — Build from user-provided samples (minimum 3 samples, 500+ words each)

To build a custom voiceprint, analyze samples for: average sentence length,
sentence-length standard deviation, paragraph length distribution, vocabulary
tier, metaphor frequency, transition preferences, opening patterns, closing
patterns, comma frequency, question frequency, and dominant syntactic structures.

---

## Genre Packs

Read the applicable file from `references/genre_packs/`. Each pack adjusts the
compiler's weighting matrix:

- `strategy.md` — Evidence weight ↑, sequence ↑, operational clarity ↑
- `sermon.md` — Cadence ↑, spiritual resonance ↑, dignity ↑, applause architecture ↑
- `fiction.md` — Scene embodiment ↑, subtext ↑, image originality ↑
- `sales.md` — Trust ↑, friction removal ↑, objection anticipation ↑, CTA integrity ↑
- `academic.md` — Citation ↑, qualification ↑, claim-evidence binding ↑
- `speech.md` — Delivery rhythm ↑, audience calibration ↑, applause architecture ↑
- `email.md` — Compression ↑, action clarity ↑, tone precision ↑
- `pitch_deck.md` — Data density ↑, narrative arc ↑, ask clarity ↑
- `legal_positioning.md` — Precision ↑, hedging ↑, precedent awareness ↑
- `cinematic_narration.md` — Atmosphere ↑, pacing ↑, sensory density ↑, shot-based structure ↑
- `dialogue.md` — Character voice distinction ↑, subtext ↑, rhythm ↑, attribution technique ↑
- `government_brief.md` — Plain language ↑, statutory precision ↑, BLUF ↑, agency calibration ↑
- `medical_writing.md` — Evidence hierarchy ↑, clinical precision ↑, IMRAD structure ↑
- `patent_claims.md` — Claim structure ↑, antecedent basis ↑, enablement ↑, prior art framing ↑

---

## Rewrite Operators

These are reversible transformation commands. Apply individually or in sequence:

| Operator | Effect |
|---|---|
| `compress(N%)` | Reduce word count by N% without losing meaning |
| `raise_intelligence` | Increase sophistication without increasing jargon |
| `add_specificity` | Replace abstractions with named actors, numbers, examples |
| `abstract_to_scene` | Convert conceptual passage into grounded narrative |
| `sharpen_thesis` | Make the core claim more precise and defensible |
| `strip_corporate` | Remove institutional voice patterns |
| `make_colder` | Reduce warmth, increase analytical distance |
| `make_warmer` | Increase empathy signals without sentimentality |
| `make_executable` | Convert insight into action steps |
| `genre_transfer(from, to)` | Rewrite in target genre while preserving content |
| `audience_shift(from, to)` | Adjust register for different reader |
| `inject_variance` | Add sentence-length and vocabulary unpredictability |
| `kill_padding` | Remove every sentence that doesn't advance the argument |
| `strengthen_closing` | Rewrite the final paragraph for maximum residue |

---

## Epistemic Integrity Layer

Every draft must classify sentences as:

- **Observed fact**: Writer witnessed or measured it
- **Sourced fact**: Attributed to a named, verifiable source
- **Inference**: Logical derivation from stated facts
- **Synthesis**: Combination of multiple sources into a new claim
- **Recommendation**: Prescriptive statement
- **Rhetoric**: Persuasive move not grounded in evidence

Enforcement rules:
- Sourced facts require citations
- Inferences must identify their premises
- Recommendations must state the basis
- Rhetoric must not masquerade as fact
- Universal quantifiers ("all," "every," "never," "always") require evidence or qualification
- Inflated verbs ("revolutionize," "transform," "redefine") require concrete backing
- No fabricated citations, statistics, quotes, or studies — ever

---

## Paragraph Physics

Read `references/positive_patterns/paragraph_shapes.md` for full detail.

Every paragraph is audited for:

- **Entry force**: Does the first sentence compel continuation?
- **Sentence variety**: Length, structure, and rhythm within the paragraph
- **Midpoint turn**: Does something shift, deepen, or complicate mid-paragraph?
- **Exit type**: Launch (propels to next), Land (resolves), Hang (creates tension)
- **Purpose**: What job does this paragraph do? (define / prove / contrast / narrate / warn / persuade / operationalize / close)
- **Overlap**: Does it repeat what the previous paragraph already said?
- **Compression opportunity**: Can it lose 20%+ without damage?

---

## Section Architecture

Read `references/compiler/section_architecture.md`.

Each section declares its job:
- Define / Prove / Contrast / Narrate / Warn / Persuade / Operationalize / Close

Then the compiler scores whether the section actually performed that job.
A section that declares "Prove" but only asserts is flagged.

---

## Argument Topology

For persuasive, academic, or strategic writing, audit:

- **Claim order**: Are claims sequenced for maximum cumulative force?
- **Premise strength**: Is each premise load-bearing or decorative?
- **Hidden assumptions**: What does the argument take for granted?
- **Evidence-to-assertion ratio**: How many claims per supporting fact?
- **Escalation logic**: Does the argument build, or does it plateau?
- **Redundancy collapse**: Are two paragraphs making the same point?
- **Ending strength**: Does the conclusion do more than summarize?

---

## Cliché and Pattern Collision Detection

Beyond phrase bans, detect cadence signatures:

- **LinkedIn cadence**: Short declarative. Line break. Another one. "And that changes everything."
- **Startup guru cadence**: "Most people think X. They're wrong. Here's why."
- **TED-talk cadence**: "What if I told you..." + pause bait + anecdote + universal lesson
- **Fake profundity**: Abstract noun + "is" + another abstract noun. "Simplicity is the ultimate sophistication."
- **LLM list rhythm**: Sentence. Sentence. Sentence. All same length. All same structure.
- **Performative empathy**: "I see you. I hear you. This matters." (without specific referent)
- **Fake decisiveness**: "The answer is simple:" (before something not simple)
- **Trailer voice**: "In a world where..." / short punchy fragments / dramatic pause

Flag any passage that matches 3+ characteristics of any single cadence signature.

---

## Intelligence-Grade Evaluators

### Abstraction Ladder
Flags when prose floats above concrete reality for more than 3 consecutive
sentences. Forces grounding: name an actor, a number, an example, or a scene.

### Concreteness Injector
Converts "significant progress was made" → "[Actor] completed [specific thing]
by [date], reducing [metric] from [X] to [Y]."

### Reader Respect Meter
Catches over-explaining, hand-holding, stating the obvious, and fake intimacy.
If the reader would think "I know that already" or "don't patronize me," cut it.

### Dominance vs. Warmth Selector
A dial, not a toggle. Strategic writing sits at 80/20 dominance/warmth.
Pastoral writing inverts. Sales copy oscillates. The skill adjusts per genre.

### Concept Density Meter
Prevents idea stacking without oxygen. No more than 2 novel concepts per
paragraph without an example, analogy, or breathing room between them.

### Originality Pressure Test
For every sentence, ask: could this appear in 10,000 other AI outputs? If yes,
rewrite until the answer is no. The sentence must bear the author's fingerprint.

---

## Academic Mode

Read `references/academic/` for full college-writing extensions.

Key additions for academic contexts:
- Course rubric compiler (extract and map to grading criteria)
- Claim-evidence binding (every paragraph tagged: claim/evidence/explanation)
- Citation intelligence (coverage gaps, source quality, paraphrase distance)
- Discipline-specific reasoning packs
- Anti-hallucination rules (no invented quotes, page numbers, studies, statistics)
- Authorship proof layer (draft provenance, revision fingerprint, idea origin map)
- Paragraph blueprints by function (thesis, close-reading, compare/contrast, method, rebuttal)
- Class-note anchoring (lecture terms, professor vocabulary, course-specific debates)
- Fact/inference/interpretation classifier

---

## Memory and Continuity (Longform)

For multi-chapter or multi-document projects:
- Character voice continuity tracking
- Thesis continuity verification
- Repeated metaphor detection
- Contradiction checking across sections
- Emotional arc continuity
- Terminology lock (same concept = same word throughout)

---

## File Reference Map

When this skill triggers, read files in this order based on the task:

1. **Always**: This SKILL.md (you're reading it)
2. **Always**: `references/anti_patterns/phrases.md`
3. **If editing/rewriting**: `references/anti_patterns/structures.md` + `cadence.md`
4. **If deep cadence analysis**: `references/anti_patterns/cadence_expanded.md` (50+ patterns)
5. **If genre-specific clichés detected**: `references/anti_patterns/genre_slop.md`
6. **If authority claims feel hollow**: `references/anti_patterns/fake_authority.md`
7. **If abstract prose needs grounding**: `references/positive_patterns/scene_grounding.md`
8. **If voice matters**: applicable voiceprint from `references/voiceprints/`
9. **If building a custom voice**: `references/voiceprints/custom_voiceprint_builder.md`
10. **If genre-specific**: applicable genre pack from `references/genre_packs/`
11. **If auto-configuring pipeline**: `references/compiler/auto_mode.md`
12. **If scoring**: `references/diagnostics/scorecard.md`
13. **If generating a full audit**: `references/diagnostics/auto_diagnostic_report.md`
14. **If diagnosing failures**: `references/diagnostics/failure_modes.md`
15. **If academic**: `references/academic/academic_mode.md` + `references/academic/discipline_primitives.md`
16. **If argument-heavy**: `references/compiler/section_architecture.md`
17. **If transferring between genres**: `references/compiler/style_transfer.md`
18. **If longform (single session)**: `references/compiler/continuity.md`
19. **If longform (multi-session)**: `references/compiler/memory_system.md`
20. **If auditing multiple documents**: `references/compiler/cross_document_audit.md`
21. **If rewriting**: `references/diagnostics/rewrite_operators.md`
22. **If calibrating against examples**: `tests/gold_output_library.md`
23. **If stress-testing output**: `tests/adversarial_cases.md`
24. **If benchmarking against detectors**: `tests/detector_benchmark_suite.md`
