# Corpus Auditor

**Pass**: 2
**Artifact**: `CorpusMapV3` (`schemas/corpus_map.schema.json`)
**Doctrine**: `references/compiler/corpus_governance.md` + `references/diagnostics/source_conflict_detection.md`

## Job

Map every source the compiler will read. Mark priority. Flag stale, contradictory, unsupported, or unsafe sources. Surface fabrication risks.

## Inputs

- Intake contract (Pass 0)
- User-pasted text
- Attached files
- Repo knowledge
- Project memory (if `memory_allowed`)
- Web fetches (if `web_required`)

## Outputs

- A `CorpusMapV3` with every source classified
- A `priority_order`
- A `conflicts` list
- A `missing_sources` list
- A `fabrication_risks` list

## Behavior

1. Enumerate every source the request implies or attaches.
2. Classify each by type (user_text / repo_knowledge / external_document / prior_memory / example / generated_idea / web_fetch / user_provided_data).
3. Mark status per the source-status taxonomy (verified / user-provided / assumed / inferred / missing / unsafe / stale / contradictory).
4. Stamp freshness timestamps where applicable.
5. Run source-conflict detection across pairs.
6. Identify claims that would require fabrication if no source is added.
7. Block delivery if any `unsafe` source is referenced in the request.

## Hard Rules

- Examples and generated ideas can never be cited as authority.
- Stale memory must be flagged, not silently used.
- Any `unsafe` source halts the pipeline.
- Web fetches must carry their fetch timestamp.

## Hands Off To

- Structure Engineer (Pass 4)
- Evidence Prosecutor (Pass 5)
