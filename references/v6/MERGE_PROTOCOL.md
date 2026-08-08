# The Merge Protocol

Conflict-preserving semantic three-way merge. This is the document that makes collaboration possible on a graph where meaning has identity above wording.

**Status: executable in `scripts/wi.py`.**

`wi merge` and `wi conflicts` run today. They operate over `wi branch`, `wi commit` and `wi log`, and they refuse to produce a merged state that neither side asserted.

v5 established that a claim, a definition, an obligation and a canonical fact each have an identity that survives a rewrite — Law G in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md). The consequence nobody can avoid once that is true is this one: **two people can now edit the same meaning without touching the same bytes**, and the tool everyone reaches for to reconcile that — a text merge — cannot see it happen.

Read this with [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md), which supplies the delta classes this protocol reasons over, and with [`../v5/STALENESS.md`](../v5/STALENESS.md), which governs what a completed merge does to every proof downstream of it.

---

## Table of contents

1. Why text merge is insufficient
2. What is merged, and against what
3. The BASE / OURS / THEIRS resolution table
4. `MergeResult` and the conflict vocabulary
5. The prohibition on splitting the difference
6. Wording-only auto-merge and the reversed burden
7. The four adversarial fixtures
8. `wi conflicts` — the surface a human reads
9. What a merge does to proof state
10. Merge policy
11. Benchmarks
12. What is executable and what is specified

---

## 1. Why text merge is insufficient

**Status: executable in `scripts/wi.py`.**

A text merge reconciles two edits by asking one question: *did these two changes touch overlapping lines?* If they did not, both apply. If they did, a human is shown the region.

That question is a proxy. It was a good proxy for source code, where a line is close enough to a unit of behavior that overlap approximates interference. It is a poor proxy for prose, and it fails in both directions.

**It merges cleanly when it must not.** Two editors work on a grant narrative. One rewrites paragraph 14 in chapter 3, changing *"the program served 11,800 households"* to *"the program served 12,400 households"* after a corrected partner report. The other rewrites a bullet on slide 7 of the board deck, changing *"nearly twelve thousand families reached"* to *"more than twelve thousand families reached."* Different files, no overlapping lines, no conflict markers, a clean merge. The result is a release in which one number is 11,800 in a footnote, 12,400 in the narrative, and rendered two ways in the deck — and every text tool in the world reports success.

**It conflicts when there is nothing to decide.** The same two editors both reflow a paragraph. One wraps at 88 columns, the other at 100. Identical tokens, identical claims, identical anchors, three conflict markers and twenty minutes of someone's afternoon.

The failure has one cause. **A text merge reconciles renderings; the thing that has to be reconciled is meaning.** A rendering is where a meaning node happens to appear today, and v5 already made that relationship explicit: a `meaning.claim_atom` is bound to a `structure.paragraph` by a `renders_as` edge, and a single claim commonly renders in six places across three formats. Merging the renderings without merging the meaning leaves the graph internally inconsistent in a way that no diff tool is looking for and no reader can see.

**Why this is load-bearing.** Once meaning has identity, the invariant a merge must preserve is not *the file is well-formed* but *every logical id has exactly one current state, and that state is one somebody asserted.* Text merge cannot preserve that invariant because it does not know logical ids exist. A team that merges prose with a line-based tool is not merging carefully with a slightly wrong tool; it is performing an operation whose success condition has nothing to do with what they are trying to protect.

---

## 2. What is merged, and against what

**Status: executable in `scripts/wi.py`.**

A v6 merge is a three-way merge over **logical ids**, not over files, paragraphs, byte ranges or lines.

| Term | Is |
|---|---|
| `BASE` | The state of a logical id at the most recent common ancestor commit of the two branches |
| `OURS` | The state of that logical id at the tip of the branch being merged into |
| `THEIRS` | The state of that logical id at the tip of the branch being merged from |

`wi branch` creates a named line of work. `wi commit` records an immutable graph state and its parent. `wi log` walks the commit chain. `wi merge` finds the common ancestor by walking both parent chains, enumerates every logical id present in any of the three states, and classifies each one.

The unit is deliberate. A logical id is stable across rewording by construction — that is what Law G bought — so a claim moved from chapter 3 to chapter 9, reworded twice and rendered into a slide is still one id with one current state. Merging at that granularity means the merge is asking the question a reviewer would ask: *do these two branches now assert different things about the same subject?*

**Three families of node participate, and their merge behavior differs:**

| Family | Merge behavior |
|---|---|
| Meaning (`meaning.claim_atom`, `meaning.definition`, `meaning.obligation`, `meaning.constraint`, `meaning.term`) | Dimension-by-dimension comparison. This is where semantic conflicts arise. |
| Structure (`structure.chapter`, `structure.paragraph`, `structure.section`) | Ordering and containment merge. Two branches reordering the same sequence conflict; two branches adding to different sequences do not. |
| Canon (`canon.event`, `canon.character`, `canon.rule`, `canon.timeline_point`) | Same dimension comparison as meaning, evaluated inside `fictional_canon`, and never rendered as an externally verified fact. |

