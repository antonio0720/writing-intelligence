# Exam Rubrics

Operator certification does not use traditional exams. Instead, applicants submit real-work portfolios audited against the rubrics in `operator_levels.md`. This document describes how the audit is conducted.

## The Audit Procedure

### Step 1 — Intake

The applicant submits:

- 3+ (Apprentice) or 5+ (Operator) real deliverables
- For each: the intake contract used, the final delivery bundle, the scorecard, and any pass artifacts (epistemic ledger, voice fingerprint, etc.)
- A cover note describing how each deliverable was produced

### Step 2 — Re-audit

The reviewer runs the 11-pass kernel against each deliverable in `audit` mode. This produces:

- An independent scorecard
- An independent epistemic ledger (for high-stakes deliverables)
- A voice fingerprint
- A stress battery

### Step 3 — Comparison

The reviewer compares:

- Applicant's claimed scores vs. audit scores. A pattern of inflated self-scoring is a flag.
- Applicant's epistemic ledger vs. audit ledger. Missing claim classifications are a flag.
- Voice fidelity claims vs. measured fingerprints.
- Domain breadth claims vs. actual arena spread.

### Step 4 — Findings

The reviewer surfaces findings in an issue thread. Findings are categorized:

- **Strengths**: where the applicant exceeded the rubric
- **Gaps**: where the applicant fell short
- **Required revisions**: must be addressed before the tier is awarded
- **Suggested improvements**: optional growth areas

### Step 5 — Award or Iterate

If the applicant meets the threshold (Apprentice ≥ 80, Operator ≥ 85, Architect ≥ 90), the tier is awarded and added to `certification/operators.md`. If not, the applicant addresses the required revisions and resubmits.

## Honesty Discipline

The audit assumes honest self-assessment. A reviewer who detects deliberate misrepresentation — composite client work presented as singular, fabricated outcomes, AI-generated portfolio pieces presented as authored — closes the application and records the finding. Re-application is permitted after 90 days.

## Time Expectation

| Tier | Reviewer Time | Applicant Time |
|---|---|---|
| Apprentice | 2-4 hours | 1-2 weeks (applicant pace) |
| Operator | 4-8 hours | 1-3 months |
| Architect | (by invitation, no audit clock) | (ongoing engagement) |

## Reviewer Roster

v3.0 launches with one reviewer: the maintainer (Antonio T. Smith Jr.). Architect-tier operators may be invited to join the reviewer pool. Reviewer assignments are made by the maintainer to avoid conflict of interest and to ensure consistent calibration.
