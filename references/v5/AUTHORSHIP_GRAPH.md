# The Authorship Graph

The central architecture of v5. Everything else in this release is a consequence of one decision:

> **The document is a rendering. The graph is the system.**

A finished PDF, a chapter of a novel, a deck, a subtitle track and a press release are not six works. They are six renderings of one governed body of meaning. v4 could tell you whether a sentence in one file had a verbatim span behind it. It could not tell you that the same sentence appears in four other files, that its supporting source was replaced last Tuesday, and that a signed release artifact from Thursday now stands on a source version that no longer exists. v5 exists so that question has a mechanical answer.

Read this before anything else in `references/v5/`. The semantic IR, the anchor system and the hashing rules all assume the identity model defined here.

---

**Contents:** why a graph · node families · edge families · identity · the proof closure · storage · scaling · worked example · executable vs. specified.

---

## 1. Why a graph

**Status: executable in `scripts/wi.py`.**

v4 produced six typed artifacts. They were good artifacts: each the product of a separate pass, each internally coherent.

| v4 artifact | What it knows | What it cannot know |
|---|---|---|
| `CorpusMapV3` | Which sources were supplied, their hygiene status | Which claims in the draft rest on which source |
| `ArchitectureGraphV3` | The structural plan of the document | Which structural units carry unsupported claims |
| `EpistemicLedgerV3` | Each claim's class and source status | Whether the claim appears in three other deliverables |
| `VoiceFingerprintV3` | Measured voice characteristics against a sample set | Which spans are protected from a rewrite that would break them |
| `StoryworldMemoryV3` | Canon facts, characters, continuity | Whether a canon fact is also asserted as external fact somewhere |
| `DeliveryBundleV3` | The packaged output and its verdict | Whether the verdict is still true |

The pattern is one failure repeated six times. The same claim, source, concept, character, decision or output acquires a **different identity in each artifact**. A claim is `c0002` in the ledger, an unnamed sentence in the architecture graph, a string inside the delivery bundle, and nothing at all in the corpus map. Nothing joins them, so nothing can propagate. That is why a v4 verdict is a photograph: true about a specific wording at a specific moment, with no way to notice when it stops being true.

v5 does not discard the six artifacts. Their conceptual boundaries were correct — corpus, structure, evidence, voice, canon, delivery are genuinely different concerns. v5 keeps every one of those boundaries and **places them all over a single graph identity system**. The ledger becomes a view over `meaning.*` nodes and their `verification.*` edges. The corpus map becomes a view over `source.*` nodes. The delivery bundle becomes a view over `release.*` nodes and the proof closure that reaches them.

**Why this is load-bearing.** Verification that cannot propagate is verification that expires silently. An author who checked a figure in March and ships the deck in July has no mechanism, in v4, that connects the July artifact to the March check — so the check simply carries forward, unchallenged, into a document nobody re-examined. One identity system per concept is what makes staleness a computable property rather than a thing you are supposed to remember.

---

## 2. Node families

**Status: executable in `scripts/wi.py` for the source, meaning, structure, authorship, verification and canon families as produced from text sources. Media node types and non-text source types are specified with adapter contracts. Release node types are executable through `wi bundle` and `wi verify-release`; `release.signature` is specified.**

A node is a typed, addressable thing that a proof can point at. Node types are namespaced `family.type`: the family carries the governing concern, the type carries the granularity.

### 2.1 Source family — everything supplied, and everything mechanically derived from it

| Type | Definition |
|---|---|
| `source.artifact` | A supplied source as a durable identity across all of its versions |
| `source.version` | One exact byte state of a source artifact, addressed by the digest of its raw bytes |
| `source.segment` | A contiguous extracted region of a text source version — page, block, paragraph or span container |
| `source.table` | A tabular region of a source version with row and column semantics attached |
| `source.audio_segment` | A time interval of an audio source version with its transcript state |
| `source.video_segment` | A time interval of a video source version with frame, transcript and shot state |
| `source.image_region` | A normalized rectangular region of an image source version |
| `source.web_capture` | A retrieved network resource frozen to bytes, with URL, retrieval time and response metadata |

### 2.2 Meaning family — what the author asserts, independent of how any renderer expresses it

