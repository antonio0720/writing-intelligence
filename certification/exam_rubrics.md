# Audit Procedure

There is no written exam. A reviewer marks the checklists in `operator_levels.md` by opening artifacts, and for the v6 tiers by putting the candidate in front of a workspace and watching what they do.

This document is how the marks get produced.

## The rule this document is written against

Every line a reviewer marks must be a thing they can fail by looking at a file or a terminal.

"Demonstrates system thinking" is not gradeable. "The child grant's expiry is later than the parent's" is: the reviewer runs `wi authority list`, reads two timestamps, and marks `FAIL`.

Where a line here reads like a judgement, it names the artifact and the comparison that settles it. If a reviewer cannot say what would have made a line fail, the line is defective and should be raised as an issue rather than marked.

## Steps

### 1 — Intake

The candidate submits:

- Deliverables: three for Apprentice, five or more for Operator.
- For each: the intake contract, the delivery bundle, the scorecard, and the pass artifacts.
- For Operator: one workspace directory containing `.wi/`, plus the `.wiab` bundle built from it.
- For Steward: nothing in advance. The Steward exercises are run live, in a workspace the reviewer prepares.
- For Architect: the merged PR and the RFC thread.
- A cover note.

### 2 — Independent re-derivation

The reviewer does not check the candidate's numbers. The reviewer produces their own and compares.

- Re-score every deliverable against `references/diagnostics/scorecard.md` without reading the candidate's scorecard first.
- Run `wi gate --exit-code` on the submitted workspace and record the exit status.
- Run `wi verify-release <bundle>` on a machine with no model and no network.
- Run `wi constraints` and record every `FAIL` and every `--`.

The order matters. A reviewer who reads the candidate's scorecard before scoring is anchored, and A4 — the honesty check — stops measuring anything.

### 3 — Mark the checklist

Mark every line in the tier's table as `ok`, `FAIL`, or `--` with a reason. Do not total them.

### 4 — Findings

Post the marked table in the application thread, with:

- **Failures** — the line, the artifact, and what the reviewer saw.
- **Not evaluated** — the line and why it could not be evaluated.
- **Notes** — anything the reviewer wants to say that is not a mark. Notes never change a mark.

### 5 — Award or return

All `ok` awards the tier and adds the candidate to `certification/operators.md` — a roster
file that **does not exist yet, because nobody has been certified.** The first award creates
it. An empty roster committed ahead of time implies a scheme that has run, which is the
failure this whole document is built to catch, committed in its own directory.

Anything else returns the application with the failing and unevaluated lines named. There is no partial award and no conditional tier.

---

## The three v6 exercises

These produce the marks for O9–O11 and S6–S12. Each one is set up by the reviewer in a scratch workspace the candidate has never seen, and each one is scored on what the candidate says before they touch anything.

### Exercise 1 — Read a simulation

**Setup.** The reviewer builds a workspace with several nodes, proposes a change to one of them, and does not accept it. Then:

```
wi simulate --actor <candidate> --json
```

The candidate is given the report and the workspace, and asked: *what does this change, and what do you have to redo?*

**Marks.**

| Line | `ok` when | `FAIL` when |
|---|---|---|
| O9a | The candidate names the changed set and it matches `changed_nodes` | They name a node that is not in it, or miss one |
| O9b | The candidate states the provably-unaffected count and it matches `provably_unaffected` | Any other number, including "most of them" |
| O9c | The candidate names the repair actions and they match `repair_plan.actions[].kind` and `.targets` | The plan omits an action the report lists |
| O10 | The repair plan touches nothing outside the frontier | The plan includes a node the report proved unaffected |
| O11a | The candidate states the workspace was not modified | They ask whether they need to undo the simulation |
| O11b | The candidate can say how they know | Only "it says simulation at the top" |

**How O11b is settled.** Two acceptable answers. The report prints `committed: false` in JSON and *Nothing was written. This root exists only to be compared.* in the human form. Or, better: the candidate runs `wi simulate` twice and shows that `base_root` is identical across both runs, so the simulation did not move the branch it was simulating against.

**The failure this catches.** Over-repair. A candidate who says "I would reverify everything to be safe" has failed O10, and the reason it matters is that the habit makes every correction expensive, and expensive corrections do not get made. `provably_unaffected` is not a hint. It is the count the engine will defend.

**A note on totals.** The repair plan reports its cost in five separate categories and says so: *categories are reported separately and never summed into a single score.* A candidate who reports "cost 4" has flattened the thing the report went to trouble to keep apart, and that is a `FAIL` on O9c.

### Exercise 2 — Read a merge refusal

**Setup.** The reviewer builds a base commit asserting a quantity, branches, changes the quantity on each branch to a different value, and merges. The merge exits 2 and preserves both.

```
wi merge <branch> --actor <candidate>
```

