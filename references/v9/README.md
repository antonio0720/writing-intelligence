# Writing Intelligence v9 — Authentic Voice & Authorship Provenance (PROPOSAL)

**Status:** Experimental proposal, **not** the published v9 release. This branch does not change the v8 release, `SKILL.md`, or the canonical v4–v8 runtime. **Project author:** Antonio T. Smith Jr. — Density6 LLC. **Date:** 2026-10-27.

**Full editorial protocol:** [`EDITORIAL_PROTOCOL.md`](EDITORIAL_PROTOCOL.md). **Blinded quality benchmark:** [`QUALITY_BENCHMARK.md`](QUALITY_BENCHMARK.md). **Wave states:** [`WAVES.yaml`](WAVES.yaml).

## Mission

Enable authors and editors to produce distinctive, credible, source-grounded writing while preserving **who actually wrote it**. Do **not** promise prose that is "100% human" when a model wrote it, a 0% AI detector score, or eligibility for a human-only venue based on surface style. A detector result is a noisy diagnostic, not a provenance record.

The trigger was an AI-generated three-part essay about miniature worlds: the content answered the questions but relied on hypothetical models instead of the author's confirmed experiences, evenly structured arguments, mirror-image contrasts, and a polished abstraction layer. A commercial detector returned "68% possible AI." That number is reported as a user observation, **not** independently validated authorship probability or baseline for optimizing a detector.

## v9 first principles — additions to, not replacements for, the 18 laws

- **WI9-A SOURCE BEFORE STYLE:** Author-supplied memories, notes, transcripts, drafts and source documents precede polishing. No invented "I did" scenes.
- **WI9-B VOICE IS EVIDENCE:** An author's voice is measured from consented authentic samples and reviewed by that author. Style stats alone cannot authenticate origin.
- **WI9-C CONCRETE BEFORE CADENCE:** Identify the actual actor, location/context, decision, friction, consequence and uncertainty where the sources support them. Do not add random sentence lengths or planted typos.
- **WI9-D DISTINCTIVE THOUGHT:** Test whether the paragraph offers an author's specific experience, disagreement, revision, mechanism, or bounded insight. Rewriting a platitude elegantly is insufficient.
- **WI9-E NO BORROWED MEMORY:** Hypothetical scenarios remain labeled hypothetical. A company roadmap does not prove a project was built or an outcome measured.
- **WI9-F AUTHORSHIP IS NOT A SOUND:** `human_authored`, `ai_assisted`, and `ai_generated` are distinct declarations. A voice mimic cannot change them.
- **WI9-G VENUE CONTRACT FIRST:** Human-only rules block AI-written and AI-rewritten submission packages, even if an author manually clicks Send. Research briefs may be created separately.
- **WI9-H DETECTOR HUMILITY:** Never optimize to a vendor score, call its percent a factual authorship fraction, or claim a score guarantees acceptance. Record vendor/version/date as optional diagnostics only.
- **WI9-I TRACEABLE TRANSFORMATION:** Preserve source and every edit; declare whether a change is mechanical proofreading, suggested edit, authored revision or substantive generation.
- **WI9-J REVIEW, DON'T AUTO-PUBLISH:** Source checks do not authenticate a person's identity or mental authorship. Release decisions remain scoped human judgments.

## What exists on this branch

All of it is experimental and reviewable; none of it is a release. The defect register is [`defects.md`](defects.md); the receipts are [`plans/receipts/WI9-00.json`](../../plans/receipts/WI9-00.json) and [`plans/receipts/WI9-P0.json`](../../plans/receipts/WI9-P0.json). The engineering handoff this work follows is [`ENGINEERING_HANDOFF.md`](ENGINEERING_HANDOFF.md). What only the owner can supply — the 60-case benchmark material and reviewers, an independent human reviewer — and the exact commands that run on it: [`OWNER_INTAKE.md`](OWNER_INTAKE.md). Voice samples are not one of them: every writer measures their own voice on their own machine ([`VOICE_BASELINE.md`](VOICE_BASELINE.md)), and none ships with v9.

### `scripts/wi-authorship.py` — authorship-claim declaration checker

This is a **declaration checker, not an authorship verifier**. `audit --input dossier.json` returns `REVIEW` (limited checks passed, exit 0) or `HOLD` (exit 3). `release --input dossier.json` returns `RELEASE_ELIGIBLE` (exit 0) or `HOLD` (exit 3) and transmits nothing. Every report carries `declaration_status: self_reported` and, for `audit`, `release_authorized: false`.