| Type | Definition |
|---|---|
| `meaning.claim_atom` | The smallest independently checkable assertion — the canonical verification unit |
| `meaning.premise` | An assertion another claim depends on, whether or not it is stated in the surface text |
| `meaning.inference` | A conclusion reached by reasoning beyond what any source states |
| `meaning.definition` | A binding of a term to a specific meaning within this work |
| `meaning.term` | A controlled vocabulary item whose usage is tracked across the work |
| `meaning.constraint` | A stated limit, scope boundary or exception governing other meaning nodes |
| `meaning.promise` | A forward-looking commitment made to a reader, funder, customer or court |
| `meaning.obligation` | A duty asserted to bind some party, including the author |
| `meaning.recommendation` | A prescribed action, whose factual premises carry the verification burden |
| `meaning.rhetoric` | Framing with no checkable content, tracked so it is never mistaken for a claim |

### 2.3 Structure family — the shape of the work, kept separate from the meaning it carries

| Type | Definition |
|---|---|
| `structure.work` | The whole governed work under one intake contract |
| `structure.volume` | A bound division of a multi-volume work |
| `structure.part` | A major division within a volume |
| `structure.chapter` | A chapter or top-level document section |
| `structure.section` | A titled subdivision of a chapter |
| `structure.paragraph` | A paragraph or equivalent prose unit |
| `structure.scene` | A dramatic unit with continuous time, place and viewpoint |
| `structure.beat` | The smallest dramatic unit — one change of state within a scene |
| `structure.dialogue_exchange` | A bounded exchange of speech between named speakers |

### 2.4 Authorship family — who decided what, and what the author placed beyond a machine's reach

| Type | Definition |
|---|---|
| `authorship.snapshot` | An immutable capture of author-supplied state before any system action (Law B) |
| `authorship.proposal` | A proposed change with `before`, `after`, reason and predicted effect (Law A) |
| `authorship.decision` | An accept, reject or modify recorded against a specific proposal state |
| `authorship.waiver` | An authorized proceed-past-hold, bound to the exact state it waived |
| `authorship.protected_span` | Text the author has marked as not rewritable by any pass |
| `authorship.voice_constraint` | A measured or declared voice rule the compiler must satisfy |

### 2.5 Verification family — the evidence apparatus, promoted from report lines to first-class nodes

| Type | Definition |
|---|---|
| `verification.check` | A deterministic check definition — quotation, numeric, date, entity, citation, dimensional |
| `verification.result` | The outcome of running one check against one node state |
| `verification.judgment` | A reasoned assessment with no external check, always labeled `judged` |
| `verification.conflict` | Two supported states that cannot both hold |
| `verification.gate` | A policy evaluation producing `RELEASE`, `HOLD` or `BLOCK` over a defined scope |
| `verification.invalidation` | A record that a specific prior state's verification no longer applies, and why |

### 2.6 Canon family — constructed-world truth, governed like external fact and never confused with it

| Type | Definition |
|---|---|
| `canon.character` | A person within the constructed world, with tracked attributes over time |
| `canon.location` | A place within the constructed world |
| `canon.event` | A thing that happens in the world's timeline, independent of narration order |
| `canon.object` | A significant object whose state and location are tracked |
| `canon.motif` | A recurring image, phrase or idea tracked for placement and density |
| `canon.plant` | A deliberately placed setup awaiting a payoff |
| `canon.payoff` | The discharge of a plant, bound to the plant it discharges |
| `canon.rule` | A law of the constructed world that later scenes must not silently break |
| `canon.timeline_point` | A fixed point in world time that events order against |

### 2.7 Media family

**Status: specified.** Media nodes are defined here so that anchors and renderers have somewhere to land; the adapters that populate them are contracts, not shipped code.

| Type | Definition |
|---|---|
| `media.asset` | A produced media file as a durable identity across versions |
| `media.shot` | A continuous camera unit within a video asset |
| `media.frame` | A single addressable frame, identified by index and hash |
| `media.track` | An audio, subtitle, or data track within an asset |
| `media.caption` | A timed caption or subtitle cue bound to a track interval |
| `media.storyboard_panel` | A planned shot with its intended content and duration |
| `media.slide` | A single slide within a deck rendering |
| `media.chart` | A rendered data figure bound to its data source and transformation |

### 2.8 Release family

| Type | Definition |
|---|---|
| `release.target` | A declared output channel and its format, policy and constraints |
| `release.build` | One execution of the renderer set against one graph state |
| `release.artifact` | One produced file, addressed by the digest of its bytes |
| `release.attestation` | The machine-checkable statement of what was verified about an artifact |
| `release.signature` | A cryptographic signature over an attestation. **Status: specified.** |

