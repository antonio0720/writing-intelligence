# WRITING INTELLIGENCE v9 — FULL ENGINEERING IMPLEMENTATION & AUTHORIAL VOICE HANDOFF

**Project author:** Antonio T. Smith Jr.  
**Organization:** Density6 LLC  
**Delivery date:** October 27, 2026  
**Scope:** Original v9 engineering handoff preserved below, expanded with a fully executable experimental local reference kernel, 334-rule editorial hot-phrase corpus, source-constrained composition interfaces, digest-bound review, 81 passing local tests, attack surfaces, implementation steps and release criteria.  
**Releases:** v8 remains the published baseline; v9 prototype only. The local reference implementation is supplied separately in a ZIP and has **not** been pushed into PR #8.  

---

# WRITING INTELLIGENCE v9 — COMPLETE ENGINEERING HANDOFF

**Project owner and designated project author:** Antonio T. Smith Jr.  
**Organization:** Density6 LLC  
**Repository:** https://github.com/antonio0720/writing-intelligence  
**Handoff date:** October 27, 2026 (America/Chicago)  
**Program:** WI9-AUTHORSHIP — Authentic Voice, Original Thought, Evidence & Publication Integrity  
**Handoff status:** Ready for implementation; **v9 is NOT released**  
**Authority:** This handoff delegates no authority to merge, publish, send pitches, deploy, or change protected production behavior. Those actions require separate owner authorization.

> **One-sentence mission:** Finish Writing Intelligence v9 so it preserves real author experience, individual voice, reasoning, meaning, and evidence while enforcing publication rules—without fabricated anecdotes, detector-evasion tactics, or false claims that machine-generated writing is human-authored.

---

## 0. THE CURRENT TRUTH — READ BEFORE ANY CODING

The existing v8 system is intact on `main`. The v9 work lives in a **separate, unmerged draft PR** and currently contains a design proposal and a **limited, tested read-only prototype**, not a new generation engine or v9 release.

| Field | Verified value / status |
|---|---|
| Repository | `antonio0720/writing-intelligence` |
| Default branch | `main` |
| Working branch | `proposal/v9-authentic-voice-provenance-20261027` |
| Pull request | https://github.com/antonio0720/writing-intelligence/pull/8 |
| PR number/state | `#8`, **open**, **draft**, unmerged |
| PR mergeability at handoff | GitHub reported `mergeable: true`, `mergeable_state: clean`; this is not permission to merge |
| Base SHA | `d9a180d9219e38c3305bbf1f30c3ed0600ab21f9` |
| Verified working head SHA | `80e7aef88441c2f2e9eb5734b43b601924592dac` |
| Branch compared with `main` | 14 commits ahead, 0 behind, 7 files changed |
| v9 prototype tests | **16 test cases**, passing on Python 3.8, 3.11 and 3.13 |
| Prototype workflow | PASS: https://github.com/antonio0720/writing-intelligence/actions/runs/40554938865 |
| Full existing repository CI | **PASS: 10/10 jobs**, including v4–v8 verifiers, API, schemas, bundle, docs and manifest |
| Full CI workflow | https://github.com/antonio0720/writing-intelligence/actions/runs/40554939305 |
| PR reviews / review threads | 0 reviews and 0 review threads seen at handoff |
| Published release | **Still v8**; do not call the new work v9.0.0 shipped |
| Editorial v9 pilot | **NOT EXECUTED** |
| 60-case evaluation corpus | **PLANNED; not collected** |
| Native integration into `scripts/wi.py` | **NOT DONE** |
| New release bundles, version alignment | **NOT DONE** |
| External author/editors' blind review | **NOT DONE** |

These are observations of the **specified head commit only**. If the branch changes, check its SHA and rerun all relevant tests; this handoff's green status does not automatically follow new commits.

### The seven files currently in the PR

1. `.github/workflows/wi9-proposal.yml` — Python 3.8/3.11/3.13 test job; experimental only.
2. `references/v9/README.md` — ten principles, file contract, illustrative scenario, provisional waves.
3. `references/v9/EDITORIAL_PROTOCOL.md` — 13 editorial gates and author interview protocol.
4. `references/v9/QUALITY_BENCHMARK.md` — planned 60-case blinded evaluation, criteria, failure invariants.
5. `references/v9/WAVES.yaml` — program plan with `PLANNED`/`PROTOTYPE` waves; **none marked shipped**.
6. `scripts/wi-authorship.py` — stdlib, local, read-only prototype for declared source/provenance and venue checks.
7. `tests/v9/test_authorship.py` — 16 bounded checks and refusal cases.

**Relevant existing repository authorities:** `SKILL.md`; `references/v4/`, `references/v5/`, `references/v6/`, `references/v7/`; `references/voiceprints/custom_voiceprint_builder.md`; `references/voiceprints/voice_fingerprint_engine.md`; `references/anti_patterns/{cadence,structures,phrases,fake_depth}.md`; `references/genre_packs/{journalism,email}.md`; `scripts/wi.py`; `scripts/build-skill.sh`; and `scripts/check-manifest.py`.

### Explicitly not accomplished

A passing prototype confirms only that the tested inputs produce expected machine-readable decisions. It does **not** prove human authorship, the truth of a supplied document, complete claim coverage, reader-rated naturalness, a better prose generator, publisher eligibility, or reliable performance outside the tested paths. The separate v8 release remains the product baseline.

---

## 1. WHY V9 EXISTS: OBSERVED FAILURE AND SYSTEMIC CAUSE

**Trigger:** An AI-generated writing demonstration discussing physical miniatures, digital worlds, and scale simulations was classified by a commercial detector as **“68% possible AI”** according to the owner's test. That number is **not** a calibrated probability of authorship; neither the vendor configuration nor the classifier's validation corpus was independently verified here.

The writing itself had real defects:

- It supplied smoothly balanced three-part commentary instead of sufficiently anchored firsthand experience.
- Hypothetical miniature communities and towns created an appearance of specificity without belonging to a documented completed project.
- It repeated abstract “not X but Y” contrasts and structurally similar closures.
- It gave polished generalities where the writer's actual decisions, uncertainties, errors, and observations were more valuable.
- It risked being mistaken for an eligible journalist submission even though the query expressly excluded AI-written pitches.

**Root cause to fix:** A system that measures sentence lengths, cadence and phrasing can still fail to preserve the writer's *original thinking*. A surface-similarity score cannot establish who wrote a passage. Solve source and author fidelity first, then improve craft.

**Hard boundary:** Do not market “100% human sounding,” “undetectable,” “guaranteed 0% detector score,” “passes every detector,” or “AI-written text becomes human-authored by copying it.” Such objectives conflict with v7's explicit prohibition against detection evasion and falsely represented authorship. Writing v9 should become **more particular, useful, attributable and credible**; detector scores are not a release gate.

---

## 2. OWNER'S NON-NEGOTIABLE RULES

1. **Only Antonio T. Smith Jr. is to be named as project owner/designated project author** in proposed headers, explanatory docs, readme bylines, and project documentation. Do not append assistant, service-provider, or external co-author credit trailers. Do not rewrite Git history or falsely assert a particular commit was manually authored. Technical provenance fields must still reflect actual activity where required.
2. Preserve the v4–v8 canonical laws, especially v4 C/D/E (no unperformed work, exact support, underclaim), v5 source-dependency and explanation laws, v6 scoped authority and bitemporal state, and v7's honest-authorship constraints.
3. **No silent edits to `main`**, no release version bump, no package replacement and no deployment until the applicable tests and an owner decision support it.
4. **Author experience is not inferred from company plans.** “Planned,” “designed,” “prototyped,” “implemented,” “measured,” and “publicly released” are distinct states.
5. Source documents and exact excerpts do not independently verify the truth of an event; they verify that a claim was *attributed to that source*. Report the distinction.
6. A venue's human-only rule is binding. Do not generate submission-ready pitches for those venues. Source research, factual issue maps and interview prompts are separate, non-submission work products.
7. All scripts should remain offline-friendly, deterministic where claimed, minimal-dependency, and testable with adversarial negative controls. Python 3.8 is the current documented support floor for the core.
8. Model/agent suggestions are proposals. Approval and release require real owner authority, exact-state validation, test receipts, and independent readback.
9. **Inspectability:** SEARCH → READ → REPRODUCE → REPAIR → TEST INCLUDING NEGATIVE CONTROLS → INDEPENDENT READBACK → AUDIT NOTES. Do not mark a wave shipped based on narrative status alone.
10. Preserve the original/source before editing. Never overwrite author samples, research files, or source evidence.

---

## 3. IMMEDIATE START — EXACT REPRODUCIBLE COMMANDS

Use a clean workspace or a working copy of the repository. Do not assume the branch currently checked out on the laptop. Run:

```bash
# Fetch the exact owner repository and v9 branch.
mkdir -p ~/Documents/Codex
cd ~/Documents/Codex
[ -d writing-intelligence/.git ] || git clone https://github.com/antonio0720/writing-intelligence.git
cd writing-intelligence

git fetch origin --prune
git switch --track origin/proposal/v9-authentic-voice-provenance-20261027 2>/dev/null \
  || git switch proposal/v9-authentic-voice-provenance-20261027
git status --short
git rev-parse HEAD
git rev-parse origin/main
git diff --stat origin/main...HEAD

# Core and v9 prototype smoke tests.
python3 scripts/wi.py --version
python3 -m unittest discover -s tests/v9 -p 'test_authorship.py' -v

# Existing regressions. Do not skip v7: it explicitly prevents a return
# to detector-evasion doctrine. Stop and investigate any nonzero exit.
bash tests/v4/test_wi.sh
bash tests/v5/test_wi5.sh
bash tests/v6/test_wi6.sh
bash tests/v7/test_wi7.sh
bash scripts/test-v8.sh

# Manifest, docs, packaging sanity. `--check` does not update root bundles.
python3 scripts/check-manifest.py
python3 scripts/check-links.py
bash scripts/build-skill.sh --check
```

