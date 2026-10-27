# Writing Intelligence v3.0 — Builder Guide

For the developer integrating Writing Intelligence into a product, editor, CI pipeline, MCP server, multi-agent system, or custom workflow.

## What v3.0 Gives You

- 11 JSON Schema definitions describing every pass artifact
- An agent manifest declaring the 12 specialist agents, their dependencies, and conflict-resolution rules
- A benchmark harness for quality regression
- A canonical kernel (`SKILL.md`) that any LLM can execute
- Doctrine files that drive the kernel's decisions

## Integration Paths

### Path 1 — Embed the Skill

Drop `SKILL.md` + `references/` + `schemas/` into your prompt context. The LLM executes the kernel. Use the user's intake contract to control the run.

Best for: chat-style integrations, AI assistants, ghostwriting tools.

### Path 2 — Programmatic Execution

Parse the schemas. Build a wrapper that:

1. Takes a user request
2. Produces an `IntakeContractV3` (call an LLM with the Intake Architect prompt)
3. For each pass, calls an LLM with the appropriate doctrine excerpt and emits the schema-validated artifact
4. Aggregates results into a `DeliveryBundleV3`

Best for: SaaS products, batch processing, CI hooks.

### Path 3 — MCP Server

Implement Writing Intelligence as a Model Context Protocol server. Expose tools per `docs/mcp/MCP_SPEC.md`. Clients (Claude Desktop, Claude Code, custom agents) call them.

Best for: editor integrations, agentic workflows, multi-tool orchestration.

### Path 4 — Multi-Agent Orchestration

Use the Claude Agent SDK (or any orchestration framework). Each of the 12 agents becomes a sub-agent. Use `agents/agent_manifest.yaml` for dependencies. The Orchestrator coordinates handoffs.

Best for: high-quality, audit-grade output where each agent's decision is logged and reviewable.

## Schema-First Discipline

Every consumer of Writing Intelligence v3.0 should validate inputs and outputs against the canonical schemas:

```python
import jsonschema
import json

intake_schema = json.load(open("schemas/intake_contract.schema.json"))
contract = {...}
jsonschema.validate(contract, intake_schema)
```

If validation fails, surface to the user. Do not silently coerce.

## Common Patterns

### Pattern: Auditing Before Publishing

```
1. User submits draft
2. Run intake contract with mode: audit
3. Run through Pass 10; emit scorecard + epistemic ledger + violations
4. If score ≥ 85 and no delivery_block: green-light
5. If score < 85 or block present: send back with findings
```

### Pattern: CI Writing Check

```
1. On every PR that touches user-facing copy:
2. Extract changed strings
3. Run intake contract per string with audit mode
4. Fail the PR if any string scores < 70 or triggers a delivery_block
5. Comment the scorecard on the PR
```

### Pattern: Team Voice Enforcement

```
1. Maintain a team voice fingerprint in the project
2. Every author's submission runs against the fingerprint
3. Editorial dashboard surfaces drift reports
4. Editor approves voice variance per contributor
```

### Pattern: Multi-Arena Distribution

```
1. Approved canonical piece sits in CMS
2. Editor triggers cross-arena repackage
3. System runs Pass 8 producing delivery bundles per arena
4. Bundles route to: scheduling tools (social), CMS (blog), email platform (newsletter), etc.
5. Each bundle carries its voice fingerprint stamp
```

## Performance Considerations

- The 11-pass kernel is heavy. A single run can take 30-60 seconds with a frontier model.
- Cache intake contracts and voice fingerprints; they're stable across sessions.
- Run benchmark cases asynchronously; don't block user-facing requests.
- Multi-arena bundles benefit from parallel execution per arena.

## Schema Backwards Compatibility

v3.0 schemas declare `version: "3.0.0"`. v3.x.y will maintain backwards compatibility:

- New optional fields may be added (consumers must ignore unknown fields)
- No required fields will be removed within the v3 major
- Breaking changes require a v4 major

## Reference Implementations Coming

In v3.1 (target Q3 2026):

- Python FastMCP server
- Node MCP SDK server
- CLI binary (Go or Rust)
- Reference OpenAPI 3.1 server (Python / FastAPI)

Track progress in `ROADMAP.md`.

## Building Custom Domain Packs

See `docs/DOMAIN_PACK_GUIDE.md` for the 15-section domain pack schema and contribution flow. Custom packs can be merged upstream via the RFC process.

## Building Custom Voiceprints

See `docs/VOICEPRINT_GUIDE.md` for the measurable fingerprint requirement.

## Building Custom Agents

Follow the agent spec format in `agents/*.md`. Each agent must declare:

- Job
- Input refs (from prior agent artifacts)
- Output artifact (schema-validated)
- Hard rules
- Conflict resolution

## Author

Antonio T. Smith Jr. / Density6 LLC

## v9 preview: building on the authorship tools

*Preview (PR #8); proposed, not a release. v8.0.0 is the published version.* The v3.0 material above is unchanged; this section covers integrating the two v9 tools you can run today. Reference: [`../references/v9/README.md`](../references/v9/README.md).

### `scripts/wi-authorship.py` exit codes

| Command | Outcome | Exit |
|---|---|---|
| `audit --input dossier.json` | `REVIEW` (limited checks passed; not permission to send) | 0 |
| `audit --input dossier.json` | `HOLD` | 3 |
| `release --input dossier.json` | `RELEASE_ELIGIBLE` (transmits nothing) | 0 |
| `release --input dossier.json` | `HOLD` | 3 |

Treat any other non-zero exit as a failed run, not a pass. Parse the JSON report rather than the exit code alone, and branch on the verdict word.

### Rules for a builder

- **Validate the dossier first** against `schemas/v9/authorship-dossier.schema.json` (`wi9-authorship-2`; `wi9-authorship-1` is still read). Surface validation errors; do not coerce.
- **Resolve paths relative to the dossier directory.** The checker refuses symlinks and needs POSIX `O_NOFOLLOW`; it will not run on Windows. Plan for Python 3.8+.
- **Pin the draft.** A submission needs `expected_sha256`; recompute it at send time, not only at audit time.
- **Never read `REVIEW` or `RELEASE_ELIGIBLE` as a send.** Sending is a separate, human-authorized step in your product.
- **Show `declaration_status: self_reported`** wherever you show a verdict. Do not label a result "verified author" or "human-written".
- **Do not build a detector-score field** into your UI or pipeline as a target, gate or claim (WI9-H). A vendor score may be stored as an optional diagnostic with vendor, version and date.

### Experimental kernel

`prototypes/wi9/` (`wi9_hotphrases.py scan`, `wi9_phrase_review.py`, `wi9_composition.py`, `wi9_core.py`) is the owner's reference kernel, not the CLI. A scan match is an editorial question and must be shown as one; a build must not auto-rewrite on a match. The composition contract refuses `human_only` venues and its best state is `DRAFT_REVIEW_REQUIRED`.

Verify an integration against the repo's own suite: `python3 -m unittest discover -s tests/v9 -p 'test_*.py'`. What is not yet true: no benchmark against editors (WI9-07 has not run), no consented author corpus, and no external review.
