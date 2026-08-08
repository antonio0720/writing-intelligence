# Counterfactual Simulation

Ask what a change would do before making it. This is the mechanism that distinguishes v6 from v5, and the distinction is one word: *before*.

**Status: executable in `scripts/wi.py`.**

`wi simulate` runs today. It creates an ephemeral branch, applies a proposed mutation, computes the full consequence, and discards the branch. It commits nothing.

v5 answers a question asked after the fact: *what broke when this source changed?* [`../v5/STALENESS.md`](../v5/STALENESS.md) is the machinery, and it is good machinery — it turns verification into a build system and prints a minimum repair frontier instead of a wall of red.

But it only ever runs after somebody has already changed something. The author who most needs the answer is the one deciding whether to change it, and they are standing at the moment before, with no way to look.

v6 answers, for a mutation that has not happened:

> **What becomes true. What becomes false. What becomes stale. What must be re-proved. Which outputs change. Which decisions expire. What it costs to repair. And what remains provably untouched.**

Read this with [`../v5/STALENESS.md`](../v5/STALENESS.md), whose invalidation walk this reuses without modification, and with [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md), because a merge is one of the mutations a simulation can be asked about.

---

## Table of contents

1. The distinction, stated precisely
2. Simulation is an ephemeral branch
3. `SimulationRequest` and `SimulationReport`
4. A worked transcript
5. The provably unaffected block
6. Repair planning as constrained optimization
7. The lexicographic safety ordering
8. Why a single blended cost score is forbidden
9. What a simulation cannot tell you
10. Benchmarks
11. What is executable and what is specified

---

## 1. The distinction, stated precisely

**Status: executable in `scripts/wi.py`.**

| | v5 `wi impact` | v6 `wi simulate` |
|---|---|---|
| Runs | After a state changed | Before any state changes |
| Input | A changed source or node | A proposed mutation |
| The workspace | Already mutated | Untouched, and provably so |
| Answers | What is now stale | What *would become* stale, false, unproved, expired |
| Produces | A repair frontier for damage that exists | A repair frontier for damage that does not exist yet, and a cost for avoiding it |
| Can be run | Once the decision is irreversible | While the decision is still a decision |

**Why this is load-bearing.** Every consequential edit in a governed document is made by somebody who cannot see past it. They know what the sentence says now and what they want it to say; they do not know that the number appears in a footnote in chapter 14, in a chart caption, in a slide the board approved in March, and in a policy brief that was filed with a regulator. v5 tells them afterward, which is genuinely valuable and arrives at the wrong time — the author has already committed, already told the partner, already redrafted around the new figure.

The gap between *"I want to raise this threshold"* and *"raising this threshold costs eleven re-proofs, two waiver renewals and a board re-approval"* is the entire difference between a document that stays governed and one whose governance is quietly abandoned on the first expensive change. Nobody abandons a discipline deliberately. They abandon it once, under deadline, when the cost of compliance was discovered too late to plan around.

A simulation moves the discovery earlier, and that is all it does. It computes nothing v5 could not compute. It computes it while the answer can still change what somebody does.

---

## 2. Simulation is an ephemeral branch

**Status: executable in `scripts/wi.py`.**

A simulation is implemented as a branch that is created, mutated, walked and destroyed.

```
current tip ──┬── (unchanged, never touched)
              │
              └── sim/<simulation_id>   created → mutated → analyzed → dropped
```

Five properties, each a rule rather than an implementation detail:

**It commits nothing.** `wi simulate` never advances any named branch, never writes a `verification.result`, never writes an `authorship.decision`, and never records an invalidation against a real state. The ephemeral branch is dropped when the report is produced, whether the report is good news or bad.

**It leaves an audit record of having been run, and that record contains no state.** A `simulation.run` entry records who asked, what mutation was proposed, when, and the digest of the report. It does not record a graph state, because there is no graph state to record — the states the simulation examined never existed outside the walk.

**It is deterministic and repeatable.** The same workspace state and the same `SimulationRequest` produce a byte-identical `SimulationReport`. That is what makes a report quotable in a decision: two people running it get the same answer, and a report attached to a proposal can be re-derived by whoever reviews the proposal a week later.