**Expected at exact handoff SHA:** GitHub CI passed; local execution must independently reproduce the outcome before any local changes are trusted. The command count/format may vary by existing scripts; preserve raw logs, exit codes and SHA rather than declaring pass from expectation.

To inspect the PR: `https://github.com/antonio0720/writing-intelligence/pull/8`. For repeat runs, compare exact new commit SHA with the run `head_sha`. Do not use an older green workflow as proof for a later commit.

**Safety before a coding session:** preserve original repo state, inspect `git status`, commit additive code to a feature branch, avoid force-push over a collaborator's branch or editing a dirty working tree. No merge until owner's explicit authorization.

---

## 4. P0 DEFECTS — FIX THESE BEFORE ADDING GENERATION FEATURES

The current script should be described as an **authorship-claim *declaration checker***, not an authorship verifier. It can be passed by a dishonest or incomplete dossier. The following issues are based on a readback of the actual current code, not claims of observed exploitation.

| ID | Defect / risk | Exact implementation task | Acceptance / negative control |
|---|---|---|---|
| P0-01 | `origin`, `consent` and `contribution_log` are self-declared | Keep a typed distinction: `declared_by`, `source_digest`, `recorded_at`, `review_decision`; never translate a declaration into independently authenticated authorship | A forged declaration can reach only `REVIEW`, **never `VERIFIED HUMAN`** |
| P0-02 | Draft claims are not comprehensively discovered | Feed existing v4/v5 claim extraction and create a **claim coverage ledger**; compare extracted atoms with supplied anchors; unmatched consequential claims => HOLD | A document with one anchored sentence plus three unsupported factual claims cannot pass |
| P0-03 | Exact excerpt match is weaker than factual entailment | Mark exact match as `ANCHOR_RESOLVED`; separate claim support (`supported`, `needs_source`, `conflicted`, etc.) and human adjudication | Unrelated paragraph containing the same words does not become factual proof |
| P0-04 | Duplicate evidence IDs / semantic mismatches not blocked | Enforce unique nonempty IDs, typed claim IDs, anchor offsets or exact quote with disambiguation, declared source digest and evidence-to-claim referential integrity | Duplicate ID, dangling link and conflicting anchors each HOLD |
| P0-05 | `analyze()` assumes root input is an object | Validate top-level JSON type and required schemas before any `.get`; return structured HOLD for `[]`, `null`, scalar, wrong key types | Malformed root never causes uncaught exception or missing JSON result |
| P0-06 | File-size limit checked after reading all bytes | Bound reads before allocation using file size and at most `MAX_BYTES + 1` bytes; reject oversize; protect UTF-8 failure paths | An oversized file refuses predictably without unbounded read |
| P0-07 | TOCTOU / symlink / path controls need threat model | Explicit local trust boundary, symlink handling, sandbox traversal checks, output-path restrictions as appropriate | `../`, absolute path, symlink escape and race tests produce HOLD without escaping workspace |
| P0-08 | Document is hashed but not checked against expected pinned digest | Support `document.expected_sha256`; preserve source-digest custody and exact commit/environment snapshot | Mutation of a draft after author approval invalidates the prior decision |
| P0-09 | Contribution log can omit AI writing while claiming human origin | Mark all results self-reported; define lifecycle and required policy questions, avoid machine-origin certification; define escalation for ambiguous mixed contributions | `human_only` + declared AI-generated prose or substantive rewrite always HOLD, even if `origin` says human |
| P0-10 | `REVIEW` returns exit 0 and is easy to misread as publishable | Make docs, CLI output and parent integration explicit that `REVIEW` means limited checks, **not RELEASE**; consider a separate `RELEASE` decision API restricted to human approval and venue checks | Automated send cannot treat `REVIEW` as permission to transmit |
| P0-11 | No structured proof of all claimed authority | Connect venue contract and release decision to v6 scoped actor/authority and immutable target digest rather than flat booleans | Expired authority, stale approval and wrong target digest block release |
| P0-12 | The v8 craft corpus still prescribes detector-oriented sentence-length manipulation | Replace incompatible *implementation directives* in `references/anti_patterns/{cadence,structures}.md` with meaning-led edits and a test that catches regressions; preserve useful rhythm diagnostics | No instruction to game detector outputs remains; v7 tests still pass |

**Do not try to remove P0-01 by claiming perfect authorship verification.** Origin cannot be inferred reliably from prose style. V9 must make provenance *auditable* and label limits honestly.

**Where the current code is:** `scripts/wi-authorship.py` provides `audit --input dossier.json [--out report.json]`. Input contains `schema`, `document`, `evidence`, `voice_samples`, optionally `contribution_log` and `document_claim_anchors`. It checks local exact strings and declared policies, produces JSON `REVIEW` or `HOLD`, and exits 0 or 3. The prototype's current outputs are *not* integrated with `wi.py` or the canonical state graph.

---

## 5. REMAINING WAVES — DO IN DEPENDENCY ORDER

**Status vocabulary:** `PLANNED` → `IN_PROGRESS` → `PROTOTYPE` → `VALIDATED` → `SHIPPED` only with explicit receipts. Current `references/v9/WAVES.yaml` names **all waves** and marks only WI9-01 and WI9-06 `PROTOTYPE`. Do not silently promote statuses.

### WI9-00 — Baseline, freeze and defect reproduction

**Inputs:** `main` base SHA, PR #8 head SHA, v4–v8 regression results, the original AI-generated miniature essay, reported detector result, actual v9 code.

**Build:** Establish evidence manifest containing source git SHA, suite names/versions, date and environment; reproduce all 16 v9 tests and existing CI; create severity-ranked P0/P1/P2 defect register; record genuine v8 cadence contradictions; confirm no prior author samples were silently treated as verified.

**Required artifacts:** `plans/receipts/WI9-00.json` when complete; `references/v9/defects.md`; deterministic baseline result; immutable original sample digest. Use existing receipt schema or design migration carefully; no parallel status authority.

**Exit:** independent readback of repository and tests; P0 claims tied to exact code locations; approved baseline. **Current status: PLANNED**, even though upstream CI is green, because no program receipt was created.

### WI9-01 — Authorship & venue contract (prototype → validated)

**Purpose:** Ensure the system knows the source of each contribution and the publication agreement before packaging a piece.

**Build:** Versioned JSON Schema for document/venue/audience/intent/word limits/AI permissions; typed contribution history with role (`human_original`, `human_edit`, `ai_research`, `ai_generated_prose`, `ai_substantive_rewrite`, `mechanical_proofread`); doc/source digests, scope, consent and explicit unresolved states. Declared vs independently evidenced claims remain separate. Model unknown policies conservatively and require manual review. For venues with “no AI pitches,” prohibit submission-ready generation or substantial AI rewriting.

**Tests:** missing log, conflicting declared origin, expired policy, unknown policy, invalid arena, ambiguity, intentional mislabeled sample, disclosure-required venue, version migration, mixed contributions. Verify different kinds of assistance are not silently treated as equivalent.

**Exit:** schema, reference parser, negative controls and authorization semantics accepted by owner.

### WI9-02 — Firsthand evidence vault and intake

**Purpose:** Specificity without invented first-person scenes.

**Build:** Private, opt-in source storage; sources include author notes, voice transcripts, photos' metadata (only if permitted), dated drafts, models, sketches, user-authored interviews and external research. Label `observed`, `said_by_author`, `inferred`, `sourced`, `hypothetical`, `planned`, and `measured` distinctly. Store source bytes / digests, provenance, optional timestamps and human corrections. Support consent withdrawal, redaction and no automatic external submission. Sensitive source material must stay out of PRs and CI artifacts.

**Integration:** use v4 exact excerpt anchors and v5 claim graph; do not create a second canonical claims truth source. Unresolved conflicts remain unresolved under v6.

**Negative controls:** roadmap presented as completed build, model-generated anecdote, edited transcript treated as verbatim, conflicting dated accounts, missing source, invalid privacy consent, stale source, metadata containing false date, cross-project data leakage.

**Exit:** 100% of autobiographical claims in test corpus have attributable source or explicit `needs_source` with HOLD; privacy tests pass.

### WI9-03 — Measured, consented author voice baseline

**Purpose:** Voice fidelity measured against what the author actually wrote.

**Build:** Intake at least **three authentic, consented samples of 500+ words each** per proposed voiceprint, from varied relevant contexts. Track originality/declaration, dates, genre, digest and representativeness. Measure existing v3 voice dimensions while adding semantic voice measures: habitual disagreements, qualifier choices, argument strategy, technical priorities, use of concrete details, distinctive but genuine idiom and editing decisions. Provide `voice_id`, per-sample distributions, confidence/limitations and per-genre baselines. Never imply that a “familiar sound” proves human origin.

**Tests:** wrong-author samples, cross-genre contamination, repeated model-generated drafts mislabeled as original, insufficient sample count, changed SHA, deliberately stylized imitation, overfitting to one paragraph, sample withdrawal.

**Exit:** author review approves the voiceprint for specific genres; compare stability using held-out author text; no claims of detector immunity.

### WI9-04 — Original thought and meaning fidelity

**Purpose:** Stop replacing original reasoning with fluent but interchangeable generic prose.

**Build:** Canonical proposition inventory sourced from author material. Capture actor, decision, mechanism, constraints, friction, consequence, counterargument, scope and real uncertainty where available. Generate a semantic diff between original thought and candidate revisions. New autobiographical facts require fresh source acceptance; unsupported strengthening must produce a proposal and HOLD. Hook into v5 dependency graph and v6 propose/simulate/decide mechanics rather than rewriting their authority model.

**Tests:** opinion reversal, missing concession, planning-to-completion promotion, measured-to-estimated promotion, reversed chronology, invented outcome, quote paraphrase disguised as verbatim, absent premises, prose with same style but different meaning.

**Exit:** zero silent protected-meaning changes in test fixtures; author can inspect and accept/reject every material semantic delta.

### WI9-05 — Meaning-first craft, cadence and genre repairs

**Purpose:** Improve readable, distinctive prose without manipulating detector behavior.

