# Scene Graph — Specialization of Architecture Graph

**Use when**: fiction, screenplay, narrative nonfiction, transmedia, audio drama, game cutscene, chapter, or any prose whose primary engine is scene-level cause and effect.

**Parent**: `references/compiler/architecture_graph.md`

---

## What a Scene Graph Adds

A scene graph specializes the architecture graph for narrative cause-and-effect. It tracks beats, dialogue exchanges, power objects, props, plants, payoffs, and the cold-open / turn / button architecture from v2.0 thriller doctrine.

---

## Node Types Specific to Scene Graphs

- `scene_beat` — a discrete action or shift (entrance, reveal, threat, retreat, reversal)
- `dialogue_exchange` — one round of speech with surface and subtext
- `cold_open` — opening that drops the reader into already-moving action
- `the_turn` — the moment the scene's surface story collapses into the operative story
- `the_button` — the closing image, line, or beat that locks the scene
- `image` — a concrete visual anchor (the record player, the second drink, the locked door)
- `plant` — foreshadowing placed for later payoff
- `payoff` — element resolving an earlier plant
- `callback` — reference to earlier element for resonance

---

## Edge Patterns Specific to Scene Graphs

| Pattern | Diagnosis |
|---|---|
| Beat → Beat (cause) | Healthy chain |
| Beat → Beat (no cause) | Episodic — flag |
| Plant → ... → Payoff | Resolves the foreshadowing ledger |
| Cold Open → Beat → Beat → Turn → Beat → Button | Five-beat thriller architecture |
| Image → Image (recurring) | Motif — track in storyworld memory |
| Power object → Holder change | Migration; logs to power_objects in storyworld memory |

---

## Audit Questions (Per v2.0 Doctrine, Now Formalized)

### Setting
- Is the space an active force or a dead backdrop?
- Does it constrain action, generate threat, or change power relations?

### Props
- Does every named object serve 2+ functions?
- Does any prop migrate (change holders) during the scene?
- Is the prop tied to identity, deception, or reveal?

### Power Dynamics
- Is there an identifiable power object?
- Does it migrate during the scene?
- Are power shifts staged through space (sitting / standing / blocking)?

### Dialogue Layers
- Does every exchange operate on surface + subtext?
- Are at least 2 of the 9 tension elements active?
- Can the reader identify the speaker with names removed?

### Pacing
- Does the scene follow a compression sequence (normalcy → friction → pressure → false relief → fatal detail → silence → explosion → aftermath)?
- Where is the turn? Is it earned by setup?

### Foreshadowing
- Are climactic details planted earlier in the scene or in prior scenes?
- Are plants invisible at the time of planting?

### Character Roles
- Can every character be mapped to one of the 12 archetypes?
- Are 4+ roles deployed in the scene?
- Does any character's archetype shift mid-scene without cause?

### Identity / Deception
- If applicable, do surface and operative narratives coexist?
- Is there an "operative second drink" — something that reads as ordinary on the surface and as signal in the operative read?

### The Fatal Detail
- Is there a single small-scale trigger with enormous consequences?
- Is it ironic — a thing the audience saw and didn't notice?

### Aftermath
- Does the final image, line, or beat burn into memory?
- Does the scene close with a button, not a fade?

---

## Confined-Space Scene (Thriller / Suspense)

When the scene is confined (basement tavern, locked car, elevator, motel room), apply `references/genre_packs/thriller_scene_architecture.md`. The scene graph adds:

- `confinement_node` — the constraint itself acts as antagonist
- `escape_attempt` — beats where a character tries to break the constraint
- `confinement_break` — final reversal: who escapes, who is trapped, who chose to stay

---

## Storyworld Memory Hooks

After Pass 4 builds the scene graph, the Narrative Architect (Pass 11) updates `storyworld_memory.schema.json`:

- New character entries
- Updated power-object migration log
- Updated foreshadowing ledger (planted / paid off / orphaned)
- Updated motif appearances
- Updated terminology lock

This is how series continuity holds across sessions and across books.

---

## Definition of Done

The scene graph passes when:

- Every scene beat has either causal incoming or causal outgoing edges (no dead beats).
- Every plant has a payoff (within the scene, the chapter, or the storyworld memory's open-ledger queue).
- Every payoff has a plant.
- At least one power object is identified and its migration logged.
- Setting is auditable as a force, not a backdrop.
- Dialogue exchanges average 2+ active tension elements.
- The button is identified.
