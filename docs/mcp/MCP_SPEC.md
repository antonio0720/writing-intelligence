# Writing Intelligence v3.0 — MCP Server Specification (Draft)

**Status**: Draft. Reference implementation ships in v3.1.

This document specifies a Model Context Protocol server surface for Writing Intelligence v3.0. Clients (Claude Desktop, Claude Code, custom agents) consume the tools to embed v3.0 capability in their workflows.

> **v9 note.** Released in 9.0.0. Two v9 tools are specified below (`wi9_authorship_audit`, `wi9_hotphrase_scan`); like every tool here they are a contract for an MCP adapter, and their behaviour is implemented and tested in the REST runtime's v9 endpoints. There is deliberately no release tool. Not served, on purpose: the per-writer tools (`vault`, `ledger`, `meaning review`, `voice`, `voice-review`, `voice-compare`, `compose`) read and write a writer's private folders and grants on their own machine, so they run only through the local CLI (`wi authorship ...`). See [`../../references/v9/README.md`](../../references/v9/README.md).

## Server Name

`writing-intelligence`

## Tools

### `wi_compile`

Run the 11-pass kernel.

**Input**:

```json
{
  "request_text": "string",
  "intake_overrides": {
    "voice": "string",
    "genre_stack": ["string"],
    "arena": "string",
    "high_stakes": "boolean",
    "output_modes": ["string"]
  }
}
```

**Output**: `DeliveryBundleV3` + selected artifacts based on output_modes.

### `wi_score`

Score a draft without rewriting.

**Input**:

```json
{
  "draft_text": "string",
  "genre_stack": ["string"],
  "voice": "string",
  "high_stakes": "boolean"
}
```

**Output**: scorecard JSON.

### `wi_voice_fingerprint_build`

Build a voice fingerprint from samples.

**Input**:

```json
{
  "voice_id": "string",
  "samples": ["string"]
}
```

**Output**: `VoiceFingerprintV3`.

### `wi_voice_drift_check`

Compare a draft's fingerprint to a baseline.

**Input**:

```json
{
  "baseline_voice_id": "string",
  "draft_text": "string"
}
```

**Output**: drift report.

### `wi_arena_repackage`

Repackage approved content across arenas.

**Input**:

```json
{
  "approved_text": "string",
  "source_voice_id": "string",
  "target_arenas": ["string"]
}
```

**Output**: array of `DeliveryBundleV3`.

### `wi_epistemic_audit`

Audit a draft for fabrication risk.

**Input**:

```json
{
  "draft_text": "string",
  "available_sources": [{"source_id": "string", "uri": "string"}]
}
```

**Output**: `EpistemicLedgerV3`.

### `wi_benchmark_run`

Run a benchmark case.

**Input**:

```json
{
  "case_id": "string",
  "against_version": "string"
}
```

**Output**: `BenchmarkResultV3`.

### `wi_get_genre_pack`

Retrieve a genre pack doctrine.

**Input**: `{"pack_id": "string"}`

**Output**: markdown content of the pack.

### `wi_get_voiceprint`

Retrieve a voiceprint doctrine.

**Input**: `{"voice_id": "string"}`

**Output**: markdown content + measurements if available.

### `wi_list_packs`

List all available genre packs.

**Output**: array of `{pack_id, title, summary}`.

### `wi_list_voiceprints`

List all available voiceprints.

**Output**: array of `{voice_id, title, summary}`.

### `wi9_authorship_audit` *(v9)*

Check an authorship and evidence dossier. A declaration checker: it never authenticates a writer.

**Input**: `{ "dossier": <wi9-authorship-2 object>, "files": { "relative/path.txt": "UTF-8 text" } }`

**Output**: `{ "exit_code": 0 | 3, "report": <wi9-authorship-audit-2>, "release_authorized": false }`. Same contract as `POST /v9/authorship/audit`. A client MUST present `REVIEW` as "limited checks passed", never as permission to send or publish.

### `wi9_hotphrase_scan` *(v9)*

Editorial phrase questions from the 334-rule catalog.

**Input**: `{ "text": "string", "include_quotes": false }`

**Output**: `{ "exit_code": 0, "report": <wi9.hotphrases.report/1> }`. Same contract as `POST /v9/hotphrases/scan`. A client MUST NOT describe a match as evidence of AI authorship or rewrite text automatically.

There is no `wi9_authorship_release` tool: release authority is read from a v6 grant store the operator names locally, and an agent is not the operator.

## Resources

The MCP server may expose resources for:

- Each genre pack doctrine
- Each voiceprint doctrine
- Each schema definition
- Each agent specification
- Each benchmark case

## Prompts

The server may expose prompt templates for:

- "Run full v3.0 kernel"
- "Audit for fabrication"
- "Build voice fingerprint"
- "Repackage for [arena]"
- "Run benchmark"

## Implementation Notes

A reference implementation in Python (FastMCP) and TypeScript (MCP SDK) will ship in v3.1. See `ROADMAP.md`.

## Conformance

A conformant MCP server MUST:

- Expose at least the 8 core tools listed above
- Validate all inputs against the schemas
- Return outputs validating against the schemas
- Honor delivery blocks from the epistemic ledger
- Never invent content in `wi_arena_repackage`

## Author

Antonio T. Smith Jr. / Density6 LLC