**It reuses the invalidation engine unchanged.** The traversal, the per-edge policy table and the byte-region non-propagation rule from [`../v5/STALENESS.md`](../v5/STALENESS.md) §2 and §3 are the same code. A simulation that had its own propagation logic would be a second implementation of "what depends on what," and Law K exists because two implementations of one truth disagree on the fifth edge case, in the surface with fewer tests, on the document that mattered.

**It pins to one graph version.** The walk reads a single graph state captured at entry, for the reason [`../v5/STALENESS.md`](../v5/STALENESS.md) §2 names: a walk that reads mutable current state mid-traversal produces a result computed against several graph states at once, internally inconsistent and non-reproducible.

---

## 3. `SimulationRequest` and `SimulationReport`

**Status: executable in `scripts/wi.py`.**

```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ProposedMutation:
    """One change to evaluate. A simulation may carry several."""
    kind: str                 # "set_dimension" | "rebind_anchor" | "replace_source_version"
                              # | "delete_node" | "add_node" | "merge_branch"
                              # | "change_policy" | "revoke_authority"
    logical_id: Optional[str] # None for source-level and policy-level mutations
    dimension: Optional[str]  # "quantity", "modality", "temporal_scope", ...
    from_value: Any
    to_value: Any
    note: str = ""


@dataclass(frozen=True)
class SimulationRequest:
    simulation_id: str
    base_commit: str
    mutations: List[ProposedMutation]
    horizon: str = "release"      # "node" | "document" | "release" | "workspace"
    include_repair_plan: bool = True
    policy_digest: Optional[str] = None   # None: use the policy in force


@dataclass(frozen=True)
class SimulationReport:
    simulation_id: str
    base_commit: str
    request_digest: str
    report_digest: str

    semantic_delta: List[Dict[str, Any]]      # per SEMANTIC_DIFF §1
    becomes_false: List[Dict[str, Any]]       # states a source now contradicts
    becomes_stale: List[Dict[str, Any]]       # proofs voided, with edge policy
    must_be_reproved: List[Dict[str, Any]]    # obligations raised, per PROOF_OBLIGATIONS
    outputs_changed: List[Dict[str, Any]]     # release targets and rendered fragments
    decisions_expiring: List[Dict[str, Any]]  # decisions and waivers whose bound state moves
    conflicts_created: List[Dict[str, Any]]   # SemanticConflict, per MERGE_PROTOCOL §4.1
    authority_required: List[Dict[str, Any]]  # grants needed that are not held

    provably_unaffected: Dict[str, Any] = field(default_factory=dict)
    repair_plan: Optional[Dict[str, Any]] = None
    gate_consequence: Dict[str, Any] = field(default_factory=dict)

    committed: bool = False       # always False. There is no code path that sets it True.
```

**`becomes_false` and `becomes_stale` are separate fields and they are not interchangeable.**

`becomes_stale` means *the check that was run no longer applies to what would be there.* The claim may be perfectly supported; nobody would have looked since it moved. Repair is a button.

`becomes_false` means *a source in this workspace would then contradict this state.* Repair is a rewrite, a retraction or a source.

Collapsing them is the failure [`../v5/STALENESS.md`](../v5/STALENESS.md) §6 names about `stale` and `needs_source`: they demand different work, and an author triaging forty findings where the cheap ones are indistinguishable from the expensive ones will treat all forty as expensive and do none of them.

**`committed` is always `False`.** It is present in the record so that no reader has to infer it from the absence of a commit id, and it exists as a field so that any future surface that tried to promote a simulation into a state would have to write a value the type system already answers.

---

## 4. A worked transcript

**Status: executable in `scripts/wi.py`.**

A workforce program's success threshold is a registered definition. It has been 0.90 — a participant cohort is "successful" when at least 90% reach placement — since the program's founding. The board is considering raising it to 0.95.

The definition is used in a 1,660-page policy book, a public website, the Q3 board deck and a policy brief filed with a state agency.

