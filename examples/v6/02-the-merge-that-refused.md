# Example 02 — The Merge That Refused

**Commands**: `branch` → `merge` → `conflicts` → `constraints`
**Law**: Q — semantic disagreement is preserved until resolved
**Doctrine**: [`MERGE_PROTOCOL.md`](../../references/v6/MERGE_PROTOCOL.md)

Every transcript below was recorded on 2026-08-08 against `wi 6.0.0`, Python
3.11.15, in a scratch workspace built by the setup block.

---

## The situation

Two people are working on the same grant narrative.

The program officer takes the figure from the agency outcomes report, table 4:
**11,800 households in 2022**.

The auditor reconciles against county intake logs and arrives at **12,400**.

Both were doing their jobs. Both were right about the job they were doing. Both
committed under a valid grant, against the same base. Neither knew the other was
answering the same question.

---

## What every other tool does with this

A text merge asks one question: did these two edits touch overlapping lines? If
the two figures live in different files — a narrative paragraph and a board deck
bullet — the answer is no, both apply, and the merge reports success. The release
now says 11,800 in one place and 12,400 in another, and nothing in the toolchain
is looking for that.

If they do overlap, the tool stops and shows a human the region, which is fine.

The dangerous case is the first one, and it is the common one.

**And a model asked to reconcile them will write something worse.** It produces
*"approximately 12,000 households"* — a figure neither branch asserted, no source
supports, and nobody can be held to. It reads like diligence. It survives review,
because a reviewer checking that sentence finds a hedge where they expected a
number and reads the hedge as caution. It arrives wearing the authority of a
machine that checked things.

The mean of 11,800 and 12,400 is 12,100. Round it and you get 12,000. Neither
number exists in any source in this workspace.

---

## Setup

```bash
mkdir -p ~/scratch/ex02 && cd ~/scratch/ex02
alias wi="python3 /path/to/writing-intelligence/scripts/wi.py"

wi init --title "Delta Regional Capacity" --mode strict
wi authority issue --subject antonio --capability claim.accept \
   --scope workspace --issuer antonio --expires 2030-01-01T00:00:00+00:00
```

Two claims form the shared base. The household figure is deliberately absent from
it — the claim gets added late, by two people at once, from two sources, which is
how this actually happens.

```bash
# waittime.json and counties.json as in example 01
for n in waittime counties; do
  wi propose --node $n --payload $n.json --why "baseline" --actor antonio
done
# accept both, then:
wi commit -m "baseline figures from the outcomes report" --actor antonio
wi branch create audit
```

```
COMMIT a15d855289e0
  branch      main
  prior root  sha256:87e2f3219580cb3db904fddc9669a3d7ecbe313f745923700b41a9bd8d60eae7
  next root   sha256:c8d72bac7d705a1b6d61af71ea8b59efb2dfe6fb2decc67836ba46ce721898bf
```

```
created audit at a15d855289e0
A branch is a ref. Nothing was copied: the objects are immutable
and shared, so this cost one row.
```

Now the two branches diverge on the same claim.

```bash
# on main
wi propose --node households --payload ours.json \
   --why "agency outcomes report, table 4" --actor antonio
# accept, then:
wi commit -m "ours: 11800 from the outcomes report" --actor antonio

# on audit
wi branch switch audit
wi propose --node households --payload theirs.json \
   --why "reconciled against county intake logs" --actor antonio
# accept, then:
wi commit -m "theirs: 12400 from county intake logs" --actor antonio

wi branch switch main
wi branch list
```

```
BRANCHES
    audit                    05d25be79f8d     3 nodes  theirs: 12400 from county intake logs
  * main                     9000e8cd6cfc     3 nodes  ours: 11800 from the outcomes report
```

---

## The merge

```bash
wi merge audit --actor antonio
```

```
MERGE audit into main

  base commit  a15d855289e0

Conflicts — preserved, not resolved
  Quantity     households
      base    (absent)
      ours    The program served 11800 households in 2022.
      theirs  The program served 12400 households in 2022.
      status  unresolved, requires an authorized decision

The engine did not average, soften or generalize these.
Neither branch asserted a middle value, so there is none.
```

```bash
echo $?
```

```
2
```

The conflict is typed. Not *a conflict in households* — a **Quantity** conflict,
because the dimension that disagrees is the one that decides what authority is
needed to settle it and what breaks downstream. Two branches that had moved
disjoint dimensions of the same claim — one adding a temporal bound, one
correcting the attribution — would have merged without asking, and that is the
row of the protocol that earns it. A merge that stopped on everything is a merge
nobody runs.

`base (absent)` is accurate here: neither side edited a shared value, both
created the node independently.

---

## The root does not move

```bash
wi log --limit 1 --json | python3 -c "import json,sys;print(json.load(sys.stdin)['commits'][0]['root'])"
```

```
sha256:cbeeac875d9a57665d34409dd3d7378a504867e20ea83f8082e800daec9ec0cd
```

That is the same root the branch held before the merge ran. A blocked merge
leaves the branch exactly where it was. There is no partial application to unwind.

---

## The number that is not there

The whole release turns on an absence, so it is worth checking rather than
asserting. Scanning the merge output for the values a helpful system would have
produced:

```
arithmetic mean of the two asserted values: 12100
ABSENT   '12100'
ABSENT   '12000'
ABSENT   '12,100'
ABSENT   '12,000'
ABSENT   'approximately'
```

