# The Storyworld OS

**Status: canon graph specified; `wi test` canon rules executable.**

`StoryworldMemoryV3` is a document. It is a good document — it records characters, motifs, power objects, a foreshadowing ledger, a series arc and a terminology lock, and a writer who returns to it after six months can resume mid-chapter without re-reading the series. What it cannot do is refuse a scene. It is read by a person, updated by a pass, and it has no mechanism by which a contradiction becomes a finding.

v5 makes it a graph-backed persistent runtime.

The claim this document rests on, stated first because everything else follows from it:

> **Nonfiction evidence and fictional canon belong in the same infrastructure — and must never be treated as the same epistemic category.**

Both are dependency-controlled authored worlds. A grant narrative binds its claims to external sources; a novel binds its claims to declared canon. In both cases a statement has a truth value, that truth value is fixed by something outside the sentence, an edit somewhere else can falsify it, and a reader can be handed the thing it rests on. That is one problem. It wants one graph, one identity model, one invalidation engine and one set of writing tests.

What differs is the binding target, and the difference is total. An `external_fact` claim binds to `source.version` states the author did not write and cannot change. A `fictional_canon` claim binds to `canon.*` states the author wrote and may change at will — but not silently, and not without knowing what breaks. The realm is what keeps them apart. `fictional_canon` is defined in [`CONSTITUTION.md`](CONSTITUTION.md) §6, it travels with every canonical claim atom, and no renderer may drop it for space.

Read this with [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) for the `canon.*` node family and the narrative edges, and with [`../compiler/storyworld_memory.md`](../compiler/storyworld_memory.md) for the v3 doctrine this preserves.

---

**Contents:** canon states · the event timeline · the character state machine · the canon compiler · canon conflict · transmedia propagation · plants and payoffs · canon writing tests · realm safety · series and adaptation forks · executable vs. specified.

---

## 1. Canon states

**Status: specified.**

`StoryworldMemoryV3` carries a three-tier canon hierarchy: `canonical`, `sanctioned`, `fan_tier`. All three are preserved with their meanings unchanged. v5 adds six more, because a three-tier hierarchy can say what is in the canon and cannot say what is *happening to* the canon while a series is being written.

| State | Used when | May govern |
|---|---|---|
| `canonical` | The author has fixed this as true in the primary world | Every check, every conflict, every gate |
| `sanctioned` | An author-approved extension — an audio drama, a licensed novella | Checks within its own line; raises `review` against primary canon, never overrides it |
| `fan-tier` | Community material the author acknowledges but has not adopted | Nothing. Recorded for reference; never a conflict basis |
| `proposed` | Drafted but not yet accepted by the author | Nothing until accepted. Visible to the compiler as a candidate, marked as such |
| `deprecated` | Superseded by later canon, retained for provenance | Historical queries only. Never admissible state for a new scene |
| `retconned` | Deliberately replaced; the replacement and the replaced are both recorded | The replacement governs. The retconned state governs all pre-discovery renderings |
| `disputed` | Two canonical states conflict and the author has not chosen | Nothing. It is a reportable condition that blocks under `regulated` canon policy |
| `adaptation-only` | True in a named adaptation and not in source canon | Checks within that adaptation's fork only |
| `simulation-only` | True inside a declared model, scenario or projection | Checks within the `simulation` realm only |

**Why the six additions are load-bearing.** A three-state hierarchy forces every in-progress decision into `canonical` or into nothing, and writers do not work that way. A fact considered but not adopted becomes either a premature commitment or an untracked note in a file the graph never sees. `proposed` gives a candidate fact an identity so it can be queried, tested against and rejected without ceremony. `deprecated` and `retconned` are separate because they answer different questions: `deprecated` means *this stopped being true*, `retconned` means *this was made never to have been true*, and only the second one changes the meaning of scenes already written. `disputed` exists because the honest state of a large series is frequently that two canonical statements disagree and nobody has decided — and a system that cannot represent that will resolve it by accident.

---

## 2. The event timeline

**Status: specified.**

