# The Semantic IR

The compiler boundary between what the author means and how any surface expresses it.

Every governed work in v5 has two layers. The **semantic intermediate representation** holds what is asserted, promised, defined, dramatized or recommended. The **renderings** — Markdown, DOCX, PDF, a deck, a podcast script, a subtitle track — are outputs compiled from it. The IR is the thing that gets verified. The renderings are the thing that gets read.

Read this with [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md). Every object described here is a `meaning.*` node in that graph and carries the dual identity defined there.

---

## 1. Why an IR is necessary

**Status: executable in `scripts/wi.py` for the claim atom, its dimensions, atomization, and Markdown and HTML rendering. Other targets are specified.**

Without a semantic layer, the draft file *is* the database. Everything downstream is a copy, and copies drift. Each row below is a real failure that has no detection mechanism when meaning lives only in prose:

| Situation | What goes wrong without an IR |
|---|---|
| The Markdown draft is the source of truth | Meaning has no identity apart from its current wording. Nothing survives a rewrite. |
| An editor changes a sentence in the DOCX | The DOCX silently diverges from the verified draft, and no check knows the two files were ever the same claim. |
| A deck restates a figure | The slide is a new string with no dependency link. Update the figure once and the deck keeps the old number forever. |
| A podcast script tightens a claim | "May reduce" becomes "reduces." Modality changed; no diff tool in the world reports that as a claim change. |
| A social post drops a hedge for length | The strongest version of the claim reaches the largest audience with the least review. |
| A translation shifts legal force | "Should" becomes an imperative in the target language. The obligation changed and the translator did not know it was one. |
| A sequel scene contradicts book one | Canon forks. Nobody notices until a reader does. |

With an IR, all seven have the same shape: a semantic node changed, or a rendering attempted to change one. Both are detectable, both are reportable, and only one of them is allowed.

**The governing rule:** every renderer consumes the same governed semantic state. A renderer may choose different words. It may not change what is asserted, and it may not create an assertion the graph does not contain.

**Why this is load-bearing.** The v4 span lock proved a sentence had support at the moment it was checked. It could not follow that sentence into the five other documents it was about to become. Every one of those documents faces its own reader, and the least-reviewed rendering is usually the one that travels furthest. An IR is what makes "the deck" and "the narrative" the same governed claim rather than two strings that happen to resemble each other.

---

## 2. The claim atom

**Status: executable in `scripts/wi.py`.**

The claim atom is the canonical unit of verification and the most important object in the system.

```json
{
  "logical_id": "0192f3a1-7c40-7b2e-9f16-2a5c9d0e4b31",
  "state_id": "sha256:9f2c1d47ab3e58b0c6d19e4f7a2b8c35de60f19a4c7b2e8d0f3a6b9c1d4e7f20",
  "node_type": "meaning.claim_atom",

  "surface": "Between 2019 and 2022, the program served 11,800 households.",

  "subject":   {"kind": "program", "ref": "meaning.term:t-0011", "label": "the program"},
  "predicate": {"lemma": "serve", "sense": "provided services to"},
  "object":    {"kind": "population", "ref": "meaning.term:t-0004", "label": "households"},

  "quantity": 11800,
  "unit": "households",
  "quantity_kind": "count",

  "temporal_scope": {
    "type": "closed_range",
    "start": "2019-01-01",
    "end": "2022-12-31",
    "granularity": "year",
    "surface_form": "Between 2019 and 2022"
  },

  "geographic_scope": {"type": "service_area", "ref": "meaning.constraint:cn-0009"},
  "population_scope": {"type": "served", "excludes": ["waitlisted", "referred_out"]},

  "modality": "is",
  "certainty": "asserted",
  "negation": false,
  "causal_force": "none",

  "attribution": {"type": "author", "on_behalf_of": null},
  "source_basis": "external_document",

  "realm": "external_fact",
  "evidence_policy": "strict",

  "anchors": [
    {
      "anchor_id": "a-0114",
      "anchor_type": "text_span",
      "source_logical_id": "0192f3a1-7c40-7b2e-a001-8c4d1e9f0b22",
      "source_state_digest": "sha256:3d81c9a4...c07f",
      "relation": "supports"
    }
  ],

  "exceptions": [],
  "legal_force": "representation_in_funding_application"
}
```

