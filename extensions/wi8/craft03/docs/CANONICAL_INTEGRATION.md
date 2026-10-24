# Canonical Integration: Map Without Forking the Engine

## Inspected upstream ownership

- `references/compiler/scene_graph.md`: beat, dialogue exchange, turn, button, plant/payoff and causal edges.
- `references/compiler/chapter_construction.md`: scene placement, spatial awareness, antagonist pressure and power dynamics.
- `references/positive_patterns/openings_and_endings.md`: existing openings and earned endings.
- `references/positive_patterns/power_dynamics.md`: objects, proxemics and social power.
- `references/genre_packs/thriller_scene_architecture.md`: action and suspense architecture.
- `references/v5/STORYWORLD_OS.md`: fictional canon, timeline, character state and canon rule tests.
- `schemas/v6/semantic_node.schema.json`: a **closed `NodeType` enum**; `narrative.*` cannot be assumed accepted.
- `scripts/check-manifest.py` and `plans/v7.manifest.yaml`: shipped-state receipts and negative control regime.

These owners were read from linked GitHub at `d4524f3caa5f75e005b23f94dcd1c71bb5002127` on 2026-10-24.

## Safe adapter protocol (NOT implemented upstream)

`v6 immutable graph root → structural extraction of canon.event + structure.scene + canon.rule + meaning.promise → temporary normalized *projection* → diagnostic evaluator → findings attached to exact source node/state digests → proposal for author review → existing v6 simulate / decide / commit path`.

The adapter must: (1) verify upstream source root/digests using v6's own native verification; (2) supply a non-counterfeit attested origin only after the schema/engine are formally adopted; (3) translate exactly-known details, never infer fictional powers or truth from mere names; (4) use the canonical IDs and version/time clocks; (5) register result dependency edges with core invalidation; (6) validate grant, authority and rights before accepting an edit; (7) on schema mismatch fail closed and produce no authoritative claim; (8) independently compare projection results against canonical scene sources. Draft fixtures are not root states.

## Required migration

The project must choose **one** pathway: extend v6's enumerated node type vocabulary through a versioned migration with tests, OR use existing `canon.*` / `structure.*` types and declare a first-class opaque, schema-tagged payload projection acceptable under the exact current policy. Do not invent `narrative.*` canonical nodes merely by writing files named that way. Never weaken type-admission constraint C018.

## No direct edits in this package

No contents of `scripts/wi.py`, `schemas/v6/*`, `references/v5/*`, `references/v6/*`, `plans/v7.manifest.yaml` or `SKILL.md` have been changed. A future merge must prepare an inspectable diff, execute v4–v7 normal + negative suites, obtain authorized review and re-read accepted state.