There is no flag that makes the merge pick a side on its own, and no setting that
turns averaging on. **The absence is the feature**, and it is asserted on every
run of the regression suite rather than left to inspection — see
[`tests/v6/test_wi6.sh`](../../tests/v6/test_wi6.sh):

```bash
hasnt "the merge did not invent 12100" "$OUT" "12100"
hasnt "the merge did not invent 12000" "$OUT" "12000"
```

Delete the conflict-preservation logic and those two assertions go red. That is
what makes them worth having. A suite that only walked the happy path would stay
green with the entire control removed, and a green suite that survives the removal
of the thing it tests is worse than no suite — it certifies nothing while looking
like assurance.

### Why Law Q is written as a prohibition

Splitting the difference is what a helpful system does. That is the difficulty.
It is not a bug anyone introduces on purpose; it is the behaviour that arrives
when a component is asked to be useful about a disagreement.

**Last-writer-wins is a correctness policy nobody would choose if asked.** It
means whoever saved second was right, about a question neither of them knew they
were answering. Averaging is worse, because it produces a value with no author.
The 11,800 can be traced to table 4. The 12,400 can be traced to the intake logs.
The 12,100 can be traced to nothing, and it is the one that would have shipped.

**A conflict is not a failure of the merge. It is the merge's most useful output.**

---

## The conflict is an object, not a message

```bash
wi conflicts
```

```
SEMANTIC CONFLICTS on main

  [unresolved] Quantity     3bdf0e13-2e67-5a14-8d0e-b25ecc559aa3
      node    households
      ours    The program served 11800 households in 2022.
      theirs  The program served 12400 households in 2022.

1 unresolved. A branch carrying an unresolved conflict
cannot be rendered as agreed (C015).
```

It survives the terminal session. It has an id you can point at in a ticket. And
it blocks release:

```bash
wi constraints
```

```
  FAIL C015 semantic-conflict-cannot-be-rendered-as-resolved
15 evaluated, 5 not evaluated, 1 failed.
VERDICT FAIL
```

Note `5 not evaluated`. Those are not passes. Five constraints depend on
subsystems that do not ship in 6.0.0, each names its reason, and folding them
into a pass would be the exact failure this project exists to catch. There is
also no percentage anywhere in that output, and the suite asserts its absence — a
constraint engine that emits a score has averaged across kinds of failure that
are not commensurable, and the number is what would get quoted.

---

## Resolution is a decision, by a named actor, under a named grant

```bash
wi conflicts --resolve 3bdf0e13-2e67-5a14-8d0e-b25ecc559aa3 --take theirs --actor antonio
```

```
resolved 3bdf0e13-2e67-5a14-8d0e-b25ecc559aa3 by taking theirs
  actor antonio under grant e322307b-57f3-5158-8108-67c315933eb2 (claim.accept.quantity_change)
```

```bash
wi constraints
```

```
  ok   C015 semantic-conflict-cannot-be-rendered-as-resolved
15 evaluated, 5 not evaluated, 0 failed.
VERDICT PASS
```

Somebody chose. The record says who, under which grant, and which capability that
grant carried.

---

## The rejected number is still there

```bash
wi conflicts --json
```

```json
{
  "base": null,
  "base_summary": "(absent)",
  "classes": ["quantity_changed"],
  "conflict_id": "3bdf0e13-2e67-5a14-8d0e-b25ecc559aa3",
  "kind": "Quantity",
  "logical_id": "households",
  "ours": "sha256:eb3684fc7e531e51ef064dd4a430d7c77cb7e744baf392d17b8632f3e708e7f0",
  "ours_summary": "The program served 11800 households in 2022.",
  "required_resolution": "authorized_decision",
  "schema": "wi.v6.conflict",
  "status": "resolved:theirs",
  "theirs": "sha256:4dc4a118114cc9c568b349dd16ae711868fed001773dee4232d2a507ec86537d",
  "theirs_summary": "The program served 12400 households in 2022."
}
```

`status` is `resolved:theirs`. The losing state is still named, still summarized,
still addressable by digest.

*Somebody chose 12,400 over 11,800* is a different historical fact from *only
12,400 ever existed*. Three years later, when a reviewer asks why the narrative
disagrees with the outcomes report, the first fact answers the question and the
second one cannot. A record that cannot tell them apart is not a record of a
decision.

---

## What this example does not show

- **The base was absent.** Both branches created the node. A conflict where all
  three states exist prints the base value too, and the resolution options are
  the same.
- **One dimension conflicted.** The protocol compares quantity, unit, temporal
  scope, modality, certainty, attribution, negation, causal force, geographic
  and population scope, exceptions and legal force. Disjoint moves merge.
- **`--take ours` and `--take theirs` are the resolutions used here.** Neither
  branch's value was edited during resolution; a third value would be a new
  proposal, decided on its own terms.
- **No source anchoring.** Whether 12,400 is right is not a question this
  workspace can answer. It verifies support within supplied sources, and none
  were supplied.

---

## Pattern to reuse

```bash
wi merge OTHER --actor YOU        # exits 2 if meaning conflicts; root does not move
wi conflicts                      # the typed disagreement, with an id
wi constraints                    # C015 fails while it stands
wi conflicts --resolve ID --take ours|theirs --actor YOU
```

Next: [`03-authority-that-expires.md`](03-authority-that-expires.md) — who was
allowed to take that decision, and for how long.