**Build:** Correct the specific v8 passages instructing artificial randomness, fixed alternation of sentence lengths, planted imperfections and detector-targeted “humanizing.” Retain anti-slop checks for hollow contrasts, repeated restatements, generic authority and empty endings *as editorial tools*. Strengthen author-owned specificity, scene consequence, thought development and appropriate unevenness that results naturally from content. Apply genre-specific weighting: short pitches; executive email; explanatory technical work; essays; fiction. Reuse `references/genre_packs/` rather than replacing existing packs.

**Evaluation:** Use side-by-side author and editor judgments. No externally invented experience, sham statistics, or falsely attributed quotes. A sentence should change because an editor can explain an improvement in clarity, credibility or meaning.

**Tests:** repetitive three-part essay, unsupported personal scene, mechanically varied but nonsensical writing, over-polished founder pitch, sterile technical prose, false binary contrast, genuinely necessary contrast that must not be cut.

**Exit:** positive quality preference in blinded pilot with no loss of claim preservation; v7 detection-evasion regression remains green.

### WI9-06 — Human-only venue policy gate (prototype → validated)

**Purpose:** Block ineligible external pitch packaging.

**Build:** Typed permissions for `research`, `draft`, `edit`, `package`, `submit` and scope of allowed assistance. A `human_only` contract must prevent generated copy being labeled submission-ready. Do not assume the venue permits AI proofreading; if unknown, preserve HOLD. The system should be able to generate an evidence brief or original-source checklist without producing a prohibited submission. Separate internal `REVIEW` from external `RELEASE` and from receipt-confirmed delivery.

**Tests:** AI-written pitch manually sent by owner, AI-generated copy with 0% detector report, AI rewrite claimed as human, unrestricted venue, AI-disclosure venue, ambiguous publication policy, deadline changed, submitted after closing, manual override without authority.

**Exit:** all prohibited paths rejected; owner-approved exception handling can narrow but not widen venue rules; no automated transmission from a limited checker.

### WI9-07 — Blinded editorial benchmark and reality test

**Purpose:** Establish whether v9 actually improves the writer's prose.

**Planned evaluation:** **60 cases** with 15 each for journalism/expert commentary, executive correspondence, fiction and technical/institutional work. Four arms as appropriate: original author text, v8 output, v9 candidate and optional author-only revision. Blind, randomized editorial review; original author's semantic acceptance; independent reader/editor ratings; source-anchored claim preservation. Ratings use the eight 1–5 dimensions already specified in `references/v9/QUALITY_BENCHMARK.md`.

**Primary measures:** percentage author-accepted ideas, rate of source-supported first-person assertions, factual distortion rate, editor-rated specificity and usefulness, voice fidelity, disagreement distribution, and the proportion of outputs meeting actual venue constraints. Predefine scoring rubrics and success criteria **before** examining outcomes.

**Critical invariants:** zero invented firsthand events, zero human-only publication violations, zero silent consequential changes. Report denominators, uncertainty, failed examples, and dissenting reviews. Do not report “100% human” and do not optimize against detector percentages.

**Exit:** actual collected corpus and recorded independent results; a real improvement finding or explicit failed pilot. **Current status: NOT EXECUTED.**

### WI9-08 — Canonical integration, distribution and regression

**Purpose:** Integrate validated components without breaking v4–v8 or lying about what ships.

**Build:** Add versioned schema and integration points into `scripts/wi.py` for the *validated* feature set only; wire claim IDs and evidence into v5 graph; enforce v6 authority, staleness and decisions; add v9 unit/negative/integration tests to existing GitHub workflows. Keep CLI commands and actual documented feature status aligned. Update `SKILL.md`, README, CHEATSHEET, docs, examples, and bundles only when ready to release—not merely when a concept is written. Update `scripts/build-skill.sh` payload and check strict 200-file ceiling per bundle; do not assume v9 content fits the existing three bundles. Introduce another additive bundle only with a justified install/release contract.

**Tests:** all previous v4/v5/v6/v7/v8 suites; Python 3.8+, multiple supported operating systems; manifest validator; schemas; docs links; reproducible packaging; installer smoke tests; tampered bundle controls; no regression to detector-evasion text; unchanged API behavior where promised.

**Exit:** entire tested distribution installs and runs from freshly extracted artifacts; SHA and release docs agree.

### WI9-09 — Independent release, receipts and owner approval

**Purpose:** Only ship what independent checks substantiate.

**Build:** Complete signed-off manifest/receipts for every wave; independent machine fresh-clone and artifact check; code review and security review; editorial pilot evidence; exact source and version checks; release notes; migration/rollback plan. Obtain owner decision for merge/release. Only then change version designation to `9.0.0`, publish bundles, create release/tag and verify install from the actual distributed files.

**Negative control:** incomplete wave, unmeasured editorial score, missing receipt, stale approval, unsigned/offline proof failure, mismatched skill bundle, old CI SHA, unsupported authorship claim, hidden disclosure violation all block release.

**Exit:** independently verifiable release, no unresolved critical defects, owner authorization, and post-release readback. Until then: **HOLD**.

---

## 6. EXECUTION ORDER, PARALLEL WORK AND HARD DEPENDENCIES

Do not start by polishing prompts. The correct sequence is **truth boundary → corpus → author voice → thought preservation → craft → external evaluation → integration → release**.

| Priority | Wave(s) | Can work in parallel? | Blocker / dependency |
|---|---|---|---|
| P0 | WI9-00, P0 fixes | Start immediately | Need baseline and defect reproductions |
| P0 | WI9-01 + WI9-06 | Parallel after baseline | Shared canonical venue/authorship contract |
| P0/P1 | WI9-02 | Parallel with WI9-01 schema finalization | Privacy, permission and source-custody contract |
| P1 | WI9-03 | Parallel with WI9-02 collection | Consented genuine author samples |
| P1 | WI9-04 | After evidence model is stable | Canonical claim graph / semantic state |
| P1 | WI9-05 | Prototype in parallel, validate after 03/04 | Cannot evaluate voice or meaning without baselines |
| P1 | WI9-07 | Design early; execute after 03–06 | 60-case corpus, blinded editor protocol |
| P1 | WI9-08 | After validated candidate features | Passed full regressions and approved contracts |
| P0 final gate | WI9-09 | Last | Owner release decision and independent proof |

**Do not conflate the two tracks:** provenance/eligibility (mostly deterministic) and writing quality/voice fidelity (human-judged and partly probabilistic). Both are needed, but passing either does not imply the other.

---

## 7. RECOMMENDED ARCHITECTURE — ADDITIVE, NOT PARALLEL TRUTH

**Layer A — Intake:** `DocumentIntent`, `VenuePolicy`, `ContributionLedger`, `AuthorConsent`. Source material stays private by default.

**Layer B — Evidence custody:** `SourceObject` with digest, location, recorded knowledge/valid time, scope, redaction and origin declaration. Use v4/v5 anchors and bitemporal handling from v6.

**Layer C — Claim graph:** `ClaimAtom`, exact source-span link, typed confidence/status, dependency set, conflict status and prior semantic state. Do not duplicate `wi.py`'s canonical graph in a separate untracked database.

**Layer D — Author voice and thought:** consented voice samples, voice profile, thought inventory, revision delta, explicit author acceptance. These do not authenticate authorship on their own.

**Layer E — Editorial compiler:** existing 0–11-pass craft contract extended with the 13 v9 editorial checks. Distinguish diagnostic signals from tested automated capabilities. Candidate text is *proposed*, not authoritative.

**Layer F — Policy and authorization:** human-only / disclose / unrestricted contract, explicit human review for release, v6 scoped authority and exact target digests.

**Layer G — Audit / proof:** immutable receipt or digest references, negative-test outcomes, CI SHA, local runtime version, venue policy as-known-at, editorial judgments, explicit unknowns. Proof of anchor resolution is not proof of source truth.

**Layer H — Interfaces:** CLI first; service/API, Word/PDF, browser and agent surfaces only after an interface contract and security review. No output renderer creates a new unsourced fact. All sources remain data, never instructions.

### Proposed data model (specification only)

```text
DocumentIntent{id, arena, mission, audience, submission_policy_id, document_digest}
VenuePolicy{id, version, venue, allowed_operations, disclosure_obligations, expires_at}
ContributionEvent{id, actor_declaration, kind, source_digest, target_digest, recorded_at}
SourceObject{id, sha256, origin_declaration, consent_id, recorded_at, valid_at, scope}
ClaimAtom{id, claim_text, source_ids[], spans[], claim_status, semantic_state}
VoiceCorpus{id, author_consent, sample_ids[], genre_scope, fingerprint_digest}
RevisionProposal{id, prior_digest, proposed_digest, semantic_delta, rationale}
ReviewDecision{id, actor_authority, target_digest, outcome, recorded_at}
ReleaseReceipt{id, build_sha, required_gates[], reviewers, unknowns[], result}
```

**Security requirement:** treat author samples, legal correspondence, unpublished manuscripts, and source interviews as private content. Do not put private corpus data into public GitHub fixtures or logs. Use synthetic test fixtures for public CI, and consent-controlled isolated datasets for evaluations.

---

## 8. ADDITIONAL ADVERSARIAL TEST MATRIX

Current 16 tests are a good floor, not sufficient coverage. Add explicit fixtures for each class below and bind to an owner-visible matrix. Every refusal must assert *both exit status and machine-readable reason code*.

