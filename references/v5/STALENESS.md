# Staleness and Impact

The dependency system. This is what turns verification from a periodic audit into a build system.

**Status: executable — `wi impact`.**

A build system does not recompile a project because a comment changed in an unrelated file, and it does not ship a binary built from source that has since moved. It knows what depends on what, it computes the difference, and it rebuilds the minimum. Verification has never worked that way. It has worked the way documentation review works: somebody remembers, or nobody does.

Law I in [`CONSTITUTION.md`](CONSTITUTION.md) states the rule — *a proof belongs to a specific source state, anchor, claim state and transformation state.* This document is the machinery.

---

## 1. The problem, stated concretely

A source changes. One file, on a Tuesday, from a partner or a federal agency or an author's own spreadsheet.

The system must now know, without anyone remembering:

| Question | Why it cannot be answered by search |
|---|---|
| Which **anchor** changed? | Anchors are byte ranges into an exact source version. A search finds text; it does not find which of eleven anchors into that file crossed the edited region. |
| Which **claim atoms** depend on that anchor? | The claim's wording may share no vocabulary with the source passage. Support is a recorded edge, not a resemblance. |
| Which **paragraphs** render those claims? | The same claim renders in a narrative paragraph, a slide bullet and a caption, in three different sentences. |
| Which **chapters** include those paragraphs? | Structure is nested and reused; a paragraph may be included in two documents. |
| Which **decks, scripts, posts, charts and videos** derive from the claim? | Derivatives are usually in other files, other formats, and often other repositories. Nothing in them contains the claim's text. |
| Which **releases** are now stale? | A release artifact is bytes on disk that have not changed. Its *attestation* is what stops being true. |

Search answers none of these, and the reason is not that search is weak. It is that every one of these questions is about a **recorded dependency**, and a dependency that was never recorded cannot be searched for. The graph in [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) exists so that these six questions are traversals.

---

## 2. The invalidation algorithm

**Status: executable in `scripts/wi.py`.**

1. **Compute the new immutable state digest.** `sha256` over the raw bytes for a source; over the canonical payload for a semantic node. The raw-bytes rule from [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) applies without exception.
2. **Compare with the prior digest.** Equal digests terminate the algorithm immediately. A re-save that changes nothing invalidates nothing, and this is the most common case in daily work.
3. **Classify the change.** For a source, compute the changed byte regions. For a claim atom, run `compare_claim_states` from [`SEMANTIC_DIFF.md`](SEMANTIC_DIFF.md) and take the delta classes.
4. **Traverse outgoing `depends_on`, `derived_from` and `renders_as` edges** from the changed node, plus every evidential edge that terminates on it.
5. **Apply the per-edge invalidation policy** at each hop — `hard`, `review`, `soft` or `none` — from the table in section 3. The policy, not the traversal, decides what happens.
6. **Mark dependent verification nodes stale**, writing a `verification.invalidation` record that names the cause state, the affected state and a reason code. Staleness is recorded, never inferred at read time.
7. **Mark release artifacts outdated** if their proof closure contains any stale node. The artifact's bytes are untouched; its attestation is what fails.
8. **Produce the minimum repair frontier** — the smallest set of nodes a human must actually revisit for every downstream state to become current again.

```python
def invalidate(changed_state, graph, policy):
    """Reverse-closure walk from one changed state. Returns the frontier."""
    queue   = deque([(changed_state, "origin", 0)])
    visited = set()                      # keyed by (state_digest, edge_relation)
    stale   = []
    frontier = []

    while queue:
        state, via, depth = queue.popleft()
        key = (state.digest, via)
        if key in visited:               # a diamond dependency is walked once
            continue
        visited.add(key)

        for edge in graph.edges_into(state):          # idx_edge_in, both directions indexed
            effect = policy.effect_of(edge.relation, edge.invalidation, change_class)
            if effect == "none":
                continue                              # illustrates, rejected_by, ...
            head = graph.current_state(edge.from_logical_id)
            if effect == "hard":
                stale.append(record(head, cause=state, reason="WI_ANCHOR_STALE"))
            elif effect == "review":
                stale.append(record(head, cause=state, reason="WI_REVIEW_REQUIRED"))
            if graph.is_repair_site(head):            # a node a human can actually fix
                frontier.append(head)
            queue.append((head, edge.relation, depth + 1))

    return {"stale": stale, "frontier": minimize(frontier), "visited": len(visited)}
```

