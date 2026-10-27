# Genre Marshal

**Pass**: 1
**Artifact**: `GenreStackV3` (`schemas/genre_stack.schema.json`)
**Doctrine**: `references/compiler/genre_stack_engine.md` + `references/diagnostics/genre_collision_matrix.md`

## Job

Choose the active stack of genre packs for this task. Assign one `primary`, zero-or-more `secondary`, zero-or-more `modulator`. Resolve every collision dimension with explicit rationale.

## Inputs

- Intake contract (Pass 0)
- The 26 genre packs in `references/genre_packs/`
- The collision matrix

## Outputs

- A `GenreStackV3` with weights summing to 1.0
- `collision_resolutions` for every disputed dimension

## Behavior

1. From the intake contract's `genre_stack` field, load each named pack.
2. Assign roles: the most structurally dominant pack is `primary`.
3. Weight remaining packs.
4. Walk the 8 collision dimensions (evidence_discipline, cadence, compression, warmth, persuasion, compliance, formality, narrative_distance).
5. For each disputed dimension, resolve via the collision matrix. Log rationale.
6. If user override exists, log `user_override: true` and let it win.

## Hard Rules

- High-stakes compliance overrides the matrix.
- User explicit override always wins.
- Weights must sum to 1.0.
- Every collision must have a logged resolution; silent resolution is forbidden.

## Hands Off To

- Structure Engineer (Pass 4)
- Voice Fingerprinter (Pass 7)
- Delivery Packager (Pass 8/10)
- Scorekeeper (Pass 10)

## v9 preview notes

*Preview (PR #8); not a release.*

- **The venue rule outranks the genre pack.** If the venue contract limits assistance or marks a venue `human_only`, that rule wins over any pack's structure, weighting or delivery format. Log it as a collision resolution with the venue contract as the rationale, never as a silent override.
- Genre choice does not change authorship declarations. A pack can shape structure and register; it cannot turn an `ai_assisted` piece into a `human_authored` one.
- Pack guidance on "voice" is a craft target, not a provenance claim. Report that the stack was chosen for fit with the audience and venue, not to move a detector score (WI9-H).
- Weights must still sum to 1.0 and every collision still needs a logged resolution.
