# Benchmark Runbook

## Running the Full Suite

1. **Load the manifest**: `benchmarks/benchmark_manifest.yaml`.
2. **For each case**:
   - Read the case file (`cases/{category}.md`).
   - Load the case's `task_contract` (intake contract JSON).
   - Run the 11-pass kernel with that contract on the case's `input`.
   - Capture the output, scorecard, and any delivery blocks.
3. **Compare to baseline**:
   - Load `v2_baseline_output` and its score.
   - Compute `delta = v3_score - v2_baseline_score`.
   - Verify the case falls within `expected_score_range`.
4. **Verify expected detections**:
   - For each `expected_failure_detection`, verify it appears in the diagnostic report, epistemic ledger, or stress battery.
5. **Verify delivery bundle**:
   - Run `delivery_bundle.schema.json` validation.
6. **Log result** to `reports/{date}_{release}.md` with the `BenchmarkResultV3` schema.

## Running a Single Case

```
wi benchmark --case GRANT-04 --against v2.0
```

(Reference CLI; reference implementation ships in v3.1.)

## Pass / Conditional Pass / Fail

| Decision | Meaning |
|---|---|
| `PASS` | Score within expected range, expected detections present, delivery bundle valid, no regression |
| `CONDITIONAL_PASS` | Score within range but with documented regression of ≤ 3 points |
| `FAIL` | Score below expected range, expected detection missing, or delivery bundle invalid |

## Release Gate Decision

Aggregate the case results. The release passes the benchmark gate when:

- `pct_cases_improved` ≥ 70%
- No `FAIL` decisions
- All gates from `benchmark_manifest.yaml` met

A single `FAIL` blocks the release.

## Adding a New Case

1. Pick the appropriate `cases/{category}.md` file.
2. Append a new case using the schema:

```yaml
case_id: GRANT-06
input: |
  [the prompt or source draft]
task_contract:
  mode: rewrite
  intent: persuade
  audience: federal program officer
  voice: investor_precision
  genre_stack: [grant_nofo, government_brief]
  high_stakes: true
  arena: grant_response
  success_condition: "Funder believes the program produces outcomes per dollar."
expected_failure_detection:
  - "Inflated verbs in outcome statements"
  - "Universal beneficiary claim"
expected_score_range:
  min: 85
  max: 95
v2_baseline_output: |
  [v2 output text]
v2_baseline_score: 78
v3_expected_output: |
  [v3 target output text]
v3_target_score: 91
scoring_notes: |
  Apply Prose Quality + Epistemic Integrity + Arena Fit.
regression_hazards:
  - "Risk of compression dropping a required compliance section"
```

3. Update `benchmark_manifest.yaml` total count.
4. Open a PR; PR cannot merge until the new case runs cleanly.

## Public Reports

Reports live in `reports/`. Each release tags its report with the version and date. Reports are public — they are the proof of the v3.0 doctrine that quality must be auditable.