**Two things a real implementation must add that this pseudocode omits.**

**State-version boundaries.** The walk above reads `graph.current_state(...)` mid-traversal. In a workspace where anything can change while the walk runs, that produces a result computed against several different graph states at once — internally inconsistent, and wrong in a way that does not reproduce. A real implementation pins the walk to a single graph version at entry and reads only that version, so the impact report describes one state of the world rather than a smear across several.

**Transaction safety.** Steps 6 and 7 write invalidation records and update release status. A crash between them leaves stale claim atoms under a release still marked current — precisely the failure this document exists to prevent, produced by the machinery meant to prevent it. Invalidation must be a single transaction: the walk commits entirely or not at all, and a partially applied invalidation is never a visible state.

---

## 3. Per-edge invalidation policy

**Status: executable in `scripts/wi.py` for edges over text-derived nodes.**

The traversal reaches many nodes. The policy decides which of them changed status. Edge semantics come from [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md); this table is what happens when the tail moves.

| Edge | Tail changes → head becomes | When it provably does **not** propagate |
|---|---|---|
| `supports` | `hard` — the head's supported state is void | The anchor's byte range lies entirely outside every changed region of the source |
| `contradicts` | `hard` — the conflict is re-evaluated from scratch | Never. A conflict whose basis moved must be re-decided. |
| `qualifies` | `hard` — the qualified claim loses its scope guarantee | The constraint's semantic payload is unchanged and only its surface wording moved |
| `cites` | `hard` — citation resolution re-runs | The citation resolves to a `source.artifact` identity, and only a non-current version changed |
| `derived_from` | `review` | The delta class is presentation-tier and the derived node carries no dimension the delta touched |
| `summarizes` | `review` — a summary may not survive a change in what it summarizes | Same condition as `derived_from` |
| `translates` | `review` | Never automatic — see [`../v4/LANGUAGE_TIERS.md`](../v4/LANGUAGE_TIERS.md); a translation's equivalence is judged, not computed |
| `renders_as` | `review` — the rendering may no longer express the claim | The delta is `wording_only` **and** the rendering does not quote the changed span |
| `asserted_in` | `review` | The structural location is unchanged and the claim's realm did not move |
| `depends_on` | `review` | The dependency is declared over a specific field and that field did not change |
| `uses_term` | `review` | The term's `definition_state` digest is unchanged |
| `defines` | `review` on every `uses_term` site | The definition text changed but the `definition_state` digest did not — a formatting edit |
| `broadens` | `hard` | Never. A claim getting stronger always re-enters proof. |
| `narrows` | `review` | The narrowed claim's evidence was already sufficient for the broader form |
| `built_from` | `hard` — the release artifact's attestation is void | No input state in the closure moved |
| `illustrates` | `none` | Always. Nothing in a proof depends on it. |
| `rejected_by` | `none` | Always. A rejected proposal applies to nothing. |

### 3.1 The load-bearing non-propagation case

**An anchor whose byte range lies outside the changed region of a source does not go stale.**

A partner sends a corrected needs assessment. The correction is on page 9. The workspace holds eleven anchors into that file, two of which fall inside the edited region and nine of which do not. A naive implementation marks all eleven stale, because the source version digest changed and every anchor names that digest.

That implementation is technically defensible and practically fatal. It produces nine false positives on a routine document update, the author re-anchors nine claims that were never in question, and after the third such update they stop running the tool.

The engine therefore compares byte regions, not just digests. The nine anchors outside the changed regions are **rebound to the new source version automatically and marked `verified`**, with the rebind recorded — the quoted bytes are identical, at a possibly different offset, in the new version. The two inside the changed regions are `WI_ANCHOR_STALE` and require a decision. This is the narrow exception Law I permits, and it is narrow by construction: it applies only where the engine can *prove* the evidence text did not move, by comparing the bytes it already hashed.

**Why this is load-bearing.** A checker that cries wolf is one somebody switches off, and the real rule goes with it. Every false positive spends the author's willingness to trust the next finding, and that budget is small and does not refill.

---

## 4. The minimum repair frontier

**Status: executable in `scripts/wi.py`.**

