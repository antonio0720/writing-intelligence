# Benchmark Category — Simulation Fidelity

Four cases. Each pressure-tests `wi simulate` against the two things a preview must do: predict the state that lands, and change nothing while predicting it.

Class B — runtime correctness. Pass or fail, never scored. The template's `**Expected Range**` line asks for a 0–100 score and a baseline delta; those do not apply here, so each case states its result as `PASS` / `FAIL` and carries an `## Assertions` and `## Negative Twin` section instead. Everything else follows `_template.md`.

Gate: `b2_simulation_fidelity`. Law P — *autonomy produces replayable proposals, not invisible mutations.*

No digest is hardcoded in these cases. Every assertion is an equality between two values read from the same run. A case that pins a literal root hash tests the fixture, not the engine.

---

## SIM-01 — The predicted root is the root that lands

**Input**: A workspace with three committed nodes. One pending proposal revising one of them. Nothing accepted.

**Task Contract**:

```yaml
mode: audit
intent: inform
audience: release reviewer
voice: n/a
genre_stack: []
high_stakes: true
arena: runtime_correctness
success_condition: "The root the simulation predicts is byte-identical to the root the commit produces."
```

**Expected Detections**: `changed_nodes` names exactly the proposed node; `candidate_root` is present and differs from `base_root`.

**Expected Result**: `PASS`. Exit code `0` for both commands.

**Why this case exists.** Everything an operator does with a simulation — deciding whether to accept, deciding what to reverify, deciding whether to escalate — is a decision about a state that does not exist yet. If the predicted root is not the root that lands, every one of those decisions was made about a state that never existed, and nobody finds out until after the commit.

---

## SIM-02 — The preview writes nothing

**Input**: The same workspace and pending proposal as SIM-01. `wi simulate` is run twice with no intervening command.

**Task Contract**:

```yaml
mode: audit
intent: inform
audience: release reviewer
voice: n/a
genre_stack: []
high_stakes: true
arena: runtime_correctness
success_condition: "Simulating a change does not move the branch the change was simulated against."
```

**Expected Detections**: `committed` is `false`; `base_root` is identical across both runs; `candidate_root` is identical across both runs; the pending proposal is still `open`.

**Expected Result**: `PASS`. Exit code `0`.

**Why this case exists.** `committed: false` is the engine's own claim about itself, and a claim you cannot point at has not been verified. The stable `base_root` across two runs is the pointer: the branch the simulation measured against is in the same place afterwards.

The determinism half is not incidental. If `candidate_root` differed between two runs over identical inputs, the prediction would be unfalsifiable — you could never tell a wrong prediction from a second, different one.

---

## SIM-03 — Fidelity holds across a multi-proposal set

**Input**: A workspace with three committed nodes and **two** pending proposals against two different nodes. Both are simulated together, then both are accepted and committed in one transaction.

**Task Contract**:

```yaml
mode: audit
intent: inform
audience: release reviewer
voice: n/a
genre_stack: []
high_stakes: true
arena: runtime_correctness
success_condition: "The candidate root for a set of proposals equals the root of the single transaction that applies them."
```

**Expected Detections**: `changed_nodes` names both nodes; `applied` equals 2 in the commit result.

**Expected Result**: `PASS`. Exit code `0`.

**Why this case exists.** SIM-01 could pass on an engine that computes the candidate root by applying one delta. A commit applies the accepted set as one transaction, and the order and grouping have to produce the same root as the simulation's. Ordering bugs are invisible with one proposal.

---

## SIM-04 — The prediction is bound to a base, and says so

**Input**: A workspace with two committed nodes. A proposal against node `a` is simulated, and `candidate_root` is recorded. Before it is accepted, an **unrelated** proposal against node `b` is accepted and committed, moving the branch. Then the original proposal is accepted and committed.

**Task Contract**:

```yaml
mode: audit
intent: inform
audience: release reviewer
voice: n/a
genre_stack: []
high_stakes: true
arena: runtime_correctness
success_condition: "When the base moves, the earlier prediction no longer matches, and the mismatch is detectable from the commit result alone."
```

**Expected Detections**: the final `root` differs from the recorded `candidate_root`; the final `prior_root` differs from the recorded `base_root`.

**Expected Result**: `PASS`. Exit code `0` throughout.

**Why this case exists.** This is the case that proves SIM-01 is not vacuous. A predicate that holds unconditionally is not a guarantee, it is a tautology. `candidate_root == root` is true **only while the base has not moved**, and this case establishes the boundary.

It also establishes how the boundary is detected, which matters more. Two kinds of drift behave differently, and only one of them announces itself:

| Drift | Behaviour |
|---|---|
| The **same** node moves under the proposal | The decision is refused: `WI_DECISION_STALE`, exit 2, *"the system will not reattach an approval to a state the reviewer never saw"*. The mismatch cannot happen because the transition cannot happen. |
| An **unrelated** node moves | The decision succeeds. The commit lands. The root differs from the prediction and nothing has said so. |

