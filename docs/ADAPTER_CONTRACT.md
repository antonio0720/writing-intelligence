# Canonical Graph Adapter Contract — Strict Read-Only Boundary

## Current technical fact

The observed `schemas/v6/semantic_node.schema.json` defines a **closed `NodeType` enum**. It contains `canon.character`, `canon.event`, `structure.scene`, and `extension.derivation`, but not `narrative.want`, `narrative.need`, `narrative.ending`. The v5 Storyworld OS documents a rich character state machine largely as **specified**, not executable. A separate JSON file containing narrative records would *not* become an authoritative character database just because it looks like graph state.

## Layering

```text
V6 Canonical meaning graph (authoritative)
       | transactional, versioned, authority-checked
       |
       +-- approved read-only export adapter (NOT IMPLEMENTED)
                      |
                      v
             wi.arc.projection/v1
                      |
          +-----------+-----------+
          |           |           |
        validate    as-of       impact/diff
          |           |           |
          +-----------+-----------+
                      v
          classified views + review findings
             (no state write capability)
                      |
                      v
    upstream wi propose / simulate / decide / commit
      only if owner authorizes actual changes
```

## How a real adapter must work

1. Pin **the exact upstream graph root, branch, commit, policy digest, and schema version**, and separately read back that the root exists. Do not just trust a user-provided `graph_root` string.
2. Resolve existing canon identities, parent scene and event identities, source spans, and event predecessors. Translate to this package's local read-only `characters` / `events` / `assertions` projection format. An export must never grant authorization to itself.
3. Map `narrative.want`, `narrative.need`, `narrative.belief`, `narrative.ghost`, `narrative.arc_turn`, `narrative.ending` to **compatible extension derivations**, until a v6-approved schema migration makes dedicated types admissible. Do not add a free-form unknown node type to the closed enum.
4. Declare `origin: canonical_export` and `readback_ref`; compare the exported graph_root against the independently read canonical root. This evaluator only requires that the readback is declared — the upstream integration must prove it. A forged readback field cannot be proof.
5. Preserve `realm=fictional_canon` and never coerce storyworld claims into the `external_fact` realm. An author-asserted inner need is an authored interpretation, not an externally verified psychological diagnosis.
6. Export **event-time order** only when supported by canon. Where story events are concurrent, partially ordered or deliberately uncertain, return HOLD/UNKNOWN instead of allocating arbitrary `order` numbers.
7. Check exact revision ancestry, source-state digest binding, decision authority and provenance before publishing an author-approved extension back to core. The standalone evaluator implements none of those writes.
8. Derive a read-only results artifact with its own digest (`sha256( 'wi8-arc-projection-v1\0' || compact_sorted_json )`). This digest is **not** v6 `state_digest` and may never be used as one.
9. If any source changes, discard/refresh derived views and run the canonical `wi impact` + obligations + decision machinery. The local `impact()` returns a *hint*, not canonical staleness clearance.

## Error and trust model

| Condition | Behavior |
|---|---|
| missing core root | refuse promotion, allow only `fixture`-labeled testing |
| unknown new node type | quarantine proposal; do not silently coerce as `meaning.claim_atom` |
| external-fact language inserted as world canon | human/realm review and core gate |
| concurrent retroactive edits | canonical merge, preserve typed conflict |
| unknown event order | no invented ordering; defer projection |
| missing source span | `unverified` / review; not proof of author intent |
| reader-report claims canon authority | reject promotion; maintain independent evidence channel |
| proposed author deviation | simulate, seek valid scoped grant, record decision and receipt |
| revoked or expired authority | core blocks; local evaluator cannot bypass |

## Explicit non-goals

The adapter is **not implemented** in this ZIP. The fixture input is not proof of a real main-branch graph. No network, telemetry, writer action, GitHub mutation, manuscript import, external model inference, or deployment is performed by `scripts/wi-arc.py`.

## v9 preview: an adapter never turns a verdict into a send

*Preview (PR #8); proposed, not a release. v8.0.0 is the published version.*

The adapter described above is a read-only export boundary, and v9 adds a second rule for any adapter, connector or integration that sits between Writing Intelligence and a venue, CMS, email system or submission portal.

- **`REVIEW` is not a send.** `scripts/wi-authorship.py audit` reports `REVIEW` when its limited checks passed, and every audit report carries `release_authorized: false`. An adapter must not read `REVIEW` as permission to transmit.
- **`RELEASE_ELIGIBLE` is not a send either.** `scripts/wi-authorship.py release` returns `RELEASE_ELIGIBLE` only when a person's decision is bound to the exact draft sha256, an unexpired grant held by that person covers `release` and the named venue, and the venue contract lists `submit` as open. The command transmits nothing. An adapter that transmits must have its own, separate, authorized step by a person, and must re-check the draft digest at that moment.
- **Honor `HOLD` (exit 3).** On `HOLD`, an adapter stops. It does not retry with a different dossier, strip a field or downgrade the venue class to get past it.
- **Carry the declaration status.** Every report states `declaration_status: self_reported`. An adapter must not rewrite it as verified, and must not turn it into an authentication claim about a writer.
- **A grant in a dossier is a declaration.** Until WI9-08 binds it to the v6 grant store, an adapter cannot treat a dossier's authority grant as the canonical grant.
- A detector score is never an adapter input, gate or output field (WI9-H).

The existing non-goals stand: the arc adapter is still not implemented, and nothing here makes a v9 verdict a canonical state change.
