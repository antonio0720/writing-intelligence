# Genre Pack — Technical Documentation

**v3.0 Domain Pack Schema**

## Purpose

Produce developer-facing documentation a competent engineer can follow without asking the author a question.

## When to Use

- API documentation
- SDK reference
- Architecture guides
- Runbooks / SRE playbooks
- Tutorials / quickstarts
- README files for libraries and CLIs
- Migration guides
- Troubleshooting docs
- Configuration reference

## When Not to Use

- Marketing copy for a technical product (use `sales.md` + `landing_page` arena)
- Internal engineering memos (use `memo` arena + `strategy.md`)
- Whitepapers (use `academic.md` + `pitch_deck.md`)

## Audience Model

- An engineer encountering this system for the first time
- An engineer who has used it before but forgot specifics
- An engineer debugging a failure at 2 AM

## Required Evidence

- A working code example for every documented function
- A failure-mode example for every error class
- Version numbers (system, library, API)
- Required permissions / credentials
- Expected output for every command
- Links to source code where applicable

## Forbidden Claims

- "Easy" / "simple" / "intuitive" (judgments, not facts)
- "Just" / "merely" / "obviously" (condescending shortcuts)
- "Should work" without test evidence
- Code examples that don't actually run
- Outdated API references presented as current

## Voice Weighting

- Clarity: **30** (highest)
- Specificity: **20**
- Evidence: **15** (working examples)
- Compression: **15**
- Warmth: **10** (patient, not condescending)
- Authority posture: **50-60** (confident, instructional, neutral)

## Structure Templates

### API Endpoint Doc

1. **Endpoint** (method + path)
2. **What it does** (one sentence)
3. **Authentication** (required tokens / scopes)
4. **Request** (parameters, body, headers)
5. **Response** (status codes, shape, examples)
6. **Errors** (every error case with cause and fix)
7. **Example** (working curl + working code in 1-2 languages)
8. **Rate limits** / quotas / pricing
9. **Related** (links to companion endpoints)

### Quickstart

1. **What you'll build** (1 sentence + screenshot if applicable)
2. **Prerequisites** (versions, accounts, keys)
3. **Steps** (numbered, each ends with verification)
4. **What just happened** (1 paragraph)
5. **Next steps**
6. **Troubleshooting** (common failures with fixes)

### Runbook

1. **What this runbook is for** (1 sentence)
2. **Symptoms** (what triggered this)
3. **Immediate actions** (numbered, time-bounded)
4. **Diagnostic steps** (numbered, with expected output)
5. **Resolution paths** (branched by diagnostic)
6. **Escalation** (when to page, whom)
7. **Postmortem template**

## Scoring Adjustments

| Metric | Weight |
|---|---|
| Code examples run | 25 |
| Error documentation completeness | 20 |
| Reproducibility | 15 |
| Scannability (headings, code blocks, tables) | 15 |
| Voice neutrality (no condescension) | 15 |
| Version accuracy | 10 |

## Failure Modes

- Code example that doesn't run → automatic fail
- "Just do X" appearing in any sentence → flagged
- Missing error documentation → score capped
- No working language-specific example → score capped
- Outdated version references → flagged

## Before/After Example

**Before**:

> Just call our authentication endpoint with your token. It's easy — just pass it in the header and you're all set!

**After**:

> POST `/v1/auth/verify`
>
> **Headers**:
> - `Authorization: Bearer <token>` — required. Obtain from the dashboard under *Settings → API Keys*.
>
> **Response (200)**:
> ```json
> {"valid": true, "expires_at": "2026-12-31T23:59:59Z"}
> ```
>
> **Errors**:
> - `401` — token invalid or revoked. Issue a new token.
> - `429` — rate limit exceeded (60 req/min). Retry after `Retry-After` header.

## Delivery Formats

- Markdown (`.md`) for repository docs
- HTML with anchors for site docs
- OpenAPI / JSON schema for machine-readable API docs
- PDF for offline reference

## Schema Hooks

- `intake_contract.arena: sop`
- `corpus_map`: must reference live code / API behavior, not memory of prior versions
- `epistemic_ledger`: every code example is `verified` or marked `assumed`

## Benchmark Cases

`TECHDOC-01` through `TECHDOC-05` in `benchmarks/cases/technical_documentation.md`.

## Stack Combinations

- + `academic.md`: technical whitepapers
- + `email.md`: developer-facing release announcements
- + `government_brief.md`: agency technical guidance
