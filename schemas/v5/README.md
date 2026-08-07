# Writing Intelligence v5 — State Schemas

The fifteen schemas in this directory describe the objects a v5 workspace **holds**, not the artifacts a writing pass **produces**. That distinction is the whole reason this directory exists alongside `../`.

A v3 artifact is a photograph: true about a specific wording at a specific moment, with nothing that notices when it stops being true. A v5 object is a **state**: it has a durable identity, a hash-addressed content state, an explicit dependency on the states it was derived from, and a mechanism that marks it stale when any of those move. Everything below follows from that.

These schemas are written against `../../scripts/wi.py` — the executable v5 core — and describe what that code actually emits. Where a field is specified in doctrine but not populated by the shipped core, the field's `description` says so in the field itself, not in a footnote.

---

## The two-identity model

Every governed thing in v5 has **two** identifiers, and confusing them is the failure mode the whole system is built to avoid.

**Logical id** answers *which thing is this?* It is a UUID-shaped string produced by `logical_id(kind, *parts)`, derived by SHA-256 from what makes the thing *the same thing across versions*. For a source artifact that is its file name. For a claim atom it is the document path plus the **proposition skeleton** — the structured quantities, temporal scope, modality, negation, attribution and entities — and deliberately *not* the wording. Reword a claim and the logical id survives; change what it asserts and you get a new one. That single choice is what lets a semantic diff distinguish an edit from a replacement.

Logical ids are content-derived rather than random on purpose. Random ids would make every build produce a different graph, which would make `wi bundle` non-reproducible and a published checksum meaningless.

**State digest** answers *is this the same verified state?* It is `sha256:` plus a hash over a domain-separated preimage that binds the canonical payload, the schema id, the schema version and the normalization version together. Two payloads that are byte-identical but written under different schema ids are different states, by construction rather than by convention.

A proof binds a **state digest**, never a logical id. That is why a verification record carries `claim_state`, a proposal carries `target_state_digest`, a decision carries both `proposal_state` and `target_state`, and an anchor carries `source_state_digest`. Edit any of them and the record still describes the state it was taken against — which is exactly what makes staleness computable rather than something a person is supposed to remember.

Source bytes are a third case: they are addressed by `blob_digest()`, a plain SHA-256 over the **raw bytes**, taken before any decoding, Unicode normalization, whitespace folding or text extraction.

---

## The canonical hashing contract, in one paragraph

Canonical JSON in v5 is RFC 8785-shaped: every string NFC-normalized, keys sorted, no insignificant whitespace, no `NaN` and no infinities (a float that is one raises `WI_INPUT_INVALID` rather than serializing to something a second implementation would read differently), UTF-8 encoded. `content_digest(obj)` hashes that canonical payload alone and answers *is this the same content?* `state_digest(obj, schema)` hashes a domain-separated preimage — the literal prefix `wi-state-v5\0`, then `schema=<id>@<schema version>\0`, then `normalization=<normalization version>\0`, then `payload=` and the canonical bytes — and answers *is this the same verified state?* The two are domain-separated deliberately: the same raw digest must never ambiguously represent a source byte stream and a semantic object. Source bytes are hashed raw by `blob_digest()` with no normalization at all, because normalizing first would mean an upgrade to the normalizer could change a source's identity without the source changing, so a proof could move while no source moved. Every digest in every schema here is constrained to `^sha256:[0-9a-f]{64}$`. Full rules, worked example and the error taxonomy: [`../../references/v5/CANONICAL_HASHING.md`](../../references/v5/CANONICAL_HASHING.md).

### A worked example of the two identities

Take one sentence in a draft:

> Between 2019 and 2022, the Delta Regional Capacity Program served 11,800 households across seven counties.

`wi atomize` splits it, builds a proposition, and derives a skeleton such as `q=11800.0/households|t=2019-2022|m=is|n=0|a=|e=Delta Regional Capacity Program`. The **logical id** is a hash over the document path and that skeleton. The **state digest** is a hash over the proposition, the class and the whitespace-folded wording, under schema id `meaning.claim_atom`.

Now three different edits, and what each one does:

