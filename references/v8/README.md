# references/v8 — Story Intelligence

v8 is the fiction half of Writing Intelligence brought up to the evidence standard v4–v7 built. It was delivered as four independent packages, each built and tested on its own, and folded into this repository additively — no v4–v7 file changed behaviour, and nothing from the four packages was dropped.

**The v8 rule:** *a structural pass is not a good novel.* Mechanical consistency, interpretive signal, human editorial judgment and independent reader reception are four states, and no engine promotes one into another. Every publication gate returns HOLD (exit 3) by design.

## The four parts

| Part | Requirements | Engine | Constitution | Package docs |
|---|---|---|---|---|
| 1 · Fiction & Thriller Intelligence | FI-01–FI-60 (B001–B060) | `scripts/wi-fiction.py` | [`FICTION_INTELLIGENCE_CONSTITUTION.md`](FICTION_INTELLIGENCE_CONSTITUTION.md) | `docs/FICTION_V8_*.md`, `UPGRADE_README.md` |
| 2 · Arc, Want/Need & Ending Intelligence | N061–N120 | `scripts/wi-arc.py` | [`ARC_ENDING_CONSTITUTION.md`](ARC_ENDING_CONSTITUTION.md) | `docs/v8/ARC_ENDING_README.md`, `docs/ADAPTER_CONTRACT.md`, `docs/MERGE_CONTRACT.md`, `docs/OWNER_CROSSWALK.md`, `docs/SCHEMA_AND_LIMITS.md`, `docs/TEST_AND_RELEASE.md` |
| 3 · The Craft | C121–C180 | `extensions/wi8/craft03/scripts/wi-craft.py` | `extensions/wi8/craft03/references/v8/CRAFT03_CONSTITUTION.md` | `extensions/wi8/craft03/README.md`, `extensions/wi8/craft03/docs/` |
| 4 · Japan Story OS | JP-181–JP-340 | `extensions/wi8/japan04/cli/wi8_japan.py` | `extensions/wi8/japan04/docs/ARCHITECTURE.md` | `JAPAN04_README.md`, `extensions/wi8/japan04/README.md`, `extensions/wi8/japan04/docs/` |

340 numbered requirements in total. The cumulative register is `source/notes/Writing_Intelligence_v8_Complete_Requirements_001-340.md`.

## Read in this order

1. [`FICTION_INTELLIGENCE_CONSTITUTION.md`](FICTION_INTELLIGENCE_CONSTITUTION.md) — creative invariants and the exception doctrine
2. [`ARC_ENDING_CONSTITUTION.md`](ARC_ENDING_CONSTITUTION.md) — the arc and ending invariants
3. [`ENDING_ALGEBRA.md`](ENDING_ALGEBRA.md) — sweet / semi-sweet / bittersweet / bitter, and every refusal case
4. [`ARC_STATE_MACHINE.md`](ARC_STATE_MACHINE.md) — two clocks: when it held in the story, when the workspace learned it
5. [`EDITORIAL_JUDGMENT.md`](EDITORIAL_JUDGMENT.md) — where code stops and an editor starts
6. [`RULE_CROSSWALK.md`](RULE_CROSSWALK.md) — the 60 fiction rules mapped to owners and test vectors
7. `extensions/wi8/craft03/references/v8/` — openings, action causality, opposition, suspense, sequence vectors
8. `extensions/wi8/japan04/docs/` — cultural evidence protocol, folklore and world design, language and chronology, young-author sovereignty

Compiler and genre material added by v8 lives with the craft library: `references/compiler/novel_architecture.md`, `fiction_rule_integrity.md`, `reader_experience.md`, `arc_ending_projection.md`; `references/genre_packs/fiction_v8_addendum.md`, `fiction_arc_v8_addendum.md`; `references/diagnostics/fiction_quality_separation.md`.

## Status

The one status source is [`plans/v8.manifest.yaml`](../../plans/v8.manifest.yaml). 8.0.0 ships the four engines as standalone offline tools (WI8-R0–WI8-R2, with receipts). Canonical integration into `wi.py` and the v6 semantic graph, manuscript extraction, reader trials and cultural review are waves FI8-03–FI8-06 and WI8-00–WI8-43, all **planned**. The per-package proposals remain beside it: `plans/v8-fiction.proposal.json`, `plans/v8-arc.proposal.json`, `extensions/wi8/craft03/plans/v8-craft03.proposal.json`, `extensions/wi8/japan04/plans/japan04_waves.json`.

## Package integrity files

Each package's checksum file is kept at the path its own verifier expects: `SHA256SUMS.txt` (part 1, at the repository root), `ARC_SHA256SUMS.txt` (part 2 — two of its entries, `README.md` and `SOURCE_SPECIFICATION.md`, live at `docs/v8/ARC_ENDING_README.md` and `docs/v8/ARC_SOURCE_SPECIFICATION.md` because the root names were already taken), `extensions/wi8/craft03/CRAFT03_SHA256SUMS.txt` (part 3) and `JAPAN04_SHA256SUMS.txt` (part 4). `scripts/check_arc_package.py` verifies the arc package as it was extracted, not this merged tree.

**Eight schemas were annotated after the merge.** This repository requires every schema to carry `$schema`, `$id`, `title` and `description`, and eight delivered v8 schemas lacked one or more: `arc_reader_review`, `arc_report`, `arc_rule_catalog`, `fiction_findings`, `fiction_gate`, `fiction_ir`, `fiction_reader_study`, `fiction_rule_catalog`. The missing annotations were added — annotations only, no validation keyword changed — so their bytes no longer match the lines for them in `SHA256SUMS.txt` and `ARC_SHA256SUMS.txt`. Those files are kept as the record of what was delivered; the delivered bytes are in git history at commit `551fdfe`.

## Verify

```bash
bash scripts/test-v8.sh
```

All four suites, the positive controls, the refusals (exit 2), the publication holds (exit 3), and the 340-requirement count.
