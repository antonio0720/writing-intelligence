# v9 Example 1: A Human-Only Venue Holds an Assisted Draft

**Synthetic.** Every name, venue and sentence below was invented for this page. Released in Writing Intelligence 9.0.0.

## Situation

A reporter desk (invented: "Synthetic Reporter Desk") accepts pitches only from people who wrote them. The author has notes of a real-in-the-story event — rebuilding a model bridge — and a draft. The draft is one sentence, copied from the notes. But the dossier's own contribution log says an assistant did a substantive rewrite:

```json
"document": { "origin": "ai_assisted", "venue_policy": "human_only", "intended_use": "submission", ... },
"venue_contract": { "allowed_assistance": ["mechanical_proofread"], "allowed_operations": ["research", "submit"] },
"contribution_log": [ { "kind": "human_original" }, { "kind": "ai_substantive_rewrite" } ]
```

The venue lists mechanical proofreading as permitted. A substantive rewrite is not on the list, and for a human-only venue an unlisted kind of assistance is treated as not allowed.

## Command and result

```
$ python3 scripts/wi-authorship.py audit --input examples/v9/venue-hold/dossier.json
```

Excerpt of the real output (full JSON is longer):

```
  "declaration_status": "self_reported",
  "decision_scope": "limited_checks",
  "declared_origin": "ai_assisted",
  "findings": [
    { "code": "HUMAN_ONLY_CONFLICT",
      "level": "hold",
      "message": "Human-only submissions cannot package AI-generated or AI-assisted authorship." },
    { "code": "SUBSTANTIVE_AI_CONTRIBUTION",
      "level": "hold",
      "message": "A declared AI prose contribution conflicts with human-only venue rules.",
      "target": "contribution_log[1]" },
    { "code": "VOICE_BASELINE_INSUFFICIENT", "level": "advisory", ... }
  ],
  "release_authorized": false,
  "status": "HOLD"
```

Exit status: **3**.

## What happened, and what did not

- The sentence is fully sourced: claim coverage found one claim and it overlaps the anchored note. A fully anchored draft is still held, because the question here was the venue contract, not the evidence.
- Nothing was rewritten, scored or sent. The checker has no send step and transmits nothing.
- There was no detector in this run. Had one been run and returned a favorable number, the result would be the same: the hold comes from the declared contribution log against the venue's rule, and a detector percentage is not a provenance record.
- The checker only compares what the dossier declares. If the log were changed to say nothing about an assistant, the checker could not know — a limitation of any declaration check, which every report states (`declaration_status: self_reported`). Declare what happened.

## What to do instead

The permitted route for this venue is **research only**: the author uses the notes to prepare source material, interview questions or a list of facts to confirm, then writes the pitch themselves. The v9 composition contract in `prototypes/wi9/wi9_composition.py` refuses to draft for a `human_only` venue for the same reason. The author decides what is true of their own history; this repository can record the declaration and refuse the combination.

Next: [`02-claim-coverage.md`](02-claim-coverage.md).
