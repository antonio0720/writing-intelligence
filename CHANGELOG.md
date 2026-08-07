# Changelog

All notable changes to Writing Intelligence are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Semantic versioning per `governance/VERSIONING.md`.

---

## [5.0.0] — 2026-08-07 — **Proof-Carrying Authorship OS**

### The Leap

v1.0 proved AI-sounding prose can be defeated by compilation instead of cosmetic cleanup.
v2.0 proved fiction can be engineered as a living architecture.
v3.0 proved authorship can be governed without being flattened.
v4.0 proved it can be held accountable.
**v5.0 proves the account can be carried, checked and re-checked by someone who was never in the room.**

v4 verifies a document at a moment. v5 keeps the verification bound to the things it depended on, so an edit made three weeks after a check cannot quietly inherit the check's result — and packages the whole account into an artifact a stranger can verify offline, with no model and no network.

**The v5 law:** *A reader can point at any sentence, number or quotation and ask why it is here, what supports it, what depends on it, and what breaks if it changes — and another machine can independently verify the answer.*

The v4 layer is preserved in force. Laws A through F are unchanged; v5 adds Laws G through L above them, in `references/v5/CONSTITUTION.md`.

### Added

**Six new system laws — G through L** (`references/v5/CONSTITUTION.md`)
- **Law G** — Meaning has identity independent of wording *(claim atoms executable; the full concept registry specified)*
- **Law H** — Every consequential transformation declares its semantic delta *(executable)*
- **Law I** — Verification is dependency-aware *(executable)*
- **Law J** — Human decisions are first-class artifacts *(specified)*
- **Law K** — One proof engine, many surfaces *(the canonical core is `scripts/wi.py`; no second implementation exists)*
- **Law L** — A release must be explainable without trusting the model that helped create it *(bundle build and offline verification executable; judgment records specified)*

**`scripts/wi.py` — the deterministic core, now 5.0.0**
Still one stdlib-only file, still Python 3.8+, still no dependencies, no network, no model, no telemetry. About 3,500 lines. Twelve new subcommands beside the five it already had, for seventeen in total.

- `init` — create a `.wi/` workspace: a SQLite index, a content-addressed object store under `.wi/objects/sha256`, a `wi.project.yaml` and a `wi.lock`
- `ingest` — content-address sources. **Raw bytes are hashed before any normalization**, so an extractor upgrade is a separate, visible change rather than a silent digest shift. Each distinct byte state becomes an immutable `source.version`
- `atomize` — split sentences into independently checkable claim atoms. A compound sentence asserting three things becomes three atoms, verified separately, invalidated separately, repaired separately. Each atom carries a structured proposition: quantity, unit, temporal scope, modality, negation, attribution, entities, realm
- `anchor` — bind atoms to evidence anchors with byte offsets and quote digests, then run the deterministic check set. `text_span` only; the other six anchor kinds are specified and are reported as unavailable rather than approximated
- `graph` — the authorship graph. Node families `source.artifact` · `source.version` · `source.segment` · `meaning.claim_atom` · `structure.paragraph` · `structure.work` · `verification.result`; edge relations `asserted_in` · `depends_on` · `derived_from` · `supports`. Every node carries **two identities**: a content-derived logical id and an immutable state digest
- `impact` — staleness and the **minimum repair frontier**. A changed source reports exactly which anchors, atoms, paragraphs, documents and verification records it broke — **and how many it provably did not** — plus a costed repair plan. The provably-unaffected count is the load-bearing half: a checker that turns the whole document red on every save is one somebody switches off
- `diff --semantic` — deterministic semantic diff over the Law H axes. `may reduce → reduces` classifies as `certainty_strengthened`; `11,800 → 12,400` classifies as `quantity_changed`; each change states whether existing proof carries forward. Paraphrase equivalence is not evaluated and the output says so
- `test` — writing tests as declarative rules over graph state: evidence coverage **with a visible denominator**, forbidden terminology, concept-registry drift with named forbidden aliases, required sections, orphan citations
- `bundle` — build a `.wiab` proof-carrying release in three profiles: `full` (source bytes travel), `hash-only` (digests only; a reviewer who does not hold the sources cannot inspect them, and the manifest says so), `redacted` (excerpts, no source blobs)
- `verify-release` — verify a `.wiab` **offline, with no model, on a machine that has never seen the workspace**, by recomputing every digest. Eleven checks: archive integrity, bundle completeness, manifest format, object digests, release artifact digest, graph reference integrity, proof dependencies, stale closure, manifest counts, core version, signature *(skipped — unsigned)*. A tampered artifact is rejected with `WI_RELEASE_TAMPERED`
- `explain path:line` — why this sentence is here: class, status, realm, extracted quantity and temporal scope, every anchor with byte range and quote digest, every check with its result and reliability type, and what depends on it
- `doctor` — capability negotiation. Reports the eleven available deterministic checks, the one available anchor type, and the seven capabilities that are **not** available here with a reason for each. Law C as protocol
- `preserve` — unchanged in behaviour, now workspace-aware