A `canon.event` is a thing that happens in world time, independent of the order it is narrated in. This separation is the entire reason a continuity engine can work: chapter order is a rendering decision, and world order is the fact being rendered.

Every canonical event supports:

| Field | Holds |
|---|---|
| `earliest` / `latest` | The bounds of when it happened in world time |
| `precision` | `exact` or `approximate` — whether the bounds are the fact or an estimate |
| `participants` | The `canon.character` logical ids present or acting |
| `location` | The `canon.location` logical id |
| `causal_predecessors` | Events that must have occurred first, as `causes` edges |
| `consequences` | Events this one brings about |
| `appearances` | The `structure.*` nodes that narrate it, in any work, in any medium |

```json
{
  "logical_id": "0192f4c8-1b30-7a44-9e02-6d71c3f8a015",
  "node_type": "canon.event",
  "state_digest": "sha256:e41b7c0d92a5f386b1c4d7e0a3f6b9c2d5e8f1a4b7c0d3e6f9a2b5c8d1e4f7a0",
  "payload": {
    "label": "Marek dies at the Verrin crossing",
    "canon_state": "canonical",
    "realm": "fictional_canon",
    "time": {
      "earliest": "Y12-D204",
      "latest": "Y12-D204",
      "precision": "exact",
      "calendar": "verrin-reckoning"
    },
    "participants": ["ch-marek", "ch-aria", "ch-solen"],
    "location": "loc-verrin-crossing",
    "causal_predecessors": ["ev-0119"],
    "consequences": ["ev-0142", "ev-0151"],
    "appearances": [
      {"work": "book-2", "unit": "structure.scene sc-0233", "mode": "narrated"},
      {"work": "audio-drama-s2", "unit": "structure.scene sc-a-0071", "mode": "narrated"},
      {"work": "lore-bible", "unit": "structure.section se-0018", "mode": "summarized"}
    ]
  }
}
```

**Why `earliest` and `latest` instead of a date.** Most canonical events are not dated and never will be. "Some months after the crossing" is a real constraint that orders events without fixing them, and a system that demands a timestamp will get an invented one. An interval with `precision: approximate` records exactly as much as the author knows, which means the ordering test can check what is checkable and stay silent about what is not. A totally ordered timeline is available where the author declares it and is never fabricated where they did not.

---

## 3. The character state machine

**Status: specified.**

A character is not a static record. `StoryworldMemoryV3` gives each character an archetype, a voice fingerprint, tells, a fatal vulnerability and an arc state — all of which are properties of the character across the whole work. v5 keeps every one of them and adds the thing continuity actually needs: **state as a function of time.**

Tracked over world time, per character:

| Dimension | Why it is tracked |
|---|---|
| `vitality` | `alive` · `dead` · `unknown` — the state most often broken and most visibly |
| `location` | Where they are, at a `canon.location`, over an interval |
| `knowledge` | What they know, and the event at which they learned it |
| `allegiances` | Who they are working for, and against |
| `injuries` | Standing physical state, with the event that caused it |
| `possessions` | What they hold, cross-referenced against `canon.object` migration |
| `relationships` | Standing relation to other characters, typed and directional |
| `public_identity` | Who the world believes they are |
| `secret_identity` | Who they actually are, and which characters know it |
| `emotional_commitments` | What they have bound themselves to caring about |
| `open_promises` | What they have said they will do, and to whom |
| `unresolved_conflicts` | What they are still in the middle of |

A state record is an interval assertion, not a field on the character:

