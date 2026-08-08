# The v6 Semantic IR

The typed representation of what a work asserts, defined so that a machine can compare two states of it without reading a single sentence.

Created by **[Antonio T. Smith Jr.](https://densitysix.com)** — Founder & CEO, Density6 LLC.

The v5 IR established that meaning is stored, not inferred, and that renderings are outputs compiled from it. That document — [`../v5/SEMANTIC_IR.md`](../v5/SEMANTIC_IR.md) — is the layer beneath this one and remains in force. What follows extends it in three directions the v5 shape could not carry: quantities that survive arithmetic, scopes that are independent of one another, and a node vocabulary wide enough that an argument, a promise and a forecast are not all filed as claims.

---

## Contents

1. [The design rule](#1-the-design-rule)
2. [The common semantic envelope](#2-the-common-semantic-envelope)
3. [ClaimAtomV6](#3-claimatomv6)
4. [The Quantity type](#4-the-quantity-type)
5. [Why binary floating point is banned](#5-why-binary-floating-point-is-banned)
6. [The first-class node types](#6-the-first-class-node-types)
7. [Independent axes: a worked contrast](#7-independent-axes-a-worked-contrast)
8. [What the IR deliberately does not hold](#8-what-the-ir-deliberately-does-not-hold)
9. [Canonicalization and identity](#9-canonicalization-and-identity)

---

## 1. The design rule

**Status: specified.**

> The IR stores only dimensions the system can use for at least one of: identity, comparison, proof obligation, invalidation, policy, rendering, merge conflict, temporal query or authority decision. A field that exists only because it sounds linguistically sophisticated is deleted.

Nine uses. A candidate field is admitted if it can name one of them and say how. It is deleted if the answer is that it captures something interesting about the sentence.

**Why it is load-bearing.** A semantic representation with no admission rule grows toward linguistics. Somebody adds `information_structure` because topic and focus are real; somebody adds `speech_act` because assertions and directives differ; somebody adds `discourse_relation` because the paragraph has one. Each is defensible in isolation and none of them is ever read. The cost is not storage. The cost is that a reviewer looking at a semantic diff cannot tell which of the twenty changed fields matter, so they stop reading the diff — and the three fields that decide whether a claim is still supported are lost inside seventeen that decide nothing. A field nobody consumes makes every field harder to trust.

The rule is applied to every field in this document. Four candidates from the v5 review that did not survive it:

| Rejected field | The argument for it | Which of the nine uses it could name |
|---|---|---|
| `register` (formal / informal) | Voice consistency across renderings | None. It is a rendering preference, so it belongs in the renderer profile, not in what is asserted. |
| `rhetorical_function` | Whether a sentence persuades or informs | None. It does not change the claim, its support, or who may accept it. |
| `sentiment` | Tone tracking | None. A negative claim and a claim about something bad are different things, and the second is not a semantic property. |
| `information_density` | Editing signal | None. It is derived from the surface, which the IR treats as an output. |

Two candidates that survived, and what each names:

| Admitted field | Use it names | How it is consumed |
|---|---|---|
| `population_scope` | Comparison, merge conflict | Two claims about the same predicate and different populations do not contradict one another, and a merge that treats them as one loses a scope somebody wrote deliberately. |
| `polarity` | Identity, proof obligation | A negated claim needs a different evidence standard from its affirmative twin: absence of evidence is not evidence of absence, and the obligation engine has to be able to tell the two apart. |

---

## 2. The common semantic envelope

**Status: specified.**

Every `meaning.*` node carries the same envelope. Only the body differs.

```json
{
  "logical_id": "0193a7c2-0f31-7a44-b6d2-1e5c9a0f7b23",
  "state_digest": "sha256:8c41f0b9d27e5a3608b1c94f7e2d06a35fc51b8047e9c2d0f3a6b9c1d4e7f205",
  "node_type": "meaning.claim_atom",
  "schema_version": "wi.meaning/6.0.0",
  "normalization": "nfc+jcs",

  "branch": "main",
  "commit": "sha256:5d2a91cf0b8e473a6c15d09fe2b84a7c3f60e1d9a4b7c2e8d0f3a6b9c1d4e7f2",

  "valid_from":  "2022-01-01T00:00:00Z",
  "valid_until": "2023-01-01T00:00:00Z",
  "known_from":  "2027-03-14T16:22:09Z",
  "known_until": null,

  "realm": "external_fact",
  "reliability_type": "verified",

  "authored_by": {"actor_id": "act-0001", "actor_kind": "human"},
  "authorized_by": "authority.grant:0193a7c2-11b4-7d3e-8f02-6a1c4e9b0d55",

  "body": { }
}
```

Field by field, and which of the nine uses admits it:

| Field | Use | What it carries |
|---|---|---|
| `logical_id` | Identity | The thing being asserted, stable across every revision of its wording. Defined in [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md). |
| `state_digest` | Identity, invalidation | This exact state. Every verification, decision and waiver binds here and nowhere else. |
| `node_type` | Policy, rendering | Which body shape follows, and which policy rules apply. |
| `schema_version` | Comparison | Two nodes under different schema versions are not compared field-by-field; they are migrated first or the comparison refuses. |
| `normalization` | Identity | Part of the hash preimage, so a node normalized differently hashes differently rather than colliding. See [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md). |
| `branch`, `commit` | Comparison, merge conflict | Where this state lives. A three-way merge needs both sides and their base. |
| `valid_from`, `valid_until` | Temporal query | When the assertion is claimed to hold in the world. Half-open. See [`BITEMPORAL_STATE.md`](BITEMPORAL_STATE.md). |
| `known_from`, `known_until` | Temporal query, invalidation | When the workspace believed it. A correction closes the old interval rather than overwriting the old state. |
| `realm` | Proof obligation | Whether this is an external fact, an author observation, fictional canon, a hypothetical, a simulation output or a rhetorical device. Six realms, six evidence standards. |
| `reliability_type` | Proof obligation | `verified`, `measured`, `judged` or `human-declared`, never collapsed into a score. See [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md). |
| `authored_by` | Authority decision | Who wrote it. Descriptive. |
| `authorized_by` | Authority decision | The grant under which it became authoritative. Not descriptive: absent this, the node is a proposal. See [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md). |

**Why the envelope is uniform.** Every mechanism above the IR — merge, freshness, temporal query, capsule export, authority check — operates on the envelope alone for the majority of its work. A merge algorithm that needed a different accessor for each of eighteen node types would grow eighteen ways to be subtly wrong, and the seventeen it was not written against would fail quietly. One envelope means one implementation of "what changed, when was it believed, and who was allowed to say so."

---

## 3. ClaimAtomV6

**Status: specified.**

```json
{
  "subject": {
    "kind": "program",
    "term": "meaning.term:t-0011",
    "label": "Program X"
  },
  "predicate": {
    "lemma": "reduce",
    "sense": "meaning.definition:d-0042",
    "argument_frame": "agent reduces measure by amount"
  },
  "object": {
    "kind": "metric",
    "term": "meaning.metric:m-0007",
    "label": "median wait time"
  },

  "quantities": [
    {
      "role": "magnitude",
      "value": "38",
      "scale": 0,
      "unit": "percent",
      "unit_system": "ratio",
      "basis": "relative_to_baseline",
      "baseline_ref": "meaning.metric:m-0007@2021"
    }
  ],

  "temporal_scope": {
    "kind": "closed_range",
    "from": "2022-01-01",
    "until": "2023-01-01",
    "granularity": "year",
    "surface_form": "during 2022"
  },
  "spatial_scope": {
    "kind": "enumerated",
    "members": ["us-oh-039", "us-oh-041", "us-oh-055",
                "us-oh-085", "us-oh-093", "us-oh-113", "us-oh-133"],
    "resolution": "county",
    "surface_form": "in seven counties"
  },
  "population_scope": {
    "kind": "subset",
    "of": "meaning.term:t-0004",
    "includes": ["enrolled"],
    "excludes": ["waitlisted", "referred_out"],
    "surface_form": "participants"
  },

  "modality": "possibility",
  "polarity": "affirmative",
  "certainty": {"kind": "hedged", "hedge": "may", "quantified": false},

  "causality": {
    "kind": "contributory",
    "direction": "subject_to_object",
    "identification": "observational",
    "confounders_declared": ["seasonal_demand", "staffing_change_2022q3"]
  },

  "attribution": {
    "kind": "author",
    "on_behalf_of": null,
    "restatement_of": null
  },

  "qualifiers": [
    {"kind": "measurement_method", "value": "meaning.definition:d-0044"},
    {"kind": "data_completeness", "value": "meaning.assumption:as-0003"}
  ],
  "exceptions": [
    {"kind": "carve_out", "node": "meaning.exception:ex-0012",
     "surface_form": "excluding the two counties that changed intake policy mid-year"}
  ],

  "terms_used": ["meaning.term:t-0011", "meaning.term:t-0004", "meaning.metric:m-0007"],

  "surface_hints": {
    "preferred_order": ["subject", "modality", "predicate", "quantities",
                        "object", "spatial_scope", "temporal_scope"],
    "register_hint": "plain",
    "may_omit": ["qualifiers"],
    "must_not_omit": ["modality", "spatial_scope", "temporal_scope"]
  }
}
```

### 3.1 Each field, and what it is for

**`subject` / `predicate` / `object`.** The triple, with every slot pointing at a registered term or definition rather than carrying a bare string. `label` is a convenience for display and is never compared. **Why:** two claims that use the same word for different things are not the same claim, and two that use different words for the same registered term are. Comparison runs on `term`, so a rewrite from "the program" to "Program X" is wording; a rewrite from `t-0011` to `t-0019` is a subject change and stops the release.

**`predicate.argument_frame`.** Which roles the predicate takes. **Why:** it is what lets a comparison notice that "reduce" gained an amount it did not have, rather than treating the added quantity as an unrelated field appearing from nowhere.

**`quantities`.** A list, not a scalar. A claim can carry a magnitude, a baseline, a margin of error and a sample size, and each is a distinct role. **Why:** "38% ± 4 points, n=1,240" is one claim with four numbers in it. Flattened into a single `quantity` field, three of them become prose and stop being checkable.

**`temporal_scope`.** When the claim says the world was that way. Distinct from `valid_from` in the envelope only in that the envelope's interval is the machine's index and this is the authored statement including its `surface_form`. **Why:** a claim about 2022 and a claim about 2023 do not contradict one another, and a system that cannot see the scope will report that they do.

**`spatial_scope`.** Where. Enumerated members, a named region, a radius, or `unbounded`. **Why:** it is the axis most often lost in compression. "In seven counties" costs three words and is the difference between a defensible finding and a national claim.

**`population_scope`.** Who. Explicit `includes` and `excludes` against a registered population term. **Why:** the same measurement over "enrolled" and over "everyone who applied" produces different numbers, and neither claim is wrong. Without the field, one of them is silently attributed to the other's denominator.

**`modality`.** `assertion`, `possibility`, `necessity`, `obligation`, `permission`, `recommendation`. **Why:** modality is legal force. "May reduce" and "reduces" carry different exposure in a funding application, and the change between them is a single word that no character diff will flag as consequential.

**`polarity`.** `affirmative` or `negated`, as a field rather than as a token inside the predicate. **Why:** a negated claim has a different evidence standard. Proving that something happened requires a record of it; proving that it did not requires an argument about the completeness of the record, which is a separate obligation the engine can only raise if it knows the polarity.

**`certainty`.** The hedge, kept apart from modality. `{"kind": "hedged", "hedge": "may"}` is not the same as a probability. **Why:** collapsing certainty into a number invents precision. "Likely" is not 0.7, and a system that stores it as 0.7 will eventually average it with something.

**`causality`.** Kind, direction, identification strategy and declared confounders. **Why:** the gap between "wait time fell while the program ran" and "the program reduced wait time" is the single most consequential unmarked upgrade in applied writing. Storing `identification` makes it visible: an `observational` identification supporting a `causal` kind is a policy violation the obligation engine can name, not a matter of taste.

**`attribution`.** Whether the workspace asserts this, is restating somebody else's assertion, or is speaking on behalf of a client. **Why:** a restatement inherits the source's reliability rather than the workspace's, and the two are not interchangeable when the source turns out to be wrong.

**`qualifiers`.** Named, typed conditions that narrow the claim without carving anything out — the measurement method, the completeness assumption, the instrument. Each points at a node. **Why:** a qualifier that lives in a footnote is prose. A qualifier that points at `meaning.definition:d-0044` becomes a dependency, so changing the measurement method invalidates every claim that used it.

**`exceptions`.** Explicit carve-outs, each pointing at an `meaning.exception` node. **Why:** an exception dropped during compression turns a bounded finding into an unbounded one, and it is the deletion that is hardest to see, because the remaining sentence reads perfectly well.

**`terms_used`.** The full closure of registered terms this claim depends on, including those reached through qualifiers and exceptions. **Why:** invalidation runs on it. Redefining a term has to reach every claim that used it, and a system that only follows the subject and object slots will miss the ones that used it in a qualifier.

**`surface_hints`.** Rendering preferences, including `must_not_omit`. **Why:** the IR does not choose words, but it does get to say which axes may not be dropped for length. A renderer that drops `spatial_scope` from a claim whose hints forbid it has produced a different claim, and that is a refusal rather than a style disagreement.

---

## 4. The Quantity type

**Status: specified.** Canonicalization of a quantity, and the digest over it, are executable through `wi canon`.

```json
{
  "role": "magnitude",
  "value": "38",
  "scale": 0,
  "unit": "percent",
  "unit_system": "ratio",
  "basis": "relative_to_baseline",
  "baseline_ref": "meaning.metric:m-0007@2021",
  "precision": {"kind": "significant_figures", "figures": 2},
  "uncertainty": {"kind": "interval", "low": "34", "high": "42", "scale": 0}
}
```

The numeric value is a **decimal**: a string of digits in `value` and an integer `scale` giving the number of digits after the point. `"value": "38", "scale": 0` is 38. `"value": "3814", "scale": 2` is 38.14. `"value": "240", "scale": -4` is 2,400,000.

```python
from decimal import Decimal, getcontext

def to_decimal(q: dict) -> Decimal:
    """Reconstruct the exact authored number. No float appears anywhere."""
    return Decimal(q["value"]).scaleb(-q["scale"])

def canonical_quantity(q: dict) -> dict:
    """Normalize for hashing: strip trailing zeros without changing the value,
    so 38.10 and 38.1 canonicalize identically and hash the same."""
    d = to_decimal(q)
    normalized = d.normalize()
    sign, digits, exponent = normalized.as_tuple()
    out = dict(q)
    out["value"] = ("-" if sign else "") + "".join(str(x) for x in digits)
    out["scale"] = -exponent
    return out
```

`role` is one of `magnitude`, `baseline`, `margin_of_error`, `sample_size`, `denominator`, `threshold`. `basis` distinguishes an absolute quantity from one that is relative to a stated baseline; a relative quantity without `baseline_ref` is rejected by the constraint engine, because a percentage with no denominator is not a measurement.

**Why `precision` is separate from `scale`.** `scale` says how the number is written; `precision` says how much of it was measured. A figure recorded as `38.00` with two significant figures is not a claim about hundredths, and a downstream calculation that treats it as one manufactures four digits of confidence nobody had.

---

## 5. Why binary floating point is banned

**Status: specified.**

For any quantity that participates in identity, comparison, arithmetic or a proof obligation, IEEE 754 binary floating point is forbidden. Not discouraged. The IR has no field capable of holding one, and a canonicalizer handed one refuses rather than converting.

The reason is not fastidiousness about the last bit. It is three separate failures, each of which produces a wrong answer that looks right.

**Identity breaks.** The state digest is a hash over the canonical serialization. `0.1 + 0.2` is `0.30000000000000004` in binary floating point. Two workspaces that arrive at the same authored number by different arithmetic paths produce different digests, so a verification bound to one does not attach to the other. The claim is identical, the hashes are not, and the system reports a change that did not happen — which is the fastest way to teach a reviewer that the change report is noise.

**Comparison breaks in the direction that hides errors.** Equality on floats is unusable, so somebody introduces a tolerance. A tolerance is a number chosen without evidence, and it silently absorbs real changes on the near side of it. A figure that moved from 4.10% to 4.1000001% is noise; a figure that moved from 4.10% to 4.11% is a correction somebody has to sign. A tolerance wide enough to suppress the first will eventually be widened to suppress a complaint about the second.

**Money and rates accumulate error that nobody attributes to the format.** Summing 12,000 line items in binary floating point and comparing the total to a figure computed elsewhere produces a discrepancy of a few cents. Nobody suspects the number format; they suspect the data, and they spend a day proving the data is fine.

```python
from decimal import Decimal

# What the IR forbids.
0.1 + 0.2 == 0.3            # False
sum([0.1] * 10) == 1.0      # False

# What the IR requires.
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")     # True
sum([Decimal("0.1")] * 10) == Decimal("1")            # True
```

**Where binary floating point remains permitted.** Layout geometry, rendering coordinates, a progress percentage in a terminal, an internal ranking score used only to order a list for a human to read. The test is the design rule from section 1: if the value participates in identity, comparison, proof obligation, invalidation, policy or a temporal query, it is a decimal. If it exists only to arrange pixels, it does not matter.

**Why this is load-bearing.** A number in a governed work is the thing a reader will act on and the thing a funder will check. Every other guarantee in this system — the digest, the verification binding, the semantic diff, the obligation engine — is a claim about exact equality of stated values. A representation that cannot express exact equality of decimal fractions is a representation that makes all four of those guarantees approximate, and an approximate guarantee about a funding figure is not a guarantee.

---

## 6. The first-class node types

**Status: specified.**

Eighteen types. Each earns its place by naming something the system must do that would be impossible if the type were collapsed into its nearest neighbour.

| Node type | What it holds | What having it as its own type buys |
|---|---|---|
| `meaning.claim_atom` | A single assertion about the world | The unit of verification. Everything else in the table exists because it is not one of these. |
| `meaning.definition` | What a term means in this work | A definition change invalidates every claim whose `terms_used` includes it. Filed as a claim, a redefinition would need its own evidence and would invalidate nothing. |
| `meaning.term` | A registered referent | Identity for subjects and objects, so "the program" and "Program X" compare equal and two different programs never do. See [`../v5/CONCEPT_REGISTRY.md`](../v5/CONCEPT_REGISTRY.md). |
| `meaning.premise` | Something taken as given for an argument | Premises are inherited by conclusions. A conclusion whose premise was withdrawn is stale even though nothing in its own text changed. |
| `meaning.inference` | A step from premises to a conclusion | The step itself becomes checkable. A valid step from a withdrawn premise and an invalid step from sound premises are different failures with different repairs. |
| `meaning.constraint` | A rule the graph must satisfy | Machine-enforceable invariants, run by `wi constraints`. A constraint stated as a claim is a sentence nobody executes. |
| `meaning.promise` | A commitment the workspace makes | Promises have a party, a deadline and a satisfaction condition. A promise filed as a claim has none of the three and cannot be reported as outstanding. |
| `meaning.obligation` | A duty imposed by policy, law or contract | Obligations are derived rather than authored, and `wi obligations` derives them. Their satisfaction is a release gate; a claim's is not. |
| `meaning.recommendation` | Advice to a reader | A recommendation is not true or false, so applying an evidence standard to it produces an obligation nobody can discharge. It needs a basis and a scope of applicability instead. |
| `meaning.hypothesis` | A proposition under test | Explicitly not asserted. Renders with its status attached, and an unresolved hypothesis rendered as a finding is a policy violation the engine can name. |
| `meaning.forecast` | A statement about the future | Carries a horizon and a method, and cannot be verified against a source that predates its horizon. Filed as a claim, it would attract an evidence obligation that no source can satisfy. |
| `meaning.metric` | A defined measurement | The thing a quantity is a quantity *of*. Changing a metric's definition invalidates every number reported against it, which is invisible if the metric lives only inside claim text. |
| `meaning.target` | A metric plus a threshold and a date | Progress against a target is derivable. Two claims — one about the metric, one about the goal — cannot be compared without restating the relationship every time. |
| `meaning.assumption` | Something relied on but not established | Assumptions are surfaced in the proof closure. An unstated assumption is the most common cause of a claim that is locally supported and globally wrong. |
| `meaning.exception` | A carve-out from a claim or rule | Attaches to what it modifies. Deleting an exception is a scope widening, which the semantic diff reports as a change of consequence rather than as removed text. |
| `meaning.question` | Something the work has not resolved | Open questions are first-class so a release can be blocked on them. As a comment in prose, a question is lost at the first compression pass. |
| `meaning.argument` | A structured case for a position | Groups premises, inferences and a conclusion into a unit that can be evaluated as a whole. See [`ARGUMENT_GRAPH.md`](ARGUMENT_GRAPH.md). |
| `meaning.counterargument` | A structured case against | Preserved rather than resolved, which is what Law Q requires. Filed as a rejected claim, the objection disappears the moment somebody disagrees with it. |

**Why eighteen and not four.** Every type here answers a question the system asks. Collapse `meaning.forecast` into `meaning.claim_atom` and the obligation engine demands a source for a statement about 2030. Collapse `meaning.recommendation` and the release gate blocks on evidence for advice. Collapse `meaning.exception` and the semantic diff reports a scope widening as a deletion of eleven words. The count is not a taxonomy for its own sake — remove any row and name the mechanism that stops working.

---

## 7. Independent axes: a worked contrast

**Status: specified.** The comparison below is a semantic diff over two IR states; `wi canon` computes the digests either side of it.

Two sentences. A copy editor would call the second a tightening of the first.

> **A.** Program X may reduce wait time by 38% in seven counties during 2022.
>
> **B.** Program X reduces wait time by 38% nationally.

The number is unchanged. Everything that makes the first defensible is gone.

| Axis | A | B | Independent of the others? | Consequence of the change |
|---|---|---|---|---|
| `modality` | `possibility` | `assertion` | Yes | Legal force changes. A hedged finding became a claim of fact. |
| `causality.kind` | `contributory` | `contributory` | Yes | Unchanged — but now carried by an assertion rather than a possibility, which raises the identification standard. |
| `spatial_scope` | 7 enumerated counties | `unbounded` | Yes | The population the claim covers grew by roughly four orders of magnitude. |
| `temporal_scope` | `[2022-01-01, 2023-01-01)` | absent | Yes | A bounded finding became a standing property. |
| `quantities[magnitude]` | 38, relative to 2021 baseline | 38, no baseline | Partly — the value is unchanged, the basis is not | A percentage with no denominator is not a measurement. |
| `certainty` | `hedged: may` | `none` | Yes | The hedge is not a synonym for the modality; both moved and each carries its own obligation. |
| `exceptions` | one carve-out | none | Yes | Two counties that changed intake policy are now inside a claim that excluded them. |
| `polarity` | `affirmative` | `affirmative` | Yes | Unchanged. |
| `population_scope` | enrolled, excluding waitlisted | absent | Yes | The denominator changed, so 38% is now a different quantity wearing the same number. |

**Nine axes, seven moved, one number.** That is the argument for storing them separately. A representation that folded modality into certainty would report one change where two occurred. One that folded spatial and population scope into a single `scope` would be unable to say that the geography widened while the population definition simply vanished — different failures, different repairs, different people to ask.

The obligation engine's response to B is not a diff. It is a list:

```
$ wi obligations --claim meaning.claim_atom:0193a7c2-0f31-7a44-b6d2-1e5c9a0f7b23

WI_OBLIGATION_UNMET   causal_identification
  modality is 'assertion' and causality.kind is 'contributory' with
  identification 'observational'. Policy release/funding.yaml requires
  identification in {experimental, quasi_experimental} for an asserted
  causal claim. Repair: restore modality 'possibility', or attach an
  identification strategy that meets the standard.

WI_OBLIGATION_UNMET   quantity_basis
  quantities[0].basis is 'relative_to_baseline' with no baseline_ref.
  Repair: name the baseline, or restate the quantity as absolute.

WI_OBLIGATION_UNMET   scope_support
  spatial_scope is 'unbounded'. Supporting anchor a-0114 covers 7 counties.
  Repair: narrow the scope to the supported set, or attach evidence at the
  asserted scope.

3 obligations, 0 discharged. Release blocked.
```

Three refusals, each naming the axis, the policy and a repair. None of them is "this sentence changed." That is the difference between a diff and a semantic diff, and it is why the axes are stored apart. The full comparison algebra is in [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md); the derivation of the obligations above is in [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md).

---

## 8. What the IR deliberately does not hold

**Status: specified.**

| Not stored | Why not |
|---|---|
| The rendered sentence as the authority | It is a build artifact. `surface_hints` influences it; nothing in the IR is derived from it. |
| A single confidence score | Reliability type, certainty, causal identification and evidence strength are four separate facts. Averaging them destroys every one. |
| Sentiment, tone, register | None of the nine uses. They belong to the renderer profile. |
| Discourse structure | Document order is a rendering decision, held in the structure graph rather than in what is asserted. |
| Model output as fact | A judgment provider may propose an IR node. It cannot author one. See [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md). |
| Free-text notes that alter meaning | A note that changes what is asserted is a qualifier and must be typed as one. Anything else is commentary and lives outside the node. |

---

## 9. Canonicalization and identity

**Status: executable in `scripts/wi.py`.**

`wi canon` produces the canonical JSON form of an IR node and the domain-separated state digest over it. The ten canonicalization rules, the JCS serialization and the preimage format are unchanged from v5 and are specified in [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md).

```
$ wi canon meaning/claim_atom/0193a7c2-0f31-7a44-b6d2-1e5c9a0f7b23.json

schema        wi.meaning/6.0.0
normalization nfc+jcs
content       sha256:1f7a0c93be48d25607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205
state         sha256:8c41f0b9d27e5a3608b1c94f7e2d06a35fc51b8047e9c2d0f3a6b9c1d4e7f205
quantities    1 normalized (38 percent, scale 0, relative_to_baseline)
terms         3 resolved, 0 unregistered
```

Two properties matter and both are consequences of the design rule.

**A node with an unregistered term does not canonicalize.** `terms_used` must resolve. A claim that depends on a term the workspace has not defined has an undeclared dependency, and an undeclared dependency cannot be invalidated when the thing it depends on changes.

**A node with a binary float does not canonicalize.** The canonicalizer refuses rather than converting. Converting would produce a digest that is stable and wrong: stable because the conversion is deterministic, wrong because the value it committed to is not the value anybody authored.

---

## Related documents

- [`../v5/SEMANTIC_IR.md`](../v5/SEMANTIC_IR.md) — the layer beneath this one, in force unamended
- [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) — dual identity, node families, proof closure
- [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md) — the ten rules and domain separation
- [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) — the comparison algebra over these fields
- [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) — why the four types are never collapsed
- [`BITEMPORAL_STATE.md`](BITEMPORAL_STATE.md) — the two time axes in the envelope
- [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md) — what `authorized_by` points at
- [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) — how obligations are derived from these fields
- [`ARGUMENT_GRAPH.md`](ARGUMENT_GRAPH.md) — premises, inferences, arguments and counterarguments
- [`CONSTITUTION.md`](CONSTITUTION.md) — the laws these structures serve

---

*The IR is not a description of a sentence. It is the state the sentence was compiled from, and it is the only thing the system agrees to be held to.*

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
