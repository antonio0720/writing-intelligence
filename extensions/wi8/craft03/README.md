# Writing Intelligence v8 — *The Craft*, Independent Package #3

This archive implements a **standalone, offline, read-only diagnostic slice** of the newly proposed `C121–C180` requirements: opening strategy, action geometry, antagonistic causality, suspense contracts, mixed sequence outcomes, dated reference hygiene, and cross-medium equivalence signals. It neither replaces ZIP #1's B001–B060 nor ZIP #2's N061–N120. There is no new canonical story database. **No changes to GitHub were made.**

## Canonical baseline

Repository: `antonio0720/writing-intelligence`, `main`, `d4524f3caa5f75e005b23f94dcd1c71bb5002127` (read using linked GitHub connection on 2026-10-24). The v6 `SemanticNodeV6.NodeType` is a closed enum; `narrative.*` types must not be written to its authoritative store absent migration and explicit acceptance. Existing canonical owners are named in `docs/CANONICAL_INTEGRATION.md`.

## Executable boundary

`./scripts/wi-craft.py` uses Python 3.8+ and the standard library only. It reads one JSON file, never writes it, derives deterministic structural findings, and returns the observed inputs' digest. Synthetic examples declare `origin: fixture`. User annotations may declare `origin: draft_projection`; that **does not make them canonical**. `origin: canonical_export` is deliberately refused until a real, reviewed, independently tested v6 adapter exists.

It computes **mechanical consistency** (typed references, event/goal cycles, fight movement and resources), **causal-integrity signals** (unsupported clues, planner omniscience, unmatched promises, nonexistent payoff), and **editorial review prompts**. It does not read a manuscript to infer the characters' inner motives or certify the quality of a twist. The 60 requirements are modeled; only a defensible subset has executable validation signals. Each partially executable requirement is still only *partially* implemented. All twelve upstream adoption waves remain `planned`.

## Quick start

```bash
cd wi8-craft-03-standalone
bash tests/v8_craft/run.sh
python3 scripts/wi-craft.py rules --id C174
python3 scripts/wi-craft.py evaluate --input tests/v8_craft/fixtures/valid_quiet_mixed_victory.json
python3 scripts/wi-craft.py as-of --input tests/v8_craft/fixtures/valid_quiet_mixed_victory.json --known-at 2026-10-23T20:00:00Z
python3 scripts/wi-craft.py gate --input tests/v8_craft/fixtures/valid_quiet_mixed_victory.json --stage publication
# Exit 3 (HOLD) is intentional. A structural PASS is not publication approval.
python3 scripts/install_craft03_additive.py --target /path/to/writing-intelligence
# Defaults to dry run. No files are written unless --apply is specified.
```

Exit status: `0` successful analysis or mechanical-only pass; `2` malformed data / structural block; `3` editorial or publication gate held. Output is deterministic JSON. Maximum accepted CLI input: 8 MiB. No accounts, telemetry, network calls, or external model dependencies.

## Reading map

| Read | Purpose |
|---|---|
| `SOURCE_SPECIFICATION.md` | User-provided source specification verbatim |
| `rules/craft_c121_c180.json` | Stable numbered and sourced requirement registry |
| `references/v8/CRAFT03_CONSTITUTION.md` | Distinguishes mechanical proof, interpretation and reader reception |
| `docs/DOMAIN_CONTRACTS.md` | Field-level operational semantics for all six domains |
| `docs/CANONICAL_INTEGRATION.md` | Exact v5–v7 ownership and safe adoption policy |
| `docs/THREE_ZIP_MERGE.md` | Collision-free staging and semantic reconciliation plan |
| `docs/ADVERSARIAL_VERIFICATION.md` | Falsification matrix, test types and release holds |
| `schemas/v8/*.schema.json` | Eight draft-2020-12 draft-projection/report schemas |
| `plans/v8-craft03.proposal.json` | WI8-12–WI8-23 upstream waves, all planned |
| `receipts/LOCAL_CRAFT03_TESTS.json` | Local measured checks, not official upstream release |

## Source boundary

The current attachment is the **187-line summary specification** referencing *The Craft(3).pdf*, not the 51-page PDF itself. Page citations and provenance assertions are preserved as submitted, not independently validated against that PDF. The ZIP includes original test fiction, not copyrighted film scripts or third-party screenshots. Attribution and publication-rights clearance remain required before any official upstream release.
