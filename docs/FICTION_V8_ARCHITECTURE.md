# Fiction Intelligence v8 — architecture specification

**Status:** proposed additive upgrade, executable standalone audit CLI + canonical integration still specified. **This is not an official v8 release.**

## The diagnosed defect

Writing Intelligence v7 contains excellent scene and canon doctrines, but existing fiction material sometimes treats formal patterns as universal obligations (e.g., fixed thriller phase order or the reduction of a character to a structural function). It also lacks an enforceable distinction between **a well-formed scene**, **a coherent novel** and **an affecting reader experience**. The 60-source-rule specification is retained verbatim in `provenance/USER_REQUIREMENTS.txt`; `rules/fiction_v8_rules.json` gives each rule a stable ID, canonical owner, intended executable or judgment method, acceptance target, two examples, and implementation status.

## Canonical authority, not a parallel compiler

The existing canonical semantic graph remains `scripts/wi.py` and the v6/v7 constitutions. **Do not** replace `references/compiler/narrative_intelligence_engine.md`, `references/v5/STORYWORLD_OS.md`, `schemas/storyworld_memory.schema.json` or `services/api/src/runtime/Kernel.ts` with the sidecar. The sidecar derives novel-wide review findings **from** a canon state and manuscript snapshot. In eventual integration, findings, author decisions and waivers will be graph nodes and governed proposals with exact digest binding. The current sidecar is read-only and writes reports to new files only.

```
Author-approved canon + StoryworldMemoryV3 + scene graph + manuscript
    ↓  [future canonical adapter: map identities, preserve provenance]
wi.fiction.manuscript/v1 (sidecar IR, digest)
    ├─ text scanner: approximations → SIGNAL
    ├─ typed world/scene checker → SIGNAL | DATA_GAP | DEFECT
    └─ editorial and reader studies → judgment, not machine proof
    ↓
60-rule report with rule/source IDs, reasons, anchors, unassessed states
    ↓
policy gate (draft → editorial → publication)
    ↓
ELIGIBLE_FOR_HUMAN_DECISION or HOLD/BLOCK — never 'bestseller verified'
    ↓  [future canonical proposal/decision, wi obligations, wi release]

```

## Dependency model and invariants

1. **Identity:** scene, character, threat, mystery, world rule, plant/payoff and intervention IDs are stable semantic identities. A cross-reference to a non-existent scene or character fails input validation; references to later books must be represented as intentional series deferrals, not fabricated local IDs.
2. **Epistemic separation:** fictional canon is author-declared and may be changed under a recorded decision, not an external real-world proof. A scientific assertion appearing as nonfiction must be cited in the appropriate non-fiction realm; FI-43 flags literary presentation but does not convert invention to physics.
3. **Change impact:** any change to a world rule invalidates relevant power-use judgments; to a scene, its chapter, mystery ledger, relationship arc, character memory, motif progression, and payoff; to the ending, every opening-promise and payoff comparison. The standalone implementation does not yet perform a canonical dependency-graph invalidation transaction.
4. **Two clocks:** distinguish story/event time, record-creation time, observer time, narration time; in a real provenance graph, add *workspace knowledge time* and *canon-valid time*. Cross-book retcons supersede rather than rewrite previously accepted history.
5. **No conflation:** `SIGNAL` means candidate editorial issue, `DATA_GAP` means absent annotation, `DEFECT` means explicit contradiction in the provided typed model, `UNASSESSED` means not judged. `REVIEWED_PASS` means a human recorded an editorial opinion, **not** a mathematically verified work of art.
6. **No formula lock:** percentages and genre beats are toolkits. Performance is tested against the declared genre/reader promise. Deliberate slow burn, intentional repeated motif, nonlinear order, quiet climax, and unreliable narration remain legitimate. Preserve exceptions as scoped decisions with reasons and anchors, never global bypass toggles.
7. **No automatic rewriting:** the compiler may propose redlines with before/after excerpts, identified semantic delta and regression cost; it does not silently delete voice, overwrite manuscript text or change canon.
8. **No self-certification:** publication requires external reader-study evidence and manual authority. Automated text counts cannot certify suspense, emotion, sales, publishing quality, or reader satisfaction.
9. **Conservation:** power actions must respect declared permissions and costs; explicitly forbidden actions without authorized retcon and explicit cost evasion are structurally blocked, including if a reviewer claims to like the result.
10. **Decision-time truth:** each audit binds exact input, rule catalog and policy digests. Later audit improvements do not retroactively alter the record of what was inspected and by whom.

## Data partitions

| Partition | Canonical content | Sidecar treatment | Proof authority |
|---|---|---|---|
| Manuscript prose | authored chapters | UTF-8 text, exact digest and optional spans | file digest only |
| Narrative IR | scene/character/arc extraction | `fiction_ir.schema.json` | extraction/author judgment |
| World constraints | Storyworld OS canon nodes | `world_rules`, `power_uses`, `interventions` | accepted fictional canon |
| Reader experience | readers' actual reactions | `fiction_reader_study.schema.json` | respondents + consent + method; never model-as-reader |
| Release policy | authoritative WI policy and decisions | proposed `fiction_profiles.json` | author/editor and canonical runtime |

## Failure semantics

- Missing spans or incomplete coverage → `UNASSESSED`/`DATA_GAP`, not `PASS`.
- A metaphor detector's false positive → reversible `SIGNAL`, not a defect.
- Forbidden power or unpaid explicit cost → `DEFECT` and gate `BLOCK`; correction requires canon repair or a traceable retcon, not a waiver.
- Reviewer disagrees with another reviewer → preserve competing assessments; do not average ratings or manufacture consensus. The draft sidecar currently groups them but does **not** implement full typed adjudication.
- Reader-study digest differs from the manuscript audit → `HOLD`; previous responses cannot approve a revised book.
- No proof of print/EPUB rendering → publication `HOLD`, even with 60 human approvals.

## Acceptance criteria (future canonical integration)

- Exact commit pin and clean-room merge into current `main` only after updating against any new commits.
- No failures in v4/v5/v6/v7 existing test suites or canonical bundle reproductions.
- Copying the additive files doesn't alter the v7 CLI, normative constitutions or package counts unnoticed.
- `wi simulate` shows impact before a canon-affecting edit; `wi decide` + `wi commit` record authority and exact state; `wi why` reconstructs the rationale.
- A negative test must demonstrate both `BLOCK` for forbidden power and `HOLD` for an untested publication.
- Full manuscript evaluation with a real human editorial reviewer and separate beta readers; accuracy and utility evaluated using blinded examples rather than model self-evaluation.
- No regression of deliberately anomalous literary form merely to satisfy a fixed threshold.

## What is implemented now

The standalone CLI validates typed IDs and relationships, audits 60 rules as `UNASSESSED` unless supported, executes a subset of text and typed structural checks, produces deterministic reports and gates, and runs 41 unit/negative tests. It does **not** parse a novel into the IR, call LLM judgment, edit canon, write to GitHub, run the core WI runtime, export EPUB/PDF or substitute for independent readers. These are explicit integration milestones, not stealth 'done' claims.