Read the annotation carefully. `surface` is one expression of this claim, not the claim. Everything above `surface` in importance lives in the structured fields.

**The structured quantity and date range survive a later, shorter rendering of the sentence.** Six months on, an editor compresses the paragraph to *"the program has served nearly twelve thousand households since 2019."* The surface has changed. So has the semantic content — and now the system can say exactly how:

| Dimension | Before | After | Consequence |
|---|---|---|---|
| `quantity` | 11800 | ~12000 | Numeric check fails against anchor a-0114 |
| `temporal_scope.end` | 2022-12-31 | open (`since`) | Date check fails — the source's range is closed |
| `certainty` | asserted | asserted | Unchanged |

Without structured fields, that edit is a style improvement. With them, it is two failed deterministic checks and a `review` on every rendering that carries the claim.

---

## 3. Meaning dimensions

**Status: executable in `scripts/wi.py` for extraction of quantity, unit, currency, temporal scope, modality, certainty language, attribution, negation and realm from text. The remaining dimensions are populated on author declaration.**

| Dimension | What it holds | Why a change here matters |
|---|---|---|
| `subject` | Who or what the claim is about | Changing the subject changes the claim entirely |
| `predicate` | The asserted relation | "served" vs. "enrolled" vs. "reached" are three different claims |
| `object` | What the predicate applies to | Households, individuals and applications are not interchangeable |
| `quantity` | The number, structured | The single most-checked field in the system |
| `unit` | What the quantity counts or measures | A quantity without a unit cannot be checked |
| `currency` | Denomination and, where relevant, basis year | $2.4M in 2019 dollars is a different claim from $2.4M today |
| `temporal_scope` | Point, closed range, open range, recurring | "Since 2019" and "2019–2022" are not the same assertion |
| `geographic_scope` | The territory the claim covers | County-level results stated statewide is the classic overreach |
| `population_scope` | Who is included and excluded | Determines whether a denominator is honest |
| `modality` | `is` · `may` · `should` · `must` · `will` | The most commonly altered dimension in editing, and the least noticed |
| `certainty` | `asserted` · `estimated` · `reported` · `disputed` · `hypothetical` | Hedges carry legal and scientific weight |
| `attribution` | Who is making the claim | An author's assertion and a quoted party's assertion have different burdens |
| `source_basis` | Author observation, external document, computation, canon | Sets which verification path applies |
| `negation` | Whether the claim asserts absence | Dropping a negation inverts the claim while barely changing the text |
| `causal_force` | `none` · `correlation` · `contribution` · `causation` | The line between "associated with" and "caused" is where most misreporting lives |
| `exceptions` | Enumerated carve-outs | An unqualified claim with silent exceptions is a false claim |
| `legal_force` | Representation, warranty, disclaimer, marketing, none | Determines who can be held to it and by whom |

**Not every claim needs every field.** A sentence in a memoir chapter may carry a subject, a predicate and a realm and nothing else. Populating fields that carry no content is ceremony, and ceremony erodes trust in the fields that matter.

The purpose of this table is narrow and worth stating plainly: **to make consequential changes mechanically visible where that is possible.** It is not an attempt to build a universal ontology of language, and it must not become one. A dependency model that works for quantities, dates, modality and negation is worth more than a complete theory of meaning that never ships. Where a dimension cannot be extracted, the correct behavior is to leave it null and say so — which is Law C applied to the IR itself.

---

## 4. Atomization

**Status: executable — `wi atomize`.**

The canonical verification unit is the claim atom, not the sentence. v4 already established this in [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md); v5 makes each atom an addressable object with its own identity rather than a line in a report.

Take a compound sentence:

> "The program served 11,800 households in seven counties and reduced median wait times by 38%."

`wi atomize` produces four atoms and the relations between them:

| Atom | Content | Dimensions carried |
|---|---|---|
| `c-0002` | The program served 11,800 households | quantity 11800 · unit households · predicate serve |
| `c-0003` | The service area comprised seven counties | quantity 7 · unit counties · geographic_scope |
| `c-0004` | Median wait times were reduced | predicate reduce · causal_force contribution · negation false |
| `c-0005` | The reduction was 38% | quantity 0.38 · unit ratio · quantity_kind proportion |

