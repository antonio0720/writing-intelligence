# The Argument Graph

Reasoning becomes inspectable without being mistaken for deterministic truth.

**Status: executable in `scripts/wi.py`.**

`wi why` runs today. It walks the argument graph from a conclusion to its premises, names the inference rule that connects them, reports each premise's own reliability basis, lists the recorded defeaters, and enumerates every place the conclusion renders.

Every layer below this one handles assertions that point at something. A claim atom has an anchor; an anchor resolves to bytes; the bytes either say the thing or they do not. That machinery is why [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) Law D is the one anti-fabrication mechanism that does not depend on a model being careful.

Consequential documents are not made of those sentences alone. They are made of those sentences **plus the conclusions drawn from them**, and the conclusion is usually the sentence the reader remembers. *The program is fiscally sustainable through 2029.* Nothing in a source says that. It is reached, from things sources do say, by a step somebody took.

v5 had two honest options for such a sentence and both were bad. Call it `needs_source` — true, useless, and it fires on every conclusion in every analytical document ever written. Or let a judgment provider bless it, producing a `judged` record that says a model found it reasonable, which tells a reader nothing they can act on.

v6 adds a third: **record the step.**

---

## Table of contents

1. Why reasoning needs a node type
2. The `Argument` node
3. The inference rule vocabulary
4. What the system can and cannot verify
5. Defeaters
6. `wi why` — a worked transcript
7. Why this beats painting a sentence green
8. Arguments under merge, simulation and obligation
9. Benchmarks
10. What is executable and what is specified

---

## 1. Why reasoning needs a node type

**Status: executable in `scripts/wi.py`.**

v5 already carries `meaning.inference` in the node families of [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) §2.2 — *a conclusion reached by reasoning beyond what any source states.* It is a node with a name and no internal structure. You can point at it. You cannot ask it anything.

The questions people actually ask about a conclusion are structural:

| Question | Answerable without an argument node? |
|---|---|
| What is this resting on? | No. `derived_from` edges say *something* preceded it, not what role each thing played. |
| Is every one of those things itself supported? | No — and this is the one that matters, because a conclusion built on four premises where one is unsupported is a conclusion with a hole in it, and the hole is invisible at the conclusion. |
| What kind of step is this — deduction, projection, analogy? | No. |
| What would have to be true for this to fail? | No. |
| Did the conclusion get stronger than the argument justifies? | No. Nothing records what the argument justified. |
| Where else does this conclusion appear? | Partly — `renders_as` answers it for the surface, not for the reasoning. |

**Why this is load-bearing.** The failure mode in analytical writing is not fabrication. It is a conclusion that was reasonable when written and has since been separated from what made it reasonable: the qualifying premise was cut for length, the model it rested on was superseded, the assumption stopped holding, or the sentence was tightened in a later pass until it asserted more than the argument ever supported. In every one of those cases the conclusion still *reads* well, and no check in v5 fires, because there is no recorded relationship for a check to test.

An argument node makes the relationship a thing in the graph. Once it is a thing in the graph, [`../v5/STALENESS.md`](../v5/STALENESS.md) propagates through it, [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) derives obligations over it, and [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) can be asked what happens if a premise is removed.

---

## 2. The `Argument` node

**Status: executable in `scripts/wi.py`.**

