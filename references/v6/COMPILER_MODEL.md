# Compiler Model

Meaning becomes compilable. A document is not authored per surface and then
kept in sync by hand; it is compiled from a selected set of semantic states
through a declared backend under a declared contract, and every byte the
backend emits is traceable to the state that produced it.

Everything described in this document is `**Status: specified.**`. No compiler
backend ships in `scripts/wi.py` at v6.0.0. The document exists so that the
first backend written is written against a contract rather than against a
deadline.

---

## 1. Why a compiler and not a template engine

**Status: specified.**

A template engine substitutes values into slots. That is sufficient when the
slots hold strings and the strings mean nothing to the system. It is not
sufficient here, for three reasons that are structural rather than incidental.

The first is that a semantic node is not a string. `c-0002` is a claim with a
subject, a quantity, a unit, a temporal scope, a modality and an attribution —
seventeen declared dimensions, enumerated in
[`../v5/SEMANTIC_IR.md`](../v5/SEMANTIC_IR.md). A template that renders it as
prose has made a hundred small decisions about which dimensions become words,
which become a footnote, and which are dropped. A template engine has no way to
declare those decisions and therefore no way to check them.

The second is that rendering is lossy in one direction and must not be lossy in
the other. A slide may legitimately render four claims as one sentence. It may
not render four claims as one sentence that asserts something none of the four
asserts. Nothing in a template engine distinguishes those two outcomes, because
both are string substitution that produced a shorter string.

The third is Law H, from [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md):
every transformation declares its semantic delta. Compilation is a
transformation. A backend that emits bytes without declaring what it did to the
meaning has broken the law that makes the rest of the system checkable.

So the model is a compiler: a plan, a backend with declared capabilities, a
contract on what the backend may and may not do to meaning, a source map, and
an incremental cache keyed on content rather than on time.

---

## 2. `BuildPlan`

**Status: specified.**

A build plan is the complete, frozen description of one compilation. It names
what is being compiled, from which states, under which policy, through which
backend. It is content-addressed, so two identical plans produce the same
identifier and the second one is a cache hit rather than a rebuild.

```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class SelectedState:
    """One semantic node pinned to one exact state."""
    logical_id: str          # never changes across the node's life
    state_digest: str        # sha256 over canonical serialization
    role: str                # "body" | "citation" | "caption" | "exhibit" | "appendix"


@dataclass(frozen=True)
class BuildPlan:
    plan_id: str                          # sha256 over the canonical plan body
    commit: str                           # the workspace commit being compiled
    backend: str                          # "markdown" | "json" | "html" | "pdf" | "docx" | "deck"
    backend_version: str
    structure_state_digest: str           # the structure.* subtree being laid out
    style_pack_digest: str
    policy_digest: str                    # evidence mode, realms permitted, tier ceiling
    selected: List[SelectedState] = field(default_factory=list)
    mission_contract: Optional[str] = None    # logical id of a mission.contract node
    voice_contract: Optional[str] = None      # logical id of an authorship.voice_constraint node
    locale: str = "en-US"
    constraints: Dict[str, Any] = field(default_factory=dict)   # length, slide count, reading level
    emit_source_map: bool = True

    def cache_key(self) -> str:
        """See §8. Deliberately not a function of wall-clock time."""
        raise NotImplementedError
```

Three properties of the plan are load-bearing.

