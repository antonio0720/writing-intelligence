# The Writing Board — Twelve Specialist Agents

Writing Intelligence decomposes the 11-pass kernel into a coordinated multi-agent writing board. Each agent owns one job and emits one artifact. The board runs as a single skill or as a multi-agent orchestration.

**Manifest**: `agents/agent_manifest.yaml` — canonical roster, dependencies, schemas, conflict resolution.

**v8:** on fiction, the Narrative Architect, Structure Engineer, Dialogue Commander and Stress Tester can hand a typed story projection to the v8 engines (`scripts/wi-fiction.py`, `scripts/wi-arc.py`, `extensions/wi8/craft03/scripts/wi-craft.py`, `extensions/wi8/japan04/cli/wi8_japan.py`) and cite their findings by requirement ID. The engines report; the agents and the author decide. No agent may present an engine pass as a verdict on the book.

**v9 preview (PR #8, not a release):** see [What changed per agent under v9](#what-changed-per-agent-under-v9) below. No agent gains authority to publish, and none may present a detector score as a target, a gate or proof of origin.

---

## The Roster

| Agent | Pass | Artifact |
|---|---|---|
| Intake Architect | 0 | Intake contract |
| Genre Marshal | 1 | Genre stack |
| Corpus Auditor | 2 | Corpus map |
| Structure Engineer | 4 | Architecture graph |
| Evidence Prosecutor | 5 | Epistemic ledger |
| Sentence Surgeon | 6 | Rewrite log |
| Dialogue Commander | 6 (narrative) | Dialogue stress report |
| Voice Fingerprinter | 7 | Voice match report + fingerprint |
| Stress Tester | 9 | Stress battery |
| Scorekeeper | 10 | Scorecard |
| Delivery Packager | 10 | Delivery bundle |
| Narrative Architect | 11 (narrative) | Storyworld memory update |

---

## Orchestration Rules

1. **Intake Architect always runs first.**
2. **Corpus Auditor always runs when sources matter.** (default: yes)
3. **Evidence Prosecutor always runs in high-stakes domains.** (academic / medical / legal / government / grant / financial)
4. **Narrative Architect runs only for fiction / story / screenplay / scene / lore / transmedia / chapter work.**
5. **Scorekeeper cannot override Evidence Prosecutor's cap rules.**
6. **Delivery Packager cannot invent content; it formats approved content only.**

---

## Conflict Resolution (from manifest)

| Conflict | Winner |
|---|---|
| User constraint vs. auto-detected genre | User constraint |
| Evidence integrity vs. persuasive force | Evidence integrity |
| Voice fidelity vs. factual clarity (high stakes) | Factual clarity |
| Voice fidelity vs. factual clarity (else) | Voice fidelity |
| Compression vs. compliance | Compliance |
| Drama vs. story continuity | Story continuity |
| CTA force vs. trust preservation | Trust preservation |

---

## Block Signals

The board halts delivery when any of:

- `epistemic_ledger.delivery_block = true`
- `delivery_bundle.delivery_decision = block`
- Any source carries `status: unsafe`
- Any claim carries `fabrication_risk: blocked`

When blocked, the board surfaces the block reason to the user. No silent overrides.

---

## Running as One Skill

When invoked as a single skill (the default mode), Claude reads `SKILL.md`, executes the 11-pass kernel, and emits the requested output modes. The agent decomposition is implicit.

## Running as a Multi-Agent Orchestration

When invoked as a multi-agent orchestration (e.g., via the Claude Agent SDK), each agent is a separate sub-agent with its own tool budget and timeout. Dependencies flow per the manifest. The Orchestrator (the parent process) coordinates artifact handoff.

A reference implementation will ship in v3.1 (`docs/api/API_SPEC.md`).

---

## What changed per agent under v9

*Preview on PR #8; not a release. The roster, passes, artifacts and conflict rules above are unchanged.*

| Agent | What v9 adds | Where it is written |
|---|---|---|
| Intake Architect | Venue contract first; claims and `experience_state` captured as stated; origin declared and treated as self-reported | `agents/intake_architect.md` |
| Genre Marshal | The venue rule outranks any genre pack; a pack cannot change an authorship declaration | `agents/genre_marshal.md` |
| Corpus Auditor | Source custody with pinned digests, consent recorded, hypothetical material kept labeled | `agents/corpus_auditor.md` |
| Structure Engineer | Fiction gates unchanged; argument nodes name their support; no symmetry for its own sake | `agents/structure_engineer.md` |
| Evidence Prosecutor | Claim coverage, presence is not support, firsthand claims need confirmed experience | `agents/evidence_prosecutor.md` |
| Sentence Surgeon | `repair_rhythm` (log op `rhythm_repaired`); acts on the author's phrase-review disposition; every change declares its kind | `agents/sentence_surgeon.md` |
| Dialogue Commander | Fiction gates unchanged; a phrase match in dialogue is character voice; no manufactured recall in memoir | `agents/dialogue_commander.md` |
| Voice Fingerprinter | Consented samples only (3 or more, 500 or more words, per genre); similarity never proves authorship | `agents/voice_fingerprinter.md` |
| Stress Tester | No change in this preview; it already treats detector scores as never a target | `agents/stress_tester.md` |
| Scorekeeper | An editorial score never authorizes release; detector scores are never a score input | `agents/scorekeeper.md` |
| Delivery Packager | Research briefs only for `human_only` venues; `RELEASE_ELIGIBLE` is a precondition, not a send | `agents/delivery_packager.md` |
| Narrative Architect | Fiction gates unchanged; no borrowed memory in memoir or autofiction | `agents/narrative_architect.md` |

The authorship checker (`scripts/wi-authorship.py`) is a declaration checker: it does not authenticate a writer, and `REVIEW` or `RELEASE_ELIGIBLE` is never a send. Context: [`../references/v9/README.md`](../references/v9/README.md).