**Why this is load-bearing.** Node types are not taxonomy for its own sake. Each type exists because some check, policy or invalidation rule needs to address exactly that granularity and nothing coarser. `meaning.claim_atom` exists because verification at sentence granularity cannot tell an author which half of the sentence failed. `source.version` exists separately from `source.artifact` because "the same document" and "the same bytes" are different questions, and only one of them can be hashed.

---

## 3. Edge families

**Status: executable in `scripts/wi.py` for edges over text-derived nodes. Edges terminating on media nodes are specified.**

An edge is typed, directed, and carries its own state digest. Every edge declares an **invalidation policy**: what happens to things downstream when the node at one end changes state.

Invalidation policies, in order of severity:

| Policy | Meaning |
|---|---|
| `hard` | Downstream verification is void immediately. Re-evaluation is required before any gate can pass. |
| `review` | Downstream state is marked review-required. A human decision clears it; nothing clears itself. |
| `soft` | Downstream state is annotated as changed. No gate consequence unless policy says otherwise. |
| `none` | Structural or informational only. No propagation. |

### 3.1 Evidential edges

| Edge | From → To | Semantics | Invalidation |
|---|---|---|---|
| `supports` | anchor / source.* → meaning.* | This evidence bears out this meaning under the stated policy | `hard` |
| `contradicts` | source.* / meaning.* → meaning.* | These two states cannot both hold | `hard` |
| `qualifies` | meaning.constraint → meaning.* | The target holds only within this limit | `hard` |
| `derived_from` | meaning.* → meaning.* / source.* | The target's content was produced from the origin | `review` |
| `summarizes` | meaning.* → meaning.* / source.segment | A compression that must not add or strengthen | `review` |
| `translates` | meaning.* → meaning.* | Same meaning expressed in another language | `review` |
| `cites` | meaning.* / structure.* → source.artifact | A citation-shaped reference that must resolve | `hard` |

### 3.2 Rendering and dependency edges

| Edge | From → To | Semantics | Invalidation |
|---|---|---|---|
| `renders_as` | meaning.* → structure.* / media.* | This semantic node appears here, in this expression | `review` |
| `asserted_in` | meaning.* → structure.* | The meaning is asserted at this location of the work | `review` |
| `depends_on` | any → any | Generic computational or logical dependency | `review` |
| `built_from` | release.artifact → structure.* / release.build | The artifact was produced from these inputs | `hard` |
| `illustrates` | media.* → meaning.* / structure.* | This visual accompanies that meaning | `none` |

### 3.3 Definitional edges

| Edge | From → To | Semantics | Invalidation |
|---|---|---|---|
| `defines` | meaning.definition → meaning.term | This definition binds this term for this work | `review` |
| `uses_term` | meaning.* / structure.* → meaning.term | The target term appears here under its binding | `review` |
| `same_meaning_as` | meaning.* → meaning.* | Two nodes assert the same thing in different words | `review` |
| `narrows` | meaning.* → meaning.* | The origin is a stricter version of the target | `review` |
| `broadens` | meaning.* → meaning.* | The origin is a weaker version of the target — the most dangerous edit direction | `hard` |

### 3.4 Authorship edges

| Edge | From → To | Semantics | Invalidation |
|---|---|---|---|
| `proposed_change_to` | authorship.proposal → any | A proposal targeting this exact node state | `hard` |
| `accepted_by` | authorship.proposal → authorship.decision | The proposal was accepted in this decision | `hard` |
| `rejected_by` | authorship.proposal → authorship.decision | The proposal was rejected in this decision | `none` |
| `waived_by` | verification.result / verification.gate → authorship.waiver | A hold was passed under this waiver | `hard` |
| `invalidates` | verification.invalidation → any state | This state is no longer valid, with a recorded basis | `hard` |
| `supersedes` | any state → any state | A later state replaces an earlier one for the same logical id | `soft` |

### 3.5 Narrative edges