So a harness that only asserts `candidate_root == root` is not enough. It must also assert `prior_root == base_root`, because that is the field that distinguishes "the prediction was wrong" from "the prediction was about a different base". Without it, an operator acting on a stale simulation of an unrelated-drift workspace has no signal at all.

---

## Assertions

`SIM` reads `wi simulate --actor <actor> --json`. `COMMIT` reads `wi commit -m <msg> --actor <actor> --json`.

### SIM-01

| # | Assertion | Kind |
|---|---|---|
| 1 | `SIM.candidate_root == COMMIT.root` | equality |
| 2 | `SIM.base_root == COMMIT.prior_root` | equality |
| 3 | `SIM.candidate_root != SIM.base_root` | inequality |
| 4 | `SIM.changed_nodes` equals the proposed set exactly | set equality |
| 5 | `COMMIT.applied == 1` | field |
| 6 | both exit codes are `0` | exit |

Assertion 3 is not decorative. A simulation that returned the base root as the candidate root would satisfy assertion 1 on an engine whose commit also did nothing.

### SIM-02

| # | Assertion | Kind |
|---|---|---|
| 1 | `SIM.committed == false` | field |
| 2 | `SIM_first.base_root == SIM_second.base_root` | equality |
| 3 | `SIM_first.candidate_root == SIM_second.candidate_root` | equality |
| 4 | the proposal's `status` is still `open` after both runs | field |
| 5 | output does **not** contain `merge commit` | **absence** |
| 6 | exit code is `0` | exit |

Assertion 2 is the one that carries the case. Assertion 1 is the engine describing itself and would pass on an engine that wrote to the branch and printed `false`.

### SIM-03

| # | Assertion | Kind |
|---|---|---|
| 1 | `SIM.candidate_root == COMMIT.root` | equality |
| 2 | `SIM.base_root == COMMIT.prior_root` | equality |
| 3 | `SIM.changed_nodes` equals both proposed nodes exactly | set equality |
| 4 | `COMMIT.applied == 2` | field |
| 5 | both exit codes are `0` | exit |

Assertion 3 is a set comparison, not a length check. Two wrong sets can have the right size.

### SIM-04

| # | Assertion | Kind |
|---|---|---|
| 1 | `SIM_before.candidate_root != COMMIT_after.root` | inequality |
| 2 | `SIM_before.base_root != COMMIT_after.prior_root` | inequality |
| 3 | the drift commit exits `0` | exit |
| 4 | the final commit exits `0` | exit |
| 5 | same-node variant: `wi decide` on the stale proposal exits `2` | exit |
| 6 | same-node variant: the refusal names `WI_DECISION_STALE` | presence |

Assertions 1 and 2 must both hold. If 1 holds and 2 does not, the roots diverged for some reason other than base drift, which is a different failure and a worse one.

---

## Negative Twin

Each twin must be run and must fail.

| Case | Mutation | Assertion that must go red |
|---|---|---|
| SIM-01 | Perturb the recorded `candidate_root` by one character before comparing | 1 |
| SIM-01 | Simulate proposal X and commit proposal Y | 1, 4 |
| SIM-02 | Accept the proposal between the two simulation runs | 2, 3, 4 |
| SIM-03 | Accept and commit only one of the two proposals | 1, 4 |
| SIM-04 | Remove the drift commit, so the base never moves | 1, 2 — the roots match and the case correctly fails |

The SIM-04 twin is the one worth running by hand. It is the only twin here that fails by the system behaving *correctly*, and it is what proves SIM-04 is testing the boundary rather than asserting that two hashes happen to differ.

---

## Scoring Rubrics Applied

None. This is a runtime-correctness case and is not scored.

A root hash is either equal to another root hash or it is not. There is no partial credit available and inventing one would put a number into the report that could later be averaged with the Class A results.

---

## Regression Hazards

- **Non-determinism in canonicalization.** Anything that admits a timestamp, a map iteration order or a locale-dependent comparison into the state digest breaks SIM-02 assertion 3 first, and SIM-01 intermittently. Intermittent is the dangerous form: it will be re-run and pass.
- **Divergent apply paths.** If `simulate` and `commit` compute the next state through different code, SIM-01 can pass on a single proposal and SIM-03 fail on two. This is the specific reason SIM-03 exists.
- **A candidate root computed from the proposal rather than the resulting state.** Passes SIM-01 and SIM-03, fails SIM-04 assertion 1 in the wrong direction: the prediction would keep matching after the base moved, which is worse than not matching, because it would confirm a stale plan.
- **Silent staleness widening.** If `WI_DECISION_STALE` were extended to fire on unrelated drift, SIM-04 assertions 1–4 become unreachable and the case reports failures that are in fact a tightened guarantee. The case would need rewriting rather than the change reverting — noted here so the next reader does not read a red SIM-04 as a regression without checking which branch of the table changed.
- **`committed: false` becoming a constant.** Assertion 1 of SIM-02 would still pass. Only assertion 2 would catch it.