It pins **states, not nodes**. A plan that named `c-0002` without a state
digest would compile differently tomorrow while claiming to be the same plan.
Pinning the digest is what allows the released artifact in
[`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) to name
exactly which version of each claim it contains.

It carries a **policy digest**, not a policy reference. Evidence mode, the set
of permitted realms and the reliability ceiling are inputs to compilation, and
a plan compiled under `standard` is not the same plan as one compiled under
`regulated` even if every other field matches. Hashing the policy rather than
naming it is what makes that difference visible in the cache key.

It declares `emit_source_map`. A backend may be asked to skip the map for a
throwaway preview. It may not skip it for anything that will be released;
[`SEMANTIC_SOURCE_MAPS.md`](SEMANTIC_SOURCE_MAPS.md) explains why an artifact
without a map is unauditable, and the release gate refuses one.

---

## 3. The `CompilerBackend` contract

**Status: specified.**

A backend is asked two questions before it is asked to build anything: what can
you do, and what will this plan cost you. Both answers are data. A backend that
cannot answer the first question honestly cannot be scheduled, because the
planner has no way to know whether the plan it is holding is expressible.

```python
from typing import Protocol


@dataclass(frozen=True)
class CompilerCapabilities:
    backend: str
    version: str

    # What the surface can physically represent.
    supports_footnotes: bool
    supports_inline_citation: bool
    supports_tables: bool
    supports_charts: bool
    supports_hyperlinks: bool
    supports_realm_markers: bool          # can it show "hypothetical" visibly?
    max_reading_level: Optional[int]

    # What the backend is permitted to vary.
    may_reorder_sentences: bool
    may_rebreak_paragraphs: bool
    may_select_wording_variant: bool
    may_shorten: bool
    may_select_chart_type: bool
    may_localize: bool

    # How it produces wording at all.
    wording_source: str                   # "verbatim" | "variant_table" | "model_backed"

    # Whether it can tell you where the bytes came from.
    emits_source_map: bool


@dataclass(frozen=True)
class BuildResult:
    plan_id: str
    artifact_bytes: bytes
    artifact_digest: str
    source_map: Optional[Dict[str, Any]]
    semantic_delta: Dict[str, Any]        # Law H: what compilation did to meaning
    proposals: List[Dict[str, Any]] = field(default_factory=list)
    stopped: bool = False                 # True when §6 fired
    unexpressible: List[Dict[str, Any]] = field(default_factory=list)


class CompilerBackend(Protocol):
    def capabilities(self) -> CompilerCapabilities: ...

    def check(self, plan: BuildPlan) -> List[Dict[str, Any]]:
        """Return every reason this plan cannot be built as written.

        Called before build. Must not emit bytes. Must report every problem,
        not the first one; a backend that stops at the first unexpressible
        node forces the author through one round trip per problem.
        """
        ...

    def build(self, plan: BuildPlan) -> BuildResult: ...
```

`check` exists as a separate call because the alternative — discovering
unexpressibility halfway through a build — produces a partial artifact, and a
partial artifact is the most dangerous thing this system can emit. It looks
finished. A deck that dropped the one slide carrying a qualifying exception is
indistinguishable, to a reader, from a deck that never had the exception.

`unexpressible` is a list on the result as well, because `check` runs against
the plan and some limits are only discovered against real content: a claim that
fits the slide in English and does not fit it in German. When that happens the
build reports it rather than truncating.

---

## 4. What a renderer may do

**Status: specified.**

The permitted variations are the ones that change how a meaning is presented
without changing what is asserted. Each is gated on a capability flag, so a
backend that does not declare the flag does not get the freedom.

| Variation | Capability flag | Constraint |
|---|---|---|
| Sentence order within a section | `may_reorder_sentences` | May not separate a claim from its qualifying exception |
| Paragraph boundaries | `may_rebreak_paragraphs` | May not split a `defines` pair across a page break in print backends |
| Approved wording variants | `may_select_wording_variant` | Variant must exist in the node's declared variant table |
| Voice profile application | — | Applies to connective tissue only; never to a quoted span |
| Citation format | `supports_inline_citation` | Target must resolve; format is presentational |
| Shortening | `may_shorten` | Only within the plan's declared length constraint, and never by dropping a dimension |
| Chart type from bound data | `may_select_chart_type` | Data binding is fixed; the chart reads the same numbers the prose reads |
| Localization | `may_localize` | A locale change is a `translates` edge, and the translated state is a state |

Two of these need their limits stated rather than implied.

**Approved wording variants** are not paraphrase. A variant table is authored,
reviewed and stored on the node; the backend picks from it. The difference
between picking from a table and generating a phrasing is the difference
between a decision that was reviewed once and a decision that is made afresh,
unreviewed, on every build.

**Shortening** never removes a dimension. A backend under a length constraint
may choose the shorter approved variant, may drop an illustrative example, may
move a citation to a footnote. It may not drop the temporal scope to save eight
characters. Dropping a scope is how `revenue grew 14% in Q3 2025 in North
America` becomes `revenue grew 14%`, which is a different and false claim.

---

## 5. What a renderer may never do

**Status: specified.**

The prohibitions are absolute and do not vary by backend, by capability flag,
or by policy mode. A backend that performs one of these has not produced a
worse document; it has produced a document that the proof carried alongside it
no longer describes.

| Prohibited | Why it is not a style question |
|---|---|
| Create a factual claim | The claim has no node, no anchor, no reliability basis, and no obligation set. Nothing in the release bundle covers it. |
| Widen scope | `in three pilot districts` to `across the state` changes the population the evidence supports. The evidence did not move. |
| Remove a qualifying exception | `except where a waiver is on file` carries the legal force. Without it the sentence asserts an obligation that does not exist. |
| Strengthen certainty | The modal lattice is `may < should < will < is < must`. Moving up it is an assertion the author did not make. |
| Change a quantity | Including rounding not declared in the plan. `11,847` to `about 12,000` is a new number with a new tolerance. |
| Change legal force | Turning a recommendation into a requirement, or a requirement into guidance. |
| Invent a citation | A plausible-looking reference that resolves to nothing is worse than no reference, because it survives a skim. |
| Hide a realm marker | A `hypothetical` or `simulation` node rendered without its marker reads as `external_fact`. |

The last one is the one most likely to be argued about on aesthetic grounds,
so the rule is stated plainly: if the backend cannot show a realm marker, the
backend does not get the node. `supports_realm_markers: false` means `check`
returns an unexpressible entry for every non-`external_fact` node in the plan,
and the author decides whether to remove the node or change the surface. The
system does not resolve that by quietly dropping the marker.

Detection is not left to inspection. Every one of these prohibitions maps onto
a check in the deterministic catalogue in
[`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md):

