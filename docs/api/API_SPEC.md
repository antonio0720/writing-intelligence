# Writing Intelligence v3.0 — REST API Specification (Draft)

**Status**: Draft. Reference implementation ships in v3.1.

This document specifies a REST API surface that any Writing Intelligence v3.0 conformant implementation can expose. v3.0 ships the doctrine; v3.1 ships the reference implementation.

## Base URL

`https://api.writing-intelligence.example/v3`

(Replace with your deployed host.)

## Authentication

Bearer token in `Authorization` header. Token issuance is implementation-specific.

## Endpoints

### POST /compile

Run the 11-pass kernel on a request.

**Request body**:

```json
{
  "request_text": "Rewrite this draft for an investor audience: ...",
  "intake_overrides": {
    "voice": "investor_precision",
    "arena": "memo",
    "high_stakes": true
  },
  "output_modes": ["clean", "scorecard", "epistemic-ledger"]
}
```

**Response (200)**:

```json
{
  "task_id": "wi_v3_2026_000001",
  "intake_contract": { ... },
  "delivery_bundle": { ... },
  "scorecard": { ... },
  "epistemic_ledger": { ... },
  "passes_run": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
  "duration_ms": 32450
}
```

**Errors**:

- `400` — invalid request body (does not validate)
- `422` — ambiguity unresolved; clarification needed (returns ambiguity_flags)
- `423` — delivery blocked (epistemic ledger blocked output)
- `429` — rate limit exceeded
- `500` — server error

### POST /score

Score a draft without rewriting.

**Request body**:

```json
{
  "draft_text": "...",
  "genre_stack": ["sales", "email"],
  "voice": "casual_sharp",
  "high_stakes": false
}
```

**Response (200)**:

```json
{
  "task_id": "wi_v3_2026_000002",
  "scorecard": { ... },
  "passes_run": [0, 1, 3, 4, 5, 9, 10]
}
```

### POST /voice/fingerprint

Build a voice fingerprint from samples.

**Request body**:

```json
{
  "voice_id": "antonio_ts_jr",
  "samples": [
    "...sample text 1, 500+ words...",
    "...sample text 2, 500+ words...",
    "...sample text 3, 500+ words..."
  ]
}
```

**Response (200)**: a `VoiceFingerprintV3`.

### POST /voice/drift

Compare a draft's fingerprint against a baseline.

**Request body**:

```json
{
  "baseline_voice_id": "antonio_ts_jr",
  "draft_text": "..."
}
```

**Response (200)**: a drift report block (per `schemas/voice_fingerprint.schema.json` `drift_report` field).

### POST /repackage

Run Pass 8 only: repackage approved content for new arenas.

**Request body**:

```json
{
  "approved_text": "...",
  "source_voice_id": "antonio_ts_jr",
  "target_arenas": ["linkedin_post", "twitter_thread", "youtube_script", "newsletter"]
}
```

**Response (200)**: an array of `DeliveryBundleV3` objects, one per arena.

### POST /benchmark/run

Run a specific benchmark case.

**Request body**:

```json
{
  "case_id": "GRANT-04",
  "against_version": "2.0"
}
```

**Response (200)**: a `BenchmarkResultV3`.

### GET /manifest

Return the agent manifest.

**Response (200)**: the contents of `agents/agent_manifest.yaml` as JSON.

### GET /schemas/{schema_id}

Return a specific schema.

**Response (200)**: the JSON Schema document.

## Webhooks

Implementations may emit webhooks for:

- `task.completed` — task finished
- `task.blocked` — delivery blocked
- `voice.drift_exceeded` — drift threshold exceeded
- `benchmark.failed` — benchmark case failed

## Rate Limits

Implementation-specific. Reference implementation will enforce per-token quotas.

## Streaming

For long-running compilations, implementations may support Server-Sent Events:

```
GET /compile/stream/{task_id}
```

Emits one event per pass completion with the artifact.

## Author

Antonio T. Smith Jr. / Density6 LLC
