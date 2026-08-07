# Evidence Anchors

The span lock is the strongest idea in v4. A claim is supported when a specific passage of a supplied source can be quoted verbatim beside it, located exactly, and checked by string comparison by someone who does not trust the system. That mechanism is the one anti-fabrication defense in this project that does not depend on anybody being careful.

**v5 generalizes the span lock. It does not replace it with embeddings.**

A text span is one kind of anchor. A PDF region, a spreadsheet range, an image region, an audio interval, a video interval and a data pointer are others. Every one of them keeps the property that made the original work: an anchor names an exact location in an exact byte state, and resolving it either reproduces the evidence or fails loudly.

Read this with [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) for the node and edge model, and [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) for the verification statuses anchors feed.

---

## 1. The anchor contract

Every anchor, of every type, carries the same four fields:

| Field | Meaning |
|---|---|
| `anchor_id` | Stable identity of this anchor |
| `source_logical_id` | Which source artifact, across all its versions |
| `source_state_digest` | Which exact byte state of that artifact — `sha256` of the raw bytes |
| `anchor_type` | Which resolution procedure applies |

Everything after those four is type-specific. An anchor without `source_state_digest` is not an anchor; it is a suggestion.

---

## 2. Anchor types

### 2.1 `text_span`

**Status: executable — `wi anchor`.**

```json
{
  "anchor_id": "a-0114",
  "source_logical_id": "0192f3a1-7c40-7b2e-a001-8c4d1e9f0b22",
  "source_state_digest": "sha256:3d81c9a4e07b5f2a1c8d3e6f9a0b4c7d2e5f8a1b4c7d0e3f6a9b2c5d8e1f4c07",
  "anchor_type": "text_span",

  "start_byte": 8975,
  "end_byte": 9021,
  "quote": "the program served 11,800 households",
  "quote_digest": "sha256:7b1e0c95d3f8a2461c0b9e7d4a3f6c81b25e0d9f7a4c3b6e1d8f0a2c5b7e9d31",

  "encoding": "utf-8",
  "normalization_applied": "none",
  "resolves": true
}
```

Byte offsets, not character offsets, and not line and column. Bytes are what the digest was taken over, so bytes are what the anchor addresses. `quote` is present so a human can read the evidence without the tool; `quote_digest` is present so a machine can confirm the quote was not edited after the fact.

### 2.2 `pdf_region`

**Status: specified.** Adapter contract below.

```json
{
  "anchor_id": "a-0211",
  "source_logical_id": "0192f3a1-7c40-7b2e-a044-1b7c2e5d8f30",
  "source_state_digest": "sha256:c41a...9e02",
  "anchor_type": "pdf_region",

  "page": 14,
  "bbox": {"x0": 72.0, "y0": 486.2, "x1": 523.4, "y1": 512.8, "units": "pt"},

  "extracted_text": "Across the 2019-2022 period the program served 11,800 households",
  "text_hash": "sha256:2f9d...4a11",
  "extractor": {"id": "wi-pdftext", "version": "5.0.0"},

  "region_render_hash": "sha256:8c30...b7f4",
  "render": {"dpi": 200, "colorspace": "gray", "renderer": "wi-pdfraster@5.0.0"}
}
```

`region_render_hash` is a hash of the rendered image of that page region, and it is not redundant with `text_hash`.

**Why the page-image hash matters: it prevents a text extractor from being the sole root of trust.** PDF text extraction is an interpretation. Different extractors disagree about reading order in multi-column layouts, about ligatures, about whether a figure caption belongs to the paragraph above or below, and about text that is drawn but visually covered. If the only evidence that page 14 says something is what one extractor reported, then upgrading the extractor can silently change what a source "says" — and a proof would move without any source moving. With a render hash, the visual state of the region is pinned independently. The extractor's output becomes a *derived* claim about the region rather than the region itself.

### 2.3 `sheet_range`

**Status: specified.**

```json
{
  "anchor_id": "a-0330",
  "source_logical_id": "0192f3a1-7c40-7b2e-a077-3e9f1a4b6c28",
  "source_state_digest": "sha256:b7a2...41d9",
  "anchor_type": "sheet_range",

  "sheet": "WaitTimes2022",
  "range": "D14:D14",
  "cell_values_hash": "sha256:5e8a...0c93",
  "display_values": ["38%"],
  "raw_values": [0.38],
  "number_formats": ["0%"],
  "extractor": {"id": "wi-xlsx", "version": "5.0.0"}
}
```

