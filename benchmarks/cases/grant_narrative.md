# Benchmark Category — Grant Narrative

Five cases. Each pressure-tests the `grant_nofo` pack against real funder constraints: compliance, evidence, outcome logic, budget narrative alignment.

---

## GRANT-01 — Federal NOFO Statement of Need

**Input**: Three-paragraph statement of need with universal beneficiary claim, inflated verbs, no quantified problem statement.

**Task Contract**: rewrite, persuade, federal program officer, investor_precision + courageous_builder voice, `grant_nofo` + `government_brief`, high_stakes, arena = `grant_response`, success: "Funder sees a scoped, evidenced problem statement they can fund."

**Expected Detections**: "transformative", "countless families", universal beneficiary claim, missing geographic scope, missing population specificity, missing data source.

**Expected Range**: 85-95. **v2 baseline**: 76. **v3 target**: 91.

---

## GRANT-02 — Foundation LOI

**Input**: A concept paper with three projected outcomes stated as facts.

**Task Contract**: rewrite, inform + persuade, foundation program officer, casual_sharp + courageous_builder, `grant_nofo`, high_stakes, arena = `grant_response`, success: "Foundation officer trusts the projection enough to request a full proposal."

**Expected Detections**: future-tense outcome stated as fact, missing methodology, missing prior-year evidence, missing organizational track record.

**Expected Range**: 83-92. **v2 baseline**: 74. **v3 target**: 88.

---

## GRANT-03 — Budget Narrative Alignment

**Input**: A budget narrative referencing "staff time" without naming the staff member, "training" without naming the program, "evaluation" without the evaluator.

**Task Contract**: rewrite, inform, federal compliance reviewer, investor_precision, `grant_nofo`, high_stakes, arena = `grant_response`, success: "Every budget line maps 1:1 to a program activity. Every program activity has a budget line."

**Expected Detections**: missing role names, missing training names, missing evaluator, missing dollar specificity, missing match-funding identification.

**Expected Range**: 88-95. **v2 baseline**: 78. **v3 target**: 92.

---

## GRANT-04 — Logic Model

**Input**: A 1-paragraph logic model that conflates outputs and outcomes.

**Task Contract**: rewrite, teach + inform, federal program officer, investor_precision, `grant_nofo`, high_stakes, arena = `grant_response`, success: "Inputs, activities, outputs, outcomes, and impact are distinct and chained."

**Expected Detections**: output / outcome conflation, missing impact level, missing measurement methodology.

**Expected Range**: 85-93. **v2 baseline**: 75. **v3 target**: 90.

---

## GRANT-05 — Sustainability Plan

**Input**: A sustainability plan that says "We will diversify funding sources" without naming any.

**Task Contract**: rewrite, persuade, federal program officer, courageous_builder, `grant_nofo`, high_stakes, arena = `grant_response`, success: "Funder sees a credible, specific path to sustaining the program after the grant period."

**Expected Detections**: vague "diversify funding sources", missing named sources, missing target percentages, missing fee-for-service or earned-revenue identification.

**Expected Range**: 82-92. **v2 baseline**: 73. **v3 target**: 88.

---

## Scoring Rubrics Applied

- Prose Quality (100)
- Epistemic Integrity (100) — **mandatory** in high-stakes
- Arena Fit (100)

## Regression Hazards

- Risk: Rewrite removes a required RFP section because the contract didn't capture it.
- Risk: Voice restoration drifts too warm and undermines compliance posture.
- Risk: Logic model becomes mechanical and loses the narrative throughline.