| Edge | From → To | Semantics | Invalidation |
|---|---|---|---|
| `causes` | canon.event → canon.event | One world event brings about another | `review` |
| `precedes` | canon.* → canon.* | Ordering in world time, not narration order | `review` |
| `foreshadows` | structure.* / canon.plant → canon.payoff | A setup pointing at a later discharge | `soft` |
| `pays_off` | canon.payoff → canon.plant | The discharge, bound to what it discharges | `review` |
| `depicts` | media.* / structure.scene → canon.* | This unit shows this world entity | `soft` |
| `narrates` | structure.* → canon.event | This unit tells this world event | `review` |
| `signed_by` | release.attestation → release.signature | The attestation carries this signature | `hard` |

### 3.6 `illustrates` is not `supports`

This is stated as its own rule because it is the edge most likely to be collapsed by convenience.

**A `media.*` node connected to a meaning node by `illustrates` contributes nothing to that meaning's proof state.** An image placed next to a claim about household counts does not raise, lower or alter that claim's verification. If the image is decorative, it is decorative. If it was produced from data, the *data* supports the claim through a `sheet_range` or `data_pointer` anchor and the image `illustrates` the same claim separately — two edges, two roles, no merging. `illustrates` therefore carries invalidation policy `none`: nothing in a proof depends on it, which is exactly the property that makes it safe.

**Why this is load-bearing.** A generated or decorative image sitting beside a number reads to a human being as evidence for that number. If that edge may enter a proof closure, a picture becomes a citation, and the one mechanism here that cannot be faked — a verbatim span in a supplied source — acquires a back door. The separation must be enforced by the type system, not by the good judgment of whoever wired the graph at 2 a.m.

---

## 4. Identity: logical id and state digest

**Status: executable in `scripts/wi.py`.**

Every node carries **two** identities. This is the single most important design decision in v5 and the one most likely to be dismissed as bookkeeping.

| Identity | Form | Answers |
|---|---|---|
| `logical_id` | UUIDv7-shaped, assigned once, never changes | *Is this the same conceptual thing as before?* |
| `state_digest` | SHA-256 over the canonical serialization of the state | *Is this the exact thing that was verified?* |

```json
{
  "logical_id": "0192f3a1-7c40-7b2e-9f16-2a5c9d0e4b31",
  "node_type": "meaning.claim_atom",
  "state_digest": "sha256:9f2c1d47ab3e58b0c6d19e4f7a2b8c35de60f19a4c7b2e8d0f3a6b9c1d4e7f20",
  "supersedes_state": "sha256:1a4b7c02de95f38a6b0c2d4e7f19a3b5c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8",
  "created_at": "2026-03-14T09:22:41Z",
  "payload": {
    "text": "Between 2019 and 2022, the program served 11,800 households.",
    "quantity": 11800,
    "unit": "households",
    "temporal_scope": {"start": "2019-01-01", "end": "2022-12-31"},
    "certainty": "asserted",
    "realm": "external_fact",
    "evidence_policy": "strict"
  }
}
```

The `logical_id` is stable across every revision of that claim: shorten the sentence, translate it, move it to another chapter, and it remains the same conceptual claim. The `state_digest` changes the instant any semantic field changes.

**Verifications, decisions, waivers and attestations always bind to a `state_digest`, never to a `logical_id`.**

That asymmetry is the whole point. A verification says *this exact state was checked*. A dependency says *this conceptual thing is used here*. When a new state arrives for a logical id, every verification bound to the old digest is, by construction, not a verification of the new one.

**Without the split, staleness is undecidable.** Bind proof to the logical id alone and every edit inherits the old verification silently — a green badge over an edited sentence, which the v4 doctrine already names as worse than no badge. Bind proof to the state digest alone and the system loses the ability to say *this is the same claim you verified in March, now differently worded*: every edit becomes an unrelated new object, dependency history evaporates, and impact analysis has nothing to walk. Both are required, and they must stay separate.

---

## 5. The proof closure

**Status: executable in `scripts/wi.py` for text-derived proof; anchors over non-text media contribute to the closure only when their adapters exist.**

For a release artifact **R**, the proof closure of R is the complete set of graph states whose validity R's claim of verification depends on.

The closure of R contains:

| Layer | Contents |
|---|---|
| 1 | All semantic nodes rendered by R |
| 2 | All claim atoms used by those nodes |
| 3 | All premises those claims require |
| 4 | All evidence anchors that policy requires for those claims |
| 5 | All source versions those anchors reference |
| 6 | All authorship decisions that created consequential states in layers 1–4 |
| 7 | All waivers still active over those states |
| 8 | All verification results and judgment records that policy requires |
| 9–10 | The policy state in force at build time; the renderer identity and build state that produced R |

