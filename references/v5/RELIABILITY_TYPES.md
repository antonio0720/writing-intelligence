# Reliability Types

The operational manual for the four reliability types. [`CONSTITUTION.md`](CONSTITUTION.md) declares them; this document is how you actually write a line of output without violating them.

**Status: `verified` and `human-declared` executable in `scripts/wi.py`; `measured` partially executable; `judged` specified and unimplemented.**

Read this before rendering any proof output, on any surface, in any format — a report, a table, a badge, a JSON record, a sentence in a chat message.

The rule underneath all of it: **the type names how the result was produced, never how sure anyone is.** Certainty is not a type. Production method is.

---

## Table of contents

1. The definition table
2. Rendering each type
3. Forbidden constructions
4. The mandatory disclosure block
5. Degradation across surfaces

---

## 1. The definition table

| Type | What produces it | What invalidates it | What it may never be rendered as |
|---|---|---|---|
| `verified` | A deterministic comparison that executed and passed — a quote matched byte-for-byte against an anchored span, a figure matched against a source figure, a date matched, a citation resolved to a supplied source | Any change to the source state, the anchor, the claim atom, or the transformation chain, unless the engine can prove the dependency is unaffected (Law I) | A confidence level · a percentage · "true" · "accurate" · a claim about the world rather than about the supplied sources |
| `measured` | A quantity computed against a stated baseline with a visible denominator — counts over a defined set, length against a stated limit, voice metrics against a supplied sample set, a calibration result against a published benchmark | A change to the baseline, the denominator, the sample set, or the population being measured; a metric computed on text the metric does not apply to | A bare number · a score without its rubric · a measurement transplanted to a different baseline · `verified` |
| `judged` | A reasoned assessment by a named provider with no external comparison behind it — paraphrase support, entailment, craft quality, structural coherence, persuasive force | A change to any input hash, the prompt/policy hash, the model identifier, or the claim being judged; a provider swap | `verified` · a percentage · "high confidence" · an unattributed statement · anything that omits the provider's name |
| `human-declared` | A named human actor asserting something on their own authority — an author's own observation, a reviewer's sign-off, a subject-matter attestation | Retraction by the attestor; a change to the text the declaration covers; expiry of a stated review period | `verified` · an anonymous assertion · a consensus · a claim the attestor did not personally make |

**Why the table is load-bearing.** Every column is a failure someone will attempt. The "what invalidates it" column is the one people forget, because invalidation happens later — after the report was read, after the badge was screenshotted, after the sentence was edited. The "may never be rendered as" column exists because most violations are not lies; they are formatting choices that mean something the record does not say.

---

## 2. Rendering each type

Each type has a shape. The shape carries the information that makes the line checkable by someone who was not there.

### `verified`

A `verified` line names the check, the source, the version and the location.

**Right:**

```
verified  quotation  c0007
  "median wait times fell by 38%"
  → needs_assessment.txt @ bytes 4180–4214  (source version sha256:9f2ac1…, quote digest sha256:be31d0…)
  check: exact string comparison · engine: deterministic · current as of state sha256:71b4e8…
```

**Wrong:**

```
[green check glyph] Verified (98% confidence) — figure confirmed accurate.
```

Wrong five times over. The check glyph asserts a completed process the reader cannot inspect. A percentage on a deterministic comparison is meaningless — the comparison either matched or it did not. "Confirmed" implies the world was consulted. "Accurate" is a claim about truth, and this system checks support within supplied sources, never truth. And nothing in the line lets a reader find the source passage.

### `measured`

A `measured` line carries its denominator in the same breath as its numerator, and names the baseline.

**Right:**

```
measured  claim coverage
  9 of 14 factual claims carry a resolvable anchor (64%)
  denominator: factual claims extracted from draft.md at state sha256:71b4e8…
  excluded: 3 rhetorical, 2 hypothetical (realm-tagged, not counted as factual)
```

**Wrong:**

```
Evidence quality: 78/100
```

There is no denominator, no rubric, no population and no way to reproduce it. It is a number wearing the costume of a measurement. If a rubric exists, publish it and show the inputs; if one does not, this is a `judged` line and must say so.

### `judged`

A `judged` line names its provider before it says anything else.

**Right:**

```
judged  paraphrase support  c0011
  provider: <named judgment provider> · model: <identifier@version>
  prompt/policy: sha256:1c9d44… · inputs: claim sha256:22ae09…, span sha256:be31d0…
  result: the anchored passage supports the claim with a scope narrowing
  calibration: none published for this task — this is an unbenchmarked judgment
  NOT a deterministic check. Verify by reading the passage.
```

**Wrong:**

```
AI-verified: this claim is supported by the source.
```

Wrong in the compound word itself. `verified` is a production method that a judgment cannot use, and prefixing it with the tool does not repair it — it makes the violation sound like a feature. There is also no provider, no inputs, no way to contest it and no statement that the result is unbenchmarked.

Nothing in this repository emits `judged` records today. The judgment tier is not implemented. This section binds the implementation when it arrives.

### `human-declared`

A `human-declared` line names the human.

**Right:**

```
human-declared  author observation  c0003
  attestor: A. Rivera (team_member) · 2026-08-04
  "I ran the intake sessions described in this paragraph."
  covers: draft.md §2 at state sha256:71b4e8… · no external source supplied
```

**Wrong:**

```
Verified by the team.
```

No named attestor, no date, no scope, no state binding, and the word `verified` used for an assertion nobody compared to anything. "The team" cannot be asked what they meant, and cannot retract.

---

## 3. Forbidden constructions

Each of these is banned outright. The reason matters more than the ban — memorize the reason and you will catch the variants this list does not name.