Both `display_values` and `raw_values` are recorded because they are different evidence. A claim that quotes "38%" is a claim about the display value. A claim that computes from the figure is a claim about the raw value. `0.38` displayed as `38%` and `0.3849` displayed as `38%` are the same evidence for the first and different evidence for the second.

### 2.4 `image_region`

**Status: specified.**

```json
{
  "anchor_id": "a-0402",
  "source_logical_id": "0192f3a1-7c40-7b2e-a091-9d0c3f5a7b14",
  "source_state_digest": "sha256:1f6d...cc80",
  "anchor_type": "image_region",

  "region": {"x": 0.184, "y": 0.402, "w": 0.311, "h": 0.166, "coords": "normalized"},
  "region_hash": "sha256:a904...37bd",
  "region_render": {"resample": "none", "colorspace": "srgb"},

  "description": {
    "text": "A line chart showing wait times declining from 2019 to 2022.",
    "basis": "judged",
    "produced_by": "vision_capability",
    "supports_claims": false
  }
}
```

Normalized coordinates so the anchor survives a resolution change; a region hash so the pixels are pinned regardless.

**The rule: a vision-model description is `judged`.** It is recorded, it is useful, it is labeled with its basis in the three-word vocabulary from [`../v4/ACCOUNTABILITY_LAYER.md`](../v4/ACCOUNTABILITY_LAYER.md), and it never carries a `supports` edge on its own. **An image does not prove an interpretation merely because a model described it.** If the chart's underlying numbers matter, the numbers need a `sheet_range` or `data_pointer` anchor into the data behind the chart. A description of a picture of a number is three removes from the number.

### 2.5 `audio_time`

**Status: specified.**

```json
{
  "anchor_id": "a-0518",
  "source_logical_id": "0192f3a1-7c40-7b2e-a103-5b2e8d1f0a67",
  "source_state_digest": "sha256:6e29...aa41",
  "anchor_type": "audio_time",

  "start_ms": 742300,
  "end_ms": 751880,
  "channel": "mixdown",

  "transcript": "we served just under twelve thousand households in that window",
  "transcript_hash": "sha256:0b73...5f2e",
  "transcriber": {"id": "wi-asr-adapter", "version": "5.0.0", "basis": "judged"},

  "audio_segment_hash": "sha256:d15c...8e70",
  "segment_encoding": {"format": "pcm_s16le", "rate_hz": 16000, "channels": 1}
}
```

Two hashes again, for the same reason as the PDF: the audio bytes for that interval are pinned independently of any transcription of them. A transcript is a derived object produced by a fallible process, and its basis is `judged`, never `verified`. A claim quoting a speaker is supported by the transcript only to the strength the policy allows for judged evidence, and the audio segment remains available for a human to check.

### 2.6 `video_time`

**Status: specified.**

```json
{
  "anchor_id": "a-0604",
  "source_logical_id": "0192f3a1-7c40-7b2e-a118-2c6f0a9d3b55",
  "source_state_digest": "sha256:39fb...71c4",
  "anchor_type": "video_time",

  "start_ms": 129000,
  "end_ms": 134500,
  "shot_id": "sh-0037",

  "representative_frames": [
    {"index": 3096, "pts_ms": 129040, "frame_hash": "sha256:aa10...42df"},
    {"index": 3210, "pts_ms": 133840, "frame_hash": "sha256:71c9...0e6b"}
  ],

  "transcript_interval": {
    "text": "the waiting list dropped by more than a third",
    "transcript_hash": "sha256:4d0a...c1b8",
    "basis": "judged"
  },

  "ocr_overlay": {
    "text": "MEDIAN WAIT: 38% LOWER",
    "ocr_hash": "sha256:9e51...6a02",
    "basis": "judged"
  }
}
```

`ocr_overlay` is present only when the frame carries burned-in text. It is the most commonly cited part of a video and the least reliable to read, so it is hashed and labeled `judged` like every other extraction.