```
create a factual claim        -> anchor.integrity, citation.resolution
widen scope                   -> scope.spatial, scope.population, scope.temporal
remove exception              -> obligation.exception-preservation
strengthen certainty          -> modality.no-strengthening
change a quantity             -> numeric.value, numeric.unit, numeric.dimension
change legal force            -> modality.no-strengthening, definition.binding
invent a citation             -> citation.resolution
hide a realm marker           -> realm.preservation
```

The compiler runs those checks against its own output before returning it. A
backend that violates a prohibition and reports success has failed twice, and
the second failure is the one that matters.

---

## 6. The stop rule

**Status: specified.**

A model-backed renderer will, given a length constraint and a paragraph, offer
wording that reads better and means something slightly different. This is not a
defect in the model. It is what wording is for.

The rule is that when a proposed wording changes semantic state, compilation
**stops** and emits a proposal. It does not finish the document with the
original wording and file a note. It does not finish the document with the new
wording and flag it. It stops.

```python
def render_span(backend, node_state, constraints, policy):
    """The shape every model-backed backend must implement."""
    candidate = backend.propose_wording(node_state, constraints)

    reparsed = extract_semantic_state(candidate, context=node_state)
    delta = compare_claim_states(node_state, reparsed)

    if delta_is_presentation_only(delta):
        return Rendered(text=candidate, delta=delta)

    # Law A: propose, never replace.
    raise CompilationStopped(
        reason="wording_changes_semantic_state",
        node=node_state.logical_id,
        proposal=build_proposal(
            base_state=node_state.state_digest,
            proposed_text=candidate,
            delta=delta,
            author={"actor_type": "judgment_provider",
                    "provider": backend.capabilities().backend,
                    "version": backend.capabilities().version},
        ),
    )
```