| Construction | Why it is forbidden |
|---|---|
| **A bare percentage** — "87% confident", "92% accurate" | A number with no denominator reads as precision and carries none. It is the fake-authority pattern the v3 doctrine already names, applied to evidence. The reader cannot ask *out of what*, so they assume it was measured. |
| **"High confidence"** | Confidence is not a reliability type and describes a feeling, not a production method. It is used almost exclusively where a `judged` result is being dressed as something firmer. Say `judged`, name the provider, and let the reader weigh it. |
| **"AI-verified"** | Compounds the one word that names deterministic production with the one actor that cannot produce it. It also credits a model as the agent of verification. Models are third-party infrastructure named in a record — never verifiers, never authors. |
| **A blended composite score** | Averaging across types destroys the only information the types carry. Once a string comparison, a benchmark measurement, a model opinion and an author assertion are one number, no one — including its author — can decompose it. The mix is exactly what the reader needed. |
| **Cosine similarity presented as support** | Embedding proximity measures distributional similarity, not entailment. Two sentences with opposite meanings sit close in embedding space; a negation barely moves the vector. Retrieval scores are for finding candidates, never for proving support. See [`NON_GOALS.md`](NON_GOALS.md). |
| **"Fact-checked" without naming which checks ran and which did not** | The phrase implies a complete and unspecified process. It is a Law C violation in two words: it reports work whose extent the reader cannot determine, and it will be read as covering the checks that did not run. Every use must be replaced with the disclosure block below. |

**The pattern connecting all six:** each one moves information *out* of the output while making the output look stronger. That is the direction of every failure this document exists to stop. A construction that looks more authoritative and says less is always the wrong one.

---

## 4. The mandatory disclosure block

**Status: executable in `scripts/wi.py`.**

Every proof output carries a disclosure block. Not an appendix — part of the output, adjacent to the result. Five sections, and empty sections are stated as empty rather than omitted.

```
## Checks

Ran (deterministic):     quotation · numeric · date · citation resolution · anchor resolution
Ran (judgment):          none — no judgment provider configured on this surface
Unavailable here:        PDF region anchors (no binary decoder) · audio interval anchors
Disabled by policy:      external citation lookup (project policy: offline only)
Invalidated by edits:    c0004, c0009 — source needs_assessment.txt changed after these
                         were checked; run `wi impact` for the repair frontier
```

**Why it is load-bearing.** These five states are not five ways of saying "no." They carry different obligations for the reader:

- **Ran (deterministic)** — a stranger can re-run this and get the same answer.
- **Ran (judgment)** — a stranger can read the record and disagree with it.
- **Unavailable here** — this can be checked, on a different surface. The reader's move is to change surfaces.
- **Disabled by policy** — someone chose this. The reader's move is to ask who and why.
- **Invalidated by edits** — this *was* checked and the answer no longer applies. The reader's move is to re-run it, and the badge they may have seen earlier is now wrong.

Collapsing them into "not checked" hides a decision inside a limitation. Omitting the empty sections is worse: a block with no "unavailable" line and a block that never had an "unavailable" concept look identical, and only one of them was honest.

The exact vocabulary of the five states is fixed by Law C in [`CONSTITUTION.md`](CONSTITUTION.md).

---

## 5. Degradation across surfaces

**Status: executable in `scripts/wi.py` via `wi doctor` where a filesystem exists; surface self-report otherwise.**

The types do not change meaning across surfaces. What changes is which of them a surface can legitimately produce.

| Surface | Can produce | Cannot produce |
|---|---|---|
| Terminal agent with a workspace | `verified` · `measured` · `human-declared` | `judged` (not implemented anywhere) |
| Cowork with filesystem and shell | `verified` · `measured` · `human-declared` | `judged` |
| CI | `verified` · `measured` | `human-declared` (no human present) · `judged` |
| Chat with no filesystem | `human-declared` (the author's own, quoted) | **`verified`** · `measured` · `judged` |
| Air-gapped review of a `.wiab` | `verified` (re-checked from the bundle) · `measured` | `judged` |

**The chat rule is the one that gets broken.** In a chat with no filesystem, `scripts/wi.py` does not exist and did not run. Careful reading happened. Careful reading is genuinely valuable and it is not mechanical verification, and the difference is not pedantry — a mechanical check does not get tired on page 40 and returns the same answer next week, and reading does neither.

**Right, in chat:**

> No workspace on this surface, so no mechanical check ran. I read the three claims against the passages you pasted and matched the figures by eye: claim 2's figure (12,400) does not appear in your text, which says 11,800. Treat that as a careful reading, not a verified result. On a filesystem, `wi verify` would settle it by string comparison.

**Wrong, in chat:**

> [green check glyph] Verified — 2 of 3 claims supported.

The glyph, the word and the count all assert machinery that was not present. This is the easiest Law C violation in the whole system to commit by accident, because it happens by *habit* — by carrying a terminal-shaped output into a surface that cannot back it.

**A surface must never imply a capability it lacks, and must say plainly what is missing and where it is available.** Full treatment, surface by surface, with the capability negotiation format: [`SURFACES.md`](SURFACES.md).

---

Read next:

- [`CONSTITUTION.md`](CONSTITUTION.md) — the laws these types serve
- [`SURFACES.md`](SURFACES.md) — Law C as protocol
- [`NON_GOALS.md`](NON_GOALS.md) — why similarity scores are not evidence
- [`../v4/ACCOUNTABILITY_LAYER.md`](../v4/ACCOUNTABILITY_LAYER.md) — the v4 reliability language these types extend
- [`../v4/LANGUAGE_TIERS.md`](../v4/LANGUAGE_TIERS.md) — when a `measured` metric is unavailable rather than zero
