# Proof Obligations

Proof stops being a checker and becomes a planner. The system derives what must be proved *before* anything is checked, states it as a set, and then evaluates that set.

**Status: executable in `scripts/wi.py`.**

`wi obligations` runs today. It derives the obligation set for a scope from typed semantic state, the release target and the policy in force, and reports each obligation's status with its basis.

v5 verifies after the fact. `wi atomize` splits sentences into claim atoms, `wi anchor` binds them to evidence, `wi verify` runs the checks that apply, and `wi gate` issues a verdict. That order has a gap in it that is invisible while everything is working: **the set of checks that ran is whatever the implementation happened to attempt.** Nobody declared what *should* have run, so nobody can tell the difference between a claim that passed every applicable check and a claim for which the applicable check was never enumerated.

v6 inverts it. The obligation set is derived first, from state and policy, and it exists whether or not any check has been attempted. A check that has not run leaves an obligation `unmet`, which is a fact about the document rather than a silence in a report.

Read this with [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — Law C and Law D are the two this document mechanizes — and with [`../v5/POLICY_AS_CODE.md`](../v5/POLICY_AS_CODE.md), whose policy object supplies half the derivation.

---

## Table of contents

1. From checker to planner
2. `ProofObligation` and `ObligationStatus`
3. Where obligations come from
4. Three worked obligation sets
5. The `ProofPlanner` contract
6. The deterministic check catalogue
7. Authority as an obligation
8. Why a declared set beats a hidden checklist
9. The closed reliability basis
10. Benchmarks
11. What is executable and what is specified

---

## 1. From checker to planner

**Status: executable in `scripts/wi.py`.**

The distinction is one of direction.

| | Checker (v5) | Planner (v6) |
|---|---|---|
| Starts from | The checks the implementation knows how to run | The state, the target and the policy |
| Produces | Results for the checks it attempted | The full obligation set, then results against it |
| A missing check is | Absent from the report | An `unmet` obligation with a named reason |
| Coverage is | Whatever happened | A denominator |
| Adding a new check | Silently changes what "verified" covered | Adds an obligation, which every prior release reports as unmet |

**Why this is load-bearing.** Law C says never report work not done, and v5 delivered the honest version of that at the level of individual checks: `unavailable_on_surface`, `disabled_by_policy`, `invalidated_by_edit`. What it could not deliver is the level above — *was there a check that should have applied and was never considered?* A report listing eight passing checks over a claim is Law C-compliant about those eight and silent about the ninth, and the reader has no way to see through the structure to the absence behind it.

An obligation set closes that. It is derived from the claim's own typed dimensions, so a claim carrying a `currency` field with a basis year *has* a `numeric.dimension` obligation whether or not any code exists to satisfy it. The obligation is a property of the state. The check is a thing that may or may not have run against it.

The practical effect is that **coverage becomes a measurement with a denominator** rather than an impression. "31 of 34 obligations met, 3 unmet, of which 2 are unavailable on this surface and 1 has no implementation" is a fact under [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md). "All checks passed" is not, and never was.

---

## 2. `ProofObligation` and `ObligationStatus`

**Status: executable in `scripts/wi.py`.**

```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ProofObligation:
    """A statement that something must be shown before this scope may be released.

    Derived, never authored. An obligation nobody can point at a derivation
    rule for is a defect in the planner, not a policy an operator wrote.
    """
    obligation_id: str
    check: str                  # a catalogue identifier from §6
    subject: str                # logical id of the node the obligation is about
    subject_state: str          # state digest the obligation was derived against
    derived_from: List[str]     # rule ids: "rule.realm.external_fact.requires_anchor", ...
    required_basis: str         # a ReliabilityBasis member, §9
    severity: str               # "block" | "hold" | "advisory"
    status: "ObligationStatus"
    satisfied_by: Optional[str] = None    # verification.result id, when met
    unmet_reason: Optional[str] = None    # required whenever status is not "met"
    note: str = ""


class ObligationStatus:
    MET = "met"                       # a check ran against this exact state and passed
    UNMET = "unmet"                   # required, and nothing has satisfied it
    STALE = "stale"                   # satisfied against a state that has since moved
    WAIVED = "waived"                 # a named actor proceeded past it, bound to this state
    UNAVAILABLE = "unavailable"       # the surface cannot perform the check
    DISABLED = "disabled"             # policy switched the capability off
    NO_IMPLEMENTATION = "no_implementation"   # the check is specified and does not exist
    NOT_APPLICABLE = "not_applicable"         # derivation excluded it, with a reason
```

**Seven statuses, and none of them is `passed`.** `met` names a relationship between an obligation and a result bound to an exact state — not a quality of the claim. The wording matters because a reader who sees `passed` next to a sentence will read it as *this sentence is true*, and the system is not in a position to say that about anything.

**`unmet_reason` is required on every non-`met` status, including `not_applicable`.** An obligation excluded from a scope must say which derivation rule excluded it. This is the field that stops the planner from quietly narrowing: a rule that decides a `numeric.denominator` obligation does not apply to a proportion has to say so, in the record, where somebody can disagree with it.

**Four statuses distinguish four different absences, and collapsing any two of them is a Law C violation.**

| Status | Means | Repair |
|---|---|---|
| `unmet` | Should have been shown; nothing shows it | Do the work |
| `unavailable` | The surface has no PDF decoder, no filesystem, no binary reader | Run it somewhere else |
| `disabled` | The capability exists and this project turned it off | A policy decision, taken by somebody |
| `no_implementation` | This check is specified in §6 and does not exist in any surface | A roadmap item, and the release should say so |

`no_implementation` is the one a system under commercial pressure would like to omit. It is the honest statement that the catalogue names a check the tool cannot yet perform, and it appears in the release manifest so that a reader of a bundle can see which parts of the standard the tool itself did not meet. Its absence would mean the obligation set silently shrinks to what the implementation can do, which is exactly the failure the obligation set exists to remove.

---

## 3. Where obligations come from

**Status: executable in `scripts/wi.py`.**

Three inputs, combined by rules that are themselves addressable.

```
   typed semantic state          release target             policy in force
   ────────────────────          ──────────────             ───────────────
   realm                         audience                   evidence mode
   populated dimensions          distribution               required_basis floor
   node family                   legal exposure             block_on / hold_on sets
   bindings (anchor, term)       format constraints         waiver reachability
            │                          │                           │
            └──────────────┬───────────┴───────────────────────────┘
                           ▼
                    derivation rules
                           ▼
                    obligation set
```

**From state.** A `meaning.claim_atom` in realm `external_fact` with a populated `quantity` and `unit` derives `anchor.integrity`, `numeric.value`, `numeric.unit` and `numeric.dimension`. The same atom in realm `author_observation` derives none of them and instead derives an attribution obligation. The realm is not a label on a report; it is an input to which obligations exist.

**From the target.** The same claim rendered into an internal memo and into a regulatory filing carries different obligations, because the target declares its audience and exposure. A filing target adds `release.artifact-digest`, `decision.state-binding` on every accepted proposal in the closure, and `authority.grant-valid`.

**From policy.** The mode sets the severity, not the membership. An obligation exists in `standard` and in `regulated`; what changes is whether an unmet one is advisory, holds or blocks. That separation is deliberate — an operator lowering the mode should be lowering the consequence, not shrinking the set of things they are being told about.

```python
def derive(node, target, policy):
    """Enumerate obligations for one node. Every append names its rule."""
    out = []

    if node.family == "meaning.claim_atom":
        if node.realm == "external_fact":
            out.append(ob("anchor.integrity", node,
                          rule="rule.realm.external_fact.requires_anchor",
                          basis="verified"))
            if node.quotes_source:
                out.append(ob("quotation.verbatim", node,
                              rule="rule.quotation.requires_verbatim_match",
                              basis="verified"))
            if node.quantity is not None:
                out.append(ob("numeric.value", node,
                              rule="rule.quantity.requires_source_figure",
                              basis="verified"))
                out.append(ob("numeric.unit", node,
                              rule="rule.quantity.requires_unit_identity",
                              basis="verified"))
                if node.quantity_kind == "proportion":
                    out.append(ob("numeric.denominator", node,
                                  rule="rule.proportion.requires_denominator",
                                  basis="measured"))
            if node.currency is not None:
                out.append(ob("numeric.dimension", node,
                              rule="rule.currency.requires_basis_year",
                              basis="verified"))

        elif node.realm == "author_observation":
            out.append(ob("attribution.preservation", node,
                          rule="rule.realm.author_observation.requires_attributed_actor",
                          basis="human-declared"))
            out.append(ob("realm.preservation", node,
                          rule="rule.realm.no_silent_promotion",
                          basis="verified"))

        elif node.realm == "fictional_canon":
            out.append(ob("realm.preservation", node,
                          rule="rule.realm.canon_never_renders_as_external",
                          basis="verified"))

    if node.family == "meaning.obligation":
        out.append(ob("obligation.exception-preservation", node,
                      rule="rule.obligation.exceptions_survive_every_rendering",
                      basis="verified"))
        out.append(ob("modality.no-strengthening", node,
                      rule="rule.modality.no_strengthening_without_decision",
                      basis="verified"))

    for o in out:
        o.severity = policy.severity_for(o.check, target)
    return out
```

**Every obligation carries `derived_from`.** An obligation set that cannot explain itself is a checklist with better formatting. A reader who disagrees with an obligation can name the rule that produced it, and an operator who wants to change the standard changes the rule rather than arguing with an output.

---

## 4. Three worked obligation sets

**Status: executable in `scripts/wi.py`.**

### 4.1 A strict external factual claim

```
$ python3 scripts/wi.py obligations --node c-0002 --target filing

c-0002   "The program served 11,800 households between 2019 and 2022."
         realm external_fact · target filing · policy strict
         state sha256:9f2c1d47…7f20

  10 obligations · 8 met · 1 unmet · 1 no_implementation

  met                anchor.integrity          verified
                     a-0114 needs_assessment.txt@v3 bytes 9,004–9,050
                     rule.realm.external_fact.requires_anchor

  met                quotation.verbatim        verified
                     quote digest matches the anchored span byte-for-byte

  met                numeric.value             verified
                     11800 == 11800 at the anchored span

  met                numeric.unit              verified
                     households == households · registered unit identity

  met                date.range                verified
                     2019-01-01..2022-12-31 closed == source range

  met                scope.temporal            verified
                     claim range is contained by the anchored range

  met                modality.no-strengthening verified
                     modality `is` unchanged since the last decision d-0104

  met                realm.preservation        verified
                     external_fact; no canon anchor in the support set

  unmet              scope.population          verified required
                     The claim says "households". The source table's row
                     semantics say "households with at least one enrolled
                     participant". The narrower population is not stated in
                     the claim and is not carried by any constraint node.
                     reason: no meaning.constraint qualifies this atom
                     repair: qualify_claim · 1 human decision

  no_implementation  numeric.denominator       measured required
                     rule.proportion.requires_denominator does not apply
                     (quantity_kind is count, not proportion) — recorded as
                     not_applicable, not omitted.

  Gate under strict: HOLD (1 unmet, severity hold)
```

The unmet obligation is the finding. Nothing about the number is wrong; the *population* is narrower than the sentence says, and that is the classic overreach — a count over a filtered set presented as a count over the whole. It is caught because `scope.population` is derived from the source table's `row_semantics`, which [`../v5/SEMANTIC_IR.md`](../v5/SEMANTIC_IR.md) §7.2 requires a tabular source to carry.

### 4.2 An obligation node

```
$ python3 scripts/wi.py obligations --node ob-0022 --target filing

ob-0022  "The applicant shall retain records for seven years, except where
          superseding state law provides a shorter period."
         family meaning.obligation · target filing · policy strict

  9 obligations · 6 met · 2 unmet · 1 waived

  met      obligation.exception-preservation   verified
           The carve-out appears in all 4 renderings:
           ch-11 ¶2 · web/terms.html · deck slide-22 · filing §4
           A rendering that dropped it would be a different duty.

  met      modality.no-strengthening           verified
           `shall` unchanged since d-0141 · no proposal has moved it

  met      definition.binding                  verified
           "records" binds def-0011 · definition_state digest unchanged

  met      entity.presence                     verified
           "the applicant" resolves to the registered party entity

  met      scope.temporal                      verified
           seven-year period is a closed duration from a stated trigger

  met      realm.preservation                  verified

  unmet    citation.resolution                 verified required
           The exception cites "superseding state law" and resolves to no
           source in this workspace. An exception whose trigger cannot be
           located is an exception nobody can apply.
           reason: no source.artifact matches the citation
           repair: attach_source

  unmet    authority.grant-valid               verified required
           This target is a filing. Creating a binding retention duty in a
           filed document requires `binding_commitment` authority.
           held by: none of the actors on this workspace
           repair: request_authority

  waived   scope.spatial                       w-0011 · m.chen · 2026-02-02
           "superseding state law" does not name a jurisdiction set. Waived
           with reason: "Counsel confirmed the phrase is intentionally
           open; jurisdiction is determined at enforcement."
           bound state: sha256:c8d0e2f4…a3b5 — unchanged since the waiver

  Gate under strict: HOLD (2 unmet)
  Gate under regulated: BLOCK (authority.grant-valid is block_on)
```

An obligation node's obligations are about **what binds whom, and whether the carve-outs survive**. `obligation.exception-preservation` checks the exception's presence in every rendering, because an exception dropped from a slide is a stricter duty asserted to the same reader.

### 4.3 A forecast node

```
$ python3 scripts/wi.py obligations --node c-0620 --target board_deck

c-0620   "Placement volume will reach 4,200 by Q4 2027."
         realm simulation · target board_deck · policy strict

  7 obligations · 3 met · 4 unmet

  met      realm.preservation                  verified
           realm is `simulation`. Every rendering carries the model marker.
           A rendering that dropped it would present a projection as a fact.

  met      attribution.preservation            verified
           attributed to the 2026 capacity model, not to the author

  met      modality.no-strengthening           verified
           `will` unchanged · a move to `is` would be a realm violation,
           not merely a certainty change

  unmet    numeric.value                       verified required
           A forecast's number is not checkable against a source. It is
           checkable against the MODEL that produced it. No model node is
           bound to this claim.
           reason: no meaning.inference or formula node supports c-0620
           repair: attach_source (the model) or remove_claim

  unmet    numeric.denominator                 measured required
           4,200 of what population, over what intake assumption? A
           projection without its base is unfalsifiable.
           repair: qualify_claim

  unmet    scope.temporal                      verified required
           "by Q4 2027" is a deadline. The model's horizon is not recorded,
           so nothing establishes the projection covers that far.
           repair: attach_source

  unmet    citation.resolution                 verified required
           The model is named in prose and resolves to no source version.
           repair: attach_source

  Gate under strict: HOLD (4 unmet)

  Note: a `simulation` claim is verified against its MODEL, its INPUTS and
  its ASSUMPTIONS — never against the world. Every obligation above asks
  whether the projection is traceable to a stated model, not whether 4,200
  is the right number. This system has no view on whether the forecast is
  correct and does not have a check that could form one.
```

**The note is the point of the third example.** A forecast is the class of claim most likely to be dressed as a fact and least amenable to verification, and the honest position is not to refuse it or to bless it but to make its apparatus checkable: which model, on which inputs, under which assumptions, over which horizon. That is exactly what [`../v5/SEMANTIC_IR.md`](../v5/SEMANTIC_IR.md) §6 says the `simulation` realm means, and the obligation set is what enforces it.

---

## 5. The `ProofPlanner` contract

**Status: executable in `scripts/wi.py`.**

```python
class ProofPlanner:
    """Derive obligations, evaluate them, and never do the second without the first.

    A planner is not a checker with a table of contents. The contract below is
    what separates the two, and every clause of it is a rule.
    """

    def derive(self, scope, target, policy) -> "ObligationSet":
        """Enumerate every obligation for the scope.

        MUST be total: every node in the scope contributes obligations or an
        explicit not_applicable with a rule id. A node the planner does not
        recognise raises; it does not silently contribute nothing.

        MUST be deterministic: same state, same target, same policy digest,
        same set, same order, same set digest.

        MUST NOT consult any check implementation. What must be shown does not
        depend on what this build can show. That is the whole inversion.
        """

    def evaluate(self, obligations, workspace) -> "ObligationSet":
        """Bind each obligation to a result, or to a reason it has none.

        MUST bind every result to the exact subject_state the obligation was
        derived against. A result computed against a different state marks the
        obligation stale, never met.

        MUST NOT add obligations. Discovering during evaluation that another
        check would be useful is a derivation change, and it goes in derive().
        """

    def coverage(self, obligations) -> dict:
        """A count against a stated population, per RELIABILITY_TYPES.

        Returns members, not only totals. Any count that cannot be expanded
        into the exact set it counts is a dashboard.
        """
```

**`derive` may not consult a check implementation, and that is the clause the whole design rests on.** If derivation asked *can we check this?*, the obligation set would shrink to the tool's current abilities and a release built by a less capable surface would report full coverage. Deriving blind means a surface with no PDF decoder still derives the anchor obligation on a PDF-anchored claim and reports it `unavailable`, which is the truth.

**`evaluate` may not add obligations**, because an obligation set that grows during evaluation has no denominator — coverage would be computed against a population that the act of measuring changed.

**The set has a digest.** `ObligationSet.digest` is a canonical hash over the ordered obligations, and it goes in the release manifest beside the gate verdict. Two releases holding the same digest were held to the same standard, provably. Two releases whose digests differ were not, and the difference is inspectable rather than a matter of recollection.

---

## 6. The deterministic check catalogue

**Status: executable in `scripts/wi.py`.**

Twenty-four checks. Each names exactly what it compares. Every one is deterministic: no model, no network, no judgment. A check absent from this catalogue cannot be an obligation's `check` field.

| Check | Compares |
|---|---|
| `anchor.integrity` | The stored locator still resolves in the named source version, and the quote digest recomputed from the bytes at that locator equals the recorded digest |
| `quotation.verbatim` | The quoted span in the document, byte-for-byte after the declared normalization, against the bytes at the anchor |
| `numeric.value` | The claim's structured `quantity` against the figure parsed at the anchored span — numeric equality on the field, never string equality on the rendering |
| `numeric.unit` | The claim's registered `unit` identity against the unit the source states for that figure |
| `numeric.dimension` | Dimensional consistency across an expression — that a rate divides a count by a period, that a currency carries its basis year, that two summed figures share a unit |
| `numeric.range` | A bounded claim's stated bound against the source's bound: `up to 38%` supported by a maximum, `at least 400` by a minimum. A point value does not satisfy a bound obligation, and a bound does not satisfy a point |
| `numeric.denominator` | That a proportion's denominator is stated and matches the population the source computed it over |
| `date.point` | A canonicalized ISO date in the claim against the date at the anchored span |
| `date.range` | Range type, start, end and granularity as a tuple — `since 2019` and `2019–2022` are different tuples |
| `entity.presence` | That each registered entity referenced by the claim appears in the anchored span under a registered name or alias |
| `citation.resolution` | That a citation-shaped reference resolves to a `source.artifact` present in the workspace, at a version the claim's anchors name |
| `scope.spatial` | The claim's `geographic_scope` against the territory the source's figures cover — county results are not statewide results |
| `scope.population` | The claim's `population_scope` against the source's `row_semantics` — who is counted, and who was filtered out before counting |
| `scope.temporal` | That the claim's period is contained by the anchored period. Containment, not overlap: a claim about 2019–2024 is not supported by a source covering 2019–2022 |
| `modality.no-strengthening` | The current `modality` against the modality at the last accepted decision, on the ordered lattice `may < should < will < is < must`. Strengthening without a decision fails; weakening is reported and does not fail |
| `negation.preservation` | The `negation` boolean against the negation at the anchored span. A dropped negation inverts the claim while barely changing the text |
| `attribution.preservation` | The `attribution` record, including `on_behalf_of`, against the attribution in the source. Removing an attribution converts a quoted party's claim into the author's |
| `definition.binding` | That every `uses_term` site resolves to the same `definition_state` digest the claim was verified under |
| `obligation.exception-preservation` | That every enumerated exception on an obligation node is present in every rendering of it. Absence in one rendering is a stricter duty asserted to that reader |
| `realm.preservation` | That the claim's realm is unchanged and that its support set contains no anchor from an incompatible realm — a `fictional_canon` anchor under an `external_fact` claim is an error, not a weak proof |
| `release.artifact-digest` | The bytes at the released path against the digest in the attestation. This is the check that answers *is the file in my hands the file that was checked?* |
| `release.closure-digest` | The proof closure recomputed from the graph against the digest the manifest names for that target |
| `decision.state-binding` | That every decision in the closure names a proposal that exists and a target state that exists, and that the target state is the one currently in force. A decision bound to a superseded state is stale, not met |
| `authority.grant-valid` | That an actor holding a valid, unexpired, in-scope grant took each act requiring one — see §7 |

**Six of these did not exist as named checks in v5** — `numeric.dimension`, `numeric.range`, `scope.population`, `obligation.exception-preservation`, `decision.state-binding` and `authority.grant-valid`. They are catalogued here because obligations are derived from state, and the state carried those dimensions all along. A dimension that can be compared and is not is a check somebody has to remember to do.

**`modality.no-strengthening` compares against the last decision, not against the source.** This is the check that catches the most common way a governed document degrades: a copyedit eighteen months on that turns `may` into `does`. There is no source to compare it against, because the source never said either — what is being protected is the last state a human approved.

**`scope.temporal` requires containment and not overlap**, and that is the difference between a check that works and one that reads as if it does. A source covering 2019–2022 overlaps a claim about 2019–2024, and a check accepting overlap would pass the claim while the last two years rest on nothing.

---

## 7. Authority as an obligation

**Status: executable in `scripts/wi.py`.**

Some acts require standing, not merely correctness. Creating a binding commitment, amending a filed document, waiving a hold in `regulated` mode, approving a claim on behalf of an organization — each is an act whose validity depends on who took it.

`wi authority` records and resolves grants. `authority.grant-valid` is the obligation that a grant was held.

```json
{
  "grant_id": "ag-0007",
  "scope": "binding_commitment",
  "granted_to": {"type": "authorized_editor", "id": "m.chen@example.org"},
  "granted_by": {"type": "human", "id": "d.okonkwo@example.org"},
  "targets": ["filings/*", "contracts/*"],
  "effective_from": "2026-01-01T00:00:00Z",
  "expires_at": "2026-12-31T23:59:59Z",
  "state": "active",
  "recorded_at": "2025-12-18T14:22:03Z"
}
```

Four rules, each of which exists because its absence is exploitable:

**A grant is a state, so it has a digest and it expires.** An unexpiring grant recorded once and never revisited is indistinguishable from no governance at all, three years later.

**A `judgment_provider` may not hold a grant.** This follows from the actor model in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) §5 — a model may not write a record typed `human`, `team_member` or `authorized_editor`, and it may not sign a decision. It may not hold authority either, because authority is what makes a signature mean something.