Verification nodes are not merged. A `verification.result` belongs to the state it was computed against, and a merge produces new states. Results are recomputed after the merge under [`../v5/STALENESS.md`](../v5/STALENESS.md), never carried across. That is section 9.

---

## 3. The BASE / OURS / THEIRS resolution table

**Status: executable in `scripts/wi.py`.**

For each logical id, the merge compares three states over the registered dimensions from [`../v5/SEMANTIC_IR.md`](../v5/SEMANTIC_IR.md) — `quantity`, `unit`, `temporal_scope`, `modality`, `certainty`, `attribution`, `negation`, `causal_force`, `geographic_scope`, `population_scope`, `exceptions`, `legal_force`, and the anchor and term bindings.

| BASE | OURS | THEIRS | Result | Reasoning |
|---|---|---|---|---|
| present | unchanged | unchanged | take BASE | Nobody touched it. |
| present | changed | unchanged | take OURS | One side moved; the other has no opinion. |
| present | unchanged | changed | take THEIRS | Symmetric with the row above. |
| present | changed | changed, **states identical** | take either | Both sides arrived at the same state. Convergence is not conflict. |
| present | changed | changed, **different dimensions** | merge dimension-wise | Ours moved `temporal_scope`, theirs moved `attribution`. Both apply; no dimension is written twice. |
| present | changed | changed, **same dimension, different values** | **CONFLICT** | Two assertions about one dimension of one meaning. This is the case the whole document exists for. |
| present | deleted | unchanged | take deletion | One side removed the claim; the other did not defend it. |
| present | deleted | changed | **CONFLICT** | One side removed the claim; the other revised it. Deleting somebody's revision is a decision, not a merge. |
| absent | added | absent | take OURS | New meaning on one side. |
| absent | absent | added | take THEIRS | Symmetric. |
| absent | added | added, **states identical** | take either, single id | Deterministic id derivation made both sides converge. |
| absent | added | added, **different states** | **CONFLICT** | Two independently created claims that the id assignment says are the same meaning. |

**The dimension-wise merge in row five is the row that earns the protocol.** Two editors working the same claim, one adding a temporal bound and one correcting the attribution, produce a merged state carrying both changes and no conflict — which a text merge could never do, because both edits are in the same sentence and therefore the same line. The merge is legitimate precisely because the two sides moved disjoint dimensions, and the engine can prove they were disjoint by comparing structured fields rather than strings.

**Row seven is the row people argue about.** OURS deleted the claim; THEIRS revised it. It would be easy to call deletion decisive — it is the destructive option, so surely it wins — or to call revision decisive, since somebody was actively working on it. Both are wrong for the same reason: they resolve a disagreement about whether an assertion belongs in the document by picking a rule, and no rule knows which editor read the retraction notice.

---

## 4. `MergeResult` and the conflict vocabulary

**Status: executable in `scripts/wi.py`.**

A merge returns a `MergeResult`. It is not a boolean, it is not a file, and it is not a merged state with markers embedded in prose.

```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class DimensionDelta:
    """One dimension of one logical id, and where the two branches put it."""
    dimension: str            # "quantity", "modality", "temporal_scope", ...
    base: Any
    ours: Any
    theirs: Any


@dataclass(frozen=True)
class SemanticConflict:
    """A disagreement the engine may not resolve. Carries both sides intact."""
    conflict_id: str
    kind: str                 # a SemanticConflictKind wire value, §4.1
    logical_id: str
    base_state: Optional[str]     # state digest, or None when BASE is absent
    ours_state: Optional[str]
    theirs_state: Optional[str]
    dimensions: List[DimensionDelta]
    ours_provenance: Dict[str, Any]    # branch, commit, actor, anchors, decisions
    theirs_provenance: Dict[str, Any]
    resolvable_by: List[str]           # "take_ours", "take_theirs", "author_new_state"
    note: str


@dataclass(frozen=True)
class MergeResult:
    merge_id: str
    base_commit: str
    ours_commit: str
    theirs_commit: str

    merged: List[str] = field(default_factory=list)          # logical ids, auto-merged
    conflicts: List[SemanticConflict] = field(default_factory=list)
    unaffected: Dict[str, Any] = field(default_factory=dict) # count + basis, §8.1

    proof_impact: Dict[str, Any] = field(default_factory=dict)
    committed: bool = False          # False whenever conflicts is non-empty

    def is_clean(self) -> bool:
        return not self.conflicts
```

