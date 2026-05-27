# Writing Intelligence v3.0 — Machine-Readable Schemas

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
