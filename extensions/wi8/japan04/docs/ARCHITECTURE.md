# Japan Story OS architecture: one owner, typed projections

## Canonical owners, not copies

| Concern | Existing owner | This package | Next integration obligation |
|---|---|---|---|
| Fictional facts, cast, timeline | v5 `STORYWORLD_OS` + `AUTHORSHIP_GRAPH` | `contracts.validate_project` accepts **explicitly untrusted projection** | Read export from canonical graph; enforce exact root and schema; reject forged graph identity |
| Source evidence | v4/v5 source and anchor layers | structured research metadata | Bind to exact source version and span; never claim a URL proves the content |
| Identity, dependency & conflict | v5/v6 | sample IDs/relations and diagnostics | Map to closed `NodeType`/graph-edge schema via versioned adapter and `wi simulate` |
| Decisions and authority | v6 | immutable *local* byte snapshots and a declared `author` role | Authenticate actor, grant and scope in core; decisions bind to exact state |
| Fiction craft passes | Fiction pack & Narrative Architect | optional culture/character projection | Feed findings as nonauthoritative diagnostics; not scores or rewrites |
| Release receipts | v7 receipt standard | reproducible local test report | rerun v4–v7 suites, constitutional gates, independent readback and receipt close |

**Never** claim the Python draft vault implements canonical `wi` authorization or ledger. Its SHA digest is domain-separated `WI8-JP04-PROJECTION-ONLY\0`, which is intentionally incompatible with canonical graph hashes. Canonical hashes, schemas, grants and commits can be produced **only** by the upstream runtime after authorized migration.

### Source / canon boundary

`external_fact`: a source-scoped assertion about the actual world. Its truth is not conferred by presence in a novel. `fictional_canon`: a rule adopted into a particular invented world under an author's own decision; doesn't become social or historical fact. `research_note`: a possibly contradictory observation. `interpretation`: critical or literary judgment. `simulation`: counterfactual no-write outcome. These realms are never silently cast to one another.

### Proposed semantic relations

`source_inspires`, `source_documents_variant`, `author_adopts`, `fiction_diverges`, `reviewed_by`, `renders_as` remain **proposed adapter relations**, not claims of existing upstream graph edge availability. The local collection of them is an experiment/projection. The core's closed node and relation vocabulary must be extended through versioned schema migration or, if valid and authorized, a core-recognized extension family. Merely putting `narrative.*` into a JSON file cannot change v6 constraint enforcement.

### Decision-time truth

Each authoritative source and author decision ultimately needs two clocks: when the claim was valid in-world and when the workspace accepted it. Later revelation may revise a working theory without rewriting what the author, characters, or reviewers knew at the time. The local draft vault stores revisions and byte digests; it is not yet a complete bitemporal implementation. Do not infer bitemporal completeness from revision history.

### Privacy/control plane

Private author drafts -> local vault -> proposed changes -> author review -> possible local adoption. Culture research -> untrusted source cards -> scoped claims -> human qualified review -> possible citation. Release candidate -> identity/guardian/license checks -> qualified review -> authorized publisher. This ZIP implements only the earliest portions. It provides **no network transport**, no publisher adapter and no account token flow.

### Required falsification of future integration

1. A story-only Ki-Thread power does **not** become a real religious practice.
2. A minority community's lore is not overwritten by a generic nationwide encyclopedia summary.
3. A forged assistant recommendation never silently commits into the user's story.
4. A fork-specific magic system cannot modify a separate realistic school drama.
5. A saved draft remains byte-identical across rejected suggestions.
6. A new manuscript build with outdated transit data remains explicit `NEEDS_CURRENT_SOURCE`, not 'verified'.
7. A guardian workflow cannot force a private creative rewrite; public distribution is independently controlled.
8. A reviewer saying 'beautiful' creates an attributed judgment, not a verified reader outcome.
