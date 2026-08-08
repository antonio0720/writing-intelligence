# Semantic Source Maps

Every artifact a backend emits carries a map from the bytes back to the meaning
that produced them. A page region in a PDF, an anchor in an HTML document, a
shape on a slide and a line range in a script are four locators pointing at one
semantic node, and the map is what makes that a fact the system can act on
rather than a claim someone remembers.

Everything in this document is `**Status: specified.**`. No backend emits a
source map at v6.0.0, and no reverse-explanation command reads one. The
document exists because the map has to be designed before the first backend is
written; a backend retrofitted with a map produces approximate locators, and an
approximate locator is worse than none, for reasons §10 sets out.

---

## 1. Why bytes need a map

**Status: specified.**

A released PDF is where the reader meets the work. Everything upstream — the
claim node, the anchor, the obligation set, the argument, the decision that
accepted the proposal — is machinery the reader neither has nor wants. If the
only path from a sentence back to its proof runs through a person who knows the
manuscript, the proof is not carried by the release. It is carried by that
person.

That is the failure the map removes. Three consequences follow, and each is
load-bearing on its own.

**Invalidation becomes precise.** When `c-0002` changes state, the system
already knows which downstream nodes are affected — that is the propagation
described in [`../v5/STALENESS.md`](../v5/STALENESS.md). What it does not know,
without a map, is which released bytes carried that claim. It can say a
document is stale. It cannot say page 12 is stale and pages 1 through 11 are
not, and the difference between those two statements is the difference between
a rebuild and a reissue notice naming one paragraph.

**Explanation becomes reversible.** With a map, a reader who can point at a
sentence can be told what supports it. Without one, explanation only runs
forward: from a node the reader does not have to a sentence they already read.