```json
{
  "logical_id": "0192f4c8-1b30-7a44-9e02-71a0d3c5f882",
  "node_type": "canon.character_state",
  "payload": {
    "character": "ch-aria",
    "canon_state": "canonical",
    "realm": "fictional_canon",
    "valid_from": "ev-0142",
    "valid_until": "ev-0187",
    "vitality": "alive",
    "location": "loc-northgate-safehouse",
    "knowledge": [
      {"fact": "kn-marek-dead", "acquired_at": "ev-0142", "certainty": "witnessed"},
      {"fact": "kn-ledger-exists", "acquired_at": "ev-0131", "certainty": "inferred"},
      {"fact": "kn-ledger-named-red", "acquired_at": null, "certainty": "unknown"}
    ],
    "allegiances": [{"party": "org-northgate", "stance": "covert", "since": "ev-0119"}],
    "injuries": [{"kind": "left hand, burn", "since": "ev-0142", "healed_at": null}],
    "possessions": ["obj-solen-key"],
    "relationships": [{"to": "ch-solen", "type": "debt_owed", "direction": "outbound"}],
    "public_identity": "id-aria-courier",
    "secret_identity": {"id": "id-aria-northgate", "known_to": ["ch-solen"]},
    "emotional_commitments": ["cm-protect-solen"],
    "open_promises": [{"promise": "pr-0022", "to": "ch-solen", "status": "open"}],
    "unresolved_conflicts": ["cf-0009"]
  }
}
```

**`knowledge` is the field that catches most continuity breaks, and it is the field most systems do not have.** Death is checked by everyone; a dead character speaking is caught by a reader on the first pass. What is not caught is a character acting on information they have not been given — referring to a name they have not heard, reacting to a death they were not told about, recognizing a face they have never seen. This is the most common continuity failure in long-form and multi-author work, it survives copy-editing, it survives beta readers, and it is invisible in a diff because every individual sentence is fine. It is only detectable against a model of what each character knew at each point, which is exactly what `knowledge` with an `acquired_at` provides. A `knowledge` entry with `acquired_at: null` is not missing data — it is the positive assertion that the character does not know this, and it is what makes the check possible.

---

## 4. The canon compiler

**Status: specified.**

Before a scene is written, the admissible state is compiled. Not recalled, not summarized into a prompt — compiled, from the `canon.*` nodes valid at the scene's position in world time, into a constraint set.

```
$ python3 scripts/wi.py canon query --at "Book 2/Chapter 7" \
      --character aria --fields knowledge,location,possessions

Canon state · storyworld sw-verrin · realm fictional_canon
Position: Book 2/Chapter 7  →  world time Y12-D211 (after ev-0142, before ev-0187)
Canon states admitted: canonical, sanctioned(audio-drama-s2)
Canon states excluded: proposed(3), adaptation-only(1), fan-tier(6)

aria — ch-aria — alive

  location
    loc-northgate-safehouse            since ev-0142      canonical

  possessions
    obj-solen-key                      since ev-0128      canonical
    obj-red-ledger                     NOT HELD           last held ch-marek @ ev-0139

  knowledge
    kn-marek-dead                      since ev-0142      witnessed    canonical
    kn-ledger-exists                   since ev-0131      inferred     canonical
    kn-northgate-compromised           since ev-0151      told         sanctioned(audio-drama-s2)
    kn-ledger-named-red                NOT KNOWN          first named to aria @ Chapter 9

Constraints:
  · aria cannot reference the red ledger by name; first named to her in Chapter 9
  · marek cannot act, speak or be present; died at ev-0142 (Book 2/Chapter 5)
  · aria's left hand is burned since ev-0142; physical business must account for it
  · aria owes ch-solen a debt (rel-0031, outbound, open) — unresolved at this position
  · kn-northgate-compromised is sanctioned-tier only; using it in primary canon
    promotes an audio-drama fact and requires an author decision

Checks run: vitality · knowledge acquisition · possession custody · location interval · promise state.
Not run: motif density, voice drift (require the drafted scene, not the canon state).
```

**This is a hard continuity constraint compiled from prior canon nodes. It is not a soft memory prompt, and the difference is the whole point of the section.** A memory prompt is a paragraph of context placed in front of a generator in the hope that it will be respected; when it is not, nothing happens, because nothing was checking. A compiled constraint is a machine-readable set with a source node behind every line, it is produced by walking the graph rather than by remembering, and it is the same object the writing tests evaluate the finished scene against. The author never has to trust that the constraint was honored. The constraint is re-run against the text.