```
$ python3 scripts/wi.py simulate \
      --set def-0007.threshold=0.95 \
      --horizon release

SIMULATION  sim-0044   base wc-0212   ephemeral branch created and dropped

  proposed   meaning.definition  def-0007  "program success threshold"
             threshold  0.90 → 0.95
             33 nodes bind this definition through `uses_term`

  ─────────────────────────────────────────────────────────────────────────
  SEMANTIC DELTA

    definition_changed        def-0007      [verified · deterministic]
      threshold  0.90 → 0.95
      A registered term's binding moves. Every node using the term inherits
      a changed meaning without any of their own text changing.

  ─────────────────────────────────────────────────────────────────────────
  BECOMES FALSE                                                          4

    c-0311   "Cohort 2021-B met the program success threshold."
             measured 0.923 · true at 0.90 · false at 0.95
             renders in  ch-07 ¶4 · web/outcomes.html · deck slide-09
             anchor a-0402 outcomes_2021.csv@v2 rows 14-21 still resolves;
             the anchor supports the RATE, and the rate no longer clears
             the threshold. The claim is refuted by evidence it cites.

    c-0318   "Cohort 2022-A met the program success threshold."
             measured 0.941 · true at 0.90 · false at 0.95

    c-0344   "Every cohort since 2019 has met the threshold."
             universal quantifier · refuted by c-0311 and c-0318

    c-0501   "The program has never missed its success threshold."
             negation of a universal · same two counterexamples

  ─────────────────────────────────────────────────────────────────────────
  BECOMES STALE                                                         27

    numeric checks           19   every claim comparing a rate to def-0007
    definition binding       33   `uses_term` sites, per STALENESS §3
                                  (6 of the 33 are already in BECOMES FALSE
                                   and are not counted twice below)
    citation resolution       2   two footnotes cite the threshold by value
    derived summaries         6   chapter abstracts stating the threshold

  ─────────────────────────────────────────────────────────────────────────
  MUST BE RE-PROVED                                                     31

    numeric.value            19   recompute each rate against 0.95
    definition.binding       33 → 27 outstanding after the 6 refuted above
    citation.resolution       2   both footnotes quote "90 percent" verbatim
                                  and would become misquotations
    obligation.exception      1   ob-0022 grants a waiver "where the cohort
                                  falls below threshold by less than 2
                                  points" — the carve-out was written
                                  against 0.90 and its arithmetic moves

  ─────────────────────────────────────────────────────────────────────────
  OUTPUTS CHANGED                                                        4

    dist/policy_book.pdf         11 fragments · ch-07, ch-09, ch-14, app-C
    web/outcomes.html             3 fragments · hero figure, table, footnote
    dist/board_deck_q3.pdf        2 fragments · slide-09, slide-17
    filings/policy_brief_2026.pdf 1 fragment  · §2 ¶3

  ─────────────────────────────────────────────────────────────────────────
  DECISIONS EXPIRING                                                     3

    d-0104   accepted  c-0311 phrasing        a.rivera   2025-11-02
             bound to a state that would move · re-take or carry forward
    d-0140   accepted  slide-09 figure        board      2026-02-14
             bound to a state that would move · this was a BOARD approval
    w-0009   waiver    c-0344 "every cohort"  m.chen     2026-01-30
             waiver binds to a claim state. The claim would become false,
             not merely unsupported. A waiver cannot cover a refuted claim.

  ─────────────────────────────────────────────────────────────────────────
  AUTHORITY REQUIRED                                                     1

    filings/policy_brief_2026.pdf was filed under an agency submission.
    Amending a filed document requires `filing_amendment` authority.
    Held by: none of the actors on this workspace.

  ─────────────────────────────────────────────────────────────────────────
  PROVABLY UNAFFECTED

    1,802  claim atoms      no dependency path from def-0007 to these nodes
    1,794  anchors          no anchor resolves through the definition
       38  chapters         ch-01..ch-06, ch-10..ch-13, ch-15..ch-38
        7  release targets  dist/annual_report.pdf, dist/methods.pdf,
                            web/about.html, web/programs.html,
                            dist/staff_handbook.pdf, feeds/rss.xml,
                            dist/archive_2019.pdf
      412  canon nodes      n/a — no fictional realm in this workspace

    basis: reverse-closure traversal from def-0007 over `uses_term`,
           `depends_on`, `derived_from`, `renders_as` and `built_from`;
           these nodes were not reached. Traversal visited 1,204 edges.

  ─────────────────────────────────────────────────────────────────────────
  GATE CONSEQUENCE   under `strict`

    BLOCK   4 refuted claims · 1 waiver covering a refuted claim
            (HOLD would be the verdict if only staleness were at issue;
             a refuted claim is not clearable by re-running a check)

  ─────────────────────────────────────────────────────────────────────────

  Nothing was committed. Branch sim-0044 dropped. Workspace at wc-0212.

Checks run: definition binding traversal · numeric recomputation against the
proposed threshold · citation verbatim comparison · universal-quantifier
refutation · decision state binding · waiver state binding · authority lookup.
Not run: paraphrase equivalence for 6 derived summaries (no judgment provider
on this surface; all 6 are reported as stale, none as unaffected).
```