**Audit becomes checkable by a third party.** A regulator holding the artifact
and the bundle can verify that the bytes on page 12 correspond to the state the
bundle claims, without access to the workspace. That is the entire promise of
[`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md), and the
map is the part of it that touches the released file.

---

## 2. `ArtifactLocator`

**Status: specified.**

A locator names a region of an artifact in terms the artifact's own format
understands. There is no universal coordinate system; a PDF page rectangle and
an HTML anchor are not two views of one address space, and pretending otherwise
produces locators that resolve in one format and drift in another.

```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Union


@dataclass(frozen=True)
class TextRangeLocator:
    kind: Literal["text_range"] = "text_range"
    unit: str = "utf8_byte"          # "utf8_byte" | "utf16_code_unit" | "grapheme"
    start: int = 0
    end: int = 0


@dataclass(frozen=True)
class LineRangeLocator:
    kind: Literal["line_range"] = "line_range"
    start_line: int = 1              # 1-based, inclusive
    end_line: int = 1                # inclusive
    start_col: Optional[int] = None
    end_col: Optional[int] = None


@dataclass(frozen=True)
class PageRegionLocator:
    kind: Literal["page_region"] = "page_region"
    page: int = 1                    # 1-based
    x: float = 0.0                   # PDF user space, origin bottom-left
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    rotation: int = 0
    # Quad list for a region broken across lines or columns.
    quads: List[List[float]] = field(default_factory=list)


@dataclass(frozen=True)
class DomAnchorLocator:
    kind: Literal["dom_anchor"] = "dom_anchor"
    element_id: str = ""             # emitted by the backend, stable across rebuilds
    css_path: Optional[str] = None   # fallback only; not authoritative
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None


@dataclass(frozen=True)
class ShapeLocator:
    kind: Literal["shape"] = "shape"
    slide: int = 1
    shape_id: str = ""
    run_start: Optional[int] = None   # character run within the shape's text body
    run_end: Optional[int] = None


@dataclass(frozen=True)
class TimeRangeLocator:
    kind: Literal["time_range"] = "time_range"
    stream: str = "audio"             # "audio" | "video" | "caption"
    start_ms: int = 0
    end_ms: int = 0


@dataclass(frozen=True)
class CellLocator:
    kind: Literal["cell"] = "cell"
    sheet: str = ""
    ref: str = ""                     # "B14" or "B14:D20"


ArtifactLocator = Union[
    TextRangeLocator,
    LineRangeLocator,
    PageRegionLocator,
    DomAnchorLocator,
    ShapeLocator,
    TimeRangeLocator,
    CellLocator,
]
```

`css_path` is marked non-authoritative deliberately. A CSS path is a function of
document structure, and document structure changes when a section moves; the
path then resolves to the wrong element rather than failing to resolve. An
`element_id` the backend emits is stable because the backend derives it from
the node's logical id, which by Law G never changes. The path is kept only as a
diagnostic for a human reading the map by hand.

`PageRegionLocator` carries `quads` as well as a bounding box because a sentence
that wraps across two lines is not a rectangle. The bounding box of a wrapped
sentence includes the end of the line above and the start of the line below,
which means a highlight drawn from it covers text belonging to a different
claim. The quad list is what makes the highlight correct.

---

## 3. `RenderMapping`

**Status: specified.**

One mapping is one relationship: this region of this artifact carries this
semantic state, in this role, and here is what the backend did to it on the way.

```python
@dataclass(frozen=True)
class RenderMapping:
    mapping_id: str
    logical_id: str                  # the semantic node
    state_digest: str                # the exact state rendered
    locator: ArtifactLocator
    role: str                        # "assertion" | "citation" | "caption"
                                     # | "realm_marker" | "exception" | "definition"
                                     # | "attribution" | "chart_binding" | "connective"
    presentation: Dict[str, Any] = field(default_factory=dict)
    # e.g. {"variant": "short", "shortened": true, "locale": "de-DE"}

    fidelity: str = "complete"       # "complete" | "partial" | "aggregated"
    aggregates: List[str] = field(default_factory=list)
    # populated when fidelity == "aggregated": the logical ids folded in

    delta_class: str = "none"        # from the v5 delta taxonomy; presentation tiers only
```

`role` carries more weight than it appears to. A region marked
`realm_marker` is the visible token that says a claim is `hypothetical`. Its
mapping is what lets the release gate confirm the marker was rendered rather
than merely present in the state — the prohibition in
[`COMPILER_MODEL.md`](COMPILER_MODEL.md) §5 against hiding a realm marker is
enforced by looking for a `realm_marker` mapping and failing when the node has a
non-`external_fact` realm and the mapping is absent.

`fidelity` exists because rendering legitimately folds. A slide bullet may
express three claims. `aggregated` with the three logical ids listed is an
honest description of that region; three separate `complete` mappings pointing
at overlapping quads is not, because it asserts that each claim is separately
locatable when the reader cannot separate them either.

`partial` is for the opposite case: a claim spanning a page break, where this
mapping covers one of two regions. Both mappings carry `partial` and both name
the same `state_digest`, so a consumer that highlights all mappings for a node
highlights both fragments.

---

## 4. `RenderSourceMap`

**Status: specified.**

The map is a sidecar. It is not embedded in the artifact, for two reasons: not
every format has a place to put it, and embedding changes the artifact bytes,
which changes the digest the map is supposed to describe.

```python
@dataclass(frozen=True)
class RenderSourceMap:
    map_version: str                 # "wi-sourcemap/1"
    plan_id: str
    commit: str
    backend: str
    backend_version: str
    artifact_digest: str             # sha256 of the bytes this map describes
    artifact_media_type: str
    locator_kinds: List[str]         # which kinds appear; lets a consumer refuse early
    mappings: List[RenderMapping] = field(default_factory=list)
    unmapped_regions: List[Dict[str, Any]] = field(default_factory=list)
    coverage: Dict[str, Any] = field(default_factory=dict)
    map_digest: str = ""             # sha256 over the canonical map, excluding this field
```

`artifact_digest` binds the map to exactly one set of bytes. A map whose digest
does not match the file it accompanies is not a stale map to be used with
caution; it is a map describing a different document, and every consumer treats
it as absent.

`unmapped_regions` is the honest half. A rendered document contains headers,
page numbers, a table of contents, a colophon and typographic furniture that
carries no semantic node. Those regions are listed with a reason:

```json
{
  "unmapped_regions": [
    {"locator": {"kind": "page_region", "page": 1, "x": 72, "y": 36,
                 "width": 468, "height": 12},
     "reason": "running_footer", "carries_meaning": false},
    {"locator": {"kind": "page_region", "page": 4, "x": 72, "y": 512,
                 "width": 468, "height": 96},
     "reason": "unmapped_prose", "carries_meaning": true,
     "note": "connective paragraph authored in structure, no claim node"}
  ]
}
```

The distinction between `carries_meaning: false` and `carries_meaning: true` is
what makes coverage a real number. A running footer is correctly unmapped. An
unmapped paragraph that carries meaning is a gap, and the release gate reads the
count of those rather than the count of unmapped regions.

---

## 5. A worked sidecar for a PDF region

**Status: specified.**

The artifact is `final.pdf`. Page 12 carries the headline outcome claim, its
attribution, and — because the claim is `hypothetical` under a projection — a
realm marker. The relevant slice of `final.pdf.wimap.json`:

```json
{
  "map_version": "wi-sourcemap/1",
  "plan_id": "bp-0311",
  "commit": "7c41e0a9",
  "backend": "pdf",
  "backend_version": "0.6.2",
  "artifact_digest": "sha256:b17d3f4c8a90e5216d7c0f9a4e33bb18c2a7d51e0f9b6c34a8e2d70f15c9a4b6",
  "artifact_media_type": "application/pdf",
  "locator_kinds": ["page_region"],

  "mappings": [
    {
      "mapping_id": "rm-0412",
      "logical_id": "c-0620",
      "state_digest": "sha256:3e9a71c0…",
      "locator": {
        "kind": "page_region",
        "page": 12,
        "x": 72.0, "y": 486.4, "width": 468.0, "height": 27.2,
        "rotation": 0,
        "quads": [
          [72.0, 500.0, 540.0, 500.0, 72.0, 486.4, 540.0, 486.4],
          [72.0, 513.6, 411.5, 513.6, 72.0, 500.0, 411.5, 500.0]
        ]
      },
      "role": "assertion",
      "presentation": {"variant": "canonical", "shortened": false, "locale": "en-US"},
      "fidelity": "complete",
      "delta_class": "none"
    },
    {
      "mapping_id": "rm-0413",
      "logical_id": "c-0620",
      "state_digest": "sha256:3e9a71c0…",
      "locator": {
        "kind": "page_region",
        "page": 12,
        "x": 72.0, "y": 470.8, "width": 214.0, "height": 11.0,
        "quads": [[72.0, 481.8, 286.0, 481.8, 72.0, 470.8, 286.0, 470.8]]
      },
      "role": "realm_marker",
      "presentation": {"rendered_as": "Projection — not a record of outcomes"},
      "fidelity": "complete",
      "delta_class": "none"
    },
    {
      "mapping_id": "rm-0414",
      "logical_id": "c-0620",
      "state_digest": "sha256:3e9a71c0…",
      "locator": {
        "kind": "page_region",
        "page": 12,
        "x": 72.0, "y": 452.0, "width": 468.0, "height": 10.5,
        "quads": [[72.0, 462.5, 540.0, 462.5, 72.0, 452.0, 540.0, 452.0]]
      },
      "role": "attribution",
      "presentation": {"citation_format": "author-date"},
      "fidelity": "complete",
      "delta_class": "none"
    }
  ],

  "unmapped_regions": [
    {"locator": {"kind": "page_region", "page": 12, "x": 72, "y": 36,
                 "width": 468, "height": 12},
     "reason": "running_footer", "carries_meaning": false}
  ],

  "coverage": {
    "nodes_in_plan": 214,
    "nodes_mapped": 214,
    "mappings": 611,
    "unmapped_meaning_regions": 0,
    "basis": "counted from the emitted map; not an estimate"
  },

  "map_digest": "sha256:0d4f92ae7b31c806fa25e1d7c4930bb2f68a1e5307c9d4b21fa8e63c05719d8f"
}
```

Three mappings, one node. The assertion, the realm marker and the attribution
are separately located because they are separately checkable. A release gate
verifying that a `hypothetical` claim was marked as such looks for `rm-0413`;
it does not parse the page and look for a phrase.

`coverage.basis` reads the way every count in this system reads: it says how the
number was obtained. The same discipline appears in the `unaffected` blocks in
[`../v5/STALENESS.md`](../v5/STALENESS.md) and for the same reason — a count
with no stated basis is indistinguishable from a count nobody took.

---

## 6. One node, four surfaces

**Status: specified.**

`c-0620` appears in four released artifacts. The maps are separate files, each
bound to its own artifact digest, and the four locators are of four different
kinds:

| Artifact | Locator | Value |
|---|---|---|
| `final.pdf` | `page_region` | page 12, quads at y 486.4–513.6 |
| `report.html` | `dom_anchor` | `#wi-c0620`, offsets 0–184 |
| `board-deck.pptx` | `shape` | slide 7, shape `tx-0031`, runs 0–96 |
| `narration.script` | `line_range` | lines 402–408 |

Nothing in the system tries to reconcile those four coordinate systems. There is
no common address space, and inventing one would require every backend to
translate into it, which is four opportunities to translate incorrectly.

What the four maps share is the pair `(logical_id, state_digest)`. That pair is
the join key, and it is exact: the same forty-byte digest appears in all four
maps or it does not. There is no fuzzy match, no text similarity, no nearest
region.

### 6.1 Why that makes invalidation precise rather than approximate

**Status: specified.**

When `c-0620` moves from `sha256:3e9a71c0…` to a new state, the question
"what is now stale?" is answered by a lookup, not by a search:

```python
def stale_regions(new_state_digest: str, old_state_digest: str, maps):
    """Exact. No text matching, no heuristics, no similarity threshold."""
    out = []
    for m in maps:
        for mapping in m.mappings:
            if mapping.state_digest == old_state_digest:
                out.append({
                    "artifact": m.artifact_digest,
                    "media_type": m.artifact_media_type,
                    "locator": mapping.locator,
                    "role": mapping.role,
                    "fidelity": mapping.fidelity,
                    "now_carries": old_state_digest,
                    "should_carry": new_state_digest,
                })
    return out
```

The alternative, without maps, is to know that a document containing `c-0620`
is stale and to say so at document granularity. That answer is correct and
nearly useless. It cannot distinguish a 240-page report where one footnote
changed from one where the headline finding changed, so every change produces
the same instruction: rebuild everything, reissue everything, re-review
everything. Recipients learn that a reissue notice means nothing in particular,
which is the state in which the next notice — the one that mattered — is also
ignored.

With maps the answer is: page 12 of `final.pdf`, one region on slide 7, one
anchor in the HTML, six lines of the script. Four regions across four artifacts,
each of which can be shown to a human who can decide in seconds whether the
change matters to that surface.

The `aggregated` fidelity is what keeps this honest at the edges. A slide bullet
folding three claims returns as stale when any of the three changes, and the
mapping says which three. A reader looking at that bullet is not told that one
of its three sources moved and left to guess which; the map names it.

---

## 7. Reverse explanation

**Status: specified.**

The command form is a locator, not a node:

```
$ wi explain final.pdf:12@72,486.4
```

or, where the artifact has a linear addressing scheme:

```
$ wi explain narration.script:412
```

The reader supplies where they are looking. The system supplies what stands
behind it. At no point does the reader name a claim id, a commit, a branch or a
file in the workspace.

```
$ wi explain final.pdf:12@72,486.4

ARTIFACT
  file            final.pdf
  digest          sha256:b17d3f4c…              matches the map
  map             final.pdf.wimap.json
  map digest      sha256:0d4f92ae…              verified
  built from      plan bp-0311 · commit 7c41e0a9 · pdf 0.6.2

REGION
  page 12, 72.0,486.4 468.0x27.2
  role            assertion
  fidelity        complete
  text            "Under the funding path adopted in March, the reserve
                   is projected to return to its statutory floor during
                   the 2029 fiscal year."

SEMANTIC NODE
  logical id      c-0620
  state           sha256:3e9a71c0…
  realm           hypothetical                  (marker rendered at rm-0413)
  modality        will
  reliability     judged
  attribution     Office of the Comptroller, projection of 2026-02-14

  RENDERED ALONGSIDE
    rm-0413  realm_marker   page 12, y 470.8   "Projection — not a record
                                                of outcomes"
    rm-0414  attribution    page 12, y 452.0

SUPPORT
  argument        arg-0118
  rule            policy_projection
  premises        4 required, 1 supporting
    p1  measured        reserve balance, 2025 close
    p2  human-declared  funding path adopted 2026-03-11
    p3  measured        statutory floor, current text
    p4  judged          contribution growth assumption
    s1  measured        five-year contribution history

  DEFEATERS
    d1  undercutting   contribution growth assumption fails      watch
    d2  rebutting      statutory floor amended before 2029       watch
    d3  undermining    reserve balance restated                  unmeasurable

OBLIGATIONS
  9 derived · 8 met · 1 waived
    waived   numeric.range        wv-0031, expires 2026-09-30

WHAT THIS OUTPUT DOES NOT SAY
  It does not say the projection is correct. `policy_projection` is not a
  deductive rule; a sound projection from true premises can still be wrong.
  It does not assess the contribution growth assumption, which is judged.
  d3 is unmeasurable from here: nothing in this workspace observes whether
  the 2025 close will be restated.

WHERE ELSE THIS APPEARS
  report.html      #wi-c0620
  board-deck.pptx  slide 7, shape tx-0031
  narration.script lines 402-408
```

### 7.1 What the reader is not required to know

**Status: specified.**

The transcript above is produced from three inputs: the artifact, its sidecar
map, and the bundle. The reader supplied a page and a coordinate. They were not
required to know:

- that `c-0620` exists, or that logical ids exist
- which branch the document was compiled from, or that branches exist
- the manuscript path, the workspace layout, or the repository at all
- which backend produced the PDF
- how to read a delta, an obligation set or an argument graph before asking

This is what "proof carried by the release" means in practice. The path from
bytes to reasoning runs through artifacts the reader already holds. Where the
forward direction — `wi why c-0620`, which is executable — serves someone who
already has the graph, reverse explanation serves someone who has only the
document, and that is almost everyone who will ever read it.

### 7.2 Resolution rules

**Status: specified.**

A coordinate can fall inside more than one mapping, and it can fall inside none.
Both cases have defined answers.

| Case | Answer |
|---|---|
| Inside exactly one mapping | That mapping |
| Inside several, nested | The innermost by area; the enclosing mappings are listed under `ALSO COVERING` |
| Inside several, overlapping without nesting | All of them, ordered by area ascending; no tie is broken silently |
| Inside an `aggregated` mapping | The mapping, plus every folded logical id named |
| Inside an `unmapped_region` with `carries_meaning: false` | "This region carries no claim: running footer" |
| Inside an `unmapped_region` with `carries_meaning: true` | "This region carries meaning that is not mapped to a node" — reported as a coverage gap |
| Outside every region | "No mapping covers this coordinate" — never the nearest one |

The last two rows are the ones that keep the command trustworthy. Returning the
nearest mapping to an uncovered coordinate would answer every query, which reads
as thorough and means the tool can never say it does not know. A reader who
clicks a caption and is shown the argument for the paragraph above it has been
told something false with the full apparatus of proof behind it.

---

## 8. Chart bindings and non-prose regions

**Status: specified.**

A chart is mapped through its binding, not its pixels. The `chart_binding` role
locates the plotted region and names the states that supplied the numbers:

```json
{
  "mapping_id": "rm-0501",
  "logical_id": "fig-0007",
  "state_digest": "sha256:c81b40e2…",
  "locator": {"kind": "page_region", "page": 14,
              "x": 90.0, "y": 220.0, "width": 432.0, "height": 268.0},
  "role": "chart_binding",
  "fidelity": "aggregated",
  "aggregates": ["c-0640", "c-0641", "c-0642", "c-0643", "c-0644"],
  "presentation": {"chart_type": "line", "selected_by": "backend",
                   "axis_units": {"y": "USD_thousands", "x": "fiscal_year"}}
}
```

`axis_units` is in the presentation block because a chart that plots thousands
against a claim expressed in units is a `numeric.unit` failure that no prose
check would catch — the prose is correct and the axis is not. The unit is
recorded so the check has something to compare.

Media follows the same pattern through `TimeRangeLocator`, and the rules in
[`../v5/MULTIMODAL.md`](../v5/MULTIMODAL.md) apply unchanged: a caption is a
`caption` mapping bound to the same node as the segment it describes, and a
segment whose transcript claim changed is stale at its time range rather than
across the whole recording.

---

## 9. Map integrity

**Status: specified.**

The map is signed material in the bundle and is verified in three steps before
any consumer reads a mapping:

1. `artifact_digest` in the map equals the digest of the artifact bytes.
2. `map_digest` equals the digest recomputed over the canonical map with that
   field excluded, under the serialization in
   [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md).
3. Every `state_digest` in `mappings` appears in the bundle's closure.

Step three is the one that catches the interesting tampering. An attacker who
edits page 12 and regenerates the map passes steps one and two — both digests
are internally consistent with the edited pair. They fail step three, because
the state digest the edited sentence would need is not in the closure the
bundle committed to, and adding it requires reproducing the whole closure digest
chain. The same argument appears in
[`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md); the map
inherits it rather than restating a weaker version.

Under the `hash-only` privacy profile the map ships with locators and digests
and without rendered text. Regions remain checkable, coverage remains countable,
and reverse explanation still resolves a coordinate to a node — the reader is
told what the region carries without the map carrying a second copy of the
document.

---

## 10. An artifact without a map is unauditable

**Status: specified.**

This is a definition rather than a policy preference, and it is worth stating in
those terms because it will be argued against by every backend author under
schedule pressure.

An audit asks: does this byte assert what the proof says it asserts. Answering
requires locating the bytes that carry the assertion. A backend that returns
bytes and no map has produced an artifact where that question can be attempted
only by reading the document and matching sentences to claims by hand. That
procedure has four properties that disqualify it:

**It is not reproducible.** Two auditors reading the same PDF will map sentences
to claims slightly differently, particularly where rendering folded or split.
Two runs of the same audit disagree, and neither is wrong.

**It does not scale with the document.** A 240-page report has several thousand
sentences. The manual procedure is performed on a sample, and a sampled audit
cannot say that no sentence overstates its evidence — only that the sampled ones
did not.

**It degrades silently.** A backend that begins folding two claims into one
sentence changes what the manual procedure should look for, and nothing signals
the change. The auditor's mental model drifts from the backend's behaviour, and
the drift is discovered by an error rather than by a check.

**It cannot be delegated to a third party.** The regulator holding the artifact
and the bundle cannot perform it without a person who knows the manuscript. At
that point the proof is carried by an employee, and the release is not
self-describing.

So the rule is enforced rather than encouraged: `wi verify-release` refuses a
bundle whose artifacts lack maps, and `unmapped_meaning_regions > 0` is a gate
failure with the regions listed. A backend author who cannot yet emit maps ships
a backend that produces preview artifacts. That is a real and useful thing to
ship. It is not a thing that can be released.

---

## 11. Failure modes the format is written against

**Status: specified.**

| Failure | What the format does |
|---|---|
| Map does not match the artifact | `artifact_digest` mismatch; the map is treated as absent, not as approximate |
| Backend maps only the prose it found easy | `unmapped_meaning_regions` counts the rest; the gate reads that count |
| Wrapped sentence highlighted as a rectangle | `quads` carry the true shape; the bounding box is a hint |
| Section moves and the CSS path breaks | `element_id` is authoritative; `css_path` is diagnostic |
| Three claims folded into one bullet, reported as three | `fidelity: aggregated` with `aggregates` naming all three |
| Claim split across a page break, reported as two claims | Two `partial` mappings sharing one `state_digest` |
| Chart axis in thousands, prose in units | `axis_units` recorded; `numeric.unit` compares them |
| Reader clicks whitespace and is shown a nearby argument | Uncovered coordinates return no mapping; never the nearest |
| Attacker edits a page and regenerates the map | Fails closure verification (§9 step three) |
| Map leaks the document under a redacted release | `hash-only` profile ships locators and digests without text |

---

## 12. What is executable and what is specified

| Capability | Status |
|---|---|
| `ArtifactLocator` union and the seven locator kinds | **Status: specified.** |
| `RenderMapping`, `RenderSourceMap` | **Status: specified.** |
| Sidecar emission by any backend | **Status: specified.** |
| `wi explain <artifact>:<locator>` reverse explanation | **Status: specified.** |
| Map integrity verification in the release gate | **Status: specified.** |
| Coverage counting and the unmapped-meaning gate | **Status: specified.** |
| Cross-artifact stale-region lookup | **Status: specified.** |
| `wi why` — forward explanation from a node | **Status: executable in `scripts/wi.py`.** |
| `wi capsule` — the portable explanation unit reverse explanation renders into | **Status: executable in `scripts/wi.py`.** |
| `wi obligations` — the obligation block in the transcript | **Status: executable in `scripts/wi.py`.** |
| `wi as-of` — resolving which state a released artifact carried | **Status: executable in `scripts/wi.py`.** |

The executable rows describe the graph side, which works today. What is missing
is the artifact side: nothing yet writes a locator, so nothing yet reads one.
The graph side was built first on purpose. A reverse explanation that resolves a
coordinate to a node is only worth building once the node resolves to an
explanation, and it does.

---

## Related documents

- [`COMPILER_MODEL.md`](COMPILER_MODEL.md) — the backend contract that requires the map
- [`ARGUMENT_GRAPH.md`](ARGUMENT_GRAPH.md) — the reasoning reverse explanation renders
- [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) — the obligation block in the transcript
- [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) — `outputs_changed`, resolved to regions rather than documents
- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — why a state digest changes without an edit
- [`../v5/STALENESS.md`](../v5/STALENESS.md) — propagation, which the map turns into page numbers
- [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) — the bundle the map ships inside
- [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md) — the serialization `map_digest` is taken over
- [`../v5/MULTIMODAL.md`](../v5/MULTIMODAL.md) — time-range locators and caption bindings
- [`../v5/EVIDENCE_ANCHORS.md`](../v5/EVIDENCE_ANCHORS.md) — anchors into sources, the mirror of maps into artifacts
- [`../v4/SURFACES.md`](../v4/SURFACES.md) — the surface inventory locator kinds are drawn from

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