**A grant cannot be self-issued.** `granted_by` and `granted_to` must be different actors. The check is a comparison, not a policy, and it is here rather than in configuration because a self-issued grant is not a bad configuration — it is the absence of authority wearing its clothes.

**Two branches recording incompatible grants over the same scope is a merge conflict of kind `authority`**, per [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) §4.1. It is in the `always_conflict` list, so the engine will not propose a resolution. Which of two people holds signing authority is not a question with an algorithmic answer, and a merge tool offering a default would get that default accepted.

**And an authority gap is not repairable by any editing action.** This is why the lexicographic ordering in [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) §7 places authority escalation above human review: every other component is work somebody in the loop can do, and this one is a dependency on somebody outside it.

---

## 8. Why a declared set beats a hidden checklist

**Status: executable in `scripts/wi.py`.**

`wi gate` evaluates a declared obligation set. It does not run a checklist compiled into a command. The difference is five properties, and each one is unavailable to the checklist design.

**The set is inspectable before the verdict.** An author can run `wi obligations` and see what will be required — before writing, before anchoring, before the deadline. A hidden checklist is discoverable only by failing it.

**The set has a digest, so two documents are comparable.** "We held both filings to the same standard" is a digest comparison. Under a compiled checklist it is a claim about two runs of the same binary, which stops being true the moment the binary changes and gives no signal that it did.