Never "reverify the whole book." That instruction is a refusal to compute dressed as diligence.

```
$ python3 scripts/wi.py impact --source hud_income_limits_2026.csv

Source hud_income_limits_2026.csv: @v3 → @v4
  raw bytes changed: sha256:0a7c…d411 → sha256:e2b8…9f05
  changed regions: 1  (bytes 41,208–41,246 — one row, one column)

Affected:
    3  anchors                       a-0771, a-0772, a-0779
    2  claim atoms                   c-0418, c-0419
    5  paragraphs                    p-0902, p-0903, p-1140, p-1141, p-1477
    3  chapters                      ch-07, ch-09, ch-14
    1  slide                         deck-board-q3/slide-11
    4  social derivatives            x-0233, li-0088, ig-0104, nl-2026-03
    2  release artifacts             dist/policy_book.pdf, dist/board_deck.pdf

Unaffected:
 1,814  claim atoms                  no dependency path from the changed regions
 1,806  anchors                      byte ranges outside the changed regions;
                                     all rebound to @v4 automatically, verified
    11  release artifacts

Cheapest safe repair — 3 steps:

  1. rerun_check  c-0418, c-0419   numeric check against a-0771 @v4
                                   the bound figure moved 51,200 → 52,650
  2. accept_proposal pr-0644       update both atoms to 52,650
                                   (drafted; 5 renderings follow automatically)
  3. rebuild_target policy_book, board_deck
                                   re-attest both artifacts

Gate consequence under `strict`: HOLD (2 claims stale).
Estimated repair cost: 3 operations · 1 human decision.
```

### 4.1 Why the unaffected count is printed

The `Unaffected` block is the more important half of that output, and it is printed on every impact report.

Three reasons, in order of weight. First, it is the only way a reader can tell the difference between *the engine found two problems* and *the engine only looked at two things*. A report listing damage with no denominator is unfalsifiable. Second, it makes the tool usable at 2 a.m. on a deadline: "1,814 claim atoms unaffected" is what allows an author to ship the other fourteen chapters tonight instead of re-reading a book. Third, it is a `measured` statement under [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md) — a count against a stated population with a stated basis — and it must therefore carry that basis, which is the traversal itself.

A system that reverifies everything teaches people to ignore it. That sentence is the design constraint for this entire document.

---

## 5. The repair planner

**Status: specified.** The typed operations are emitted by `wi impact`; automated planning across weighted alternatives is defined here and unimplemented.

A repair is a typed operation, not a suggestion in prose. Each names exactly what a human or the engine must do.

| Operation | Does |
|---|---|
| `attach_source` | Bring a missing source into the workspace and ingest it |
| `approve_source` | Record a human decision that a supplied source may be relied on |
| `replace_anchor` | Bind a claim to a different location or a different source version |
| `rerun_check` | Re-execute a deterministic check against current state |
| `rerun_judgment` | Re-request a judgment whose inputs or policy hash moved |
| `restore_hedge` | Put back a modality or certainty qualifier a change removed |
| `qualify_claim` | Add a scope, exception or temporal bound that makes the claim supportable |
| `remove_claim` | Delete the assertion; the cheapest repair is sometimes not making the claim |
| `resolve_conflict` | Decide between two states that cannot both hold, with a stated reason |
| `accept_proposal` | Apply a drafted change and produce a new state |
| `reject_proposal` | Decline a drafted change; it stays in audit history |
| `renew_waiver` | Re-take a waiver whose bound claim state moved |
| `update_term` | Change a registered term's binding across every use site |
| `rebuild_target` | Re-render and re-attest a release artifact |

Cost weights are configuration:

```yaml
# .wi/policy/repair_cost.yaml
weights:
  rerun_check:        1      # deterministic, seconds, no human
  replace_anchor:     3      # deterministic, but a human confirms the rebind
  rebuild_target:     4      # cheap per artifact, expensive across a set
  accept_proposal:    8      # requires a human decision under Law J
  qualify_claim:     12      # requires the author to write a sentence
  restore_hedge:     12
  rerun_judgment:    15      # provider cost, latency, and a judged record
  resolve_conflict:  25      # requires reading two sources
  remove_claim:      30      # cheap mechanically, expensive editorially
  attach_source:     40      # may require contacting a third party
  renew_waiver:      60      # requires an authorized actor and a recorded reason
objective: minimize_human_decisions      # or: minimize_total_weight
```