```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Premise:
    """One thing the argument rests on, and the role it plays."""
    logical_id: str            # a meaning.claim_atom, meaning.inference, or canon.*
    role: str                  # "evidence" | "assumption" | "definition"
                               # | "model_output" | "prior_conclusion"
    required: bool = True      # False for a premise that strengthens but is not load-bearing
    note: str = ""


@dataclass(frozen=True)
class Warrant:
    """Why the rule licenses this step, for these premises.

    Toulmin's term, used in his sense: the warrant is what connects the
    evidence to the claim, and it is usually the part nobody writes down.
    """
    statement: str
    basis: str                 # "verified" | "measured" | "judged" | "human-declared"
    support: List[str] = field(default_factory=list)   # anchors or node ids


@dataclass(frozen=True)
class Defeater:
    """A condition under which the conclusion would not follow.

    Recorded by the author, not inferred. A defeater the system invented
    would be a machine deciding what could undermine somebody's reasoning.
    """
    defeater_id: str
    statement: str
    kind: str                  # "rebutting" | "undercutting" | "undermining"
    watch: Optional[str] = None    # a logical id whose state change triggers review
    status: str = "not_triggered"  # "not_triggered" | "triggered" | "unmeasurable"
    evidence: Optional[str] = None


@dataclass(frozen=True)
class Argument:
    argument_id: str
    conclusion: str                    # logical id of the meaning.inference it produces
    premises: List[Premise]
    rule: str                          # an InferenceRule member, §3
    warrants: List[Warrant] = field(default_factory=list)
    defeaters: List[Defeater] = field(default_factory=list)

    strength_claimed: str = "supports"   # "entails" | "supports" | "suggests"
    author: Dict[str, Any] = field(default_factory=dict)   # the actor who made the step
    state_digest: str = ""
```

Four fields carry the design.

**`role` on a premise, not just a reference.** A definition, an empirical finding, an assumption and a model output are four different things to depend on, and they fail differently. An assumption that stops holding is a live risk; a definition that is rebound is a mechanical propagation; a model output that is superseded invalidates everything computed from it. `derived_from` alone flattens all four into "came before."

**`required`.** An argument commonly cites supporting material that is not load-bearing. Marking it lets the impact walk distinguish *this premise fell and the conclusion is unsupported* from *this premise fell and the conclusion still stands on the other three*, which is precisely the discrimination that keeps an impact report from crying wolf.

**`strength_claimed`, closed at three values.** `entails` means the conclusion cannot be false if the premises are true. `supports` means the premises make it more reasonable. `suggests` is weaker still. The field exists so that `modality.no-strengthening` from [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) §6 has something to compare against: a conclusion whose rendered modality moves to `is` while its argument claims `suggests` has strengthened past its own basis, and that is a check, not an opinion.

**`author`.** A step in reasoning was taken by somebody. Under the actor model in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) §5, a `judgment_provider` may propose an argument and may not be its author, because an argument is an assertion about what follows from what and a model may not assert on its own authority.

---

## 3. The inference rule vocabulary

**Status: executable in `scripts/wi.py`.**

Nine rules. The vocabulary is closed. A step that does not fit one of them is recorded as `unclassified` and reported as such, never assigned the nearest fit.

| Rule | The step | What it can go wrong by |
|---|---|---|
| `deductive` | The conclusion follows necessarily from the premises | A false premise; a form that is not actually valid |
| `inductive` | A general pattern inferred from observed instances | Too few instances; instances not representative of the population claimed |
| `abductive` | The best available explanation of an observation | A better explanation not considered; "best available" mistaken for "true" |
| `causal_model` | A causal claim from a stated model of a mechanism | The mechanism not established; confounders unaddressed; correlation asserted as causation |
| `statistical_generalization` | A population property inferred from a sample | Sampling frame; sample size; the denominator |
| `analogy` | What holds in one case is argued to hold in a relevantly similar one | The relevant similarity not established; a disanalogy that matters |
| `legal_application` | A rule applied to facts to reach a legal conclusion | Facts not established; the rule superseded; an exception unaddressed |
| `policy_projection` | A future state projected from present conditions and stated assumptions | An assumption that stops holding; a horizon beyond the model's validity |
| `narrative_inference` | A conclusion about a constructed world drawn from its canon | Canon that has since moved; a rule of the world not applied |

**The rule is recorded, not detected.** The engine does not read a paragraph and decide it contains an analogy. The author states which step they took, or a judgment provider proposes one and a human accepts it under Law A. A system that classified inference rules by reading would be making a `judged` assertion and storing it in a field that every downstream check treats as structural.

**`unclassified` is a real value and it is reported.** An argument whose rule nobody has stated is a recorded gap. Forcing it into `inductive` because it looks like one produces an argument whose stated form is wrong, and every obligation derived from that form is derived from a fiction.

