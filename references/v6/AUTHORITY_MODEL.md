# The Authority Model

Who may change what, over which part of the work, for how long, and under what conditions.

Created by **[Antonio T. Smith Jr.](https://densitysix.com)** — Founder & CEO, Density6 LLC.

Law O of the v6 constitution states that authority is explicit, scoped and expiring. This document is the mechanism. It defines actors, capability grants, scope, delegation, quorum and the one property that separates this model from every access-control list in the field: **authorization is transition-aware.** You do not authorize a person to touch a paragraph. You authorize a person to make a particular kind of semantic change to a particular part of the work.

Read this with [`SEMANTIC_IR.md`](SEMANTIC_IR.md) for what a semantic change is, and with [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) for how grants are enforced at the boundary.

---

## Contents

1. [Actor kinds are descriptive](#1-actor-kinds-are-descriptive)
2. [The capability grant](#2-the-capability-grant)
3. [The capability vocabulary](#3-the-capability-vocabulary)
4. [Scope](#4-scope)
5. [Authorization is transition-aware](#5-authorization-is-transition-aware)
6. [Delegation monotonicity](#6-delegation-monotonicity)
7. [Quorum and approval rules](#7-quorum-and-approval-rules)
8. [Revocation and expiry](#8-revocation-and-expiry)
9. [The command surface](#9-the-command-surface)

---

## 1. Actor kinds are descriptive

**Status: specified.** Grant issue, delegation, revocation and checking are executable through `wi authority`.

An actor kind says what something is. It does not say what it may do.

| Actor kind | What it describes | What it authorizes |
|---|---|---|
| `human` | A person acting for themselves | Nothing |
| `team_member` | A person acting within an organization | Nothing |
| `authorized_editor` | A person in an editing role | Nothing |
| `automated_policy` | A deterministic rule set | Nothing |
| `deterministic_engine` | A reproducible computation | Nothing |
| `judgment_provider` | A model or service that produces an opinion | Nothing, and by constitutional constraint it cannot be granted `*.accept`, `*.approve`, `canon.modify`, `proof.waive` or `authority.delegate` |
| `external_import` | Content arriving from another workspace | Nothing |
| `autonomous_agent` | A bounded process acting on a schedule or trigger | Nothing |
| `remote_workspace` | A federated peer | Nothing |

Every row in the third column reads *nothing*. That is the point, and it is worth stating flatly because the alternative is what almost every system does: the role is the permission.

**A human with no grant cannot commit.** Being a person is not a capability. The founder of the organization, opening the workspace on their own machine, holds exactly the authority their grants describe and no more. If that set is empty, `wi commit` refuses with `WI_AUTHORITY_ABSENT` and names the capability that was missing.

**Why roles-as-permissions fails.** A role is a summary of an intention, and summaries drift from intentions the moment the organization changes shape. Somebody joins as an editor to fix wording and inherits the ability to change a funding figure, because both are "editing." Somebody leaves the legal team and keeps `legal_reviewer` for eight months because nobody remembers that removing a title is also removing a permission. The failure is not that the wrong person acted — it is that nothing in the system was ever a statement of what they were permitted to do, so nothing could be checked, and the audit reconstructs an intention from a job title.

A grant is a statement. It names a capability, a scope, an interval and conditions, and every one of those is checkable at the moment of the transition rather than inferred afterwards.

**The judgment provider denial is constitutional, not configurable.** It is not a default that an administrator may change; it is a constraint the constraint engine enforces on the grant graph itself. Issuing such a grant fails at issue time:

```
$ wi authority issue --capability claim.accept \
                     --subject act-0031 \
                     --scope structure_subtree:structure.chapter:ch-02

WI_AUTHORITY_EXCEEDED
  Subject act-0031 has actor_kind 'judgment_provider'.
  Capability 'claim.accept' is denied to that kind by constitutional
  constraint C007. The denial is not waivable by any grant.

  A judgment provider may hold: claim.propose, source.ingest.
  Repair: issue claim.propose, and route acceptance to a human grant holder.
```

**Why the denial is absolute.** A model that can accept its own proposal has closed the loop, and every guarantee in this system rests on that loop staying open. The distinction between a proposal and a state is the distinction between something a person decided and something that happened. Once a provider can decide, the graph records decisions nobody made, and the proof closure — which exists to let a reader verify a release without trusting the model — is verifying a chain the model authored end to end.

---

## 2. The capability grant

**Status: specified.** Issue and inspection are executable through `wi authority`.

```json
{
  "node_type": "authority.grant",
  "logical_id": "0193a7c2-11b4-7d3e-8f02-6a1c4e9b0d55",
  "state_digest": "sha256:2b91f0ac47d3e5860c1b9a4f7e206d38ca5f1904b7e2c8d0f3a6b9c1d4e7f205",

  "capability": "claim.accept.quantity_change",

  "subject": {"actor_id": "act-0007", "actor_kind": "team_member"},
  "issuer":  {"actor_id": "act-0001", "actor_kind": "human"},
  "issued_at": "2027-03-01T09:00:00Z",

  "scope": {
    "kind": "structure_subtree",
    "root": "structure.chapter:ch-02",
    "realms": ["external_fact"],
    "branch": "main"
  },

  "transition": {
    "axes_permitted": ["quantity"],
    "axes_denied": ["scope", "modality", "causality", "legal_force"],
    "max_magnitude_delta_bps": 500
  },

  "not_before": "2027-03-01T00:00:00Z",
  "not_after":  "2027-06-01T00:00:00Z",

  "conditions": [
    {"kind": "requires_no_open_conflicts", "value": true},
    {"kind": "requires_evidence_reliability", "value": "verified"},
    {"kind": "requires_second_approver_role", "value": "finance_reviewer"}
  ],

  "delegable": false,
  "parent_grant": null,
  "revoked_at": null,
  "revocation_basis": null
}
```

| Field | What it decides | What happens if it is absent |
|---|---|---|
| `capability` | Which verb | Nothing is authorized. A grant with no capability is not a grant. |
| `subject` | Who holds it | Unassignable. |
| `issuer` | Who is accountable for it | The grant cannot be audited backward, so it is rejected at issue. |
| `scope` | Which part of the work | Rejected. An unscoped grant is a workspace-wide grant, and if that is intended it must be stated as `kind: "workspace"` rather than implied by omission. |
| `transition` | Which semantic axes may move | Defaults to the capability's own axis set. See section 5. |
| `not_before` / `not_after` | The lifetime | `not_after: null` is permitted only for `kind: "workspace"` grants held by `human` actors, and is reported by `wi authority` on every listing. Everything else expires. |
| `conditions` | What must hold at use time | An unconditional grant. Legal, and the condition list is the difference between "may change a figure" and "may change a figure when the evidence is verified and finance has signed." |
| `delegable` | Whether it can be passed on | Defaults false. Delegability is granted, never assumed. |
| `parent_grant` | What it was derived from | Null means a root grant. Non-null means monotonicity is checked. See section 6. |
| `revoked_at` | Whether it still exists | Null means live. Revocation is a stamp, never a deletion. |

**Why expiry is the default rather than the exception.** Permission granted for a project outlives the project. Nobody revokes it, because revoking permissions is work with no visible reward and it is never anybody's task. An expiring grant inverts the default: the effort is required to *keep* authority, which is the direction that matches how organizations actually behave. The grant that mattered gets renewed by somebody who noticed it lapse; the grant that did not simply ends.

---

## 3. The capability vocabulary

**Status: specified.**

Sixteen capabilities. The vocabulary is closed — a capability outside this list cannot be granted, because a capability nothing checks is a string in a database.

| Capability | Permits | Why it is separate from its neighbour |
|---|---|---|
| `source.ingest` | Bringing external material into the workspace | Ingesting a source is not asserting anything from it. The two are separated so a research assistant can gather without being able to claim. |
| `claim.propose` | Creating a proposal against a target state | A proposal is not a state. This is the widest capability in the set and the only one a judgment provider may hold. |
| `claim.accept` | Turning a proposal into authoritative state | The decision. Everything the constitution protects turns on this being distinct from `claim.propose`. |
| `claim.accept.wording_only` | Accepting a change whose semantic delta is empty | A copy editor needs this and needs nothing else. Without the split, fixing a typo requires the authority to change a figure. |
| `claim.accept.quantity_change` | Accepting a change to a quantity | The most consequential single-axis change and the one most often reviewed by a different person from the one who reviews prose. |
| `concept.define` | Creating or changing a `meaning.definition` or `meaning.term` | A definition change invalidates every claim that used the term. Its blast radius is unrelated to its size, so it is authorized separately. |
| `obligation.create` | Adding a `meaning.obligation` | Creating a duty binds the organization. It is not editing. |
| `canon.modify` | Changing established fictional or organizational canon | Canon is the thing everything else is consistent with. Changing it is not the same act as adding to it. |
| `proof.waive` | Releasing with an unmet obligation, on a recorded basis | The most dangerous capability in the system. It is separate so it can be granted to almost nobody and audited exhaustively. |
| `release.build` | Compiling a release candidate | Building is mechanical and produces nothing authoritative. |
| `release.approve` | Declaring a candidate fit to publish | The judgment. Separate from building so the person who ran the command is not automatically the person who vouched for the result. |
| `release.sign` | Attaching a cryptographic signature | Separate from approval so that a compromised signing key does not imply a compromised approval, and an approval by someone without the key is still a recorded approval. |
| `policy.modify` | Changing the rules the gates enforce | Changing the gate is not passing it. Held apart so that nobody can respond to a failing check by editing the check. |
| `authority.delegate` | Issuing a derived grant | Delegation is its own act, and holding a capability does not imply the right to hand it on. |
| `capsule.export.full` | Exporting a proof capsule with full disclosure | Export is disclosure. It is a distinct decision from anything to do with authoring. |
| `capsule.export.redacted` | Exporting with selective disclosure | Narrower than full export and far more commonly granted. Splitting them means the common case does not require the dangerous one. |

**Why sixteen and not four.** Every split above exists because two acts that look similar have different consequences and are, in practice, reviewed by different people. The test for adding a seventeenth is not whether it names something real — it is whether any organization would grant one of the pair and withhold the other. If nobody would ever split them, they are one capability.

---

## 4. Scope

**Status: specified.**

A grant without a scope is a grant over everything. Scope variants:

| Variant | Shape | What it selects |
|---|---|---|
| `workspace` | `{"kind": "workspace"}` | Everything. Reported in every listing precisely because it is the widest thing anybody can hold. |
| `branch` | `{"kind": "branch", "branch": "release/2027-q2"}` | One branch. The common shape for a release-window grant. |
| `structure_subtree` | `{"kind": "structure_subtree", "root": "structure.chapter:ch-02"}` | A part of the document tree and everything under it. |
| `node_set` | `{"kind": "node_set", "nodes": ["meaning.claim_atom:...", "..."]}` | An enumerated list. Narrow, explicit, and the right shape for a one-off correction. |
| `realm` | `{"kind": "realm", "realms": ["fictional_canon"]}` | All nodes in a realm. Lets a continuity editor hold canon authority without holding authority over external facts. |
| `node_type` | `{"kind": "node_type", "types": ["meaning.forecast"]}` | All nodes of a type, wherever they sit. |
| `intersection` | `{"kind": "intersection", "of": [ ... ]}` | Every member scope must admit the node. |

Scopes compose by intersection only. There is no union.

**Why no union.** A union of two scopes is wider than either, and every mistake in scope composition should make a grant narrower rather than wider. Somebody who needs authority over two disjoint areas holds two grants, which is one line longer in the listing and impossible to misread. A union operator would let a scope expression grow permissions through a nesting error, and nesting errors are found by the person who exploits them.

```python
def in_scope(scope: dict, node: dict, graph) -> bool:
    kind = scope["kind"]
    if kind == "workspace":
        return True
    if kind == "branch":
        return node["branch"] == scope["branch"]
    if kind == "structure_subtree":
        return scope["root"] in graph.ancestors_of(node["logical_id"])
    if kind == "node_set":
        return node["logical_id"] in scope["nodes"]
    if kind == "realm":
        return node["realm"] in scope["realms"]
    if kind == "node_type":
        return node["node_type"] in scope["types"]
    if kind == "intersection":
        return all(in_scope(s, node, graph) for s in scope["of"])
    raise UnknownScopeKind(kind)      # never a permissive default
```

The final line matters. An unrecognized scope kind raises rather than returning `True` or `False`. Returning `True` grants authority the workspace could not describe; returning `False` silently disables a grant somebody is relying on and produces a refusal nobody can explain. Raising says the grant is not interpretable by this version and stops.

**Realm scoping interacts with proof.** A grant scoped to `fictional_canon` cannot authorize a change to an `external_fact` node even inside the same chapter, so a continuity editor working through a manuscript passes over the two paragraphs that cite a real statistic. That is the intended behaviour and it is invisible without realm scoping.

---

## 5. Authorization is transition-aware

**Status: specified.**

This is the property that distinguishes the model. You do not authorize an endpoint. You authorize a **semantic delta**.

Two edits, both landing in the same paragraph of chapter two, both a handful of characters:

> **Edit 1.** "Program X may reduce wait time by 38%" → "Program X reduces wait time by 38%"
>
> **Edit 2.** "the colour of the intake form" → "the color of the intake form"

A file-scoped permission model sees one thing: somebody modified `chapter-02.md`. Both edits are permitted or both are refused. Under a transition-aware model:

| | Edit 1 | Edit 2 |
|---|---|---|
| Semantic delta | `modality: possibility → assertion` | none |
| Axes touched | `modality`, and consequentially `legal_force` | `wording_only` |
| Capability required | `claim.accept` with `modality` in `axes_permitted` | `claim.accept.wording_only` |
| Obligations raised | Causal identification standard re-derived; the claim now asserts | None |
| Who can do it | A grant holder with modality authority, subject to conditions | A copy editor |

The copy editor's grant permits edit 2 and refuses edit 1, and it refuses it by naming the axis:

```
$ wi decide --proposal prop-0231 --accept

WI_AUTHORITY_EXCEEDED
  Grant 0193a7c2-11b4-7d3e-8f02-6a1c4e9b0d55 permits capability
  'claim.accept.wording_only' over structure.chapter:ch-02.

  The proposed delta is not wording-only:
    meaning.claim_atom:0193a7c2-0f31-...-7b23
      modality  possibility -> assertion

  Axis 'modality' is not in axes_permitted for this grant.
  Repair: route this proposal to a holder of claim.accept with modality
  authority over ch-02, or withdraw the modality change and resubmit.
```

**Why the endpoint is the wrong thing to authorize.** Authorizing a location assumes that changes to one place are alike. They are not — the two most consequential axes in the IR, modality and scope, are also the two whose surface footprint is smallest. A permission model keyed on where you are editing will always be most permissive exactly where it should be least. Keying on the delta inverts that: a three-character change that widens a claim from seven counties to the whole country requires more authority than rewriting an entire paragraph that asserts nothing new.

**The delta is computed before the check, not after.** `wi simulate` produces the semantic delta without mutating anything, which means the authority check runs against the actual axes that would move rather than against a declaration by the person proposing. Somebody cannot describe their own change as wording-only and have that description believed.

**`max_magnitude_delta_bps` bounds a permitted axis.** A grant may permit the `quantity` axis and still bound how far a quantity may move — five hundred basis points in the example in section 2. Correcting 4.10% to 4.11% is inside it; restating it as 6% is not. The bound is on the *change*, not the value, because the question a reviewer is answering is how far this figure moved and whether that magnitude needs a different signature.

---

## 6. Delegation monotonicity

**Status: specified.** Delegation is executable through `wi authority delegate`.

> A derived grant may never exceed its parent in capability, scope, lifetime, transition axes or condition set.

Every one of the five is checked. Failing any of them rejects the delegation at issue time rather than at use time.

```python
CAPABILITY_ANCESTRY = {
    "claim.accept.wording_only":    "claim.accept",
    "claim.accept.quantity_change": "claim.accept",
    "capsule.export.redacted":      "capsule.export.full",
}

def narrower_or_equal_capability(child: str, parent: str) -> bool:
    """A child may be the same capability or a strict specialization of it."""
    if child == parent:
        return True
    return CAPABILITY_ANCESTRY.get(child) == parent


def check_delegation(child: dict, parent: dict, graph) -> list[str]:
    """Return the reasons a delegation is refused. Empty means permitted."""
    reasons = []

    if parent.get("revoked_at") is not None:
        reasons.append("parent_revoked")

    if not parent.get("delegable", False):
        reasons.append("parent_not_delegable")

    if not narrower_or_equal_capability(child["capability"], parent["capability"]):
        reasons.append("capability_widened")

    if not scope_within(child["scope"], parent["scope"], graph):
        reasons.append("scope_widened")

    if child["not_before"] < parent["not_before"]:
        reasons.append("lifetime_starts_before_parent")
    if parent["not_after"] is not None and (
        child["not_after"] is None or child["not_after"] > parent["not_after"]
    ):
        reasons.append("lifetime_outlives_parent")

    parent_axes = set(parent["transition"]["axes_permitted"])
    child_axes = set(child["transition"]["axes_permitted"])
    if not child_axes.issubset(parent_axes):
        reasons.append("transition_axes_widened")

    parent_bound = parent["transition"].get("max_magnitude_delta_bps")
    child_bound = child["transition"].get("max_magnitude_delta_bps")
    if parent_bound is not None and (child_bound is None or child_bound > parent_bound):
        reasons.append("magnitude_bound_relaxed")

    parent_conditions = {(c["kind"], c["value"]) for c in parent["conditions"]}
    child_conditions = {(c["kind"], c["value"]) for c in child["conditions"]}
    if not parent_conditions.issubset(child_conditions):
        reasons.append("conditions_dropped")

    if child.get("delegable") and not parent.get("delegable"):
        reasons.append("delegability_granted_without_parent_delegability")

    return reasons
```

Read the condition check carefully: the **parent's** conditions must be a subset of the **child's**. A child may add conditions and may never drop one. Every other comparison in the function narrows in the obvious direction; conditions narrow by growing, and writing the subset test the intuitive way around is the single easiest mistake to make here. A delegation that dropped `requires_second_approver_role` would look like a routine handover and would remove a signature from the release.

**Why monotonicity is enforced at issue rather than at use.** A grant chain that is checked only when used produces a refusal at the worst moment, to the person least able to explain it, and the widening might have sat in the graph for months first. Checking at issue means the delegation either exists and is sound or does not exist, and there is no third state in which an unsound grant is present and quiet.

**Chains terminate.** A delegation depth limit is enforced at issue. Each hop can only narrow, so an unbounded chain converges to nothing anyway, but the limit makes the reasoning finite for the audit — reconstructing the basis of an action means walking a bounded number of grants, not an arbitrary graph.

**Revocation cascades.** Revoking a parent revokes every descendant, at the same instant, in the same transaction. A surviving child of a revoked parent is authority derived from something that no longer exists.

---

## 7. Quorum and approval rules

**Status: specified.**

Some transitions require more than one holder. The rule is attached to the transition class in policy, not to the grant, because the requirement belongs to the change rather than to any individual's permission.

| Rule | Satisfied when | Where it fits |
|---|---|---|
| `AnyOne` | One holder of the required capability approves | The default. Most changes. |
| `All` | Every named party approves, in any order | A small set of specific people, all of whom must see it. Contract language, canon changes in a shared universe. |
| `Threshold(k, n)` | At least *k* of *n* named parties approve | A committee where full attendance is not achievable and a majority is meaningful. |
| `Sequence` | Named parties approve in the given order | Where a later reviewer's judgment depends on an earlier one having been made. Technical review, then legal, then sign-off. |

```json
{
  "node_type": "policy.approval_rule",
  "applies_to": {
    "capability": "claim.accept.quantity_change",
    "scope": {"kind": "realm", "realms": ["external_fact"]},
    "when": {"max_magnitude_delta_bps_exceeds": 500}
  },
  "rule": {
    "kind": "Sequence",
    "steps": [
      {"role": "author",           "capability": "claim.propose"},
      {"role": "finance_reviewer", "capability": "claim.accept.quantity_change"},
      {"role": "release_approver", "capability": "release.approve"}
    ]
  },
  "distinct_actors_required": true
}
```

**`distinct_actors_required` defaults to true.** One person holding three grants does not constitute three approvals. Without it, `Threshold(2, 5)` is satisfied by a single actor who happens to hold two of the five grants, and the rule that was written to require two judgments records one. This is the most common way a quorum rule becomes decorative, and the default is set against it.

**Why `Sequence` rather than `All` in the example.** A legal reviewer assessing a figure that finance has not yet confirmed is assessing a number that may change, and their approval will be attached to a state that no longer exists by the time finance is done. `Sequence` makes the dependency explicit and forces re-approval when an earlier step's state changes — because each approval binds to a `state_digest`, and a change upstream produces a new one.

**Approvals go stale.** Every approval in a quorum names the exact target state. If the target moves, prior approvals do not transfer. The refusal is `WI_DECISION_STALE` and it is discussed in [`SEMANTIC_VERSION_CONTROL.md`](SEMANTIC_VERSION_CONTROL.md). A quorum system in which approvals survive changes to the thing approved is a quorum system that records agreement to something nobody read.

---

## 8. Revocation and expiry

**Status: specified.** Revocation is executable through `wi authority revoke`.

| Event | Effect on the grant | Effect on prior actions |
|---|---|---|
| Expiry (`not_after` passes) | Grant stops authorizing. Not deleted. | None. Actions taken while it was live remain authorized. |
| Revocation | `revoked_at` stamped, descendants cascade | None by default. |
| Revocation with `invalidate_actions: true` | As above | Actions taken under the grant since a named instant are flagged for review. Not reversed. |

**Why revocation does not reverse prior actions by default.** The action was authorized when it was taken, and rewriting that fact is a false statement about the past — the same error `BITEMPORAL_STATE.md` refuses on the knowledge axis. If a grant is revoked because it was issued in error or abused, the actions taken under it need review by a person, and flagging them for review is the honest operation. Automatic reversal would also produce a second problem: a cascade of retractions with no decision record behind any of them.

**Revocation is a stamp, never a deletion.** A deleted grant makes every action taken under it unexplainable. The audit question is not *who has authority now* but *what authorized this change* — and that question is asked most often about grants that no longer exist.

**Expiry is not a failure state.** A lapsed grant produces `WI_AUTHORITY_ABSENT` with the expiry instant named, which is a different message from never having held it. The distinction matters because the repairs differ: one is a renewal, the other is a request.

---

## 9. The command surface

**Status: executable in `scripts/wi.py`.**

```
$ wi authority check --actor act-0007 \
                     --capability claim.accept.quantity_change \
                     --node meaning.claim_atom:0193a7c2-0f31-7a44-b6d2-1e5c9a0f7b23 \
                     --delta quantity:+0.01pp

grant     0193a7c2-11b4-7d3e-8f02-6a1c4e9b0d55
capability claim.accept.quantity_change  (exact match)
scope      structure_subtree structure.chapter:ch-02  (node is in scope)
lifetime   [2027-03-01, 2027-06-01)  valid at 2027-04-12T10:02:11Z
axes       quantity permitted; delta touches quantity only
magnitude  1 bps requested, 500 bps permitted
conditions requires_no_open_conflicts        satisfied (0 open)
           requires_evidence_reliability     satisfied (verified)
           requires_second_approver_role     UNSATISFIED (finance_reviewer)

RESULT  authorized_pending_quorum
        1 of 2 required approvals present.
```

```
$ wi authority list --actor act-0007

grant        capability                    scope                     expires
0193a7c2..55 claim.accept.quantity_change  ch-02 / external_fact     2027-06-01
0193a7c2..91 claim.accept.wording_only     ch-02                     2027-06-01
0193a7c2..a4 claim.propose                 branch main               2027-09-01

3 live, 0 expired, 1 revoked (use --all)
```

```
$ wi authority delegate --parent 0193a7c2-11b4-7d3e-8f02-6a1c4e9b0d55 \
                        --subject act-0019 \
                        --not-after 2027-07-01

WI_AUTHORITY_EXCEEDED
  Refusing delegation for 2 reasons:
    lifetime_outlives_parent   child not_after 2027-07-01 > parent 2027-06-01
    parent_not_delegable       parent grant has delegable: false

  A delegation may only narrow. Repair: set --not-after on or before
  2027-06-01, and have the parent reissued as delegable if onward
  delegation is intended.
```

Every refusal names the grant, the reason and a repair. A refusal that says only *permission denied* teaches the person nothing except to ask somebody with more access, which is how permission models get worked around rather than fixed.

---

## Related documents

- [`CONSTITUTION.md`](CONSTITUTION.md) — Law O, and the constitutional denials
- [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) — enforcement at the boundary
- [`SECURITY_MODEL.md`](SECURITY_MODEL.md) — the threat model these grants sit inside
- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — the axes a transition-aware grant names
- [`SEMANTIC_VERSION_CONTROL.md`](SEMANTIC_VERSION_CONTROL.md) — decisions, staleness and the proposal DAG
- [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) — what an `autonomous_agent` may hold
- [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) — why a provider's output is an opinion
- [`../v5/POLICY_AS_CODE.md`](../v5/POLICY_AS_CODE.md) — where approval rules are declared

---

*A role describes somebody. A grant states what they may do, to what, until when. Only one of those can be checked at the moment it matters.*

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
