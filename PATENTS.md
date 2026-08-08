# Patents and Invention Disclosure

**Project:** Writing Intelligence — The Sovereign Meaning Runtime
**Inventor:** Antonio T. Smith Jr.
**Assignee of record (intended):** Density6 LLC
**This record compiled:** 8 August 2026
**Repository:** https://github.com/antonio0720/writing-intelligence

> **Not legal advice.** This file was not written by a patent attorney. It is a
> technical disclosure record and a statement of position. Anyone whose plans
> depend on the answers here — including the maintainer — should obtain their
> own counsel. Where this file states a rule of law it states the general shape
> of that rule and nothing more, and the general shape of a rule is exactly the
> thing that has exceptions.

---

## 1. Status, stated exactly

**No patent has been granted covering any mechanism in this repository. No
patent application has been filed. Nothing in this project is patent pending,
and nothing in this project is marked as such.**

That sentence is the most important one in this file and it is deliberately
first, because the alternative — a vague notice that lets a reader infer
protection that does not exist — is false marking, and this project's entire
doctrine is that a claim you cannot point at has not been verified. A patent
notice on an unfiled invention is precisely the failure mode the software is
built to prevent, committed in the software's own repository.

What *does* exist is this: a dated, public, specific description of sixteen
mechanisms, and a reservation of rights in them under `NOTICE` §3.

## 2. What this file is for

Three functions, in descending order of how much they are actually worth.

**It is a defensive publication.** Everything described below is published
here, in public, with a date. That makes it prior art. A third party who files
on one of these mechanisms after the disclosure date recorded below is filing
against a public disclosure that predates them. This protection is real, it is
already in force, and it costs nothing. It is also the only protection in this
file that does not depend on somebody taking a further action.

**It is a dated invention-disclosure record.** Each family below names the
mechanism, the file and function that implements it, the doctrine document that
reasons it, and the release in which it first became public. The dates are not
asserted from memory — they are the commit and tag dates in this repository's
own history, which is independently checkable by anyone who clones it.

**It is a reservation of rights.** See `NOTICE` §3, including the honest
statement of why a reservation notice is weaker than it reads.

## 3. The disclosure clock — read this part twice

This repository has been public since 30 March 2026. Every mechanism below was
publicly disclosed on the date recorded in its row. Two consequences follow and
they point in opposite directions.

**In the United States**, an inventor's own disclosure generally does not itself
bar that inventor from patenting, provided an application is filed within one
year of the disclosure (35 U.S.C. § 102(b)(1)). That grace period is running.
The earliest-disclosed families in this repository are the furthest along it.

| First disclosed | Release | Approximate U.S. filing deadline |
|---|---|---|
| 26 May 2026 | v3.0.0 | **26 May 2027** |
| 6 August 2026 | v4.0.0 | **6 August 2027** |
| 7 August 2026 | v5.0.0 and v6.0.0 | **7 August 2027** |

**Outside the United States, the position is materially worse and the grace
period is mostly not there.** The European Patent Convention applies absolute
novelty with only narrow exceptions (evident abuse, and certain official
international exhibitions) — a public disclosure before the filing date is
generally novelty-destroying, and a GitHub repository is a public disclosure.
Several jurisdictions do provide a grace period — Japan, South Korea, Australia
and Canada among them — but the length, the conditions and the procedural steps
required to claim it differ by country and some require an affirmative request
at filing. China provides only a narrow six-month exception.

The practical reading, and the reason this section is not buried: **for the
mechanisms already disclosed, European patent protection is likely already
unavailable, and the U.S. window closes on a schedule that has been running
since May 2026.** Adding a notice to this repository does not change either
fact. Only a filing does. This file exists to make the position legible, not to
improve it.

**Anything not yet published is a different situation.** Mechanisms that exist
only in private work — unreleased branches, unpublished doctrine, anything held
back from a tag — have not started either clock. **Everything in this file has.**
Every one of the sixteen families in §4 and §5, including the four secondary
ones, carries a first-disclosed date, and the clock started on that date whether
the entry is described in a paragraph or in a line. Brevity of description is not
the test; publication is. If a portfolio strategy matters, the ordering that
follows is *file, then publish*, and this repository's release cadence is the
thing that would need to bend to it.

## 4. Primary families

Sixteen entries: twelve primary, four secondary. Each is described as the
concrete technical operation the code performs, not as the outcome it produces
for a user. That framing is deliberate. Under U.S. patent-eligibility doctrine
an abstract idea implemented on a generic computer is a poor candidate; a
specific architecture that solves a specific technical problem in a specific way
is a better one. Every row below therefore names a data structure, a
computation and a failure it prevents — because that is what is actually
implemented, and because a claim drafted from the marketing sentence would
deserve to fail.

