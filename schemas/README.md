# Writing Intelligence — Machine-Readable Schemas

There are two schema families in this repository, and they answer different questions.

| Family | Where | What it describes | Question it answers |
|---|---|---|---|
| **v3 craft schemas** | this directory, unchanged | The artifacts a writing pass produces — intake, corpus, voice, genre, architecture, ledger, rewrite log, storyworld, delivery, benchmark, agent task | *What did this pass find?* |
| **v5 state schemas** | [`v5/`](v5/README.md) | The objects a governed workspace holds — sources, versions, anchors, claim atoms, graph nodes and edges, verification, judgment, proposals, decisions, invalidations, policy, concepts, release manifests | *Is that finding still true?* |

The v5 family does not replace the v3 family and does not deprecate it. The eleven v3 schemas below are the **craft artifacts** and remain valid for the craft kernel; their conceptual boundaries — corpus, structure, evidence, voice, canon, delivery — were correct and v5 keeps every one of them. What v5 adds is a single graph identity system underneath, so that the same claim, source or output has one name everywhere instead of a different name in each artifact. That is the difference between a photograph of a document's accuracy and a state that notices when it expires.

Start with [`v5/README.md`](v5/README.md) for the two-identity model (logical id vs. state digest), the canonical hashing contract, which schemas are executable today, and how each v3 artifact becomes a view over the v5 graph.

The rest of this document describes the v3 craft schemas.

---

## Writing Intelligence v3.0 — the craft schemas

Every pass of the v3.0 kernel emits a structured artifact. The schemas here define those artifacts as JSON Schema draft 2020-12 documents.

## Purpose

Schemas unlock:

- CLI execution
- MCP server execution
- Web app integration
- CI writing checks
- Automated scoring
- Benchmark reports
- Issue templates
- Reproducible outputs
- Traceable quality improvement

Without schemas, v3.0 would remain a brilliant skill. With schemas, it becomes infrastructure.

## The 11 Canonical Schemas

| Schema | Purpose | Pass |
|---|---|---|
| `intake_contract.schema.json` | Governed task object | 0 |
| `corpus_map.schema.json` | Allowed sources, priority, conflicts | 2 |
| `voice_fingerprint.schema.json` | Measurable voice features | 7 |
| `genre_stack.schema.json` | Active packs and weights | 8 |
| `architecture_graph.schema.json` | Section / scene / claim nodes | 4 |
| `epistemic_ledger.schema.json` | Claim classification + source status | 5 |
| `prose_rewrite_log.schema.json` | Sentence transformation log | 6 |
| `storyworld_memory.schema.json` | Longform continuity | 4 (narrative) |
| `delivery_bundle.schema.json` | Final output assets | 10 |
| `benchmark_result.schema.json` | Regression and quality delta | 11 |
| `agent_task.schema.json` | Multi-agent orchestration | All |

## Versioning

Schemas follow semantic versioning. v3.x.y maintains backwards compatibility within the v3 major. Breaking schema changes require a major version bump and an `MIGRATION_v3_to_v4.md`.

## Usage

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$ref": "https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/schemas/intake_contract.schema.json"
}
```

## Conformance

A v3.0-conforming implementation MUST:

1. Accept any document validating against the listed schemas.
2. Emit pass artifacts that validate against the corresponding schema.
3. Treat any `unsafe` source status as a delivery block.
4. Treat any high-stakes domain output without an `epistemic_ledger` as a benchmark fail.
5. Refuse to package a `delivery_bundle` that contains content not present in approved upstream artifacts.

## Author

Antonio T. Smith Jr. / Density6 LLC