`delta_is_presentation_only` is the whole decision, and it is decided against
the tiers already defined in
[`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md): `format_only`,
`whitespace_only` and `punctuation_only` pass. Every one of the twenty-eight
substantive delta classes stops the build.

### 6.1 Why stopping is the correct behaviour

**Status: specified.**

Three alternatives were considered and each fails in a specific way.

**Finish with the original wording, log the proposal.** The build succeeds, so
nobody reads the log. The proposal accumulates in a queue that is never drained
because nothing depends on draining it. Six months later the queue holds four
hundred entries and the useful ones are indistinguishable from the noise.

**Finish with the new wording, flag it.** The artifact now contains an assertion
no human approved, and the flag lives beside the artifact rather than inside
it. Anyone who receives the PDF receives the assertion and not the flag. This
is the failure mode the whole system exists to prevent.

**Ask the model to try again with a stricter instruction.** This converts a
detected semantic change into an undetected one, because the second attempt is
subject to exactly the same check and the same failure, and the loop terminates
when the check happens to pass rather than when the meaning happens to be
preserved. Retrying against a checker is search against the checker.

Stopping is the only option that leaves a human holding a decision that a human
must make. The cost is a failed build. That cost is visible, which is the point.

### 6.2 The stopped-build transcript

**Status: specified.**

```
$ wi compile --plan bp-0311 --backend deck

COMPILATION STOPPED

  plan            bp-0311
  backend         deck 0.4.0  (wording_source: model_backed)
  stopped at      slide 7 of 22

  node            c-0418
  base state      sha256:9f31c2…
  base text       "Applicants who filed before 1 March 2025 may request an
                   extension, except where a prior extension is on file."
  proposed text   "Applicants who filed before 1 March 2025 can request an
                   extension."

  SEMANTIC DELTA (deterministic)
    obligation.exception-preservation   FAIL
      base has 1 exception clause; proposal has 0
      dropped: "except where a prior extension is on file"

  PROPOSAL WRITTEN
    id            pr-0092
    author        judgment_provider · deck 0.4.0
    disposition   pending
    review with   wi proposals --id pr-0092

  SLIDES 1-6 NOT WRITTEN
    A partial deck is not emitted. Six correct slides and a missing
    seventh reads as a finished deck with a shorter argument.

  TO PROCEED
    accept the proposal    wi decide pr-0092 --accept --actor <you>
    reject and rebuild     wi decide pr-0092 --reject --actor <you>
    raise the constraint   wi compile --plan bp-0311 --max-slide-chars 260
```

The last line matters. The model shortened the sentence because it was told to.
Raising the constraint is frequently the correct resolution, and the transcript
says so rather than leaving the author to infer that the length limit caused it.

---

## 7. Backend build order

**Status: specified.**

Backends are written in this order, and the order is not a convenience:

1. **JSON** — the semantic state, serialized. No layout, no wording decisions.
2. **Markdown** — prose, structure, citations. Wording is `verbatim` or
   `variant_table`. No pagination.
3. **HTML** — Markdown plus anchors, plus the first backend where a source map
   locates something a reader can click.
4. **DOCX / PDF** — pagination, which introduces the first genuinely lossy
   constraint: a page break can separate a claim from its exception.
5. **Deck** — severe length constraints, which is where model-backed wording
   first becomes tempting and §6 first fires in anger.

JSON is first because it is the only backend where the round trip is exact. A
JSON artifact re-parsed yields the state it came from, byte for byte, which
makes it the reference implementation for every source map: if the mapping is
wrong in JSON it is wrong everywhere, and it is visible in JSON.

Markdown is second because it exercises the wording pipeline, the citation
pipeline and the realm-marker pipeline without pagination confusing the
diagnosis. When a scope check fails in a Markdown build, the cause is the
wording. When it fails in a PDF build, the cause might be the wording or might
be a page break, and separating those two is a day of work that the ordering
avoids.

Every later backend is validated against the Markdown build of the same plan.
Same plan, same selected states, same policy: the semantic deltas must match.
A PDF backend whose delta differs from the Markdown backend's delta on the same
plan has introduced a change during layout, and that is a defect regardless of
how the PDF reads.

---

## 8. Incremental compilation

**Status: specified.**

A fragment is cached under a digest of everything that could change it:

```python
import hashlib


def fragment_cache_key(
    backend_version: str,
    style_pack_digest: str,
    selected_semantic_state_digests: List[str],
    structure_state_digest: str,
    policy_digest: str,
) -> str:
    h = hashlib.sha256()
    h.update(b"wi-fragment-v1\n")
    h.update(backend_version.encode("utf-8") + b"\n")
    h.update(style_pack_digest.encode("utf-8") + b"\n")
    # Sorted: fragment identity must not depend on selection order.
    for d in sorted(selected_semantic_state_digests):
        h.update(d.encode("utf-8") + b"\n")
    h.update(b"--\n")
    h.update(structure_state_digest.encode("utf-8") + b"\n")
    h.update(policy_digest.encode("utf-8") + b"\n")
    return "sha256:" + h.hexdigest()
```

Five inputs, and each one is there because leaving it out produces a specific
wrong answer.

| Input | Omitting it causes |
|---|---|
| `backend_version` | A backend bug fix does not invalidate anything; the fixed build serves the broken bytes |
| `style_pack_digest` | A style change renders on new fragments and not on cached ones; the document is half-restyled |
| `selected_semantic_state_digests` | The claim changed and the paragraph did not; this is the failure the cache exists to prevent |
| `structure_state_digest` | A section moved, a cross-reference now points at the wrong section, and nothing rebuilt |
| `policy_digest` | The evidence mode tightened from `standard` to `strict`; cached fragments were built under the looser rule |

### 8.1 Why this beats a timestamp heuristic

**Status: specified.**

A timestamp cache rebuilds a fragment when an input file is newer than the
output. It is wrong in both directions, and the two errors have very different
costs.

It **rebuilds unnecessarily** whenever a file is touched without changing —
a checkout, a formatter run, a filesystem restore. This is wasted work and
nothing more.

It **fails to rebuild** whenever the content changed without the timestamp
moving forward: a clock skew across machines, a restore from backup writing an
older mtime, a state produced by merge rather than by edit, or an input that is
not a file at all. Under this system the third case is ordinary rather than
exotic — a semantic state can change because
[`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) resolved a merge, because
[`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) was promoted from
a simulation, or because an upstream node was repaired and invalidation
propagated. None of those touch a file the way an editor does.

The cost of the second error is the one that decides the design. A stale
fragment is not a slow build; it is a released document containing a sentence
that states last quarter's number under this quarter's proof. The bundle
verifies, because the bundle was built from the same stale cache. Nothing
anywhere disagrees.

Content addressing has no second error. If any of the five inputs differs, the
key differs and the fragment rebuilds. If none differs, the cached bytes are
the bytes the current inputs produce, and serving them is not an approximation.

### 8.2 What the cache does not key on

**Status: specified.**

Deliberately absent: the wall clock, the build host, the user, the working
directory, the order in which nodes were selected, and the presence of a source
map. The first four would make identical builds miss, which turns a cache into
a slow rebuild with extra steps. The fifth is sorted before hashing. The sixth
is handled by caching the map alongside the fragment rather than in the key,
because a fragment and its map are one artifact and separating them permits a
state where one is fresh and the other is not.

---

## 9. Mission contracts and voice contracts

**Status: specified.**

Both are compilation constraints. Neither is advice.

A **mission contract** declares what the document is for and what it must not
become. It is checked at plan time and again against the built artifact.

```yaml
# mission.contract · mc-0004
mission_id: mc-0004
document: "2026 Annual Community Report"
audience: "residents; no assumed technical background"

must_include:
  - node: c-0002          # headline outcome
    reason: "the report is required to state the outcome it reports on"
  - node: ob-0022         # the statutory obligation
    reason: "statutory disclosure"

must_not_include:
  - realm: hypothetical
    reason: "audience reads this as a record of what happened"
  - reliability_basis: judged
    reason: "no model-judged content in a statutory document"

reading_level_max: 9
length:
  unit: words
  max: 4200

on_violation: stop        # stop | propose | warn
```

`on_violation: stop` is the default for a reason. A mission contract that
warns is a comment. The contract exists because someone decided the document
must not contain hypotheticals; a build that contains one and prints a warning
has produced the document the contract forbade.

A **voice contract** constrains wording. It is an
`authorship.voice_constraint` node, and it inherits the consent rules in
[`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md): a voice may be applied only
by an actor the voice owner has authorized, and the authorization is a node
with a state, not a configuration flag.