The last line of the constraint block is the pattern worth noticing: the compiler does not silently blend a `sanctioned` fact into primary canon. It admits it, marks its tier, and states what using it would cost. Tier promotion is an authorship decision under Law J, and the compiler's job is to put the decision in front of a person, not to make it.

---

## 5. Canon conflict

**Status: canon rules executable in `scripts/wi.py` via `wi test`; the conflict router is specified.**

Work the example fully, because the routes are the part that matters.

**Scene text, Book 2, Chapter 7:**

> *Marek handed Aria the red ledger.*

**Canon at that position:** Marek died at `ev-0142`, narrated in Book 2, Chapter 5. Aria has not learned the ledger's name; it is first named to her in Chapter 9.

The system emits **two separate typed conflicts.** They are separate because they have different causes, different blast radii and different repairs, and merging them into one "continuity error" would force the author to fix both the same way.

```
$ python3 scripts/wi.py test --scene sc-0261

2 canon conflicts.

[1] actor_continuity                                       WI_CLAIM_CONFLICTED
    ch-marek acts at Book 2/Chapter 7 (world time Y12-D211)
    ch-marek vitality = dead since ev-0142 (Book 2/Chapter 5, canonical)
    span: "Marek handed Aria"  ·  rule: no_character_post_death_without_exception
    blast radius: 1 scene, 0 downstream artifacts

[2] knowledge_continuity                                   WI_CLAIM_CONFLICTED
    text names obj-red-ledger to ch-aria at Book 2/Chapter 7
    kn-ledger-named-red acquired_at = null at this position;
    first named to ch-aria at Book 2/Chapter 9 (ev-0203, canonical)
    span: "the red ledger"  ·  rule: no_knowledge_before_acquisition
    blast radius: 1 scene, 2 downstream artifacts (audio-drama-s2 ep-07, lore-bible se-0018)

Routes (per conflict, no default taken):

  change_the_scene       Rewrite the span so it no longer asserts the conflicting state.
                         [1] another character hands over the ledger.
                         [2] refer to it as "the ledger" — unnamed reference is admissible.
  retcon_canon           Move or replace the canon node. [1] move ev-0142 later than
                         Y12-D211. Impact walk before accepting: 14 nodes, 3 works.
  change_viewpoint       Re-anchor the scene to a viewpoint for which the state holds.
                         [2] narrate from ch-solen, who knows the name at this position.
  reveal_an_exception    Declare a canon.rule that admits the state, scoped and recorded.
                         [1] "marek survives ev-0142 concealed" — a canonical exception,
                         not a suppression; every prior scene depending on his death
                         enters review.

No route applied. Canon is unchanged.
```

**The rule: the system never fixes canon silently.** Not by choosing the cheapest route, not by preferring the newest text, not by weakening a `canonical` state to `disputed` to make a gate pass. Every one of the four routes is an authorship decision under Law J, recorded against the exact state it resolves. A continuity engine that repairs a contradiction on its own has replaced the author's world with its own preference for consistency, and it has done so in the one domain where the contradiction might have been the point. Authors break their own canon deliberately. The system's job is to make sure it was deliberate.

The fourth route is worth its own sentence. `reveal_an_exception` is not a suppression flag. It creates a `canon.rule` node with a scope, and that rule is itself canon — checkable, queryable, and capable of being contradicted later. An exception that is not part of the world is a lie told to the checker.

---

## 6. Transmedia propagation

**Status: specified.**

A retcon is accepted: `ev-0142`, Marek's death, moves from Book 2 Chapter 3 to Book 2 Chapter 4. The question the author needs answered before accepting is not "is this allowed." It is *what else did I just change.*