**A new claim status: `span_supported`**
Every checkable component of a claim was found co-located inside **one span of one source**. It is distinct from `supported` (verbatim presence of the claim itself) and distinct from `candidate_support` (components found, but scattered across the corpus). Whether that span *entails* the sentence is a judgment-tier question, and the output says it was not evaluated. This status exists because collapsing it into `supported` overstates and collapsing it into `needs_source` understates, and both errors are silent.

**Canonical serialization and domain-separated digests** (`references/v5/CANONICAL_HASHING.md`)
- RFC 8785-shaped canonical JSON: NFC, sorted keys, no insignificant whitespace
- Two digests per object — a content digest and a domain-separated state digest under `wi-state-v5`, with the schema identifier and schema version inside the preimage
- Error taxonomy with a repair route on every code: `WI_INPUT_INVALID` · `WI_SOURCE_UNREADABLE` · `WI_SOURCE_VERSION_MISSING` · `WI_GRAPH_INTEGRITY` · `WI_RELEASE_TAMPERED` · `WI_BUILD_FAILED` · `WI_DIR`

**The `.wi/` workspace** (`references/v5/WORKSPACE.md`)
SQLite index, content-addressed object store, `snapshots/`, `graph/`, `decisions/`, and a `wi.lock` that pins the core version and every ingested source digest.

**Twenty doctrine documents** — `references/v5/`
CONSTITUTION · NON_GOALS · RELIABILITY_TYPES · AUTHORSHIP_GRAPH · SEMANTIC_IR · EVIDENCE_ANCHORS · CANONICAL_HASHING · CONCEPT_REGISTRY · SEMANTIC_DIFF · STALENESS · JUDGMENT_TIER · PROOF_CARRYING_RELEASE · POLICY_AS_CODE · WORKSPACE · STORYWORLD_OS · MULTIMODAL · RIGHTS_AND_CONSENT · SECURITY_MODEL · ARCHITECTURE · SURFACES, indexed by `references/v5/README.md`.

Every section of every one of them carries one of exactly two status markers on its first line: **executable in `scripts/wi.py`** or **specified**. No document in that directory describes a capability as though it ships when it does not.

**Fifteen JSON Schemas** — `schemas/v5/`
`claim_atom` · `concept_registry` · `decision` · `evidence_anchor` · `graph_edge` · `graph_node` · `invalidation` · `judgment_record` · `policy` · `proposal` · `release_manifest` · `source_artifact` · `source_version` · `verification_record` · `workspace`. The v3 schemas are unchanged and remain valid under their own namespace.

**Eight new permanent refusals** (`references/v5/NON_GOALS.md`)
No hosted-account dependency · no proprietary-model dependency · no vector database as the truth layer · no blockchain · no public transparency log by default · no autonomous source approval · no automatic legal or medical adjudication · no claim of invention over prior art. The v4 refusals carry forward unchanged. Embeddings are candidate retrieval and never evidence: a similarity score may not appear in a proof record, and would happily rank 11,800 as support for 12,400 — the exact fixture this project ships to prove the point.

