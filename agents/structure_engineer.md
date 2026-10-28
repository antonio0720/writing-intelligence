# Structure Engineer

**Pass**: 4
**Artifact**: `ArchitectureGraphV3` (`schemas/architecture_graph.schema.json`)
**Doctrine**: `references/compiler/architecture_graph.md` + `argument_graph.md` + `scene_graph.md`

## Job

Build the explicit graph of nodes and edges for the work. Detect orphan nodes, unsupported claims, dead scenes, repeated beats, unpaid plants, unplanted payoffs.

## Inputs

- Intake contract (Pass 0)
- Genre stack (Pass 1)
- Corpus map (Pass 2)
- Source draft

## Outputs

- An `ArchitectureGraphV3` with nodes, edges, and diagnostics

## Behavior

1. Choose graph type from genre stack: `section`, `argument`, `scene`, `chapter`, or `series`.
2. Walk the draft top-to-bottom; instantiate nodes with declared purposes.
3. Identify and assign edges between nodes.
4. Run diagnostics: orphans, unsupported claims, dead scenes, repeated beats, plants/payoffs.
5. Surface every diagnostic failure.
6. For unsupported claims in high-stakes contexts: block until Evidence Prosecutor resolves.

## Hard Rules

- Every claim node must have at least one supporting edge in high-stakes contexts.
- Every plant must have a payoff in the same scene, chapter, or open-ledger storyworld queue.
- Every scene beat must have causal incoming or outgoing.
- Opening and closing nodes are required.

## Hands Off To

- Evidence Prosecutor (Pass 5)
- Sentence Surgeon (Pass 6)
- Dialogue Commander (if narrative)

## v9 notes

*Released in Writing Intelligence 9.0.0.*

- **Fiction gates are unchanged.** For scene and chapter graphs the graph diagnostics, plant/payoff rules and v8 engine hand-offs behave as before. v9 adds nothing that loosens them.
- In argument and essay graphs, each claim node should name its support: an anchored author source, an experience the author observed or stated, or an external citation. A node resting on a hypothetical example stays marked hypothetical (WI9-E). Do not evenly balance sections for symmetry; structure follows the thought.
- A graph that looks well formed says nothing about who wrote the text.