```
$ python3 scripts/wi.py impact --canon ev-0142 --proposed-move "B2/C3 → B2/C4"

canon.event ev-0142  "Marek dies at the Verrin crossing"
  narration position: Book 2/Chapter 3 → Book 2/Chapter 4
  world time unchanged: Y12-D204 (exact)

Affected — states that depend on the discovery point (18):

  novel/book-2      sc-0208, sc-0211            2   post-discovery grief beats now
                                                     precede the discovery       [hard]
  novel/book-3      sc-0417, sc-0429, sc-0433   3   reference "since Marek died"  [review]
  novel/book-4      sc-0602                     1   flashback dated to discovery  [review]
  audio-drama-s2    ep-07 L44, L51, L88         3   lines assume prior knowledge  [hard]
  audio-drama-s3    ep-02 L17                   1   recap line                    [review]
  game/cutscenes    cs-0031, cs-0044            2   dialogue gated on flag
                                                     marek_dead_known             [hard]
  lore-bible        se-0018, se-0033            2   chapter-indexed entries       [review]
  companion-app     tl-0009 … tl-0012           4   timeline entries              [review]

Not affected — pre-discovery scenes (11):

  novel/book-2      sc-0181 … sc-0199           9   narrated before either position
  audio-drama-s2    ep-06 L12, L29              2   pre-discovery, no dependency

Not affected — world-time dependents (6):
  Events ordered against ev-0142 by world time are unmoved; only the narration
  position changed. causes/precedes edges are intact.

Gate consequence if accepted: HOLD on 3 targets (audio-drama-s2, game/cutscenes,
novel/book-2). Minimum repair frontier: 8 nodes.
```

**Why "not affected" is printed at the same weight as "affected."** An impact report that lists only damage teaches the author that every canon change is catastrophic, and an author who believes that stops making canon changes — or stops running the tool. The eleven pre-discovery scenes are the reason the report is usable: they are provably unaffected, the proof is the absence of a dependency edge, and printing them converts an eighteen-item problem into an eight-node repair frontier. This is the same discipline Law I applies to source staleness, applied to canon.

---

## 7. Plants and payoffs

**Status: specified.**

`canon.plant` and `canon.payoff` are first-class nodes, joined by the `foreshadows` and `pays_off` edges defined in [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) §3.5. The v3 `foreshadowing_ledger` — with its `planted` · `paid_off` · `orphaned` · `telegraphed` statuses — is preserved as a view over these nodes.

The two consequences of making them dependency edges rather than ledger rows:

**An unpaid plant is a reportable condition.** Not an error, not a gate block by default — a condition, surfaced with its age and its position. A plant that has been open for two books is a different fact about the work than a plant planted in the last chapter, and the report says which.

```
$ python3 scripts/wi.py test --rule every_plant_has_payoff_or_waiver

3 open plants.

  pl-0007  "the burned hand" B1/C4 → open across 2 books   review-required
  pl-0019  "solen's second key" B2/C1 → open across 1 book  review-required
  pl-0031  "the northgate seal" B3/C9 → open, current book  informational

  1 waived:  pl-0012  waiver w-0004 — "deliberate, series-level, pays off in Book 5"
```

**Cutting a scene that contained a plant makes its payoff review-required.** The `pays_off` edge carries invalidation policy `review`. Delete `sc-0114` and the payoff at `sc-0398` is not deleted, not auto-repaired and not silently orphaned; it enters review with its cause named. This is the failure mode that survives every editorial pass, because the cut looks correct in isolation and the payoff three hundred pages later still reads fine — it just no longer lands on anything. The author who cut the scene is rarely the person reading the payoff.

---

## 8. Canon writing tests

**Status: executable in `scripts/wi.py` via `wi test`.**

Writing tests are declarative rules evaluated against the graph. Canon rules are ordinary writing tests whose scope is `realm: fictional_canon`.

