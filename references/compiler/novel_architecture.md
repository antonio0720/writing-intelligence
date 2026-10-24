# Novel Architecture — additive FI-45 through FI-52 engine contract

**Status:** narrative doctrine plus limited annotated checks in `scripts/fiction_v8/engine.py`. A complete novel parser and canonical graph adapter do not yet exist.

The state of a novel at moment *t* is a typed vector: 

`N(t) = (objective, available_choices, reader_knowledge, protagonist_knowledge, antagonist_knowledge, personal_stakes, external_stakes, relationships, costs, threats, unpaid_promises)`.

A narrative transition is **meaningful** when it changes a causally relevant coordinate or changes the reader's appraisal of one coordinate. It is not required that threat magnitude monotonically increase. A lowered-tension chapter may enlarge attachment, reveal a boundary or restore a choice, and may thus be critical to escalation.

## Scene → act → book transformation

- A scene records what changes and why, who chooses, at what cost, who knows, and what must persist into the next scene.
- An act records a transformation in possibility space: new objective, impossibility, revelation, power change or binding commitment.
- A book records the answer to its opening dramatic contract. Escalation needs novelty, not merely increasing numbers.
- A series records which local questions close and which new unresolved conditions legitimately carry forward; canonical book closure and series appetite are separately evaluated.

### Transition anti-patterns

`identical threat repeated → identical failure → another alarm` is a likely plateau. `defeated enemy → four aftermath chapters repeating that enemy is defeated` is a third-act drag candidate. `final philosophical lecture explaining what the victory means` is an ending-explanation risk. These are **review hypotheses** rather than automatic deletion commands.

## Promise and payoff matching

Opening promises have IDs, domain (dramatic/mystery/emotional/genre), anchor, expected satisfaction class and eventual settlement. Plant/payoff connections require a *causal consequence*, not merely a repeated name. If the payoff is intentionally unresolved, record why, who authorized series deferral, and which book must carry the obligation. A mysterious teaser introduced on the last page is not a substitute for closure to a mystery planted in the first chapter.

## Novel-level measurements are descriptive, not grading formulae

Suggested visual diagnostics: change points in choices, knowledge and relationships; pressure variety; tension recovery intervals; mystery liability over chapters; presence of deliberate motifs; irreversible cost ledger. Plotting these yields information but does not prove reading pleasure. Each alert returns chapter/scene anchors and a falsification question, so an editor can check it against the actual manuscript.

## Manual questions (required for prose judgment)

- What would a reader lose if a flagged scene were removed?
- Does the book's final action cost the protagonist something personally specific?
- Was this emotional condition genuinely altered, or merely described in fresher vocabulary?
- Does the antagonist's capacity remain inside the world rules and resources established earlier?
- Is the reader curious because the author constructed a question, or disoriented because the author withheld orientation?
- Does the final chapter end through events, or explain what the events allegedly mean?

## Failure modes and their proof

A novel may have excellent local prose and yet fail the central resolution test. The engine must report this as `editorial concern` with a cited opening/ending pair; it must not "repair" the issue by forcing a conventional three-act structure. Conversely, an experimental novel may intentionally deny closure. A documented authorial contract and human reader evidence can defend the exception; a model cannot silently recategorize it as success.