**Why the vocabulary is closed.** Each rule determines which obligations attach. `statistical_generalization` derives a `numeric.denominator` obligation and a sampling-frame obligation; `policy_projection` derives a horizon obligation and an assumption-currency obligation; `legal_application` derives an exception-preservation obligation. An open vocabulary would mean an argument could be recorded under a rule with no obligations attached, which is a way to get a conclusion into a document with nothing asking anything of it.

---

## 4. What the system can and cannot verify

**Status: executable in `scripts/wi.py`.**

This is the section the document exists for, and both halves are stated flatly.

### 4.1 What it can verify

Five things, all deterministic, none of them requiring anybody to read the argument.

| It can verify | By |
|---|---|
| **Every cited premise exists** | Resolving each `Premise.logical_id` to a node in the graph. A premise that names nothing is a dangling reference — the argument cites something that is not there. |
| **Every premise carries its own proof state** | Reading each premise's obligation set and reliability basis. The argument does not inherit a status; it reports the statuses beneath it, individually and by type. |
| **A declared exception was not dropped** | Comparing the exceptions on every `definition` and `legal_application` premise against the renderings of the conclusion. `obligation.exception-preservation` from [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) §6, applied through the argument. |
| **The conclusion did not strengthen beyond the stored argument state** | Comparing the conclusion's current `modality` and `certainty` against the values at the last accepted decision, and against `strength_claimed`. A `suggests` argument whose conclusion now reads `is` fails. |
| **The same chain renders consistently across outputs** | Walking `renders_as` from the conclusion and comparing the semantic state at each site. A conclusion hedged in the book and unhedged in the deck is a detectable inconsistency, not a stylistic difference. |

Each of those is a comparison. None is an assessment. All of them produce `verified` records a stranger can reproduce.

### 4.2 What it cannot verify

**It cannot verify that an inductive inference is persuasive.** Whether four cohorts justify a generalization to a fifth is a question about the world, the sampling, the domain and the stakes. There is no comparison that settles it, and no threshold of provider agreement that turns it into one.

**It cannot verify that a warrant is sound.** A warrant is the connecting principle. Judging it requires knowing the field.

**It cannot verify that the defeaters are the right ones.** It can check whether a recorded defeater has triggered. It has no way to know which defeaters were never written down, and the unrecorded ones are the dangerous ones.

**It cannot verify that the rule was the right rule.** An argument recorded as `causal_model` that is really a `statistical_generalization` will be checked against the wrong obligations, correctly.

**It cannot verify that the conclusion is true.** Not for any argument, under any rule, at any premise quality. An argument with every premise `verified`, no triggered defeater and a valid form has established that the reasoning is intact and the inputs check out. That is a genuinely valuable thing and it is not truth.

**Why the second list is published as prominently as the first.** A tool that lists what it checks and stays quiet about what it does not is Law C violated by structure — the reader infers coverage from the shape of the report. The five things in §4.1 are worth a great deal precisely because the list is short and closed: they are the parts of "is this argument any good" that can be settled by machinery, and separating them from the parts that cannot is what stops the machinery from being read as a verdict on the reasoning.

---

## 5. Defeaters

**Status: executable in `scripts/wi.py`.**

A defeater is a condition under which the conclusion would not follow. Three kinds, and the distinction is not academic — it changes what a triggered defeater does.

| Kind | Attacks | When triggered |
|---|---|---|
| `rebutting` | The conclusion directly | The conclusion is contradicted. It becomes `becomes_false` under [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) §3. |
| `undercutting` | The inference step | The premises may still hold; the step no longer licenses the conclusion. The conclusion drops to unsupported, not false. |
| `undermining` | A premise | That premise fails; the conclusion's status is recomputed from the remaining `required` premises. |

**`watch` is what makes a defeater a live check rather than a note.** A defeater carrying `watch: "c-0411"` is registered against that node, and any state change to it puts the defeater into review through the ordinary invalidation walk. A defeater with no `watch` is a stated risk nobody is monitoring, and it reports as `unmeasurable` rather than as `not_triggered` — because *nothing is watching this* and *this has not happened* are different facts, and the second is the one a reader will assume.

**Defeaters are authored.** The system does not generate them. A generated defeater set would be a model deciding what could undermine somebody's reasoning and recording that decision in a field the author is then accountable for. A provider may *propose* defeaters — that is a genuinely useful thing for a provider to do — and the proposal goes through Law A like every other proposal.

