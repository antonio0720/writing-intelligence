# Writing Intelligence v9 — Owner Handoff Reference Kernel

**Project owner and designated author:** Antonio T. Smith Jr. — Density6 LLC

This is an **isolated experimental reference implementation**, not the canonical Writing Intelligence v9 release or a replacement for `scripts/wi.py`.

## Quick start

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 wi9_core.py preflight --root examples --input research_case.json
python3 wi9_core.py plan --root examples --input research_case.json
python3 wi9_core.py diagnose --root examples --input sample_essay.txt
```

The `preflight` and `voice` tools check declared provenance and specific text evidence; they do **not** authenticate a writer or establish the truth of a statement. The `diagnose` tool is editorial linting, not AI detection. `benchmark` requires actual independent scored cases and does not ship invented results. All commands are offline and standard-library-only. On systems without POSIX `dir_fd` and `O_NOFOLLOW`, the file reader fails closed.

## Integration warning

Do not drop these files into the released v8 package. Port through v9 compatibility adapters, protect `wi.py` as the canonical source of claims and release state, and run all v4–v9 regressions before any version change. Hold all external submission transitions until actual owner approval and venue compliance.

**One authorship checker.** In this repository the canonical v9 authorship and venue checker is `scripts/wi-authorship.py` (`audit`, `release`), which carries the P0 repairs listed in `references/v9/defects.md`, including claim coverage from the v4 classifier. `wi9_core.py preflight` is kept as the reference specimen it was delivered as; when the two disagree, `scripts/wi-authorship.py` is the answer and the difference is a defect to record, not a second policy.

**Changes since the delivered ZIP** (SHA-256 `610453b2…724b8`): `wi9_phrase_review.py` now requires `reviewed_at` to be offset-aware ISO 8601 and not in the future (D-15), with three new tests; one test fixture time moved into the past so it is not refused by that check. Everything else is byte-identical to the delivery.

## Composition contract

`wi9_composition.py` specifies source-card constrained model requests and validates candidate paragraph evidence IDs and exact direct quotations. This is a **model-neutral I/O contract**. No model runtime or automatic rewriting service is bundled. `prepare_request()` refuses to create prose-generation requests for `human_only` venues. For authorized venues, `inspect_candidate()` can only reach `DRAFT_REVIEW_REQUIRED`, never a release or send state. A future model provider can implement the request schema without being trusted with publication authority.

## Editorial hot-phrase library (334 proposed rule candidates)

The `rules/v9_hotphrases.json` catalog includes **321 literal and 13 regex expressions**, including "that matters," "here's why," "the reality is," "it's worth noting," and stereotyped contrast patterns. A match asks an *editorial question*; it never declares a passage AI-generated and never triggers an automatic rewrite.

```bash
python3 wi9_hotphrases.py scan --input examples/sample_essay.txt --format text
python3 wi9_hotphrases.py scan --input examples/sample_essay.txt --format json > /tmp/wi9_scan.json
python3 wi9_hotphrases.py scan --input examples/sample_essay.txt --include-quotes --format text
```

Reports carry original code-point offsets and 1-based lines/columns, a SHA-256 of the document and rule pack, repeated-rule counts, and a truncation flag; a long file is scanned in chunks (`chunks`, `complete`) rather than cut off. Quotes, URLs, code spans and code fences are masked by default. Masking is heuristic and legitimate phrases can be flagged: the human author or editor must decide whether to retain them.

## Human editorial-review ledger

`wi9_phrase_review.py` checks reviewer decisions against the exact unchanged document and rule pack: each names a finding, its original offset and excerpt, its disposition and rationale, and the review time. Since 2026-10-28 a decision counts only when it comes from the review ledger (`wi9_ledger.py`), recorded under the reviewer's own v6 grant; a typed reviewer name on its own holds `REVIEWER_UNBOUND`. A valid review means *reviewed*, never publication-approved, and a grant shows who was authorized, not who typed the decision. The bundled `examples/sample_hotphrases.review.json` carries a typed name and therefore shows that HOLD:

```bash
python3 wi9_hotphrases.py scan --input examples/sample_hotphrases.txt \
  --format json > /tmp/sample_hotphrases.scan.json
python3 wi9_phrase_review.py --input examples/sample_hotphrases.txt \
  --report /tmp/sample_hotphrases.scan.json \
  --decisions examples/sample_hotphrases.review.json        # HOLD: REVIEWER_UNBOUND:0
python3 wi9_phrase_review.py --input examples/sample_hotphrases.txt \
  --report /tmp/sample_hotphrases.scan.json \
  --ledger ~/wi9-private/ledger --authority-store ~/wi-authority   # REVIEW once you recorded each finding
```

## Per-writer tools added after the ZIP (2026-10-28)

Every one works on the writer's own material on their own machine and is reachable as `wi authorship <tool>` from the repository root.

| Module | Tool | What |
|---|---|---|
| `wi9_fs.py` | — | shared private-file rules: POSIX only (`PLATFORM_UNSUPPORTED` elsewhere), 0700 folders, never inside a git working tree, 0600 files, `O_NOFOLLOW`, `O_EXCL` for records that must not be overwritten |
| `wi9_vault.py` | `vault` | WI9-02 firsthand vault: consented, labelled items; redaction and withdrawal delete bytes; digest-only event log; `check` holds unsourced first-person claims |
| `wi9_ledger.py` | `ledger` | review decisions recorded under the reviewer's v6 grant; append-only, hash-chained, explicit supersession; grants re-read then and now |
| `wi9_meaning.py` | `meaning` | WI9-04 thought inventory, lexical meaning diff, grant-bound review with vault anchoring for new first-person sentences |
| `wi9_structure.py` | `structure` | WI9-05C repeated openings, hollow contrasts, template paragraphs, triads, restatement |
| `wi9_core.py` | `voice`, `voice-review`, `voice-compare` | WI9-05F measures (qualifiers, intensifiers, disagreement, concrete detail, argument strategy), held-out stability, drift against the writer's own baseline, near-copy refusal |
| `wi9_hotphrases.py` | `scan` | `scan_document`: chunked scanning to 20 million characters with whole-document offsets |
| `wi9_provider.py` | `compose` | bring-your-own-model connector, gated by `wi9_composition.py`; best result `DRAFT_REVIEW_REQUIRED` |

Use `python3 -m unittest discover -s tests -p 'test_*.py' -q` for the local unit tests (**190** at 2026-10-28; 84 at the ZIP plus D-15). They are synthetic-fixture tests, not a blinded writing-quality study and not evidence of any writer's experience. The complete engineering handoff is [`references/v9/ENGINEERING_HANDOFF.md`](../../references/v9/ENGINEERING_HANDOFF.md).