**`committed` is `False` whenever `conflicts` is non-empty, and there is no flag that changes it.** A merge with unresolved semantic conflicts does not produce a commit. It produces a `MergeResult` a human works through. The alternative — write a state and mark the conflicted ids for later attention — creates a graph in which some current states were asserted by nobody, and there is no subsequent point at which that becomes visible.

### 4.1 `SemanticConflictKind`

Sixteen kinds. The vocabulary is closed, and a comparison the engine cannot place in it escalates rather than defaulting.

| Kind | Wire value | Arises when |
|---|---|---|
| Quantity | `quantity` | Both branches set a different number, magnitude, count or proportion on the same claim |
| Unit | `unit` | Both branches changed what the quantity counts or measures — households against individuals, dollars against 2019 dollars |
| Scope | `scope` | Both branches moved `geographic_scope` or `population_scope`, or one narrowed while the other broadened |
| Time | `time` | Both branches moved a date point |
| Entity | `entity` | Both branches substituted a different named person, organization or place |
| Attribution | `attribution` | Both branches changed who says, finds, funds or is responsible — including one side removing attribution entirely |
| Certainty | `certainty` | Both branches moved `modality` or `certainty` on the modal lattice, in different directions or to different rungs |
| Causality | `causality` | Both branches moved `causal_force` between `none`, `correlation`, `contribution` and `causation` |
| Definition | `definition` | Both branches rebound the same registered term |
| Obligation | `obligation` | Both branches changed whether a duty exists, on whom, or with what exceptions |
| LegalForce | `legal_force` | Both branches moved a statement between representation, warranty, disclaimer, marketing and none |
| Canon | `canon` | Both branches moved the same canonical fact inside a constructed world |
| Authority | `authority` | Both branches recorded incompatible authority grants over the same scope — see [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) §7 |
| Policy | `policy` | The two branches were committed under policies whose digests differ in a field governing this node |
| Evidence | `evidence` | Both branches rebound the same claim to different anchors, or to the same anchor at incompatible source versions |
| TemporalOverlap | `temporal_overlap` | Two obligations, effective periods or canon events now cover overlapping time with incompatible content |

**`temporal_overlap` is the one that is not a dimension comparison**, and it is here because it is the conflict class that survives every other check. Two branches each add an obligation — one says records are retained for five years from 2024, the other says seven years from 2026. Neither modified the other's node. Both merge cleanly on every row of section 3. The document now contains two live retention rules covering 2026 through 2029 with different answers, and nothing about either node is individually wrong. It is caught by evaluating the merged set, not the pairwise states.

**`policy` is the second one that is not about content.** A branch committed under `standard` and a branch committed under `regulated` can produce nodes whose merge is arithmetically clean and whose gate behavior is not. Merging them silently means a node that was never held to the stricter standard enters a workspace that claims it was. The merge names the policy divergence and the affected node set; it does not choose a policy.

---

## 5. The prohibition on splitting the difference

**Status: executable in `scripts/wi.py`.**

**No merge may produce a state that neither branch asserted.** There is no averaging, no rounding to a value both sides are near, no hedge synthesized to cover a disagreement, no range constructed from two points, and no confidence-weighted selection.

This is the single hardest rule in the protocol to hold, because splitting the difference is what a helpful system does.

### 5.1 The case, worked

Branch `partner-corrections` and branch `q3-narrative` both edit claim `c-0002`.

```
logical id   c-0002
realm        external_fact
predicate    serve
unit         households

BASE      quantity 11800   anchor a-0114  needs_assessment.txt@v3  bytes 9,004–9,050
                                          > "served 11,800 households between 2019 and 2022"

OURS      quantity 11800   unchanged
          (this branch did not touch the number; it added a temporal bound)

THEIRS    quantity 12400   anchor a-0140  partner_report.txt@v1    bytes 2,204–2,251
                                          > "12,400 households received services in the period"
```

That is not the interesting case. Now the symmetric one, which is the case this section is about:

```
BASE      quantity 11800   anchor a-0114  needs_assessment.txt@v3

OURS      quantity 11800   anchor a-0114  unchanged
                           + temporal_scope 2019-01-01 .. 2022-12-31  (closed)

THEIRS    quantity 12400   anchor a-0140  partner_report.txt@v1
                           temporal_scope unchanged (open, "since 2019")
```

Ours moved `temporal_scope`. Theirs moved `quantity` and `evidence_binding`. Under section 3 row five these are disjoint dimensions, so the dimension-wise merge applies and produces:

```
MERGED    quantity 12400   anchor a-0140
                           temporal_scope 2019-01-01 .. 2022-12-31
```

**And that merged state is illegal**, even though every individual step was correct. The anchor `a-0140` supports 12,400 over an open period beginning in 2019. Nothing in the workspace supports 12,400 *within a closed 2019–2022 window*. The dimension-wise merge composed two states nobody wrote into a third state nobody checked, and it would have carried `a-0140` forward as its support.

