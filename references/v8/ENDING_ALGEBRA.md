# Ending Algebra, Partiality and Valence

**Status:** classifier executable; quality tests specified and human-reviewed. This is the semantics of `classify()` in `scripts/arc_v8/engine.py`.

## Variables

For character `c` and an **explicitly selected terminal** central want `w` and interpreted need `n`, define:

- `W = 1` only for `attained`; `W = 0` for `thwarted`, `renounced` or `sacrificed` when the author closes that pursuit.
- `N = 1` only for `fulfilled`; `N = 0` for `unfulfilled` or `rejected` when the author says that need remains unmet/rejected.
- `W = ⊥` for `partial`, `unresolved`, `disputed`, `n_a`, missing or otherwise not terminal.
- `N = ⊥` for `partial`, `unresolved`, `disputed`, `n_a`, missing or otherwise not terminal.

The function `Q(W,N)` is defined **only** if `W,N ∈ {0,1}`, the ending is `closed`, and both the need and ending interpretations are `author_asserted`. All else yields `not_classifiable` with reasons; `⊥` is not false.

| W (want) | N (need) | Q, strictly as a classification view |
|---|---|---|
| 1 | 1 | sweet |
| 0 | 1 | semi_sweet |
| 1 | 0 | bittersweet |
| 0 | 0 | bitter |

Formally, **the model does not decide W or N**. A human's interpretation supplies them. This function is deterministic *conditional on those assertions*; its output must read `derived_from_author_asserted_interpretation`, never `verified_reader_satisfaction`.

## Why four endings are not four narratives

Arc trajectory `A∈{positive_change,flat,corruption,fall,disillusionment,open,custom}` is independent of Q. The author may record a sweet ending in a tragedy's local subplot, a bitter ending for an ethically consistent flat protagonist, or no terminal quadrant at all. Avoid globalizing a character's outcome to the entire book; an ensemble carries a vector `(Q(c1),Q(c2),...)`, each with its own evidence.

`Ending = (selected_focus_want, selected_focus_need, external_outcome, interpreted_need_outcome, closure, moral_cost, justice, author_intended_valence, reader_observed_valence)` — only the two middle binary outcomes feed Q. Reader valence is an independent observational study, not assigned by prose heuristics.

## Want replacement

A character can start wanting to win a medal and later want to protect a friend. The older want is historically recoverable, not silently reinterpreted as the later need. The ending's `want_ref` must name the focus that the author means to classify; a mere latest timestamp does **not** authorize selecting a replacement without disclosure.

## Interpretation provenance

- `author_asserted`: a declared reading of the invented character.
- `reviewer_inferred`: an editorial interpretation, which can conflict with the author without changing canon.
- `reader_reported`: what an independent reader reports experiencing; this is observational, not authoritative character intent.
- `consistent_with_canon`: a machine's limited structural conclusion; not an assertion of the person's mental truth.
- `unverified`: a proposition lacking adequate attribution or evidence.

## Falsifying controls

1. `want=partial, need=fulfilled, closure=closed` => **not_classifiable**, not semi-sweet.
2. `want=attained, need=fulfilled, closure=open` => **not_classifiable**.
3. `need basis=reviewer_inferred` => **not_classifiable** even if fields would algebraically map.
4. `want=attained, need=unfulfilled` => bittersweet, *not* moral judgment on the reader.
5. `arc_family=flat, ending=sweet` => valid; no forced personal change.
6. `two protagonists with opposed goals` => two independent ending projections; no synthesized “book succeeded” scalar.
