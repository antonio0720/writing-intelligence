# v9 Example 2: One Anchor Does Not Carry Three Claims

**Synthetic.** The author, the notes, the draft and the "statistics" below were invented for this page and make no claim about any real hobby, club or year. v9 is a proposal (PR #8), not a release.

## Situation

Draft, three sentences. The author's notes support only the first:

```
I rebuilt the model bridge twice in March because the first glue joint sheared.
Hobbyists abandon the craft within a year in 60 percent of cases.
The club's membership doubled in 2023.
```

The dossier anchors the first sentence to the note (`notes.txt`, evidence `e1`). Venue is human-only, the declared origin is human-authored, and the log shows only `human_original`, so the venue contract is satisfied. The open question is whether the draft's claims are sourced.

## Command and result

```
$ python3 scripts/wi-authorship.py audit --input examples/v9/claim-coverage/dossier.json
```

Excerpt of the real output:

```
  "claim_coverage": [
    { "claim_id": "c0001", "anchored": true,  "support": "anchor_resolved_unadjudicated" },
    { "claim_id": "c0002", "anchored": false, "support": "needs_source" },
    { "claim_id": "c0003", "anchored": false, "support": "needs_source" } ],
  "findings": [
    { "code": "CLAIM_UNANCHORED", "level": "hold",
      "message": "Draft claim has no anchored evidence: 'Hobbyists abandon the craft within a year in 60 percent of cases.'" },
    { "code": "CLAIM_UNANCHORED", "level": "hold",
      "message": "Draft claim has no anchored evidence: \"The club's membership doubled in 2023.\"" },
    { "code": "VOICE_BASELINE_INSUFFICIENT", "level": "advisory", ... } ],
  "status": "HOLD"
```

Exit status: **3**. The classifier in `scripts/wi.py` found three consequential claims; one supplied anchor covers one of them.

## Two honest ways forward

1. **Supply the source.** The author finds where the 60 percent and the doubling come from, adds those sources and anchors to the dossier. If no source exists, the figures stay out. The checker never invents a source and never softens a number to make it pass.
2. **Cut the claims.** `draft-cut.txt` keeps only the supported sentence, with its own pinned digest in `dossier-cut.json`:

```
$ python3 scripts/wi-authorship.py audit --input examples/v9/claim-coverage/dossier-cut.json
REVIEW: limited checks passed. This is not permission to publish or send.
```

Exit status: **0**, `status: REVIEW`, `release_authorized: false`.

## The next gate is still closed

`REVIEW` is not an approval. Running the second subcommand on the same dossier:

```
$ python3 scripts/wi-authorship.py release --input examples/v9/claim-coverage/dossier-cut.json --authority-store ~/wi-authority
```

returns `HOLD` (exit **3**) with, among others, `DECISION_REQUIRED` and `AUTHORITY_REQUIRED`: no person has recorded a decision bound to this exact draft digest, and the decision names no v6 grant store to check. Release authority is never read from the dossier: the deciding person needs a `release.approve` grant for this venue in a v6 workspace (`scripts/wi.py authority issue`). Even when both are supplied, `RELEASE_ELIGIBLE` means the gates agree; it is not proof the text was written by a person, and the tool still sends nothing.

## Limits of this example

- An excerpt that appears in the notes is a **text anchor**, not proof the event happened or that the sentence follows from it. Semantic entailment is not implemented.
- Sentences the v4 classifier labels rhetoric are not checked for sourcing.
- The checker reads local files only and does not look anything up.

Back to [`README.md`](README.md).