So the rule has a second half, and it is what makes the first half enforceable:

> **A dimension-wise merge is permitted only when the merged state's evidence bindings support the merged state.** Where they do not, the result is a conflict of kind `evidence`, and the merge stops.

### 5.2 What is forbidden, exactly

Given `OURS: 11,800` and `THEIRS: 12,400`, every one of the following is an illegal merge output:

| Illegal output | Why |
|---|---|
| `approximately 12,000` | Neither branch asserted it. No anchor supports it. The engine invented a third claim and would then have to invent a certainty qualifier to make it defensible. |
| `between 11,800 and 12,400` | A range is a different claim from a point value, with a different evidentiary burden. Neither branch made it. |
| `12,100` | Arithmetic on two assertions is not an assertion. |
| `12,400` because THEIRS is newer | Recency is not evidence. The later commit may be the stale one — an author working from an older partner report on a branch cut last week. |
| `12,400` because its anchor is a more recent source version | Source recency is not correctness either, and this rule would let any partner overwrite any figure by re-sending a file. |
| `11,800` because OURS is the branch being merged into | Direction of merge is an accident of who typed the command. |
| `12,400 (revised from 11,800)` | A parenthetical is prose. It does not change `quantity`, so the graph still holds one value while the rendering shows two, which is worse than either. |

**Why this is load-bearing.** "Approximately 12,000" is the most dangerous output this system could produce, and it is dangerous in a way that is nearly impossible to detect afterward. It reads as careful. It is hedged, so it survives casual scrutiny. It is close to both inputs, so nobody reviewing the diff feels alarmed. And it is **unsupported by any source in the workspace**, so the claim now in the document is one no anchor bears out, carried by a proof chain the merge itself constructed. A wrong number an author chose is a wrong number somebody can be asked about. A number the merge algorithm synthesized has no author at all, and the first time anyone discovers that is when a reviewer asks where it came from.

Under Law E in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md), uncertainty resolves toward less claiming, never toward a plausible middle. A merge conflict is the system under-claiming correctly: it says *two people asserted different things and I am not entitled to decide*, which is true.

### 5.3 The conflict object emitted instead

```json
{
  "conflict_id": "mc-0007",
  "kind": "quantity",
  "logical_id": "c-0002",
  "base_state":   "sha256:4b19c0d7e2a5f83b16c04d9e7a2b8c35de60f19a4c7b2e8d0f3a6b9c1d4e7f20",
  "ours_state":   "sha256:8e02f1a4c6b9d03e5f7a1b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e",
  "theirs_state": "sha256:1f77b3a05c8d26e4f9a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4",

  "dimensions": [
    {"dimension": "quantity",      "base": 11800, "ours": 11800, "theirs": 12400},
    {"dimension": "evidence_binding",
     "base":   "a-0114 needs_assessment.txt@v3 bytes 9004-9050",
     "ours":   "a-0114 needs_assessment.txt@v3 bytes 9004-9050",
     "theirs": "a-0140 partner_report.txt@v1  bytes 2204-2251"}
  ],

  "ours_provenance": {
    "branch": "q3-narrative",
    "commit": "wc-0188",
    "actor": {"type": "team_member", "id": "a.rivera@example.org"},
    "decision": "d-0104",
    "anchor_quote": "served 11,800 households between 2019 and 2022"
  },
  "theirs_provenance": {
    "branch": "partner-corrections",
    "commit": "wc-0191",
    "actor": {"type": "team_member", "id": "j.okafor@example.org"},
    "decision": "d-0119",
    "anchor_quote": "12,400 households received services in the period"
  },

  "resolvable_by": ["take_ours", "take_theirs", "author_new_state"],
  "note": "Both branches bind c-0002 to a supporting anchor, and the two sources disagree. This is a source conflict surfaced by a merge, not a merge defect. Resolving it by choosing a branch selects which source the document relies on; that choice is recorded as a decision under Law J."
}
```

Three properties of that object matter.

**Both anchors are carried, with their quoted bytes.** The person resolving this does not have to go find out what each side was reading. The disagreement between the two sources is the actual problem, and the merge's job is to put it in front of somebody with both quotations visible.

**`resolvable_by` includes `author_new_state`.** Taking a side is not always right. The correct resolution here may well be *"the program served 11,800 households in the 2019–2022 window and 12,400 through Q2 2024"* — two claims, two anchors, no conflict. The merge cannot write that sentence, and it must not pretend the only options are the two it was handed. Offering accept-or-reject on a disagreement about the world frames a factual question as a preference.

**`note` states what kind of problem this is.** A source conflict surfaced by a merge is not a merge failure, and telling the operator that keeps them from looking for a bug in the tool.

