# v9 Examples — Authorship Provenance (PROPOSED, preview)

**Status:** v9 is a proposal on PR #8, not a release; v8.0.0 is the published version. These two worked examples exercise `scripts/wi-authorship.py`, an authorship-claim **declaration checker**. It tests whether declarations are complete and consistent. It does not verify who wrote anything.

**Everything here is synthetic.** The author, the "Synthetic Reporter Desk" venue, the notes and the drafts were written for this teaching page. No real person, publication, study or statistic appears. The terminal output was produced by running the commands below against the files in this folder on 2026-10-27; the document digests are a record of those files and you will get the same values only if the files are unchanged.

- [`01-human-only-venue-hold.md`](01-human-only-venue-hold.md) — a venue that accepts only human-written pitches meets a draft whose own log says an assistant rewrote it. The checker holds (exit 3). Nothing is sent and nothing is rewritten.
- [`02-claim-coverage.md`](02-claim-coverage.md) — a draft with one sourced sentence and two unsourced ones. One safe anchor does not carry the other two. Cutting them yields REVIEW (exit 0), which is still not permission to send.

Fixture files (each example folder is self-contained):

| Folder | Files |
|---|---|
| `venue-hold/` | `dossier.json`, `draft.txt`, `notes.txt` |
| `claim-coverage/` | `dossier.json`, `draft.txt`, `notes.txt`, `dossier-cut.json`, `draft-cut.txt` |

## What these examples do not show

- No authorship is authenticated. Every report carries `declaration_status: self_reported`.
- `REVIEW` and `RELEASE_ELIGIBLE` are limited-check results, not a claim of human authorship and not publication approval.
- No detector is run and no detector score is used or targeted. A detector percentage is not a provenance record.
- No quality score, benchmark result or editor validation exists for v9. The 60-case editorial benchmark (WI9-07) has not run.

Doctrine: [`../../references/v9/README.md`](../../references/v9/README.md) · defect register: [`../../references/v9/defects.md`](../../references/v9/defects.md) · schema: [`../../schemas/v9/authorship-dossier.schema.json`](../../schemas/v9/authorship-dossier.schema.json).

## Author

Antonio T. Smith Jr. / Density6 LLC