Plus the relations:

```
c-0003  qualifies  c-0002        the household count holds within the seven counties
c-0005  qualifies  c-0004        the magnitude belongs to the reduction, not to the count
c-0002  depends_on c-0003        the population scope is defined by the service area
```

```
$ python3 scripts/wi.py atomize draft.md --paragraph p-0031

p-0031 → 4 atoms

  c-0002  quantity=11800  unit=households   modality=is  certainty=asserted
  c-0003  quantity=7      unit=counties     modality=is  certainty=asserted
  c-0004  predicate=reduce                  modality=is  causal_force=contribution
  c-0005  quantity=0.38   unit=ratio        modality=is  attaches_to=c-0004

  relations: qualifies×2  depends_on×1
```

### 4.1 Partial support

Because the atoms are independent objects, **a compound sentence can be partially supported, and only the unsupported atom is marked.**

Suppose the supplied source states the household count and the county count but says nothing about wait times. Then:

| Atom | Status |
|---|---|
| `c-0002` | `supported` — anchor a-0114 |
| `c-0003` | `supported` — anchor a-0115 |
| `c-0004` | `needs_source` |
| `c-0005` | `needs_source` |

The paragraph's status is `partially_supported`, and the repair is precise: the author is told that the wait-time half of one sentence lacks support, not that "a sentence in chapter 2 has a problem." That precision is the whole return on atomization. A verdict an author cannot act on is a verdict they learn to ignore.

### 4.2 Over-splitting is a failure mode, and it is scored

The opposite error is real. Split *"the program served 11,800 households"* into `the program exists`, `households were served`, `the count was 11,800` and you have three atoms, two of which are unverifiable in isolation and none of which is what anyone claimed. Over-splitting produces noise that looks like rigor.

`wi atomize --score` reports two measures against the paragraph it split:

| Measure | Definition | Failing behavior |
|---|---|---|
| Reconstruction fidelity | Whether the atoms, recombined, assert exactly what the sentence asserts — no more, no less | Atoms that add or drop content |
| Independent checkability | The proportion of atoms that could be supported or refuted on their own | Fragments with no standalone truth conditions |

Both are reported as counts against a stated denominator, never as a blended score. An atom set where four of four atoms are independently checkable and reconstruction is exact passes. An atom set where three of seven are checkable is flagged `WI_CLAIM_ATOMIZATION_FAILED` with the offending fragments named, and the paragraph falls back to sentence-level verification with that fallback stated in the report.

**Why this is load-bearing.** Atomization is the mechanism that turns "this document has problems" into "this half of this sentence has a problem and here is the cheapest fix." But an atomizer that shatters prose into unverifiable dust produces a report full of red that means nothing, and the author's rational response is to stop reading it. Scoring the split is how the mechanism stays honest about its own output.

---

## 5. Renderers

**Status: executable in `scripts/wi.py` for Markdown and HTML. All other targets are specified, with the same renderer contract.**

The IR compiles to: Markdown · HTML · DOCX · PDF · EPUB · slide outline · podcast script · screenplay · subtitles · voiceover script · storyboard manifest · social bundle · email · press release · game dialogue manifest · API documentation.

Every one of them obeys one rule.

> **Renderers may change expression. They may not silently change semantic nodes.**

A renderer is free to reorder sentences, choose shorter words, split a paragraph, adjust register for a channel, or drop a subordinate clause that carries no semantic dimension. Those are expression decisions and they are the renderer's job.

A renderer may not change a quantity, widen or narrow a scope, alter modality, drop a hedge, remove a negation, strengthen a causal claim, or drop an enumerated exception. Those are semantic changes, and a renderer that makes one has stopped being a renderer.

### 5.1 When a target constraint requires semantic compression

Real targets have real limits. A social post has a character budget. A subtitle cue has a reading-speed ceiling. A slide has a line count. Sometimes the semantically complete version does not fit.

**The renderer must raise a proposal.** It does not compress and move on.