Four things in that transcript are worth naming.

**`c-0344` and `c-0501` were found by refutation, not by search.** Neither sentence contains the number 0.90, and neither would appear in a text search for the threshold. They are universal claims over a set whose membership changes, and they are refuted by two specific counterexamples the simulation names. A human reading the book would have to hold the whole outcomes table in their head to notice.

**`ob-0022` is the finding that would have been missed.** A carve-out written as *"below threshold by less than 2 points"* is arithmetic anchored to a threshold value. It is not a claim, it does not contain a rate, and it survives every check that looks at claims. It is caught because an obligation's exceptions are a registered dimension and the exception's scope is bound to `def-0007`.

**`d-0140` is a board approval.** A decision record bound to a state that would move is not merely stale bookkeeping — it means a slide the board approved would say something different, and Law J's whole purpose is that "approved" names *what* was approved. The simulation surfaces it as a scheduling problem before somebody discovers it the week of the meeting.

**The authority row is the one that changes the plan rather than the text.** The policy brief was filed. Amending a filed document is not an editing operation, and no repair action in the plan can produce that authority. Section 7 is why this row sorts above everything else.

---

## 5. The provably unaffected block

**Status: executable in `scripts/wi.py`.**

The unaffected block is printed with equal prominence, on every simulation, with its basis. It is not reassurance and it is not a footer.

Three reasons, the same three that govern the impact report in [`../v5/STALENESS.md`](../v5/STALENESS.md) §4.1, and one more that is specific to simulation.

**It is the only way to distinguish a thorough analysis from a shallow one.** A report listing thirty-one problems and no denominator is unfalsifiable. "1,802 claim atoms unaffected, basis: not reached by a traversal that visited 1,204 edges" is a `measured` statement under [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md), and a reader can ask for the traversal.

**It makes the decision tractable.** The board is not deciding whether to raise a threshold in the abstract. They are deciding whether to accept a bounded, enumerated cost — eleven fragments in one book, four claims, one filing amendment — against thirty-eight chapters and seven release targets that do not move. Without the second half they are deciding in the dark and will either refuse a good change or approve it without understanding it.

**Naming what does not change is what keeps the tool switched on.** A system that reports only damage teaches one lesson quickly: every question produces a wall of red, the wall is mostly irrelevant, reading it is a waste of time. The rational response is to stop reading it, and the first thing lost is the finding that mattered.

**And the reason specific to simulation:** a counterfactual that only enumerates harm is an argument against changing anything. That is not a neutral tool. A system whose output is structurally biased toward the status quo will be used to justify inaction, and it will be right often enough to be trusted and wrong exactly when a change was overdue. The unaffected block is what makes the report a description rather than a recommendation.

**The word `provably` is doing work.** A node appears in this block only when the traversal did not reach it — a graph-theoretic fact about recorded edges, not an assessment. A node whose analysis was skipped, whose escalation went unresolved, or whose adapter is unavailable on this surface **does not appear here**. It appears under `becomes_stale` with the reason, as the six derived summaries do in section 4. Law E governs this block as it governs everything else: an unavailable analysis does not become a clean bill of health.

