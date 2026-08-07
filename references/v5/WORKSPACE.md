# The Workspace

**Status: executable — `wi init` / `wi ingest` / `wi graph`.**

v5 needs persistence. A graph of claim atoms, anchors, decisions and invalidations is not something that can live in a conversation, and neither is a proof closure that has to survive an edit made three weeks later.

Persistence usually arrives as a hosted service. It does not have to.

**Nothing constitutional requires a server.** Every guarantee in this project — content-addressed identity, deterministic canonicalization, closure recomputation, offline verification — is satisfied by a directory on a laptop. The workspace is that directory, and it is designed so that handing someone the folder hands them the whole system.

Read this with [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md), which specifies the SQLite schema the workspace index implements, and [`PROOF_CARRYING_RELEASE.md`](PROOF_CARRYING_RELEASE.md), which is what a workspace produces.

---

## Table of contents

1. The workspace layout
2. Storage strategy
3. The project file and the lockfile
4. Build reproducibility classes
5. Encryption and confidentiality
6. Long-form book mode
7. Performance targets
8. Migration from v4
9. What is executable and what is specified

---

## 1. The workspace layout

**Status: executable — `wi init`.**

```
my-grant-project/
├── wi.project.yaml          project identity, inputs, style, targets — §3
├── wi.lock                  pinned versions and digests of everything used — §3
│
├── .wi/
│   ├── workspace.db         SQLite index: nodes, states, edges, invalidations
│   ├── objects/sha256/      content-addressed blobs, sharded by digest prefix
│   ├── snapshots/           Law B originals: every author draft, immutable
│   ├── graph/               exported node and edge JSONL, regenerable
│   ├── decisions/           proposals, decisions and waivers as durable records
│   ├── judgments/           judgment records with provider, inputs and outputs
│   ├── builds/              build manifests, one per render execution
│   ├── reports/             gate reports and impact reports, kept for history
│   ├── attestations/        attestations over produced artifacts
│   └── cache/               derived indexes and closures — deletable at any time
│
├── sources/                 supplied source documents, as the author filed them
├── drafts/                  the author's working text
└── outputs/                 rendered artifacts
```

One line each:

| Path | Holds |
|---|---|
| `wi.project.yaml` | What this project is, what it reads, how it renders |
| `wi.lock` | Exactly what was used, pinned by version and digest |
| `.wi/workspace.db` | The index: node identities, state digests, edges, invalidations. Schema in [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) §6.1 |
| `.wi/objects/sha256/` | Immutable blobs addressed by digest — raw source bytes, canonical payloads, render outputs |
| `.wi/snapshots/` | Every version of the author's own text, so the original is always recoverable |
| `.wi/graph/` | JSONL export of nodes and edges, for portability and for bundling |
| `.wi/decisions/` | Proposal, decision and waiver records, bound to target states |
| `.wi/judgments/` | Judgment records: provider, model identifier, prompt policy hash, inputs, output |
| `.wi/builds/` | One manifest per build: inputs, renderer identities, artifact digests |
| `.wi/reports/` | Gate and impact reports as produced, retained rather than overwritten |
| `.wi/attestations/` | The machine-checkable statements about what was verified for each artifact |
| `.wi/cache/` | Pure derivation. Deleting it costs time and nothing else |
| `sources/` | What the author supplied, untouched |
| `drafts/` | What the author is writing |
| `outputs/` | What gets sent |

**`.wi/cache/` is the only directory that may be deleted without loss.** That is a design constraint, not an observation: anything that cannot be recomputed from `workspace.db` and `objects/` does not belong in the cache, and anything a verdict depends on does not belong there either. A cache whose absence changes a verdict is a correctness surface pretending to be an optimization.

---

## 2. Storage strategy

**Status: executable — `wi init` / `wi ingest` / `wi graph`.**

Four layers, each doing one job:

| Layer | Used for | Why this and not something else |
|---|---|---|
| SQLite | Indexes, transactions, local queries, graph adjacency | Transactional, single-file, ubiquitous, fast enough for millions of edges with the right indexes |
| Content-addressed object store | Immutable source bytes and canonical state payloads | Identity *is* the digest, so deduplication is free and tampering is detectable |
| JSONL export | Portability — bundles, diffs, review, version control | Line-oriented, greppable, diffable, readable without any tool from this project |
| Optional server backend | Scale, concurrency, shared teams | Must implement the same interfaces and produce the same digests |