**Adding a check is visible as a standard change.** Under the obligation design, a new check adds an obligation, the set digest moves, and every prior release reports it unmet against the new standard. Under a compiled checklist, a new check simply starts running, and every document checked before it exists appears — retroactively, in the same visual language — to have been held to a standard it never met. That is the silent-widening failure [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) §7 protects the word `verified` from, arriving through the back door of an implementation detail.

**Coverage becomes a measurement.** A denominator exists because the set exists. "31 of 34" carries membership; "all checks passed" carries a structure that implies coverage the run never had.

**The gate is separable from the planner.** The gate compares statuses to severities. It does not know what a numeric check is. That separation means the severity policy can be audited by somebody who does not read code, and it means a surface may render the obligation set without being able to evaluate it — which is exactly what a reviewer holding a `hash-only` bundle needs.

The obligation set travels in the release bundle, in `proof/`, beside the results. A reader of a `.wiab` can see what was required, what was met, what was not, and why — which is the eleven questions in [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) §1 answered at the level of the standard rather than the level of the run.

---

## 9. The closed reliability basis

**Status: executable in `scripts/wi.py`.**

Restated here because an obligation names a `required_basis`, and the enum is closed.

| Member | Produced by |
|---|---|
| `verified` | A deterministic comparison that executed and passed |
| `measured` | A quantity computed against a stated baseline, with a visible denominator |
| `judged` | A reasoned assessment by a named provider, with no external comparison behind it |
| `human-declared` | A named human asserting something on their own authority |