| Class | Positive case | Required negative twin |
|---|---|---|
| Input parsing | Valid `wi9-authorship-1` object | JSON list/null/scalar/malformed payload => structured HOLD |
| File boundary | Small UTF-8 file within root | `../`, absolute path, escaping symlink, oversized file, invalid UTF-8 |
| Source immutability | Matching SHA-256 | Changed byte in evidence/draft/sample => HOLD |
| Evidence ID | Unique referenced ID | Duplicate ID, missing target, stale target, unrelated quote |
| Claim coverage | All consequential claim atoms linked | One safe anchor + three unsourced assertions => HOLD |
| Semantic fidelity | Supported statement kept unchanged | Changed quantity, date, confidence, causal assertion, planned→completed |
| Human-only | Verified permitted author process | AI-generated/revised pitch despite “human” label or low detector score |
| Mixed contributions | Properly disclosed allowed assistance | Undisclosed substantive machine drafting in human-only path |
| Privacy | Consent and scoped access | Withdrawn consent, private corpus in public logs, cross-project source |
| Authority | Valid reviewer/grant for exact digest | Stale signature, expired grant, wrong document SHA, wrong venue |
| Editorial craft | Human reader improves clarity | Artificial sentence-length alternation that damages meaning |
| Voice fidelity | Held-out authentic samples agree | Wrong writer's samples, genre contamination, model-written samples |
| Packaging | Installed bundle reproduces expected CLI | Stale committed bundle, package over file limit, missing CLI command |
| Regression | v4–v8 continue passing | Deliberate mutation disables a refusal and suite must fail |

**Mutation testing:** Temporarily remove a key `HOLD` branch in an isolated fixture. A sound negative suite must go red. Restore source and verify baseline SHA afterward.

**Security review:** In the prototype, local JSON can contain deliberately hostile text. All supplied source excerpts must be treated as untrusted content, not instructions to the compiler or agent. Audit symlinks, size-bounded ingestion, output-path handling, oversized nested objects, Unicode edge cases, log redaction and denial-of-service cases.

---

## 9. DOCUMENTATION AND VERSION ALIGNMENT

Known repository constraint: the existing v7 regression checks that `scripts/wi.py --version`, `SKILL.md` and the **newest active** `plans/v*.manifest.yaml` match. A premature `plans/v9.manifest.yaml` in the ordinary release manifest folder can break v7 checks and packaging. **The proposal deliberately uses `references/v9/WAVES.yaml`** until WI9-08.

At the real integration wave:

- Create canonical v9 release manifest in the correct versioned location only when version transition is authorized; satisfy the manifest checker and required receipts.
- Run `bash tests/v7/test_wi7.sh`, `python3 scripts/check-manifest.py`, and `bash scripts/build-skill.sh --check` **after** each version/packaging change.
- Observe bundle limit **200 files per `.skill` package**; full existing repository CI currently validates the three v8 bundles.
- Update `SKILL.md`, CLI version, README, CHANGELOG, docs, schemas, install instructions, bundle metadata, release artifact SHA files and tests atomically as one reviewed release wave.
- Keep the v8 program and its four engine registers (340 fiction requirements) unchanged unless separate authorized functionality requires migration.
- Do not call a future feature “implemented” because prose in a design spec says it should exist.

**Git discipline:** Branch from exact reviewed v9 SHA; use small thematic commits with clear descriptions, independent readback, and no unrequested co-author credit. Honor GitHub's actual commit provenance rather than fabricating attribution. Do not squash a test failure into a false PASS receipt.

---

## 10. REALISTIC SUCCESS DEFINITION

A finished v9 should be able to answer *why this piece sounds like this particular author*, what source supports its claims, what it changed from the original, who approved those changes and whether its actual publication venue permits this workflow.

**Acceptance dimensions:**

| Dimension | Release requirement |
|---|---|
| Authorial thought | Author accepts major propositions as originating in or faithfully reflecting actual source intent |
| First-person accuracy | Zero invented or silently inferred firsthand events in validation sample |
| Factual integrity | Every claimed supporting span resolves; disputed truth stays flagged for review |
| Personal voice | Author and independent reviewers evaluate held-out genre-appropriate samples |
| Readability | Demonstrated editor preference versus pinned v8 comparator; report distribution and failures |
| Policies | Zero human-only policy violations in tests and real governed workflow |
| Provenance | Document digest and declared contribution history retained; no unsupported certification |
| Regression | All v4–v8 and v9 tests, negative controls, CI and bundles pass at exact release SHA |
| Packaging | Fresh install from final distributed artifact works; published docs describe only shipped features |
| Authority | Explicit owner approval and independent release receipt |

An “AI detector score” may be archived as an external observation if desired, but it cannot substitute for any acceptance criterion. **No guaranteed detector outcome is promised.**

---

## 11. OWNER DECISIONS NEEDED BEFORE FINAL RELEASE

These are genuine scope decisions, not blockers to documenting v9. Make and record them before final integration:

- **Scope:** Keep v9 strictly within writing and publishing workflows, or enable cross-product reuse through existing platform interfaces? Recommended: writing core first, interfaces additive later.
- **Private corpus:** Allow opt-in voice samples and recordings locally; define retention/withdrawal defaults and who may access them. Recommended: private and local by default, explicit opt-in for any transfer.
- **Judgment:** Set the required number of blinded reviewer ratings and author approval conditions before seeing v9 trial scores. The 60-case corpus is a proposed minimum, not yet approved or collected.
- **Editorial policy:** Confirm how a venue distinguishes “no AI pitches,” “no AI writing,” “AI proofreading permitted,” and disclosure-required. Unknown conditions => HOLD.
- **Release boundary:** Choose when to accept integration from the experimental PR into core and when to publish tagged v9 binaries. Default: after WI9-09 receipt.

Owner decisions should be versioned records bound to a precise proposed state, not informal labels that can be treated as eternal authorization.

---

## 12. ENGINEERING EXECUTION CHECKLIST

Use this as the single operational checklist. Mark complete only with linked inspectable evidence.

### Phase 0 — Resume and secure baseline

- [ ] Clone/fetch correct branch and record clean `git status`.
- [ ] Verify head SHA and latest CI run's exact `head_sha`.
- [ ] Reproduce v9 16-test suite and all v4–v8 regressions locally.
- [ ] Run manifest/link/skill bundle validation.
- [ ] Record known P0 code defects and baseline receipts.

### Phase 1 — Truth/provenance floor

- [ ] Harden malformed JSON and oversized file handling.
- [ ] Version input schema and validate nested types.
- [ ] Add unique claim/evidence IDs; prohibit dangling links.
- [ ] Add complete claim coverage rather than arbitrary supplied snippets.
- [ ] Add expected document digest, change detection and authority binding.
- [ ] Enforce human-only venue restrictions and distinguish research from submission.
- [ ] Prove a declaration cannot be misrepresented as verified human authorship.
- [ ] Add negative tests for all new refusals.

### Phase 2 — Actual author source / voice / thought

- [ ] Build opt-in private firsthand-source intake with strict provenance.
- [ ] Add voice sample consent and per-genre sampling checks.
- [ ] Build and validate author voice baseline from authentic samples.
- [ ] Build thought-inventory and semantic-diff pipeline linked to v5/v6.
- [ ] Ensure unsupported first-person scenes produce HOLD.
- [ ] Restore genuine uncertainty and disagreement, never invent evidence.

### Phase 3 — Quality engine

- [ ] Correct detector-oriented prose directives via reviewed changes.
- [ ] Implement editorial protocol diagnostics using real source material.
- [ ] Create old-v8 vs candidate-v9 benchmark fixtures.
- [ ] Collect 60 consented comparison cases or record authorized revised scope.
- [ ] Run blinded reviewer/author evaluation with full result distribution.
- [ ] Repair regressions before expanding release claims.

### Phase 4 — Integration and proof

- [ ] Integrate validated features with `wi.py` canonical architecture.
- [ ] Add schemas, docs, versioned manifest and required receipts.
- [ ] Run all old/new tests on supported Python versions and operating systems.
- [ ] Rebuild all `.skill` bundles and verify 200-file ceiling each.
- [ ] Verify reproducibility and fresh-install smoke test.
- [ ] Obtain independent review and owner release decision.
- [ ] Merge/release only after authorization; verify actual external release artifacts.

---

## 13. FAILURE RECOVERY AND STOP CONDITIONS

**Stop immediately and mark HOLD/BLOCKED if:**

1. An external proposal is packaged contrary to the venue's declared authorship rules.
2. A generated or hypothetical scenario is promoted to a personal experience without source support.
3. A model-generated paragraph is labeled human-authored because a detector predicted “human.”
4. A changed source invalidates a previous anchor and a dependent fact continues to display as verified.
5. A core regression, reproducibility check, installer file ceiling, privacy boundary, or negative-control mutation check fails.
6. A code change modifies v4–v8 behavior without an accepted semantic delta and owner authority.
7. An engineering report claims full v9 completion based only on passing the 16 current tests.
8. A release or send action lacks authorized approval tied to the exact reviewed artifact digest.

Recovery: collect evidence → isolate smallest affected behavior → reproduce → repair at the correct layer → run positive and negative controls → run regressions → independent readback → append immutable receipt. Failed receipts stay failed; the next valid attempt gets a new record. Never relabel a failed proof as a pass.

---

## 14. TEMPLATE — INDEPENDENT CHECKPOINT RECEIPT

The following is a template, not a recorded PASS:

```json
{
  "program": "WI9-AUTHORSHIP",
  "checkpoint": "WI9-XX",
  "owner": "Antonio T. Smith Jr.",
  "status": "NOT_RUN",
  "base_sha": "<exact-base-sha>",
  "head_sha": "<exact-current-head-sha>",
  "purpose": "<falsifiable objective>",
  "source_digests": [],
  "commands": [],
  "environment": {},
  "positive_controls": [],
  "negative_controls": [],
  "observed_exit_codes": {},
  "independent_readback": null,
  "known_unknowns": [],
  "defects": [],
  "decision": "HOLD",
  "release_authority": null
}
```

`NOT_RUN` may become `PASS` only on actual evidence. Receipt names, field formats and hashes must conform to or intentionally extend the canonical repo receipt policy before claiming integration.

---

## 15. COPYABLE CONTINUATION PROMPT FOR THE NEXT ENGINEERING SESSION