**SQLite is not a concession.** It is not the thing chosen because a real database was too much work. It is the thing chosen because the project's central claim is that a hostile reader can check the work, and a reader who must first be issued database credentials cannot. `.wi/workspace.db` is one file. It can be committed beside the manuscript, mailed to counsel, carried into an air-gapped room, opened in ten years with tools that ship on every operating system, and inspected with `sqlite3` by someone who has never heard of Writing Intelligence.

The portability *is* the accountability argument. A server backend is legitimate and expected at scale; the requirement on it is not architectural taste but arithmetic — identical canonicalization, identical digests, identical closure semantics. Where a server-computed digest and a locally computed digest differ, the local file is normative and the server has a bug.

---

## 3. The project file and the lockfile

**Status: executable — `wi init` writes both; `wi ingest` and `wi graph` update `wi.lock`.**

### 3.1 `wi.project.yaml`

```yaml
project:
  id: 0192f3a1-7c40-7b2e-9000-0d4a1b6c3e77   # stable across renames
  title: "Delta Regional Capacity Initiative — 2026 Application"
  language: en

inputs:
  sources:
    - "sources/**/*.pdf"
    - "sources/**/*.txt"
    - "sources/**/*.xlsx"
  drafts:
    - "drafts/**/*.md"

style:
  citation: chicago-notes-bibliography
  terminology: "style/terms.yaml"       # protected terms and their bindings

targets:
  - name: book
    renderer: wi.render.pdf
    entry: drafts/narrative.md
  - name: web
    renderer: wi.render.html
    entry: drafts/narrative.md
  - name: audio
    renderer: wi.render.audio_script
    entry: drafts/narrative.md
```

`project.id` is a UUID rather than the title because titles change and identity must not. `inputs` are globs so that adding a source is a file operation, not a configuration edit. `style.terminology` points at the protected-term bindings whose violation is a `block_on` condition in [`POLICY_AS_CODE.md`](POLICY_AS_CODE.md). Each target names a renderer and an entry, and a target that declares neither is a build with no defined output.

### 3.2 `wi.lock`

```yaml
lockfile_version: 1
generated_at: "2026-03-19T09:41:02Z"

core:
  version: "5.0.0"
  schema_version: "5.0.0"
  canonicalization: "wi-json-v1"
  normalization: "nfc-1"

packs:
  - id: wi.genre.grant_nofo
    version: "2.1.0"
    digest: "sha256:6b41c0d9...73ea"

renderers:
  - id: wi.render.pdf
    version: "5.0.0"
    digest: "sha256:c0a71fe4...92b8"

language_packs:
  - id: wi.lang.en
    version: "5.0.0"

tokenizers:
  - id: wi.tok.en-sentence
    version: "3.2.0"

judgment_providers:
  - id: local.none
    prompt_policy_hash: "sha256:0000...0000"
    available: false

sources:
  - path: "sources/needs_assessment.txt"
    logical_id: 0192f3a1-7c40-7b2e-a001-8c4d1e9f0b22
    version: 3
    object_digest: "sha256:b7a241d9...0c17"
```

The lockfile pins the core version, the schema version, pack digests, renderer digests, language pack versions, tokenizer versions, judgment provider policy hashes and source object digests. It answers one question completely: *what, exactly, was used*.

**The honest caveat, stated in the file's own documentation and repeated here:**

> The lockfile is **not** a claim that remote generative models are reproducible. It is a record of exactly what was used.

Pinning `model_identifier: vendor-model-3.7` and a prompt policy hash does not make that provider return the same output tomorrow. It makes the judgment *attributable* — a reviewer can see which system produced it, what it was asked, and what it saw, and can therefore disagree with it. That is the achievable guarantee, and pretending it is reproducibility would put a determinism claim on the one component in the stack that cannot honor it.

---

## 4. Build reproducibility classes

**Status: specified.**

Every build step is assigned exactly one class. Not a badge on the build — a class per step, recorded in the build manifest.

| Class | Means |
|---|---|
| `deterministic` | Same inputs, same outputs, byte for byte, on any machine, forever |
| `deterministic_given_cached_judgments` | Deterministic provided the recorded judgments are reused rather than re-requested |
| `best_effort_replay` | Can be re-run with the same inputs; output equivalence is likely and not guaranteed |
| `nonreproducible_external` | Depends on an external service whose output is not under this project's control |

**Why the word matters.** "Reproducible build" is a phrase with real meaning in software supply chain work, and it is being spent quickly by tools that mean "we saved the inputs." A build that calls a hosted model in the middle and calls itself reproducible has redefined the term to mean nothing, and the redefinition is invisible to the person relying on it.