**There is no `confident`. There is no `ai_verified`. There is no `94.7% true`. There is no fifth member, and there is no numeric field anywhere in an obligation record where one could be written.**

An obligation requiring `verified` is met only by a deterministic result. A judgment does not satisfy it — not at any provider quality, not at any agreement rate across providers, not with a calibration study attached. The type names *how the result was produced*, and a judgment was produced by reading. A calibration result is itself `measured`, and it must publish its benchmark set and its N.

**Why this belongs in the obligations document rather than only in the types document.** The obligation set is where the pressure lands. A release blocked by one unmet `verified` obligation, on a deadline, with a provider available that would happily return an opinion about it, is the exact moment somebody proposes that a sufficiently confident judgment ought to count. It is a reasonable-sounding proposal and it is the end of the system: once one obligation can be satisfied by a judgment, `verified` means "we did something," and every artifact ever issued under the word is retroactively weaker without anyone editing it.

The correct action at that moment is a waiver — a named person choosing to proceed, bound to the exact state, with a recorded reason. That is honest, it is auditable, it is reversible, and it does not spend a word that other people's compliance processes depend on.

Full treatment: [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md). The amendment rule that protects `verified` is [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) §7.

---

## 10. Benchmarks

**Status: specified.** The derivation fixtures are shipped; the coverage harness across all twenty-four checks is defined here and partially implemented.