R's attestation is valid if and only if every state in its closure is the state that was present at build time and none of those states has been invalidated since.

This is the formal reason **a stale source can invalidate a finished PDF**. The PDF's bytes have not changed. Nothing in the document has been edited. But layer 5 of its closure contains `source.version` states, and if one of those source artifacts acquires a new version, the anchors in layer 4 that pointed into the old version are now `WI_ANCHOR_STALE`. The `supports` edges carrying those anchors have invalidation policy `hard`. The claim atoms in layer 2 lose their supported state. The attestation over R no longer describes reality.

The PDF is not wrong. **The claim that the PDF was verified is wrong**, and those are different failures with the same remedy: re-evaluate the closure and say plainly what changed. `wi verify-release` recomputes the closure against the workspace and reports drift as `INVALID` with the states that moved.

**Why this is load-bearing.** Every organization that has shipped documents has a folder of PDFs nobody can vouch for. The closure turns "we think this was checked" into a query. It also sets an honest boundary: the closure proves that the checks that were run still apply to the state they were run against. It does not prove the sources were right — a limit stated in [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) that v5 does not relax.

---

## 6. Storage

**Status: executable in `scripts/wi.py`.**

The workspace is a directory named `.wi/` containing a SQLite index and a content-addressed object store.

```
.wi/
  index.sqlite3        node, edge, state and invalidation tables
  objects/9f/2c/...    content-addressed blobs: raw source bytes, canonical
                       payloads, render outputs, sharded by digest prefix
  policy/              policy documents in force, themselves content-addressed
  builds/              build manifests and attestations
```

Large payloads never live in table rows. A row carries the digest; the bytes live in `objects/` under that digest. This keeps the index small enough to stay fast on a laptop and makes deduplication automatic: two sources with identical bytes are one object.

### 6.1 Migration sketch

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE workspace (
    workspace_id      TEXT PRIMARY KEY,
    schema_version    TEXT NOT NULL,
    normalization     TEXT NOT NULL,          -- e.g. 'nfc-1'
    canonicalization  TEXT NOT NULL,          -- e.g. 'wi-json-v1'
    created_at        TEXT NOT NULL
);

CREATE TABLE object_blob (
    digest            TEXT PRIMARY KEY,       -- 'sha256:...'
    byte_length       INTEGER NOT NULL,
    media_type        TEXT,
    stored_path       TEXT NOT NULL           -- relative to .wi/objects/
);

CREATE TABLE node (
    logical_id        TEXT PRIMARY KEY,
    node_type         TEXT NOT NULL,
    created_at        TEXT NOT NULL
);

CREATE TABLE node_state (
    state_digest      TEXT PRIMARY KEY,
    logical_id        TEXT NOT NULL REFERENCES node(logical_id),
    payload_digest    TEXT NOT NULL REFERENCES object_blob(digest),
    supersedes_state  TEXT REFERENCES node_state(state_digest),
    schema_version    TEXT NOT NULL,
    created_at        TEXT NOT NULL
);

CREATE TABLE edge (
    edge_state_digest TEXT PRIMARY KEY,
    relation          TEXT NOT NULL,
    from_logical_id   TEXT NOT NULL REFERENCES node(logical_id),
    from_state_digest TEXT REFERENCES node_state(state_digest),
    to_logical_id     TEXT NOT NULL REFERENCES node(logical_id),
    to_state_digest   TEXT REFERENCES node_state(state_digest),
    invalidation      TEXT NOT NULL,          -- hard | review | soft | none
    payload_digest    TEXT REFERENCES object_blob(digest),
    created_at        TEXT NOT NULL
);

CREATE TABLE current_state (
    logical_id        TEXT PRIMARY KEY REFERENCES node(logical_id),
    state_digest      TEXT NOT NULL REFERENCES node_state(state_digest),
    updated_at        TEXT NOT NULL
);

CREATE TABLE invalidation (
    invalidation_id       TEXT PRIMARY KEY,
    affected_state_digest TEXT NOT NULL REFERENCES node_state(state_digest),
    cause_state_digest    TEXT REFERENCES node_state(state_digest),
    reason_code           TEXT NOT NULL,      -- WI_ANCHOR_STALE, WI_DECISION_STALE, ...
    created_at            TEXT NOT NULL
);

