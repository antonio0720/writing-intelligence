# Storyworld Memory — Doctrine

**Schema**: `schemas/storyworld_memory.schema.json`

**Read alongside**: `references/compiler/narrative_intelligence_engine.md`

---

## Purpose

Storyworld memory is the canonical record of everything that persists across scenes, chapters, books, and formats in a fictional or narrative-nonfiction project. It is the operating system for long-form continuity.

Without storyworld memory:
- Characters drift
- Motifs die
- Power objects vanish
- Plants are orphaned
- Series plateau

With storyworld memory, every chapter inherits the full state of the world and contributes back. Continuity becomes auditable instead of accidental.

---

## When to Initialize

Initialize a storyworld memory the first time a project crosses any of these thresholds:

- 2+ chapters (continuity matters)
- 2+ books / installments (series)
- 2+ formats (transmedia — novel + audio drama, e.g.)
- 5+ named characters
- Any planted-and-paid-off foreshadowing
- Any character whose voice must remain stable across appearances

---

## What It Records

See `schemas/storyworld_memory.schema.json` for the full structure. Summary:

- **Canon hierarchy**: canonical / sanctioned / fan-tier
- **Characters**: archetype, voice fingerprint, tells, fatal vulnerability, arc state
- **Motifs**: every appearance logged
- **Power objects**: migration log per object
- **Foreshadowing ledger**: planted / paid off / orphaned / telegraphed
- **Series arc**: escalation curve, stakes per book
- **Terminology lock**: concept → canonical word

---

## How It Updates

Updates happen in Pass 11 (Memory & Benchmark Update) after every compilation. The Narrative Architect emits a delta against the prior state:

- New characters → appended
- Character changes → arc_state updated, fingerprint drift logged
- New plants → ledger entry created
- Plants paid off → status updated
- Power object transfers → migration entry appended
- New motifs → motif entry created
- Motif appearances → appearance list updated
- Terminology changes → flagged for user resolution (drift is rarely desirable)

---

## Cross-Format Notes

For transmedia projects, the same `storyworld_memory` powers:

- Novel chapters
- Audio drama scripts (`references/genre_packs/transmedia_character.md`)
- Game cutscenes (`bcc-sovereign-runtime-unified` / D6 game pipelines)
- AR experiences
- Lore bibles
- Character diaries

Each format reads the storyworld memory before producing content and writes back updates after.

---

## Voice Fingerprint Per Character

Each character carries a `voice_fingerprint_id` pointing to `schemas/voice_fingerprint.schema.json`. This is what makes "can I tell who's speaking with names removed?" a measurable question.

When a character drifts beyond ±15% on any major fingerprint metric (avg sentence length, abstraction tolerance, metaphor density, dominant syntactic structure), the Narrative Architect surfaces the drift for the writer to confirm or correct.

---

## The Operating Promise

If a writer abandons a project for six months, returns, and reads the storyworld memory, they should be able to resume mid-chapter without re-reading the entire series. That is the promise. Storyworld memory makes longform sovereign.