```yaml
# authorship.voice_constraint · vc-0011
voice_id: vc-0011
owner: "antonio"
authorized_actors:
  - actor_type: authorized_editor
    identity: "editorial-team"
  - actor_type: deterministic_engine
    identity: "markdown-backend"

applies_to:
  - connective_tissue
  - section_openings
never_applies_to:
  - quoted_span
  - statutory_text
  - definition_body

declared_preferences:
  - "no rhetorical questions"
  - "no second person in body prose"
  - "sentences under 34 words in body prose"

measured_targets:
  mean_sentence_length: {min: 14, max: 26}
  subordinate_clause_ratio: {max: 0.42}
  passive_voice_ratio: {max: 0.18}
```

`never_applies_to` is the load-bearing half. A voice profile applied to a
quoted span rewrites someone else's words in the author's style and presents
the result inside quotation marks. Applied to statutory text it alters legal
force. Applied to a definition body it changes what a term means everywhere the
term is used, which is the widest possible blast radius from the smallest
possible edit.

---

## 10. Voice is three readings, never one score

**Status: specified.**

A backend reports voice conformance as three separate values with three
different reliability bases. They are never combined.

| Reading | Basis | What it is | What it cannot tell you |
|---|---|---|---|
| Measured features | `measured` | Sentence length distribution, clause ratios, passive ratio, vocabulary overlap with a declared corpus | Whether the result sounds like the author |
| Declared preferences | `human-declared` | The author said: no rhetorical questions, no second person | Whether the preference was honoured in a case the rule does not cover |
| Judged resemblance | `judged` | A judgment provider's assessment, with provider, version and prompt digest recorded | Anything, without the provider's identity attached |

