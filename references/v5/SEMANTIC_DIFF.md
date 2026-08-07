# The Semantic Diff Engine

v4 required every proposal to state its `EFFECT` — *what this changes about meaning, claims, or voice, or "wording only."* That field was the one authors actually read, and it was written by hand, in prose, by whoever wrote the proposal. v5 turns `EFFECT` into an engine.

**Status: deterministic layer executable (`wi diff --semantic`); judged remainder specified.**

A character diff is a report about typography. A semantic diff answers the question an author, a reviewer, a compliance officer and a court all ask in the same words: **did the meaning move, and in which direction?** Read this with [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — the dimensions compared here are the dimensions defined there — and with [`../v4/PROPOSAL_PROTOCOL.md`](../v4/PROPOSAL_PROTOCOL.md), which this document makes mechanical.

---

## 1. The delta taxonomy

**Status: executable in `scripts/wi.py` for the deterministic classes; the remainder specified.**

Every consequential transformation is classified into one or more delta classes. A single edit may carry several — tightening a sentence often produces `compression` and `certainty_strengthened` together, and the second is the one that matters.

| Class | Definition | Before → After |
|---|---|---|
| `wording_only` | Expression changes; no semantic dimension moves | "Between 2019 and 2022, the program served 11,800 households." → "The program served 11,800 households between 2019 and 2022." |
| `compression` | Fewer words, identical asserted content, no dimension dropped | "over the course of the 2019 to 2022 period" → "from 2019 to 2022" |
| `expansion` | More words, identical asserted content, no dimension added | "seven counties" → "the seven counties of the declared service area" |
| `scope_narrowed` | The claim now covers less than it did | "households across the state" → "households in seven counties" |
| `scope_broadened` | The claim now covers more than it did | "in seven counties" → "statewide" |
| `quantity_changed` | A number, magnitude, count or proportion moves | "11,800 households" → "12,400 households" |
| `unit_changed` | What the quantity counts or measures changes | "11,800 households" → "11,800 individuals" |
| `date_changed` | A specific point in time moves | "filings in March 2021" → "filings in March 2022" |
| `temporal_scope_changed` | The type or bounds of a period change | "since 2019" → "from 2019 to 2022" |
| `entity_changed` | A named person, organization or place is substituted | "the Barnes Foundation" → "the Barnes Family Trust" |
| `attribution_changed` | Who says, finds, funds or is responsible for it changes | "According to the county auditor, filings rose." → "Filings rose." |
| `certainty_strengthened` | Hedging removed or modality hardened | "may reduce" → "reduces" |
| `certainty_weakened` | Hedging added or modality softened | "reduces" → "may reduce" |
| `causality_added` | A causal relation is asserted where none was | "wait times fell after intake opened" → "opening intake cut wait times" |
| `causality_removed` | An asserted causal relation is downgraded or dropped | "the program cut wait times" → "wait times fell during the program" |
| `recommendation_changed` | The advised action, or its strength, changes | "consider a quarterly review" → "adopt a quarterly review" |
| `obligation_added` | A duty is created or made binding on some party | "Partners share intake data." → "Partners shall share intake data monthly." |
| `obligation_removed` | A duty is dropped or made optional | "The applicant must retain records for seven years." → "The applicant retains records." |
| `definition_changed` | A registered term's binding changes | `household: persons sharing a dwelling and a budget` → `household: persons sharing a dwelling` |
| `terminology_changed` | The term used for a registered concept changes | "service area" → "catchment" |
| `canon_changed` | A canonical fact inside a constructed world moves | "Maria found the ledger in 1987." → "Maria found the ledger in 1991." |
| `evidence_binding_changed` | The anchor backing the claim is replaced | a-0114 `needs_assessment.txt@v3` bytes 9,004–9,050 → a-0140 `partner_report.txt@v1` bytes 2,204–2,251 |
| `citation_binding_changed` | A citation-shaped reference now resolves to a different source | "(County Auditor, 2022)" → "(Whitfield & Barnes, 2021)" |
| `voice_only` | Register, diction or rhythm changes; the registered sense is unchanged | "The program provided services to 11,800 households." → "The program served 11,800 households." |
| `structure_only` | Ordering or nesting of renderings changes; no meaning node moves | §3 Methods before §4 Budget → §4 Budget before §3 Methods |

### 1.1 The presentation tier

Three classes sit **below** the taxonomy above. They are named separately because they are the only classes eligible for automatic acceptance, and a class that can be auto-accepted must be defined narrowly enough that the definition is itself the safety mechanism.

| Class | Definition |
|---|---|
| `format_only` | Heading level, list marker, emphasis, table alignment. No token sequence inside a sentence changes. |
| `whitespace_only` | Spacing, indentation, line wrapping, trailing newlines. Byte-different, token-identical. |
| `punctuation_only` | Punctuation that does not fall inside a quoted span and does not alter enumeration, negation or scope. |

**Why the tier is separate.** `wording_only` sounds like it belongs here and does not. Deciding that two different sentences say the same thing is a judgment; deciding that two byte sequences tokenize identically is a comparison. The auto-accept list in section 6 contains only classes a machine can *prove*, plus `wording_only` under an explicit user grant in ordinary mode — and never in strict or regulated mode.

---

## 2. Deterministic first, judged only for the remainder

**Status: executable in `scripts/wi.py`.**

Ten semantic dimensions are decidable by structural comparison of two claim-atom states. No model. No network. No judgment. They cover the classes where documents actually go wrong.

| Dimension compared | Classes it decides | How |
|---|---|---|
| `quantity`, `quantity_kind` | `quantity_changed` | Numeric equality on the structured field, not the surface string |
| `unit`, `currency` | `unit_changed` | Registered unit identity; currency includes basis year |
| Date points | `date_changed` | Canonicalized ISO comparison |
| `temporal_scope` | `temporal_scope_changed` | Range type, start, end and granularity compared as a tuple |
| `modality`, `certainty` | `certainty_strengthened` · `certainty_weakened` · `obligation_added` · `obligation_removed` | Ordered modal lattice: `may` < `should` < `will` < `is` < `must` |
| `attribution` | `attribution_changed` | Attribution record identity, including `on_behalf_of` |
| `subject`, `object` entity refs | `entity_changed` | Registered entity identity, not string similarity |
| `negation` | Inverts the sign of every other class | Boolean field comparison |
| `uses_term` bindings | `terminology_changed` · `definition_changed` | Term id and `definition_state` digest comparison |
| Citation and anchor bindings | `citation_binding_changed` · `evidence_binding_changed` | Anchor id and `source_state_digest` comparison |

The remaining classes need the judgment tier, because deciding them requires reading:

| Class | Why structure cannot decide it |
|---|---|
| `wording_only` · `compression` · `expansion` · `voice_only` | All three describe *sameness of meaning under different words*. Distinguishing them from each other, and all of them from a quiet semantic move, is paraphrase assessment. |
| `scope_narrowed` · `scope_broadened` | Decidable when scope is a registered constraint node. Not decidable when the narrowing lives in an unregistered adjective — "eligible households," "active partners." |
| `causality_added` · `causality_removed` | The `causal_force` field is decidable when populated. Inferring it from a new verb is not. |
| `recommendation_changed` | The strength ordering of advice is domain-specific and unregistered by default. |
| `canon_changed` | Decidable against a `canon.*` registry entry. Not decidable for an unregistered world fact. |

**The principle: prefer deterministic detection and escalate only what cannot be resolved structurally.**

**Why this is load-bearing.** A judged classification costs money, latency, a network round trip and a provider dependency, and it produces a `judged` record that a reader is entitled to disagree with. A deterministic classification costs microseconds and produces a `verified` record a stranger can reproduce. Every class moved from the second tier to the first is a permanent reduction in what the system has to ask anyone to trust. It also fails safe in the right direction: under Law E, an escalated comparison that no provider is available to resolve becomes `needs_review`, never `wording_only`.

---

## 3. The comparison function

**Status: executable in `scripts/wi.py` for the deterministic branch; the `escalate` branch is specified.**

```python
def compare_claim_states(a, b):
    """Classify the delta between two claim-atom states.

    a, b are canonical claim-atom payloads (SEMANTIC_IR.md §2).
    Returns three lists. Never a score, never a single label.
    """
    deterministic, judged, invalidations = [], [], []

    # --- Tier 1: structural comparison over registered dimensions -----------
    for dim, cls in DECIDABLE_DIMENSIONS:          # the ten rows of §2
        if a.get(dim) != b.get(dim):
            deterministic.append(delta(cls, dim, a.get(dim), b.get(dim)))

    # Modality is ordered, so direction is decidable, not merely difference.
    if a["modality"] != b["modality"]:
        step = MODAL_LATTICE.index(b["modality"]) - MODAL_LATTICE.index(a["modality"])
        deterministic.append(
            delta("certainty_strengthened" if step > 0 else "certainty_weakened",
                  "modality", a["modality"], b["modality"]))

    # Negation flips the meaning of every other delta in this set.
    if a["negation"] != b["negation"]:
        deterministic.append(delta("negation_flipped", "negation", a, b))

    # --- Tier 2: escalate only what tier 1 could not settle -----------------
    if a["surface"] != b["surface"] and not deterministic:
        # Same structured content, different words. The only case in which
        # wording_only is even a candidate — and it is still not free.
        judged.append(escalate("paraphrase_equivalence", a["surface"], b["surface"]))

    for dim in UNREGISTERED_SCOPE_FIELDS:          # adjectival scope, causal verbs
        if a.get(dim) != b.get(dim):
            judged.append(escalate("scope_direction", a.get(dim), b.get(dim)))

    # --- Proof consequences: per-edge policy, STALENESS.md §3 ---------------
    for d in deterministic + judged:
        for proof in proofs_bound_to(a["state_id"]):
            if voids(d, proof):
                invalidations.append({"proof_id": proof.id, "reason": d.cls,
                                      "policy": proof.edge_policy})

    # Law E: an escalation nobody can resolve does not become wording_only.
    if judged and not judgment_provider_available():
        for j in judged:
            j.result = "needs_review"

    return {"deterministic": deterministic, "judged": judged,
            "proof_invalidations": invalidations}
```

Three properties of this function are non-negotiable. It never returns a single label, because a real edit is usually several deltas at once and the dangerous one is rarely the largest. It never returns a score. And an empty `deterministic` list is a precondition for even *considering* `wording_only` — a structural difference in any registered dimension removes that classification from the table before a provider is consulted.

---

## 4. The canonical examples

**Status: executable in `scripts/wi.py`. These seven are gold cases in the benchmark suite of section 10.**

| Edit | Class | Proof consequence |
|---|---|---|
| `may reduce → reduces` | `certainty_strengthened` | Hard. Every anchor supporting the hedged form is void — a source that says "may reduce" does not support "reduces." The claim drops to `needs_source` until an anchor asserting the unhedged form exists. |
| `up to 38% → 38%` | `certainty_strengthened` + `quantity_changed` | Hard. "Up to 38%" is a bound; "38%" is a value. The numeric check re-runs against the anchored figure and fails unless the source states the point value. |
| `since 2019 → from 2019 to 2022` | `temporal_scope_changed` | Hard on the date check; the range type moved from open to closed. Often a *repair* rather than a break — the closed form frequently matches a source the open form did not. |
| `recommended → required` | `obligation_added` + `legal_force` change | Hard. Every rendering carrying the claim enters `review`. Never auto-accepts in any mode. In regulated mode this is a `require_human` class by policy. |
| `most → all` | `scope_broadened` | Hard, on the `broadens` edge. A universal quantifier is refuted by one counterexample; the evidence that supported "most" almost never supports "all." |
| `contributes to → causes` | `causality_added` | Hard. `causal_force` moves `contribution` → `causation`. This is the single most common misreporting failure in sourced writing and the least visible in a line diff. |
| `11,800 → 12,400` | `quantity_changed` | Hard and immediate. The numeric check fails against the bound anchor before any judgment runs; no provider is consulted, because none is needed. |

Six of the seven are detected without a model. That ratio is the argument for the deterministic-first design, and it is not an accident — those six are the classes that arise from *editing*, which is where consequential documents break.

---

## 5. Proof impact

**Status: executable in `scripts/wi.py`.**

Every proposal carries a proof-impact object. It is produced by the engine, not written by whoever wrote the proposal.

```json
{
  "proposal_id": "pr-0311",
  "target_state": "sha256:9f2c1d47ab3e58b0c6d19e4f7a2b8c35de60f19a4c7b2e8d0f3a6b9c1d4e7f20",
  "semantic_delta": [
    {
      "class": "certainty_strengthened",
      "dimension": "modality",
      "before": "may",
      "after": "is",
      "basis": "verified",
      "detected_by": "deterministic"
    },
    {
      "class": "compression",
      "dimension": "surface",
      "basis": "judged",
      "detected_by": "escalated",
      "result": "needs_review",
      "note": "no judgment provider configured on this surface"
    }
  ],
  "proof_impact": {
    "invalidates": [
      {"proof_id": "vr-0442", "claim": "c-0004", "anchor": "a-0141", "policy": "hard"}
    ],
    "requires_recheck": [
      {"node": "p-0031", "kind": "structure.paragraph", "policy": "review"},
      {"node": "slide-07", "kind": "media.slide", "policy": "review"},
      {"node": "script-podcast-ep12", "kind": "structure.section", "policy": "review"}
    ],
    "unaffected": {
      "claim_atoms": 1806, "anchors": 1794, "release_artifacts": 4,
      "basis": "no dependency path from the target state to these nodes"
    }
  }
}
```

### 5.1 Naming what is unaffected is as important as naming what breaks

The `unaffected` block is not reassurance; it is the field that keeps the system usable. A dependency engine that reports only damage teaches its user one lesson very quickly: every edit produces a wall of red, the wall is mostly irrelevant, and reading it is a waste of time. The rational response is to stop reading it, and the first thing lost is the finding that mattered. A system that reverifies everything has the same effect as a system that verifies nothing, arrived at from the opposite direction. So `unaffected` carries a **basis**, not just a count. "1,806 claim atoms unaffected" is a measured statement with a stated denominator and a stated reason: no dependency path exists from the changed state to those nodes. A reader can ask how it was computed and get the traversal. That is what separates it from a comfortable number. The same discipline governs [`STALENESS.md`](STALENESS.md), where the unaffected count is printed in every impact report.

---

## 6. Auto-accept policy

**Status: executable in `scripts/wi.py`.**

Auto-acceptance is a delegation of authorship. It is legitimate — nobody should approve a trailing newline by hand — and it is bounded by class, never by confidence. **In ordinary mode, a user may grant automatic acceptance of:**

| Class | Condition |
|---|---|
| `wording_only` | Only when `deterministic` is empty and a judgment resolved the paraphrase; never on an unresolved escalation |
| `format_only` | Always eligible |
| `whitespace_only` | Always eligible |
| `punctuation_only` | Only where the change does not fall inside a quoted span and does not alter enumeration, negation or scope |

The grant is explicit, recorded, and attributed to an `automated_policy` actor — not to the human who set it. The record says the system did it under a rule, because that is what happened.

**In strict or regulated mode, four rules hold absolutely:**

1. **No claim-changing proposal auto-accepts.** Any delta outside the presentation tier requires a human decision, regardless of how small the text change is.
2. **No citation-binding change auto-accepts.** `citation_binding_changed` and `evidence_binding_changed` are decisions about what supports a claim, and a machine may not make them silently.
3. **No waiver is generated automatically.** A waiver is a person choosing to proceed past a hold. There is no rule that can be that person.
4. **No human-attested observation is rewritten into an external fact.** A `human-declared` claim whose realm is `author_observation` may not have its realm changed by any automated process. The author said they saw it; the system does not get to promote that into a claim about the world that then needs a source it was never going to have.

**Why these four.** Each names a place where a small textual edit produces a large accountability change. A punctuation fix inside a quotation is a misquotation. A swapped citation is a different evidentiary claim in the same sentence. An auto-generated waiver is a hold that cleared itself. And an observation silently reclassified as external fact converts the author's own testimony into an unsupported assertion about the world — the exact inversion of Law D's purpose.

---

## 7. The proposal and decision state machine

**Status: specified.**

```
                          ┌──────────────┐
                          │   proposed   │
                          └──────┬───────┘
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
        ┌───────────┐      ┌───────────┐      ┌───────────┐
        │ accepted  │      │ rejected  │      │   stale   │
        └─────┬─────┘      └─────┬─────┘      └─────┬─────┘
              │                  │                  │
              ▼                  ▼                  ▼
        ┌───────────┐     audit history      ┌─────────────┐
        │  applied  │       (terminal —      │ superseded  │
        └─────┬─────┘        never applies)  └─────────────┘
              │
              ▼
        ┌─────────────┐
        │ reverified  │  ← proof runs here, against the RESULTING state
        └─────┬───────┘
              │
              ▼
        ┌───────────┐
        │ released  │
        └───────────┘
```

**The eight binding rules:**

1. **A proposal binds to an exact target state digest.** Not to a file, not to a line number, not to a paragraph identity — to the digest of the state it was derived from.
2. **If the target state changes, the proposal is stale.** No fuzzy re-application. A changed target usually means the author already fixed it themselves, and overwriting their fix with a stale machine suggestion is the failure Law A exists to prevent.
3. **An accepted proposal produces a new state.** It does not mutate the old one. The prior state remains addressable and quotable forever.
4. **Acceptance does not imply proof.** This is the rule the whole diagram exists to make visible. A human agreeing that a sentence should read differently is a statement about the sentence, not about the evidence behind it.
5. **Proof must run against the resulting state.** The `reverified` node is not optional and cannot be skipped by an accepting actor. A proof bound to the pre-acceptance digest is, by construction, not a proof of what now exists.
6. **A waiver binds to an exact claim state.** Same rule as a proposal, for the same reason.
7. **If the claim changes, the waiver is stale.** You cannot waive a claim and then rewrite it under the waiver. v4 stated this; v5 makes it a digest comparison.
8. **Rejected proposals remain audit history and never apply.** A rejection is a decision worth keeping — it is evidence of review, and it is the record that answers *did anyone look at this?*

**Why rule 4 is the one that matters.** The most common way a governed document becomes an ungoverned document is an accepted proposal whose green badge was inherited from the state before the change. Acceptance and proof are different events, produced by different actors, binding to different digests. Collapsing them produces a document where every sentence appears approved *and* verified, and where nobody can say which sentences were which.

---

## 8. The decision record and delegated policy

**Status: specified.**

A decision is an artifact under Law J, not a line in a chat log.

```json
{
  "decision_id": "d-0021",
  "proposal_state": "sha256:c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f81a4b7c02de95f38a6b0c2d4e7f19a3b5",
  "target_state":   "sha256:9f2c1d47ab3e58b0c6d19e4f7a2b8c35de60f19a4c7b2e8d0f3a6b9c1d4e7f20",
  "actor": {
    "type": "team_member",
    "id": "a.rivera@example.org",
    "display_name": "A. Rivera"
  },
  "decision": "accepted_with_modification",
  "reason": "Kept the tightened rhythm and restored the hedge; the source says 'may'.",
  "created_at": "2026-03-11T16:04:52Z"
}
```

`proposal_state` and `target_state` are both present and both required. A decision that names the proposal but not the state it applied to is a signature on a blank page: the text can move underneath it and the approval still appears to cover it. Delegated authority is configuration, and it is written in the same vocabulary the engine classifies with:

```yaml
# .wi/policy/delegation.yaml
delegation:
  actor: automated_policy
  mode: standard
  allow:
    - punctuation_only
    - whitespace_only
    - heading_format_only
  require_human:
    - meaning_change        # any delta outside the presentation tier
    - evidence_change       # evidence_binding_changed, citation_binding_changed
    - legal_force_change    # obligation_*, recommendation_changed
    - canon_change          # canon_changed
    - waiver                # never delegable, in any mode
  on_unresolved_escalation: require_human
  record_as: automated_policy      # never as the human who configured it
```

The `allow` list is a whitelist and behaves like one: a class absent from it requires a human, including classes invented after the file was written. A delegation policy that fails open is not a policy.

---

## 9. The Meaning Diff a human reads

**Status: executable in `scripts/wi.py`.**

The JSON above is what the graph stores. This is what a surface prints. Same object, rendered for the person who has to decide.

```
MEANING DIFF  ·  pr-0311  ·  c-0004  ·  paragraph p-0031

  before   The program may reduce median wait times.
  after    The program reduces median wait times.

  semantic effect   certainty_strengthened          [verified · deterministic]
                    modality   may → is
                    certainty  estimated → asserted
                    A hedge was removed. The sentence now asserts as fact what
                    the previous sentence offered as a possibility.

  proof effect      invalidates       1 proof
                                        anchor a-0141 supports the hedged form.
                                        needs_assessment.txt@v3, bytes 4,180-4,236:
                                        > "the intervention may reduce median wait
                                        >  times where intake capacity permits"
                    requires_recheck  3 renderings
                                        p-0031 (narrative) · slide-07 · script-ep12
                    unaffected        1,806 claim atoms · 4 release artifacts
                                        (no dependency path from this state)

  required action   This proposal changes what the sentence asserts. It does not
                    auto-accept in any mode. Accepting it leaves c-0004 at
                    needs_source until an anchor supporting the unhedged form
                    exists; the gate moves to HOLD under `strict`.

  your choices      (a) accept   record the strengthened claim as a new state,
                                 drop c-0004 to needs_source, gate → HOLD
                    (b) reject   keep the hedge; the proposal stays in history
                    (c) qualify  keep the tightened rhythm and the hedge:
                                 "The program reduces median wait times where
                                  intake capacity permits."   → wording_only

Checks run: modality · certainty · quantity · temporal scope · anchor integrity.
Not run: paraphrase equivalence (needs a judgment tier, not this script).
```

Option (c) is the reason this format exists. A diff that offers accept-or-reject frames a hedge removal as a binary between better prose and defensible prose. There is almost always a third sentence that is both, and the author is the only one who can write it — but they will not go looking for it if the interface never suggests one exists.

---

## 10. Benchmarks

**Status: specified.** The gold pairs are shipped; the scoring harness for the judged tier is defined here and unimplemented.

The engine is scored with **per-class confusion matrices, published individually.** There is no blended accuracy number, and there will not be one.

**Why not one number.** A blended score over twenty-eight classes is dominated by whichever classes appear most often, which are the presentation classes, which are the easy ones. A system that detects `whitespace_only` perfectly and `causality_added` at chance can post an excellent aggregate. The classes are not interchangeable and their costs are not comparable: a missed `wording_only` produces a needless review, and a missed `obligation_added` ships a document that binds someone to something nobody approved. Averaging those is the composite-score failure named in [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md), applied to the diff engine. Each class publishes:

```
class: certainty_strengthened
  gold pairs        140
  true positive     136      false negative      4
  false positive      2      true negative     998
  basis             verified · deterministic comparison over modality lattice
  benchmark set     tests/v5/diff/gold_pairs.jsonl @ sha256:44c1a0…
```

The gold pairs, by group:

| Group | Pairs of the form |
|---|---|
| Modality and obligation | `may reduce → reduces` · `should file → must file` · `recommended → required` · `may submit → shall submit` · `retains records → must retain records for seven years` |
| Quantity | `11,800 → 12,400` · `38% → 31%` · `seven counties → nine counties` · `$2.4M → $2.4M (2019 dollars)` |
| Bounded to point | `up to 38% → 38%` · `at least 400 → 400` · `nearly 12,000 → 12,000` |
| Temporal | `since 2019 → from 2019 to 2022` · `in 2021 → in 2022` · `by year end → by December 31` · `annually → quarterly` |
| Quantifier scope | `most → all` · `some → many` · `several counties → the region` · `eligible households → households` |
| Causality | `contributes to → causes` · `associated with → drives` · `followed → resulted from` |
| Attribution and negation | `according to the auditor, filings rose → filings rose` · `the report found → we found` · `no household waited → households waited` · `did not decline → declined` |
| Terminology and binding | `service area → catchment` · `household → family` · citation swap · anchor rebind to a different source version |
| True negatives | 1,000 pairs that must classify as presentation-tier or `wording_only`, drawn from real copyedits |

The true-negative set is the largest group on purpose. A diff engine that flags everything is trivially perfect on recall and useless in practice, and precision on ordinary copyediting is the property that determines whether anyone leaves it switched on.

---

## 11. What is executable and what is specified

| Mechanism | Status |
|---|---|
| The delta taxonomy and the presentation tier as a vocabulary | Executable in `scripts/wi.py` |
| Deterministic classification over the ten registered dimensions | Executable in `scripts/wi.py` |
| `wi diff --semantic`, the Meaning Diff rendering, the proof-impact object | Executable in `scripts/wi.py` |
| Auto-accept policy enforcement, including the four strict-mode rules | Executable in `scripts/wi.py` |
| Gold pairs and per-class confusion matrices for the deterministic classes | Executable in `scripts/wi.py` |
| Escalation of paraphrase equivalence and unregistered scope direction | Specified — see [`JUDGMENT_TIER.md`](JUDGMENT_TIER.md) |
| Proposal and decision state machine, decision records, delegated-policy enforcement | Specified |
| Scoring harness for judged classes | Specified |

---

## Related documents

- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — the dimensions this engine compares
- [`STALENESS.md`](STALENESS.md) — what the engine's output does to everything downstream
- [`JUDGMENT_TIER.md`](JUDGMENT_TIER.md) — the provider contract for the escalated remainder
- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — edge invalidation policies, proposals and decisions as nodes
- [`CONSTITUTION.md`](CONSTITUTION.md) — Law A, Law H and Law J
- [`../v4/PROPOSAL_PROTOCOL.md`](../v4/PROPOSAL_PROTOCOL.md) — the `EFFECT` field this engine mechanizes
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