`audit` checks: the root and nested types; bounded, symlink-free reads under the dossier directory (POSIX `O_NOFOLLOW` per component; refuses to run elsewhere); the draft against its pinned `expected_sha256` (required for any submission); unique evidence ids; exact source anchors and pinned source digests; typed `experience_state` (a planned or hypothetical item cannot support a firsthand claim) and `support_status`; draft anchors that resolve uniquely in the draft; **claim coverage** — every consequential claim the v4 classifier in `scripts/wi.py` finds in the draft must overlap an anchored span, so one safe anchor cannot carry three unsourced claims; the contribution log against the declared origin on every venue; and human-only venue rules, where assistance the venue contract does not list is refused.

`release` additionally requires: a person's `review_decision` whose `target_sha256` is the exact draft digest, a v6 grant-store check (`review_decision.authority = {"store": "v6"}`, with the store named by the operator through `--authority-store` and refused if it sits inside the dossier folder, if `.wi` or its database is a symlink, or if it cannot be opened read-only) proving that person holds `release.approve` in scope `release_target:<venue>`, active when they decided and now, by a human subject; a venue contract recording `submit` as open; and an unpassed deadline. A grant declared only in the dossier holds (`AUTHORITY_UNBOUND`). The v6 store's own refusals (`DENIED`, `REVOKED`, `EXPIRED`, `GRANT_SCOPE_EXCEEDED`) come through as `AUTHORITY_*` codes.

Dossier contract: [`schemas/v9/authorship-dossier.schema.json`](../../schemas/v9/authorship-dossier.schema.json) (`wi9-authorship-2`; `wi9-authorship-1` dossiers are still read). `tests/v9/test_schema_parity.py` keeps the schema and the checker on one vocabulary.

Paths resolve relative to the dossier directory. Sources are not sent to a service. It **cannot prove** whether a self-declared human-only manuscript was actually written by a person, and exact excerpt presence is a text anchor, not truth or entailment.

### Per-writer tools (WI9-02, WI9-03, WI9-04, WI9-05C/F, review ledger, model connector)

Every one of these works on the writer's own material, on their own machine. None ships a corpus, none uploads anything, and each is reachable as `wi authorship <tool> ...`.