Derivation is scored on **exact set equality against hand-authored expected sets**, per node kind and per realm.

| Case | Asserts |
|---|---|
| `external_fact` claim with quantity, unit and closed date range | Exactly the 8-obligation set of §4.1, in canonical order, with a stable set digest |
| Same claim, realm changed to `author_observation` | Numeric and anchor obligations disappear; attribution and realm obligations appear; no obligation is silently retained |
| Same claim, target changed from `internal` to `filing` | Membership grows by exactly the target-derived obligations; no state-derived obligation changes |
| Same claim, policy mode `standard` → `regulated` | Membership is **identical**; only severities move |
| Proportion claim with no stated denominator | `numeric.denominator` present and `unmet`, never omitted |
| Obligation node whose exception is dropped from one of four renderings | `obligation.exception-preservation` unmet, naming the rendering |
| Claim whose modality moved with no intervening decision | `modality.no-strengthening` unmet; a weakening reports and does not fail |
| Claim supported only by a `fictional_canon` anchor while typed `external_fact` | `realm.preservation` unmet, classified as an error rather than a weak proof |
| Surface with no PDF decoder, PDF-anchored claim | Obligation derived; status `unavailable`; **not** absent from the set |
| Check specified in §6 with no implementation | Status `no_implementation`; appears in the coverage denominator |
| Node kind the planner does not recognise | `derive` raises. It does not return an empty set |
| Same state, target and policy digest, run twice | Byte-identical set digest |