| # | Family | Mechanism as implemented | Implementation | Doctrine | First disclosed |
|---|---|---|---|---|---|
| 1 | **Semantic intermediate representation for governed meaning** | Typed meaning nodes carrying a persistent logical identity independent of wording, each addressed by a domain-separated state digest over canonical bytes, from which renderings are compiled rather than edited | `v6_logical_id`, `canonical_bytes`, `v6_state_digest`, `class V6` | `references/v5/SEMANTIC_IR.md`, `references/v6/SEMANTIC_IR.md`, `references/v6/EXECUTABLE_MEANING.md` | v5.0.0 · 7 Aug 2026 |
| 2 | **Claim-atom verification with partial-support states** | Decomposition of compound prose into independently verifiable assertions, each carrying its own verification state including explicit partial and unmet states, so an unavailable check remains visibly unmet rather than dropping out of the denominator | `gate_atoms`, `render_atom_gate`, `anchor_and_check` | `references/v4/PROOF_PROTOCOL.md`, `references/v5/CONSTITUTION.md` | v4.0.0 · 6 Aug 2026 |
| 3 | **Multimodal evidence anchors over immutable source bytes** | An evidence location pinned to an exact byte range of an immutably hashed raw source, with the extractor's derived output hashed separately, so a change in the source and a change in the extractor are mechanically distinguishable | `make_anchor`, `_candidate_anchor`, `blob_digest` | `references/v5/EVIDENCE_ANCHORS.md`, `references/v5/MULTIMODAL.md` | v5.0.0 · 7 Aug 2026 |
| 4 | **Dependency-aware proof and staleness graph** | Typed dependency edges over meaning nodes such that a change to a source or node mechanically invalidates dependent proofs, and — the load-bearing half — identifies the set that is provably unaffected | `compute_impact`, `mark_stale`, `stale_frontier`, `cmd_impact` | `references/v5/STALENESS.md`, `references/v5/AUTHORSHIP_GRAPH.md` | v5.0.0 · 7 Aug 2026 |
| 5 | **Minimum safe repair frontier** | Computation of the smallest ordered set of verification and repair operations sufficient to restore proof closure after a semantic state change, ordered by a declared cost class rather than by graph position | `repair_plan`, `v6_repair_plan` | `references/v5/STALENESS.md`, `references/v6/COUNTERFACTUAL_SIMULATION.md` | v5.0.0 · 7 Aug 2026 |
| 6 | **Proof-carrying document and release architecture** | A released artifact bound to its proof closure, its executed checks, its declared omissions and its source digests, such that a second machine can verify the release offline with no model and no network | `v6_capsule_create`, `v6_capsule_verify`, release verification path | `references/v5/PROOF_CARRYING_RELEASE.md`, `references/v6/BUILD_MANIFEST.md` | v5.0.0 · 7 Aug 2026 |
| 7 | **Semantic version control** | Branches, commits, refs and merge-base resolution over structured meaning nodes rather than over file lines, with a graph root digest identifying an entire semantic state | `put_root`, `set_ref`, `commit_obj`, `history`, `merge_base` | `references/v6/SEMANTIC_VERSION_CONTROL.md` | v6.0.0 · 7 Aug 2026 |
| 8 | **Conflict-preserving semantic three-way merge** | A dimension-aware BASE/OURS/THEIRS merge over persistent logical ids that merges non-conflicting dimensions, types the conflicting ones by what disagrees, halts with a non-zero exit, and structurally cannot emit a value neither branch asserted | `v6_merge`, `_v6_conflict_kind`, `cmd_merge`, `cmd_conflicts` | `references/v6/MERGE_PROTOCOL.md` | v6.0.0 · 7 Aug 2026 |
| 9 | **Counterfactual semantic change simulator** | Construction of an ephemeral candidate state from a proposed change; traversal of the dependency system to compute breakage, proof invalidation, required authority, repair cost and the provably-unaffected set; emission of the candidate graph root the commit would produce; discard of the candidate without writing | `v6_simulate`, `v6_apply`, `cmd_simulate` | `references/v6/COUNTERFACTUAL_SIMULATION.md` | v6.0.0 · 7 Aug 2026 |
| 10 | **Derived proof-obligation planner** | Derivation of what must be proved from typed semantic state, release target and policy *before* any check runs, inverting normal validation so that a nonexistent or unavailable check remains a visibly unmet obligation | `v6_obligations_for`, `v6_run_constraints`, `cmd_obligations` | `references/v6/PROOF_OBLIGATIONS.md` | v6.0.0 · 7 Aug 2026 |
| 11 | **Authority-governed semantic state transitions** | Scoped, expiring capability grants derived from the semantic delta class, controlling which actor or process may cause which category of meaning change, with delegation permitted to narrow scope and structurally unable to widen it, and absence of a grant as refusal rather than default-allow | `v6_required_capability`, `v6_capability_covers`, `v6_scope_covers`, `v6_validate_child_grant`, `cmd_authority` | `references/v6/AUTHORITY_MODEL.md`, `references/v6/CAPABILITY_SECURITY.md` | v6.0.0 · 7 Aug 2026 |
| 12 | **Selective-disclosure proof capsules** | A Merkleized proof closure permitting disclosure of a selected subset of governed claims while cryptographically proving membership in the full closure and explicitly declaring what was withheld | `v6_leaf_digest`, `v6_merkle_root`, `v6_inclusion_proof`, `v6_verify_inclusion`, `v6_closure_leaves` | `references/v6/PROOF_CAPSULES.md` | v6.0.0 · 7 Aug 2026 |