> Continue Antonio T. Smith Jr.'s Writing Intelligence v9 implementation in `https://github.com/antonio0720/writing-intelligence`, draft PR #8, branch `proposal/v9-authentic-voice-provenance-20261027`.
>
> First read this handoff, current `references/v9/{README.md,EDITORIAL_PROTOCOL.md,QUALITY_BENCHMARK.md,WAVES.yaml}`, existing `SKILL.md`, v4–v8 laws, the exact CLI code in `scripts/wi-authorship.py`, its 16-test suite, and GitHub Actions status. Confirm baseline PR head SHA `80e7aef88441c2f2e9eb5734b43b601924592dac`; do not assume it is still current. Reproduce tests and preserve evidence before coding.
>
> Begin with WI9-00 and the P0 defects identified here, especially comprehensive claim coverage, malformed input, file bounds, exact source integrity, human-only venue gates, and the distinction between declared versus independently verified authorship. Then complete WI9-01 through WI9-09 in dependency order, making additive, inspectable changes with negative controls and independent readback. Preserve v8, the canonical v4–v6 proof/state architecture, the v7 ban on detector evasion, and a clean, consented authorship process. Don't target detector scores, invent personal anecdotes, misrepresent the author, send external pitches, merge, or release without explicit owner authorization. Mark each wave's actual status honestly and update canonical receipts only on verified PASS.
>
> Keep **Antonio T. Smith Jr.** as the sole named project owner/designated project author in headers and project docs; do not add additional co-author trailers. Preserve truthful contribution metadata wherever it is a required provenance field. Report what changed, what was tested, what failed, why, and the next wave with exact repo paths and SHA.

---

## 16. REFERENCE INDEX

**Canonical project:** https://github.com/antonio0720/writing-intelligence  
**Draft PR:** https://github.com/antonio0720/writing-intelligence/pull/8  
**Validated head commit:** https://github.com/antonio0720/writing-intelligence/commit/80e7aef88441c2f2e9eb5734b43b601924592dac  
**Full repository green CI:** https://github.com/antonio0720/writing-intelligence/actions/runs/40554939305  
**16-test prototype green CI:** https://github.com/antonio0720/writing-intelligence/actions/runs/40554938865  
**Architecture proposal:** `references/v9/README.md` on PR branch  
**Editorial protocol:** `references/v9/EDITORIAL_PROTOCOL.md`  
**Evaluation plan:** `references/v9/QUALITY_BENCHMARK.md`  
**Wave status:** `references/v9/WAVES.yaml`  
**Experimental checker:** `scripts/wi-authorship.py`  
**Prototype tests:** `tests/v9/test_authorship.py`  
**Prototype workflow:** `.github/workflows/wi9-proposal.yml`  
**Existing craft:** `references/anti_patterns/`, `references/voiceprints/`, `references/genre_packs/`  
**Canonical runtime:** `scripts/wi.py` and v4/v5/v6 references  
**Existing regression:** `tests/v4`, `tests/v5`, `tests/v6`, `tests/v7`, `scripts/test-v8.sh`  
**Packaging:** `scripts/build-skill.sh` and `scripts/check-manifest.py`

---

## 17. HANDOFF CONCLUSION

The verified condition today is **a green, unmerged draft proposal with a functional but narrow authorship-policy/evidence checker**. It is a good starting floor, **not** a complete v9 writing system.

The next work should be WI9-00 plus P0 correctness and governance fixes. A complete v9 will not be defined by its ability to evade a detector, but by its ability to retain the author's actual ideas, individual voice, firsthand evidence, uncertainties, and publication rights while producing writing real readers regard as clear, precise, compelling, and trustworthy.

**Final handoff state:** `PROPOSED / PROTOTYPE`, owner release authorization **NOT GIVEN**, v9 release **HOLD**.  
**Project owner and designated project author:** **Antonio T. Smith Jr.**

---

# PART II — V9 AUTHORIAL FIDELITY, COMPOSITION ENGINE, 334-RULE EDITORIAL HOT-PHRASE SYSTEM, AND HARD-CODE IMPLEMENTATION

**Project author and owner:** **Antonio T. Smith Jr.**  
**Company:** **Density6 LLC**  
**Edition:** Engineering expansion 2026-10-27  
**Status:** Tested local experimental reference kernel; **not** merged into the canonical GitHub repository and **not** a v9.0.0 release.

> **Engineering directive:** This section supersedes generic suggestions in the previous handoff where it is more specific. Keep all original governance, v4–v8 proof contracts, strict journalism evidence checks, and the human-only publication restriction. The objective is prose that is **substantively individual, evidentially particular, syntactically appropriate to the author's real voice, and useful to actual readers**. Phrase cleanup alone cannot deliver that objective.

## 18. What is now concretely available (separate reference implementation)

A local `WI9_OWNER_HANDOFF_REFERENCE/` package now contains executable Python rather than only a proposed architecture. It was created in an isolated working directory and tested in that directory. **It is not yet part of GitHub PR #8.** The existing PR still has its own narrower 16-test prototype; avoid conflating the two.

| Implementation | Local package path | Actual capability | Boundary |
|---|---|---|---|
| Deterministic intake, evidence and policy preflight | `wi9_core.py` | Bounded POSIX file ingestion; digests; anchor and self-declared origin checks; human-only venue holds; editorial diagnostics; voice sample statistics; benchmark aggregation | No independent authorship or factual-truth certification |
| Model-neutral source-based composition contract | `wi9_composition.py` | Creates structured candidate requests for eligible venues; requires typed paragraphs, evidence IDs, verbatim quote checks, review flags | No model backend or semantic entailment engine; never releases content |
| **334-rule editorial phrase scanner** | `wi9_hotphrases.py` | Exact-span linting, group summaries, line/column, repeated-expression counts, quotation/code masking | No automatic rewrite, authorship classification, or detector bypass |
| Versioned phrase rules | `rules/v9_hotphrases.json` | 321 literal expressions plus 13 regex patterns, 11 report categories | Rules are editorial prompts, not banned vocabulary |
| Exact-state human review audit | `wi9_phrase_review.py` | Decisions about each alert bound to manuscript and rule-set SHA-256; stale or forged span blocks review | Does not authenticate reviewer or authorize publication |
| Unit and negative tests | `tests/test_wi9_*.py` | **81 tests passing locally** at creation of this handoff | Tests prove bounded behavior on chosen fixtures, not improved prose generation |
| Synthetic example corpus | `examples/` | Research and sample-text fixtures | None is a real completed Density6 incident |

### Actual local verification

```bash
cd WI9_OWNER_HANDOFF_REFERENCE
python3 -m unittest discover -s tests -p 'test_*.py' -q
# Observed locally for this package: Ran 81 tests ... OK

python3 wi9_hotphrases.py scan \
  --input examples/sample_essay.txt --format text

python3 wi9_core.py diagnose \
  --root examples --input sample_essay.txt

python3 wi9_core.py preflight \
  --root examples --input research_case.json
```

The sample-editorial scanner runs. The model-neutral composition code is executable and unit tested, but **does not generate prose itself**. Integration into `scripts/wi.py`, the v6 canonical authority model, and installable `.skill` bundles is still future work. No human reader study has been conducted, and no new AI-detector success claim is being made.

## 19. The actual problem the previous approach missed

A model can remove obvious clichés while remaining generic. Conversely, an original author can deliberately use “that matters,” “ultimately,” or “here's the thing” in a sentence that is perfectly appropriate. **A phrase is evidence of a possible editorial weakness; it is not evidence of machine authorship.** The repair process must ask:

1. Does the piece contain a claim only this author would make, *based on material genuinely belonging to the author*?
2. Does the paragraph provide an actor, action, mechanism, obstacle, choice, observation, or consequence that can be identified and checked?
3. Does the argument advance? Can a later paragraph exist without the earlier evidence?
4. Has the text been standardized into an essay-template shape by polishing?
5. Does the genre require this level of formality and explanation?
6. Is a phrase acting as filler **here**, or is it doing real work in context?
7. Did the proposed revision add a first-person anecdote, finding, price, credential, dialogue line, or result the source did not supply?
8. Did any machine-assisted intervention change an author's meaning, rhetoric, or publication eligibility?

A v9 document passes *editorial quality review* only on **meaning, source integrity, voice, utility, and independent readers**. The current code only produces machine-readable suggestions for that process; the human quality component still has to be developed and measured.

## 20. The 334-rule phrase system — inventory and operational semantics

**Total:** 334 inspectable rules: **321 literal expressions, 13 bounded regex rules**. The literal pack intentionally includes familiar overused phrasing; not all of it is defective on every appearance.

| Taxonomy | Rules | Examples to flag for editorial inspection | Editorial decision |
|---|---:|---|---|
| Marketing abstraction | 53 | “cutting-edge,” “seamless integration,” “unlock the potential,” “drive meaningful outcomes,” “world-class,” “paradigm shift” | Name the actual product behavior, evidence, or recipient benefit |
| Staged explanation | 49 | “let's dive in,” “here's why,” “it's worth noting,” “furthermore,” “in conclusion,” “picture this” | Remove only when announcing structure instead of developing thought |
| Empty emphasis | 44 | **“that matters,”** “this matters,” “the reality is,” “here's the thing,” “and that changes everything,” “what this means is” | Identify the exact fact, decision, consequence, or uncertainty |
| Generic claims | 34 | “studies show,” “experts agree,” “the numbers don't lie,” “it is widely known,” “numerous studies” | Cite the specific publication, timeframe, cohort, source, or bound |
| Generic conclusions | 30 | “the possibilities are endless,” “only time will tell,” “the journey continues,” “the future is bright” | Conclude with earned change, evidence, remaining risk, or action |
| Performed candor | 26 | “let's be honest,” “truth be told,” “the harsh truth,” “here's what nobody tells you” | Preserve only if it is authentically characteristic and substantiated |
| Qualifier padding | 25 | “with that being said,” “nuanced approach,” “no simple answer,” “in many ways” | Protect real uncertainty; remove ornamental hedging |
| Domainless solutionism | 25 | “empower organizations,” “enhance productivity,” “drive transformation,” “unlock efficiency” | Who does what, with what input, to produce what result? |
| Empty metaphor | 22 | “rich tapestry,” “symphony of,” “beacon of hope,” “bridge the gap,” “secret sauce” | Keep earned imagery; remove metaphor standing in for information |
| Forced audience engagement | 20 | “consider this,” “let that sink in,” “have you ever wondered,” “you read that right” | Does the audience need this invitation? |
| Repetitive rhetorical structures | 6 | “not just X but also Y,” “less about X more about Y,” “not because X but because Y” | Test logical distinction; don't suppress genuine contrast |

