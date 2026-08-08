# Example 01 — Simulate Before You Edit

**Commands**: `propose` → `simulate` → `decide` → `commit`
**Laws**: M (state is canonical), P (proposals, not mutations), R (freshness is a property of dependencies)
**Doctrine**: [`COUNTERFACTUAL_SIMULATION.md`](../../references/v6/COUNTERFACTUAL_SIMULATION.md)

Every transcript below was recorded on 2026-08-08 against `wi 6.0.0`, Python
3.11.15, in a scratch workspace built by the setup block.

---

## The situation

A grant narrative rests on a figure from an agency outcomes report: the program
served 11,800 households in 2022. The agency reissues the report after
deduplicating its intake records. The number is now 11,240.

The author knows what happens next, because it has happened before. Search the
manuscript. Hope you found every instance. Hope somebody updated the board deck.
Hope the website is not still quoting the old figure. The work is not the edit —
the work is the uncertainty about the blast radius, and it is unbounded, so it
gets budgeted as *the rest of the afternoon*.

The question that would end it is *what does this change actually touch*, and in
v5 the only way to ask was to make the change.

---

## Setup

```bash
mkdir -p ~/scratch/ex01 && cd ~/scratch/ex01
alias wi="python3 /path/to/writing-intelligence/scripts/wi.py"

wi init --title "Delta Regional Capacity" --mode strict
wi authority issue --subject antonio --capability claim.accept \
   --scope workspace --issuer antonio --expires 2030-01-01T00:00:00+00:00
```

Three claims go in as the baseline. Only the first one matters to this example;
the other two exist so the report has a denominator.

```bash
cat > households.json <<'JSON'
{"text":"The program served 11800 households in 2022.",
 "quantities":[{"coefficient":11800,"scale":0,"unit":"households"}],
 "temporal_scope":{"from":"2022-01-01","until":"2023-01-01"},
 "modality":"is","subject":"program","spatial_scope":["Delta region"]}
JSON
cat > waittime.json <<'JSON'
{"text":"Median intake wait time fell from 42 days to 26 days.",
 "quantities":[{"coefficient":26,"scale":0,"unit":"days"}],
 "temporal_scope":{"from":"2019-01-01","until":"2023-01-01"},
 "modality":"is","subject":"intake","spatial_scope":["Delta region"]}
JSON
cat > counties.json <<'JSON'
{"text":"Services reached seven counties.",
 "quantities":[{"coefficient":7,"scale":0,"unit":"counties"}],
 "temporal_scope":{"from":"2019-01-01","until":"2023-01-01"},
 "modality":"is","subject":"services","spatial_scope":["Delta region"]}
JSON

for n in households waittime counties; do
  wi propose --node $n --payload $n.json \
     --why "baseline figure from the outcomes report" --actor antonio
done
# accept all three, then:
wi commit -m "baseline figures from the outcomes report" --actor antonio
```

```
COMMIT cd1e46340db6
  branch      main
  prior root  sha256:87e2f3219580cb3db904fddc9669a3d7ecbe313f745923700b41a9bd8d60eae7
  next root   sha256:f82c7e756fc6395a1f5c629a0eb87e682aa367dd7ac96b41ff9351f7229f13a0
  applied     3 accepted proposal(s)

  households       node_created
  waittime         node_created
  counties         node_created
```

---

## Step 1 — Propose. Nothing moves.

```bash
cat > households-v2.json <<'JSON'
{"text":"The program served 11240 households in 2022.",
 "quantities":[{"coefficient":11240,"scale":0,"unit":"households"}],
 "temporal_scope":{"from":"2022-01-01","until":"2023-01-01"},
 "modality":"is","subject":"program","spatial_scope":["Delta region"]}
JSON

wi propose --node households --payload households-v2.json \
   --why "the agency republished its 2022 count after deduplication" --actor antonio
```

```
PROPOSED on main

  9e2a3e66-50e1-5112-b275-a528da9dfddd
    node      households
    delta     quantity_changed
    requires  claim.accept.quantity_change
    bound to  sha256:9a7dc2d8bb967c83970fa967d142c51adb0da4b99c5ef0abbbd4c63c75c0ed42

Nothing has changed on main. A proposal is not an edit — run
`wi simulate` to see what accepting it would do.
```