```json
{
  "voice_report": {
    "contract": "vc-0011",
    "measured": {
      "basis": "measured",
      "mean_sentence_length": 21.4,
      "in_range": true,
      "subordinate_clause_ratio": 0.39,
      "in_range": true,
      "passive_voice_ratio": 0.23,
      "in_range": false,
      "method": "deterministic parse; counts reproducible from artifact bytes"
    },
    "declared": {
      "basis": "human-declared",
      "rhetorical_questions": 0,
      "second_person_in_body": 2,
      "violations": ["section 3 paragraph 2", "section 7 paragraph 1"]
    },
    "judged": {
      "basis": "judged",
      "provider": "voice-resemblance",
      "provider_version": "2.1.0",
      "prompt_digest": "sha256:41a0c7…",
      "verdict": "close",
      "note": "one reading, not a measurement"
    }
  }
}
```

### 10.1 Why a blended score is forbidden

**Status: specified.**

Averaging these produces a number that cannot be acted on, and the reason is
not that the arithmetic is imprecise. It is that the three readings fail
differently and a single number erases which one failed.

A passive-voice ratio of 0.23 against a maximum of 0.18 is a **measurement**
against a **threshold the author set**. The remedy is mechanical: find the
passive constructions, rewrite eight of them. Two instances of second person is
a **declared preference violated in two named places**. The remedy is to edit
two paragraphs. A resemblance verdict of `close` from a provider is **one
provider's reading**, and the remedy — if there is one — is a conversation
about whether the provider is worth listening to.

