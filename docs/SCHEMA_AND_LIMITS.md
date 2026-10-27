# Data Model: Noncanonical Normalized Projections

## Provenance-bearing records

`wi.arc.projection/v1` contains only: source identity, scope, characters, events, and semantic assertions. Events carry a *fixture/adapter-supplied* total world order and scene identifiers. The assertions may represent a `want`, `need`, `belief`, `ghost`, `arc_turn`, `choice`, `impact`, `relationship`, `cost` or `ending`, with stable identity and a version-specific record ID.

Validation requires a character owner and explicit epistemic attribution. `evidence_refs` refer to local witnessed events/assertions. `derived_from` defines local causal dependencies for the impact walk. The `source.graph_root` is supplied, not verified, and exists only as provenance metadata until an independent canonical readback compares it. `source.origin=fixture` is not production data.

## Why no scalar “best ending” score

This system does not use a single weighted sum of `want`, `need`, `arc`, `reader happiness` and `technical quality`. Such a number hides conflicts in objectives and claims of authority. Output separates: typed integrity, arc-family declaration, binary-classification eligibility, source witnesses, editorial questions, independent reader observations and publication holds.

## Limits

- A total event ordering is expected; partly ordered/circular storyworld calendars are rejected or held for adapter resolution.
- `known_at` is a single timestamp per assertion; this minimal sidecar does **not** implement the canonical v6 full valid/known interval logic, branch conflicts, or retroactive revocations. Preserve those through the canonical core.
- A revision supplied to the projection may be wrong or dishonest. The tool checks local consistency but cannot authenticate actual author approval.
- `evidence_refs` prove *references exist* within this projection, not that readers observed the listed event, nor that the event causes a lasting change.
- `impact()` walks local references, not upstream graph reverse dependencies. It names things **may be stale**, never “reverified unaffected.”
- No tool can treat a human's claimed internal need as an experimentally measured physical fact. Source and reviewer provenance must remain visible.
- `gate` always holds editorial and publication, even with a passing schema, because evidence authenticity, print output, copyrights, independent reader sample and institutional acceptance are not observed.
- Input bounded to 8 MiB to limit expensive local processing; large-scale manuscript ingestion belongs in a separately reviewed streaming adapter.

## Contract evolution

Backward-compatible additions require a new `schema` version whenever semantics change, even if field names remain the same. On admission to main, native v6 canonical representations must own identity, time, authority and hashes; this sidecar must be safely discardable and reproducible from that source.

---

## v9 preview: the authorship dossier and its limits

Everything below belongs to the v9 preview (PR #8), not to the v8.0.0 release, and is checked by `scripts/wi-authorship.py`.

**Schema.** [`../schemas/v9/authorship-dossier.schema.json`](../schemas/v9/authorship-dossier.schema.json) — current version `wi9-authorship-2`; `wi9-authorship-1` dossiers are still read. It describes the draft and its pinned `expected_sha256`, evidence spans (unique ids, exact excerpt, optional `start`, pinned source digest, typed `experience_state`, reviewer-recorded `support_status`), the contribution log, the declared origin, the venue contract and, for `release`, the person's `review_decision` and authority grant. `tests/v9/test_schema_parity.py` keeps the schema and the checker on one vocabulary.

**Limits the checker enforces.**

| Limit | Value |
|---|---|
| Draft or source file | 5 MB; size is taken from the open descriptor and at most limit + 1 bytes are read |
| Dossier file | 2 MB |
| JSON nesting depth | 32 |
| List and object sizes | bounded |
| Paths | relative to the dossier directory; absolute paths, `..`, NUL bytes and symlinked files, directories or dossiers are refused |
| Platform | POSIX only — component-by-component `os.open` with `dir_fd` and `O_NOFOLLOW`; where those do not exist the tool fails closed instead of reading less safely |

**Phrase scanner limits** (`prototypes/wi9/wi9_hotphrases.py`, the 334-rule reference catalog): at most 500,000 characters of input and 500 reported hits per run. When either bound is reached the report sets a `truncated` flag; a truncated report is a partial list, not a clean bill. Quotes, URLs, code spans and fences are masked unless `--include-quotes`; the masking is heuristic.

**What the dossier cannot establish.** Authorship is self-declared and every report says `declaration_status: self_reported`. An exact excerpt is a text anchor, not truth or entailment. Claim discovery depends on the v4 classifier, so a sentence it calls rhetoric is not checked. Python `re` has no timeout, so only reviewed local rule packs are accepted. See the open list in [`../references/v9/defects.md`](../references/v9/defects.md).