The literal rules have exact IDs such as `empty_emphasis_001` for **“that matters”**. Regex rules have stable semantic IDs such as `contrast_not_just`, `contrast_not_because`, `empty_impact_claim`, and `generic_statement_of_value`. The catalog is machine-readable and versioned. Do not force an arbitrary rule count in future work; add or remove entries only with human-reviewed counterexamples and a compatibility note.

### A. Hot-phrase sample output and semantics

For the input:

```text
That matters. Studies show the innovation is a game changer.
But here's why: it will unlock the potential of every business.
```

The scanner creates objects of this shape:

```json
{
  "id": "empty_emphasis_001",
  "category": "empty_emphasis",
  "severity": "review",
  "line": 1,
  "column": 1,
  "start": 0,
  "end": 12,
  "excerpt": "That matters",
  "question": "What specific decision, consequence, or observation makes this important?"
}
```

**`severity: review` is not an error.** It means a person should assess the expression in context. **`severity: evidence`** means a claim such as “studies show” especially needs an attributable basis, not that the phrase alone proves anything false. The scan report includes `document_sha256`, `rules_sha256`, category counts, matching offsets, repeated rule IDs, and a bounded hit count. Those digests identify exactly which document and rules were reviewed.

### B. When not to “fix” a phrase

- “The number **that matters** in this filing is the net reserve after recapture.” The phrase can be legitimate if the sentence identifies the number and its reason.
- A direct interview quotation containing **“that matters”** may require verbatim retention. The default scanner suppresses common quotation spans and Markdown blockquotes; `--include-quotes` displays them when the editor requests a wider review.
- A scientific paper may correctly use “in summary” or “notably” as a needed signpost; it is not a hard ban.
- An executive message may use “bottom line” naturally as a decision cue. If approved by the author, retain it.
- “Not because of speed, but because the buyer rejected the incomplete evidence” is a meaningful causal distinction if the evidence supports it.

**Never inject grammatical errors, illogical transitions, arbitrary word substitutions, invented stories, or randomly alternating sentence lengths to defeat an AI detector.** Changes must earn their place through reader comprehension and author voice.

### C. Unicode, Markdown, and exact spans

Implementation detail: the scanner applies a **one-code-point-to-one-code-point Unicode translation** for curly apostrophes and dash variants before matching. It executes matches over translated text of equal length and reports **original code-point offsets** in the unchanged UTF-8-decoded source. It masks fenced code blocks, inline code, URLs, email addresses, and common quoted text. This is a deliberately bounded Markdown heuristic, not a CommonMark parser, and the doc says so. Multi-column, nested, indented, or exotic Markdown can still produce false positives; resolve them through human editorial review rather than claiming perfect parsing.

The scan caps text at **500,000 code points** and findings at **500**. If the result is truncated, the report sets `truncated=true`: **a truncated report is incomplete and cannot establish absence of issues**. Large manuscripts must be chunked by stable boundaries, with global offsets and document digests preserved.

### D. Why raw counts are not the objective

`density_per_1000_words` is a diagnostic count of matched expressions, **not** an AI probability, grade, or universal prose-quality score. A writer may lower the number while worsening the writing. Tracking the result is useful for a blind editorial study only if author acceptance, evidence fidelity, meaning preservation, and reader preference also improve. Do not reward deleting a phrase that was the author's own appropriate idiom.

## 21. Hard-code contract: rule pack and scanner

The ZIP accompanying this handoff contains the complete runnable code. Important contracts are reproduced here for an engineer implementing the next wave.

### `rules/v9_hotphrases.json`

```json
{
  "schema": "wi9.hotphrases/1",
  "version": "0.2.0-experimental",
  "owner": "Antonio T. Smith Jr.",
  "rules": [
    {
      "id": "empty_emphasis_001",
      "category": "empty_emphasis",
      "kind": "literal",
      "expression": "that matters",
      "severity": "review",
      "question": "What specific decision, consequence, or observation makes this important?",
      "context_note": "Not a claim of machine authorship; allow legitimate domain use and direct quotations."
    }
  ]
}
```

That example is a **schema illustration**, not the full rule pack. The actual file contains all 334 verified, compiled rules.

### `wi9_hotphrases.py` — essential API

```python
from wi9_hotphrases import read_rules, scan_text

rules = read_rules()                      # validates 334 trusted local rules
report = scan_text(source_text)           # returns editorial diagnostics, no rewriting
assert report['schema'] == 'wi9.hotphrases.report/1'
assert report['release_authorized'] is False
assert report['document_sha256']

for item in report['findings']:
    print(item['id'], item['line'], item['column'], item['excerpt'])
    print('EDITORIAL QUESTION:', item['question'])
```

### CLI commands

```bash
python3 wi9_hotphrases.py scan --input my_essay.md --format text
python3 wi9_hotphrases.py scan --input my_essay.md --format json > editorial_findings.json
python3 wi9_hotphrases.py scan --input my_essay.md --include-quotes --format text
```

**Python version:** stdlib Python 3.8+ is targeted; POSIX capability requirements apply to `wi9_core.py` bounded file opening. The phrase scanner itself uses no model, network, or external libraries. No developer should insert a model call or send author manuscripts to a remote system inside `scan_text()`.

## 22. New human review ledger — no silent deletion

A writing engine becomes less trustworthy when it silently converts every phrase match into a rewrite. V9 instead preserves decisions in a review ledger, tied to the exact document and exact rule catalog.

### Decision contract

```json
{
  "schema": "wi9.editorial.review/1",
  "document_sha256": "<64-lowercase-hex-from-scan>",
  "rules_sha256": "<64-lowercase-hex-from-scan>",
  "decisions": [
    {
      "rule_id": "empty_emphasis_001",
      "start": 0,
      "end": 12,
      "excerpt": "That matters",
      "status": "retain_as_written",
      "rationale": "This is the writer's intentional emphasis and the following fact makes the causal point explicit.",
      "reviewer": "Antonio T. Smith Jr.",
      "reviewed_at": "2026-10-27T21:00:00-05:00"
    }
  ]
}
```

Allowed dispositions: `retain_as_written`, `revise_for_clarity`, `needs_source`, and `not_applicable`. **The review ledger does not edit the manuscript.** It checks whether the targeted rule/span/excerpt exists in the original findings, validates pinned digests, rejects conflicting or duplicate targets, and requires a meaningful rationale, reviewer declaration, and date. It reports review coverage without equating review coverage with author approval or factual truth.

```bash
python3 wi9_phrase_review.py \
  --input my_essay.md \
  --report editorial_findings.json \
  --decisions editorial_review.json
# status REVIEW is still not RELEASE; stale source or rule digest => HOLD.
```

**Next necessary hardening:** validate timestamps as offset-aware ISO 8601 rather than nonempty strings; retain reviewer authority from the v6 grant system, not a name field; require all critical `needs_source` cases to be resolved before publication; support reproducible signed decisions; provide append-only supersession rather than mutable history; and test redaction/consent withdrawal.

## 23. Source-based composition engine — full sequence and interfaces

The composition code already provides a thin, model-neutral request/response contract. A production-quality v9 writing engine still needs a **real provider adapter** and a multi-stage compiler. Do not pretend a JSON request builder is a completed prose model.

### Required pipeline

```text
Author-provided material + publication contract
       |
       v
   [Intake / venue policy] -- human-only --> RESEARCH ONLY / HOLD
       |
       v
   [Source custody + exact hashes + scope/consent]
       |
       v
   [Canonical v5 claims / v6 authority & time]
       |
       v
   [Author thought inventory: thesis, friction, decision, consequence]
       |
       v
   [Source-based scene / argument plan]
       |
       v
   [Candidate composition, only if venue permits it]
       |
       v
   [Claim-span / quotation / temporal / meaning-delta checks]
       |
       v
   [334-rule phrase lint + structural slop review]
       |
       v
   [Real author voice review with consented comparison samples]
       |
       v
   [Human editorial decision and exact state approval]
       |
       v
   [v6 RELEASE authority gate, not an editorial score]
```

### Composition request constraints

`wi9_composition.py:prepare_request()` must continue returning `HOLD/HUMAN_ONLY_NO_GENERATED_PROSE` if venue policy is `human_only` **even when the intended use says internal review**. The intent of this conservative behavior is to eliminate a pathway by which the prohibited pitch is first generated and then relabeled as a research artifact. A separate `render_research_only()` can produce questions and an evidence inventory, not submission copy.

For an AI-permitted or appropriately disclosed venue, compose only through a typed request:

```python
from wi9_composition import prepare_request, inspect_candidate

req = prepare_request(dossier)
if req['status'] != 'REQUEST_READY':
    raise RuntimeError('No prose-generation permission: ' + req['reason'])

# A separately implemented, authorized provider may return typed candidate data.
# Never embed an API key or private author source in source control.
# candidate = authorized_provider.generate(req['request'])
# audit = inspect_candidate(candidate, req)
# assert audit['release_authorized'] is False
```

A candidate must contain `schema='wi9.candidate/1'`, an array of paragraph objects, IDs resolving to source cards, `author_review_required=true`, and verbatim quote references matching exact cited source text. Every paragraph is **provisional**. The validator deliberately stops at `DRAFT_REVIEW_REQUIRED` at best. The model or renderer does not get to issue `RELEASE`.

### Next composition APIs to implement

```python
# contracts only — DO NOT describe these as currently implemented

def extract_author_thoughts(source_atoms, author_notes) -> 'ThoughtInventory':
    """Human-source propositions only; require evidence ID per original idea."""

def build_argument_graph(thoughts, genre_contract) -> 'ArgumentGraph':
    """Each node needs claim, function, prerequisite, and expected reader effect."""

def generate_candidate(request, provider) -> 'CandidateDocument':
    """Provider runs only after venue/consent/cost checks, returns no release flag."""

def review_semantic_delta(original_claims, candidate_claims) -> 'DeltaReport':
    """Protect quantities, time, cause, uncertainty, subject and user position."""

def run_human_editorial_review(candidate, source_text, voice_profile) -> 'ReviewDecision':
    """Collect actual person-issued judgments, not a fabricated model pass."""
```

