# Narrative Intelligence Engine

**Purpose**: Expand v2.0 Fiction Intelligence into longform, series, and transmedia architecture. Produces storyworld memory, series arc audits, and cross-book voice fidelity scores.

**Schema**: `schemas/storyworld_memory.schema.json` (`StoryworldMemoryV3`)

**Agent**: Narrative Architect (`agents/narrative_architect.md`)

---

## When This Engine Runs

The Narrative Architect runs only for: fiction, story, screenplay, scene, lore, transmedia, chapter, novel, short story, audio drama, game cutscene, comic, or any narrative content with a storyworld.

For non-narrative prose, this engine is skipped.

---

## What It Tracks

### Characters

Every character is recorded with:

- `character_id`, `name`, `archetype` (one of 12 character roles + protagonist / antagonist / supporting)
- `voice_fingerprint_id` — linked to a measurable voice profile
- `tells` — observable behaviors that signal the character
- `fatal_vulnerability` — the thing that, when revealed, decides outcomes
- `first_appearance` and `last_appearance`
- `arc_state` — current position in their arc

### Motifs

Recurring images, phrases, objects, weather, color, sound — anything that gains meaning by repetition. Each motif logs every appearance.

### Power Objects

Items that confer power and migrate between characters. Each power object carries a `migration_log` recording every transfer.

### Foreshadowing Ledger

Every plant logs `plant_location` and target `payoff_location`. Status:

- `planted` — placed; not yet paid off
- `paid_off` — payoff delivered
- `orphaned` — plant exists, payoff never arrived (must surface)
- `telegraphed` — plant is too obvious (must surface)

### Series Arc

For multi-book or multi-season work:

- `escalation_curve` — rising / plateau / declining / uneven
- `stakes_per_book` — measured stakes score per installment
- A plateau curve across 3+ books = the series is repeating itself

### Terminology Lock

Concept-to-canonical-word map. Same concept = same word across the entire storyworld. Prevents drift: if "the operative" is the word for the protagonist's profession in book one, "the agent" cannot appear in book three.

---

## Canon Hierarchy

The engine maintains three tiers:

| Tier | What | Authority |
|---|---|---|
| Canonical | Author-approved source material | Final word |
| Sanctioned | Adaptations, audio dramas, transmedia | Subordinate; cannot rewrite canon |
| Fan tier | Community work | Acknowledged; not authoritative |

When sanctioned and canonical conflict, canonical wins. The engine logs the conflict.

---

## Series Continuity Audit

Run at chapter boundaries, book boundaries, and on demand. Produces:

- Character voice fingerprint drift report per character
- Motif appearance histogram (frequency, gaps, dead motifs)
- Power object migration map (orphaned objects, broken chains)
- Foreshadowing ledger summary (planted / paid off / orphaned counts)
- Stakes escalation curve
- Terminology drift report

---

## Cross-Format Consistency

For transmedia work (novel + audio drama + AR + game), the Narrative Architect enforces:

- Voice fingerprint stability per character across formats
- Power object continuity (the locket in the audio drama is the locket in the novel)
- Plant-payoff continuity across formats (a plant in the audio drama can pay off in the novel — must be tracked)
- Terminology lock applied universally

See `references/genre_packs/transmedia_character.md` for format-specific rules.

---

## Output

The engine emits a `StoryworldMemoryV3` artifact that:

- Validates against `storyworld_memory.schema.json`
- Updates with every chapter / scene / installment
- Persists across sessions (loaded by Pass 2 Corpus Auditor)
- Powers Pass 4 (scene graph) and Pass 11 (memory update)

---

## Audit Questions (Per Run)

1. Has any character's archetype shifted without narrative cause?
2. Has any character's voice fingerprint drifted from baseline > 15%?
3. Are there orphaned plants? Are there unplanted payoffs?
4. Has any motif appeared once then disappeared (dead motif)?
5. Has the terminology lock been broken anywhere?
6. Is the stakes escalation curve positive?
7. Is the power object migration chain unbroken?
8. Does the canonical-sanctioned-fan hierarchy hold?

Any "yes" to a problem question surfaces for the user.

---

## Definition of Done

The Narrative Architect emits a storyworld memory that:

- Validates against `storyworld_memory.schema.json`
- Contains every character introduced in the current work
- Logs every plant and payoff
- Tracks every power object migration
- Reports the series arc state
- Persists for future sessions

If any of the above fails, the engine has not completed.