**Tests**
- `tests/v5/test_wi5.sh` — 32 checks, each with a negative twin. A tampered bundle must be rejected *for the right reason*; an unchanged sentence must **not** be reported as a change; a concept registry that cannot fail is decoration
- `tests/v5/world/` — a full worked fixture: two sources, two draft revisions, a tests file, a concept registry
- `tests/v5/EXPECTED_TRANSCRIPT.txt` — a real end-to-end session, command by command
- `tests/v4/test_wi.sh` — the 3-check v4 adversarial suite, unchanged and still required to pass

**Documentation**
- `docs/MIGRATION_v4_to_v5.md` — staged adoption path in six steps
- `docs/INSTALL.md` extended to eight surfaces with a v5 capability matrix
- `release/RELEASE_NOTES_v5.0.0.md`

### Changed

- **`scripts/wi.py` reports version `5.0.0`.** Release tooling checks the tag, `wi.py --version` and the `CHANGELOG.md` heading against one another, so this is a breaking version for anything that pinned the string
- **`gate` accepts both ledger shapes.** A v4 sentence ledger and a v5 atom ledger are both valid input. The output adapts: sentences and claim counts for the former, claim atoms plus a stale-node count for the latter. Existing CI jobs and git hooks keep working with no edit
- **`gate --mode` now defaults to the project's `evidence.default_mode`** instead of `standard`. Where there is no project file, the default is still `standard`. **This is a behaviour change for anyone who ran `gate` inside a workspace and relied on the old implicit default** — a project initialized with `--mode strict` now gates at `strict` without the flag
- **The claim status vocabulary gained `span_supported` and `candidate_support`.** Anything consuming the status strings must handle both. `span_supported` counts toward evidence coverage; `candidate_support` holds the gate
- **`preserve` writes into `.wi/snapshots/` when a workspace exists**, rather than beside the file. Outside a workspace the v4 behaviour is unchanged
- **The verification unit is the claim atom, not the sentence.** A sentence asserting three things used to get one status, which meant an author told `needs_source` could not tell which third of their sentence failed
- Reliability types are now enforced types in the record format rather than adjectives in a report: `verified` · `measured` · `judged` · `human-declared`. They never collapse into one score, and a judgment can never emit a `verified` record
- `references/v5/` supersedes nothing in `references/v4/`; the v4 documents remain the normative text for Laws A through F

### Fixed

Pre-release testing of the v5 core caught and fixed six defects. They are recorded because a release that only lists what was added is describing a system nobody stress-tested.

- **YAML flow-mapping crash in `wi test`.** The minimal stdlib YAML reader did not handle inline flow mappings, so a tests file written with `{ }` syntax aborted the run instead of parsing it. A test harness that crashes on valid input reports nothing, which is the most dangerous output it has
- **Source-version state digests were conflated with raw blob digests.** A `source.version` node was being identified by the digest of its bytes rather than by its own domain-separated state digest. Two objects that mean different things must not share an identity, and version identity is what every staleness computation walks
- **Anchors bound to the artifact instead of the version.** An anchor that points at a source *artifact* cannot go stale when the artifact's bytes change — it points at a name, not a state. This defeated Law I at its root and is the single most consequential of the six
- **Schema identifiers inside the digest preimage were inconsistent** between the write path and the verification path, so a digest recomputed by `verify-release` could disagree with the one recorded at build time for an untampered bundle. A verifier that fails on honest artifacts is as useless as one that passes on dishonest ones
- **`realm` mislabelled inferences as rhetorical.** Atoms classified `inference` fell through to the `rhetorical` default, which removes a claim from checking entirely — an inference about the world is an `external_fact` realm claim whose support is reasoning, not a figure of speech
- **`wi test` miscounted unavailable tests.** Assertions that could not run were being counted in the passed total. An unimplemented assertion is `unavailable`, never a pass and never a fail; reporting it either way is the exact confusion Law C forbids

### Deprecated

Nothing is removed in 5.0.0. Two things are superseded and will keep working:

- **The sentence as the verification unit.** `extract-claims` and `verify` still operate on sentences and still ship. New work should use `atomize` and `anchor`, which produce atoms with persistent identity inside a workspace. There is no converter and none is needed — re-run `atomize` on the draft; the old `claims.json` is not consumed, migrated or deleted
- **Standalone `claims.json` ledgers outside a workspace.** Still valid input to `verify` and `gate` forever, but nothing outside a workspace can be dependency-aware, so a ledger with no workspace cannot go stale and cannot be bundled

`services/api/` remains the **v3 craft kernel** and still does not expose the accountability or proof tier. That is Law K, not an oversight.

### Not yet implemented

Specified in this repository, normatively described, and **not executable anywhere**. Each is labelled at the point of description, and `wi doctor` reports the live list on any machine.

- **A compiled Rust/WASM core.** Nothing in this release is written in Rust. Every `crates/` path in `references/v5/ARCHITECTURE.md` §4 is a target, not a directory that exists
- **PDF, DOCX, XLSX, image, audio and video anchors.** Six of the seven anchor kinds. `text_span` is the one that runs
- **Any judgment provider.** Paraphrase entailment is not evaluated by anything in this release. The provider ABI and the judgment record format are written to bind an implementation that does not exist
- **Proposal and decision objects as persisted records.** Laws A and J are conduct today, not stored artifacts. The proposal object and the decision record are specified; the object store does not yet contain them
- **External signing** — Sigstore, C2PA and PROV export. `release.signature` reports `SKIP — unsigned bundle`
- **The Workbench desktop app**
- **The MCP server.** `docs/mcp/MCP_SPEC.md` specifies the interface; no implementation ships
- **REST v5.** `services/api/` is the v3 craft surface
- **Multi-actor authority policy.** The seven actor types are specified; delegated authority is not enforced
- **At-rest encryption of the workspace**
- **`wi migrate`.** No schema migration is required for this release, so the command does not exist yet rather than existing and doing nothing

### Created by