---

## 6. Wording-only auto-merge and the reversed burden

**Status: executable in `scripts/wi.py`.**

Two branches may edit the surface text of the same claim without disagreeing about anything. That case is common, it is safe, and refusing to merge it would make the protocol unusable — a system that conflicts on every copyedit is one somebody stops branching in.

So `wording_only` merges automatically. The burden is what changes.

> **In a text merge, sameness is assumed and difference must be detected. In a semantic merge, difference is assumed and sameness must be proven.**

The proof is `compare_claim_states` from [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) §3, run twice — BASE against OURS, and BASE against THEIRS — with the auto-merge permitted only when **both** comparisons return an empty `deterministic` list and no unresolved escalation.

```python
def may_auto_merge_wording(base, ours, theirs, provider_available):
    """Prove that neither branch moved a registered dimension.

    Returns (True, evidence) or (False, reason). Never returns True on the
    strength of the surfaces being similar — similarity is not the test.
    """
    a = compare_claim_states(base, ours)
    b = compare_claim_states(base, theirs)

    # Any structural difference in any registered dimension removes
    # wording_only from the table before a provider is consulted.
    if a["deterministic"] or b["deterministic"]:
        return False, "a registered dimension moved on at least one branch"

    # Anchors must still bind, and to the same evidence.
    if ours["anchors"] != base["anchors"] or theirs["anchors"] != base["anchors"]:
        return False, "evidence binding changed; that is an evidence conflict"

    # Paraphrase equivalence is judged, not computed. Law E: an escalation
    # nobody can resolve does not become wording_only.
    if not provider_available:
        return False, "paraphrase equivalence unresolved; no judgment provider"

    for j in a["judged"] + b["judged"]:
        if j.result != "equivalent":
            return False, "paraphrase equivalence not established: %s" % j.result

    # Both branches reworded the same meaning. Still two surfaces, one meaning.
    return True, {
        "basis": "judged",
        "judgments": [j.judgment_id for j in a["judged"] + b["judged"]],
        "chosen_surface": "requires_selection",   # §6.1
    }
```

### 6.1 Two surfaces, one meaning, and which words survive

An auto-merged `wording_only` conflict still leaves a question the engine may not answer: **whose sentence appears in the document.**

The meaning merged. The prose did not. Two people wrote two sentences and both are correct.

The engine's rule is narrow and boring on purpose:

| Situation | Result |
|---|---|
| Only one branch changed the surface | That surface. |
| Both changed the surface, one is inside an `authorship.protected_span` | The protected surface, always. A protected span is the author placing text beyond a machine's reach; a merge is a machine. |
| Both changed the surface, neither protected | **`wording_only` selection required** — reported in `MergeResult.conflicts` with kind `wording_only_selection`, resolvable only by `take_ours`, `take_theirs` or `author_new_state`. |

That third row means the merge is not clean, and it means so honestly. It is the cheapest conflict in the system — no evidence is at stake, no dimension moved, and every option is defensible — and it is still a conflict, because choosing whose voice appears in a document is an authorship decision under Law A and the system does not have standing to make it.

**Why the burden is reversed.** The failure modes are not symmetric. A wrongly-detected difference costs a review that resolves in seconds. A wrongly-assumed sameness silently merges a semantic change into a document under a classification that carries the old proofs forward untouched — which is the whole reason `wording_only` is the classification an over-eager system reaches for, as [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) §1 already names. In a merge that failure is worse than in a diff, because a diff shows a human the before and after and a merge is the operation people run in order to *not* read everything.

---

## 7. The four adversarial fixtures

**Status: executable in `scripts/wi.py`. These four are gold cases in the merge benchmark suite of section 11.**

Each is a case where a line-based diff and a semantic diff give opposite answers. Two of them a text merge treats as dangerous and are safe; two it treats as safe and are not.

### 7.1 Large text change, same meaning

```
BASE    The program, over the course of the period running from 2019 through
        the end of 2022, provided direct services to a total of 11,800
        households located within the seven-county declared service area.

OURS    Between 2019 and 2022 the program served 11,800 households across
        seven counties.

THEIRS  unchanged
```

| Tool | Answer |
|---|---|
| Line diff | Whole paragraph replaced. 32 words changed. Large change. |
| Semantic diff | `deterministic: []`. `quantity` 11800, `unit` households, `temporal_scope` 2019-01-01..2022-12-31 closed, `geographic_scope` seven-county service area, `modality` is, `negation` false — every registered dimension identical. `compression` escalated to judgment. |
| Merge | Auto-merges under §6 when the paraphrase judgment returns `equivalent`. Proofs carry forward. Anchor `a-0114` still binds. |

**The point:** the size of a text change carries no information about whether meaning moved. This is the copyedit that makes prose better, and a system that conflicts on it is a system people route around.

