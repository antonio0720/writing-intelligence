# Multimodal Authorship

**Status: adapter contracts and anchor types specified; text-span anchors executable.**

The shallow reading of "multimodal" is *let a model look at images*. That reading produces a feature — the system can now describe a picture — and it produces nothing that survives an edit, a review, or a question from someone who was not there.

Multimodal authorship means something narrower and harder: **shared semantic and provenance identity across media.**

A claim made in a grant narrative, spoken in a recorded briefing, charted in a slide and depicted in a storyboard panel is *one* claim with four renderings. Change the number and all four go into review. Change a character's age in chapter nine and the shot list that depicts her at that age becomes review-required. The identity is in the graph, not in the pixels — and no amount of vision capability substitutes for it.

Read this with [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md), which specifies each non-text anchor type, and [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) §2.7 for the media node family.

---

## Table of contents

1. The ingestion contract
2. The rollout order
3. Audio and voice
4. Voice privacy
5. Script ↔ shot binding
6. Storyboard continuity
7. The audio-drama production manifest
8. Chart provenance
9. Generated media
10. Rights and consent
11. Multimodal anchor benchmarks
12. What is executable and what is specified

---

## 1. The ingestion contract

**Status: specified.** One shape, implemented once per format.

```python
class IngestAdapter:
    def descriptor(self) -> AdapterDescriptor:
        """Identity, version, MIME types handled, capabilities, limits."""

    def inspect(self, source: SourceRef) -> InspectionReport:
        """Static analysis only. No decoding of content, no execution.
        Returns declared vs. sniffed type, structural counts, hazard flags."""

    def extract(self, source: SourceRef, limits: Limits) -> NormalizedSource:
        """Decode under the given limits. Returns derived objects with their
        own digests, an extractor identity, and anchorable regions."""
```

Three methods, in that order, always. `inspect` runs before `extract` because the decision to decode a file is itself a decision that should be informed by what the file claims to be and what it actually appears to be.

**No adapter gets network permission by default.** A source that references a URL, an external workbook, a remote font or a linked asset records the reference and does not fetch it. Fetching would let a supplied document choose what code runs and what host it talks to, which is Law F defeated by a hyperlink.

Binary parsers are the largest attack surface in this system, so they run under constraints that are not configurable away:

| Constraint | Why |
|---|---|
| Out-of-process execution | A parser crash or exploit does not reach the workspace |
| CPU limit | A decompression bomb consumes a budget, not a machine |
| Memory limit | Enforced by the OS, not by the parser's own bookkeeping |
| File-size limit | Checked before decoding, not discovered during it |
| Page, sheet and duration limits | Format-specific ceilings, from [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) §7 |
| Temporary filesystem | The parser sees a scratch directory and nothing else |
| MIME sniffing independent of extension | A `.txt` that is a zip is a finding, not a text file |

Breaching any limit produces `WI_SOURCE_LIMIT_EXCEEDED` with the limit named and the observed value stated, and the partial output is discarded. A partial extraction presented as a complete one is a source the system is wrong about, silently.

---

## 2. The rollout order

**Status: specified.** The order is a commitment about sequence, not a schedule.

```
PDF → DOCX → XLSX → image → audio → video
```

| Format | Why here |
|---|---|
| PDF | The dominant format for supplied evidence, and the one where hidden-text attacks are most practical |
| DOCX | Structured, well-documented, and carries tracked changes and comments that are themselves authorship records |
| XLSX | Where numbers actually live; formula dependencies make it the highest-value non-text anchor |
| Image | Region anchoring is straightforward; the hard part is refusing to let descriptions become evidence |
| Audio | Transcription is `judged`, so the anchor design matters more than the model |
| Video | Audio plus image plus time plus shot structure — everything above, composed |

**Do not promise all formats at once.** A tool that announces support for six media types on the day it ships one is making a claim its users will discover is false at the worst possible moment, which is when they have already built a workflow on it. Each adapter lands with its anchor benchmark (§11) passing, or it does not land.

---

## 3. Audio and voice

**Status: specified.**

What the audio pipeline extracts, per source:

| Feature | Kind |
|---|---|
| Transcript | Text, derived, `judged` |
| Sentence boundaries | Structural, derived from the transcript |
| Pause distributions | Acoustic measurement |
| Words per minute | Acoustic measurement over transcript alignment |
| Emphasis contours | Acoustic measurement |
| Interruption style | Acoustic measurement over multi-speaker segments |
| Rhetorical repetition | Text-derived stylistic pattern |
| Question cadence | Text-derived, with acoustic confirmation |
| Phrase recurrence | Text-derived stylistic pattern |
| Pronunciation lexicon | Acoustic, per-speaker, for rendering fidelity |

These are kept in **three layers that never merge**:

