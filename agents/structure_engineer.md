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