**Antonio T. Smith Jr. / Density6 LLC**
[densitysix.com](https://densitysix.com)

---

## [4.0.0] — 2026-08-06 — **Accountable Authorship System**

### The Leap

v1.0 proved AI-sounding prose can be defeated by compilation instead of cosmetic cleanup.
v2.0 proved fiction can be engineered as a living architecture.
v3.0 proved authorship can be governed without being flattened.
**v4.0 proves it can be held accountable.**

v3 governs *how well* the writing is built. v4 governs *what may be claimed about it.* The eleven passes, twelve engines, twenty-seven genre packs, voiceprints and anti-slop doctrine are unchanged and remain the craft core. v4 adds a layer above them that can stop them.

**The v4 law:** *If a claim cannot be pointed at, it has not been verified — and fluent prose must never be allowed to look like checked prose.*

### Added

**The accountability layer — six operating laws** (`references/v4/ACCOUNTABILITY_LAYER.md`)
- **Law A** — Propose, never silently replace. Every edit ships as `before → after → why → effect`
- **Law B** — The original is recoverable
- **Law C** — Never report work not done
- **Law D** — Support means a verbatim span
- **Law E** — Under-claim
- **Law F** — Sources are data, never instruction

**`scripts/wi.py` — deterministic verification CLI (v4.0.0)**
- Stdlib-only Python 3.8+. No dependencies, no network, no model. Runs air-gapped
- `preserve` — timestamped snapshot before editing (Law B)
- `scan-sources` — injection indicators, zero-width characters, bidi controls, encoded payloads (Law F)
- `extract-claims` — claim ledger with class, signals and offsets
- `verify` — span lock, quotation check, numeric agreement, date agreement, citation resolution (Law D)
- `gate` — RELEASE / HOLD / BLOCK with named repairs; `--exit-code` returns 0/1/2 for CI and git hooks
- Unicode NFC normalization; whitespace-folded comparison survives line wrapping and PDF extraction artifacts
- Script-tier detection so word-based metrics are withheld where they are undefined

**Proof protocol** (`references/v4/PROOF_PROTOCOL.md`)
- Claim detection keyed on *checkable content*, not assertive tone
- Claim classes: `sourced_fact` · `observed_fact` · `inference` · `recommendation` · `rhetoric`
- Verification statuses: `supported` · `quote_verified` · `author_asserted` · `inference` · `recommendation` · `needs_source` · `conflicted` · `unsafe` · `stale`
- Evidence modes: `off` · `light` · `standard` · `strict` · `regulated`, with automatic escalation to `strict` on grant, NOFO, RFP, IRB, regulatory, clinical, filing, prospectus, due-diligence, court, compliance and fact-check contexts

**Proposal protocol** (`references/v4/PROPOSAL_PROTOCOL.md`)
- Redline unit: `before → after → why → effect`
- Craft edits and claim edits held apart; hedge removal is always a claim change

**Source hygiene** (`references/v4/SOURCE_HYGIENE.md`)
- Prompt-injection defense on supplied documents
- Quarantine on imperative-to-system text, role markers, verification overrides, suppression instructions and invisible text
- Conflicts between two supplied documents surfaced *before* writing, not after submission

**Language tiers** (`references/v4/LANGUAGE_TIERS.md`)
- Tier 1 space-delimited · Tier 2 CJK · Tier 3 no word boundaries
- An unavailable metric is reported unavailable, never faked with an English-shaped substitute

**Voice and consent** (`references/v4/VOICE_CONSENT.md`)
- Five bases for modeling a named person's voice; three unrestricted
- Consent basis required before building a voiceprint from samples attributable to a real, identifiable person

**Surfaces** (`references/v4/SURFACES.md`)
- Chat, Cowork and Claude Code capability matrix; output shaped to what the surface can actually do
- Surface detected from available tools rather than by asking

**Non-goals** (`references/v4/NON_GOALS.md`)
- Detector evasion, source generation, truth verification and absolute quality scores stated as explicit refusals

**Tests**
- `tests/v4/` adversarial fixture: inflated figure, reshaped quotation, fabricated citation, prompt injection with zero-width characters
- `tests/v4/test_wi.sh` regression suite

**Documentation and distribution**
- `docs/INSTALL.md` — six install surfaces with a capability matrix, CLI reference, git-hook and CI recipes, troubleshooting
- `docs/MIGRATION_v3_to_v4.md` — staged adoption path
- `scripts/build-skill.sh` — reproducible skill bundle build
- `.github/workflows/ci.yml` — verifier regression, API tests and bundle build on every push
- `.github/workflows/release.yml` — bundle and checksum attached to every tag

### Changed

- Reliability language: `verified` / `measured` / `judged` replaces confidence percentages. **A percentage is never attached to a judgment with no denominator**
- Default edit return is a proposal set rather than a rewritten document. The clean rewrite is still available on request
- `README.md` rewritten as the v4 front door
- `CHEATSHEET.md`, `USER_GUIDE.md`, `ROADMAP.md`, `CONTRIBUTING.md` updated for v4
- Genre pack count corrected to 27 (previously documented as 26)

### Unchanged

The 11-pass kernel · 12 engines · 12 agents · 11 JSON schemas · 27 genre packs · voiceprints · benchmark harness · gold outputs · `services/api` REST runtime.

**No schema version bump. No field changes. Every v3 workflow still runs.**

### Deliberately not done

`services/api` still implements the **v3 craft kernel** and does not expose the v4 accountability tier. That tier has exactly one implementation — `scripts/wi.py` — and it stays that way. Two implementations of a verification rule drift, and the one that drifts is invisible because both look correct until they disagree about something that matters.

---

## [3.1.0] — 2026-05-27 — **REST Reference Runtime**

### Added

- `services/api/` — containerized TypeScript reference runtime for the v3 craft kernel
- Routes: `compile` · `score` · `voice` · `benchmark` · `repackage` · `manifest`
- Deterministic kernel with banned-phrase detection, claim scanning and voice metrics
- Per-tenant auth, rate limits, input sanitization
- Test suite: kernel, determinism, banned phrases, epistemic, voice, benchmark
- Dockerfile and deployment configuration

---

## [3.0.0] — 2026-05-26 — **Sovereign Writing Operating System**

### The Leap

v1.0 proved AI-sounding prose can be defeated by compilation instead of cosmetic cleanup.
v2.0 proved fiction can be engineered as a living architecture.
**v3.0 proves authorship can be governed without being flattened.**

Writing Intelligence v3.0 is no longer only a writing skill. It is an operating system for producing, auditing, scoring, preserving, and deploying high-integrity writing across genres, voices, teams, products, and longform worlds.

### Added

**11-Pass Governed Kernel**
- Pass 0: Intake Contract — every request becomes a governed task object
- Pass 1: Mission Lock — preserved from v2.0, extended
- Pass 2: Corpus & Context Ingestion — source governance, prevent hallucination
- Pass 3: Diagnostic Scan — preserved from v2.0
- Pass 4: Architecture Compile — section / scene / argument graphs
- Pass 5: Evidence & Epistemic Ledger — claim classification, source status
- Pass 6: Sentence Surgery — preserved from v2.0, now logged
- Pass 7: Voice Restoration — preserved from v2.0, now measurable
- Pass 8: Genre & Arena Alignment — arena delivery bundles
- Pass 9: Adversarial Stress Battery — extended interrogation
- Pass 10: Score & Delivery Packaging — multi-format output
- Pass 11: Memory & Benchmark Update — regression discipline

**12 Engines**
- Intake Contract Engine
- Corpus Governance Engine
- Voice Fingerprint Engine
- Genre Stack Engine
- Architecture Graph Engine
- Epistemic Ledger Engine
- Prose Compiler Engine (v3)
- Narrative Intelligence Engine
- Arena Delivery Engine
- Benchmark & Regression Engine
- Agent Orchestration Engine
- Certification & Governance Engine

**12 Specialist Agents (The Writing Board)**
- Intake Architect, Corpus Auditor, Voice Fingerprinter, Genre Marshal, Structure Engineer, Evidence Prosecutor, Sentence Surgeon, Dialogue Commander, Narrative Architect, Stress Tester, Scorekeeper, Delivery Packager
- Agent manifest, orchestration protocol, conflict resolution rules

**11 Machine-Readable Schemas (JSON Schema)**
- `intake_contract.schema.json`
- `corpus_map.schema.json`
- `voice_fingerprint.schema.json`
- `genre_stack.schema.json`
- `architecture_graph.schema.json`
- `epistemic_ledger.schema.json`
- `prose_rewrite_log.schema.json`
- `storyworld_memory.schema.json`
- `delivery_bundle.schema.json`
- `benchmark_result.schema.json`
- `agent_task.schema.json`

**10 New Domain Packs**
- `grant_nofo.md` — Grant writing / NOFO responses
- `technical_documentation.md` — Developer-facing docs
- `journalism.md` — Feature writing, narrative nonfiction
- `resume_cover_letter.md` — ATS-clean, evidence-of-impact
- `social_media.md` — Platform-specific cadence and hook variants
- `youtube_script.md` — Retention hooks, beat pacing, open loops
- `newsletter.md` — Recurring sections, voice consistency
- `real_estate.md` — Listings, investor memos, buyer education
- `loan_officer.md` — Trust, compliance-safe clarity, rate/term precision
- `church_leadership.md` — Sermon, study guide, devotional, announcement
- `small_business_operator.md` — Offer clarity, customer journey

**New Voiceprint**
- `courageous_builder.md` — pattern for branded operator personas (Grace, founder assistants, ministry assistants, sales assistants, grant assistants, vertical bots)

**Voice Fingerprint Engine**
- Measurable authorial profiles (avg sentence length, variance, compression, abstraction tolerance, metaphor density, question frequency, transition habits, dominant syntactic structures, authority posture)
- Drift detection against baseline
- Team voice library support

**Genre Stack Engine + Collision Matrix**
- Multiple genre packs operate simultaneously
- Conflict weighting matrix (evidence vs. voice vs. compression vs. compliance)
- Mixed-genre task support ("church grant proposal in plain language with sermon-level dignity but government-level precision")

**Architecture Graph Engine**
- Explicit graphs for sections, paragraphs, claims, scene beats, dialogue exchanges, proof points
- Edge types: supports, contrasts, escalates, resolves, foreshadows, pays off
- Orphan detection, unsupported-claim detection, dead-scene detection, repeated-beat detection

**Epistemic Ledger Engine**
- Claim classification: observed fact / sourced fact / inference / synthesis / recommendation / rhetoric
- Source status: verified / user-provided / assumed / inferred / missing / unsafe
- Mandatory in high-stakes domains (academic, medical, legal, government, grant, financial)
- Hard-blocks invented source attribution, fabricated statistics, fake citations

**Narrative Intelligence Engine**
- Storyworld memory (schema-typed)
- Series arc audit (does each book raise stakes or repeat?)
- Cross-book voice fingerprint stability
- Foreshadowing ledger (planted / paid off / orphaned)

**Arena Delivery Engine**
- 13+ delivery arenas: memo, grant response, sermon, caption, article, chapter, email, pitch slide, YouTube script, newsletter, government brief, SOP, speech, landing page
- Channel constraint enforcement
- Single-content-multi-arena repackaging

**Benchmark & Regression Engine**
- 60 benchmark cases across 12 categories
- Score improvement gates (v3 must beat v2 by 5+ points on 70%+ of cases)
- No-regression gates
- Public benchmark report format

**5 New Rewrite Operators**
- `intake_contract` — emit governed task object from chaotic request
- `corpus_audit` — map allowed sources, flag stale/contradictory
- `epistemic_classify` — tag every claim with type + source status
- `voice_fingerprint` — emit measurable voice profile + drift report
- `arena_repackage` — convert approved content to target arena format
- `benchmark_run` — run regression against prior version

**2 New Scoring Systems**
- Epistemic Integrity (100 points)
- Arena Fit (100 points)
- v3.0 Composite (1000 points, weighted)

**5 New Output Modes**
- `epistemic-ledger`
- `delivery-bundle`
- `voice-drift-report`
- `benchmark-result`
- (existing modes preserved)

**Governance & Certification**
- `governance/RFC_PROCESS.md` — formal proposal process
- `governance/ADR_TEMPLATE.md` — architecture decision records
- `governance/RELEASE_CHECKLIST.md` — release-grade gates
- `governance/VERSIONING.md` — semantic versioning rules
- `certification/operator_levels.md` — Apprentice / Operator / Architect tiers
- `certification/exam_rubrics.md` — operator certification scoring

**Documentation Reframe**
- `docs/operator_manual/` — advanced execution, scoring, troubleshooting
- `docs/builder_guide/` — schemas, agents, APIs, integration
- `docs/api/API_SPEC.md` — REST/JSON contracts
- `docs/mcp/MCP_SPEC.md` — Model Context Protocol server spec
- `docs/MIGRATION_v2_to_v3.md` — step-by-step migration
- `docs/DOMAIN_PACK_GUIDE.md` — how to build new packs
- `docs/VOICEPRINT_GUIDE.md` — how to build measurable voices
- USER_GUIDE expanded to 250+ prompts, organized by operator tier

### Preserved from v2.0

- All v2.0 7-pass kernel logic (now nested inside v3.0's 11-pass kernel)
- All v2.0 anti-pattern libraries (150+ banned phrases, 9 structural patterns, 59 cadence signatures, fake depth, fake authority, genre-specific clichés)
- All v2.0 positive patterns (paragraph blueprints, openings/closings, evidence integration, scene grounding, power dynamics, tension mechanics)
- All v2.0 fiction intelligence (chapter construction, 12 character roles, dialogue v2.0, thriller scene architecture, transmedia)
- All v2.0 voiceprints (sovereign commander, literary recursive, sermon Black church, investor precision, founder manifesto, academic rigorous, casual sharp, custom)
- All v2.0 genre packs (16 — strategy, fiction, sales, academic, speech, sermon, email, pitch_deck, legal_positioning, cinematic_narration, dialogue, government_brief, medical_writing, patent_claims, thriller_scene_architecture, transmedia_character)
- All v2.0 scoring systems (7)
- All v2.0 rewrite operators (19)
- Academic mode

### Changed

- README reframes the project as a Sovereign Writing Operating System
- ROADMAP rewritten for post-v3 trajectory (v3.1 multilingual, v3.2 MCP server reference impl, v3.3 collaborative team voice, v4.0 multimodal)
- CONTRIBUTING aligned to governance/RFC_PROCESS
- File count grows from 58 → 120+
- About description on the GitHub repo updated to reflect v3.0 positioning

### Migration Notes

- v2.0 prompts continue to work; the 7-pass kernel is preserved inside the 11-pass kernel.
- High-stakes domain output now mandatorily emits an Epistemic Ledger.
- Cross-arena distribution should use Arena Delivery Bundles rather than ad-hoc reformatting.
- Machine-readable JSON output available at every pass via `output_mode: json`.
- See `docs/MIGRATION_v2_to_v3.md` for detail.

### Created by

**Antonio T. Smith Jr. / Density6 LLC**
[densitysix.com](https://densitysix.com)

---

## [2.0.0] — 2026-04-01

### Added — The Fiction Intelligence Engine

- 7th compilation pass: Scene & Chapter Audit
- Chapter Construction Doctrine (11-section framework)
- 12 Character Role Archetypes
- Dialogue v2.0 (7 laws + 9 tension elements + 15 advanced techniques + 100-point scoring)
- Power Dynamics (props, space, gesture, consumption, environment as narrative weapons)
- Tension Mechanics (8-phase slow-burn compression + silence taxonomy + psychological warfare)
- Thriller Scene Architecture (confined-space doctrine, 5 structural beats, WWGW framework)
- Transmedia Character Deepening (diaries, audio dramas, lore bibles, interactive serials, AR experiences)
- 7 scoring systems (independent 100-point rubrics)
- 5 new rewrite operators (scene_audit, role_audit, dialogue_stress_test, power_map, plant_audit)
- 6 new adversarial tests
- 3 new gold outputs

### File count
- 52 → 58 files, 42,264 → 68,770 words

---

## [1.0.0] — 2026-03-30

### Released

The complete Writing Intelligence Compiler — 52 files, 42,264 words, free and open source under MIT license.

### Added

**Core**
- 6-pass compilation pipeline (Mission Lock → Diagnostic Scan → Structural Rewrite → Sentence Surgery → Voice Restoration → Stress Test)
- 100-point scoring system across 10 axes with 8 auto-fail conditions
- Auto-mode engine: automatic intent, genre, voice, and audience detection

**Anti-Pattern Engine (7 files)**
- 150+ banned phrases with hard/soft/earned-exception tiers
- 9 structural anti-patterns
- 9 core + 50 expanded cadence signatures
- Fake depth, fake authority, genre cliché libraries

**Positive Construction System (4 files)**
- 9 paragraph blueprints with physics auditing
- 12 strong opening/closing types
- 6 evidence integration techniques
- 8 scene grounding methods

**Voiceprint Engine (8 files)**
- 7 pre-built voiceprints + custom builder

**Genre Packs (14 files)**
- Strategy, fiction, sales, academic, speech, sermon, email, pitch deck, legal positioning, cinematic narration, dialogue, government brief, medical writing, patent claims

**Diagnostics (4 files)**
- 100-point scorecard
- 14 reversible rewrite operators
- 25 failure modes
- Auto-diagnostic report with violation heatmaps

**Compiler (6 files)**
- Section architecture, continuity, memory system, style transfer, auto-mode, cross-document audit

**Academic Mode (2 files)**
- Rubric compiler, claim-evidence binding, citation intelligence, anti-hallucination rules, authorship proof layer, 8-pass academic revision stack, 10 discipline reasoning libraries

**Tests (5 files)**
- Benchmark samples, adversarial cases, transformation examples, gold output library, detector benchmark methodology

### Created by
**Antonio T. Smith Jr. / Density6 LLC**