Three fields are doing the work.

`delta` is `quantity_changed`. That was computed by comparing typed state, not
characters. The tool did not conclude *a number changed* because digits moved in
a string — it compared the `quantities` array of two states.

`requires` is `claim.accept.quantity_change`, and it is narrower than the
`claim.accept` grant issued in the setup. The capability follows from the delta.
A wording fix and a figure correction can land in the same sentence and require
different authority.

`bound to` is the digest of the state this proposal was written against. It is
what makes the approval answerable later: when the target moves, the proposal
does not follow it.

---

## Step 2 — Simulate. Still nothing moves.

```bash
wi simulate --actor antonio
```

```
SIMULATION ONLY — main is unchanged

Semantic change
  households
    class   quantity_changed
    proof   invalidates: quantity_changed

Authority required
  households                               claim.accept.quantity_change  [held]

Impact
     1 node(s) directly changed
     0 node(s) become stale
     0 node(s) stale through an invalidated proof

Minimum safe repair frontier
  1. reverify           households
     delta class quantity_changed does not carry a prior proof forward

  ordering: lexicographic: human_reviews > deterministic_runs > judgment_calls > external_dependencies > changed_renderings

Provably unaffected
     2 of 3 node(s) on main

candidate root  sha256:be8d16b079973bf2ff14da735df70d2d17560400cd3a3ef47977ec5cd844093e
Nothing was written. This root exists only to be compared.
```

### The provably-unaffected count is the load-bearing line

**Provably unaffected: 2 of 3.** Not *reverify everything*. Not *3 warnings*.
Two named nodes are untouched, and the count carries a denominator so the claim
can be checked.

The word `provably` is not decoration. A node lands in that block only because
the dependency traversal did not reach it — a fact about recorded edges. A node
whose analysis was skipped, or whose adapter does not run on this surface, does
**not** appear here. It appears under the stale counts with its reason. An
unavailable analysis never becomes a clean bill of health.

This is what keeps the mechanism switched on. A report that answers every
question with a wall of red teaches one lesson quickly: the wall is mostly
irrelevant, reading it is a waste of time. The rational response is to stop
reading, and the first thing lost is the finding that mattered. A counterfactual
that only enumerates harm is also an argument against changing anything, which is
not a neutral tool — it would be trusted often enough to be believed and wrong
exactly when a change was overdue.

### The repair frontier says what to fix, and it is one thing

```
  1. reverify           households
```

One action. The narrative does not need re-reading. The other two claims do not
need re-checking. `waittime` and `counties` do not depend on the household count,
and that is not an assumption — it is the absence of an edge.

The ordering line matters when the frontier is longer than one item. Costs are
compared lexicographically and never summed, because a human review and a
deterministic re-run are not commensurable and any single blended number would
have to pretend they are.

---

## Step 3 — Check that the simulation really wrote nothing

```bash
wi log --limit 1 --json | python3 -c "import json,sys;print(json.load(sys.stdin)['commits'][0]['root'])"
```

```
sha256:f82c7e756fc6395a1f5c629a0eb87e682aa367dd7ac96b41ff9351f7229f13a0
```

That is the root from the baseline commit, unchanged, read back after the
simulation ran. The candidate root and the live root are different values,
which is exactly right: one describes a state that exists and the other
describes one that does not.

---

## Step 4 — Decide, then commit

```bash
wi decide 9e2a3e66-50e1-5112-b275-a528da9dfddd --accept --actor antonio
```

```
DECISION ACCEPTED
  proposal   9e2a3e66-50e1-5112-b275-a528da9dfddd
  bound to   sha256:9a7dc2d8bb967c83970fa967d142c51adb0da4b99c5ef0abbbd4c63c75c0ed42
  actor      antonio
  grant      e322307b-57f3-5158-8108-67c315933eb2 (claim.accept.quantity_change)

Accepted is a decision, not an application. Run `wi commit`
to apply every accepted proposal as one transaction.
```

```bash
wi commit -m "agency correction: 11,240 households" --actor antonio
```

```
COMMIT 137fe801664b
  branch      main
  prior root  sha256:f82c7e756fc6395a1f5c629a0eb87e682aa367dd7ac96b41ff9351f7229f13a0
  next root   sha256:be8d16b079973bf2ff14da735df70d2d17560400cd3a3ef47977ec5cd844093e
  applied     1 accepted proposal(s)

  households       quantity_changed
```

