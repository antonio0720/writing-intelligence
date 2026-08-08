# Semantic Version Control

Branches, commits and merges over meaning rather than over lines of text.

Created by **[Antonio T. Smith Jr.](https://densitysix.com)** — Founder & CEO, Density6 LLC.

Law M of the v6 constitution states that the semantic state is canonical and renderings are builds. This document is the version control system that follows from it. A commit records a transition in the meaning graph. A branch is a named pointer into an immutable object store. A diff is a set of semantic deltas on named axes. None of the three has anything to do with files, and that is the entire point: two documents that assert the same thing in different words have no difference worth recording, and two that assert different things in identical words have one that no line-based tool can see.

Read this with [`SEMANTIC_IR.md`](SEMANTIC_IR.md) for what a state is, [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md) for who may move it, and [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) for what happens when two branches disagree.

---

## Contents

1. [The three objects](#1-the-three-objects)
2. [Branches](#2-branches)
3. [Commits](#3-commits)
4. [The graph delta](#4-the-graph-delta)
5. [Semantic branch protection](#5-semantic-branch-protection)
6. [The proposal DAG](#6-the-proposal-dag)
7. [Proposal status, and the state that does not exist](#7-proposal-status-and-the-state-that-does-not-exist)
8. [Decisions bind to a digest](#8-decisions-bind-to-a-digest)
9. [A session, end to end](#9-a-session-end-to-end)

---

## 1. The three objects

**Status: executable in `scripts/wi.py`.**

| Object | What it is | Mutable? |
|---|---|---|
| `GraphRoot` | A hash committing to the entire meaning graph at one instant | No |
| `SemanticCommit` | A transition from one graph root to another, with its delta, actor and basis | No |
| `GraphDelta` | The set of semantic changes between two roots, on named axes | No — derived, and derived deterministically |

Everything in the store is content-addressed and immutable. A branch is the only mutable thing in the system, and all it holds is a pointer.

```json
{
  "node_type": "vcs.graph_root",
  "root": "sha256:5d2a91cf0b8e473a6c15d09fe2b84a7c3f60e1d9a4b7c2e8d0f3a6b9c1d4e7f2",
  "algorithm": "merkle/sha256-jcs-v1",
  "node_count": 1274,
  "edge_count": 3891,
  "computed_at": "2027-04-12T10:02:11Z",
  "sections": {
    "meaning":   "sha256:1f7a0c93be48d25607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",
    "structure": "sha256:9b04e7a2c15d38f607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",
    "evidence":  "sha256:44c1908fbe2d75a307a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",
    "authority": "sha256:7e30bd91c48a25f607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",
    "policy":    "sha256:0a58f2c9d417be3607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205"
  }
}
```

**Why the root is sectioned.** A single hash over everything answers one question — did anything change — and that is the least useful question available. Sectioning lets a comparison start by ruling out four fifths of the graph in four equality tests. A release that touched only wording has an unchanged `meaning` section, and the release gate can say so without walking 1,274 nodes.

**Why the algorithm is named in the object.** A root computed under a different Merkle construction is not comparable to this one. Naming it means a future change to the construction produces an explicit refusal rather than a silent mismatch reported as a graph-wide change.

---

## 2. Branches

**Status: executable in `scripts/wi.py`.**

```
$ wi branch create release/2027-q2 --from main

created release/2027-q2 at sha256:5d2a91cf...e7f2
0 objects written
```

Zero objects written. That number is the design.

A branch is a named reference to a commit. Creating one writes a single row: a name, a commit digest, an instant and the actor who created it. It copies nothing, because there is nothing to copy — every node in the graph is already an immutable object in the store, and both branches now point at commits that reference the same objects.

```sql
CREATE TABLE branch (
    name            TEXT PRIMARY KEY,
    head_commit     TEXT NOT NULL,
    created_at      TEXT NOT NULL,
    created_by      TEXT NOT NULL,
    protection_rule TEXT,
    FOREIGN KEY (head_commit) REFERENCES commit_object(digest)
);
```

**Why O(1) branching is load-bearing rather than a performance note.** The cost of an operation decides whether people use it. Branching that duplicates a workspace is expensive enough that authors stop doing it, so exploratory work happens on the branch that matters, and the safeguard exists in the manual rather than in practice. Branching that costs one row makes the safe path the cheap path — a contributor who wants to try restating a chapter does it on a branch because that is less work than not doing it.

The property follows from immutability. Because a state is identified by the hash of its content, two branches holding the same state hold the same object, and divergence costs only the objects that actually differ. A workspace with forty branches and one active line of work is barely larger than one with a single branch.

**Deletion removes the pointer and nothing else.**

```
$ wi branch delete experiment/tighter-claims

deleted experiment/tighter-claims (was sha256:8f21bc40...9d31)
0 objects removed; 3 commits remain reachable by digest
```

Objects are not garbage collected on branch deletion. A commit that was the head of a deleted branch is still addressable, and any decision or verification that bound to a state in it still resolves. Deleting a branch removes a name, not history.

---

## 3. Commits

**Status: executable in `scripts/wi.py`.**

```json
{
  "node_type": "vcs.commit",
  "digest": "sha256:a72f10c9bd485e3607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",

  "parent_roots": ["sha256:5d2a91cf0b8e473a6c15d09fe2b84a7c3f60e1d9a4b7c2e8d0f3a6b9c1d4e7f2"],
  "graph_root":   "sha256:c9014f7a2b8d365e07a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",

  "branch": "main",
  "committed_at": "2027-04-12T10:02:11Z",

  "actor": {"actor_id": "act-0007", "actor_kind": "team_member"},
  "authorized_by": "authority.grant:0193a7c2-11b4-7d3e-8f02-6a1c4e9b0d55",
  "decision": "decision.record:0193a7c2-7f10-7b93-a48c-2d6e1f0a9c34",

  "delta_digest": "sha256:3e8b0d41ca975f2607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",
  "delta_summary": {
    "nodes_added": 0,
    "nodes_superseded": 1,
    "edges_added": 0,
    "edges_removed": 0,
    "axes_touched": ["quantity"],
    "wording_only": false
  },

  "message": "Correct 2026 unemployment figure to 4.0% per BLS August 2029 revision"
}
```

Four fields carry the weight.

**`parent_roots` is a list.** One parent for an ordinary commit, two for a merge. The list is what makes a three-way merge possible later: the common ancestor is found by walking parents, and a commit that recorded only its immediate predecessor would leave every merge without a base.

**`authorized_by` is not optional on a consequential commit.** It names the grant under which the transition became authoritative. A commit with a null grant is refused by `wi commit` with `WI_AUTHORITY_ABSENT`, and the refusal names the capability that was missing and the axes the delta touched.

**`decision` is present when a decision was required.** Not every commit needs one — a wording-only change under a `claim.accept.wording_only` grant is authorized and does not require a separate decision record. A quantity change above the grant's magnitude bound does, and the commit names it.

**`delta_digest` commits to the full delta.** `delta_summary` is a convenience for `wi log`; the digest is the thing anything else binds to. A summary that disagreed with the delta would be a report about a change that did not happen, so the summary is derived from the delta at commit time and never authored.

```
$ wi log --branch main --limit 4

a72f10c9  2027-04-12 10:02  act-0007   quantity            1 superseded
          Correct 2026 unemployment figure to 4.0% per BLS August 2029 revision
          decision decision.record:0193a7c2-7f10-...  grant 0193a7c2-11b4-...

5d2a91cf  2027-04-09 15:47  act-0002   wording_only        3 superseded
          Tighten chapter two introduction
          grant 0193a7c2-...-91  (no decision required)

8f21bc40  2027-04-08 11:20  act-0001   scope, modality     2 superseded
          Narrow the wait-time finding to the seven observed counties
          decision decision.record:0193a7c2-4a02-...  grant 0193a7c2-...-a4

3ce07b19  2027-04-08 09:05  act-0031   —                   0 superseded
          Ingest BLS 2029-08 revision as source
          grant 0193a7c2-...-c7  (source.ingest)
```

The axis column is the log's most useful field. Three of these four commits are unremarkable; the third widened nothing and narrowed a claim, and the first moved a number. Somebody scanning for what changed in the work reads the axes, not the messages, because the messages are written by people and the axes are derived.

---

## 4. The graph delta

**Status: executable in `scripts/wi.py`.** Computing a delta without mutating anything is `wi simulate`.

```json
{
  "node_type": "vcs.delta",
  "digest": "sha256:3e8b0d41ca975f2607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",
  "from_root": "sha256:5d2a91cf...e7f2",
  "to_root":   "sha256:c9014f7a...f205",

  "changes": [
    {
      "logical_id": "0193a7c2-4d18-7f61-b209-3c7e0a4b9d12",
      "from_state": "sha256:6b30e9a1...f205",
      "to_state":   "sha256:c85f1a70...f205",
      "kind": "supersede",
      "axes": [
        {
          "axis": "quantity",
          "path": "body.quantities[0]",
          "from": {"value": "41", "scale": 1, "unit": "percent"},
          "to":   {"value": "40", "scale": 1, "unit": "percent"},
          "magnitude_delta_bps": 10,
          "direction": "decrease"
        },
        {
          "axis": "attribution",
          "path": "body.attribution.restatement_of",
          "from": "source:bls-2027-03",
          "to":   "source:bls-2029-08"
        }
      ]
    }
  ],

  "invalidated": [
    {"logical_id": "0193a7c2-9c41-...", "reason": "hard_dependency_on_changed_quantity"}
  ],
  "provably_unaffected": 1271
}
```

**`provably_unaffected` is a count, not an assumption.** It is the number of nodes the invalidation walk proved could not be reached from any changed state through an edge with a non-`none` invalidation policy. Reporting it as a number rather than leaving it implicit is what makes the invalidated list trustworthy: a reviewer can see that the system considered the whole graph and concluded, rather than that it looked at a few neighbours and stopped. The walk itself is specified in [`../v5/STALENESS.md`](../v5/STALENESS.md).

**Axes are named, and the magnitude is computed.** `magnitude_delta_bps` is what an authority check reads against a grant's `max_magnitude_delta_bps` bound. Computing it in the delta rather than at the check means one implementation produces it and every consumer — the authority check, the log, the release gate, the quorum rule — reads the same number.

**A delta is derived, never authored.** Nobody writes a delta. `wi simulate` computes it from two roots, and `wi commit` recomputes it rather than accepting one from the caller. A caller-supplied delta would let the description of a change disagree with the change, which is the failure the whole object exists to prevent.

---

## 5. Semantic branch protection

**Status: specified.**

Line-based protection rules ask questions about files: which paths changed, how many reviewers approved, did the tests pass. None of those questions is about what the work now asserts.

```yaml
# .wi/policy/branch-protection.yaml
branches:
  main:
    rules:
      - no_unresolved_semantic_conflicts
      - no_stale_hard_dependencies
      - no_quantity_change_without_budget_recheck
      - no_legal_force_change_without_role: legal_reviewer
      - no_external_fact_without_required_evidence
      - no_provider_as_decision_actor
```

| Rule | What it refuses | Why it cannot be expressed over files |
|---|---|---|
| `no_unresolved_semantic_conflicts` | A merge into `main` while any conflict node remains open | A conflict is two states of one logical node that both claim to hold. It has no file location, and preserving it rather than resolving it is Law Q. |
| `no_stale_hard_dependencies` | A commit where any node is downstream of a changed source through a `hard` edge and has not been re-verified | Staleness is a property of a dependency graph. The file containing the stale claim may not have been touched in months. |
| `no_quantity_change_without_budget_recheck` | Any commit whose delta touches `quantity` on a node inside the budget subtree, without a matching recomputation | The change is three characters in one cell. The check is that everything computed from it moved with it. |
| `no_legal_force_change_without_role: legal_reviewer` | A modality or obligation change without an approval from a holder of that role | Modality is one word. No file rule can distinguish "may" becoming "will" from any other word substitution. |
| `no_external_fact_without_required_evidence` | A commit that adds or supersedes an `external_fact` node whose evidence does not meet the realm's standard | The evidence requirement depends on the node's realm and reliability type, neither of which is visible from a path. |
| `no_provider_as_decision_actor` | A commit whose decision record names a `judgment_provider` | Constitutional. It is a statement about who decided, not about what changed. |

```
$ wi merge feature/tighter-claims --into main

WI_CONFLICT_OPEN
  Refusing merge into 'main': branch protection.

  no_unresolved_semantic_conflicts
    1 open conflict on meaning.claim_atom:0193a7c2-4d18-...-9d12
      main    4.0 percent   valid [2026-01-01, 2027-01-01)
      feature 4.1 percent   valid [2026-01-01, 2027-01-01)
    Both currently believed; valid intervals intersect; values differ.

  no_stale_hard_dependencies
    2 nodes downstream of source:bls-2029-08 have not been re-verified:
      meaning.claim_atom:0193a7c2-9c41-...   hard
      meaning.metric:m-0031                  hard

  Repair: resolve the conflict with a recorded basis (wi decide), then
  re-verify the 2 stale nodes. Neither is bypassable by re-running merge.
```

**Why protection is expressed over meaning.** A rule about files is a proxy for a rule about consequences, and proxies drift. Requiring two reviewers on `finance/*.md` is an attempt to say *a figure should not move without a second pair of eyes* — and it fails in both directions the moment a figure moves in a file outside that path, or somebody reorganizes the directory. Stating the rule over the axis it is about removes the proxy: the check follows the quantity wherever it lives.

---

## 6. The proposal DAG

**Status: executable in `scripts/wi.py`.**

A proposal is a candidate transition bound to an exact target state. Proposals may depend on other proposals, which makes the set a directed acyclic graph rather than a queue.

```json
{
  "node_type": "vcs.proposal",
  "proposal_id": "prop-0231",
  "created_at": "2027-04-11T14:08:52Z",
  "created_by": {"actor_id": "act-0031", "actor_kind": "judgment_provider"},

  "branch": "main",
  "target_state": "sha256:6b30e9a1c47d2f5808b1c94f7e2d06a35fc51b8047e9c2d0f3a6b9c1d4e7f205",
  "target_logical_id": "0193a7c2-4d18-7f61-b209-3c7e0a4b9d12",

  "depends_on": ["prop-0229"],

  "proposed_state": "sha256:c85f1a70d2b94e3607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",
  "delta_digest":   "sha256:3e8b0d41ca975f2607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",

  "basis": {
    "kind": "source_revision",
    "source": "source:bls-2029-08",
    "note": "Agency revised the 2026 annual figure from 4.1 to 4.0."
  },

  "status": "open"
}
```

**`target_state` is a digest, not a logical id.** The proposal is a statement about one exact state of one node. If that state is superseded before the proposal is decided, the proposal does not silently re-attach to the successor. It goes stale, and section 8 explains why that is the whole point.

**`depends_on` makes ordering explicit.** Proposal 0231 revises a figure; proposal 0229 ingests the source that justifies it. Accepting 0231 first would produce a commit whose basis points at a source the workspace has not ingested.

```
$ wi proposals --branch main

id        target                          axes            status    depends
prop-0229 source:bls-2029-08              —               open      —
prop-0231 meaning.claim_atom:...-9d12     quantity,       blocked   prop-0229
                                          attribution
prop-0234 meaning.claim_atom:...-7b23     modality        stale     —
prop-0236 structure.chapter:ch-02         wording_only    open      —

4 proposals: 2 open, 1 blocked, 1 stale
```

`blocked` is derived from `depends_on`, not authored. A proposal whose dependency is undecided cannot be accepted, and the listing says which one is holding it. Cycles are refused at creation: a proposal that depends, transitively, on itself would be a set that can never be entered.

---

## 7. Proposal status, and the state that does not exist

**Status: executable in `scripts/wi.py`.**

| Status | Meaning | Set by |
|---|---|---|
| `open` | Awaiting a decision | Creation |
| `blocked` | A dependency is undecided | Derived from `depends_on` |
| `stale` | The target state has been superseded | Derived from the graph |
| `accepted` | A decision to accept has been recorded | `wi decide` |
| `rejected` | A decision to reject has been recorded, with a basis | `wi decide` |
| `withdrawn` | The proposer withdrew it | The proposer |
| `superseded` | Replaced by a later proposal against the same target | Creation of the replacement |

**There is no `applied` status.**

That absence is deliberate and it is the most consequential design decision in this document. A proposal being `accepted` is a statement that a person with authority decided it should become state. The commit that makes it state is a separate, transactional event with its own digest, its own actor and its own entry in `wi log`.

**Why conflating them creates exactly the ambiguity v6 exists to remove.** With a single `applied` status, the record cannot distinguish four situations that require four different responses:

| Situation | Under `accepted` + commit | Under a single `applied` |
|---|---|---|
| Decided, commit succeeded | `accepted`, commit present | `applied` |
| Decided, commit failed on a protection rule | `accepted`, no commit — visible and repairable | Ambiguous: was it decided? |
| Decided, commit failed on a transaction fault | `accepted`, no commit — retryable | Ambiguous, and retrying may double-apply |
| Never decided, but state changed by another route | No `accepted` record — an unexplained commit | Looks identical to a decided change |

The fourth row is the dangerous one. A system in which acceptance and application are one thing cannot represent a state change that nobody decided, so when one occurs it is recorded as though somebody had. Keeping them apart means an authoritative change with no decision behind it is a visible inconsistency rather than a well-formed record of a decision that was never made.

```
$ wi decide --proposal prop-0231 --accept \
            --basis "BLS August 2029 annual revision, table A-1"

decision  decision.record:0193a7c2-7f10-7b93-a48c-2d6e1f0a9c34
proposal  prop-0231 -> accepted
actor     act-0007  grant 0193a7c2-11b4-...
bound to  sha256:6b30e9a1...f205

Proposal accepted. No state has changed.
Run `wi commit` to apply it; the commit will re-check authority and
branch protection against the graph as it stands at that moment.
```

The last two lines are the sentence the whole design exists to make true.

---

## 8. Decisions bind to a digest

**Status: executable in `scripts/wi.py`.**

A decision names the exact state it was made about. If that state moves, the decision does not follow it.

```json
{
  "node_type": "decision.record",
  "logical_id": "0193a7c2-7f10-7b93-a48c-2d6e1f0a9c34",
  "decided_at": "2027-04-12T09:58:03Z",
  "actor": {"actor_id": "act-0007", "actor_kind": "team_member"},
  "authorized_by": "authority.grant:0193a7c2-11b4-7d3e-8f02-6a1c4e9b0d55",

  "proposal": "prop-0231",
  "bound_to_state": "sha256:6b30e9a1c47d2f5808b1c94f7e2d06a35fc51b8047e9c2d0f3a6b9c1d4e7f205",
  "bound_to_delta": "sha256:3e8b0d41ca975f2607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",

  "verdict": "accept",
  "basis": "BLS August 2029 annual revision, table A-1"
}
```

If the target is superseded between the decision and the commit, the commit refuses:

```
$ wi commit

WI_DECISION_STALE
  Decision decision.record:0193a7c2-7f10-... was bound to
    sha256:6b30e9a1...f205
  The current state of meaning.claim_atom:0193a7c2-4d18-...-9d12 is
    sha256:d47b02e9...f205   (superseded 2027-04-12T09:59:41Z by act-0002)

  The decision is not transferable. The delta it approved is not the
  delta that would now be applied:

    approved   quantity  4.1 -> 4.0            (10 bps)
    current    quantity  4.1 -> 4.0, and
               spatial_scope  7 counties -> unbounded

  Repair: re-simulate against the current state and decide again.
  `wi simulate --proposal prop-0231` shows the delta as it now stands.
```

**Why a decision does not re-attach.** Re-attaching is the accommodating behaviour and it is the one that produces a false record. The person approved a ten basis point correction to a figure. In the ninety-eight seconds between their decision and the commit, somebody else widened the claim from seven counties to the whole country. Under re-attachment, the record says they approved both, and it says so in a form indistinguishable from an approval they actually gave. Nothing in the graph would ever reveal the difference, and the person's name is on a scope widening they never saw.

The cost of not re-attaching is that they are asked again. That is a small cost, paid visibly, by the person best placed to notice that the change has grown.

**Staleness is detected by digest equality, not by heuristics.** There is no tolerance and no attempt to decide whether the intervening change was material. The decision named a digest; the digest either matches or it does not. Any rule of the form *re-attach if the additional change is small* is a rule that eventually re-attaches an approval to something the approver would have refused, and it does so precisely in the cases nobody reviewed.

---

## 9. A session, end to end

**Status: executable in `scripts/wi.py`.**

A revision arrives from a statistical agency. The whole loop, with nothing elided.

```
$ wi branch create fix/bls-2029-revision --from main
created fix/bls-2029-revision at sha256:5d2a91cf...e7f2
0 objects written

$ wi propose --node meaning.claim_atom:0193a7c2-4d18-7f61-b209-3c7e0a4b9d12 \
             --set body.quantities[0].value=40 \
             --set body.attribution.restatement_of=source:bls-2029-08 \
             --depends-on prop-0229 \
             --basis "BLS August 2029 annual revision, table A-1"

prop-0231 created
target    sha256:6b30e9a1...f205   (current)
status    blocked  (prop-0229 undecided)
```

```
$ wi simulate --proposal prop-0231

candidate root   sha256:c9014f7a...f205
semantic deltas  1 node superseded
  meaning.claim_atom:0193a7c2-4d18-...-9d12
    quantity     4.1 -> 4.0 percent      10 bps, decrease
    attribution  bls-2027-03 -> bls-2029-08

stale frontier   2 nodes
  meaning.claim_atom:0193a7c2-9c41-...   hard    downstream quantity
  meaning.metric:m-0031                  hard    metric restatement

provably unaffected  1271 nodes
conflicts            0
repair plan          re-verify 2 nodes after commit; no re-authoring required

Nothing was mutated.
```

```
$ wi decide --proposal prop-0229 --accept --basis "Source retrieved from bls.gov, hash verified"
decision  decision.record:0193a7c2-3b71-...
proposal  prop-0229 -> accepted

$ wi decide --proposal prop-0231 --accept --basis "BLS August 2029 annual revision, table A-1"
decision  decision.record:0193a7c2-7f10-...
proposal  prop-0231 -> accepted
bound to  sha256:6b30e9a1...f205

Proposal accepted. No state has changed.
```

```
$ wi commit --message "Correct 2026 unemployment figure to 4.0% per BLS August 2029 revision"

authority   grant 0193a7c2-11b4-...  claim.accept.quantity_change
            axes touched: quantity, attribution — both permitted
            magnitude 10 bps of 500 permitted
            conditions: no open conflicts ok; evidence verified ok;
                        second approver finance_reviewer ok (act-0011)

commit      a72f10c9bd485e36...
root        sha256:5d2a91cf...e7f2 -> sha256:c9014f7a...f205
superseded  1 node; knowledge interval closed at 2027-04-12T10:02:11Z
stale       2 nodes flagged for re-verification
```

```
$ wi merge fix/bls-2029-revision --into main

WI_CONFLICT_OPEN  0
protection        no_unresolved_semantic_conflicts    pass
                  no_stale_hard_dependencies          FAIL  2 nodes
                  no_quantity_change_without_budget_recheck  pass
                  no_legal_force_change_without_role  pass  (no modality delta)
                  no_external_fact_without_required_evidence pass
                  no_provider_as_decision_actor       pass

Merge refused. Re-verify the 2 stale nodes, then merge again.
```

The refusal at the end is the system working. A correct figure has been committed on a branch, two claims downstream of it have not been checked against the new value, and `main` will not take it until they are. Nothing about that sequence required anybody to remember which downstream claims existed.

---

## Related documents

- [`CONSTITUTION.md`](CONSTITUTION.md) — Laws M, P and Q, which this implements
- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — what a state contains
- [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md) — grants, transition-awareness and quorum
- [`BITEMPORAL_STATE.md`](BITEMPORAL_STATE.md) — how a commit stamps knowledge time
- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — conflict-preserving three-way merge
- [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) — what `wi simulate` computes
- [`../v5/STALENESS.md`](../v5/STALENESS.md) — the invalidation walk and the unaffected set
- [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) — the object store and dual identity
- [`../v4/PROPOSAL_PROTOCOL.md`](../v4/PROPOSAL_PROTOCOL.md) — the original propose-never-replace rule

---

*Accepting a proposal and applying it are two events. A system that records them as one cannot tell you which of them happened.*

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
