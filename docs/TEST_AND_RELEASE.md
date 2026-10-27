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

---

## v9 preview lanes (not a release)

v8.0.0 is published. v9 is a preview on PR #8 and is **PROPOSED, release on HOLD until WI9-09**. Its lanes are separate from the v8 arc suite above and never stand in for it.

| Lane | Command | What it covers |
|---|---|---|
| Authorship checker | `python3 -m unittest discover -s tests/v9 -p 'test_*.py'` | `audit` / `release` behavior, schema-to-checker vocabulary parity (`test_schema_parity.py`), and the meaning-led doctrine scan (`test_doctrine_meaning_led.py`) |
| Reference kernel | `python3 -m unittest discover -s prototypes/wi9/tests -p 'test_*.py'` | The 334-rule phrase scanner, the review ledger, the composition contract and the hardening cases |
| Existing floor | `bash tests/v7/test_wi7.sh` | Version strings in `scripts/wi.py`, `SKILL.md` and the manifests still agree; v9 must not move them |
| Links | `python3 scripts/check-links.py` | Every relative link resolves |
| Mutation step | the `A disabled guard must turn the suite red` step in `.github/workflows/wi9-proposal.yml` | Disables four guards in turn (claim-coverage hold, draft-digest compare, origin-versus-log, grant expiry); the suite must go red each time or CI fails |

The workflow runs on Python 3.8, 3.11 and 3.13 and checks that `references/v9/README.md` still says it is a proposal and sets no detector-score target.

**Receipts.** [`../plans/receipts/WI9-00.json`](../plans/receipts/WI9-00.json) records the baseline and defect audit (validated; owner approval pending). [`../plans/receipts/WI9-P0.json`](../plans/receipts/WI9-P0.json) records the P0 repairs. A receipt says what ran, not that a wave shipped.

**What v9.0.0 requires and does not yet have.** A `9.0.0` tag needs WI9-09 (independent review and rollout) and the owner's approval. Neither has happened. The 60-case editorial benchmark (WI9-07), a consented author corpus and an external review have not run, so no document may report v9 quality results.
