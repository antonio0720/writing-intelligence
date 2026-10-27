# Writing Intelligence v9 — defect register (WI9-00)

**Project owner:** Antonio T. Smith Jr. — Density6 LLC
**Baseline measured:** 2026-10-27 against PR #8 head `80e7aef88441c2f2e9eb5734b43b601924592dac`
(base `d9a180d9219e38c3305bbf1f30c3ed0600ab21f9`). Receipt: [`plans/receipts/WI9-00.json`](../../plans/receipts/WI9-00.json).

Each row names the code location at the baseline, the repair, and the test
that goes red if the defect returns. "Repaired" means the guard exists and was
made to fail by a mutation; it does not mean the wave that owns the defect is
validated or shipped.

## P0 — fixed before any generation feature

| ID | Defect at baseline (`scripts/wi-authorship.py`) | Repair | Guard (tests/v9/test_authorship_p0.py) | State |
|---|---|---|---|---|
| P0-01 | `origin`, `consent`, `contribution_log` read as facts | Every report carries `declaration_status: self_reported`, `decision_scope: limited_checks`, `release_authorized: false`; no state named VERIFIED exists | `test_forged_human_declaration_reaches_review_never_verified` | Repaired |
| P0-02 | Only supplied anchors were checked; unanchored claims passed | `discover_claims` runs the v4 classifier (`wi.py sentences`/`classify`) over the draft; every consequential claim must overlap an anchored span; unmatched claims HOLD a strict-arena submission and are reported elsewhere | `test_one_safe_anchor_cannot_carry_three_unsourced_claims`, `test_internal_review_reports_coverage_without_holding_on_it` | Repaired |
| P0-03 | Exact excerpt match read as support | Anchors report `ANCHOR_RESOLVED`; support is `unadjudicated` unless a reviewer records `support_status`; `needs_source`/`conflicted` HOLD strict submissions | `test_resolved_anchor_is_not_reported_as_support`, `test_needs_source_and_conflicted_evidence_hold_submission` | Repaired |
| P0-04 | Duplicate/missing evidence ids; dangling and ambiguous draft anchors | Unique nonempty ids; dangling links HOLD; an excerpt that occurs twice needs `start`; a wrong `start` HOLDs | `EvidenceIdentity` (6 cases) | Repaired |
| P0-05 | `analyze()` called `.get` on any root | Root type checked first; nested types checked before use; JSON depth, list and object size bounded | `InputParsing` (4 cases) | Repaired |
| P0-06 | `read_bytes()` before the size check | Size taken from the open descriptor; at most `limit+1` bytes read; dossier itself bounded at 2 MB | `test_oversized_document_refused_before_full_read`, `test_oversized_dossier_refused` | Repaired |
| P0-07 | `resolve()` then read: symlink and race exposure | Component-by-component `os.open(..., dir_fd, O_NOFOLLOW)`; absolute, `..`, NUL and symlinked file, directory or dossier refused; non-POSIX fails closed | `FileBoundary` (6 cases) | Repaired; Windows strategy not built |
| P0-08 | Draft hashed, never compared | `document.expected_sha256` compared; required for any submission; strict-arena submissions must pin each source | `Immutability` (3 cases) | Repaired |
| P0-09 | Log could omit AI prose while origin said human | `ORIGIN_CONTRADICTS_LOG` on any venue; human-only venues refuse assistance the venue contract does not list (unknown means no); a human-only contract cannot permit AI prose | `DeclarationsAndVenue` (5 cases) | Repaired |
| P0-10 | REVIEW exited 0 and read like permission | REVIEW prints a stderr notice; `audit` can never emit a release state; release is a separate subcommand | `test_audit_never_returns_release`, `test_bound_decision_is_release_eligible_and_sends_nothing` | Repaired |
| P0-11 | No authority binding | `release` requires a REVIEW audit, a person's decision bound to the exact draft digest, a grant held by that person covering `release` and the named venue and unexpired, an open `submit` operation and an unpassed deadline. Binding the grant to the v6 store is WI9-08 | `Release` (17 cases incl. 14 subtests) | Repaired at the declaration layer; v6 binding open |
| P0-12 | v8 craft doctrine prescribed detector-oriented variance | Doctrine rewritten meaning-led (WI9-05A); `inject_variance` → `repair_rhythm`; detector benchmark retired as a method; fabricated statistics removed from a gold example | `tests/v9/test_doctrine_meaning_led.py` with a planted twin | Repaired |

Mutation run at repair time: six guards (coverage hold, digest compare, origin
contradiction, root check, file `O_NOFOLLOW`, grant expiry) were each disabled
in turn; the suite went red every time. The grant-expiry mutation first
escaped — an expired grant was still caught by the "decided after expiry"
branch — and a case isolating it was added before the run was repeated.

## Found during the repair, not in the handoff

| ID | Defect | Repair | State |
|---|---|---|---|
| D-13 | `tests/gold_outputs.md` Example 3 added statistics absent from its "before" text and claimed detector reclassification — a gold example teaching v4 Law C/D violations | Rewritten under P0-12 | Repaired |
| D-14 | Detector-oriented instruction lived in 12+ doctrine files, not the two the handoff named (`rewrite_operators.md`, `failure_modes.md`, `scorecard.md`, `auto_diagnostic_report.md`, `prose_compiler_v3.md`, `academic_mode.md`, `cadence_expanded.md`, `SKILL.md`, `packs/craft/SKILL.md`, `tests/detector_benchmark_suite.md`, `tests/adversarial_cases.md`, `agents/stress_tester.md`) | Rewritten under P0-12; v7's scan did not cover these words | Repaired |
| D-16 | `tests/gold_output_library.md` academic exemplar attributed specific figures to real authors and an agency (BLS 2023, a 2009 study "in 42%", a 2017 study) that nothing in the repository anchors, and listed sentence lengths as a reason for the score | Figures re-pointed to synthetic source cards S1–S3; a synthetic-figure rule added to the library's purpose; every sentence-length line labelled descriptive | Repaired |
| D-17 | Further invented real-world facts in teaching material: `examples/01`, `03`, `05` (named researchers, a university, national policies, an AI lab claim, a named bakery), `tests/gold_output_library.md` government brief (real counties, a statute subsection), and `references/positive_patterns/evidence_moves.md` and `scene_grounding.md` (a named study, a real person's quote, international-body counts, a polling series, budget-office figures). `scene_grounding.md` also taught that a good detail is one a language model could not generate | Replaced with synthetic source cards or `[needs source]`; the detector framing rewritten meaning-led | Repaired |
| D-15 | Reference kernel review ledger accepted any nonempty `reviewed_at` | Offset-aware ISO 8601 required, future times refused | Repaired (`prototypes/wi9/tests/test_wi9_phrase_review.py`) |

## Open — not repaired, stated rather than hidden

- Authorship remains self-declared by design. No tool here can authenticate a writer.
- Claim discovery depends on the v4 classifier; sentences it calls rhetoric are not checked, and semantic entailment is not implemented.
- The grant in `release` is a declaration until WI9-08 binds it to `scripts/wi.py authority`.
- No Windows file-safety strategy; the checkers refuse to run there.
- The phrase scanner's Markdown masking is heuristic and Python `re` has no timeout; only reviewed local rule packs are accepted.
- No consented author corpus, no 60-case benchmark, no external review: WI9-03, WI9-07 and WI9-09 have not run.
