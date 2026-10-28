# Integration contract: Writing Intelligence mainline

## Baseline observed

`antonio0720/writing-intelligence`, branch `main`, observed commit `d4524f3caa5f75e005b23f94dcd1c71bb5002127` on 2026-10-24 using the connected GitHub repository. `README.md` reports v7.0.0. The existing compiler owns the 11 passes and canonical WI Python runtime; fiction is governed by the Fiction v2 pack, chapter construction, Narrative Intelligence Engine, Storyworld OS and storyworld schema. It already has `/tests/v7`, `/schemas/v6`, and `plans/v7.manifest.yaml` with shipped receipts. Do not rewrite its history or claim these new tests are v8 platform acceptance.

## Safe installation (add-only, no source override)

1. Verify the upstream commit and reconcile if main has moved. `git rev-parse HEAD` must be reviewed against the pinned baseline; do not auto-reset upstream.
2. Extract the package to a **new directory** and inspect file list. It contains only new paths relative to the repo, not replacement versions of pre-existing canonical docs. `UPGRADE_README.md` and `provenance/*` are packaging support.
3. From the target clone, copy new paths without overwrite. Example with GNU/macOS tools: `cp -Rn /path/to/package/{rules,policies,schemas,scripts,tests,docs,references,benchmarks,plans,provenance} .` but **beware** `cp -Rn` recursion is platform-dependent; use `scripts/install_additive.py --target /path/to/clone` for collision-safe dry run and installation.
4. Run `python3 scripts/wi-fiction.py validate --input tests/v8/fixtures/valid_draft.json` and `bash tests/v8/run.sh` from the clone root; then run the existing `python3 scripts/wi.py doctor`, `tests/v4/test_wi.sh`, `tests/v5/test_wi5.sh`, `tests/v6/test_wi6.sh`, `tests/v7/test_wi7.sh`, and `scripts/build-skill.sh` on the **actual cloned repository**.
5. Review and implement the adapter described below only after the old canonical graph and provenance contracts are read. PR and CI acceptance are separate. Do not label v8 shipped or add a CLI claim to `README.md` until verified.

## Existing owner → additive module → future insertion point

| Existing canonical owner | Proposed additive docs/code | Required canonical change (not included as a destructive replacement) |
|---|---|---|
| `references/genre_packs/fiction.md` | `references/genre_packs/fiction_v8_addendum.md` | change 'Character as Function' from identity rule to scene-contribution lens; refer to FI-25 and FI-12 |
| `references/genre_packs/thriller_scene_architecture.md` | `references/compiler/novel_architecture.md` | make five beats selectable instead of mandatory; preserve exception record |
| `references/positive_patterns/tension_mechanics.md` | `references/v8/FICTION_INTELLIGENCE_CONSTITUTION.md` | fixed eight-phase compression sequence becomes technique with scope; no default hard gate |
| `references/compiler/narrative_intelligence_engine.md` | `references/compiler/novel_architecture.md` | consume typed work summaries and treat total novel state as distinct from scene state |
| `references/v5/STORYWORLD_OS.md` | `references/compiler/fiction_rule_integrity.md` | map sidecar world rule IDs to `canon.*` nodes, preserve realm and bitemporal history |
| `references/compiler/continuity.md` | `references/compiler/novel_architecture.md` | ambiguity and repetition detection to work-level index and reader state |
| `references/diagnostics/scorecard.md` | `references/compiler/reader_experience.md` | separate machine coverage, developmental judgment and human reader evidence |
| `agents/narrative_architect.md` | `rules/fiction_v8_rules.json` | call sidecar as a read-only inspector; never upgrade `SIGNAL` to approved |
| `scripts/wi.py` | `scripts/wi-fiction.py` | integrate via canonical proposal/authority APIs after tests; do not call sidecar an official wi subcommand yet |
| `services/api/src/runtime/Kernel.ts` | none replaced | future REST adapter requires authorization, request caps and explicit fiction mode; not implemented |

## Future semantic sidecar adapter

Map `canon.*` and `StoryworldMemoryV3` to IR IDs without retyping source truth. Every IR record must carry `source_node_id`, `source_state_digest`, `canon_tier`, `realm=fictional_canon`, `valid_from`, `known_from`, `provenance`. Validate that the source digest and repository root are current before trusting sidecar results. If a sidecar proposes prose edits, convert to native WI proposals. A change that modifies fictional world rules or character state requires a canon decision; only wording-only edits may take an authorized automatic path, and only when the existing policy allows it.

## Build and release hazards

`SKILL.md` reports two `.skill` bundles due to a 200-file cap. New files **must not silently be stuffed into the wrong bundle or exceed the cap**. Inspect and update `scripts/build-skill.sh` and both delivery manifests, including reachability of rule docs and runtime files. The package does not claim bundle acceptance.

The v7 manifest is a different program: do not mark its waves shipped on the strength of v8 fiction tests. For a formal v8 release, create a new authoritative program manifest and receipt format compatible with `scripts/check-manifest.py`, with actual console output, negative controls and remote readback. The included `plans/v8-fiction.proposal.json` is an explicit proposal, not a substitute for a WI release receipt.

## v9 preview: integration notes

*Preview (PR #8); proposed, not a release. v8.0.0 is the published version.*

- v9 is additive on the same mainline. It adds `scripts/wi-authorship.py`, `schemas/v9/`, `references/v9/` and `prototypes/wi9/`; it removes nothing from the install list above and does not change the v7 CLI, or the fiction sidecar. The 200-file bundle ceiling still applies; re-check the file count before building any bundle that includes v9 files.
- Add the v9 checks to the verification list for a clone that carries them: `python3 -m unittest discover -s tests/v9 -p 'test_*.py'` alongside `tests/v7/test_wi7.sh`.
- A fiction sidecar result does not feed the authorship checker, and the checker does not feed fiction gates. They are separate questions: whether the story holds, and what the author declares about who wrote it.
- The published release is v8.0.0. Do not mark any v9 wave shipped on the strength of fiction tests; wave states live in `references/v9/WAVES.yaml`.