---

## 6. Repair planning as constrained optimization

**Status: executable in `scripts/wi.py` for plan enumeration and ordering; model-proposed candidate actions specified.**

A simulation that names damage without naming the repair has done half the work. The plan is the other half, and it is an optimization problem with a hard constraint set.

```python
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class RepairAction:
    """One typed operation. The vocabulary extends STALENESS §5."""
    action: str          # "rerun_check" | "replace_anchor" | "attach_source"
                         # | "qualify_claim" | "restore_hedge" | "remove_claim"
                         # | "resolve_conflict" | "accept_proposal" | "renew_waiver"
                         # | "update_term" | "rebuild_target" | "request_authority"
                         # | "retake_decision" | "amend_filing"
    targets: List[str]                 # logical ids or artifact paths
    cost: "CostVector"
    preconditions: List[str]           # action ids that must complete first
    produced_by: str = "engine"        # "engine" | "operator" | "model_proposed"
    rationale: str = ""


@dataclass(frozen=True)
class CostVector:
    """Seven incommensurable components. Compared lexicographically, never summed.

    Component 0 is a feasibility gate, not a cost: 0 means the action is
    permitted under policy and law, 1 means it is not available at any price.
    """
    infeasible: int          # 0 permitted · 1 forbidden by policy or law
    proof_gap: int           # obligations that would remain unmet after this action
    authority_escalation: int  # grants required that are not currently held
    human_reviews: int       # decisions a named person must take
    recomputations: int      # deterministic checks to re-run
    judgments: int           # external judgment calls required
    rendering_churn: int     # release fragments that must be re-rendered

    def key(self) -> Tuple[int, ...]:
        return (self.infeasible, self.proof_gap, self.authority_escalation,
                self.human_reviews, self.recomputations, self.judgments,
                self.rendering_churn)


def cheapest_safe_plan(candidate_plans: List[List[RepairAction]]) -> List[RepairAction]:
    """Lexicographic minimum over summed component vectors.

    There is no weighting configuration, because the ordering is not a
    preference. A plan that leaves a proof gap is not 'more expensive' than
    one that does not; it is a different kind of thing.
    """
    def plan_key(plan: List[RepairAction]) -> Tuple[int, ...]:
        totals = [0] * 7
        for a in plan:
            for i, v in enumerate(a.cost.key()):
                totals[i] += v
        return tuple(totals)

    feasible = [p for p in candidate_plans if plan_key(p)[0] == 0]
    if not feasible:
        # Every candidate is forbidden. This is a real answer and it is
        # reported as one, never as the least-forbidden option.
        return []
    return min(feasible, key=plan_key)
```

The plan for the worked case:

```
  MINIMUM SAFE REPAIR FRONTIER                      7 actions · 4 human decisions

  1  request_authority   filing_amendment for filings/policy_brief_2026.pdf
                         authority · 1 escalation · blocks actions 6 and 7

  2  update_term         def-0007 threshold 0.90 → 0.95
                         33 use sites rebind · 0 human decisions

  3  qualify_claim       c-0311, c-0318
                         "met the threshold in force at the time" — both
                         claims become true again under a temporal
                         qualification the anchors already support
                         2 human decisions · author writes 2 sentences

  4  retake_decision     d-0140  board approval of slide-09
                         1 human decision · board, not an editor

  5  renew_waiver        w-0009 does not renew — c-0344 becomes false, and a
                         waiver may not cover a refuted claim. Action is
                         remove_claim or qualify_claim, not renewal.
                         1 human decision

  6  rerun_check         19 numeric checks against the new binding
                         0 human decisions · deterministic

  7  rebuild_target      policy_book, outcomes.html, board_deck_q3,
                         policy_brief_2026
                         0 human decisions · 17 fragments

  proof gap after plan   0
  authority escalations  1   (action 1; nothing in this plan can produce it)
  human decisions        4
  recomputations        19
  judgments              0
  rendering churn       17

  Alternative plan rejected:
    remove_claim c-0311, c-0318, c-0344, c-0501
      infeasible 0 · proof_gap 0 · authority 1 · human 4 · recompute 19 ·
      judgments 0 · churn 21
      Rejected at component 6: identical through five components, higher
      rendering churn. Retained in the report because "make the claim
      smaller" is sometimes the right answer and the operator should see it.
```

