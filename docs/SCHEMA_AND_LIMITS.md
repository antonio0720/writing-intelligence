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