Combine them into `voice: 0.81` and every one of those remedies disappears.
The author is told the document is 81% correct in a way that does not identify
a single sentence to change. Worse, the number is stable under substitution:
fixing the passive voice and introducing a second-person sentence leaves the
score roughly where it was, so the dial reports no change while the document
changed in both directions.

The same argument appears in
[`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) about the four
reliability types, in [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md)
about repair cost, and in [`ARGUMENT_GRAPH.md`](ARGUMENT_GRAPH.md) about
argument strength. It is the same argument each time because it is the same
mistake each time: unlike quantities averaged into a single number, which then
reads as a measurement of something.

---

## 11. Failure modes the contract is written against

**Status: specified.**

| Failure | What the contract does |
|---|---|
| Backend silently drops an unexpressible node | `check` must enumerate; `build` returns `unexpressible`; the release gate refuses a plan with a non-empty list |
| Model rewords a claim and the build succeeds | §6 stops; a proposal is written; no bytes are emitted |
| Cache serves a fragment built under the old policy | `policy_digest` is in the key |
| PDF page break separates a claim from its exception | Prohibition in §5; detected by `obligation.exception-preservation` against the built artifact |
| Voice profile applied to a quotation | `never_applies_to` in the voice contract; `quotation.verbatim` check fails the build |
| Localization changes a number | A locale change is a `translates` edge producing a new state; `numeric.value` runs across it |
| Two backends disagree about the delta | The Markdown build is the reference; disagreement is a backend defect (§7) |
| Artifact emitted without a source map | Release gate refuses it; see [`SEMANTIC_SOURCE_MAPS.md`](SEMANTIC_SOURCE_MAPS.md) |

---

## 12. What is executable and what is specified

| Capability | Status |
|---|---|
| `BuildPlan` and plan content addressing | **Status: specified.** |
| `CompilerBackend` protocol and `CompilerCapabilities` | **Status: specified.** |
| Markdown backend | **Status: specified.** |
| JSON backend | **Status: specified.** |
| HTML, DOCX, PDF, deck backends | **Status: specified.** |
| The §6 stop rule and proposal emission | **Status: specified.** |
| Fragment cache keying | **Status: specified.** |
| Mission contract enforcement | **Status: specified.** |
| Voice contract enforcement and the three voice readings | **Status: specified.** |
| Source map emission | **Status: specified.** |
| `wi propose`, `wi proposals`, `wi decide` — the proposal surface §6 writes into | **Status: executable in `scripts/wi.py`.** |
| `wi constraints` — reading the constraint set a plan compiles under | **Status: executable in `scripts/wi.py`.** |
| `wi why` — explaining a compiled sentence back to its argument | **Status: executable in `scripts/wi.py`.** |

The three executable rows are the reason the compiler can be specified now and
written later. The proposal surface, the constraint surface and the explanation
surface exist and are exercised. A backend written against this contract emits
into machinery that already runs.

---

## Related documents

- [`SEMANTIC_SOURCE_MAPS.md`](SEMANTIC_SOURCE_MAPS.md) — what a backend must return alongside the bytes
- [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) — the checks a build runs against its own output
- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — why a state can change without a file changing
- [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) — `outputs_changed`, and what a rebuild costs
- [`ARGUMENT_GRAPH.md`](ARGUMENT_GRAPH.md) — the reasoning a compiled sentence renders
- [`../v5/SEMANTIC_IR.md`](../v5/SEMANTIC_IR.md) — the seventeen dimensions a backend must preserve
- [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) — the delta tiers `delta_is_presentation_only` reads
- [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) — what the compiled artifact ships inside
- [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) — why the three voice readings stay separate
- [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md) — the serialization the digests are taken over
- [`../v5/SURFACES.md`](../v5/SURFACES.md) — the surface inventory backends are written for
- [`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md) — who may apply a voice, and to what
- [`../v4/LANGUAGE_TIERS.md`](../v4/LANGUAGE_TIERS.md) — reading level as a declared constraint

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