Per-step classification is what stops that. A pipeline whose ingest, atomize, anchor, check and render steps are `deterministic` and whose one paraphrase-support step is `nonreproducible_external` is an honest and useful pipeline — and a reviewer can see precisely which sentence's proof rests on the one step that will not replay. Collapsing the same pipeline into a single word would either overclaim on eight steps or underclaim on one.

The build manifest records the class beside each step, and `wi verify-release` reports the set of classes present in the closure.

---

## 5. Encryption and confidentiality

**Status: confidentiality labels executable; at-rest encryption specified.**

| Mechanism | What it does | Status |
|---|---|---|
| Workspace encryption at rest | Encrypts `objects/`, `snapshots/` and `workspace.db` on disk | Specified |
| OS keychain integration | Local key material held by the platform keystore, never in a dotfile | Specified |
| Customer-managed keys | Server mode: the operator holds the key, the service holds ciphertext | Specified |
| Source confidentiality labels | Per-source classification that governs export and bundling | **Executable** |
| Redaction-aware export | A `redacted` bundle carries only approved excerpts, with their approvals | **Executable** |

A confidentiality label rides with the source through every derived object:

```yaml
sources:
  - path: "sources/patient_summaries.txt"
    confidentiality: restricted     # public | internal | confidential | restricted
    redistribute: false
```

`restricted` with `redistribute: false` means `wi bundle --profile full` refuses to run, and names the source. Not a warning after the archive is written — a refusal before.

**The hard default: no external telemetry contains source text, ever.** Not truncated. Not hashed-and-sampled. Not in a crash report, not in an error string, not in a diagnostic bundle, not behind a verbose flag, not with consent. Counts, error codes, durations and version strings are the entire vocabulary available to telemetry. This is stated as an absolute because every partial version of it has been violated by accident somewhere — a stack trace that carried a filename, an error message that quoted the offending line. Filenames and quoted lines are source content. The rule has no exceptions because the exceptions are how it fails.

---

## 6. Long-form book mode

**Status: structure layout and chapter contracts specified; text-span proof over chapter content executable.**

A 400-page manuscript with 3,000 claims and a bibliography is not a long draft. It has structure the checker must respect.

```
book/
├── book.yaml              title, volumes, global evidence mode, citation style
├── volumes/               volume manifests, for multi-volume works
├── parts/                 part manifests
├── chapters/              one file per chapter, plus its contract
├── figures/               figure assets and their provenance records
├── tables/                table data and its source bindings
├── notes/                 footnotes and endnotes as addressable nodes
├── bibliography/          source entries, bound to ingested source identities
├── concepts/              registered definitions, terms and canonical facts
└── sources/               the supplied evidence corpus for the work
```

Each chapter carries a **contract**:

```yaml
id: ch-02
title: "Demonstrated Need"
required_sections:
  - population_description
  - service_gap_evidence
  - geographic_scope
  - prior_intervention_outcomes
evidence_mode: strict
citation_style: chicago-notes-bibliography
```

**The build fails if a required structural commitment vanishes.** A chapter that declared `service_gap_evidence` and no longer contains it is not a stylistic choice discovered at proof stage; it is a missing section in a document whose reviewer has a checklist with that section on it. The contract is how the author's own earlier decision gets to outlive the afternoon they made it.

`evidence_mode` per chapter exists because long works are not uniform. An acknowledgements chapter and a methodology chapter do not need the same discipline, and forcing one mode across a book means either burying the author in friction or under-checking the chapter that matters.

---

## 7. Performance targets

**Status: specified — these are target budgets, not measured claims.**

| Operation | Target budget |
|---|---|
| Deterministic checks over 10,000 claim atoms | Under 2 seconds, excluding source parsing, on a modern laptop |
| Impact traversal over 1,000,000 edges | Under 1 second for ordinary localized invalidation |
| Workspace open at 100,000 nodes | Under 500 ms of indexed metadata load |
| First meaningful UI render | Under 1.5 seconds after workspace metadata is available |

**These are budgets, not benchmark results.** No measurement is being reported here. They are the numbers the design is built to hold, published so that a failure to hold them is a visible regression rather than a quiet drift.

Two qualifications are part of the target, not footnotes to it:

- **"Modern laptop" and "ordinary localized invalidation" are unmeasured phrases** until a benchmark publishes the hardware and the workload. A source change that touches one paragraph is localized; a policy change that invalidates every judgment in the project is not, and no traversal budget covers both.
- **Any result quoted from these budgets must publish its benchmark hardware and its dataset.** A performance number without a machine and a corpus behind it is a claim with no denominator, and this project has a name for that: it is the same fake-authority pattern the doctrine refuses everywhere else, applied to speed.

---

## 8. Migration from v4