```yaml
# .wi/tests/canon.yaml
version: "5.0"
realm: fictional_canon
storyworld: sw-verrin

tests:
  - id: no_character_post_death_without_exception
    description: >
      A character whose vitality is dead at a position may not act, speak,
      or be present at that position, unless a canon.rule exception admits it.
    scope: canon.character_state
    severity: block
    exception_node_type: canon.rule
    failure_code: WI_CLAIM_CONFLICTED

  - id: no_knowledge_before_acquisition
    description: >
      A character may not reference, act on, or react to a fact whose
      acquired_at is null or later than the position of the scene.
    scope: canon.character_state.knowledge
    severity: block
    applies_to_states: [canonical, sanctioned]
    failure_code: WI_CLAIM_CONFLICTED

  - id: every_plant_has_payoff_or_waiver
    description: >
      Every canon.plant must have a pays_off edge from a canon.payoff, or an
      authorship.waiver bound to the plant's current state.
    scope: canon.plant
    severity: review
    age_thresholds:
      informational: within_current_volume
      review: crosses_volume_boundary
    failure_code: WI_CLAIM_UNSUPPORTED

  - id: timeline_is_totally_ordered_where_declared
    description: >
      Where an author has declared a total order over a set of canon.event
      nodes, no precedes or causes edge may contradict it, and no event's
      [earliest, latest] interval may fall outside its declared position.
    scope: canon.event
    severity: block
    applies_where: declared_total_order
    failure_code: WI_GRAPH_INTEGRITY
```

**`applies_where: declared_total_order` is the important line in the file.** The test does not demand that a timeline be totally ordered. Most storyworlds are partially ordered by design, and a checker that insists on a full order will produce hundreds of findings about facts the author has deliberately left loose. The rule fires only over the subsets where the author has said *these are in this order*, which is where a contradiction is a real defect rather than an unmade decision. Under Law E, an undeclared ordering is not a violated ordering.

Severities map to the gate exactly as they do for external fact: `block` reaches `BLOCK`, `review` reaches `HOLD`, `informational` reaches neither. A canon test is not a lesser test because its realm is fiction.

---

## 9. Realm safety

**Status: specified.**

> **A canonical fictional statement is verified against canon, inside the fictional realm only, and must never render as an externally verified fact.**

The proof output for a canon check says so on its face:

```
c-0771  fictional_canon  ·  storyworld sw-verrin  ·  status: canon_supported

  Supported against canon node ev-0142 (canonical), not against any external source.
  This is a continuity result. It is not a statement about the world.
```

The prohibition is not decorative and it is not primarily about novels. It matters most in four cases where fictional and external material sit inside the same document:

| Case | The specific danger |
|---|---|
| **Transmedia** | A lore-bible entry, a marketing page and a press release are rendered from the same graph. A canon fact reaching a press release with a `verified` badge asserts a fact about the world. |
| **Alternate history** | Every claim is a real place, a real institution and a real date with one thing changed. The realms are interleaved at sentence granularity, and a realm mismatch is invisible to a reader. |
| **Simulation writing** | Scenario output is true *of the model*. Stripped of its realm it becomes a forecast, which is the most consequential realm error available. |
| **Narrative nonfiction** | Reconstructed scenes, composite dialogue and inferred interiority sit beside externally sourced fact in the same paragraph, in the same voice, deliberately. |

**Realm mismatch is itself a finding, not a weak proof.** A claim atom tagged `external_fact` whose only support is a `fictional_canon` anchor fails; it does not degrade to `partially_supported`. And the inverse failure has its own code path: a `fictional_canon` claim that a renderer emits without its realm marker is a rendering defect, caught by the renderer contract in [`SEMANTIC_IR.md`](SEMANTIC_IR.md), not a cosmetic omission. The realm is a required field of the rendering, at every target, at every length. There is no summary short enough to drop it.

---

## 10. Multi-book series and adaptation forks

**Status: specified.**

An adaptation diverges. That is what adaptations are for. The question is whether the divergence corrupts the source canon on its way through the graph, and the answer is the two fork states.

`adaptation-only` marks a canon state true within one named adaptation line and false — or simply absent — in source canon. `simulation-only` does the same for a declared model or scenario. Both create a **fork**: a named canon line with its own admissible-state set, its own tests and its own gate scope.