```
$ python3 scripts/wi.py bundle --target social/x --dry-run

Target social/x: 280 characters. Semantic rendering of p-0031 requires 341.

PROPOSAL pr-0207  ·  semantic compression required
  before  Between 2019 and 2022, the program served 11,800 households across a
          seven-county service area, excluding waitlisted and referred-out cases.
  after   Between 2019 and 2022, the program served 11,800 households across
          seven counties.
  drops   population_scope.excludes = [waitlisted, referred_out]
  effect  c-0002 broadens. Downstream: 1 claim, invalidation policy hard.
  routes  (a) accept, recording the broadened claim as a distinct node
          (b) reject and link to the full statement instead
          (c) rewrite the source claim so both renderings are exact

Nothing rendered. 1 proposal pending.
```

That is Law A — propose, never silently replace — applied at the renderer boundary. The `broadens` edge in [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) carries invalidation policy `hard` for exactly this reason: a claim getting stronger is the change most likely to be waved through and the change most likely to be indefensible.

**Why this is load-bearing.** Compression pressure always runs one direction: toward the shorter, more confident, more quotable sentence. Every channel constraint in existence is an argument for dropping the hedge. If the renderer is allowed to resolve that pressure by itself, the system will reliably produce its strongest claims in its least-reviewed formats.

---

## 6. Realms

**Status: executable in `scripts/wi.py`.**

Not everything in a work is a claim about the world, and treating it that way is as wrong as treating a claim about the world as decoration. Every semantic node carries a `realm`.

| Realm | Definition | Verification burden |
|---|---|---|
| `external_fact` | An assertion about the world outside the work | Evidence anchors per policy |
| `author_observation` | Something the author directly did, saw, built or owns | Labeled as the author's assertion; no source demanded |
| `fictional_canon` | True within the constructed world | Checked against `canon.*` nodes for consistency, never against external sources |
| `hypothetical` | An explicitly conditional or counterfactual construction | Its premises are checkable; the conditional is not |
| `simulation` | Output of a stated model under stated assumptions | The model, inputs and assumptions are checkable; the output inherits their status |
| `rhetorical` | Framing with no checkable content | None |

Realm is a graph property, not a formatting decision. It stays attached whether or not the surface displays it.

### 6.1 Mixed-realm documents

A serious nonfiction narrative routinely mixes established fact, documented reconstruction, reasoned speculation and outright dramatization — sometimes within one paragraph. A speculative-fiction work grounded in real science mixes canon and external fact the other direction. Both are legitimate forms. Both are dangerous when the labels are lost.

An author can write the realms explicitly during drafting:

```markdown
[FACT] The county recorded 412 eviction filings in March 2021.

[INFERENCE] Filings of that volume in a single month exceed the court's
stated docket capacity, which suggests hearings were consolidated.

[DRAMATIZATION] Maria counted the notices on the counter twice before
she let herself understand what the stack meant.
```

`wi ingest` reads those markers, assigns `external_fact`, `inference` under `external_fact`, and a `fictional_canon` node inside a declared reconstruction respectively — and then **the markers come out of the rendered prose**. The published page reads as prose. The graph keeps the labels permanently.

That separation is the point. A reader should not have to read bracket tags to follow a narrative. A fact-checker, an editor, a lawyer or the author at 2 a.m. two years later must be able to ask which sentences were which, and get an exact answer.

**Why this is load-bearing.** The most damaging error in mixed-realm work is not a wrong fact. It is a dramatized detail that later gets quoted as a documented one — usually by someone who was not the author, reading a rendering that dropped the distinction. Once the realm is in the graph, that quotation has a checkable answer instead of a debate.

---

## 7. Mathematical and tabular claims

**Status: specified.** The formula and table node types and their binding rules are defined here; `wi atomize` recognizes numeric claims that reference a table or figure and records the dependency, but the dimensional checker and spreadsheet adapter are contracts, not shipped code.

### 7.1 Formula nodes

A number in a narrative is very often not a source figure. It is the output of a calculation whose inputs are source figures. Treating the output as a bare claim loses every dependency that produced it.