**Strongest candidates, in the maintainer's own assessment:** #9, #8, #12, #6 and
#1. #9 because an ephemeral candidate state that is computed, traversed, reported
on and discarded without ever being written is a concrete technical architecture
rather than an abstract aim. #8 because refusing to produce an output is an
unusual and specific technical behaviour with a specific failure it prevents.
#12 because the cryptographic construction is the invention and is fully
specified. This is an inventor's assessment, not a patentability opinion; none
of these has been through a prior-art search.

## 5. Secondary families

Four mechanisms that a strategy might file separately, as continuations, or not
at all. They are recorded here so the disclosure date is fixed either way.

| # | Family | Mechanism | Implementation | Doctrine | First disclosed |
|---|---|---|---|---|---|
| 13 | **Bitemporal meaning state** | Independent valid-time and knowledge-time intervals on a meaning node, such that a correction supersedes without erasing, a schedule of values over time is not reported as a contradiction, and "what do we believe now about 2022" and "what did we believe in March 2028" are separately answerable | `v6_valid_interval`, `v6_knowledge_interval`, `v6_intervals_overlap`, `_v6_covers` | `references/v6/BITEMPORAL_STATE.md` | v6.0.0 · 7 Aug 2026 |
| 14 | **Semantic source maps** | A mapping from emitted rendering bytes back to the meaning nodes that produced them, making a rendering diff attributable to a semantic cause | rendering path | `references/v6/SEMANTIC_SOURCE_MAPS.md` | v6.0.0 · 7 Aug 2026 |
| 15 | **Federated re-verification across organizational boundaries** | Verification of imported governed meaning against another organization's closure without importing that organization's workspace or trusting its assertions | import/verify path | `references/v6/FEDERATION.md` | v6.0.0 · 7 Aug 2026 |
| 16 | **Reliability and argument-basis propagation** | Typed reliability classes propagated along argument edges, so the basis of a downstream conclusion is computed from the basis of its supports rather than declared | `v6_carries_proof`, argument graph traversal | `references/v5/RELIABILITY_TYPES.md`, `references/v6/ARGUMENT_GRAPH.md` | v5.0.0 · 7 Aug 2026 |

## 6. What is *not* claimed

Stated so the boundary is legible, and because a disclosure record that quietly
implies more than it holds is the same failure as a proof that implies more than
it checked.

- No claim is made to writing assistance, text generation, grammar correction,
  style transfer, summarization, or any use of a language model to improve
  prose. That is not what any of the above is.
- No claim is made to Merkle trees, content-addressed storage, three-way merge,
  capability-based security, bitemporal databases or semantic versioning as
  general techniques. Each of those is decades old and belongs to everyone. What
  is described above is their application to *governed meaning* in specific
  combinations that solve specific failures, and any claim would have to live in
  that specificity or fail.
- No claim is made to any mechanism not implemented in this repository. Doctrine
  documents that describe intended behaviour ahead of the code are marked as
  such where they are, and `references/v6/NON_GOALS.md` records what the system
  deliberately will not do.
- No patent right will be asserted against offline verification of an artifact
  this project produced. See `NOTICE` §5.

## 7. If you believe you disclosed one of these first

Open an issue with the date, the public artifact and what it disclosed. Prior
art that predates this repository is prior art and this file will be corrected
to say so. A disclosure record that will not accept a correction is a marketing
document with a date on it.

---

*Compiled 8 August 2026. Dates verifiable against this repository's git history
and release tags. Corrections welcome under the process in §7.*
