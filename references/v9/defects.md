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
| P0-11 | No authority binding | `release` requires a REVIEW audit, a person's decision bound to the exact draft digest, an open `submit` operation and an unpassed deadline, and asks the v6 grant store (`scripts/wi.py authority`) whether that person holds `release.approve` in scope `release_target:<venue>` — at decision time and now, as a human subject. A grant declared in the dossier holds `AUTHORITY_UNBOUND`; the operator names the store (`--authority-store`, outside the dossier folder, read-only) — see R-01, R-04, R-05 | `Release` tests; 4 binding mutations in CI | Repaired; bound to v6 |
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

## Independent review (2026-10-27) — automated, fresh context

A separate reviewer with no context from the build read the code and ran its own reproductions under the threat model "the dossier and every file it names are hostile". It is an automated review, not the human review WI9-09 requires. Every confirmed finding below was reproduced, repaired, and guarded by a test shown to fail against the code as it was.

| ID | Severity | Finding | Repair | Guard |
|---|---|---|---|---|
| R-01 | high | `release` read authority from a store the dossier's own folder supplied, so an author could ship a store granting themselves release — the declared-grant defect one layer down | The operator names the store with `--authority-store`; a store inside the dossier folder holds `AUTHORITY_STORE_UNTRUSTED`; a dossier naming a store holds `AUTHORITY_STORE_FROM_DOSSIER` | `test_store_planted_inside_the_dossier_is_untrusted`, `test_dossier_cannot_choose_the_store`, `test_release_needs_the_operator_to_name_a_store`; CI mutation |
| R-02 | high (DoS) | each draft anchor built a full list of every match in the draft | `startswith` at a given offset, otherwise two `find` calls; at most 1,000 anchors; spans bisected against claims | `test_many_anchors_on_a_large_draft_stay_fast`, `test_too_many_anchors_hold` |
| R-03 | high (DoS) | `scripts/wi.py sentences` joined the whole buffer at every terminator — quadratic on a run of `a.` | Only the last eight characters are tested; output proved identical on 5,000 random strings and every repository document; 400 KB now 0.16 s | `test_long_unbroken_draft_is_linear`; v4–v8 suites unchanged |
| R-04 | medium | a symlinked `.wi` inside the named store was followed | `.wi` and `workspace.db` must be real files (`lstat`) | `test_symlinked_store_database_is_refused` |
| R-05 | medium | the check opened the store read-write and created tables | sqlite `mode=ro`; the v6 authorize rule reimplemented over read-only queries with the same order and codes | `test_release_never_writes_to_the_store` (bytes and file list unchanged) |
| R-06 | medium | a submission with no arena, or `Journalism` capitalised, was treated as non-strict | arena normalised; every submission is strict unless `document.consequential` is explicitly `false` | `test_submission_without_an_arena_is_held_to_the_strict_rules`, `test_arena_case_does_not_lower_the_bar` |
| R-07 | medium (DoS) | rule `meta_conclusion` backtracked quadratically on long whitespace | `\s*,?\s+` → `(?:\s*,\s*|\s+)` (one line; rule digest and the example review updated) | `test_long_whitespace_after_a_closing_word_is_linear` |
| R-08 | medium (DoS) | phrase masking rescanned every interval per match | intervals merged; one bisect per match; 478 KB adversarial input 41.9 s → 4.2 s | `test_many_masked_spans_are_cheap` |
| R-09 | medium | composition opened a prose request for `human-only`, `Human_Only` or any unknown policy | allowlist: only `ai_permitted` and `disclosure_required` open a request | `test_unrecognised_policies_never_open_a_prose_request` |
| R-10 | medium | `inspect_candidate` raised on malformed `evidence_ids`; an empty quotation verified | ids type-checked before use; empty quotation refused | `test_malformed_evidence_ids_hold_without_a_traceback`, `test_empty_quotation_is_not_verified` |
| R-11 | medium | the review ledger reached REVIEW with nothing reviewed, and accepted a report with findings deleted | unreviewed findings hold (`FINDINGS_UNREVIEWED`); the report is re-scanned and must reproduce (`REPORT_NOT_REPRODUCED`) | `test_nothing_reviewed_is_not_review`, `test_forged_report_with_findings_removed_holds` |
| R-12 | low–medium | the review ledger crashed on list-valued fields or deep JSON | field types checked; `TypeError` and `RecursionError` caught; 2 MB input cap | `test_unhashable_decision_fields_hold_without_a_traceback` |
| R-13 | low | an unwritable `--out` raised a traceback; `--out` followed symlinks | `O_NOFOLLOW` write; failure is a structured HOLD | `test_unwritable_out_is_a_structured_hold` |
| R-14 | low | `wi9_core` had no work caps | 5,000-item caps on evidence, links, contributions, samples; 20,000 ratings | `test_oversized_evidence_list_holds` |
| R-15 | low | `test-v9.sh` counted "Ran 0 tests" as a pass; the builder followed symlinks in the authorship payload | a lane passes only with at least one test run; a payload symlink fails the build | inspected; the zero-test case cannot pass `grep '^Ran [1-9]'` |

Not reproduced and left open: `decided_at` is self-declared, so "the grant was active when they decided" proves the declared time fell inside the window, not when the decision really happened.

## Open — not repaired, stated rather than hidden

- Authorship remains self-declared by design. No tool here can authenticate a writer.
- Claim discovery depends on the v4 classifier; sentences it calls rhetoric are not checked, and semantic entailment is not implemented.
- No Windows file-safety strategy; the checkers refuse to run there.
- The phrase scanner's Markdown masking is heuristic and Python `re` has no timeout; only reviewed local rule packs are accepted.
- No consented author corpus, no 60-case benchmark, no external review: WI9-03, WI9-07 and WI9-09 have not run.