CREATE TABLE release_build (
    build_id          TEXT PRIMARY KEY,
    target            TEXT NOT NULL,
    artifact_digest   TEXT NOT NULL REFERENCES object_blob(digest),
    closure_digest    TEXT NOT NULL,          -- digest over the sorted closure
    policy_digest     TEXT NOT NULL,
    renderer_id       TEXT NOT NULL,
    created_at        TEXT NOT NULL
);

CREATE INDEX idx_node_state_history   ON node_state(logical_id, created_at);
CREATE INDEX idx_edge_out             ON edge(from_logical_id, relation);
CREATE INDEX idx_edge_in              ON edge(to_logical_id, relation);
CREATE INDEX idx_invalidation_target  ON invalidation(affected_state_digest);
```

`idx_edge_out` and `idx_edge_in` are what make closure walks and impact walks the same cost in either direction. `idx_invalidation_target` is what makes "is this state still good?" a point lookup rather than a scan, which matters because that question is asked once per state per gate evaluation.

### 6.2 SQLite is not a concession

SQLite was chosen for the same reason `scripts/wi.py` is stdlib-only: a workspace that requires a running server cannot be handed to a reviewer, mailed to counsel, opened in an air-gapped room, or committed beside the manuscript. `.wi/index.sqlite3` is one file, inspectable with tools that ship on every operating system, readable in ten years.

A server-backed implementation is legitimate and expected at scale. The requirement is that it implement **the same interfaces and the same guarantees** — identical canonicalization, identical digests, identical closure semantics. A digest computed by a server backend and a digest computed from the local file must be the same string. Where they differ, the local file is normative.

**Why this is load-bearing.** The project's claim is that a hostile reader can check the work. A hostile reader who must first be granted database credentials cannot. Portability is not convenience here; it is the delivery mechanism for the entire accountability argument.

---

## 7. Scaling

**Status: executable in `scripts/wi.py` for the indexing and transaction strategy; cached closures and background indexing are specified.**

A single novel is tens of thousands of nodes. A multi-volume work with a large source corpus, media assets and per-frame anchors reaches millions. The design targets that range without changing its correctness model. Every technique below is a performance technique only.

| Technique | What it buys | Constraint |
|---|---|---|
| Adjacency indexes on both edge directions | Closure and impact walks stay index-driven | Both indexes must exist or one direction degrades to a scan |
| Batched transactions on ingest and atomization | Orders-of-magnitude fewer fsyncs on bulk load | A batch is all-or-nothing; a partial batch must roll back |
| Large blobs outside rows | Index stays in page cache; dedup is free | Row-to-blob references must be checked by `wi doctor` |
| Cached proof closures keyed by node-state digest | Repeat gate evaluations become lookups | Cache key is the digest; a changed digest can never hit a stale entry |
| Streamed queries with bounded result windows | Constant memory over million-row walks | Callers must tolerate partial results and continue |
| Background indexing | Faster interactive queries | **Never correctness state** |

The last row is a rule, not a tuning note. **Background indexing is an optimization and never a correctness state.** If a background index is incomplete, absent, corrupt or mid-rebuild, every gate must still produce the same verdict — more slowly. No verdict may depend on an index having finished. The moment a system says `RELEASE` because a background job had not yet flagged something, the accountability layer has been quietly deleted.

Cached closures obey the same discipline by construction: the cache key is a state digest, the digest changes whenever the state changes, so a cache hit is provably a hit on the same state. A cache that can go stale would be a cache that can lie, and this system cannot hold one.

---

## 8. Worked example

**Status: executable in `scripts/wi.py`.**

A grant narrative cites a partner needs assessment. The chain, forward:

```
source.artifact     needs_assessment.txt
      │  version of
source.version      @v2   sha256:3d81...c07f   (raw bytes, unnormalized)
      │  segment of
source.segment      seg-0042   bytes 8,912–9,144   "…served 11,800 households…"
      │  anchor into
anchor              a-0114   text_span   start_byte 8,975   end_byte 9,021
      │  supports                                            [hard]
meaning.claim_atom  c-0002    quantity 11800  unit households  2019-01-01..2022-12-31
      │  asserted_in · renders_as                             [review]
structure.paragraph p-0031    "Between 2019 and 2022, the program served 11,800 households."
      │  section of
structure.chapter   ch-02     "Demonstrated Need"
      │  built_from                                           [hard]
release.artifact    dist/narrative.pdf   sha256:4c1e...9b3a
```

`wi graph` walks it:

```
$ python3 scripts/wi.py graph --from c-0002 --depth 3