**Cost is project-specific and the system must not pretend it is universal.** For a solo author, `attach_source` is a two-minute download. For a regulated filing, it is a procurement request and a two-week wait. For a newsroom on deadline, `remove_claim` is trivial; for a grant narrative where that claim is the eligibility argument, it is the end of the application. The defaults above are a starting point that an operator is expected to overwrite, and the planner prints the weights it used with every plan so that a reader can see what "cheapest" meant.

---

## 6. Stale is a status, not a failure

**Status: executable in `scripts/wi.py`.**

`stale` does not mean wrong. It means *the check that was run no longer applies to what is there now.* The claim may still be perfectly supported; nobody has looked since it moved.

| Mode | `stale_claim` produces | Reasoning |
|---|---|---|
| `off`, `light` | Advisory note | No verdict is being issued at all |
| `standard` | Advisory note | Unsupported claims are advisory here; stale claims are no stronger |
| `strict` | **HOLD** | The document is going to a funder, a court or a newsroom. A claim nobody has re-checked does not ship. |
| `regulated` | **BLOCK** | Medical, legal and compliance work has no acceptable rate of unexamined claims |

A HOLD is clearable by a human: re-run the check, or waive with a recorded reason under [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md). A BLOCK in regulated mode is clearable only by repairing the state.

**Why `stale` is separate from `needs_source`.** They demand different work. `needs_source` means go find evidence. `stale` means the evidence exists and may still be fine — press a button. Collapsing them makes the cheap repair look like the expensive one, and an author triaging forty findings will treat all forty as expensive and do none of them.

---

## 7. A worked scenario

**Status: executable in `scripts/wi.py`.**

### 7.1 A 1,660-page policy book, one federal source, one number

The book cites a federal income-limit table in fourteen places. The agency publishes a revision. One figure in one row changes.

**The traditional workflow:**

Search the manuscript for `51,200`. Find nine hits. Hope that is all of them — some renderings spell it "just over fifty-one thousand," which the search does not find. Edit the nine. Hope the deck was updated; open it and check. Hope the website was updated; email whoever owns it. Recheck the footnotes, because three of them cite the table by year and the year moved. Hope no social post preserved the old figure, knowing that four did and that nobody can now say which. Ship.

That workflow is not careless. It is what careful people do when the dependency information does not exist. Every "hope" in it is a place where the system offered no answer and a human substituted memory.

**The v5 output** is section 4's block: three anchors, two claim atoms, five paragraphs, three chapters, one slide, four social derivatives, two release artifacts — named, individually, with 1,814 claim atoms and eleven artifacts explicitly cleared. Three repair steps and one human decision.

The difference is not speed. It is that the second workflow produces a **statement a stranger can check** — here is the traversal, here is what it reached, here is what it did not — and the first produces a person's recollection of having been thorough.

### 7.2 The same engine on a fiction series

The dependency engine has no opinion about realm. A canon fact is a node with edges, exactly like a policy figure.

Book two, chapter 31: the author moves the date on which Maria discovers the ledger from 1987 to 1991.

```
$ python3 scripts/wi.py impact --node canon-ev-0044

canon.event canon-ev-0044  "Maria discovers the ledger"
  timeline_point  1987-04 → 1991-04        delta: canon_changed, date_changed

Inconsistent (6):
  sc-0112  bk1 ch09   Maria references the ledger in 1989 — now before discovery
  sc-0301  bk2 ch14   "four years after she found it" — arithmetic now wrong
  sc-0455  bk3 ch02   Dario's alibi depends on the ledger being unfound in 1990
  cut-0007 cinematic  on-screen title card reads "1987"
  aud-0219 audio      voice line: "seven years ago, in eighty-seven"
  cap-0338 subtitle   burned caption "APRIL 1987"

Consistent, and why (4 of the 11 nodes that reference this event):
  sc-0088  bk1 ch04   references the ledger's existence, not its discovery date
  sc-0520  bk3 ch11   relative ordering only — "after she found it" — still true
  canon-ch-0002       Maria's age at discovery is derived, not stated; recomputed
  mot-0015            the ledger motif carries no date

Unaffected: 4,102 canon nodes · 38 scenes · 2 cinematics · 611 audio lines.

Gate consequence under `standard`: advisory. Under `strict`: HOLD (6 inconsistencies).
Cheapest repair: 6 operations, of which 3 are re-renders (title card, audio line,
subtitle) and 3 require the author to rewrite a sentence.
```