| Edit | Logical id | State digest | Consequence |
|---|---|---|---|
| Reorder the clause so the years come last | unchanged | changes | `wording_only`; existing support carries forward |
| Change 11,800 to 12,400 | **changes** | changes | `quantity_changed`; support does not carry forward, and the numeric check fails against the bound anchor before any judgment would be consulted |
| Replace the source file the anchor points into | unchanged | unchanged | The atom is untouched; the *anchor* goes stale if its byte range overlaps the edit, and the invalidation walks outward from there |

The third row is the one that does not exist in v4 at all, and it is the reason a state digest and a logical id have to be separate fields rather than one identifier doing both jobs.

### Where each digest lives

| Field | Kind | Taken over |
|---|---|---|
| `blob_digest` (source version) | raw bytes | The source file exactly as supplied, no normalization |
| `state_digest` (any node) | domain-separated state | Canonical payload + schema id + schema version + normalization version |
| `quote_digest` (text span anchor) | content | The whitespace-folded quote, UTF-8 |
| `project_state_digest` (manifest) | content | Nodes, edges, checks, source lock and anchors together — the proof closure |
| `policy_digest` (manifest) | content | The resolved policy object sealed at `policy/wi.policy.json` |
| `proof_closure_digest` (target) | content | The closure the shipped artifact was verified under |

---

## The schema family

| Schema | What emits it | What consumes it |
|---|---|---|
| [`workspace.schema.json`](workspace.schema.json) | `wi init` → the `workspace` table | Every later command; `wi doctor` |
| [`source_artifact.schema.json`](source_artifact.schema.json) | `wi ingest` → `register_sources()` | `wi anchor`, `wi impact`, `wi graph`, `sources/sources.lock` |
| [`source_version.schema.json`](source_version.schema.json) | `wi ingest` → `register_sources()` | `wi impact` (version diff), anchor resolution, bundle source lock |
| [`evidence_anchor.schema.json`](evidence_anchor.schema.json) | `wi anchor` → `make_anchor()` | `anchor_and_check()`, `compute_impact()`, `sources/anchor-index.json` |
| [`claim_atom.schema.json`](claim_atom.schema.json) | `wi atomize` → `atomize_document()`, completed by `wi anchor` | `gate_atoms()`, `run_writing_tests()`, `semantic_diff()`, `wi explain`, bundle |
| [`graph_node.schema.json`](graph_node.schema.json) | `Workspace.put_node()`; projected by `build_bundle()` | `wi graph`, `graph/nodes.jsonl`, `verify_bundle()` |
| [`graph_edge.schema.json`](graph_edge.schema.json) | `Workspace.put_edge()`; projected by `build_bundle()` | `wi impact` traversal, `graph/edges.jsonl`, `verify_bundle()` |
| [`verification_record.schema.json`](verification_record.schema.json) | `wi anchor` → `anchor_and_check()` | `wi gate`, `proof/checks.jsonl`, `verify_bundle()` |
| [`judgment_record.schema.json`](judgment_record.schema.json) | A judgment provider — **none ships in v5.0** | Reserved: `proof/judgments.jsonl` (written empty) |
| [`proposal.schema.json`](proposal.schema.json) | `wi diff --semantic` computes the delta and impact blocks; the persisted object is specified | A decision loop; `wi impact` repair planning |
| [`decision.schema.json`](decision.schema.json) | A human actor — specified, not executable in v5.0 | Reserved: `decisions/decisions.jsonl` (written empty) |
| [`invalidation.schema.json`](invalidation.schema.json) | `wi impact --apply` → `Workspace.mark_stale()` | `gate_atoms()`, `build_bundle()` staleness flags, `verify_bundle()` |
| [`policy.schema.json`](policy.schema.json) | An operator, as `wi.policy.yaml` / `wi.project.yaml` | `wi gate`, `wi test`, `wi bundle` → `policy/wi.policy.json` + `policy_digest` |
| [`concept_registry.schema.json`](concept_registry.schema.json) | An operator, as `.wi/concepts.yaml` or the project `concepts` / `tests` blocks | `wi test` → `run_writing_tests()` |
| [`release_manifest.schema.json`](release_manifest.schema.json) | `wi bundle` → `build_bundle()` | `wi verify-release` → `verify_bundle()`; any third-party verifier |

---

## Executable today vs. specified

"Executable" means `../../scripts/wi.py` produces or consumes objects of this shape right now, offline, with no model and no network. "Specified" means the shape is fixed and the code that fills it is a contract rather than shipped software — and the tool reports the gap rather than approximating it.

