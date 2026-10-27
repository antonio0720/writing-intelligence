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

Reports carry original code-point offsets and 1-based lines/columns, a SHA-256 of the document and rule pack, repeated-rule counts, and a truncation flag. Quotes, URLs, code spans and code fences are masked by default. Masking is heuristic and legitimate phrases can be flagged: the human author or editor must decide whether to retain them.

## Human editorial-review ledger

`wi9_phrase_review.py` checks a reviewer decision against the exact unchanged document and rule pack. A decision must name a finding, its original offset and excerpt, its disposition and rationale, the declared reviewer, and the review date. A valid decision means *reviewed*, never publication-approved. The reader/reviewer name in the JSON is a self-declaration, not independent identity verification.

```bash
python3 wi9_hotphrases.py scan --input examples/sample_hotphrases.txt \
  --format json > /tmp/sample_hotphrases.scan.json
python3 wi9_phrase_review.py --input examples/sample_hotphrases.txt \
  --report /tmp/sample_hotphrases.scan.json \
  --decisions examples/sample_hotphrases.review.json
```

Use `python3 -m unittest discover -s tests -p 'test_*.py' -q` for the **84** observed passing local unit tests (81 delivered + 3 added for D-15). These tests are not a blinded writing-quality study. The complete engineering handoff is included as a separate Markdown artifact outside this folder.