**Action 3 is the reason the planner exists.** The obvious repair is to delete two claims. The cheaper and more honest repair is a temporal qualification that both existing anchors already support — the cohorts *did* meet the threshold that was in force. A planner ordered by "fewest edits" would have proposed deletion. A planner ordered by proof completeness first finds that both plans close the gap and separates them on a later component.

**Action 5 is a refusal.** The plan does not offer to renew a waiver over a claim that would be refuted, and it says why rather than omitting the option. A waiver is a person choosing to proceed past a hold on a claim nobody has checked; it is not a mechanism for proceeding past a claim a source in the workspace contradicts.

**`produced_by` distinguishes three origins.** `engine` actions are enumerated deterministically from the damage set — every `becomes_stale` numeric check yields a `rerun_check`, every changed target yields a `rebuild_target`. `operator` actions are ones a human added. `model_proposed` marks a candidate action a judgment provider suggested, such as the specific wording of a qualification in action 3.

**Model-proposed candidate actions are specified and do not run.** A provider may propose *that* a qualification exists and *what it might say*; it may never cost the action, order the plan, or mark it complete. The costing and the ordering are deterministic, because a planner whose ordering could be argued into is a planner that will be argued into.

---

## 7. The lexicographic safety ordering

**Status: executable in `scripts/wi.py`.**

Plans are compared component by component, in this order. A difference at any component decides the comparison and later components are not consulted.

| # | Component | Question | Why it sorts here |
|---|---|---|---|
| 0 | **Legal and policy feasibility** | Is this action permitted at all? | An action forbidden by policy or law is not expensive, it is unavailable. It is a gate, and it is component zero so that no amount of saving anywhere else can purchase it. |
| 1 | **Proof completeness** | Would any obligation remain unmet? | A plan that leaves the document unprovable has not repaired it. Every subsequent component is a question about how to close the gap; a plan that does not close it is answering a different question. |
| 2 | **Authority escalation** | Does this require a grant nobody holds? | Escalation is not a cost paid in effort. It is a dependency on a person outside the loop, on their calendar, sometimes on an external body. A plan needing one escalation is categorically different from one needing none. |
| 3 | **Human review** | How many decisions must a named person take? | Human attention is the scarcest input and the only one that cannot be parallelized or bought. Every decision is also a place the process can stop for a week. |
| 4 | **Recomputation** | How many deterministic checks re-run? | Cheap, fast, no human, no provider. Deliberately below human review: a plan that trades 200 recomputations for one fewer decision is the better plan, and a weighted sum would usually say the opposite. |
| 5 | **External judgment** | How many provider calls? | Costs money, latency and a dependency, and produces a `judged` record a reader may disagree with. Below recomputation because it is strictly worse than a deterministic check of the same thing. |
| 6 | **Rendering churn** | How many fragments re-render? | Machine work at the end of the pipeline. It is last because it is the only component with no epistemic consequence at all. |

**Why 0 and 1 are separated.** Both look like gates. They are not the same gate. Component 0 says *you may not do this*; component 1 says *you may do this and it will not finish the job*. A plan that is infeasible is discarded. A plan that leaves a proof gap is retained, reported, and sorted below every plan that closes one — because sometimes every available plan leaves a gap, and the operator needs to see the smallest one rather than an empty report.

**Why 3 sits above 4 and 5.** This is the ordering that produces counter-intuitive plans, and it is right. Consider two plans for the worked case: one re-runs 19 checks and asks for 4 decisions; another asks for 6 decisions and re-runs 3. A weighted sum with almost any plausible weights prefers the second, because 16 saved recomputations look like a lot. In practice the second plan takes three weeks, because two of those extra decisions belong to people who are travelling. Recomputation is seconds. Human decisions are calendars.

