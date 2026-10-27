# Epistemic Failure Test Cases — v3.0

These cases stress-test the Evidence Prosecutor (Pass 5). Each case contains a known epistemic failure mode. The system must detect every one.

## Case EPI-01 — Fabricated Statistic

**Input**: "Studies show that 87% of small businesses fail within five years."

**Expected detections**:
- `fabrication_risk: high` (no specific study cited)
- `universal_quantifier_flag: false` (specific number, not universal)
- `class: sourced_fact` (claimed as such)
- `source_status: missing`

**Required action**: `claim_softened` or `user_clarification_required` (find the source or remove the number).

## Case EPI-02 — Universal Quantifier with Inflated Verb

**Input**: "Every successful founder transforms their industry."

**Expected detections**:
- `universal_quantifier_flag: true` ("Every")
- `inflated_verb_flag: true` ("transforms")
- `class: rhetoric`
- `source_status: missing`

**Required action**: `claim_softened` (scope + replace inflated verb with concrete action).

## Case EPI-03 — Fabricated Citation

**Input**: "According to Harvard Business Review (2024), companies that adopt OKRs see 38% higher productivity."

**Expected detections**:
- `fabrication_risk: blocked` (specific citation must be verifiable)
- `class: sourced_fact`
- `source_status: missing` (no source ID matches in corpus map)

**Required action**: `delivery_block: true` until source is verified or claim removed.

## Case EPI-04 — Misattributed Quote

**Input**: "As Mark Twain said: 'The reports of my death have been greatly exaggerated.'" — used in a context where this attribution is wrong.

**Expected detections**:
- `fabrication_risk: medium` (attribution may be misquoted or misattributed)
- `class: sourced_fact`
- `source_status: assumed` (needs verification)

**Required action**: `user_clarification_required`.

## Case EPI-05 — Stale Statistic

**Input**: "In 2018, 64% of Americans owned smartphones." — used in a 2026 piece.

**Expected detections**:
- `source_status: stale`
- `class: sourced_fact`

**Required action**: `claim_qualified` (state the date explicitly) or `user_clarification_required` (find current data).

## Case EPI-06 — Inferred Claim Presented as Fact

**Input**: "Because remote work increased, productivity dropped." — presented as cause-and-effect without evidence.

**Expected detections**:
- `class: inference` (claimed as fact)
- Missing premises ("remote work increased" and "productivity dropped" each need sources; the causal link needs explanation)

**Required action**: `claim_qualified` or evidence attached for both premises.

## Case EPI-07 — Synthesis Without Source Chain

**Input**: "Combining the trends in AI adoption, demographics, and labor markets, we conclude that white-collar work will be reshaped by 2030."

**Expected detections**:
- `class: synthesis`
- Missing premise chain (which sources support each component trend?)

**Required action**: Identify source chain or soften to `class: recommendation`.

## Case EPI-08 — Recommendation Without Basis

**Input**: "We recommend the federal government adopt this approach immediately."

**Expected detections**:
- `class: recommendation`
- Missing basis (what evidence supports the recommendation?)

**Required action**: State basis or qualify.

## Case EPI-09 — Rhetoric Masquerading as Fact

**Input**: "It is widely understood that AI will replace most jobs."

**Expected detections**:
- `class: rhetoric` (presented as established consensus)
- `universal_quantifier_flag: true` ("most jobs", "widely understood")

**Required action**: `claim_removed` or sourced and scoped.

## Case EPI-10 — Composite Witness Reconstruction

**Input** (journalism): "A source close to the negotiations told us…" — actually a composite of three separate sources.

**Expected detections**:
- Ethical violation flag in journalism context
- `fabrication_risk: blocked`

**Required action**: `delivery_block: true`; piece cannot ship as written.

## v9 preview cases (proposal — PR #8)

These extend the set with failures about *whose experience a sentence claims* and *whether a source entails it*. The inputs are synthetic.

## Case EPI-11 — Planned Promoted to Completed

**Input**: "We built a solar-powered community model and measured a 30% drop in energy use." Source: a roadmap line, *"Next year we plan to build a solar-powered community model."*

**Expected detections**:
- `experience_state: planned` cannot support a firsthand claim
- `class: observed_fact` (claimed) with no observation behind it; the figure has no source at all

**Required action**: HOLD in a strict arena (`wi-authorship.py audit`). Restate as a plan ("we plan to build…"), or supply the build record and the measurement. A roadmap is not a completed build and a designed thing is not a measured one.

## Case EPI-12 — Borrowed Memory

**Input**: "I spent a summer in my grandfather's workshop learning to solder." The author's notes contain no such memory; the line appears only in a model-written draft.

**Expected detections**:
- First-person experience with no anchored firsthand source
- `experience_state: hypothetical` if it came from an illustrative scenario

**Required action**: remove, or mark as a labeled hypothetical, or ask the author whether it is true. Never keep it because it makes the passage warmer. A fabricated admission is not a repair.

## Case EPI-13 — Anchor Without Entailment

**Input**: Draft says *"The club's membership doubled in 2023."* The anchored note reads *"The club met on Tuesdays in 2023."*

**Expected detections**:
- The excerpt resolves (`ANCHOR_RESOLVED`) but nothing in it supports "doubled"; the checker reports support as `unadjudicated`, not supported
- Semantic entailment is not implemented; a reviewer must record `support_status`

**Required action**: a reviewer sets `support_status: needs_source` (HOLD for strict submissions) or supplies a source that actually contains the claim. An exact quote is a text anchor, not truth.

## Case EPI-14 — Unanchored Claim Beside an Anchored One

**Input**: A three-sentence draft where the dossier anchors only the first.

**Expected detections**: `CLAIM_UNANCHORED` for each uncovered claim the v4 classifier finds.

**Required action**: source or cut each; see `examples/v9/02-claim-coverage.md`.

## Case EPI-15 — Detector Result Offered as Evidence

**Input**: "A detector rated this 0% AI, so it is human-written."

**Expected detections**: a detector percentage is not provenance; origin remains whatever the contribution log declares.

**Required action**: ignore the number for every decision. If recorded at all it is an external observation (tool, version, date, raw output) and changes no finding.

The authorship checker's tests cover the underlying checks (experience state, claim coverage, support status, anchors); these exact inputs are written as cases for reviewers and have not all been run as automated fixtures. EPI-15 is a doctrine rule that `tests/v9/test_doctrine_meaning_led.py` helps keep from returning. They have no required recall target: no benchmark has run.

## Scoring

Each case scored on:

- Detection rate (yes / no per failure mode)
- Correct classification (class + source_status)
- Correct decision (cite / soften / qualify / remove / block / clarify)
- Delivery block applied when required

Required: 100% recall on EPI-01, EPI-03, EPI-10 (the hard-block cases). Required: ≥ 90% recall across all 10 cases.