The returned type names are design interfaces, not existing imported modules. Build each behind explicit schemas and negative controls before integrating it into the canonical runtime.

## 24. Implementable model-provider isolation, cost and security

**Do not embed an LLM into evidence or publication code.** Define an asynchronous provider adapter in a separate service/process, but keep validation/gates deterministic and independent of provider trust. The model receives only appropriately scoped and redacted source cards. An off-network model is preferred for sensitive manuscripts; remote inference requires explicit consent and a documented retention/subprocessor policy.

### Typed provider boundary (design pseudocode)

```python
from dataclasses import dataclass
from typing import Protocol, Dict, Any

@dataclass(frozen=True)
class GenerationBudget:
    max_input_chars: int
    max_output_chars: int
    max_candidates: int
    cost_ceiling_usd: float
    deadline_seconds: float

class DraftProvider(Protocol):
    def generate(self, request: Dict[str, Any], budget: GenerationBudget) -> Dict[str, Any]: ...

class SafeCompositionCoordinator:
    def __init__(self, provider: DraftProvider, policy_gate, evidence_gate):
        self.provider = provider
        self.policy_gate = policy_gate
        self.evidence_gate = evidence_gate

    def propose(self, dossier, budget):
        permission = self.policy_gate(dossier)
        if not permission.allowed_to_generate_prose:
            return {'status': 'HOLD', 'release_authorized': False}
        proof = self.evidence_gate(dossier)
        if not proof.ready:
            return {'status': 'HOLD', 'release_authorized': False}
        proposal = self.provider.generate(proof.redacted_request, budget)
        return {'status': 'DRAFT_REVIEW_REQUIRED',
                'proposal': proposal, 'release_authorized': False}
```

The coordinator above is **design pseudocode**. It demonstrates that provider access happens *after* policies and evidence constraints. Implementations must also enforce JSON depth/size limits, timeouts, retries, idempotency tokens, per-tenant isolation, audit traces without PII, and strict schema validation. Provider output is untrusted, even when it looks like a citation or approval instruction.

### Security threat model

| Threat | Guard |
|---|---|
| Private author corpus leaking into prompts/logs | Scope-tagged source cards; opt-in remote transfer; no full source logging; local encryption and access controls |
| Prompt injection in retrieved research | Treat source text as data, never as executable instructions; source cards cannot carry tool grants |
| Dishonest “human-authored” flag | Explicit self-declaration status; no inferred verification; documentary contribution history |
| Unsupported first-person detail | Require original author source and source-to-claim mapping; HOLD if missing |
| Claim temporality drift | v6 valid time/knowledge time; planned/completed/measured states typed |
| Symlink/path traversal | Existing POSIX `openat`/`O_NOFOLLOW` strategy; continue to test portability and races |
| Catastrophic regex from untrusted rule | Only ship reviewed local regex pack; bounded input and rule count; do not accept remote regex updates |
| Stale approval on changed text | Bind document hash and rule pack hash; reject mismatches |
| Publishing from editorial tool | All lints return `release_authorized=false`; v6 grant-controlled release separate |
| Cross-tenant voice leakage | Per-tenant vault and voice profile; consent + hard resource partition |
| Detector gaming | No detector-based paraphrasing, artificial imperfection, or false author identity |

**Important limitation:** the `wi9_hotphrases.py` Markdown masker is heuristic; the POSIX source reader is not guaranteed on Windows. The reference package does not currently encrypt at-rest storage or implement multi-tenant identity and authorization. Those are mandatory gates before production use.

## 25. From source to genuinely distinctive writing — meaning-first editorial compiler

A realistic v9 compiler should **not** operate as “generate generic response → find 334 phrases → replace synonyms.” The correct order is:

**Pass 1 — Claim and experience intake.** Source `WHO/WHAT/WHEN/WHERE`, specific artifact, event, operator action, consequence, uncertainty, evidence citation. For personal essay samples, source material must originate with the author. A strategic roadmap is `planned`, not `performed`.

**Pass 2 — Thought topology.** Model real thesis, atypical premise, decision rule, disconfirming observation, competing explanation, cost of being wrong. For every paragraph, define its semantic job (`observation`, `mechanism`, `consequence`, `counterargument`, `qualification`, `turn`, `resolution`). Avoid mechanically creating a three-part structure just because the question has three parts.

**Pass 3 — Argument/scene order.** Determine whether the passage requires a narrated incident, technical explanation, quantitative evidence, concession, or direct conclusion. Remove sections with no downstream dependency. For fiction, scene changes must constrain character choices and produce aftermath—not atmospheric repetition.

**Pass 4 — First candidate.** Compose only in eligible arenas. Write from actual source cards, preserve specificity and contradictions. Every paragraph carries evidence IDs and the model's own disclosed state as a proposal.

**Pass 5 — Claim integrity.** Compare against canonical source; inspect entity, quantity, timeline, speaker, completion status, cause and uncertainty. First-person claims without accepted supporting author material => HOLD. Quote precision checks are necessary but not proof of semantic entailment.

**Pass 6 — Editorial lint.** Run 334 hot-phrase rules, repetitive openings, hollow contrast detection, paragraph template symmetry, repeated ideas and abstract noun density. Each alert must present *why* the sentence might be weak and what evidence would make it stronger.

**Pass 7 — Author voice fidelity.** Compare to at least three genuinely human-origin, consented samples per genre. Voice-match statistics are secondary to the author's explicit approval of intent, rhetoric, and position. A model cannot independently certify origin by imitating that style.

**Pass 8 — Human decision.** The author sees before/after and accepts/rejects semantic edits, not just copyedits. Retained hot phrases are logged as legitimate when they serve the genre. For human-only venues, compose the external message personally with no forbidden model authorship.

**Pass 9 — Release gate.** External publication requires venue compliance, verified scope of authority, source status, editorial approval, exact document digest, and explicit approval. A stylistic “green” report alone never permits sending.

## 26. Two evaluation tracks that must never be confused

### Track A — Deterministic source and eligibility integrity

Goals: correct file reading, stable digests, unique claim IDs, venue gate consistency, exact quote spans, provenance declarations, source freshness and held state when required. **Unit tests** are appropriate for these properties.

### Track B — Reader and author-assessed writing quality

Goals: preserve author belief, make concrete choices visible, avoid meaningless repetition, deliver useful narrative consequence, express appropriate emotion and rhythm, and remain original without invented facts. Use **actual blinded editors and the source author**. Statistical syntax features and rule counts provide diagnostic clues; they cannot certify naturalness. Pre-register evaluation criteria and do not revise them after seeing scores.

For the planned **60-case** study (15 each in journalism, executive correspondence, fiction, and technical/institutional writing): randomize presentation; compare genuine original, v8 baseline, v9 candidate, optional manual revision. Reviewer panels must record both preferences and reasons. Report paired-case outcomes, medians, distributions, author vetoes, consequential factual changes, and confidence intervals where justified. Make an explicit `FAIL` finding if v9 prose is more pleasant but introduces more unsupported facts or misrepresents the author's intent.

**Do not claim “10/10” as an outcome before those evaluations.** A 10/10 engineering handoff is one with concrete testable specifications, a runnable implementation floor, and an explicit path to evidence—not an invented benchmark score.

## 27. Expanded implementation plan: exact subwaves inside WI9-05

The parent project still uses `WI9-00`–`WI9-09`. These are **subtasks of WI9-05**, not new shipped waves or a competing status registry.

| Subwave | Deliverable | Hard acceptance |
|---|---|---|
| WI9-05A | Checked-in 334-rule catalog and schema | All rule IDs unique; no invalid patterns; examples + legitimacy counterexample per category |
| WI9-05B | Portable editorial scan CLI with digests/offsets | Unicode locations exact; code/quote masking; bounded inputs; 0 model/network calls |
| WI9-05C | Repetition and structural diagnostics | Duplicate turns, hollow contrast, conclusion template; category outputs reviewable |
| WI9-05D | Author-specific false-positive judgments | Decisions bound to immutable source/rules digests; no automatic suppression without reviewer authority |
| WI9-05E | Source-based composition contract | Human-only venue refusal; source cards and quote checks; all outputs review required |
| WI9-05F | Meaning/causality/voice evaluator | Held-out genuine voice corpus; paragraph claim links; no author thought reversal in fixtures |
| WI9-05G | Independent reader preference trial | Predefined blinded assessment, actual scored sample with rationale, critical integrity invariants preserved |

**Reference implementation status:** 05A, 05B and portions of 05C–05E have local prototype code/tests. 05F and 05G **are not implemented or measured**. In particular, the new phrase scanner has *not* been merged into the canonical release or GitHub PR, so 05A/B are not `SHIPPED` regardless of local tests.

## 28. Integration recipe for the repository — controlled, non-destructive

Work in a new implementation branch from the reviewed draft PR head. **Do not merge, release, rebase an uninspected dirty tree, or overwrite current production files.** Keep the local package available as a separate artifact for reproduction before copying source into GitHub.

```bash
# ASSUMES owner has cloned the repository and possesses the reference ZIP.
cd ~/Documents/Codex/writing-intelligence

git fetch origin --prune
git switch proposal/v9-authentic-voice-provenance-20261027
# Ensure status is clean and inspect the actual current SHA.
git status --short
git rev-parse HEAD

git switch -c feat/wi9-05-meaning-led-editorial-lint
mkdir -p prototypes/wi9
# Extract reference ZIP into a separate temporary path, then copy files into prototypes/wi9.
# Example after extracting ZIP:
cp -R /tmp/WI9_OWNER_HANDOFF_REFERENCE/. prototypes/wi9/

python3 -m unittest discover -s prototypes/wi9/tests -p 'test_*.py' -q
bash tests/v7/test_wi7.sh
bash scripts/test-v8.sh
python3 scripts/check-manifest.py
bash scripts/build-skill.sh --check

git diff --check
# Inspect before staging. Do not silently modify v8 release files.
git status --short
```