| Layer | Contains | Reliability type |
|---|---|---|
| Text-derived voice features | Phrase recurrence, sentence shape, rhetorical repetition, question cadence | `measured` against a stated corpus |
| Acoustic features | Pause distribution, WPM, emphasis contour, pronunciation | `measured` against a stated sample set |
| Judgment-tier stylistic features | Register, warmth, authority, humor, "sounds like him" | `judged`, provider named |

**Never pretend acoustic features are authorial meaning.** A speaker who pauses before a number is a speaker who paused before a number. It is not evidence of doubt, emphasis, deception, or importance. Those readings are interpretations, they belong in the judgment layer with a named provider, and they never carry a `supports` edge to a claim about what the speaker meant.

The failure this rule prevents is specific and seductive: a system that measures pause length precisely, reports it precisely, and lets the precision of the measurement launder an interpretation that has no precision at all. Measured is `measured`. What it means is `judged`. The layers exist so that the second cannot borrow the first's authority.

---

## 4. Voice privacy

**Status: specified.**

Three different things get three different names, because collapsing them is how a style tool becomes a biometric one:

| Artifact | Is | Is not |
|---|---|---|
| `voice_style_profile` | Text-derived and prosodic patterns describing how this person writes and speaks | Anything that can identify a speaker |
| `acoustic_voice_profile` | Measured acoustic characteristics of recorded speech | A model that can generate or match that voice |
| `speaker_identity_model` | A model capable of recognizing or verifying a specific speaker | Anything Writing Intelligence needs |

**Writing Intelligence does not need speaker identification to provide authorial voice continuity.** The thing an author wants — *make this sound like me* — is served by the first artifact. The second is needed only for pronunciation fidelity and prosodic matching in audio rendering. The third is a biometric system, it is regulated as one in several jurisdictions, and building it would be scope creep with legal consequences attached.

Defaults:

- **Do not store raw audio in shared cloud storage unless explicitly configured.** Local by default, like everything else.
- **Store derived metrics separately from raw media**, so that keeping the first does not require keeping the second.
- **Allow deletion of raw voice samples while preserving approved, non-identifying aggregate style metrics** where policy permits. A person who withdraws their recordings should not have to choose between that and every downstream document losing its voice calibration — but the aggregate must be non-identifying and the permission must be real.
- **Keep the consent basis attached** to the profile, not filed somewhere else. A profile whose consent record has to be looked up in another system is a profile whose consent will eventually not be looked up.

The five bases for modeling a named person's voice are unchanged from v4: [`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md).

**A voice model permission and a writing-style permission are not automatically the same permission.** Someone who agreed to have their prose style analyzed for a ghostwriting engagement has not agreed to an acoustic profile of their speech, and someone who consented to a recorded interview has not consented to a synthesis-capable model of their voice. Each is a separate grant, recorded separately, and the system asks rather than inferring the wider one from the narrower.

---

## 5. Script ↔ shot binding

**Status: specified.**

The naive production pipeline copies script text into a shot list. The copy is dead the moment the script changes, and nobody finds out.

**A script line gets a stable semantic node. A shot refers to the node, not to a copied string.**

```json
{
  "shot_id": "sh-0037",
  "sequence": "02",
  "renders": [
    {"node": "c-0002", "node_type": "meaning.claim_atom",
     "surface": "Between 2019 and 2022, the program served 11,800 households."},
    {"node": "b-0114", "node_type": "canon.beat",
     "surface": "The scale of the need lands before the ask."}
  ],
  "visual_intent": "Wide of the county intake office at opening, line already formed; hold long enough that the number reads as people.",
  "duration_target_ms": 5500,
  "review_state": "accepted"
}
```

`surface` is present so a human can read the shot list without a database. It is a **display copy, not the binding** — the binding is `node`. When `c-0002` moves from 11,800 to 12,400, the shot's `review_state` becomes review-required, and the reason is recorded as a dependency change rather than a mystery.

**If the claim changes, the shot becomes review-required.** Not automatically re-rendered, not silently updated, not left alone. A shot exists to serve a meaning, and when the meaning moves, a person has to decide whether the shot still serves it. Sometimes a wide of a waiting room works for either number and sometimes the whole visual argument was the specific figure on a whiteboard in frame.

---

## 6. Storyboard continuity

**Status: specified.**

A storyboard panel binds seven kinds of world state, each to a canon node:

| Binding | Panel declares |
|---|---|
| Character state | Which characters are present, and their canonical state at this point |
| Location state | Which location, in which canonical condition |
| Wardrobe continuity | What each character is wearing, bound to the wardrobe node |
| Object state | Which props are present and in what condition |
| Chronology | Where this sits in world time, not in narration order |
| Dialogue line | The dialogue node this panel carries |
| Narrative beat | The beat this panel discharges |