**Why 5 sits below 4.** A judgment and a recomputation may answer the same question — *does this paraphrase preserve the claim?* — with the recomputation available only when the dimensions are registered. Where both are available, the deterministic one produces a `verified` record a stranger can reproduce and the judged one produces a record a stranger is entitled to disagree with. Every plan that prefers the first is permanently cheaper in a way that does not show up in latency.

---

## 8. Why a single blended cost score is forbidden

**Status: executable in `scripts/wi.py`.**

The obvious design is a weighted sum:

```python
# This is the design this document exists to refuse.
score = (10 * infeasible + 8 * proof_gap + 6 * authority
         + 4 * human_reviews + 1 * recomputations
         + 3 * judgments + 0.5 * rendering_churn)
```

It is compact, it sorts cleanly, it is easy to explain, and it is wrong in four separate ways.

**The components have no common unit.** `infeasible` is a boolean about permission. `human_reviews` is a count of people's decisions. `rendering_churn` is a count of machine operations. Adding them requires an exchange rate between *a thing you may not do* and *a page that must re-render*, and no such rate exists. Any number chosen for `10` is asserting one, and asserting it invisibly.

**Every weighting is purchasable.** With `infeasible` at weight 10 and `rendering_churn` at 0.5, twenty-one saved fragments outweigh one forbidden action. That is not a hypothetical: the rejected alternative plan in section 6 differs from the chosen one by exactly four fragments of churn. Under a blended score, a plan that requires an action policy forbids beats a permitted plan often enough to matter, and the output looks like arithmetic rather than like a violation. **A constraint that can be outvoted is not a constraint.**

**The number cannot be inverted.** Handed a plan scoring 47, nobody — including the person who computed it — can recover whether it needs one forbidden action or ninety-four re-renders. That is precisely the composite-score failure [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) names for reliability, applied to cost: a single dial hiding several unlike things, and once they are on the dial they average.

**It hides the disagreement people should be having.** Two organizations weigh `attach_source` differently — a two-minute download for a solo author, a procurement request and a two-week wait for a regulated filing, as [`../v5/STALENESS.md`](../v5/STALENESS.md) §5 states. Under a lexicographic ordering that difference is expressible in the ordering itself and visible to anyone reading the plan. Under a weighted sum it disappears into a constant somebody set once, and every plan afterward silently inherits an assumption nobody remembers making.

**What is configurable and what is not.** The seven components are fixed and their order is fixed. What an operator may configure is the *unit cost of individual actions within a component* — how many human decisions `attach_source` implies in this organization, whether `renew_waiver` requires one authorized actor or two. That is local knowledge and the system should not pretend it knows it. The ordering is not local knowledge; it is the safety property, and a safety property with a tuning knob is a preference.

Every plan prints the seven totals separately, and prints the component at which the runner-up was rejected. That is what makes "cheapest safe" a checkable statement rather than a claim.

---

## 9. What a simulation cannot tell you

**Status: executable in `scripts/wi.py`.**

Stated plainly, because a counterfactual engine is the component most likely to be mistaken for an oracle.

**It cannot tell you whether the change is right.** Raising a threshold from 0.90 to 0.95 is a program decision about what the organization should hold itself to. The simulation costs it. It has no view on it, and any report that read as advice would be a tool substituting its arithmetic for somebody's judgment.

**It cannot see dependencies nobody recorded.** This is the same limit [`../v5/STALENESS.md`](../v5/STALENESS.md) §1 names: a dependency that was never recorded cannot be traversed. A threshold quoted in an email to a funder, in a slide somebody made outside the workspace, or in a verbal commitment at a board meeting is invisible here, and the `provably_unaffected` block does not cover it — it covers nodes in this graph.

**It cannot predict how a reader will react.** `becomes_false` is a statement about a contradiction between a claim and an anchor in the workspace. It is not a statement about whether the resulting document is persuasive, defensible in argument, or good.

**It cannot resolve an escalation it has no provider for.** The six derived summaries in section 4 are reported stale rather than analyzed, because paraphrase equivalence needs a judgment tier. Under Law E they do not become unaffected, and the report says which analysis did not run.