| Tool | What it does | Refuses with |
|---|---|---|
| `vault` ([`wi9_vault.py`](../../prototypes/wi9/wi9_vault.py)) — WI9-02 | A private 0700 folder of the writer's firsthand material (notes, transcripts, dated drafts, interviews), refused inside any git working tree. Every item carries consent and a label: `observed`, `said_by_author`, `measured`, `sourced`, `inferred`, `hypothetical` or `planned`. `redact` and `withdraw` delete the earlier bytes; the event log keeps digests, never text. `check` holds every first-person claim that has no anchored source. | `CLAIM_NEEDS_SOURCE`, `PLANNED_AS_DONE`, `HYPOTHETICAL_AS_EXPERIENCE`, `EVIDENCE_MODEL_GENERATED`, `QUOTE_NOT_VERBATIM`, `CONFLICTING_ACCOUNTS`, `DATE_CONFLICT`, `EVIDENCE_WITHDRAWN`, `EVIDENCE_STALE`, `VAULT_PROJECT_MISMATCH`, `STORE_INSIDE_REPOSITORY` |
| `meaning` ([`wi9_meaning.py`](../../prototypes/wi9/wi9_meaning.py)) — WI9-04 | A thought inventory of the writer's text and a sentence-by-sentence meaning diff against a revision. Every material change is listed as a delta for the writer to accept or reject: numbers, dates, plans written up as done, estimates read as measured, flipped negation, reversed stance, moved or invented causes and outcomes, dropped hedges and concessions, swapped chronology, altered quotations, dropped claims, new first-person or factual sentences. `review` reaches REVIEW only when every delta was accepted in the ledger under a grant whose capability covers it, and every new first-person fact is anchored in the vault. The comparison is lexical: it finds where meaning often moves, it does not understand it. | `DELTA_UNDECIDED`, `DELTA_REJECTED`, `DELTA_CAPABILITY_INSUFFICIENT`, `DELTA_NEEDS_SOURCE` |
| `ledger` ([`wi9_ledger.py`](../../prototypes/wi9/wi9_ledger.py)) | The review ledger. A decision is recorded only after the operator's v6 grant store shows the person holds the capability, as a human, in scope; the entry carries the grant id. Append-only and hash-chained; a later decision supersedes an earlier one explicitly and the earlier one stays. `verify` re-reads every grant at decision time and now. A typed reviewer name alone holds `REVIEWER_UNBOUND` in `phrase-review`. | `AUTHORITY_DENIED`, `AUTHORITY_NOT_HUMAN`, `AUTHORITY_STORE_UNTRUSTED`, `LEDGER_DECISION_EXISTS`, `LEDGER_CHAIN_BROKEN`, `REVIEWER_UNBOUND` |
| `voice`, `voice-review`, `voice-compare` ([`wi9_core.py`](../../prototypes/wi9/wi9_core.py)) — WI9-03, WI9-05F | Each writer measures their own samples: sentence length and spread, vocabulary range, first person, and how they argue (qualifiers, intensifiers, disagreement, concrete detail, examples, reasons, concessions, questions). A held-out check leaves each sample out in turn; a measure the writer's own samples do not agree on is named as unstable. `voice-compare` places a new text against the baseline and says plainly that matching it proves nothing about who wrote it. | `VOICE_SAMPLE_SHORT`, `VOICE_SAMPLE_COUNT`, `VOICE_GENRE_MIX`, `VOICE_SAMPLES_TOO_SIMILAR`, `VOICE_BASELINE_NOT_READY` |
| `structure` ([`wi9_structure.py`](../../prototypes/wi9/wi9_structure.py)) — WI9-05C | Questions about shape with exact spans: three or more sentences opening the same way, a contrast whose two sides are both abstractions, paragraphs poured into one mould, three-item lists on every page, a sentence that repeats the last. A contrast carrying a number, a date or a named place is left alone. | editorial questions only |
| `scan` (chunked) ([`wi9_hotphrases.py`](../../prototypes/wi9/wi9_hotphrases.py)) | The 334-rule scan now covers a manuscript up to 20 million characters in chunks cut at paragraph breaks outside code and quotations, with global offsets, instead of stopping at 500 findings. A pathological chunk is reported, by range, as incomplete. | `complete: false` with the ranges |
| `compose` ([`wi9_provider.py`](../../prototypes/wi9/wi9_provider.py)) | Bring your own model. The venue policy and evidence gates run first, so a human-only or unknown venue never reaches the model; the writer must consent to the source cards leaving the process. The writer's program runs with no shell, a deadline, an output cap and only the key variable they name, by name. The best result is `DRAFT_REVIEW_REQUIRED`; `release_authorized` is always false; the draft is `ai_generated`. v9 ships no model and no key. | `HUMAN_ONLY_NO_GENERATED_PROSE`, `SEND_CONSENT_REQUIRED`, `KEY_ENV_INVALID`, `PROVIDER_CLAIMED_AUTHORITY`, `QUOTATION_UNVERIFIED:<n>`, `PROVIDER_TIMEOUT` |

Platform: these tools need POSIX file safety (`O_NOFOLLOW`, `dir_fd`). On Windows they refuse with `PLATFORM_UNSUPPORTED`, and CI proves that refusal on a Windows runner rather than assuming it.

### `prototypes/wi9/` — reference kernel (WI9-05)

The owner's reference kernel, ported unchanged except where a defect was repaired: a **334-rule editorial phrase catalog** (321 literal, 13 regex, 11 categories) and scanner with exact code-point offsets and document/rule digests; a review ledger that binds each keep-or-revise decision to the exact document and rule pack (offset-aware review times since D-15); a model-neutral composition contract that refuses human-only venues outright and can only reach `DRAFT_REVIEW_REQUIRED`; voice-sample statistics; and a benchmark aggregator that holds until 60 matched cases exist. A phrase match is an editorial question. It never declares a passage AI-generated and never triggers a rewrite.

## Planned architecture (no false shipped claims)

