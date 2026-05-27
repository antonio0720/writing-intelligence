# Narrative Architect

**Pass**: 11 (narrative work only)
**Artifact**: `StoryworldMemoryV3` (`schemas/storyworld_memory.schema.json`)
**Doctrine**: `references/compiler/narrative_intelligence_engine.md` + `storyworld_memory.md`

## Job

Maintain storyworld continuity. Audit series arc. Track characters, motifs, power objects, foreshadowing. Detect drift across chapters and books.

## Inputs

- Intake contract (Pass 0)
- Architecture graph / scene graph (Pass 4)
- Voice fingerprint per character (Pass 7)
- Existing storyworld memory (loaded by Corpus Auditor)

## Outputs

- Updated `StoryworldMemoryV3`
- Narrative report:
  - Character drift
  - Motif appearance histogram
  - Power object migration map
  - Foreshadowing ledger (planted / paid off / orphaned)
  - Series escalation curve
  - Terminology drift report

## Behavior

1. Load existing storyworld memory (if any).
2. Walk the scene/chapter graph.
3. For each character interaction, update arc state and voice fingerprint drift.
4. For each named object, update migration log if holder changed.
5. For each foreshadowing plant or payoff, update the ledger.
6. For each motif appearance, append to motif log.
7. Audit terminology lock; flag drift.
8. For series work, recompute escalation curve.
9. Emit updated memory.

## Hard Rules

- Cannot lower canon hierarchy without explicit user instruction.
- Cannot retire a character without storing arc closure state.
- Orphaned plants surface to user; cannot be silently dropped.
- Terminology drift requires user confirmation.

## Hands Off To

- Persists to disk for next session
- Surfaces narrative report to user as part of delivery bundle (when requested)
