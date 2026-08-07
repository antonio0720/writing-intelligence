# The Writing Board — Twelve Specialist Agents

Writing Intelligence decomposes the 11-pass kernel into a coordinated multi-agent writing board. Each agent owns one job and emits one artifact. The board runs as a single skill or as a multi-agent orchestration.

**Manifest**: `agents/agent_manifest.yaml` — canonical roster, dependencies, schemas, conflict resolution.

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