### 7.2 One-word change, different meaning

```
BASE    Partners should share intake data monthly.

OURS    Partners shall share intake data monthly.

THEIRS  unchanged
```

| Tool | Answer |
|---|---|
| Line diff | One word. Six characters. Trivial change. |
| Semantic diff | `obligation_added` + `certainty_strengthened`. `modality` moves `should` → `must` on the ordered lattice. `legal_force` moves from `none` to a binding representation. |
| Merge | Applies, because THEIRS did not touch it — but it is **flagged for review on the merge report** and never auto-accepted, and every proof bound to the hedged form is void under [`../v5/STALENESS.md`](../v5/STALENESS.md) §3. In `regulated` mode this is a `require_human` class before the merge commits. |

**The point:** this is a one-word merge that creates a contractual duty. A text merge applies it without comment because there is nothing to conflict with. The merge report is the only place anybody finds out.

### 7.3 Temporal broadening — `in 2022` → `since 2022`

```
BASE    Filings rose in 2022.

OURS    Filings rose since 2022.

THEIRS  unchanged
```

| Tool | Answer |
|---|---|
| Line diff | Two characters. `in` → `since`. Below most reviewers' threshold entirely. |
| Semantic diff | `temporal_scope_changed`. The range type moves from a closed point-year to an open range with no end. |
| Merge | Applies, and the anchor is **void**. The source states a figure for calendar 2022. It says nothing about 2023, 2024 or any month since. The claim drops to `needs_source`. |

**The point:** the edit reads as a stylistic preference and is a scope broadening. An open range asserts something about every period after the start, including periods that had not happened when the source was written. This is the class of change that gets made during a light copyedit pass eighteen months after a document was first checked, and it is invisible in every diff tool ever shipped.

### 7.4 Legal force — `should` → `shall`, from both sides

```
BASE    The applicant should retain records for seven years.

OURS    The applicant shall retain records for seven years.

THEIRS  The applicant should retain records for seven years, except where
        superseding state law provides a shorter period.
```

| Tool | Answer |
|---|---|
| Line diff | Overlapping edit on one line. Conflict, with markers, resolved by whoever is at the keyboard. |
| Semantic diff | OURS: `obligation_added`, `modality` `should` → `must`. THEIRS: `exceptions` gains a carve-out; `modality` unchanged. **Different dimensions.** |
| Merge | Section 3 row five says these are disjoint and dimension-wise merge applies. Section 5.1's second half then stops it: the merged state is a **binding** obligation carrying an exception whose scope neither branch evaluated against a binding duty. Result: `SemanticConflict` of kind `obligation`, with both dimension deltas carried. |

**The point:** this is the case that shows dimension-wise merge is not a license. Two disjoint edits composed into a state that is legally different from either input, and the difference is exactly the kind a court reads closely. The engine detects it because `legal_force` moving and `exceptions` moving are both registered dimensions on the same node, and a merged state that changes what binds *and* what is carved out of it is a state a human has to approve.

**A text merge would have shown a conflict here and been right for the wrong reason** — it conflicts because the characters overlap, and it would have conflicted identically if THEIRS had only fixed a typo. Being right by accident is not a property you can build on.

---

## 8. `wi conflicts` — the surface a human reads

**Status: executable in `scripts/wi.py`.**

`wi merge` produces the `MergeResult`. `wi conflicts` renders it for the person who has to decide.

```
$ python3 scripts/wi.py conflicts

MERGE  m-0031   partner-corrections → q3-narrative
       base wc-0166 · ours wc-0188 · theirs wc-0191

  merged automatically      412 logical ids
       dimension-wise         38   disjoint dimensions on the same node
       one-sided             361   only one branch moved
       wording_only           13   paraphrase equivalence judged · 13 records

  conflicts                   3

  ─────────────────────────────────────────────────────────────────────────
  mc-0007   quantity   c-0002   "the program served N households"

    ours     11,800    q3-narrative @ wc-0188 · a.rivera
             anchor a-0114  needs_assessment.txt@v3  bytes 9,004–9,050
             > "served 11,800 households between 2019 and 2022"

    theirs   12,400    partner-corrections @ wc-0191 · j.okafor
             anchor a-0140  partner_report.txt@v1    bytes 2,204–2,251
             > "12,400 households received services in the period"

    Two sources disagree. This is a source conflict, not a merge defect.
    No merged value is available: neither branch asserted a third number,
    and no anchor in this workspace supports one.

    choices  (a) take ours     rely on needs_assessment.txt@v3
             (b) take theirs   rely on partner_report.txt@v1
             (c) author        write a state both sources support, e.g. two
                               claims with two windows and two anchors

  ─────────────────────────────────────────────────────────────────────────
  mc-0008   obligation   ob-0014   record retention

    ours     modality should → must          (binding duty created)
    theirs   exceptions += "superseding state law provides a shorter period"

    Different dimensions, so these would merge. The composed state is a
    BINDING duty carrying an exception that was written against advisory
    language. Neither branch evaluated that combination.

    choices  (a) take ours     binding, no exception
             (b) take theirs   advisory, with exception
             (c) author        binding with an exception scoped to it

  ─────────────────────────────────────────────────────────────────────────
  mc-0009   wording_only_selection   c-0018

    Both branches reworded the same claim. Paraphrase equivalence judged:
    equivalent (jr-0233, jr-0234). No dimension moved. No proof is at stake.
    Whose sentence appears is an authorship decision.

    ours     "Median wait times fell across all seven counties."
    theirs   "Wait times fell in every county in the service area."

  ─────────────────────────────────────────────────────────────────────────

  unaffected   1,806 claim atoms · 1,794 anchors · 11 release artifacts
               basis: present and identical in BASE, OURS and THEIRS

  This merge did not commit. 3 conflicts are open.

Checks run: dimension comparison over 13 registered dimensions · anchor binding
comparison · temporal overlap scan · policy digest comparison.
Not run: paraphrase equivalence for 2 pairs (no judgment provider on this
surface; both are held as conflicts, not merged).
```

