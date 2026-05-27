# Architecture Graph Engine — Pass 4

**Purpose**: Replace loose structural advice with explicit graphs of nodes (sections, paragraphs, claims, beats) and edges (supports, contrasts, escalates, resolves, foreshadows, pays off).

**Schema**: `schemas/architecture_graph.schema.json` (`ArchitectureGraphV3`)

**Agent**: Structure Engineer (`agents/structure_engineer.md`)

---

## Why a Graph

Prose feels linear. Argument and narrative are graphs. v2.0 audited structure by reading sections in sequence. v3.0 builds the actual dependency graph so orphan sections, unsupported claims, dead scenes, repeated beats, unpaid plants, and unplanted payoffs are detectable in finite time.

---

## Graph Types

| Type | When to Build |
|---|---|
| `section` | Any structured prose: memo, brief, article, manifesto |
| `argument` | Persuasive prose, academic writing, op-ed, position paper |
| `scene` | Single fiction scene |
| `chapter` | Fiction chapter |
| `series` | Multi-chapter or multi-book work |

The graph type is chosen by the Structure Engineer from the genre stack. Multiple graphs may coexist for the same task (e.g., a thriller chapter has both a `scene` graph and a chapter-level `argument` graph for the thematic spine).

---

## Node Types

| Node | Used In | Purpose |
|---|---|---|
| `section` | section / argument | Top-level block with a declared job |
| `paragraph` | all | Unit of prose with a single function |
| `claim` | argument | Assertion that requires support |
| `premise` | argument | Sub-claim that supports a parent claim |
| `evidence` | argument | Sourced fact, citation, data point |
| `scene_beat` | scene / chapter | Discrete action / shift within a scene |
| `dialogue_exchange` | scene / chapter | One round of speech with subtext |
| `proof_point` | argument / pitch | Compressed evidence + claim packaged for impact |
| `image` | all | Concrete visual anchor |
| `callback` | all | Reference back to an earlier element |
| `plant` | chapter / series | Foreshadowing inserted now for payoff later |
| `payoff` | chapter / series | Element that resolves an earlier plant |
| `transition` | all | Bridge between sections |
| `opening` | all | First node, must earn the next 30 seconds |
| `closing` | all | Last node, must leave residue |

Every node carries a `purpose` (define / prove / contrast / narrate / warn / persuade / operationalize / close / escalate / resolve / reveal / foreshadow / pay_off / interrogate / comfort).

---

## Edge Types

| Edge | Meaning |
|---|---|
| `supports` | A → B: A provides backing for B |
| `contrasts` | A → B: A creates contrast against B |
| `escalates` | A → B: A raises stakes leading into B |
| `resolves` | A → B: A resolves tension created by B |
| `foreshadows` | A → B: A is a plant for B |
| `pays_off` | A → B: A is the payoff for B |
| `transitions_to` | A → B: A bridges into B |
| `depends_on` | A → B: A cannot stand without B |
| `rebuts` | A → B: A counters B |
| `complicates` | A → B: A adds complexity to B |

Each edge carries a `strength` (0 to 1). Strong edges (>0.7) indicate load-bearing relationships.

---

## Diagnostics

The Architecture Graph Engine emits a `diagnostics` block:

- `orphan_nodes` — nodes with no incoming or outgoing edges
- `unsupported_claims` — claim nodes with no `supports` edge from evidence or premise
- `dead_scenes` — scene beats with no causal edge to any other beat
- `repeated_beats` — beats that duplicate other beats without escalation
- `unpaid_plants` — `plant` nodes with no matching `pays_off` payoff
- `unplanted_payoffs` — `payoff` nodes with no preceding plant

A high-stakes piece cannot pass Pass 4 with any `unsupported_claims`. A fiction piece cannot pass Pass 4 with `unpaid_plants` or `unplanted_payoffs` unless explicitly intentional (rare).

---

## Building the Graph

The Structure Engineer's procedure:

1. Identify the graph type from the genre stack.
2. Walk the draft top-to-bottom. For each unit (paragraph or beat), instantiate a node with a declared purpose.
3. For each node, identify edges to prior nodes.
4. Run the diagnostics.
5. If any diagnostic fails, surface to Pass 9 (Stress Test) for review. If it can be fixed via a Pass 6 rewrite, queue the fix.

---

## Example: Argument Graph for a Persuasive Memo

```json
{
  "task_id": "wi_v3_2026_000002",
  "version": "3.0.0",
  "graph_type": "argument",
  "nodes": [
    {"node_id": "n1", "type": "opening", "label": "Hook: 'The funder doesn't want a story. They want proof.'", "purpose": "define"},
    {"node_id": "n2", "type": "claim", "label": "Our model produces measurable outcomes per dollar.", "purpose": "prove"},
    {"node_id": "n3", "type": "evidence", "label": "FY25 results: 312 households served at $2,140/household.", "purpose": "prove"},
    {"node_id": "n4", "type": "evidence", "label": "Independent eval: 89% retention at 12 months.", "purpose": "prove"},
    {"node_id": "n5", "type": "claim", "label": "We can scale 3x with this funding.", "purpose": "persuade"},
    {"node_id": "n6", "type": "premise", "label": "Operational capacity is built; bottleneck is capital.", "purpose": "operationalize"},
    {"node_id": "n7", "type": "closing", "label": "The ask: $642K, FY26-FY27.", "purpose": "close"}
  ],
  "edges": [
    {"from": "n3", "to": "n2", "relation": "supports", "strength": 0.9},
    {"from": "n4", "to": "n2", "relation": "supports", "strength": 0.85},
    {"from": "n2", "to": "n5", "relation": "depends_on", "strength": 0.95},
    {"from": "n6", "to": "n5", "relation": "supports", "strength": 0.8},
    {"from": "n5", "to": "n7", "relation": "transitions_to", "strength": 0.9}
  ],
  "diagnostics": {
    "orphan_nodes": [],
    "unsupported_claims": [],
    "dead_scenes": [],
    "repeated_beats": [],
    "unpaid_plants": [],
    "unplanted_payoffs": []
  }
}
```

---

## Definition of Done

The Structure Engineer produces a graph that:

- Validates against `architecture_graph.schema.json`
- Contains at least an `opening` and a `closing` node
- Resolves every diagnostic or queues a fix
- Survives the orphan check, unsupported-claim check, dead-scene check, repeated-beat check, plant-and-payoff balance check

If any of the above fails, Pass 4 has not completed.