The "Consistent, and why" block is not decoration. `sc-0520` says *"after she found it"* — a relative reference that survives any absolute date, and telling the author that is worth more than telling them about the six that broke, because it is the part they would otherwise have re-read to be sure.

**Why the fiction case matters to the nonfiction case.** They are the same engine, and neither is a special mode. A system that could only do policy books would be a compliance tool; a system that could only do novels would be a continuity checker. The reason one engine does both is that "which things depend on this thing" is a graph question, and the realm — `external_fact` or `fictional_canon` — governs what verification *means* for a node without changing how impact propagates. The realm rule from [`CONSTITUTION.md`](CONSTITUTION.md) still holds absolutely: a canon check never renders as an externally verified fact.

---

## 8. Invalidation benchmarks

**Status: specified.** The generator and assertion harness are defined here; the shipped suite covers the deterministic anchor and claim-atom cases.

The method: generate dependency graphs with known structure, mutate exactly one source node, and assert the **exact** downstream stale set — not a count, not a superset, the set.

| Generated case | Asserts |
|---|---|
| Linear chain, depth 12 | Every node downstream of the mutation is stale; every node upstream is not |
| Diamond dependency | The join node appears once, not twice; the visited set works |
| Two anchors into one source, one inside the changed region | Exactly one goes stale; the other rebinds and stays `verified` |
| A claim rendered in six targets | All six enter `review`; no seventh node is touched |
| An `illustrates` edge into a claim under audit | Zero propagation, always |
| A rejected proposal in the history of a changed node | Zero propagation, always |
| A cycle introduced by `depends_on` | Terminates; each state visited once per relation |
| A 400,000-node graph, one leaf mutated | Frontier of size 1; walk stays index-driven |
| A definition change with 900 use sites | All 900 enter `review`; the 12 sites using an allowed alias are included |
| A waiver whose claim state moved | The waiver is stale and the gate does not clear |

**This suite must be the most heavily tested thing in the project.**

The asymmetry is the reason, and it is total. A false positive here is a wasted review: the author re-checks something that was fine, is annoyed, and moves on. A false negative here **silently ships a stale release** — a document that carries a proof-of-verification attestation covering a claim whose evidence moved, delivered to a funder or a regulator or a court, with a green badge on it. There is no recovery from that failure because nobody knows it happened. Every other component in this system can fail loudly. This one can fail quietly, which is why its test suite is not proportional to its line count.

Coverage is reported the way every other measurement in this project is reported: as a count against an enumerable population. "10 of 10 generated topologies assert exact stale sets" is a measurement. "Invalidation coverage: 96%" is not.

---

## 9. What is executable and what is specified

| Mechanism | Status |
|---|---|
| State-digest comparison, change-region classification, `wi impact` | Executable in `scripts/wi.py` |
| Reverse-closure traversal with visited set and per-edge policy | Executable in `scripts/wi.py` |
| Byte-region non-propagation and automatic anchor rebinding | Executable in `scripts/wi.py` |
| Minimum repair frontier with unaffected counts and basis | Executable in `scripts/wi.py` |
| `stale_claim` gate behavior across the five evidence modes | Executable in `scripts/wi.py` |
| Typed repair operations emitted with each impact report | Executable in `scripts/wi.py` |
| Weighted repair planning across alternative repair paths | Specified |
| Propagation across media, spreadsheet and audio anchors | Specified — awaiting the adapters in [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) |
| Generated-topology invalidation benchmark harness | Specified |

---

## Related documents

- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — the edges this engine walks and the proof closure it protects
- [`SEMANTIC_DIFF.md`](SEMANTIC_DIFF.md) — the change classification that feeds step 3
- [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) — anchor integrity, staleness codes and the raw-bytes rule
- [`CONSTITUTION.md`](CONSTITUTION.md) — Law I, and the realm rule the fiction case depends on
- [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md) — `invalidated_by_edit` in the disclosure block
- [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) — the `stale` status in its original form, and waivers
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
