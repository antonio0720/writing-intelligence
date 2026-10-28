# Example 3 — a revision that reads better and says something else

**Everything here is synthetic**, written for this page. The writer, the harbour model and the workshop do not exist.

A writer's paragraph and a smoother revision of it ([`meaning/original.txt`](meaning/original.txt), [`meaning/revised.txt`](meaning/revised.txt)):

> **Original.** I think the harbour model took about eleven evenings, mostly because the card kept curling. Although the paint went on fast, the roof still warps when the room is damp. Next spring I will build a second harbour with a working crane.
>
> **Revised.** The harbour model took eleven evenings, because the glue was slow to set. The roof still warps when the room is damp. I built a second harbour with a working crane, which doubled the visitors to my workshop.

The revision is tidier. It also changes six things the writer said.

```bash
python3 scripts/wi.py authorship meaning diff \
  --original examples/v9/meaning/original.txt --candidate examples/v9/meaning/revised.txt
```

Exit **3**: deltas found. The report lists each one with a question for the writer (output abridged to id, kind and detail):

```text
cabfb4db2a19caca ESTIMATE_TO_MEASURED  the approximation is gone          "about eleven" became "eleven"
4367c15845b8e1ad CAUSE_CHANGED         the reason after the causal word differs   card curling -> glue slow to set
4fa43cc7c0f809cd UNCERTAINTY_REMOVED   the hedge is gone                  "I think" is gone
3254af0041f2b0b9 CONCESSION_DROPPED    the concession word is gone        "Although the paint went on fast" is gone
c9659129e34ced5b PLANNED_TO_COMPLETED  the plan marker is gone            "Next spring I will build" became "I built"
1e4698e659ecc999 OUTCOME_ADDED         a result appears: doubled          an outcome nobody stated
```

The first needs a grant covering `claim.accept.quantity_change`; the rest need `claim.accept`.

## What the writer does next

The writer answers each question, in their own ledger, under their own grant. Here they would likely **reject** the plan written up as done and the invented outcome (they have not built the second harbour, and nothing measured the visitors), and **reject** the new cause (the card curled; the glue was fine). They might **accept** dropping the concession if they agree it added nothing.

```bash
python3 scripts/wi.py authorship ledger record --ledger ~/wi9-private/ledger --authority-store ~/wi-authority \
  --actor writer --kind meaning --target <pair_sha256 from the report> --item c9659129e34ced5b \
  --decision reject --rationale "The second harbour is still a plan."
python3 scripts/wi.py authorship meaning review \
  --original examples/v9/meaning/original.txt --candidate examples/v9/meaning/revised.txt \
  --ledger ~/wi9-private/ledger --authority-store ~/wi-authority
```

`review` holds while any delta is undecided (`DELTA_UNDECIDED`) or rejected (`DELTA_REJECTED`). A rejected delta means the revision must change, not the writer's text. Had the revision added a new first-person sentence, accepting it would also need an anchored claim in the writer's vault (`DELTA_NEEDS_SOURCE` otherwise).

## What this does not show

- The diff is **lexical**. It catches where meaning most often moves — numbers, dates, plan and hedge words, negation, stance and cause words, concessions, quotations, first person — and a paraphrase that changes meaning without touching any of them can pass it.
- Accepting a delta is the writer's decision, not a check that the new wording is true.
- No detector is run, and nothing here says who wrote either version.