### 8.1 The unaffected block

The `unaffected` line is printed on every merge report, with its basis, for the same three reasons it is printed on every impact report in [`../v5/STALENESS.md`](../v5/STALENESS.md) §4.1.

It is the only way a reader can tell *the merge found three problems* from *the merge only looked at three things*. It is what lets somebody merge at 2 a.m. and know the other 1,806 claims are untouched. And it is a `measured` statement under [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) — a count against a stated population — so it carries the basis that produced it, which here is the strongest basis available: those nodes are byte-identical in all three states.

---

## 9. What a merge does to proof state

**Status: executable in `scripts/wi.py`.**

A merge produces new states, and Law I is unconditional: a proof belongs to the state it was computed against.

| Merge outcome for a node | Proof consequence |
|---|---|
| Taken from BASE unchanged | Proofs carry forward. Nothing moved. |
| One-sided change | Same as any accepted proposal — reclassified by `compare_claim_states`, proofs invalidated per the edge policy table in [`../v5/STALENESS.md`](../v5/STALENESS.md) §3. |
| Dimension-wise merge | **All proofs on the node are stale.** The merged state was verified by nobody: OURS was checked, THEIRS was checked, the composition was not. |
| `wording_only` auto-merge | Proofs carry forward, and the merge records *why* — the two paraphrase judgment ids and the surface selection. This is the narrow Law I exception, and it is narrow because both comparisons had to return empty. |
| Conflict resolved by `take_ours` / `take_theirs` | Proofs from the chosen branch carry forward. The decision record binds to the chosen state digest. |
| Conflict resolved by `author_new_state` | New state, no inherited proofs, full re-verification. |

**The third row is the one worth stating twice.** A dimension-wise merge is the protocol's most useful move and its most dangerous: it produces a state that is correct in each part and unverified as a whole. Carrying proofs across it would mean a claim whose quantity was checked against one source and whose temporal scope was checked against another, presented as a single verified assertion that no single check ever evaluated. So the merge marks it stale and `wi merge` reports how many nodes it did that to.

The merge itself is a single transaction, for the reason [`../v5/STALENESS.md`](../v5/STALENESS.md) §2 gives about invalidation: a crash partway through leaves some nodes merged and others not, and a partially merged graph is a state nobody designed and nobody can reason about. The merge commits entirely or not at all.

---

## 10. Merge policy

**Status: executable in `scripts/wi.py`.**

```yaml
# .wi/policy/merge.yaml
merge:
  auto_merge:
    one_sided: true
    dimension_wise: true            # subject to the §5.1 evidence-support rule
    wording_only: judged_only       # never on an unresolved escalation
    format_only: true
    whitespace_only: true
    punctuation_only: outside_quoted_spans

  always_conflict:
    - obligation
    - legal_force
    - authority
    - definition
    - evidence
    - canon
    - policy

  require_human:
    - quantity
    - unit
    - scope
    - time
    - entity
    - attribution
    - certainty
    - causality
    - temporal_overlap
    - wording_only_selection

  on_policy_divergence: conflict    # never: take_stricter, never: take_ours
  on_unresolved_escalation: conflict
  record_as: automated_policy       # never as the human who ran wi merge
```

**`always_conflict` is not the same list as `require_human`, and the difference is deliberate.** `require_human` means a person decides. `always_conflict` means a person decides *and the engine will not propose a resolution*, because for those seven kinds even suggesting an answer is a form of deciding. A merge tool that offers a default on an obligation change will get that default accepted, and the record will show a human accepting it, and nobody will be able to say afterward whether anyone read it.

