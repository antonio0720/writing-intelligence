# Writing Intelligence v8 — Arc, Want/Need & Ending Intelligence

**Independent ZIP #2.** This package implements the arc/ending portion of the user-supplied **120-requirement** specification while preserving the 60 previous fiction/thriller requirements as *references* to the separately delivered ZIP #1. It is **not** a replacement for that ZIP, does **not** incorporate its source code, and does **not** edit GitHub.

**Observed canonical repository:** [`antonio0720/writing-intelligence`](https://github.com/antonio0720/writing-intelligence), branch `main`, at commit `d4524f3caa5f75e005b23f94dcd1c71bb5002127`. This HEAD was independently read from the connected GitHub connector on 2026-10-24. **Upstream release: NOT performed.**

## Precisely what executes

Standalone, offline, stdlib-only Python 3.8+ source: `scripts/wi-arc.py` and `scripts/arc_v8/engine.py`. Read-only against the input and repository. The executable mechanisms perform:

1. Validate a typed projection of authored narrative state: characters, world events, belief/want/need versions, provenance, dependency references, and ending-focused character states.
2. Preserve **two clocks**: world-event time (`valid_from` / `valid_until`) and when the workspace learned an assertion (`known_at`). Reject invalid intervals, missing causes, cross-character ending references, missing history parents, and causal cycles.
3. Derive **sweet / semi-sweet / bittersweet / bitter** only when want/need results and author-declared provenance support the binary classification. Partial, unknown, conflicting, open, or reviewer-inferred outcomes produce `not_classifiable` with explanations. No invented certainty.
4. Keep character-arc family independent from ending quadrant. Flat protagonists and unresolved plots are valid inputs, not automatic failures.
5. Produce read-only downstream impact frontiers, opening/closing state diffs, and reported interpretive signals (e.g., a claimed emotional change without a witnessed choice).
6. Run a mechanical gate, which **never** upgrades itself into editorial or publication certification. Publication requires independent evidence beyond this package and always returns `HOLD` here.

**What does not execute:** direct integration with `scripts/wi.py`, extraction from novel prose, creation or mutation of authoritative v6 semantic nodes, character psychological inference, independent human reader recruitment, publication/rights/typesetting certification, or the 60 mechanisms owned by the other ZIP. These are specified, not shipped. The catalog identifies 21 of 120 requirements as **partially executable**, not 120 completed features.

## Quick commands

```bash
cd wi8-arc-ending-standalone
bash tests/v8_arc/run.sh
python3 scripts/wi-arc.py rules --id N064
python3 scripts/wi-arc.py validate --input tests/v8_arc/fixtures/four_quadrants.json
python3 scripts/wi-arc.py evaluate --input tests/v8_arc/fixtures/four_quadrants.json
python3 scripts/wi-arc.py classify --want sacrificed --need fulfilled
python3 scripts/wi-arc.py as-of --input tests/v8_arc/fixtures/four_quadrants.json --event ev-2 --known-at 2026-10-24T13:00:00-05:00
python3 scripts/wi-arc.py diff --input tests/v8_arc/fixtures/four_quadrants.json --start ev-0 --end ev-4 --known-at 2026-10-24T13:00:00-05:00 --character ch-ada
python3 scripts/wi-arc.py impact --input tests/v8_arc/fixtures/four_quadrants.json --changed want-ada-v2
python3 scripts/wi-arc.py gate --input tests/v8_arc/fixtures/four_quadrants.json --stage publication
# EXPECTED exit code 3 = HOLD, not acceptance.
```

CLI exit codes: `0` = successful command or mechanical-only pass, `2` = invalid input/block, `3` = editorial/publication hold. Every 'success' is only a locally executed evaluator outcome. `--input` is bounded to 8 MiB. Output is JSON to stdout; input files are not overwritten.

## Read in this order

1. `SOURCE_SPECIFICATION.md` — original 120 numbered requirements with provenance caveats.
2. `references/v8/ARC_ENDING_CONSTITUTION.md` — proposed creative and governance invariants.
3. `references/v8/ENDING_ALGEBRA.md` — exact semantics and refusal cases.
4. `references/v8/ARC_STATE_MACHINE.md` — two-clock character state and causal links.
5. `docs/ADAPTER_CONTRACT.md` — where this fits the v6 graph, without a competing store.
6. `docs/MERGE_CONTRACT.md` — future two-ZIP reconciliation.
7. `rules/arc_120_requirements.json` — lossless numbered normative register with implementation states.
8. `plans/v8-arc.proposal.json` — 12 release waves, all `planned` at upstream release level.
9. `receipts/LOCAL_TEST_RECEIPT.json` — local measured tests, not an upstream v8 release receipt.

The separate package manifest can be checked with `python3 scripts/check_arc_package.py` after extraction.

## Important conceptual distinction

A want is a character's perceived external goal. A need is **an interpretation** of possible inner development, attributed to a human or source. Neither fiction writers nor models receive supernatural access to a person's psychological truth. A human can intend a bittersweet ending and readers can feel satisfied, horrified or confused; the two claims are not interchangeable.

This is a *projection evaluator* — a read-only experiment over records exported from the canonical graph. Test fixtures use a clearly declared `fixture` origin and a synthetic graph root. Do not present fixture identities as real canonical graph digests. See `docs/ADAPTER_CONTRACT.md` before allowing `canonical_export` input.

## Ownership and rights

Owner-supplied concept notes inspired the design. They discuss K. M. Weiland and several copyrighted films as *interpretive examples*. These are acknowledged in `provenance/ATTRIBUTION.json`; no screenplay dialogue or protected passages were copied into code or fixtures. For distribution with the MIT repository, counsel or the owner should validate which newly authored files to license and the original notes' permitted scope. The bundle does not relabel third-party craft concepts as proprietary discoveries.

## v9 preview: relation to arc and ending work

*Preview (PR #8); proposed, not a release. v8.0.0 is the published version.*

Arc, want/need and ending intelligence are unchanged by v9; `scripts/wi-arc.py` and its gates are untouched. Two points carry over. A want or need is still an authored interpretation attributed to a person, and v9's rule that no assistance invents an author's memory (WI9-E) applies when the work is memoir: do not supply a "need" or a remembered turning point the author did not state. And an arc audit says nothing about who wrote the book; origin is a declaration checked by `scripts/wi-authorship.py`.