**The assertion checked on every case:** *the obligation set derived without consulting any check implementation equals the set derived with all implementations available.* That is the mechanical form of the §5 contract, and a planner failing it has begun deriving what it can do rather than what is required — which is the failure that would be invisible, because the reports would all be green.

---

## 11. What is executable and what is specified

| Mechanism | Status |
|---|---|
| `wi obligations`, derivation from state, target and policy | Executable in `scripts/wi.py` |
| `ProofObligation`, the seven statuses, required `unmet_reason` | Executable in `scripts/wi.py` |
| Rule ids on every obligation, and `derived_from` in the record | Executable in `scripts/wi.py` |
| `ObligationSet` digest, and its presence in the release manifest | Executable in `scripts/wi.py` |
| Coverage as a count with expandable membership | Executable in `scripts/wi.py` |
| `wi gate` evaluating a declared set rather than a compiled checklist | Executable in `scripts/wi.py` |
| `wi authority`, grant records, self-issue and expiry checks | Executable in `scripts/wi.py` |
| The 24-check catalogue as a closed vocabulary | Executable in `scripts/wi.py` |
| `anchor.integrity`, `quotation.verbatim`, `numeric.*`, `date.*`, `scope.temporal`, `modality.no-strengthening`, `negation.preservation`, `attribution.preservation`, `definition.binding`, `realm.preservation`, `release.*`, `decision.state-binding`, `authority.grant-valid` over text sources | Executable in `scripts/wi.py` |
| `scope.spatial`, `scope.population` over sources with declared row semantics | Executable in `scripts/wi.py` |
| `entity.presence` beyond registered-name matching | Specified |
| `numeric.dimension` across multi-source derived expressions | Specified |
| Every check over PDF, spreadsheet, audio, video and image anchors | Specified — awaiting the adapters in [`../v5/EVIDENCE_ANCHORS.md`](../v5/EVIDENCE_ANCHORS.md) |
| Coverage harness across all twenty-four checks | Specified |

---

## Related documents

- [`ARGUMENT_GRAPH.md`](ARGUMENT_GRAPH.md) — obligations over inference, premises and defeaters
- [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) — `must_be_reproved` is an obligation-set delta
- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — what a merged state owes, and the `authority` conflict kind
- [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) — the closed basis enum in full
- [`../v5/POLICY_AS_CODE.md`](../v5/POLICY_AS_CODE.md) — the policy object that sets severity
- [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) — where the obligation set travels
- [`../v5/EVIDENCE_ANCHORS.md`](../v5/EVIDENCE_ANCHORS.md) — anchor integrity and the raw-bytes rule
- [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — Law C, Law D, Law E and the actor model
- [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) — waivers, and the original status vocabulary
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