**It cannot promise the cost is complete.** The plan enumerates repairs for damage the traversal found. A repair may itself have consequences — action 3 writes two new sentences, and those sentences are new claim atoms with their own obligations. `wi simulate` may be run on a plan, and the transitive case terminates because each round's mutations are strictly smaller, but the report describes one round unless asked for more.

---

## 10. Benchmarks

**Status: specified.** The generator and the assertion harness are defined here; the shipped suite covers the deterministic damage classes and the plan-ordering assertions.

Simulation is scored on **exact set equality against a known-damage graph**, not on counts.

| Generated case | Asserts |
|---|---|
| Definition change with 900 use sites | Exactly 900 in `becomes_stale`; the 12 sites using an approved alias are included; zero in `provably_unaffected` |
| Threshold change refuting 2 of 40 measured claims | Exactly 2 in `becomes_false`; the other 38 recompute and remain true |
| Universal claim over a set whose membership moves | The universal appears in `becomes_false` with its counterexamples named |
| Obligation with an exception whose arithmetic is bound to a changed value | The exception appears in `must_be_reproved`; the obligation is not silently unchanged |
| Waiver bound to a claim that becomes false | `renew_waiver` is **absent** from every candidate plan |
| Filed artifact with no held amendment authority | Every plan touching it carries `authority_escalation ≥ 1`; no plan reports `infeasible 0` by omitting the action |
| Two plans differing only in component 6 | The lower-churn plan wins; the runner-up is reported with its rejection component |
| Two plans where one trades 200 recomputations for 1 decision | The 200-recomputation plan wins |
| Every candidate plan infeasible | Empty plan returned; report says so; no least-forbidden option is emitted |
| Simulation run twice on the same state | Byte-identical `report_digest` |
| Simulation on a 400,000-node graph, one definition mutated | Frontier exact; walk index-driven; workspace state digest unchanged before and after |

**The assertion checked on every case, and the one that matters most:** *the workspace state digest before the simulation equals the state digest after it.* A simulation that mutates the workspace it was asked to reason about has done the one thing it exists not to do, and it will do it quietly — the report will still look right.

The asymmetry from [`../v5/STALENESS.md`](../v5/STALENESS.md) §8 applies unchanged. A false positive here is a plan that repairs something that was fine. A false negative is a change made on the strength of a report that said it was safe, and nobody finds out until a reviewer does.

---

## 11. What is executable and what is specified

| Mechanism | Status |
|---|---|
| `wi simulate`, ephemeral branch creation and drop | Executable in `scripts/wi.py` |
| `SimulationRequest`, `SimulationReport`, deterministic `report_digest` | Executable in `scripts/wi.py` |
| `becomes_false` by refutation against bound anchors | Executable in `scripts/wi.py` |
| `becomes_stale` reusing the v5 invalidation walk and edge policy | Executable in `scripts/wi.py` |
| `decisions_expiring` and `authority_required` | Executable in `scripts/wi.py` |
| `provably_unaffected` with traversal basis and edge count | Executable in `scripts/wi.py` |
| `RepairAction`, `CostVector`, lexicographic plan ordering | Executable in `scripts/wi.py` |
| Runner-up plan reporting with its rejection component | Executable in `scripts/wi.py` |
| Gate consequence projection under the policy in force | Executable in `scripts/wi.py` |
| Model-proposed candidate repair actions | Specified — see [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) |
| Paraphrase-equivalence analysis of derived summaries | Specified |
| Transitive simulation of a plan's own consequences beyond one round | Specified |
| Generated-topology simulation benchmark harness | Specified |

---

## Related documents

- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — merging is a simulable mutation; conflicts appear in `conflicts_created`
- [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) — what `must_be_reproved` enumerates, and where obligations come from
- [`ARGUMENT_GRAPH.md`](ARGUMENT_GRAPH.md) — simulating the removal of a premise
- [`COMPILER_MODEL.md`](COMPILER_MODEL.md) — how `outputs_changed` becomes an incremental rebuild
- [`../v5/STALENESS.md`](../v5/STALENESS.md) — the invalidation walk this reuses, and the repair operation vocabulary
- [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) — the delta classes in `semantic_delta`
- [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) — why the cost vector does not collapse
- [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — Law E, Law I, Law J and Law K
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
