# Later Two-ZIP Merge Contract — Keep Them Separate Until Authorized

The owner explicitly requested **two separate ZIPs** for a later combined v8. This archive, WI8-ARC, represents notes-driven `N061–N120`; the preceding FICTION package owns the implementation of the carried-forward `B001–B060`. This ZIP includes all 120 textual requirements in its source-specification and JSON register for traceability **but does not vendor or redefine the previous module's runtime**.

## Path collision policy

| This ZIP | Earlier ZIP | Merge disposition |
|---|---|---|
| `scripts/wi-arc.py` + `scripts/arc_v8/` | `scripts/wi-fiction.py` + `scripts/fiction_v8/` | distinct, keep both, then canonical integration |
| `schemas/v8/arc_*.schema.json` | `schemas/v8/fiction_*.schema.json` | distinct types, later common graph contract |
| `references/v8/ARC_*.md` | `references/v8/FICTION_INTELLIGENCE_CONSTITUTION.md` | one eventual v8 constitutional document, review before combining |
| `tests/v8_arc/` | `tests/v8/` | distinct suites, run both |
| `rules/arc_120_requirements.json` | `rules/fiction_v8_rules.json` | keep full register; dedupe B rule IDs via one owner |
| `plans/v8-arc.proposal.json` | `plans/v8-fiction.proposal.json` | both proposed; merge into one authoritative v8 release manifest after review |
| `SOURCE_SPECIFICATION.md` | `provenance/USER_REQUIREMENTS.txt` | independent originals; preserve source and history |

## Reconciliation algorithm

1. Extract both archives in **different** directories. Check SHA256SUMS of each. Never unzip one on top of the other or delete a conflicting file by default.
2. Re-read live GitHub HEAD and compare with pinned `d4524f3caa5f75e005b23f94dcd1c71bb5002127`. A changed HEAD triggers rebase/architecture review, not a force application.
3. Compute path collisions and content digests. Existing repo owners win until an authorized file-level migration is accepted. Keep prior `B001–B060` mechanics as the canonical owner of these rules; merge new N rules as additive projections.
4. Verify that both products share one semantic source graph, one authority/decision engine and one release proof system. No independent truth cache can silently become canonical.
5. Classify each B/N requirement: `specified`, `local_test_pass`, `upstream_integration_test_pass`, `human_review_complete`, `reader_validated`, `shipped`. A B/N rule cannot be marked `shipped` because either ZIP merely contains it.
6. For each migration, run source tests, negative controls, existing `tests/v4`, `tests/v5`, `tests/v6`, `tests/v7`, prior package tests, new arc tests, impact/authority and release-verification checks. Mutation-style refusal tests must prove that a disabled gate blocks unsafe actions.
7. Merge doctrinal text by an explicit owner decision; fixed eight-phase tension diagrams remain craft templates rather than universal acceptance criteria. No new v8 constitution may silently weaken v6 law A–R.
8. Rebuild the official `.skill` payloads and verify actual file ceilings/character constraints, manifest receipts, branch CI and independent clean extraction. Do **not** copy `.skill` bundle files into this ZIP and assume they are installed.

## Collision-fail installer

Run `python3 scripts/install_arc_additive.py --target /path/to/writing-intelligence` to preview *only* the add-only paths. `--apply` writes only paths that do not already exist and refuses any collision. It does **not** edit existing core files, create branches, commit or push. Using it with a repo already containing conflicting v8 files is expected to fail until reviewed.

## Canonical integration work still missing

- Formal admission of dedicated narrative schema extensions or versioned native node types.
- A real core readback adapter and source-linked canonical projections.
- Owner-authorized rewrite proposals and v6 contract-driven migrations.
- An integrated compiler pass, public API and UI surface.
- A unified B/N quality diagnostic and reader study.
- Production and release acceptance with receipts.

## v9 preview: contribution logs and authorship declarations across a merge

*Preview (PR #8); proposed, not a release. v8.0.0 is the published version.* The two-ZIP reconciliation above concerns the v8 packages. v9 adds a smaller rule about what a merge of work containing authorship dossiers may and may not do.

- **A merge never reconciles declarations by averaging or choosing.** If two branches declare different `origin` values, different contribution logs, or different venue contracts for the same draft, that is a conflict between declarations. Preserve both and stop for a person, as the v6 merge protocol does for meaning (`examples/v6/02-the-merge-that-refused.md`). Do not write a blended `origin`.
- **Contribution logs are append-only history.** Merge them as a union of entries with their kinds intact (`human_original`, `human_edit`, `ai_research`, `ai_generated_prose`, `ai_substantive_rewrite`, `mechanical_proofread`). Dropping an AI entry to satisfy a `human_only` venue is a falsified record, not a merge.
- **A merge invalidates earlier digests.** A review decision is bound to the exact draft sha256. If the merged draft differs, the earlier decision and any `RELEASE_ELIGIBLE` result no longer apply; re-run `audit` and `release` on the merged draft.
- **Release grants do not merge into authority.** A grant in one dossier does not extend to the other branch's draft or venue.
- Re-run the checker and keep every output labeled `declaration_status: self_reported`. A merge cannot authenticate a writer.
