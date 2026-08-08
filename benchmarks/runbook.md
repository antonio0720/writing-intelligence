# Benchmark Runbook

Two classes, two procedures. Run both. Report them separately.

There is no `wi benchmark` subcommand. The v3 runbook named one and marked it "reference implementation ships in v3.1"; it never shipped, and naming a command that does not exist is the failure mode this project exists to prevent. Every command below was read out of `scripts/wi.py` before it was written here.

## Class A — prose quality

### Full suite

1. Load `benchmarks/benchmark_manifest.yaml`.
2. For each **authored** case (`authored: > 0` in `categories`):
   - Read the case file.
   - Load the case's `task_contract`.
   - Run the 11-pass kernel with that contract on the case's `input`.
   - Capture the output, the scorecard, and the delivery bundle.
3. Compare to baseline: `delta = current_score - baseline_score`, and check the case falls within `expected_score_range`.
4. For each `expected_failure_detection`, verify it appears in the diagnostic report, the epistemic ledger, or the stress battery.
5. Validate the delivery bundle against `schemas/delivery_bundle.schema.json`.
6. Log the result with the `BenchmarkResultV3` schema.

Reserved slots are not run and are reported as reserved, never as passed.

### Decisions

| Decision | Meaning |
|---|---|
| `PASS` | Score within range, expected detections present, bundle valid, no regression |
| `CONDITIONAL_PASS` | Score within range with a documented regression of ≤ 3 points |
| `FAIL` | Score below range, an expected detection missing, or the bundle invalid |

## Class B — runtime correctness

Each case is a scripted sequence against a scratch workspace, an assertion set, and a negative twin.

### The shape

```
setup    build a workspace whose correct answer is known by construction
run      the exact command in the case
assert   field equality, string presence, string absence, exit code
twin     mutate the setup so the assertion must fail; confirm it does
teardown discard the workspace
```

A case that has not had its twin run has not been shown to fail. `negative_twin_required: true` in the manifest is the gate.

### Assertion helpers

`tests/v6/test_wi6.sh` already defines the four helpers the cases assume. Reuse them rather than writing new ones.

```sh
check "label" "$ACTUAL" "$EXPECTED"   # equality
has   "label" "$OUT" "needle"         # substring present
hasnt "label" "$OUT" "needle"         # substring absent
ok / bad                              # direct pass / fail
```

`hasnt` is the one that matters. B1 and B6 are both absence assertions, and a suite with no `hasnt` cannot detect a fabricated value or a verifier that prints its verdict independently of its checks.

### Reading a result out of JSON

Every v6 command takes `--json`. Read fields rather than grepping human output, except where the assertion is deliberately about the rendered bytes.

```sh
python3 -c 'import sys,json; print(json.load(sys.stdin)["candidate_root"])'
```

Field names used by the authored cases, confirmed against the running tool:

| Command | Fields read |
|---|---|
| `wi proposals --json` | `proposals[].proposal_id`, `.status`, `.node`, `.requires` |
| `wi simulate --json` | `base_root`, `candidate_root`, `committed`, `changed_nodes`, `stale_frontier`, `hard_stale_frontier`, `provably_unaffected`, `total_nodes`, `repair_plan.actions[].kind`, `.targets` |
| `wi commit --json` | `root`, `prior_root`, `commit`, `applied` |
| `wi merge --json` | `clean`, `merge_commit`, `conflicts[].kind`, `.logical_id`, `.conflict_id`, `.classes`, `.base_summary`, `.ours_summary`, `.theirs_summary`, `.required_resolution`, `.status`, `stored_conflicts` |
| `wi conflicts --json` | `unresolved`, `conflicts[].conflict_id`, `.status` |
| `wi canon --json` | `content_digest`, `state_digest_v5`, `state_digest_v6`, `canonicalization`, `normalization` |
| `wi constraints --json` | per-constraint `id`, `status`, `detail` |

`wi proposals --json` returns `proposal_id`, not `id`. Getting this wrong yields a `KeyError` in the harness, not a wrong answer, which is the good failure — but it is the first thing that goes wrong when writing a new case.

### Decisions

| Decision | Meaning |
|---|---|
| `PASS` | Every assertion held, and the negative twin failed |
| `FAIL` | Any assertion did not hold |
| `NOT_EVALUATED` | The case did not run. Always carries the reason. |