### 2.7 `data_pointer`

**Status: specified.**

```json
{
  "anchor_id": "a-0711",
  "source_logical_id": "0192f3a1-7c40-7b2e-a126-7f3b1c8e0d49",
  "source_state_digest": "sha256:5c8e...b302",
  "anchor_type": "data_pointer",

  "pointer_kind": "json_pointer",
  "pointer": "/counties/7/metrics/median_wait_change_pct",
  "value": 0.38,
  "value_digest": "sha256:c703...19ae"
}
```

Three pointer kinds are defined. `json_pointer` addresses a location in a structured document. `row_key` addresses a record by its declared primary key rather than by position, so an inserted row does not silently move the anchor. `recorded_query` stores the query text, the engine identity and a digest of the result set:

```json
{
  "pointer_kind": "recorded_query",
  "query": "SELECT median_wait_change_pct FROM county_metrics WHERE fips = '29095'",
  "engine": {"id": "sqlite", "version": "3.45"},
  "result_digest": "sha256:e610...84fd",
  "executed_at": "2026-03-11T14:02:19Z"
}
```

A recorded query is evidence about a result at a moment, and the anchor says so. Re-running it later and getting a different digest is not a bug; it is the anchor doing its job.

---

## 3. Anchor integrity

**Status: executable in `scripts/wi.py` for `text_span`; the same procedure is specified for every other type.**

Anchor integrity is a deterministic check with three conditions. It runs before any judgment, and no proof state exists without it.

| Condition | Failure code |
|---|---|
| The anchor resolves — the location exists in the named source state | `WI_ANCHOR_INVALID` |
| The quote digest matches what resolving the anchor produces | `WI_ANCHOR_INVALID` |
| The anchor's `source_state_digest` is the current version of that source artifact | `WI_ANCHOR_STALE` |

The third condition is the one that turns a photograph into a live system. An anchor into `needs_assessment.txt@v2` is perfectly valid as a historical record and completely unusable as present support once `@v3` exists. It does not silently re-resolve against the new version — re-resolution is a decision, and decisions are recorded.

```
$ python3 scripts/wi.py anchor --check

14 anchors checked.

  OK       12
  STALE     2   a-0114, a-0115  →  needs_assessment.txt@v2 (current: @v3)

Re-anchor with:  wi anchor --rebind a-0114 --to needs_assessment.txt@v3
The quoted text is present in @v3 at bytes 9,004-9,050; the rebind is exact.
```

---

## 4. The raw-bytes rule

**Status: executable in `scripts/wi.py`.**

> **Source identity is `sha256(raw bytes)`. Bytes are never normalized before hashing.**

Not trimmed. Not NFC-normalized. Not line-ending-converted. Not re-encoded. The digest is taken over exactly what the author supplied.

Everything the system learns from a source — extracted text, a transcript, a parsed table, a rendered page image — is a **derived object with its own digest**, produced by a named extractor at a named version, and linked to the source version by a `derived_from` edge.

This separation is what lets the system make a statement no single-hash design can make:

> *PDF bytes unchanged. Text extractor upgraded from 5.0.0 to 5.1.0. Derived text state changed at pages 14 and 22. Three proof links reference those pages and require re-evaluation.*

Every clause there is separately true and separately actionable. The author is not told their source changed, because it did not. They are told the system's reading of it changed, which is a different event with a different repair. Collapse source and extraction into one hash and this becomes indistinguishable from the author's own document being altered — which is both alarming and false.

**Why this is load-bearing.** Extractors improve. Renderers change. Transcription gets better. Every one of those upgrades rewrites what the system believes documents say, and if that rewriting is invisible, then proofs quietly re-found themselves on new interpretations of unchanged evidence. The raw-bytes rule is what keeps the author's document the fixed point.

---

## 5. Retrieval is not proof

**Status: executable in `scripts/wi.py` for exact-quote and trigram candidate retrieval; BM25 and embedding retrieval are specified.**

Retrieval finds candidates. Verification decides. Those are different jobs and v5 never lets the first do the second's work.

The pipeline, in order, with no stage skippable:

```
  candidate retrieval          BM25 · trigram · exact quote · embeddings
          │                    produces candidates and nothing else
          ▼
  candidate anchor             a proposed location, unverified
          │
          ▼
  anchor integrity             resolves? quote digest matches? current version?
          │                    fails here → WI_ANCHOR_INVALID / WI_ANCHOR_STALE
          ▼
  deterministic checks         quotation · numeric · date · entity · citation
          │
          ▼
  judgment, if required        labeled `judged`, never `verified`
          │
          ▼
  policy evaluation            evidence mode, realm, legal force
          │
          ▼
  permitted proof state        supported · partially_supported · needs_source · conflicted
```

A retrieval result is exactly this shape and nothing more:

```json
{
  "candidate_anchor": {
    "source_logical_id": "0192f3a1-7c40-7b2e-a001-8c4d1e9f0b22",
    "source_state_digest": "sha256:3d81...c07f",
    "anchor_type": "text_span",
    "start_byte": 8975,
    "end_byte": 9021
  },
  "retrieval_basis": "bm25",
  "score": 12.4,
  "verification_state": "not_checked"
}
```

`verification_state` is `not_checked` at birth and stays that way until the deterministic stages run. The score is diagnostic information about the retriever. It is never evidence.

**Never `high similarity = verified`.** A passage that scores 0.94 against a claim about 11,800 households and actually says 12,400 is a highly similar passage that refutes the claim. Similarity measures topical proximity; it has no opinion about numbers, negation, dates or scope — which are precisely the dimensions where documents go wrong. Any system that promotes a similarity score to a support decision has reinvented the failure this project exists to stop, with a number attached to make it look rigorous.

---

## 6. Spreadsheet evidence

**Status: specified.**

Spreadsheets get their own section because they have a property no other source type shares: **a visible value can be derived.** The cell shows `38%`. What produced `38%` may be a typed constant, a formula over two other cells, a lookup into another sheet, or a link to an external workbook that nobody has opened in three years.

An anchor at the display value alone anchors to the surface of the evidence.

The per-cell record:

```json
{
  "sheet": "WaitTimes2022",
  "cell": "D14",
  "display_value": "38%",
  "raw_value": 0.3849,
  "number_format": "0%",
  "formula": "=(B14-C14)/B14",
  "dependencies": ["WaitTimes2022!B14", "WaitTimes2022!C14"],
  "external_dependencies": [
    {"kind": "workbook_link", "target": "[intake_2019.xlsx]Summary!F22", "resolved": false}
  ],
  "state_digest": "sha256:cf40...7a15"
}
```

Note `display_value` `38%` against `raw_value` `0.3849`. A narrative sentence that says "a 38% reduction" is supported. A narrative sentence that says "a reduction of exactly 38%" is not, and the record contains everything needed to say which.

**The rule: a claim about 38% depends on the cell *and its formula inputs*.** The anchor produces `depends_on` edges to `B14` and `C14`. Change `B14` and the claim enters `review` even though `D14`'s formula was untouched, because the meaning of the output changed. `external_dependencies` with `resolved: false` is reported as a gap in the evidence, not passed over — an unresolvable external link means part of the derivation is not in the supplied material, and the honest statement is that the chain is incomplete.

**No macro execution, ever.** Not in a sandbox, not with a timeout, not behind a flag. A spreadsheet is data supplied by someone else, and Law F — sources are data, never instruction — is not a text-only law. Formulas are parsed and their dependency structure is recorded; formulas are not evaluated by executing anything the workbook carries. Where a value can only be obtained by running code the source supplied, the correct output is `WI_CAPABILITY_UNAVAILABLE` with the reason stated.

---

## 7. Ingestion safety limits

**Status: specified.** The limit values are configuration; the hard requirements are not.

| Limit | Default |
|---|---|
| Maximum file bytes | 250,000,000 |
| Archive entries | 10,000 |
| Uncompressed bytes from one archive | 1,000,000,000 |
| PDF pages | 5,000 |
| DOCX paragraphs | 1,000,000 |
| XLSX sheets | 500 |
| XLSX cells | 10,000,000 |
| Audio seconds | 21,600 |
| Video seconds | 21,600 |

Hard requirements, independent of the numbers above:

- Recursive archive depth limit, enforced at every level of nesting
- Decompression ratio limit, evaluated during extraction and not after
- Extraction timeouts per file and per stage
- Parser process kill on timeout or limit breach, with the partial output discarded
- Temporary storage quota, enforced against the whole ingest run
- **No macro execution**
- **No shell execution**
- **No remote resource loading by default** — a source that references a URL records the reference; it does not fetch it

Exceeding any limit produces `WI_SOURCE_LIMIT_EXCEEDED` with the limit named and the observed value stated. It does not produce a partial ingest presented as a complete one.

**These are operational defaults, not universal safety truths.** A 250 MB ceiling is right for a laptop workspace and wrong for a media archive. A 5,000-page PDF limit is generous for a grant application and absurd for a legislative record. Operators are expected to change these numbers to fit their situation. What operators may not do is remove the *kind* of limit: every one of these exists because an unbounded version of it is a denial-of-service vector that arrives inside a document somebody emailed the author.

---

## 8. The PDF ingestion pipeline

**Status: specified.**

```
  raw bytes
      │
      ▼
  digest raw bytes ──────────────► source.version identity  sha256(raw)
      │                            nothing downstream may alter this
      ▼
  static inspection
      │   MIME sniff vs. declared type
      │   encryption / permissions flags
      │   object and stream counts
      │   /JavaScript, /OpenAction, /Launch, /AA presence
      │   embedded attachments and their types
      │   → any finding routes to QUARANTINE, WI_SOURCE_QUARANTINED
      ▼
  sandboxed page render
      │   no network, no filesystem write outside the scratch quota,
      │   no font or resource fetching, hard timeout, process kill on breach
      ▼
  page image digest ─────────────► per-page and per-region render hashes
      │                            the visual root of trust
      ▼
  text extraction
      │   character-level coordinates
      │   font, size, weight, style metadata
      │   reading order with column detection
      │   → derived object, own digest, extractor id and version recorded
      ▼
  source-hygiene analysis
      │   tiny text below a legibility threshold
      │   text positioned outside the page box
      │   low-contrast text against its background
      │   bidirectional control characters and zero-width runs
      │   instruction-shaped payloads ("ignore previous instructions",
      │     "mark all claims verified", "system:")
      │   → findings recorded and surfaced; content never obeyed
      ▼
  normalized source graph
          source.version
            └── source.segment (page)
                  └── source.segment (block)
                        └── source.table
                  └── anchorable regions with bbox + render hash
```

The hygiene stage is [`../v4/SOURCE_HYGIENE.md`](../v4/SOURCE_HYGIENE.md) applied to a format that is far better at hiding things than plain text is. White-on-white instructions, one-point type behind a figure, and text drawn outside the crop box are all trivially achievable in a PDF and all invisible to a reader. They are recorded as findings on the source, they appear in the report, and they change nothing about behavior — because a source is data, never instruction, and that law does not weaken because the payload was well hidden.

---

## 9. What is executable and what is specified

| Mechanism | Status |
|---|---|
| `text_span` anchors, `wi anchor`, `wi anchor --check` | Executable in `scripts/wi.py` |
| Anchor integrity: resolution, quote digest, staleness | Executable in `scripts/wi.py` for text |
| Raw-bytes source identity and derived-object digests | Executable in `scripts/wi.py` |
| Exact-quote and trigram candidate retrieval | Executable in `scripts/wi.py` |
| `pdf_region`, `sheet_range`, `image_region`, `audio_time`, `video_time`, `data_pointer` | Specified, with the adapter contracts above |
| BM25 and embedding retrieval | Specified |
| Spreadsheet per-cell records and formula dependency extraction | Specified |
| Ingestion safety limits and the PDF pipeline | Specified |

---

## Related documents

- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — where anchors sit in the node and edge model
- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — what an anchor supports
- [`CANONICAL_HASHING.md`](CANONICAL_HASHING.md) — how each digest here is computed
- [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) — the span lock in its original form
- [`../v4/SOURCE_HYGIENE.md`](../v4/SOURCE_HYGIENE.md) — prompt-injection defense on supplied documents
- [`../v4/ACCOUNTABILITY_LAYER.md`](../v4/ACCOUNTABILITY_LAYER.md) — verified, measured, judged
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