Continuity becomes a graph query instead of an act of memory. A character who acquires a scar in panel 40 has a canonical state change; every panel after it that binds her character state and does not reflect the scar is a query result, available before the shoot rather than after the edit.

The chronology binding is separate from panel order for the same reason `precedes` is separate from document order in the graph: a flashback is out of narration order and in world order, and a continuity checker that cannot tell the difference will flag every non-linear story as broken.

---

## 7. The audio-drama production manifest

**Status: specified.**

```json
{
  "cue_id": "ad-0212",
  "scene": "02.04",
  "dialogue": {
    "node": "d-0331",
    "line": "We stopped counting at eleven thousand. That was March.",
    "speaker": {"character": "char-0007", "performer": "perf-0002"},
    "voice_constraints": {
      "profile": "voice_style_profile:char-0007",
      "acoustic_profile": "acoustic_voice_profile:perf-0002",
      "consent_basis": "contract",
      "synthesis_permitted": false
    }
  },
  "sound_cue": {"id": "sfx-0088", "description": "Door latch, interior, close"},
  "ambience": {"id": "amb-0014", "description": "County office, low crowd, HVAC"},
  "music_cue": {"id": "mus-0009", "rights": "licensed", "expires_at": "2029-01-01"},
  "timing": {"start_ms": 184200, "duration_ms": 4100},
  "canonical_events": ["ev-0121"],
  "rights_state": "cleared"
}
```

`synthesis_permitted: false` beside a real performer's acoustic profile is the field that matters most in this object. A performer contract that covers recording does not cover synthesis, and the manifest carries the distinction at the cue level, where a producer will actually see it.

`canonical_events` binds the cue to world events, so a retcon in the canon registry surfaces every cue that narrates the changed event. `rights_state` is checked at build; a cue whose music license has expired is a build finding, not a discovery made by a rights holder.

---

## 8. Chart provenance

**Status: specified.**

**Charts are authored claims.** A chart asserts something about data — a trend, a comparison, a magnitude — with all the force of a sentence and none of the scrutiny, because it does not look like prose.

A chart node knows:

| Field | Holds |
|---|---|
| `source_cells` or `query` | Where the numbers came from — a `sheet_range` anchor or a `recorded_query` |
| `transformation` | What was done to them, as an ordered, inspectable list |
| `aggregation` | Sum, mean, median, rate — named, not implied by the axis label |
| `filters` | Every row exclusion, stated |
| `units` | The unit of the plotted quantity |
| `labeling` | Axis labels, legend text and the caption, as authored text |
| `referenced_by` | The claim nodes that cite this chart |

**A chart goes stale when its source data changes.** The `depends_on` edges run from the chart to the cells or query behind it, and a change to `B14` puts the chart into review even though the image bytes are untouched. That is exactly the right behavior: the image is still a correct rendering of numbers that are no longer the numbers.

Filters deserve their own row because they are where charts lie most often and most innocently. A bar chart of county outcomes that excludes two counties with incomplete data is defensible, publishable, and misleading if the exclusion is not stated. Recording the filter list makes the exclusion a fact in the graph, which means a reviewer can ask about it.

---

## 9. Generated media

**Status: specified.**

If a generated image or audio asset is used in a work, the asset carries a record:

```json
{
  "asset_id": "img-0044",
  "generated": true,
  "generator": {"identity": "if available", "model": "if available", "version": "if available"},
  "prompt_digest": "sha256:2c90f4a1...6b83",
  "seed": 41822,
  "source_assets": ["img-0012"],
  "author_approval": {"actor": "a.smith", "at": "2026-03-17T15:22:04Z"},
  "rights_status": "owned",
  "depicts_factual_claim": false,
  "role": "illustrative"
}
```

Generator identity, model and version are recorded **if available** — some pipelines do not expose them, and inventing a value to fill the field would be worse than the empty field. The prompt is stored as a digest rather than plaintext by default, because prompts routinely contain source material and confidential context; the plaintext is retained in the workspace under the same confidentiality label as its inputs.

**The edge is `illustrates`, never `supports`, unless a separate evidentiary basis exists.**

This is the single most important rule in this document. A generated image placed beside a claim about household counts reads to a human being as evidence for that claim, and it is not evidence of anything except that someone generated an image. `illustrates` carries invalidation policy `none` precisely so that nothing in a proof can ever depend on it.

**An illustration must never silently become evidence.** If the chart in the image was produced from real data, then the *data* supports the claim through a `sheet_range` or `data_pointer` anchor, and the image `illustrates` the same claim as a second, separate edge. Two edges, two roles, no merging. The separation is enforced by the type system rather than by the good judgment of whoever wired the graph, because good judgment is exactly what is unavailable at the end of a production week.

`depicts_factual_claim` exists so that the distinction is answerable by query. An illustrative rendering of a waiting room is one thing; a generated image depicting a real event that a reader will take as documentation is another, and the second requires a rights and accuracy conversation the first does not.