```
$ python3 scripts/wi.py canon fork --list

sw-verrin                        source canon              1,204 canonical states
  ├── audio-drama-s2             sanctioned                   88 sanctioned states
  ├── screen-adaptation-s1       adaptation-only             141 adaptation-only states
  └── scenario/what-if-marek     simulation-only              19 simulation-only states

$ python3 scripts/wi.py canon diverge --fork screen-adaptation-s1

Divergences from source canon: 23

  ch-solen        merged with ch-tavin              structural   declared  D-0002
  ev-0142         relocated to Y12-D190             timeline     declared  D-0004
  obj-red-ledger  renamed "the accounts"            naming       declared  D-0007
  loc-northgate   omitted entirely                  omission     declared  D-0011
  kn-ledger-named-red
                  acquired 4 scenes earlier         knowledge    UNDECLARED

  22 declared, each with an authorship.decision.
  1 undeclared — this is the finding.

  Undeclared divergence D?  kn-ledger-named-red
    source canon:      acquired at ev-0203 (Book 2/Chapter 9)
    adaptation state:  acquired at ep-05 (equivalent of Book 2/Chapter 5)
    No decision record binds this change.
    Routes: declare_divergence · align_to_source · retcon_source
```

**Divergence is reported, never silently merged.** No write in an `adaptation-only` fork can produce, alter or promote a `canonical` state in source canon. Promotion is a one-way, explicit, recorded operation — an author decision under Law J, with an impact walk in front of it. This is the fork property that makes the whole arrangement usable: the adaptation team can work at speed inside their own line without any possibility of their choices leaking into the novel canon that three other productions depend on.

The undeclared divergence in the output above is the reason the feature exists. A declared change is a creative decision and needs no defense. An undeclared one is usually a mistake, occasionally a drift nobody noticed across two years of production, and always something the author should see before it is shipped in a form that a fan wiki will treat as canon by Tuesday.

For multi-book series, the same machinery answers the series-level question without any new mechanism: a canon state's `valid_from` and `valid_until` are world-time bounds, book boundaries are narration positions, and "what did this character know at the start of Book 4" is a query, not an act of memory. The v3 promise — *return after six months and resume mid-chapter* — is preserved and made mechanical. The addition is that the world can now refuse.

---

## 11. What is executable and what is specified

| Mechanism | Status |
|---|---|
| Writing tests and the `wi test` runner, including canon rule evaluation over graph state | Executable in `scripts/wi.py` |
| Graph identity, invalidation policy and impact walks that canon rules run over | Executable in `scripts/wi.py` |
| The nine canon states | Specified |
| `canon.event` timeline with interval bounds and precision | Specified |
| `canon.character_state` and the twelve tracked dimensions | Specified |
| `wi canon query` and the compiled constraint block | Specified |
| Typed canon conflicts and the four-route conflict router | Specified |
| Transmedia propagation reporting over `wi impact --canon` | Specified |
| `canon.plant` / `canon.payoff` as dependency edges | Specified |
| Canon forks, `adaptation-only`, `simulation-only`, divergence reporting | Specified |
| `StoryworldMemoryV3` as a view over `canon.*` nodes | Specified |

The v3 schema at [`../../schemas/storyworld_memory.schema.json`](../../schemas/storyworld_memory.schema.json) is not deleted and not deprecated. It remains the canonical serialization of the v3 storyworld record; v5 places it over the graph as a view. A project that never adopts the graph loses nothing it had.

---

## Related documents

- [`CONSTITUTION.md`](CONSTITUTION.md) — the epistemic realms, and why `fictional_canon` may never render as external fact
- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — the `canon.*` node family and the narrative edges
- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — claim atoms, realms, and the renderer contract that carries them
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — where storyworld persistence sits in the migration path
- [`../compiler/storyworld_memory.md`](../compiler/storyworld_memory.md) — the v3 doctrine this preserves
- [`../compiler/narrative_intelligence_engine.md`](../compiler/narrative_intelligence_engine.md) and [`../compiler/continuity.md`](../compiler/continuity.md) — the engines that produce and consume canon
- [`../genre_packs/transmedia_character.md`](../genre_packs/transmedia_character.md) — the transmedia pack
- [`../../schemas/storyworld_memory.schema.json`](../../schemas/storyworld_memory.schema.json) — the v3 record; [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
