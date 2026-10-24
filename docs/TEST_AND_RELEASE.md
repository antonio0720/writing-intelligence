# Verification Contract and Release Refusal

## Locally executable verification

- `bash tests/v8_arc/run.sh` runs deterministic unittest cases, CLI positive tests, negative-control refusal and release-hold control.
- `python3 scripts/wi-arc.py validate --input ...` exercises local typed constraints.
- `schemas/v8/*.schema.json` are Draft 2020-12 JSON Schemas. `jsonschema` can validate the schema themselves **if independently installed**; it is not required to execute this package.
- `ARC_SHA256SUMS.txt` manifests the archive's files; verify from an extracted directory with `sha256sum -c ARC_SHA256SUMS.txt` (or `shasum -a 256 -c ARC_SHA256SUMS.txt` on macOS).

## Negative controls and expected behavior

| Control | Result |
|---|---|
| Unknown evidence reference | `ARC_REF_DANGLING`, CLI exit 2 |
| Ending focus belongs to other character | `ARC_FOCUS_WRONG_OWNER`, exit 2 |
| An event causes an earlier event in a cycle | `ARC_CAUSAL_CYCLE`, exit 2 |
| Version number leaps over a revision | `ARC_REVISION_GAP`, exit 2 |
| Changed goal at an earlier knowledge timestamp | later goal absent from `as-of` |
| Partial, disputed, not-applicable need/want | `not_classifiable` |
| Reader inference treated as author's need truth | `not_classifiable` |
| Flat protagonist unchanged | permitted; no mandated transformative failure |
| Multiple protagonists with divergent outcomes | four independent projections; no book-wide fiction scalar |
| Claimed final change with no behavior | `ARC_CLAIMED_CHANGE_NO_CHOICE` review signal |
| Local schema check passed then publication requested | `HOLD`, CLI exit 3 |
| Reader form supplied without reliable independence/readback | still `HOLD` |
| “canonical_export” without a readback pointer | `ARC_READBACK_MISSING`, exit 2 |

## What would falsify local claims?

A reproducible counterexample in which a dangling ref passes validation, the same input produces inconsistent classification, a partial ending acquires an invented quadrant, a future-known revision leaks into past knowledge queries, or an editorial/publication request returns mechanical PASS would falsify our local conformance claims. Add such cases as regression tests rather than weakening tests to fit outputs.

## What upstream proof is still required?

Run v4–v7 shell suites **inside the real repository checkout** against an authorized v8 integration branch. Pin actual root and decision states, run `wi simulate` to identify changed dependent claims, submit required owner decisions, verify merge conflict preservation, run release obligations and verify the resulting proof capsule from a second environment. Any output requiring genuine reader impact needs source-linked reader research. A generated JSON file is neither an independent readback nor a publishing outcome.

The supplied `plans/v8-arc.proposal.json` deliberately marks all upstream waves `planned`. Its local test receipt proves only what this extracted package executed. Never mark one of those waves `shipped` on the basis of local standalone checks.