meaning.claim_atom  c-0002
  logical_id   0192f3a1-7c40-7b2e-9f16-2a5c9d0e4b31
  state        sha256:9f2c1d47…  (current)
  realm        external_fact     policy strict

  ← supports        a-0114            text_span   needs_assessment.txt@v2   [hard]
  ← qualifies       cn-0009           "counties served, not statewide"      [hard]
  → asserted_in     p-0031            structure.paragraph                   [review]
  → renders_as      p-0031            markdown                              [review]
  → renders_as      slide-07          slide outline                         [review]
  → uses_term       t-0004            "household"                           [review]

3 downstream release artifacts reach this node.
```

Now run it backwards. The partner sends a corrected assessment; `wi ingest` records `needs_assessment.txt@v3`:

```
$ python3 scripts/wi.py impact --source needs_assessment.txt

Source needs_assessment.txt: @v2 → @v3
  raw bytes changed: sha256:3d81…c07f → sha256:b7a2…41d9

Impact walk (reverse closure), 4 levels:

  L1  anchors into @v2                      2   WI_ANCHOR_STALE
  L2  claim atoms losing support            2   c-0002, c-0006
  L3  paragraphs asserting those claims     3   p-0031, p-0047, p-0102
  L4  release artifacts built from those    2   dist/narrative.pdf, dist/deck.md

Gate consequence under `strict`: HOLD (2 claims unsupported)
Cheapest repair: re-anchor c-0002 and c-0006 against @v3 — the quoted figure is
unchanged in @v3 at bytes 9,004–9,050, so both re-anchor without rewording.
```

And `wi explain` answers the question a reviewer actually asks — *why does this sentence say what it says?*

```
$ python3 scripts/wi.py explain p-0031

structure.paragraph p-0031  ·  chapter ch-02 "Demonstrated Need"
  "Between 2019 and 2022, the program served 11,800 households."

Carries 1 claim atom:

  c-0002  external_fact  ·  strict  ·  status: needs_source (was: supported)
    Supported until 2026-03-19 by anchor a-0114:
      > "Across the 2019–2022 period the program served 11,800 households
      >  in the seven-county service area."
      needs_assessment.txt@v2, bytes 8,975–9,021
    Anchor is stale: source advanced to @v3 on 2026-03-19.

  Decisions: d-0021  2026-03-11  accepted pr-0088 (figure 12,400 → 11,800)
  Waivers: none.   Judgments: none required at this policy level.

Checks run: quotation · numeric · date · entity · citation resolution · anchor integrity.
Not run: paraphrase support (needs a judgment tier, not this script).
```

That last pair of lines is Law C in its executable form. The tool says what it checked and what it did not, every time, without being asked.

---

## 9. What is executable and what is specified

| Mechanism | Status |
|---|---|
| Graph identity — logical id and state digest | Executable in `scripts/wi.py` |
| Source, meaning, structure, authorship, verification, canon nodes over text | Executable in `scripts/wi.py` |
| Edge families over text-derived nodes, with invalidation policy | Executable in `scripts/wi.py` |
| SQLite index and content-addressed object store | Executable in `scripts/wi.py` |
| `wi init · ingest · atomize · anchor · graph · impact · diff --semantic · test · explain · bundle · verify-release · doctor` | Executable in `scripts/wi.py` |
| Proof closure computation and release attestation | Executable in `scripts/wi.py` |
| Media node family and its adapters | Specified |
| Non-text source types — PDF, spreadsheet, audio, video, image, web capture | Specified, with adapter contracts in [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) |
| `release.signature`, signature verification, cached closures, background indexing | Specified |
| A compiled core in another language | Roadmap. Nothing in this release is written in Rust, and no part of the system requires it. |

---

## Related documents

- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — what a `meaning.*` node contains and how renderers consume it
- [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) — how anchors bind meaning to source bytes
- [`CANONICAL_HASHING.md`](CANONICAL_HASHING.md) — how a state digest is computed, exactly
- [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) and [`../v4/ACCOUNTABILITY_LAYER.md`](../v4/ACCOUNTABILITY_LAYER.md) — the protocol and the six laws this architecture serves
- [`../../schemas/epistemic_ledger.schema.json`](../../schemas/epistemic_ledger.schema.json) — the v4 ledger, now a view over the graph; [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
