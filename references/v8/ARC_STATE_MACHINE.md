# Event- and Knowledge-Time Character Arc State

**Status:** local projection validator / as-of / impact / diff executable; upstream canonical state transitions specified only.

## Canonical ownership

This module is a *view* over the existing graph: `canon.character`, `canon.event`, `structure.scene`, `canon.plant`, `canon.payoff`, `authorship.decision`, `verification.*` and `extension.derivation`. A new `narrative.*` node family cannot be committed directly through the observed v6 schema because `schemas/v6/semantic_node.schema.json` has a **closed enum**. A domain pack must first be admitted by v6-compatible extension semantics or by an explicitly authorized, versioned migration. Do not invent silent writes to the object store.

## Revision semantics

Each interpreted assertion carries `id` (version-specific), `logical_id` (stable identity), `revision`, `kind`, `character_ref`, `valid_from`/`valid_until` (half-open *world event* interval), `known_at` (knowledge clock), `supersedes`, `derived_from`, `evidence_refs` and `provenance`.

- `valid_from` and `valid_until` reference declared canon events whose `order` establishes a **fixture-local** strict sequence; event times are not guessed timestamps.
- `known_at` is timezone-aware ISO time. Future known revisions cannot leak into earlier as-of queries.
- A new revision must identify the earlier revision and preserve `logical_id`, `kind` and `character_ref`.
- After an event, prior valid states must still be answerable at an earlier event; after a new knowledge timestamp, prior *belief of the workspace* must still be answerable at an earlier `known_at`.
- Event-causal cycles, an impossible interval, or a revision leap are typed defects, not literary choices.

Algorithm sketch:

```text
for each logical_id:
    eligible := revisions whose world-event interval contains queried event
                and whose known_at <= queried knowledge time
    chosen := newest eligible known_at, then highest revision
    project(chosen) # read-only; never mutate graph
```

This does **not** yet resolve full bitemporal retroactive retcons or concurrent branch merges. Those require canonical `wi.py` as-of/merge and v6 proof obligations. `order` supports only a fully ordered export or test fixture; partially ordered story calendars must be resolved or represented as an incomparability/hold in a future adapter. Never invent an order for simultaneous events.

## Turning points and agency

`arc_turn` records a claimed change with world-event evidence. `choice` records what was actually done and by whom; changes justified by dialogue alone should be flagged for human review. A “ghost” is optional: not every lie or defense is trauma-caused. `flat` arcs can preserve conviction while changing relationships and institutions.

## Dependency contract

`derived_from` and `evidence_refs` are references to other nodes in the *same export*. `impact()` walks their downstream dependency frontier, labeling the result `downstream_may_be_stale`; it does not issue canonical invalidations. If the causal bridge to an ending is absent from the export, the tool cannot invent it. After any upstream change, run the upstream v6 `wi impact`, `wi simulate`, obligations and authority review before rewriting canon.

## Original fixture walkthrough

Ada first wants a public award, later replaces the central goal after witnessing an incident, and finally asks a rival for help. At the opening world event, `as-of` reports her original pursuit; at the later event with the later knowledge clock, it reports the revised pursuit; a final-state diff preserves both declarations without claiming that those declarations make a compelling arc. No screenplay or proprietary novel text is used.
