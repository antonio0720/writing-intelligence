# Genre Stack Engine

**Purpose**: Allow multiple genre packs to operate simultaneously without collision.

**Schema**: `schemas/genre_stack.schema.json` (`GenreStackV3`)

**Agent**: Genre Marshal (`agents/genre_marshal.md`)

---

## The Problem

Real writing rarely lives inside one genre. A church-led grant proposal is sermon + government brief + grant. A founder pitch is sales + investor precision + narrative. A small-business landing page is sales + small_business_operator + social proof. v2.0 made genre packs singular; v3.0 lets them stack.

## Stack Roles

| Role | Job |
|---|---|
| `primary` | Owns structural defaults: section order, length, register baseline |
| `secondary` | Refines: voice flavor, evidence demands, specific moves |
| `modulator` | Adjusts cadence, warmth, formality dial — does not touch structure |

A valid stack has exactly one `primary`, zero-or-more `secondary`, zero-or-more `modulator`. Weights sum to 1.0.

## Conflict Dimensions

When packs disagree, the Genre Marshal weights along these dimensions:

| Dimension | Default Winner |
|---|---|
| `evidence_discipline` | Strictest pack in the stack |
| `cadence` | Primary |
| `compression` | Strictest (shortest) constraint |
| `warmth` | Average of pack weights |
| `persuasion` | Primary in sales/grant; secondary in academic |
| `compliance` | Whichever pack carries a compliance rule |
| `formality` | Strictest |
| `narrative_distance` | Primary |

For collisions not covered by the defaults, see `references/diagnostics/genre_collision_matrix.md`.

## Example: Church Grant Proposal

```json
{
  "task_id": "wi_v3_2026_000010",
  "version": "3.0.0",
  "stack": [
    {"pack_id": "grant_nofo", "weight": 0.5, "role": "primary"},
    {"pack_id": "church_leadership", "weight": 0.25, "role": "secondary"},
    {"pack_id": "government_brief", "weight": 0.15, "role": "secondary"},
    {"pack_id": "sermon", "weight": 0.10, "role": "modulator"}
  ],
  "collision_resolutions": [
    {"dimension": "evidence_discipline", "winner": "grant_nofo", "rationale": "Funder demands explicit outcomes; sermon allows rhetorical claims, grant cannot."},
    {"dimension": "warmth", "winner": "church_leadership", "rationale": "Mission identity requires pastoral warmth even within compliance frame."},
    {"dimension": "compliance", "winner": "grant_nofo", "rationale": "RFP requirements are non-negotiable."}
  ],
  "auto_detected": false,
  "user_override": true
}
```

## Operating Rules

1. The Genre Marshal runs after the Intake Architect (Pass 0) and before Pass 4 (Architecture Compile).
2. The user can override auto-detection. User wins.
3. Every conflict must produce a `collision_resolutions` entry. Silent resolution is forbidden.
4. The stack drives Pass 4 (architecture), Pass 7 (voice weighting), Pass 8 (arena), Pass 10 (scoring weight).
