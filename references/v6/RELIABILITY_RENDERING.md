# Reliability Rendering

**How a result object becomes a line a reader can check.**

[`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) defines the four reliability types and how to write one line of output without violating them. This document is the v6 continuation: the types are closed into an enum, the prohibition on coercion between them is made constitutional, omission becomes an object rather than an absence, and the rules extend from a terminal report to five other places a result is read — a table, a UI margin, a slide, a capsule and a release manifest.

Every v5 rule is carried forward unamended. Nothing below relaxes one.

The rule underneath all of it is unchanged: **the basis names how the result was produced, never how sure anyone is.** Certainty is not a basis. Production method is.

---

## Table of contents

1. The `ReliabilityBasis` enum and the coercion prohibition
2. Denominators, and the green badge
3. Declared omission
4. The five disclosure states
5. Rendering in prose
6. Rendering in a table
7. Rendering in a UI margin
8. Rendering in a slide
9. Rendering in a capsule
10. Rendering in a release manifest
11. Realm preservation
12. Model self-drift
13. Forbidden constructions at v6
14. What is executable and what is specified

---

## 1. The `ReliabilityBasis` enum and the coercion prohibition

**Status: specified as a closed enum; the four values are executable as v5 reliability types in `scripts/wi.py`.**

v5 named four reliability types. v6 closes them into an enum with no open variant, no `other`, no `custom` and no numeric ordering:

```
ReliabilityBasis :=
    Verified        — a deterministic comparison executed and passed
  | Measured        — a quantity computed against a stated baseline with a visible denominator
  | Judged          — a reasoned assessment by a named provider, with no external comparison behind it
  | HumanDeclared   — a named human actor asserting something on their own authority
```

Four values. There is no fifth, and the absence of a fifth is deliberate: every proposal for one has been a request for a category that means *somewhat verified*, and there is no such production method.

### 1.1 The prohibition

> **No basis may be coerced into another. Not by a renderer, not by an aggregator, not by a merge, not by a policy, not by an import, and not by a flag.**

This is Law K seen from the output side, and it forbids six specific moves:

| Coercion | What it looks like in practice |
|---|---|
| `Judged` → `Verified` | A model's entailment result rendered with the word `verified`, or with the check glyph the verified renderer uses |
| `Measured` → `Verified` | A metric that passed a threshold rendered as a passed check |
| `HumanDeclared` → `Verified` | An author's attestation rendered as though the system compared it to something |
| `Verified` → `Measured` | A deterministic pass rendered as a percentage or a score |
| Any → a composite | Four bases averaged, weighted or summed into one number |
| Any → a colour | Four bases collapsed into green, amber and red |

**Why the enum is closed rather than extensible.** An extensible basis set means the first integrator with an unusual check adds a value, and the value has no rendering rule, and the renderer falls back to something — almost always the one that looks most authoritative, because that is what a fallback tends to be styled as. A closed enum makes the addition a constitutional amendment under [`CONSTITUTION.md`](CONSTITUTION.md) §10 rather than a pull request, which is the correct weight for a change that alters what every reader in the system is being told.

**Why there is no ordering.** `Verified` is not *better* than `HumanDeclared`. They answer different questions. A deterministic comparison can confirm that a quotation matches a source and can say nothing about whether the author was in the room; a human attestation can say the author was in the room and can be compared to nothing. An ordering invites a `max()`, and a `max()` over bases is the composite score in one line of code.

### 1.2 The one legal transformation

A basis may be **narrowed to a refusal**. A result that was `Verified` and whose closure has since moved does not become `Judged` or `Measured` — it becomes *not currently verified*, with `invalidated_by_edit` naming what moved. That is the only transformation, it always loses information, and it never crosses into another basis.

---

## 2. Denominators, and the green badge

**Status: `wi gate` renders counts with their population; the badge rules are specified.**

### 2.1 Every count carries a visible denominator

A number without a denominator reads as precision and carries none. The reader cannot ask *out of what*, so they assume it was measured over everything.

**Right:**

```
9 of 14 factual claims carry a resolvable anchor (64%)
denominator: factual claims extracted from draft.md at state sha256:71b4e8…
excluded: 3 rhetorical, 2 hypothetical (realm-tagged, not counted as factual)
```

**Wrong:**

```
64% of claims verified
```

The second sentence is not shorter than the first in the way that matters. It has dropped the population, the state binding and the exclusions — which is to say it has dropped everything a second reader would need to get the same number.

`wi gate` does this today. The header line reads `Evidence mode: strict · 4 claims · 2 readable source(s)`, and the status table lists every claim by status with a count, so the denominator is on the page rather than implied.

### 2.2 Why `98.7% of semantic nodes provably unaffected` is legitimate

It names a population (semantic nodes), a method (provably — a dependency walk that terminated), and a specific property (unaffected by this change). It is falsifiable: a reader can re-run the walk and get the same number, and can name a node they believe was reached in order to contest it. It is a `Measured` line, and it renders as one.

### 2.3 Why `98.7% healthy` is not

There is no population — *healthy* is not a set anything belongs to. There is no method — nothing computes health. There is no property — the number cannot be contested, because there is no claim in it to disagree with. And there is no basis: the number is a composite of at least four incompatible things, which the enum in §1 exists to prevent.

The difference between the two sentences is not tone. The first is a measurement of a stated set; the second is a mood with a decimal point.

### 2.4 The green badge

> **A green badge is the most dangerous element in the system.**

Six properties make it so, and they compound:

1. **It compresses to a single bit** a result that has a basis, a population, a state binding, a closure and five disclosure states.
2. **It survives screenshots.** A badge is the part of a report that leaves the system, and it leaves without the disclosure block, without the state digest and without the date.
3. **It does not go stale visibly.** The closure moves, the claim becomes `invalidated_by_edit`, and the screenshot in the shared document is still green.
4. **It is read as a claim about the world.** *Verified* to a reader outside this project means *true*. Inside it means *a comparison against supplied sources executed and matched*.
5. **It has no denominator.** A badge over eleven claims and a badge over one look identical.
6. **It is the element every stakeholder asks for**, which means it is the element most likely to be added by someone who has not read this document.

**The rules, if a badge exists at all:**

- It renders the **basis**, never a verdict — `Verified` rather than a checkmark, and never a bare glyph.
- It renders the **fraction**, not a colour alone — `9/14 Verified`.
- It renders the **state binding**, at minimum a truncated digest, so a stale screenshot is identifiable as one.
- It is **not clickable-through-to-nothing**: a badge that does not open the Proof Inspector is decoration, and decoration in this position is a claim.
- It is **absent, not amber, when nothing ran.** An amber badge says a check ran and was unhappy. A missing check is `unavailable_on_surface` and renders as §3, which is a different sentence.

---

## 3. Declared omission

**Status: `wi doctor` renders declared omissions with per-entry reasons today; the structured object below is specified.**

An omission is an object, not an absence.

```json
{
  "kind": "judgment.entailment",
  "status": "unavailable_on_surface",
  "reason": "offline verifier profile contains no judgment provider"
}
```

**Why this is strictly stronger than a missing field.** A missing field has exactly one rendering and three possible meanings, and the reader cannot distinguish them:

| The reader sees | It might mean |
|---|---|
| nothing | the check ran and found nothing to report |
| nothing | the check could not run here |
| nothing | this build has no concept of that check |

The third is the one that ends careers quietly: a report produced by a version that never had entailment checking looks identical to a report produced by a version that had it and ran it clean. A declared omission separates all three, and it does so in a form a machine can act on — a downstream policy can require that every `unavailable_on_surface` entry be closed before a regulated release, which it cannot do against an absence.

**The three fields are all required.**

- **`kind`** names what was omitted, from the same vocabulary the check registry uses. Not prose. A reader deciding whether to change surfaces needs the identifier, not a description of it.
- **`status`** is one of the five disclosure states in §4. Nothing else.
- **`reason`** is a sentence a person can act on. *"no judgment provider configured"* tells the reader what to install. *"unavailable"* tells them nothing and reads as an apology.

`wi doctor` renders this today, in prose, under a heading that states the rule rather than the outcome:

```
Not available here — and therefore never reported as done:
  audio_time             adapter specified, not executable in this build
  external_signing       Sigstore and C2PA paths are specified, not executable
  image_region           adapter specified, not executable in this build
  paraphrase_entailment  no judgment provider is configured
  pdf_region             adapter specified, not executable in this build
  sheet_range            adapter specified, not executable in this build
  video_time             adapter specified, not executable in this build
```

Each line carries a `kind` and a `reason`. The v6 addition is the `status` field and the machine-readable form, so that the same information survives a pipe, a capsule and an API response rather than only a terminal.

---

## 4. The five disclosure states

**Status: `ran_deterministic` and `unavailable_on_surface` have producers in `scripts/wi.py`; the five-state structured block on every result object is specified.**

The vocabulary is fixed by Law C and unchanged from v5. Every result object carries all five, and empty states are stated as empty rather than omitted.

| State | Means | The reader's next move |
|---|---|---|
| `ran_deterministic` | A stranger can re-run this and get the same answer | Re-run it if you doubt it |
| `ran_judgment` | A stranger can read the record and disagree with it | Read the passage and form your own view |
| `unavailable_on_surface` | This can be checked, elsewhere | Change surfaces |
| `disabled_by_policy` | Someone chose this | Ask who, and why |
| `invalidated_by_edit` | This *was* checked and the answer no longer applies | Re-run it — and the badge you saw earlier is now wrong |

**Why five rather than "checked" and "not checked."** The four not-checked states carry four different obligations, and collapsing them hides a decision inside a limitation. `disabled_by_policy` is a person's choice; `unavailable_on_surface` is a property of where you are standing; `invalidated_by_edit` means the report you are holding was true and is not. A reader who cannot tell those apart cannot act on any of them.

**Empty states are stated.** A block with no `unavailable_on_surface` line and a block from a system that has no concept of unavailability look identical, and only one of them was honest. This is §3's argument applied to the block itself.

**What has a producer today.** `scripts/wi.py` emits a reduced form: `gate` prints a checks-run line and a not-run line, the claim ledger carries a `checks_not_run` field, and `doctor` renders the declared-omission list above. `disabled_by_policy` and `invalidated_by_edit` have no producer at v5.0.1 and are specified. Saying so is the point of the section.

---

## 5. Rendering in prose

**Status: `Verified`, `Measured` and `HumanDeclared` executable in `scripts/wi.py`; `Judged` specified.**

Prose is the reference rendering. Every other context in §§6–10 is a compression of it, and the compression is legitimate only when it drops presentation rather than the fields below.

**`Verified`** names the check, the source, the version and the location.

```
Verified  quotation  c0007
  "median wait times fell by 38%"
  → needs_assessment.txt @ bytes 4180–4214  (source sha256:9f2ac1…, quote sha256:be31d0…)
  check: exact string comparison · engine: deterministic · closure sha256:71b4e8…
```

**`Measured`** carries its denominator in the same breath as its numerator, and names the baseline.

```
Measured  claim coverage
  9 of 14 factual claims carry a resolvable anchor (64%)
  baseline: factual claims extracted from draft.md at state sha256:71b4e8…
  excluded: 3 rhetorical, 2 hypothetical (realm-tagged, not counted as factual)
```

**`Judged`** names its provider before it says anything else.

```
Judged  paraphrase support  c0011
  provider: <named judgment provider> · model: <identifier@version>
  prompt/policy: sha256:1c9d44… · inputs: claim sha256:22ae09…, span sha256:be31d0…
  result: the anchored passage supports the claim with a scope narrowing
  calibration: none published for this task — this is an unbenchmarked judgment
  NOT a deterministic check. Verify by reading the passage.
```

**`HumanDeclared`** names the human.

```
HumanDeclared  author observation  c0003
  attestor: A. Rivera (team_member) · 2026-08-04
  "I ran the intake sessions described in this paragraph."
  covers: draft.md §2 at state sha256:71b4e8… · no external source supplied
```

**The invariant across all four.** Each rendering answers *who or what produced this, over what inputs, at what state, and how would I check it myself.* A rendering that drops any of the four has produced a sentence the reader must take on trust, which is the condition this system exists to remove.

---

## 6. Rendering in a table

**Status: specified.**

A table is the most common compression and the most common place a basis is lost, because a column header is a strong invitation to make every row the same shape.

**The rule: the basis is a column, never a styling.**

| Claim | Basis | Result | Population / provider | State |
|---|---|---|---|---|
| c0007 | `Verified` | quotation matched | needs_assessment.txt sha256:9f2ac1… | sha256:71b4e8… |
| c0011 | `Judged` | supports, with scope narrowing | provider `<name>` model `<id@version>` | sha256:71b4e8… |
| c0003 | `HumanDeclared` | author was present | A. Rivera, 2026-08-04 | sha256:71b4e8… |
| coverage | `Measured` | 9 of 14 (64%) | factual claims in draft.md | sha256:71b4e8… |

**Three rules for tables.**

1. **Never sort by basis in a way that implies rank.** Sort by claim order or by consequence. An ordering that puts `Verified` at the top and `Judged` at the bottom has rendered the prohibited ordering from §1.2 as a layout.
2. **Never use a shared `Result` column with a shared vocabulary.** `pass` in a `Verified` row and `pass` in a `Judged` row are different assertions, and one column of `pass` makes them the same word.
3. **A row with no basis is not rendered.** If the basis is unknown, the row is a declared omission and belongs in the disclosure block, not in the table with an empty cell.

---

## 7. Rendering in a UI margin

**Status: specified.**

The proof margin sits beside the text, and it is the rendering with the least room and the most readers. Every temptation here is to compress further.

**What the margin shows per claim, in order:**

1. The **basis**, as a word.
2. The **result**, in three or four words.
3. A **denominator** where the result is a count.
4. A **state marker** — a truncated closure digest — so a stale view is identifiable.
5. An **affordance** that opens the Proof Inspector.

```
┌─────────────────────────────────────────┐
│ Between 2019 and 2022, the program       │  Verified · quotation
│ served 12,400 households across seven    │  needs_assessment.txt
│ counties, and median wait times fell     │  sha256:71b4e8…            ⓘ
│ by 38%.                                  │
│                                          │
│ The independent evaluator concluded      │  Judged · paraphrase
│ that case management was decisive.       │  provider <name>
│                                          │  unbenchmarked             ⓘ
│                                          │
│ According to Whitfield and Barnes        │  ⊘ citation unresolved
│ (2021), regional capacity programs…      │  repairs: 4                ⓘ
└─────────────────────────────────────────┘
```

**Four margin rules.**

- **The word survives the compression; the glyph does not.** A glyph is a colour with an outline, and §2.4 applies to every one of them. The basis word is four to twelve characters and there is room for it.
- **`Judged` renders its provider in the margin.** Not on hover. A provider name behind a hover is a provider name that does not exist in a screenshot, a printout or a screen reader's default traversal.
- **Unbenchmarked is stated in the margin.** It is the single most decision-relevant fact about a `Judged` line, and it is the first thing dropped for space.
- **A margin with no disclosure block is incomplete.** The block goes at the end of the document, not in the margin, and the margin's presence does not discharge it.

---

## 8. Rendering in a slide

**Status: specified.**

A slide is the least controllable rendering in the system: it is read at distance, from an image, by people who did not run anything, and it outlives the state it was built from by months.

**The slide rules, which are stricter than every other context:**

- **A bare percentage is prohibited on a slide even where it would be legal in prose.** In prose the denominator is on the next line. On a slide the next line is a different slide.
- **Every number carries its population in the same visual unit.** `9 of 14 factual claims` on one line, not `64%` with a footnote.
- **The state binding and the date appear on any slide carrying a result.** A slide is the artifact most likely to be re-shown after the state moved; a truncated digest and a date are what let a viewer ask whether it is current.
- **No composite, no gauge, no traffic light, no dial.** All four are the composite score from §1.1 in a graphical costume, and the graphical costume is more persuasive than the number would have been.
- **A `Judged` result names its provider on the slide.** If there is no room for the provider, there is no room for the result.

**The honest slide when the room wants one number:**

```
  Draft state sha256:71b4e8…  ·  2026-08-04

  14 factual claims
   9  Verified against supplied sources
   2  Judged — unbenchmarked, provider <name>
   1  HumanDeclared — author observation
   2  unresolved: 1 citation, 1 figure

  Nothing on this slide is a claim about whether the sources are correct.
```

Five lines, no composite, and every number has its population beside it. The room that wanted one number gets four and can act on all of them.

---

## 9. Rendering in a capsule

**Status: `verify-release` executable in `scripts/wi.py`; capsule rendering specified.**

A capsule is read by someone who has none of the context and cannot ask a question. Its rendering carries two things nothing else has to: the **profile** it was built at, and the **withheld set**.

```
Capsule review.wicap · profile `redacted` · built from root sha256:c31f07…

  Verified        11 checks reproduced from carried source versions
  Measured         1 coverage figure, denominator carried
  Judged           0 — no judgment records in this capsule
  HumanDeclared    6 decision records, each bound to its target state

  Withheld under this profile (3):
    source.body      needs_assessment.txt   commitment carried, bytes withheld
    source.body      internal_memo.txt      commitment carried, bytes withheld
    decision.reason  d0004                  commitment carried, text withheld

  Inclusion proofs verify for all 3 withheld leaves.

  This confirms the record is intact and untampered.
  It does not confirm the sources are correct.
```

**Three capsule rules.**

1. **A withheld leaf is rendered, never omitted.** Withheld and absent are different facts and only one of them means the evidence does not exist. A capsule reader who sees eleven rows where a fuller profile has fourteen, with no statement that three were withheld, has been given a false impression of completeness by a renderer that thought it was being tidy.
2. **`Judged 0` is rendered.** Zero is a result. Removing the row makes a capsule with no judgment records indistinguishable from a build that has no judgment concept.
3. **The scope sentence is part of the output.** Not a footer, not documentation. It is the sentence that prevents *the capsule verified* from being read as *the claims are true*, and it must survive being printed on paper.

---

## 10. Rendering in a release manifest

**Status: `bundle` and `verify-release` executable in `scripts/wi.py`; the v6 manifest fields are specified.**

A manifest is machine-first and human-second, and the human reading it is usually deciding whether to ship.

```json
{
  "wi": "6.0.0",
  "built_from": "sha256:c31f07…",
  "target": "release/regulated",
  "verdict": "HOLD",
  "bases": {
    "verified":       { "count": 11, "population": 14 },
    "measured":       { "count": 1,  "population": 1 },
    "judged":         { "count": 0,  "population": 14 },
    "human_declared": { "count": 6,  "population": 6 }
  },
  "obligations": { "met": 7, "unmet": 1, "waived": 0 },
  "disclosure": {
    "ran_deterministic": ["quotation", "numeric", "date", "citation.resolution"],
    "ran_judgment": [],
    "unavailable_on_surface": [
      { "kind": "judgment.entailment", "status": "unavailable_on_surface",
        "reason": "offline verifier profile contains no judgment provider" }
    ],
    "disabled_by_policy": [
      { "kind": "source.fetch", "status": "disabled_by_policy",
        "reason": "project policy: offline only" }
    ],
    "invalidated_by_edit": []
  },
  "signing": null
}
```

**Four manifest rules.**

- **Every basis carries both a count and a population.** `judged: 0 of 14` is a different statement from `judged: 0 of 0`, and a manifest that carries only the count cannot distinguish them.
- **`signing: null` rather than an omitted field.** An absent key reads as *not applicable*. `null` reads as *this was not done*, which is the true thing — there is no signing implementation anywhere in this repository.
- **The disclosure block is structured here, not prose.** A manifest is consumed by policy engines, and a policy that must require the closure of every `unavailable_on_surface` entry needs objects to iterate, not a paragraph to parse.
- **`verdict` is not a basis.** `HOLD` is a policy outcome computed from bases and obligations. Rendering it in the `bases` object, or rendering a basis in the verdict field, collapses the two — and the collapse is what produces a manifest where *verified* and *approved to ship* are the same word.

---

## 11. Realm preservation

**Status: realm tagging executable in `scripts/wi.py`; realm-aware rendering specified.**

The six epistemic realms — `external_fact`, `author_observation`, `fictional_canon`, `hypothetical`, `simulation`, `rhetorical` — are carried forward from v5 unchanged. The v6 addition is a rendering rule.

> **A check verified inside `fictional_canon` must never render as externally verified fact.**

A canon check is a real, deterministic, reproducible comparison. It confirms that a statement is consistent with the supplied canon — that the character's eye colour matches the bible, that the timeline holds, that the invented statute says what the scene says it says. It is `Verified`, correctly, and the basis is not the problem.

The problem is the sentence a reader constructs when the realm is dropped:

| Rendered | Read as |
|---|---|
| `Verified · quotation · c0042` | This is true of the world |
| `Verified · quotation · c0042 · realm: fictional_canon` | This is consistent with the invented material |

The two are the same check. Only one of them can be pasted into a factual document without becoming a false claim.

### 11.1 The rule

**The realm marker is not metadata a renderer may drop for space.** It travels with the basis in every context in §§5–10 — prose, table, margin, slide, capsule and manifest — and a rendering that has room for `Verified` has room for the realm.

The three realms this bites hardest on:

- **`fictional_canon`** — the check is rigorous and the subject is invented. Dropping the realm converts a canon-consistency result into a claim about the world.
- **`simulation`** — a figure verified against a model's output is verified against a model's output. Dropping the realm makes a projection read as a measurement of something that happened.
- **`hypothetical`** — a claim inside a conditional. Dropping the realm strips the condition and leaves the consequent standing alone, which is the most common way a careful sentence becomes a false one.

`author_observation` and `rhetorical` matter too, and matter less, because both usually render into surrounding text that carries the frame. `external_fact` is the only realm whose omission is harmless, and it is harmless only because it is the one every reader assumes.

### 11.2 Realm mixing in a count

A count that mixes realms is a `Measured` line with an incoherent population. The exclusions belong in the denominator statement, which is why the coverage example in §5 says `excluded: 3 rhetorical, 2 hypothetical (realm-tagged, not counted as factual)` rather than silently filtering them. A reader who disagrees with the exclusion can see it and argue with it; a reader looking at a filtered number cannot see that filtering happened.

---

## 12. Model self-drift

**Status: specified.**

A judgment provider changes underneath its callers. The same model identifier answers differently after a provider-side update; a new version answers differently by design. v5's [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) requires every `Judged` record to carry the model identifier and version so that a change is visible. v6 adds the rendering rule for what happens when someone measures the change.

**The measurement.** Run one provider against itself across two versions, on identical hashed inputs — the same claim digests, the same span digests, the same prompt/policy hash — and count how many results differ.

**What that produces:**

```
Measured  provider self-drift
  provider <name> · model <id@2026-06> vs <id@2026-08>
  inputs: 412 judgment requests, identical claim and span digests, identical prompt/policy sha256:1c9d44…
  differing results: 37 of 412 (9.0%)
  direction: 22 became more supportive, 15 less
  baseline: this workspace's judgment corpus at state sha256:71b4e8…
```

That is a `Measured` line. It has a population (412 requests), a method (identical hashed inputs across two versions), a stated baseline, and a number a reader can contest by re-running it.

**What it may never produce.**

> **A case-level confidence number.**

The forbidden rendering is the one everybody wants:

```
Judged  paraphrase support  c0011
  confidence: 91%          ← prohibited
```

A 9% population drift rate says nothing about claim `c0011`. It is a property of the corpus, not of the case. Rendering it beside a single result invents a per-case probability out of an aggregate, and it does so in the direction that makes the result look firmer than the record supports — which is the direction of every failure this document exists to stop.

**The three sub-rules:**

1. **Self-drift is reported at the population level with its denominator, or not at all.**
2. **It never modifies a `Judged` record.** The record carries its own provider, model, version and inputs. A drift measurement is a separate `Measured` object that references the corpus, not the case.
3. **It is never coerced into a calibration.** Calibration compares a provider's outputs against known-correct answers. Self-drift compares a provider against itself, where neither side is known to be correct, and a system with a high self-agreement rate may simply be consistently wrong. Rendering self-drift where calibration belongs is the `Measured` → `Verified` coercion from §1.1 with an extra step.

---

## 13. Forbidden constructions at v6

**Status: specified.**

v5's six forbidden constructions are carried forward in full: a bare percentage, *"high confidence"*, *"AI-verified"*, a blended composite score, cosine similarity presented as support, and *"fact-checked"* without naming which checks ran. Each is banned for the reason stated in [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) §3, and the reasons are worth more than the list, because they catch the variants the list does not name.

v6 adds six, all of which become possible only because v6 has state, authority, time and federation:

| Construction | Why it is forbidden |
|---|---|
| **"Verified as of today"** with no state digest | *Today* is not a state binding. The closure moves within the day, and a reader six weeks on cannot recover which state was meant. Print the digest. |
| **"Approved"** used for a gate result | A gate reads verdicts; it does not approve. Approval is a `HumanDeclared` act by a named actor holding a live grant, and a pipeline has neither. |
| **"Verified by <organization>"** for imported state | A remote's verdict is not a local verdict. The evidence travels in a capsule; the verdict does not. Render it as an import record with the remote's assertion named as theirs. |
| **A trend line across bases** | *Verification is improving* over a chart that mixes `Verified`, `Judged` and `HumanDeclared` counts is the composite score with a time axis. Chart one basis or none. |
| **"Auto-verified"** or **"agent-verified"** | An autonomous agent holds no write capability and cannot produce a verification record. The compound word claims an actor that constitutionally cannot act. |
| **A conflict rendered as a single value** | Where a merge preserved two sides, rendering one is a decision the system did not make. Render both, marked unresolved. See [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md). |

**The pattern connecting all twelve.** Each one moves information *out* of the output while making the output look stronger. That is the direction of every failure this document exists to stop, and it is the test to apply to a construction not on either list: **a rendering that looks more authoritative and says less is always the wrong one.**

---

## 14. What is executable and what is specified

**Status: executable in `scripts/wi.py`.**

| Subject | State |
|---|---|
| The four reliability types as v5 types | Executable — `verify`, `gate`, `bundle`, `verify-release` |
| Counts rendered with their population | Executable — `wi gate` header and status table |
| Repairs rendered beside every blocking and holding item | Executable — `wi gate` |
| Declared omissions with per-entry reasons | Executable — `wi doctor` |
| `ran_deterministic` and `unavailable_on_surface` | Executable — `gate`, the ledger's `checks_not_run` field, `doctor` |
| Realm tagging on claim atoms | Executable |
| Machine rendering of a verified release | Executable — `verify-release --json` |
| `ReliabilityBasis` as a closed enum | Specified |
| The five-state disclosure block on every result object | Specified — two of five states have producers today |
| `disabled_by_policy` and `invalidated_by_edit` | Specified — no producer at v5.0.1 |
| The declared-omission object with `kind`, `status`, `reason` | Specified — the prose form runs; the structured form does not |
| Table, margin, slide, capsule and manifest renderings | Specified |
| Realm-aware rendering rules | Specified |
| Model self-drift measurement | Specified — no judgment provider exists anywhere |
| The v6 forbidden constructions | Specified |

**The honest summary.** What runs today renders two of the four bases with their populations and their repairs, and states plainly what it could not do. Everything about margins, slides, capsules and drift is written down and does not run. That distinction is the document's own subject applied to itself.

---

Read next:

- [`../v5/RELIABILITY_TYPES.md`](../v5/RELIABILITY_TYPES.md) — the four types in full, and the six v5 forbidden constructions
- [`CONSTITUTION.md`](CONSTITUTION.md) — Law C, Law K and Law R
- [`SURFACES.md`](SURFACES.md) — the result object these renderings derive from
- [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) — profiles, withheld sets and inclusion proofs
- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — why an unresolved conflict renders as two values
- [`NON_GOALS.md`](NON_GOALS.md) — why there is no overall health gauge
- [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) — what a `Judged` record must carry

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