```json
{
  "node_type": "meaning.formula",
  "logical_id": "0192f3a1-7c40-7b2e-b117-6d2a0f3c8e41",
  "expression": "(baseline_median - current_median) / baseline_median",
  "symbols": {
    "baseline_median": {"unit": "days", "source": "anchor:a-0141"},
    "current_median":  {"unit": "days", "source": "anchor:a-0142"}
  },
  "assumptions": [
    "Median computed over completed applications only",
    "Baseline period is calendar 2019"
  ],
  "computed": {"value": 0.38, "unit": "ratio", "rounding": "half_up", "places": 2},
  "dimensional_check": {"status": "pass", "result_unit": "dimensionless"}
}
```

The dimensional check is deterministic and it catches a specific, common, embarrassing class of error: a rate divided by a count and reported as a percentage, a currency subtracted from a ratio, a per-household figure multiplied by a per-county figure. Units either reconcile or they do not.

**A change to a variable definition makes every dependent narrative claim review-required.** Redefine `baseline_median` to include withdrawn applications and the formula's meaning changes even if the computed value barely moves. Every claim atom with a `derived_from` edge to this formula node enters `review`, and no gate passes until an author has looked at each one. The value changing is a numeric event. The definition changing is a semantic event, and it is the more dangerous of the two because the number on the page may not move at all.

### 7.2 Tables and figures are not opaque blobs

A table dropped into a document as an image, an HTML block or a pasted grid is a wall the dependency system cannot see through. In v5 a table node binds:

| Binding | Content |
|---|---|
| `data_source` | The source version and range the data came from |
| `transformation` | The filter, aggregation or join applied, stated explicitly |
| `display_formatting` | Rounding, units, currency, thousands separators, suppression rules |
| `row_semantics` | What one row means — one household, one month, one county |
| `column_semantics` | What each column asserts, with unit and definition |
| `caption_claim` | The claim atom the caption itself asserts |
| `notes` | Footnotes, exclusions and denominators that qualify the cells |

The payoff is concrete. A sentence that says *"Table 14 shows a 38% reduction in median wait times"* does not merely sit near Table 14. It binds to the **cell** — table 14, row `median_wait_days`, column `change_pct` — through a `data_pointer` anchor described in [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md).

When the figure updates, that binding does the work automatically:

```
$ python3 scripts/wi.py impact --table t-0014

t-0014 recomputed from wait_times.xlsx@v4
  cell [median_wait_days, change_pct]  0.38 → 0.31

Impact:
  c-0005   quantity 0.38 no longer matches bound cell        WI_CLAIM_UNSUPPORTED
  p-0031   paragraph asserting c-0005                        review
  slide-07 renders c-0005                                    review
  script-podcast-ep12 renders c-0005                         review

Gate consequence under `strict`: HOLD.
Repair: update c-0005 to 0.31 and re-render 3 targets, or restate the claim
against the prior table version with the period named in the text.
```

**Why this is load-bearing.** "The narrative said 38% and the appendix table said 31%" is one of the most common findings in grant audits, financial reviews and investigative corrections — and it is almost never dishonesty. It is a figure that got updated in one place. Binding the sentence to the cell makes that class of error structurally impossible to commit quietly.

---

## 8. What is executable and what is specified

| Mechanism | Status |
|---|---|
| Claim atom object, dual identity, meaning dimensions from text | Executable in `scripts/wi.py` |
| `wi atomize`, partial support, over-splitting scores | Executable in `scripts/wi.py` |
| Realms, mixed-realm markers, marker stripping on render | Executable in `scripts/wi.py` |
| Markdown and HTML renderers, renderer proposal protocol | Executable in `scripts/wi.py` |
| DOCX, PDF, EPUB, slides, podcast, screenplay, subtitles, voiceover, storyboard, social, email, press release, game dialogue, API docs | Specified |
| Formula nodes and dimensional checking | Specified |
| Table and figure binding, cell-level `data_pointer` anchors | Specified |

---

## Related documents

- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — the identity system every node here depends on
- [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) — how a claim atom binds to source bytes
- [`CANONICAL_HASHING.md`](CANONICAL_HASHING.md) — how a claim atom's `state_id` is computed
- [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) — find, classify, verify, gate
- [`../v4/PROPOSAL_PROTOCOL.md`](../v4/PROPOSAL_PROTOCOL.md) — Law A, which the renderer boundary enforces
- [`../../schemas/epistemic_ledger.schema.json`](../../schemas/epistemic_ledger.schema.json) — the v4 claim record this IR generalizes
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
