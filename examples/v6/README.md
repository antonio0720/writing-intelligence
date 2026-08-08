# v6 Examples — The Sovereign Meaning Runtime

Four walkthroughs of the v6 layer. Each one follows a single decision from the
moment somebody wants to make it to the moment a stranger can check it.

## Index

- [`01-simulate-before-you-edit.md`](01-simulate-before-you-edit.md) — a grant figure moves. Ask what that would cost before the change exists, then repair one node instead of the manuscript.
- [`02-the-merge-that-refused.md`](02-the-merge-that-refused.md) — 11,800 against 12,400. The merge stops, exits 2, keeps both numbers, and never writes the average.
- [`03-authority-that-expires.md`](03-authority-that-expires.md) — a reviewer helps for two weeks. The same decision succeeds inside the window and is refused after it, with nobody revoking anything.
- [`04-a-capsule-a-stranger-verifies.md`](04-a-capsule-a-stranger-verifies.md) — a funder verifies one claim, offline, from two files, without receiving the workspace.

## What makes a v6 example different

The five examples in [`../`](../) and the ten in [`../v3/`](../v3/README.md) show a
better paragraph coming out. A weak draft goes in, the passes run, and the
output is more specific, better built and easier to read. The unit of work is
prose and the evidence is the prose itself: you read the after and you can see it.

These show a **decision being made safely**. The output of a v6 example is
usually not a paragraph at all. It is a refusal, a cost estimate for a change
that has not happened, a conflict that was preserved instead of resolved, or a
file that proves one claim and declares what it withheld.

That changes what you are looking at while you read:

| v1–v5 example | v6 example |
|---|---|
| Before and after text | Before and after **state**, and often no text changes at all |
| The improvement is visible in the prose | The improvement is that something did **not** happen |
| Success is a higher score | Success is frequently a non-zero exit code |
| You judge the result by reading it | You judge the result by re-running the check |

The last row is the important one. A rewrite is assessed by a reader. A governed
transition is assessed by recomputation — which is why every transcript in these
four files was produced by running the tool rather than by describing it, and why
each file says which parts of its output you will see change on your own machine.

## How these were recorded

Every terminal block in these four files was recorded on **2026-08-08** against
`wi 6.0.0` on Python 3.11.15, in scratch workspaces created for the purpose. Each
file states its exact setup so you can rebuild it.

Two things about reproducing them:

**Content digests are stable.** `wi canon` over the same payload returns the same
`state_digest_v6` on any machine, which is what makes staleness meaningful at all.

**Graph roots and commit ids are not.** A node's state carries the instant this
workspace came to know it, so rebuilding the same workspace tomorrow produces
different roots. The digests printed in these files are a record of one run and
not a value to match. What holds across runs is the **relationship** between
them — and where an example rests on such a relationship, it says so and shows
the comparison rather than asking you to trust the number.

## Reading order

Read `01` first. Simulation is the command that changes how the work feels, and
the other three are easier once you have seen a change costed before it existed.

Doctrine behind each one: [`COUNTERFACTUAL_SIMULATION`](../../references/v6/COUNTERFACTUAL_SIMULATION.md) ·
[`MERGE_PROTOCOL`](../../references/v6/MERGE_PROTOCOL.md) ·
[`AUTHORITY_MODEL`](../../references/v6/AUTHORITY_MODEL.md) ·
[`PROOF_CAPSULES`](../../references/v6/PROOF_CAPSULES.md)

## Author

Antonio T. Smith Jr. / Density6 LLC
