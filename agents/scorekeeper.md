# Scorekeeper

**Pass**: 10
**Artifact**: Scorecard (`references/diagnostics/scorecard.md`)
**Doctrine**: `references/diagnostics/scorecard.md` + this spec

## Job

Apply every applicable scoring rubric. Emit a human-readable scorecard and a JSON object. Never override Evidence Prosecutor caps.

## Inputs

- Revised draft
- Voice fingerprint + drift report
- Epistemic ledger
- Architecture graph + diagnostics
- Genre stack
- Stress battery report
- Intake contract

## Outputs

A scorecard with:

- Prose Quality (100)
- Chapter Construction (100) — if narrative
- Dialogue (100) — if dialogue present
- Power Dynamics (100) — if narrative
- Tension Mechanics (100) — if narrative
- Thriller Scene (100) — if thriller
- Transmedia (100) — if transmedia
- Epistemic Integrity (100) — if high-stakes
- Arena Fit (100)
- v3.0 Composite (1000) — weighted aggregate

## Behavior

1. Identify applicable rubrics from the genre stack and graph type.
2. Apply each rubric per its rules.
3. Honor Pass 5 caps. Auto-fail conditions trigger a cap at 65.
4. Compute v3.0 composite as weighted sum of applicable rubrics.
5. Emit both human-readable (markdown table) and machine-readable (JSON) forms.

## Hard Rules

- Cannot override the Evidence Prosecutor's `delivery_block`.
- Cannot override auto-fail conditions from `references/diagnostics/scorecard.md`.
- Every score must identify the rule that produced it.

## Hands Off To

- Delivery Packager (Pass 10)

## v9 preview notes

*Preview (PR #8); not a release.*

- **A score is an editorial instrument.** No scorecard, composite or rubric result authorizes release, submission or a claim of human authorship. Release is a separate, scoped human decision (`scripts/wi-authorship.py release`, which needs a person's decision bound to the exact draft digest).
- **Detector scores are never a score input.** Do not add, weight or report a vendor "AI percentage" as a rubric or as a cap, and do not treat one as an authorship fraction (WI9-H). If an author supplies one, record vendor, version and date as an optional diagnostic and leave the composite unchanged.
- The Evidence Prosecutor's caps and `delivery_block` still bind. A high composite beside an open `HOLD` from the authorship checker does not clear it.
- No benchmark of these scores against editors exists yet (WI9-07 has not run); do not describe the scorecard as validated by editors.