| Schema | Status |
|---|---|
| `workspace` | **Executable.** Every field written by `wi init`. |
| `source_artifact` | **Partly executable.** `logical_id`, `path`, `title`, `media_type` are written by `wi ingest`. The `confidentiality`, `rights` and `identity` blocks are specified; they are declared by a person, never inferred, and no ingestion path populates them. |
| `source_version` | **Executable** for `logical_id`, `artifact`, `blob_digest`, `byte_length` and `state_digest`. `supersedes` is stored as edges rather than as a node field. |
| `evidence_anchor` | **`text_span` executable.** `pdf_region`, `sheet_range`, `image_region`, `audio_time`, `video_time` and `data_pointer` are specified with adapter contracts and appear in `checks_not_run`. |
| `claim_atom` | **Executable**, including the proposition IR, all six deterministic checks and the full status vocabulary — except that paraphrase entailment is never attempted and `stale` is carried in the invalidation table rather than written into the atom. |
| `graph_node` | **Executable** for the source, meaning, structure, verification and release node types the text pipeline produces. The canon, media, authorship and remaining families are specified. |
| `graph_edge` | **Executable** for `supports`, `derived_from`, `supersedes`, `asserted_in`, `renders_as` and `depends_on`. The other twenty-four relations are specified. |
| `verification_record` | **Executable.** Every record the core emits carries basis `verified`, because every check it runs is a deterministic comparison. |
| `judgment_record` | **Specified. No provider ships in v5.0.** Nothing in this repository executes a judgment. |
| `proposal` | **Partly executable.** `semantic_delta` and `proof_impact` are computed by `wi diff --semantic`. The persisted proposal object and its lifecycle are specified. |
| `decision` | **Specified.** The actor model and the decision loop are defined; the bundle reserves the file and ships it empty. |
| `invalidation` | **Executable** for `source_version_changed` via `wi impact --apply`. The other reason codes are specified. |
| `policy` | **Executable** for `evidence`, `release`, `privacy` and `mode`, which are read by `gate`, `test` and `bundle` and sealed into the manifest digest. `allowed_basis`, `proposals`, `sources.freshness` and `authority` are specified. |
| `concept_registry` | **Executable** for the five implemented assertions. Any other assertion returns `unavailable` — never a pass. |
| `release_manifest` | **Executable** at profiles `full` and `hash-only`, including offline verification. `redacted` and external signing are specified. |

Ask the tool directly rather than trusting this table: `python3 scripts/wi.py doctor` prints the live capability set, including the `unavailable` map with a reason for each entry.

### The seven anchor types

`evidence_anchor.schema.json` is a `oneOf` over seven variants discriminated by `anchor_type`. Only the first is executable, and a consumer that does not implement a type must report the anchor unresolvable rather than treat it as resolved.

| Anchor type | Addresses | v5.0 |
|---|---|---|
| `text_span` | A UTF-8 byte range of a text source version | **Executable** — `wi anchor` |
| `pdf_region` | A page and bounding box, with independent text and render hashes | Specified |
| `sheet_range` | A named sheet and A1 range, with display and raw values kept apart | Specified |
| `image_region` | A normalized rectangle, with a region hash and a `judged` description that never supports a claim | Specified |
| `audio_time` | A millisecond interval, with the audio segment hashed independently of its transcript | Specified |
| `video_time` | A millisecond interval with representative frame hashes, transcript and OCR overlay | Specified |
| `data_pointer` | A JSON pointer, a row key, or a recorded query with its result digest and execution time | Specified |

The pattern repeated across the specified six is deliberate: **two hashes, never one.** The bytes of the region are pinned separately from any extraction of them, so an extractor upgrade becomes a visible, separate change rather than a silent shift in what a source "says."

---

## Validating against these schemas

Each file is standalone. There are no cross-file `$ref`s, so no resolver and no network are needed:

```bash
python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('schemas/v5/*.json')]"
```

To check live output against them, run the tool and validate what it wrote:

```bash
python3 scripts/wi.py init --mode strict
python3 scripts/wi.py ingest sources/
python3 scripts/wi.py atomize drafts/report.md
python3 scripts/wi.py anchor .wi/graph/ledger-*.json sources/
python3 scripts/wi.py bundle out/release.wiab --artifact drafts/report.md
python3 scripts/wi.py verify-release out/release.wiab
```