**Status: specified.**

```
$ wi migrate --from v4
```

The migration is conservative by rule, and the rule is one sentence:

> **A v3 or v4 `verified` status becomes `legacy_status: verified` plus `v5_proof_state: unverified_pending_migration`, with the reason recorded.**

The reason recorded is always the same and always true: *the old status did not carry a v5 evidence anchor*. A v4 verification was a real check against a real source, and it was recorded as a line in a report rather than as a typed anchor into a hashed source version. There is no honest procedure that converts the first into the second, because the information the second requires — the exact byte state, the exact offsets, the quote digest — was never captured.

Promoting it anyway would manufacture the one thing this system exists to prevent: an anchor that looks inspectable and points nowhere a reviewer can go.

```
$ wi migrate --from v4 --report

Migration: v4 workspace → v5

Imported
  sources                          6
  claims → claim atoms           182   (41 sentences split into 2+ atoms)
  proposals                       74
  gate reports                     9

Requires re-verification
  claims with v4 `verified` status  63   → legacy_status: verified
                                          v5_proof_state: unverified_pending_migration
                                          reason: no v5 evidence anchor

Mapped without re-verification
  claims with `needs_source`        88   → status carried forward unchanged
  claims classified non-factual     31   → realm assigned, no proof required

Lossy mappings — named
  · v4 span offsets were character offsets over normalized text. v5 anchors
    address raw bytes. 63 spans were re-located against the ingested source
    bytes; 58 matched exactly and 5 did not. The 5 are listed below and are
    NOT carried forward as anchors.
  · v4 reports recorded "checks run" as prose. There is no mechanical mapping
    from that prose to the v5 five-state capability record. All migrated
    claims carry check state `unavailable_on_surface: pre-migration`.
  · v4 had no decision records. 74 proposals were imported with no deciding
    actor. They are `proposed`, not `accepted`, regardless of whether the
    change appears in the current draft.
  · v4 had no source versioning. Each imported source was ingested as @v1;
    prior states of those files are not recoverable and are not claimed to be.

Unmatched spans (5): c-0014, c-0031, c-0077, c-0102, c-0140

Nothing in this migration produced a v5 `verified` state. 63 claims are ready
for re-anchoring; run `wi anchor --suggest` to get candidate locations.
```

**Do not hide migration loss.** The temptation in a migration report is to lead with the imported counts and let the losses appear as a footnote, because a clean import looks like a good tool. The fourth block above is the one an author actually needs: it names what did not survive, in specifics, with the affected identifiers listed. An author who reads "182 claims imported successfully" and later discovers that 74 proposals lost their acceptance records has been told a true sentence and left with a false belief, which is the failure mode this entire project is built to refuse.

---

## 9. What is executable and what is specified

| Mechanism | Status |
|---|---|
| `wi init`, workspace layout, `.wi/` creation | Executable in `scripts/wi.py` |
| `wi ingest`, raw-byte source identity, object store writes | Executable in `scripts/wi.py` |
| `wi graph`, node and edge queries, JSONL export | Executable in `scripts/wi.py` |
| SQLite index with adjacency indexes in both directions | Executable in `scripts/wi.py` |
| `wi.project.yaml` and `wi.lock` generation and update | Executable in `scripts/wi.py` |
| Source confidentiality labels and redaction-aware export | Executable in `scripts/wi.py` |
| Snapshots satisfying Law B | Executable in `scripts/wi.py` |
| Build reproducibility classes in the build manifest | Specified |
| Workspace encryption at rest, keychain and customer-managed keys | Specified |
| Long-form book layout and chapter contracts | Specified |
| Performance budgets | Specified — targets, not measurements |
| `wi migrate --from v4` and its report | Specified |
| Server backend implementing the same interfaces | Specified |

---

## Related documents

- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — the SQLite schema and storage reasoning in full
- [`CANONICAL_HASHING.md`](CANONICAL_HASHING.md) — the digests the object store is addressed by
- [`POLICY_AS_CODE.md`](POLICY_AS_CODE.md) — the policy file that sits beside `wi.project.yaml`
- [`PROOF_CARRYING_RELEASE.md`](PROOF_CARRYING_RELEASE.md) — what a workspace produces
- [`CONSTITUTION.md`](CONSTITUTION.md) — Law B, which snapshots implement
- [`../v4/ACCOUNTABILITY_LAYER.md`](../v4/ACCOUNTABILITY_LAYER.md) — the v4 statuses this migration carries forward
- [`../../docs/MIGRATION_v3_to_v4.md`](../../docs/MIGRATION_v3_to_v4.md) — the previous migration, for shape
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