The ZIP folder may be extracted elsewhere; change `/tmp` to the actual extraction directory. For canonical integration, move only features whose policies and tests are accepted into a versioned `scripts/` or extension module; keep the optional lint module importable from a feature-specific entry point until the Python 3.8, bundle-size, and CLI packaging contracts are verified. **Do not simply import a prototype's `REVIEW` into `wi.py` as `RELEASE`.**

### CI addition — prototype reference lane

```yaml
name: WI9 Reference Kernel
on:
  pull_request:
    paths:
      - 'prototypes/wi9/**'
      - '.github/workflows/wi9-reference.yml'
permissions:
  contents: read
jobs:
  negative-controls:
    runs-on: ubuntu-22.04
    strategy:
      fail-fast: false
      matrix:
        python: ['3.8', '3.11', '3.13']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - name: Local reference tests
        run: python -m unittest discover -s prototypes/wi9/tests -p 'test_*.py' -v
```

The lane above is a proposed integration file, **not** a claim that it already exists in GitHub. Before merging, CI needs negative-control mutation testing (deliberately disable a hold guard and require test failure), source-corpus redaction, and reproducible bundle verification.

## 29. Exact technical debt — do not ignore these just because 81 tests pass

1. **Authorship remains self-declared.** This is necessary and honest; do not rename a review state `VERIFIED HUMAN`.
2. **Claim coverage is incomplete.** Existing preflight checks supplied claims and links, not exhaustive discovered claims; the original v4/v5 claim extraction must supply coverage and human adjudication.
3. **Semantic entailment is not implemented.** Exact quote matching cannot prove the paraphrase is true.
4. **Text-generation backend is missing.** The source-constrained request/response contract is ready for integration work, but no actual prose provider is attached in the reference package.
5. **Voice matching lacks genuine controlled corpus.** Existing profile statistics are diagnostic only. Need consented authentic samples and held-out blind reader comparison.
6. **Phrase scanner Markdown parsing is heuristic.** More complete CommonMark handling or a proven package is needed for highly complex documents, if the dependency policy allows it.
7. **Python regex lacks guaranteed timeouts.** Accept only reviewed trusted local rules; for user-custom patterns use a safe regular expression engine with a time budget or refuse untrusted regex.
8. **Bounded scanner's 500-hit truncation is incomplete.** For full manuscripts, run stable chunking and aggregate offsets, then expose incomplete scans honestly.
9. **Reviewer identity is not authenticated.** Self-entered name is a declaration; v6 grants must govern publishing decisions.
10. **Review timestamps are merely nonempty in the prototype.** Validate offset-aware ISO-8601 and sequence them against the current document and policy versions.
11. **Local file safety is platform-specific.** `wi9_core.py` fails closed when secure POSIX flags are absent; ship a separate verified Windows strategy or document unsupported Windows behavior.
12. **No privacy vault exists.** Production requires encryption, tenant ACLs, consent/withdrawal, retention and secure deletion policies.
13. **Not all phrase scan false positives have been measured.** Need a reviewed sample across genres; a false-positive phrase alert must not lower an author's score automatically.
14. **No canonical v9 packaging is installed.** Current reference scripts sit outside `scripts/wi.py`, v9 manifests and three v8 skill bundles. Preserve the existing release boundary.
15. **No independent prose-quality uplift exists yet.** Benchmarks proposed, not run. Detector score changes are neither ground truth nor a substitute.
16. **The 334 rules require ongoing maintenance.** Track rule changes with actual author/editor feedback. Expansion for its own sake can degrade specificity and readability.
17. **False permission claims must remain impossible.** `REVIEW`, `DRAFT_REVIEW_REQUIRED`, and `RESEARCH_ONLY` never confer `submit` or `publish` authority.
18. **Model-source injection and indirect instructions are unresolved in the provider contract.** Treat all retrieved source cards as untrusted and forbid them from altering the tool/sending policy.

## 30. New acceptance and negative controls for hot phrases

Every positive fixture should have a **legitimate counterexample**. A scorer that flags all occurrences as “AI” is defective; a system that deletes them on sight is also defective.

| Test | Input | Expected behavior |
|---|---|---|
| Literal match | `That matters.` | `empty_emphasis_001` reported with exact offset |
| Lower/upper case | `THAT MATTERS` | Same rule ID, original uppercase excerpt preserved |
| Morphology boundary | `Whatever matters ...` | Not matched as `that matters` |
| Curly punctuation | `Here’s the thing` | Match via one-to-one Unicode normalization; span maps to original |
| Verbatim quote | `She said “that matters.”` | Suppressed by default, visible with `--include-quotes` |
| Source blockquote | `> That matters.` | Suppressed by default, visible if requested |
| Inline/fenced code | `` `that matters` `` | Suppressed as code/data, including when quotes are requested |
| Genuine context | `That matters because the invoice was 32 days late.` | Review alert, **not** automatic rewrite |
| Vague authority | `Studies show ...` | `evidence` review; exact source required before strengthening |
| Fake opposition | `It's not just X, but also Y` | Structure inspected for real distinction |
| Repetition | `That matters` repeated three times | Stable same-ID count, no invented origin classification |
| Large input | More than 500,000 code points | Deterministic refusal |
| Too many matches | More than configured cap | Explicit `truncated=true` |
| Edited manuscript | One changed byte after review | `DOCUMENT_STALE` / `REVIEW_DOCUMENT_STALE` HOLD |
| Edited rule catalog | Changed rule digest after review | `REVIEW_RULESET_STALE` HOLD |
| Faked reviewed occurrence | Wrong span/excerpt/rule ID | `DECISION_TARGET_UNKNOWN` HOLD |
| Duplicate decisions | Same finding approved twice | `DECISION_DUPLICATE` HOLD |
| Missing judgment | Empty rationale, reviewer/date absent | HOLD |
| Attempt to publish from linter | Any lint status | `release_authorized=false` always |

**Observed local result:** All existing 44 original reference tests plus new scanner/review coverage produced **81 passing tests** in this working session. That count does not replace GitHub's separate 16-test prototype and does not prove 334 individually annotated rules were independently judged by humans. The suite validates catalog integrity and representative cases.

## 31. Engineering quality review — how to get from 4/10 to an actually excellent product

The previous version put governance first and deferred the writing engine. That explains why it was inadequate as a complete authoring upgrade: a source checker is not a prose compiler. The corrected emphasis is:

| Requirement | Earlier gap | v9 addition | What must still be proved |
|---|---|---|---|
| Concrete authorial specificity | Generic first person and examples | Firsthand source cards + author interview contract | No unsupported personal scenes across full corpus |
| Rhetorical individuality | Polished, generic transitions | Author voice baseline; hot phrase and argument diagnostics | Held-out author preference, per genre |
| Repeated AI-style formulas | Limited phrase lint | 334-rule versioned context-aware phrase taxonomy | Precision/false-positive rates from real editor annotations |
| Meaning preservation | Claim anchors alone | Thought inventory and semantic diff design | Regression fixtures for opinion reversal, source promotion, causality |
| Full composition | Missing | Typed candidate-generation contract | Integrated provider and independent evaluation, no policy bypass |
| Editorial release | Only limited review | Digest-bound review ledger and hard human-only holds | Real v6 grants and independent recipient-side validation |
| Evidence of improvement | None | 60-case randomized blind study protocol | Collected samples, reviewer results, honest failure accounting |
| Developer reproducibility | Design-only | Runnable Python ZIP + tests + exact commands | New branch CI and fresh extraction tests |

**Expected outcome after completing this plan:** Writing Intelligence can generate eligible prose from real source material, preserve the author's intended beliefs and voice, provide exact evidence trails, identify generic phrasing without destructive automation, and submit only when the publication policy and actual human authority permit it. **This is a target, not a claim already achieved.**

## 32. Handoff checkpoint and next-session prompt

**Exact GitHub state at verification:** Draft PR #8 remained open and mergeable at `80e7aef88441c2f2e9eb5734b43b601924592dac`, with full baseline CI and v9 prototype workflow both green. That reflects GitHub only, **not the new local reference package**. The local code can be transported through the companion ZIP; record its file SHA-256 before adding it to a feature branch.

**Resume in this order:** (1) extract the companion ZIP, run all 81 local tests; (2) compare the current GitHub PR and SHA; (3) implement WI9-00/P0 input, source, and authorship hardening; (4) add experimental scanner and review ledgers under `prototypes/wi9` with CI; (5) finalize source, thought and voice contracts; (6) implement a genuinely source-constrained composition adapter for eligible venues; (7) evaluate the actual 60-case human quality trial; (8) integrate with `wi.py` and v6 scoped authority only after negative tests and owner acceptance; (9) rebuild packages/receipts and release only on fresh independent proof.

**Continuation instruction:** Continue the implementation of Writing Intelligence v9 for Antonio T. Smith Jr. Use the original complete handoff, this expansion, the companion `WI9_OWNER_HANDOFF_REFERENCE` source tree, and current GitHub PR #8. Do not repeat repository-wide discovery without a named unknown; compare exact current SHAs first. Preserve v8 and prior source semantics. Extend the 334-rule phrase pack only with judged examples and negative controls. Implement the missing author-thought/voice and model-neutral composition stages. Keep `human_only` publication gates closed to AI prose. Do not optimize for a detector score or claim human authorship for machine prose. Tests alone do not constitute a writing-quality pilot or permission to merge. Record actual work, errors, exact commits, SHA digests, reviewer decisions, and next actionable checkpoint. Project author: Antonio T. Smith Jr. No co-author trailers.

**Final state of this expansion:** Runnable offline v9 experimental reference kernel + **334 editorial hot-phrase rules** + **81 local tests PASS**; GitHub v9 PR #8 remains a separate unmerged proposal; **v9 release HOLD** pending voice, thought, composition, editorial trials, canonical integration, and owner approval.
