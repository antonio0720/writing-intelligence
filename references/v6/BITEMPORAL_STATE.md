# Bitemporal State

Two clocks. When the world was that way, and when we believed it.

Created by **[Antonio T. Smith Jr.](https://densitysix.com)** — Founder & CEO, Density6 LLC.

Law N of the v6 constitution states that time is part of meaning. This document is the mechanism. Every governed semantic state carries two independent intervals, and the pair is what allows the system to answer a question no single-clock store can answer: *was the report we filed in March 2027 accurate at the time we filed it?*

Read this with [`SEMANTIC_IR.md`](SEMANTIC_IR.md), which defines the envelope the intervals live in, and with [`CONSTITUTION.md`](CONSTITUTION.md) for the law they serve.

---

## Contents

1. [Two axes](#1-two-axes)
2. [Half-open intervals](#2-half-open-intervals)
3. [A revision, worked](#3-a-revision-worked)
4. [The query surface](#4-the-query-surface)
5. [Temporal contradiction requires intersection](#5-temporal-contradiction-requires-intersection)
6. [Archival authorship, not overwrite history](#6-archival-authorship-not-overwrite-history)
7. [Reconstructing a release](#7-reconstructing-a-release)
8. [What the two clocks do not do](#8-what-the-two-clocks-do-not-do)

---

## 1. Two axes

**Status: specified.** Querying across both axes is executable through `wi as-of`.

| Axis | Field pair | Question it answers | Who moves it |
|---|---|---|---|
| **Valid time** | `valid_from`, `valid_until` | When is this claimed to have been true in the world? | The author, deliberately. It is part of what the claim says. |
| **Knowledge time** | `known_from`, `known_until` | When did this workspace hold this belief? | The system, on commit. Never authored by hand. |

Valid time is a statement. Knowledge time is a record. Confusing them is the single most common failure in systems that add one clock and stop.

A claim about 2022 unemployment has a valid interval covering 2022 and a knowledge interval that begins whenever somebody wrote it down. If the figure is revised in 2029, the *valid* interval of both the old and the new state still covers 2022 — the year did not change. What changed is which of the two the workspace believes, and that is knowledge time.

**Why one clock is not enough.** With valid time alone, a correction overwrites the prior figure and the workspace becomes unable to say what it reported last year. With knowledge time alone, the workspace can replay its own history but cannot answer questions about the world across time, so a claim about 2022 and a claim about 2023 look like a contradiction. Both questions are asked in practice, usually by different people, and usually at the worst moment. A funder asks the first. An analyst asks the second.

**Why knowledge time is never authored.** If a human can set `known_from`, the audit trail becomes a claim rather than a record, and the one property that made it worth keeping — that it says what the workspace actually believed, whether or not that is convenient — is gone. `known_from` is stamped by the commit transaction from the workspace clock and is immutable thereafter. A backdated belief is not representable.

---

## 2. Half-open intervals

**Status: specified.**

Every interval on both axes is half-open: `[from, until)`. The `from` instant is included, the `until` instant is excluded. `until: null` means open — still holding, no known end.

```json
{
  "valid_from":  "2022-01-01T00:00:00Z",
  "valid_until": "2023-01-01T00:00:00Z",
  "known_from":  "2027-03-14T16:22:09Z",
  "known_until": null
}
```

That interval covers the whole of 2022 and nothing of 2023.

**Why half-open and not inclusive on both ends.** Inclusive intervals cannot tile a timeline without either a gap or an overlap. Two adjacent closed years are `[2022-01-01, 2022-12-31]` and `[2023-01-01, 2023-12-31]`, which leaves the last day of 2022 and the first of 2023 adjacent but not contiguous — fine at day granularity and wrong the moment somebody stores a timestamp, because `2022-12-31T18:00:00Z` falls in the first and `2022-12-31T23:59:59.500Z` falls in neither. The workaround is an end-of-day sentinel, then a last-microsecond sentinel, and the sentinel is different for every granularity the system supports.

Half-open intervals tile exactly. `[2022-01-01, 2023-01-01)` and `[2023-01-01, 2024-01-01)` are contiguous, non-overlapping, and correct at every resolution from a year to a nanosecond. Adjacency is a single equality test rather than a comparison against a granularity-dependent epsilon.

```python
from datetime import datetime

def overlaps(a_from, a_until, b_from, b_until) -> bool:
    """Half-open intersection. None means open-ended."""
    if a_until is not None and b_from is not None and a_until <= b_from:
        return False
    if b_until is not None and a_from is not None and b_until <= a_from:
        return False
    return True

def contains(from_, until, instant) -> bool:
    if from_ is not None and instant < from_:
        return False
    if until is not None and instant >= until:
        return False
    return True
```

Note the asymmetry in `contains`: `<` on the lower bound and `>=` on the upper. That is the whole of half-openness, and it is the reason two adjacent intervals never both contain the same instant.

**Granularity is recorded, not inferred.** A claim stated at year granularity stores `granularity: "year"` alongside its interval. The interval is still an exact instant pair, so comparison is exact; the granularity tells a renderer to write *2022* rather than *1 January 2022 to 31 December 2022*, and tells the constraint engine not to report a conflict between two claims that differ only below their stated resolution.

---

## 3. A revision, worked

**Status: specified.** The queries shown are executable through `wi as-of`.

The unemployment rate for 2026 is first reported in a March 2027 statistical release as 4.1%. In August 2029 the agency issues a revision: the 2026 figure was 4.0%.

Both states are retained. Neither is edited.

**State one, authored March 2027:**

```json
{
  "logical_id": "0193a7c2-4d18-7f61-b209-3c7e0a4b9d12",
  "state_digest": "sha256:6b30e9a1c47d2f5808b1c94f7e2d06a35fc51b8047e9c2d0f3a6b9c1d4e7f205",
  "node_type": "meaning.claim_atom",

  "valid_from":  "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "known_from":  "2027-03-14T16:22:09Z",
  "known_until": "2029-08-21T11:04:53Z",

  "body": {
    "subject":   {"kind": "region", "term": "meaning.term:t-0002", "label": "national"},
    "object":    {"kind": "metric", "term": "meaning.metric:m-0031",
                  "label": "unemployment rate"},
    "quantities": [{"role": "magnitude", "value": "41", "scale": 1,
                    "unit": "percent", "unit_system": "ratio", "basis": "absolute"}],
    "attribution": {"kind": "restatement", "restatement_of": "source:bls-2027-03"}
  }
}
```

**State two, authored August 2029:**

```json
{
  "logical_id": "0193a7c2-4d18-7f61-b209-3c7e0a4b9d12",
  "state_digest": "sha256:c85f1a70d2b94e3607a1b8f4e3d90c26ba5f0197c4e2b8d0f3a6b9c1d4e7f205",
  "node_type": "meaning.claim_atom",

  "valid_from":  "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "known_from":  "2029-08-21T11:04:53Z",
  "known_until": null,

  "body": {
    "quantities": [{"role": "magnitude", "value": "40", "scale": 1,
                    "unit": "percent", "unit_system": "ratio", "basis": "absolute"}],
    "attribution": {"kind": "restatement", "restatement_of": "source:bls-2029-08"},
    "supersedes": "sha256:6b30e9a1c47d2f5808b1c94f7e2d06a35fc51b8047e9c2d0f3a6b9c1d4e7f205"
  }
}
```

Four things to read off the pair.

**The `logical_id` is the same and the `state_digest` is not.** The thing being asserted — the national unemployment rate for 2026 — is one thing with one identity. Two states of it exist, and every verification, decision and waiver in the workspace binds to a digest, so none of them silently transfers from the 4.1% state to the 4.0% state.

**Valid time is identical in both.** 2026 is 2026. A revision is not a claim about a different year, and a store that moved the valid interval to record the revision would be recording a fact that is not true.

**Knowledge time partitions.** The first state's knowledge interval closes at exactly the instant the second's opens. There is no moment at which the workspace believed both and no moment at which it believed neither. That is the tiling property from section 2 doing real work: the closure instant and the opening instant are the same value, and half-openness makes that unambiguous.

**Nothing was overwritten.** The March 2027 state still exists, still hashes to the same digest, and still supports the verification that was attached to it in 2027. The filed report has not become retroactively wrong; it has become superseded, which is a different fact and the one that is true.

---

## 4. The query surface

**Status: executable in `scripts/wi.py`.**

`wi as-of` takes two independent flags and returns the state selected by both.

```
$ wi as-of --valid-at 2026-06-01 --known-at 2027-06-01 \
           --node 0193a7c2-4d18-7f61-b209-3c7e0a4b9d12

state    sha256:6b30e9a1...f205
value    4.1 percent
valid    [2026-01-01, 2027-01-01)
known    [2027-03-14T16:22:09Z, 2029-08-21T11:04:53Z)
source   source:bls-2027-03
```

```
$ wi as-of --valid-at 2026-06-01 --known-at now \
           --node 0193a7c2-4d18-7f61-b209-3c7e0a4b9d12

state    sha256:c85f1a70...f205
value    4.0 percent
valid    [2026-01-01, 2027-01-01)
known    [2029-08-21T11:04:53Z, open)
source   source:bls-2029-08
supersedes sha256:6b30e9a1...f205
```

Same valid time. Different knowledge time. Two different answers, both correct, and the difference between them is the entire reason the second clock exists.

| Flag combination | The question | Who asks it |
|---|---|---|
| `--valid-at T --known-at now` | What do we now believe was true at T? | An analyst preparing current material. |
| `--valid-at T --known-at K` | What did we believe at K about time T? | A reviewer auditing a document filed at K. |
| `--valid-at now --known-at now` | What do we currently believe about now? | The default, and the only question a single-clock store can answer. |
| `--known-at K` alone | The complete state of the workspace as of K. | Reconstruction of a release. |

**Defaults.** Both flags default to `now`, so a query with neither returns current belief about the present. That is the common case, and making it the default keeps the two-clock model out of the way of people who do not need it.

**Why the two flags are independent.** Somebody will propose collapsing them — "as of March 2027" seems like one idea. It is two, and the collapse loses the most useful query in the set. *What did we believe in March 2027 about 2022?* has both flags at different values, and it is exactly the question asked when a 2027 filing is challenged in 2030.

**Query result when nothing was known.** A query at a knowledge instant before any state existed returns an explicit empty result, not a null value:

```
$ wi as-of --valid-at 2026-06-01 --known-at 2026-12-01 \
           --node 0193a7c2-4d18-7f61-b209-3c7e0a4b9d12

WI_TEMPORAL_UNDEFINED
  No state of this node was known at 2026-12-01T00:00:00Z.
  Earliest knowledge instant: 2027-03-14T16:22:09Z.
```

Returning nothing and returning a value of zero are different answers. A store that renders the first as the second reports that the unemployment rate was zero, which is the failure mode this whole document exists to prevent one level down.

---

## 5. Temporal contradiction requires intersection

**Status: specified.** The constraint that enforces it is executable through `wi constraints`.

A contradiction is two claims that cannot both hold. Two claims about a metric with different values are not a contradiction unless their scopes intersect — and time is a scope.

**Not a contradiction.** A corporate tax rate of 21% valid `[2018-01-01, 2029-01-01)` and a rate of 24% valid `[2029-01-01, null)`. The intervals are adjacent and disjoint. Both statements are true, they describe a scheduled change, and a system that reports them as a conflict will be switched off within a week by whoever has to dismiss the warning every time they open the file.

**A contradiction.** A rate of 24% valid `[2029-01-01, null)` and a rate of 25% valid `[2029-01-01, null)`, both currently believed. The valid intervals intersect over an unbounded region and the values differ. Two open-ended rates for the same jurisdiction cannot both hold.

```python
def temporal_conflict(a: dict, b: dict) -> bool:
    """Two claims conflict only where their scopes actually meet.

    Order matters: knowledge time is checked first. Two states that were
    never believed at the same instant are a revision, not a disagreement,
    and reporting a revision as a conflict makes every correction look
    like an error.
    """
    if not overlaps(a["known_from"], a["known_until"],
                    b["known_from"], b["known_until"]):
        return False                      # a supersession, not a conflict
    if not overlaps(a["valid_from"], a["valid_until"],
                    b["valid_from"], b["valid_until"]):
        return False                      # different periods
    if not same_scope(a, b):              # spatial, population, metric
        return False                      # different subjects
    return values_differ(a, b)
```

**Why knowledge time is tested before valid time.** The revision in section 3 has identical valid intervals and different values — every ingredient of a contradiction except the one that matters. Their knowledge intervals do not intersect, so the workspace never held both beliefs simultaneously. Testing valid time first would report every correction the workspace has ever made as an unresolved conflict, and the conflict list would fill with entries whose only resolution is to delete history.

**Why intersection and not equality.** Intervals rarely match exactly. A claim about `[2022-01-01, 2023-01-01)` and one about `[2022-07-01, 2022-10-01)` describe overlapping periods at different resolutions, and if their values disagree over the overlap that is a genuine conflict. Equality would miss it; intersection catches it and reports the intersecting region:

```
$ wi constraints --check C014

C014  temporal_value_coherence          FAIL

  meaning.claim_atom:0193a7c2-...-9d12   4.1 percent
    valid [2022-01-01, 2023-01-01)   known [2027-03-14, open)
  meaning.claim_atom:0193a7c2-...-8e04   3.8 percent
    valid [2022-07-01, 2022-10-01)   known [2027-09-02, open)

  intersecting valid region: [2022-07-01, 2022-10-01)
  both currently believed; values differ over the intersection

  Repair: narrow one scope, revise one value, or record the pair as an
  open conflict with a basis.
```

Conflicts are preserved rather than auto-resolved. Law Q governs what happens next, and the mechanism is in [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md).

---

## 6. Archival authorship, not overwrite history

**Status: specified.**

Two designs produce a history. Only one of them is trustworthy.

| | Overwrite plus audit log | Archival authorship |
|---|---|---|
| Where the current value lives | A mutable row | The state whose `known_until` is open |
| Where the previous value lives | A log entry describing the change | A state, identical in kind to the current one |
| Can the previous state be verified? | No — the log holds a description, not the object | Yes — it hashes to the digest its verification was bound to |
| Can the log and the row disagree? | Yes, and nothing detects it | There is no second place for them to disagree |
| Cost of reconstructing March 2027 | Replay every log entry in order and hope none is missing | One query |

v6 uses archival authorship. A correction appends a new state and closes the previous state's knowledge interval. Nothing is edited in place, and the previous state remains a first-class object with its own digest, its own verifications and its own proof closure.

**Why the audit-log design fails specifically here.** An audit log is a *description* of a change. Descriptions drift from the thing they describe, and the drift is undetectable because there is nothing to compare the description against. Worse, the object a 2027 verification was bound to no longer exists after an overwrite — the digest it names cannot be reproduced, so a 2030 auditor asking whether the March 2027 filing was supported gets no answer at all. Under archival authorship the object still exists, still hashes to the same value, and the answer is a query.

**The cost, stated plainly.** Archival authorship keeps every state forever. A node revised twenty times holds twenty-one states. The `.wi/` object store is content-addressed, so identical states across branches are stored once, and the index carries the interval columns rather than the payloads — but the growth is real and it is monotone. That is the trade: storage in exchange for the ability to answer questions about the past without trusting a narrative of what happened.

**Redaction is the one exception, and it is not deletion.** A capsule may exclude a state from disclosure while retaining its commitment, so the recipient can verify that a state existed and was covered by the proof closure without seeing its content. Retention obligations and disclosure obligations are separate, and neither is served by destroying the object. The mechanism is in [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md).

---

## 7. Reconstructing a release

**Status: specified.** The underlying query is executable through `wi as-of`.

The most demanding thing the two clocks are asked to do is answer, years later, what a published document said and what supported it at the moment it was published.

A release manifest names a commit and a build instant. Both are enough to fix the knowledge axis: the commit fixes the graph root, and the build instant fixes what the workspace believed. Valid time is then whatever each claim in the release asserted, unchanged by anything that happened afterwards.

```
$ wi as-of --known-at 2027-03-14T18:40:00Z --release rel-2027-03-annual

release       rel-2027-03-annual
commit        sha256:5d2a91cf...e7f2
built         2027-03-14T18:40:00Z
claims        412 states resolved
  superseded since       37
  still current          375
  verifications binding  412 of 412 states present in the object store
```

Three numbers matter in that report and each is a separate fact.

**Thirty-seven states have been superseded since publication.** That is ordinary. A workspace that corrected nothing in two years has either published nothing consequential or has stopped checking.

**All 412 states are still present.** Archival authorship guarantees it. Under an overwrite design, thirty-seven of the objects the release's verifications were bound to would no longer exist, and the release would be unreconstructable in exactly the places where it had been revised — which is to say, in exactly the places somebody is asking about.

**Every verification still binds.** A verification names a `state_digest`. The digest of a superseded state is unchanged by the existence of its successor, so the 2027 verification of the 4.1% figure is still a valid, checkable statement about the 4.1% figure. It is not evidence that 4.1% is *currently* believed, and the report does not say it is.

The distinction that makes this useful:

| Question | Answer from the reconstruction |
|---|---|
| Was the report accurate when filed? | Yes — every claim was supported by a verification bound to the state that was published. |
| Is the report accurate now? | No — 37 of its claims have been superseded. |
| Was anything published that was unsupported at the time? | No — 412 of 412 bound. |
| Did the workspace know about the corrections before it filed? | No — every superseding state has a `known_from` after the build instant. |

The last row is the one that cannot be answered without a knowledge axis, and it is the one that decides whether a correction is a revision or a problem.

---

## 8. What the two clocks do not do

**Status: specified.**

| Not provided | Why not |
|---|---|
| A third clock for "decision time" | A decision is a node with its own knowledge interval. Adding an axis to every state to carry one node type's timestamp makes every query more expensive to serve one question. |
| Automatic valid-time inference from prose | A date mentioned in a sentence is not necessarily the scope of the claim. "In our 2027 report we found that 2022 was unusual" contains two years and neither is guaranteed to be the valid interval. Inferring it would author a scope nobody wrote. |
| Timezone-local intervals | All instants are UTC. A local interval is a rendering concern, and storing local times makes interval arithmetic depend on a jurisdiction's legislature. |
| Fractional-second knowledge ordering across machines | Knowledge instants come from the committing workspace's clock. Two workspaces are ordered by their federation import records, not by comparing wall clocks. Distributed ordering is in [`FEDERATION.md`](FEDERATION.md). |
| Retroactive knowledge editing | By construction. See section 1. |

---

## Related documents

- [`CONSTITUTION.md`](CONSTITUTION.md) — Law N, which this document implements
- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — the envelope carrying both intervals
- [`SEMANTIC_VERSION_CONTROL.md`](SEMANTIC_VERSION_CONTROL.md) — how a commit stamps knowledge time
- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — what happens to a preserved conflict
- [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) — retention, disclosure and redaction
- [`../v5/STALENESS.md`](../v5/STALENESS.md) — dependency-aware invalidation, which reads the knowledge axis
- [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) — dual identity and the object store

---

*A correction does not make the earlier report false. It makes it superseded, and those are different words because they are different facts.*

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