There is no conditional pass in Class B. A merge either fabricated a value or it did not.

`NOT_EVALUATED` blocks the release exactly as `FAIL` does, and is reported separately, because a broken mechanism and an unwritten case need different work.

## A worked Class B setup

The pattern both authored case files use. Reproduce it exactly; the divergence order is the part that is easy to get wrong.

```sh
WI=scripts/wi.py
P(){ python3 $WI proposals --status open ${1:+--branch $1} --json \
     | python3 -c 'import sys,json;print(json.load(sys.stdin)["proposals"][0]["proposal_id"])'; }

python3 $WI init . --title bench
python3 $WI authority issue --subject ant --capability claim.accept \
        --scope workspace --issuer author
python3 $WI authority issue --subject ant --capability claim.accept.quantity_change \
        --scope workspace --issuer author

# base
python3 $WI propose --node hh --payload base.json --why base --actor ant
python3 $WI decide $(P) --accept --actor ant
python3 $WI commit -m base --actor ant

# diverge — branch from the base, then move BOTH sides
python3 $WI branch create audit
python3 $WI propose --node hh --payload ours.json --why ours --actor ant
python3 $WI decide $(P) --accept --actor ant
python3 $WI commit -m ours --actor ant

python3 $WI branch switch audit
python3 $WI propose --node hh --payload theirs.json --why theirs --actor ant --branch audit
python3 $WI decide $(P audit) --accept --actor ant
python3 $WI commit -m theirs --actor ant --branch audit

python3 $WI branch switch main
python3 $WI merge audit --actor ant --json
```

**The mistake to avoid.** Creating the branch *after* main has already moved leaves only one side diverged from the base, and the merge is correctly clean: it reports `Clean merge.` and exits 0. A conflict-preservation case built that way asserts nothing, and passes.

**Quantities must be typed.** The conflict *kind* is derived from the semantic delta classes, and `quantity_changed` is detected from a typed `quantities` array in the payload, not from digits in the prose. A payload carrying only `text` classifies as `evidence_changed` and the conflict reports as `Evidence`. Both are real conflicts and both are preserved; only the typed form produces `Quantity` and requires `claim.accept.quantity_change`.

```json
{"text": "The programme served 11800 households in 2024.",
 "quantities": [{"coefficient": 11800, "scale": 0, "unit": "household"}]}
```

## Release gate

The release passes when:

- Every Class A gate in `gates:` is met, computed over `authored_category_cases`.
- No Class A `FAIL`.
- Every runtime gate in `runtime_gates:` reports `0` failures.
- No runtime gate reports `NOT_EVALUATED`.

A single Class B failure blocks the release. Class B does not contribute to any Class A average and does not offset a Class A regression.

At v6.0.0 four runtime gates report `NOT_EVALUATED` because their cases are not authored: `b3_impact_precision`, `b4_authority`, `b5_digest_stability`, `b6_capsule_verification`. The mechanisms exist and are exercised by `tests/v6/test_wi6.sh`; what does not exist is a benchmark case with a negative twin. Until those are written the benchmark suite cannot clear its own gate, and the report says so rather than omitting the rows.

## Adding a case

### Class A

Follow `cases/_template.md`. Append to the appropriate `cases/{category}.md`, then in `benchmark_manifest.yaml` increment that category's `authored`, `authored_category_cases`, `authored_cases` and `total_cases` as applicable.

### Class B

Follow `cases/_template.md` for structure. Then:

1. Write the setup so the correct answer is known by construction, not by running the tool and recording what it said. A case whose expected value was copied from the output cannot detect a regression; it will agree with whatever the tool does next.
2. State every assertion as a field equality, a string presence, a string absence or an exit code.
3. Include at least one absence assertion.
4. Write the negative twin and run it. Record what it broke.
5. Register under `runtime_cases`, increment `authored_runtime_cases`, `authored_cases` and `total_cases`.

Point 1 is the one that gets skipped. Recording observed output as the expectation produces a suite that passes forever.

## Reports

Reports live in `reports/`, which does not exist until the first run writes one. Each report is tagged with the version and the date, and prints Class A and Class B separately with no combined figure.