**`on_policy_divergence: conflict`, and specifically not `take_stricter`.** Taking the stricter policy sounds safe and is not: it produces a workspace holding nodes to a standard nobody in the merge chose, and the gate verdicts that follow are computed under a policy no commit recorded. Two branches under two policies is a governance question, and governance questions do not have algorithmic answers.

**In `strict` and `regulated` mode, four rules hold absolutely**, mirroring the auto-accept rules in [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) §6:

1. No claim-changing merge auto-commits. Any conflict outside the presentation tier requires a decision.
2. No evidence rebinding auto-merges, in either direction, ever.
3. No waiver merges. A waiver is a person choosing to proceed past a hold, bound to an exact claim state; a merge changes claim states, so every waiver whose bound state moved is stale on the merged side and must be re-taken.
4. No `human-declared` observation is merged into an `external_fact`. If OURS holds a claim in `author_observation` and THEIRS holds the same logical id in `external_fact`, that is a realm conflict and it goes to a human. The realm rule from [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) §6 is not a merge-time convenience.

---

## 11. Benchmarks

**Status: specified.** The gold cases are shipped; the scoring harness for the judged tier is defined here and unimplemented.

Merge is scored the way the diff engine is scored in [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) §10: **per-conflict-kind confusion matrices, published individually, with no blended number.**

| Generated case | Asserts |
|---|---|
| Disjoint dimensions on one node, evidence supports the composition | Merges dimension-wise; exactly one new state; all proofs stale |
| Disjoint dimensions on one node, evidence does **not** support the composition | Conflict of kind `evidence`; no state written |
| Same dimension, same value, both branches | Convergence, not conflict; one merged id |
| Same dimension, different value | Conflict; both anchors carried with quoted bytes; no synthesized value anywhere in the output |
| OURS deletes, THEIRS revises | Conflict, never a silent deletion |
| Two obligations with overlapping effective periods, neither node modified | `temporal_overlap` conflict, detected on the merged set |
| Two branches under `standard` and `regulated` | `policy` conflict; no policy is selected |
| Paraphrase pair with no provider configured | Conflict, never `wording_only` |
| Protected span reworded on both sides | Protected surface wins; no selection conflict raised |
| 40,000-node graph, 3 conflicting ids | Exactly 3 conflicts; unaffected count exact; walk stays index-driven |

**The assertion that matters most is negative and it is checked on every case:** *no output state has a value that is absent from BASE, OURS and THEIRS.* That is a set-membership test over every dimension of every merged node, it is cheap, and it is the mechanical form of section 5. A merge engine that passes every other test and fails this one has invented a claim, and it will do it quietly.

---

## 12. What is executable and what is specified

| Mechanism | Status |
|---|---|
| `wi branch`, `wi commit`, `wi log`, common-ancestor resolution | Executable in `scripts/wi.py` |
| Three-way merge over logical ids, the §3 resolution table | Executable in `scripts/wi.py` |
| Dimension-wise merge with the evidence-support precondition | Executable in `scripts/wi.py` |
| `MergeResult`, `SemanticConflict`, the sixteen conflict kinds | Executable in `scripts/wi.py` |
| The no-invented-state rule and its set-membership assertion | Executable in `scripts/wi.py` |
| `wi merge`, `wi conflicts`, the unaffected block with basis | Executable in `scripts/wi.py` |
| Temporal overlap detection over the merged set | Executable in `scripts/wi.py` |
| Policy divergence detection over commit policy digests | Executable in `scripts/wi.py` |
| Merge policy enforcement, including the four strict-mode rules | Executable in `scripts/wi.py` |
| Paraphrase equivalence for `wording_only` auto-merge | Specified — requires the provider contract in [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) |
| Scoring harness for judged conflict kinds | Specified |
| Merge across media, spreadsheet and audio anchors | Specified — awaiting the adapters in [`../v5/EVIDENCE_ANCHORS.md`](../v5/EVIDENCE_ANCHORS.md) |

---

## Related documents

- [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) — simulating a merge before running it, and the repair frontier it produces
- [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) — what a merged state owes before it can be released
- [`ARGUMENT_GRAPH.md`](ARGUMENT_GRAPH.md) — merging arguments, premises and defeaters
- [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) — the delta classes and `compare_claim_states`
- [`../v5/STALENESS.md`](../v5/STALENESS.md) — the edge policy table a merge's output propagates through
- [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) — logical ids, state digests and the node families that merge
- [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — Law A, Law E, Law G, Law I and Law J
- [`../v4/PROPOSAL_PROTOCOL.md`](../v4/PROPOSAL_PROTOCOL.md) — the proposal shape a conflict resolution produces
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
