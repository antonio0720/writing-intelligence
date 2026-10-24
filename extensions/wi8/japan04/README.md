# Writing Intelligence v8 — Japan Story OS (Independent ZIP #4)

**Product claim:** A locally executable, offline *projection and draft studio*, with reusable Japan-focused research/fiction contracts. **NOT** a fully shipped v8 feature, real-world culture verification, guardian authentication, source ingestion engine, manuscript generator, manga renderer, publishing integration, or canonical graph runtime. **GitHub is unchanged.**

**Repository target:** `antonio0720/writing-intelligence`; inspected `main` at `d4524f3caa5f75e005b23f94dcd1c71bb5002127`, 2026-10-24. Revalidate HEAD before applying. Source: 160 requirements JP-181..JP-340 and the author's 97-page Japan Story OS planning PDF. Complete cumulative register 001..340 included as read-only reference in `source/notes/` at the archive root.

## Purpose

Japan Story OS is the final fourth independent upgrade bundle. It must protect creative sovereignty, encourage accurate research without cultural essentialism, preserve folklore variants, and make experimental fiction genuinely joyful. It is not a parallel Writing Intelligence database. V5 `STORYWORLD_OS`, `AUTHORSHIP_GRAPH`, `SEMANTIC_IR` and v6 `AUTHORITY_MODEL` remain canonical upstream owners. The local projection is explicitly marked `authority=noncanonical_projection`; the private draft vault is **not** a replacement for the authoritative `.wi` graph. Integration to graph writes requires a future adapter, proposal simulation, authorized decision and upstream re-verification.

The difference between a cultural statement and a fictional act is fundamental: `external_fact` demands attributed, region/date/institution-scoped evidence; `fictional_canon` requires a named world and an author's adoption record; `interpretation` cannot be machine-certified as truth. Names, honorifics, school calendars, shrine practices, Ainu/Ryukyuan material, and living religious traditions require the right kind of sources before publication. Missing information stays missing.

## Package layout

All **installable code** is beneath `extensions/wi8/japan04/` (no core file replacements). `source/notes/` preserves uploaded research artifacts; see `references/SOURCE_PIN.json` for checksums. The 97-page source PDF is not copied because the compiled work has third-party excerpts/screenshots. Neither its absence nor this package establishes rights to publish its content.

- `src/japan_story_os/`: typed contracts, deterministic diagnostics, optional world mechanics, local author vault, context-aware language/time checks, research source cards, migration previews, studio permission planning, release preflight
- `cli/wi8_japan.py`: executable offline, no external calls; does not own canonical commands
- `schemas/`: 12 JSON Schema 2020-12 definitions
- `fixtures/`: original invented test data, source-untrusted negative case and provenance-labeled proposed seed cards
- `references/`: all 160 requirements, traceability CSV, PDF/source fingerprints, source page locator index
- `docs/`: governance, language, folklore, safety, merge instructions, gap matrix
- `plans/`: WI8-24..43 proposal (all **planned**) and acceptance obligations
- `tests/`: unittest positive/negative controls
- `receipts/`: locally generated evidence; check file hashes and commands independently

## Run now (Python 3.8+; stdlib only)

From package root `extensions/wi8/japan04`:

```bash
python3 cli/wi8_japan.py check fixtures/sample_project.json
python3 cli/wi8_japan.py preflight fixtures/sample_project.json  # exits 2: NOT AUTHORIZED
python3 cli/wi8_japan.py studio questions-only fixtures/draft.txt
python3 cli/wi8_japan.py untrusted-scan fixtures/untrusted_lore.txt
python3 cli/wi8_japan.py migration-preview fixtures/legacy_v1.json
python3 -m unittest discover -s tests -v
```

Local author vault (this creates a **local-only** directory; choose one on a private disk):

```bash
python3 cli/wi8_japan.py init /path/to/author-private-vault
python3 cli/wi8_japan.py draft-save /path/to/author-private-vault opening fixtures/draft.txt
python3 cli/wi8_japan.py draft-history /path/to/author-private-vault opening
```

Use the saved draft SHA when proposing a change, and only an **author-designated actor** can accept a proposal. That designation is a **local workflow convention, not secure identity authentication**; a real deployment needs an upstream identity provider, guardian release authorization, revocation, and server-enforced role boundaries. The module never calls a publishing service.

## Tested versus designed

**Executable now, locally:** structural model validation; source/fiction boundary checks; location/school/cultural-scope triage; variant coexistence; source citations/rights metadata; Japanese era labels for Gregorian dates since 1873; Unicode script and lossy macron-display helpers; original-byte draft snapshots and non-destructive proposals; simple resource-budget simulation; local legacy ID previews; no-publish preflight; medium opt-in descriptions. Tests measure those contracts only.

**Not implemented/verified:** Japanese cultural authenticity adjudication, full retrieval/RAG, Japanese morphological parsing or dialect correctness, live transit/festival lookup, generative SonGPT or translation model, real-world source qualification, qualified cultural/rights/native-speaker review, full document/manga/anime/audio rendering, complete multi-user identity enforcement, cloud storage, cross-device synchronization, rights clearance, upstream semantic graph commits, official v8 release, or real reader satisfaction.

## Releases cannot be forged

Generating a package file is not publication. Supplying true booleans to `preflight()` is not an authenticated guardian decision. A human reader may disagree with a code finding, and cultural recommendations must be challengeable. Any apparent cultural authority or author credit emitted from weak source evidence is a defect. No automatic publishing or source-upload action exists here.

## Work with three earlier ZIPs

The previous independent packages define rules 001–060, 061–120 and 121–180. This ZIP contributes JP-181..JP-340. The installable root is dedicated to `extensions/wi8/japan04`; see `docs/MERGE_PROTOCOL.md`. Never concatenate distinct JSON schemas into one truth store or replace v6's closed `NodeType` list without its governed extension/ABI migration. All upstream waves must be reviewed against the current repo when a future merge begins.