| Wave | Name | Exit condition | Status |
|---|---|---|---|
| WI9-00 | Baseline & evidence audit | Reproduce existing v4–v8 tests; record defects with code locations | VALIDATED — receipt WI9-00; owner approval pending |
| WI9-01 | Authorship contract | Machine-readable venue policy, human/AI contribution history, meaningful disclosure | PROTOTYPE — schema 2, hardened checker |
| WI9-02 | Firsthand material vault | Opt-in private author notes, exact anchors, consent + redaction, no external uploads | PROTOTYPE — `wi authorship vault` built; awaiting a real writer's material |
| WI9-03 | Voice baseline | Each writer: 3+ of their own samples, >=500 words, reviewed by that writer; no shipped corpus | PROTOTYPE — `voice`, `voice-review`, `voice-compare` and a held-out stability check built; awaiting a real writer's run |
| WI9-04 | Thought fidelity | Preserve author claims, uncertainty and point of view across revisions | PROTOTYPE — `wi authorship meaning` inventory, diff and grant-bound review built; lexical, not semantic |
| WI9-05 | Craft repair | Correct overbalanced transitions, hollow contrasts and unsupported examples based on meaning | IN_PROGRESS — 05A–05F built; 05G (independent reader trial) not run |
| WI9-06 | Human-only venue gate | Enforce research-only vs pitch modes and author declaration, refusal negative tests | PROTOTYPE — `release` gate added |
| WI9-07 | Editorial benchmark | Author-rated fidelity, originality of observation, evidence accuracy, editor-rated usefulness | PLANNED — NOT EXECUTED |
| WI9-08 | Integration | Additive integration into `wi.py`, CLI docs, schema, regression and versioned release | VALIDATED — receipt `WI9-08` (CI run 40612980598); plans/v9.manifest.yaml, `wi authorship {audit,release,scan}`, REST `POST /v9/authorship/audit` and `/v9/hotphrases/scan` (release refused, 403), MCP tool contracts, the fourth bundle, release bound to the operator's v6 store; open: the API container image is not built in CI, no MCP server exists in this repository (as for every WI MCP tool), and a WI9-08 receipt with a CI readback |
| WI9-09 | Independent review & rollout | Artifact verification, negative controls, external review, owner's release decision | PLANNED — release HOLD |

### Measurement, not mythology

Compare each candidate with (a) the author's original material, (b) the original AI draft, and (c) an author revision, using blinded human editorial judgments and anchored claim preservation. Measures: claim-level evidence coverage; unsupported autobiographical claims (target: **zero**); venue-policy violations (target: **zero**); author's rating of whether the ideas are genuinely theirs; external editor ratings of specificity/clarity; number of factual distortions introduced; transformations disclosed; author acceptance. Report denominators, uncertainty and source provenance. **No target for AI detector score.**

### Adversarial negative controls

1. A human-only venue plus an AI-generated/AI-assisted submission **HOLD** even when the detector gives 0%.
2. A first-person experience backed only by hypothetical model text **HOLD**.
3. A source claim with wrong exact quote or digest **HOLD**.
4. A source lacking explicit consent **HOLD**.
5. A human-authored claim is **self-declared**, never certified by a file label.
6. No randomly inserted typos, fabricated admissions, staged personal scenes or detector-driven paraphrasing.
7. Existing v4–v8 releases, packages and tests remain unmodified until the proper integration wave.

## Correction to existing craft guidance (done in WI9-05A)

The v8 craft doctrine told writers to alternate sentence lengths by formula, inject "unpredictability", swap synonyms to dodge repetition counts and score "AI detection risk". That conflicted with the v7 ban on evasion and reduced authorial fidelity. The instruction lived in more files than `cadence.md` and `structures.md` (see D-14 in [`defects.md`](defects.md)); every one now says: **revise for meaning, voice, clarity and evidence; let cadence result from the author's thinking and genre.** `inject_variance` is now `repair_rhythm`, and `tests/v9/test_doctrine_meaning_led.py` fails if a detector-oriented instruction returns. Detector-oriented rewriting has no release role.

## Venue example: HARO miniature worlds

The author confirmed experience building, collecting and designing physical miniatures, digital worlds, and scale simulations. The organizational blueprint describes game design and infrastructure research; it is not a dated account of a completed specific build. An invented "solar community model" is illustrative, not firsthand. An AI-generated essay remains AI-generated regardless of how natural it sounds. For a human-only journalist, the permitted output is source research and interview prompts, not an AI-written email for submission.

## Decision

**PROPOSAL ONLY.** Prototype tests are separate from author ownership, editor signoff, ethical eligibility, or a version-9 release. Review the PR, check the independent tests and accept/reject each program wave explicitly.