---

## 10. Rights and consent

**Status: specified.** Every media asset, generated or supplied, carries both blocks.

```json
{
  "rights": {
    "basis": "licensed",
    "scope": "web and print, North America, through 2029-01-01",
    "expires_at": "2029-01-01"
  },
  "identity": {
    "contains_identifiable_person": true,
    "consent_basis": "explicit_permission"
  }
}
```

| `rights.basis` | Means |
|---|---|
| `owned` | The project holds the rights outright |
| `licensed` | Used under a license, with a scope and usually an expiry |
| `public_domain` | Not under copyright |
| `permission` | Used by permission of the holder, outside a formal license |
| `unknown` | **Not yet determined.** A real state, recorded as such |

| `identity.consent_basis` | Means |
|---|---|
| `self` | The subject is the author |
| `contract` | Covered by a signed agreement |
| `explicit_permission` | The subject agreed to this use, specifically |
| `public_figure_context` | A public figure in a context where the use is customary |
| `unknown` | **Not yet determined.** A real state, recorded as such |

`unknown` is a permitted value in both blocks and is the most important one. A system that required a rights answer before an asset could be added would be a system whose users type `owned` to get past the dialog. An honest `unknown` is a finding: it appears in the gate report, it is a release condition an operator can configure, and it survives until somebody actually answers it.

An expired `expires_at` is a build finding on every artifact that uses the asset. Rights expire quietly and documents outlive them, which is how an organization ends up distributing a report containing a photograph it stopped being allowed to use two years ago.

---

## 11. Multimodal anchor benchmarks

**Status: specified.** No adapter ships without its benchmark passing.

Every supported anchor type gets an **exact round-trip test against the exact source version**: construct the anchor, resolve it against the recorded `source_state_digest`, and confirm the resolved content matches the recorded digest byte for byte.

| Anchor type | Round trip |
|---|---|
| Text span | Byte offsets → resolved bytes → `quote_digest` match |
| PDF page/region | Page and bbox → re-rendered region → `region_render_hash` match, and extracted text → `text_hash` match |
| Spreadsheet cell/range | Sheet and range → cell values → `cell_values_hash` match, with `display_values` and `raw_values` both compared |
| Audio timecode | Start and end ms → decoded segment → `audio_segment_hash` match at the recorded encoding |
| Image crop | Normalized region → cropped pixels → `region_hash` match |
| Video frame interval | Frame indexes and PTS → decoded frames → per-frame `frame_hash` match |

The benchmark is exact rather than approximate because approximate anchor resolution is indistinguishable from a broken anchor that happens to land near the right place. A PDF region that re-renders to a *similar* image is a region whose bounding box may have shifted a line, and the claim it supports may now be anchored to the sentence above the one that says the thing.

**A round-trip failure is a shipping blocker for that adapter, not a known issue.** The whole value proposition of an anchor is that resolving it reproduces the evidence. An adapter whose anchors resolve to approximately the right place has replaced a checkable guarantee with a plausible one, which is the substitution this project exists to refuse.

---

## 12. What is executable and what is specified

| Mechanism | Status |
|---|---|
| `text_span` anchors, resolution, quote digests, staleness | Executable in `scripts/wi.py` |
| Source confidentiality labels applied to media assets | Executable in `scripts/wi.py` |
| `illustrates` vs. `supports` edge separation in the graph model | Executable in `scripts/wi.py` for text-derived nodes |
| The `IngestAdapter` contract and out-of-process parser sandbox | Specified |
| PDF, DOCX, XLSX, image, audio and video adapters | Specified — none ships in this build |
| Audio feature extraction and the three-layer separation | Specified |
| `voice_style_profile` / `acoustic_voice_profile` / `speaker_identity_model` distinction | Specified |
| Script ↔ shot binding, storyboard continuity, audio-drama manifest | Specified |
| Chart provenance and data-dependency staleness | Specified |
| Generated-media provenance records | Specified |
| Rights and consent blocks on media assets | Specified |
| Multimodal anchor round-trip benchmarks | Specified |

---

## Related documents

- [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) — every non-text anchor type, in full
- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — the media node family and the `illustrates` rule
- [`WORKSPACE.md`](WORKSPACE.md) — where media assets and their derived objects are stored
- [`POLICY_AS_CODE.md`](POLICY_AS_CODE.md) — the ingestion and privacy policy adapters run under
- [`CONSTITUTION.md`](CONSTITUTION.md) — Law D and Law F, which the adapter boundary implements
- [`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md) — the five bases for modeling a named person's voice
- [`../v4/SOURCE_HYGIENE.md`](../v4/SOURCE_HYGIENE.md) — why binary parsers are the largest attack surface here
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