---

## The candidate root equals the commit root

Put the two lines next to each other:

```
simulate  candidate root  sha256:be8d16b079973bf2ff14da735df70d2d17560400cd3a3ef47977ec5cd844093e
commit    next root       sha256:be8d16b079973bf2ff14da735df70d2d17560400cd3a3ef47977ec5cd844093e
```

Identical. The simulation did not describe the change — it computed the exact
graph the commit would produce, and then threw it away.

**A simulation that produces a different root than the commit is not a preview.
It is a guess with formatting.** The distinction is normally impossible for a
reader to test, which is why this one is printed: the equality is checkable
rather than promised, and checking it costs one comparison.

### What you will and will not reproduce

Run this whole file on your own machine and the invariant holds — the candidate
root will equal the commit root. Re-running the setup in a second workspace on
the same machine confirmed it a second time, with a different pair of values.

The **values** will not match the ones above. A node state carries the instant
this workspace came to know it, so two workspaces built from identical payloads
produce different roots. What is stable is content addressing:

```bash
wi canon households-v2.json --json | python3 -c "import json,sys;print(json.load(sys.stdin)['state_digest_v6'])"
```

```
sha256:f9bf9ff11b0e38e9a837a0d0c10d421f09fcf0ce4acc7199aaa6441b782ed879
```

That digest is the same on any machine for that payload, which is what makes
staleness mean something. Do not treat the roots in this file as expected values.
Treat the equality between them as the assertion.

---

## Step 5 — Ask the sentence how it got here

```bash
wi why households
```

```
WHY

  The program served 11240 households in 2022.

NODE
  logical id  households
  state       sha256:f03060983186e7eb2599fd85891854c164a18b1e42655a752801a6901ba7252b
  type        meaning.claim_atom
  realm       external_fact

BASIS
  human_declared
      actor: antonio

TIME
  valid       2022-01-01 -> 2023-01-01
  known from  2026-08-08T01:42:34

INTRODUCED BY
  commit 137fe801664b  agency correction: 11,240 households
  actor  antonio at 2026-08-08T01:42:41
  delta  quantity_changed

AUTHORIZED BY
  antonio decided accepted
  under grant e322307b-57f3-5158-8108-67c315933eb2 (claim.accept.quantity_change)
  bound to state sha256:9a7dc2d8bb967c83970fa967d142c51adb0da4b99c5ef0abbbd4c63c75c0ed42
```

`BASIS` reads `human_declared`, not `verified`. A person asserted this figure.
Nothing has yet compared it to an ingested source, and the tool will not use the
stronger word until something has. The two clocks are on the record separately:
the claim held in calendar 2022, and this workspace has known it since 2026.

---

## What the author does differently

Without simulation, the response to a moved figure is to re-read the document.
The cost is unbounded, so it is deferred, and deferred often enough that the
discipline is quietly abandoned — not deliberately, but once, under deadline,
when the cost of compliance was discovered too late to plan around.

With it, the sequence is: propose, simulate, read one number, repair one node,
commit.

**The change is not that the tool found the damage. v5 could already do that.
The change is that it found it while the decision was still a decision.**

---

## What this example does not show

- **Nothing here is verified against a source.** No document was ingested and no
  anchor was bound, so every claim is `human_declared`. Anchoring is the v5 layer
  and is unchanged: `wi ingest`, `wi atomize`, `wi anchor`.
- **The repair frontier has one item** because the fixture has one dependency
  edge. On a real manuscript this block is where the cost actually appears.
- **No rendering was built.** Law M says a `.docx` or a deck is a build from a
  graph root; the compiler backends that would produce one are specified and do
  not ship in 6.0.0.

---

## Pattern to reuse

```bash
wi propose --node NODE --payload NEW.json --why "REASON" --actor YOU
wi simulate --actor YOU          # read: provably unaffected, and the frontier
wi decide PROPOSAL_ID --accept --actor YOU
wi commit -m "MESSAGE" --actor YOU
# then compare: simulate's candidate root == commit's next root
```

Next: [`02-the-merge-that-refused.md`](02-the-merge-that-refused.md) — what happens
when two people run this sequence at the same time and disagree.