The claim ledger's `atoms[]` validate against `claim_atom`, its `anchors[]` against `evidence_anchor`, and inside the bundle `graph/nodes.jsonl`, `graph/edges.jsonl`, `proof/checks.jsonl` and `manifest.json` validate against `graph_node`, `graph_edge`, `verification_record` and `release_manifest` respectively.

---

## What these schemas deliberately refuse to express

Absences here are decisions, and each one is load-bearing:

- **No confidence score anywhere.** Not on a check, not on a judgment, not on a claim. Reliability is a *type* — `verified`, `measured`, `judged`, `human_declared` — and types do not average. A single blended number containing one string comparison, one benchmark measurement, one model opinion and one author assertion has a meaning nobody can recover, including whoever computed it.
- **No field in which a model could become an author.** `judgment_record` names a provider and a model as third-party infrastructure, exactly like a PDF decoder. There is no authorship field on it, and `decision` will not accept a `judgment_provider` in a human actor slot.
- **No percentage without a denominator.** `counts.claim_atoms_required` is present in every manifest precisely so that a coverage figure is a fact about a count.
- **No silent omission of an unrun check.** `checks_not_run` is required in the manifest, `unavailable` is a legal check result, and an unimplemented writing-test assertion returns `unavailable` rather than passing.
- **No inference path out of `unknown`.** A rights basis moves only by a recorded human declaration.

---

## How the v3 schemas in `../` relate

**They are not deleted, not deprecated, and not superseded.** The eleven schemas in [`../`](../README.md) are the **v3 craft artifacts**, and they remain valid for the craft kernel: the intake contract, the corpus map, the voice fingerprint, the genre stack, the architecture graph, the epistemic ledger, the prose rewrite log, the storyworld memory, the delivery bundle, the benchmark result and the agent task.

Their conceptual boundaries were correct. Corpus, structure, evidence, voice, canon and delivery are genuinely different concerns, and v5 keeps every one of those boundaries. What v5 changes is that each of them now sits **over a single graph identity system** instead of over its own private naming scheme. The v4-era failure was one failure repeated six times: the same claim was `c0002` in the ledger, an unnamed sentence in the architecture graph, a string inside the delivery bundle, and nothing at all in the corpus map — so nothing joined them and nothing could propagate.

In v5 terms:

- `EpistemicLedgerV3` becomes a **view** over `meaning.*` nodes and their `verification.*` records — see `claim_atom` and `verification_record` here.
- `CorpusMapV3` becomes a **view** over `source.*` nodes — see `source_artifact` and `source_version`.
- `ArchitectureGraphV3` becomes a **view** over `structure.*` nodes and the `asserted_in` / `renders_as` edges.
- `DeliveryBundleV3` becomes a **view** over `release.*` nodes and the proof closure that reaches them — see `release_manifest`.
- `VoiceFingerprintV3`, `GenreStackV3`, `ProseRewriteLogV3`, `StoryworldMemoryV3`, `IntakeContractV3`, `BenchmarkResultV3` and `AgentTaskV3` have **no v5 replacement in this directory** and are used unchanged.

Use the v3 schemas when the deliverable is a pass artifact. Use the v5 schemas when the deliverable is governed state that has to survive a source changing under it. A project can run both: the v3 ledger describes what a pass found, and the v5 graph describes whether that finding is still true.

---

## Conventions

Every schema in this directory:

- declares `"$schema": "https://json-schema.org/draft/2020-12/schema"`;
- declares `"$id": "https://writing-intelligence.dev/schemas/v5/<name>.schema.json"`;
- carries a `title` ending in `V5`;
- carries a `description` explaining what the object is **for**, not only what it holds;
- gives every field its own `description`;
- names a `required` array;
- sets `"additionalProperties": false` wherever the shape is closed, and uses `unevaluatedProperties` where a variant composes a shared base;
- constrains digests as `^sha256:[0-9a-f]{64}$` and logical ids as a lowercase UUID string;
- keeps shared shapes — digest, logical id, timestamp, actor, basis, evidence mode — in local `$defs` and references them with `$ref`, so each file validates standalone with no network retrieval.

## Author

Antonio T. Smith Jr. / Density6 LLC
