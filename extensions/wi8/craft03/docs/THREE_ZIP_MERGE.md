# Three-Way Merge Contract — ZIP #1 + ZIP #2 + ZIP #3

**Independent root namespace for ZIP #3:** `extensions/wi8/craft03/`. Its installer never writes outside that subtree. ZIP #1 owns B001–B060 prose/fiction diagnostics. ZIP #2 owns N061–N120 want/need/arc/ending semantics. ZIP #3 owns C121–C180 opening/action/opposition/suspense/sequence semantics. Neither this package nor the others should be flattened into repository root.

## Merge procedure

1. Pin exact starting commit of `writing-intelligence/main`. Compare to baseline `d4524f3caa5f75e005b23f94dcd1c71bb5002127`. Stop if HEAD changed until reviewing its diff.
2. Extract each ZIP to *separate staging folders*. Check all SHA256SUMS and receipt labels. No `--overwrite` extraction into existing repository directories.
3. Install ZIP #3 at `extensions/wi8/craft03/` with the `install_craft03_additive.py` command. It is dry-run unless `--apply`; it refuses any existing destination even if bytes appear equal.
4. Resolve the canonical owner of scene and character IDs. Preserve one graph identity model and v6's inherited bitemporal and authority rules. ZIPs provide distinct projections, not independent stores.
5. Merge semantics, not files by basename: B019 mystery ledger governs promise debt, B017 knowledge asymmetry governs suspense, B036 power boundaries governs action exceptions, N061+ want/need governs sequence goal consequences, C159 is an extension over B019 not a new debt database.
6. Compose JSON Schema namespaces into one versioned dependency graph. Validate typed referents and actual canonical graph exports using existing state-digest logic. Reject records with mismatched schema or provenance.
7. Run the three packages' own suites unchanged, then add *cross-module* negative tests: reinterpretation alters goal but not past knowledge; a fight move cannot violate canon power; a scene-pledge payoff affects ending; a new source edition stales derived editorial findings.
8. Run existing upstream v4, v5, v6, v7 tests, including negative controls, against a pinned branch. Obtain independent receipts for all shipped wave claims. Do not call planned domains released.
9. Preserve every original author decision, old graph root, source version and explicit approval. Simulate impact before acceptance. Use branch+PR, not direct `main` edits, for adoption.

## Collision rules

Literal ZIP entry paths include different top-level folders; canonical installation paths are independently namespaced. The actual upstream files listed in docs are **ownership targets, not files silently replacing those targets**. No automatic semantic resolution of overlapping domain claims is permitted. The merge plan is a proposal; no merge took place in this session.

## Stop conditions

Block adoption on ambiguous canon owner, broken dependency closure, missing source rights, incompatible schema ID, undisclosed human decision, failing legacy regression, reader-review fabrication, or any wave claiming `shipped` without receipt. Do not lower tests or relax constraints to force a green result.