---

## 6. `wi why` — a worked transcript

**Status: executable in `scripts/wi.py`.**

```
$ python3 scripts/wi.py why c-0704

CONCLUSION  c-0704   meaning.inference   realm simulation
            "The program is fiscally sustainable through 2029 under
             current funding."

            basis        derived — this conclusion has no anchor and is
                         not verifiable against any source. It is reached
                         by argument arg-0031.
            strength     supports          (not: entails)
            modality     may               unchanged since d-0208
            author       d.okonkwo@example.org  ·  team_member

  ─────────────────────────────────────────────────────────────────────────
  ARGUMENT  arg-0031        rule: policy_projection

  PREMISES  4 required · 1 supporting

    p1  required   evidence
        c-0688  "The 2026 appropriation is $4.1M."
        basis   VERIFIED · deterministic
                a-0512 state_budget_2026.pdf@v1 p.214 table 7 row 12
                numeric.value · numeric.unit · numeric.dimension all met

    p2  required   measured
        c-0691  "Cost per placement was $1,940 across 2024–2025."
        basis   MEASURED · 2,113 placements over 2 program years
                denominator stated · baseline: audited program ledger @v4
                NOT verified — this is a computation over our own records,
                not a figure any external source states.

    p3  required   assumption
        c-0693  "Placement volume grows no faster than 6% annually."
        basis   HUMAN-DECLARED · d.okonkwo@example.org · 2026-01-14
                An assumption the author asserted on their own authority.
                No source states it. Nothing in this workspace tests it.
                → watched by defeater df-0003

    p4  required   model_output
        c-0698  "Reserve balance remains positive through FY2029."
        basis   derived — output of the 2026 capacity model (mdl-0004)
                inherits the status of its inputs and assumptions
                model horizon: FY2030 · claim horizon FY2029 is inside it

    p5  supporting judged
        c-0701  "Partner renewal is likely at current service levels."
        basis   JUDGED · provider: (none configured on this surface)
                result: needs_review
                NOT required. The conclusion does not rest on it, and
                removing it changes nothing about the argument's status.

  WARRANT
        "A program whose per-unit cost is stable and whose reserve
         remains positive across the projection horizon is fiscally
         sustainable across that horizon."
        basis   HUMAN-DECLARED · d.okonkwo@example.org
        This is the connecting principle. It is asserted, not established.
        A reader who disagrees with the warrant rejects the conclusion
        without disputing a single premise.

  DEFEATERS  3 recorded · 0 triggered · 1 unmeasurable

    df-0001  rebutting     "The appropriation is reduced or not renewed."
             watch  c-0688 (appropriation)      status  not_triggered
             The 2026 figure is current. FY2027 is not yet appropriated;
             this defeater is expected to become live in the next cycle.

    df-0002  undermining   "Cost per placement rises above $2,200."
             watch  c-0691 (cost per placement) status  not_triggered
             current $1,940 · threshold $2,200 · headroom 13.4%

    df-0003  undercutting  "Growth exceeds 6% and the projection's basis
                            no longer holds."
             watch  c-0693 (growth assumption)  status  UNMEASURABLE
             Nothing in this workspace measures actual growth against the
             assumption. The defeater is recorded and unmonitored.
             repair: attach_source (enrollment series) · 1 action

  ─────────────────────────────────────────────────────────────────────────
  RENDERS IN  6 places

    ch-14 ¶7              "may be fiscally sustainable through 2029"     hedged
    exec-summary ¶2       "is positioned for sustainability through 2029" hedged
    deck slide-04         "SUSTAINABLE THROUGH 2029"                     UNHEDGED
    web/funding.html §3   "expected to remain sustainable through 2029"  hedged
    filing §6 ¶1          "projected to be sustainable through FY2029"   hedged
    board_memo ¶4         "sustainable through 2029 under current funding" hedged

    INCONSISTENT RENDERING   1 site
      deck slide-04 asserts without the modality the argument carries.
      The argument claims `supports`, the conclusion's modality is `may`,
      and this rendering reads as an unqualified assertion.
      check: modality.no-strengthening · status UNMET at this site
      repair: restore_hedge · 1 human decision

  ─────────────────────────────────────────────────────────────────────────
  WHAT THIS OUTPUT DOES NOT SAY

    It does not say the program is fiscally sustainable.
    It says: the argument is well-formed, its four required premises
    resolve, one is verified, one is measured, one is an author's
    assumption and one is a model output; no defeater has triggered; one
    defeater is unmonitored; and one of six renderings asserts more than
    the argument claims.

Checks run: premise resolution · per-premise basis · exception preservation ·
modality against stored argument state · cross-rendering consistency ·
defeater watch resolution.
Not run: paraphrase support for p5 (no judgment provider on this surface) ·
soundness of the warrant (not checkable by any mechanism in this system).
```