The candidate is asked: *what happened, and what are my options?*

**Marks.**

| Line | `ok` when | `FAIL` when |
|---|---|---|
| S8 | The candidate identifies the conflict as real, not a tool failure | They report it as a bug or ask how to force the merge |
| S9a | The candidate states that no third value was produced | They propose one |
| S9b | The candidate can name the values in the output and confirm all three appear in base, ours or theirs | They cannot say where a value came from |
| S10a | The candidate names the logical id | They describe the conflict without naming the node |
| S10b | The candidate names the conflict kind | Wrong kind, or none |
| S10c | The candidate cites Law Q as the reason the engine did not choose | They give a mechanical reason only |
| S11 | The resolution names the grant it ran under | Resolved with an actor holding no grant |
| S12 | The reason recorded is one a third party could disagree with | "Took theirs" |

**How S9a is settled.** The reviewer computes the values a splitting engine would have produced — the mean, the midpoint, the more recent one dressed as a range — and greps the merge output for each. Absent is `ok`. This is the same assertion the project's own suite makes against its own merge engine, and it is made on absence for the same reason: an averaged number reads as a decision.

**How S10c is settled.** Law Q is *semantic disagreement is preserved until resolved*. The candidate does not have to quote it. They have to say that preserving the disagreement is the correct behaviour and that resolving it requires a human decision, not a rule.

**The failure this catches.** Treating a refusal as an obstacle. Both branches were right about their own source. The engine has no basis for choosing and does not invent one — and a candidate who reaches for the middle value has produced a number no one asserted and no source supports, in a record that will later attest a human decided it.

### Exercise 3 — Read an authority refusal

**Setup.** The reviewer issues the candidate a grant that has already expired, and a second identity with no grant at all. The candidate attempts the same transition as each.

```
wi authority issue --subject <candidate> --capability claim.accept \
    --scope workspace --issuer <reviewer> --expires <a past timestamp>
wi decide <proposal> --accept --actor <candidate>
wi decide <proposal> --accept --actor nobody
```

**Marks.**

| Line | `ok` when | `FAIL` when |
|---|---|---|
| S6a | The candidate reports the expired refusal as correct behaviour | They report it as a defect, or look for a flag that overrides it |
| S6b | The candidate names the correct repair | They propose editing state directly |
| S7a | The candidate distinguishes the two refusals | They describe both as "not allowed" |
| S7b | The candidate says what each tells an operator to do next | They can name the codes and not the consequence |

**How S7a is settled.** The two refusals differ in code and in repair, and the difference is the point. Expired authority means the grant existed and its window has passed; the repair is to re-issue with a current window, and the operator should ask why nobody noticed the expiry. Absent authority means no grant was ever issued; the repair is to issue one, and the operator should ask whether this subject should hold it at all.

**Worth noticing.** `wi authority check` exits 1 for a refusal while `wi decide` exits 2 for the same condition. A check that says no is a check that worked. A transition that says no is a transition that did not happen. A candidate who spots that unprompted has demonstrated S7 conclusively.

**The failure this catches.** Expiry is the mechanism that makes delegation survivable — a grant with a window bounds the damage of a mistake to that window. An operator who treats every expiry as friction will issue everything unbounded, and then revocation is the only control left, and revocation only works if someone is watching.

---

## Honesty discipline

The audit assumes honest submission. A reviewer who finds deliberate misrepresentation — composite client work presented as a single deliverable, fabricated outcomes, generated portfolio pieces presented as authored — closes the application and records the finding in the thread. Re-application is permitted after 90 days.

Three things are not misrepresentation and are not treated as such:

- Self-scoring low. A4 fails inflation, not modesty.
- Submitting work that fails. A candidate who submits a deliverable and says "this one scored 71 and here is why" is doing what the tier is for.
- A `--` the candidate could not resolve. Unevaluated is not dishonest.

## Time

| Tier | Reviewer time | Candidate elapsed |
|---|---|---|
| Apprentice | 2–4 hours | candidate's own pace |
| Operator | 4–8 hours, plus one live session for Exercise 1 | weeks to months |
| Steward | 2–3 hours, all live: three exercises in one session | one session, after the workspace is prepared |
| Architect | no clock; the contribution is the audit | ongoing |

Steward is the shortest audit and the hardest to pass. Nothing is submitted in advance, so nothing can be rehearsed against.

## Reviewer roster

One reviewer: the maintainer, Antonio T. Smith Jr.

This is a limit and it is stated in `README.md` under "What certification cannot tell you". Cross-reviewer calibration has not been demonstrated, because there has never been a second reviewer. Architect-tier operators may be invited into the pool; when a second reviewer exists, two reviewers will mark one application independently and the disagreements will be published, because that is the only way to find out whether the checklists mean the same thing to two people.
