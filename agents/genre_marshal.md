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