---

## 7. Why this beats painting a sentence green

**Status: executable in `scripts/wi.py`.**

The alternative design is one badge. Run the argument through an assessment, get back `supported` or a score, render it beside the sentence.

That design is more compact, easier to build, and easier to sell. It fails in five ways, and the transcript above shows each one.

**A badge averages four unlike things.** p1 is `verified`, p2 is `measured`, p3 is `human-declared` and p4 is derived. Any single indicator over that mix has to pick a rule — the weakest, the average, the modal — and every rule discards the information a reader needs. The one that matters here is p3: **the conclusion rests on an assumption the author made up.** That is not a criticism; it is how projections work. It is also the first thing a board member should know, and it is exactly what a green badge erases.

**A badge cannot express `unmeasurable`.** `df-0003` is recorded, unmonitored, and attached to the assumption the whole projection rests on. It is the single most useful line in the report and there is no colour for it.

**A badge is computed at the conclusion, so it cannot see the renderings.** The unhedged deck slide is a semantic inconsistency between two sites of one conclusion. Nothing that scores the sentence can find it, because the defect is a relationship between two sentences neither of which is individually wrong.

**A badge invites the strengthening it should prevent.** A sentence marked supported is a sentence somebody will tighten in the next pass, because it has been blessed. `modality.no-strengthening` compares against the stored argument state and catches that; a badge is the thing that encouraged it.

**A badge cannot be argued with.** A reader who disagrees with the warrant — *"stable unit cost plus positive reserve equals sustainable"* — has a substantive objection that leaves every premise intact. Under `wi why` they can say which line they reject. Under a badge, disagreement has nothing to attach to, so it becomes an argument about the tool.

**The deeper reason.** A badge answers *should I believe this?* — a question the system is not entitled to answer. `wi why` answers *what is this made of, and what would have to be true for it to fail?* That is the question a reviewer, an auditor, a board member and opposing counsel are all actually asking, and it is answerable from structure. Making the reasoning inspectable is more honest than making it look settled, and it is more useful, because it hands the reader the specific thing to check.

---

## 8. Arguments under merge, simulation and obligation

**Status: executable in `scripts/wi.py`.**

**Merge.** An `Argument` is a node with a logical id, so it merges under [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) §3. Two branches editing disjoint parts — one adding a defeater, one restating a warrant — merge dimension-wise. Two branches changing `rule`, `strength_claimed`, or the `required` flag on the same premise conflict, and there is no averaging of a strength claim: `entails` and `supports` do not merge to something in between, for the reason §5 of the merge protocol gives about splitting the difference.

**Removing a premise on one branch while another strengthens the conclusion is a conflict even though the dimensions are disjoint**, by the same evidence-support precondition: the composed state is an argument standing on fewer premises and claiming more, which neither branch asserted.

**Simulation.** `wi simulate --remove-premise c-0693` answers the question a reviewer actually asks — *what if the growth assumption is wrong?* The report names the conclusions that lose a required premise, the defeaters that trigger, the renderings that must be requalified and the release targets that change. That is the argument graph earning its keep: without recorded premises, the question has no mechanical form.

**Obligations.** The rule determines the obligation set. `policy_projection` derives:

| Obligation | Because |
|---|---|
| `scope.temporal` on the conclusion | The claim horizon must be contained by the model horizon — FY2029 inside FY2030 |
| `numeric.denominator` on every `measured` premise | p2 is a rate over a stated population |
| `attribution.preservation` on every `assumption` premise | An assumption must render as the author's, never as a finding |
| `realm.preservation` on the conclusion | A `simulation` claim must carry its model marker in every rendering |
| `modality.no-strengthening` at every render site | Six sites, six comparisons — which is how slide-04 was caught |

A `statistical_generalization` derives a different set, and a `legal_application` a different one again. That is why the vocabulary in §3 is closed: the rule is the key into the obligation table.

---

## 9. Benchmarks

**Status: specified.** The structural fixtures are shipped; scoring for provider-proposed rules and defeaters is defined here and unimplemented.

Arguments are scored on **structural assertions only**. There is no benchmark for whether an argument is good, because there is no ground truth this project could honestly construct for that.

| Case | Asserts |
|---|---|
| Argument with a premise naming a node that does not exist | Dangling premise reported; conclusion status is `unsupported`, never `met` |
| Argument with one `required: False` premise unsupported | Conclusion status unchanged; the supporting premise is reported separately |
| Argument with one `required: True` premise unsupported | Conclusion drops to unsupported and names which premise |
| Conclusion modality moved to `is` while `strength_claimed` is `suggests` | `modality.no-strengthening` unmet at every site where it moved |
| Six renderings, one unhedged | Exactly one inconsistency, naming the site |
| `legal_application` premise with an exception dropped in one rendering | `obligation.exception-preservation` unmet, naming that rendering |
| Defeater with no `watch` | Status `unmeasurable`, never `not_triggered` |
| Defeater whose watched node changes state | Status `triggered`; the conclusion enters review through the ordinary walk |
| Argument with `rule: unclassified` | Reported as unclassified; no obligation set is derived from a guessed rule |
| Chain of five arguments, the deepest premise invalidated | Every downstream conclusion reached; each reports the specific broken premise, not a generic failure |
| Two branches changing `strength_claimed` differently | Conflict; no intermediate value appears in any output |

**The assertion checked on every case:** *no output field asserts that a conclusion is true.* The record vocabulary has no member for it, and a benchmark that could pass while such a value existed would be testing the wrong thing.

---

## 10. What is executable and what is specified

| Mechanism | Status |
|---|---|
| The `Argument` node, `Premise` roles, `Warrant`, `Defeater` | Executable in `scripts/wi.py` |
| The nine-rule closed vocabulary and `unclassified` | Executable in `scripts/wi.py` |
| Premise resolution and per-premise basis reporting | Executable in `scripts/wi.py` |
| `strength_claimed` compared against rendered modality | Executable in `scripts/wi.py` |
| Cross-rendering consistency over `renders_as` | Executable in `scripts/wi.py` |
| Defeater `watch` registration and trigger detection | Executable in `scripts/wi.py` |
| `unmeasurable` for an unwatched defeater | Executable in `scripts/wi.py` |
| `wi why` traversal and rendering | Executable in `scripts/wi.py` |
| Rule-keyed obligation derivation | Executable in `scripts/wi.py` |
| Argument merge and the strength-claim conflict | Executable in `scripts/wi.py` |
| `wi simulate --remove-premise` | Executable in `scripts/wi.py` |
| Provider-proposed inference rules and defeaters | Specified — see [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) |
| Assessment of warrant soundness | **Permanently out of scope.** No mechanism in this system evaluates it, and none is planned. |
| Scoring harness for provider-proposed structure | Specified |

---

## Related documents

- [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) — the rule-keyed obligation sets an argument derives
- [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) — removing a premise and reading the consequence
- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — merging arguments; why strength claims do not average
- [`SEMANTIC_SOURCE_MAPS.md`](SEMANTIC_SOURCE_MAPS.md) — how the six render sites are located in released bytes
- [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) — `meaning.inference` and `meaning.premise` in the node families
- [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) — the four bases a premise can carry, and why they never average
- [`../v5/SEMANTIC_IR.md`](../v5/SEMANTIC_IR.md) — realms, and what `simulation` means
- [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) — the provider contract for proposed structure
- [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — Law A, Law C, Law D and the actor model
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
